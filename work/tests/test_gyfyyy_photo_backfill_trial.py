from __future__ import annotations

import io
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import gyfyyy_photo_backfill_trial as trial  # noqa: E402


class GyfyyyPhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_paths_are_relative_to_checkout(self) -> None:
        self.assertEqual(trial.ROOT, Path(__file__).resolve().parents[2])
        self.assertEqual(trial.ISSUE_NUMBER, 63)
        self.assertEqual(trial.EXPECTED_SCOPE_COUNT, 616)

    def test_detail_url_and_two_page_referenced_styles(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html"
        self.assertEqual(trial.detail_id(source), "1")
        self.assertEqual(
            trial.page_referenced_photo_url(
                "/Upload/202112/637750146771733237.jpg", source
            ),
            (
                "https://www.gyfyyy.cn/Upload/202112/637750146771733237.jpg",
                "Upload原图",
            ),
        )
        self.assertEqual(
            trial.page_referenced_photo_url("/images/doctor/LAIKEFANG.jpg", source),
            (
                "https://www.gyfyyy.cn/images/doctor/LAIKEFANG.jpg",
                "doctor原图",
            ),
        )

    def test_rejects_query_third_party_and_unapproved_paths(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html"
        for value in (
            "/Upload/202112/637750146771733237.jpg?v=1",
            "https://example.com/Upload/202112/637750146771733237.jpg",
            "/Upload/202106/zhongnanshan-lab.png",
            "/images/news/zhongnanshan.jpg",
        ):
            self.assertEqual(trial.page_referenced_photo_url(value, source), ("", ""))
        self.assertEqual(
            trial.detail_id("https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html?x=1"),
            "",
        )

    def test_parser_uses_only_unique_photo_container(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html"
        html = """
        <html><head><title>钟南山_呼吸与危重症医学科_广州医科大学附属第一医院官方网站www.gyfyy.com</title></head>
        <body>
          <img src="/Upload/202106/zhongnanshan-lab.png">
          <div class="photo"><img src="/Upload/202112/637750146771733237.jpg"></div>
          <div class="floatcard"><img src="/Upload/202112/637750146771733237.jpg"></div>
        </body></html>
        """
        state, portrait = trial.inspect_portrait_reference(html, source, "钟南山")
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)
        assert portrait is not None
        self.assertEqual(portrait.reference_kind, "Upload原图")
        self.assertEqual(
            portrait.photo_url,
            "https://www.gyfyyy.cn/Upload/202112/637750146771733237.jpg",
        )
        self.assertEqual(portrait.template_signature, "div.photo img")

    def test_parser_accepts_doctor_style_and_rejects_ambiguous_container(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_9.html"
        html = """
        <title>赖克方_呼吸与危重症医学科_广州医科大学附属第一医院官方网站www.gyfyy.com</title>
        <div class="doctor-card photo"><img src="/images/doctor/LAIKEFANG.jpg"></div>
        """
        state, portrait = trial.inspect_portrait_reference(html, source, "赖克方")
        self.assertEqual(state, "")
        assert portrait is not None
        self.assertEqual(portrait.reference_kind, "doctor原图")
        with self.assertRaisesRegex(RuntimeError, "div.photo 容器不唯一"):
            trial.inspect_portrait_reference(
                html + '<div class="photo"><img src="/images/doctor/OTHER.jpg"></div>',
                source,
                "赖克方",
            )

    def test_parser_tolerates_official_title_space_before_separator(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/xxgnk/doctor_910.html"
        html = """
        <title>李培鑫 _心血管内科_广州医科大学附属第一医院官方网站www.gyfyy.com</title>
        <div class="photo"><img src="/images/doctor/LIPEIXIN.jpg"></div>
        """
        state, portrait = trial.inspect_portrait_reference(html, source, "李培鑫")
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)

    def test_scope_and_fixed_sample_plan_are_stable(self) -> None:
        payload = json.loads(trial.MASTER_JSON_PATH.read_text(encoding="utf-8"))
        for row in payload["rows"]:
            if row.get("医院") == trial.HOSPITAL:
                row["照片链接"] = ""
                row["照片文件"] = ""
        with tempfile.TemporaryDirectory() as directory:
            baseline = Path(directory) / "master_payload.json"
            baseline.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            with patch.object(trial, "MASTER_JSON_PATH", baseline):
                rows = trial.load_scope_rows()
                selected = trial.select_trial_rows(rows)
        self.assertEqual(len(rows), 616)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(
            len({trial.atomic_department(row) for row in selected}), 8
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
                "https://www.gyfyyy.cn/images/doctor/avatar.gif", content, "gif"
            ),
        )

    def test_colorful_small_gif_and_large_gif_are_not_format_placeholders(self) -> None:
        colorful = Image.new("RGB", (30, 30), (0, 80, 220))
        buffer = io.BytesIO()
        colorful.save(buffer, format="GIF")
        content = buffer.getvalue()
        self.assertEqual(
            trial.downloaded_placeholder_reason(
                "https://www.gyfyyy.cn/images/doctor/doctor.gif", content, "gif"
            ),
            "",
        )
        large_gif = b"GIF89a" + b"x" * trial.SMALL_GIF_PLACEHOLDER_BYTES
        self.assertEqual(
            trial.downloaded_placeholder_reason(
                "https://www.gyfyyy.cn/images/doctor/portrait.gif", large_gif, "gif"
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
            "来源链接": "https://www.gyfyyy.cn/cn/ks/nk/test/doctor_999.html",
        }
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(trial, "TRIAL_PHOTO_DIR", Path(directory)):
                filename, path = trial.allocate_trial_photo(row, "png", content)
                self.assertEqual(
                    filename,
                    "测试医生-测试科-副主任医师-广州医科大学附属第一医院.png",
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
                "测试医生", "https://www.gyfyyy.cn/images/doctor/TEST.bmp", "", 100
            )
        with self.assertRaisesRegex(RuntimeError, "超过 20 MiB"):
            trial.enforce_photo_policy(
                "测试医生",
                "https://www.gyfyyy.cn/images/doctor/TEST.jpg",
                "jpg",
                trial.FULL_FUSE_BYTES + 1,
            )

    def test_full_authorization_and_failure_warning_are_explicit(self) -> None:
        self.assertIn("PR #64", trial.FULL_AUTHORIZATION)
        self.assertIn("FULL_APPEND_AND_OBSIDIAN", trial.FULL_AUTHORIZATION)
        self.assertIn("616 行全量", trial.FULL_AUTHORIZATION)
        self.assertIn("台账序号 15", trial.FULL_AUTHORIZATION)
        warning = trial.append_failure_warning("既有提示", "无照片容器")
        self.assertEqual(
            warning,
            f"既有提示；{trial.FULL_WARNING_BY_STATE['无照片容器']}",
        )
        self.assertEqual(trial.append_failure_warning(warning, "无照片容器"), warning)

    def test_full_row_diff_allows_only_target_photo_columns(self) -> None:
        source = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html"
        before = [
            {
                "来源链接": source,
                "照片链接": "",
                "照片文件": "",
                "异常提示": "",
                "姓名": "钟南山",
            }
        ]
        after = [{**before[0], "照片链接": "https://www.gyfyyy.cn/images/doctor/A.jpg"}]
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
        self.assertEqual(first, "同名-内科-主任医师-广州医科大学附属第一医院.jpg")
        self.assertEqual(
            second,
            "同名-内科-主任医师-广州医科大学附属第一医院-101.jpg",
        )

    def test_profile_photo_insert_preserves_bom_newlines_and_other_bytes(self) -> None:
        before = (
            b"\xef\xbb\xbf---\r\nprotected: true\r\n---\r\n\r\n# Doctor\r\n\r\n"
            + "## 基础信息\r\n\r\n".encode("utf-8")
            + b"| field | value |\r\n|---|---|\r\n| x | y |\r\n"
        )
        photo_file = (
            "01_试点医院/广州医科大学附属第一医院/照片/"
            "钟南山-呼吸与危重症医学科-主任医师-广州医科大学附属第一医院.jpg"
        )
        after = trial.insert_profile_photo_block_bytes(before, "钟南山", photo_file)
        expected = (
            "![钟南山](照片/钟南山-呼吸与危重症医学科-主任医师-"
            "广州医科大学附属第一医院.jpg)\r\n\r\n"
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

    def test_ledger_skip_note_is_append_only_and_idempotent(self) -> None:
        self.assertEqual(
            trial.append_ledger_skip_note("入口锚文本：专家介绍"),
            "入口锚文本：专家介绍；管理员裁决跳过（军队医院，2026-08-17）",
        )
        complete = "入口锚文本：专家介绍；管理员裁决跳过（军队医院，2026-08-17）"
        self.assertEqual(trial.append_ledger_skip_note(complete), complete)

    def test_full_validator_closes_616_rows_with_three_failure_states(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (8, 9), "blue").save(buffer, format="JPEG")
        content = buffer.getvalue()
        digest = hashlib.sha256(content).hexdigest()
        success_count = 500
        failed_count = trial.EXPECTED_SCOPE_COUNT - success_count
        rows = []
        reconciliation = []
        photos = []
        with tempfile.TemporaryDirectory() as directory:
            photo_root = Path(directory)
            for index in range(trial.EXPECTED_SCOPE_COUNT):
                source = (
                    "https://www.gyfyyy.cn/cn/ks/nk/test/"
                    f"doctor_{10000 + index}.html"
                )
                if index < success_count:
                    filename = f"医生{index}.jpg"
                    photo_url = f"https://www.gyfyyy.cn/images/doctor/DOCTOR{index}.jpg"
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
                },
                "rows": rows,
                "reconciliation": reconciliation,
                "photo_samples": photos,
            }
            trial.validate_full_payload(payload, photo_root)


if __name__ == "__main__":
    unittest.main()
