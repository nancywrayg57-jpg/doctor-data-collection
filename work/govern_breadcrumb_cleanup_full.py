from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import shutil
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import collect_official_doctors_batch as collector
import govern_breadcrumb_cleanup_trial as trial


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
PROFILE_ROOT = VAULT / "01_试点医院"
SOURCE_DIR = VAULT / "99_资料来源"
MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_PAYLOAD = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_REPORT = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
LEDGER = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"

ISSUE_NUMBER = 87
PHASE = "FULL_CLEANUP_AND_SYNC"
OWNER_COMMENT_ID = 5351062056
EXPECTED_MASTER_ROWS = 9222
EXPECTED_CELL_CHANGES = 596
EXPECTED_PROFILE_FILES = 242
EXPECTED_PROFILE_REPLACEMENTS = 288
EXPECTED_RETAINED_OUT_OF_SCOPE_MARKER_CELLS = 53
EXPECTED_RETAINED_OUT_OF_SCOPE_BY_COLUMN = {
    "亮眼经历线索": 46,
    "擅长诊疗方向摘录": 7,
}
ALLOWED_COLUMN = "详情正文摘录"

FULL_BASENAME = "GOVERN-2_导航文本污染清理_full"
EVIDENCE_PATH = WORK_DIR / f"{FULL_BASENAME}_evidence.json"
RECONCILIATION_PATH = WORK_DIR / f"{FULL_BASENAME}_reconciliation.csv"
SUMMARY_PATH = WORK_DIR / f"{FULL_BASENAME}_summary.md"

RECONCILIATION_FIELDS = (
    "row_number",
    "sequence",
    "hospital",
    "name",
    "source_link",
    "column",
    "removed_length",
    "original_sha256",
    "remaining_sha256",
    "profile_path",
    "profile_replacements",
    "profile_before_sha256",
    "profile_after_sha256",
)
MARKER_BYTES = ("面包屑".encode("utf-8"), "导航痕迹".encode("utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def row_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def normalized_row(row: dict[str, Any]) -> dict[str, str]:
    return {header: row_value(row.get(header)) for header in collector.BASE_HEADERS}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def digest_selected(paths: Iterable[Path], root: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    count = 0
    raw_bytes = 0
    for path in sorted({item.resolve() for item in paths}):
        if not path.is_file():
            continue
        try:
            relative = path.relative_to(root.resolve()).as_posix()
        except ValueError as exc:
            raise RuntimeError(f"摘要路径越界：{path}") from exc
        data = trial.repository_digest_bytes(path)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
        count += 1
        raw_bytes += path.stat().st_size
    return {"file_count": count, "bytes": raw_bytes, "sha256": digest.hexdigest()}


def protected_snapshot(target_profiles: set[Path]) -> dict[str, Any]:
    resolved_targets = {path.resolve() for path in target_profiles}
    excluded = {MASTER_CSV.resolve(), MASTER_XLSX.resolve(), *resolved_targets}
    transient_suffixes = {".tmp", ".temp", ".lock"}
    protected_vault_files = [
        path
        for path in VAULT.rglob("*")
        if path.is_file()
        and path.resolve() not in excluded
        and path.name != "_索引.md"
        and path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}
        and path.suffix.lower() not in transient_suffixes
        and not path.name.startswith("~$")
    ]
    indexes = [path for path in PROFILE_ROOT.rglob("_索引.md") if path.is_file()]
    photos = [
        path
        for path in PROFILE_ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    ]
    return {
        "protected_vault": digest_selected(protected_vault_files, VAULT),
        "indexes": digest_selected(indexes, PROFILE_ROOT),
        "photos": digest_selected(photos, PROFILE_ROOT),
        "ledger": trial.digest_path(LEDGER),
        "master_report": trial.digest_path(MASTER_REPORT),
        "retired_prompt": trial.digest_path(ROOT / "docs" / "agent_prompts" / "codex_next_prompt.md"),
    }


def load_master_payload_and_layers() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(MASTER_PAYLOAD.read_text(encoding="utf-8"))
    payload_rows = payload.get("rows")
    if not isinstance(payload_rows, list) or not payload_rows:
        raise RuntimeError("主 payload 缺少有效 rows")
    with MASTER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    xlsx_rows = collector.read_bottom_table_rows(MASTER_XLSX)
    compare_layers(payload_rows, csv_rows, xlsx_rows)
    return payload, payload_rows


def compare_layers(
    payload_rows: list[dict[str, Any]],
    csv_rows: list[dict[str, Any]],
    xlsx_rows: list[dict[str, Any]],
) -> None:
    if not (len(payload_rows) == len(csv_rows) == len(xlsx_rows)):
        raise RuntimeError(
            "三载体行数不一致："
            f"payload={len(payload_rows)}、CSV={len(csv_rows)}、XLSX={len(xlsx_rows)}"
        )
    for row_number, (payload_row, csv_row, xlsx_row) in enumerate(
        zip(payload_rows, csv_rows, xlsx_rows, strict=True), start=2
    ):
        expected = normalized_row(payload_row)
        if normalized_row(csv_row) != expected:
            raise RuntimeError(f"payload 与 CSV 在底表第 {row_number} 行不一致")
        if normalized_row(xlsx_row) != expected:
            raise RuntimeError(f"payload 与 XLSX 在底表第 {row_number} 行不一致")


def load_trial_evidence(require_current_snapshot: bool) -> dict[str, Any]:
    if require_current_snapshot:
        payload = trial.validate_outputs()
    else:
        payload = json.loads(trial.PAYLOAD_PATH.read_text(encoding="utf-8"))
        trial.validate_payload(payload, require_current_snapshot=False)
    return payload


def validate_owner_full_scope(trial_payload: dict[str, Any]) -> None:
    manifest = trial_payload.get("manifest", [])
    profiles = trial_payload.get("profile_impact", [])
    errors: list[str] = []
    if len(manifest) != EXPECTED_CELL_CHANGES:
        errors.append(f"manifest 不是 {EXPECTED_CELL_CHANGES} 行")
    if len(profiles) != EXPECTED_PROFILE_FILES:
        errors.append(f"profile impact 不是 {EXPECTED_PROFILE_FILES} 份")
    if any(item.get("segment_position") != "START" for item in manifest):
        errors.append("存在非 START 导航段，触发 Owner FULL 熔断")
    if any(item.get("quote_boundary_status") != "NO_ADJACENT_QUOTE" for item in manifest):
        errors.append("存在邻接孤立撇号，触发 Owner FULL 熔断")
    if sum(int(item.get("marker_occurrences", 0)) for item in profiles) != EXPECTED_PROFILE_REPLACEMENTS:
        errors.append(f"画像 marker 合计不是 {EXPECTED_PROFILE_REPLACEMENTS}")
    if errors:
        raise RuntimeError("[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 范围门禁失败：\n- " + "\n- ".join(errors))


def apply_master_changes(
    rows: list[dict[str, Any]], manifest: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    seen_rows: set[int] = set()
    changes: list[dict[str, Any]] = []
    for item in manifest:
        row_number = int(item["row_number"])
        if row_number in seen_rows:
            raise RuntimeError(f"manifest 底表行重复：{row_number}")
        seen_rows.add(row_number)
        index = row_number - 2
        if index < 0 or index >= len(rows):
            raise RuntimeError(f"manifest 底表行越界：{row_number}")
        row = rows[index]
        if row_value(row.get("医院")) != item["hospital"]:
            raise RuntimeError(f"底表第 {row_number} 行医院漂移")
        if row_value(row.get("来源链接")) != item["source_link"]:
            raise RuntimeError(f"底表第 {row_number} 行来源链接漂移")
        original = row_value(row.get(ALLOWED_COLUMN))
        segment = item["removed_segment"]
        start = int(item["segment_start"])
        end = int(item["segment_end"])
        if start != 0 or item["segment_position"] != "START":
            raise RuntimeError(f"底表第 {row_number} 行出现非 START 导航段")
        if item["quote_boundary_status"] != "NO_ADJACENT_QUOTE":
            raise RuntimeError(f"底表第 {row_number} 行出现邻接孤立撇号")
        if sha256_text(original) != item["original_sha256"]:
            raise RuntimeError(f"底表第 {row_number} 行 original_sha256 漂移")
        if original[start:end] != segment or not original.startswith(segment):
            raise RuntimeError(f"底表第 {row_number} 行删除边界漂移")
        remaining = original[:start] + original[end:]
        if sha256_text(remaining) != item["remaining_sha256"]:
            raise RuntimeError(f"底表第 {row_number} 行 remaining_sha256 不一致")
        if "面包屑" in remaining or "导航痕迹" in remaining:
            raise RuntimeError(f"底表第 {row_number} 行清理后仍有导航标记")
        row[ALLOWED_COLUMN] = remaining
        changes.append(
            {
                "row_number": row_number,
                "sequence": row_value(row.get("序号")),
                "hospital": item["hospital"],
                "name": row_value(row.get("姓名")),
                "source_link": item["source_link"],
                "column": ALLOWED_COLUMN,
                "removed_length": len(segment),
                "original_sha256": item["original_sha256"],
                "remaining_sha256": item["remaining_sha256"],
            }
        )
    if len(changes) != EXPECTED_CELL_CHANGES:
        raise RuntimeError(f"底表处理数不是 {EXPECTED_CELL_CHANGES}")
    return changes


def collect_cell_diffs(
    before_rows: list[dict[str, Any]], after_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    if len(before_rows) != len(after_rows):
        raise RuntimeError("治理前后总底表行数变化")
    diffs: list[dict[str, Any]] = []
    for row_number, (before, after) in enumerate(
        zip(before_rows, after_rows, strict=True), start=2
    ):
        for column in collector.BASE_HEADERS:
            old = row_value(before.get(column))
            new = row_value(after.get(column))
            if old != new:
                diffs.append({"row_number": row_number, "column": column, "before": old, "after": new})
    unexpected = sorted({item["column"] for item in diffs} - {ALLOWED_COLUMN})
    if unexpected:
        raise RuntimeError("发现越界字段修改：" + "、".join(unexpected))
    if len(diffs) != EXPECTED_CELL_CHANGES:
        raise RuntimeError(f"逐单元格差异不是 {EXPECTED_CELL_CHANGES} 个：{len(diffs)}")
    return diffs


def profile_path_from_item(item: dict[str, Any]) -> Path:
    path = (ROOT / item["profile_path"]).resolve()
    try:
        path.relative_to(PROFILE_ROOT.resolve())
    except ValueError as exc:
        raise RuntimeError(f"画像路径越出正式画像根目录：{path}") from exc
    if path.name == "_索引.md":
        raise RuntimeError(f"画像工作集意外包含索引：{path}")
    return path


def build_profile_outputs(
    temp_profile_root: Path,
    profile_impact: list[dict[str, Any]],
    manifest: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[Path, Path]]:
    by_source: dict[str, dict[str, Any]] = {}
    for item in manifest:
        source = item["source_link"]
        if source in by_source:
            raise RuntimeError(f"画像映射来源在 manifest 不唯一：{source}")
        by_source[source] = item
    changes: list[dict[str, Any]] = []
    file_map: dict[Path, Path] = {}
    total_replacements = 0
    for impact in profile_impact:
        target = profile_path_from_item(impact)
        if target in file_map:
            raise RuntimeError(f"画像路径重复：{target}")
        manifest_item = by_source.get(impact["source_link"])
        if manifest_item is None:
            raise RuntimeError(f"画像来源未映射到底表 manifest：{impact['source_link']}")
        original = target.read_bytes()
        segment = manifest_item["removed_segment"].encode("utf-8")
        expected = int(impact["marker_occurrences"])
        actual = original.count(segment)
        if actual != expected:
            raise RuntimeError(
                f"画像 exact segment 次数漂移：{trial.repo_relative(target)} "
                f"expected={expected} actual={actual}"
            )
        updated = original.replace(segment, b"")
        if updated == original or any(marker in updated for marker in MARKER_BYTES):
            raise RuntimeError(f"画像清理不闭合：{trial.repo_relative(target)}")
        relative = target.relative_to(PROFILE_ROOT)
        temporary = temp_profile_root / relative
        temporary.parent.mkdir(parents=True, exist_ok=True)
        temporary.write_bytes(updated)
        file_map[target] = temporary
        total_replacements += actual
        changes.append(
            {
                "hospital": impact["hospital"],
                "profile_path": trial.repo_relative(target),
                "source_link": impact["source_link"],
                "master_row_number": int(impact["master_row_number"]),
                "replacements": actual,
                "carrier_line_numbers": impact["carrier_line_numbers"],
                "carrier_sections": impact["carrier_sections"],
                "before_bytes": len(original),
                "after_bytes": len(updated),
                "before_sha256": sha256_bytes(original),
                "after_sha256": sha256_bytes(updated),
            }
        )
    if len(changes) != EXPECTED_PROFILE_FILES:
        raise RuntimeError(f"画像处理文件不是 {EXPECTED_PROFILE_FILES} 份")
    if total_replacements != EXPECTED_PROFILE_REPLACEMENTS:
        raise RuntimeError(f"画像替换次数不是 {EXPECTED_PROFILE_REPLACEMENTS}：{total_replacements}")
    return changes, file_map


def validate_profile_outputs(
    profile_changes: list[dict[str, Any]], file_map: dict[Path, Path]
) -> None:
    if len(profile_changes) != EXPECTED_PROFILE_FILES or len(file_map) != EXPECTED_PROFILE_FILES:
        raise RuntimeError("临时画像文件数不闭合")
    for change in profile_changes:
        target = (ROOT / change["profile_path"]).resolve()
        temporary = file_map[target]
        data = temporary.read_bytes()
        if sha256_bytes(data) != change["after_sha256"]:
            raise RuntimeError(f"临时画像摘要不一致：{change['profile_path']}")
        if any(marker in data for marker in MARKER_BYTES):
            raise RuntimeError(f"临时画像仍有导航标记：{change['profile_path']}")


def marker_scan(root: Path) -> list[str]:
    matches: list[str] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if path.suffix.lower() not in trial.TEXT_EXTENSIONS:
            continue
        data = path.read_bytes()
        if any(marker in data for marker in MARKER_BYTES):
            matches.append(path.relative_to(root).as_posix())
    return matches


def retained_out_of_scope_marker_cells(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    retained: list[dict[str, Any]] = []
    for row_number, row in enumerate(rows, start=2):
        for column in collector.BASE_HEADERS:
            if column == ALLOWED_COLUMN:
                continue
            value = row_value(row.get(column))
            if "面包屑" not in value and "导航痕迹" not in value:
                continue
            retained.append(
                {
                    "row_number": row_number,
                    "hospital": row_value(row.get("医院")),
                    "name": row_value(row.get("姓名")),
                    "source_link": row_value(row.get("来源链接")),
                    "column": column,
                    "sha256": sha256_text(value),
                }
            )
    return retained


def validate_revised_scan_scope(
    rows: list[dict[str, Any]], target_profiles: Iterable[Path]
) -> dict[str, Any]:
    detail_marker_rows = [
        row_number
        for row_number, row in enumerate(rows, start=2)
        if "面包屑" in row_value(row.get(ALLOWED_COLUMN))
        or "导航痕迹" in row_value(row.get(ALLOWED_COLUMN))
    ]
    profile_marker_files = [
        trial.repo_relative(path)
        for path in sorted(target_profiles)
        if any(marker in path.read_bytes() for marker in MARKER_BYTES)
    ]
    retained = retained_out_of_scope_marker_cells(rows)
    retained_counts = dict(Counter(item["column"] for item in retained))
    if len(retained) != EXPECTED_RETAINED_OUT_OF_SCOPE_MARKER_CELLS:
        raise RuntimeError(
            "管理员修订扫描口径下的范围外留存单元格不是 "
            f"{EXPECTED_RETAINED_OUT_OF_SCOPE_MARKER_CELLS}：{len(retained)}"
        )
    if retained_counts != EXPECTED_RETAINED_OUT_OF_SCOPE_BY_COLUMN:
        raise RuntimeError(f"范围外留存列分组漂移：{retained_counts}")
    return {
        "detail_marker_rows": detail_marker_rows,
        "profile_marker_files": profile_marker_files,
        "retained_out_of_scope_cells": retained,
        "retained_out_of_scope_by_column": retained_counts,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_reconciliation(
    path: Path,
    master_changes: list[dict[str, Any]],
    profile_changes: list[dict[str, Any]],
) -> None:
    profile_by_source = {item["source_link"]: item for item in profile_changes}
    rows: list[dict[str, Any]] = []
    for change in master_changes:
        profile = profile_by_source.get(change["source_link"], {})
        rows.append(
            {
                **change,
                "profile_path": profile.get("profile_path", ""),
                "profile_replacements": profile.get("replacements", 0),
                "profile_before_sha256": profile.get("before_sha256", ""),
                "profile_after_sha256": profile.get("after_sha256", ""),
            }
        )
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RECONCILIATION_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, evidence: dict[str, Any]) -> None:
    meta = evidence["meta"]
    lines = [
        "# Issue #87 GOVERN-2 导航文本污染清理 FULL 报告",
        "",
        f"- Owner 授权：PR #88 comment `{OWNER_COMMENT_ID}`，`TRIAL_AUDIT_PASSED → FULL_CLEANUP_AND_SYNC`。",
        f"- 总底表：{meta['master_cell_changes']} 个 `详情正文摘录` 单元格；其他列差异 0。",
        f"- 三载体：payload/CSV/XLSX 各 {meta['master_rows']} 行且逐值一致。",
        f"- 画像：{meta['profile_files_changed']} 份，精确清除 {meta['profile_replacements']} 处导航载体。",
        "- 管理员修订验收扫描范围：596 个 `详情正文摘录` 单元格 + 242 份授权画像，最终命中 0。",
        f"- 范围外留存：{meta['retained_out_of_scope_marker_cells']} 个既有单元格（亮眼经历线索 46、擅长诊疗方向摘录 7），本批零修改。",
        "- 入口台账、更新报告、全部 `_索引.md`、照片以及非目标画像保持仓库摘要不变。",
        "",
        "## 严格边界",
        "",
        "1. 596/596 manifest 行必须为 `START`，且必须为 `NO_ADJACENT_QUOTE`；否则在写入前熔断。",
        "2. 只按 manifest 的 `segment_start/end` 与 SHA-256 双向校验更新 `详情正文摘录`。",
        "3. 画像只按来源链接映射 manifest，并删除 242 份文件中 288 个完全一致的 `removed_segment` 字节串。",
        "4. 管理员在两次安全回滚后裁决修订扫描口径，不扩大到 53 个其他列单元格；继续保持其他列零修改。",
        "5. 不修改姓名、行性质、复核状态、异常提示、其他列、照片、索引、台账、更新报告或退役提示词。",
        "",
        "当前阶段：`FULL_DONE_WAITING_FOR_OWNER_FINAL_AUDIT`。不得自行合并 PR #88 或关闭 Issue #87。",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def backup_targets(paths: Iterable[Path], backup_root: Path) -> dict[Path, Path | None]:
    backups: dict[Path, Path | None] = {}
    for target in paths:
        if not target.exists():
            backups[target] = None
            continue
        backup = backup_root / target.relative_to(ROOT)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
        backups[target] = backup
    return backups


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


def ensure_outputs_absent() -> None:
    existing = [
        trial.repo_relative(path)
        for path in (EVIDENCE_PATH, RECONCILIATION_PATH, SUMMARY_PATH)
        if path.exists()
    ]
    if existing:
        raise RuntimeError("FULL 输出已存在，拒绝覆盖：\n- " + "\n- ".join(existing))


def validate_live_full(evidence: dict[str, Any]) -> dict[str, Any]:
    trial_payload = load_trial_evidence(require_current_snapshot=False)
    validate_owner_full_scope(trial_payload)
    manifest = trial_payload["manifest"]
    profile_changes = evidence.get("profile_changes", [])
    payload, rows = load_master_payload_and_layers()
    del payload
    if len(rows) != EXPECTED_MASTER_ROWS:
        raise RuntimeError(f"FULL 后总底表不是 {EXPECTED_MASTER_ROWS} 行")
    for item in manifest:
        row_number = int(item["row_number"])
        value = row_value(rows[row_number - 2].get(ALLOWED_COLUMN))
        if sha256_text(value) != item["remaining_sha256"]:
            raise RuntimeError(f"FULL 后底表第 {row_number} 行未命中 remaining_sha256")
        if "面包屑" in value or "导航痕迹" in value:
            raise RuntimeError(f"FULL 后底表第 {row_number} 行仍有导航标记")
    if len(profile_changes) != EXPECTED_PROFILE_FILES:
        raise RuntimeError("FULL evidence 画像记录数漂移")
    target_profiles: set[Path] = set()
    replacement_total = 0
    for change in profile_changes:
        path = (ROOT / change["profile_path"]).resolve()
        target_profiles.add(path)
        data = path.read_bytes()
        if sha256_bytes(data) != change["after_sha256"]:
            raise RuntimeError(f"FULL 后画像摘要不一致：{change['profile_path']}")
        if any(marker in data for marker in MARKER_BYTES):
            raise RuntimeError(f"FULL 后画像仍有导航标记：{change['profile_path']}")
        replacement_total += int(change["replacements"])
    if len(target_profiles) != EXPECTED_PROFILE_FILES:
        raise RuntimeError("FULL 后画像路径不唯一")
    if replacement_total != EXPECTED_PROFILE_REPLACEMENTS:
        raise RuntimeError("FULL evidence 画像替换总数漂移")
    current_protected = protected_snapshot(target_profiles)
    if current_protected != evidence.get("protected_after"):
        raise RuntimeError("FULL 后受保护资产摘要漂移")
    scan = validate_revised_scan_scope(rows, target_profiles)
    if scan["detail_marker_rows"]:
        raise RuntimeError(
            "FULL 后授权的详情正文摘录仍有导航标记："
            + "、".join(str(item) for item in scan["detail_marker_rows"][:20])
        )
    if scan["profile_marker_files"]:
        raise RuntimeError(
            "FULL 后授权画像仍有导航标记：\n- "
            + "\n- ".join(scan["profile_marker_files"][:20])
        )
    return {
        "master_rows": len(rows),
        "master_cell_changes": EXPECTED_CELL_CHANGES,
        "profile_files_changed": len(profile_changes),
        "profile_replacements": replacement_total,
        "authorized_scope_marker_hits_after": 0,
        "retained_out_of_scope_marker_cells": len(scan["retained_out_of_scope_cells"]),
    }


def run_full() -> dict[str, Any]:
    ensure_outputs_absent()
    trial_payload = load_trial_evidence(require_current_snapshot=True)
    validate_owner_full_scope(trial_payload)
    manifest = copy.deepcopy(trial_payload["manifest"])
    profile_impact = copy.deepcopy(trial_payload["profile_impact"])
    current_inventory, _ = trial.profile_impact_inventory(copy.deepcopy(manifest))
    expected_inventory = [
        {field: row_value(item.get(field)) for field in trial.PROFILE_FIELDS}
        for item in profile_impact
    ]
    actual_inventory = [
        {field: row_value(item.get(field)) for field in trial.PROFILE_FIELDS}
        for item in current_inventory
    ]
    if actual_inventory != expected_inventory:
        raise RuntimeError("当前画像载体清单已偏离 TRIAL evidence")

    payload, current_rows = load_master_payload_and_layers()
    if len(current_rows) != EXPECTED_MASTER_ROWS:
        raise RuntimeError(f"当前总底表不是 {EXPECTED_MASTER_ROWS} 行")
    before_rows = copy.deepcopy(current_rows)
    updated_payload = copy.deepcopy(payload)
    updated_rows = updated_payload["rows"]
    master_changes = apply_master_changes(updated_rows, manifest)
    cell_diffs = collect_cell_diffs(before_rows, updated_rows)
    if {item["row_number"] for item in cell_diffs} != {
        int(item["row_number"]) for item in manifest
    }:
        raise RuntimeError("逐单元格差异行集与 manifest 不一致")

    target_profiles = {profile_path_from_item(item) for item in profile_impact}
    protected_before = protected_snapshot(target_profiles)
    revised_scan_before = validate_revised_scan_scope(before_rows, target_profiles)

    with tempfile.TemporaryDirectory(prefix="issue87_full_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_payload = temp_root / MASTER_PAYLOAD.name
        temp_csv = temp_root / MASTER_CSV.name
        temp_xlsx = temp_root / MASTER_XLSX.name
        temp_preview = temp_root / "master_preview.png"
        temp_profile_root = temp_root / "profiles"
        temp_evidence = temp_root / EVIDENCE_PATH.name
        temp_reconciliation = temp_root / RECONCILIATION_PATH.name
        temp_summary = temp_root / SUMMARY_PATH.name
        temp_profile_root.mkdir()

        write_json(temp_payload, updated_payload)
        collector.write_csv(temp_csv, updated_rows)
        collector.build_workbook(temp_payload, temp_xlsx, temp_preview)
        with temp_csv.open("r", encoding="utf-8-sig", newline="") as handle:
            temp_csv_rows = list(csv.DictReader(handle))
        temp_xlsx_rows = collector.read_bottom_table_rows(temp_xlsx)
        compare_layers(updated_rows, temp_csv_rows, temp_xlsx_rows)

        profile_changes, profile_file_map = build_profile_outputs(
            temp_profile_root, profile_impact, manifest
        )
        validate_profile_outputs(profile_changes, profile_file_map)
        protected_after_temp = protected_snapshot(target_profiles)
        if protected_after_temp != protected_before:
            changed = [
                key for key in protected_before if protected_before[key] != protected_after_temp.get(key)
            ]
            raise RuntimeError(
                "临时构建阶段受保护资产发生变化：" + "、".join(changed)
            )

        evidence: dict[str, Any] = {
            "meta": {
                "issue_number": ISSUE_NUMBER,
                "phase": PHASE,
                "owner_comment_id": OWNER_COMMENT_ID,
                "generated_utc": utc_now(),
                "master_rows": len(updated_rows),
                "master_cell_changes": len(master_changes),
                "changed_columns": dict(Counter(item["column"] for item in cell_diffs)),
                "profile_files_changed": len(profile_changes),
                "profile_replacements": sum(item["replacements"] for item in profile_changes),
                "authorized_detail_marker_rows_before": len(
                    revised_scan_before["detail_marker_rows"]
                ),
                "authorized_profile_marker_files_before": len(
                    revised_scan_before["profile_marker_files"]
                ),
                "authorized_scope_marker_hits_after": 0,
                "retained_out_of_scope_marker_cells": len(
                    revised_scan_before["retained_out_of_scope_cells"]
                ),
                "retained_out_of_scope_by_column": revised_scan_before[
                    "retained_out_of_scope_by_column"
                ],
            },
            "rules": {
                "start_only": True,
                "adjacent_quote_allowed": False,
                "master_allowed_column": ALLOWED_COLUMN,
                "profile_exact_segment_only": True,
            },
            "master_changes": master_changes,
            "profile_changes": profile_changes,
            "protected_before": protected_before,
            "protected_after": protected_before,
            "artifacts": {
                "evidence": trial.repo_relative(EVIDENCE_PATH),
                "reconciliation": trial.repo_relative(RECONCILIATION_PATH),
                "summary": trial.repo_relative(SUMMARY_PATH),
            },
        }
        write_json(temp_evidence, evidence)
        write_reconciliation(temp_reconciliation, master_changes, profile_changes)
        write_summary(temp_summary, evidence)

        file_map: dict[Path, Path] = {
            MASTER_PAYLOAD: temp_payload,
            MASTER_CSV: temp_csv,
            MASTER_XLSX: temp_xlsx,
            EVIDENCE_PATH: temp_evidence,
            RECONCILIATION_PATH: temp_reconciliation,
            SUMMARY_PATH: temp_summary,
            **profile_file_map,
        }
        backups = backup_targets(file_map, temp_root / "backups")
        try:
            apply_outputs(file_map)
            live_summary = validate_live_full(evidence)
            if live_summary != {
                key: evidence["meta"][key]
                for key in live_summary
            }:
                raise RuntimeError("FULL live summary 与 evidence meta 不一致")
        except Exception:
            restore_targets(backups)
            raise
    return evidence


def validate_outputs() -> dict[str, Any]:
    if not all(path.is_file() for path in (EVIDENCE_PATH, RECONCILIATION_PATH, SUMMARY_PATH)):
        raise RuntimeError("FULL evidence/reconciliation/summary 不完整")
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    meta = evidence.get("meta", {})
    if meta.get("issue_number") != ISSUE_NUMBER or meta.get("phase") != PHASE:
        raise RuntimeError("FULL evidence Issue/Phase 不一致")
    with RECONCILIATION_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        reconciliation = list(reader)
        if tuple(reader.fieldnames or ()) != RECONCILIATION_FIELDS:
            raise RuntimeError("FULL reconciliation schema 漂移")
    if len(reconciliation) != EXPECTED_CELL_CHANGES:
        raise RuntimeError("FULL reconciliation 行数漂移")
    validate_live_full(evidence)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Issue #87 GOVERN-2 导航文本污染清理 FULL")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--apply-full", action="store_true", help="事务式写入 596 单元格与 242 份画像")
    modes.add_argument("--validate-full", action="store_true", help="验证 FULL 正式资产与证据")
    args = parser.parse_args()
    evidence = run_full() if args.apply_full else validate_outputs()
    meta = evidence["meta"]
    print(
        "issue87_full_complete: "
        f"rows={meta['master_cell_changes']} profiles={meta['profile_files_changed']} "
        f"replacements={meta['profile_replacements']} "
        f"authorized_scope_markers={meta['authorized_scope_marker_hits_after']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
