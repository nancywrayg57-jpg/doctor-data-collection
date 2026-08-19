from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import four_hospital_photo_cleanup_full as target


class FourHospitalPhotoCleanupFullTests(unittest.TestCase):
    def test_equivalent_warning_rules_cover_existing_adjudications(self) -> None:
        self.assertTrue(
            target.has_equivalent_failure_warning(
                "官网详情未提供符合范围的本人职业照", "无照片容器"
            )
        )
        self.assertTrue(
            target.has_equivalent_failure_warning(
                "照片连续两次获取失败，管理员裁决留空", "照片资源不可达"
            )
        )
        self.assertTrue(
            target.has_equivalent_failure_warning(
                "官网本人职业照补录失败：占位图", "占位图"
            )
        )
        self.assertFalse(target.has_equivalent_failure_warning("详情缺少职称", "占位图"))

    def test_append_warning_preserves_original_and_is_idempotent(self) -> None:
        updated, action = target.append_failure_warning("详情缺少职称", "占位图")
        self.assertEqual(action, "更新留痕")
        self.assertEqual(updated, "详情缺少职称；官网本人职业照补录失败：占位图")
        second, second_action = target.append_failure_warning(updated, "占位图")
        self.assertEqual(second, updated)
        self.assertEqual(second_action, "维持留痕")

    def test_photo_reference_count_uses_raw_or_transport_reference(self) -> None:
        sample = {
            "raw_photo_reference": "/system/profile/a.jpg",
            "photo_url": "https://gd2h.com/system/profile/a.jpg",
            "page_image_references": [
                {
                    "raw_reference": "/system/profile/a.jpg",
                    "absolute_url": "https://gd2h.com/system/profile/a.jpg",
                }
            ],
        }
        self.assertEqual(target.photo_reference_count(sample), 1)

    def test_failure_resource_urls_keeps_raw_transport_pair(self) -> None:
        sample = {
            "source_link": "https://gd2h.com/site/doctor/1.html",
            "raw_photo_reference": "/system/profile/a b.jpg",
            "photo_url": "https://gd2h.com/system/profile/a%20b.jpg",
        }
        self.assertEqual(
            target.failure_resource_urls(sample),
            [
                "https://gd2h.com/system/profile/a%20b.jpg",
                "https://gd2h.com/system/profile/a b.jpg",
            ],
        )

    def test_allocate_formal_filename_avoids_existing_collision(self) -> None:
        row = {
            "医院": target.trial.GY120,
            "姓名": "医生甲",
            "科室_列表卡片": "内科",
            "职称_关键词": "主任医师",
            "来源链接": "https://www.gy120.net/articleshow.asp?ArticleID=123",
        }
        with tempfile.TemporaryDirectory(dir=target.WORK_DIR) as temporary:
            photo_root = Path(temporary)
            base = f"{target.trial.filename_stem(row)}.jpg"
            (photo_root / base).write_bytes(b"old")
            with mock.patch.dict(
                target.FORMAL_PHOTO_DIRS,
                {target.trial.GY120: photo_root},
                clear=False,
            ):
                filename = target.allocate_formal_filename(
                    row,
                    "jpg",
                    {hospital: set() for hospital in target.HOSPITALS},
                )
        self.assertNotEqual(filename, base)
        self.assertIn("123", filename)

    def test_cross_doctor_duplicate_sha_is_rejected_but_same_doctor_is_not(self) -> None:
        photos = [
            {"sha256": "a", "hospital": "甲院", "name": "甲", "source_link": "1"},
            {"sha256": "a", "hospital": "甲院", "name": "乙", "source_link": "2"},
            {"sha256": "b", "hospital": "甲院", "name": "丙", "source_link": "3"},
            {"sha256": "b", "hospital": "甲院", "name": "丙", "source_link": "4"},
        ]
        self.assertEqual(set(target.cross_doctor_duplicate_sha_groups(photos)), {"a"})

    def test_count_summary_accepts_zero_downloads(self) -> None:
        rows = []
        for hospital, count in target.EXPECTED_BY_HOSPITAL.items():
            for index in range(count):
                rows.append(
                    {
                        "医院": hospital,
                        "对账分类": "维持留痕" if index % 2 else "更新留痕",
                    }
                )
        summary = target.count_summary(rows)
        target.validate_count_summary(summary)
        self.assertEqual(summary["补采"], 0)
        self.assertEqual(summary["维持留痕"] + summary["更新留痕"], 249)

    def test_collect_row_diffs_allows_only_three_authorized_columns(self) -> None:
        before = [{header: "" for header in target.collector.BASE_HEADERS}]
        before[0].update({"来源链接": "https://example.test/1", "姓名": "甲"})
        after = copy.deepcopy(before)
        after[0]["异常提示"] = "新增"
        diffs = target.collect_row_diffs(
            before, after, {"https://example.test/1"}
        )
        self.assertEqual([item["列名"] for item in diffs], ["异常提示"])
        after[0]["姓名"] = "乙"
        with self.assertRaisesRegex(RuntimeError, "范围外字段"):
            target.collect_row_diffs(before, after, {"https://example.test/1"})

    def test_transaction_helpers_restore_existing_and_remove_new_files(self) -> None:
        with tempfile.TemporaryDirectory(dir=target.WORK_DIR) as temporary:
            root = Path(temporary)
            existing = root / "existing.txt"
            new_file = root / "new.txt"
            replacement = root / "replacement.txt"
            new_source = root / "new_source.txt"
            existing.write_text("before", encoding="utf-8")
            replacement.write_text("after", encoding="utf-8")
            new_source.write_text("new", encoding="utf-8")
            backups = target.backup_targets([existing, new_file], root / "backup")
            target.apply_file_map({existing: replacement, new_file: new_source})
            self.assertEqual(existing.read_text(encoding="utf-8"), "after")
            self.assertTrue(new_file.exists())
            target.restore_targets(backups)
            self.assertEqual(existing.read_text(encoding="utf-8"), "before")
            self.assertFalse(new_file.exists())

    def test_failure_audit_sheet_has_two_samples_per_hospital(self) -> None:
        failures = []
        for hospital in target.HOSPITALS:
            for index in range(2):
                failures.append(
                    {
                        "hospital": hospital,
                        "name": f"医生{index}",
                        "source_link": f"https://example.test/{hospital}/{index}",
                        "state": "占位图",
                        "action": "更新留痕",
                        "evidence": {
                            "observed_utc": "2026-08-20T00:00:00Z",
                            "raw_photo_reference": "/default.png",
                            "transport_url": "https://example.test/default.png",
                            "photo_reference_count": 1,
                            "detection_feature": "known placeholder",
                        },
                    }
                )
        with tempfile.TemporaryDirectory(dir=target.WORK_DIR) as temporary:
            output = Path(temporary) / "audit.jpg"
            selected = target.draw_failure_audit_sheet(failures, output)
            self.assertTrue(output.is_file())
            self.assertEqual(len(selected), 8)

    def test_failure_audit_wrap_width_prevents_long_line_clipping(self) -> None:
        wrapped = target.wrap_text(
            "feature: 详情照片位命中显式 default/placeholder 门禁；页面共享 uploads 图按 known-SHA 排除",
            60,
        )
        self.assertGreater(len(wrapped), 1)
        self.assertTrue(all(len(line) <= 60 for line in wrapped))


if __name__ == "__main__":
    unittest.main()
