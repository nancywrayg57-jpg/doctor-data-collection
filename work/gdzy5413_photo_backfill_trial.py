from __future__ import annotations

import argparse
import csv
import hashlib
import html as html_module
import json
import re
import statistics
import time
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qsl, urljoin, urlparse

from PIL import Image, ImageDraw, ImageFont, ImageOps

import sys2_photo_backfill_trial as common


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "广东省第二中医院"
ISSUE_NUMBER = 73
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

OFFICIAL_HOME = "https://www.gdzy5413.com/"
DIRECTORY_URL = (
    "https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850"
)
OFFICIAL_HOST = "gdzy5413.com"
EXPECTED_SCOPE_COUNT = 342
EXPECTED_KSDOCTOR_COUNT = 321
EXPECTED_SPECIALIST_COUNT = 21
EXPECTED_TRIAL_COUNT = 10
EXPECTED_PROFILE_MARKDOWN_COUNT = 343
DETAIL_RETRY_SECONDS = 30
MAX_PHOTO_BYTES = 20 * 1024 * 1024
OWNER_REPORT_BYTES = 5 * 1024 * 1024
VISUAL_PASS = "PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10"

BASE_HEADERS = common.BASE_HEADERS

SAMPLE_PLAN = (
    ("靳利利", "specialist", "正高"),
    ("范德辉", "specialist", "正高"),
    ("孙正平", "ksdoctorinfo", "其他"),
    ("周永霞", "ksdoctorinfo", "正高"),
    ("陈伟萍", "ksdoctorinfo", "副高"),
    ("宫静", "ksdoctorinfo", "副高"),
    ("林谋清", "ksdoctorinfo", "其他"),
    ("何宇巍", "ksdoctorinfo", "其他"),
    ("付啸峰", "ksdoctorinfo", "其他"),
    ("唐敏", "ksdoctorinfo", "正高"),
)

PRIMARY_TITLE_TERMS = (
    "一级主任医师",
    "副主任中医师",
    "副主任医师",
    "副主任技师",
    "主任中医师",
    "主任医师",
    "主任技师",
    "主治中医师",
    "主治医师",
    "主管技师",
    "主管药师",
    "主管护师",
    "住院医师",
    "副研究员",
    "研究员",
    "医师",
    "技师",
    "药师",
    "护师",
    "副教授",
    "教授",
)

PLACEHOLDER_MARKERS = (
    "default",
    "placeholder",
    "nopic",
    "no_pic",
    "no-photo",
    "noimage",
    "no-image",
)
KNOWN_PLACEHOLDER_SHA256 = {
    "636b19e12d195b9da003dbbed0c68c0004864d6d86e990f8b606aa069b67b5a9",
}
KNOWN_PUBLIC_ASSET_MARKERS = (
    "20131226040613496",
    "20131226040736895",
    "20250620113738740",
    "20131202104531799",
    "20190325083422870",
)
EXCLUSION_POLICY = (
    {
        "rule": "template-style-assets",
        "match": "path contains /style/images/",
        "reason": "模板 logo、边框、按钮、排班图或装饰图，不在医生照片容器内",
    },
    {
        "rule": "public-navigation-footer-assets",
        "match": "known 就诊指南/专家目录/页脚/二维码 asset identifiers",
        "reason": "全站公共资源，不是医生本人职业照",
    },
    {
        "rule": "empty-upload-path",
        "match": "path is /UploadFiles/image/ without filename",
        "reason": "详情页明确没有照片文件，禁止构造或猜测文件名",
    },
    {
        "rule": "placeholder-name-markers",
        "match": "default/placeholder/nopic/noimage variants",
        "reason": "占位图命名特征，不作为本人职业照",
    },
    {
        "rule": "placeholder-response-content",
        "match": "known placeholder SHA-256 or <=4 KiB small 120×160-class response",
        "reason": "拦截 URL 文件名伪装为医生照片、实际内容为‘暂无图片’的小型合法 JPEG",
    },
    {
        "rule": "outside-doctor-container",
        "match": "image/background reference is outside the authorized template container",
        "reason": "仅采页面本人照片容器实际引用版本，其他页面资源全部排除",
    },
)


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def comparable_host(value: str) -> str:
    host = (urlparse(value).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def detail_template(value: Any) -> str:
    text = clean_text(value)
    parsed = urlparse(text)
    if parsed.scheme != "https" or comparable_host(text) != OFFICIAL_HOST or parsed.fragment:
        return ""
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    if len(pairs) != len({key for key, _ in pairs}):
        return ""
    query = dict(pairs)
    path = parsed.path.lower()
    if path == "/main/doctor/specialist.aspx":
        return "specialist" if set(query) == {"typeid"} and query["typeid"].isdigit() else ""
    if path == "/main/ks/templet2/ksdoctorinfo.aspx":
        required = {"bid", "typeid", "cid", "ksid", "id"}
        return (
            "ksdoctorinfo"
            if set(query) == required and all(query[key].isdigit() for key in required)
            else ""
        )
    return ""


def detail_id(value: Any) -> str:
    template = detail_template(value)
    query = dict(parse_qsl(urlparse(clean_text(value)).query, keep_blank_values=True))
    if template == "specialist":
        return f"specialist-{query['typeid']}"
    if template == "ksdoctorinfo":
        return f"ksdoctorinfo-{query['id']}"
    return ""


def atomic_department(row: dict[str, Any]) -> str:
    value = clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
    atom = re.split(r"[、,，;；/|]", value, maxsplit=1)[0].strip()
    return safe_photo_part(atom)


def primary_title(value: Any) -> str:
    text = clean_text(value)
    matches: list[tuple[int, int, str]] = []
    for term in PRIMARY_TITLE_TERMS:
        position = text.find(term)
        if position >= 0:
            matches.append((position, -len(term), term))
    return min(matches)[2] if matches else "未标注"


def title_level(value: Any) -> str:
    title = primary_title(value)
    if title.startswith("一级主任") or title.startswith("主任"):
        return "正高"
    if title.startswith("副主任"):
        return "副高"
    return "其他"


def safe_photo_part(value: Any) -> str:
    text = clean_text(value) or "未标注"
    return re.sub(r'[<>:"/\\|?*]', "_", text).strip(" .") or "未标注"


def attribute_map(tag: str) -> dict[str, str]:
    return {
        key.lower(): html_module.unescape(value).strip()
        for key, _, value in re.findall(
            r"([:\w-]+)\s*=\s*(['\"])(.*?)\2", tag, flags=re.DOTALL
        )
    }


def html_visible_text(value: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", value)
    return clean_text(html_module.unescape(without_tags))


def all_page_references(page_html: str, source_link: str) -> list[str]:
    references: list[str] = []
    for tag in re.findall(r"<img\b[^>]*>", page_html, flags=re.IGNORECASE | re.DOTALL):
        src = attribute_map(tag).get("src", "")
        references.append(urljoin(source_link, src))
    for raw in re.findall(
        r"background\s*:\s*url\(([^)]+)\)", page_html, flags=re.IGNORECASE
    ):
        references.append(urljoin(source_link, raw.strip(" \t\r\n\"'")))
    return list(dict.fromkeys(references))


def excluded_reason(url: str, accepted_url: str) -> str:
    if url == accepted_url:
        return ""
    parsed = urlparse(url)
    path = parsed.path.lower()
    if path.rstrip("/") == "/uploadfiles/image":
        return "empty-upload-path"
    if "/style/images/" in path:
        return "template-style-assets"
    if any(marker in path for marker in KNOWN_PUBLIC_ASSET_MARKERS):
        return "public-navigation-footer-assets"
    if any(marker in path for marker in PLACEHOLDER_MARKERS):
        return "placeholder-name-markers"
    return "outside-doctor-container"


def page_referenced_photo_url(raw_url: str, source_link: str) -> str:
    absolute = urljoin(source_link, html_module.unescape(clean_text(raw_url)))
    parsed = urlparse(absolute)
    path = parsed.path.lower()
    if (
        parsed.scheme != "https"
        or comparable_host(absolute) != OFFICIAL_HOST
        or parsed.fragment
        or not path.startswith("/uploadfiles/image/")
        or path.rstrip("/") == "/uploadfiles/image"
        or any(marker in path for marker in PLACEHOLDER_MARKERS)
    ):
        return ""
    return absolute


def placeholder_response_reason(content: bytes, width: int, height: int) -> str:
    digest = hashlib.sha256(content).hexdigest()
    if digest in KNOWN_PLACEHOLDER_SHA256:
        return f"known-placeholder-sha256:{digest}"
    if len(content) <= 4 * 1024 and width <= 120 and height <= 160:
        return f"small-placeholder-like-response:{len(content)}B:{width}x{height}"
    return ""


def condense_snippet(value: str, limit: int = 1400) -> str:
    return clean_text(value)[:limit]


def parse_specialist_page(
    page_html: str, source_link: str, expected_name: str
) -> dict[str, Any]:
    name_match = re.search(
        r'<div\b[^>]*class=["\'][^"\']*\bdocimg_title\b[^"\']*["\'][^>]*>'
        r"(.*?)</div>",
        page_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    page_name = html_visible_text(name_match.group(1)) if name_match else ""
    if page_name != expected_name:
        raise RuntimeError(f"specialist 详情姓名不一致：期望 {expected_name}，页面 {page_name or '空'}")
    section_match = re.search(
        r'<div\b[^>]*class=["\'][^"\']*\bmain_left_img\b[^"\']*["\'][^>]*>'
        r"(.*?)"
        r'<div\b[^>]*class=["\'][^"\']*\bkeylist_bg\b',
        page_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not section_match:
        raise RuntimeError(f"specialist 医生照片容器缺失：{source_link}")
    section = section_match.group(1)
    raw_candidates = re.findall(
        r"background\s*:\s*url\(([^)]+)\)", section, flags=re.IGNORECASE
    )
    candidates = [
        page_referenced_photo_url(raw.strip(" \t\r\n\"'"), source_link)
        for raw in raw_candidates
    ]
    candidates = [item for item in candidates if item]
    if len(candidates) != 1:
        raise RuntimeError(
            f"specialist 本人照片引用应恰为 1，实际 {len(candidates)}：{source_link}"
        )
    accepted = candidates[0]
    references = all_page_references(page_html, source_link)
    excluded = [
        {"url": item, "reason": excluded_reason(item, accepted)}
        for item in references
        if excluded_reason(item, accepted)
    ]
    snippet_match = re.search(
        r'<div\b[^>]*class=["\'][^"\']*\bdocimg_title\b[^"\']*["\'][^>]*>.*?</div>'
        r".*?"
        r'<div\b[^>]*style=["\'][^"\']*background\s*:\s*url\([^)]+\)[^"\']*["\'][^>]*>\s*</div>',
        section,
        flags=re.IGNORECASE | re.DOTALL,
    )
    snippet = condense_snippet(snippet_match.group(0) if snippet_match else section)
    return {
        "template": "specialist",
        "page_name": page_name,
        "photo_url": accepted,
        "container_selector": ".main_left_img .docimg_title + .docimg_ming + .docimg_cover + div[style*='background:url']",
        "html_snippet": snippet,
        "candidate_count": len(candidates),
        "excluded_resources": excluded,
        "detection_feature": "main_left_img 内 docimg_title 姓名一致，且恰有一个 inline background:url(/UploadFiles/image/<file>)",
    }


def parse_ksdoctorinfo_page(
    page_html: str, source_link: str, expected_name: str
) -> dict[str, Any]:
    name_match = re.search(r"姓名\s*[：:]\s*([^<\r\n]+)", page_html, flags=re.IGNORECASE)
    page_name = clean_text(html_module.unescape(name_match.group(1))) if name_match else ""
    if page_name != expected_name:
        raise RuntimeError(
            f"ksdoctorinfo 详情姓名不一致：期望 {expected_name}，页面 {page_name or '空'}"
        )
    matching_tags: list[tuple[str, dict[str, str], int]] = []
    for match in re.finditer(r"<img\b[^>]*>", page_html, flags=re.IGNORECASE | re.DOTALL):
        tag = match.group(0)
        attrs = attribute_map(tag)
        if attrs.get("width", "").lower() == "120px" and attrs.get("height", "").lower() == "155px":
            matching_tags.append((tag, attrs, match.start()))
    if len(matching_tags) != 1:
        raise RuntimeError(
            f"ksdoctorinfo 120×155 资料卡照片标签应恰为 1，实际 {len(matching_tags)}：{source_link}"
        )
    tag, attrs, position = matching_tags[0]
    accepted = page_referenced_photo_url(attrs.get("src", ""), source_link)
    if not accepted:
        raise RuntimeError(f"ksdoctorinfo 固定样本无本人照片文件引用：{source_link}")
    start = page_html.rfind("<div", max(0, position - 500), position)
    end = page_html.find("</div>", position)
    snippet = condense_snippet(page_html[start : end + 6] if start >= 0 and end >= 0 else tag)
    references = all_page_references(page_html, source_link)
    excluded = [
        {"url": item, "reason": excluded_reason(item, accepted)}
        for item in references
        if excluded_reason(item, accepted)
    ]
    return {
        "template": "ksdoctorinfo",
        "page_name": page_name,
        "photo_url": accepted,
        "container_selector": "资料卡 div[style*='width: 120px'] > img[width='120px'][height='155px']",
        "html_snippet": snippet,
        "candidate_count": 1,
        "excluded_resources": excluded,
        "detection_feature": "资料卡姓名字段一致，且恰有一个 120px×155px img 指向 /UploadFiles/image/<file>",
    }


def analyze_page(page_html: str, source_link: str, expected_name: str) -> dict[str, Any]:
    template = detail_template(source_link)
    if template == "specialist":
        return parse_specialist_page(page_html, source_link, expected_name)
    if template == "ksdoctorinfo":
        return parse_ksdoctorinfo_page(page_html, source_link, expected_name)
    raise RuntimeError(f"非授权详情模板：{source_link}")


def file_snapshot(paths: list[Path]) -> dict[str, dict[str, Any]]:
    return common.file_snapshot(paths)


def tree_snapshot(root: Path) -> dict[str, Any]:
    return common.tree_snapshot(root)


def protected_snapshot() -> dict[str, Any]:
    return {
        "protected_files": file_snapshot(
            [
                MASTER_JSON_PATH,
                MASTER_CSV_PATH,
                MASTER_XLSX_PATH,
                MASTER_REPORT_PATH,
                LEDGER_JSON_PATH,
                LEDGER_CSV_PATH,
                LEDGER_XLSX_PATH,
            ]
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
        raise RuntimeError(f"本院固定范围应为 {EXPECTED_SCOPE_COUNT}，实际 {len(rows)}")
    links = [clean_text(row.get("来源链接")) for row in rows]
    if len(set(links)) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("本院来源链接不是 342 条唯一固定工作集")
    counts = Counter(detail_template(link) for link in links)
    if counts != Counter(
        {"ksdoctorinfo": EXPECTED_KSDOCTOR_COUNT, "specialist": EXPECTED_SPECIALIST_COUNT}
    ):
        raise RuntimeError(f"本院详情模板分布异常：{dict(counts)}")
    if any(clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")) for row in rows):
        raise RuntimeError("TRIAL 前本院已有照片字段，拒绝覆盖")
    markdown_files = sorted(PROFILE_DIR.glob("*.md"))
    if len(markdown_files) != EXPECTED_PROFILE_MARKDOWN_COUNT:
        raise RuntimeError(
            f"本院画像 Markdown 应为 {EXPECTED_PROFILE_MARKDOWN_COUNT}，实际 {len(markdown_files)}"
        )
    if not (PROFILE_DIR / "_索引.md").is_file():
        raise RuntimeError("本院 _索引.md 缺失")
    doctor_profiles = [path for path in markdown_files if path.name != "_索引.md"]
    if len(doctor_profiles) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("本院医生画像数量与固定工作集不一致")
    marker = b"<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->"
    if any(marker not in path.read_bytes() for path in doctor_profiles):
        raise RuntimeError("本院存在非 AUTO 画像，拒绝进入照片 TRIAL")
    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("TRIAL 前正式照片目录已存在，拒绝覆盖")
    return rows


def select_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for name, template, expected_level in SAMPLE_PLAN:
        matches = [
            row
            for row in rows
            if clean_text(row.get("姓名")) == name
            and detail_template(row.get("来源链接")) == template
        ]
        if len(matches) != 1:
            raise RuntimeError(f"固定样本应唯一：{name}/{template}，实际 {len(matches)}")
        row = matches[0]
        actual_level = title_level(row.get("职称_关键词") or row.get("职称身份原文"))
        if actual_level != expected_level:
            raise RuntimeError(
                f"固定样本职称分层变化：{name} 期望 {expected_level}，实际 {actual_level}"
            )
        selected.append(row)
    template_counts = Counter(detail_template(row.get("来源链接")) for row in selected)
    if template_counts != Counter({"ksdoctorinfo": 8, "specialist": 2}):
        raise RuntimeError(f"固定样本模板分布异常：{dict(template_counts)}")
    departments = [atomic_department(row) for row in selected]
    if len(set(departments)) != EXPECTED_TRIAL_COUNT or "未标注" in departments:
        raise RuntimeError(f"固定样本科室首原子不满足 10 个分散科室：{departments}")
    return selected


def fetch_with_retry(
    session: common.OfficialSession,
    url: str,
    referer: str,
    label: str,
    sleep_func: Callable[[float], None] = time.sleep,
) -> tuple[common.HttpResult, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    last_result: common.HttpResult | None = None
    for attempt in range(2):
        try:
            result = session.get(url, referer=referer)
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
        raise RuntimeError(f"{label} 连续两次非 200：{url} {attempts}")
    raise RuntimeError(f"{label} 连续两次请求失败：{url} {attempts}")


def allocate_trial_photo(
    row: dict[str, Any], extension: str, content: bytes
) -> tuple[str, Path]:
    title_text = row.get("职称_关键词") or row.get("职称身份原文")
    stem = "-".join(
        [
            safe_photo_part(row.get("姓名")),
            atomic_department(row),
            safe_photo_part(primary_title(title_text)),
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
    return common.contact_sheet_font(size)


def build_contact_sheet(samples: list[dict[str, Any]]) -> None:
    cell_width, cell_height = 320, 430
    columns, rows = 5, 2
    sheet = Image.new("RGB", (cell_width * columns, cell_height * rows), "white")
    title_font = contact_sheet_font(20)
    detail_font = contact_sheet_font(14)
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
            f"{sample['template']} | {sample['department']} | {sample['primary_title']}",
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


MANIFEST_FIELDS = [
    "name",
    "department",
    "primary_title",
    "title_level",
    "template",
    "source_link",
    "detail_id",
    "photo_url",
    "filename",
    "disk_path",
    "bytes",
    "sha256",
    "width",
    "height",
    "detail_status",
    "detail_final_url",
    "photo_status",
    "photo_final_url",
    "container_selector",
    "detection_feature",
    "html_snippet",
    "detail_attempts",
    "photo_attempts",
    "excluded_resources",
]


def write_manifest(samples: list[dict[str, Any]]) -> None:
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for sample in samples:
            row = {key: sample.get(key, "") for key in MANIFEST_FIELDS}
            for key in ("detail_attempts", "photo_attempts", "excluded_resources"):
                row[key] = json.dumps(row[key], ensure_ascii=False, separators=(",", ":"))
            writer.writerow(row)


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


def sample_format_metadata(samples: list[dict[str, Any]]) -> tuple[dict[str, int], int]:
    formats = Counter(
        Path(clean_text(sample.get("filename"))).suffix.lstrip(".").lower()
        for sample in samples
    )
    expected_by_content_type = {
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
    }
    mismatch_count = 0
    for sample in samples:
        actual = Path(clean_text(sample.get("filename"))).suffix.lstrip(".").lower()
        reported = expected_by_content_type.get(
            clean_text(sample.get("photo_content_type")).split(";", 1)[0].lower(), ""
        )
        if reported and reported != actual:
            mismatch_count += 1
    return dict(formats), mismatch_count


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    samples = payload["samples"]
    lines = [
        f"# {HOSPITAL}照片补录 TRIAL 报告",
        "",
        f"- GitHub Issue：#{ISSUE_NUMBER}",
        f"- 医院官网：{OFFICIAL_HOME}",
        f"- 医生目录：{DIRECTORY_URL}",
        f"- 固定范围：{meta['scope_count']}（ksdoctorinfo {meta['scope_template_counts']['ksdoctorinfo']} + specialist {meta['scope_template_counts']['specialist']}）",
        f"- TRIAL：{meta['trial_count']} 张页面引用原始响应照片；specialist {meta['trial_template_counts']['specialist']} + ksdoctorinfo {meta['trial_template_counts']['ksdoctorinfo']}",
        f"- 科室首原子：{meta['distinct_department_count']} 个",
        f"- 职称分层：{json.dumps(meta['title_level_counts'], ensure_ascii=False)}",
        f"- 视觉复核：{meta['visual_review']}",
        "",
        "## 两类详情模板结构诊断",
        "",
    ]
    for diagnostic in payload["structure_diagnostics"]:
        lines.extend(
            [
                f"### {diagnostic['template']}",
                "",
                f"- 代表医生：{diagnostic['sample_name']}",
                f"- 代表详情：{diagnostic['source_link']}",
                f"- 容器选择器：`{diagnostic['container_selector']}`",
                f"- URL 特征：{diagnostic['detection_feature']}",
                "- 现场 HTML 片段：",
                "",
                "```html",
                diagnostic["html_snippet"],
                "```",
                "",
            ]
        )
    lines.extend(["## 排除清单", ""])
    for item in payload["exclusion_policy"]:
        lines.append(f"- `{item['rule']}`：{item['match']}；{item['reason']}。")
    lines.extend(
        [
            "",
            "## 样本对账",
            "",
            "| # | 模板 | 姓名 | 科室首原子 | 主职称 | 页面 | 照片 | 字节 | 尺寸 |",
            "|---:|---|---|---|---|---|---|---:|---:|",
        ]
    )
    for index, sample in enumerate(samples, start=1):
        lines.append(
            f"| {index} | {sample['template']} | {sample['name']} | {sample['department']} | "
            f"{sample['primary_title']} | [详情]({sample['source_link']}) | "
            f"[页面引用版本]({sample['photo_url']}) | {sample['bytes']:,} | "
            f"{sample['width']}×{sample['height']} |"
        )
    sizes = [int(sample["bytes"]) for sample in samples]
    lines.extend(
        [
            "",
            "## 字节与验证",
            "",
            f"- 总字节：{sum(sizes):,}",
            f"- 最小/中位数/平均/最大：{min(sizes):,} / {statistics.median(sizes):,.0f} / {statistics.mean(sizes):,.0f} / {max(sizes):,}",
            f"- 大小分桶：{json.dumps(meta['size_buckets'], ensure_ascii=False)}",
            f"- 实际魔数格式：{json.dumps(meta['format_counts'], ensure_ascii=False)}；响应头/魔数格式不一致 {meta['content_type_magic_mismatch_count']} 张，落盘扩展名均跟随实际魔数。",
            f"- 详情页：{meta['detail_success_count']}/{EXPECTED_TRIAL_COUNT} HTTP 200；照片：{meta['photo_success_count']}/{EXPECTED_TRIAL_COUNT} HTTP 200。",
            "- 每张照片均验证最终 host、HTTP、Content-Type、魔数、SHA-256 与可解码尺寸；原始响应字节未压缩、未转码。",
            "- 页面未引用路径构造/探测：0；第三方来源：0；登录/验证码/WAF 绕过：0。常规浏览器 UA 属 Issue #73 明确允许的正常官网请求。",
            "",
            "## 正式资产保护",
            "",
            f"- TRIAL 前后快照一致：{meta['protected_assets_unchanged']}。",
            f"- 本院画像树：{payload['protected_after']['profile_tree']['file_count']} 文件；正式照片目录存在：{payload['protected_after']['formal_photo_tree']['exists']}。",
            "- 本轮仅写 work/ TRIAL 工件；总底表三载体、入口台账三载体、更新报告、342 份画像和 _索引.md 均未修改。",
            "",
            "## 工件",
            "",
            f"- `{TRIAL_JSON_PATH.relative_to(ROOT).as_posix()}`",
            f"- `{TRIAL_CSV_PATH.relative_to(ROOT).as_posix()}`",
            f"- `{TRIAL_REPORT_PATH.relative_to(ROOT).as_posix()}`",
            f"- `{CONTACT_SHEET_PATH.relative_to(ROOT).as_posix()}`",
            f"- `{TRIAL_PHOTO_DIR.relative_to(ROOT).as_posix()}/`",
            "",
        ]
    )
    TRIAL_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def validate_manifest(payload: dict[str, Any]) -> None:
    with TRIAL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED_TRIAL_COUNT:
        raise RuntimeError(f"manifest 应为 {EXPECTED_TRIAL_COUNT} 行，实际 {len(rows)}")
    expected = {(item["name"], item["source_link"], item["sha256"]) for item in payload["samples"]}
    actual = {(item["name"], item["source_link"], item["sha256"]) for item in rows}
    if actual != expected:
        raise RuntimeError("manifest 与 payload 样本不一致")
    for row in rows:
        for key in ("detail_attempts", "photo_attempts", "excluded_resources"):
            json.loads(row[key])


def validate_payload(payload: dict[str, Any], require_visual_pass: bool) -> None:
    meta = payload.get("meta", {})
    samples = payload.get("samples", [])
    errors: list[str] = []
    if int(meta.get("scope_count") or 0) != EXPECTED_SCOPE_COUNT:
        errors.append("固定范围不是 342")
    if len(samples) != EXPECTED_TRIAL_COUNT:
        errors.append("TRIAL 样本不是 10")
    if Counter(sample.get("template") for sample in samples) != Counter(
        {"ksdoctorinfo": 8, "specialist": 2}
    ):
        errors.append("两类模板样本分布不是 8+2")
    departments = [clean_text(sample.get("department")) for sample in samples]
    if len(set(departments)) != EXPECTED_TRIAL_COUNT or any(not item for item in departments):
        errors.append("科室首原子未覆盖 10 个不同非空值")
    levels = Counter(sample.get("title_level") for sample in samples)
    if levels != Counter({"正高": 4, "副高": 2, "其他": 4}):
        errors.append(f"职称分层变化：{dict(levels)}")
    diagnostics = {item.get("template"): item for item in payload.get("structure_diagnostics", [])}
    if set(diagnostics) != {"specialist", "ksdoctorinfo"}:
        errors.append("缺少两类模板结构诊断")
    for template, diagnostic in diagnostics.items():
        if not clean_text(diagnostic.get("container_selector")):
            errors.append(f"{template} 缺少容器选择器")
        if "/UploadFiles/image/" not in clean_text(diagnostic.get("html_snippet")):
            errors.append(f"{template} HTML 片段缺少照片 URL 特征")
    if payload.get("protected_before") != payload.get("protected_after"):
        errors.append("正式资产快照发生变化")
    if payload.get("protected_after"):
        try:
            current_protected = protected_snapshot()
        except RuntimeError as exc:
            errors.append(f"当前正式资产快照无法读取：{exc}")
        else:
            if current_protected != payload.get("protected_after"):
                errors.append("当前正式资产与 TRIAL 结束快照不一致")
    for sample in samples:
        photo_url = clean_text(sample.get("photo_url"))
        if page_referenced_photo_url(photo_url, clean_text(sample.get("source_link"))) != photo_url:
            errors.append(f"页面引用照片 URL 非授权：{sample.get('name')}")
        if comparable_host(clean_text(sample.get("detail_final_url"))) != OFFICIAL_HOST:
            errors.append(f"详情最终 host 非官网：{sample.get('name')}")
        if comparable_host(clean_text(sample.get("photo_final_url"))) != OFFICIAL_HOST:
            errors.append(f"照片最终 host 非官网：{sample.get('name')}")
        path = ROOT / clean_text(sample.get("disk_path"))
        if not path.is_file():
            errors.append(f"TRIAL 照片缺失：{sample.get('name')}")
            continue
        content = path.read_bytes()
        if len(content) != int(sample.get("bytes") or -1):
            errors.append(f"照片字节数不一致：{sample.get('name')}")
        if hashlib.sha256(content).hexdigest() != sample.get("sha256"):
            errors.append(f"照片 SHA-256 不一致：{sample.get('name')}")
        extension = common.magic_extension(content, f"image/{path.suffix.lstrip('.')}")
        if extension != path.suffix.lstrip(".").lower().replace("jpeg", "jpg"):
            errors.append(f"照片扩展名/魔数不一致：{sample.get('name')}")
        width, height = common.image_dimensions(content)
        if (width, height) != (int(sample.get("width") or 0), int(sample.get("height") or 0)):
            errors.append(f"照片尺寸不一致：{sample.get('name')}")
        if int(sample.get("bytes") or 0) > MAX_PHOTO_BYTES:
            errors.append(f"照片超过 20 MiB：{sample.get('name')}")
    if require_visual_pass and meta.get("visual_review") != VISUAL_PASS:
        errors.append("联系表尚未记录视觉通过")
    if errors:
        raise RuntimeError("GDZY5413 照片 TRIAL 门禁失败：" + "；".join(errors))
    validate_manifest(payload)


def prepare_outputs() -> None:
    existing = [
        path
        for path in (TRIAL_JSON_PATH, TRIAL_CSV_PATH, TRIAL_REPORT_PATH, CONTACT_SHEET_PATH, TRIAL_PHOTO_DIR)
        if path.exists()
    ]
    if existing:
        raise RuntimeError(f"TRIAL 工件已存在，拒绝盲目覆盖：{[str(path) for path in existing]}")
    TRIAL_PHOTO_DIR.mkdir(parents=False)


def run_trial(run_date: str) -> dict[str, Any]:
    before = protected_snapshot()
    rows = load_scope_rows()
    selected = select_trial_rows(rows)
    prepare_outputs()
    session = common.OfficialSession()
    samples: list[dict[str, Any]] = []
    for row in selected:
        name = clean_text(row.get("姓名"))
        source_link = clean_text(row.get("来源链接"))
        detail_result, detail_attempts = fetch_with_retry(
            session, source_link, DIRECTORY_URL, f"{name} 详情"
        )
        if comparable_host(detail_result.final_url) != OFFICIAL_HOST:
            raise RuntimeError(f"详情最终 host 越界：{name} {detail_result.final_url}")
        if not detail_result.content_type.startswith("text/html"):
            raise RuntimeError(
                f"详情 Content-Type 非 HTML：{name} {detail_result.content_type}"
            )
        page_html = detail_result.content.decode(detail_result.charset or "utf-8", errors="replace")
        analysis = analyze_page(page_html, source_link, name)
        photo_result, photo_attempts = fetch_with_retry(
            session, analysis["photo_url"], source_link, f"{name} 照片"
        )
        if comparable_host(photo_result.final_url) != OFFICIAL_HOST:
            raise RuntimeError(f"照片最终 host 越界：{name} {photo_result.final_url}")
        content = photo_result.content
        extension = common.magic_extension(content, photo_result.content_type)
        if not extension:
            raise RuntimeError(
                f"照片 Content-Type/魔数不一致：{name} {photo_result.content_type}"
            )
        if len(content) > MAX_PHOTO_BYTES:
            raise RuntimeError(f"[FATAL - HUMAN_INTERVENTION_REQUIRED] {name} 照片超过 20 MiB")
        width, height = common.image_dimensions(content)
        placeholder_reason = placeholder_response_reason(content, width, height)
        if placeholder_reason:
            raise RuntimeError(
                f"固定样本响应内容为占位图：{name} {placeholder_reason} {analysis['photo_url']}"
            )
        filename, photo_path = allocate_trial_photo(row, extension, content)
        photo_path.write_bytes(content)
        title_text = row.get("职称_关键词") or row.get("职称身份原文")
        samples.append(
            {
                "name": name,
                "department": atomic_department(row),
                "primary_title": primary_title(title_text),
                "title_level": title_level(title_text),
                "template": analysis["template"],
                "source_link": source_link,
                "detail_id": detail_id(source_link),
                "photo_url": analysis["photo_url"],
                "filename": filename,
                "disk_path": photo_path.relative_to(ROOT).as_posix(),
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
                "width": width,
                "height": height,
                "detail_status": detail_result.status,
                "detail_content_type": detail_result.content_type,
                "detail_final_url": detail_result.final_url,
                "photo_status": photo_result.status,
                "photo_content_type": photo_result.content_type,
                "photo_final_url": photo_result.final_url,
                "container_selector": analysis["container_selector"],
                "detection_feature": analysis["detection_feature"],
                "html_snippet": analysis["html_snippet"],
                "candidate_count": analysis["candidate_count"],
                "excluded_resources": analysis["excluded_resources"],
                "detail_attempts": detail_attempts,
                "photo_attempts": photo_attempts,
                "over_5_mib": len(content) > OWNER_REPORT_BYTES,
            }
        )
    write_manifest(samples)
    build_contact_sheet(samples)
    after = protected_snapshot()
    if before != after:
        raise RuntimeError("TRIAL 写入期间正式资产快照发生变化")
    template_counts = Counter(sample["template"] for sample in samples)
    level_counts = Counter(sample["title_level"] for sample in samples)
    format_counts, content_type_magic_mismatch_count = sample_format_metadata(samples)
    structure_diagnostics = []
    for template in ("specialist", "ksdoctorinfo"):
        representative = next(sample for sample in samples if sample["template"] == template)
        structure_diagnostics.append(
            {
                "template": template,
                "sample_name": representative["name"],
                "source_link": representative["source_link"],
                "container_selector": representative["container_selector"],
                "detection_feature": representative["detection_feature"],
                "html_snippet": representative["html_snippet"],
            }
        )
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "hospital": HOSPITAL,
            "run_date": run_date,
            "generated_at_utc": utc_now(),
            "phase": "TRIAL",
            "official_home": OFFICIAL_HOME,
            "directory_url": DIRECTORY_URL,
            "scope_count": len(rows),
            "scope_template_counts": {
                "ksdoctorinfo": EXPECTED_KSDOCTOR_COUNT,
                "specialist": EXPECTED_SPECIALIST_COUNT,
            },
            "trial_count": len(samples),
            "trial_template_counts": dict(template_counts),
            "distinct_department_count": len({sample["department"] for sample in samples}),
            "title_level_counts": dict(level_counts),
            "detail_success_count": sum(sample["detail_status"] == 200 for sample in samples),
            "photo_success_count": sum(sample["photo_status"] == 200 for sample in samples),
            "total_photo_bytes": sum(int(sample["bytes"]) for sample in samples),
            "size_buckets": size_buckets(samples),
            "format_counts": format_counts,
            "content_type_magic_mismatch_count": content_type_magic_mismatch_count,
            "over_5_mib_count": sum(bool(sample["over_5_mib"]) for sample in samples),
            "over_20_mib_count": sum(
                int(sample["bytes"]) > MAX_PHOTO_BYTES for sample in samples
            ),
            "constructed_unreferenced_path_count": 0,
            "third_party_source_count": 0,
            "excluded_resource_download_count": 0,
            "protected_assets_unchanged": True,
            "profile_markdown_count": EXPECTED_PROFILE_MARKDOWN_COUNT,
            "formal_photo_directory_exists": FORMAL_PHOTO_DIR.exists(),
            "session_cookie_names": session.cookie_names,
            "incomplete_read_retry_count": session.incomplete_read_retry_count,
            "visual_review": "PENDING_MANUAL_REVIEW",
        },
        "sample_plan": [
            {"name": name, "template": template, "title_level": level}
            for name, template, level in SAMPLE_PLAN
        ],
        "structure_diagnostics": structure_diagnostics,
        "exclusion_policy": list(EXCLUSION_POLICY),
        "samples": samples,
        "protected_before": before,
        "protected_after": after,
    }
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_report(payload)
    validate_payload(payload, require_visual_pass=False)
    return payload


def load_trial_payload() -> dict[str, Any]:
    if not TRIAL_JSON_PATH.is_file():
        raise RuntimeError(f"TRIAL payload 不存在：{TRIAL_JSON_PATH}")
    return json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))


def mark_visual_pass() -> dict[str, Any]:
    payload = load_trial_payload()
    validate_payload(payload, require_visual_pass=False)
    format_counts, content_type_magic_mismatch_count = sample_format_metadata(
        payload["samples"]
    )
    payload["meta"]["format_counts"] = format_counts
    payload["meta"]["content_type_magic_mismatch_count"] = (
        content_type_magic_mismatch_count
    )
    payload["meta"]["visual_review"] = VISUAL_PASS
    payload["meta"]["visual_reviewed_at_utc"] = utc_now()
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_report(payload)
    validate_payload(payload, require_visual_pass=True)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #73 广东省第二中医院照片补录 TRIAL")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--run", action="store_true", help="执行 10 人 TRIAL，正式资产零修改")
    action.add_argument("--mark-visual-pass", action="store_true", help="目视联系表后写入视觉通过")
    action.add_argument("--validate", action="store_true", help="验证既有 TRIAL 工件")
    parser.add_argument("--run-date", default=date.today().isoformat())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.run:
        payload = run_trial(args.run_date)
        print(
            json.dumps(
                {
                    "status": "TRIAL_READY_FOR_VISUAL_REVIEW",
                    "samples": len(payload["samples"]),
                    "total_bytes": payload["meta"]["total_photo_bytes"],
                    "payload": str(TRIAL_JSON_PATH),
                    "manifest": str(TRIAL_CSV_PATH),
                    "report": str(TRIAL_REPORT_PATH),
                    "contact_sheet": str(CONTACT_SHEET_PATH),
                },
                ensure_ascii=False,
            )
        )
    elif args.mark_visual_pass:
        payload = mark_visual_pass()
        print(
            json.dumps(
                {"status": "TRIAL_VISUAL_PASS_RECORDED", "samples": len(payload["samples"])},
                ensure_ascii=False,
            )
        )
    else:
        payload = load_trial_payload()
        validate_payload(payload, require_visual_pass=True)
        print(
            json.dumps(
                {"status": "TRIAL_VALIDATED", "samples": len(payload["samples"])},
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
