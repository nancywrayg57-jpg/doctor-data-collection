from __future__ import annotations

import base64
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import ny5y_photo_backfill_trial as trial


class Ny5yPhotoBackfillTrialTests(unittest.TestCase):
    def test_detail_id_accepts_only_authorized_shape(self) -> None:
        self.assertEqual(trial.detail_id("http://www.ny5y.cn/yisheng_xq.php?id=282"), "282")
        self.assertEqual(trial.detail_id("https://ny5y.cn/yisheng_xq.php?id=1"), "1")
        self.assertEqual(trial.detail_id("http://www.ny5y.cn/yisheng_xq.php?id=0"), "")
        self.assertEqual(trial.detail_id("http://www.ny5y.cn/yisheng_xq.php?id=1&x=2"), "")
        self.assertEqual(trial.detail_id("https://example.com/yisheng_xq.php?id=282"), "")

    def test_inspect_portrait_uses_unique_css_container_and_name(self) -> None:
        html = """
        <html><body>
          <div class="top" style="background-image:url(images/logo.jpg)"></div>
          <div class="yisheng_xq_bug_left"
               style="background-image: url(/ueditor/php/upload/image/20221014/a.png)"></div>
          <div class="yuanzhang">黄艺洪 <span>门诊部副主任</span></div>
        </body></html>
        """
        state, portrait = trial.inspect_portrait_reference(
            html, "http://www.ny5y.cn/yisheng_xq.php?id=282", "黄艺洪"
        )
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)
        assert portrait is not None
        self.assertEqual(
            portrait.photo_url,
            "http://www.ny5y.cn/ueditor/php/upload/image/20221014/a.png",
        )
        self.assertIn("yisheng_xq_bug_left", portrait.source_attribute)

    def test_inspect_portrait_rejects_wrong_name_and_duplicate_container(self) -> None:
        wrong_name = """
        <div class="yisheng_xq_bug_left" style="background-image:url(/ueditor/php/upload/image/a.png)"></div>
        <div class="yuanzhang">其他人</div>
        """
        with self.assertRaisesRegex(RuntimeError, "详情姓名与底表不一致"):
            trial.inspect_portrait_reference(
                wrong_name, "http://www.ny5y.cn/yisheng_xq.php?id=282", "黄艺洪"
            )
        duplicate = """
        <div class="yisheng_xq_bug_left" style="background-image:url(/ueditor/php/upload/image/a.png)"></div>
        <div class="yisheng_xq_bug_left" style="background-image:url(/ueditor/php/upload/image/b.png)"></div>
        <div class="yuanzhang">黄艺洪</div>
        """
        with self.assertRaisesRegex(RuntimeError, "容器不唯一"):
            trial.inspect_portrait_reference(
                duplicate, "http://www.ny5y.cn/yisheng_xq.php?id=282", "黄艺洪"
            )

    def test_query_base64_placeholder_gate(self) -> None:
        encoded = base64.b64encode("blank2.jpg".encode()).decode()
        url = f"http://www.ny5y.cn/ueditor/php/upload/image/a.jpg?token={encoded}"
        self.assertEqual(trial.suspicious_query_decoding(url), "blank2.jpg")
        self.assertEqual(
            trial.page_referenced_photo_url(url, "http://www.ny5y.cn/yisheng_xq.php?id=1"),
            "",
        )

    def test_unique_color_gate(self) -> None:
        one_color = io.BytesIO()
        Image.new("RGB", (20, 20), "white").save(one_color, format="PNG")
        self.assertEqual(trial.limited_unique_color_count(one_color.getvalue()), 1)
        many_colors = Image.new("RGB", (3, 1))
        many_colors.putdata([(0, 0, 0), (128, 128, 128), (255, 255, 255)])
        output = io.BytesIO()
        many_colors.save(output, format="PNG")
        self.assertEqual(trial.limited_unique_color_count(output.getvalue()), 3)

    def test_page_referenced_photo_url_boundary(self) -> None:
        base_url = "http://www.ny5y.cn/yisheng_xq.php?id=282"
        self.assertEqual(
            trial.page_referenced_photo_url(
                "/ueditor/php/upload/image/20221014/a.png", base_url
            ),
            "http://www.ny5y.cn/ueditor/php/upload/image/20221014/a.png",
        )
        self.assertEqual(trial.page_referenced_photo_url("/images/logo.jpg", base_url), "")
        self.assertEqual(
            trial.page_referenced_photo_url("https://example.com/ueditor/php/upload/image/a.png", base_url),
            "",
        )

    def test_sample_plan_meets_owner_coverage(self) -> None:
        self.assertEqual(len(trial.SAMPLE_PLAN), 10)
        counts = {level: 0 for level in trial.EXPECTED_TITLE_COUNTS}
        for _, level in trial.SAMPLE_PLAN:
            counts[level] += 1
        self.assertEqual(counts, trial.EXPECTED_TITLE_COUNTS)

    def test_select_trial_rows_accepts_actual_three_level_distribution(self) -> None:
        rows = []
        for index, (name, level) in enumerate(trial.SAMPLE_PLAN):
            title = {"正高": "主任医师", "副高": "副主任医师", "中级": "主治医师"}[level]
            rows.append(
                {
                    "姓名": name,
                    "职称身份原文": title,
                    "科室_分类页": f"科室{index % 6}",
                }
            )
        selected = trial.select_trial_rows(rows)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(
            len({trial.base.atomic_department(row) for row in selected}),
            trial.MIN_TRIAL_DEPARTMENTS,
        )

    def test_reachability_preflight_uses_two_rounds_and_detail_gate(self) -> None:
        class FakeSession:
            def get(self, url: str, referer: str = "") -> tuple[int, str, str, bytes]:
                if url == trial.OFFICIAL_HOME:
                    return 502, "text/html", "utf-8", b"gateway"
                return 200, "text/html", "utf-8", b"detail"

        with patch.object(trial.time, "sleep") as sleep:
            observations = trial.reachability_preflight(
                FakeSession(),
                "http://www.ny5y.cn/yisheng_xq.php?id=282",
                interval_seconds=30,
            )
        self.assertEqual(len(observations), 4)
        self.assertEqual(
            [item["status"] for item in observations if item["target"] == "homepage_non_gate"],
            [502, 502],
        )
        self.assertEqual(
            [item["status"] for item in observations if item["target"] == "sample_detail_gate"],
            [200, 200],
        )
        sleep.assert_called_once_with(30)


if __name__ == "__main__":
    unittest.main()
