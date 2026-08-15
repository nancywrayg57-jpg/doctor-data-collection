from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import shutil
import tempfile
from collections import Counter, defaultdict
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

import collect_official_doctors_batch as collector
import generate_obsidian_profiles as profiles


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
SOURCE_DIR = ROOT / "医生画像仓库" / "99_资料来源"
PROFILE_ROOT = ROOT / "医生画像仓库" / "01_试点医院"
MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_PAYLOAD = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_REPORT = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
LEDGER = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"
CLEANUP_REPORT = ROOT / "docs" / "2026-08-15_issue_53_治理清理对账报告.md"
CELL_DIFF_CSV = ROOT / "docs" / "2026-08-15_issue_53_逐单元格差异.csv"
SAME_NAME_REPORT = ROOT / "docs" / "同名待甄别辅助表.md"

TARGET_HOSPITALS = (
    "中山大学附属第五医院",
    "中山大学中山眼科中心",
    "南部战区空军医院",
    "中山大学肿瘤防治中心",
    "中山大学附属第三医院",
)
NAVIGATION_WARNING = "亮眼经历含导航文本，已清洗"
ALLOWED_ROW_COLUMNS = {"亮眼经历线索", "异常提示", "已建画像"}
NAVIGATION_RESIDUAL_PATTERNS = (
    re.compile(r"首页\s*(?:/|>|＞|»|›|→)"),
    re.compile(r"(?:临床科室|内科系列|外科系列|平台科室)\s*(?:/|>|＞|»|›|→)"),
)


def clean(value: Any) -> str:
    return collector.clean_text(str(value or ""))


def sha256_file(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest().upper()}


def manifest_hash(
    root: Path,
    hospitals: Iterable[str],
    marker_filter: bool | None = None,
) -> dict[str, Any]:
    digest = hashlib.sha256()
    file_count = 0
    byte_count = 0
    for hospital in sorted(hospitals):
        hospital_dir = root / hospital
        if not hospital_dir.exists():
            continue
        for path in sorted(hospital_dir.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            is_auto = profiles.AUTO_MARKER in text
            if marker_filter is not None and is_auto != marker_filter:
                continue
            relative = path.relative_to(root).as_posix().encode("utf-8")
            content = path.read_bytes()
            digest.update(relative)
            digest.update(b"\0")
            digest.update(hashlib.sha256(content).digest())
            file_count += 1
            byte_count += len(content)
    return {
        "files": file_count,
        "bytes": byte_count,
        "sha256": digest.hexdigest().upper(),
    }


def row_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def normalized_row(row: dict[str, Any]) -> dict[str, str]:
    return {header: row_value(row.get(header)) for header in collector.BASE_HEADERS}


def compare_layers(
    payload_rows: list[dict[str, Any]],
    csv_rows: list[dict[str, Any]],
    xlsx_rows: list[dict[str, Any]],
) -> None:
    if not (len(payload_rows) == len(csv_rows) == len(xlsx_rows)):
        raise RuntimeError(
            f"总底表分层行数不一致：payload={len(payload_rows)}、CSV={len(csv_rows)}、XLSX={len(xlsx_rows)}"
        )
    for index, (payload_row, csv_row, xlsx_row) in enumerate(
        zip(payload_rows, csv_rows, xlsx_rows, strict=True),
        start=2,
    ):
        expected = normalized_row(payload_row)
        if normalized_row(csv_row) != expected:
            raise RuntimeError(f"payload 与 CSV 在底表第 {index} 行不一致")
        if normalized_row(xlsx_row) != expected:
            raise RuntimeError(f"payload 与 XLSX 在底表第 {index} 行不一致")


def load_current_layers() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(MASTER_PAYLOAD.read_text(encoding="utf-8"))
    rows = payload.get("rows")
    if not isinstance(rows, list) or not rows:
        raise RuntimeError("主 payload 缺少有效 rows")
    with MASTER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    xlsx_rows = collector.read_bottom_table_rows(MASTER_XLSX)
    compare_layers(rows, csv_rows, xlsx_rows)
    return payload, rows


def append_warning(value: Any, warning: str) -> str:
    parts = [clean(part) for part in clean(value).split("；") if clean(part)]
    if warning not in parts:
        parts.append(warning)
    return "；".join(parts)


def contains_navigation_residual(value: Any) -> bool:
    text = clean(value)
    return collector.contains_navigation_text(text) or any(
        pattern.search(text) for pattern in NAVIGATION_RESIDUAL_PATTERNS
    )


def apply_navigation_cleanup(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    for row_number, row in enumerate(rows, start=2):
        if clean(row.get("医院")) not in TARGET_HOSPITALS:
            continue
        before = clean(row.get("亮眼经历线索"))
        if not collector.contains_navigation_text(before):
            continue
        after = collector.extract_clean_highlights(before)
        if contains_navigation_residual(after):
            raise RuntimeError(f"导航清洗后仍有残留：底表第 {row_number} 行 {clean(row.get('姓名'))}")
        old_warning = clean(row.get("异常提示"))
        new_warning = append_warning(old_warning, NAVIGATION_WARNING)
        row["亮眼经历线索"] = after
        row["异常提示"] = new_warning
        changes.append(
            {
                "row_number": row_number,
                "sequence": clean(row.get("序号")),
                "hospital": clean(row.get("医院")),
                "name": clean(row.get("姓名")),
                "source": clean(row.get("来源链接")),
                "highlight_before": before,
                "highlight_after": after,
                "warning_before": old_warning,
                "warning_after": new_warning,
            }
        )
    return changes


def profile_sources_by_hospital() -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for hospital in TARGET_HOSPITALS:
        existing = profiles.extract_existing_sources(PROFILE_ROOT / hospital)
        result[hospital] = {
            collector.canonical_url(source)
            for source in existing
            if collector.canonical_url(source)
        }
    return result


def apply_profile_backfill(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], Counter[str], Counter[str]]:
    sources = profile_sources_by_hospital()
    changes: list[dict[str, Any]] = []
    missing = Counter()
    existing = Counter()
    for row_number, row in enumerate(rows, start=2):
        hospital = clean(row.get("医院"))
        if hospital not in TARGET_HOSPITALS:
            continue
        source = collector.canonical_url(clean(row.get("来源链接")))
        has_profile = bool(source and source in sources[hospital])
        if has_profile:
            existing[hospital] += 1
        else:
            missing[hospital] += 1
        before = clean(row.get("已建画像"))
        if before or not has_profile:
            continue
        row["已建画像"] = "是"
        changes.append(
            {
                "row_number": row_number,
                "sequence": clean(row.get("序号")),
                "hospital": hospital,
                "name": clean(row.get("姓名")),
                "source": clean(row.get("来源链接")),
                "before": before,
                "after": "是",
            }
        )
    return changes, existing, missing


def recompute_payload(payload: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result["rows"] = rows
    category_counter: Counter[str] = Counter()
    priority_counter: Counter[str] = Counter()
    group_counter: Counter[str] = Counter()
    warning_counter: Counter[str] = Counter()
    for row in rows:
        department = collector.first_nonempty(
            clean(row.get("科室_分类页")),
            clean(row.get("科室_列表卡片")),
        )
        if department:
            category_counter[department] += 1
        priority = clean(row.get("重点优先级")) or "普通"
        priority_counter[priority] += 1
        for group in clean(row.get("重点关注范围")).split("、"):
            if group:
                group_counter[group] += 1
        for warning in clean(row.get("异常提示")).split("；"):
            if warning:
                warning_counter[warning] += 1
    result["category_counts"] = category_counter.most_common()
    result["priority_counts"] = dict(priority_counter)
    result["group_counts"] = dict(group_counter)
    result["warning_counts"] = dict(warning_counter)
    result["hospital_batches"] = collector.build_hospital_batches(rows)
    meta = result.setdefault("meta", {})
    meta.update(
        {
            "collected_at": date.today().isoformat(),
            "unique_doctor_count": len(rows),
            "existing_profile_count": sum(clean(row.get("已建画像")) == "是" for row in rows),
            "hospital_count": len(result["hospital_batches"]),
            "current_batch_hospital": "Issue #53 存量治理",
            "current_batch_rows": 0,
            "new_rows_added": 0,
            "duplicate_rows_skipped": 0,
            "existing_rows_refreshed": 0,
            "existing_duplicate_rows": 0,
        }
    )
    return result


def collect_cell_diffs(
    before_rows: list[dict[str, Any]],
    after_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if len(before_rows) != len(after_rows):
        raise RuntimeError("治理前后行数发生变化")
    diffs: list[dict[str, Any]] = []
    for row_number, (before, after) in enumerate(zip(before_rows, after_rows, strict=True), start=2):
        for column in collector.BASE_HEADERS:
            old = row_value(before.get(column))
            new = row_value(after.get(column))
            if old == new:
                continue
            diffs.append(
                {
                    "底表行": row_number,
                    "序号": clean(after.get("序号")),
                    "医院": clean(after.get("医院")),
                    "姓名": clean(after.get("姓名")),
                    "来源链接": clean(after.get("来源链接")),
                    "列名": column,
                    "修改前": old,
                    "修改后": new,
                }
            )
    unexpected = sorted({diff["列名"] for diff in diffs} - ALLOWED_ROW_COLUMNS)
    if unexpected:
        raise RuntimeError("发现越界字段修改：" + "、".join(unexpected))
    return diffs


def write_cell_diff_csv(path: Path, diffs: list[dict[str, Any]]) -> None:
    headers = ["底表行", "序号", "医院", "姓名", "来源链接", "列名", "修改前", "修改后"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(diffs)


def normalized_name(value: Any) -> str:
    return re.sub(r"\s+", "", clean(value))


def normalized_compare_text(value: Any) -> str:
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "", clean(value)).lower()


def photo_path(value: Any) -> Path | None:
    relative = clean(value).replace("\\", "/").lstrip("/")
    if not relative:
        return None
    candidate = ROOT / "医生画像仓库" / Path(relative)
    return candidate if candidate.is_file() else None


def specialty_text(row: dict[str, Any]) -> str:
    return clean(row.get("擅长诊疗方向摘录") or row.get("列表简介") or row.get("详情正文摘录"))


def classify_same_name_group(items: list[tuple[int, dict[str, Any]]]) -> tuple[str, str]:
    if len(items) < 2:
        return "疑似不同人", "仅有一条带标记记录，缺少同组对照；按需人工核查陈旧标记"

    rows = [row for _row_number, row in items]
    sources = [collector.canonical_url(clean(row.get("来源链接"))) for row in rows]
    if sources and all(sources) and len(set(sources)) == 1:
        return "疑似同一人", "来源链接完全一致"

    photo_values = [clean(row.get("照片文件")) for row in rows]
    if all(photo_values) and len(set(photo_values)) == 1:
        return "疑似同一人", "照片文件路径完全一致"

    photo_hashes = []
    for row in rows:
        path = photo_path(row.get("照片文件"))
        photo_hashes.append(sha256_file(path)["sha256"] if path else "")
    if all(photo_hashes) and len(set(photo_hashes)) == 1:
        return "疑似同一人", "照片文件内容 SHA-256 完全一致"

    hospitals = {clean(row.get("医院")) for row in rows}
    departments = [normalized_compare_text(row.get("科室_分类页") or row.get("科室_列表卡片")) for row in rows]
    titles = [normalized_compare_text(row.get("职称身份原文") or row.get("职称_关键词")) for row in rows]
    specialties = [normalized_compare_text(specialty_text(row)) for row in rows]
    specialty_pairs = [
        SequenceMatcher(None, specialties[left], specialties[right]).ratio()
        for left in range(len(specialties))
        for right in range(left + 1, len(specialties))
        if specialties[left] and specialties[right]
    ]
    if (
        len(hospitals) == 1
        and all(departments)
        and len(set(departments)) == 1
        and all(titles)
        and len(set(titles)) == 1
        and specialty_pairs
        and min(specialty_pairs) >= 0.72
    ):
        return "疑似同一人", "同院、科室与职称一致，且擅长文本相似度不低于 0.72"

    reasons = []
    if len(hospitals) > 1:
        reasons.append("医院不同")
    if len(set(filter(None, departments))) > 1:
        reasons.append("科室不同")
    if len(set(filter(None, titles))) > 1:
        reasons.append("职称/身份不同")
    if len(set(filter(None, sources))) > 1:
        reasons.append("官方来源链接不同")
    if len(set(filter(None, photo_values))) > 1:
        reasons.append("照片文件不同")
    if not reasons:
        reasons.append("缺少可证明同一人的强一致证据")
    return "疑似不同人", "、".join(reasons)


def md_cell(value: Any, limit: int | None = None) -> str:
    text = clean(value)
    if limit and len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text.replace("|", "\\|").replace("\n", " ")


def build_same_name_report(rows: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    groups: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for row_number, row in enumerate(rows, start=2):
        if "同名待甄别" not in clean(row.get("异常提示")):
            continue
        groups[normalized_name(row.get("姓名"))].append((row_number, row))

    decision_counter: Counter[str] = Counter()
    lines = [
        "# 同名待甄别辅助表",
        "",
        "> 机器初判仅用于缩小人工复核范围，不修改总底表，也不构成身份确认。",
        "",
        "## 汇总",
        "",
        f"- 带“同名待甄别”记录：{sum(len(items) for items in groups.values())}",
        f"- 归一化姓名组：{len(groups)}",
    ]
    rendered_groups = []
    for group_index, (name, items) in enumerate(sorted(groups.items()), start=1):
        decision, basis = classify_same_name_group(items)
        decision_counter[decision] += 1
        rendered_groups.append((group_index, name, items, decision, basis))
    lines.extend(
        [
            f"- 疑似同一人组：{decision_counter['疑似同一人']}",
            f"- 疑似不同人组：{decision_counter['疑似不同人']}",
            "",
            "## 分组对照",
            "",
        ]
    )
    for group_index, name, items, decision, basis in rendered_groups:
        lines.extend(
            [
                f"### {group_index}. {md_cell(name)}（{len(items)} 条）",
                "",
                "| 底表行 | 姓名 | 医院 | 科室 | 职称 | 擅长摘要 | 来源链接 | 照片文件 | 机器初判 | 判定依据 |",
                "|---:|---|---|---|---|---|---|---|---|---|",
            ]
        )
        for row_number, row in items:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row_number),
                        md_cell(row.get("姓名")),
                        md_cell(row.get("医院")),
                        md_cell(row.get("科室_分类页") or row.get("科室_列表卡片"), 80),
                        md_cell(row.get("职称身份原文") or row.get("职称_关键词"), 80),
                        md_cell(specialty_text(row), 140),
                        md_cell(row.get("来源链接")),
                        md_cell(row.get("照片文件")),
                        decision,
                        md_cell(basis),
                    ]
                )
                + " |"
            )
        lines.append("")
    summary = {
        "flagged_rows": sum(len(items) for items in groups.values()),
        "groups": len(groups),
        "same_person_groups": decision_counter["疑似同一人"],
        "different_person_groups": decision_counter["疑似不同人"],
    }
    return "\n".join(lines).rstrip() + "\n", summary


def index_link_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if "[[" in line and "|" in line)


def profile_counts(root: Path) -> dict[str, dict[str, int]]:
    result = {}
    for hospital in TARGET_HOSPITALS:
        hospital_dir = root / hospital
        files = [path for path in hospital_dir.glob("*.md") if path.name != "_索引.md"]
        auto = sum(profiles.is_auto_generated_profile(path) for path in files)
        result[hospital] = {
            "profiles": len(files),
            "auto_generated": auto,
            "protected_without_marker": len(files) - auto,
            "index_links": index_link_count(hospital_dir / "_索引.md"),
        }
    return result


def markdown_counter(counter: Counter[str] | dict[str, int]) -> str:
    lines = ["| 医院 | 数量 |", "|---|---:|"]
    for hospital in TARGET_HOSPITALS:
        lines.append(f"| {hospital} | {int(counter.get(hospital, 0))} |")
    return "\n".join(lines)


def build_cleanup_report(
    baseline: dict[str, Any],
    after_hashes: dict[str, Any],
    navigation_changes: list[dict[str, Any]],
    profile_backfills: list[dict[str, Any]],
    existing_profiles: Counter[str],
    missing_profiles: Counter[str],
    cell_diffs: list[dict[str, Any]],
    same_name_summary: dict[str, Any],
    profile_before: dict[str, dict[str, int]],
    profile_after: dict[str, dict[str, int]],
    refresh_result: dict[str, Any],
) -> str:
    nav_by_hospital = Counter(change["hospital"] for change in navigation_changes)
    backfill_by_hospital = Counter(change["hospital"] for change in profile_backfills)
    empty_after = sum(not clean(change["highlight_after"]) for change in navigation_changes)
    diff_by_column = Counter(diff["列名"] for diff in cell_diffs)
    hash_lines = ["| 资产 | 修改前 SHA-256 | 修改后 SHA-256 | 结论 |", "|---|---|---|---|"]
    for key, label in [
        ("ledger", "官网入口台账"),
        ("payload", "总底表 payload"),
        ("csv", "总底表 CSV"),
        ("xlsx", "总底表 XLSX"),
        ("report", "总底表更新报告"),
        ("profiles", "五院画像与索引聚合"),
        ("manual_profiles", "五院无自动标记画像聚合"),
    ]:
        before = baseline[key]["sha256"]
        after = after_hashes[key]["sha256"]
        conclusion = "不变" if before == after else "已变更"
        hash_lines.append(f"| {label} | `{before}` | `{after}` | {conclusion} |")

    profile_lines = [
        "| 医院 | 修改前画像 | 修改后画像 | 修改前索引链接 | 修改后索引链接 | 自动画像 | 受保护画像 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for hospital in TARGET_HOSPITALS:
        before = profile_before[hospital]
        after = profile_after[hospital]
        profile_lines.append(
            f"| {hospital} | {before['profiles']} | {after['profiles']} | "
            f"{before['index_links']} | {after['index_links']} | "
            f"{after['auto_generated']} | {after['protected_without_marker']} |"
        )

    return f"""# Issue #53 存量治理清理对账报告

## 总结

- 治理前后总底表：{baseline['rows']} 行、{baseline['hospitals']} 家医院，均保持不变。
- 子任务 A：应清 {len(navigation_changes)} 行、实清 {len(navigation_changes)} 行、清洗后留空 {empty_after} 行。
- 子任务 B：回填 {len(profile_backfills)} 行；五院实际已有画像 {sum(existing_profiles.values())} 行，仍无画像 {sum(missing_profiles.values())} 行。
- 子任务 C：带“同名待甄别” {same_name_summary['flagged_rows']} 行，归一化姓名 {same_name_summary['groups']} 组；辅助表只读生成，未据机器初判修改总底表。
- 自动画像精准刷新 {refresh_result['refreshed_auto_generated_profiles']} 份；新增画像 {refresh_result['generated_missing_profiles']} 份；人工/无自动标记画像未覆盖。

## A. 亮眼经历导航污染

{markdown_counter(nav_by_hospital)}

异常提示统一追加：`{NAVIGATION_WARNING}`。逐单元格前后值见 `{CELL_DIFF_CSV.relative_to(ROOT).as_posix()}`。

## B. 已建画像回填

### 回填分布

{markdown_counter(backfill_by_hospital)}

### 仍无画像分布

{markdown_counter(missing_profiles)}

现场 `已建画像` 列已无空值，且来源链接与现有画像一致的记录均已标记“是”，因此本轮没有制造零必要性的字段改写。

## C. 同名待甄别辅助表

- 辅助表：`{SAME_NAME_REPORT.relative_to(ROOT).as_posix()}`
- 疑似同一人组：{same_name_summary['same_person_groups']}
- 疑似不同人组：{same_name_summary['different_person_groups']}
- 机器初判仅供人工参考，不回写总底表。

## 逐单元格差异

| 列名 | 单元格数 |
|---|---:|
{chr(10).join(f'| {column} | {count} |' for column, count in sorted(diff_by_column.items()))}

实际差异列集合：{', '.join(sorted(diff_by_column)) or '无'}；允许列集合：{', '.join(sorted(ALLOWED_ROW_COLUMNS))}。

## 画像与索引

{chr(10).join(profile_lines)}

五院索引链接数逐院保持不变。

## 受保护资产哈希

{chr(10).join(hash_lines)}

台账不改；序号 10/12/27 挂账事项未处理。
"""


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def backup_targets(paths: Iterable[Path], backup_root: Path) -> dict[Path, Path | None]:
    result: dict[Path, Path | None] = {}
    for path in paths:
        if not path.exists():
            result[path] = None
            continue
        backup = backup_root / path.relative_to(ROOT)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
        result[path] = backup
    return result


def restore_targets(backups: dict[Path, Path | None]) -> None:
    for target, backup in backups.items():
        if backup is None:
            if target.exists():
                target.unlink()
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup, target)


def apply_outputs(file_map: dict[Path, Path]) -> None:
    for target, source in file_map.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #53 纯离线存量治理。")
    parser.add_argument("--apply", action="store_true", help="通过全部临时构建和门禁后提交受保护资产修改。")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload, current_rows = load_current_layers()
    before_rows = copy.deepcopy(current_rows)
    rows = copy.deepcopy(current_rows)
    hospital_count = len({clean(row.get("医院")) for row in rows if clean(row.get("医院"))})
    profile_before = profile_counts(PROFILE_ROOT)
    baseline = {
        "rows": len(rows),
        "hospitals": hospital_count,
        "ledger": sha256_file(LEDGER),
        "payload": sha256_file(MASTER_PAYLOAD),
        "csv": sha256_file(MASTER_CSV),
        "xlsx": sha256_file(MASTER_XLSX),
        "report": sha256_file(MASTER_REPORT),
        "profiles": manifest_hash(PROFILE_ROOT, TARGET_HOSPITALS),
        "manual_profiles": manifest_hash(PROFILE_ROOT, TARGET_HOSPITALS, marker_filter=False),
    }

    navigation_changes = apply_navigation_cleanup(rows)
    profile_backfills, existing_profiles, missing_profiles = apply_profile_backfill(rows)
    cell_diffs = collect_cell_diffs(before_rows, rows)
    updated_payload = recompute_payload(payload, rows)
    updated_payload["meta"]["current_batch_rows"] = len(navigation_changes) + len(profile_backfills)
    updated_payload["meta"]["existing_rows_refreshed"] = len(navigation_changes) + len(profile_backfills)
    same_name_text, same_name_summary = build_same_name_report(rows)

    summary = {
        "mode": "apply" if args.apply else "dry_run",
        "rows": len(rows),
        "hospitals": hospital_count,
        "navigation_expected": len(navigation_changes),
        "navigation_cleaned": len(navigation_changes),
        "navigation_empty_after": sum(not clean(change["highlight_after"]) for change in navigation_changes),
        "profile_backfilled": len(profile_backfills),
        "profiles_still_missing": sum(missing_profiles.values()),
        "same_name": same_name_summary,
        "cell_diffs": len(cell_diffs),
        "cell_diff_columns": dict(Counter(diff["列名"] for diff in cell_diffs)),
    }
    if len(navigation_changes) != 343:
        raise RuntimeError(f"现场导航污染为 {len(navigation_changes)} 行，偏离 Issue #53 预期 343 行")
    if not args.apply:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    with tempfile.TemporaryDirectory(prefix="issue53_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_payload = temp_root / MASTER_PAYLOAD.name
        temp_csv = temp_root / MASTER_CSV.name
        temp_xlsx = temp_root / MASTER_XLSX.name
        temp_preview = temp_root / "master_preview.png"
        temp_master_report = temp_root / MASTER_REPORT.name
        temp_cleanup_report = temp_root / CLEANUP_REPORT.name
        temp_cell_diff = temp_root / CELL_DIFF_CSV.name
        temp_same_name = temp_root / SAME_NAME_REPORT.name
        temp_profile_root = temp_root / "profiles"
        temp_profile_root.mkdir()

        write_json(temp_payload, updated_payload)
        collector.write_csv(temp_csv, rows)
        collector.build_workbook(temp_payload, temp_xlsx, temp_preview)
        collector.write_master_report(temp_master_report, updated_payload, MASTER_CSV, MASTER_XLSX)
        write_cell_diff_csv(temp_cell_diff, cell_diffs)
        temp_same_name.write_text(same_name_text, encoding="utf-8", newline="\n")

        affected_hospitals = sorted({change["hospital"] for change in navigation_changes})
        for hospital in affected_hospitals:
            shutil.copytree(PROFILE_ROOT / hospital, temp_profile_root / hospital)
        skip_hospitals = {
            clean(row.get("医院"))
            for row in rows
            if clean(row.get("医院")) and clean(row.get("医院")) not in affected_hospitals
        }
        refresh_sources = {change["source"] for change in navigation_changes if change["source"]}
        refresh_result = profiles.generate_missing_profiles(
            rows=rows,
            output_root=temp_profile_root,
            skip_hospitals=skip_hospitals,
            report_path=temp_root / "profile_refresh_report.md",
            refresh_auto_generated=True,
            refresh_sources=refresh_sources,
        )
        if refresh_result["generated_missing_profiles"] != 0:
            raise RuntimeError("精准画像刷新意外生成了新画像")

        profile_after = copy.deepcopy(profile_before)
        for hospital in affected_hospitals:
            profile_after[hospital] = profile_counts(temp_profile_root)[hospital]
            if profile_after[hospital]["index_links"] != profile_before[hospital]["index_links"]:
                raise RuntimeError(f"{hospital} 索引链接数发生变化")

        after_hashes = {
            "ledger": baseline["ledger"],
            "payload": sha256_file(temp_payload),
            "csv": sha256_file(temp_csv),
            "xlsx": sha256_file(temp_xlsx),
            "report": sha256_file(temp_master_report),
            "profiles": manifest_hash(temp_profile_root, affected_hospitals),
            "manual_profiles": manifest_hash(PROFILE_ROOT, TARGET_HOSPITALS, marker_filter=False),
        }
        if set(affected_hospitals) != set(TARGET_HOSPITALS):
            combined_root = temp_root / "combined_profiles"
            combined_root.mkdir()
            for hospital in TARGET_HOSPITALS:
                source_dir = temp_profile_root / hospital if hospital in affected_hospitals else PROFILE_ROOT / hospital
                shutil.copytree(source_dir, combined_root / hospital)
            after_hashes["profiles"] = manifest_hash(combined_root, TARGET_HOSPITALS)
            after_hashes["manual_profiles"] = manifest_hash(
                combined_root,
                TARGET_HOSPITALS,
                marker_filter=False,
            )

        temp_cleanup_report.write_text(
            build_cleanup_report(
                baseline=baseline,
                after_hashes=after_hashes,
                navigation_changes=navigation_changes,
                profile_backfills=profile_backfills,
                existing_profiles=existing_profiles,
                missing_profiles=missing_profiles,
                cell_diffs=cell_diffs,
                same_name_summary=same_name_summary,
                profile_before=profile_before,
                profile_after=profile_after,
                refresh_result=refresh_result,
            ),
            encoding="utf-8",
            newline="\n",
        )

        file_map: dict[Path, Path] = {
            MASTER_PAYLOAD: temp_payload,
            MASTER_CSV: temp_csv,
            MASTER_XLSX: temp_xlsx,
            MASTER_REPORT: temp_master_report,
            CLEANUP_REPORT: temp_cleanup_report,
            CELL_DIFF_CSV: temp_cell_diff,
            SAME_NAME_REPORT: temp_same_name,
        }
        for hospital in affected_hospitals:
            temp_hospital_dir = temp_profile_root / hospital
            source_map = profiles.extract_existing_sources(temp_hospital_dir)
            for source in refresh_sources:
                path = source_map.get(source)
                if path is not None and profiles.is_auto_generated_profile(path):
                    file_map[PROFILE_ROOT / hospital / path.name] = path
            file_map[PROFILE_ROOT / hospital / "_索引.md"] = temp_hospital_dir / "_索引.md"

        backups = backup_targets(file_map, temp_root / "backups")
        try:
            apply_outputs(file_map)
            final_payload, final_rows = load_current_layers()
            del final_payload
            final_hospitals = len({clean(row.get("医院")) for row in final_rows if clean(row.get("医院"))})
            if len(final_rows) != baseline["rows"] or final_hospitals != baseline["hospitals"]:
                raise RuntimeError("治理后总底表行数或医院数变化")
            actual_diffs = collect_cell_diffs(before_rows, final_rows)
            if actual_diffs != cell_diffs:
                raise RuntimeError("治理后实际逐单元格差异与预期不一致")
            if sha256_file(LEDGER) != baseline["ledger"]:
                raise RuntimeError("官网入口台账发生变化")
            if manifest_hash(PROFILE_ROOT, TARGET_HOSPITALS, marker_filter=False) != baseline["manual_profiles"]:
                raise RuntimeError("人工/无自动标记画像发生变化")
            for hospital in TARGET_HOSPITALS:
                before_count = profile_before[hospital]["index_links"]
                after_count = index_link_count(PROFILE_ROOT / hospital / "_索引.md")
                if before_count != after_count:
                    raise RuntimeError(f"{hospital} 索引链接数由 {before_count} 变为 {after_count}")
        except Exception:
            restore_targets(backups)
            raise

        summary.update(
            {
                "refreshed_auto_generated_profiles": refresh_result[
                    "refreshed_auto_generated_profiles"
                ],
                "indexes_rebuilt": refresh_result["indexes_rebuilt"],
                "outputs": [str(path.relative_to(ROOT)) for path in file_map],
            }
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
