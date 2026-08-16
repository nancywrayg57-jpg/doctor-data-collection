from __future__ import annotations

import io
import sys
import tempfile
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

    def test_governance_generic_department_media_is_classified_placeholder(self) -> None:
        media = '<div class="media-img" data-image-url="/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/%E5%B9%BB%E7%81%AF%E7%89%871_0.PNG"></div>'
        state, result = target.inspect_portrait_reference(
            self.page("神经内科", media),
            "https://www.zssy.com.cn/node/15390",
            "神经内科",
        )
        self.assertEqual(state, "占位图")
        self.assertIsNone(result)

    def test_complete_page_title_alias_map_from_780_page_preflight(self) -> None:
        self.assertEqual(
            target.PAGE_TITLE_ALIAS_BY_SOURCE,
            {
                "https://www.zssy.com.cn/node/6008": "内科ICU",
                "https://www.zssy.com.cn/node/14062": "外科ICU",
                "https://www.zssy.com.cn/node/14071": "精神（心理）科",
                "https://www.zssy.com.cn/node/14068": "口腔医学中心",
                "https://www.zssy.com.cn/node/14098": "变态反应（过敏）学科",
                "https://www.zssy.com.cn/node/11316": "甲状腺、乳腺外科",
                "https://www.zssy.com.cn/node/15410": "神经外科（天河）",
                "https://www.zssy.com.cn/node/15466": "精神（心理）科",
                "https://www.zssy.com.cn/node/30221": "针灸专科（脑病方向）",
            },
        )

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

    def test_official_session_retries_incomplete_read_once(self) -> None:
        class Headers:
            @staticmethod
            def get_content_type() -> str:
                return "image/jpeg"

            @staticmethod
            def get_content_charset() -> None:
                return None

        class Response:
            status = 200
            headers = Headers()

            def __enter__(self) -> "Response":
                return self

            def __exit__(self, *args: object) -> None:
                return None

            @staticmethod
            def read() -> bytes:
                return b"\xff\xd8\xffpayload"

        class Opener:
            def __init__(self) -> None:
                self.calls = 0

            def open(self, request: object, timeout: int) -> Response:
                self.calls += 1
                if self.calls == 1:
                    raise target.IncompleteRead(b"partial", 5)
                return Response()

        session = target.OfficialSession()
        opener = Opener()
        session.opener = opener
        status, content_type, _, content = session.get(
            "https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/a.jpg",
            "https://www.zssy.com.cn/node/11100",
        )
        self.assertEqual((status, content_type), (200, "image/jpeg"))
        self.assertEqual(content, b"\xff\xd8\xffpayload")
        self.assertEqual(opener.calls, 2)
        self.assertEqual(session.incomplete_read_retry_count, 1)

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

    def test_full_authorization_and_warning_are_explicit(self) -> None:
        self.assertIn("PR #58", target.FULL_AUTHORIZATION)
        self.assertIn("FULL_APPEND_AND_OBSIDIAN", target.FULL_AUTHORIZATION)
        warning = target.append_failure_warning("既有提示", "无照片容器")
        self.assertEqual(
            warning,
            f"既有提示；{target.FULL_WARNING_BY_STATE['无照片容器']}",
        )

    def test_full_row_diff_allows_only_target_photo_columns(self) -> None:
        source = "https://www.zssy.com.cn/node/11100"
        before = [{"来源链接": source, "照片链接": "", "照片文件": "", "姓名": "甲"}]
        after = [{**before[0], "照片链接": "https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/a.jpg"}]
        diffs = target.collect_full_row_diffs(before, after, {source})
        self.assertEqual([item["列名"] for item in diffs], ["照片链接"])
        with self.assertRaisesRegex(RuntimeError, "范围外行"):
            target.collect_full_row_diffs(before, after, set())
        with self.assertRaisesRegex(RuntimeError, "范围外字段"):
            target.collect_full_row_diffs(before, [{**before[0], "姓名": "乙"}], {source})

    def test_surgical_profile_insert_preserves_bom_and_crlf(self) -> None:
        before = (
            b"\xef\xbb\xbf---\r\n"
            b"generated_by: generate_obsidian_profiles.py\r\n"
            b"---\r\n\r\n# Doctor\r\n\r\n## Basic\r\n\r\n"
        )
        before = before.replace(b"## Basic", "## 基础信息".encode("utf-8"))
        photo_file = "01_试点医院/中山大学附属第三医院/照片/甲-内科-医师-中山大学附属第三医院.jpg"
        after = target.insert_profile_photo_block_bytes(before, "甲", photo_file)
        self.assertTrue(after.startswith(b"\xef\xbb\xbf"))
        self.assertIn(
            "![甲](照片/甲-内科-医师-中山大学附属第三医院.jpg)\r\n\r\n".encode("utf-8"),
            after,
        )
        target.validate_profile_photo_only_bytes(before, after, "甲", photo_file)

    def test_full_validator_closes_780_failure_rows(self) -> None:
        rows = []
        reconciliation = []
        warning = target.FULL_WARNING_BY_STATE["无照片容器"]
        for index in range(target.EXPECTED_SCOPE_COUNT):
            source = f"https://www.zssy.com.cn/node/{10000 + index}"
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
        payload = {
            "meta": {
                "expected_count": target.EXPECTED_SCOPE_COUNT,
                "downloaded_count": 0,
                "failed_count": target.EXPECTED_SCOPE_COUNT,
                "blank_count": target.EXPECTED_SCOPE_COUNT,
                "failure_state_counts": {
                    "详情不可达": 0,
                    "无照片容器": target.EXPECTED_SCOPE_COUNT,
                    "占位图": 0,
                },
                "detail_unreachable_count": 0,
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "existing_profile_count": target.EXPECTED_EXISTING_PROFILE_COUNT,
                "no_profile_scope_count": target.EXPECTED_SCOPE_COUNT
                - target.EXPECTED_EXISTING_PROFILE_COUNT,
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
