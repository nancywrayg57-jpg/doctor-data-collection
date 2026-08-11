from __future__ import annotations

import sys
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

from collect_official_doctors_batch import (  # noqa: E402
    HospitalTarget,
    build_hospital_batches,
    classify_generic_record,
    clean_generic_department,
    discover_generic_detail_links,
    effective_entry_urls,
    generic_record_quality,
    looks_like_person_name,
    matches_generic_directory_detail_url,
    parse_generic_detail,
    round_robin_generic_items,
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
