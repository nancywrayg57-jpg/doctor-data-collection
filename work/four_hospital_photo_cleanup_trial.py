from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageOps

import collect_official_doctors_batch as collector


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
MASTER_CSV = SOURCE_DIR / "珠三角三甲医院_医生画像自动采集总底表.csv"
MASTER_XLSX = SOURCE_DIR / "珠三角三甲医院_医生画像自动采集总底表.xlsx"
MASTER_REPORT = SOURCE_DIR / "珠三角三甲医院_医生画像自动采集总底表_更新报告.md"
MASTER_PAYLOAD = WORK_DIR / "珠三角三甲医院_医生画像自动采集总底表_payload.json"
LEDGER = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"

ISSUE_NUMBER = 85
PHASE = "TRIAL"
EXPECTED_SCOPE_COUNT = 249
EXPECTED_TRIAL_COUNT = 12
REQUEST_INTERVAL_SECONDS = 1.0
TRIAL_BASENAME = "四院零散照片清尾_photo_backfill_trial"
PAYLOAD_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
MANIFEST_PATH = WORK_DIR / f"{TRIAL_BASENAME}_manifest.csv"
REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
TRIAL_PHOTO_DIR = WORK_DIR / f"{TRIAL_BASENAME}_photos"

GDMCH = "广东省妇幼保健院"
GD2H = "广东省第二人民医院"
GZTCM = "广州中医药大学第一附属医院"
GY120 = "广东药科大学附属第一医院"
HOSPITALS = (GDMCH, GD2H, GZTCM, GY120)
EXPECTED_SCOPE_BY_HOSPITAL = {GDMCH: 174, GD2H: 48, GZTCM: 25, GY120: 2}
EXPECTED_SAMPLE_BY_HOSPITAL = {GDMCH: 5, GD2H: 5, GZTCM: 1, GY120: 1}
OFFICIAL_HOSTS = {
    GDMCH: {"e3861.com", "www.e3861.com", "wx.e3861.com"},
    GD2H: {"gd2h.com", "www.gd2h.com"},
    GZTCM: {"gztcm.com.cn", "www.gztcm.com.cn"},
    GY120: {"gy120.net", "www.gy120.net"},
}
SAMPLE_PLAN = {
    GDMCH: ("贾杰", "袁超", "秦克旺", "陈佳", "胡克"),
    GD2H: ("杨莲娣", "陈鹏程", "廖耀华", "陈抒扬", "刘婷"),
    GZTCM: ("王超",),
    GY120: ("臧晶",),
}
GDMCH_SHARED_QR_URL = (
    "https://www.e3861.com/uploads/20250421/99cfbdba56620ba44a7c2e8b6bec9515.jpg"
)
GDMCH_SHARED_QR_SHA256 = (
    "d374158a2f4a485f1b402591def08daac36d1b10e0d6bcfbd5989d597318eb9c"
)
KNOWN_PLACEHOLDER_SHA256 = frozenset({GDMCH_SHARED_QR_SHA256})
PLACEHOLDER_MARKERS = (
    "default_ys.gif",
    "/images/default/",
    "placeholder",
    "no-photo",
    "nophoto",
    "noimage",
    "blank",
    "占位",
)
FAILURE_STATES = frozenset(
    {"详情不可达", "照片资源不可达", "无照片容器", "占位图"}
)
TEXT_EXTENSIONS = frozenset(
    {".csv", ".json", ".md", ".py", ".txt", ".yaml", ".yml"}
)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
)
MANIFEST_FIELDS = (
    "hospital",
    "name",
    "department",
    "title",
    "source_link",
    "detail_id",
    "detail_http_status",
    "raw_photo_reference",
    "photo_url",
    "result",
    "failure_state",
    "decision_feature",
    "filename",
    "declared_content_type",
    "actual_extension",
    "bytes",
    "sha256",
    "width",
    "height",
    "retry_count",
    "observed_utc",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def comparable_host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def repo_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"工件路径越出仓库：{resolved}") from exc


def repository_digest_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data


def digest_path(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "file_count": 0, "bytes": 0, "sha256": ""}
    files = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
    digest = hashlib.sha256()
    total_bytes = 0
    for item in files:
        data = repository_digest_bytes(item)
        relative = item.name if path.is_file() else item.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
        total_bytes += len(item.read_bytes())
    return {
        "exists": True,
        "file_count": len(files),
        "bytes": total_bytes,
        "sha256": digest.hexdigest(),
    }


def protected_snapshot() -> dict[str, Any]:
    paths = [LEDGER, MASTER_PAYLOAD, MASTER_CSV, MASTER_XLSX, MASTER_REPORT]
    paths.extend(VAULT / "01_试点医院" / hospital for hospital in HOSPITALS)
    return {repo_relative(path): digest_path(path) for path in paths}


class RateLimitedSession(requests.Session):
    def __init__(self, interval_seconds: float = REQUEST_INTERVAL_SECONDS) -> None:
        super().__init__()
        self.interval_seconds = interval_seconds
        self.trust_env = False
        self.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            }
        )
        self.trace: list[dict[str, Any]] = []
        self._last_start = 0.0

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        now = time.monotonic()
        if self._last_start:
            wait = self.interval_seconds - (now - self._last_start)
            if wait > 0:
                time.sleep(wait)
        started = time.monotonic()
        self._last_start = started
        record: dict[str, Any] = {
            "method": method.upper(),
            "url": url,
            "started_monotonic": round(started, 6),
            "started_utc": utc_now(),
        }
        try:
            response = super().request(method, url, **kwargs)
        except requests.RequestException as exc:
            record["error"] = f"{type(exc).__name__}: {exc}"
            self.trace.append(record)
            raise
        record.update(
            {
                "status": response.status_code,
                "final_url": response.url,
                "content_type": clean_text(response.headers.get("Content-Type")),
                "response_bytes": len(response.content),
            }
        )
        self.trace.append(record)
        return response


def load_scope_rows() -> list[dict[str, str]]:
    with MASTER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    scope = [
        row
        for row in rows
        if row.get("医院") in HOSPITALS
        and not clean_text(row.get("照片链接"))
        and not clean_text(row.get("照片文件"))
    ]
    counts = Counter(row["医院"] for row in scope)
    if len(scope) != EXPECTED_SCOPE_COUNT or dict(counts) != EXPECTED_SCOPE_BY_HOSPITAL:
        raise RuntimeError(
            f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 固定范围漂移：total={len(scope)} counts={dict(counts)}"
        )
    if len({row["来源链接"] for row in scope}) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("[FATAL - HUMAN_INTERVENTION_REQUIRED] 固定范围来源链接不唯一")
    return scope


def select_trial_rows(scope: list[dict[str, str]]) -> list[dict[str, str]]:
    index = {(row["医院"], row["姓名"]): row for row in scope}
    selected: list[dict[str, str]] = []
    for hospital, names in SAMPLE_PLAN.items():
        for name in names:
            key = (hospital, name)
            if key not in index:
                raise RuntimeError(f"TRIAL 样本不在固定范围：{hospital}/{name}")
            selected.append(dict(index[key]))
    counts = Counter(row["医院"] for row in selected)
    if len(selected) != EXPECTED_TRIAL_COUNT or dict(counts) != EXPECTED_SAMPLE_BY_HOSPITAL:
        raise RuntimeError(f"TRIAL 样本构成错误：{dict(counts)}")
    return selected


def detail_id(hospital: str, url: str) -> str:
    if hospital == GDMCH:
        return collector.gdmch_detail_id(url)
    if hospital == GD2H:
        return collector.gd2h_detail_id(url)
    if hospital == GZTCM:
        return collector.gztcm_detail_id(url)
    if hospital == GY120:
        return collector.gy120_detail_id(url)
    return ""


def validate_source_link(hospital: str, url: str) -> str:
    identifier = detail_id(hospital, url)
    if not identifier:
        raise RuntimeError(f"来源链接不符合既有医院详情契约：{hospital} {url}")
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in OFFICIAL_HOSTS[hospital]:
        raise RuntimeError(f"来源链接越出医院官网：{hospital} {url}")
    return identifier


def first_department(row: dict[str, str]) -> str:
    value = clean_text(row.get("科室_列表卡片") or row.get("科室_分类页"))
    value = re.sub(r"（(?:琶洲|民航)院区）$", "", value)
    value = value.split("、", 1)[0]
    return value or "未标注"


def primary_title(row: dict[str, str]) -> str:
    raw = clean_text(row.get("职称_关键词") or row.get("职称身份原文"))
    if not raw:
        return "未标注"
    terms = (
        "主任中医师",
        "副主任中医师",
        "主任医师",
        "副主任医师",
        "主治医师",
        "住院医师",
        "医师",
        "主任技师",
        "副主任技师",
        "主管技师",
        "技师",
        "教授",
        "研究员",
    )
    matches = [term for term in terms if term in raw]
    return max(matches, key=len) if matches else raw.split("、", 1)[0]


def safe_filename_part(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", clean_text(value)).strip(" .-")
    return cleaned or "未标注"


def filename_stem(row: dict[str, str]) -> str:
    return "-".join(
        safe_filename_part(value)
        for value in (row["姓名"], first_department(row), primary_title(row), row["医院"])
    )


def placeholder_reason(url: str, sha256: str = "") -> str:
    normalized = clean_text(url).casefold()
    if sha256 and sha256.casefold() in KNOWN_PLACEHOLDER_SHA256:
        return "known_sha256"
    if normalized.startswith("data:") and any(
        marker in normalized for marker in ("blank", "placeholder", "default")
    ):
        return "base64_marker"
    for marker in PLACEHOLDER_MARKERS:
        if marker.casefold() in normalized:
            return f"url_marker:{marker}"
    return ""


def image_extension(data: bytes, content_type: str = "") -> str:
    return collector.gdgh_photo_extension(data, content_type) or ""


def image_dimensions(data: bytes, extension: str) -> tuple[int, int]:
    return collector.gdmch_photo_dimensions(data, extension)


def limited_unique_color_count(path: Path) -> int:
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        colors = image.getcolors(maxcolors=3)
    return len(colors) if colors is not None else 3


def page_images(soup: BeautifulSoup, source_link: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for image in soup.find_all("img"):
        raw = clean_text(image.get("src"))
        if not raw:
            continue
        rows.append(
            {
                "raw_reference": raw,
                "absolute_url": urljoin(source_link, raw),
                "alt": clean_text(image.get("alt")),
                "outer_html": str(image)[:800],
            }
        )
    return rows


def portrait_node(hospital: str, soup: BeautifulSoup) -> Any:
    selectors = {
        GDMCH: ".expert-detail .detail-head .img-box img",
        GD2H: ".grjj img",
        GZTCM: ".zj-list.details img",
        GY120: ".part1 .img img",
    }
    return soup.select_one(selectors[hospital])


def parse_detail(hospital: str, html: str, row: dict[str, str]) -> dict[str, Any]:
    fallback = {
        "name": row["姓名"],
        "list_title": row.get("职称_关键词", ""),
        "department": first_department(row),
        "source_link": row["来源链接"],
        "list_specialty": row.get("擅长诊疗方向摘录", ""),
        "list_photo_url": "",
        "photo_url": "",
    }
    if hospital == GDMCH:
        parsed = collector.parse_gdmch_detail(html, fallback)
        raw = ""
        node = portrait_node(hospital, BeautifulSoup(html, "html.parser"))
        if node:
            raw = clean_text(node.get("src"))
        parsed["raw_photo_reference"] = raw
        if placeholder_reason(raw):
            parsed["photo_state"] = "placeholder"
            parsed["photo_url"] = ""
        elif parsed.get("photo_url"):
            parsed["photo_state"] = "available"
        else:
            parsed["photo_state"] = "empty"
        return parsed
    if hospital == GD2H:
        return collector.parse_gd2h_detail(html, fallback)
    if hospital == GZTCM:
        return collector.parse_gztcm_detail(html, fallback)
    if hospital == GY120:
        return collector.parse_gy120_detail(html, fallback)
    raise RuntimeError(f"不支持医院：{hospital}")


def fetch_detail(
    session: RateLimitedSession, hospital: str, source_link: str
) -> tuple[int | None, str, str]:
    if hospital == GZTCM:
        return collector.fetch_gztcm_html(session, source_link)
    if hospital == GY120:
        return collector.fetch_gy120_html(session, source_link)
    try:
        response = session.get(source_link, timeout=35)
    except requests.RequestException as exc:
        return None, "", f"{type(exc).__name__}: {exc}"
    if comparable_host(response.url) != comparable_host(source_link):
        return response.status_code, "", f"跨域重定向：{response.url}"
    content_type = clean_text(response.headers.get("Content-Type")).casefold()
    if response.status_code != 200:
        return response.status_code, "", f"HTTP {response.status_code}"
    if "text/html" not in content_type:
        return response.status_code, "", f"非 HTML 响应：{content_type or '未声明'}"
    return response.status_code, response.text, ""


def download_photo(
    session: RateLimitedSession,
    row: dict[str, str],
    parsed: dict[str, Any],
    identifier: str,
    used_filenames: set[str],
) -> dict[str, Any]:
    hospital = row["医院"]
    photo_url = clean_text(parsed.get("photo_url"))
    stem = filename_stem(row)
    if hospital == GDMCH:
        return collector.download_gdmch_photo(
            session, photo_url, TRIAL_PHOTO_DIR, stem, identifier, used_filenames
        )
    if hospital == GD2H:
        return collector.download_gd2h_photo(
            session,
            photo_url,
            row["来源链接"],
            TRIAL_PHOTO_DIR,
            stem,
            identifier,
            used_filenames,
        )
    if hospital == GZTCM:
        return collector.download_gztcm_photo(
            session,
            photo_url,
            row["来源链接"],
            TRIAL_PHOTO_DIR,
            stem,
            identifier,
            used_filenames,
        )
    if hospital == GY120:
        return collector.download_gy120_photo(
            session,
            photo_url,
            row["来源链接"],
            TRIAL_PHOTO_DIR,
            stem,
            identifier,
            used_filenames,
        )
    raise RuntimeError(f"不支持医院：{hospital}")


def last_response_trace(session: RateLimitedSession, url: str) -> dict[str, Any]:
    comparable = clean_text(url)
    for item in reversed(session.trace):
        if item.get("url") == comparable or item.get("final_url") == comparable:
            return item
    return {}


def collect_shared_qr_evidence(
    session: RateLimitedSession, observed_urls: set[str]
) -> dict[str, Any]:
    if GDMCH_SHARED_QR_URL not in observed_urls:
        raise RuntimeError("省妇幼共享二维码 URL 未在 TRIAL 页面中出现")
    response = session.get(GDMCH_SHARED_QR_URL, timeout=35)
    digest = hashlib.sha256(response.content).hexdigest()
    extension = image_extension(response.content, response.headers.get("Content-Type", ""))
    width, height = image_dimensions(response.content, extension) if extension else (0, 0)
    if (
        response.status_code != 200
        or digest != GDMCH_SHARED_QR_SHA256
        or (width, height) != (235, 234)
    ):
        raise RuntimeError(
            f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 共享二维码证据漂移：HTTP={response.status_code} sha={digest} size={width}x{height}"
        )
    return {
        "url": GDMCH_SHARED_QR_URL,
        "http_status": response.status_code,
        "content_type": clean_text(response.headers.get("Content-Type")),
        "bytes": len(response.content),
        "sha256": digest,
        "width": width,
        "height": height,
        "classification": "预约二维码（跨页共享功能图，禁止作为医生照片）",
        "saved_to_disk": False,
        "observed_utc": utc_now(),
    }


def failure_from_state(state: str) -> tuple[str, str]:
    if state == "placeholder":
        return "占位图", "详情照片位命中显式 default/placeholder 门禁"
    if state in {"empty", "rejected"}:
        return "无照片容器", "详情页无符合既有医院白名单的本人职业照引用"
    return "照片资源不可达", "页面实际引用的官方照片资源在既有有界请求规则下不可得"


def collect_sample(
    session: RateLimitedSession,
    row: dict[str, str],
    used_filenames: set[str],
) -> dict[str, Any]:
    hospital = row["医院"]
    source_link = row["来源链接"]
    identifier = validate_source_link(hospital, source_link)
    status, html, error = fetch_detail(session, hospital, source_link)
    result: dict[str, Any] = {
        "hospital": hospital,
        "name": row["姓名"],
        "department": first_department(row),
        "title": primary_title(row),
        "source_link": source_link,
        "detail_id": identifier,
        "detail_http_status": status,
        "detail_error": error,
        "original_warning": row.get("异常提示", ""),
        "observed_utc": utc_now(),
    }
    if status != 200 or not html:
        result.update(
            {
                "result": "failed",
                "failure_state": "详情不可达",
                "decision_feature": error or f"HTTP {status}",
                "raw_photo_reference": "",
                "photo_url": "",
            }
        )
        return result

    soup = BeautifulSoup(html, "html.parser")
    images = page_images(soup, source_link)
    node = portrait_node(hospital, soup)
    parsed = parse_detail(hospital, html, row)
    parsed_name = clean_text(parsed.get("name"))
    if parsed_name != clean_text(row["姓名"]):
        raise RuntimeError(
            f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 姓名不一致：{hospital}/{row['姓名']} != {parsed_name}"
        )
    raw_reference = clean_text(
        parsed.get("raw_photo_reference")
        or parsed.get("raw_photo_url")
        or parsed.get("raw_photo")
        or (node.get("src") if node else "")
    )
    result.update(
        {
            "parsed_name": parsed_name,
            "identity_match": True,
            "raw_photo_reference": raw_reference,
            "photo_url": clean_text(parsed.get("photo_url")),
            "photo_state": parsed.get("photo_state", "empty"),
            "portrait_container_html": str(node)[:1200] if node else "",
            "page_image_references": images,
            "page_image_reference_count": len(images),
            "excluded_resource_urls": [
                item["absolute_url"]
                for item in images
                if item["absolute_url"] != clean_text(parsed.get("photo_url"))
            ],
        }
    )
    state = clean_text(parsed.get("photo_state")) or "empty"
    if state != "available" or not result["photo_url"]:
        failure_state, feature = failure_from_state(state)
        if hospital == GDMCH and GDMCH_SHARED_QR_URL in result["excluded_resource_urls"]:
            feature += "；页面共享 /uploads/ 图为预约二维码，按 known-SHA 排除"
        result.update(
            {
                "result": "failed",
                "failure_state": failure_state,
                "decision_feature": feature,
                "placeholder_reason": placeholder_reason(raw_reference),
            }
        )
        return result

    try:
        photo = download_photo(session, row, parsed, identifier, used_filenames)
    except RuntimeError as exc:
        if hospital == GDMCH and "照片下载 HTTP" in str(exc):
            result.update(
                {
                    "result": "failed",
                    "failure_state": "照片资源不可达",
                    "decision_feature": str(exc),
                }
            )
            return result
        raise
    if photo.get("approved_no_source"):
        result.update(
            {
                "result": "failed",
                "failure_state": "照片资源不可达",
                "decision_feature": clean_text(
                    photo.get("approved_no_source_reason") or "有界请求后不可得"
                ),
                "photo_attempt_results": photo.get("attempt_results", []),
                "retry_count": photo.get("retry_count", 0),
            }
        )
        return result

    disk_path = Path(photo["disk_path"]).resolve()
    trace = last_response_trace(session, photo["photo_url"])
    result.update(photo)
    result.update(
        {
            "result": "downloaded",
            "failure_state": "",
            "decision_feature": "页面本人照片容器实际引用；官方原始字节通过魔数、尺寸、占位与唯一性门禁",
            "disk_path": repo_relative(disk_path),
            "declared_content_type": trace.get("content_type", ""),
            "actual_extension": disk_path.suffix.lower().lstrip("."),
            "unique_color_count_gate": limited_unique_color_count(disk_path),
        }
    )
    return result


def request_summary(trace: list[dict[str, Any]]) -> dict[str, Any]:
    starts = [float(item["started_monotonic"]) for item in trace]
    gaps = [round(starts[index] - starts[index - 1], 6) for index in range(1, len(starts))]
    return {
        "request_count": len(trace),
        "minimum_adjacent_start_interval_seconds": min(gaps) if gaps else None,
        "maximum_adjacent_start_interval_seconds": max(gaps) if gaps else None,
        "all_requests_serial": True,
        "configured_interval_seconds": REQUEST_INTERVAL_SECONDS,
        "manually_injected_cookie": False,
        "proxy_enabled": False,
    }


def contact_sheet_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def build_contact_sheet(samples: list[dict[str, Any]]) -> None:
    if not samples:
        raise RuntimeError("TRIAL 样本为空，无法生成联系表")
    columns = 2
    cell_width = 560
    cell_height = 540
    image_box = (500, 390)
    rows = (len(samples) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_width, rows * cell_height), "#D9DEE3")
    draw = ImageDraw.Draw(canvas)
    title_font = contact_sheet_font(19)
    detail_font = contact_sheet_font(15)
    for index, sample in enumerate(samples):
        left = (index % columns) * cell_width
        top = (index // columns) * cell_height
        draw.rectangle(
            (left + 4, top + 4, left + cell_width - 5, top + cell_height - 5),
            fill="#C8CDD2",
            outline="#2F3942",
            width=3,
        )
        if sample.get("result") == "downloaded":
            with Image.open(ROOT / sample["disk_path"]) as source:
                image = ImageOps.exif_transpose(source).convert("RGB")
                thumb = ImageOps.contain(image, image_box)
            if thumb.width < 2 or thumb.height < 2:
                raise RuntimeError(
                    f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 拼图不可见格：{sample['name']}"
                )
            image_left = left + (cell_width - thumb.width) // 2
            image_top = top + 10 + (image_box[1] - thumb.height) // 2
            canvas.paste(thumb, (image_left, image_top))
            draw.rectangle(
                (
                    image_left - 2,
                    image_top - 2,
                    image_left + thumb.width + 1,
                    image_top + thumb.height + 1,
                ),
                outline="#111820",
                width=2,
            )
        else:
            box_left = left + 30
            box_top = top + 28
            box_right = left + cell_width - 30
            box_bottom = top + 28 + image_box[1] - 36
            draw.rectangle(
                (box_left, box_top, box_right, box_bottom),
                fill="#E7EAED",
                outline="#7A2525",
                width=4,
            )
            draw.line((box_left + 18, box_top + 18, box_right - 18, box_bottom - 18), fill="#9C5656", width=5)
            draw.line((box_right - 18, box_top + 18, box_left + 18, box_bottom - 18), fill="#9C5656", width=5)
            draw.text(
                (box_left + 92, box_top + 132),
                "无可采本人职业照",
                fill="#4C1717",
                font=title_font,
            )
            draw.text(
                (box_left + 155, box_top + 184),
                clean_text(sample.get("failure_state")),
                fill="#4C1717",
                font=title_font,
            )
        draw.text(
            (left + 16, top + 414),
            f"{index + 1}. {sample['name']}｜{sample['title']}",
            fill="#111111",
            font=title_font,
        )
        draw.text(
            (left + 16, top + 452),
            f"{sample['hospital']}｜{sample['department']}",
            fill="#222222",
            font=detail_font,
        )
        draw.text(
            (left + 16, top + 486),
            (
                f"{sample['width']}×{sample['height']}｜{sample['bytes']} bytes"
                if sample.get("result") == "downloaded"
                else clean_text(sample.get("raw_photo_reference") or "页面无照片引用")[:62]
            ),
            fill="#333333",
            font=detail_font,
        )
    canvas.save(CONTACT_SHEET_PATH, format="JPEG", quality=92, optimize=True)


def visual_pass_status(downloaded_count: int) -> str:
    if downloaded_count:
        return "PASSED_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS"
    return "PASSED_ZERO_DOWNLOADS_FAILURE_EVIDENCE_CONTACT_SHEET_REVIEW"


def validate_payload(payload: dict[str, Any], require_visual: bool) -> None:
    errors: list[str] = []
    meta = payload.get("meta", {})
    samples = payload.get("samples", [])
    if meta.get("issue_number") != ISSUE_NUMBER or meta.get("phase") != PHASE:
        errors.append("Issue/Phase 不一致")
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("固定范围不是 249")
    if meta.get("sample_count") != EXPECTED_TRIAL_COUNT or len(samples) != EXPECTED_TRIAL_COUNT:
        errors.append("TRIAL 不是 12 行")
    sample_counts = Counter(item.get("hospital") for item in samples)
    if dict(sample_counts) != EXPECTED_SAMPLE_BY_HOSPITAL:
        errors.append(f"四院样本构成错误：{dict(sample_counts)}")
    if payload.get("protected_before") != payload.get("protected_after"):
        errors.append("正式受保护资产发生变化")
    if meta.get("formal_assets_modified") is not False:
        errors.append("formal_assets_modified 不是 false")
    if any(item.get("identity_match") is not True for item in samples if item.get("result") != "failed" or item.get("detail_http_status") == 200):
        errors.append("存在姓名身份未严格对齐样本")
    if any(item.get("failure_state") not in FAILURE_STATES for item in samples if item.get("result") == "failed"):
        errors.append("失败行未归入四类")
    successes = [item for item in samples if item.get("result") == "downloaded"]
    failures = [item for item in samples if item.get("result") == "failed"]
    if len(successes) + len(failures) != EXPECTED_TRIAL_COUNT:
        errors.append("成功/失败四数不闭合")
    sha_values: list[str] = []
    for item in successes:
        path = ROOT / item.get("disk_path", "")
        if not path.is_file():
            errors.append(f"照片文件不存在：{item.get('name')}")
            continue
        data = path.read_bytes()
        actual_sha = hashlib.sha256(data).hexdigest()
        extension = image_extension(data, item.get("declared_content_type", ""))
        width, height = image_dimensions(data, extension) if extension else (0, 0)
        if actual_sha != item.get("sha256") or len(data) != item.get("bytes"):
            errors.append(f"照片字节/SHA 不一致：{item.get('name')}")
        if extension != item.get("actual_extension") or (width, height) != (
            item.get("width"),
            item.get("height"),
        ):
            errors.append(f"照片魔数/尺寸不一致：{item.get('name')}")
        if placeholder_reason(item.get("photo_url", ""), actual_sha):
            errors.append(f"成功照片命中占位门禁：{item.get('name')}")
        if limited_unique_color_count(path) <= 2:
            errors.append(f"成功照片唯一颜色数不大于 2：{item.get('name')}")
        sha_values.append(actual_sha)
    if len(sha_values) != len(set(sha_values)):
        errors.append("成功照片存在跨医生同 SHA")
    qr = payload.get("placeholder_evidence", {}).get("gdmch_shared_qr", {})
    if qr.get("sha256") != GDMCH_SHARED_QR_SHA256 or qr.get("saved_to_disk") is not False:
        errors.append("省妇幼共享二维码 known-SHA 证据不完整")
    gdmch_samples = [item for item in samples if item.get("hospital") == GDMCH]
    if sum(item.get("failure_state") in {"占位图", "无照片容器"} for item in gdmch_samples) < 2:
        errors.append("省妇幼未覆盖至少 2 个无本人照片代表")
    if not any(GDMCH_SHARED_QR_URL in item.get("excluded_resource_urls", []) for item in gdmch_samples):
        errors.append("省妇幼未覆盖疑似共享 uploads 资源排除判例")
    if not any(item.get("name") == "陈鹏程" for item in samples):
        errors.append("缺少陈鹏程可补采实证行")
    if not any(item.get("name") == "杨莲娣" and item.get("failure_state") == "占位图" for item in samples):
        errors.append("缺少杨莲娣 default_ys.gif 占位判例")
    if not any(item.get("name") == "廖耀华" for item in samples):
        errors.append("缺少省二医已裁决 404 复测行")
    request_meta = payload.get("request_summary", {})
    minimum_gap = request_meta.get("minimum_adjacent_start_interval_seconds")
    if minimum_gap is not None and minimum_gap < REQUEST_INTERVAL_SECONDS - 0.01:
        errors.append(f"请求间隔小于 1 秒：{minimum_gap}")
    if request_meta.get("all_requests_serial") is not True:
        errors.append("请求不是串行")
    if require_visual and meta.get("visual_status") != visual_pass_status(len(successes)):
        errors.append("联系表尚未完成人工视觉通过标记")
    if errors:
        raise RuntimeError("[FATAL - HUMAN_INTERVENTION_REQUIRED] TRIAL 验证失败：\n- " + "\n- ".join(errors))


def manifest_rows(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{field: sample.get(field, "") for field in MANIFEST_FIELDS} for sample in samples]


def write_manifest(samples: list[dict[str, Any]]) -> None:
    with MANIFEST_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(manifest_rows(samples))


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|")


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    samples = payload["samples"]
    counts = Counter(
        sample.get("failure_state") or "实采成功" for sample in samples
    )
    lines = [
        "# Issue #85 四院零散照片清尾 TRIAL 报告",
        "",
        f"- Phase：`{meta['phase']}`",
        f"- 固定范围：{meta['scope_count']} 行（174 + 48 + 25 + 2）",
        f"- TRIAL：{meta['sample_count']} 行（5 + 5 + 1 + 1）",
        f"- 四数：12 = {counts.get('实采成功', 0)} 实采 + {len(samples) - counts.get('实采成功', 0)} 失败留痕",
        f"- 失败分类：详情不可达 {counts.get('详情不可达', 0)} / 照片资源不可达 {counts.get('照片资源不可达', 0)} / 无照片容器 {counts.get('无照片容器', 0)} / 占位图 {counts.get('占位图', 0)}",
        f"- 正式资产修改：{meta['formal_assets_modified']}",
        f"- 视觉状态：`{meta['visual_status']}`",
        "",
        "## 样本对账",
        "",
        "| 医院 | 姓名 | 详情 HTTP | 页面照片引用 | 结果 | 判定依据 |",
        "|---|---|---:|---|---|---|",
    ]
    for sample in samples:
        lines.append(
            "| "
            + " | ".join(
                markdown_cell(value)
                for value in (
                    sample.get("hospital"),
                    sample.get("name"),
                    sample.get("detail_http_status"),
                    sample.get("raw_photo_reference"),
                    sample.get("failure_state") or f"实采 {sample.get('filename', '')}",
                    sample.get("decision_feature"),
                )
            )
            + " |"
        )
    qr = payload["placeholder_evidence"]["gdmch_shared_qr"]
    request_meta = payload["request_summary"]
    lines.extend(
        [
            "",
            "## 容器与占位诊断",
            "",
            "- 省妇幼本人照片位严格沿用 `.expert-detail .detail-head .img-box img`；`/Images/Default/doct.png` 为显式占位。",
            "- 省妇幼页面共享 `/uploads/20250421/99cfbdba…jpg` 经原字节复核为预约二维码，跨页共享且不属于本人照片容器。",
            f"- 二维码：HTTP {qr['http_status']}，{qr['bytes']} bytes，{qr['width']}×{qr['height']}，SHA-256 `{qr['sha256']}`；未落盘。",
            "- 省二医本人照片位严格沿用 `img.col-lg-3.col-6` / `.grjj img`；`default_ys.gif` 为显式默认图。",
            "- 广中医一附沿用 `.zj-list.details` 内既有专家资源白名单；广药附一沿用 `.part1 .img img` 与 `/files/`、`/upsfile/` 既有判例。",
            "- 所有页面仅使用实际引用；未构造、猜测或探测任何未引用路径。",
            "",
            "## 请求与保护",
            "",
            f"- 真实请求：{request_meta['request_count']}；最小相邻启动间隔：{request_meta['minimum_adjacent_start_interval_seconds']} 秒；串行：{request_meta['all_requests_serial']}。",
            "- 固定浏览器 UA；未手工注入 Cookie；禁用环境代理；无并发。",
            "- 总底表 JSON/CSV/XLSX、更新报告、入口台账及四院正式画像树前后摘要完全一致。",
            "",
            "## 工件",
            "",
            f"- `{repo_relative(PAYLOAD_PATH)}`",
            f"- `{repo_relative(MANIFEST_PATH)}`",
            f"- `{repo_relative(REPORT_PATH)}`",
            f"- `{repo_relative(CONTACT_SHEET_PATH)}`",
            f"- `{repo_relative(TRIAL_PHOTO_DIR)}/`",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def ensure_outputs_absent() -> None:
    existing = [
        str(path)
        for path in (PAYLOAD_PATH, MANIFEST_PATH, REPORT_PATH, CONTACT_SHEET_PATH, TRIAL_PHOTO_DIR)
        if path.exists()
    ]
    if existing:
        raise RuntimeError("TRIAL 输出已存在，拒绝覆盖：\n- " + "\n- ".join(existing))


def run_trial() -> dict[str, Any]:
    ensure_outputs_absent()
    scope = load_scope_rows()
    selected = select_trial_rows(scope)
    before = protected_snapshot()
    session = RateLimitedSession()
    used_filenames: set[str] = set()
    samples = [collect_sample(session, row, used_filenames) for row in selected]
    observed_urls = {
        image["absolute_url"]
        for sample in samples
        for image in sample.get("page_image_references", [])
    }
    qr_evidence = collect_shared_qr_evidence(session, observed_urls)
    successes = [sample for sample in samples if sample.get("result") == "downloaded"]
    build_contact_sheet(samples)
    after = protected_snapshot()
    payload: dict[str, Any] = {
        "meta": {
            "issue_number": ISSUE_NUMBER,
            "phase": PHASE,
            "scope_count": len(scope),
            "scope_by_hospital": dict(Counter(row["医院"] for row in scope)),
            "sample_count": len(samples),
            "sample_by_hospital": dict(Counter(row["hospital"] for row in samples)),
            "downloaded_count": len(successes),
            "failed_count": len(samples) - len(successes),
            "formal_assets_modified": before != after,
            "visual_status": "PENDING_MANUAL_CONTACT_SHEET_REVIEW",
            "generated_utc": utc_now(),
        },
        "request_summary": request_summary(session.trace),
        "request_trace": session.trace,
        "placeholder_evidence": {"gdmch_shared_qr": qr_evidence},
        "protected_before": before,
        "protected_after": after,
        "samples": samples,
        "artifacts": {
            "payload": repo_relative(PAYLOAD_PATH),
            "manifest": repo_relative(MANIFEST_PATH),
            "report": repo_relative(REPORT_PATH),
            "contact_sheet": repo_relative(CONTACT_SHEET_PATH),
            "photo_dir": repo_relative(TRIAL_PHOTO_DIR),
        },
    }
    validate_payload(payload, require_visual=False)
    PAYLOAD_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_manifest(samples)
    write_report(payload)
    return payload


def load_payload() -> dict[str, Any]:
    return json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))


def mark_visual_pass() -> dict[str, Any]:
    payload = load_payload()
    validate_payload(payload, require_visual=False)
    payload["meta"]["visual_status"] = visual_pass_status(
        int(payload["meta"]["downloaded_count"])
    )
    payload["meta"]["visual_reviewed_utc"] = utc_now()
    PAYLOAD_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_report(payload)
    validate_payload(payload, require_visual=True)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #85 四院零散照片清尾 TRIAL")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--validate", action="store_true")
    group.add_argument("--mark-visual-pass", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.validate:
        payload = load_payload()
        validate_payload(payload, require_visual=True)
        print(
            f"validated: scope={payload['meta']['scope_count']} sample={payload['meta']['sample_count']} downloaded={payload['meta']['downloaded_count']} failed={payload['meta']['failed_count']}"
        )
        return 0
    if args.mark_visual_pass:
        payload = mark_visual_pass()
        print(f"visual_pass: downloaded={payload['meta']['downloaded_count']}")
        return 0
    payload = run_trial()
    print(
        f"trial_complete: sample={payload['meta']['sample_count']} downloaded={payload['meta']['downloaded_count']} failed={payload['meta']['failed_count']} visual={payload['meta']['visual_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
