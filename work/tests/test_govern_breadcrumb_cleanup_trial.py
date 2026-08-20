from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import govern_breadcrumb_cleanup_trial as trial  # noqa: E402


class FakeSession:
    def __init__(self, html_by_url: dict[str, str]) -> None:
        self.html_by_url = html_by_url
        self.trace: list[dict[str, object]] = []

    def get(self, url: str, timeout: int) -> SimpleNamespace:
        del timeout
        html = self.html_by_url[url].encode("utf-8")
        return SimpleNamespace(
            status_code=200,
            url=url,
            headers={"Content-Type": "text/html; charset=utf-8"},
            content=html,
        )


class BreadcrumbCleanupTrialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = trial.load_current_layers()
        cls.manifest = trial.affected_master_manifest(cls.rows)
        cls.profile_impact, cls.atypical = trial.profile_impact_inventory(cls.manifest)

    def test_sysucc_start_position_removal(self) -> None:
        original = (
            "临床专家 面包屑 首页 / 临床科室 / 放疗系列 / 放疗科 / "
            "临床专家 张三 职称：主任医师 正文"
        )
        result = trial.strip_navigation(original, trial.SYSUCC)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual("职称：主任医师 正文", result["remaining"])
        self.assertEqual("START", result["segment_position"])
        self.assertEqual("SYSUCC_CLINICAL_EXPERT", result["match_type"])

    def test_sysucc_middle_position_preserves_prefix_suffix_and_quote(self) -> None:
        original = (
            "论文列表'临床专家 面包屑 首页 / 临床科室 / 外科系列 / 胸科 / "
            "临床专家 李四 职称：副主任医师"
        )
        result = trial.strip_navigation(original, trial.SYSUCC)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual("论文列表'职称：副主任医师", result["remaining"])
        self.assertEqual("MIDDLE", result["segment_position"])
        self.assertEqual(
            "ISOLATED_QUOTE_PRESERVED_PENDING_OWNER",
            result["quote_boundary_status"],
        )

    def test_liuhui_site_variant_is_a_valid_terminal_anchor(self) -> None:
        original = (
            "临床专家 面包屑 首页 / 临床科室 / 放疗系列 / 放疗科 / "
            "临床专家 刘慧(小) 职务：放疗科副主任"
        )
        result = trial.strip_navigation(original, trial.SYSUCC)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual("刘慧(小)", result["site_title"])
        self.assertEqual("职务：放疗科副主任", result["remaining"])

    def test_zssy_start_position_removes_only_dom_breadcrumb(self) -> None:
        original = "导航痕迹 首页 / 专家介绍 / 王五 王五 科室 呼吸科"
        result = trial.strip_navigation(original, trial.ZSSY)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual("王五 科室 呼吸科", result["remaining"])
        self.assertEqual("ZSSY_EXPERT", result["match_type"])

    def test_zssy_department_row_is_supported(self) -> None:
        original = "导航痕迹 首页 / 变态反应（过敏）学科 变态反应（过敏）学科 正文"
        result = trial.strip_navigation(original, trial.ZSSY)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual("变态反应（过敏）学科 正文", result["remaining"])
        self.assertEqual("ZSSY_DEPARTMENT", result["match_type"])

    def test_unrelated_marker_or_hospital_is_rejected(self) -> None:
        self.assertIsNone(trial.strip_navigation("普通正文 面包屑不是导航", trial.SYSUCC))
        self.assertIsNone(trial.strip_navigation("导航痕迹 首页 / A A 正文", "其他医院"))

    def test_real_master_scope_is_exact(self) -> None:
        self.assertEqual(trial.EXPECTED_ROWS, len(self.manifest))
        self.assertEqual(
            trial.EXPECTED_BY_HOSPITAL,
            dict(trial.Counter(item["hospital"] for item in self.manifest)),
        )
        self.assertTrue(
            all(
                int(item["original_length"])
                == int(item["removed_length"]) + int(item["remaining_length"])
                for item in self.manifest
            )
        )

    def test_real_profile_scope_and_eight_atypical_cases_are_exact(self) -> None:
        self.assertEqual(trial.EXPECTED_PROFILES, len(self.profile_impact))
        self.assertEqual(
            trial.EXPECTED_PROFILES_BY_HOSPITAL,
            dict(trial.Counter(item["hospital"] for item in self.profile_impact)),
        )
        self.assertEqual(trial.EXPECTED_ATYPICAL_PROFILES, len(self.atypical))
        self.assertEqual(
            {"医学教育", "卢雅立", "周冠群", "宋远斌", "温丽丽", "罗敏", "谢丹", "郑利民"},
            {item["master_name"] for item in self.atypical},
        )

    def test_repository_digest_normalizes_text_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "lf.md"
            crlf = root / "crlf.md"
            binary = root / "binary.bin"
            lf.write_bytes(b"a\nb\n")
            crlf.write_bytes(b"a\r\nb\r\n")
            binary.write_bytes(b"a\r\nb\r\n")
            self.assertEqual(
                trial.repository_digest_bytes(lf),
                trial.repository_digest_bytes(crlf),
            )
            self.assertEqual(b"a\r\nb\r\n", trial.repository_digest_bytes(binary))

    def test_manifest_schemas_are_stable(self) -> None:
        self.assertEqual(19, len(trial.MANIFEST_FIELDS))
        self.assertEqual("row_number", trial.MANIFEST_FIELDS[0])
        self.assertEqual("remaining_sha256", trial.MANIFEST_FIELDS[-1])
        self.assertEqual("profile_path", trial.PROFILE_FIELDS[1])
        self.assertEqual("agreement", trial.DOM_FIELDS[9])

    def test_pure_dry_run_calculation_keeps_formal_snapshot_unchanged(self) -> None:
        before = trial.protected_snapshot()
        trial.affected_master_manifest(self.rows)
        trial.profile_impact_inventory(self.manifest)
        self.assertEqual(before, trial.protected_snapshot())

    def test_online_dom_comparison_is_mockable_and_uses_official_samples(self) -> None:
        by_source = {item["source_link"]: item for item in self.manifest}
        html_by_url: dict[str, str] = {}
        for hospital, _name, source_link in trial.DOM_SAMPLE_PLAN:
            item = by_source[source_link]
            if hospital == trial.SYSUCC:
                removed = item["removed_segment"].strip()
                marker = removed.index("面包屑")
                dom = removed[marker : removed.rfind(item["site_title"])].strip()
                page_title = item["site_title"]
            else:
                dom = item["removed_segment"].strip()
                page_title = item["site_title"]
            html_by_url[source_link] = (
                f"<html><head><title>{page_title} | 官方</title></head>"
                f"<body><nav class='breadcrumb'>{dom}</nav></body></html>"
            )
        evidence, trace = trial.collect_dom_evidence(self.manifest, FakeSession(html_by_url))
        self.assertEqual([], trace)
        self.assertEqual(10, len(evidence))
        self.assertTrue(all(item["agreement"] == "YES" for item in evidence))


if __name__ == "__main__":
    unittest.main()
