from __future__ import annotations

import base64
import copy
import io
import json
import sys
import unittest
from pathlib import Path, PureWindowsPath

from PIL import Image


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import ny5y_photo_backfill_full as full


class Ny5yPhotoBackfillFullTests(unittest.TestCase):
    def test_scope_and_authorization_are_issue_79_specific(self) -> None:
        self.assertEqual(full.ISSUE_NUMBER, 79)
        self.assertEqual(full.EXPECTED_SCOPE_COUNT, 134)
        self.assertEqual(full.EXPECTED_TRIAL_REUSE_COUNT, 10)
        self.assertEqual(full.EXPECTED_FRESH_COUNT, 124)
        self.assertIn("PR #80", full.FULL_AUTHORIZATION)

    def test_analyze_full_media_uses_unique_css_background_container(self) -> None:
        html = """
        <html><body>
          <img src="images/logo.jpg">
          <div class="yisheng_xq_bug_left"
               style="background-image:url(/ueditor/php/upload/image/20221014/a.png)"></div>
          <div class="yuanzhang">黄艺洪 <span>门诊部副主任</span></div>
          <div class="xq_zhicheng">主任医师、医学硕士、岭南名医</div>
        </body></html>
        """
        analysis = full.analyze_full_doctor_media(
            html, "http://www.ny5y.cn/yisheng_xq.php?id=282", "黄艺洪"
        )
        self.assertEqual(analysis.page_name, "黄艺洪")
        self.assertEqual(analysis.page_title, "主任医师、医学硕士、岭南名医")
        self.assertEqual(analysis.state, "")
        self.assertEqual(
            analysis.photo_url,
            "http://www.ny5y.cn/ueditor/php/upload/image/20221014/a.png",
        )
        self.assertEqual(analysis.photo_reference_count, 1)

    def test_analyze_full_media_rejects_duplicate_container(self) -> None:
        html = """
        <div class="yisheng_xq_bug_left" style="background-image:url(/ueditor/php/upload/image/a.png)"></div>
        <div class="yisheng_xq_bug_left" style="background-image:url(/ueditor/php/upload/image/b.png)"></div>
        <div class="yuanzhang">黄艺洪</div>
        <div class="xq_zhicheng">主任医师、医学硕士、岭南名医</div>
        """
        with self.assertRaisesRegex(RuntimeError, "容器不唯一"):
            full.analyze_full_doctor_media(
                html, "http://www.ny5y.cn/yisheng_xq.php?id=282", "黄艺洪"
            )

    def test_analyze_full_media_classifies_missing_container(self) -> None:
        html = "<html><title>南方医科大学第五附属医院</title><body></body></html>"
        analysis = full.analyze_full_doctor_media(
            html, "http://www.ny5y.cn/yisheng_xq.php?id=282", "黄艺洪"
        )
        self.assertEqual(analysis.state, "无照片容器")
        self.assertEqual(analysis.photo_reference_count, 0)

    def test_placeholder_gate_decodes_query_base64(self) -> None:
        encoded = base64.b64encode(b"blank2.jpg").decode()
        image = io.BytesIO()
        color = Image.new("RGB", (20, 20), "red")
        color.putpixel((0, 0), (0, 255, 0))
        color.putpixel((1, 0), (0, 0, 255))
        color.save(image, format="PNG")
        reason = full.placeholder_response_reason(
            f"http://www.ny5y.cn/ueditor/php/upload/image/a.png?token={encoded}",
            image.getvalue(),
            20,
            20,
        )
        self.assertIn("blank2.jpg", reason)

    def test_placeholder_gate_blocks_near_monochrome_image(self) -> None:
        image = io.BytesIO()
        Image.new("RGB", (200, 200), "white").save(image, format="PNG")
        reason = full.placeholder_response_reason(
            "http://www.ny5y.cn/ueditor/php/upload/image/a.png",
            image.getvalue(),
            200,
            200,
        )
        self.assertIn("唯一颜色数=1", reason)

    def test_full_page_reference_returns_url_and_query(self) -> None:
        url, query = full.page_referenced_photo_url_for_full(
            "/ueditor/php/upload/image/20221014/a.png?x=1",
            "http://www.ny5y.cn/yisheng_xq.php?id=282",
        )
        self.assertEqual(
            url, "http://www.ny5y.cn/ueditor/php/upload/image/20221014/a.png?x=1"
        )
        self.assertEqual(query, "x=1")

    def test_size_buckets_cover_all_owner_thresholds(self) -> None:
        samples = [
            {"bytes": 100},
            {"bytes": 300 * 1024},
            {"bytes": 2 * 1024 * 1024},
            {"bytes": 6 * 1024 * 1024},
            {"bytes": 21 * 1024 * 1024},
        ]
        self.assertEqual(
            full.size_buckets(samples),
            {
                "<200KiB": 1,
                "200KiB-1MiB": 1,
                "1-5MiB": 1,
                "5-20MiB": 1,
                ">20MiB": 1,
            },
        )

    def test_session_declares_only_owner_approved_user_agent(self) -> None:
        session = full.OfficialUrlOpenSession()
        self.assertEqual(session.cookie_names, [])
        self.assertEqual(session.default_headers, [["User-Agent", full.trial.USER_AGENT]])

    def test_owner_same_person_allowlist_is_exact_and_annotated(self) -> None:
        samples = []
        reconciliation = {}
        for digest, approved in full.OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS.items():
            for index, source in enumerate(sorted(approved["sources"])):
                samples.append(
                    {
                        "sha256": digest,
                        "name": approved["name"],
                        "source_link": source,
                        "photo_url": f"http://www.ny5y.cn/ueditor/php/upload/image/{digest[:8]}-{index}.png",
                    }
                )
                reconciliation[source] = {"来源链接": source, "错误证据": ""}

        full.decorate_owner_approved_duplicate_groups(samples, reconciliation)
        prior = full.framework.OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS
        full.framework.OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS = (
            full.OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS
        )
        try:
            self.assertEqual(full.framework.cross_doctor_duplicate_sha_groups(samples), {})
            for item in samples:
                note = full.same_person_allowlist_note(item["sha256"])
                self.assertEqual(item["same_person_allowlist_decision"], note)
                self.assertEqual(reconciliation[item["source_link"]]["错误证据"], note)

            unexpected = [dict(item) for item in samples[:2]]
            unexpected[1]["source_link"] = "http://www.ny5y.cn/yisheng_xq.php?id=999"
            self.assertIn(
                unexpected[0]["sha256"],
                full.framework.cross_doctor_duplicate_sha_groups(unexpected),
            )
        finally:
            full.framework.OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS = prior

    def test_committed_trial_manifest_still_matches_payload(self) -> None:
        payload = json.loads(full.trial.TRIAL_JSON_PATH.read_text(encoding="utf-8"))
        portable_payload = copy.deepcopy(payload)
        for sample in portable_payload["photo_samples"]:
            legacy_path = PureWindowsPath(sample["disk_path"])
            if legacy_path.is_absolute():
                work_index = next(
                    index
                    for index, part in enumerate(legacy_path.parts)
                    if part.casefold() == "work"
                )
                relative_path = Path(*legacy_path.parts[work_index:])
                resolved_path = full.ROOT / relative_path
                self.assertTrue(resolved_path.is_file())
                sample["disk_path"] = str(resolved_path)
        full.validate_trial_payload_for_full(
            portable_payload, require_visual_pass=True
        )
        full.validate_trial_manifest(payload)


if __name__ == "__main__":
    unittest.main()
