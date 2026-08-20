from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

import collect_official_doctors_batch as collector


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
PROFILE_ROOT = VAULT / "01_试点医院"
MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_PAYLOAD = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_REPORT = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
LEDGER = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"

ISSUE_NUMBER = 87
PHASE = "TRIAL"
SYSUCC = "中山大学肿瘤防治中心"
ZSSY = "中山大学附属第三医院"
HOSPITALS = (SYSUCC, ZSSY)
EXPECTED_ROWS = 596
EXPECTED_BY_HOSPITAL = {SYSUCC: 506, ZSSY: 90}
EXPECTED_PROFILES = 242
EXPECTED_PROFILES_BY_HOSPITAL = {SYSUCC: 204, ZSSY: 38}
EXPECTED_ATYPICAL_PROFILES = 8
REQUEST_INTERVAL_SECONDS = 1.0

TRIAL_BASENAME = "GOVERN-2_导航文本污染清理_trial"
PAYLOAD_PATH = WORK_DIR / f"{TRIAL_BASENAME}_evidence.json"
MANIFEST_PATH = WORK_DIR / f"{TRIAL_BASENAME}_manifest.csv"
PROFILE_IMPACT_PATH = WORK_DIR / "GOVERN-2_导航文本污染清理_profile_impact.csv"
DOM_EVIDENCE_PATH = WORK_DIR / "GOVERN-2_导航文本污染清理_dom_evidence.csv"
REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_summary.md"

TEXT_EXTENSIONS = frozenset({".csv", ".json", ".md", ".py", ".txt", ".yaml", ".yml"})
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
)
OFFICIAL_HOSTS = {
    SYSUCC: "sysucc.org.cn",
    ZSSY: "zssy.com.cn",
}

SYSUCC_PROFILE_RE = re.compile(
    r"(?P<segment>(?P<label>临床专家|科研学者) 面包屑 首页 / "
    r"(?P<path>.+?) / (?P=label) (?P<site_title>[^ ]+) )"
)
SYSUCC_TRAINING_RE = re.compile(
    r"(?P<segment>住院医师规范化培训 面包屑 首页 / 医学教育 / "
    r"住院医师规范化培训 )"
)
ZSSY_RE = re.compile(
    r"(?P<segment>导航痕迹 首页 / (?P<expert>专家介绍 / )?"
    r"(?P<site_title>.+?) )(?=(?P=site_title) )"
)

MANIFEST_FIELDS = (
    "row_number",
    "sequence",
    "hospital",
    "name",
    "source_link",
    "original_length",
    "removed_segment",
    "removed_length",
    "remaining_length",
    "segment_start",
    "segment_end",
    "segment_position",
    "match_type",
    "site_title",
    "name_variant",
    "owner_atypical_profile_case",
    "quote_boundary_status",
    "original_sha256",
    "remaining_sha256",
)
PROFILE_FIELDS = (
    "hospital",
    "profile_path",
    "source_link",
    "master_row_number",
    "master_name",
    "marker_occurrences",
    "carrier_line_numbers",
    "carrier_sections",
    "non_detail_carrier",
    "owner_atypical_profile_case",
)
DOM_FIELDS = (
    "hospital",
    "name",
    "source_link",
    "http_status",
    "final_url",
    "selector",
    "dom_breadcrumb",
    "page_title",
    "removed_segment",
    "agreement",
    "observed_utc",
    "error",
)
DOM_SAMPLE_PLAN = (
    (SYSUCC, "丘惠娟", "https://www.sysucc.org.cn/node/3768"),
    (SYSUCC, "张蓓", "https://www.sysucc.org.cn/node/3773"),
    (SYSUCC, "卢雅立", "https://www.sysucc.org.cn/node/3829"),
    (SYSUCC, "谢丹", "https://www.sysucc.org.cn/node/1541"),
    (SYSUCC, "刘慧", "https://www.sysucc.org.cn/node/1658"),
    (SYSUCC, "郑利民", "https://www.sysucc.org.cn/node/1542"),
    (ZSSY, "刘慧", "https://www.zssy.com.cn/node/11033"),
    (ZSSY, "刘穗玲", "https://www.zssy.com.cn/node/15106"),
    (ZSSY, "余步云", "https://www.zssy.com.cn/node/14193"),
    (ZSSY, "变态反应", "https://www.zssy.com.cn/node/14098"),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def repo_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"工件路径越出仓库：{resolved}") from exc


def repository_digest_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data


def digest_path(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "file_count": 0, "bytes": 0, "sha256": ""}
    files = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
    digest = hashlib.sha256()
    raw_bytes = 0
    for item in files:
        data = repository_digest_bytes(item)
        relative = item.name if path.is_file() else item.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
        raw_bytes += item.stat().st_size
    return {
        "exists": True,
        "file_count": len(files),
        "bytes": raw_bytes,
        "sha256": digest.hexdigest(),
    }


def protected_snapshot() -> dict[str, Any]:
    paths = [LEDGER, MASTER_PAYLOAD, MASTER_CSV, MASTER_XLSX, MASTER_REPORT]
    paths.extend(PROFILE_ROOT / hospital for hospital in HOSPITALS)
    paths.extend(PROFILE_ROOT / hospital / "_索引.md" for hospital in HOSPITALS)
    return {repo_relative(path): digest_path(path) for path in paths}


def row_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def normalized_row(row: dict[str, Any]) -> dict[str, str]:
    return {header: row_value(row.get(header)) for header in collector.BASE_HEADERS}


def load_current_layers() -> list[dict[str, str]]:
    payload = json.loads(MASTER_PAYLOAD.read_text(encoding="utf-8"))
    payload_rows = payload.get("rows")
    if not isinstance(payload_rows, list) or not payload_rows:
        raise RuntimeError("主 payload 缺少有效 rows")
    with MASTER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    xlsx_rows = collector.read_bottom_table_rows(MASTER_XLSX)
    if not (len(payload_rows) == len(csv_rows) == len(xlsx_rows)):
        raise RuntimeError(
            f"三载体行数不一致：payload={len(payload_rows)}、CSV={len(csv_rows)}、XLSX={len(xlsx_rows)}"
        )
    for row_number, (payload_row, csv_row, xlsx_row) in enumerate(
        zip(payload_rows, csv_rows, xlsx_rows, strict=True), start=2
    ):
        expected = normalized_row(payload_row)
        if normalized_row(csv_row) != expected or normalized_row(xlsx_row) != expected:
            raise RuntimeError(f"三载体在底表第 {row_number} 行不一致")
    return [{key: row_value(value) for key, value in row.items()} for row in csv_rows]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def strip_navigation(text: str, hospital: str) -> dict[str, Any] | None:
    patterns: list[tuple[re.Pattern[str], str]]
    if hospital == SYSUCC:
        patterns = [
            (SYSUCC_PROFILE_RE, "SYSUCC_PROFILE"),
            (SYSUCC_TRAINING_RE, "SYSUCC_TRAINING_PAGE"),
        ]
    elif hospital == ZSSY:
        patterns = [(ZSSY_RE, "ZSSY")]
    else:
        return None

    matches: list[tuple[re.Match[str], str]] = []
    for pattern, family in patterns:
        matches.extend((match, family) for match in pattern.finditer(text))
    if not matches:
        return None
    if len(matches) != 1:
        raise RuntimeError(f"导航段命中不唯一：hospital={hospital} count={len(matches)}")

    match, family = matches[0]
    segment = match.group("segment")
    start, end = match.span("segment")
    remaining = text[:start] + text[end:]
    groups = match.groupdict()
    if family == "SYSUCC_PROFILE":
        label = groups.get("label") or ""
        match_type = (
            "SYSUCC_CLINICAL_EXPERT" if label == "临床专家" else "SYSUCC_RESEARCH_SCHOLAR"
        )
    elif family == "SYSUCC_TRAINING_PAGE":
        match_type = family
    else:
        match_type = "ZSSY_EXPERT" if groups.get("expert") else "ZSSY_DEPARTMENT"
    quote_before = start > 0 and text[start - 1] in {"'", "’", "‘"}
    return {
        "removed_segment": segment,
        "remaining": remaining,
        "segment_start": start,
        "segment_end": end,
        "segment_position": "START" if start == 0 else "MIDDLE",
        "match_type": match_type,
        "site_title": groups.get("site_title") or "",
        "quote_boundary_status": (
            "ISOLATED_QUOTE_PRESERVED_PENDING_OWNER" if quote_before else "NO_ADJACENT_QUOTE"
        ),
    }


def affected_master_manifest(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    manifest: list[dict[str, Any]] = []
    for row_number, row in enumerate(rows, start=2):
        text = row.get("详情正文摘录", "")
        has_marker = "面包屑" in text or "导航痕迹" in text
        if not has_marker:
            continue
        hospital = row.get("医院", "")
        result = strip_navigation(text, hospital)
        if result is None:
            raise RuntimeError(f"底表第 {row_number} 行导航污染无法唯一试算")
        remaining = result.pop("remaining")
        if "面包屑" in remaining or "导航痕迹" in remaining:
            raise RuntimeError(f"底表第 {row_number} 行试算后仍有导航标记")
        if len(text) - len(result["removed_segment"]) != len(remaining):
            raise RuntimeError(f"底表第 {row_number} 行长度不闭合")
        site_title = result.get("site_title", "")
        name = row.get("姓名", "")
        manifest.append(
            {
                "row_number": row_number,
                "sequence": row.get("序号", ""),
                "hospital": hospital,
                "name": name,
                "source_link": row.get("来源链接", ""),
                "original_length": len(text),
                "removed_length": len(result["removed_segment"]),
                "remaining_length": len(remaining),
                "name_variant": "YES" if site_title and site_title != name else "NO",
                "owner_atypical_profile_case": "NO",
                "original_sha256": sha256_text(text),
                "remaining_sha256": sha256_text(remaining),
                **result,
            }
        )
    return manifest


def source_link_from_profile(text: str) -> str:
    match = re.search(r'^来源链接:\s*["\']?([^"\'\r\n]+)["\']?\s*$', text, re.MULTILINE)
    return clean_text(match.group(1)) if match else ""


def carrier_section(lines: list[str], line_index: int) -> str:
    for index in range(line_index - 1, -1, -1):
        if lines[index].startswith("#"):
            return lines[index]
    return ""


def profile_impact_inventory(
    manifest: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    master_by_source = {item["source_link"]: item for item in manifest}
    inventory: list[dict[str, Any]] = []
    atypical: list[dict[str, Any]] = []
    for hospital in HOSPITALS:
        hospital_dir = PROFILE_ROOT / hospital
        for path in sorted(hospital_dir.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            if "面包屑" not in text and "导航痕迹" not in text:
                continue
            lines = text.splitlines()
            hits: list[dict[str, Any]] = []
            for index, line in enumerate(lines):
                marker_count = line.count("面包屑") + line.count("导航痕迹")
                if not marker_count:
                    continue
                hits.append(
                    {
                        "line_number": index + 1,
                        "section": carrier_section(lines, index),
                        "line": line,
                        "marker_count": marker_count,
                    }
                )
            source_link = source_link_from_profile(text)
            master = master_by_source.get(source_link)
            common_sysucc = (
                hospital == SYSUCC
                and len(hits) == 1
                and hits[0]["line"].lstrip("- ").startswith("临床专家 面包屑")
            )
            is_atypical = hospital == SYSUCC and not common_sysucc
            item = {
                "hospital": hospital,
                "profile_path": repo_relative(path),
                "source_link": source_link,
                "master_row_number": master.get("row_number", "") if master else "",
                "master_name": master.get("name", "") if master else "",
                "marker_occurrences": sum(hit["marker_count"] for hit in hits),
                "carrier_line_numbers": ";".join(str(hit["line_number"]) for hit in hits),
                "carrier_sections": ";".join(dict.fromkeys(hit["section"] for hit in hits)),
                "non_detail_carrier": (
                    "YES" if any(hit["section"] != "## 详情正文摘录" for hit in hits) else "NO"
                ),
                "owner_atypical_profile_case": "YES" if is_atypical else "NO",
            }
            inventory.append(item)
            if is_atypical:
                atypical.append(
                    {
                        **item,
                        "carrier_evidence": [
                            {
                                "line_number": hit["line_number"],
                                "section": hit["section"],
                                "marker_context": clean_text(hit["line"])[:500],
                            }
                            for hit in hits
                        ],
                    }
                )
    atypical_sources = {item["source_link"] for item in atypical}
    for item in manifest:
        if item["source_link"] in atypical_sources:
            item["owner_atypical_profile_case"] = "YES"
    return inventory, atypical


class RateLimitedSession(requests.Session):
    def __init__(self, interval_seconds: float = REQUEST_INTERVAL_SECONDS) -> None:
        super().__init__()
        self.interval_seconds = interval_seconds
        self.trust_env = False
        self.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        )
        self.trace: list[dict[str, Any]] = []
        self._last_start = 0.0

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        now = time.monotonic()
        if self._last_start:
            wait = self.interval_seconds - (now - self._last_start)
            if wait > 0:
                time.sleep(wait)
        started = time.monotonic()
        self._last_start = started
        record: dict[str, Any] = {
            "method": method.upper(),
            "url": url,
            "started_monotonic": round(started, 6),
            "started_utc": utc_now(),
        }
        try:
            response = super().request(method, url, **kwargs)
        except requests.RequestException as exc:
            record["error"] = f"{type(exc).__name__}: {exc}"
            self.trace.append(record)
            raise
        record.update(
            {
                "status": response.status_code,
                "final_url": response.url,
                "content_type": clean_text(response.headers.get("Content-Type")),
            }
        )
        self.trace.append(record)
        return response


def comparable_host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def collect_dom_evidence(
    manifest: list[dict[str, Any]], session: requests.Session | None = None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_source = {item["source_link"]: item for item in manifest}
    active_session = session or RateLimitedSession()
    evidence: list[dict[str, Any]] = []
    for hospital, name, source_link in DOM_SAMPLE_PLAN:
        item = by_source.get(source_link)
        if item is None:
            raise RuntimeError(f"DOM 样本不在 596 行工作集：{source_link}")
        if comparable_host(source_link) != OFFICIAL_HOSTS[hospital]:
            raise RuntimeError(f"DOM 样本不是授权医院官方域名：{source_link}")
        record: dict[str, Any] = {
            "hospital": hospital,
            "name": name,
            "source_link": source_link,
            "http_status": "",
            "final_url": "",
            "selector": "nav.breadcrumb",
            "dom_breadcrumb": "",
            "page_title": "",
            "removed_segment": item["removed_segment"],
            "agreement": "NO",
            "observed_utc": utc_now(),
            "error": "",
        }
        try:
            response = active_session.get(source_link, timeout=30)
            record["http_status"] = response.status_code
            record["final_url"] = response.url
            content_type = clean_text(response.headers.get("Content-Type"))
            if response.status_code != 200 or "html" not in content_type.lower():
                raise RuntimeError(f"HTTP {response.status_code} content-type={content_type}")
            if comparable_host(response.url) != OFFICIAL_HOSTS[hospital]:
                raise RuntimeError(f"重定向越出官方域名：{response.url}")
            soup = BeautifulSoup(response.content, "html.parser")
            breadcrumb = soup.select_one("nav.breadcrumb")
            if breadcrumb is None:
                raise RuntimeError("未找到 nav.breadcrumb")
            dom_text = clean_text(breadcrumb.get_text(" ", strip=True))
            page_title = clean_text(soup.title.get_text(" ", strip=True)).split(" | ", 1)[0]
            record["dom_breadcrumb"] = dom_text
            record["page_title"] = page_title
            if hospital == SYSUCC:
                agrees = dom_text in item["removed_segment"] and page_title in item["removed_segment"]
            else:
                agrees = dom_text == item["removed_segment"].strip()
            record["agreement"] = "YES" if agrees else "NO"
        except (requests.RequestException, RuntimeError) as exc:
            record["error"] = f"{type(exc).__name__}: {exc}"
        evidence.append(record)
    trace = getattr(active_session, "trace", [])
    return evidence, list(trace)


def request_summary(trace: list[dict[str, Any]]) -> dict[str, Any]:
    starts = [float(item["started_monotonic"]) for item in trace if "started_monotonic" in item]
    gaps = [round(right - left, 3) for left, right in zip(starts, starts[1:])]
    return {
        "request_count": len(trace),
        "minimum_adjacent_start_interval_seconds": min(gaps) if gaps else None,
        "all_requests_serial": True,
        "trust_env": False,
        "manual_cookies": False,
    }


def validate_payload(payload: dict[str, Any], require_current_snapshot: bool = False) -> None:
    errors: list[str] = []
    meta = payload.get("meta", {})
    manifest = payload.get("manifest", [])
    profiles = payload.get("profile_impact", [])
    atypical = payload.get("atypical_profile_cases", [])
    dom = payload.get("dom_evidence", [])
    if meta.get("issue_number") != ISSUE_NUMBER or meta.get("phase") != PHASE:
        errors.append("Issue/Phase 不一致")
    if len(manifest) != EXPECTED_ROWS or meta.get("affected_rows") != EXPECTED_ROWS:
        errors.append(f"底表工作集不是 {EXPECTED_ROWS}")
    if dict(Counter(item.get("hospital") for item in manifest)) != EXPECTED_BY_HOSPITAL:
        errors.append("底表医院分组不是 506 + 90")
    if len(profiles) != EXPECTED_PROFILES or meta.get("affected_profiles") != EXPECTED_PROFILES:
        errors.append(f"画像工作集不是 {EXPECTED_PROFILES}")
    if dict(Counter(item.get("hospital") for item in profiles)) != EXPECTED_PROFILES_BY_HOSPITAL:
        errors.append("画像医院分组不是 204 + 38")
    if len(atypical) != EXPECTED_ATYPICAL_PROFILES:
        errors.append(f"SYSUCC 异型画像不是 {EXPECTED_ATYPICAL_PROFILES} 份")
    if any(item.get("source_link") not in {row.get("source_link") for row in manifest} for item in profiles):
        errors.append("存在无法映射到 596 行工作集的污染画像")
    if any(
        int(item.get("original_length", 0))
        != int(item.get("removed_length", 0)) + int(item.get("remaining_length", 0))
        for item in manifest
    ):
        errors.append("存在长度不闭合试算行")
    if any("面包屑" not in item.get("removed_segment", "") and "导航痕迹" not in item.get("removed_segment", "") for item in manifest):
        errors.append("存在 removed_segment 缺少导航标记")
    liuhui = [
        item
        for item in manifest
        if item.get("hospital") == SYSUCC and item.get("name") == "刘慧"
    ]
    if len(liuhui) != 1 or liuhui[0].get("site_title") != "刘慧(小)":
        errors.append("刘慧 -> 刘慧(小) 专项证据不唯一")
    if meta.get("middle_position_rows") != 0 or meta.get("adjacent_quote_rows") != 0:
        errors.append("当前基线中段/孤立撇号现场计数不是 0")
    if len(dom) != 10 or dict(Counter(item.get("hospital") for item in dom)) != {
        SYSUCC: 6,
        ZSSY: 4,
    }:
        errors.append("DOM 对照不是 6 + 4")
    if any(item.get("http_status") != 200 or item.get("agreement") != "YES" for item in dom):
        errors.append("存在 DOM 对照未成功或未同意剥离边界")
    atypical_sources = {item.get("source_link") for item in atypical}
    if sum(item.get("source_link") in atypical_sources for item in dom if item.get("hospital") == SYSUCC) < 2:
        errors.append("SYSUCC DOM 对照未覆盖至少 2 个异型画像")
    if not any(item.get("name") == "变态反应" for item in dom if item.get("hospital") == ZSSY):
        errors.append("ZSSY DOM 对照缺少科室名行")
    request_meta = payload.get("request_summary", {})
    minimum_gap = request_meta.get("minimum_adjacent_start_interval_seconds")
    if minimum_gap is not None and minimum_gap < REQUEST_INTERVAL_SECONDS - 0.01:
        errors.append(f"真实请求相邻启动间隔小于 1 秒：{minimum_gap}")
    if request_meta.get("all_requests_serial") is not True or request_meta.get("trust_env") is not False:
        errors.append("请求未满足串行/禁用环境代理")
    if payload.get("protected_before") != payload.get("protected_after"):
        errors.append("正式受保护资产在 TRIAL 前后发生变化")
    if meta.get("formal_assets_modified") is not False:
        errors.append("formal_assets_modified 不是 false")
    if require_current_snapshot and protected_snapshot() != payload.get("protected_after"):
        errors.append("当前正式受保护资产已偏离 TRIAL 快照")
    if errors:
        raise RuntimeError("[FATAL - HUMAN_INTERVENTION_REQUIRED] TRIAL 验证失败：\n- " + "\n- ".join(errors))


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|")


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    by_type = Counter(item["match_type"] for item in payload["manifest"])
    atypical = payload["atypical_profile_cases"]
    lines = [
        "# Issue #87 GOVERN-2 导航文本污染清理 TRIAL 报告",
        "",
        f"- Phase：`{meta['phase']}`；仅 dry-run，正式资产修改：`{meta['formal_assets_modified']}`。",
        f"- 底表：{meta['affected_rows']} = SYSUCC 506 + ZSSY 90。",
        f"- 画像：{meta['affected_profiles']} = SYSUCC 204 + ZSSY 38。",
        f"- 规则命中：{dict(by_type)}。",
        f"- 在线 DOM：{len(payload['dom_evidence'])} = SYSUCC 6 + ZSSY 4；全部 HTTP 200 且边界同意。",
        "",
        "## 剥离规则",
        "",
        "1. SYSUCC 使用整体特征定位：`<页面类型> 面包屑 首页 / ... / <页面类型> <站方标题> `；支持 `临床专家`、`科研学者` 与住培页，使用 search 而非仅从字符串起点匹配。",
        "2. ZSSY 使用重复页标题锚定位：`导航痕迹 首页 / [专家介绍 /] <页标题> <页标题> `；只删除前一个 DOM breadcrumb，保留正文中的第二个页标题。",
        "3. 删除后值严格等于原值前缀 + 原值后缀；不做 strip、空白归一、字段改写或其他列处理。",
        "4. 若导航段前紧邻孤立 `'` / `’` / `‘`，TRIAL 只标记并保留，待 owner 决定；当前基线实测 0 行。",
        "",
        "## Owner 预核验与当前基线差异",
        "",
        "- 当前 `main 8c591d90` 三载体逐值一致；596 个底表单元格的待删除段均从索引 0 开始，未复现中段导航段，也未复现前邻孤立撇号。",
        "- 8 个异型可在画像载体上精确复现：它们违反“单一承载行且行首为 `临床专家 面包屑`”的常见形态，表现为非标准区块、重复承载、正文前缀、`科研学者` 或住培页。",
        "- 因此 TRIAL 未静默扩大规则：中段匹配能力已有离线测试，但 FULL 前应由 owner 确认是否以当前现场 0 中段/0 撇号为准。",
        "- 站方页标题与底表 `姓名` 不同共 16 行：SYSUCC 10 行、ZSSY 6 行。除 `刘慧 -> 刘慧(小)` 外，包含 6 个科室短名与 9 个历史姓名污染；本批全部只留证，不改姓名或其他列。",
        "- 对应底表行：SYSUCC 689/745/884/889/961/975/1074/1123/1157/1190；ZSSY 1215/1216/1221/1327/1373/1602。",
        "",
        "## 8 个异型画像载体",
        "",
        "| 底表行 | 姓名 | 画像 | 承载行 | 承载区块 |",
        "|---:|---|---|---|---|",
    ]
    for item in atypical:
        lines.append(
            "| "
            + " | ".join(
                markdown_cell(item.get(field))
                for field in (
                    "master_row_number",
                    "master_name",
                    "profile_path",
                    "carrier_line_numbers",
                    "carrier_sections",
                )
            )
            + " |"
        )
    liuhui = next(
        item
        for item in payload["manifest"]
        if item["hospital"] == SYSUCC and item["name"] == "刘慧"
    )
    lines.extend(
        [
            "",
            "## 刘慧站方后缀专项",
            "",
            f"- 底表第 {liuhui['row_number']} 行姓名为 `刘慧`，官方页标题与导航终止标题为 `刘慧(小)`。",
            f"- 试算删除 `{liuhui['removed_segment']}`；只以站方 DOM 标题作为导航终止锚，不改底表姓名。",
            "",
            "## 正式资产保护",
            "",
            "- 总底表 payload/CSV/XLSX/更新报告、入口台账、两院完整画像树及两份 `_索引.md` 的仓库 blob 摘要前后完全一致。",
            "- 文本摘要统一先把 CRLF/CR 归一为 LF；二进制文件按原始字节。",
            "",
            "## 工件",
            "",
            f"- `{repo_relative(PAYLOAD_PATH)}`",
            f"- `{repo_relative(MANIFEST_PATH)}`",
            f"- `{repo_relative(PROFILE_IMPACT_PATH)}`",
            f"- `{repo_relative(DOM_EVIDENCE_PATH)}`",
            f"- `{repo_relative(REPORT_PATH)}`",
            "",
            "当前阶段：`TRIAL_READY_FOR_OWNER_AUDIT`。未取得 owner 在关联 PR 明确下发的 FULL 指令前，不得写入正式总底表或画像。",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def ensure_outputs_absent() -> None:
    existing = [
        repo_relative(path)
        for path in (PAYLOAD_PATH, MANIFEST_PATH, PROFILE_IMPACT_PATH, DOM_EVIDENCE_PATH, REPORT_PATH)
        if path.exists()
    ]
    if existing:
        raise RuntimeError("TRIAL 输出已存在，拒绝覆盖：\n- " + "\n- ".join(existing))


def run_trial(session: requests.Session | None = None) -> dict[str, Any]:
    ensure_outputs_absent()
    before = protected_snapshot()
    rows = load_current_layers()
    manifest = affected_master_manifest(rows)
    profile_impact, atypical = profile_impact_inventory(manifest)
    dom_evidence, trace = collect_dom_evidence(manifest, session=session)
    after = protected_snapshot()
    payload: dict[str, Any] = {
        "meta": {
            "issue_number": ISSUE_NUMBER,
            "phase": PHASE,
            "base_commit": "8c591d902e8435d8c203f9f639c8454cd6687601",
            "master_rows": len(rows),
            "affected_rows": len(manifest),
            "affected_by_hospital": dict(Counter(item["hospital"] for item in manifest)),
            "affected_profiles": len(profile_impact),
            "affected_profiles_by_hospital": dict(
                Counter(item["hospital"] for item in profile_impact)
            ),
            "atypical_profile_cases": len(atypical),
            "middle_position_rows": sum(item["segment_position"] == "MIDDLE" for item in manifest),
            "adjacent_quote_rows": sum(
                item["quote_boundary_status"] != "NO_ADJACENT_QUOTE" for item in manifest
            ),
            "formal_assets_modified": before != after,
            "generated_utc": utc_now(),
        },
        "rules": {
            "preserve_prefix_suffix_exactly": True,
            "match_anywhere": True,
            "isolated_quote_policy": "PRESERVE_AND_FLAG_PENDING_OWNER",
            "current_base_discrepancy": (
                "596/596 master segments start at index 0 and 0 have adjacent quotes; "
                "the exact eight atypical cases are observable in profile carrier layout."
            ),
        },
        "request_summary": request_summary(trace),
        "request_trace": trace,
        "protected_before": before,
        "protected_after": after,
        "manifest": manifest,
        "profile_impact": profile_impact,
        "atypical_profile_cases": atypical,
        "dom_evidence": dom_evidence,
        "artifacts": {
            "payload": repo_relative(PAYLOAD_PATH),
            "manifest": repo_relative(MANIFEST_PATH),
            "profile_impact": repo_relative(PROFILE_IMPACT_PATH),
            "dom_evidence": repo_relative(DOM_EVIDENCE_PATH),
            "report": repo_relative(REPORT_PATH),
        },
    }
    validate_payload(payload)
    PAYLOAD_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_csv(MANIFEST_PATH, MANIFEST_FIELDS, manifest)
    write_csv(PROFILE_IMPACT_PATH, PROFILE_FIELDS, profile_impact)
    write_csv(DOM_EVIDENCE_PATH, DOM_FIELDS, dom_evidence)
    write_report(payload)
    return payload


def validate_outputs() -> dict[str, Any]:
    payload = json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
    validate_payload(payload, require_current_snapshot=True)
    expected_files = {
        MANIFEST_PATH: (MANIFEST_FIELDS, payload["manifest"]),
        PROFILE_IMPACT_PATH: (PROFILE_FIELDS, payload["profile_impact"]),
        DOM_EVIDENCE_PATH: (DOM_FIELDS, payload["dom_evidence"]),
    }
    for path, (fields, expected_rows) in expected_files.items():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if tuple(reader.fieldnames or ()) != fields:
                raise RuntimeError(f"{repo_relative(path)} schema 漂移")
        projected = [{field: row_value(item.get(field)) for field in fields} for item in expected_rows]
        if rows != projected:
            raise RuntimeError(f"{repo_relative(path)} 与 payload 不一致")
    if not REPORT_PATH.is_file():
        raise RuntimeError("TRIAL 报告不存在")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Issue #87 GOVERN-2 导航文本污染清理 TRIAL")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--trial", action="store_true", help="执行 596 行 dry-run 与 10 行官方 DOM 对照")
    modes.add_argument("--validate", action="store_true", help="验证既有 TRIAL 工件与正式资产快照")
    args = parser.parse_args()
    payload = run_trial() if args.trial else validate_outputs()
    meta = payload["meta"]
    print(
        f"issue87_{'trial' if args.trial else 'validate'}_complete: "
        f"rows={meta['affected_rows']} profiles={meta['affected_profiles']} "
        f"dom={len(payload['dom_evidence'])} formal_modified={meta['formal_assets_modified']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
