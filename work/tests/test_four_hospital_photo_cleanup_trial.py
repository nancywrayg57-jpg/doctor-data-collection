from __future__ import annotations

import csv
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import four_hospital_photo_cleanup_trial as trial  # noqa: E402


class FourHospitalPhotoCleanupTrialTests(unittest.TestCase):
    def test_scope_is_fixed_249_rows(self) -> None:
        rows = trial.load_scope_rows()
        self.assertEqual(249, len(rows))
        counts: dict[str, int] = {}
        for row in rows:
            counts[row["医院"]] = counts.get(row["医院"], 0) + 1
        self.assertEqual(trial.EXPECTED_SCOPE_BY_HOSPITAL, counts)

    def test_sample_plan_is_5_5_1_1(self) -> None:
        selected = trial.select_trial_rows(trial.load_scope_rows())
        counts: dict[str, int] = {}
        for row in selected:
            counts[row["医院"]] = counts.get(row["医院"], 0) + 1
        self.assertEqual(trial.EXPECTED_SAMPLE_BY_HOSPITAL, counts)
        self.assertEqual(12, len(selected))

    def test_required_gd2h_cases_are_selected(self) -> None:
        selected = trial.select_trial_rows(trial.load_scope_rows())
        names = {row["姓名"] for row in selected if row["医院"] == trial.GD2H}
        self.assertTrue({"陈鹏程", "杨莲娣", "廖耀华"}.issubset(names))

    def test_source_contracts_use_existing_adapters(self) -> None:
        selected = trial.select_trial_rows(trial.load_scope_rows())
        for row in selected:
            self.assertTrue(trial.validate_source_link(row["医院"], row["来源链接"]))

    def test_placeholder_markers(self) -> None:
        self.assertIn("default_ys.gif", trial.placeholder_reason("/static/default_ys.gif"))
        self.assertIn("/images/default/", trial.placeholder_reason("https://wx.e3861.com/sfyAdmin/Images/Default/doct.png"))
        self.assertEqual("known_sha256", trial.placeholder_reason("https://example.test/x.jpg", trial.GDMCH_SHARED_QR_SHA256))
        self.assertEqual("base64_marker", trial.placeholder_reason("data:image/png;base64,placeholder"))

    def test_failure_states_are_closed(self) -> None:
        self.assertEqual(("占位图", "详情照片位命中显式 default/placeholder 门禁"), trial.failure_from_state("placeholder"))
        self.assertEqual("无照片容器", trial.failure_from_state("empty")[0])
        self.assertEqual("照片资源不可达", trial.failure_from_state("available")[0])

    def test_filename_uses_first_department_and_primary_title(self) -> None:
        row = {
            "姓名": "测试医生",
            "医院": trial.GD2H,
            "科室_列表卡片": "关节骨一科（琶洲院区）",
            "科室_分类页": "",
            "职称_关键词": "副主任医师、博士",
            "职称身份原文": "",
        }
        self.assertEqual(
            "测试医生-关节骨一科-副主任医师-广东省第二人民医院",
            trial.filename_stem(row),
        )

    def test_repository_digest_normalizes_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.md"
            path.write_bytes(b"a\r\nb\r\n")
            first = hashlib.sha256(trial.repository_digest_bytes(path)).hexdigest()
            path.write_bytes(b"a\nb\n")
            second = hashlib.sha256(trial.repository_digest_bytes(path)).hexdigest()
        self.assertEqual(first, second)

    def test_manifest_fields_are_stable(self) -> None:
        self.assertEqual("hospital", trial.MANIFEST_FIELDS[0])
        self.assertEqual("observed_utc", trial.MANIFEST_FIELDS[-1])
        self.assertEqual(len(trial.MANIFEST_FIELDS), len(set(trial.MANIFEST_FIELDS)))

    def test_visual_status_does_not_claim_portraits_when_none_downloaded(self) -> None:
        self.assertEqual(
            "PASSED_ZERO_DOWNLOADS_FAILURE_EVIDENCE_CONTACT_SHEET_REVIEW",
            trial.visual_pass_status(0),
        )
        self.assertEqual(
            "PASSED_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS",
            trial.visual_pass_status(1),
        )

    def test_run_trial_assembles_sample_counts_from_sample_schema(self) -> None:
        scope = [
            {"医院": hospital, "姓名": f"样本{index}", "来源链接": f"https://example.test/{index}"}
            for hospital, count in trial.EXPECTED_SCOPE_BY_HOSPITAL.items()
            for index in range(count)
        ]
        selected = [
            row
            for hospital, count in trial.EXPECTED_SAMPLE_BY_HOSPITAL.items()
            for row in [item for item in scope if item["医院"] == hospital][:count]
        ]

        def collect_sample(_session, row, _used_filenames):
            return {
                "hospital": row["医院"],
                "name": row["姓名"],
                "result": "failed",
                "failure_state": "无照片容器",
                "page_image_references": [],
            }

        session = mock.Mock(trace=[])
        snapshot = {"protected": {"sha256": "stable"}}
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            with (
                mock.patch.object(trial, "PAYLOAD_PATH", temporary / "payload.json"),
                mock.patch.object(trial, "MANIFEST_PATH", temporary / "manifest.csv"),
                mock.patch.object(trial, "REPORT_PATH", temporary / "report.md"),
                mock.patch.object(trial, "CONTACT_SHEET_PATH", temporary / "sheet.jpg"),
                mock.patch.object(trial, "TRIAL_PHOTO_DIR", temporary / "photos"),
                mock.patch.object(trial, "ensure_outputs_absent"),
                mock.patch.object(trial, "load_scope_rows", return_value=scope),
                mock.patch.object(trial, "select_trial_rows", return_value=selected),
                mock.patch.object(trial, "protected_snapshot", side_effect=[snapshot, snapshot]),
                mock.patch.object(trial, "RateLimitedSession", return_value=session),
                mock.patch.object(trial, "collect_sample", side_effect=collect_sample),
                mock.patch.object(trial, "collect_shared_qr_evidence", return_value={}),
                mock.patch.object(trial, "build_contact_sheet"),
                mock.patch.object(trial, "validate_payload"),
                mock.patch.object(trial, "write_manifest"),
                mock.patch.object(trial, "write_report"),
                mock.patch.object(trial, "repo_relative", side_effect=lambda path: Path(path).name),
            ):
                payload = trial.run_trial()

        self.assertEqual(
            trial.EXPECTED_SAMPLE_BY_HOSPITAL,
            payload["meta"]["sample_by_hospital"],
        )


if __name__ == "__main__":
    unittest.main()
