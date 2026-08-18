from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import sys2_photo_backfill_trial as target


class Sys2PhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_paths_are_relative_to_checkout(self) -> None:
        self.assertEqual(target.ROOT, Path(__file__).resolve().parents[2])
        self.assertEqual(target.ISSUE_NUMBER, 69)
        self.assertEqual(target.EXPECTED_SCOPE_COUNT, 658)

    def test_detail_id_accepts_only_two_authorized_routes(self) -> None:
        self.assertEqual(target.detail_id("https://www.gzsys.org.cn/node/14894"), "14894")
        self.assertEqual(target.detail_id("https://www.gzsys.org.cn/doctor/14811"), "14811")
        self.assertEqual(target.detail_id("http://www.gzsys.org.cn/node/14894"), "")
        self.assertEqual(target.detail_id("https://example.com/node/14894"), "")
        self.assertEqual(target.detail_id("https://www.gzsys.org.cn/mingyi"), "")

    def test_parser_is_scoped_to_doctor_container(self) -> None:
        html = """
        <title>宋尔卫 | 中山大学孙逸仙纪念医院</title>
        <div data-image-url="/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/naoz.png"></div>
        <div class="other-left">
          <div class="other-media">
            <div class="media-img" data-image-url="/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/doctor/10155.jpg"></div>
          </div>
          <div class="other-left-title">宋尔卫</div>
        </div>
        """
        state, reference = target.extract_portrait_reference(
            html, "https://www.gzsys.org.cn/node/14894", "宋尔卫"
        )
        self.assertEqual(state, "")
        self.assertIsNotNone(reference)
        assert reference is not None
        self.assertEqual(reference.path_kind, "doctor-subdir")
        self.assertEqual(reference.excluded_reference_count, 1)

    def test_accepts_both_original_path_styles(self) -> None:
        source = "https://www.gzsys.org.cn/node/14820"
        doctor_url, doctor_kind = target.page_referenced_photo_url(
            "/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/doctor/10155.jpg", source
        )
        root_url, root_kind = target.page_referenced_photo_url(
            "/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/12822.jpg", source
        )
        self.assertEqual(doctor_kind, "doctor-subdir")
        self.assertEqual(root_kind, "files-root")
        self.assertTrue(doctor_url.startswith("https://www.gzsys.org.cn/"))
        self.assertTrue(root_url.startswith("https://www.gzsys.org.cn/"))

    def test_rejects_default_and_decorative_paths(self) -> None:
        source = "https://www.gzsys.org.cn/node/14820"
        for path in (
            "/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/default_images/doctor-1.png",
            "/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/naoz.png",
            "/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/inline-images/banner.jpg",
        ):
            self.assertEqual(target.page_referenced_photo_url(path, source), ("", ""))

    def test_rejects_title_mismatch(self) -> None:
        html = """
        <div class="other-left"><div class="other-media">
        <div class="media-img" data-image-url="/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/12822.jpg"></div>
        </div><div class="other-left-title">另一人</div></div>
        """
        with self.assertRaisesRegex(RuntimeError, "姓名不一致"):
            target.extract_portrait_reference(
                html, "https://www.gzsys.org.cn/node/14820", "陈样新"
            )

    def test_title_levels_cover_fixed_plan(self) -> None:
        self.assertEqual(target.title_level("教授, 主任医师, 研究员"), "正高")
        self.assertEqual(target.title_level("副研究员"), "副高")
        self.assertEqual(target.title_level("主治医师"), "其他")
        self.assertEqual(
            target.primary_title("副主任医师, 主任医师"), "副主任医师"
        )

    def test_select_trial_rows_enforces_10_departments_and_343(self) -> None:
        rows = []
        for index, (name, level) in enumerate(target.SAMPLE_PLAN):
            title = {"正高": "主任医师", "副高": "副主任医师", "其他": "主治医师"}[level]
            route = "node" if index < 7 else "doctor"
            rows.append(
                {
                    "姓名": name,
                    "科室_分类页": f"科室{index}",
                    "职称身份原文": title,
                    "来源链接": f"https://www.gzsys.org.cn/{route}/{10000 + index}",
                }
            )
        selected = target.select_trial_rows(rows)
        self.assertEqual(len(selected), 10)
        self.assertEqual(len({target.atomic_department(row) for row in selected}), 10)

    def test_magic_extension_requires_image_content_type(self) -> None:
        self.assertEqual(target.magic_extension(b"\xff\xd8\xffrest", "image/jpeg"), "jpg")
        self.assertEqual(target.magic_extension(b"\x89PNG\r\n\x1a\nrest", "image/png"), "png")
        self.assertEqual(target.magic_extension(b"\xff\xd8\xffrest", "text/html"), "")

    def test_validate_rejects_protected_asset_change(self) -> None:
        payload = {
            "meta": {
                "scope_count": 658,
                "trial_count": 10,
                "department_coverage_count": 10,
                "title_level_counts": {"正高": 3, "副高": 4, "其他": 3},
                "path_kind_counts": {"doctor-subdir": 5, "files-root": 5},
                "detail_template_counts": {"node": 5, "doctor": 5},
                "detail_failure_count": 0,
                "no_photo_container_count": 0,
                "placeholder_count": 0,
                "photo_failure_count": 0,
                "status_flicker_count": 0,
                "over_20mib_count": 0,
                "trial_excluded_reference_download_count": 0,
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "pretrial_diagnostic_excluded_request_count": 18,
                "pretrial_diagnostic_persisted_count": 0,
                "protected_assets_before": {"same": True},
                "protected_assets_after": {"same": False},
                "visual_review_status": target.VISUAL_PASS,
            },
            "photo_samples": [],
        }
        with self.assertRaisesRegex(RuntimeError, "正式资产发生变化"):
            target.validate_payload(payload, require_visual_pass=False)

    def test_load_scope_rows_rejects_existing_photo_fields(self) -> None:
        rows = []
        for index in range(658):
            rows.append(
                {
                    "医院": target.HOSPITAL,
                    "姓名": f"医生{index}",
                    "来源链接": f"https://www.gzsys.org.cn/node/{10000 + index}",
                    "照片链接": "https://www.gzsys.org.cn/photo.jpg" if index == 0 else "",
                    "照片文件": "",
                }
            )
        with tempfile.TemporaryDirectory() as temp_dir:
            payload_path = Path(temp_dir) / "master.json"
            payload_path.write_text(json.dumps({"rows": rows}, ensure_ascii=False), encoding="utf-8")
            with patch.object(target, "MASTER_JSON_PATH", payload_path):
                with self.assertRaisesRegex(RuntimeError, "已有照片字段"):
                    target.load_scope_rows()

    def test_validate_requires_visual_pass(self) -> None:
        payload = {"meta": {}, "photo_samples": []}
        with self.assertRaisesRegex(RuntimeError, "视觉通过"):
            target.validate_payload(copy.deepcopy(payload), require_visual_pass=True)


if __name__ == "__main__":
    unittest.main()
