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
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, unquote, urljoin, urlparse
from urllib.request import HTTPCookieProcessor, Request, build_opener

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"D:\workspace\信息收集整理")
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "中山大学附属第三医院"
ISSUE_NUMBER = 57
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
OFFICIAL_HOME = "https://www.zssy.com.cn/"
DIRECTORY_URL = "https://www.zssy.com.cn/page/5968"
OFFICIAL_HOST = "zssy.com.cn"
PHOTO_PREFIX = "/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/"
EXPECTED_SCOPE_COUNT = 780
EXPECTED_EXISTING_PROFILE_COUNT = 742
EXPECTED_TRIAL_COUNT = 10
MIN_TRIAL_DEPARTMENTS = 3
MAX_FAILURE_RATIO = 0.30
LARGE_BYTES = 200 * 1024
LARGE_WIDTH = 800
MAX_OWNER_REPORT_BYTES = 5 * 1024 * 1024
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
    "PR #58 owner comment 2026-08-16T11:49:02Z: "
    "TRIAL 通过 + FULL_APPEND_AND_OBSIDIAN"
)

SAMPLE_PLAN = (
    ("张晓红", "正高"),
    ("张炎", "正高"),
    ("吴玲玲", "正高"),
    ("李名安", "副高"),
    ("唐新意", "副高"),
    ("巴俊慧", "中级"),
    ("杨婷", "中级"),
    ("周攀", "初级"),
    ("黄晓飞", "初级"),
    ("李舣婷", "初级"),
)

PRIMARY_TITLES = (
    "一级主任医师",
    "副主任中医师",
    "主任中医师",
    "主治中医师",
    "副主任医师",
    "主任医师",
    "主治医师",
    "住院医师",
    "副主任技师",
    "主任技师",
    "主管技师",
    "副主任药师",
    "主任药师",
    "主管药师",
    "助理研究员",
    "副研究员",
    "研究员",
    "副教授",
    "教授",
    "医师",
)

PLACEHOLDER_MARKERS = (
    "placeholder",
    "default",
    "avatar",
    "head-logo",
    "header-logo",
    "footer-logo",
    "naoz",
    "chuzhen",
    "fuwu",
    "wx1",
    "wx2",
    "qrcode",
    "qr-code",
    "cloud-hospital",
    "幻灯片",
    "官网各科室专家介绍封面图",
)

PAGE_TITLE_ALIAS_BY_SOURCE = {
    "https://www.zssy.com.cn/node/6008": "内科ICU",
    "https://www.zssy.com.cn/node/14062": "外科ICU",
    "https://www.zssy.com.cn/node/14071": "精神（心理）科",
    "https://www.zssy.com.cn/node/14068": "口腔医学中心",
    "https://www.zssy.com.cn/node/14098": "变态反应（过敏）学科",
    "https://www.zssy.com.cn/node/11316": "甲状腺、乳腺外科",
    "https://www.zssy.com.cn/node/15410": "神经外科（天河）",
    "https://www.zssy.com.cn/node/15466": "精神（心理）科",
    "https://www.zssy.com.cn/node/30221": "针灸专科（脑病方向）",
}

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
    match = re.fullmatch(r"/node/(\d+)", parsed.path)
    return match.group(1) if match else ""


def safe_photo_part(value: Any) -> str:
    text = re.sub(r'[\\/:*?"<>|]', "_", clean_text(value)).strip(" .")
    return text or "未标注"


def atomic_department(row: dict[str, Any]) -> str:
    value = clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
    atoms = [clean_text(item) for item in re.split(r"[、,，;/；|]+", value) if clean_text(item)]
    chinese_atoms = [item for item in atoms if re.search(r"[\u4e00-\u9fff]", item)]
    return safe_photo_part(chinese_atoms[-1] if chinese_atoms else (atoms[0] if atoms else "未标注"))


def primary_title(value: Any) -> str:
    text = clean_text(value)
    for title in PRIMARY_TITLES:
        if title in text:
            return title
    return "未标注"


def title_level(value: Any) -> str:
    title = primary_title(value)
    if title in {"一级主任医师", "主任医师", "主任中医师", "主任技师", "主任药师", "研究员", "教授"}:
        return "正高"
    if title in {"副主任医师", "副主任中医师", "副主任技师", "副主任药师", "副研究员", "副教授"}:
        return "副高"
    if title in {"主治医师", "主治中医师", "主管技师", "主管药师", "助理研究员"}:
        return "中级"
    if title in {"住院医师", "医师"}:
        return "初级"
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
    if any(name != "itok" or not item for name, item in query) or len(query) > 1:
        return ""
    lowered = unquote(parsed.path).lower()
    if any(marker in lowered for marker in PLACEHOLDER_MARKERS):
        return ""
    return absolute


def style_background_url(value: Any) -> str:
    match = re.search(
        r"background-image\s*:\s*url\(\s*(['\"]?)([^)'\"]+)\1\s*\)",
        str(value or ""),
        flags=re.IGNORECASE,
    )
    return clean_text(match.group(2)) if match else ""


class PhysicianPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._div_left_stack: list[bool] = []
        self._in_title = False
        self._title_parts: list[str] = []
        self.media_attrs: list[dict[str, str]] = []

    @property
    def title(self) -> str:
        return clean_text(" ".join(self._title_parts))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {name: str(value or "") for name, value in attrs}
        if tag.lower() == "title":
            self._in_title = True
            return
        if tag.lower() != "div":
            return
        classes = set(clean_text(attrs_dict.get("class")).split())
        parent_is_left = self._div_left_stack[-1] if self._div_left_stack else False
        in_left = parent_is_left or "physician-details-left" in classes
        self._div_left_stack.append(in_left)
        if in_left and "media-img" in classes:
            self.media_attrs.append(attrs_dict)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False
        elif tag.lower() == "div" and self._div_left_stack:
            self._div_left_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)


@dataclass(frozen=True)
class PortraitReference:
    page_title: str
    photo_url: str
    source_attribute: str


def inspect_portrait_reference(html: str, source_link: str, expected_name: str) -> tuple[str, PortraitReference | None]:
    if not detail_id(source_link):
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    parser = PhysicianPageParser()
    parser.feed(html)
    expected_title = f"{clean_text(expected_name)} | {HOSPITAL}"
    if parser.title != expected_title:
        raise RuntimeError(
            f"详情标题与底表不一致：底表={expected_name} 官网={parser.title or '空'} {source_link}"
        )
    if not parser.media_attrs:
        return "无照片容器", None
    if len(parser.media_attrs) != 1:
        raise RuntimeError(
            f"医生详情区 media-img 不唯一：{source_link} 数量={len(parser.media_attrs)}"
        )
    attrs = parser.media_attrs[0]
    data_value = clean_text(attrs.get("data-image-url"))
    style_value = style_background_url(attrs.get("style"))
    candidates = [value for value in (data_value, style_value) if value]
    if not candidates:
        return "无照片容器", None
    normalized = [page_referenced_photo_url(value, source_link) for value in candidates]
    if not all(normalized):
        raw_path = " ".join(unquote(urlparse(urljoin(source_link, value)).path).lower() for value in candidates)
        if any(marker in raw_path for marker in PLACEHOLDER_MARKERS):
            return "占位图", None
        raise RuntimeError(f"页面引用照片 URL 越界：{source_link} {candidates}")
    if len(set(normalized)) != 1:
        raise RuntimeError(f"data-image-url 与 background-image 不一致：{source_link}")
    return "", PortraitReference(
        page_title=parser.title,
        photo_url=normalized[0],
        source_attribute="data-image-url" if data_value else "inline background-image",
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
                    content = response.read()
                    return (
                        int(response.status),
                        response.headers.get_content_type(),
                        response.headers.get_content_charset() or "utf-8",
                        content,
                    )
            except IncompleteRead as exc:
                if attempt == 0:
                    self.incomplete_read_retry_count += 1
                    continue
                raise RuntimeError(
                    f"官网响应连续两次传输不完整：{url} "
                    f"已读 {len(exc.partial)} bytes，缺少 {exc.expected} bytes"
                ) from exc
            except HTTPError as exc:
                content = exc.read()
                return (
                    int(exc.code),
                    exc.headers.get_content_type(),
                    exc.headers.get_content_charset() or "utf-8",
                    content,
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
        result[str(path)] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    return result


def tree_snapshot(root: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    count = 0
    total_bytes = 0
    if root.is_dir():
        for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix()):
            relative = path.relative_to(root).as_posix().encode("utf-8")
            content = path.read_bytes()
            digest.update(relative + b"\0" + content)
            count += 1
            total_bytes += len(content)
    return {"exists": root.is_dir(), "file_count": count, "bytes": total_bytes, "sha256": digest.hexdigest()}


def protected_snapshot() -> dict[str, Any]:
    return {
        "master_assets": file_snapshot(
            [MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH, MASTER_REPORT_PATH]
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
        raise RuntimeError("Issue #57 TRIAL 范围内已有照片字段，需 owner 先裁决")
    sources = [clean_text(row.get("来源链接")) for row in rows]
    if len(sources) != len(set(sources)):
        raise RuntimeError("Issue #57 范围来源链接不唯一")
    invalid = [source for source in sources if not detail_id(source)]
    if invalid:
        raise RuntimeError("Issue #57 范围存在非授权详情链接：" + "、".join(invalid[:5]))
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
    levels = {title_level(row.get("职称身份原文")) for row in result}
    if len(departments) < MIN_TRIAL_DEPARTMENTS:
        raise RuntimeError(f"科室覆盖不足：{len(departments)}")
    if levels != {"正高", "副高", "中级", "初级"}:
        raise RuntimeError(f"职称分层覆盖不完整：{sorted(levels)}")
    return result


def allocate_trial_photo(row: dict[str, Any], extension: str, content: bytes) -> tuple[str, Path]:
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
    columns = 2
    cell_width = 500
    cell_height = 520
    rows = (len(samples) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_width, rows * cell_height), "white")
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
        draw.rectangle((left, top, left + cell_width - 1, top + cell_height - 1), outline="#B7C0C8", width=2)
        draw.text((left + 20, top + 410), f"{index + 1}. {sample['name']}｜{sample['title']}", fill="black", font=font)
        draw.text((left + 20, top + 448), sample["department"], fill="#333333", font=small_font)
        draw.text((left + 20, top + 482), f"{sample['width']}×{sample['height']}｜{sample['bytes']} bytes", fill="#555555", font=small_font)
    canvas.save(CONTACT_SHEET_PATH, format="JPEG", quality=90, optimize=True)


def write_manifest(rows: list[dict[str, Any]]) -> None:
    fields = [
        "姓名",
        "科室",
        "职称层级",
        "主职称",
        "来源链接",
        "详情HTTP",
        "照片链接",
        "照片HTTP",
        "文件名",
        "字节",
        "SHA-256",
        "魔数",
        "宽",
        "高",
        "大图判定",
    ]
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|").replace("\n", " ")


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    rows = []
    for sample in payload["photo_samples"]:
        rows.append(
            "| {name} | {department} | {level} | {title} | {filename} | {bytes} | {width}×{height} | `{sha256}` | {photo_url} |".format(
                name=markdown_cell(sample["name"]),
                department=markdown_cell(sample["department"]),
                level=sample["title_level"],
                title=markdown_cell(sample["title"]),
                filename=markdown_cell(sample["filename"]),
                bytes=sample["bytes"],
                width=sample["width"],
                height=sample["height"],
                sha256=sample["sha256"],
                photo_url=sample["photo_url"],
            )
        )
    protected_rows = []
    for path, facts in meta["protected_assets_before"]["master_assets"].items():
        protected_rows.append(f"| `{path}` | {facts['bytes']} | `{facts['sha256']}` |")
    level_text = "、".join(f"{key} {value}" for key, value in meta["title_level_counts"].items())
    report = f"""# Issue #57 {HOSPITAL}照片补录 TRIAL 报告

> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 生成日期：{meta['run_date']}
> 视觉复核：`{meta['visual_review_status']}`

## 范围与抽样

- 总底表目标范围：{meta['scope_count']} 行；照片链接/照片文件均为空；来源链接唯一 {meta['scope_unique_source_count']}。
- 固定样本：{meta['trial_detail_count']} 位，覆盖 {meta['department_coverage_count']} 个科室；职称分层为 {level_text}。
- 详情页：HTTP 200 为 {meta['detail_http_200_count']}/{meta['trial_detail_count']}；无照片容器 {meta['no_photo_container_count']}；占位图 {meta['placeholder_count']}；结构异常 {meta['structure_mismatch_count']}。
- 熔断三态合计 {meta['fuse_problem_count']}/{meta['trial_detail_count']}（{meta['fuse_problem_ratio']:.1%}），未超过 owner 规定的 30% 门槛。
- 常规会话仅记录 Cookie 名称：{', '.join(meta['cookie_names']) or '无'}；不记录 Cookie 值。照片请求均携带对应详情页 Referer。

## 实图、命名与容量

- 实图：{meta['photo_sample_count']} 张；全部保存页面自身引用的官网响应原始字节，未压缩。
- 总字节：{meta['photo_total_bytes']}；平均：{meta['photo_average_bytes']} bytes。
- 按平均值对 780 行线性估算：{meta['estimated_full_bytes']} bytes（约 {meta['estimated_full_mib']:.2f} MiB）；仅供 owner 裁决，不代表 FULL 最终可得数或实际容量。
- 单张 >200KB：{meta['over_200kb_count']}/{meta['photo_sample_count']}；宽 >800px：{meta['over_800px_count']}/{meta['photo_sample_count']}。
- 页面未引用路径构造/探测请求：0；第三方来源：0。

| 姓名 | 科室 | 层级 | 主职称 | 文件名 | 字节 | 尺寸 | SHA-256 | 页面引用照片 |
|---|---|---|---|---|---:|---:|---|---|
{chr(10).join(rows)}

详细 HTTP、魔数和逐图命名清单见：`{TRIAL_CSV_PATH}` 与 `{TRIAL_JSON_PATH}`。

## 视觉判定标准与复核

1. 本人职业照：必须位于该医生 `.physician-details-left .physician-details-media .media-img` 内，详情标题与底表姓名一致，照片由 `data-image-url` 或同容器内联 `background-image` 明确引用；联系表中视觉上为单人成人职业照。
2. 占位图：路径含 default/avatar/placeholder 等标记、多个医生重复同一 SHA-256、或视觉为站点通用图/云上三院入口图/期刊二维码时拒绝。
3. 站点通用图：即使位于同页，只要不属于医生左侧详情容器，或是“脑病服务、出诊、服务、云上三院、二维码”等功能图，均不采纳。
4. 联系表：`{CONTACT_SHEET_PATH}`；当前状态为 `{meta['visual_review_status']}`。

## 受保护正式资产零变更

| 文件 | 字节 | SHA-256 |
|---|---:|---|
{chr(10).join(protected_rows)}

- 本院画像树：{meta['protected_assets_before']['profile_tree']['file_count']} 个文件，SHA-256 `{meta['protected_assets_before']['profile_tree']['sha256']}`。
- 本院正式照片目录执行前后状态一致：{json.dumps(meta['protected_assets_before']['formal_photo_tree'], ensure_ascii=False)}。
- TRIAL 照片只写入 `work` 下独立目录：`{TRIAL_PHOTO_DIR}`；未写总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件完成后停止，等待 owner 审计照片质量、样本大图分布和 780 行容量估算。未取得 owner 明确 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填三载体、刷新画像或写正式照片目录。
"""
    TRIAL_REPORT_PATH.write_text(report, encoding="utf-8")


def validate_payload(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    errors: list[str] = []
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围不是 780 行")
    if meta.get("trial_detail_count") != EXPECTED_TRIAL_COUNT:
        errors.append("详情样本不是 10 位")
    if meta.get("department_coverage_count", 0) < MIN_TRIAL_DEPARTMENTS:
        errors.append("科室覆盖不足 3 个")
    if set(meta.get("title_level_counts", {})) != {"正高", "副高", "中级", "初级"}:
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
        if not page_referenced_photo_url(sample.get("photo_url"), sample.get("source_link")):
            errors.append(f"照片 URL 越界：{path.name}")
        filenames.add(path.name.casefold())
    if len(filenames) != meta.get("photo_sample_count"):
        errors.append("照片文件名覆盖或数量不一致")
    if not CONTACT_SHEET_PATH.is_file():
        errors.append("联系表不存在")
    if errors:
        raise RuntimeError("Issue #57 TRIAL 门禁失败：" + "；".join(errors))


def run_trial(run_date: str) -> dict[str, Any]:
    protected_before = protected_snapshot()
    scope_rows = load_scope_rows()
    trial_rows = select_trial_rows(scope_rows)
    session = OfficialSession()
    home_status, _, _, _ = session.get(OFFICIAL_HOME)
    if home_status != 200:
        raise RuntimeError(f"官网首页常规会话建立失败：HTTP {home_status}")

    detail_errors: list[dict[str, Any]] = []
    structure_mismatches: list[dict[str, Any]] = []
    failure_states: list[dict[str, Any]] = []
    portrait_rows: list[tuple[dict[str, Any], PortraitReference, int]] = []
    for row in trial_rows:
        source_link = clean_text(row.get("来源链接"))
        status, content_type, charset, content = session.get(source_link, DIRECTORY_URL)
        if status != 200 or content_type != "text/html":
            detail_errors.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "status": status, "content_type": content_type}
            )
            continue
        html = content.decode(charset, errors="replace")
        try:
            failure_state, portrait = inspect_portrait_reference(html, source_link, clean_text(row.get("姓名")))
        except RuntimeError as exc:
            structure_mismatches.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "error": str(exc)}
            )
            continue
        if failure_state or portrait is None:
            failure_states.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "state": failure_state or "未知"}
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
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "photo_url": portrait.photo_url, "status": photo_status}
            )
            continue
        extension = magic_extension(content, content_type)
        if not extension:
            photo_errors.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "photo_url": portrait.photo_url, "error": f"非受支持图片：{content_type}"}
            )
            continue
        try:
            width, height = image_dimensions(content)
            filename, path = allocate_trial_photo(row, extension, content)
            if not path.exists():
                path.write_bytes(content)
        except Exception as exc:  # noqa: BLE001 - retain exact per-image evidence
            photo_errors.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "photo_url": portrait.photo_url, "error": str(exc)}
            )
            continue
        digest = hashlib.sha256(content).hexdigest()
        large_reasons = []
        if len(content) > LARGE_BYTES:
            large_reasons.append(">200KB")
        if width > LARGE_WIDTH:
            large_reasons.append("宽>800px")
        sample = {
            "name": clean_text(row.get("姓名")),
            "department": atomic_department(row),
            "title_level": title_level(row.get("职称身份原文")),
            "title": primary_title(row.get("职称身份原文")),
            "detail_id": detail_id(source_link),
            "source_link": source_link,
            "detail_http_status": detail_status,
            "photo_url": portrait.photo_url,
            "photo_source_attribute": portrait.source_attribute,
            "photo_http_status": photo_status,
            "content_type": content_type,
            "filename": filename,
            "disk_path": str(path),
            "bytes": len(content),
            "sha256": digest,
            "magic_hex": content[:12].hex().upper(),
            "width": width,
            "height": height,
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
                "详情HTTP": detail_status,
                "照片链接": portrait.photo_url,
                "照片HTTP": photo_status,
                "文件名": filename,
                "字节": len(content),
                "SHA-256": digest,
                "魔数": sample["magic_hex"],
                "宽": width,
                "高": height,
                "大图判定": "、".join(large_reasons) or "未命中",
            }
        )

    build_contact_sheet(photo_samples)
    protected_after = protected_snapshot()
    fuse_problem_count = len(detail_errors) + len(structure_mismatches) + len(failure_states) + len(photo_errors)
    fuse_ratio = fuse_problem_count / EXPECTED_TRIAL_COUNT
    if fuse_ratio > MAX_FAILURE_RATIO:
        raise RuntimeError(
            f"[FATAL - HUMAN_INTERVENTION_REQUIRED] TRIAL 熔断问题超过 30%：{fuse_problem_count}/{EXPECTED_TRIAL_COUNT}"
        )
    total_bytes = sum(sample["bytes"] for sample in photo_samples)
    average_bytes = total_bytes // max(1, len(photo_samples))
    estimated_full = average_bytes * EXPECTED_SCOPE_COUNT
    title_counts = Counter(title_level(row.get("职称身份原文")) for row in trial_rows)
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "phase": "TRIAL_READY_FOR_OWNER_AUDIT",
            "hospital": HOSPITAL,
            "run_date": run_date,
            "scope_count": len(scope_rows),
            "scope_unique_source_count": len({clean_text(row.get("来源链接")) for row in scope_rows}),
            "trial_detail_count": len(trial_rows),
            "department_coverage_count": len({atomic_department(row) for row in trial_rows}),
            "covered_departments": sorted({atomic_department(row) for row in trial_rows}),
            "title_level_counts": {level: title_counts[level] for level in ("正高", "副高", "中级", "初级")},
            "home_http_status": home_status,
            "cookie_names": session.cookie_names,
            "detail_http_200_count": len(portrait_rows) + len(failure_states),
            "no_photo_container_count": sum(item["state"] == "无照片容器" for item in failure_states),
            "placeholder_count": sum(item["state"] == "占位图" for item in failure_states),
            "structure_mismatch_count": len(structure_mismatches),
            "detail_error_count": len(detail_errors),
            "photo_error_count": len(photo_errors),
            "photo_sample_count": len(photo_samples),
            "fuse_problem_count": fuse_problem_count,
            "fuse_problem_ratio": fuse_ratio,
            "photo_total_bytes": total_bytes,
            "photo_average_bytes": average_bytes,
            "estimated_full_count": EXPECTED_SCOPE_COUNT,
            "estimated_full_bytes": estimated_full,
            "estimated_full_mib": estimated_full / 1024 / 1024,
            "over_200kb_count": sum(sample["bytes"] > LARGE_BYTES for sample in photo_samples),
            "over_800px_count": sum(sample["width"] > LARGE_WIDTH for sample in photo_samples),
            "constructed_unreferenced_probe_count": 0,
            "third_party_source_count": 0,
            "visual_review_status": "PENDING_MANUAL_CONTACT_SHEET_REVIEW",
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
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(manifest_rows)
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
                raise RuntimeError(f"发现 Issue #57 范围外行修改：{source} {column}")
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
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 FULL 报告

> 日期：{meta['run_date']}
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`
> 照片政策：`OWNER_APPROVED_PAGE_REFERENCED_ORIGINAL_BYTES`

## 四数对账

| 应采 | 实采 | 失败 | 留空 |
|---:|---:|---:|---:|
| {meta['expected_count']} | {meta['downloaded_count']} | {meta['failed_count']} | {meta['blank_count']} |

| 失败三态 | 数量 |
|---|---:|
{failure_lines}

- 详情不可达率：{meta['detail_unreachable_count']}/{meta['expected_count']}（{meta['detail_unreachable_rate']:.2%}），未超过 10% 熔断线。
- 照片总字节：{meta['photo_total_bytes']} bytes（{meta['photo_total_mib']:.2f} MiB）。
- 最大单张：{meta['photo_max_bytes']} bytes；超过 5 MiB：{meta['over_5mib_count']} 张。
- 页面未引用路径的构造/探测请求：0；第三方来源：0。
- 传输不完整原样重试：{meta['incomplete_read_retry_count']} 次；每个请求至多重试 1 次。
- 780 页只读普查固化的官网标题别名映射：{meta['page_title_alias_count']} 条；仅用于校验来源页身份，不修改底表姓名等字段。
- 总底表：payload/CSV/XLSX 三载体行数与 25 列逐值一致；仅目标行照片两列及失败行异常提示允许变化。
- 画像：既有 {meta['existing_profile_count']} 份画像中，成功实采且有既有画像的 {meta['profile_refreshed_count']} 份只新增照片嵌入区块；{meta['no_profile_scope_count']} 条无画像行不新建画像；索引未改。

## 工件

- `{FULL_JSON_PATH}`
- `{FULL_CSV_PATH}`
- `{FULL_REPORT_PATH}`

## 合规边界

1. 只访问 780 条既有医院官网来源链接及页面自身引用的 `.physician-details-media .media-img` 公开照片。
2. 使用官网首页建立的常规 Cookie 会话和对应详情页 Referer；页面引用原始字节保存，不压缩。
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
        raise RuntimeError("FULL 应采/实采/失败/留空未形成四数闭环")
    state_counts = Counter(meta.get("failure_state_counts") or {})
    if (
        set(state_counts) - set(FULL_FAILURE_STATES)
        or sum(state_counts.values()) != failed
    ):
        raise RuntimeError("FULL 失败三态分布不闭合")
    unreachable = int(meta.get("detail_unreachable_count") or 0)
    if (
        unreachable != state_counts.get("详情不可达", 0)
        or unreachable / expected > 0.10
    ):
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] 详情不可达率超过 10% 或计数不一致"
        )
    if int(meta.get("constructed_unreferenced_probe_count") or 0) != 0:
        raise RuntimeError("FULL 发生页面未引用路径探测")
    if int(meta.get("third_party_source_count") or 0) != 0:
        raise RuntimeError("FULL 发生第三方来源访问")
    if int(meta.get("existing_profile_count") or 0) != EXPECTED_EXISTING_PROFILE_COUNT:
        raise RuntimeError("FULL 既有画像数量漂移")
    if int(meta.get("no_profile_scope_count") or 0) != (
        EXPECTED_SCOPE_COUNT - EXPECTED_EXISTING_PROFILE_COUNT
    ):
        raise RuntimeError("FULL 无画像范围数量漂移")
    if int(meta.get("page_title_alias_count") or 0) != len(
        PAGE_TITLE_ALIAS_BY_SOURCE
    ):
        raise RuntimeError("FULL 官网标题别名映射数量漂移")

    reconciliation = payload.get("reconciliation", [])
    rows = payload.get("rows", [])
    photos = payload.get("photo_samples", [])
    if (
        len(reconciliation) != expected
        or len(rows) != expected
        or len(photos) != downloaded
    ):
        raise RuntimeError("FULL 780 行对账工件数量不一致")
    rows_by_source = {clean_text(row.get("来源链接")): row for row in rows}
    photos_by_source = {
        clean_text(item.get("source_link")): item for item in photos
    }
    if len(rows_by_source) != expected or len(photos_by_source) != downloaded:
        raise RuntimeError("FULL 来源链接对账不唯一")

    expected_files: set[str] = set()
    total_bytes = 0
    max_bytes = 0
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
            if (
                not clean_text(row.get("照片链接"))
                or not clean_text(row.get("照片文件"))
            ):
                raise RuntimeError(f"FULL 实采行照片字段为空：{source}")
            photo = photos_by_source[source]
            filename = clean_text(photo.get("filename"))
            disk_path = photo_root / filename
            content = disk_path.read_bytes()
            if len(content) != int(photo.get("bytes") or 0):
                raise RuntimeError(f"照片字节数对账失败：{filename}")
            if hashlib.sha256(content).hexdigest() != photo.get("sha256"):
                raise RuntimeError(f"照片 SHA-256 对账失败：{filename}")
            expected_extension = disk_path.suffix.lower().lstrip(".")
            content_type = (
                "image/jpeg"
                if expected_extension == "jpg"
                else f"image/{expected_extension}"
            )
            if magic_extension(content, content_type) != expected_extension:
                raise RuntimeError(f"照片魔数与扩展名不符：{filename}")
            if image_dimensions(content) != (
                int(photo.get("width") or 0),
                int(photo.get("height") or 0),
            ):
                raise RuntimeError(f"照片尺寸对账失败：{filename}")
            if len(content) > MAX_OWNER_REPORT_BYTES:
                raise RuntimeError(f"单张照片超过 5 MiB，需先回报 owner：{filename}")
            expected_files.add(filename)
            total_bytes += len(content)
            max_bytes = max(max_bytes, len(content))
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
    if int(meta.get("over_5mib_count") or 0) != 0:
        raise RuntimeError("FULL 存在超过 5 MiB 未回报照片")


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
        staging = target.with_name(f".{target.name}.issue57.tmp")
        if staging.exists():
            staging.unlink()
        shutil.copy2(source, staging)
        staging.replace(target)


def restore_file_targets(backups: dict[Path, Path | None]) -> None:
    for target, backup in backups.items():
        staging = target.with_name(f".{target.name}.issue57.restore")
        if staging.exists():
            staging.unlink()
        if backup is None:
            target.unlink(missing_ok=True)
            continue
        shutil.copy2(backup, staging)
        staging.replace(target)


def run_full(run_date: str) -> dict[str, Any]:
    import collect_official_doctors_batch as collector
    import generate_obsidian_profiles as profiles

    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("FULL 前正式照片目录已存在，拒绝覆盖；需 owner 先裁决")
    baseline_protected = file_snapshot([LEDGER_PATH, MASTER_REPORT_PATH])
    master_payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    before_rows = copy.deepcopy(master_payload.get("rows", []))
    scope_rows = load_scope_rows()
    target_sources = {clean_text(row.get("来源链接")) for row in scope_rows}
    if len(target_sources) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 固定范围来源链接不是 780 个唯一 node")

    before_profile_paths = profiles.extract_existing_sources(PROFILE_DIR)
    extra_profile_sources = set(before_profile_paths) - target_sources
    if extra_profile_sources:
        raise RuntimeError(
            "既有画像存在 Issue #57 范围外来源："
            + "、".join(sorted(extra_profile_sources)[:5])
        )
    profile_target_sources = target_sources & set(before_profile_paths)
    if len(profile_target_sources) != EXPECTED_EXISTING_PROFILE_COUNT:
        raise RuntimeError(
            "FULL 前既有画像来源数量漂移："
            f"应为 {EXPECTED_EXISTING_PROFILE_COUNT}，实际 {len(profile_target_sources)}"
        )
    no_profile_sources = target_sources - profile_target_sources
    alias_sources = set(PAGE_TITLE_ALIAS_BY_SOURCE)
    if not alias_sources <= target_sources:
        raise RuntimeError("官网标题别名映射越出 Issue #57 固定 780 行范围")
    before_profile_bytes: dict[str, bytes] = {}
    for source in profile_target_sources:
        path = before_profile_paths[source]
        if not profiles.is_auto_generated_profile(path):
            raise RuntimeError(f"发现非自动画像，超出 Issue #57 授权：{path}")
        before_profile_bytes[source] = path.read_bytes()
    before_profile_tree = profile_markdown_tree(PROFILE_DIR)

    session = OfficialSession()
    home_status, _, _, _ = session.get(OFFICIAL_HOME)
    if home_status != 200:
        raise RuntimeError(f"官网首页常规会话建立失败：HTTP {home_status}")

    with tempfile.TemporaryDirectory(prefix="issue57_full_", dir=WORK_DIR) as temporary:
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

        def record_failure(
            row: dict[str, Any], state: str, evidence: str
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
                    "宽": "",
                    "高": "",
                    "错误证据": evidence,
                }
            )
            unreachable = sum(
                item["state"] == "详情不可达" for item in failures
            )
            if unreachable / EXPECTED_SCOPE_COUNT > 0.10:
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] 详情不可达率超过 10%："
                    f"{unreachable}/{EXPECTED_SCOPE_COUNT}"
                )

        for index, row in enumerate(scope_rows, start=1):
            source_link = clean_text(row.get("来源链接"))
            name = clean_text(row.get("姓名"))
            source_id = detail_id(source_link)
            portrait: PortraitReference | None = None
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
            expected_page_name = PAGE_TITLE_ALIAS_BY_SOURCE.get(
                source_link, name
            )
            failure_state, portrait = inspect_portrait_reference(
                html, source_link, expected_page_name
            )
            if failure_state:
                record_failure(row, failure_state, failure_state)
                continue
            if portrait is None:
                raise RuntimeError(f"职业照检查未返回明确结果：{source_link}")
            if source_link in no_profile_sources:
                raise RuntimeError(
                    "GOVERN-1 无画像行发现未归入占位图的媒体，拒绝映射为本人照片："
                    f"{source_link} {portrait.photo_url}"
                )

            try:
                photo_status, photo_type, _, photo_content = session.get(
                    portrait.photo_url, source_link
                )
            except RuntimeError as exc:
                record_failure(row, "详情不可达", f"照片资源请求异常：{exc}")
                continue
            if photo_status != 200:
                record_failure(
                    row, "详情不可达", f"照片资源 HTTP {photo_status}"
                )
                continue
            extension = magic_extension(photo_content, photo_type)
            if not extension:
                record_failure(
                    row,
                    "详情不可达",
                    f"照片响应格式不受支持：{photo_type}",
                )
                continue
            try:
                width, height = image_dimensions(photo_content)
            except Exception as exc:  # noqa: BLE001 - retain exact image evidence
                record_failure(row, "详情不可达", f"照片尺寸无法解析：{exc}")
                continue
            if len(photo_content) > MAX_OWNER_REPORT_BYTES:
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] 单张照片超过 5 MiB，需先回报 owner："
                    f"{name} {len(photo_content)} bytes {portrait.photo_url}"
                )

            filename, disk_path = allocate_full_photo_path(
                row,
                source_id,
                extension,
                temp_photo_dir,
                used_filenames,
            )
            disk_path.write_bytes(photo_content)
            relative_path = (PHOTO_RELATIVE_ROOT / filename).as_posix()
            result_row = dict(row)
            result_row["照片链接"] = portrait.photo_url
            result_row["照片文件"] = relative_path
            result_rows.append(result_row)
            digest = hashlib.sha256(photo_content).hexdigest()
            photo_samples.append(
                {
                    "name": name,
                    "department": atomic_department(row),
                    "title": primary_title(row.get("职称身份原文")),
                    "detail_id": source_id,
                    "source_link": source_link,
                    "photo_url": portrait.photo_url,
                    "photo_source_attribute": portrait.source_attribute,
                    "photo_file": relative_path,
                    "filename": filename,
                    "content_type": photo_type,
                    "bytes": len(photo_content),
                    "width": width,
                    "height": height,
                    "sha256": digest,
                    "disk_path": str(FORMAL_PHOTO_DIR / filename),
                    "has_existing_profile": source_link
                    in profile_target_sources,
                }
            )
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
            raise RuntimeError(f"FULL 结果行不是 780：{len(result_rows)}")
        updated_by_source = {
            clean_text(row.get("来源链接")): row for row in result_rows
        }
        after_rows = [
            copy.deepcopy(
                updated_by_source.get(clean_text(row.get("来源链接")), row)
            )
            for row in before_rows
        ]
        row_diffs = collect_full_row_diffs(
            before_rows, after_rows, target_sources
        )
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
        profile_refresh_sources = success_sources & profile_target_sources
        after_profile_paths = profiles.extract_existing_sources(temp_hospital_dir)
        photo_by_source = {
            clean_text(item.get("source_link")): item for item in photo_samples
        }
        for source in profile_refresh_sources:
            before_path = before_profile_paths[source]
            after_path = after_profile_paths.get(source)
            if after_path is None or after_path.name != before_path.name:
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
            for source in profile_refresh_sources
        }
        validate_profile_tree_surgical(
            before_profile_tree,
            temp_hospital_dir,
            expected_changed_profile_paths,
        )

        state_counter = Counter(item["state"] for item in failures)
        total_bytes = sum(int(item["bytes"]) for item in photo_samples)
        max_bytes = max(
            (int(item["bytes"]) for item in photo_samples), default=0
        )
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
                "failure_state_counts": {
                    state: state_counter.get(state, 0)
                    for state in FULL_FAILURE_STATES
                },
                "detail_unreachable_count": state_counter.get(
                    "详情不可达", 0
                ),
                "detail_unreachable_rate": state_counter.get(
                    "详情不可达", 0
                )
                / EXPECTED_SCOPE_COUNT,
                "photo_total_bytes": total_bytes,
                "photo_total_mib": total_bytes / 1024 / 1024,
                "photo_max_bytes": max_bytes,
                "over_5mib_count": sum(
                    int(item["bytes"]) > MAX_OWNER_REPORT_BYTES
                    for item in photo_samples
                ),
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "cookie_names": session.cookie_names,
                "incomplete_read_retry_count": session.incomplete_read_retry_count,
                "existing_profile_count": len(profile_target_sources),
                "no_profile_scope_count": EXPECTED_SCOPE_COUNT
                - len(profile_target_sources),
                "profile_refreshed_count": len(profile_refresh_sources),
                "profile_not_created_count": len(
                    success_sources - profile_target_sources
                ),
                "profile_index_replacement_required": False,
                "page_title_alias_count": len(PAGE_TITLE_ALIAS_BY_SOURCE),
                "row_diff_count": len(row_diffs),
                "row_diff_columns": dict(
                    Counter(item["列名"] for item in row_diffs)
                ),
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
        for source in profile_refresh_sources:
            file_map[before_profile_paths[source]] = after_profile_paths[source]

        backups = backup_file_targets(
            list(file_map), temp_root / "file_backups"
        )
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
            final_profile_paths = profiles.extract_existing_sources(PROFILE_DIR)
            if set(final_profile_paths) != profile_target_sources:
                raise RuntimeError("FULL 落盘后画像来源集合发生变化")
            for source in profile_refresh_sources:
                item = photo_by_source[source]
                validate_profile_photo_only_bytes(
                    before_profile_bytes[source],
                    final_profile_paths[source].read_bytes(),
                    clean_text(item.get("name")),
                    clean_text(item.get("photo_file")),
                )
            validate_profile_tree_surgical(
                before_profile_tree,
                PROFILE_DIR,
                expected_changed_profile_paths,
            )
            if file_snapshot([LEDGER_PATH, MASTER_REPORT_PATH]) != baseline_protected:
                raise RuntimeError("FULL 触碰了入口台账或总底表更新报告")
            with FULL_CSV_PATH.open(
                "r", encoding="utf-8-sig", newline=""
            ) as handle:
                if len(list(csv.DictReader(handle))) != EXPECTED_SCOPE_COUNT:
                    raise RuntimeError("FULL 照片对账 CSV 不是 780 行")
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
    parser = argparse.ArgumentParser(description="Issue #57 中山三院照片补录")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--trial-only", action="store_true", help="执行固定 10 位 TRIAL")
    mode.add_argument(
        "--full-apply",
        action="store_true",
        help="按 PR #58 owner FULL 授权执行 780 行照片回填与既有画像外科式刷新",
    )
    parser.add_argument("--run-date", default=date.today().isoformat())
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.validate_only:
        path = FULL_JSON_PATH if FULL_JSON_PATH.exists() else TRIAL_JSON_PATH
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("meta", {}).get("phase") == "FULL_READY_FOR_FINAL_OWNER_AUDIT":
            validate_full_payload(payload, FORMAL_PHOTO_DIR)
            photos = payload["meta"]["downloaded_count"]
        else:
            validate_payload(payload)
            photos = payload["meta"]["photo_sample_count"]
        print(
            json.dumps(
                {"status": "validated", "photos": photos}, ensure_ascii=False
            )
        )
        return
    if args.full_apply:
        payload = run_full(args.run_date)
        print(
            json.dumps(
                {
                    "mode": "photo_backfill_full",
                    "issue": ISSUE_NUMBER,
                    "hospital": HOSPITAL,
                    "expected": payload["meta"]["expected_count"],
                    "downloaded": payload["meta"]["downloaded_count"],
                    "failed": payload["meta"]["failed_count"],
                    "blank": payload["meta"]["blank_count"],
                    "failure_states": payload["meta"]["failure_state_counts"],
                    "photo_total_bytes": payload["meta"]["photo_total_bytes"],
                    "profiles_refreshed": payload["meta"]["profile_refreshed_count"],
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
    if not args.trial_only:
        raise RuntimeError("必须显式指定 --trial-only 或 --full-apply")
    payload = run_trial(args.run_date)
    print(json.dumps(payload["meta"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
