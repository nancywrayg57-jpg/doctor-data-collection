from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import re
import shutil
import tempfile
import textwrap
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urljoin, urlparse

from PIL import Image, ImageDraw, ImageOps

import collect_official_doctors_batch as collector
import four_hospital_photo_cleanup_trial as trial
import generate_obsidian_profiles as profiles
import gzbrain_photo_backfill_full as full_helpers


ROOT = trial.ROOT
WORK_DIR = trial.WORK_DIR
VAULT = trial.VAULT
SOURCE_DIR = trial.SOURCE_DIR
MASTER_JSON = trial.MASTER_PAYLOAD
MASTER_CSV = trial.MASTER_CSV
MASTER_XLSX = trial.MASTER_XLSX
MASTER_REPORT = trial.MASTER_REPORT
LEDGER = trial.LEDGER

ISSUE_NUMBER = 85
PULL_REQUEST_NUMBER = 86
EXPECTED_SCOPE_COUNT = trial.EXPECTED_SCOPE_COUNT
EXPECTED_BY_HOSPITAL = trial.EXPECTED_SCOPE_BY_HOSPITAL
HOSPITALS = trial.HOSPITALS
FAILURE_STATES = tuple(sorted(trial.FAILURE_STATES))
ALLOWED_ROW_COLUMNS = {"照片链接", "照片文件", "异常提示"}
MAX_PHOTO_BYTES = 20 * 1024 * 1024
OWNER_REPORT_BYTES = 5 * 1024 * 1024
VISUAL_PAGE_SIZE = 25
AUTO_MARKER = "<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->"
FULL_VISUAL_PASS_STATUS = "PASSED_ALL_FULL_SUCCESS_CONTACT_SHEETS_AND_FAILURE_AUDIT_SAMPLES"
FULL_AUTHORIZATION = (
    "PR #86 owner comment 2026-08-19T15:25:00Z: "
    "TRIAL_AUDIT_PASSED -> FULL_APPEND_AND_OBSIDIAN; fixed four-hospital scope 249; "
    "administrator confirmation 2026-08-20 limits execution to Issue #85 / PR #86"
)

FULL_BASENAME = "四院零散照片清尾_photo_backfill_full"
FULL_PAYLOAD = WORK_DIR / f"{FULL_BASENAME}_payload.json"
FULL_RECONCILIATION = WORK_DIR / f"{FULL_BASENAME}_reconciliation.csv"
FULL_REPORT = WORK_DIR / f"{FULL_BASENAME}_report.md"
FAILURE_AUDIT_SHEET = WORK_DIR / f"{FULL_BASENAME}_failure_audit_sheet.jpg"
SUCCESS_VISUAL_DIR = WORK_DIR / f"{FULL_BASENAME}_success_visual_review"
RETIRED_PROMPT = ROOT / "docs" / "agent_prompts" / "codex_next_prompt.md"

PROFILE_DIRS = {
    hospital: VAULT / "01_试点医院" / hospital for hospital in HOSPITALS
}
FORMAL_PHOTO_DIRS = {
    hospital: PROFILE_DIRS[hospital] / "照片" for hospital in HOSPITALS
}

WARNING_BY_STATE = {
    state: f"官网本人职业照补录失败：{state}" for state in FAILURE_STATES
}
RECONCILIATION_FIELDS = (
    "医院",
    "详情ID",
    "姓名",
    "来源链接",
    "对账分类",
    "失败分类",
    "原异常提示",
    "新异常提示",
    "复测UTC",
    "照片原始引用",
    "照片传输URL",
    "照片引用数",
    "判定特征",
    "详情HTTP",
    "请求证据",
    "照片链接",
    "照片文件",
    "声明格式",
    "实际格式",
    "字节数",
    "SHA-256",
    "宽",
    "高",
)


def clean_text(value: Any) -> str:
    return trial.clean_text(value)


def row_value(value: Any) -> str:
    return "" if value is None else str(value)


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def file_digest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(f"受保护文件缺失：{path}")
    content = trial.repository_digest_bytes(path)
    return {"bytes": len(content), "sha256": sha256_bytes(content)}


def protected_snapshot() -> dict[str, Any]:
    files = [
        LEDGER,
        MASTER_REPORT,
        RETIRED_PROMPT,
        trial.PAYLOAD_PATH,
        trial.MANIFEST_PATH,
        trial.REPORT_PATH,
        trial.CONTACT_SHEET_PATH,
    ]
    files.extend(PROFILE_DIRS[hospital] / "_索引.md" for hospital in HOSPITALS)
    return {
        path.relative_to(ROOT).as_posix(): file_digest(path)
        for path in files
    }


def existing_photo_snapshot() -> dict[str, dict[str, dict[str, Any]]]:
    snapshot: dict[str, dict[str, dict[str, Any]]] = {}
    for hospital, root in FORMAL_PHOTO_DIRS.items():
        if not root.is_dir():
            raise RuntimeError(f"正式照片目录缺失：{root}")
        snapshot[hospital] = {
            path.name: file_digest(path)
            for path in sorted(root.iterdir())
            if path.is_file()
        }
    return snapshot


def validate_existing_photos_unchanged(
    snapshot: dict[str, dict[str, dict[str, Any]]]
) -> None:
    for hospital, files in snapshot.items():
        root = FORMAL_PHOTO_DIRS[hospital]
        for filename, expected in files.items():
            path = root / filename
            if not path.is_file() or file_digest(path) != expected:
                raise RuntimeError(f"既有正式照片被修改或删除：{hospital}/{filename}")


def load_master_payload() -> dict[str, Any]:
    payload = json.loads(MASTER_JSON.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("rows"), list):
        raise RuntimeError("总底表 payload 结构非法")
    return payload


def scope_rows_from(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scope = [
        dict(row)
        for row in rows
        if clean_text(row.get("医院")) in HOSPITALS
        and not clean_text(row.get("照片链接"))
        and not clean_text(row.get("照片文件"))
    ]
    counts = Counter(clean_text(row.get("医院")) for row in scope)
    if len(scope) != EXPECTED_SCOPE_COUNT or dict(counts) != EXPECTED_BY_HOSPITAL:
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 固定范围漂移："
            f"total={len(scope)} counts={dict(counts)}"
        )
    sources = [clean_text(row.get("来源链接")) for row in scope]
    if len(set(sources)) != EXPECTED_SCOPE_COUNT or any(not source for source in sources):
        raise RuntimeError("FULL 固定范围来源链接缺失或不唯一")
    for row in scope:
        trial.validate_source_link(clean_text(row.get("医院")), clean_text(row.get("来源链接")))
    csv_sources = {clean_text(row.get("来源链接")) for row in trial.load_scope_rows()}
    if set(sources) != csv_sources:
        raise RuntimeError("总底表 payload 与 CSV 的 Issue #85 固定范围不一致")
    return scope


def warning_parts(value: Any) -> list[str]:
    return [part for part in (clean_text(item) for item in clean_text(value).split("；")) if part]


def has_equivalent_failure_warning(value: Any, state: str) -> bool:
    warning = clean_text(value)
    if not warning:
        return False
    if WARNING_BY_STATE[state] in warning:
        return True
    state_rules = {
        "占位图": ("占位", "默认图", "default"),
        "无照片容器": (
            "无照片容器",
            "未提供符合范围的本人职业照",
            "未提供本人职业照",
            "无本人职业照",
        ),
        "照片资源不可达": (
            "照片资源不可达",
            "照片获取失败",
            "照片下载失败",
            "连续两次获取失败",
            "double_404",
            "照片404",
            "照片 404",
            "裁决留空",
        ),
        "详情不可达": ("详情不可达", "详情页404", "详情页 404", "详情获取失败"),
    }
    folded = warning.casefold()
    if state == "照片资源不可达" and "照片" in folded and any(
        token in folded for token in ("404", "获取失败", "下载失败", "不可达", "裁决")
    ):
        return True
    return any(token.casefold() in folded for token in state_rules[state])


def append_failure_warning(value: Any, state: str) -> tuple[str, str]:
    original = clean_text(value)
    if has_equivalent_failure_warning(original, state):
        return original, "维持留痕"
    parts = warning_parts(original)
    marker = WARNING_BY_STATE[state]
    if marker not in parts:
        parts.append(marker)
    return "；".join(parts), "更新留痕"


def formal_photo_relative(hospital: str, filename: str) -> str:
    return (Path("01_试点医院") / hospital / "照片" / filename).as_posix()


def allocate_formal_filename(
    row: dict[str, Any], extension: str, used_by_hospital: dict[str, set[str]]
) -> str:
    hospital = clean_text(row.get("医院"))
    used = used_by_hospital[hospital]
    root = FORMAL_PHOTO_DIRS[hospital]
    stem = trial.filename_stem(row)
    candidates = [
        f"{stem}.{extension}",
        f"{stem}-{trial.detail_id(hospital, clean_text(row.get('来源链接')))}.{extension}",
    ]
    for sequence in range(2, 1000):
        candidates.append(f"{stem}-{sequence}.{extension}")
    for candidate in candidates:
        folded = candidate.casefold()
        if folded not in used and not (root / candidate).exists():
            used.add(folded)
            return candidate
    raise RuntimeError(f"无法分配正式照片文件名：{hospital}/{row.get('姓名')}")


def photo_reference_count(sample: dict[str, Any]) -> int:
    raw = clean_text(sample.get("raw_photo_reference"))
    transport = clean_text(sample.get("photo_url"))
    references = sample.get("page_image_references") or []
    matches = 0
    for item in references:
        if transport and clean_text(item.get("absolute_url")) == transport:
            matches += 1
        elif raw and clean_text(item.get("raw_reference")) == raw:
            matches += 1
    return max(matches, int(bool(raw or transport)))


def failure_resource_urls(sample: dict[str, Any]) -> list[str]:
    source = clean_text(sample.get("source_link"))
    raw = clean_text(sample.get("raw_photo_reference"))
    transport = clean_text(sample.get("photo_url"))
    values = [transport]
    if raw:
        values.append(urljoin(source, raw))
    if not any(values):
        values.append(source)
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def request_evidence(trace_rows: list[dict[str, Any]]) -> str:
    compact = [
        {
            key: item.get(key)
            for key in ("method", "url", "started_utc", "status", "final_url", "content_type", "response_bytes", "error")
            if item.get(key) not in (None, "")
        }
        for item in trace_rows
    ]
    return json.dumps(compact, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def collect_row_diffs(
    before_rows: list[dict[str, Any]],
    after_rows: list[dict[str, Any]],
    target_sources: set[str],
) -> list[dict[str, str]]:
    if len(before_rows) != len(after_rows):
        raise RuntimeError("FULL 前后总底表行数发生变化")
    diffs: list[dict[str, str]] = []
    for sheet_row, (before, after) in enumerate(zip(before_rows, after_rows, strict=True), start=2):
        for column in collector.BASE_HEADERS:
            old = row_value(before.get(column))
            new = row_value(after.get(column))
            if old == new:
                continue
            source = clean_text(after.get("来源链接"))
            if source not in target_sources:
                raise RuntimeError(f"发现 Issue #85 范围外行修改：{source} {column}")
            if column not in ALLOWED_ROW_COLUMNS:
                raise RuntimeError(f"发现范围外字段修改：{column}")
            diffs.append(
                {
                    "底表行": str(sheet_row),
                    "医院": clean_text(after.get("医院")),
                    "姓名": clean_text(after.get("姓名")),
                    "来源链接": source,
                    "列名": column,
                    "修改前": old,
                    "修改后": new,
                }
            )
    return diffs


def recompute_master_derivatives(payload: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    warnings: Counter[str] = Counter()
    for row in rows:
        for warning in warning_parts(row.get("异常提示")):
            warnings[warning] += 1
    payload["warning_counts"] = dict(warnings)
    payload["hospital_batches"] = collector.build_hospital_batches(rows)


def write_master_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    headers = list(collector.BASE_HEADERS)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in headers} for row in rows)


def canonical_row(row: dict[str, Any]) -> tuple[str, ...]:
    return tuple(row_value(row.get(header)) for header in collector.BASE_HEADERS)


def validate_master_layers(payload_path: Path, csv_path: Path, xlsx_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    payload_rows = payload.get("rows", [])
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    xlsx_rows = profiles.read_xlsx_rows_basic(xlsx_path)
    expected = [canonical_row(row) for row in payload_rows]
    if [canonical_row(row) for row in csv_rows] != expected:
        raise RuntimeError("总底表 payload 与 CSV 不一致")
    if [canonical_row(row) for row in xlsx_rows] != expected:
        raise RuntimeError("总底表 payload 与 XLSX 自动采集底表不一致")
    return [dict(row) for row in payload_rows]


def profile_maps(
    target_sources_by_hospital: dict[str, set[str]],
    rows_by_source: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Path]]:
    result: dict[str, dict[str, Path]] = {}
    for hospital, target_sources in target_sources_by_hospital.items():
        source_map = profiles.extract_existing_sources(PROFILE_DIRS[hospital])
        missing = target_sources - set(source_map)
        if missing:
            raise RuntimeError(
                f"FULL 前 {hospital} 缺少目标画像：" + "、".join(sorted(missing)[:5])
            )
        selected = {source: source_map[source] for source in target_sources}
        if len(set(selected.values())) != len(selected):
            raise RuntimeError(f"{hospital} 目标来源未与画像一一对应")
        for source, path in selected.items():
            content = path.read_bytes()
            if AUTO_MARKER.encode("utf-8") not in content:
                raise RuntimeError(f"画像缺少 AUTO 标记：{hospital}/{path.name}")
            full_helpers.insert_profile_photo_block_bytes(
                content,
                clean_text(rows_by_source[source].get("姓名")),
                "照片/__preflight__.jpg",
            )
        result[hospital] = selected
    return result


def profile_tree(root: Path) -> dict[Path, bytes]:
    return {path.relative_to(root): path.read_bytes() for path in sorted(root.rglob("*.md"))}


def validate_profile_tree(
    before: dict[Path, bytes], after_root: Path, expected_changed: set[Path]
) -> None:
    after = profile_tree(after_root)
    if set(after) != set(before):
        raise RuntimeError("画像 Markdown 文件集合发生变化")
    changed = {path for path, content in before.items() if after[path] != content}
    if changed != expected_changed:
        delta = sorted(str(path) for path in changed ^ expected_changed)
        raise RuntimeError("画像外科式变更集合不一致：" + "、".join(delta[:8]))


def cross_doctor_duplicate_sha_groups(
    photos: list[dict[str, Any]],
) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = {}
    for item in photos:
        groups.setdefault(item["sha256"], []).append(
            {"hospital": item["hospital"], "name": item["name"], "source_link": item["source_link"]}
        )
    return {
        digest: rows
        for digest, rows in groups.items()
        if len({(row["hospital"], row["name"]) for row in rows}) > 1
    }


def wrap_text(value: Any, width: int) -> list[str]:
    text = clean_text(value)
    if not text:
        return [""]
    return textwrap.wrap(text, width=width, break_long_words=True, break_on_hyphens=False)


def draw_failure_audit_sheet(
    failures: list[dict[str, Any]], output_path: Path
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for hospital in HOSPITALS:
        hospital_failures = sorted(
            (item for item in failures if item["hospital"] == hospital),
            key=lambda item: item["source_link"],
        )
        if len(hospital_failures) < 2:
            raise RuntimeError(f"{hospital} 失败审计样本不足 2 条")
        selected.extend(hospital_failures[:2])
    columns = 2
    cell_width, cell_height = 860, 340
    canvas = Image.new("RGB", (columns * cell_width, 4 * cell_height), "#eeeeee")
    draw = ImageDraw.Draw(canvas)
    title_font = trial.contact_sheet_font(24)
    body_font = trial.contact_sheet_font(17)
    for index, item in enumerate(selected):
        row, col = divmod(index, columns)
        left, top = col * cell_width, row * cell_height
        draw.rectangle((left + 8, top + 8, left + cell_width - 8, top + cell_height - 8), fill="#f7f7f7", outline="#555555", width=2)
        draw.line((left + 28, top + 32, left + 108, top + 112), fill="#b91c1c", width=8)
        draw.line((left + 108, top + 32, left + 28, top + 112), fill="#b91c1c", width=8)
        draw.text((left + 132, top + 24), f"{item['hospital']}｜{item['name']}", font=title_font, fill="#111111")
        draw.text((left + 132, top + 64), f"{item['state']}｜{item['action']}", font=body_font, fill="#991b1b")
        lines = [
            f"UTC: {item['evidence']['observed_utc']}",
            f"raw: {item['evidence']['raw_photo_reference'] or '-'}",
            f"transport: {item['evidence']['transport_url'] or '-'}",
            f"refs: {item['evidence']['photo_reference_count']}",
            f"feature: {item['evidence']['detection_feature']}",
        ]
        y = top + 126
        for line in lines:
            for wrapped in wrap_text(line, 60):
                draw.text((left + 28, y), wrapped, font=body_font, fill="#333333")
                y += 27
    canvas.save(output_path, "JPEG", quality=92)
    return [
        {
            "hospital": item["hospital"],
            "name": item["name"],
            "source_link": item["source_link"],
            "state": item["state"],
        }
        for item in selected
    ]


def draw_success_sheet(
    page: list[dict[str, Any]], photo_paths: dict[str, Path], output_path: Path
) -> None:
    columns = 5
    cell_width, cell_height = 336, 430
    rows = (len(page) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_width, rows * cell_height), "#eeeeee")
    draw = ImageDraw.Draw(canvas)
    name_font = trial.contact_sheet_font(22)
    meta_font = trial.contact_sheet_font(14)
    for index, item in enumerate(page):
        row, col = divmod(index, columns)
        left, top = col * cell_width + 18, row * cell_height + 8
        path = photo_paths[item["source_link"]]
        content = path.read_bytes()
        with Image.open(io.BytesIO(content)) as source:
            source.load()
            preview = ImageOps.contain(ImageOps.exif_transpose(source).convert("RGB"), (300, 315))
        draw.rectangle((left - 2, top - 2, left + 302, top + 317), fill="#dddddd", outline="#555555", width=2)
        x = left + (300 - preview.width) // 2
        canvas.paste(preview, (x, top))
        draw.text((left, top + 322), f"{item['hospital']}｜{item['name']}", fill="#111111", font=name_font)
        draw.text((left, top + 355), f"{item['department']}｜{item['title']}", fill="#333333", font=meta_font)
        draw.text((left, top + 382), f"{item['width']}×{item['height']}｜{int(item['bytes']):,} B", fill="#555555", font=meta_font)
    canvas.save(output_path, "JPEG", quality=92)


def build_success_visual_sheets(
    photos: list[dict[str, Any]], photo_paths: dict[str, Path], output_root: Path
) -> list[dict[str, Any]]:
    if not photos:
        return []
    output_root.mkdir()
    ordered = sorted(photos, key=lambda item: (HOSPITALS.index(item["hospital"]), item["source_link"]))
    sheets: list[dict[str, Any]] = []
    for start in range(0, len(ordered), VISUAL_PAGE_SIZE):
        page = ordered[start : start + VISUAL_PAGE_SIZE]
        path = output_root / f"page_{start // VISUAL_PAGE_SIZE + 1:02d}.jpg"
        draw_success_sheet(page, photo_paths, path)
        content = path.read_bytes()
        sheets.append(
            {
                "path": path.name,
                "count": len(page),
                "first": f"{page[0]['hospital']}/{page[0]['name']}",
                "last": f"{page[-1]['hospital']}/{page[-1]['name']}",
                "bytes": len(content),
                "sha256": sha256_bytes(content),
            }
        )
    return sheets


def write_reconciliation(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RECONCILIATION_FIELDS)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in RECONCILIATION_FIELDS} for row in rows)


def count_summary(reconciliation: list[dict[str, Any]]) -> dict[str, Any]:
    total = Counter(item["对账分类"] for item in reconciliation)
    by_hospital: dict[str, dict[str, int]] = {}
    for hospital in HOSPITALS:
        counts = Counter(item["对账分类"] for item in reconciliation if item["医院"] == hospital)
        by_hospital[hospital] = {
            "expected": EXPECTED_BY_HOSPITAL[hospital],
            "补采": counts.get("补采", 0),
            "维持留痕": counts.get("维持留痕", 0),
            "更新留痕": counts.get("更新留痕", 0),
        }
    return {
        "expected": EXPECTED_SCOPE_COUNT,
        "补采": total.get("补采", 0),
        "维持留痕": total.get("维持留痕", 0),
        "更新留痕": total.get("更新留痕", 0),
        "by_hospital": by_hospital,
    }


def validate_count_summary(summary: dict[str, Any]) -> None:
    if summary["补采"] + summary["维持留痕"] + summary["更新留痕"] != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 249 = 补采 + 维持留痕 + 更新留痕未闭合")
    for hospital, counts in summary["by_hospital"].items():
        if counts["补采"] + counts["维持留痕"] + counts["更新留痕"] != counts["expected"]:
            raise RuntimeError(f"{hospital} 分组四数未闭合")


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|")


def write_report(path: Path, payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    summary = meta["reconciliation"]
    by_hospital_lines = "\n".join(
        f"| {hospital} | {counts['expected']} | {counts['补采']} | {counts['维持留痕']} | {counts['更新留痕']} |"
        for hospital, counts in summary["by_hospital"].items()
    )
    failure_counts = meta["failure_state_counts"]
    failure_lines = "\n".join(f"| {state} | {failure_counts.get(state, 0)} |" for state in FAILURE_STATES)
    large_lines = "\n".join(
        f"- {item['hospital']}｜{item['name']}｜{int(item['bytes']):,} bytes｜{item['photo_url']}｜`{item['sha256']}`"
        for item in payload["photos"]
        if int(item["bytes"]) > OWNER_REPORT_BYTES
    ) or "- 无"
    report = f"""# Issue #85 四院零散照片清尾 FULL 报告

> 日期：{meta['run_date']}
> Phase：`{meta['phase']}`
> 授权：{meta['authorization']}

## 249 行对账

`249 = {summary['补采']} 补采 + {summary['维持留痕']} 维持留痕 + {summary['更新留痕']} 更新留痕`

| 医院 | 固定范围 | 补采 | 维持留痕 | 更新留痕 |
|---|---:|---:|---:|---:|
{by_hospital_lines}

| 失败分类 | 数量 |
|---|---:|
{failure_lines}

## 数据与画像约束

- 总底表 payload/CSV/XLSX 逐值一致；逐单元格变化 {meta['row_diff_count']}：{json.dumps(meta['row_diff_columns'], ensure_ascii=False)}。
- 补采行仅填写照片双列且原异常提示不变；留痕行照片双列保持空白，既有等价判定维持，其他行仅追加幂等失败提示。
- 补采画像 {meta['profile_refreshed_count']} 份严格 `+2/-0`；失败画像 {meta['profile_untouched_count']} 份零触碰；四院 `_索引.md` 零修改。
- 成功照片联系表覆盖 {meta['success_visual_photo_count']} 张 / {meta['success_visual_sheet_count']} 页；失败抽样 {meta['failure_audit_sample_count']} 格（每院 2 格）。
- 视觉状态：`{meta['visual_status']}`。

## 图片大小终审

- 照片总字节 {meta['photo_total_bytes']:,}；最大 {meta['photo_max_bytes']:,} bytes。
- 超过 5 MiB：{meta['over_5mib_count']}；超过 20 MiB：{meta['over_20mib_count']}（必须为 0）。

{large_lines}

## 合规与请求

- 仅四院官网详情页实际引用；构造未引用路径 0，第三方来源 0，二维码 known-SHA 未落盘。
- 串行请求 {meta['request_count']} 次，最小相邻启动间隔 {meta['minimum_request_gap_seconds']} 秒；无环境代理、无并发、无手工 Cookie。
- 入口台账、总底表更新报告、退役提示词与 TRIAL 工件保持不变。

## 工件

- `{FULL_PAYLOAD.relative_to(ROOT).as_posix()}`
- `{FULL_RECONCILIATION.relative_to(ROOT).as_posix()}`
- `{FULL_REPORT.relative_to(ROOT).as_posix()}`
- `{FAILURE_AUDIT_SHEET.relative_to(ROOT).as_posix()}`
- `{SUCCESS_VISUAL_DIR.relative_to(ROOT).as_posix()}/`（补采为 0 时不生成）

## 停止点

完成本地实图与工作簿视觉核验、`--validate-full`、测试、提交、标准推送和 CI 后，在 PR #{PULL_REQUEST_NUMBER} 发布 `FULL_DONE`，等待 Owner 终审；不得自行合并、关闭 Issue 或领取下一任务。
"""
    path.write_text(report, encoding="utf-8", newline="\n")


def ensure_workspace_target(path: Path) -> None:
    root = ROOT.resolve()
    resolved = path.resolve()
    if resolved == root or root not in resolved.parents:
        raise RuntimeError(f"拒绝操作工作区外路径：{path}")


def backup_targets(targets: list[Path], backup_root: Path) -> dict[Path, Path | None]:
    backup_root.mkdir(parents=True, exist_ok=True)
    backups: dict[Path, Path | None] = {}
    for index, target in enumerate(targets):
        ensure_workspace_target(target)
        if target.exists():
            backup = backup_root / f"{index:04d}_{target.name}"
            shutil.copy2(target, backup)
            backups[target] = backup
        else:
            backups[target] = None
    return backups


def apply_file_map(file_map: dict[Path, Path]) -> None:
    for target, source in file_map.items():
        ensure_workspace_target(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = target.with_name(f".{target.name}.issue85.tmp")
        if staging.exists():
            staging.unlink()
        shutil.copy2(source, staging)
        staging.replace(target)


def restore_targets(backups: dict[Path, Path | None]) -> None:
    for target, backup in backups.items():
        ensure_workspace_target(target)
        staging = target.with_name(f".{target.name}.issue85.restore")
        if staging.exists():
            staging.unlink()
        if backup is None:
            if target.exists():
                target.unlink()
            continue
        shutil.copy2(backup, staging)
        staging.replace(target)


def assert_outputs_absent() -> None:
    existing = [
        str(path)
        for path in (FULL_PAYLOAD, FULL_RECONCILIATION, FULL_REPORT, FAILURE_AUDIT_SHEET, SUCCESS_VISUAL_DIR)
        if path.exists()
    ]
    if existing:
        raise RuntimeError("FULL 输出已存在，拒绝覆盖：\n- " + "\n- ".join(existing))


def validate_payload_structure(payload: dict[str, Any]) -> None:
    meta = payload.get("meta", {})
    reconciliation = payload.get("reconciliation", [])
    photos = payload.get("photos", [])
    failures = payload.get("failures", [])
    if meta.get("issue") != ISSUE_NUMBER or meta.get("expected_count") != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL Issue/固定范围不一致")
    if len(reconciliation) != EXPECTED_SCOPE_COUNT or len({item["来源链接"] for item in reconciliation}) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL reconciliation 不是唯一 249 行")
    validate_count_summary(meta["reconciliation"])
    if len(photos) != meta["reconciliation"]["补采"]:
        raise RuntimeError("FULL 补采照片数与对账不一致")
    if len(failures) != meta["reconciliation"]["维持留痕"] + meta["reconciliation"]["更新留痕"]:
        raise RuntimeError("FULL 失败留痕数与对账不一致")
    if len(payload.get("profile_integrity", [])) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 画像完整性清单不是 249 行")
    if int(meta.get("over_20mib_count") or 0):
        raise RuntimeError("FULL 存在超过 20 MiB 照片")
    if cross_doctor_duplicate_sha_groups(photos):
        raise RuntimeError("FULL 存在跨医生同 SHA")
    if meta.get("protected_before") != meta.get("protected_after_preinstall"):
        raise RuntimeError("FULL 临时事务触碰受保护文件")
    audit_samples = payload.get("failure_audit_samples", [])
    if len(audit_samples) != 8 or Counter(item["hospital"] for item in audit_samples) != Counter({hospital: 2 for hospital in HOSPITALS}):
        raise RuntimeError("FULL 失败审计样本未达到每院 2 格")
    if sum(int(item["count"]) for item in payload.get("success_visual_sheets", [])) != len(photos):
        raise RuntimeError("FULL 成功联系表未覆盖全部补采照片")


def validate_full_installation(payload: dict[str, Any], require_visual: bool = True) -> None:
    validate_payload_structure(payload)
    final_rows = validate_master_layers(MASTER_JSON, MASTER_CSV, MASTER_XLSX)
    target_rows = {
        clean_text(row.get("来源链接")): row
        for row in final_rows
        if clean_text(row.get("来源链接")) in {item["来源链接"] for item in payload["reconciliation"]}
    }
    if len(target_rows) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 落盘总底表目标行不是 249")
    for item in payload["reconciliation"]:
        row = target_rows[item["来源链接"]]
        if item["对账分类"] == "补采":
            if row_value(row.get("照片链接")) != row_value(item["照片链接"]) or row_value(row.get("照片文件")) != row_value(item["照片文件"]):
                raise RuntimeError(f"补采行照片双列不一致：{item['来源链接']}")
            if clean_text(row.get("异常提示")) != clean_text(item["原异常提示"]):
                raise RuntimeError(f"补采行改动了既有异常提示：{item['来源链接']}")
        else:
            if clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")):
                raise RuntimeError(f"失败行照片双列未保持空白：{item['来源链接']}")
            if clean_text(row.get("异常提示")) != clean_text(item["新异常提示"]):
                raise RuntimeError(f"失败行异常提示不一致：{item['来源链接']}")
            if not all(clean_text(item.get(field)) for field in ("复测UTC", "判定特征", "请求证据")):
                raise RuntimeError(f"失败行复测证据不完整：{item['来源链接']}")
    for photo in payload["photos"]:
        path = FORMAL_PHOTO_DIRS[photo["hospital"]] / photo["filename"]
        content = path.read_bytes()
        extension = trial.image_extension(content, photo.get("declared_content_type", ""))
        width, height = trial.image_dimensions(content, extension)
        if (
            len(content) != int(photo["bytes"])
            or sha256_bytes(content) != photo["sha256"]
            or extension != photo["actual_extension"]
            or (width, height) != (int(photo["width"]), int(photo["height"]))
        ):
            raise RuntimeError(f"补采照片字节/魔数/尺寸不一致：{path}")
        if trial.placeholder_reason(photo["photo_url"], photo["sha256"]):
            raise RuntimeError(f"补采照片命中占位门禁：{path}")
    validate_existing_photos_unchanged(payload["existing_photo_snapshot"])
    for item in payload["profile_integrity"]:
        path = ROOT / item["path"]
        if sha256_bytes(path.read_bytes()) != item["after_sha256"]:
            raise RuntimeError(f"画像落盘哈希不一致：{path}")
        expected_added = 2 if item["status"] == "补采" else 0
        if item["added_lines"] != expected_added or item["removed_lines"] != 0:
            raise RuntimeError(f"画像变化不是规定的 +2/-0：{path}")
    if protected_snapshot() != payload["meta"]["protected_before"]:
        raise RuntimeError("入口台账、更新报告、退役提示词、TRIAL 工件或索引发生变化")
    if not FAILURE_AUDIT_SHEET.is_file() or sha256_bytes(FAILURE_AUDIT_SHEET.read_bytes()) != payload["meta"]["failure_audit_sha256"]:
        raise RuntimeError("失败审计拼图缺失或哈希不一致")
    expected_visual = {item["path"] for item in payload["success_visual_sheets"]}
    actual_visual = {path.name for path in SUCCESS_VISUAL_DIR.glob("*.jpg")} if SUCCESS_VISUAL_DIR.exists() else set()
    if actual_visual != expected_visual:
        raise RuntimeError("成功联系表目录存在缺失或孤儿")
    for item in payload["success_visual_sheets"]:
        content = (SUCCESS_VISUAL_DIR / item["path"]).read_bytes()
        if len(content) != item["bytes"] or sha256_bytes(content) != item["sha256"]:
            raise RuntimeError(f"成功联系表哈希不一致：{item['path']}")
    with FULL_RECONCILIATION.open("r", encoding="utf-8-sig", newline="") as handle:
        if len(list(csv.DictReader(handle))) != EXPECTED_SCOPE_COUNT:
            raise RuntimeError("FULL reconciliation CSV 不是 249 行")
    if require_visual and payload["meta"].get("visual_status") != FULL_VISUAL_PASS_STATUS:
        raise RuntimeError("FULL 视觉工件尚未标记通过")


def run_full(run_date: str) -> dict[str, Any]:
    assert_outputs_absent()
    protected_before = protected_snapshot()
    photo_snapshot = existing_photo_snapshot()
    master_payload = load_master_payload()
    before_rows = copy.deepcopy(master_payload["rows"])
    scope_rows = scope_rows_from(before_rows)
    rows_by_source = {clean_text(row.get("来源链接")): row for row in scope_rows}
    target_sources = {clean_text(row.get("来源链接")) for row in scope_rows}
    target_sources_by_hospital = {
        hospital: {
            clean_text(row.get("来源链接"))
            for row in scope_rows
            if clean_text(row.get("医院")) == hospital
        }
        for hospital in HOSPITALS
    }
    live_profile_maps = profile_maps(target_sources_by_hospital, rows_by_source)
    before_profile_trees = {hospital: profile_tree(PROFILE_DIRS[hospital]) for hospital in HOSPITALS}
    before_profile_bytes = {
        source: path.read_bytes()
        for hospital in HOSPITALS
        for source, path in live_profile_maps[hospital].items()
    }

    session = trial.RateLimitedSession()
    used_download_names: set[str] = set()
    used_formal_names = {
        hospital: {name.casefold() for name in photo_snapshot[hospital]}
        for hospital in HOSPITALS
    }
    result_by_source: dict[str, dict[str, Any]] = {}
    reconciliation_by_source: dict[str, dict[str, Any]] = {}
    photos_out: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="issue85_full_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        download_dir = temp_root / "downloads"
        trial.TRIAL_PHOTO_DIR = download_dir
        staged_photos = temp_root / "formal_photos"
        staged_profiles: dict[str, Path] = {}
        for hospital in HOSPITALS:
            target = temp_root / f"profile_{HOSPITALS.index(hospital)}"
            shutil.copytree(PROFILE_DIRS[hospital], target)
            staged_profiles[hospital] = target

        for index, row in enumerate(scope_rows, start=1):
            trace_start = len(session.trace)
            sample = trial.collect_sample(session, row, used_download_names)
            row_trace = session.trace[trace_start:]
            source = clean_text(row.get("来源链接"))
            hospital = clean_text(row.get("医院"))
            original_warning = clean_text(row.get("异常提示"))
            ref_count = photo_reference_count(sample)
            if sample.get("result") == "downloaded":
                content = (ROOT / sample["disk_path"]).read_bytes()
                if len(content) > MAX_PHOTO_BYTES:
                    raise RuntimeError(
                        "[FATAL - HUMAN_INTERVENTION_REQUIRED] 单图超过 20 MiB："
                        f"{hospital}/{row.get('姓名')} {len(content)}"
                    )
                extension = clean_text(sample.get("actual_extension")) or trial.image_extension(
                    content, sample.get("declared_content_type", "")
                )
                if not extension:
                    raise RuntimeError(f"补采照片格式无法识别：{hospital}/{row.get('姓名')}")
                filename = allocate_formal_filename(row, extension, used_formal_names)
                stage_path = staged_photos / hospital / filename
                stage_path.parent.mkdir(parents=True, exist_ok=True)
                stage_path.write_bytes(content)
                photo_file = formal_photo_relative(hospital, filename)
                updated = dict(row)
                updated["照片链接"] = clean_text(sample.get("photo_url"))
                updated["照片文件"] = photo_file
                result_by_source[source] = updated
                declared = Path(unquote(urlparse(updated["照片链接"]).path)).suffix.lower().lstrip(".")
                photo_item = {
                    "hospital": hospital,
                    "detail_id": sample["detail_id"],
                    "name": clean_text(row.get("姓名")),
                    "department": trial.first_department(row),
                    "title": trial.primary_title(row),
                    "source_link": source,
                    "photo_url": updated["照片链接"],
                    "photo_file": photo_file,
                    "filename": filename,
                    "declared_extension": declared,
                    "declared_content_type": clean_text(sample.get("declared_content_type")),
                    "actual_extension": extension,
                    "bytes": len(content),
                    "sha256": sha256_bytes(content),
                    "width": int(sample["width"]),
                    "height": int(sample["height"]),
                    "raw_photo_reference": clean_text(sample.get("raw_photo_reference")),
                    "photo_reference_count": ref_count,
                    "observed_utc": clean_text(sample.get("observed_utc")),
                    "request_trace": row_trace,
                }
                if trial.placeholder_reason(photo_item["photo_url"], photo_item["sha256"]):
                    raise RuntimeError(f"成功照片命中占位门禁：{hospital}/{row.get('姓名')}")
                photos_out.append(photo_item)
                reconciliation_by_source[source] = {
                    "医院": hospital,
                    "详情ID": sample["detail_id"],
                    "姓名": clean_text(row.get("姓名")),
                    "来源链接": source,
                    "对账分类": "补采",
                    "失败分类": "",
                    "原异常提示": original_warning,
                    "新异常提示": original_warning,
                    "复测UTC": clean_text(sample.get("observed_utc")),
                    "照片原始引用": clean_text(sample.get("raw_photo_reference")),
                    "照片传输URL": updated["照片链接"],
                    "照片引用数": ref_count,
                    "判定特征": clean_text(sample.get("decision_feature")),
                    "详情HTTP": sample.get("detail_http_status", ""),
                    "请求证据": request_evidence(row_trace),
                    "照片链接": updated["照片链接"],
                    "照片文件": photo_file,
                    "声明格式": declared,
                    "实际格式": extension,
                    "字节数": len(content),
                    "SHA-256": photo_item["sha256"],
                    "宽": photo_item["width"],
                    "高": photo_item["height"],
                }
            else:
                state = clean_text(sample.get("failure_state"))
                if state not in FAILURE_STATES:
                    raise RuntimeError(f"失败行未归入四类：{hospital}/{row.get('姓名')} {state}")
                new_warning, action = append_failure_warning(original_warning, state)
                updated = dict(row)
                updated["照片链接"] = ""
                updated["照片文件"] = ""
                updated["异常提示"] = new_warning
                result_by_source[source] = updated
                evidence = {
                    "observed_utc": clean_text(sample.get("observed_utc")) or trial.utc_now(),
                    "resource_urls": failure_resource_urls(sample),
                    "raw_photo_reference": clean_text(sample.get("raw_photo_reference")),
                    "transport_url": clean_text(sample.get("photo_url")),
                    "photo_reference_count": ref_count,
                    "detection_feature": clean_text(sample.get("decision_feature")),
                    "request_trace": row_trace,
                }
                failure = {
                    "hospital": hospital,
                    "detail_id": sample["detail_id"],
                    "name": clean_text(row.get("姓名")),
                    "source_link": source,
                    "state": state,
                    "action": action,
                    "original_warning": original_warning,
                    "new_warning": new_warning,
                    "evidence": evidence,
                }
                failures.append(failure)
                reconciliation_by_source[source] = {
                    "医院": hospital,
                    "详情ID": sample["detail_id"],
                    "姓名": failure["name"],
                    "来源链接": source,
                    "对账分类": action,
                    "失败分类": state,
                    "原异常提示": original_warning,
                    "新异常提示": new_warning,
                    "复测UTC": evidence["observed_utc"],
                    "照片原始引用": evidence["raw_photo_reference"],
                    "照片传输URL": evidence["transport_url"],
                    "照片引用数": ref_count,
                    "判定特征": evidence["detection_feature"],
                    "详情HTTP": sample.get("detail_http_status", ""),
                    "请求证据": request_evidence(row_trace),
                    "照片链接": "",
                    "照片文件": "",
                    "声明格式": "",
                    "实际格式": "",
                    "字节数": "",
                    "SHA-256": "",
                    "宽": "",
                    "高": "",
                }
            if index % 20 == 0 or index == EXPECTED_SCOPE_COUNT:
                print(
                    f"[FULL] {index}/{EXPECTED_SCOPE_COUNT} 补采={len(photos_out)} 留痕={len(failures)}",
                    flush=True,
                )

        # All GDMCH pages are checked inside collect_sample; retain the TRIAL known-SHA
        # evidence and assert that the known QR was never written to the download tree.
        if any(
            sha256_bytes(path.read_bytes()) == trial.GDMCH_SHARED_QR_SHA256
            for path in download_dir.glob("*")
            if path.is_file()
        ):
            raise RuntimeError("省妇幼 known-SHA 二维码被错误落盘")

        duplicates = cross_doctor_duplicate_sha_groups(photos_out)
        if duplicates:
            raise RuntimeError(
                "CROSS_DOCTOR_DUPLICATE_SHA_REQUIRES_MANUAL_REVIEW: "
                + json.dumps(duplicates, ensure_ascii=False, sort_keys=True)
            )
        if set(result_by_source) != target_sources:
            raise RuntimeError("FULL 249 行来源集合未闭合")
        reconciliation = [reconciliation_by_source[clean_text(row.get("来源链接"))] for row in scope_rows]
        summary = count_summary(reconciliation)
        validate_count_summary(summary)
        result_rows = [result_by_source[clean_text(row.get("来源链接"))] for row in scope_rows]
        updated_by_source = {clean_text(row.get("来源链接")): row for row in result_rows}
        after_rows = [copy.deepcopy(updated_by_source.get(clean_text(row.get("来源链接")), row)) for row in before_rows]
        row_diffs = collect_row_diffs(before_rows, after_rows, target_sources)
        updated_master = copy.deepcopy(master_payload)
        updated_master["rows"] = after_rows
        recompute_master_derivatives(updated_master, after_rows)

        temp_master_json = temp_root / MASTER_JSON.name
        temp_master_csv = temp_root / MASTER_CSV.name
        temp_master_xlsx = temp_root / MASTER_XLSX.name
        temp_master_preview = temp_root / "master_preview.png"
        write_json(temp_master_json, updated_master)
        write_master_csv(temp_master_csv, after_rows)
        collector.build_workbook(temp_master_json, temp_master_xlsx, temp_master_preview)
        validate_master_layers(temp_master_json, temp_master_csv, temp_master_xlsx)

        success_sources = {item["source_link"] for item in photos_out}
        photos_by_source = {item["source_link"]: item for item in photos_out}
        staged_photo_paths = {
            item["source_link"]: staged_photos / item["hospital"] / item["filename"]
            for item in photos_out
        }
        profile_integrity: list[dict[str, Any]] = []
        for hospital in HOSPITALS:
            live_map = live_profile_maps[hospital]
            temp_profile_root = staged_profiles[hospital]
            changed: set[Path] = set()
            for source in target_sources_by_hospital[hospital]:
                live_path = live_map[source]
                relative = live_path.relative_to(PROFILE_DIRS[hospital])
                temp_path = temp_profile_root / relative
                before_content = before_profile_bytes[source]
                if source in success_sources:
                    item = photos_by_source[source]
                    after_content = full_helpers.insert_profile_photo_block_bytes(
                        before_content,
                        item["name"],
                        f"照片/{item['filename']}",
                    )
                    temp_path.write_bytes(after_content)
                    full_helpers.validate_profile_photo_only_bytes(
                        before_content,
                        after_content,
                        item["name"],
                        f"照片/{item['filename']}",
                    )
                    changed.add(relative)
                after_content = temp_path.read_bytes()
                profile_integrity.append(
                    {
                        "hospital": hospital,
                        "source_link": source,
                        "path": live_path.relative_to(ROOT).as_posix(),
                        "status": "补采" if source in success_sources else "留痕",
                        "before_sha256": sha256_bytes(before_content),
                        "after_sha256": sha256_bytes(after_content),
                        "added_lines": 2 if source in success_sources else 0,
                        "removed_lines": 0,
                    }
                )
            validate_profile_tree(before_profile_trees[hospital], temp_profile_root, changed)

        temp_failure_audit = temp_root / FAILURE_AUDIT_SHEET.name
        failure_audit_samples = draw_failure_audit_sheet(failures, temp_failure_audit)
        temp_visual_dir = temp_root / SUCCESS_VISUAL_DIR.name
        success_visual_sheets = build_success_visual_sheets(photos_out, staged_photo_paths, temp_visual_dir)
        request_meta = trial.request_summary(session.trace)
        state_counts = Counter(item["state"] for item in failures)
        total_bytes = sum(int(item["bytes"]) for item in photos_out)
        protected_after_preinstall = protected_snapshot()
        payload: dict[str, Any] = {
            "meta": {
                "issue": ISSUE_NUMBER,
                "pull_request": PULL_REQUEST_NUMBER,
                "phase": "FULL_READY_FOR_CODEX_VISUAL_REVIEW",
                "run_date": run_date,
                "authorization": FULL_AUTHORIZATION,
                "expected_count": EXPECTED_SCOPE_COUNT,
                "reconciliation": summary,
                "failure_state_counts": {state: state_counts.get(state, 0) for state in FAILURE_STATES},
                "photo_total_bytes": total_bytes,
                "photo_max_bytes": max((int(item["bytes"]) for item in photos_out), default=0),
                "over_5mib_count": sum(int(item["bytes"]) > OWNER_REPORT_BYTES for item in photos_out),
                "over_20mib_count": sum(int(item["bytes"]) > MAX_PHOTO_BYTES for item in photos_out),
                "profile_refreshed_count": len(success_sources),
                "profile_untouched_count": EXPECTED_SCOPE_COUNT - len(success_sources),
                "row_diff_count": len(row_diffs),
                "row_diff_columns": dict(Counter(item["列名"] for item in row_diffs)),
                "request_count": request_meta["request_count"],
                "minimum_request_gap_seconds": request_meta["minimum_adjacent_start_interval_seconds"],
                "all_requests_serial": request_meta["all_requests_serial"],
                "known_qr_sha256": trial.GDMCH_SHARED_QR_SHA256,
                "known_qr_saved_to_disk": False,
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "failure_audit_sample_count": len(failure_audit_samples),
                "failure_audit_sha256": sha256_bytes(temp_failure_audit.read_bytes()),
                "success_visual_photo_count": len(photos_out),
                "success_visual_sheet_count": len(success_visual_sheets),
                "visual_status": "PENDING_CODEX_FULL_VISUAL_REVIEW",
                "protected_before": protected_before,
                "protected_after_preinstall": protected_after_preinstall,
            },
            "reconciliation": reconciliation,
            "photos": photos_out,
            "failures": failures,
            "row_diffs": row_diffs,
            "rows": result_rows,
            "profile_integrity": profile_integrity,
            "failure_audit_samples": failure_audit_samples,
            "success_visual_sheets": success_visual_sheets,
            "request_summary": request_meta,
            "request_trace": session.trace,
            "existing_photo_snapshot": photo_snapshot,
        }
        validate_payload_structure(payload)

        temp_full_payload = temp_root / FULL_PAYLOAD.name
        temp_full_reconciliation = temp_root / FULL_RECONCILIATION.name
        temp_full_report = temp_root / FULL_REPORT.name
        write_json(temp_full_payload, payload)
        write_reconciliation(temp_full_reconciliation, reconciliation)
        write_report(temp_full_report, payload)

        file_map: dict[Path, Path] = {
            MASTER_JSON: temp_master_json,
            MASTER_CSV: temp_master_csv,
            MASTER_XLSX: temp_master_xlsx,
            FULL_PAYLOAD: temp_full_payload,
            FULL_RECONCILIATION: temp_full_reconciliation,
            FULL_REPORT: temp_full_report,
            FAILURE_AUDIT_SHEET: temp_failure_audit,
        }
        for item in photos_out:
            file_map[FORMAL_PHOTO_DIRS[item["hospital"]] / item["filename"]] = staged_photo_paths[item["source_link"]]
            source = item["source_link"]
            hospital = item["hospital"]
            relative = live_profile_maps[hospital][source].relative_to(PROFILE_DIRS[hospital])
            file_map[live_profile_maps[hospital][source]] = staged_profiles[hospital] / relative
        for sheet in success_visual_sheets:
            file_map[SUCCESS_VISUAL_DIR / sheet["path"]] = temp_visual_dir / sheet["path"]

        backups = backup_targets(list(file_map), temp_root / "backups")
        try:
            apply_file_map(file_map)
            final_rows = validate_master_layers(MASTER_JSON, MASTER_CSV, MASTER_XLSX)
            if collect_row_diffs(before_rows, final_rows, target_sources) != row_diffs:
                raise RuntimeError("FULL 落盘逐单元格差异与预期不一致")
            validate_full_installation(payload, require_visual=False)
        except Exception:
            restore_targets(backups)
            if SUCCESS_VISUAL_DIR.exists() and not any(SUCCESS_VISUAL_DIR.iterdir()):
                SUCCESS_VISUAL_DIR.rmdir()
            raise
        return payload


def mark_visual_pass() -> dict[str, Any]:
    payload = json.loads(FULL_PAYLOAD.read_text(encoding="utf-8"))
    validate_full_installation(payload, require_visual=False)
    payload["meta"]["visual_status"] = FULL_VISUAL_PASS_STATUS
    payload["meta"]["visual_reviewed_utc"] = trial.utc_now()
    payload["meta"]["phase"] = "FULL_READY_FOR_FINAL_OWNER_AUDIT"
    write_json(FULL_PAYLOAD, payload)
    write_report(FULL_REPORT, payload)
    validate_full_installation(payload, require_visual=True)
    return payload


def refresh_failure_audit() -> dict[str, Any]:
    payload = json.loads(FULL_PAYLOAD.read_text(encoding="utf-8"))
    validate_full_installation(payload, require_visual=False)
    with tempfile.TemporaryDirectory(prefix="issue85_audit_refresh_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_sheet = temp_root / FAILURE_AUDIT_SHEET.name
        samples = draw_failure_audit_sheet(payload["failures"], temp_sheet)
        updated = copy.deepcopy(payload)
        updated["failure_audit_samples"] = samples
        updated["meta"]["failure_audit_sample_count"] = len(samples)
        updated["meta"]["failure_audit_sha256"] = sha256_bytes(temp_sheet.read_bytes())
        temp_payload = temp_root / FULL_PAYLOAD.name
        temp_report = temp_root / FULL_REPORT.name
        write_json(temp_payload, updated)
        write_report(temp_report, updated)
        file_map = {
            FAILURE_AUDIT_SHEET: temp_sheet,
            FULL_PAYLOAD: temp_payload,
            FULL_REPORT: temp_report,
        }
        backups = backup_targets(list(file_map), temp_root / "backups")
        try:
            apply_file_map(file_map)
            validate_full_installation(updated, require_visual=False)
        except Exception:
            restore_targets(backups)
            raise
    return updated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #85 四院零散照片清尾 FULL")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--full", action="store_true", help="执行固定 249 行 FULL 事务")
    mode.add_argument("--validate-full", action="store_true", help="验证已落盘 FULL")
    mode.add_argument("--mark-visual-pass", action="store_true", help="人工目视通过后写入视觉状态")
    mode.add_argument("--refresh-failure-audit", action="store_true", help="事务化重生成失败抽样拼图")
    parser.add_argument("--run-date", default=str(date.today()), help="执行日期 YYYY-MM-DD")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.full:
        payload = run_full(args.run_date)
        summary = payload["meta"]["reconciliation"]
        print(
            "FULL_APPLIED "
            f"expected={summary['expected']} downloaded={summary['补采']} "
            f"maintained={summary['维持留痕']} updated={summary['更新留痕']}"
        )
        return 0
    if args.mark_visual_pass:
        payload = mark_visual_pass()
        print(f"FULL_VISUAL_REVIEW_MARKED status={payload['meta']['visual_status']}")
        return 0
    if args.refresh_failure_audit:
        payload = refresh_failure_audit()
        print(
            "FULL_FAILURE_AUDIT_REFRESHED "
            f"samples={payload['meta']['failure_audit_sample_count']}"
        )
        return 0
    payload = json.loads(FULL_PAYLOAD.read_text(encoding="utf-8"))
    validate_full_installation(payload, require_visual=True)
    summary = payload["meta"]["reconciliation"]
    print(
        "FULL_VALIDATED "
        f"expected={summary['expected']} downloaded={summary['补采']} "
        f"maintained={summary['维持留痕']} updated={summary['更新留痕']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
