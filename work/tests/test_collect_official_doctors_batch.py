from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

from collect_official_doctors_batch import (  # noqa: E402
    HospitalTarget,
    build_master_payload,
    build_hospital_batches,
    classify_generic_record,
    clean_generic_department,
    covered_department_names,
    collect_gyfyyy,
    collect_gy3y,
    collect_gzbrain,
    collect_gzszyy,
    collect_gzsys,
    collect_gykqyy,
    collect_generic,
    confirmed_a_targets,
    dedicated_adapter_for,
    discover_gdskin_excluded_links,
    discover_gdskin_postback_documents,
    discover_generic_detail_links,
    discover_gy3y_directory,
    discover_gzbrain_list_pages,
    discover_gzszyy_care_sites,
    discover_gzszyy_department_filters,
    discover_gzszyy_department_pages,
    discover_gzszyy_unfiltered_pages,
    discover_gzsys_default_pages,
    effective_entry_urls,
    expand_gdzy5413_full_detail_items,
    extract_clean_highlights,
    fetch_json,
    find_node,
    generic_record_quality,
    generic_detail_identity,
    gdzy5413_detail_id,
    gdzy5413_entry_kind,
    gdzy5413_ksdoctor_detail_id,
    gdzy5413_rows_same_identity,
    gyfyyy_detail_id,
    gy3y_detail_id,
    gzbrain_detail_id,
    gzszyy_detail_id,
    gzsys_detail_id,
    parse_gzbrain_detail,
    parse_gzbrain_list_page,
    parse_gzszyy_department_page,
    parse_gzszyy_detail,
    parse_gzsys_detail,
    parse_gzsys_list_page,
    parse_gyfyyy_detail,
    strip_gyfyyy_schedule_text,
    strip_gzsys_schedule_text,
    looks_like_person_name,
    matches_generic_directory_detail_url,
    merge_rows_for_master,
    merge_gdzy5413_identity_rows,
    merge_gzszyy_identity_rows,
    merge_gyfyyy_identity_rows,
    ny5y_detail_id,
    ny5y_entry_kind,
    parse_generic_detail,
    parse_gdskin_detail,
    parse_gdzy5413_detail,
    parse_gdzy5413_ksdoctor_detail,
    parse_ny5y_detail,
    round_robin_generic_items,
    select_gyfyyy_trial_doctors,
    select_gzbrain_trial_doctors,
    select_gzszyy_trial_doctors,
    select_gzsys_trial_doctors,
    select_gykqyy_trial_doctors,
    sync_profile_flags,
    validate_gykqyy_full_append,
    validate_gyfyyy_full_append,
    validate_gy3y_full_append,
    validate_gzbrain_full_append,
    validate_gzszyy_full_append,
    validate_gzsys_full_append,
    validate_gzsys_trial,
    select_gdzy5413_trial2_items,
    validate_gdskin_full_append,
    validate_gdzy5413_full_append,
    validate_gdzy5413_trial2,
    validate_ny5y_full_append,
    write_report,
)


class GenericDetailNoiseFilteringTests(unittest.TestCase):
    def test_breadcrumb_is_used_for_department_but_removed_from_profile(self) -> None:
        html = """
        <html>
          <head><title>丘惠娟 - 临床专家</title></head>
          <body>
            <main class="content">
              <nav role="navigation" class="breadcrumb">
                <h2 class="visually-hidden">面包屑</h2>
                <a href="/">首页</a> /
                <a href="/departments">临床科室</a> /
                <a href="/medicine">内科系列</a> /
                <a href="/tcm">中医科</a> /
                <span>临床专家</span>
              </nav>
              <article class="doctor-detail">
                <h1>丘惠娟</h1>
                <div>职称：副主任医师</div>
                <div>专长：中西医结合治疗肿瘤。</div>
                <div>个人简介：从事肿瘤临床工作近二十年。</div>
              </article>
            </main>
          </body>
        </html>
        """

        detail = parse_generic_detail(html, {})

        self.assertEqual(detail["name"], "丘惠娟")
        self.assertEqual(detail["department"], "中医科")
        self.assertIn("中西医结合治疗肿瘤", detail["specialty"])
        self.assertIn("从事肿瘤临床工作", detail["profile_text"])
        self.assertNotIn("面包屑", detail["profile_text"])
        self.assertNotIn("首页", detail["profile_text"])
        self.assertNotIn("临床科室", detail["profile_text"])

    def test_page_chrome_and_controls_are_removed_from_profile(self) -> None:
        html = """
        <html>
          <head><title>陈医生</title></head>
          <body>
            <header class="site-header">医院首页 科室导航 新闻中心</header>
            <main>
              <article class="expert-detail">
                <h1>陈医生</h1>
                <p>科室：呼吸内科</p>
                <p>职称：主任医师</p>
                <p>擅长：肺癌的规范化诊疗。</p>
                <p>个人简介：长期从事呼吸系统疾病诊疗。</p>
                <button>加载更多</button>
                <aside>相关医生 热门新闻</aside>
              </article>
            </main>
            <footer>联系我们 网站地图</footer>
          </body>
        </html>
        """

        detail = parse_generic_detail(html, {})

        self.assertIn("长期从事呼吸系统疾病诊疗", detail["profile_text"])
        for noise in ["医院首页", "科室导航", "新闻中心", "加载更多", "相关医生", "联系我们", "网站地图"]:
            self.assertNotIn(noise, detail["profile_text"])

    def test_unmarked_breadcrumb_prefix_is_removed_defensively(self) -> None:
        html = """
        <html>
          <head><title>周医生</title></head>
          <body>
            <main class="content">
              <div>当前位置：首页 &gt; 医疗服务 &gt; 专家介绍 &gt; 周医生 职称：主治医师</div>
              <div>擅长：糖尿病综合管理。</div>
              <div>个人简介：长期从事内分泌疾病诊疗。</div>
            </main>
          </body>
        </html>
        """

        detail = parse_generic_detail(html, {})

        self.assertIn("长期从事内分泌疾病诊疗", detail["profile_text"])
        self.assertNotIn("当前位置", detail["profile_text"])
        self.assertNotIn("医疗服务", detail["profile_text"])
        self.assertNotIn("专家介绍", detail["profile_text"])

    def test_smukq_navigation_block_is_removed_before_highlight_extraction(self) -> None:
        html = """
        <main class="content">
          <h1>谢跃强</h1>
          <div>你当前所在的位置： 海珠广场院区/ 口腔正畸科 /详细
          海珠广场院区 口腔种植修复科 牙体牙髓病科一室 口腔正畸科
          专家信息 谢跃强 主治医师，正畸学硕士 科室：口腔正畸科
          中华口腔正畸专业委员会会员，隐形病例荣获全国中青年正畸医师病例大赛50强。</div>
        </main>
        """

        detail = parse_generic_detail(html, {})
        highlights = extract_clean_highlights(detail["profile_text"])

        self.assertEqual(detail["highlight_navigation_polluted"], "yes")
        self.assertNotIn("你当前所在的位置", detail["profile_text"])
        self.assertNotIn("口腔种植修复科", detail["profile_text"])
        self.assertIn("荣获全国中青年正畸医师病例大赛50强", highlights)

    def test_highlight_is_empty_when_navigation_removal_leaves_no_evidence(self) -> None:
        raw = (
            "你当前所在的位置：海珠广场院区/儿童口腔科/详细 "
            "海珠广场院区 口腔种植修复科 儿童口腔科 "
            "医师信息 陈焱 主治医师 科室：儿童口腔科"
        )

        self.assertEqual(extract_clean_highlights(raw), "")


class GykqyyPublicDoctorApiTests(unittest.TestCase):
    ENTRY_URL = "https://www.gykqyy.com/list.html?category=55"

    @staticmethod
    def directory_payload() -> dict[str, object]:
        departments = []
        doctor_id = 1
        for department_id, department_name in enumerate(
            ["荔湾院区牙体牙髓科", "越秀院区牙周病科", "全科口腔中心", "麻醉手术中心"],
            start=10,
        ):
            doctors = []
            for _ in range(3):
                doctors.append(
                    {
                        "id": doctor_id,
                        "title": f"医生{doctor_id}",
                        "intro": f"擅长{department_name}常见疾病。",
                        "keshi": department_name,
                        "zhicheng": "主任医师",
                        "weigh": 100 - doctor_id,
                    }
                )
                doctor_id += 1
            departments.append({"id": department_id, "name": department_name, "child": doctors})
        return {
            "code": 1,
            "msg": "ok",
            "data": {
                "banner": [item for department in departments for item in department["child"]],
                "list": [{"id": 1, "name": "官网院区", "child": departments}],
            },
        }

    def test_adapter_scope_is_exact(self) -> None:
        self.assertEqual(dedicated_adapter_for(self.ENTRY_URL), "gykqyy_public_doctor_api")
        self.assertEqual(dedicated_adapter_for(f"{self.ENTRY_URL}&id=195"), "gykqyy_public_doctor_api")
        self.assertEqual(dedicated_adapter_for("https://www.gykqyy.com/list.html?category=56"), "")
        self.assertEqual(dedicated_adapter_for("https://api.gykqyy.com/list.html?category=55"), "")

    def test_trial_selection_spreads_across_departments(self) -> None:
        doctors = [
            {"id": str(index), "departments": [f"科室{(index - 1) // 4}"]}
            for index in range(1, 13)
        ]
        selected = select_gykqyy_trial_doctors(doctors, 10)

        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(len({item["departments"][0] for item in selected}), 3)

    def test_collect_uses_only_page_declared_public_json_apis(self) -> None:
        target = HospitalTarget(
            city="广州市",
            hospital="广州医科大学附属口腔医院",
            homepage="https://www.gykqyy.com/",
            entry_url=self.ENTRY_URL,
            difficulty="A-优先自动采集",
            review="确认可采集",
            adapter_id="gykqyy_public_doctor_api",
        )
        entry_html = """
        <script>
        axios.get("https://www.gykqyy.com/api/article/getZhuanjiaList");
        axios.get("https://www.gykqyy.com/api/article/getArticleDetail");
        </script>
        """
        directory_payload = self.directory_payload()

        def fake_fetch_json(_session, url, params=None):
            if url.endswith("getZhuanjiaList"):
                return 200, directory_payload, ""
            doctor_id = str((params or {})["article_id"])
            return (
                200,
                {
                    "code": 1,
                    "data": {
                        "detail": {
                            "id": int(doctor_id),
                            "title": f"医生{doctor_id}",
                            "intro": f"擅长科室{doctor_id}常见疾病。",
                            "content": f"<p>医生{doctor_id}，主任医师。擅长疑难口腔疾病。</p>",
                        }
                    },
                },
                "",
            )

        with (
            patch("collect_official_doctors_batch.create_official_session", return_value=__import__("requests").Session()),
            patch("collect_official_doctors_batch.fetch", return_value=(200, entry_html, "")),
            patch("collect_official_doctors_batch.fetch_json", side_effect=fake_fetch_json),
            patch("collect_official_doctors_batch.collect_existing_profile_links", return_value=set()),
        ):
            payload = collect_gykqyy(target, "2026-08-13", max_doctors=10)

        self.assertEqual(len(payload["rows"]), 10)
        self.assertEqual(payload["meta"]["census_unique_detail_count"], 12)
        self.assertEqual(payload["meta"]["census_department_count"], 4)
        self.assertEqual(payload["meta"]["pagination_count"], 1)
        self.assertGreaterEqual(len({row["科室_分类页"] for row in payload["rows"]}), 3)
        self.assertTrue(all("详情接口" in row["采集方式"] for row in payload["rows"]))

    def test_fetch_json_retries_transient_server_error(self) -> None:
        class FakeResponse:
            def __init__(self, status_code, payload=None):
                self.status_code = status_code
                self.headers = {"Content-Type": "application/json"}
                self._payload = payload or {}

            def json(self):
                return self._payload

        session = Mock()
        session.get.side_effect = [
            FakeResponse(502),
            FakeResponse(200, {"code": 1, "data": {}}),
        ]
        with patch("collect_official_doctors_batch.time.sleep"):
            status, payload, error = fetch_json(session, "https://www.gykqyy.com/api/test")

        self.assertEqual(status, 200)
        self.assertEqual(payload["code"], 1)
        self.assertEqual(error, "")
        self.assertEqual(session.get.call_count, 2)

    def test_full_gate_keeps_four_same_name_rows_and_zero_blank_names(self) -> None:
        names = [f"医生{index}" for index in range(1, 294)] + ["方颖", "方颖", "赵稚宁", "赵稚宁"]
        rows = []
        reconciliation = []
        for index, name in enumerate(names, start=1):
            warning = "同名待甄别" if name in {"方颖", "赵稚宁"} else ""
            source = f"https://www.gykqyy.com/list.html?category=55&id={index}"
            rows.append({"姓名": name, "来源链接": source, "异常提示": warning})
            reconciliation.append({"detail_id": str(index), "name": name, "source_link": source})
        payload = {
            "meta": {
                "candidate_membership_count": 317,
                "census_unique_detail_count": 297,
                "census_named_detail_count": 297,
                "census_blank_name_detail_count": 0,
                "detail_error_count": 0,
                "gykqyy_final_row_count": 297,
                "gykqyy_same_name_separate_row_count": 4,
                "census_same_name_groups": {"方颖": ["128", "307"], "赵稚宁": ["29", "323"]},
            },
            "rows": rows,
            "excluded_candidates": [],
            "gykqyy_identity_reconciliation": reconciliation,
        }

        validate_gykqyy_full_append(payload)
        payload["meta"]["detail_error_count"] = 1
        with self.assertRaisesRegex(RuntimeError, "详情接口失败应为 0"):
            validate_gykqyy_full_append(payload)

    def test_profile_flags_are_synchronized_from_canonical_source_links(self) -> None:
        rows = [
            {"来源链接": "https://www.gykqyy.com/list.html?category=55&id=128", "已建画像": "否"},
            {"来源链接": "https://www.gykqyy.com/list.html?category=55&id=307", "已建画像": "是"},
        ]

        sync_profile_flags(rows, {"https://www.gykqyy.com/list.html?category=55&id=128"})

        self.assertEqual([row["已建画像"] for row in rows], ["是", "否"])

    def test_master_rebuild_preserves_last_batch_metadata(self) -> None:
        existing_rows = [
            {
                "医院": "广州医科大学附属口腔医院",
                "姓名": "方颖",
                "来源链接": "https://www.gykqyy.com/list.html?category=55&id=128",
                "已建画像": "否",
            }
        ]
        previous_meta = {
            "hospital": "珠三角三甲医院医生画像总表",
            "raw_card_rows": 317,
            "category_error_count": 0,
            "detail_error_count": 0,
            "current_batch_hospital": "广州医科大学附属口腔医院",
            "current_batch_rows": 297,
            "new_rows_added": 297,
            "duplicate_rows_skipped": 0,
            "existing_rows_refreshed": 0,
            "existing_duplicate_rows": 0,
        }

        with (
            patch(
                "collect_official_doctors_batch.load_existing_rows_for_master",
                return_value=(existing_rows, "test.xlsx", True),
            ),
            patch(
                "collect_official_doctors_batch.collect_existing_profile_links",
                return_value={"https://www.gykqyy.com/list.html?category=55&id=128"},
            ),
        ):
            payload = build_master_payload(
                "2026-08-13",
                batch_meta_override=previous_meta,
            )

        self.assertEqual(payload["meta"]["current_batch_hospital"], previous_meta["current_batch_hospital"])
        self.assertEqual(payload["meta"]["raw_card_rows"], 317)
        self.assertEqual(payload["meta"]["current_batch_rows"], 297)
        self.assertEqual(payload["meta"]["new_rows_added"], 297)
        self.assertEqual(payload["rows"][0]["已建画像"], "是")


class GyfyyyStaticDepartmentTreeTests(unittest.TestCase):
    ENTRY_URL = "https://www.gyfyyy.cn/cn/ks/"

    def test_adapter_and_detail_scope_are_exact(self) -> None:
        self.assertEqual(dedicated_adapter_for(self.ENTRY_URL), "gyfyyy_static_department_tree")
        for invalid in [
            "https://www.gyfyyy.cn/cn/ks",
            "https://www.gyfyyy.cn/cn/ks/?page=1",
            "https://api.gyfyyy.cn/cn/ks/",
            "https://www.gyfyyy.cn/cn/ylfw/czcx/",
        ]:
            self.assertEqual(dedicated_adapter_for(invalid), "")
        detail = "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_101.html"
        self.assertEqual(gyfyyy_detail_id(detail, "https://www.gyfyyy.cn/cn/ks/nk/hxnk/"), "101")
        self.assertEqual(gyfyyy_detail_id(detail, "https://www.gyfyyy.cn/cn/ks/nk/btfyk/"), "")
        self.assertEqual(gyfyyy_detail_id("https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_101.html?x=1"), "")

    def test_detail_parser_is_limited_to_doctor_sections(self) -> None:
        html = """
        <section class="doctorcard">
          <strong>陈如冲</strong><b></b><b>变态反应科副主任 主任医师</b>
          <p>擅长呼吸系统过敏性疾病。</p>
        </section>
        <section class="doctorintro"><div class="title">医生简介</div><p>从事临床工作二十年。</p></section>
        <section class="patientcases"><p>患者评价和案例不得采集。</p></section>
        <section class="news"><p>医院新闻不得采集。</p></section>
        """

        detail = parse_gyfyyy_detail(html, {})

        self.assertEqual(detail["name"], "陈如冲")
        self.assertIn("主任医师", detail["title"])
        self.assertEqual(detail["specialty"], "呼吸系统过敏性疾病。")
        self.assertEqual(detail["profile_text"], "从事临床工作二十年。")
        self.assertNotIn("患者评价", detail["profile_text"])
        self.assertNotIn("医院新闻", detail["profile_text"])

    def test_repeated_specialty_prefixes_are_fully_removed(self) -> None:
        html = """
        <section class="doctorcard">
          <strong>测试医生</strong><b>主任医师</b><p>擅长：擅长 肺癌规范化诊疗。</p>
        </section>
        <section class="doctorintro"><p>长期从事临床工作。</p></section>
        """
        detail = parse_gyfyyy_detail(html, {})
        self.assertEqual(detail["specialty"], "肺癌规范化诊疗。")

    def test_schedule_blocks_are_removed_without_dropping_clinical_profile(self) -> None:
        html = """
        <section class="doctorcard">
          <strong>测试医生</strong><b>主任医师</b><p>擅长肺癌诊疗。</p>
        </section>
        <section class="doctorintro">
          <p>开诊院区: 沿江院区 开诊时间：周一上午 擅长：肺癌规范化诊疗。</p>
          <p>简介：长期从事临床工作。专家门诊每周二上午、特需门诊每周四晚上。</p>
        </section>
        """

        detail = parse_gyfyyy_detail(html, {})

        self.assertEqual(detail["profile_text"], "擅长：肺癌规范化诊疗。 简介：长期从事临床工作。")
        self.assertNotRegex(detail["profile_text"], r"开诊|出诊|每?周[一二三四五六日天]|上午|晚上")
        self.assertEqual(strip_gyfyyy_schedule_text("门诊出诊时间：总院周一下午。"), "")
        self.assertEqual(
            strip_gyfyyy_schedule_text(
                "开诊时间：海印院区 周三下午14：30-19：00 泌尿外科主任，医学博士。"
            ),
            "泌尿外科主任，医学博士。",
        )
        self.assertEqual(strip_gyfyyy_schedule_text("每周一下午出诊"), "")
        self.assertEqual(
            strip_gyfyyy_schedule_text("教授，硕士生导师。 胸部影像诊断门诊（沿江综合楼）：周一、周四全天"),
            "教授，硕士生导师。",
        )
        self.assertEqual(strip_gyfyyy_schedule_text("擅长脊柱外科技术。 周三下午：14:30--17:30"), "擅长脊柱外科技术。")

    def test_trial_selection_spreads_across_departments(self) -> None:
        doctors = [
            {"id": str(index), "departments": [f"科室{(index - 1) // 4}"]}
            for index in range(1, 13)
        ]
        selected = select_gyfyyy_trial_doctors(doctors, 10)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(len({item["departments"][0] for item in selected}), 3)

    def test_abnormal_rows_do_not_receive_priority_or_disease_tags(self) -> None:
        target = HospitalTarget(
            city="广州市",
            hospital="广州医科大学附属第一医院",
            homepage="https://www.gyfyyy.cn/",
            entry_url=self.ENTRY_URL,
            difficulty="A-优先自动采集",
            review="确认可采集",
            adapter_id="gyfyyy_static_department_tree",
        )
        pages = {
            self.ENTRY_URL: '<a href="/cn/ks/nk/hxnk/">呼吸与危重症医学科</a>',
            "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctorList.html": (
                '<section class="doctors team"><li><a href="doctor_1.html">肺癌科室介绍 主任医师</a></li></section>'
            ),
            "https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_1.html": (
                '<section class="doctorcard"><strong>肺癌科室介绍</strong><b>主任医师</b>'
                '<p>擅长肺癌。</p></section><section class="doctorintro"><p>疑难肺癌诊疗。</p></section>'
            ),
        }

        def fake_fetch(_session, url, retries=3):
            return 200, pages[url], ""

        with (
            patch("collect_official_doctors_batch.create_official_session", return_value=object()),
            patch("collect_official_doctors_batch.fetch", side_effect=fake_fetch),
            patch("collect_official_doctors_batch.collect_existing_profile_links", return_value=set()),
        ):
            row = collect_gyfyyy(target, "2026-08-13", max_doctors=1)["rows"][0]

        self.assertIn("非医生页面或姓名异常", row["异常提示"])
        self.assertEqual(row["重点优先级"], "普通")
        self.assertEqual(row["重点关注范围"], "")
        self.assertEqual(row["重点疾病标签"], "")

    def test_collect_censuses_tree_merges_ids_and_excludes_nursing_only(self) -> None:
        departments = [
            ("呼吸与危重症医学科", "/cn/ks/nk/hxnk/", [1, 2, 101]),
            ("变态反应科", "/cn/ks/nk/btfyk/", [3, 4, 101]),
            ("心血管内科", "/cn/ks/nk/xxgnk/", [5, 6, 7]),
            ("内科门诊", "/cn/ks/nk/ptnk/", [8, 9, 13]),
        ]
        entry_html = "".join(f'<a href="{path}">{name}</a>' for name, path, _ids in departments)
        pages = {self.ENTRY_URL: entry_html}
        for name, path, ids in departments:
            team_url = f"https://www.gyfyyy.cn{path}doctorList.html"
            cards = []
            for doctor_id in ids:
                identity = "主管护师" if doctor_id == 13 else "主任医师"
                cards.append(f'<li><a href="doctor_{doctor_id}.html">医生{doctor_id} {identity}</a></li>')
                if doctor_id != 13:
                    pages[f"https://www.gyfyyy.cn{path}doctor_{doctor_id}.html"] = f"""
                    <section class="doctorcard"><strong>医生{doctor_id}</strong><b>{identity}</b>
                    <p>擅长{name}常见疾病。</p></section>
                    <section class="doctorintro"><p>长期从事{name}临床诊疗。</p></section>
                    <section class="patientcases"><p>患者评价不得采集。</p></section>
                    """
            pages[team_url] = '<section class="doctors team"><ul>' + "".join(cards) + "</ul></section>"

        def fake_fetch(_session, url, retries=3):
            html = pages.get(url)
            return (200, html, "") if html is not None else (None, "", "fixture missing")

        target = HospitalTarget(
            city="广州市",
            hospital="广州医科大学附属第一医院",
            homepage="https://www.gyfyyy.cn/",
            entry_url=self.ENTRY_URL,
            difficulty="A-优先自动采集",
            review="确认可采集",
            adapter_id="gyfyyy_static_department_tree",
        )
        with (
            patch("collect_official_doctors_batch.create_official_session", return_value=object()),
            patch("collect_official_doctors_batch.fetch", side_effect=fake_fetch),
            patch("collect_official_doctors_batch.collect_existing_profile_links", return_value=set()),
        ):
            payload = collect_gyfyyy(target, "2026-08-13", max_doctors=10)

        self.assertEqual(payload["meta"]["category_count"], 4)
        self.assertEqual(payload["meta"]["candidate_membership_count"], 12)
        self.assertEqual(payload["meta"]["census_unique_detail_count"], 11)
        self.assertEqual(payload["meta"]["cross_entry_duplicate_count"], 1)
        self.assertEqual(payload["meta"]["gyfyyy_cross_department_identity_count"], 1)
        self.assertEqual(len(payload["rows"]), 10)
        self.assertGreaterEqual(len({row["科室_分类页"] for row in payload["rows"]}), 3)
        merged = next(row for row in payload["rows"] if row["姓名"] == "医生101")
        self.assertIn("呼吸与危重症医学科", merged["科室_分类页"])
        self.assertIn("变态反应科", merged["科室_分类页"])
        self.assertNotIn("患者评价", merged["详情正文摘录"])
        self.assertEqual(len(payload["excluded_candidates"]), 1)
        self.assertIn("护理身份", payload["excluded_candidates"][0]["reason"])
        self.assertEqual(payload["meta"]["detail_error_count"], 0)

        covered_departments = covered_department_names(
            [
                {"科室_分类页": "呼吸与危重症医学科、变态反应科", "异常提示": ""},
                {"科室_分类页": "心血管内科", "异常提示": ""},
                {"科室_分类页": "内科门诊", "异常提示": ""},
            ]
        )
        self.assertEqual(
            set(covered_departments),
            {"呼吸与危重症医学科", "变态反应科", "心血管内科", "内科门诊"},
        )

    def test_full_gate_requires_complete_authorized_reconciliation(self) -> None:
        rows = []
        detail_reconciliation = []
        identity_reconciliation = []
        excluded = []
        nursing_ids = {str(value) for value in range(700, 709)}
        cross_ids = {"101", "549", "607", "618"}
        for doctor_id in range(1, 617):
            distinct_index = (doctor_id - 1) // 2 + 1
            name = f"同名{distinct_index}" if doctor_id <= 8 else f"医生{doctor_id}"
            warning = "同名待甄别" if doctor_id <= 8 else ""
            rows.append(
                {
                    "姓名": name,
                    "来源链接": f"https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_{doctor_id}.html",
                    "擅长诊疗方向摘录": "呼吸系统疾病。",
                    "异常提示": warning,
                    "重点关注范围": "",
                    "重点疾病标签": "",
                    "重点优先级": "普通",
                }
            )
            merged_id = doctor_id + 608 if 9 <= doctor_id <= 29 else None
            detail_ids = [str(doctor_id)] + ([str(merged_id)] if merged_id else [])
            identity_reconciliation.append(
                {
                    "name": name,
                    "detail_ids": detail_ids,
                    "primary_source_link": rows[-1]["来源链接"],
                    "relation_count": len(detail_ids),
                }
            )
        for doctor_id in range(1, 638):
            detail_reconciliation.append(
                {
                    "detail_id": str(doctor_id),
                    "relation_count": 2 if str(doctor_id) in cross_ids else 1,
                }
            )
        for doctor_id in sorted(nursing_ids):
            excluded.append(
                {
                    "source_link": f"https://www.gyfyyy.cn/cn/ks/wk/bnwk/doctor_{doctor_id}.html",
                    "reason": "官网团队卡片仅标注护理身份，排除医生画像采集范围",
                }
            )
        payload = {
            "meta": {
                "category_count": 59,
                "candidate_membership_count": 650,
                "census_unique_detail_count": 646,
                "cross_entry_duplicate_count": 4,
                "gyfyyy_cross_department_identity_count": 4,
                "excluded_non_doctor_count": 9,
                "category_error_count": 0,
                "detail_error_count": 0,
                "unique_doctor_count": 616,
                "gyfyyy_final_identity_count": 616,
                "gyfyyy_same_identity_merge_group_count": 21,
                "gyfyyy_distinct_same_name_group_count": 4,
                "gyfyyy_distinct_same_name_row_count": 8,
                "census_same_name_group_count": 25,
            },
            "rows": rows,
            "excluded_candidates": excluded,
            "gyfyyy_detail_reconciliation": detail_reconciliation,
            "gyfyyy_identity_reconciliation": identity_reconciliation,
        }
        validate_gyfyyy_full_append(payload)
        payload["meta"]["candidate_membership_count"] = 649
        with self.assertRaisesRegex(RuntimeError, "candidate_membership_count 应为 650"):
            validate_gyfyyy_full_append(payload)

    def test_same_name_identity_clustering_merges_and_preserves_distinct_rows(self) -> None:
        def row(doctor_id: int, name: str, department: str, title: str, specialty: str) -> dict[str, object]:
            return {
                "姓名": name,
                "医院": "广州医科大学附属第一医院",
                "科室_分类页": department,
                "科室_列表卡片": department,
                "职称身份原文": title,
                "异常提示": "",
                "擅长诊疗方向摘录": specialty,
                "详情正文摘录": "",
                "来源链接": f"https://www.gyfyyy.cn/cn/ks/nk/hxnk/doctor_{doctor_id}.html",
            }

        source_rows = [
            row(1, "同一医生", "呼吸科", "主任医师", "慢阻肺和哮喘诊疗。"),
            row(2, "同一医生", "变态反应科", "主任医师", "慢阻肺和哮喘诊疗。"),
            row(3, "同名医生", "心血管内科", "副主任医师", "高血压和冠心病诊疗。"),
            row(4, "同名医生", "呼吸科", "副主任医师", "肺动脉高压和肺栓塞诊疗。"),
        ]

        merged, reconciliation = merge_gyfyyy_identity_rows(source_rows)

        self.assertEqual(len(merged), 3)
        same_identity = next(item for item in reconciliation if item["name"] == "同一医生")
        self.assertEqual(same_identity["resolution"], "同一人归并")
        self.assertEqual(same_identity["detail_ids"], ["1", "2"])
        self.assertIn("呼吸科", same_identity["departments"])
        self.assertIn("变态反应科", same_identity["departments"])
        distinct_rows = [item for item in merged if item["姓名"] == "同名医生"]
        self.assertEqual(len(distinct_rows), 2)
        self.assertTrue(all("同名待甄别" in item["异常提示"] for item in distinct_rows))


class GzbrainStaticExpertDirectoryTests(unittest.TestCase):
    ENTRY_URL = "https://www.gzbrain.cn/myzj/list.html"

    def _valid_full_payload(self) -> dict[str, object]:
        detail_ids = ["551", "102037", "990", "1231"] + [
            str(value) for value in range(1, 180)
        ]
        names = {
            "551": "沈峰",
            "102037": "沈峰",
            "990": "王丹逢",
            "1231": "王丹逢",
        }
        excluded_id = detail_ids[-1]
        rows = []
        reconciliation = []
        for detail_id in detail_ids:
            name = names.get(detail_id, f"医生{detail_id}")
            source_link = f"https://www.gzbrain.cn/myzj/info_itemid_{detail_id}.html"
            if detail_id == excluded_id:
                reconciliation.append(
                    {
                        "detail_id": detail_id,
                        "source_link": source_link,
                        "name": name,
                        "resolution": "护理排除",
                        "reason": "官网详情仅标注护理身份，排除医生画像采集范围",
                    }
                )
                continue
            warning = "同名待甄别" if name in {"沈峰", "王丹逢"} else ""
            rows.append(
                {
                    "姓名": name,
                    "重点优先级": "普通" if warning else "中",
                    "重点关注范围": "",
                    "重点疾病标签": "",
                    "擅长诊疗方向摘录": "精神疾病规范诊疗。",
                    "亮眼经历线索": "长期从事临床工作。",
                    "列表简介": "",
                    "详情正文摘录": "长期从事临床工作。",
                    "来源链接": source_link,
                    "异常提示": warning,
                }
            )
            reconciliation.append(
                {
                    "detail_id": detail_id,
                    "source_link": source_link,
                    "name": name,
                    "resolution": "正式行",
                    "reason": "",
                }
            )
        return {
            "meta": {
                "category_count": 31,
                "pagination_count": 31,
                "candidate_membership_count": 183,
                "unique_candidate_count": 183,
                "unique_doctor_count": len(rows),
                "census_unique_detail_count": 183,
                "census_named_detail_count": 183,
                "census_blank_name_detail_count": 0,
                "census_unique_nonblank_name_count": 181,
                "census_same_name_group_count": 2,
                "census_same_name_groups": {
                    "沈峰": ["551", "102037"],
                    "王丹逢": ["990", "1231"],
                },
                "category_error_count": 0,
                "detail_error_count": 0,
                "schedule_field_ingested_count": 0,
                "excluded_non_doctor_count": 1,
            },
            "rows": rows,
            "excluded_candidates": [
                {
                    "source_link": f"https://www.gzbrain.cn/myzj/info_itemid_{excluded_id}.html",
                    "reason": "官网详情仅标注护理身份，排除医生画像采集范围",
                }
            ],
            "gzbrain_detail_reconciliation": reconciliation,
        }

    def test_full_append_gate_accepts_complete_183_id_reconciliation(self) -> None:
        validate_gzbrain_full_append(self._valid_full_payload())

    def test_full_append_gate_rejects_missing_detail_id(self) -> None:
        payload = self._valid_full_payload()
        payload["rows"].pop()
        payload["gzbrain_detail_reconciliation"].pop(-2)
        payload["meta"]["unique_doctor_count"] -= 1
        with self.assertRaisesRegex(RuntimeError, "逐 ID 对账"):
            validate_gzbrain_full_append(payload)

    def test_full_append_gate_rejects_duplicate_source(self) -> None:
        payload = self._valid_full_payload()
        payload["rows"][-1]["来源链接"] = payload["rows"][0]["来源链接"]
        with self.assertRaisesRegex(RuntimeError, "来源详情 ID 不唯一"):
            validate_gzbrain_full_append(payload)

    def test_full_append_gate_rejects_schedule_pollution(self) -> None:
        payload = self._valid_full_payload()
        payload["rows"][0]["详情正文摘录"] = "每周一上午出诊。"
        with self.assertRaisesRegex(RuntimeError, "排班片段"):
            validate_gzbrain_full_append(payload)

    def test_full_append_gate_rejects_patient_identifiable_text(self) -> None:
        payload = self._valid_full_payload()
        payload["rows"][0]["亮眼经历线索"] = "患者案例：某某女性42岁，病情好转。"
        with self.assertRaisesRegex(RuntimeError, "患者案例或可识别信息"):
            validate_gzbrain_full_append(payload)

    def test_full_append_gate_rejects_tagged_abnormal_row(self) -> None:
        payload = self._valid_full_payload()
        payload["rows"][0].update(
            {"异常提示": "详情正文为空或未识别", "重点关注范围": "慢性病", "重点优先级": "高"}
        )
        with self.assertRaisesRegex(RuntimeError, "异常行仍被打标签"):
            validate_gzbrain_full_append(payload)

    def test_full_append_gate_rejects_unmarked_same_name_row(self) -> None:
        payload = self._valid_full_payload()
        same_name_row = next(row for row in payload["rows"] if row["姓名"] == "沈峰")
        same_name_row["异常提示"] = ""
        same_name_row["重点优先级"] = "中"
        with self.assertRaisesRegex(RuntimeError, "同名待甄别"):
            validate_gzbrain_full_append(payload)

    def test_full_append_gate_rejects_nonofficial_detail_url(self) -> None:
        payload = self._valid_full_payload()
        payload["rows"][0]["来源链接"] = "https://example.com/myzj/info_itemid_551.html"
        with self.assertRaisesRegex(RuntimeError, "非授权"):
            validate_gzbrain_full_append(payload)

    def test_adapter_and_detail_scope_are_exact(self) -> None:
        self.assertEqual(
            dedicated_adapter_for(self.ENTRY_URL), "gzbrain_static_expert_directory"
        )
        for invalid in [
            "https://www.gzbrain.cn/myzj/list.html?page=1",
            "https://www.gzbrain.cn/myzj/list.html#page",
            "https://api.gzbrain.cn/myzj/list.html",
            "https://www.gzbrain.cn/czys/list.html",
        ]:
            self.assertEqual(dedicated_adapter_for(invalid), "")
        self.assertEqual(
            gzbrain_detail_id("https://www.gzbrain.cn/myzj/info_itemid_966.html"),
            "966",
        )
        self.assertEqual(
            gzbrain_detail_id("https://www.gzbrain.cn/myzj/info_itemid_966.html?page=1"),
            "",
        )

    def test_human_confirmation_allows_non_a_difficulty(self) -> None:
        targets = confirmed_a_targets(
            [
                {
                    "城市": "广州市",
                    "医院名称": "广州医科大学附属脑科医院",
                    "官网首页_候选": "https://www.gzbrain.cn/",
                    "医生目录入口_候选": self.ENTRY_URL,
                    "采集难度_初判": "D-待人工补官网",
                    "人工复核结果": "确认可采集",
                }
            ],
            include_generic=True,
        )
        self.assertEqual(len(targets), 1)
        self.assertEqual(targets[0].adapter_id, "gzbrain_static_expert_directory")

    def test_list_page_discovery_expands_sparse_pager_window(self) -> None:
        html = """
        <section class="p_page">
          <a href="/myzj/list_page_1.html">1</a>
          <a href="/myzj/list_page_2.html">2</a>
          <a href="/myzj/list_page_31.html">末页</a>
        </section>
        """
        page_urls = discover_gzbrain_list_pages(html, self.ENTRY_URL)
        self.assertEqual(len(page_urls), 31)
        self.assertEqual(page_urls[0], self.ENTRY_URL)
        self.assertEqual(
            page_urls[1], "https://www.gzbrain.cn/myzj/list_page_2.html"
        )
        self.assertEqual(
            page_urls[-1], "https://www.gzbrain.cn/myzj/list_page_31.html"
        )

    def test_list_parser_uses_only_directory_cards_and_drops_schedule(self) -> None:
        html = """
        <div class="content_right"><a href="/myzj/info_itemid_999.html">轮播专家</a></div>
        <div class="expert_list"><ul class="ul clearfix">
          <li><a href="/myzj/info_itemid_966.html"><div class="txt">
            <h2>宁玉萍</h2><h3>主任医师 神经内科</h3>
            <h4><span>专长：</span>记忆障碍诊疗。</h4>
            <p>开诊时间：芳村门诊星期三上午</p>
          </div></a></li>
          <li><a href="/news/info_itemid_1.html"><div class="txt"><h2>新闻</h2></div></a></li>
        </ul></div>
        """
        rows = parse_gzbrain_list_page(html, self.ENTRY_URL)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "966")
        self.assertEqual(rows[0]["department"], "神经内科")
        self.assertEqual(rows[0]["specialty"], "记忆障碍诊疗。")
        self.assertIn("开诊时间", rows[0]["schedule"])

    def test_detail_parser_excludes_schedule_and_patient_case_sentences(self) -> None:
        html = """
        <div class="single_con">
          <div class="single-header"><h2>宁玉萍</h2><h3><span>主任医师</span></h3></div>
          <div class="single_cn"><div class="single_tex">
            <p>专长: 记忆障碍诊疗。</p><p>开诊时间: 芳村门诊星期三上午</p>
          </div></div>
          <div class="single-content"><span>*此排班仅作参考，以当日出诊为准</span>
            <h3>详细介绍</h3><p>长期从事神经内科临床工作。</p>
            <p>患者案例：某某女性42岁，病情好转。</p>
            <p>主持国家自然科学基金项目。</p>
          </div>
        </div>
        """
        detail = parse_gzbrain_detail(html, {})
        self.assertEqual(detail["name"], "宁玉萍")
        self.assertEqual(detail["specialty"], "记忆障碍诊疗。")
        self.assertNotRegex(detail["profile_text"], r"开诊|排班|患者案例|某某")
        self.assertIn("国家自然科学基金", detail["profile_text"])
        self.assertEqual(detail["patient_case_exclusion_count"], 1)

    def test_trial_selection_spreads_across_departments(self) -> None:
        doctors = [
            {"id": str(index), "department": f"科室{(index - 1) // 4}"}
            for index in range(1, 13)
        ]
        selected = select_gzbrain_trial_doctors(doctors, 10)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(len({item["department"] for item in selected}), 3)

    def test_collect_censuses_all_pages_and_keeps_trial_fields_clean(self) -> None:
        page_1 = """
        <section class="p_page"><a href="/myzj/list_page_1.html">1</a>
          <a href="/myzj/list_page_2.html">2</a></section>
        <div class="expert_list"><ul class="ul clearfix">{cards}</ul></div>
        """

        def card(doctor_id: int, department: str) -> str:
            return f"""<li><a href="/myzj/info_itemid_{doctor_id}.html"><div class="txt">
              <h2>医生{doctor_id}</h2><h3>主任医师 {department}</h3>
              <h4>专长：{department}常见疾病诊疗。</h4><p>开诊时间：芳村周一上午</p>
            </div></a></li>"""

        page_1_html = page_1.format(
            cards="".join(card(index, f"科室{(index - 1) // 3}") for index in range(1, 7))
        )
        page_2_html = '<div class="expert_list"><ul class="ul clearfix">' + "".join(
            card(index, f"科室{(index - 1) // 3}") for index in range(7, 13)
        ) + "</ul></div>"
        pages = {
            self.ENTRY_URL: page_1_html,
            "https://www.gzbrain.cn/myzj/list_page_2.html": page_2_html,
        }
        for index in range(1, 13):
            pages[f"https://www.gzbrain.cn/myzj/info_itemid_{index}.html"] = f"""
            <div class="single_con"><div class="single-header"><h2>医生{index}</h2>
              <h3><span>主任医师</span></h3></div><div class="single_cn"><div class="single_tex">
              <p>专长: 科室疾病诊疗。</p><p>开诊时间: 芳村周一上午</p></div></div>
              <div class="single-content"><h3>详细介绍</h3><p>长期从事临床工作。</p></div></div>
            """

        def fake_fetch(url: str, retries: int = 3):
            del retries
            html = pages.get(url)
            return (200, html, "") if html is not None else (None, "", "fixture missing")

        target = HospitalTarget(
            city="广州市",
            hospital="广州医科大学附属脑科医院",
            homepage="https://www.gzbrain.cn/",
            entry_url=self.ENTRY_URL,
            difficulty="D-待人工补官网",
            review="确认可采集",
            adapter_id="gzbrain_static_expert_directory",
        )
        with (
            patch("collect_official_doctors_batch.fetch_standard_public_get", side_effect=fake_fetch),
            patch("collect_official_doctors_batch.collect_existing_profile_links", return_value=set()),
            patch("collect_official_doctors_batch.time.sleep", return_value=None),
        ):
            payload = collect_gzbrain(target, "2026-08-13", max_doctors=10)

        self.assertEqual(payload["meta"]["pagination_count"], 2)
        self.assertEqual(payload["meta"]["census_unique_detail_count"], 12)
        self.assertEqual(len(payload["rows"]), 10)
        self.assertGreaterEqual(len({row["科室_分类页"] for row in payload["rows"]}), 3)
        self.assertEqual(payload["meta"]["schedule_field_ingested_count"], 0)
        for row in payload["rows"]:
            self.assertNotRegex(row["详情正文摘录"], r"开诊|出诊|排班")


class GzsysDrupalDoctorCardsTests(unittest.TestCase):
    ENTRY = "https://www.gzsys.org.cn/doctor/592/search"

    def test_adapter_requires_exact_official_entry(self) -> None:
        self.assertEqual(
            dedicated_adapter_for(self.ENTRY),
            "gzsys_drupal_doctor_cards",
        )
        self.assertEqual(dedicated_adapter_for(self.ENTRY + "?page=1"), "")
        self.assertEqual(dedicated_adapter_for("https://www.gzsys.org.cn/node/14894"), "")

    def test_node_and_doctor_aliases_share_numeric_identity(self) -> None:
        self.assertEqual(gzsys_detail_id("https://www.gzsys.org.cn/node/14894"), "14894")
        self.assertEqual(gzsys_detail_id("https://www.gzsys.org.cn/doctor/14894"), "14894")
        self.assertEqual(gzsys_detail_id("https://www.gzsys.org.cn/node/not-id"), "")

    def test_declared_default_all_pages_are_the_only_pages_constructed(self) -> None:
        html = """
        <a href="?department_target_id=All&talent_project=All&tutor_qualification=All&doctor_title=All&page=0">1</a>
        <a href="?department_target_id=All&talent_project=All&tutor_qualification=All&doctor_title=All&page=2">3</a>
        <a href="?department_target_id=296&talent_project=All&tutor_qualification=All&doctor_title=All&page=9">filtered</a>
        """
        pages = discover_gzsys_default_pages(html, self.ENTRY)
        self.assertEqual(len(pages), 3)
        self.assertTrue(pages[0].endswith("page=0"))
        self.assertTrue(pages[2].endswith("page=2"))
        self.assertNotIn("296", " ".join(pages))

    def test_only_strict_card_dom_authorizes_a_doctor(self) -> None:
        html = """
        <a href="/node/999">unrelated department node</a>
        <div class="card-4-0">
          <div class="card-title"><a href="/node/14894">宋尔卫</a></div>
          <div class="card-subtitle-content">教授, 主任医师</div>
          <div class="card-tag"><a href="/node/15187">乳腺外科</a></div>
        </div>
        <div class="card-4-0">
          <div class="card-title"><a href="/doctor/14811">李医生</a></div>
          <div class="card-subtitle-content">副主任医师</div>
          <div class="card-tag">心血管内科</div>
        </div>
        """
        rows = parse_gzsys_list_page(html, self.ENTRY)
        self.assertEqual([row["id"] for row in rows], ["14894", "14811"])
        self.assertEqual(rows[0]["department"], "乳腺外科")

    def test_detail_excludes_schedule_rank_patient_text_and_private_use(self) -> None:
        html = """
        <div class="other-2">
          <div class="other-left-title">宋尔卫</div>
          <div class="other-left-text"><span>职称：</span>教授, 主任医师</div>
          <div class="other-left-text"><span>科室：</span>乳腺外科</div>
          <div class="desc line-6">
            <p>擅长：乳腺癌诊疗。\ue001</p>
            <p>从事乳腺外科临床工作。</p>
            <p>好医生榜第一名。</p>
            <p>患者评价：非常好。</p>
          </div>
        </div>
        <div class="calendar-3-1">周一上午出诊</div>
        """
        detail = parse_gzsys_detail(html, {})
        self.assertEqual(detail["name"], "宋尔卫")
        self.assertEqual(detail["department"], "乳腺外科")
        self.assertEqual(detail["specialty"], "乳腺癌诊疗。")
        self.assertNotIn("好医生榜", detail["profile_text"])
        self.assertNotIn("患者评价", detail["profile_text"])
        self.assertNotRegex(detail["profile_text"], r"[\ue000-\uf8ff]")
        self.assertEqual(detail["schedule_exclusion_count"], 1)
        self.assertEqual(detail["forbidden_segment_count"], 2)

    def test_department_values_are_merged_with_chinese_separator(self) -> None:
        html = """
        <div class="other-2">
          <div class="other-left-title">姚和瑞</div>
          <div class="other-left-text"><span>职称：</span>主任医师</div>
          <div class="other-left-text"><span>科室：</span>乳腺内科, 肿瘤内科</div>
          <div class="desc line-6"><p>从事肿瘤内科临床工作。</p></div>
        </div>
        """
        detail = parse_gzsys_detail(html, {})
        self.assertEqual(detail["department"], "乳腺内科、肿瘤内科")

    def test_inline_clinic_time_is_removed_but_later_specialty_is_kept(self) -> None:
        value = (
            "熟悉各种内分泌疾病的诊断与治疗。"
            "出诊时间：周二下午，周四下午 特长：擅长糖尿病和甲状腺疾病。"
        )
        self.assertEqual(
            strip_gzsys_schedule_text(value),
            "熟悉各种内分泌疾病的诊断与治疗。 特长：擅长糖尿病和甲状腺疾病。",
        )
        html = f"""
        <div class="other-2">
          <div class="other-left-title">肖辉盛</div>
          <div class="other-left-text"><span>职称：</span>副主任医师</div>
          <div class="other-left-text"><span>科室：</span>内分泌内科</div>
          <div class="desc line-6"><p>{value}</p></div>
        </div>
        """
        detail = parse_gzsys_detail(html, {})
        self.assertNotRegex(detail["profile_text"], r"出诊时间|周二下午|周四下午")
        self.assertIn("糖尿病和甲状腺疾病", detail["profile_text"])
        self.assertEqual(detail["schedule_exclusion_count"], 1)

    def test_unlabeled_campus_schedule_tail_is_removed(self) -> None:
        value = "擅长中医内科疾病。院本部周二、三上午；南院区周一下午。"
        self.assertEqual(strip_gzsys_schedule_text(value), "擅长中医内科疾病。")

    def test_trial_selection_is_deterministic_round_robin_by_department(self) -> None:
        doctors = [
            {"id": str(index), "department": department}
            for index, department in enumerate(["A", "A", "B", "B", "C", "C"], start=1)
        ]
        selected = select_gzsys_trial_doctors(doctors, 5)
        self.assertEqual([doctor["id"] for doctor in selected], ["1", "3", "5", "2", "4"])

    def test_trial_gate_rejects_scope_drift_before_writing_artifacts(self) -> None:
        payload = {
            "meta": {
                "category_count": 22,
                "raw_card_rows": 664,
                "candidate_membership_count": 664,
                "unique_candidate_count": 664,
                "census_unique_detail_count": 664,
                "census_named_detail_count": 664,
                "census_blank_name_detail_count": 0,
                "census_nonempty_department_count": 664,
                "census_empty_department_count": 0,
                "census_same_name_group_count": 0,
                "cross_entry_duplicate_count": 0,
                "excluded_non_doctor_count": 6,
                "eligible_candidate_count": 658,
                "category_error_count": 0,
                "detail_error_count": 0,
                "schedule_field_ingested_count": 0,
                "private_use_character_count": 0,
                "unique_doctor_count": 0,
                "sample_entry_coverage_count": 0,
            },
            "rows": [],
            "excluded_candidates": [],
        }
        with self.assertRaisesRegex(RuntimeError, "category_count 应为 23"):
            validate_gzsys_trial(payload, expected_rows=10)

    def _valid_full_payload(self) -> dict[str, object]:
        formal_rows = []
        identity_reconciliation = []
        detail_reconciliation = []
        for detail_id in range(1, 659):
            source = f"https://www.gzsys.org.cn/node/{detail_id}"
            row = {
                "医院": "中山大学孙逸仙纪念医院",
                "姓名": f"医生{detail_id}",
                "科室_分类页": "内科",
                "职称身份原文": "主任医师",
                "重点优先级": "中",
                "重点关注范围": "",
                "重点疾病标签": "",
                "擅长诊疗方向摘录": "疾病诊疗",
                "亮眼经历线索": "",
                "列表简介": "",
                "详情正文摘录": "从事临床工作。",
                "来源类型": "医院官网",
                "来源链接": source,
                "采集入口": self.ENTRY,
                "详情页状态": "200",
                "异常提示": "",
            }
            formal_rows.append(row)
            detail_reconciliation.append(
                {
                    "detail_id": str(detail_id),
                    "name": row["姓名"],
                    "source_link": source,
                    "resolution": "正式行",
                    "reason": "",
                }
            )
            identity_reconciliation.append(
                {
                    "name": row["姓名"],
                    "resolution": "唯一身份",
                    "detail_ids": [str(detail_id)],
                    "primary_source_link": source,
                }
            )
        excluded = []
        for detail_id in range(659, 665):
            source = f"https://www.gzsys.org.cn/doctor/{detail_id}"
            excluded.append(
                {
                    "source_link": source,
                    "reason": "官网医生卡片仅标注护理身份，排除医生画像采集范围",
                }
            )
            detail_reconciliation.append(
                {
                    "detail_id": str(detail_id),
                    "name": f"护士{detail_id}",
                    "source_link": source,
                    "resolution": "护理排除",
                    "reason": excluded[-1]["reason"],
                }
            )
        return {
            "meta": {
                "category_count": 23,
                "pagination_count": 23,
                "raw_card_rows": 664,
                "candidate_membership_count": 664,
                "unique_candidate_count": 664,
                "unique_doctor_count": 658,
                "census_unique_detail_count": 664,
                "census_named_detail_count": 664,
                "census_blank_name_detail_count": 0,
                "census_unique_nonblank_name_count": 664,
                "census_same_name_group_count": 0,
                "census_department_count": 65,
                "census_nonempty_department_count": 664,
                "census_empty_department_count": 0,
                "eligible_candidate_count": 658,
                "cross_entry_duplicate_count": 0,
                "excluded_non_doctor_count": 6,
                "category_error_count": 0,
                "detail_error_count": 0,
                "schedule_field_ingested_count": 0,
                "private_use_character_count": 0,
                "gzsys_final_identity_count": 658,
                "gzsys_same_identity_merge_group_count": 0,
                "gzsys_distinct_same_name_group_count": 0,
                "filter_dictionary_counts": {
                    "department_target_id": 96,
                    "talent_project": 4,
                    "tutor_qualification": 5,
                    "doctor_title": 33,
                },
                "source_path_counts": {"node": 432, "doctor": 232},
            },
            "rows": formal_rows,
            "excluded_candidates": excluded,
            "gzsys_detail_reconciliation": detail_reconciliation,
            "gzsys_identity_reconciliation": identity_reconciliation,
        }

    def test_full_gate_accepts_complete_664_id_reconciliation(self) -> None:
        validate_gzsys_full_append(self._valid_full_payload())

    def test_full_gate_allows_only_known_25208_detail_failure(self) -> None:
        payload = self._valid_full_payload()
        failed_row = payload["rows"][0]  # type: ignore[index]
        failed_row["来源链接"] = "https://www.gzsys.org.cn/node/25208"
        failed_row["详情页状态"] = "失败"
        failed_row["异常提示"] = "详情页读取失败"
        failed_row["重点优先级"] = "普通"
        payload["gzsys_detail_reconciliation"][0]["detail_id"] = "25208"  # type: ignore[index]
        payload["gzsys_detail_reconciliation"][0]["source_link"] = failed_row["来源链接"]  # type: ignore[index]
        payload["gzsys_identity_reconciliation"][0]["detail_ids"] = ["25208"]  # type: ignore[index]
        payload["gzsys_identity_reconciliation"][0]["primary_source_link"] = failed_row["来源链接"]  # type: ignore[index]
        payload["rows"][251]["来源链接"] = "https://www.gzsys.org.cn/node/1"  # type: ignore[index]
        payload["gzsys_detail_reconciliation"][251]["detail_id"] = "1"  # type: ignore[index]
        payload["gzsys_detail_reconciliation"][251]["source_link"] = "https://www.gzsys.org.cn/node/1"  # type: ignore[index]
        payload["gzsys_identity_reconciliation"][251]["detail_ids"] = ["1"]  # type: ignore[index]
        payload["gzsys_identity_reconciliation"][251]["primary_source_link"] = "https://www.gzsys.org.cn/node/1"  # type: ignore[index]
        payload["detail_errors"] = [
            {"source_link": "https://www.gzsys.org.cn/node/25208", "error": "HTTP 404"}
        ]
        payload["meta"]["detail_error_count"] = 1  # type: ignore[index]
        validate_gzsys_full_append(payload)

    def test_full_gate_rejects_missing_id_and_abnormal_row_promotion(self) -> None:
        payload = self._valid_full_payload()
        payload["gzsys_detail_reconciliation"].pop()  # type: ignore[union-attr]
        payload["rows"][0]["异常提示"] = "列表与详情姓名不一致"  # type: ignore[index]
        payload["rows"][0]["重点关注范围"] = "慢性病"  # type: ignore[index]
        with self.assertRaisesRegex(RuntimeError, "逐 ID 对账工件不完整|异常行仍被"):
            validate_gzsys_full_append(payload)


class GzszyyDepartmentExpertDirectoryTests(unittest.TestCase):
    ENTRY_URL = "https://www.gzszyy.com/expert/"

    def test_adapter_and_detail_scope_are_exact(self) -> None:
        self.assertEqual(
            dedicated_adapter_for(self.ENTRY_URL),
            "gzszyy_department_expert_directory",
        )
        for invalid in [
            "https://www.gzszyy.com/expert/?page=1",
            "https://api.gzszyy.com/expert/",
            "https://www.gzszyy.com/expert/1/dp/3773/",
        ]:
            with self.subTest(invalid=invalid):
                self.assertEqual(dedicated_adapter_for(invalid), "")
        self.assertEqual(
            gzszyy_detail_id("https://www.gzszyy.com/expert/2026/w9aADOev.html"),
            "w9aADOev",
        )
        for invalid in [
            "https://www.gzszyy.com/expert/2026/w9aADOev.html?x=1",
            "https://www.gzszyy.com/expert/1/pr/99/",
            "https://other.example/expert/2026/w9aADOev.html",
        ]:
            with self.subTest(invalid=invalid):
                self.assertEqual(gzszyy_detail_id(invalid), "")

    def test_department_filters_and_pages_ignore_professional_and_level_filters(self) -> None:
        html = """
        <a href="/expert/1/dp/3773/">肿瘤一区</a>
        <a href="/expert/1/dp/3774/">肿瘤二区</a>
        <a href="/expert/1/pr/99/">主任中医师</a>
        <a href="/expert/1/le/3/">二级专家</a>
        """
        departments = discover_gzszyy_department_filters(html, self.ENTRY_URL)
        self.assertEqual(
            [(item["department_id"], item["department"]) for item in departments],
            [("3773", "肿瘤一区"), ("3774", "肿瘤二区")],
        )
        pages = discover_gzszyy_department_pages(
            '<div class="pager"><button data-all="2"></button></div>',
            departments[0],
        )
        self.assertEqual(
            pages,
            [
                "https://www.gzszyy.com/expert/1/dp/3773/",
                "https://www.gzszyy.com/expert/2/dp/3773/",
            ],
        )
        self.assertEqual(
            discover_gzszyy_unfiltered_pages(
                '<div class="pager"><button data-all="18"></button></div>',
                self.ENTRY_URL,
            ),
            [
                self.ENTRY_URL,
                *[f"https://www.gzszyy.com/expert/{page}/" for page in range(2, 19)],
            ],
        )

    def test_homepage_care_sites_are_strict_and_exclude_non_care_entities(self) -> None:
        html = """
        <a href="/district1_zzlyq/" title="珠玑院区">珠玑院区</a>
        <a href="/district1_thxyq/" title="天河新院区">天河新院区</a>
        <a href="/district1_tdfy/" title="同德院区">同德院区</a>
        <a href="/district1_wymzb/" title="五羊门诊部">五羊门诊部</a>
        <a href="/district1_tdmzb/" title="同德门诊部">同德门诊部</a>
        <a href="/district1_gzykdxzxylcxy/">广州医科大学中西医临床学院</a>
        <a href="https://other.example/district1_zzlyq/">外站</a>
        """
        sites = discover_gzszyy_care_sites(html, "https://www.gzszyy.com/patient/")
        self.assertEqual(
            [item["name"] for item in sites],
            ["珠玑院区", "天河新院区", "同德院区", "五羊门诊部", "同德门诊部"],
        )

    def test_department_card_and_detail_parsers_keep_schedule_out(self) -> None:
        list_html = """
        <ul class="doctor-list"><li>
          <h2><a href="/expert/2026/w9aADOev.html">叶穗林</a></h2>
          <div class="info"><div class="depart-info"><a title="名医堂">名医堂</a></div>
            <div>职称：主任中医师</div></div>
          <p><strong>擅长：</strong>擅长冠心病诊疗。</p>
        </li></ul>
        """
        department = {
            "department_id": "3780",
            "department": "心病科（心血管内科）",
            "entry_url": "https://www.gzszyy.com/expert/1/dp/3780/",
        }
        cards = parse_gzszyy_department_page(list_html, department["entry_url"], department)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["department"], "心病科（心血管内科）")
        self.assertEqual(cards[0]["card_department"], "名医堂")
        self.assertEqual(cards[0]["specialty"], "冠心病诊疗。")

        detail_html = """
        <div class="doctor-resume"><h1>叶穗林</h1><p>
          <u>科室：</u><a href="/department_a0/">名医堂<i></i></a>
          <a href="/department_b0/">心病科（心血管内科）<i></i></a><br/>
          <u>职称：</u>主任中医师<br/><u>级别：</u>二级专家</p>
          <p class="good-at"><u>擅长：</u>擅长冠心病诊疗。</p></div>
        <div class="doctor-items-intro"><p>医学硕士，硕士生导师。</p>
          <p>出诊时间：每周一上午。</p></div>
        <div class="doctor-code"><div class="qr-img">
          <span title="珠玑路院区">珠玑路院区</span>
        </div><div class="qr-img">
          <span title="同德围分院">同德围分院</span>
        </div></div>
        """
        detail = parse_gzszyy_detail(detail_html, cards[0])
        self.assertEqual(detail["name"], "叶穗林")
        self.assertEqual(detail["title"], "主任中医师")
        self.assertEqual(
            detail["departments"], ["名医堂", "心病科（心血管内科）"]
        )
        self.assertEqual(detail["specialty"], "冠心病诊疗。")
        self.assertEqual(detail["campuses"], ["珠玑路院区", "同德围分院"])
        self.assertIn("医学硕士", detail["profile_text"])
        self.assertNotRegex(detail["profile_text"], r"出诊|每周一")

    def test_qr_title_noise_is_reduced_to_explicit_campus_labels(self) -> None:
        detail_html = """
        <div class="doctor-resume"><h1>钟居孟</h1><p><u>职称：</u>主任医师</p></div>
        <div class="doctor-code">
          <div class="qr-img"><span title="广州医科大学附属中医医院同德围分院_综合门诊妇科_钟居孟T(60875)">二维码</span></div>
          <div class="qr-img"><span title="珠玑路院区v珠玑路院区">二维码</span></div>
        </div>
        """
        detail = parse_gzszyy_detail(
            detail_html,
            {"name": "钟居孟", "title": "主任医师", "specialty": "", "departments": []},
        )
        self.assertEqual(detail["campuses"], ["同德围分院", "珠玑路院区"])

    def test_trial_selection_spreads_across_departments(self) -> None:
        doctors = [
            {"id": str(index), "departments": [f"科室{(index - 1) // 4}"]}
            for index in range(1, 13)
        ]
        selected = select_gzszyy_trial_doctors(doctors, 10)
        self.assertEqual(len(selected), 10)
        self.assertGreaterEqual(
            len({department for item in selected for department in item["departments"]}),
            3,
        )

    def test_collect_censuses_department_tree_and_excludes_nursing(self) -> None:
        entry_html = """
        <a href="/expert/1/dp/1/">科室甲</a>
        <a href="/expert/1/dp/2/">科室乙</a>
        <a href="/expert/1/dp/3/">科室丙</a>
        <a href="/expert/1/pr/95/">主任护师</a>
        """

        def list_html(department: str, start: int, count: int, nursing: bool = False) -> str:
            cards = []
            for index in range(start, start + count):
                title = "主任护师" if nursing and index == start else "主任医师"
                cards.append(
                    f'<li><h2><a href="/expert/2026/id{index}.html">医生{index}</a></h2>'
                    f'<div class="info"><div class="depart-info"><a title="{department}">{department}</a></div>'
                    f'<div>职称：{title}</div></div><p>擅长：科室疾病诊疗。</p></li>'
                )
            return '<ul class="doctor-list">' + "".join(cards) + "</ul>"

        entry_html += '<div class="pager"><button data-all="1"></button></div>'
        entry_html += list_html("总目录", 1, 13, True)
        entry_html += """
          <ul class="doctor-list"><li>
            <h2><a href="/expert/2026/id14.html">医生14</a></h2>
            <div class="info"><div>职称：主任医师</div></div>
            <p>擅长：科室疾病诊疗。</p>
          </li></ul>
        """
        pages = {
            self.ENTRY_URL: entry_html,
            "https://www.gzszyy.com/patient/": """
                <a href="/district1_zzlyq/">珠玑院区</a>
                <a href="/district1_thxyq/">天河新院区</a>
                <a href="/district1_tdfy/">同德院区</a>
                <a href="/district1_wymzb/">五羊门诊部</a>
                <a href="/district1_tdmzb/">同德门诊部</a>
            """,
            "https://www.gzszyy.com/expert/1/dp/1/": list_html("科室甲", 1, 5, True),
            "https://www.gzszyy.com/expert/1/dp/2/": list_html("科室乙", 6, 4),
            "https://www.gzszyy.com/expert/1/dp/3/": list_html("科室丙", 10, 4),
        }
        for index in range(2, 15):
            pages[f"https://www.gzszyy.com/expert/2026/id{index}.html"] = f"""
            <div class="doctor-resume"><h1>医生{index}</h1><p>
              <u>科室：</u><a href="/department_a0/">科室{index}</a><br/>
              <u>职称：</u>主任医师</p><p class="good-at">擅长：科室疾病诊疗。</p></div>
            <div class="doctor-items-intro"><p>从事临床诊疗工作。</p></div>
            <div class="doctor-code"><div class="qr-img">
              <span title="珠玑路院区">珠玑路院区</span>
            </div></div>
            """

        def fake_fetch(_session: object, url: str, retries: int = 3) -> tuple[int, str, str]:
            del retries
            return (200, pages[url], "") if url in pages else (404, "", "HTTP 404")

        target = HospitalTarget(
            city="广州市",
            hospital="广州市中医院",
            homepage="https://www.gzszyy.com/patient/",
            entry_url=self.ENTRY_URL,
            difficulty="A-优先自动采集",
            review="确认可采集",
            adapter_id="gzszyy_department_expert_directory",
        )
        with (
            patch("collect_official_doctors_batch.create_official_session", return_value=object()),
            patch("collect_official_doctors_batch.fetch", side_effect=fake_fetch),
            patch("collect_official_doctors_batch.collect_existing_profile_links", return_value=set()),
            patch("collect_official_doctors_batch.time.sleep", return_value=None),
        ):
            payload = collect_gzszyy(target, "2026-08-13", max_doctors=10)

        self.assertEqual(payload["meta"]["census_department_count"], 3)
        self.assertEqual(payload["meta"]["candidate_membership_count"], 14)
        self.assertEqual(payload["meta"]["census_unique_detail_count"], 14)
        self.assertEqual(payload["meta"]["excluded_non_doctor_count"], 1)
        self.assertEqual(payload["meta"]["eligible_candidate_count"], 13)
        self.assertEqual(payload["meta"]["filter_link_counts"], {"dp": 3, "pr": 1, "le": 0})
        self.assertEqual(payload["meta"]["gzszyy_unfiltered_unique_detail_count"], 14)
        self.assertEqual(payload["meta"]["gzszyy_dp_unique_detail_count"], 13)
        self.assertEqual(payload["meta"]["gzszyy_unfiltered_only_detail_ids"], ["id14"])
        self.assertEqual(payload["meta"]["census_empty_department_count"], 1)
        self.assertEqual(payload["meta"]["census_group_count"], 5)
        self.assertEqual(payload["meta"]["gzszyy_campus_tagged_sample_count"], 10)
        self.assertTrue(
            all("珠玑路院区" in row["科室_列表卡片"] for row in payload["rows"])
        )
        self.assertEqual(len(payload["rows"]), 10)
        self.assertGreaterEqual(len({row["科室_分类页"] for row in payload["rows"]}), 3)
        self.assertEqual(payload["meta"]["detail_error_count"], 0)

    def test_full_identity_decisions_merge_three_groups_and_keep_wang_jian_separate(self) -> None:
        def row(detail_id: str, name: str, department: str, title: str, specialty: str) -> dict[str, object]:
            return {
                "序号": 0,
                "医院": "广州市中医院",
                "姓名": name,
                "科室_分类页": department,
                "科室_列表卡片": department,
                "职称_关键词": title,
                "职称身份原文": title,
                "重点优先级": "普通",
                "重点关注范围": "",
                "重点疾病标签": "",
                "擅长诊疗方向摘录": specialty,
                "亮眼经历线索": "",
                "列表简介": "",
                "详情正文摘录": specialty,
                "来源类型": "医院官网",
                "来源链接": f"https://www.gzszyy.com/expert/2026/{detail_id}.html",
                "采集入口": self.ENTRY_URL,
                "采集方式": "测试",
                "采集日期": "2026-08-13",
                "详情页状态": "200",
                "已建画像": "否",
                "异常提示": "同名待甄别",
                "复核状态": "待人工复核",
            }

        source_rows = [
            row("ELe31Mb6", "林少贞", "科室甲", "主任医师", "同一专长"),
            row("JxboyNeg", "林少贞", "科室乙", "主任医师", "同一专长"),
            row("4QbYVOdz", "唐瑾秋", "科室丙", "主任医师", "相同经历"),
            row("X7ax9byv", "唐瑾秋", "科室丁", "副主任医师", "相同经历"),
            row("LDdwkmd1", "高三德", "科室戊", "主任医师", "相同背景"),
            row("QBeXY8ay", "高三德", "科室己", "副主任医师", "相同背景"),
            row("3YaOggax", "王健", "检验病理科", "主管技师", "检验诊断"),
            row("WZdP6yaK", "王健", "外科", "主任医师", "外科诊疗"),
        ]
        detail_reconciliation = [
            {
                "detail_id": gzszyy_detail_id(str(item["来源链接"])),
                "relation_count": 1,
                "campuses": ["珠玑路院区"],
            }
            for item in source_rows
        ]

        merged, reconciliation = merge_gzszyy_identity_rows(
            source_rows, detail_reconciliation
        )

        self.assertEqual(len(merged), 5)
        self.assertEqual(
            {item["name"] for item in reconciliation if item["resolution"] == "同一人归并"},
            {"林少贞", "唐瑾秋", "高三德"},
        )
        wang_jian = [item for item in merged if item["姓名"] == "王健"]
        self.assertEqual(len(wang_jian), 2)
        self.assertTrue(all("同名待甄别" in item["异常提示"] for item in wang_jian))
        lin_shaozhen = next(item for item in merged if item["姓名"] == "林少贞")
        self.assertNotIn("同名待甄别", lin_shaozhen["异常提示"])
        self.assertIn("科室甲", lin_shaozhen["科室_分类页"])
        self.assertIn("科室乙", lin_shaozhen["科室_分类页"])
        self.assertIn(
            "多详情职称不一致",
            next(item for item in merged if item["姓名"] == "唐瑾秋")["异常提示"],
        )

    def test_full_gate_requires_all_423_ids_and_audited_name_decisions(self) -> None:
        excluded_ids = {f"nurse{index}" for index in range(1, 6)}
        merge_groups = [
            ("林少贞", ["ELe31Mb6", "JxboyNeg"]),
            ("唐瑾秋", ["4QbYVOdz", "X7ax9byv"]),
            ("高三德", ["LDdwkmd1", "QBeXY8ay"]),
        ]
        distinct_group = ("王健", ["3YaOggax", "WZdP6yaK"])
        special_ids = {
            detail_id
            for _, detail_ids in [*merge_groups, distinct_group]
            for detail_id in detail_ids
        }
        ordinary_ids = [f"id{index}" for index in range(1, 411)]
        formal_ids = [*sorted(special_ids), *ordinary_ids]
        self.assertEqual(len(formal_ids), 418)

        rows: list[dict[str, object]] = []
        identity_reconciliation: list[dict[str, object]] = []
        detail_reconciliation: list[dict[str, object]] = []
        for detail_id in formal_ids:
            name = next(
                (
                    group_name
                    for group_name, group_ids in [*merge_groups, distinct_group]
                    if detail_id in group_ids
                ),
                "李爱平" if detail_id == "id1" else f"医生{detail_id}",
            )
            detail_reconciliation.append(
                {
                    "detail_id": detail_id,
                    "name": name,
                    "resolution": "正式行",
                    "relation_count": 1,
                    "departments": [] if detail_id == "id1" else ["科室"],
                    "campuses": [],
                    "source_link": f"https://www.gzszyy.com/expert/2026/{detail_id}.html",
                }
            )

        used_ids: set[str] = set()
        for name, detail_ids in merge_groups:
            used_ids.update(detail_ids)
            primary = detail_ids[0]
            warning = "多详情职称不一致" if name in {"唐瑾秋", "高三德"} else ""
            rows.append(
                {
                    "姓名": name,
                    "来源链接": f"https://www.gzszyy.com/expert/2026/{primary}.html",
                    "科室_分类页": "科室甲、科室乙",
                    "职称身份原文": "主任医师",
                    "擅长诊疗方向摘录": "诊疗方向",
                    "详情正文摘录": "官方简介",
                    "亮眼经历线索": "",
                    "列表简介": "",
                    "重点优先级": "普通" if warning else "中",
                    "重点关注范围": "",
                    "重点疾病标签": "",
                    "异常提示": warning,
                }
            )
            identity_reconciliation.append(
                {
                    "name": name,
                    "resolution": "同一人归并",
                    "detail_ids": detail_ids,
                    "primary_source_link": rows[-1]["来源链接"],
                    "merged_source_links": [
                        f"https://www.gzszyy.com/expert/2026/{detail_ids[1]}.html"
                    ],
                    "departments": ["科室甲", "科室乙"],
                    "campuses": [],
                    "relation_count": 2,
                }
            )
        for detail_id in distinct_group[1]:
            used_ids.add(detail_id)
            rows.append(
                {
                    "姓名": "王健",
                    "来源链接": f"https://www.gzszyy.com/expert/2026/{detail_id}.html",
                    "科室_分类页": "检验病理科" if detail_id == "3YaOggax" else "外科",
                    "职称身份原文": "主管技师" if detail_id == "3YaOggax" else "主任医师",
                    "擅长诊疗方向摘录": "",
                    "详情正文摘录": "",
                    "亮眼经历线索": "",
                    "列表简介": "",
                    "重点优先级": "普通",
                    "重点关注范围": "",
                    "重点疾病标签": "",
                    "异常提示": "同名待甄别",
                }
            )
            identity_reconciliation.append(
                {
                    "name": "王健",
                    "resolution": "同名待甄别",
                    "detail_ids": [detail_id],
                    "primary_source_link": rows[-1]["来源链接"],
                    "merged_source_links": [],
                    "departments": [rows[-1]["科室_分类页"]],
                    "campuses": [],
                    "relation_count": 1,
                }
            )
        for detail_id in formal_ids:
            if detail_id in used_ids:
                continue
            is_top_only = detail_id == "id1"
            rows.append(
                {
                    "姓名": "李爱民" if is_top_only else f"医生{detail_id}",
                    "来源链接": (
                        "https://www.gzszyy.com/expert/2026/lNbWW4by.html"
                        if is_top_only
                        else f"https://www.gzszyy.com/expert/2026/{detail_id}.html"
                    ),
                    "科室_分类页": "" if is_top_only else "科室",
                    "职称身份原文": "" if is_top_only else "主任医师",
                    "擅长诊疗方向摘录": "",
                    "详情正文摘录": "官网新增公开履历" if is_top_only else "",
                    "亮眼经历线索": "",
                    "列表简介": "",
                    "重点优先级": "普通" if is_top_only else "中",
                    "重点关注范围": "",
                    "重点疾病标签": "",
                    "异常提示": (
                        "科室需人工复核；职称/身份需人工复核；详情正文为空或未识别"
                        if is_top_only
                        else ""
                    ),
                }
            )
            actual_id = "lNbWW4by" if is_top_only else detail_id
            identity_reconciliation.append(
                {
                    "name": rows[-1]["姓名"],
                    "resolution": "唯一身份",
                    "detail_ids": [actual_id],
                    "primary_source_link": rows[-1]["来源链接"],
                    "merged_source_links": [],
                    "departments": [],
                    "campuses": [],
                    "relation_count": 1,
                }
            )
        # Replace the placeholder ID with the audited top-only ID in detail coverage.
        formal_ids.remove("id1")
        formal_ids.append("lNbWW4by")
        detail_reconciliation = [
            item for item in detail_reconciliation if item["detail_id"] != "id1"
        ] + [
            {
                "detail_id": "lNbWW4by",
                "name": "李爱民",
                "resolution": "正式行",
                "relation_count": 1,
                "departments": [],
                "campuses": [],
                "source_link": "https://www.gzszyy.com/expert/2026/lNbWW4by.html",
            }
        ]
        excluded = [
            {
                "source_link": f"https://www.gzszyy.com/expert/2026/{detail_id}.html",
                "reason": "官网科室目录仅标注护理身份，排除医生画像采集范围",
            }
            for detail_id in excluded_ids
        ]
        meta = {
            "candidate_membership_count": 434,
            "unique_candidate_count": 423,
            "unique_doctor_count": 415,
            "census_unique_detail_count": 423,
            "census_named_detail_count": 423,
            "census_blank_name_detail_count": 0,
            "census_unique_nonblank_name_count": 419,
            "census_same_name_group_count": 4,
            "census_same_name_groups": {
                "林少贞": ["ELe31Mb6", "JxboyNeg"],
                "唐瑾秋": ["4QbYVOdz", "X7ax9byv"],
                "王健": ["3YaOggax", "WZdP6yaK"],
                "高三德": ["LDdwkmd1", "QBeXY8ay"],
            },
            "census_department_count": 35,
            "census_nonempty_department_count": 422,
            "census_empty_department_count": 1,
            "gzszyy_unfiltered_page_count": 18,
            "gzszyy_unfiltered_unique_detail_count": 423,
            "gzszyy_dp_unique_detail_count": 422,
            "gzszyy_unfiltered_only_detail_count": 1,
            "gzszyy_unfiltered_only_detail_ids": ["lNbWW4by"],
            "gzszyy_dp_only_detail_count": 0,
            "gzszyy_official_care_site_count": 5,
            "excluded_non_doctor_count": 5,
            "eligible_candidate_count": 418,
            "category_error_count": 0,
            "detail_error_count": 0,
            "schedule_field_ingested_count": 0,
            "gzszyy_final_identity_count": 415,
            "gzszyy_same_identity_merge_group_count": 3,
            "gzszyy_distinct_same_name_group_count": 1,
            "gzszyy_distinct_same_name_row_count": 2,
            "campus_relation_counts": {"珠玑路院区": 418},
        }
        payload = {
            "meta": meta,
            "rows": rows,
            "excluded_candidates": excluded,
            "gzszyy_detail_reconciliation": detail_reconciliation,
            "gzszyy_identity_reconciliation": identity_reconciliation,
        }
        for item in payload["gzszyy_detail_reconciliation"]:
            item["campuses"] = ["珠玑路院区"]

        validate_gzszyy_full_append(payload)
        payload["meta"]["candidate_membership_count"] = 433
        with self.assertRaisesRegex(RuntimeError, "candidate_membership_count 应为 434"):
            validate_gzszyy_full_append(payload)


class Gy3yStaticTeamDirectoryTests(unittest.TestCase):
    ENTRY_URL = "https://www.gy3y.cn/ks/team.html"

    def test_adapter_and_detail_scope_are_exact(self) -> None:
        self.assertEqual(dedicated_adapter_for(self.ENTRY_URL), "gy3y_static_team_directory")
        for invalid in [
            "https://www.gy3y.cn/ks/team.html?page=1",
            "https://www.gy3y.cn/ks/team.html#huangpu",
            "https://api.gy3y.cn/ks/team.html",
            "https://www.gy3y.cn/kstd/zjjs.html",
        ]:
            self.assertEqual(dedicated_adapter_for(invalid), "")
        liwan = "https://www.gy3y.cn/ks/nkxt/xxgnk/doctor_251.html"
        huangpu = "https://www.gy3y.cn/ks/hp/nk/xxgnk/doctor_251.html"
        self.assertEqual(gy3y_detail_id(liwan), "251")
        self.assertEqual(gy3y_detail_id(huangpu), "251")
        self.assertEqual(
            gy3y_detail_id(huangpu, "https://www.gy3y.cn/ks/hp/nk/xxgnk/"), "251"
        )
        self.assertEqual(gy3y_detail_id(huangpu, "https://www.gy3y.cn/ks/nkxt/xxgnk/"), "")
        self.assertEqual(gy3y_detail_id(f"{huangpu}?page=1"), "")
        self.assertEqual(gy3y_detail_id("https://www.gy3y.com/ks/hp/nk/xxgnk/doctor_251.html"), "")

    def test_directory_uses_formal_blocks_and_excludes_featured_carousel(self) -> None:
        html = """
        <section class="areatab tab">
          <div class="tabnav"><span class="current">荔湾院区</span><span>黄埔院区</span></div>
          <div class="tabcontent">
            <div class="tabsingle">
              <section class="threedslide"><a href="/ks/nkxt/xxgnk/doctor_999.html">推荐医生</a></section>
              <div class="title">内科系统</div>
              <section class="ksdoclist">
                <dl><dt>心血管内科</dt><dd><a href="/ks/nkxt/xxgnk/doctor_251.html">燕翼</a></dd></dl>
                <dl><dt>空科室</dt><dd></dd></dl>
              </section>
            </div>
            <div class="tabsingle">
              <section class="threedslide"><a href="/ks/hp/nk/xxgnk/doctor_998.html">推荐医生</a></section>
              <div class="title">内科系统</div>
              <section class="ksdoclist">
                <dl><dt>心血管内科</dt><dd><a href="/ks/hp/nk/xxgnk/doctor_251.html">燕翼</a></dd></dl>
              </section>
            </div>
          </div>
        </section>
        """

        result = discover_gy3y_directory(html, self.ENTRY_URL)

        self.assertEqual([item["name"] for item in result["campuses"]], ["荔湾院区", "黄埔院区"])
        self.assertEqual(len(result["categories"]), 3)
        self.assertEqual(len(result["relations"]), 2)
        self.assertEqual({item["id"] for item in result["relations"]}, {"251"})
        self.assertNotIn("999", {item["id"] for item in result["relations"]})
        self.assertNotIn("998", {item["id"] for item in result["relations"]})
        self.assertEqual(
            {item["department"] for item in result["relations"]},
            {"荔湾院区心血管内科", "黄埔院区心血管内科"},
        )

    def test_collect_merges_two_campuses_and_spreads_trial_sample(self) -> None:
        liwan_departments = [
            ("心血管内科", "nkxt", "xxgnk", [1, 2, 3, 4]),
            ("神经内科", "nkxt", "sjnk", [5, 6, 7, 8]),
        ]
        huangpu_departments = [
            ("心血管内科", "nk", "xxgnk", [1, 2]),
            ("儿科", "ek", "xenk", [9, 10, 11, 12]),
        ]

        def tab(campus: str, departments: list[tuple[str, str, str, list[int]]]) -> str:
            prefix = "/ks/hp" if campus == "黄埔院区" else "/ks"
            blocks = []
            for name, group, slug, ids in departments:
                links = "".join(
                    f'<dd><a href="{prefix}/{group}/{slug}/doctor_{doctor_id}.html">医生{doctor_id}</a></dd>'
                    for doctor_id in ids
                )
                blocks.append(f"<dl><dt>{name}</dt>{links}</dl>")
            return '<div class="tabsingle"><div class="title">系统</div><section class="ksdoclist">' + "".join(blocks) + "</section></div>"

        entry_html = f"""
        <section class="areatab tab">
          <div class="tabnav"><span>荔湾院区</span><span>黄埔院区</span></div>
          <div class="tabcontent">{tab("荔湾院区", liwan_departments)}{tab("黄埔院区", huangpu_departments)}</div>
        </section>
        """
        pages = {self.ENTRY_URL: entry_html}
        for campus, departments in [
            ("荔湾院区", liwan_departments),
            ("黄埔院区", huangpu_departments),
        ]:
            prefix = "/ks/hp" if campus == "黄埔院区" else "/ks"
            for department, group, slug, ids in departments:
                for doctor_id in ids:
                    pages[f"https://www.gy3y.cn{prefix}/{group}/{slug}/doctor_{doctor_id}.html"] = f"""
                    <section class="doctorcard"><strong>医生{doctor_id}</strong><b>主任医师</b>
                    <p>擅长{department}常见疾病。</p></section>
                    <section class="doctorintro"><p>长期从事{department}临床诊疗。</p></section>
                    <section class="calendar"><p>每周一上午出诊</p></section>
                    """

        def fake_fetch(_session, url, retries=3):
            html = pages.get(url)
            return (200, html, "") if html is not None else (None, "", "fixture missing")

        target = HospitalTarget(
            city="广州市",
            hospital="广州医科大学附属第三医院",
            homepage="https://www.gy3y.cn/index",
            entry_url=self.ENTRY_URL,
            difficulty="A-优先自动采集",
            review="确认可采集",
            adapter_id="gy3y_static_team_directory",
        )
        with (
            patch("collect_official_doctors_batch.create_official_session", return_value=object()),
            patch("collect_official_doctors_batch.fetch", side_effect=fake_fetch),
            patch("collect_official_doctors_batch.collect_existing_profile_links", return_value=set()),
        ):
            payload = collect_gy3y(target, "2026-08-13", max_doctors=10)

        self.assertEqual(payload["meta"]["category_count"], 4)
        self.assertEqual(payload["meta"]["candidate_membership_count"], 14)
        self.assertEqual(payload["meta"]["census_unique_detail_count"], 12)
        self.assertEqual(payload["meta"]["gy3y_cross_campus_identity_count"], 2)
        self.assertEqual(payload["meta"]["campus_relation_counts"], {"荔湾院区": 8, "黄埔院区": 6})
        self.assertEqual(len(payload["rows"]), 10)
        self.assertGreaterEqual(len({row["科室_分类页"] for row in payload["rows"]}), 3)
        self.assertTrue(any("/ks/hp/" in row["来源链接"] for row in payload["rows"]))
        merged = next(row for row in payload["rows"] if row["姓名"] == "医生1")
        self.assertIn("荔湾院区心血管内科", merged["科室_分类页"])
        self.assertIn("黄埔院区心血管内科", merged["科室_分类页"])
        self.assertNotRegex(merged["详情正文摘录"], r"排班|出诊|每?周[一二三四五六日天]")
        self.assertEqual(payload["meta"]["detail_error_count"], 0)

    def test_report_only_renders_current_adapter_reconciliation(self) -> None:
        from tempfile import TemporaryDirectory

        payload = {
            "meta": {
                "execution_mode": "trial",
                "hospital": "广州医科大学附属第三医院",
                "city": "广州市",
                "collected_at": "2026-08-13",
                "entry_url": self.ENTRY_URL,
                "homepage": "https://www.gy3y.cn/index",
                "entry_url_source": "Issue #27",
                "ledger_entry_url": self.ENTRY_URL,
                "adapter_id": "gy3y_static_team_directory",
                "ledger_review": "确认可采集",
                "ledger_difficulty": "A-优先自动采集",
                "unique_doctor_count": 1,
                "raw_card_rows": 2,
                "category_count": 2,
                "department_coverage_count": 2,
                "detail_error_count": 0,
                "category_error_count": 0,
                "existing_profile_count": 0,
                "census_group_count": 2,
                "census_department_count": 2,
                "census_unique_detail_count": 1,
                "gy3y_multi_relation_identity_count": 1,
                "gy3y_cross_campus_identity_count": 1,
                "census_nursing_identity_status": "TRIAL 详情样本纯护理身份排除 0 位",
            },
            "entry_reconnaissance": [],
            "excluded_candidates": [],
            "cross_entry_duplicates": [],
            "gy3y_detail_reconciliation": [{"detail_id": "1"}],
            "gy3y_identity_reconciliation": [],
            "category_errors": [],
            "detail_errors": [],
            "category_counts": [],
            "priority_counts": {},
            "group_counts": {},
            "warning_counts": {},
            "rows": [],
        }
        with TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "report.md"
            write_report(report_path, payload, root / "trial.csv", root / "trial.xlsx")
            report = report_path.read_text(encoding="utf-8")

        self.assertIn("## 广医三院两院区详情身份对账", report)
        self.assertNotIn("## 广医一院同名详情身份聚类对账", report)
        self.assertNotIn("## 广医口腔逐 ID 归并/排除对账", report)
        self.assertNotIn("## 广东省第二中医院同名归并对账", report)

    def test_full_append_gate_reconciles_every_detail_id(self) -> None:
        rows = []
        detail_reconciliation = []
        identity_reconciliation = []
        for doctor_id in range(1, 439):
            source = f"https://www.gy3y.cn/ks/nkxt/ks/doctor_{doctor_id}.html"
            row = {
                "姓名": f"医生{doctor_id}",
                "科室_分类页": "荔湾院区内科",
                "重点优先级": "普通",
                "重点关注范围": "",
                "重点疾病标签": "",
                "擅长诊疗方向摘录": "常见疾病诊疗",
                "亮眼经历线索": "",
                "列表简介": "",
                "详情正文摘录": "曾赴基层出诊并长期从事临床工作",
                "来源链接": source,
                "异常提示": "",
            }
            rows.append(row)
            detail_reconciliation.append(
                {
                    "detail_id": str(doctor_id),
                    "name": f"医生{doctor_id}",
                    "departments": ["荔湾院区产科、妇科"],
                }
            )
            identity_reconciliation.append(
                {
                    "detail_ids": [str(doctor_id)],
                    "primary_source_link": source,
                }
            )
        payload = {
            "meta": {
                "category_count": 104,
                "candidate_membership_count": 580,
                "census_unique_detail_count": 438,
                "cross_entry_duplicate_count": 142,
                "gy3y_multi_relation_identity_count": 126,
                "gy3y_cross_campus_identity_count": 117,
                "census_nonempty_department_count": 99,
                "census_empty_department_count": 5,
                "category_error_count": 0,
                "detail_error_count": 0,
                "excluded_non_doctor_count": 0,
                "unique_doctor_count": 438,
                "gy3y_final_identity_count": 438,
                "campus_relation_counts": {"荔湾院区": 390, "黄埔院区": 190},
            },
            "rows": rows,
            "excluded_candidates": [],
            "gy3y_detail_reconciliation": detail_reconciliation,
            "gy3y_identity_reconciliation": identity_reconciliation,
        }

        validate_gy3y_full_append(payload)
        payload["meta"]["candidate_membership_count"] = 579
        with self.assertRaisesRegex(RuntimeError, "candidate_membership_count"):
            validate_gy3y_full_append(payload)
        payload["meta"]["candidate_membership_count"] = 580
        payload["rows"][0]["详情正文摘录"] = "专家门诊时间：每周一上午"
        with self.assertRaisesRegex(RuntimeError, "排班片段"):
            validate_gy3y_full_append(payload)


class NodeRuntimeResolutionTests(unittest.TestCase):
    def test_bundled_runtime_is_preferred_without_hardcoded_user(self) -> None:
        bundled = Path("C:/Users/current/.cache/codex-runtimes/node.exe")
        with (
            patch("collect_official_doctors_batch.BUNDLED_NODE", bundled),
            patch.object(Path, "exists", return_value=True),
            patch("collect_official_doctors_batch.shutil.which", return_value="C:/node.exe"),
        ):
            self.assertEqual(find_node(), str(bundled))

    def test_path_runtime_is_used_when_bundled_runtime_is_missing(self) -> None:
        with (
            patch("collect_official_doctors_batch.BUNDLED_NODE", Path("C:/missing/node.exe")),
            patch.object(Path, "exists", return_value=False),
            patch("collect_official_doctors_batch.shutil.which", return_value="C:/node.exe"),
        ):
            self.assertEqual(find_node(), "C:/node.exe")

    def test_missing_runtime_is_reported(self) -> None:
        with (
            patch("collect_official_doctors_batch.BUNDLED_NODE", Path("C:/missing/node.exe")),
            patch.object(Path, "exists", return_value=False),
            patch("collect_official_doctors_batch.shutil.which", return_value=None),
        ):
            with self.assertRaisesRegex(RuntimeError, "未找到 Node.js"):
                find_node()


class GenericDirectoryFilteringTests(unittest.TestCase):
    def test_hospital_batch_keeps_all_unique_collection_entries(self) -> None:
        rows = [
            {
                "医院": "南方医科大学口腔医院(海珠广场院区)",
                "采集入口": "https://www.smukqyy.cn/section/341",
            },
            {
                "医院": "南方医科大学口腔医院(海珠广场院区)",
                "采集入口": "https://www.smukqyy.cn/section/342",
            },
            {
                "医院": "南方医科大学口腔医院(海珠广场院区)",
                "采集入口": "https://www.smukqyy.cn/section/341",
            },
        ]

        batches = build_hospital_batches(rows)

        self.assertEqual(
            batches[0]["采集入口"],
            "https://www.smukqyy.cn/section/341、https://www.smukqyy.cn/section/342",
        )

    def test_section_directory_only_accepts_matching_prods_links(self) -> None:
        entry_url = "https://www.smukqyy.cn/section/364"
        html = """
        <div><a href="/prods/364/200">万蕾 主任医师 科室：牙体牙髓病科一室</a></div>
        <div><a href="/prods/364/201">张三 临床硕士生...</a></div>
        <div><a href="/doctor/166">就诊须知 医师 门诊</a></div>
        <div><a href="/prods/999/200">张三 主任医师 科室：口腔科</a></div>
        """

        rows = discover_generic_detail_links(html, entry_url, entry_url)

        self.assertEqual(
            [row["source_link"] for row in rows],
            [
                "https://www.smukqyy.cn/prods/364/200",
                "https://www.smukqyy.cn/prods/364/201",
            ],
        )
        self.assertTrue(matches_generic_directory_detail_url(entry_url, rows[0]["source_link"]))
        self.assertFalse(matches_generic_directory_detail_url(entry_url, "https://www.smukqyy.cn/doctor/166"))
        self.assertTrue(
            matches_generic_directory_detail_url(
                "https://hospital.example/section/364",
                "https://hospital.example/doctor/166",
            )
        )

    def test_navigation_names_are_blacklisted(self) -> None:
        for value in ["就诊须知", "住院须知", "联系我们", "门诊时间"]:
            with self.subTest(value=value):
                self.assertFalse(looks_like_person_name(value))
        self.assertTrue(looks_like_person_name("万蕾"))

    def test_multi_entry_urls_are_deduplicated_in_owner_order(self) -> None:
        target = HospitalTarget(
            city="广州市",
            hospital="南方医科大学口腔医院(海珠广场院区)",
            homepage="https://www.smukqyy.cn/home",
            entry_url="https://www.smukqyy.cn/section/341",
            difficulty="A-优先自动采集",
            review="确认可采集",
            adapter_id="generic_official_template",
            entry_urls=(
                "https://www.smukqyy.cn/section/341",
                "https://www.smukqyy.cn/section/342",
                "https://www.smukqyy.cn/section/341/",
            ),
        )

        self.assertEqual(
            effective_entry_urls(target),
            [
                "https://www.smukqyy.cn/section/341",
                "https://www.smukqyy.cn/section/342",
            ],
        )

    def test_multi_entry_trial_sampling_round_robins_across_sections(self) -> None:
        entry_urls = [
            "https://www.smukqyy.cn/section/341",
            "https://www.smukqyy.cn/section/342",
            "https://www.smukqyy.cn/section/434",
        ]
        items = [
            {"entry_url": entry_urls[0], "source_link": "https://www.smukqyy.cn/prods/341/2"},
            {"entry_url": entry_urls[0], "source_link": "https://www.smukqyy.cn/prods/341/1"},
            {"entry_url": entry_urls[1], "source_link": "https://www.smukqyy.cn/prods/342/1"},
            {"entry_url": entry_urls[2], "source_link": "https://www.smukqyy.cn/prods/434/1"},
        ]

        selected = round_robin_generic_items(items, entry_urls, max_items=3)

        self.assertEqual([item["entry_url"] for item in selected], entry_urls)
        self.assertEqual(selected[0]["source_link"], "https://www.smukqyy.cn/prods/341/1")

    def test_spread_sampling_keeps_entry_coverage_and_uses_distant_candidates(self) -> None:
        entry_urls = ["http://www.ny5y.cn/a", "http://www.ny5y.cn/b"]
        items = [
            {
                "entry_url": entry_urls[0],
                "source_link": f"http://www.ny5y.cn/yisheng_xq.php?id={index}",
            }
            for index in range(1, 101)
        ] + [
            {
                "entry_url": entry_urls[1],
                "source_link": "http://www.ny5y.cn/yisheng_xq.php?id=999",
            }
        ]

        selected = round_robin_generic_items(items, entry_urls, max_items=10, spread=True)

        self.assertEqual(len(selected), 10)
        self.assertEqual(selected[1]["entry_url"], entry_urls[1])
        selected_ids = [int(item["source_link"].rsplit("=", 1)[-1]) for item in selected]
        self.assertGreater(max(selected_ids[:-1]) - min(selected_ids[:-1]), 70)


class GdskinAspNetExpertTests(unittest.TestCase):
    ENTRY_URL = "https://www.gdskin.com/Showclass.aspx?id=917"

    def test_adapter_and_detail_url_scope_are_strict(self) -> None:
        self.assertEqual(dedicated_adapter_for(self.ENTRY_URL), "gdskin_aspnet_expert")
        self.assertTrue(
            matches_generic_directory_detail_url(
                self.ENTRY_URL,
                "https://www.gdskin.com/ShowNews.ASPX?ID=5000",
            )
        )
        self.assertFalse(
            matches_generic_directory_detail_url(
                self.ENTRY_URL,
                "https://www.gdskin.com/ShowNews.ASPX?ID=3992&t?id=163",
            )
        )
        self.assertEqual(
            generic_detail_identity("https://www.gdskin.com/shownews.aspx?id=5000"),
            "gdskin:5000",
        )

    def test_gridview_keeps_doctors_and_reports_nurse_exclusion(self) -> None:
        html = """
        <table class="masterTitleH">
          <tr><td><a href="ShowNews.ASPX?ID=5000">刘振锋 主任医师 医学博士</a></td></tr>
          <tr><td><a href="ShowNews.ASPX?ID=5737">王辉 主管护师</a></td></tr>
        </table>
        """

        rows = discover_generic_detail_links(html, self.ENTRY_URL, self.ENTRY_URL)
        excluded = discover_gdskin_excluded_links(html, self.ENTRY_URL, self.ENTRY_URL)

        self.assertEqual([row["name"] for row in rows], ["刘振锋"])
        self.assertEqual(rows[0]["department"], "激光美肤中心")
        self.assertEqual([row["list_title"] for row in excluded], ["王辉 主管护师"])

    def test_label_content_parser_avoids_site_navigation(self) -> None:
        html = """
        <html><head><title>曲永彬 主任医师__医院官网</title></head><body>
          <nav>网站首页 医院概况 专家团队</nav>
          <div class="labelContent">预约挂号 曲永彬 主任医师、医学硕士
          专长：银屑病、痤疮、黄褐斑
          简介：从事中医皮肤病临床工作20年，发表学术论文10余篇。</div>
        </body></html>
        """

        detail = parse_gdskin_detail(
            html,
            {"name": "曲永彬", "department": "中医皮肤科", "list_title": "曲永彬 主任医师"},
        )

        self.assertEqual(detail["name"], "曲永彬")
        self.assertEqual(detail["department"], "中医皮肤科")
        self.assertEqual(detail["specialty"], "银屑病、痤疮、黄褐斑")
        self.assertIn("发表学术论文10余篇", detail["profile_text"])
        self.assertNotIn("网站首页", detail["profile_text"])

    def test_label_content_paragraphs_separate_specialty_from_academic_profile(self) -> None:
        html = """
        <html><head><title>刘振锋 主任医师__医院官网</title></head><body>
          <div class="labelContent">
            <p><a href="appointment">预约挂号</a></p>
            <p>刘振锋 主任医师 医学博士 硕士研究生导师</p>
            <p>专长：痤疮、色素性疾病、血管性疾病、皮肤激光美容、面部年轻化</p>
            <p>国家重点学科博士毕业。从事临床工作10余年。主持科研基金项目，发表SCI论文多篇。</p>
          </div>
        </body></html>
        """

        detail = parse_gdskin_detail(
            html,
            {"name": "刘振锋", "department": "激光美肤中心", "list_title": "刘振锋 主任医师"},
        )

        self.assertEqual(
            detail["specialty"],
            "痤疮、色素性疾病、血管性疾病、皮肤激光美容、面部年轻化",
        )
        self.assertNotIn("博士毕业", detail["specialty"])
        self.assertIn("主持科研基金项目", detail["profile_text"])
        self.assertIn("发表SCI论文多篇", detail["profile_text"])

    def test_unlabeled_profile_keeps_specialty_blank_and_moves_biography_out_of_title(self) -> None:
        html = """
        <html><head><title>李畅畅 医师__医院官网</title></head><body>
          <div class="labelContent">
            <p>李畅畅 博士 医师 博士毕业于中山大学，从事性病预防控制近10年。主持科研项目，发表SCI文章4篇。</p>
          </div>
        </body></html>
        """

        detail = parse_gdskin_detail(
            html,
            {"name": "李畅畅", "department": "外阴皮肤病/性病科", "list_title": "李畅畅 博士 医师"},
        )

        self.assertEqual(detail["title_field"], "博士 医师")
        self.assertEqual(detail["specialty"], "")
        self.assertIn("博士毕业于中山大学", detail["profile_text"])

    def test_explicit_refresh_replaces_matching_master_row_only(self) -> None:
        existing = [{"医院": "测试医院", "姓名": "张强", "来源链接": "https://example.test/1", "职称身份原文": "旧职称"}]
        incoming = [{"医院": "测试医院", "姓名": "张强", "来源链接": "https://example.test/1", "职称身份原文": "新职称"}]

        merged, added, skipped, refreshed, existing_duplicates = merge_rows_for_master(
            existing,
            incoming,
            preserve_existing=True,
            refresh_incoming=True,
        )

        self.assertEqual(merged[0]["职称身份原文"], "新职称")
        self.assertEqual((added, skipped, refreshed, existing_duplicates), (0, 0, 1, 0))

    def test_gridview_postback_page_is_materialized(self) -> None:
        html = """
        <form>
          <input type="hidden" name="__VIEWSTATE" value="state" />
          <input type="hidden" name="__EVENTVALIDATION" value="validation" />
          <table class="masterTitleH"><tr><td>
            <a href="javascript:__doPostBack('doctorGrid','Page$2')">2</a>
          </td></tr></table>
        </form>
        """

        class FakeResponse:
            status_code = 200
            apparent_encoding = "utf-8"
            encoding = "utf-8"
            text = "<table class='masterTitleH'><a href='ShowNews.ASPX?ID=5575'>余晓玲 主治医师</a></table>"

        class FakeSession:
            def __init__(self) -> None:
                self.calls: list[tuple[str, dict[str, str]]] = []

            def post(self, url: str, data: dict[str, str], timeout: int) -> FakeResponse:
                self.calls.append((url, data))
                return FakeResponse()

        session = FakeSession()
        documents, errors = discover_gdskin_postback_documents(session, self.ENTRY_URL, html, 5)

        self.assertEqual(errors, [])
        self.assertEqual([document["page"] for document in documents], ["1", "2"])
        self.assertEqual(session.calls[0][1]["__EVENTTARGET"], "doctorGrid")
        self.assertEqual(session.calls[0][1]["__EVENTARGUMENT"], "Page$2")

    def test_collect_generic_returns_complete_gdskin_payload(self) -> None:
        entry_urls = (
            "https://www.gdskin.com/Showclass.aspx?id=901",
            "https://www.gdskin.com/Showclass.aspx?id=906",
            "https://www.gdskin.com/Showclass.aspx?id=917",
        )
        list_html = {
            entry_urls[0]: """
                <table class="masterTitleH">
                  <a href="ShowNews.ASPX?ID=5000">张强 主任医师</a>
                  <a href="ShowNews.ASPX?ID=5001">李明 副主任医师</a>
                </table>
            """,
            entry_urls[1]: """
                <table class="masterTitleH">
                  <a href="ShowNews.ASPX?ID=5000">张强 主任医师</a>
                  <a href="ShowNews.ASPX?ID=5002">王敏 主治医师</a>
                </table>
            """,
            entry_urls[2]: """
                <table class="masterTitleH">
                  <a href="ShowNews.ASPX?ID=5003">赵芳 主治医师</a>
                  <a href="ShowNews.ASPX?ID=5737">王辉 主管护师</a>
                </table>
            """,
        }
        details = {
            "5000": ("张强", "主任医师"),
            "5001": ("李明", "副主任医师"),
            "5002": ("王敏", "主治医师"),
            "5003": ("赵芳", "主治医师"),
        }

        def fake_fetch(_session: object, url: str, retries: int = 3) -> tuple[int, str, str]:
            del retries
            if url in list_html:
                return 200, list_html[url], ""
            detail_id = url.rsplit("=", 1)[-1]
            name, title = details[detail_id]
            return (
                200,
                f'<div class="labelContent">{name} {title} 专长：皮肤病规范诊疗。简介：从事临床工作十年。</div>',
                "",
            )

        target = HospitalTarget(
            city="广州市",
            hospital="南方医科大学皮肤病医院",
            homepage="https://www.gdskin.com/",
            entry_url=entry_urls[0],
            difficulty="A-优先自动采集",
            review="确认可采集",
            adapter_id="gdskin_aspnet_expert",
            entry_urls=entry_urls,
            ledger_entry_url=entry_urls[0],
        )
        with (
            patch("collect_official_doctors_batch.create_official_session", return_value=object()),
            patch("collect_official_doctors_batch.collect_existing_profile_links", return_value=set()),
            patch("collect_official_doctors_batch.fetch", side_effect=fake_fetch),
            patch("collect_official_doctors_batch.time.sleep", return_value=None),
        ):
            payload = collect_generic(target, "2026-08-11", max_doctors=None, max_pages=5)

        self.assertEqual(payload["meta"]["candidate_membership_count"], 5)
        self.assertEqual(payload["meta"]["unique_candidate_count"], 4)
        self.assertEqual(payload["meta"]["cross_entry_duplicate_count"], 1)
        self.assertEqual(payload["meta"]["sample_entry_coverage_count"], 3)
        self.assertEqual(payload["meta"]["excluded_non_doctor_count"], 1)
        self.assertEqual(len(payload["entry_reconnaissance"]), 3)
        self.assertEqual([item["unique_detail_count"] for item in payload["entry_reconnaissance"]], [2, 2, 1])
        self.assertEqual(len(payload["cross_entry_duplicates"]), 1)
        self.assertEqual(len(payload["rows"]), 4)
        self.assertCountEqual(
            payload["meta"]["sample_entry_categories"],
            ["首席专家", "皮肤内科", "激光美肤中心"],
        )
        self.assertEqual({row["采集入口"] for row in payload["rows"]}, set(entry_urls))
        shared_row = next(row for row in payload["rows"] if row["姓名"] == "张强")
        self.assertEqual(shared_row["科室_分类页"], "皮肤内科")
        general_only_row = next(row for row in payload["rows"] if row["姓名"] == "李明")
        self.assertEqual(general_only_row["科室_分类页"], "")
        self.assertIn("科室需人工复核", general_only_row["异常提示"])

    def test_full_append_gate_rejects_general_expert_category(self) -> None:
        counts = {
            "901": 1,
            "902": 3,
            "906": 29,
            "910": 7,
            "913": 8,
            "915": 14,
            "917": 6,
            "921": 4,
            "922": 5,
            "924": 0,
        }
        payload = {
            "meta": {
                "unique_candidate_count": 77,
                "unique_doctor_count": 77,
                "candidate_membership_count": 77,
                "cross_entry_duplicate_count": 0,
                "category_error_count": 0,
                "detail_error_count": 0,
                "excluded_non_doctor_count": 1,
            },
            "entry_reconnaissance": [
                {
                    "entry_url": f"https://www.gdskin.com/Showclass.aspx?id={entry_id}",
                    "unique_detail_count": count,
                    "list_page_count": 2 if entry_id == "906" else 1,
                }
                for entry_id, count in counts.items()
            ],
            "rows": [{"姓名": "张强", "科室_分类页": "首席专家"}],
        }

        with self.assertRaisesRegex(RuntimeError, "科室仍为首席/知名专家类目：张强"):
            validate_gdskin_full_append(payload)


class Ny5yOfficialExpertTests(unittest.TestCase):
    ENTRY_MAIN = "http://www.ny5y.cn/zhuanjia_mingyi.php?id=100"
    ENTRY_LINGNAN = "http://www.ny5y.cn/zhuanjia_lingnan.php?id=162"

    def test_entry_and_detail_url_scope_are_strict(self) -> None:
        self.assertEqual(ny5y_entry_kind(self.ENTRY_MAIN), "100")
        self.assertEqual(ny5y_entry_kind(self.ENTRY_LINGNAN), "162")
        self.assertEqual(
            dedicated_adapter_for(self.ENTRY_MAIN),
            "ny5y_official_expert",
        )
        self.assertEqual(ny5y_detail_id("http://www.ny5y.cn/yisheng_xq.php?id=229"), "229")
        self.assertEqual(
            generic_detail_identity("http://ny5y.cn/yisheng_xq.php?id=229"),
            "ny5y:229",
        )
        for invalid in [
            "http://www.ny5y.cn/keshi_jianjie.php?id=125",
            "http://www.ny5y.cn/keyanjiaoxue_zhuanjia.php?id=55",
            "http://www.ny5y.cn/yisheng_xq.php?id=229&from=third-party",
            "http://example.com/yisheng_xq.php?id=229",
        ]:
            with self.subTest(invalid=invalid):
                self.assertFalse(matches_generic_directory_detail_url(self.ENTRY_MAIN, invalid))

    def test_directory_only_accepts_yisheng_detail_links(self) -> None:
        html = """
        <div><a href="yisheng_xq.php?id=229"><span>· 赵汉民</span></a></div>
        <div><a href="keshi_jianjie.php?id=125">创伤骨科</a></div>
        <div><a href="keyanjiaoxue_zhuanjia.php?id=55">研究生导师</a></div>
        <div><a href="yisheng_xq.php?id=229&extra=1">异常参数</a></div>
        """

        rows = discover_generic_detail_links(html, self.ENTRY_MAIN, self.ENTRY_MAIN)

        self.assertEqual([row["source_link"] for row in rows], ["http://www.ny5y.cn/yisheng_xq.php?id=229"])
        self.assertEqual(rows[0]["name"], "赵汉民")
        self.assertEqual(rows[0]["department"], "专家风采")

    def test_detail_dom_parser_uses_only_profile_blocks(self) -> None:
        html = """
        <nav>医院首页 新闻动态 联系我们</nav>
        <div class="yuanzhang">赵汉民 <span>创伤骨科副主任</span></div>
        <a href="keshi_jianjie.php?id=125"><div class="suoshulei">进入创伤骨科</div></a>
        <div class="xq_zhicheng">副主任医师</div>
        <div class="xq_content">擅长：足踝外科、儿童骨科、运动系统创伤。</div>
        <div class="xq_xiangxi_jieshao_xq">副主任医师。专业擅长：足踝外科；从事临床工作十余年。</div>
        <footer>网站地图 采购公告</footer>
        """

        detail = parse_ny5y_detail(html, {})

        self.assertEqual(detail["name"], "赵汉民")
        self.assertEqual(detail["department"], "创伤骨科")
        self.assertEqual(detail["title_field"], "副主任医师")
        self.assertEqual(detail["specialty"], "足踝外科、儿童骨科、运动系统创伤。")
        self.assertEqual(detail["specialty_raw"], "擅长：足踝外科、儿童骨科、运动系统创伤。")
        self.assertIn("从事临床工作十余年", detail["profile_text"])
        for pollution in ["医院首页", "联系我们", "网站地图", "采购公告"]:
            self.assertNotIn(pollution, detail["profile_text"])

    def test_honor_category_is_not_used_as_department(self) -> None:
        html = """
        <div class="yuanzhang">黄艺洪 <span>门诊部副主任（主持工作）</span></div>
        <div class="suoshulei">岭南名医</div>
        <div class="xq_zhicheng">主任医师、岭南名医</div>
        <div class="xq_xiangxi_jieshao_xq">擅长脑血管病诊疗。</div>
        """

        detail = parse_ny5y_detail(html, {})

        self.assertEqual(detail["name"], "黄艺洪")
        self.assertEqual(detail["department"], "")
        self.assertIn("岭南名医", detail["title_field"])

    def test_missing_explicit_specialty_stays_empty(self) -> None:
        html = """
        <div class="yuanzhang">无专长医生</div>
        <div class="suoshulei">进入全科</div>
        <div class="xq_zhicheng">医师</div>
        <div class="xq_xiangxi_jieshao_xq">长期从事临床工作。</div>
        """

        detail = parse_ny5y_detail(html, {})

        self.assertEqual(detail["specialty"], "")
        self.assertEqual(detail["specialty_raw"], "")

    def test_full_append_gate_runs_before_master_write(self) -> None:
        rows = [
            {
                "姓名": f"医生{doctor_id}",
                "科室_分类页": "全科",
                "擅长诊疗方向摘录": "疾病规范诊疗。",
                "职称身份原文": "主任医师",
                "亮眼经历线索": "",
                "来源链接": f"http://www.ny5y.cn/yisheng_xq.php?id={doctor_id}",
                "异常提示": "",
            }
            for doctor_id in range(1, 135)
        ]
        rows[-1].update(
            {
                "姓名": "黄艺洪",
                "科室_分类页": "",
                "职称身份原文": "主任医师、岭南名医",
                "亮眼经历线索": "岭南名医",
                "异常提示": "科室需人工复核",
            }
        )
        payload = {
            "meta": {
                "unique_doctor_count": 134,
                "unique_candidate_count": 134,
                "candidate_membership_count": 213,
                "cross_entry_duplicate_count": 79,
                "category_error_count": 0,
                "detail_error_count": 0,
                "excluded_non_doctor_count": 0,
                "entry_candidate_counts": {
                    self.ENTRY_MAIN: 133,
                    self.ENTRY_LINGNAN: 80,
                },
            },
            "rows": rows,
        }

        validate_ny5y_full_append(payload)
        payload["meta"]["unique_doctor_count"] = 133
        with self.assertRaisesRegex(RuntimeError, "医生记录预期 134，实际 133"):
            validate_ny5y_full_append(payload)

    def test_collect_generic_returns_complete_ny5y_payload(self) -> None:
        shared_ids = list(range(1, 80))
        main_ids = shared_ids + list(range(80, 134))
        lingnan_ids = shared_ids + [134]

        def list_html(ids: list[int]) -> str:
            return "".join(
                f'<a href="yisheng_xq.php?id={doctor_id}">医生{doctor_id}</a>'
                for doctor_id in ids
            )

        entry_html = {
            self.ENTRY_MAIN: list_html(main_ids),
            self.ENTRY_LINGNAN: list_html(lingnan_ids),
        }

        def fake_fetch(_session: object, url: str, retries: int = 3) -> tuple[int, str, str]:
            del retries
            if url in entry_html:
                return 200, entry_html[url], ""
            doctor_id = int(url.rsplit("=", 1)[-1])
            department = f"科室{doctor_id % 10}"
            return (
                200,
                f"""
                <div class="yuanzhang">医生{doctor_id}</div>
                <div class="suoshulei">进入{department}</div>
                <div class="xq_zhicheng">主任医师</div>
                <div class="xq_content">疾病规范诊疗。</div>
                <div class="xq_xiangxi_jieshao_xq">长期从事临床工作。</div>
                """,
                "",
            )

        target = HospitalTarget(
            city="广州市",
            hospital="南方医科大学第五附属医院",
            homepage="http://www.ny5y.cn/",
            entry_url=self.ENTRY_MAIN,
            difficulty="A-优先自动采集",
            review="确认可采集",
            adapter_id="ny5y_official_expert",
            entry_urls=(self.ENTRY_MAIN, self.ENTRY_LINGNAN),
            ledger_entry_url=self.ENTRY_MAIN,
        )
        with (
            patch("collect_official_doctors_batch.create_official_session", return_value=object()),
            patch("collect_official_doctors_batch.collect_existing_profile_links", return_value=set()),
            patch("collect_official_doctors_batch.fetch", side_effect=fake_fetch),
            patch("collect_official_doctors_batch.time.sleep", return_value=None),
        ):
            payload = collect_generic(target, "2026-08-12", max_doctors=10, max_pages=5)

        self.assertEqual(payload["meta"]["entry_candidate_counts"][self.ENTRY_MAIN], 133)
        self.assertEqual(payload["meta"]["entry_candidate_counts"][self.ENTRY_LINGNAN], 80)
        self.assertEqual(payload["meta"]["candidate_membership_count"], 213)
        self.assertEqual(payload["meta"]["unique_candidate_count"], 134)
        self.assertEqual(payload["meta"]["cross_entry_duplicate_count"], 79)
        self.assertEqual(payload["meta"]["sample_entry_categories"], ["专家风采", "岭南名医"])
        self.assertEqual([item["list_page_count"] for item in payload["entry_reconnaissance"]], [1, 1])
        self.assertEqual(len(payload["cross_entry_duplicates"]), 79)
        self.assertEqual(len(payload["rows"]), 10)
        self.assertGreaterEqual(len({row["科室_分类页"] for row in payload["rows"]}), 5)
        self.assertTrue(
            all(
                row["来源链接"].startswith("http://www.ny5y.cn/yisheng_xq.php?id=")
                for row in payload["rows"]
            )
        )
        lingnan_row = next(row for row in payload["rows"] if row["采集入口"] == self.ENTRY_LINGNAN)
        self.assertNotEqual(lingnan_row["科室_分类页"], "岭南名医")
        self.assertIn("岭南名医", lingnan_row["亮眼经历线索"])


class Gdzy5413OfficialSpecialistTests(unittest.TestCase):
    ENTRY_FAMOUS = "https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850"
    ENTRY_EXPERTS = "https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850"

    def test_entry_and_detail_scope_are_strict(self) -> None:
        self.assertEqual(gdzy5413_entry_kind(self.ENTRY_FAMOUS), "851")
        self.assertEqual(gdzy5413_entry_kind(self.ENTRY_EXPERTS), "852")
        self.assertEqual(dedicated_adapter_for(self.ENTRY_FAMOUS), "gdzy5413_official_specialist")
        self.assertEqual(
            gdzy5413_detail_id("https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=1290"),
            "1290",
        )
        self.assertEqual(
            generic_detail_identity("https://gdzy5413.com/main/doctor/specialist.aspx?typeid=1290"),
            "gdzy5413:1290",
        )
        ksdoctor_url = (
            "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?"
            "bid=22&typeid=20&cid=22&ksid=20&id=47"
        )
        self.assertEqual(gdzy5413_ksdoctor_detail_id(ksdoctor_url), "47")
        self.assertEqual(generic_detail_identity(ksdoctor_url), "gdzy5413:ksdoctor:47")
        self.assertTrue(matches_generic_directory_detail_url(self.ENTRY_EXPERTS, ksdoctor_url))
        for invalid in [
            "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?ksid=1&id=1290",
            "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=23&ksid=20&id=47",
            "https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=1290&extra=1",
            "https://example.com/main/doctor/specialist.aspx?typeid=1290",
        ]:
            with self.subTest(invalid=invalid):
                self.assertFalse(matches_generic_directory_detail_url(self.ENTRY_FAMOUS, invalid))

    def test_directory_uses_card_fields_and_typeid_identity(self) -> None:
        html = """
        <li class="xinyutitle1">
          <div class="doc_img"><a href="doctor/specialist.aspx?typeid=634"></a></div>
          <div class="docnameall">吕 雄</div>
          <div class="docjich">内分泌科主任、主任中医师、教授</div>
          <a href="doctor/specialist.aspx?typeid=634">了解详情</a>
        </li>
        <a href="ks/templet2/ksdoctorinfo.aspx?ksid=1&id=634">另一模板</a>
        """

        rows = discover_generic_detail_links(html, self.ENTRY_FAMOUS, self.ENTRY_FAMOUS)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "吕雄")
        self.assertEqual(rows[0]["department"], "内分泌科")
        self.assertEqual(rows[0]["list_title"], "内分泌科主任、主任中医师、教授")

    def test_852_directory_uses_explicit_department_and_strict_ksdoctor_urls(self) -> None:
        html = """
        <div class="contentinfo">
          <div class="ks_title">心血管科</div>
          <div class="pudocname">
            <a href="ks/templet2/ksdoctorinfo.aspx?bid=22&amp;typeid=20&amp;cid=22&amp;ksid=20&amp;id=47">王 清 海</a>
          </div>
        </div>
        <a href="ks/templet2/ksdoctorinfo.aspx?ksid=1&amp;id=10">参数不完整</a>
        """

        rows = discover_generic_detail_links(html, self.ENTRY_EXPERTS, self.ENTRY_EXPERTS)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "王清海")
        self.assertEqual(rows[0]["department"], "心血管科")
        self.assertEqual(gdzy5413_ksdoctor_detail_id(rows[0]["source_link"]), "47")

    def test_detail_dom_ignores_generic_title_and_uses_explicit_department_evidence(self) -> None:
        html = """
        <html><head><title>广东省第二中医院--广东省中医药工程技术研究院</title></head><body>
          <nav>医院首页 新闻动态 招标公告</nav>
          <div id="news_info_plAll"><div class="news_info_s">
            范德辉，主任中医师、二级教授，广东省第二中医院针灸康复科五区区长。
            主持科研课题多项。擅长治疗：中风病、颈椎病及各种创伤术后康复等。
          </div></div>
          <footer>网站地图 采购公告</footer>
        </body></html>
        """

        detail = parse_gdzy5413_detail(
            html,
            {"name": "范德辉", "list_title": "广东省名中医、主任中医师、针康五区区长"},
        )

        self.assertEqual(detail["name"], "范德辉")
        self.assertEqual(detail["department"], "针灸康复科五区")
        self.assertIn("中风病", detail["specialty"])
        self.assertIn("主持科研课题多项", detail["profile_text"])
        self.assertNotIn("招标公告", detail["profile_text"])

    def test_ksdoctor_detail_uses_breadcrumb_and_labeled_sections(self) -> None:
        html = """
        <div class="newslistbg_m_c">
          <div class="typeall_right">您现在所在的位置：官网&gt;科室列表&gt;临床科室&gt;内科&gt;心血管科&gt;专家介绍&gt;</div>
          <div>【基本资料】 姓名：王清海 职称：主任中医师、教授、博士生导师 擅长：中医治疗高血压、冠心病。</div>
          <div>【医生简介】 广东省名中医，承担省部级科研课题多项。</div>
          <div>【出诊安排】 星期一上午</div>
        </div>
        """

        detail = parse_gdzy5413_ksdoctor_detail(html, {"name": "王清海", "department": "心血管科"})

        self.assertEqual(detail["name"], "王清海")
        self.assertEqual(detail["department"], "心血管科")
        self.assertEqual(detail["title_field"], "主任中医师、教授、博士生导师")
        self.assertEqual(detail["specialty"], "中医治疗高血压、冠心病。")
        self.assertIn("承担省部级科研课题", detail["profile_text"])
        self.assertNotIn("星期一", detail["profile_text"])

    def test_trial2_selection_includes_duplicate_group_and_baiyun_identity(self) -> None:
        items = [
            {"name": "黄培红", "department": "心血管科", "source_link": "u125"},
            {"name": "黄培红", "department": "心血管科", "source_link": "u658"},
            {"name": "白云医生", "department": "白云院区骨科", "source_link": "u749"},
            {"name": "妇科医生", "department": "妇科", "source_link": "u1"},
            {"name": "儿科医生", "department": "儿科", "source_link": "u2"},
        ]

        selected = select_gdzy5413_trial2_items(items, 4)

        self.assertEqual(len({item["name"] for item in selected}), 4)
        self.assertEqual(sum(1 for item in selected if item["name"] == "黄培红"), 2)
        self.assertTrue(any("白云院区" in item["department"] for item in selected))

    def test_full_detail_expansion_keeps_all_same_name_links(self) -> None:
        items = [
            {"name": "王清海", "source_link": "u47"},
            {"name": "张三", "source_link": "u1"},
            {"name": "王清海", "source_link": "u598"},
        ]

        expanded = expand_gdzy5413_full_detail_items(items)

        self.assertEqual([item["source_link"] for item in expanded], ["u47", "u598", "u1"])

    def test_identity_merge_chooses_richest_link_and_combines_departments(self) -> None:
        sparse = {
            "姓名": "黄培红",
            "科室_分类页": "特诊室",
            "科室_列表卡片": "特诊室",
            "职称身份原文": "副主任中医师、医学博士",
            "擅长诊疗方向摘录": "心力衰竭、冠心病、高血压。",
            "详情正文摘录": "",
            "来源链接": "u658",
            "异常提示": "",
        }
        rich = {
            **sparse,
            "科室_分类页": "心血管科",
            "科室_列表卡片": "心血管科",
            "详情正文摘录": "副主任中医师，医学博士，主要研究方向为心血管急重症的诊治，擅长心力衰竭、冠心病、高血压。",
            "来源链接": "u125",
        }

        self.assertTrue(gdzy5413_rows_same_identity(sparse, rich))
        merged, reconciliation = merge_gdzy5413_identity_rows([sparse, rich])

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["来源链接"], "u125")
        self.assertEqual(merged[0]["科室_分类页"], "特诊室、心血管科")
        self.assertEqual(merged[0]["职称身份原文"], "副主任中医师、医学博士")
        self.assertEqual(reconciliation[0]["merged_source_links"], ["u658"])
        self.assertEqual(reconciliation[0]["resolution"], "同一人归并")

    def test_identity_merge_keeps_primary_title_and_flags_title_mismatch(self) -> None:
        secondary = {
            "姓名": "张医生",
            "科室_分类页": "门诊部",
            "科室_列表卡片": "门诊部",
            "职称_关键词": "主任医师、教授",
            "职称身份原文": "主任医师、教授、硕士研究生导师",
            "擅长诊疗方向摘录": "高血压、冠心病。",
            "详情正文摘录": "",
            "来源链接": "u2",
            "异常提示": "",
        }
        primary = {
            **secondary,
            "科室_分类页": "心血管科",
            "科室_列表卡片": "心血管科",
            "职称_关键词": "主任医师",
            "职称身份原文": "主任医师",
            "详情正文摘录": "长期从事心血管临床工作，擅长高血压、冠心病诊治。",
            "来源链接": "u1",
        }

        merged, _ = merge_gdzy5413_identity_rows([secondary, primary])

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["来源链接"], "u1")
        self.assertEqual(merged[0]["职称身份原文"], "主任医师")
        self.assertEqual(merged[0]["职称_关键词"], "主任医师")
        self.assertIn("多详情职称不一致", merged[0]["异常提示"])

    def test_full_append_gate_requires_complete_authorized_reconciliation(self) -> None:
        specialist_links = [
            f"https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid={value}"
            for value in range(1, 22)
        ]
        ksdoctor_links = [
            "https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?"
            f"bid=81&typeid=1&cid=81&ksid=1&id={value}"
            for value in range(1, 347)
        ]
        relation_links = specialist_links + ksdoctor_links
        rows = [
            {
                "医院": "广东省第二中医院",
                "姓名": f"医生{value}",
                "职称_关键词": "主任医师",
                "职称身份原文": "主任医师",
                "擅长诊疗方向摘录": "",
                "来源链接": relation_links[value],
            }
            for value in range(290)
        ]
        reconciliation = [
            {
                "primary_source_link": relation_links[value],
                "merged_source_links": relation_links[290:] if value == 0 else [],
                "relation_count": 78 if value == 0 else 1,
            }
            for value in range(290)
        ]
        payload = {
            "meta": {
                "entry_candidate_counts": {
                    "https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850": 21,
                    "https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850": 346,
                },
                "gdzy5413_851_unique_name_count": 21,
                "gdzy5413_852_unique_name_count": 289,
                "gdzy5413_cross_mode_name_match_count": 20,
                "category_error_count": 0,
                "detail_error_count": 0,
            },
            "rows": rows,
            "gdzy5413_identity_reconciliation": reconciliation,
        }

        validate_gdzy5413_full_append(payload)
        payload["gdzy5413_identity_reconciliation"][0]["primary_source_link"] = (
            "https://example.com/not-authorized"
        )
        with self.assertRaisesRegex(RuntimeError, "非授权"):
            validate_gdzy5413_full_append(payload)

    def test_distinct_same_name_rows_are_retained_and_flagged(self) -> None:
        heart = {
            "姓名": "李桂明",
            "科室_分类页": "心血管科",
            "科室_列表卡片": "心血管科",
            "职称身份原文": "主任中医师",
            "擅长诊疗方向摘录": "高血压病、冠心病、心力衰竭。",
            "详情正文摘录": "长期从事心血管科临床工作。",
            "来源链接": "u317",
            "异常提示": "",
        }
        kidney = {
            **heart,
            "科室_分类页": "内科",
            "科室_列表卡片": "内科",
            "职称身份原文": "主任中医师、教授、硕士研究生导师",
            "擅长诊疗方向摘录": "慢性肾衰、急慢性肾炎、糖尿病肾病。",
            "详情正文摘录": "长期从事肾病临床工作。",
            "来源链接": "u553",
        }

        self.assertFalse(gdzy5413_rows_same_identity(heart, kidney))
        merged, reconciliation = merge_gdzy5413_identity_rows([heart, kidney])

        self.assertEqual(len(merged), 2)
        self.assertTrue(all("同名待甄别" in row["异常提示"] for row in merged))
        self.assertTrue(all(item["resolution"] == "同名待甄别" for item in reconciliation))

        master_rows, added, skipped, refreshed, duplicates = merge_rows_for_master(
            [], merged, preserve_existing=True
        )
        self.assertEqual(len(master_rows), 2)
        self.assertEqual((added, skipped, refreshed, duplicates), (2, 0, 0, 0))

    def test_collect_generic_records_scope_evidence_and_department_spread(self) -> None:
        famous_ids = list(range(1, 22))
        names = ["张三", "李四", "王五", "赵六", "陈明", "刘强", "杨敏", "黄芳", "周军", "吴静", "徐勇", "孙丽", "胡伟", "朱燕", "高峰", "林涛", "何娟", "郭鹏", "罗英", "梁杰", "宋梅"]
        departments = ["内分泌科", "妇科", "儿科", "肿瘤科", "呼吸科", "脑病科", "心血管科"]

        famous_html = "".join(
            (
                '<li class="xinyutitle1">'
                f'<div class="doc_img"><a href="doctor/specialist.aspx?typeid={doctor_id}"></a></div>'
                f'<div class="docnameall">{names[doctor_id - 1]}</div>'
                f'<div class="docjich">{departments[(doctor_id - 1) % len(departments)]}主任、主任医师</div>'
                "</li>"
            )
            for doctor_id in famous_ids
        )
        expert_names = names[:20] + [f"张{chr(0x4E00 + doctor_id)}" for doctor_id in range(21, 347)]
        expert_names[124] = "黄培红"
        expert_names[344] = "黄培红"
        expert_html = "".join(
            (
                '<div class="contentinfo">'
                f'<div class="ks_title">{"白云院区骨科" if doctor_id == 346 else departments[(doctor_id - 1) % len(departments)]}</div>'
                '<div class="pudocname">'
                f'<a href="ks/templet2/ksdoctorinfo.aspx?bid={doctor_id}&amp;typeid={doctor_id + 1000}&amp;cid={doctor_id}&amp;ksid={doctor_id + 1000}&amp;id={doctor_id}">'
                f'{expert_names[doctor_id - 1]}</a></div></div>'
            )
            for doctor_id in range(1, 347)
        )

        def fake_fetch(_session: object, url: str, retries: int = 3) -> tuple[int, str, str]:
            del retries
            if url == self.ENTRY_FAMOUS:
                return 200, famous_html, ""
            if url == self.ENTRY_EXPERTS:
                return 200, expert_html, ""
            doctor_id = int(url.rsplit("=", 1)[-1])
            department = departments[(doctor_id - 1) % len(departments)]
            if doctor_id == 346:
                department = "白云院区骨科"
            if "ksdoctorinfo" in url:
                name = expert_names[doctor_id - 1]
                return (
                    200,
                    '<div class="newslistbg_m_c">'
                    f'<div class="typeall_right">官网&gt;科室列表&gt;临床科室&gt;{department}&gt;专家介绍&gt;</div>'
                    f'<div>【基本资料】 姓名：{name} 职称：主任医师 擅长：{department}常见疾病。</div>'
                    f'<div>【医生简介】 {name}长期从事临床工作。</div><div>【出诊安排】</div></div>',
                    "",
                )
            return (
                200,
                f'<div id="news_info_plAll"><div class="news_info_s">擅长治疗：{department}常见疾病。</div></div>',
                "",
            )

        target = HospitalTarget(
            city="广州市",
            hospital="广东省第二中医院",
            homepage="https://www.gdzy5413.com/main/main.aspx",
            entry_url=self.ENTRY_FAMOUS,
            difficulty="A-优先自动采集",
            review="确认可采集",
            adapter_id="gdzy5413_official_specialist",
            entry_urls=(self.ENTRY_FAMOUS, self.ENTRY_EXPERTS),
            ledger_entry_url=self.ENTRY_FAMOUS,
        )
        with (
            patch("collect_official_doctors_batch.create_official_session", return_value=object()),
            patch("collect_official_doctors_batch.collect_existing_profile_links", return_value=set()),
            patch("collect_official_doctors_batch.fetch", side_effect=fake_fetch),
            patch("collect_official_doctors_batch.time.sleep", return_value=None),
        ):
            payload = collect_generic(
                target,
                "2026-08-12",
                max_doctors=10,
                max_pages=5,
                gdzy5413_trial2=True,
            )

        self.assertEqual(payload["meta"]["entry_candidate_counts"][self.ENTRY_FAMOUS], 21)
        self.assertEqual(payload["meta"]["entry_candidate_counts"][self.ENTRY_EXPERTS], 346)
        self.assertEqual(payload["meta"]["unique_candidate_count"], 367)
        self.assertEqual(payload["meta"]["excluded_non_doctor_count"], 0)
        self.assertEqual(payload["meta"]["out_of_scope_candidate_count"], 0)
        self.assertEqual(payload["entry_reconnaissance"][1]["out_of_scope_detail_count"], 0)
        self.assertIn(
            "院区/门诊均属同一法人实体授权范围",
            payload["entry_reconnaissance"][1]["independent_entity_check"],
        )
        self.assertEqual(payload["meta"]["gdzy5413_cross_mode_name_match_count"], 20)
        self.assertEqual(len(payload["rows"]), 10)
        self.assertGreaterEqual(len({row["科室_分类页"] for row in payload["rows"]}), 3)
        self.assertTrue(all(gdzy5413_ksdoctor_detail_id(row["来源链接"]) for row in payload["rows"]))
        self.assertTrue(all(not row["亮眼经历线索"].startswith("广东省第二中医院") for row in payload["rows"]))
        self.assertGreaterEqual(payload["meta"]["gdzy5413_trial2_baiyun_sample_count"], 1)
        self.assertGreaterEqual(payload["meta"]["gdzy5413_trial2_merged_identity_count"], 1)
        self.assertGreater(payload["meta"]["gdzy5413_trial2_sample_relation_count"], 10)
        payload["meta"]["department_coverage_count"] = len(
            {row["科室_分类页"] for row in payload["rows"]}
        )
        payload["meta"]["gdzy5413_852_unique_name_count"] = 289
        validate_gdzy5413_trial2(payload)
        merged_item = next(
            item
            for item in payload["gdzy5413_identity_reconciliation"]
            if item["merged_source_links"]
        )
        merged_item["merged_source_links"] = ["https://example.com/not-authorized"]
        with self.assertRaisesRegex(RuntimeError, "非授权 ksdoctorinfo"):
            validate_gdzy5413_trial2(payload)


class GenericFieldCleaningTests(unittest.TestCase):
    def test_department_is_truncated_before_profile_text(self) -> None:
        raw = "牙体牙髓病科一室 介绍：主任医师，博士，2015年毕业于南方医科大学。"
        self.assertEqual(clean_generic_department(raw), "牙体牙髓病科一室")

        html = f"""
        <main><h1>万蕾</h1><p>科室：{raw}</p><p>职称：主任医师</p></main>
        """
        detail = parse_generic_detail(html, {})
        self.assertEqual(detail["department"], "牙体牙髓病科一室")
        self.assertEqual(detail["department_polluted"], "yes")

    def test_specialty_requires_an_explicit_label(self) -> None:
        unlabelled = """
        <main><h1>何敏昭</h1><p>科室：牙体牙髓病科一室</p>
        <p>擅长龋病、牙髓病及根尖周疾病的诊疗工作。</p></main>
        """
        explicit = """
        <main><h1>万蕾</h1><p>科室：牙体牙髓病科一室</p>
        <p>擅长：龋病、牙髓病及根尖周疾病的诊疗。</p>
        <p>介绍：主任医师，长期从事口腔内科临床工作。</p></main>
        """

        self.assertEqual(parse_generic_detail(unlabelled, {})["specialty"], "")
        specialty = parse_generic_detail(explicit, {})["specialty"]
        self.assertIn("龋病", specialty)
        self.assertNotIn("介绍", specialty)
        self.assertNotIn("主任医师", specialty)

    def test_navigation_specialty_is_cleared_and_marked(self) -> None:
        html = """
        <main><h1>张伟炎</h1><p>科室：牙体牙髓病科一室</p>
        <p>擅长：你当前所在的位置：首页 &gt; 医疗服务 &gt; 专家介绍</p></main>
        """

        detail = parse_generic_detail(html, {})

        self.assertEqual(detail["specialty"], "")
        self.assertEqual(detail["specialty_navigation_polluted"], "yes")


class GenericRecordQualityTests(unittest.TestCase):
    def test_invalid_record_receives_no_priority_or_tags(self) -> None:
        priority, groups, tags = classify_generic_record(
            False,
            "感染 术后 康复 伤口 主任医师",
            ["主任医师"],
        )

        self.assertEqual(priority, "")
        self.assertEqual(groups, [])
        self.assertEqual(tags, [])

    def test_quality_warnings_cover_all_requested_pollution_types(self) -> None:
        valid, warnings = generic_record_quality(
            "就诊须知",
            "https://www.smukqyy.cn/doctor/166",
            "https://www.smukqyy.cn/section/364",
            {
                "department_polluted": "yes",
                "specialty_navigation_polluted": "yes",
            },
            {"department": "牙体牙髓病科一室 介绍：正文"},
        )

        self.assertFalse(valid)
        self.assertIn("非医生页面或姓名异常", warnings)
        self.assertIn("科室原文含正文，已清洗", warnings)
        self.assertIn("擅长原文含导航文本，已清空", warnings)


if __name__ == "__main__":
    unittest.main()
