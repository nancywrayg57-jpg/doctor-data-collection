from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import governance_cleanup_issue_53 as governance  # noqa: E402


class Issue53GovernanceCleanupTests(unittest.TestCase):
    def test_manifest_hash_excludes_index_from_marker_filtered_profiles(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            hospital = governance.TARGET_HOSPITALS[0]
            hospital_dir = root / hospital
            hospital_dir.mkdir(parents=True)
            (hospital_dir / "_索引.md").write_text("# 初始索引\n", encoding="utf-8")
            (hospital_dir / "人工画像.md").write_text("人工精修内容\n", encoding="utf-8")
            (hospital_dir / "自动画像.md").write_text(
                f"{governance.profiles.AUTO_MARKER}\n自动内容\n",
                encoding="utf-8",
            )

            all_before = governance.manifest_hash(root, [hospital])
            manual_before = governance.manifest_hash(root, [hospital], marker_filter=False)
            auto_before = governance.manifest_hash(root, [hospital], marker_filter=True)
            (hospital_dir / "_索引.md").write_text("# 重建后的索引\n", encoding="utf-8")

            self.assertEqual(all_before["files"], 3)
            self.assertEqual(manual_before["files"], 1)
            self.assertEqual(auto_before["files"], 1)
            self.assertNotEqual(all_before, governance.manifest_hash(root, [hospital]))
            self.assertEqual(
                manual_before,
                governance.manifest_hash(root, [hospital], marker_filter=False),
            )

    def test_navigation_cleanup_changes_only_allowed_fields(self) -> None:
        row = {
            "序号": 1,
            "医院": "中山大学肿瘤防治中心",
            "姓名": "丘惠娟",
            "亮眼经历线索": (
                "副主任医师 临床专家 面包屑 首页 / 临床科室 / 内科系列 / 中医科 / "
                "临床专家 丘惠娟 职称：副主任医师，主持科研项目。"
            ),
            "异常提示": "原提示",
            "来源链接": "https://example.com/doctor/1",
            "复核状态": "待人工复核",
        }
        before = dict(row)

        changes = governance.apply_navigation_cleanup([row])

        self.assertEqual(len(changes), 1)
        self.assertNotIn("面包屑", row["亮眼经历线索"])
        self.assertNotIn("首页 /", row["亮眼经历线索"])
        self.assertEqual(row["异常提示"], "原提示；亮眼经历含导航文本，已清洗")
        changed_columns = {key for key in row if row.get(key) != before.get(key)}
        self.assertEqual(changed_columns, {"亮眼经历线索", "异常提示"})

    def test_profile_backfill_only_fills_blank_matching_source(self) -> None:
        rows = [
            {
                "医院": "中山大学肿瘤防治中心",
                "姓名": "应回填",
                "来源链接": "https://example.com/a",
                "已建画像": "",
            },
            {
                "医院": "中山大学肿瘤防治中心",
                "姓名": "保留否",
                "来源链接": "https://example.com/a",
                "已建画像": "否",
            },
            {
                "医院": "中山大学肿瘤防治中心",
                "姓名": "无画像",
                "来源链接": "https://example.com/b",
                "已建画像": "",
            },
        ]
        mocked_sources = {
            hospital: ({"https://example.com/a"} if hospital == "中山大学肿瘤防治中心" else set())
            for hospital in governance.TARGET_HOSPITALS
        }

        with patch.object(governance, "profile_sources_by_hospital", return_value=mocked_sources):
            changes, _existing, missing = governance.apply_profile_backfill(rows)

        self.assertEqual(len(changes), 1)
        self.assertEqual(rows[0]["已建画像"], "是")
        self.assertEqual(rows[1]["已建画像"], "否")
        self.assertEqual(rows[2]["已建画像"], "")
        self.assertEqual(missing["中山大学肿瘤防治中心"], 1)

    def test_same_name_report_groups_whitespace_variants_without_writing_rows(self) -> None:
        rows = [
            {
                "姓名": "张 文",
                "医院": "测试医院",
                "科室_分类页": "生殖医学科",
                "职称身份原文": "主任医师",
                "来源链接": "https://example.com/a",
                "异常提示": "同名待甄别",
            },
            {
                "姓名": "张文",
                "医院": "测试医院",
                "科室_分类页": "男科",
                "职称身份原文": "主治医师",
                "来源链接": "https://example.com/b",
                "异常提示": "同名待甄别",
            },
        ]
        before = [dict(row) for row in rows]

        report, summary = governance.build_same_name_report(rows)

        self.assertEqual(summary["flagged_rows"], 2)
        self.assertEqual(summary["groups"], 1)
        self.assertIn("疑似不同人", report)
        self.assertEqual(rows, before)


if __name__ == "__main__":
    unittest.main()
