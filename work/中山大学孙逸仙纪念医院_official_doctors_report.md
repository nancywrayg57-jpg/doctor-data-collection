---
类型: 全量采集归并审计报告
医院: 中山大学孙逸仙纪念医院
城市: 广州市
采集日期: 2026-08-13
来源范围: 医院官网
采集入口: https://www.gzsys.org.cn/doctor/592/search
适配器: gzsys_drupal_doctor_cards
---

# 中山大学孙逸仙纪念医院 官方医生全量采集归并审计报告

## 结论

本次全量采集只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集全量采集底表，共 658 位唯一医生；官网列表页原始卡片记录 664 条；读取入口分类 23 个；覆盖 69 个科室；详情页失败 1 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 中山大学孙逸仙纪念医院 |
| 官网首页 | https://www.gzsys.org.cn/home |
| 本轮医生入口 | https://www.gzsys.org.cn/doctor/592/search |
| 入口来源 | GitHub Issue #35（与官网入口台账一致） |
| 原台账医生入口 | https://www.gzsys.org.cn/doctor/592/search |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | D-待人工补官网 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
| 官网名医名师默认目录 | https://www.gzsys.org.cn/doctor/592/search | 医院官网 Drupal 公开医生目录 | 23 | 664 | 664 | 6 | 中山大学孙逸仙纪念医院 | 仅 .card-4-0 卡片授权；/node/<ID> 与 /doctor/<ID> 按数字 ID 去重 |

### 动态目录专项证据

- 医生分页/载入方式：页面声明的默认 All 查询 page=0..末页；不遍历搜索词或筛选组合
- 医生目录公开接口：不适用
- 医生详情公开接口：不适用
- 接口出处证据：不适用
- 院区/分组：0 个；科室分类：65 个
- 医生-科室关系：664 条
- 唯一详情 ID：664 个
- 有姓名详情 ID：664 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：664 个
- 同名不同详情 ID：0 组
- 非空/空科室块：664 / 0
- 院区/出诊点标签关系：无
- 跨院区/出诊点详情 ID：0 个

| 同名 | 详情 ID |
|---|---|
| 无 | 无 |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：664
- 跨入口去重后唯一候选：664
- 跨入口重复关系：0
- 试采覆盖入口分类：69 个（中医科、临床营养科、乳腺内科、乳腺外科、乳腺放疗专科、乳腺整形专科、乳腺肿瘤中心、乳腺诊断专科、健康体检中心、健康管理中心、儿科呼吸专科、儿科心血管专科、儿科神经内分泌专科、儿科肿瘤专科、儿科血液专科、儿科风湿免疫专科、全科医学科、全科医学科一科、全科医学科二科、内分泌内科、医工融合中心、口腔科、呼吸与危重症医学科、围产专科、基础与转化医学研究中心、外科、妇产科、妇科生殖内分泌专科、妇科肿瘤专科、小儿外科、康复医学科、心血管内科、心血管外科、急诊科、放射科介入专科、放射科影像专科、整形外科、新生儿及儿童重症专科、普通外科、普通妇科专科、树华乳腺癌研究中心、核医学科、检验科、泌尿外科、消化内科、生物治疗技术中心、甲状腺外科、病理科、皮肤科、眼科、神经外科、神经科、细胞分子诊断中心、耳鼻喉科、肝胆外科、肾内科、肿瘤内科、肿瘤科放疗专科、胃肠外科、胆胰外科、胸外科、药学部、血液内科、超声科、输血科、重症医学科、风湿免疫科、骨外科、麻醉科）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 无 | 无 | 无 |

## 中山大学孙逸仙纪念医院默认目录范围门禁

- 默认 All 目录：23 页、664 张严格 `.card-4-0` 卡片、664 个唯一数字 ID。
- 身份别名：`/node/<ID>` 与 `/doctor/<ID>` 只按同一数字 ID 去重；非卡片链接不构成授权详情。
- 页面筛选字典：科室 96、人才项目 4、导师资格 5、职称 33；仅解析留痕，不遍历组合或构造关键词。
- 纯护理排除：6 个；排除后合规候选 658 个。
- 详情清洗：排班 DOM 排除 479 个；排名/患者片段排除 51 个；正式字段排班写入 0、私用区字符 0。
- 普通公开会话：requests 常规重定向与站点自设 Cookie；无挑战求解、指纹模拟或绕过；本轮最终 Cookie 名称仅留痕为 `CT6T、CT6TS`。

### 逐 ID / 身份归并对账表

- 对账范围：664 个唯一数字 ID；正式身份 658 行；护理排除 6 行。
- 同一人归并：0 组；实质不同同名：0 组。

| 详情 ID | 姓名 | 裁决 | 来源链接 | 理由 |
|---|---|---|---|---|
| 14598 | 王庄斐 | 护理排除 | https://www.gzsys.org.cn/doctor/14598 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| 16987 | 徐静 | 护理排除 | https://www.gzsys.org.cn/node/16987 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| 18532 | 陈丽莉 | 护理排除 | https://www.gzsys.org.cn/node/18532 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| 14576 | 黄佩贤 | 护理排除 | https://www.gzsys.org.cn/doctor/14576 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| 16988 | 温作珍 | 护理排除 | https://www.gzsys.org.cn/node/16988 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| 15353 | 黄淑婷 | 护理排除 | https://www.gzsys.org.cn/doctor/15353 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| 14894 | 宋尔卫 | 正式行 | https://www.gzsys.org.cn/node/14894 | 无 |
| 14820 | 陈样新 | 正式行 | https://www.gzsys.org.cn/node/14820 | 无 |
| 14897 | 姚和瑞 | 正式行 | https://www.gzsys.org.cn/node/14897 | 无 |
| 14700 | 唐亚梅 | 正式行 | https://www.gzsys.org.cn/node/14700 | 无 |
| 15288 | 陈穗俊 | 正式行 | https://www.gzsys.org.cn/node/15288 | 无 |
| 15263 | 黄海 | 正式行 | https://www.gzsys.org.cn/node/15263 | 无 |
| 15255 | 黄健 | 正式行 | https://www.gzsys.org.cn/node/15255 | 无 |
| 14816 | 王景峰 | 正式行 | https://www.gzsys.org.cn/node/14816 | 无 |
| 15315 | 严励 | 正式行 | https://www.gzsys.org.cn/node/15315 | 无 |
| 14697 | 沈君 | 正式行 | https://www.gzsys.org.cn/node/14697 | 无 |
| 14811 | 詹俊 | 正式行 | https://www.gzsys.org.cn/doctor/14811 | 无 |
| 14896 | 刘强 | 正式行 | https://www.gzsys.org.cn/node/14896 | 无 |
| 14861 | 刘宜敏 | 正式行 | https://www.gzsys.org.cn/node/14861 | 无 |
| 14825 | 谢双伦 | 正式行 | https://www.gzsys.org.cn/node/14825 | 无 |
| 14805 | 林㼆 | 正式行 | https://www.gzsys.org.cn/node/14805 | 无 |
| 14630 | 黎阳 | 正式行 | https://www.gzsys.org.cn/node/14630 | 无 |
| 14611 | 曹林 | 正式行 | https://www.gzsys.org.cn/node/14611 | 无 |
| 14637 | 曹铭辉 | 正式行 | https://www.gzsys.org.cn/node/14637 | 无 |
| 14646 | 周敦华 | 正式行 | https://www.gzsys.org.cn/node/14646 | 无 |
| 14536 | 陈勍 | 正式行 | https://www.gzsys.org.cn/node/14536 | 无 |
| 14614 | 罗葆明 | 正式行 | https://www.gzsys.org.cn/node/14614 | 无 |
| 15260 | 郭正辉 | 正式行 | https://www.gzsys.org.cn/node/15260 | 无 |
| 14773 | 杨琼琼 | 正式行 | https://www.gzsys.org.cn/node/14773 | 无 |
| 14845 | 王铭辉 | 正式行 | https://www.gzsys.org.cn/node/14845 | 无 |
| 15269 | 马超 | 正式行 | https://www.gzsys.org.cn/node/15269 | 无 |
| 14671 | 许林锋 | 正式行 | https://www.gzsys.org.cn/node/14671 | 无 |
| 14903 | 苏士成 | 正式行 | https://www.gzsys.org.cn/node/14903 | 无 |
| 14561 | 李春海 | 正式行 | https://www.gzsys.org.cn/node/14561 | 无 |
| 14725 | 张立伐 | 正式行 | https://www.gzsys.org.cn/doctor/14725 | 无 |
| 14587 | 蒋龙元 | 正式行 | https://www.gzsys.org.cn/node/14587 | 无 |
| 15215 | 邓小耿 | 正式行 | https://www.gzsys.org.cn/node/15215 | 无 |
| 14721 | 吴卓 | 正式行 | https://www.gzsys.org.cn/node/14721 | 无 |
| 14617 | 李勇 | 正式行 | https://www.gzsys.org.cn/node/14617 | 无 |
| 15242 | 张红卫 | 正式行 | https://www.gzsys.org.cn/node/15242 | 无 |
| 14902 | 贾卫娟 | 正式行 | https://www.gzsys.org.cn/node/14902 | 无 |
| 14629 | 梁立阳 | 正式行 | https://www.gzsys.org.cn/node/14629 | 无 |
| 14680 | 黄霖 | 正式行 | https://www.gzsys.org.cn/node/14680 | 无 |
| 14668 | 林道炜 | 正式行 | https://www.gzsys.org.cn/node/14668 | 无 |
| 29131 | 李鹤平 | 正式行 | https://www.gzsys.org.cn/doctor/29131 | 无 |
| 15230 | 江山平 | 正式行 | https://www.gzsys.org.cn/node/15230 | 无 |
| 15238 | 陈亚进 | 正式行 | https://www.gzsys.org.cn/node/15238 | 无 |
| 15244 | 商昌珍 | 正式行 | https://www.gzsys.org.cn/node/15244 | 无 |
| 14898 | 龚畅 | 正式行 | https://www.gzsys.org.cn/node/14898 | 无 |
| 14732 | 陈慧 | 正式行 | https://www.gzsys.org.cn/node/14732 | 无 |
| 29537 | 刘天润 | 正式行 | https://www.gzsys.org.cn/doctor/29537 | 无 |
| 15201 | 郑俊猛 | 正式行 | https://www.gzsys.org.cn/node/15201 | 无 |
| 14675 | 戴冽 | 正式行 | https://www.gzsys.org.cn/node/14675 | 无 |
| 14592 | 蓝育青 | 正式行 | https://www.gzsys.org.cn/node/14592 | 无 |
| 14743 | 高梁斌 | 正式行 | https://www.gzsys.org.cn/node/14743 | 无 |
| 14651 | 丁悦 | 正式行 | https://www.gzsys.org.cn/node/14651 | 无 |
| 14658 | 刘安民 | 正式行 | https://www.gzsys.org.cn/node/14658 | 无 |
| 15203 | 张金明 | 正式行 | https://www.gzsys.org.cn/node/15203 | 无 |
| 14590 | 李劲松 | 正式行 | https://www.gzsys.org.cn/node/14590 | 无 |
| 14735 | 王亮春 | 正式行 | https://www.gzsys.org.cn/node/14735 | 无 |
| 15284 | 黄晓明 | 正式行 | https://www.gzsys.org.cn/node/15284 | 无 |
| 14681 | 张丙忠 | 正式行 | https://www.gzsys.org.cn/node/14681 | 无 |
| 14573 | 谭剑平 | 正式行 | https://www.gzsys.org.cn/node/14573 | 无 |
| 14539 | 陈庆瑜 | 正式行 | https://www.gzsys.org.cn/node/14539 | 无 |
| 14807 | 王凌云 | 正式行 | https://www.gzsys.org.cn/node/14807 | 无 |
| 14848 | 聂大年 | 正式行 | https://www.gzsys.org.cn/node/14848 | 无 |
| 14691 | 陈超刚 | 正式行 | https://www.gzsys.org.cn/node/14691 | 无 |
| 14599 | 王艺东 | 正式行 | https://www.gzsys.org.cn/node/14599 | 无 |
| 14687 | 张萌 | 正式行 | https://www.gzsys.org.cn/node/14687 | 无 |
| 14640 | 伍俊妍 | 正式行 | https://www.gzsys.org.cn/node/14640 | 无 |
| 14619 | 段朝晖 | 正式行 | https://www.gzsys.org.cn/node/14619 | 无 |
| 14588 | 金小岩 | 正式行 | https://www.gzsys.org.cn/node/14588 | 无 |
| 14812 | 张世能 | 正式行 | https://www.gzsys.org.cn/node/14812 | 无 |
| 14841 | 张惠忠 | 正式行 | https://www.gzsys.org.cn/node/14841 | 无 |
| 14771 | 石忠松 | 正式行 | https://www.gzsys.org.cn/node/14771 | 无 |
| 15320 | 李焱 | 正式行 | https://www.gzsys.org.cn/node/15320 | 无 |
| 15318 | 徐明彤 | 正式行 | https://www.gzsys.org.cn/node/15318 | 无 |
| 15222 | 李海刚 | 正式行 | https://www.gzsys.org.cn/node/15222 | 无 |
| 14788 | 褚忠华 | 正式行 | https://www.gzsys.org.cn/node/14788 | 无 |
| 14801 | 陈茵婷 | 正式行 | https://www.gzsys.org.cn/node/14801 | 无 |
| 14583 | 檀卫平 | 正式行 | https://www.gzsys.org.cn/node/14583 | 无 |
| 15199 | 华平 | 正式行 | https://www.gzsys.org.cn/node/15199 | 无 |
| 14673 | 徐安平 | 正式行 | https://www.gzsys.org.cn/node/14673 | 无 |
| 14636 | 王志 | 正式行 | https://www.gzsys.org.cn/node/14636 | 无 |
| 14855 | 李建军 | 正式行 | https://www.gzsys.org.cn/node/14855 | 无 |
| 14580 | 罗向阳 | 正式行 | https://www.gzsys.org.cn/node/14580 | 无 |
| 14905 | 汪颖 | 正式行 | https://www.gzsys.org.cn/node/14905 | 无 |
| 14827 | 罗年桑 | 正式行 | https://www.gzsys.org.cn/node/14827 | 无 |
| 14791 | 杨斌 | 正式行 | https://www.gzsys.org.cn/node/14791 | 无 |
| 14766 | 宋凤卿 | 正式行 | https://www.gzsys.org.cn/node/14766 | 无 |
| 14720 | 余涛 | 正式行 | https://www.gzsys.org.cn/node/14720 | 无 |
| 15270 | 伍少玲 | 正式行 | https://www.gzsys.org.cn/node/15270 | 无 |
| 14857 | 潘爱珍 | 正式行 | https://www.gzsys.org.cn/doctor/14857 | 无 |
| 14648 | 李玉娟 | 正式行 | https://www.gzsys.org.cn/node/14648 | 无 |
| 14554 | 郑东辉 | 正式行 | https://www.gzsys.org.cn/node/14554 | 无 |
| 14718 | 杨海云 | 正式行 | https://www.gzsys.org.cn/node/14718 | 无 |
| 17019 | 吴文睿 | 正式行 | https://www.gzsys.org.cn/node/17019 | 无 |
| 14852 | 谢双锋 | 正式行 | https://www.gzsys.org.cn/node/14852 | 无 |
| 31850 | 马剑达 | 正式行 | https://www.gzsys.org.cn/doctor/31850 | 无 |
| 15391 | 张静 | 正式行 | https://www.gzsys.org.cn/node/15391 | 无 |
| 14895 | 苏逢锡 | 正式行 | https://www.gzsys.org.cn/node/14895 | 无 |
| 14579 | 方建培 | 正式行 | https://www.gzsys.org.cn/node/14579 | 无 |
| 14526 | 林仲秋 | 正式行 | https://www.gzsys.org.cn/node/14526 | 无 |
| 15596 | 程桦 | 正式行 | https://www.gzsys.org.cn/node/15596 | 无 |
| 15322 | 杨川 | 正式行 | https://www.gzsys.org.cn/doctor/15322 | 无 |
| 14815 | 朱兆华 | 正式行 | https://www.gzsys.org.cn/doctor/14815 | 无 |
| 14814 | 钟英强 | 正式行 | https://www.gzsys.org.cn/doctor/14814 | 无 |
| 14803 | 黄开红 | 正式行 | https://www.gzsys.org.cn/node/14803 | 无 |
| 15259 | 谢文练 | 正式行 | https://www.gzsys.org.cn/doctor/15259 | 无 |
| 14849 | 尹松梅 | 正式行 | https://www.gzsys.org.cn/doctor/14849 | 无 |
| 14542 | 潘朝斌 | 正式行 | https://www.gzsys.org.cn/doctor/14542 | 无 |
| 15601 | 黄子通 | 正式行 | https://www.gzsys.org.cn/node/15601 | 无 |
| 14747 | 卢淮武 | 正式行 | https://www.gzsys.org.cn/node/14747 | 无 |
| 14585 | 黄科 | 正式行 | https://www.gzsys.org.cn/node/14585 | 无 |
| 15623 | 周力学 | 正式行 | https://www.gzsys.org.cn/node/15623 | 无 |
| 14692 | 智慧 | 正式行 | https://www.gzsys.org.cn/doctor/14692 | 无 |
| 14818 | 周淑娴 | 正式行 | https://www.gzsys.org.cn/node/14818 | 无 |
| 15326 | 刘丹 | 正式行 | https://www.gzsys.org.cn/doctor/15326 | 无 |
| 15327 | 张锦 | 正式行 | https://www.gzsys.org.cn/doctor/15327 | 无 |
| 15317 | 张少玲 | 正式行 | https://www.gzsys.org.cn/doctor/15317 | 无 |
| 15225 | 唐琼兰 | 正式行 | https://www.gzsys.org.cn/doctor/15225 | 无 |
| 14847 | 马丽萍 | 正式行 | https://www.gzsys.org.cn/node/14847 | 无 |
| 14806 | 王连源 | 正式行 | https://www.gzsys.org.cn/doctor/14806 | 无 |
| 14800 | 陈为宪 | 正式行 | https://www.gzsys.org.cn/doctor/14800 | 无 |
| 14809 | 于涛 | 正式行 | https://www.gzsys.org.cn/doctor/14809 | 无 |
| 14808 | 夏忠胜 | 正式行 | https://www.gzsys.org.cn/doctor/14808 | 无 |
| 15266 | 何旺 | 正式行 | https://www.gzsys.org.cn/node/15266 | 无 |
| 15258 | 姚友生 | 正式行 | https://www.gzsys.org.cn/node/15258 | 无 |
| 14726 | 覃丽君 | 正式行 | https://www.gzsys.org.cn/node/14726 | 无 |
| 14844 | 陈炬 | 正式行 | https://www.gzsys.org.cn/node/14844 | 无 |
| 14677 | 王建广 | 正式行 | https://www.gzsys.org.cn/node/14677 | 无 |
| 14524 | 黄东生 | 正式行 | https://www.gzsys.org.cn/node/14524 | 无 |
| 14647 | 方向韶 | 正式行 | https://www.gzsys.org.cn/doctor/14647 | 无 |
| 15594 | 许俭兴 | 正式行 | https://www.gzsys.org.cn/node/15594 | 无 |
| 15234 | 黄林洁 | 正式行 | https://www.gzsys.org.cn/node/15234 | 无 |
| 15233 | 梁瑞韵 | 正式行 | https://www.gzsys.org.cn/node/15233 | 无 |
| 15208 | 李文滨 | 正式行 | https://www.gzsys.org.cn/node/15208 | 无 |
| 14738 | 许吕宏 | 正式行 | https://www.gzsys.org.cn/node/14738 | 无 |
| 15246 | 肖治宇 | 正式行 | https://www.gzsys.org.cn/node/15246 | 无 |
| 15243 | 张磊 | 正式行 | https://www.gzsys.org.cn/node/15243 | 无 |
| 14908 | 陈凯 | 正式行 | https://www.gzsys.org.cn/node/14908 | 无 |
| 14906 | 刘洁琼 | 正式行 | https://www.gzsys.org.cn/node/14906 | 无 |
| 14862 | 白守民 | 正式行 | https://www.gzsys.org.cn/node/14862 | 无 |
| 14722 | 肖晓云 | 正式行 | https://www.gzsys.org.cn/node/14722 | 无 |
| 14682 | 李栋方 | 正式行 | https://www.gzsys.org.cn/node/14682 | 无 |
| 15211 | 林浩铭 | 正式行 | https://www.gzsys.org.cn/node/15211 | 无 |
| 14819 | 聂如琼 | 正式行 | https://www.gzsys.org.cn/node/14819 | 无 |
| 14684 | 欧阳颖 | 正式行 | https://www.gzsys.org.cn/node/14684 | 无 |
| 14593 | 王梅 | 正式行 | https://www.gzsys.org.cn/node/14593 | 无 |
| 15204 | 梁伟强 | 正式行 | https://www.gzsys.org.cn/node/15204 | 无 |
| 14742 | 范松 | 正式行 | https://www.gzsys.org.cn/node/14742 | 无 |
| 14596 | 谭国珍 | 正式行 | https://www.gzsys.org.cn/node/14596 | 无 |
| 15289 | 杨海弟 | 正式行 | https://www.gzsys.org.cn/node/15289 | 无 |
| 15283 | 张志钢 | 正式行 | https://www.gzsys.org.cn/node/15283 | 无 |
| 25002 | 师林 | 正式行 | https://www.gzsys.org.cn/node/25002 | 无 |
| 14724 | 王飞 | 正式行 | https://www.gzsys.org.cn/node/14724 | 无 |
| 15273 | 谭杰文 | 正式行 | https://www.gzsys.org.cn/node/15273 | 无 |
| 14708 | 余晓霞 | 正式行 | https://www.gzsys.org.cn/node/14708 | 无 |
| 14662 | 邱凯锋 | 正式行 | https://www.gzsys.org.cn/node/14662 | 无 |
| 14863 | 黄晓波 | 正式行 | https://www.gzsys.org.cn/node/14863 | 无 |
| 14676 | 陈锦武 | 正式行 | https://www.gzsys.org.cn/node/14676 | 无 |
| 14572 | 张睿 | 正式行 | https://www.gzsys.org.cn/node/14572 | 无 |
| 15223 | 王林 | 正式行 | https://www.gzsys.org.cn/node/15223 | 无 |
| 14665 | 吕军 | 正式行 | https://www.gzsys.org.cn/node/14665 | 无 |
| 14717 | 纪风涛 | 正式行 | https://www.gzsys.org.cn/node/14717 | 无 |
| 14653 | 傅艳妮 | 正式行 | https://www.gzsys.org.cn/node/14653 | 无 |
| 14546 | 罗晓红 | 正式行 | https://www.gzsys.org.cn/node/14546 | 无 |
| 15593 | 黄绍良 | 正式行 | https://www.gzsys.org.cn/node/15593 | 无 |
| 15598 | 李文益 | 正式行 | https://www.gzsys.org.cn/node/15598 | 无 |
| 15228 | 李建国 | 正式行 | https://www.gzsys.org.cn/node/15228 | 无 |
| 14616 | 黄穗乔 | 正式行 | https://www.gzsys.org.cn/node/14616 | 无 |
| 14523 | 梁碧玲 | 正式行 | https://www.gzsys.org.cn/node/14523 | 无 |
| 14531 | 李国照 | 正式行 | https://www.gzsys.org.cn/doctor/14531 | 无 |
| 24800 | 杜国庆 | 正式行 | https://www.gzsys.org.cn/node/24800 | 无 |
| 15307 | 谢梅青 | 正式行 | https://www.gzsys.org.cn/node/15307 | 无 |
| 15241 | 陈涛 | 正式行 | https://www.gzsys.org.cn/node/15241 | 无 |
| 15240 | 闵军 | 正式行 | https://www.gzsys.org.cn/node/15240 | 无 |
| 15239 | 王捷 | 正式行 | https://www.gzsys.org.cn/node/15239 | 无 |
| 14910 | 聂燕 | 正式行 | https://www.gzsys.org.cn/node/14910 | 无 |
| 15620 | 杨冬梓 | 正式行 | https://www.gzsys.org.cn/node/15620 | 无 |
| 14817 | 伍卫 | 正式行 | https://www.gzsys.org.cn/node/14817 | 无 |
| 14821 | 刘品明 | 正式行 | https://www.gzsys.org.cn/doctor/14821 | 无 |
| 14824 | 张玉玲 | 正式行 | https://www.gzsys.org.cn/node/14824 | 无 |
| 25008 | 吴现瑞 | 正式行 | https://www.gzsys.org.cn/node/25008 | 无 |
| 15328 | 任萌 | 正式行 | https://www.gzsys.org.cn/node/15328 | 无 |
| 14581 | 黄花荣 | 正式行 | https://www.gzsys.org.cn/node/14581 | 无 |
| 14525 | 张建平 | 正式行 | https://www.gzsys.org.cn/node/14525 | 无 |
| 14570 | 刘颖琳 | 正式行 | https://www.gzsys.org.cn/doctor/14570 | 无 |
| 14799 | 陈其奎 | 正式行 | https://www.gzsys.org.cn/node/14799 | 无 |
| 15592 | 沙孝珍 | 正式行 | https://www.gzsys.org.cn/node/15592 | 无 |
| 15590 | 黄洪铮 | 正式行 | https://www.gzsys.org.cn/node/15590 | 无 |
| 15587 | 刘尚礼 | 正式行 | https://www.gzsys.org.cn/node/15587 | 无 |
| 14727 | 叶伟 | 正式行 | https://www.gzsys.org.cn/doctor/14727 | 无 |
| 14679 | 杨睿 | 正式行 | https://www.gzsys.org.cn/node/14679 | 无 |
| 14535 | 李卫平 | 正式行 | https://www.gzsys.org.cn/node/14535 | 无 |
| 15591 | 林吉惠 | 正式行 | https://www.gzsys.org.cn/node/15591 | 无 |
| 14685 | 黄志权 | 正式行 | https://www.gzsys.org.cn/doctor/14685 | 无 |
| 14529 | 陈伟良 | 正式行 | https://www.gzsys.org.cn/node/14529 | 无 |
| 15595 | 邢诒刚 | 正式行 | https://www.gzsys.org.cn/node/15595 | 无 |
| 15281 | 刘中霖 | 正式行 | https://www.gzsys.org.cn/node/15281 | 无 |
| 15275 | 陶恩祥 | 正式行 | https://www.gzsys.org.cn/node/15275 | 无 |
| 14723 | 彭英 | 正式行 | https://www.gzsys.org.cn/node/14723 | 无 |
| 14527 | 郭庆 | 正式行 | https://www.gzsys.org.cn/node/14527 | 无 |
| 14522 | 曾凡钦 | 正式行 | https://www.gzsys.org.cn/doctor/14522 | 无 |
| 15304 | 郑亿庆 | 正式行 | https://www.gzsys.org.cn/node/15304 | 无 |
| 21989 | 李晶 | 正式行 | https://www.gzsys.org.cn/node/21989 | 无 |
| 15333 | 王吉文 | 正式行 | https://www.gzsys.org.cn/node/15333 | 无 |
| 15311 | 李志花 | 正式行 | https://www.gzsys.org.cn/node/15311 | 无 |
| 15309 | 谢德荣 | 正式行 | https://www.gzsys.org.cn/node/15309 | 无 |
| 15232 | 陈瑞 | 正式行 | https://www.gzsys.org.cn/node/15232 | 无 |
| 14774 | 段小慧 | 正式行 | https://www.gzsys.org.cn/doctor/14774 | 无 |
| 14733 | 王丽娟 | 正式行 | https://www.gzsys.org.cn/node/14733 | 无 |
| 14744 | 姚婷婷 | 正式行 | https://www.gzsys.org.cn/node/14744 | 无 |
| 14683 | 徐宏贵 | 正式行 | https://www.gzsys.org.cn/doctor/14683 | 无 |
| 14666 | 周晖 | 正式行 | https://www.gzsys.org.cn/doctor/14666 | 无 |
| 14574 | 彭永排 | 正式行 | https://www.gzsys.org.cn/node/14574 | 无 |
| 14543 | 陈建宇 | 正式行 | https://www.gzsys.org.cn/node/14543 | 无 |
| 15428 | 杨雅平 | 正式行 | https://www.gzsys.org.cn/node/15428 | 无 |
| 15248 | 叶华 | 正式行 | https://www.gzsys.org.cn/node/15248 | 无 |
| 15247 | 张建龙 | 正式行 | https://www.gzsys.org.cn/node/15247 | 无 |
| 15245 | 曹君 | 正式行 | https://www.gzsys.org.cn/node/15245 | 无 |
| 14904 | 李顺荣 | 正式行 | https://www.gzsys.org.cn/doctor/14904 | 无 |
| 14909 | 吴畏 | 正式行 | https://www.gzsys.org.cn/node/14909 | 无 |
| 14865 | 邱幸生 | 正式行 | https://www.gzsys.org.cn/node/14865 | 无 |
| 14751 | 郝少云 | 正式行 | https://www.gzsys.org.cn/doctor/14751 | 无 |
| 14741 | 狄娜 | 正式行 | https://www.gzsys.org.cn/doctor/14741 | 无 |
| 14719 | 何展文 | 正式行 | https://www.gzsys.org.cn/doctor/14719 | 无 |
| 14669 | 陈耀庭 | 正式行 | https://www.gzsys.org.cn/node/14669 | 无 |
| 15341 | 陈晓莉 | 正式行 | https://www.gzsys.org.cn/node/15341 | 无 |
| 15343 | 李轶 | 正式行 | https://www.gzsys.org.cn/node/15343 | 无 |
| 15335 | 张清学 | 正式行 | https://www.gzsys.org.cn/node/15335 | 无 |
| 15336 | 王文军 | 正式行 | https://www.gzsys.org.cn/node/15336 | 无 |
| 15209 | 张锐 | 正式行 | https://www.gzsys.org.cn/node/15209 | 无 |
| 15214 | 刘建平 | 正式行 | https://www.gzsys.org.cn/node/15214 | 无 |
| 15210 | 许磊波 | 正式行 | https://www.gzsys.org.cn/node/15210 | 无 |
| 14835 | 林茂欢 | 正式行 | https://www.gzsys.org.cn/doctor/14835 | 无 |
| 14836 | 张海峰 | 正式行 | https://www.gzsys.org.cn/node/14836 | 无 |
| 14832 | 郑韶欣 | 正式行 | https://www.gzsys.org.cn/doctor/14832 | 无 |
| 14823 | 耿登峰 | 正式行 | https://www.gzsys.org.cn/doctor/14823 | 无 |
| 14822 | 杨莉 | 正式行 | https://www.gzsys.org.cn/doctor/14822 | 无 |
| 14582 | 麦友刚 | 正式行 | https://www.gzsys.org.cn/node/14582 | 无 |
| 15329 | 王川 | 正式行 | https://www.gzsys.org.cn/node/15329 | 无 |
| 15319 | 吴木潮 | 正式行 | https://www.gzsys.org.cn/doctor/15319 | 无 |
| 15323 | 郭颖 | 正式行 | https://www.gzsys.org.cn/node/15323 | 无 |
| 15324 | 劳国娟 | 正式行 | https://www.gzsys.org.cn/node/15324 | 无 |
| 15331 | 孙侃 | 正式行 | https://www.gzsys.org.cn/node/15331 | 无 |
| 14795 | 来伟 | 正式行 | https://www.gzsys.org.cn/node/14795 | 无 |
| 14793 | 赖东明 | 正式行 | https://www.gzsys.org.cn/doctor/14793 | 无 |
| 14584 | 吴葆菁 | 正式行 | https://www.gzsys.org.cn/doctor/14584 | 无 |
| 15628 | 闵筱辉 | 正式行 | https://www.gzsys.org.cn/doctor/15628 | 无 |
| 14900 | 饶南燕 | 正式行 | https://www.gzsys.org.cn/node/14900 | 无 |
| 14802 | 黄凤婷 | 正式行 | https://www.gzsys.org.cn/node/14802 | 无 |
| 14813 | 钟娃 | 正式行 | https://www.gzsys.org.cn/doctor/14813 | 无 |
| 14559 | 黎洪浩 | 正式行 | https://www.gzsys.org.cn/node/14559 | 无 |
| 14532 | 熊小强 | 正式行 | https://www.gzsys.org.cn/node/14532 | 无 |
| 15439 | 李锴文 | 正式行 | https://www.gzsys.org.cn/node/15439 | 无 |
| 15261 | 江春 | 正式行 | https://www.gzsys.org.cn/node/15261 | 无 |
| 15262 | 韩金利 | 正式行 | https://www.gzsys.org.cn/node/15262 | 无 |
| 15265 | 董文 | 正式行 | https://www.gzsys.org.cn/node/15265 | 无 |
| 14850 | 王秀菊 | 正式行 | https://www.gzsys.org.cn/node/14850 | 无 |
| 14853 | 李益清 | 正式行 | https://www.gzsys.org.cn/node/14853 | 无 |
| 15202 | 黄楷 | 正式行 | https://www.gzsys.org.cn/node/15202 | 无 |
| 34141 | 于水莲 | 正式行 | https://www.gzsys.org.cn/doctor/34141 | 无 |
| 20599 | 李丹 | 正式行 | https://www.gzsys.org.cn/node/20599 | 无 |
| 15219 | 刘生 | 正式行 | https://www.gzsys.org.cn/doctor/15219 | 无 |
| 15220 | 张弘 | 正式行 | https://www.gzsys.org.cn/node/15220 | 无 |
| 14842 | 谢绚 | 正式行 | https://www.gzsys.org.cn/node/14842 | 无 |
| 14745 | 莫颖倩 | 正式行 | https://www.gzsys.org.cn/node/14745 | 无 |
| 14638 | 肖剑晖 | 正式行 | https://www.gzsys.org.cn/node/14638 | 无 |
| 14776 | 艾福志 | 正式行 | https://www.gzsys.org.cn/node/14776 | 无 |
| 14746 | 叶记超 | 正式行 | https://www.gzsys.org.cn/doctor/14746 | 无 |
| 14701 | 彭焰 | 正式行 | https://www.gzsys.org.cn/node/14701 | 无 |
| 14678 | 宋卫东 | 正式行 | https://www.gzsys.org.cn/node/14678 | 无 |
| 14660 | 许杰 | 正式行 | https://www.gzsys.org.cn/node/14660 | 无 |
| 14562 | 马若凡 | 正式行 | https://www.gzsys.org.cn/node/14562 | 无 |
| 14765 | 王友元 | 正式行 | https://www.gzsys.org.cn/node/14765 | 无 |
| 14699 | 杨朝晖 | 正式行 | https://www.gzsys.org.cn/node/14699 | 无 |
| 14713 | 张彬 | 正式行 | https://www.gzsys.org.cn/node/14713 | 无 |
| 14540 | 常少海 | 正式行 | https://www.gzsys.org.cn/doctor/14540 | 无 |
| 14541 | 叶剑涛 | 正式行 | https://www.gzsys.org.cn/doctor/14541 | 无 |
| 15276 | 杨炼红 | 正式行 | https://www.gzsys.org.cn/node/15276 | 无 |
| 15279 | 梁嫣然 | 正式行 | https://www.gzsys.org.cn/node/15279 | 无 |
| 14739 | 李艺 | 正式行 | https://www.gzsys.org.cn/node/14739 | 无 |
| 14652 | 沈庆煜 | 正式行 | https://www.gzsys.org.cn/node/14652 | 无 |
| 14600 | 李梅 | 正式行 | https://www.gzsys.org.cn/node/14600 | 无 |
| 14758 | 鲁莎 | 正式行 | https://www.gzsys.org.cn/node/14758 | 无 |
| 14645 | 张军民 | 正式行 | https://www.gzsys.org.cn/doctor/14645 | 无 |
| 14595 | 陈明春 | 正式行 | https://www.gzsys.org.cn/node/14595 | 无 |
| 14537 | 李希清 | 正式行 | https://www.gzsys.org.cn/doctor/14537 | 无 |
| 14696 | 李莉 | 正式行 | https://www.gzsys.org.cn/node/14696 | 无 |
| 14703 | 杨正飞 | 正式行 | https://www.gzsys.org.cn/node/14703 | 无 |
| 15618 | 彭解人 | 正式行 | https://www.gzsys.org.cn/node/15618 | 无 |
| 15299 | 田鹏 | 正式行 | https://www.gzsys.org.cn/doctor/15299 | 无 |
| 15298 | 梁茂金 | 正式行 | https://www.gzsys.org.cn/doctor/15298 | 无 |
| 15296 | 韩萍 | 正式行 | https://www.gzsys.org.cn/doctor/15296 | 无 |
| 15282 | 邹华 | 正式行 | https://www.gzsys.org.cn/node/15282 | 无 |
| 15285 | 许耀东 | 正式行 | https://www.gzsys.org.cn/doctor/15285 | 无 |
| 15286 | 区永康 | 正式行 | https://www.gzsys.org.cn/doctor/15286 | 无 |
| 15287 | 关中 | 正式行 | https://www.gzsys.org.cn/doctor/15287 | 无 |
| 15292 | 刘翔 | 正式行 | https://www.gzsys.org.cn/node/15292 | 无 |
| 15300 | 蔡跃新 | 正式行 | https://www.gzsys.org.cn/node/15300 | 无 |
| 15301 | 梁发雅 | 正式行 | https://www.gzsys.org.cn/doctor/15301 | 无 |
| 15332 | 何志捷 | 正式行 | https://www.gzsys.org.cn/node/15332 | 无 |
| 15334 | 何清 | 正式行 | https://www.gzsys.org.cn/node/15334 | 无 |
| 15271 | 金冬梅 | 正式行 | https://www.gzsys.org.cn/node/15271 | 无 |
| 14856 | 黄启辉 | 正式行 | https://www.gzsys.org.cn/node/14856 | 无 |
| 14705 | 彭俊 | 正式行 | https://www.gzsys.org.cn/doctor/14705 | 无 |
| 34475 | 杨林槟 | 正式行 | https://www.gzsys.org.cn/doctor/34475 | 无 |
| 19853 | 黄迪 | 正式行 | https://www.gzsys.org.cn/node/19853 | 无 |
| 15496 | 陈旭 | 正式行 | https://www.gzsys.org.cn/node/15496 | 无 |
| 14769 | 吕立 | 正式行 | https://www.gzsys.org.cn/node/14769 | 无 |
| 14657 | 廖日房 | 正式行 | https://www.gzsys.org.cn/node/14657 | 无 |
| 14623 | 李国成 | 正式行 | https://www.gzsys.org.cn/node/14623 | 无 |
| 14624 | 刘春霞 | 正式行 | https://www.gzsys.org.cn/node/14624 | 无 |
| 15229 | 吕志强 | 正式行 | https://www.gzsys.org.cn/node/15229 | 无 |
| 14631 | 胡辉军 | 正式行 | https://www.gzsys.org.cn/doctor/14631 | 无 |
| 14551 | 钟镜联 | 正式行 | https://www.gzsys.org.cn/node/14551 | 无 |
| 15339 | 欧阳能勇 | 正式行 | https://www.gzsys.org.cn/node/15339 | 无 |
| 14760 | 郑明慧 | 正式行 | https://www.gzsys.org.cn/node/14760 | 无 |
| 14656 | 黄松音 | 正式行 | https://www.gzsys.org.cn/node/14656 | 无 |
| 14649 | 严海燕 | 正式行 | https://www.gzsys.org.cn/node/14649 | 无 |
| 14689 | 闫振文 | 正式行 | https://www.gzsys.org.cn/node/14689 | 无 |
| 15235 | 颛孙永勋 | 正式行 | https://www.gzsys.org.cn/node/15235 | 无 |
| 14698 | 孟哲 | 正式行 | https://www.gzsys.org.cn/node/14698 | 无 |
| 15627 | 沈昌理 | 正式行 | https://www.gzsys.org.cn/node/15627 | 无 |
| 15206 | 唐启彬 | 正式行 | https://www.gzsys.org.cn/node/15206 | 无 |
| 14833 | 张殷殷 | 正式行 | https://www.gzsys.org.cn/doctor/14833 | 无 |
| 14838 | 林永青 | 正式行 | https://www.gzsys.org.cn/node/14838 | 无 |
| 14834 | 邱琼 | 正式行 | https://www.gzsys.org.cn/doctor/14834 | 无 |
| 14829 | 方昶 | 正式行 | https://www.gzsys.org.cn/node/14829 | 无 |
| 14828 | 刘英梅 | 正式行 | https://www.gzsys.org.cn/doctor/14828 | 无 |
| 15325 | 梁颖 | 正式行 | https://www.gzsys.org.cn/doctor/15325 | 无 |
| 14804 | 李楚强 | 正式行 | https://www.gzsys.org.cn/node/14804 | 无 |
| 14810 | 于钟 | 正式行 | https://www.gzsys.org.cn/doctor/14810 | 无 |
| 14798 | 苏红 | 正式行 | https://www.gzsys.org.cn/doctor/14798 | 无 |
| 14756 | 彭新治 | 正式行 | https://www.gzsys.org.cn/doctor/14756 | 无 |
| 14736 | 冯敏 | 正式行 | https://www.gzsys.org.cn/doctor/14736 | 无 |
| 14843 | 陈柏深 | 正式行 | https://www.gzsys.org.cn/doctor/14843 | 无 |
| 14846 | 吴多光 | 正式行 | https://www.gzsys.org.cn/doctor/14846 | 无 |
| 14730 | 梁安靖 | 正式行 | https://www.gzsys.org.cn/doctor/14730 | 无 |
| 14750 | 梁衍灿 | 正式行 | https://www.gzsys.org.cn/doctor/14750 | 无 |
| 14667 | 伍虹 | 正式行 | https://www.gzsys.org.cn/doctor/14667 | 无 |
| 15297 | 陈仁辉 | 正式行 | https://www.gzsys.org.cn/doctor/15297 | 无 |
| 14729 | 朱颉 | 正式行 | https://www.gzsys.org.cn/doctor/14729 | 无 |
| 14768 | 侯婧瑛 | 正式行 | https://www.gzsys.org.cn/doctor/14768 | 无 |
| 15280 | 吕瑞妍 | 正式行 | https://www.gzsys.org.cn/node/15280 | 无 |
| 14754 | 容小明 | 正式行 | https://www.gzsys.org.cn/node/14754 | 无 |
| 14755 | 潘经锐 | 正式行 | https://www.gzsys.org.cn/node/14755 | 无 |
| 14759 | 何蕾 | 正式行 | https://www.gzsys.org.cn/node/14759 | 无 |
| 15272 | 庄志强 | 正式行 | https://www.gzsys.org.cn/doctor/15272 | 无 |
| 14858 | 易伟民 | 正式行 | https://www.gzsys.org.cn/doctor/14858 | 无 |
| 14860 | 罗丹峰 | 正式行 | https://www.gzsys.org.cn/doctor/14860 | 无 |
| 14710 | 杨涛 | 正式行 | https://www.gzsys.org.cn/doctor/14710 | 无 |
| 15321 | 薛声能 | 正式行 | https://www.gzsys.org.cn/doctor/15321 | 无 |
| 15221 | 沈溪明 | 正式行 | https://www.gzsys.org.cn/node/15221 | 无 |
| 14797 | 曾志勇 | 正式行 | https://www.gzsys.org.cn/doctor/14797 | 无 |
| 14550 | 刘朗 | 正式行 | https://www.gzsys.org.cn/doctor/14550 | 无 |
| 15256 | 林天歆 | 正式行 | https://www.gzsys.org.cn/node/15256 | 无 |
| 15205 | 刘超 | 正式行 | https://www.gzsys.org.cn/node/15205 | 无 |
| 15257 | 许可慰 | 正式行 | https://www.gzsys.org.cn/node/15257 | 无 |
| 19850 | 曾伟科 | 正式行 | https://www.gzsys.org.cn/doctor/19850 | 无 |
| 16976 | 林小玲 | 正式行 | https://www.gzsys.org.cn/doctor/16976 | 无 |
| 18541 | 袁萍 | 正式行 | https://www.gzsys.org.cn/doctor/18541 | 无 |
| 14831 | 雷娟 | 正式行 | https://www.gzsys.org.cn/node/14831 | 无 |
| 14826 | 韦育林 | 正式行 | https://www.gzsys.org.cn/doctor/14826 | 无 |
| 14830 | 袁沃亮 | 正式行 | https://www.gzsys.org.cn/doctor/14830 | 无 |
| 15388 | 林海燕 | 正式行 | https://www.gzsys.org.cn/node/15388 | 无 |
| 15624 | 丁红 | 正式行 | https://www.gzsys.org.cn/doctor/15624 | 无 |
| 15597 | 钟志坚 | 正式行 | https://www.gzsys.org.cn/doctor/15597 | 无 |
| 14851 | 吴裕丹 | 正式行 | https://www.gzsys.org.cn/doctor/14851 | 无 |
| 15607 | 梅少芬 | 正式行 | https://www.gzsys.org.cn/doctor/15607 | 无 |
| 15629 | 胡玉新 | 正式行 | https://www.gzsys.org.cn/doctor/15629 | 无 |
| 15218 | 梁九根 | 正式行 | https://www.gzsys.org.cn/doctor/15218 | 无 |
| 19849 | 杨泽宏 | 正式行 | https://www.gzsys.org.cn/node/19849 | 无 |
| 19851 | 张芳 | 正式行 | https://www.gzsys.org.cn/node/19851 | 无 |
| 19804 | 唐恬恬 | 正式行 | https://www.gzsys.org.cn/node/19804 | 无 |
| 17746 | 邱坤银 | 正式行 | https://www.gzsys.org.cn/node/17746 | 无 |
| 17010 | 刘昀昀 | 正式行 | https://www.gzsys.org.cn/node/17010 | 无 |
| 15609 | 冯华英 | 正式行 | https://www.gzsys.org.cn/doctor/15609 | 无 |
| 15442 | 李欣瑜 | 正式行 | https://www.gzsys.org.cn/doctor/15442 | 无 |
| 15460 | 石健庭 | 正式行 | https://www.gzsys.org.cn/node/15460 | 无 |
| 15396 | 林琳 | 正式行 | https://www.gzsys.org.cn/doctor/15396 | 无 |
| 15310 | 林显敢 | 正式行 | https://www.gzsys.org.cn/doctor/15310 | 无 |
| 15312 | 杨琼 | 正式行 | https://www.gzsys.org.cn/doctor/15312 | 无 |
| 15231 | 张蔚 | 正式行 | https://www.gzsys.org.cn/node/15231 | 无 |
| 15236 | 陈茗 | 正式行 | https://www.gzsys.org.cn/node/15236 | 无 |
| 14748 | 杨绮华 | 正式行 | https://www.gzsys.org.cn/doctor/14748 | 无 |
| 14706 | 王东烨 | 正式行 | https://www.gzsys.org.cn/doctor/14706 | 无 |
| 14711 | 潘恒 | 正式行 | https://www.gzsys.org.cn/doctor/14711 | 无 |
| 14571 | 陈志辽 | 正式行 | https://www.gzsys.org.cn/doctor/14571 | 无 |
| 14615 | 袁小平 | 正式行 | https://www.gzsys.org.cn/doctor/14615 | 无 |
| 14530 | 许晓矛 | 正式行 | https://www.gzsys.org.cn/doctor/14530 | 无 |
| 26682 | 黄拼搏 | 正式行 | https://www.gzsys.org.cn/node/26682 | 无 |
| 23701 | 陆艺文 | 正式行 | https://www.gzsys.org.cn/node/23701 | 无 |
| 23372 | 周振宇 | 正式行 | https://www.gzsys.org.cn/node/23372 | 无 |
| 20720 | 张岚 | 正式行 | https://www.gzsys.org.cn/node/20720 | 无 |
| 19809 | 罗旋 | 正式行 | https://www.gzsys.org.cn/node/19809 | 无 |
| 18533 | 丁淼 | 正式行 | https://www.gzsys.org.cn/node/18533 | 无 |
| 17020 | 吴荧宸 | 正式行 | https://www.gzsys.org.cn/node/17020 | 无 |
| 15606 | 杨泉林 | 正式行 | https://www.gzsys.org.cn/doctor/15606 | 无 |
| 15611 | 张玉兰 | 正式行 | https://www.gzsys.org.cn/doctor/15611 | 无 |
| 15507 | 赵菁华 | 正式行 | https://www.gzsys.org.cn/doctor/15507 | 无 |
| 15423 | 朱李玲 | 正式行 | https://www.gzsys.org.cn/node/15423 | 无 |
| 15430 | 龙腾飞 | 正式行 | https://www.gzsys.org.cn/doctor/15430 | 无 |
| 15446 | 陈圣福 | 正式行 | https://www.gzsys.org.cn/node/15446 | 无 |
| 15461 | 韦金星 | 正式行 | https://www.gzsys.org.cn/node/15461 | 无 |
| 15370 | 金亮 | 正式行 | https://www.gzsys.org.cn/doctor/15370 | 无 |
| 15377 | 李扬志 | 正式行 | https://www.gzsys.org.cn/doctor/15377 | 无 |
| 15382 | 张丽娜 | 正式行 | https://www.gzsys.org.cn/node/15382 | 无 |
| 15402 | 邓贺然 | 正式行 | https://www.gzsys.org.cn/doctor/15402 | 无 |
| 15408 | 陈捷 | 正式行 | https://www.gzsys.org.cn/node/15408 | 无 |
| 15409 | 陈冬梅 | 正式行 | https://www.gzsys.org.cn/doctor/15409 | 无 |
| 15412 | 侯乐乐 | 正式行 | https://www.gzsys.org.cn/doctor/15412 | 无 |
| 15366 | 陈亚肖 | 正式行 | https://www.gzsys.org.cn/node/15366 | 无 |
| 15305 | 翁梅英 | 正式行 | https://www.gzsys.org.cn/doctor/15305 | 无 |
| 15306 | 王良岸 | 正式行 | https://www.gzsys.org.cn/node/15306 | 无 |
| 15308 | 冯淑英 | 正式行 | https://www.gzsys.org.cn/doctor/15308 | 无 |
| 15249 | 张贺云 | 正式行 | https://www.gzsys.org.cn/node/15249 | 无 |
| 15252 | 何传超 | 正式行 | https://www.gzsys.org.cn/node/15252 | 无 |
| 15253 | 叶义标 | 正式行 | https://www.gzsys.org.cn/node/15253 | 无 |
| 15254 | 毛凯 | 正式行 | https://www.gzsys.org.cn/node/15254 | 无 |
| 14907 | 吴建南 | 正式行 | https://www.gzsys.org.cn/doctor/14907 | 无 |
| 14864 | 罗铭 | 正式行 | https://www.gzsys.org.cn/node/14864 | 无 |
| 14740 | 吴欢 | 正式行 | https://www.gzsys.org.cn/doctor/14740 | 无 |
| 14749 | 赵新保 | 正式行 | https://www.gzsys.org.cn/node/14749 | 无 |
| 14753 | 李平甘 | 正式行 | https://www.gzsys.org.cn/doctor/14753 | 无 |
| 14770 | 许晓琳 | 正式行 | https://www.gzsys.org.cn/doctor/14770 | 无 |
| 14693 | 欧冰 | 正式行 | https://www.gzsys.org.cn/node/14693 | 无 |
| 14533 | 潘景升 | 正式行 | https://www.gzsys.org.cn/doctor/14533 | 无 |
| 17458 | 邓冰清 | 正式行 | https://www.gzsys.org.cn/node/17458 | 无 |
| 17148 | 谢勇 | 正式行 | https://www.gzsys.org.cn/node/17148 | 无 |
| 17147 | 黄图城 | 正式行 | https://www.gzsys.org.cn/node/17147 | 无 |
| 16979 | 余先焕 | 正式行 | https://www.gzsys.org.cn/node/16979 | 无 |
| 15619 | 陈锡龙 | 正式行 | https://www.gzsys.org.cn/doctor/15619 | 无 |
| 15632 | 刁飞宇 | 正式行 | https://www.gzsys.org.cn/doctor/15632 | 无 |
| 15602 | 谭桂明 | 正式行 | https://www.gzsys.org.cn/doctor/15602 | 无 |
| 15616 | 苏浩彬 | 正式行 | https://www.gzsys.org.cn/doctor/15616 | 无 |
| 15554 | 丁林潇潇 | 正式行 | https://www.gzsys.org.cn/node/15554 | 无 |
| 15472 | 黄斐斐 | 正式行 | https://www.gzsys.org.cn/node/15472 | 无 |
| 15490 | 苏子焯 | 正式行 | https://www.gzsys.org.cn/node/15490 | 无 |
| 15493 | 付志强 | 正式行 | https://www.gzsys.org.cn/node/15493 | 无 |
| 15419 | 温主治 | 正式行 | https://www.gzsys.org.cn/node/15419 | 无 |
| 15421 | 黄佳 | 正式行 | https://www.gzsys.org.cn/doctor/15421 | 无 |
| 15422 | 吴雯静 | 正式行 | https://www.gzsys.org.cn/node/15422 | 无 |
| 15427 | 曾银朵 | 正式行 | https://www.gzsys.org.cn/node/15427 | 无 |
| 15444 | 潘萍 | 正式行 | https://www.gzsys.org.cn/doctor/15444 | 无 |
| 15466 | 赵健丽 | 正式行 | https://www.gzsys.org.cn/node/15466 | 无 |
| 15386 | 彭耀荣 | 正式行 | https://www.gzsys.org.cn/doctor/15386 | 无 |
| 15340 | 李琳 | 正式行 | https://www.gzsys.org.cn/doctor/15340 | 无 |
| 14837 | 麦憬霆 | 正式行 | https://www.gzsys.org.cn/doctor/14837 | 无 |
| 14839 | 陈煜阳 | 正式行 | https://www.gzsys.org.cn/doctor/14839 | 无 |
| 14840 | 袁桂仪 | 正式行 | https://www.gzsys.org.cn/doctor/14840 | 无 |
| 19810 | 叶剑虹 | 正式行 | https://www.gzsys.org.cn/node/19810 | 无 |
| 17001 | 蓝球生 | 正式行 | https://www.gzsys.org.cn/node/17001 | 无 |
| 15630 | 罗兴喜 | 正式行 | https://www.gzsys.org.cn/doctor/15630 | 无 |
| 15612 | 麦贤弟 | 正式行 | https://www.gzsys.org.cn/doctor/15612 | 无 |
| 15503 | 付帅 | 正式行 | https://www.gzsys.org.cn/node/15503 | 无 |
| 15420 | 张蜀宁 | 正式行 | https://www.gzsys.org.cn/doctor/15420 | 无 |
| 15467 | 张璟璐 | 正式行 | https://www.gzsys.org.cn/node/15467 | 无 |
| 15378 | 刘梅兰 | 正式行 | https://www.gzsys.org.cn/doctor/15378 | 无 |
| 15354 | 林小鸿 | 正式行 | https://www.gzsys.org.cn/node/15354 | 无 |
| 15316 | 肖辉盛 | 正式行 | https://www.gzsys.org.cn/doctor/15316 | 无 |
| 14790 | 伍衡 | 正式行 | https://www.gzsys.org.cn/doctor/14790 | 无 |
| 14792 | 刘璐 | 正式行 | https://www.gzsys.org.cn/doctor/14792 | 无 |
| 14794 | 曾育杰 | 正式行 | https://www.gzsys.org.cn/doctor/14794 | 无 |
| 14775 | 卫星 | 正式行 | https://www.gzsys.org.cn/node/14775 | 无 |
| 14702 | 陈晓彤 | 正式行 | https://www.gzsys.org.cn/node/14702 | 无 |
| 14712 | 刘玉昆 | 正式行 | https://www.gzsys.org.cn/doctor/14712 | 无 |
| 14555 | 甘小玲 | 正式行 | https://www.gzsys.org.cn/node/14555 | 无 |
| 29923 | 雍娟娟 | 正式行 | https://www.gzsys.org.cn/doctor/29923 | 无 |
| 15610 | 梅志勇 | 正式行 | https://www.gzsys.org.cn/doctor/15610 | 无 |
| 15441 | 朱玥 | 正式行 | https://www.gzsys.org.cn/node/15441 | 无 |
| 15450 | 林少建 | 正式行 | https://www.gzsys.org.cn/node/15450 | 无 |
| 15379 | 张碧红 | 正式行 | https://www.gzsys.org.cn/node/15379 | 无 |
| 15224 | 曾弘 | 正式行 | https://www.gzsys.org.cn/doctor/15224 | 无 |
| 14761 | 罗定远 | 正式行 | https://www.gzsys.org.cn/doctor/14761 | 无 |
| 22045 | 贺情情 | 正式行 | https://www.gzsys.org.cn/node/22045 | 无 |
| 17023 | 张国扬 | 正式行 | https://www.gzsys.org.cn/node/17023 | 无 |
| 15600 | 曾宪平 | 正式行 | https://www.gzsys.org.cn/doctor/15600 | 无 |
| 15473 | 赖义明 | 正式行 | https://www.gzsys.org.cn/node/15473 | 无 |
| 15387 | 曾乐祥 | 正式行 | https://www.gzsys.org.cn/node/15387 | 无 |
| 15414 | 朱定军 | 正式行 | https://www.gzsys.org.cn/doctor/15414 | 无 |
| 15417 | 范新祥 | 正式行 | https://www.gzsys.org.cn/doctor/15417 | 无 |
| 15267 | 刘皓 | 正式行 | https://www.gzsys.org.cn/node/15267 | 无 |
| 14854 | 肖洁 | 正式行 | https://www.gzsys.org.cn/doctor/14854 | 无 |
| 19807 | 梁石 | 正式行 | https://www.gzsys.org.cn/node/19807 | 无 |
| 17002 | 李佳佳 | 正式行 | https://www.gzsys.org.cn/node/17002 | 无 |
| 16981 | 陈志波 | 正式行 | https://www.gzsys.org.cn/node/16981 | 无 |
| 15608 | 余妙真 | 正式行 | https://www.gzsys.org.cn/doctor/15608 | 无 |
| 15475 | 陶俊 | 正式行 | https://www.gzsys.org.cn/node/15475 | 无 |
| 15449 | 徐振健 | 正式行 | https://www.gzsys.org.cn/doctor/15449 | 无 |
| 15360 | 梁佩芬 | 正式行 | https://www.gzsys.org.cn/node/15360 | 无 |
| 14586 | 翁文骏 | 正式行 | https://www.gzsys.org.cn/doctor/14586 | 无 |
| 14553 | 赖德源 | 正式行 | https://www.gzsys.org.cn/doctor/14553 | 无 |
| 14556 | 李劲高 | 正式行 | https://www.gzsys.org.cn/doctor/14556 | 无 |
| 14557 | 宛霞 | 正式行 | https://www.gzsys.org.cn/doctor/14557 | 无 |
| 17456 | 梁锦坚 | 正式行 | https://www.gzsys.org.cn/node/17456 | 无 |
| 15514 | 张一弛 | 正式行 | https://www.gzsys.org.cn/node/15514 | 无 |
| 15393 | 温鑫 | 正式行 | https://www.gzsys.org.cn/node/15393 | 无 |
| 15415 | 李谦华 | 正式行 | https://www.gzsys.org.cn/doctor/15415 | 无 |
| 15217 | 卢献平 | 正式行 | https://www.gzsys.org.cn/doctor/15217 | 无 |
| 14538 | 洪俊 | 正式行 | https://www.gzsys.org.cn/node/14538 | 无 |
| 30707 | 孙浩 | 正式行 | https://www.gzsys.org.cn/doctor/30707 | 无 |
| 30288 | 张帆 | 正式行 | https://www.gzsys.org.cn/doctor/30288 | 无 |
| 21906 | 李登 | 正式行 | https://www.gzsys.org.cn/node/21906 | 无 |
| 18011 | 傅国 | 正式行 | https://www.gzsys.org.cn/node/18011 | 无 |
| 16995 | 陈仲 | 正式行 | https://www.gzsys.org.cn/node/16995 | 无 |
| 15578 | 刘文宙 | 正式行 | https://www.gzsys.org.cn/doctor/15578 | 无 |
| 15524 | 张正政 | 正式行 | https://www.gzsys.org.cn/node/15524 | 无 |
| 15495 | 江川 | 正式行 | https://www.gzsys.org.cn/doctor/15495 | 无 |
| 15462 | 李长川 | 正式行 | https://www.gzsys.org.cn/doctor/15462 | 无 |
| 14674 | 陈燕涛 | 正式行 | https://www.gzsys.org.cn/doctor/14674 | 无 |
| 14714 | 唐勇 | 正式行 | https://www.gzsys.org.cn/node/14714 | 无 |
| 28311 | 欧阳乐平 | 正式行 | https://www.gzsys.org.cn/doctor/28311 | 无 |
| 25812 | 潘琪 | 正式行 | https://www.gzsys.org.cn/node/25812 | 无 |
| 25291 | 雷炳喜 | 正式行 | https://www.gzsys.org.cn/node/25291 | 无 |
| 25208 | 郑眉光 | 正式行 | https://www.gzsys.org.cn/node/25208 | 无 |
| 14772 | 王伟 | 正式行 | https://www.gzsys.org.cn/node/14772 | 无 |
| 14757 | 张善义 | 正式行 | https://www.gzsys.org.cn/node/14757 | 无 |
| 14763 | 翁胤仑 | 正式行 | https://www.gzsys.org.cn/node/14763 | 无 |
| 17016 | 汪延 | 正式行 | https://www.gzsys.org.cn/node/17016 | 无 |
| 15548 | 夏昕 | 正式行 | https://www.gzsys.org.cn/node/15548 | 无 |
| 15477 | 张佳琦 | 正式行 | https://www.gzsys.org.cn/doctor/15477 | 无 |
| 15502 | 肖小莲 | 正式行 | https://www.gzsys.org.cn/doctor/15502 | 无 |
| 14762 | 庄沛林 | 正式行 | https://www.gzsys.org.cn/node/14762 | 无 |
| 14686 | 刘墨 | 正式行 | https://www.gzsys.org.cn/node/14686 | 无 |
| 14589 | 郑美华 | 正式行 | https://www.gzsys.org.cn/node/14589 | 无 |
| 15351 | 张杰 | 正式行 | https://www.gzsys.org.cn/node/15351 | 无 |
| 15368 | 伍耀豪 | 正式行 | https://www.gzsys.org.cn/node/15368 | 无 |
| 15534 | 李红红 | 正式行 | https://www.gzsys.org.cn/node/15534 | 无 |
| 15535 | 徐永腾 | 正式行 | https://www.gzsys.org.cn/node/15535 | 无 |
| 15469 | 雷鸣 | 正式行 | https://www.gzsys.org.cn/node/15469 | 无 |
| 15392 | 王鸿轩 | 正式行 | https://www.gzsys.org.cn/node/15392 | 无 |
| 14639 | 黎祥喷 | 正式行 | https://www.gzsys.org.cn/node/14639 | 无 |
| 15613 | 林宝珠 | 正式行 | https://www.gzsys.org.cn/doctor/15613 | 无 |
| 15470 | 熊慧 | 正式行 | https://www.gzsys.org.cn/doctor/15470 | 无 |
| 15405 | 马坚池 | 正式行 | https://www.gzsys.org.cn/doctor/15405 | 无 |
| 15357 | 唐增奇 | 正式行 | https://www.gzsys.org.cn/node/15357 | 无 |
| 14695 | 曾颖 | 正式行 | https://www.gzsys.org.cn/doctor/14695 | 无 |
| 14715 | 罗益金 | 正式行 | https://www.gzsys.org.cn/doctor/14715 | 无 |
| 14597 | 毛越苹 | 正式行 | https://www.gzsys.org.cn/doctor/14597 | 无 |
| 16997 | 邓文婷 | 正式行 | https://www.gzsys.org.cn/node/16997 | 无 |
| 15520 | 陈越勃 | 正式行 | https://www.gzsys.org.cn/node/15520 | 无 |
| 15521 | 马赟 | 正式行 | https://www.gzsys.org.cn/node/15521 | 无 |
| 15443 | 林沛亮 | 正式行 | https://www.gzsys.org.cn/node/15443 | 无 |
| 15455 | 司瑜 | 正式行 | https://www.gzsys.org.cn/node/15455 | 无 |
| 15290 | 丁健慧 | 正式行 | https://www.gzsys.org.cn/doctor/15290 | 无 |
| 15291 | 陈秋坚 | 正式行 | https://www.gzsys.org.cn/doctor/15291 | 无 |
| 15294 | 党华 | 正式行 | https://www.gzsys.org.cn/node/15294 | 无 |
| 16983 | 周明根 | 正式行 | https://www.gzsys.org.cn/node/16983 | 无 |
| 19848 | 郭明炎 | 正式行 | https://www.gzsys.org.cn/node/19848 | 无 |
| 16986 | 梁建军 | 正式行 | https://www.gzsys.org.cn/node/16986 | 无 |
| 14654 | 曾静贤 | 正式行 | https://www.gzsys.org.cn/doctor/14654 | 无 |
| 14610 | 何波 | 正式行 | https://www.gzsys.org.cn/doctor/14610 | 无 |
| 14612 | 徐忠东 | 正式行 | https://www.gzsys.org.cn/doctor/14612 | 无 |
| 18242 | 吴文霞 | 正式行 | https://www.gzsys.org.cn/node/18242 | 无 |
| 15425 | 刘淑琼 | 正式行 | https://www.gzsys.org.cn/doctor/15425 | 无 |
| 15448 | 包金兰 | 正式行 | https://www.gzsys.org.cn/node/15448 | 无 |
| 14688 | 温立强 | 正式行 | https://www.gzsys.org.cn/doctor/14688 | 无 |
| 24064 | 黎江 | 正式行 | https://www.gzsys.org.cn/node/24064 | 无 |
| 32104 | 林建子 | 正式行 | https://www.gzsys.org.cn/doctor/32104 | 无 |
| 14767 | 王鹏 | 正式行 | https://www.gzsys.org.cn/doctor/14767 | 无 |
| 14694 | 林茵 | 正式行 | https://www.gzsys.org.cn/node/14694 | 无 |
| 14621 | 吴庆欢 | 正式行 | https://www.gzsys.org.cn/node/14621 | 无 |
| 14626 | 陈楚雄 | 正式行 | https://www.gzsys.org.cn/node/14626 | 无 |
| 14620 | 吕永丰 | 正式行 | https://www.gzsys.org.cn/node/14620 | 无 |
| 14867 | 吴少焜 | 正式行 | https://www.gzsys.org.cn/node/14867 | 无 |
| 19852 | 杨亚波 | 正式行 | https://www.gzsys.org.cn/node/19852 | 无 |
| 16989 | 王英 | 正式行 | https://www.gzsys.org.cn/node/16989 | 无 |
| 14690 | 曾华 | 正式行 | https://www.gzsys.org.cn/doctor/14690 | 无 |
| 14709 | 刘晓强 | 正式行 | https://www.gzsys.org.cn/doctor/14709 | 无 |
| 14661 | 林向华 | 正式行 | https://www.gzsys.org.cn/doctor/14661 | 无 |
| 14664 | 陈梅 | 正式行 | https://www.gzsys.org.cn/doctor/14664 | 无 |
| 14545 | 鲍蕴文 | 正式行 | https://www.gzsys.org.cn/doctor/14545 | 无 |
| 14552 | 胡俊庭 | 正式行 | https://www.gzsys.org.cn/doctor/14552 | 无 |
| 15330 | 李娜 | 正式行 | https://www.gzsys.org.cn/doctor/15330 | 无 |
| 15314 | 黎锋 | 正式行 | https://www.gzsys.org.cn/doctor/15314 | 无 |
| 14627 | 何杰民 | 正式行 | https://www.gzsys.org.cn/doctor/14627 | 无 |
| 15274 | 麦明泉 | 正式行 | https://www.gzsys.org.cn/doctor/15274 | 无 |
| 14528 | 阮毅 | 正式行 | https://www.gzsys.org.cn/node/14528 | 无 |
| 15251 | 彭林辉 | 正式行 | https://www.gzsys.org.cn/node/15251 | 无 |
| 15361 | 黄泽坚 | 正式行 | https://www.gzsys.org.cn/doctor/15361 | 无 |
| 15413 | 曾志芬 | 正式行 | https://www.gzsys.org.cn/doctor/15413 | 无 |
| 29823 | 李卓 | 正式行 | https://www.gzsys.org.cn/doctor/29823 | 无 |
| 17005 | 李睿歆 | 正式行 | https://www.gzsys.org.cn/node/17005 | 无 |
| 17008 | 凌小婷 | 正式行 | https://www.gzsys.org.cn/node/17008 | 无 |
| 17017 | 王东雁 | 正式行 | https://www.gzsys.org.cn/node/17017 | 无 |
| 17018 | 王静姝 | 正式行 | https://www.gzsys.org.cn/node/17018 | 无 |
| 15561 | 程帝 | 正式行 | https://www.gzsys.org.cn/doctor/15561 | 无 |
| 15374 | 刘婷 | 正式行 | https://www.gzsys.org.cn/doctor/15374 | 无 |
| 15345 | 何剑峰 | 正式行 | https://www.gzsys.org.cn/doctor/15345 | 无 |
| 29732 | 周睿 | 正式行 | https://www.gzsys.org.cn/doctor/29732 | 无 |
| 27140 | 丁林 | 正式行 | https://www.gzsys.org.cn/node/27140 | 无 |
| 18537 | 赵雅男 | 正式行 | https://www.gzsys.org.cn/node/18537 | 无 |
| 18534 | 方庭枫 | 正式行 | https://www.gzsys.org.cn/node/18534 | 无 |
| 18536 | 郑澄宇 | 正式行 | https://www.gzsys.org.cn/node/18536 | 无 |
| 17015 | 沈婷 | 正式行 | https://www.gzsys.org.cn/node/17015 | 无 |
| 15479 | 马婷婷 | 正式行 | https://www.gzsys.org.cn/doctor/15479 | 无 |
| 15482 | 刘祖霖 | 正式行 | https://www.gzsys.org.cn/doctor/15482 | 无 |
| 15506 | 李玉东 | 正式行 | https://www.gzsys.org.cn/doctor/15506 | 无 |
| 17459 | 吕函璐 | 正式行 | https://www.gzsys.org.cn/node/17459 | 无 |
| 15471 | 黄波水 | 正式行 | https://www.gzsys.org.cn/doctor/15471 | 无 |
| 15491 | 舒晓蓉 | 正式行 | https://www.gzsys.org.cn/doctor/15491 | 无 |
| 15504 | 李金 | 正式行 | https://www.gzsys.org.cn/doctor/15504 | 无 |
| 15505 | 曾敏慧 | 正式行 | https://www.gzsys.org.cn/node/15505 | 无 |
| 15445 | 杨刚 | 正式行 | https://www.gzsys.org.cn/doctor/15445 | 无 |
| 15452 | 谢言信 | 正式行 | https://www.gzsys.org.cn/doctor/15452 | 无 |
| 31031 | 蔡雷琴 | 正式行 | https://www.gzsys.org.cn/doctor/31031 | 无 |
| 19811 | 王培 | 正式行 | https://www.gzsys.org.cn/node/19811 | 无 |
| 19812 | 李奇观 | 正式行 | https://www.gzsys.org.cn/node/19812 | 无 |
| 19813 | 韦丽娅 | 正式行 | https://www.gzsys.org.cn/node/19813 | 无 |
| 17013 | 梅静思 | 正式行 | https://www.gzsys.org.cn/node/17013 | 无 |
| 15451 | 聂晓露 | 正式行 | https://www.gzsys.org.cn/doctor/15451 | 无 |
| 15854 | 欧榕琼 | 正式行 | https://www.gzsys.org.cn/doctor/15854 | 无 |
| 15544 | 谭浪平 | 正式行 | https://www.gzsys.org.cn/doctor/15544 | 无 |
| 15453 | 王海燕 | 正式行 | https://www.gzsys.org.cn/node/15453 | 无 |
| 18538 | 刘擘 | 正式行 | https://www.gzsys.org.cn/node/18538 | 无 |
| 17024 | 张露 | 正式行 | https://www.gzsys.org.cn/node/17024 | 无 |
| 17003 | 李敬彦 | 正式行 | https://www.gzsys.org.cn/node/17003 | 无 |
| 17004 | 李凌 | 正式行 | https://www.gzsys.org.cn/node/17004 | 无 |
| 15424 | 杨荟 | 正式行 | https://www.gzsys.org.cn/doctor/15424 | 无 |
| 15376 | 张黎黎 | 正式行 | https://www.gzsys.org.cn/doctor/15376 | 无 |
| 35422 | 王稳健 | 正式行 | https://www.gzsys.org.cn/doctor/35422 | 无 |
| 32792 | 彭丽琴 | 正式行 | https://www.gzsys.org.cn/doctor/32792 | 无 |
| 15536 | 李梓敬 | 正式行 | https://www.gzsys.org.cn/doctor/15536 | 无 |
| 15492 | 陈乐锋 | 正式行 | https://www.gzsys.org.cn/doctor/15492 | 无 |
| 15513 | 余韵 | 正式行 | https://www.gzsys.org.cn/doctor/15513 | 无 |
| 15406 | 韦秀宁 | 正式行 | https://www.gzsys.org.cn/doctor/15406 | 无 |
| 33228 | 李明 | 正式行 | https://www.gzsys.org.cn/doctor/33228 | 无 |
| 17028 | 蔡志清 | 正式行 | https://www.gzsys.org.cn/node/17028 | 无 |
| 22712 | 李忠军 | 正式行 | https://www.gzsys.org.cn/node/22712 | 无 |
| 16999 | 何明亮 | 正式行 | https://www.gzsys.org.cn/node/16999 | 无 |
| 17011 | 刘正豪 | 正式行 | https://www.gzsys.org.cn/node/17011 | 无 |
| 18241 | 王永振 | 正式行 | https://www.gzsys.org.cn/node/18241 | 无 |
| 15565 | 苏正 | 正式行 | https://www.gzsys.org.cn/node/15565 | 无 |
| 15501 | 张剑 | 正式行 | https://www.gzsys.org.cn/doctor/15501 | 无 |
| 15438 | 林秀红 | 正式行 | https://www.gzsys.org.cn/doctor/15438 | 无 |
| 25212 | 万欢 | 正式行 | https://www.gzsys.org.cn/node/25212 | 无 |
| 18542 | 邱荣林 | 正式行 | https://www.gzsys.org.cn/node/18542 | 无 |
| 15511 | 彭晴霞 | 正式行 | https://www.gzsys.org.cn/node/15511 | 无 |
| 15468 | 陈颖 | 正式行 | https://www.gzsys.org.cn/node/15468 | 无 |
| 17012 | 麦岚 | 正式行 | https://www.gzsys.org.cn/node/17012 | 无 |
| 17009 | 刘艳琼 | 正式行 | https://www.gzsys.org.cn/node/17009 | 无 |
| 17025 | 植耀炜 | 正式行 | https://www.gzsys.org.cn/node/17025 | 无 |
| 17026 | 周林 | 正式行 | https://www.gzsys.org.cn/node/17026 | 无 |
| 15517 | 康梦如 | 正式行 | https://www.gzsys.org.cn/doctor/15517 | 无 |
| 18243 | 胡星云 | 正式行 | https://www.gzsys.org.cn/node/18243 | 无 |
| 16772 | 王澄 | 正式行 | https://www.gzsys.org.cn/node/16772 | 无 |
| 15480 | 邱绮 | 正式行 | https://www.gzsys.org.cn/doctor/15480 | 无 |
| 15401 | 梁中锟 | 正式行 | https://www.gzsys.org.cn/doctor/15401 | 无 |
| 15857 | 陈雪贞 | 正式行 | https://www.gzsys.org.cn/doctor/15857 | 无 |
| 14716 | 常瑞明 | 正式行 | https://www.gzsys.org.cn/node/14716 | 无 |
| 24210 | 李键芬 | 正式行 | https://www.gzsys.org.cn/node/24210 | 无 |
| 35441 | 王科喜 | 正式行 | https://www.gzsys.org.cn/doctor/35441 | 无 |
| 24151 | 王靖淞 | 正式行 | https://www.gzsys.org.cn/node/24151 | 无 |
| 24010 | 梁育玮 | 正式行 | https://www.gzsys.org.cn/node/24010 | 无 |
| 29579 | 邵莉滨 | 正式行 | https://www.gzsys.org.cn/doctor/29579 | 无 |
| 15566 | 王静 | 正式行 | https://www.gzsys.org.cn/doctor/15566 | 无 |
| 17007 | 林少丹 | 正式行 | https://www.gzsys.org.cn/node/17007 | 无 |
| 16994 | 陈钦标 | 正式行 | https://www.gzsys.org.cn/node/16994 | 无 |
| 17006 | 廖文华 | 正式行 | https://www.gzsys.org.cn/node/17006 | 无 |
| 16996 | 戴佳颖 | 正式行 | https://www.gzsys.org.cn/node/16996 | 无 |
| 15278 | 肖颂华 | 正式行 | https://www.gzsys.org.cn/node/15278 | 无 |
| 27187 | 余孝丽 | 正式行 | https://www.gzsys.org.cn/node/27187 | 无 |


## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| https://www.gzsys.org.cn/doctor/592/search | 王庄斐 副主任护师 | https://www.gzsys.org.cn/doctor/14598 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| https://www.gzsys.org.cn/doctor/592/search | 徐静 副主任护师 | https://www.gzsys.org.cn/node/16987 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| https://www.gzsys.org.cn/doctor/592/search | 陈丽莉 副主任护师 | https://www.gzsys.org.cn/node/18532 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| https://www.gzsys.org.cn/doctor/592/search | 黄佩贤 副主任护师 | https://www.gzsys.org.cn/doctor/14576 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| https://www.gzsys.org.cn/doctor/592/search | 温作珍 副主任护师 | https://www.gzsys.org.cn/node/16988 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |
| https://www.gzsys.org.cn/doctor/592/search | 黄淑婷 主管护师 | https://www.gzsys.org.cn/doctor/15353 | 官网医生卡片仅标注护理身份，排除医生画像采集范围 |

## 输出文件

- Excel 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx`
- CSV 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 23 |
| 原始医生卡片记录 | 664 |
| 跨入口去重前候选关系 | 664 |
| 跨入口去重后唯一候选 | 664 |
| 排除非医生候选 | 6 |
| 合规医生详情页 | 658 |
| 最终医生身份 | 658 |
| 覆盖科室数 | 69 |
| 列表页失败数 | 0 |
| 详情页失败数 | 1 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 130 |
| 慢性病 | 142 |
| 术后恢复/康复 | 121 |
| 生殖疾病 | 71 |
| 疑难重症 | 184 |
| 肿瘤 | 290 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 心血管内科 | 36 |
| 骨外科 | 32 |
| 耳鼻喉科 | 25 |
| 神经科 | 24 |
| 肝胆外科 | 24 |
| 乳腺外科 | 21 |
| 消化内科 | 21 |
| 口腔科 | 21 |
| 内分泌内科 | 20 |
| 妇科生殖内分泌专科 | 20 |
| 泌尿外科 | 19 |
| 放射科影像专科 | 18 |
| 普通妇科专科 | 17 |
| 妇科肿瘤专科 | 16 |
| 呼吸与危重症医学科 | 16 |
| 皮肤科 | 16 |
| 麻醉科 | 15 |
| 神经外科 | 14 |
| 超声科 | 13 |
| 肾内科 | 13 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 非医生页面或姓名异常 | 1 |
| 职称/身份需人工复核 | 15 |
| 详情正文为空或未识别 | 65 |
| 详情页读取失败 | 1 |

## 列表页读取异常

| 页码 | URL | 错误 |
|---|---|---|
| 无 | 无 | 无 |

## 详情页读取异常

| 来源链接 | 错误 |
|---|---|
| https://www.gzsys.org.cn/node/25208 | HTTP 404 |

## 人工复核建议

1. 优先复核“异常提示”不为空的医生。
2. “亮眼经历线索”只作为官方证据线索，不直接改写为对外宣传语。
3. 官网没有展示的擅长、经历、疾病标签保持空白，不补造。
4. 标记为试采门禁的适配器必须先完成小样本复核；只有取得 Claude 明确通过指令后才可全量追加。

## 合规边界

- 仅使用医院官网公开网页。
- 不采集私人电话、私人微信、家庭住址、患者隐私或非公开排班信息。
- 不使用第三方医疗平台评价、排名、患者评论。
- 不写“保证治愈”“包治疑难杂症”“疗效第一”等无法由官网证明的表达。
