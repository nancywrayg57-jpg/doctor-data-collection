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
from collections import Counter
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from http.client import IncompleteRead
from http.cookiejar import CookieJar
from pathlib import Path
from statistics import median
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, unquote, urljoin, urlparse
from urllib.request import HTTPCookieProcessor, Request, build_opener

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "中山大学附属第五医院"
ISSUE_NUMBER = 61
MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_JSON_PATH = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_REPORT_PATH = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
LEDGER_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"
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
OFFICIAL_HOME = "https://www.sysu5.cn/"
DIRECTORY_URL = (
    "https://www.sysu5.cn/medical-service/department-expert/doctor/"
    "category?category_target_id=All&combine="
)
OFFICIAL_HOST = "sysu5.cn"
PHOTO_PREFIX = "/sites/default/files/styles/watermark/public/"
EXPECTED_SCOPE_COUNT = 413
EXPECTED_TRIAL_COUNT = 10
MIN_TRIAL_DEPARTMENTS = 8
MAX_FAILURE_RATIO = 0.30
LARGE_BYTES = 200 * 1024
MAX_OWNER_REPORT_BYTES = 5 * 1024 * 1024
MAX_FULL_IMAGE_BYTES = 20 * 1024 * 1024
SUPPORTED_PHOTO_EXTENSIONS = frozenset({"jpg", "png", "gif", "webp"})
EXPECTED_PROFILE_COUNT = 413
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
    "PR #62 owner comments 2026-08-17T03:49:07Z and 2026-08-17T04:27:48Z: "
    "TRIAL 通过 + FULL_APPEND_AND_OBSIDIAN + 方案 A + 5-20 MiB 原始字节授权"
)
SMALL_GIF_PLACEHOLDER_BYTES = 40 * 1024
SMALL_GIF_PLACEHOLDER_MARKERS = (
    "nopic",
    "no_pic",
    "no-photo",
    "noimage",
    "no-image",
    "placeholder",
)
PAGE_PLACEHOLDER_MARKERS = SMALL_GIF_PLACEHOLDER_MARKERS + ("default", "avatar")
SAMPLE_PLAN = (
    ("丁立", "正高", "10285"),
    ("王莉", "正高", "9108"),
    ("何欢欢", "正高", "10860"),
    ("韩宗萍", "副高", "10837"),
    ("孙一", "副高", "12229"),
    ("林子玲", "副高", "10767"),
    ("张玉龙", "其他", "10710"),
    ("徐晓露", "其他", "14096"),
    ("余圆圆", "其他", "10904"),
    ("刘天民", "其他", "2241"),
)
PRIMARY_TITLES = (
    "一级主任医师",
    "副主任中医师",
    "副主任医师",
    "主任中医师",
    "主任医师",
    "副主任技师",
    "主任技师",
    "副主任药师",
    "主任药师",
    "副主任护师",
    "主任护师",
    "主治中医师",
    "主治医师",
    "主管技师",
    "主管药师",
    "主管护师",
    "住院医师",
    "助理研究员",
    "副研究员",
    "研究员",
    "副教授",
    "教授",
    "医师",
)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36; "
    "public official-site photo backfill trial"
)


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def comparable_host(value: str) -> str:
    host = (urlparse(value).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def detail_id(value: Any) -> str:
    text = clean_text(value)
    parsed = urlparse(text)
    if (
        parsed.scheme not in {"http", "https"}
        or comparable_host(text) != OFFICIAL_HOST
        or parsed.query
        or parsed.fragment
    ):
        return ""
    match = re.fullmatch(r"/medical-service/department-expert/doctor/(\d+)", parsed.path)
    return match.group(1) if match else ""


def safe_photo_part(value: Any) -> str:
    text = re.sub(r'[\\/:*?"<>|]', "_", clean_text(value)).strip(" .")
    return text or "未标注"


def atomic_department(row: dict[str, Any]) -> str:
    value = clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
    atoms = [clean_text(item) for item in re.split(r"[、,，;/；|]+", value) if clean_text(item)]
    chinese_atoms = [item for item in atoms if re.search(r"[\u4e00-\u9fff]", item)]
    return safe_photo_part(chinese_atoms[0] if chinese_atoms else (atoms[0] if atoms else "未标注"))


def primary_title(value: Any) -> str:
    text = clean_text(value)
    for title in PRIMARY_TITLES:
        if title in text:
            return title
    return "未标注"


def title_level(value: Any) -> str:
    title = primary_title(value)
    if title in {
        "一级主任医师",
        "主任医师",
        "主任中医师",
        "主任技师",
        "主任药师",
        "主任护师",
        "研究员",
        "教授",
    }:
        return "正高"
    if title in {
        "副主任医师",
        "副主任中医师",
        "副主任技师",
        "副主任药师",
        "副主任护师",
        "副研究员",
        "副教授",
    }:
        return "副高"
    return "其他"


def page_referenced_photo_url(value: Any, base_url: str) -> str:
    raw = clean_text(value)
    if not raw:
        return ""
    absolute = urljoin(base_url, raw)
    parsed = urlparse(absolute)
    if (
        parsed.scheme not in {"http", "https"}
        or comparable_host(absolute) != OFFICIAL_HOST
        or parsed.fragment
        or not parsed.path.startswith(PHOTO_PREFIX)
    ):
        return ""
    query = parse_qsl(parsed.query, keep_blank_values=True)
    if len(query) != 1 or query[0][0] != "itok" or not query[0][1]:
        return ""
    return absolute


class PhysicianPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._div_stack: list[bool] = []
        self._in_title = False
        self._title_parts: list[str] = []
        self.body_classes: set[str] = set()
        self.featured_images: list[dict[str, str]] = []

    @property
    def title(self) -> str:
        return clean_text(" ".join(self._title_parts))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {name.lower(): str(value or "") for name, value in attrs}
        lowered = tag.lower()
        if lowered == "title":
            self._in_title = True
            return
        classes = set(clean_text(attrs_dict.get("class")).split())
        if lowered == "body":
            self.body_classes = classes
        if lowered == "div":
            parent_featured = self._div_stack[-1] if self._div_stack else False
            is_featured = {
                "field",
                "field-featured-media",
                "field-item",
            }.issubset(classes)
            self._div_stack.append(parent_featured or is_featured)
            return
        if lowered == "img" and self._div_stack and self._div_stack[-1]:
            self.featured_images.append(attrs_dict)

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        if lowered == "title":
            self._in_title = False
        elif lowered == "div" and self._div_stack:
            self._div_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)


@dataclass(frozen=True)
class PortraitReference:
    page_title: str
    photo_url: str
    source_attribute: str
    template_signature: str
    reference_kind: str
    derivative_style: str


def inspect_portrait_reference(
    html: str, source_link: str, expected_name: str
) -> tuple[str, PortraitReference | None]:
    if not detail_id(source_link):
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    parser = PhysicianPageParser()
    parser.feed(html)
    expected_title = f"{clean_text(expected_name)} | {HOSPITAL}"
    if parser.title != expected_title:
        raise RuntimeError(
            f"详情标题与底表不一致：底表={expected_name} 官网={parser.title or '空'} {source_link}"
        )
    if "page-node-type-doctor" not in parser.body_classes:
        raise RuntimeError(f"详情 body 模板不是 doctor：{source_link} {sorted(parser.body_classes)}")
    if not parser.featured_images:
        return "无照片容器", None
    if len(parser.featured_images) != 1:
        raise RuntimeError(
            f"医生 field-featured-media 内 img 不唯一：{source_link} 数量={len(parser.featured_images)}"
        )
    attrs = parser.featured_images[0]
    candidates: list[tuple[str, str]] = []
    for attribute in ("src", "data-src", "data-original", "data-lazy-src"):
        value = clean_text(attrs.get(attribute))
        if value:
            candidates.append((attribute, value))
    if not candidates and clean_text(attrs.get("srcset")):
        first = clean_text(attrs["srcset"]).split(",", 1)[0].split()[0]
        candidates.append(("srcset", first))
    if not candidates:
        return "无照片容器", None
    normalized = [page_referenced_photo_url(value, source_link) for _, value in candidates]
    valid = [(attribute, url) for (attribute, _), url in zip(candidates, normalized) if url]
    if not valid:
        raw_paths = " ".join(
            unquote(urlparse(urljoin(source_link, value)).path).lower() for _, value in candidates
        )
        if any(marker in raw_paths for marker in PAGE_PLACEHOLDER_MARKERS):
            return "占位图", None
        raise RuntimeError(f"页面引用照片 URL 越界：{source_link} {candidates}")
    unique = {url for _, url in valid}
    if len(unique) != 1:
        raise RuntimeError(f"医生照片容器多属性 URL 不一致：{source_link}")
    return "", PortraitReference(
        page_title=parser.title,
        photo_url=next(iter(unique)),
        source_attribute=valid[0][0],
        template_signature="body.page-node-type-doctor .field.field-featured-media.field-item img",
        reference_kind="派生图",
        derivative_style="watermark",
    )


class OfficialSession:
    def __init__(self) -> None:
        self.cookie_jar = CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.cookie_jar))
        self.incomplete_read_retry_count = 0

    @property
    def cookie_names(self) -> list[str]:
        return sorted(cookie.name for cookie in self.cookie_jar)

    def get(self, url: str, referer: str = "") -> tuple[int, str, str, bytes]:
        headers = {"User-Agent": USER_AGENT}
        if referer:
            headers["Referer"] = referer
        request = Request(url, headers=headers)
        for attempt in range(2):
            try:
                with self.opener.open(request, timeout=35) as response:
                    return (
                        int(response.status),
                        response.headers.get_content_type(),
                        response.headers.get_content_charset() or "utf-8",
                        response.read(),
                    )
            except IncompleteRead as exc:
                if attempt == 0:
                    self.incomplete_read_retry_count += 1
                    continue
                raise RuntimeError(
                    f"官网响应连续两次传输不完整：{url} 已读 {len(exc.partial)} bytes，缺少 {exc.expected} bytes"
                ) from exc
            except HTTPError as exc:
                return (
                    int(exc.code),
                    exc.headers.get_content_type(),
                    exc.headers.get_content_charset() or "utf-8",
                    exc.read(),
                )
            except URLError as exc:
                raise RuntimeError(f"官网请求失败：{url} {exc}") from exc
        raise AssertionError("官网请求重试循环未返回")


def magic_extension(content: bytes, content_type: str | None) -> str:
    media_type = clean_text(content_type).split(";", 1)[0].lower()
    if not media_type.startswith("image/"):
        return ""
    if content.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if content.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if len(content) >= 12 and content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return "webp"
    return ""


def enforce_full_photo_policy(
    name: str, photo_url: str, extension: str, byte_count: int
) -> None:
    if extension not in SUPPORTED_PHOTO_EXTENSIONS:
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 照片格式不受支持，"
            f"仅允许 jpg/png/gif/webp：{name} {photo_url}"
        )
    if byte_count > MAX_FULL_IMAGE_BYTES:
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 单张照片超过 20 MiB："
            f"{name} {byte_count} bytes {photo_url}"
        )


def downloaded_placeholder_reason(photo_url: str, content: bytes, extension: str) -> str:
    if extension != "gif" or len(content) >= SMALL_GIF_PLACEHOLDER_BYTES:
        return ""
    path = unquote(urlparse(photo_url).path).lower()
    marker_hit = any(marker in path for marker in SMALL_GIF_PLACEHOLDER_MARKERS)
    try:
        with Image.open(io.BytesIO(content)) as image:
            image.load()
            rgb = image.convert("RGB")
            colors = rgb.getcolors(maxcolors=65)
            pixels = list(rgb.get_flattened_data())
    except Exception as exc:
        raise RuntimeError(f"小 GIF 占位图视觉判定失败：{photo_url} {exc}") from exc
    neutral_light = sum(
        max(pixel) >= 210 and max(pixel) - min(pixel) <= 24 for pixel in pixels
    )
    gray_ratio = neutral_light / len(pixels) if pixels else 0.0
    gray_placeholder = colors is not None and gray_ratio >= 0.70
    if marker_hit or gray_placeholder:
        return (
            "照片为占位图（暂无图片），留空；"
            f"GIF {len(content)} bytes，灰底占比 {gray_ratio:.2%}，路径 {path}"
        )
    return ""


def image_dimensions(content: bytes) -> tuple[int, int]:
    with Image.open(io.BytesIO(content)) as image:
        image.verify()
    with Image.open(io.BytesIO(content)) as image:
        image.load()
        return int(image.width), int(image.height)


def file_snapshot(paths: list[Path]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in paths:
        if not path.is_file():
            raise RuntimeError(f"受保护资产缺失：{path}")
        content = path.read_bytes()
        result[str(path)] = {
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
    return result


def tree_snapshot(root: Path, suffix: str = "") -> dict[str, Any]:
    if not root.exists():
        return {"exists": False, "file_count": 0, "bytes": 0, "sha256": ""}
    files = sorted(
        path for path in root.rglob("*") if path.is_file() and (not suffix or path.suffix == suffix)
    )
    digest = hashlib.sha256()
    total_bytes = 0
    for path in files:
        content = path.read_bytes()
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(hashlib.sha256(content).digest())
        total_bytes += len(content)
    return {
        "exists": True,
        "file_count": len(files),
        "bytes": total_bytes,
        "sha256": digest.hexdigest(),
    }


def protected_snapshot() -> dict[str, Any]:
    return {
        "formal_files": file_snapshot(
            [LEDGER_PATH, MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH, MASTER_REPORT_PATH]
        ),
        "profile_markdown_tree": tree_snapshot(PROFILE_DIR, ".md"),
        "formal_photo_tree": tree_snapshot(FORMAL_PHOTO_DIR),
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
    if any(clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")) for row in rows):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} TRIAL 范围内已有照片字段，需 owner 先裁决")
    sources = [clean_text(row.get("来源链接")) for row in rows]
    if len(sources) != len(set(sources)):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} 范围来源链接不唯一")
    invalid_sources = [source for source in sources if not detail_id(source)]
    if invalid_sources:
        raise RuntimeError("范围存在非授权官网详情来源：" + "、".join(invalid_sources[:5]))
    return rows


def select_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for expected_name, expected_level, expected_id in SAMPLE_PLAN:
        matches = [row for row in rows if clean_text(row.get("姓名")) == expected_name]
        if len(matches) != 1:
            raise RuntimeError(f"试采姓名范围不唯一：{expected_name} 数量={len(matches)}")
        row = dict(matches[0])
        if detail_id(row.get("来源链接")) != expected_id:
            raise RuntimeError(f"试采详情 ID 漂移：{expected_name}")
        actual_level = title_level(row.get("职称身份原文"))
        if actual_level != expected_level:
            raise RuntimeError(
                f"试采职称层级漂移：{expected_name} 应为 {expected_level} 实际 {actual_level}"
            )
        result.append(row)
    if len({atomic_department(row) for row in result}) < MIN_TRIAL_DEPARTMENTS:
        raise RuntimeError("试采科室覆盖不足")
    if {title_level(row.get("职称身份原文")) for row in result} != {"正高", "副高", "其他"}:
        raise RuntimeError("试采职称分层覆盖漂移")
    return result


def allocate_trial_photo(
    row: dict[str, Any], extension: str, content: bytes
) -> tuple[str, Path]:
    stem = "-".join(
        [
            safe_photo_part(row.get("姓名")),
            atomic_department(row),
            safe_photo_part(primary_title(row.get("职称身份原文"))),
            safe_photo_part(HOSPITAL),
        ]
    )
    filename = f"{stem}.{extension}"
    path = TRIAL_PHOTO_DIR / filename
    if path.exists() and path.read_bytes() != content:
        filename = f"{stem}-{detail_id(row.get('来源链接'))}.{extension}"
        path = TRIAL_PHOTO_DIR / filename
    if path.exists() and path.read_bytes() != content:
        raise RuntimeError(f"TRIAL 照片已存在且字节不同，拒绝覆盖：{path}")
    return filename, path


def contact_sheet_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
    ):
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def build_contact_sheet(samples: list[dict[str, Any]]) -> None:
    if not samples:
        raise RuntimeError("没有可生成联系表的 TRIAL 实图")
    columns = 2
    cell_width = 500
    cell_height = 520
    row_count = (len(samples) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_width, row_count * cell_height), "white")
    draw = ImageDraw.Draw(canvas)
    font = contact_sheet_font(20)
    small_font = contact_sheet_font(17)
    for index, sample in enumerate(samples):
        left = (index % columns) * cell_width
        top = (index // columns) * cell_height
        with Image.open(sample["disk_path"]) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            thumb = ImageOps.contain(image, (440, 390))
        image_left = left + (cell_width - thumb.width) // 2
        image_top = top + 10 + (390 - thumb.height) // 2
        canvas.paste(thumb, (image_left, image_top))
        draw.rectangle(
            (left, top, left + cell_width - 1, top + cell_height - 1),
            outline="#B7C0C8",
            width=2,
        )
        draw.text(
            (left + 20, top + 410),
            f"{index + 1}. {sample['name']}｜{sample['title']}",
            fill="black",
            font=font,
        )
        draw.text((left + 20, top + 448), sample["department"], fill="#333333", font=small_font)
        draw.text(
            (left + 20, top + 482),
            f"{sample['width']}×{sample['height']}｜{sample['bytes']} bytes",
            fill="#555555",
            font=small_font,
        )
    canvas.save(CONTACT_SHEET_PATH, format="JPEG", quality=90, optimize=True)


def write_manifest(rows: list[dict[str, Any]]) -> None:
    fields = [
        "姓名",
        "科室",
        "职称层级",
        "主职称",
        "来源链接",
        "页面模板",
        "详情HTTP",
        "照片引用属性",
        "引用类型",
        "派生样式",
        "照片链接",
        "照片HTTP",
        "文件名",
        "字节",
        "SHA-256",
        "魔数",
        "宽",
        "高",
        "大小分布",
        "大图判定",
    ]
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def size_bucket(size: int) -> str:
    if size < LARGE_BYTES:
        return "<200KiB"
    if size < 1024 * 1024:
        return "200KiB-1MiB"
    if size <= MAX_OWNER_REPORT_BYTES:
        return "1-5MiB"
    return ">5MiB"


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|").replace("\n", " ")


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    sample_rows = []
    for sample in payload["photo_samples"]:
        sample_rows.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(sample["name"]),
                    markdown_cell(sample["department"]),
                    markdown_cell(sample["title_level"]),
                    markdown_cell(sample["title"]),
                    markdown_cell(sample["filename"]),
                    str(sample["bytes"]),
                    f"{sample['width']}×{sample['height']}",
                    markdown_cell(sample["sha256"]),
                    markdown_cell(sample["photo_url"]),
                ]
            )
            + " |"
        )
    protected_rows = []
    for path, item in meta["protected_assets_before"]["formal_files"].items():
        protected_rows.append(f"| `{path}` | {item['bytes']} | `{item['sha256']}` |")
    report = f"""# Issue #61 中山大学附属第五医院照片补录 TRIAL 报告

## 执行结论

- 阶段：`{meta['phase']}`；范围：{meta['scope_count']} 行 / {meta['scope_unique_source_count']} 个唯一官网详情 URL。
- 固定分层样本：{meta['trial_detail_count']} 人，覆盖 {meta['department_coverage_count']} 个科室，职称层级 `{json.dumps(meta['title_level_counts'], ensure_ascii=False)}`。
- 实采：{meta['photo_sample_count']}；熔断问题：{meta['fuse_problem_count']}/{meta['trial_detail_count']}（{meta['fuse_problem_ratio']:.2%}）。
- 仅请求详情页 `field-featured-media` 容器自身引用的 `styles/watermark` 派生图，逐字保留 `itok`；图片请求携带对应详情页 Referer；未构造或探测页面未引用原图路径。
- 未使用第三方来源，未绕过登录、验证码、反爬或权限限制。

## 大小分布

| 指标 | 结果 |
|---|---:|
| 总字节 | {meta['photo_total_bytes']} |
| 最小 | {meta['photo_min_bytes']} |
| 中位数 | {meta['photo_median_bytes']} |
| 平均 | {meta['photo_average_bytes']} |
| 最大 | {meta['photo_max_bytes']} |
| 超过 200 KiB | {meta['over_200kb_count']} |
| 超过 5 MiB | {meta['over_5mib_count']} |
| 413 行估算 | {meta['estimated_full_mib']:.2f} MiB |

分桶：`{json.dumps(meta['size_bucket_counts'], ensure_ascii=False)}`。

## 逐图三重核验与尺寸

| 姓名 | 科室 | 层级 | 主职称 | 文件名 | 字节 | 尺寸 | SHA-256 | 页面引用照片 |
|---|---|---|---|---|---:|---:|---|---|
{chr(10).join(sample_rows)}

详细 HTTP、引用属性、魔数和逐图命名清单见：`{TRIAL_CSV_PATH}` 与 `{TRIAL_JSON_PATH}`。

## 占位图检测

- 复用 Issue #59 口径：仅对小于 40 KiB 的 GIF 执行 `nopic/noimage/placeholder` 路径标记或低色板且浅灰中性像素占比至少 70% 判定；彩色小 GIF 不因体积小而误判。
- 页面级路径标记只作用于唯一照片容器引用；公共页头、招聘图、二维码和页脚图不属于候选容器。

## 联系表人工核验

- 联系表：`{CONTACT_SHEET_PATH}`。
- 当前状态：`{meta['visual_review_status']}`。
- 判定目标：10 张均应为对应医生的单人职业照，不得出现占位图、公共装饰图、二维码、患者、儿童或合影。

## 受保护正式资产零变更

| 文件 | 字节 | SHA-256 |
|---|---:|---|
{chr(10).join(protected_rows)}

- 本院画像 Markdown 树：{meta['protected_assets_before']['profile_markdown_tree']['file_count']} 个文件，SHA-256 `{meta['protected_assets_before']['profile_markdown_tree']['sha256']}`。
- 本院正式照片目录执行前后状态一致：`{json.dumps(meta['protected_assets_before']['formal_photo_tree'], ensure_ascii=False)}`。
- TRIAL 只写入 `work` 独立工件，未写总底表、正式照片目录、画像或索引。

## 裁决依据缺口

Issue 正文引用的 `docs/中山五院照片嵌入方式裁决单.md` 在本次基线不存在。Issue 正文已完整给出方案 A，但 TRIAL 不执行画像写入，因此不影响本阶段；进入 FULL 前仍应由 owner 确保该裁决依据可追溯。

## 当前停止点

TRIAL 工件完成后停止，等待 owner 审计实图、大小分布、来源边界及缺失裁决单风险。未取得当前关联 PR 中 owner 明确 `通过` / `有条件通过` 且切换为 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填总底表、写正式照片目录或修改画像。
"""
    TRIAL_REPORT_PATH.write_text(report, encoding="utf-8")


def validate_payload(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    errors: list[str] = []
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围不是 413 行")
    if meta.get("scope_unique_source_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围官网详情 URL 不唯一")
    if meta.get("trial_detail_count") != EXPECTED_TRIAL_COUNT:
        errors.append("详情样本不是 10 位")
    if meta.get("department_coverage_count", 0) < MIN_TRIAL_DEPARTMENTS:
        errors.append("科室覆盖不足")
    if set(meta.get("title_level_counts", {})) != {"正高", "副高", "其他"}:
        errors.append("职称分层不完整")
    if float(meta.get("fuse_problem_ratio", 1)) > MAX_FAILURE_RATIO:
        errors.append("熔断问题占比超过 30%")
    if meta.get("constructed_unreferenced_probe_count") != 0:
        errors.append("发生页面未引用路径探测")
    if meta.get("third_party_source_count") != 0:
        errors.append("发生第三方来源访问")
    if meta.get("protected_assets_before") != meta.get("protected_assets_after"):
        errors.append("正式受保护资产发生变化")
    filenames: set[str] = set()
    hashes: set[str] = set()
    for sample in payload.get("photo_samples", []):
        path = Path(sample["disk_path"])
        if not path.is_file():
            errors.append(f"照片不存在：{path}")
            continue
        content = path.read_bytes()
        if len(content) != sample.get("bytes"):
            errors.append(f"照片字节不一致：{path.name}")
        if hashlib.sha256(content).hexdigest() != sample.get("sha256"):
            errors.append(f"照片 SHA-256 不一致：{path.name}")
        extension = magic_extension(content, sample.get("content_type"))
        if extension != path.suffix.lower().lstrip("."):
            errors.append(f"照片魔数与扩展名不一致：{path.name}")
        if image_dimensions(content) != (sample.get("width"), sample.get("height")):
            errors.append(f"照片尺寸不一致：{path.name}")
        if downloaded_placeholder_reason(sample["photo_url"], content, extension):
            errors.append(f"照片命中占位图：{path.name}")
        if not page_referenced_photo_url(sample.get("photo_url"), sample.get("source_link")):
            errors.append(f"照片 URL 越界：{path.name}")
        filenames.add(path.name.casefold())
        hashes.add(str(sample.get("sha256")))
    if len(filenames) != meta.get("photo_sample_count"):
        errors.append("照片文件名覆盖或数量不一致")
    if len(hashes) != meta.get("photo_sample_count"):
        errors.append("样本照片 SHA-256 重复，疑似占位图")
    problem_count = sum(
        len(payload.get(key, []))
        for key in ("detail_errors", "structure_mismatches", "failure_states", "photo_errors")
    )
    if len(payload.get("photo_samples", [])) + problem_count != EXPECTED_TRIAL_COUNT:
        errors.append("10 位样本未形成互斥闭环")
    if TRIAL_PHOTO_DIR.is_dir():
        actual_files = {path.name.casefold() for path in TRIAL_PHOTO_DIR.iterdir() if path.is_file()}
        if actual_files != filenames:
            errors.append("TRIAL 照片目录含缺失或多余文件")
    if not CONTACT_SHEET_PATH.is_file():
        errors.append("联系表不存在")
    if errors:
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} TRIAL 门禁失败：" + "；".join(errors))


def run_trial(run_date: str) -> dict[str, Any]:
    protected_before = protected_snapshot()
    scope_rows = load_scope_rows()
    trial_rows = select_trial_rows(scope_rows)
    session = OfficialSession()
    home_status, _, _, _ = session.get(OFFICIAL_HOME)
    if home_status != 200:
        raise RuntimeError(f"官网首页常规会话建立失败：HTTP {home_status}")
    directory_status, directory_type, _, _ = session.get(DIRECTORY_URL, OFFICIAL_HOME)
    if directory_status != 200 or directory_type != "text/html":
        raise RuntimeError(
            f"医生目录常规会话访问失败：HTTP {directory_status} {directory_type}"
        )

    detail_errors: list[dict[str, Any]] = []
    structure_mismatches: list[dict[str, Any]] = []
    failure_states: list[dict[str, Any]] = []
    portrait_rows: list[tuple[dict[str, Any], PortraitReference, int]] = []
    for row in trial_rows:
        source_link = clean_text(row.get("来源链接"))
        status, content_type, charset, content = session.get(source_link, DIRECTORY_URL)
        if status != 200 or content_type != "text/html":
            detail_errors.append(
                {
                    "name": clean_text(row.get("姓名")),
                    "source_link": source_link,
                    "status": status,
                    "content_type": content_type,
                }
            )
            continue
        html = content.decode(charset, errors="replace")
        try:
            failure_state, portrait = inspect_portrait_reference(
                html, source_link, clean_text(row.get("姓名"))
            )
        except RuntimeError as exc:
            structure_mismatches.append(
                {
                    "name": clean_text(row.get("姓名")),
                    "source_link": source_link,
                    "error": str(exc),
                }
            )
            continue
        if failure_state or portrait is None:
            failure_states.append(
                {
                    "name": clean_text(row.get("姓名")),
                    "source_link": source_link,
                    "state": failure_state or "未知",
                }
            )
            continue
        portrait_rows.append((row, portrait, status))

    TRIAL_PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    photo_errors: list[dict[str, Any]] = []
    photo_samples: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    for row, portrait, detail_status in portrait_rows:
        source_link = clean_text(row.get("来源链接"))
        photo_status, content_type, _, content = session.get(portrait.photo_url, source_link)
        if photo_status != 200:
            photo_errors.append(
                {
                    "name": clean_text(row.get("姓名")),
                    "source_link": source_link,
                    "photo_url": portrait.photo_url,
                    "status": photo_status,
                }
            )
            continue
        extension = magic_extension(content, content_type)
        if not extension:
            photo_errors.append(
                {
                    "name": clean_text(row.get("姓名")),
                    "source_link": source_link,
                    "photo_url": portrait.photo_url,
                    "error": f"非受支持图片：{content_type}",
                }
            )
            continue
        placeholder_reason = downloaded_placeholder_reason(
            portrait.photo_url, content, extension
        )
        if placeholder_reason:
            failure_states.append(
                {
                    "name": clean_text(row.get("姓名")),
                    "source_link": source_link,
                    "state": "占位图",
                    "error": placeholder_reason,
                }
            )
            continue
        try:
            width, height = image_dimensions(content)
            filename, path = allocate_trial_photo(row, extension, content)
            if not path.exists():
                path.write_bytes(content)
        except Exception as exc:  # noqa: BLE001 - retain exact per-image evidence
            photo_errors.append(
                {
                    "name": clean_text(row.get("姓名")),
                    "source_link": source_link,
                    "photo_url": portrait.photo_url,
                    "error": str(exc),
                }
            )
            continue
        digest = hashlib.sha256(content).hexdigest()
        large_reasons = []
        if len(content) > LARGE_BYTES:
            large_reasons.append(">200KiB")
        if len(content) > MAX_OWNER_REPORT_BYTES:
            large_reasons.append(">5MiB")
        sample = {
            "name": clean_text(row.get("姓名")),
            "department": atomic_department(row),
            "title_level": title_level(row.get("职称身份原文")),
            "title": primary_title(row.get("职称身份原文")),
            "detail_id": detail_id(source_link),
            "source_link": source_link,
            "detail_http_status": detail_status,
            "page_title": portrait.page_title,
            "template_signature": portrait.template_signature,
            "photo_url": portrait.photo_url,
            "photo_source_attribute": portrait.source_attribute,
            "reference_kind": portrait.reference_kind,
            "derivative_style": portrait.derivative_style,
            "photo_http_status": photo_status,
            "content_type": content_type,
            "filename": filename,
            "disk_path": str(path),
            "bytes": len(content),
            "sha256": digest,
            "magic_hex": content[:12].hex().upper(),
            "width": width,
            "height": height,
            "size_bucket": size_bucket(len(content)),
            "large_reasons": large_reasons,
        }
        photo_samples.append(sample)
        manifest_rows.append(
            {
                "姓名": sample["name"],
                "科室": sample["department"],
                "职称层级": sample["title_level"],
                "主职称": sample["title"],
                "来源链接": source_link,
                "页面模板": portrait.template_signature,
                "详情HTTP": detail_status,
                "照片引用属性": portrait.source_attribute,
                "引用类型": portrait.reference_kind,
                "派生样式": portrait.derivative_style,
                "照片链接": portrait.photo_url,
                "照片HTTP": photo_status,
                "文件名": filename,
                "字节": len(content),
                "SHA-256": digest,
                "魔数": sample["magic_hex"],
                "宽": width,
                "高": height,
                "大小分布": sample["size_bucket"],
                "大图判定": "、".join(large_reasons) or "未命中",
            }
        )

    build_contact_sheet(photo_samples)
    protected_after = protected_snapshot()
    fuse_problem_count = sum(
        len(items)
        for items in (detail_errors, structure_mismatches, failure_states, photo_errors)
    )
    fuse_ratio = fuse_problem_count / EXPECTED_TRIAL_COUNT
    if fuse_ratio > MAX_FAILURE_RATIO:
        raise RuntimeError(
            f"[FATAL - HUMAN_INTERVENTION_REQUIRED] TRIAL 熔断问题超过 30%：{fuse_problem_count}/{EXPECTED_TRIAL_COUNT}"
        )
    sizes = [sample["bytes"] for sample in photo_samples]
    total_bytes = sum(sizes)
    average_bytes = total_bytes // max(1, len(sizes))
    title_counts = Counter(title_level(row.get("职称身份原文")) for row in trial_rows)
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "phase": "TRIAL_READY_FOR_OWNER_AUDIT",
            "hospital": HOSPITAL,
            "run_date": run_date,
            "scope_count": len(scope_rows),
            "scope_unique_source_count": len(
                {clean_text(row.get("来源链接")) for row in scope_rows}
            ),
            "scope_blank_photo_row_count": sum(
                not clean_text(row.get("照片链接")) and not clean_text(row.get("照片文件"))
                for row in scope_rows
            ),
            "trial_detail_count": len(trial_rows),
            "department_coverage_count": len({atomic_department(row) for row in trial_rows}),
            "covered_departments": sorted({atomic_department(row) for row in trial_rows}),
            "title_level_counts": {
                level: title_counts[level] for level in ("正高", "副高", "其他")
            },
            "home_http_status": home_status,
            "directory_http_status": directory_status,
            "cookie_names": session.cookie_names,
            "incomplete_read_retry_count": session.incomplete_read_retry_count,
            "detail_http_200_count": len(portrait_rows) + len(failure_states),
            "no_photo_container_count": sum(
                item["state"] == "无照片容器" for item in failure_states
            ),
            "placeholder_count": sum(item["state"] == "占位图" for item in failure_states),
            "structure_mismatch_count": len(structure_mismatches),
            "detail_error_count": len(detail_errors),
            "photo_error_count": len(photo_errors),
            "photo_sample_count": len(photo_samples),
            "fuse_problem_count": fuse_problem_count,
            "fuse_problem_ratio": fuse_ratio,
            "photo_total_bytes": total_bytes,
            "photo_min_bytes": min(sizes, default=0),
            "photo_median_bytes": int(median(sizes)) if sizes else 0,
            "photo_average_bytes": average_bytes,
            "photo_max_bytes": max(sizes, default=0),
            "size_bucket_counts": dict(Counter(size_bucket(size) for size in sizes)),
            "over_200kb_count": sum(size > LARGE_BYTES for size in sizes),
            "over_5mib_count": sum(size > MAX_OWNER_REPORT_BYTES for size in sizes),
            "estimated_full_count": EXPECTED_SCOPE_COUNT,
            "estimated_full_bytes": average_bytes * EXPECTED_SCOPE_COUNT,
            "estimated_full_mib": average_bytes * EXPECTED_SCOPE_COUNT / 1024 / 1024,
            "derivative_reference_count": sum(
                sample["reference_kind"] == "派生图" for sample in photo_samples
            ),
            "derivative_style_counts": dict(
                Counter(sample["derivative_style"] for sample in photo_samples)
            ),
            "constructed_unreferenced_probe_count": 0,
            "third_party_source_count": 0,
            "visual_review_status": "PENDING_MANUAL_CONTACT_SHEET_REVIEW",
            "missing_embedding_ruling_doc": str(ROOT / "docs" / "中山五院照片嵌入方式裁决单.md"),
            "missing_embedding_ruling_doc_exists": (
                ROOT / "docs" / "中山五院照片嵌入方式裁决单.md"
            ).is_file(),
            "protected_assets_before": protected_before,
            "protected_assets_after": protected_after,
            "trial_photo_dir": str(TRIAL_PHOTO_DIR),
            "json_path": str(TRIAL_JSON_PATH),
            "csv_path": str(TRIAL_CSV_PATH),
            "report_path": str(TRIAL_REPORT_PATH),
            "contact_sheet_path": str(CONTACT_SHEET_PATH),
        },
        "detail_errors": detail_errors,
        "structure_mismatches": structure_mismatches,
        "failure_states": failure_states,
        "photo_errors": photo_errors,
        "photo_samples": photo_samples,
        "selected_rows": [
            {
                "姓名": clean_text(row.get("姓名")),
                "科室": atomic_department(row),
                "职称层级": title_level(row.get("职称身份原文")),
                "主职称": primary_title(row.get("职称身份原文")),
                "来源链接": clean_text(row.get("来源链接")),
            }
            for row in trial_rows
        ],
    }
    validate_payload(payload)
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_manifest(manifest_rows)
    write_report(payload)
    return payload


def mark_visual_pass() -> dict[str, Any]:
    payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
    validate_payload(payload)
    payload["meta"]["visual_review_status"] = "MANUAL_CONTACT_SHEET_REVIEW_PASSED"
    payload["meta"]["visual_review_date"] = date.today().isoformat()
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(payload)
    return payload


def append_failure_warning(value: Any, state: str) -> str:
    if state not in FULL_WARNING_BY_STATE:
        raise ValueError(f"未知照片失败状态：{state}")
    warning = FULL_WARNING_BY_STATE[state]
    existing = [item for item in clean_text(value).split("；") if item]
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
            safe_photo_part(row.get("姓名")),
            atomic_department(row),
            safe_photo_part(primary_title(row.get("职称身份原文"))),
            safe_photo_part(HOSPITAL),
        ]
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
            if source not in target_sources:
                raise RuntimeError(f"发现 Issue #61 范围外行修改：{source} {column}")
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


def canonical_master_row(row: dict[str, Any]) -> tuple[str, ...]:
    return tuple(row_value(row.get(header)) for header in BASE_HEADERS)


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
    large_photos = [
        item
        for item in payload.get("photo_samples", [])
        if int(item.get("bytes") or 0) > MAX_OWNER_REPORT_BYTES
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
    )
    if not large_photo_lines:
        large_photo_lines = "| 无 | — | 0 | — |"
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 FULL 报告

> 日期：{meta['run_date']}
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`
> 照片政策：`OWNER_APPROVED_PAGE_REFERENCED_STYLES_WATERMARK_ORIGINAL_BYTES`

## 四数对账

| 范围 / 应采 | 实采 | 失败 | 留空 |
|---:|---:|---:|---:|
| {meta['expected_count']} | {meta['downloaded_count']} | {meta['failed_count']} | {meta['blank_count']} |

| 失败三态 | 数量 |
|---|---:|
{failure_lines}

- 总问题率：{meta['failed_count']}/{meta['expected_count']}（{meta['failure_ratio']:.2%}），未超过 30% 熔断线。
- 照片总字节：{meta['photo_total_bytes']} bytes（{meta['photo_total_mib']:.2f} MiB）。
- 最大单张：{meta['photo_max_bytes']} bytes；超过 5 MiB：{meta['over_5mib_count']} 张；超过 20 MiB：{meta['over_20mib_count']} 张。
- 页面未引用路径的构造/探测请求：0；第三方来源：0。
- 传输不完整原样重试：{meta['incomplete_read_retry_count']} 次；每个请求至多重试 1 次。
- 总底表：payload/CSV/XLSX 三载体行数与 25 列逐值一致；仅本院 413 行的照片两列及失败行异常提示允许变化。
- 画像：既有 {meta['existing_profile_count']} 份画像中，实采成功的 {meta['profile_refreshed_count']} 份仅新增方案 A 照片引用区块；失败留空画像零触碰；不新建画像；`_索引.md` 零修改。

## >5 MiB Owner 终审清单

| 姓名 | URL | 字节 | 尺寸 |
|---|---|---:|---:|
{large_photo_lines}

## 工件

- `{FULL_JSON_PATH}`
- `{FULL_CSV_PATH}`
- `{FULL_REPORT_PATH}`
- `{FORMAL_PHOTO_DIR}`
- `{ROOT / 'docs' / '中山五院照片嵌入方式裁决单.md'}`

## 合规边界

1. 只访问 413 条既有医院官网医生详情链接及页面 `.field.field-featured-media.field-item img` 容器自身引用的 `styles/watermark` 派生图。
2. 使用官网首页建立的常规 Cookie 会话和对应详情页 Referer；保留 `itok`，按页面引用原始响应字节保存，不压缩。
3. 禁止构造或探测页面未引用图片路径；禁止第三方来源。
4. 失败仅按“详情不可达 / 无照片容器 / 占位图”留空并追加异常提示。
"""
    path.write_text(report, encoding="utf-8", newline="\n")


def validate_full_payload(payload: dict[str, Any], photo_root: Path) -> None:
    meta = payload.get("meta", {})
    expected = int(meta.get("expected_count") or 0)
    downloaded = int(meta.get("downloaded_count") or 0)
    failed = int(meta.get("failed_count") or 0)
    blank = int(meta.get("blank_count") or 0)
    if (
        expected != EXPECTED_SCOPE_COUNT
        or downloaded + failed != expected
        or blank != failed
    ):
        raise RuntimeError("FULL 范围/应采/实采/失败/留空未形成四数闭环")
    state_counts = Counter(meta.get("failure_state_counts") or {})
    if set(state_counts) - set(FULL_FAILURE_STATES) or sum(state_counts.values()) != failed:
        raise RuntimeError("FULL 失败三态分布不闭合")
    if expected and failed / expected > MAX_FAILURE_RATIO:
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 总问题率超过 30%："
            f"{failed}/{expected}"
        )
    if int(meta.get("constructed_unreferenced_probe_count") or 0) != 0:
        raise RuntimeError("FULL 发生页面未引用路径探测")
    if int(meta.get("third_party_source_count") or 0) != 0:
        raise RuntimeError("FULL 发生第三方来源访问")
    if int(meta.get("existing_profile_count") or 0) != EXPECTED_PROFILE_COUNT:
        raise RuntimeError("FULL 既有画像数量漂移")
    if int(meta.get("no_profile_scope_count") or 0) != 0:
        raise RuntimeError("FULL 目标范围存在缺失画像")
    if int(meta.get("profile_refreshed_count") or 0) != downloaded:
        raise RuntimeError("FULL 成功照片数与画像嵌入数不一致")

    reconciliation = payload.get("reconciliation", [])
    rows = payload.get("rows", [])
    photos = payload.get("photo_samples", [])
    if len(reconciliation) != expected or len(rows) != expected or len(photos) != downloaded:
        raise RuntimeError("FULL 413 行对账工件数量不一致")
    rows_by_source = {clean_text(row.get("来源链接")): row for row in rows}
    photos_by_source = {clean_text(item.get("source_link")): item for item in photos}
    if len(rows_by_source) != expected or len(photos_by_source) != downloaded:
        raise RuntimeError("FULL 来源链接对账不唯一")

    expected_files: set[str] = set()
    total_bytes = 0
    max_bytes = 0
    over_5mib_count = 0
    over_20mib_count = 0
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
            if len(content) != int(photo.get("bytes") or 0):
                raise RuntimeError(f"照片字节数对账失败：{filename}")
            if hashlib.sha256(content).hexdigest() != photo.get("sha256"):
                raise RuntimeError(f"照片 SHA-256 对账失败：{filename}")
            expected_extension = disk_path.suffix.lower().lstrip(".")
            enforce_full_photo_policy(
                clean_text(row.get("姓名")),
                clean_text(photo.get("photo_url")),
                expected_extension,
                len(content),
            )
            content_type = "image/jpeg" if expected_extension == "jpg" else f"image/{expected_extension}"
            if magic_extension(content, content_type) != expected_extension:
                raise RuntimeError(f"照片魔数与扩展名不符：{filename}")
            if content[:12].hex().upper() != clean_text(photo.get("magic_hex")):
                raise RuntimeError(f"照片魔数证据不一致：{filename}")
            if image_dimensions(content) != (
                int(photo.get("width") or 0),
                int(photo.get("height") or 0),
            ):
                raise RuntimeError(f"照片尺寸对账失败：{filename}")
            expected_files.add(filename)
            total_bytes += len(content)
            max_bytes = max(max_bytes, len(content))
            over_5mib_count += int(len(content) > MAX_OWNER_REPORT_BYTES)
            over_20mib_count += int(len(content) > MAX_FULL_IMAGE_BYTES)
        elif status == "失败":
            if state not in FULL_FAILURE_STATES:
                raise RuntimeError(f"FULL 失败行未归入三态：{source}")
            if clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")):
                raise RuntimeError(f"FULL 失败行未留空照片字段：{source}")
            if FULL_WARNING_BY_STATE[state] not in clean_text(row.get("异常提示")):
                raise RuntimeError(f"FULL 失败行未追加异常提示：{source}")
        else:
            raise RuntimeError(f"FULL 对账状态非法：{source} {status}")

    actual_files = {item.name for item in photo_root.iterdir() if item.is_file()}
    if actual_files != expected_files:
        raise RuntimeError("FULL 照片目录磁盘集合与照片对账不一致")
    if total_bytes != int(meta.get("photo_total_bytes") or 0):
        raise RuntimeError("FULL 照片总字节对账失败")
    if max_bytes != int(meta.get("photo_max_bytes") or 0):
        raise RuntimeError("FULL 最大单张字节对账失败")
    if int(meta.get("over_5mib_count") or 0) != over_5mib_count:
        raise RuntimeError("FULL 超过 5 MiB 照片计数对账失败")
    if int(meta.get("over_20mib_count") or 0) != over_20mib_count:
        raise RuntimeError("FULL 超过 20 MiB 照片计数对账失败")
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
    marker = re.compile(
        r"(?m)^## 基础信息[ \t]*(?P<newline>\r\n|\n)(?P=newline)"
    )
    matches = list(marker.finditer(before_text))
    if len(matches) != 1:
        raise RuntimeError(
            f"画像基础信息插入点不唯一：{doctor_name} 数量={len(matches)}"
        )
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
    if after_bytes != insert_profile_photo_block_bytes(
        before_bytes, doctor_name, photo_file
    ):
        raise RuntimeError(f"画像出现照片嵌入区块以外字节变化：{doctor_name}")


def profile_markdown_tree(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes()
        for path in sorted(root.rglob("*.md"))
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
        staging = target.with_name(f".{target.name}.issue61.tmp")
        if staging.exists():
            staging.unlink()
        shutil.copy2(source, staging)
        staging.replace(target)


def restore_file_targets(backups: dict[Path, Path | None]) -> None:
    for target, backup in backups.items():
        staging = target.with_name(f".{target.name}.issue61.restore")
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
        raise RuntimeError("FULL 前 413 个来源与 413 份画像不是一一对应")
    return result


def preflight_profile_bytes(
    profile_paths: dict[str, Path], rows_by_source: dict[str, dict[str, Any]]
) -> dict[str, bytes]:
    before_profile_bytes: dict[str, bytes] = {}
    probe_file = (PHOTO_RELATIVE_ROOT / "__preflight__.jpg").as_posix()
    for source, path in profile_paths.items():
        content = path.read_bytes()
        doctor_name = clean_text(rows_by_source[source].get("姓名"))
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
        row
        for row in final_rows
        if clean_text(row.get("医院")) == HOSPITAL
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
        content = path.read_bytes()
        expected = integrity.get(source)
        if expected is None:
            raise RuntimeError(f"FULL 画像完整性清单缺少来源：{source}")
        if hashlib.sha256(content).hexdigest() != clean_text(expected.get("after_sha256")):
            raise RuntimeError(f"FULL 画像落盘哈希不一致：{path}")
    index_path = PROFILE_DIR / "_索引.md"
    if hashlib.sha256(index_path.read_bytes()).hexdigest() != clean_text(
        payload.get("meta", {}).get("profile_index_before_sha256")
    ):
        raise RuntimeError("FULL 修改了 _索引.md")
    if file_snapshot([LEDGER_PATH, MASTER_REPORT_PATH]) != payload["meta"].get(
        "protected_assets_before"
    ):
        raise RuntimeError("FULL 触碰了入口台账或总底表更新报告")
    with FULL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        if len(list(csv.DictReader(handle))) != EXPECTED_SCOPE_COUNT:
            raise RuntimeError("FULL 照片对账 CSV 不是 413 行")


def run_full(run_date: str) -> dict[str, Any]:
    import collect_official_doctors_batch as collector
    import generate_obsidian_profiles as profiles

    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("FULL 前正式照片目录已存在，拒绝覆盖；需 owner 先裁决")
    baseline_protected = file_snapshot([LEDGER_PATH, MASTER_REPORT_PATH])
    index_path = PROFILE_DIR / "_索引.md"
    if not index_path.is_file():
        raise RuntimeError("FULL 前本院 _索引.md 缺失")
    index_before_sha256 = hashlib.sha256(index_path.read_bytes()).hexdigest()
    master_payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    before_rows = copy.deepcopy(master_payload.get("rows", []))
    scope_rows = load_scope_rows()
    target_sources = {clean_text(row.get("来源链接")) for row in scope_rows}
    if len(scope_rows) != EXPECTED_SCOPE_COUNT or len(target_sources) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 固定范围不是 413 个唯一官网医生详情来源")
    rows_by_source = {
        clean_text(row.get("来源链接")): row for row in scope_rows
    }
    before_profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
    before_profile_bytes = preflight_profile_bytes(before_profile_paths, rows_by_source)
    before_profile_tree = profile_markdown_tree(PROFILE_DIR)

    session = OfficialSession()
    home_status, _, _, _ = session.get(OFFICIAL_HOME)
    if home_status != 200:
        raise RuntimeError(f"官网首页常规会话建立失败：HTTP {home_status}")

    with tempfile.TemporaryDirectory(prefix="issue61_full_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_photo_dir = temp_root / "photos"
        temp_photo_dir.mkdir()
        temp_profile_root = temp_root / "profiles"
        temp_hospital_dir = temp_profile_root / HOSPITAL
        shutil.copytree(PROFILE_DIR, temp_hospital_dir)

        used_filenames: set[str] = set()
        result_rows: list[dict[str, Any]] = []
        photo_samples: list[dict[str, Any]] = []
        failures: list[dict[str, str]] = []
        reconciliation: list[dict[str, Any]] = []

        def record_failure(row: dict[str, Any], state: str, evidence: str) -> None:
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
            try:
                status, content_type, charset, content = session.get(
                    source_link, DIRECTORY_URL
                )
            except RuntimeError as exc:
                record_failure(row, "详情不可达", f"详情请求异常：{exc}")
                continue
            if status != 200 or content_type != "text/html":
                record_failure(
                    row,
                    "详情不可达",
                    f"详情 HTTP {status} Content-Type {content_type}",
                )
                continue
            try:
                html = content.decode(charset, errors="replace")
            except LookupError:
                html = content.decode("utf-8", errors="replace")
            failure_state, portrait = inspect_portrait_reference(
                html, source_link, name
            )
            if failure_state:
                record_failure(row, failure_state, failure_state)
                continue
            if portrait is None:
                raise RuntimeError(f"职业照检查未返回明确结果：{source_link}")

            try:
                photo_status, photo_type, _, photo_content = session.get(
                    portrait.photo_url, source_link
                )
            except RuntimeError as exc:
                record_failure(row, "详情不可达", f"照片资源请求异常：{exc}")
                continue
            if photo_status != 200:
                record_failure(row, "详情不可达", f"照片资源 HTTP {photo_status}")
                continue
            extension = magic_extension(photo_content, photo_type)
            enforce_full_photo_policy(
                name, portrait.photo_url, extension, len(photo_content)
            )
            placeholder_reason = downloaded_placeholder_reason(
                portrait.photo_url, photo_content, extension
            )
            if placeholder_reason:
                record_failure(row, "占位图", placeholder_reason)
                continue
            try:
                width, height = image_dimensions(photo_content)
            except Exception as exc:  # noqa: BLE001 - retain exact image evidence
                record_failure(row, "详情不可达", f"照片尺寸无法解析：{exc}")
                continue
            filename, disk_path = allocate_full_photo_path(
                row, source_id, extension, temp_photo_dir, used_filenames
            )
            disk_path.write_bytes(photo_content)
            relative_path = (PHOTO_RELATIVE_ROOT / filename).as_posix()
            result_row = dict(row)
            result_row["照片链接"] = portrait.photo_url
            result_row["照片文件"] = relative_path
            result_rows.append(result_row)
            digest = hashlib.sha256(photo_content).hexdigest()
            sample = {
                "name": name,
                "department": atomic_department(row),
                "title": primary_title(row.get("职称身份原文")),
                "detail_id": source_id,
                "source_link": source_link,
                "photo_url": portrait.photo_url,
                "photo_source_attribute": portrait.source_attribute,
                "reference_kind": portrait.reference_kind,
                "derivative_style": portrait.derivative_style,
                "photo_file": relative_path,
                "filename": filename,
                "content_type": photo_type,
                "bytes": len(photo_content),
                "sha256": digest,
                "magic_hex": photo_content[:12].hex().upper(),
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
                    "照片链接": portrait.photo_url,
                    "照片文件": relative_path,
                    "字节数": len(photo_content),
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
            raise RuntimeError(f"FULL 结果行不是 413：{len(result_rows)}")
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
            json.dumps(updated_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        write_master_csv(temp_master_csv, after_rows)
        collector.build_workbook(
            temp_master_payload, temp_master_xlsx, temp_master_preview
        )
        validate_master_layers(
            temp_master_payload, temp_master_csv, temp_master_xlsx
        )

        success_sources = {
            clean_text(item.get("source_link")) for item in photo_samples
        }
        after_profile_paths = target_profile_paths(
            temp_hospital_dir, target_sources
        )
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
                    "path": before_profile_paths[source].relative_to(PROFILE_DIR).as_posix(),
                    "changed": source in success_sources,
                    "before_sha256": hashlib.sha256(before_content).hexdigest(),
                    "after_sha256": hashlib.sha256(after_content).hexdigest(),
                }
            )

        state_counter = Counter(item["state"] for item in failures)
        total_bytes = sum(int(item["bytes"]) for item in photo_samples)
        max_bytes = max((int(item["bytes"]) for item in photo_samples), default=0)
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
                    state: state_counter.get(state, 0)
                    for state in FULL_FAILURE_STATES
                },
                "detail_unreachable_count": state_counter.get("详情不可达", 0),
                "no_photo_container_count": state_counter.get("无照片容器", 0),
                "placeholder_count": state_counter.get("占位图", 0),
                "photo_total_bytes": total_bytes,
                "photo_total_mib": total_bytes / 1024 / 1024,
                "photo_max_bytes": max_bytes,
                "over_5mib_count": sum(
                    int(item["bytes"]) > MAX_OWNER_REPORT_BYTES
                    for item in photo_samples
                ),
                "over_20mib_count": sum(
                    int(item["bytes"]) > MAX_FULL_IMAGE_BYTES
                    for item in photo_samples
                ),
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "cookie_names": session.cookie_names,
                "incomplete_read_retry_count": session.incomplete_read_retry_count,
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
            json.dumps(full_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
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
        photo_backup = temp_root / "formal_photo_backup"
        photo_swapped = False
        try:
            ensure_workspace_target(FORMAL_PHOTO_DIR)
            if FORMAL_PHOTO_DIR.exists():
                FORMAL_PHOTO_DIR.replace(photo_backup)
            temp_photo_dir.replace(FORMAL_PHOTO_DIR)
            photo_swapped = True
            apply_file_map(file_map)

            final_rows = validate_master_layers(
                MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH
            )
            final_diffs = collect_full_row_diffs(
                before_rows, final_rows, target_sources
            )
            if final_diffs != row_diffs:
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
            if file_snapshot([LEDGER_PATH, MASTER_REPORT_PATH]) != baseline_protected:
                raise RuntimeError("FULL 触碰了入口台账或总底表更新报告")
            with FULL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
                if len(list(csv.DictReader(handle))) != EXPECTED_SCOPE_COUNT:
                    raise RuntimeError("FULL 照片对账 CSV 不是 413 行")
            validate_full_installation(full_payload)
        except Exception:
            restore_file_targets(backups)
            if photo_swapped and FORMAL_PHOTO_DIR.exists():
                ensure_workspace_target(FORMAL_PHOTO_DIR)
                shutil.rmtree(FORMAL_PHOTO_DIR)
            if photo_backup.exists():
                photo_backup.replace(FORMAL_PHOTO_DIR)
            raise
        return full_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #61 中山五院照片补录")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trial-only", action="store_true", help="执行固定 10 位 TRIAL")
    mode.add_argument(
        "--mark-visual-pass", action="store_true", help="人工查看联系表后固化视觉通过结论"
    )
    mode.add_argument("--validate", action="store_true", help="验证现有 TRIAL payload")
    mode.add_argument(
        "--full",
        action="store_true",
        help="按 PR #62 owner FULL 授权执行 413 行照片回填与方案 A 画像嵌入",
    )
    mode.add_argument(
        "--validate-full",
        action="store_true",
        help="验证已落盘 FULL payload、三载体、照片与画像完整性",
    )
    parser.add_argument("--run-date", default=date.today().isoformat())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.full:
        payload = run_full(args.run_date)
    elif args.validate_full:
        payload = json.loads(FULL_JSON_PATH.read_text(encoding="utf-8"))
        validate_full_installation(payload)
    elif args.trial_only:
        payload = run_trial(args.run_date)
    elif args.mark_visual_pass:
        payload = mark_visual_pass()
    else:
        payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
        validate_payload(payload)
    meta = payload["meta"]
    if meta.get("phase") == "FULL_READY_FOR_FINAL_OWNER_AUDIT":
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
                "mode": "photo_backfill_trial",
                "phase": meta["phase"],
                "hospital": meta["hospital"],
                "scope": meta["scope_count"],
                "photos": meta["photo_sample_count"],
                "visual_review": meta["visual_review_status"],
                "total_bytes": meta["photo_total_bytes"],
                "average_bytes": meta["photo_average_bytes"],
                "report": meta["report_path"],
                "contact_sheet": meta["contact_sheet_path"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
