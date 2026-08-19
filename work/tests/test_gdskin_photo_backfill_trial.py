from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gdskin_photo_backfill_trial as target


class GdskinPhotoBackfillTrialTests(unittest.TestCase):
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

    def test_scope_and_authorization_are_issue_83_specific(self) -> None:
        rows = target.load_scope_rows(require_blank_photo_fields=False)
        selected = target.select_trial_rows(rows)
        self.assertEqual(len(rows), 77)
        self.assertEqual(len(selected), 10)
        self.assertEqual(
            {target.entry_id(row["采集入口"]) for row in selected},
            set(target.ENTRY_COUNTS),
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

    def test_owner_replacement_plan_and_failure_evidence_are_fixed(self) -> None:
        self.assertEqual(
            {item["replacement_name"] for item in target.REPLACEMENT_MATRIX},
            {"谷梅", "杜美毅", "钟泽敏"},
        )
        self.assertEqual(
            {item["name"] for item in target.PRIOR_FAILURE_EVIDENCE},
            {"吴芳芳", "孟凡琪", "杨超"},
        )
        meng = next(
            item
            for item in target.PRIOR_FAILURE_EVIDENCE
            if item["name"] == "孟凡琪"
        )
        self.assertIn("\u00a0 \u00a0", meng["raw_photo_reference"])
        self.assertIn("%C2%A0%20%C2%A0.jpg", meng["transport_url"])
        self.assertEqual(meng["photo_http_status"], 404)
        self.assertEqual(
            {item["name"] for item in target.REPLACEMENT_CANDIDATE_EVIDENCE},
            {"于碧慧", "龚洋洋", "郭先荟"},
        )
        for name in ("龚洋洋", "郭先荟"):
            item = next(
                evidence
                for evidence in target.REPLACEMENT_CANDIDATE_EVIDENCE
                if evidence["name"] == name
            )
            self.assertIn("\u00a0", item["raw_photo_reference"])
            self.assertIn("%C2%A0.jpg", item["transport_url"])
            self.assertEqual(item["photo_http_status"], 404)
        self.assertEqual(target.EXPECTED_REUSE_COUNT, 9)
        self.assertEqual(target.EXPECTED_NETWORK_REQUEST_COUNT, 17)
        self.assertEqual(target.EXPECTED_NEW_DOWNLOAD_COUNT, 1)

    def test_detail_url_is_strict_https_shownews_id(self) -> None:
        self.assertEqual(
            target.detail_id("https://www.gdskin.com/ShowNews.ASPX?ID=3847"),
            "3847",
        )
        for value in (
            "http://www.gdskin.com/ShowNews.ASPX?ID=3847",
            "https://evil.example/ShowNews.ASPX?ID=3847",
            "https://www.gdskin.com/ShowNews.ASPX?ID=0",
            "https://www.gdskin.com/ShowNews.ASPX?ID=3847&x=1",
            "https://www.gdskin.com/Showclass.aspx?id=906",
        ):
            self.assertEqual(target.detail_id(value), "")

    def test_entry_url_accepts_case_variant_and_rejects_unknown_id(self) -> None:
        self.assertEqual(
            target.entry_id("https://www.gdskin.com/Showclass.aspx?id=906"),
            "906",
        )
        self.assertEqual(
            target.entry_id("https://www.gdskin.com/ShowClass.aspx?id=922"),
            "922",
        )
        self.assertEqual(
            target.entry_id("https://www.gdskin.com/Showclass.aspx?id=999"),
            "",
        )

    def test_unique_uploadimg_is_the_only_eligible_container(self) -> None:
        html = """
        <title>钟泽敏 主治医师__广东省皮肤病医院官方网站</title>
        <img alt="跳过导航链接" src="/WebResource.axd?d=abc" width="0" height="0">
        <img width="400" alt="" src="../system_dntb/../uploadimg/钟泽敏\t.jpg">
        <img src="images/备案图标.png" alt="备案">
        """
        state, portrait = target.inspect_portrait_reference(
            html, "https://www.gdskin.com/ShowNews.ASPX?ID=5576", "钟泽敏"
        )
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)
        self.assertEqual(
            portrait.photo_url,
            "https://www.gdskin.com/uploadimg/钟泽敏.jpg",
        )
        self.assertEqual(
            portrait.source_attribute, "unique body img src under /uploadimg/"
        )

    def test_duplicate_uploadimg_candidates_are_rejected(self) -> None:
        html = """
        <title>杨斌 主任医师__广东省皮肤病医院官方网站</title>
        <img src="../uploadimg/a.jpg">
        <img src="../uploadimg/b.jpg">
        """
        with self.assertRaisesRegex(RuntimeError, "容器不唯一"):
            target.inspect_portrait_reference(
                html, "https://www.gdskin.com/ShowNews.ASPX?ID=3847", "杨斌"
            )

    def test_page_title_must_contain_exact_expected_name(self) -> None:
        html = """
        <title>陈永锋 主任医师__广东省皮肤病医院官方网站</title>
        <img src="../uploadimg/doctor.jpg">
        """
        with self.assertRaisesRegex(RuntimeError, "姓名与底表不一致"):
            target.inspect_portrait_reference(
                html, "https://www.gdskin.com/ShowNews.ASPX?ID=3847", "杨斌"
            )

    def test_explicit_chinese_placeholder_is_rejected_and_recorded(self) -> None:
        target.PLACEHOLDER_EVIDENCE.clear()
        html = """
        <title>文海泉 主任医师__广东省皮肤病医院官方网站</title>
        <img src="../uploadimg/占位.png" width="200" height="200">
        """
        state, portrait = target.inspect_portrait_reference(
            html, target.KNOWN_PLACEHOLDER_DETAIL_URL, target.KNOWN_PLACEHOLDER_NAME
        )
        self.assertEqual(state, "占位图")
        self.assertIsNone(portrait)
        self.assertEqual(
            target.PLACEHOLDER_EVIDENCE["marker_reason"],
            "explicit_chinese_placeholder_filename",
        )
        self.assertEqual(target.PLACEHOLDER_EVIDENCE["detail_id"], "5566")

    def test_photo_url_rejects_decorations_and_placeholder_markers(self) -> None:
        source = "https://www.gdskin.com/ShowNews.ASPX?ID=3847"
        self.assertEqual(
            target.page_referenced_photo_url("../uploadimg/杨斌2021.jpg", source),
            "https://www.gdskin.com/uploadimg/杨斌2021.jpg",
        )
        for value in (
            "/WebResource.axd?d=abc",
            "images/备案图标.png",
            "../uploadimg/占位.png",
            "../uploadimg/default.jpg",
            "https://evil.example/uploadimg/doctor.jpg",
            "../uploadimg/doctor.jpg?token=YmxhbmsuanBn",
        ):
            self.assertEqual(target.page_referenced_photo_url(value, source), "")

    def test_owner_known_placeholder_digest_is_exact(self) -> None:
        self.assertTrue(
            target.is_known_placeholder_digest(target.KNOWN_PLACEHOLDER_SHA256)
        )
        self.assertFalse(target.is_known_placeholder_digest("0" * 64))

    def test_unicode_page_reference_is_percent_encoded_only_for_transport(self) -> None:
        value = "https://www.gdskin.com/uploadimg/占位.png"
        self.assertEqual(
            target.transport_url(value),
            "https://www.gdskin.com/uploadimg/%E5%8D%A0%E4%BD%8D.png",
        )
        self.assertEqual(
            target.page_referenced_photo_url(
                "../uploadimg/杨斌2021.jpg",
                "https://www.gdskin.com/ShowNews.ASPX?ID=3847",
            ),
            "https://www.gdskin.com/uploadimg/杨斌2021.jpg",
        )

    def test_session_enforces_two_second_start_interval(self) -> None:
        session = target.GdskinOfficialSession()
        with (
            patch.object(target.time, "monotonic", side_effect=[100.0, 100.5, 102.0]),
            patch.object(target.time, "sleep") as sleep,
        ):
            self.assertIsNone(session._wait_for_slot())
            interval = session._wait_for_slot()
        sleep.assert_called_once_with(1.5)
        self.assertEqual(interval, 2.0)
        self.assertEqual(session.cookie_names, [])

    def test_session_reuses_prior_success_without_network_download(self) -> None:
        url = "https://www.gdskin.com/uploadimg/cached.jpg"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "顾有守-cached.jpg"
            content = b"\xff\xd8\xff\xe0cached-jpeg"
            path.write_bytes(content)
            target.PHOTO_CACHE_BY_URL.clear()
            target.REUSE_TRACE.clear()
            target.REQUEST_TRACE.clear()
            target.PHOTO_CACHE_BY_URL[url] = path
            session = target.GdskinOfficialSession()
            with (
                patch.object(target, "repo_relative", return_value="work/cached.jpg"),
                patch.object(target._BaseOfficialSession, "get") as network_get,
            ):
                status, content_type, _, actual = session.get(url)
            network_get.assert_not_called()
            self.assertEqual(status, 200)
            self.assertEqual(content_type, "image/jpeg")
            self.assertEqual(actual, content)
            self.assertEqual(len(target.REUSE_TRACE), 1)
            self.assertEqual(target.REQUEST_TRACE, [])
        target.PHOTO_CACHE_BY_URL.clear()
        target.REUSE_TRACE.clear()

    def test_repository_digest_normalizes_text_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text_path = root / "sample.md"
            binary_path = root / "sample.bin"
            text_path.write_bytes(b"a\r\nb\r\n")
            binary_path.write_bytes(b"a\r\nb\r\n")
            self.assertEqual(
                target.base.repository_digest_bytes(text_path), b"a\nb\n"
            )
            self.assertEqual(
                target.base.repository_digest_bytes(binary_path), b"a\r\nb\r\n"
            )

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
            "work/南方医科大学皮肤病医院_photo_backfill_trial_photos/sample.jpg",
        )


if __name__ == "__main__":
    unittest.main()
