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

from collect_official_doctors_batch import (  # noqa: E402
    GZTCM_ADAPTER_ID,
    GZTCM_EXPECTED_CATEGORY_COUNTS,
    GZTCM_EXPECTED_CATEGORY_RELATION_COUNTS,
    GZTCM_FAMOUS_URL,
    GZTCM_PHOTO_INVALID_WARNING,
    GZTCM_PHOTO_RETRY_POLICY,
    GZTCM_SCOPE_TREE_URL,
    decode_gztcm_html,
    dedicated_adapter_for,
    download_gztcm_photo,
    gztcm_detail_id,
    gztcm_paging_metadata,
    gztcm_photo_url,
    parse_gztcm_detail,
    parse_gztcm_list_page,
    parse_gztcm_scope_tree,
    select_gztcm_trial_doctors,
    validate_gztcm_full_append,
    validate_gztcm_trial,
)


def png_bytes(width: int, height: int) -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\rIHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x02\x00\x00\x00"
    )


class GztcmPhotoTrialTests(unittest.TestCase):
    def test_exact_entry_detail_photo_and_utf8(self) -> None:
        tree_detail = "https://www.gztcm.com.cn/pwb/kszj/a123.shtml"
        famous_detail = "https://www.gztcm.com.cn/myzl/myhc/b456.shtml"

        self.assertEqual(dedicated_adapter_for(GZTCM_FAMOUS_URL), GZTCM_ADAPTER_ID)
        self.assertNotEqual(
            dedicated_adapter_for(f"{GZTCM_FAMOUS_URL}?_page_=1"), GZTCM_ADAPTER_ID
        )
        self.assertEqual(gztcm_detail_id(tree_detail), "a123")
        self.assertEqual(gztcm_detail_id(famous_detail), "b456")
        self.assertEqual(gztcm_detail_id(f"{tree_detail}?from=search"), "")
        self.assertEqual(gztcm_detail_id("https://example.com/pwb/kszj/a123.shtml"), "")
        self.assertEqual(
            gztcm_photo_url(
                "/export/sites/default/gztcm/pwb/kszj/resource/a123.JPG",
                tree_detail,
            ),
            "https://www.gztcm.com.cn/export/sites/default/gztcm/pwb/kszj/resource/a123.JPG",
        )
        self.assertEqual(
            gztcm_photo_url(
                "/export/sites/default/gztcm/myzl/myhc/resource/b456.png",
                famous_detail,
            ),
            "https://www.gztcm.com.cn/export/sites/default/gztcm/myzl/myhc/resource/b456.png",
        )
        self.assertEqual(gztcm_photo_url("https://example.com/a.jpg", tree_detail), "")
        self.assertEqual(
            gztcm_photo_url(
                "/export/sites/default/gztcm/pwb/kszj/resource/default.jpg",
                tree_detail,
            ),
            "",
        )
        self.assertEqual(decode_gztcm_html("广州中医药大学".encode("utf-8")), "广州中医药大学")
        with self.assertRaises(UnicodeDecodeError):
            decode_gztcm_html(b"\xff")

    def test_scope_tree_paging_and_dual_channel_list_parsers(self) -> None:
        html = """
        <!-- <a href="/ksjs/nk/">大内科</a><a href="/ksjs/wk/">大外科</a> -->
        <section><div class="department_name">大内科</div>
          <a href="/pwb/" title="脾胃病科">脾胃病科</a>
          <a href="/hxk/" title="呼吸科">呼吸科</a>
        </section>
        <section><div class="department_name">大外科</div>
          <a href="/ptwk/" title="普通外科">普通外科</a>
        </section>
        """
        categories, departments = parse_gztcm_scope_tree(html)
        self.assertEqual(
            [(item["category_name"], item["department_count"]) for item in categories],
            [("大内科", 2), ("大外科", 1)],
        )
        self.assertEqual(categories[0]["category_url"], "https://www.gztcm.com.cn/ksjs/nk/")
        self.assertEqual(departments[0]["directory_url"], "https://www.gztcm.com.cn/pwb/kszj/")

        paging = "var p = {'size':20,'page':1,'itemCount':2,'pageCount':1};"
        self.assertEqual(
            gztcm_paging_metadata(paging),
            {"size": 20, "page": 1, "item_count": 2, "page_count": 1},
        )
        tree_html = """
        <div id="pageregion"><div class="list"><ul><li>
          <a href="a1.shtml" title="张甲"><img src="resource/a1.jpg"></a>
          <h4>张甲</h4><div class="title"><span>主任中医师</span></div>
          <div class="description">擅长：脾胃疾病诊疗</div>
        </li></ul></div></div>
        """
        tree_rows = parse_gztcm_list_page(
            tree_html,
            "https://www.gztcm.com.cn/pwb/kszj/index.html?_page_=1",
            "科室树",
            "大内科",
            "脾胃病科",
        )
        self.assertEqual(len(tree_rows), 1)
        self.assertEqual(tree_rows[0]["id"], "a1")
        self.assertEqual(tree_rows[0]["department"], "脾胃病科")
        self.assertEqual(tree_rows[0]["list_specialty"], "脾胃疾病诊疗")

        famous_html = """
        <div id="pageregion"><div class="list_ul"><ul><li>
          <a href="f1.shtml" title="李乙"><img src="resource/f1.png"></a>
          <h4>李乙</h4><div class="subtitle">主任中医师</div>
        </li></ul></div></div>
        """
        famous_rows = parse_gztcm_list_page(
            famous_html,
            "https://www.gztcm.com.cn/myzl/myhc/index.html?_page_=1",
            "名医荟萃",
        )
        self.assertEqual(len(famous_rows), 1)
        self.assertEqual(famous_rows[0]["id"], "f1")
        self.assertEqual(famous_rows[0]["department"], "")

    def test_detail_parser_cleans_schedule_patient_and_private_use_text(self) -> None:
        source = "https://www.gztcm.com.cn/pwb/kszj/a1.shtml"
        html = """
        <div class="zj-list details">
          <h3 class="title">张甲</h3><div class="subtitle">主任中医师</div>
          <img src="/export/sites/default/gztcm/pwb/kszj/resource/a1.jpg">
          <div class="description">擅长治疗复杂脾胃疾病。门诊时间：周一上午；
          患者王某治疗后排名第一。长期从事中医临床工作。</div>
        </div>
        """
        parsed = parse_gztcm_detail(
            html,
            {"name": "张甲", "source_link": source, "list_specialty": ""},
        )
        self.assertEqual(parsed["name"], "张甲")
        self.assertIn("主任中医师", parsed["title"])
        self.assertEqual(parsed["specialty"], "复杂脾胃疾病")
        self.assertNotIn("周一", parsed["profile_text"])
        self.assertNotIn("王某", parsed["profile_text"])
        self.assertNotIn("\ue06b", parsed["profile_text"])
        self.assertEqual(parsed["photo_state"], "available")
        self.assertGreaterEqual(parsed["private_use_character_exclusion_count"], 1)

    def test_trial_selector_keeps_same_name_different_ids_and_dual_channels(self) -> None:
        doctors = [
            {
                "id": "f1",
                "name": "同名甲",
                "channels": ["名医荟萃"],
                "departments": [],
            },
            {
                "id": "t1",
                "name": "同名甲",
                "channels": ["科室树"],
                "departments": ["科室甲"],
            },
        ]
        doctors.extend(
            {
                "id": f"t{index}",
                "name": f"张{chr(0x4E00 + index)}",
                "channels": ["科室树"],
                "departments": [f"科室{chr(0x4E00 + index)}"],
            }
            for index in range(2, 15)
        )
        selected = select_gztcm_trial_doctors(doctors, 10)
        self.assertEqual(len(selected), 10)
        self.assertTrue({"f1", "t1"}.issubset({item["id"] for item in selected}))
        self.assertTrue(any("名医荟萃" in item["channels"] for item in selected))
        self.assertGreaterEqual(
            len({department for item in selected for department in item["departments"]}), 3
        )

    def test_photo_download_retries_once_with_identical_request(self) -> None:
        source = "https://www.gztcm.com.cn/pwb/kszj/a1.shtml"
        photo_url = (
            "https://www.gztcm.com.cn/export/sites/default/gztcm/"
            "pwb/kszj/resource/a1.png"
        )
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
                result = download_gztcm_photo(
                    session,  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-脾胃病科-主任中医师-广州中医药大学第一附属医院",
                    "a1",
                    set(),
                )
        self.assertEqual(result["retry_count"], 1)
        self.assertEqual(len(session.calls), 2)
        self.assertEqual(session.calls[0], session.calls[1])
        sleep_mock.assert_called_once_with(1)

    def test_chunked_and_incomplete_read_failures_are_approved_blank(self) -> None:
        source = "https://www.gztcm.com.cn/pwb/kszj/a1.shtml"
        photo_url = (
            "https://www.gztcm.com.cn/export/sites/default/gztcm/"
            "pwb/kszj/resource/a1.png"
        )

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
                result = download_gztcm_photo(
                    session,  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-脾胃病科-主任中医师-广州中医药大学第一附属医院",
                    "a1",
                    set(),
                )
        self.assertTrue(result["approved_no_source"])
        self.assertEqual(result["approved_no_source_reason"], "bounded_transfer_failure")
        self.assertEqual(result["attempt_results"], ["ChunkedEncodingError", "IncompleteRead"])
        self.assertEqual(result["retry_count"], 1)
        sleep_mock.assert_called_once_with(1)

    def test_invalid_official_image_is_approved_blank_without_retry(self) -> None:
        source = "https://www.gztcm.com.cn/pwb/kszj/a1.shtml"
        photo_url = (
            "https://www.gztcm.com.cn/export/sites/default/gztcm/"
            "pwb/kszj/resource/a1.png"
        )

        class Response:
            status_code = 200
            content = b"<html>broken image</html>"
            headers = {"Content-Type": "text/html"}

        class Session:
            def get(self, url: str, *, headers: dict[str, str], timeout: int) -> Response:
                return Response()

        with patch("collect_official_doctors_batch.time.sleep") as sleep_mock:
            with tempfile.TemporaryDirectory() as directory:
                result = download_gztcm_photo(
                    Session(),  # type: ignore[arg-type]
                    photo_url,
                    source,
                    Path(directory),
                    "张甲-脾胃病科-主任中医师-广州中医药大学第一附属医院",
                    "a1",
                    set(),
                )
        self.assertTrue(result["approved_no_source"])
        self.assertEqual(result["approved_no_source_reason"], "invalid_official_image")
        self.assertEqual(result["retry_count"], 0)
        self.assertIn("不受支持", result["validation_error"])
        sleep_mock.assert_not_called()

    def _trial_payload(self, photo_root: Path) -> dict[str, object]:
        category_plan = [
            ("大内科", 13, [6, 6, 6]),
            ("大外科", 10, [6, 6]),
            ("妇儿中心", 7, [2]),
            ("骨伤中心", 13, []),
            ("针灸推拿康复中心", 3, [3]),
            ("肿瘤中心", 5, []),
            ("脑病中心", 2, []),
            ("急诊中心", 2, []),
            ("其他", 15, [3, 3]),
        ]
        departments: list[dict[str, object]] = []
        relations: list[dict[str, object]] = []
        categories: list[dict[str, object]] = []
        empty_remaining = 42
        dead_remaining = 19
        detail_number = 1
        department_number = 1
        for category_index, (category, total, chunks) in enumerate(category_plan, start=1):
            for local_index in range(total):
                department = f"{category}科室{chr(0x4E00 + local_index)}"
                department_path = f"d{department_number:03d}"
                department_url = f"https://www.gztcm.com.cn/{department_path}/"
                directory_url = f"{department_url}kszj/"
                relation_count = chunks[local_index] if local_index < len(chunks) else 0
                if relation_count:
                    status = 200
                    state = "公开专家目录"
                elif empty_remaining:
                    status = 200
                    state = "公开空专家目录"
                    empty_remaining -= 1
                else:
                    status = 404
                    state = "官网科室首页所链专家目录 HTTP 404"
                    dead_remaining -= 1
                unique_ids: list[str] = []
                for _ in range(relation_count):
                    detail_id = f"t{detail_number:03d}"
                    source = f"{directory_url}{detail_id}.shtml"
                    unique_ids.append(detail_id)
                    relations.append(
                        {
                            "id": detail_id,
                            "name": f"张{chr(0x4E00 + detail_number)}",
                            "source_link": source,
                            "channel": "科室树",
                            "category": category,
                            "department": department,
                        }
                    )
                    detail_number += 1
                departments.append(
                    {
                        "category": category,
                        "department": department,
                        "department_url": department_url,
                        "directory_url": directory_url,
                        "http_status": status,
                        "page_count": 1 if status == 200 else 0,
                        "relation_count": relation_count,
                        "unique_detail_ids": unique_ids,
                        "directory_state": state,
                    }
                )
                department_number += 1
            categories.append(
                {
                    "category_index": category_index,
                    "category_name": category,
                    "category_url": f"https://www.gztcm.com.cn/ksjs/c{category_index}/",
                    "department_count": total,
                    "row_count": GZTCM_EXPECTED_CATEGORY_RELATION_COUNTS[category],
                }
            )
        self.assertEqual(empty_remaining, 0)
        self.assertEqual(dead_remaining, 0)
        self.assertEqual(len(relations), 41)

        for index in range(1, 42):
            detail_id = f"f{index:03d}"
            relations.append(
                {
                    "id": detail_id,
                    "name": f"李{chr(0x4E40 + index)}",
                    "source_link": f"{GZTCM_FAMOUS_URL}{detail_id}.shtml",
                    "channel": "名医荟萃",
                    "category": "",
                    "department": "",
                }
            )

        details: list[dict[str, object]] = []
        relation_by_id = {str(item["id"]): item for item in relations}
        for item in relations:
            detail_id = str(item["id"])
            details.append(
                {
                    "detail_id": detail_id,
                    "directory_name": item["name"],
                    "detail_name": item["name"],
                    "name_matches_directory": True,
                    "channels": [item["channel"]],
                    "categories": [item["category"]] if item["category"] else [],
                    "departments": [item["department"]] if item["department"] else [],
                    "title": "主任中医师",
                    "campuses": [],
                    "photo_state": "available",
                    "photo_url": (
                        "https://www.gztcm.com.cn/export/sites/default/gztcm/"
                        f"myzl/myhc/resource/{detail_id}.png"
                    ),
                    "source_link": item["source_link"],
                    "channel_audit": [
                        {
                            "source_link": item["source_link"],
                            "detail_status": 200,
                            "detail_error": "",
                            "detail_name": item["name"],
                        }
                    ],
                    "resolution": "详情已读取",
                }
            )

        selected_ids = ["f001", "t001", "t007", "t013", "t019", "t025", "t031", "t034", "t037", "t040"]
        selected_details = [next(item for item in details if item["detail_id"] == value) for value in selected_ids]
        content = png_bytes(640, 480)
        rows: list[dict[str, object]] = []
        photos: list[dict[str, object]] = []
        selected_tree_departments: list[str] = []
        for index, detail in enumerate(selected_details, start=1):
            detail_id = str(detail["detail_id"])
            relation = relation_by_id[detail_id]
            department = str(relation["department"])
            if department and department not in selected_tree_departments:
                selected_tree_departments.append(department)
            source = str(relation["source_link"])
            name = str(relation["name"])
            photo_url = str(detail["photo_url"])
            filename = f"{detail_id}.png"
            disk_path = photo_root / filename
            disk_path.write_bytes(content)
            relative = (
                Path("01_试点医院")
                / "广州中医药大学第一附属医院"
                / "照片"
                / filename
            ).as_posix()
            warning = "名医荟萃详情未标当前科室" if not department else ""
            rows.append(
                {
                    "序号": index,
                    "医院": "广州中医药大学第一附属医院",
                    "姓名": name,
                    "科室_分类页": department,
                    "科室_列表卡片": department,
                    "职称_关键词": "主任中医师",
                    "职称身份原文": "主任中医师",
                    "重点优先级": "普通",
                    "重点关注范围": "",
                    "重点疾病标签": "",
                    "擅长诊疗方向摘录": "中医临床诊疗",
                    "亮眼经历线索": "官网名医荟萃收录" if not department else "",
                    "列表简介": "",
                    "详情正文摘录": "长期从事中医临床工作。",
                    "来源类型": "医院官网",
                    "来源链接": source,
                    "照片链接": photo_url,
                    "照片文件": relative,
                    "采集入口": f"{GZTCM_SCOPE_TREE_URL} + {GZTCM_FAMOUS_URL}",
                    "采集方式": "官网科室树+名医荟萃",
                    "采集日期": "2026-08-15",
                    "详情页状态": "200",
                    "已建画像": "否",
                    "异常提示": warning,
                    "复核状态": "待人工复核",
                }
            )
            photos.append(
                {
                    "name": name,
                    "department": department or "未标注",
                    "title": "主任中医师",
                    "detail_id": detail_id,
                    "source_link": source,
                    "channels": [relation["channel"]],
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

        average = len(content)
        dead = [item for item in departments if item["http_status"] == 404]
        return {
            "meta": {
                "city": "广州市",
                "hospital": "广州中医药大学第一附属医院",
                "homepage": "https://www.gztcm.com.cn/gztcm/gzb.html",
                "entry_url": GZTCM_FAMOUS_URL,
                "adapter_id": GZTCM_ADAPTER_ID,
                "collected_at": "2026-08-15",
                "category_count": 10,
                "scope_category_count": 9,
                "pagination_count": 54,
                "census_department_count": 70,
                "census_dead_directory_count": 19,
                "census_empty_department_count": 42,
                "census_nonempty_department_count": 9,
                "department_relation_count": 41,
                "department_unique_detail_count": 41,
                "famous_relation_count": 41,
                "famous_page_count": 3,
                "department_famous_overlap_count": 0,
                "famous_only_detail_count": 41,
                "candidate_membership_count": 82,
                "unique_candidate_count": 82,
                "census_unique_detail_count": 82,
                "census_named_detail_count": 82,
                "census_blank_name_detail_count": 0,
                "census_unique_nonblank_name_count": 82,
                "census_same_name_group_count": 0,
                "cross_entry_duplicate_count": 0,
                "raw_card_rows": 82,
                "raw_person_rows": 82,
                "unique_doctor_count": 10,
                "excluded_non_doctor_count": 0,
                "eligible_candidate_count": 82,
                "detail_error_count": 0,
                "category_error_count": 0,
                "name_mismatch_count": 0,
                "encoding_replacement_count": 0,
                "encoding_mojibake_count": 0,
                "schedule_field_ingested_count": 0,
                "private_use_character_count": 0,
                "independent_entity_count": 0,
                "sample_entry_coverage_count": 2,
                "sample_entry_categories": ["名医荟萃", "科室树"],
                "sample_tree_department_coverage_count": len(selected_tree_departments),
                "sample_tree_departments": selected_tree_departments,
                "department_coverage_count": len(selected_tree_departments),
                "covered_departments": selected_tree_departments,
                "photo_expected_count": 10,
                "photo_sample_count": 10,
                "photo_downloaded_count": 10,
                "photo_failed_count": 0,
                "photo_no_source_count": 0,
                "photo_error_count": 0,
                "photo_bounded_retry_count": 0,
                "photo_retry_policy": GZTCM_PHOTO_RETRY_POLICY,
                "photo_census_available_count": 82,
                "photo_census_empty_count": 0,
                "photo_census_rejected_count": 0,
                "photo_average_bytes": average,
                "photo_estimated_full_count": 82,
                "photo_estimated_full_bytes": average * 82,
                "large_photo_count": 0,
                "photo_policy_status": "OWNER_APPROVED_ORIGINAL_NO_WIDTH_LIMIT",
                "category_relation_counts": dict(GZTCM_EXPECTED_CATEGORY_RELATION_COUNTS),
                "final_identity_count": 10,
                "execution_mode": "trial",
            },
            "categories": categories,
            "department_tree": departments,
            "gztcm_dead_directories": dead,
            "gztcm_channel_relations": relations,
            "gztcm_detail_reconciliation": details,
            "gztcm_sample_detail_reconciliation": selected_details,
            "same_name_groups": {},
            "excluded_candidates": [],
            "photo_samples": photos,
            "photo_no_sources": [],
            "photo_errors": [],
            "category_errors": [],
            "detail_errors": [],
            "rows": rows,
        }

    def test_trial_validator_closes_scope_details_photos_and_full_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            payload = self._trial_payload(Path(directory))
            validate_gztcm_trial(payload, expected_rows=10)  # type: ignore[arg-type]

            broken = copy.deepcopy(payload)
            broken["meta"]["census_department_count"] = 69  # type: ignore[index]
            with self.assertRaisesRegex(RuntimeError, "census_department_count"):
                validate_gztcm_trial(broken, expected_rows=10)  # type: ignore[arg-type]

            with self.assertRaisesRegex(RuntimeError, "FULL 授权证据未写入 payload"):
                validate_gztcm_full_append(payload)  # type: ignore[arg-type]

    def test_invalid_image_warning_constant_is_explicit(self) -> None:
        self.assertIn("留空", GZTCM_PHOTO_INVALID_WARNING)
        self.assertIn("仅重试 1 次", GZTCM_PHOTO_RETRY_POLICY)
        self.assertEqual(sum(GZTCM_EXPECTED_CATEGORY_COUNTS.values()), 70)


if __name__ == "__main__":
    unittest.main()
