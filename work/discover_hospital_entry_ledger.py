from __future__ import annotations

import csv
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date
from html import unescape
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(r"D:\workspace\信息收集整理")
SOURCE_XLSX = ROOT / "珠三角三甲医院_三甲候选清单_清洗版.xlsx"
SOURCE_SHEET = "三甲候选清单"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
WORK_DIR = ROOT / "work"

JSON_OUT = WORK_DIR / "pearl_delta_hospital_entry_ledger.json"
CSV_OUT = SOURCE_DIR / "珠三角三甲医院官网入口台账.csv"
REPORT_OUT = SOURCE_DIR / "珠三角三甲医院官网入口台账_自动检索报告.md"

TODAY = date.today().isoformat()

CITY_ORDER = [
    "广州市",
    "深圳市",
    "佛山市",
    "东莞市",
    "珠海市",
    "惠州市",
    "中山市",
    "江门市",
    "肇庆市",
]

BAD_DOMAIN_PARTS = [
    "baidu.",
    "bing.",
    "sogou.",
    "so.com",
    "360.cn",
    "qq.com",
    "sina.",
    "sohu.",
    "163.com",
    "toutiao.",
    "zhihu.",
    "weibo.",
    "amap.",
    "map.",
    "haodf.",
    "39.net",
    "bohe.",
    "ynzmk.cn",
    "companyhomepages.",
    "yyszq.",
    "gov.tag.org.cn",
    "dayi.org.cn",
    "chealth.org.cn",
    "grimterra.",
    "fh21.com.cn",
    "hospital.51daifu.",
    "ask.51daifu.",
    "kanghuwang.",
    "guanwangquanji.",
    "miaoshou.",
    "91160.",
    "99.com.cn",
    "cnkang.",
    "mingyihui.",
    "guanwangdaquan.",
    "114gh.",
    "wetrial.",
    "yihu.",
    "guahao.",
    "familydoctor.",
    "120ask.",
    "youlai.",
    "xywy.",
    "cn-healthcare.",
    "qcc.",
    "tianyancha.",
    "maigoo.",
    "findzd.",
    "mvyxws.",
    "a-hospital.",
    "hospital.ucas.",
    "wed114.",
    "fwol.",
    "daoyi.",
    "kangxun.",
    "docin.",
    "dxy.",
    "baike.",
    "wikipedia.",
    "qyiliao.",
    "hao120.",
    "120.net",
    "jianke.",
    "city8.",
    "zhuangshengsheng.",
    "gdsyy.org",
    "csp.ncmi.cn",
    "gdyuchen.",
]

BAD_TITLE_PARTS = [
    "预约挂号",
    "官网大全",
    "官网全集",
    "官网是什么",
    "医院库",
    "复禾",
    "医生在线",
    "康护网",
    "妙手医生",
    "导医",
    "中国医药信息查询平台",
    "全国各地医院",
    "推荐专家",
    "门诊时间表",
    "挂号",
]

WEAK_SOURCE_DOMAIN_PARTS = [
    "gov.cn",
    "gdyf.org.cn",
    "gzdaily.",
    "southcn.",
]

OFFICIAL_WORDS = ["官网", "官方网站", "医院官网", "首页"]
DOCTOR_WORDS = [
    "医生",
    "医师",
    "专家",
    "科室专家",
    "专家介绍",
    "专家团队",
    "医生团队",
    "医疗团队",
    "名医",
    "出诊",
    "门诊安排",
    "科室导航",
    "科室介绍",
    "临床科室",
]
DOCTOR_PATH_WORDS = [
    "doctor",
    "expert",
    "specialist",
    "department",
    "dept",
    "medical",
    "zhuanjia",
    "kesh",
    "ks",
]
NOISE_WORDS = ["招聘", "招标", "公告", "新闻", "采购", "党建", "收费", "路线", "地址"]

HEADERS = [
    "序号",
    "推进批次",
    "城市",
    "区县",
    "医院名称",
    "医院别名",
    "医院等级",
    "医院类型",
    "官网首页_候选",
    "官网标题_自动识别",
    "医生目录入口_候选",
    "入口类型_自动判断",
    "是否可按科室_初判",
    "是否可全院采集_初判",
    "采集难度_初判",
    "官方确认状态",
    "自动置信度",
    "检索关键词",
    "搜索依据链接",
    "排除或注意事项",
    "下一步动作",
    "人工复核结果",
    "人工备注",
    "更新时间",
]


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    return str(value).strip()


def strip_tags(value: str) -> str:
    value = re.sub(r"<script.*?</script>", "", value, flags=re.I | re.S)
    value = re.sub(r"<style.*?</style>", "", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", "", value)
    value = unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def clean_search_name(name: str) -> str:
    cleaned = re.sub(r"[（(].*?[)）]", "", name).strip()
    if len(cleaned) >= 6:
        return cleaned
    return name


def name_variants(name: str, alias: str) -> list[str]:
    items = [name, clean_search_name(name)]
    if alias:
        for part in re.split(r"[,，/、;；\s]+", alias):
            part = part.strip()
            if part:
                items.append(part)
    deduped: list[str] = []
    for item in items:
        if item and item not in deduped:
            deduped.append(item)
    return deduped


def canonical_host(url: str) -> str:
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except ValueError:
        return ""
    return host.lower().removeprefix("www.")


def domain_is_bad(host: str) -> bool:
    if not host:
        return True
    return any(part in host for part in BAD_DOMAIN_PARTS)


def domain_is_weak_source(host: str) -> bool:
    return any(part in host for part in WEAK_SOURCE_DOMAIN_PARTS)


def resolve_search_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if "duckduckgo.com" in (parsed.hostname or "") and parsed.path.startswith("/l/"):
        query = urllib.parse.parse_qs(parsed.query)
        raw = query.get("uddg", [""])[0]
        return urllib.parse.unquote(raw) if raw else url
    if "bing.com" not in (parsed.hostname or ""):
        return url
    query = urllib.parse.parse_qs(parsed.query)
    raw = query.get("u", [""])[0]
    if raw.startswith("a1"):
        raw = raw[2:]
    if raw:
        padded = raw + "=" * (-len(raw) % 4)
        try:
            import base64

            return base64.urlsafe_b64decode(padded).decode("utf-8", "ignore")
        except Exception:
            return url
    return url


def duckduckgo_search(query: str, max_results: int = 8) -> list[dict[str, str]]:
    url = "https://duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    try:
        status, final_url, html = fetch(url, timeout=15, limit=900_000)
    except Exception as exc:
        return [
            {
                "title": "",
                "url": "",
                "snippet": f"搜索失败：{type(exc).__name__}",
                "source": url,
            }
        ]
    if status != 200:
        return [{"title": "", "url": "", "snippet": f"搜索状态码：{status}", "source": final_url}]

    results: list[dict[str, str]] = []
    link_pattern = re.compile(
        r'<a[^>]+class=["\']result__a["\'][^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        flags=re.I | re.S,
    )
    matches = list(link_pattern.finditer(html))
    for index, match in enumerate(matches):
        href = resolve_search_url(unescape(match.group(1)))
        title = strip_tags(match.group(2))
        block_end = matches[index + 1].start() if index + 1 < len(matches) else min(len(html), match.end() + 5000)
        block = html[match.end() : block_end]
        snippet_match = re.search(
            r'class=["\']result__snippet["\'][^>]*>(.*?)</a>',
            block,
            flags=re.I | re.S,
        )
        snippet = strip_tags(snippet_match.group(1)) if snippet_match else ""
        if href and title:
            results.append(
                {
                    "title": title,
                    "url": href,
                    "snippet": snippet,
                    "source": final_url,
                }
            )
        if len(results) >= max_results:
            break
    return results


def fetch(url: str, timeout: int = 12, limit: int = 500_000) -> tuple[int, str, str]:
    context = ssl.create_default_context()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.5",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
        data = resp.read(limit)
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.status, resp.geturl(), data.decode(charset, "ignore")


def bing_search(query: str, max_results: int = 8) -> list[dict[str, str]]:
    duck_results = duckduckgo_search(query, max_results=max_results)
    if any(item.get("url") for item in duck_results):
        return duck_results

    url = "https://www.bing.com/search?q=" + urllib.parse.quote(query) + "&cc=cn&setlang=zh-cn"
    try:
        status, final_url, html = fetch(url, timeout=15, limit=900_000)
    except Exception as exc:
        return [
            {
                "title": "",
                "url": "",
                "snippet": f"搜索失败：{type(exc).__name__}",
                "source": url,
            }
        ]
    if status != 200:
        return [{"title": "", "url": "", "snippet": f"搜索状态码：{status}", "source": final_url}]

    blocks = re.findall(r'<li class="b_algo".*?</li>', html, flags=re.I | re.S)
    results: list[dict[str, str]] = []
    for block in blocks:
        link = re.search(r'<h2.*?<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block, flags=re.I | re.S)
        if not link:
            continue
        href = resolve_search_url(unescape(link.group(1)))
        title = strip_tags(link.group(2))
        snippet_match = re.search(r"<p[^>]*>(.*?)</p>", block, flags=re.I | re.S)
        snippet = strip_tags(snippet_match.group(1)) if snippet_match else ""
        if href and title:
            results.append(
                {
                    "title": title,
                    "url": href,
                    "snippet": snippet,
                    "source": final_url,
                }
            )
        if len(results) >= max_results:
            break
    return results


def score_result(result: dict[str, str], variants: list[str], prefer_home: bool) -> int:
    url = result["url"]
    host = canonical_host(url)
    if domain_is_bad(host):
        return -999
    score = 0
    haystack = f"{result['title']} {result['snippet']} {url}".lower()
    if any(word.lower() in haystack for word in BAD_TITLE_PARTS):
        return -999
    has_name_match = False
    for item in variants:
        if item and item in haystack:
            has_name_match = True
            score += 36
            break
    for item in variants:
        short = item.replace("医院", "").replace("中心", "")
        if len(short) >= 4 and short in haystack:
            has_name_match = True
            score += 16
            break
    if not has_name_match:
        return -999
    if "医院" in haystack:
        score += 10
    if any(word in haystack for word in OFFICIAL_WORDS):
        score += 16
    if domain_is_weak_source(host):
        score -= 18
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip("/")
    if prefer_home and len(path) <= 8:
        score += 10
    if not prefer_home and has_doctor_signal(result):
        score += 30
    if any(word in haystack for word in NOISE_WORDS):
        score -= 12
    return score


def has_doctor_signal(result: dict[str, str]) -> bool:
    value = f"{result.get('title', '')} {result.get('snippet', '')} {result.get('url', '')}".lower()
    return any(word in value for word in DOCTOR_WORDS) or any(word in value for word in DOCTOR_PATH_WORDS)


def has_doctor_entry_signal(result: dict[str, str]) -> bool:
    value = f"{result.get('title', '')} {result.get('url', '')}".lower()
    return any(word in value for word in DOCTOR_WORDS) or any(word in value for word in DOCTOR_PATH_WORDS)


def result_url_is_same_site(url: str, home_url: str) -> bool:
    host = canonical_host(url)
    home_host = canonical_host(home_url)
    if not host or not home_host:
        return False
    return host == home_host or host.endswith("." + home_host) or home_host.endswith("." + host)


def extract_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    return strip_tags(match.group(1)) if match else ""


def absolute_url(base: str, href: str) -> str:
    href = unescape(href).strip()
    if not href or href.startswith(("javascript:", "#", "mailto:", "tel:")):
        return ""
    return urllib.parse.urljoin(base, href)


def classify_entry_type(label: str, url: str) -> str:
    value = f"{label} {url}".lower()
    if "医生" in value or "doctor" in value:
        return "医生目录"
    if "专家" in value or "expert" in value or "zhuanjia" in value:
        return "专家介绍"
    if "出诊" in value or "门诊安排" in value:
        return "出诊信息"
    if "科室" in value or "department" in value or "dept" in value:
        return "科室导航"
    if "名医" in value:
        return "名医团队"
    return "疑似医生入口"


def score_anchor(label: str, url: str) -> int:
    value = f"{label} {url}".lower()
    score = 0
    for word in ["医生", "doctor"]:
        if word in value:
            score += 36
    for word in ["专家", "expert", "zhuanjia"]:
        if word in value:
            score += 30
    for word in ["医疗团队", "医生团队", "专家团队", "名医"]:
        if word in value:
            score += 26
    for word in ["科室专家", "科室介绍", "科室导航", "临床科室", "department", "dept"]:
        if word in value:
            score += 18
    for word in ["出诊", "门诊安排"]:
        if word in value:
            score += 12
    if any(word in value for word in NOISE_WORDS):
        score -= 18
    return score


def find_entry_from_home(home_url: str) -> tuple[str, str, str]:
    try:
        _status, final_url, html = fetch(home_url, timeout=12, limit=700_000)
    except Exception:
        return "", "", ""
    candidates: list[tuple[int, str, str]] = []
    for match in re.finditer(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", html, flags=re.I | re.S):
        href = absolute_url(final_url, match.group(1))
        label = strip_tags(match.group(2))
        if not href:
            continue
        if href.rstrip("/") == final_url.rstrip("/"):
            continue
        if canonical_host(href) and domain_is_bad(canonical_host(href)):
            continue
        score = score_anchor(label, href)
        if score > 0:
            candidates.append((score, label, href))
    candidates.sort(key=lambda item: item[0], reverse=True)
    for _score, label, href in candidates[:12]:
        if result_url_is_same_site(href, home_url) or not canonical_host(home_url):
            return href, classify_entry_type(label, href), label
    return "", "", ""


def choose_home(results: list[dict[str, str]], variants: list[str]) -> tuple[dict[str, str] | None, int]:
    candidates: list[tuple[int, dict[str, str]]] = []
    for result in results:
        if not result["url"]:
            continue
        score = score_result(result, variants, prefer_home=True)
        if score >= 25:
            candidates.append((score, result))
    candidates.sort(key=lambda item: item[0], reverse=True)
    return (candidates[0][1], candidates[0][0]) if candidates else (None, 0)


def choose_doctor(
    results: list[dict[str, str]],
    variants: list[str],
    home_url: str,
) -> tuple[dict[str, str] | None, int]:
    if not home_url:
        return None, 0
    candidates: list[tuple[int, dict[str, str]]] = []
    for result in results:
        if not result["url"] or not has_doctor_entry_signal(result):
            continue
        if home_url and not result_url_is_same_site(result["url"], home_url):
            continue
        score = score_result(result, variants, prefer_home=False)
        if score >= 30:
            candidates.append((score, result))
    candidates.sort(key=lambda item: item[0], reverse=True)
    return (candidates[0][1], candidates[0][0]) if candidates else (None, 0)


def difficulty(entry_type: str, home: str, doctor_entry: str) -> str:
    if doctor_entry and entry_type in {"医生目录", "专家介绍", "名医团队", "疑似医生入口"}:
        return "A-优先自动采集"
    if doctor_entry and entry_type in {"科室导航", "出诊信息"}:
        return "B-半自动采集"
    if home:
        return "C-仅官网待找入口"
    return "D-待人工补官网"


def confidence(home_score: int, doctor_score: int, title: str, variants: list[str]) -> str:
    title_hit = any(item and item in title for item in variants)
    if home_score >= 70 and (doctor_score >= 45 or title_hit):
        return "高"
    if home_score >= 45:
        return "中"
    if home_score > 0:
        return "低"
    return "未找到"


def next_action(row: dict[str, str]) -> str:
    if row["官方确认状态"] == "已试点确认":
        return "可进入正式采集"
    if row["官网首页_候选"] and row["医生目录入口_候选"]:
        return "人工打开医生入口，确认是否覆盖全院"
    if row["官网首页_候选"]:
        return "人工打开官网首页，查找专家/医生/科室入口"
    return "人工补充官网首页"


def write_csv(rows: list[dict[str, str]]) -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def build_report(rows: list[dict[str, str]], city_summary: list[dict[str, Any]]) -> str:
    status_counts = Counter(row["官方确认状态"] for row in rows)
    confidence_counts = Counter(row["自动置信度"] for row in rows)
    difficulty_counts = Counter(row["采集难度_初判"] for row in rows)
    lines = [
        "# 珠三角三甲医院官网入口台账自动检索报告",
        "",
        f"- 生成日期：{TODAY}",
        f"- 候选医院数：{len(rows)}",
        f"- 城市数：{len(city_summary)}",
        f"- 官网候选已找到：{sum(1 for row in rows if row['官网首页_候选'])}",
        f"- 医生入口候选已找到：{sum(1 for row in rows if row['医生目录入口_候选'])}",
        "",
        "## 状态统计",
        "",
    ]
    for key, value in status_counts.most_common():
        lines.append(f"- {key}：{value}")
    lines.extend(["", "## 自动置信度", ""])
    for key, value in confidence_counts.most_common():
        lines.append(f"- {key}：{value}")
    lines.extend(["", "## 采集难度初判", ""])
    for key, value in difficulty_counts.most_common():
        lines.append(f"- {key}：{value}")
    lines.extend(["", "## 城市汇总", ""])
    lines.append("| 城市 | 医院数 | 官网候选 | 医生入口候选 | A级 | B级 | C级 | D级 |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for item in city_summary:
        lines.append(
            "| {城市} | {医院数} | {官网候选数} | {医生入口候选数} | {A级} | {B级} | {C级} | {D级} |".format(
                **item
            )
        )
    lines.extend(
        [
            "",
            "## 使用边界",
            "",
            "- 本台账仅使用公开搜索结果和医院官网候选链接做入口发现。",
            "- 自动结果均需人工打开复核后，才进入医生数据采集。",
            "- 不使用第三方医疗平台医生资料，不采集私人联系方式、患者隐私或非公开接口。",
            "- 对院区、门诊部、历史军队医院名称等条目，需重点确认是否有独立官网及独立医生目录。",
        ]
    )
    return "\n".join(lines) + "\n"


def summarize_by_city(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for city in CITY_ORDER:
        city_rows = [row for row in rows if row["城市"] == city]
        if not city_rows:
            continue
        summary.append(
            {
                "城市": city,
                "医院数": len(city_rows),
                "官网候选数": sum(1 for row in city_rows if row["官网首页_候选"]),
                "医生入口候选数": sum(1 for row in city_rows if row["医生目录入口_候选"]),
                "A级": sum(1 for row in city_rows if row["采集难度_初判"].startswith("A-")),
                "B级": sum(1 for row in city_rows if row["采集难度_初判"].startswith("B-")),
                "C级": sum(1 for row in city_rows if row["采集难度_初判"].startswith("C-")),
                "D级": sum(1 for row in city_rows if row["采集难度_初判"].startswith("D-")),
            }
        )
    return summary


def discover_one(record: dict[str, str], seq: int) -> dict[str, str]:
    city = text(record.get("市"))
    name = text(record.get("医院名称"))
    alias = text(record.get("医院别名"))
    variants = name_variants(name, alias)
    search_name = clean_search_name(name)
    query = f"{search_name} 官方网站 官网"

    if name == "中山大学附属第五医院":
        row = {
            "序号": str(seq),
            "推进批次": str(CITY_ORDER.index(city) + 1 if city in CITY_ORDER else 99),
            "城市": city,
            "区县": text(record.get("区县")),
            "医院名称": name,
            "医院别名": alias,
            "医院等级": text(record.get("医院等级")),
            "医院类型": text(record.get("医院类型")),
            "官网首页_候选": "https://www.sysu5.cn/",
            "官网标题_自动识别": "中山大学附属第五医院",
            "医生目录入口_候选": (
                "https://www.sysu5.cn/medical-service/department-expert/doctor/"
                "category?category_target_id=All&combine="
            ),
            "入口类型_自动判断": "医生目录",
            "是否可按科室_初判": "是",
            "是否可全院采集_初判": "是",
            "采集难度_初判": "A-优先自动采集",
            "官方确认状态": "已试点确认",
            "自动置信度": "高",
            "检索关键词": query,
            "搜索依据链接": "https://www.sysu5.cn/",
            "排除或注意事项": "已完成试点采集和Obsidian画像生成",
            "下一步动作": "可作为流程样板",
            "人工复核结果": "",
            "人工备注": "",
            "更新时间": TODAY,
        }
        return row

    results = bing_search(query, max_results=20)
    time.sleep(0.25)

    home_result, home_score = choose_home(results, variants)
    if not home_result:
        fallback_query = f"{search_name} 官网 医生 专家 科室"
        results = bing_search(fallback_query, max_results=20)
        time.sleep(0.25)
        home_result, home_score = choose_home(results, variants)
        query = f"{query} / {fallback_query}"
    home_url = home_result["url"] if home_result else ""
    source_url = home_result["source"] if home_result else (results[0].get("source", "") if results else "")
    home_title = home_result["title"] if home_result else ""

    if home_url:
        try:
            _status, final_home, home_html = fetch(home_url, timeout=10, limit=400_000)
            home_url = final_home
            fetched_title = extract_title(home_html)
            if fetched_title:
                home_title = fetched_title
        except Exception:
            pass

    doctor_result, doctor_score = choose_doctor(results, variants, home_url)
    doctor_url = doctor_result["url"] if doctor_result else ""
    entry_type = classify_entry_type(doctor_result["title"], doctor_url) if doctor_result else ""
    anchor_label = ""

    if home_url and not doctor_url:
        doctor_url, entry_type, anchor_label = find_entry_from_home(home_url)

    if home_url and not doctor_url:
        host = canonical_host(home_url)
        if host:
            site_query = f"site:{host} {search_name} 医生 专家 科室"
            site_results = bing_search(site_query, max_results=8)
            time.sleep(0.25)
            site_doctor, site_score = choose_doctor(site_results, variants, home_url)
            if site_doctor:
                doctor_url = site_doctor["url"]
                doctor_score = max(doctor_score, site_score)
                entry_type = classify_entry_type(site_doctor["title"], doctor_url)
                source_url = site_doctor["source"] or source_url

    if doctor_url and not entry_type:
        entry_type = "疑似医生入口"

    conf = confidence(home_score, doctor_score, home_title, variants)
    diff = difficulty(entry_type, home_url, doctor_url)
    if home_url and doctor_url:
        status = "自动候选-待人工复核"
    elif home_url:
        status = "已找到官网-待补医生入口"
    else:
        status = "未找到-待人工补充"

    note_parts = []
    if anchor_label:
        note_parts.append(f"入口锚文本：{anchor_label}")
    if domain_is_weak_source(canonical_host(home_url)):
        note_parts.append("官网候选可能来自政府/行业信息页，需重点核验")
    if any(word in name for word in ["院区", "门诊部", "分院"]):
        note_parts.append("院区/分院条目需确认是否独立采集")

    row = {
        "序号": str(seq),
        "推进批次": str(CITY_ORDER.index(city) + 1 if city in CITY_ORDER else 99),
        "城市": city,
        "区县": text(record.get("区县")),
        "医院名称": name,
        "医院别名": alias,
        "医院等级": text(record.get("医院等级")),
        "医院类型": text(record.get("医院类型")),
        "官网首页_候选": home_url,
        "官网标题_自动识别": home_title,
        "医生目录入口_候选": doctor_url,
        "入口类型_自动判断": entry_type,
        "是否可按科室_初判": "是" if entry_type in {"科室导航", "科室介绍"} or "科室" in entry_type else ("可能" if doctor_url else ""),
        "是否可全院采集_初判": "待确认" if doctor_url else "",
        "采集难度_初判": diff,
        "官方确认状态": status,
        "自动置信度": conf,
        "检索关键词": query,
        "搜索依据链接": source_url,
        "排除或注意事项": "；".join(note_parts),
        "下一步动作": "",
        "人工复核结果": "",
        "人工备注": "",
        "更新时间": TODAY,
    }
    row["下一步动作"] = next_action(row)
    return row


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(SOURCE_XLSX, sheet_name=SOURCE_SHEET, dtype=str)
    df = df[df["市"].isin(CITY_ORDER)].copy()
    df["城市排序"] = df["市"].map({city: index for index, city in enumerate(CITY_ORDER)})
    df["医院名称排序"] = df["医院名称"].map(lambda value: text(value))
    df = df.sort_values(["城市排序", "医院名称排序"], kind="stable")

    rows: list[dict[str, str]] = []
    for index, record in enumerate(df.to_dict(orient="records"), start=1):
        name = text(record.get("医院名称"))
        city = text(record.get("市"))
        print(f"[{index}/{len(df)}] {city} {name}", flush=True)
        try:
            row = discover_one(record, index)
        except urllib.error.URLError as exc:
            row = {
                header: ""
                for header in HEADERS
            }
            row.update(
                {
                    "序号": str(index),
                    "推进批次": str(CITY_ORDER.index(city) + 1 if city in CITY_ORDER else 99),
                    "城市": city,
                    "区县": text(record.get("区县")),
                    "医院名称": name,
                    "医院别名": text(record.get("医院别名")),
                    "医院等级": text(record.get("医院等级")),
                    "医院类型": text(record.get("医院类型")),
                    "官方确认状态": "未找到-待人工补充",
                    "自动置信度": "未找到",
                    "检索关键词": f"{clean_search_name(name)} 官网 医生 专家 科室",
                    "排除或注意事项": f"检索异常：{type(exc).__name__}",
                    "下一步动作": "人工补充官网首页",
                    "更新时间": TODAY,
                }
            )
        rows.append(row)

    city_summary = summarize_by_city(rows)
    payload = {
        "generated_at": TODAY,
        "source_xlsx": str(SOURCE_XLSX),
        "source_sheet": SOURCE_SHEET,
        "headers": HEADERS,
        "rows": rows,
        "city_summary": city_summary,
        "field_notes": [
            {"字段": "官网首页_候选", "说明": "自动检索得到的疑似医院官网首页，未人工复核前不得视为最终确认。"},
            {"字段": "医生目录入口_候选", "说明": "自动检索得到的疑似医生、专家或科室入口，需人工确认覆盖范围。"},
            {"字段": "采集难度_初判", "说明": "A=优先自动采集，B=半自动，C=仅找到官网，D=待人工补官网。"},
            {"字段": "官方确认状态", "说明": "自动结果默认待人工复核；已试点确认仅适用于中山大学附属第五医院。"},
        ],
    }
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(rows)
    REPORT_OUT.write_text(build_report(rows, city_summary), encoding="utf-8")
    print(f"JSON: {JSON_OUT}")
    print(f"CSV: {CSV_OUT}")
    print(f"REPORT: {REPORT_OUT}")


if __name__ == "__main__":
    main()
