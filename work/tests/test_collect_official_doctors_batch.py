from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

from collect_official_doctors_batch import (  # noqa: E402
    HospitalTarget,
    build_hospital_batches,
    classify_generic_record,
    clean_generic_department,
    collect_generic,
    dedicated_adapter_for,
    discover_gdskin_excluded_links,
    discover_gdskin_postback_documents,
    discover_generic_detail_links,
    effective_entry_urls,
    extract_clean_highlights,
    generic_record_quality,
    generic_detail_identity,
    looks_like_person_name,
    matches_generic_directory_detail_url,
    merge_rows_for_master,
    ny5y_detail_id,
    ny5y_entry_kind,
    parse_generic_detail,
    parse_gdskin_detail,
    parse_ny5y_detail,
    round_robin_generic_items,
    validate_gdskin_full_append,
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
        <div class="xq_content">足踝外科、儿童骨科、运动系统创伤。</div>
        <div class="xq_xiangxi_jieshao_xq">副主任医师。专业擅长：足踝外科；从事临床工作十余年。</div>
        <footer>网站地图 采购公告</footer>
        """

        detail = parse_ny5y_detail(html, {})

        self.assertEqual(detail["name"], "赵汉民")
        self.assertEqual(detail["department"], "创伤骨科")
        self.assertEqual(detail["title_field"], "副主任医师")
        self.assertIn("足踝外科", detail["specialty"])
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
