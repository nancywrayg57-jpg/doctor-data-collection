from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import shutil
import tempfile
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as exc:
    raise SystemExit(
        "缺少依赖：需要 requests、beautifulsoup4。请使用已安装这些库的本机 Python 运行。"
    ) from exc


ROOT = Path(r"D:\workspace\信息收集整理")
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "中山大学中山眼科中心"
ISSUE_NUMBER = 55
MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_JSON_PATH = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_REPORT_PATH = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
LEDGER_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"
PHOTO_DIR = VAULT / "01_试点医院" / HOSPITAL / "照片"
TRIAL_BASENAME = f"{HOSPITAL}_photo_backfill_trial"
TRIAL_JSON_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
TRIAL_CSV_PATH = WORK_DIR / f"{TRIAL_BASENAME}_doctors.csv"
TRIAL_REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
FULL_BASENAME = f"{HOSPITAL}_photo_backfill_full"
FULL_JSON_PATH = WORK_DIR / f"{FULL_BASENAME}_payload.json"
FULL_CSV_PATH = WORK_DIR / f"{FULL_BASENAME}_reconciliation.csv"
FULL_REPORT_PATH = WORK_DIR / f"{FULL_BASENAME}_report.md"
EXPECTED_SCOPE_COUNT = 205
EXPECTED_TRIAL_COUNT = 10
MIN_TRIAL_DEPARTMENTS = 3
MAX_OWNER_REPORT_BYTES = 5 * 1024 * 1024
OFFICIAL_HOST = "gzzoc.org.cn"
PORTRAIT_SELECTOR = ".showcase-5-0 .showcase-media img"
PORTRAIT_CONTAINER_SELECTOR = ".showcase-5-0"
DERIVATIVE_PREFIX = (
    "/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/"
    "styles/large_960_x_auto_/public/"
)
ORIGINAL_PREFIX = "/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/public/"
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
    "event-hero",
)
FULL_FAILURE_STATES = ("详情不可达", "无照片元素", "占位图")
FULL_WARNING_BY_STATE = {
    state: f"官网本人职业照补录失败：{state}" for state in FULL_FAILURE_STATES
}
FULL_ALLOWED_ROW_COLUMNS = {"照片链接", "照片文件", "异常提示"}


@dataclass(frozen=True)
class PortraitReference:
    doctor_name: str
    derivative_url: str
    original_urls: tuple[str, ...]
    referenced_urls: tuple[str, ...]


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def comparable_host(value: str) -> str:
    host = (urlparse(value).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def detail_id(value: str) -> str:
    parsed = urlparse(clean_text(value))
    if (
        parsed.scheme not in {"http", "https"}
        or comparable_host(value) != OFFICIAL_HOST
        or parsed.query
        or parsed.fragment
    ):
        return ""
    match = re.fullmatch(r"/node/(\d+)", parsed.path)
    return match.group(1) if match else ""


def page_referenced_photo_url(value: str | None, base_url: str) -> str:
    raw = clean_text(value)
    if not raw:
        return ""
    absolute = urljoin(base_url, raw)
    parsed = urlparse(absolute)
    if (
        parsed.scheme not in {"http", "https"}
        or comparable_host(absolute) != OFFICIAL_HOST
        or parsed.fragment
        or not parsed.path.startswith(
            "/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/"
        )
    ):
        return ""
    query = parse_qsl(parsed.query, keep_blank_values=True)
    if any(name != "itok" or not value for name, value in query) or len(query) > 1:
        return ""
    lowered = parsed.path.lower()
    if any(marker in lowered for marker in PLACEHOLDER_MARKERS):
        return ""
    return absolute


def raw_image_attribute_urls(image: Any) -> list[str]:
    candidates: list[str] = []
    for attribute in ("src", "data-src", "data-original"):
        value = image.get(attribute)
        if value:
            candidates.append(str(value))
    srcset = clean_text(image.get("srcset"))
    if srcset:
        for part in srcset.split(","):
            url_part = clean_text(part).split(" ", 1)[0]
            if url_part:
                candidates.append(url_part)
    return candidates


def image_attribute_urls(image: Any, base_url: str) -> list[str]:
    normalized: list[str] = []
    for candidate in raw_image_attribute_urls(image):
        url = page_referenced_photo_url(candidate, base_url)
        if url and url not in normalized:
            normalized.append(url)
    return normalized


def inspect_portrait_reference(
    html: str,
    source_link: str,
    expected_name: str,
) -> tuple[str, PortraitReference | None]:
    if not detail_id(source_link):
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    soup = BeautifulSoup(html, "html.parser")
    containers = soup.select(PORTRAIT_CONTAINER_SELECTOR)
    if not containers:
        return "无照片元素", None
    if len(containers) != 1:
        raise RuntimeError(
            f"本人职业照结构与预核验不符：{source_link} showcase 容器={len(containers)}"
        )
    container = containers[0]
    heading = container.select_one("h2")
    page_name = clean_text(heading.get_text(" ", strip=True) if heading else "")
    if not page_name or page_name != clean_text(expected_name):
        raise RuntimeError(
            f"详情姓名与底表不一致：底表={clean_text(expected_name)} 官网={page_name or '空'} {source_link}"
        )
    images = container.select(PORTRAIT_SELECTOR.replace(f"{PORTRAIT_CONTAINER_SELECTOR} ", ""))
    if not images:
        return "无照片元素", None
    if len(images) != 1:
        raise RuntimeError(
            f"本人职业照结构与预核验不符：{source_link} portrait img={len(images)}"
        )
    raw_urls = raw_image_attribute_urls(images[0])
    if not raw_urls:
        return "无照片元素", None
    normalized_raw_urls = [urljoin(source_link, value) for value in raw_urls]
    if any(
        marker in (urlparse(value).path or "").lower()
        for value in normalized_raw_urls
        for marker in PLACEHOLDER_MARKERS
    ):
        return "占位图", None
    referenced_urls = image_attribute_urls(images[0], source_link)
    derivatives = [
        url for url in referenced_urls if urlparse(url).path.startswith(DERIVATIVE_PREFIX)
    ]
    originals = [
        url for url in referenced_urls if urlparse(url).path.startswith(ORIGINAL_PREFIX)
    ]
    if not derivatives:
        raise RuntimeError(f"页面职业照 URL 越界或未引用 large_960_x_auto_：{source_link}")
    if len(derivatives) != 1:
        raise RuntimeError(
            f"页面未唯一引用 large_960_x_auto_ 本人职业照：{source_link} 数量={len(derivatives)}"
        )
    return "", PortraitReference(
        doctor_name=page_name,
        derivative_url=derivatives[0],
        original_urls=tuple(originals),
        referenced_urls=tuple(referenced_urls),
    )


def parse_portrait_reference(
    html: str,
    source_link: str,
    expected_name: str,
) -> PortraitReference:
    failure_state, portrait = inspect_portrait_reference(html, source_link, expected_name)
    if failure_state or portrait is None:
        raise RuntimeError(
            f"本人职业照结构与预核验不符：{source_link} 状态={failure_state or '未知'}"
        )
    return portrait


def primary_title(value: Any) -> str:
    text = clean_text(value)
    for title in PRIMARY_TITLES:
        if title in text:
            return title
    return "未标注"


def safe_photo_part(value: Any) -> str:
    text = re.sub(r'[\\/:*?"<>|]', "_", clean_text(value)).strip(" .")
    return text or "未标注"


def atomic_department(row: dict[str, Any]) -> str:
    value = clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
    return safe_photo_part(re.split(r"[、,，;/；|]+", value, maxsplit=1)[0])


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


def image_dimensions(content: bytes, extension: str) -> tuple[int, int]:
    if extension == "png" and len(content) >= 24:
        return int.from_bytes(content[16:20], "big"), int.from_bytes(content[20:24], "big")
    if extension == "gif" and len(content) >= 10:
        return int.from_bytes(content[6:8], "little"), int.from_bytes(content[8:10], "little")
    if extension == "jpg" and content.startswith(b"\xff\xd8"):
        offset = 2
        sof_markers = {
            0xC0,
            0xC1,
            0xC2,
            0xC3,
            0xC5,
            0xC6,
            0xC7,
            0xC9,
            0xCA,
            0xCB,
            0xCD,
            0xCE,
            0xCF,
        }
        while offset + 8 < len(content):
            if content[offset] != 0xFF:
                offset += 1
                continue
            marker = content[offset + 1]
            if marker in sof_markers:
                height = int.from_bytes(content[offset + 5 : offset + 7], "big")
                width = int.from_bytes(content[offset + 7 : offset + 9], "big")
                return width, height
            if marker in {0xD8, 0xD9}:
                offset += 2
                continue
            segment_length = int.from_bytes(content[offset + 2 : offset + 4], "big")
            if segment_length < 2:
                break
            offset += 2 + segment_length
    if extension == "webp" and len(content) >= 30 and content[:4] == b"RIFF":
        if content[12:16] == b"VP8X":
            return (
                1 + int.from_bytes(content[24:27], "little"),
                1 + int.from_bytes(content[27:30], "little"),
            )
        if content[12:16] == b"VP8 " and content[23:26] == b"\x9d\x01\x2a":
            return (
                int.from_bytes(content[26:28], "little") & 0x3FFF,
                int.from_bytes(content[28:30], "little") & 0x3FFF,
            )
    return 0, 0


def snapshot(paths: list[Path]) -> dict[str, dict[str, Any]]:
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


def load_scope_rows(path: Path = MASTER_JSON_PATH) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = [
        dict(row)
        for row in payload.get("rows", [])
        if clean_text(row.get("医院")) == HOSPITAL
        and not clean_text(row.get("照片文件"))
    ]
    if len(rows) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError(
            f"Issue #{ISSUE_NUMBER} 范围漂移：应为 {EXPECTED_SCOPE_COUNT} 行，实际 {len(rows)} 行"
        )
    if any(clean_text(row.get("照片链接")) for row in rows):
        raise RuntimeError("照片文件为空范围内存在非空照片链接，需 owner 先裁决")
    source_links = [clean_text(row.get("来源链接")) for row in rows]
    if len(source_links) != len(set(source_links)):
        raise RuntimeError("Issue 范围内来源链接不唯一")
    invalid_links = [link for link in source_links if not detail_id(link)]
    if invalid_links:
        raise RuntimeError("存在非授权官网详情链接：" + "、".join(invalid_links[:5]))
    return rows


def select_trial_rows(rows: list[dict[str, Any]], count: int) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    selected_sources: set[str] = set()
    seen_departments: set[str] = set()
    for row in rows:
        department = clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
        source = clean_text(row.get("来源链接"))
        if department and department not in seen_departments and source not in selected_sources:
            seen_departments.add(department)
            selected_sources.add(source)
            selected.append(dict(row))
            if len(selected) == count:
                return selected
    for row in rows:
        source = clean_text(row.get("来源链接"))
        if source not in selected_sources:
            selected_sources.add(source)
            selected.append(dict(row))
            if len(selected) == count:
                return selected
    raise RuntimeError(f"无法从 {len(rows)} 行中选出 {count} 位唯一详情样本")


def allocate_photo_path(
    row: dict[str, Any],
    detail: str,
    extension: str,
    content: bytes,
    output_dir: Path,
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
    path = output_dir / filename
    if path.exists() and path.read_bytes() != content:
        filename = f"{stem}-{safe_photo_part(detail)}.{extension}"
        path = output_dir / filename
    if path.exists() and path.read_bytes() != content:
        raise RuntimeError(f"照片目标已存在且内容不同，拒绝覆盖：{path}")
    return filename, path


def download_image(
    session: requests.Session,
    photo_url: str,
    source_link: str,
) -> tuple[bytes, str, int, int]:
    response = session.get(
        photo_url,
        headers={"Referer": source_link},
        timeout=35,
    )
    if response.status_code != 200:
        raise RuntimeError(f"照片下载 HTTP {response.status_code}：{photo_url}")
    extension = magic_extension(response.content, response.headers.get("Content-Type"))
    if not extension:
        raise RuntimeError(f"照片响应格式不受支持：{photo_url}")
    width, height = image_dimensions(response.content, extension)
    if width <= 0 or height <= 0:
        raise RuntimeError(f"照片尺寸无法解析：{photo_url}")
    return response.content, extension, width, height


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BASE_HEADERS)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in BASE_HEADERS} for row in rows)


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|")


def write_report(path: Path, payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    photo_lines = "\n".join(
        "| {name} | {department} | {title} | {detail_id} | {filename} | {bytes} | "
        "{width}×{height} | `{sha256}` | {derivative_url} | {original} |".format(
            name=markdown_cell(item["name"]),
            department=markdown_cell(item["department"]),
            title=markdown_cell(item["title"]),
            detail_id=item["detail_id"],
            filename=markdown_cell(item["filename"]),
            bytes=item["bytes"],
            width=item["width"],
            height=item["height"],
            sha256=item["sha256"],
            derivative_url=item["derivative_url"],
            original=item["page_referenced_original_url"] or "页面未引用，不请求",
        )
        for item in payload["photo_samples"]
    )
    protected_lines = "\n".join(
        f"| `{file_path}` | {facts['bytes']} | `{facts['sha256']}` |"
        for file_path, facts in meta["protected_assets_after"].items()
    )
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 TRIAL 报告

> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 照片政策：`WAITING_OWNER_DERIVATIVE_OR_ORIGINAL_DECISION`
> 生成日期：{meta['run_date']}

## 范围与结果

- 总底表照片文件为空范围：{meta['scope_count']} 行；来源链接唯一：{meta['scope_unique_source_count']}。
- TRIAL：{meta['trial_row_count']} 位，覆盖 {meta['department_coverage_count']} 个科室；详情失败 {meta['detail_error_count']}，结构不符 {meta['structure_mismatch_count']}，照片失败 {meta['photo_error_count']}。
- 样本实图：{meta['photo_sample_count']} 张，均保留官网响应原始字节，不压缩；字节数、SHA-256、魔数和尺寸已核验。
- 页面实际引用的 `large_960_x_auto_` 派生图：{meta['derivative_reference_count']}；同一职业照容器实际引用的原图 URL：{meta['page_referenced_original_count']}。
- 原图路径探测请求：{meta['constructed_original_probe_count']}。页面未引用的原图 URL 未构造、未请求，不能给出虚假的原图字节估算。
- 派生图平均大小：{meta['derivative_average_bytes']} bytes；按 205 行线性估算：{meta['derivative_estimated_full_bytes']} bytes（约 {meta['derivative_estimated_full_mib']:.2f} MiB）。
- 原图容量估算：{meta['original_size_estimate_status']}。
- 总底表 payload/CSV/XLSX/更新报告：TRIAL 前后哈希一致，未写入；正式画像未刷新。

## 派生图 / 原图对比与命名清单

| 姓名 | 科室 | 主职称 | 详情 ID | 文件名 | 字节 | 尺寸 | SHA-256 | 页面引用派生图 | 页面引用原图 |
|---|---|---|---:|---|---:|---:|---|---|---|
{photo_lines}

## 大图裁决说明

1. 10 张页面引用派生图均来自详情页本人职业照容器，宽度为 960px，命中“宽度 >800px”的大图裁决门禁。
2. 当前详情 DOM 没有引用同一职业照的原图 URL；按 Issue 红线不得通过移除 `/styles/large_960_x_auto_/` 等方式构造或探测原图。
3. 因此当前可审计的二选一事实为：派生图有真实样本与容量估算；原图在授权 URL 集合中不可得，大小未知。FULL 必须等待 owner 明确裁决使用页面派生图，或由 owner 下发页面自身引用的原图入口。

## 视觉复核

- 联系表：`{CONTACT_SHEET_PATH}`（生成后人工复核）。
- 自动结构门禁只接受与医生姓名同容器的唯一职业照，已排除页头、页尾、预约图和正文插图。
- 患者/儿童影像、占位图、通用图最终仍须以样本实图人工视觉复核为准。

## 受保护资产零变更

| 文件 | 字节 | SHA-256 |
|---|---:|---|
{protected_lines}
"""
    path.write_text(report, encoding="utf-8")


def validate_trial(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    errors: list[str] = []
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围行数不是 205")
    if meta.get("trial_row_count") != EXPECTED_TRIAL_COUNT:
        errors.append("试采不是 10 位")
    if meta.get("department_coverage_count", 0) < MIN_TRIAL_DEPARTMENTS:
        errors.append("科室覆盖不足 3 个")
    if meta.get("detail_error_count"):
        errors.append("存在详情失败")
    if meta.get("structure_mismatch_count"):
        errors.append("存在职业照结构不符")
    if meta.get("photo_error_count"):
        errors.append("存在照片失败")
    if meta.get("photo_sample_count") != EXPECTED_TRIAL_COUNT:
        errors.append("实图样本不是 10 张")
    if meta.get("constructed_original_probe_count") != 0:
        errors.append("发生了页面未引用原图路径探测")
    if meta.get("protected_assets_before") != meta.get("protected_assets_after"):
        errors.append("受保护资产发生变化")
    expected_files: set[str] = set()
    for row, photo in zip(payload.get("rows", []), payload.get("photo_samples", [])):
        if clean_text(row.get("照片链接")) != photo.get("derivative_url"):
            errors.append(f"照片链接对账失败：{row.get('姓名')}")
        if clean_text(row.get("照片文件")) != photo.get("photo_file"):
            errors.append(f"照片文件对账失败：{row.get('姓名')}")
        disk_path = Path(photo.get("disk_path", ""))
        if not disk_path.is_file():
            errors.append(f"照片文件不存在：{disk_path}")
            continue
        content = disk_path.read_bytes()
        if len(content) != photo.get("bytes"):
            errors.append(f"照片字节对账失败：{disk_path.name}")
        if hashlib.sha256(content).hexdigest() != photo.get("sha256"):
            errors.append(f"照片 SHA-256 对账失败：{disk_path.name}")
        extension = magic_extension(content, f"image/{disk_path.suffix.lstrip('.')}")
        if extension != disk_path.suffix.lower().lstrip("."):
            errors.append(f"照片魔数与扩展名不符：{disk_path.name}")
        width, height = image_dimensions(content, extension)
        if (width, height) != (photo.get("width"), photo.get("height")):
            errors.append(f"照片尺寸对账失败：{disk_path.name}")
        expected_files.add(disk_path.name.casefold())
    if len(expected_files) != EXPECTED_TRIAL_COUNT:
        errors.append("照片文件名发生覆盖")
    if errors:
        raise RuntimeError("Issue #55 TRIAL 门禁失败：" + "；".join(errors))


def run_trial(
    run_date: str,
    max_doctors: int = EXPECTED_TRIAL_COUNT,
    min_departments: int = MIN_TRIAL_DEPARTMENTS,
) -> dict[str, Any]:
    if max_doctors != EXPECTED_TRIAL_COUNT or min_departments < MIN_TRIAL_DEPARTMENTS:
        raise RuntimeError("Issue #55 TRIAL 固定为 10 位且至少覆盖 3 个科室")
    protected_paths = [
        MASTER_JSON_PATH,
        MASTER_CSV_PATH,
        MASTER_XLSX_PATH,
        MASTER_REPORT_PATH,
    ]
    protected_before = snapshot(protected_paths)
    scope_rows = load_scope_rows()
    trial_rows = select_trial_rows(scope_rows, max_doctors)
    covered_departments = sorted(
        {
            clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
            for row in trial_rows
            if clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
        }
    )
    if len(covered_departments) < min_departments:
        raise RuntimeError(
            f"科室覆盖门禁不满足：要求至少 {min_departments}，实际 {len(covered_departments)}"
        )

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36; "
                "public official-site photo backfill trial"
            )
        }
    )
    detail_pages: list[tuple[dict[str, Any], PortraitReference]] = []
    detail_errors: list[dict[str, str]] = []
    structure_mismatches: list[dict[str, str]] = []
    for row in trial_rows:
        source_link = clean_text(row.get("来源链接"))
        try:
            response = session.get(source_link, timeout=35)
        except requests.RequestException as exc:
            detail_errors.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "error": str(exc)}
            )
            continue
        if response.status_code != 200:
            detail_errors.append(
                {
                    "name": clean_text(row.get("姓名")),
                    "source_link": source_link,
                    "error": f"HTTP {response.status_code}",
                }
            )
            continue
        response.encoding = response.apparent_encoding or response.encoding or "utf-8"
        try:
            portrait = parse_portrait_reference(
                response.text,
                source_link,
                clean_text(row.get("姓名")),
            )
        except RuntimeError as exc:
            structure_mismatches.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "error": str(exc)}
            )
            continue
        detail_pages.append((row, portrait))

    if len(detail_errors) / max(1, len(trial_rows)) > 0.10:
        raise RuntimeError(
            f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 详情页不可达率超过 10%："
            f"{len(detail_errors)}/{len(trial_rows)}"
        )
    if structure_mismatches:
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] 照片元素结构与预核验不符："
            + "；".join(item["error"] for item in structure_mismatches)
        )
    if detail_errors:
        raise RuntimeError("TRIAL 存在详情失败，未下载照片：" + json.dumps(detail_errors, ensure_ascii=False))

    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    result_rows: list[dict[str, Any]] = []
    photo_samples: list[dict[str, Any]] = []
    photo_errors: list[dict[str, str]] = []
    for row, portrait in detail_pages:
        source_link = clean_text(row.get("来源链接"))
        source_id = detail_id(source_link)
        try:
            content, extension, width, height = download_image(
                session,
                portrait.derivative_url,
                source_link,
            )
            filename, disk_path = allocate_photo_path(
                row,
                source_id,
                extension,
                content,
                PHOTO_DIR,
            )
            if not disk_path.exists():
                disk_path.write_bytes(content)
        except Exception as exc:  # noqa: BLE001 - keep exact per-photo evidence
            photo_errors.append(
                {
                    "name": clean_text(row.get("姓名")),
                    "source_link": source_link,
                    "photo_url": portrait.derivative_url,
                    "error": str(exc),
                }
            )
            continue
        relative_path = (PHOTO_RELATIVE_ROOT / filename).as_posix()
        result_row = dict(row)
        result_row["照片链接"] = portrait.derivative_url
        result_row["照片文件"] = relative_path
        result_rows.append(result_row)
        original_url = portrait.original_urls[0] if portrait.original_urls else ""
        photo_samples.append(
            {
                "name": clean_text(row.get("姓名")),
                "department": atomic_department(row),
                "title": primary_title(row.get("职称身份原文")),
                "detail_id": source_id,
                "source_link": source_link,
                "derivative_url": portrait.derivative_url,
                "page_referenced_original_url": original_url,
                "page_referenced_url_count": len(portrait.referenced_urls),
                "photo_file": relative_path,
                "filename": filename,
                "bytes": len(content),
                "width": width,
                "height": height,
                "sha256": hashlib.sha256(content).hexdigest(),
                "disk_path": str(disk_path),
            }
        )

    protected_after = snapshot(protected_paths)
    derivative_total = sum(item["bytes"] for item in photo_samples)
    derivative_average = derivative_total // max(1, len(photo_samples))
    estimated_full = derivative_average * EXPECTED_SCOPE_COUNT
    page_referenced_original_count = sum(
        bool(item["page_referenced_original_url"]) for item in photo_samples
    )
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
            "trial_row_count": len(result_rows),
            "department_coverage_count": len(covered_departments),
            "covered_departments": covered_departments,
            "detail_error_count": len(detail_errors),
            "structure_mismatch_count": len(structure_mismatches),
            "photo_error_count": len(photo_errors),
            "photo_sample_count": len(photo_samples),
            "derivative_reference_count": len(photo_samples),
            "page_referenced_original_count": page_referenced_original_count,
            "constructed_original_probe_count": 0,
            "derivative_total_bytes": derivative_total,
            "derivative_average_bytes": derivative_average,
            "derivative_estimated_full_count": EXPECTED_SCOPE_COUNT,
            "derivative_estimated_full_bytes": estimated_full,
            "derivative_estimated_full_mib": estimated_full / 1024 / 1024,
            "original_size_estimate_status": (
                "页面未引用原图 URL，按红线未请求，大小未知"
                if page_referenced_original_count == 0
                else "页面引用原图 URL 待 owner 明确授权下载比较"
            ),
            "photo_policy_status": "WAITING_OWNER_DERIVATIVE_OR_ORIGINAL_DECISION",
            "visual_review_status": "PENDING_MANUAL_CONTACT_SHEET_REVIEW",
            "third_party_source_count": 0,
            "protected_assets_before": protected_before,
            "protected_assets_after": protected_after,
            "json_path": str(TRIAL_JSON_PATH),
            "csv_path": str(TRIAL_CSV_PATH),
            "report_path": str(TRIAL_REPORT_PATH),
            "contact_sheet_path": str(CONTACT_SHEET_PATH),
        },
        "detail_errors": detail_errors,
        "structure_mismatches": structure_mismatches,
        "photo_errors": photo_errors,
        "photo_samples": photo_samples,
        "rows": result_rows,
    }
    validate_trial(payload)
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_csv(TRIAL_CSV_PATH, result_rows)
    write_report(TRIAL_REPORT_PATH, payload)
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
    if filename in used_filenames:
        filename = f"{stem}-{safe_photo_part(source_id)}.{extension}"
    if filename in used_filenames or (output_dir / filename).exists():
        raise RuntimeError(f"照片命名仍冲突，拒绝覆盖：{filename}")
    used_filenames.add(filename)
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
                raise RuntimeError(f"发现 Issue #55 范围外行修改：{source} {column}")
    unexpected = sorted({item["列名"] for item in diffs} - FULL_ALLOWED_ROW_COLUMNS)
    if unexpected:
        raise RuntimeError("发现范围外字段修改：" + "、".join(unexpected))
    return diffs


def recompute_failure_derivatives(
    payload: dict[str, Any],
    rows: list[dict[str, Any]],
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


def validate_master_layers(
    payload_path: Path,
    csv_path: Path,
    xlsx_path: Path,
) -> list[dict[str, Any]]:
    import generate_obsidian_profiles as profiles

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    payload_rows = payload.get("rows", [])
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    # The project basic reader closes its ZipFile eagerly. The openpyxl read-only
    # path keeps a Windows handle alive until GC and prevents transaction temp
    # cleanup after validation.
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
> 照片政策：`OWNER_APPROVED_PAGE_REFERENCED_LARGE_960_ORIGINAL_BYTES`

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
- 页面未引用原图的构造/探测请求：0。
- 总底表：payload/CSV/XLSX 三载体行数与 25 列逐值一致；仅目标行照片两列及失败行异常提示允许变化。
- 画像：成功实采对应自动画像仅新增照片嵌入区块；失败留空画像保持不变；索引文件名与链接集合无需变化。

## 工件

- `{FULL_JSON_PATH}`
- `{FULL_CSV_PATH}`
- `{FULL_REPORT_PATH}`

## 合规边界

1. 只访问 205 条既有医院官网来源链接及页面自身引用的 `large_960_x_auto_` 公开资源。
2. `itok` 与 Referer 按 owner 指令原样使用；响应原始字节保存，不压缩。
3. 禁止构造或探测页面未引用的原图；禁止患者、儿童、合影、占位图或通用图入库。
4. 失败仅按“详情不可达 / 无照片元素 / 占位图”留空并追加异常提示。
"""
    path.write_text(report, encoding="utf-8", newline="\n")


def validate_full_payload(payload: dict[str, Any], photo_root: Path) -> None:
    meta = payload.get("meta", {})
    expected = int(meta.get("expected_count") or 0)
    downloaded = int(meta.get("downloaded_count") or 0)
    failed = int(meta.get("failed_count") or 0)
    blank = int(meta.get("blank_count") or 0)
    if expected != EXPECTED_SCOPE_COUNT or downloaded + failed != expected or blank != failed:
        raise RuntimeError("FULL 应采/实采/失败/留空未形成四数闭环")
    state_counts = Counter(meta.get("failure_state_counts") or {})
    if set(state_counts) - set(FULL_FAILURE_STATES) or sum(state_counts.values()) != failed:
        raise RuntimeError("FULL 失败三态分布不闭合")
    unreachable = int(meta.get("detail_unreachable_count") or 0)
    if unreachable != state_counts.get("详情不可达", 0) or unreachable / expected > 0.10:
        raise RuntimeError("[FATAL - HUMAN_INTERVENTION_REQUIRED] 详情不可达率超过 10% 或计数不一致")

    reconciliation = payload.get("reconciliation", [])
    rows = payload.get("rows", [])
    photos = payload.get("photo_samples", [])
    if len(reconciliation) != expected or len(rows) != expected or len(photos) != downloaded:
        raise RuntimeError("FULL 205 行对账工件数量不一致")
    rows_by_source = {clean_text(row.get("来源链接")): row for row in rows}
    photos_by_source = {clean_text(item.get("source_link")): item for item in photos}
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
            if not clean_text(row.get("照片链接")) or not clean_text(row.get("照片文件")):
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
            content_type = "image/jpeg" if expected_extension == "jpg" else f"image/{expected_extension}"
            extension = magic_extension(content, content_type)
            if extension != expected_extension:
                raise RuntimeError(f"照片魔数与扩展名不符：{filename}")
            if image_dimensions(content, extension) != (
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
    markdown_path = "/".join(
        Path(photo_file.replace("\\", "/")).parts[-2:]
    )
    if not markdown_path.startswith("照片/"):
        raise RuntimeError(f"画像照片相对路径越界：{photo_file}")
    return markdown_path


def insert_profile_photo_block(
    before_text: str,
    doctor_name: str,
    photo_file: str,
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
    before_bytes: bytes,
    doctor_name: str,
    photo_file: str,
) -> bytes:
    bom = b"\xef\xbb\xbf" if before_bytes.startswith(b"\xef\xbb\xbf") else b""
    body = before_bytes[len(bom) :]
    try:
        before_text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"画像不是有效 UTF-8：{doctor_name}") from exc
    after_text = insert_profile_photo_block(before_text, doctor_name, photo_file)
    return bom + after_text.encode("utf-8")


def validate_profile_photo_only(
    before_text: str,
    after_text: str,
    doctor_name: str,
    photo_file: str,
) -> None:
    markdown_path = profile_photo_markdown_path(photo_file)
    newline = "\r\n" if "\r\n" in after_text else "\n"
    photo_block = f"![{doctor_name}]({markdown_path}){newline}{newline}"
    if after_text.count(photo_block) != 1:
        raise RuntimeError(f"画像照片嵌入区块不唯一：{doctor_name}")
    if after_text != insert_profile_photo_block(before_text, doctor_name, photo_file):
        raise RuntimeError(f"画像出现照片嵌入区块以外变化：{doctor_name}")


def validate_profile_photo_only_bytes(
    before_bytes: bytes,
    after_bytes: bytes,
    doctor_name: str,
    photo_file: str,
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
    targets: list[Path],
    backup_root: Path,
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
        staging = target.with_name(f".{target.name}.issue55.tmp")
        if staging.exists():
            staging.unlink()
        shutil.copy2(source, staging)
        staging.replace(target)


def restore_file_targets(backups: dict[Path, Path | None]) -> None:
    for target, backup in backups.items():
        staging = target.with_name(f".{target.name}.issue55.restore")
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

    baseline_protected = snapshot([LEDGER_PATH, MASTER_REPORT_PATH])
    master_payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    before_rows = copy.deepcopy(master_payload.get("rows", []))
    scope_rows = load_scope_rows()
    target_sources = {clean_text(row.get("来源链接")) for row in scope_rows}
    if len(target_sources) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 固定范围来源链接不是 205 个唯一 node")

    formal_hospital_dir = PHOTO_DIR.parent
    before_profile_paths = profiles.extract_existing_sources(formal_hospital_dir)
    missing_profiles = sorted(target_sources - set(before_profile_paths))
    if missing_profiles:
        raise RuntimeError("FULL 前缺少既有自动画像：" + "、".join(missing_profiles[:5]))
    before_profile_bytes: dict[str, bytes] = {}
    for source in target_sources:
        path = before_profile_paths[source]
        if not profiles.is_auto_generated_profile(path):
            raise RuntimeError(f"发现非自动画像，超出 Issue #55 授权：{path}")
        before_profile_bytes[source] = path.read_bytes()
    before_profile_tree = profile_markdown_tree(formal_hospital_dir)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36; "
                "public official-site photo backfill full"
            )
        }
    )

    with tempfile.TemporaryDirectory(prefix="issue55_full_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_photo_dir = temp_root / "photos"
        temp_photo_dir.mkdir()
        temp_profile_root = temp_root / "profiles"
        shutil.copytree(formal_hospital_dir, temp_profile_root / HOSPITAL)
        used_filenames: set[str] = set()
        result_rows: list[dict[str, Any]] = []
        photo_samples: list[dict[str, Any]] = []
        failures: list[dict[str, str]] = []
        reconciliation: list[dict[str, Any]] = []
        original_reference_count = 0

        for row in scope_rows:
            source_link = clean_text(row.get("来源链接"))
            name = clean_text(row.get("姓名"))
            source_id = detail_id(source_link)
            failure_state = ""
            error_evidence = ""
            portrait: PortraitReference | None = None
            try:
                response = session.get(source_link, timeout=35)
            except requests.RequestException as exc:
                failure_state = "详情不可达"
                error_evidence = f"详情请求异常：{exc}"
            else:
                if response.status_code != 200:
                    failure_state = "详情不可达"
                    error_evidence = f"详情 HTTP {response.status_code}"
                else:
                    response.encoding = response.apparent_encoding or response.encoding or "utf-8"
                    failure_state, portrait = inspect_portrait_reference(
                        response.text,
                        source_link,
                        name,
                    )
                    if failure_state:
                        error_evidence = failure_state

            if failure_state:
                result_row = dict(row)
                result_row["照片链接"] = ""
                result_row["照片文件"] = ""
                result_row["异常提示"] = append_failure_warning(
                    result_row.get("异常提示"), failure_state
                )
                result_rows.append(result_row)
                failures.append(
                    {
                        "name": name,
                        "source_link": source_link,
                        "state": failure_state,
                        "error": error_evidence,
                    }
                )
                reconciliation.append(
                    {
                        "姓名": name,
                        "来源链接": source_link,
                        "状态": "失败",
                        "失败三态": failure_state,
                        "照片链接": "",
                        "照片文件": "",
                        "字节数": "",
                        "SHA-256": "",
                        "宽": "",
                        "高": "",
                        "错误证据": error_evidence,
                    }
                )
                unreachable = sum(item["state"] == "详情不可达" for item in failures)
                if unreachable / EXPECTED_SCOPE_COUNT > 0.10:
                    raise RuntimeError(
                        "[FATAL - HUMAN_INTERVENTION_REQUIRED] 详情不可达率超过 10%："
                        f"{unreachable}/{EXPECTED_SCOPE_COUNT}"
                    )
                continue

            if portrait is None:
                raise RuntimeError(f"职业照检查未返回明确结果：{source_link}")
            original_reference_count += int(bool(portrait.original_urls))
            try:
                content, extension, width, height = download_image(
                    session,
                    portrait.derivative_url,
                    source_link,
                )
            except (requests.RequestException, RuntimeError) as exc:
                failure_state = "详情不可达"
                error_evidence = f"照片资源不可达：{exc}"
                result_row = dict(row)
                result_row["照片链接"] = ""
                result_row["照片文件"] = ""
                result_row["异常提示"] = append_failure_warning(
                    result_row.get("异常提示"), failure_state
                )
                result_rows.append(result_row)
                failures.append(
                    {
                        "name": name,
                        "source_link": source_link,
                        "state": failure_state,
                        "error": error_evidence,
                    }
                )
                reconciliation.append(
                    {
                        "姓名": name,
                        "来源链接": source_link,
                        "状态": "失败",
                        "失败三态": failure_state,
                        "照片链接": "",
                        "照片文件": "",
                        "字节数": "",
                        "SHA-256": "",
                        "宽": "",
                        "高": "",
                        "错误证据": error_evidence,
                    }
                )
                unreachable = sum(item["state"] == "详情不可达" for item in failures)
                if unreachable / EXPECTED_SCOPE_COUNT > 0.10:
                    raise RuntimeError(
                        "[FATAL - HUMAN_INTERVENTION_REQUIRED] 详情不可达率超过 10%："
                        f"{unreachable}/{EXPECTED_SCOPE_COUNT}"
                    )
                continue
            if len(content) > MAX_OWNER_REPORT_BYTES:
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] 单张照片超过 5 MiB，需先回报 owner："
                    f"{name} {len(content)} bytes {portrait.derivative_url}"
                )
            filename, disk_path = allocate_full_photo_path(
                row,
                source_id,
                extension,
                temp_photo_dir,
                used_filenames,
            )
            disk_path.write_bytes(content)
            relative_path = (PHOTO_RELATIVE_ROOT / filename).as_posix()
            result_row = dict(row)
            result_row["照片链接"] = portrait.derivative_url
            result_row["照片文件"] = relative_path
            result_rows.append(result_row)
            digest = hashlib.sha256(content).hexdigest()
            photo_samples.append(
                {
                    "name": name,
                    "department": atomic_department(row),
                    "title": primary_title(row.get("职称身份原文")),
                    "detail_id": source_id,
                    "source_link": source_link,
                    "derivative_url": portrait.derivative_url,
                    "page_referenced_original_urls": list(portrait.original_urls),
                    "photo_file": relative_path,
                    "filename": filename,
                    "bytes": len(content),
                    "width": width,
                    "height": height,
                    "sha256": digest,
                    "disk_path": str(PHOTO_DIR / filename),
                }
            )
            reconciliation.append(
                {
                    "姓名": name,
                    "来源链接": source_link,
                    "状态": "实采",
                    "失败三态": "",
                    "照片链接": portrait.derivative_url,
                    "照片文件": relative_path,
                    "字节数": len(content),
                    "SHA-256": digest,
                    "宽": width,
                    "高": height,
                    "错误证据": "",
                }
            )

        if len(result_rows) != EXPECTED_SCOPE_COUNT:
            raise RuntimeError(f"FULL 结果行不是 205：{len(result_rows)}")
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
        write_csv(temp_master_csv, after_rows)
        collector.build_workbook(
            temp_master_payload,
            temp_master_xlsx,
            temp_master_preview,
        )
        validate_master_layers(temp_master_payload, temp_master_csv, temp_master_xlsx)

        success_sources = {
            clean_text(item.get("source_link")) for item in photo_samples
        }
        after_profile_paths = profiles.extract_existing_sources(
            temp_profile_root / HOSPITAL
        )
        photo_by_source = {
            clean_text(item.get("source_link")): item for item in photo_samples
        }
        for source in success_sources:
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
            before_profile_paths[source].relative_to(formal_hospital_dir)
            for source in success_sources
        }
        validate_profile_tree_surgical(
            before_profile_tree,
            temp_profile_root / HOSPITAL,
            expected_changed_profile_paths,
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
                "expected_count": EXPECTED_SCOPE_COUNT,
                "downloaded_count": len(photo_samples),
                "failed_count": len(failures),
                "blank_count": len(failures),
                "failure_state_counts": {
                    state: state_counter.get(state, 0) for state in FULL_FAILURE_STATES
                },
                "detail_unreachable_count": state_counter.get("详情不可达", 0),
                "detail_unreachable_rate": state_counter.get("详情不可达", 0)
                / EXPECTED_SCOPE_COUNT,
                "photo_total_bytes": total_bytes,
                "photo_total_mib": total_bytes / 1024 / 1024,
                "photo_max_bytes": max_bytes,
                "over_5mib_count": sum(
                    int(item["bytes"]) > MAX_OWNER_REPORT_BYTES
                    for item in photo_samples
                ),
                "page_referenced_original_count": original_reference_count,
                "constructed_original_probe_count": 0,
                "profile_refreshed_count": len(success_sources),
                "profile_index_replacement_required": False,
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
        for source in success_sources:
            file_map[before_profile_paths[source]] = after_profile_paths[source]

        backups = backup_file_targets(list(file_map), temp_root / "file_backups")
        photo_backup = temp_root / "formal_photo_backup"
        photo_swapped = False
        try:
            ensure_workspace_target(PHOTO_DIR)
            if PHOTO_DIR.exists():
                PHOTO_DIR.replace(photo_backup)
            temp_photo_dir.replace(PHOTO_DIR)
            photo_swapped = True
            apply_file_map(file_map)

            final_rows = validate_master_layers(
                MASTER_JSON_PATH,
                MASTER_CSV_PATH,
                MASTER_XLSX_PATH,
            )
            final_diffs = collect_full_row_diffs(before_rows, final_rows, target_sources)
            if final_diffs != row_diffs:
                raise RuntimeError("FULL 落盘后的逐单元格差异与预期不一致")
            validate_full_payload(full_payload, PHOTO_DIR)
            final_profile_paths = profiles.extract_existing_sources(formal_hospital_dir)
            for source in success_sources:
                item = photo_by_source[source]
                validate_profile_photo_only_bytes(
                    before_profile_bytes[source],
                    final_profile_paths[source].read_bytes(),
                    clean_text(item.get("name")),
                    clean_text(item.get("photo_file")),
                )
            validate_profile_tree_surgical(
                before_profile_tree,
                formal_hospital_dir,
                expected_changed_profile_paths,
            )
            if snapshot([LEDGER_PATH, MASTER_REPORT_PATH]) != baseline_protected:
                raise RuntimeError("FULL 触碰了入口台账或总底表更新报告")
            with FULL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
                if len(list(csv.DictReader(handle))) != EXPECTED_SCOPE_COUNT:
                    raise RuntimeError("FULL 照片对账 CSV 不是 205 行")
        except Exception:
            restore_file_targets(backups)
            if photo_swapped and PHOTO_DIR.exists():
                ensure_workspace_target(PHOTO_DIR)
                shutil.rmtree(PHOTO_DIR)
            if photo_backup.exists():
                photo_backup.replace(PHOTO_DIR)
            raise

        return full_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Issue #55 中山大学中山眼科中心存量照片补录。"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trial-only", action="store_true")
    mode.add_argument(
        "--full-apply",
        action="store_true",
        help="按 2026-08-16 owner 批准的页面派生图原始字节政策执行 205 行 FULL。",
    )
    parser.add_argument("--today", default=date.today().isoformat())
    parser.add_argument("--max-doctors", type=int, default=EXPECTED_TRIAL_COUNT)
    parser.add_argument("--min-departments", type=int, default=MIN_TRIAL_DEPARTMENTS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.full_apply:
        payload = run_full(args.today)
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
    payload = run_trial(args.today, args.max_doctors, args.min_departments)
    print(
        json.dumps(
            {
                "mode": "photo_backfill_trial",
                "issue": ISSUE_NUMBER,
                "hospital": HOSPITAL,
                "rows": payload["meta"]["trial_row_count"],
                "departments": payload["meta"]["department_coverage_count"],
                "photos": payload["meta"]["photo_sample_count"],
                "original_probes": payload["meta"]["constructed_original_probe_count"],
                "json": str(TRIAL_JSON_PATH),
                "csv": str(TRIAL_CSV_PATH),
                "report": str(TRIAL_REPORT_PATH),
                "master_updated": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("用户中断")
    except Exception as exc:  # noqa: BLE001 - CLI should expose exact blocker
        print(f"[ERROR] {exc}", file=__import__("sys").stderr)
        raise SystemExit(1) from exc
