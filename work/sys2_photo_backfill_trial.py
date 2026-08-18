from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import time
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from http.client import IncompleteRead
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlparse
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
HOSPITAL = "中山大学孙逸仙纪念医院"
ISSUE_NUMBER = 69
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

OFFICIAL_HOME = "https://www.gzsys.org.cn/"
DIRECTORY_URL = "https://www.gzsys.org.cn/doctor/592/search"
OFFICIAL_HOST = "gzsys.org.cn"
PHOTO_ROOT = "/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/"
EXPECTED_SCOPE_COUNT = 658
EXPECTED_TRIAL_COUNT = 10
EXPECTED_PROFILE_MARKDOWN_COUNT = 659
MAX_PHOTO_BYTES = 20 * 1024 * 1024
OWNER_REPORT_BYTES = 5 * 1024 * 1024
DETAIL_RETRY_SECONDS = 30
PRETRIAL_DIAGNOSTIC_EXCLUDED_REQUEST_COUNT = 18

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

SAMPLE_PLAN = (
    ("宋尔卫", "正高"),
    ("陈样新", "正高"),
    ("詹俊", "正高"),
    ("黄晓波", "副高"),
    ("黎江", "副高"),
    ("常瑞明", "副高"),
    ("马剑达", "副高"),
    ("黄泽坚", "其他"),
    ("曾志芬", "其他"),
    ("李卓", "其他"),
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
    "副研究员",
    "研究员",
    "副教授",
    "教授",
    "医师",
)

PHOTO_PATH_RE = re.compile(
    r"^/sites/syshospital\.prod\.sysucloud1\.sysu\.edu\.cn/files/"
    r"(?:(doctor)/)?[^/]+\.(?:jpe?g|png|gif|webp)$",
    re.IGNORECASE,
)
PLACEHOLDER_PATH_MARKERS = (
    "/default_images/",
    "placeholder",
    "nopic",
    "no_pic",
    "no-photo",
    "noimage",
    "no-image",
)
EXCLUDED_PATH_MARKERS = (
    "/styles/mini200/",
    "/inline-images/",
    "gongan",
    "favicon",
    "logo",
    "weixin",
    "chuzhen",
    "naoz",
    "fuwu",
    "dh_",
    "订阅号",
)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36; "
    "public official-site photo backfill trial"
)
VISUAL_PASS = "PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10"


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def comparable_host(value: str) -> str:
    host = (urlparse(value).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


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
    match = re.fullmatch(r"/(?:node|doctor)/(\d+)", parsed.path)
    return match.group(1) if match else ""


def detail_template(value: Any) -> str:
    path = urlparse(clean_text(value)).path
    if re.fullmatch(r"/node/\d+", path):
        return "node"
    if re.fullmatch(r"/doctor/\d+", path):
        return "doctor"
    return ""


def safe_photo_part(value: Any) -> str:
    text = re.sub(r'[\\/:*?"<>|]', "_", clean_text(value)).strip(" .")
    return text or "未标注"


def atomic_department(row: dict[str, Any]) -> str:
    value = clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
    atoms = [clean_text(item) for item in re.split(r"[、,，;/；|]+", value) if clean_text(item)]
    chinese = [item for item in atoms if re.search(r"[\u4e00-\u9fff]", item)]
    return safe_photo_part(chinese[0] if chinese else (atoms[0] if atoms else "未标注"))


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
        "主任中医师",
        "主任医师",
        "主任技师",
        "主任药师",
        "主任护师",
        "研究员",
        "教授",
    }:
        return "正高"
    if title in {
        "副主任中医师",
        "副主任医师",
        "副主任技师",
        "副主任药师",
        "副主任护师",
        "副研究员",
        "副教授",
    }:
        return "副高"
    return "其他"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def excluded_reference_reason(raw_url: str, source_link: str) -> str:
    absolute = urljoin(source_link, clean_text(raw_url))
    path = unquote(urlparse(absolute).path).lower()
    if any(marker in path for marker in PLACEHOLDER_PATH_MARKERS):
        return "占位图"
    if any(marker in path for marker in EXCLUDED_PATH_MARKERS):
        return "公共装饰图"
    return ""


def page_referenced_photo_url(raw_url: str, source_link: str) -> tuple[str, str]:
    raw = clean_text(raw_url)
    if not raw:
        return "", ""
    if excluded_reference_reason(raw, source_link):
        return "", ""
    absolute = urljoin(source_link, raw)
    parsed = urlparse(absolute)
    if (
        parsed.scheme not in {"http", "https"}
        or comparable_host(absolute) != OFFICIAL_HOST
        or parsed.query
        or parsed.fragment
    ):
        return "", ""
    match = PHOTO_PATH_RE.fullmatch(unquote(parsed.path))
    if not match:
        return "", ""
    kind = "doctor-subdir" if match.group(1) else "files-root"
    return absolute, kind


class DoctorPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, set[str]]] = []
        self.doctor_candidates: list[str] = []
        self.other_data_images: list[str] = []
        self._name_depth: int | None = None
        self._name_parts: list[str] = []
        self._title_depth: int | None = None
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = {key.lower(): clean_text(value) for key, value in attrs}
        classes = {item for item in attrs_map.get("class", "").split() if item}
        ancestors = [item[1] for item in self.stack]
        in_other_left = any("other-left" in item for item in ancestors) or "other-left" in classes
        in_other_media = any("other-media" in item for item in ancestors) or "other-media" in classes
        data_image = attrs_map.get("data-image-url", "")
        if data_image:
            if tag.lower() == "div" and "media-img" in classes and in_other_left and in_other_media:
                self.doctor_candidates.append(data_image)
            else:
                self.other_data_images.append(data_image)
        depth = len(self.stack)
        if tag.lower() == "div" and "other-left-title" in classes and in_other_left:
            self._name_depth = depth
        if tag.lower() == "title":
            self._title_depth = depth
        self.stack.append((tag.lower(), classes))

    def handle_data(self, data: str) -> None:
        if self._name_depth is not None:
            self._name_parts.append(data)
        if self._title_depth is not None:
            self._title_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        index = next(
            (index for index in range(len(self.stack) - 1, -1, -1) if self.stack[index][0] == tag),
            None,
        )
        if index is None:
            return
        if self._name_depth is not None and index <= self._name_depth:
            self._name_depth = None
        if self._title_depth is not None and index <= self._title_depth:
            self._title_depth = None
        del self.stack[index:]

    @property
    def doctor_name(self) -> str:
        return clean_text(" ".join(self._name_parts))

    @property
    def page_title(self) -> str:
        return clean_text(" ".join(self._title_parts))


@dataclass(frozen=True)
class PortraitReference:
    page_name: str
    page_title: str
    photo_url: str
    path_kind: str
    template_signature: str
    excluded_reference_count: int


def extract_portrait_reference(
    html: str, source_link: str, expected_name: str
) -> tuple[str, PortraitReference | None]:
    parser = DoctorPageParser()
    parser.feed(html)
    if parser.doctor_name != clean_text(expected_name):
        raise RuntimeError(
            f"医生详情标题与底表姓名不一致：{source_link} "
            f"expected={expected_name!r} actual={parser.doctor_name!r}"
        )
    candidates = [clean_text(item) for item in parser.doctor_candidates if clean_text(item)]
    if not candidates:
        return "无照片容器", None
    if len(set(candidates)) != 1:
        raise RuntimeError(f"医生照片容器存在多个不一致引用：{source_link} {candidates}")
    raw = candidates[0]
    reason = excluded_reference_reason(raw, source_link)
    if reason:
        return "占位图" if reason == "占位图" else "无照片容器", None
    photo_url, kind = page_referenced_photo_url(raw, source_link)
    if not photo_url:
        raise RuntimeError(f"医生照片容器 URL 越界：{source_link} {raw}")
    return "", PortraitReference(
        page_name=parser.doctor_name,
        page_title=parser.page_title,
        photo_url=photo_url,
        path_kind=kind,
        template_signature=".other-left .other-media .media-img[data-image-url]",
        excluded_reference_count=len(parser.other_data_images),
    )


class RedirectRecorder(HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.events: list[dict[str, Any]] = []

    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> Request | None:
        self.events.append(
            {"from": req.full_url, "to": newurl, "status": int(code), "utc": utc_now()}
        )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


@dataclass(frozen=True)
class HttpResult:
    status: int
    content_type: str
    charset: str
    content: bytes
    final_url: str
    redirects: tuple[dict[str, Any], ...]


class OfficialSession:
    def __init__(self) -> None:
        self.cookie_jar = CookieJar()
        self.redirect_recorder = RedirectRecorder()
        self.opener = build_opener(
            HTTPCookieProcessor(self.cookie_jar), self.redirect_recorder
        )
        self.incomplete_read_retry_count = 0

    @property
    def cookie_names(self) -> list[str]:
        return sorted(cookie.name for cookie in self.cookie_jar)

    def get(self, url: str, referer: str = "") -> HttpResult:
        headers = {"User-Agent": USER_AGENT}
        if referer:
            headers["Referer"] = referer
        request = Request(url, headers=headers)
        redirect_start = len(self.redirect_recorder.events)
        for attempt in range(2):
            try:
                with self.opener.open(request, timeout=35) as response:
                    content = response.read()
                    return HttpResult(
                        status=int(response.status),
                        content_type=response.headers.get_content_type(),
                        charset=response.headers.get_content_charset() or "utf-8",
                        content=content,
                        final_url=response.geturl(),
                        redirects=tuple(self.redirect_recorder.events[redirect_start:]),
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
                    redirects=tuple(self.redirect_recorder.events[redirect_start:]),
                )
            except URLError as exc:
                raise RuntimeError(f"官网请求失败：{url} {exc}") from exc
        raise AssertionError("官网请求循环未返回")


def fetch_detail_with_retry(
    session: OfficialSession,
    source_link: str,
    sleep_func: Callable[[float], None] = time.sleep,
) -> tuple[HttpResult, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    last_result: HttpResult | None = None
    for attempt in range(2):
        try:
            result = session.get(source_link, referer=DIRECTORY_URL)
            last_result = result
            attempts.append(
                {
                    "attempt": attempt + 1,
                    "utc": utc_now(),
                    "status": result.status,
                    "content_type": result.content_type,
                    "final_url": result.final_url,
                    "error": "",
                }
            )
            if result.status == 200:
                return result, attempts
        except RuntimeError as exc:
            attempts.append(
                {
                    "attempt": attempt + 1,
                    "utc": utc_now(),
                    "status": None,
                    "content_type": "",
                    "final_url": "",
                    "error": str(exc),
                }
            )
        if attempt == 0:
            sleep_func(DETAIL_RETRY_SECONDS)
    if last_result is not None:
        return last_result, attempts
    raise RuntimeError(f"详情连续两次请求失败：{source_link} {attempts}")


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
        result[str(path.relative_to(ROOT))] = {
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
    return result


def tree_snapshot(root: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    count = 0
    total_bytes = 0
    if root.is_dir():
        for path in sorted(
            (item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix()
        ):
            relative = path.relative_to(root).as_posix().encode("utf-8")
            content = path.read_bytes()
            digest.update(relative + b"\0" + content)
            count += 1
            total_bytes += len(content)
    return {
        "exists": root.is_dir(),
        "file_count": count,
        "bytes": total_bytes,
        "sha256": digest.hexdigest(),
    }


def protected_snapshot() -> dict[str, Any]:
    return {
        "master_assets": file_snapshot(
            [MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH, MASTER_REPORT_PATH, LEDGER_PATH]
        ),
        "profile_tree": tree_snapshot(PROFILE_DIR),
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
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} TRIAL 范围内已有照片字段")
    sources = [clean_text(row.get("来源链接")) for row in rows]
    if len(sources) != len(set(sources)):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} 范围来源链接不唯一")
    invalid = [source for source in sources if not detail_id(source)]
    if invalid:
        raise RuntimeError("范围存在非授权详情 URL：" + "、".join(invalid[:5]))
    if tree_snapshot(PROFILE_DIR)["file_count"] != EXPECTED_PROFILE_MARKDOWN_COUNT:
        raise RuntimeError("本院画像文件数不是 659")
    return rows


def select_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for expected_name, expected_level in SAMPLE_PLAN:
        matches = [row for row in rows if clean_text(row.get("姓名")) == expected_name]
        if len(matches) != 1:
            raise RuntimeError(f"试采姓名范围不唯一：{expected_name} 数量={len(matches)}")
        row = dict(matches[0])
        actual_level = title_level(row.get("职称身份原文"))
        if actual_level != expected_level:
            raise RuntimeError(
                f"试采职称层级漂移：{expected_name} 应为 {expected_level} 实际 {actual_level}"
            )
        result.append(row)
    departments = {atomic_department(row) for row in result}
    if len(departments) != EXPECTED_TRIAL_COUNT:
        raise RuntimeError(f"试采科室首原子不是 10 个：{len(departments)}")
    if Counter(title_level(row.get("职称身份原文")) for row in result) != Counter(
        {"正高": 3, "副高": 4, "其他": 3}
    ):
        raise RuntimeError("试采职称分层不是 3/4/3")
    if {detail_template(row.get("来源链接")) for row in result} != {"node", "doctor"}:
        raise RuntimeError("试采未覆盖 node 与 doctor 两种详情路由")
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
        raise RuntimeError(f"TRIAL 照片同名且字节不同：{path}")
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
    cell_width, cell_height = 320, 430
    columns, rows = 5, 2
    sheet = Image.new("RGB", (cell_width * columns, cell_height * rows), "white")
    title_font = contact_sheet_font(20)
    detail_font = contact_sheet_font(15)
    for index, sample in enumerate(samples):
        with Image.open(ROOT / sample["disk_path"]) as image:
            image.load()
            tile = ImageOps.contain(image.convert("RGB"), (280, 330))
        x = (index % columns) * cell_width
        y = (index // columns) * cell_height
        sheet.paste(tile, (x + (cell_width - tile.width) // 2, y + 8))
        draw = ImageDraw.Draw(sheet)
        draw.text((x + 12, y + 348), sample["name"], font=title_font, fill="black")
        draw.text(
            (x + 12, y + 378),
            f"{sample['department']} | {sample['primary_title']}",
            font=detail_font,
            fill="#333333",
        )
        draw.text(
            (x + 12, y + 404),
            f"{sample['width']}×{sample['height']} | {sample['bytes']:,} B",
            font=detail_font,
            fill="#555555",
        )
    sheet.save(CONTACT_SHEET_PATH, format="JPEG", quality=92, optimize=True)


def size_buckets(samples: list[dict[str, Any]]) -> dict[str, int]:
    result = {"<200KiB": 0, "200KiB-1MiB": 0, "1-5MiB": 0, "5-20MiB": 0, ">20MiB": 0}
    for sample in samples:
        size = int(sample["bytes"])
        if size < 200 * 1024:
            result["<200KiB"] += 1
        elif size < 1024 * 1024:
            result["200KiB-1MiB"] += 1
        elif size <= OWNER_REPORT_BYTES:
            result["1-5MiB"] += 1
        elif size <= MAX_PHOTO_BYTES:
            result["5-20MiB"] += 1
        else:
            result[">20MiB"] += 1
    return result


def write_manifest(samples: list[dict[str, Any]]) -> None:
    fields = [
        "name",
        "department",
        "primary_title",
        "title_level",
        "source_link",
        "detail_template",
        "photo_url",
        "path_kind",
        "filename",
        "bytes",
        "sha256",
        "width",
        "height",
        "detail_status",
        "photo_status",
        "photo_final_url",
    ]
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for sample in samples:
            writer.writerow({key: sample.get(key, "") for key in fields})


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    sample_lines = "\n".join(
        f"- {item['name']}｜{item['department']}｜{item['primary_title']}｜"
        f"{item['detail_template']}｜{item['path_kind']}｜{item['bytes']:,} bytes｜"
        f"{item['width']}×{item['height']}｜`{item['sha256']}`"
        for item in payload["photo_samples"]
    )
    owner_large = [item for item in payload["photo_samples"] if item["bytes"] > OWNER_REPORT_BYTES]
    owner_lines = "\n".join(
        f"- {item['name']}｜{item['photo_url']}｜{item['bytes']:,} bytes｜"
        f"{item['width']}×{item['height']}｜`{item['sha256']}`"
        for item in owner_large
    ) or "- 无"
    report = f"""# 中山大学孙逸仙纪念医院照片补录 TRIAL 报告

## 门禁与范围

- GitHub Issue：#{ISSUE_NUMBER}
- Phase：TRIAL
- 医院官网：{OFFICIAL_HOME}
- 医生目录：{DIRECTORY_URL}
- 总底表固定范围：{meta['scope_count']} 行；来源链接唯一 {meta['unique_source_count']}；TRIAL 前照片字段非空 {meta['baseline_photo_filled_count']}。
- 试采：{meta['trial_count']}/10；科室首原子 {meta['department_coverage_count']}；职称分层 {json.dumps(meta['title_level_counts'], ensure_ascii=False)}。

## 来源与会话边界

- 只解析 `{meta['template_signature']}`；TRIAL 对公共 `mini200`、默认图、院徽和 inline-images 的下载数为 {meta['trial_excluded_reference_download_count']}。
- 照片路径风格：{json.dumps(meta['path_kind_counts'], ensure_ascii=False)}；详情路由：{json.dumps(meta['detail_template_counts'], ensure_ascii=False)}。
- 常规 Cookie 会话只记录名称：{', '.join(meta['cookie_names']) or '无'}；所有照片请求携带对应详情页 Referer；页面未引用路径探测 {meta['constructed_unreferenced_probe_count']}；第三方来源 {meta['third_party_source_count']}。
- 实现前结构诊断曾由宽泛 `data-image-url` 正则额外请求 {meta['pretrial_diagnostic_excluded_request_count']} 个页面已引用 `mini200` 公共图标；未写文件、未进入 payload/联系表/正式资产。TRIAL 已改为容器限定解析，并以测试固定排除边界。

## 结果

- 详情成功 {meta['detail_success_count']}/10；照片成功 {meta['photo_success_count']}/10；详情失败 {meta['detail_failure_count']}；无照片容器 {meta['no_photo_container_count']}；占位图 {meta['placeholder_count']}；照片失败 {meta['photo_failure_count']}。
- 状态闪烁 {meta['status_flicker_count']}；>20 MiB 熔断 {meta['over_20mib_count']}；>5 MiB owner 清单 {meta['over_5mib_count']}。
- 总字节 {meta['total_bytes']:,}；最小 {meta['min_bytes']:,}；中位数 {meta['median_bytes']:,}；平均 {meta['average_bytes']:,}；最大 {meta['max_bytes']:,}。
- 大小分桶：{json.dumps(meta['size_buckets'], ensure_ascii=False)}。
- 按样本平均值线性估算 658 行容量：{meta['estimated_scope_bytes']:,} bytes（{meta['estimated_scope_mib']:.2f} MiB），只作容量估算。
- 联系表视觉状态：`{meta['visual_review_status']}`。

## 样本清单

{sample_lines}

## >5 MiB owner 终审清单

{owner_lines}

## 正式资产保护

- 入口台账、总底表 JSON/CSV/XLSX、更新报告、659 个本院 Markdown 聚合快照与正式照片目录在 TRIAL 前后完全一致：{meta['protected_assets_before'] == meta['protected_assets_after']}。
- TRIAL 只写 `work/` 工件；未回填三载体、未刷新画像、未创建正式照片目录。

## 停止点

TRIAL 工件完成后停止，等待 owner 审计。未取得明确 `FULL_APPEND_AND_OBSIDIAN` 前，不得写正式资产。
"""
    TRIAL_REPORT_PATH.write_text(report, encoding="utf-8")


def validate_payload(payload: dict[str, Any], require_visual_pass: bool) -> None:
    meta = payload.get("meta", {})
    errors: list[str] = []
    expected_names = [item[0] for item in SAMPLE_PLAN]
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围不是 658 行")
    if meta.get("trial_count") != EXPECTED_TRIAL_COUNT:
        errors.append("样本不是 10 位")
    if meta.get("department_coverage_count") != EXPECTED_TRIAL_COUNT:
        errors.append("科室首原子不是 10 个")
    if meta.get("title_level_counts") != {"正高": 3, "副高": 4, "其他": 3}:
        errors.append("职称分层不是 3/4/3")
    if set(meta.get("path_kind_counts", {})) != {"doctor-subdir", "files-root"}:
        errors.append("未覆盖两种原图路径风格")
    if set(meta.get("detail_template_counts", {})) != {"node", "doctor"}:
        errors.append("未覆盖两种详情路由")
    if any(
        meta.get(key) != 0
        for key in (
            "detail_failure_count",
            "no_photo_container_count",
            "placeholder_count",
            "photo_failure_count",
            "status_flicker_count",
            "over_20mib_count",
            "trial_excluded_reference_download_count",
            "constructed_unreferenced_probe_count",
            "third_party_source_count",
        )
    ):
        errors.append("TRIAL 存在失败、闪烁、越界或排除资源下载")
    if meta.get("pretrial_diagnostic_excluded_request_count") != 18:
        errors.append("实现前诊断偏差计数未固化")
    if meta.get("pretrial_diagnostic_persisted_count") != 0:
        errors.append("实现前排除资源发生落盘")
    if meta.get("protected_assets_before") != meta.get("protected_assets_after"):
        errors.append("正式资产发生变化")
    if require_visual_pass and meta.get("visual_review_status") != VISUAL_PASS:
        errors.append("联系表尚未人工视觉通过")
    samples = payload.get("photo_samples", [])
    if [item.get("name") for item in samples] != expected_names:
        errors.append("固定样本顺序或姓名漂移")
    hashes: set[str] = set()
    for sample in samples:
        relative = Path(sample.get("disk_path", ""))
        path = ROOT / relative
        try:
            path.relative_to(TRIAL_PHOTO_DIR)
        except ValueError:
            errors.append(f"照片不在 TRIAL 目录：{relative}")
            continue
        if not path.is_file():
            errors.append(f"照片不存在：{relative}")
            continue
        content = path.read_bytes()
        if len(content) != sample.get("bytes"):
            errors.append(f"照片字节不一致：{path.name}")
        digest = hashlib.sha256(content).hexdigest()
        if digest != sample.get("sha256"):
            errors.append(f"照片 SHA-256 不一致：{path.name}")
        if digest in hashes:
            errors.append(f"照片 SHA-256 重复：{path.name}")
        hashes.add(digest)
        extension = magic_extension(content, sample.get("content_type"))
        if extension != sample.get("extension"):
            errors.append(f"照片魔数/扩展名不一致：{path.name}")
        if image_dimensions(content) != (sample.get("width"), sample.get("height")):
            errors.append(f"照片尺寸不一致：{path.name}")
        url, kind = page_referenced_photo_url(sample.get("photo_url", ""), sample.get("source_link", ""))
        if url != sample.get("photo_url") or kind != sample.get("path_kind"):
            errors.append(f"照片 URL 越界：{path.name}")
        if comparable_host(sample.get("photo_final_url", "")) != OFFICIAL_HOST:
            errors.append(f"照片最终响应越出官网：{path.name}")
    if require_visual_pass and not CONTACT_SHEET_PATH.is_file():
        errors.append("联系表缺失")
    if errors:
        raise RuntimeError("TRIAL 验证失败：\n- " + "\n- ".join(errors))


def run_trial(run_date: str) -> dict[str, Any]:
    before = protected_snapshot()
    if before["profile_tree"]["file_count"] != EXPECTED_PROFILE_MARKDOWN_COUNT:
        raise RuntimeError("TRIAL 前本院画像聚合数量漂移")
    if before["formal_photo_tree"]["exists"]:
        raise RuntimeError("TRIAL 前正式照片目录已存在，需 owner 裁决")
    rows = load_scope_rows()
    trial_rows = select_trial_rows(rows)
    for path in (TRIAL_JSON_PATH, TRIAL_CSV_PATH, TRIAL_REPORT_PATH, CONTACT_SHEET_PATH):
        if path.exists():
            raise RuntimeError(f"TRIAL 工件已存在，拒绝覆盖：{path}")
    if TRIAL_PHOTO_DIR.exists():
        if any(TRIAL_PHOTO_DIR.iterdir()):
            raise RuntimeError(f"TRIAL 照片目录非空，拒绝覆盖：{TRIAL_PHOTO_DIR}")
    else:
        TRIAL_PHOTO_DIR.mkdir(parents=False)

    session = OfficialSession()
    landing = session.get(OFFICIAL_HOME)
    if landing.status != 200 or landing.content_type != "text/html":
        raise RuntimeError(f"官网首页响应异常：{landing.status} {landing.content_type}")
    directory = session.get(DIRECTORY_URL, referer=OFFICIAL_HOME)
    if directory.status != 200 or directory.content_type != "text/html":
        raise RuntimeError(f"医生目录响应异常：{directory.status} {directory.content_type}")

    samples: list[dict[str, Any]] = []
    detail_failure_count = 0
    no_photo_container_count = 0
    placeholder_count = 0
    photo_failure_count = 0
    status_flicker_count = 0

    for row in trial_rows:
        source_link = clean_text(row.get("来源链接"))
        detail, attempts = fetch_detail_with_retry(session, source_link)
        statuses = {item["status"] for item in attempts if item["status"] is not None}
        if len(statuses) > 1:
            status_flicker_count += 1
        if detail.status != 200:
            detail_failure_count += 1
            continue
        if detail.content_type != "text/html":
            raise RuntimeError(
                f"详情返回非 HTML：{source_link} HTTP {detail.status} {detail.content_type}"
            )
        html = detail.content.decode(detail.charset, errors="replace")
        state, reference = extract_portrait_reference(html, source_link, clean_text(row.get("姓名")))
        if state == "无照片容器":
            no_photo_container_count += 1
            continue
        if state == "占位图":
            placeholder_count += 1
            continue
        if reference is None:
            raise AssertionError("照片引用状态与对象不一致")
        photo = session.get(reference.photo_url, referer=source_link)
        if photo.status != 200:
            photo_failure_count += 1
            continue
        if comparable_host(photo.final_url) != OFFICIAL_HOST:
            raise RuntimeError(f"照片重定向越出官网：{reference.photo_url} -> {photo.final_url}")
        extension = magic_extension(photo.content, photo.content_type)
        if not extension:
            raise RuntimeError(
                f"照片响应格式异常：{reference.photo_url} HTTP {photo.status} {photo.content_type}"
            )
        if len(photo.content) > MAX_PHOTO_BYTES:
            raise RuntimeError(f"照片超过 20 MiB 熔断：{reference.photo_url} {len(photo.content)}")
        width, height = image_dimensions(photo.content)
        filename, disk_path = allocate_trial_photo(row, extension, photo.content)
        disk_path.write_bytes(photo.content)
        samples.append(
            {
                "name": clean_text(row.get("姓名")),
                "department": atomic_department(row),
                "primary_title": primary_title(row.get("职称身份原文")),
                "title_level": title_level(row.get("职称身份原文")),
                "source_link": source_link,
                "detail_template": detail_template(source_link),
                "detail_status": detail.status,
                "detail_final_url": detail.final_url,
                "detail_attempts": attempts,
                "page_name": reference.page_name,
                "page_title": reference.page_title,
                "template_signature": reference.template_signature,
                "excluded_reference_count": reference.excluded_reference_count,
                "photo_url": reference.photo_url,
                "path_kind": reference.path_kind,
                "photo_status": photo.status,
                "photo_final_url": photo.final_url,
                "photo_redirects": list(photo.redirects),
                "content_type": photo.content_type,
                "extension": extension,
                "filename": filename,
                "disk_path": disk_path.relative_to(ROOT).as_posix(),
                "bytes": len(photo.content),
                "sha256": hashlib.sha256(photo.content).hexdigest(),
                "width": width,
                "height": height,
            }
        )

    if len(samples) != EXPECTED_TRIAL_COUNT:
        raise RuntimeError(
            "TRIAL 未形成 10 张正式样本："
            f"success={len(samples)} detail_failure={detail_failure_count} "
            f"no_container={no_photo_container_count} placeholder={placeholder_count} "
            f"photo_failure={photo_failure_count}"
        )
    values = sorted(int(item["bytes"]) for item in samples)
    total_bytes = sum(values)
    median_bytes = (values[4] + values[5]) // 2
    average_bytes = total_bytes // len(values)
    after = protected_snapshot()
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "phase": "TRIAL",
            "hospital": HOSPITAL,
            "official_home": OFFICIAL_HOME,
            "doctor_directory": DIRECTORY_URL,
            "run_date": run_date,
            "scope_count": len(rows),
            "unique_source_count": len({clean_text(row.get("来源链接")) for row in rows}),
            "baseline_photo_filled_count": sum(
                bool(clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")))
                for row in rows
            ),
            "trial_count": len(samples),
            "department_coverage_count": len({item["department"] for item in samples}),
            "title_level_counts": dict(Counter(item["title_level"] for item in samples)),
            "detail_template_counts": dict(Counter(item["detail_template"] for item in samples)),
            "path_kind_counts": dict(Counter(item["path_kind"] for item in samples)),
            "template_signature": samples[0]["template_signature"],
            "detail_success_count": len(samples),
            "photo_success_count": len(samples),
            "detail_failure_count": detail_failure_count,
            "no_photo_container_count": no_photo_container_count,
            "placeholder_count": placeholder_count,
            "photo_failure_count": photo_failure_count,
            "status_flicker_count": status_flicker_count,
            "over_5mib_count": sum(item["bytes"] > OWNER_REPORT_BYTES for item in samples),
            "over_20mib_count": sum(item["bytes"] > MAX_PHOTO_BYTES for item in samples),
            "total_bytes": total_bytes,
            "min_bytes": values[0],
            "median_bytes": median_bytes,
            "average_bytes": average_bytes,
            "max_bytes": values[-1],
            "size_buckets": size_buckets(samples),
            "estimated_scope_bytes": average_bytes * EXPECTED_SCOPE_COUNT,
            "estimated_scope_mib": average_bytes * EXPECTED_SCOPE_COUNT / (1024 * 1024),
            "cookie_names": session.cookie_names,
            "incomplete_read_retry_count": session.incomplete_read_retry_count,
            "trial_excluded_reference_download_count": 0,
            "pretrial_diagnostic_excluded_request_count": PRETRIAL_DIAGNOSTIC_EXCLUDED_REQUEST_COUNT,
            "pretrial_diagnostic_persisted_count": 0,
            "constructed_unreferenced_probe_count": 0,
            "third_party_source_count": 0,
            "visual_review_status": "PENDING_MANUAL_CONTACT_SHEET_REVIEW",
            "protected_assets_before": before,
            "protected_assets_after": after,
        },
        "photo_samples": samples,
    }
    validate_payload(payload, require_visual_pass=False)
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(samples)
    build_contact_sheet(samples)
    write_report(payload)
    return payload


def load_trial_payload() -> dict[str, Any]:
    if not TRIAL_JSON_PATH.is_file():
        raise RuntimeError(f"TRIAL payload 不存在：{TRIAL_JSON_PATH}")
    return json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))


def mark_visual_pass() -> dict[str, Any]:
    payload = load_trial_payload()
    if not CONTACT_SHEET_PATH.is_file():
        raise RuntimeError("联系表不存在，不能标记视觉通过")
    payload["meta"]["visual_review_status"] = VISUAL_PASS
    validate_payload(payload, require_visual_pass=True)
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #69 孙逸仙纪念医院照片补录 TRIAL")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trial-only", action="store_true", help="执行固定 10 位 TRIAL")
    mode.add_argument("--mark-visual-pass", action="store_true", help="人工查看联系表后标记通过")
    mode.add_argument("--validate", action="store_true", help="验证现有 TRIAL 工件")
    parser.add_argument("--run-date", default=str(date.today()), help="采集日期 YYYY-MM-DD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.trial_only:
        payload = run_trial(args.run_date)
        print(
            json.dumps(
                {
                    "status": "TRIAL_READY_FOR_MANUAL_VISUAL_REVIEW",
                    "samples": payload["meta"]["trial_count"],
                    "payload": str(TRIAL_JSON_PATH),
                    "manifest": str(TRIAL_CSV_PATH),
                    "report": str(TRIAL_REPORT_PATH),
                    "contact_sheet": str(CONTACT_SHEET_PATH),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.mark_visual_pass:
        payload = mark_visual_pass()
        print(json.dumps({"status": payload["meta"]["visual_review_status"]}, ensure_ascii=False))
    else:
        payload = load_trial_payload()
        validate_payload(payload, require_visual_pass=True)
        if protected_snapshot() != payload["meta"]["protected_assets_after"]:
            raise RuntimeError("当前正式资产与 TRIAL 后快照不一致")
        print(json.dumps({"status": "TRIAL_VALIDATED", "samples": len(payload["photo_samples"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
