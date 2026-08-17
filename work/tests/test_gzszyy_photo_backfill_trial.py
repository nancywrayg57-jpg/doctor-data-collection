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

import gzszyy_photo_backfill_trial as trial  # noqa: E402


def image_bytes(fmt: str = "PNG", color: tuple[int, int, int] = (40, 90, 140)) -> bytes:
    stream = io.BytesIO()
    Image.new("RGB", (120, 160), color).save(stream, format=fmt)
    return stream.getvalue()


def response(
    *,
    status: int = 200,
    content: bytes = b"",
    content_type: str = "text/html; charset=utf-8",
    url: str = "https://www.gzszyy.com/",
) -> trial.HttpResult:
    return trial.HttpResult(
        status_code=status,
        url=url,
        trace=((status, url),),
        headers={"content-type": content_type},
        content=content,
        charset="utf-8",
    )


class GzszyyPhotoBackfillTrialTests(unittest.TestCase):
    def test_detail_scope_is_exact(self) -> None:
        valid = "https://www.gzszyy.com/expert/2026/w9aADOev.html"
        self.assertEqual(trial.detail_id(valid), "w9aADOev")
        for invalid in (
            "http://www.gzszyy.com/expert/2026/w9aADOev.html",
            "https://oss.gzszyy.com/expert/2026/w9aADOev.html",
            "https://www.gzszyy.com/expert/2026/w9aADOev.html?x=1",
            "https://www.gzszyy.com/expert/1/dp/3780/",
            "https://www.gzszyy.com/expert/2026/w9a-DOev.html",
        ):
            with self.subTest(invalid=invalid):
                self.assertEqual(trial.detail_id(invalid), "")

    def test_page_photo_only_uses_unique_doctor_img_reference(self) -> None:
        source = "https://www.gzszyy.com/expert/2026/w9aADOev.html"
        html = """
        <html><body><div class="doctor-resume">
          <div class="doctor-img"><img src="https://oss.gzszyy.com/20200722/175120692.jpg"></div>
          <h1>叶穗林</h1>
        </div><div class="doctor-code"><div class="qr-img">
          <img src="https://oss.gzszyy.com/20200630/170722311.png">
        </div></div><img src="//static.gzszyy.com/images/qualification.png"></body></html>
        """
        self.assertEqual(
            trial.page_referenced_photo(html, source, "叶穗林"),
            "https://oss.gzszyy.com/20200722/175120692.jpg",
        )

    def test_page_photo_rejects_static_qr_empty_and_multiple_references(self) -> None:
        source = "https://www.gzszyy.com/expert/2026/w9aADOev.html"
        cases = (
            '<div class="doctor-resume"><div class="doctor-img"><img src=""></div><h1>叶穗林</h1></div>',
            '<div class="doctor-resume"><div class="doctor-img"><img src="//static.gzszyy.com/images/a.jpg"></div><h1>叶穗林</h1></div>',
            '<div class="doctor-resume"><h1>叶穗林</h1></div><div class="qr-img"><img src="https://oss.gzszyy.com/20200101/1.jpg"></div>',
            '<div class="doctor-resume"><div class="doctor-img"><img src="https://oss.gzszyy.com/20200101/1.jpg"><img src="https://oss.gzszyy.com/20200101/2.jpg"></div><h1>叶穗林</h1></div>',
        )
        for html in cases:
            with self.subTest(html=html), self.assertRaisesRegex(RuntimeError, "图片|src|容器|路径"):
                trial.page_referenced_photo(html, source, "叶穗林")

    def test_page_photo_rejects_name_mismatch_and_query(self) -> None:
        source = "https://www.gzszyy.com/expert/2026/w9aADOev.html"
        mismatch = '<div class="doctor-resume"><div class="doctor-img"><img src="https://oss.gzszyy.com/20200101/1.jpg"></div><h1>其他人</h1></div>'
        with self.assertRaisesRegex(RuntimeError, "姓名不匹配"):
            trial.page_referenced_photo(mismatch, source, "叶穗林")
        query = '<div class="doctor-resume"><div class="doctor-img"><img src="https://oss.gzszyy.com/20200101/1.jpg?x=1"></div><h1>叶穗林</h1></div>'
        with self.assertRaisesRegex(RuntimeError, "越出授权"):
            trial.page_referenced_photo(query, source, "叶穗林")

    def test_magic_dimensions_and_photo_response_validation(self) -> None:
        content = image_bytes("PNG")
        photo_response = response(
            content=content,
            content_type="image/png",
            url="https://oss.gzszyy.com/20260101/1.png",
        )
        extension, width, height, content_type = trial.inspect_photo_response(
            photo_response, photo_response.url
        )
        self.assertEqual((extension, width, height), ("png", 120, 160))
        self.assertEqual(content_type, "image/png")
        self.assertEqual(trial.magic_extension(image_bytes("JPEG")), "jpg")

    def test_photo_response_rejects_http_content_type_magic_and_twenty_mib(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "HTTP 404"):
            trial.inspect_photo_response(response(status=404), "https://oss.gzszyy.com/20260101/1.jpg")
        with self.assertRaisesRegex(RuntimeError, "非图片"):
            trial.inspect_photo_response(response(content=b"<html>bad</html>"), "https://oss.gzszyy.com/20260101/1.jpg")
        with self.assertRaisesRegex(RuntimeError, "魔数"):
            trial.inspect_photo_response(
                response(content=b"not-an-image", content_type="image/jpeg"),
                "https://oss.gzszyy.com/20260101/1.jpg",
            )
        with patch.object(trial, "FULL_FUSE_BYTES", 8):
            with self.assertRaisesRegex(RuntimeError, "FATAL"):
                trial.inspect_photo_response(
                    response(content=image_bytes("JPEG"), content_type="image/jpeg"),
                    "https://oss.gzszyy.com/20260101/1.jpg",
                )

    def test_small_gif_placeholder_requires_two_sided_boundary(self) -> None:
        neutral = image_bytes("GIF", (230, 230, 230))
        colorful = image_bytes("GIF", (20, 80, 160))
        self.assertRegex(
            trial.placeholder_reason(
                "https://oss.gzszyy.com/20260101/1.gif", neutral, "gif"
            ),
            "浅灰",
        )
        self.assertEqual(
            trial.placeholder_reason(
                "https://oss.gzszyy.com/20260101/1.gif", colorful, "gif"
            ),
            "",
        )
        self.assertEqual(
            trial.placeholder_reason(
                "https://oss.gzszyy.com/20260101/placeholder.jpg", neutral, "jpg"
            ),
            "",
        )

    def test_require_html_checks_status_and_content_type(self) -> None:
        good = response(content="<html>中文</html>".encode("utf-8"))
        self.assertIn("中文", trial.require_html(good, "详情"))
        with self.assertRaisesRegex(RuntimeError, "HTTP 503"):
            trial.require_html(response(status=503), "详情")
        with self.assertRaisesRegex(RuntimeError, "Content-Type"):
            trial.require_html(
                response(content=b"{}", content_type="application/json"), "详情"
            )

    def test_sample_plan_is_ten_departments_and_three_three_four(self) -> None:
        rows = []
        title_by_level = {"正高": "主任中医师", "副高": "副主任中医师", "其他": "医师"}
        for name, department, level, identifier in trial.SAMPLE_PLAN:
            rows.append(
                {
                    "医院": trial.HOSPITAL,
                    "姓名": name,
                    "科室_分类页": department,
                    "职称_关键词": title_by_level[level],
                    "来源链接": f"https://www.gzszyy.com/expert/2026/{identifier}.html",
                }
            )
        selected = trial.select_trial_rows(rows)
        self.assertEqual(len(selected), 10)
        self.assertEqual(len({trial.atomic_department(row) for row in selected}), 10)
        self.assertEqual(
            {level: sum(trial.title_level(row["职称_关键词"]) == level for row in selected) for level in ("正高", "副高", "其他")},
            {"正高": 3, "副高": 3, "其他": 4},
        )

    def test_allocate_trial_photo_is_idempotent_and_rejects_byte_change(self) -> None:
        row = {"姓名": "叶穗林", "科室_分类页": "名医堂、心病科", "职称_关键词": "主任中医师"}
        with tempfile.TemporaryDirectory() as temp_dir, patch.object(
            trial, "TRIAL_PHOTO_DIR", Path(temp_dir)
        ):
            content = image_bytes("JPEG")
            path, filename = trial.allocate_trial_photo(row, "jpg", content)
            self.assertEqual(path.read_bytes(), content)
            self.assertIn("叶穗林-名医堂-主任中医师-广州市中医院.jpg", filename)
            trial.allocate_trial_photo(row, "jpg", content)
            with self.assertRaisesRegex(RuntimeError, "拒绝覆盖"):
                trial.allocate_trial_photo(row, "jpg", content + b"changed")

    def test_tree_digest_tracks_path_and_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "a.md").write_text("a", encoding="utf-8")
            first = trial.tree_digest(root, "*.md")
            self.assertEqual(first["file_count"], 1)
            (root / "a.md").write_text("b", encoding="utf-8")
            second = trial.tree_digest(root, "*.md")
            self.assertNotEqual(first["sha256"], second["sha256"])

    def test_full_failure_warning_is_idempotent(self) -> None:
        first = trial.append_failure_warning("既有提示", "详情不可达")
        second = trial.append_failure_warning(first, "详情不可达")
        self.assertEqual(first, second)
        self.assertEqual(first.count("官网本人职业照补录失败：详情不可达"), 1)

    def test_full_page_reference_classifies_missing_and_accepts_unique_oss(self) -> None:
        source = "https://www.gzszyy.com/expert/2026/w9aADOev.html"
        missing = '<div class="doctor-resume"><h1>叶穗林</h1></div>'
        state, photo_url, evidence = trial.inspect_full_page_reference(
            missing, source, "叶穗林"
        )
        self.assertEqual((state, photo_url), ("无照片容器", ""))
        self.assertIn("doctor-img", evidence)
        good = '<div class="doctor-resume"><div class="doctor-img"><img src="https://oss.gzszyy.com/20200101/1.jpg"></div><h1>叶穗林</h1></div>'
        self.assertEqual(
            trial.inspect_full_page_reference(good, source, "叶穗林"),
            ("", "https://oss.gzszyy.com/20200101/1.jpg", ""),
        )

    def test_retryable_get_records_three_spaced_failures(self) -> None:
        class FakeSession:
            def get(self, url: str, referer: str = "") -> trial.HttpResult:
                return response(status=503, url=url)

        stamps = [
            "2026-08-17T00:00:00Z",
            "2026-08-17T00:00:30Z",
            "2026-08-17T00:01:00Z",
        ]
        with patch.object(trial, "utc_now_text", side_effect=stamps), patch.object(
            trial.time, "sleep"
        ) as sleep:
            result, attempts = trial.retryable_get(
                FakeSession(), "https://www.gzszyy.com/a", "", lambda item: item.ok
            )
        self.assertIsNone(result)
        self.assertEqual(len(attempts), 3)
        self.assertEqual(sleep.call_count, 2)
        sleep.assert_called_with(30)
        trial.validate_retry_attempts(attempts)

    def test_retryable_get_fuses_on_status_flicker(self) -> None:
        class FakeSession:
            def __init__(self) -> None:
                self.calls = 0

            def get(self, url: str, referer: str = "") -> trial.HttpResult:
                self.calls += 1
                return response(status=503 if self.calls == 1 else 200, url=url)

        stamps = ["2026-08-17T00:00:00Z", "2026-08-17T00:00:30Z"]
        with patch.object(trial, "utc_now_text", side_effect=stamps), patch.object(
            trial.time, "sleep"
        ), self.assertRaisesRegex(RuntimeError, "FATAL.*状态闪烁"):
            trial.retryable_get(
                FakeSession(), "https://www.gzszyy.com/a", "", lambda item: item.ok
            )

    def test_profile_photo_insert_is_surgical(self) -> None:
        before = (
            "---\n姓名: 叶穗林\n---\n"
            + trial.AUTO_MARKER
            + "\n\n# 叶穗林\n\n## 基础信息\n\n| 字段 | 内容 |\n"
        ).encode("utf-8")
        photo_file = "01_试点医院/广州市中医院/照片/叶穗林.jpg"
        after = trial.insert_profile_photo_block_bytes(before, "叶穗林", photo_file)
        self.assertIn("![叶穗林](照片/叶穗林.jpg)".encode("utf-8"), after)
        trial.validate_profile_photo_only_bytes(before, after, "叶穗林", photo_file)

    def test_full_row_diff_rejects_out_of_scope_columns(self) -> None:
        source = "https://www.gzszyy.com/expert/2026/w9aADOev.html"
        before = [{header: "" for header in trial.BASE_HEADERS}]
        before[0]["来源链接"] = source
        after = [dict(before[0])]
        after[0]["照片链接"] = "https://oss.gzszyy.com/20200101/1.jpg"
        diffs = trial.collect_full_row_diffs(before, after, {source})
        self.assertEqual([item["列名"] for item in diffs], ["照片链接"])
        after[0]["姓名"] = "改名"
        with self.assertRaisesRegex(RuntimeError, "范围外字段"):
            trial.collect_full_row_diffs(before, after, {source})


if __name__ == "__main__":
    unittest.main()
