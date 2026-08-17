from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
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
        description=f"Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 TRIAL"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trial-only", action="store_true")
    mode.add_argument("--validate", action="store_true")
    mode.add_argument("--mark-visual-pass", action="store_true")
    parser.add_argument("--today", default=date.today().isoformat())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.trial_only:
        payload = run_trial(args.today)
    else:
        if not TRIAL_JSON_PATH.is_file():
            raise RuntimeError("TRIAL payload 不存在")
        if args.mark_visual_pass:
            payload = mark_visual_pass()
        else:
            payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
            validate_payload(payload)
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
