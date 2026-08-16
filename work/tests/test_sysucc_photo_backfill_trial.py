from __future__ import annotations

import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image


WORK_DIR = Path(r"D:\workspace\信息收集整理\work")
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import sysucc_photo_backfill_trial as target  # noqa: E402


class SysuccPhotoBackfillTrialTests(unittest.TestCase):
    def test_parses_standard_item_media_src(self) -> None:
        photo = (
            "/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/"
            "media_2_3_400_600/public/2023-04/xiazhongjun.jpg?itok=abc123"
        )
        html = f"""
        <html><head><title>夏忠军 | 中山大学肿瘤防治中心</title></head>
        <body class="page-node page-node-type-doctor">
          <div class="title-4-0"><div class="item-media">
            <img class="w-full" src="{photo}">
          </div></div>
        </body></html>
        """
        state, portrait = target.inspect_portrait_reference(
            html, "https://www.sysucc.org.cn/node/3795", "夏忠军"
        )
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)
        assert portrait is not None
        self.assertEqual(portrait.source_attribute, "src")
        self.assertEqual(portrait.reference_kind, "派生图")
        self.assertEqual(portrait.derivative_style, "media_2_3_400_600")
        self.assertEqual(
            portrait.photo_url,
            "https://www.sysucc.org.cn" + photo,
        )

    def test_rejects_off_path_photo(self) -> None:
        html = """
        <title>夏忠军 | 中山大学肿瘤防治中心</title>
        <body class="page-node-type-doctor">
          <div class="title-4-0"><div class="item-media">
            <img src="https://www.sysucc.org.cn/themes/custom/photo.jpg">
          </div></div>
        </body>
        """
        with self.assertRaisesRegex(RuntimeError, "越界"):
            target.inspect_portrait_reference(
                html, "https://www.sysucc.org.cn/node/3795", "夏忠军"
            )

    def test_marks_known_public_decoration_as_placeholder(self) -> None:
        html = """
        <title>夏忠军 | 中山大学肿瘤防治中心</title>
        <body class="page-node-type-doctor">
          <div class="title-4-0"><div class="item-media">
            <img src="/sites/cc.prod.sysucloud2.sysu.edu.cn/files/2022-11/Bitmap.png">
          </div></div>
        </body>
        """
        state, portrait = target.inspect_portrait_reference(
            html, "https://www.sysucc.org.cn/node/3795", "夏忠军"
        )
        self.assertEqual(state, "占位图")
        self.assertIsNone(portrait)

    def test_rejects_unexpected_query_parameter(self) -> None:
        value = (
            "/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/"
            "media_2_3_400_600/public/a.jpg?width=800"
        )
        self.assertEqual(
            target.page_referenced_photo_url(
                value, "https://www.sysucc.org.cn/node/3795"
            ),
            "",
        )

    def test_accepts_original_reference_without_constructing_it(self) -> None:
        value = "/sites/cc.prod.sysucloud2.sysu.edu.cn/files/2024-01/a.jpg"
        url = target.page_referenced_photo_url(
            value, "https://www.sysucc.org.cn/node/3795"
        )
        self.assertEqual(
            url,
            "https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/2024-01/a.jpg",
        )
        self.assertEqual(target.reference_kind(url), ("原图", ""))

    def test_title_layers_and_primary_titles(self) -> None:
        self.assertEqual(target.primary_title("主诊教授、副主任医师"), "副主任医师")
        self.assertEqual(target.title_level("主诊教授、副主任医师"), "副高")
        self.assertEqual(target.primary_title("二级教授、一级主任医师"), "一级主任医师")
        self.assertEqual(target.title_level("二级教授、一级主任医师"), "正高")
        self.assertEqual(target.primary_title("科主任导师 职称：教授"), "教授")
        self.assertEqual(target.title_level("张玉晶"), "其他")

    def test_scope_and_fixed_sample_plan_are_stable(self) -> None:
        rows = target.load_scope_rows()
        selected = target.select_trial_rows(rows)
        self.assertEqual(len(rows), 543)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(len({target.atomic_department(row) for row in selected}), 3)
        self.assertEqual(
            {target.title_level(row.get("职称身份原文")) for row in selected},
            {"正高", "副高", "其他"},
        )
        self.assertEqual(
            [target.clean_text(row.get("姓名")) for row in selected],
            [name for name, _ in target.SAMPLE_PLAN],
        )

    def test_magic_and_dimensions(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (37, 53), "white").save(buffer, format="JPEG")
        content = buffer.getvalue()
        self.assertEqual(target.magic_extension(content, "image/jpeg"), "jpg")
        self.assertEqual(target.image_dimensions(content), (37, 53))

    def test_allocate_trial_name_and_no_overwrite(self) -> None:
        row = {
            "姓名": "夏忠军",
            "科室_分类页": "血液肿瘤科",
            "职称身份原文": "主诊教授、副主任医师",
            "来源链接": "https://www.sysucc.org.cn/node/3795",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(target, "TRIAL_PHOTO_DIR", Path(temp_dir)):
                filename, path = target.allocate_trial_photo(row, "jpg", b"one")
                self.assertEqual(
                    filename,
                    "夏忠军-血液肿瘤科-副主任医师-中山大学肿瘤防治中心.jpg",
                )
                path.write_bytes(b"one")
                same_name, same_path = target.allocate_trial_photo(row, "jpg", b"one")
                self.assertEqual((same_name, same_path), (filename, path))
                alternate, _ = target.allocate_trial_photo(row, "jpg", b"two")
                self.assertTrue(alternate.endswith("-3795.jpg"))


if __name__ == "__main__":
    unittest.main()
