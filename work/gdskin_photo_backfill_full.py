from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from dataclasses import dataclass
from datetime import date
from http.client import IncompleteRead
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import ProxyHandler, Request, build_opener

import gzbrain_photo_backfill_full as framework
import gdskin_photo_backfill_trial as trial


ROOT = trial.ROOT
WORK_DIR = trial.WORK_DIR
HOSPITAL = trial.HOSPITAL
ISSUE_NUMBER = trial.ISSUE_NUMBER
EXPECTED_SCOPE_COUNT = trial.EXPECTED_SCOPE_COUNT
EXPECTED_TRIAL_REUSE_COUNT = trial.EXPECTED_TRIAL_COUNT
EXPECTED_FRESH_COUNT = EXPECTED_SCOPE_COUNT - EXPECTED_TRIAL_REUSE_COUNT
PROFILE_DIR = trial.PROFILE_DIR
FORMAL_PHOTO_DIR = trial.FORMAL_PHOTO_DIR
FULL_BASENAME = f"{HOSPITAL}_photo_backfill_full"
FULL_JSON_PATH = WORK_DIR / f"{FULL_BASENAME}_payload.json"
FULL_CSV_PATH = WORK_DIR / f"{FULL_BASENAME}_reconciliation.csv"
FULL_REPORT_PATH = WORK_DIR / f"{FULL_BASENAME}_report.md"
FULL_AUDIT_SHEET_PATH = WORK_DIR / f"{FULL_BASENAME}_audit_sheet.jpg"
FULL_VISUAL_DIR = WORK_DIR / f"{FULL_BASENAME}_visual_review"
PHOTO_RELATIVE_ROOT = Path("01_试点医院") / HOSPITAL / "照片"
FULL_AUTHORIZATION = (
    "PR #84 owner comment 2026-08-19T12:45:24Z: "
    "TRIAL_AUDIT_PASSED -> FULL_APPEND_AND_OBSIDIAN; fixed scope 77; "
    "reuse 10 audited TRIAL originals; serial requests >=2 seconds; strict unique "
    "/uploadimg/ page-reference gate; NBSP dangling references are failure evidence"
)
PULL_REQUEST_NUMBER = 84
REQUEST_MODE = "urllib-browser-ua-get/no-cookie/no-proxy/no-bypass/serial-min-2s"
TEMPLATE_SIGNATURE = "unique body img src resolving under /uploadimg/"
MAX_PHOTO_BYTES = 20 * 1024 * 1024
OWNER_REPORT_BYTES = 5 * 1024 * 1024
VISUAL_PAGE_SIZE = 25
FULL_VISUAL_PASS_STATUS = framework.FULL_VISUAL_PASS_STATUS
OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS: dict[str, Any] = {}
TITLE_VARIANCE_EVIDENCE: dict[str, dict[str, str]] = {}
REFERENCE_EVIDENCE_BY_SOURCE: dict[str, dict[str, str]] = {}
FULL_REQUEST_TRACE: list[dict[str, Any]] = []
FULL_PROTECTED_FILES = (
    trial.base.MASTER_REPORT_PATH,
    trial.base.LEDGER_PATH,
    trial.TRIAL_JSON_PATH,
    trial.TRIAL_CSV_PATH,
    trial.TRIAL_REPORT_PATH,
    trial.CONTACT_SHEET_PATH,
)

ORIGINAL_TRIAL_VALIDATE_PAYLOAD = trial.validate_payload
ORIGINAL_TRIAL_PAGE_REFERENCED_PHOTO_URL = trial.page_referenced_photo_url
ORIGINAL_FRAMEWORK_VALIDATE_FULL_PAYLOAD = framework.validate_full_payload
ORIGINAL_FRAMEWORK_VALIDATE_FULL_INSTALLATION = framework.validate_full_installation
ORIGINAL_FRAMEWORK_WRITE_FULL_REPORT = framework.write_full_report


@dataclass(frozen=True)
class HttpResult:
    status: int
    content_type: str
    charset: str
    content: bytes
    final_url: str
    redirects: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class MediaAnalysis:
    page_name: str
    page_title: str
    state: str
    photo_url: str
    opaque_query: str
    template_signature: str
    photo_reference_count: int
    single_con_image_count: int
    outside_image_reference_count: int
    excluded_resource_examples: tuple[dict[str, str], ...]
    container_html_snippet: str
    detection_feature: str


class OfficialUrlOpenSession:
    """Owner-approved serial browser-UA GET without Cookie, proxy, or bypass."""

    def __init__(self) -> None:
        self.opener = build_opener(ProxyHandler({}))
        self.incomplete_read_retry_count = 0
        self._last_started_at: float | None = None

    @property
    def cookie_names(self) -> list[str]:
        return []

    @property
    def default_headers(self) -> list[list[str]]:
        return [["User-Agent", trial.framework.USER_AGENT]]

    def _wait_for_slot(self) -> float | None:
        now = time.monotonic()
        if self._last_started_at is None:
            self._last_started_at = now
            return None
        remaining = trial.REQUEST_INTERVAL_SECONDS - (now - self._last_started_at)
        while remaining > 0:
            time.sleep(remaining)
            now = time.monotonic()
            remaining = trial.REQUEST_INTERVAL_SECONDS - (now - self._last_started_at)
        interval = now - self._last_started_at
        self._last_started_at = now
        return interval

    def get(self, url: str) -> HttpResult:
        serialized_url = trial.transport_url(url)
        for attempt in range(2):
            interval = self._wait_for_slot()
            FULL_REQUEST_TRACE.append(
                {
                    "sequence": len(FULL_REQUEST_TRACE) + 1,
                    "requested_url": url,
                    "transport_url": serialized_url,
                    "interval_seconds_from_previous": (
                        None if interval is None else round(interval, 6)
                    ),
                    "observed_utc": trial.framework.utc_now(),
                }
            )
            request = Request(
                serialized_url, headers={"User-Agent": trial.framework.USER_AGENT}
            )
            try:
                with self.opener.open(request, timeout=35) as response:
                    return HttpResult(
                        status=int(response.status),
                        content_type=response.headers.get_content_type(),
                        charset=response.headers.get_content_charset() or "utf-8",
                        content=response.read(),
                        final_url=response.geturl(),
                        redirects=(),
                    )
            except IncompleteRead as exc:
                if attempt == 0:
                    self.incomplete_read_retry_count += 1
                    continue
                raise RuntimeError(
                    f"官网响应连续两次传输不完整：{url} 已读 {len(exc.partial)} bytes"
                ) from exc
            except HTTPError as exc:
                return HttpResult(
                    status=int(exc.code),
                    content_type=exc.headers.get_content_type(),
                    charset=exc.headers.get_content_charset() or "utf-8",
                    content=exc.read(),
                    final_url=exc.geturl(),
                    redirects=(),
                )
            except URLError as exc:
                raise RuntimeError(f"官网请求失败：{url} {exc}") from exc
        raise AssertionError("官网请求循环未返回")


def page_referenced_photo_url_for_full(
    value: Any, source_link: str
) -> tuple[str, str]:
    normalized = ORIGINAL_TRIAL_PAGE_REFERENCED_PHOTO_URL(value, source_link)
    if not normalized:
        return "", ""
    return normalized, urlparse(normalized).query


def excluded_page_resources(
    parser: trial.GdskinPhysicianPageParser, source_link: str
) -> tuple[dict[str, str], ...]:
    examples: list[dict[str, str]] = []
    for attrs in parser.image_attrs:
        raw = str(attrs.get("src") or "").strip()
        if not raw or trial.authorized_photo_candidate(raw, source_link):
            continue
        examples.append(
            {
                "url": raw,
                "reason": "站架或装饰图排除",
                "feature": "not a same-site /uploadimg/ page reference",
            }
        )
        if len(examples) == 5:
            break
    return tuple(examples)


def media_analysis(
    *,
    page_name: str,
    page_title: str,
    state: str,
    photo_url: str = "",
    photo_reference_count: int = 0,
    outside_image_reference_count: int = 0,
    excluded: tuple[dict[str, str], ...] = (),
    snippet: str = "",
    detection_feature: str,
) -> MediaAnalysis:
    return MediaAnalysis(
        page_name=page_name,
        page_title=page_title,
        state=state,
        photo_url=photo_url,
        opaque_query=urlparse(photo_url).query if photo_url else "",
        template_signature=TEMPLATE_SIGNATURE,
        photo_reference_count=photo_reference_count,
        single_con_image_count=0,
        outside_image_reference_count=outside_image_reference_count,
        excluded_resource_examples=excluded,
        container_html_snippet=snippet,
        detection_feature=detection_feature,
    )


def analyze_full_doctor_media(
    html: str, source_link: str, expected_name: str
) -> MediaAnalysis:
    if not trial.detail_id(source_link):
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    parser = trial.GdskinPhysicianPageParser()
    parser.feed(html)
    expected = trial.clean_text(expected_name)
    title_core = parser.page_title.split("__", 1)[0].strip()
    if not title_core or title_core.count(expected) != 1:
        raise RuntimeError(
            f"详情姓名与底表不一致：底表={expected_name} 官网标题={title_core or '空'} "
            f"{source_link}"
        )
    page_title = trial.clean_text(title_core.replace(expected, " ", 1))
    outside = excluded_page_resources(parser, source_link)
    candidates: list[tuple[dict[str, str], str, str]] = []
    for attrs, snippet in zip(parser.image_attrs, parser.image_snippets, strict=True):
        absolute = trial.authorized_photo_candidate(attrs.get("src"), source_link)
        if absolute:
            candidates.append((attrs, snippet, absolute))
    if not candidates:
        return media_analysis(
            page_name=expected,
            page_title=page_title,
            state="无照片容器",
            outside_image_reference_count=len(parser.image_attrs),
            excluded=outside,
            detection_feature=(
                "HTTP 200 detail contains no same-site /uploadimg/ img reference; "
                "WebResource and filing/site decoration images remain excluded"
            ),
        )
    if len(candidates) != 1:
        raise RuntimeError(
            f"/uploadimg/ 正文 img 容器不唯一：{source_link} 数量={len(candidates)}"
        )

    attrs, snippet, absolute = candidates[0]
    raw_reference = str(attrs.get("src") or "").strip()
    marker = trial.placeholder_marker_reason(absolute)
    if marker:
        return media_analysis(
            page_name=expected,
            page_title=page_title,
            state="占位图",
            photo_reference_count=1,
            outside_image_reference_count=len(parser.image_attrs) - 1,
            excluded=(
                {
                    "url": absolute,
                    "reason": "占位图",
                    "feature": f"raw_reference={raw_reference!r}; marker={marker}",
                },
            ),
            snippet=snippet,
            detection_feature=f"页面引用命中占位门禁：{marker}",
        )
    normalized = ORIGINAL_TRIAL_PAGE_REFERENCED_PHOTO_URL(
        raw_reference, source_link
    )
    if not normalized:
        raise RuntimeError(
            f"页面引用照片 URL 越界：{source_link} {raw_reference}"
        )
    transport = trial.transport_url(normalized)
    REFERENCE_EVIDENCE_BY_SOURCE[source_link] = {
        "page_raw_reference": raw_reference,
        "normalized_photo_url": normalized,
        "transport_url": transport,
        "container_html_snippet": snippet,
    }
    return media_analysis(
        page_name=expected,
        page_title=page_title,
        state="",
        photo_url=normalized,
        photo_reference_count=1,
        outside_image_reference_count=len(parser.image_attrs) - 1,
        excluded=(
            {
                "url": normalized,
                "reason": "页面引用与传输留证",
                "feature": (
                    f"raw_reference={raw_reference!r}; transport_url={transport}"
                ),
            },
        ),
        snippet=snippet,
        detection_feature=(
            "only the unique same-site img src resolving under /uploadimg/ is eligible; "
            f"raw_reference={raw_reference!r}; transport_url={transport}"
        ),
    )


def limited_unique_color_count(content: bytes, limit: int = 2) -> int:
    return trial.framework.limited_unique_color_count(content, limit)


def placeholder_response_reason(
    photo_url: str, content: bytes, width: int, height: int
) -> str:
    if hashlib.sha256(content).hexdigest() == trial.KNOWN_PLACEHOLDER_SHA256:
        return "响应命中站方已知占位 SHA-256"
    marker = trial.placeholder_marker_reason(photo_url)
    if marker:
        return f"照片 URL 命中占位标记：{marker}"
    unique_colors = limited_unique_color_count(content, limit=2)
    if unique_colors <= 2:
        return f"全图唯一颜色数={unique_colors}，命中单色/近单色占位启发式"
    if len(content) <= 10 * 1024 and width <= 128 and height <= 128:
        return f"响应呈小尺寸占位图特征：{len(content)} bytes；{width}×{height}"
    return ""


def validate_full_page_title(
    row: dict[str, Any], analysis: MediaAnalysis
) -> None:
    source = trial.clean_text(row.get("来源链接"))
    expected = trial.clean_text(row.get("职称身份原文"))
    actual = trial.clean_text(analysis.page_title)
    if not actual:
        raise RuntimeError(f"详情 title 中姓名后的职称为空：{source}")
    if actual != expected:
        TITLE_VARIANCE_EVIDENCE[source] = {
            "name": trial.clean_text(row.get("姓名")),
            "source_link": source,
            "master_title_preserved": expected,
            "page_title_observed": actual,
            "decision": (
                "PHOTO_ONLY_SCOPE: exact name and unique /uploadimg/ reference passed; "
                "retain the authorized master title without modification"
            ),
        }


def validate_trial_payload_for_full(
    payload: dict[str, Any], require_visual_pass: bool = False
) -> None:
    ORIGINAL_TRIAL_VALIDATE_PAYLOAD(payload)
    if require_visual_pass and payload["meta"].get("visual_review_status") != (
        "PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS"
    ):
        raise RuntimeError("TRIAL 联系表尚未通过人工视觉门禁")


def validate_trial_manifest(payload: dict[str, Any]) -> None:
    with trial.TRIAL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED_TRIAL_REUSE_COUNT:
        raise RuntimeError("TRIAL manifest 不是 10 行")
    rows_by_source = {row["来源链接"]: row for row in rows}
    if len(rows_by_source) != EXPECTED_TRIAL_REUSE_COUNT:
        raise RuntimeError("TRIAL manifest 来源链接不唯一")
    for sample in payload["photo_samples"]:
        row = rows_by_source.get(sample["source_link"])
        if row is None or any(
            (
                row["姓名"] != sample["name"],
                row["照片链接"] != sample["photo_url"],
                row["SHA-256"] != sample["sha256"],
                int(row["字节"]) != int(sample["bytes"]),
                row["实际魔数格式"] != sample["actual_extension"],
                row["声明格式"] != sample["declared_extension"],
            )
        ):
            raise RuntimeError(
                f"TRIAL manifest 与 payload 不一致：{sample['source_link']}"
            )


def size_buckets(samples: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "<200KiB": 0,
        "200KiB-1MiB": 0,
        "1-5MiB": 0,
        "5-20MiB": 0,
        ">20MiB": 0,
    }
    for sample in samples:
        size = int(sample["bytes"])
        if size < 200 * 1024:
            counts["<200KiB"] += 1
        elif size < 1024 * 1024:
            counts["200KiB-1MiB"] += 1
        elif size <= OWNER_REPORT_BYTES:
            counts["1-5MiB"] += 1
        elif size <= MAX_PHOTO_BYTES:
            counts["5-20MiB"] += 1
        else:
            counts[">20MiB"] += 1
    return counts


def file_digest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(f"受保护文件缺失：{path}")
    content = trial.base.repository_digest_bytes(path)
    return {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}


def immutable_snapshot() -> dict[str, Any]:
    return {
        "files": {
            trial.repo_relative(path): file_digest(path)
            for path in FULL_PROTECTED_FILES
        },
        "trial_photo_tree": trial.base.tree_snapshot(trial.TRIAL_PHOTO_DIR),
    }


def normalized_trial_protected_snapshot() -> dict[str, Any]:
    return trial.normalize_snapshot(trial.base.protected_snapshot())


def inject_runtime_evidence(payload: dict[str, Any]) -> None:
    meta = payload.setdefault("meta", {})
    if FULL_REQUEST_TRACE:
        intervals = [
            item["interval_seconds_from_previous"]
            for item in FULL_REQUEST_TRACE
            if item["interval_seconds_from_previous"] is not None
        ]
        payload["serial_request_trace"] = list(FULL_REQUEST_TRACE)
        meta["serial_request_count"] = len(FULL_REQUEST_TRACE)
        meta["serial_request_interval_seconds"] = trial.REQUEST_INTERVAL_SECONDS
        meta["minimum_observed_request_interval_seconds"] = min(intervals)
    if TITLE_VARIANCE_EVIDENCE:
        payload["page_title_variances"] = [
            TITLE_VARIANCE_EVIDENCE[source]
            for source in sorted(TITLE_VARIANCE_EVIDENCE)
        ]
    if payload.get("page_title_variances") is not None:
        meta["page_title_variance_count"] = len(payload["page_title_variances"])
        meta["page_title_validation_policy"] = (
            "detail title must contain the exact name and a non-empty title; differences "
            "are recorded while the master title remains immutable"
        )

    failures_by_source = {
        item.get("source_link"): item for item in payload.get("failures", [])
    }
    reconciliation_by_source = {
        item.get("来源链接"): item for item in payload.get("reconciliation", [])
    }
    for source, reference in REFERENCE_EVIDENCE_BY_SOURCE.items():
        failure = failures_by_source.get(source)
        if failure is None or failure.get("state") != "照片资源不可达":
            continue
        evidence = failure.setdefault("evidence", {})
        evidence.update(reference)
        failure["error"] = framework.failure_evidence_text(evidence)
        if source in reconciliation_by_source:
            reconciliation_by_source[source]["错误证据"] = failure["error"]


def enforce_repository_relative_payload(payload: dict[str, Any]) -> None:
    inject_runtime_evidence(payload)
    meta = payload.setdefault("meta", {})
    meta["repository_relative_paths_only"] = True
    meta["artifact_hash_policy"] = "repository_blob_lf"
    for item in payload.get("profile_integrity", []):
        raw_path = trial.clean_text(item.get("path"))
        if re.match(r"^[A-Za-z]:[\\/]", raw_path) or raw_path.startswith(("\\\\", "//")):
            raise RuntimeError(f"FULL 画像清单泄漏绝对路径：{raw_path}")
        path = Path(raw_path.replace("\\", "/"))
        if path.is_absolute():
            raise RuntimeError(f"FULL 画像清单泄漏绝对路径：{raw_path}")
        item["path"] = path.as_posix()
    serialized = json.dumps(payload, ensure_ascii=False)
    forbidden = {str(ROOT), ROOT.as_posix(), r"D:\workspace", "D:/workspace"}
    leaked = [value for value in forbidden if value and value in serialized]
    if leaked:
        raise RuntimeError("FULL payload 泄漏仓库绝对路径：" + "、".join(leaked))


def validate_gdskin_evidence(payload: dict[str, Any]) -> None:
    meta = payload.get("meta", {})
    trace = payload.get("serial_request_trace", [])
    intervals = [
        item.get("interval_seconds_from_previous")
        for item in trace
        if item.get("interval_seconds_from_previous") is not None
    ]
    if not trace or meta.get("serial_request_count") != len(trace):
        raise RuntimeError("FULL 串行请求留痕缺失")
    if not intervals or any(value < trial.REQUEST_INTERVAL_SECONDS for value in intervals):
        raise RuntimeError("FULL 串行请求间隔存在小于 2 秒")
    for failure in payload.get("failures", []):
        evidence = failure.get("evidence") or {}
        raw = trial.clean_text(evidence.get("page_raw_reference"))
        if failure.get("state") != "照片资源不可达" or "\u00a0" not in raw:
            continue
        transport = trial.clean_text(evidence.get("transport_url"))
        attempts = failure.get("attempts") or []
        if "%C2%A0" not in transport or not any(
            "%C2%A0" in trial.clean_text(item.get("final_url"))
            for item in attempts
        ):
            raise RuntimeError(
                f"FULL NBSP 原引用/编码传输证据不完整：{failure.get('name')}"
            )


def validate_full_payload(
    payload: dict[str, Any], photo_root: Path, audit_sheet: Path, visual_root: Path
) -> None:
    enforce_repository_relative_payload(payload)
    ORIGINAL_FRAMEWORK_VALIDATE_FULL_PAYLOAD(
        payload, photo_root, audit_sheet, visual_root
    )
    validate_gdskin_evidence(payload)


def write_full_report(path: Path, payload: dict[str, Any]) -> None:
    enforce_repository_relative_payload(payload)
    ORIGINAL_FRAMEWORK_WRITE_FULL_REPORT(path, payload)
    text = path.read_text(encoding="utf-8")
    if str(ROOT) in text or ROOT.as_posix() in text or r"D:\workspace" in text:
        raise RuntimeError("FULL report 泄漏仓库绝对路径")


def configure_framework() -> None:
    trial.configure_framework()
    master_paths = {
        "MASTER_JSON_PATH": trial.base.MASTER_JSON_PATH,
        "MASTER_CSV_PATH": trial.base.MASTER_CSV_PATH,
        "MASTER_XLSX_PATH": trial.base.MASTER_XLSX_PATH,
        "MASTER_REPORT_PATH": trial.base.MASTER_REPORT_PATH,
        "LEDGER_PATH": trial.base.LEDGER_PATH,
    }
    for name, value in master_paths.items():
        setattr(trial, name, value)

    compatibility = {
        "safe_photo_part": trial.base.safe_photo_part,
        "atomic_department": trial.base.atomic_department,
        "primary_title": trial.base.primary_title,
        "magic_extension": trial.base.magic_extension,
        "image_dimensions": trial.base.image_dimensions,
        "contact_sheet_font": trial.framework.contact_sheet_font,
        "tree_snapshot": trial.base.tree_snapshot,
        "protected_snapshot": normalized_trial_protected_snapshot,
        "validate_payload": validate_trial_payload_for_full,
        "validate_manifest": validate_trial_manifest,
        "page_referenced_photo_url": page_referenced_photo_url_for_full,
        "size_buckets": size_buckets,
        "HttpResult": HttpResult,
        "MediaAnalysis": MediaAnalysis,
        "OfficialUrlOpenSession": OfficialUrlOpenSession,
        "TEMPLATE_SIGNATURE": TEMPLATE_SIGNATURE,
        "MAX_PHOTO_BYTES": MAX_PHOTO_BYTES,
        "OWNER_REPORT_BYTES": OWNER_REPORT_BYTES,
        "PLACEHOLDER_PATH_MARKERS": trial.base.PLACEHOLDER_MARKERS,
        "comparable_host": trial.framework.comparable_host,
        "utc_now": trial.framework.utc_now,
        "unquote": unquote,
        "urlparse": urlparse,
    }
    for name, value in compatibility.items():
        setattr(trial, name, value)

    framework_values = {
        "trial": trial,
        "ROOT": ROOT,
        "WORK_DIR": WORK_DIR,
        "SOURCE_DIR": trial.SOURCE_DIR,
        "HOSPITAL": HOSPITAL,
        "ISSUE_NUMBER": ISSUE_NUMBER,
        "MASTER_JSON_PATH": trial.MASTER_JSON_PATH,
        "MASTER_CSV_PATH": trial.MASTER_CSV_PATH,
        "MASTER_XLSX_PATH": trial.MASTER_XLSX_PATH,
        "MASTER_REPORT_PATH": trial.MASTER_REPORT_PATH,
        "LEDGER_PATH": trial.LEDGER_PATH,
        "PROFILE_DIR": PROFILE_DIR,
        "FORMAL_PHOTO_DIR": FORMAL_PHOTO_DIR,
        "EXPECTED_SCOPE_COUNT": EXPECTED_SCOPE_COUNT,
        "EXPECTED_TRIAL_REUSE_COUNT": EXPECTED_TRIAL_REUSE_COUNT,
        "EXPECTED_FRESH_COUNT": EXPECTED_FRESH_COUNT,
        "EXPECTED_PROFILE_COUNT": EXPECTED_SCOPE_COUNT,
        "FULL_BASENAME": FULL_BASENAME,
        "FULL_JSON_PATH": FULL_JSON_PATH,
        "FULL_CSV_PATH": FULL_CSV_PATH,
        "FULL_REPORT_PATH": FULL_REPORT_PATH,
        "FULL_AUDIT_SHEET_PATH": FULL_AUDIT_SHEET_PATH,
        "FULL_VISUAL_DIR": FULL_VISUAL_DIR,
        "PHOTO_RELATIVE_ROOT": PHOTO_RELATIVE_ROOT,
        "FULL_AUTHORIZATION": FULL_AUTHORIZATION,
        "REQUEST_MODE": REQUEST_MODE,
        "VISUAL_PAGE_SIZE": VISUAL_PAGE_SIZE,
        "HOME_IS_GATE": False,
        "PULL_REQUEST_NUMBER": PULL_REQUEST_NUMBER,
        "OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS": {},
        "FULL_PROTECTED_FILES": FULL_PROTECTED_FILES,
        "analyze_full_doctor_media": analyze_full_doctor_media,
        "placeholder_response_reason": placeholder_response_reason,
        "validate_full_page_title": validate_full_page_title,
        "immutable_snapshot": immutable_snapshot,
        "validate_full_payload": validate_full_payload,
        "write_full_report": write_full_report,
        "decorate_owner_approved_duplicate_groups": None,
        "validate_owner_approved_duplicate_groups": None,
    }
    for name, value in framework_values.items():
        setattr(framework, name, value)


def run_full(run_date: str) -> dict[str, Any]:
    configure_framework()
    TITLE_VARIANCE_EVIDENCE.clear()
    REFERENCE_EVIDENCE_BY_SOURCE.clear()
    FULL_REQUEST_TRACE.clear()
    return framework.run_full(run_date)


def validate_full_installation(payload: dict[str, Any]) -> None:
    configure_framework()
    ORIGINAL_FRAMEWORK_VALIDATE_FULL_INSTALLATION(payload)
    validate_gdskin_evidence(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Issue #{ISSUE_NUMBER} {HOSPITAL} photo-backfill FULL"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--full", action="store_true")
    mode.add_argument("--validate-full", action="store_true")
    mode.add_argument("--mark-visual-pass", action="store_true")
    parser.add_argument("--run-date", default=date.today().isoformat())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_framework()
    if args.full:
        payload = run_full(args.run_date)
        print(
            "FULL_DONE "
            f"expected={payload['meta']['expected_count']} "
            f"downloaded={payload['meta']['downloaded_count']} "
            f"failed={payload['meta']['failed_count']} "
            f"profiles={payload['meta']['profile_refreshed_count']}"
        )
        return
    if args.mark_visual_pass:
        payload = framework.mark_visual_pass()
        print(
            "FULL_VISUAL_REVIEW_MARKED "
            f"status={payload['meta']['visual_review_status']}"
        )
        return
    payload = framework.load_full_payload()
    validate_full_installation(payload)
    print(
        "FULL_VALIDATED "
        f"expected={payload['meta']['expected_count']} "
        f"downloaded={payload['meta']['downloaded_count']} "
        f"failed={payload['meta']['failed_count']}"
    )


if __name__ == "__main__":
    main()
