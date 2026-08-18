from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gykqyy_photo_backfill_full as target


class GykqyyPhotoBackfillFullTests(unittest.TestCase):
    def test_scope_constants_match_owner_full_instruction(self) -> None:
        self.assertEqual(target.ISSUE_NUMBER, 75)
        self.assertEqual(target.EXPECTED_SCOPE_COUNT, 297)
        self.assertEqual(target.EXPECTED_SUCCESS_COUNT, 58)
        self.assertEqual(target.EXPECTED_EMPTY_IMAGE_COUNT, 231)
        self.assertEqual(target.EXPECTED_NON_UPLOAD_COUNT, 8)
        self.assertEqual(target.EXPECTED_FAILURE_COUNT, 239)

    def test_append_warning_is_idempotent_and_preserves_existing(self) -> None:
        result = target.append_warning("同名待甄别", target.NO_PHOTO_WARNING)
        self.assertEqual(result, f"同名待甄别；{target.NO_PHOTO_WARNING}")
        self.assertEqual(
            target.append_warning(result, target.NO_PHOTO_WARNING), result
        )

    def test_allocate_full_photo_path_adds_id_for_collision(self) -> None:
        row = {
            "姓名": "方颖",
            "科室_分类页": "荔湾院区口腔种植科",
            "职称身份原文": "副教授",
            "来源链接": "https://www.gykqyy.com/list.html?category=55&id=128",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            used: set[str] = set()
            first, _path = target.allocate_full_photo_path(row, "jpg", root, used)
            second, _path = target.allocate_full_photo_path(row, "jpg", root, used)
        self.assertTrue(first.endswith(".jpg"))
        self.assertTrue(second.endswith("-128.jpg"))

    def test_reconcile_scope_records_missing_api_id_as_detail_unreachable(self) -> None:
        rows = [
            {
                "姓名": "医生",
                "科室_分类页": "科室",
                "职称身份原文": "主任医师",
                "来源链接": "https://www.gykqyy.com/list.html?category=55&id=1",
            }
        ]
        records, extra = target.reconcile_scope_with_missing(rows, [], "2026-08-19T00:00:00Z")
        self.assertEqual(extra, [])
        self.assertEqual(records[0]["image_signal"], "DETAIL_UNREACHABLE_API_ID_MISSING")

    def test_reconcile_scope_ignores_but_reports_extra_api_ids(self) -> None:
        rows = [
            {
                "姓名": "医生一",
                "科室_分类页": "科室一",
                "职称身份原文": "主任医师",
                "来源链接": "https://www.gykqyy.com/list.html?category=55&id=1",
            }
        ]
        doctors = [
            {
                "id": "1",
                "title": "医生一",
                "yccms_category_id": 55,
                "keshi_ids": "1",
                "keshi": "科室一",
                "zhicheng": "主任医师",
                "image": "",
            },
            {"id": "2", "title": "范围外"},
        ]
        records, extra = target.reconcile_scope_with_missing(rows, doctors, "utc")
        self.assertEqual(len(records), 1)
        self.assertEqual(extra, ["2"])

    def test_profile_insert_is_exact_plus_two_lines(self) -> None:
        before = (
            f"{target.AUTO_MARKER}\n# 医生\n\n## 基础信息\n\n- 姓名：医生\n"
        ).encode("utf-8")
        photo_file = "01_试点医院/广州医科大学附属口腔医院/照片/医生.jpg"
        after = target.insert_profile_photo_block_bytes(before, "医生", photo_file)
        target.validate_profile_photo_only_bytes(before, after, "医生", photo_file)
        self.assertIn("![医生](照片/医生.jpg)", after.decode("utf-8"))

    def test_profile_insert_rejects_existing_photo_block(self) -> None:
        before = "## 基础信息\n\n![医生](照片/医生.jpg)\n\n"
        with self.assertRaisesRegex(RuntimeError, "已存在照片"):
            target.insert_profile_photo_block(before, "医生", "照片/医生.jpg")

    def test_collect_row_diffs_rejects_non_photo_columns(self) -> None:
        source = "https://www.gykqyy.com/list.html?category=55&id=1"
        before = [{"姓名": "医生", "来源链接": source, "照片链接": ""}]
        after = [{"姓名": "另一人", "来源链接": source, "照片链接": ""}]
        with self.assertRaisesRegex(RuntimeError, "范围外字段"):
            target.collect_full_row_diffs(
                before, after, {source}, ["姓名", "来源链接", "照片链接"]
            )

    def test_failure_evidence_includes_raw_image_and_utc(self) -> None:
        text = target.failure_evidence_text(
            {
                "observed_utc": "2026-08-19T00:00:00Z",
                "api_category": "55",
                "api_image_field_value": "https://www.gykqyy.com",
                "image_signal": "NO_PHOTO_CONTAINER_NON_UPLOAD_IMAGE_FIELD",
                "detection_feature": "not uploads",
            }
        )
        self.assertIn("2026-08-19T00:00:00Z", text)
        self.assertIn("https://www.gykqyy.com", text)
        self.assertIn("not uploads", text)

    def test_placeholder_gate_is_conservative(self) -> None:
        self.assertIn(
            "占位",
            target.placeholder_response_reason(
                "https://www.gykqyy.com/uploads/20240710/default.jpg",
                b"x" * 100,
                10,
                10,
            ),
        )
        self.assertEqual(
            target.placeholder_response_reason(
                "https://www.gykqyy.com/uploads/20240710/"
                "668ba01bea0b1840f1a4770078a74e74.jpg",
                b"x" * 20000,
                315,
                422,
            ),
            "",
        )

    def test_validate_full_payload_rejects_wrong_four_number_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            audit = root / "audit.jpg"
            payload = {"meta": {"expected_count": 297, "downloaded_count": 57}}
            with self.assertRaisesRegex(RuntimeError, "四数对账"):
                target.validate_full_payload(payload, root, audit)

    def test_write_reconciliation_preserves_classification_status(self) -> None:
        payload = {
            "reconciliation": [
                {
                    "ID": "1",
                    "姓名": "医生",
                    "来源链接": "source",
                    "状态": "失败留空",
                    "失败分类": "无照片容器",
                    "分类状态": "OWNER_FINAL_CLASSIFICATION_REQUIRED",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "reconciliation.csv"
            target.write_reconciliation_csv(path, payload)
            content = path.read_text(encoding="utf-8-sig")
        self.assertIn("OWNER_FINAL_CLASSIFICATION_REQUIRED", content)


if __name__ == "__main__":
    unittest.main()
