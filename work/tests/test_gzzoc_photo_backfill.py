from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

from gzzoc_photo_backfill import (  # noqa: E402
    HOSPITAL,
    atomic_department,
    detail_id,
    image_dimensions,
    magic_extension,
    page_referenced_photo_url,
    parse_portrait_reference,
    primary_title,
    select_trial_rows,
    validate_trial,
)


def png_bytes(width: int, height: int) -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\rIHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x02\x00\x00\x00"
    )


class GzzocPhotoBackfillTests(unittest.TestCase):
    def test_strict_detail_and_page_referenced_photo_urls(self) -> None:
        detail = "http://www.gzzoc.org.cn/node/12767"
        derivative = (
            "/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/styles/"
            "large_960_x_auto_/public/2024-10/yizhen_2.jpg?itok=DVZxrNdb"
        )
        self.assertEqual(detail_id(detail), "12767")
        self.assertEqual(detail_id(f"{detail}?from=search"), "")
        self.assertEqual(
            page_referenced_photo_url(derivative, detail),
            "http://www.gzzoc.org.cn" + derivative,
        )
        self.assertEqual(
            page_referenced_photo_url("https://example.com/files/a.jpg", detail),
            "",
        )
        self.assertEqual(
            page_referenced_photo_url(
                "/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/default-avatar.jpg",
                detail,
            ),
            "",
        )

    def test_portrait_parser_accepts_only_named_showcase_image(self) -> None:
        detail = "http://www.gzzoc.org.cn/node/12767"
        derivative = (
            "/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/styles/"
            "large_960_x_auto_/public/2024-10/yizhen_2.jpg?itok=DVZxrNdb"
        )
        html = f"""
        <header><img src="/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/header-logo.png"></header>
        <div class="showcase-5-0"><div class="showcase-media">
          <img src="{derivative}">
        </div><h2>易珍</h2></div>
        <article><img src="/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/child-case.jpg"></article>
        """
        result = parse_portrait_reference(html, detail, "易珍")
        self.assertEqual(result.doctor_name, "易珍")
        self.assertEqual(result.derivative_url, "http://www.gzzoc.org.cn" + derivative)
        self.assertEqual(result.original_urls, ())
        self.assertEqual(len(result.referenced_urls), 1)

    def test_portrait_parser_rejects_name_or_structure_mismatch(self) -> None:
        detail = "http://www.gzzoc.org.cn/node/12767"
        photo = (
            "/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/styles/"
            "large_960_x_auto_/public/2024-10/yizhen_2.jpg?itok=token"
        )
        with self.assertRaisesRegex(RuntimeError, "姓名"):
            parse_portrait_reference(
                f'<div class="showcase-5-0"><div class="showcase-media"><img src="{photo}"></div><h2>他人</h2></div>',
                detail,
                "易珍",
            )
        with self.assertRaisesRegex(RuntimeError, "结构"):
            parse_portrait_reference("<main>无职业照容器</main>", detail, "易珍")

    def test_page_referenced_original_is_recorded_without_construction(self) -> None:
        detail = "https://www.gzzoc.org.cn/node/1"
        derivative = (
            "/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/styles/"
            "large_960_x_auto_/public/2024-10/a.jpg?itok=token"
        )
        original = "/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/public/2024-10/a.jpg"
        html = f"""
        <div class="showcase-5-0"><div class="showcase-media">
          <img src="{derivative}" data-original="{original}">
        </div><h2>张甲</h2></div>
        """
        result = parse_portrait_reference(html, detail, "张甲")
        self.assertEqual(result.original_urls, ("https://www.gzzoc.org.cn" + original,))

    def test_selection_spreads_departments_before_filling(self) -> None:
        rows = [
            {"姓名": "甲", "科室_分类页": "科室一", "来源链接": "http://www.gzzoc.org.cn/node/1"},
            {"姓名": "乙", "科室_分类页": "科室一", "来源链接": "http://www.gzzoc.org.cn/node/2"},
            {"姓名": "丙", "科室_分类页": "科室二", "来源链接": "http://www.gzzoc.org.cn/node/3"},
            {"姓名": "丁", "科室_分类页": "科室三", "来源链接": "http://www.gzzoc.org.cn/node/4"},
        ]
        selected = select_trial_rows(rows, 3)
        self.assertEqual([row["姓名"] for row in selected], ["甲", "丙", "丁"])

    def test_filename_parts_and_magic_dimensions(self) -> None:
        row = {
            "科室_分类页": "玻璃体、视网膜视神经疾病",
            "职称身份原文": "副主任医师、医学博士",
        }
        content = png_bytes(960, 1280)
        self.assertEqual(atomic_department(row), "玻璃体")
        self.assertEqual(primary_title(row["职称身份原文"]), "副主任医师")
        self.assertEqual(primary_title("副主任中医师"), "副主任中医师")
        self.assertEqual(primary_title("副主任技师"), "副主任技师")
        self.assertEqual(primary_title("副主任药师"), "副主任药师")
        self.assertEqual(primary_title("助理研究员"), "助理研究员")
        self.assertEqual(primary_title("副研究员"), "副研究员")
        self.assertEqual(primary_title("副教授"), "副教授")
        self.assertEqual(magic_extension(content, "image/png"), "png")
        self.assertEqual(image_dimensions(content, "png"), (960, 1280))
        self.assertEqual(magic_extension(b"<html>", "text/html"), "")

    def test_trial_validator_accepts_ten_immutable_samples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = []
            samples = []
            content = png_bytes(960, 1280)
            digest = hashlib.sha256(content).hexdigest()
            protected = {"master": {"bytes": 123, "sha256": "abc"}}
            for index in range(10):
                name = f"医生{index}"
                filename = f"{name}-科室{index}-主任医师-{HOSPITAL}.png"
                disk_path = root / filename
                disk_path.write_bytes(content)
                source_link = f"http://www.gzzoc.org.cn/node/{100 + index}"
                derivative_url = (
                    "http://www.gzzoc.org.cn/sites/zoc.live1.sysucloud2.sysu.edu.cn/"
                    "files/styles/large_960_x_auto_/public/2024-10/"
                    f"{index}.png?itok=token{index}"
                )
                photo_file = f"01_试点医院/{HOSPITAL}/照片/{filename}"
                rows.append(
                    {
                        "姓名": name,
                        "照片链接": derivative_url,
                        "照片文件": photo_file,
                    }
                )
                samples.append(
                    {
                        "name": name,
                        "derivative_url": derivative_url,
                        "photo_file": photo_file,
                        "filename": filename,
                        "bytes": len(content),
                        "width": 960,
                        "height": 1280,
                        "sha256": digest,
                        "disk_path": str(disk_path),
                    }
                )
            payload = {
                "meta": {
                    "scope_count": 205,
                    "trial_row_count": 10,
                    "department_coverage_count": 10,
                    "detail_error_count": 0,
                    "structure_mismatch_count": 0,
                    "photo_error_count": 0,
                    "photo_sample_count": 10,
                    "constructed_original_probe_count": 0,
                    "protected_assets_before": protected,
                    "protected_assets_after": protected,
                },
                "rows": rows,
                "photo_samples": samples,
            }
            validate_trial(payload)

    def test_trial_validator_rejects_original_path_probe(self) -> None:
        payload = {
            "meta": {
                "scope_count": 205,
                "trial_row_count": 10,
                "department_coverage_count": 3,
                "detail_error_count": 0,
                "structure_mismatch_count": 0,
                "photo_error_count": 0,
                "photo_sample_count": 10,
                "constructed_original_probe_count": 1,
                "protected_assets_before": {},
                "protected_assets_after": {},
            },
            "rows": [],
            "photo_samples": [],
        }
        with self.assertRaisesRegex(RuntimeError, "原图路径探测"):
            validate_trial(payload)


if __name__ == "__main__":
    unittest.main()
