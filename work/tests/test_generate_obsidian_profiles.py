from __future__ import annotations

import sys
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

from generate_obsidian_profiles import (  # noqa: E402
    build_profile,
    extract_profile_fact_sections,
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


if __name__ == "__main__":
    unittest.main()
