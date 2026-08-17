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

import sysu5_photo_backfill_trial as target  # noqa: E402


class Sysu5PhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_paths_are_relative_to_checkout(self) -> None:
        self.assertEqual(target.ROOT, WORK_DIR.parent)
        self.assertEqual(target.WORK_DIR, WORK_DIR)

    def test_parses_unique_featured_media_image(self) -> None:
        photo = (
            "/sites/default/files/styles/watermark/public/2026-01/"
            "%E4%B8%81%E7%AB%8B.jpg?itok=abc123"
        )
        html = f"""
        <html><head><title>丁立 | 中山大学附属第五医院</title></head>
        <body class="page-node page-node-type-doctor">
          <img src="/sites/default/files/styles/watermark/public/banner.jpg?itok=banner">
          <div class="field field-featured-media field-item"><picture>
            <img width="800" height="1173" src="{photo}">
          </picture></div>
        </body></html>
        """
        state, portrait = target.inspect_portrait_reference(
            html,
            "https://www.sysu5.cn/medical-service/department-expert/doctor/10285",
            "丁立",
        )
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)
        assert portrait is not None
        self.assertEqual(portrait.source_attribute, "src")
        self.assertEqual(portrait.reference_kind, "派生图")
        self.assertEqual(portrait.derivative_style, "watermark")
        self.assertEqual(portrait.photo_url, "https://www.sysu5.cn" + photo)

    def test_non_featured_image_is_not_a_portrait_container(self) -> None:
        html = """
        <title>丁立 | 中山大学附属第五医院</title>
        <body class="page-node-type-doctor">
          <picture><img src="/sites/default/files/styles/watermark/public/a.jpg?itok=x"></picture>
        </body>
        """
        state, portrait = target.inspect_portrait_reference(
            html,
            "https://www.sysu5.cn/medical-service/department-expert/doctor/10285",
            "丁立",
        )
        self.assertEqual(state, "无照片容器")
        self.assertIsNone(portrait)

    def test_rejects_original_or_unexpected_query_parameter(self) -> None:
        base = "https://www.sysu5.cn/medical-service/department-expert/doctor/10285"
        self.assertEqual(
            target.page_referenced_photo_url(
                "/sites/default/files/2026-01/a.jpg", base
            ),
            "",
        )
        self.assertEqual(
            target.page_referenced_photo_url(
                "/sites/default/files/styles/watermark/public/a.jpg?width=800", base
            ),
            "",
        )
        self.assertEqual(
            target.page_referenced_photo_url(
                "/sites/default/files/styles/watermark/public/a.jpg?itok=ok", base
            ),
            "https://www.sysu5.cn/sites/default/files/styles/watermark/public/a.jpg?itok=ok",
        )

    def test_title_layers_and_primary_titles(self) -> None:
        self.assertEqual(target.primary_title("教授，主任医师"), "主任医师")
        self.assertEqual(target.title_level("教授，主任医师"), "正高")
        self.assertEqual(target.title_level("副主任医师，医学博士"), "副高")
        self.assertEqual(target.title_level("主治医师，医学硕士"), "其他")

    def test_scope_and_fixed_sample_plan_are_stable(self) -> None:
        rows = target.load_scope_rows()
        selected = target.select_trial_rows(rows)
        self.assertEqual(len(rows), 413)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(
            len({target.atomic_department(row) for row in selected}),
            target.MIN_TRIAL_DEPARTMENTS,
        )
        self.assertEqual(
            {target.title_level(row.get("职称身份原文")) for row in selected},
            {"正高", "副高", "其他"},
        )
        self.assertEqual(
            [target.clean_text(row.get("姓名")) for row in selected],
            [name for name, _, _ in target.SAMPLE_PLAN],
        )
        self.assertEqual(
            [target.detail_id(row.get("来源链接")) for row in selected],
            [detail for _, _, detail in target.SAMPLE_PLAN],
        )

    def test_magic_and_dimensions(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (37, 53), "white").save(buffer, format="JPEG")
        content = buffer.getvalue()
        self.assertEqual(target.magic_extension(content, "image/jpeg"), "jpg")
        self.assertEqual(target.image_dimensions(content), (37, 53))

    def test_small_gif_gray_or_nopic_is_placeholder(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (400, 600), (238, 238, 238)).save(buffer, format="GIF")
        content = buffer.getvalue()
        self.assertLess(len(content), target.SMALL_GIF_PLACEHOLDER_BYTES)
        self.assertIn(
            "占位图",
            target.downloaded_placeholder_reason(
                "https://www.sysu5.cn/sites/default/files/styles/watermark/public/nopic.gif?itok=x",
                content,
                "gif",
            ),
        )
        self.assertIn(
            "灰底占比",
            target.downloaded_placeholder_reason(
                "https://www.sysu5.cn/sites/default/files/styles/watermark/public/portrait.gif?itok=x",
                content,
                "gif",
            ),
        )

    def test_small_colorful_gif_is_not_placeholder(self) -> None:
        image = Image.new("RGB", (32, 32))
        for y in range(32):
            for x in range(32):
                image.putpixel(
                    (x, y),
                    ((x * 37 + y * 13) % 256, (x * 17) % 256, (y * 29) % 256),
                )
        buffer = io.BytesIO()
        image.save(buffer, format="GIF")
        content = buffer.getvalue()
        self.assertEqual(
            target.downloaded_placeholder_reason(
                "https://www.sysu5.cn/sites/default/files/styles/watermark/public/portrait.gif?itok=x",
                content,
                "gif",
            ),
            "",
        )

    def test_allocate_trial_name_and_no_overwrite(self) -> None:
        row = {
            "姓名": "丁立",
            "科室_分类页": "感染病防治中心",
            "职称身份原文": "感染病一科主任，主任医师",
            "来源链接": "https://www.sysu5.cn/medical-service/department-expert/doctor/10285",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(target, "TRIAL_PHOTO_DIR", Path(temp_dir)):
                filename, path = target.allocate_trial_photo(row, "jpg", b"one")
                self.assertEqual(
                    filename,
                    "丁立-感染病防治中心-主任医师-中山大学附属第五医院.jpg",
                )
                path.write_bytes(b"one")
                self.assertEqual(
                    target.allocate_trial_photo(row, "jpg", b"one"),
                    (filename, path),
                )
                alternate, _ = target.allocate_trial_photo(row, "jpg", b"two")
                self.assertTrue(alternate.endswith("-10285.jpg"))

    def test_size_buckets(self) -> None:
        self.assertEqual(target.size_bucket(10), "<200KiB")
        self.assertEqual(target.size_bucket(target.LARGE_BYTES), "200KiB-1MiB")
        self.assertEqual(target.size_bucket(2 * 1024 * 1024), "1-5MiB")
        self.assertEqual(target.size_bucket(6 * 1024 * 1024), ">5MiB")


if __name__ == "__main__":
    unittest.main()
