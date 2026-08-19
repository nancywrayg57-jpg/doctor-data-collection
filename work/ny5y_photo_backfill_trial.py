from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import re
import time
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from http.client import IncompleteRead
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, unquote, urljoin, urlparse
from urllib.request import ProxyHandler, Request, build_opener

from PIL import Image, ImageDraw, ImageFont, ImageOps

import zssy_photo_backfill_trial as base


ROOT = Path(r"D:\workspace\信息收集整理")
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "南方医科大学第五附属医院"
ISSUE_NUMBER = 79
EXPECTED_SCOPE_COUNT = 134
EXPECTED_TRIAL_COUNT = 10
MIN_TRIAL_DEPARTMENTS = 5
OFFICIAL_HOME = "http://www.ny5y.cn/"
DIRECTORY_URL = "http://www.ny5y.cn/zhuanjia_mingyi.php?id=100"
SECONDARY_DIRECTORY_URL = "http://www.ny5y.cn/zhuanjia_lingnan.php?id=162"
OFFICIAL_HOST = "ny5y.cn"
PHOTO_PREFIX = "/ueditor/php/upload/image/"
PROFILE_DIR = VAULT / "01_试点医院" / HOSPITAL
FORMAL_PHOTO_DIR = PROFILE_DIR / "照片"
TRIAL_BASENAME = f"{HOSPITAL}_photo_backfill_trial"
TRIAL_JSON_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
TRIAL_CSV_PATH = WORK_DIR / f"{TRIAL_BASENAME}_manifest.csv"
TRIAL_REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
TRIAL_PHOTO_DIR = WORK_DIR / f"{TRIAL_BASENAME}_photos"
EXPECTED_TITLE_COUNTS = {"正高": 3, "副高": 4, "中级": 3, "初级": 0}
SAMPLE_PLAN = (
    ("黄艺洪", "正高"),
    ("司昌荣", "正高"),
    ("安得辉", "中级"),
    ("周姗", "副高"),
    ("郭丽冬", "副高"),
    ("王波涛", "副高"),
    ("沈玉才", "正高"),
    ("吴智勇", "中级"),
    ("许桂璇", "中级"),
    ("杨柳", "副高"),
)
EXCLUDED_RESOURCE_EXAMPLES = (
    "images/logo.jpg",
    "images/gzwm.jpg",
    "images/float1.png ... images/float5.png",
    "dcs.conac.cn government badge",
    "正文 ueditor 叙事配图（非 yisheng_xq_bug_left 容器）",
)
PLACEHOLDER_QUERY_MARKERS = ("blank", "placeholder", "default")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
REACHABILITY_RETRY_INTERVAL_SECONDS = 30
STRUCTURE_EVIDENCE: dict[str, dict[str, Any]] = {}


def clean_text(value: Any) -> str:
    return base.clean_text(value)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def comparable_host(value: str) -> str:
    host = (urlparse(value).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def detail_id(value: Any) -> str:
    parsed = urlparse(clean_text(value))
    if (
        parsed.scheme not in {"http", "https"}
        or comparable_host(parsed.geturl()) != OFFICIAL_HOST
        or parsed.path != "/yisheng_xq.php"
        or parsed.fragment
    ):
        return ""
    query = parse_qsl(parsed.query, keep_blank_values=True)
    if len(query) != 1 or query[0][0] != "id" or not re.fullmatch(r"[1-9]\d*", query[0][1]):
        return ""
    return query[0][1]


def decoded_query_values(value: str) -> list[str]:
    parsed = urlparse(value)
    decoded: list[str] = []
    for name, item in parse_qsl(parsed.query, keep_blank_values=True):
        for candidate in (name, item):
            raw = unquote(candidate).strip()
            if not raw or not re.fullmatch(r"[A-Za-z0-9_\-+/=]+", raw):
                continue
            padded = raw + "=" * (-len(raw) % 4)
            try:
                content = base64.b64decode(padded, altchars=b"-_", validate=True)
                text = content.decode("utf-8")
            except (ValueError, UnicodeDecodeError):
                continue
            if text and text not in decoded:
                decoded.append(text)
    return decoded


def suspicious_query_decoding(value: str) -> str:
    for decoded in decoded_query_values(value):
        lowered = decoded.casefold()
        if any(marker in lowered for marker in PLACEHOLDER_QUERY_MARKERS):
            return decoded
    return ""


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
    lowered = unquote(parsed.path).casefold()
    if any(marker in lowered for marker in base.PLACEHOLDER_MARKERS):
        return ""
    if suspicious_query_decoding(absolute):
        return ""
    return absolute


class Ny5yPhysicianPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.portrait_attrs: list[dict[str, str]] = []
        self.portrait_snippets: list[str] = []
        self.names: list[str] = []
        self._name_div_depth = 0
        self._name_span_depth = 0
        self._name_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {name: str(value or "") for name, value in attrs}
        if self._name_div_depth:
            if tag.lower() == "div":
                self._name_div_depth += 1
            elif tag.lower() == "span":
                self._name_span_depth += 1
        if tag.lower() != "div":
            return
        classes = set(clean_text(attrs_dict.get("class")).split())
        if "yisheng_xq_bug_left" in classes:
            self.portrait_attrs.append(attrs_dict)
            self.portrait_snippets.append(clean_text(self.get_starttag_text()))
        if "yuanzhang" in classes and not self._name_div_depth:
            self._name_div_depth = 1
            self._name_span_depth = 0
            self._name_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "span" and self._name_span_depth:
            self._name_span_depth -= 1
            return
        if tag.lower() == "div" and self._name_div_depth:
            self._name_div_depth -= 1
            if not self._name_div_depth:
                name = clean_text(" ".join(self._name_parts))
                if name:
                    self.names.append(name)
                self._name_parts = []

    def handle_data(self, data: str) -> None:
        if self._name_div_depth and not self._name_span_depth:
            self._name_parts.append(data)


def inspect_portrait_reference(
    html: str, source_link: str, expected_name: str
) -> tuple[str, base.PortraitReference | None]:
    if not detail_id(source_link):
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    parser = Ny5yPhysicianPageParser()
    parser.feed(html)
    if parser.names != [clean_text(expected_name)]:
        raise RuntimeError(
            f"详情姓名与底表不一致：底表={expected_name} 官网={parser.names or ['空']} {source_link}"
        )
    if not parser.portrait_attrs:
        return "无照片容器", None
    if len(parser.portrait_attrs) != 1:
        raise RuntimeError(
            f"yisheng_xq_bug_left 容器不唯一：{source_link} 数量={len(parser.portrait_attrs)}"
        )
    raw_url = base.style_background_url(parser.portrait_attrs[0].get("style"))
    if not raw_url:
        return "无照片容器", None
    absolute = urljoin(source_link, raw_url)
    decoded_query = suspicious_query_decoding(absolute)
    lowered_path = unquote(urlparse(absolute).path).casefold()
    if decoded_query or any(marker in lowered_path for marker in base.PLACEHOLDER_MARKERS):
        return "占位图", None
    normalized = page_referenced_photo_url(raw_url, source_link)
    if not normalized:
        raise RuntimeError(f"页面引用照片 URL 越界：{source_link} {raw_url}")
    STRUCTURE_EVIDENCE[source_link] = {
        "name": clean_text(expected_name),
        "detail_id": detail_id(source_link),
        "container_selector": "div.yisheng_xq_bug_left",
        "container_count": 1,
        "html_snippet": parser.portrait_snippets[0],
        "raw_background_url": raw_url,
        "normalized_photo_url": normalized,
        "decoded_query_values": decoded_query_values(normalized),
        "excluded_resource_examples": list(EXCLUDED_RESOURCE_EXAMPLES),
        "decision_basis": (
            "only the unique yisheng_xq_bug_left inline background-image is eligible; "
            "all other page and narrative images are excluded"
        ),
        "observed_utc": utc_now(),
    }
    return "", base.PortraitReference(
        page_title=HOSPITAL,
        photo_url=normalized,
        source_attribute="div.yisheng_xq_bug_left inline background-image",
    )


class OfficialSession:
    """Owner-approved browser-UA urllib session without cookies, proxy, or bypass."""

    def __init__(self) -> None:
        self.incomplete_read_retry_count = 0
        self.opener = build_opener(ProxyHandler({}))

    @property
    def cookie_names(self) -> list[str]:
        return []

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
                raise RuntimeError(f"官网响应连续两次传输不完整：{url}") from exc
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


def reachability_preflight(
    session: OfficialSession,
    sample_detail_url: str,
    interval_seconds: int = REACHABILITY_RETRY_INTERVAL_SECONDS,
) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    for round_number in (1, 2):
        for target, url, referer in (
            ("homepage_non_gate", OFFICIAL_HOME, ""),
            ("sample_detail_gate", sample_detail_url, DIRECTORY_URL),
        ):
            observed_utc = utc_now()
            try:
                status, content_type, _, content = session.get(url, referer)
                observations.append(
                    {
                        "round": round_number,
                        "target": target,
                        "url": url,
                        "status": status,
                        "content_type": content_type,
                        "bytes": len(content),
                        "observed_utc": observed_utc,
                        "error": "",
                    }
                )
            except RuntimeError as exc:
                observations.append(
                    {
                        "round": round_number,
                        "target": target,
                        "url": url,
                        "status": None,
                        "content_type": "",
                        "bytes": 0,
                        "observed_utc": observed_utc,
                        "error": str(exc),
                    }
                )
        if round_number == 1:
            time.sleep(interval_seconds)

    detail_observations = [item for item in observations if item["target"] == "sample_detail_gate"]
    if len(detail_observations) != 2 or any(item["status"] != 200 for item in detail_observations):
        raise RuntimeError(
            "抽样详情两轮 UA 可达性门禁未全部 HTTP 200；须先在 Issue 回报并启动 5 轮聚合探测"
        )
    return observations


def limited_unique_color_count(content: bytes, limit: int = 2) -> int:
    with Image.open(io.BytesIO(content)) as image:
        rgba = ImageOps.exif_transpose(image).convert("RGBA")
        colors = rgba.getcolors(maxcolors=limit + 1)
    return limit + 1 if colors is None else len(colors)


def assert_placeholder_gates(samples: list[dict[str, Any]]) -> None:
    by_sha: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for sample in samples:
        content = Path(sample["disk_path"]).read_bytes()
        unique_colors = limited_unique_color_count(content, limit=2)
        if unique_colors <= 2:
            raise RuntimeError(
                "[FATAL - HUMAN_INTERVENTION_REQUIRED] "
                f"{sample['name']} 全图唯一颜色数={unique_colors}，命中占位人工复判门禁"
            )
        decoded = suspicious_query_decoding(sample["photo_url"])
        if decoded:
            raise RuntimeError(
                "[FATAL - HUMAN_INTERVENTION_REQUIRED] "
                f"{sample['name']} query Base64 解码={decoded}，命中占位人工复判门禁"
            )
        sample["unique_color_count_lower_bound"] = unique_colors
        sample["decoded_query_values"] = decoded_query_values(sample["photo_url"])
        by_sha[sample["sha256"]].append(sample)
    for digest, group in by_sha.items():
        distinct_sources = {sample["source_link"] for sample in group}
        if len(distinct_sources) > 1:
            names = sorted({sample["name"] for sample in group})
            raise RuntimeError(
                "[FATAL - HUMAN_INTERVENTION_REQUIRED] "
                f"跨详情同 SHA 待 owner 追认：sha256={digest} names={names}"
            )


def contact_sheet_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return base.contact_sheet_font(size)


def build_contact_sheet(samples: list[dict[str, Any]]) -> None:
    assert_placeholder_gates(samples)
    columns = 2
    cell_width = 520
    cell_height = 520
    image_box = (460, 380)
    row_count = (len(samples) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_width, row_count * cell_height), "#D9DEE3")
    draw = ImageDraw.Draw(canvas)
    title_font = contact_sheet_font(20)
    detail_font = contact_sheet_font(16)
    for index, sample in enumerate(samples):
        left = (index % columns) * cell_width
        top = (index // columns) * cell_height
        draw.rectangle(
            (left + 4, top + 4, left + cell_width - 5, top + cell_height - 5),
            fill="#C8CDD2",
            outline="#2F3942",
            width=3,
        )
        with Image.open(sample["disk_path"]) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            thumb = ImageOps.contain(image, image_box)
        if thumb.width < 2 or thumb.height < 2:
            raise RuntimeError(f"[FATAL - HUMAN_INTERVENTION_REQUIRED] 拼图不可见格：{sample['name']}")
        image_left = left + (cell_width - thumb.width) // 2
        image_top = top + 12 + (image_box[1] - thumb.height) // 2
        canvas.paste(thumb, (image_left, image_top))
        draw.rectangle(
            (image_left - 2, image_top - 2, image_left + thumb.width + 1, image_top + thumb.height + 1),
            outline="#111820",
            width=2,
        )
        draw.text(
            (left + 18, top + 410),
            f"{index + 1}. {sample['name']}｜{sample['title']}",
            fill="#111111",
            font=title_font,
        )
        draw.text((left + 18, top + 448), sample["department"], fill="#222222", font=detail_font)
        draw.text(
            (left + 18, top + 480),
            f"{sample['width']}×{sample['height']}｜{sample['bytes']} bytes",
            fill="#333333",
            font=detail_font,
        )
    canvas.save(CONTACT_SHEET_PATH, format="JPEG", quality=92, optimize=True)


def load_scope_rows() -> list[dict[str, Any]]:
    payload = json.loads(base.MASTER_JSON_PATH.read_text(encoding="utf-8"))
    rows = [dict(row) for row in payload.get("rows", []) if clean_text(row.get("医院")) == HOSPITAL]
    if len(rows) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError(
            f"Issue #{ISSUE_NUMBER} 范围漂移：应为 {EXPECTED_SCOPE_COUNT} 行，实际 {len(rows)} 行"
        )
    if any(clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")) for row in rows):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} TRIAL 范围内已有照片字段，需 owner 先裁决")
    sources = [clean_text(row.get("来源链接")) for row in rows]
    if len(sources) != len(set(sources)):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} 范围来源链接不唯一")
    invalid = [source for source in sources if not detail_id(source)]
    if invalid:
        raise RuntimeError("范围存在非授权详情链接：" + "、".join(invalid[:5]))
    entries = Counter(clean_text(row.get("采集入口")) for row in rows)
    if entries != Counter({DIRECTORY_URL: 133, SECONDARY_DIRECTORY_URL: 1}):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} 采集入口分布漂移：{dict(entries)}")
    return rows


def select_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for expected_name, expected_level in SAMPLE_PLAN:
        matches = [row for row in rows if clean_text(row.get("姓名")) == expected_name]
        if len(matches) != 1:
            raise RuntimeError(f"试采姓名范围不唯一：{expected_name} 数量={len(matches)}")
        row = dict(matches[0])
        actual_level = base.title_level(row.get("职称身份原文"))
        if actual_level != expected_level:
            raise RuntimeError(
                f"试采职称层级漂移：{expected_name} 应为 {expected_level} 实际 {actual_level}"
            )
        result.append(row)
    departments = {base.atomic_department(row) for row in result}
    counts = Counter(base.title_level(row.get("职称身份原文")) for row in result)
    actual_counts = {level: counts[level] for level in EXPECTED_TITLE_COUNTS}
    if len(departments) < MIN_TRIAL_DEPARTMENTS:
        raise RuntimeError(f"科室覆盖不足：{len(departments)}")
    if actual_counts != EXPECTED_TITLE_COUNTS:
        raise RuntimeError(f"职称分层覆盖漂移：{actual_counts}")
    return result


def declared_extension(content_type: str) -> str:
    return {
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
    }.get(clean_text(content_type).split(";", 1)[0].casefold(), "unknown")


def validate_payload(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    errors: list[str] = []
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围不是 134 行")
    if meta.get("trial_detail_count") != EXPECTED_TRIAL_COUNT:
        errors.append("详情样本不是 10 位")
    if meta.get("department_coverage_count", 0) < MIN_TRIAL_DEPARTMENTS:
        errors.append("科室覆盖不足 5 个")
    if meta.get("title_level_counts") != EXPECTED_TITLE_COUNTS:
        errors.append(f"职称分层漂移：{meta.get('title_level_counts')}")
    if meta.get("photo_sample_count") != EXPECTED_TRIAL_COUNT:
        errors.append("实图样本不是 10 张")
    if meta.get("fuse_problem_count") != 0:
        errors.append("TRIAL 存在失败或结构异常")
    if meta.get("constructed_unreferenced_probe_count") != 0:
        errors.append("发生页面未引用路径探测")
    if meta.get("third_party_source_count") != 0:
        errors.append("发生第三方来源访问")
    if meta.get("cookie_names"):
        errors.append("urllib 会话意外产生 Cookie")
    if meta.get("user_agent") != USER_AGENT:
        errors.append("未使用 Owner 批准的固定浏览器 User-Agent")
    reachability = meta.get("reachability_preflight", [])
    if len(reachability) != 4:
        errors.append("UA 可达性留痕不是两轮首页+抽样详情")
    detail_preflight = [item for item in reachability if item.get("target") == "sample_detail_gate"]
    if len(detail_preflight) != 2 or any(item.get("status") != 200 for item in detail_preflight):
        errors.append("抽样详情两轮 UA 可达性门禁未全部 HTTP 200")
    if meta.get("homepage_is_gate") is not False:
        errors.append("首页被错误提升为采集门禁")
    if meta.get("protected_assets_before") != meta.get("protected_assets_after"):
        errors.append("正式受保护资产发生变化")
    if len({sample.get("sha256") for sample in payload.get("photo_samples", [])}) != EXPECTED_TRIAL_COUNT:
        errors.append("TRIAL 跨医生 SHA 不唯一")
    if not CONTACT_SHEET_PATH.is_file():
        errors.append("联系表不存在")
    for sample in payload.get("photo_samples", []):
        path = Path(sample["disk_path"])
        if not path.is_file():
            errors.append(f"照片不存在：{path}")
            continue
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != sample.get("sha256"):
            errors.append(f"照片 SHA 不一致：{path.name}")
        if len(content) != sample.get("bytes"):
            errors.append(f"照片字节不一致：{path.name}")
        if limited_unique_color_count(content, limit=2) <= 2:
            errors.append(f"照片命中近单色门禁：{path.name}")
        if suspicious_query_decoding(sample.get("photo_url", "")):
            errors.append(f"照片 query 命中占位门禁：{path.name}")
    if errors:
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} TRIAL 门禁失败：" + "；".join(errors))


def manifest_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for sample in payload["photo_samples"]:
        actual = Path(sample["filename"]).suffix.lower().lstrip(".")
        declared = declared_extension(sample["content_type"])
        result.append(
            {
                "姓名": sample["name"],
                "科室": sample["department"],
                "职称层级": sample["title_level"],
                "主职称": sample["title"],
                "来源链接": sample["source_link"],
                "详情HTTP": sample["detail_http_status"],
                "照片容器": sample["photo_source_attribute"],
                "照片链接": sample["photo_url"],
                "照片HTTP": sample["photo_http_status"],
                "声明Content-Type": sample["content_type"],
                "声明格式": declared,
                "实际魔数格式": actual,
                "声明/实际一致": "是" if declared == actual else "否",
                "文件名": sample["filename"],
                "字节": sample["bytes"],
                "SHA-256": sample["sha256"],
                "魔数": sample["magic_hex"],
                "宽": sample["width"],
                "高": sample["height"],
                "唯一颜色下界": sample.get("unique_color_count_lower_bound"),
                "大图判定": "、".join(sample["large_reasons"]) or "未命中",
            }
        )
    return result


def write_manifest(payload: dict[str, Any]) -> None:
    rows = manifest_rows(payload)
    fields = list(rows[0])
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|").replace("\n", " ")


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    samples = []
    for sample in payload["photo_samples"]:
        actual = Path(sample["filename"]).suffix.lower().lstrip(".")
        declared = declared_extension(sample["content_type"])
        samples.append(
            f"| {markdown_cell(sample['name'])} | {markdown_cell(sample['department'])} | "
            f"{sample['title_level']} | {markdown_cell(sample['title'])} | {sample['bytes']} | "
            f"{sample['width']}×{sample['height']} | {declared}/{actual} | "
            f"`{sample['sha256']}` | {sample['photo_url']} |"
        )
    diagnostics = []
    for item in payload.get("structure_diagnostics", []):
        diagnostics.append(
            f"### {item['name']} / ID {item['detail_id']}\n\n"
            f"```html\n{item['html_snippet']}\n```\n\n"
            f"- 页面引用：`{item['raw_background_url']}`\n"
            f"- 规范化 URL：{item['normalized_photo_url']}\n"
            f"- 判定：{item['decision_basis']}\n"
        )
    protected = []
    for path, facts in meta["protected_assets_before"]["master_assets"].items():
        protected.append(f"| `{path}` | {facts['bytes']} | `{facts['sha256']}` |")
    levels = "、".join(f"{key} {value}" for key, value in meta["title_level_counts"].items())
    reachability_rows = []
    for item in meta["reachability_preflight"]:
        reachability_rows.append(
            f"| {item['round']} | {item['target']} | {item['status']} | {item['content_type']} | "
            f"{item['bytes']} | {item['observed_utc']} |"
        )
    report = f"""# Issue #79 {HOSPITAL}照片补录 TRIAL 报告

> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 生成日期：{meta['run_date']}
> 视觉复核：`{meta['visual_review_status']}`

## 范围与抽样

- 固定范围：{meta['scope_count']} 行、{meta['scope_unique_source_count']} 个唯一详情 URL；照片双列全空。
- 采集入口：主入口 133 行，岭南名医入口 1 行；两者均为 Issue #79 明示官网入口。
- TRIAL：{meta['trial_detail_count']} 位、覆盖 {meta['department_coverage_count']} 个科室；职称分层 {levels}。全院无初级记录，已覆盖全部可用层级。
- 详情 HTTP 200：{meta['detail_http_200_count']}/{meta['trial_detail_count']}；实图 {meta['photo_sample_count']}/{meta['trial_detail_count']}；失败/结构异常 {meta['fuse_problem_count']}。
- Owner 批准的固定浏览器 UA urllib：Cookie 0、代理 0、挑战绕过 0、页面未引用路径探测 0、第三方来源 0。
- 首页仅留痕、不是采集门禁；固定详情页及其唯一容器照片资源才是门禁。

## FATAL 解除后的 UA 可达性复测

- 两轮间隔：{meta['reachability_retry_interval_seconds']} 秒。
- User-Agent：`{meta['user_agent']}`。

| 轮次 | 目标 | HTTP | Content-Type | 字节 | UTC |
|---:|---|---:|---|---:|---|
{chr(10).join(reachability_rows)}

## 容器结构诊断

- 唯一允许容器：`div.yisheng_xq_bug_left` 的内联 `background-image`。
- 页面其他 `background-image`、正文 ueditor 叙事配图、logo、悬浮按钮、二维码和政府徽标全部排除。
- 排除样例：{'; '.join(EXCLUDED_RESOURCE_EXAMPLES)}。

{chr(10).join(diagnostics)}

## TRIAL 原始字节

- 10 张共 {meta['photo_total_bytes']} bytes；平均 {meta['photo_average_bytes']} bytes。
- >5 MiB：{meta['over_5mib_count']}；>20 MiB：{meta['over_20mib_count']}。
- 仅保存页面容器实际引用响应原始字节；未压缩、未转码；扩展名随实际魔数。

| 姓名 | 科室 | 层级 | 主职称 | 字节 | 尺寸 | 声明/实际 | SHA-256 | 页面引用照片 |
|---|---|---|---|---:|---:|---|---|---|
{chr(10).join(samples)}

详细声明/实际双列、HTTP、魔数和命名见 `{TRIAL_CSV_PATH}` 与 `{TRIAL_JSON_PATH}`。

## 占位与视觉四门禁

1. query Base64 解码含 blank/placeholder/default 时拦截。
2. 全图唯一颜色数不大于 2 时拦截。
3. 跨医生同 SHA 时停止并标注“待 owner 追认”；本样本重复 SHA 组 0。
4. 拼图使用灰底和深色边框；空白/不可见格熔断。联系表：`{CONTACT_SHEET_PATH}`。

视觉状态：`{meta['visual_review_status']}`。

## 正式资产零修改

| 文件 | 字节 | SHA-256 |
|---|---:|---|
{chr(10).join(protected)}

- 本院画像树：{meta['protected_assets_before']['profile_tree']['file_count']} 个文件，聚合 SHA-256 `{meta['protected_assets_before']['profile_tree']['sha256']}`。
- 正式照片树前后一致：`{json.dumps(meta['protected_assets_before']['formal_photo_tree'], ensure_ascii=False)}`。
- TRIAL 仅写 `work/` 工件，未回填总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件完成后提交并发布 `TRIAL_READY_FOR_OWNER_AUDIT`，等待 Owner 审计。未取得当前 PR 的明确 `FULL_APPEND_AND_OBSIDIAN` 指令前，不得回填正式资产。
"""
    TRIAL_REPORT_PATH.write_text(report, encoding="utf-8")


def enrich_payload(payload: dict[str, Any]) -> dict[str, Any]:
    assert_placeholder_gates(payload["photo_samples"])
    for sample in payload["photo_samples"]:
        actual = Path(sample["filename"]).suffix.lower().lstrip(".")
        declared = declared_extension(sample["content_type"])
        sample["declared_extension"] = declared
        sample["actual_extension"] = actual
        sample["declared_matches_actual"] = declared == actual
    payload["structure_diagnostics"] = [
        STRUCTURE_EVIDENCE[key] for key in sorted(STRUCTURE_EVIDENCE, key=lambda value: int(detail_id(value)))
    ]
    meta = payload["meta"]
    meta["visual_review_status"] = "PENDING_MANUAL_CONTACT_SHEET_REVIEW"
    meta["over_5mib_count"] = sum(sample["bytes"] > 5 * 1024 * 1024 for sample in payload["photo_samples"])
    meta["over_20mib_count"] = sum(sample["bytes"] > 20 * 1024 * 1024 for sample in payload["photo_samples"])
    meta["cross_doctor_duplicate_sha_groups"] = 0
    meta["placeholder_query_gate_hits"] = 0
    meta["near_monochrome_gate_hits"] = 0
    meta["contact_sheet_background"] = "gray with dark borders"
    return payload


def configure_base() -> None:
    values = {
        "HOSPITAL": HOSPITAL,
        "ISSUE_NUMBER": ISSUE_NUMBER,
        "PROFILE_DIR": PROFILE_DIR,
        "FORMAL_PHOTO_DIR": FORMAL_PHOTO_DIR,
        "TRIAL_BASENAME": TRIAL_BASENAME,
        "TRIAL_JSON_PATH": TRIAL_JSON_PATH,
        "TRIAL_CSV_PATH": TRIAL_CSV_PATH,
        "TRIAL_REPORT_PATH": TRIAL_REPORT_PATH,
        "CONTACT_SHEET_PATH": CONTACT_SHEET_PATH,
        "TRIAL_PHOTO_DIR": TRIAL_PHOTO_DIR,
        "OFFICIAL_HOME": OFFICIAL_HOME,
        "DIRECTORY_URL": DIRECTORY_URL,
        "OFFICIAL_HOST": OFFICIAL_HOST,
        "PHOTO_PREFIX": PHOTO_PREFIX,
        "EXPECTED_SCOPE_COUNT": EXPECTED_SCOPE_COUNT,
        "EXPECTED_TRIAL_COUNT": EXPECTED_TRIAL_COUNT,
        "MIN_TRIAL_DEPARTMENTS": MIN_TRIAL_DEPARTMENTS,
        "SAMPLE_PLAN": SAMPLE_PLAN,
    }
    for name, value in values.items():
        setattr(base, name, value)
    base.detail_id = detail_id
    base.page_referenced_photo_url = page_referenced_photo_url
    base.inspect_portrait_reference = inspect_portrait_reference
    base.OfficialSession = OfficialSession
    base.load_scope_rows = load_scope_rows
    base.select_trial_rows = select_trial_rows
    base.build_contact_sheet = build_contact_sheet
    base.validate_payload = validate_payload
    base.write_manifest = lambda rows: None
    base.write_report = lambda payload: None


def collect_trial_payload(run_date: str) -> dict[str, Any]:
    protected_before = base.protected_snapshot()
    scope_rows = load_scope_rows()
    trial_rows = select_trial_rows(scope_rows)
    STRUCTURE_EVIDENCE.clear()
    session = OfficialSession()
    sample_detail_url = clean_text(trial_rows[0].get("来源链接"))
    reachability = reachability_preflight(session, sample_detail_url)

    detail_errors: list[dict[str, Any]] = []
    structure_mismatches: list[dict[str, Any]] = []
    failure_states: list[dict[str, Any]] = []
    portrait_rows: list[tuple[dict[str, Any], base.PortraitReference, int]] = []
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
        extension = base.magic_extension(content, content_type)
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
        try:
            width, height = base.image_dimensions(content)
            filename, path = base.allocate_trial_photo(row, extension, content)
            if not path.exists():
                path.write_bytes(content)
        except Exception as exc:  # noqa: BLE001 - preserve per-image evidence
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
        if len(content) > base.LARGE_BYTES:
            large_reasons.append(">200KB")
        if width > base.LARGE_WIDTH:
            large_reasons.append("宽>800px")
        photo_samples.append(
            {
                "name": clean_text(row.get("姓名")),
                "department": base.atomic_department(row),
                "title_level": base.title_level(row.get("职称身份原文")),
                "title": base.primary_title(row.get("职称身份原文")),
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
        )

    build_contact_sheet(photo_samples)
    protected_after = base.protected_snapshot()
    fuse_problem_count = (
        len(detail_errors) + len(structure_mismatches) + len(failure_states) + len(photo_errors)
    )
    fuse_ratio = fuse_problem_count / EXPECTED_TRIAL_COUNT
    if fuse_ratio > base.MAX_FAILURE_RATIO:
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] "
            f"TRIAL 熔断问题超过 30%：{fuse_problem_count}/{EXPECTED_TRIAL_COUNT}"
        )
    total_bytes = sum(sample["bytes"] for sample in photo_samples)
    average_bytes = total_bytes // max(1, len(photo_samples))
    title_counts = Counter(base.title_level(row.get("职称身份原文")) for row in trial_rows)
    homepage_observations = [
        item for item in reachability if item["target"] == "homepage_non_gate"
    ]
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
            "trial_detail_count": len(trial_rows),
            "department_coverage_count": len(
                {base.atomic_department(row) for row in trial_rows}
            ),
            "covered_departments": sorted(
                {base.atomic_department(row) for row in trial_rows}
            ),
            "title_level_counts": {
                level: title_counts[level] for level in ("正高", "副高", "中级", "初级")
            },
            "home_http_status": homepage_observations[-1]["status"],
            "homepage_is_gate": False,
            "reachability_preflight": reachability,
            "reachability_retry_interval_seconds": REACHABILITY_RETRY_INTERVAL_SECONDS,
            "user_agent": USER_AGENT,
            "proxy_enabled": False,
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
            "photo_average_bytes": average_bytes,
            "estimated_full_count": EXPECTED_SCOPE_COUNT,
            "estimated_full_bytes": average_bytes * EXPECTED_SCOPE_COUNT,
            "estimated_full_mib": average_bytes * EXPECTED_SCOPE_COUNT / 1024 / 1024,
            "over_200kb_count": sum(
                sample["bytes"] > base.LARGE_BYTES for sample in photo_samples
            ),
            "over_800px_count": sum(
                sample["width"] > base.LARGE_WIDTH for sample in photo_samples
            ),
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
                "科室": base.atomic_department(row),
                "职称层级": base.title_level(row.get("职称身份原文")),
                "主职称": base.primary_title(row.get("职称身份原文")),
                "来源链接": clean_text(row.get("来源链接")),
            }
            for row in trial_rows
        ],
    }
    return payload


def run_trial(run_date: str) -> dict[str, Any]:
    configure_base()
    payload = enrich_payload(collect_trial_payload(run_date))
    validate_payload(payload)
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(payload)
    write_report(payload)
    return payload


def mark_visual_pass() -> dict[str, Any]:
    payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
    validate_payload(payload)
    payload["meta"]["visual_review_status"] = (
        "PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS"
    )
    payload["meta"]["visual_reviewed_utc"] = utc_now()
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(payload)
    write_report(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"Issue #{ISSUE_NUMBER} {HOSPITAL} photo-backfill TRIAL")
    parser.add_argument("--run-date", default=date.today().isoformat())
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--mark-visual-pass", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_base()
    if args.mark_visual_pass:
        payload = mark_visual_pass()
    elif args.validate:
        payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
        validate_payload(payload)
    else:
        payload = run_trial(args.run_date)
    print(
        "TRIAL_VALIDATED "
        f"scope={payload['meta']['scope_count']} samples={payload['meta']['photo_sample_count']} "
        f"departments={payload['meta']['department_coverage_count']} "
        f"visual={payload['meta']['visual_review_status']}"
    )


if __name__ == "__main__":
    main()
