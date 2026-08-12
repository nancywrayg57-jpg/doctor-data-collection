from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

from generate_obsidian_profiles import (  # noqa: E402
    build_profile,
    extract_profile_fact_sections,
    generate_missing_profiles,
    select_hospital_rows,
)


class ProfileFactSectionTests(unittest.TestCase):
    DETAIL = (
        "毕业于南方医科大学，曾赴北京大学第一医院进修学习。"
        "主持省级科研基金项目2项，获得授权专利1项。"
        "以第一作者发表SCI论文5篇，参编专业著作1部。"
    )

    def test_official_profile_facts_are_routed_to_corresponding_sections(self) -> None:
        sections = extract_profile_fact_sections(self.DETAIL)

        self.assertEqual(len(sections["教育与进修经历"]), 1)
        self.assertIn("进修学习", sections["教育与进修经历"][0])
        self.assertEqual(len(sections["科研项目与成果"]), 1)
        self.assertIn("科研基金", sections["科研项目与成果"][0])
        self.assertEqual(len(sections["论文与学术产出"]), 1)
        self.assertIn("SCI论文", sections["论文与学术产出"][0])

    def test_generated_profile_renders_only_evidence_backed_optional_sections(self) -> None:
        profile = build_profile(
            {
                "医院": "南方医科大学皮肤病医院",
                "姓名": "测试医生",
                "科室_分类页": "皮肤内科",
                "职称身份原文": "主任医师",
                "擅长诊疗方向摘录": "皮肤病规范诊疗",
                "详情正文摘录": self.DETAIL,
                "亮眼经历线索": "主持省级科研基金项目2项，发表SCI论文5篇。",
                "来源链接": "https://www.gdskin.com/ShowNews.ASPX?ID=5000",
                "采集日期": "2026-08-11",
                "复核状态": "待人工复核",
            },
            "2026-08-11",
        )

        self.assertIn("## 教育与进修经历", profile)
        self.assertIn("## 科研项目与成果", profile)
        self.assertIn("## 论文与学术产出", profile)
        self.assertIn("毕业于南方医科大学", profile)
        self.assertIn("主持省级科研基金项目2项", profile)
        self.assertIn("发表SCI论文5篇", profile)

    def test_hospital_filter_limits_single_issue_generation(self) -> None:
        rows = [
            {"医院": "南方医科大学皮肤病医院", "姓名": "测试医生"},
            {"医院": "其他医院", "姓名": "其他医生"},
        ]

        selected = select_hospital_rows(rows, ["南方医科大学皮肤病医院"])

        self.assertEqual(selected, [rows[0]])

    def test_generated_profile_preserves_current_anomaly_warning(self) -> None:
        profile = build_profile(
            {
                "医院": "广州医科大学附属口腔医院",
                "姓名": "方颖",
                "科室_分类页": "越秀院区儿童口腔科",
                "职称身份原文": "教授",
                "来源链接": "https://www.gykqyy.com/list.html?category=55&id=307",
                "采集日期": "2026-08-13",
                "复核状态": "待人工复核",
                "异常提示": "同名待甄别",
            },
            "2026-08-13",
        )

        self.assertIn("- 异常提示：同名待甄别", profile)

    def test_refresh_auto_generated_does_not_overwrite_manual_profile(self) -> None:
        rows = [
            {
                "医院": "测试医院",
                "姓名": "自动医生",
                "科室_分类页": "测试科",
                "来源链接": "https://example.com/auto",
                "异常提示": "同名待甄别",
            },
            {
                "医院": "测试医院",
                "姓名": "人工医生",
                "科室_分类页": "测试科",
                "来源链接": "https://example.com/manual",
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            hospital_dir = Path(directory) / "测试医院"
            hospital_dir.mkdir()
            auto_path = hospital_dir / "自动医生.md"
            auto_path.write_text(
                "<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->\n"
                "来源链接: https://example.com/auto\n",
                encoding="utf-8",
            )
            manual_path = hospital_dir / "人工医生.md"
            manual_path.write_text("人工内容\n来源链接: https://example.com/manual\n", encoding="utf-8")

            result = generate_missing_profiles(
                rows=rows,
                output_root=Path(directory),
                skip_hospitals=set(),
                report_path=Path(directory) / "report.md",
                refresh_auto_generated=True,
            )

            self.assertEqual(result["refreshed_auto_generated_profiles"], 1)
            self.assertIn("异常提示：同名待甄别", auto_path.read_text(encoding="utf-8"))
            self.assertEqual(manual_path.read_text(encoding="utf-8"), "人工内容\n来源链接: https://example.com/manual\n")

    def test_unlabeled_specialty_does_not_fall_back_to_list_title_or_biography(self) -> None:
        profile = build_profile(
            {
                "医院": "南方医科大学皮肤病医院",
                "姓名": "测试医生",
                "科室_分类页": "外阴皮肤病/性病科",
                "职称身份原文": "主治医师",
                "擅长诊疗方向摘录": "",
                "列表简介": "测试医生 主治医师",
                "详情正文摘录": "毕业于南方医科大学，主持科研项目1项。",
                "来源链接": "https://www.gdskin.com/ShowNews.ASPX?ID=5001",
                "采集日期": "2026-08-11",
                "复核状态": "待人工复核",
            },
            "2026-08-11",
        )

        specialty_block = profile.split("## 简介/擅长", 1)[1].split("## 教育与进修经历", 1)[0]
        self.assertEqual(specialty_block.strip(), "")
        self.assertFalse(any(line != line.rstrip() for line in profile.splitlines()))


if __name__ == "__main__":
    unittest.main()
