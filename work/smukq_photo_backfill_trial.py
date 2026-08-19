from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urljoin, urlparse

import ny5y_photo_backfill_trial as framework


base = framework.base
ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "南方医科大学口腔医院(海珠广场院区)"
ISSUE_NUMBER = 81
EXPECTED_SCOPE_COUNT = 95
EXPECTED_TRIAL_COUNT = 10
MIN_TRIAL_DEPARTMENTS = 5
OFFICIAL_HOME = "https://www.smukqyy.cn/"
DIRECTORY_URL = "https://www.smukqyy.cn/section/341"
OFFICIAL_HOST = "smukqyy.cn"
PHOTO_PREFIX = "/Uploads/Upload/"
PROFILE_DIR = VAULT / "01_试点医院" / HOSPITAL
FORMAL_PHOTO_DIR = PROFILE_DIR / "照片"
TRIAL_BASENAME = f"{HOSPITAL}_photo_backfill_trial"
TRIAL_JSON_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
TRIAL_CSV_PATH = WORK_DIR / f"{TRIAL_BASENAME}_manifest.csv"
TRIAL_REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
TRIAL_PHOTO_DIR = WORK_DIR / f"{TRIAL_BASENAME}_photos"
SECTION_COUNTS = {
    "341": 12,
    "342": 12,
    "343": 10,
    "384": 12,
    "385": 12,
    "386": 12,
    "431": 7,
    "434": 11,
    "504": 7,
}
EXPECTED_TITLE_COUNTS = {"正高": 2, "副高": 2, "中级": 3, "初级": 3}
SAMPLE_PLAN = (
    ("管东华", "正高", "341"),
    ("陈欢", "副高", "342"),
    ("何龙文", "中级", "343"),
    ("叶晓平", "初级", "384"),
    ("熊华翠", "副高", "385"),
    ("孟文霞", "正高", "386"),
    ("曹恒隆", "初级", "431"),
    ("张彩美", "中级", "434"),
    ("唐凤翔", "中级", "504"),
    ("梁慧珉", "初级", "341"),
)
EXCLUDED_RESOURCE_EXAMPLES = (
    "/Home/images/（top_tel/banner/content_zs/footer/sidebar/btn/oa/wz/wx 等）",
    "/Public/Home/images/（站架与装饰资源）",
    "除 img.content_img 外的所有页面图片",
)


def clean_text(value: Any) -> str:
    return framework.clean_text(value)


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"路径越出仓库根目录：{path}") from exc


def detail_parts(value: Any) -> tuple[str, str] | None:
    parsed = urlparse(clean_text(value))
    match = re.fullmatch(r"/prods/(\d+)/(\d+)", parsed.path)
    if (
        parsed.scheme != "https"
        or framework.comparable_host(parsed.geturl()) != OFFICIAL_HOST
        or parsed.query
        or parsed.fragment
        or not match
        or match.group(1) not in SECTION_COUNTS
    ):
        return None
    return match.group(1), match.group(2)


def detail_id(value: Any) -> str:
    parts = detail_parts(value)
    return parts[1] if parts else ""


def section_id(value: Any) -> str:
    parts = detail_parts(value)
    return parts[0] if parts else ""


def page_referenced_photo_url(value: Any, base_url: str) -> str:
    raw = clean_text(value)
    if not raw:
        return ""
    absolute = urljoin(base_url, raw)
    parsed = urlparse(absolute)
    if (
        parsed.scheme != "https"
        or framework.comparable_host(absolute) != OFFICIAL_HOST
        or parsed.fragment
        or not parsed.path.startswith(PHOTO_PREFIX)
    ):
        return ""
    lowered = unquote(parsed.path).casefold()
    if any(marker in lowered for marker in base.PLACEHOLDER_MARKERS):
        return ""
    if framework.suspicious_query_decoding(absolute):
        return ""
    return absolute


def magic_extension(content: bytes, content_type: str | None) -> str:
    """Use the image signature as SSOT; the site serves some JPGs as octet-stream."""
    del content_type
    if content.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if content.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if len(content) >= 12 and content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return "webp"
    return ""


class SmukqPhysicianPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.portrait_attrs: list[dict[str, str]] = []
        self.portrait_snippets: list[str] = []
        self.names: list[str] = []
        self.titles: list[str] = []
        self._capture: str = ""
        self._parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = {name.lower(): str(value or "") for name, value in attrs}
        classes = set(clean_text(values.get("class")).split())
        lowered = tag.lower()
        if lowered == "img" and "content_img" in classes:
            self.portrait_attrs.append(values)
            self.portrait_snippets.append(clean_text(self.get_starttag_text()))
        if lowered == "span" and classes & {"content2_span1", "content2_span2"}:
            if self._capture:
                raise RuntimeError("详情姓名/职称容器发生意外嵌套")
            self._capture = (
                "name" if "content2_span1" in classes else "title"
            )
            self._parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "span" or not self._capture:
            return
        value = clean_text(" ".join(self._parts))
        if value:
            if self._capture == "name":
                self.names.append(value)
            else:
                self.titles.append(value)
        self._capture = ""
        self._parts = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._parts.append(data)


def inspect_portrait_reference(
    html: str, source_link: str, expected_name: str
) -> tuple[str, base.PortraitReference | None]:
    parts = detail_parts(source_link)
    if not parts:
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    parser = SmukqPhysicianPageParser()
    parser.feed(html)
    if parser.names != [clean_text(expected_name)]:
        raise RuntimeError(
            f"详情姓名与底表不一致：底表={expected_name} 官网={parser.names or ['空']} {source_link}"
        )
    if not parser.portrait_attrs:
        return "无照片容器", None
    if len(parser.portrait_attrs) != 1:
        raise RuntimeError(
            f"img.content_img 容器不唯一：{source_link} 数量={len(parser.portrait_attrs)}"
        )
    raw_url = clean_text(parser.portrait_attrs[0].get("src"))
    if not raw_url:
        return "无照片容器", None
    absolute = urljoin(source_link, raw_url)
    decoded_query = framework.suspicious_query_decoding(absolute)
    lowered_path = unquote(urlparse(absolute).path).casefold()
    if decoded_query or any(
        marker in lowered_path for marker in base.PLACEHOLDER_MARKERS
    ):
        return "占位图", None
    normalized = page_referenced_photo_url(raw_url, source_link)
    if not normalized:
        raise RuntimeError(f"页面引用照片 URL 越界：{source_link} {raw_url}")
    framework.STRUCTURE_EVIDENCE[source_link] = {
        "name": clean_text(expected_name),
        "section_id": parts[0],
        "detail_id": parts[1],
        "container_selector": "img.content_img",
        "container_count": 1,
        "html_snippet": parser.portrait_snippets[0],
        "raw_src": raw_url,
        "normalized_photo_url": normalized,
        "decoded_query_values": framework.decoded_query_values(normalized),
        "excluded_resource_examples": list(EXCLUDED_RESOURCE_EXAMPLES),
        "decision_basis": (
            "only the unique img.content_img src is eligible; /Home/images/, "
            "/Public/Home/images/ and all other page images are excluded"
        ),
        "observed_utc": framework.utc_now(),
    }
    return "", base.PortraitReference(
        page_title=parser.titles[0] if len(parser.titles) == 1 else HOSPITAL,
        photo_url=normalized,
        source_attribute="img.content_img src",
    )


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
    invalid = [source for source in sources if not detail_parts(source)]
    if invalid:
        raise RuntimeError("范围存在非授权详情链接：" + "、".join(invalid[:5]))
    actual_sections = Counter(section_id(source) for source in sources)
    if actual_sections != Counter(SECTION_COUNTS):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} section 分布漂移：{dict(actual_sections)}")
    entry_sections = Counter(
        urlparse(clean_text(row.get("采集入口"))).path.removeprefix("/section/")
        for row in rows
    )
    if entry_sections != Counter(SECTION_COUNTS):
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} 采集入口分布漂移：{dict(entry_sections)}")
    return rows


def select_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for expected_name, expected_level, expected_section in SAMPLE_PLAN:
        matches = [
            row for row in rows if clean_text(row.get("姓名")) == expected_name
        ]
        if len(matches) != 1:
            raise RuntimeError(f"试采姓名范围不唯一：{expected_name} 数量={len(matches)}")
        row = dict(matches[0])
        actual_level = base.title_level(row.get("职称身份原文"))
        actual_section = section_id(row.get("来源链接"))
        if actual_level != expected_level or actual_section != expected_section:
            raise RuntimeError(
                f"试采分层漂移：{expected_name} 应为 {expected_section}/{expected_level} "
                f"实际 {actual_section}/{actual_level}"
            )
        result.append(row)
    counts = Counter(base.title_level(row.get("职称身份原文")) for row in result)
    actual_counts = {level: counts[level] for level in EXPECTED_TITLE_COUNTS}
    covered_sections = {section_id(row.get("来源链接")) for row in result}
    if len(covered_sections) < MIN_TRIAL_DEPARTMENTS:
        raise RuntimeError(f"section 覆盖不足：{len(covered_sections)}")
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


_framework_enrich_payload = framework.enrich_payload
_framework_validate_payload = framework.validate_payload


def enrich_payload(payload: dict[str, Any]) -> dict[str, Any]:
    payload = _framework_enrich_payload(payload)
    normalize_payload_paths(payload)
    payload["meta"]["section_coverage_count"] = len(
        {section_id(item["source_link"]) for item in payload["photo_samples"]}
    )
    payload["meta"]["covered_sections"] = sorted(
        {section_id(item["source_link"]) for item in payload["photo_samples"]}
    )
    payload["meta"]["repository_relative_paths_only"] = True
    payload["meta"]["artifact_hash_policy"] = "repository_blob_lf"
    return payload


def validate_payload(payload: dict[str, Any]) -> None:
    _framework_validate_payload(payload)
    meta = payload["meta"]
    errors: list[str] = []
    if meta.get("section_coverage_count") != 9:
        errors.append("TRIAL 未覆盖全部 9 个 section")
    if meta.get("covered_sections") != sorted(SECTION_COUNTS):
        errors.append("TRIAL section 集合漂移")
    if meta.get("repository_relative_paths_only") is not True:
        errors.append("工件未声明仅使用仓库相对路径")
    if meta.get("artifact_hash_policy") != "repository_blob_lf":
        errors.append("工件哈希政策不是 repository_blob_lf")
    if any(
        not clean_text(item.get("html_snippet")).startswith("<img")
        or "content_img" not in clean_text(item.get("html_snippet"))
        for item in payload.get("structure_diagnostics", [])
    ):
        errors.append("容器诊断不是 img.content_img")
    serialized = json.dumps(payload, ensure_ascii=False)
    if str(ROOT) in serialized or ROOT.as_posix() in serialized:
        errors.append("payload 泄漏仓库绝对路径")
    for sample in payload.get("photo_samples", []):
        path = Path(sample["disk_path"])
        if path.is_absolute() or not (ROOT / path).is_file():
            errors.append(f"照片路径不是有效仓库相对路径：{path}")
    if errors:
        raise RuntimeError(f"Issue #{ISSUE_NUMBER} TRIAL 工程门禁失败：" + "；".join(errors))


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|").replace("\n", " ")


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    levels = "、".join(
        f"{level} {count}" for level, count in meta["title_level_counts"].items()
    )
    samples = [
        f"| {markdown_cell(item['name'])} | {section_id(item['source_link'])} | "
        f"{markdown_cell(item['department'])} | {item['title_level']} | "
        f"{item['bytes']} | {item['width']}×{item['height']} | "
        f"{item['declared_extension']}/{item['actual_extension']} | "
        f"`{item['sha256']}` | {item['photo_url']} |"
        for item in payload["photo_samples"]
    ]
    diagnostics = [
        f"### {item['name']} / section {item['section_id']} / ID {item['detail_id']}\n\n"
        f"```html\n{item['html_snippet']}\n```\n\n"
        f"- 页面引用：`{item['raw_src']}`\n"
        f"- 规范化 URL：{item['normalized_photo_url']}\n"
        f"- 判定：{item['decision_basis']}\n"
        for item in payload["structure_diagnostics"]
    ]
    protected = [
        f"| `{path}` | {facts['bytes']} | `{facts['sha256']}` |"
        for path, facts in meta["protected_assets_before"]["master_assets"].items()
    ]
    reachability = [
        f"| {item['round']} | {item['target']} | {item['status']} | "
        f"{item['content_type']} | {item['bytes']} | {item['observed_utc']} |"
        for item in meta["reachability_preflight"]
    ]
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 TRIAL 报告

> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 生成日期：{meta['run_date']}
> 视觉复核：`{meta['visual_review_status']}`

## 范围与抽样

- 固定范围：{meta['scope_count']} 行、{meta['scope_unique_source_count']} 个唯一详情 URL；照片双列全空。
- 9 个 section 分布：{json.dumps(SECTION_COUNTS, ensure_ascii=False, sort_keys=True)}。
- TRIAL：{meta['trial_detail_count']} 位，覆盖全部 {meta['section_coverage_count']} 个 section；职称分层 {levels}，覆盖正高/副高/中级/初级四层。
- 详情 HTTP 200：{meta['detail_http_200_count']}/{meta['trial_detail_count']}；实图 {meta['photo_sample_count']}/{meta['trial_detail_count']}；失败/结构异常 {meta['fuse_problem_count']}。
- 固定浏览器 UA urllib：Cookie 0、代理 0、挑战绕过 0、页面未引用路径探测 0、第三方来源 0。

## UA 可达性复测

| 轮次 | 目标 | HTTP | Content-Type | 字节 | UTC |
|---:|---|---:|---|---:|---|
{chr(10).join(reachability)}

## 容器结构诊断

- 唯一允许容器：`img.content_img` 的 `src`。
- `/Home/images/`、`/Public/Home/images/` 与其他所有页面图片均排除。

{chr(10).join(diagnostics)}

## TRIAL 原始字节

- 10 张共 {meta['photo_total_bytes']} bytes；平均 {meta['photo_average_bytes']} bytes。
- >5 MiB：{meta['over_5mib_count']}；>20 MiB：{meta['over_20mib_count']}。
- 仅保存页面实际引用响应原始字节；未压缩、未转码；扩展名随实际魔数。

| 姓名 | section | 科室 | 层级 | 字节 | 尺寸 | 声明/实际 | SHA-256 | 页面引用照片 |
|---|---:|---|---|---:|---:|---|---|---|
{chr(10).join(samples)}

详细清单见 `{repo_relative(TRIAL_CSV_PATH)}` 与 `{repo_relative(TRIAL_JSON_PATH)}`。

## 工程与占位门禁

1. ROOT 由 `Path(__file__).resolve().parents[1]` 定位；payload/manifest/report 只记录仓库相对路径。
2. 发布时引用工件 SHA-256 必须按仓库 blob（LF）计算。
3. query Base64 占位标记、全图唯一颜色数不大于 2、跨医生同 SHA、灰底拼图空白/不可见格均拦截。
4. 联系表：`{repo_relative(CONTACT_SHEET_PATH)}`；当前状态 `{meta['visual_review_status']}`。

## 正式资产零修改

| 文件 | 字节 | SHA-256 |
|---|---:|---|
{chr(10).join(protected)}

- 本院画像树：{meta['protected_assets_before']['profile_tree']['file_count']} 个文件，聚合 SHA-256 `{meta['protected_assets_before']['profile_tree']['sha256']}`。
- 正式照片树前后一致：`{json.dumps(meta['protected_assets_before']['formal_photo_tree'], ensure_ascii=False)}`。
- TRIAL 仅写 `work/` 工件，未回填总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件提交并发布 `TRIAL_READY_FOR_OWNER_AUDIT` 后停止。未取得 PR #82（创建后）的明确 `FULL_APPEND_AND_OBSIDIAN` 指令前，不得回填正式资产。
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
    base.magic_extension = magic_extension
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
    framework.load_scope_rows = load_scope_rows
    framework.select_trial_rows = select_trial_rows
    framework.enrich_payload = enrich_payload
    framework.validate_payload = validate_payload
    framework.write_report = write_report
    framework.configure_base()


def run_trial(run_date: str) -> dict[str, Any]:
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
        f"sections={payload['meta']['section_coverage_count']} "
        f"visual={payload['meta']['visual_review_status']}"
    )


if __name__ == "__main__":
    main()
