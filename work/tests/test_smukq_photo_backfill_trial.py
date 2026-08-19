from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import smukq_photo_backfill_trial as target


class SmukqPhotoBackfillTrialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.framework_state = dict(vars(target.framework))
        self.base_state = dict(vars(target.base))
        target.configure_framework()

    def tearDown(self) -> None:
        for module, state in (
            (target.framework, self.framework_state),
            (target.base, self.base_state),
        ):
            for name in set(vars(module)) - set(state):
                delattr(module, name)
            for name, value in state.items():
                setattr(module, name, value)

    def test_root_is_repository_relative_to_script(self) -> None:
        self.assertEqual(target.ROOT, Path(target.__file__).resolve().parents[1])
        source = Path(target.__file__).read_text(encoding="utf-8")
        self.assertNotIn("D:\\workspace", source)

    def test_scope_and_authorization_are_issue_81_specific(self) -> None:
        rows = target.load_scope_rows()
        selected = target.select_trial_rows(rows)
        self.assertEqual(len(rows), 95)
        self.assertEqual(len(selected), 10)
        self.assertEqual(
            {target.section_id(row["来源链接"]) for row in selected},
            set(target.SECTION_COUNTS),
        )
        self.assertEqual(
            {
                level: sum(
                    target.base.title_level(row["职称身份原文"]) == level
                    for row in selected
                )
                for level in target.EXPECTED_TITLE_COUNTS
            },
            target.EXPECTED_TITLE_COUNTS,
        )

    def test_detail_url_is_strict_https_section_and_id(self) -> None:
        self.assertEqual(
            target.detail_parts("https://www.smukqyy.cn/prods/343/555"),
            ("343", "555"),
        )
        for value in (
            "http://www.smukqyy.cn/prods/343/555",
            "https://evil.example/prods/343/555",
            "https://www.smukqyy.cn/prods/999/555",
            "https://www.smukqyy.cn/prods/343/555?x=1",
            "https://www.smukqyy.cn/section/343",
        ):
            self.assertIsNone(target.detail_parts(value))

    def test_content_img_is_the_only_eligible_container(self) -> None:
        html = """
        <img src="/Home/images/top_tel.png">
        <img class="content_img" width="118" height="147"
             src="/Uploads/Upload/2022-08-18/doctor.jpg">
        <span class="content2_span1">何龙文</span>
        <span class="content2_span2">主治医师，硕士</span>
        <img src="/Public/Home/images/footer.png">
        """
        state, portrait = target.inspect_portrait_reference(
            html, "https://www.smukqyy.cn/prods/343/555", "何龙文"
        )
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)
        self.assertEqual(
            portrait.photo_url,
            "https://www.smukqyy.cn/Uploads/Upload/2022-08-18/doctor.jpg",
        )
        self.assertEqual(portrait.source_attribute, "img.content_img src")

    def test_duplicate_content_img_is_rejected(self) -> None:
        html = """
        <img class="content_img" src="/Uploads/Upload/a.jpg">
        <img class="content_img" src="/Uploads/Upload/b.jpg">
        <span class="content2_span1">何龙文</span>
        """
        with self.assertRaisesRegex(RuntimeError, "容器不唯一"):
            target.inspect_portrait_reference(
                html, "https://www.smukqyy.cn/prods/343/555", "何龙文"
            )

    def test_photo_url_rejects_decorations_and_placeholders(self) -> None:
        source = "https://www.smukqyy.cn/prods/343/555"
        self.assertEqual(
            target.page_referenced_photo_url(
                "/Uploads/Upload/2022-08-18/doctor.jpg", source
            ),
            "https://www.smukqyy.cn/Uploads/Upload/2022-08-18/doctor.jpg",
        )
        for value in (
            "/Home/images/top_tel.png",
            "/Public/Home/images/footer.png",
            "/Uploads/Upload/default.jpg",
            "https://evil.example/Uploads/Upload/doctor.jpg",
        ):
            self.assertEqual(target.page_referenced_photo_url(value, source), "")

    def test_query_base64_placeholder_gate_is_preserved(self) -> None:
        source = "https://www.smukqyy.cn/prods/343/555"
        value = "/Uploads/Upload/doctor.jpg?token=YmxhbmsuanBn"
        self.assertEqual(target.page_referenced_photo_url(value, source), "")

    def test_magic_signature_overrides_octet_stream_declaration(self) -> None:
        self.assertEqual(
            target.magic_extension(b"\xff\xd8\xff\xe0jpeg", "application/octet-stream"),
            "jpg",
        )
        self.assertEqual(
            target.magic_extension(b"<html>not an image</html>", "image/jpeg"),
            "",
        )

    def test_session_uses_only_owner_approved_user_agent(self) -> None:
        session = target.framework.OfficialSession()
        self.assertEqual(session.cookie_names, [])
        self.assertIsInstance(session.opener.handlers[0], object)

    def test_normalized_payload_contains_no_absolute_repo_path(self) -> None:
        sample_path = target.TRIAL_PHOTO_DIR / "sample.jpg"
        payload = {
            "meta": {
                "protected_assets_before": {
                    "master_assets": {
                        str(target.base.MASTER_JSON_PATH): {
                            "bytes": 1,
                            "sha256": "x",
                        }
                    },
                    "profile_tree": {},
                    "formal_photo_tree": {},
                },
                "protected_assets_after": {
                    "master_assets": {
                        str(target.base.MASTER_JSON_PATH): {
                            "bytes": 1,
                            "sha256": "x",
                        }
                    },
                    "profile_tree": {},
                    "formal_photo_tree": {},
                },
            },
            "photo_samples": [{"disk_path": str(sample_path)}],
        }
        target.normalize_payload_paths(payload)
        text = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn(str(target.ROOT), text)
        self.assertEqual(
            payload["photo_samples"][0]["disk_path"],
            "work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_photos/sample.jpg",
        )


if __name__ == "__main__":
    unittest.main()
