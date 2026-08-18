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
from http.client import IncompleteRead
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, ProxyHandler, build_opener

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "广州医科大学附属脑科医院"
ISSUE_NUMBER = 77
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

OFFICIAL_HOME = "https://www.gzbrain.cn/"
DIRECTORY_URL = "https://www.gzbrain.cn/myzj/list.html"
OFFICIAL_HOST = "gzbrain.cn"
EXPECTED_SCOPE_COUNT = 183
EXPECTED_PROFILE_FILE_COUNT = 184
EXPECTED_TRIAL_COUNT = 10
MAX_PHOTO_BYTES = 20 * 1024 * 1024
OWNER_REPORT_BYTES = 5 * 1024 * 1024
DETAIL_RETRY_SECONDS = 30
VISUAL_PASS = "PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10"
TEMPLATE_SIGNATURE = ".single_con > .single_cn > .single-img > img[src]"

SAMPLE_PLAN = (
    ("宁玉萍", "神经内科", "正高", "966"),
    ("成友军", "神经外科", "副高", "803"),
    ("周素妙", "中西医结合科", "中级", "96281"),
    ("张双春", "临床心理科", "其他", "11791"),
    ("周亮", "社区精神科", "正高", "4746"),
    ("彭妙官", "内分泌科", "副高", "100106"),
    ("王治华", "司法鉴定科", "中级", "560"),
    ("郭耀光", "康复科", "副高", "101440"),
    ("张继辉", "睡眠与节律医学中心", "正高", "49356"),
    ("韩为", "中医科", "正高", "33179"),
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
    "心理治疗师",
    "中医师",
    "医师",
)

PHOTO_PATH_RE = re.compile(
    r"^/uploadfiles/\d{4}/\d{2}/[^/]+\.(?:jpe?g|png|gif|webp)$",
    re.IGNORECASE,
)
OPAQUE_QUERY_RE = re.compile(r"^[A-Za-z0-9+/=_-]+$")
PLACEHOLDER_PATH_MARKERS = (
    "placeholder",
    "nopic",
    "no_pic",
    "no-photo",
    "noimage",
    "no-image",
    "default",
)
DECORATION_PATH_MARKERS = (
    "/banner/",
    "/image/yyhj_",
    "gongan",
    "favicon",
    "logo",
    "weixin",
    "wechat",
    "qrcode",
    "qr_code",
    "erweima",
)
EXCLUSION_RULES = (
    {
        "kind": "公共图标",
        "rule": "严格照片容器之外的 header/menu/action 图标一律排除",
    },
    {
        "kind": "装饰图片",
        "rule": "banner、医院环境、新闻/科普卡片及任何非 single-img 资源一律排除",
    },
    {
        "kind": "二维码",
        "rule": "路径或语义命中 qrcode/qr_code/erweima/weixin/wechat 时排除",
    },
    {
        "kind": "占位图",
        "rule": "路径命中 placeholder/nopic/noimage/default 时定格为占位图，不下载",
    },
    {
        "kind": "院徽/Logo",
        "rule": "路径命中 logo、favicon、gongan 或位于页眉区域时排除",
    },
    {
        "kind": "患者及合影",
        "rule": "即使位于候选容器，联系表目视发现患者、儿童、合影或非本人职业照也必须排除",
    },
)


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def comparable_host(value: str) -> str:
    host = (urlparse(value).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


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
    if title in {
        "主治中医师",
        "主治医师",
        "主管技师",
        "主管药师",
        "主管护师",
    }:
        return "中级"
    return "其他"


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
    match = re.fullmatch(r"/myzj/info_itemid_(\d+)\.html", parsed.path)
    return match.group(1) if match else ""


def excluded_reference_reason(raw_url: str, source_link: str) -> tuple[str, str]:
    absolute = urljoin(source_link, clean_text(raw_url))
    path = unquote(urlparse(absolute).path).lower()
    for marker in PLACEHOLDER_PATH_MARKERS:
        if marker in path:
            return "占位图", f"path contains {marker}"
    for marker in DECORATION_PATH_MARKERS:
        if marker in path:
            return "公共装饰图", f"path contains {marker}"
    return "", ""


def page_referenced_photo_url(raw_url: str, source_link: str) -> tuple[str, str]:
    raw = clean_text(raw_url)
    if not raw or excluded_reference_reason(raw, source_link)[0]:
        return "", ""
    absolute = urljoin(source_link, raw)
    parsed = urlparse(absolute)
    if (
        parsed.scheme != "https"
        or comparable_host(absolute) != OFFICIAL_HOST
        or parsed.fragment
        or not PHOTO_PATH_RE.fullmatch(unquote(parsed.path))
        or not parsed.query
        or not OPAQUE_QUERY_RE.fullmatch(parsed.query)
    ):
        return "", ""
    return absolute, parsed.query


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


def analyze_doctor_media(html: str, source_link: str, expected_name: str) -> MediaAnalysis:
    soup = BeautifulSoup(html, "html.parser")
    single_con = soup.select_one("div.single_con")
    if single_con is None:
        raise RuntimeError(f"医生详情缺少 .single_con：{source_link}")
    header = single_con.find("div", class_="single-header", recursive=False)
    single_cn = single_con.find("div", class_="single_cn", recursive=False)
    if header is None or single_cn is None:
        raise RuntimeError(f"医生详情主结构漂移：{source_link}")
    name_node = header.find("h2")
    title_node = header.find("h3")
    page_name = clean_text(name_node.get_text(" ", strip=True) if name_node else "")
    page_title = clean_text(title_node.get_text(" ", strip=True) if title_node else "")
    if page_name != clean_text(expected_name):
        raise RuntimeError(
            f"医生详情标题与底表姓名不一致：{source_link} "
            f"expected={expected_name!r} actual={page_name!r}"
        )
    photo_container = single_cn.find("div", class_="single-img", recursive=False)
    if photo_container is None:
        return MediaAnalysis(
            page_name=page_name,
            page_title=page_title,
            state="无照片容器",
            photo_url="",
            opaque_query="",
            template_signature=TEMPLATE_SIGNATURE,
            photo_reference_count=0,
            single_con_image_count=len(single_con.find_all("img")),
            outside_image_reference_count=len(soup.find_all("img", src=True)),
            excluded_resource_examples=(),
            container_html_snippet="",
            detection_feature=".single_cn direct child .single-img missing",
        )
    images = photo_container.find_all("img", recursive=False)
    if len(images) != 1 or not clean_text(images[0].get("src")):
        raise RuntimeError(f"医生照片容器不是唯一直接 img[src]：{source_link} count={len(images)}")
    raw_url = clean_text(images[0].get("src"))
    excluded_state, excluded_feature = excluded_reference_reason(raw_url, source_link)
    if excluded_state:
        return MediaAnalysis(
            page_name=page_name,
            page_title=page_title,
            state=excluded_state,
            photo_url="",
            opaque_query="",
            template_signature=TEMPLATE_SIGNATURE,
            photo_reference_count=1,
            single_con_image_count=len(single_con.find_all("img")),
            outside_image_reference_count=max(0, len(soup.find_all("img", src=True)) - 1),
            excluded_resource_examples=(
                {
                    "url": urljoin(source_link, raw_url),
                    "reason": excluded_state,
                    "feature": excluded_feature,
                },
            ),
            container_html_snippet=clean_text(str(photo_container)),
            detection_feature=excluded_feature,
        )
    photo_url, opaque_query = page_referenced_photo_url(raw_url, source_link)
    if not photo_url:
        raise RuntimeError(f"医生照片容器 URL 越界：{source_link} {raw_url}")
    outside: list[dict[str, str]] = []
    for img in soup.find_all("img", src=True):
        if img is images[0]:
            continue
        absolute = urljoin(source_link, clean_text(img.get("src")))
        if absolute and absolute not in {item["url"] for item in outside}:
            outside.append(
                {
                    "url": absolute,
                    "reason": "公共图标/装饰候选",
                    "feature": "outside strict .single-img doctor portrait container",
                }
            )
    return MediaAnalysis(
        page_name=page_name,
        page_title=page_title,
        state="",
        photo_url=photo_url,
        opaque_query=opaque_query,
        template_signature=TEMPLATE_SIGNATURE,
        photo_reference_count=1,
        single_con_image_count=len(single_con.find_all("img")),
        outside_image_reference_count=len(outside),
        excluded_resource_examples=tuple(outside[:12]),
        container_html_snippet=clean_text(str(photo_container)),
        detection_feature=(
            "single_con direct single_cn; direct single-img contains exactly one img[src]; "
            "same-site HTTPS /uploadfiles/YYYY/MM file with one opaque query token"
        ),
    )


class RedirectRecorder(HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.events: list[dict[str, Any]] = []

    def redirect_request(
        self,
        req: Any,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> Any:
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


class OfficialUrlOpenSession:
    """urllib public GET with its default UA and no cookies, proxy, or custom headers."""

    def __init__(self) -> None:
        self.redirect_recorder = RedirectRecorder()
        self.opener = build_opener(ProxyHandler({}), self.redirect_recorder)
        self.incomplete_read_retry_count = 0

    @property
    def cookie_names(self) -> list[str]:
        return []

    @property
    def default_headers(self) -> list[list[str]]:
        return [[str(key), str(value)] for key, value in self.opener.addheaders]

    def get(self, url: str) -> HttpResult:
        redirect_start = len(self.redirect_recorder.events)
        for attempt in range(2):
            try:
                with self.opener.open(url, timeout=35) as response:
                    return HttpResult(
                        status=int(response.status),
                        content_type=response.headers.get_content_type(),
                        charset=response.headers.get_content_charset() or "utf-8",
                        content=response.read(),
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
    session: OfficialUrlOpenSession,
    source_link: str,
    sleep_func: Callable[[float], None] = time.sleep,
) -> tuple[HttpResult, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    last_result: HttpResult | None = None
    for attempt in range(2):
        try:
            result = session.get(source_link)
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
        result[path.relative_to(ROOT).as_posix()] = {
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
    return result


def tree_snapshot(root: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    count = 0
    total_bytes = 0
    if root.is_dir():
        files = sorted(
            (item for item in root.rglob("*") if item.is_file()),
            key=lambda item: item.as_posix(),
        )
        for path in files:
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
    profile_tree = tree_snapshot(PROFILE_DIR)
    if profile_tree["file_count"] != EXPECTED_PROFILE_FILE_COUNT:
        raise RuntimeError(f"本院画像目录文件数不是 {EXPECTED_PROFILE_FILE_COUNT}")
    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("TRIAL 前正式照片目录已存在")
    return rows


def select_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_name: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_name.setdefault(clean_text(row.get("姓名")), []).append(row)
    selected: list[dict[str, Any]] = []
    for expected_name, expected_department, expected_level, expected_id in SAMPLE_PLAN:
        matches = by_name.get(expected_name, [])
        if len(matches) != 1:
            raise RuntimeError(f"TRIAL 样本姓名范围不唯一：{expected_name} 数量={len(matches)}")
        row = dict(matches[0])
        if atomic_department(row) != expected_department:
            raise RuntimeError(f"TRIAL 样本科室漂移：{expected_name}")
        if title_level(row.get("职称身份原文")) != expected_level:
            raise RuntimeError(f"TRIAL 样本职称层级漂移：{expected_name}")
        if detail_id(row.get("来源链接")) != expected_id:
            raise RuntimeError(f"TRIAL 样本详情 ID 漂移：{expected_name}")
        selected.append(row)
    if len({atomic_department(row) for row in selected}) != EXPECTED_TRIAL_COUNT:
        raise RuntimeError("TRIAL 样本未覆盖 10 个不同科室首原子")
    expected_levels = Counter({"正高": 4, "副高": 3, "中级": 2, "其他": 1})
    if Counter(title_level(row.get("职称身份原文")) for row in selected) != expected_levels:
        raise RuntimeError("TRIAL 职称分层不是正高4/副高3/中级2/其他1")
    return selected


def allocate_trial_photo(row: dict[str, Any], extension: str) -> tuple[str, Path]:
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
    if path.exists():
        filename = f"{stem}-{detail_id(row.get('来源链接'))}.{extension}"
        path = TRIAL_PHOTO_DIR / filename
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
            f"{sample['department']} | {sample['primary_title']} | {sample['title_level']}",
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
    buckets = {"<200KiB": 0, "200KiB-1MiB": 0, "1-5MiB": 0, "5-20MiB": 0, ">20MiB": 0}
    for sample in samples:
        size = int(sample["bytes"])
        if size < 200 * 1024:
            buckets["<200KiB"] += 1
        elif size <= 1024 * 1024:
            buckets["200KiB-1MiB"] += 1
        elif size <= OWNER_REPORT_BYTES:
            buckets["1-5MiB"] += 1
        elif size <= MAX_PHOTO_BYTES:
            buckets["5-20MiB"] += 1
        else:
            buckets[">20MiB"] += 1
    return buckets


MANIFEST_FIELDS = [
    "name",
    "department",
    "primary_title",
    "title_level",
    "source_link",
    "detail_id",
    "detail_status",
    "detail_probe_utc",
    "detail_attempts",
    "detail_final_url",
    "page_name",
    "page_title",
    "template_signature",
    "photo_reference_count",
    "single_con_image_count",
    "outside_image_reference_count",
    "detection_feature",
    "container_html_snippet",
    "excluded_resource_examples",
    "photo_url",
    "opaque_query",
    "filename",
    "disk_path",
    "bytes",
    "sha256",
    "declared_extension",
    "extension",
    "content_type",
    "width",
    "height",
    "photo_status",
    "photo_final_url",
]


def write_manifest(samples: list[dict[str, Any]]) -> None:
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for sample in samples:
            row = {key: sample.get(key, "") for key in MANIFEST_FIELDS}
            for key in ("detail_attempts", "excluded_resource_examples"):
                row[key] = json.dumps(row[key], ensure_ascii=False, separators=(",", ":"))
            writer.writerow(row)


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    samples = payload["photo_samples"]
    sample_lines = "\n".join(
        f"- {item['name']}｜{item['department']}｜{item['primary_title']}（{item['title_level']}）｜"
        f"{item['bytes']:,} bytes｜{item['width']}×{item['height']}｜"
        f"`{item['extension']}`｜`{item['sha256']}`"
        for item in samples
    )
    exclusion_lines = "\n".join(
        f"- {item['kind']}：{item['rule']}" for item in meta["exclusion_rules"]
    )
    large_lines = "\n".join(
        f"- {item['name']}｜{item['photo_url']}｜{item['bytes']:,} bytes｜`{item['sha256']}`"
        for item in samples
        if item["bytes"] > OWNER_REPORT_BYTES
    ) or "- 无"
    if meta["visual_review_status"] == VISUAL_PASS:
        visual_text = (
            "10/10 均已目视确认为医生本人单人职业照；未见患者、儿童、合影、二维码、"
            "公共装饰或占位图。"
        )
    else:
        visual_text = "待人工查看联系表；在标记通过前不得请求 Owner 审计。"
    representative = samples[0]["container_html_snippet"]
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 TRIAL 报告

## 门禁与范围

- Phase：`TRIAL_READY_FOR_OWNER_AUDIT`（视觉状态：`{meta['visual_review_status']}`）。
- 医院官网：{OFFICIAL_HOME}
- 医生目录：{DIRECTORY_URL}
- 固定范围：{meta['scope_count']} 行 / {meta['unique_source_count']} 个唯一 `myzj/info_itemid_<N>.html`；TRIAL 前照片两列非空 {meta['baseline_photo_filled_count']}。
- 样本：10 人、10 个不同科室首原子；职称分层 {json.dumps(meta['title_level_counts'], ensure_ascii=False)}。
- TRIAL 只写 `work/` 工件；入口台账、总底表三载体、报告、184 个本院 Markdown 和正式照片目录前后快照一致：{meta['protected_assets_before'] == meta['protected_assets_after']}。

## 访问与照片容器结构诊断

- 请求实现：`{meta['request_mode']}`；Cookie {len(meta['cookie_names'])}；代理禁用；未添加浏览器型请求头、Referer 或第三方来源。
- 首页、目录和 10 个详情页均为 HTTP 200；状态闪烁 {meta['status_flicker_count']}，详情失败 {meta['detail_failure_count']}。
- 严格容器：`{meta['template_signature']}`。10/10 页面在 `.single_con` 的直接子 `.single_cn` 下仅有一个直接子 `.single-img`，其中恰有一个直接 `img[src]`；该 URL 是唯一可下载候选。
- URL 门禁：同站 HTTPS；路径严格为 `/uploadfiles/YYYY/MM/<文件>.<jpg|jpeg|png|gif|webp>`；保留页面实际引用的不透明查询串；禁止构造、去查询串、猜测或探测其他路径。
- 10 个页面照片引用唯一数 {meta['unique_photo_url_count']}；页面外部图片引用只作排除诊断，不下载。页面未引用路径探测 {meta['constructed_unreferenced_probe_count']}；排除资源下载 {meta['excluded_reference_download_count']}；第三方来源 {meta['third_party_source_count']}。

代表性容器 HTML（宁玉萍；其余逐页片段在 manifest/payload）：

```html
{representative}
```

## 自拟排除清单与患者红线

{exclusion_lines}

- 判定依据：结构白名单先于路径白名单；即使路径形似图片，只要不在严格医生照片容器内即排除。
- 专科医院患者红线：自动结构门禁不能替代实图判断，必须以 10 图联系表逐图排除患者、儿童、合影或其他可识别患者信息。
- 视觉结论：{visual_text}

## 成功结果

- 详情成功 {meta['detail_success_count']}/10；照片成功 {meta['photo_success_count']}/10；无照片容器、占位图、照片资源不可达均为 0。
- 页面引用原始字节直接落盘，不压缩、不转码；按魔数命名。声明扩展名与魔数不一致 {meta['declared_extension_mismatch_count']}（成友军页面 URL/Content-Type 声明 JPEG，但原始魔数为 PNG，因此文件按 `.png` 命名）。
- 总字节 {meta['total_bytes']:,}；最小 {meta['min_bytes']:,}；中位数 {meta['median_bytes']:,}；平均 {meta['average_bytes']:,}；最大 {meta['max_bytes']:,}。
- 大小分桶：{json.dumps(meta['size_buckets'], ensure_ascii=False)}；>5 MiB {meta['over_5mib_count']}；>20 MiB {meta['over_20mib_count']}。
- 按样本平均值线性估算 183 行约 {meta['estimated_scope_mib']:.2f} MiB，仅作容量估算，不代表 FULL 成功率。

{sample_lines}

## Owner 大图终审清单（>5 MiB）

{large_lines}

## 工件与停止点

- Payload：`{TRIAL_JSON_PATH.relative_to(ROOT).as_posix()}`
- Manifest：`{TRIAL_CSV_PATH.relative_to(ROOT).as_posix()}`
- 联系表：`{CONTACT_SHEET_PATH.relative_to(ROOT).as_posix()}`
- 原图目录：`{TRIAL_PHOTO_DIR.relative_to(ROOT).as_posix()}`（10 张）
- 当前停止点：`TRIAL_READY_FOR_OWNER_AUDIT`。未取得 Owner 明确 `FULL_APPEND_AND_OBSIDIAN` 前，不得修改正式资产。
"""
    TRIAL_REPORT_PATH.write_text(report, encoding="utf-8")


def validate_payload(payload: dict[str, Any], require_visual_pass: bool) -> None:
    meta = payload.get("meta", {})
    samples = payload.get("photo_samples", [])
    errors: list[str] = []
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("固定范围不是 183 行")
    if meta.get("photo_success_count") != EXPECTED_TRIAL_COUNT or len(samples) != EXPECTED_TRIAL_COUNT:
        errors.append("TRIAL 成功照片不是 10 张")
    if meta.get("department_coverage_count") != EXPECTED_TRIAL_COUNT:
        errors.append("TRIAL 未覆盖 10 个科室首原子")
    if meta.get("title_level_counts") != {"正高": 4, "副高": 3, "中级": 2, "其他": 1}:
        errors.append("TRIAL 职称分层不是正高4/副高3/中级2/其他1")
    if any(
        meta.get(key) != 0
        for key in (
            "detail_failure_count",
            "no_photo_container_count",
            "placeholder_count",
            "photo_failure_count",
            "status_flicker_count",
            "over_20mib_count",
            "excluded_reference_download_count",
            "constructed_unreferenced_probe_count",
            "third_party_source_count",
        )
    ):
        errors.append("TRIAL 存在失败、闪烁、越界或排除资源下载")
    if meta.get("protected_assets_before") != meta.get("protected_assets_after"):
        errors.append("TRIAL 正式资产发生变化")
    if meta.get("cookie_names"):
        errors.append("urllib 会话出现 Cookie")
    if meta.get("request_mode") != "urllib-default-get/no-cookie/no-proxy/no-custom-headers":
        errors.append("请求模式不符合本院授权")
    if require_visual_pass and meta.get("visual_review_status") != VISUAL_PASS:
        errors.append("联系表尚未人工视觉通过")
    expected_names = [item[0] for item in SAMPLE_PLAN]
    if [sample.get("name") for sample in samples] != expected_names:
        errors.append("TRIAL 样本姓名或顺序漂移")
    if len({sample.get("photo_url") for sample in samples}) != EXPECTED_TRIAL_COUNT:
        errors.append("TRIAL 照片 URL 不唯一")
    if len({sample.get("sha256") for sample in samples}) != EXPECTED_TRIAL_COUNT:
        errors.append("TRIAL 照片 SHA-256 不唯一")
    for sample in samples:
        if sample.get("page_name") != sample.get("name"):
            errors.append(f"页面姓名漂移：{sample.get('name')}")
        if sample.get("page_title") != sample.get("title_raw"):
            errors.append(f"页面职称漂移：{sample.get('name')}")
        if sample.get("template_signature") != TEMPLATE_SIGNATURE:
            errors.append(f"照片容器签名漂移：{sample.get('name')}")
        if sample.get("photo_reference_count") != 1 or sample.get("single_con_image_count") != 1:
            errors.append(f"医生内容容器图片数量漂移：{sample.get('name')}")
        if 'class="single-img"' not in clean_text(sample.get("container_html_snippet")):
            errors.append(f"照片容器 HTML 片段缺失：{sample.get('name')}")
        relative = Path(clean_text(sample.get("disk_path")))
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
        if hashlib.sha256(content).hexdigest() != sample.get("sha256"):
            errors.append(f"照片 SHA-256 不一致：{path.name}")
        extension = magic_extension(content, sample.get("content_type"))
        if extension != sample.get("extension") or path.suffix.lower() != f".{extension}":
            errors.append(f"照片魔数/扩展名不一致：{path.name}")
        if image_dimensions(content) != (sample.get("width"), sample.get("height")):
            errors.append(f"照片尺寸不一致：{path.name}")
        url, opaque_query = page_referenced_photo_url(
            sample.get("photo_url", ""), sample.get("source_link", "")
        )
        if (url, opaque_query) != (sample.get("photo_url"), sample.get("opaque_query")):
            errors.append(f"照片 URL 门禁失败：{path.name}")
        if comparable_host(clean_text(sample.get("photo_final_url"))) != OFFICIAL_HOST:
            errors.append(f"照片最终响应越出官网：{path.name}")
        if detail_id(sample.get("source_link")) != sample.get("detail_id"):
            errors.append(f"详情 URL 门禁失败：{path.name}")
    if not CONTACT_SHEET_PATH.is_file():
        errors.append("联系表缺失")
    else:
        content = CONTACT_SHEET_PATH.read_bytes()
        if hashlib.sha256(content).hexdigest() != meta.get("contact_sheet_sha256"):
            errors.append("联系表 SHA-256 不一致")
        if len(content) != meta.get("contact_sheet_bytes"):
            errors.append("联系表字节数不一致")
    if errors:
        raise RuntimeError("TRIAL 验证失败：\n- " + "\n- ".join(errors))


def validate_manifest(payload: dict[str, Any]) -> None:
    if not TRIAL_CSV_PATH.is_file():
        raise RuntimeError("TRIAL manifest 缺失")
    with TRIAL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    samples = payload.get("photo_samples", [])
    if len(rows) != EXPECTED_TRIAL_COUNT:
        raise RuntimeError(f"TRIAL manifest 不是 10 行：{len(rows)}")
    keys = ("name", "source_link", "photo_url", "filename", "disk_path", "sha256", "extension")
    for row, sample in zip(rows, samples, strict=True):
        for key in keys:
            if row.get(key) != str(sample.get(key, "")):
                raise RuntimeError(f"manifest 与 payload 不一致：{sample.get('name')} {key}")
        if int(row.get("bytes", "-1")) != sample.get("bytes"):
            raise RuntimeError(f"manifest 与 payload 字节不一致：{sample.get('name')}")


def clean_output_preflight() -> None:
    for path in (TRIAL_JSON_PATH, TRIAL_CSV_PATH, TRIAL_REPORT_PATH, CONTACT_SHEET_PATH):
        if path.exists():
            raise RuntimeError(f"TRIAL 工件已存在，拒绝覆盖：{path}")
    if TRIAL_PHOTO_DIR.exists():
        raise RuntimeError(f"TRIAL 照片目录已存在，拒绝覆盖：{TRIAL_PHOTO_DIR}")


def run_trial(run_date: str) -> dict[str, Any]:
    before = protected_snapshot()
    rows = load_scope_rows()
    selected = select_trial_rows(rows)
    clean_output_preflight()
    session = OfficialUrlOpenSession()
    home = session.get(OFFICIAL_HOME)
    if home.status != 200 or home.content_type != "text/html":
        raise RuntimeError(f"官网首页响应异常：{home.status} {home.content_type}")
    directory = session.get(DIRECTORY_URL)
    if directory.status != 200 or directory.content_type != "text/html":
        raise RuntimeError(f"医生目录响应异常：{directory.status} {directory.content_type}")

    downloads: list[tuple[Path, bytes]] = []
    samples: list[dict[str, Any]] = []
    status_flicker_count = 0
    for row in selected:
        source_link = clean_text(row.get("来源链接"))
        detail, attempts = fetch_detail_with_retry(session, source_link)
        statuses = {item["status"] for item in attempts if item["status"] is not None}
        if len(statuses) > 1:
            status_flicker_count += 1
        if detail.status != 200 or detail.content_type != "text/html":
            raise RuntimeError(
                f"详情响应异常：{source_link} HTTP {detail.status} {detail.content_type}"
            )
        if comparable_host(detail.final_url) != OFFICIAL_HOST or not detail_id(detail.final_url):
            raise RuntimeError(f"详情最终响应越界：{source_link} -> {detail.final_url}")
        html = detail.content.decode(detail.charset, errors="replace")
        analysis = analyze_doctor_media(html, source_link, clean_text(row.get("姓名")))
        if analysis.state or not analysis.photo_url:
            raise RuntimeError(
                f"固定成功样本无可用本人照片：{row.get('姓名')} state={analysis.state}"
            )
        title_raw = clean_text(row.get("职称身份原文"))
        if analysis.page_title != title_raw:
            raise RuntimeError(
                f"详情职称与底表不一致：{row.get('姓名')} "
                f"expected={title_raw!r} actual={analysis.page_title!r}"
            )
        photo = session.get(analysis.photo_url)
        if photo.status != 200:
            raise RuntimeError(f"照片响应异常：{analysis.photo_url} HTTP {photo.status}")
        if comparable_host(photo.final_url) != OFFICIAL_HOST:
            raise RuntimeError(f"照片重定向越出官网：{analysis.photo_url} -> {photo.final_url}")
        extension = magic_extension(photo.content, photo.content_type)
        if not extension:
            raise RuntimeError(f"照片响应格式异常：{analysis.photo_url} {photo.content_type}")
        if len(photo.content) > MAX_PHOTO_BYTES:
            raise RuntimeError(f"照片超过 20 MiB 熔断：{analysis.photo_url} {len(photo.content)}")
        width, height = image_dimensions(photo.content)
        filename, disk_path = allocate_trial_photo(row, extension)
        downloads.append((disk_path, photo.content))
        declared_extension = Path(unquote(urlparse(analysis.photo_url).path)).suffix.lower().lstrip(".")
        samples.append(
            {
                "name": clean_text(row.get("姓名")),
                "department": atomic_department(row),
                "primary_title": primary_title(title_raw),
                "title_raw": title_raw,
                "title_level": title_level(title_raw),
                "source_link": source_link,
                "detail_id": detail_id(source_link),
                "detail_status": detail.status,
                "detail_probe_utc": attempts[-1]["utc"],
                "detail_attempts": attempts,
                "detail_final_url": detail.final_url,
                "page_name": analysis.page_name,
                "page_title": analysis.page_title,
                "template_signature": analysis.template_signature,
                "photo_reference_count": analysis.photo_reference_count,
                "single_con_image_count": analysis.single_con_image_count,
                "outside_image_reference_count": analysis.outside_image_reference_count,
                "excluded_resource_examples": list(analysis.excluded_resource_examples),
                "container_html_snippet": analysis.container_html_snippet,
                "detection_feature": analysis.detection_feature,
                "photo_url": analysis.photo_url,
                "opaque_query": analysis.opaque_query,
                "filename": filename,
                "disk_path": disk_path.relative_to(ROOT).as_posix(),
                "bytes": len(photo.content),
                "sha256": hashlib.sha256(photo.content).hexdigest(),
                "declared_extension": declared_extension,
                "extension": extension,
                "content_type": photo.content_type,
                "width": width,
                "height": height,
                "photo_status": photo.status,
                "photo_final_url": photo.final_url,
                "photo_redirects": list(photo.redirects),
            }
        )

    after = protected_snapshot()
    if after != before:
        raise RuntimeError("TRIAL 下载阶段正式资产发生变化")
    TRIAL_PHOTO_DIR.mkdir(parents=False)
    for path, content in downloads:
        path.write_bytes(content)
    build_contact_sheet(samples)
    contact_content = CONTACT_SHEET_PATH.read_bytes()
    values = sorted(int(item["bytes"]) for item in samples)
    total_bytes = sum(values)
    average_bytes = total_bytes // len(values)
    median_bytes = (values[4] + values[5]) // 2
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
            "photo_success_count": len(samples),
            "detail_success_count": len(samples),
            "detail_failure_count": 0,
            "no_photo_container_count": 0,
            "placeholder_count": 0,
            "photo_failure_count": 0,
            "status_flicker_count": status_flicker_count,
            "department_coverage_count": len({item["department"] for item in samples}),
            "title_level_counts": dict(Counter(item["title_level"] for item in samples)),
            "template_signature": TEMPLATE_SIGNATURE,
            "unique_photo_url_count": len({item["photo_url"] for item in samples}),
            "declared_extension_mismatch_count": sum(
                item["declared_extension"].replace("jpeg", "jpg") != item["extension"]
                for item in samples
            ),
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
            "request_mode": "urllib-default-get/no-cookie/no-proxy/no-custom-headers",
            "urllib_default_headers": session.default_headers,
            "cookie_names": session.cookie_names,
            "incomplete_read_retry_count": session.incomplete_read_retry_count,
            "excluded_reference_download_count": 0,
            "constructed_unreferenced_probe_count": 0,
            "third_party_source_count": 0,
            "exclusion_rules": list(EXCLUSION_RULES),
            "visual_review_status": "PENDING_MANUAL_CONTACT_SHEET_REVIEW",
            "visual_review_utc": "",
            "contact_sheet_sha256": hashlib.sha256(contact_content).hexdigest(),
            "contact_sheet_bytes": len(contact_content),
            "protected_assets_before": before,
            "protected_assets_after": after,
        },
        "photo_samples": samples,
    }
    validate_payload(payload, require_visual_pass=False)
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(samples)
    write_report(payload)
    validate_manifest(payload)
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
    payload["meta"]["visual_review_utc"] = utc_now()
    validate_payload(payload, require_visual_pass=True)
    validate_manifest(payload)
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #77 广州医科大学附属脑科医院照片补录 TRIAL")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trial-only", action="store_true", help="执行固定 10 人 TRIAL")
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
                    "success_photos": payload["meta"]["photo_success_count"],
                    "manifest_rows": len(payload["photo_samples"]),
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
        validate_manifest(payload)
        if protected_snapshot() != payload["meta"]["protected_assets_after"]:
            raise RuntimeError("当前正式资产与 TRIAL 后快照不一致")
        print(
            json.dumps(
                {
                    "status": "TRIAL_VALIDATED",
                    "success_photos": len(payload["photo_samples"]),
                    "manifest_rows": len(payload["photo_samples"]),
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
