from __future__ import annotations

import io
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from PIL import Image


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

import fahsysu_photo_backfill_full as target


def gif_bytes(color: tuple[int, int, int]) -> bytes:
    output = io.BytesIO()
    Image.new("RGB", (20, 20), color).save(output, format="GIF")
    return output.getvalue()


class FakeSession:
    def __init__(self, results: list[object]) -> None:
        self.results = iter(results)

    def get(self, url: str, referer: str) -> object:
        del url, referer
        return next(self.results)


class FahsysuPhotoBackfillFullTests(unittest.TestCase):
    def test_full_scope_reuses_ten_successes_and_two_failures(self) -> None:
        self.assertEqual(target.EXPECTED_SCOPE_COUNT, 860)
        self.assertEqual(target.EXPECTED_TRIAL_REUSE_COUNT, 10)
        self.assertEqual(target.EXPECTED_TRIAL_FAILURE_REUSE_COUNT, 2)
        self.assertEqual(target.EXPECTED_FRESH_COUNT, 848)
        self.assertFalse(target.is_fresh_failure_origin("TRIAL_FAILURE_REUSE"))
        self.assertTrue(target.is_fresh_failure_origin("FULL_FETCH"))
        self.assertTrue(target.is_fresh_failure_origin(target.FLICKER_PROBE_ORIGIN))

    def test_failure_evidence_keeps_url_reference_count_and_feature(self) -> None:
        source = "https://www.fahsysu.org.cn/node/5780"
        excluded = {
            "url": "https://www.fahsysu.org.cn/sites/example/files/styles/mini200/public/icon.png?itok=x",
            "reason": "公共装饰图",
            "feature": "path contains /styles/mini200/",
        }
        analysis = target.trial.MediaAnalysis(
            page_name="黄雄庆",
            page_title="黄雄庆 | 中山大学附属第一医院",
            state="无照片容器",
            photo_url="",
            path_kind="",
            itok="",
            template_signature=".other-left .other-media .media-img[data-image-url]",
            focal_point_480_reference_count=0,
            media_candidate_count=1,
            excluded_resources=(excluded,),
            detection_feature="focal_point_480 引用数=0；医生照片容器缺失",
        )
        evidence = target.media_failure_evidence(
            analysis,
            [
                {
                    "utc": "2026-08-18T12:28:35Z",
                    "status": 200,
                    "final_url": source,
                }
            ],
        )
        self.assertEqual(evidence["focal_point_480_reference_count"], 0)
        self.assertEqual(evidence["resource_urls"], [excluded["url"]])
        self.assertIn("医生照片容器缺失", evidence["detection_feature"])
        self.assertIn(excluded["url"], target.failure_evidence_text(evidence))

    def test_failure_warning_is_idempotent(self) -> None:
        once = target.append_failure_warning("既有提示", "详情不可达")
        twice = target.append_failure_warning(once, "详情不可达")
        self.assertEqual(once, twice)
        self.assertEqual(twice.count(target.FULL_WARNING_BY_STATE["详情不可达"]), 1)

    def test_fetch_retries_three_times_with_two_30_second_intervals(self) -> None:
        results = [
            SimpleNamespace(status=503, content_type="text/html", final_url="https://www.fahsysu.org.cn/node/1"),
            SimpleNamespace(status=503, content_type="text/html", final_url="https://www.fahsysu.org.cn/node/1"),
            SimpleNamespace(status=503, content_type="text/html", final_url="https://www.fahsysu.org.cn/node/1"),
        ]
        sleeps: list[float] = []
        utc_values = [
            "2026-08-18T10:00:00+00:00",
            "2026-08-18T10:00:30+00:00",
            "2026-08-18T10:01:00+00:00",
        ]
        with patch.object(target.trial, "utc_now", side_effect=utc_values):
            result, attempts = target.fetch_with_retry(
                FakeSession(results),
                "https://www.fahsysu.org.cn/node/1",
                target.trial.DIRECTORY_URL,
                lambda response: response.status == 200,
                sleep_func=sleeps.append,
            )
        self.assertEqual(result.status, 503)
        self.assertEqual([item["attempt"] for item in attempts], [1, 2, 3])
        self.assertEqual(sleeps, [target.trial.DETAIL_RETRY_SECONDS] * 2)
        target.validate_retry_attempts(attempts)

    def test_small_gif_placeholder_uses_path_and_visual_boundaries(self) -> None:
        colored = gif_bytes((180, 10, 10))
        gray = gif_bytes((235, 235, 235))
        self.assertIn(
            "占位图",
            target.downloaded_placeholder_reason(
                "https://www.fahsysu.org.cn/files/noimage.gif", colored, "gif"
            ),
        )
        self.assertIn(
            "占位图",
            target.downloaded_placeholder_reason(
                "https://www.fahsysu.org.cn/files/doctor/real.gif", gray, "gif"
            ),
        )
        self.assertEqual(
            target.downloaded_placeholder_reason(
                "https://www.fahsysu.org.cn/files/doctor/real.gif", colored, "gif"
            ),
            "",
        )

    def test_profile_photo_refresh_is_exactly_plus_two_minus_zero(self) -> None:
        before = (
            "<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->\n"
            "# 医生\n\n## 基础信息\n\n- 姓名：郭宇\n"
        ).encode("utf-8")
        photo_file = "01_试点医院/中山大学附属第一医院/照片/郭宇.jpg"
        after = target.insert_profile_photo_block_bytes(before, "郭宇", photo_file)
        target.validate_profile_photo_only_bytes(before, after, "郭宇", photo_file)
        self.assertEqual(len(after.decode("utf-8").splitlines()), len(before.decode("utf-8").splitlines()) + 2)

    def test_filename_collision_appends_source_id(self) -> None:
        row = {
            "姓名": "张三",
            "科室_分类页": "心内科",
            "职称身份原文": "主任医师",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            used: set[str] = set()
            first, _ = target.allocate_full_photo_path(row, "100", "jpg", output_dir, used)
            second, _ = target.allocate_full_photo_path(row, "200", "jpg", output_dir, used)
        self.assertTrue(first.endswith("中山大学附属第一医院.jpg"))
        self.assertTrue(second.endswith("中山大学附属第一医院-200.jpg"))

    def test_audit_samples_are_min_max_and_eight_deterministic_random(self) -> None:
        samples = [
            {
                "bytes": index,
                "source_link": f"https://www.fahsysu.org.cn/node/{1000 + index}",
            }
            for index in range(1, 13)
        ]
        selected = target.select_audit_samples(samples)
        self.assertEqual(selected, target.select_audit_samples(list(reversed(samples))))
        self.assertEqual(len(selected), 10)
        self.assertEqual(selected[0]["bytes"], 1)
        self.assertEqual(selected[0]["audit_kind"], "最小")
        self.assertEqual(selected[1]["bytes"], 12)
        self.assertEqual(selected[1]["audit_kind"], "最大")
        self.assertEqual(
            sum(item["audit_kind"] == "确定性随机" for item in selected), 8
        )

    def test_five_round_flicker_probe_freezes_first_photo(self) -> None:
        source = "https://www.fahsysu.org.cn/node/25212"
        photo_url = (
            "https://www.fahsysu.org.cn/sites/"
            "1h.prod.sysucloud1.sysu.edu.cn/files/styles/focal_point_480/"
            "public/probe.jpg?itok=probe-token"
        )
        detail_html = f"""
        <div class="other-left">
          <div class="other-media">
            <div class="media-img" data-image-url="{photo_url}"></div>
          </div>
          <div class="other-left-title">万欢</div>
        </div>
        """.encode("utf-8")
        photo_buffer = io.BytesIO()
        Image.new("RGB", (31, 37), "navy").save(photo_buffer, format="JPEG")
        photo_bytes = photo_buffer.getvalue()
        sessions: list[object] = []

        class AggregateSession:
            def __init__(self) -> None:
                self.calls: list[str] = []

            def get(self, url: str, referer: str = "") -> object:
                del referer
                self.calls.append(url)
                if url == target.trial.OFFICIAL_HOME:
                    return SimpleNamespace(
                        status=200,
                        content_type="text/html",
                        charset="utf-8",
                        content=b"<html></html>",
                        final_url=url,
                    )
                if url == source:
                    return SimpleNamespace(
                        status=200,
                        content_type="text/html",
                        charset="utf-8",
                        content=detail_html,
                        final_url=url,
                    )
                if url == photo_url:
                    return SimpleNamespace(
                        status=200,
                        content_type="image/jpeg",
                        charset="utf-8",
                        content=photo_bytes,
                        final_url=url,
                    )
                raise AssertionError(f"unexpected URL {url}")

        now = [0.0]

        def sleeper(seconds: float) -> None:
            now[0] += seconds

        def session_factory() -> object:
            session = AggregateSession()
            sessions.append(session)
            return session

        started = datetime(2026, 8, 18, 10, 40, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_json = Path(temp_dir) / "probe.json"
            output_photo = Path(temp_dir) / "probe.bin"
            with patch.object(
                target.trial,
                "load_scope_rows",
                return_value=[
                    {
                        "医院": target.HOSPITAL,
                        "姓名": "万欢",
                        "来源链接": source,
                    }
                ],
            ):
                payload = target.run_status_flicker_probe(
                    source,
                    photo_url,
                    session_factory=session_factory,  # type: ignore[arg-type]
                    sleeper=sleeper,
                    monotonic=lambda: now[0],
                    utc_now=lambda: (
                        started + timedelta(seconds=now[0])
                    ).isoformat(),
                    output_json_path=output_json,
                    output_photo_path=output_photo,
                )
            target.validate_status_flicker_probe(payload, output_photo)
            self.assertEqual(output_photo.read_bytes(), photo_bytes)
            self.assertTrue(output_json.is_file())
        self.assertEqual(payload["meta"]["round_count"], 5)
        self.assertEqual(payload["meta"]["captured_round"], 1)
        self.assertEqual(payload["meta"]["round_intervals_seconds"], [60.0] * 4)
        self.assertEqual(len(sessions), 5)
        self.assertEqual(
            sum(
                session.calls.count(photo_url)  # type: ignore[attr-defined]
                for session in sessions
            ),
            1,
        )

    def test_five_round_flicker_probe_persists_dangling_reference(self) -> None:
        source = "https://www.fahsysu.org.cn/node/33035"
        photo_url = (
            "https://www.fahsysu.org.cn/sites/"
            "1h.prod.sysucloud1.sysu.edu.cn/files/styles/focal_point_480/"
            "public/dangling.jpg?itok=dangling-token"
        )
        detail_html = f"""
        <div class="other-left">
          <div class="other-media">
            <div class="media-img" data-image-url="{photo_url}"></div>
          </div>
          <div class="other-left-title">杨嵩</div>
        </div>
        """.encode("utf-8")

        class DanglingSession:
            def get(self, url: str, referer: str = "") -> object:
                del referer
                if url == target.trial.OFFICIAL_HOME:
                    return SimpleNamespace(
                        status=200,
                        content_type="text/html",
                        charset="utf-8",
                        content=b"<html></html>",
                        final_url=url,
                    )
                if url == source:
                    return SimpleNamespace(
                        status=200,
                        content_type="text/html",
                        charset="utf-8",
                        content=detail_html,
                        final_url=url,
                    )
                if url == photo_url:
                    return SimpleNamespace(
                        status=404,
                        content_type="text/html",
                        charset="utf-8",
                        content=b"<html>404</html>",
                        final_url=url,
                    )
                raise AssertionError(f"unexpected URL {url}")

        now = [0.0]

        def sleeper(seconds: float) -> None:
            now[0] += seconds

        started = datetime(2026, 8, 18, 13, 30, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_json = Path(temp_dir) / "probe.json"
            output_photo = Path(temp_dir) / "probe.bin"
            with patch.object(
                target.trial,
                "load_scope_rows",
                return_value=[
                    {
                        "医院": target.HOSPITAL,
                        "姓名": "杨嵩",
                        "来源链接": source,
                    }
                ],
            ):
                payload = target.run_status_flicker_probe(
                    source,
                    photo_url,
                    session_factory=DanglingSession,  # type: ignore[arg-type]
                    sleeper=sleeper,
                    monotonic=lambda: now[0],
                    utc_now=lambda: (
                        started + timedelta(seconds=now[0])
                    ).isoformat(),
                    output_json_path=output_json,
                    output_photo_path=output_photo,
                )
            target.validate_status_flicker_probe(payload, output_photo)
            self.assertTrue(output_json.is_file())
            self.assertFalse(output_photo.exists())
        self.assertEqual(payload["meta"]["captured_round"], 0)
        self.assertEqual(payload["meta"]["resolution_state"], "照片资源不可达")
        self.assertEqual([item["photo_status"] for item in payload["rounds"]], [404] * 5)
        self.assertEqual(payload["meta"]["round_intervals_seconds"], [60.0] * 4)


if __name__ == "__main__":
    unittest.main()
