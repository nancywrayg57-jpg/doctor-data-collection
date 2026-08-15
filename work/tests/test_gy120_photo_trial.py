from __future__ import annotations

import copy
import hashlib
import sys
import tempfile
import unittest
from http.client import IncompleteRead
from pathlib import Path
from unittest.mock import patch

import requests


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import collect_official_doctors_batch as collector  # noqa: E402
from collect_official_doctors_batch import (  # noqa: E402
    GY120_ADAPTER_ID,
    GY120_PHOTO_RETRY_POLICY,
    GY120_PHOTO_UNAVAILABLE_WARNING,
    HospitalTarget,
    collect_gy120,
    decode_gy120_html,
    dedicated_adapter_for,
    download_gy120_photo,
    gy120_detail_id,
    gy120_photo_url,
    merge_gy120_identity_rows,
    parse_gy120_detail,
    parse_gy120_directory,
    select_gy120_trial_doctors,
    validate_gy120_full_append,
    validate_gy120_trial,
)


def png_bytes(width: int, height: int) -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\rIHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x02\x00\x00\x00"
    )


class Gy120PhotoTrialTests(unittest.TestCase):
    def test_exact_entry_detail_photo_and_strict_gb18030(self) -> None:
        entry = "https://www.gy120.net/zhuanjia.asp"
        detail = "https://www.gy120.net/ArticleShow.asp?ArticleID=404"

        self.assertEqual(dedicated_adapter_for(entry), GY120_ADAPTER_ID)
        self.assertNotEqual(dedicated_adapter_for(f"{entry}?page=1"), GY120_ADAPTER_ID)
        self.assertEqual(gy120_detail_id(detail), "404")
        self.assertEqual(gy120_detail_id(detail.replace("ArticleShow", "articleshow")), "404")
        self.assertEqual(gy120_detail_id(f"{detail}&from=search"), "")
        self.assertEqual(
            gy120_photo_url("files/20260428202157997.jpg", detail),
            "https://www.gy120.net/files/20260428202157997.jpg",
        )
        self.assertEqual(
            gy120_photo_url("upsfile/丁彩萍.jpg", detail),
            "https://www.gy120.net/upsfile/丁彩萍.jpg",
        )
        self.assertEqual(gy120_photo_url("other/丁彩萍.jpg", detail), "")
        self.assertEqual(gy120_photo_url("upsfile/%2Fescape.jpg", detail), "")
        self.assertEqual(gy120_photo_url("https://example.com/files/a.jpg", detail), "")
        self.assertEqual(decode_gy120_html("广东药科大学".encode("gb18030")), "广东药科大学")
        with self.assertRaises(UnicodeDecodeError):
            decode_gy120_html(b"\x81")

    def test_directory_parser_reconciles_featured_roles_and_department_tree(self) -> None:
        entry = "https://www.gy120.net/zhuanjia.asp"
        html = """
        <dl class="expert_index_roll_box01"><dt>首席专家</dt><dd>
          <a href="ArticleShow.asp?ArticleID=1"><img src="files/1.jpg">张甲 心内科</a>
        </dd></dl>
        <dl class="expert_index_roll_box01"><dt>科室负责人</dt><dd>
          <a href="ArticleShow.asp?ArticleID=1">张甲 心内科</a>
          <a href="ArticleShow.asp?ArticleID=2">李乙 外科</a>
        </dd></dl>
        <div id="a1"><div class="index_list">
          <dl class="index_list_4"><li><h4>心内科</h4>
            <a href="ArticleShow.asp?ArticleID=1">张甲</a></li></dl>
          <dl class="index_list_2"><li><h4>普通外科</h4>
            <a href="ArticleShow.asp?ArticleID=2">李乙</a></li></dl>
          <dl class="index_list_3"><li><h4>康复科</h4></li></dl>
          <dl class="index_list_5"><li><h4>检验科</h4>
            <a href="ArticleShow.asp?ArticleID=3">王丙</a></li></dl>
        </div></div>
        """

        relations, categories, departments, featured = parse_gy120_directory(html, entry)

        self.assertEqual([item["id"] for item in relations], ["1", "2", "3"])
        self.assertEqual(relations[0]["featured_roles"], ["首席专家", "科室负责人"])
        self.assertEqual(len(featured), 3)
        self.assertEqual(len({item["detail_id"] for item in featured}), 2)
        self.assertEqual(len(categories), 4)
        self.assertEqual(len(departments), 4)
        self.assertEqual(sum(item["relation_count"] for item in departments), 3)
        self.assertEqual(sum(item["relation_count"] == 0 for item in departments), 1)

    def test_detail_parser_keeps_care_sites_but_not_schedule_or_patient_text(self) -> None:
        source = "https://www.gy120.net/ArticleShow.asp?ArticleID=1"
        html = """
        <div class="part1">
          <div class="img"><img src="files/1.JPG"></div>
          <div class="dorname"><div class="title1"><strong>张甲</strong></div>
            <div class="title2">专业职称：主任医师</div>
            <div class="title2">擅长：</div><div class="title2">复杂心血管疾病诊疗</div>
          </div>
        </div>
        <div class="part2"><div class="outpatient_box"><h5><span class="fs18">心血管内科</span></h5>
          <span class="zhuyuanqu1">农林门诊</span><span class="zhuyuanqu2">共和门诊</span>
          <p>周一上午</p></div></div>
        <div class="part3">
          <div class="title1">个人介绍</div><div class="desc">长期从事心血管疾病诊疗。</div>
          <div class="title1">出诊安排</div><div class="desc">周一上午</div>
        </div>
        """

        parsed = parse_gy120_detail(html, {"name": "张甲", "source_link": source})

        self.assertEqual(parsed["name"], "张甲")
        self.assertEqual(parsed["title"], "主任医师")
        self.assertEqual(parsed["specialty"], "复杂心血管疾病诊疗")
        self.assertEqual(parsed["detail_departments"], ["心血管内科"])
        self.assertEqual(parsed["campuses"], ["农林门诊", "共和门诊"])
        self.assertNotIn("周一", parsed["profile_text"])
        self.assertEqual(parsed["photo_state"], "available")
        self.assertEqual(parsed["photo_url"], "https://www.gy120.net/files/1.JPG")

    def test_detail_parser_removes_schedule_tail_and_private_use_character(self) -> None:
        source = "https://www.gy120.net/ArticleShow.asp?ArticleID=290"
        html = """
        <div class="part1">
          <div class="img"><img src="files/290.jpg"></div>
          <div class="dorname"><div class="title1"><strong>何智君</strong></div>
            <div class="title2">专业职称：主治医师</div>
            <div class="title2">擅长：</div>
            <div class="title2">各类错\ue06b畸形矫治 特需门诊时间：周四上午，需预约</div>
          </div>
        </div>
        <div class="part3"><div class="title1">个人介绍</div>
          <div class="desc">论文作者包括周四萍，内容为公开职业资料。</div></div>
        """

        parsed = parse_gy120_detail(html, {"name": "何智君", "source_link": source})

        self.assertEqual(parsed["specialty"], "各类错畸形矫治")
        self.assertNotIn("门诊时间", parsed["specialty"])
        self.assertIn("周四萍", parsed["profile_text"])
        self.assertEqual(parsed["schedule_exclusion_count"], 1)
        self.assertEqual(parsed["private_use_character_exclusion_count"], 1)

    def test_trial_selector_guarantees_three_roles_and_department_spread(self) -> None:
        doctors = []
        for index in range(1, 16):
            roles = ["首席专家"] if index <= 8 else ["科室负责人"] if index <= 12 else []
            doctors.append(
                {
                    "id": str(index),
                    "department": f"科室{index}",
                    "featured_roles": roles,
                    "relation_order": index,
                }
            )

        selected = select_gy120_trial_doctors(doctors, 10)

        self.assertEqual(len(selected), 10)
        self.assertEqual(len({item["department"] for item in selected}), 10)
        self.assertTrue(any("首席专家" in item["featured_roles"] for item in selected))
        self.assertTrue(any("科室负责人" in item["featured_roles"] for item in selected))
        self.assertTrue(any(not item["featured_roles"] for item in selected))

    def test_photo_download_retries_once_with_identical_referer(self) -> None:
        source = "https://www.gy120.net/ArticleShow.asp?ArticleID=1"
        photo_url = "https://www.gy120.net/files/1.png"
        content = png_bytes(640, 480)

        class Response:
            headers = {"Content-Type": "image/png"}

            def __init__(self, status_code: int) -> None:
                self.status_code = status_code
                self.content = content

        class Session:
            def __init__(self) -> None:
                self.calls: list[tuple[str, dict[str, str], int]] = []

            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> Response:
                self.calls.append((url, headers.copy(), timeout))
                return Response(503 if len(self.calls) == 1 else 200)

        session = Session()
        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                result = download_gy120_photo(
                    session,  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-心内科-主任医师-广东药科大学附属第一医院",
                    "1",
                    set(),
                )

        self.assertEqual(result["retry_count"], 1)
        self.assertEqual(len(session.calls), 2)
        self.assertEqual(session.calls[0], session.calls[1])
        sleep_mock.assert_called_once_with(1)

    def test_double_incomplete_transfer_is_approved_blank_result(self) -> None:
        source = "https://www.gy120.net/ArticleShow.asp?ArticleID=1"
        photo_url = "https://www.gy120.net/files/1.png"

        class Session:
            def __init__(self) -> None:
                self.calls = 0

            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> object:
                self.calls += 1
                if self.calls == 1:
                    raise requests.exceptions.ChunkedEncodingError("partial")
                raise IncompleteRead(b"partial", 10)

        session = Session()
        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                result = download_gy120_photo(
                    session,  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-心内科-主任医师-广东药科大学附属第一医院",
                    "1",
                    set(),
                )

        self.assertTrue(result["approved_no_source"])
        self.assertEqual(result["attempt_results"], ["ChunkedEncodingError", "IncompleteRead"])
        self.assertEqual(result["retry_count"], 1)
        sleep_mock.assert_called_once_with(1)

    def test_full_mode_enters_owner_authorized_collection(self) -> None:
        target = HospitalTarget(
            city="广州市",
            hospital="广东药科大学附属第一医院",
            homepage="https://www.gy120.net/",
            entry_url="https://www.gy120.net/zhuanjia.asp",
            review="确认可采集",
            difficulty="D-待人工补官网",
            adapter_id=GY120_ADAPTER_ID,
        )
        with patch(
            "collect_official_doctors_batch.create_official_session",
            side_effect=RuntimeError("authorized-session-created"),
        ) as session_mock:
            with self.assertRaisesRegex(RuntimeError, "authorized-session-created"):
                collect_gy120(target, "2026-08-15", full_mode=True)
        session_mock.assert_called_once_with()

    def test_full_identity_merge_requires_same_name_and_exact_photo_url(self) -> None:
        def row(detail_id: str, photo_url: str, department: str) -> dict[str, object]:
            return {
                "姓名": "张甲",
                "科室_分类页": department,
                "科室_列表卡片": department,
                "职称身份原文": "主任医师",
                "职称_关键词": "主任医师",
                "擅长诊疗方向摘录": "",
                "亮眼经历线索": "",
                "详情正文摘录": "",
                "异常提示": "",
                "重点优先级": "普通",
                "重点关注范围": "",
                "重点疾病标签": "",
                "来源链接": f"https://www.gy120.net/ArticleShow.asp?ArticleID={detail_id}",
                "_gy120_detail_id": detail_id,
                "_gy120_photo_url": photo_url,
                "_gy120_relation_order": int(detail_id),
            }

        rows = [
            row("1", "https://www.gy120.net/files/a.jpg", "科室甲"),
            row("2", "https://www.gy120.net/files/a.jpg", "科室乙"),
            row("3", "https://www.gy120.net/files/b.jpg", "科室丙"),
        ]

        merged, reconciliation = merge_gy120_identity_rows(rows)

        self.assertEqual(len(merged), 2)
        self.assertEqual(
            sorted(len(item["detail_ids"]) for item in reconciliation),
            [1, 2],
        )
        self.assertTrue(all("同名待甄别" in str(item["异常提示"]) for item in merged))

    def test_trial_validator_accepts_closed_synthetic_reconciliation(self) -> None:
        names = ["张甲", "李乙", "王丙", "赵丁", "周戊", "吴己", "郑庚", "孙辛", "陈壬", "刘癸"]
        content = png_bytes(640, 480)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = []
            details = []
            photos = []
            for index, name in enumerate(names, start=1):
                detail_id = "42" if index == 10 else str(index)
                source = f"https://www.gy120.net/ArticleShow.asp?ArticleID={detail_id}"
                photo_url = (
                    "https://www.gy120.net/upsfile/丁彩萍.jpg"
                    if detail_id == "42"
                    else f"https://www.gy120.net/files/{detail_id}.png"
                )
                filename = f"{name}-科室-主任医师-广东药科大学附属第一医院.png"
                disk_path = root / filename
                disk_path.write_bytes(content)
                department = f"科室{(index - 1) % 4 + 1}"
                roles = ["首席专家"] if index == 1 else ["科室负责人"] if index == 2 else []
                details.append(
                    {
                        "detail_id": detail_id,
                        "directory_name": name,
                        "detail_name": name,
                        "name_matches_directory": True,
                        "category": "内科",
                        "directory_department": department,
                        "detail_departments": [department],
                        "campuses": ["农林门诊"],
                        "title": "主任医师",
                        "featured_roles": roles,
                        "photo_state": "available",
                        "photo_url": photo_url,
                        "source_link": source,
                        "detail_status": 200,
                        "detail_error": "",
                        "resolution": "详情已读取",
                    }
                )
                relative = (
                    Path("01_试点医院")
                    / "广东药科大学附属第一医院"
                    / "照片"
                    / filename
                ).as_posix()
                rows.append(
                    {
                        "医院": "广东药科大学附属第一医院",
                        "姓名": name,
                        "科室_分类页": department,
                        "科室_列表卡片": department,
                        "职称_关键词": "主任医师",
                        "职称身份原文": "主任医师",
                        "重点优先级": "普通",
                        "重点关注范围": "",
                        "重点疾病标签": "",
                        "擅长诊疗方向摘录": "",
                        "亮眼经历线索": "",
                        "列表简介": "",
                        "详情正文摘录": "论文作者：周四萍" if index == 1 else "",
                        "来源类型": "医院官网",
                        "来源链接": source,
                        "照片链接": photo_url,
                        "照片文件": relative,
                        "采集入口": "https://www.gy120.net/zhuanjia.asp",
                        "采集方式": "测试",
                        "采集日期": "2026-08-15",
                        "详情页状态": "200",
                        "已建画像": "否",
                        "异常提示": "",
                        "复核状态": "待人工复核",
                    }
                )
                photos.append(
                    {
                        "name": name,
                        "department": department,
                        "title": "主任医师",
                        "detail_id": detail_id,
                        "source_link": source,
                        "photo_url": photo_url,
                        "photo_file": relative,
                        "filename": filename,
                        "bytes": len(content),
                        "sha256": hashlib.sha256(content).hexdigest(),
                        "width": 640,
                        "height": 480,
                        "disk_path": str(disk_path),
                        "retry_count": 0,
                        "attempt_results": ["HTTP 200"],
                    }
                )
            details.append(
                {
                    "detail_id": "11",
                    "directory_name": "何护士",
                    "detail_name": "何护士",
                    "name_matches_directory": True,
                    "category": "其他科室",
                    "directory_department": "护理门诊",
                    "detail_departments": ["护理门诊"],
                    "campuses": ["共和门诊"],
                    "title": "护师",
                    "featured_roles": [],
                    "photo_state": "available",
                    "photo_url": "https://www.gy120.net/files/11.png",
                    "source_link": "https://www.gy120.net/ArticleShow.asp?ArticleID=11",
                    "detail_status": 200,
                    "detail_error": "",
                    "resolution": "护理身份排除",
                }
            )
            featured = [
                {
                    "detail_id": "1" if index < 14 else "2",
                    "role": "首席专家" if index < 14 else "科室负责人",
                    "name_and_department": "测试",
                    "source_link": "https://www.gy120.net/ArticleShow.asp?ArticleID=1",
                }
                for index in range(58)
            ]
            identities = [
                {
                    "name": row["姓名"],
                    "identity_index": 1,
                    "detail_ids": [gy120_detail_id(str(row["来源链接"]))],
                    "resolution": "唯一身份",
                    "relation_count": 1,
                    "classification_departments": [row["科室_分类页"]],
                    "card_departments": [row["科室_列表卡片"]],
                    "titles": [row["职称身份原文"]],
                    "primary_detail_id": gy120_detail_id(str(row["来源链接"])),
                    "primary_source_link": row["来源链接"],
                    "official_photo_url": row["照片链接"],
                    "merged_source_links": [],
                }
                for row in rows
            ]
            payload = {
                "meta": {
                    "category_count": 4,
                    "pagination_count": 1,
                    "census_department_count": 4,
                    "census_empty_department_count": 0,
                    "candidate_membership_count": 11,
                    "unique_candidate_count": 11,
                    "census_unique_detail_count": 11,
                    "featured_occurrence_count": 58,
                    "featured_unique_count": 2,
                    "featured_department_overlap_count": 58,
                    "excluded_non_doctor_count": 1,
                    "eligible_candidate_count": 10,
                    "unique_doctor_count": 10,
                    "final_identity_count": 10,
                    "identity_merge_count": 0,
                    "identity_reconciliation_count": 10,
                    "full_authorization": (
                        "PR #48 owner 评论明确审计通过并切换 "
                        "FULL_APPEND_AND_OBSIDIAN"
                    ),
                    "category_error_count": 0,
                    "detail_error_count": 0,
                    "name_mismatch_count": 0,
                    "encoding_replacement_count": 0,
                    "encoding_mojibake_count": 0,
                    "schedule_field_ingested_count": 0,
                    "private_use_character_count": 0,
                    "independent_entity_count": 0,
                    "photo_error_count": 0,
                    "photo_census_available_count": 10,
                    "photo_census_placeholder_count": 0,
                    "photo_census_empty_count": 0,
                    "photo_census_rejected_count": 0,
                    "department_coverage_count": 4,
                    "sample_featured_role_counts": {"首席专家": 1, "科室负责人": 1},
                    "sample_non_featured_count": 8,
                    "photo_expected_count": 10,
                    "photo_downloaded_count": 10,
                    "photo_failed_count": 0,
                    "photo_no_source_count": 0,
                    "photo_bounded_retry_count": 0,
                    "photo_retry_policy": GY120_PHOTO_RETRY_POLICY,
                    "photo_average_bytes": len(content),
                    "photo_estimated_full_count": 10,
                    "photo_estimated_full_bytes": len(content) * 10,
                    "large_photo_count": 0,
                    "photo_policy_status": "OWNER_APPROVED_ORIGINAL_NO_WIDTH_LIMIT",
                    "census_campus_counts": {
                        "农林门诊": 8,
                        "共和门诊": 2,
                        "健康管理中心": 1,
                    },
                },
                "categories": [
                    {"category_name": "内科", "department_count": 1, "row_count": 3},
                    {"category_name": "外科", "department_count": 1, "row_count": 3},
                    {"category_name": "其他科室", "department_count": 1, "row_count": 3},
                    {"category_name": "医技", "department_count": 1, "row_count": 2},
                ],
                "department_tree": [
                    {"category": "内科", "department": "科室1", "relation_count": 3},
                    {"category": "外科", "department": "科室2", "relation_count": 3},
                    {"category": "其他科室", "department": "科室3", "relation_count": 3},
                    {"category": "医技", "department": "科室4", "relation_count": 2},
                ],
                "gy120_detail_reconciliation": details,
                "gy120_sample_detail_reconciliation": details[:10],
                "gy120_featured_reconciliation": featured,
                "gy120_identity_reconciliation": identities,
                "detail_errors": [],
                "excluded_candidates": [
                    {
                        "detail_id": "11",
                        "name": "何护士",
                        "list_title": "护师",
                        "department": "护理门诊",
                        "reason": "官网详情专业职称明确为纯护理身份",
                        "source_link": "https://www.gy120.net/ArticleShow.asp?ArticleID=11",
                    }
                ],
                "photo_samples": photos,
                "photo_no_sources": [],
                "rows": rows,
            }
            patched = {
                "GY120_EXPECTED_DEPARTMENT_COUNT": 4,
                "GY120_EXPECTED_EMPTY_DEPARTMENT_COUNT": 0,
                "GY120_EXPECTED_RELATION_COUNT": 11,
                "GY120_EXPECTED_UNIQUE_ID_COUNT": 11,
                "GY120_EXPECTED_FEATURED_UNIQUE_COUNT": 2,
                "GY120_EXPECTED_NURSING_COUNT": 1,
                "GY120_EXPECTED_PHOTO_AVAILABLE_COUNT": 10,
                "GY120_EXPECTED_PHOTO_PLACEHOLDER_COUNT": 0,
                "GY120_EXPECTED_PHOTO_EMPTY_COUNT": 0,
                "GY120_EXPECTED_PHOTO_REJECTED_COUNT": 0,
                "GY120_EXPECTED_CATEGORY_COUNTS": {
                    "内科": 1,
                    "外科": 1,
                    "其他科室": 1,
                    "医技": 1,
                },
                "GY120_EXPECTED_CATEGORY_RELATION_COUNTS": {
                    "内科": 3,
                    "外科": 3,
                    "其他科室": 3,
                    "医技": 2,
                },
            }
            with patch.multiple(collector, **patched):
                validate_gy120_trial(payload, expected_rows=10)
                validate_gy120_full_append(payload)

                failure_payload = copy.deepcopy(payload)
                failed_source = "https://www.gy120.net/ArticleShow.asp?ArticleID=1"
                failed_detail = failure_payload["gy120_detail_reconciliation"][0]
                failed_detail.update(
                    {
                        "detail_status": None,
                        "detail_error": "ConnectionError: bounded detail request failed",
                        "photo_state": "empty",
                        "photo_url": "",
                        "resolution": "详情读取失败",
                    }
                )
                failure_payload["detail_errors"] = [
                    {
                        "detail_id": "1",
                        "name": "张甲",
                        "source_link": failed_source,
                        "error": "ConnectionError: bounded detail request failed",
                    }
                ]
                failed_row = next(
                    row for row in failure_payload["rows"] if row["来源链接"] == failed_source
                )
                failed_row.update(
                    {
                        "照片链接": "",
                        "照片文件": "",
                        "详情页状态": "",
                        "异常提示": "详情读取失败，按 Issue 指令保守成行",
                    }
                )
                failed_identity = next(
                    item
                    for item in failure_payload["gy120_identity_reconciliation"]
                    if item["primary_detail_id"] == "1"
                )
                failed_identity["official_photo_url"] = ""
                failure_payload["photo_samples"] = [
                    item
                    for item in failure_payload["photo_samples"]
                    if item["source_link"] != failed_source
                ]
                failure_payload["photo_no_sources"] = [
                    {
                        "name": "张甲",
                        "detail_id": "1",
                        "source_link": failed_source,
                        "photo_state": "empty",
                        "retry_count": 0,
                        "reason": "官网详情读取失败，照片按批准口径留空",
                    }
                ]
                failure_payload["meta"].update(
                    {
                        "detail_error_count": 1,
                        "photo_census_available_count": 9,
                        "photo_census_empty_count": 1,
                        "photo_downloaded_count": 9,
                        "photo_failed_count": 1,
                        "photo_no_source_count": 1,
                    }
                )
                validate_gy120_full_append(failure_payload)

                payload["photo_samples"][0]["sha256"] = "0" * 64
                with self.assertRaisesRegex(RuntimeError, "SHA-256"):
                    validate_gy120_trial(payload, expected_rows=10)


if __name__ == "__main__":
    unittest.main()
