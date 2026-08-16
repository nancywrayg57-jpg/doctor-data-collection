from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, unquote, urljoin, urlparse
from urllib.request import HTTPCookieProcessor, Request, build_opener

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"D:\workspace\信息收集整理")
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "中山大学附属第三医院"
ISSUE_NUMBER = 57
MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_JSON_PATH = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_REPORT_PATH = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
PROFILE_DIR = VAULT / "01_试点医院" / HOSPITAL
FORMAL_PHOTO_DIR = PROFILE_DIR / "照片"
TRIAL_BASENAME = f"{HOSPITAL}_photo_backfill_trial"
TRIAL_JSON_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
TRIAL_CSV_PATH = WORK_DIR / f"{TRIAL_BASENAME}_manifest.csv"
TRIAL_REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
TRIAL_PHOTO_DIR = WORK_DIR / f"{TRIAL_BASENAME}_photos"
OFFICIAL_HOME = "https://www.zssy.com.cn/"
DIRECTORY_URL = "https://www.zssy.com.cn/page/5968"
OFFICIAL_HOST = "zssy.com.cn"
PHOTO_PREFIX = "/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/"
EXPECTED_SCOPE_COUNT = 780
EXPECTED_TRIAL_COUNT = 10
MIN_TRIAL_DEPARTMENTS = 3
MAX_FAILURE_RATIO = 0.30
LARGE_BYTES = 200 * 1024
LARGE_WIDTH = 800

SAMPLE_PLAN = (
    ("张晓红", "正高"),
    ("张炎", "正高"),
    ("吴玲玲", "正高"),
    ("李名安", "副高"),
    ("唐新意", "副高"),
    ("巴俊慧", "中级"),
    ("杨婷", "中级"),
    ("周攀", "初级"),
    ("黄晓飞", "初级"),
    ("李舣婷", "初级"),
)

PRIMARY_TITLES = (
    "一级主任医师",
    "副主任中医师",
    "主任中医师",
    "主治中医师",
    "副主任医师",
    "主任医师",
    "主治医师",
    "住院医师",
    "副主任技师",
    "主任技师",
    "主管技师",
    "副主任药师",
    "主任药师",
    "主管药师",
    "助理研究员",
    "副研究员",
    "研究员",
    "副教授",
    "教授",
    "医师",
)

PLACEHOLDER_MARKERS = (
    "placeholder",
    "default",
    "avatar",
    "head-logo",
    "header-logo",
    "footer-logo",
    "naoz",
    "chuzhen",
    "fuwu",
    "wx1",
    "wx2",
    "qrcode",
    "qr-code",
    "cloud-hospital",
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36; "
    "public official-site photo backfill trial"
)


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def comparable_host(value: str) -> str:
    host = (urlparse(value).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def detail_id(value: Any) -> str:
    text = clean_text(value)
    parsed = urlparse(text)
    if (
        parsed.scheme not in {"http", "https"}
        or comparable_host(text) != OFFICIAL_HOST
        or parsed.query
        or parsed.fragment
    ):
        return ""
    match = re.fullmatch(r"/node/(\d+)", parsed.path)
    return match.group(1) if match else ""


def safe_photo_part(value: Any) -> str:
    text = re.sub(r'[\\/:*?"<>|]', "_", clean_text(value)).strip(" .")
    return text or "未标注"


def atomic_department(row: dict[str, Any]) -> str:
    value = clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
    atoms = [clean_text(item) for item in re.split(r"[、,，;/；|]+", value) if clean_text(item)]
    chinese_atoms = [item for item in atoms if re.search(r"[\u4e00-\u9fff]", item)]
    return safe_photo_part(chinese_atoms[-1] if chinese_atoms else (atoms[0] if atoms else "未标注"))


def primary_title(value: Any) -> str:
    text = clean_text(value)
    for title in PRIMARY_TITLES:
        if title in text:
            return title
    return "未标注"


def title_level(value: Any) -> str:
    title = primary_title(value)
    if title in {"一级主任医师", "主任医师", "主任中医师", "主任技师", "主任药师", "研究员", "教授"}:
        return "正高"
    if title in {"副主任医师", "副主任中医师", "副主任技师", "副主任药师", "副研究员", "副教授"}:
        return "副高"
    if title in {"主治医师", "主治中医师", "主管技师", "主管药师", "助理研究员"}:
        return "中级"
    if title in {"住院医师", "医师"}:
        return "初级"
    return "其他"


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
    query = parse_qsl(parsed.query, keep_blank_values=True)
    if any(name != "itok" or not item for name, item in query) or len(query) > 1:
        return ""
    lowered = unquote(parsed.path).lower()
    if any(marker in lowered for marker in PLACEHOLDER_MARKERS):
        return ""
    return absolute


def style_background_url(value: Any) -> str:
    match = re.search(
        r"background-image\s*:\s*url\(\s*(['\"]?)([^)'\"]+)\1\s*\)",
        str(value or ""),
        flags=re.IGNORECASE,
    )
    return clean_text(match.group(2)) if match else ""


class PhysicianPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._div_left_stack: list[bool] = []
        self._in_title = False
        self._title_parts: list[str] = []
        self.media_attrs: list[dict[str, str]] = []

    @property
    def title(self) -> str:
        return clean_text(" ".join(self._title_parts))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {name: str(value or "") for name, value in attrs}
        if tag.lower() == "title":
            self._in_title = True
            return
        if tag.lower() != "div":
            return
        classes = set(clean_text(attrs_dict.get("class")).split())
        parent_is_left = self._div_left_stack[-1] if self._div_left_stack else False
        in_left = parent_is_left or "physician-details-left" in classes
        self._div_left_stack.append(in_left)
        if in_left and "media-img" in classes:
            self.media_attrs.append(attrs_dict)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False
        elif tag.lower() == "div" and self._div_left_stack:
            self._div_left_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)


@dataclass(frozen=True)
class PortraitReference:
    page_title: str
    photo_url: str
    source_attribute: str


def inspect_portrait_reference(html: str, source_link: str, expected_name: str) -> tuple[str, PortraitReference | None]:
    if not detail_id(source_link):
        raise RuntimeError(f"非授权官网详情链接：{source_link}")
    parser = PhysicianPageParser()
    parser.feed(html)
    expected_title = f"{clean_text(expected_name)} | {HOSPITAL}"
    if parser.title != expected_title:
        raise RuntimeError(
            f"详情标题与底表不一致：底表={expected_name} 官网={parser.title or '空'} {source_link}"
        )
    if not parser.media_attrs:
        return "无照片容器", None
    if len(parser.media_attrs) != 1:
        raise RuntimeError(
            f"医生详情区 media-img 不唯一：{source_link} 数量={len(parser.media_attrs)}"
        )
    attrs = parser.media_attrs[0]
    data_value = clean_text(attrs.get("data-image-url"))
    style_value = style_background_url(attrs.get("style"))
    candidates = [value for value in (data_value, style_value) if value]
    if not candidates:
        return "无照片容器", None
    normalized = [page_referenced_photo_url(value, source_link) for value in candidates]
    if not all(normalized):
        raw_path = " ".join(unquote(urlparse(urljoin(source_link, value)).path).lower() for value in candidates)
        if any(marker in raw_path for marker in PLACEHOLDER_MARKERS):
            return "占位图", None
        raise RuntimeError(f"页面引用照片 URL 越界：{source_link} {candidates}")
    if len(set(normalized)) != 1:
        raise RuntimeError(f"data-image-url 与 background-image 不一致：{source_link}")
    return "", PortraitReference(
        page_title=parser.title,
        photo_url=normalized[0],
        source_attribute="data-image-url" if data_value else "inline background-image",
    )


class OfficialSession:
    def __init__(self) -> None:
        self.cookie_jar = CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.cookie_jar))

    @property
    def cookie_names(self) -> list[str]:
        return sorted(cookie.name for cookie in self.cookie_jar)

    def get(self, url: str, referer: str = "") -> tuple[int, str, str, bytes]:
        headers = {"User-Agent": USER_AGENT}
        if referer:
            headers["Referer"] = referer
        request = Request(url, headers=headers)
        try:
            with self.opener.open(request, timeout=35) as response:
                content = response.read()
                return (
                    int(response.status),
                    response.headers.get_content_type(),
                    response.headers.get_content_charset() or "utf-8",
                    content,
                )
        except HTTPError as exc:
            content = exc.read()
            return int(exc.code), exc.headers.get_content_type(), exc.headers.get_content_charset() or "utf-8", content
        except URLError as exc:
            raise RuntimeError(f"官网请求失败：{url} {exc}") from exc


def magic_extension(content: bytes, content_type: str | None) -> str:
    media_type = clean_text(content_type).split(";", 1)[0].lower()
    if not media_type.startswith("image/"):
        return ""
    if content.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if content.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if len(content) >= 12 and content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return "webp"
    return ""


def image_dimensions(content: bytes) -> tuple[int, int]:
    with Image.open(io.BytesIO(content)) as image:
        image.verify()
    with Image.open(io.BytesIO(content)) as image:
        image.load()
        return int(image.width), int(image.height)


def file_snapshot(paths: list[Path]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in paths:
        if not path.is_file():
            raise RuntimeError(f"受保护资产缺失：{path}")
        content = path.read_bytes()
        result[str(path)] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    return result


def tree_snapshot(root: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    count = 0
    total_bytes = 0
    if root.is_dir():
        for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix()):
            relative = path.relative_to(root).as_posix().encode("utf-8")
            content = path.read_bytes()
            digest.update(relative + b"\0" + content)
            count += 1
            total_bytes += len(content)
    return {"exists": root.is_dir(), "file_count": count, "bytes": total_bytes, "sha256": digest.hexdigest()}


def protected_snapshot() -> dict[str, Any]:
    return {
        "master_assets": file_snapshot(
            [MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH, MASTER_REPORT_PATH]
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
        raise RuntimeError("Issue #57 TRIAL 范围内已有照片字段，需 owner 先裁决")
    sources = [clean_text(row.get("来源链接")) for row in rows]
    if len(sources) != len(set(sources)):
        raise RuntimeError("Issue #57 范围来源链接不唯一")
    invalid = [source for source in sources if not detail_id(source)]
    if invalid:
        raise RuntimeError("Issue #57 范围存在非授权详情链接：" + "、".join(invalid[:5]))
    return rows


def select_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for expected_name, expected_level in SAMPLE_PLAN:
        matches = [row for row in rows if clean_text(row.get("姓名")) == expected_name]
        if len(matches) != 1:
            raise RuntimeError(f"试采姓名范围不唯一：{expected_name} 数量={len(matches)}")
        row = dict(matches[0])
        actual_level = title_level(row.get("职称身份原文"))
        if actual_level != expected_level:
            raise RuntimeError(
                f"试采职称层级漂移：{expected_name} 应为 {expected_level} 实际 {actual_level}"
            )
        result.append(row)
    departments = {atomic_department(row) for row in result}
    levels = {title_level(row.get("职称身份原文")) for row in result}
    if len(departments) < MIN_TRIAL_DEPARTMENTS:
        raise RuntimeError(f"科室覆盖不足：{len(departments)}")
    if levels != {"正高", "副高", "中级", "初级"}:
        raise RuntimeError(f"职称分层覆盖不完整：{sorted(levels)}")
    return result


def allocate_trial_photo(row: dict[str, Any], extension: str, content: bytes) -> tuple[str, Path]:
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
        raise RuntimeError(f"TRIAL 照片已存在且字节不同，拒绝覆盖：{path}")
    return filename, path


def contact_sheet_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
    ):
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def build_contact_sheet(samples: list[dict[str, Any]]) -> None:
    columns = 2
    cell_width = 500
    cell_height = 520
    rows = (len(samples) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_width, rows * cell_height), "white")
    draw = ImageDraw.Draw(canvas)
    font = contact_sheet_font(20)
    small_font = contact_sheet_font(17)
    for index, sample in enumerate(samples):
        left = (index % columns) * cell_width
        top = (index // columns) * cell_height
        with Image.open(sample["disk_path"]) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            thumb = ImageOps.contain(image, (440, 390))
        image_left = left + (cell_width - thumb.width) // 2
        image_top = top + 10 + (390 - thumb.height) // 2
        canvas.paste(thumb, (image_left, image_top))
        draw.rectangle((left, top, left + cell_width - 1, top + cell_height - 1), outline="#B7C0C8", width=2)
        draw.text((left + 20, top + 410), f"{index + 1}. {sample['name']}｜{sample['title']}", fill="black", font=font)
        draw.text((left + 20, top + 448), sample["department"], fill="#333333", font=small_font)
        draw.text((left + 20, top + 482), f"{sample['width']}×{sample['height']}｜{sample['bytes']} bytes", fill="#555555", font=small_font)
    canvas.save(CONTACT_SHEET_PATH, format="JPEG", quality=90, optimize=True)


def write_manifest(rows: list[dict[str, Any]]) -> None:
    fields = [
        "姓名",
        "科室",
        "职称层级",
        "主职称",
        "来源链接",
        "详情HTTP",
        "照片链接",
        "照片HTTP",
        "文件名",
        "字节",
        "SHA-256",
        "魔数",
        "宽",
        "高",
        "大图判定",
    ]
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def markdown_cell(value: Any) -> str:
    return clean_text(value).replace("|", "\\|").replace("\n", " ")


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    rows = []
    for sample in payload["photo_samples"]:
        rows.append(
            "| {name} | {department} | {level} | {title} | {filename} | {bytes} | {width}×{height} | `{sha256}` | {photo_url} |".format(
                name=markdown_cell(sample["name"]),
                department=markdown_cell(sample["department"]),
                level=sample["title_level"],
                title=markdown_cell(sample["title"]),
                filename=markdown_cell(sample["filename"]),
                bytes=sample["bytes"],
                width=sample["width"],
                height=sample["height"],
                sha256=sample["sha256"],
                photo_url=sample["photo_url"],
            )
        )
    protected_rows = []
    for path, facts in meta["protected_assets_before"]["master_assets"].items():
        protected_rows.append(f"| `{path}` | {facts['bytes']} | `{facts['sha256']}` |")
    level_text = "、".join(f"{key} {value}" for key, value in meta["title_level_counts"].items())
    report = f"""# Issue #57 {HOSPITAL}照片补录 TRIAL 报告

> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 生成日期：{meta['run_date']}
> 视觉复核：`{meta['visual_review_status']}`

## 范围与抽样

- 总底表目标范围：{meta['scope_count']} 行；照片链接/照片文件均为空；来源链接唯一 {meta['scope_unique_source_count']}。
- 固定样本：{meta['trial_detail_count']} 位，覆盖 {meta['department_coverage_count']} 个科室；职称分层为 {level_text}。
- 详情页：HTTP 200 为 {meta['detail_http_200_count']}/{meta['trial_detail_count']}；无照片容器 {meta['no_photo_container_count']}；占位图 {meta['placeholder_count']}；结构异常 {meta['structure_mismatch_count']}。
- 熔断三态合计 {meta['fuse_problem_count']}/{meta['trial_detail_count']}（{meta['fuse_problem_ratio']:.1%}），未超过 owner 规定的 30% 门槛。
- 常规会话仅记录 Cookie 名称：{', '.join(meta['cookie_names']) or '无'}；不记录 Cookie 值。照片请求均携带对应详情页 Referer。

## 实图、命名与容量

- 实图：{meta['photo_sample_count']} 张；全部保存页面自身引用的官网响应原始字节，未压缩。
- 总字节：{meta['photo_total_bytes']}；平均：{meta['photo_average_bytes']} bytes。
- 按平均值对 780 行线性估算：{meta['estimated_full_bytes']} bytes（约 {meta['estimated_full_mib']:.2f} MiB）；仅供 owner 裁决，不代表 FULL 最终可得数或实际容量。
- 单张 >200KB：{meta['over_200kb_count']}/{meta['photo_sample_count']}；宽 >800px：{meta['over_800px_count']}/{meta['photo_sample_count']}。
- 页面未引用路径构造/探测请求：0；第三方来源：0。

| 姓名 | 科室 | 层级 | 主职称 | 文件名 | 字节 | 尺寸 | SHA-256 | 页面引用照片 |
|---|---|---|---|---|---:|---:|---|---|
{chr(10).join(rows)}

详细 HTTP、魔数和逐图命名清单见：`{TRIAL_CSV_PATH}` 与 `{TRIAL_JSON_PATH}`。

## 视觉判定标准与复核

1. 本人职业照：必须位于该医生 `.physician-details-left .physician-details-media .media-img` 内，详情标题与底表姓名一致，照片由 `data-image-url` 或同容器内联 `background-image` 明确引用；联系表中视觉上为单人成人职业照。
2. 占位图：路径含 default/avatar/placeholder 等标记、多个医生重复同一 SHA-256、或视觉为站点通用图/云上三院入口图/期刊二维码时拒绝。
3. 站点通用图：即使位于同页，只要不属于医生左侧详情容器，或是“脑病服务、出诊、服务、云上三院、二维码”等功能图，均不采纳。
4. 联系表：`{CONTACT_SHEET_PATH}`；当前状态为 `{meta['visual_review_status']}`。

## 受保护正式资产零变更

| 文件 | 字节 | SHA-256 |
|---|---:|---|
{chr(10).join(protected_rows)}

- 本院画像树：{meta['protected_assets_before']['profile_tree']['file_count']} 个文件，SHA-256 `{meta['protected_assets_before']['profile_tree']['sha256']}`。
- 本院正式照片目录执行前后状态一致：{json.dumps(meta['protected_assets_before']['formal_photo_tree'], ensure_ascii=False)}。
- TRIAL 照片只写入 `work` 下独立目录：`{TRIAL_PHOTO_DIR}`；未写总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件完成后停止，等待 owner 审计照片质量、样本大图分布和 780 行容量估算。未取得 owner 明确 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填三载体、刷新画像或写正式照片目录。
"""
    TRIAL_REPORT_PATH.write_text(report, encoding="utf-8")


def validate_payload(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    errors: list[str] = []
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围不是 780 行")
    if meta.get("trial_detail_count") != EXPECTED_TRIAL_COUNT:
        errors.append("详情样本不是 10 位")
    if meta.get("department_coverage_count", 0) < MIN_TRIAL_DEPARTMENTS:
        errors.append("科室覆盖不足 3 个")
    if set(meta.get("title_level_counts", {})) != {"正高", "副高", "中级", "初级"}:
        errors.append("职称分层不完整")
    if float(meta.get("fuse_problem_ratio", 1)) > MAX_FAILURE_RATIO:
        errors.append("熔断问题占比超过 30%")
    if meta.get("constructed_unreferenced_probe_count") != 0:
        errors.append("发生页面未引用路径探测")
    if meta.get("third_party_source_count") != 0:
        errors.append("发生第三方来源访问")
    if meta.get("protected_assets_before") != meta.get("protected_assets_after"):
        errors.append("正式受保护资产发生变化")
    filenames: set[str] = set()
    for sample in payload.get("photo_samples", []):
        path = Path(sample["disk_path"])
        if not path.is_file():
            errors.append(f"照片不存在：{path}")
            continue
        content = path.read_bytes()
        if len(content) != sample.get("bytes"):
            errors.append(f"照片字节不一致：{path.name}")
        if hashlib.sha256(content).hexdigest() != sample.get("sha256"):
            errors.append(f"照片 SHA-256 不一致：{path.name}")
        extension = magic_extension(content, sample.get("content_type"))
        if extension != path.suffix.lower().lstrip("."):
            errors.append(f"照片魔数与扩展名不一致：{path.name}")
        if image_dimensions(content) != (sample.get("width"), sample.get("height")):
            errors.append(f"照片尺寸不一致：{path.name}")
        if not page_referenced_photo_url(sample.get("photo_url"), sample.get("source_link")):
            errors.append(f"照片 URL 越界：{path.name}")
        filenames.add(path.name.casefold())
    if len(filenames) != meta.get("photo_sample_count"):
        errors.append("照片文件名覆盖或数量不一致")
    if not CONTACT_SHEET_PATH.is_file():
        errors.append("联系表不存在")
    if errors:
        raise RuntimeError("Issue #57 TRIAL 门禁失败：" + "；".join(errors))


def run_trial(run_date: str) -> dict[str, Any]:
    protected_before = protected_snapshot()
    scope_rows = load_scope_rows()
    trial_rows = select_trial_rows(scope_rows)
    session = OfficialSession()
    home_status, _, _, _ = session.get(OFFICIAL_HOME)
    if home_status != 200:
        raise RuntimeError(f"官网首页常规会话建立失败：HTTP {home_status}")

    detail_errors: list[dict[str, Any]] = []
    structure_mismatches: list[dict[str, Any]] = []
    failure_states: list[dict[str, Any]] = []
    portrait_rows: list[tuple[dict[str, Any], PortraitReference, int]] = []
    for row in trial_rows:
        source_link = clean_text(row.get("来源链接"))
        status, content_type, charset, content = session.get(source_link, DIRECTORY_URL)
        if status != 200 or content_type != "text/html":
            detail_errors.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "status": status, "content_type": content_type}
            )
            continue
        html = content.decode(charset, errors="replace")
        try:
            failure_state, portrait = inspect_portrait_reference(html, source_link, clean_text(row.get("姓名")))
        except RuntimeError as exc:
            structure_mismatches.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "error": str(exc)}
            )
            continue
        if failure_state or portrait is None:
            failure_states.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "state": failure_state or "未知"}
            )
            continue
        portrait_rows.append((row, portrait, status))

    TRIAL_PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    photo_errors: list[dict[str, Any]] = []
    photo_samples: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    for row, portrait, detail_status in portrait_rows:
        source_link = clean_text(row.get("来源链接"))
        photo_status, content_type, _, content = session.get(portrait.photo_url, source_link)
        if photo_status != 200:
            photo_errors.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "photo_url": portrait.photo_url, "status": photo_status}
            )
            continue
        extension = magic_extension(content, content_type)
        if not extension:
            photo_errors.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "photo_url": portrait.photo_url, "error": f"非受支持图片：{content_type}"}
            )
            continue
        try:
            width, height = image_dimensions(content)
            filename, path = allocate_trial_photo(row, extension, content)
            if not path.exists():
                path.write_bytes(content)
        except Exception as exc:  # noqa: BLE001 - retain exact per-image evidence
            photo_errors.append(
                {"name": clean_text(row.get("姓名")), "source_link": source_link, "photo_url": portrait.photo_url, "error": str(exc)}
            )
            continue
        digest = hashlib.sha256(content).hexdigest()
        large_reasons = []
        if len(content) > LARGE_BYTES:
            large_reasons.append(">200KB")
        if width > LARGE_WIDTH:
            large_reasons.append("宽>800px")
        sample = {
            "name": clean_text(row.get("姓名")),
            "department": atomic_department(row),
            "title_level": title_level(row.get("职称身份原文")),
            "title": primary_title(row.get("职称身份原文")),
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
        photo_samples.append(sample)
        manifest_rows.append(
            {
                "姓名": sample["name"],
                "科室": sample["department"],
                "职称层级": sample["title_level"],
                "主职称": sample["title"],
                "来源链接": source_link,
                "详情HTTP": detail_status,
                "照片链接": portrait.photo_url,
                "照片HTTP": photo_status,
                "文件名": filename,
                "字节": len(content),
                "SHA-256": digest,
                "魔数": sample["magic_hex"],
                "宽": width,
                "高": height,
                "大图判定": "、".join(large_reasons) or "未命中",
            }
        )

    build_contact_sheet(photo_samples)
    protected_after = protected_snapshot()
    fuse_problem_count = len(detail_errors) + len(structure_mismatches) + len(failure_states) + len(photo_errors)
    fuse_ratio = fuse_problem_count / EXPECTED_TRIAL_COUNT
    if fuse_ratio > MAX_FAILURE_RATIO:
        raise RuntimeError(
            f"[FATAL - HUMAN_INTERVENTION_REQUIRED] TRIAL 熔断问题超过 30%：{fuse_problem_count}/{EXPECTED_TRIAL_COUNT}"
        )
    total_bytes = sum(sample["bytes"] for sample in photo_samples)
    average_bytes = total_bytes // max(1, len(photo_samples))
    estimated_full = average_bytes * EXPECTED_SCOPE_COUNT
    title_counts = Counter(title_level(row.get("职称身份原文")) for row in trial_rows)
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "phase": "TRIAL_READY_FOR_OWNER_AUDIT",
            "hospital": HOSPITAL,
            "run_date": run_date,
            "scope_count": len(scope_rows),
            "scope_unique_source_count": len({clean_text(row.get("来源链接")) for row in scope_rows}),
            "trial_detail_count": len(trial_rows),
            "department_coverage_count": len({atomic_department(row) for row in trial_rows}),
            "covered_departments": sorted({atomic_department(row) for row in trial_rows}),
            "title_level_counts": {level: title_counts[level] for level in ("正高", "副高", "中级", "初级")},
            "home_http_status": home_status,
            "cookie_names": session.cookie_names,
            "detail_http_200_count": len(portrait_rows) + len(failure_states),
            "no_photo_container_count": sum(item["state"] == "无照片容器" for item in failure_states),
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
            "estimated_full_bytes": estimated_full,
            "estimated_full_mib": estimated_full / 1024 / 1024,
            "over_200kb_count": sum(sample["bytes"] > LARGE_BYTES for sample in photo_samples),
            "over_800px_count": sum(sample["width"] > LARGE_WIDTH for sample in photo_samples),
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
                "科室": atomic_department(row),
                "职称层级": title_level(row.get("职称身份原文")),
                "主职称": primary_title(row.get("职称身份原文")),
                "来源链接": clean_text(row.get("来源链接")),
            }
            for row in trial_rows
        ],
    }
    validate_payload(payload)
    TRIAL_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(manifest_rows)
    write_report(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #57 中山三院照片补录 TRIAL")
    parser.add_argument("--trial-only", action="store_true", help="执行固定 10 位 TRIAL")
    parser.add_argument("--run-date", default=date.today().isoformat())
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.validate_only:
        payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
        validate_payload(payload)
        print(json.dumps({"status": "validated", "photos": payload["meta"]["photo_sample_count"]}, ensure_ascii=False))
        return
    if not args.trial_only:
        raise RuntimeError("Issue #57 当前仅授权 --trial-only；FULL 在联网与正式资产写入前硬熔断")
    payload = run_trial(args.run_date)
    print(json.dumps(payload["meta"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
