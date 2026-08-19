from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import date
from http.client import IncompleteRead
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import ProxyHandler, Request, build_opener

from bs4 import BeautifulSoup

import gzbrain_photo_backfill_full as framework
import ny5y_photo_backfill_trial as trial


ROOT = trial.ROOT
WORK_DIR = trial.WORK_DIR
HOSPITAL = trial.HOSPITAL
ISSUE_NUMBER = trial.ISSUE_NUMBER
EXPECTED_SCOPE_COUNT = trial.EXPECTED_SCOPE_COUNT
EXPECTED_TRIAL_REUSE_COUNT = trial.EXPECTED_TRIAL_COUNT
EXPECTED_FRESH_COUNT = EXPECTED_SCOPE_COUNT - EXPECTED_TRIAL_REUSE_COUNT
PROFILE_DIR = trial.PROFILE_DIR
FORMAL_PHOTO_DIR = trial.FORMAL_PHOTO_DIR
FULL_BASENAME = f"{HOSPITAL}_photo_backfill_full"
FULL_JSON_PATH = WORK_DIR / f"{FULL_BASENAME}_payload.json"
FULL_CSV_PATH = WORK_DIR / f"{FULL_BASENAME}_reconciliation.csv"
FULL_REPORT_PATH = WORK_DIR / f"{FULL_BASENAME}_report.md"
FULL_AUDIT_SHEET_PATH = WORK_DIR / f"{FULL_BASENAME}_audit_sheet.jpg"
FULL_VISUAL_DIR = WORK_DIR / f"{FULL_BASENAME}_visual_review"
PHOTO_RELATIVE_ROOT = Path("01_试点医院") / HOSPITAL / "照片"
FULL_AUTHORIZATION = (
    "PR #80 owner comment 2026-08-19T03:33:37Z: "
    "TRIAL_AUDIT_PASSED -> FULL_APPEND_AND_OBSIDIAN; fixed scope 134; "
    "reuse 10 audited TRIAL originals; strict yisheng_xq_bug_left page-reference gate; "
    "same-person duplicate-SHA ruling 2026-08-19T03:56:54Z"
)
OWNER_DUPLICATE_RULING_URL = (
    "https://github.com/nancywrayg57-jpg/doctor-data-collection/"
    "pull/80#issuecomment-5337332486"
)
OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS = {
    "d48a3b1b579a99f88d01d48d201cdc5001efd9361095a81e81c2b1fc93e372f7": {
        "name": "陈特立",
        "sources": frozenset(
            {
                "http://www.ny5y.cn/yisheng_xq.php?id=489",
                "http://www.ny5y.cn/yisheng_xq.php?id=314",
            }
        ),
    },
    "de6da92057b28cb02f8b431ebf32e7b73f9e8229d05571be7ef5d3a1c28c22fc": {
        "name": "何卓凯",
        "sources": frozenset(
            {
                "http://www.ny5y.cn/yisheng_xq.php?id=494",
                "http://www.ny5y.cn/yisheng_xq.php?id=478",
            }
        ),
    },
}
REQUEST_MODE = "urllib-browser-ua-get/no-cookie/no-proxy/no-bypass"
TEMPLATE_SIGNATURE = "div.yisheng_xq_bug_left inline background-image"
MAX_PHOTO_BYTES = 20 * 1024 * 1024
OWNER_REPORT_BYTES = 5 * 1024 * 1024
VISUAL_PAGE_SIZE = 25
FULL_VISUAL_PASS_STATUS = framework.FULL_VISUAL_PASS_STATUS
ORIGINAL_TRIAL_VALIDATE_PAYLOAD = trial.validate_payload
ORIGINAL_PAGE_REFERENCED_PHOTO_URL = trial.page_referenced_photo_url


@dataclass(frozen=True)
class HttpResult:
    status: int
    content_type: str
    charset: str
    content: bytes
    final_url: str
    redirects: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class MediaAnalysis:
    page_name: str
    page_title: str
    state: str
    photo_url: str
    opaque_query: str
    template_signature: str
    photo_reference_count: int
    single_con_image_count: int
    outside_image_reference_count: int
    excluded_resource_examples: tuple[dict[str, str], ...]
    container_html_snippet: str
    detection_feature: str


class OfficialUrlOpenSession:
    """Owner-approved browser-UA GET without Cookie, proxy, or challenge bypass."""

    def __init__(self) -> None:
        self.opener = build_opener(ProxyHandler({}))
        self.incomplete_read_retry_count = 0

    @property
    def cookie_names(self) -> list[str]:
        return []

    @property
    def default_headers(self) -> list[list[str]]:
        return [["User-Agent", trial.USER_AGENT]]

    def get(self, url: str) -> HttpResult:
        request = Request(url, headers={"User-Agent": trial.USER_AGENT})
        for attempt in range(2):
            try:
                with self.opener.open(request, timeout=35) as response:
                    return HttpResult(
                        status=int(response.status),
                        content_type=response.headers.get_content_type(),
                        charset=response.headers.get_content_charset() or "utf-8",
                        content=response.read(),
                        final_url=response.geturl(),
                        redirects=(),
                    )
            except IncompleteRead as exc:
                if attempt == 0:
                    self.incomplete_read_retry_count += 1
                    continue
                raise RuntimeError(
                    f"官网响应连续两次传输不完整：{url} 已读 {len(exc.partial)} bytes"
                ) from exc
            except HTTPError as exc:
                return HttpResult(
                    status=int(exc.code),
                    content_type=exc.headers.get_content_type(),
                    charset=exc.headers.get_content_charset() or "utf-8",
                    content=exc.read(),
                    final_url=exc.geturl(),
                    redirects=(),
                )
            except URLError as exc:
                raise RuntimeError(f"官网请求失败：{url} {exc}") from exc
        raise AssertionError("官网请求循环未返回")


def page_referenced_photo_url_for_full(value: Any, source_link: str) -> tuple[str, str]:
    normalized = ORIGINAL_PAGE_REFERENCED_PHOTO_URL(value, source_link)
    if not normalized:
        return "", ""
    return normalized, urlparse(normalized).query


def analyze_full_doctor_media(
    html: str, source_link: str, expected_name: str
) -> MediaAnalysis:
    if not trial.detail_id(source_link):
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    soup = BeautifulSoup(html, "html.parser")
    containers = soup.select("div.yisheng_xq_bug_left")
    if not containers:
        return MediaAnalysis(
            page_name="",
            page_title="",
            state="无照片容器",
            photo_url="",
            opaque_query="",
            template_signature=TEMPLATE_SIGNATURE,
            photo_reference_count=0,
            single_con_image_count=0,
            outside_image_reference_count=len(soup.find_all("img", src=True)),
            excluded_resource_examples=(),
            container_html_snippet="",
            detection_feature=(
                "HTTP 200 detail template contains no div.yisheng_xq_bug_left "
                "and no physician detail body"
            ),
        )
    if len(containers) != 1:
        raise RuntimeError(
            f"yisheng_xq_bug_left 容器不唯一：{source_link} 数量={len(containers)}"
        )

    name_nodes = soup.select("div.yuanzhang")
    title_nodes = soup.select("div.xq_zhicheng")
    if len(name_nodes) != 1 or len(title_nodes) != 1:
        raise RuntimeError(f"详情姓名或职称主结构不唯一：{source_link}")
    direct_name = " ".join(
        str(item) for item in name_nodes[0].find_all(string=True, recursive=False)
    )
    page_name = trial.clean_text(direct_name)
    page_title = trial.clean_text(title_nodes[0].get_text(" ", strip=True))
    if page_name != trial.clean_text(expected_name):
        raise RuntimeError(
            f"详情姓名与底表不一致：底表={expected_name} 官网={page_name or '空'} {source_link}"
        )

    container = containers[0]
    raw_url = trial.base.style_background_url(container.get("style"))
    if not raw_url:
        return MediaAnalysis(
            page_name=page_name,
            page_title=page_title,
            state="无照片容器",
            photo_url="",
            opaque_query="",
            template_signature=TEMPLATE_SIGNATURE,
            photo_reference_count=0,
            single_con_image_count=0,
            outside_image_reference_count=len(soup.find_all("img", src=True)),
            excluded_resource_examples=(),
            container_html_snippet=trial.clean_text(str(container)),
            detection_feature="unique container lacks inline background-image URL",
        )

    absolute = urljoin(source_link, raw_url)
    decoded_query = trial.suspicious_query_decoding(absolute)
    lowered_path = unquote(urlparse(absolute).path).casefold()
    path_marker = next(
        (marker for marker in trial.base.PLACEHOLDER_MARKERS if marker in lowered_path), ""
    )
    if decoded_query or path_marker:
        feature = (
            f"URL query Base64 解码命中占位标记：{decoded_query}"
            if decoded_query
            else f"URL 路径命中占位标记：{path_marker}"
        )
        return MediaAnalysis(
            page_name=page_name,
            page_title=page_title,
            state="占位图",
            photo_url="",
            opaque_query="",
            template_signature=TEMPLATE_SIGNATURE,
            photo_reference_count=1,
            single_con_image_count=0,
            outside_image_reference_count=len(soup.find_all("img", src=True)),
            excluded_resource_examples=(
                {"url": absolute, "reason": "占位图", "feature": feature},
            ),
            container_html_snippet=trial.clean_text(str(container)),
            detection_feature=feature,
        )

    normalized = ORIGINAL_PAGE_REFERENCED_PHOTO_URL(raw_url, source_link)
    if not normalized:
        raise RuntimeError(f"页面引用照片 URL 越界：{source_link} {raw_url}")
    return MediaAnalysis(
        page_name=page_name,
        page_title=page_title,
        state="",
        photo_url=normalized,
        opaque_query=urlparse(normalized).query,
        template_signature=TEMPLATE_SIGNATURE,
        photo_reference_count=1,
        single_con_image_count=0,
        outside_image_reference_count=len(soup.find_all("img", src=True)),
        excluded_resource_examples=(),
        container_html_snippet=trial.clean_text(str(container)),
        detection_feature=(
            "only the unique yisheng_xq_bug_left inline background-image is eligible; "
            "all other page and narrative images are excluded"
        ),
    )


def limited_unique_color_count(content: bytes, limit: int = 2) -> int:
    return trial.limited_unique_color_count(content, limit)


def placeholder_response_reason(
    photo_url: str, content: bytes, width: int, height: int
) -> str:
    lowered_path = unquote(urlparse(photo_url).path).casefold()
    for marker in trial.base.PLACEHOLDER_MARKERS:
        if marker in lowered_path:
            return f"URL 路径命中占位标记：{marker}"
    decoded_query = trial.suspicious_query_decoding(photo_url)
    if decoded_query:
        return f"URL query Base64 解码命中占位标记：{decoded_query}"
    unique_colors = limited_unique_color_count(content, limit=2)
    if unique_colors <= 2:
        return f"全图唯一颜色数={unique_colors}，命中单色/近单色占位启发式"
    if len(content) <= 10 * 1024 and width <= 128 and height <= 128:
        return f"响应呈小尺寸占位图特征：{len(content)} bytes；{width}×{height}"
    return ""


def validate_trial_payload_for_full(
    payload: dict[str, Any], require_visual_pass: bool = False
) -> None:
    ORIGINAL_TRIAL_VALIDATE_PAYLOAD(payload)
    if require_visual_pass and payload["meta"].get("visual_review_status") != (
        "PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS"
    ):
        raise RuntimeError("TRIAL 联系表尚未通过人工视觉门禁")


def validate_trial_manifest(payload: dict[str, Any]) -> None:
    with trial.TRIAL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED_TRIAL_REUSE_COUNT:
        raise RuntimeError("TRIAL manifest 不是 10 行")
    rows_by_source = {row["来源链接"]: row for row in rows}
    if len(rows_by_source) != EXPECTED_TRIAL_REUSE_COUNT:
        raise RuntimeError("TRIAL manifest 来源链接不唯一")
    for sample in payload["photo_samples"]:
        row = rows_by_source.get(sample["source_link"])
        if row is None or any(
            (
                row["姓名"] != sample["name"],
                row["照片链接"] != sample["photo_url"],
                row["SHA-256"] != sample["sha256"],
                int(row["字节"]) != int(sample["bytes"]),
                row["实际魔数格式"] != sample["actual_extension"],
                row["声明格式"] != sample["declared_extension"],
            )
        ):
            raise RuntimeError(f"TRIAL manifest 与 payload 不一致：{sample['source_link']}")


def size_buckets(samples: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "<200KiB": 0,
        "200KiB-1MiB": 0,
        "1-5MiB": 0,
        "5-20MiB": 0,
        ">20MiB": 0,
    }
    for sample in samples:
        size = int(sample["bytes"])
        if size < 200 * 1024:
            counts["<200KiB"] += 1
        elif size < 1024 * 1024:
            counts["200KiB-1MiB"] += 1
        elif size <= OWNER_REPORT_BYTES:
            counts["1-5MiB"] += 1
        elif size <= MAX_PHOTO_BYTES:
            counts["5-20MiB"] += 1
        else:
            counts[">20MiB"] += 1
    return counts


def same_person_allowlist_note(digest: str) -> str:
    return (
        "OWNER_APPROVED_SAME_PERSON_ALLOWLIST: 同名+同职称+擅长逐字一致+"
        f"同 SHA 异上传路径; sha256={digest}; owner_ruling={OWNER_DUPLICATE_RULING_URL}"
    )


def decorate_owner_approved_duplicate_groups(
    samples: list[dict[str, Any]], reconciliation_by_source: dict[str, dict[str, Any]]
) -> None:
    for digest, approved in OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS.items():
        group = [item for item in samples if item.get("sha256") == digest]
        names = {trial.clean_text(item.get("name")) for item in group}
        sources = {trial.clean_text(item.get("source_link")) for item in group}
        photo_urls = {trial.clean_text(item.get("photo_url")) for item in group}
        if (
            names != {approved["name"]}
            or sources != set(approved["sources"])
            or len(photo_urls) != 2
        ):
            raise RuntimeError(f"Owner same-person allowlist 证据不闭合：{digest}")
        note = same_person_allowlist_note(digest)
        for item in group:
            item["same_person_allowlist_decision"] = note
            reconciliation_by_source[item["source_link"]]["错误证据"] = note


def validate_owner_approved_duplicate_groups(payload: dict[str, Any]) -> None:
    photos = payload.get("photo_samples", [])
    reconciliation = {
        item.get("来源链接"): item for item in payload.get("reconciliation", [])
    }
    duplicate_groups = payload.get("duplicate_sha256_groups", {})
    if set(duplicate_groups) != set(OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS):
        raise RuntimeError("FULL same-person allowlist SHA 组不精确")
    for digest, approved in OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS.items():
        group = [item for item in photos if item.get("sha256") == digest]
        note = same_person_allowlist_note(digest)
        if (
            {item.get("name") for item in group} != {approved["name"]}
            or {item.get("source_link") for item in group} != set(approved["sources"])
            or len({item.get("photo_url") for item in group}) != 2
            or any(item.get("same_person_allowlist_decision") != note for item in group)
            or any(
                reconciliation[source].get("错误证据") != note
                for source in approved["sources"]
            )
        ):
            raise RuntimeError(f"FULL same-person allowlist 证据验证失败：{digest}")


def configure_framework() -> None:
    trial.configure_base()
    master_paths = {
        "MASTER_JSON_PATH": trial.base.MASTER_JSON_PATH,
        "MASTER_CSV_PATH": trial.base.MASTER_CSV_PATH,
        "MASTER_XLSX_PATH": trial.base.MASTER_XLSX_PATH,
        "MASTER_REPORT_PATH": trial.base.MASTER_REPORT_PATH,
        "LEDGER_PATH": trial.base.LEDGER_PATH,
    }
    for name, value in master_paths.items():
        setattr(trial, name, value)

    compatibility = {
        "safe_photo_part": trial.base.safe_photo_part,
        "atomic_department": trial.base.atomic_department,
        "primary_title": trial.base.primary_title,
        "magic_extension": trial.base.magic_extension,
        "image_dimensions": trial.base.image_dimensions,
        "tree_snapshot": trial.base.tree_snapshot,
        "protected_snapshot": trial.base.protected_snapshot,
        "validate_payload": validate_trial_payload_for_full,
        "validate_manifest": validate_trial_manifest,
        "page_referenced_photo_url": page_referenced_photo_url_for_full,
        "size_buckets": size_buckets,
        "HttpResult": HttpResult,
        "MediaAnalysis": MediaAnalysis,
        "OfficialUrlOpenSession": OfficialUrlOpenSession,
        "TEMPLATE_SIGNATURE": TEMPLATE_SIGNATURE,
        "MAX_PHOTO_BYTES": MAX_PHOTO_BYTES,
        "OWNER_REPORT_BYTES": OWNER_REPORT_BYTES,
        "PLACEHOLDER_PATH_MARKERS": trial.base.PLACEHOLDER_MARKERS,
    }
    for name, value in compatibility.items():
        setattr(trial, name, value)

    framework_values = {
        "trial": trial,
        "ROOT": ROOT,
        "WORK_DIR": WORK_DIR,
        "SOURCE_DIR": trial.SOURCE_DIR,
        "HOSPITAL": HOSPITAL,
        "ISSUE_NUMBER": ISSUE_NUMBER,
        "MASTER_JSON_PATH": trial.MASTER_JSON_PATH,
        "MASTER_CSV_PATH": trial.MASTER_CSV_PATH,
        "MASTER_XLSX_PATH": trial.MASTER_XLSX_PATH,
        "MASTER_REPORT_PATH": trial.MASTER_REPORT_PATH,
        "LEDGER_PATH": trial.LEDGER_PATH,
        "PROFILE_DIR": PROFILE_DIR,
        "FORMAL_PHOTO_DIR": FORMAL_PHOTO_DIR,
        "EXPECTED_SCOPE_COUNT": EXPECTED_SCOPE_COUNT,
        "EXPECTED_TRIAL_REUSE_COUNT": EXPECTED_TRIAL_REUSE_COUNT,
        "EXPECTED_FRESH_COUNT": EXPECTED_FRESH_COUNT,
        "EXPECTED_PROFILE_COUNT": EXPECTED_SCOPE_COUNT,
        "FULL_BASENAME": FULL_BASENAME,
        "FULL_JSON_PATH": FULL_JSON_PATH,
        "FULL_CSV_PATH": FULL_CSV_PATH,
        "FULL_REPORT_PATH": FULL_REPORT_PATH,
        "FULL_AUDIT_SHEET_PATH": FULL_AUDIT_SHEET_PATH,
        "FULL_VISUAL_DIR": FULL_VISUAL_DIR,
        "PHOTO_RELATIVE_ROOT": PHOTO_RELATIVE_ROOT,
        "FULL_AUTHORIZATION": FULL_AUTHORIZATION,
        "REQUEST_MODE": REQUEST_MODE,
        "VISUAL_PAGE_SIZE": VISUAL_PAGE_SIZE,
        "HOME_IS_GATE": False,
        "PULL_REQUEST_NUMBER": 80,
        "OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS": (
            OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS
        ),
        "FULL_PROTECTED_FILES": (
            trial.MASTER_REPORT_PATH,
            trial.LEDGER_PATH,
            trial.TRIAL_JSON_PATH,
            trial.TRIAL_CSV_PATH,
            trial.TRIAL_REPORT_PATH,
            trial.CONTACT_SHEET_PATH,
        ),
        "analyze_full_doctor_media": analyze_full_doctor_media,
        "placeholder_response_reason": placeholder_response_reason,
        "decorate_owner_approved_duplicate_groups": (
            decorate_owner_approved_duplicate_groups
        ),
        "validate_owner_approved_duplicate_groups": (
            validate_owner_approved_duplicate_groups
        ),
    }
    for name, value in framework_values.items():
        setattr(framework, name, value)


def run_full(run_date: str) -> dict[str, Any]:
    configure_framework()
    return framework.run_full(run_date)


def validate_full_payload(
    payload: dict[str, Any], photo_root: Path, audit_sheet: Path, visual_root: Path
) -> None:
    configure_framework()
    framework.validate_full_payload(payload, photo_root, audit_sheet, visual_root)


def validate_full_installation(payload: dict[str, Any]) -> None:
    configure_framework()
    framework.validate_full_installation(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Issue #{ISSUE_NUMBER} {HOSPITAL} photo-backfill FULL"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--full", action="store_true")
    mode.add_argument("--validate-full", action="store_true")
    mode.add_argument("--mark-visual-pass", action="store_true")
    parser.add_argument("--run-date", default=date.today().isoformat())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_framework()
    if args.full:
        payload = framework.run_full(args.run_date)
        print(
            "FULL_DONE "
            f"expected={payload['meta']['expected_count']} "
            f"downloaded={payload['meta']['downloaded_count']} "
            f"failed={payload['meta']['failed_count']} "
            f"profiles={payload['meta']['profile_refreshed_count']}"
        )
        return
    if args.mark_visual_pass:
        payload = framework.mark_visual_pass()
        print(f"FULL_VISUAL_REVIEW_MARKED status={payload['meta']['visual_review_status']}")
        return
    payload = framework.load_full_payload()
    framework.validate_full_installation(payload)
    print(
        "FULL_VALIDATED "
        f"expected={payload['meta']['expected_count']} "
        f"downloaded={payload['meta']['downloaded_count']} "
        f"failed={payload['meta']['failed_count']}"
    )


if __name__ == "__main__":
    main()
