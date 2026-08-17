from __future__ import annotations

import hashlib
import io
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from PIL import Image


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gy3y_photo_backfill_trial as trial  # noqa: E402


class Gy3yPhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_paths_are_relative_to_checkout(self) -> None:
        self.assertEqual(trial.ROOT, Path(__file__).resolve().parents[2])
        self.assertEqual(trial.ISSUE_NUMBER, 65)
        self.assertEqual(trial.EXPECTED_SCOPE_COUNT, 422)
        self.assertEqual(trial.KNOWN_UNREACHABLE_SCOPE, (("李文杰", "6"),))

    def test_html_mime_guard_accepts_only_html_shaped_text(self) -> None:
        self.assertTrue(
            trial.is_html_document("text/plain", b"<html><head><title>x</title></head></html>")
        )
        self.assertTrue(trial.is_html_document("text/html", b"<!doctype html><html></html>"))
        self.assertFalse(trial.is_html_document("text/plain", b"plain text"))
        self.assertFalse(trial.is_html_document("application/json", b"<html></html>"))

    def test_detail_url_and_two_page_referenced_styles(self) -> None:
        source = "https://www.gy3y.cn/ks/nk/hxnk/doctor_1.html"
        self.assertEqual(trial.detail_id(source), "1")
        self.assertEqual(
            trial.page_referenced_photo_url(
                "/Upload/202112/637750146771733237.jpg", source
            ),
            (
                "https://www.gy3y.cn/Upload/202112/637750146771733237.jpg",
                "Upload原图",
            ),
        )
        self.assertEqual(
            trial.page_referenced_photo_url("/images/doctor/LAIKEFANG.jpg", source),
            (
                "https://www.gy3y.cn/images/doctor/LAIKEFANG.jpg",
                "doctor原图",
            ),
        )

    def test_rejects_query_third_party_and_unapproved_paths(self) -> None:
        source = "https://www.gy3y.cn/ks/nk/hxnk/doctor_1.html"
        for value in (
            "/Upload/202112/637750146771733237.jpg?v=1",
            "https://example.com/Upload/202112/637750146771733237.jpg",
            "/Upload/202106/zhongnanshan-lab.png",
            "/images/news/zhongnanshan.jpg",
        ):
            self.assertEqual(trial.page_referenced_photo_url(value, source), ("", ""))
        self.assertEqual(
            trial.detail_id("https://www.gy3y.cn/ks/nk/hxnk/doctor_1.html?x=1"),
            "",
        )

    def test_exact_placeholder_path_is_left_blank_without_admin_claim(self) -> None:
        source = "https://www.gy3y.cn/ks/wkxt/pwyq/doctor_495.html"
        self.assertEqual(
            trial.page_referenced_photo_url("/html/images/doctor.jpg", source),
            (
                "https://www.gy3y.cn/html/images/doctor.jpg",
                "精确路径占位图",
            ),
        )
        state, portrait = trial.inspect_portrait_reference(
            """
            <title>王军伟_普外一区（肝胆外科）_广州医科大学附属第三医院</title>
            <div class="photo"><img src="/html/images/doctor.jpg"></div>
            """,
            source,
            "王军伟",
        )
        self.assertEqual(state, "占位图")
        self.assertIsNone(portrait)
        self.assertEqual(
            trial.page_referenced_photo_url("/html/images/doctor-2.jpg", source),
            ("", ""),
        )

    def test_five_round_aggregate_probes_all_sources_and_freezes_first_photo(self) -> None:
        unreachable = "https://www.gy3y.cn/ks/nkxt/jsyxk/doctor_12.html"
        recovered = "https://www.gy3y.cn/ks/wkxt/gkeq/doctor_310.html"
        empty = "https://www.gy3y.cn/ks/nkxt/jsyxk/doctor_190.html"
        photo_a = "https://www.gy3y.cn/Upload/202003/6371942997440786323463805.jpg"
        photo_b = "https://www.gy3y.cn/Upload/202003/6371942997440786323463806.jpg"
        not_found_html = b"<html><head><title>404</title></head><body></body></html>"
        recovered_html_a = (
            "<html><head><title>王钊_骨科二区_广州医科大学附属第三医院</title></head>"
            '<body><div class="photo"><img src="/Upload/202003/6371942997440786323463805.jpg"></div></body></html>'
        ).encode("utf-8")
        recovered_html_b = recovered_html_a.replace(
            b"6371942997440786323463805.jpg",
            b"6371942997440786323463806.jpg",
        )
        empty_html = (
            "<html><head><title>麦伟文_神经内科_广州医科大学附属第三医院</title></head>"
            '<body><div class="photo"></div></body></html>'
        ).encode("utf-8")
        first_photo_buffer = io.BytesIO()
        Image.new("RGB", (19, 23), "navy").save(first_photo_buffer, format="JPEG")
        first_photo = first_photo_buffer.getvalue()
        sessions: list[FakeSession] = []

        class FakeSession:
            def __init__(self, round_index: int) -> None:
                self.round_index = round_index
                self.calls: list[str] = []
                self.last_status_trace: tuple[int, ...] = ()
                self.incomplete_read_retry_count = 0

            def get(self, url: str, referer: str = "") -> tuple[int, str, str, bytes]:
                self.calls.append(url)
                if url == trial.OFFICIAL_HOME:
                    self.last_status_trace = (200,)
                    return 200, "text/html", "utf-8", b"<html></html>"
                if url == unreachable:
                    self.last_status_trace = (302, 404)
                    return 404, "text/html", "utf-8", not_found_html
                if url == empty:
                    if self.round_index == 0:
                        self.last_status_trace = (200,)
                        return 200, "text/html", "utf-8", empty_html
                    self.last_status_trace = (302, 404)
                    return 404, "text/html", "utf-8", not_found_html
                if url == recovered:
                    if self.round_index == 0:
                        self.last_status_trace = (302, 404)
                        return 404, "text/html", "utf-8", not_found_html
                    self.last_status_trace = (302, 200)
                    content = recovered_html_a if self.round_index == 1 else recovered_html_b
                    return 200, "text/html", "utf-8", content
                if url == photo_a:
                    self.last_status_trace = (200,)
                    return 200, "image/jpeg", "utf-8", first_photo
                if url == photo_b:
                    raise AssertionError("后续轮不得下载或覆盖已冻结照片")
                raise AssertionError(f"unexpected URL {url}")

        now = [0.0]

        def sleeper(seconds: float) -> None:
            now[0] += seconds

        def session_factory() -> FakeSession:
            session = FakeSession(len(sessions))
            sessions.append(session)
            return session

        started = datetime(2026, 8, 17, 11, 20, tzinfo=timezone.utc)
        aggregate = trial.collect_detail_retry_results(
            [
                {"姓名": "周伯荣", "来源链接": unreachable},
                {"姓名": "王钊", "来源链接": recovered},
                {"姓名": "麦伟文", "来源链接": empty},
            ],
            session_factory=session_factory,  # type: ignore[arg-type]
            sleeper=sleeper,
            monotonic=lambda: now[0],
            utcnow=lambda: started + timedelta(seconds=now[0]),
        )
        results = aggregate.by_source
        self.assertEqual(results[unreachable]["state"], "详情不可达")
        self.assertEqual(results[unreachable]["round_count"], 5)
        self.assertEqual(results[unreachable]["evidence"].count("HTTP 302→404@"), 5)
        self.assertEqual(results[recovered]["state"], "")
        self.assertEqual(results[recovered]["round_count"], 5)
        self.assertEqual(results[recovered]["captured_round"], 2)
        captured = results[recovered]["captured_photo"]
        self.assertIsInstance(captured, trial.CapturedPhoto)
        self.assertEqual(captured.content, first_photo)
        self.assertEqual(captured.portrait.photo_url, photo_a)
        self.assertIn("后续轮不覆盖", results[recovered]["evidence"])
        self.assertEqual(results[empty]["state"], "无照片容器")
        self.assertEqual(len(sessions), 5)
        self.assertTrue(all(trial.OFFICIAL_HOME in item.calls for item in sessions))
        self.assertTrue(all(unreachable in item.calls for item in sessions))
        self.assertTrue(all(recovered in item.calls for item in sessions))
        self.assertTrue(all(empty in item.calls for item in sessions))
        self.assertEqual(sum(item.calls.count(photo_a) for item in sessions), 1)
        self.assertEqual(sum(item.calls.count(photo_b) for item in sessions), 0)
        self.assertEqual(aggregate.total_detail_probes, 15)
        self.assertEqual(aggregate.round_intervals_seconds, [60.0] * 4)
        self.assertEqual(
            aggregate.round_start_utc,
            [
                "2026-08-17T11:20:00Z",
                "2026-08-17T11:21:00Z",
                "2026-08-17T11:22:00Z",
                "2026-08-17T11:23:00Z",
                "2026-08-17T11:24:00Z",
            ],
        )

    def test_recording_redirect_handler_retains_original_status(self) -> None:
        from urllib.request import Request

        handler = trial.RecordingRedirectHandler()
        redirected = handler.redirect_request(
            Request("https://www.gy3y.cn/original"),
            None,
            302,
            "Found",
            {},
            "https://www.gy3y.cn/final",
        )
        self.assertIsNotNone(redirected)
        self.assertEqual(handler.status_codes, [302])

    def test_parser_uses_only_unique_photo_container(self) -> None:
        source = "https://www.gy3y.cn/ks/nk/hxnk/doctor_1.html"
        html = """
        <html><head><title>许治强_呼吸与危重症医学科_广州医科大学附属第三医院官方网站www.gyfyy.com</title></head>
        <body>
          <img src="/Upload/202106/zhongnanshan-lab.png">
          <div class="photo"><img src="/Upload/202112/637750146771733237.jpg"></div>
          <div class="floatcard"><img src="/Upload/202112/637750146771733237.jpg"></div>
        </body></html>
        """
        state, portrait = trial.inspect_portrait_reference(html, source, "许治强")
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)
        assert portrait is not None
        self.assertEqual(portrait.reference_kind, "Upload原图")
        self.assertEqual(
            portrait.photo_url,
            "https://www.gy3y.cn/Upload/202112/637750146771733237.jpg",
        )
        self.assertEqual(portrait.template_signature, "div.photo img")

    def test_parser_accepts_doctor_style_and_rejects_ambiguous_container(self) -> None:
        source = "https://www.gy3y.cn/ks/nk/hxnk/doctor_9.html"
        html = """
        <title>张建瑜_呼吸与危重症医学科_广州医科大学附属第三医院官方网站www.gyfyy.com</title>
        <div class="doctor-card photo"><img src="/images/doctor/LAIKEFANG.jpg"></div>
        """
        state, portrait = trial.inspect_portrait_reference(html, source, "张建瑜")
        self.assertEqual(state, "")
        assert portrait is not None
        self.assertEqual(portrait.reference_kind, "doctor原图")
        with self.assertRaisesRegex(RuntimeError, "div.photo 容器不唯一"):
            trial.inspect_portrait_reference(
                html + '<div class="photo"><img src="/images/doctor/OTHER.jpg"></div>',
                source,
                "张建瑜",
            )

    def test_scope_and_fixed_sample_plan_are_stable(self) -> None:
        rows = trial.load_scope_rows(require_blank_photo_fields=False)
        selected = trial.select_trial_rows(rows)
        self.assertEqual(len(rows), 422)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(
            len({trial.atomic_department(row) for row in selected}), 10
        )
        levels = [trial.title_level(row.get("职称身份原文")) for row in selected]
        self.assertEqual(levels.count("正高"), 3)
        self.assertEqual(levels.count("副高"), 3)
        self.assertEqual(levels.count("其他"), 4)

    def test_small_gray_or_marked_gif_is_placeholder(self) -> None:
        gray = Image.new("RGB", (40, 40), (235, 235, 235))
        buffer = io.BytesIO()
        gray.save(buffer, format="GIF")
        content = buffer.getvalue()
        self.assertLess(len(content), trial.SMALL_GIF_PLACEHOLDER_BYTES)
        self.assertIn(
            "占位图",
            trial.downloaded_placeholder_reason(
                "https://www.gy3y.cn/images/doctor/avatar.gif", content, "gif"
            ),
        )

    def test_colorful_small_gif_and_large_gif_are_not_format_placeholders(self) -> None:
        colorful = Image.new("RGB", (30, 30), (0, 80, 220))
        buffer = io.BytesIO()
        colorful.save(buffer, format="GIF")
        content = buffer.getvalue()
        self.assertEqual(
            trial.downloaded_placeholder_reason(
                "https://www.gy3y.cn/images/doctor/doctor.gif", content, "gif"
            ),
            "",
        )
        large_gif = b"GIF89a" + b"x" * trial.SMALL_GIF_PLACEHOLDER_BYTES
        self.assertEqual(
            trial.downloaded_placeholder_reason(
                "https://www.gy3y.cn/images/doctor/portrait.gif", large_gif, "gif"
            ),
            "",
        )

    def test_magic_dimensions_and_filename_policy(self) -> None:
        image = Image.new("RGB", (17, 23), (20, 40, 60))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        content = buffer.getvalue()
        self.assertEqual(trial.magic_extension(content, "image/png"), "png")
        self.assertEqual(trial.image_dimensions(content), (17, 23))
        row = {
            "姓名": "测试医生",
            "科室_分类页": "测试科",
            "职称身份原文": "副主任医师",
            "来源链接": "https://www.gy3y.cn/ks/nk/test/doctor_999.html",
        }
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(trial, "TRIAL_PHOTO_DIR", Path(directory)):
                filename, path = trial.allocate_trial_photo(row, "png", content)
                self.assertEqual(
                    filename,
                    "测试医生-测试科-副主任医师-广州医科大学附属第三医院.png",
                )
                self.assertEqual(path.parent, Path(directory))

    def test_size_buckets_cover_owner_reporting_and_fuse_boundary(self) -> None:
        self.assertEqual(trial.size_bucket(100), "<200KiB")
        self.assertEqual(trial.size_bucket(300 * 1024), "200KiB-1MiB")
        self.assertEqual(trial.size_bucket(2 * 1024 * 1024), "1-5MiB")
        self.assertEqual(trial.size_bucket(6 * 1024 * 1024), "5-20MiB")
        self.assertEqual(trial.size_bucket(21 * 1024 * 1024), ">20MiB")

    def test_abnormal_format_and_over_20mib_are_immediate_fuses(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "格式不受支持"):
            trial.enforce_photo_policy(
                "测试医生", "https://www.gy3y.cn/images/doctor/TEST.bmp", "", 100
            )
        with self.assertRaisesRegex(RuntimeError, "超过 20 MiB"):
            trial.enforce_photo_policy(
                "测试医生",
                "https://www.gy3y.cn/images/doctor/TEST.jpg",
                "jpg",
                trial.FULL_FUSE_BYTES + 1,
            )


    def test_internal_404_title_is_detail_unreachable(self) -> None:
        source = "https://www.gy3y.cn/ks/nk/hxnk/doctor_6.html"
        state, portrait = trial.inspect_portrait_reference(
            "<html><head><title>404</title></head><body></body></html>",
            source,
            "李文杰",
        )
        self.assertEqual(state, "详情不可达")
        self.assertIsNone(portrait)

    def test_parser_tolerates_official_title_space_before_separator(self) -> None:
        source = "https://www.gy3y.cn/ks/wkxt/qgyzk/doctor_307.html"
        html = """
        <title>赵国志 _器官移植科_广州医科大学附属第三医院</title>
        <div class="photo"><img src="/Upload/202112/637750146771733237.jpg"></div>
        """
        state, portrait = trial.inspect_portrait_reference(html, source, "赵国志")
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)

    def test_full_authorization_and_failure_warning_are_explicit(self) -> None:
        self.assertIn("PR #66", trial.FULL_AUTHORIZATION)
        self.assertIn("FULL_APPEND_AND_OBSIDIAN", trial.FULL_AUTHORIZATION)
        self.assertIn("422 行全量", trial.FULL_AUTHORIZATION)
        self.assertNotIn("管理员确认", trial.FULL_AUTHORIZATION)
        self.assertFalse(hasattr(trial, "stage_ledger_assets"))
        self.assertEqual(len(trial.FULL_PROTECTED_FILES), 4)
        warning = trial.append_failure_warning("既有提示", "无照片容器")
        self.assertEqual(
            warning,
            f"既有提示；{trial.FULL_WARNING_BY_STATE['无照片容器']}",
        )
        self.assertEqual(trial.append_failure_warning(warning, "无照片容器"), warning)
        self.assertEqual(
            trial.replace_failure_warning(
                "既有提示；官网本人职业照补录失败：详情不可达",
                "详情不可达",
                "无照片容器",
            ),
            "既有提示；官网本人职业照补录失败：无照片容器",
        )

    def test_reconstruct_pre_full_rows_reverses_only_recorded_diffs(self) -> None:
        source = "https://www.gy3y.cn/ks/nkxt/jsyxk/doctor_12.html"
        installed = [
            {
                "来源链接": source,
                "照片链接": "https://www.gy3y.cn/Upload/201411/example.jpg",
                "照片文件": "01_试点医院/广州医科大学附属第三医院/照片/example.jpg",
                "异常提示": "既有提示",
            },
            {"来源链接": "https://example.com/outside", "照片链接": "保持"},
        ]
        payload = {
            "row_diffs": [
                {
                    "来源链接": source,
                    "列名": "照片链接",
                    "修改前": "",
                    "修改后": installed[0]["照片链接"],
                },
                {
                    "来源链接": source,
                    "列名": "照片文件",
                    "修改前": "",
                    "修改后": installed[0]["照片文件"],
                },
            ]
        }
        before = trial.reconstruct_pre_full_rows(installed, payload, {source})
        self.assertEqual(before[0]["照片链接"], "")
        self.assertEqual(before[0]["照片文件"], "")
        self.assertEqual(before[0]["异常提示"], "既有提示")
        self.assertEqual(before[1], installed[1])
        self.assertEqual(installed[0]["照片链接"], "https://www.gy3y.cn/Upload/201411/example.jpg")

    def test_full_row_diff_allows_only_target_photo_columns(self) -> None:
        source = "https://www.gy3y.cn/cn/ks/nk/hxnk/doctor_1.html"
        before = [
            {
                "来源链接": source,
                "照片链接": "",
                "照片文件": "",
                "异常提示": "",
                "姓名": "钟南山",
            }
        ]
        after = [{**before[0], "照片链接": "https://www.gy3y.cn/images/doctor/A.jpg"}]
        diffs = trial.collect_full_row_diffs(before, after, {source})
        self.assertEqual([item["列名"] for item in diffs], ["照片链接"])
        with self.assertRaisesRegex(RuntimeError, "范围外行"):
            trial.collect_full_row_diffs(before, after, set())
        with self.assertRaisesRegex(RuntimeError, "范围外字段"):
            trial.collect_full_row_diffs(
                before, [{**before[0], "姓名": "错误"}], {source}
            )
    def test_full_filename_uses_detail_id_only_for_collision(self) -> None:
        row = {
            "姓名": "同名",
            "科室_分类页": "内科",
            "职称身份原文": "主任医师",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            used: set[str] = set()
            first, _ = trial.allocate_full_photo_path(row, "100", "jpg", root, used)
            second, _ = trial.allocate_full_photo_path(row, "101", "jpg", root, used)
        self.assertEqual(first, "同名-内科-主任医师-广州医科大学附属第三医院.jpg")
        self.assertEqual(
            second,
            "同名-内科-主任医师-广州医科大学附属第三医院-101.jpg",
        )
    def test_profile_photo_insert_preserves_bom_newlines_and_other_bytes(self) -> None:
        before = (
            b"\xef\xbb\xbf---\r\nprotected: true\r\n---\r\n\r\n# Doctor\r\n\r\n"
            + "## 基础信息\r\n\r\n".encode("utf-8")
            + b"| field | value |\r\n|---|---|\r\n| x | y |\r\n"
        )
        photo_file = (
            "01_试点医院/广州医科大学附属第三医院/照片/"
            "钟南山-呼吸与危重症医学科-主任医师-广州医科大学附属第三医院.jpg"
        )
        after = trial.insert_profile_photo_block_bytes(before, "钟南山", photo_file)
        expected = (
            "![钟南山](照片/钟南山-呼吸与危重症医学科-主任医师-"
            "广州医科大学附属第三医院.jpg)\r\n\r\n"
        ).encode("utf-8")
        self.assertTrue(after.startswith(b"\xef\xbb\xbf"))
        self.assertEqual(
            after,
            before.replace(
                "## 基础信息\r\n\r\n".encode("utf-8"),
                "## 基础信息\r\n\r\n".encode("utf-8") + expected,
            ),
        )
        trial.validate_profile_photo_only_bytes(before, after, "钟南山", photo_file)
        with self.assertRaisesRegex(RuntimeError, "已存在照片"):
            trial.insert_profile_photo_block_bytes(after, "钟南山", photo_file)
    def test_full_validator_closes_422_rows_with_three_failure_states(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (8, 9), "blue").save(buffer, format="JPEG")
        content = buffer.getvalue()
        digest = hashlib.sha256(content).hexdigest()
        success_count = trial.EXPECTED_SCOPE_COUNT - 22
        failed_count = trial.EXPECTED_SCOPE_COUNT - success_count
        rows = []
        reconciliation = []
        photos = []
        with tempfile.TemporaryDirectory() as directory:
            photo_root = Path(directory)
            owner_union_ids = sorted(
                trial.OWNER_THREE_ROUND_UNION_SOURCE_IDS, key=int
            )
            for index in range(trial.EXPECTED_SCOPE_COUNT):
                source_id = (
                    owner_union_ids[index]
                    if index < len(owner_union_ids)
                    else str(10000 + index)
                )
                source = (
                    "https://www.gy3y.cn/ks/nk/test/"
                    f"doctor_{source_id}.html"
                )
                if index < success_count:
                    filename = f"医生{index}.jpg"
                    photo_url = f"https://www.gy3y.cn/images/doctor/DOCTOR{index}.jpg"
                    photo_file = f"01_试点医院/{trial.HOSPITAL}/照片/{filename}"
                    (photo_root / filename).write_bytes(content)
                    rows.append(
                        {
                            "来源链接": source,
                            "照片链接": photo_url,
                            "照片文件": photo_file,
                            "异常提示": "",
                        }
                    )
                    photos.append(
                        {
                            "source_link": source,
                            "photo_url": photo_url,
                            "photo_file": photo_file,
                            "filename": filename,
                            "bytes": len(content),
                            "sha256": digest,
                            "magic_hex": content[:12].hex().upper(),
                            "width": 8,
                            "height": 9,
                            "reference_kind": "doctor原图",
                        }
                    )
                    reconciliation.append(
                        {
                            "来源链接": source,
                            "状态": "实采",
                            "失败三态": "",
                        }
                    )
                else:
                    state = trial.FULL_FAILURE_STATES[
                        (index - success_count) % len(trial.FULL_FAILURE_STATES)
                    ]
                    rows.append(
                        {
                            "来源链接": source,
                            "照片链接": "",
                            "照片文件": "",
                            "异常提示": trial.FULL_WARNING_BY_STATE[state],
                        }
                    )
                    reconciliation.append(
                        {
                            "来源链接": source,
                            "状态": "失败",
                            "失败三态": state,
                        }
                    )
            state_counts = {
                state: sum(item.get("失败三态") == state for item in reconciliation)
                for state in trial.FULL_FAILURE_STATES
            }
            probe_sources = [
                item["来源链接"] for item in reconciliation[:66]
            ]
            probe_evidence = "；".join(
                f"第 {round_number} 轮 HTTP 302→200@2026-08-17T12:0{round_number - 1}:00Z"
                for round_number in range(1, trial.DETAIL_PROBE_ROUNDS + 1)
            )
            photos_by_source = {item["source_link"]: item for item in photos}
            for item in reconciliation[:66]:
                item["错误证据"] = probe_evidence
                photo = photos_by_source[item["来源链接"]]
                photo["detail_probe_evidence"] = probe_evidence
                photo["detail_probe_round_count"] = trial.DETAIL_PROBE_ROUNDS
                photo["captured_round"] = 1
            payload = {
                "meta": {
                    "expected_count": trial.EXPECTED_SCOPE_COUNT,
                    "downloaded_count": success_count,
                    "failed_count": failed_count,
                    "blank_count": failed_count,
                    "failure_state_counts": state_counts,
                    "constructed_unreferenced_probe_count": 0,
                    "third_party_source_count": 0,
                    "existing_profile_count": trial.EXPECTED_PROFILE_COUNT,
                    "no_profile_scope_count": 0,
                    "profile_refreshed_count": success_count,
                    "photo_total_bytes": len(content) * success_count,
                    "photo_max_bytes": len(content),
                    "over_5mib_count": 0,
                    "over_20mib_count": 0,
                    "size_bucket_counts": {trial.size_bucket(len(content)): success_count},
                    "reference_kind_counts": {"doctor原图": success_count},
                    "detail_probe_policy": "test five-round aggregate",
                    "detail_probe_sources": probe_sources,
                    "detail_probe_source_count": 66,
                    "detail_probe_round_count": trial.DETAIL_PROBE_ROUNDS,
                    "detail_probe_total_requests": 66 * trial.DETAIL_PROBE_ROUNDS,
                    "detail_probe_round_start_utc": [
                        f"2026-08-17T12:0{index}:00Z"
                        for index in range(trial.DETAIL_PROBE_ROUNDS)
                    ],
                    "detail_probe_round_intervals_seconds": [60.0] * 4,
                    "detail_probe_home_evidence": [
                        f"第 {index + 1} 轮首页 HTTP 200@2026-08-17T12:0{index}:00Z"
                        for index in range(trial.DETAIL_PROBE_ROUNDS)
                    ],
                    "owner_three_round_union_comparison": [
                        {
                            "detail_id": source_id,
                            "source_link": next(
                                source
                                for source in probe_sources
                                if trial.detail_id(source) == source_id
                            ),
                            "result": "实采",
                            "captured_round": 1,
                        }
                        for source_id in owner_union_ids
                    ],
                },
                "rows": rows,
                "reconciliation": reconciliation,
                "photo_samples": photos,
            }
            trial.validate_full_payload(payload, photo_root)

if __name__ == "__main__":
    unittest.main()
