from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gdskin_photo_backfill_full as target


class GdskinPhotoBackfillFullTests(unittest.TestCase):
    def setUp(self) -> None:
        self.framework_state = dict(vars(target.framework))
        self.trial_state = dict(vars(target.trial))
        self.trial_framework_state = dict(vars(target.trial.framework))
        self.base_state = dict(vars(target.trial.base))
        target.configure_framework()

    def tearDown(self) -> None:
        target.TITLE_VARIANCE_EVIDENCE.clear()
        target.REFERENCE_EVIDENCE_BY_SOURCE.clear()
        target.FULL_REQUEST_TRACE.clear()
        for module, state in (
            (target.framework, self.framework_state),
            (target.trial, self.trial_state),
            (target.trial.framework, self.trial_framework_state),
            (target.trial.base, self.base_state),
        ):
            for name in set(vars(module)) - set(state):
                delattr(module, name)
            for name, value in state.items():
                setattr(module, name, value)

    def test_scope_and_authorization_are_issue_83_specific(self) -> None:
        self.assertEqual(target.ISSUE_NUMBER, 83)
        self.assertEqual(target.EXPECTED_SCOPE_COUNT, 77)
        self.assertEqual(target.EXPECTED_TRIAL_REUSE_COUNT, 10)
        self.assertEqual(target.EXPECTED_FRESH_COUNT, 67)
        self.assertEqual(target.PULL_REQUEST_NUMBER, 84)
        self.assertIn("FULL_APPEND_AND_OBSIDIAN", target.FULL_AUTHORIZATION)
        self.assertIn("serial-min-2s", target.REQUEST_MODE)

    def test_root_and_artifact_paths_are_repository_relative(self) -> None:
        self.assertEqual(target.ROOT, Path(target.__file__).resolve().parents[1])
        source = Path(target.__file__).read_text(encoding="utf-8")
        self.assertNotIn("ROOT = Path(r\"D:\\workspace", source)
        for path in (
            target.FULL_JSON_PATH,
            target.FULL_CSV_PATH,
            target.FULL_REPORT_PATH,
            target.FULL_AUDIT_SHEET_PATH,
            target.FULL_VISUAL_DIR,
        ):
            self.assertTrue(path.is_relative_to(target.ROOT))

    def test_nbsp_transport_url_only_encodes_for_request(self) -> None:
        unicode_url = "https://www.gdskin.com/uploadimg/孟凡琪\u00a0 \u00a0.jpg"
        encoded = target.trial.transport_url(unicode_url)
        self.assertIn("%C2%A0%20%C2%A0.jpg", encoded)
        self.assertIn("\u00a0 \u00a0", unicode_url)

    def test_analyzer_accepts_unique_uploadimg_and_records_nbsp(self) -> None:
        html = """
        <html><head><title>龚洋洋 医师__广东省皮肤病医院官方网站</title></head>
        <body><img src="/WebResource.axd?x=1"><img src="../system_dntb/../uploadimg/龚洋洋&nbsp;.jpg"></body></html>
        """
        source = "https://www.gdskin.com/ShowNews.ASPX?ID=5594"
        result = target.analyze_full_doctor_media(html, source, "龚洋洋")
        self.assertEqual(result.state, "")
        self.assertEqual(result.page_title, "医师")
        self.assertEqual(result.photo_reference_count, 1)
        self.assertIn("\u00a0.jpg", result.photo_url)
        evidence = target.REFERENCE_EVIDENCE_BY_SOURCE[source]
        self.assertIn("\u00a0", evidence["page_raw_reference"])
        self.assertIn("%C2%A0.jpg", evidence["transport_url"])

    def test_analyzer_allows_title_prefix_while_name_remains_exact(self) -> None:
        html = """
        <html><head><title>首席专家 顾有守 主任医师__广东省皮肤病医院官方网站</title></head>
        <body><img src="../uploadimg/广东省皮肤病医院院长.jpg"></body></html>
        """
        result = target.analyze_full_doctor_media(
            html, "https://www.gdskin.com/ShowNews.ASPX?ID=3829", "顾有守"
        )
        self.assertEqual(result.page_name, "顾有守")
        self.assertEqual(result.page_title, "首席专家 主任医师")

    def test_analyzer_classifies_no_photo_container(self) -> None:
        html = """
        <html><head><title>吴芳芳 医师__广东省皮肤病医院官方网站</title></head>
        <body><img src="/WebResource.axd?x=1"><img src="/images/beian.png"></body></html>
        """
        result = target.analyze_full_doctor_media(
            html, "https://www.gdskin.com/ShowNews.ASPX?ID=6197", "吴芳芳"
        )
        self.assertEqual(result.state, "无照片容器")
        self.assertEqual(result.photo_reference_count, 0)
        self.assertEqual(result.outside_image_reference_count, 2)

    def test_analyzer_classifies_explicit_chinese_placeholder(self) -> None:
        html = """
        <html><head><title>文海泉 主任医师__广东省皮肤病医院官方网站</title></head>
        <body><img src="../uploadimg/占位.png"></body></html>
        """
        result = target.analyze_full_doctor_media(
            html, "https://www.gdskin.com/ShowNews.ASPX?ID=5566", "文海泉"
        )
        self.assertEqual(result.state, "占位图")
        self.assertIn("explicit_chinese_placeholder_filename", result.detection_feature)

    def test_analyzer_rejects_name_mismatch(self) -> None:
        html = """
        <html><head><title>陈永锋 主任医师__广东省皮肤病医院官方网站</title></head>
        <body><img src="../uploadimg/陈永锋.jpg"></body></html>
        """
        with self.assertRaisesRegex(RuntimeError, "姓名与底表不一致"):
            target.analyze_full_doctor_media(
                html, "https://www.gdskin.com/ShowNews.ASPX?ID=3847", "杨斌"
            )

    def test_title_variance_is_recorded_without_mutating_master(self) -> None:
        row = {
            "姓名": "杜美毅",
            "来源链接": "https://www.gdskin.com/ShowNews.ASPX?ID=5596",
            "职称身份原文": "住院医师",
        }
        analysis = target.MediaAnalysis(
            page_name="杜美毅",
            page_title="医师",
            state="",
            photo_url="https://www.gdskin.com/uploadimg/杜美毅.jpg",
            opaque_query="",
            template_signature=target.TEMPLATE_SIGNATURE,
            photo_reference_count=1,
            single_con_image_count=0,
            outside_image_reference_count=0,
            excluded_resource_examples=(),
            container_html_snippet="<img>",
            detection_feature="strict",
        )
        target.validate_full_page_title(row, analysis)
        evidence = target.TITLE_VARIANCE_EVIDENCE[row["来源链接"]]
        self.assertEqual(evidence["master_title_preserved"], "住院医师")
        self.assertEqual(evidence["page_title_observed"], "医师")

    def test_trial_payload_and_manifest_are_full_ready(self) -> None:
        payload = json.loads(target.trial.TRIAL_JSON_PATH.read_text(encoding="utf-8"))
        target.validate_trial_payload_for_full(payload, require_visual_pass=True)
        target.validate_trial_manifest(payload)
        self.assertEqual(len(payload["photo_samples"]), 10)

    def test_runtime_injection_preserves_raw_and_transport_failure_evidence(self) -> None:
        source = "https://www.gdskin.com/ShowNews.ASPX?ID=5594"
        target.REFERENCE_EVIDENCE_BY_SOURCE[source] = {
            "page_raw_reference": "../uploadimg/龚洋洋\u00a0.jpg",
            "normalized_photo_url": "https://www.gdskin.com/uploadimg/龚洋洋\u00a0.jpg",
            "transport_url": "https://www.gdskin.com/uploadimg/%E9%BE%9A%E6%B4%8B%E6%B4%8B%C2%A0.jpg",
            "container_html_snippet": "<img src='../uploadimg/龚洋洋&nbsp;.jpg'>",
        }
        target.FULL_REQUEST_TRACE.extend(
            [
                {
                    "sequence": 1,
                    "requested_url": source,
                    "transport_url": source,
                    "interval_seconds_from_previous": None,
                    "observed_utc": "2026-08-19T00:00:00Z",
                },
                {
                    "sequence": 2,
                    "requested_url": source,
                    "transport_url": source,
                    "interval_seconds_from_previous": 2.0,
                    "observed_utc": "2026-08-19T00:00:02Z",
                },
            ]
        )
        payload = {
            "meta": {},
            "failures": [
                {
                    "name": "龚洋洋",
                    "source_link": source,
                    "state": "照片资源不可达",
                    "evidence": {},
                    "attempts": [
                        {
                            "final_url": "https://www.gdskin.com/uploadimg/%E9%BE%9A%E6%B4%8B%E6%B4%8B%C2%A0.jpg"
                        }
                    ],
                }
            ],
            "reconciliation": [{"来源链接": source, "错误证据": ""}],
        }
        target.inject_runtime_evidence(payload)
        evidence = payload["failures"][0]["evidence"]
        self.assertIn("\u00a0", evidence["page_raw_reference"])
        self.assertIn("%C2%A0.jpg", evidence["transport_url"])
        self.assertEqual(
            payload["reconciliation"][0]["错误证据"],
            payload["failures"][0]["error"],
        )
        target.validate_gdskin_evidence(payload)

    def test_immutable_snapshot_uses_relative_protected_paths(self) -> None:
        snapshot = target.immutable_snapshot()
        self.assertEqual(len(snapshot["files"]), 6)
        self.assertTrue(
            all(not Path(path).is_absolute() for path in snapshot["files"])
        )
        self.assertEqual(snapshot["trial_photo_tree"]["file_count"], 10)

    def test_framework_is_configured_for_transactional_full(self) -> None:
        self.assertIs(target.framework.analyze_full_doctor_media, target.analyze_full_doctor_media)
        self.assertIs(target.framework.validate_full_payload, target.validate_full_payload)
        self.assertIs(target.framework.immutable_snapshot, target.immutable_snapshot)
        self.assertEqual(target.framework.EXPECTED_SCOPE_COUNT, 77)
        self.assertEqual(target.framework.PULL_REQUEST_NUMBER, 84)
        self.assertFalse(target.framework.HOME_IS_GATE)


if __name__ == "__main__":
    unittest.main()
