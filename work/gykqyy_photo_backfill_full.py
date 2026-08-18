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
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps

import gykqyy_photo_backfill_trial as trial


ROOT = trial.ROOT
WORK_DIR = trial.WORK_DIR
SOURCE_DIR = trial.SOURCE_DIR
HOSPITAL = trial.HOSPITAL
ISSUE_NUMBER = trial.ISSUE_NUMBER
BRANCH = trial.BRANCH
MASTER_JSON_PATH = trial.MASTER_JSON_PATH
MASTER_CSV_PATH = trial.MASTER_CSV_PATH
MASTER_XLSX_PATH = trial.MASTER_XLSX_PATH
MASTER_REPORT_PATH = trial.MASTER_REPORT_PATH
PROFILE_DIR = trial.PROFILE_DIR
FORMAL_PHOTO_DIR = trial.FORMAL_PHOTO_DIR
LEDGER_JSON_PATH = trial.LEDGER_JSON_PATH
LEDGER_CSV_PATH = trial.LEDGER_CSV_PATH
LEDGER_XLSX_PATH = trial.LEDGER_XLSX_PATH

EXPECTED_SCOPE_COUNT = trial.EXPECTED_SCOPE_COUNT
EXPECTED_SUCCESS_COUNT = 58
EXPECTED_FAILURE_COUNT = 239
EXPECTED_EMPTY_IMAGE_COUNT = 231
EXPECTED_NON_UPLOAD_COUNT = 8
EXPECTED_TRIAL_REUSE_COUNT = trial.EXPECTED_TRIAL_COUNT
EXPECTED_FRESH_COUNT = EXPECTED_SCOPE_COUNT - EXPECTED_TRIAL_REUSE_COUNT
EXPECTED_FRESH_SUCCESS_COUNT = EXPECTED_SUCCESS_COUNT - EXPECTED_TRIAL_REUSE_COUNT
EXPECTED_PROFILE_COUNT = EXPECTED_SCOPE_COUNT

FULL_BASENAME = f"{HOSPITAL}_photo_backfill_full"
FULL_JSON_PATH = WORK_DIR / f"{FULL_BASENAME}_payload.json"
FULL_CSV_PATH = WORK_DIR / f"{FULL_BASENAME}_reconciliation.csv"
FULL_REPORT_PATH = WORK_DIR / f"{FULL_BASENAME}_report.md"
FULL_AUDIT_SHEET_PATH = WORK_DIR / f"{FULL_BASENAME}_audit_sheet.jpg"
PHOTO_RELATIVE_ROOT = Path("01_试点医院") / HOSPITAL / "照片"

FULL_ALLOWED_ROW_COLUMNS = {"照片链接", "照片文件", "异常提示"}
FULL_FAILURE_STATES = ("详情不可达", "照片资源不可达", "无照片容器", "占位图")
FULL_AUTHORIZATION = (
    "PR #76 owner comment 5333032694: TRIAL_AUDIT_PASSED -> "
    "FULL_APPEND_AND_OBSIDIAN"
)
AUTO_MARKER = "<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->"

NO_PHOTO_WARNING = "官网 image 字段为空，无照片容器"
NON_UPLOAD_WARNING = "官网 image 字段非 uploads 原图，待 Owner 终审归类"
DETAIL_MISSING_WARNING = "官网目录接口缺少固定 ID，详情不可达"
RESOURCE_UNREACHABLE_WARNING = "官网照片资源不可达"
PLACEHOLDER_WARNING = "官网照片为占位图"

FULL_PROTECTED_FILES = (
    LEDGER_JSON_PATH,
    LEDGER_CSV_PATH,
    LEDGER_XLSX_PATH,
    MASTER_REPORT_PATH,
    trial.TRIAL_JSON_PATH,
    trial.TRIAL_CSV_PATH,
    trial.TRIAL_REPORT_PATH,
    trial.CONTACT_SHEET_PATH,
)


def row_value(value: Any) -> str:
    return "" if value is None else str(value)


def file_digest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(f"受保护文件缺失：{path}")
    content = path.read_bytes()
    return {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}


def immutable_snapshot() -> dict[str, Any]:
    return {
        "files": {str(path): file_digest(path) for path in FULL_PROTECTED_FILES},
        "trial_photo_tree": trial.tree_snapshot(trial.TRIAL_PHOTO_DIR),
    }


def append_warning(value: Any, warning: str) -> str:
    warnings = [trial.clean_text(item) for item in trial.clean_text(value).split("；")]
    warnings = [item for item in warnings if item]
    if warning not in warnings:
        warnings.append(warning)
    return "；".join(warnings)


def normalized_photo_reference(value: Any) -> str:
    raw = trial.clean_text(value)
    return trial.page_referenced_photo_url(raw)


def allocate_full_photo_path(
    row: dict[str, Any], extension: str, photo_root: Path, used_names: set[str]
) -> tuple[str, Path]:
    source_id = trial.source_id(row.get("来源链接"))
    stem = "-".join(
        [
            trial.safe_photo_part(row.get("姓名")),
            trial.atomic_department(row),
            trial.safe_photo_part(trial.primary_title(row.get("职称身份原文"))),
            trial.safe_photo_part(HOSPITAL),
        ]
    )
    filename = f"{stem}.{extension}"
    if filename.casefold() in used_names:
        filename = f"{stem}-{source_id}.{extension}"
    if filename.casefold() in used_names:
        raise RuntimeError(f"FULL 照片文件名仍冲突：{filename}")
    used_names.add(filename.casefold())
    return filename, photo_root / filename


def placeholder_response_reason(
    photo_url: str, content: bytes, width: int, height: int
) -> str:
    path = Path(photo_url.split("?", 1)[0]).name.casefold()
    if any(marker in path for marker in ("default", "null", "nopic", "noimage", "placeholder")):
        return f"URL 文件名命中占位标记：{path}"
    if len(content) <= 10 * 1024 and width <= 128 and height <= 128:
        return f"响应为小尺寸占位图特征：{len(content)} bytes；{width}×{height}"
    return ""


def reconcile_scope_with_missing(
    rows: list[dict[str, Any]], doctors: list[dict[str, Any]], observed_utc: str
) -> tuple[list[dict[str, Any]], list[str]]:
    by_id = {trial.clean_text(item.get("id")): item for item in doctors}
    row_ids = {trial.source_id(row.get("来源链接")) for row in rows}
    extra_ids = sorted(set(by_id) - row_ids, key=int)
    records: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda item: int(trial.source_id(item.get("来源链接")))):
        item_id = trial.source_id(row.get("来源链接"))
        item = by_id.get(item_id)
        if item is None:
            records.append(
                {
                    "id": item_id,
                    "name": trial.clean_text(row.get("姓名")),
                    "source_link": trial.clean_text(row.get("来源链接")),
                    "master_department": trial.clean_text(row.get("科室_分类页")),
                    "first_department_atom": trial.atomic_department(row),
                    "master_title": trial.clean_text(row.get("职称身份原文")),
                    "api_category": "",
                    "api_keshi_ids": "",
                    "api_keshi": "",
                    "api_title": "",
                    "api_image_field_value": "",
                    "image_signal": "DETAIL_UNREACHABLE_API_ID_MISSING",
                    "valid_photo_url": "",
                    "observed_utc": observed_utc,
                }
            )
            continue
        master_name = trial.clean_text(row.get("姓名"))
        api_name = trial.clean_text(item.get("title"))
        if not master_name or master_name != api_name:
            raise RuntimeError(
                f"API/底表姓名不一致：id={item_id} master={master_name} api={api_name}"
            )
        raw_image = trial.clean_text(item.get("image"))
        records.append(
            {
                "id": item_id,
                "name": master_name,
                "source_link": trial.clean_text(row.get("来源链接")),
                "master_department": trial.clean_text(row.get("科室_分类页")),
                "first_department_atom": trial.atomic_department(row),
                "master_title": trial.clean_text(row.get("职称身份原文")),
                "api_category": trial.clean_text(item.get("yccms_category_id")),
                "api_keshi_ids": trial.clean_text(item.get("keshi_ids")),
                "api_keshi": trial.clean_text(item.get("keshi")),
                "api_title": trial.clean_text(item.get("zhicheng")),
                "api_image_field_value": raw_image,
                "image_signal": trial.image_field_signal(raw_image),
                "valid_photo_url": normalized_photo_reference(raw_image),
                "observed_utc": observed_utc,
            }
        )
    return records, extra_ids


def failure_evidence_text(evidence: dict[str, Any]) -> str:
    return "；".join(
        [
            f"UTC={trial.clean_text(evidence.get('observed_utc'))}",
            f"API={trial.DIRECTORY_API}",
            f"category={trial.clean_text(evidence.get('api_category')) or 'missing'}",
            f"image_field={json.dumps(evidence.get('image_field_value'), ensure_ascii=False)}",
            f"signal={trial.clean_text(evidence.get('image_signal'))}",
            f"判定={trial.clean_text(evidence.get('detection_feature'))}",
        ]
    )


def canonical_master_row(row: dict[str, Any], headers: list[str]) -> tuple[str, ...]:
    return tuple(row_value(row.get(header)) for header in headers)


def collect_full_row_diffs(
    before_rows: list[dict[str, Any]],
    after_rows: list[dict[str, Any]],
    target_sources: set[str],
    headers: list[str],
) -> list[dict[str, str]]:
    if len(before_rows) != len(after_rows):
        raise RuntimeError("FULL 前后总底表行数发生变化")
    diffs: list[dict[str, str]] = []
    for sheet_row, (before, after) in enumerate(
        zip(before_rows, after_rows, strict=True), start=2
    ):
        for column in headers:
            old = row_value(before.get(column))
            new = row_value(after.get(column))
            if old == new:
                continue
            source = trial.clean_text(after.get("来源链接"))
            if source not in target_sources:
                raise RuntimeError(f"发现 Issue #75 范围外行修改：{source} {column}")
            diffs.append(
                {
                    "底表行": str(sheet_row),
                    "序号": trial.clean_text(after.get("序号")),
                    "姓名": trial.clean_text(after.get("姓名")),
                    "来源链接": source,
                    "列名": column,
                    "修改前": old,
                    "修改后": new,
                }
            )
    unexpected = sorted({item["列名"] for item in diffs} - FULL_ALLOWED_ROW_COLUMNS)
    if unexpected:
        raise RuntimeError("发现范围外字段修改：" + "、".join(unexpected))
    return diffs


def recompute_master_derivatives(
    payload: dict[str, Any], rows: list[dict[str, Any]]
) -> None:
    import collect_official_doctors_batch as collector

    warnings: Counter[str] = Counter()
    for row in rows:
        for warning in trial.clean_text(row.get("异常提示")).split("；"):
            if warning:
                warnings[warning] += 1
    payload["warning_counts"] = dict(warnings)
    payload["hospital_batches"] = collector.build_hospital_batches(rows)


def write_master_csv(path: Path, rows: list[dict[str, Any]], headers: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in headers} for row in rows)


def validate_master_layers(
    payload_path: Path, csv_path: Path, xlsx_path: Path
) -> list[dict[str, Any]]:
    import collect_official_doctors_batch as collector
    import generate_obsidian_profiles as profiles

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    payload_rows = payload.get("rows", [])
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    xlsx_rows = profiles.read_xlsx_rows_basic(xlsx_path)
    headers = list(collector.BASE_HEADERS)
    expected = [canonical_master_row(row, headers) for row in payload_rows]
    if [canonical_master_row(row, headers) for row in csv_rows] != expected:
        raise RuntimeError("总底表 payload 与 CSV 不一致")
    if [canonical_master_row(row, headers) for row in xlsx_rows] != expected:
        raise RuntimeError("总底表 payload 与 XLSX 自动采集底表不一致")
    return [dict(row) for row in payload_rows]


def write_reconciliation_csv(path: Path, payload: dict[str, Any]) -> None:
    headers = [
        "ID",
        "姓名",
        "来源链接",
        "状态",
        "失败分类",
        "分类状态",
        "API category",
        "API keshi_ids",
        "API image 字段原值",
        "照片链接",
        "照片文件",
        "实际格式",
        "字节数",
        "SHA-256",
        "宽",
        "高",
        "来源批次",
        "错误证据",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(
            {header: item.get(header, "") for header in headers}
            for item in payload["reconciliation"]
        )


def profile_photo_markdown_path(photo_file: str) -> str:
    markdown_path = "/".join(Path(photo_file.replace("\\", "/")).parts[-2:])
    if not markdown_path.startswith("照片/"):
        raise RuntimeError(f"画像照片相对路径越界：{photo_file}")
    return markdown_path


def insert_profile_photo_block(
    before_text: str, doctor_name: str, photo_file: str
) -> str:
    markdown_path = profile_photo_markdown_path(photo_file)
    if re.search(r"(?m)^!\[[^\]]*\]\(照片/[^)]+\)[ \t\r]*$", before_text):
        raise RuntimeError(f"画像已存在照片嵌入区块：{doctor_name}")
    marker = re.compile(r"(?m)^## 基础信息[ \t]*(?P<newline>\r\n|\n)(?P=newline)")
    matches = list(marker.finditer(before_text))
    if len(matches) != 1:
        raise RuntimeError(f"画像基础信息插入点不唯一：{doctor_name} 数量={len(matches)}")
    match = matches[0]
    newline = match.group("newline")
    photo_block = f"![{doctor_name}]({markdown_path}){newline}{newline}"
    return before_text[: match.end()] + photo_block + before_text[match.end() :]


def insert_profile_photo_block_bytes(
    before_bytes: bytes, doctor_name: str, photo_file: str
) -> bytes:
    bom = b"\xef\xbb\xbf" if before_bytes.startswith(b"\xef\xbb\xbf") else b""
    body = before_bytes[len(bom) :]
    try:
        before_text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"画像不是有效 UTF-8：{doctor_name}") from exc
    return bom + insert_profile_photo_block(before_text, doctor_name, photo_file).encode(
        "utf-8"
    )


def validate_profile_photo_only_bytes(
    before_bytes: bytes, after_bytes: bytes, doctor_name: str, photo_file: str
) -> None:
    expected = insert_profile_photo_block_bytes(before_bytes, doctor_name, photo_file)
    if after_bytes != expected:
        raise RuntimeError(f"画像出现照片嵌入区块以外字节变化：{doctor_name}")
    if len(after_bytes.decode("utf-8-sig").splitlines()) - len(
        before_bytes.decode("utf-8-sig").splitlines()
    ) != 2:
        raise RuntimeError(f"画像照片最小刷新不是 +2/-0：{doctor_name}")


def profile_markdown_tree(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes() for path in sorted(root.rglob("*.md"))
    }


def validate_profile_tree_surgical(
    before_tree: dict[Path, bytes],
    after_root: Path,
    expected_changed_paths: set[Path],
) -> None:
    after_tree = profile_markdown_tree(after_root)
    if set(after_tree) != set(before_tree):
        raise RuntimeError("画像 Markdown 文件集合发生变化")
    changed = {path for path, content in before_tree.items() if after_tree[path] != content}
    if changed != expected_changed_paths:
        delta = sorted(str(path) for path in changed ^ expected_changed_paths)
        raise RuntimeError("画像外科式变更集合不一致：" + "、".join(delta[:5]))


def target_profile_paths(
    profile_root: Path, target_sources: set[str]
) -> dict[str, Path]:
    import generate_obsidian_profiles as profiles

    sources = profiles.extract_existing_sources(profile_root)
    missing = target_sources - set(sources)
    if missing:
        raise RuntimeError("FULL 前目标范围缺少既有画像：" + "、".join(sorted(missing)[:5]))
    result = {source: sources[source] for source in target_sources}
    profile_files = {
        path for path in profile_root.glob("*.md") if path.name != "_索引.md"
    }
    if (
        len(result) != EXPECTED_PROFILE_COUNT
        or len(profile_files) != EXPECTED_PROFILE_COUNT
        or set(result.values()) != profile_files
    ):
        raise RuntimeError("FULL 前 297 个来源与 297 份画像不是一一对应")
    return result


def preflight_profile_bytes(
    profile_paths: dict[str, Path], rows_by_source: dict[str, dict[str, Any]]
) -> dict[str, bytes]:
    before: dict[str, bytes] = {}
    probe_file = (PHOTO_RELATIVE_ROOT / "__preflight__.jpg").as_posix()
    marker = AUTO_MARKER.encode("utf-8")
    for source, path in profile_paths.items():
        content = path.read_bytes()
        name = trial.clean_text(rows_by_source[source].get("姓名"))
        if marker not in content:
            raise RuntimeError(f"画像缺少 AUTO 标记：{name}")
        insert_profile_photo_block_bytes(content, name, probe_file)
        before[source] = content
    return before


def select_audit_samples(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(samples) < 10:
        raise RuntimeError("FULL 成功照片不足 10 张，无法生成抽样拼图")
    smallest = min(samples, key=lambda item: (int(item["bytes"]), item["source_link"]))
    largest = max(samples, key=lambda item: (int(item["bytes"]), item["source_link"]))
    remaining = [item for item in samples if item not in (smallest, largest)]
    random_like = sorted(
        remaining,
        key=lambda item: hashlib.sha256(item["source_link"].encode("utf-8")).hexdigest(),
    )[:8]
    selected = [{**smallest, "audit_kind": "最小"}, {**largest, "audit_kind": "最大"}]
    selected.extend({**item, "audit_kind": "确定性随机"} for item in random_like)
    return selected


def build_full_audit_sheet(
    samples: list[dict[str, Any]], photo_root: Path, output_path: Path
) -> list[dict[str, Any]]:
    selected = select_audit_samples(samples)
    canvas = Image.new("RGB", (1700, 880), "white")
    draw = ImageDraw.Draw(canvas)
    name_font = trial.common.contact_sheet_font(22)
    meta_font = trial.common.contact_sheet_font(14)
    for index, item in enumerate(selected):
        row, col = divmod(index, 5)
        left = 20 + col * 336
        top = 10 + row * 430
        with Image.open(photo_root / item["filename"]) as image:
            image.load()
            preview = ImageOps.contain(image.convert("RGB"), (300, 315))
        x = left + (300 - preview.width) // 2
        canvas.paste(preview, (x, top))
        draw.text((left, top + 320), f"{item['audit_kind']}｜{item['name']}", fill="black", font=name_font)
        draw.text((left, top + 353), f"{item['department']}｜{item['title']}", fill="#333333", font=meta_font)
        draw.text(
            (left, top + 380),
            f"{item['width']}×{item['height']}｜{int(item['bytes']):,} B",
            fill="#555555",
            font=meta_font,
        )
    canvas.save(output_path, "JPEG", quality=92)
    return [
        {
            "audit_kind": item["audit_kind"],
            "name": item["name"],
            "source_link": item["source_link"],
            "filename": item["filename"],
            "bytes": item["bytes"],
            "sha256": item["sha256"],
        }
        for item in selected
    ]


def ensure_workspace_target(path: Path) -> None:
    root = ROOT.resolve()
    resolved = path.resolve()
    if resolved == root or root not in resolved.parents:
        raise RuntimeError(f"拒绝操作工作区外路径：{path}")


def backup_file_targets(
    targets: list[Path], backup_root: Path
) -> dict[Path, Path | None]:
    backups: dict[Path, Path | None] = {}
    backup_root.mkdir(parents=True, exist_ok=True)
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
        staging = target.with_name(f".{target.name}.issue75.tmp")
        if staging.exists():
            staging.unlink()
        shutil.copy2(source, staging)
        staging.replace(target)


def restore_file_targets(backups: dict[Path, Path | None]) -> None:
    for target, backup in backups.items():
        ensure_workspace_target(target)
        staging = target.with_name(f".{target.name}.issue75.restore")
        if staging.exists():
            staging.unlink()
        if backup is None:
            target.unlink(missing_ok=True)
            continue
        shutil.copy2(backup, staging)
        staging.replace(target)


def write_full_report(path: Path, payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    state_lines = "\n".join(
        f"| {state} | {meta['failure_state_counts'].get(state, 0)} |"
        for state in FULL_FAILURE_STATES
    )
    bucket_lines = "\n".join(
        f"| {bucket} | {meta['size_bucket_counts'].get(bucket, 0)} |"
        for bucket in ("<200KiB", "200KiB-1MiB", "1-5MiB", "5-20MiB", ">20MiB")
    )
    non_upload_lines = "\n".join(
        f"- ID {item['id']}｜{item['name']}｜image=`{item['api_image_field_value']}`｜"
        f"判定 `{item['classification_status']}`｜UTC {item['observed_utc']}"
        for item in payload["non_upload_review"]
    ) or "- 无"
    large_lines = "\n".join(
        f"- {item['name']}｜{item['photo_url']}｜{item['bytes']:,} bytes｜"
        f"{item['width']}×{item['height']}｜`{item['sha256']}`"
        for item in payload["photo_samples"]
        if int(item["bytes"]) > trial.OWNER_REPORT_BYTES
    ) or "- 无"
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 FULL 报告

> 日期：{meta['run_date']}
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`

## 四数对账

| 固定目标 | 实采 | 失败留空 | 正式落盘 |
|---:|---:|---:|---:|
| {meta['expected_count']} | {meta['downloaded_count']} | {meta['failed_count']} | {meta['disk_photo_count']} |

- 复用已审计 TRIAL：{meta['trial_reused_count']}；FULL 新抓取成功：{meta['fresh_downloaded_count']}；新抓取目标：{meta['fresh_target_count']}。
- API category 唯一值：{json.dumps(meta['category_values'], ensure_ascii=False)}；其他 category 请求 0；未声明接口探测 0；构造路径 0。

| 失败四类（8 条非 uploads 暂按无照片容器计数，待 Owner 终审） | 数量 |
|---|---:|
{state_lines}

## 8 条非 uploads image 字段终审清单

{non_upload_lines}

## 照片与大小

| 大小分桶 | 数量 |
|---|---:|
{bucket_lines}

- 照片总字节 {meta['photo_total_bytes']:,}（{meta['photo_total_mib']:.2f} MiB）；最大 {meta['photo_max_bytes']:,} bytes。
- 超过 5 MiB {meta['over_5mib_count']}；超过 20 MiB {meta['over_20mib_count']}；状态波动 {meta['status_flicker_count']}。
- 实际格式：{json.dumps(meta['format_counts'], ensure_ascii=False)}；重复 SHA-256 组 {meta['duplicate_sha256_group_count']}。

## >5 MiB Owner 终审清单

{large_lines}

## 三载体、画像与审计

- 总底表 payload/CSV/XLSX 逐值一致；只修改本院 `照片链接`、`照片文件` 与失败行 `异常提示`。
- 逐单元格变化 {meta['row_diff_count']}：{json.dumps(meta['row_diff_columns'], ensure_ascii=False)}。
- FULL reconciliation/manifest 对 58 张逐一复算字节、SHA-256、魔数/扩展名与尺寸；照片目录零孤儿零缺失。
- 成功 {meta['profile_refreshed_count']} 份 AUTO 画像严格 +2/-0；失败 {meta['profile_untouched_count']} 份零触碰；`_索引.md` 零修改。
- 入口台账 JSON/CSV/XLSX、总底表更新报告与全部 TRIAL 工件保持不变。
- FULL 抽样拼图：`{FULL_AUDIT_SHEET_PATH.relative_to(ROOT).as_posix()}`（最小、最大、8 个确定性随机样本）。

## 工件

- `{FULL_JSON_PATH.relative_to(ROOT).as_posix()}`
- `{FULL_CSV_PATH.relative_to(ROOT).as_posix()}`
- `{FULL_REPORT_PATH.relative_to(ROOT).as_posix()}`
- `{FULL_AUDIT_SHEET_PATH.relative_to(ROOT).as_posix()}`
- `{FORMAL_PHOTO_DIR.relative_to(ROOT).as_posix()}/`（58 张）

## 停止点

`FULL_READY_FOR_FINAL_OWNER_AUDIT`。提交并推送 PR #76 后停止；不得自行合并 PR、关闭 Issue 或领取下一任务。
"""
    path.write_text(report, encoding="utf-8", newline="\n")


def validate_full_payload(
    payload: dict[str, Any], photo_root: Path, audit_sheet: Path
) -> None:
    meta = payload.get("meta", {})
    if (
        meta.get("expected_count") != EXPECTED_SCOPE_COUNT
        or meta.get("downloaded_count") != EXPECTED_SUCCESS_COUNT
        or meta.get("failed_count") != EXPECTED_FAILURE_COUNT
        or meta.get("blank_count") != EXPECTED_FAILURE_COUNT
        or meta.get("disk_photo_count") != EXPECTED_SUCCESS_COUNT
    ):
        raise RuntimeError("FULL 四数对账不符合 297=58+239，落盘不是 58")
    if (
        meta.get("trial_reused_count") != EXPECTED_TRIAL_REUSE_COUNT
        or meta.get("fresh_target_count") != EXPECTED_FRESH_COUNT
        or meta.get("fresh_downloaded_count") != EXPECTED_FRESH_SUCCESS_COUNT
        or meta.get("fresh_failed_count") != EXPECTED_FAILURE_COUNT
    ):
        raise RuntimeError("FULL TRIAL 复用/新处理计数不闭合")
    if meta.get("category_values") != [trial.EXPECTED_CATEGORY]:
        raise RuntimeError("FULL API category 不是唯一 55")
    states = meta.get("failure_state_counts", {})
    if states != {"详情不可达": 0, "照片资源不可达": 0, "无照片容器": 239, "占位图": 0}:
        raise RuntimeError("FULL 失败四类分布不符合现场结果")
    if meta.get("non_upload_review_count") != EXPECTED_NON_UPLOAD_COUNT:
        raise RuntimeError("FULL 非 uploads 终审清单不是 8 条")
    if meta.get("empty_image_count") != EXPECTED_EMPTY_IMAGE_COUNT:
        raise RuntimeError("FULL 空 image 数不是 231")
    if any(
        int(meta.get(key, 0)) != 0
        for key in (
            "status_flicker_count",
            "over_20mib_count",
            "other_category_request_count",
            "undeclared_api_probe_count",
            "constructed_unreferenced_probe_count",
            "third_party_source_count",
            "api_missing_fixed_id_count",
            "api_extra_scope_id_count",
        )
    ):
        raise RuntimeError("FULL 存在波动、越界、超限或 API 范围漂移")
    if meta.get("existing_profile_count") != EXPECTED_PROFILE_COUNT:
        raise RuntimeError("FULL 既有画像不是 297 份")
    if meta.get("profile_refreshed_count") != EXPECTED_SUCCESS_COUNT:
        raise RuntimeError("FULL 画像刷新数不是 58")
    if meta.get("profile_untouched_count") != EXPECTED_FAILURE_COUNT:
        raise RuntimeError("FULL 失败画像零触碰数不是 239")
    if meta.get("row_diff_columns") != {
        "照片链接": EXPECTED_SUCCESS_COUNT,
        "照片文件": EXPECTED_SUCCESS_COUNT,
        "异常提示": EXPECTED_FAILURE_COUNT,
    }:
        raise RuntimeError("FULL 总底表逐列变化计数不符合 58/58/239")
    if meta.get("immutable_before") != meta.get("immutable_after_preinstall"):
        raise RuntimeError("FULL 临时事务触碰了受保护资产")

    rows = payload.get("rows", [])
    reconciliation = payload.get("reconciliation", [])
    photos = payload.get("photo_samples", [])
    failures = payload.get("failures", [])
    if not (
        len(rows) == len(reconciliation) == EXPECTED_SCOPE_COUNT
        and len(photos) == EXPECTED_SUCCESS_COUNT
        and len(failures) == EXPECTED_FAILURE_COUNT
    ):
        raise RuntimeError("FULL rows/reconciliation/photo/failure 数量不闭合")
    if len({item.get("来源链接") for item in reconciliation}) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL reconciliation 来源不唯一")
    if len(payload.get("non_upload_review", [])) != EXPECTED_NON_UPLOAD_COUNT:
        raise RuntimeError("FULL 非 uploads 逐条证据清单不完整")

    actual_files = {path.name: path for path in photo_root.iterdir() if path.is_file()}
    if len(actual_files) != EXPECTED_SUCCESS_COUNT:
        raise RuntimeError("FULL 照片目录文件数不是 58")
    expected_files = {item["filename"] for item in photos}
    if set(actual_files) != expected_files:
        raise RuntimeError("FULL 照片目录存在孤儿或缺失")
    for item in photos:
        path = actual_files[item["filename"]]
        content = path.read_bytes()
        if len(content) != item["bytes"]:
            raise RuntimeError(f"FULL 照片字节不一致：{path.name}")
        if hashlib.sha256(content).hexdigest() != item["sha256"]:
            raise RuntimeError(f"FULL 照片 SHA-256 不一致：{path.name}")
        extension = trial.common.magic_extension(content, item["content_type"])
        if extension != item["extension"] or path.suffix.lower() != f".{extension}":
            raise RuntimeError(f"FULL 照片魔数/扩展名不一致：{path.name}")
        if trial.common.image_dimensions(content) != (item["width"], item["height"]):
            raise RuntimeError(f"FULL 照片尺寸不一致：{path.name}")
        if normalized_photo_reference(item["photo_url"]) != item["photo_url"]:
            raise RuntimeError(f"FULL 照片 URL 越界：{path.name}")
        if trial.comparable_host(item["photo_final_url"]) != trial.OFFICIAL_HOST:
            raise RuntimeError(f"FULL 照片最终响应越出官网：{path.name}")
    if not audit_sheet.is_file():
        raise RuntimeError("FULL 抽样拼图缺失")


def validate_full_installation(payload: dict[str, Any]) -> None:
    import collect_official_doctors_batch as collector

    final_rows = validate_master_layers(MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH)
    validate_full_payload(payload, FORMAL_PHOTO_DIR, FULL_AUDIT_SHEET_PATH)
    target_rows = [row for row in final_rows if trial.clean_text(row.get("医院")) == HOSPITAL]
    headers = list(collector.BASE_HEADERS)
    if {
        trial.clean_text(row.get("来源链接")): canonical_master_row(row, headers)
        for row in target_rows
    } != {
        trial.clean_text(row.get("来源链接")): canonical_master_row(row, headers)
        for row in payload["rows"]
    }:
        raise RuntimeError("FULL payload 目标行与已落盘总底表不一致")
    target_sources = {trial.clean_text(row.get("来源链接")) for row in payload["rows"]}
    profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
    integrity = {
        trial.clean_text(item.get("source_link")): item
        for item in payload.get("profile_integrity", [])
    }
    if len(integrity) != EXPECTED_PROFILE_COUNT:
        raise RuntimeError("FULL 画像完整性清单不是 297 条")
    for source, path in profile_paths.items():
        expected = integrity[source]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected["after_sha256"]:
            raise RuntimeError(f"FULL 画像落盘哈希不一致：{path}")
        added = 2 if expected["status"] == "实采" else 0
        if expected["added_lines"] != added or expected["removed_lines"] != 0:
            raise RuntimeError(f"FULL 画像行级变化不符合 +2/-0：{path}")
    if hashlib.sha256((PROFILE_DIR / "_索引.md").read_bytes()).hexdigest() != meta_value(
        payload, "profile_index_before_sha256"
    ):
        raise RuntimeError("FULL 修改了 _索引.md")
    if immutable_snapshot() != meta_value(payload, "immutable_before"):
        raise RuntimeError("FULL 修改了入口台账、更新报告或 TRIAL 工件")
    with FULL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        if len(list(csv.DictReader(handle))) != EXPECTED_SCOPE_COUNT:
            raise RuntimeError("FULL reconciliation CSV 不是 297 行")


def meta_value(payload: dict[str, Any], key: str) -> Any:
    return payload.get("meta", {}).get(key)


def run_full(run_date: str) -> dict[str, Any]:
    import collect_official_doctors_batch as collector

    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("FULL 前正式照片目录已存在，拒绝覆盖")
    for path in (FULL_JSON_PATH, FULL_CSV_PATH, FULL_REPORT_PATH, FULL_AUDIT_SHEET_PATH):
        if path.exists():
            raise RuntimeError(f"FULL 工件已存在，拒绝覆盖：{path}")

    immutable_before = immutable_snapshot()
    master_payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    before_rows = copy.deepcopy(master_payload.get("rows", []))
    scope_rows = trial.load_scope_rows()
    target_sources = {trial.clean_text(row.get("来源链接")) for row in scope_rows}
    rows_by_source = {trial.clean_text(row.get("来源链接")): row for row in scope_rows}
    if len(target_sources) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 固定范围不是 297 个唯一来源")

    profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
    before_profile_bytes = preflight_profile_bytes(profile_paths, rows_by_source)
    before_profile_tree = profile_markdown_tree(PROFILE_DIR)
    index_before_sha256 = hashlib.sha256((PROFILE_DIR / "_索引.md").read_bytes()).hexdigest()

    trial_payload = json.loads(trial.TRIAL_JSON_PATH.read_text(encoding="utf-8"))
    trial.validate_payload(trial_payload, require_visual_pass=True, check_artifacts=True)
    if trial.protected_snapshot() != trial_payload["meta"]["protected_assets_after"]:
        raise RuntimeError("FULL 前正式资产与 TRIAL 后快照不一致")
    seed_samples = trial_payload["photo_samples"]
    seed_by_source = {trial.clean_text(item["source_link"]): item for item in seed_samples}
    if len(seed_by_source) != EXPECTED_TRIAL_REUSE_COUNT or not set(seed_by_source) <= target_sources:
        raise RuntimeError("FULL 复用的 10 张 TRIAL 样本范围漂移")

    session = trial.OfficialSession()
    directory_result = session.get(trial.DIRECTORY_URL, referer=trial.OFFICIAL_HOME)
    if directory_result.status != 200 or directory_result.content_type != "text/html":
        raise RuntimeError("FULL 医生目录会话门禁失败")
    directory_html = directory_result.content.decode(directory_result.charset, errors="replace")
    directory_evidence = trial.directory_source_evidence(directory_html)
    api_observed_utc = trial.utc_now()
    api_result = session.get(trial.DIRECTORY_API, referer=trial.DIRECTORY_URL)
    api_payload = trial.decode_json_response(api_result, "FULL 医生目录 API")
    parsed = trial.parse_directory_payload(api_payload)
    category_values = sorted(set(parsed["category_occurrences"]))
    if category_values != [trial.EXPECTED_CATEGORY]:
        raise RuntimeError(f"FULL API 出现未授权 category：{category_values}")
    scope_records, extra_ids = reconcile_scope_with_missing(
        scope_rows, parsed["doctors"], api_observed_utc
    )
    records_by_source = {record["source_link"]: record for record in scope_records}

    with tempfile.TemporaryDirectory(prefix="issue75_full_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_photo_dir = temp_root / "photos"
        temp_photo_dir.mkdir()
        temp_hospital_dir = temp_root / HOSPITAL
        shutil.copytree(PROFILE_DIR, temp_hospital_dir)
        used_names: set[str] = set()
        result_by_source: dict[str, dict[str, Any]] = {}
        reconciliation_by_source: dict[str, dict[str, Any]] = {}
        photo_samples: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []
        status_flicker_count = 0

        def add_success(
            row: dict[str, Any],
            record: dict[str, Any],
            sample: dict[str, Any],
            content: bytes,
            origin: str,
        ) -> None:
            source = trial.clean_text(row.get("来源链接"))
            extension = trial.clean_text(sample.get("extension"))
            if not extension:
                extension = trial.common.magic_extension(content, sample.get("content_type"))
            if not extension:
                raise RuntimeError(f"FULL 照片扩展名缺失：{source}")
            filename, disk_path = allocate_full_photo_path(
                row, extension, temp_photo_dir, used_names
            )
            if origin == "TRIAL_REUSE" and filename != trial.clean_text(sample.get("filename")):
                raise RuntimeError(
                    f"TRIAL 复用照片命名漂移：{sample.get('filename')} -> {filename}"
                )
            disk_path.write_bytes(content)
            width, height = trial.common.image_dimensions(content)
            digest = hashlib.sha256(content).hexdigest()
            photo_url = normalized_photo_reference(record["valid_photo_url"])
            photo_file = (PHOTO_RELATIVE_ROOT / filename).as_posix()
            result_row = dict(row)
            result_row["照片链接"] = photo_url
            result_row["照片文件"] = photo_file
            result_by_source[source] = result_row
            item = {
                "id": trial.source_id(source),
                "name": trial.clean_text(row.get("姓名")),
                "department": trial.atomic_department(row),
                "title": trial.primary_title(row.get("职称身份原文")),
                "source_link": source,
                "api_category": record["api_category"],
                "api_keshi_ids": record["api_keshi_ids"],
                "api_image_field_value": record["api_image_field_value"],
                "photo_url": photo_url,
                "photo_final_url": trial.clean_text(sample.get("photo_final_url")) or photo_url,
                "photo_file": photo_file,
                "filename": filename,
                "extension": extension,
                "content_type": trial.clean_text(sample.get("content_type")),
                "bytes": len(content),
                "width": width,
                "height": height,
                "sha256": digest,
                "origin": origin,
                "photo_attempts": sample.get("photo_attempts", []),
            }
            photo_samples.append(item)
            reconciliation_by_source[source] = {
                "ID": item["id"],
                "姓名": item["name"],
                "来源链接": source,
                "状态": "实采",
                "失败分类": "",
                "分类状态": "FINAL",
                "API category": record["api_category"],
                "API keshi_ids": record["api_keshi_ids"],
                "API image 字段原值": record["api_image_field_value"],
                "照片链接": photo_url,
                "照片文件": photo_file,
                "实际格式": extension,
                "字节数": len(content),
                "SHA-256": digest,
                "宽": width,
                "高": height,
                "来源批次": origin,
                "错误证据": "",
            }

        def record_failure(
            row: dict[str, Any],
            record: dict[str, Any],
            state: str,
            warning: str,
            detection_feature: str,
            attempts: list[dict[str, Any]] | None = None,
            classification_status: str = "FINAL",
        ) -> None:
            source = trial.clean_text(row.get("来源链接"))
            evidence = {
                "observed_utc": record["observed_utc"],
                "api_category": record["api_category"],
                "api_image_field_value": record["api_image_field_value"],
                "image_signal": record["image_signal"],
                "detection_feature": detection_feature,
            }
            error = failure_evidence_text(evidence)
            result_row = dict(row)
            result_row["照片链接"] = ""
            result_row["照片文件"] = ""
            result_row["异常提示"] = append_warning(result_row.get("异常提示"), warning)
            result_by_source[source] = result_row
            failures.append(
                {
                    "id": record["id"],
                    "name": record["name"],
                    "source_link": source,
                    "state": state,
                    "classification_status": classification_status,
                    "error": error,
                    "evidence": evidence,
                    "attempts": attempts or [],
                    "origin": "FULL_API_SIGNAL" if not attempts else "FULL_FETCH",
                }
            )
            reconciliation_by_source[source] = {
                "ID": record["id"],
                "姓名": record["name"],
                "来源链接": source,
                "状态": "失败留空",
                "失败分类": state,
                "分类状态": classification_status,
                "API category": record["api_category"],
                "API keshi_ids": record["api_keshi_ids"],
                "API image 字段原值": record["api_image_field_value"],
                "照片链接": "",
                "照片文件": "",
                "实际格式": "",
                "字节数": "",
                "SHA-256": "",
                "宽": "",
                "高": "",
                "来源批次": "FULL_API_SIGNAL" if not attempts else "FULL_FETCH",
                "错误证据": error,
            }

        for index, row in enumerate(scope_rows, start=1):
            source = trial.clean_text(row.get("来源链接"))
            record = records_by_source[source]
            signal = record["image_signal"]
            if signal == "DETAIL_UNREACHABLE_API_ID_MISSING":
                record_failure(
                    row,
                    record,
                    "详情不可达",
                    DETAIL_MISSING_WARNING,
                    "固定底表 ID 未出现在本次 category=55 API 科室树对象中",
                )
            elif signal == "NO_PHOTO_CONTAINER_EMPTY_IMAGE_FIELD":
                record_failure(
                    row,
                    record,
                    "无照片容器",
                    NO_PHOTO_WARNING,
                    "API image 字段为空/null；页面 fallback 为 ./images/null.jpg，未下载 fallback",
                )
            elif signal == "NO_PHOTO_CONTAINER_NON_UPLOAD_IMAGE_FIELD":
                record_failure(
                    row,
                    record,
                    "无照片容器",
                    NON_UPLOAD_WARNING,
                    "API image 字段非空但不是获准 /uploads 原图；未请求、未构造路径",
                    classification_status="OWNER_FINAL_CLASSIFICATION_REQUIRED",
                )
            elif signal == "VALID_REFERENCED_ORIGINAL":
                if source in seed_by_source:
                    sample = seed_by_source[source]
                    if normalized_photo_reference(sample["photo_url"]) != record["valid_photo_url"]:
                        raise RuntimeError(f"TRIAL 复用 URL 与 FULL API image 漂移：{source}")
                    content = (ROOT / trial.clean_text(sample["disk_path"])).read_bytes()
                    add_success(row, record, sample, content, "TRIAL_REUSE")
                else:
                    photo, attempts = trial.fetch_photo_with_retry(
                        session, record["valid_photo_url"], source
                    )
                    statuses = {
                        item.get("status") for item in attempts if item.get("status") is not None
                    }
                    had_error = any(item.get("error") for item in attempts)
                    if len(statuses) > 1 or (had_error and photo.status == 200):
                        status_flicker_count += 1
                        raise RuntimeError(
                            "STATUS_FLICKER_REQUIRES_PR_COMMENT_AND_AGGREGATION: "
                            f"{record['valid_photo_url']} attempts={attempts}"
                        )
                    if photo.status != 200:
                        record_failure(
                            row,
                            record,
                            "照片资源不可达",
                            RESOURCE_UNREACHABLE_WARNING,
                            "API image 引用唯一原图连续两次不可达",
                            attempts,
                        )
                    else:
                        if trial.comparable_host(photo.final_url) != trial.OFFICIAL_HOST:
                            raise RuntimeError(
                                f"照片重定向越出官网：{record['valid_photo_url']} -> {photo.final_url}"
                            )
                        extension = trial.common.magic_extension(photo.content, photo.content_type)
                        if not extension:
                            raise RuntimeError(
                                "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 照片格式异常："
                                f"{record['name']} {record['valid_photo_url']} {photo.content_type}"
                            )
                        if len(photo.content) > trial.MAX_PHOTO_BYTES:
                            raise RuntimeError(
                                "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 单图超过 20 MiB："
                                f"{record['name']} {len(photo.content)}"
                            )
                        width, height = trial.common.image_dimensions(photo.content)
                        placeholder = placeholder_response_reason(
                            record["valid_photo_url"], photo.content, width, height
                        )
                        if placeholder:
                            record_failure(
                                row,
                                record,
                                "占位图",
                                PLACEHOLDER_WARNING,
                                placeholder,
                                attempts,
                            )
                        else:
                            add_success(
                                row,
                                record,
                                {
                                    "extension": extension,
                                    "content_type": photo.content_type,
                                    "photo_final_url": photo.final_url,
                                    "photo_attempts": attempts,
                                },
                                photo.content,
                                "FULL_FETCH",
                            )
            else:
                raise RuntimeError(f"未知 image 信号：{signal}")
            if index % 25 == 0 or index == EXPECTED_SCOPE_COUNT:
                print(
                    f"[FULL] {index}/{EXPECTED_SCOPE_COUNT} 实采={len(photo_samples)} 失败={len(failures)}",
                    flush=True,
                )

        if set(result_by_source) != target_sources:
            raise RuntimeError("FULL 297 行结果来源集合未闭合")
        result_rows = [
            result_by_source[trial.clean_text(row.get("来源链接"))] for row in scope_rows
        ]
        reconciliation = [
            reconciliation_by_source[trial.clean_text(row.get("来源链接"))]
            for row in scope_rows
        ]
        updated_by_source = {
            trial.clean_text(row.get("来源链接")): row for row in result_rows
        }
        after_rows = [
            copy.deepcopy(updated_by_source.get(trial.clean_text(row.get("来源链接")), row))
            for row in before_rows
        ]
        headers = list(collector.BASE_HEADERS)
        row_diffs = collect_full_row_diffs(
            before_rows, after_rows, target_sources, headers
        )
        updated_master = copy.deepcopy(master_payload)
        updated_master["rows"] = after_rows
        recompute_master_derivatives(updated_master, after_rows)

        temp_master_payload = temp_root / MASTER_JSON_PATH.name
        temp_master_csv = temp_root / MASTER_CSV_PATH.name
        temp_master_xlsx = temp_root / MASTER_XLSX_PATH.name
        temp_master_preview = temp_root / "master_preview.png"
        temp_master_payload.write_text(
            json.dumps(updated_master, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_master_csv(temp_master_csv, after_rows, headers)
        collector.build_workbook(temp_master_payload, temp_master_xlsx, temp_master_preview)
        validate_master_layers(temp_master_payload, temp_master_csv, temp_master_xlsx)

        temp_profile_paths = target_profile_paths(temp_hospital_dir, target_sources)
        photos_by_source = {item["source_link"]: item for item in photo_samples}
        success_sources = set(photos_by_source)
        for source in success_sources:
            item = photos_by_source[source]
            path = temp_profile_paths[source]
            path.write_bytes(
                insert_profile_photo_block_bytes(
                    before_profile_bytes[source], item["name"], item["photo_file"]
                )
            )
            validate_profile_photo_only_bytes(
                before_profile_bytes[source], path.read_bytes(), item["name"], item["photo_file"]
            )
        expected_changed_paths = {
            profile_paths[source].relative_to(PROFILE_DIR) for source in success_sources
        }
        validate_profile_tree_surgical(
            before_profile_tree, temp_hospital_dir, expected_changed_paths
        )
        if hashlib.sha256((temp_hospital_dir / "_索引.md").read_bytes()).hexdigest() != index_before_sha256:
            raise RuntimeError("FULL 临时事务修改了 _索引.md")

        profile_integrity: list[dict[str, Any]] = []
        for source in sorted(target_sources):
            before_content = before_profile_bytes[source]
            after_content = temp_profile_paths[source].read_bytes()
            success = source in success_sources
            profile_integrity.append(
                {
                    "source_link": source,
                    "path": str(profile_paths[source].relative_to(ROOT)),
                    "status": "实采" if success else "失败留空",
                    "before_sha256": hashlib.sha256(before_content).hexdigest(),
                    "after_sha256": hashlib.sha256(after_content).hexdigest(),
                    "added_lines": 2 if success else 0,
                    "removed_lines": 0,
                }
            )

        temp_audit_sheet = temp_root / FULL_AUDIT_SHEET_PATH.name
        audit_samples = build_full_audit_sheet(
            photo_samples, temp_photo_dir, temp_audit_sheet
        )
        state_counter = Counter(item["state"] for item in failures)
        non_upload_review = [
            {
                "id": item["id"],
                "name": item["name"],
                "source_link": item["source_link"],
                "api_image_field_value": item["evidence"]["api_image_field_value"],
                "classification_status": item["classification_status"],
                "observed_utc": item["evidence"]["observed_utc"],
            }
            for item in failures
            if item["classification_status"] == "OWNER_FINAL_CLASSIFICATION_REQUIRED"
        ]
        duplicate_groups: dict[str, list[str]] = defaultdict(list)
        for item in photo_samples:
            duplicate_groups[item["sha256"]].append(item["source_link"])
        duplicate_groups = {
            digest: sources for digest, sources in duplicate_groups.items() if len(sources) > 1
        }
        total_bytes = sum(int(item["bytes"]) for item in photo_samples)
        immutable_after_preinstall = immutable_snapshot()
        full_payload = {
            "meta": {
                "issue": ISSUE_NUMBER,
                "branch": BRANCH,
                "phase": "FULL_READY_FOR_FINAL_OWNER_AUDIT",
                "hospital": HOSPITAL,
                "run_date": run_date,
                "authorization": FULL_AUTHORIZATION,
                "expected_count": EXPECTED_SCOPE_COUNT,
                "downloaded_count": len(photo_samples),
                "failed_count": len(failures),
                "blank_count": len(failures),
                "disk_photo_count": len(photo_samples),
                "failure_state_counts": {
                    state: state_counter.get(state, 0) for state in FULL_FAILURE_STATES
                },
                "empty_image_count": sum(
                    item["image_signal"] == "NO_PHOTO_CONTAINER_EMPTY_IMAGE_FIELD"
                    for item in scope_records
                ),
                "non_upload_review_count": len(non_upload_review),
                "trial_reused_count": sum(
                    item["origin"] == "TRIAL_REUSE" for item in photo_samples
                ),
                "fresh_target_count": EXPECTED_FRESH_COUNT,
                "fresh_downloaded_count": sum(
                    item["origin"] == "FULL_FETCH" for item in photo_samples
                ),
                "fresh_failed_count": len(failures),
                "category_values": category_values,
                "api_object_occurrence_count": len(parsed["category_occurrences"]),
                "api_missing_fixed_id_count": sum(
                    item["image_signal"] == "DETAIL_UNREACHABLE_API_ID_MISSING"
                    for item in scope_records
                ),
                "api_extra_scope_id_count": len(extra_ids),
                "other_category_request_count": 0,
                "undeclared_api_probe_count": 0,
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "status_flicker_count": status_flicker_count,
                "photo_total_bytes": total_bytes,
                "photo_total_mib": total_bytes / 1024 / 1024,
                "photo_max_bytes": max(int(item["bytes"]) for item in photo_samples),
                "size_bucket_counts": trial.size_buckets(photo_samples),
                "over_5mib_count": sum(
                    int(item["bytes"]) > trial.OWNER_REPORT_BYTES for item in photo_samples
                ),
                "over_20mib_count": sum(
                    int(item["bytes"]) > trial.MAX_PHOTO_BYTES for item in photo_samples
                ),
                "format_counts": dict(Counter(item["extension"] for item in photo_samples)),
                "duplicate_sha256_group_count": len(duplicate_groups),
                "existing_profile_count": len(profile_paths),
                "profile_refreshed_count": len(success_sources),
                "profile_untouched_count": EXPECTED_SCOPE_COUNT - len(success_sources),
                "profile_index_before_sha256": index_before_sha256,
                "row_diff_count": len(row_diffs),
                "row_diff_columns": dict(Counter(item["列名"] for item in row_diffs)),
                "audit_sheet_sha256": hashlib.sha256(temp_audit_sheet.read_bytes()).hexdigest(),
                "directory_source_evidence": directory_evidence,
                "immutable_before": immutable_before,
                "immutable_after_preinstall": immutable_after_preinstall,
            },
            "api_trace": {
                "url": trial.DIRECTORY_API,
                "method": "GET",
                "query": {"category": trial.EXPECTED_CATEGORY},
                "status": api_result.status,
                "content_type": api_result.content_type,
                "final_url": api_result.final_url,
                "bytes": len(api_result.content),
                "sha256": hashlib.sha256(api_result.content).hexdigest(),
                "observed_utc": api_observed_utc,
            },
            "scope_records": scope_records,
            "api_extra_scope_ids": extra_ids,
            "failures": failures,
            "non_upload_review": non_upload_review,
            "photo_samples": photo_samples,
            "duplicate_sha256_groups": duplicate_groups,
            "reconciliation": reconciliation,
            "row_diffs": row_diffs,
            "rows": result_rows,
            "profile_integrity": profile_integrity,
            "audit_samples": audit_samples,
        }
        validate_full_payload(full_payload, temp_photo_dir, temp_audit_sheet)

        temp_full_payload = temp_root / FULL_JSON_PATH.name
        temp_full_csv = temp_root / FULL_CSV_PATH.name
        temp_full_report = temp_root / FULL_REPORT_PATH.name
        temp_full_payload.write_text(
            json.dumps(full_payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_reconciliation_csv(temp_full_csv, full_payload)
        write_full_report(temp_full_report, full_payload)

        file_map: dict[Path, Path] = {
            MASTER_JSON_PATH: temp_master_payload,
            MASTER_CSV_PATH: temp_master_csv,
            MASTER_XLSX_PATH: temp_master_xlsx,
            FULL_JSON_PATH: temp_full_payload,
            FULL_CSV_PATH: temp_full_csv,
            FULL_REPORT_PATH: temp_full_report,
            FULL_AUDIT_SHEET_PATH: temp_audit_sheet,
        }
        for source in success_sources:
            file_map[profile_paths[source]] = temp_profile_paths[source]
        backups = backup_file_targets(list(file_map), temp_root / "file_backups")
        photo_swapped = False
        try:
            ensure_workspace_target(FORMAL_PHOTO_DIR)
            temp_photo_dir.replace(FORMAL_PHOTO_DIR)
            photo_swapped = True
            apply_file_map(file_map)
            final_rows = validate_master_layers(
                MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH
            )
            if collect_full_row_diffs(
                before_rows, final_rows, target_sources, headers
            ) != row_diffs:
                raise RuntimeError("FULL 落盘后的逐单元格差异与预期不一致")
            validate_full_installation(full_payload)
        except Exception:
            restore_file_targets(backups)
            if photo_swapped and FORMAL_PHOTO_DIR.exists():
                ensure_workspace_target(FORMAL_PHOTO_DIR)
                shutil.rmtree(FORMAL_PHOTO_DIR)
            raise
        return full_payload


def load_full_payload() -> dict[str, Any]:
    if not FULL_JSON_PATH.is_file():
        raise RuntimeError(f"FULL payload 不存在：{FULL_JSON_PATH}")
    payload = json.loads(FULL_JSON_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("FULL payload 顶层不是对象")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Issue #75 广州医科大学附属口腔医院照片补录 FULL"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--full", action="store_true", help="执行 297 行 FULL 事务")
    mode.add_argument("--validate", action="store_true", help="验证已落盘 FULL")
    parser.add_argument("--run-date", default=str(date.today()), help="执行日期 YYYY-MM-DD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.full:
        payload = run_full(args.run_date)
        print(
            "FULL_DONE "
            f"expected={payload['meta']['expected_count']} "
            f"downloaded={payload['meta']['downloaded_count']} "
            f"failed={payload['meta']['failed_count']} "
            f"profiles={payload['meta']['profile_refreshed_count']}"
        )
        return
    payload = load_full_payload()
    validate_full_installation(payload)
    print(
        "FULL_VALIDATED "
        f"expected={payload['meta']['expected_count']} "
        f"downloaded={payload['meta']['downloaded_count']} "
        f"failed={payload['meta']['failed_count']}"
    )


if __name__ == "__main__":
    main()
