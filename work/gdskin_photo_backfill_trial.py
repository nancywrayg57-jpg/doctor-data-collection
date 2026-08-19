from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, quote, unquote, urljoin, urlparse, urlunparse

import ny5y_photo_backfill_trial as framework


base = framework.base
ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "南方医科大学皮肤病医院"
ISSUE_NUMBER = 83
EXPECTED_SCOPE_COUNT = 77
EXPECTED_TRIAL_COUNT = 10
# The 77 historical rows have empty department fields. Issue #83 requires
# classification-entry coverage instead, which is enforced separately below.
MIN_TRIAL_DEPARTMENTS = 1
OFFICIAL_HOME = "https://www.gdskin.com/"
DIRECTORY_URL = "https://www.gdskin.com/Showclass.aspx?id=906"
OFFICIAL_HOST = "gdskin.com"
PHOTO_PREFIX = "/uploadimg/"
PROFILE_DIR = VAULT / "01_试点医院" / HOSPITAL
FORMAL_PHOTO_DIR = PROFILE_DIR / "照片"
TRIAL_BASENAME = f"{HOSPITAL}_photo_backfill_trial"
TRIAL_JSON_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
TRIAL_CSV_PATH = WORK_DIR / f"{TRIAL_BASENAME}_manifest.csv"
TRIAL_REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
TRIAL_PHOTO_DIR = WORK_DIR / f"{TRIAL_BASENAME}_photos"
ENTRY_COUNTS = {
    "901": 1,
    "902": 3,
    "906": 29,
    "910": 7,
    "913": 8,
    "915": 14,
    "917": 6,
    "921": 4,
    "922": 5,
}
EXPECTED_TITLE_COUNTS = {"正高": 4, "副高": 2, "中级": 3, "初级": 1}
SAMPLE_PLAN = (
    ("顾有守", "正高", "901"),
    ("杨斌", "正高", "902"),
    ("吉苏云", "副高", "906"),
    ("谷梅", "正高", "906"),
    ("王柳苑", "中级", "910"),
    ("鲜华", "副高", "913"),
    ("杜美毅", "初级", "915"),
    ("严婷婷", "中级", "917"),
    ("何仁亮", "正高", "921"),
    ("钟泽敏", "中级", "922"),
)
REUSED_SUCCESS_NAMES = frozenset(
    {
        "顾有守",
        "杨斌",
        "吉苏云",
        "谷梅",
        "王柳苑",
        "鲜华",
        "严婷婷",
        "何仁亮",
        "钟泽敏",
    }
)
REPLACEMENT_MATRIX = (
    {
        "original_name": "吴芳芳",
        "replacement_name": "谷梅",
        "entry_id": "906",
        "original_title_level": "初级",
        "replacement_title_level": "正高",
        "reason": "入口906/初级唯一替代人于碧慧同样无照片容器；Owner裁决入口覆盖优先并允许入口内跨层，取最高可用层",
    },
    {
        "original_name": "孟凡琪",
        "replacement_name": "杜美毅",
        "entry_id": "915",
        "original_title_level": "初级",
        "replacement_title_level": "初级",
        "reason": "原样本及龚洋洋/郭先荟候选的NBSP尾缀页面引用均悬空；按Owner指定改用同入口同层且资源200的杜美毅",
    },
    {
        "original_name": "杨超",
        "replacement_name": "钟泽敏",
        "entry_id": "922",
        "original_title_level": "中级",
        "replacement_title_level": "中级",
        "reason": "原页面无照片容器；按Owner裁决同入口同层替换",
    },
)
PRIOR_FAILURE_EVIDENCE = (
    {
        "name": "吴芳芳",
        "entry_id": "906",
        "title_level": "初级",
        "detail_id": "6197",
        "source_link": "https://www.gdskin.com/ShowNews.ASPX?ID=6197",
        "detail_http_status": 200,
        "failure_state": "无照片容器",
        "page_referenced_photo_count": 0,
        "decision_feature": "全页无 /uploadimg/ 引用；仅 WebResource 与备案装饰图",
        "observed_utc": "2026-08-19T11:24:41Z",
    },
    {
        "name": "孟凡琪",
        "entry_id": "915",
        "title_level": "初级",
        "detail_id": "5593",
        "source_link": "https://www.gdskin.com/ShowNews.ASPX?ID=5593",
        "detail_http_status": 200,
        "failure_state": "照片资源不可达",
        "page_referenced_photo_count": 1,
        "raw_photo_reference": "../system_dntb/../uploadimg/孟凡琪\u00a0 \u00a0.jpg",
        "normalized_photo_url": "https://www.gdskin.com/uploadimg/孟凡琪\u00a0 \u00a0.jpg",
        "transport_url": "https://www.gdskin.com/uploadimg/%E5%AD%9F%E5%87%A1%E7%90%AA%C2%A0%20%C2%A0.jpg",
        "photo_http_status": 404,
        "photo_content_type": "text/html",
        "photo_response_bytes": 1163,
        "decision_feature": "页面原引用含 NBSP+空格尾缀；浏览器语义编码后仍为404，禁止构造变体",
        "observed_utc": "2026-08-19T11:24:41Z",
    },
    {
        "name": "杨超",
        "entry_id": "922",
        "title_level": "中级",
        "detail_id": "6200",
        "source_link": "https://www.gdskin.com/ShowNews.ASPX?ID=6200",
        "detail_http_status": 200,
        "failure_state": "无照片容器",
        "page_referenced_photo_count": 0,
        "decision_feature": "全页无 /uploadimg/ 引用；仅 WebResource 与备案装饰图",
        "observed_utc": "2026-08-19T11:24:41Z",
    },
)
REPLACEMENT_CANDIDATE_EVIDENCE = (
    {
        "name": "于碧慧",
        "entry_id": "906",
        "title_level": "初级",
        "detail_id": "6196",
        "source_link": "https://www.gdskin.com/ShowNews.ASPX?ID=6196",
        "detail_http_status": 200,
        "failure_state": "无照片容器",
        "page_referenced_photo_count": 0,
        "decision_feature": "入口906/初级唯一替代候选同样无 /uploadimg/ 引用",
        "observed_utc": "2026-08-19T12:07:00Z",
    },
    {
        "name": "龚洋洋",
        "entry_id": "915",
        "title_level": "初级",
        "detail_id": "5594",
        "source_link": "https://www.gdskin.com/ShowNews.ASPX?ID=5594",
        "detail_http_status": 200,
        "failure_state": "照片资源不可达",
        "page_referenced_photo_count": 1,
        "raw_photo_reference": "../system_dntb/../uploadimg/龚洋洋\u00a0.jpg",
        "normalized_photo_url": "https://www.gdskin.com/uploadimg/龚洋洋\u00a0.jpg",
        "transport_url": "https://www.gdskin.com/uploadimg/%E9%BE%9A%E6%B4%8B%E6%B4%8B%C2%A0.jpg",
        "photo_http_status": 404,
        "photo_content_type": "text/html",
        "photo_response_bytes": 1163,
        "decision_feature": "页面原引用含NBSP尾缀；仅作浏览器语义百分号编码后仍为404，禁止构造变体",
        "observed_utc": "2026-08-19T12:20:58Z",
    },
    {
        "name": "郭先荟",
        "entry_id": "915",
        "title_level": "初级",
        "detail_id": "5595",
        "source_link": "https://www.gdskin.com/ShowNews.ASPX?ID=5595",
        "detail_http_status": 200,
        "failure_state": "照片资源不可达",
        "page_referenced_photo_count": 1,
        "raw_photo_reference": "../system_dntb/../uploadimg/郭先荟\u00a0.jpg",
        "normalized_photo_url": "https://www.gdskin.com/uploadimg/郭先荟\u00a0.jpg",
        "transport_url": "https://www.gdskin.com/uploadimg/%E9%83%AD%E5%85%88%E8%8D%9F%C2%A0.jpg",
        "photo_http_status": 404,
        "decision_feature": "页面属性以&nbsp;表达NBSP尾缀；按浏览器语义解析并编码后仍为404，禁止构造变体",
        "observed_utc": "2026-08-19T12:27:35Z",
    },
)
EXCLUDED_RESOURCE_EXAMPLES = (
    "/WebResource.axd 跳过导航零尺寸图",
    "images/备案图标.png",
    "logo/banner/nav/foot 等站架资源",
    "除唯一 /uploadimg/ 正文 img src 外的所有页面图片",
)
KNOWN_PLACEHOLDER_DETAIL_URL = "https://www.gdskin.com/ShowNews.ASPX?ID=5566"
KNOWN_PLACEHOLDER_NAME = "文海泉"
KNOWN_PLACEHOLDER_SHA256 = (
    "d2565a802cdc8d7ca29f218cd60685542d139a7de68ffc9ee559011e2f693aac"
)
REQUEST_INTERVAL_SECONDS = 2.0
EXPECTED_NETWORK_REQUEST_COUNT = 17
EXPECTED_REUSE_COUNT = 9
EXPECTED_NEW_DOWNLOAD_COUNT = 1

REQUEST_TRACE: list[dict[str, Any]] = []
REUSE_TRACE: list[dict[str, Any]] = []
PLACEHOLDER_EVIDENCE: dict[str, Any] = {}
SCOPE_ENTRY_BY_SOURCE: dict[str, str] = {}
PHOTO_CACHE_BY_URL: dict[str, Path] = {}

_BaseOfficialSession = framework.OfficialSession
_framework_reachability_preflight = framework.reachability_preflight
_framework_assert_placeholder_gates = framework.assert_placeholder_gates
_framework_enrich_payload = framework.enrich_payload
_framework_validate_payload = framework.validate_payload
_framework_manifest_rows = framework.manifest_rows


def clean_text(value: Any) -> str:
    return framework.clean_text(value)


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"路径越出仓库根目录：{path}") from exc


def detail_id(value: Any) -> str:
    parsed = urlparse(clean_text(value))
    if (
        parsed.scheme != "https"
        or framework.comparable_host(parsed.geturl()) != OFFICIAL_HOST
        or parsed.path.casefold() != "/shownews.aspx"
        or parsed.fragment
    ):
        return ""
    query = parse_qsl(parsed.query, keep_blank_values=True)
    if (
        len(query) != 1
        or query[0][0].casefold() != "id"
        or not re.fullmatch(r"[1-9]\d*", query[0][1])
    ):
        return ""
    return query[0][1]


def entry_id(value: Any) -> str:
    parsed = urlparse(clean_text(value))
    if (
        parsed.scheme != "https"
        or framework.comparable_host(parsed.geturl()) != OFFICIAL_HOST
        or parsed.path.casefold() != "/showclass.aspx"
        or parsed.fragment
    ):
        return ""
    query = parse_qsl(parsed.query, keep_blank_values=True)
    if len(query) != 1 or query[0][0].casefold() != "id":
        return ""
    return query[0][1] if query[0][1] in ENTRY_COUNTS else ""


def authorized_photo_candidate(value: Any, base_url: str) -> str:
    # URL attributes are not prose. The live site contains a tab before one
    # filename suffix; collapsing whitespace would invent a literal space URL,
    # while urljoin follows browser URL parsing and removes the tab.
    raw = str(value or "").strip()
    if not raw:
        return ""
    absolute = urljoin(base_url, raw)
    parsed = urlparse(absolute)
    if (
        parsed.scheme != "https"
        or framework.comparable_host(absolute) != OFFICIAL_HOST
        or parsed.fragment
        or not parsed.path.casefold().startswith(PHOTO_PREFIX)
    ):
        return ""
    return absolute


def placeholder_marker_reason(value: str) -> str:
    decoded_path = unquote(urlparse(value).path).casefold()
    if "占位" in decoded_path:
        return "explicit_chinese_placeholder_filename"
    if any(marker in decoded_path for marker in base.PLACEHOLDER_MARKERS):
        return "generic_placeholder_path_marker"
    decoded_query = framework.suspicious_query_decoding(value)
    if decoded_query:
        return f"base64_query_marker:{decoded_query}"
    return ""


def page_referenced_photo_url(value: Any, base_url: str) -> str:
    absolute = authorized_photo_candidate(value, base_url)
    if not absolute or placeholder_marker_reason(absolute):
        return ""
    return absolute


def is_known_placeholder_digest(value: Any) -> bool:
    return clean_text(value).casefold() == KNOWN_PLACEHOLDER_SHA256


def transport_url(value: str) -> str:
    """Serialize the page-referenced Unicode URL for urllib transport only."""
    parsed = urlparse(value)
    return urlunparse(
        parsed._replace(path=quote(unquote(parsed.path), safe="/%:@"))
    )


def reused_trial_photo(name: str) -> Path | None:
    if name not in REUSED_SUCCESS_NAMES:
        return None
    matches = sorted(
        path
        for path in TRIAL_PHOTO_DIR.glob(f"{name}-*")
        if path.is_file()
    )
    if len(matches) != 1:
        raise RuntimeError(
            f"既有成功样本文件不唯一：{name} 数量={len(matches)}"
        )
    return matches[0]


class GdskinPhysicianPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.image_attrs: list[dict[str, str]] = []
        self.image_snippets: list[str] = []
        self._in_title = False
        self._title_parts: list[str] = []

    @property
    def page_title(self) -> str:
        return clean_text(" ".join(self._title_parts))

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        lowered = tag.lower()
        if lowered == "title":
            self._in_title = True
            return
        if lowered != "img":
            return
        self.image_attrs.append(
            {name.lower(): str(value or "") for name, value in attrs}
        )
        self.image_snippets.append(clean_text(self.get_starttag_text()))

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)


def inspect_portrait_reference(
    html: str, source_link: str, expected_name: str
) -> tuple[str, base.PortraitReference | None]:
    source_id = detail_id(source_link)
    if not source_id:
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    parser = GdskinPhysicianPageParser()
    parser.feed(html)
    title_core = parser.page_title.split("__", 1)[0].strip()
    expected = clean_text(expected_name)
    if not title_core or title_core.count(expected) != 1:
        raise RuntimeError(
            f"详情姓名与底表不一致：底表={expected_name} 官网标题={title_core or '空'} {source_link}"
        )

    candidates: list[tuple[dict[str, str], str, str]] = []
    for attrs, snippet in zip(parser.image_attrs, parser.image_snippets, strict=True):
        absolute = authorized_photo_candidate(attrs.get("src"), source_link)
        if absolute:
            candidates.append((attrs, snippet, absolute))
    if not candidates:
        return "无照片容器", None
    if len(candidates) != 1:
        raise RuntimeError(
            f"/uploadimg/ 正文 img 容器不唯一：{source_link} 数量={len(candidates)}"
        )

    attrs, snippet, absolute = candidates[0]
    marker_reason = placeholder_marker_reason(absolute)
    if marker_reason:
        PLACEHOLDER_EVIDENCE.clear()
        PLACEHOLDER_EVIDENCE.update(
            {
                "name": expected,
                "detail_id": source_id,
                "source_link": source_link,
                "page_title": title_core,
                "html_snippet": snippet,
                "raw_src": str(attrs.get("src") or "").strip(),
                "photo_url": absolute,
                "marker_reason": marker_reason,
                "decision": "占位图",
                "observed_utc": framework.utc_now(),
            }
        )
        return "占位图", None

    normalized = page_referenced_photo_url(attrs.get("src"), source_link)
    if not normalized:
        raise RuntimeError(f"页面引用照片 URL 越界：{source_link} {attrs.get('src', '')}")
    cached_path = reused_trial_photo(expected)
    if cached_path is not None:
        PHOTO_CACHE_BY_URL[normalized] = cached_path
    framework.STRUCTURE_EVIDENCE[source_link] = {
        "name": expected,
        "entry_id": SCOPE_ENTRY_BY_SOURCE.get(source_link, ""),
        "detail_id": source_id,
        "page_title": title_core,
        "container_selector": "unique img[src] resolving under /uploadimg/",
        "container_count": 1,
        "html_snippet": snippet,
        "raw_src": str(attrs.get("src") or "").strip(),
        "normalized_photo_url": normalized,
        "decoded_query_values": framework.decoded_query_values(normalized),
        "excluded_resource_examples": list(EXCLUDED_RESOURCE_EXAMPLES),
        "decision_basis": (
            "only the unique page-referenced img src resolving under /uploadimg/ "
            "is eligible; WebResource, filing icon and all site decorations are excluded"
        ),
        "photo_bytes_reused_from_prior_attempt": cached_path is not None,
        "observed_utc": framework.utc_now(),
    }
    return "", base.PortraitReference(
        page_title=title_core,
        photo_url=normalized,
        source_attribute="unique body img src under /uploadimg/",
    )


class GdskinOfficialSession(_BaseOfficialSession):
    """Owner-approved browser-UA session with a hard serial 2-second floor."""

    def __init__(self) -> None:
        super().__init__()
        self._last_started_at: float | None = None

    def _wait_for_slot(self) -> float | None:
        now = time.monotonic()
        if self._last_started_at is None:
            self._last_started_at = now
            return None
        remaining = REQUEST_INTERVAL_SECONDS - (now - self._last_started_at)
        while remaining > 0:
            time.sleep(remaining)
            now = time.monotonic()
            remaining = REQUEST_INTERVAL_SECONDS - (now - self._last_started_at)
        interval = now - self._last_started_at
        self._last_started_at = now
        return interval

    def get(self, url: str, referer: str = "") -> tuple[int, str, str, bytes]:
        cached_path = PHOTO_CACHE_BY_URL.get(url)
        if cached_path is not None:
            content = cached_path.read_bytes()
            suffix = cached_path.suffix.lower().lstrip(".")
            declared_type = {
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "png": "image/png",
                "gif": "image/gif",
                "webp": "image/webp",
            }.get(suffix, "")
            extension = base.magic_extension(content, declared_type)
            if not extension or extension != ("jpg" if suffix == "jpeg" else suffix):
                raise RuntimeError(f"既有成功样本魔数/扩展名漂移：{cached_path.name}")
            content_type = declared_type
            REUSE_TRACE.append(
                {
                    "sequence": len(REUSE_TRACE) + 1,
                    "name": cached_path.name.split("-", 1)[0],
                    "photo_url": url,
                    "disk_path": repo_relative(cached_path),
                    "bytes": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "observed_utc": framework.utc_now(),
                }
            )
            return 200, content_type, "utf-8", content
        interval = self._wait_for_slot()
        serialized_url = transport_url(url)
        REQUEST_TRACE.append(
            {
                "sequence": len(REQUEST_TRACE) + 1,
                "url": url,
                "transport_url": serialized_url,
                "interval_seconds_from_previous": (
                    None if interval is None else round(interval, 6)
                ),
                "observed_utc": framework.utc_now(),
            }
        )
        return super().get(serialized_url, referer)


def collect_known_placeholder_evidence(session: GdskinOfficialSession) -> None:
    status, content_type, charset, content = session.get(
        KNOWN_PLACEHOLDER_DETAIL_URL, DIRECTORY_URL
    )
    if status != 200 or content_type != "text/html":
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] "
            f"已知占位判例详情不可达：status={status} type={content_type}"
        )
    html = content.decode(charset, errors="replace")
    state, portrait = inspect_portrait_reference(
        html, KNOWN_PLACEHOLDER_DETAIL_URL, KNOWN_PLACEHOLDER_NAME
    )
    if state != "占位图" or portrait is not None or not PLACEHOLDER_EVIDENCE:
        raise RuntimeError("已知占位判例未命中正文 img 文件名门禁")
    photo_url = clean_text(PLACEHOLDER_EVIDENCE.get("photo_url"))
    photo_status, photo_type, _, photo = session.get(
        photo_url, KNOWN_PLACEHOLDER_DETAIL_URL
    )
    digest = hashlib.sha256(photo).hexdigest()
    if photo_status != 200 or not is_known_placeholder_digest(digest):
        raise RuntimeError(
            "[FATAL - HUMAN_INTERVENTION_REQUIRED] "
            f"已知占位判例字节漂移：status={photo_status} sha256={digest}"
        )
    width, height = base.image_dimensions(photo)
    PLACEHOLDER_EVIDENCE.update(
        {
            "photo_http_status": photo_status,
            "content_type": photo_type,
            "bytes": len(photo),
            "sha256": digest,
            "width": width,
            "height": height,
            "known_sha_match": True,
            "downloaded_for_gate_only": True,
            "written_to_disk": False,
        }
    )


def reachability_preflight(
    session: GdskinOfficialSession,
    sample_detail_url: str,
    interval_seconds: int = framework.REACHABILITY_RETRY_INTERVAL_SECONDS,
) -> list[dict[str, Any]]:
    observations = _framework_reachability_preflight(
        session, sample_detail_url, interval_seconds
    )
    collect_known_placeholder_evidence(session)
    return observations


def assert_placeholder_gates(samples: list[dict[str, Any]]) -> None:
    for sample in samples:
        if is_known_placeholder_digest(sample.get("sha256")):
            raise RuntimeError(
                "[FATAL - HUMAN_INTERVENTION_REQUIRED] "
                f"{sample.get('name')} 命中站方已知占位 SHA"
            )
        reason = placeholder_marker_reason(clean_text(sample.get("photo_url")))
        if reason:
            raise RuntimeError(
                "[FATAL - HUMAN_INTERVENTION_REQUIRED] "
                f"{sample.get('name')} 命中占位 URL 门禁：{reason}"
            )
    _framework_assert_placeholder_gates(samples)


def load_scope_rows() -> list[dict[str, Any]]:
    payload = json.loads(base.MASTER_JSON_PATH.read_text(encoding="utf-8"))
    rows = [
        dict(row)
        for row in payload.get("rows", [])
        if clean_text(row.get("医院")) == HOSPITAL
    ]
    if len(rows) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError(
            f"Issue #{ISSUE_NUMBER} 范围漂移：应为 {EXPECTED_SCOPE_COUNT} 行，实际 {len(rows)} 行"
        )
    if any(
        clean_text(row.get("照片链接")) or clean_text(row.get("照片文件"))
        for row in rows
    ):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} TRIAL 范围内已有照片字段")
    sources = [clean_text(row.get("来源链接")) for row in rows]
    if len(sources) != len(set(sources)):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} 范围来源链接不唯一")
    invalid_sources = [source for source in sources if not detail_id(source)]
    if invalid_sources:
        raise RuntimeError("范围存在非授权详情链接：" + "、".join(invalid_sources[:5]))
    actual_entries = Counter(entry_id(row.get("采集入口")) for row in rows)
    if actual_entries != Counter(ENTRY_COUNTS):
        raise RuntimeError(
            f"Issue #{ISSUE_NUMBER} 分类入口分布漂移：{dict(actual_entries)}"
        )
    SCOPE_ENTRY_BY_SOURCE.clear()
    SCOPE_ENTRY_BY_SOURCE.update(
        {
            clean_text(row.get("来源链接")): entry_id(row.get("采集入口"))
            for row in rows
        }
    )
    return rows


def select_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for expected_name, expected_level, expected_entry in SAMPLE_PLAN:
        matches = [
            row for row in rows if clean_text(row.get("姓名")) == expected_name
        ]
        if len(matches) != 1:
            raise RuntimeError(f"试采姓名范围不唯一：{expected_name} 数量={len(matches)}")
        row = dict(matches[0])
        actual_level = base.title_level(row.get("职称身份原文"))
        actual_entry = entry_id(row.get("采集入口"))
        if actual_level != expected_level or actual_entry != expected_entry:
            raise RuntimeError(
                f"试采分层漂移：{expected_name} 应为 {expected_entry}/{expected_level} "
                f"实际 {actual_entry}/{actual_level}"
            )
        result.append(row)
    counts = Counter(base.title_level(row.get("职称身份原文")) for row in result)
    actual_counts = {level: counts[level] for level in EXPECTED_TITLE_COUNTS}
    covered_entries = {entry_id(row.get("采集入口")) for row in result}
    if covered_entries != set(ENTRY_COUNTS):
        raise RuntimeError(f"试采未覆盖全部 9 个分类入口：{sorted(covered_entries)}")
    if actual_counts != EXPECTED_TITLE_COUNTS:
        raise RuntimeError(f"职称分层覆盖漂移：{actual_counts}")
    if set(counts) != set(EXPECTED_TITLE_COUNTS):
        raise RuntimeError(f"试采出现未授权职称层：{dict(counts)}")
    return result


def normalize_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    result = dict(snapshot)
    result["master_assets"] = {
        repo_relative(Path(path)): facts
        for path, facts in snapshot["master_assets"].items()
    }
    return result


def normalize_payload_paths(payload: dict[str, Any]) -> dict[str, Any]:
    for sample in payload["photo_samples"]:
        sample["disk_path"] = repo_relative(Path(sample["disk_path"]))
    meta = payload["meta"]
    meta["protected_assets_before"] = normalize_snapshot(
        meta["protected_assets_before"]
    )
    meta["protected_assets_after"] = normalize_snapshot(
        meta["protected_assets_after"]
    )
    meta["trial_photo_dir"] = repo_relative(TRIAL_PHOTO_DIR)
    meta["json_path"] = repo_relative(TRIAL_JSON_PATH)
    meta["csv_path"] = repo_relative(TRIAL_CSV_PATH)
    meta["report_path"] = repo_relative(TRIAL_REPORT_PATH)
    meta["contact_sheet_path"] = repo_relative(CONTACT_SHEET_PATH)
    return payload


def enrich_payload(payload: dict[str, Any]) -> dict[str, Any]:
    payload = _framework_enrich_payload(payload)
    for sample in payload["photo_samples"]:
        sample["entry_id"] = SCOPE_ENTRY_BY_SOURCE.get(sample["source_link"], "")
        sample["reused_from_prior_attempt"] = sample["name"] in REUSED_SUCCESS_NAMES
    normalize_payload_paths(payload)
    intervals = [
        item["interval_seconds_from_previous"]
        for item in REQUEST_TRACE
        if item["interval_seconds_from_previous"] is not None
    ]
    meta = payload["meta"]
    meta["entry_coverage_count"] = len(
        {sample["entry_id"] for sample in payload["photo_samples"]}
    )
    meta["covered_entry_ids"] = sorted(
        {sample["entry_id"] for sample in payload["photo_samples"]}
    )
    meta["historical_department_fields_empty"] = True
    meta["known_placeholder_gate_verified"] = bool(
        PLACEHOLDER_EVIDENCE.get("known_sha_match")
    )
    meta["known_placeholder_gate_hits_in_samples"] = 0
    meta["serial_request_interval_seconds"] = REQUEST_INTERVAL_SECONDS
    meta["serial_request_count"] = len(REQUEST_TRACE)
    meta["minimum_observed_request_interval_seconds"] = min(intervals)
    meta["reused_photo_count"] = len(REUSE_TRACE)
    meta["newly_downloaded_photo_count"] = sum(
        not sample["reused_from_prior_attempt"]
        for sample in payload["photo_samples"]
    )
    meta["prior_failure_evidence_count"] = len(PRIOR_FAILURE_EVIDENCE)
    meta["replacement_candidate_evidence_count"] = len(
        REPLACEMENT_CANDIDATE_EVIDENCE
    )
    meta["repository_relative_paths_only"] = True
    meta["artifact_hash_policy"] = "repository_blob_lf"
    payload["known_placeholder_evidence"] = dict(PLACEHOLDER_EVIDENCE)
    payload["serial_request_trace"] = list(REQUEST_TRACE)
    payload["reused_photo_trace"] = list(REUSE_TRACE)
    payload["replacement_matrix"] = [dict(item) for item in REPLACEMENT_MATRIX]
    payload["prior_failure_evidence"] = [
        dict(item) for item in PRIOR_FAILURE_EVIDENCE
    ]
    payload["replacement_candidate_evidence"] = [
        dict(item) for item in REPLACEMENT_CANDIDATE_EVIDENCE
    ]
    return payload


def validate_payload(payload: dict[str, Any]) -> None:
    _framework_validate_payload(payload)
    meta = payload["meta"]
    errors: list[str] = []
    if meta.get("entry_coverage_count") != len(ENTRY_COUNTS):
        errors.append("TRIAL 未覆盖全部 9 个分类入口")
    if meta.get("covered_entry_ids") != sorted(ENTRY_COUNTS):
        errors.append("TRIAL 分类入口集合漂移")
    if meta.get("known_placeholder_gate_verified") is not True:
        errors.append("站方已知占位 SHA 判例未验证")
    evidence = payload.get("known_placeholder_evidence", {})
    if (
        evidence.get("detail_id") != "5566"
        or evidence.get("marker_reason") != "explicit_chinese_placeholder_filename"
        or evidence.get("sha256") != KNOWN_PLACEHOLDER_SHA256
        or evidence.get("known_sha_match") is not True
        or evidence.get("written_to_disk") is not False
    ):
        errors.append("已知占位判例证据不完整")
    trace = payload.get("serial_request_trace", [])
    intervals = [
        item.get("interval_seconds_from_previous")
        for item in trace
        if item.get("interval_seconds_from_previous") is not None
    ]
    if (
        meta.get("serial_request_count") != EXPECTED_NETWORK_REQUEST_COUNT
        or len(trace) != EXPECTED_NETWORK_REQUEST_COUNT
    ):
        errors.append(
            f"串行网络请求留痕数量不是 {EXPECTED_NETWORK_REQUEST_COUNT}：{len(trace)}"
        )
    if not intervals or any(value < REQUEST_INTERVAL_SECONDS for value in intervals):
        errors.append("串行请求间隔存在小于 2 秒")
    reuse_trace = payload.get("reused_photo_trace", [])
    if meta.get("reused_photo_count") != EXPECTED_REUSE_COUNT or len(
        reuse_trace
    ) != EXPECTED_REUSE_COUNT:
        errors.append(
            f"既有成功照片复用数不是 {EXPECTED_REUSE_COUNT}：{len(reuse_trace)}"
        )
    if {item.get("name") for item in reuse_trace} != set(REUSED_SUCCESS_NAMES):
        errors.append("既有成功照片复用姓名集合漂移")
    if meta.get("newly_downloaded_photo_count") != EXPECTED_NEW_DOWNLOAD_COUNT:
        errors.append(
            f"新替换照片下载数不是 {EXPECTED_NEW_DOWNLOAD_COUNT}"
        )
    replacements = payload.get("replacement_matrix", [])
    if replacements != [dict(item) for item in REPLACEMENT_MATRIX]:
        errors.append("替换对照表漂移")
    failures = payload.get("prior_failure_evidence", [])
    if failures != [dict(item) for item in PRIOR_FAILURE_EVIDENCE]:
        errors.append("三条原样本失败证据漂移")
    if {item.get("failure_state") for item in failures} != {
        "无照片容器",
        "照片资源不可达",
    }:
        errors.append("失败四类口径漂移")
    meng = next(
        (item for item in failures if item.get("name") == "孟凡琪"), {}
    )
    if (
        "\u00a0 \u00a0" not in meng.get("raw_photo_reference", "")
        or "%C2%A0%20%C2%A0.jpg" not in meng.get("transport_url", "")
        or meng.get("photo_http_status") != 404
    ):
        errors.append("孟凡琪 NBSP 悬空引用证据不完整")
    candidate_evidence = payload.get("replacement_candidate_evidence", [])
    if candidate_evidence != [dict(item) for item in REPLACEMENT_CANDIDATE_EVIDENCE]:
        errors.append("替代候选失败证据漂移")
    for name in ("龚洋洋", "郭先荟"):
        item = next(
            (row for row in candidate_evidence if row.get("name") == name), {}
        )
        if (
            "\u00a0" not in item.get("raw_photo_reference", "")
            or "%C2%A0.jpg" not in item.get("transport_url", "")
            or item.get("photo_http_status") != 404
        ):
            errors.append(f"{name} NBSP 悬空引用证据不完整")
    if meta.get("repository_relative_paths_only") is not True:
        errors.append("工件未声明仅使用仓库相对路径")
    if meta.get("artifact_hash_policy") != "repository_blob_lf":
        errors.append("工件哈希政策不是 repository_blob_lf")
    diagnostics = payload.get("structure_diagnostics", [])
    if len(diagnostics) != EXPECTED_TRIAL_COUNT:
        errors.append("正文 img 结构诊断不是 10 条")
    if any(
        not clean_text(item.get("html_snippet")).startswith("<img")
        or "/uploadimg/" not in unquote(
            urlparse(clean_text(item.get("normalized_photo_url"))).path
        ).casefold()
        for item in diagnostics
    ):
        errors.append("容器诊断不是唯一 /uploadimg/ 正文 img")
    serialized = json.dumps(payload, ensure_ascii=False)
    if str(ROOT) in serialized or ROOT.as_posix() in serialized:
        errors.append("payload 泄漏仓库绝对路径")
    for sample in payload.get("photo_samples", []):
        path = Path(sample["disk_path"])
        if path.is_absolute() or not (ROOT / path).is_file():
            errors.append(f"照片路径不是有效仓库相对路径：{path}")
        if placeholder_marker_reason(clean_text(sample.get("photo_url"))):
            errors.append(f"实采样本 URL 命中占位标记：{sample.get('name')}")
        if is_known_placeholder_digest(sample.get("sha256")):
            errors.append(f"实采样本命中已知占位 SHA：{sample.get('name')}")
    if {
        sample.get("name")
        for sample in payload.get("photo_samples", [])
        if sample.get("reused_from_prior_attempt")
    } != set(REUSED_SUCCESS_NAMES):
        errors.append("payload 复用标记姓名集合漂移")
    if errors:
        raise RuntimeError(
            f"Issue #{ISSUE_NUMBER} TRIAL 工程门禁失败：" + "；".join(errors)
        )


def manifest_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = _framework_manifest_rows(payload)
    by_source = {
        sample["source_link"]: sample.get("entry_id", "")
        for sample in payload["photo_samples"]
    }
    for row in rows:
        row["分类入口ID"] = by_source.get(row["来源链接"], "")
    return rows


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|").replace("\n", " ")


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    samples = "\n".join(
        "| {entry_id} | {name} | {title_level} | {source_link} | {photo_url} | "
        "{content_type} | {actual_extension} | {width}×{height} | {bytes} | {reused} | {sha256} |".format(
            reused=("复用" if sample["reused_from_prior_attempt"] else "新下载"),
            **{key: markdown_cell(value) for key, value in sample.items()}
        )
        for sample in payload["photo_samples"]
    )
    diagnostics = "\n".join(
        "| {entry_id} | {name} | {detail_id} | `{html}` | {basis} |".format(
            entry_id=markdown_cell(item.get("entry_id")),
            name=markdown_cell(item.get("name")),
            detail_id=markdown_cell(item.get("detail_id")),
            html=markdown_cell(item.get("html_snippet")),
            basis=markdown_cell(item.get("decision_basis")),
        )
        for item in payload["structure_diagnostics"]
    )
    replacements = "\n".join(
        "| {original_name} | {replacement_name} | {entry_id} | {original_title_level}→{replacement_title_level} | {reason} |".format(
            **{key: markdown_cell(value) for key, value in item.items()}
        )
        for item in payload["replacement_matrix"]
    )
    failures = "\n".join(
        "| {name} | {entry_id} | {detail_id} | {failure_state} | {references} | `{raw}` | `{transport}` | {photo_status} | {feature} | {observed} |".format(
            name=markdown_cell(item.get("name")),
            entry_id=markdown_cell(item.get("entry_id")),
            detail_id=markdown_cell(item.get("detail_id")),
            failure_state=markdown_cell(item.get("failure_state")),
            references=markdown_cell(item.get("page_referenced_photo_count")),
            raw=markdown_cell(item.get("raw_photo_reference", "-")),
            transport=markdown_cell(item.get("transport_url", "-")),
            photo_status=markdown_cell(item.get("photo_http_status", "-")),
            feature=markdown_cell(item.get("decision_feature")),
            observed=markdown_cell(item.get("observed_utc")),
        )
        for item in payload["prior_failure_evidence"]
    )
    candidate_failures = "\n".join(
        "| {name} | {entry_id} | {detail_id} | {failure_state} | {references} | `{raw}` | `{transport}` | {photo_status} | {feature} | {observed} |".format(
            name=markdown_cell(item.get("name")),
            entry_id=markdown_cell(item.get("entry_id")),
            detail_id=markdown_cell(item.get("detail_id")),
            failure_state=markdown_cell(item.get("failure_state")),
            references=markdown_cell(item.get("page_referenced_photo_count")),
            raw=markdown_cell(item.get("raw_photo_reference", "-")),
            transport=markdown_cell(item.get("transport_url", "-")),
            photo_status=markdown_cell(item.get("photo_http_status", "-")),
            feature=markdown_cell(item.get("decision_feature")),
            observed=markdown_cell(item.get("observed_utc")),
        )
        for item in payload["replacement_candidate_evidence"]
    )
    protected = []
    for path, facts in meta["protected_assets_before"]["master_assets"].items():
        protected.append(
            f"| `{path}` | {facts['bytes']} | `{facts['sha256']}` |"
        )
    evidence = payload["known_placeholder_evidence"]
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL} 照片补录 TRIAL 报告

## 授权与范围

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/{ISSUE_NUMBER}>
- Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
- 医院官网：<{OFFICIAL_HOME}>
- 代表医生目录：<{DIRECTORY_URL}>
- 固定范围：{meta['scope_count']} 行；来源链接唯一 {meta['scope_unique_source_count']} 条；照片双列在 TRIAL 前均为空。
- 历史科室字段为空，按 Issue 要求改以分类入口分层；本样本覆盖 {meta['entry_coverage_count']}/9 个入口：{', '.join(meta['covered_entry_ids'])}。
- 职称层级：{json.dumps(meta['title_level_counts'], ensure_ascii=False)}。

## 串行访问与结构诊断

- 固定浏览器 UA；无 Cookie、无代理、无并发；请求间隔下限 {meta['serial_request_interval_seconds']} 秒。
- 本轮共 {meta['serial_request_count']} 次官网网络请求，实测最小相邻启动间隔 {meta['minimum_observed_request_interval_seconds']:.6f} 秒。
- 既有成功照片复用 {meta['reused_photo_count']} 张，不重新下载；本轮仅新下载 {meta['newly_downloaded_photo_count']} 张替换照片。
- 页面唯一 `/uploadimg/` 正文 `img src` 才可进入候选；WebResource、备案图标及 logo/banner/nav/foot 全部排除。
- 页面引用照片原始字节直接保存，不压缩、不转码、不构造未引用路径。

| 分类入口 | 姓名 | 详情 ID | 正文 img HTML | 判定依据 |
|---|---|---:|---|---|
{diagnostics}

## 已知占位判例

- 文海泉详情：<{evidence['source_link']}>，页面实际引用：<{evidence['photo_url']}>。
- 文件名明文门禁：`{evidence['marker_reason']}`；HTTP {evidence['photo_http_status']}，{evidence['bytes']} bytes，{evidence['width']}×{evidence['height']}。
- SHA-256：`{evidence['sha256']}`，与 Owner 指定 known-SHA 一致：`{evidence['known_sha_match']}`。
- 该字节仅用于门禁取证，未写入磁盘、未计入 10 位实采样本。

## Owner 裁决后的替换对照

| 原样本 | 替换人 | 入口 | 职称层变化 | 替换理由 |
|---|---|---:|---|---|
{replacements}

最终 10 人分层按 Owner 裁决以实际构成为准：{json.dumps(meta['title_level_counts'], ensure_ascii=False)}；入口覆盖保持 9/9。

## 原样本失败证据行

| 姓名 | 入口 | 详情ID | 失败类 | 页面引用数 | 页面原引用 | 编码传输URL | 照片HTTP | 判定特征 | UTC |
|---|---:|---:|---|---:|---|---|---:|---|---|
{failures}

孟凡琪证据同时保留含 NBSP 的页面原引用与标准百分号编码 URL；未构造、未探测任何路径变体。

### 替代候选失败留档（供 FULL）

| 姓名 | 入口 | 详情ID | 失败类 | 页面引用数 | 页面原引用 | 编码传输URL | 照片HTTP | 判定特征 | UTC |
|---|---:|---:|---|---:|---|---|---:|---|---|
{candidate_failures}

龚洋洋、郭先荟证据均保留 NBSP 页面引用与仅用于传输的百分号编码 URL；与孟凡琪共同构成本站 NBSP 尾缀悬空判例。于碧慧保留无照片容器证据。

## 10 位实采结果

- 10/10 详情 HTTP 200，10/10 照片 HTTP 200，失败与结构异常共 {meta['fuse_problem_count']}。
- 总字节 {meta['photo_total_bytes']}，平均 {meta['photo_average_bytes']}；预计全院 77 行约 {meta['estimated_full_mib']:.2f} MiB。
- >5 MiB：{meta['over_5mib_count']}；>20 MiB：{meta['over_20mib_count']}；跨医生重复 SHA：{meta['cross_doctor_duplicate_sha_groups']}。
- 联系表：`{meta['contact_sheet_path']}`；当前视觉状态：`{meta['visual_review_status']}`。

| 入口 | 姓名 | 层级 | 详情页 | 页面引用照片 | 声明类型 | 实际格式 | 尺寸 | 字节 | 来源 | SHA-256 |
|---|---|---|---|---|---|---|---:|---:|---|---|
{samples}

## 工程与保护门禁

1. ROOT 由 `Path(__file__).resolve().parents[1]` 定位；payload/manifest/report 只记录仓库相对路径。
2. 引用工件哈希按仓库 blob（文本 CRLF→LF，二进制原字节）口径计算。
3. 中文“占位”文件名、known-SHA、query Base64、近单色、跨医生同 SHA、灰底拼图空白/不可见格均拦截。

| 受保护文件 | 字节 | SHA-256 |
|---|---:|---|
{chr(10).join(protected)}

- 本院画像树：{meta['protected_assets_before']['profile_tree']['file_count']} 个文件，聚合 SHA-256 `{meta['protected_assets_before']['profile_tree']['sha256']}`。
- 正式照片树前后一致：`{json.dumps(meta['protected_assets_before']['formal_photo_tree'], ensure_ascii=False)}`。
- TRIAL 仅写 `work/` 工件，未回填总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件提交、推送并发布 `TRIAL_READY_FOR_OWNER_AUDIT` 后停止。未取得 Owner 在关联 PR 明确下发的 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填正式资产。
"""
    TRIAL_REPORT_PATH.write_text(report, encoding="utf-8")


def configure_framework() -> None:
    master_basename = "珠三角三甲医院_医生画像自动采集总底表"
    base_values = {
        "ROOT": ROOT,
        "WORK_DIR": WORK_DIR,
        "VAULT": VAULT,
        "SOURCE_DIR": SOURCE_DIR,
        "MASTER_JSON_PATH": WORK_DIR / f"{master_basename}_payload.json",
        "MASTER_CSV_PATH": SOURCE_DIR / f"{master_basename}.csv",
        "MASTER_XLSX_PATH": SOURCE_DIR / f"{master_basename}.xlsx",
        "MASTER_REPORT_PATH": SOURCE_DIR / f"{master_basename}_更新报告.md",
        "LEDGER_PATH": SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx",
    }
    for name, value in base_values.items():
        setattr(base, name, value)
    module_values = {
        "ROOT": ROOT,
        "WORK_DIR": WORK_DIR,
        "VAULT": VAULT,
        "SOURCE_DIR": SOURCE_DIR,
        "HOSPITAL": HOSPITAL,
        "ISSUE_NUMBER": ISSUE_NUMBER,
        "EXPECTED_SCOPE_COUNT": EXPECTED_SCOPE_COUNT,
        "EXPECTED_TRIAL_COUNT": EXPECTED_TRIAL_COUNT,
        "MIN_TRIAL_DEPARTMENTS": MIN_TRIAL_DEPARTMENTS,
        "OFFICIAL_HOME": OFFICIAL_HOME,
        "DIRECTORY_URL": DIRECTORY_URL,
        "OFFICIAL_HOST": OFFICIAL_HOST,
        "PHOTO_PREFIX": PHOTO_PREFIX,
        "PROFILE_DIR": PROFILE_DIR,
        "FORMAL_PHOTO_DIR": FORMAL_PHOTO_DIR,
        "TRIAL_BASENAME": TRIAL_BASENAME,
        "TRIAL_JSON_PATH": TRIAL_JSON_PATH,
        "TRIAL_CSV_PATH": TRIAL_CSV_PATH,
        "TRIAL_REPORT_PATH": TRIAL_REPORT_PATH,
        "CONTACT_SHEET_PATH": CONTACT_SHEET_PATH,
        "TRIAL_PHOTO_DIR": TRIAL_PHOTO_DIR,
        "EXPECTED_TITLE_COUNTS": EXPECTED_TITLE_COUNTS,
        "SAMPLE_PLAN": SAMPLE_PLAN,
        "EXCLUDED_RESOURCE_EXAMPLES": EXCLUDED_RESOURCE_EXAMPLES,
    }
    for name, value in module_values.items():
        setattr(framework, name, value)
    framework.detail_id = detail_id
    framework.page_referenced_photo_url = page_referenced_photo_url
    framework.inspect_portrait_reference = inspect_portrait_reference
    framework.OfficialSession = GdskinOfficialSession
    framework.reachability_preflight = reachability_preflight
    framework.assert_placeholder_gates = assert_placeholder_gates
    framework.load_scope_rows = load_scope_rows
    framework.select_trial_rows = select_trial_rows
    framework.enrich_payload = enrich_payload
    framework.validate_payload = validate_payload
    framework.manifest_rows = manifest_rows
    framework.write_report = write_report
    framework.configure_base()


def run_trial(run_date: str) -> dict[str, Any]:
    REQUEST_TRACE.clear()
    REUSE_TRACE.clear()
    PLACEHOLDER_EVIDENCE.clear()
    SCOPE_ENTRY_BY_SOURCE.clear()
    PHOTO_CACHE_BY_URL.clear()
    configure_framework()
    payload = enrich_payload(framework.collect_trial_payload(run_date))
    validate_payload(payload)
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    framework.write_manifest(payload)
    write_report(payload)
    return payload


def mark_visual_pass() -> dict[str, Any]:
    configure_framework()
    payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
    validate_payload(payload)
    payload["meta"]["visual_review_status"] = (
        "PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS"
    )
    payload["meta"]["visual_reviewed_utc"] = framework.utc_now()
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    framework.write_manifest(payload)
    write_report(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Issue #{ISSUE_NUMBER} {HOSPITAL} photo-backfill TRIAL"
    )
    parser.add_argument("--run-date", default=date.today().isoformat())
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--mark-visual-pass", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_framework()
    if args.mark_visual_pass:
        payload = mark_visual_pass()
    elif args.validate:
        payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
        validate_payload(payload)
    else:
        payload = run_trial(args.run_date)
    print(
        "TRIAL_VALIDATED "
        f"scope={payload['meta']['scope_count']} "
        f"samples={payload['meta']['photo_sample_count']} "
        f"entries={payload['meta']['entry_coverage_count']} "
        f"visual={payload['meta']['visual_review_status']}"
    )


if __name__ == "__main__":
    main()
