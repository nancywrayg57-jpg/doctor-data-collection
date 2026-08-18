from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import re
import shutil
import tempfile
import time
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote, urljoin, urlparse

from PIL import Image, ImageDraw, ImageOps

import gdzy5413_photo_backfill_trial as trial


ROOT = trial.ROOT
WORK_DIR = trial.WORK_DIR
SOURCE_DIR = trial.SOURCE_DIR
HOSPITAL = trial.HOSPITAL
ISSUE_NUMBER = trial.ISSUE_NUMBER
MASTER_JSON_PATH = trial.MASTER_JSON_PATH
MASTER_CSV_PATH = trial.MASTER_CSV_PATH
MASTER_XLSX_PATH = trial.MASTER_XLSX_PATH
MASTER_REPORT_PATH = trial.MASTER_REPORT_PATH
PROFILE_DIR = trial.PROFILE_DIR
FORMAL_PHOTO_DIR = trial.FORMAL_PHOTO_DIR
EXPECTED_SCOPE_COUNT = trial.EXPECTED_SCOPE_COUNT
EXPECTED_PROFILE_COUNT = EXPECTED_SCOPE_COUNT
EXPECTED_TRIAL_REUSE_COUNT = trial.EXPECTED_TRIAL_COUNT
EXPECTED_TRIAL_FAILURE_REUSE_COUNT = 0
EXPECTED_FRESH_COUNT = EXPECTED_SCOPE_COUNT - EXPECTED_TRIAL_REUSE_COUNT
MAX_FAILURE_RATIO = 0.30

FULL_BASENAME = f"{HOSPITAL}_photo_backfill_full"
FULL_JSON_PATH = WORK_DIR / f"{FULL_BASENAME}_payload.json"
FULL_CSV_PATH = WORK_DIR / f"{FULL_BASENAME}_reconciliation.csv"
FULL_REPORT_PATH = WORK_DIR / f"{FULL_BASENAME}_report.md"
FULL_AUDIT_SHEET_PATH = WORK_DIR / f"{FULL_BASENAME}_audit_sheet.jpg"
FULL_BLOCKER_JSON_PATH = WORK_DIR / f"{FULL_BASENAME}_blocker.json"
FLICKER_PROBE_JSON_PATH = WORK_DIR / f"{FULL_BASENAME}_flicker_probe.json"
FLICKER_PROBE_PHOTO_PATH = WORK_DIR / f"{FULL_BASENAME}_flicker_probe_photo.bin"
PHOTO_RELATIVE_ROOT = Path("01_试点医院") / HOSPITAL / "照片"
LEDGER_JSON_PATH = WORK_DIR / "pearl_delta_hospital_entry_ledger.json"
LEDGER_CSV_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.csv"
LEDGER_XLSX_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"
FULL_PROTECTED_FILES = (
    MASTER_REPORT_PATH,
    LEDGER_JSON_PATH,
    LEDGER_CSV_PATH,
    LEDGER_XLSX_PATH,
)
FULL_FAILURE_STATES = ("详情不可达", "照片资源不可达", "无照片容器", "占位图")
FULL_WARNING_BY_STATE = {
    state: f"官网本人职业照补录失败：{state}" for state in FULL_FAILURE_STATES
}
FULL_WARNING_BY_STATE["照片资源不可达"] = (
    "官网本人职业照补录失败：照片资源不可达（详情页存在唯一本人照片引用，资源不可达）"
)
FULL_ALLOWED_ROW_COLUMNS = {"照片链接", "照片文件", "异常提示"}
FULL_AUTHORIZATION = (
    "PR #74 owner comment 2026-08-18T15:56:41Z: "
    "TRIAL_AUDIT_PASSED -> FULL_APPEND_AND_OBSIDIAN; reuse 10 audited TRIAL photos "
    "and collect the remaining 332 official detail URLs from the two diagnosed "
    "portrait containers with URL and response-content placeholder gates"
)
AUTO_MARKER = "<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->"
FLICKER_PROBE_ROUNDS = 5
FLICKER_PROBE_INTERVAL_SECONDS = 60.0
FLICKER_PROBE_ORIGIN = "FULL_FLICKER_PROBE_REUSE"
RESOURCE_FAILURE_PAUSE_COUNT = 10


@dataclass(frozen=True)
class FullMediaAnalysis:
    state: str
    photo_url: str
    reference_count: int
    excluded_resources: tuple[dict[str, Any], ...]
    detection_feature: str
    template_signature: str


def row_value(value: Any) -> str:
    return "" if value is None else str(value)


def normalized_person_name(value: Any) -> str:
    return re.sub(r"\s+", "", trial.clean_text(value))


def normalized_photo_reference(photo_url: str, source_link: str) -> tuple[str, str]:
    normalized = trial.page_referenced_photo_url(photo_url, source_link)
    return normalized, trial.detail_template(source_link)


def media_failure_evidence(
    analysis: FullMediaAnalysis,
    attempts: list[dict[str, Any]],
) -> dict[str, Any]:
    resource_urls = [
        trial.clean_text(item.get("url"))
        for item in analysis.excluded_resources
        if trial.clean_text(item.get("url"))
    ]
    if not resource_urls:
        resource_urls = [trial.clean_text(attempts[-1].get("final_url"))] if attempts else []
    return {
        "observed_utc": trial.clean_text(attempts[-1].get("utc")) if attempts else "",
        "detail_http": attempts[-1].get("status") if attempts else None,
        "photo_reference_count": analysis.reference_count,
        "resource_urls": [item for item in resource_urls if item],
        "excluded_resources": [dict(item) for item in analysis.excluded_resources],
        "detection_feature": analysis.detection_feature,
        "template_signature": analysis.template_signature,
    }


def analyze_doctor_media(
    page_html: str, source_link: str, expected_name: str
) -> FullMediaAnalysis:
    template = trial.detail_template(source_link)
    if template == "specialist":
        name_match = re.search(
            r'<div\b[^>]*class=["\'][^"\']*\bdocimg_title\b[^"\']*["\'][^>]*>'
            r"(.*?)</div>",
            page_html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        page_name = trial.html_visible_text(name_match.group(1)) if name_match else ""
        if normalized_person_name(page_name) != normalized_person_name(expected_name):
            raise RuntimeError(
                f"specialist 详情姓名不一致：期望 {expected_name}，页面 {page_name or '空'}"
            )
        section_match = re.search(
            r'<div\b[^>]*class=["\'][^"\']*\bmain_left_img\b[^"\']*["\'][^>]*>'
            r"(.*?)"
            r'<div\b[^>]*class=["\'][^"\']*\bkeylist_bg\b',
            page_html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if not section_match:
            return FullMediaAnalysis(
                "无照片容器",
                "",
                0,
                ({"url": source_link, "reason": "main_left_img 医生照片容器缺失"},),
                "specialist 页面姓名一致，但 .main_left_img 医生照片容器缺失",
                ".main_left_img inline background:url(...)"
            )
        raw_candidates = re.findall(
            r"background\s*:\s*url\(([^)]+)\)",
            section_match.group(1),
            flags=re.IGNORECASE,
        )
        signature = ".main_left_img inline background:url(...)"
    elif template == "ksdoctorinfo":
        name_match = re.search(
            r"姓名\s*[：:]\s*([^<\r\n]+)", page_html, flags=re.IGNORECASE
        )
        page_name = (
            trial.clean_text(trial.html_module.unescape(name_match.group(1)))
            if name_match
            else ""
        )
        if normalized_person_name(page_name) != normalized_person_name(expected_name):
            raise RuntimeError(
                f"ksdoctorinfo 详情姓名不一致：期望 {expected_name}，页面 {page_name or '空'}"
            )
        matching_tags: list[tuple[str, dict[str, str]]] = []
        for match in re.finditer(
            r"<img\b[^>]*>", page_html, flags=re.IGNORECASE | re.DOTALL
        ):
            tag = match.group(0)
            attrs = trial.attribute_map(tag)
            if (
                attrs.get("width", "").lower() == "120px"
                and attrs.get("height", "").lower() == "155px"
            ):
                matching_tags.append((tag, attrs))
        if len(matching_tags) > 1:
            raise RuntimeError(
                f"ksdoctorinfo 120×155 资料卡照片标签多于 1：{source_link}"
            )
        raw_candidates = (
            [matching_tags[0][1].get("src", "")] if matching_tags else []
        )
        signature = (
            "资料卡 div[style*='width: 120px'] > "
            "img[width='120px'][height='155px']"
        )
    else:
        raise RuntimeError(f"非授权详情模板：{source_link}")

    if len(raw_candidates) != 1:
        return FullMediaAnalysis(
            "无照片容器",
            "",
            len(raw_candidates),
            ({"url": source_link, "reason": "授权本人照片容器没有唯一照片引用"},),
            f"{template} 授权本人照片容器引用数={len(raw_candidates)}",
            signature,
        )
    raw_candidate = trial.clean_text(raw_candidates[0]).strip("\"'")
    candidate_url = urljoin(source_link, raw_candidate)
    candidate_path = unquote(urlparse(candidate_url).path)
    if not raw_candidate or candidate_path.rstrip("/").lower() == "/uploadfiles/image":
        return FullMediaAnalysis(
            "无照片容器",
            "",
            0,
            ({"url": candidate_url or source_link, "reason": "照片引用为空目录且无文件名"},),
            f"{template} 本人照片容器存在，但 src/background 为空或仅为 /UploadFiles/image/",
            signature,
        )
    lowered_url = candidate_url.lower()
    if any(marker in lowered_url for marker in trial.PLACEHOLDER_MARKERS):
        return FullMediaAnalysis(
            "占位图",
            "",
            1,
            ({"url": candidate_url, "reason": "照片 URL 命中占位图命名特征"},),
            "页面唯一本人照片引用命中 default/placeholder/nopic/noimage URL 特征",
            signature,
        )
    parsed = trial.analyze_page(page_html, source_link, page_name)
    return FullMediaAnalysis(
        "",
        trial.clean_text(parsed["photo_url"]),
        int(parsed.get("candidate_count") or 0),
        tuple(dict(item) for item in parsed.get("excluded_resources", [])),
        trial.clean_text(parsed.get("detection_feature")),
        trial.clean_text(parsed.get("container_selector")),
    )


def failure_evidence_text(evidence: dict[str, Any]) -> str:
    return json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def persist_resource_failure_blocker(failures: list[dict[str, Any]]) -> None:
    resource_failures = [
        item for item in failures if item.get("state") == "照片资源不可达"
    ]
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "phase": "FULL_PAUSED_RESOURCE_FAILURE_BATCH",
            "threshold": RESOURCE_FAILURE_PAUSE_COUNT,
            "count": len(resource_failures),
            "generated_at_utc": trial.utc_now(),
        },
        "failures": resource_failures,
    }
    staging = FULL_BLOCKER_JSON_PATH.with_name(
        f".{FULL_BLOCKER_JSON_PATH.name}.staging"
    )
    staging.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    staging.replace(FULL_BLOCKER_JSON_PATH)


def is_fresh_failure_origin(origin: Any) -> bool:
    return trial.clean_text(origin) != "TRIAL_FAILURE_REUSE"


def file_digest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exists": False}
    content = path.read_bytes()
    return {
        "exists": True,
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def append_failure_warning(value: Any, state: str) -> str:
    if state not in FULL_WARNING_BY_STATE:
        raise ValueError(f"未知照片失败状态：{state}")
    warning = FULL_WARNING_BY_STATE[state]
    existing = [item for item in trial.clean_text(value).split("；") if item]
    if warning not in existing:
        existing.append(warning)
    return "；".join(existing)


def allocate_full_photo_path(
    row: dict[str, Any],
    source_id: str,
    extension: str,
    output_dir: Path,
    used_filenames: set[str],
) -> tuple[str, Path]:
    stem = "-".join(
        [
            trial.safe_photo_part(row.get("姓名")),
            trial.atomic_department(row),
            trial.safe_photo_part(
                trial.primary_title(row.get("职称_关键词") or row.get("职称身份原文"))
            ),
            trial.safe_photo_part(HOSPITAL),
        ]
    )
    filename = f"{stem}.{extension}"
    folded = filename.casefold()
    if folded in used_filenames:
        filename = f"{stem}-{trial.safe_photo_part(source_id)}.{extension}"
        folded = filename.casefold()
    if folded in used_filenames or (output_dir / filename).exists():
        raise RuntimeError(f"照片命名仍冲突，拒绝覆盖：{filename}")
    used_filenames.add(folded)
    return filename, output_dir / filename


def response_signature(item: dict[str, Any]) -> str:
    if item.get("error"):
        return f"ERROR {item['error']}"
    return f"HTTP {item.get('status')} {item.get('content_type') or ''}"


def attempts_flicker(attempts: list[dict[str, Any]]) -> bool:
    return len({response_signature(item) for item in attempts}) > 1


def fetch_with_retry(
    session: trial.common.OfficialSession,
    url: str,
    referer: str,
    accept: Callable[[trial.common.HttpResult], bool],
    sleep_func: Callable[[float], None] = time.sleep,
) -> tuple[trial.common.HttpResult | None, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    last_result: trial.common.HttpResult | None = None
    for attempt_index in range(3):
        try:
            result = session.get(url, referer=referer)
            last_result = result
            attempts.append(
                {
                    "attempt": attempt_index + 1,
                    "utc": trial.utc_now(),
                    "status": result.status,
                    "content_type": result.content_type,
                    "final_url": result.final_url,
                    "error": "",
                }
            )
            if accept(result):
                return result, attempts
        except RuntimeError as exc:
            attempts.append(
                {
                    "attempt": attempt_index + 1,
                    "utc": trial.utc_now(),
                    "status": None,
                    "content_type": "",
                    "final_url": "",
                    "error": str(exc),
                }
            )
        if attempt_index < 2:
            sleep_func(trial.DETAIL_RETRY_SECONDS)
    return last_result, attempts


def validate_retry_attempts(attempts: list[dict[str, Any]]) -> None:
    if len(attempts) < 3:
        raise RuntimeError("详情不可达证据少于初次请求加 2 次重试")
    parsed: list[datetime] = []
    for expected_attempt, item in enumerate(attempts, start=1):
        if int(item.get("attempt") or 0) != expected_attempt:
            raise RuntimeError("不可达重试序号不连续")
        parsed.append(datetime.fromisoformat(str(item.get("utc"))))
    for earlier, later in zip(parsed, parsed[1:]):
        if (later - earlier).total_seconds() < trial.DETAIL_RETRY_SECONDS - 0.5:
            raise RuntimeError("不可达重试间隔不足 30 秒")


def attempt_evidence(attempts: list[dict[str, Any]]) -> str:
    return " | ".join(
        f"#{item.get('attempt')} {item.get('utc')} {response_signature(item)}"
        for item in attempts
    )


def downloaded_placeholder_reason(
    photo_url: str, content: bytes, extension: str
) -> str:
    try:
        width, height = trial.common.image_dimensions(content)
    except Exception as exc:
        raise RuntimeError(f"照片占位内容门禁无法解码：{photo_url} {exc}") from exc
    reason = trial.placeholder_response_reason(content, width, height)
    if reason:
        return f"照片响应内容判定为占位图：{reason}；{len(content)} bytes；{width}×{height}"
    return ""


def validate_status_flicker_probe(
    payload: dict[str, Any], photo_path: Path
) -> None:
    meta = payload.get("meta", {})
    source = trial.clean_text(meta.get("source_link"))
    photo_url = trial.clean_text(meta.get("photo_url"))
    normalized_url, path_kind = normalized_photo_reference(photo_url, source)
    if not trial.detail_id(source) or normalized_url != photo_url:
        raise RuntimeError("状态闪烁聚合来源或照片 URL 越界")
    if path_kind != meta.get("path_kind"):
        raise RuntimeError("状态闪烁聚合照片路径类型不一致")
    if int(meta.get("round_count") or 0) != FLICKER_PROBE_ROUNDS:
        raise RuntimeError("状态闪烁聚合不是 5 轮")
    rounds = payload.get("rounds", [])
    if len(rounds) != FLICKER_PROBE_ROUNDS:
        raise RuntimeError("状态闪烁聚合轮次证据不完整")
    starts = [datetime.fromisoformat(str(item.get("start_utc"))) for item in rounds]
    if any(
        (later - earlier).total_seconds() < FLICKER_PROBE_INTERVAL_SECONDS
        for earlier, later in zip(starts, starts[1:])
    ):
        raise RuntimeError("状态闪烁聚合相邻轮开始间隔不足 60 秒")
    intervals = [float(item) for item in meta.get("round_intervals_seconds", [])]
    if len(intervals) != FLICKER_PROBE_ROUNDS - 1 or any(
        item < FLICKER_PROBE_INTERVAL_SECONDS for item in intervals
    ):
        raise RuntimeError("状态闪烁聚合单调时钟间隔证据不足 60 秒")
    captured_round = int(meta.get("captured_round") or 0)
    if captured_round == 0:
        if meta.get("resolution_state") != "照片资源不可达":
            raise RuntimeError("状态闪烁聚合全失败未定格为照片资源不可达")
        if photo_path.exists():
            raise RuntimeError("状态闪烁聚合全失败却存在冻结照片")
        if any(
            item.get("photo_state") not in {"照片资源不可达", ""}
            or (
                item.get("photo_state") == ""
                and not item.get("detail_state")
                and not item.get("error")
            )
            for item in rounds
        ):
            raise RuntimeError("状态闪烁聚合全失败轮次缺少 HTTP/错误证据")
        return
    if captured_round not in range(1, FLICKER_PROBE_ROUNDS + 1):
        raise RuntimeError("状态闪烁聚合 captured_round 越界")
    if meta.get("resolution_state") != "CAPTURED":
        raise RuntimeError("状态闪烁聚合已冻结照片但状态未标记 CAPTURED")
    if not photo_path.is_file():
        raise RuntimeError("状态闪烁聚合冻结照片缺失")
    content = photo_path.read_bytes()
    if len(content) != int(meta.get("bytes") or 0):
        raise RuntimeError("状态闪烁聚合冻结照片字节数不一致")
    if hashlib.sha256(content).hexdigest() != meta.get("sha256"):
        raise RuntimeError("状态闪烁聚合冻结照片 SHA-256 不一致")
    extension = trial.clean_text(meta.get("extension"))
    media_type = "image/jpeg" if extension == "jpg" else f"image/{extension}"
    if trial.common.magic_extension(content, media_type) != extension:
        raise RuntimeError("状态闪烁聚合冻结照片魔数不一致")
    if trial.common.image_dimensions(content) != (
        int(meta.get("width") or 0),
        int(meta.get("height") or 0),
    ):
        raise RuntimeError("状态闪烁聚合冻结照片尺寸不一致")
    if len(content) > trial.MAX_PHOTO_BYTES:
        raise RuntimeError("状态闪烁聚合冻结照片超过 20 MiB")
    if downloaded_placeholder_reason(photo_url, content, extension):
        raise RuntimeError("状态闪烁聚合冻结照片为占位图")
    if trial.comparable_host(meta.get("photo_final_url", "")) != trial.OFFICIAL_HOST:
        raise RuntimeError("状态闪烁聚合冻结照片最终响应越出官网")


def run_status_flicker_probe(
    source_link: str,
    photo_url: str,
    *,
    session_factory: Callable[[], trial.common.OfficialSession] = trial.common.OfficialSession,
    sleeper: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
    utc_now: Callable[[], str] = trial.utc_now,
    output_json_path: Path = FLICKER_PROBE_JSON_PATH,
    output_photo_path: Path = FLICKER_PROBE_PHOTO_PATH,
) -> dict[str, Any]:
    if output_json_path.exists() or output_photo_path.exists():
        raise RuntimeError("状态闪烁聚合工件已存在，拒绝覆盖")
    source = trial.clean_text(source_link)
    normalized_url, path_kind = normalized_photo_reference(photo_url, source)
    if not trial.detail_id(source) or not normalized_url:
        raise RuntimeError("状态闪烁聚合来源或照片 URL 不在 Issue #73 授权范围")
    matching_rows = [
        row
        for row in trial.load_scope_rows()
        if trial.clean_text(row.get("来源链接")) == source
    ]
    if len(matching_rows) != 1:
        raise RuntimeError("状态闪烁聚合来源不在 342 行固定范围内且唯一")
    row = matching_rows[0]
    name = trial.clean_text(row.get("姓名"))
    round_start_monotonic: list[float] = []
    round_evidence: list[dict[str, Any]] = []
    captured_content: bytes | None = None
    captured_meta: dict[str, Any] = {}

    for round_number in range(1, FLICKER_PROBE_ROUNDS + 1):
        if round_start_monotonic:
            remaining = FLICKER_PROBE_INTERVAL_SECONDS - (
                monotonic() - round_start_monotonic[-1]
            )
            if remaining > 0:
                sleeper(remaining)
        started_monotonic = monotonic()
        started_utc = utc_now()
        round_start_monotonic.append(started_monotonic)
        item: dict[str, Any] = {
            "round": round_number,
            "start_utc": started_utc,
            "home_status": None,
            "detail_status": None,
            "detail_state": "",
            "photo_status": None,
            "photo_state": "",
            "photo_bytes": 0,
            "photo_sha256": "",
            "error": "",
        }
        session = session_factory()
        try:
            home = session.get(trial.OFFICIAL_HOME)
            item["home_status"] = home.status
            if home.status != 200 or home.content_type != "text/html":
                item["error"] = f"官网首页会话门禁失败：HTTP {home.status}"
                round_evidence.append(item)
                continue
            detail = session.get(source, referer=trial.DIRECTORY_URL)
            item["detail_status"] = detail.status
            if detail.status != 200 or detail.content_type != "text/html":
                item["detail_state"] = "详情不可达"
                round_evidence.append(item)
                continue
            html = detail.content.decode(detail.charset or "utf-8", errors="replace")
            reference = analyze_doctor_media(html, source, name)
            state = reference.state
            item["detail_state"] = state
            if state or reference is None:
                round_evidence.append(item)
                continue
            if reference.photo_url != normalized_url:
                raise RuntimeError(
                    "状态闪烁聚合页面实际引用照片发生漂移："
                    f"{reference.photo_url} != {normalized_url}"
                )
            if captured_content is not None:
                item["photo_state"] = (
                    f"已冻结第 {captured_meta['captured_round']} 轮原始照片，后续轮不覆盖"
                )
                round_evidence.append(item)
                continue
            photo = session.get(normalized_url, referer=source)
            item["photo_status"] = photo.status
            if photo.status != 200 or not photo.content_type.startswith("image/"):
                item["photo_state"] = "照片资源不可达"
                round_evidence.append(item)
                continue
            if trial.comparable_host(photo.final_url) != trial.OFFICIAL_HOST:
                raise RuntimeError("状态闪烁聚合照片重定向越出官网")
            extension = trial.common.magic_extension(photo.content, photo.content_type)
            if not extension:
                raise RuntimeError("状态闪烁聚合照片格式异常")
            if len(photo.content) > trial.MAX_PHOTO_BYTES:
                raise RuntimeError("状态闪烁聚合照片超过 20 MiB")
            placeholder = downloaded_placeholder_reason(
                normalized_url, photo.content, extension
            )
            if placeholder:
                item["photo_state"] = "占位图"
                item["error"] = placeholder
                round_evidence.append(item)
                continue
            width, height = trial.common.image_dimensions(photo.content)
            digest = hashlib.sha256(photo.content).hexdigest()
            captured_content = photo.content
            captured_meta = {
                "captured_round": round_number,
                "photo_final_url": photo.final_url,
                "extension": extension,
                "bytes": len(photo.content),
                "width": width,
                "height": height,
                "sha256": digest,
            }
            item["photo_state"] = "当轮冻结"
            item["photo_bytes"] = len(photo.content)
            item["photo_sha256"] = digest
        except RuntimeError as exc:
            item["error"] = str(exc)
        round_evidence.append(item)

    intervals = [
        round_start_monotonic[index] - round_start_monotonic[index - 1]
        for index in range(1, len(round_start_monotonic))
    ]
    if captured_content is None:
        captured_meta = {
            "captured_round": 0,
            "resolution_state": "照片资源不可达",
            "photo_final_url": "",
            "extension": "",
            "bytes": 0,
            "width": 0,
            "height": 0,
            "sha256": "",
        }
    else:
        captured_meta["resolution_state"] = "CAPTURED"
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "phase": "FULL_STATUS_FLICKER_AGGREGATED",
            "source_link": source,
            "name": name,
            "photo_url": normalized_url,
            "path_kind": path_kind,
            "round_count": FLICKER_PROBE_ROUNDS,
            "round_intervals_seconds": intervals,
            **captured_meta,
        },
        "rounds": round_evidence,
    }
    with tempfile.TemporaryDirectory(
        prefix="issue73_flicker_probe_", dir=WORK_DIR
    ) as temporary:
        temporary_root = Path(temporary)
        temporary_photo = temporary_root / output_photo_path.name
        temporary_json = temporary_root / output_json_path.name
        if captured_content is not None:
            temporary_photo.write_bytes(captured_content)
        temporary_json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        validate_status_flicker_probe(payload, temporary_photo)
        photo_staging = output_photo_path.with_name(
            f".{output_photo_path.name}.staging"
        )
        json_staging = output_json_path.with_name(
            f".{output_json_path.name}.staging"
        )
        try:
            shutil.copy2(temporary_json, json_staging)
            if captured_content is not None:
                shutil.copy2(temporary_photo, photo_staging)
                photo_staging.replace(output_photo_path)
            json_staging.replace(output_json_path)
        finally:
            photo_staging.unlink(missing_ok=True)
            json_staging.unlink(missing_ok=True)
    return payload


def collect_full_row_diffs(
    before_rows: list[dict[str, Any]],
    after_rows: list[dict[str, Any]],
    target_sources: set[str],
) -> list[dict[str, str]]:
    if len(before_rows) != len(after_rows):
        raise RuntimeError("FULL 前后总底表行数发生变化")
    diffs: list[dict[str, str]] = []
    for sheet_row, (before, after) in enumerate(
        zip(before_rows, after_rows, strict=True), start=2
    ):
        for column in trial.BASE_HEADERS:
            old = row_value(before.get(column))
            new = row_value(after.get(column))
            if old == new:
                continue
            source = trial.clean_text(after.get("来源链接"))
            diffs.append(
                {
                    "底表行": str(sheet_row),
                    "序号": trial.clean_text(after.get("序号")),
                    "姓名": trial.clean_text(after.get("姓名")),
                    "来源链接": source,
                    "列名": column,
                    "修改前": old,
                    "修改后": new,
                }
            )
            if source not in target_sources:
                raise RuntimeError(f"发现 Issue #73 范围外行修改：{source} {column}")
    unexpected = sorted({item["列名"] for item in diffs} - FULL_ALLOWED_ROW_COLUMNS)
    if unexpected:
        raise RuntimeError("发现范围外字段修改：" + "、".join(unexpected))
    return diffs


def recompute_failure_derivatives(
    payload: dict[str, Any], rows: list[dict[str, Any]]
) -> None:
    warning_counter: Counter[str] = Counter()
    for row in rows:
        for warning in trial.clean_text(row.get("异常提示")).split("；"):
            if warning:
                warning_counter[warning] += 1
    payload["warning_counts"] = dict(warning_counter)
    import collect_official_doctors_batch as collector

    payload["hospital_batches"] = collector.build_hospital_batches(rows)


def canonical_master_row(row: dict[str, Any]) -> tuple[str, ...]:
    return tuple(row_value(row.get(header)) for header in trial.BASE_HEADERS)


def write_master_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=trial.BASE_HEADERS)
        writer.writeheader()
        writer.writerows(
            {key: row.get(key, "") for key in trial.BASE_HEADERS} for row in rows
        )


def validate_master_layers(
    payload_path: Path, csv_path: Path, xlsx_path: Path
) -> list[dict[str, Any]]:
    import generate_obsidian_profiles as profiles

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    payload_rows = payload.get("rows", [])
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    xlsx_rows = profiles.read_xlsx_rows_basic(xlsx_path)
    expected = [canonical_master_row(row) for row in payload_rows]
    if [canonical_master_row(row) for row in csv_rows] != expected:
        raise RuntimeError("总底表 payload 与 CSV 不一致")
    if [canonical_master_row(row) for row in xlsx_rows] != expected:
        raise RuntimeError("总底表 payload 与 XLSX 自动采集底表不一致")
    return [dict(row) for row in payload_rows]


def write_full_reconciliation_csv(path: Path, payload: dict[str, Any]) -> None:
    headers = [
        "姓名",
        "来源链接",
        "状态",
        "失败分类",
        "照片链接",
        "照片文件",
        "实际格式",
        "字节数",
        "SHA-256",
        "宽",
        "高",
        "来源批次",
        "错误证据",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(
            {header: item.get(header, "") for header in headers}
            for item in payload["reconciliation"]
        )


def profile_photo_markdown_path(photo_file: str) -> str:
    markdown_path = "/".join(Path(photo_file.replace("\\", "/")).parts[-2:])
    if not markdown_path.startswith("照片/"):
        raise RuntimeError(f"画像照片相对路径越界：{photo_file}")
    return markdown_path


def insert_profile_photo_block(
    before_text: str, doctor_name: str, photo_file: str
) -> str:
    markdown_path = profile_photo_markdown_path(photo_file)
    if re.search(r"(?m)^!\[[^\]]*\]\(照片/[^)]+\)[ \t\r]*$", before_text):
        raise RuntimeError(f"画像已存在照片嵌入区块：{doctor_name}")
    marker = re.compile(r"(?m)^## 基础信息[ \t]*(?P<newline>\r\n|\n)(?P=newline)")
    matches = list(marker.finditer(before_text))
    if len(matches) != 1:
        raise RuntimeError(f"画像基础信息插入点不唯一：{doctor_name} 数量={len(matches)}")
    match = matches[0]
    newline = match.group("newline")
    photo_block = f"![{doctor_name}]({markdown_path}){newline}{newline}"
    return before_text[: match.end()] + photo_block + before_text[match.end() :]


def insert_profile_photo_block_bytes(
    before_bytes: bytes, doctor_name: str, photo_file: str
) -> bytes:
    bom = b"\xef\xbb\xbf" if before_bytes.startswith(b"\xef\xbb\xbf") else b""
    body = before_bytes[len(bom) :]
    try:
        before_text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"画像不是有效 UTF-8：{doctor_name}") from exc
    return bom + insert_profile_photo_block(
        before_text, doctor_name, photo_file
    ).encode("utf-8")


def validate_profile_photo_only_bytes(
    before_bytes: bytes, after_bytes: bytes, doctor_name: str, photo_file: str
) -> None:
    expected = insert_profile_photo_block_bytes(before_bytes, doctor_name, photo_file)
    if after_bytes != expected:
        raise RuntimeError(f"画像出现照片嵌入区块以外字节变化：{doctor_name}")
    before_lines = before_bytes.decode("utf-8-sig").splitlines()
    after_lines = after_bytes.decode("utf-8-sig").splitlines()
    if len(after_lines) - len(before_lines) != 2:
        raise RuntimeError(f"画像照片最小刷新不是 +2/-0：{doctor_name}")


def profile_markdown_tree(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes() for path in sorted(root.rglob("*.md"))
    }


def validate_profile_tree_surgical(
    before_tree: dict[Path, bytes],
    after_root: Path,
    expected_changed_paths: set[Path],
) -> None:
    after_tree = profile_markdown_tree(after_root)
    if set(after_tree) != set(before_tree):
        raise RuntimeError("画像 Markdown 文件集合发生变化")
    changed_paths = {
        path for path, content in before_tree.items() if after_tree[path] != content
    }
    if changed_paths != expected_changed_paths:
        unexpected = sorted(str(path) for path in changed_paths ^ expected_changed_paths)
        raise RuntimeError("画像外科式变更集合不一致：" + "、".join(unexpected[:5]))


def target_profile_paths(
    profile_root: Path, target_sources: set[str]
) -> dict[str, Path]:
    import generate_obsidian_profiles as profiles

    all_sources = profiles.extract_existing_sources(profile_root)
    missing = target_sources - set(all_sources)
    if missing:
        raise RuntimeError("FULL 前目标范围缺少既有画像：" + "、".join(sorted(missing)[:5]))
    result = {source: all_sources[source] for source in target_sources}
    profile_files = {
        path for path in profile_root.glob("*.md") if path.name != "_索引.md"
    }
    if (
        len(result) != EXPECTED_PROFILE_COUNT
        or len(profile_files) != EXPECTED_PROFILE_COUNT
        or set(result.values()) != profile_files
    ):
        raise RuntimeError("FULL 前 342 个来源与 342 份画像不是一一对应")
    return result


def preflight_profile_bytes(
    profile_paths: dict[str, Path], rows_by_source: dict[str, dict[str, Any]]
) -> dict[str, bytes]:
    before: dict[str, bytes] = {}
    probe_file = (PHOTO_RELATIVE_ROOT / "__preflight__.jpg").as_posix()
    marker_bytes = AUTO_MARKER.encode("utf-8")
    for source, path in profile_paths.items():
        content = path.read_bytes()
        name = trial.clean_text(rows_by_source[source].get("姓名"))
        if marker_bytes not in content:
            raise RuntimeError(f"画像缺少 AUTO 标记：{name}")
        insert_profile_photo_block_bytes(content, name, probe_file)
        before[source] = content
    return before


def select_audit_samples(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(samples) < 10:
        raise RuntimeError("FULL 成功照片不足 10 张，无法生成最小/最大/随机抽样拼图")
    smallest = min(samples, key=lambda item: (int(item["bytes"]), item["source_link"]))
    largest = max(samples, key=lambda item: (int(item["bytes"]), item["source_link"]))
    remaining = [item for item in samples if item not in (smallest, largest)]
    random_like = sorted(
        remaining,
        key=lambda item: hashlib.sha256(item["source_link"].encode("utf-8")).hexdigest(),
    )[:8]
    selected: list[dict[str, Any]] = []
    for kind, item in [("最小", smallest), ("最大", largest)]:
        selected.append({**item, "audit_kind": kind})
    selected.extend({**item, "audit_kind": "确定性随机"} for item in random_like)
    return selected


def build_full_audit_sheet(
    samples: list[dict[str, Any]], photo_root: Path, output_path: Path
) -> list[dict[str, Any]]:
    selected = select_audit_samples(samples)
    canvas = Image.new("RGB", (1600, 840), "white")
    draw = ImageDraw.Draw(canvas)
    name_font = trial.contact_sheet_font(22)
    meta_font = trial.contact_sheet_font(15)
    for index, item in enumerate(selected):
        row, col = divmod(index, 5)
        left = 20 + col * 316
        top = 10 + row * 410
        with Image.open(photo_root / item["filename"]) as image:
            preview = ImageOps.contain(image.convert("RGB"), (280, 300))
        x = left + (280 - preview.width) // 2
        canvas.paste(preview, (x, top))
        draw.text((left, top + 305), f"{item['audit_kind']}｜{item['name']}", fill="black", font=name_font)
        draw.text(
            (left, top + 338),
            f"{item['department']}｜{item['title']}",
            fill="#333333",
            font=meta_font,
        )
        draw.text(
            (left, top + 365),
            f"{item['width']}×{item['height']}｜{int(item['bytes']):,} B",
            fill="#555555",
            font=meta_font,
        )
    canvas.save(output_path, "JPEG", quality=92)
    return [
        {
            "audit_kind": item["audit_kind"],
            "name": item["name"],
            "source_link": item["source_link"],
            "filename": item["filename"],
            "bytes": item["bytes"],
            "sha256": item["sha256"],
        }
        for item in selected
    ]


def ensure_workspace_target(path: Path) -> None:
    root = ROOT.resolve()
    resolved = path.resolve()
    if resolved == root or root not in resolved.parents:
        raise RuntimeError(f"拒绝操作工作区外路径：{path}")


def backup_file_targets(
    targets: list[Path], backup_root: Path
) -> dict[Path, Path | None]:
    backups: dict[Path, Path | None] = {}
    backup_root.mkdir(parents=True, exist_ok=True)
    for index, target in enumerate(targets):
        ensure_workspace_target(target)
        if target.exists():
            backup = backup_root / f"{index:04d}_{target.name}"
            shutil.copy2(target, backup)
            backups[target] = backup
        else:
            backups[target] = None
    return backups


def apply_file_map(file_map: dict[Path, Path]) -> None:
    for target, source in file_map.items():
        ensure_workspace_target(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = target.with_name(f".{target.name}.issue73.tmp")
        if staging.exists():
            staging.unlink()
        shutil.copy2(source, staging)
        staging.replace(target)


def restore_file_targets(backups: dict[Path, Path | None]) -> None:
    for target, backup in backups.items():
        staging = target.with_name(f".{target.name}.issue73.restore")
        if staging.exists():
            staging.unlink()
        if backup is None:
            target.unlink(missing_ok=True)
            continue
        shutil.copy2(backup, staging)
        staging.replace(target)


def write_full_report(path: Path, payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    failure_lines = "\n".join(
        f"| {state} | {meta['failure_state_counts'].get(state, 0)} |"
        for state in FULL_FAILURE_STATES
    )
    large_lines = "\n".join(
        f"- {item['name']}｜{item['photo_url']}｜{int(item['bytes']):,} bytes｜"
        f"{item['width']}×{item['height']}｜`{item['sha256']}`"
        for item in payload["photo_samples"]
        if int(item["bytes"]) > trial.OWNER_REPORT_BYTES
    ) or "- 无"
    failure_evidence = "\n".join(
        f"- {item['name']}｜{item['state']}｜{item['source_link']}｜{item['error']}"
        for item in payload["failures"]
    ) or "- 无"
    bucket_lines = "\n".join(
        f"| {bucket} | {meta['size_bucket_counts'].get(bucket, 0)} |"
        for bucket in ["<200KiB", "200KiB-1MiB", "1-5MiB", "5-20MiB", ">20MiB"]
    )
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 FULL 报告

> 日期：{meta['run_date']}
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`

## 四数对账

| 目标 | 实采 | 失败 | 落盘 | 留空 |
|---:|---:|---:|---:|---:|
| {meta['expected_count']} | {meta['downloaded_count']} | {meta['failed_count']} | {meta['disk_photo_count']} | {meta['blank_count']} |

- 复用已审计 TRIAL 照片：{meta['trial_reused_count']}；FULL 新抓取成功：{meta['fresh_downloaded_count']}；FULL 新抓取失败：{meta['fresh_failed_count']}；新抓取目标：{meta['fresh_target_count']}。
- 失败率：{meta['failure_ratio']:.2%}；状态闪烁：{meta['status_flicker_count']}；已完成 5 轮聚合闭环：{meta['status_flicker_resolved_count']}。

| 失败四类 | 数量 |
|---|---:|
{failure_lines}

## 大小与来源

| 大小分桶 | 数量 |
|---|---:|
{bucket_lines}

- 总字节：{meta['photo_total_bytes']:,}（{meta['photo_total_mib']:.2f} MiB）；最大：{meta['photo_max_bytes']:,} bytes。
- 超过 5 MiB：{meta['over_5mib_count']}；超过 20 MiB：{meta['over_20mib_count']}。
- 详情模板：{json.dumps(meta['detail_template_counts'], ensure_ascii=False)}；实际魔数格式：{json.dumps(meta['format_counts'], ensure_ascii=False)}。
- 页面未引用路径探测 0；第三方来源 0；TRIAL/正式下载均只使用医生照片容器的页面实际引用。

## >5 MiB Owner 终审清单

{large_lines}

## 失败证据

{failure_evidence}

## 三载体、画像与抽样

- 总底表 payload/CSV/XLSX 逐值一致；仅本院照片两列及失败行异常提示允许变化。
- FULL manifest 对每张照片执行落盘字节数、SHA-256、魔数/扩展名三重复算，且照片目录零孤儿零缺失。
- 成功 {meta['profile_refreshed_count']} 份 AUTO 画像严格 +2/-0；失败画像零触碰；不新建画像；`_索引.md` 零修改。
- FULL 抽样拼图：`{FULL_AUDIT_SHEET_PATH}`，包含最小、最大及 8 个确定性随机样本。
- 入口台账 JSON/CSV/XLSX 与总底表更新报告保持不变。

## 工件

- `{FULL_JSON_PATH}`
- `{FULL_CSV_PATH}`
- `{FULL_REPORT_PATH}`
- `{FULL_AUDIT_SHEET_PATH}`
"""
    path.write_text(report, encoding="utf-8", newline="\n")


def validate_full_payload(
    payload: dict[str, Any], photo_root: Path, audit_sheet_path: Path
) -> None:
    meta = payload.get("meta", {})
    expected = int(meta.get("expected_count") or 0)
    downloaded = int(meta.get("downloaded_count") or 0)
    failed = int(meta.get("failed_count") or 0)
    blank = int(meta.get("blank_count") or 0)
    if expected != EXPECTED_SCOPE_COUNT or downloaded + failed != expected or blank != failed:
        raise RuntimeError("FULL 目标/实采/失败/留空未形成四数闭环")
    if int(meta.get("disk_photo_count") or 0) != downloaded:
        raise RuntimeError("FULL 实采数与照片落盘数不一致")
    if int(meta.get("trial_reused_count") or 0) != EXPECTED_TRIAL_REUSE_COUNT:
        raise RuntimeError("FULL 复用 TRIAL 数量漂移")
    if int(meta.get("trial_failure_reused_count") or 0) != EXPECTED_TRIAL_FAILURE_REUSE_COUNT:
        raise RuntimeError("FULL 复用 TRIAL 失败证据数量漂移")
    if int(meta.get("fresh_target_count") or 0) != EXPECTED_FRESH_COUNT:
        raise RuntimeError("FULL 新抓取目标数量漂移")
    if (
        int(meta.get("fresh_downloaded_count") or 0)
        + int(meta.get("fresh_failed_count") or 0)
        != EXPECTED_FRESH_COUNT
    ):
        raise RuntimeError("FULL 332 个新抓取目标未闭合")
    state_counts = Counter(meta.get("failure_state_counts") or {})
    if set(state_counts) - set(FULL_FAILURE_STATES) or sum(state_counts.values()) != failed:
        raise RuntimeError("FULL 失败四类分布不闭合")
    if expected and failed / expected > MAX_FAILURE_RATIO:
        raise RuntimeError("[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 总问题率超过 30%")
    flicker_count = int(meta.get("status_flicker_count") or 0)
    flicker_resolved = int(meta.get("status_flicker_resolved_count") or 0)
    flicker_probe_reused = int(meta.get("flicker_probe_reused_count") or 0)
    if flicker_count != flicker_resolved or flicker_count != flicker_probe_reused:
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 状态闪烁未完成 5 轮聚合闭环"
        )
    if flicker_count not in (0, 1):
        raise RuntimeError("FULL 状态闪烁聚合来源数量越界")
    if int(meta.get("constructed_unreferenced_probe_count") or 0):
        raise RuntimeError("FULL 发生页面未引用路径探测")
    if int(meta.get("third_party_source_count") or 0):
        raise RuntimeError("FULL 发生第三方来源访问")
    if int(meta.get("existing_profile_count") or 0) != EXPECTED_PROFILE_COUNT:
        raise RuntimeError("FULL 既有画像数量漂移")
    if int(meta.get("profile_refreshed_count") or 0) != downloaded:
        raise RuntimeError("FULL 实采照片数与画像刷新数不一致")

    reconciliation = payload.get("reconciliation", [])
    rows = payload.get("rows", [])
    photos = payload.get("photo_samples", [])
    failures = payload.get("failures", [])
    if len(reconciliation) != expected or len(rows) != expected or len(photos) != downloaded:
        raise RuntimeError("FULL 对账、目标行或照片数量不一致")
    rows_by_source = {trial.clean_text(row.get("来源链接")): row for row in rows}
    photos_by_source = {
        trial.clean_text(item.get("source_link")): item for item in photos
    }
    failures_by_source = {
        trial.clean_text(item.get("source_link")): item for item in failures
    }
    if (
        len(rows_by_source) != expected
        or len(photos_by_source) != downloaded
        or len(failures_by_source) != failed
        or set(photos_by_source) | set(failures_by_source) != set(rows_by_source)
        or set(photos_by_source) & set(failures_by_source)
    ):
        raise RuntimeError("FULL 来源链接对账不唯一")
    flicker_probe = payload.get("status_flicker_probe")
    if flicker_count:
        if not isinstance(flicker_probe, dict):
            raise RuntimeError("FULL 状态闪烁聚合证据缺失")
        validate_status_flicker_probe(flicker_probe, FLICKER_PROBE_PHOTO_PATH)
        probe_source = trial.clean_text(flicker_probe["meta"].get("source_link"))
        if int(flicker_probe["meta"].get("captured_round") or 0):
            probe_photo = photos_by_source.get(probe_source)
            if (
                probe_photo is None
                or probe_photo.get("origin") != FLICKER_PROBE_ORIGIN
                or probe_photo.get("sha256") != flicker_probe["meta"].get("sha256")
            ):
                raise RuntimeError("FULL 状态闪烁聚合冻结照片未进入最终工作集")
        else:
            probe_failure = failures_by_source.get(probe_source)
            if (
                probe_failure is None
                or probe_failure.get("origin") != FLICKER_PROBE_ORIGIN
                or probe_failure.get("state") != "照片资源不可达"
            ):
                raise RuntimeError("FULL 状态闪烁聚合失败证据未进入最终工作集")
    elif flicker_probe is not None:
        raise RuntimeError("FULL 无状态闪烁却携带聚合证据")

    expected_files: set[str] = set()
    total_bytes = 0
    max_bytes = 0
    over_5 = 0
    over_20 = 0
    for item in reconciliation:
        source = trial.clean_text(item.get("来源链接"))
        row = rows_by_source[source]
        status = trial.clean_text(item.get("状态"))
        state = trial.clean_text(item.get("失败分类"))
        if status == "实采":
            if state or source not in photos_by_source:
                raise RuntimeError(f"FULL 实采行状态不一致：{source}")
            photo = photos_by_source[source]
            filename = trial.clean_text(photo.get("filename"))
            disk_path = photo_root / filename
            content = disk_path.read_bytes()
            if len(content) != int(photo.get("bytes") or 0):
                raise RuntimeError(f"照片字节数对账失败：{filename}")
            if hashlib.sha256(content).hexdigest() != photo.get("sha256"):
                raise RuntimeError(f"照片 SHA-256 对账失败：{filename}")
            extension = disk_path.suffix.lower().lstrip(".")
            media_type = "image/jpeg" if extension == "jpg" else f"image/{extension}"
            if trial.common.magic_extension(content, media_type) != extension:
                raise RuntimeError(f"照片魔数与扩展名不符：{filename}")
            if trial.clean_text(item.get("实际格式")) != extension:
                raise RuntimeError(f"manifest 实际格式与照片魔数不一致：{filename}")
            if trial.common.image_dimensions(content) != (
                int(photo.get("width") or 0),
                int(photo.get("height") or 0),
            ):
                raise RuntimeError(f"照片尺寸对账失败：{filename}")
            normalized_url, kind = normalized_photo_reference(
                trial.clean_text(photo.get("photo_url")), source
            )
            if normalized_url != photo.get("photo_url") or kind != photo.get("path_kind"):
                raise RuntimeError(f"照片 URL 越界：{filename}")
            if trial.comparable_host(photo.get("photo_final_url", "")) != trial.OFFICIAL_HOST:
                raise RuntimeError(f"照片最终响应越出官网：{filename}")
            if trial.clean_text(row.get("照片链接")) != normalized_url:
                raise RuntimeError(f"总底表照片链接不一致：{filename}")
            if trial.clean_text(row.get("照片文件")) != photo.get("photo_file"):
                raise RuntimeError(f"总底表照片文件不一致：{filename}")
            expected_files.add(filename)
            total_bytes += len(content)
            max_bytes = max(max_bytes, len(content))
            over_5 += int(len(content) > trial.OWNER_REPORT_BYTES)
            over_20 += int(len(content) > trial.MAX_PHOTO_BYTES)
        elif status == "失败":
            if state not in FULL_FAILURE_STATES:
                raise RuntimeError(f"FULL 失败行未归入四类：{source}")
            if trial.clean_text(row.get("照片链接")) or trial.clean_text(row.get("照片文件")):
                raise RuntimeError(f"FULL 失败行未留空照片字段：{source}")
            if FULL_WARNING_BY_STATE[state] not in trial.clean_text(row.get("异常提示")):
                raise RuntimeError(f"FULL 失败行未追加异常提示：{source}")
            failure = failures_by_source.get(source)
            if failure is None:
                raise RuntimeError(f"FULL 失败行缺少证据：{source}")
            evidence = failure.get("evidence") or {}
            if not evidence.get("resource_urls"):
                raise RuntimeError(f"FULL 失败证据缺少资源 URL：{source}")
            if "photo_reference_count" not in evidence:
                raise RuntimeError(f"FULL 失败证据缺少引用数：{source}")
            if not trial.clean_text(evidence.get("detection_feature")):
                raise RuntimeError(f"FULL 失败证据缺少判定特征：{source}")
            if state == "详情不可达" or (
                state == "照片资源不可达"
                and failure.get("origin") != FLICKER_PROBE_ORIGIN
            ):
                validate_retry_attempts(failure.get("attempts") or [])
        else:
            raise RuntimeError(f"FULL 对账状态非法：{source} {status}")

    actual_files = {item.name for item in photo_root.iterdir() if item.is_file()}
    if actual_files != expected_files:
        raise RuntimeError("FULL 照片目录与照片对账集合不一致")
    if total_bytes != int(meta.get("photo_total_bytes") or 0):
        raise RuntimeError("FULL 照片总字节对账失败")
    if max_bytes != int(meta.get("photo_max_bytes") or 0):
        raise RuntimeError("FULL 最大单张字节对账失败")
    if over_5 != int(meta.get("over_5mib_count") or 0):
        raise RuntimeError("FULL >5 MiB 数量对账失败")
    if over_20 != int(meta.get("over_20mib_count") or 0) or over_20:
        raise RuntimeError("FULL 存在超过 20 MiB 照片")
    if not audit_sheet_path.is_file():
        raise RuntimeError("FULL 抽样拼图缺失")
    if hashlib.sha256(audit_sheet_path.read_bytes()).hexdigest() != meta.get(
        "audit_sheet_sha256"
    ):
        raise RuntimeError("FULL 抽样拼图哈希不一致")
    audit_samples = payload.get("audit_samples", [])
    if len(audit_samples) != 10 or {item.get("audit_kind") for item in audit_samples} != {
        "最小",
        "最大",
        "确定性随机",
    }:
        raise RuntimeError("FULL 抽样拼图未覆盖最小/最大/随机")


def validate_full_installation(payload: dict[str, Any]) -> None:
    final_rows = validate_master_layers(MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH)
    validate_full_payload(payload, FORMAL_PHOTO_DIR, FULL_AUDIT_SHEET_PATH)
    payload_rows = payload.get("rows", [])
    target_sources = {trial.clean_text(row.get("来源链接")) for row in payload_rows}
    final_target_rows = [
        row for row in final_rows if trial.clean_text(row.get("医院")) == HOSPITAL
    ]
    if {
        trial.clean_text(row.get("来源链接")): canonical_master_row(row)
        for row in final_target_rows
    } != {
        trial.clean_text(row.get("来源链接")): canonical_master_row(row)
        for row in payload_rows
    }:
        raise RuntimeError("FULL payload 目标行与已落盘总底表不一致")
    profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
    integrity = {
        trial.clean_text(item.get("source_link")): item
        for item in payload.get("profile_integrity", [])
    }
    if len(integrity) != EXPECTED_PROFILE_COUNT:
        raise RuntimeError("FULL 画像完整性清单数量漂移")
    for source, path in profile_paths.items():
        expected = integrity[source]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected.get("after_sha256"):
            raise RuntimeError(f"FULL 画像落盘哈希不一致：{path}")
        expected_added = 2 if expected.get("status") == "实采" else 0
        if int(expected.get("added_lines") or 0) != expected_added or int(
            expected.get("removed_lines") or 0
        ):
            raise RuntimeError(f"FULL 画像行级差异不符合 +2/-0：{path}")
    index_path = PROFILE_DIR / "_索引.md"
    if hashlib.sha256(index_path.read_bytes()).hexdigest() != payload["meta"].get(
        "profile_index_before_sha256"
    ):
        raise RuntimeError("FULL 修改了 _索引.md")
    current_protected = {str(path): file_digest(path) for path in FULL_PROTECTED_FILES}
    if current_protected != payload["meta"].get("protected_assets_before"):
        raise RuntimeError("FULL 触碰了入口台账三载体或总底表更新报告")
    with FULL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        if len(list(csv.DictReader(handle))) != EXPECTED_SCOPE_COUNT:
            raise RuntimeError("FULL 照片对账 CSV 不是 342 行")


def run_full(run_date: str) -> dict[str, Any]:
    import collect_official_doctors_batch as collector
    import generate_obsidian_profiles as profiles

    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("FULL 前正式照片目录已存在，拒绝覆盖；需 owner 先裁决")
    if FULL_BLOCKER_JSON_PATH.exists():
        raise RuntimeError(
            f"FULL 资源失败批次 blocker 已存在，保持暂停并等待 owner：{FULL_BLOCKER_JSON_PATH}"
        )
    for path in (FULL_JSON_PATH, FULL_CSV_PATH, FULL_REPORT_PATH, FULL_AUDIT_SHEET_PATH):
        if path.exists():
            raise RuntimeError(f"FULL 工件已存在，拒绝覆盖：{path}")
    baseline_protected = {str(path): file_digest(path) for path in FULL_PROTECTED_FILES}
    master_payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    before_rows = copy.deepcopy(master_payload.get("rows", []))
    scope_rows = trial.load_scope_rows()
    target_sources = {trial.clean_text(row.get("来源链接")) for row in scope_rows}
    rows_by_source = {trial.clean_text(row.get("来源链接")): row for row in scope_rows}
    if len(target_sources) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 固定范围来源链接不是 342 个唯一官网详情 URL")
    flicker_probe_payload: dict[str, Any] | None = None
    if FLICKER_PROBE_JSON_PATH.exists() or FLICKER_PROBE_PHOTO_PATH.exists():
        if not FLICKER_PROBE_JSON_PATH.is_file():
            raise RuntimeError("状态闪烁聚合 JSON 缺失")
        flicker_probe_payload = json.loads(
            FLICKER_PROBE_JSON_PATH.read_text(encoding="utf-8")
        )
        validate_status_flicker_probe(
            flicker_probe_payload, FLICKER_PROBE_PHOTO_PATH
        )
        probe_source = trial.clean_text(
            flicker_probe_payload.get("meta", {}).get("source_link")
        )
        if probe_source not in target_sources:
            raise RuntimeError("状态闪烁聚合来源不在 FULL 342 行固定范围")
        captured_round = int(
            flicker_probe_payload.get("meta", {}).get("captured_round") or 0
        )
        if bool(captured_round) != FLICKER_PROBE_PHOTO_PATH.is_file():
            raise RuntimeError("状态闪烁聚合冻结照片与 captured_round 不一致")
    profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
    before_profile_bytes = preflight_profile_bytes(profile_paths, rows_by_source)
    before_profile_tree = profile_markdown_tree(PROFILE_DIR)
    index_path = PROFILE_DIR / "_索引.md"
    index_before_sha256 = hashlib.sha256(index_path.read_bytes()).hexdigest()

    trial_payload = json.loads(trial.TRIAL_JSON_PATH.read_text(encoding="utf-8"))
    trial.validate_payload(trial_payload, require_visual_pass=True)
    if trial.protected_snapshot() != trial_payload["protected_after"]:
        raise RuntimeError("FULL 前正式资产与 TRIAL 后快照不一致")
    seed_samples = trial_payload.get("samples", [])
    seed_sources = {trial.clean_text(item.get("source_link")) for item in seed_samples}
    if len(seed_sources) != EXPECTED_TRIAL_REUSE_COUNT or not seed_sources <= target_sources:
        raise RuntimeError("FULL 复用的 10 张 TRIAL 样本范围漂移")
    trial_failure_records = trial_payload.get("failure_evidence", [])
    if trial_failure_records:
        raise RuntimeError("Issue #73 TRIAL 不应携带失败复用证据")
    trial_failure_sources: set[str] = set()

    session = trial.common.OfficialSession()
    home = session.get(trial.OFFICIAL_HOME)
    directory = session.get(trial.DIRECTORY_URL, referer=trial.OFFICIAL_HOME)
    if home.status != 200 or home.content_type != "text/html":
        raise RuntimeError("FULL 官网首页会话门禁失败")
    if directory.status != 200 or directory.content_type != "text/html":
        raise RuntimeError("FULL 医生目录门禁失败")

    with tempfile.TemporaryDirectory(prefix="issue73_full_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_photo_dir = temp_root / "photos"
        temp_photo_dir.mkdir()
        temp_hospital_dir = temp_root / HOSPITAL
        shutil.copytree(PROFILE_DIR, temp_hospital_dir)
        used_filenames: set[str] = set()
        result_by_source: dict[str, dict[str, Any]] = {}
        photo_samples: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []
        reconciliation_by_source: dict[str, dict[str, Any]] = {}

        def add_success(
            row: dict[str, Any],
            sample: dict[str, Any],
            content: bytes,
            origin: str,
        ) -> None:
            source = trial.clean_text(row.get("来源链接"))
            source_id = trial.detail_id(source)
            extension = trial.clean_text(sample.get("extension")) or Path(
                trial.clean_text(sample.get("filename"))
            ).suffix.lstrip(".").lower().replace("jpeg", "jpg")
            if not extension:
                raise RuntimeError(f"照片扩展名缺失：{source}")
            filename, disk_path = allocate_full_photo_path(
                row, source_id, extension, temp_photo_dir, used_filenames
            )
            expected_name = trial.clean_text(sample.get("filename"))
            if origin == "TRIAL_REUSE" and filename != expected_name:
                raise RuntimeError(f"TRIAL 复用照片命名漂移：{expected_name} -> {filename}")
            disk_path.write_bytes(content)
            width, height = trial.common.image_dimensions(content)
            digest = hashlib.sha256(content).hexdigest()
            photo_url, path_kind = normalized_photo_reference(
                trial.clean_text(sample.get("photo_url")), source
            )
            photo_file = (PHOTO_RELATIVE_ROOT / filename).as_posix()
            result_row = dict(row)
            result_row["照片链接"] = photo_url
            result_row["照片文件"] = photo_file
            result_by_source[source] = result_row
            photo_item = {
                "name": trial.clean_text(row.get("姓名")),
                "department": trial.atomic_department(row),
                "title": trial.primary_title(
                    row.get("职称_关键词") or row.get("职称身份原文")
                ),
                "detail_id": source_id,
                "detail_template": trial.detail_template(source),
                "source_link": source,
                "photo_url": photo_url,
                "path_kind": path_kind,
                "photo_final_url": trial.clean_text(sample.get("photo_final_url")) or photo_url,
                "photo_file": photo_file,
                "filename": filename,
                "extension": extension,
                "bytes": len(content),
                "width": width,
                "height": height,
                "sha256": digest,
                "origin": origin,
                "detail_attempts": sample.get("detail_attempts", []),
                "photo_attempts": sample.get("photo_attempts", []),
            }
            photo_samples.append(photo_item)
            reconciliation_by_source[source] = {
                "姓名": photo_item["name"],
                "来源链接": source,
                "状态": "实采",
                "失败分类": "",
                "照片链接": photo_url,
                "照片文件": photo_file,
                "实际格式": extension,
                "字节数": len(content),
                "SHA-256": digest,
                "宽": width,
                "高": height,
                "来源批次": origin,
                "错误证据": "",
            }

        def record_failure(
            row: dict[str, Any],
            state: str,
            evidence_detail: dict[str, Any],
            attempts: list[dict[str, Any]],
            origin: str = "FULL_FETCH",
        ) -> None:
            source = trial.clean_text(row.get("来源链接"))
            evidence = failure_evidence_text(evidence_detail)
            result_row = dict(row)
            result_row["照片链接"] = ""
            result_row["照片文件"] = ""
            result_row["异常提示"] = append_failure_warning(
                result_row.get("异常提示"), state
            )
            result_by_source[source] = result_row
            failures.append(
                {
                    "name": trial.clean_text(row.get("姓名")),
                    "source_link": source,
                    "state": state,
                    "error": evidence,
                    "evidence": evidence_detail,
                    "attempts": attempts,
                    "origin": origin,
                }
            )
            reconciliation_by_source[source] = {
                "姓名": trial.clean_text(row.get("姓名")),
                "来源链接": source,
                "状态": "失败",
                "失败分类": state,
                "照片链接": "",
                "照片文件": "",
                "实际格式": "",
                "字节数": "",
                "SHA-256": "",
                "宽": "",
                "高": "",
                "来源批次": origin,
                "错误证据": evidence,
            }
            resource_failure_count = sum(
                item.get("state") == "照片资源不可达" for item in failures
            )
            if resource_failure_count >= RESOURCE_FAILURE_PAUSE_COUNT:
                persist_resource_failure_blocker(failures)
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] "
                    f"照片资源不可达累计 {resource_failure_count} 条，已按 Owner 门禁暂停并留证"
                )
            if len(failures) / EXPECTED_SCOPE_COUNT > MAX_FAILURE_RATIO:
                raise RuntimeError("[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 总问题率超过 30%")

        seed_by_source = {
            trial.clean_text(item.get("source_link")): item for item in seed_samples
        }
        for source in sorted(seed_sources):
            item = seed_by_source[source]
            content = (ROOT / trial.clean_text(item.get("disk_path"))).read_bytes()
            add_success(rows_by_source[source], item, content, "TRIAL_REUSE")

        fresh_rows = [
            row
            for row in scope_rows
            if trial.clean_text(row.get("来源链接"))
            not in seed_sources | trial_failure_sources
        ]
        if len(fresh_rows) != EXPECTED_FRESH_COUNT:
            raise RuntimeError("FULL 待新抓取范围不是 332 行")

        for index, row in enumerate(fresh_rows, start=1):
            source = trial.clean_text(row.get("来源链接"))
            name = trial.clean_text(row.get("姓名"))
            if (
                flicker_probe_payload is not None
                and source
                == trial.clean_text(
                    flicker_probe_payload.get("meta", {}).get("source_link")
                )
            ):
                probe_meta = flicker_probe_payload["meta"]
                if int(probe_meta.get("captured_round") or 0):
                    add_success(
                        row,
                        {
                            "photo_url": probe_meta["photo_url"],
                            "photo_final_url": probe_meta["photo_final_url"],
                            "extension": probe_meta["extension"],
                            "detail_attempts": flicker_probe_payload["rounds"],
                            "photo_attempts": flicker_probe_payload["rounds"],
                        },
                        FLICKER_PROBE_PHOTO_PATH.read_bytes(),
                        FLICKER_PROBE_ORIGIN,
                    )
                else:
                    rounds = list(flicker_probe_payload["rounds"])
                    record_failure(
                        row,
                        "照片资源不可达",
                        {
                            "observed_utc": trial.clean_text(
                                rounds[-1].get("start_utc")
                            ),
                            "detail_http": 200,
                            "photo_reference_count": 1,
                            "resource_urls": [probe_meta["photo_url"]],
                            "excluded_resources": [],
                            "detection_feature": (
                                "官网悬空引用：详情页 HTTP 200、页面引用唯一 "
                                "本人照片 URL；执行时点 3 次尝试后，5 轮聚合均未取得照片"
                            ),
                            "template_signature": trial.detail_template(source),
                            "aggregate_rounds": rounds,
                        },
                        rounds,
                        FLICKER_PROBE_ORIGIN,
                    )
                continue
            detail, detail_attempts = fetch_with_retry(
                session,
                source,
                trial.DIRECTORY_URL,
                lambda result: result.status == 200
                and result.content_type.startswith("text/html"),
            )
            if attempts_flicker(detail_attempts):
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] 详情状态闪烁，需回报后执行 5 轮聚合："
                    f"{source} {attempt_evidence(detail_attempts)}"
                )
            if (
                detail is None
                or detail.status != 200
                or not detail.content_type.startswith("text/html")
            ):
                evidence_detail = {
                    "observed_utc": trial.clean_text(detail_attempts[-1].get("utc"))
                    if detail_attempts
                    else "",
                    "detail_http": detail_attempts[-1].get("status")
                    if detail_attempts
                    else None,
                    "photo_reference_count": 0,
                    "resource_urls": [source],
                    "excluded_resources": [],
                    "detection_feature": "详情页不可达，无法解析医生照片容器；"
                    + attempt_evidence(detail_attempts),
                    "template_signature": "unparsed",
                }
                record_failure(
                    row,
                    "详情不可达",
                    evidence_detail,
                    detail_attempts,
                )
                continue
            html = detail.content.decode(detail.charset or "utf-8", errors="replace")
            reference = analyze_doctor_media(html, source, name)
            state = reference.state
            if state:
                record_failure(
                    row,
                    state,
                    media_failure_evidence(reference, detail_attempts),
                    detail_attempts,
                )
                continue
            photo, photo_attempts = fetch_with_retry(
                session,
                reference.photo_url,
                source,
                lambda result: result.status == 200
                and result.content_type.startswith("image/"),
            )
            if attempts_flicker(photo_attempts):
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] 照片状态闪烁，需回报后执行 5 轮聚合："
                    f"{reference.photo_url} {attempt_evidence(photo_attempts)}"
                )
            if photo is None or photo.status != 200 or not photo.content_type.startswith("image/"):
                evidence_detail = {
                    "observed_utc": trial.clean_text(photo_attempts[-1].get("utc"))
                    if photo_attempts
                    else "",
                    "detail_http": 200,
                    "photo_reference_count": reference.reference_count,
                    "resource_urls": [reference.photo_url],
                    "excluded_resources": [],
                    "detection_feature": "页面授权本人照片容器引用唯一；照片资源不可达；"
                    + attempt_evidence(photo_attempts),
                    "template_signature": reference.template_signature,
                }
                record_failure(
                    row,
                    "照片资源不可达",
                    evidence_detail,
                    photo_attempts,
                )
                continue
            if trial.comparable_host(photo.final_url) != trial.OFFICIAL_HOST:
                raise RuntimeError(f"照片重定向越出官网：{reference.photo_url} -> {photo.final_url}")
            extension = trial.common.magic_extension(photo.content, photo.content_type)
            if not extension:
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 照片格式异常："
                    f"{name} {reference.photo_url} {photo.content_type}"
                )
            if len(photo.content) > trial.MAX_PHOTO_BYTES:
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 单图超过 20 MiB："
                    f"{name} {len(photo.content)} {reference.photo_url}"
                )
            placeholder = downloaded_placeholder_reason(
                reference.photo_url, photo.content, extension
            )
            if placeholder:
                record_failure(
                    row,
                    "占位图",
                    {
                        "observed_utc": trial.clean_text(photo_attempts[-1].get("utc"))
                        if photo_attempts
                        else "",
                        "detail_http": 200,
                        "photo_reference_count": reference.reference_count,
                        "resource_urls": [reference.photo_url],
                        "excluded_resources": [],
                        "detection_feature": placeholder,
                        "template_signature": reference.template_signature,
                    },
                    photo_attempts,
                )
                continue
            add_success(
                row,
                {
                    "photo_url": reference.photo_url,
                    "photo_final_url": photo.final_url,
                    "extension": extension,
                    "detail_attempts": detail_attempts,
                    "photo_attempts": photo_attempts,
                },
                photo.content,
                "FULL_FETCH",
            )
            if index % 25 == 0 or index == EXPECTED_FRESH_COUNT:
                print(
                    f"[FULL] {index}/{EXPECTED_FRESH_COUNT} fresh "
                    f"实采={len(photo_samples)} 失败={len(failures)}",
                    flush=True,
                )

        if set(result_by_source) != target_sources:
            raise RuntimeError("FULL 342 行结果来源集合未闭合")
        result_rows = [
            result_by_source[trial.clean_text(row.get("来源链接"))]
            for row in scope_rows
        ]
        reconciliation = [
            reconciliation_by_source[trial.clean_text(row.get("来源链接"))]
            for row in scope_rows
        ]
        updated_by_source = {
            trial.clean_text(row.get("来源链接")): row for row in result_rows
        }
        after_rows = [
            copy.deepcopy(updated_by_source.get(trial.clean_text(row.get("来源链接")), row))
            for row in before_rows
        ]
        row_diffs = collect_full_row_diffs(before_rows, after_rows, target_sources)
        updated_master = copy.deepcopy(master_payload)
        updated_master["rows"] = after_rows
        if failures:
            recompute_failure_derivatives(updated_master, after_rows)

        temp_master_payload = temp_root / MASTER_JSON_PATH.name
        temp_master_csv = temp_root / MASTER_CSV_PATH.name
        temp_master_xlsx = temp_root / MASTER_XLSX_PATH.name
        temp_master_preview = temp_root / "master_preview.png"
        temp_master_payload.write_text(
            json.dumps(updated_master, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_master_csv(temp_master_csv, after_rows)
        collector.build_workbook(temp_master_payload, temp_master_xlsx, temp_master_preview)
        validate_master_layers(temp_master_payload, temp_master_csv, temp_master_xlsx)

        temp_profile_paths = target_profile_paths(temp_hospital_dir, target_sources)
        photo_by_source = {
            trial.clean_text(item.get("source_link")): item for item in photo_samples
        }
        success_sources = set(photo_by_source)
        for source in success_sources:
            item = photo_by_source[source]
            path = temp_profile_paths[source]
            path.write_bytes(
                insert_profile_photo_block_bytes(
                    before_profile_bytes[source], item["name"], item["photo_file"]
                )
            )
            validate_profile_photo_only_bytes(
                before_profile_bytes[source],
                path.read_bytes(),
                item["name"],
                item["photo_file"],
            )
        expected_changed_paths = {
            profile_paths[source].relative_to(PROFILE_DIR) for source in success_sources
        }
        validate_profile_tree_surgical(
            before_profile_tree, temp_hospital_dir, expected_changed_paths
        )
        if hashlib.sha256((temp_hospital_dir / "_索引.md").read_bytes()).hexdigest() != index_before_sha256:
            raise RuntimeError("FULL 临时事务修改了 _索引.md")

        profile_integrity: list[dict[str, Any]] = []
        for source in sorted(target_sources):
            before_content = before_profile_bytes[source]
            after_content = temp_profile_paths[source].read_bytes()
            status = "实采" if source in success_sources else "失败留空"
            profile_integrity.append(
                {
                    "source_link": source,
                    "path": str(profile_paths[source].relative_to(ROOT)),
                    "status": status,
                    "before_sha256": hashlib.sha256(before_content).hexdigest(),
                    "after_sha256": hashlib.sha256(after_content).hexdigest(),
                    "added_lines": 2 if source in success_sources else 0,
                    "removed_lines": 0,
                }
            )

        temp_audit_sheet = temp_root / FULL_AUDIT_SHEET_PATH.name
        audit_samples = build_full_audit_sheet(photo_samples, temp_photo_dir, temp_audit_sheet)
        total_bytes = sum(int(item["bytes"]) for item in photo_samples)
        max_bytes = max((int(item["bytes"]) for item in photo_samples), default=0)
        state_counter = Counter(item["state"] for item in failures)
        full_payload = {
            "meta": {
                "issue": ISSUE_NUMBER,
                "phase": "FULL_READY_FOR_FINAL_OWNER_AUDIT",
                "hospital": HOSPITAL,
                "run_date": run_date,
                "authorization": FULL_AUTHORIZATION,
                "expected_count": EXPECTED_SCOPE_COUNT,
                "downloaded_count": len(photo_samples),
                "failed_count": len(failures),
                "blank_count": len(failures),
                "disk_photo_count": len(photo_samples),
                "failure_ratio": len(failures) / EXPECTED_SCOPE_COUNT,
                "failure_state_counts": {
                    state: state_counter.get(state, 0) for state in FULL_FAILURE_STATES
                },
                "detail_unreachable_count": state_counter.get("详情不可达", 0),
                "photo_resource_unreachable_count": state_counter.get(
                    "照片资源不可达", 0
                ),
                "no_photo_container_count": state_counter.get("无照片容器", 0),
                "placeholder_count": state_counter.get("占位图", 0),
                "trial_reused_count": sum(
                    item["origin"] == "TRIAL_REUSE" for item in photo_samples
                ),
                "trial_failure_reused_count": sum(
                    item["origin"] == "TRIAL_FAILURE_REUSE" for item in failures
                ),
                "fresh_target_count": EXPECTED_FRESH_COUNT,
                "fresh_downloaded_count": sum(
                    item["origin"] != "TRIAL_REUSE" for item in photo_samples
                ),
                "fresh_failed_count": sum(
                    is_fresh_failure_origin(item["origin"]) for item in failures
                ),
                "flicker_probe_reused_count": sum(
                    item["origin"] == FLICKER_PROBE_ORIGIN for item in photo_samples
                )
                + sum(
                    item["origin"] == FLICKER_PROBE_ORIGIN for item in failures
                ),
                "photo_total_bytes": total_bytes,
                "photo_total_mib": total_bytes / 1024 / 1024,
                "photo_max_bytes": max_bytes,
                "size_bucket_counts": trial.size_buckets(photo_samples),
                "over_5mib_count": sum(
                    int(item["bytes"]) > trial.OWNER_REPORT_BYTES for item in photo_samples
                ),
                "over_20mib_count": sum(
                    int(item["bytes"]) > trial.MAX_PHOTO_BYTES for item in photo_samples
                ),
                "detail_template_counts": dict(
                    Counter(item["detail_template"] for item in photo_samples)
                ),
                "format_counts": dict(
                    Counter(item["extension"] for item in photo_samples)
                ),
                "path_kind_counts": dict(
                    Counter(item["path_kind"] for item in photo_samples)
                ),
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "status_flicker_count": int(flicker_probe_payload is not None),
                "status_flicker_resolved_count": int(
                    flicker_probe_payload is not None
                ),
                "cookie_names": session.cookie_names,
                "incomplete_read_retry_count": session.incomplete_read_retry_count,
                "existing_profile_count": len(profile_paths),
                "profile_refreshed_count": len(success_sources),
                "profile_index_before_sha256": index_before_sha256,
                "row_diff_count": len(row_diffs),
                "row_diff_columns": dict(Counter(item["列名"] for item in row_diffs)),
                "audit_sheet_sha256": hashlib.sha256(temp_audit_sheet.read_bytes()).hexdigest(),
                "protected_assets_before": baseline_protected,
                "json_path": str(FULL_JSON_PATH),
                "csv_path": str(FULL_CSV_PATH),
                "report_path": str(FULL_REPORT_PATH),
                "audit_sheet_path": str(FULL_AUDIT_SHEET_PATH),
            },
            "failures": failures,
            "photo_samples": photo_samples,
            "reconciliation": reconciliation,
            "row_diffs": row_diffs,
            "rows": result_rows,
            "profile_integrity": profile_integrity,
            "audit_samples": audit_samples,
            "status_flicker_probe": flicker_probe_payload,
        }
        validate_full_payload(full_payload, temp_photo_dir, temp_audit_sheet)

        temp_full_payload = temp_root / FULL_JSON_PATH.name
        temp_full_csv = temp_root / FULL_CSV_PATH.name
        temp_full_report = temp_root / FULL_REPORT_PATH.name
        temp_full_payload.write_text(
            json.dumps(full_payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_full_reconciliation_csv(temp_full_csv, full_payload)
        write_full_report(temp_full_report, full_payload)

        file_map: dict[Path, Path] = {
            MASTER_JSON_PATH: temp_master_payload,
            MASTER_CSV_PATH: temp_master_csv,
            MASTER_XLSX_PATH: temp_master_xlsx,
            FULL_JSON_PATH: temp_full_payload,
            FULL_CSV_PATH: temp_full_csv,
            FULL_REPORT_PATH: temp_full_report,
            FULL_AUDIT_SHEET_PATH: temp_audit_sheet,
        }
        for source in success_sources:
            file_map[profile_paths[source]] = temp_profile_paths[source]
        backups = backup_file_targets(list(file_map), temp_root / "file_backups")
        photo_swapped = False
        try:
            ensure_workspace_target(FORMAL_PHOTO_DIR)
            temp_photo_dir.replace(FORMAL_PHOTO_DIR)
            photo_swapped = True
            apply_file_map(file_map)
            final_rows = validate_master_layers(
                MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH
            )
            if collect_full_row_diffs(before_rows, final_rows, target_sources) != row_diffs:
                raise RuntimeError("FULL 落盘后的逐单元格差异与预期不一致")
            validate_full_installation(full_payload)
        except Exception:
            restore_file_targets(backups)
            if photo_swapped and FORMAL_PHOTO_DIR.exists():
                ensure_workspace_target(FORMAL_PHOTO_DIR)
                shutil.rmtree(FORMAL_PHOTO_DIR)
            raise
        return full_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #73 广东省第二中医院照片补录 FULL")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--full", action="store_true", help="执行 342 行 FULL 事务")
    mode.add_argument("--validate-full", action="store_true", help="验证已安装 FULL 工件")
    mode.add_argument(
        "--aggregate-flicker", action="store_true", help="执行状态闪烁资源 5 轮聚合"
    )
    parser.add_argument("--run-date", default=str(date.today()), help="执行日期 YYYY-MM-DD")
    parser.add_argument("--source-link", default="", help="聚合探测医生详情 URL")
    parser.add_argument("--photo-url", default="", help="聚合探测页面实际引用照片 URL")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.full:
        payload = run_full(args.run_date)
        meta = payload["meta"]
        print(
            json.dumps(
                {
                    "status": meta["phase"],
                    "expected": meta["expected_count"],
                    "downloaded": meta["downloaded_count"],
                    "failed": meta["failed_count"],
                    "disk_photos": meta["disk_photo_count"],
                    "profiles_refreshed": meta["profile_refreshed_count"],
                    "over_5mib": meta["over_5mib_count"],
                    "payload": str(FULL_JSON_PATH),
                    "reconciliation": str(FULL_CSV_PATH),
                    "report": str(FULL_REPORT_PATH),
                    "audit_sheet": str(FULL_AUDIT_SHEET_PATH),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.validate_full:
        if not FULL_JSON_PATH.is_file():
            raise RuntimeError("FULL payload 不存在")
        payload = json.loads(FULL_JSON_PATH.read_text(encoding="utf-8"))
        validate_full_installation(payload)
        print(
            json.dumps(
                {
                    "status": "FULL_VALIDATED",
                    "downloaded": payload["meta"]["downloaded_count"],
                    "failed": payload["meta"]["failed_count"],
                },
                ensure_ascii=False,
            )
        )
    else:
        if not args.source_link or not args.photo_url:
            raise RuntimeError("--aggregate-flicker 必须同时提供 --source-link 和 --photo-url")
        payload = run_status_flicker_probe(args.source_link, args.photo_url)
        print(
            json.dumps(
                {
                    "status": payload["meta"]["phase"],
                    "source_link": payload["meta"]["source_link"],
                    "round_count": payload["meta"]["round_count"],
                    "captured_round": payload["meta"]["captured_round"],
                    "bytes": payload["meta"]["bytes"],
                    "sha256": payload["meta"]["sha256"],
                    "evidence": str(FLICKER_PROBE_JSON_PATH),
                    "photo": str(FLICKER_PROBE_PHOTO_PATH),
                },
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
