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
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from http.cookiejar import CookieJar
from pathlib import Path
from statistics import median
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import (
    HTTPCookieProcessor,
    HTTPRedirectHandler,
    Request,
    build_opener,
)

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "广州市中医院"
ISSUE_NUMBER = 67
OFFICIAL_HOME = "https://www.gzszyy.com/"
DIRECTORY_URL = "https://www.gzszyy.com/expert/"
OFFICIAL_HOST = "gzszyy.com"
PHOTO_HOST = "oss.gzszyy.com"
EXPECTED_SCOPE_COUNT = 415
EXPECTED_TRIAL_COUNT = 10
EXPECTED_DEPARTMENT_COUNT = 10
MAX_FAILURE_RATIO = 0.30
OWNER_REPORT_BYTES = 5 * 1024 * 1024
FULL_FUSE_BYTES = 20 * 1024 * 1024
SMALL_GIF_PLACEHOLDER_BYTES = 40 * 1024
SUPPORTED_EXTENSIONS = frozenset({"jpg", "png", "gif", "webp"})

MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_JSON_PATH = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_REPORT_PATH = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
LEDGER_JSON_PATH = WORK_DIR / "pearl_delta_hospital_entry_ledger.json"
LEDGER_CSV_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.csv"
LEDGER_XLSX_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"
PROFILE_DIR = VAULT / "01_试点医院" / HOSPITAL
FORMAL_PHOTO_DIR = PROFILE_DIR / "照片"
TRIAL_BASENAME = f"{HOSPITAL}_photo_backfill_trial"
TRIAL_JSON_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
TRIAL_CSV_PATH = WORK_DIR / f"{TRIAL_BASENAME}_manifest.csv"
TRIAL_REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
TRIAL_PHOTO_DIR = WORK_DIR / f"{TRIAL_BASENAME}_photos"
FULL_BASENAME = f"{HOSPITAL}_photo_backfill_full"
FULL_JSON_PATH = WORK_DIR / f"{FULL_BASENAME}_payload.json"
FULL_CSV_PATH = WORK_DIR / f"{FULL_BASENAME}_reconciliation.csv"
FULL_REPORT_PATH = WORK_DIR / f"{FULL_BASENAME}_report.md"
EXPECTED_PROFILE_COUNT = EXPECTED_SCOPE_COUNT
PHOTO_RELATIVE_ROOT = Path("01_试点医院") / HOSPITAL / "照片"

BASE_HEADERS = [
    "序号",
    "医院",
    "姓名",
    "科室_分类页",
    "科室_列表卡片",
    "职称_关键词",
    "职称身份原文",
    "重点优先级",
    "重点关注范围",
    "重点疾病标签",
    "擅长诊疗方向摘录",
    "亮眼经历线索",
    "列表简介",
    "详情正文摘录",
    "来源类型",
    "来源链接",
    "照片链接",
    "照片文件",
    "采集入口",
    "采集方式",
    "采集日期",
    "详情页状态",
    "已建画像",
    "异常提示",
    "复核状态",
]
FULL_FAILURE_STATES = ("详情不可达", "无照片容器", "占位图")
FULL_WARNING_BY_STATE = {
    state: f"官网本人职业照补录失败：{state}" for state in FULL_FAILURE_STATES
}
FULL_ALLOWED_ROW_COLUMNS = {"照片链接", "照片文件", "异常提示"}
FULL_AUTHORIZATION = (
    "PR #68 owner comment 2026-08-17T12:35:05Z: TRIAL 通过并切换 "
    "FULL_APPEND_AND_OBSIDIAN；415 行全量；失败三态、重试留证、三载体和画像最小刷新"
)
DETAIL_RETRY_COUNT = 2
DETAIL_RETRY_INTERVAL_SECONDS = 30
FULL_PROTECTED_FILES = (
    MASTER_REPORT_PATH,
    LEDGER_JSON_PATH,
    LEDGER_CSV_PATH,
    LEDGER_XLSX_PATH,
)

PROTECTED_FILES = (
    MASTER_JSON_PATH,
    MASTER_CSV_PATH,
    MASTER_XLSX_PATH,
    MASTER_REPORT_PATH,
    LEDGER_JSON_PATH,
    LEDGER_CSV_PATH,
    LEDGER_XLSX_PATH,
)
AUTO_MARKER = "<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->"
PHOTO_PATH_RE = re.compile(
    r"^/\d{8}/\d+\.(?:jpe?g|png|gif|webp)$", re.IGNORECASE
)
DETAIL_PATH_RE = re.compile(
    r"^/expert/(20\d{2})/([A-Za-z0-9]+)\.html$", re.IGNORECASE
)
PLACEHOLDER_MARKERS = (
    "nopic",
    "no_pic",
    "no-photo",
    "noimage",
    "no-image",
    "placeholder",
)
SAMPLE_PLAN = (
    ("叶穗林", "名医堂", "正高", "w9aADOev"),
    ("吴薏婷", "肿瘤一区", "正高", "4zbqjrdp"),
    ("林少贞", "针灸科", "正高", "ELe31Mb6"),
    ("陈庆强", "肿瘤二区", "副高", "pmbk5Xez"),
    ("欧阳智", "脑病科（神经内科）", "副高", "YqaQlenj"),
    ("周艳利", "肾病科", "副高", "MYerEdOB"),
    ("夏思", "血液科", "其他", "LDdwEma1"),
    ("赵鸿", "重症医学科", "其他", "YQdJZodO"),
    ("金华伟", "肺病科（呼吸内科）", "其他", "MYer8wbO"),
    ("陈燕珊", "内分泌科", "其他", "y1aK6zeQ"),
)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36; "
    "public official-site photo backfill trial"
)


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def comparable_host(value: str) -> str:
    return (urlparse(value).hostname or "").lower().removeprefix("www.")


def detail_id(value: Any) -> str:
    text = clean_text(value)
    parsed = urlparse(text)
    if (
        parsed.scheme != "https"
        or comparable_host(text) != OFFICIAL_HOST
        or parsed.query
        or parsed.fragment
    ):
        return ""
    match = DETAIL_PATH_RE.fullmatch(parsed.path)
    return match.group(2) if match else ""


def safe_photo_part(value: Any) -> str:
    result = clean_text(value) or "未标注"
    result = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", result).strip(" .")
    return result or "未标注"


def atomic_department(row: dict[str, Any]) -> str:
    value = clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
    return clean_text(re.split(r"[、,，;/；]", value, maxsplit=1)[0]) or "未标注"


def title_level(value: Any) -> str:
    title = clean_text(value)
    if "副主任" in title:
        return "副高"
    if "主任" in title:
        return "正高"
    return "其他"


@dataclass(frozen=True)
class HttpResult:
    status_code: int
    url: str
    trace: tuple[tuple[int, str], ...]
    headers: dict[str, str]
    content: bytes
    charset: str

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300

    @property
    def text(self) -> str:
        return self.content.decode(self.charset or "utf-8", errors="replace")


class RecordingRedirectHandler(HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.trace: list[tuple[int, str]] = []

    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> Request | None:
        self.trace.append((code, req.full_url))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class OfficialSession:
    def __init__(self) -> None:
        self.redirect_handler = RecordingRedirectHandler()
        self.opener = build_opener(
            HTTPCookieProcessor(CookieJar()), self.redirect_handler
        )

    def get(self, url: str, referer: str = "") -> HttpResult:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,image/*;q=0.9,*/*;q=0.8",
        }
        if referer:
            headers["Referer"] = referer
        request = Request(url, headers=headers, method="GET")
        self.redirect_handler.trace = []
        try:
            with self.opener.open(request, timeout=30) as response:
                content = response.read(FULL_FUSE_BYTES + 1)
                status = int(response.status)
                final_url = response.geturl()
                response_headers = {
                    key.lower(): value for key, value in response.headers.items()
                }
                charset = response.headers.get_content_charset() or "utf-8"
        except HTTPError as exc:
            content = exc.read(FULL_FUSE_BYTES + 1)
            status = int(exc.code)
            final_url = exc.geturl()
            response_headers = {
                key.lower(): value for key, value in exc.headers.items()
            }
            charset = exc.headers.get_content_charset() or "utf-8"
        except URLError as exc:
            raise RuntimeError(f"GET 失败：{url}：{exc.reason}") from exc
        trace = (*self.redirect_handler.trace, (status, final_url))
        return HttpResult(
            status_code=status,
            url=final_url,
            trace=trace,
            headers=response_headers,
            content=content,
            charset=charset,
        )


def response_trace(response: HttpResult) -> str:
    return ";".join(f"{status}@{url}" for status, url in response.trace)


def require_html(response: HttpResult, label: str) -> str:
    if not response.ok:
        raise RuntimeError(f"{label} HTTP {response.status_code}")
    content_type = clean_text(response.headers.get("content-type")).lower()
    mime = content_type.partition(";")[0]
    if mime not in {"text/html", "application/xhtml+xml"}:
        raise RuntimeError(
            f"{label} HTTP {response.status_code} 返回非 HTML Content-Type: {content_type or '缺失'}"
        )
    return response.text


class PhotoPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, frozenset[str]]] = []
        self.resume_container_count = 0
        self.photo_container_count = 0
        self.photo_sources: list[str] = []
        self.name_parts: list[str] = []

    def _inside(self, class_name: str) -> bool:
        return any(class_name in classes for _, classes in self.stack)

    def _start(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        classes = frozenset(values.get("class", "").split())
        inside_resume_before = self._inside("doctor-resume")
        inside_photo_before = self._inside("doctor-img")
        lowered = tag.lower()
        if lowered == "div" and "doctor-resume" in classes:
            self.resume_container_count += 1
        if tag.lower() == "div" and "doctor-img" in classes and inside_resume_before:
            self.photo_container_count += 1
        if (
            lowered == "img"
            and inside_resume_before
            and inside_photo_before
            and "src" in values
        ):
            self.photo_sources.append(values["src"])
        if lowered not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((lowered, classes))

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self._start(tag, attrs)

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self._start(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == lowered:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if self._inside("doctor-resume") and any(
            tag == "h1" for tag, _ in self.stack
        ):
            self.name_parts.append(data)


def page_referenced_photo(html: str, source_link: str, expected_name: str) -> str:
    parser = PhotoPageParser()
    parser.feed(html)
    if parser.resume_container_count != 1:
        raise RuntimeError("详情页缺少 doctor-resume 容器")
    actual_name = clean_text(" ".join(parser.name_parts))
    if actual_name != expected_name:
        raise RuntimeError(f"详情姓名不匹配：预期 {expected_name}，实际 {actual_name or '缺失'}")
    if parser.photo_container_count != 1:
        raise RuntimeError(
            f"doctor-img 容器数量不是 1：{parser.photo_container_count}"
        )
    if len(parser.photo_sources) != 1:
        raise RuntimeError(
            f"doctor-img 图片引用数量不是 1：{len(parser.photo_sources)}"
        )
    raw_url = clean_text(parser.photo_sources[0])
    if not raw_url:
        raise RuntimeError("doctor-img 图片 src 为空")
    photo_url = urljoin(source_link, raw_url)
    parsed = urlparse(photo_url)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != PHOTO_HOST
        or parsed.query
        or parsed.fragment
        or not PHOTO_PATH_RE.fullmatch(parsed.path)
    ):
        raise RuntimeError(f"页面引用照片越出授权 OSS 路径：{photo_url}")
    return photo_url


def magic_extension(content: bytes) -> str:
    if content.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if content.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP":
        return "webp"
    return ""


def image_dimensions(content: bytes) -> tuple[int, int]:
    with Image.open(io.BytesIO(content)) as image:
        image.verify()
    with Image.open(io.BytesIO(content)) as image:
        return image.size


def placeholder_reason(photo_url: str, content: bytes, extension: str) -> str:
    if extension != "gif" or len(content) >= SMALL_GIF_PLACEHOLDER_BYTES:
        return ""
    path = urlparse(photo_url).path.lower()
    if any(marker in path for marker in PLACEHOLDER_MARKERS):
        return "小 GIF 路径命中占位标记"
    with Image.open(io.BytesIO(content)) as image:
        probe = image.convert("RGB")
        probe.thumbnail((64, 64))
        colors = probe.getcolors(maxcolors=64 * 64 + 1) or []
        pixels = list(probe.get_flattened_data())
    if not pixels or len(colors) > 16:
        return ""
    neutral = sum(
        1
        for red, green, blue in pixels
        if min(red, green, blue) >= 180 and max(red, green, blue) - min(red, green, blue) <= 15
    )
    if neutral / len(pixels) >= 0.70:
        return "小 GIF 低色板且浅灰中性像素不少于 70%"
    return ""


def inspect_photo_response(
    response: HttpResult, photo_url: str
) -> tuple[str, int, int, str]:
    if not response.ok:
        raise RuntimeError(f"照片 HTTP {response.status_code}")
    content_type = clean_text(response.headers.get("content-type")).lower()
    mime = content_type.partition(";")[0]
    if not mime.startswith("image/"):
        raise RuntimeError(
            f"照片 HTTP {response.status_code} 返回非图片 Content-Type: {content_type or '缺失'}"
        )
    content = response.content
    if len(content) > FULL_FUSE_BYTES:
        raise RuntimeError(f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 单图超过 20 MiB：{photo_url}")
    extension = magic_extension(content)
    if extension not in SUPPORTED_EXTENSIONS:
        raise RuntimeError(f"照片魔数格式异常：{photo_url}")
    reason = placeholder_reason(photo_url, content, extension)
    if reason:
        raise RuntimeError(f"占位图：{reason}")
    width, height = image_dimensions(content)
    if width <= 0 or height <= 0:
        raise RuntimeError("照片尺寸无效")
    return extension, width, height, content_type


def file_digest(path: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "exists": True,
        "size": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def tree_digest(root: Path, pattern: str = "*") -> dict[str, Any]:
    if not root.exists():
        return {"exists": False, "file_count": 0, "total_bytes": 0, "sha256": ""}
    digest = hashlib.sha256()
    files = sorted(
        (path for path in root.rglob(pattern) if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    total_bytes = 0
    for path in files:
        content = path.read_bytes()
        total_bytes += len(content)
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(content).digest())
    return {
        "exists": True,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "sha256": digest.hexdigest(),
    }


def protected_snapshot() -> dict[str, Any]:
    files: dict[str, Any] = {}
    for path in PROTECTED_FILES:
        files[str(path)] = file_digest(path) if path.is_file() else {"exists": False}
    return {
        "files": files,
        "profile_markdown_tree": tree_digest(PROFILE_DIR, "*.md"),
        "formal_photo_tree": tree_digest(FORMAL_PHOTO_DIR),
    }


def load_scope_rows() -> list[dict[str, Any]]:
    payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    rows = [
        dict(row)
        for row in payload.get("rows", [])
        if clean_text(row.get("医院")) == HOSPITAL
    ]
    if len(rows) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError(
            f"Issue #{ISSUE_NUMBER} 范围漂移：应为 {EXPECTED_SCOPE_COUNT} 行，实际 {len(rows)} 行"
        )
    ids = [detail_id(row.get("来源链接")) for row in rows]
    if any(not value for value in ids) or len(set(ids)) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("范围内来源链接不是 415 个唯一授权官网详情")
    if any(clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")) for row in rows):
        raise RuntimeError("TRIAL 范围内已有正式照片字段，需 owner 先裁决")
    profile_files = [
        path for path in PROFILE_DIR.glob("*.md") if path.name != "_索引.md"
    ]
    if len(profile_files) != EXPECTED_SCOPE_COUNT or not (PROFILE_DIR / "_索引.md").is_file():
        raise RuntimeError("本院画像或索引数量不符合 415+1 基线")
    for path in [*profile_files, PROFILE_DIR / "_索引.md"]:
        text = path.read_text(encoding="utf-8")
        if AUTO_MARKER not in text:
            raise RuntimeError(f"画像缺少自动生成标记：{path}")
        if re.search(r"^!\[", text, flags=re.MULTILINE):
            raise RuntimeError(f"TRIAL 前画像已含图片引用：{path}")
    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("TRIAL 前正式照片目录已存在")
    return rows


def select_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {detail_id(row.get("来源链接")): row for row in rows}
    selected: list[dict[str, Any]] = []
    for expected_name, expected_department, expected_level, expected_id in SAMPLE_PLAN:
        row = by_id.get(expected_id)
        if row is None:
            raise RuntimeError(f"固定样本 ID 缺失：{expected_id}")
        if clean_text(row.get("姓名")) != expected_name:
            raise RuntimeError(f"固定样本姓名漂移：{expected_id}")
        if atomic_department(row) != expected_department:
            raise RuntimeError(f"固定样本科室漂移：{expected_name}")
        if title_level(row.get("职称_关键词")) != expected_level:
            raise RuntimeError(f"固定样本职称层级漂移：{expected_name}")
        selected.append(row)
    if len({atomic_department(row) for row in selected}) != EXPECTED_DEPARTMENT_COUNT:
        raise RuntimeError("固定样本未覆盖 10 个不同科室首原子")
    if Counter(title_level(row.get("职称_关键词")) for row in selected) != Counter(
        {"正高": 3, "副高": 3, "其他": 4}
    ):
        raise RuntimeError("固定样本职称分层不是 3/3/4")
    return selected


def allocate_trial_photo(
    row: dict[str, Any], extension: str, content: bytes
) -> tuple[Path, str]:
    filename = "-".join(
        (
            safe_photo_part(row.get("姓名")),
            safe_photo_part(atomic_department(row)),
            safe_photo_part(row.get("职称_关键词")),
            safe_photo_part(HOSPITAL),
        )
    ) + f".{extension}"
    path = TRIAL_PHOTO_DIR / filename
    if path.exists() and path.read_bytes() != content:
        raise RuntimeError(f"TRIAL 照片已存在且字节不同，拒绝覆盖：{path}")
    path.write_bytes(content)
    return path, filename


def contact_sheet_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    )
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def build_contact_sheet(samples: list[dict[str, Any]]) -> None:
    if len(samples) != EXPECTED_TRIAL_COUNT:
        raise RuntimeError("联系表要求 10 张实图")
    card_width, card_height = 320, 430
    sheet = Image.new("RGB", (card_width * 5, card_height * 2), "white")
    name_font = contact_sheet_font(24)
    meta_font = contact_sheet_font(17)
    for index, sample in enumerate(samples):
        with Image.open(sample["trial_file"]) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            image.thumbnail((280, 315), Image.Resampling.LANCZOS)
        left = (index % 5) * card_width
        top = (index // 5) * card_height
        x = left + (card_width - image.width) // 2
        y = top + 12 + (315 - image.height) // 2
        sheet.paste(image, (x, y))
        draw = ImageDraw.Draw(sheet)
        draw.rectangle((left, top, left + card_width - 1, top + card_height - 1), outline="#c9d2dc")
        draw.text((left + 16, top + 337), sample["name"], fill="#111827", font=name_font)
        draw.text(
            (left + 16, top + 372),
            f"{sample['department']}｜{sample['title'] or '未标注'}",
            fill="#374151",
            font=meta_font,
        )
        draw.text(
            (left + 16, top + 401),
            f"{sample['width']}×{sample['height']}｜{sample['byte_size']:,} B",
            fill="#6b7280",
            font=meta_font,
        )
    sheet.save(CONTACT_SHEET_PATH, format="JPEG", quality=92, optimize=True)


def write_manifest(samples: list[dict[str, Any]]) -> None:
    headers = (
        "姓名",
        "科室",
        "职称",
        "职称层级",
        "详情ID",
        "来源链接",
        "详情HTTP链",
        "照片链接",
        "照片HTTP链",
        "照片Content-Type",
        "照片文件",
        "字节数",
        "宽度",
        "高度",
        "SHA-256",
        "魔数格式",
        "Referer",
        "大图终审",
    )
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for sample in samples:
            writer.writerow(
                {
                    "姓名": sample["name"],
                    "科室": sample["department"],
                    "职称": sample["title"],
                    "职称层级": sample["title_level"],
                    "详情ID": sample["detail_id"],
                    "来源链接": sample["source_link"],
                    "详情HTTP链": sample["detail_http_trace"],
                    "照片链接": sample["photo_url"],
                    "照片HTTP链": sample["photo_http_trace"],
                    "照片Content-Type": sample["photo_content_type"],
                    "照片文件": sample["filename"],
                    "字节数": sample["byte_size"],
                    "宽度": sample["width"],
                    "高度": sample["height"],
                    "SHA-256": sample["sha256"],
                    "魔数格式": sample["extension"],
                    "Referer": sample["referer"],
                    "大图终审": "是" if sample["owner_review_required"] else "否",
                }
            )


def size_bucket(size: int) -> str:
    if size < 200 * 1024:
        return "<200KiB"
    if size < 1024 * 1024:
        return "200KiB-1MiB"
    if size <= OWNER_REPORT_BYTES:
        return "1-5MiB"
    return "5-20MiB"


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    table = "\n".join(
        "| {name} | {department} | {title} | {byte_size:,} | {width}×{height} | `{sha256}` |".format(
            **sample
        )
        for sample in payload["photo_samples"]
    )
    buckets = "、".join(
        f"{name}={count}" for name, count in meta["size_buckets"].items()
    )
    TRIAL_REPORT_PATH.write_text(
        f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 TRIAL 报告

## 结论

- 阶段：`TRIAL_READY_FOR_OWNER_AUDIT`
- 范围：本院 {meta['scope_count']} 行，TRIAL 前照片字段全空。
- 固定样本：{meta['trial_detail_count']} 人 / {meta['department_coverage_count']} 个科室首原子；职称分层 `正高 3 / 副高 3 / 其他 4`。
- 实采：{meta['downloaded_count']}/{meta['trial_detail_count']}；问题 {meta['problem_count']}；熔断问题 0。
- 照片总字节：{meta['total_bytes']:,}；最小 {meta['min_bytes']:,}；中位数 {meta['median_bytes']:,}；平均 {meta['average_bytes']:,}；最大 {meta['max_bytes']:,}。
- 大小分桶：{buckets}；超过 5 MiB：{meta['owner_review_photo_count']}；超过 20 MiB：0。
- 估算 415 行容量：约 {meta['estimated_full_mib']:.2f} MiB（仅容量估算，不代表 FULL 实际结果）。

## 来源与排除边界

- 官网首页：<{OFFICIAL_HOME}>
- 医生目录：<{DIRECTORY_URL}>
- 详情来源仅接受 `https://www.gzszyy.com/expert/<年份>/<ID>.html`。
- 照片仅取详情 `.doctor-resume div.doctor-img` 唯一 `img[src]`，并仅接受页面实际引用的 `https://{PHOTO_HOST}/<YYYYMMDD>/<数字>.<格式>`。
- 图片请求携带对应详情页 Referer；不构造或探测页面未引用路径。
- `div.qr-img`、`static.gzszyy.com/images/`、空 `src` 均不进入候选。
- 占位检测沿用小 GIF 双侧边界；未单凭格式或尺寸判定占位。

## 固定样本

| 姓名 | 科室 | 职称 | 字节数 | 尺寸 | SHA-256 |
|---|---|---|---:|---:|---|
{table}

## 正式资产保护

- TRIAL 仅写入 `work` 独立工件；入口台账、总底表三载体、总底表更新报告、415 份画像、索引和正式照片目录前后快照一致。
- 本院 415 份画像与 `_索引.md` 均保留 `{AUTO_MARKER}`；TRIAL 前零图片引用，正式照片目录不存在。
- 联系表：`{CONTACT_SHEET_PATH}`。
- 联系表视觉结论：`{meta.get('visual_review', 'PENDING_CONTACT_SHEET_REVIEW')}`。

## 停止点

TRIAL 工件完成后停止，等待 `nancywrayg57-jpg` 审计联系表、逐图来源和大小分布。未取得关联 PR 中 owner 明确 `通过` / `有条件通过` 且切换为 `FULL_APPEND_AND_OBSIDIAN` 前，不得修改正式资产。
""",
        encoding="utf-8",
    )


def validate_payload(payload: dict[str, Any]) -> None:
    errors: list[str] = []
    meta = payload.get("meta", {})
    samples = payload.get("photo_samples", [])
    if meta.get("issue") != ISSUE_NUMBER or meta.get("hospital") != HOSPITAL:
        errors.append("Issue 或医院不匹配")
    if meta.get("phase") != "TRIAL_READY_FOR_OWNER_AUDIT":
        errors.append("阶段不是 TRIAL_READY_FOR_OWNER_AUDIT")
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围不是 415")
    if meta.get("scope_blank_photo_row_count") != EXPECTED_SCOPE_COUNT:
        errors.append("TRIAL 基线照片字段不是全空")
    if meta.get("trial_detail_count") != EXPECTED_TRIAL_COUNT:
        errors.append("固定样本不是 10")
    if meta.get("department_coverage_count") != EXPECTED_DEPARTMENT_COUNT:
        errors.append("科室首原子覆盖不是 10")
    if Counter(meta.get("title_level_counts", {})) != Counter(
        {"正高": 3, "副高": 3, "其他": 4}
    ):
        errors.append("职称分层不是 3/3/4")
    if len(samples) != EXPECTED_TRIAL_COUNT or meta.get("problem_count") != 0:
        errors.append("TRIAL 未达到 10/10 实采")
    if len({sample.get("detail_id") for sample in samples}) != len(samples):
        errors.append("样本详情 ID 不唯一")
    if len({sample.get("department") for sample in samples}) != EXPECTED_DEPARTMENT_COUNT:
        errors.append("样本科室不唯一")
    for sample in samples:
        path = Path(sample.get("trial_file") or "")
        if not path.is_file():
            errors.append(f"TRIAL 照片缺失：{path}")
            continue
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != sample.get("sha256"):
            errors.append(f"SHA-256 不一致：{path.name}")
        if len(content) != sample.get("byte_size"):
            errors.append(f"字节数不一致：{path.name}")
        if magic_extension(content) != sample.get("extension"):
            errors.append(f"魔数格式不一致：{path.name}")
        if image_dimensions(content) != (sample.get("width"), sample.get("height")):
            errors.append(f"尺寸不一致：{path.name}")
        parsed = urlparse(clean_text(sample.get("photo_url")))
        if (
            (parsed.hostname or "").lower() != PHOTO_HOST
            or parsed.query
            or parsed.fragment
            or not PHOTO_PATH_RE.fullmatch(parsed.path)
        ):
            errors.append(f"照片 URL 越界：{sample.get('photo_url')}")
        if clean_text(sample.get("referer")) != clean_text(sample.get("source_link")):
            errors.append(f"Referer 不匹配：{sample.get('name')}")
    if not CONTACT_SHEET_PATH.is_file():
        errors.append("联系表缺失")
    before = meta.get("protected_snapshot_before")
    after = meta.get("protected_snapshot_after")
    if before != after or after != protected_snapshot():
        errors.append("正式受保护资产快照发生变化")
    if errors:
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} TRIAL 门禁失败：" + "；".join(errors))


def run_trial(run_date: str) -> dict[str, Any]:
    baseline = protected_snapshot()
    rows = load_scope_rows()
    selected = select_trial_rows(rows)
    session = OfficialSession()
    home = session.get(OFFICIAL_HOME)
    require_html(home, "官网首页")
    directory = session.get(DIRECTORY_URL, OFFICIAL_HOME)
    require_html(directory, "医生目录")
    TRIAL_PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    samples: list[dict[str, Any]] = []
    problems: list[dict[str, Any]] = []
    for row in selected:
        name = clean_text(row.get("姓名"))
        source_link = clean_text(row.get("来源链接"))
        try:
            detail_response = session.get(source_link, DIRECTORY_URL)
            detail_html = require_html(detail_response, f"{name}详情页")
            photo_url = page_referenced_photo(detail_html, source_link, name)
            photo_response = session.get(photo_url, source_link)
            extension, width, height, photo_type = inspect_photo_response(
                photo_response, photo_url
            )
            content = photo_response.content
            trial_path, filename = allocate_trial_photo(row, extension, content)
            samples.append(
                {
                    "name": name,
                    "department": atomic_department(row),
                    "title": clean_text(row.get("职称_关键词")),
                    "title_level": title_level(row.get("职称_关键词")),
                    "detail_id": detail_id(source_link),
                    "source_link": source_link,
                    "detail_status": detail_response.status_code,
                    "detail_http_trace": response_trace(detail_response),
                    "detail_content_type": clean_text(detail_response.headers.get("content-type")),
                    "photo_url": photo_url,
                    "photo_status": photo_response.status_code,
                    "photo_http_trace": response_trace(photo_response),
                    "photo_content_type": photo_type,
                    "referer": source_link,
                    "extension": extension,
                    "filename": filename,
                    "trial_file": str(trial_path),
                    "byte_size": len(content),
                    "width": width,
                    "height": height,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "owner_review_required": len(content) > OWNER_REPORT_BYTES,
                }
            )
        except (RuntimeError, OSError) as exc:
            problems.append(
                {
                    "name": name,
                    "department": atomic_department(row),
                    "title": clean_text(row.get("职称_关键词")),
                    "detail_id": detail_id(source_link),
                    "source_link": source_link,
                    "error": str(exc),
                }
            )
    if len(problems) / EXPECTED_TRIAL_COUNT > MAX_FAILURE_RATIO:
        raise RuntimeError(
            f"[FATAL - HUMAN_INTERVENTION_REQUIRED] TRIAL 熔断问题超过 30%：{len(problems)}/{EXPECTED_TRIAL_COUNT}"
        )
    build_contact_sheet(samples)
    sizes = [sample["byte_size"] for sample in samples]
    if not sizes:
        raise RuntimeError("TRIAL 未采得任何照片")
    after = protected_snapshot()
    if baseline != after:
        raise RuntimeError("TRIAL 执行修改了正式受保护资产")
    bucket_counter = Counter(size_bucket(size) for size in sizes)
    ordered_buckets = {
        name: bucket_counter.get(name, 0)
        for name in ("<200KiB", "200KiB-1MiB", "1-5MiB", "5-20MiB")
    }
    average_bytes = sum(sizes) / len(sizes)
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "hospital": HOSPITAL,
            "phase": "TRIAL_READY_FOR_OWNER_AUDIT",
            "run_date": run_date,
            "official_home": OFFICIAL_HOME,
            "doctor_directory": DIRECTORY_URL,
            "scope_count": len(rows),
            "scope_unique_source_count": len({detail_id(row.get('来源链接')) for row in rows}),
            "scope_blank_photo_row_count": sum(
                1
                for row in rows
                if not clean_text(row.get("照片链接")) and not clean_text(row.get("照片文件"))
            ),
            "trial_detail_count": len(selected),
            "department_coverage_count": len({atomic_department(row) for row in selected}),
            "title_level_counts": dict(Counter(title_level(row.get("职称_关键词")) for row in selected)),
            "downloaded_count": len(samples),
            "problem_count": len(problems),
            "total_bytes": sum(sizes),
            "min_bytes": min(sizes),
            "median_bytes": int(median(sizes)),
            "average_bytes": int(round(average_bytes)),
            "max_bytes": max(sizes),
            "size_buckets": ordered_buckets,
            "owner_review_photo_count": sum(1 for size in sizes if size > OWNER_REPORT_BYTES),
            "estimated_full_count": EXPECTED_SCOPE_COUNT,
            "estimated_full_bytes": int(round(average_bytes * EXPECTED_SCOPE_COUNT)),
            "estimated_full_mib": average_bytes * EXPECTED_SCOPE_COUNT / 1024 / 1024,
            "home_http_trace": response_trace(home),
            "directory_http_trace": response_trace(directory),
            "formal_photo_dir_existed_before": baseline["formal_photo_tree"]["exists"],
            "profile_markdown_count": baseline["profile_markdown_tree"]["file_count"],
            "visual_review": "PENDING_CONTACT_SHEET_REVIEW",
            "protected_snapshot_before": baseline,
            "protected_snapshot_after": after,
        },
        "photo_samples": samples,
        "problems": problems,
        "artifacts": {
            "json_path": str(TRIAL_JSON_PATH),
            "csv_path": str(TRIAL_CSV_PATH),
            "report_path": str(TRIAL_REPORT_PATH),
            "contact_sheet_path": str(CONTACT_SHEET_PATH),
            "trial_photo_dir": str(TRIAL_PHOTO_DIR),
        },
    }
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_manifest(samples)
    write_report(payload)
    validate_payload(payload)
    return payload


def utc_now_text() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_failure_warning(value: Any, state: str) -> str:
    if state not in FULL_WARNING_BY_STATE:
        raise ValueError(f"未知照片失败状态：{state}")
    warning = FULL_WARNING_BY_STATE[state]
    existing = [item for item in clean_text(value).split("；") if item]
    if warning not in existing:
        existing.append(warning)
    return "；".join(existing)


def response_signature(response: HttpResult) -> str:
    content_type = clean_text(response.headers.get("content-type")).lower()
    mime = content_type.partition(";")[0]
    return f"HTTP {response.status_code} {mime or 'NO-CONTENT-TYPE'}"


def retryable_get(
    session: OfficialSession,
    url: str,
    referer: str,
    accept_response: Any,
) -> tuple[HttpResult | None, list[dict[str, Any]]]:
    """GET once when healthy; on failure, make two 30-second-spaced retries."""
    attempts: list[dict[str, Any]] = []
    response: HttpResult | None = None
    for attempt_number in range(1, DETAIL_RETRY_COUNT + 2):
        if attempt_number > 1:
            time.sleep(DETAIL_RETRY_INTERVAL_SECONDS)
        started_at = utc_now_text()
        try:
            candidate = session.get(url, referer)
            accepted = bool(accept_response(candidate))
            signature = response_signature(candidate)
            attempts.append(
                {
                    "attempt": attempt_number,
                    "utc": started_at,
                    "status": candidate.status_code,
                    "content_type": clean_text(candidate.headers.get("content-type")),
                    "signature": signature,
                    "accepted": accepted,
                    "http_trace": response_trace(candidate),
                }
            )
            response = candidate
        except (RuntimeError, OSError) as exc:
            attempts.append(
                {
                    "attempt": attempt_number,
                    "utc": started_at,
                    "status": "EXCEPTION",
                    "content_type": "",
                    "signature": f"EXCEPTION {type(exc).__name__}",
                    "accepted": False,
                    "http_trace": "",
                    "error": str(exc),
                }
            )
            response = None
            accepted = False
        if accepted:
            break
    if len(attempts) > 1:
        signatures = {clean_text(item.get("signature")) for item in attempts}
        accepted_states = {bool(item.get("accepted")) for item in attempts}
        if len(signatures) > 1 or len(accepted_states) > 1:
            raise RuntimeError(
                "[FATAL - HUMAN_INTERVENTION_REQUIRED] 同一 URL 状态闪烁，"
                "停止正式写入并申请 owner 启动 5 轮聚合协议："
                f"{url}；" + "；".join(
                    f"{item['utc']} {item['signature']} accepted={item['accepted']}"
                    for item in attempts
                )
            )
    return response if attempts[-1]["accepted"] else None, attempts


def attempt_evidence_text(attempts: list[dict[str, Any]]) -> str:
    return "；".join(
        f"attempt={item['attempt']} utc={item['utc']} status={item['status']} "
        f"content-type={item.get('content_type') or '缺失'}"
        for item in attempts
    )


def validate_retry_attempts(attempts: list[dict[str, Any]]) -> None:
    if len(attempts) < DETAIL_RETRY_COUNT + 1:
        raise RuntimeError("详情不可达证据少于初次请求加 2 次重试")
    parsed: list[datetime] = []
    for expected_attempt, item in enumerate(attempts, start=1):
        if int(item.get("attempt") or 0) != expected_attempt:
            raise RuntimeError("详情不可达重试序号不连续")
        stamp = clean_text(item.get("utc"))
        if not stamp.endswith("Z") or item.get("status") in {None, ""}:
            raise RuntimeError("详情不可达重试缺少 UTC 或 HTTP 状态")
        parsed.append(datetime.fromisoformat(stamp.replace("Z", "+00:00")))
    for before, after in zip(parsed, parsed[1:]):
        if (after - before).total_seconds() < DETAIL_RETRY_INTERVAL_SECONDS:
            raise RuntimeError("详情不可达重试间隔不足 30 秒")
    signatures = {clean_text(item.get("signature")) for item in attempts}
    accepted_states = {bool(item.get("accepted")) for item in attempts}
    if len(signatures) != 1 or len(accepted_states) != 1:
        raise RuntimeError("详情不可达证据出现状态闪烁")


def inspect_full_page_reference(
    html: str, source_link: str, expected_name: str
) -> tuple[str, str, str]:
    parser = PhotoPageParser()
    parser.feed(html)
    actual_name = clean_text(" ".join(parser.name_parts))
    if parser.resume_container_count != 1:
        return "无照片容器", "", f"doctor-resume 数量={parser.resume_container_count}"
    if actual_name != expected_name:
        return (
            "无照片容器",
            "",
            f"详情姓名不匹配：预期 {expected_name}，实际 {actual_name or '缺失'}",
        )
    if parser.photo_container_count != 1:
        return "无照片容器", "", f"doctor-img 数量={parser.photo_container_count}"
    if len(parser.photo_sources) != 1 or not clean_text(parser.photo_sources[0]):
        return (
            "无照片容器",
            "",
            f"doctor-img 非空图片引用数量={sum(bool(clean_text(item)) for item in parser.photo_sources)}",
        )
    photo_url = urljoin(source_link, clean_text(parser.photo_sources[0]))
    parsed = urlparse(photo_url)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != PHOTO_HOST
        or parsed.query
        or parsed.fragment
        or not PHOTO_PATH_RE.fullmatch(parsed.path)
    ):
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] 页面唯一 doctor-img 引用越出授权 OSS 路径："
            f"{photo_url}"
        )
    return "", photo_url, ""


def allocate_full_photo_path(
    row: dict[str, Any],
    source_id: str,
    extension: str,
    output_dir: Path,
    used_filenames: set[str],
) -> tuple[str, Path]:
    stem = "-".join(
        (
            safe_photo_part(row.get("姓名")),
            safe_photo_part(atomic_department(row)),
            safe_photo_part(row.get("职称_关键词")),
            safe_photo_part(HOSPITAL),
        )
    )
    filename = f"{stem}.{extension}"
    folded = filename.casefold()
    if folded in used_filenames:
        filename = f"{stem}-{safe_photo_part(source_id)}.{extension}"
        folded = filename.casefold()
    if folded in used_filenames or (output_dir / filename).exists():
        raise RuntimeError(f"照片命名仍冲突，拒绝覆盖：{filename}")
    used_filenames.add(folded)
    return filename, output_dir / filename


def row_value(value: Any) -> str:
    return "" if value is None else str(value)


def canonical_master_row(row: dict[str, Any]) -> tuple[str, ...]:
    return tuple(row_value(row.get(header)) for header in BASE_HEADERS)


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
        for column in BASE_HEADERS:
            old = row_value(before.get(column))
            new = row_value(after.get(column))
            if old == new:
                continue
            source = clean_text(after.get("来源链接"))
            if source not in target_sources:
                raise RuntimeError(f"发现 Issue #{ISSUE_NUMBER} 范围外行修改：{source} {column}")
            diffs.append(
                {
                    "底表行": str(sheet_row),
                    "序号": clean_text(after.get("序号")),
                    "姓名": clean_text(after.get("姓名")),
                    "来源链接": source,
                    "列名": column,
                    "修改前": old,
                    "修改后": new,
                }
            )
    unexpected = sorted({item["列名"] for item in diffs} - FULL_ALLOWED_ROW_COLUMNS)
    if unexpected:
        raise RuntimeError("发现范围外字段修改：" + "、".join(unexpected))
    return diffs


def recompute_failure_derivatives(
    payload: dict[str, Any], rows: list[dict[str, Any]]
) -> None:
    warning_counter: Counter[str] = Counter()
    for row in rows:
        for warning in clean_text(row.get("异常提示")).split("；"):
            if warning:
                warning_counter[warning] += 1
    payload["warning_counts"] = dict(warning_counter)
    import collect_official_doctors_batch as collector

    payload["hospital_batches"] = collector.build_hospital_batches(rows)


def write_master_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BASE_HEADERS)
        writer.writeheader()
        writer.writerows(
            {key: row.get(key, "") for key in BASE_HEADERS} for row in rows
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
        "失败三态",
        "照片链接",
        "照片文件",
        "字节数",
        "SHA-256",
        "魔数",
        "宽",
        "高",
        "错误证据",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(
            {header: item.get(header, "") for header in headers}
            for item in payload["reconciliation"]
        )


def write_full_report(path: Path, payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    state_counts = meta["failure_state_counts"]
    failure_lines = "\n".join(
        f"| {state} | {state_counts.get(state, 0)} |" for state in FULL_FAILURE_STATES
    )
    bucket_order = ["<200KiB", "200KiB-1MiB", "1-5MiB", "5-20MiB", ">20MiB"]
    bucket_lines = "\n".join(
        f"| {bucket} | {meta['size_bucket_counts'].get(bucket, 0)} |"
        for bucket in bucket_order
    )
    large_photos = [
        item
        for item in payload.get("photo_samples", [])
        if int(item.get("bytes") or 0) > OWNER_REPORT_BYTES
    ]
    large_photo_lines = "\n".join(
        "| {name} | <{url}> | {bytes_count} | {width}×{height} |".format(
            name=clean_text(item.get("name")),
            url=clean_text(item.get("photo_url")),
            bytes_count=int(item.get("bytes") or 0),
            width=int(item.get("width") or 0),
            height=int(item.get("height") or 0),
        )
        for item in large_photos
    ) or "| 无 | — | 0 | — |"
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 FULL 报告

> 日期：{meta['run_date']}
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`
> 照片政策：`OWNER_APPROVED_UNIQUE_DOCTOR_IMG_OSS_ORIGINAL_BYTES`

## 四数对账

| 范围 / 应采 | 实采 | 失败 | 留空 |
|---:|---:|---:|---:|
| {meta['expected_count']} | {meta['downloaded_count']} | {meta['failed_count']} | {meta['blank_count']} |

| 失败三态 | 数量 |
|---|---:|
{failure_lines}

## 大小分布

| 分桶 | 数量 |
|---|---:|
{bucket_lines}

- 总问题率：{meta['failed_count']}/{meta['expected_count']}（{meta['failure_ratio']:.2%}），未超过 30% 熔断线。
- 照片总字节：{meta['photo_total_bytes']} bytes（{meta['photo_total_mib']:.2f} MiB）。
- 最大单张：{meta['photo_max_bytes']} bytes；超过 5 MiB：{meta['over_5mib_count']} 张；超过 20 MiB：{meta['over_20mib_count']} 张。
- 详情不可达：初次请求后至少重试 2 次，间隔均不低于 30 秒，逐次 HTTP 状态与 UTC 已写入 payload；状态闪烁数 0。
- 页面未引用路径构造/探测：0；第三方来源：0；仅使用 `.doctor-resume div.doctor-img` 唯一引用及 `oss.gzszyy.com`。
- 排除 `div.qr-img`、`static.gzszyy.com/images/`、空 src 和页面未引用路径。
- 总底表：payload/CSV/XLSX 三载体逐值一致；仅本院 415 行照片两列及失败行异常提示允许变化。
- 画像：既有 {meta['existing_profile_count']} 份 AUTO 标记画像中，成功的 {meta['profile_refreshed_count']} 份仅在基础信息区新增照片引用；失败画像零触碰；不新建画像；`_索引.md` 零修改。
- 入口台账三载体与总底表更新报告保持不变。

## >5 MiB Owner 终审清单

| 姓名 | URL | 字节 | 尺寸 |
|---|---|---:|---:|
{large_photo_lines}

## 工件

- `{FULL_JSON_PATH}`
- `{FULL_CSV_PATH}`
- `{FULL_REPORT_PATH}`
- `{FORMAL_PHOTO_DIR}`

## 合规边界

1. 只访问 415 条既有医院官网医生详情链接及页面唯一 `.doctor-resume div.doctor-img img[src]` 实际引用的医院 OSS 原图。
2. 照片请求携带对应详情页 Referer；保存页面引用版本原始字节，不压缩。
3. 禁止构造或探测页面未引用图片路径；禁止第三方来源；二维码、装饰图与空 src 不进入候选。
4. 失败仅按“详情不可达 / 无照片容器 / 占位图”留空并幂等追加异常提示。
"""
    path.write_text(report, encoding="utf-8", newline="\n")


def validate_full_payload(payload: dict[str, Any], photo_root: Path) -> None:
    meta = payload.get("meta", {})
    expected = int(meta.get("expected_count") or 0)
    downloaded = int(meta.get("downloaded_count") or 0)
    failed = int(meta.get("failed_count") or 0)
    blank = int(meta.get("blank_count") or 0)
    if expected != EXPECTED_SCOPE_COUNT or downloaded + failed != expected or blank != failed:
        raise RuntimeError("FULL 范围/应采/实采/失败/留空未形成四数闭环")
    state_counts = Counter(meta.get("failure_state_counts") or {})
    if set(state_counts) - set(FULL_FAILURE_STATES) or sum(state_counts.values()) != failed:
        raise RuntimeError("FULL 失败三态分布不闭合")
    if expected and failed / expected > MAX_FAILURE_RATIO:
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 总问题率超过 30%："
            f"{failed}/{expected}"
        )
    if int(meta.get("status_flicker_count") or 0):
        raise RuntimeError("FULL 存在状态闪烁，必须启动 5 轮聚合协议")
    if int(meta.get("constructed_unreferenced_probe_count") or 0):
        raise RuntimeError("FULL 发生页面未引用路径探测")
    if int(meta.get("third_party_source_count") or 0):
        raise RuntimeError("FULL 发生第三方来源访问")
    if int(meta.get("existing_profile_count") or 0) != EXPECTED_PROFILE_COUNT:
        raise RuntimeError("FULL 既有画像数量漂移")
    if int(meta.get("no_profile_scope_count") or 0):
        raise RuntimeError("FULL 目标范围存在缺失画像")
    if int(meta.get("profile_refreshed_count") or 0) != downloaded:
        raise RuntimeError("FULL 成功照片数与画像嵌入数不一致")

    reconciliation = payload.get("reconciliation", [])
    rows = payload.get("rows", [])
    photos = payload.get("photo_samples", [])
    failures = payload.get("failures", [])
    if len(reconciliation) != expected or len(rows) != expected or len(photos) != downloaded:
        raise RuntimeError("FULL 415 行对账工件数量不一致")
    rows_by_source = {clean_text(row.get("来源链接")): row for row in rows}
    photos_by_source = {clean_text(item.get("source_link")): item for item in photos}
    failure_by_source = {clean_text(item.get("source_link")): item for item in failures}
    if len(rows_by_source) != expected or len(photos_by_source) != downloaded:
        raise RuntimeError("FULL 来源链接对账不唯一")

    expected_files: set[str] = set()
    total_bytes = 0
    max_bytes = 0
    over_5mib_count = 0
    over_20mib_count = 0
    bucket_counter: Counter[str] = Counter()
    for item in reconciliation:
        source = clean_text(item.get("来源链接"))
        row = rows_by_source.get(source)
        if row is None:
            raise RuntimeError(f"FULL 对账缺少总底表目标行：{source}")
        state = clean_text(item.get("失败三态"))
        status = clean_text(item.get("状态"))
        if status == "实采":
            if state or source not in photos_by_source:
                raise RuntimeError(f"FULL 实采行状态不一致：{source}")
            photo = photos_by_source[source]
            if clean_text(row.get("照片链接")) != clean_text(photo.get("photo_url")):
                raise RuntimeError(f"FULL 实采行照片链接不一致：{source}")
            if clean_text(row.get("照片文件")) != clean_text(photo.get("photo_file")):
                raise RuntimeError(f"FULL 实采行照片文件不一致：{source}")
            filename = clean_text(photo.get("filename"))
            disk_path = photo_root / filename
            content = disk_path.read_bytes()
            extension = disk_path.suffix.lower().lstrip(".")
            if len(content) != int(photo.get("bytes") or 0):
                raise RuntimeError(f"照片字节数对账失败：{filename}")
            if hashlib.sha256(content).hexdigest() != clean_text(photo.get("sha256")):
                raise RuntimeError(f"照片 SHA-256 对账失败：{filename}")
            if magic_extension(content) != extension:
                raise RuntimeError(f"照片魔数与扩展名不符：{filename}")
            if content[:12].hex().upper() != clean_text(photo.get("magic_hex")):
                raise RuntimeError(f"照片魔数证据不一致：{filename}")
            if image_dimensions(content) != (
                int(photo.get("width") or 0),
                int(photo.get("height") or 0),
            ):
                raise RuntimeError(f"照片尺寸对账失败：{filename}")
            parsed_photo = urlparse(clean_text(photo.get("photo_url")))
            if (
                parsed_photo.scheme != "https"
                or (parsed_photo.hostname or "").lower() != PHOTO_HOST
                or parsed_photo.query
                or parsed_photo.fragment
                or not PHOTO_PATH_RE.fullmatch(parsed_photo.path)
            ):
                raise RuntimeError(f"照片 URL 越界：{photo.get('photo_url')}")
            expected_files.add(filename)
            total_bytes += len(content)
            max_bytes = max(max_bytes, len(content))
            over_5mib_count += int(len(content) > OWNER_REPORT_BYTES)
            over_20mib_count += int(len(content) > FULL_FUSE_BYTES)
            bucket_counter[size_bucket(len(content))] += 1
        elif status == "失败":
            if state not in FULL_FAILURE_STATES:
                raise RuntimeError(f"FULL 失败行未归入三态：{source}")
            if clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")):
                raise RuntimeError(f"FULL 失败行未留空照片字段：{source}")
            if FULL_WARNING_BY_STATE[state] not in clean_text(row.get("异常提示")):
                raise RuntimeError(f"FULL 失败行未追加异常提示：{source}")
            failure = failure_by_source.get(source)
            if failure is None:
                raise RuntimeError(f"FULL 失败行缺少失败证据：{source}")
            if state == "详情不可达":
                validate_retry_attempts(failure.get("attempts") or [])
        else:
            raise RuntimeError(f"FULL 对账状态非法：{source} {status}")

    actual_files = {item.name for item in photo_root.iterdir() if item.is_file()}
    if actual_files != expected_files:
        raise RuntimeError("FULL 照片目录磁盘集合与照片对账不一致")
    if total_bytes != int(meta.get("photo_total_bytes") or 0):
        raise RuntimeError("FULL 照片总字节对账失败")
    if max_bytes != int(meta.get("photo_max_bytes") or 0):
        raise RuntimeError("FULL 最大单张字节对账失败")
    if over_5mib_count != int(meta.get("over_5mib_count") or 0):
        raise RuntimeError("FULL 超过 5 MiB 照片计数对账失败")
    if over_20mib_count != int(meta.get("over_20mib_count") or 0):
        raise RuntimeError("FULL 超过 20 MiB 照片计数对账失败")
    if dict(bucket_counter) != dict(meta.get("size_bucket_counts") or {}):
        raise RuntimeError("FULL 照片大小分布对账失败")
    if over_20mib_count:
        raise RuntimeError("FULL 存在超过 20 MiB 照片")


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
    return bom + insert_profile_photo_block(before_text, doctor_name, photo_file).encode(
        "utf-8"
    )


def validate_profile_photo_only_bytes(
    before_bytes: bytes, after_bytes: bytes, doctor_name: str, photo_file: str
) -> None:
    if after_bytes != insert_profile_photo_block_bytes(
        before_bytes, doctor_name, photo_file
    ):
        raise RuntimeError(f"画像出现照片嵌入区块以外字节变化：{doctor_name}")


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
        staging = target.with_name(f".{target.name}.issue67.tmp")
        if staging.exists():
            staging.unlink()
        shutil.copy2(source, staging)
        staging.replace(target)


def restore_file_targets(backups: dict[Path, Path | None]) -> None:
    for target, backup in backups.items():
        staging = target.with_name(f".{target.name}.issue67.restore")
        if staging.exists():
            staging.unlink()
        if backup is None:
            target.unlink(missing_ok=True)
            continue
        shutil.copy2(backup, staging)
        staging.replace(target)


def target_profile_paths(
    profile_root: Path, target_sources: set[str]
) -> dict[str, Path]:
    import generate_obsidian_profiles as profiles

    all_sources = profiles.extract_existing_sources(profile_root)
    missing = target_sources - set(all_sources)
    if missing:
        raise RuntimeError("FULL 前目标范围缺少既有画像：" + "、".join(sorted(missing)[:5]))
    result = {source: all_sources[source] for source in target_sources}
    if len(result) != EXPECTED_PROFILE_COUNT:
        raise RuntimeError(
            f"FULL 前目标画像来源数量漂移：应为 {EXPECTED_PROFILE_COUNT}，实际 {len(result)}"
        )
    profile_files = {
        path for path in profile_root.glob("*.md") if path.name != "_索引.md"
    }
    if len(profile_files) != EXPECTED_PROFILE_COUNT or set(result.values()) != profile_files:
        raise RuntimeError("FULL 前 415 个来源与 415 份画像不是一一对应")
    return result


def preflight_profile_bytes(
    profile_paths: dict[str, Path], rows_by_source: dict[str, dict[str, Any]]
) -> dict[str, bytes]:
    before_profile_bytes: dict[str, bytes] = {}
    probe_file = (PHOTO_RELATIVE_ROOT / "__preflight__.jpg").as_posix()
    marker_bytes = AUTO_MARKER.encode("utf-8")
    for source, path in profile_paths.items():
        content = path.read_bytes()
        doctor_name = clean_text(rows_by_source[source].get("姓名"))
        if marker_bytes not in content:
            raise RuntimeError(f"画像缺少 AUTO 标记：{doctor_name}")
        insert_profile_photo_block_bytes(content, doctor_name, probe_file)
        before_profile_bytes[source] = content
    return before_profile_bytes


def validate_full_installation(payload: dict[str, Any]) -> None:
    final_rows = validate_master_layers(
        MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH
    )
    validate_full_payload(payload, FORMAL_PHOTO_DIR)
    payload_rows = payload.get("rows", [])
    target_sources = {clean_text(row.get("来源链接")) for row in payload_rows}
    if len(target_sources) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL payload 目标来源数量漂移")
    final_target_rows = [
        row for row in final_rows if clean_text(row.get("医院")) == HOSPITAL
    ]
    if {
        clean_text(row.get("来源链接")): canonical_master_row(row)
        for row in final_target_rows
    } != {
        clean_text(row.get("来源链接")): canonical_master_row(row)
        for row in payload_rows
    }:
        raise RuntimeError("FULL payload 目标行与已落盘总底表不一致")
    profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
    integrity = {
        clean_text(item.get("source_link")): item
        for item in payload.get("profile_integrity", [])
    }
    if len(integrity) != EXPECTED_PROFILE_COUNT:
        raise RuntimeError("FULL 画像完整性清单数量漂移")
    for source, path in profile_paths.items():
        expected = integrity.get(source)
        if expected is None:
            raise RuntimeError(f"FULL 画像完整性清单缺少来源：{source}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != clean_text(
            expected.get("after_sha256")
        ):
            raise RuntimeError(f"FULL 画像落盘哈希不一致：{path}")
    index_path = PROFILE_DIR / "_索引.md"
    if hashlib.sha256(index_path.read_bytes()).hexdigest() != clean_text(
        payload.get("meta", {}).get("profile_index_before_sha256")
    ):
        raise RuntimeError("FULL 修改了 _索引.md")
    if {
        str(path): file_digest(path) if path.is_file() else {"exists": False}
        for path in FULL_PROTECTED_FILES
    } != payload.get("meta", {}).get("protected_assets_before"):
        raise RuntimeError("FULL 触碰了入口台账三载体或总底表更新报告")
    with FULL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        if len(list(csv.DictReader(handle))) != EXPECTED_SCOPE_COUNT:
            raise RuntimeError("FULL 照片对账 CSV 不是 415 行")


def run_full(run_date: str) -> dict[str, Any]:
    import collect_official_doctors_batch as collector

    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("FULL 前正式照片目录已存在，拒绝覆盖；需 owner 先裁决")
    baseline_protected = {
        str(path): file_digest(path) if path.is_file() else {"exists": False}
        for path in FULL_PROTECTED_FILES
    }
    index_path = PROFILE_DIR / "_索引.md"
    if not index_path.is_file():
        raise RuntimeError("FULL 前本院 _索引.md 缺失")
    index_before_sha256 = hashlib.sha256(index_path.read_bytes()).hexdigest()
    master_payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    before_rows = copy.deepcopy(master_payload.get("rows", []))
    validate_master_layers(MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH)
    scope_rows = load_scope_rows()
    target_sources = {clean_text(row.get("来源链接")) for row in scope_rows}
    if len(scope_rows) != EXPECTED_SCOPE_COUNT or len(target_sources) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 固定范围不是 415 个唯一官网医生详情来源")
    rows_by_source = {clean_text(row.get("来源链接")): row for row in scope_rows}
    before_profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
    before_profile_bytes = preflight_profile_bytes(before_profile_paths, rows_by_source)
    before_profile_tree = profile_markdown_tree(PROFILE_DIR)

    session = OfficialSession()
    home = session.get(OFFICIAL_HOME)
    require_html(home, "官网首页")
    directory = session.get(DIRECTORY_URL, OFFICIAL_HOME)
    require_html(directory, "医生目录")

    with tempfile.TemporaryDirectory(prefix="issue67_full_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_photo_dir = temp_root / "photos"
        temp_photo_dir.mkdir()
        temp_hospital_dir = temp_root / "profiles" / HOSPITAL
        temp_hospital_dir.parent.mkdir(parents=True)
        shutil.copytree(PROFILE_DIR, temp_hospital_dir)

        used_filenames: set[str] = set()
        result_rows: list[dict[str, Any]] = []
        photo_samples: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []
        reconciliation: list[dict[str, Any]] = []

        def record_failure(
            row: dict[str, Any],
            state: str,
            evidence: str,
            attempts: list[dict[str, Any]] | None = None,
        ) -> None:
            source_link = clean_text(row.get("来源链接"))
            name = clean_text(row.get("姓名"))
            result_row = dict(row)
            result_row["照片链接"] = ""
            result_row["照片文件"] = ""
            result_row["异常提示"] = append_failure_warning(
                result_row.get("异常提示"), state
            )
            result_rows.append(result_row)
            failures.append(
                {
                    "name": name,
                    "source_link": source_link,
                    "state": state,
                    "error": evidence,
                    "attempts": attempts or [],
                }
            )
            reconciliation.append(
                {
                    "姓名": name,
                    "来源链接": source_link,
                    "状态": "失败",
                    "失败三态": state,
                    "照片链接": "",
                    "照片文件": "",
                    "字节数": "",
                    "SHA-256": "",
                    "魔数": "",
                    "宽": "",
                    "高": "",
                    "错误证据": evidence,
                }
            )
            if len(failures) / EXPECTED_SCOPE_COUNT > MAX_FAILURE_RATIO:
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 总问题率超过 30%："
                    f"{len(failures)}/{EXPECTED_SCOPE_COUNT}"
                )

        for index, row in enumerate(scope_rows, start=1):
            source_link = clean_text(row.get("来源链接"))
            name = clean_text(row.get("姓名"))
            source_id = detail_id(source_link)
            detail_response, detail_attempts = retryable_get(
                session,
                source_link,
                DIRECTORY_URL,
                lambda response: response.ok
                and clean_text(response.headers.get("content-type"))
                .lower()
                .partition(";")[0]
                in {"text/html", "application/xhtml+xml"},
            )
            if detail_response is None:
                record_failure(
                    row,
                    "详情不可达",
                    "详情请求三次均未取得有效 HTML：" + attempt_evidence_text(detail_attempts),
                    detail_attempts,
                )
                continue
            detail_html = detail_response.text
            failure_state, photo_url, structural_evidence = inspect_full_page_reference(
                detail_html, source_link, name
            )
            if failure_state:
                record_failure(row, failure_state, structural_evidence)
                continue

            photo_response, photo_attempts = retryable_get(
                session,
                photo_url,
                source_link,
                lambda response: response.ok
                and clean_text(response.headers.get("content-type"))
                .lower()
                .partition(";")[0]
                .startswith("image/"),
            )
            if photo_response is None:
                record_failure(
                    row,
                    "详情不可达",
                    "照片资源三次均不可达：" + attempt_evidence_text(photo_attempts),
                    photo_attempts,
                )
                continue
            content = photo_response.content
            if len(content) > FULL_FUSE_BYTES:
                raise RuntimeError(
                    f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 单图超过 20 MiB：{photo_url}"
                )
            extension = magic_extension(content)
            if extension not in SUPPORTED_EXTENSIONS:
                raise RuntimeError(
                    f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 照片魔数格式异常：{photo_url}"
                )
            placeholder = placeholder_reason(photo_url, content, extension)
            if placeholder:
                record_failure(row, "占位图", placeholder)
                continue
            width, height = image_dimensions(content)
            if width <= 0 or height <= 0:
                raise RuntimeError(f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 照片尺寸无效：{photo_url}")
            filename, disk_path = allocate_full_photo_path(
                row, source_id, extension, temp_photo_dir, used_filenames
            )
            disk_path.write_bytes(content)
            relative_path = (PHOTO_RELATIVE_ROOT / filename).as_posix()
            result_row = dict(row)
            result_row["照片链接"] = photo_url
            result_row["照片文件"] = relative_path
            result_rows.append(result_row)
            digest = hashlib.sha256(content).hexdigest()
            sample = {
                "name": name,
                "department": atomic_department(row),
                "title": clean_text(row.get("职称_关键词")),
                "detail_id": source_id,
                "source_link": source_link,
                "detail_attempts": detail_attempts,
                "photo_url": photo_url,
                "photo_attempts": photo_attempts,
                "photo_file": relative_path,
                "filename": filename,
                "content_type": clean_text(photo_response.headers.get("content-type")),
                "bytes": len(content),
                "sha256": digest,
                "magic_hex": content[:12].hex().upper(),
                "width": width,
                "height": height,
                "disk_path": str(FORMAL_PHOTO_DIR / filename),
            }
            photo_samples.append(sample)
            reconciliation.append(
                {
                    "姓名": name,
                    "来源链接": source_link,
                    "状态": "实采",
                    "失败三态": "",
                    "照片链接": photo_url,
                    "照片文件": relative_path,
                    "字节数": len(content),
                    "SHA-256": digest,
                    "魔数": sample["magic_hex"],
                    "宽": width,
                    "高": height,
                    "错误证据": "",
                }
            )
            if index % 25 == 0 or index == EXPECTED_SCOPE_COUNT:
                print(
                    f"[FULL] {index}/{EXPECTED_SCOPE_COUNT} "
                    f"实采={len(photo_samples)} 失败={len(failures)}",
                    flush=True,
                )

        if len(result_rows) != EXPECTED_SCOPE_COUNT:
            raise RuntimeError(f"FULL 结果行不是 415：{len(result_rows)}")
        updated_by_source = {
            clean_text(row.get("来源链接")): row for row in result_rows
        }
        after_rows = [
            copy.deepcopy(updated_by_source.get(clean_text(row.get("来源链接")), row))
            for row in before_rows
        ]
        row_diffs = collect_full_row_diffs(before_rows, after_rows, target_sources)
        updated_payload = copy.deepcopy(master_payload)
        updated_payload["rows"] = after_rows
        if failures:
            recompute_failure_derivatives(updated_payload, after_rows)

        temp_master_payload = temp_root / MASTER_JSON_PATH.name
        temp_master_csv = temp_root / MASTER_CSV_PATH.name
        temp_master_xlsx = temp_root / MASTER_XLSX_PATH.name
        temp_master_preview = temp_root / "master_preview.png"
        temp_master_payload.write_text(
            json.dumps(updated_payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_master_csv(temp_master_csv, after_rows)
        collector.build_workbook(
            temp_master_payload, temp_master_xlsx, temp_master_preview
        )
        validate_master_layers(temp_master_payload, temp_master_csv, temp_master_xlsx)

        success_sources = {
            clean_text(item.get("source_link")) for item in photo_samples
        }
        after_profile_paths = target_profile_paths(temp_hospital_dir, target_sources)
        photo_by_source = {
            clean_text(item.get("source_link")): item for item in photo_samples
        }
        for source in success_sources:
            before_path = before_profile_paths[source]
            after_path = after_profile_paths[source]
            if after_path.name != before_path.name:
                raise RuntimeError(f"FULL 画像文件映射发生变化：{source}")
            item = photo_by_source[source]
            after_path.write_bytes(
                insert_profile_photo_block_bytes(
                    before_profile_bytes[source],
                    clean_text(item.get("name")),
                    clean_text(item.get("photo_file")),
                )
            )
            validate_profile_photo_only_bytes(
                before_profile_bytes[source],
                after_path.read_bytes(),
                clean_text(item.get("name")),
                clean_text(item.get("photo_file")),
            )
        expected_changed_profile_paths = {
            before_profile_paths[source].relative_to(PROFILE_DIR)
            for source in success_sources
        }
        validate_profile_tree_surgical(
            before_profile_tree, temp_hospital_dir, expected_changed_profile_paths
        )

        profile_integrity = []
        for source in sorted(target_sources):
            before_content = before_profile_bytes[source]
            after_content = after_profile_paths[source].read_bytes()
            profile_integrity.append(
                {
                    "source_link": source,
                    "path": before_profile_paths[source]
                    .relative_to(PROFILE_DIR)
                    .as_posix(),
                    "changed": source in success_sources,
                    "before_sha256": hashlib.sha256(before_content).hexdigest(),
                    "after_sha256": hashlib.sha256(after_content).hexdigest(),
                }
            )

        state_counter = Counter(item["state"] for item in failures)
        total_bytes = sum(int(item["bytes"]) for item in photo_samples)
        max_bytes = max((int(item["bytes"]) for item in photo_samples), default=0)
        size_counter = Counter(size_bucket(int(item["bytes"])) for item in photo_samples)
        full_payload = {
            "meta": {
                "issue": ISSUE_NUMBER,
                "phase": "FULL_READY_FOR_FINAL_OWNER_AUDIT",
                "hospital": HOSPITAL,
                "run_date": run_date,
                "authorization": FULL_AUTHORIZATION,
                "scope_count": EXPECTED_SCOPE_COUNT,
                "expected_count": EXPECTED_SCOPE_COUNT,
                "downloaded_count": len(photo_samples),
                "failed_count": len(failures),
                "blank_count": len(failures),
                "failure_ratio": len(failures) / EXPECTED_SCOPE_COUNT,
                "failure_state_counts": {
                    state: state_counter.get(state, 0) for state in FULL_FAILURE_STATES
                },
                "detail_unreachable_count": state_counter.get("详情不可达", 0),
                "no_photo_container_count": state_counter.get("无照片容器", 0),
                "placeholder_count": state_counter.get("占位图", 0),
                "photo_total_bytes": total_bytes,
                "photo_total_mib": total_bytes / 1024 / 1024,
                "photo_max_bytes": max_bytes,
                "size_bucket_counts": dict(size_counter),
                "over_5mib_count": sum(
                    int(item["bytes"]) > OWNER_REPORT_BYTES for item in photo_samples
                ),
                "over_20mib_count": sum(
                    int(item["bytes"]) > FULL_FUSE_BYTES for item in photo_samples
                ),
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "status_flicker_count": 0,
                "existing_profile_count": len(before_profile_paths),
                "no_profile_scope_count": 0,
                "profile_refreshed_count": len(success_sources),
                "profile_not_created_count": 0,
                "profile_index_replacement_required": False,
                "profile_index_before_sha256": index_before_sha256,
                "row_diff_count": len(row_diffs),
                "row_diff_columns": dict(Counter(item["列名"] for item in row_diffs)),
                "protected_assets_before": baseline_protected,
                "json_path": str(FULL_JSON_PATH),
                "csv_path": str(FULL_CSV_PATH),
                "report_path": str(FULL_REPORT_PATH),
            },
            "failures": failures,
            "photo_samples": photo_samples,
            "reconciliation": reconciliation,
            "row_diffs": row_diffs,
            "rows": result_rows,
            "profile_integrity": profile_integrity,
        }
        validate_full_payload(full_payload, temp_photo_dir)

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
        }
        for source in success_sources:
            file_map[before_profile_paths[source]] = after_profile_paths[source]
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
            validate_full_payload(full_payload, FORMAL_PHOTO_DIR)
            final_profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
            for source in success_sources:
                item = photo_by_source[source]
                validate_profile_photo_only_bytes(
                    before_profile_bytes[source],
                    final_profile_paths[source].read_bytes(),
                    clean_text(item.get("name")),
                    clean_text(item.get("photo_file")),
                )
            validate_profile_tree_surgical(
                before_profile_tree, PROFILE_DIR, expected_changed_profile_paths
            )
            if hashlib.sha256(index_path.read_bytes()).hexdigest() != index_before_sha256:
                raise RuntimeError("FULL 修改了 _索引.md")
            current_protected = {
                str(path): file_digest(path) if path.is_file() else {"exists": False}
                for path in FULL_PROTECTED_FILES
            }
            if current_protected != baseline_protected:
                raise RuntimeError("FULL 触碰了入口台账三载体或总底表更新报告")
            validate_full_installation(full_payload)
        except Exception:
            restore_file_targets(backups)
            if photo_swapped and FORMAL_PHOTO_DIR.exists():
                ensure_workspace_target(FORMAL_PHOTO_DIR)
                shutil.rmtree(FORMAL_PHOTO_DIR)
            raise
        return full_payload


def mark_visual_pass() -> dict[str, Any]:
    payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
    validate_payload(payload)
    if len(payload.get("photo_samples", [])) != EXPECTED_TRIAL_COUNT:
        raise RuntimeError("视觉复核标记要求 10 张实图")
    payload["meta"]["visual_review"] = (
        "PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10"
    )
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_report(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 TRIAL/FULL"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trial-only", action="store_true")
    mode.add_argument("--validate", action="store_true")
    mode.add_argument("--mark-visual-pass", action="store_true")
    mode.add_argument(
        "--full",
        action="store_true",
        help="按 PR #68 Owner 授权执行 415 行照片回填与画像照片块最小刷新",
    )
    mode.add_argument(
        "--validate-full",
        action="store_true",
        help="校验已落盘 FULL payload、三载体、受保护资产、照片与画像完整性",
    )
    parser.add_argument("--today", default=date.today().isoformat())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.full:
        payload = run_full(args.today)
    elif args.validate_full:
        if not FULL_JSON_PATH.is_file():
            raise RuntimeError("FULL payload 不存在")
        payload = json.loads(FULL_JSON_PATH.read_text(encoding="utf-8"))
        validate_full_installation(payload)
    elif args.trial_only:
        payload = run_trial(args.today)
    else:
        if not TRIAL_JSON_PATH.is_file():
            raise RuntimeError("TRIAL payload 不存在")
        if args.mark_visual_pass:
            payload = mark_visual_pass()
        else:
            payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
            validate_payload(payload)
    if payload.get("meta", {}).get("phase") == "FULL_READY_FOR_FINAL_OWNER_AUDIT":
        meta = payload["meta"]
        print(
            json.dumps(
                {
                    "mode": "photo_backfill_full",
                    "phase": meta["phase"],
                    "hospital": meta["hospital"],
                    "scope": meta["expected_count"],
                    "downloaded": meta["downloaded_count"],
                    "failed": meta["failed_count"],
                    "blank": meta["blank_count"],
                    "failure_states": meta["failure_state_counts"],
                    "photo_total_bytes": meta["photo_total_bytes"],
                    "size_bucket_counts": meta["size_bucket_counts"],
                    "profiles_refreshed": meta["profile_refreshed_count"],
                    "json": str(FULL_JSON_PATH),
                    "csv": str(FULL_CSV_PATH),
                    "report": str(FULL_REPORT_PATH),
                    "master_updated": True,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    print(
        json.dumps(
            {
                "phase": payload["meta"]["phase"],
                "downloaded_count": payload["meta"]["downloaded_count"],
                "problem_count": payload["meta"]["problem_count"],
                "visual_review": payload["meta"].get("visual_review"),
                "payload": str(TRIAL_JSON_PATH),
                "manifest": str(TRIAL_CSV_PATH),
                "report": str(TRIAL_REPORT_PATH),
                "contact_sheet": str(CONTACT_SHEET_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
