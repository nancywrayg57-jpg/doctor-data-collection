from __future__ import annotations

import sys
import unittest
from pathlib import Path


WORK_DIR = Path(__file__).resolve().parents[1]
if str(WORK_DIR) not in sys.path:
    sys.path.insert(0, str(WORK_DIR))

from collect_official_doctors_batch import parse_generic_detail  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
