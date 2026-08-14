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
    GDMCH_EXPECTED_NON_DOCTOR_COUNT,
    GDMCH_EXPECTED_PAGE_COUNT,
    GDMCH_EXPECTED_DEFAULT_PHOTO_COUNT,
    GDMCH_EXPECTED_PHOTO_AVAILABLE_COUNT,
    GDMCH_EXPECTED_RELATION_COUNT,
    discover_gdmch_page_count,
    gdmch_detail_id,
    gdmch_covered_department_names,
    gdmch_list_page_url,
    gdmch_non_doctor_card,
    gdmch_photo_dimensions,
    gdmch_photo_url,
    parse_gdmch_detail,
    validate_gdmch_full_append,
    validate_gdmch_trial,
)


def png_bytes(width: int, height: int) -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\rIHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x02\x00\x00\x00"
    )


class GdmchPhotoTrialTests(unittest.TestCase):
    def test_strict_detail_and_photo_urls(self) -> None:
        detail = "https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32798.html"
        photo = "https://wx.e3861.com/sfyAdmin/Images/Doctor/32798.png"

        self.assertEqual(gdmch_detail_id(detail), "32798")
        self.assertEqual(gdmch_photo_url(photo, photo), photo)
        self.assertEqual(gdmch_detail_id(f"{detail}?from=search"), "")
        self.assertEqual(
            gdmch_photo_url("https://www.e3861.com/uploads/patient.png", detail),
            "",
        )

    def test_pagination_uses_blank_search_fields_and_server_page(self) -> None:
        entry = "https://www.e3861.com/keshizhuanjia/zhuanjiajieshao"
        page_url = gdmch_list_page_url(entry, 111)
        html = f'<div class="paged"><a href="{page_url}">111</a></div>'

        self.assertIn("searchDoctor=&searchDepartment=&page=111", page_url)
        self.assertEqual(discover_gdmch_page_count(html, entry), 111)

    def test_non_doctor_accounts_are_excluded_but_doctor_is_kept(self) -> None:
        for value in (
            "续费专用号",
            "test123",
            "系统管理员-正式库",
            "急诊号",
            "政府免费筛查就诊号",
        ):
            self.assertTrue(gdmch_non_doctor_card(value, ""), value)
        self.assertFalse(gdmch_non_doctor_card("何伟健", "主任医师"))

    def test_detail_parser_keeps_department_and_excludes_schedule_text(self) -> None:
        source = "https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32798.html"
        photo = "https://wx.e3861.com/sfyAdmin/Images/Doctor/32798.png"
        html = f"""
        <div class="expert-detail">
          <div class="detail-head">
            <div class="img-box"><img src="{photo}"></div>
            <div class="info"><span>姓名：</span><span>何伟健</span></div>
            <div class="info"><span>职称：</span><span>主任医师</span></div>
            <div class="info"><span>出诊安排：</span><span>周一上午（心理科（番禺））</span></div>
          </div>
          <div class="content-box"><div class="content">
            <p>专业专长：心理咨询与心理治疗</p>
            <p>出诊时间：</p>
            <p>周一上午</p>
          </div></div>
        </div>
        """
        parsed = parse_gdmch_detail(
            html,
            {
                "name": "何伟健",
                "list_title": "主任医师",
                "source_link": source,
                "photo_url": photo,
            },
        )

        self.assertEqual(parsed["departments"], ["心理科"])
        self.assertEqual(parsed["campuses"], ["番禺院区"])
        self.assertEqual(parsed["specialty"], "心理咨询与心理治疗")
        self.assertNotIn("周一", parsed["profile_text"])
        self.assertNotIn("上午", parsed["profile_text"])

    def test_png_dimensions_are_parsed_without_reencoding(self) -> None:
        self.assertEqual(gdmch_photo_dimensions(png_bytes(640, 480), "png"), (640, 480))

    def test_department_coverage_does_not_count_campus_suffixes(self) -> None:
        rows = [
            {"科室_分类页": "乳腺科（番禺院区、越秀院区）"},
            {"科室_分类页": "小儿骨科、小儿外科（番禺院区、天河院区）"},
        ]

        self.assertEqual(
            gdmch_covered_department_names(rows),
            ["乳腺科", "小儿外科", "小儿骨科"],
        )

    def test_trial_validator_accepts_exact_census_and_ten_photos(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = png_bytes(640, 480)
            digest = hashlib.sha256(content).hexdigest()
            eligible = GDMCH_EXPECTED_RELATION_COUNT - GDMCH_EXPECTED_NON_DOCTOR_COUNT
            names = ["赵甲", "钱乙", "孙丙", "李丁", "周戊", "吴己", "郑庚", "王辛", "冯壬", "陈癸"]
            rows = []
            photos = []
            details = []
            for index, name in enumerate(names, start=1):
                detail_id = str(32000 + index)
                department = ("心理科", "妇女保健科", "产科")[index % 3]
                filename = f"{name}-{department}-主任医师-广东省妇幼保健院.png"
                disk_path = root / filename
                disk_path.write_bytes(content)
                source = (
                    "https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/"
                    f"{detail_id}.html"
                )
                photo_url = (
                    "https://wx.e3861.com/sfyAdmin/Images/Doctor/"
                    f"{detail_id}.png"
                )
                relative = f"01_试点医院/广东省妇幼保健院/照片/{filename}"
                rows.append(
                    {
                        "姓名": name,
                        "科室_分类页": department,
                        "科室_列表卡片": "",
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
                        "width": 640,
                        "height": 480,
                        "disk_path": str(disk_path),
                    }
                )
                details.append(
                    {
                        "detail_id": detail_id,
                        "name": name,
                        "departments": [department],
                        "campuses": ["番禺院区"],
                        "source_link": source,
                        "resolution": "详情已读取",
                    }
                )

            excluded = [
                {
                    "detail_id": str(40000 + index),
                    "name": f"测试号{index}",
                    "list_title": "",
                }
                for index in range(GDMCH_EXPECTED_NON_DOCTOR_COUNT)
            ]
            payload = {
                "meta": {
                    "category_count": GDMCH_EXPECTED_PAGE_COUNT,
                    "pagination_count": GDMCH_EXPECTED_PAGE_COUNT,
                    "raw_card_rows": GDMCH_EXPECTED_RELATION_COUNT,
                    "candidate_membership_count": GDMCH_EXPECTED_RELATION_COUNT,
                    "unique_candidate_count": GDMCH_EXPECTED_RELATION_COUNT,
                    "census_unique_detail_count": GDMCH_EXPECTED_RELATION_COUNT,
                    "excluded_non_doctor_count": GDMCH_EXPECTED_NON_DOCTOR_COUNT,
                    "eligible_candidate_count": eligible,
                    "photo_census_available_count": GDMCH_EXPECTED_PHOTO_AVAILABLE_COUNT,
                    "photo_census_placeholder_count": eligible
                    - GDMCH_EXPECTED_PHOTO_AVAILABLE_COUNT,
                    "photo_default_placeholder_count": GDMCH_EXPECTED_DEFAULT_PHOTO_COUNT,
                    "cross_entry_duplicate_count": 0,
                    "category_error_count": 0,
                    "detail_error_count": 0,
                    "photo_error_count": 0,
                    "photo_failed_count": 0,
                    "photo_no_source_count": 0,
                    "schedule_field_ingested_count": 0,
                    "private_use_character_count": 0,
                    "independent_entity_count": 0,
                    "affiliate_count": 4,
                    "department_coverage_count": 3,
                    "photo_sample_count": 10,
                    "photo_expected_count": 10,
                    "photo_downloaded_count": 10,
                    "photo_average_bytes": len(content),
                    "photo_estimated_full_count": GDMCH_EXPECTED_PHOTO_AVAILABLE_COUNT,
                    "photo_estimated_full_bytes": len(content)
                    * GDMCH_EXPECTED_PHOTO_AVAILABLE_COUNT,
                    "large_photo_count": 0,
                    "photo_policy_status": "OWNER_APPROVED_ORIGINAL_NO_WIDTH_LIMIT",
                },
                "rows": rows,
                "excluded_candidates": excluded,
                "gdmch_detail_reconciliation": details,
                "photo_samples": photos,
                "affiliate_reconnaissance": [
                    {
                        "name": "番禺院区",
                        "url": "https://www.e3861.com/keshizhuanjia/panyuyuanqu",
                        "relation": "同一官网院区",
                    },
                    {
                        "name": "越秀院区",
                        "url": "https://www.e3861.com/keshizhuanjia/yuexiuyuanqu",
                        "relation": "同一官网院区",
                    },
                    {
                        "name": "天河院区",
                        "url": "https://www.e3861.com/keshizhuanjia/tianheyuanqu",
                        "relation": "同一官网院区",
                    },
                    {
                        "name": "清远院区",
                        "url": "https://www.e3861.com/keshizhuanjia/qingyuanyuanqu",
                        "relation": "同一官网院区",
                    },
                ],
            }

            validate_gdmch_trial(payload, expected_rows=10)

    def test_full_append_is_always_fused_until_owner_switches_phase(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "FULL 发布熔断"):
            validate_gdmch_full_append({})


if __name__ == "__main__":
    unittest.main()
