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

import gdzy5413_photo_backfill_trial as target


class Gdzy5413PhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_scope_constants(self) -> None:
        self.assertEqual(target.ROOT, Path(__file__).resolve().parents[2])
        self.assertEqual(target.ISSUE_NUMBER, 73)
        self.assertEqual(target.EXPECTED_SCOPE_COUNT, 342)
        self.assertEqual(target.EXPECTED_KSDOCTOR_COUNT, 321)
        self.assertEqual(target.EXPECTED_SPECIALIST_COUNT, 21)

    def test_detail_template_accepts_only_fixed_authorized_routes(self) -> None:
        specialist = "https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=699"
        ksdoctor = (
            "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?"
            "bid=47&typeid=45&cid=47&ksid=45&id=417"
        )
        self.assertEqual(target.detail_template(specialist), "specialist")
        self.assertEqual(target.detail_template(ksdoctor), "ksdoctorinfo")
        self.assertEqual(target.detail_id(specialist), "specialist-699")
        self.assertEqual(target.detail_id(ksdoctor), "ksdoctorinfo-417")
        for invalid in (
            specialist.replace("https://", "http://"),
            specialist + "&extra=1",
            specialist.replace("www.gdzy5413.com", "example.com"),
            ksdoctor.replace("&id=417", ""),
            ksdoctor + "&id=999",
        ):
            self.assertEqual(target.detail_template(invalid), "")

    def test_specialist_parser_selects_only_inline_portrait_background(self) -> None:
        source = "https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=699"
        html = """
        <div class="main_left_img">
          <div style="position:relative"><div class="docimg_title">靳利利</div>
          <div class="docimg_ming"></div><div class="docimg_cover"></div>
          <div style="overflow:hidden;width:340px;background:url(/UploadFiles/image/2014-2/doctor.jpg) no-repeat center;height:369px"></div></div>
        </div><div class="keylist_bg">
          <img alt="就诊指南" src="/UploadFiles/image/2013-12/20131226040613496.jpg">
          <img src="style/images/logo.png">
        </div>
        """
        result = target.analyze_page(html, source, "靳利利")
        self.assertEqual(result["template"], "specialist")
        self.assertEqual(
            result["photo_url"],
            "https://www.gdzy5413.com/UploadFiles/image/2014-2/doctor.jpg",
        )
        self.assertEqual(result["candidate_count"], 1)
        self.assertEqual(len(result["excluded_resources"]), 2)
        self.assertIn("main_left_img", result["container_selector"])

    def test_ksdoctor_parser_selects_only_120_by_155_profile_image(self) -> None:
        source = (
            "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?"
            "bid=47&typeid=45&cid=47&ksid=45&id=417"
        )
        html = """
        <img src="style/images/logo.png">
        <div style="float:left;width:120px">
          <img border="5px" src="/UploadFiles/image/2014-2/doctor_s.jpg" width="120px" height="155px">
        </div>
        <div>姓名：林谋清<br>职称：主治中医师</div>
        <img src="/UploadFiles/image/2013-12/20131202104531799.png">
        """
        result = target.analyze_page(html, source, "林谋清")
        self.assertEqual(result["template"], "ksdoctorinfo")
        self.assertEqual(
            result["photo_url"],
            "https://www.gdzy5413.com/UploadFiles/image/2014-2/doctor_s.jpg",
        )
        self.assertIn("120px", result["container_selector"])
        self.assertIn("/UploadFiles/image/", result["html_snippet"])

    def test_ksdoctor_parser_rejects_empty_upload_path(self) -> None:
        source = (
            "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?"
            "bid=65&typeid=63&cid=65&ksid=63&id=370"
        )
        html = """
        <div><img src="/UploadFiles/image/" width="120px" height="155px"></div>
        <div>姓名：付亚斐<br>职称：中医师</div>
        """
        with self.assertRaisesRegex(RuntimeError, "无本人照片文件引用"):
            target.analyze_page(html, source, "付亚斐")

    def test_parser_rejects_name_mismatch(self) -> None:
        source = "https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=699"
        html = """
        <div class="main_left_img"><div class="docimg_title">另一人</div>
        <div style="background:url(/UploadFiles/image/doctor.jpg)"></div></div>
        <div class="keylist_bg"></div>
        """
        with self.assertRaisesRegex(RuntimeError, "姓名不一致"):
            target.analyze_page(html, source, "靳利利")

    def test_page_referenced_photo_url_rejects_placeholders_and_other_hosts(self) -> None:
        source = "https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=699"
        valid = "https://www.gdzy5413.com/UploadFiles/image/2014-2/doctor.jpg"
        self.assertEqual(target.page_referenced_photo_url(valid, source), valid)
        for invalid in (
            "https://example.com/UploadFiles/image/doctor.jpg",
            "https://www.gdzy5413.com/style/images/logo.jpg",
            "https://www.gdzy5413.com/UploadFiles/image/",
            "https://www.gdzy5413.com/UploadFiles/image/default_doctor.jpg",
        ):
            self.assertEqual(target.page_referenced_photo_url(invalid, source), "")

    def test_response_content_gate_rejects_disguised_small_placeholder(self) -> None:
        known_digest_bytes = b"not-the-known-image"
        with patch.object(
            target,
            "KNOWN_PLACEHOLDER_SHA256",
            {target.hashlib.sha256(known_digest_bytes).hexdigest()},
        ):
            self.assertIn(
                "known-placeholder-sha256",
                target.placeholder_response_reason(known_digest_bytes, 86, 126),
            )
        self.assertIn(
            "small-placeholder-like-response",
            target.placeholder_response_reason(b"x" * 1622, 86, 126),
        )
        self.assertEqual(target.placeholder_response_reason(b"x" * 11401, 68, 100), "")

    def test_format_metadata_uses_magic_filename_not_mislabeled_header(self) -> None:
        formats, mismatch_count = target.sample_format_metadata(
            [
                {"filename": "doctor.png", "photo_content_type": "image/jpeg"},
                {"filename": "doctor2.jpg", "photo_content_type": "image/jpeg"},
                {"filename": "doctor3.png", "photo_content_type": "image/png"},
            ]
        )
        self.assertEqual(formats, {"png": 2, "jpg": 1})
        self.assertEqual(mismatch_count, 1)

    def test_select_trial_rows_enforces_two_templates_ten_departments_and_levels(self) -> None:
        rows: list[dict[str, str]] = []
        for index, (name, template, level) in enumerate(target.SAMPLE_PLAN):
            if template == "specialist":
                link = f"https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid={100 + index}"
            else:
                link = (
                    "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?"
                    f"bid={index + 1}&typeid={index + 2}&cid={index + 1}&ksid={index + 2}&id={200 + index}"
                )
            title = "主任医师" if level == "正高" else "副主任医师" if level == "副高" else "主治医师"
            rows.append(
                {
                    "姓名": name,
                    "科室_分类页": f"科室{index}",
                    "职称_关键词": title,
                    "来源链接": link,
                }
            )
        selected = target.select_trial_rows(rows)
        self.assertEqual(len(selected), 10)
        self.assertEqual(
            {target.atomic_department(row) for row in selected},
            {f"科室{index}" for index in range(10)},
        )

    def test_load_scope_rows_rejects_existing_photo_fields(self) -> None:
        rows = []
        for index in range(342):
            if index < 321:
                source = (
                    "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?"
                    f"bid={index + 1}&typeid={index + 2}&cid={index + 1}&ksid={index + 2}&id={index + 1}"
                )
            else:
                source = (
                    "https://www.gdzy5413.com/main/doctor/specialist.aspx?"
                    f"typeid={index + 1}"
                )
            rows.append(
                {
                    "医院": target.HOSPITAL,
                    "姓名": f"医生{index}",
                    "来源链接": source,
                    "照片链接": "https://www.gdzy5413.com/photo.jpg" if index == 0 else "",
                    "照片文件": "",
                }
            )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            payload_path = root / "master.json"
            profile_dir = root / "profiles"
            profile_dir.mkdir()
            payload_path.write_text(
                json.dumps({"rows": rows}, ensure_ascii=False), encoding="utf-8"
            )
            for index in range(342):
                (profile_dir / f"医生{index}.md").write_text(
                    "<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->",
                    encoding="utf-8",
                )
            (profile_dir / "_索引.md").write_text("index", encoding="utf-8")
            with (
                patch.object(target, "MASTER_JSON_PATH", payload_path),
                patch.object(target, "PROFILE_DIR", profile_dir),
                patch.object(target, "FORMAL_PHOTO_DIR", root / "photos"),
            ):
                with self.assertRaisesRegex(RuntimeError, "已有照片字段"):
                    target.load_scope_rows()

    def test_write_manifest_serializes_evidence_columns(self) -> None:
        sample = {
            "name": "医生",
            "source_link": "https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=1",
            "sha256": "abc",
            "detail_attempts": [{"status": 200}],
            "photo_attempts": [{"status": 200}],
            "excluded_resources": [{"url": "https://www.gdzy5413.com/style/images/logo.png"}],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "manifest.csv"
            with patch.object(target, "TRIAL_CSV_PATH", path):
                target.write_manifest([sample])
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(json.loads(rows[0]["detail_attempts"]), [{"status": 200}])
        self.assertEqual(json.loads(rows[0]["photo_attempts"]), [{"status": 200}])
        self.assertEqual(len(json.loads(rows[0]["excluded_resources"])), 1)

    def test_validate_requires_visual_pass(self) -> None:
        payload = {"meta": {}, "samples": [], "structure_diagnostics": []}
        with self.assertRaisesRegex(RuntimeError, "视觉通过"):
            target.validate_payload(payload, require_visual_pass=True)


if __name__ == "__main__":
    unittest.main()
