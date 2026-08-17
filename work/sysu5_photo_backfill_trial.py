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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #61 中山五院照片补录 TRIAL")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trial-only", action="store_true", help="执行固定 10 位 TRIAL")
    mode.add_argument(
        "--mark-visual-pass", action="store_true", help="人工查看联系表后固化视觉通过结论"
    )
    mode.add_argument("--validate", action="store_true", help="验证现有 TRIAL payload")
    parser.add_argument("--run-date", default=date.today().isoformat())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.trial_only:
        payload = run_trial(args.run_date)
    elif args.mark_visual_pass:
        payload = mark_visual_pass()
    else:
        payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
        validate_payload(payload)
    meta = payload["meta"]
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
