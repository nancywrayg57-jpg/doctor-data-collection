from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass, replace
from datetime import date
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

try:
    import requests
    from bs4 import BeautifulSoup
    from openpyxl import load_workbook
except ImportError as exc:
    raise SystemExit(
        "缺少依赖：需要 requests、beautifulsoup4、openpyxl。请使用已安装这些库的本机 Python 运行。"
    ) from exc


ROOT = Path(r"D:\workspace\信息收集整理")
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
WORK_DIR = ROOT / "work"
LEDGER_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"
WORKBOOK_BUILDER = WORK_DIR / "build_doctor_workbook.mjs"
MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_JSON_PATH = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_PREVIEW_PATH = WORK_DIR / f"{MASTER_BASENAME}_preview.png"
MASTER_REPORT_PATH = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
BUNDLED_NODE = Path(
    r"C:\Users\zhouxinting\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
)

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
    "采集入口",
    "采集方式",
    "采集日期",
    "详情页状态",
    "已建画像",
    "异常提示",
    "复核状态",
]

TITLE_TERMS = [
    "主任医师",
    "副主任医师",
    "主治医师",
    "住院医师",
    "医师",
    "主任护师",
    "副主任护师",
    "主管护师",
    "研究员",
    "副研究员",
    "教授",
    "副教授",
    "博士生导师",
    "硕士生导师",
    "医学博士",
    "医学硕士",
    "博士",
    "硕士",
    "科主任",
    "副主任",
    "首席专家",
    "院长",
    "副院长",
]

GROUP_KEYWORDS = {
    "慢性病": [
        "高血压",
        "糖尿病",
        "冠心病",
        "心力衰竭",
        "心衰",
        "高脂血症",
        "动脉粥样硬化",
        "慢性",
        "代谢",
    ],
    "肿瘤": [
        "肿瘤",
        "癌",
        "瘤",
        "淋巴瘤",
        "白血病",
        "放疗",
        "化疗",
        "靶向",
        "鼻咽癌",
        "肺癌",
        "肝癌",
        "胃癌",
        "肠癌",
        "乳腺癌",
    ],
    "生殖疾病": [
        "生殖",
        "不孕",
        "卵巢",
        "辅助生殖",
        "试管",
        "胚胎",
        "妇科内分泌",
        "多囊",
        "月经",
    ],
    "免疫/风湿/感染": [
        "风湿",
        "免疫",
        "感染",
        "免疫功能",
        "红斑狼疮",
        "类风湿",
        "强直性脊柱炎",
    ],
    "术后恢复/康复": [
        "术后",
        "康复",
        "恢复",
        "营养",
        "姑息",
        "疼痛",
        "创面",
        "烧伤",
        "伤口",
        "功能障碍",
    ],
    "疑难重症": [
        "疑难",
        "危重",
        "重症",
        "急危重",
        "难治",
        "复杂",
        "多学科",
        "MDT",
        "高危",
        "罕见",
        "转化治疗",
    ],
}

PRIORITY_DEPARTMENTS = [
    "呼吸",
    "消化",
    "内分泌",
    "血液",
    "风湿",
    "心血管",
    "胃肠",
    "肝胆",
    "胸部肿瘤",
    "腹盆部肿瘤",
    "中医肿瘤",
    "肿瘤介入",
    "鼻咽癌",
    "乳腺肿瘤",
    "放射肿瘤",
    "妇科",
    "生殖",
    "康复",
    "营养",
]

HIGHLIGHT_TERMS = [
    "科主任",
    "首席专家",
    "主任医师",
    "副主任医师",
    "博士生导师",
    "硕士生导师",
    "政府特殊津贴",
    "突出贡献",
    "高层次人才",
    "领军人才",
    "学科带头人",
    "国家重点研发",
    "重点研发",
    "访问",
    "研修",
    "进修",
    "美国",
    "英国",
    "德国",
    "国家自然科学基金",
    "SCI",
    "发表",
    "专利",
    "指南",
    "名医",
    "好医生",
    "人才",
    "奖",
    "委员会",
    "协会",
    "学会",
    "建设",
    "率先",
    "多学科",
    "MDT",
    "疑难",
    "危重",
    "精准",
]

GENERIC_ADAPTER_ID = "generic_official_template"
GENERIC_MAX_PAGES_DEFAULT = 60
GENERIC_DETAIL_PATH_HINTS = [
    "doctor",
    "expert",
    "zhuanjia",
    "specialist",
    "physician",
    "staff",
    "team",
    "doctorinfo",
    "expertinfo",
    "node",
]
GENERIC_PATH_BLOCK_HINTS = [
    "news",
    "notice",
    "article",
    "video",
    "cggg",
    "cgjggg",
    "cgzb",
    "dzcggg",
    "scdygg",
    "qtgsxx",
    "xwzx",
    "mtbd",
    "zxtg",
    "zlkp",
    "boshihou",
    "bgpt",
    "tender",
    "zhaobiao",
    "caigou",
    "research",
    "keyan",
    "home",
]
GENERIC_STRONG_TITLE_TERMS = [
    "主任医师",
    "副主任医师",
    "主治医师",
    "住院医师",
    "医师",
    "主任护师",
    "副主任护师",
    "主管护师",
    "研究员",
    "副研究员",
    "教授",
    "副教授",
    "博士生导师",
    "硕士生导师",
    "科主任",
    "首席专家",
]
GENERIC_DETAIL_TEXT_HINTS = [
    "姓名",
    "医生",
    "专家",
    "科室",
    "职称",
    "擅长",
    "专长",
    "简介",
    "出诊",
    "门诊",
]
GENERIC_IGNORED_LINK_TEXTS = [
    "首页",
    "更多",
    "更多>>",
    "查看",
    "查看详情",
    "详情",
    "上一页",
    "下一页",
    "尾页",
    "末页",
    "返回",
    "预约挂号",
    "在线预约",
    "登录",
]
GENERIC_NAME_BLOCK_TERMS = [
    "医院",
    "中心",
    "科室",
    "专科",
    "专家",
    "医生",
    "主任",
    "医师",
    "教授",
    "导师",
    "博士",
    "硕士",
    "门诊",
    "简介",
    "擅长",
    "详情",
    "预约",
    "全部",
    "面包屑",
    "院士",
    "风采",
    "临床",
    "护理",
    "名医",
    "名家",
    "列表",
    "团队",
    "学科",
    "护理",
    "公告",
    "新闻",
    "患者",
    "就诊须知",
    "住院须知",
    "联系我们",
    "门诊时间",
]

PROFILE_NOISE_TAGS = {
    "aside",
    "button",
    "footer",
    "form",
    "nav",
    "noscript",
    "script",
    "style",
    "svg",
    "template",
}
PROFILE_NOISE_ATTRIBUTE_TOKENS = {
    "action-tools",
    "actions",
    "breadcrumb",
    "breadcrumbs",
    "crumb",
    "crumbs",
    "footer",
    "header",
    "hidden",
    "menu",
    "nav",
    "navigation",
    "pager",
    "pagination",
    "print",
    "share",
    "sidebar",
    "side-nav",
    "sidenav",
    "site-footer",
    "site-header",
    "social",
    "sr-only",
    "toolbar",
    "visually-hidden",
}
PROFILE_INLINE_NOISE_PHRASES = [
    "加载更多",
    "打印本页",
    "关闭窗口",
    "返回顶部",
]


@dataclass
class HospitalTarget:
    city: str
    hospital: str
    homepage: str
    entry_url: str
    difficulty: str
    review: str
    adapter_id: str


def clean_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", unescape(value or "")).strip()


def clip(value: str | None, max_len: int) -> str:
    text = clean_text(value)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def first_nonempty(*values: str | None) -> str:
    for value in values:
        text = clean_text(value)
        if text:
            return text
    return ""


def safe_file_part(value: str) -> str:
    text = re.sub(r'[\\/:*?"<>|\s]+', "_", value).strip("_")
    return text or "unnamed"


def canonical_url(value: str) -> str:
    parsed = urlparse(value)
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return parsed._replace(netloc=netloc, fragment="").geturl().rstrip("/")


def fetch(session: requests.Session, url: str, retries: int = 3) -> tuple[int | None, str, str]:
    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=35)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding or response.encoding or "utf-8"
                return response.status_code, response.text, ""
            last_error = f"HTTP {response.status_code}"
        except Exception as exc:  # noqa: BLE001 - keep collection failure visible
            last_error = str(exc)
        time.sleep(0.8 * attempt)
    return None, "", last_error


def create_official_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36; "
                "public official-site collection"
            )
        }
    )
    return session


def extract_terms(text: str, terms: list[str]) -> list[str]:
    found: list[str] = []
    used_spans: list[tuple[int, int]] = []
    for term in sorted(terms, key=len, reverse=True):
        matched = False
        for match in re.finditer(re.escape(term), text):
            span = match.span()
            if any(max(span[0], used[0]) < min(span[1], used[1]) for used in used_spans):
                continue
            used_spans.append(span)
            matched = True
        if matched and term not in found:
            found.append(term)
    return [term for term in terms if term in found]


def extract_sentences(text: str, terms: list[str], limit: int = 4, max_len: int = 420) -> str:
    parts = [clean_text(part) for part in re.split(r"(?<=[。！？；;])|\n", text) if clean_text(part)]
    hits: list[str] = []
    for part in parts:
        if any(term in part for term in terms):
            hits.append(part)
        if len(hits) >= limit:
            break
    return clip(" ".join(hits), max_len)


def group_tags(text: str) -> tuple[list[str], list[str]]:
    groups: list[str] = []
    tags: list[str] = []
    for group, keywords in GROUP_KEYWORDS.items():
        matches = extract_terms(text, keywords)
        if matches:
            groups.append(group)
            tags.extend(matches)
    return groups, list(dict.fromkeys(tags))


def strip_article_tail(text: str) -> str:
    cleaned = clean_text(text)
    markers = [
        "上一篇：",
        "下一篇：",
        "相关文章：",
        "上一篇:",
        "下一篇:",
        "相关文章:",
        "最新文章",
        "南部战区空军医院 南部战区空军医院",
    ]
    positions = [cleaned.find(marker) for marker in markers if cleaned.find(marker) >= 0]
    if positions:
        cleaned = cleaned[: min(positions)]
    return clean_text(cleaned)


def infer_department(text: str) -> str:
    source = clean_text(text)
    if not source:
        return ""
    pattern = (
        r"([\u4e00-\u9fff、]{1,24}?"
        r"(?:内科|外科|妇科|儿科|骨科|皮肤科|肿瘤科|口腔科|营养科|保健办|科|中心|病房|门诊))"
        r"(?=主任|副主任|主治|医师|专家|博士|硕士|，|,|；|;|\s|$)"
    )
    candidates = [clean_text(match) for match in re.findall(pattern, source)]
    candidates = [
        candidate
        for candidate in candidates
        if not any(term in candidate for term in ["本中心", "聘任", "攻读", "获得", "入职"])
    ]
    candidates = [candidate for candidate in candidates if candidate]
    return candidates[-1] if candidates else ""


def clean_generic_department(value: str | None) -> str:
    text = clean_text(value)
    if not text:
        return ""
    text = re.sub(r"^(?:科室|所在科室|出诊科室|专业|专科)\s*[:：]\s*", "", text)
    stop_pattern = (
        r"\s*(?:介绍|简介|个人简介|职称|职务|专业擅长|擅长|医疗专长|诊疗专长|"
        r"技术专长|业务专长|专长|研究方向)\s*[:：]"
        r"|\s*(?=(?:19|20)\d{2}年)"
        r"|[。！？；;]"
    )
    text = clean_text(re.split(stop_pattern, text, maxsplit=1)[0])
    match = re.match(
        r"^[\u4e00-\u9fff、]{1,28}?(?:科|中心|病房|门诊)(?:[一二三四五六七八九十\d]+室)?",
        text,
    )
    if match:
        return clean_text(match.group(0))
    return text if len(text) <= 30 else ""


def has_department_text_pollution(raw_value: str | None, cleaned_value: str | None) -> bool:
    raw = clean_text(raw_value)
    cleaned = clean_text(cleaned_value)
    return bool(raw and cleaned and raw != cleaned)


def read_ledger(path: Path) -> list[dict[str, Any]]:
    workbook = load_workbook(path, read_only=True, data_only=True)
    sheet = workbook["入口台账"]
    headers = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
    rows: list[dict[str, Any]] = []
    for raw in sheet.iter_rows(min_row=2, values_only=True):
        item = {headers[index]: raw[index] if index < len(raw) else "" for index in range(len(headers))}
        if item.get("医院名称"):
            rows.append(item)
    return rows


def normalize_bottom_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for header in BASE_HEADERS:
        value = row.get(header, "")
        if value is None:
            normalized[header] = ""
        elif header == "序号":
            normalized[header] = value
        else:
            normalized[header] = clean_text(str(value))
    return normalized


def doctor_row_key(row: dict[str, Any]) -> tuple[str, ...]:
    hospital = clean_text(str(row.get("医院") or ""))
    name = clean_text(str(row.get("姓名") or ""))
    department = first_nonempty(
        str(row.get("科室_分类页") or ""),
        str(row.get("科室_列表卡片") or ""),
    )
    source = clean_text(str(row.get("来源链接") or ""))
    if hospital and name and department:
        return ("doctor", hospital, name, department)
    if hospital and source:
        return ("source", hospital, canonical_url(source))
    return ("row", hospital, name, source)


def row_quality_score(row: dict[str, Any]) -> int:
    quality_fields = [
        "职称_关键词",
        "职称身份原文",
        "重点关注范围",
        "重点疾病标签",
        "擅长诊疗方向摘录",
        "亮眼经历线索",
        "列表简介",
        "详情正文摘录",
        "来源链接",
    ]
    nonempty = sum(1 for field in quality_fields if clean_text(str(row.get(field) or "")))
    length = sum(len(clean_text(str(row.get(field) or ""))) for field in quality_fields)
    return nonempty * 1000 + length


def read_bottom_table_rows(path: Path) -> list[dict[str, Any]]:
    workbook = load_workbook(path, read_only=True, data_only=True)
    if "自动采集底表" not in workbook.sheetnames:
        return []
    sheet = workbook["自动采集底表"]
    raw_headers = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
    headers = [clean_text(str(header or "")) for header in raw_headers]
    index_by_header = {header: index for index, header in enumerate(headers) if header}
    rows: list[dict[str, Any]] = []
    for values in sheet.iter_rows(min_row=2, values_only=True):
        if not values or not any(values):
            continue
        item = {}
        for header in BASE_HEADERS:
            column_index = index_by_header.get(header)
            item[header] = values[column_index] if column_index is not None and column_index < len(values) else ""
        normalized = normalize_bottom_row(item)
        if not normalized["医院"] and not normalized["姓名"] and not normalized["来源链接"]:
            continue
        rows.append(normalized)
    return rows


def load_existing_rows_for_master() -> tuple[list[dict[str, Any]], str, bool]:
    if MASTER_XLSX_PATH.exists():
        return read_bottom_table_rows(MASTER_XLSX_PATH), str(MASTER_XLSX_PATH), True

    legacy_paths = [
        path
        for path in sorted(SOURCE_DIR.glob("*_全院医生自动采集底表.xlsx"))
        if path.name != MASTER_XLSX_PATH.name
    ]
    rows: list[dict[str, Any]] = []
    for path in legacy_paths:
        rows.extend(read_bottom_table_rows(path))
    source_label = "；".join(str(path) for path in legacy_paths) if legacy_paths else "无既有底表"
    return rows, source_label, False


def merge_rows_for_master(
    existing_rows: list[dict[str, Any]],
    incoming_rows: list[dict[str, Any]],
    preserve_existing: bool,
) -> tuple[list[dict[str, Any]], int, int, int]:
    merged: list[dict[str, Any]] = []
    index_by_key: dict[tuple[str, ...], int] = {}
    existing_duplicates = 0
    incoming_added = 0
    incoming_skipped = 0

    for row in existing_rows:
        normalized = normalize_bottom_row(row)
        key = doctor_row_key(normalized)
        if key in index_by_key:
            existing_duplicates += 1
            if not preserve_existing and row_quality_score(normalized) > row_quality_score(merged[index_by_key[key]]):
                merged[index_by_key[key]] = normalized
            continue
        index_by_key[key] = len(merged)
        merged.append(normalized)

    for row in incoming_rows:
        normalized = normalize_bottom_row(row)
        key = doctor_row_key(normalized)
        if key in index_by_key:
            incoming_skipped += 1
            continue
        index_by_key[key] = len(merged)
        merged.append(normalized)
        incoming_added += 1

    for index, row in enumerate(merged, start=1):
        row["序号"] = index
    return merged, incoming_added, incoming_skipped, existing_duplicates


def build_hospital_batches(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        hospital = clean_text(str(row.get("医院") or "未识别医院"))
        grouped.setdefault(hospital, []).append(row)

    batches: list[dict[str, Any]] = []
    for hospital, hospital_rows in sorted(grouped.items()):
        dates = sorted({clean_text(str(row.get("采集日期") or "")) for row in hospital_rows if row.get("采集日期")})
        review_count = sum(1 for row in hospital_rows if clean_text(str(row.get("复核状态") or "")) != "已复核")
        batches.append(
            {
                "医院": hospital,
                "医生数": len(hospital_rows),
                "采集日期": "、".join(dates),
                "待复核数": review_count,
                "已建画像数": sum(1 for row in hospital_rows if clean_text(str(row.get("已建画像") or "")) == "是"),
                "采集入口": first_nonempty(*(str(row.get("采集入口") or "") for row in hospital_rows)),
            }
        )
    return batches


def build_master_payload(
    today: str,
    incoming_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    existing_rows, source_label, preserve_existing = load_existing_rows_for_master()
    incoming_rows = incoming_payload["rows"] if incoming_payload else []
    rows, added, skipped, existing_duplicates = merge_rows_for_master(
        existing_rows,
        incoming_rows,
        preserve_existing=preserve_existing,
    )

    category_counter = Counter()
    priority_counter = Counter()
    group_counter = Counter()
    warning_counter = Counter()
    for row in rows:
        department = first_nonempty(str(row.get("科室_分类页") or ""), str(row.get("科室_列表卡片") or ""))
        if department:
            category_counter[department] += 1
        priority = clean_text(str(row.get("重点优先级") or "普通"))
        if priority:
            priority_counter[priority] += 1
        for group in clean_text(str(row.get("重点关注范围") or "")).split("、"):
            if group:
                group_counter[group] += 1
        for warning in clean_text(str(row.get("异常提示") or "")).split("；"):
            if warning:
                warning_counter[warning] += 1

    incoming_meta = incoming_payload.get("meta", {}) if incoming_payload else {}
    hospital_batches = build_hospital_batches(rows)
    return {
        "meta": {
            "city": "珠三角",
            "hospital": "珠三角三甲医院医生画像总表",
            "homepage": "",
            "entry_url": "详见各行采集入口",
            "adapter_id": "multi_hospital_official_pipeline",
            "collected_at": today,
            "category_count": len({row.get("采集入口") for row in rows if row.get("采集入口")}),
            "raw_card_rows": incoming_meta.get("raw_card_rows", 0),
            "unique_doctor_count": len(rows),
            "category_error_count": incoming_meta.get("category_error_count", 0),
            "detail_error_count": incoming_meta.get("detail_error_count", 0),
            "existing_profile_count": sum(1 for row in rows if clean_text(str(row.get("已建画像") or "")) == "是"),
            "ledger_review": "多院汇总，详见官网入口台账",
            "ledger_difficulty": "多院汇总",
            "source_seed": source_label,
            "current_batch_hospital": incoming_meta.get("hospital", ""),
            "current_batch_rows": len(incoming_rows),
            "new_rows_added": added,
            "duplicate_rows_skipped": skipped,
            "existing_duplicate_rows": existing_duplicates,
            "hospital_count": len(hospital_batches),
        },
        "categories": [],
        "category_errors": incoming_payload.get("category_errors", []) if incoming_payload else [],
        "detail_errors": incoming_payload.get("detail_errors", []) if incoming_payload else [],
        "category_counts": category_counter.most_common(),
        "priority_counts": dict(priority_counter),
        "group_counts": dict(group_counter),
        "warning_counts": dict(warning_counter),
        "hospital_batches": hospital_batches,
        "rows": rows,
    }


def dedicated_adapter_for(entry_url: str) -> str:
    parsed = urlparse(entry_url or "")
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    if "gzzoc.org.cn" in host and "/expert-introduction" in path:
        return "gzzoc_drupal_doctor"
    if "nbkjyy.mil.cn" in host and "/expert" in path:
        return "nbkjyy_static_expert"
    return ""


def adapter_for(entry_url: str, include_generic: bool = False) -> str:
    adapter_id = dedicated_adapter_for(entry_url)
    if adapter_id:
        return adapter_id
    parsed = urlparse(entry_url or "")
    if include_generic and parsed.scheme in {"http", "https"} and parsed.netloc:
        return GENERIC_ADAPTER_ID
    return ""


def confirmed_a_targets(rows: list[dict[str, Any]], include_generic: bool = False) -> list[HospitalTarget]:
    targets: list[HospitalTarget] = []
    for row in rows:
        review = clean_text(str(row.get("人工复核结果") or ""))
        difficulty = clean_text(str(row.get("采集难度_初判") or ""))
        entry_url = clean_text(str(row.get("医生目录入口_候选") or ""))
        adapter_id = adapter_for(entry_url, include_generic=include_generic)
        if review != "确认可采集":
            continue
        if not difficulty.startswith("A-"):
            continue
        if not adapter_id:
            continue
        targets.append(
            HospitalTarget(
                city=clean_text(str(row.get("城市") or "")),
                hospital=clean_text(str(row.get("医院名称") or "")),
                homepage=clean_text(str(row.get("官网首页_候选") or "")),
                entry_url=entry_url,
                difficulty=difficulty,
                review=review,
                adapter_id=adapter_id,
            )
        )
    return targets


def collect_existing_profile_links() -> set[str]:
    links: set[str] = set()
    if not VAULT.exists():
        return links
    for path in VAULT.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in re.finditer(r"来源链接[:：]\s*(https?://\S+)", text):
                links.add(canonical_url(match.group(1)))
    return links


def with_query_param(url: str, key: str, value: str | int) -> str:
    parsed = urlparse(url)
    pairs = [(name, item) for name, item in parse_qsl(parsed.query, keep_blank_values=True) if name != key]
    pairs.append((key, str(value)))
    return urlunparse(parsed._replace(query=urlencode(pairs)))


def comparable_host(url: str) -> str:
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def is_same_official_host(base_url: str, candidate_url: str) -> bool:
    return comparable_host(base_url) == comparable_host(candidate_url)


def is_collectable_url(base_url: str, candidate_url: str) -> bool:
    parsed = urlparse(candidate_url)
    if parsed.scheme not in {"http", "https"}:
        return False
    if not is_same_official_host(base_url, candidate_url):
        return False
    path = parsed.path.lower()
    if any(path.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip"]):
        return False
    if any(block in path for block in ["/login", "/register", "/search", "/user", "/admin"]):
        return False
    return True


def compact_visible_text(element: Any, max_len: int = 1200) -> str:
    return clip(clean_text(element.get_text(" ", strip=True)), max_len)


def strip_profile_navigation_text(value: str | None) -> str:
    text = clean_text(value)
    if not text:
        return ""

    separator = r"(?:/|>|＞|»|›|→)"
    label = r"(?:姓名|科室|所在科室|职称|职务|专业擅长|擅长|专长|简介|个人简介|一、|二、)"
    breadcrumb_patterns = [
        rf"(?:临床专家\s*)?面包屑\s*首页\s*(?:{separator}\s*[^/＞>»›→]{{1,60}}?\s*){{1,10}}(?={label}|$)",
        rf"(?:你)?当前所在的位置\s*[:：]?\s*[^/＞>»›→]{{0,60}}\s*(?:{separator}\s*[^/＞>»›→]{{1,60}}?\s*){{1,10}}(?={label}|$)",
        rf"当前位置\s*[:：]?\s*首页\s*(?:{separator}\s*[^/＞>»›→]{{1,60}}?\s*){{1,10}}(?={label}|$)",
    ]
    for pattern in breadcrumb_patterns:
        text = re.sub(pattern, " ", text, count=1)
    for phrase in PROFILE_INLINE_NOISE_PHRASES:
        text = text.replace(phrase, " ")
    return clean_text(text)


def contains_navigation_text(value: str | None) -> bool:
    text = clean_text(value)
    if not text:
        return False
    return any(
        marker in text
        for marker in ["你当前所在的位置", "当前所在的位置", "当前位置", "面包屑", "首页 >", "首页＞"]
    )


def element_attribute_tokens(element: Any) -> set[str]:
    values: list[str] = []
    element_id = element.get("id")
    if element_id:
        values.append(str(element_id))
    values.extend(str(value) for value in (element.get("class") or []))
    return {
        token
        for value in values
        for token in re.split(r"\s+", value.lower())
        if token
    }


def is_profile_noise_element(element: Any) -> bool:
    name = str(getattr(element, "name", "") or "").lower()
    if name in PROFILE_NOISE_TAGS:
        return True
    if clean_text(element.get("role")).lower() == "navigation":
        return True
    if element.has_attr("hidden") or clean_text(element.get("aria-hidden")).lower() == "true":
        return True

    tokens = element_attribute_tokens(element)
    if tokens & PROFILE_NOISE_ATTRIBUTE_TOKENS:
        return True
    return any("breadcrumb" in token for token in tokens)


def extract_navigation_context(soup: BeautifulSoup) -> str:
    candidates: list[tuple[int, str]] = []
    seen: set[str] = set()
    for element in soup.find_all(True):
        tokens = element_attribute_tokens(element)
        role = clean_text(element.get("role")).lower()
        has_breadcrumb_token = (
            bool(tokens & {"breadcrumb", "breadcrumbs", "crumb", "crumbs"})
            or any("breadcrumb" in token for token in tokens)
        )
        is_navigation = role == "navigation" or has_breadcrumb_token
        if not is_navigation:
            continue
        text = compact_visible_text(element, 1200)
        if not text or text in seen:
            continue
        seen.add(text)
        score = 100 if has_breadcrumb_token else 0
        if "面包屑" in text or "当前位置" in text:
            score += 50
        if "首页" in text and any(separator in text for separator in ["/", ">", "＞", "»", "›"]):
            score += 20
        candidates.append((score, text))
    contexts = [text for _, text in sorted(candidates, key=lambda item: item[0], reverse=True)]
    return clip(" ".join(contexts), 2400)


def remove_profile_noise_elements(soup: BeautifulSoup) -> None:
    for element in reversed(soup.find_all(True)):
        if is_profile_noise_element(element):
            element.decompose()


def nearest_card_text(anchor: Any) -> str:
    parts = [clean_text(anchor.get_text(" ", strip=True))]
    image = anchor.find("img")
    if image:
        parts.append(clean_text(image.get("alt")))
        parts.append(clean_text(image.get("title")))

    seed_text = clean_text(" ".join(part for part in parts if part))
    parent = anchor.parent
    for _ in range(4):
        if not parent:
            break
        text = compact_visible_text(parent)
        link_count = len(parent.find_all("a"))
        if 4 <= len(text) <= 700:
            strong_title_hits = extract_terms(text, GENERIC_STRONG_TITLE_TERMS)
            if link_count <= 4 and (strong_title_hits or "擅长" in text or "专长" in text or looks_like_person_name(seed_text)):
                return strip_profile_navigation_text(" ".join([seed_text, text]))
        parent = parent.parent
    return strip_profile_navigation_text(seed_text)


def looks_like_person_name(value: str) -> bool:
    candidate = clean_text(value).strip("：:，,、；;（）()[]【】<>《》")
    if "·" in candidate:
        if not re.fullmatch(r"[\u4e00-\u9fff·]{3,8}", candidate):
            return False
    elif not re.fullmatch(r"[\u4e00-\u9fff]{2,4}", candidate):
        return False
    if any(term in candidate for term in GENERIC_NAME_BLOCK_TERMS):
        return False
    return True


def matches_generic_directory_detail_url(entry_url: str, candidate_url: str) -> bool:
    entry_match = re.fullmatch(r"/section/(\d+)/?", urlparse(entry_url).path)
    if comparable_host(entry_url) != "smukqyy.cn" or not entry_match:
        return True
    directory_id = re.escape(entry_match.group(1))
    return bool(re.fullmatch(rf"/prods/{directory_id}/\d+/?", urlparse(candidate_url).path))


def generic_record_quality(
    name: str,
    source_link: str,
    entry_url: str,
    detail: dict[str, str],
    item: dict[str, str],
) -> tuple[bool, list[str]]:
    valid = looks_like_person_name(name) and matches_generic_directory_detail_url(entry_url, source_link)
    warnings: list[str] = []
    if not valid:
        warnings.append("非医生页面或姓名异常")
    if detail.get("department_polluted") == "yes" or has_department_text_pollution(
        item.get("department"), clean_generic_department(item.get("department"))
    ):
        warnings.append("科室原文含正文，已清洗")
    if detail.get("specialty_navigation_polluted") == "yes":
        warnings.append("擅长原文含导航文本，已清空")
    return valid, warnings


def classify_generic_record(
    valid_doctor_record: bool,
    combined_text: str,
    title_hits: list[str],
) -> tuple[str, list[str], list[str]]:
    if not valid_doctor_record:
        return "", [], []
    groups, tags = group_tags(combined_text)
    priority = "普通"
    if any(term in combined_text for term in PRIORITY_DEPARTMENTS) or groups:
        priority = "高"
    elif any(term != "医师" for term in title_hits):
        priority = "中"
    return priority, groups, tags


def extract_person_name(*texts: str | None) -> str:
    for raw in texts:
        text = clean_text(raw)
        if not text:
            continue
        text = re.sub(r"(姓名|专家姓名|医生姓名)\s*[:：]", " ", text)
        title_positions = [text.find(term) for term in TITLE_TERMS if text.find(term) > 0]
        fragments = [text]
        if title_positions:
            fragments.insert(0, text[: min(title_positions)])
        for fragment in fragments:
            for match in re.finditer(r"[\u4e00-\u9fff·]{2,8}", fragment):
                candidate = match.group(0)
                if looks_like_person_name(candidate):
                    return candidate
    return ""


def generic_link_score(href: str, context: str) -> int:
    parsed = urlparse(href)
    path = parsed.path.lower()
    if any(hint in path for hint in GENERIC_PATH_BLOCK_HINTS):
        return -10

    path_hint = any(hint in path for hint in GENERIC_DETAIL_PATH_HINTS)
    has_numeric_detail = bool(re.search(r"[/_-]\d{2,}(\.html?)?$", path) or re.search(r"/node/\d+$", path))
    strong_title_hits = extract_terms(context, GENERIC_STRONG_TITLE_TERMS)
    has_name = bool(extract_person_name(context))
    detail_text_signal = any(term in context for term in ["姓名", "科室", "职称", "擅长", "专长"])
    if path_hint and not (has_name or strong_title_hits or detail_text_signal):
        return -10
    if path_hint and not has_numeric_detail and not has_name and not (strong_title_hits and detail_text_signal):
        return -10
    if not path_hint and not (has_name and (strong_title_hits or detail_text_signal)):
        return -10

    score = 0
    if path_hint:
        score += 4
    if has_numeric_detail:
        score += 2
    if strong_title_hits:
        score += 4
    if has_name:
        score += 3
    if any(term in context for term in GENERIC_DETAIL_TEXT_HINTS):
        score += 2
    if "擅长" in context or "专长" in context:
        score += 2
    short_text = clean_text(context)
    if short_text in GENERIC_IGNORED_LINK_TEXTS:
        score -= 4
    return score


def discover_generic_detail_links(html: str, page_url: str, entry_url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = urljoin(page_url, anchor["href"])
        if canonical_url(href) == canonical_url(page_url):
            continue
        if not is_collectable_url(entry_url, href):
            continue
        if not matches_generic_directory_detail_url(entry_url, href):
            continue
        context = nearest_card_text(anchor)
        score = generic_link_score(href, context)
        if score < 6:
            continue
        key = canonical_url(href)
        if key in seen:
            continue
        seen.add(key)
        name = extract_person_name(context)
        rows.append(
            {
                "source_link": href,
                "name": name,
                "list_title": clip(context, 500),
                "department": infer_department(context),
                "description": clip(context, 700),
                "list_page": page_url,
                "score": str(score),
            }
        )
    return rows


def discover_generic_list_pages(entry_url: str, html: str, max_pages: int) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    pages = [entry_url]
    seen = {canonical_url(entry_url)}
    entry_path = urlparse(entry_url).path.rstrip("/")
    for anchor in soup.find_all("a", href=True):
        text = clean_text(anchor.get_text(" ", strip=True))
        href = urljoin(entry_url, anchor["href"])
        if not is_collectable_url(entry_url, href):
            continue
        parsed = urlparse(href)
        path = parsed.path.rstrip("/")
        query = parsed.query.lower()
        page_like = False
        if re.fullmatch(r"\d{1,3}", text):
            page_like = True
        if any(word in text for word in ["下一页", "尾页", "末页"]):
            page_like = True
        if re.search(r"(?:page|p|pageindex|current|start)=\d+", query):
            page_like = True
        if re.search(r"(?:list_|index_)?\d{1,3}\.html?$", path.lower()):
            page_like = True
        if not page_like:
            continue
        if entry_path and path and not path.startswith(entry_path.rsplit("/", 1)[0]):
            continue
        key = canonical_url(href)
        if key in seen:
            continue
        seen.add(key)
        pages.append(href)
        if len(pages) >= max_pages:
            break
    return pages


def best_detail_scope_text(soup: BeautifulSoup) -> str:
    selectors = [
        "article",
        "main",
        ".main",
        ".content",
        ".cont",
        ".detail",
        ".article",
        ".doctor-detail",
        ".expert-detail",
        ".field-body",
        ".views-field-body",
    ]
    candidates: list[tuple[int, str]] = []
    for selector in selectors:
        for element in soup.select(selector):
            text = strip_profile_navigation_text(compact_visible_text(element, 6000))
            if len(text) < 20:
                continue
            label_score = sum(1 for term in ["姓名", "科室", "职称", "擅长", "简介", "专长"] if term in text)
            title_score = len(extract_terms(text, TITLE_TERMS))
            candidates.append((len(text) + label_score * 500 + title_score * 400, text))
    if candidates:
        return strip_article_tail(max(candidates, key=lambda item: item[0])[1])
    return strip_article_tail(strip_profile_navigation_text(compact_visible_text(soup, 6000)))


def first_visible_heading_text(soup: BeautifulSoup) -> str:
    for heading in soup.find_all(["h1", "h2", "h3"]):
        classes = " ".join(heading.get("class") or []).lower()
        if "hidden" in classes or "breadcrumb" in classes:
            continue
        text = clean_text(heading.get_text(" ", strip=True))
        if text and not any(term in text for term in ["面包屑", "当前位置"]):
            return text
    return ""


def extract_breadcrumb_department(text: str) -> str:
    source = clean_text(text)
    patterns = [
        r"临床科室\s*/\s*[^/]{1,30}\s*/\s*([^/]{1,24}?)\s*/\s*临床专家",
        r"科室导航\s*/\s*[^/]{1,30}\s*/\s*([^/]{1,24}?)\s*/",
        r"首页\s*/\s*临床科室\s*/\s*[^/]{1,30}\s*/\s*([^/]{1,24}?)\s*/",
    ]
    for pattern in patterns:
        match = re.search(pattern, source)
        if not match:
            continue
        candidate = clean_text(match.group(1)).strip("/ ")
        if candidate and not any(term in candidate for term in ["系列", "临床专家", "首页"]):
            return candidate
    return ""


def extract_labeled_value_any(text: str, labels: list[str], stop_labels: list[str]) -> str:
    value = extract_labeled_value(text, labels, stop_labels)
    if value:
        return value
    lines = [clean_text(line) for line in re.split(r"[\n\r]+", text) if clean_text(line)]
    for label in labels:
        value = extract_label_from_lines(lines, label, stop_labels)
        if value:
            return value
    label_pattern = "|".join(re.escape(label) for label in labels)
    stop_pattern = "|".join(re.escape(label) for label in stop_labels + ["一、", "二、", "三、", "四、", "五、", "更新时间", "专科门诊时间", "门诊时间"])
    pattern = rf"(?:^|[\s，,；;。])(?:{label_pattern})\s+(.+?)(?=(?:{stop_pattern})\s*[:：]?|$)"
    match = re.search(pattern, clean_text(text), flags=re.S)
    return clean_text(match.group(1)) if match else ""


def extract_explicit_labeled_value(text: str, labels: list[str], stop_labels: list[str]) -> str:
    value = extract_labeled_value(text, labels, stop_labels)
    if value:
        return value
    lines = [clean_text(line) for line in re.split(r"[\n\r]+", text) if clean_text(line)]
    for label in labels:
        value = extract_label_from_lines(lines, label, stop_labels)
        if value:
            return value
    return ""


def parse_generic_detail(html: str, fallback: dict[str, str]) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = clean_text(soup.title.get_text(" ", strip=True)) if soup.title else ""
    h1 = first_visible_heading_text(soup)
    navigation_context = extract_navigation_context(soup)
    remove_profile_noise_elements(soup)
    raw_scope_text = compact_visible_text(soup, 6000)
    main_text = best_detail_scope_text(soup)
    compact = clean_text("\n".join([h1, title, main_text]))
    name = first_nonempty(
        extract_labeled_value_any(
            compact,
            ["姓名", "专家姓名", "医生姓名", "名称"],
            ["科室", "所在科室", "职称", "专业擅长", "擅长", "专长", "简介"],
        ),
        extract_person_name(h1, title, fallback.get("name", ""), fallback.get("list_title", "")),
    )
    department_raw = first_nonempty(
        extract_labeled_value_any(
            compact,
            ["科室", "所在科室", "出诊科室", "专业", "专科"],
            ["职称", "职务", "专业擅长", "擅长", "专长", "简介", "个人简介"],
        ),
        extract_breadcrumb_department(navigation_context),
        fallback.get("department", ""),
        infer_department(compact[:500]),
    )
    department = clean_generic_department(department_raw)
    title_field = first_nonempty(
        extract_labeled_value_any(
            compact,
            ["职称", "职务", "专家职称", "技术职称"],
            ["科室", "所在科室", "专业擅长", "擅长", "专长", "简介", "个人简介"],
        ),
        "、".join(extract_terms(compact[:1000], TITLE_TERMS)),
        fallback.get("list_title", ""),
    )
    specialty_labels = [
        "专业擅长",
        "擅长",
        "医疗专长",
        "诊疗专长",
        "技术专长",
        "业务专长",
        "专长",
        "研究方向",
    ]
    specialty_stop_labels = [
        "个人简介",
        "简介",
        "介绍",
        "专家简介",
        "医生简介",
        "出诊",
        "门诊",
        "社会任职",
        "学术任职",
    ]
    specialty_raw = strip_article_tail(
        extract_explicit_labeled_value(
            compact,
            specialty_labels,
            specialty_stop_labels,
        )
    )
    specialty_preclean = strip_article_tail(
        extract_explicit_labeled_value(raw_scope_text, specialty_labels, specialty_stop_labels)
    )
    specialty_navigation_polluted = contains_navigation_text(specialty_raw) or contains_navigation_text(
        specialty_preclean
    )
    specialty = "" if specialty_navigation_polluted else specialty_raw
    profile_text = strip_article_tail(
        first_nonempty(
            extract_labeled_value_any(
                compact,
                ["个人简介", "专家简介", "医生简介", "简介", "详细介绍"],
                ["专业擅长", "擅长", "专长", "出诊", "门诊", "上一篇", "下一篇"],
            ),
            main_text,
        )
    )
    return {
        "name": clean_text(name),
        "department": clean_text(department),
        "department_raw": clean_text(department_raw),
        "department_polluted": "yes" if has_department_text_pollution(department_raw, department) else "no",
        "title_field": clean_text(title_field),
        "specialty": clean_text(specialty),
        "specialty_raw": clean_text(first_nonempty(specialty_raw, specialty_preclean)),
        "specialty_navigation_polluted": "yes" if specialty_navigation_polluted else "no",
        "profile_text": clean_text(profile_text),
        "title_text": first_nonempty(h1, title),
    }


def gzzoc_list_pages(entry_url: str, html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    max_page = 0
    for anchor in soup.select(".pager a[href]"):
        parsed = urlparse(urljoin(entry_url, anchor["href"]))
        for name, value in parse_qsl(parsed.query, keep_blank_values=True):
            if name == "page" and value.isdigit():
                max_page = max(max_page, int(value))
    return [with_query_param(entry_url, "page", page) for page in range(max_page + 1)]


def parse_gzzoc_list_page(html: str, page_url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict[str, str]] = []
    for item in soup.select("li.list-item"):
        anchor = item.select_one(".item-name a[href]") or item.select_one('a[href*="/node/"]')
        if not anchor:
            continue
        href = urljoin(page_url, anchor["href"])
        if not re.search(r"/node/\d+$", urlparse(href).path):
            continue
        name = clean_text((item.select_one(".item-name") or anchor).get_text(" ", strip=True))
        list_title = clean_text((item.select_one(".item-post") or item).get_text(" ", strip=True))
        department = clean_text((item.select_one(".item-dept") or item).get_text(" ", strip=True))
        description = clean_text((item.select_one(".item-desc") or item).get_text(" ", strip=True))
        rows.append(
            {
                "source_link": href,
                "name": name,
                "list_title": list_title,
                "department": department,
                "description": description,
                "list_page": page_url,
            }
        )
    return rows


def extract_label_from_lines(lines: list[str], label: str, stop_labels: list[str]) -> str:
    stop_set = {clean_text(stop.rstrip(":：")) for stop in stop_labels}
    label_clean = clean_text(label.rstrip(":："))
    for index, line in enumerate(lines):
        normalized = clean_text(line.rstrip(":："))
        value = ""
        if normalized == label_clean:
            values: list[str] = []
            for next_line in lines[index + 1 :]:
                next_normalized = clean_text(next_line.rstrip(":："))
                if next_normalized in stop_set:
                    break
                if next_line:
                    values.append(next_line)
            return clean_text(" ".join(values))
        for marker in (f"{label_clean}:", f"{label_clean}："):
            if line.startswith(marker):
                value = clean_text(line[len(marker) :])
                break
        if value:
            for stop in stop_labels:
                for marker in (f"{stop}:", f"{stop}：", stop):
                    position = value.find(marker)
                    if position > 0:
                        value = value[:position]
            return clean_text(value)
    return ""


def parse_gzzoc_detail(html: str, fallback: dict[str, str]) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = clean_text(soup.title.get_text(" ", strip=True)) if soup.title else ""
    title_name = title.split("|", 1)[0].strip() if "|" in title else ""
    remove_profile_noise_elements(soup)
    main = soup.select_one(".main") or soup
    lines = [clean_text(line) for line in main.get_text("\n", strip=True).splitlines() if clean_text(line)]

    specialty = clean_text((soup.select_one(".field-adept") or "").get_text(" ", strip=True)) if soup.select_one(".field-adept") else ""
    profile_text = clean_text((soup.select_one(".field-body") or "").get_text(" ", strip=True)) if soup.select_one(".field-body") else ""
    department = extract_label_from_lines(lines, "专业", ["职称", "擅长", "简介", "预约挂号"])
    title_field = extract_label_from_lines(lines, "职称", ["擅长", "简介", "预约挂号"])

    if not specialty:
        specialty = extract_label_from_lines(lines, "擅长", ["简介", "预约挂号", "在线预约"])
    if not profile_text:
        profile_text = extract_label_from_lines(lines, "简介", ["预约挂号", "在线预约", "快速连接"])

    return {
        "name": first_nonempty(title_name, fallback.get("name", "")),
        "department": first_nonempty(department, fallback.get("department", "")),
        "title_field": first_nonempty(title_field, fallback.get("list_title", "")),
        "specialty": specialty,
        "profile_text": profile_text,
        "title_text": title_name,
    }


def collect_gzzoc(target: HospitalTarget, today: str, max_doctors: int | None = None) -> dict[str, Any]:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36; "
                "public official-site collection"
            )
        }
    )
    status, entry_html, entry_error = fetch(session, target.entry_url)
    if status != 200:
        raise RuntimeError(f"入口页读取失败：{entry_error}")

    page_urls = gzzoc_list_pages(target.entry_url, entry_html)
    page_errors: list[dict[str, str]] = []
    raw_rows: list[dict[str, str]] = []
    for index, page_url in enumerate(page_urls, start=1):
        if index == 1 and canonical_url(page_url) == canonical_url(with_query_param(target.entry_url, "page", 0)):
            html = entry_html
            page_status = status
            page_error = ""
        else:
            page_status, html, page_error = fetch(session, page_url)
        if page_status != 200:
            page_errors.append({"page": str(index), "url": page_url, "error": page_error})
            continue
        page_rows = parse_gzzoc_list_page(html, page_url)
        raw_rows.extend(page_rows)
        print(f"[{index}/{len(page_urls)}] list rows: {len(page_rows)}")
        time.sleep(0.2)

    by_link: dict[str, dict[str, str]] = {}
    for row in raw_rows:
        key = canonical_url(row["source_link"])
        item = by_link.setdefault(
            key,
            {
                "source_link": row["source_link"],
                "name": row["name"],
                "list_title": row["list_title"],
                "department": row["department"],
                "description": row["description"],
                "list_pages": "",
            },
        )
        for field in ["name", "list_title", "department", "description"]:
            if row[field] and len(row[field]) > len(item.get(field, "")):
                item[field] = row[field]
        pages = [value for value in item["list_pages"].split("；") if value]
        if row["list_page"] not in pages:
            pages.append(row["list_page"])
            item["list_pages"] = "；".join(pages)

    detail_items = sorted(by_link.values(), key=lambda item: item["source_link"])
    if max_doctors:
        detail_items = detail_items[:max_doctors]

    existing_links = collect_existing_profile_links()
    rows: list[dict[str, Any]] = []
    detail_errors: list[dict[str, str]] = []
    for index, item in enumerate(detail_items, start=1):
        link = item["source_link"]
        detail_status, detail_html, detail_error = fetch(session, link)
        detail = {
            "name": item.get("name", ""),
            "department": item.get("department", ""),
            "title_field": item.get("list_title", ""),
            "specialty": "",
            "profile_text": "",
            "title_text": "",
        }
        if detail_status == 200:
            detail = parse_gzzoc_detail(detail_html, item)
        else:
            detail_errors.append({"source_link": link, "error": detail_error})

        name = first_nonempty(detail.get("name"), item.get("name"))
        department = first_nonempty(detail.get("department"), item.get("department"))
        combined_text = "\n".join(
            [
                target.hospital,
                department,
                item.get("list_title", ""),
                item.get("description", ""),
                detail.get("title_field", ""),
                detail.get("specialty", ""),
                detail.get("profile_text", ""),
            ]
        )
        title_source = first_nonempty(detail.get("title_field"), item.get("list_title"))
        title_hits = extract_terms(title_source, TITLE_TERMS) or extract_terms(combined_text, TITLE_TERMS)
        groups, tags = group_tags(combined_text)
        specialty = clip(
            first_nonempty(
                detail.get("specialty"),
                item.get("description"),
                extract_sentences(
                    combined_text,
                    ["擅长", "研究方向", "诊治", "治疗", "诊断", "手术", "专长", "复杂", "疑难"],
                    limit=4,
                    max_len=520,
                ),
            ),
            520,
        )
        highlights = extract_sentences(combined_text, HIGHLIGHT_TERMS)

        warnings: list[str] = []
        if detail_status != 200:
            warnings.append("详情页读取失败")
        if not name:
            warnings.append("姓名需人工复核")
        if not department:
            warnings.append("专业/科室需人工复核")
        if not title_hits:
            warnings.append("职称/身份需人工复核")
        if not detail.get("specialty") and not detail.get("profile_text") and not item.get("description"):
            warnings.append("详情页正文为空或未识别")

        priority = "普通"
        if any(term in combined_text for term in PRIORITY_DEPARTMENTS) or groups:
            priority = "高"
        elif any(term != "医师" for term in title_hits):
            priority = "中"

        rows.append(
            {
                "序号": index,
                "医院": target.hospital,
                "姓名": name,
                "科室_分类页": department,
                "科室_列表卡片": item.get("department", ""),
                "职称_关键词": "、".join(title_hits),
                "职称身份原文": clip(first_nonempty(detail.get("title_field"), item.get("list_title")), 500),
                "重点优先级": priority,
                "重点关注范围": "、".join(groups),
                "重点疾病标签": "、".join(tags),
                "擅长诊疗方向摘录": specialty,
                "亮眼经历线索": highlights,
                "列表简介": clip(item.get("description", ""), 700),
                "详情正文摘录": clip(detail.get("profile_text", ""), 1800),
                "来源类型": "医院官网",
                "来源链接": link,
                "采集入口": target.entry_url,
                "采集方式": "官网专家列表页+官网医生详情页",
                "采集日期": today,
                "详情页状态": "200" if detail_status == 200 else "失败",
                "已建画像": "是" if canonical_url(link) in existing_links else "否",
                "异常提示": "；".join(warnings),
                "复核状态": "待人工复核",
            }
        )
        if index % 20 == 0:
            print(f"details: {index}/{len(detail_items)}")
        time.sleep(0.18)

    rows.sort(key=lambda row: (row["重点优先级"] != "高", row["科室_分类页"], row["姓名"]))
    for new_index, row in enumerate(rows, start=1):
        row["序号"] = new_index

    category_counter = Counter()
    priority_counter = Counter(row["重点优先级"] for row in rows)
    group_counter = Counter()
    warning_counter = Counter()
    for row in rows:
        if row["科室_分类页"]:
            category_counter[row["科室_分类页"]] += 1
        for group in row["重点关注范围"].split("、"):
            if group:
                group_counter[group] += 1
        for warning in row["异常提示"].split("；"):
            if warning:
                warning_counter[warning] += 1

    return {
        "meta": {
            "city": target.city,
            "hospital": target.hospital,
            "homepage": target.homepage,
            "entry_url": target.entry_url,
            "adapter_id": target.adapter_id,
            "collected_at": today,
            "category_count": len(page_urls),
            "raw_card_rows": len(raw_rows),
            "unique_doctor_count": len(rows),
            "category_error_count": len(page_errors),
            "detail_error_count": len(detail_errors),
            "existing_profile_count": sum(1 for row in rows if row["已建画像"] == "是"),
            "ledger_review": target.review,
            "ledger_difficulty": target.difficulty,
        },
        "categories": [{"category_id": str(index), "category_name": f"专家列表第{index}页", "url": url} for index, url in enumerate(page_urls, start=1)],
        "category_errors": page_errors,
        "detail_errors": detail_errors,
        "category_counts": category_counter.most_common(),
        "priority_counts": dict(priority_counter),
        "group_counts": dict(group_counter),
        "warning_counts": dict(warning_counter),
        "rows": rows,
    }


def nbkj_list_pages(entry_url: str, html: str) -> list[str]:
    page_numbers = [int(match.group(1)) for match in re.finditer(r"(?:/expert/)?list_(\d+)\.html", html)]
    max_page = max(page_numbers) if page_numbers else 1
    pages = [entry_url]
    for page in range(2, max_page + 1):
        pages.append(urljoin(entry_url.rstrip("/") + "/", f"list_{page}.html"))
    return pages


def parse_nbkj_list_page(html: str, page_url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict[str, str]] = []
    for anchor in soup.find_all("a", href=True):
        href = urljoin(page_url, anchor["href"])
        if not re.search(r"/expert/\d+\.html$", urlparse(href).path):
            continue
        text = clean_text(anchor.get_text(" ", strip=True))
        image = anchor.find("img")
        image_alt = clean_text(image.get("alt")) if image else ""
        list_title = first_nonempty(text, image_alt)
        rows.append(
            {
                "source_link": href,
                "list_title": list_title,
                "list_page": page_url,
            }
        )
    return rows


def extract_labeled_value(text: str, labels: list[str], stop_labels: list[str]) -> str:
    label_pattern = "|".join(re.escape(label) for label in labels)
    stop_pattern = "|".join(re.escape(label) for label in stop_labels)
    pattern = rf"(?:{label_pattern})\s*[:：]\s*(.*?)(?=(?:{stop_pattern})\s*[:：]?|上一篇[:：]|下一篇[:：]|相关文章[:：]|南部战区空军医院|$)"
    match = re.search(pattern, text, flags=re.S)
    return clean_text(match.group(1)) if match else ""


def parse_nbkj_detail(html: str, fallback_title: str) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = clean_text(soup.title.get_text(" ", strip=True)) if soup.title else ""
    title_name = title.split("_", 1)[0].strip() if "_" in title else ""
    remove_profile_noise_elements(soup)
    cont = soup.find("div", class_="cont")
    paragraph_scope = cont if cont else soup
    paragraphs = [
        clean_text(paragraph.get_text(" ", strip=True))
        for paragraph in paragraph_scope.find_all("p")
        if clean_text(paragraph.get_text(" ", strip=True))
    ]
    body_text = strip_article_tail(" ".join(paragraphs))
    text = "\n".join(
        clean_text(line)
        for line in soup.get_text("\n", strip=True).splitlines()
        if clean_text(line)
    )
    compact = clean_text(text)
    name = extract_labeled_value(compact, ["姓名", "医生名称"], ["科室", "所在科室", "职称", "专家职称", "专业擅长", "专家专长"])
    department = extract_labeled_value(compact, ["科室", "所在科室"], ["职称", "专家职称", "专家学历", "专业擅长", "专家专长"])
    title_field = extract_labeled_value(compact, ["职称", "专家职称"], ["专家学历", "专业擅长", "专家专长"])
    specialty = strip_article_tail(extract_labeled_value(compact, ["专业擅长", "专家专长"], ["上一篇", "下一篇", "相关文章"]))
    title_context = title_name
    if len(clean_text(fallback_title)) > len(clean_text(title_context)):
        title_context = clean_text(fallback_title)
    title_context = first_nonempty(title_context, fallback_title)
    if not name and title_context:
        name = clean_text(re.split(r"[\s，,、；;]", title_context, maxsplit=1)[0])
    if not name:
        name = title_name.split(" ", 1)[0] if title_name else ""

    title_rest = title_context
    if name and title_rest.startswith(name):
        title_rest = clean_text(title_rest[len(name) :])
    if not department:
        department = infer_department(title_rest) or infer_department(body_text[:180])
    if not title_field:
        title_field = "、".join(extract_terms(f"{title_context} {body_text[:260]}", TITLE_TERMS))
    if not specialty:
        specialty = body_text
    profile_text = strip_article_tail(specialty or body_text)
    return {
        "name": name,
        "department": department,
        "title_field": title_field,
        "specialty": specialty,
        "profile_text": profile_text,
        "title_text": title_name,
    }


def collect_nbkj(target: HospitalTarget, today: str, max_doctors: int | None = None) -> dict[str, Any]:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36; "
                "public official-site collection"
            )
        }
    )
    status, entry_html, entry_error = fetch(session, target.entry_url)
    if status != 200:
        raise RuntimeError(f"入口页读取失败：{entry_error}")

    page_urls = nbkj_list_pages(target.entry_url, entry_html)
    page_errors: list[dict[str, str]] = []
    raw_rows: list[dict[str, str]] = []
    for index, page_url in enumerate(page_urls, start=1):
        if index == 1:
            html = entry_html
            page_status = status
            page_error = ""
        else:
            page_status, html, page_error = fetch(session, page_url)
        if page_status != 200:
            page_errors.append({"page": str(index), "url": page_url, "error": page_error})
            continue
        page_rows = parse_nbkj_list_page(html, page_url)
        raw_rows.extend(page_rows)
        print(f"[{index}/{len(page_urls)}] list rows: {len(page_rows)}")
        time.sleep(0.25)

    by_link: dict[str, dict[str, str]] = {}
    for row in raw_rows:
        key = canonical_url(row["source_link"])
        item = by_link.setdefault(
            key,
            {
                "source_link": row["source_link"],
                "list_title": row["list_title"],
                "list_pages": "",
            },
        )
        if row["list_title"] and len(row["list_title"]) > len(item.get("list_title", "")):
            item["list_title"] = row["list_title"]
        pages = [value for value in item["list_pages"].split("；") if value]
        if row["list_page"] not in pages:
            pages.append(row["list_page"])
            item["list_pages"] = "；".join(pages)

    detail_items = sorted(by_link.values(), key=lambda item: item["source_link"])
    if max_doctors:
        detail_items = detail_items[:max_doctors]

    existing_links = collect_existing_profile_links()
    rows: list[dict[str, Any]] = []
    detail_errors: list[dict[str, str]] = []
    for index, item in enumerate(detail_items, start=1):
        link = item["source_link"]
        detail_status, detail_html, detail_error = fetch(session, link)
        detail = {
            "name": "",
            "department": "",
            "title_field": "",
            "specialty": "",
            "profile_text": "",
            "title_text": "",
        }
        if detail_status == 200:
            detail = parse_nbkj_detail(detail_html, item.get("list_title", ""))
        else:
            detail_errors.append({"source_link": link, "error": detail_error})

        name = first_nonempty(detail.get("name"), item.get("list_title"))
        department = clean_text(detail.get("department"))
        combined_text = "\n".join(
            [
                target.hospital,
                department,
                item.get("list_title", ""),
                detail.get("title_field", ""),
                detail.get("specialty", ""),
                detail.get("profile_text", ""),
            ]
        )
        title_hits = extract_terms(combined_text, TITLE_TERMS)
        groups, tags = group_tags(combined_text)
        specialty = clip(
            first_nonempty(
                detail.get("specialty"),
                extract_sentences(
                    combined_text,
                    ["擅长", "研究方向", "诊治", "治疗", "诊断", "手术", "放疗", "介入", "专长"],
                    limit=4,
                    max_len=520,
                ),
            ),
            520,
        )
        highlights = extract_sentences(combined_text, HIGHLIGHT_TERMS)

        warnings: list[str] = []
        if detail_status != 200:
            warnings.append("详情页读取失败")
        if not name:
            warnings.append("姓名需人工复核")
        if not department:
            warnings.append("科室需人工复核")
        if not title_hits:
            warnings.append("职称/身份需人工复核")
        if not detail.get("specialty") and not detail.get("profile_text"):
            warnings.append("详情页正文为空或未识别")

        priority = "普通"
        if any(term in combined_text for term in PRIORITY_DEPARTMENTS) or groups:
            priority = "高"
        elif any(term != "医师" for term in title_hits):
            priority = "中"

        rows.append(
            {
                "序号": index,
                "医院": target.hospital,
                "姓名": name,
                "科室_分类页": department,
                "科室_列表卡片": item.get("list_title", ""),
                "职称_关键词": "、".join(title_hits),
                "职称身份原文": clip(first_nonempty(detail.get("title_field"), item.get("list_title")), 500),
                "重点优先级": priority,
                "重点关注范围": "、".join(groups),
                "重点疾病标签": "、".join(tags),
                "擅长诊疗方向摘录": specialty,
                "亮眼经历线索": highlights,
                "列表简介": clip(item.get("list_title", ""), 700),
                "详情正文摘录": clip(detail.get("profile_text", ""), 1800),
                "来源类型": "医院官网",
                "来源链接": link,
                "采集入口": target.entry_url,
                "采集方式": "官网专家列表页+官网医生详情页",
                "采集日期": today,
                "详情页状态": "200" if detail_status == 200 else "失败",
                "已建画像": "是" if canonical_url(link) in existing_links else "否",
                "异常提示": "；".join(warnings),
                "复核状态": "待人工复核",
            }
        )
        if index % 20 == 0:
            print(f"details: {index}/{len(detail_items)}")
        time.sleep(0.22)

    rows.sort(key=lambda row: (row["重点优先级"] != "高", row["科室_分类页"], row["姓名"]))
    for new_index, row in enumerate(rows, start=1):
        row["序号"] = new_index

    category_counter = Counter()
    priority_counter = Counter(row["重点优先级"] for row in rows)
    group_counter = Counter()
    warning_counter = Counter()
    for row in rows:
        if row["科室_分类页"]:
            category_counter[row["科室_分类页"]] += 1
        for group in row["重点关注范围"].split("、"):
            if group:
                group_counter[group] += 1
        for warning in row["异常提示"].split("；"):
            if warning:
                warning_counter[warning] += 1

    return {
        "meta": {
            "city": target.city,
            "hospital": target.hospital,
            "homepage": target.homepage,
            "entry_url": target.entry_url,
            "adapter_id": target.adapter_id,
            "collected_at": today,
            "category_count": len(page_urls),
            "raw_card_rows": len(raw_rows),
            "unique_doctor_count": len(rows),
            "category_error_count": len(page_errors),
            "detail_error_count": len(detail_errors),
            "existing_profile_count": sum(1 for row in rows if row["已建画像"] == "是"),
            "ledger_review": target.review,
            "ledger_difficulty": target.difficulty,
        },
        "categories": [{"category_id": str(index), "category_name": f"专家列表第{index}页", "url": url} for index, url in enumerate(page_urls, start=1)],
        "category_errors": page_errors,
        "detail_errors": detail_errors,
        "category_counts": category_counter.most_common(),
        "priority_counts": dict(priority_counter),
        "group_counts": dict(group_counter),
        "warning_counts": dict(warning_counter),
        "rows": rows,
    }


def collect_generic(
    target: HospitalTarget,
    today: str,
    max_doctors: int | None = None,
    max_pages: int = GENERIC_MAX_PAGES_DEFAULT,
) -> dict[str, Any]:
    session = create_official_session()
    status, entry_html, entry_error = fetch(session, target.entry_url)
    if status != 200:
        raise RuntimeError(f"入口页读取失败：{entry_error}")

    page_urls = discover_generic_list_pages(target.entry_url, entry_html, max_pages=max_pages)
    page_errors: list[dict[str, str]] = []
    raw_rows: list[dict[str, str]] = []
    for index, page_url in enumerate(page_urls, start=1):
        if index == 1:
            html = entry_html
            page_status = status
            page_error = ""
        else:
            page_status, html, page_error = fetch(session, page_url)
        if page_status != 200:
            page_errors.append({"page": str(index), "url": page_url, "error": page_error})
            continue
        page_rows = discover_generic_detail_links(html, page_url, target.entry_url)
        raw_rows.extend(page_rows)
        print(f"[{index}/{len(page_urls)}] generic list rows: {len(page_rows)}")
        time.sleep(0.2)

    by_link: dict[str, dict[str, str]] = {}
    for row in raw_rows:
        key = canonical_url(row["source_link"])
        item = by_link.setdefault(
            key,
            {
                "source_link": row["source_link"],
                "name": row.get("name", ""),
                "list_title": row.get("list_title", ""),
                "department": row.get("department", ""),
                "description": row.get("description", ""),
                "list_pages": "",
                "score": row.get("score", ""),
            },
        )
        for field in ["name", "list_title", "department", "description"]:
            if row.get(field, "") and len(row.get(field, "")) > len(item.get(field, "")):
                item[field] = row[field]
        if int(row.get("score") or 0) > int(item.get("score") or 0):
            item["score"] = row.get("score", "")
        pages = [value for value in item["list_pages"].split("；") if value]
        if row["list_page"] not in pages:
            pages.append(row["list_page"])
            item["list_pages"] = "；".join(pages)

    detail_items = sorted(by_link.values(), key=lambda item: item["source_link"])
    if max_doctors:
        detail_items = detail_items[:max_doctors]

    existing_links = collect_existing_profile_links()
    rows: list[dict[str, Any]] = []
    detail_errors: list[dict[str, str]] = []
    for index, item in enumerate(detail_items, start=1):
        link = item["source_link"]
        detail_status, detail_html, detail_error = fetch(session, link)
        detail = {
            "name": item.get("name", ""),
            "department": item.get("department", ""),
            "title_field": item.get("list_title", ""),
            "specialty": "",
            "profile_text": "",
            "title_text": "",
            "department_raw": item.get("department", ""),
            "department_polluted": "no",
            "specialty_raw": "",
            "specialty_navigation_polluted": "no",
        }
        if detail_status == 200:
            detail = parse_generic_detail(detail_html, item)
        else:
            detail_errors.append({"source_link": link, "error": detail_error})

        name = first_nonempty(detail.get("name"), item.get("name"))
        department = first_nonempty(detail.get("department"), item.get("department"))
        combined_text = "\n".join(
            [
                target.hospital,
                department,
                item.get("list_title", ""),
                item.get("description", ""),
                detail.get("title_field", ""),
                detail.get("specialty", ""),
                detail.get("profile_text", ""),
            ]
        )
        title_source = first_nonempty(detail.get("title_field"), item.get("list_title"))
        title_hits = extract_terms(title_source, TITLE_TERMS) or extract_terms(combined_text, TITLE_TERMS)
        valid_doctor_record, quality_warnings = generic_record_quality(
            name,
            link,
            target.entry_url,
            detail,
            item,
        )
        priority, groups, tags = classify_generic_record(valid_doctor_record, combined_text, title_hits)
        specialty = clip(detail.get("specialty"), 520) if valid_doctor_record else ""
        highlights = extract_sentences(combined_text, HIGHLIGHT_TERMS)

        warnings: list[str] = []
        if detail_status != 200:
            warnings.append("详情页读取失败")
        warnings.extend(quality_warnings)
        if not name:
            warnings.append("姓名需人工复核")
        if not department:
            warnings.append("科室需人工复核")
        if not title_hits:
            warnings.append("职称/身份需人工复核")
        if not detail.get("specialty") and not detail.get("profile_text") and not item.get("description"):
            warnings.append("详情页正文为空或未识别")
        if int(item.get("score") or 0) < 8:
            warnings.append("通用模板低置信度")

        rows.append(
            {
                "序号": index,
                "医院": target.hospital,
                "姓名": name,
                "科室_分类页": department,
                "科室_列表卡片": item.get("department", ""),
                "职称_关键词": "、".join(title_hits),
                "职称身份原文": clip(first_nonempty(detail.get("title_field"), item.get("list_title")), 500),
                "重点优先级": priority,
                "重点关注范围": "、".join(groups),
                "重点疾病标签": "、".join(tags),
                "擅长诊疗方向摘录": specialty,
                "亮眼经历线索": highlights,
                "列表简介": clip(item.get("description", ""), 700),
                "详情正文摘录": clip(detail.get("profile_text", ""), 1800),
                "来源类型": "医院官网",
                "来源链接": link,
                "采集入口": target.entry_url,
                "采集方式": "医院官网通用模板：列表页自动发现+详情页文本抽取",
                "采集日期": today,
                "详情页状态": "200" if detail_status == 200 else "失败",
                "已建画像": "是" if canonical_url(link) in existing_links else "否",
                "异常提示": "；".join(warnings),
                "复核状态": "待人工复核",
            }
        )
        if index % 20 == 0:
            print(f"generic details: {index}/{len(detail_items)}")
        time.sleep(0.18)

    rows.sort(key=lambda row: (row["重点优先级"] != "高", row["科室_分类页"], row["姓名"]))
    for new_index, row in enumerate(rows, start=1):
        row["序号"] = new_index

    category_counter = Counter()
    priority_counter = Counter(row["重点优先级"] for row in rows)
    group_counter = Counter()
    warning_counter = Counter()
    for row in rows:
        if row["科室_分类页"]:
            category_counter[row["科室_分类页"]] += 1
        for group in row["重点关注范围"].split("、"):
            if group:
                group_counter[group] += 1
        for warning in row["异常提示"].split("；"):
            if warning:
                warning_counter[warning] += 1

    return {
        "meta": {
            "city": target.city,
            "hospital": target.hospital,
            "homepage": target.homepage,
            "entry_url": target.entry_url,
            "adapter_id": target.adapter_id,
            "collected_at": today,
            "category_count": len(page_urls),
            "raw_card_rows": len(raw_rows),
            "unique_doctor_count": len(rows),
            "category_error_count": len(page_errors),
            "detail_error_count": len(detail_errors),
            "existing_profile_count": sum(1 for row in rows if row["已建画像"] == "是"),
            "ledger_review": target.review,
            "ledger_difficulty": target.difficulty,
            "generic_template": "yes",
            "generic_max_pages": max_pages,
        },
        "categories": [
            {"category_id": str(index), "category_name": f"通用模板列表第{index}页", "url": url}
            for index, url in enumerate(page_urls, start=1)
        ],
        "category_errors": page_errors,
        "detail_errors": detail_errors,
        "category_counts": category_counter.most_common(),
        "priority_counts": dict(priority_counter),
        "group_counts": dict(group_counter),
        "warning_counts": dict(warning_counter),
        "rows": rows,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BASE_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def render_counter_table(counter: dict[str, int] | list[tuple[str, int]], empty: str = "| 无 | 0 |") -> str:
    items = counter.items() if isinstance(counter, dict) else counter
    lines = [f"| {name} | {count} |" for name, count in items if name]
    return "\n".join(lines) if lines else empty


def write_report(path: Path, payload: dict[str, Any], csv_path: Path, xlsx_path: Path) -> None:
    meta = payload["meta"]
    top_departments = render_counter_table(payload["category_counts"][:20])
    group_lines = render_counter_table(dict(sorted(payload["group_counts"].items())))
    warning_lines = render_counter_table(payload["warning_counts"])
    category_error_lines = "\n".join(
        f"| {err.get('page', '')} | {err.get('url', '')} | {err.get('error', '')} |"
        for err in payload["category_errors"]
    )
    if not category_error_lines:
        category_error_lines = "| 无 | 无 | 无 |"
    detail_error_lines = "\n".join(
        f"| {err.get('source_link', '')} | {err.get('error', '')} |"
        for err in payload["detail_errors"][:50]
    )
    if not detail_error_lines:
        detail_error_lines = "| 无 | 无 |"

    report = f"""---
类型: 自动采集试跑报告
医院: {meta['hospital']}
城市: {meta['city']}
采集日期: {meta['collected_at']}
来源范围: 医院官网
采集入口: {meta['entry_url']}
适配器: {meta['adapter_id']}
---

# {meta['hospital']} 全院医生自动采集试跑报告

## 结论

本次试跑只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成全院医生自动采集底表，共 {meta['unique_doctor_count']} 位唯一医生；官网列表页原始卡片记录 {meta['raw_card_rows']} 条；识别到官网列表分页 {meta['category_count']} 页；详情页失败 {meta['detail_error_count']} 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | {meta['city']} |
| 医院 | {meta['hospital']} |
| 官网首页 | {meta['homepage']} |
| 医生入口 | {meta['entry_url']} |
| 台账人工复核 | {meta['ledger_review']} |
| 采集难度初判 | {meta['ledger_difficulty']} |

## 输出文件

- Excel 底表：`{xlsx_path}`
- CSV 底表：`{csv_path}`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 官网列表分页数 | {meta['category_count']} |
| 原始医生卡片记录 | {meta['raw_card_rows']} |
| 唯一医生详情页 | {meta['unique_doctor_count']} |
| 列表页失败数 | {meta['category_error_count']} |
| 详情页失败数 | {meta['detail_error_count']} |
| 已建画像匹配数 | {meta['existing_profile_count']} |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
{group_lines}

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
{top_departments}

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
{warning_lines}

## 列表页读取异常

| 页码 | URL | 错误 |
|---|---|---|
{category_error_lines}

## 详情页读取异常

| 来源链接 | 错误 |
|---|---|
{detail_error_lines}

## 人工复核建议

1. 优先复核“异常提示”不为空的医生。
2. “亮眼经历线索”只作为官方证据线索，不直接改写为对外宣传语。
3. 官网没有展示的擅长、经历、疾病标签保持空白，不补造。
4. 专用适配器结果可直接进入正式追加；通用模板结果需先完成小样本试采复核，确认字段质量后再全量追加。

## 合规边界

- 仅使用医院官网公开网页。
- 不采集私人电话、私人微信、家庭住址、患者隐私或非公开排班信息。
- 不使用第三方医疗平台评价、排名、患者评论。
- 不写“保证治愈”“包治疑难杂症”“疗效第一”等无法由官网证明的表达。
"""
    path.write_text(report, encoding="utf-8")


def write_master_report(path: Path, payload: dict[str, Any], csv_path: Path, xlsx_path: Path) -> None:
    meta = payload["meta"]
    hospital_lines = "\n".join(
        (
            f"| {row.get('医院', '')} | {row.get('医生数', 0)} | {row.get('采集日期', '')} | "
            f"{row.get('待复核数', 0)} | {row.get('已建画像数', 0)} | {row.get('采集入口', '')} |"
        )
        for row in payload.get("hospital_batches", [])
    )
    if not hospital_lines:
        hospital_lines = "| 无 | 0 |  | 0 | 0 |  |"

    group_lines = render_counter_table(dict(sorted(payload["group_counts"].items())))
    warning_lines = render_counter_table(payload["warning_counts"])

    report = f"""---
类型: 自动采集总底表更新报告
范围: 珠三角三甲医院
采集日期: {meta['collected_at']}
来源范围: 医院官网
适配器: {meta['adapter_id']}
---

# 珠三角三甲医院医生画像自动采集总底表更新报告

## 结论

总底表当前包含 {meta['hospital_count']} 家医院、{meta['unique_doctor_count']} 位医生。后续新增医院医生将继续写入同一张总底表，不再默认生成单院 Excel/CSV。

本次批次医院：{meta.get('current_batch_hospital') or '无，本次仅重建总表'}；本次批次原始医生数 {meta.get('current_batch_rows', 0)}；新增写入 {meta.get('new_rows_added', 0)}；重复跳过 {meta.get('duplicate_rows_skipped', 0)}；初始化合并时识别并折叠既有重复 {meta.get('existing_duplicate_rows', 0)}。

## 输出文件

- Excel 总底表：`{xlsx_path}`
- CSV 总底表：`{csv_path}`

## 医院批次说明

| 医院 | 医生数 | 采集日期 | 待复核数 | 已建画像数 | 采集入口 |
|---|---:|---|---:|---:|---|
{hospital_lines}

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
{group_lines}

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
{warning_lines}

## 合规边界

- 仅使用医院官网公开网页。
- 不采集私人电话、私人微信、家庭住址、患者隐私或非公开排班信息。
- 不使用第三方医疗平台评价、排名、患者评论。
- 官网没有展示的信息保持空白，不推断、不补造。
"""
    path.write_text(report, encoding="utf-8")


def find_node() -> str:
    if BUNDLED_NODE.exists():
        return str(BUNDLED_NODE)
    node = shutil.which("node")
    if node:
        return node
    raise RuntimeError("未找到 Node.js，无法生成 Excel 底表。")


def build_workbook(json_path: Path, xlsx_path: Path, preview_path: Path) -> None:
    if not WORKBOOK_BUILDER.exists():
        raise RuntimeError(f"Excel 生成脚本不存在：{WORKBOOK_BUILDER}")
    command = [
        find_node(),
        str(WORKBOOK_BUILDER),
        "--json",
        str(json_path),
        "--xlsx",
        str(xlsx_path),
    ]
    completed = subprocess.run(command, cwd=str(WORK_DIR), check=False)
    if completed.returncode != 0 and not xlsx_path.exists():
        raise RuntimeError(f"Excel 生成失败，退出码：{completed.returncode}")
    if completed.returncode != 0:
        print(f"[WARN] Excel 生成器返回非零退出码 {completed.returncode}，但输出文件已存在，继续生成报告。")
    inspect_path = Path(f"{xlsx_path}.inspect.ndjson")
    if inspect_path.exists():
        inspect_path.unlink()


def select_target(rows: list[dict[str, Any]], hospital: str | None) -> HospitalTarget:
    targets = confirmed_a_targets(rows, include_generic=bool(hospital))
    if not targets:
        generic_targets = confirmed_a_targets(rows, include_generic=True)
        if not hospital and generic_targets:
            supported = "、".join(target.hospital for target in generic_targets)
            raise RuntimeError(f"当前只有通用模板候选医院，请用 --hospital 指定医院后先试采。当前候选：{supported}")
        raise RuntimeError("台账中没有找到已确认可采集的A级医院；请先补齐官网入口台账。")
    if hospital:
        for target in targets:
            if target.hospital == hospital:
                return target
        supported = "、".join(target.hospital for target in targets)
        raise RuntimeError(f"未找到指定医院的已确认A级采集入口。当前可测试：{supported}")

    dedicated_targets = [target for target in targets if target.adapter_id != GENERIC_ADAPTER_ID]
    if dedicated_targets:
        return dedicated_targets[0]

    supported = "、".join(target.hospital for target in confirmed_a_targets(rows, include_generic=True))
    raise RuntimeError(f"当前只有通用模板候选医院，请用 --hospital 指定医院后先试采。当前候选：{supported}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从已人工确认的医院官网入口批量采集医生基础画像底表。")
    parser.add_argument("--ledger", default=str(LEDGER_PATH), help="官网入口台账路径")
    parser.add_argument("--hospital", default="", help="指定医院名称；为空则选择首个已确认A级且已有适配器的医院")
    parser.add_argument("--today", default=date.today().isoformat(), help="采集日期")
    parser.add_argument("--max-doctors", type=int, default=0, help="仅测试前 N 位医生；0 表示全量")
    parser.add_argument("--max-pages", type=int, default=GENERIC_MAX_PAGES_DEFAULT, help="通用模板最多读取的列表分页数")
    parser.add_argument("--trial-only", action="store_true", help="仅试采并输出临时底表/报告，不追加统一总底表；未指定 --max-doctors 时默认试采 10 位")
    parser.add_argument("--force-generic", action="store_true", help="即使已有专用适配器，也强制使用通用模板试采")
    parser.add_argument("--allow-generic-append", action="store_true", help="允许通用模板结果追加统一总底表；建议先完成 --trial-only 人工复核")
    parser.add_argument("--no-xlsx", action="store_true", help="只生成 JSON/CSV/报告，不生成 Excel")
    parser.add_argument("--single-output", action="store_true", help="保留旧模式：按单家医院生成单独底表")
    parser.add_argument("--rebuild-master-only", action="store_true", help="不联网采集，仅用已有底表重建总底表")
    parser.add_argument("--list-targets", action="store_true", help="列出当前已确认A级医院；无专用适配器的医院标记为通用模板候选")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    ledger_rows = read_ledger(Path(args.ledger))
    if args.list_targets:
        targets = confirmed_a_targets(ledger_rows, include_generic=True)
        print(json.dumps([target.__dict__ for target in targets], ensure_ascii=False, indent=2))
        return

    if args.rebuild_master_only:
        payload = build_master_payload(args.today)
        MASTER_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_csv(MASTER_CSV_PATH, payload["rows"])
        if not args.no_xlsx:
            build_workbook(MASTER_JSON_PATH, MASTER_XLSX_PATH, MASTER_PREVIEW_PATH)
        write_master_report(MASTER_REPORT_PATH, payload, MASTER_CSV_PATH, MASTER_XLSX_PATH)
        print(
            json.dumps(
                {
                    "mode": "master_rebuild",
                    "hospitals": payload["meta"]["hospital_count"],
                    "rows": payload["meta"]["unique_doctor_count"],
                    "xlsx": str(MASTER_XLSX_PATH),
                    "csv": str(MASTER_CSV_PATH),
                    "report": str(MASTER_REPORT_PATH),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    target = select_target(ledger_rows, args.hospital or None)
    if args.force_generic:
        target = replace(target, adapter_id=GENERIC_ADAPTER_ID)
    print(f"selected: {target.city} {target.hospital} {target.entry_url} adapter={target.adapter_id}")

    if (
        target.adapter_id == GENERIC_ADAPTER_ID
        and not args.trial_only
        and not args.single_output
        and not args.allow_generic_append
    ):
        raise RuntimeError(
            "通用模板结果存在误识别风险。请先运行 --trial-only --max-doctors 10 试采复核；"
            "确认质量可接受后，再增加 --allow-generic-append 全量追加统一总底表。"
        )

    max_doctors = args.max_doctors or (10 if args.trial_only else None)
    if target.adapter_id == "gzzoc_drupal_doctor":
        payload = collect_gzzoc(target, args.today, max_doctors=max_doctors)
    elif target.adapter_id == "nbkjyy_static_expert":
        payload = collect_nbkj(target, args.today, max_doctors=max_doctors)
    elif target.adapter_id == GENERIC_ADAPTER_ID:
        payload = collect_generic(target, args.today, max_doctors=max_doctors, max_pages=args.max_pages)
    else:
        raise RuntimeError(f"暂不支持的适配器：{target.adapter_id}")

    safe_name = safe_file_part(target.hospital)
    json_path = WORK_DIR / f"{safe_name}_official_doctors_payload.json"
    preview_path = WORK_DIR / f"{safe_name}_official_doctors_preview.png"

    if args.trial_only:
        json_path = WORK_DIR / f"{safe_name}_trial_payload.json"
        csv_path = WORK_DIR / f"{safe_name}_trial_doctors.csv"
        xlsx_path = WORK_DIR / f"{safe_name}_trial_doctors.xlsx"
        report_path = WORK_DIR / f"{safe_name}_trial_report.md"

        payload["meta"]["json_path"] = str(json_path)
        payload["meta"]["csv_path"] = str(csv_path)
        payload["meta"]["xlsx_path"] = str(xlsx_path)
        payload["meta"]["preview_path"] = str(preview_path)

        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_csv(csv_path, payload["rows"])

        if not args.no_xlsx:
            build_workbook(json_path, xlsx_path, preview_path)

        write_report(report_path, payload, csv_path, xlsx_path)
        print(
            json.dumps(
                {
                    "mode": "trial_only",
                    "hospital": target.hospital,
                    "adapter_id": target.adapter_id,
                    "rows": payload["meta"]["unique_doctor_count"],
                    "detail_errors": payload["meta"]["detail_error_count"],
                    "csv": str(csv_path),
                    "xlsx": str(xlsx_path),
                    "report": str(report_path),
                    "master_updated": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.single_output:
        csv_path = SOURCE_DIR / f"{target.hospital}_全院医生自动采集底表.csv"
        xlsx_path = SOURCE_DIR / f"{target.hospital}_全院医生自动采集底表.xlsx"
        report_path = SOURCE_DIR / f"{target.hospital}_全院医生自动采集试跑报告.md"

        payload["meta"]["json_path"] = str(json_path)
        payload["meta"]["csv_path"] = str(csv_path)
        payload["meta"]["xlsx_path"] = str(xlsx_path)
        payload["meta"]["preview_path"] = str(preview_path)

        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_csv(csv_path, payload["rows"])

        if not args.no_xlsx:
            build_workbook(json_path, xlsx_path, preview_path)

        write_report(report_path, payload, csv_path, xlsx_path)
        print(
            json.dumps(
                {
                    "mode": "single_output",
                    "hospital": target.hospital,
                    "rows": payload["meta"]["unique_doctor_count"],
                    "detail_errors": payload["meta"]["detail_error_count"],
                    "csv": str(csv_path),
                    "xlsx": str(xlsx_path),
                    "report": str(report_path),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    master_payload = build_master_payload(args.today, incoming_payload=payload)
    MASTER_JSON_PATH.write_text(json.dumps(master_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(MASTER_CSV_PATH, master_payload["rows"])

    if not args.no_xlsx:
        build_workbook(MASTER_JSON_PATH, MASTER_XLSX_PATH, MASTER_PREVIEW_PATH)

    write_master_report(MASTER_REPORT_PATH, master_payload, MASTER_CSV_PATH, MASTER_XLSX_PATH)
    print(
        json.dumps(
            {
                "mode": "master_append",
                "hospital": target.hospital,
                "batch_rows": payload["meta"]["unique_doctor_count"],
                "new_rows_added": master_payload["meta"]["new_rows_added"],
                "duplicate_rows_skipped": master_payload["meta"]["duplicate_rows_skipped"],
                "master_rows": master_payload["meta"]["unique_doctor_count"],
                "detail_errors": payload["meta"]["detail_error_count"],
                "csv": str(MASTER_CSV_PATH),
                "xlsx": str(MASTER_XLSX_PATH),
                "report": str(MASTER_REPORT_PATH),
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
    except Exception as exc:  # noqa: BLE001 - CLI should report exact blocker
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
