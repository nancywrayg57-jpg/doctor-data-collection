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

import fahsysu_photo_backfill_trial as target


class FahsysuPhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_scope_constants(self) -> None:
        self.assertEqual(target.ROOT, Path(__file__).resolve().parents[2])
        self.assertEqual(target.ISSUE_NUMBER, 71)
        self.assertEqual(target.EXPECTED_SCOPE_COUNT, 860)
        self.assertEqual(target.EXPECTED_RECONCILIATION_COUNT, 12)

    def test_detail_id_accepts_only_authorized_node_route(self) -> None:
        self.assertEqual(target.detail_id("https://www.fahsysu.org.cn/node/620"), "620")
        self.assertEqual(target.detail_id("http://www.fahsysu.org.cn/node/620"), "")
        self.assertEqual(target.detail_id("https://example.com/node/620"), "")
        self.assertEqual(target.detail_id("https://www.fahsysu.org.cn/doctor/620"), "")
        self.assertEqual(target.detail_id("https://www.fahsysu.org.cn/node/620?x=1"), "")

    def test_accepts_only_page_referenced_focal_style_with_one_itok(self) -> None:
        source = "https://www.fahsysu.org.cn/node/620"
        valid = (
            "https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/"
            "styles/focal_point_480/public/2023-07/%E9%83%AD%E5%AE%87.jpg?itok=abc123"
        )
        self.assertEqual(
            target.page_referenced_photo_url(valid, source),
            (valid, "focal_point_480", "abc123"),
        )
        for invalid in (
            valid.split("?", 1)[0],
            valid + "&other=1",
            valid.replace("focal_point_480", "mini200"),
            "https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/"
            "2023-07/%E9%83%AD%E5%AE%87.jpg?itok=abc123",
        ):
            self.assertEqual(target.page_referenced_photo_url(invalid, source), ("", "", ""))

    def test_parser_selects_focal_and_records_excluded_public_icons(self) -> None:
        source = "https://www.fahsysu.org.cn/node/620"
        focal = (
            "/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/focal_point_480/"
            "public/2023-07/doctor.jpg?itok=unique"
        )
        html = f"""
        <title>郭宇 | 中山大学附属第一医院</title>
        <div class="other-left"><div class="other-media">
          <div class="media-img" data-image-url="{focal}"></div>
          <div class="media-img" data-image-url="/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-1.png?itok=a"></div>
          <div class="media-img" data-image-url="/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-2.png?itok=b"></div>
        </div><div class="other-left-title">郭宇</div></div>
        """
        analysis = target.analyze_doctor_media(html, source, "郭宇")
        self.assertEqual(analysis.state, "")
        self.assertEqual(analysis.path_kind, "focal_point_480")
        self.assertEqual(analysis.itok, "unique")
        self.assertEqual(analysis.focal_point_480_reference_count, 1)
        self.assertEqual(analysis.media_candidate_count, 3)
        self.assertEqual(len(analysis.excluded_resources), 2)

    def test_parser_records_five_mini_icons_as_no_photo_evidence(self) -> None:
        source = "https://www.fahsysu.org.cn/node/5780"
        icons = "".join(
            f'<div class="media-img" data-image-url="/sites/1h.prod.sysucloud1.sysu.edu.cn/'
            f'files/styles/mini200/public/action-{index}.png?itok=t{index}"></div>'
            for index in range(5)
        )
        html = f"""
        <title>黄雄庆 | 中山大学附属第一医院</title>
        <div class="other-left"><div class="other-media"></div>
        <div class="other-left-title">黄雄庆</div></div>
        <div class="action-media">{icons}</div>
        """
        analysis = target.analyze_doctor_media(html, source, "黄雄庆")
        self.assertEqual(analysis.state, "无照片容器")
        self.assertEqual(analysis.focal_point_480_reference_count, 0)
        self.assertEqual(analysis.media_candidate_count, 5)
        self.assertEqual(len(analysis.excluded_resources), 5)
        self.assertIn("/styles/mini200/", analysis.detection_feature)

    def test_parser_rejects_name_mismatch(self) -> None:
        html = """
        <div class="other-left"><div class="other-media"></div>
        <div class="other-left-title">另一人</div></div>
        """
        with self.assertRaisesRegex(RuntimeError, "姓名不一致"):
            target.analyze_doctor_media(
                html, "https://www.fahsysu.org.cn/node/620", "郭宇"
            )

    def test_select_trial_rows_enforces_owner_ruling(self) -> None:
        rows: list[dict[str, str]] = []
        for index, (name, level) in enumerate(target.SUCCESS_SAMPLE_PLAN):
            rows.append(
                {
                    "姓名": name,
                    "科室_分类页": f"科室{index}",
                    "职称身份原文": "主任医师" if level == "正高" else "副主任医师",
                    "来源链接": f"https://www.fahsysu.org.cn/node/{1000 + index}",
                }
            )
        for name, url in target.FAILURE_EVIDENCE_PLAN:
            rows.append(
                {
                    "姓名": name,
                    "科室_分类页": "麻醉科",
                    "职称身份原文": "",
                    "来源链接": url,
                }
            )
        success, failures = target.select_trial_rows(rows)
        self.assertEqual(len(success), 10)
        self.assertEqual(len(failures), 2)
        self.assertEqual(
            {target.title_level(row["职称身份原文"]) for row in success},
            {"正高", "副高"},
        )

    def test_failure_evidence_requires_urls_and_detection_feature(self) -> None:
        records = []
        for name, source in target.FAILURE_EVIDENCE_PLAN:
            records.append(
                {
                    "name": name,
                    "source_link": source,
                    "failure_state": "无照片容器",
                    "detail_status": 200,
                    "detail_probe_utc": "2026-08-18T12:15:02Z",
                    "focal_point_480_reference_count": 0,
                    "media_candidate_count": 5,
                    "excluded_resources": [
                        {
                            "url": "https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/"
                            f"files/styles/mini200/public/action-{index}.png?itok=t{index}"
                        }
                        for index in range(5)
                    ],
                    "detection_feature": (
                        "focal_point_480 引用数=0；media-img 候选均为 "
                        "path contains /styles/mini200/"
                    ),
                    "photo_url": "",
                    "filename": "",
                    "bytes": 0,
                    "sha256": "",
                }
            )
        self.assertEqual(target.validate_failure_evidence(records), [])
        records[0]["excluded_resources"] = []
        self.assertTrue(target.validate_failure_evidence(records))

    def test_write_manifest_preserves_twelve_row_reconciliation(self) -> None:
        records = []
        for index in range(12):
            records.append(
                {
                    "record_type": "success" if index < 10 else "failure_evidence",
                    "name": f"医生{index}",
                    "outcome": "success" if index < 10 else "failure_evidence",
                    "detail_attempts": [{"status": 200}],
                    "excluded_resource_urls": ["https://www.fahsysu.org.cn/icon.png"],
                }
            )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "manifest.csv"
            with patch.object(target, "TRIAL_CSV_PATH", path):
                target.write_manifest(records)
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 12)
        self.assertEqual(json.loads(rows[-1]["detail_attempts"]), [{"status": 200}])

    def test_load_scope_rows_rejects_existing_photo_fields(self) -> None:
        rows = []
        for index in range(860):
            rows.append(
                {
                    "医院": target.HOSPITAL,
                    "姓名": f"医生{index}",
                    "来源链接": f"https://www.fahsysu.org.cn/node/{10000 + index}",
                    "照片链接": "https://www.fahsysu.org.cn/photo.jpg" if index == 0 else "",
                    "照片文件": "",
                }
            )
        with tempfile.TemporaryDirectory() as temp_dir:
            payload_path = Path(temp_dir) / "master.json"
            payload_path.write_text(
                json.dumps({"rows": rows}, ensure_ascii=False), encoding="utf-8"
            )
            with patch.object(target, "MASTER_JSON_PATH", payload_path):
                with self.assertRaisesRegex(RuntimeError, "已有照片字段"):
                    target.load_scope_rows()

    def test_validate_requires_visual_pass(self) -> None:
        payload = {"meta": {}, "photo_samples": [], "failure_evidence": [], "trial_records": []}
        with self.assertRaisesRegex(RuntimeError, "视觉通过"):
            target.validate_payload(payload, require_visual_pass=True)


if __name__ == "__main__":
    unittest.main()
