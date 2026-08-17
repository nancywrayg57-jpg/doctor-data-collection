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

import sysu5_photo_backfill_trial as target  # noqa: E402


class Sysu5PhotoBackfillTrialTests(unittest.TestCase):
    def test_repository_paths_are_relative_to_checkout(self) -> None:
        self.assertEqual(target.ROOT, WORK_DIR.parent)
        self.assertEqual(target.WORK_DIR, WORK_DIR)

    def test_parses_unique_featured_media_image(self) -> None:
        photo = (
            "/sites/default/files/styles/watermark/public/2026-01/"
            "%E4%B8%81%E7%AB%8B.jpg?itok=abc123"
        )
        html = f"""
        <html><head><title>丁立 | 中山大学附属第五医院</title></head>
        <body class="page-node page-node-type-doctor">
          <img src="/sites/default/files/styles/watermark/public/banner.jpg?itok=banner">
          <div class="field field-featured-media field-item"><picture>
            <img width="800" height="1173" src="{photo}">
          </picture></div>
        </body></html>
        """
        state, portrait = target.inspect_portrait_reference(
            html,
            "https://www.sysu5.cn/medical-service/department-expert/doctor/10285",
            "丁立",
        )
        self.assertEqual(state, "")
        self.assertIsNotNone(portrait)
        assert portrait is not None
        self.assertEqual(portrait.source_attribute, "src")
        self.assertEqual(portrait.reference_kind, "派生图")
        self.assertEqual(portrait.derivative_style, "watermark")
        self.assertEqual(portrait.photo_url, "https://www.sysu5.cn" + photo)

    def test_non_featured_image_is_not_a_portrait_container(self) -> None:
        html = """
        <title>丁立 | 中山大学附属第五医院</title>
        <body class="page-node-type-doctor">
          <picture><img src="/sites/default/files/styles/watermark/public/a.jpg?itok=x"></picture>
        </body>
        """
        state, portrait = target.inspect_portrait_reference(
            html,
            "https://www.sysu5.cn/medical-service/department-expert/doctor/10285",
            "丁立",
        )
        self.assertEqual(state, "无照片容器")
        self.assertIsNone(portrait)

    def test_rejects_original_or_unexpected_query_parameter(self) -> None:
        base = "https://www.sysu5.cn/medical-service/department-expert/doctor/10285"
        self.assertEqual(
            target.page_referenced_photo_url(
                "/sites/default/files/2026-01/a.jpg", base
            ),
            "",
        )
        self.assertEqual(
            target.page_referenced_photo_url(
                "/sites/default/files/styles/watermark/public/a.jpg?width=800", base
            ),
            "",
        )
        self.assertEqual(
            target.page_referenced_photo_url(
                "/sites/default/files/styles/watermark/public/a.jpg?itok=ok", base
            ),
            "https://www.sysu5.cn/sites/default/files/styles/watermark/public/a.jpg?itok=ok",
        )

    def test_title_layers_and_primary_titles(self) -> None:
        self.assertEqual(target.primary_title("教授，主任医师"), "主任医师")
        self.assertEqual(target.title_level("教授，主任医师"), "正高")
        self.assertEqual(target.title_level("副主任医师，医学博士"), "副高")
        self.assertEqual(target.title_level("主治医师，医学硕士"), "其他")

    def test_scope_and_fixed_sample_plan_are_stable(self) -> None:
        payload = json.loads(target.MASTER_JSON_PATH.read_text(encoding="utf-8"))
        for row in payload.get("rows", []):
            if target.clean_text(row.get("医院")) == target.HOSPITAL:
                row["照片链接"] = ""
                row["照片文件"] = ""
        with tempfile.TemporaryDirectory() as directory:
            trial_baseline = Path(directory) / "trial_baseline.json"
            trial_baseline.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            with patch.object(target, "MASTER_JSON_PATH", trial_baseline):
                rows = target.load_scope_rows()
        selected = target.select_trial_rows(rows)
        self.assertEqual(len(rows), 413)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(
            len({target.atomic_department(row) for row in selected}),
            target.MIN_TRIAL_DEPARTMENTS,
        )
        self.assertEqual(
            {target.title_level(row.get("职称身份原文")) for row in selected},
            {"正高", "副高", "其他"},
        )
        self.assertEqual(
            [target.clean_text(row.get("姓名")) for row in selected],
            [name for name, _, _ in target.SAMPLE_PLAN],
        )
        self.assertEqual(
            [target.detail_id(row.get("来源链接")) for row in selected],
            [detail for _, _, detail in target.SAMPLE_PLAN],
        )

    def test_magic_and_dimensions(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (37, 53), "white").save(buffer, format="JPEG")
        content = buffer.getvalue()
        self.assertEqual(target.magic_extension(content, "image/jpeg"), "jpg")
        self.assertEqual(target.image_dimensions(content), (37, 53))

    def test_small_gif_gray_or_nopic_is_placeholder(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (400, 600), (238, 238, 238)).save(buffer, format="GIF")
        content = buffer.getvalue()
        self.assertLess(len(content), target.SMALL_GIF_PLACEHOLDER_BYTES)
        self.assertIn(
            "占位图",
            target.downloaded_placeholder_reason(
                "https://www.sysu5.cn/sites/default/files/styles/watermark/public/nopic.gif?itok=x",
                content,
                "gif",
            ),
        )
        self.assertIn(
            "灰底占比",
            target.downloaded_placeholder_reason(
                "https://www.sysu5.cn/sites/default/files/styles/watermark/public/portrait.gif?itok=x",
                content,
                "gif",
            ),
        )

    def test_small_colorful_gif_is_not_placeholder(self) -> None:
        image = Image.new("RGB", (32, 32))
        for y in range(32):
            for x in range(32):
                image.putpixel(
                    (x, y),
                    ((x * 37 + y * 13) % 256, (x * 17) % 256, (y * 29) % 256),
                )
        buffer = io.BytesIO()
        image.save(buffer, format="GIF")
        content = buffer.getvalue()
        self.assertEqual(
            target.downloaded_placeholder_reason(
                "https://www.sysu5.cn/sites/default/files/styles/watermark/public/portrait.gif?itok=x",
                content,
                "gif",
            ),
            "",
        )

    def test_allocate_trial_name_and_no_overwrite(self) -> None:
        row = {
            "姓名": "丁立",
            "科室_分类页": "感染病防治中心",
            "职称身份原文": "感染病一科主任，主任医师",
            "来源链接": "https://www.sysu5.cn/medical-service/department-expert/doctor/10285",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(target, "TRIAL_PHOTO_DIR", Path(temp_dir)):
                filename, path = target.allocate_trial_photo(row, "jpg", b"one")
                self.assertEqual(
                    filename,
                    "丁立-感染病防治中心-主任医师-中山大学附属第五医院.jpg",
                )
                path.write_bytes(b"one")
                self.assertEqual(
                    target.allocate_trial_photo(row, "jpg", b"one"),
                    (filename, path),
                )
                alternate, _ = target.allocate_trial_photo(row, "jpg", b"two")
                self.assertTrue(alternate.endswith("-10285.jpg"))

    def test_size_buckets(self) -> None:
        self.assertEqual(target.size_bucket(10), "<200KiB")
        self.assertEqual(target.size_bucket(target.LARGE_BYTES), "200KiB-1MiB")
        self.assertEqual(target.size_bucket(2 * 1024 * 1024), "1-5MiB")
        self.assertEqual(target.size_bucket(6 * 1024 * 1024), ">5MiB")

    def test_full_authorization_and_warning_are_explicit_and_idempotent(self) -> None:
        self.assertIn("PR #62", target.FULL_AUTHORIZATION)
        self.assertIn("FULL_APPEND_AND_OBSIDIAN", target.FULL_AUTHORIZATION)
        self.assertIn("方案 A", target.FULL_AUTHORIZATION)
        self.assertIn("5-20 MiB", target.FULL_AUTHORIZATION)
        warning = target.append_failure_warning("既有提示", "无照片容器")
        self.assertEqual(
            warning,
            f"既有提示；{target.FULL_WARNING_BY_STATE['无照片容器']}",
        )
        self.assertEqual(
            target.append_failure_warning(warning, "无照片容器"), warning
        )

    def test_full_row_diff_allows_only_authorized_target_columns(self) -> None:
        source = "https://www.sysu5.cn/medical-service/department-expert/doctor/10285"
        before = [
            {
                "来源链接": source,
                "照片链接": "",
                "照片文件": "",
                "异常提示": "",
                "姓名": "丁立",
            }
        ]
        after = [{**before[0], "照片链接": "https://www.sysu5.cn/photo.jpg"}]
        diffs = target.collect_full_row_diffs(before, after, {source})
        self.assertEqual([item["列名"] for item in diffs], ["照片链接"])
        with self.assertRaisesRegex(RuntimeError, "范围外行"):
            target.collect_full_row_diffs(before, after, set())
        with self.assertRaisesRegex(RuntimeError, "范围外字段"):
            target.collect_full_row_diffs(
                before, [{**before[0], "姓名": "错误"}], {source}
            )

    def test_full_photo_policy_reports_5_to_20_mib_and_fuses_above_20_mib(self) -> None:
        target.enforce_full_photo_policy(
            "大图医生",
            "https://www.sysu5.cn/photo.jpg",
            "jpg",
            target.MAX_OWNER_REPORT_BYTES + 1,
        )
        target.enforce_full_photo_policy(
            "边界医生",
            "https://www.sysu5.cn/photo.webp",
            "webp",
            target.MAX_FULL_IMAGE_BYTES,
        )
        with self.assertRaisesRegex(RuntimeError, "超过 20 MiB"):
            target.enforce_full_photo_policy(
                "超限医生",
                "https://www.sysu5.cn/photo.png",
                "png",
                target.MAX_FULL_IMAGE_BYTES + 1,
            )
        with self.assertRaisesRegex(RuntimeError, "格式不受支持"):
            target.enforce_full_photo_policy(
                "格式医生",
                "https://www.sysu5.cn/photo.bmp",
                "bmp",
                1024,
            )

    def test_full_report_lists_owner_review_large_photos(self) -> None:
        photo_url = "https://www.sysu5.cn/photo.jpg?itok=owner-review"
        payload = {
            "meta": {
                "run_date": "2026-08-17",
                "expected_count": target.EXPECTED_SCOPE_COUNT,
                "downloaded_count": target.EXPECTED_SCOPE_COUNT,
                "failed_count": 0,
                "blank_count": 0,
                "failure_state_counts": {state: 0 for state in target.FULL_FAILURE_STATES},
                "failure_ratio": 0.0,
                "photo_total_bytes": target.MAX_OWNER_REPORT_BYTES + 1,
                "photo_total_mib": (target.MAX_OWNER_REPORT_BYTES + 1) / 1024 / 1024,
                "photo_max_bytes": target.MAX_OWNER_REPORT_BYTES + 1,
                "over_5mib_count": 1,
                "over_20mib_count": 0,
                "incomplete_read_retry_count": 0,
                "existing_profile_count": target.EXPECTED_PROFILE_COUNT,
                "profile_refreshed_count": target.EXPECTED_PROFILE_COUNT,
            },
            "photo_samples": [
                {
                    "name": "大图医生",
                    "photo_url": photo_url,
                    "bytes": target.MAX_OWNER_REPORT_BYTES + 1,
                    "width": 4831,
                    "height": 4833,
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            report_path = Path(directory) / "report.md"
            target.write_full_report(report_path, payload)
            report = report_path.read_text(encoding="utf-8")
        self.assertIn("## >5 MiB Owner 终审清单", report)
        self.assertIn("大图医生", report)
        self.assertIn(photo_url, report)
        self.assertIn(str(target.MAX_OWNER_REPORT_BYTES + 1), report)
        self.assertIn("4831×4833", report)

    def test_allocate_full_photo_uses_detail_id_only_for_collision(self) -> None:
        first = {
            "姓名": "同名",
            "科室_分类页": "内科",
            "职称身份原文": "主任医师",
        }
        second = dict(first)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            used: set[str] = set()
            first_name, _ = target.allocate_full_photo_path(
                first, "100", "jpg", root, used
            )
            second_name, _ = target.allocate_full_photo_path(
                second, "101", "jpg", root, used
            )
        self.assertEqual(
            first_name, "同名-内科-主任医师-中山大学附属第五医院.jpg"
        )
        self.assertEqual(
            second_name, "同名-内科-主任医师-中山大学附属第五医院-101.jpg"
        )

    def test_scheme_a_insert_preserves_bom_newlines_and_other_bytes(self) -> None:
        before = (
            b"\xef\xbb\xbf---\r\nprotected: true\r\n---\r\n\r\n# Doctor\r\n\r\n"
            + "## 基础信息\r\n\r\n".encode("utf-8")
            + b"| field | value |\r\n|---|---|\r\n| x | y |\r\n"
        )
        photo_file = (
            "01_试点医院/中山大学附属第五医院/照片/"
            "丁立-感染病防治中心-主任医师-中山大学附属第五医院.jpg"
        )
        after = target.insert_profile_photo_block_bytes(before, "丁立", photo_file)
        expected_block = (
            "![丁立](照片/丁立-感染病防治中心-主任医师-中山大学附属第五医院.jpg)"
            "\r\n\r\n"
        ).encode("utf-8")
        self.assertTrue(after.startswith(b"\xef\xbb\xbf"))
        self.assertEqual(after, before.replace(
            "## 基础信息\r\n\r\n".encode("utf-8"),
            "## 基础信息\r\n\r\n".encode("utf-8") + expected_block,
        ))
        target.validate_profile_photo_only_bytes(before, after, "丁立", photo_file)
        with self.assertRaisesRegex(RuntimeError, "已存在照片"):
            target.insert_profile_photo_block_bytes(after, "丁立", photo_file)

    def test_profile_tree_validator_forbids_file_set_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile = root / "医生.md"
            index = root / "_索引.md"
            profile.write_text("before", encoding="utf-8")
            index.write_text("index", encoding="utf-8")
            before = target.profile_markdown_tree(root)
            profile.write_text("after", encoding="utf-8")
            target.validate_profile_tree_surgical(
                before, root, {Path("医生.md")}
            )
            (root / "新增.md").write_text("new", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "文件集合"):
                target.validate_profile_tree_surgical(
                    before, root, {Path("医生.md")}
                )

    def test_full_validator_closes_413_rows_below_fuse_ratio(self) -> None:
        buffer = io.BytesIO()
        Image.new("RGB", (8, 9), "blue").save(buffer, format="JPEG")
        content = buffer.getvalue()
        digest = hashlib.sha256(content).hexdigest()
        success_count = 300
        failed_count = target.EXPECTED_SCOPE_COUNT - success_count
        rows = []
        reconciliation = []
        photos = []
        with tempfile.TemporaryDirectory() as directory:
            photo_root = Path(directory)
            for index in range(target.EXPECTED_SCOPE_COUNT):
                source = (
                    "https://www.sysu5.cn/medical-service/department-expert/doctor/"
                    f"{10000 + index}"
                )
                if index < success_count:
                    filename = f"医生{index}.jpg"
                    photo_url = (
                        "https://www.sysu5.cn/sites/default/files/styles/"
                        f"watermark/public/{filename}?itok=x{index}"
                    )
                    photo_file = (
                        f"01_试点医院/{target.HOSPITAL}/照片/{filename}"
                    )
                    (photo_root / filename).write_bytes(content)
                    rows.append(
                        {
                            "姓名": f"医生{index}",
                            "来源链接": source,
                            "照片链接": photo_url,
                            "照片文件": photo_file,
                            "异常提示": "",
                        }
                    )
                    reconciliation.append(
                        {
                            "姓名": f"医生{index}",
                            "来源链接": source,
                            "状态": "实采",
                            "失败三态": "",
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
                        }
                    )
                else:
                    warning = target.FULL_WARNING_BY_STATE["无照片容器"]
                    rows.append(
                        {
                            "姓名": f"医生{index}",
                            "来源链接": source,
                            "照片链接": "",
                            "照片文件": "",
                            "异常提示": warning,
                        }
                    )
                    reconciliation.append(
                        {
                            "姓名": f"医生{index}",
                            "来源链接": source,
                            "状态": "失败",
                            "失败三态": "无照片容器",
                        }
                    )
            payload = {
                "meta": {
                    "expected_count": target.EXPECTED_SCOPE_COUNT,
                    "downloaded_count": success_count,
                    "failed_count": failed_count,
                    "blank_count": failed_count,
                    "failure_state_counts": {
                        "详情不可达": 0,
                        "无照片容器": failed_count,
                        "占位图": 0,
                    },
                    "constructed_unreferenced_probe_count": 0,
                    "third_party_source_count": 0,
                    "existing_profile_count": target.EXPECTED_PROFILE_COUNT,
                    "no_profile_scope_count": 0,
                    "profile_refreshed_count": success_count,
                    "photo_total_bytes": len(content) * success_count,
                    "photo_max_bytes": len(content),
                    "over_5mib_count": 0,
                    "over_20mib_count": 0,
                },
                "rows": rows,
                "reconciliation": reconciliation,
                "photo_samples": photos,
            }
            target.validate_full_payload(payload, photo_root)


if __name__ == "__main__":
    unittest.main()
