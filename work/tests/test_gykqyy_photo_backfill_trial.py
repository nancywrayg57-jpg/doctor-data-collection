from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gykqyy_photo_backfill_trial as target


class GykqyyPhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_scope_constants(self) -> None:
        self.assertEqual(target.ROOT, Path(__file__).resolve().parents[2])
        self.assertEqual(target.ISSUE_NUMBER, 75)
        self.assertEqual(target.EXPECTED_SCOPE_COUNT, 297)
        self.assertEqual(target.DIRECTORY_API.split("?", 1)[1], "category=55")

    def test_source_id_accepts_only_fixed_category_55_detail_urls(self) -> None:
        valid = "https://www.gykqyy.com/list.html?category=55&id=195"
        self.assertEqual(target.source_id(valid), "195")
        self.assertEqual(
            target.source_id("https://www.gykqyy.com/list.html?id=195&category=55"),
            "195",
        )
        for invalid in (
            valid.replace("https://", "http://"),
            valid.replace("category=55", "category=56"),
            valid.replace("www.gykqyy.com", "example.com"),
            valid + "&extra=1",
            valid.replace("&id=195", ""),
            valid + "#fragment",
        ):
            self.assertEqual(target.source_id(invalid), "")

    def test_photo_url_accepts_only_api_referenced_upload_paths(self) -> None:
        valid = (
            "https://www.gykqyy.com/uploads/20240710/"
            "668ba01bea0b1840f1a4770078a74e74.jpg"
        )
        self.assertEqual(target.page_referenced_photo_url(valid), valid)
        for invalid in (
            "https://www.gykqyy.com",
            "https://www.gykqyy.com/images/null.jpg",
            "https://www.gykqyy.com/uploads/doctor.jpg",
            valid.replace("www.gykqyy.com", "example.com"),
            valid + "?size=large",
            valid.replace("668ba01bea0b1840f1a4770078a74e74", "not-a-hash"),
        ):
            self.assertEqual(target.page_referenced_photo_url(invalid), "")

    def test_directory_source_evidence_requires_all_page_markers(self) -> None:
        html = """
        if (currentId.value == 55) {
          axios.get("https://www.gykqyy.com/api/article/getZhuanjiaList")
        }
        :src="item3.image || './images/null.jpg'"
        :href="'list.html?category=' + item3.yccms_category_id"
        """
        evidence = target.directory_source_evidence(html)
        self.assertEqual(set(evidence["markers"]), set(target.DIRECTORY_MARKERS))
        with self.assertRaisesRegex(RuntimeError, "image_fallback"):
            target.directory_source_evidence(html.replace("./images/null.jpg", ""))

    @staticmethod
    def directory_payload() -> dict[str, object]:
        doctors = []
        for index, (item_id, name, _level) in enumerate(target.SAMPLE_PLAN):
            doctors.append(
                {
                    "id": item_id,
                    "title": name,
                    "yccms_category_id": 55,
                    "keshi_ids": str(index + 1),
                    "keshi": f"科室{index}",
                    "zhicheng": "主任医师" if index < 5 else "副主任医师",
                    "image": (
                        "https://www.gykqyy.com/uploads/20240710/"
                        f"{item_id:032x}.jpg"
                    ),
                    "weigh": 100 - index,
                }
            )
        return {
            "code": 1,
            "data": {
                "banner": doctors[:2],
                "list": [
                    {
                        "name": "院区",
                        "child": [
                            {"id": 1, "name": "科室", "child": doctors},
                        ],
                    }
                ],
            },
        }

    def test_parse_directory_payload_merges_banner_and_relations(self) -> None:
        result = target.parse_directory_payload(self.directory_payload())
        self.assertEqual(len(result["doctors"]), 10)
        self.assertEqual(len(result["relations"]), 10)
        self.assertEqual(set(result["category_occurrences"]), {"55"})
        self.assertEqual(len(result["category_occurrences"]), 12)

    def test_parse_directory_payload_rejects_business_failure(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "业务失败"):
            target.parse_directory_payload({"code": 0, "msg": "failed", "data": {}})

    def test_decode_json_response_reports_http_and_content_type(self) -> None:
        response = target.HttpResult(
            status=200,
            content_type="text/html",
            charset="utf-8",
            content=b"<html></html>",
            final_url=target.DIRECTORY_API,
            redirects=(),
        )
        with self.assertRaisesRegex(RuntimeError, "HTTP 200.*非 JSON"):
            target.decode_json_response(response, "test")

    def test_select_trial_rows_enforces_plan_levels_and_department_atoms(self) -> None:
        rows = []
        records = []
        for index, (item_id, name, level) in enumerate(target.SAMPLE_PLAN):
            title = "主任医师" if level == "正高" else "副主任医师"
            source = f"https://www.gykqyy.com/list.html?category=55&id={item_id}"
            rows.append(
                {
                    "姓名": name,
                    "科室_分类页": f"科室{index}、共享科室",
                    "职称身份原文": title,
                    "来源链接": source,
                }
            )
            records.append(
                {
                    "id": str(item_id),
                    "valid_photo_url": (
                        "https://www.gykqyy.com/uploads/20240710/"
                        f"{item_id:032x}.jpg"
                    ),
                    "api_keshi_ids": str(index + 1),
                }
            )
        selected = target.select_trial_rows(rows, records)
        self.assertEqual(len(selected), 10)
        self.assertEqual(len({target.atomic_department(row) for row in selected}), 10)

    def test_load_scope_rows_rejects_existing_photo_fields(self) -> None:
        rows = []
        for index in range(297):
            rows.append(
                {
                    "医院": target.HOSPITAL,
                    "姓名": f"医生{index}",
                    "来源链接": (
                        "https://www.gykqyy.com/list.html?category=55&"
                        f"id={index + 1}"
                    ),
                    "照片链接": "https://www.gykqyy.com/photo.jpg" if index == 0 else "",
                    "照片文件": "",
                }
            )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "master.json"
            path.write_text(json.dumps({"rows": rows}, ensure_ascii=False), encoding="utf-8")
            with patch.object(target, "MASTER_JSON_PATH", path):
                with self.assertRaisesRegex(RuntimeError, "已有照片字段"):
                    target.load_scope_rows()

    def test_write_manifest_serializes_attempt_evidence(self) -> None:
        sample = {key: "" for key in target.MANIFEST_FIELDS}
        sample.update(
            {
                "id": "195",
                "name": "李江",
                "bytes": 123,
                "photo_attempts": [{"attempt": 1, "status": 200}],
            }
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "manifest.csv"
            with patch.object(target, "TRIAL_CSV_PATH", path):
                target.write_manifest([sample])
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle))
        self.assertEqual(json.loads(row["photo_attempts"]), sample["photo_attempts"])

    def test_validate_requires_visual_pass(self) -> None:
        payload = {"meta": {}, "scope_records": [], "photo_samples": []}
        with self.assertRaisesRegex(RuntimeError, "视觉通过"):
            target.validate_payload(
                payload, require_visual_pass=True, check_artifacts=False
            )


if __name__ == "__main__":
    unittest.main()
