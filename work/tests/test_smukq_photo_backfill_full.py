from __future__ import annotations

import ast
import base64
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import smukq_photo_backfill_full as full


class SmukqPhotoBackfillFullTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module_snapshots = {
            module: dict(vars(module))
            for module in (
                full.framework,
                full.trial,
                full.trial.framework,
                full.trial.base,
            )
        }

    def tearDown(self) -> None:
        for module, snapshot in self.module_snapshots.items():
            module.__dict__.clear()
            module.__dict__.update(snapshot)

    def test_scope_authorization_and_duplicate_policy_are_issue_81_specific(self) -> None:
        self.assertEqual(full.ISSUE_NUMBER, 81)
        self.assertEqual(full.EXPECTED_SCOPE_COUNT, 95)
        self.assertEqual(full.EXPECTED_TRIAL_REUSE_COUNT, 10)
        self.assertEqual(full.EXPECTED_FRESH_COUNT, 85)
        self.assertEqual(full.PULL_REQUEST_NUMBER, 82)
        self.assertIn("PR #82", full.FULL_AUTHORIZATION)
        self.assertEqual(full.OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS, {})

    def test_analyze_full_media_uses_unique_content_img(self) -> None:
        html = """
        <html><body>
          <img src="/Home/images/logo.png">
          <span class="content2_span1">管东华</span>
          <span class="content2_span2">主任医师</span>
          <img class="content_img" src="/Uploads/Upload/2024-07-19/a.png">
        </body></html>
        """
        analysis = full.analyze_full_doctor_media(
            html, "https://www.smukqyy.cn/prods/341/36", "管东华"
        )
        self.assertEqual(analysis.page_name, "管东华")
        self.assertEqual(analysis.page_title, "主任医师")
        self.assertEqual(analysis.state, "")
        self.assertEqual(
            analysis.photo_url,
            "https://www.smukqyy.cn/Uploads/Upload/2024-07-19/a.png",
        )
        self.assertEqual(analysis.photo_reference_count, 1)

    def test_analyze_full_media_rejects_duplicate_content_img(self) -> None:
        html = """
        <span class="content2_span1">管东华</span>
        <span class="content2_span2">主任医师</span>
        <img class="content_img" src="/Uploads/Upload/a.png">
        <img class="content_img" src="/Uploads/Upload/b.png">
        """
        with self.assertRaisesRegex(RuntimeError, "容器不唯一"):
            full.analyze_full_doctor_media(
                html, "https://www.smukqyy.cn/prods/341/36", "管东华"
            )

    def test_analyze_full_media_classifies_missing_container(self) -> None:
        html = """
        <span class="content2_span1">管东华</span>
        <span class="content2_span2">主任医师</span>
        """
        analysis = full.analyze_full_doctor_media(
            html, "https://www.smukqyy.cn/prods/341/36", "管东华"
        )
        self.assertEqual(analysis.state, "无照片容器")
        self.assertEqual(analysis.photo_reference_count, 0)

    def test_analyze_full_media_rejects_home_images_even_in_container(self) -> None:
        html = """
        <span class="content2_span1">管东华</span>
        <span class="content2_span2">主任医师</span>
        <img class="content_img" src="/Home/images/person.png">
        """
        with self.assertRaisesRegex(RuntimeError, "URL 越界"):
            full.analyze_full_doctor_media(
                html, "https://www.smukqyy.cn/prods/341/36", "管东华"
            )

    def test_placeholder_gate_decodes_query_base64(self) -> None:
        encoded = base64.b64encode(b"blank2.jpg").decode()
        image = io.BytesIO()
        color = Image.new("RGB", (20, 20), "red")
        color.putpixel((0, 0), (0, 255, 0))
        color.putpixel((1, 0), (0, 0, 255))
        color.save(image, format="PNG")
        reason = full.placeholder_response_reason(
            "https://www.smukqyy.cn/Uploads/Upload/a.png?token=" + encoded,
            image.getvalue(),
            20,
            20,
        )
        self.assertIn("blank2.jpg", reason)

    def test_magic_signature_overrides_declared_content_type(self) -> None:
        png = io.BytesIO()
        Image.new("RGB", (20, 20), "blue").save(png, format="PNG")
        jpg = io.BytesIO()
        Image.new("RGB", (20, 20), "green").save(jpg, format="JPEG")
        self.assertEqual(full.trial.magic_extension(png.getvalue(), "image/jpeg"), "png")
        self.assertEqual(
            full.trial.magic_extension(jpg.getvalue(), "application/octet-stream"),
            "jpg",
        )

    def test_photo_only_title_variance_is_recorded_without_master_mutation(self) -> None:
        full.TITLE_VARIANCE_EVIDENCE.clear()
        row = {
            "姓名": "梁慧珉",
            "来源链接": "https://www.smukqyy.cn/prods/343/555",
            "职称身份原文": "副主任医师,医师,硕士",
        }
        analysis = full.MediaAnalysis(
            page_name="梁慧珉",
            page_title="副主任医师,硕士",
            state="",
            photo_url="https://www.smukqyy.cn/Uploads/Upload/a.jpg",
            opaque_query="",
            template_signature=full.TEMPLATE_SIGNATURE,
            photo_reference_count=1,
            single_con_image_count=0,
            outside_image_reference_count=0,
            excluded_resource_examples=(),
            container_html_snippet='<img class="content_img" src="/Uploads/Upload/a.jpg">',
            detection_feature="strict content_img",
        )
        full.validate_full_page_title(row, analysis)
        evidence = full.TITLE_VARIANCE_EVIDENCE[row["来源链接"]]
        self.assertEqual(evidence["master_title_preserved"], row["职称身份原文"])
        self.assertEqual(evidence["page_title_observed"], analysis.page_title)
        payload = {"meta": {}, "profile_integrity": []}
        full.enforce_repository_relative_payload(payload)
        self.assertEqual(payload["meta"]["page_title_variance_count"], 1)

    def test_photo_only_title_gate_rejects_empty_span(self) -> None:
        row = {
            "姓名": "梁慧珉",
            "来源链接": "https://www.smukqyy.cn/prods/343/555",
            "职称身份原文": "副主任医师,医师,硕士",
        }
        analysis = full.MediaAnalysis(
            page_name="梁慧珉",
            page_title="",
            state="",
            photo_url="https://www.smukqyy.cn/Uploads/Upload/a.jpg",
            opaque_query="",
            template_signature=full.TEMPLATE_SIGNATURE,
            photo_reference_count=1,
            single_con_image_count=0,
            outside_image_reference_count=0,
            excluded_resource_examples=(),
            container_html_snippet='<img class="content_img" src="/Uploads/Upload/a.jpg">',
            detection_feature="strict content_img",
        )
        with self.assertRaisesRegex(RuntimeError, "content2_span2"):
            full.validate_full_page_title(row, analysis)

    def test_committed_trial_manifest_and_relative_snapshot_are_reusable(self) -> None:
        full.configure_framework()
        payload = json.loads(full.trial.TRIAL_JSON_PATH.read_text(encoding="utf-8"))
        full.validate_trial_payload_for_full(payload, require_visual_pass=True)
        full.validate_trial_manifest(payload)
        if full.FULL_JSON_PATH.is_file():
            installed = json.loads(full.FULL_JSON_PATH.read_text(encoding="utf-8"))
            self.assertEqual(
                full.immutable_snapshot(),
                installed["meta"]["immutable_before"],
            )
        else:
            self.assertEqual(
                full.normalized_trial_protected_snapshot(),
                payload["meta"]["protected_assets_after"],
            )
        snapshot = full.immutable_snapshot()
        self.assertEqual(set(snapshot["files"]), {
            full.trial.repo_relative(path) for path in full.FULL_PROTECTED_FILES
        })
        self.assertNotIn(str(full.ROOT), json.dumps(snapshot, ensure_ascii=False))

    def test_full_payload_declares_relative_paths_and_blob_hash_policy(self) -> None:
        payload = {
            "meta": {},
            "profile_integrity": [
                {"path": r"医生画像仓库\01_试点医院\画像.md"}
            ],
        }
        full.enforce_repository_relative_payload(payload)
        self.assertIs(payload["meta"]["repository_relative_paths_only"], True)
        self.assertEqual(
            payload["meta"]["artifact_hash_policy"], "repository_blob_lf"
        )
        self.assertEqual(
            payload["profile_integrity"][0]["path"],
            "医生画像仓库/01_试点医院/画像.md",
        )

    def test_full_payload_rejects_absolute_profile_path(self) -> None:
        payload = {
            "meta": {},
            "profile_integrity": [{"path": str(full.ROOT / "画像.md")}],
        }
        with self.assertRaisesRegex(RuntimeError, "绝对路径"):
            full.enforce_repository_relative_payload(payload)

    def test_shared_full_runtime_trial_compatibility_is_complete(self) -> None:
        full.configure_framework()
        framework_path = Path(full.framework.__file__)
        tree = ast.parse(
            framework_path.read_text(encoding="utf-8"), filename=str(framework_path)
        )
        functions = {
            node.name: node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        reachable = set()
        pending = ["run_full", "validate_full_installation", "mark_visual_pass"]
        terminal_overrides = {"analyze_full_doctor_media"}
        self.assertIs(
            full.framework.analyze_full_doctor_media,
            full.analyze_full_doctor_media,
        )
        while pending:
            name = pending.pop()
            if name in reachable or name not in functions:
                continue
            reachable.add(name)
            for node in ast.walk(functions[name]):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in functions
                    and node.func.id not in terminal_overrides
                ):
                    pending.append(node.func.id)
        attributes = sorted(
            {
                node.attr
                for name in reachable
                for node in ast.walk(functions[name])
                if isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id == "trial"
            }
        )
        missing = [name for name in attributes if not hasattr(full.trial, name)]
        self.assertIn("contact_sheet_font", attributes)
        self.assertEqual(missing, [])

    def test_offline_full_audit_and_visual_sheet_renderers(self) -> None:
        full.configure_framework()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            photo_root = root / "photos"
            photo_root.mkdir()
            samples = []
            for index in range(10):
                image = Image.new(
                    "RGB", (120 + index, 140 + index), (30 + index, 80, 140)
                )
                image.putpixel((0, 0), (255, 0, 0))
                image.putpixel((1, 0), (0, 255, 0))
                filename = f"doctor-{index:02d}.jpg"
                path = photo_root / filename
                image.save(path, format="JPEG", quality=90)
                content = path.read_bytes()
                samples.append(
                    {
                        "detail_id": str(index + 1),
                        "name": f"医生{index + 1}",
                        "department": "口腔科",
                        "title": "医师",
                        "source_link": (
                            f"https://www.smukqyy.cn/prods/341/{index + 1}"
                        ),
                        "photo_url": (
                            f"https://www.smukqyy.cn/Uploads/Upload/{filename}"
                        ),
                        "filename": filename,
                        "bytes": len(content),
                        "width": 120 + index,
                        "height": 140 + index,
                        "sha256": hashlib.sha256(content).hexdigest(),
                    }
                )
            audit_path = root / "audit.jpg"
            audit = full.framework.build_full_audit_sheet(
                samples, photo_root, audit_path
            )
            visual_root = root / "visual"
            sheets = full.framework.build_visual_review_sheets(
                samples, photo_root, visual_root
            )
            self.assertEqual(len(audit), 10)
            self.assertTrue(audit_path.is_file())
            self.assertEqual(sum(item["count"] for item in sheets), 10)
            self.assertEqual(
                {path.name for path in visual_root.glob("*.jpg")},
                {item["path"] for item in sheets},
            )

    def test_configure_framework_clears_duplicate_allowlist_hooks(self) -> None:
        full.framework.decorate_owner_approved_duplicate_groups = object()
        full.framework.validate_owner_approved_duplicate_groups = object()
        full.configure_framework()
        self.assertEqual(full.framework.OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS, {})
        self.assertIsNone(full.framework.decorate_owner_approved_duplicate_groups)
        self.assertIsNone(full.framework.validate_owner_approved_duplicate_groups)
        self.assertIs(
            full.framework.validate_full_page_title, full.validate_full_page_title
        )
        self.assertEqual(full.framework.PULL_REQUEST_NUMBER, 82)
        self.assertFalse(full.framework.HOME_IS_GATE)
        self.assertIs(
            full.trial.contact_sheet_font, full.trial.framework.contact_sheet_font
        )


if __name__ == "__main__":
    unittest.main()
