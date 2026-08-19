from __future__ import annotations

import argparse
import base64
import copy
import csv
import hashlib
import io
import json
import re
import shutil
import tempfile
import time
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable

from PIL import Image, ImageDraw, ImageOps

import gzbrain_photo_backfill_trial as trial


ROOT = trial.ROOT
WORK_DIR = trial.WORK_DIR
SOURCE_DIR = trial.SOURCE_DIR
HOSPITAL = trial.HOSPITAL
ISSUE_NUMBER = trial.ISSUE_NUMBER
MASTER_JSON_PATH = trial.MASTER_JSON_PATH
MASTER_CSV_PATH = trial.MASTER_CSV_PATH
MASTER_XLSX_PATH = trial.MASTER_XLSX_PATH
MASTER_REPORT_PATH = trial.MASTER_REPORT_PATH
LEDGER_PATH = trial.LEDGER_PATH
PROFILE_DIR = trial.PROFILE_DIR
FORMAL_PHOTO_DIR = trial.FORMAL_PHOTO_DIR

EXPECTED_SCOPE_COUNT = trial.EXPECTED_SCOPE_COUNT
EXPECTED_TRIAL_REUSE_COUNT = trial.EXPECTED_TRIAL_COUNT
EXPECTED_FRESH_COUNT = EXPECTED_SCOPE_COUNT - EXPECTED_TRIAL_REUSE_COUNT
EXPECTED_PROFILE_COUNT = EXPECTED_SCOPE_COUNT

FULL_BASENAME = f"{HOSPITAL}_photo_backfill_full"
FULL_JSON_PATH = WORK_DIR / f"{FULL_BASENAME}_payload.json"
FULL_CSV_PATH = WORK_DIR / f"{FULL_BASENAME}_reconciliation.csv"
FULL_REPORT_PATH = WORK_DIR / f"{FULL_BASENAME}_report.md"
FULL_AUDIT_SHEET_PATH = WORK_DIR / f"{FULL_BASENAME}_audit_sheet.jpg"
FULL_VISUAL_DIR = WORK_DIR / f"{FULL_BASENAME}_visual_review"
PHOTO_RELATIVE_ROOT = Path("01_试点医院") / HOSPITAL / "照片"

FULL_FAILURE_STATES = ("详情不可达", "照片资源不可达", "无照片容器", "占位图")
FULL_WARNING_BY_STATE = {
    state: f"官网本人职业照补录失败：{state}" for state in FULL_FAILURE_STATES
}
FULL_ALLOWED_ROW_COLUMNS = {"照片链接", "照片文件", "异常提示"}
FULL_AUTHORIZATION = (
    "PR #78 owner comment 2026-08-18T20:38:28Z: "
    "TRIAL_AUDIT_PASSED -> FULL_APPEND_AND_OBSIDIAN; fixed scope 183; "
    "reuse the 10 audited TRIAL originals; strict single-img page-reference gate"
)
AUTO_MARKER = "<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->"
REQUEST_MODE = "urllib-default-get/no-cookie/no-proxy/no-custom-headers"
HOME_IS_GATE = True
PULL_REQUEST_NUMBER = 78
FULL_RETRY_SECONDS = 30
VISUAL_PAGE_SIZE = 25
FULL_VISUAL_PASS_STATUS = (
    "PASSED_ALL_FULL_CONTACT_SHEETS_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS"
)
OWNER_FIX_COMMENT_UTC = "2026-08-19T01:56:51Z"
OWNER_PLACEHOLDER_DETAIL_IDS = frozenset({"765", "766"})
OWNER_PLACEHOLDER_NAMES = frozenset({"李莹珊", "李荷花"})
OWNER_PLACEHOLDER_SHA256 = (
    "42dac34e29cd304174e89e8552fadacd4a0380b9e3346b9f5c5ebf2393cb96fd"
)
OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS = {
    "15898b8d1e158a7ba97ab05ec83d6f2c90d12186c9c74d4213c203070b769cc9": {
        "name": "沈峰",
        "sources": frozenset(
            {
                "https://www.gzbrain.cn/myzj/info_itemid_102037.html",
                "https://www.gzbrain.cn/myzj/info_itemid_551.html",
            }
        ),
    }
}
DECODED_QUERY_PLACEHOLDER_MARKERS = ("blank", "placeholder", "default")

FULL_PROTECTED_FILES = (
    MASTER_REPORT_PATH,
    LEDGER_PATH,
    trial.TRIAL_JSON_PATH,
    trial.TRIAL_CSV_PATH,
    trial.TRIAL_REPORT_PATH,
    trial.CONTACT_SHEET_PATH,
)


def row_value(value: Any) -> str:
    return "" if value is None else str(value)


def file_digest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(f"受保护文件缺失：{path}")
    content = path.read_bytes()
    return {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}


def immutable_snapshot() -> dict[str, Any]:
    return {
        "files": {str(path): file_digest(path) for path in FULL_PROTECTED_FILES},
        "trial_photo_tree": trial.tree_snapshot(trial.TRIAL_PHOTO_DIR),
    }


def append_warning(value: Any, state: str) -> str:
    if state not in FULL_WARNING_BY_STATE:
        raise ValueError(f"未知失败分类：{state}")
    warning = FULL_WARNING_BY_STATE[state]
    warnings = [trial.clean_text(item) for item in trial.clean_text(value).split("；")]
    warnings = [item for item in warnings if item]
    if warning not in warnings:
        warnings.append(warning)
    return "；".join(warnings)


def allocate_full_photo_path(
    row: dict[str, Any],
    extension: str,
    photo_root: Path,
    used_names: set[str],
    preferred_filename: str = "",
) -> tuple[str, Path]:
    if preferred_filename:
        filename = trial.safe_photo_part(preferred_filename)
        if Path(filename).suffix.lower() != f".{extension}":
            raise RuntimeError(f"TRIAL 复用文件名与实际格式不一致：{filename}")
    else:
        stem = "-".join(
            [
                trial.safe_photo_part(row.get("姓名")),
                trial.atomic_department(row),
                trial.safe_photo_part(trial.primary_title(row.get("职称身份原文"))),
                trial.safe_photo_part(HOSPITAL),
            ]
        )
        filename = f"{stem}.{extension}"
        if filename.casefold() in used_names:
            filename = f"{stem}-{trial.detail_id(row.get('来源链接'))}.{extension}"
    folded = filename.casefold()
    if folded in used_names or (photo_root / filename).exists():
        raise RuntimeError(f"FULL 照片文件名仍冲突：{filename}")
    used_names.add(folded)
    return filename, photo_root / filename


def response_signature(item: dict[str, Any]) -> str:
    if item.get("error"):
        return f"ERROR {item['error']}"
    return f"HTTP {item.get('status')} {item.get('content_type') or ''}"


def attempts_flicker(attempts: list[dict[str, Any]]) -> bool:
    return len({response_signature(item) for item in attempts}) > 1


def fetch_with_retry(
    session: trial.OfficialUrlOpenSession,
    url: str,
    accept: Callable[[trial.HttpResult], bool],
    sleep_func: Callable[[float], None] = time.sleep,
) -> tuple[trial.HttpResult | None, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    last_result: trial.HttpResult | None = None
    for attempt_index in range(2):
        try:
            result = session.get(url)
            last_result = result
            attempts.append(
                {
                    "attempt": attempt_index + 1,
                    "utc": trial.utc_now(),
                    "status": result.status,
                    "content_type": result.content_type,
                    "final_url": result.final_url,
                    "error": "",
                }
            )
            if accept(result):
                return result, attempts
        except RuntimeError as exc:
            attempts.append(
                {
                    "attempt": attempt_index + 1,
                    "utc": trial.utc_now(),
                    "status": None,
                    "content_type": "",
                    "final_url": "",
                    "error": str(exc),
                }
            )
        if attempt_index == 0:
            sleep_func(FULL_RETRY_SECONDS)
    return last_result, attempts


def validate_failure_attempts(attempts: list[dict[str, Any]]) -> None:
    if len(attempts) != 2:
        raise RuntimeError("失败证据必须包含 2 次请求")
    parsed = [datetime.fromisoformat(str(item["utc"]).replace("Z", "+00:00")) for item in attempts]
    if (parsed[1] - parsed[0]).total_seconds() < FULL_RETRY_SECONDS - 0.5:
        raise RuntimeError("失败请求间隔不足 30 秒")


def placeholder_response_reason(
    photo_url: str, content: bytes, width: int, height: int
) -> str:
    path = trial.unquote(trial.urlparse(photo_url).path).casefold()
    for marker in trial.PLACEHOLDER_PATH_MARKERS:
        if marker in path:
            return f"URL 路径命中占位标记：{marker}"
    decoded_query = decoded_photo_query(photo_url)
    lowered_query = decoded_query.casefold()
    for marker in DECODED_QUERY_PLACEHOLDER_MARKERS:
        if marker in lowered_query:
            return f"URL query Base64 解码命中占位标记：{decoded_query}"
    unique_colors = limited_unique_color_count(content, limit=2)
    if unique_colors <= 2:
        return f"全图唯一颜色数={unique_colors}，命中单色/近单色占位启发式"
    if len(content) <= 10 * 1024 and width <= 128 and height <= 128:
        return f"响应呈小尺寸占位图特征：{len(content)} bytes；{width}×{height}"
    return ""


def decoded_photo_query(photo_url: str) -> str:
    query = trial.clean_text(trial.urlparse(photo_url).query)
    if not query or not re.fullmatch(r"[A-Za-z0-9_+/=-]+", query):
        return ""
    padded = query + "=" * (-len(query) % 4)
    try:
        decoded = base64.b64decode(padded, altchars=b"-_", validate=True)
        return decoded.decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return ""


def limited_unique_color_count(content: bytes, limit: int = 2) -> int:
    with Image.open(io.BytesIO(content)) as image:
        image.load()
        colors = image.convert("RGBA").getcolors(maxcolors=limit + 1)
    return limit + 1 if colors is None else len(colors)


def cross_doctor_duplicate_sha_groups(
    samples: list[dict[str, Any]],
) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for sample in samples:
        digest = trial.clean_text(sample.get("sha256"))
        grouped.setdefault(digest, []).append(
            {
                "name": trial.clean_text(sample.get("name")),
                "source_link": trial.clean_text(sample.get("source_link")),
            }
        )
    rejected: dict[str, list[dict[str, str]]] = {}
    for digest, items in grouped.items():
        if not digest or len(items) < 2:
            continue
        approved = OWNER_APPROVED_SAME_DOCTOR_DUPLICATE_GROUPS.get(digest)
        names = {item["name"] for item in items}
        sources = {item["source_link"] for item in items}
        if (
            approved is not None
            and names == {approved["name"]}
            and sources == set(approved["sources"])
        ):
            continue
        rejected[digest] = items
    return rejected


def analyze_full_doctor_media(
    html: str, source_link: str, expected_name: str
) -> trial.MediaAnalysis:
    try:
        return trial.analyze_doctor_media(html, source_link, expected_name)
    except RuntimeError as exc:
        if "医生照片容器 URL 越界" not in str(exc):
            raise
    soup = trial.BeautifulSoup(html, "html.parser")
    single_con = soup.select_one("div.single_con")
    single_cn = (
        single_con.find("div", class_="single_cn", recursive=False)
        if single_con is not None
        else None
    )
    header = (
        single_con.find("div", class_="single-header", recursive=False)
        if single_con is not None
        else None
    )
    photo_container = (
        single_cn.find("div", class_="single-img", recursive=False)
        if single_cn is not None
        else None
    )
    images = photo_container.find_all("img", recursive=False) if photo_container else []
    if header is None or len(images) != 1 or not trial.clean_text(images[0].get("src")):
        raise RuntimeError(f"FULL 非标准照片容器无法归类：{source_link}")
    name_node = header.find("h2")
    title_node = header.find("h3")
    page_name = trial.clean_text(name_node.get_text(" ", strip=True) if name_node else "")
    page_title = trial.clean_text(title_node.get_text(" ", strip=True) if title_node else "")
    if page_name != trial.clean_text(expected_name):
        raise RuntimeError(f"医生详情标题与底表姓名不一致：{source_link}")
    raw_url = trial.clean_text(images[0].get("src"))
    absolute = trial.urljoin(source_link, raw_url)
    parsed = trial.urlparse(absolute)
    path = trial.unquote(parsed.path).casefold()
    base_valid = (
        parsed.scheme == "https"
        and trial.comparable_host(absolute) == trial.OFFICIAL_HOST
        and not parsed.fragment
        and bool(parsed.query)
        and bool(trial.OPAQUE_QUERY_RE.fullmatch(parsed.query))
        and path.startswith("/uploadfiles/")
    )
    snippet = trial.clean_text(str(photo_container))
    if base_valid and path == "/uploadfiles/image/doctor_img1.jpg":
        return trial.MediaAnalysis(
            page_name=page_name,
            page_title=page_title,
            state="占位图",
            photo_url="",
            opaque_query="",
            template_signature=trial.TEMPLATE_SIGNATURE,
            photo_reference_count=1,
            single_con_image_count=len(single_con.find_all("img")),
            outside_image_reference_count=max(0, len(soup.find_all("img", src=True)) - 1),
            excluded_resource_examples=(
                {
                    "url": absolute,
                    "reason": "占位图",
                    "feature": "strict container references generic doctor_img1.jpg default",
                },
            ),
            container_html_snippet=snippet,
            detection_feature="strict container references generic doctor_img1.jpg default",
        )
    if base_valid and path.endswith(".bmp"):
        return trial.MediaAnalysis(
            page_name=page_name,
            page_title=page_title,
            state="",
            photo_url=absolute,
            opaque_query=parsed.query,
            template_signature=trial.TEMPLATE_SIGNATURE,
            photo_reference_count=1,
            single_con_image_count=len(single_con.find_all("img")),
            outside_image_reference_count=max(0, len(soup.find_all("img", src=True)) - 1),
            excluded_resource_examples=(),
            container_html_snippet=snippet,
            detection_feature=(
                "strict container same-site page-referenced BMP; download only to determine "
                "placeholder before abnormal-format fuse"
            ),
        )
    raise RuntimeError(f"医生照片容器 URL 越界：{source_link} {raw_url}")


def failure_evidence_text(evidence: dict[str, Any]) -> str:
    return json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_master_row(row: dict[str, Any], headers: list[str]) -> tuple[str, ...]:
    return tuple(row_value(row.get(header)) for header in headers)


def collect_full_row_diffs(
    before_rows: list[dict[str, Any]],
    after_rows: list[dict[str, Any]],
    target_sources: set[str],
    headers: list[str],
) -> list[dict[str, str]]:
    if len(before_rows) != len(after_rows):
        raise RuntimeError("FULL 前后总底表行数发生变化")
    diffs: list[dict[str, str]] = []
    for sheet_row, (before, after) in enumerate(
        zip(before_rows, after_rows, strict=True), start=2
    ):
        for column in headers:
            old = row_value(before.get(column))
            new = row_value(after.get(column))
            if old == new:
                continue
            source = trial.clean_text(after.get("来源链接"))
            if source not in target_sources:
                raise RuntimeError(f"发现 Issue #77 范围外行修改：{source} {column}")
            diffs.append(
                {
                    "底表行": str(sheet_row),
                    "序号": trial.clean_text(after.get("序号")),
                    "姓名": trial.clean_text(after.get("姓名")),
                    "来源链接": source,
                    "列名": column,
                    "修改前": old,
                    "修改后": new,
                }
            )
    unexpected = sorted({item["列名"] for item in diffs} - FULL_ALLOWED_ROW_COLUMNS)
    if unexpected:
        raise RuntimeError("发现范围外字段修改：" + "、".join(unexpected))
    return diffs


def recompute_master_derivatives(payload: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    import collect_official_doctors_batch as collector

    warnings: Counter[str] = Counter()
    for row in rows:
        for warning in trial.clean_text(row.get("异常提示")).split("；"):
            if warning:
                warnings[warning] += 1
    payload["warning_counts"] = dict(warnings)
    payload["hospital_batches"] = collector.build_hospital_batches(rows)


def write_master_csv(path: Path, rows: list[dict[str, Any]], headers: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in headers} for row in rows)


def validate_master_layers(
    payload_path: Path, csv_path: Path, xlsx_path: Path
) -> list[dict[str, Any]]:
    import collect_official_doctors_batch as collector
    import generate_obsidian_profiles as profiles

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    payload_rows = payload.get("rows", [])
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    xlsx_rows = profiles.read_xlsx_rows_basic(xlsx_path)
    headers = list(collector.BASE_HEADERS)
    expected = [canonical_master_row(row, headers) for row in payload_rows]
    if [canonical_master_row(row, headers) for row in csv_rows] != expected:
        raise RuntimeError("总底表 payload 与 CSV 不一致")
    if [canonical_master_row(row, headers) for row in xlsx_rows] != expected:
        raise RuntimeError("总底表 payload 与 XLSX 自动采集底表不一致")
    return [dict(row) for row in payload_rows]


def write_reconciliation_csv(path: Path, payload: dict[str, Any]) -> None:
    headers = [
        "详情ID",
        "姓名",
        "来源链接",
        "状态",
        "失败分类",
        "照片引用数",
        "照片链接",
        "照片文件",
        "声明格式",
        "实际格式",
        "字节数",
        "SHA-256",
        "宽",
        "高",
        "来源批次",
        "错误证据",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(
            {header: item.get(header, "") for header in headers}
            for item in payload["reconciliation"]
        )


def profile_photo_markdown_path(photo_file: str) -> str:
    markdown_path = "/".join(Path(photo_file.replace("\\", "/")).parts[-2:])
    if not markdown_path.startswith("照片/"):
        raise RuntimeError(f"画像照片相对路径越界：{photo_file}")
    return markdown_path


def insert_profile_photo_block(
    before_text: str, doctor_name: str, photo_file: str
) -> str:
    markdown_path = profile_photo_markdown_path(photo_file)
    if re.search(r"(?m)^!\[[^\]]*\]\(照片/[^)]+\)[ \t\r]*$", before_text):
        raise RuntimeError(f"画像已存在照片嵌入区块：{doctor_name}")
    marker = re.compile(r"(?m)^## 基础信息[ \t]*(?P<newline>\r\n|\n)(?P=newline)")
    matches = list(marker.finditer(before_text))
    if len(matches) != 1:
        raise RuntimeError(f"画像基础信息插入点不唯一：{doctor_name} 数量={len(matches)}")
    match = matches[0]
    newline = match.group("newline")
    block = f"![{doctor_name}]({markdown_path}){newline}{newline}"
    return before_text[: match.end()] + block + before_text[match.end() :]


def insert_profile_photo_block_bytes(
    before_bytes: bytes, doctor_name: str, photo_file: str
) -> bytes:
    bom = b"\xef\xbb\xbf" if before_bytes.startswith(b"\xef\xbb\xbf") else b""
    body = before_bytes[len(bom) :]
    try:
        before_text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"画像不是有效 UTF-8：{doctor_name}") from exc
    return bom + insert_profile_photo_block(before_text, doctor_name, photo_file).encode(
        "utf-8"
    )


def remove_profile_photo_block_bytes(
    after_bytes: bytes, doctor_name: str, photo_file: str
) -> bytes:
    bom = b"\xef\xbb\xbf" if after_bytes.startswith(b"\xef\xbb\xbf") else b""
    body = after_bytes[len(bom) :]
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"画像不是有效 UTF-8：{doctor_name}") from exc
    markdown_path = profile_photo_markdown_path(photo_file)
    pattern = re.compile(
        rf"(?m)^!\[{re.escape(doctor_name)}\]\({re.escape(markdown_path)}\)"
        r"(?P<newline>\r\n|\n)(?P=newline)"
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"画像待回滚照片区块不唯一：{doctor_name} 数量={len(matches)}")
    match = matches[0]
    return bom + (text[: match.start()] + text[match.end() :]).encode("utf-8")


def validate_profile_photo_only_bytes(
    before_bytes: bytes, after_bytes: bytes, doctor_name: str, photo_file: str
) -> None:
    expected = insert_profile_photo_block_bytes(before_bytes, doctor_name, photo_file)
    if after_bytes != expected:
        raise RuntimeError(f"画像出现照片嵌入区块以外字节变化：{doctor_name}")
    before_lines = before_bytes.decode("utf-8-sig").splitlines()
    after_lines = after_bytes.decode("utf-8-sig").splitlines()
    if len(after_lines) - len(before_lines) != 2:
        raise RuntimeError(f"画像照片最小刷新不是 +2/-0：{doctor_name}")


def profile_markdown_tree(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes() for path in sorted(root.rglob("*.md"))
    }


def validate_profile_tree_surgical(
    before_tree: dict[Path, bytes],
    after_root: Path,
    expected_changed_paths: set[Path],
) -> None:
    after_tree = profile_markdown_tree(after_root)
    if set(after_tree) != set(before_tree):
        raise RuntimeError("画像 Markdown 文件集合发生变化")
    changed = {path for path, content in before_tree.items() if after_tree[path] != content}
    if changed != expected_changed_paths:
        delta = sorted(str(path) for path in changed ^ expected_changed_paths)
        raise RuntimeError("画像外科式变更集合不一致：" + "、".join(delta[:5]))


def target_profile_paths(
    profile_root: Path, target_sources: set[str]
) -> dict[str, Path]:
    import generate_obsidian_profiles as profiles

    sources = profiles.extract_existing_sources(profile_root)
    missing = target_sources - set(sources)
    if missing:
        raise RuntimeError("FULL 前目标范围缺少既有画像：" + "、".join(sorted(missing)[:5]))
    result = {source: sources[source] for source in target_sources}
    profile_files = {
        path for path in profile_root.glob("*.md") if path.name != "_索引.md"
    }
    if (
        len(result) != EXPECTED_PROFILE_COUNT
        or len(profile_files) != EXPECTED_PROFILE_COUNT
        or set(result.values()) != profile_files
    ):
        raise RuntimeError("FULL 前 183 个来源与 183 份画像不是一一对应")
    return result


def preflight_profile_bytes(
    profile_paths: dict[str, Path], rows_by_source: dict[str, dict[str, Any]]
) -> dict[str, bytes]:
    before: dict[str, bytes] = {}
    probe_file = (PHOTO_RELATIVE_ROOT / "__preflight__.jpg").as_posix()
    marker = AUTO_MARKER.encode("utf-8")
    for source, path in profile_paths.items():
        content = path.read_bytes()
        name = trial.clean_text(rows_by_source[source].get("姓名"))
        if marker not in content:
            raise RuntimeError(f"画像缺少 AUTO 标记：{name}")
        insert_profile_photo_block_bytes(content, name, probe_file)
        before[source] = content
    return before


def select_audit_samples(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(samples) < 10:
        raise RuntimeError("FULL 成功照片不足 10 张，无法生成抽样拼图")
    smallest = min(samples, key=lambda item: (int(item["bytes"]), item["source_link"]))
    largest = max(samples, key=lambda item: (int(item["bytes"]), item["source_link"]))
    remaining = [item for item in samples if item not in (smallest, largest)]
    random_like = sorted(
        remaining,
        key=lambda item: hashlib.sha256(item["source_link"].encode("utf-8")).hexdigest(),
    )[:8]
    selected = [{**smallest, "audit_kind": "最小"}, {**largest, "audit_kind": "最大"}]
    selected.extend({**item, "audit_kind": "确定性随机"} for item in random_like)
    return selected


def draw_review_sheet(
    selected: list[dict[str, Any]], photo_root: Path, output_path: Path, columns: int = 5
) -> None:
    cell_width, cell_height = 336, 430
    rows = (len(selected) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_width, rows * cell_height), "white")
    draw = ImageDraw.Draw(canvas)
    name_font = trial.contact_sheet_font(22)
    meta_font = trial.contact_sheet_font(14)
    for index, item in enumerate(selected):
        row, col = divmod(index, columns)
        left, top = col * cell_width + 18, row * cell_height + 8
        photo_path = photo_root / item["filename"]
        content = photo_path.read_bytes()
        visibility_reason = placeholder_response_reason(
            item["photo_url"], content, int(item["width"]), int(item["height"])
        )
        if visibility_reason:
            raise RuntimeError(
                "CONTACT_SHEET_BLANK_OR_INVISIBLE_CELL_REQUIRES_MANUAL_REVIEW: "
                f"{item['name']} {visibility_reason}"
            )
        with Image.open(io.BytesIO(content)) as image:
            image.load()
            preview = ImageOps.contain(image.convert("RGB"), (300, 315))
        x = left + (300 - preview.width) // 2
        draw.rectangle(
            (left - 2, top - 2, left + 302, top + 317),
            fill="#e6e6e6",
            outline="#555555",
            width=2,
        )
        canvas.paste(preview, (x, top))
        draw.rectangle(
            (x - 1, top - 1, x + preview.width, top + preview.height),
            outline="#333333",
            width=1,
        )
        label = item.get("audit_kind") or f"#{index + 1}"
        draw.text((left, top + 320), f"{label}｜{item['name']}", fill="black", font=name_font)
        draw.text(
            (left, top + 353),
            f"{item['department']}｜{item['title']}",
            fill="#333333",
            font=meta_font,
        )
        draw.text(
            (left, top + 380),
            f"{item['width']}×{item['height']}｜{int(item['bytes']):,} B",
            fill="#555555",
            font=meta_font,
        )
    canvas.save(output_path, "JPEG", quality=92)


def build_full_audit_sheet(
    samples: list[dict[str, Any]], photo_root: Path, output_path: Path
) -> list[dict[str, Any]]:
    selected = select_audit_samples(samples)
    draw_review_sheet(selected, photo_root, output_path)
    return [
        {
            "audit_kind": item["audit_kind"],
            "name": item["name"],
            "source_link": item["source_link"],
            "filename": item["filename"],
            "bytes": item["bytes"],
            "sha256": item["sha256"],
        }
        for item in selected
    ]


def build_visual_review_sheets(
    samples: list[dict[str, Any]], photo_root: Path, output_root: Path
) -> list[dict[str, Any]]:
    output_root.mkdir()
    ordered = sorted(samples, key=lambda item: int(item["detail_id"]))
    sheets: list[dict[str, Any]] = []
    for start in range(0, len(ordered), VISUAL_PAGE_SIZE):
        page = ordered[start : start + VISUAL_PAGE_SIZE]
        path = output_root / f"page_{start // VISUAL_PAGE_SIZE + 1:02d}.jpg"
        draw_review_sheet(page, photo_root, path)
        content = path.read_bytes()
        sheets.append(
            {
                "path": path.name,
                "first_name": page[0]["name"],
                "last_name": page[-1]["name"],
                "count": len(page),
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    return sheets


def ensure_workspace_target(path: Path) -> None:
    root = ROOT.resolve()
    resolved = path.resolve()
    if resolved == root or root not in resolved.parents:
        raise RuntimeError(f"拒绝操作工作区外路径：{path}")


def backup_file_targets(
    targets: list[Path], backup_root: Path
) -> dict[Path, Path | None]:
    backups: dict[Path, Path | None] = {}
    backup_root.mkdir(parents=True, exist_ok=True)
    for index, target in enumerate(targets):
        ensure_workspace_target(target)
        if target.exists():
            backup = backup_root / f"{index:04d}_{target.name}"
            shutil.copy2(target, backup)
            backups[target] = backup
        else:
            backups[target] = None
    return backups


def apply_file_map(file_map: dict[Path, Path]) -> None:
    for target, source in file_map.items():
        ensure_workspace_target(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = target.with_name(f".{target.name}.issue77.tmp")
        staging.unlink(missing_ok=True)
        shutil.copy2(source, staging)
        staging.replace(target)


def restore_file_targets(backups: dict[Path, Path | None]) -> None:
    for target, backup in backups.items():
        ensure_workspace_target(target)
        staging = target.with_name(f".{target.name}.issue77.restore")
        staging.unlink(missing_ok=True)
        if backup is None:
            target.unlink(missing_ok=True)
            continue
        shutil.copy2(backup, staging)
        staging.replace(target)


def full_visual_review_report_line(meta: dict[str, Any]) -> str:
    prefix = (
        "- FULL 抽样拼图覆盖最小、最大、8 个确定性随机；全量视觉联系表 "
        f"{meta['visual_review_sheet_count']} 页覆盖 {meta['visual_review_photo_count']} 张"
    )
    if meta.get("visual_review_status") == FULL_VISUAL_PASS_STATUS:
        return (
            f"{prefix}，已由 Codex 逐页目视确认为单人医生职业照，"
            "未见患者、儿童、合影、二维码、装饰或占位图。"
        )
    return f"{prefix}，待 Codex 逐页目视确认患者红线。"


def write_full_report(path: Path, payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    state_lines = "\n".join(
        f"| {state} | {meta['failure_state_counts'].get(state, 0)} |"
        for state in FULL_FAILURE_STATES
    )
    bucket_lines = "\n".join(
        f"| {bucket} | {meta['size_bucket_counts'].get(bucket, 0)} |"
        for bucket in ("<200KiB", "200KiB-1MiB", "1-5MiB", "5-20MiB", ">20MiB")
    )
    failure_lines = "\n".join(
        f"- {item['name']}｜{item['state']}｜{item['source_link']}｜{item['error']}"
        for item in payload["failures"]
    ) or "- 无"
    large_lines = "\n".join(
        f"- {item['name']}｜{item['photo_url']}｜{int(item['bytes']):,} bytes｜"
        f"{item['width']}×{item['height']}｜`{item['sha256']}`"
        for item in payload["photo_samples"]
        if int(item["bytes"]) > trial.OWNER_REPORT_BYTES
    ) or "- 无"
    visual_review_line = full_visual_review_report_line(meta)
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 FULL 报告

> 日期：{meta['run_date']}
> Phase：`{meta['phase']}`

## 四数对账

| 固定目标 | 实采 | 失败留空 | 正式落盘 | 照片字段留空 |
|---:|---:|---:|---:|---:|
| {meta['expected_count']} | {meta['downloaded_count']} | {meta['failed_count']} | {meta['disk_photo_count']} | {meta['blank_count']} |

- 复用已审计 TRIAL：{meta['trial_reused_count']}；FULL 新抓取成功：{meta['fresh_downloaded_count']}；FULL 新抓取失败：{meta['fresh_failed_count']}；新抓取目标：{meta['fresh_target_count']}。
- 详情状态波动 {meta['detail_status_flicker_count']}；照片状态波动 {meta['photo_status_flicker_count']}；页面未引用路径探测 0；第三方来源 0。

| 失败四类 | 数量 |
|---|---:|
{state_lines}

## 失败逐条证据

{failure_lines}

## 照片与大小

| 大小分桶 | 数量 |
|---|---:|
{bucket_lines}

- 照片总字节 {meta['photo_total_bytes']:,}（{meta['photo_total_mib']:.2f} MiB）；最大 {meta['photo_max_bytes']:,} bytes。
- 超过 5 MiB {meta['over_5mib_count']}；超过 20 MiB {meta['over_20mib_count']}；声明/魔数不一致 {meta['declared_extension_mismatch_count']}。
- 实际格式：{json.dumps(meta['format_counts'], ensure_ascii=False)}；重复 SHA-256 组 {meta['duplicate_sha256_group_count']}；跨医生重复 SHA-256 组 {meta.get('cross_doctor_duplicate_sha256_group_count', 0)}。

## >5 MiB Owner 终审清单

{large_lines}

## 三载体、画像与视觉门禁

- 总底表 payload/CSV/XLSX 逐值一致；只修改本院成功行 `照片链接`、`照片文件` 与失败行 `异常提示`。
- 逐单元格变化 {meta['row_diff_count']}：{json.dumps(meta['row_diff_columns'], ensure_ascii=False)}。
- FULL reconciliation/manifest 对每张照片逐一复算字节、SHA-256、魔数/扩展名、尺寸和同站页面引用 URL；URL query Base64 占位词、全图唯一颜色数 ≤2、跨医生同 SHA 均已固化拦截；照片目录零孤儿零缺失。
- 成功 {meta['profile_refreshed_count']} 份 AUTO 画像严格 +2/-0；失败 {meta['profile_untouched_count']} 份零触碰；`_索引.md` 零修改。
{visual_review_line}
- 入口台账、总底表更新报告与全部 TRIAL 工件保持不变。

## 工件

- `{FULL_JSON_PATH.relative_to(ROOT).as_posix()}`
- `{FULL_CSV_PATH.relative_to(ROOT).as_posix()}`
- `{FULL_REPORT_PATH.relative_to(ROOT).as_posix()}`
- `{FULL_AUDIT_SHEET_PATH.relative_to(ROOT).as_posix()}`
- `{FULL_VISUAL_DIR.relative_to(ROOT).as_posix()}/`
- `{FORMAL_PHOTO_DIR.relative_to(ROOT).as_posix()}/`

## 停止点

`{meta['phase']}`。完成本地实图和工作簿目视核验、提交并推送 PR #{PULL_REQUEST_NUMBER} 后发布 `{meta.get('publication_signal', 'FULL_DONE')}`；不得自行合并、关闭 Issue 或领取下一任务。
"""
    path.write_text(report, encoding="utf-8", newline="\n")


def validate_full_payload(
    payload: dict[str, Any], photo_root: Path, audit_sheet: Path, visual_root: Path
) -> None:
    meta = payload.get("meta", {})
    expected = int(meta.get("expected_count") or 0)
    downloaded = int(meta.get("downloaded_count") or 0)
    failed = int(meta.get("failed_count") or 0)
    if (
        expected != EXPECTED_SCOPE_COUNT
        or downloaded + failed != expected
        or int(meta.get("disk_photo_count") or 0) != downloaded
        or int(meta.get("blank_count") or 0) != failed
    ):
        raise RuntimeError("FULL 四数对账未闭合")
    if (
        int(meta.get("trial_reused_count") or 0) != EXPECTED_TRIAL_REUSE_COUNT
        or int(meta.get("fresh_target_count") or 0) != EXPECTED_FRESH_COUNT
        or int(meta.get("fresh_downloaded_count") or 0)
        + int(meta.get("fresh_failed_count") or 0)
        != EXPECTED_FRESH_COUNT
    ):
        raise RuntimeError("FULL TRIAL 复用与 173 个新抓取目标未闭合")
    states = meta.get("failure_state_counts") or {}
    if set(states) != set(FULL_FAILURE_STATES) or sum(int(value) for value in states.values()) != failed:
        raise RuntimeError("FULL 失败四类未闭合")
    if any(
        int(meta.get(key) or 0)
        for key in (
            "detail_status_flicker_count",
            "photo_status_flicker_count",
            "over_20mib_count",
            "constructed_unreferenced_probe_count",
            "third_party_source_count",
        )
    ):
        raise RuntimeError("FULL 存在状态波动、越界来源或超过 20 MiB 照片")
    if meta.get("request_mode") != REQUEST_MODE or meta.get("cookie_names"):
        raise RuntimeError("FULL 网络访问模式不符合授权")
    if meta.get("immutable_before") != meta.get("immutable_after_preinstall"):
        raise RuntimeError("FULL 临时事务触碰了受保护资产")
    if int(meta.get("existing_profile_count") or 0) != EXPECTED_PROFILE_COUNT:
        raise RuntimeError("FULL 既有画像不是 183 份")
    if int(meta.get("profile_refreshed_count") or 0) != downloaded:
        raise RuntimeError("FULL 成功照片与画像刷新数不一致")
    if int(meta.get("profile_untouched_count") or 0) != failed:
        raise RuntimeError("FULL 失败画像零触碰数不一致")

    rows = payload.get("rows", [])
    reconciliation = payload.get("reconciliation", [])
    photos = payload.get("photo_samples", [])
    failures = payload.get("failures", [])
    if not (
        len(rows) == len(reconciliation) == expected
        and len(photos) == downloaded
        and len(failures) == failed
    ):
        raise RuntimeError("FULL rows/reconciliation/photo/failure 数量不闭合")
    if len({item.get("来源链接") for item in reconciliation}) != expected:
        raise RuntimeError("FULL reconciliation 来源链接不唯一")
    cross_doctor_duplicates = cross_doctor_duplicate_sha_groups(photos)
    if cross_doctor_duplicates or int(
        meta.get("cross_doctor_duplicate_sha256_group_count") or 0
    ):
        raise RuntimeError(
            "FULL 存在跨医生重复 SHA，必须拦截人工复判："
            + json.dumps(cross_doctor_duplicates, ensure_ascii=False, sort_keys=True)
        )
    duplicate_validator = globals().get("validate_owner_approved_duplicate_groups")
    if duplicate_validator is not None:
        duplicate_validator(payload)

    rows_by_source = {trial.clean_text(row.get("来源链接")): row for row in rows}
    photos_by_source = {item["source_link"]: item for item in photos}
    failures_by_source = {item["source_link"]: item for item in failures}
    actual_files = {path.name: path for path in photo_root.iterdir() if path.is_file()}
    if set(actual_files) != {item["filename"] for item in photos}:
        raise RuntimeError("FULL 照片目录存在孤儿或缺失")
    total_bytes = 0
    max_bytes = 0
    over_5 = 0
    over_20 = 0
    for item in reconciliation:
        source = trial.clean_text(item.get("来源链接"))
        row = rows_by_source[source]
        status = trial.clean_text(item.get("状态"))
        if status == "实采":
            photo = photos_by_source.get(source)
            if photo is None or trial.clean_text(item.get("失败分类")):
                raise RuntimeError(f"FULL 实采行状态不一致：{source}")
            path = actual_files[photo["filename"]]
            content = path.read_bytes()
            extension = trial.magic_extension(content, photo["content_type"])
            if (
                len(content) != int(photo["bytes"])
                or hashlib.sha256(content).hexdigest() != photo["sha256"]
                or extension != photo["extension"]
                or path.suffix.lower() != f".{extension}"
                or trial.image_dimensions(content) != (int(photo["width"]), int(photo["height"]))
            ):
                raise RuntimeError(f"FULL 照片三重对账失败：{path.name}")
            placeholder = placeholder_response_reason(
                photo["photo_url"], content, int(photo["width"]), int(photo["height"])
            )
            if placeholder:
                raise RuntimeError(f"FULL 实采照片命中占位门禁：{path.name} {placeholder}")
            normalized, opaque = trial.page_referenced_photo_url(photo["photo_url"], source)
            if (normalized, opaque) != (photo["photo_url"], photo["opaque_query"]):
                raise RuntimeError(f"FULL 照片 URL 越界：{path.name}")
            if trial.comparable_host(photo["photo_final_url"]) != trial.OFFICIAL_HOST:
                raise RuntimeError(f"FULL 照片最终响应越出官网：{path.name}")
            if row.get("照片链接") != photo["photo_url"] or row.get("照片文件") != photo["photo_file"]:
                raise RuntimeError(f"FULL 总底表照片字段不一致：{source}")
            total_bytes += len(content)
            max_bytes = max(max_bytes, len(content))
            over_5 += int(len(content) > trial.OWNER_REPORT_BYTES)
            over_20 += int(len(content) > trial.MAX_PHOTO_BYTES)
        elif status == "失败留空":
            state = trial.clean_text(item.get("失败分类"))
            failure = failures_by_source.get(source)
            if state not in FULL_FAILURE_STATES or failure is None:
                raise RuntimeError(f"FULL 失败行未归入四类：{source}")
            if trial.clean_text(row.get("照片链接")) or trial.clean_text(row.get("照片文件")):
                raise RuntimeError(f"FULL 失败行照片字段未留空：{source}")
            if FULL_WARNING_BY_STATE[state] not in trial.clean_text(row.get("异常提示")):
                raise RuntimeError(f"FULL 失败行未追加幂等异常提示：{source}")
            evidence = failure.get("evidence") or {}
            if (
                not evidence.get("resource_urls")
                or "photo_reference_count" not in evidence
                or not trial.clean_text(evidence.get("detection_feature"))
                or not trial.clean_text(evidence.get("observed_utc"))
            ):
                raise RuntimeError(f"FULL 失败证据不完整：{source}")
            if state in {"详情不可达", "照片资源不可达"}:
                validate_failure_attempts(failure.get("attempts") or [])
        else:
            raise RuntimeError(f"FULL reconciliation 状态非法：{source} {status}")
    if (
        total_bytes != int(meta.get("photo_total_bytes") or 0)
        or max_bytes != int(meta.get("photo_max_bytes") or 0)
        or over_5 != int(meta.get("over_5mib_count") or 0)
        or over_20 != int(meta.get("over_20mib_count") or 0)
        or over_20
    ):
        raise RuntimeError("FULL 图片字节或大小分桶对账失败")

    if not audit_sheet.is_file() or hashlib.sha256(audit_sheet.read_bytes()).hexdigest() != meta.get(
        "audit_sheet_sha256"
    ):
        raise RuntimeError("FULL 抽样拼图缺失或哈希不一致")
    audit_samples = payload.get("audit_samples", [])
    if len(audit_samples) != 10 or {item["audit_kind"] for item in audit_samples} != {
        "最小",
        "最大",
        "确定性随机",
    }:
        raise RuntimeError("FULL 抽样拼图未覆盖最小/最大/确定性随机")
    visual_sheets = payload.get("visual_review_sheets", [])
    if sum(int(item["count"]) for item in visual_sheets) != downloaded:
        raise RuntimeError("FULL 全量视觉联系表未覆盖全部实采照片")
    if {path.name for path in visual_root.glob("*.jpg")} != {
        item["path"] for item in visual_sheets
    }:
        raise RuntimeError("FULL 全量视觉联系表目录存在孤儿或缺失")
    for item in visual_sheets:
        content = (visual_root / item["path"]).read_bytes()
        if len(content) != int(item["bytes"]) or hashlib.sha256(content).hexdigest() != item["sha256"]:
            raise RuntimeError(f"FULL 全量视觉联系表哈希不一致：{item['path']}")


def validate_full_installation(payload: dict[str, Any]) -> None:
    import collect_official_doctors_batch as collector

    final_rows = validate_master_layers(MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH)
    validate_full_payload(payload, FORMAL_PHOTO_DIR, FULL_AUDIT_SHEET_PATH, FULL_VISUAL_DIR)
    headers = list(collector.BASE_HEADERS)
    target_rows = [row for row in final_rows if trial.clean_text(row.get("医院")) == HOSPITAL]
    if {
        trial.clean_text(row.get("来源链接")): canonical_master_row(row, headers)
        for row in target_rows
    } != {
        trial.clean_text(row.get("来源链接")): canonical_master_row(row, headers)
        for row in payload["rows"]
    }:
        raise RuntimeError("FULL payload 目标行与已落盘总底表不一致")
    target_sources = {trial.clean_text(row.get("来源链接")) for row in payload["rows"]}
    profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
    integrity = {item["source_link"]: item for item in payload.get("profile_integrity", [])}
    if len(integrity) != EXPECTED_PROFILE_COUNT:
        raise RuntimeError("FULL 画像完整性清单不是 183 条")
    for source, path in profile_paths.items():
        expected = integrity[source]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected["after_sha256"]:
            raise RuntimeError(f"FULL 画像落盘哈希不一致：{path}")
        added = 2 if expected["status"] == "实采" else 0
        if int(expected["added_lines"]) != added or int(expected["removed_lines"]):
            raise RuntimeError(f"FULL 画像行级变化不符合 +2/-0：{path}")
    if hashlib.sha256((PROFILE_DIR / "_索引.md").read_bytes()).hexdigest() != payload["meta"][
        "profile_index_before_sha256"
    ]:
        raise RuntimeError("FULL 修改了 _索引.md")
    if immutable_snapshot() != payload["meta"]["immutable_before"]:
        raise RuntimeError("FULL 修改了入口台账、总底表更新报告或 TRIAL 工件")
    with FULL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        if len(list(csv.DictReader(handle))) != EXPECTED_SCOPE_COUNT:
            raise RuntimeError("FULL reconciliation CSV 不是 183 行")


def run_full(run_date: str) -> dict[str, Any]:
    import collect_official_doctors_batch as collector

    if FORMAL_PHOTO_DIR.exists():
        raise RuntimeError("FULL 前正式照片目录已存在，拒绝覆盖")
    for path in (
        FULL_JSON_PATH,
        FULL_CSV_PATH,
        FULL_REPORT_PATH,
        FULL_AUDIT_SHEET_PATH,
        FULL_VISUAL_DIR,
    ):
        if path.exists():
            raise RuntimeError(f"FULL 工件已存在，拒绝覆盖：{path}")

    immutable_before = immutable_snapshot()
    master_payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    before_rows = copy.deepcopy(master_payload.get("rows", []))
    scope_rows = [
        dict(row)
        for row in before_rows
        if trial.clean_text(row.get("医院")) == HOSPITAL
    ]
    if len(scope_rows) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("FULL 固定范围不是 183 行")
    if any(
        trial.clean_text(row.get("照片链接")) or trial.clean_text(row.get("照片文件"))
        for row in scope_rows
    ):
        raise RuntimeError("FULL 前固定范围照片字段不是全空")
    target_sources = {trial.clean_text(row.get("来源链接")) for row in scope_rows}
    if len(target_sources) != EXPECTED_SCOPE_COUNT or any(
        not trial.detail_id(source) for source in target_sources
    ):
        raise RuntimeError("FULL 固定范围详情 URL 不唯一或越界")
    rows_by_source = {trial.clean_text(row.get("来源链接")): row for row in scope_rows}

    profile_paths = target_profile_paths(PROFILE_DIR, target_sources)
    before_profile_bytes = preflight_profile_bytes(profile_paths, rows_by_source)
    before_profile_tree = profile_markdown_tree(PROFILE_DIR)
    index_before_sha256 = hashlib.sha256((PROFILE_DIR / "_索引.md").read_bytes()).hexdigest()

    trial_payload = json.loads(trial.TRIAL_JSON_PATH.read_text(encoding="utf-8"))
    trial.validate_payload(trial_payload, require_visual_pass=True)
    trial.validate_manifest(trial_payload)
    if trial.protected_snapshot() != trial_payload["meta"]["protected_assets_after"]:
        raise RuntimeError("FULL 前正式资产与 TRIAL 后快照不一致")
    seeds = trial_payload["photo_samples"]
    seed_by_source = {trial.clean_text(item["source_link"]): item for item in seeds}
    if len(seed_by_source) != EXPECTED_TRIAL_REUSE_COUNT or not set(seed_by_source) <= target_sources:
        raise RuntimeError("FULL 复用的 10 张 TRIAL 样本范围漂移")

    session = trial.OfficialUrlOpenSession()
    home = session.get(trial.OFFICIAL_HOME)
    directory = session.get(trial.DIRECTORY_URL)
    if HOME_IS_GATE and (home.status != 200 or home.content_type != "text/html"):
        raise RuntimeError("FULL 官网首页门禁失败")
    if directory.status != 200 or directory.content_type != "text/html":
        raise RuntimeError("FULL 医生目录门禁失败")

    with tempfile.TemporaryDirectory(prefix=f"issue{ISSUE_NUMBER}_full_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_photo_dir = temp_root / "photos"
        temp_photo_dir.mkdir()
        temp_hospital_dir = temp_root / HOSPITAL
        shutil.copytree(PROFILE_DIR, temp_hospital_dir)
        used_names: set[str] = set()
        result_by_source: dict[str, dict[str, Any]] = {}
        reconciliation_by_source: dict[str, dict[str, Any]] = {}
        photo_samples: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []
        detail_status_flicker_count = 0
        photo_status_flicker_count = 0

        def add_success(
            row: dict[str, Any],
            analysis: trial.MediaAnalysis,
            detail: trial.HttpResult,
            sample: dict[str, Any],
            content: bytes,
            origin: str,
        ) -> None:
            source = trial.clean_text(row.get("来源链接"))
            extension = trial.clean_text(sample.get("extension")) or trial.magic_extension(
                content, sample.get("content_type")
            )
            if not extension:
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 照片格式异常："
                    f"{row.get('姓名')} {analysis.photo_url}"
                )
            if len(content) > trial.MAX_PHOTO_BYTES:
                raise RuntimeError(
                    "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 单图超过 20 MiB："
                    f"{row.get('姓名')} {len(content)}"
                )
            width, height = trial.image_dimensions(content)
            placeholder = placeholder_response_reason(analysis.photo_url, content, width, height)
            if placeholder:
                record_failure(
                    row,
                    "占位图",
                    [analysis.photo_url],
                    analysis.photo_reference_count,
                    placeholder,
                    sample.get("photo_attempts") or [],
                )
                return
            preferred = trial.clean_text(sample.get("filename")) if origin == "TRIAL_REUSE" else ""
            filename, disk_path = allocate_full_photo_path(
                row, extension, temp_photo_dir, used_names, preferred
            )
            disk_path.write_bytes(content)
            digest = hashlib.sha256(content).hexdigest()
            photo_file = (PHOTO_RELATIVE_ROOT / filename).as_posix()
            result_row = dict(row)
            result_row["照片链接"] = analysis.photo_url
            result_row["照片文件"] = photo_file
            result_by_source[source] = result_row
            declared = Path(trial.unquote(trial.urlparse(analysis.photo_url).path)).suffix.lower().lstrip(".")
            item = {
                "detail_id": trial.detail_id(source),
                "name": trial.clean_text(row.get("姓名")),
                "department": trial.atomic_department(row),
                "title": trial.primary_title(row.get("职称身份原文")),
                "source_link": source,
                "detail_status": detail.status,
                "detail_final_url": detail.final_url,
                "template_signature": analysis.template_signature,
                "photo_reference_count": analysis.photo_reference_count,
                "container_html_snippet": analysis.container_html_snippet,
                "detection_feature": analysis.detection_feature,
                "photo_url": analysis.photo_url,
                "opaque_query": analysis.opaque_query,
                "photo_final_url": trial.clean_text(sample.get("photo_final_url")) or analysis.photo_url,
                "photo_file": photo_file,
                "filename": filename,
                "declared_extension": declared,
                "extension": extension,
                "content_type": trial.clean_text(sample.get("content_type")),
                "bytes": len(content),
                "width": width,
                "height": height,
                "sha256": digest,
                "origin": origin,
                "photo_attempts": sample.get("photo_attempts") or [],
            }
            photo_samples.append(item)
            reconciliation_by_source[source] = {
                "详情ID": item["detail_id"],
                "姓名": item["name"],
                "来源链接": source,
                "状态": "实采",
                "失败分类": "",
                "照片引用数": analysis.photo_reference_count,
                "照片链接": analysis.photo_url,
                "照片文件": photo_file,
                "声明格式": declared,
                "实际格式": extension,
                "字节数": len(content),
                "SHA-256": digest,
                "宽": width,
                "高": height,
                "来源批次": origin,
                "错误证据": "",
            }

        def record_failure(
            row: dict[str, Any],
            state: str,
            resource_urls: list[str],
            photo_reference_count: int,
            detection_feature: str,
            attempts: list[dict[str, Any]] | None = None,
            analysis: trial.MediaAnalysis | None = None,
        ) -> None:
            source = trial.clean_text(row.get("来源链接"))
            observed = trial.clean_text((attempts or [{}])[-1].get("utc")) or trial.utc_now()
            evidence = {
                "observed_utc": observed,
                "resource_urls": [url for url in resource_urls if trial.clean_text(url)],
                "photo_reference_count": int(photo_reference_count),
                "detection_feature": detection_feature,
                "template_signature": analysis.template_signature if analysis else trial.TEMPLATE_SIGNATURE,
                "excluded_resource_examples": list(analysis.excluded_resource_examples) if analysis else [],
            }
            result_row = dict(row)
            result_row["照片链接"] = ""
            result_row["照片文件"] = ""
            result_row["异常提示"] = append_warning(result_row.get("异常提示"), state)
            result_by_source[source] = result_row
            error = failure_evidence_text(evidence)
            failure = {
                "detail_id": trial.detail_id(source),
                "name": trial.clean_text(row.get("姓名")),
                "source_link": source,
                "state": state,
                "error": error,
                "evidence": evidence,
                "attempts": attempts or [],
                "origin": "FULL_FETCH",
            }
            failures.append(failure)
            reconciliation_by_source[source] = {
                "详情ID": failure["detail_id"],
                "姓名": failure["name"],
                "来源链接": source,
                "状态": "失败留空",
                "失败分类": state,
                "照片引用数": int(photo_reference_count),
                "照片链接": "",
                "照片文件": "",
                "声明格式": "",
                "实际格式": "",
                "字节数": "",
                "SHA-256": "",
                "宽": "",
                "高": "",
                "来源批次": "FULL_FETCH",
                "错误证据": error,
            }

        for index, row in enumerate(scope_rows, start=1):
            source = trial.clean_text(row.get("来源链接"))
            detail, detail_attempts = fetch_with_retry(
                session,
                source,
                lambda result: result.status == 200 and result.content_type == "text/html",
            )
            if attempts_flicker(detail_attempts):
                detail_status_flicker_count += 1
                raise RuntimeError(
                    "STATUS_FLICKER_REQUIRES_PR_COMMENT_AND_5_ROUND_AGGREGATION: "
                    f"detail={source} attempts={detail_attempts}"
                )
            if (
                detail is None
                or detail.status != 200
                or detail.content_type != "text/html"
                or trial.comparable_host(detail.final_url) != trial.OFFICIAL_HOST
                or not trial.detail_id(detail.final_url)
            ):
                record_failure(
                    row,
                    "详情不可达",
                    [source],
                    0,
                    "fixed detail URL failed two official urllib GET attempts",
                    detail_attempts,
                )
                continue
            html = detail.content.decode(detail.charset, errors="replace")
            analysis = analyze_full_doctor_media(
                html, source, trial.clean_text(row.get("姓名"))
            )
            if not analysis.state and analysis.page_title != trial.clean_text(
                row.get("职称身份原文")
            ):
                raise RuntimeError(
                    f"详情职称与底表不一致：{source} "
                    f"expected={row.get('职称身份原文')!r} actual={analysis.page_title!r}"
                )
            if analysis.state:
                failure_state = (
                    analysis.state
                    if analysis.state in FULL_FAILURE_STATES
                    else "占位图"
                )
                record_failure(
                    row,
                    failure_state,
                    [item["url"] for item in analysis.excluded_resource_examples] or [source],
                    analysis.photo_reference_count,
                    (
                        analysis.detection_feature
                        if analysis.state in FULL_FAILURE_STATES
                        else f"strict container resource excluded as {analysis.state}: "
                        f"{analysis.detection_feature}"
                    ),
                    analysis=analysis,
                )
                continue
            seed = seed_by_source.get(source)
            if seed is not None:
                if seed["photo_url"] != analysis.photo_url:
                    raise RuntimeError(f"TRIAL 复用 URL 与 FULL 详情页漂移：{source}")
                content = (ROOT / trial.clean_text(seed["disk_path"])).read_bytes()
                if hashlib.sha256(content).hexdigest() != seed["sha256"]:
                    raise RuntimeError(f"TRIAL 复用照片哈希漂移：{source}")
                add_success(row, analysis, detail, seed, content, "TRIAL_REUSE")
            else:
                photo, photo_attempts = fetch_with_retry(
                    session, analysis.photo_url, lambda result: result.status == 200
                )
                if attempts_flicker(photo_attempts):
                    photo_status_flicker_count += 1
                    raise RuntimeError(
                        "STATUS_FLICKER_REQUIRES_PR_COMMENT_AND_5_ROUND_AGGREGATION: "
                        f"photo={analysis.photo_url} attempts={photo_attempts}"
                    )
                if (
                    photo is None
                    or photo.status != 200
                    or trial.comparable_host(photo.final_url) != trial.OFFICIAL_HOST
                ):
                    record_failure(
                        row,
                        "照片资源不可达",
                        [analysis.photo_url],
                        analysis.photo_reference_count,
                        "strict single-img page-referenced resource failed two official urllib GET attempts",
                        photo_attempts,
                        analysis,
                    )
                else:
                    try:
                        width, height = trial.image_dimensions(photo.content)
                    except Exception as exc:
                        raise RuntimeError(
                            "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 照片无法解码："
                            f"{row.get('姓名')} {analysis.photo_url}"
                        ) from exc
                    placeholder = placeholder_response_reason(
                        analysis.photo_url, photo.content, width, height
                    )
                    if placeholder:
                        record_failure(
                            row,
                            "占位图",
                            [analysis.photo_url],
                            analysis.photo_reference_count,
                            placeholder,
                            photo_attempts,
                            analysis,
                        )
                        continue
                    extension = trial.magic_extension(photo.content, photo.content_type)
                    if not extension:
                        raise RuntimeError(
                            "[FATAL - HUMAN_INTERVENTION_REQUIRED] FULL 照片格式异常："
                            f"{row.get('姓名')} {analysis.photo_url} {photo.content_type}"
                        )
                    add_success(
                        row,
                        analysis,
                        detail,
                        {
                            "extension": extension,
                            "content_type": photo.content_type,
                            "photo_final_url": photo.final_url,
                            "photo_attempts": photo_attempts,
                        },
                        photo.content,
                        "FULL_FETCH",
                    )
            if len([item for item in failures if item["state"] == "照片资源不可达"]) >= 10:
                raise RuntimeError(
                    "BULK_RESOURCE_UNREACHABLE_REQUIRES_PR_COMMENT: "
                    "同类照片资源不可达已达到 10 条"
                )
            if index % 20 == 0 or index == EXPECTED_SCOPE_COUNT:
                print(
                    f"[FULL] {index}/{EXPECTED_SCOPE_COUNT} 实采={len(photo_samples)} 失败={len(failures)}",
                    flush=True,
                )

        cross_doctor_duplicates = cross_doctor_duplicate_sha_groups(photo_samples)
        if cross_doctor_duplicates:
            raise RuntimeError(
                "CROSS_DOCTOR_DUPLICATE_SHA_REQUIRES_MANUAL_REVIEW: "
                + json.dumps(cross_doctor_duplicates, ensure_ascii=False, sort_keys=True)
            )
        duplicate_decorator = globals().get("decorate_owner_approved_duplicate_groups")
        if duplicate_decorator is not None:
            duplicate_decorator(photo_samples, reconciliation_by_source)
        if set(result_by_source) != target_sources:
            raise RuntimeError("FULL 183 行结果来源集合未闭合")
        result_rows = [result_by_source[trial.clean_text(row.get("来源链接"))] for row in scope_rows]
        reconciliation = [
            reconciliation_by_source[trial.clean_text(row.get("来源链接"))]
            for row in scope_rows
        ]
        updated_by_source = {
            trial.clean_text(row.get("来源链接")): row for row in result_rows
        }
        after_rows = [
            copy.deepcopy(updated_by_source.get(trial.clean_text(row.get("来源链接")), row))
            for row in before_rows
        ]
        headers = list(collector.BASE_HEADERS)
        row_diffs = collect_full_row_diffs(before_rows, after_rows, target_sources, headers)
        updated_master = copy.deepcopy(master_payload)
        updated_master["rows"] = after_rows
        recompute_master_derivatives(updated_master, after_rows)

        temp_master_payload = temp_root / MASTER_JSON_PATH.name
        temp_master_csv = temp_root / MASTER_CSV_PATH.name
        temp_master_xlsx = temp_root / MASTER_XLSX_PATH.name
        temp_master_preview = temp_root / "master_preview.png"
        temp_master_payload.write_text(
            json.dumps(updated_master, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_master_csv(temp_master_csv, after_rows, headers)
        collector.build_workbook(temp_master_payload, temp_master_xlsx, temp_master_preview)
        validate_master_layers(temp_master_payload, temp_master_csv, temp_master_xlsx)

        temp_profile_paths = target_profile_paths(temp_hospital_dir, target_sources)
        photos_by_source = {item["source_link"]: item for item in photo_samples}
        success_sources = set(photos_by_source)
        for source in success_sources:
            item = photos_by_source[source]
            path = temp_profile_paths[source]
            path.write_bytes(
                insert_profile_photo_block_bytes(
                    before_profile_bytes[source], item["name"], item["photo_file"]
                )
            )
            validate_profile_photo_only_bytes(
                before_profile_bytes[source], path.read_bytes(), item["name"], item["photo_file"]
            )
        expected_changed_paths = {
            profile_paths[source].relative_to(PROFILE_DIR) for source in success_sources
        }
        validate_profile_tree_surgical(
            before_profile_tree, temp_hospital_dir, expected_changed_paths
        )
        if hashlib.sha256((temp_hospital_dir / "_索引.md").read_bytes()).hexdigest() != index_before_sha256:
            raise RuntimeError("FULL 临时事务修改了 _索引.md")

        profile_integrity: list[dict[str, Any]] = []
        for source in sorted(target_sources):
            before_content = before_profile_bytes[source]
            after_content = temp_profile_paths[source].read_bytes()
            success = source in success_sources
            profile_integrity.append(
                {
                    "source_link": source,
                    "path": str(profile_paths[source].relative_to(ROOT)),
                    "status": "实采" if success else "失败留空",
                    "before_sha256": hashlib.sha256(before_content).hexdigest(),
                    "after_sha256": hashlib.sha256(after_content).hexdigest(),
                    "added_lines": 2 if success else 0,
                    "removed_lines": 0,
                }
            )

        temp_audit_sheet = temp_root / FULL_AUDIT_SHEET_PATH.name
        audit_samples = build_full_audit_sheet(photo_samples, temp_photo_dir, temp_audit_sheet)
        temp_visual_dir = temp_root / FULL_VISUAL_DIR.name
        visual_review_sheets = build_visual_review_sheets(
            photo_samples, temp_photo_dir, temp_visual_dir
        )
        state_counter = Counter(item["state"] for item in failures)
        duplicate_counter = Counter(item["sha256"] for item in photo_samples)
        duplicate_groups = {
            digest: [item["source_link"] for item in photo_samples if item["sha256"] == digest]
            for digest, count in duplicate_counter.items()
            if count > 1
        }
        total_bytes = sum(int(item["bytes"]) for item in photo_samples)
        immutable_after_preinstall = immutable_snapshot()
        full_payload = {
            "meta": {
                "issue": ISSUE_NUMBER,
                "phase": "FULL_READY_FOR_FINAL_OWNER_AUDIT",
                "hospital": HOSPITAL,
                "run_date": run_date,
                "authorization": FULL_AUTHORIZATION,
                "expected_count": EXPECTED_SCOPE_COUNT,
                "downloaded_count": len(photo_samples),
                "failed_count": len(failures),
                "blank_count": len(failures),
                "disk_photo_count": len(photo_samples),
                "failure_state_counts": {
                    state: state_counter.get(state, 0) for state in FULL_FAILURE_STATES
                },
                "trial_reused_count": sum(
                    item["origin"] == "TRIAL_REUSE" for item in photo_samples
                ),
                "fresh_target_count": EXPECTED_FRESH_COUNT,
                "fresh_downloaded_count": sum(
                    item["origin"] == "FULL_FETCH" for item in photo_samples
                ),
                "fresh_failed_count": len(failures),
                "detail_status_flicker_count": detail_status_flicker_count,
                "photo_status_flicker_count": photo_status_flicker_count,
                "request_mode": REQUEST_MODE,
                "urllib_default_headers": session.default_headers,
                "cookie_names": session.cookie_names,
                "incomplete_read_retry_count": session.incomplete_read_retry_count,
                "constructed_unreferenced_probe_count": 0,
                "third_party_source_count": 0,
                "photo_total_bytes": total_bytes,
                "photo_total_mib": total_bytes / 1024 / 1024,
                "photo_max_bytes": max((int(item["bytes"]) for item in photo_samples), default=0),
                "size_bucket_counts": trial.size_buckets(photo_samples),
                "over_5mib_count": sum(
                    int(item["bytes"]) > trial.OWNER_REPORT_BYTES for item in photo_samples
                ),
                "over_20mib_count": sum(
                    int(item["bytes"]) > trial.MAX_PHOTO_BYTES for item in photo_samples
                ),
                "declared_extension_mismatch_count": sum(
                    item["declared_extension"].replace("jpeg", "jpg") != item["extension"]
                    for item in photo_samples
                ),
                "format_counts": dict(Counter(item["extension"] for item in photo_samples)),
                "duplicate_sha256_group_count": len(duplicate_groups),
                "cross_doctor_duplicate_sha256_group_count": len(
                    cross_doctor_duplicate_sha_groups(photo_samples)
                ),
                "existing_profile_count": len(profile_paths),
                "profile_refreshed_count": len(success_sources),
                "profile_untouched_count": EXPECTED_SCOPE_COUNT - len(success_sources),
                "profile_index_before_sha256": index_before_sha256,
                "row_diff_count": len(row_diffs),
                "row_diff_columns": dict(Counter(item["列名"] for item in row_diffs)),
                "audit_sheet_sha256": hashlib.sha256(temp_audit_sheet.read_bytes()).hexdigest(),
                "visual_review_sheet_count": len(visual_review_sheets),
                "visual_review_photo_count": sum(item["count"] for item in visual_review_sheets),
                "visual_review_status": "PENDING_CODEX_FULL_CONTACT_SHEET_REVIEW",
                "immutable_before": immutable_before,
                "immutable_after_preinstall": immutable_after_preinstall,
            },
            "failures": failures,
            "photo_samples": photo_samples,
            "duplicate_sha256_groups": duplicate_groups,
            "reconciliation": reconciliation,
            "row_diffs": row_diffs,
            "rows": result_rows,
            "profile_integrity": profile_integrity,
            "audit_samples": audit_samples,
            "visual_review_sheets": visual_review_sheets,
        }
        validate_full_payload(
            full_payload, temp_photo_dir, temp_audit_sheet, temp_visual_dir
        )

        temp_full_payload = temp_root / FULL_JSON_PATH.name
        temp_full_csv = temp_root / FULL_CSV_PATH.name
        temp_full_report = temp_root / FULL_REPORT_PATH.name
        temp_full_payload.write_text(
            json.dumps(full_payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_reconciliation_csv(temp_full_csv, full_payload)
        write_full_report(temp_full_report, full_payload)

        file_map: dict[Path, Path] = {
            MASTER_JSON_PATH: temp_master_payload,
            MASTER_CSV_PATH: temp_master_csv,
            MASTER_XLSX_PATH: temp_master_xlsx,
            FULL_JSON_PATH: temp_full_payload,
            FULL_CSV_PATH: temp_full_csv,
            FULL_REPORT_PATH: temp_full_report,
            FULL_AUDIT_SHEET_PATH: temp_audit_sheet,
        }
        for source in success_sources:
            file_map[profile_paths[source]] = temp_profile_paths[source]
        backups = backup_file_targets(list(file_map), temp_root / "file_backups")
        photo_swapped = False
        visual_swapped = False
        try:
            ensure_workspace_target(FORMAL_PHOTO_DIR)
            temp_photo_dir.replace(FORMAL_PHOTO_DIR)
            photo_swapped = True
            ensure_workspace_target(FULL_VISUAL_DIR)
            temp_visual_dir.replace(FULL_VISUAL_DIR)
            visual_swapped = True
            apply_file_map(file_map)
            final_rows = validate_master_layers(
                MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH
            )
            if collect_full_row_diffs(
                before_rows, final_rows, target_sources, headers
            ) != row_diffs:
                raise RuntimeError("FULL 落盘后的逐单元格差异与预期不一致")
            validate_full_installation(full_payload)
        except Exception:
            restore_file_targets(backups)
            if photo_swapped and FORMAL_PHOTO_DIR.exists():
                shutil.rmtree(FORMAL_PHOTO_DIR)
            if visual_swapped and FULL_VISUAL_DIR.exists():
                shutil.rmtree(FULL_VISUAL_DIR)
            raise
        return full_payload


def reconstruct_baseline_rows(
    current_rows: list[dict[str, Any]], prior_payload: dict[str, Any]
) -> list[dict[str, Any]]:
    baseline = copy.deepcopy(current_rows)
    for item in prior_payload.get("row_diffs", []):
        index = int(item["底表行"]) - 2
        column = trial.clean_text(item.get("列名"))
        if not (0 <= index < len(baseline)) or column not in FULL_ALLOWED_ROW_COLUMNS:
            raise RuntimeError("FULL 既有逐单元格 diff 无法重建基线")
        if row_value(baseline[index].get(column)) != row_value(item.get("修改后")):
            raise RuntimeError(
                f"FULL 既有逐单元格 diff 与当前底表不一致：row={index + 2} column={column}"
            )
        baseline[index][column] = item.get("修改前", "")
    return baseline


def owner_placeholder_failure(
    photo: dict[str, Any], duplicate_photos: list[dict[str, Any]]
) -> tuple[dict[str, Any], dict[str, Any]]:
    resource_urls = sorted({item["photo_url"] for item in duplicate_photos})
    sources = sorted({item["source_link"] for item in duplicate_photos})
    decoded_query = decoded_photo_query(photo["photo_url"])
    evidence = {
        "observed_utc": OWNER_FIX_COMMENT_UTC,
        "resource_urls": resource_urls,
        "photo_reference_count": int(photo["photo_reference_count"]),
        "detection_feature": (
            "same-SHA cross-doctor reuse "
            f"sha256={OWNER_PLACEHOLDER_SHA256}; full-image unique_color_count=1 "
            "all pixels RGBA=(255,255,255,255); query Base64 decodes to blank2.jpg"
        ),
        "template_signature": photo["template_signature"],
        "excluded_resource_examples": [],
        "sha256": OWNER_PLACEHOLDER_SHA256,
        "cross_doctor_sources": sources,
        "unique_color_count": 1,
        "decoded_query_filename": decoded_query,
        "owner_audit_comment": (
            "https://github.com/nancywrayg57-jpg/doctor-data-collection/"
            "pull/78#issuecomment-5336568337"
        ),
    }
    error = failure_evidence_text(evidence)
    failure = {
        "detail_id": photo["detail_id"],
        "name": photo["name"],
        "source_link": photo["source_link"],
        "state": "占位图",
        "error": error,
        "evidence": evidence,
        "attempts": photo.get("photo_attempts") or [],
        "origin": "FULL_FETCH",
    }
    reconciliation = {
        "详情ID": photo["detail_id"],
        "姓名": photo["name"],
        "来源链接": photo["source_link"],
        "状态": "失败留空",
        "失败分类": "占位图",
        "照片引用数": int(photo["photo_reference_count"]),
        "照片链接": "",
        "照片文件": "",
        "声明格式": "",
        "实际格式": "",
        "字节数": "",
        "SHA-256": "",
        "宽": "",
        "高": "",
        "来源批次": "FULL_FETCH",
        "错误证据": error,
    }
    return failure, reconciliation


def fix_owner_rejected_placeholders() -> dict[str, Any]:
    import collect_official_doctors_batch as collector

    prior = load_full_payload()
    if (
        prior.get("meta", {}).get("owner_fix_comment_utc") == OWNER_FIX_COMMENT_UTC
        and int(prior["meta"].get("downloaded_count") or 0) == 179
        and int(prior["meta"].get("failed_count") or 0) == 4
    ):
        validate_full_installation(prior)
        return prior
    if (
        int(prior.get("meta", {}).get("downloaded_count") or 0) != 181
        or int(prior["meta"].get("failed_count") or 0) != 2
    ):
        raise RuntimeError("Owner 修正前 FULL 状态不是 181 实采 + 2 失败")

    photos = [dict(item) for item in prior.get("photo_samples", [])]
    affected = [item for item in photos if item["detail_id"] in OWNER_PLACEHOLDER_DETAIL_IDS]
    if (
        len(affected) != 2
        or {item["name"] for item in affected} != set(OWNER_PLACEHOLDER_NAMES)
        or {item["sha256"] for item in affected} != {OWNER_PLACEHOLDER_SHA256}
    ):
        raise RuntimeError("Owner 指定的两条占位记录与已落盘 FULL 不一致")
    if cross_doctor_duplicate_sha_groups(affected).get(OWNER_PLACEHOLDER_SHA256) is None:
        raise RuntimeError("Owner 指定的两条记录未形成跨医生同 SHA 证据")
    affected_by_source = {item["source_link"]: item for item in affected}
    affected_sources = set(affected_by_source)
    affected_photo_paths: list[Path] = []
    for item in affected:
        path = FORMAL_PHOTO_DIR / item["filename"]
        ensure_workspace_target(path)
        content = path.read_bytes()
        if (
            len(content) != 1_147
            or hashlib.sha256(content).hexdigest() != OWNER_PLACEHOLDER_SHA256
            or trial.image_dimensions(content) != (148, 208)
            or decoded_photo_query(item["photo_url"]) != "blank2.jpg"
            or limited_unique_color_count(content, limit=2) != 1
        ):
            raise RuntimeError(f"Owner 占位三重证据复算失败：{item['name']}")
        affected_photo_paths.append(path)

    master_payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    current_rows = [dict(row) for row in master_payload.get("rows", [])]
    headers = list(collector.BASE_HEADERS)
    baseline_rows = reconstruct_baseline_rows(current_rows, prior)
    target_sources = {trial.clean_text(row.get("来源链接")) for row in prior["rows"]}
    if len(target_sources) != EXPECTED_SCOPE_COUNT or not affected_sources <= target_sources:
        raise RuntimeError("Owner 修正范围越出 Issue #77 固定 183 条")

    corrected_rows = copy.deepcopy(current_rows)
    corrected_global_by_source = {
        trial.clean_text(row.get("来源链接")): row for row in corrected_rows
    }
    for source in affected_sources:
        row = corrected_global_by_source[source]
        row["照片链接"] = ""
        row["照片文件"] = ""
        row["异常提示"] = append_warning(row.get("异常提示"), "占位图")
    row_diffs = collect_full_row_diffs(
        baseline_rows, corrected_rows, target_sources, headers
    )
    corrected_target_rows = [
        corrected_global_by_source[trial.clean_text(row.get("来源链接"))]
        for row in prior["rows"]
    ]
    corrected_master = copy.deepcopy(master_payload)
    corrected_master["rows"] = corrected_rows
    recompute_master_derivatives(corrected_master, corrected_rows)

    corrected_photos = [item for item in photos if item["source_link"] not in affected_sources]
    existing_failures = {
        item["source_link"]: dict(item) for item in prior.get("failures", [])
    }
    reconciliation_by_source = {
        item["来源链接"]: dict(item) for item in prior["reconciliation"]
    }
    for source, photo in affected_by_source.items():
        failure, reconciliation = owner_placeholder_failure(photo, affected)
        existing_failures[source] = failure
        reconciliation_by_source[source] = reconciliation
    corrected_failures = [
        existing_failures[source]
        for source in (
            trial.clean_text(row.get("来源链接")) for row in corrected_target_rows
        )
        if source in existing_failures
    ]
    corrected_reconciliation = [
        reconciliation_by_source[trial.clean_text(row.get("来源链接"))]
        for row in corrected_target_rows
    ]

    integrity_by_source = {
        item["source_link"]: dict(item) for item in prior["profile_integrity"]
    }
    restored_profile_bytes: dict[Path, bytes] = {}
    for source, photo in affected_by_source.items():
        integrity = integrity_by_source[source]
        path = ROOT / integrity["path"]
        restored = remove_profile_photo_block_bytes(
            path.read_bytes(), photo["name"], photo["photo_file"]
        )
        if hashlib.sha256(restored).hexdigest() != integrity["before_sha256"]:
            raise RuntimeError(f"Owner 修正画像未恢复 origin/main 字节：{photo['name']}")
        restored_profile_bytes[path] = restored
        integrity.update(
            {
                "status": "失败留空",
                "after_sha256": integrity["before_sha256"],
                "added_lines": 0,
                "removed_lines": 0,
            }
        )
    corrected_integrity = [
        integrity_by_source[item["source_link"]] for item in prior["profile_integrity"]
    ]

    with tempfile.TemporaryDirectory(prefix="issue77_owner_fix_", dir=WORK_DIR) as temporary:
        temp_root = Path(temporary)
        temp_photo_dir = temp_root / "photos"
        shutil.copytree(FORMAL_PHOTO_DIR, temp_photo_dir)
        for item in affected:
            (temp_photo_dir / item["filename"]).unlink()

        temp_master_payload = temp_root / MASTER_JSON_PATH.name
        temp_master_csv = temp_root / MASTER_CSV_PATH.name
        temp_master_xlsx = temp_root / MASTER_XLSX_PATH.name
        temp_master_preview = temp_root / "master_preview.png"
        temp_master_payload.write_text(
            json.dumps(corrected_master, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_master_csv(temp_master_csv, corrected_rows, headers)
        collector.build_workbook(temp_master_payload, temp_master_xlsx, temp_master_preview)
        validate_master_layers(temp_master_payload, temp_master_csv, temp_master_xlsx)

        temp_profiles: dict[Path, Path] = {}
        for index, (target, content) in enumerate(restored_profile_bytes.items()):
            temp_path = temp_root / f"profile_{index:02d}.md"
            temp_path.write_bytes(content)
            temp_profiles[target] = temp_path

        temp_audit_sheet = temp_root / FULL_AUDIT_SHEET_PATH.name
        audit_samples = build_full_audit_sheet(
            corrected_photos, temp_photo_dir, temp_audit_sheet
        )
        temp_visual_dir = temp_root / FULL_VISUAL_DIR.name
        visual_review_sheets = build_visual_review_sheets(
            corrected_photos, temp_photo_dir, temp_visual_dir
        )
        duplicate_counter = Counter(item["sha256"] for item in corrected_photos)
        duplicate_groups = {
            digest: [
                item["source_link"]
                for item in corrected_photos
                if item["sha256"] == digest
            ]
            for digest, count in duplicate_counter.items()
            if count > 1
        }
        cross_doctor_duplicates = cross_doctor_duplicate_sha_groups(corrected_photos)
        if cross_doctor_duplicates:
            raise RuntimeError(
                "Owner 修正后仍存在跨医生同 SHA："
                + json.dumps(cross_doctor_duplicates, ensure_ascii=False, sort_keys=True)
            )

        corrected = copy.deepcopy(prior)
        meta = corrected["meta"]
        state_counter = Counter(item["state"] for item in corrected_failures)
        total_bytes = sum(int(item["bytes"]) for item in corrected_photos)
        meta.update(
            {
                "phase": "FULL_FIXED_READY_FOR_OWNER_REAUDIT",
                "publication_signal": "FULL_FIXED_DONE",
                "owner_fix_comment_utc": OWNER_FIX_COMMENT_UTC,
                "owner_fix_affected_detail_ids": sorted(OWNER_PLACEHOLDER_DETAIL_IDS),
                "owner_fix_removed_sha256": OWNER_PLACEHOLDER_SHA256,
                "downloaded_count": len(corrected_photos),
                "failed_count": len(corrected_failures),
                "blank_count": len(corrected_failures),
                "disk_photo_count": len(corrected_photos),
                "failure_state_counts": {
                    state: state_counter.get(state, 0) for state in FULL_FAILURE_STATES
                },
                "trial_reused_count": sum(
                    item["origin"] == "TRIAL_REUSE" for item in corrected_photos
                ),
                "fresh_downloaded_count": sum(
                    item["origin"] == "FULL_FETCH" for item in corrected_photos
                ),
                "fresh_failed_count": sum(
                    item.get("origin") == "FULL_FETCH" for item in corrected_failures
                ),
                "photo_total_bytes": total_bytes,
                "photo_total_mib": total_bytes / 1024 / 1024,
                "photo_max_bytes": max(
                    (int(item["bytes"]) for item in corrected_photos), default=0
                ),
                "size_bucket_counts": trial.size_buckets(corrected_photos),
                "over_5mib_count": sum(
                    int(item["bytes"]) > trial.OWNER_REPORT_BYTES
                    for item in corrected_photos
                ),
                "over_20mib_count": sum(
                    int(item["bytes"]) > trial.MAX_PHOTO_BYTES
                    for item in corrected_photos
                ),
                "declared_extension_mismatch_count": sum(
                    item["declared_extension"].replace("jpeg", "jpg")
                    != item["extension"]
                    for item in corrected_photos
                ),
                "format_counts": dict(
                    Counter(item["extension"] for item in corrected_photos)
                ),
                "duplicate_sha256_group_count": len(duplicate_groups),
                "cross_doctor_duplicate_sha256_group_count": 0,
                "profile_refreshed_count": len(corrected_photos),
                "profile_untouched_count": len(corrected_failures),
                "row_diff_count": len(row_diffs),
                "row_diff_columns": dict(Counter(item["列名"] for item in row_diffs)),
                "audit_sheet_sha256": hashlib.sha256(
                    temp_audit_sheet.read_bytes()
                ).hexdigest(),
                "visual_review_sheet_count": len(visual_review_sheets),
                "visual_review_photo_count": sum(
                    item["count"] for item in visual_review_sheets
                ),
                "visual_review_status": "PENDING_CODEX_OWNER_FIX_CONTACT_SHEET_REVIEW",
                "immutable_after_preinstall": immutable_snapshot(),
            }
        )
        meta.pop("visual_review_utc", None)
        corrected.update(
            {
                "failures": corrected_failures,
                "photo_samples": corrected_photos,
                "duplicate_sha256_groups": duplicate_groups,
                "reconciliation": corrected_reconciliation,
                "row_diffs": row_diffs,
                "rows": corrected_target_rows,
                "profile_integrity": corrected_integrity,
                "audit_samples": audit_samples,
                "visual_review_sheets": visual_review_sheets,
            }
        )
        validate_full_payload(
            corrected, temp_photo_dir, temp_audit_sheet, temp_visual_dir
        )

        temp_full_payload = temp_root / FULL_JSON_PATH.name
        temp_full_csv = temp_root / FULL_CSV_PATH.name
        temp_full_report = temp_root / FULL_REPORT_PATH.name
        temp_full_payload.write_text(
            json.dumps(corrected, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_reconciliation_csv(temp_full_csv, corrected)
        write_full_report(temp_full_report, corrected)

        file_map: dict[Path, Path] = {
            MASTER_JSON_PATH: temp_master_payload,
            MASTER_CSV_PATH: temp_master_csv,
            MASTER_XLSX_PATH: temp_master_xlsx,
            FULL_JSON_PATH: temp_full_payload,
            FULL_CSV_PATH: temp_full_csv,
            FULL_REPORT_PATH: temp_full_report,
            FULL_AUDIT_SHEET_PATH: temp_audit_sheet,
            **temp_profiles,
        }
        for sheet in visual_review_sheets:
            file_map[FULL_VISUAL_DIR / sheet["path"]] = temp_visual_dir / sheet["path"]
        targets = list(file_map) + affected_photo_paths
        backups = backup_file_targets(targets, temp_root / "file_backups")
        try:
            apply_file_map(file_map)
            for path in affected_photo_paths:
                ensure_workspace_target(path)
                path.unlink()
            validate_full_installation(corrected)
        except Exception:
            restore_file_targets(backups)
            raise
        return corrected


def load_full_payload() -> dict[str, Any]:
    if not FULL_JSON_PATH.is_file():
        raise RuntimeError(f"FULL payload 不存在：{FULL_JSON_PATH}")
    payload = json.loads(FULL_JSON_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("FULL payload 顶层不是对象")
    return payload


def mark_visual_pass() -> dict[str, Any]:
    payload = load_full_payload()
    validate_full_installation(payload)
    payload["meta"]["visual_review_status"] = FULL_VISUAL_PASS_STATUS
    payload["meta"]["visual_review_utc"] = trial.utc_now()
    FULL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_full_report(FULL_REPORT_PATH, payload)
    validate_full_installation(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Issue #77 广州医科大学附属脑科医院照片补录 FULL"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--full", action="store_true", help="执行 183 行 FULL 事务")
    mode.add_argument("--validate-full", action="store_true", help="验证已落盘 FULL")
    mode.add_argument(
        "--fix-owner-rejected-placeholders",
        action="store_true",
        help="按 PR #78 Owner 终审仅回滚两条纯白占位图并重算受影响工件",
    )
    mode.add_argument(
        "--mark-visual-pass",
        action="store_true",
        help="全量联系表逐页人工通过后写入视觉审计状态",
    )
    parser.add_argument("--run-date", default=str(date.today()), help="执行日期 YYYY-MM-DD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.full:
        payload = run_full(args.run_date)
        print(
            "FULL_DONE "
            f"expected={payload['meta']['expected_count']} "
            f"downloaded={payload['meta']['downloaded_count']} "
            f"failed={payload['meta']['failed_count']} "
            f"profiles={payload['meta']['profile_refreshed_count']}"
        )
        return
    if args.fix_owner_rejected_placeholders:
        payload = fix_owner_rejected_placeholders()
        print(
            "FULL_OWNER_FIX_DONE "
            f"expected={payload['meta']['expected_count']} "
            f"downloaded={payload['meta']['downloaded_count']} "
            f"failed={payload['meta']['failed_count']} "
            f"profiles={payload['meta']['profile_refreshed_count']}"
        )
        return
    if args.mark_visual_pass:
        payload = mark_visual_pass()
        print(
            "FULL_VISUAL_REVIEW_MARKED "
            f"status={payload['meta']['visual_review_status']}"
        )
        return
    payload = load_full_payload()
    validate_full_installation(payload)
    print(
        "FULL_VALIDATED "
        f"expected={payload['meta']['expected_count']} "
        f"downloaded={payload['meta']['downloaded_count']} "
        f"failed={payload['meta']['failed_count']}"
    )


if __name__ == "__main__":
    main()
