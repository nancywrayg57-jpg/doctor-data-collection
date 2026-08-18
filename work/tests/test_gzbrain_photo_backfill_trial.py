from __future__ import annotations

import sys
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gzbrain_photo_backfill_trial as trial  # noqa: E402


class GzbrainPhotoBackfillTrialTests(unittest.TestCase):
    def test_detail_id_accepts_only_exact_official_https_template(self) -> None:
        self.assertEqual(
            trial.detail_id("https://www.gzbrain.cn/myzj/info_itemid_966.html"), "966"
        )
        for value in (
            "http://www.gzbrain.cn/myzj/info_itemid_966.html",
            "https://evil.example/myzj/info_itemid_966.html",
            "https://www.gzbrain.cn/myzj/info_itemid_966.html?x=1",
            "https://www.gzbrain.cn/myzj/info_itemid_abc.html",
            "https://www.gzbrain.cn/yydt/info_itemid_966.html",
        ):
            self.assertEqual(trial.detail_id(value), "")

    def test_photo_url_preserves_page_opaque_query(self) -> None:
        source = "https://www.gzbrain.cn/myzj/info_itemid_966.html"
        raw = "/uploadfiles/2019/06/a.png?5a6B546J6JCNLnBuZw=="
        self.assertEqual(
            trial.page_referenced_photo_url(raw, source),
            ("https://www.gzbrain.cn/uploadfiles/2019/06/a.png?5a6B546J6JCNLnBuZw==", "5a6B546J6JCNLnBuZw=="),
        )

    def test_photo_url_rejects_unreferenced_or_nonportrait_shapes(self) -> None:
        source = "https://www.gzbrain.cn/myzj/info_itemid_966.html"
        for raw in (
            "/uploadfiles/2019/06/a.png",
            "/uploadfiles/2019/06/a.png?x=1&y=2",
            "https://evil.example/uploadfiles/2019/06/a.png?abc",
            "http://www.gzbrain.cn/uploadfiles/2019/06/a.png?abc",
            "/uploadfiles/banner/hero.jpg?abc",
            "/uploadfiles/image/yyhj_img4.jpg?abc",
            "/uploadfiles/2019/06/logo.png?abc",
        ):
            self.assertEqual(trial.page_referenced_photo_url(raw, source), ("", ""))

    def test_analysis_accepts_only_exact_single_img_hierarchy(self) -> None:
        html = """
        <html><body>
          <header><img src="/uploadfiles/2023/11/logo.png?abc"></header>
          <div class="single_con">
            <div class="single-header"><h2>宁玉萍</h2><h3><span>主任医师</span></h3></div>
            <div class="single_cn">
              <div class="single-img"><img src="/uploadfiles/2019/06/a.png?abc==" alt=""></div>
              <div class="single_tex"><p>官方简介</p></div>
            </div>
          </div>
        </body></html>
        """
        result = trial.analyze_doctor_media(
            html, "https://www.gzbrain.cn/myzj/info_itemid_966.html", "宁玉萍"
        )
        self.assertEqual(result.state, "")
        self.assertEqual(result.page_title, "主任医师")
        self.assertEqual(result.photo_reference_count, 1)
        self.assertEqual(result.single_con_image_count, 1)
        self.assertEqual(result.outside_image_reference_count, 1)
        self.assertEqual(result.template_signature, trial.TEMPLATE_SIGNATURE)
        self.assertIn('class="single-img"', result.container_html_snippet)

    def test_analysis_does_not_promote_outside_images(self) -> None:
        html = """
        <html><body>
          <img src="/uploadfiles/2019/06/someone.png?abc">
          <div class="single_con">
            <div class="single-header"><h2>宁玉萍</h2><h3>主任医师</h3></div>
            <div class="single_cn"><div class="single_tex">无照片</div></div>
          </div>
        </body></html>
        """
        result = trial.analyze_doctor_media(
            html, "https://www.gzbrain.cn/myzj/info_itemid_966.html", "宁玉萍"
        )
        self.assertEqual(result.state, "无照片容器")
        self.assertEqual(result.photo_url, "")

    def test_analysis_rejects_multiple_direct_photo_images(self) -> None:
        html = """
        <div class="single_con">
          <div class="single-header"><h2>宁玉萍</h2><h3>主任医师</h3></div>
          <div class="single_cn"><div class="single-img">
            <img src="/uploadfiles/2019/06/a.png?abc">
            <img src="/uploadfiles/2019/06/b.png?def">
          </div></div>
        </div>
        """
        with self.assertRaisesRegex(RuntimeError, "不是唯一直接"):
            trial.analyze_doctor_media(
                html, "https://www.gzbrain.cn/myzj/info_itemid_966.html", "宁玉萍"
            )

    def test_analysis_rejects_name_mismatch(self) -> None:
        html = """
        <div class="single_con">
          <div class="single-header"><h2>其他人</h2><h3>主任医师</h3></div>
          <div class="single_cn"><div class="single-img">
            <img src="/uploadfiles/2019/06/a.png?abc">
          </div></div>
        </div>
        """
        with self.assertRaisesRegex(RuntimeError, "姓名不一致"):
            trial.analyze_doctor_media(
                html, "https://www.gzbrain.cn/myzj/info_itemid_966.html", "宁玉萍"
            )

    def test_placeholder_inside_strict_container_is_not_downloadable(self) -> None:
        html = """
        <div class="single_con">
          <div class="single-header"><h2>宁玉萍</h2><h3>主任医师</h3></div>
          <div class="single_cn"><div class="single-img">
            <img src="/uploadfiles/2019/06/noimage.png?abc">
          </div></div>
        </div>
        """
        result = trial.analyze_doctor_media(
            html, "https://www.gzbrain.cn/myzj/info_itemid_966.html", "宁玉萍"
        )
        self.assertEqual(result.state, "占位图")
        self.assertEqual(result.photo_url, "")

    def test_sample_plan_covers_ten_departments_and_four_levels(self) -> None:
        title_by_level = {
            "正高": "主任医师",
            "副高": "副主任医师",
            "中级": "主治医师",
            "其他": "心理治疗师",
        }
        rows = [
            {
                "姓名": name,
                "科室_分类页": department,
                "职称身份原文": title_by_level[level],
                "来源链接": f"https://www.gzbrain.cn/myzj/info_itemid_{item_id}.html",
            }
            for name, department, level, item_id in trial.SAMPLE_PLAN
        ]
        selected = trial.select_trial_rows(rows)
        self.assertEqual(len(selected), 10)
        self.assertEqual(len({trial.atomic_department(row) for row in selected}), 10)

    def test_magic_extension_uses_bytes_when_url_and_header_say_jpeg(self) -> None:
        png = b"\x89PNG\r\n\x1a\n" + b"payload"
        self.assertEqual(trial.magic_extension(png, "image/jpeg"), "png")
        self.assertEqual(trial.magic_extension(png, "text/html"), "")

    def test_urllib_session_has_no_cookie_or_custom_browser_headers(self) -> None:
        session = trial.OfficialUrlOpenSession()
        self.assertEqual(session.cookie_names, [])
        self.assertFalse(
            any("mozilla" in value.lower() for _, value in session.default_headers)
        )


if __name__ == "__main__":
    unittest.main()
