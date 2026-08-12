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
from difflib import SequenceMatcher
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
    Path.home()
    / ".cache"
    / "codex-runtimes"
    / "codex-primary-runtime"
    / "dependencies"
    / "node"
    / "bin"
    / "node.exe"
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
    "主任中医师",
    "副主任中医师",
    "主治中医师",
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
GDSKIN_ADAPTER_ID = "gdskin_aspnet_expert"
NY5Y_ADAPTER_ID = "ny5y_official_expert"
GDZY5413_ADAPTER_ID = "gdzy5413_official_specialist"
GYKQYY_ADAPTER_ID = "gykqyy_public_doctor_api"
GYKQYY_DIRECTORY_API = "https://www.gykqyy.com/api/article/getZhuanjiaList"
GYKQYY_DETAIL_API = "https://www.gykqyy.com/api/article/getArticleDetail"
GENERIC_MAX_PAGES_DEFAULT = 60
GDSKIN_ENTRY_METADATA = {
    "901": {
        "category_name": "首席专家",
        "affiliation": "南方医科大学皮肤病医院（官网专家团队栏目）",
    },
    "902": {
        "category_name": "知名专家",
        "affiliation": "南方医科大学皮肤病医院（官网专家团队栏目）",
    },
    "906": {
        "category_name": "皮肤内科",
        "affiliation": "南方医科大学皮肤病医院（官网专家团队栏目）",
    },
    "910": {
        "category_name": "外阴皮肤病/性病科",
        "affiliation": "南方医科大学皮肤病医院（官网专家团队栏目）",
    },
    "913": {
        "category_name": "整形美容外科",
        "affiliation": "南方医科大学皮肤病医院（官网专家团队栏目）",
    },
    "915": {
        "category_name": "中医皮肤科",
        "affiliation": "南方医科大学皮肤病医院（官网专家团队栏目）",
    },
    "917": {
        "category_name": "激光美肤中心",
        "affiliation": "南方医科大学皮肤病医院（官网专家团队栏目）",
    },
    "921": {
        "category_name": "皮肤外科",
        "affiliation": "南方医科大学皮肤病医院（官网专家团队栏目）",
    },
    "922": {
        "category_name": "儿童皮肤科",
        "affiliation": "南方医科大学皮肤病医院（官网专家团队栏目）",
    },
    "924": {
        "category_name": "珠江新城医学美容中心",
        "affiliation": "南方医科大学皮肤病医院·珠江新城医学美容中心",
    },
}
GDSKIN_GENERAL_CATEGORIES = {"首席专家", "知名专家"}
GDSKIN_EXPECTED_ENTRY_COUNTS = {
    "901": 1,
    "902": 3,
    "906": 29,
    "910": 7,
    "913": 8,
    "915": 14,
    "917": 6,
    "921": 4,
    "922": 5,
    "924": 0,
}
GDSKIN_EXPECTED_PAGE_COUNTS = {entry_id: (2 if entry_id == "906" else 1) for entry_id in GDSKIN_ENTRY_METADATA}
GDSKIN_DOCTOR_ROLE_TERMS = [
    "主任医师",
    "副主任医师",
    "主治医师",
    "住院医师",
    "主管医师",
    "医师",
    "医生",
    "首席专家",
]
NY5Y_ENTRY_METADATA = {
    "100": {
        "path": "/zhuanjia_mingyi.php",
        "category_name": "专家风采",
        "affiliation": "南方医科大学第五附属医院（官网专家风采栏目）",
    },
    "162": {
        "path": "/zhuanjia_lingnan.php",
        "category_name": "岭南名医",
        "affiliation": "南方医科大学第五附属医院（官网岭南名医荣誉栏目）",
    },
}
NY5Y_GENERAL_CATEGORIES = {"专家风采", "岭南名医"}
NY5Y_EXPECTED_ENTRY_COUNTS = {"100": 133, "162": 80}
NY5Y_EXPECTED_UNIQUE_COUNT = 134
NY5Y_EXPECTED_CROSS_ENTRY_DUPLICATES = 79
GDZY5413_ENTRY_METADATA = {
    "851": {
        "category_name": "名医名家",
        "affiliation": "广东省第二中医院（官网名医名家栏目）",
    },
    "852": {
        "category_name": "各科专家",
        "affiliation": "广东省第二中医院（官网各科专家栏目）",
    },
}
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
    entry_urls: tuple[str, ...] = ()
    ledger_entry_url: str = ""


def effective_entry_urls(target: HospitalTarget) -> list[str]:
    values = target.entry_urls or (target.entry_url,)
    unique: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = clean_text(value)
        key = canonical_url(cleaned)
        if cleaned and key not in seen:
            seen.add(key)
            unique.append(cleaned)
    return unique


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


def extract_gdzy5413_department(title_text: str | None, profile_text: str | None) -> str:
    source = clean_text(" ".join(value for value in [title_text, profile_text] if value))
    patterns = [
        r"广东省第二中医院([\u4e00-\u9fff\d]{1,20}(?:科|中心)(?:[一二三四五六七八九十\d]+区)?)\s*(?:主任|区长|负责人)",
        r"([\u4e00-\u9fff\d]{1,20}(?:科|中心)(?:[一二三四五六七八九十\d]+区)?)\s*(?:主任|区长|负责人)",
        r"([\u4e00-\u9fff\d]{1,20}科)主任(?:中|西)医师",
    ]
    blocked = {"医务科"}
    for pattern in patterns:
        match = re.search(pattern, source)
        if not match:
            continue
        candidate = clean_text(match.group(1))
        if candidate and candidate not in blocked:
            return candidate
    return ""


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
    warnings = clean_text(str(row.get("异常提示") or ""))
    if "同名待甄别" in warnings and hospital and source:
        return ("source", hospital, canonical_url(source))
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
    refresh_incoming: bool = False,
) -> tuple[list[dict[str, Any]], int, int, int, int]:
    merged: list[dict[str, Any]] = []
    index_by_key: dict[tuple[str, ...], int] = {}
    existing_duplicates = 0
    incoming_added = 0
    incoming_skipped = 0
    incoming_refreshed = 0

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
            if refresh_incoming:
                merged[index_by_key[key]] = normalized
                incoming_refreshed += 1
            else:
                incoming_skipped += 1
            continue
        index_by_key[key] = len(merged)
        merged.append(normalized)
        incoming_added += 1

    for index, row in enumerate(merged, start=1):
        row["序号"] = index
    return merged, incoming_added, incoming_skipped, incoming_refreshed, existing_duplicates


def build_hospital_batches(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        hospital = clean_text(str(row.get("医院") or "未识别医院"))
        grouped.setdefault(hospital, []).append(row)

    batches: list[dict[str, Any]] = []
    for hospital, hospital_rows in sorted(grouped.items()):
        dates = sorted({clean_text(str(row.get("采集日期") or "")) for row in hospital_rows if row.get("采集日期")})
        review_count = sum(1 for row in hospital_rows if clean_text(str(row.get("复核状态") or "")) != "已复核")
        entry_urls = list(
            dict.fromkeys(
                clean_text(str(row.get("采集入口") or ""))
                for row in hospital_rows
                if clean_text(str(row.get("采集入口") or ""))
            )
        )
        batches.append(
            {
                "医院": hospital,
                "医生数": len(hospital_rows),
                "采集日期": "、".join(dates),
                "待复核数": review_count,
                "已建画像数": sum(1 for row in hospital_rows if clean_text(str(row.get("已建画像") or "")) == "是"),
                "采集入口": "、".join(entry_urls),
            }
        )
    return batches


def sync_profile_flags(rows: list[dict[str, Any]], profile_links: set[str]) -> None:
    normalized_profile_links = {canonical_url(link) for link in profile_links if canonical_url(link)}
    for row in rows:
        source = canonical_url(str(row.get("来源链接") or ""))
        row["已建画像"] = "是" if source and source in normalized_profile_links else "否"


def build_master_payload(
    today: str,
    incoming_payload: dict[str, Any] | None = None,
    refresh_incoming: bool = False,
    replace_incoming_hospital: bool = False,
    batch_meta_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    existing_rows, source_label, preserve_existing = load_existing_rows_for_master()
    incoming_rows = incoming_payload["rows"] if incoming_payload else []
    incoming_hospital = clean_text(
        str((incoming_payload or {}).get("meta", {}).get("hospital") or "")
    )
    if replace_incoming_hospital and incoming_hospital:
        existing_rows = [
            row
            for row in existing_rows
            if clean_text(str(row.get("医院") or "")) != incoming_hospital
        ]
    rows, added, skipped, refreshed, existing_duplicates = merge_rows_for_master(
        existing_rows,
        incoming_rows,
        preserve_existing=preserve_existing,
        refresh_incoming=refresh_incoming,
    )
    sync_profile_flags(rows, collect_existing_profile_links())

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
    batch_meta = incoming_meta if incoming_payload else (batch_meta_override or {})
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
            "raw_card_rows": batch_meta.get("raw_card_rows", 0),
            "unique_doctor_count": len(rows),
            "category_error_count": batch_meta.get("category_error_count", 0),
            "detail_error_count": batch_meta.get("detail_error_count", 0),
            "existing_profile_count": sum(1 for row in rows if clean_text(str(row.get("已建画像") or "")) == "是"),
            "ledger_review": "多院汇总，详见官网入口台账",
            "ledger_difficulty": "多院汇总",
            "source_seed": source_label,
            "current_batch_hospital": (
                batch_meta.get("hospital", "")
                if incoming_payload
                else batch_meta.get("current_batch_hospital", "")
            ),
            "current_batch_rows": (
                len(incoming_rows)
                if incoming_payload
                else int(batch_meta.get("current_batch_rows") or 0)
            ),
            "new_rows_added": (
                added if incoming_payload else int(batch_meta.get("new_rows_added") or 0)
            ),
            "duplicate_rows_skipped": (
                skipped
                if incoming_payload
                else int(batch_meta.get("duplicate_rows_skipped") or 0)
            ),
            "existing_rows_refreshed": (
                refreshed
                if incoming_payload
                else int(batch_meta.get("existing_rows_refreshed") or 0)
            ),
            "existing_duplicate_rows": (
                existing_duplicates
                if incoming_payload
                else int(batch_meta.get("existing_duplicate_rows") or 0)
            ),
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
    if host.removeprefix("www.") == "gdskin.com" and path == "/showclass.aspx":
        entry_ids = [
            value
            for name, value in parse_qsl(parsed.query, keep_blank_values=True)
            if name.lower() == "id"
        ]
        if entry_ids and entry_ids[0] in GDSKIN_ENTRY_METADATA:
            return GDSKIN_ADAPTER_ID
    if ny5y_entry_kind(entry_url):
        return NY5Y_ADAPTER_ID
    if gdzy5413_entry_kind(entry_url):
        return GDZY5413_ADAPTER_ID
    if host.removeprefix("www.") == "gykqyy.com" and path == "/list.html":
        category_ids = [
            value
            for name, value in parse_qsl(parsed.query, keep_blank_values=True)
            if name.lower() == "category"
        ]
        if category_ids == ["55"]:
            return GYKQYY_ADAPTER_ID
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


def gdskin_entry_id(url: str | None) -> str:
    parsed = urlparse(clean_text(url))
    if comparable_host(parsed.geturl()) != "gdskin.com" or parsed.path.lower() != "/showclass.aspx":
        return ""
    for name, value in parse_qsl(parsed.query, keep_blank_values=True):
        if name.lower() == "id" and value in GDSKIN_ENTRY_METADATA:
            return value
    return ""


def gdskin_detail_id(url: str | None) -> str:
    parsed = urlparse(clean_text(url))
    if comparable_host(parsed.geturl()) != "gdskin.com" or parsed.path.lower() != "/shownews.aspx":
        return ""
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    if len(pairs) != 1 or pairs[0][0].lower() != "id" or not pairs[0][1].isdigit():
        return ""
    return pairs[0][1]


def ny5y_entry_kind(url: str | None) -> str:
    parsed = urlparse(clean_text(url))
    if comparable_host(parsed.geturl()) != "ny5y.cn":
        return ""
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    if len(pairs) != 1 or pairs[0][0].lower() != "id":
        return ""
    entry_id = pairs[0][1]
    metadata = NY5Y_ENTRY_METADATA.get(entry_id)
    if not metadata or parsed.path.lower() != metadata["path"]:
        return ""
    return entry_id


def ny5y_detail_id(url: str | None) -> str:
    parsed = urlparse(clean_text(url))
    if comparable_host(parsed.geturl()) != "ny5y.cn" or parsed.path.lower() != "/yisheng_xq.php":
        return ""
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    if len(pairs) != 1 or pairs[0][0].lower() != "id" or not pairs[0][1].isdigit():
        return ""
    return pairs[0][1]


def gdzy5413_entry_kind(url: str | None) -> str:
    parsed = urlparse(clean_text(url))
    if comparable_host(parsed.geturl()) != "gdzy5413.com" or parsed.path.lower() != "/main/famousdoctorinfo.aspx":
        return ""
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    if len(pairs) != 3:
        return ""
    params = {name.lower(): value for name, value in pairs}
    if len(params) != 3 or params.get("fid") != "81" or params.get("pid") != "850":
        return ""
    cid = params.get("cid", "")
    return cid if cid in GDZY5413_ENTRY_METADATA else ""


def gdzy5413_detail_id(url: str | None) -> str:
    parsed = urlparse(clean_text(url))
    if comparable_host(parsed.geturl()) != "gdzy5413.com" or parsed.path.lower() != "/main/doctor/specialist.aspx":
        return ""
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    if len(pairs) != 1 or pairs[0][0].lower() != "typeid" or not pairs[0][1].isdigit():
        return ""
    return pairs[0][1]


def gdzy5413_ksdoctor_detail_id(url: str | None) -> str:
    parsed = urlparse(clean_text(url))
    if (
        comparable_host(parsed.geturl()) != "gdzy5413.com"
        or parsed.path.lower() != "/main/ks/templet2/ksdoctorinfo.aspx"
    ):
        return ""
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    allowed = {"bid", "typeid", "cid", "ksid", "id"}
    if len(pairs) != 5 or {name.lower() for name, _value in pairs} != allowed:
        return ""
    params = {name.lower(): value for name, value in pairs}
    if any(not params[name].isdigit() for name in allowed):
        return ""
    if not (params["bid"] == params["cid"] and params["typeid"] == params["ksid"]):
        return ""
    return params["id"]


def generic_detail_identity(url: str) -> str:
    detail_id = gdskin_detail_id(url)
    if detail_id:
        return f"gdskin:{detail_id}"
    detail_id = ny5y_detail_id(url)
    if detail_id:
        return f"ny5y:{detail_id}"
    detail_id = gdzy5413_detail_id(url)
    if detail_id:
        return f"gdzy5413:{detail_id}"
    detail_id = gdzy5413_ksdoctor_detail_id(url)
    return f"gdzy5413:ksdoctor:{detail_id}" if detail_id else canonical_url(url)


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
        (
            r"^.*?(?:你)?当前所在的位置\s*[:：]?\s*.*?"
            r"(?:专家|医师)信息\s*[^。！？；;\n]{0,160}?"
            r"科室\s*[:：]\s*[\u4e00-\u9fff、（）()]{1,30}?"
            r"(?:科(?:一室|二室)?|中心)\s*"
        ),
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


def extract_clean_highlights(value: str | None) -> str:
    cleaned_source = strip_profile_navigation_text(value)
    highlights = extract_sentences(cleaned_source, HIGHLIGHT_TERMS)
    if contains_navigation_text(highlights):
        return ""
    return highlights


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
    if gdskin_entry_id(entry_url):
        return bool(gdskin_detail_id(candidate_url))
    if ny5y_entry_kind(entry_url):
        return bool(ny5y_detail_id(candidate_url))
    if (gdzy5413_id := gdzy5413_entry_kind(entry_url)):
        return bool(
            gdzy5413_detail_id(candidate_url)
            or (gdzy5413_id == "852" and gdzy5413_ksdoctor_detail_id(candidate_url))
        )
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
    if gdskin_entry_id(entry_url):
        role_text = " ".join(
            [
                clean_text(detail.get("title_field")),
                clean_text(item.get("list_title")),
            ]
        )
        if not any(term in role_text for term in GDSKIN_DOCTOR_ROLE_TERMS):
            valid = False
            warnings.append("专家团队列表身份不属于医生角色")
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


def generic_link_score(href: str, context: str, entry_url: str = "") -> int:
    parsed = urlparse(href)
    path = parsed.path.lower()
    if gdskin_entry_id(entry_url) and gdskin_detail_id(href):
        has_name = bool(extract_person_name(context))
        has_doctor_role = any(term in context for term in GDSKIN_DOCTOR_ROLE_TERMS)
        return 12 if has_name and has_doctor_role else -10
    if ny5y_entry_kind(entry_url) and ny5y_detail_id(href):
        return 12
    if gdzy5413_entry_kind(entry_url) and (
        gdzy5413_detail_id(href) or gdzy5413_ksdoctor_detail_id(href)
    ):
        return 12
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
    gdskin_id = gdskin_entry_id(entry_url)
    ny5y_id = ny5y_entry_kind(entry_url)
    gdzy5413_id = gdzy5413_entry_kind(entry_url)
    strict_smukq_directory = comparable_host(entry_url) == "smukqyy.cn" and bool(
        re.fullmatch(r"/section/\d+/?", urlparse(entry_url).path)
    )
    anchors = (
        soup.select("table.masterTitleH a[href]")
        if gdskin_id
        else soup.select("li.xinyutitle1 a[href]")
        if gdzy5413_id == "851"
        else soup.select("div.contentinfo div.pudocname a[href]")
        if gdzy5413_id == "852"
        else soup.find_all("a", href=True)
    )
    for anchor in anchors:
        href = urljoin(page_url, anchor["href"])
        if canonical_url(href) == canonical_url(page_url):
            continue
        if not is_collectable_url(entry_url, href):
            continue
        if not matches_generic_directory_detail_url(entry_url, href):
            continue
        gdzy5413_card = anchor.find_parent("li", class_="xinyutitle1") if gdzy5413_id == "851" else None
        gdzy5413_department_block = (
            anchor.find_parent("div", class_="contentinfo") if gdzy5413_id == "852" else None
        )
        context = (
            compact_visible_text(gdzy5413_card, 700)
            if gdzy5413_card
            else
            strip_profile_navigation_text(compact_visible_text(anchor, 700))
            if gdskin_id or ny5y_id
            else nearest_card_text(anchor)
        )
        score = generic_link_score(href, context, entry_url)
        if score < 6 and not strict_smukq_directory:
            continue
        key = generic_detail_identity(href)
        if key in seen:
            continue
        seen.add(key)
        name_element = gdzy5413_card.select_one(".docnameall") if gdzy5413_card else None
        honor_element = gdzy5413_card.select_one(".docjich") if gdzy5413_card else None
        name = (
            re.sub(r"\s+", "", clean_text(name_element.get_text(" ", strip=True)))
            if name_element
            else re.sub(r"\s+", "", clean_text(anchor.get_text(" ", strip=True)))
            if gdzy5413_department_block
            else extract_person_name(context)
        )
        list_title = clean_text(honor_element.get_text(" ", strip=True)) if honor_element else context
        gdzy5413_department = ""
        if gdzy5413_department_block:
            department_element = gdzy5413_department_block.select_one(".ks_title")
            gdzy5413_department = clean_generic_department(
                compact_visible_text(department_element, 200) if department_element else ""
            )
        rows.append(
            {
                "source_link": href,
                "name": name,
                "list_title": clip(list_title, 500),
                "department": (
                    GDSKIN_ENTRY_METADATA[gdskin_id]["category_name"]
                    if gdskin_id
                    else NY5Y_ENTRY_METADATA[ny5y_id]["category_name"]
                    if ny5y_id
                    else gdzy5413_department
                    if gdzy5413_id == "852"
                    else extract_gdzy5413_department(list_title, "")
                    if gdzy5413_id == "851"
                    else infer_department(context)
                ),
                "description": clip(list_title if gdzy5413_id == "851" else context, 700),
                "list_page": page_url,
                "score": str(score),
            }
        )
    return rows


def discover_gdskin_excluded_links(html: str, page_url: str, entry_url: str) -> list[dict[str, str]]:
    if not gdskin_entry_id(entry_url):
        return []
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for anchor in soup.select("table.masterTitleH a[href]"):
        href = urljoin(page_url, anchor["href"])
        detail_id = gdskin_detail_id(href)
        if not detail_id or detail_id in seen:
            continue
        seen.add(detail_id)
        context = strip_profile_navigation_text(compact_visible_text(anchor, 700))
        if any(term in context for term in GDSKIN_DOCTOR_ROLE_TERMS):
            continue
        rows.append(
            {
                "entry_url": entry_url,
                "source_link": href,
                "list_title": context,
                "reason": "专家团队列表身份不属于医生角色，已排除",
            }
        )
    return rows


def gdzy5413_raw_detail_relation_count(html: str, page_url: str, entry_url: str) -> int:
    if not gdzy5413_entry_kind(entry_url):
        return 0
    soup = BeautifulSoup(html, "html.parser")
    return sum(
        1
        for anchor in soup.find_all("a", href=True)
        if gdzy5413_detail_id(urljoin(page_url, anchor["href"]))
        or (
            gdzy5413_entry_kind(entry_url) == "852"
            and gdzy5413_ksdoctor_detail_id(urljoin(page_url, anchor["href"]))
        )
    )


def discover_generic_list_pages(entry_url: str, html: str, max_pages: int) -> list[str]:
    if ny5y_entry_kind(entry_url) or gdzy5413_entry_kind(entry_url):
        # Owner 指定入口均按现场证据视为单页目录；其他栏目或模板不得自行扩围。
        return [entry_url]
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


def discover_gdskin_postback_documents(
    session: requests.Session,
    entry_url: str,
    entry_html: str,
    max_pages: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    documents = [{"page": "1", "url": entry_url, "html": entry_html}]
    errors: list[dict[str, str]] = []
    soup = BeautifulSoup(entry_html, "html.parser")
    postback_pages: dict[int, str] = {}
    for anchor in soup.find_all("a", href=True):
        match = re.search(r"__doPostBack\('([^']+)','Page\$(\d+)'\)", anchor["href"])
        if not match:
            continue
        page_number = int(match.group(2))
        if 1 < page_number <= max_pages:
            postback_pages[page_number] = match.group(1)

    base_payload: dict[str, str] = {}
    for field in soup.select("form input[name]"):
        if clean_text(field.get("type")).lower() in {"submit", "button", "image", "file"}:
            continue
        base_payload[str(field["name"])] = str(field.get("value") or "")

    for page_number, event_target in sorted(postback_pages.items()):
        payload = dict(base_payload)
        payload["__EVENTTARGET"] = event_target
        payload["__EVENTARGUMENT"] = f"Page${page_number}"
        page_error = ""
        for attempt in range(1, 4):
            try:
                response = session.post(entry_url, data=payload, timeout=35)
                if response.status_code == 200:
                    response.encoding = response.apparent_encoding or response.encoding or "utf-8"
                    documents.append(
                        {
                            "page": str(page_number),
                            "url": f"{entry_url}#postback-page-{page_number}",
                            "html": response.text,
                        }
                    )
                    page_error = ""
                    break
                page_error = f"HTTP {response.status_code}"
            except Exception as exc:  # noqa: BLE001 - keep collection failure visible
                page_error = str(exc)
            time.sleep(0.8 * attempt)
        if page_error:
            errors.append(
                {
                    "page": str(page_number),
                    "entry_url": entry_url,
                    "url": f"{entry_url}#postback-page-{page_number}",
                    "error": page_error,
                }
            )
    return documents, errors


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
    raw_highlights = extract_sentences(raw_scope_text, HIGHLIGHT_TERMS)
    highlight_navigation_polluted = contains_navigation_text(raw_highlights)
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
        "highlight_navigation_polluted": "yes" if highlight_navigation_polluted else "no",
        "profile_text": clean_text(profile_text),
        "title_text": first_nonempty(h1, title),
    }


def parse_ny5y_detail(html: str, fallback: dict[str, str]) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")

    def selected_text(selector: str, max_len: int) -> str:
        element = soup.select_one(selector)
        return clip(element.get_text(" ", strip=True), max_len) if element else ""

    name_element = soup.select_one(".yuanzhang")
    direct_name = clean_text(
        " ".join(str(value) for value in name_element.find_all(string=True, recursive=False))
    ) if name_element else ""
    name = first_nonempty(direct_name, fallback.get("name", ""))
    department_raw = selected_text(".suoshulei", 200)
    department = clean_generic_department(re.sub(r"^进入\s*", "", department_raw))
    if department in NY5Y_GENERAL_CATEGORIES:
        department = ""
    title_field = first_nonempty(selected_text(".xq_zhicheng", 500), fallback.get("list_title", ""))
    specialty_raw = selected_text(".xq_content", 1200)
    specialty = clean_text(re.sub(r"^\s*擅长\s*[:：]\s*", "", specialty_raw))
    profile_text = selected_text(".xq_xiangxi_jieshao_xq", 6000)
    raw_highlights = extract_sentences(profile_text, HIGHLIGHT_TERMS)
    return {
        "name": clean_text(name),
        "department": clean_text(department),
        "department_raw": clean_text(department_raw),
        # “进入”是详情页科室链接的固定 UI 前缀，不属于正文污染。
        "department_polluted": "no",
        "title_field": clean_text(title_field),
        "specialty": clean_text(specialty),
        "specialty_raw": clean_text(specialty_raw),
        "specialty_navigation_polluted": "yes" if contains_navigation_text(specialty) else "no",
        "highlight_navigation_polluted": "yes" if contains_navigation_text(raw_highlights) else "no",
        "profile_text": clean_text(profile_text),
        "title_text": clean_text(name),
    }


def parse_gdzy5413_detail(html: str, fallback: dict[str, str]) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    profile_element = (
        soup.select_one("#news_info_plAll .news_info_s")
        or soup.select_one("#news_info_plAll")
        or soup.select_one(".news_info_s")
    )
    profile_text = compact_visible_text(profile_element, 6000) if profile_element else ""
    profile_text = re.sub(r"\s*了解详情[>＞]*\s*$", "", profile_text)
    name = re.sub(r"\s+", "", clean_text(fallback.get("name", "")))
    title_field = first_nonempty(
        fallback.get("list_title", ""),
        re.split(r"[。；;]", profile_text, maxsplit=1)[0] if profile_text else "",
    )
    department = extract_gdzy5413_department(title_field, profile_text)
    specialty_raw = ""
    specialty_match = re.search(
        r"(?:主攻方向为|主攻|专长于|专长|尤其擅长|擅长治疗|擅长诊治|擅长|擅治|长于|善于|善用|专科)\s*[:：]?\s*(.+)$",
        profile_text,
    )
    if specialty_match:
        specialty_raw = clean_text(specialty_match.group(1))
    specialty_raw = re.split(r"(?<=。)\s*(?:主持|承担|发表|获|出版|现任)", specialty_raw, maxsplit=1)[0]
    return {
        "name": name,
        "department": department,
        "department_raw": department,
        "department_polluted": "no",
        "title_field": title_field,
        "specialty": clip(specialty_raw, 1200),
        "specialty_raw": clip(specialty_raw, 1200),
        "specialty_navigation_polluted": "no",
        "highlight_navigation_polluted": "no",
        "profile_text": profile_text,
        "title_text": name,
    }


def parse_gdzy5413_ksdoctor_detail(html: str, fallback: dict[str, str]) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one(".newslistbg_m_c") or soup.select_one("table.newslist")
    content_text = compact_visible_text(content, 12000) if content else ""
    breadcrumb_element = content.select_one(".typeall_right") if content else None
    breadcrumb = compact_visible_text(breadcrumb_element, 500) if breadcrumb_element else ""
    department_match = re.search(r">\s*([^>]{1,40}?)\s*>\s*专家介绍", breadcrumb)
    department = clean_generic_department(department_match.group(1) if department_match else "")
    if not department:
        department = clean_generic_department(fallback.get("department", ""))

    basic_match = re.search(r"【基本资料】\s*(.*?)(?=【医生简介】|【出诊安排】|$)", content_text)
    profile_match = re.search(r"【医生简介】\s*(.*?)(?=【出诊安排】|$)", content_text)
    basic_text = clean_text(basic_match.group(1)) if basic_match else ""
    profile_text = clean_text(profile_match.group(1)) if profile_match else ""
    name_match = re.search(r"姓名\s*[:：]\s*([\u4e00-\u9fff·\s]{2,10}?)(?=\s*职称\s*[:：]|$)", basic_text)
    title_match = re.search(r"职称\s*[:：]\s*(.*?)(?=\s*擅长\s*[:：]|$)", basic_text)
    specialty_match = re.search(r"擅长\s*[:：]\s*(.*)$", basic_text)
    name = re.sub(
        r"\s+",
        "",
        clean_text(name_match.group(1) if name_match else fallback.get("name", "")),
    )
    title_field = clean_text(title_match.group(1)) if title_match else ""
    specialty = clean_text(specialty_match.group(1)) if specialty_match else ""
    return {
        "name": name,
        "department": department,
        "department_raw": department,
        "department_polluted": "no",
        "title_field": title_field,
        "specialty": clip(specialty, 1200),
        "specialty_raw": clip(specialty, 1200),
        "specialty_navigation_polluted": "no",
        "highlight_navigation_polluted": "no",
        "profile_text": clip(profile_text, 6000),
        "title_text": name,
    }


def parse_gdskin_detail(html: str, fallback: dict[str, str]) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    content_element = soup.select_one(".labelContent")
    if not content_element:
        return parse_generic_detail(html, fallback)

    title = clean_text(soup.title.get_text(" ", strip=True)) if soup.title else ""
    content = strip_article_tail(compact_visible_text(content_element, 6000))
    content = re.sub(r"^预约挂号\s*", "", content)
    content_paragraphs: list[str] = []
    for paragraph in content_element.find_all("p"):
        paragraph_text = strip_article_tail(compact_visible_text(paragraph, 2400))
        paragraph_text = re.sub(r"^预约挂号\s*", "", paragraph_text)
        if paragraph_text and paragraph_text not in content_paragraphs:
            content_paragraphs.append(paragraph_text)
    name = first_nonempty(
        fallback.get("name"),
        extract_person_name(title, content[:160], fallback.get("list_title", "")),
    )

    specialty_raw = ""
    profile_text = ""
    for paragraph_index, paragraph_text in enumerate(content_paragraphs):
        specialty_match = re.match(r"^(?:专长|擅长)\s*[:：]\s*(.+)$", paragraph_text, flags=re.S)
        if not specialty_match:
            continue
        specialty_parts = re.split(r"简介\s*[:：]", specialty_match.group(1), maxsplit=1)
        specialty_raw = clean_text(specialty_parts[0])
        if len(specialty_parts) > 1:
            profile_text = clean_text(specialty_parts[1])
        else:
            following_paragraphs = [
                clean_text(re.sub(r"^简介\s*[:：]\s*", "", value))
                for value in content_paragraphs[paragraph_index + 1 :]
            ]
            profile_text = clean_text(" ".join(value for value in following_paragraphs if value))
        break
    if not specialty_raw:
        specialty_match = re.search(
            r"(?:专长|擅长)\s*[:：]\s*(.+?)(?=简介\s*[:：]|$)",
            content,
            flags=re.S,
        )
        specialty_raw = clean_text(specialty_match.group(1)) if specialty_match else ""
    specialty_navigation_polluted = contains_navigation_text(specialty_raw)
    specialty = "" if specialty_navigation_polluted else specialty_raw

    if not profile_text:
        profile_match = re.search(r"简介\s*[:：]\s*(.+)$", content, flags=re.S)
        profile_text = clean_text(profile_match.group(1)) if profile_match else ""

    first_label_positions = [
        position
        for marker in ["专长：", "专长:", "擅长：", "擅长:", "简介：", "简介:"]
        if (position := content.find(marker)) >= 0
    ]
    title_field = content[: min(first_label_positions)] if first_label_positions else content
    if name:
        title_field = re.sub(rf"^\s*{re.escape(name)}\s*", "", title_field, count=1)
    title_field = clean_text(title_field).strip("、，,；;_- ")
    if not first_label_positions and not profile_text:
        biography_match = re.search(
            r"(?=(?:(?:博士|硕士|本科)毕业于|毕业于|主要从事|从事|曾赴|曾任|主持|参与|以第一作者|发表))",
            title_field,
        )
        if biography_match and biography_match.start() > 0:
            candidate_title = clean_text(title_field[: biography_match.start()]).strip("、，,；;_- ")
            if extract_terms(candidate_title, TITLE_TERMS):
                profile_text = clean_text(title_field[biography_match.start() :])
                title_field = candidate_title

    department_raw = clean_text(fallback.get("department"))
    department = clean_generic_department(department_raw)
    raw_highlights = extract_sentences(content, HIGHLIGHT_TERMS)
    return {
        "name": clean_text(name),
        "department": department,
        "department_raw": department_raw,
        "department_polluted": "yes" if has_department_text_pollution(department_raw, department) else "no",
        "title_field": title_field,
        "specialty": specialty,
        "specialty_raw": specialty_raw,
        "specialty_navigation_polluted": "yes" if specialty_navigation_polluted else "no",
        "highlight_navigation_polluted": "yes" if contains_navigation_text(raw_highlights) else "no",
        "profile_text": profile_text,
        "title_text": first_nonempty(name, title),
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


def fetch_json(
    session: requests.Session,
    url: str,
    params: dict[str, Any] | None = None,
    retries: int = 3,
) -> tuple[int | None, dict[str, Any], str]:
    last_status: int | None = None
    last_error = ""
    retryable_statuses = {429, 500, 502, 503, 504}
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, params=params, timeout=35)
        except Exception as exc:  # noqa: BLE001 - keep collection failure visible
            last_error = str(exc)
            if attempt < retries:
                time.sleep(0.8 * attempt)
                continue
            return None, {}, last_error
        last_status = response.status_code
        content_type = clean_text(response.headers.get("Content-Type"))
        if response.status_code != 200:
            last_error = f"HTTP {response.status_code}"
            if response.status_code in retryable_statuses and attempt < retries:
                time.sleep(0.8 * attempt)
                continue
            return response.status_code, {}, last_error
        if "json" not in content_type.lower():
            return response.status_code, {}, f"非 JSON 响应：{content_type or '未声明 Content-Type'}"
        try:
            payload = response.json()
        except ValueError as exc:
            return response.status_code, {}, f"JSON 解析失败：{exc}"
        if not isinstance(payload, dict):
            return response.status_code, {}, "JSON 顶层不是对象"
        return response.status_code, payload, ""
    return last_status, {}, last_error or "JSON 请求失败"


def flatten_gykqyy_directory_groups(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    relations: list[dict[str, Any]] = []
    for group in groups:
        group_name = clean_text(str(group.get("name") or ""))
        for department in group.get("child") or []:
            if not isinstance(department, dict):
                continue
            department_name = clean_text(str(department.get("name") or ""))
            for doctor in department.get("child") or []:
                if not isinstance(doctor, dict):
                    continue
                relations.append(
                    {
                        "group": group_name,
                        "department": department_name,
                        "doctor": doctor,
                    }
                )
    return relations


def select_gykqyy_trial_doctors(
    doctors: list[dict[str, Any]],
    max_doctors: int | None,
) -> list[dict[str, Any]]:
    if not max_doctors or len(doctors) <= max_doctors:
        return doctors[:]
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    covered_departments: set[str] = set()
    for doctor in doctors:
        departments = [
            clean_text(str(value))
            for value in doctor.get("departments", [])
            if clean_text(str(value))
        ]
        if departments and any(value not in covered_departments for value in departments):
            selected.append(doctor)
            selected_ids.add(str(doctor["id"]))
            covered_departments.update(departments)
        if len(selected) >= max_doctors:
            return selected
    for doctor in doctors:
        if str(doctor["id"]) in selected_ids:
            continue
        selected.append(doctor)
        selected_ids.add(str(doctor["id"]))
        if len(selected) >= max_doctors:
            break
    return selected


def gykqyy_profile_text(detail: dict[str, Any]) -> str:
    html = str(detail.get("content") or "")
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    return strip_profile_navigation_text(soup.get_text(" ", strip=True))


def collect_gykqyy(target: HospitalTarget, today: str, max_doctors: int | None = None) -> dict[str, Any]:
    session = create_official_session()
    session.headers.update({"Referer": target.entry_url})
    entry_status, entry_html, entry_error = fetch(session, target.entry_url)
    if entry_status != 200:
        raise RuntimeError(f"入口页读取失败：{entry_error}")
    if GYKQYY_DIRECTORY_API not in entry_html or GYKQYY_DETAIL_API not in entry_html:
        raise RuntimeError("入口页未同时公开医生目录与详情接口，拒绝调用页面外接口。")

    directory_status, directory_payload, directory_error = fetch_json(session, GYKQYY_DIRECTORY_API)
    data = directory_payload.get("data") if isinstance(directory_payload, dict) else None
    if directory_status != 200 or not isinstance(data, dict):
        raise RuntimeError(f"官网医生目录接口读取失败：{directory_error or '响应结构异常'}")
    if directory_payload.get("code") != 1:
        raise RuntimeError(f"官网医生目录接口返回失败：{directory_payload.get('msg')}")

    groups = [item for item in data.get("list") or [] if isinstance(item, dict)]
    banner = [item for item in data.get("banner") or [] if isinstance(item, dict)]
    banner_by_id = {
        clean_text(str(item.get("id") or "")): item
        for item in banner
        if clean_text(str(item.get("id") or ""))
    }
    relations = flatten_gykqyy_directory_groups(groups)
    departments = [
        {
            "group": clean_text(str(group.get("name") or "")),
            "id": str(department.get("id") or ""),
            "name": clean_text(str(department.get("name") or "")),
            "doctor_relation_count": len(department.get("child") or []),
        }
        for group in groups
        for department in (group.get("child") or [])
        if isinstance(department, dict)
    ]

    by_id: dict[str, dict[str, Any]] = {}
    for relation in relations:
        doctor = relation["doctor"]
        doctor_id = clean_text(str(doctor.get("id") or ""))
        if not doctor_id:
            continue
        item = by_id.setdefault(
            doctor_id,
            {
                **doctor,
                "id": doctor_id,
                "departments": [],
                "groups": [],
            },
        )
        department = relation["department"]
        if department and department not in item["departments"]:
            item["departments"].append(department)
        group_name = relation["group"]
        if group_name and group_name not in item["groups"]:
            item["groups"].append(group_name)

    all_doctors = sorted(
        (
            {
                **item,
                **{
                    key: value
                    for key, value in banner_by_id.get(doctor_id, {}).items()
                    if value not in {None, ""}
                },
                "id": doctor_id,
            }
            for doctor_id, item in by_id.items()
        ),
        key=lambda item: (-int(item.get("weigh") or 0), int(str(item["id"]))),
    )
    ids_by_name: dict[str, list[str]] = {}
    for doctor in all_doctors:
        doctor_name = clean_text(str(doctor.get("title") or ""))
        if doctor_name:
            ids_by_name.setdefault(doctor_name, []).append(str(doctor["id"]))
    same_name_groups = {
        name: sorted(set(ids), key=int)
        for name, ids in ids_by_name.items()
        if len(set(ids)) > 1
    }
    selected_doctors = select_gykqyy_trial_doctors(all_doctors, max_doctors)
    existing_links = collect_existing_profile_links()
    rows: list[dict[str, Any]] = []
    detail_errors: list[dict[str, str]] = []
    excluded_detail_candidates: list[dict[str, str]] = []
    identity_reconciliation: list[dict[str, Any]] = []
    for item in selected_doctors:
        doctor_id = str(item["id"])
        link = f"{target.entry_url}&id={doctor_id}"
        detail_status, detail_payload, detail_error = fetch_json(
            session,
            GYKQYY_DETAIL_API,
            params={"category_id": 55, "article_id": doctor_id},
        )
        detail_data = detail_payload.get("data") if isinstance(detail_payload, dict) else None
        detail = detail_data.get("detail") if isinstance(detail_data, dict) else None
        if detail_status != 200 or detail_payload.get("code") != 1 or not isinstance(detail, dict):
            detail_errors.append({"source_link": link, "error": detail_error or "详情接口响应结构异常"})
            detail = {}

        name = first_nonempty(str(detail.get("title") or ""), str(item.get("title") or ""))
        departments_for_doctor = [clean_text(str(value)) for value in item.get("departments", [])]
        department = "、".join(value for value in departments_for_doctor if value)
        if not name:
            excluded_detail_candidates.append(
                {
                    "entry_url": target.entry_url,
                    "list_title": "",
                    "source_link": link,
                    "reason": "目录与详情均无姓名，核心追溯字段缺失，排除正式行与画像",
                }
            )
            continue
        list_department = clean_text(str(item.get("keshi") or ""))
        title_field = clean_text(str(item.get("zhicheng") or ""))
        profile_text = gykqyy_profile_text(detail)
        list_intro = clean_text(str(item.get("intro") or ""))
        detail_intro = clean_text(str(detail.get("intro") or ""))
        specialty = clip(first_nonempty(detail_intro, list_intro), 520)
        combined_text = "\n".join(
            [target.hospital, department, list_department, title_field, specialty, profile_text]
        )
        title_hits = extract_terms(title_field, TITLE_TERMS) or extract_terms(profile_text, TITLE_TERMS)
        title_identity = first_nonempty(title_field, "、".join(title_hits))
        groups_found, tags = group_tags(combined_text)
        highlights = extract_clean_highlights(profile_text)
        warnings: list[str] = []
        if not detail:
            warnings.append("详情接口读取失败")
        if not looks_like_person_name(name):
            warnings.append("非医生页面或姓名异常")
        if not department:
            warnings.append("科室需人工复核")
        if not title_hits:
            warnings.append("职称/身份需人工复核")
        if not specialty and not profile_text:
            warnings.append("详情正文为空或未识别")
        if name in same_name_groups:
            warnings.append("同名待甄别")
        priority = "普通"
        if any(term in combined_text for term in PRIORITY_DEPARTMENTS) or groups_found:
            priority = "高"
        elif any(term != "医师" for term in title_hits):
            priority = "中"

        rows.append(
            {
                "序号": len(rows) + 1,
                "医院": target.hospital,
                "姓名": name,
                "科室_分类页": department,
                "科室_列表卡片": list_department,
                "职称_关键词": "、".join(title_hits),
                "职称身份原文": clip(title_identity, 500),
                "重点优先级": priority,
                "重点关注范围": "、".join(groups_found),
                "重点疾病标签": "、".join(tags),
                "擅长诊疗方向摘录": specialty,
                "亮眼经历线索": highlights,
                "列表简介": clip(list_intro, 700),
                "详情正文摘录": clip(profile_text, 1800),
                "来源类型": "医院官网",
                "来源链接": link,
                "采集入口": target.entry_url,
                "采集方式": "官网页面公开同域目录接口+官网页面公开同域详情接口",
                "采集日期": today,
                "详情页状态": "200" if detail else "失败",
                "已建画像": "是" if canonical_url(link) in existing_links else "否",
                "异常提示": "；".join(warnings),
                "复核状态": "待人工复核",
            }
        )
        identity_reconciliation.append(
            {
                "detail_id": doctor_id,
                "name": name,
                "resolution": "同名不同 ID 分行保留" if name in same_name_groups else "唯一 ID 保留",
                "departments": departments_for_doctor,
                "source_link": link,
                "reason": "同名待甄别" if name in same_name_groups else "官网科室树唯一详情 ID",
            }
        )

    category_counter = Counter(row["科室_分类页"] for row in rows if row["科室_分类页"])
    priority_counter = Counter(row["重点优先级"] for row in rows)
    group_counter = Counter(
        group
        for row in rows
        for group in str(row["重点关注范围"]).split("、")
        if group
    )
    warning_counter = Counter(
        warning
        for row in rows
        for warning in str(row["异常提示"]).split("；")
        if warning
    )
    directory_names = [clean_text(str(item.get("title") or "")) for item in all_doctors]
    nonblank_names = {name for name in directory_names if name}
    named_detail_count = sum(1 for name in directory_names if name)
    blank_name_detail_count = len(directory_names) - named_detail_count
    tree_ids = {str(item["id"]) for item in all_doctors}
    banner_only = [
        item
        for item in banner
        if clean_text(str(item.get("id") or "")) not in tree_ids
    ]

    return {
        "meta": {
            "city": target.city,
            "hospital": target.hospital,
            "homepage": target.homepage,
            "entry_url": target.entry_url,
            "entry_url_source": "GitHub Issue #22（与官网入口台账一致）",
            "ledger_entry_url": target.ledger_entry_url or target.entry_url,
            "adapter_id": target.adapter_id,
            "collected_at": today,
            "category_count": 1,
            "raw_card_rows": len(relations),
            "candidate_membership_count": len(relations),
            "unique_candidate_count": len(all_doctors),
            "sample_entry_coverage_count": 1,
            "sample_entry_categories": ["医生团队（category=55）"],
            "unique_doctor_count": len(rows),
            "census_unique_detail_count": len(all_doctors),
            "census_named_detail_count": named_detail_count,
            "census_blank_name_detail_count": blank_name_detail_count,
            "census_unique_nonblank_name_count": len(nonblank_names),
            "census_same_name_group_count": len(same_name_groups),
            "census_same_name_groups": same_name_groups,
            "census_department_count": len(departments),
            "census_group_count": len(groups),
            "census_banner_count": len(banner),
            "excluded_non_doctor_count": len(banner_only),
            "pagination_count": 1,
            "pagination_method": "医生专区由单次 getZhuanjiaList 请求一次性返回，无 page/pageNo 参数",
            "directory_api": GYKQYY_DIRECTORY_API,
            "detail_api": GYKQYY_DETAIL_API,
            "api_source_evidence": "医生目录 HTML 内联 Vue 脚本的 axios.get 明确声明两个同域公开接口",
            "category_error_count": 0,
            "detail_error_count": len(detail_errors),
            "gykqyy_final_row_count": len(rows),
            "gykqyy_same_name_separate_row_count": sum(
                1 for row in rows if clean_text(str(row.get("姓名") or "")) in same_name_groups
            ),
            "existing_profile_count": sum(1 for row in rows if row["已建画像"] == "是"),
            "ledger_review": target.review,
            "ledger_difficulty": target.difficulty,
        },
        "categories": departments,
        "entry_reconnaissance": [
            {
                "category_name": "医生团队（category=55）",
                "entry_url": target.entry_url,
                "page_nature": "动态 Vue 医生目录；单次同域公开接口载入",
                "list_page_count": 1,
                "raw_detail_relation_count": len(relations),
                "unique_detail_count": len(all_doctors),
                "out_of_scope_detail_count": len(banner_only),
                "affiliation": target.hospital,
                "independent_entity_check": "官网同域、无鉴权、无内部参数",
            }
        ],
        "excluded_candidates": [
            {
                "entry_url": target.entry_url,
                "list_title": clean_text(str(item.get("title") or "")),
                "source_link": f"{target.entry_url}&id={item.get('id')}",
                "reason": "焦点推荐记录未出现在科室医生树中且姓名为空，排除",
            }
            for item in banner_only
        ]
        + excluded_detail_candidates,
        "gykqyy_identity_reconciliation": identity_reconciliation,
        "category_errors": [],
        "detail_errors": detail_errors,
        "category_counts": category_counter.most_common(),
        "priority_counts": dict(priority_counter),
        "group_counts": dict(group_counter),
        "warning_counts": dict(warning_counter),
        "rows": rows,
    }


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
        key = generic_detail_identity(row["source_link"])
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


def round_robin_generic_items(
    items: list[dict[str, str]],
    entry_urls: list[str],
    max_items: int | None,
    spread: bool = False,
) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = {canonical_url(url): [] for url in entry_urls}
    for item in items:
        grouped.setdefault(canonical_url(item.get("entry_url", "")), []).append(item)
    for values in grouped.values():
        if spread and max_items and len(values) > 1:
            sample_count = min(max_items, len(values))
            spread_indices = {
                round(index * (len(values) - 1) / (sample_count - 1))
                for index in range(sample_count)
            }
            values[:] = [values[index] for index in sorted(spread_indices)] + [
                item for index, item in enumerate(values) if index not in spread_indices
            ]
        else:
            values.sort(key=lambda item: item["source_link"])

    ordered: list[dict[str, str]] = []
    offsets = {key: 0 for key in grouped}
    while True:
        added = False
        for entry_url in entry_urls:
            key = canonical_url(entry_url)
            values = grouped.get(key, [])
            offset = offsets.get(key, 0)
            if offset >= len(values):
                continue
            ordered.append(values[offset])
            offsets[key] = offset + 1
            added = True
            if max_items and len(ordered) >= max_items:
                return ordered
        if not added:
            return ordered


def gdzy5413_normalized_name(value: str | None) -> str:
    return re.sub(r"\s+", "", clean_text(value))


def select_gdzy5413_trial2_items(
    items: list[dict[str, str]],
    max_doctors: int | None,
) -> list[dict[str, str]]:
    """Select auditable 852 name groups, including one merge case and one Baiyun record."""

    if not max_doctors:
        return items
    groups: dict[str, list[dict[str, str]]] = {}
    for item in items:
        name = gdzy5413_normalized_name(item.get("name"))
        if name:
            groups.setdefault(name, []).append(item)

    duplicate_groups = [values for values in groups.values() if len(values) > 1]
    duplicate_groups.sort(
        key=lambda values: (
            len({clean_text(item.get("department")) for item in values}) != 1,
        )
    )
    selected_names: list[str] = []
    if duplicate_groups:
        selected_names.append(gdzy5413_normalized_name(duplicate_groups[0][0].get("name")))

    baiyun_names = [
        name
        for name, values in groups.items()
        if len(values) == 1 and "白云院区" in clean_text(values[0].get("department"))
    ]
    if baiyun_names and baiyun_names[0] not in selected_names:
        selected_names.append(baiyun_names[0])

    covered_departments = {
        clean_text(item.get("department"))
        for name in selected_names
        for item in groups[name]
        if clean_text(item.get("department"))
    }
    unique_groups = [(name, values) for name, values in groups.items() if len(values) == 1]
    for name, values in unique_groups:
        if len(selected_names) >= max_doctors:
            break
        department = clean_text(values[0].get("department"))
        if name in selected_names or not department or department in covered_departments:
            continue
        selected_names.append(name)
        covered_departments.add(department)
    for name, _values in unique_groups:
        if len(selected_names) >= max_doctors:
            break
        if name not in selected_names:
            selected_names.append(name)

    selected: list[dict[str, str]] = []
    for name in selected_names[:max_doctors]:
        selected.extend(groups[name])
    return selected


def expand_gdzy5413_full_detail_items(items: list[dict[str, str]]) -> list[dict[str, str]]:
    """FULL must fetch every same-name link so the owner identity rule has complete evidence."""

    groups: dict[str, list[dict[str, str]]] = {}
    order: list[str] = []
    for item in items:
        name = gdzy5413_normalized_name(item.get("name"))
        if name not in groups:
            groups[name] = []
            order.append(name)
        groups[name].append(item)
    return [item for name in order for item in groups[name]]


def gdzy5413_identity_text(value: str | None) -> str:
    return re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]+", "", clean_text(value)).lower()


def gdzy5413_text_similarity(left: str | None, right: str | None) -> float:
    first = gdzy5413_identity_text(left)
    second = gdzy5413_identity_text(right)
    if not first or not second:
        return 0.0
    if first in second or second in first:
        return 1.0
    return SequenceMatcher(None, first, second).ratio()


def gdzy5413_rows_same_identity(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if gdzy5413_normalized_name(left.get("姓名")) != gdzy5413_normalized_name(right.get("姓名")):
        return False
    left_titles = set(extract_terms(clean_text(left.get("职称身份原文")), TITLE_TERMS))
    right_titles = set(extract_terms(clean_text(right.get("职称身份原文")), TITLE_TERMS))
    title_consistent = bool(left_titles & right_titles) or not left_titles or not right_titles
    specialty_similarity = gdzy5413_text_similarity(
        left.get("擅长诊疗方向摘录"), right.get("擅长诊疗方向摘录")
    )
    profile_similarity = gdzy5413_text_similarity(
        left.get("详情正文摘录"), right.get("详情正文摘录")
    )
    specialty_evidence = bool(
        gdzy5413_identity_text(left.get("擅长诊疗方向摘录"))
        and gdzy5413_identity_text(right.get("擅长诊疗方向摘录"))
    )
    if specialty_evidence:
        return title_consistent and specialty_similarity >= 0.55
    return title_consistent and profile_similarity >= 0.7


def gdzy5413_primary_row_score(row: dict[str, Any]) -> int:
    """Prefer the detail with the richest clinical biography over noisy title repetition."""

    return (
        len(clean_text(row.get("详情正文摘录"))) * 5
        + len(clean_text(row.get("擅长诊疗方向摘录"))) * 2
        + len(clean_text(row.get("职称身份原文")))
        + len(clean_text(row.get("亮眼经历线索")))
    )


def merge_gdzy5413_identity_rows(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Apply the owner rule: merge materially consistent names, preserve distinct identities."""

    by_name: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_name.setdefault(gdzy5413_normalized_name(row.get("姓名")), []).append(row)

    merged_rows: list[dict[str, Any]] = []
    reconciliation: list[dict[str, Any]] = []
    longest_fields = [
        "擅长诊疗方向摘录",
        "亮眼经历线索",
        "列表简介",
        "详情正文摘录",
    ]
    for name, name_rows in by_name.items():
        clusters: list[list[dict[str, Any]]] = []
        for row in name_rows:
            for cluster in clusters:
                if any(gdzy5413_rows_same_identity(row, member) for member in cluster):
                    cluster.append(row)
                    break
            else:
                clusters.append([row])

        distinct_same_name = len(clusters) > 1
        for identity_index, cluster in enumerate(clusters, start=1):
            primary = max(cluster, key=gdzy5413_primary_row_score)
            merged = dict(primary)
            departments: list[str] = []
            for member in cluster:
                for field in ["科室_分类页", "科室_列表卡片"]:
                    for department in clean_text(member.get(field)).split("、"):
                        department = clean_text(department)
                        if department and department not in departments:
                            departments.append(department)
                for field in longest_fields:
                    if len(clean_text(member.get(field))) > len(clean_text(merged.get(field))):
                        merged[field] = member.get(field, "")
            merged["科室_分类页"] = "、".join(departments)
            merged["科室_列表卡片"] = "、".join(departments)
            merged["职称_关键词"] = "、".join(
                extract_terms(clean_text(primary.get("职称身份原文")), TITLE_TERMS)
            )
            warnings = [
                warning
                for member in cluster
                for warning in clean_text(member.get("异常提示")).split("；")
                if warning
            ]
            distinct_titles = {
                clean_text(member.get("职称身份原文"))
                for member in cluster
                if clean_text(member.get("职称身份原文"))
            }
            if len(distinct_titles) > 1:
                warnings.append("多详情职称不一致")
            if distinct_same_name:
                warnings.append("同名待甄别")
            merged["异常提示"] = "；".join(dict.fromkeys(warnings))
            merged_rows.append(merged)
            reconciliation.append(
                {
                    "name": name,
                    "identity_index": identity_index,
                    "resolution": (
                        "同名待甄别"
                        if distinct_same_name
                        else "同一人归并"
                        if len(cluster) > 1
                        else "唯一身份"
                    ),
                    "primary_source_link": merged.get("来源链接", ""),
                    "merged_source_links": [
                        member.get("来源链接", "")
                        for member in cluster
                        if member.get("来源链接") != merged.get("来源链接")
                    ],
                    "departments": departments,
                    "relation_count": len(cluster),
                }
            )

    return merged_rows, reconciliation


def collect_generic(
    target: HospitalTarget,
    today: str,
    max_doctors: int | None = None,
    max_pages: int = GENERIC_MAX_PAGES_DEFAULT,
    gdzy5413_trial2: bool = False,
) -> dict[str, Any]:
    session = create_official_session()
    entry_urls = effective_entry_urls(target)
    if not entry_urls:
        raise RuntimeError("通用模板未提供医生目录入口。")

    categories: list[dict[str, str]] = []
    page_errors: list[dict[str, str]] = []
    raw_rows: list[dict[str, str]] = []
    excluded_candidates_by_link: dict[str, dict[str, str]] = {}
    entry_candidate_links: dict[str, set[str]] = {entry_url: set() for entry_url in entry_urls}
    entry_raw_relation_counts: dict[str, int] = {entry_url: 0 for entry_url in entry_urls}
    accessible_entry_count = 0
    for entry_index, entry_url in enumerate(entry_urls, start=1):
        status, entry_html, entry_error = fetch(session, entry_url)
        if status != 200:
            page_errors.append({"page": "1", "entry_url": entry_url, "url": entry_url, "error": entry_error})
            continue
        accessible_entry_count += 1
        if gdskin_entry_id(entry_url):
            page_documents, postback_errors = discover_gdskin_postback_documents(
                session,
                entry_url,
                entry_html,
                max_pages=max_pages,
            )
            page_errors.extend(postback_errors)
        else:
            page_documents = []
            for page_index, page_url in enumerate(
                discover_generic_list_pages(entry_url, entry_html, max_pages=max_pages),
                start=1,
            ):
                if page_index == 1:
                    html = entry_html
                    page_status = status
                    page_error = ""
                else:
                    page_status, html, page_error = fetch(session, page_url)
                if page_status != 200:
                    page_errors.append(
                        {
                            "page": str(page_index),
                            "entry_url": entry_url,
                            "url": page_url,
                            "error": page_error,
                        }
                    )
                    continue
                page_documents.append({"page": str(page_index), "url": page_url, "html": html})

        for page_document in page_documents:
            page_number = page_document["page"]
            page_url = page_document["url"]
            categories.append(
                {
                    "category_id": f"{entry_index}-{page_number}",
                    "category_name": f"通用模板入口{entry_index}列表第{page_number}页",
                    "url": page_url,
                    "entry_url": entry_url,
                }
            )
            page_rows = discover_generic_detail_links(page_document["html"], page_url, entry_url)
            entry_raw_relation_counts[entry_url] += gdzy5413_raw_detail_relation_count(
                page_document["html"], page_url, entry_url
            )
            for excluded in discover_gdskin_excluded_links(page_document["html"], page_url, entry_url):
                excluded_candidates_by_link.setdefault(
                    generic_detail_identity(excluded["source_link"]),
                    excluded,
                )
            for row in page_rows:
                row["entry_url"] = entry_url
                entry_candidate_links[entry_url].add(generic_detail_identity(row["source_link"]))
            raw_rows.extend(page_rows)
            print(
                f"[entry {entry_index}/{len(entry_urls)} page {page_number}/{len(page_documents)}] "
                f"generic list rows: {len(page_rows)}"
            )
            time.sleep(0.2)

    entry_candidate_counts = {
        entry_url: len(candidate_links)
        for entry_url, candidate_links in entry_candidate_links.items()
    }

    if accessible_entry_count == 0:
        errors = "；".join(error.get("error", "") for error in page_errors if error.get("error"))
        raise RuntimeError(f"全部医生目录入口读取失败：{errors}")

    by_link: dict[str, dict[str, str]] = {}
    for row in raw_rows:
        key = generic_detail_identity(row["source_link"])
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
                "entry_url": row.get("entry_url", ""),
                "all_entry_urls": row.get("entry_url", ""),
            },
        )
        for field in ["name", "list_title", "description"]:
            if row.get(field, "") and len(row.get(field, "")) > len(item.get(field, "")):
                item[field] = row[field]
        row_department = row.get("department", "")
        item_department = item.get("department", "")
        if row_department and (
            not item_department
            or (
                item_department in (GDSKIN_GENERAL_CATEGORIES | NY5Y_GENERAL_CATEGORIES)
                and row_department not in (GDSKIN_GENERAL_CATEGORIES | NY5Y_GENERAL_CATEGORIES)
            )
            or len(row_department) > len(item_department)
        ):
            item["department"] = row_department
        if int(row.get("score") or 0) > int(item.get("score") or 0):
            item["score"] = row.get("score", "")
        entry_members = [value for value in item["all_entry_urls"].split("；") if value]
        if row.get("entry_url", "") and row["entry_url"] not in entry_members:
            entry_members.append(row["entry_url"])
            item["all_entry_urls"] = "；".join(entry_members)
        pages = [value for value in item["list_pages"].split("；") if value]
        if row["list_page"] not in pages:
            pages.append(row["list_page"])
            item["list_pages"] = "；".join(pages)

    sampling_items = list(by_link.values())
    sampling_entry_urls = entry_urls
    if gdzy5413_trial2:
        sampling_items = [
            item
            for item in sampling_items
            if gdzy5413_entry_kind(item.get("entry_url")) == "852"
            and gdzy5413_ksdoctor_detail_id(item.get("source_link"))
        ]
        sampling_items = select_gdzy5413_trial2_items(sampling_items, max_doctors)
        sampling_entry_urls = [
            entry_url for entry_url in entry_urls if gdzy5413_entry_kind(entry_url) == "852"
        ]
    elif target.adapter_id == GDZY5413_ADAPTER_ID and max_doctors is None:
        sampling_items = expand_gdzy5413_full_detail_items(sampling_items)
    detail_items = round_robin_generic_items(
        sampling_items,
        sampling_entry_urls,
        None if gdzy5413_trial2 else max_doctors,
        spread=target.adapter_id in {NY5Y_ADAPTER_ID, GDZY5413_ADAPTER_ID},
    )
    if target.adapter_id == GDSKIN_ADAPTER_ID:
        for item in detail_items:
            if item.get("department") in GDSKIN_GENERAL_CATEGORIES:
                # 首席/知名专家是官网荣誉分组，不是院内科室；官网未给出真实科室时保持空白。
                item["department"] = ""
    elif target.adapter_id == NY5Y_ADAPTER_ID:
        for item in detail_items:
            if item.get("department") in NY5Y_GENERAL_CATEGORIES:
                # 专家风采/岭南名医是官网栏目或荣誉分组，不是院内科室。
                item["department"] = ""

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
            "highlight_navigation_polluted": "no",
        }
        if detail_status == 200:
            detail = (
                parse_gdskin_detail(detail_html, item)
                if gdskin_detail_id(link)
                else parse_ny5y_detail(detail_html, item)
                if ny5y_detail_id(link)
                else parse_gdzy5413_detail(detail_html, item)
                if gdzy5413_detail_id(link)
                else parse_gdzy5413_ksdoctor_detail(detail_html, item)
                if gdzy5413_ksdoctor_detail_id(link)
                else parse_generic_detail(detail_html, item)
            )
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
            item.get("entry_url", target.entry_url),
            detail,
            item,
        )
        priority, groups, tags = classify_generic_record(valid_doctor_record, combined_text, title_hits)
        specialty = clip(detail.get("specialty"), 520) if valid_doctor_record else ""
        highlight_source = (
            detail.get("profile_text", "")
            if ny5y_detail_id(link) or gdzy5413_detail_id(link) or gdzy5413_ksdoctor_detail_id(link)
            else combined_text
        )
        highlights = extract_clean_highlights(highlight_source)
        gdzy5413_honor = ""
        if gdzy5413_detail_id(link) and any(
            term in item.get("list_title", "")
            for term in ["国务院特殊津贴", "名中医", "名老中医", "学科带头人", "优秀中医临床人才"]
        ):
            gdzy5413_honor = item.get("list_title", "")

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
        if detail.get("highlight_navigation_polluted") == "yes":
            warnings.append(
                "亮眼经历含导航文本，已清洗" if highlights else "亮眼经历含导航文本，已清空"
            )

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
                "亮眼经历线索": clip(
                    clean_text(
                        " ".join(
                            part
                            for part in [
                                "岭南名医"
                                if any(
                                    ny5y_entry_kind(entry_url) == "162"
                                    for entry_url in item.get("all_entry_urls", "").split("；")
                                    if entry_url
                                )
                                else "",
                                gdzy5413_honor,
                                highlights,
                            ]
                            if part
                        )
                    ),
                    520,
                ),
                "列表简介": clip(item.get("description", ""), 700),
                "详情正文摘录": clip(detail.get("profile_text", ""), 1800),
                "来源类型": "医院官网",
                "来源链接": link,
                "采集入口": item.get("entry_url", target.entry_url),
                "采集方式": (
                    "医院官网 ASP.NET 专家团队：GridView 列表+详情页结构化抽取"
                    if gdskin_detail_id(link)
                    else "医院官网专家栏目：指定入口普查+医生详情 DOM 结构化抽取"
                    if ny5y_detail_id(link)
                    else "医院官网名医栏目：严格 specialist typeid 过滤+详情 DOM 结构化抽取"
                    if gdzy5413_detail_id(link)
                    else "医院官网各科专家栏目：严格 ksdoctorinfo 参数过滤+详情 DOM 结构化抽取"
                    if gdzy5413_ksdoctor_detail_id(link)
                    else "医院官网通用模板：列表页自动发现+详情页文本抽取"
                ),
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

    gdzy5413_identity_reconciliation: list[dict[str, Any]] = []
    if target.adapter_id == GDZY5413_ADAPTER_ID:
        rows, gdzy5413_identity_reconciliation = merge_gdzy5413_identity_rows(rows)
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

    sample_entry_urls: list[str] = []
    seen_sample_entries: set[str] = set()
    for row in rows:
        entry_url = clean_text(row.get("采集入口"))
        entry_key = canonical_url(entry_url)
        if entry_url and entry_key not in seen_sample_entries:
            seen_sample_entries.add(entry_key)
            sample_entry_urls.append(entry_url)
    sample_entry_categories = [
        (
            GDSKIN_ENTRY_METADATA[entry_id]["category_name"]
            if (entry_id := gdskin_entry_id(entry_url))
            else NY5Y_ENTRY_METADATA[ny5y_id]["category_name"]
            if (ny5y_id := ny5y_entry_kind(entry_url))
            else GDZY5413_ENTRY_METADATA[gdzy5413_id]["category_name"]
        )
        for entry_url in sample_entry_urls
        if (entry_id := gdskin_entry_id(entry_url))
        or (ny5y_id := ny5y_entry_kind(entry_url))
        or (gdzy5413_id := gdzy5413_entry_kind(entry_url))
    ]
    entry_page_counts = Counter(category.get("entry_url", "") for category in categories)
    gdzy5413_names_by_mode: dict[str, dict[str, dict[str, str]]] = {"851": {}, "852": {}}
    for row in raw_rows:
        entry_kind = gdzy5413_entry_kind(row.get("entry_url"))
        name = re.sub(r"\s+", "", clean_text(row.get("name")))
        if entry_kind in gdzy5413_names_by_mode and name:
            gdzy5413_names_by_mode[entry_kind].setdefault(
                name,
                {"name": name, "source_link": row.get("source_link", ""), "department": row.get("department", "")},
            )
    gdzy5413_cross_mode_matches = [
        {
            "name": name,
            "specialist_source_link": gdzy5413_names_by_mode["851"][name]["source_link"],
            "specialist_department": gdzy5413_names_by_mode["851"][name]["department"],
            "ksdoctor_source_link": gdzy5413_names_by_mode["852"][name]["source_link"],
            "ksdoctor_department": gdzy5413_names_by_mode["852"][name]["department"],
        }
        for name in sorted(set(gdzy5413_names_by_mode["851"]) & set(gdzy5413_names_by_mode["852"]))
    ]
    entry_reconnaissance: list[dict[str, Any]] = []
    for entry_url in entry_urls:
        entry_id = gdskin_entry_id(entry_url)
        ny5y_id = ny5y_entry_kind(entry_url)
        candidate_count = entry_candidate_counts.get(entry_url, 0)
        metadata = (
            GDSKIN_ENTRY_METADATA.get(entry_id, {})
            if entry_id
            else NY5Y_ENTRY_METADATA.get(ny5y_id, {})
            if ny5y_id
            else GDZY5413_ENTRY_METADATA.get(gdzy5413_entry_kind(entry_url), {})
        )
        gdzy5413_id = gdzy5413_entry_kind(entry_url)
        out_of_scope_count = sum(
            1
            for item in excluded_candidates_by_link.values()
            if item.get("entry_url") == entry_url and "另一详情模板" in item.get("reason", "")
        )
        list_page_count = entry_page_counts.get(entry_url, 0)
        entry_reconnaissance.append(
            {
                "entry_url": entry_url,
                "category_name": metadata.get("category_name", f"入口 {entry_id or entry_url}"),
                "page_nature": (
                    "医院官网 ASP.NET GridView 专家列表"
                    if entry_id and candidate_count
                    else "医院官网单页专家名单"
                    if ny5y_id and candidate_count
                    else "医院官网名医名家单页名单"
                    if gdzy5413_id == "851"
                    else "医院官网各科专家单页主目录（ksdoctorinfo 已获 TRIAL-2 授权）"
                    if gdzy5413_id == "852"
                    else "医院官网专家团队分类页（当前未列出可采医生详情）"
                ),
                "raw_detail_relation_count": entry_raw_relation_counts.get(entry_url, 0),
                "unique_detail_count": candidate_count,
                "out_of_scope_detail_count": out_of_scope_count,
                "list_page_count": list_page_count,
                "pagination_evidence": "未发现分页证据" if list_page_count == 1 else f"发现 {list_page_count} 个列表文档",
                "affiliation": metadata.get("affiliation", target.hospital),
                "independent_entity_check": (
                    "未发现独立院区归属；页面保持在本院官网同站专家栏目"
                    if ny5y_id
                    else "owner 已裁决院区/门诊均属同一法人实体授权范围"
                    if gdzy5413_id
                    else "未发现独立挂牌机构；页面保持在医院官网同站专家团队栏目"
                ),
            }
        )

    cross_entry_duplicates = [
        {
            "source_link": item["source_link"],
            "name": item.get("name", ""),
            "entry_urls": item.get("all_entry_urls", "").split("；"),
        }
        for item in by_link.values()
        if len([value for value in item.get("all_entry_urls", "").split("；") if value]) > 1
    ]
    candidate_membership_count = sum(entry_candidate_counts.values())
    out_of_scope_candidate_count = sum(
        1
        for item in excluded_candidates_by_link.values()
        if "另一详情模板" in item.get("reason", "")
    )

    return {
        "meta": {
            "city": target.city,
            "hospital": target.hospital,
            "homepage": target.homepage,
            "entry_url": " ".join(entry_urls),
            "entry_url_count": len(entry_urls),
            "entry_candidate_counts": entry_candidate_counts,
            "entry_raw_relation_counts": entry_raw_relation_counts,
            "entry_url_source": "Claude owner Issue 显式多入口" if target.entry_urls else "官网入口台账",
            "ledger_entry_url": target.ledger_entry_url or target.entry_url,
            "adapter_id": target.adapter_id,
            "collected_at": today,
            "category_count": len(categories),
            "raw_card_rows": len(raw_rows),
            "candidate_membership_count": candidate_membership_count,
            "unique_candidate_count": len(by_link),
            "cross_entry_duplicate_count": candidate_membership_count - len(by_link),
            "unique_doctor_count": len(rows),
            "category_error_count": len(page_errors),
            "detail_error_count": len(detail_errors),
            "existing_profile_count": sum(1 for row in rows if row["已建画像"] == "是"),
            "ledger_review": target.review,
            "ledger_difficulty": target.difficulty,
            "generic_template": "yes" if target.adapter_id == GENERIC_ADAPTER_ID else "no",
            "site_adapter_profile": (
                "gdskin_aspnet_gridview" if target.adapter_id == GDSKIN_ADAPTER_ID else "generic"
                if target.adapter_id not in {NY5Y_ADAPTER_ID, GDZY5413_ADAPTER_ID}
                else "ny5y_strict_expert_dom"
                if target.adapter_id == NY5Y_ADAPTER_ID
                else "gdzy5413_strict_specialist_dom"
            ),
            "generic_max_pages": max_pages,
            "sample_entry_coverage_count": len(sample_entry_urls),
            "sample_entry_categories": sample_entry_categories,
            "excluded_non_doctor_count": len(excluded_candidates_by_link) - out_of_scope_candidate_count,
            "out_of_scope_candidate_count": out_of_scope_candidate_count,
            "gdzy5413_trial2": gdzy5413_trial2,
            "gdzy5413_851_unique_name_count": len(gdzy5413_names_by_mode["851"]),
            "gdzy5413_852_unique_name_count": len(gdzy5413_names_by_mode["852"]),
            "gdzy5413_cross_mode_name_match_count": len(gdzy5413_cross_mode_matches),
            "gdzy5413_detail_relation_count": len(detail_items),
            "gdzy5413_final_identity_count": len(rows),
            "gdzy5413_trial2_sample_relation_count": len(detail_items),
            "gdzy5413_trial2_sample_identity_count": len(rows),
            "gdzy5413_trial2_baiyun_sample_count": sum(
                1 for row in rows if "白云院区" in clean_text(row.get("科室_分类页"))
            ),
            "gdzy5413_trial2_merged_identity_count": sum(
                1
                for item in gdzy5413_identity_reconciliation
                if item.get("resolution") == "同一人归并" and int(item.get("relation_count") or 0) > 1
            ),
        },
        "categories": categories,
        "entry_reconnaissance": entry_reconnaissance,
        "cross_entry_duplicates": cross_entry_duplicates,
        "gdzy5413_cross_mode_matches": gdzy5413_cross_mode_matches,
        "gdzy5413_identity_reconciliation": gdzy5413_identity_reconciliation,
        "excluded_candidates": list(excluded_candidates_by_link.values()),
        "category_errors": page_errors,
        "detail_errors": detail_errors,
        "category_counts": category_counter.most_common(),
        "priority_counts": dict(priority_counter),
        "group_counts": dict(group_counter),
        "warning_counts": dict(warning_counter),
        "rows": rows,
    }


def validate_gdskin_full_append(payload: dict[str, Any]) -> None:
    """Fail before master writes when the owner-audited GDSKIN census has drifted."""

    errors: list[str] = []
    meta = payload.get("meta", {})
    expected_total = sum(GDSKIN_EXPECTED_ENTRY_COUNTS.values())
    if int(meta.get("unique_candidate_count") or 0) != expected_total:
        errors.append(
            f"唯一候选预期 {expected_total}，实际 {meta.get('unique_candidate_count', 0)}"
        )
    if int(meta.get("unique_doctor_count") or 0) != expected_total:
        errors.append(f"医生记录预期 {expected_total}，实际 {meta.get('unique_doctor_count', 0)}")
    if int(meta.get("candidate_membership_count") or 0) != expected_total:
        errors.append(
            f"入口候选关系预期 {expected_total}，实际 {meta.get('candidate_membership_count', 0)}"
        )
    if int(meta.get("cross_entry_duplicate_count") or 0) != 0:
        errors.append(f"跨入口重复预期 0，实际 {meta.get('cross_entry_duplicate_count', 0)}")
    if int(meta.get("category_error_count") or 0) != 0:
        errors.append(f"列表读取失败 {meta.get('category_error_count', 0)} 条")
    if int(meta.get("detail_error_count") or 0) != 0:
        errors.append(f"详情读取失败 {meta.get('detail_error_count', 0)} 条")
    if int(meta.get("excluded_non_doctor_count") or 0) != 1:
        errors.append(f"非医生排除预期 1，实际 {meta.get('excluded_non_doctor_count', 0)}")

    reconnaissance_by_id = {
        entry_id: item
        for item in payload.get("entry_reconnaissance", [])
        if (entry_id := gdskin_entry_id(str(item.get("entry_url") or "")))
    }
    for entry_id, expected_count in GDSKIN_EXPECTED_ENTRY_COUNTS.items():
        item = reconnaissance_by_id.get(entry_id)
        if item is None:
            errors.append(f"入口 {entry_id} 缺少普查记录")
            continue
        actual_count = int(item.get("unique_detail_count") or 0)
        if actual_count != expected_count:
            errors.append(f"入口 {entry_id} 唯一详情预期 {expected_count}，实际 {actual_count}")
        expected_pages = GDSKIN_EXPECTED_PAGE_COUNTS[entry_id]
        actual_pages = int(item.get("list_page_count") or 0)
        if actual_pages != expected_pages:
            errors.append(f"入口 {entry_id} 列表页预期 {expected_pages}，实际 {actual_pages}")

    general_department_rows = [
        str(row.get("姓名") or "未命名")
        for row in payload.get("rows", [])
        if str(row.get("科室_分类页") or "") in GDSKIN_GENERAL_CATEGORIES
    ]
    if general_department_rows:
        errors.append(
            "科室仍为首席/知名专家类目：" + "、".join(general_department_rows)
        )

    if errors:
        raise RuntimeError("GDSKIN 全量写入前门禁失败：" + "；".join(errors))


def validate_gdzy5413_trial2(payload: dict[str, Any], expected_identities: int = 10) -> None:
    """Protect the owner-audited TRIAL-2 census, sample composition, and URL scope."""

    meta = payload.get("meta", {})
    rows = payload.get("rows", [])
    errors: list[str] = []
    entry_counts = meta.get("entry_candidate_counts", {})
    if sorted(int(value) for value in entry_counts.values()) != [21, 346]:
        errors.append(f"851/852 唯一详情应为 21/346，实际 {entry_counts}")
    if int(meta.get("gdzy5413_852_unique_name_count") or 0) != 289:
        errors.append(f"852 唯一姓名应为 289，实际 {meta.get('gdzy5413_852_unique_name_count')}")
    if int(meta.get("gdzy5413_cross_mode_name_match_count") or 0) != 20:
        errors.append(
            "851/852 同名应为 20，实际 "
            f"{meta.get('gdzy5413_cross_mode_name_match_count')}"
        )
    if len(rows) != expected_identities:
        errors.append(f"最终身份应为 {expected_identities}，实际 {len(rows)}")
    if int(meta.get("gdzy5413_trial2_baiyun_sample_count") or 0) < 1:
        errors.append("样本缺少白云院区条目")
    if int(meta.get("gdzy5413_trial2_merged_identity_count") or 0) < 1:
        errors.append("样本缺少多链接同一人归并案例")
    if int(meta.get("gdzy5413_trial2_sample_relation_count") or 0) <= len(rows):
        errors.append("样本详情关系数未体现多链接归并")
    if int(meta.get("department_coverage_count") or 0) < 3:
        errors.append("样本科室覆盖不足 3 个")
    if int(meta.get("category_error_count") or 0) or int(meta.get("detail_error_count") or 0):
        errors.append("列表或详情存在读取失败")
    relation_links = [
        link
        for item in payload.get("gdzy5413_identity_reconciliation", [])
        for link in [item.get("primary_source_link"), *item.get("merged_source_links", [])]
        if link
    ]
    if len(relation_links) != int(meta.get("gdzy5413_trial2_sample_relation_count") or 0):
        errors.append("归并对账中的详情关系数与抽样关系数不一致")
    if any(not gdzy5413_ksdoctor_detail_id(link) for link in relation_links):
        errors.append("样本归并对账含非授权 ksdoctorinfo 来源")
    if errors:
        raise RuntimeError("GDZY5413 TRIAL-2 门禁失败：" + "；".join(errors))


def validate_gdzy5413_full_append(payload: dict[str, Any]) -> None:
    """Fail before master writes when the owner-audited FULL census or identity audit drifts."""

    meta = payload.get("meta", {})
    rows = payload.get("rows", [])
    reconciliation = payload.get("gdzy5413_identity_reconciliation", [])
    errors: list[str] = []
    entry_counts = {
        gdzy5413_entry_kind(str(entry_url)): int(count)
        for entry_url, count in meta.get("entry_candidate_counts", {}).items()
        if gdzy5413_entry_kind(str(entry_url))
    }
    if entry_counts != {"851": 21, "852": 346}:
        errors.append(f"851/852 唯一详情应为 21/346，实际 {entry_counts}")
    if int(meta.get("gdzy5413_851_unique_name_count") or 0) != 21:
        errors.append(f"851 唯一姓名应为 21，实际 {meta.get('gdzy5413_851_unique_name_count')}")
    if int(meta.get("gdzy5413_852_unique_name_count") or 0) != 289:
        errors.append(f"852 唯一姓名应为 289，实际 {meta.get('gdzy5413_852_unique_name_count')}")
    if int(meta.get("gdzy5413_cross_mode_name_match_count") or 0) != 20:
        errors.append(
            "851/852 同名应为 20，实际 "
            f"{meta.get('gdzy5413_cross_mode_name_match_count')}"
        )
    if int(meta.get("category_error_count") or 0) or int(meta.get("detail_error_count") or 0):
        errors.append("列表或详情存在读取失败")
    if not 290 <= len(rows) <= 367:
        errors.append(f"最终身份数应在姓名并集 290 与详情关系 367 之间，实际 {len(rows)}")
    if len(reconciliation) != len(rows):
        errors.append(f"归并对账行数应等于最终身份数，实际 {len(reconciliation)}/{len(rows)}")

    relation_links = [
        str(link)
        for item in reconciliation
        for link in [item.get("primary_source_link"), *item.get("merged_source_links", [])]
        if link
    ]
    relation_count = sum(int(item.get("relation_count") or 0) for item in reconciliation)
    if len(relation_links) != 367 or relation_count != 367:
        errors.append(f"归并详情关系应为 367，实际链接 {len(relation_links)} / 对账 {relation_count}")
    if len(set(relation_links)) != len(relation_links):
        errors.append("归并对账存在重复详情链接")
    specialist_links = [link for link in relation_links if gdzy5413_detail_id(link)]
    ksdoctor_links = [link for link in relation_links if gdzy5413_ksdoctor_detail_id(link)]
    if len(specialist_links) != 21 or len(ksdoctor_links) != 346:
        errors.append(
            f"归并对账授权链接应为 specialist 21 / ksdoctorinfo 346，实际 "
            f"{len(specialist_links)} / {len(ksdoctor_links)}"
        )
    if len(specialist_links) + len(ksdoctor_links) != len(relation_links):
        errors.append("归并对账含非授权详情链接")

    for row in rows:
        if clean_text(row.get("医院")) != "广东省第二中医院":
            errors.append("存在医院字段未统一为广东省第二中医院")
            break
        source_link = str(row.get("来源链接") or "")
        if not (gdzy5413_detail_id(source_link) or gdzy5413_ksdoctor_detail_id(source_link)):
            errors.append("最终行含非授权主详情链接")
            break
        expected_titles = "、".join(extract_terms(clean_text(row.get("职称身份原文")), TITLE_TERMS))
        if clean_text(row.get("职称_关键词")) != expected_titles:
            errors.append(f"{row.get('姓名', '未命名')} 的职称关键词未严格取自主详情")
            break
        if re.match(r"^\s*擅长\s*[:：]", str(row.get("擅长诊疗方向摘录") or "")):
            errors.append(f"{row.get('姓名', '未命名')} 的擅长字段仍保留前缀")
            break

    if errors:
        raise RuntimeError("GDZY5413 FULL 写入前门禁失败：" + "；".join(errors))


def validate_ny5y_full_append(payload: dict[str, Any]) -> None:
    meta = payload.get("meta", {})
    rows = payload.get("rows", [])
    errors: list[str] = []

    if int(meta.get("unique_doctor_count") or 0) != NY5Y_EXPECTED_UNIQUE_COUNT:
        errors.append(
            f"医生记录预期 {NY5Y_EXPECTED_UNIQUE_COUNT}，实际 {meta.get('unique_doctor_count', 0)}"
        )
    if len(rows) != NY5Y_EXPECTED_UNIQUE_COUNT:
        errors.append(f"结果行数预期 {NY5Y_EXPECTED_UNIQUE_COUNT}，实际 {len(rows)}")
    if int(meta.get("unique_candidate_count") or 0) != NY5Y_EXPECTED_UNIQUE_COUNT:
        errors.append(
            f"去重候选预期 {NY5Y_EXPECTED_UNIQUE_COUNT}，实际 {meta.get('unique_candidate_count', 0)}"
        )
    expected_memberships = sum(NY5Y_EXPECTED_ENTRY_COUNTS.values())
    if int(meta.get("candidate_membership_count") or 0) != expected_memberships:
        errors.append(
            f"入口候选关系预期 {expected_memberships}，实际 {meta.get('candidate_membership_count', 0)}"
        )
    if int(meta.get("cross_entry_duplicate_count") or 0) != NY5Y_EXPECTED_CROSS_ENTRY_DUPLICATES:
        errors.append(
            "跨入口重复预期 "
            f"{NY5Y_EXPECTED_CROSS_ENTRY_DUPLICATES}，实际 {meta.get('cross_entry_duplicate_count', 0)}"
        )
    if int(meta.get("category_error_count") or 0) != 0:
        errors.append(f"列表读取失败 {meta.get('category_error_count', 0)} 条")
    if int(meta.get("detail_error_count") or 0) != 0:
        errors.append(f"详情读取失败 {meta.get('detail_error_count', 0)} 条")
    if int(meta.get("excluded_non_doctor_count") or 0) != 0:
        errors.append(f"非医生排除预期 0，实际 {meta.get('excluded_non_doctor_count', 0)}")

    actual_entry_counts: dict[str, int] = {}
    for entry_url, count in meta.get("entry_candidate_counts", {}).items():
        if entry_id := ny5y_entry_kind(str(entry_url)):
            actual_entry_counts[entry_id] = int(count)
    for entry_id, expected_count in NY5Y_EXPECTED_ENTRY_COUNTS.items():
        actual_count = actual_entry_counts.get(entry_id)
        if actual_count != expected_count:
            errors.append(f"入口 {entry_id} 唯一详情预期 {expected_count}，实际 {actual_count}")

    source_ids = [ny5y_detail_id(str(row.get("来源链接") or "")) for row in rows]
    if any(not source_id for source_id in source_ids):
        errors.append("存在非授权 yisheng_xq.php?id=<数字> 来源")
    if len({source_id for source_id in source_ids if source_id}) != len(rows):
        errors.append("结果中存在重复来源详情 ID")

    prefixed_specialties = [
        str(row.get("姓名") or "未命名")
        for row in rows
        if re.match(r"^\s*擅长\s*[:：]", str(row.get("擅长诊疗方向摘录") or ""))
    ]
    if prefixed_specialties:
        errors.append("擅长字段仍保留前缀：" + "、".join(prefixed_specialties[:10]))

    huang_rows = [row for row in rows if clean_text(str(row.get("姓名") or "")) == "黄艺洪"]
    if len(huang_rows) != 1:
        errors.append(f"黄艺洪记录预期 1，实际 {len(huang_rows)}")
    else:
        huang = huang_rows[0]
        if clean_text(str(huang.get("科室_分类页") or "")):
            errors.append("黄艺洪真实科室应保持空白")
        if "科室需人工复核" not in str(huang.get("异常提示") or ""):
            errors.append("黄艺洪缺少科室需人工复核标记")
        if "岭南名医" not in " ".join(
            [str(huang.get("职称身份原文") or ""), str(huang.get("亮眼经历线索") or "")]
        ):
            errors.append("黄艺洪缺少岭南名医官方荣誉证据")

    if errors:
        raise RuntimeError("NY5Y 全量写入前门禁失败：" + "；".join(errors))


def validate_gykqyy_full_append(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    rows = payload["rows"]
    reconciliation = payload.get("gykqyy_identity_reconciliation", [])
    errors: list[str] = []
    if int(meta.get("candidate_membership_count") or 0) != 317:
        errors.append(f"医生-科室关系应为 317，实际 {meta.get('candidate_membership_count', 0)}")
    if int(meta.get("census_unique_detail_count") or 0) != 297:
        errors.append(f"唯一详情 ID 应为 297，实际 {meta.get('census_unique_detail_count', 0)}")
    named_count = int(meta.get("census_named_detail_count") or 0)
    blank_count = int(meta.get("census_blank_name_detail_count") or 0)
    if named_count + blank_count != 297:
        errors.append("有姓名与空姓名详情 ID 之和不等于 297")
    if int(meta.get("detail_error_count") or 0) != 0:
        errors.append(f"详情接口失败应为 0，实际 {meta.get('detail_error_count', 0)}")
    if len(rows) != named_count or int(meta.get("gykqyy_final_row_count") or 0) != named_count:
        errors.append(f"正式行应等于有姓名详情 ID 数 {named_count}，实际 {len(rows)}")
    if len(reconciliation) != len(rows):
        errors.append(f"逐 ID 对账行应等于正式行，实际 {len(reconciliation)}/{len(rows)}")
    if any(not clean_text(str(row.get("姓名") or "")) for row in rows):
        errors.append("正式行存在空姓名")
    if len({canonical_url(str(row.get("来源链接") or "")) for row in rows}) != len(rows):
        errors.append("正式行来源链接不唯一")
    expected_same_name_groups = {"方颖": ["128", "307"], "赵稚宁": ["29", "323"]}
    if meta.get("census_same_name_groups") != expected_same_name_groups:
        errors.append(f"同名不同 ID 组不符合审计基线：{meta.get('census_same_name_groups', {})}")
    if int(meta.get("gykqyy_same_name_separate_row_count") or 0) != 4:
        errors.append(
            f"方颖/赵稚宁应共保留 4 行，实际 {meta.get('gykqyy_same_name_separate_row_count', 0)}"
        )
    same_name_rows = [row for row in rows if clean_text(str(row.get("姓名") or "")) in expected_same_name_groups]
    if len(same_name_rows) != 4 or any(
        "同名待甄别" not in str(row.get("异常提示") or "") for row in same_name_rows
    ):
        errors.append("同名不同 ID 行未全部保留“同名待甄别”")
    blank_excluded_count = sum(
        1
        for item in payload.get("excluded_candidates", [])
        if "核心追溯字段缺失" in str(item.get("reason") or "")
    )
    if blank_excluded_count != blank_count:
        errors.append(f"空姓名详情应全部进入排除对账，实际 {blank_excluded_count}/{blank_count}")
    if errors:
        raise RuntimeError("GYKQYY FULL 写入前门禁失败：" + "；".join(errors))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BASE_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def render_counter_table(counter: dict[str, int] | list[tuple[str, int]], empty: str = "| 无 | 0 |") -> str:
    items = counter.items() if isinstance(counter, dict) else counter
    lines = [f"| {name} | {count} |" for name, count in items if name]
    return "\n".join(lines) if lines else empty


def markdown_table_cell(value: Any) -> str:
    return clean_text(str(value or "")).replace("|", "\\|")


def write_report(path: Path, payload: dict[str, Any], csv_path: Path, xlsx_path: Path) -> None:
    meta = payload["meta"]
    full_append = meta.get("execution_mode") == "full_append"
    report_label = "全量采集归并审计报告" if full_append else "自动采集试跑报告"
    report_title = "官方医生全量采集归并审计报告" if full_append else "官方医生自动采集试跑报告"
    run_label = "全量采集" if full_append else "试采"
    xlsx_output = f"`{xlsx_path}`" if xlsx_path.exists() else "未生成（本轮使用 --no-xlsx）"
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
    entry_recon_lines = "\n".join(
        (
            f"| {item.get('category_name', '')} | {item.get('entry_url', '')} | "
            f"{item.get('page_nature', '')} | {item.get('list_page_count', 0)} | "
            f"{item.get('raw_detail_relation_count', item.get('unique_detail_count', 0))} | "
            f"{item.get('unique_detail_count', 0)} | {item.get('out_of_scope_detail_count', 0)} | "
            f"{item.get('affiliation', '')} | "
            f"{item.get('independent_entity_check', '')} |"
        )
        for item in payload.get("entry_reconnaissance", [])
    ) or "| 无 | 无 | 无 | 0 | 0 | 0 | 0 | 无 | 无 |"
    excluded_lines = "\n".join(
        (
            f"| {item.get('entry_url', '')} | {markdown_table_cell(item.get('list_title', ''))} | "
            f"{item.get('source_link', '')} | {item.get('reason', '')} |"
        )
        for item in payload.get("excluded_candidates", [])
    ) or "| 无 | 无 | 无 | 无 |"
    duplicate_lines = "\n".join(
        (
            f"| {item.get('name', '')} | {item.get('source_link', '')} | "
            f"{'；'.join(item.get('entry_urls', []))} |"
        )
        for item in payload.get("cross_entry_duplicates", [])
    ) or "| 无 | 无 | 无 |"
    same_name_lines = "\n".join(
        f"| {markdown_table_cell(name)} | {','.join(ids)} |"
        for name, ids in meta.get("census_same_name_groups", {}).items()
    ) or "| 无 | 无 |"
    identity_reconciliation_lines = "\n".join(
        (
            f"| {item.get('name', '')} | {item.get('resolution', '')} | "
            f"{item.get('relation_count', 0)} | {'、'.join(item.get('departments', []))} | "
            f"{item.get('primary_source_link', '')} | "
            f"{'；'.join(item.get('merged_source_links', [])) or '无'} |"
        )
        for item in payload.get("gdzy5413_identity_reconciliation", [])
    ) or "| 无 | 无 | 0 | 无 | 无 | 无 |"
    gykqyy_reconciliation_lines = "\n".join(
        (
            f"| {item.get('detail_id', '')} | {markdown_table_cell(item.get('name', ''))} | "
            f"{item.get('resolution', '')} | {'、'.join(item.get('departments', [])) or '无'} | "
            f"{item.get('source_link', '')} | {item.get('reason', '')} |"
        )
        for item in payload.get("gykqyy_identity_reconciliation", [])
    ) or "| 无 | 无 | 无 | 无 | 无 | 无 |"

    report = f"""---
类型: {report_label}
医院: {meta['hospital']}
城市: {meta['city']}
采集日期: {meta['collected_at']}
来源范围: 医院官网
采集入口: {meta['entry_url']}
适配器: {meta['adapter_id']}
---

# {meta['hospital']} {report_title}

## 结论

本次试跑只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集{run_label}底表，共 {meta['unique_doctor_count']} 位唯一医生；官网列表页原始卡片记录 {meta['raw_card_rows']} 条；读取入口分类 {meta['category_count']} 个；覆盖 {meta.get('department_coverage_count', 0)} 个科室；详情页失败 {meta['detail_error_count']} 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | {meta['city']} |
| 医院 | {meta['hospital']} |
| 官网首页 | {meta['homepage']} |
| 本轮医生入口 | {meta['entry_url']} |
| 入口来源 | {meta.get('entry_url_source', '官网入口台账')} |
| 原台账医生入口 | {meta.get('ledger_entry_url', meta['entry_url'])} |
| 台账人工复核 | {meta['ledger_review']} |
| 采集难度初判 | {meta['ledger_difficulty']} |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
{entry_recon_lines}

### 动态目录专项证据

- 医生分页/载入方式：{meta.get('pagination_method', '按列表页分页读取')}
- 医生目录公开接口：{meta.get('directory_api', '不适用')}
- 医生详情公开接口：{meta.get('detail_api', '不适用')}
- 接口出处证据：{meta.get('api_source_evidence', '不适用')}
- 院区/分组：{meta.get('census_group_count', 0)} 个；科室分类：{meta.get('census_department_count', 0)} 个
- 医生-科室关系：{meta.get('candidate_membership_count', meta['raw_card_rows'])} 条
- 唯一详情 ID：{meta.get('census_unique_detail_count', meta.get('unique_candidate_count', meta['unique_doctor_count']))} 个
- 有姓名详情 ID：{meta.get('census_named_detail_count', meta.get('census_unique_nonblank_name_count', meta['unique_doctor_count']))} 个
- 空姓名详情 ID：{meta.get('census_blank_name_detail_count', 0)} 个
- 去重后的非空姓名值：{meta.get('census_unique_nonblank_name_count', meta['unique_doctor_count'])} 个
- 同名不同详情 ID：{meta.get('census_same_name_group_count', 0)} 组

| 同名 | 详情 ID |
|---|---|
{same_name_lines}

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：{meta.get('candidate_membership_count', meta['raw_card_rows'])}
- 跨入口去重后唯一候选：{meta.get('unique_candidate_count', meta['unique_doctor_count'])}
- 跨入口重复关系：{meta.get('cross_entry_duplicate_count', 0)}
- 试采覆盖入口分类：{meta.get('sample_entry_coverage_count', 0)} 个（{'、'.join(meta.get('sample_entry_categories', [])) or '无'}）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
{duplicate_lines}

## 广东省第二中医院同名归并对账

- 详情关系：{meta.get('gdzy5413_detail_relation_count', meta.get('gdzy5413_trial2_sample_relation_count', 0))}
- 最终身份：{meta.get('gdzy5413_final_identity_count', meta.get('gdzy5413_trial2_sample_identity_count', 0))}
- 白云院区样本：{meta.get('gdzy5413_trial2_baiyun_sample_count', 0)}
- 多链接同一人归并样本：{meta.get('gdzy5413_trial2_merged_identity_count', 0)}

| 姓名 | 裁决 | 详情关系 | 合并科室 | 主详情 | 其余详情 |
|---|---|---:|---|---|---|
{identity_reconciliation_lines}

## 广医口腔逐 ID 归并/排除对账

- 目录详情 ID：{meta.get('census_unique_detail_count', meta.get('unique_candidate_count', 0))}
- 有姓名详情 ID / 正式行：{meta.get('census_named_detail_count', 0)} / {meta.get('gykqyy_final_row_count', 0)}
- 空姓名详情 ID：{meta.get('census_blank_name_detail_count', 0)}
- 同名不同 ID 分行：{meta.get('gykqyy_same_name_separate_row_count', 0)}

| 详情 ID | 姓名 | 处置 | 科室 | 来源链接 | 理由 |
|---|---|---|---|---|---|
{gykqyy_reconciliation_lines}

## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
{excluded_lines}

## 输出文件

- Excel 底表：{xlsx_output}
- CSV 底表：`{csv_path}`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | {meta['category_count']} |
| 原始医生卡片记录 | {meta['raw_card_rows']} |
| 跨入口去重前候选关系 | {meta.get('candidate_membership_count', meta['raw_card_rows'])} |
| 跨入口去重后唯一候选 | {meta.get('unique_candidate_count', meta['unique_doctor_count'])} |
| 排除非医生候选 | {meta.get('excluded_non_doctor_count', 0)} |
| 唯一医生详情页 | {meta['unique_doctor_count']} |
| 覆盖科室数 | {meta.get('department_coverage_count', 0)} |
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
4. 标记为试采门禁的适配器必须先完成小样本复核；只有取得 Claude 明确通过指令后才可全量追加。

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

本次批次医院：{meta.get('current_batch_hospital') or '无，本次仅重建总表'}；本次批次原始医生数 {meta.get('current_batch_rows', 0)}；新增写入 {meta.get('new_rows_added', 0)}；重复跳过 {meta.get('duplicate_rows_skipped', 0)}；显式刷新既有记录 {meta.get('existing_rows_refreshed', 0)}；初始化合并时识别并折叠既有重复 {meta.get('existing_duplicate_rows', 0)}。

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
    parser.add_argument(
        "--entry-url",
        action="append",
        default=[],
        help="显式覆盖医生目录入口；多入口时重复传入，且必须与医院官网同域",
    )
    parser.add_argument("--today", default=date.today().isoformat(), help="采集日期")
    parser.add_argument("--max-doctors", type=int, default=0, help="仅测试前 N 位医生；0 表示全量")
    parser.add_argument("--min-departments", type=int, default=0, help="要求结果至少覆盖的非空科室数；0 表示不设门禁")
    parser.add_argument(
        "--min-entry-categories",
        type=int,
        default=0,
        help="要求试采结果至少覆盖的显式入口分类数；0 表示不设门禁",
    )
    parser.add_argument("--max-pages", type=int, default=GENERIC_MAX_PAGES_DEFAULT, help="通用模板最多读取的列表分页数")
    parser.add_argument("--trial-only", action="store_true", help="仅试采并输出临时底表/报告，不追加统一总底表；未指定 --max-doctors 时默认试采 10 位")
    parser.add_argument("--force-generic", action="store_true", help="即使已有专用适配器，也强制使用通用模板试采")
    parser.add_argument("--allow-generic-append", action="store_true", help="允许通用模板结果追加统一总底表；建议先完成 --trial-only 人工复核")
    parser.add_argument(
        "--refresh-existing-hospital",
        action="store_true",
        help="仅在显式指定医院并通过追加门禁时，用本轮官网结果刷新同来源既有记录。",
    )
    parser.add_argument("--no-xlsx", action="store_true", help="只生成 JSON/CSV/报告，不生成 Excel")
    parser.add_argument(
        "--gdzy5413-trial2",
        action="store_true",
        help="Issue #17 TRIAL-2：仅从 cid=852 的 ksdoctorinfo 主目录抽样，仍普查 851 用于跨模式去重说明",
    )
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

    if args.refresh_existing_hospital and (not args.hospital or not args.allow_generic_append):
        raise RuntimeError("刷新既有医院记录必须同时指定 --hospital 和 --allow-generic-append。")

    if args.rebuild_master_only:
        previous_batch_meta: dict[str, Any] = {}
        if MASTER_JSON_PATH.exists():
            try:
                previous_payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
                previous_batch_meta = previous_payload.get("meta", {})
            except (OSError, ValueError, TypeError):
                previous_batch_meta = {}
        payload = build_master_payload(args.today, batch_meta_override=previous_batch_meta)
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
    if args.gdzy5413_trial2 and (target.hospital != "广东省第二中医院" or not args.trial_only):
        raise RuntimeError("--gdzy5413-trial2 只允许广东省第二中医院的 --trial-only 补充试采。")
    if args.entry_url:
        if not args.hospital:
            raise RuntimeError("使用 --entry-url 覆盖入口时必须同时指定 --hospital。")
        override_urls: list[str] = []
        seen_override_urls: set[str] = set()
        official_host = comparable_host(target.homepage)
        for raw_url in args.entry_url:
            value = clean_text(raw_url)
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise RuntimeError(f"无效的医生目录入口：{value}")
            if comparable_host(value) != official_host:
                raise RuntimeError(f"医生目录入口与医院官网不同域，拒绝执行：{value}")
            key = canonical_url(value)
            if key not in seen_override_urls:
                seen_override_urls.add(key)
                override_urls.append(value)
        target = replace(
            target,
            entry_url=override_urls[0],
            entry_urls=tuple(override_urls),
            ledger_entry_url=target.entry_url,
            adapter_id=adapter_for(override_urls[0], include_generic=True),
        )
    if args.force_generic:
        target = replace(target, adapter_id=GENERIC_ADAPTER_ID)
    print(
        f"selected: {target.city} {target.hospital} "
        f"{' '.join(effective_entry_urls(target))} adapter={target.adapter_id}"
    )

    if (
        target.adapter_id in {GENERIC_ADAPTER_ID, GDSKIN_ADAPTER_ID, NY5Y_ADAPTER_ID, GDZY5413_ADAPTER_ID}
        and not args.trial_only
        and not args.single_output
        and not args.allow_generic_append
    ):
        raise RuntimeError(
            "试采门禁适配器结果存在误识别风险。请先运行 --trial-only --max-doctors 10 试采复核；"
            "确认质量可接受后，再增加 --allow-generic-append 全量追加统一总底表。"
        )

    max_doctors = args.max_doctors or (10 if args.trial_only else None)
    if target.adapter_id == "gzzoc_drupal_doctor":
        payload = collect_gzzoc(target, args.today, max_doctors=max_doctors)
    elif target.adapter_id == "nbkjyy_static_expert":
        payload = collect_nbkj(target, args.today, max_doctors=max_doctors)
    elif target.adapter_id == GYKQYY_ADAPTER_ID:
        payload = collect_gykqyy(target, args.today, max_doctors=max_doctors)
    elif target.adapter_id in {GENERIC_ADAPTER_ID, GDSKIN_ADAPTER_ID, NY5Y_ADAPTER_ID, GDZY5413_ADAPTER_ID}:
        payload = collect_generic(
            target,
            args.today,
            max_doctors=max_doctors,
            max_pages=args.max_pages,
            gdzy5413_trial2=args.gdzy5413_trial2,
        )
    else:
        raise RuntimeError(f"暂不支持的适配器：{target.adapter_id}")

    if args.entry_url:
        failed_entries = [
            entry_url
            for entry_url, count in payload["meta"].get("entry_candidate_counts", {}).items()
            if int(count) == 0
        ]
        empty_entries_blocking = [
            entry_url
            for entry_url in failed_entries
            if not (
                (target.adapter_id == GDSKIN_ADAPTER_ID and gdskin_entry_id(entry_url) == "924")
                or (target.adapter_id == GDZY5413_ADAPTER_ID and gdzy5413_entry_kind(entry_url) == "852")
            )
        ]
        if payload["meta"].get("category_error_count") or empty_entries_blocking:
            raise RuntimeError(
                "显式多入口采集不完整："
                f"列表错误 {payload['meta'].get('category_error_count', 0)} 条，"
                f"无候选入口 {'、'.join(empty_entries_blocking) or '无'}"
            )

    if args.min_entry_categories:
        coverage_count = int(payload["meta"].get("sample_entry_coverage_count") or 0)
        if coverage_count < args.min_entry_categories:
            raise RuntimeError(
                "入口分类覆盖门禁不满足："
                f"要求至少 {args.min_entry_categories} 个，实际 {coverage_count} 个："
                f"{'、'.join(payload['meta'].get('sample_entry_categories', [])) or '无'}"
            )

    covered_departments = sorted(
        {
            clean_text(str(row.get("科室_分类页") or ""))
            for row in payload["rows"]
            if clean_text(str(row.get("科室_分类页") or ""))
            and "非医生页面或姓名异常" not in str(row.get("异常提示") or "")
        }
    )
    payload["meta"]["department_coverage_count"] = len(covered_departments)
    payload["meta"]["covered_departments"] = covered_departments
    if args.min_departments and len(covered_departments) < args.min_departments:
        raise RuntimeError(
            f"科室覆盖门禁不满足：要求至少 {args.min_departments} 个，实际 {len(covered_departments)} 个："
            f"{'、'.join(covered_departments) or '无'}"
        )

    if args.gdzy5413_trial2:
        validate_gdzy5413_trial2(payload, expected_identities=max_doctors or 10)

    if target.adapter_id == GDZY5413_ADAPTER_ID and not args.trial_only and not args.single_output:
        validate_gdzy5413_full_append(payload)
    if target.adapter_id == GYKQYY_ADAPTER_ID and not args.trial_only and not args.single_output:
        validate_gykqyy_full_append(payload)
    if target.adapter_id == GDSKIN_ADAPTER_ID and not args.trial_only and not args.single_output:
        validate_gdskin_full_append(payload)
    if target.adapter_id == NY5Y_ADAPTER_ID and not args.trial_only and not args.single_output:
        validate_ny5y_full_append(payload)

    safe_name = safe_file_part(target.hospital)
    json_path = WORK_DIR / f"{safe_name}_official_doctors_payload.json"
    preview_path = WORK_DIR / f"{safe_name}_official_doctors_preview.png"

    if args.trial_only:
        payload["meta"]["execution_mode"] = "trial"
        json_path = WORK_DIR / f"{safe_name}_trial_payload.json"
        csv_path = WORK_DIR / f"{safe_name}_trial_doctors.csv"
        xlsx_path = WORK_DIR / f"{safe_name}_trial_doctors.xlsx"
        report_path = WORK_DIR / f"{safe_name}_trial_report.md"

        payload["meta"]["json_path"] = str(json_path)
        payload["meta"]["csv_path"] = str(csv_path)
        payload["meta"]["xlsx_path"] = "" if args.no_xlsx else str(xlsx_path)
        payload["meta"]["preview_path"] = "" if args.no_xlsx else str(preview_path)

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
                    "xlsx": "" if args.no_xlsx else str(xlsx_path),
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

    payload["meta"]["execution_mode"] = "full_append"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    master_payload = build_master_payload(
        args.today,
        incoming_payload=payload,
        refresh_incoming=args.refresh_existing_hospital,
        replace_incoming_hospital=target.adapter_id == GDZY5413_ADAPTER_ID,
    )
    MASTER_JSON_PATH.write_text(json.dumps(master_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(MASTER_CSV_PATH, master_payload["rows"])

    if not args.no_xlsx:
        build_workbook(MASTER_JSON_PATH, MASTER_XLSX_PATH, MASTER_PREVIEW_PATH)

    write_master_report(MASTER_REPORT_PATH, master_payload, MASTER_CSV_PATH, MASTER_XLSX_PATH)
    full_report_path = WORK_DIR / f"{safe_name}_official_doctors_report.md"
    write_report(full_report_path, payload, MASTER_CSV_PATH, MASTER_XLSX_PATH)
    print(
        json.dumps(
            {
                "mode": "master_append",
                "hospital": target.hospital,
                "batch_rows": payload["meta"]["unique_doctor_count"],
                "new_rows_added": master_payload["meta"]["new_rows_added"],
                "duplicate_rows_skipped": master_payload["meta"]["duplicate_rows_skipped"],
                "existing_rows_refreshed": master_payload["meta"]["existing_rows_refreshed"],
                "master_rows": master_payload["meta"]["unique_doctor_count"],
                "detail_errors": payload["meta"]["detail_error_count"],
                "csv": str(MASTER_CSV_PATH),
                "xlsx": str(MASTER_XLSX_PATH),
                "report": str(MASTER_REPORT_PATH),
                "hospital_audit_report": str(full_report_path),
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
