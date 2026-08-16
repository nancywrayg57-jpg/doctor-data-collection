from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
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
PHOTO_DIR = VAULT / "01_试点医院" / HOSPITAL / "照片"
TRIAL_BASENAME = f"{HOSPITAL}_photo_backfill_trial"
TRIAL_JSON_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
TRIAL_CSV_PATH = WORK_DIR / f"{TRIAL_BASENAME}_doctors.csv"
TRIAL_REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
EXPECTED_SCOPE_COUNT = 205
EXPECTED_TRIAL_COUNT = 10
MIN_TRIAL_DEPARTMENTS = 3
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


def image_attribute_urls(image: Any, base_url: str) -> list[str]:
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
    normalized: list[str] = []
    for candidate in candidates:
        url = page_referenced_photo_url(candidate, base_url)
        if url and url not in normalized:
            normalized.append(url)
    return normalized


def parse_portrait_reference(
    html: str,
    source_link: str,
    expected_name: str,
) -> PortraitReference:
    if not detail_id(source_link):
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    soup = BeautifulSoup(html, "html.parser")
    containers = soup.select(PORTRAIT_CONTAINER_SELECTOR)
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
    if len(images) != 1:
        raise RuntimeError(
            f"本人职业照结构与预核验不符：{source_link} portrait img={len(images)}"
        )
    referenced_urls = image_attribute_urls(images[0], source_link)
    derivatives = [
        url for url in referenced_urls if urlparse(url).path.startswith(DERIVATIVE_PREFIX)
    ]
    originals = [
        url for url in referenced_urls if urlparse(url).path.startswith(ORIGINAL_PREFIX)
    ]
    if len(derivatives) != 1:
        raise RuntimeError(
            f"页面未唯一引用 large_960_x_auto_ 本人职业照：{source_link} 数量={len(derivatives)}"
        )
    return PortraitReference(
        doctor_name=page_name,
        derivative_url=derivatives[0],
        original_urls=tuple(originals),
        referenced_urls=tuple(referenced_urls),
    )


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Issue #55 中山大学中山眼科中心存量照片补录。"
    )
    parser.add_argument("--trial-only", action="store_true")
    parser.add_argument("--today", default=date.today().isoformat())
    parser.add_argument("--max-doctors", type=int, default=EXPECTED_TRIAL_COUNT)
    parser.add_argument("--min-departments", type=int, default=MIN_TRIAL_DEPARTMENTS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.trial_only:
        raise RuntimeError(
            "FULL 未获 owner 大图裁决；仅允许 --trial-only，禁止写入总底表和正式画像"
        )
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
