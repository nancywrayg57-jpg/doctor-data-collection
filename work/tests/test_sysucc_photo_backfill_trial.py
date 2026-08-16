from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import sysucc_photo_backfill_trial as target  # noqa: E402


class SysuccPhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_paths_are_relative_to_checkout(self) -> None:
        self.assertEqual(target.ROOT, WORK_DIR.parent)
        self.assertEqual(target.WORK_DIR, WORK_DIR)

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

    def test_overlong_polluted_department_is_unlabeled_for_filename(self) -> None:
        row = {
            "科室_分类页": "本科 " + "教育经历与工作经历污染文本" * 20,
            "科室_列表卡片": "",
        }
        self.assertEqual(target.photo_filename_department(row), "未标注")
        self.assertEqual(
            target.photo_filename_department({"科室_分类页": "妇科"}),
            "妇科",
        )

    def test_scope_and_fixed_sample_plan_are_stable(self) -> None:
        payload = json.loads(target.MASTER_JSON_PATH.read_text(encoding="utf-8"))
        for row in payload["rows"]:
            if target.clean_text(row.get("医院")) == target.HOSPITAL:
                row["照片链接"] = ""
                row["照片文件"] = ""
        with tempfile.TemporaryDirectory() as temp_dir:
            baseline_path = Path(temp_dir) / "master-before-photo-backfill.json"
            baseline_path.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            with patch.object(target, "MASTER_JSON_PATH", baseline_path):
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

    def test_complete_page_title_alias_map_from_542_page_preflight(self) -> None:
        self.assertEqual(
            target.PAGE_TITLE_ALIAS_BY_SOURCE,
            {
                "https://www.sysucc.org.cn/node/3741": "肖祥胜",
                "https://www.sysucc.org.cn/node/1488": "周宁宁",
                "https://www.sysucc.org.cn/node/1482": "李宇红",
                "https://www.sysucc.org.cn/node/1505": "王德深",
                "https://www.sysucc.org.cn/node/1479": "王树森",
                "https://www.sysucc.org.cn/node/1485": "王风华",
                "https://www.sysucc.org.cn/node/1475": "黄慧强",
                "https://www.sysucc.org.cn/node/1683": "曹新平",
                "https://www.sysucc.org.cn/node/1658": "刘慧(小)",
                "https://www.sysucc.org.cn/node/3883": "张琳",
                "https://www.sysucc.org.cn/node/3723": "秦自科",
                "https://www.sysucc.org.cn/node/3645": "邱际亮",
                "https://www.sysucc.org.cn/node/3612": "杨浩贤",
                "https://www.sysucc.org.cn/node/6668": "刘敏",
                "https://www.sysucc.org.cn/node/1528": "郭灵",
            },
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

    def test_full_authorization_and_taxonomy_warning_are_explicit(self) -> None:
        self.assertIn("PR #60", target.FULL_AUTHORIZATION)
        self.assertIn("FULL_APPEND_AND_OBSIDIAN", target.FULL_AUTHORIZATION)
        warning = target.append_warning("既有提示", target.TAXONOMY_WARNING)
        self.assertEqual(
            warning,
            f"既有提示；{target.TAXONOMY_WARNING}",
        )
        self.assertEqual(
            target.append_warning(warning, target.TAXONOMY_WARNING),
            warning,
        )

    def test_full_row_diff_allows_only_target_photo_columns(self) -> None:
        source = "https://www.sysucc.org.cn/node/3795"
        before = [
            {
                "来源链接": source,
                "照片链接": "",
                "照片文件": "",
                "异常提示": "",
                "姓名": "夏忠军",
            }
        ]
        after = [
            {
                **before[0],
                "照片链接": (
                    "https://www.sysucc.org.cn/sites/"
                    "cc.prod.sysucloud2.sysu.edu.cn/files/styles/"
                    "media_2_3_400_600/public/a.jpg?itok=x"
                ),
            }
        ]
        diffs = target.collect_full_row_diffs(before, after, {source})
        self.assertEqual([item["列名"] for item in diffs], ["照片链接"])
        with self.assertRaisesRegex(RuntimeError, "范围外行"):
            target.collect_full_row_diffs(before, after, set())
        with self.assertRaisesRegex(RuntimeError, "范围外字段"):
            target.collect_full_row_diffs(
                before, [{**before[0], "姓名": "错误"}], {source}
            )

    def test_surgical_profile_insert_preserves_bom_and_crlf(self) -> None:
        before = (
            b"\xef\xbb\xbf---\r\n"
            b"generated_by: generate_obsidian_profiles.py\r\n"
            b"---\r\n\r\n# Doctor\r\n\r\n## Basic\r\n\r\n"
        )
        before = before.replace(b"## Basic", "## 基础信息".encode("utf-8"))
        photo_file = (
            "01_试点医院/中山大学肿瘤防治中心/照片/"
            "夏忠军-血液肿瘤科-副主任医师-中山大学肿瘤防治中心.jpg"
        )
        after = target.insert_profile_photo_block_bytes(
            before, "夏忠军", photo_file
        )
        self.assertTrue(after.startswith(b"\xef\xbb\xbf"))
        self.assertIn(
            (
                "![夏忠军](照片/"
                "夏忠军-血液肿瘤科-副主任医师-中山大学肿瘤防治中心.jpg)"
                "\r\n\r\n"
            ).encode("utf-8"),
            after,
        )
        target.validate_profile_photo_only_bytes(
            before, after, "夏忠军", photo_file
        )

    def test_full_validator_closes_542_plus_1_blank_rows(self) -> None:
        rows = []
        reconciliation = []
        warning = target.FULL_WARNING_BY_STATE["无照片容器"]
        for index in range(target.EXPECTED_COLLECT_COUNT):
            source = f"https://www.sysucc.org.cn/node/{10000 + index}"
            rows.append(
                {
                    "姓名": f"医生{index}",
                    "来源链接": source,
                    "照片链接": "",
                    "照片文件": "",
                    "异常提示": warning,
                }
            )
            reconciliation.append(
                {
                    "姓名": f"医生{index}",
                    "来源链接": source,
                    "状态": "失败",
                    "失败三态": "无照片容器",
                }
            )
        rows.append(
            {
                "姓名": "医学教育",
                "来源链接": target.TAXONOMY_SOURCE,
                "照片链接": "",
                "照片文件": "",
                "异常提示": target.TAXONOMY_WARNING,
            }
        )
        reconciliation.append(
            {
                "姓名": "医学教育",
                "来源链接": target.TAXONOMY_SOURCE,
                "状态": "不适用",
                "失败三态": "",
            }
        )
        payload = {
            "meta": {
                "scope_count": target.EXPECTED_SCOPE_COUNT,
                "expected_count": target.EXPECTED_COLLECT_COUNT,
                "downloaded_count": 0,
                "failed_count": target.EXPECTED_COLLECT_COUNT,
                "not_applicable_count": 1,
                "blank_count": target.EXPECTED_SCOPE_COUNT,
                "taxonomy_source": target.TAXONOMY_SOURCE,
                "failure_state_counts": {
                    "详情不可达": 0,
                    "无照片容器": target.EXPECTED_COLLECT_COUNT,
                    "占位图": 0,
                },
                "detail_unreachable_count": 0,
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "existing_profile_source_count": target.EXPECTED_PROFILE_SOURCE_COUNT,
                "page_title_alias_count": len(target.PAGE_TITLE_ALIAS_BY_SOURCE),
                "photo_total_bytes": 0,
                "photo_max_bytes": 0,
                "over_5mib_count": 0,
            },
            "rows": rows,
            "reconciliation": reconciliation,
            "photo_samples": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            target.validate_full_payload(payload, Path(directory))


if __name__ == "__main__":
    unittest.main()
