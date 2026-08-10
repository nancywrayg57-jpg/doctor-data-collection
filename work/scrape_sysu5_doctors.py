from __future__ import annotations

import csv
import json
import re
import time
from collections import Counter, defaultdict
from datetime import date
from html import unescape
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


BASE = "https://www.sysu5.cn"
HOSPITAL = "中山大学附属第五医院"
ENTRY_URL = (
    "https://www.sysu5.cn/medical-service/department-expert/doctor/"
    "category?category_target_id=All&combine="
)
TODAY = "2026-08-08"

ROOT = Path(r"D:\workspace\信息收集整理")
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL_DIR = VAULT / "01_试点医院" / HOSPITAL
WORK_DIR = ROOT / "work"

JSON_OUT = WORK_DIR / "sysu5_doctors_auto_base.json"
CSV_OUT = SOURCE_DIR / "中山大学附属第五医院_全院医生自动采集底表.csv"
XLSX_OUT = SOURCE_DIR / "中山大学附属第五医院_全院医生自动采集底表.xlsx"
REPORT_OUT = SOURCE_DIR / "中山大学附属第五医院_全院医生自动采集试跑报告.md"


TITLE_TERMS = [
    "主任医师",
    "副主任医师",
    "主治医师",
    "住院医师",
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


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value or "")).strip()


def clip(value: str, max_len: int) -> str:
    value = clean_text(value)
    if len(value) <= max_len:
        return value
    return value[: max_len - 3] + "..."


def fetch(session: requests.Session, url: str, retries: int = 3) -> tuple[int | None, str, str]:
    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=40)
            if response.status_code == 200:
                response.encoding = "utf-8"
                return response.status_code, response.text, ""
            last_error = f"HTTP {response.status_code}"
        except Exception as exc:  # noqa: BLE001 - preserve exact collection failure
            last_error = str(exc)
        time.sleep(0.8 * attempt)
    return None, "", last_error


def parse_categories(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    categories: list[dict[str, str]] = []
    for option in soup.find_all("option"):
        value = clean_text(option.get("value", ""))
        name = clean_text(option.get_text())
        if not value or value == "All" or not name or name == "全部专家":
            continue
        categories.append({"category_id": value, "category_name": name})
    return categories


def max_page_from_html(html: str) -> int:
    pages = [int(m.group(1)) for m in re.finditer(r"page=(\d+)", html)]
    return max(pages) if pages else 0


def parse_cards(html: str, category_id: str, category_name: str, page: int) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict[str, Any]] = []
    for li in soup.find_all("li"):
        classes = set(li.get("class") or [])
        if not {"md-col-span-6", "col-span-12"}.issubset(classes):
            continue
        anchor = li.find("a", href=re.compile(r"^/medical-service/department-expert/doctor/\d+$"))
        if not anchor:
            continue
        href = clean_text(anchor.get("href", ""))
        span = li.find("span", class_=lambda c: c and "text-xl" in c and "pr-4" in c)
        name = clean_text(span.get_text()) if span else ""
        card_department = ""
        if span and span.parent:
            parent_text = clean_text(span.parent.get_text(" ", strip=True))
            if parent_text.startswith(name):
                card_department = clean_text(parent_text[len(name) :])
            else:
                card_department = parent_text.replace(name, "", 1).strip()
        brief_div = li.find("div", class_=lambda c: c and "h-28" in str(c).split())
        list_brief = clean_text(brief_div.get_text(" ", strip=True)) if brief_div else ""
        rows.append(
            {
                "category_id": category_id,
                "category_name": category_name,
                "category_page": page,
                "name_from_list": name,
                "department_from_card": card_department,
                "list_brief": list_brief,
                "source_link": BASE + href,
            }
        )
    return rows


def parse_article_detail(html: str, fallback_name: str) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title_text = clean_text(soup.title.get_text()) if soup.title else ""
    title_name = title_text.split("|", 1)[0].strip() if "|" in title_text else ""
    article = soup.find("article")
    if not article:
        return {
            "name_from_detail": title_name or fallback_name,
            "identity_raw": "",
            "profile_text": "",
            "schedule_text": "",
            "language_text": "",
        }

    lines = [clean_text(line) for line in article.get_text("\n", strip=True).splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return {
            "name_from_detail": title_name or fallback_name,
            "identity_raw": "",
            "profile_text": "",
            "schedule_text": "",
            "language_text": "",
        }

    name = title_name or lines[0] or fallback_name
    start = 0
    for idx, line in enumerate(lines[:5]):
        if line == name:
            start = idx + 1
            break
    body_lines: list[str] = []
    schedule = ""
    language = ""
    for line in lines[start:]:
        if line.startswith("出诊时间"):
            schedule = line
            continue
        if line.startswith("工作语言"):
            language = line
            continue
        if line.startswith("扫一扫"):
            break
        body_lines.append(line)
    identity_raw = body_lines[0] if body_lines else ""
    body_lines = [line for line in body_lines if not re.fullmatch(r"\d+", line)]
    return {
        "name_from_detail": name,
        "identity_raw": identity_raw,
        "profile_text": "\n".join(body_lines),
        "schedule_text": schedule,
        "language_text": language,
    }


def extract_terms(text: str, terms: list[str]) -> list[str]:
    found: list[str] = []
    for term in terms:
        if term in text and term not in found:
            found.append(term)
    return found


def has_plain_doctor_identity(identity_raw: str, list_brief: str) -> bool:
    text = clean_text(identity_raw) or clean_text(list_brief)
    if not text:
        return False
    first_phrase = re.split(r"[，,。；;\s]", text, maxsplit=1)[0]
    return first_phrase == "医师"


def extract_sentences(text: str, terms: list[str], limit: int = 4, max_len: int = 420) -> str:
    parts = [clean_text(p) for p in re.split(r"(?<=[。！？；;])|\n", text) if clean_text(p)]
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


def collect_existing_profile_links() -> set[str]:
    links: set[str] = set()
    if not HOSPITAL_DIR.exists():
        return links
    for path in HOSPITAL_DIR.glob("*.md"):
        if path.name == "_索引.md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"来源链接:\s*(https?://\S+)", text):
            links.add(match.group(1).strip())
    return links


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0 Safari/537.36; public official-site collection"
            )
        }
    )

    status, entry_html, entry_error = fetch(session, ENTRY_URL)
    if status != 200:
        raise RuntimeError(f"入口页读取失败：{entry_error}")

    categories = parse_categories(entry_html)
    category_errors: list[dict[str, Any]] = []
    raw_rows: list[dict[str, Any]] = []

    for index, category in enumerate(categories, start=1):
        category_id = category["category_id"]
        category_name = category["category_name"]
        first_url = (
            f"{BASE}/medical-service/department-expert/doctor/category"
            f"?category_target_id={category_id}&combine="
        )
        first_status, first_html, first_error = fetch(session, first_url)
        if first_status != 200:
            category_errors.append(
                {
                    "category_id": category_id,
                    "category_name": category_name,
                    "page": 0,
                    "url": first_url,
                    "error": first_error,
                }
            )
            continue

        max_page = max_page_from_html(first_html)
        raw_rows.extend(parse_cards(first_html, category_id, category_name, 0))
        time.sleep(0.35)

        for page in range(1, max_page + 1):
            url = first_url + f"&page={page}"
            page_status, page_html, page_error = fetch(session, url)
            if page_status != 200:
                category_errors.append(
                    {
                        "category_id": category_id,
                        "category_name": category_name,
                        "page": page,
                        "url": url,
                        "error": page_error,
                    }
                )
                continue
            raw_rows.extend(parse_cards(page_html, category_id, category_name, page))
            time.sleep(0.35)

        print(f"[{index}/{len(categories)}] {category_name}: done")

    by_link: dict[str, dict[str, Any]] = {}
    for row in raw_rows:
        link = row["source_link"]
        item = by_link.setdefault(
            link,
            {
                "source_link": link,
                "name_from_list": row["name_from_list"],
                "departments_from_category": [],
                "departments_from_card": [],
                "category_ids": [],
                "category_pages": [],
                "list_brief": row["list_brief"],
            },
        )
        for field, source in [
            ("departments_from_category", row["category_name"]),
            ("departments_from_card", row["department_from_card"]),
            ("category_ids", row["category_id"]),
            ("category_pages", f"{row['category_name']}:page={row['category_page']}"),
        ]:
            if source and source not in item[field]:
                item[field].append(source)
        if len(row["list_brief"]) > len(item.get("list_brief", "")):
            item["list_brief"] = row["list_brief"]

    existing_links = collect_existing_profile_links()
    final_rows: list[dict[str, Any]] = []
    detail_errors: list[dict[str, str]] = []

    for idx, item in enumerate(sorted(by_link.values(), key=lambda x: x["source_link"]), start=1):
        link = item["source_link"]
        detail_status, detail_html, detail_error = fetch(session, link)
        detail = {
            "name_from_detail": "",
            "identity_raw": "",
            "profile_text": "",
            "schedule_text": "",
            "language_text": "",
        }
        if detail_status == 200:
            detail = parse_article_detail(detail_html, item["name_from_list"])
        else:
            detail_errors.append({"source_link": link, "error": detail_error})

        name = detail["name_from_detail"] or item["name_from_list"]
        department = "；".join(item["departments_from_category"])
        card_department = "；".join(item["departments_from_card"])
        combined_text = "\n".join(
            [
                department,
                card_department,
                item.get("list_brief", ""),
                detail.get("profile_text", ""),
            ]
        )
        title_hits = extract_terms(combined_text, TITLE_TERMS)
        if not title_hits and has_plain_doctor_identity(
            detail.get("identity_raw", ""), item.get("list_brief", "")
        ):
            title_hits = ["医师"]
        groups, tags = group_tags(combined_text)
        highlights = extract_sentences(combined_text, HIGHLIGHT_TERMS)
        specialty = extract_sentences(
            combined_text,
            [
                "擅长",
                "研究方向",
                "诊治",
                "治疗",
                "诊断",
                "手术",
                "放疗",
                "介入",
                "内镜",
                "主攻",
                "专长",
            ],
            limit=4,
            max_len=520,
        )

        warnings: list[str] = []
        if detail_status != 200:
            warnings.append("详情页读取失败")
        if not detail.get("profile_text"):
            warnings.append("详情页正文为空或未识别")
        if not title_hits:
            warnings.append("职称/身份需人工复核")
        if len(item["departments_from_category"]) > 1:
            warnings.append("多分类归属，科室需复核")

        priority = "普通"
        if any(term in combined_text for term in PRIORITY_DEPARTMENTS) or groups:
            priority = "高"
        elif any(term != "医师" for term in title_hits):
            priority = "中"

        final_rows.append(
            {
                "序号": idx,
                "医院": HOSPITAL,
                "姓名": name,
                "科室_分类页": department,
                "科室_列表卡片": card_department,
                "职称_关键词": "、".join(title_hits),
                "职称身份原文": clip(detail.get("identity_raw", "") or item.get("list_brief", ""), 500),
                "重点优先级": priority,
                "重点关注范围": "、".join(groups),
                "重点疾病标签": "、".join(tags),
                "擅长诊疗方向摘录": specialty,
                "亮眼经历线索": highlights,
                "列表简介": clip(item.get("list_brief", ""), 700),
                "详情正文摘录": clip(detail.get("profile_text", ""), 1800),
                "来源类型": "医院官网",
                "来源链接": link,
                "采集入口": ENTRY_URL,
                "采集方式": "官网分类页+官网医生详情页",
                "采集日期": TODAY,
                "详情页状态": "200" if detail_status == 200 else "失败",
                "已建画像": "是" if link in existing_links else "否",
                "异常提示": "；".join(warnings),
                "复核状态": "待人工复核",
            }
        )
        if idx % 30 == 0:
            print(f"details: {idx}/{len(by_link)}")
        time.sleep(0.28)

    final_rows.sort(key=lambda row: (row["重点优先级"] != "高", row["科室_分类页"], row["姓名"]))
    for new_index, row in enumerate(final_rows, start=1):
        row["序号"] = new_index

    headers = [
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
    with CSV_OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(final_rows)

    category_counter = Counter()
    priority_counter = Counter(row["重点优先级"] for row in final_rows)
    group_counter = Counter()
    warning_counter = Counter()
    for row in final_rows:
        for dept in row["科室_分类页"].split("；"):
            if dept:
                category_counter[dept] += 1
        for group in row["重点关注范围"].split("、"):
            if group:
                group_counter[group] += 1
        for warning in row["异常提示"].split("；"):
            if warning:
                warning_counter[warning] += 1

    payload = {
        "meta": {
            "hospital": HOSPITAL,
            "entry_url": ENTRY_URL,
            "collected_at": TODAY,
            "category_count": len(categories),
            "raw_card_rows": len(raw_rows),
            "unique_doctor_count": len(final_rows),
            "category_error_count": len(category_errors),
            "detail_error_count": len(detail_errors),
            "existing_profile_count": sum(1 for row in final_rows if row["已建画像"] == "是"),
        },
        "categories": categories,
        "category_errors": category_errors,
        "detail_errors": detail_errors,
        "category_counts": category_counter.most_common(),
        "priority_counts": dict(priority_counter),
        "group_counts": dict(group_counter),
        "warning_counts": dict(warning_counter),
        "rows": final_rows,
    }
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    top_departments = "\n".join(
        f"| {dept} | {count} |" for dept, count in category_counter.most_common(20)
    )
    group_lines = "\n".join(
        f"| {group} | {count} |" for group, count in sorted(group_counter.items())
    )
    warning_lines = "\n".join(
        f"| {warning} | {count} |" for warning, count in warning_counter.most_common()
    )
    category_error_lines = "\n".join(
        f"| {err['category_name']} | page={err['page']} | {err['error']} |"
        for err in category_errors
    )
    if not category_error_lines:
        category_error_lines = "| 无 | 无 | 无 |"
    if not warning_lines:
        warning_lines = "| 无 | 0 |"

    report = f"""---
类型: 自动采集试跑报告
医院: {HOSPITAL}
采集日期: {TODAY}
来源范围: 医院官网
采集入口: {ENTRY_URL}
---

# {HOSPITAL} 全院医生自动采集试跑报告

## 结论

本次试跑已从医院官网公开分类页批量读取医生列表，并进一步读取官网医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成全院医生自动采集底表，共 {len(final_rows)} 位唯一医生；官网分类页原始卡片记录 {len(raw_rows)} 条；识别到官网分类 {len(categories)} 个；已匹配到前期人工建立画像 {payload['meta']['existing_profile_count']} 条。

## 输出文件

- Excel 底表：`{XLSX_OUT}`
- CSV 底表：`{CSV_OUT}`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 官网分类数 | {len(categories)} |
| 原始医生卡片记录 | {len(raw_rows)} |
| 唯一医生详情页 | {len(final_rows)} |
| 分类页失败数 | {len(category_errors)} |
| 详情页失败数 | {len(detail_errors)} |
| 已建画像匹配数 | {payload['meta']['existing_profile_count']} |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
{group_lines}

## 科室/分类数量 Top 20

| 科室/分类 | 医生数 |
|---|---:|
{top_departments}

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
{warning_lines}

## 分类页读取异常

| 分类 | 页码 | 错误 |
|---|---|---|
{category_error_lines}

## 管理员复核重点

1. 优先筛选“重点优先级=高”的医生。
2. 优先处理“异常提示”不为空的行；“医师”按普通医生处理，不单独列为职称异常。
3. “亮眼经历线索”只是自动摘取的证据线索，不能直接当成最终宣传语。
4. 官网简介不足时，不补造擅长、疾病标签或亮眼经历，无法填写的画像字段保持空白。
5. “免疫”如果出现在“肿瘤免疫治疗”语境中，不能直接归为免疫功能低下医生，需要人工复核。
6. 复核无误后，再批量生成正式 Obsidian 医生画像。

## 合规边界

- 仅使用医院官网公开网页。
- 不采集私人电话、私人微信、家庭住址、患者隐私或非公开排班信息。
- 不使用第三方医疗平台评价、排名、患者评论。
- 不写“保证治愈”“包治疑难杂症”“疗效第一”等无法由官网证明的表达。
"""
    REPORT_OUT.write_text(report, encoding="utf-8")

    print(json.dumps(payload["meta"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
