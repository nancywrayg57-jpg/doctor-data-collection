from __future__ import annotations

import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gyfyyy_photo_backfill_trial as trial  # noqa: E402


class GyfyyyPhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_paths_are_relative_to_checkout(self) -> None:
        self.assertEqual(trial.ROOT, Path(__file__).resolve().parents[2])
        self.assertEqual(trial.ISSUE_NUMBER, 63)
        self.assertEqual(trial.EXPECTED_SCOPE_COUNT, 616)

    def test_detail_url_and_two_page_referenced_styles(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html"
        self.assertEqual(trial.detail_id(source), "1")
        self.assertEqual(
            trial.page_referenced_photo_url(
                "/Upload/202112/637750146771733237.jpg", source
            ),
            (
                "https://www.gyfyyy.cn/Upload/202112/637750146771733237.jpg",
                "Upload原图",
            ),
        )
        self.assertEqual(
            trial.page_referenced_photo_url("/images/doctor/LAIKEFANG.jpg", source),
            (
                "https://www.gyfyyy.cn/images/doctor/LAIKEFANG.jpg",
                "doctor原图",
            ),
        )

    def test_rejects_query_third_party_and_unapproved_paths(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html"
        for value in (
            "/Upload/202112/637750146771733237.jpg?v=1",
            "https://example.com/Upload/202112/637750146771733237.jpg",
            "/Upload/202106/zhongnanshan-lab.png",
            "/images/news/zhongnanshan.jpg",
        ):
            self.assertEqual(trial.page_referenced_photo_url(value, source), ("", ""))
        self.assertEqual(
            trial.detail_id("https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html?x=1"),
            "",
        )

    def test_parser_uses_only_unique_photo_container(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html"
        html = """
        <html><head><title>钟南山_呼吸与危重症医学科_广州医科大学附属第一医院官方网站www.gyfyy.com</title></head>
        <body>
          <img src="/Upload/202106/zhongnanshan-lab.png">
          <div class="photo"><img src="/Upload/202112/637750146771733237.jpg"></div>
          <div class="floatcard"><img src="/Upload/202112/637750146771733237.jpg"></div>
        </body></html>
        """
        state, portrait = trial.inspect_portrait_reference(html, source, "钟南山")
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)
        assert portrait is not None
        self.assertEqual(portrait.reference_kind, "Upload原图")
        self.assertEqual(
            portrait.photo_url,
            "https://www.gyfyyy.cn/Upload/202112/637750146771733237.jpg",
        )
        self.assertEqual(portrait.template_signature, "div.photo img")

    def test_parser_accepts_doctor_style_and_rejects_ambiguous_container(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_9.html"
        html = """
        <title>赖克方_呼吸与危重症医学科_广州医科大学附属第一医院官方网站www.gyfyy.com</title>
        <div class="doctor-card photo"><img src="/images/doctor/LAIKEFANG.jpg"></div>
        """
        state, portrait = trial.inspect_portrait_reference(html, source, "赖克方")
        self.assertEqual(state, "")
        assert portrait is not None
        self.assertEqual(portrait.reference_kind, "doctor原图")
        with self.assertRaisesRegex(RuntimeError, "div.photo 容器不唯一"):
            trial.inspect_portrait_reference(
                html + '<div class="photo"><img src="/images/doctor/OTHER.jpg"></div>',
                source,
                "赖克方",
            )

    def test_scope_and_fixed_sample_plan_are_stable(self) -> None:
        rows = trial.load_scope_rows()
        selected = trial.select_trial_rows(rows)
        self.assertEqual(len(rows), 616)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(
            len({trial.atomic_department(row) for row in selected}), 8
        )
        levels = [trial.title_level(row.get("职称身份原文")) for row in selected]
        self.assertEqual(levels.count("正高"), 3)
        self.assertEqual(levels.count("副高"), 3)
        self.assertEqual(levels.count("其他"), 4)

    def test_small_gray_or_marked_gif_is_placeholder(self) -> None:
        gray = Image.new("RGB", (40, 40), (235, 235, 235))
        buffer = io.BytesIO()
        gray.save(buffer, format="GIF")
        content = buffer.getvalue()
        self.assertLess(len(content), trial.SMALL_GIF_PLACEHOLDER_BYTES)
        self.assertIn(
            "占位图",
            trial.downloaded_placeholder_reason(
                "https://www.gyfyyy.cn/images/doctor/avatar.gif", content, "gif"
            ),
        )

    def test_colorful_small_gif_and_large_gif_are_not_format_placeholders(self) -> None:
        colorful = Image.new("RGB", (30, 30), (0, 80, 220))
        buffer = io.BytesIO()
        colorful.save(buffer, format="GIF")
        content = buffer.getvalue()
        self.assertEqual(
            trial.downloaded_placeholder_reason(
                "https://www.gyfyyy.cn/images/doctor/doctor.gif", content, "gif"
            ),
            "",
        )
        large_gif = b"GIF89a" + b"x" * trial.SMALL_GIF_PLACEHOLDER_BYTES
        self.assertEqual(
            trial.downloaded_placeholder_reason(
                "https://www.gyfyyy.cn/images/doctor/portrait.gif", large_gif, "gif"
            ),
            "",
        )

    def test_magic_dimensions_and_filename_policy(self) -> None:
        image = Image.new("RGB", (17, 23), (20, 40, 60))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        content = buffer.getvalue()
        self.assertEqual(trial.magic_extension(content, "image/png"), "png")
        self.assertEqual(trial.image_dimensions(content), (17, 23))
        row = {
            "姓名": "测试医生",
            "科室_分类页": "测试科",
            "职称身份原文": "副主任医师",
            "来源链接": "https://www.gyfyyy.cn/cn/ks/nk/test/doctor_999.html",
        }
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(trial, "TRIAL_PHOTO_DIR", Path(directory)):
                filename, path = trial.allocate_trial_photo(row, "png", content)
                self.assertEqual(
                    filename,
                    "测试医生-测试科-副主任医师-广州医科大学附属第一医院.png",
                )
                self.assertEqual(path.parent, Path(directory))

    def test_size_buckets_cover_owner_reporting_and_fuse_boundary(self) -> None:
        self.assertEqual(trial.size_bucket(100), "<200KiB")
        self.assertEqual(trial.size_bucket(300 * 1024), "200KiB-1MiB")
        self.assertEqual(trial.size_bucket(2 * 1024 * 1024), "1-5MiB")
        self.assertEqual(trial.size_bucket(6 * 1024 * 1024), "5-20MiB")
        self.assertEqual(trial.size_bucket(21 * 1024 * 1024), ">20MiB")

    def test_abnormal_format_and_over_20mib_are_immediate_fuses(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "格式不受支持"):
            trial.enforce_photo_policy(
                "测试医生", "https://www.gyfyyy.cn/images/doctor/TEST.bmp", "", 100
            )
        with self.assertRaisesRegex(RuntimeError, "超过 20 MiB"):
            trial.enforce_photo_policy(
                "测试医生",
                "https://www.gyfyyy.cn/images/doctor/TEST.jpg",
                "jpg",
                trial.FULL_FUSE_BYTES + 1,
            )


if __name__ == "__main__":
    unittest.main()
