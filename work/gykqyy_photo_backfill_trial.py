from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from http.client import IncompleteRead
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, unquote, urlparse
from urllib.request import (
    HTTPRedirectHandler,
    HTTPCookieProcessor,
    Request,
    build_opener,
)

from PIL import Image, ImageDraw, ImageOps

import sys2_photo_backfill_trial as common


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work"
VAULT = ROOT / "医生画像仓库"
SOURCE_DIR = VAULT / "99_资料来源"
HOSPITAL = "广州医科大学附属口腔医院"
ISSUE_NUMBER = 75
BRANCH = "codex/mhrj/issue-75-gykqyy-photo-backfill-trial"

MASTER_BASENAME = "珠三角三甲医院_医生画像自动采集总底表"
MASTER_JSON_PATH = WORK_DIR / f"{MASTER_BASENAME}_payload.json"
MASTER_CSV_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.csv"
MASTER_XLSX_PATH = SOURCE_DIR / f"{MASTER_BASENAME}.xlsx"
MASTER_REPORT_PATH = SOURCE_DIR / f"{MASTER_BASENAME}_更新报告.md"
LEDGER_JSON_PATH = WORK_DIR / "pearl_delta_hospital_entry_ledger.json"
LEDGER_CSV_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.csv"
LEDGER_XLSX_PATH = SOURCE_DIR / "珠三角三甲医院官网入口台账.xlsx"
PROFILE_DIR = VAULT / "01_试点医院" / HOSPITAL
FORMAL_PHOTO_DIR = PROFILE_DIR / "照片"

TRIAL_BASENAME = f"{HOSPITAL}_photo_backfill_trial"
TRIAL_JSON_PATH = WORK_DIR / f"{TRIAL_BASENAME}_payload.json"
TRIAL_CSV_PATH = WORK_DIR / f"{TRIAL_BASENAME}_manifest.csv"
TRIAL_REPORT_PATH = WORK_DIR / f"{TRIAL_BASENAME}_report.md"
CONTACT_SHEET_PATH = WORK_DIR / f"{TRIAL_BASENAME}_contact_sheet.jpg"
TRIAL_PHOTO_DIR = WORK_DIR / f"{TRIAL_BASENAME}_photos"

OFFICIAL_HOME = "https://www.gykqyy.com/"
DIRECTORY_URL = "https://www.gykqyy.com/list.html?category=55"
DIRECTORY_API = "https://www.gykqyy.com/api/article/getZhuanjiaList?category=55"
OFFICIAL_HOST = "gykqyy.com"
EXPECTED_CATEGORY = "55"
EXPECTED_SCOPE_COUNT = 297
EXPECTED_GROUP_COUNT = 5
EXPECTED_DEPARTMENT_COUNT = 31
EXPECTED_RELATION_COUNT = 317
EXPECTED_API_OBJECT_OCCURRENCES = 384
EXPECTED_TRIAL_COUNT = 10
EXPECTED_PROFILE_FILE_COUNT = 298
MAX_PHOTO_BYTES = 20 * 1024 * 1024
OWNER_REPORT_BYTES = 5 * 1024 * 1024
PHOTO_RETRY_SECONDS = 30
VISUAL_PASS = "PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36; "
    "public official-site photo backfill trial"
)

PHOTO_PATH_RE = re.compile(
    r"^/uploads/\d{8}/[0-9a-f]{32}\.(?:jpe?g|png|gif|webp)$",
    re.IGNORECASE,
)

DIRECTORY_MARKERS = {
    "directory_api": re.compile(r"getZhuanjiaList"),
    "category_branch": re.compile(r"currentId\.value\s*==\s*55"),
    "image_fallback": re.compile(
        r"item3\.image\s*\|\|\s*['\"]\./images/null\.jpg['\"]"
    ),
    "detail_category": re.compile(r"item3\.yccms_category_id"),
}

# Owner ruling in Issue #75 changed the category gate to official department
# coverage. These ten IDs cover ten distinct first department atoms and the two
# available title levels among the 58 valid /uploads photo candidates.
SAMPLE_PLAN = (
    (195, "李江", "正高"),
    (136, "张清彬", "正高"),
    (80, "江千舟", "正高"),
    (51, "朴正国", "正高"),
    (110, "刘畅", "正高"),
    (152, "张云燕", "副高"),
    (5, "杜发亮", "副高"),
    (241, "余挺", "副高"),
    (287, "熊洁", "副高"),
    (258, "张斌", "副高"),
)

EXCLUSION_POLICY = (
    "API image 为空/null：无照片容器，记录字段值，不下载 fallback",
    "./images/null.jpg：页面 fallback，占位资源，下载数必须为 0",
    "/images/ 下 search、yuandian、logo 等静态资源：公共装饰图，下载数必须为 0",
    "非 www.gykqyy.com/uploads/<日期>/<hash>.<格式>：不是获准 image 原图，禁止构造或探测",
)


def clean_text(value: Any) -> str:
    return common.clean_text(value)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def comparable_host(value: str) -> str:
    return common.comparable_host(value)


def source_id(value: Any) -> str:
    text = clean_text(value)
    parsed = urlparse(text)
    if (
        parsed.scheme != "https"
        or comparable_host(text) != OFFICIAL_HOST
        or parsed.path != "/list.html"
        or parsed.fragment
    ):
        return ""
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    if len(pairs) != 2 or {key for key, _value in pairs} != {"category", "id"}:
        return ""
    values = dict(pairs)
    if values.get("category") != EXPECTED_CATEGORY or not re.fullmatch(r"\d+", values.get("id", "")):
        return ""
    return values["id"]


def safe_photo_part(value: Any) -> str:
    return common.safe_photo_part(value)


def atomic_department(row: dict[str, Any]) -> str:
    value = clean_text(row.get("科室_分类页") or row.get("科室_列表卡片"))
    atoms = [clean_text(item) for item in re.split(r"[、,，;/；|]+", value) if clean_text(item)]
    return safe_photo_part(atoms[0] if atoms else "未标注")


def primary_title(value: Any) -> str:
    return common.primary_title(value)


def title_level(value: Any) -> str:
    return common.title_level(value)


def page_referenced_photo_url(raw_url: Any) -> str:
    value = clean_text(raw_url)
    if not value:
        return ""
    parsed = urlparse(value)
    if (
        parsed.scheme != "https"
        or comparable_host(value) != OFFICIAL_HOST
        or parsed.query
        or parsed.fragment
        or not PHOTO_PATH_RE.fullmatch(unquote(parsed.path))
    ):
        return ""
    return value


def image_field_signal(value: Any) -> str:
    raw = clean_text(value)
    if not raw:
        return "NO_PHOTO_CONTAINER_EMPTY_IMAGE_FIELD"
    if page_referenced_photo_url(raw):
        return "VALID_REFERENCED_ORIGINAL"
    return "NO_PHOTO_CONTAINER_NON_UPLOAD_IMAGE_FIELD"


class RedirectRecorder(HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.events: list[dict[str, Any]] = []

    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> Request | None:
        self.events.append({"status": int(code), "from": req.full_url, "to": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


@dataclass(frozen=True)
class HttpResult:
    status: int
    content_type: str
    charset: str
    content: bytes
    final_url: str
    redirects: tuple[dict[str, Any], ...]


class OfficialSession:
    def __init__(self) -> None:
        self.cookie_jar = CookieJar()
        self.redirect_recorder = RedirectRecorder()
        self.opener = build_opener(
            HTTPCookieProcessor(self.cookie_jar), self.redirect_recorder
        )
        self.incomplete_read_retry_count = 0

    @property
    def cookie_names(self) -> list[str]:
        return sorted(cookie.name for cookie in self.cookie_jar)

    def get(self, url: str, referer: str = "") -> HttpResult:
        if comparable_host(url) != OFFICIAL_HOST:
            raise RuntimeError(f"请求越出官网：{url}")
        headers = {"User-Agent": USER_AGENT}
        if referer:
            headers["Referer"] = referer
        request = Request(url, headers=headers)
        redirect_start = len(self.redirect_recorder.events)
        for attempt in range(2):
            try:
                with self.opener.open(request, timeout=35) as response:
                    content = response.read()
                    return HttpResult(
                        status=int(response.status),
                        content_type=response.headers.get_content_type(),
                        charset=response.headers.get_content_charset() or "utf-8",
                        content=content,
                        final_url=response.geturl(),
                        redirects=tuple(self.redirect_recorder.events[redirect_start:]),
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
                    redirects=tuple(self.redirect_recorder.events[redirect_start:]),
                )
            except URLError as exc:
                raise RuntimeError(f"官网请求失败：{url} {exc}") from exc
        raise AssertionError("官网请求循环未返回")


def fetch_photo_with_retry(
    session: OfficialSession,
    photo_url: str,
    source_link: str,
    sleep_func: Callable[[float], None] = time.sleep,
) -> tuple[HttpResult, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    last: HttpResult | None = None
    for attempt in range(2):
        try:
            result = session.get(photo_url, referer=source_link)
            last = result
            attempts.append(
                {
                    "attempt": attempt + 1,
                    "utc": utc_now(),
                    "status": result.status,
                    "content_type": result.content_type,
                    "final_url": result.final_url,
                    "bytes": len(result.content),
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
                    "bytes": 0,
                    "error": str(exc),
                }
            )
        if attempt == 0:
            sleep_func(PHOTO_RETRY_SECONDS)
    if last is not None:
        return last, attempts
    raise RuntimeError(f"照片资源连续两次请求失败：{photo_url} {attempts}")


def decode_json_response(result: HttpResult, label: str) -> dict[str, Any]:
    if result.status != 200:
        raise RuntimeError(f"{label} HTTP {result.status}")
    if result.content_type != "application/json":
        raise RuntimeError(
            f"{label} HTTP {result.status} 返回非 JSON Content-Type：{result.content_type}"
        )
    try:
        payload = json.loads(result.content.decode(result.charset, errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{label} HTTP {result.status} JSON 解析失败：{exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label} HTTP {result.status} JSON 顶层不是对象")
    return payload


def directory_source_evidence(html: str) -> dict[str, Any]:
    missing = [name for name, pattern in DIRECTORY_MARKERS.items() if not pattern.search(html)]
    if missing:
        raise RuntimeError(f"目录页缺少页面自身调用证据：{', '.join(missing)}")
    marker = "getZhuanjiaList"
    start = max(0, html.index(marker) - 500)
    end = min(len(html), html.index(marker) + 1200)
    snippet = re.sub(r"\s+", " ", html[start:end]).strip()
    return {
        "markers": sorted(DIRECTORY_MARKERS),
        "snippet": snippet,
        "html_bytes": len(html.encode("utf-8")),
        "html_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
    }


def parse_directory_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("code") != 1:
        raise RuntimeError(f"目录 API 业务失败：code={payload.get('code')} msg={payload.get('msg')}")
    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("目录 API data 不是对象")
    groups = data.get("list")
    banner = data.get("banner")
    if not isinstance(groups, list) or not isinstance(banner, list):
        raise RuntimeError("目录 API list/banner 结构异常")

    by_id: dict[str, dict[str, Any]] = {}
    relations: list[dict[str, Any]] = []
    category_occurrences: list[str] = []
    departments: list[dict[str, Any]] = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        group_name = clean_text(group.get("name"))
        children = group.get("child") or []
        if not isinstance(children, list):
            raise RuntimeError("目录 API 分组 child 不是数组")
        for department in children:
            if not isinstance(department, dict):
                continue
            department_name = clean_text(department.get("name"))
            department_id = clean_text(department.get("id"))
            doctors = department.get("child") or []
            if not isinstance(doctors, list):
                raise RuntimeError("目录 API 科室 child 不是数组")
            departments.append(
                {
                    "group": group_name,
                    "id": department_id,
                    "name": department_name,
                    "doctor_relation_count": len(doctors),
                }
            )
            for doctor in doctors:
                if not isinstance(doctor, dict):
                    continue
                doctor_id = clean_text(doctor.get("id"))
                if not doctor_id or not re.fullmatch(r"\d+", doctor_id):
                    raise RuntimeError("目录 API 科室树出现空或非数字医生 ID")
                category_occurrences.append(clean_text(doctor.get("yccms_category_id")))
                relations.append(
                    {
                        "group": group_name,
                        "department": department_name,
                        "department_id": department_id,
                        "doctor_id": doctor_id,
                    }
                )
                item = by_id.setdefault(
                    doctor_id,
                    {**doctor, "id": doctor_id, "departments": [], "department_ids": [], "groups": []},
                )
                if department_name and department_name not in item["departments"]:
                    item["departments"].append(department_name)
                if department_id and department_id not in item["department_ids"]:
                    item["department_ids"].append(department_id)
                if group_name and group_name not in item["groups"]:
                    item["groups"].append(group_name)

    banner_by_id: dict[str, dict[str, Any]] = {}
    for item in banner:
        if not isinstance(item, dict):
            continue
        item_id = clean_text(item.get("id"))
        if not item_id:
            continue
        category_occurrences.append(clean_text(item.get("yccms_category_id")))
        banner_by_id[item_id] = item

    doctors: list[dict[str, Any]] = []
    for doctor_id, item in by_id.items():
        merged = {**item}
        merged.update(
            {
                key: value
                for key, value in banner_by_id.get(doctor_id, {}).items()
                if value not in {None, ""}
            }
        )
        merged["id"] = doctor_id
        doctors.append(merged)
    doctors.sort(key=lambda item: (-int(item.get("weigh") or 0), int(item["id"])))

    return {
        "groups": groups,
        "banner": banner,
        "departments": departments,
        "relations": relations,
        "doctors": doctors,
        "banner_unique_ids": sorted(banner_by_id, key=int),
        "category_occurrences": category_occurrences,
    }


def file_snapshot(paths: list[Path]) -> dict[str, dict[str, Any]]:
    return common.file_snapshot(paths)


def tree_snapshot(path: Path) -> dict[str, Any]:
    return common.tree_snapshot(path)


def protected_snapshot() -> dict[str, Any]:
    return {
        "ledger_assets": file_snapshot(
            [LEDGER_JSON_PATH, LEDGER_CSV_PATH, LEDGER_XLSX_PATH]
        ),
        "master_assets": file_snapshot(
            [MASTER_JSON_PATH, MASTER_CSV_PATH, MASTER_XLSX_PATH, MASTER_REPORT_PATH]
        ),
        "profile_tree": tree_snapshot(PROFILE_DIR),
        "formal_photo_tree": tree_snapshot(FORMAL_PHOTO_DIR),
    }


def load_scope_rows() -> list[dict[str, Any]]:
    payload = json.loads(MASTER_JSON_PATH.read_text(encoding="utf-8"))
    rows = [row for row in payload.get("rows", []) if row.get("医院") == HOSPITAL]
    if len(rows) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError(f"总底表本院范围不是 {EXPECTED_SCOPE_COUNT} 行：{len(rows)}")
    ids: set[str] = set()
    for row in rows:
        item_id = source_id(row.get("来源链接"))
        if not item_id:
            raise RuntimeError(f"总底表存在越界来源链接：{row.get('来源链接')}")
        if item_id in ids:
            raise RuntimeError(f"总底表来源 ID 重复：{item_id}")
        ids.add(item_id)
        if clean_text(row.get("照片链接")) or clean_text(row.get("照片文件")):
            raise RuntimeError(f"TRIAL 前已有照片字段：{row.get('姓名')} id={item_id}")
    if len(ids) != EXPECTED_SCOPE_COUNT:
        raise RuntimeError("总底表固定范围来源 ID 不唯一")
    return rows


def reconcile_scope(
    rows: list[dict[str, Any]], doctors: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    by_id = {clean_text(item.get("id")): item for item in doctors}
    row_ids = {source_id(row.get("来源链接")) for row in rows}
    if set(by_id) != row_ids:
        missing_api = sorted(row_ids - set(by_id), key=int)
        extra_api = sorted(set(by_id) - row_ids, key=int)
        raise RuntimeError(f"API/底表 ID 不一致：missing_api={missing_api} extra_api={extra_api}")
    records: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda item: int(source_id(item.get("来源链接")))):
        item_id = source_id(row.get("来源链接"))
        doctor = by_id[item_id]
        row_name = clean_text(row.get("姓名"))
        api_name = clean_text(doctor.get("title"))
        if not row_name or row_name != api_name:
            raise RuntimeError(f"API/底表姓名不一致：id={item_id} master={row_name} api={api_name}")
        raw_image = clean_text(doctor.get("image"))
        records.append(
            {
                "id": item_id,
                "name": row_name,
                "source_link": clean_text(row.get("来源链接")),
                "master_department": clean_text(row.get("科室_分类页")),
                "first_department_atom": atomic_department(row),
                "master_title": clean_text(row.get("职称身份原文")),
                "api_category": clean_text(doctor.get("yccms_category_id")),
                "api_keshi_ids": clean_text(doctor.get("keshi_ids")),
                "api_keshi": clean_text(doctor.get("keshi")),
                "api_title": clean_text(doctor.get("zhicheng")),
                "api_image_field_value": raw_image,
                "image_signal": image_field_signal(raw_image),
                "valid_photo_url": page_referenced_photo_url(raw_image),
            }
        )
    return records


def select_trial_rows(
    rows: list[dict[str, Any]], scope_records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows_by_id = {source_id(row.get("来源链接")): row for row in rows}
    records_by_id = {record["id"]: record for record in scope_records}
    selected: list[dict[str, Any]] = []
    for numeric_id, expected_name, expected_level in SAMPLE_PLAN:
        item_id = str(numeric_id)
        row = rows_by_id.get(item_id)
        record = records_by_id.get(item_id)
        if row is None or record is None:
            raise RuntimeError(f"固定样本缺失：id={item_id}")
        if clean_text(row.get("姓名")) != expected_name:
            raise RuntimeError(f"固定样本姓名漂移：id={item_id}")
        level = title_level(row.get("职称身份原文"))
        if level != expected_level:
            raise RuntimeError(f"固定样本职称层漂移：id={item_id} {level}")
        if not record["valid_photo_url"]:
            raise RuntimeError(f"固定样本无有效 API image 原图：id={item_id}")
        selected.append({**row, "_scope_record": record})
    atoms = {atomic_department(row) for row in selected}
    if len(selected) != EXPECTED_TRIAL_COUNT or len(atoms) != EXPECTED_TRIAL_COUNT:
        raise RuntimeError("固定样本不是 10 位或科室首原子未全部分散")
    return selected


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
        filename = f"{stem}-{source_id(row.get('来源链接'))}.{extension}"
        path = TRIAL_PHOTO_DIR / filename
    if path.exists() and path.read_bytes() != content:
        raise RuntimeError(f"TRIAL 照片同名且字节不同：{path}")
    return filename, path


def build_contact_sheet(samples: list[dict[str, Any]]) -> None:
    cell_width, cell_height = 340, 450
    columns, rows = 5, 2
    sheet = Image.new("RGB", (cell_width * columns, cell_height * rows), "white")
    draw = ImageDraw.Draw(sheet)
    title_font = common.contact_sheet_font(20)
    detail_font = common.contact_sheet_font(14)
    for index, sample in enumerate(samples):
        with Image.open(ROOT / sample["disk_path"]) as image:
            image.load()
            tile = ImageOps.contain(image.convert("RGB"), (300, 335))
        x = (index % columns) * cell_width
        y = (index // columns) * cell_height
        sheet.paste(tile, (x + (cell_width - tile.width) // 2, y + 8))
        draw.text((x + 10, y + 350), sample["name"], font=title_font, fill="black")
        draw.text(
            (x + 10, y + 380),
            f"{sample['department']} | {sample['primary_title']}",
            font=detail_font,
            fill="#333333",
        )
        draw.text(
            (x + 10, y + 405),
            f"ID {sample['id']} | {sample['width']}×{sample['height']} | {sample['bytes']:,} B",
            font=detail_font,
            fill="#555555",
        )
    sheet.save(CONTACT_SHEET_PATH, format="JPEG", quality=92, optimize=True)


MANIFEST_FIELDS = [
    "id",
    "name",
    "department",
    "api_keshi_ids",
    "api_keshi",
    "primary_title",
    "title_level",
    "source_link",
    "api_url",
    "api_category",
    "api_image_field_value",
    "photo_url",
    "filename",
    "disk_path",
    "bytes",
    "sha256",
    "width",
    "height",
    "content_type",
    "extension",
    "photo_status",
    "photo_final_url",
    "photo_attempts",
]


def write_manifest(samples: list[dict[str, Any]]) -> None:
    with TRIAL_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for sample in samples:
            values = {key: sample.get(key, "") for key in MANIFEST_FIELDS}
            values["photo_attempts"] = json.dumps(
                sample.get("photo_attempts", []), ensure_ascii=False, separators=(",", ":")
            )
            writer.writerow(values)


def size_buckets(samples: list[dict[str, Any]]) -> dict[str, int]:
    return common.size_buckets(samples)


def write_report(payload: dict[str, Any]) -> None:
    meta = payload["meta"]
    samples = payload["photo_samples"]
    sample_lines = "\n".join(
        f"- {item['name']}｜ID {item['id']}｜{item['department']}｜{item['primary_title']}"
        f"（{item['title_level']}）｜keshi_ids={item['api_keshi_ids']}｜{item['bytes']:,} bytes｜"
        f"{item['width']}×{item['height']}｜`{item['sha256']}`"
        for item in samples
    )
    owner_large = [item for item in samples if item["bytes"] > OWNER_REPORT_BYTES]
    owner_lines = "\n".join(
        f"- {item['name']}｜{item['photo_url']}｜{item['bytes']:,} bytes｜"
        f"{item['width']}×{item['height']}｜`{item['sha256']}`"
        for item in owner_large
    ) or "- 无"
    policy_lines = "\n".join(f"- {item}" for item in payload["exclusion_policy"])
    trace = payload["api_trace"]
    report = f"""# Issue #{ISSUE_NUMBER} {HOSPITAL}照片补录 TRIAL 报告

## 门禁与范围

- GitHub Issue：#{ISSUE_NUMBER}
- Phase：TRIAL
- Owner 裁决：采纳方案 A，豁免第二 category；固定 category=55，改为覆盖至少两个官网科室。
- 医院官网：{OFFICIAL_HOME}
- 医生目录：{DIRECTORY_URL}
- 唯一获准 API：{DIRECTORY_API}
- 总底表固定范围：{meta['scope_count']} 行；唯一来源 {meta['unique_source_count']}；TRIAL 前照片字段非空 {meta['baseline_photo_filled_count']}。
- API 范围：{meta['group_count']} 分组、{meta['department_count']} 科室、{meta['relation_count']} 医生-科室关系、{meta['api_scope_count']} 唯一固定 ID；对象出现 {meta['api_object_occurrence_count']} 次。
- category 现场值：{json.dumps(meta['category_values'], ensure_ascii=False)}；第二 category 请求/枚举/探测均为 0。

## 页面调用与接口留痕

- 目录页 HTTP {meta['directory_status']} / `{meta['directory_content_type']}`；已验证 `currentId.value == 55`、`getZhuanjiaList`、`item3.image || './images/null.jpg'` 和 `item3.yccms_category_id`。
- API HTTP {trace['status']} / `{trace['content_type']}`；最终 URL `{trace['final_url']}`；响应 {trace['bytes']:,} bytes；SHA-256 `{trace['sha256']}`；UTC `{trace['observed_utc']}`。
- API 响应仅按 `data.list` 固定 297 ID 建立工作集；banner 范围外空白焦点项不进入固定范围。
- 未调用详情 API、未请求其他 category、未探测其他接口、未构造任何图片路径。

## image 字段普查与排除

- 固定 297 行 image 信号：{json.dumps(meta['image_signal_counts'], ensure_ascii=False)}。
- 有效 `/uploads/<日期>/<hash>.<格式>` 原图候选 {meta['valid_photo_candidate_count']}；其职称层可用数 {json.dumps(meta['valid_candidate_title_level_counts'], ensure_ascii=False)}。
- 有效照片候选中“其他”职称层为 0，故本批可实现的最大职称覆盖只有正高/副高；TRIAL 固定为 5 正高 + 5 副高并在此回报，不把无有效 image 的主治/医师伪作照片样本。
- 排除资源下载数 {meta['excluded_resource_download_count']}；未引用路径构造/探测 {meta['constructed_unreferenced_probe_count']}；第三方来源 {meta['third_party_source_count']}。

{policy_lines}

## TRIAL 结果

- 样本 {meta['trial_count']}/10；科室首原子 {meta['department_coverage_count']} 个；keshi_ids 联集 {meta['api_department_id_coverage_count']} 个；满足 Owner 裁决后的至少两个官网科室门禁。
- 职称层：{json.dumps(meta['trial_title_level_counts'], ensure_ascii=False)}；照片成功 {meta['photo_success_count']}/10；照片资源失败 {meta['photo_failure_count']}；状态波动 {meta['status_flicker_count']}。
- 10 张均为 API `image` 字段实际引用的官网原始响应字节，未压缩、未转码。
- 总字节 {meta['total_bytes']:,}；最小 {meta['min_bytes']:,}；中位数 {meta['median_bytes']:,}；平均 {meta['average_bytes']:,}；最大 {meta['max_bytes']:,}。
- 大小分桶：{json.dumps(meta['size_buckets'], ensure_ascii=False)}；>5 MiB {meta['over_5mib_count']}；>20 MiB {meta['over_20mib_count']}。
- 联系表视觉状态：`{meta['visual_review_status']}`。

## 样本清单

{sample_lines}

## >5 MiB Owner 终审清单

{owner_lines}

## 正式资产保护

- 入口台账 JSON/CSV/XLSX、总底表 JSON/CSV/XLSX、更新报告、本院 298 个 Markdown 文件聚合快照与正式照片目录在 TRIAL 前后完全一致：{meta['protected_assets_before'] == meta['protected_assets_after']}。
- TRIAL 仅写 `work/` 独立工件；未回填底表、未刷新画像、未创建正式照片目录。

## 工件

- `{TRIAL_JSON_PATH.relative_to(ROOT).as_posix()}`
- `{TRIAL_CSV_PATH.relative_to(ROOT).as_posix()}`
- `{TRIAL_REPORT_PATH.relative_to(ROOT).as_posix()}`
- `{CONTACT_SHEET_PATH.relative_to(ROOT).as_posix()}`
- `{TRIAL_PHOTO_DIR.relative_to(ROOT).as_posix()}/`（10 张）

## 停止点

`TRIAL_READY_FOR_OWNER_AUDIT`。未取得 Owner 在关联 PR 的明确 `FULL_APPEND_AND_OBSIDIAN` 前，不写正式资产。
"""
    TRIAL_REPORT_PATH.write_text(report, encoding="utf-8")


def validate_manifest(payload: dict[str, Any]) -> None:
    if not TRIAL_CSV_PATH.is_file():
        raise RuntimeError("TRIAL manifest 缺失")
    with TRIAL_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    samples = payload.get("photo_samples", [])
    if len(rows) != len(samples):
        raise RuntimeError("TRIAL manifest 行数与 payload 不一致")
    for row, sample in zip(rows, samples, strict=True):
        for key in ("id", "name", "source_link", "photo_url", "filename", "sha256"):
            if clean_text(row.get(key)) != clean_text(sample.get(key)):
                raise RuntimeError(f"TRIAL manifest 字段不一致：{key} {sample.get('name')}")
        if int(row["bytes"]) != sample["bytes"]:
            raise RuntimeError(f"TRIAL manifest 字节数不一致：{sample.get('name')}")
        if json.loads(row["photo_attempts"]) != sample["photo_attempts"]:
            raise RuntimeError(f"TRIAL manifest 请求留痕不一致：{sample.get('name')}")


def validate_payload(
    payload: dict[str, Any], require_visual_pass: bool, check_artifacts: bool = True
) -> None:
    meta = payload.get("meta", {})
    errors: list[str] = []
    expected_ids = [str(item[0]) for item in SAMPLE_PLAN]
    if meta.get("issue") != ISSUE_NUMBER or meta.get("phase") != "TRIAL":
        errors.append("Issue/Phase 不一致")
    if meta.get("scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("范围不是 297 行")
    if meta.get("api_scope_count") != EXPECTED_SCOPE_COUNT:
        errors.append("API 固定范围不是 297 ID")
    if meta.get("group_count") != EXPECTED_GROUP_COUNT:
        errors.append("官网分组数不是 5")
    if meta.get("department_count") != EXPECTED_DEPARTMENT_COUNT:
        errors.append("官网科室数不是 31")
    if meta.get("relation_count") != EXPECTED_RELATION_COUNT:
        errors.append("医生-科室关系不是 317")
    if meta.get("api_object_occurrence_count") != EXPECTED_API_OBJECT_OCCURRENCES:
        errors.append("API 含 image 对象出现数不是 384")
    if meta.get("category_values") != [EXPECTED_CATEGORY]:
        errors.append("API category 不是唯一 55")
    if meta.get("trial_count") != EXPECTED_TRIAL_COUNT:
        errors.append("样本不是 10 位")
    if meta.get("department_coverage_count") != EXPECTED_TRIAL_COUNT:
        errors.append("科室首原子没有分散到 10 个")
    if int(meta.get("api_department_id_coverage_count", 0)) < 2:
        errors.append("未覆盖至少两个官网科室 ID")
    if meta.get("trial_title_level_counts") != {"正高": 5, "副高": 5}:
        errors.append("TRIAL 职称层不是正高 5 / 副高 5")
    valid_levels = meta.get("valid_candidate_title_level_counts", {})
    if valid_levels.get("其他", 0) != 0 or not valid_levels.get("正高") or not valid_levels.get("副高"):
        errors.append("有效照片候选职称层证据不一致")
    if any(
        int(meta.get(key, 0)) != 0
        for key in (
            "baseline_photo_filled_count",
            "photo_failure_count",
            "status_flicker_count",
            "over_20mib_count",
            "excluded_resource_download_count",
            "constructed_unreferenced_probe_count",
            "other_category_request_count",
            "third_party_source_count",
        )
    ):
        errors.append("TRIAL 存在既有照片、失败、波动、越界或排除资源下载")
    if meta.get("protected_assets_before") != meta.get("protected_assets_after"):
        errors.append("正式资产发生变化")
    if require_visual_pass and meta.get("visual_review_status") != VISUAL_PASS:
        errors.append("联系表尚未视觉通过")

    scope_records = payload.get("scope_records", [])
    if len(scope_records) != EXPECTED_SCOPE_COUNT:
        errors.append("scope_records 不是 297 行")
    if len({record.get("id") for record in scope_records}) != EXPECTED_SCOPE_COUNT:
        errors.append("scope_records ID 不唯一")
    samples = payload.get("photo_samples", [])
    if [item.get("id") for item in samples] != expected_ids:
        errors.append("固定样本 ID 顺序漂移")
    hashes: set[str] = set()
    for sample in samples:
        relative = Path(clean_text(sample.get("disk_path")))
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
            errors.append(f"照片字节数不一致：{path.name}")
        digest = hashlib.sha256(content).hexdigest()
        if digest != sample.get("sha256"):
            errors.append(f"照片 SHA-256 不一致：{path.name}")
        if digest in hashes:
            errors.append(f"照片 SHA-256 重复：{path.name}")
        hashes.add(digest)
        extension = common.magic_extension(content, sample.get("content_type"))
        if extension != sample.get("extension") or path.suffix.lower() != f".{extension}":
            errors.append(f"照片魔数/扩展名不一致：{path.name}")
        if common.image_dimensions(content) != (sample.get("width"), sample.get("height")):
            errors.append(f"照片尺寸不一致：{path.name}")
        if page_referenced_photo_url(sample.get("photo_url")) != sample.get("photo_url"):
            errors.append(f"照片 URL 越界：{path.name}")
        if comparable_host(sample.get("photo_final_url", "")) != OFFICIAL_HOST:
            errors.append(f"照片最终响应越出官网：{path.name}")
        if sample.get("api_category") != EXPECTED_CATEGORY:
            errors.append(f"样本 category 不是 55：{path.name}")

    if check_artifacts:
        for path in (TRIAL_JSON_PATH, TRIAL_REPORT_PATH, CONTACT_SHEET_PATH):
            if not path.is_file():
                errors.append(f"TRIAL 工件缺失：{path.name}")
        if TRIAL_PHOTO_DIR.is_dir():
            actual = [path for path in TRIAL_PHOTO_DIR.iterdir() if path.is_file()]
            if len(actual) != EXPECTED_TRIAL_COUNT:
                errors.append("TRIAL 照片目录不是 10 个文件")
        else:
            errors.append("TRIAL 照片目录缺失")
        try:
            validate_manifest(payload)
        except RuntimeError as exc:
            errors.append(str(exc))
    if errors:
        raise RuntimeError("TRIAL 验证失败：\n- " + "\n- ".join(errors))


def prepare_outputs() -> None:
    for path in (TRIAL_JSON_PATH, TRIAL_CSV_PATH, TRIAL_REPORT_PATH, CONTACT_SHEET_PATH):
        if path.exists():
            raise RuntimeError(f"TRIAL 工件已存在，拒绝覆盖：{path}")
    if TRIAL_PHOTO_DIR.exists():
        if any(TRIAL_PHOTO_DIR.iterdir()):
            raise RuntimeError(f"TRIAL 照片目录非空，拒绝覆盖：{TRIAL_PHOTO_DIR}")
    else:
        TRIAL_PHOTO_DIR.mkdir(parents=False)


def run_trial(run_date: str) -> dict[str, Any]:
    before = protected_snapshot()
    if before["profile_tree"]["file_count"] != EXPECTED_PROFILE_FILE_COUNT:
        raise RuntimeError("TRIAL 前本院画像聚合数量漂移")
    if before["formal_photo_tree"]["exists"]:
        raise RuntimeError("TRIAL 前正式照片目录已存在，需 Owner 裁决")
    rows = load_scope_rows()
    prepare_outputs()

    session = OfficialSession()
    directory_result = session.get(DIRECTORY_URL, referer=OFFICIAL_HOME)
    if directory_result.status != 200 or directory_result.content_type != "text/html":
        raise RuntimeError(
            f"医生目录响应异常：HTTP {directory_result.status} {directory_result.content_type}"
        )
    directory_html = directory_result.content.decode(directory_result.charset, errors="replace")
    source_evidence = directory_source_evidence(directory_html)

    api_observed_utc = utc_now()
    api_result = session.get(DIRECTORY_API, referer=DIRECTORY_URL)
    api_payload = decode_json_response(api_result, "医生目录 API")
    parsed = parse_directory_payload(api_payload)
    category_values = sorted(set(parsed["category_occurrences"]))
    if category_values != [EXPECTED_CATEGORY]:
        raise RuntimeError(f"目录 API 出现未授权 category：{category_values}")
    if len(parsed["groups"]) != EXPECTED_GROUP_COUNT:
        raise RuntimeError("目录 API 分组数漂移")
    if len(parsed["departments"]) != EXPECTED_DEPARTMENT_COUNT:
        raise RuntimeError("目录 API 科室数漂移")
    if len(parsed["relations"]) != EXPECTED_RELATION_COUNT:
        raise RuntimeError("目录 API 医生-科室关系数漂移")
    if len(parsed["category_occurrences"]) != EXPECTED_API_OBJECT_OCCURRENCES:
        raise RuntimeError("目录 API 含 image 对象出现数漂移")

    scope_records = reconcile_scope(rows, parsed["doctors"])
    trial_rows = select_trial_rows(rows, scope_records)
    samples: list[dict[str, Any]] = []
    status_flicker_count = 0
    photo_failure_count = 0
    for row in trial_rows:
        record = row["_scope_record"]
        photo_url = record["valid_photo_url"]
        photo, attempts = fetch_photo_with_retry(
            session, photo_url, clean_text(row.get("来源链接"))
        )
        statuses = {item.get("status") for item in attempts if item.get("status") is not None}
        had_error = any(item.get("error") for item in attempts)
        if len(statuses) > 1 or (had_error and photo.status == 200):
            status_flicker_count += 1
            raise RuntimeError(
                "STATUS_FLICKER_REQUIRES_ISSUE_COMMENT_AND_AGGREGATION: "
                f"{photo_url} attempts={attempts}"
            )
        if photo.status != 200:
            photo_failure_count += 1
            raise RuntimeError(f"照片资源两次请求仍失败：{photo_url} attempts={attempts}")
        if comparable_host(photo.final_url) != OFFICIAL_HOST:
            raise RuntimeError(f"照片重定向越出官网：{photo_url} -> {photo.final_url}")
        extension = common.magic_extension(photo.content, photo.content_type)
        if not extension:
            raise RuntimeError(
                f"照片响应格式异常：{photo_url} HTTP {photo.status} {photo.content_type}"
            )
        if len(photo.content) > MAX_PHOTO_BYTES:
            raise RuntimeError(f"照片超过 20 MiB 熔断：{photo_url} {len(photo.content)}")
        width, height = common.image_dimensions(photo.content)
        filename, photo_path = allocate_trial_photo(row, extension, photo.content)
        photo_path.write_bytes(photo.content)
        samples.append(
            {
                "id": source_id(row.get("来源链接")),
                "name": clean_text(row.get("姓名")),
                "department": atomic_department(row),
                "api_keshi_ids": record["api_keshi_ids"],
                "api_keshi": record["api_keshi"],
                "primary_title": primary_title(row.get("职称身份原文")),
                "title_level": title_level(row.get("职称身份原文")),
                "source_link": clean_text(row.get("来源链接")),
                "api_url": DIRECTORY_API,
                "api_category": record["api_category"],
                "api_image_field_value": record["api_image_field_value"],
                "photo_url": photo_url,
                "photo_status": photo.status,
                "photo_final_url": photo.final_url,
                "photo_redirects": list(photo.redirects),
                "photo_attempts": attempts,
                "content_type": photo.content_type,
                "extension": extension,
                "filename": filename,
                "disk_path": photo_path.relative_to(ROOT).as_posix(),
                "bytes": len(photo.content),
                "sha256": hashlib.sha256(photo.content).hexdigest(),
                "width": width,
                "height": height,
            }
        )

    if len(samples) != EXPECTED_TRIAL_COUNT:
        raise RuntimeError(f"TRIAL 未形成 10 张样本：{len(samples)}")
    values = sorted(int(item["bytes"]) for item in samples)
    total_bytes = sum(values)
    median_bytes = (values[4] + values[5]) // 2
    average_bytes = total_bytes // len(values)
    valid_records = [record for record in scope_records if record["valid_photo_url"]]
    rows_by_id = {source_id(row.get("来源链接")): row for row in rows}
    valid_level_counts = Counter(
        title_level(rows_by_id[record["id"]].get("职称身份原文"))
        for record in valid_records
    )
    for level in ("正高", "副高", "其他"):
        valid_level_counts.setdefault(level, 0)
    image_signal_counts = Counter(record["image_signal"] for record in scope_records)
    api_department_ids = {
        item
        for sample in samples
        for item in sample["api_keshi_ids"].split(",")
        if clean_text(item)
    }
    after = protected_snapshot()
    payload = {
        "meta": {
            "issue": ISSUE_NUMBER,
            "branch": BRANCH,
            "phase": "TRIAL",
            "owner_ruling": "OPTION_A_CATEGORY_55_ONLY_DEPARTMENT_COVERAGE",
            "hospital": HOSPITAL,
            "official_home": OFFICIAL_HOME,
            "doctor_directory": DIRECTORY_URL,
            "directory_api": DIRECTORY_API,
            "run_date": run_date,
            "scope_count": len(rows),
            "unique_source_count": len({source_id(row.get("来源链接")) for row in rows}),
            "baseline_photo_filled_count": 0,
            "group_count": len(parsed["groups"]),
            "department_count": len(parsed["departments"]),
            "relation_count": len(parsed["relations"]),
            "api_scope_count": len(parsed["doctors"]),
            "api_banner_unique_id_count": len(parsed["banner_unique_ids"]),
            "api_object_occurrence_count": len(parsed["category_occurrences"]),
            "category_values": category_values,
            "other_category_request_count": 0,
            "image_signal_counts": dict(sorted(image_signal_counts.items())),
            "valid_photo_candidate_count": len(valid_records),
            "valid_candidate_title_level_counts": {
                level: valid_level_counts[level] for level in ("正高", "副高", "其他")
            },
            "trial_count": len(samples),
            "department_coverage_count": len({item["department"] for item in samples}),
            "api_department_id_coverage_count": len(api_department_ids),
            "api_department_ids": sorted(api_department_ids, key=int),
            "trial_title_level_counts": dict(Counter(item["title_level"] for item in samples)),
            "photo_success_count": len(samples),
            "photo_failure_count": photo_failure_count,
            "status_flicker_count": status_flicker_count,
            "over_5mib_count": sum(item["bytes"] > OWNER_REPORT_BYTES for item in samples),
            "over_20mib_count": sum(item["bytes"] > MAX_PHOTO_BYTES for item in samples),
            "total_bytes": total_bytes,
            "min_bytes": values[0],
            "median_bytes": median_bytes,
            "average_bytes": average_bytes,
            "max_bytes": values[-1],
            "size_buckets": size_buckets(samples),
            "estimated_valid_scope_bytes": average_bytes * len(valid_records),
            "estimated_valid_scope_mib": average_bytes * len(valid_records) / (1024 * 1024),
            "directory_status": directory_result.status,
            "directory_content_type": directory_result.content_type,
            "directory_source_evidence": source_evidence,
            "cookie_names": session.cookie_names,
            "incomplete_read_retry_count": session.incomplete_read_retry_count,
            "excluded_resource_download_count": 0,
            "constructed_unreferenced_probe_count": 0,
            "third_party_source_count": 0,
            "visual_review_status": "PENDING_MANUAL_CONTACT_SHEET_REVIEW",
            "protected_assets_before": before,
            "protected_assets_after": after,
        },
        "api_trace": {
            "url": DIRECTORY_API,
            "method": "GET",
            "query": {"category": EXPECTED_CATEGORY},
            "status": api_result.status,
            "content_type": api_result.content_type,
            "final_url": api_result.final_url,
            "redirects": list(api_result.redirects),
            "bytes": len(api_result.content),
            "sha256": hashlib.sha256(api_result.content).hexdigest(),
            "observed_utc": api_observed_utc,
        },
        "exclusion_policy": list(EXCLUSION_POLICY),
        "scope_records": scope_records,
        "photo_samples": samples,
    }
    validate_payload(payload, require_visual_pass=False, check_artifacts=False)
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_manifest(samples)
    build_contact_sheet(samples)
    write_report(payload)
    validate_payload(payload, require_visual_pass=False, check_artifacts=True)
    return payload


def load_trial_payload() -> dict[str, Any]:
    if not TRIAL_JSON_PATH.is_file():
        raise RuntimeError(f"TRIAL payload 不存在：{TRIAL_JSON_PATH}")
    payload = json.loads(TRIAL_JSON_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("TRIAL payload 顶层不是对象")
    return payload


def mark_visual_pass() -> dict[str, Any]:
    payload = load_trial_payload()
    if not CONTACT_SHEET_PATH.is_file():
        raise RuntimeError("联系表不存在，不能标记视觉通过")
    payload["meta"]["visual_review_status"] = VISUAL_PASS
    validate_payload(payload, require_visual_pass=True, check_artifacts=True)
    TRIAL_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Issue #75 广州医科大学附属口腔医院照片补录 TRIAL"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trial-only", action="store_true", help="执行固定 10 人 TRIAL")
    mode.add_argument("--mark-visual-pass", action="store_true", help="人工查看联系表后标记通过")
    mode.add_argument("--validate", action="store_true", help="验证现有 TRIAL 工件")
    parser.add_argument("--run-date", default=str(date.today()), help="采集日期 YYYY-MM-DD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.trial_only:
        payload = run_trial(args.run_date)
        print(
            "TRIAL_COMPLETE_PENDING_VISUAL_REVIEW "
            f"samples={payload['meta']['trial_count']} photos={payload['meta']['photo_success_count']}"
        )
        return
    if args.mark_visual_pass:
        payload = mark_visual_pass()
        print(
            "TRIAL_VISUAL_REVIEW_PASSED "
            f"status={payload['meta']['visual_review_status']}"
        )
        return
    payload = load_trial_payload()
    validate_payload(payload, require_visual_pass=True, check_artifacts=True)
    print(
        "TRIAL_VALIDATED "
        f"samples={payload['meta']['trial_count']} photos={payload['meta']['photo_success_count']}"
    )


if __name__ == "__main__":
    main()
