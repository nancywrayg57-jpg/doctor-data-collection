from __future__ import annotations

import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gdzy5413_photo_backfill_full as target


class FakeResult:
    def __init__(self, status: int, content_type: str = "text/html") -> None:
        self.status = status
        self.content_type = content_type
        self.final_url = "https://www.gdzy5413.com/resource"


class FakeSession:
    def __init__(self, results: list[FakeResult]) -> None:
        self.results = list(results)

    def get(self, _url: str, *, referer: str = "") -> FakeResult:
        del referer
        return self.results.pop(0)


class Gdzy5413PhotoBackfillFullTests(unittest.TestCase):
    def test_full_scope_reuses_ten_and_fetches_332(self) -> None:
        self.assertEqual(target.EXPECTED_SCOPE_COUNT, 342)
        self.assertEqual(target.EXPECTED_TRIAL_REUSE_COUNT, 10)
        self.assertEqual(target.EXPECTED_TRIAL_FAILURE_REUSE_COUNT, 0)
        self.assertEqual(target.EXPECTED_FRESH_COUNT, 332)
        self.assertEqual(
            set(target.FULL_FAILURE_STATES),
            {"详情不可达", "照片资源不可达", "无照片容器", "占位图"},
        )

    def test_specialist_analysis_uses_only_inline_portrait_background(self) -> None:
        source = "https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=699"
        html = """
        <div class="main_left_img">
          <div><div class="docimg_title">靳利利</div>
          <div class="docimg_ming"></div><div class="docimg_cover"></div>
          <div style="background:url(/UploadFiles/image/2014-2/doctor.jpg)"></div></div>
        </div><div class="keylist_bg"><img src="/style/images/logo.png"></div>
        """
        result = target.analyze_doctor_media(html, source, "靳利利")
        self.assertEqual(result.state, "")
        self.assertEqual(result.reference_count, 1)
        self.assertEqual(
            result.photo_url,
            "https://www.gdzy5413.com/UploadFiles/image/2014-2/doctor.jpg",
        )
        self.assertIn("main_left_img", result.template_signature)

    def test_person_name_comparison_ignores_official_page_whitespace(self) -> None:
        source = "https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=700"
        html = """
        <div class="main_left_img"><div><div class="docimg_title">汪 何</div>
        <div style="background:url(/UploadFiles/image/wang-he.jpg)"></div></div>
        </div><div class="keylist_bg"></div>
        """
        result = target.analyze_doctor_media(html, source, "汪何")
        self.assertEqual(result.state, "")
        self.assertIn("wang-he.jpg", result.photo_url)

    def test_ksdoctor_empty_upload_path_is_no_photo_container(self) -> None:
        source = (
            "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?"
            "bid=65&typeid=63&cid=65&ksid=63&id=370"
        )
        html = """
        <div><img src="/UploadFiles/image/" width="120px" height="155px"></div>
        <div>姓名：付亚斐<br>职称：中医师</div>
        """
        result = target.analyze_doctor_media(html, source, "付亚斐")
        self.assertEqual(result.state, "无照片容器")
        self.assertEqual(result.reference_count, 0)
        self.assertIn("/UploadFiles/image/", result.excluded_resources[0]["url"])

    def test_url_named_placeholder_is_classified_without_download(self) -> None:
        source = (
            "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?"
            "bid=47&typeid=45&cid=47&ksid=45&id=417"
        )
        html = """
        <div><img src="/UploadFiles/image/noimage.jpg" width="120px" height="155px"></div>
        <div>姓名：林谋清<br>职称：主治中医师</div>
        """
        result = target.analyze_doctor_media(html, source, "林谋清")
        self.assertEqual(result.state, "占位图")
        self.assertEqual(result.reference_count, 1)
        self.assertIn("noimage.jpg", result.excluded_resources[0]["url"])

    def test_response_content_gate_rejects_small_portrait_class_image(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (86, 126), "#dcecff").save(buffer, "JPEG", quality=70)
        reason = target.downloaded_placeholder_reason(
            "https://www.gdzy5413.com/UploadFiles/image/normal-name.jpg",
            buffer.getvalue(),
            "jpg",
        )
        self.assertIn("占位图", reason)

    def test_fetch_retries_three_times_with_30_second_intervals(self) -> None:
        sleeps: list[float] = []
        session = FakeSession([FakeResult(404), FakeResult(404), FakeResult(404)])
        result, attempts = target.fetch_with_retry(
            session,
            "https://www.gdzy5413.com/missing",
            target.trial.DIRECTORY_URL,
            lambda item: item.status == 200,
            sleep_func=sleeps.append,
        )
        self.assertEqual(result.status, 404)
        self.assertEqual(len(attempts), 3)
        self.assertEqual(sleeps, [30, 30])

    def test_profile_photo_refresh_is_exactly_plus_two_minus_zero(self) -> None:
        before = (
            "<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->\n"
            "# 靳利利\n\n## 基础信息\n\n- 医院：广东省第二中医院\n"
        ).encode("utf-8")
        photo_file = "01_试点医院/广东省第二中医院/照片/靳利利-心血管科-主任医师-广东省第二中医院.jpg"
        after = target.insert_profile_photo_block_bytes(before, "靳利利", photo_file)
        target.validate_profile_photo_only_bytes(before, after, "靳利利", photo_file)
        self.assertEqual(len(after.decode("utf-8").splitlines()), len(before.decode("utf-8").splitlines()) + 2)

    def test_filename_uses_keyword_title_and_collision_appends_detail_id(self) -> None:
        row = {
            "姓名": "测试医生",
            "科室": "内科、门诊",
            "职称_关键词": "主任医师",
            "职称身份原文": "医师",
        }
        with tempfile.TemporaryDirectory() as directory:
            used: set[str] = set()
            first, _ = target.allocate_full_photo_path(
                row, "417", "jpg", Path(directory), used
            )
            second, _ = target.allocate_full_photo_path(
                row, "418", "jpg", Path(directory), used
            )
        self.assertIn("主任医师", first)
        self.assertTrue(second.endswith("-418.jpg"))

    def test_audit_samples_cover_min_max_and_eight_deterministic_random(self) -> None:
        samples = [
            {
                "name": f"医生{index}",
                "source_link": f"https://www.gdzy5413.com/detail/{index}",
                "bytes": index + 1,
            }
            for index in range(12)
        ]
        selected = target.select_audit_samples(samples)
        self.assertEqual(len(selected), 10)
        self.assertEqual(
            {item["audit_kind"] for item in selected},
            {"最小", "最大", "确定性随机"},
        )
        self.assertEqual(target.select_audit_samples(samples), selected)

    def test_reconciliation_manifest_includes_failure_class_and_magic_format(self) -> None:
        payload = {
            "reconciliation": [
                {
                    "姓名": "靳利利",
                    "来源链接": "https://www.gdzy5413.com/detail/1",
                    "状态": "实采",
                    "失败分类": "",
                    "照片链接": "https://www.gdzy5413.com/UploadFiles/image/1.jpg",
                    "照片文件": "01_试点医院/广东省第二中医院/照片/1.jpg",
                    "实际格式": "jpg",
                    "字节数": 100,
                    "SHA-256": "a" * 64,
                    "宽": 120,
                    "高": 155,
                    "来源批次": "TRIAL_REUSE",
                    "错误证据": "",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.csv"
            target.write_full_reconciliation_csv(path, payload)
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle))
        self.assertEqual(row["失败分类"], "")
        self.assertEqual(row["实际格式"], "jpg")

    def test_resource_failure_blocker_keeps_url_reference_and_detection(self) -> None:
        failure = {
            "name": "测试医生",
            "source_link": "https://www.gdzy5413.com/detail/1",
            "state": "照片资源不可达",
            "evidence": {
                "resource_urls": ["https://www.gdzy5413.com/UploadFiles/image/1.jpg"],
                "photo_reference_count": 1,
                "detection_feature": "页面授权本人照片容器引用唯一；资源 404",
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            blocker = Path(directory) / "blocker.json"
            with patch.object(target, "FULL_BLOCKER_JSON_PATH", blocker):
                target.persist_resource_failure_blocker([failure] * 10)
            text = blocker.read_text(encoding="utf-8")
        self.assertIn("FULL_PAUSED_RESOURCE_FAILURE_BATCH", text)
        self.assertIn("photo_reference_count", text)


if __name__ == "__main__":
    unittest.main()
