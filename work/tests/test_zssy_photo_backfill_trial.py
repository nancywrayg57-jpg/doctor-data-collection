from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path

from PIL import Image


WORK_DIR = Path(r"D:\workspace\信息收集整理\work")
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import zssy_photo_backfill_trial as target  # noqa: E402


class ZssyPhotoBackfillTrialTests(unittest.TestCase):
    def page(self, name: str, media_tag: str, generic_tag: str = "") -> str:
        return f"""
        <html><head><title>{name} | {target.HOSPITAL}</title></head><body>
          <div class="physician-details-left">
            <div class="physician-details-media">{media_tag}</div>
          </div>
          {generic_tag}
        </body></html>
        """

    def test_accepts_data_image_url_and_excludes_generic_media(self) -> None:
        portrait = '<div class="media-img" data-image-url="/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/a.jpg"></div>'
        generic = '<div class="media-img" data-image-url="/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/naoz.png?itok=x"></div>'
        state, result = target.inspect_portrait_reference(
            self.page("张晓红", portrait, generic),
            "https://www.zssy.com.cn/node/11100",
            "张晓红",
        )
        self.assertEqual(state, "")
        self.assertIsNotNone(result)
        self.assertEqual(
            result.photo_url,
            "https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/a.jpg",
        )

    def test_accepts_inline_background_image(self) -> None:
        media = '<div class="media-img" style="background-image:url(\'/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/a.png\')"></div>'
        state, result = target.inspect_portrait_reference(
            self.page("张晓红", media),
            "https://www.zssy.com.cn/node/11100",
            "张晓红",
        )
        self.assertEqual(state, "")
        self.assertEqual(result.source_attribute, "inline background-image")

    def test_rejects_conflicting_data_and_style_urls(self) -> None:
        media = (
            '<div class="media-img" '
            'data-image-url="/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/a.jpg" '
            'style="background-image:url(/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/b.jpg)"></div>'
        )
        with self.assertRaisesRegex(RuntimeError, "不一致"):
            target.inspect_portrait_reference(
                self.page("张晓红", media),
                "https://www.zssy.com.cn/node/11100",
                "张晓红",
            )

    def test_rejects_official_page_but_off_path_photo(self) -> None:
        media = '<div class="media-img" data-image-url="/themes/logo.png"></div>'
        with self.assertRaisesRegex(RuntimeError, "越界"):
            target.inspect_portrait_reference(
                self.page("张晓红", media),
                "https://www.zssy.com.cn/node/11100",
                "张晓红",
            )

    def test_placeholder_marker_is_classified(self) -> None:
        media = '<div class="media-img" data-image-url="/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/default-avatar.jpg"></div>'
        state, result = target.inspect_portrait_reference(
            self.page("张晓红", media),
            "https://www.zssy.com.cn/node/11100",
            "张晓红",
        )
        self.assertEqual(state, "占位图")
        self.assertIsNone(result)

    def test_primary_title_is_longest_first(self) -> None:
        self.assertEqual(target.primary_title("副主任医师 导师资格 硕士生导师"), "副主任医师")
        self.assertEqual(target.title_level("副主任医师 导师资格 硕士生导师"), "副高")
        self.assertEqual(target.title_level("主任医师 导师资格 博士生导师"), "正高")
        self.assertEqual(target.title_level("主治医师"), "中级")
        self.assertEqual(target.title_level("住院医师、硕士"), "初级")

    def test_bilingual_department_prefers_chinese_atom(self) -> None:
        row = {"科室_分类页": "Interventional Radiology Program, 介入科"}
        self.assertEqual(target.atomic_department(row), "介入科")

    def test_magic_and_dimensions(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (37, 53), "white").save(buffer, format="JPEG")
        content = buffer.getvalue()
        self.assertEqual(target.magic_extension(content, "image/jpeg"), "jpg")
        self.assertEqual(target.image_dimensions(content), (37, 53))

    def test_page_referenced_url_rejects_query_or_third_party(self) -> None:
        base = "https://www.zssy.com.cn/node/11100"
        self.assertEqual(
            target.page_referenced_photo_url(
                "https://example.com/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/a.jpg",
                base,
            ),
            "",
        )
        self.assertEqual(
            target.page_referenced_photo_url(
                "/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/a.jpg?bad=1",
                base,
            ),
            "",
        )


if __name__ == "__main__":
    unittest.main()
