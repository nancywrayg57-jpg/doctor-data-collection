from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import govern_breadcrumb_cleanup_full as full  # noqa: E402


def manifest_item(original: str, segment: str) -> dict[str, object]:
    remaining = original[len(segment) :]
    return {
        "row_number": 2,
        "hospital": full.trial.SYSUCC,
        "source_link": "https://www.sysucc.org.cn/node/test",
        "removed_segment": segment,
        "segment_start": 0,
        "segment_end": len(segment),
        "segment_position": "START",
        "quote_boundary_status": "NO_ADJACENT_QUOTE",
        "original_sha256": full.sha256_text(original),
        "remaining_sha256": full.sha256_text(remaining),
    }


class BreadcrumbCleanupFullTests(unittest.TestCase):
    def test_apply_master_change_updates_only_authorized_cell(self) -> None:
        segment = "临床专家 面包屑 首页 / 临床专家 张三 "
        original = segment + "正文保持原样"
        rows = [{header: "" for header in full.collector.BASE_HEADERS}]
        rows[0].update(
            {
                "序号": 1,
                "医院": full.trial.SYSUCC,
                "姓名": "张三",
                "来源链接": "https://www.sysucc.org.cn/node/test",
                full.ALLOWED_COLUMN: original,
                "复核状态": "待人工复核",
            }
        )
        before = [dict(rows[0])]
        with mock.patch.object(full, "EXPECTED_CELL_CHANGES", 1):
            changes = full.apply_master_changes(rows, [manifest_item(original, segment)])
            diffs = full.collect_cell_diffs(before, rows)
        self.assertEqual("正文保持原样", rows[0][full.ALLOWED_COLUMN])
        self.assertEqual("待人工复核", rows[0]["复核状态"])
        self.assertEqual(1, len(changes))
        self.assertEqual([full.ALLOWED_COLUMN], [item["column"] for item in diffs])

    def test_non_start_match_triggers_fuse(self) -> None:
        segment = "临床专家 面包屑 首页 / 临床专家 张三 "
        original = "前缀" + segment + "正文"
        item = manifest_item(segment + "正文", segment)
        item.update(
            {
                "segment_start": 2,
                "segment_end": 2 + len(segment),
                "segment_position": "MIDDLE",
                "original_sha256": full.sha256_text(original),
            }
        )
        rows = [{header: "" for header in full.collector.BASE_HEADERS}]
        rows[0].update(
            {
                "医院": full.trial.SYSUCC,
                "来源链接": item["source_link"],
                full.ALLOWED_COLUMN: original,
            }
        )
        with mock.patch.object(full, "EXPECTED_CELL_CHANGES", 1):
            with self.assertRaisesRegex(RuntimeError, "非 START"):
                full.apply_master_changes(rows, [item])

    def test_adjacent_quote_policy_triggers_fuse(self) -> None:
        segment = "临床专家 面包屑 首页 / 临床专家 张三 "
        original = segment + "正文"
        item = manifest_item(original, segment)
        item["quote_boundary_status"] = "ISOLATED_QUOTE_PRESERVED_PENDING_OWNER"
        rows = [{header: "" for header in full.collector.BASE_HEADERS}]
        rows[0].update(
            {
                "医院": full.trial.SYSUCC,
                "来源链接": item["source_link"],
                full.ALLOWED_COLUMN: original,
            }
        )
        with mock.patch.object(full, "EXPECTED_CELL_CHANGES", 1):
            with self.assertRaisesRegex(RuntimeError, "孤立撇号"):
                full.apply_master_changes(rows, [item])

    def test_original_sha_drift_is_rejected(self) -> None:
        segment = "临床专家 面包屑 首页 / 临床专家 张三 "
        original = segment + "正文"
        item = manifest_item(original, segment)
        item["original_sha256"] = "0" * 64
        rows = [{header: "" for header in full.collector.BASE_HEADERS}]
        rows[0].update(
            {
                "医院": full.trial.SYSUCC,
                "来源链接": item["source_link"],
                full.ALLOWED_COLUMN: original,
            }
        )
        with mock.patch.object(full, "EXPECTED_CELL_CHANGES", 1):
            with self.assertRaisesRegex(RuntimeError, "original_sha256"):
                full.apply_master_changes(rows, [item])

    def test_cell_diff_rejects_other_columns(self) -> None:
        before = [{header: "" for header in full.collector.BASE_HEADERS}]
        after = [dict(before[0])]
        after[0]["姓名"] = "越界"
        with mock.patch.object(full, "EXPECTED_CELL_CHANGES", 1):
            with self.assertRaisesRegex(RuntimeError, "越界字段"):
                full.collect_cell_diffs(before, after)

    def test_profile_rewrite_preserves_all_non_segment_bytes(self) -> None:
        segment = "导航痕迹 首页 / 王五 "
        source = "https://www.zssy.com.cn/node/test"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile_root = root / "profiles"
            target = profile_root / "中山大学附属第三医院" / "王五.md"
            target.parent.mkdir(parents=True)
            original = ("---\r\n来源链接: \"" + source + "\"\r\n---\r\n" + segment + "正文\r\n").encode("utf-8")
            target.write_bytes(original)
            impact = {
                "hospital": full.trial.ZSSY,
                "profile_path": target.relative_to(root).as_posix(),
                "source_link": source,
                "master_row_number": 2,
                "marker_occurrences": 1,
                "carrier_line_numbers": "4",
                "carrier_sections": "## 详情正文摘录",
            }
            manifest = [{"source_link": source, "removed_segment": segment}]
            temp_profiles = root / "temp"
            temp_profiles.mkdir()
            with (
                mock.patch.object(full, "ROOT", root),
                mock.patch.object(full, "PROFILE_ROOT", profile_root),
                mock.patch.object(full.trial, "ROOT", root),
                mock.patch.object(full, "EXPECTED_PROFILE_FILES", 1),
                mock.patch.object(full, "EXPECTED_PROFILE_REPLACEMENTS", 1),
            ):
                changes, file_map = full.build_profile_outputs(temp_profiles, [impact], manifest)
                full.validate_profile_outputs(changes, file_map)
            expected = original.replace(segment.encode("utf-8"), b"")
            self.assertEqual(expected, next(iter(file_map.values())).read_bytes())
            self.assertIn(b"\r\n", next(iter(file_map.values())).read_bytes())

    def test_marker_scan_reports_only_text_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("正文 面包屑", encoding="utf-8")
            (root / "b.bin").write_bytes("导航痕迹".encode("utf-8"))
            self.assertEqual(["a.md"], full.marker_scan(root))

    def test_current_revised_scan_scope_is_exact(self) -> None:
        _payload, rows = full.load_master_payload_and_layers()
        evidence = json.loads(full.trial.PAYLOAD_PATH.read_text(encoding="utf-8"))
        profiles = {full.profile_path_from_item(item) for item in evidence["profile_impact"]}
        scan = full.validate_revised_scan_scope(rows, profiles)
        observed_scope = (
            len(scan["detail_marker_rows"]),
            len(scan["profile_marker_files"]),
        )
        self.assertIn(observed_scope, {(596, 242), (0, 0)})
        if observed_scope == (0, 0):
            full_evidence = json.loads(full.EVIDENCE_PATH.read_text(encoding="utf-8"))
            self.assertEqual(596, full_evidence["meta"]["master_cell_changes"])
            self.assertEqual(242, full_evidence["meta"]["profile_files_changed"])
            self.assertEqual(0, full_evidence["meta"]["authorized_scope_marker_hits_after"])
        self.assertEqual(53, len(scan["retained_out_of_scope_cells"]))
        self.assertEqual(
            {"亮眼经历线索": 46, "擅长诊疗方向摘录": 7},
            scan["retained_out_of_scope_by_column"],
        )

    def test_owner_scope_rejects_non_start_and_quote(self) -> None:
        payload = {
            "manifest": [
                {"segment_position": "MIDDLE", "quote_boundary_status": "NO_ADJACENT_QUOTE"}
            ],
            "profile_impact": [{"marker_occurrences": 1}],
        }
        with (
            mock.patch.object(full, "EXPECTED_CELL_CHANGES", 1),
            mock.patch.object(full, "EXPECTED_PROFILE_FILES", 1),
            mock.patch.object(full, "EXPECTED_PROFILE_REPLACEMENTS", 1),
        ):
            with self.assertRaisesRegex(RuntimeError, "非 START"):
                full.validate_owner_full_scope(payload)

    def test_reconciliation_schema_and_profile_mapping(self) -> None:
        master = [
            {
                "row_number": 2,
                "sequence": "1",
                "hospital": full.trial.SYSUCC,
                "name": "张三",
                "source_link": "https://www.sysucc.org.cn/node/test",
                "column": full.ALLOWED_COLUMN,
                "removed_length": 8,
                "original_sha256": "a",
                "remaining_sha256": "b",
            }
        ]
        profiles = [
            {
                "source_link": master[0]["source_link"],
                "profile_path": "profiles/张三.md",
                "replacements": 2,
                "before_sha256": "c",
                "after_sha256": "d",
            }
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reconciliation.csv"
            full.write_reconciliation(path, master, profiles)
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)
            self.assertEqual(full.RECONCILIATION_FIELDS, tuple(reader.fieldnames or ()))
            self.assertEqual("2", rows[0]["profile_replacements"])

    def test_repository_digest_normalizes_text_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "a.md"
            crlf = root / "b.md"
            lf.write_bytes(b"same\n")
            crlf.write_bytes(b"same\r\n")
            self.assertEqual(
                full.sha256_bytes(full.trial.repository_digest_bytes(lf)),
                full.sha256_bytes(full.trial.repository_digest_bytes(crlf)),
            )

    def test_protected_snapshot_ignores_transient_lock_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            profile_root = vault / "profiles"
            source = vault / "source"
            target = profile_root / "目标.md"
            target.parent.mkdir(parents=True)
            source.mkdir(parents=True)
            target.write_text("目标", encoding="utf-8")
            (vault / "稳定.md").write_text("稳定", encoding="utf-8")
            (vault / "~$瞬时.xlsx").write_text("锁", encoding="utf-8")
            ledger = source / "ledger.xlsx"
            report = source / "report.md"
            ledger.write_bytes(b"ledger")
            report.write_text("report", encoding="utf-8")
            retired = root / "docs" / "agent_prompts" / "codex_next_prompt.md"
            retired.parent.mkdir(parents=True)
            retired.write_text("retired", encoding="utf-8")
            with (
                mock.patch.object(full, "ROOT", root),
                mock.patch.object(full, "VAULT", vault),
                mock.patch.object(full, "PROFILE_ROOT", profile_root),
                mock.patch.object(full, "SOURCE_DIR", source),
                mock.patch.object(full, "MASTER_CSV", source / "master.csv"),
                mock.patch.object(full, "MASTER_XLSX", source / "master.xlsx"),
                mock.patch.object(full, "LEDGER", ledger),
                mock.patch.object(full, "MASTER_REPORT", report),
            ):
                before = full.protected_snapshot({target})
                (vault / "~$瞬时.xlsx").unlink()
                after = full.protected_snapshot({target})
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
