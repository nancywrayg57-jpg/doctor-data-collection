from __future__ import annotations

import hashlib
import requests
import sys
import tempfile
import unittest
from collections import Counter
from http.client import IncompleteRead
from pathlib import Path
from unittest.mock import patch


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

from collect_official_doctors_batch import (  # noqa: E402
    GD2H_ADAPTER_ID,
    GD2H_BROKEN_PHOTO_WARNING,
    GD2H_EXPECTED_CATEGORY_COUNTS,
    GD2H_EXPECTED_ELIGIBLE_COUNT,
    GD2H_EXPECTED_EMPTY_PHOTO_COUNT,
    GD2H_EXPECTED_FINAL_IDENTITY_COUNT,
    GD2H_EXPECTED_HASH_ID_COUNT,
    GD2H_EXPECTED_NURSING_COUNT,
    GD2H_EXPECTED_NUMERIC_ID_COUNT,
    GD2H_EXPECTED_PHOTO_AVAILABLE_COUNT,
    GD2H_EXPECTED_PLACEHOLDER_COUNT,
    GD2H_EXPECTED_RELATION_COUNT,
    GD2H_PHOTO_RETRY_POLICY,
    GD2H_TRANSPORT_FAILURE_WARNING,
    HospitalTarget,
    collect_gd2h,
    dedicated_adapter_for,
    download_gd2h_photo,
    gd2h_detail_id,
    gd2h_photo_url,
    gd2h_primary_title,
    mark_gd2h_broken_photo_row,
    mark_gd2h_transport_failed_photo_row,
    merge_gd2h_identity_rows,
    parse_gd2h_detail,
    parse_gd2h_directory,
    select_gd2h_trial_doctors,
    strip_gd2h_breadcrumb_prefix,
    validate_gd2h_full_append,
    validate_gd2h_trial,
)


def png_bytes(width: int, height: int) -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\rIHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x02\x00\x00\x00"
    )


class Gd2hPhotoTrialTests(unittest.TestCase):
    def test_exact_entry_and_case_sensitive_detail_id(self) -> None:
        entry = "https://gd2h.com/site/column/107_1_20.html"
        detail = "https://gd2h.com/site/detail/AbC123Def.html"

        self.assertEqual(dedicated_adapter_for(entry), GD2H_ADAPTER_ID)
        self.assertNotEqual(dedicated_adapter_for(f"{entry}?page=1"), GD2H_ADAPTER_ID)
        self.assertEqual(gd2h_detail_id(detail), "AbC123Def")
        self.assertNotEqual(gd2h_detail_id(detail), gd2h_detail_id(detail.lower()))
        self.assertEqual(gd2h_detail_id(f"{detail}?from=search"), "")

    def test_static_two_campus_six_column_directory_and_nursing_identity(self) -> None:
        entry = "https://gd2h.com/site/column/107_1_20.html"
        html = """
        <div class="xxk-item1">
          <ul class="zjlist0"><li><div class="subject">心血管内科</div>
            <a href="/site/detail/AbC1.html">\u200b张甲</a></li></ul>
          <ul class="zjlist1"><li><div class="subject">放射科</div>
            <a href="/site/detail/1002.html">钱乙</a></li></ul>
          <div class="zjlist2"><div class="item"><a href="/site/detail/1003.html">
            <div class="info"><span>孙丙</span><li>主管护师</li></div></a></div></div>
        </div>
        <div class="xxk-item2">
          <ul class="zjlist0"><li><div class="subject">内科</div>
            <a href="/site/detail/2001.html">李丁</a></li></ul>
          <ul class="zjlist1"><li><div class="subject">超声科</div>
            <a href="/site/detail/HashTwo.html">周戊</a></li></ul>
          <div class="zjlist2"><div class="item"><a href="/site/detail/2003.html">
            <div class="info"><span>吴己</span><li>护师</li></div></a></div></div>
        </div>
        """

        relations, categories, departments = parse_gd2h_directory(html, entry)

        self.assertEqual(len(relations), 6)
        self.assertEqual(len({item["id"] for item in relations}), 6)
        self.assertEqual(relations[0]["name"], "张甲")
        self.assertNotIn("\u200b", "".join(item["name"] for item in relations))
        self.assertEqual(len(categories), 6)
        self.assertEqual(sum(item["row_count"] for item in categories), 6)
        self.assertEqual(sum(item["relation_count"] for item in departments), 6)
        nursing = [item for item in relations if item["category"] == "护理专家"]
        self.assertEqual([item["list_title"] for item in nursing], ["主管护师", "护师"])

    def test_detail_parser_strips_schedule_and_normalizes_official_photo(self) -> None:
        source = "https://gd2h.com/site/detail/AbC123.html"
        html = """
        <div class="right-container">
          <div class="grjj">
            <img src="http://gd2h.com/static/seygw/resources/upload/doctor/AbC123.png">
            <p>姓名：\u200b张甲</p><p>职称：主任医师</p><p>科室：心血管内科</p>
            <p>擅长：复杂心血管疾病诊疗</p>
          </div>
          <div class="expertIntro">
            <p>首页 &gt; 患者服务</p><p>专家介绍（民航院区）</p><p>临床专家</p>
            <p>长期从事心血管疾病诊疗。</p>
            <p>门诊时间：周一上午</p>
            <p>此排班尾段不得保留</p>
          </div>
        </div>
        """

        parsed = parse_gd2h_detail(
            html,
            {"name": "张甲", "department": "心内科", "source_link": source},
        )

        self.assertEqual(parsed["name"], "张甲")
        self.assertNotIn("\u200b", "".join(str(value) for value in parsed.values()))
        self.assertEqual(parsed["department"], "心血管内科")
        self.assertEqual(parsed["photo_state"], "available")
        self.assertTrue(parsed["photo_url"].startswith("https://gd2h.com/static/"))
        self.assertIn("长期从事", parsed["profile_text"])
        self.assertNotIn("首页 >", parsed["profile_text"])
        self.assertNotIn("专家介绍", parsed["profile_text"])
        self.assertNotIn("门诊时间", parsed["profile_text"])
        self.assertNotIn("排班尾段", parsed["profile_text"])
        self.assertEqual(parsed["schedule_exclusion_count"], 1)
        self.assertEqual(
            gd2h_photo_url(
                "/static//seygw//resources/upload/2024/05/28/default_ys.gif",
                source,
            ),
            "",
        )
        self.assertEqual(gd2h_photo_url("", source), "")
        self.assertEqual(
            strip_gd2h_breadcrumb_prefix(
                "首页 > 患者服务 专家介绍（民航院区） 医技专家 颜剑豪简介"
            ),
            "颜剑豪简介",
        )
        self.assertEqual(
            strip_gd2h_breadcrumb_prefix("医生介绍中保留 首页 > 的原始表述"),
            "医生介绍中保留 首页 > 的原始表述",
        )

    def test_photo_download_uses_matching_public_detail_referer(self) -> None:
        content = png_bytes(640, 480)
        source = "https://gd2h.com/site/detail/AbC123.html"
        photo_url = "https://gd2h.com/static/seygw/resources/upload/doctor/AbC123.png"

        class Response:
            headers = {"Content-Type": "image/png"}

            def __init__(self, value: bytes, status_code: int) -> None:
                self.content = value
                self.status_code = status_code

        class Session:
            def __init__(self) -> None:
                self.calls: list[tuple[str, dict[str, str], int]] = []

            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> Response:
                self.calls.append((url, headers.copy(), timeout))
                return Response(content, 403 if len(self.calls) == 1 else 200)

        session = Session()
        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                result = download_gd2h_photo(
                    session,  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-心血管内科-主任医师-广东省第二人民医院",
                    "AbC123",
                    set(),
                )

        self.assertEqual(
            session.calls,
            [
                (photo_url, {"Referer": source}, 30),
                (photo_url, {"Referer": source}, 30),
            ],
        )
        sleep_mock.assert_called_once_with(1)
        self.assertEqual(result["retry_count"], 1)
        self.assertEqual(result["bytes"], len(content))
        self.assertEqual(result["width"], 640)
        self.assertEqual(result["height"], 480)

        class AlwaysFailSession(Session):
            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> Response:
                self.calls.append((url, headers.copy(), timeout))
                return Response(content, 403)

        failing_session = AlwaysFailSession()
        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(RuntimeError, "单次重试后仍为 HTTP 403"):
                    download_gd2h_photo(
                        failing_session,  # type: ignore[arg-type]
                        photo_url,
                        source,
                        Path(directory),
                        "张甲-心血管内科-主任医师-广东省第二人民医院",
                        "AbC123",
                        set(),
                    )
        self.assertEqual(len(failing_session.calls), 2)
        self.assertEqual(failing_session.calls[0], failing_session.calls[1])
        sleep_mock.assert_called_once_with(1)

        class ApprovedBrokenSession(Session):
            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> Response:
                self.calls.append((url, headers.copy(), timeout))
                return Response(content, 404)

        approved_session = ApprovedBrokenSession()
        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                approved = download_gd2h_photo(
                    approved_session,  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-心血管内科-主任医师-广东省第二人民医院",
                    "AbC123",
                    set(),
                )
        self.assertTrue(approved["approved_no_source"])
        self.assertEqual(approved["original_photo_url"], photo_url)
        self.assertEqual(approved["http_status"], 404)
        self.assertEqual(approved["approved_no_source_reason"], "double_404")
        self.assertEqual(approved["retry_count"], 1)
        self.assertEqual(len(approved_session.calls), 2)
        self.assertEqual(approved_session.calls[0], approved_session.calls[1])
        sleep_mock.assert_called_once_with(1)

        class TimeoutThenSuccessSession(Session):
            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> Response:
                self.calls.append((url, headers.copy(), timeout))
                if len(self.calls) == 1:
                    raise requests.Timeout("first timeout")
                return Response(content, 200)

        timeout_then_success = TimeoutThenSuccessSession()
        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                recovered = download_gd2h_photo(
                    timeout_then_success,  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-心血管内科-主任医师-广东省第二人民医院",
                    "AbC123",
                    set(),
                )
        self.assertEqual(recovered["retry_count"], 1)
        self.assertEqual(len(timeout_then_success.calls), 2)
        self.assertEqual(
            timeout_then_success.calls[0], timeout_then_success.calls[1]
        )
        sleep_mock.assert_called_once_with(1)

        class DoubleTransportFailureSession(Session):
            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> Response:
                self.calls.append((url, headers.copy(), timeout))
                if len(self.calls) == 1:
                    raise requests.Timeout("first timeout")
                raise requests.ConnectionError("second connection error")

        double_transport_failure = DoubleTransportFailureSession()
        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                transport_approved = download_gd2h_photo(
                    double_transport_failure,  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-心血管内科-主任医师-广东省第二人民医院",
                    "AbC123",
                    set(),
                )
        self.assertTrue(transport_approved["approved_no_source"])
        self.assertEqual(
            transport_approved["approved_no_source_reason"], "transport_failure"
        )
        self.assertEqual(
            transport_approved["transport_error_kinds"],
            ["timeout", "connection_error"],
        )
        self.assertEqual(len(double_transport_failure.calls), 2)
        self.assertEqual(
            double_transport_failure.calls[0], double_transport_failure.calls[1]
        )
        sleep_mock.assert_called_once_with(1)

        class DoubleIncompleteReadSession(Session):
            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> Response:
                self.calls.append((url, headers.copy(), timeout))
                if len(self.calls) == 1:
                    raise requests.exceptions.ChunkedEncodingError(
                        "first incomplete response"
                    )
                raise IncompleteRead(b"partial", 10)

        double_incomplete_read = DoubleIncompleteReadSession()
        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                incomplete_approved = download_gd2h_photo(
                    double_incomplete_read,  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-心血管内科-主任医师-广东省第二人民医院",
                    "AbC123",
                    set(),
                )
        self.assertTrue(incomplete_approved["approved_no_source"])
        self.assertEqual(
            incomplete_approved["transport_error_kinds"],
            ["incomplete_read", "incomplete_read"],
        )
        self.assertEqual(len(double_incomplete_read.calls), 2)
        self.assertEqual(
            double_incomplete_read.calls[0], double_incomplete_read.calls[1]
        )
        sleep_mock.assert_called_once_with(1)

        class MixedFailureSession(Session):
            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> Response:
                self.calls.append((url, headers.copy(), timeout))
                if len(self.calls) == 1:
                    raise requests.Timeout("first timeout")
                return Response(content, 404)

        mixed_failure = MixedFailureSession()
        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(
                    RuntimeError, "首次发生传输层 timeout，唯一重试为 HTTP 404"
                ):
                    download_gd2h_photo(
                        mixed_failure,  # type: ignore[arg-type]
                        photo_url,
                        source,
                        Path(directory),
                        "张甲-心血管内科-主任医师-广东省第二人民医院",
                        "AbC123",
                        set(),
                    )
        self.assertEqual(len(mixed_failure.calls), 2)
        self.assertEqual(mixed_failure.calls[0], mixed_failure.calls[1])
        sleep_mock.assert_called_once_with(1)

    def test_admin_approved_broken_photo_is_blank_and_downgraded(self) -> None:
        row = {
            "异常提示": "既有提示",
            "重点优先级": "高",
            "重点关注范围": "慢性病",
            "重点疾病标签": "高血压",
            "照片链接": "https://gd2h.com/static/doctor/broken.jpg",
            "照片文件": "01_试点医院/广东省第二人民医院/照片/失效.jpg",
        }

        mark_gd2h_broken_photo_row(row)
        mark_gd2h_broken_photo_row(row)

        self.assertEqual(
            row["异常提示"], f"既有提示；{GD2H_BROKEN_PHOTO_WARNING}"
        )
        self.assertEqual(row["重点优先级"], "普通")
        self.assertEqual(row["重点关注范围"], "")
        self.assertEqual(row["重点疾病标签"], "")
        self.assertEqual(row["照片链接"], "")
        self.assertEqual(row["照片文件"], "")

        transport_row = {
            "异常提示": "",
            "重点优先级": "高",
            "重点关注范围": "术后恢复",
            "重点疾病标签": "骨折",
            "照片链接": "https://gd2h.com/static/doctor/timeout.jpg",
            "照片文件": "01_试点医院/广东省第二人民医院/照片/超时.jpg",
        }
        mark_gd2h_transport_failed_photo_row(transport_row)
        self.assertEqual(
            transport_row["异常提示"], GD2H_TRANSPORT_FAILURE_WARNING
        )
        self.assertEqual(transport_row["重点优先级"], "普通")
        self.assertEqual(transport_row["重点关注范围"], "")
        self.assertEqual(transport_row["重点疾病标签"], "")
        self.assertEqual(transport_row["照片链接"], "")
        self.assertEqual(transport_row["照片文件"], "")

    def test_primary_title_keeps_deputy_director_title(self) -> None:
        self.assertEqual(gd2h_primary_title("副主任医师"), "副主任医师")
        self.assertEqual(gd2h_primary_title("主任医师"), "主任医师")

    def test_trial_selector_covers_both_campuses_categories_and_id_formats(self) -> None:
        doctors = []
        definitions = [
            ("HashPz", "琶洲院区", "临床专家", "心血管内科"),
            ("1001", "琶洲院区", "临床专家", "神经内科"),
            ("1002", "琶洲院区", "医技专家", "放射科"),
            ("HashMh", "民航院区", "临床专家", "内科"),
            ("HashTechMh", "民航院区", "医技专家", "超声科"),
        ]
        definitions.extend(
            (str(2000 + index), "琶洲院区", "临床专家", f"科室{index}")
            for index in range(6)
        )
        for index, (detail_id, campus, category, department) in enumerate(definitions):
            doctors.append(
                {
                    "id": detail_id,
                    "name": f"医生{chr(0x7532 + index)}",
                    "campus": campus,
                    "category": category,
                    "department": department,
                    "relation_order": index + 1,
                }
            )

        selected = select_gd2h_trial_doctors(doctors, 10)

        self.assertEqual(len(selected), 10)
        self.assertEqual({item["campus"] for item in selected}, {"琶洲院区", "民航院区"})
        self.assertEqual({item["category"] for item in selected}, {"临床专家", "医技专家"})
        self.assertEqual(
            {"numeric" if item["id"].isdigit() else "hash" for item in selected},
            {"numeric", "hash"},
        )
        self.assertGreaterEqual(len({item["department"] for item in selected}), 3)

    def test_trial_validator_accepts_exact_census_and_rejects_id_case_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = png_bytes(640, 480)
            digest = hashlib.sha256(content).hexdigest()
            numeric_ids = [str(100000 + index) for index in range(457)]
            hash_ids = [f"AbC{index:029X}" for index in range(GD2H_EXPECTED_HASH_ID_COUNT)]
            eligible_ids = numeric_ids + hash_ids
            self.assertEqual(len(eligible_ids), GD2H_EXPECTED_ELIGIBLE_COUNT)

            details = []
            for detail_id in eligible_ids:
                details.append(
                    {
                        "detail_id": detail_id,
                        "id_format": "numeric" if detail_id.isdigit() else "hash",
                        "directory_name": "普通医生",
                        "detail_name": "普通医生",
                        "name": "普通医生",
                        "name_matches_directory": True,
                        "campus": "琶洲院区",
                        "category": "临床专家",
                        "directory_department": "内科",
                        "detail_department": "内科",
                        "title": "主任医师",
                        "photo_state": "available",
                        "source_link": f"https://gd2h.com/site/detail/{detail_id}.html",
                        "resolution": "详情已读取",
                    }
                )

            sample_indexes = [0, 1, 2, 3, 4, 457, 458, 459, 460, 461]
            sample_shape = [
                ("琶洲院区", "临床专家", "心血管内科"),
                ("琶洲院区", "临床专家", "神经内科"),
                ("琶洲院区", "医技专家", "放射科"),
                ("民航院区", "临床专家", "内科"),
                ("民航院区", "医技专家", "超声科"),
                ("琶洲院区", "临床专家", "肿瘤科"),
                ("民航院区", "临床专家", "呼吸内科"),
                ("琶洲院区", "医技专家", "检验科"),
                ("琶洲院区", "临床专家", "外科"),
                ("民航院区", "临床专家", "康复科"),
            ]
            rows = []
            photos = []
            for position, detail_index in enumerate(sample_indexes):
                detail = details[detail_index]
                detail_id = detail["detail_id"]
                campus, category, department = sample_shape[position]
                name = f"赵{chr(0x7532 + position)}"
                detail.update(
                    {
                        "directory_name": name,
                        "detail_name": name,
                        "name": name,
                        "campus": campus,
                        "category": category,
                        "directory_department": department,
                        "detail_department": department,
                    }
                )
                filename = f"{name}-{department}-主任医师-广东省第二人民医院.png"
                disk_path = root / filename
                disk_path.write_bytes(content)
                source = detail["source_link"]
                photo_url = (
                    "https://gd2h.com/static/seygw/resources/upload/doctor/"
                    f"{detail_id}.png"
                )
                relative = f"01_试点医院/广东省第二人民医院/照片/{filename}"
                rows.append(
                    {
                        "姓名": name,
                        "科室_分类页": f"{department}（{campus}）",
                        "科室_列表卡片": f"{department}（{campus}）",
                        "职称身份原文": "主任医师",
                        "重点优先级": "普通",
                        "重点关注范围": "",
                        "重点疾病标签": "",
                        "擅长诊疗方向摘录": "疾病诊疗",
                        "亮眼经历线索": "",
                        "列表简介": "",
                        "详情正文摘录": "公开职业简介",
                        "来源链接": source,
                        "照片链接": photo_url,
                        "照片文件": relative,
                        "异常提示": "",
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
                        "sha256": digest,
                        "width": 640,
                        "height": 480,
                        "disk_path": str(disk_path),
                    }
                )

            sample_details = [details[index] for index in sample_indexes]
            sample_campus_counts = Counter(item["campus"] for item in sample_details)
            sample_category_counts = Counter(item["category"] for item in sample_details)
            sample_id_counts = Counter(item["id_format"] for item in sample_details)
            excluded = [
                {
                    "detail_id": str(900000 + index),
                    "name": f"护理{index}",
                    "list_title": "护师",
                    "campus": "琶洲院区" if index < 21 else "民航院区",
                    "category": "护理专家",
                    "department": "护理专家",
                    "source_link": f"https://gd2h.com/site/detail/{900000 + index}.html",
                    "individual_nursing_identity": True,
                    "reason": "官网护理专家栏目整栏排除；个体职称同时明确为护理身份",
                }
                for index in range(GD2H_EXPECTED_NURSING_COUNT)
            ]
            payload = {
                "meta": {
                    "category_count": len(GD2H_EXPECTED_CATEGORY_COUNTS),
                    "pagination_count": 1,
                    "raw_card_rows": GD2H_EXPECTED_RELATION_COUNT,
                    "candidate_membership_count": GD2H_EXPECTED_RELATION_COUNT,
                    "unique_candidate_count": GD2H_EXPECTED_RELATION_COUNT,
                    "census_unique_detail_count": GD2H_EXPECTED_RELATION_COUNT,
                    "census_numeric_id_count": GD2H_EXPECTED_NUMERIC_ID_COUNT,
                    "census_hash_id_count": GD2H_EXPECTED_HASH_ID_COUNT,
                    "excluded_non_doctor_count": GD2H_EXPECTED_NURSING_COUNT,
                    "nursing_column_count": GD2H_EXPECTED_NURSING_COUNT,
                    "nursing_identity_mismatch_count": 0,
                    "eligible_candidate_count": GD2H_EXPECTED_ELIGIBLE_COUNT,
                    "photo_census_available_count": GD2H_EXPECTED_PHOTO_AVAILABLE_COUNT,
                    "photo_census_placeholder_count": GD2H_EXPECTED_PLACEHOLDER_COUNT,
                    "photo_census_empty_count": GD2H_EXPECTED_EMPTY_PHOTO_COUNT,
                    "photo_census_rejected_count": 0,
                    "cross_entry_duplicate_count": 0,
                    "category_error_count": 0,
                    "detail_error_count": 0,
                    "photo_error_count": 0,
                    "photo_failed_count": 0,
                    "photo_no_source_count": 0,
                    "schedule_field_ingested_count": 0,
                    "private_use_character_count": 0,
                    "affiliate_count": 2,
                    "independent_entity_count": 0,
                    "department_coverage_count": len({item[2] for item in sample_shape}),
                    "sample_campus_counts": dict(sample_campus_counts),
                    "sample_category_counts": dict(sample_category_counts),
                    "sample_id_format_counts": dict(sample_id_counts),
                    "photo_sample_count": 10,
                    "photo_expected_count": 10,
                    "photo_downloaded_count": 10,
                    "photo_average_bytes": len(content),
                    "photo_bounded_retry_count": 0,
                    "photo_retry_policy": GD2H_PHOTO_RETRY_POLICY,
                    "photo_estimated_full_count": GD2H_EXPECTED_PHOTO_AVAILABLE_COUNT,
                    "photo_estimated_full_bytes": len(content)
                    * GD2H_EXPECTED_PHOTO_AVAILABLE_COUNT,
                    "large_photo_count": 0,
                    "photo_policy_status": "OWNER_APPROVED_ORIGINAL_NO_WIDTH_LIMIT",
                },
                "categories": [
                    {
                        "category_name": name,
                        "row_count": count,
                        "url": "https://gd2h.com/site/column/107_1_20.html",
                    }
                    for name, count in GD2H_EXPECTED_CATEGORY_COUNTS.items()
                ],
                "department_tree": [
                    {
                        "campus": name.split("-", 1)[0],
                        "category": name.split("-", 1)[1],
                        "department": name.split("-", 1)[1],
                        "relation_count": count,
                    }
                    for name, count in GD2H_EXPECTED_CATEGORY_COUNTS.items()
                ],
                "rows": rows,
                "excluded_candidates": excluded,
                "gd2h_detail_reconciliation": details,
                "gd2h_sample_detail_reconciliation": sample_details,
                "photo_samples": photos,
            }

            validate_gd2h_trial(payload, expected_rows=10)

            hash_detail = details[457]
            hash_detail["source_link"] = hash_detail["source_link"].lower()
            with self.assertRaisesRegex(RuntimeError, "大小写原样"):
                validate_gd2h_trial(payload, expected_rows=10)

    def test_full_identity_merge_uses_explicit_groups_and_preserves_distinct_names(self) -> None:
        def row(
            name: str,
            detail_id: str,
            department: str,
            campus: str,
            profile: str,
            *,
            photo_state: str = "available",
        ) -> dict[str, object]:
            source = f"https://gd2h.com/site/detail/{detail_id}.html"
            return {
                "姓名": name,
                "科室_分类页": f"{department}（{campus}）",
                "科室_列表卡片": f"{department}（{campus}）",
                "职称身份原文": "副主任医师",
                "职称_关键词": "副主任医师",
                "重点优先级": "高",
                "重点关注范围": "慢性病",
                "重点疾病标签": "高血压",
                "擅长诊疗方向摘录": profile,
                "亮眼经历线索": "",
                "详情正文摘录": profile,
                "来源链接": source,
                "异常提示": "",
                "_gd2h_detail_id": detail_id,
                "_gd2h_photo_url": f"https://gd2h.com/static/{detail_id}.jpg",
                "_gd2h_photo_state": photo_state,
                "_gd2h_first_department": department,
                "_gd2h_campus": campus,
                "_gd2h_relation_order": 1,
            }

        rows = [
            row("张晓", "42013", "儿科", "琶洲院区", "短简介"),
            row("张晓", "42041", "风湿免疫科", "琶洲院区", "更完整的官方职业简介"),
            row("张辉", "41995", "脊柱骨科", "琶洲院区", "骨科职业简介"),
            row("张辉", "42337", "麻醉科", "琶洲院区", "麻醉职业简介"),
        ]

        merged, reconciliation = merge_gd2h_identity_rows(rows)

        self.assertEqual(len(merged), 3)
        self.assertEqual(
            sum(len(item["detail_ids"]) for item in reconciliation),  # type: ignore[arg-type]
            4,
        )
        zhang_xiao = next(item for item in merged if item["姓名"] == "张晓")
        self.assertEqual(
            zhang_xiao["科室_分类页"],
            "儿科（琶洲院区）、风湿免疫科（琶洲院区）",
        )
        self.assertEqual(zhang_xiao["来源链接"], "https://gd2h.com/site/detail/42041.html")
        zhang_hui = [item for item in merged if item["姓名"] == "张辉"]
        self.assertEqual(len(zhang_hui), 2)
        self.assertTrue(all("同名待甄别" in str(item["异常提示"]) for item in zhang_hui))
        self.assertTrue(all(item["重点优先级"] == "普通" for item in zhang_hui))
        self.assertTrue(all(not item["重点关注范围"] for item in zhang_hui))
        self.assertEqual(GD2H_EXPECTED_FINAL_IDENTITY_COUNT, 567)

    def test_full_is_authorised_but_requires_complete_payload(self) -> None:
        target = HospitalTarget(
            city="广州市",
            hospital="广东省第二人民医院",
            homepage="https://gd2h.com/",
            entry_url="https://gd2h.com/site/column/107_1_20.html",
            difficulty="D-待人工补官网",
            review="确认可采集",
            adapter_id=GD2H_ADAPTER_ID,
        )

        with patch(
            "collect_official_doctors_batch.create_official_session",
            side_effect=RuntimeError("FULL reached official network boundary"),
        ):
            with self.assertRaisesRegex(RuntimeError, "official network boundary"):
                collect_gd2h(target, "2026-08-14", full_mode=True)
        with self.assertRaisesRegex(RuntimeError, "缺少全量 payload"):
            validate_gd2h_full_append({})


if __name__ == "__main__":
    unittest.main()
