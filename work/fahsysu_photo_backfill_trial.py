from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qsl, unquote, urljoin, urlparse

from PIL import Image, ImageDraw, ImageFont, ImageOps

import sys2_photo_backfill_trial as common


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "中山大学附属第一医院"
ISSUE_NUMBER = 71
MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_JSON_PATH = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_REPORT_PATH = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
LEDGER_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"
PROFILE_DIR = VAULT / "01_试点医院" / HOSPITAL
FORMAL_PHOTO_DIR = PROFILE_DIR / "照片"

TRIAL_BASENAME = f"{HOSPITAL}_photo_backfill_trial"
TRIAL_JSON_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
TRIAL_CSV_PATH = WORK_DIR / f"{TRIAL_BASENAME}_manifest.csv"
TRIAL_REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
TRIAL_PHOTO_DIR = WORK_DIR / f"{TRIAL_BASENAME}_photos"

OFFICIAL_HOME = "https://www.fahsysu.org.cn/"
DIRECTORY_URL = "https://www.fahsysu.org.cn/page/6945"
OFFICIAL_HOST = "fahsysu.org.cn"
PHOTO_STYLE_ROOT = (
    "/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/focal_point_480/public/"
)
EXPECTED_SCOPE_COUNT = 860
EXPECTED_SUCCESS_COUNT = 10
EXPECTED_FAILURE_EVIDENCE_COUNT = 2
EXPECTED_RECONCILIATION_COUNT = 12
EXPECTED_PROFILE_FILE_COUNT = 861
EXPECTED_TRIAL_COUNT = EXPECTED_SUCCESS_COUNT
MAX_PHOTO_BYTES = 20 * 1024 * 1024
OWNER_REPORT_BYTES = 5 * 1024 * 1024
DETAIL_RETRY_SECONDS = 30
VISUAL_PASS = "PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10"

# FULL 事务复用上一批已经过验证的 HTTP、魔数、尺寸与底表契约实现。
# 这些别名只暴露只读能力，不改变 Issue #71 的 URL 和照片范围门禁。
BASE_HEADERS = common.BASE_HEADERS
HttpResult = common.HttpResult
OfficialSession = common.OfficialSession
magic_extension = common.magic_extension
image_dimensions = common.image_dimensions

SUCCESS_SAMPLE_PLAN = (
    ("郭宇", "正高"),
    ("陈昆", "正高"),
    ("陈蕾", "正高"),
    ("陈炜", "正高"),
    ("高勇", "正高"),
    ("陈华东", "副高"),
    ("程钢", "副高"),
    ("雷艺炎", "副高"),
    ("汪睿", "副高"),
    ("林维浩", "副高"),
)
FAILURE_EVIDENCE_PLAN = (
    ("黄雄庆", "https://www.fahsysu.org.cn/node/5780"),
    ("张旭宇", "https://www.fahsysu.org.cn/node/5795"),
)

PHOTO_PATH_RE = re.compile(
    r"^/sites/1h\.prod\.sysucloud1\.sysu\.edu\.cn/files/styles/"
    r"focal_point_480/public/.+\.(?:jpe?g|png|gif|webp)$",
    re.IGNORECASE,
)
PLACEHOLDER_PATH_MARKERS = (
    "/default_images/",
    "placeholder",
    "nopic",
    "no_pic",
    "no-photo",
    "noimage",
    "no-image",
)
EXCLUDED_PATH_MARKERS = (
    "/styles/mini200/",
    "/inline-images/",
    "/banner.jpg",
    "gongan",
    "favicon",
    "logo",
)


def clean_text(value: Any) -> str:
    return common.clean_text(value)


def comparable_host(value: str) -> str:
    return common.comparable_host(value)


def utc_now() -> str:
    return common.utc_now()


def detail_id(value: Any) -> str:
    text = clean_text(value)
    parsed = urlparse(text)
    if (
        parsed.scheme != "https"
        or comparable_host(text) != OFFICIAL_HOST
        or parsed.query
        or parsed.fragment
    ):
        return ""
    match = re.fullmatch(r"/node/(\d+)", parsed.path)
    return match.group(1) if match else ""


def detail_template(value: Any) -> str:
    return "fahsysu_node" if detail_id(value) else ""


def atomic_department(row: dict[str, Any]) -> str:
    return common.atomic_department(row)


def primary_title(value: Any) -> str:
    return common.primary_title(value)


def title_level(value: Any) -> str:
    return common.title_level(value)


def safe_photo_part(value: Any) -> str:
    return common.safe_photo_part(value)


def excluded_reference_reason(raw_url: str, source_link: str) -> tuple[str, str]:
    absolute = urljoin(source_link, clean_text(raw_url))
    path = unquote(urlparse(absolute).path).lower()
    for marker in PLACEHOLDER_PATH_MARKERS:
        if marker in path:
            return "占位图", f"path contains {marker}"
    for marker in EXCLUDED_PATH_MARKERS:
        if marker in path:
            return "公共装饰图", f"path contains {marker}"
    return "", ""


def page_referenced_photo_url(raw_url: str, source_link: str) -> tuple[str, str, str]:
    raw = clean_text(raw_url)
    if not raw or excluded_reference_reason(raw, source_link)[0]:
        return "", "", ""
    absolute = urljoin(source_link, raw)
    parsed = urlparse(absolute)
    query = parse_qsl(parsed.query, keep_blank_values=True)
    if (
        parsed.scheme != "https"
        or comparable_host(absolute) != OFFICIAL_HOST
        or parsed.fragment
        or len(query) != 1
        or query[0][0] != "itok"
        or not query[0][1]
        or not PHOTO_PATH_RE.fullmatch(unquote(parsed.path))
    ):
        return "", "", ""
    return absolute, "focal_point_480", query[0][1]


@dataclass(frozen=True)
class MediaAnalysis:
    page_name: str
    page_title: str
    state: str
    photo_url: str
    path_kind: str
    itok: str
    template_signature: str
    focal_point_480_reference_count: int
    media_candidate_count: int
    excluded_resources: tuple[dict[str, str], ...]
    detection_feature: str


def analyze_doctor_media(html: str, source_link: str, expected_name: str) -> MediaAnalysis:
    parser = common.DoctorPageParser()
    parser.feed(html)
    if parser.doctor_name != clean_text(expected_name):
        raise RuntimeError(
            f"医生详情标题与底表姓名不一致：{source_link} "
            f"expected={expected_name!r} actual={parser.doctor_name!r}"
        )
    candidate_urls = list(
        dict.fromkeys(
            urljoin(source_link, clean_text(item))
            for item in parser.doctor_candidates
            if clean_text(item)
        )
    )
    allowed: list[tuple[str, str, str]] = []
    excluded: list[dict[str, str]] = []
    for candidate in candidate_urls:
        reason, feature = excluded_reference_reason(candidate, source_link)
        if reason:
            excluded.append({"url": candidate, "reason": reason, "feature": feature})
            continue
        photo_url, path_kind, itok = page_referenced_photo_url(candidate, source_link)
        if not photo_url:
            raise RuntimeError(f"医生照片容器 URL 越界：{source_link} {candidate}")
        allowed.append((photo_url, path_kind, itok))
    allowed = list(dict.fromkeys(allowed))
    if len(allowed) > 1:
        raise RuntimeError(f"医生照片容器存在多个 focal_point_480 引用：{source_link}")
    if not allowed:
        placeholder = any(item["reason"] == "占位图" for item in excluded)
        evidence_media_count = len(candidate_urls)
        if not candidate_urls:
            page_mini200: list[dict[str, str]] = []
            for raw_url in parser.other_data_images:
                absolute = urljoin(source_link, clean_text(raw_url))
                reason, feature = excluded_reference_reason(absolute, source_link)
                if (
                    reason == "公共装饰图"
                    and comparable_host(absolute) == OFFICIAL_HOST
                    and "/styles/mini200/" in urlparse(absolute).path
                ):
                    page_mini200.append(
                        {"url": absolute, "reason": reason, "feature": feature}
                    )
            page_mini200 = list(
                {item["url"]: item for item in page_mini200}.values()
            )
            if page_mini200:
                excluded.extend(page_mini200)
                evidence_media_count = len(page_mini200)
        if candidate_urls:
            detection = (
                "focal_point_480 引用数=0；media-img 候选均为 "
                + ", ".join(sorted({item["feature"] for item in excluded}))
            )
        elif excluded:
            detection = (
                "focal_point_480 引用数=0；医生照片容器缺失；页面 media-img 仅有 "
                f"{evidence_media_count} 个 path contains /styles/mini200/ 公共图标"
            )
        else:
            detection = "focal_point_480 引用数=0；医生照片容器内无 data-image-url"
        return MediaAnalysis(
            page_name=parser.doctor_name,
            page_title=parser.page_title,
            state="占位图" if placeholder else "无照片容器",
            photo_url="",
            path_kind="",
            itok="",
            template_signature=".other-left .other-media .media-img[data-image-url]",
            focal_point_480_reference_count=0,
            media_candidate_count=evidence_media_count,
            excluded_resources=tuple(excluded),
            detection_feature=detection,
        )
    photo_url, path_kind, itok = allowed[0]
    return MediaAnalysis(
        page_name=parser.doctor_name,
        page_title=parser.page_title,
        state="",
        photo_url=photo_url,
        path_kind=path_kind,
        itok=itok,
        template_signature=".other-left .other-media .media-img[data-image-url]",
        focal_point_480_reference_count=1,
        media_candidate_count=len(candidate_urls),
        excluded_resources=tuple(excluded),
        detection_feature="page references exactly one focal_point_480 URL with one itok",
    )


def file_snapshot(paths: list[Path]) -> dict[str, dict[str, Any]]:
    return common.file_snapshot(paths)


def tree_snapshot(root: Path) -> dict[str, Any]:
    return common.tree_snapshot(root)


def protected_snapshot() -> dict[str, Any]:
    return {
        "master_assets": file_snapshot(
            [MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH, MASTER_REPORT_PATH, LEDGER_PATH]
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
        raise RuntimeError(
            f"Issue #{ISSUE_NUMBER} 范围漂移：应为 {EXPECTED_SCOPE_COUNT} 行，实际 {len(rows)} 行"
        )
    if any(clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")) for row in rows):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} TRIAL 范围内已有照片字段")
    sources = [clean_text(row.get("来源链接")) for row in rows]
    if len(sources) != len(set(sources)):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} 范围来源链接不唯一")
    invalid = [source for source in sources if not detail_id(source)]
    if invalid:
        raise RuntimeError("范围存在非授权详情 URL：" + "、".join(invalid[:5]))
    if tree_snapshot(PROFILE_DIR)["file_count"] != EXPECTED_PROFILE_FILE_COUNT:
        raise RuntimeError(f"本院画像目录文件数不是 {EXPECTED_PROFILE_FILE_COUNT}")
    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("TRIAL 前正式照片目录已存在")
    return rows


def select_trial_rows(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_name: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_name.setdefault(clean_text(row.get("姓名")), []).append(row)

    success_rows: list[dict[str, Any]] = []
    for expected_name, expected_level in SUCCESS_SAMPLE_PLAN:
        matches = by_name.get(expected_name, [])
        if len(matches) != 1:
            raise RuntimeError(f"成功样本姓名范围不唯一：{expected_name} 数量={len(matches)}")
        row = dict(matches[0])
        actual_level = title_level(row.get("职称身份原文"))
        if actual_level != expected_level:
            raise RuntimeError(
                f"成功样本职称层级漂移：{expected_name} 应为 {expected_level} 实际 {actual_level}"
            )
        success_rows.append(row)

    failure_rows: list[dict[str, Any]] = []
    for expected_name, expected_url in FAILURE_EVIDENCE_PLAN:
        matches = by_name.get(expected_name, [])
        if len(matches) != 1:
            raise RuntimeError(f"失败证据姓名范围不唯一：{expected_name} 数量={len(matches)}")
        row = dict(matches[0])
        if clean_text(row.get("来源链接")) != expected_url:
            raise RuntimeError(f"失败证据 URL 漂移：{expected_name}")
        if title_level(row.get("职称身份原文")) != "其他":
            raise RuntimeError(f"失败证据职称层级不再是其他：{expected_name}")
        failure_rows.append(row)

    if len({atomic_department(row) for row in success_rows}) != EXPECTED_SUCCESS_COUNT:
        raise RuntimeError("成功样本未覆盖 10 个不同科室首原子")
    if Counter(title_level(row.get("职称身份原文")) for row in success_rows) != Counter(
        {"正高": 5, "副高": 5}
    ):
        raise RuntimeError("成功样本职称分层不是正高 5 / 副高 5")
    return success_rows, failure_rows


def fetch_detail_with_retry(
    session: common.OfficialSession,
    source_link: str,
    sleep_func: Callable[[float], None] = time.sleep,
) -> tuple[common.HttpResult, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    last_result: common.HttpResult | None = None
    for attempt in range(2):
        try:
            result = session.get(source_link, referer=DIRECTORY_URL)
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
        return last_result, attempts
    raise RuntimeError(f"详情连续两次请求失败：{source_link} {attempts}")


def allocate_trial_photo(
    row: dict[str, Any], extension: str, content: bytes
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
    detail_font = contact_sheet_font(15)
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
            f"{sample['department']} | {sample['primary_title']}",
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


def size_buckets(samples: list[dict[str, Any]]) -> dict[str, int]:
    return common.size_buckets(samples)


MANIFEST_FIELDS = [
    "record_type",
    "name",
    "department",
    "primary_title",
    "title_level",
    "source_link",
    "detail_id",
    "detail_status",
    "detail_probe_utc",
    "detail_attempts",
    "outcome",
    "failure_state",
    "focal_point_480_reference_count",
    "media_candidate_count",
    "detection_feature",
    "excluded_resource_urls",
    "photo_url",
    "itok",
    "path_kind",
    "filename",
    "bytes",
    "sha256",
    "extension",
    "width",
    "height",
    "photo_status",
    "photo_final_url",
]


def write_manifest(records: list[dict[str, Any]]) -> None:
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for record in records:
            row = {key: record.get(key, "") for key in MANIFEST_FIELDS}
            for key in ("detail_attempts", "excluded_resource_urls"):
                row[key] = json.dumps(row[key], ensure_ascii=False, separators=(",", ":"))
            writer.writerow(row)


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    success_lines = "\n".join(
        f"- {item['name']}｜{item['department']}｜{item['primary_title']}｜"
        f"{item['bytes']:,} bytes｜{item['width']}×{item['height']}｜"
        f"`{item['sha256']}`｜itok `{item['itok']}`"
        for item in payload["photo_samples"]
    )
    failure_sections: list[str] = []
    for item in payload["failure_evidence"]:
        resources = "\n".join(
            f"  - {resource['url']}｜{resource['feature']}"
            for resource in item["excluded_resources"]
        )
        failure_sections.append(
            f"- {item['name']}｜{item['source_link']}｜HTTP {item['detail_status']}｜"
            f"UTC `{item['detail_probe_utc']}`｜`{item['failure_state']}`｜"
            f"{item['detection_feature']}\n{resources}"
        )
    owner_large = [item for item in payload["photo_samples"] if item["bytes"] > OWNER_REPORT_BYTES]
    owner_lines = "\n".join(
        f"- {item['name']}｜{item['photo_url']}｜{item['bytes']:,} bytes｜"
        f"{item['width']}×{item['height']}｜`{item['sha256']}`"
        for item in owner_large
    ) or "- 无"
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 TRIAL 报告

## 门禁与范围

- Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
- 医院官网：{OFFICIAL_HOME}
- 医生目录：{DIRECTORY_URL}
- 固定范围：{meta['scope_count']} 行 / {meta['unique_source_count']} 个唯一 `/node/<ID>`；TRIAL 前照片字段非空 {meta['baseline_photo_filled_count']}。
- Owner 裁决：10 张成功照片采用正高 5 + 副高 5、覆盖 10 个不同科室首原子；另以 2 条“其他”层无照片记录验证失败留证。
- TRIAL 对账：{meta['reconciliation_count']} 行 = 成功 {meta['photo_success_count']} + 失败留证 {meta['failure_evidence_count']}。

## 来源与字节边界

- 只解析 `{meta['template_signature']}` 中页面实际引用的 `styles/focal_point_480` URL，并保留每个 URL 唯一的 `itok`；不构造原图路径。
- 公共 `styles/mini200`、banner、inline-images、default_images 和装饰资源下载数：{meta['trial_excluded_reference_download_count']}。
- 页面未引用路径探测：{meta['constructed_unreferenced_probe_count']}；第三方来源：{meta['third_party_source_count']}。
- 正式资产前后快照一致：{meta['protected_assets_before'] == meta['protected_assets_after']}。

## 成功结果

- 详情成功 {meta['detail_success_count']}/12；照片成功 {meta['photo_success_count']}/10；职称分层 {json.dumps(meta['success_title_level_counts'], ensure_ascii=False)}。
- 总字节 {meta['total_bytes']:,}；最小 {meta['min_bytes']:,}；中位数 {meta['median_bytes']:,}；平均 {meta['average_bytes']:,}；最大 {meta['max_bytes']:,}。
- 大小分桶：{json.dumps(meta['size_buckets'], ensure_ascii=False)}；>5 MiB owner 清单 {meta['over_5mib_count']}；>20 MiB {meta['over_20mib_count']}。
- 按样本平均值线性估算 860 行：{meta['estimated_scope_bytes']:,} bytes（{meta['estimated_scope_mib']:.2f} MiB），仅作容量估算。
- 联系表视觉状态：`{meta['visual_review_status']}`。

{success_lines}

## 两条失败路径证据

{chr(10).join(failure_sections)}

两条记录均未下载照片字节、未创建照片文件；其 5 个 `mini200` URL 只作为排除证据记录。

## >5 MiB owner 终审清单

{owner_lines}

## 正式资产保护与停止点

- 入口台账、总底表 JSON/CSV/XLSX、更新报告、861 个本院文件聚合快照与不存在的正式照片目录在 TRIAL 前后完全一致。
- TRIAL 只写 `work/` 工件；未回填三载体、未刷新画像、未创建正式照片目录。
- 工件完成后停止，等待 owner 审计；未取得明确 `FULL_APPEND_AND_OBSIDIAN` 前不得写正式资产。
"""
    TRIAL_REPORT_PATH.write_text(report, encoding="utf-8")


def validate_failure_evidence(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    expected_names = [item[0] for item in FAILURE_EVIDENCE_PLAN]
    if [item.get("name") for item in records] != expected_names:
        errors.append("失败证据姓名或顺序漂移")
    for item in records:
        if item.get("failure_state") != "无照片容器":
            errors.append(f"失败状态不是无照片容器：{item.get('name')}")
        if item.get("detail_status") != 200:
            errors.append(f"失败证据 HTTP 不是 200：{item.get('name')}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", clean_text(item.get("detail_probe_utc"))):
            errors.append(f"失败证据 UTC 缺失：{item.get('name')}")
        if item.get("focal_point_480_reference_count") != 0:
            errors.append(f"失败证据 focal_point_480 不是 0：{item.get('name')}")
        if item.get("media_candidate_count") != 5:
            errors.append(f"失败证据 media 候选不是 5：{item.get('name')}")
        resources = item.get("excluded_resources", [])
        if len(resources) != 5:
            errors.append(f"失败证据公共资源不是 5：{item.get('name')}")
        for resource in resources:
            url = clean_text(resource.get("url"))
            if comparable_host(url) != OFFICIAL_HOST or "/styles/mini200/" not in urlparse(url).path:
                errors.append(f"失败证据资源越界：{item.get('name')} {url}")
        feature = clean_text(item.get("detection_feature"))
        if "focal_point_480 引用数=0" not in feature or "/styles/mini200/" not in feature:
            errors.append(f"失败判定特征不完整：{item.get('name')}")
        if any(item.get(key) for key in ("photo_url", "filename", "bytes", "sha256")):
            errors.append(f"失败证据意外包含照片工件：{item.get('name')}")
    return errors


def validate_payload(payload: dict[str, Any], require_visual_pass: bool) -> None:
    meta = payload.get("meta", {})
    samples = payload.get("photo_samples", [])
    failures = payload.get("failure_evidence", [])
    records = payload.get("trial_records", [])
    errors: list[str] = []
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围不是 860 行")
    if meta.get("photo_success_count") != EXPECTED_SUCCESS_COUNT:
        errors.append("成功照片不是 10 张")
    if meta.get("failure_evidence_count") != EXPECTED_FAILURE_EVIDENCE_COUNT:
        errors.append("失败证据不是 2 条")
    if meta.get("reconciliation_count") != EXPECTED_RECONCILIATION_COUNT:
        errors.append("TRIAL 对账不是 12 行")
    if meta.get("department_coverage_count") != EXPECTED_SUCCESS_COUNT:
        errors.append("成功样本未覆盖 10 个科室首原子")
    if meta.get("success_title_level_counts") != {"正高": 5, "副高": 5}:
        errors.append("成功样本职称分层不是正高 5 / 副高 5")
    if meta.get("failure_title_level_counts") != {"其他": 2}:
        errors.append("失败证据职称分层不是其他 2")
    if meta.get("path_kind_counts") != {"focal_point_480": 10}:
        errors.append("成功样本不是 10 个 focal_point_480 引用")
    if any(
        meta.get(key) != 0
        for key in (
            "detail_failure_count",
            "placeholder_count",
            "photo_failure_count",
            "status_flicker_count",
            "over_20mib_count",
            "trial_excluded_reference_download_count",
            "constructed_unreferenced_probe_count",
            "third_party_source_count",
        )
    ):
        errors.append("TRIAL 存在异常失败、闪烁、越界或排除资源下载")
    if meta.get("no_photo_container_count") != 2:
        errors.append("无照片容器计数不是 2")
    if meta.get("protected_assets_before") != meta.get("protected_assets_after"):
        errors.append("正式资产发生变化")
    if require_visual_pass and meta.get("visual_review_status") != VISUAL_PASS:
        errors.append("联系表尚未人工视觉通过")
    expected_success_names = [item[0] for item in SUCCESS_SAMPLE_PLAN]
    if [item.get("name") for item in samples] != expected_success_names:
        errors.append("成功样本姓名或顺序漂移")
    if len(records) != EXPECTED_RECONCILIATION_COUNT:
        errors.append("payload trial_records 不是 12 行")
    if [item.get("record_type") for item in records] != ["success"] * 10 + ["failure_evidence"] * 2:
        errors.append("trial_records 类型或顺序漂移")
    errors.extend(validate_failure_evidence(failures))
    hashes: set[str] = set()
    for sample in samples:
        relative = Path(sample.get("disk_path", ""))
        path = ROOT / relative
        try:
            path.relative_to(TRIAL_PHOTO_DIR)
        except ValueError:
            errors.append(f"照片不在 TRIAL 目录：{relative}")
            continue
        if not path.is_file():
            errors.append(f"照片不存在：{relative}")
            continue
        content = path.read_bytes()
        if len(content) != sample.get("bytes"):
            errors.append(f"照片字节不一致：{path.name}")
        digest = hashlib.sha256(content).hexdigest()
        if digest != sample.get("sha256"):
            errors.append(f"照片 SHA-256 不一致：{path.name}")
        if digest in hashes:
            errors.append(f"照片 SHA-256 重复：{path.name}")
        hashes.add(digest)
        extension = common.magic_extension(content, sample.get("content_type"))
        if extension != sample.get("extension"):
            errors.append(f"照片魔数/扩展名不一致：{path.name}")
        if common.image_dimensions(content) != (sample.get("width"), sample.get("height")):
            errors.append(f"照片尺寸不一致：{path.name}")
        url, kind, itok = page_referenced_photo_url(
            sample.get("photo_url", ""), sample.get("source_link", "")
        )
        if (url, kind, itok) != (
            sample.get("photo_url"),
            sample.get("path_kind"),
            sample.get("itok"),
        ):
            errors.append(f"照片 URL/itok 越界：{path.name}")
        if comparable_host(sample.get("photo_final_url", "")) != OFFICIAL_HOST:
            errors.append(f"照片最终响应越出官网：{path.name}")
    if require_visual_pass and not CONTACT_SHEET_PATH.is_file():
        errors.append("联系表缺失")
    if errors:
        raise RuntimeError("TRIAL 验证失败：\n- " + "\n- ".join(errors))


def validate_manifest(payload: dict[str, Any]) -> None:
    if not TRIAL_CSV_PATH.is_file():
        raise RuntimeError("TRIAL manifest 缺失")
    with TRIAL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED_RECONCILIATION_COUNT:
        raise RuntimeError(f"TRIAL manifest 不是 12 行：{len(rows)}")
    expected = payload.get("trial_records", [])
    if [row.get("name") for row in rows] != [row.get("name") for row in expected]:
        raise RuntimeError("TRIAL manifest 姓名或顺序漂移")
    if [row.get("outcome") for row in rows] != [row.get("outcome") for row in expected]:
        raise RuntimeError("TRIAL manifest outcome 漂移")


def record_base(
    row: dict[str, Any], detail: common.HttpResult, attempts: list[dict[str, Any]], analysis: MediaAnalysis
) -> dict[str, Any]:
    return {
        "name": clean_text(row.get("姓名")),
        "department": atomic_department(row),
        "primary_title": primary_title(row.get("职称身份原文")),
        "title_level": title_level(row.get("职称身份原文")),
        "source_link": clean_text(row.get("来源链接")),
        "detail_id": detail_id(row.get("来源链接")),
        "detail_status": detail.status,
        "detail_probe_utc": attempts[-1]["utc"],
        "detail_attempts": attempts,
        "detail_final_url": detail.final_url,
        "page_name": analysis.page_name,
        "page_title": analysis.page_title,
        "template_signature": analysis.template_signature,
        "focal_point_480_reference_count": analysis.focal_point_480_reference_count,
        "media_candidate_count": analysis.media_candidate_count,
        "detection_feature": analysis.detection_feature,
        "excluded_resources": list(analysis.excluded_resources),
        "excluded_resource_urls": [item["url"] for item in analysis.excluded_resources],
    }


def run_trial(run_date: str) -> dict[str, Any]:
    before = protected_snapshot()
    rows = load_scope_rows()
    success_rows, failure_rows = select_trial_rows(rows)
    for path in (TRIAL_JSON_PATH, TRIAL_CSV_PATH, TRIAL_REPORT_PATH, CONTACT_SHEET_PATH):
        if path.exists():
            raise RuntimeError(f"TRIAL 工件已存在，拒绝覆盖：{path}")
    if TRIAL_PHOTO_DIR.exists():
        if any(TRIAL_PHOTO_DIR.iterdir()):
            raise RuntimeError(f"TRIAL 照片目录非空，拒绝覆盖：{TRIAL_PHOTO_DIR}")
    else:
        TRIAL_PHOTO_DIR.mkdir(parents=False)

    session = common.OfficialSession()
    landing = session.get(OFFICIAL_HOME)
    if landing.status != 200 or landing.content_type != "text/html":
        raise RuntimeError(f"官网首页响应异常：{landing.status} {landing.content_type}")
    directory = session.get(DIRECTORY_URL, referer=OFFICIAL_HOME)
    if directory.status != 200 or directory.content_type != "text/html":
        raise RuntimeError(f"医生目录响应异常：{directory.status} {directory.content_type}")

    samples: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    status_flicker_count = 0

    for row in [*success_rows, *failure_rows]:
        source_link = clean_text(row.get("来源链接"))
        detail, attempts = fetch_detail_with_retry(session, source_link)
        statuses = {item["status"] for item in attempts if item["status"] is not None}
        if len(statuses) > 1:
            status_flicker_count += 1
        if detail.status != 200 or detail.content_type != "text/html":
            raise RuntimeError(
                f"详情响应异常：{source_link} HTTP {detail.status} {detail.content_type}"
            )
        html = detail.content.decode(detail.charset, errors="replace")
        analysis = analyze_doctor_media(html, source_link, clean_text(row.get("姓名")))
        base = record_base(row, detail, attempts, analysis)
        if row in failure_rows:
            if analysis.state != "无照片容器":
                raise RuntimeError(
                    f"Owner 指定失败证据状态漂移：{base['name']} actual={analysis.state or 'success'}"
                )
            failure = {
                **base,
                "record_type": "failure_evidence",
                "outcome": "failure_evidence",
                "failure_state": "无照片容器",
                "photo_url": "",
                "itok": "",
                "path_kind": "",
                "filename": "",
                "bytes": 0,
                "sha256": "",
                "extension": "",
                "width": "",
                "height": "",
                "photo_status": "",
                "photo_final_url": "",
            }
            failures.append(failure)
            records.append(failure)
            continue
        if analysis.state or not analysis.photo_url:
            raise RuntimeError(
                f"Owner 批准成功样本无可用照片：{base['name']} state={analysis.state}"
            )
        photo = session.get(analysis.photo_url, referer=source_link)
        if photo.status != 200:
            raise RuntimeError(f"照片响应异常：{analysis.photo_url} HTTP {photo.status}")
        if comparable_host(photo.final_url) != OFFICIAL_HOST:
            raise RuntimeError(f"照片重定向越出官网：{analysis.photo_url} -> {photo.final_url}")
        extension = common.magic_extension(photo.content, photo.content_type)
        if not extension:
            raise RuntimeError(
                f"照片响应格式异常：{analysis.photo_url} {photo.content_type}"
            )
        if len(photo.content) > MAX_PHOTO_BYTES:
            raise RuntimeError(f"照片超过 20 MiB 熔断：{analysis.photo_url} {len(photo.content)}")
        width, height = common.image_dimensions(photo.content)
        filename, disk_path = allocate_trial_photo(row, extension, photo.content)
        disk_path.write_bytes(photo.content)
        sample = {
            **base,
            "record_type": "success",
            "outcome": "success",
            "failure_state": "",
            "photo_url": analysis.photo_url,
            "itok": analysis.itok,
            "path_kind": analysis.path_kind,
            "filename": filename,
            "disk_path": disk_path.relative_to(ROOT).as_posix(),
            "bytes": len(photo.content),
            "sha256": hashlib.sha256(photo.content).hexdigest(),
            "content_type": photo.content_type,
            "extension": extension,
            "width": width,
            "height": height,
            "photo_status": photo.status,
            "photo_final_url": photo.final_url,
            "photo_redirects": list(photo.redirects),
        }
        samples.append(sample)
        records.append(sample)

    values = sorted(int(item["bytes"]) for item in samples)
    total_bytes = sum(values)
    average_bytes = total_bytes // len(values)
    median_bytes = (values[4] + values[5]) // 2
    after = protected_snapshot()
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "phase": "TRIAL",
            "hospital": HOSPITAL,
            "official_home": OFFICIAL_HOME,
            "doctor_directory": DIRECTORY_URL,
            "run_date": run_date,
            "scope_count": len(rows),
            "unique_source_count": len({clean_text(row.get("来源链接")) for row in rows}),
            "baseline_photo_filled_count": sum(
                bool(clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")))
                for row in rows
            ),
            "reconciliation_count": len(records),
            "photo_success_count": len(samples),
            "failure_evidence_count": len(failures),
            "department_coverage_count": len({item["department"] for item in samples}),
            "success_title_level_counts": dict(Counter(item["title_level"] for item in samples)),
            "failure_title_level_counts": dict(Counter(item["title_level"] for item in failures)),
            "detail_template_counts": {"node": len(records)},
            "path_kind_counts": dict(Counter(item["path_kind"] for item in samples)),
            "template_signature": samples[0]["template_signature"],
            "detail_success_count": len(records),
            "detail_failure_count": 0,
            "no_photo_container_count": len(failures),
            "placeholder_count": 0,
            "photo_failure_count": 0,
            "status_flicker_count": status_flicker_count,
            "over_5mib_count": sum(item["bytes"] > OWNER_REPORT_BYTES for item in samples),
            "over_20mib_count": sum(item["bytes"] > MAX_PHOTO_BYTES for item in samples),
            "total_bytes": total_bytes,
            "min_bytes": values[0],
            "median_bytes": median_bytes,
            "average_bytes": average_bytes,
            "max_bytes": values[-1],
            "size_buckets": size_buckets(samples),
            "estimated_scope_bytes": average_bytes * EXPECTED_SCOPE_COUNT,
            "estimated_scope_mib": average_bytes * EXPECTED_SCOPE_COUNT / (1024 * 1024),
            "cookie_names": session.cookie_names,
            "incomplete_read_retry_count": session.incomplete_read_retry_count,
            "trial_excluded_reference_download_count": 0,
            "constructed_unreferenced_probe_count": 0,
            "third_party_source_count": 0,
            "visual_review_status": "PENDING_MANUAL_CONTACT_SHEET_REVIEW",
            "protected_assets_before": before,
            "protected_assets_after": after,
        },
        "photo_samples": samples,
        "failure_evidence": failures,
        "trial_records": records,
    }
    validate_payload(payload, require_visual_pass=False)
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(records)
    build_contact_sheet(samples)
    write_report(payload)
    validate_manifest(payload)
    return payload


def load_trial_payload() -> dict[str, Any]:
    if not TRIAL_JSON_PATH.is_file():
        raise RuntimeError(f"TRIAL payload 不存在：{TRIAL_JSON_PATH}")
    return json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))


def mark_visual_pass() -> dict[str, Any]:
    payload = load_trial_payload()
    if not CONTACT_SHEET_PATH.is_file():
        raise RuntimeError("联系表不存在，不能标记视觉通过")
    payload["meta"]["visual_review_status"] = VISUAL_PASS
    validate_payload(payload, require_visual_pass=True)
    validate_manifest(payload)
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #71 中山一院照片补录 TRIAL")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trial-only", action="store_true", help="执行 10 成功 + 2 失败证据 TRIAL")
    mode.add_argument("--mark-visual-pass", action="store_true", help="人工查看联系表后标记通过")
    mode.add_argument("--validate", action="store_true", help="验证现有 TRIAL 工件")
    parser.add_argument("--run-date", default=str(date.today()), help="采集日期 YYYY-MM-DD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.trial_only:
        payload = run_trial(args.run_date)
        print(
            json.dumps(
                {
                    "status": "TRIAL_READY_FOR_MANUAL_VISUAL_REVIEW",
                    "success_photos": payload["meta"]["photo_success_count"],
                    "failure_evidence": payload["meta"]["failure_evidence_count"],
                    "manifest_rows": payload["meta"]["reconciliation_count"],
                    "payload": str(TRIAL_JSON_PATH),
                    "manifest": str(TRIAL_CSV_PATH),
                    "report": str(TRIAL_REPORT_PATH),
                    "contact_sheet": str(CONTACT_SHEET_PATH),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.mark_visual_pass:
        payload = mark_visual_pass()
        print(json.dumps({"status": payload["meta"]["visual_review_status"]}, ensure_ascii=False))
    else:
        payload = load_trial_payload()
        validate_payload(payload, require_visual_pass=True)
        validate_manifest(payload)
        if protected_snapshot() != payload["meta"]["protected_assets_after"]:
            raise RuntimeError("当前正式资产与 TRIAL 后快照不一致")
        print(
            json.dumps(
                {
                    "status": "TRIAL_VALIDATED",
                    "success_photos": len(payload["photo_samples"]),
                    "failure_evidence": len(payload["failure_evidence"]),
                    "manifest_rows": len(payload["trial_records"]),
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
