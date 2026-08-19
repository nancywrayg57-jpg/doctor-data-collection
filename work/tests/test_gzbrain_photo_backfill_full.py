from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gzbrain_photo_backfill_full as target  # noqa: E402


class GzbrainPhotoBackfillFullTests(unittest.TestCase):
    def test_scope_constants_match_owner_full_instruction(self) -> None:
        self.assertEqual(target.ISSUE_NUMBER, 77)
        self.assertEqual(target.EXPECTED_SCOPE_COUNT, 183)
        self.assertEqual(target.EXPECTED_TRIAL_REUSE_COUNT, 10)
        self.assertEqual(target.EXPECTED_FRESH_COUNT, 173)
        self.assertEqual(
            target.FULL_FAILURE_STATES,
            ("详情不可达", "照片资源不可达", "无照片容器", "占位图"),
        )

    def test_append_warning_is_idempotent_and_preserves_existing(self) -> None:
        result = target.append_warning("同名待甄别", "无照片容器")
        self.assertEqual(
            result,
            "同名待甄别；官网本人职业照补录失败：无照片容器",
        )
        self.assertEqual(target.append_warning(result, "无照片容器"), result)

    def test_allocate_full_photo_path_uses_detail_id_for_collision(self) -> None:
        row = {
            "姓名": "医生",
            "科室_分类页": "神经内科",
            "职称身份原文": "主任医师",
            "来源链接": "https://www.gzbrain.cn/myzj/info_itemid_966.html",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            used: set[str] = set()
            first, _ = target.allocate_full_photo_path(row, "jpg", root, used)
            second, _ = target.allocate_full_photo_path(row, "jpg", root, used)
        self.assertTrue(first.endswith("医院.jpg"))
        self.assertTrue(second.endswith("医院-966.jpg"))

    def test_allocate_full_photo_path_preserves_trial_filename(self) -> None:
        row = {
            "姓名": "成友军",
            "科室_分类页": "神经外科",
            "职称身份原文": "副主任医师",
            "来源链接": "https://www.gzbrain.cn/myzj/info_itemid_803.html",
        }
        preferred = "成友军-神经外科-副主任医师-广州医科大学附属脑科医院.png"
        with tempfile.TemporaryDirectory() as temp_dir:
            filename, _ = target.allocate_full_photo_path(
                row, "png", Path(temp_dir), set(), preferred
            )
        self.assertEqual(filename, preferred)

    def test_attempts_flicker_detects_status_change(self) -> None:
        attempts = [
            {"status": 403, "content_type": "text/html", "error": ""},
            {"status": 200, "content_type": "text/html", "error": ""},
        ]
        self.assertTrue(target.attempts_flicker(attempts))
        self.assertFalse(target.attempts_flicker([attempts[0], attempts[0]]))

    def test_placeholder_gate_is_conservative(self) -> None:
        self.assertIn(
            "占位",
            target.placeholder_response_reason(
                "https://www.gzbrain.cn/uploadfiles/2020/01/noimage.jpg?abc",
                b"x" * 100,
                10,
                10,
            ),
        )
        self.assertEqual(
            target.placeholder_response_reason(
                "https://www.gzbrain.cn/uploadfiles/2020/01/doctor.jpg?abc",
                b"x" * 20000,
                315,
                422,
            ),
            "",
        )

    def test_full_analysis_classifies_generic_doctor_image_as_placeholder(self) -> None:
        html = """
        <div class="single_con">
          <div class="single-header"><h2>医生</h2><h3>主任医师</h3></div>
          <div class="single_cn"><div class="single-img">
            <img src="/uploadfiles/image/doctor_img1.jpg?ZG9jdG9yX2ltZzEuanBn">
          </div></div>
        </div>
        """
        result = target.analyze_full_doctor_media(
            html, "https://www.gzbrain.cn/myzj/info_itemid_877.html", "医生"
        )
        self.assertEqual(result.state, "占位图")
        self.assertEqual(result.photo_reference_count, 1)

    def test_full_analysis_allows_page_referenced_bmp_only_for_later_gate(self) -> None:
        html = """
        <div class="single_con">
          <div class="single-header"><h2>医生</h2><h3>主任医师</h3></div>
          <div class="single_cn"><div class="single-img">
            <img src="/uploadfiles/2019/06/x.bmp?dmNyZWRpc3QuYm1w">
          </div></div>
        </div>
        """
        result = target.analyze_full_doctor_media(
            html, "https://www.gzbrain.cn/myzj/info_itemid_989.html", "医生"
        )
        self.assertEqual(result.state, "")
        self.assertTrue(result.photo_url.endswith("?dmNyZWRpc3QuYm1w"))

    def test_profile_insert_is_exact_plus_two_lines(self) -> None:
        before = (
            f"{target.AUTO_MARKER}\n# 医生\n\n## 基础信息\n\n- 姓名：医生\n"
        ).encode("utf-8")
        photo_file = "01_试点医院/广州医科大学附属脑科医院/照片/医生.jpg"
        after = target.insert_profile_photo_block_bytes(before, "医生", photo_file)
        target.validate_profile_photo_only_bytes(before, after, "医生", photo_file)
        self.assertIn("![医生](照片/医生.jpg)", after.decode("utf-8"))

    def test_profile_insert_rejects_existing_photo(self) -> None:
        before = "## 基础信息\n\n![医生](照片/医生.jpg)\n\n"
        with self.assertRaisesRegex(RuntimeError, "已存在照片"):
            target.insert_profile_photo_block(before, "医生", "照片/医生.jpg")

    def test_collect_row_diffs_rejects_non_photo_columns(self) -> None:
        source = "https://www.gzbrain.cn/myzj/info_itemid_1.html"
        before = [{"姓名": "医生", "来源链接": source, "照片链接": ""}]
        after = [{"姓名": "另一人", "来源链接": source, "照片链接": ""}]
        with self.assertRaisesRegex(RuntimeError, "范围外字段"):
            target.collect_full_row_diffs(
                before,
                after,
                {source},
                ["姓名", "来源链接", "照片链接"],
            )

    def test_failure_evidence_is_machine_auditable(self) -> None:
        evidence = {
            "observed_utc": "2026-08-19T00:00:00Z",
            "resource_urls": ["https://www.gzbrain.cn/myzj/info_itemid_1.html"],
            "photo_reference_count": 0,
            "detection_feature": "single-img missing",
        }
        parsed = json.loads(target.failure_evidence_text(evidence))
        self.assertEqual(parsed, evidence)

    def test_visual_review_report_line_reflects_completed_review(self) -> None:
        line = target.full_visual_review_report_line(
            {
                "visual_review_sheet_count": 8,
                "visual_review_photo_count": 181,
                "visual_review_status": target.FULL_VISUAL_PASS_STATUS,
            }
        )
        self.assertIn("已由 Codex 逐页目视确认", line)
        self.assertNotIn("待 Codex", line)

    def test_validate_full_payload_rejects_unclosed_four_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with self.assertRaisesRegex(RuntimeError, "四数对账"):
                target.validate_full_payload(
                    {"meta": {"expected_count": 183, "downloaded_count": 182}},
                    root,
                    root / "audit.jpg",
                    root / "visual",
                )

    def test_write_reconciliation_keeps_failure_evidence(self) -> None:
        payload = {
            "reconciliation": [
                {
                    "详情ID": "1",
                    "姓名": "医生",
                    "来源链接": "source",
                    "状态": "失败留空",
                    "失败分类": "无照片容器",
                    "照片引用数": 0,
                    "错误证据": '{"observed_utc":"2026-08-19T00:00:00Z"}',
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "reconciliation.csv"
            target.write_reconciliation_csv(path, payload)
            content = path.read_text(encoding="utf-8-sig")
        self.assertIn("无照片容器", content)
        self.assertIn("observed_utc", content)


if __name__ == "__main__":
    unittest.main()
