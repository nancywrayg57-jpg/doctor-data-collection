from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

from collect_official_doctors_batch import (  # noqa: E402
    GDGH_EXPECTED_DEPARTMENT_COUNT,
    GDGH_EXPECTED_GROUP_COUNT,
    GDGH_EXPECTED_NURSING_COUNT,
    GDGH_EXPECTED_RELATION_COUNT,
    gdgh_detail_id,
    gdgh_photo_extension,
    gdgh_photo_url,
    merge_gdgh_identity_rows,
    select_gdgh_trial_doctors,
    validate_gdgh_trial,
)


class GdghPhotoTrialTests(unittest.TestCase):
    def test_strict_urls_and_magic_bytes(self) -> None:
        detail = (
            "https://www.gdghospital.org.cn/Expertlistt/"
            "info_itemid_123_subjectid_45.html"
        )
        photo = "https://www.gdghospital.org.cn/uploadfiles/doctor/123.jpg"

        self.assertEqual(gdgh_detail_id(detail, "45"), "123")
        self.assertEqual(gdgh_photo_url(photo, photo), photo)
        self.assertEqual(gdgh_photo_extension(b"\xff\xd8\xffsample", "image/jpeg"), "jpg")
        self.assertEqual(gdgh_photo_extension(b"<html>", "text/html"), "")

    def test_same_name_anomaly_is_never_tagged_or_promoted(self) -> None:
        rows = [
            {
                "姓名": "测试同名",
                "科室_分类页": "心内科",
                "科室_列表卡片": "心内科",
                "职称身份原文": "主任医师",
                "擅长诊疗方向摘录": "心律失常",
                "亮眼经历线索": "",
                "详情正文摘录": "长期从事心律失常诊疗。",
                "来源链接": "https://www.gdghospital.org.cn/Expertlistt/info_itemid_1_subjectid_1.html",
                "异常提示": "",
                "重点优先级": "高",
                "重点关注范围": "慢性病",
                "重点疾病标签": "高血压",
                "_gdgh_item_id": "1",
            },
            {
                "姓名": "测试同名",
                "科室_分类页": "骨科",
                "科室_列表卡片": "骨科",
                "职称身份原文": "副主任医师",
                "擅长诊疗方向摘录": "脊柱骨折",
                "亮眼经历线索": "",
                "详情正文摘录": "长期从事脊柱骨折诊疗。",
                "来源链接": "https://www.gdghospital.org.cn/Expertlistt/info_itemid_2_subjectid_2.html",
                "异常提示": "",
                "重点优先级": "高",
                "重点关注范围": "术后恢复/康复",
                "重点疾病标签": "脊柱骨折",
                "_gdgh_item_id": "2",
            },
        ]

        merged, _ = merge_gdgh_identity_rows(rows)

        self.assertEqual(len(merged), 2)
        for row in merged:
            self.assertIn("同名待甄别", row["异常提示"])
            self.assertEqual(row["重点优先级"], "普通")
            self.assertEqual(row["重点关注范围"], "")
            self.assertEqual(row["重点疾病标签"], "")

    def test_trial_selection_keeps_department_spread_without_duplicate_names(self) -> None:
        doctors = [
            {"id": "1", "name": "同名医生", "departments": ["科室甲"]},
            {"id": "2", "name": "同名医生", "departments": ["科室乙"]},
            {"id": "3", "name": "医生乙", "departments": ["科室乙"]},
            {"id": "4", "name": "医生丙", "departments": ["科室丙"]},
        ]

        selected = select_gdgh_trial_doctors(doctors, 3)

        self.assertEqual([item["id"] for item in selected], ["1", "3", "4"])
        self.assertEqual(len({item["name"] for item in selected}), 3)

    def test_trial_validator_accepts_ten_auditable_photo_samples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = b"\xff\xd8\xff" + b"official-photo-bytes"
            digest = hashlib.sha256(content).hexdigest()
            rows = []
            photos = []
            names = ["测试甲", "测试乙", "测试丙", "测试丁", "测试戊", "测试己", "测试庚", "测试辛", "测试壬", "测试癸"]
            for index, name in enumerate(names):
                filename = f"{name}-科室{index % 3}-主任医师-广东省人民医院.jpg"
                disk_path = root / filename
                disk_path.write_bytes(content)
                source = (
                    "https://www.gdghospital.org.cn/Expertlistt/"
                    f"info_itemid_{100 + index}_subjectid_{200 + index}.html"
                )
                photo_url = (
                    "https://www.gdghospital.org.cn/uploadfiles/doctor/"
                    f"{100 + index}.jpg"
                )
                relative = f"01_试点医院/广东省人民医院/照片/{filename}"
                rows.append(
                    {
                        "姓名": name,
                        "科室_分类页": f"科室{index % 3}",
                        "科室_列表卡片": f"科室{index % 3}",
                        "职称身份原文": "主任医师",
                        "重点优先级": "普通",
                        "重点关注范围": "",
                        "重点疾病标签": "",
                        "擅长诊疗方向摘录": "",
                        "亮眼经历线索": "",
                        "列表简介": "",
                        "详情正文摘录": "",
                        "来源链接": source,
                        "照片链接": photo_url,
                        "照片文件": relative,
                        "异常提示": "",
                    }
                )
                photos.append(
                    {
                        "name": name,
                        "source_link": source,
                        "photo_url": photo_url,
                        "photo_file": relative,
                        "filename": filename,
                        "bytes": len(content),
                        "sha256": digest,
                        "disk_path": str(disk_path),
                    }
                )

            eligible = GDGH_EXPECTED_RELATION_COUNT - GDGH_EXPECTED_NURSING_COUNT
            payload = {
                "meta": {
                    "census_group_count": GDGH_EXPECTED_GROUP_COUNT,
                    "census_department_count": GDGH_EXPECTED_DEPARTMENT_COUNT,
                    "candidate_membership_count": GDGH_EXPECTED_RELATION_COUNT,
                    "census_unique_detail_count": GDGH_EXPECTED_RELATION_COUNT,
                    "excluded_non_doctor_count": GDGH_EXPECTED_NURSING_COUNT,
                    "eligible_candidate_count": eligible,
                    "photo_census_available_count": eligible,
                    "independent_entity_count": 0,
                    "category_error_count": 0,
                    "detail_error_count": 0,
                    "photo_error_count": 0,
                    "schedule_field_ingested_count": 0,
                    "private_use_character_count": 0,
                    "sample_entry_coverage_count": 3,
                    "photo_sample_count": 10,
                    "photo_policy_status": "WAITING_OWNER_SIZE_POLICY",
                    "photo_average_bytes": len(content),
                    "photo_estimated_full_count": eligible,
                    "photo_estimated_full_bytes": len(content) * eligible,
                },
                "rows": rows,
                "photo_samples": photos,
                "affiliate_reconnaissance": [
                    {"name": "广东省心血管病研究所", "relation": "所属研究所"},
                    {"name": "广东省老年医学研究所", "relation": "一套人马、两块牌子"},
                    {"name": "惠福分院", "relation": "重要组成部分"},
                    {"name": "广东省肺癌研究所", "relation": "所属研究所"},
                ],
            }

            validate_gdgh_trial(payload, expected_rows=10)


if __name__ == "__main__":
    unittest.main()
