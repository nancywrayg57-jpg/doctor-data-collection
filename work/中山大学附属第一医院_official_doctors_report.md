---
类型: 全量采集归并审计报告
医院: 中山大学附属第一医院
城市: 广州市
采集日期: 2026-08-13
来源范围: 医院官网
采集入口: https://www.fahsysu.org.cn/page/6945
适配器: fahsysu_drupal_expert_directory
---

# 中山大学附属第一医院 官方医生全量采集归并审计报告

## 结论

本次全量采集只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集全量采集底表，共 860 位唯一医生；官网列表页原始卡片记录 881 条；读取入口分类 90 个；覆盖 90 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 中山大学附属第一医院 |
| 官网首页 | https://www.fahsysu.org.cn/home |
| 本轮医生入口 | https://www.fahsysu.org.cn/page/6945 |
| 入口来源 | GitHub Issue #37（与官网入口台账一致） |
| 原台账医生入口 | https://www.fahsysu.org.cn/page/6945 |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | D-待人工补官网 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
| 官网专家介绍科室树 | https://www.fahsysu.org.cn/page/6945 | 医院官网 Drupal 公开专家单页长列表 | 1 | 881 | 860 | 0 | 中山大学附属第一医院 | 仅 action-item 结构内 /node/<数字ID> 授权；同 ID 跨科室合并，同名不同 ID 分行 |

### 动态目录专项证据

- 医生分页/载入方式：官网服务端完整输出单页长列表；未提交搜索词、未构造筛选组合、未探测接口
- 医生目录公开接口：不适用
- 医生详情公开接口：不适用
- 接口出处证据：不适用
- 院区/分组：42 个；科室分类：90 个
- 医生-科室关系：881 条
- 唯一详情 ID：860 个
- 有姓名详情 ID：860 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：852 个
- 同名不同详情 ID：8 组
- 非空/空科室块：860 / 0
- 院区/出诊点标签关系：无
- 跨院区/出诊点详情 ID：0 个

| 同名 | 详情 ID |
|---|---|
| 庄锦涛 | 29148,31480 |
| 涂响安 | 735,31481 |
| 匡铭 | 650,5582 |
| 梁力建 | 653,21325 |
| 王伟 | 5592,25409 |
| 刘敏 | 5684,25838 |
| 陈宇 | 5708,5784 |
| 何潇芳 | 38113,38613 |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：881
- 跨入口去重后唯一候选：860
- 跨入口重复关系：21
- 试采覆盖入口分类：90 个（中医科、临床心理科（门诊）、临床营养科、乳腺外科、产科、介入超声专科、体外循环科、健康管理中心、儿科ICU、儿科一科、儿科三科（新生儿科）、儿科二科、关节外科、内分泌内科、内科门诊、内镜中心、分子诊断与基因检测中心、医学检验科、变态反应专科、口内修复科、口腔科、口腔颌面外科、呼吸与危重症医学科、咽喉专科、器官移植科、外科门诊、妇科、小儿外科、康复医学科、心内一科、心内三科（高血压血管病）、心内二科（心介科）、心内五科（心血管康复科）、心内六科（CCU）、心胸外科ICU、心脏外科、心血管儿科、心血管内科、急诊科、放射介入专科、放射治疗科、放射诊断专科、整形外科、显微创伤外手科、普通外科、核医学科、泌尿外科、消化内科、烧伤与创面修复科、特需一科（老年病科）、特需三科、特需二科、生殖医学中心、生殖男科专科、甲状腺外科、男科、病理科、皮肤科、眼科、神经一科、神经三科（神经功能专科）、神经二科（脑血管病专科）、神经外科、神经科、神经科ICU、老年病科、耳专科、耳鼻咽喉科、肝外科、肝移植专科、肾内科、肾移植专科、肿瘤介入科、肿瘤科、胃肠外科一科、胃肠外科三科、胃肠外科二科、胆胰外科、胸外科、脊柱外科、药学部、血液内科、血管外科、超声医学科、转化医学研究中心、运动医学科、风湿免疫科、骨肿瘤科、麻醉科、鼻专科）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 无 | 无 | 无 |

## 中山大学附属第一医院目录范围与 ID 门禁

- 官网服务端单页目录：顶层容器 42（其中含医生关系 32、空容器 10）、下级专科 90、医生—专科关系 881、唯一数字 ID 860。
- 空顶层容器：手术麻醉中心、输血科、高压氧科、保健门诊中心、精准医学研究院、临床研究中心、药物临床试验机构、动物实验中心、无菌动物研究平台、消毒供应中心。计入页面结构普查，但不构造医生或专科关系。
- 跨专科重复：21 条关系增量；同一数字 ID 的科室以顿号合并，不按姓名归并。
- 同名不同 ID：8 组，全部按数字 ID 保持独立；样本命中时标记“同名待甄别”。
- 目录职级线索：正高 447、副高 434；正式职称只取详情页显式字段，不拼接正高/副高。
- 分页/交互：官网服务端完整输出单页长列表；未提交搜索词、未构造筛选组合、未探测接口。
- 院区词扫描：目录页 院本部=0、本部=0、东院区=0、东院=0、南沙=0、南院区=0、黄埔=0、院区=0；本轮详情 东院=42、黄埔=14、院区=31、南沙=18、院本部=18、本部=20，涉及 40 位。目录页未发现院区词；试采详情仅在履历正文发现院区词，官网未提供统一结构化院区字段，不能据此为全目录医生推断本部、东院、南沙或黄埔归属
- 黄埔边界：未使用台账序号 8 黄埔院区专属目录；目录与试采详情均无黄埔标记，仍无法证明或排除未抽样医生中是否混入黄埔归属
- 黄埔去重预案：执行台账序号 8 时，必须以其目录数字 node ID 与本轮 860-ID 对账；命中本轮 ID 的医生不得重复入库。
- 详情清洗：排班 DOM 排除 34400 个；排名/患者片段排除 131 个；正式字段排班写入 0、私用区字符 0。

### 逐 ID 对账

| 详情 ID | 姓名 | 裁决 | 顶层分组 | 科室 | 目录职级线索 | 原关系数 | 来源链接 | 理由 |
|---|---|---|---|---|---|---:|---|---|
| 620 | 郭宇 | 正式行 | 外科 | 普通外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/620 | 无 |
| 619 | 詹文华 | 正式行 | 外科 | 普通外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/619 | 无 |
| 628 | 陈昆 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/628 | 无 |
| 641 | 郭少雷 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/641 | 无 |
| 632 | 黄正松 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/632 | 无 |
| 631 | 黄权 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/631 | 无 |
| 630 | 何东升 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/630 | 无 |
| 634 | 刘金龙 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/634 | 无 |
| 25607 | 梁丰 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25607 | 无 |
| 633 | 林佳平 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/633 | 无 |
| 32417 | 刘雪松 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/32417 | 无 |
| 645 | 毛志钢 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/645 | 无 |
| 635 | 齐铁伟 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/635 | 无 |
| 637 | 夏之柏 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/637 | 无 |
| 638 | 杨超 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/638 | 无 |
| 639 | 杨李轩 | 正式行 | 外科 | 神经外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/639 | 无 |
| 29222 | 丁之明 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29222 | 无 |
| 33075 | 何科君 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33075 | 无 |
| 642 | 金华伟 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/642 | 无 |
| 643 | 柯春龙 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/643 | 无 |
| 644 | 廖创新 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/644 | 无 |
| 35658 | 谢宝树 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35658 | 无 |
| 35088 | 徐桂兴 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35088 | 无 |
| 647 | 余振华 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/647 | 无 |
| 35759 | 姚顺 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35759 | 无 |
| 29225 | 杨帅 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29225 | 无 |
| 35650 | 章昌明 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35650 | 无 |
| 38215 | 赵坤 | 正式行 | 外科 | 神经外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38215 | 无 |
| 666 | 陈蕾 | 正式行 | 外科 | 烧伤与创面修复科 | 正高 | 1 | https://www.fahsysu.org.cn/node/666 | 无 |
| 667 | 胡志成 | 正式行 | 外科 | 烧伤与创面修复科 | 正高 | 1 | https://www.fahsysu.org.cn/node/667 | 无 |
| 660 | 刘旭盛 | 正式行 | 外科 | 烧伤与创面修复科 | 正高 | 1 | https://www.fahsysu.org.cn/node/660 | 无 |
| 668 | 舒斌 | 正式行 | 外科 | 烧伤与创面修复科 | 正高 | 1 | https://www.fahsysu.org.cn/node/668 | 无 |
| 663 | 谢举临 | 正式行 | 外科 | 烧伤与创面修复科 | 正高 | 1 | https://www.fahsysu.org.cn/node/663 | 无 |
| 664 | 徐盈斌 | 正式行 | 外科 | 烧伤与创面修复科 | 正高 | 1 | https://www.fahsysu.org.cn/node/664 | 无 |
| 665 | 朱家源 | 正式行 | 外科 | 烧伤与创面修复科 | 正高 | 1 | https://www.fahsysu.org.cn/node/665 | 无 |
| 31089 | 赵菁玲 | 正式行 | 外科 | 烧伤与创面修复科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31089 | 无 |
| 671 | 陈炜 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/671 | 无 |
| 669 | 陈俊星 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/669 | 无 |
| 732 | 陈凌武 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/732 | 无 |
| 682 | 陈旭 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/682 | 无 |
| 681 | 陈羽 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/681 | 无 |
| 672 | 戴宇平 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/672 | 无 |
| 733 | 邓春华 | 正式行 | 外科 | 泌尿外科、男科 | 正高 | 2 | https://www.fahsysu.org.cn/node/733 | 无 |
| 683 | 黄斌 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/683 | 无 |
| 26632 | 罗俊航 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/26632 | 无 |
| 674 | 李晓飞 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/674 | 无 |
| 675 | 梁月有 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/675 | 无 |
| 685 | 莫承强 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/685 | 无 |
| 684 | 毛晓鹏 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/684 | 无 |
| 676 | 丘少鹏 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/676 | 无 |
| 734 | 孙祥宙 | 正式行 | 外科 | 泌尿外科、男科 | 正高 | 2 | https://www.fahsysu.org.cn/node/734 | 无 |
| 678 | 王道虎 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/678 | 无 |
| 679 | 吴荣佩 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/679 | 无 |
| 680 | 郑伏甫 | 正式行 | 外科 | 泌尿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/680 | 无 |
| 37245 | 曹明欣 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/37245 | 无 |
| 31148 | 陈振华 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31148 | 无 |
| 34185 | 邓立文 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/34185 | 无 |
| 36760 | 方咏 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36760 | 无 |
| 25417 | 潘金成 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25417 | 无 |
| 25418 | 韦锦焕 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25418 | 无 |
| 686 | 王文卫 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/686 | 无 |
| 29157 | 王宗任 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29157 | 无 |
| 687 | 项勇 | 正式行 | 外科 | 泌尿外科、男科 | 副高 | 2 | https://www.fahsysu.org.cn/node/687 | 无 |
| 31142 | 杨其运 | 正式行 | 外科 | 泌尿外科、男科 | 副高 | 2 | https://www.fahsysu.org.cn/node/31142 | 无 |
| 38124 | 张俊隆 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38124 | 无 |
| 29148 | 庄锦涛 | 同名待甄别 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29148 | 同名不同数字 ID 分行保留 |
| 34930 | 赵亮 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/34930 | 无 |
| 25475 | 曾钦松 | 正式行 | 外科 | 泌尿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25475 | 无 |
| 608 | 高勇 | 正式行 | 外科、妇产科 | 男科、生殖医学中心 | 正高 | 2 | https://www.fahsysu.org.cn/node/608 | 无 |
| 735 | 涂响安 | 同名待甄别 | 外科 | 男科 | 正高 | 1 | https://www.fahsysu.org.cn/node/735 | 同名不同数字 ID 分行保留 |
| 688 | 刘钧澄 | 正式行 | 外科 | 小儿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/688 | 无 |
| 33115 | 徐哲 | 正式行 | 外科 | 小儿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/33115 | 无 |
| 690 | 周李 | 正式行 | 外科 | 小儿外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/690 | 无 |
| 35591 | 陈华东 | 正式行 | 外科 | 小儿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35591 | 无 |
| 31106 | 蒋宏 | 正式行 | 外科 | 小儿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31106 | 无 |
| 36848 | 张志崇 | 正式行 | 外科 | 小儿外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36848 | 无 |
| 662 | 唐冰 | 正式行 | 外科 | 整形外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/662 | 无 |
| 36849 | 唐庆 | 正式行 | 外科 | 整形外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/36849 | 无 |
| 697 | 程钢 | 正式行 | 外科 | 整形外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/697 | 无 |
| 33065 | 许澍洽 | 正式行 | 外科 | 整形外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33065 | 无 |
| 700 | 曾瑞曦 | 正式行 | 外科 | 整形外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/700 | 无 |
| 36847 | 张毅 | 正式行 | 外科 | 整形外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36847 | 无 |
| 31245 | 朱昭炜 | 正式行 | 外科 | 整形外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31245 | 无 |
| 701 | 陈振光 | 正式行 | 外科 | 胸外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/701 | 无 |
| 702 | 程超 | 正式行 | 外科 | 胸外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/702 | 无 |
| 703 | 顾勇 | 正式行 | 外科 | 胸外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/703 | 无 |
| 705 | 罗红鹤 | 正式行 | 外科 | 胸外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/705 | 无 |
| 704 | 鲁建军 | 正式行 | 外科 | 胸外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/704 | 无 |
| 25478 | 刘振国 | 正式行 | 外科 | 胸外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25478 | 无 |
| 706 | 巫国勇 | 正式行 | 外科 | 胸外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/706 | 无 |
| 708 | 雷艺炎 | 正式行 | 外科 | 胸外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/708 | 无 |
| 25425 | 马俊 | 正式行 | 外科 | 胸外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25425 | 无 |
| 709 | 苏春华 | 正式行 | 外科 | 胸外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/709 | 无 |
| 35663 | 曾博 | 正式行 | 外科 | 胸外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35663 | 无 |
| 25471 | 邹健勇 | 正式行 | 外科 | 胸外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25471 | 无 |
| 31149 | 张水深 | 正式行 | 外科 | 胸外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31149 | 无 |
| 5600 | 黄文生 | 正式行 | 外科 | 外科门诊 | 副高 | 1 | https://www.fahsysu.org.cn/node/5600 | 无 |
| 720 | 李强 | 正式行 | 外科 | 外科门诊 | 副高 | 1 | https://www.fahsysu.org.cn/node/720 | 无 |
| 621 | 常光其 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/621 | 无 |
| 622 | 胡作军 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/622 | 无 |
| 627 | 王冕 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/627 | 无 |
| 25317 | 武日东 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25317 | 无 |
| 625 | 姚陈 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/625 | 无 |
| 626 | 李梓伦 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/626 | 无 |
| 38171 | 汪睿 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38171 | 无 |
| 35587 | 王斯文 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35587 | 无 |
| 33031 | 吴伟滨 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33031 | 无 |
| 35672 | 王折存 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35672 | 无 |
| 38598 | 周昱 | 正式行 | 血管甲状腺乳腺中心 | 血管外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38598 | 无 |
| 724 | 吕伟明 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/724 | 无 |
| 721 | 李松奇 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/721 | 无 |
| 729 | 徐向东 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/729 | 无 |
| 726 | 林维浩 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/726 | 无 |
| 38174 | 林勃 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38174 | 无 |
| 29456 | 林小红 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29456 | 无 |
| 25543 | 单臻 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25543 | 无 |
| 728 | 吴壮宏 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/728 | 无 |
| 36846 | 朱易凡 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36846 | 无 |
| 33150 | 张展强 | 正式行 | 血管甲状腺乳腺中心 | 甲状腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33150 | 无 |
| 723 | 林颖 | 正式行 | 血管甲状腺乳腺中心 | 乳腺外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/723 | 无 |
| 624 | 王深明 | 正式行 | 血管甲状腺乳腺中心 | 乳腺外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/624 | 无 |
| 731 | 张赟建 | 正式行 | 血管甲状腺乳腺中心 | 乳腺外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/731 | 无 |
| 31358 | 匡夏颖 | 正式行 | 血管甲状腺乳腺中心 | 乳腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31358 | 无 |
| 727 | 邵楠 | 正式行 | 血管甲状腺乳腺中心 | 乳腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/727 | 无 |
| 25781 | 史雅薇 | 正式行 | 血管甲状腺乳腺中心 | 乳腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25781 | 无 |
| 730 | 于亮 | 正式行 | 血管甲状腺乳腺中心 | 乳腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/730 | 无 |
| 33081 | 叶润仪 | 正式行 | 血管甲状腺乳腺中心 | 乳腺外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33081 | 无 |
| 658 | 胡文杰 | 正式行 | 肝胆胰外科中心 | 肝外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/658 | 无 |
| 18614 | 何强 | 正式行 | 肝胆胰外科中心 | 肝外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/18614 | 无 |
| 649 | 华赟鹏 | 正式行 | 肝胆胰外科中心 | 肝外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/649 | 无 |
| 650 | 匡铭 | 同名待甄别 | 肝胆胰外科中心 | 肝外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/650 | 同名不同数字 ID 分行保留 |
| 5584 | 吕明德 | 正式行 | 肝胆胰外科中心、超声医学科 | 肝外科、超声医学科、介入超声专科 | 正高 | 3 | https://www.fahsysu.org.cn/node/5584 | 无 |
| 653 | 梁力建 | 同名待甄别 | 肝胆胰外科中心 | 肝外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/653 | 同名不同数字 ID 分行保留 |
| 651 | 黎东明 | 正式行 | 肝胆胰外科中心 | 肝外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/651 | 无 |
| 652 | 李绍强 | 正式行 | 肝胆胰外科中心 | 肝外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/652 | 无 |
| 655 | 沈顺利 | 正式行 | 肝胆胰外科中心 | 肝外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/655 | 无 |
| 656 | 周奇 | 正式行 | 肝胆胰外科中心 | 肝外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/656 | 无 |
| 35583 | 陈泽斌 | 正式行 | 肝胆胰外科中心 | 肝外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35583 | 无 |
| 38160 | 钱柏锋 | 正式行 | 肝胆胰外科中心 | 肝外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38160 | 无 |
| 718 | 吴健 | 正式行 | 肝胆胰外科中心 | 肝外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/718 | 无 |
| 35707 | 王恕同 | 正式行 | 肝胆胰外科中心 | 肝外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35707 | 无 |
| 31479 | 谢文轩 | 正式行 | 肝胆胰外科中心 | 肝外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31479 | 无 |
| 716 | 陈伟 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/716 | 无 |
| 715 | 陈流华 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/715 | 无 |
| 710 | 陈东 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/710 | 无 |
| 712 | 赖佳明 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/712 | 无 |
| 21325 | 梁力建 | 同名待甄别 | 肝胆胰外科中心 | 胆胰外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/21325 | 同名不同数字 ID 分行保留 |
| 713 | 殷晓煜 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/713 | 无 |
| 714 | 郑朝旭 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/714 | 无 |
| 719 | 张昆松 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/719 | 无 |
| 35694 | 蔡建鹏 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35694 | 无 |
| 32861 | 黄晨松 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/32861 | 无 |
| 717 | 黄力 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/717 | 无 |
| 33078 | 黄锡泰 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33078 | 无 |
| 33079 | 彭洪 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33079 | 无 |
| 35662 | 许琼聪 | 正式行 | 肝胆胰外科中心 | 胆胰外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35662 | 无 |
| 750 | 陈剑辉 | 正式行 | 胃肠外科中心 | 胃肠外科一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/750 | 无 |
| 738 | 蔡世荣 | 正式行 | 胃肠外科中心 | 胃肠外科一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/738 | 无 |
| 740 | 侯洵 | 正式行 | 胃肠外科中心 | 胃肠外科一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/740 | 无 |
| 746 | 何裕隆 | 正式行 | 胃肠外科中心 | 胃肠外科一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/746 | 无 |
| 741 | 李引 | 正式行 | 胃肠外科中心 | 胃肠外科一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/741 | 无 |
| 742 | 吴晖 | 正式行 | 胃肠外科中心 | 胃肠外科一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/742 | 无 |
| 25542 | 李广华 | 正式行 | 胃肠外科中心 | 胃肠外科一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25542 | 无 |
| 29238 | 叶锦宁 | 正式行 | 胃肠外科中心 | 胃肠外科一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29238 | 无 |
| 33099 | 翟二涛 | 正式行 | 胃肠外科中心 | 胃肠外科一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33099 | 无 |
| 745 | 陈创奇 | 正式行 | 胃肠外科中心 | 胃肠外科二科 | 正高 | 1 | https://www.fahsysu.org.cn/node/745 | 无 |
| 747 | 马晋平 | 正式行 | 胃肠外科中心 | 胃肠外科二科 | 正高 | 1 | https://www.fahsysu.org.cn/node/747 | 无 |
| 748 | 宋新明 | 正式行 | 胃肠外科中心 | 胃肠外科二科 | 正高 | 1 | https://www.fahsysu.org.cn/node/748 | 无 |
| 752 | 王昭 | 正式行 | 胃肠外科中心 | 胃肠外科二科 | 正高 | 1 | https://www.fahsysu.org.cn/node/752 | 无 |
| 756 | 陈志辉 | 正式行 | 胃肠外科中心 | 胃肠外科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/756 | 无 |
| 25422 | 彭建军 | 正式行 | 胃肠外科中心 | 胃肠外科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25422 | 无 |
| 31152 | 王志雄 | 正式行 | 胃肠外科中心 | 胃肠外科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31152 | 无 |
| 753 | 余红兰 | 正式行 | 胃肠外科中心 | 胃肠外科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/753 | 无 |
| 23538 | 杨世斌 | 正式行 | 胃肠外科中心 | 胃肠外科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/23538 | 无 |
| 757 | 崔冀 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 正高 | 1 | https://www.fahsysu.org.cn/node/757 | 无 |
| 754 | 宋武 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 正高 | 1 | https://www.fahsysu.org.cn/node/754 | 无 |
| 755 | 谭敏 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 正高 | 1 | https://www.fahsysu.org.cn/node/755 | 无 |
| 25668 | 魏哲威 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25668 | 无 |
| 743 | 徐建波 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 正高 | 1 | https://www.fahsysu.org.cn/node/743 | 无 |
| 744 | 张信华 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 正高 | 1 | https://www.fahsysu.org.cn/node/744 | 无 |
| 33147 | 戴伟钢 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33147 | 无 |
| 29215 | 孙开宇 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29215 | 无 |
| 759 | 谭进富 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 副高 | 1 | https://www.fahsysu.org.cn/node/759 | 无 |
| 35629 | 袁凯涛 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35629 | 无 |
| 29068 | 袁玉杰 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29068 | 无 |
| 29065 | 左继东 | 正式行 | 胃肠外科中心 | 胃肠外科三科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29065 | 无 |
| 462 | 陈玉清 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/462 | 无 |
| 463 | 何勉 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/463 | 无 |
| 465 | 柯珮琪 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/465 | 无 |
| 582 | 刘军秀 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/582 | 无 |
| 583 | 牛刚 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/583 | 无 |
| 584 | 沈宏伟 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/584 | 无 |
| 466 | 沈慧敏 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/466 | 无 |
| 467 | 王宁宁 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/467 | 无 |
| 575 | 徐成康 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/575 | 无 |
| 468 | 谢洪哲 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/468 | 无 |
| 576 | 杨国奋 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/576 | 无 |
| 577 | 姚书忠 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/577 | 无 |
| 578 | 游泽山 | 正式行 | 妇产科 | 妇科 | 正高 | 1 | https://www.fahsysu.org.cn/node/578 | 无 |
| 25411 | 陈明 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25411 | 无 |
| 33348 | 曹铁凤 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33348 | 无 |
| 30713 | 黄佳明 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/30713 | 无 |
| 580 | 何科 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/580 | 无 |
| 31105 | 何伟鹏 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31105 | 无 |
| 460 | 梁明懿 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/460 | 无 |
| 29809 | 刘兴阳 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29809 | 无 |
| 25410 | 梁炎春 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25410 | 无 |
| 35730 | 谭金凤 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35730 | 无 |
| 25409 | 王伟 | 同名待甄别 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25409 | 同名不同数字 ID 分行保留 |
| 33308 | 徐漫漫 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33308 | 无 |
| 33311 | 袁林静 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33311 | 无 |
| 29217 | 赵云荷 | 正式行 | 妇产科 | 妇科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29217 | 无 |
| 593 | 陈海天 | 正式行 | 妇产科 | 产科 | 正高 | 1 | https://www.fahsysu.org.cn/node/593 | 无 |
| 589 | 罗艳敏 | 正式行 | 妇产科 | 产科 | 正高 | 1 | https://www.fahsysu.org.cn/node/589 | 无 |
| 596 | 刘斌 | 正式行 | 妇产科 | 产科 | 正高 | 1 | https://www.fahsysu.org.cn/node/596 | 无 |
| 590 | 王子莲 | 正式行 | 妇产科 | 产科 | 正高 | 1 | https://www.fahsysu.org.cn/node/590 | 无 |
| 598 | 王冬昱 | 正式行 | 妇产科 | 产科 | 正高 | 1 | https://www.fahsysu.org.cn/node/598 | 无 |
| 591 | 周祎 | 正式行 | 妇产科 | 产科 | 正高 | 1 | https://www.fahsysu.org.cn/node/591 | 无 |
| 592 | 蔡坚 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/592 | 无 |
| 29710 | 陈汉青 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29710 | 无 |
| 594 | 黄林环 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/594 | 无 |
| 595 | 黄轩 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/595 | 无 |
| 25405 | 何志明 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25405 | 无 |
| 31955 | 刘立群 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31955 | 无 |
| 31109 | 李珠玉 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31109 | 无 |
| 597 | 彭田玉 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/597 | 无 |
| 35627 | 王晶 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35627 | 无 |
| 29223 | 吴艳欣 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29223 | 无 |
| 35590 | 祝彩霞 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35590 | 无 |
| 600 | 张颖 | 正式行 | 妇产科 | 产科 | 副高 | 1 | https://www.fahsysu.org.cn/node/600 | 无 |
| 606 | 陈明晖 | 正式行 | 妇产科 | 生殖医学中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/606 | 无 |
| 601 | 麦庆云 | 正式行 | 妇产科 | 生殖医学中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/601 | 无 |
| 602 | 王琼 | 正式行 | 妇产科 | 生殖医学中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/602 | 无 |
| 603 | 徐艳文 | 正式行 | 妇产科 | 生殖医学中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/603 | 无 |
| 605 | 周灿权 | 正式行 | 妇产科 | 生殖医学中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/605 | 无 |
| 604 | 钟依平 | 正式行 | 妇产科 | 生殖医学中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/604 | 无 |
| 26415 | 古芳 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/26415 | 无 |
| 607 | 高军 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/607 | 无 |
| 609 | 黄珈 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/609 | 无 |
| 29220 | 胡晓坤 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/29220 | 无 |
| 612 | 罗璐 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/612 | 无 |
| 611 | 李宇彬 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/611 | 无 |
| 613 | 苗本郁 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/613 | 无 |
| 35769 | 王轶子 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/35769 | 无 |
| 33092 | 文扬幸 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/33092 | 无 |
| 615 | 张丹 | 正式行 | 妇产科 | 生殖医学中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/615 | 无 |
| 31481 | 涂响安 | 同名待甄别 | 妇产科 | 生殖男科专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31481 | 同名不同数字 ID 分行保留 |
| 31480 | 庄锦涛 | 同名待甄别 | 妇产科 | 生殖男科专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31480 | 同名不同数字 ID 分行保留 |
| 5605 | 陈柏龄 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5605 | 无 |
| 5614 | 李泽民 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5614 | 无 |
| 25414 | 刘辉 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25414 | 无 |
| 5608 | 彭新生 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5608 | 无 |
| 5609 | 苏培强 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5609 | 无 |
| 5617 | 王建儒 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5617 | 无 |
| 5610 | 万勇 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5610 | 无 |
| 5612 | 邹学农 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5612 | 无 |
| 5611 | 郑召民 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5611 | 无 |
| 31103 | 崔尚斌 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31103 | 无 |
| 33113 | 戴驭虎 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33113 | 无 |
| 31108 | 郭玮 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31108 | 无 |
| 5613 | 黄阳亮 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5613 | 无 |
| 38190 | 李翔 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38190 | 无 |
| 33068 | 刘希哲 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33068 | 无 |
| 5616 | 王华 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5616 | 无 |
| 29146 | 王乐 | 正式行 | 骨科显微外科医学部 | 脊柱外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29146 | 无 |
| 5618 | 傅明 | 正式行 | 骨科显微外科医学部 | 关节外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5618 | 无 |
| 5619 | 何爱珊 | 正式行 | 骨科显微外科医学部 | 关节外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5619 | 无 |
| 5620 | 康焱 | 正式行 | 骨科显微外科医学部 | 关节外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5620 | 无 |
| 29219 | 刘建华 | 正式行 | 骨科显微外科医学部 | 关节外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/29219 | 无 |
| 5621 | 廖威明 | 正式行 | 骨科显微外科医学部 | 关节外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5621 | 无 |
| 5622 | 盛璞义 | 正式行 | 骨科显微外科医学部 | 关节外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5622 | 无 |
| 5623 | 徐栋梁 | 正式行 | 骨科显微外科医学部 | 关节外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5623 | 无 |
| 5629 | 张紫机 | 正式行 | 骨科显微外科医学部 | 关节外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5629 | 无 |
| 5628 | 张志奇 | 正式行 | 骨科显微外科医学部 | 关节外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5628 | 无 |
| 31110 | 陈蔚深 | 正式行 | 骨科显微外科医学部 | 关节外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31110 | 无 |
| 29033 | 古明晖 | 正式行 | 骨科显微外科医学部 | 关节外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29033 | 无 |
| 5625 | 胡俊勇 | 正式行 | 骨科显微外科医学部 | 关节外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5625 | 无 |
| 5624 | 何沛恒 | 正式行 | 骨科显微外科医学部 | 关节外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5624 | 无 |
| 25537 | 孟繁钢 | 正式行 | 骨科显微外科医学部 | 关节外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25537 | 无 |
| 5627 | 杨子波 | 正式行 | 骨科显微外科医学部 | 关节外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5627 | 无 |
| 25536 | 赵潇艺 | 正式行 | 骨科显微外科医学部 | 关节外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25536 | 无 |
| 5626 | 邬培慧 | 正式行 | 骨科显微外科医学部 | 运动医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5626 | 无 |
| 5630 | 黄纲 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5630 | 无 |
| 5631 | 沈靖南 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5631 | 无 |
| 25782 | 王永谦 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25782 | 无 |
| 5633 | 谢显彪 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5633 | 无 |
| 5632 | 尹军强 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5632 | 无 |
| 5634 | 邹昌业 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5634 | 无 |
| 29147 | 林调 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29147 | 无 |
| 31104 | 涂剑 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31104 | 无 |
| 29224 | 王博 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29224 | 无 |
| 29124 | 赵志强 | 正式行 | 骨科显微外科医学部 | 骨肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29124 | 无 |
| 5635 | 顾立强 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5635 | 无 |
| 5636 | 刘小林 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5636 | 无 |
| 5639 | 李平 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5639 | 无 |
| 5640 | 戚剑 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5640 | 无 |
| 23551 | 郑灿镔 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 正高 | 1 | https://www.fahsysu.org.cn/node/23551 | 无 |
| 5637 | 朱庆棠 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5637 | 无 |
| 5638 | 胡军 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5638 | 无 |
| 5641 | 秦本刚 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5641 | 无 |
| 5643 | 王洪刚 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5643 | 无 |
| 5644 | 向剑平 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5644 | 无 |
| 5646 | 易建华 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5646 | 无 |
| 5645 | 杨建涛 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5645 | 无 |
| 33064 | 闫立伟 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33064 | 无 |
| 38169 | 杨羿 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38169 | 无 |
| 25511 | 周翔 | 正式行 | 骨科显微外科医学部 | 显微创伤外手科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25511 | 无 |
| 38085 | 胡章威 | 正式行 | 耳鼻咽喉科 | 耳鼻咽喉科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38085 | 无 |
| 5686 | 吴旋 | 正式行 | 耳鼻咽喉科 | 耳专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5686 | 无 |
| 5682 | 熊观霞 | 正式行 | 耳鼻咽喉科 | 耳专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5682 | 无 |
| 20862 | 陈垲钿 | 正式行 | 耳鼻咽喉科 | 耳专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/20862 | 无 |
| 38089 | 方淑斌 | 正式行 | 耳鼻咽喉科 | 耳专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38089 | 无 |
| 5683 | 江广理 | 正式行 | 耳鼻咽喉科 | 耳专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5683 | 无 |
| 5684 | 刘敏 | 同名待甄别 | 耳鼻咽喉科 | 耳专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5684 | 同名不同数字 ID 分行保留 |
| 29050 | 任红苗 | 正式行 | 耳鼻咽喉科 | 耳专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29050 | 无 |
| 5685 | 魏凡钦 | 正式行 | 耳鼻咽喉科 | 耳专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5685 | 无 |
| 30448 | 王仙仁 | 正式行 | 耳鼻咽喉科 | 耳专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/30448 | 无 |
| 5687 | 庄惠文 | 正式行 | 耳鼻咽喉科 | 耳专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5687 | 无 |
| 5673 | 陈冬 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5673 | 无 |
| 5688 | 陈合新 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5688 | 无 |
| 5689 | 李健 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5689 | 无 |
| 5693 | 赖银妍 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5693 | 无 |
| 5690 | 史剑波 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5690 | 无 |
| 5694 | 文译辉 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5694 | 无 |
| 5691 | 徐睿 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5691 | 无 |
| 5675 | 许庚 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5675 | 无 |
| 5695 | 左可军 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5695 | 无 |
| 33080 | 陈德华 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33080 | 无 |
| 5692 | 郭洁波 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5692 | 无 |
| 31087 | 高文翔 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31087 | 无 |
| 30376 | 李光启 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/30376 | 无 |
| 33070 | 钟华 | 正式行 | 耳鼻咽喉科 | 鼻专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33070 | 无 |
| 5697 | 雷文斌 | 正式行 | 耳鼻咽喉科 | 咽喉专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5697 | 无 |
| 25406 | 马仁强 | 正式行 | 耳鼻咽喉科 | 咽喉专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25406 | 无 |
| 5698 | 文卫平 | 正式行 | 耳鼻咽喉科 | 咽喉专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5698 | 无 |
| 5676 | 祝小林 | 正式行 | 耳鼻咽喉科 | 咽喉专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5676 | 无 |
| 35791 | 陈林 | 正式行 | 耳鼻咽喉科 | 咽喉专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35791 | 无 |
| 29067 | 邓洁 | 正式行 | 耳鼻咽喉科 | 咽喉专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29067 | 无 |
| 5680 | 王章锋 | 正式行 | 耳鼻咽喉科 | 咽喉专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5680 | 无 |
| 5674 | 付清玲 | 正式行 | 耳鼻咽喉科 | 变态反应专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5674 | 无 |
| 5664 | 黄刚 | 正式行 | 器官移植科 | 肾移植专科、器官移植科 | 正高 | 2 | https://www.fahsysu.org.cn/node/5664 | 无 |
| 5653 | 邱江 | 正式行 | 器官移植科 | 肾移植专科、器官移植科 | 正高 | 2 | https://www.fahsysu.org.cn/node/5653 | 无 |
| 35698 | 傅茜 | 正式行 | 器官移植科 | 肾移植专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35698 | 无 |
| 5671 | 赵强 | 正式行 | 器官移植科 | 肝移植专科、器官移植科 | 正高 | 2 | https://www.fahsysu.org.cn/node/5671 | 无 |
| 38159 | 唐云华 | 正式行 | 器官移植科 | 肝移植专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38159 | 无 |
| 5647 | 陈国栋 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5647 | 无 |
| 5658 | 陈茂根 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5658 | 无 |
| 5663 | 郭志勇 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5663 | 无 |
| 5650 | 胡安斌 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5650 | 无 |
| 5649 | 何晓顺 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5649 | 无 |
| 5665 | 鞠卫强 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5665 | 无 |
| 5667 | 刘龙山 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5667 | 无 |
| 5652 | 马毅 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5652 | 无 |
| 5655 | 王东平 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5655 | 无 |
| 5654 | 王长希 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5654 | 无 |
| 5670 | 吴成林 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5670 | 无 |
| 5657 | 朱晓峰 | 正式行 | 器官移植科 | 器官移植科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5657 | 无 |
| 5659 | 陈颖华 | 正式行 | 器官移植科 | 器官移植科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5659 | 无 |
| 5661 | 邓素雄 | 正式行 | 器官移植科 | 器官移植科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5661 | 无 |
| 5660 | 邓荣海 | 正式行 | 器官移植科 | 器官移植科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5660 | 无 |
| 5666 | 李军 | 正式行 | 器官移植科 | 器官移植科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5666 | 无 |
| 5668 | 王国栋 | 正式行 | 器官移植科 | 器官移植科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5668 | 无 |
| 5753 | 万鹏霞 | 正式行 | 眼科 | 眼科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5753 | 无 |
| 34343 | 陈婷婷 | 正式行 | 眼科 | 眼科 | 副高 | 1 | https://www.fahsysu.org.cn/node/34343 | 无 |
| 5750 | 陈雪梅（曾用名：陈咏冲） | 正式行 | 眼科 | 眼科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5750 | 无 |
| 20861 | 甘世斌 | 正式行 | 眼科 | 眼科 | 副高 | 1 | https://www.fahsysu.org.cn/node/20861 | 无 |
| 5751 | 霍丽君 | 正式行 | 眼科 | 眼科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5751 | 无 |
| 33056 | 苏毅华 | 正式行 | 眼科 | 眼科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33056 | 无 |
| 33169 | 余芬芬 | 正式行 | 眼科 | 眼科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33169 | 无 |
| 5755 | 朱文珲 | 正式行 | 眼科 | 眼科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5755 | 无 |
| 25474 | 何倩婷 | 正式行 | 口腔科 | 口腔颌面外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25474 | 无 |
| 34931 | 李祥 | 正式行 | 口腔科 | 口腔颌面外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/34931 | 无 |
| 38112 | 舒大龙 | 正式行 | 口腔科 | 口腔颌面外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38112 | 无 |
| 34929 | 朱双喜 | 正式行 | 口腔科 | 口腔颌面外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/34929 | 无 |
| 29277 | 陈珊 | 正式行 | 口腔科 | 口内修复科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29277 | 无 |
| 31338 | 吉利 | 正式行 | 口腔科 | 口内修复科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31338 | 无 |
| 33076 | 姜瑞 | 正式行 | 口腔科 | 口内修复科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33076 | 无 |
| 29071 | 聂二民 | 正式行 | 口腔科 | 口内修复科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29071 | 无 |
| 25785 | 彭伟 | 正式行 | 口腔科 | 口内修复科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25785 | 无 |
| 38209 | 任静 | 正式行 | 口腔科 | 口内修复科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38209 | 无 |
| 29226 | 燕王翔 | 正式行 | 口腔科 | 口内修复科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29226 | 无 |
| 5701 | 陈松龄 | 正式行 | 口腔科 | 口腔科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5701 | 无 |
| 5703 | 冯崇锦 | 正式行 | 口腔科 | 口腔科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5703 | 无 |
| 5705 | 王安训 | 正式行 | 口腔科 | 口腔科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5705 | 无 |
| 5706 | 杨军英 | 正式行 | 口腔科 | 口腔科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5706 | 无 |
| 5707 | 张春元 | 正式行 | 口腔科 | 口腔科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5707 | 无 |
| 5708 | 陈宇 | 同名待甄别 | 口腔科 | 口腔科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5708 | 同名不同数字 ID 分行保留 |
| 5710 | 郭俊兵 | 正式行 | 口腔科 | 口腔科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5710 | 无 |
| 5711 | 黄代营 | 正式行 | 口腔科 | 口腔科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5711 | 无 |
| 5777 | 安珂 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5777 | 无 |
| 5784 | 陈宇 | 同名待甄别 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5784 | 同名不同数字 ID 分行保留 |
| 5785 | 房洁渝 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5785 | 无 |
| 5778 | 冯霞 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5778 | 无 |
| 5780 | 黄雄庆 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5780 | 无 |
| 5779 | 黄文起 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5779 | 无 |
| 5786 | 江楠 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5786 | 无 |
| 5781 | 孙来保 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5781 | 无 |
| 5791 | 肖颖 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5791 | 无 |
| 5782 | 肖亮灿 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5782 | 无 |
| 5783 | 徐康清 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5783 | 无 |
| 5795 | 张旭宇 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5795 | 无 |
| 5794 | 张劲军 | 正式行 | 麻醉科 | 麻醉科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5794 | 无 |
| 5787 | 林世清 | 正式行 | 麻醉科 | 麻醉科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5787 | 无 |
| 39253 | 刘家欣 | 正式行 | 麻醉科 | 麻醉科 | 副高 | 1 | https://www.fahsysu.org.cn/node/39253 | 无 |
| 5788 | 莫利求 | 正式行 | 麻醉科 | 麻醉科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5788 | 无 |
| 36757 | 丘煜鑫 | 正式行 | 麻醉科 | 麻醉科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36757 | 无 |
| 5790 | 王钟兴 | 正式行 | 麻醉科 | 麻醉科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5790 | 无 |
| 775 | 刘俊茹 | 正式行 | 内科 | 血液内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/775 | 无 |
| 768 | 李娟 | 正式行 | 内科 | 血液内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/768 | 无 |
| 770 | 童秀珍 | 正式行 | 内科 | 血液内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/770 | 无 |
| 771 | 许多荣 | 正式行 | 内科 | 血液内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/771 | 无 |
| 779 | 邹外一 | 正式行 | 内科 | 血液内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/779 | 无 |
| 773 | 周振海 | 正式行 | 内科 | 血液内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/773 | 无 |
| 772 | 郑冬 | 正式行 | 内科 | 血液内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/772 | 无 |
| 32822 | 谷景立 | 正式行 | 内科 | 血液内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/32822 | 无 |
| 774 | 黄蓓晖 | 正式行 | 内科 | 血液内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/774 | 无 |
| 35916 | 李晓哲 | 正式行 | 内科 | 血液内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35916 | 无 |
| 777 | 苏畅 | 正式行 | 内科 | 血液内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/777 | 无 |
| 778 | 王荷花 | 正式行 | 内科 | 血液内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/778 | 无 |
| 781 | 陈旻湖 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/781 | 无 |
| 793 | 陈白莉 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/793 | 无 |
| 782 | 何瑶 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/782 | 无 |
| 23536 | 毛仁 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/23536 | 无 |
| 785 | 彭穗 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/785 | 无 |
| 786 | 任明 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/786 | 无 |
| 787 | 王锦辉 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/787 | 无 |
| 789 | 熊理守 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/789 | 无 |
| 795 | 邢象斌 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/795 | 无 |
| 788 | 肖英莲 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/788 | 无 |
| 792 | 朱森林 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/792 | 无 |
| 796 | 张宁 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/796 | 无 |
| 797 | 张盛洪 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/797 | 无 |
| 790 | 曾志荣 | 正式行 | 内科 | 消化内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/790 | 无 |
| 29397 | 冯瑞 | 正式行 | 内科 | 消化内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29397 | 无 |
| 35760 | 李莉 | 正式行 | 内科 | 消化内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35760 | 无 |
| 25717 | 邱云 | 正式行 | 内科 | 消化内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25717 | 无 |
| 794 | 王锦萍 | 正式行 | 内科 | 消化内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/794 | 无 |
| 38455 | 熊珊珊 | 正式行 | 内科 | 消化内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38455 | 无 |
| 798 | 郭禹标 | 正式行 | 内科 | 呼吸与危重症医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/798 | 无 |
| 806 | 廖槐 | 正式行 | 内科 | 呼吸与危重症医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/806 | 无 |
| 807 | 罗益锋 | 正式行 | 内科 | 呼吸与危重症医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/807 | 无 |
| 799 | 唐可京 | 正式行 | 内科 | 呼吸与危重症医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/799 | 无 |
| 800 | 谢灿茂 | 正式行 | 内科 | 呼吸与危重症医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/800 | 无 |
| 5771 | 曾勉 | 正式行 | 内科 | 呼吸与危重症医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5771 | 无 |
| 803 | 周燕斌 | 正式行 | 内科 | 呼吸与危重症医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/803 | 无 |
| 31204 | 陈海红 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31204 | 无 |
| 38132 | 杜宏春 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38132 | 无 |
| 804 | 关开泮 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/804 | 无 |
| 805 | 黄建强 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/805 | 无 |
| 38785 | 黄鑫炎 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38785 | 无 |
| 29237 | 匡煜坤 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29237 | 无 |
| 25606 | 林耿鹏 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25606 | 无 |
| 36747 | 刘杨丽 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36747 | 无 |
| 29503 | 谭卫平 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29503 | 无 |
| 31107 | 张菁 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31107 | 无 |
| 29370 | 朱坚华 | 正式行 | 内科 | 呼吸与危重症医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29370 | 无 |
| 809 | 陈伟英 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/809 | 无 |
| 808 | 陈崴 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/808 | 无 |
| 818 | 陈雄辉 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/818 | 无 |
| 810 | 郭群英 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/810 | 无 |
| 811 | 黄锋先 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/811 | 无 |
| 819 | 李剑波 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/819 | 无 |
| 814 | 刘庆华 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/814 | 无 |
| 813 | 李志坚 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/813 | 无 |
| 815 | 毛海萍 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/815 | 无 |
| 821 | 文琼 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/821 | 无 |
| 820 | 王欣 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/820 | 无 |
| 822 | 许元文 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/822 | 无 |
| 816 | 阳晓 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/816 | 无 |
| 823 | 张涤华 | 正式行 | 内科 | 肾内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/823 | 无 |
| 31193 | 黄娜娅 | 正式行 | 内科 | 肾内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31193 | 无 |
| 38311 | 吴海珊 | 正式行 | 内科 | 肾内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38311 | 无 |
| 36239 | 王娅婷 | 正式行 | 内科 | 肾内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36239 | 无 |
| 28957 | 夏茜 | 正式行 | 内科 | 肾内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/28957 | 无 |
| 32541 | 叶红坚 | 正式行 | 内科 | 肾内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/32541 | 无 |
| 29454 | 余健文 | 正式行 | 内科 | 肾内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29454 | 无 |
| 25780 | 郑勋华 | 正式行 | 内科 | 肾内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25780 | 无 |
| 35682 | 钟忠 | 正式行 | 内科 | 肾内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35682 | 无 |
| 824 | 连帆 | 正式行 | 内科 | 风湿免疫科 | 正高 | 1 | https://www.fahsysu.org.cn/node/824 | 无 |
| 825 | 梁柳琴 | 正式行 | 内科 | 风湿免疫科 | 正高 | 1 | https://www.fahsysu.org.cn/node/825 | 无 |
| 826 | 许韩师 | 正式行 | 内科 | 风湿免疫科 | 正高 | 1 | https://www.fahsysu.org.cn/node/826 | 无 |
| 25886 | 肖游君 | 正式行 | 内科 | 风湿免疫科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25886 | 无 |
| 827 | 杨念生 | 正式行 | 内科 | 风湿免疫科 | 正高 | 1 | https://www.fahsysu.org.cn/node/827 | 无 |
| 829 | 叶玉津 | 正式行 | 内科 | 风湿免疫科 | 正高 | 1 | https://www.fahsysu.org.cn/node/829 | 无 |
| 830 | 詹钟平 | 正式行 | 内科 | 风湿免疫科 | 正高 | 1 | https://www.fahsysu.org.cn/node/830 | 无 |
| 833 | 赵继军 | 正式行 | 内科 | 风湿免疫科 | 正高 | 1 | https://www.fahsysu.org.cn/node/833 | 无 |
| 831 | 邱茜 | 正式行 | 内科 | 风湿免疫科 | 副高 | 1 | https://www.fahsysu.org.cn/node/831 | 无 |
| 832 | 王双 | 正式行 | 内科 | 风湿免疫科 | 副高 | 1 | https://www.fahsysu.org.cn/node/832 | 无 |
| 834 | 曹筱佩 | 正式行 | 内科 | 内分泌内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/834 | 无 |
| 839 | 洪澍彬 | 正式行 | 内科 | 内分泌内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/839 | 无 |
| 840 | 黄知敏 | 正式行 | 内科 | 内分泌内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/840 | 无 |
| 841 | 李海 | 正式行 | 内科 | 内分泌内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/841 | 无 |
| 842 | 刘烈华 | 正式行 | 内科 | 内分泌内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/842 | 无 |
| 835 | 李延兵 | 正式行 | 内科 | 内分泌内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/835 | 无 |
| 836 | 廖志红 | 正式行 | 内科 | 内分泌内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/836 | 无 |
| 837 | 肖海鹏 | 正式行 | 内科 | 内分泌内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/837 | 无 |
| 844 | 喻爽 | 正式行 | 内科 | 内分泌内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/844 | 无 |
| 25419 | 刘娟 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25419 | 无 |
| 29409 | 崔卫玲 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29409 | 无 |
| 31190 | 何筱莹 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31190 | 无 |
| 38088 | 金洁雯 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38088 | 无 |
| 38121 | 柯伟健 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38121 | 无 |
| 35743 | 梁巍巍 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35743 | 无 |
| 843 | 闵运兵 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/843 | 无 |
| 29051 | 卫国红 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29051 | 无 |
| 29101 | 万学思 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29101 | 无 |
| 31191 | 许丽娟 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31191 | 无 |
| 29426 | 徐文明 | 正式行 | 内科 | 内分泌内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29426 | 无 |
| 845 | 崔毅 | 正式行 | 内科 | 内镜中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/845 | 无 |
| 28902 | 丁震 | 正式行 | 内科 | 内镜中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/28902 | 无 |
| 28391 | 谭年娣 | 正式行 | 内科 | 内镜中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/28391 | 无 |
| 30715 | 李佩文 | 正式行 | 内科 | 内科门诊 | 副高 | 1 | https://www.fahsysu.org.cn/node/30715 | 无 |
| 30714 | 王丹 | 正式行 | 内科 | 内科门诊 | 副高 | 1 | https://www.fahsysu.org.cn/node/30714 | 无 |
| 33071 | 龚迎迎 | 正式行 | 内科、特需医疗中心 | 老年病科、特需一科（老年病科） | 副高 | 2 | https://www.fahsysu.org.cn/node/33071 | 无 |
| 852 | 蒋小云 | 正式行 | 儿科 | 儿科一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/852 | 无 |
| 855 | 李燕虹 | 正式行 | 儿科 | 儿科一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/855 | 无 |
| 853 | 莫樱 | 正式行 | 儿科 | 儿科一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/853 | 无 |
| 35711 | 陈丽植 | 正式行 | 儿科 | 儿科一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35711 | 无 |
| 34056 | 陈美姬 | 正式行 | 儿科 | 儿科一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/34056 | 无 |
| 854 | 黄柳一 | 正式行 | 儿科 | 儿科一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/854 | 无 |
| 35630 | 姜梦婕 | 正式行 | 儿科 | 儿科一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35630 | 无 |
| 32512 | 裴瑜馨 | 正式行 | 儿科 | 儿科一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/32512 | 无 |
| 856 | 岳智慧 | 正式行 | 儿科 | 儿科一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/856 | 无 |
| 861 | 黄礼彬 | 正式行 | 儿科 | 儿科二科 | 正高 | 1 | https://www.fahsysu.org.cn/node/861 | 无 |
| 858 | 罗学群 | 正式行 | 儿科 | 儿科二科 | 正高 | 1 | https://www.fahsysu.org.cn/node/858 | 无 |
| 859 | 马华梅 | 正式行 | 儿科 | 儿科二科 | 正高 | 1 | https://www.fahsysu.org.cn/node/859 | 无 |
| 848 | 陈秋莉 | 正式行 | 儿科 | 儿科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/848 | 无 |
| 36749 | 郭松 | 正式行 | 儿科 | 儿科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36749 | 无 |
| 862 | 柯志勇 | 正式行 | 儿科 | 儿科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/862 | 无 |
| 35712 | 唐燕来 | 正式行 | 儿科 | 儿科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35712 | 无 |
| 31111 | 张军 | 正式行 | 儿科 | 儿科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31111 | 无 |
| 38128 | 张晓莉 | 正式行 | 儿科 | 儿科二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38128 | 无 |
| 863 | 黄越芳 | 正式行 | 儿科 | 儿科三科（新生儿科） | 正高 | 1 | https://www.fahsysu.org.cn/node/863 | 无 |
| 864 | 余慕雪 | 正式行 | 儿科 | 儿科三科（新生儿科） | 正高 | 1 | https://www.fahsysu.org.cn/node/864 | 无 |
| 865 | 李晓瑜 | 正式行 | 儿科 | 儿科三科（新生儿科） | 副高 | 1 | https://www.fahsysu.org.cn/node/865 | 无 |
| 867 | 刘美娜 | 正式行 | 儿科 | 儿科三科（新生儿科） | 副高 | 1 | https://www.fahsysu.org.cn/node/867 | 无 |
| 868 | 沈振宇 | 正式行 | 儿科 | 儿科三科（新生儿科） | 副高 | 1 | https://www.fahsysu.org.cn/node/868 | 无 |
| 866 | 李易娟 | 正式行 | 儿科 | 儿科ICU | 正高 | 1 | https://www.fahsysu.org.cn/node/866 | 无 |
| 33151 | 梁玉坚 | 正式行 | 儿科 | 儿科ICU | 副高 | 1 | https://www.fahsysu.org.cn/node/33151 | 无 |
| 33069 | 徐玲玲 | 正式行 | 儿科 | 儿科ICU | 副高 | 1 | https://www.fahsysu.org.cn/node/33069 | 无 |
| 870 | 裴中 | 正式行 | 神经科 | 神经科 | 正高 | 1 | https://www.fahsysu.org.cn/node/870 | 无 |
| 37040 | 王雪晶 | 正式行 | 神经科 | 神经科 | 正高 | 1 | https://www.fahsysu.org.cn/node/37040 | 无 |
| 872 | 曾进胜 | 正式行 | 神经科 | 神经科 | 正高 | 1 | https://www.fahsysu.org.cn/node/872 | 无 |
| 35659 | 陈裴 | 正式行 | 神经科 | 神经科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35659 | 无 |
| 38110 | 尚文锦 | 正式行 | 神经科 | 神经科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38110 | 无 |
| 880 | 周香雪 | 正式行 | 神经科 | 神经科 | 副高 | 1 | https://www.fahsysu.org.cn/node/880 | 无 |
| 882 | 李洵桦 | 正式行 | 神经科 | 神经一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/882 | 无 |
| 890 | 陈子怡 | 正式行 | 神经科 | 神经一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/890 | 无 |
| 34899 | 丁雪冰 | 正式行 | 神经科 | 神经一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/34899 | 无 |
| 875 | 廖松洁 | 正式行 | 神经科 | 神经一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/875 | 无 |
| 884 | 吴琪 | 正式行 | 神经科 | 神经一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/884 | 无 |
| 885 | 姚晓黎 | 正式行 | 神经科 | 神经一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/885 | 无 |
| 887 | 张为西 | 正式行 | 神经科 | 神经一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/887 | 无 |
| 889 | 陈定邦 | 正式行 | 神经科 | 神经一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/889 | 无 |
| 891 | 戴启麟 | 正式行 | 神经科 | 神经一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/891 | 无 |
| 893 | 丰岩清 | 正式行 | 神经科 | 神经一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/893 | 无 |
| 892 | 方莹莹 | 正式行 | 神经科 | 神经一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/892 | 无 |
| 29218 | 黄鑫 | 正式行 | 神经科 | 神经一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29218 | 无 |
| 32589 | 梁颖茵 | 正式行 | 神经科 | 神经一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/32589 | 无 |
| 33067 | 吴超 | 正式行 | 神经科 | 神经一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33067 | 无 |
| 33114 | 冼文彪 | 正式行 | 神经科 | 神经一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33114 | 无 |
| 33062 | 郑一帆 | 正式行 | 神经科 | 神经一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33062 | 无 |
| 896 | 黄海威 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/896 | 无 |
| 895 | 洪华 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/895 | 无 |
| 20863 | 刘刚 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/20863 | 无 |
| 35738 | 李玲 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/35738 | 无 |
| 898 | 盛文利 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/898 | 无 |
| 899 | 陶玉倩 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/899 | 无 |
| 877 | 邢世会 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/877 | 无 |
| 900 | 余剑 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/900 | 无 |
| 878 | 张健 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/878 | 无 |
| 35586 | 陈歆然 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/35586 | 无 |
| 873 | 党超 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/873 | 无 |
| 902 | 林健雯 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/902 | 无 |
| 20881 | 李骄星 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/20881 | 无 |
| 36940 | 林少英 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/36940 | 无 |
| 29069 | 欧紫琳 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/29069 | 无 |
| 876 | 王莹 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/876 | 无 |
| 903 | 曾缨 | 正式行 | 神经科 | 神经二科（脑血管病专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/903 | 无 |
| 904 | 范玉华 | 正式行 | 神经科 | 神经三科（神经功能专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/904 | 无 |
| 901 | 李晶晶 | 正式行 | 神经科 | 神经三科（神经功能专科） | 正高 | 1 | https://www.fahsysu.org.cn/node/901 | 无 |
| 29032 | 倪冠中 | 正式行 | 神经科 | 神经三科（神经功能专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/29032 | 无 |
| 26414 | 谭双全 | 正式行 | 神经科 | 神经三科（神经功能专科） | 副高 | 1 | https://www.fahsysu.org.cn/node/26414 | 无 |
| 869 | 陈玲 | 正式行 | 神经科 | 神经科ICU | 正高 | 1 | https://www.fahsysu.org.cn/node/869 | 无 |
| 881 | 冯慧宇 | 正式行 | 神经科 | 神经科ICU | 正高 | 1 | https://www.fahsysu.org.cn/node/881 | 无 |
| 33066 | 冯黎 | 正式行 | 神经科 | 神经科ICU | 副高 | 1 | https://www.fahsysu.org.cn/node/33066 | 无 |
| 20882 | 孙逊沙 | 正式行 | 神经科 | 神经科ICU | 副高 | 1 | https://www.fahsysu.org.cn/node/20882 | 无 |
| 33032 | 王海燕 | 正式行 | 神经科 | 神经科ICU | 副高 | 1 | https://www.fahsysu.org.cn/node/33032 | 无 |
| 879 | 周鸿雁 | 正式行 | 神经科 | 神经科ICU | 副高 | 1 | https://www.fahsysu.org.cn/node/879 | 无 |
| 906 | 崔立谦 | 正式行 | 神经科 | 临床心理科（门诊） | 正高 | 1 | https://www.fahsysu.org.cn/node/906 | 无 |
| 910 | 陈艺莉 | 正式行 | 心血管医学部 | 心血管内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/910 | 无 |
| 907 | 马虹 | 正式行 | 心血管医学部 | 心血管内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/907 | 无 |
| 909 | 王琴梅 | 正式行 | 心血管医学部 | 心血管内科 | 正高 | 1 | https://www.fahsysu.org.cn/node/909 | 无 |
| 5595 | 姚凤娟 | 正式行 | 心血管医学部、超声医学科 | 心血管内科、超声医学科 | 正高 | 2 | https://www.fahsysu.org.cn/node/5595 | 无 |
| 912 | 黄涌 | 正式行 | 心血管医学部 | 心血管内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/912 | 无 |
| 36851 | 罗劲华 | 正式行 | 心血管医学部 | 心血管内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36851 | 无 |
| 914 | 郑东诞 | 正式行 | 心血管医学部 | 心血管内科 | 副高 | 1 | https://www.fahsysu.org.cn/node/914 | 无 |
| 915 | 董吁钢 | 正式行 | 心血管医学部 | 心内一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/915 | 无 |
| 918 | 黄至斌 | 正式行 | 心血管医学部 | 心内一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/918 | 无 |
| 16991 | 罗初凡 | 正式行 | 心血管医学部 | 心内一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/16991 | 无 |
| 919 | 廖新学 | 正式行 | 心血管医学部 | 心内一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/919 | 无 |
| 920 | 唐安丽 | 正式行 | 心血管医学部 | 心内一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/920 | 无 |
| 928 | 吴杏 | 正式行 | 心血管医学部 | 心内一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/928 | 无 |
| 941 | 王礼春 | 正式行 | 心血管医学部 | 心内一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/941 | 无 |
| 23544 | 杨达雅 | 正式行 | 心血管医学部 | 心内一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/23544 | 无 |
| 929 | 庄晓东 | 正式行 | 心血管医学部 | 心内一科 | 正高 | 1 | https://www.fahsysu.org.cn/node/929 | 无 |
| 36850 | 冯冲 | 正式行 | 心血管医学部 | 心内一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36850 | 无 |
| 33149 | 郭玥 | 正式行 | 心血管医学部 | 心内一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33149 | 无 |
| 923 | 黄煜 | 正式行 | 心血管医学部 | 心内一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/923 | 无 |
| 35915 | 江竞舟 | 正式行 | 心血管医学部 | 心内一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35915 | 无 |
| 25427 | 卢贵华 | 正式行 | 心血管医学部 | 心内一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25427 | 无 |
| 924 | 冷秀玉 | 正式行 | 心血管医学部 | 心内一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/924 | 无 |
| 38081 | 熊振宇 | 正式行 | 心血管医学部 | 心内一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38081 | 无 |
| 922 | 曾武涛 | 正式行 | 心血管医学部 | 心内一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/922 | 无 |
| 29450 | 赵静静 | 正式行 | 心血管医学部 | 心内一科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29450 | 无 |
| 945 | 李怡 | 正式行 | 心血管医学部 | 心内二科（心介科） | 正高 | 1 | https://www.fahsysu.org.cn/node/945 | 无 |
| 946 | 龙明 | 正式行 | 心血管医学部 | 心内二科（心介科） | 正高 | 1 | https://www.fahsysu.org.cn/node/946 | 无 |
| 925 | 马跃东 | 正式行 | 心血管医学部 | 心内二科（心介科） | 正高 | 1 | https://www.fahsysu.org.cn/node/925 | 无 |
| 926 | 彭龙云 | 正式行 | 心血管医学部 | 心内二科（心介科） | 正高 | 1 | https://www.fahsysu.org.cn/node/926 | 无 |
| 944 | 胡承恒 | 正式行 | 心血管医学部 | 心内二科（心介科） | 副高 | 1 | https://www.fahsysu.org.cn/node/944 | 无 |
| 29234 | 胡洵 | 正式行 | 心血管医学部 | 心内二科（心介科） | 副高 | 1 | https://www.fahsysu.org.cn/node/29234 | 无 |
| 31090 | 刘岗 | 正式行 | 心血管医学部 | 心内二科（心介科） | 副高 | 1 | https://www.fahsysu.org.cn/node/31090 | 无 |
| 930 | 麦炜颐 | 正式行 | 心血管医学部 | 心内三科（高血压血管病） | 正高 | 1 | https://www.fahsysu.org.cn/node/930 | 无 |
| 931 | 欧志君 | 正式行 | 心血管医学部 | 心内三科（高血压血管病） | 正高 | 1 | https://www.fahsysu.org.cn/node/931 | 无 |
| 932 | 陶军 | 正式行 | 心血管医学部 | 心内三科（高血压血管病） | 正高 | 1 | https://www.fahsysu.org.cn/node/932 | 无 |
| 934 | 夏文豪 | 正式行 | 心血管医学部 | 心内三科（高血压血管病） | 正高 | 1 | https://www.fahsysu.org.cn/node/934 | 无 |
| 38071 | 何江 | 正式行 | 心血管医学部 | 心内三科（高血压血管病） | 副高 | 1 | https://www.fahsysu.org.cn/node/38071 | 无 |
| 927 | 苏晨 | 正式行 | 心血管医学部 | 心内三科（高血压血管病） | 副高 | 1 | https://www.fahsysu.org.cn/node/927 | 无 |
| 31145 | 徐诗岳 | 正式行 | 心血管医学部 | 心内三科（高血压血管病） | 副高 | 1 | https://www.fahsysu.org.cn/node/31145 | 无 |
| 29083 | 张小宇 | 正式行 | 心血管医学部 | 心内三科（高血压血管病） | 副高 | 1 | https://www.fahsysu.org.cn/node/29083 | 无 |
| 13569 | 张焰 | 正式行 | 心血管医学部 | 心内五科（心血管康复科） | 正高 | 1 | https://www.fahsysu.org.cn/node/13569 | 无 |
| 939 | 何建桂 | 正式行 | 心血管医学部 | 心内六科（CCU） | 正高 | 1 | https://www.fahsysu.org.cn/node/939 | 无 |
| 940 | 柳俊 | 正式行 | 心血管医学部 | 心内六科（CCU） | 正高 | 1 | https://www.fahsysu.org.cn/node/940 | 无 |
| 32844 | 刘晨 | 正式行 | 心血管医学部 | 心内六科（CCU） | 正高 | 1 | https://www.fahsysu.org.cn/node/32844 | 无 |
| 30375 | 吴德熙 | 正式行 | 心血管医学部 | 心内六科（CCU） | 正高 | 1 | https://www.fahsysu.org.cn/node/30375 | 无 |
| 942 | 吴素华 | 正式行 | 心血管医学部 | 心内六科（CCU） | 正高 | 1 | https://www.fahsysu.org.cn/node/942 | 无 |
| 38129 | 董玢 | 正式行 | 心血管医学部 | 心内六科（CCU） | 副高 | 1 | https://www.fahsysu.org.cn/node/38129 | 无 |
| 38087 | 黄沛森 | 正式行 | 心血管医学部 | 心内六科（CCU） | 副高 | 1 | https://www.fahsysu.org.cn/node/38087 | 无 |
| 38473 | 纪程程 | 正式行 | 心血管医学部 | 心内六科（CCU） | 副高 | 1 | https://www.fahsysu.org.cn/node/38473 | 无 |
| 35628 | 魏方菲 | 正式行 | 心血管医学部 | 心内六科（CCU） | 副高 | 1 | https://www.fahsysu.org.cn/node/35628 | 无 |
| 35080 | 吴泽璇 | 正式行 | 心血管医学部 | 心内六科（CCU） | 副高 | 1 | https://www.fahsysu.org.cn/node/35080 | 无 |
| 28386 | 薛睿聪 | 正式行 | 心血管医学部 | 心内六科（CCU） | 副高 | 1 | https://www.fahsysu.org.cn/node/28386 | 无 |
| 38540 | 朱文根 | 正式行 | 心血管医学部 | 心内六科（CCU） | 副高 | 1 | https://www.fahsysu.org.cn/node/38540 | 无 |
| 25429 | 李淑娟 | 正式行 | 心血管医学部 | 心血管儿科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25429 | 无 |
| 935 | 覃有振 | 正式行 | 心血管医学部 | 心血管儿科 | 正高 | 1 | https://www.fahsysu.org.cn/node/935 | 无 |
| 936 | 王慧深 | 正式行 | 心血管医学部 | 心血管儿科 | 正高 | 1 | https://www.fahsysu.org.cn/node/936 | 无 |
| 39252 | 巴宏军 | 正式行 | 心血管医学部 | 心血管儿科 | 副高 | 1 | https://www.fahsysu.org.cn/node/39252 | 无 |
| 938 | 朱玲 | 正式行 | 心血管医学部 | 心血管儿科 | 副高 | 1 | https://www.fahsysu.org.cn/node/938 | 无 |
| 947 | 陈光献 | 正式行 | 心血管医学部 | 心脏外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/947 | 无 |
| 5537 | 梁孟亚 | 正式行 | 心血管医学部 | 心脏外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5537 | 无 |
| 23546 | 区景松 | 正式行 | 心血管医学部 | 心脏外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/23546 | 无 |
| 949 | 吴钟凯 | 正式行 | 心血管医学部 | 心脏外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/949 | 无 |
| 950 | 徐颖琦 | 正式行 | 心血管医学部 | 心脏外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/950 | 无 |
| 952 | 殷胜利 | 正式行 | 心血管医学部 | 心脏外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/952 | 无 |
| 951 | 姚尖平 | 正式行 | 心血管医学部 | 心脏外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/951 | 无 |
| 953 | 张希 | 正式行 | 心血管医学部 | 心脏外科 | 正高 | 1 | https://www.fahsysu.org.cn/node/953 | 无 |
| 5538 | 熊迈 | 正式行 | 心血管医学部 | 心脏外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5538 | 无 |
| 25512 | 许哲 | 正式行 | 心血管医学部 | 心脏外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25512 | 无 |
| 23547 | 周立 | 正式行 | 心血管医学部 | 心脏外科 | 副高 | 1 | https://www.fahsysu.org.cn/node/23547 | 无 |
| 943 | 荣健 | 正式行 | 心血管医学部 | 体外循环科 | 正高 | 1 | https://www.fahsysu.org.cn/node/943 | 无 |
| 31409 | 黄勇 | 正式行 | 急诊科 | 急诊科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31409 | 无 |
| 5756 | 荆小莉 | 正式行 | 急诊科 | 急诊科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5756 | 无 |
| 20880 | 刘江辉 | 正式行 | 急诊科 | 急诊科 | 正高 | 1 | https://www.fahsysu.org.cn/node/20880 | 无 |
| 31405 | 刘志豪 | 正式行 | 急诊科 | 急诊科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31405 | 无 |
| 31406 | 魏红艳 | 正式行 | 急诊科 | 急诊科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31406 | 无 |
| 31410 | 王科科 | 正式行 | 急诊科 | 急诊科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31410 | 无 |
| 31442 | 徐嘉 | 正式行 | 急诊科 | 急诊科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31442 | 无 |
| 933 | 杨震 | 正式行 | 急诊科 | 急诊科 | 正高 | 1 | https://www.fahsysu.org.cn/node/933 | 无 |
| 5761 | 詹红 | 正式行 | 急诊科 | 急诊科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5761 | 无 |
| 35584 | 黄应雄 | 正式行 | 急诊科 | 急诊科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35584 | 无 |
| 31441 | 廖瑾莉 | 正式行 | 急诊科 | 急诊科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31441 | 无 |
| 5762 | 梁艳冰 | 正式行 | 急诊科 | 急诊科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5762 | 无 |
| 31407 | 叶子 | 正式行 | 急诊科 | 急诊科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31407 | 无 |
| 31408 | 郑梓煜 | 正式行 | 急诊科 | 急诊科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31408 | 无 |
| 5830 | 包勇 | 正式行 | 肿瘤中心 | 放射治疗科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5830 | 无 |
| 5837 | 陈勇 | 正式行 | 肿瘤中心 | 放射治疗科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5837 | 无 |
| 5833 | 彭振维 | 正式行 | 肿瘤中心 | 放射治疗科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5833 | 无 |
| 5834 | 任玉峰 | 正式行 | 肿瘤中心 | 放射治疗科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5834 | 无 |
| 5836 | 王岩 | 正式行 | 肿瘤中心 | 放射治疗科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5836 | 无 |
| 38145 | 毕月 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38145 | 无 |
| 5831 | 陈瑞莞 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5831 | 无 |
| 38113 | 何潇芳 | 同名待甄别 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38113 | 同名不同数字 ID 分行保留 |
| 33085 | 牛绍清 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33085 | 无 |
| 5832 | 彭芳 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5832 | 无 |
| 5835 | 沈国平 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5835 | 无 |
| 31088 | 王成涛 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31088 | 无 |
| 38114 | 韦广滟 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38114 | 无 |
| 35695 | 吴双 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35695 | 无 |
| 38116 | 王雪涔 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38116 | 无 |
| 29320 | 张群 | 正式行 | 肿瘤中心 | 放射治疗科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29320 | 无 |
| 5828 | 龙健婷 | 正式行 | 肿瘤中心 | 肿瘤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5828 | 无 |
| 25473 | 许丽霞 | 正式行 | 肿瘤中心 | 肿瘤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25473 | 无 |
| 5829 | 张家兴 | 正式行 | 肿瘤中心 | 肿瘤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5829 | 无 |
| 31146 | 陈翠 | 正式行 | 肿瘤中心 | 肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31146 | 无 |
| 35592 | 陈凯 | 正式行 | 肿瘤中心 | 肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35592 | 无 |
| 5827 | 戴强生 | 正式行 | 肿瘤中心 | 肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5827 | 无 |
| 25605 | 花蕊熙 | 正式行 | 肿瘤中心 | 肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25605 | 无 |
| 38613 | 何潇芳 | 同名待甄别 | 肿瘤中心 | 肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38613 | 同名不同数字 ID 分行保留 |
| 38108 | 汪芳 | 正式行 | 肿瘤中心 | 肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38108 | 无 |
| 31147 | 叶文 | 正式行 | 肿瘤中心 | 肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31147 | 无 |
| 28258 | 张梦萍 | 正式行 | 肿瘤中心 | 肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/28258 | 无 |
| 35705 | 郑胄三 | 正式行 | 肿瘤中心 | 肿瘤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35705 | 无 |
| 34804 | 成艳美 | 正式行 | 重症医学科 | 心胸外科ICU | 副高 | 1 | https://www.fahsysu.org.cn/node/34804 | 无 |
| 33314 | 王翠苹 | 正式行 | 重症医学科 | 心胸外科ICU | 副高 | 1 | https://www.fahsysu.org.cn/node/33314 | 无 |
| 33035 | 杨嵩 | 正式行 | 重症医学科 | 心胸外科ICU | 副高 | 1 | https://www.fahsysu.org.cn/node/33035 | 无 |
| 5715 | 陈泽雄 | 正式行 | 中医科 | 中医科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5715 | 无 |
| 5724 | 金明华 | 正式行 | 中医科 | 中医科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5724 | 无 |
| 5716 | 李琼 | 正式行 | 中医科 | 中医科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5716 | 无 |
| 5719 | 伍新林 | 正式行 | 中医科 | 中医科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5719 | 无 |
| 5720 | 张诗军 | 正式行 | 中医科 | 中医科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5720 | 无 |
| 20875 | 陈树清 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/20875 | 无 |
| 20876 | 邓伟 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/20876 | 无 |
| 5722 | 黄春莲 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5722 | 无 |
| 5723 | 黄颖娟 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5723 | 无 |
| 5726 | 林佑武 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5726 | 无 |
| 29052 | 刘嘉辉 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29052 | 无 |
| 5727 | 孟君 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5727 | 无 |
| 5728 | 孙保国 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5728 | 无 |
| 5729 | 谭畅 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5729 | 无 |
| 5730 | 韦志辉 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5730 | 无 |
| 20864 | 吴国珍 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/20864 | 无 |
| 38070 | 汪园园 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38070 | 无 |
| 25423 | 周厚明 | 正式行 | 中医科 | 中医科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25423 | 无 |
| 5735 | 陈木开 | 正式行 | 皮肤科 | 皮肤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5735 | 无 |
| 5736 | 韩建德 | 正式行 | 皮肤科 | 皮肤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5736 | 无 |
| 5737 | 罗迪青 | 正式行 | 皮肤科 | 皮肤科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5737 | 无 |
| 5741 | 陈小红 | 正式行 | 皮肤科 | 皮肤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5741 | 无 |
| 5744 | 廖绮曼 | 正式行 | 皮肤科 | 皮肤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5744 | 无 |
| 28714 | 刘隽华 | 正式行 | 皮肤科 | 皮肤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/28714 | 无 |
| 29212 | 马春光 | 正式行 | 皮肤科 | 皮肤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29212 | 无 |
| 31141 | 唐旭华 | 正式行 | 皮肤科 | 皮肤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31141 | 无 |
| 33309 | 叶艳婷 | 正式行 | 皮肤科 | 皮肤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33309 | 无 |
| 5747 | 周晖 | 正式行 | 皮肤科 | 皮肤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5747 | 无 |
| 34932 | 赵玉昆 | 正式行 | 皮肤科 | 皮肤科 | 副高 | 1 | https://www.fahsysu.org.cn/node/34932 | 无 |
| 5796 | 陈曦 | 正式行 | 康复医学科 | 康复医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5796 | 无 |
| 30753 | 陈少贞 | 正式行 | 康复医学科 | 康复医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/30753 | 无 |
| 5800 | 刘汉军 | 正式行 | 康复医学科 | 康复医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5800 | 无 |
| 5801 | 刘鹏 | 正式行 | 康复医学科 | 康复医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5801 | 无 |
| 5802 | 王楚怀 | 正式行 | 康复医学科 | 康复医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5802 | 无 |
| 38214 | 赵江莉 | 正式行 | 康复医学科 | 康复医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/38214 | 无 |
| 5803 | 丁明晖 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5803 | 无 |
| 36160 | 韩秀兰 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36160 | 无 |
| 33228 | 江沁 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33228 | 无 |
| 34219 | 梁崎 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/34219 | 无 |
| 33461 | 李咏雪 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33461 | 无 |
| 31102 | 冷雁 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31102 | 无 |
| 33224 | 吴秀勤 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33224 | 无 |
| 36204 | 张桂芳 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36204 | 无 |
| 35683 | 张珊珊 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35683 | 无 |
| 38126 | 张思韵 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38126 | 无 |
| 33153 | 张洲 | 正式行 | 康复医学科 | 康复医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33153 | 无 |
| 5554 | 初建平 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5554 | 无 |
| 5562 | 冯仕庭 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5562 | 无 |
| 5561 | 范淼 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5561 | 无 |
| 31701 | 关键 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31701 | 无 |
| 5563 | 郭燕 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5563 | 无 |
| 5564 | 李向民 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5564 | 无 |
| 31699 | 罗宴吉 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31699 | 无 |
| 31687 | 孟悛非 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31687 | 无 |
| 31702 | 彭振鹏 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31702 | 无 |
| 5558 | 沈冰奇 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5558 | 无 |
| 5567 | 孙灿辉 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5567 | 无 |
| 31691 | 王焕军 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31691 | 无 |
| 5570 | 余深平 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5570 | 无 |
| 5568 | 杨有优 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5568 | 无 |
| 5569 | 杨智云 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5569 | 无 |
| 5571 | 郑可国 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5571 | 无 |
| 31694 | 张小玲 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/31694 | 无 |
| 5559 | 张朝晖 | 正式行 | 医学影像科 | 放射诊断专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5559 | 无 |
| 5556 | 邝健谊 | 正式行 | 医学影像科 | 放射诊断专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5556 | 无 |
| 5555 | 江利 | 正式行 | 医学影像科 | 放射诊断专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5555 | 无 |
| 31686 | 李雪华 | 正式行 | 医学影像科 | 放射诊断专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31686 | 无 |
| 38312 | 王霁朏 | 正式行 | 医学影像科 | 放射诊断专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38312 | 无 |
| 31688 | 赵静 | 正式行 | 医学影像科 | 放射诊断专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31688 | 无 |
| 5573 | 黄勇慧 | 正式行 | 医学影像科 | 放射介入专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5573 | 无 |
| 5578 | 向贤宏 | 正式行 | 医学影像科 | 放射介入专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5578 | 无 |
| 5574 | 杨建勇 | 正式行 | 医学影像科 | 放射介入专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5574 | 无 |
| 5575 | 庄文权 | 正式行 | 医学影像科 | 放射介入专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5575 | 无 |
| 5576 | 郭文波 | 正式行 | 医学影像科 | 放射介入专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5576 | 无 |
| 25408 | 林润 | 正式行 | 医学影像科 | 放射介入专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25408 | 无 |
| 5577 | 谭国胜 | 正式行 | 医学影像科 | 放射介入专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5577 | 无 |
| 5580 | 范文哲 | 正式行 | 医学影像科 | 肿瘤介入科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5580 | 无 |
| 5581 | 王于 | 正式行 | 医学影像科 | 肿瘤介入科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5581 | 无 |
| 35812 | 吴艳琴 | 正式行 | 医学影像科 | 肿瘤介入科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35812 | 无 |
| 33148 | 姚望 | 正式行 | 医学影像科 | 肿瘤介入科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33148 | 无 |
| 35648 | 赵月 | 正式行 | 医学影像科 | 肿瘤介入科 | 副高 | 1 | https://www.fahsysu.org.cn/node/35648 | 无 |
| 30518 | 王晓燕 | 正式行 | 核医学科 | 核医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/30518 | 无 |
| 5548 | 张祥松 | 正式行 | 核医学科 | 核医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5548 | 无 |
| 5549 | 陈丹云 | 正式行 | 核医学科 | 核医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5549 | 无 |
| 5550 | 陈维安 | 正式行 | 核医学科 | 核医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5550 | 无 |
| 5553 | 岳殿超 | 正式行 | 核医学科 | 核医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5553 | 无 |
| 25889 | 陈立达 | 正式行 | 超声医学科 | 超声医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25889 | 无 |
| 32032 | 陈淑玲 | 正式行 | 超声医学科 | 超声医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/32032 | 无 |
| 5582 | 匡铭 | 同名待甄别 | 超声医学科 | 超声医学科、介入超声专科 | 正高 | 2 | https://www.fahsysu.org.cn/node/5582 | 同名不同数字 ID 分行保留 |
| 5583 | 刘东红 | 正式行 | 超声医学科 | 超声医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5583 | 无 |
| 5589 | 梁瑾瑜 | 正式行 | 超声医学科 | 超声医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5589 | 无 |
| 5593 | 王竹 | 正式行 | 超声医学科 | 超声医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5593 | 无 |
| 5592 | 王伟 | 同名待甄别 | 超声医学科 | 超声医学科、介入超声专科 | 正高 | 2 | https://www.fahsysu.org.cn/node/5592 | 同名不同数字 ID 分行保留 |
| 5585 | 谢红宁 | 正式行 | 超声医学科 | 超声医学科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5585 | 无 |
| 20891 | 徐明 | 正式行 | 超声医学科 | 超声医学科、介入超声专科 | 正高 | 2 | https://www.fahsysu.org.cn/node/20891 | 无 |
| 5594 | 谢晓华 | 正式行 | 超声医学科 | 超声医学科、介入超声专科 | 正高 | 2 | https://www.fahsysu.org.cn/node/5594 | 无 |
| 5586 | 谢晓燕 | 正式行 | 超声医学科 | 超声医学科、介入超声专科 | 正高 | 2 | https://www.fahsysu.org.cn/node/5586 | 无 |
| 5596 | 郑艳玲 | 正式行 | 超声医学科 | 超声医学科、介入超声专科 | 正高 | 2 | https://www.fahsysu.org.cn/node/5596 | 无 |
| 38734 | 程美清 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38734 | 无 |
| 31956 | 陈瑜君 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/31956 | 无 |
| 38208 | 段妤 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38208 | 无 |
| 5587 | 黄光亮 | 正式行 | 超声医学科 | 超声医学科、介入超声专科 | 副高 | 2 | https://www.fahsysu.org.cn/node/5587 | 无 |
| 38806 | 胡航通 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38806 | 无 |
| 32232 | 刘保娴 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/32232 | 无 |
| 5591 | 刘丽 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5591 | 无 |
| 33214 | 雷婷 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/33214 | 无 |
| 29084 | 李薇 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29084 | 无 |
| 38176 | 李晓菊 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38176 | 无 |
| 38936 | 阮思敏 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38936 | 无 |
| 38757 | 佟文娟 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38757 | 无 |
| 38152 | 谭洋 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38152 | 无 |
| 29158 | 庄博文 | 正式行 | 超声医学科 | 超声医学科、介入超声专科 | 副高 | 2 | https://www.fahsysu.org.cn/node/29158 | 无 |
| 36784 | 郑巧 | 正式行 | 超声医学科 | 超声医学科 | 副高 | 1 | https://www.fahsysu.org.cn/node/36784 | 无 |
| 33352 | 张晓儿 | 正式行 | 超声医学科 | 超声医学科、介入超声专科 | 副高 | 2 | https://www.fahsysu.org.cn/node/33352 | 无 |
| 20890 | 林满霞 | 正式行 | 超声医学科 | 介入超声专科 | 正高 | 1 | https://www.fahsysu.org.cn/node/20890 | 无 |
| 38693 | 黄通毅 | 正式行 | 超声医学科 | 介入超声专科 | 副高 | 1 | https://www.fahsysu.org.cn/node/38693 | 无 |
| 25838 | 刘敏 | 同名待甄别 | 医学检验科 | 医学检验科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25838 | 同名不同数字 ID 分行保留 |
| 25887 | 欧阳涓 | 正式行 | 医学检验科 | 医学检验科 | 正高 | 1 | https://www.fahsysu.org.cn/node/25887 | 无 |
| 5840 | 陈培松 | 正式行 | 医学检验科 | 医学检验科 | 副高 | 1 | https://www.fahsysu.org.cn/node/5840 | 无 |
| 5804 | 陈文芳 | 正式行 | 病理科 | 病理科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5804 | 无 |
| 5805 | 韩安家 | 正式行 | 病理科 | 病理科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5805 | 无 |
| 5808 | 彭挺生 | 正式行 | 病理科 | 病理科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5808 | 无 |
| 5816 | 王芬 | 正式行 | 病理科 | 病理科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5816 | 无 |
| 5809 | 王连唐 | 正式行 | 病理科 | 病理科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5809 | 无 |
| 5812 | 余俐 | 正式行 | 病理科 | 病理科 | 正高 | 1 | https://www.fahsysu.org.cn/node/5812 | 无 |
| 30447 | 刘大伟 | 正式行 | 病理科 | 病理科 | 副高 | 1 | https://www.fahsysu.org.cn/node/30447 | 无 |
| 38127 | 邸宇琴 | 正式行 | 分子诊断与基因检测中心 | 分子诊断与基因检测中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/38127 | 无 |
| 30465 | 陈杰 | 正式行 | 药学部 | 药学部 | 正高 | 1 | https://www.fahsysu.org.cn/node/30465 | 无 |
| 30466 | 陈攀 | 正式行 | 药学部 | 药学部 | 正高 | 1 | https://www.fahsysu.org.cn/node/30466 | 无 |
| 5817 | 黎曙霞 | 正式行 | 药学部 | 药学部 | 正高 | 1 | https://www.fahsysu.org.cn/node/5817 | 无 |
| 30467 | 唐欲博 | 正式行 | 药学部 | 药学部 | 副高 | 1 | https://www.fahsysu.org.cn/node/30467 | 无 |
| 33213 | 夏延哲 | 正式行 | 药学部 | 药学部 | 副高 | 1 | https://www.fahsysu.org.cn/node/33213 | 无 |
| 30468 | 曾嘉炜 | 正式行 | 药学部 | 药学部 | 副高 | 1 | https://www.fahsysu.org.cn/node/30468 | 无 |
| 30469 | 赵丽岩 | 正式行 | 药学部 | 药学部 | 副高 | 1 | https://www.fahsysu.org.cn/node/30469 | 无 |
| 29817 | 隋昳 | 正式行 | 临床营养科 | 临床营养科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29817 | 无 |
| 23548 | 王妍 | 正式行 | 健康管理中心 | 健康管理中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/23548 | 无 |
| 25337 | 张亚东 | 正式行 | 健康管理中心 | 健康管理中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/25337 | 无 |
| 5540 | 何文 | 正式行 | 特需医疗中心 | 特需一科（老年病科） | 正高 | 1 | https://www.fahsysu.org.cn/node/5540 | 无 |
| 5541 | 元刚 | 正式行 | 特需医疗中心 | 特需一科（老年病科） | 正高 | 1 | https://www.fahsysu.org.cn/node/5541 | 无 |
| 25416 | 劳敏曦 | 正式行 | 特需医疗中心 | 特需一科（老年病科） | 副高 | 1 | https://www.fahsysu.org.cn/node/25416 | 无 |
| 35681 | 邵奕嘉 | 正式行 | 特需医疗中心 | 特需一科（老年病科） | 副高 | 1 | https://www.fahsysu.org.cn/node/35681 | 无 |
| 32703 | 吴芳 | 正式行 | 特需医疗中心 | 特需一科（老年病科） | 副高 | 1 | https://www.fahsysu.org.cn/node/32703 | 无 |
| 29299 | 张玲 | 正式行 | 特需医疗中心 | 特需一科（老年病科） | 副高 | 1 | https://www.fahsysu.org.cn/node/29299 | 无 |
| 36759 | 丁美琳 | 正式行 | 特需医疗中心 | 特需二科 | 正高 | 1 | https://www.fahsysu.org.cn/node/36759 | 无 |
| 29070 | 李进 | 正式行 | 特需医疗中心 | 特需二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/29070 | 无 |
| 25837 | 苏磊 | 正式行 | 特需医疗中心 | 特需二科 | 副高 | 1 | https://www.fahsysu.org.cn/node/25837 | 无 |
| 657 | 陈锡林 | 正式行 | 特需医疗中心 | 特需三科 | 副高 | 1 | https://www.fahsysu.org.cn/node/657 | 无 |
| 29542 | 黄展鹏 | 正式行 | 转化医学研究中心 | 转化医学研究中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/29542 | 无 |
| 5820 | 纪卫东 | 正式行 | 转化医学研究中心 | 转化医学研究中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/5820 | 无 |
| 5821 | 林水宾 | 正式行 | 转化医学研究中心 | 转化医学研究中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/5821 | 无 |
| 5824 | 徐彩霞 | 正式行 | 转化医学研究中心 | 转化医学研究中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/5824 | 无 |
| 5823 | 杨蜀岚 | 正式行 | 转化医学研究中心 | 转化医学研究中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/5823 | 无 |
| 5822 | 邵兰 | 正式行 | 转化医学研究中心 | 转化医学研究中心 | 正高 | 1 | https://www.fahsysu.org.cn/node/5822 | 无 |
| 38111 | 王子洋 | 正式行 | 转化医学研究中心 | 转化医学研究中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/38111 | 无 |
| 38122 | 张灿峰 | 正式行 | 转化医学研究中心 | 转化医学研究中心 | 副高 | 1 | https://www.fahsysu.org.cn/node/38122 | 无 |

### 身份归并对账

- 正式身份：860 行；同一人归并 0 组；实质不同同名 8 组 / 16 行。

| 姓名 | 详情 ID | 裁决 | 原关系数 | 合并科室 | 主详情 | 理由 |
|---|---|---|---:|---|---|---|
| 郭宇 | 620 | 唯一身份 | 1 | 普通外科 | https://www.fahsysu.org.cn/node/620 | 无 |
| 詹文华 | 619 | 唯一身份 | 1 | 普通外科 | https://www.fahsysu.org.cn/node/619 | 无 |
| 陈昆 | 628 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/628 | 无 |
| 郭少雷 | 641 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/641 | 无 |
| 黄正松 | 632 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/632 | 无 |
| 黄权 | 631 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/631 | 无 |
| 何东升 | 630 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/630 | 无 |
| 刘金龙 | 634 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/634 | 无 |
| 梁丰 | 25607 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/25607 | 无 |
| 林佳平 | 633 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/633 | 无 |
| 刘雪松 | 32417 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/32417 | 无 |
| 毛志钢 | 645 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/645 | 无 |
| 齐铁伟 | 635 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/635 | 无 |
| 夏之柏 | 637 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/637 | 无 |
| 杨超 | 638 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/638 | 无 |
| 杨李轩 | 639 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/639 | 无 |
| 丁之明 | 29222 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/29222 | 无 |
| 何科君 | 33075 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/33075 | 无 |
| 金华伟 | 642 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/642 | 无 |
| 柯春龙 | 643 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/643 | 无 |
| 廖创新 | 644 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/644 | 无 |
| 谢宝树 | 35658 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/35658 | 无 |
| 徐桂兴 | 35088 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/35088 | 无 |
| 余振华 | 647 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/647 | 无 |
| 姚顺 | 35759 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/35759 | 无 |
| 杨帅 | 29225 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/29225 | 无 |
| 章昌明 | 35650 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/35650 | 无 |
| 赵坤 | 38215 | 唯一身份 | 1 | 神经外科 | https://www.fahsysu.org.cn/node/38215 | 无 |
| 陈蕾 | 666 | 唯一身份 | 1 | 烧伤与创面修复科 | https://www.fahsysu.org.cn/node/666 | 无 |
| 胡志成 | 667 | 唯一身份 | 1 | 烧伤与创面修复科 | https://www.fahsysu.org.cn/node/667 | 无 |
| 刘旭盛 | 660 | 唯一身份 | 1 | 烧伤与创面修复科 | https://www.fahsysu.org.cn/node/660 | 无 |
| 舒斌 | 668 | 唯一身份 | 1 | 烧伤与创面修复科 | https://www.fahsysu.org.cn/node/668 | 无 |
| 谢举临 | 663 | 唯一身份 | 1 | 烧伤与创面修复科 | https://www.fahsysu.org.cn/node/663 | 无 |
| 徐盈斌 | 664 | 唯一身份 | 1 | 烧伤与创面修复科 | https://www.fahsysu.org.cn/node/664 | 无 |
| 朱家源 | 665 | 唯一身份 | 1 | 烧伤与创面修复科 | https://www.fahsysu.org.cn/node/665 | 无 |
| 赵菁玲 | 31089 | 唯一身份 | 1 | 烧伤与创面修复科 | https://www.fahsysu.org.cn/node/31089 | 无 |
| 陈炜 | 671 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/671 | 无 |
| 陈俊星 | 669 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/669 | 无 |
| 陈凌武 | 732 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/732 | 无 |
| 陈旭 | 682 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/682 | 无 |
| 陈羽 | 681 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/681 | 无 |
| 戴宇平 | 672 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/672 | 无 |
| 邓春华 | 733 | 唯一身份 | 2 | 泌尿外科、男科 | https://www.fahsysu.org.cn/node/733 | 无 |
| 黄斌 | 683 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/683 | 无 |
| 罗俊航 | 26632 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/26632 | 无 |
| 李晓飞 | 674 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/674 | 无 |
| 梁月有 | 675 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/675 | 无 |
| 莫承强 | 685 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/685 | 无 |
| 毛晓鹏 | 684 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/684 | 无 |
| 丘少鹏 | 676 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/676 | 无 |
| 孙祥宙 | 734 | 唯一身份 | 2 | 泌尿外科、男科 | https://www.fahsysu.org.cn/node/734 | 无 |
| 王道虎 | 678 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/678 | 无 |
| 吴荣佩 | 679 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/679 | 无 |
| 郑伏甫 | 680 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/680 | 无 |
| 曹明欣 | 37245 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/37245 | 无 |
| 陈振华 | 31148 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/31148 | 无 |
| 邓立文 | 34185 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/34185 | 无 |
| 方咏 | 36760 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/36760 | 无 |
| 潘金成 | 25417 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/25417 | 无 |
| 韦锦焕 | 25418 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/25418 | 无 |
| 王文卫 | 686 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/686 | 无 |
| 王宗任 | 29157 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/29157 | 无 |
| 项勇 | 687 | 唯一身份 | 2 | 泌尿外科、男科 | https://www.fahsysu.org.cn/node/687 | 无 |
| 杨其运 | 31142 | 唯一身份 | 2 | 泌尿外科、男科 | https://www.fahsysu.org.cn/node/31142 | 无 |
| 张俊隆 | 38124 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/38124 | 无 |
| 庄锦涛 | 29148 | 同名待甄别 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/29148 | 同名不同数字 ID 分行保留 |
| 赵亮 | 34930 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/34930 | 无 |
| 曾钦松 | 25475 | 唯一身份 | 1 | 泌尿外科 | https://www.fahsysu.org.cn/node/25475 | 无 |
| 高勇 | 608 | 唯一身份 | 2 | 男科、生殖医学中心 | https://www.fahsysu.org.cn/node/608 | 无 |
| 涂响安 | 735 | 同名待甄别 | 1 | 男科 | https://www.fahsysu.org.cn/node/735 | 同名不同数字 ID 分行保留 |
| 刘钧澄 | 688 | 唯一身份 | 1 | 小儿外科 | https://www.fahsysu.org.cn/node/688 | 无 |
| 徐哲 | 33115 | 唯一身份 | 1 | 小儿外科 | https://www.fahsysu.org.cn/node/33115 | 无 |
| 周李 | 690 | 唯一身份 | 1 | 小儿外科 | https://www.fahsysu.org.cn/node/690 | 无 |
| 陈华东 | 35591 | 唯一身份 | 1 | 小儿外科 | https://www.fahsysu.org.cn/node/35591 | 无 |
| 蒋宏 | 31106 | 唯一身份 | 1 | 小儿外科 | https://www.fahsysu.org.cn/node/31106 | 无 |
| 张志崇 | 36848 | 唯一身份 | 1 | 小儿外科 | https://www.fahsysu.org.cn/node/36848 | 无 |
| 唐冰 | 662 | 唯一身份 | 1 | 整形外科 | https://www.fahsysu.org.cn/node/662 | 无 |
| 唐庆 | 36849 | 唯一身份 | 1 | 整形外科 | https://www.fahsysu.org.cn/node/36849 | 无 |
| 程钢 | 697 | 唯一身份 | 1 | 整形外科 | https://www.fahsysu.org.cn/node/697 | 无 |
| 许澍洽 | 33065 | 唯一身份 | 1 | 整形外科 | https://www.fahsysu.org.cn/node/33065 | 无 |
| 曾瑞曦 | 700 | 唯一身份 | 1 | 整形外科 | https://www.fahsysu.org.cn/node/700 | 无 |
| 张毅 | 36847 | 唯一身份 | 1 | 整形外科 | https://www.fahsysu.org.cn/node/36847 | 无 |
| 朱昭炜 | 31245 | 唯一身份 | 1 | 整形外科 | https://www.fahsysu.org.cn/node/31245 | 无 |
| 陈振光 | 701 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/701 | 无 |
| 程超 | 702 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/702 | 无 |
| 顾勇 | 703 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/703 | 无 |
| 罗红鹤 | 705 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/705 | 无 |
| 鲁建军 | 704 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/704 | 无 |
| 刘振国 | 25478 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/25478 | 无 |
| 巫国勇 | 706 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/706 | 无 |
| 雷艺炎 | 708 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/708 | 无 |
| 马俊 | 25425 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/25425 | 无 |
| 苏春华 | 709 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/709 | 无 |
| 曾博 | 35663 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/35663 | 无 |
| 邹健勇 | 25471 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/25471 | 无 |
| 张水深 | 31149 | 唯一身份 | 1 | 胸外科 | https://www.fahsysu.org.cn/node/31149 | 无 |
| 黄文生 | 5600 | 唯一身份 | 1 | 外科门诊 | https://www.fahsysu.org.cn/node/5600 | 无 |
| 李强 | 720 | 唯一身份 | 1 | 外科门诊 | https://www.fahsysu.org.cn/node/720 | 无 |
| 常光其 | 621 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/621 | 无 |
| 胡作军 | 622 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/622 | 无 |
| 王冕 | 627 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/627 | 无 |
| 武日东 | 25317 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/25317 | 无 |
| 姚陈 | 625 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/625 | 无 |
| 李梓伦 | 626 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/626 | 无 |
| 汪睿 | 38171 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/38171 | 无 |
| 王斯文 | 35587 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/35587 | 无 |
| 吴伟滨 | 33031 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/33031 | 无 |
| 王折存 | 35672 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/35672 | 无 |
| 周昱 | 38598 | 唯一身份 | 1 | 血管外科 | https://www.fahsysu.org.cn/node/38598 | 无 |
| 吕伟明 | 724 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/724 | 无 |
| 李松奇 | 721 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/721 | 无 |
| 徐向东 | 729 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/729 | 无 |
| 林维浩 | 726 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/726 | 无 |
| 林勃 | 38174 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/38174 | 无 |
| 林小红 | 29456 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/29456 | 无 |
| 单臻 | 25543 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/25543 | 无 |
| 吴壮宏 | 728 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/728 | 无 |
| 朱易凡 | 36846 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/36846 | 无 |
| 张展强 | 33150 | 唯一身份 | 1 | 甲状腺外科 | https://www.fahsysu.org.cn/node/33150 | 无 |
| 林颖 | 723 | 唯一身份 | 1 | 乳腺外科 | https://www.fahsysu.org.cn/node/723 | 无 |
| 王深明 | 624 | 唯一身份 | 1 | 乳腺外科 | https://www.fahsysu.org.cn/node/624 | 无 |
| 张赟建 | 731 | 唯一身份 | 1 | 乳腺外科 | https://www.fahsysu.org.cn/node/731 | 无 |
| 匡夏颖 | 31358 | 唯一身份 | 1 | 乳腺外科 | https://www.fahsysu.org.cn/node/31358 | 无 |
| 邵楠 | 727 | 唯一身份 | 1 | 乳腺外科 | https://www.fahsysu.org.cn/node/727 | 无 |
| 史雅薇 | 25781 | 唯一身份 | 1 | 乳腺外科 | https://www.fahsysu.org.cn/node/25781 | 无 |
| 于亮 | 730 | 唯一身份 | 1 | 乳腺外科 | https://www.fahsysu.org.cn/node/730 | 无 |
| 叶润仪 | 33081 | 唯一身份 | 1 | 乳腺外科 | https://www.fahsysu.org.cn/node/33081 | 无 |
| 胡文杰 | 658 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/658 | 无 |
| 何强 | 18614 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/18614 | 无 |
| 华赟鹏 | 649 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/649 | 无 |
| 匡铭 | 650 | 同名待甄别 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/650 | 同名不同数字 ID 分行保留 |
| 吕明德 | 5584 | 唯一身份 | 3 | 肝外科、超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/5584 | 无 |
| 梁力建 | 653 | 同名待甄别 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/653 | 同名不同数字 ID 分行保留 |
| 黎东明 | 651 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/651 | 无 |
| 李绍强 | 652 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/652 | 无 |
| 沈顺利 | 655 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/655 | 无 |
| 周奇 | 656 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/656 | 无 |
| 陈泽斌 | 35583 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/35583 | 无 |
| 钱柏锋 | 38160 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/38160 | 无 |
| 吴健 | 718 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/718 | 无 |
| 王恕同 | 35707 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/35707 | 无 |
| 谢文轩 | 31479 | 唯一身份 | 1 | 肝外科 | https://www.fahsysu.org.cn/node/31479 | 无 |
| 陈伟 | 716 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/716 | 无 |
| 陈流华 | 715 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/715 | 无 |
| 陈东 | 710 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/710 | 无 |
| 赖佳明 | 712 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/712 | 无 |
| 梁力建 | 21325 | 同名待甄别 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/21325 | 同名不同数字 ID 分行保留 |
| 殷晓煜 | 713 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/713 | 无 |
| 郑朝旭 | 714 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/714 | 无 |
| 张昆松 | 719 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/719 | 无 |
| 蔡建鹏 | 35694 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/35694 | 无 |
| 黄晨松 | 32861 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/32861 | 无 |
| 黄力 | 717 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/717 | 无 |
| 黄锡泰 | 33078 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/33078 | 无 |
| 彭洪 | 33079 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/33079 | 无 |
| 许琼聪 | 35662 | 唯一身份 | 1 | 胆胰外科 | https://www.fahsysu.org.cn/node/35662 | 无 |
| 陈剑辉 | 750 | 唯一身份 | 1 | 胃肠外科一科 | https://www.fahsysu.org.cn/node/750 | 无 |
| 蔡世荣 | 738 | 唯一身份 | 1 | 胃肠外科一科 | https://www.fahsysu.org.cn/node/738 | 无 |
| 侯洵 | 740 | 唯一身份 | 1 | 胃肠外科一科 | https://www.fahsysu.org.cn/node/740 | 无 |
| 何裕隆 | 746 | 唯一身份 | 1 | 胃肠外科一科 | https://www.fahsysu.org.cn/node/746 | 无 |
| 李引 | 741 | 唯一身份 | 1 | 胃肠外科一科 | https://www.fahsysu.org.cn/node/741 | 无 |
| 吴晖 | 742 | 唯一身份 | 1 | 胃肠外科一科 | https://www.fahsysu.org.cn/node/742 | 无 |
| 李广华 | 25542 | 唯一身份 | 1 | 胃肠外科一科 | https://www.fahsysu.org.cn/node/25542 | 无 |
| 叶锦宁 | 29238 | 唯一身份 | 1 | 胃肠外科一科 | https://www.fahsysu.org.cn/node/29238 | 无 |
| 翟二涛 | 33099 | 唯一身份 | 1 | 胃肠外科一科 | https://www.fahsysu.org.cn/node/33099 | 无 |
| 陈创奇 | 745 | 唯一身份 | 1 | 胃肠外科二科 | https://www.fahsysu.org.cn/node/745 | 无 |
| 马晋平 | 747 | 唯一身份 | 1 | 胃肠外科二科 | https://www.fahsysu.org.cn/node/747 | 无 |
| 宋新明 | 748 | 唯一身份 | 1 | 胃肠外科二科 | https://www.fahsysu.org.cn/node/748 | 无 |
| 王昭 | 752 | 唯一身份 | 1 | 胃肠外科二科 | https://www.fahsysu.org.cn/node/752 | 无 |
| 陈志辉 | 756 | 唯一身份 | 1 | 胃肠外科二科 | https://www.fahsysu.org.cn/node/756 | 无 |
| 彭建军 | 25422 | 唯一身份 | 1 | 胃肠外科二科 | https://www.fahsysu.org.cn/node/25422 | 无 |
| 王志雄 | 31152 | 唯一身份 | 1 | 胃肠外科二科 | https://www.fahsysu.org.cn/node/31152 | 无 |
| 余红兰 | 753 | 唯一身份 | 1 | 胃肠外科二科 | https://www.fahsysu.org.cn/node/753 | 无 |
| 杨世斌 | 23538 | 唯一身份 | 1 | 胃肠外科二科 | https://www.fahsysu.org.cn/node/23538 | 无 |
| 崔冀 | 757 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/757 | 无 |
| 宋武 | 754 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/754 | 无 |
| 谭敏 | 755 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/755 | 无 |
| 魏哲威 | 25668 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/25668 | 无 |
| 徐建波 | 743 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/743 | 无 |
| 张信华 | 744 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/744 | 无 |
| 戴伟钢 | 33147 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/33147 | 无 |
| 孙开宇 | 29215 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/29215 | 无 |
| 谭进富 | 759 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/759 | 无 |
| 袁凯涛 | 35629 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/35629 | 无 |
| 袁玉杰 | 29068 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/29068 | 无 |
| 左继东 | 29065 | 唯一身份 | 1 | 胃肠外科三科 | https://www.fahsysu.org.cn/node/29065 | 无 |
| 陈玉清 | 462 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/462 | 无 |
| 何勉 | 463 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/463 | 无 |
| 柯珮琪 | 465 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/465 | 无 |
| 刘军秀 | 582 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/582 | 无 |
| 牛刚 | 583 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/583 | 无 |
| 沈宏伟 | 584 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/584 | 无 |
| 沈慧敏 | 466 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/466 | 无 |
| 王宁宁 | 467 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/467 | 无 |
| 徐成康 | 575 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/575 | 无 |
| 谢洪哲 | 468 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/468 | 无 |
| 杨国奋 | 576 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/576 | 无 |
| 姚书忠 | 577 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/577 | 无 |
| 游泽山 | 578 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/578 | 无 |
| 陈明 | 25411 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/25411 | 无 |
| 曹铁凤 | 33348 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/33348 | 无 |
| 黄佳明 | 30713 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/30713 | 无 |
| 何科 | 580 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/580 | 无 |
| 何伟鹏 | 31105 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/31105 | 无 |
| 梁明懿 | 460 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/460 | 无 |
| 刘兴阳 | 29809 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/29809 | 无 |
| 梁炎春 | 25410 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/25410 | 无 |
| 谭金凤 | 35730 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/35730 | 无 |
| 王伟 | 25409 | 同名待甄别 | 1 | 妇科 | https://www.fahsysu.org.cn/node/25409 | 同名不同数字 ID 分行保留 |
| 徐漫漫 | 33308 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/33308 | 无 |
| 袁林静 | 33311 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/33311 | 无 |
| 赵云荷 | 29217 | 唯一身份 | 1 | 妇科 | https://www.fahsysu.org.cn/node/29217 | 无 |
| 陈海天 | 593 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/593 | 无 |
| 罗艳敏 | 589 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/589 | 无 |
| 刘斌 | 596 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/596 | 无 |
| 王子莲 | 590 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/590 | 无 |
| 王冬昱 | 598 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/598 | 无 |
| 周祎 | 591 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/591 | 无 |
| 蔡坚 | 592 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/592 | 无 |
| 陈汉青 | 29710 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/29710 | 无 |
| 黄林环 | 594 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/594 | 无 |
| 黄轩 | 595 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/595 | 无 |
| 何志明 | 25405 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/25405 | 无 |
| 刘立群 | 31955 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/31955 | 无 |
| 李珠玉 | 31109 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/31109 | 无 |
| 彭田玉 | 597 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/597 | 无 |
| 王晶 | 35627 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/35627 | 无 |
| 吴艳欣 | 29223 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/29223 | 无 |
| 祝彩霞 | 35590 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/35590 | 无 |
| 张颖 | 600 | 唯一身份 | 1 | 产科 | https://www.fahsysu.org.cn/node/600 | 无 |
| 陈明晖 | 606 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/606 | 无 |
| 麦庆云 | 601 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/601 | 无 |
| 王琼 | 602 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/602 | 无 |
| 徐艳文 | 603 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/603 | 无 |
| 周灿权 | 605 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/605 | 无 |
| 钟依平 | 604 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/604 | 无 |
| 古芳 | 26415 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/26415 | 无 |
| 高军 | 607 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/607 | 无 |
| 黄珈 | 609 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/609 | 无 |
| 胡晓坤 | 29220 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/29220 | 无 |
| 罗璐 | 612 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/612 | 无 |
| 李宇彬 | 611 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/611 | 无 |
| 苗本郁 | 613 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/613 | 无 |
| 王轶子 | 35769 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/35769 | 无 |
| 文扬幸 | 33092 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/33092 | 无 |
| 张丹 | 615 | 唯一身份 | 1 | 生殖医学中心 | https://www.fahsysu.org.cn/node/615 | 无 |
| 涂响安 | 31481 | 同名待甄别 | 1 | 生殖男科专科 | https://www.fahsysu.org.cn/node/31481 | 同名不同数字 ID 分行保留 |
| 庄锦涛 | 31480 | 同名待甄别 | 1 | 生殖男科专科 | https://www.fahsysu.org.cn/node/31480 | 同名不同数字 ID 分行保留 |
| 陈柏龄 | 5605 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5605 | 无 |
| 李泽民 | 5614 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5614 | 无 |
| 刘辉 | 25414 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/25414 | 无 |
| 彭新生 | 5608 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5608 | 无 |
| 苏培强 | 5609 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5609 | 无 |
| 王建儒 | 5617 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5617 | 无 |
| 万勇 | 5610 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5610 | 无 |
| 邹学农 | 5612 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5612 | 无 |
| 郑召民 | 5611 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5611 | 无 |
| 崔尚斌 | 31103 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/31103 | 无 |
| 戴驭虎 | 33113 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/33113 | 无 |
| 郭玮 | 31108 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/31108 | 无 |
| 黄阳亮 | 5613 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5613 | 无 |
| 李翔 | 38190 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/38190 | 无 |
| 刘希哲 | 33068 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/33068 | 无 |
| 王华 | 5616 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/5616 | 无 |
| 王乐 | 29146 | 唯一身份 | 1 | 脊柱外科 | https://www.fahsysu.org.cn/node/29146 | 无 |
| 傅明 | 5618 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5618 | 无 |
| 何爱珊 | 5619 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5619 | 无 |
| 康焱 | 5620 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5620 | 无 |
| 刘建华 | 29219 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/29219 | 无 |
| 廖威明 | 5621 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5621 | 无 |
| 盛璞义 | 5622 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5622 | 无 |
| 徐栋梁 | 5623 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5623 | 无 |
| 张紫机 | 5629 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5629 | 无 |
| 张志奇 | 5628 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5628 | 无 |
| 陈蔚深 | 31110 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/31110 | 无 |
| 古明晖 | 29033 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/29033 | 无 |
| 胡俊勇 | 5625 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5625 | 无 |
| 何沛恒 | 5624 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5624 | 无 |
| 孟繁钢 | 25537 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/25537 | 无 |
| 杨子波 | 5627 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/5627 | 无 |
| 赵潇艺 | 25536 | 唯一身份 | 1 | 关节外科 | https://www.fahsysu.org.cn/node/25536 | 无 |
| 邬培慧 | 5626 | 唯一身份 | 1 | 运动医学科 | https://www.fahsysu.org.cn/node/5626 | 无 |
| 黄纲 | 5630 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/5630 | 无 |
| 沈靖南 | 5631 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/5631 | 无 |
| 王永谦 | 25782 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/25782 | 无 |
| 谢显彪 | 5633 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/5633 | 无 |
| 尹军强 | 5632 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/5632 | 无 |
| 邹昌业 | 5634 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/5634 | 无 |
| 林调 | 29147 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/29147 | 无 |
| 涂剑 | 31104 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/31104 | 无 |
| 王博 | 29224 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/29224 | 无 |
| 赵志强 | 29124 | 唯一身份 | 1 | 骨肿瘤科 | https://www.fahsysu.org.cn/node/29124 | 无 |
| 顾立强 | 5635 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5635 | 无 |
| 刘小林 | 5636 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5636 | 无 |
| 李平 | 5639 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5639 | 无 |
| 戚剑 | 5640 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5640 | 无 |
| 郑灿镔 | 23551 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/23551 | 无 |
| 朱庆棠 | 5637 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5637 | 无 |
| 胡军 | 5638 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5638 | 无 |
| 秦本刚 | 5641 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5641 | 无 |
| 王洪刚 | 5643 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5643 | 无 |
| 向剑平 | 5644 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5644 | 无 |
| 易建华 | 5646 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5646 | 无 |
| 杨建涛 | 5645 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/5645 | 无 |
| 闫立伟 | 33064 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/33064 | 无 |
| 杨羿 | 38169 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/38169 | 无 |
| 周翔 | 25511 | 唯一身份 | 1 | 显微创伤外手科 | https://www.fahsysu.org.cn/node/25511 | 无 |
| 胡章威 | 38085 | 唯一身份 | 1 | 耳鼻咽喉科 | https://www.fahsysu.org.cn/node/38085 | 无 |
| 吴旋 | 5686 | 唯一身份 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/5686 | 无 |
| 熊观霞 | 5682 | 唯一身份 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/5682 | 无 |
| 陈垲钿 | 20862 | 唯一身份 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/20862 | 无 |
| 方淑斌 | 38089 | 唯一身份 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/38089 | 无 |
| 江广理 | 5683 | 唯一身份 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/5683 | 无 |
| 刘敏 | 5684 | 同名待甄别 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/5684 | 同名不同数字 ID 分行保留 |
| 任红苗 | 29050 | 唯一身份 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/29050 | 无 |
| 魏凡钦 | 5685 | 唯一身份 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/5685 | 无 |
| 王仙仁 | 30448 | 唯一身份 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/30448 | 无 |
| 庄惠文 | 5687 | 唯一身份 | 1 | 耳专科 | https://www.fahsysu.org.cn/node/5687 | 无 |
| 陈冬 | 5673 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5673 | 无 |
| 陈合新 | 5688 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5688 | 无 |
| 李健 | 5689 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5689 | 无 |
| 赖银妍 | 5693 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5693 | 无 |
| 史剑波 | 5690 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5690 | 无 |
| 文译辉 | 5694 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5694 | 无 |
| 徐睿 | 5691 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5691 | 无 |
| 许庚 | 5675 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5675 | 无 |
| 左可军 | 5695 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5695 | 无 |
| 陈德华 | 33080 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/33080 | 无 |
| 郭洁波 | 5692 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/5692 | 无 |
| 高文翔 | 31087 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/31087 | 无 |
| 李光启 | 30376 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/30376 | 无 |
| 钟华 | 33070 | 唯一身份 | 1 | 鼻专科 | https://www.fahsysu.org.cn/node/33070 | 无 |
| 雷文斌 | 5697 | 唯一身份 | 1 | 咽喉专科 | https://www.fahsysu.org.cn/node/5697 | 无 |
| 马仁强 | 25406 | 唯一身份 | 1 | 咽喉专科 | https://www.fahsysu.org.cn/node/25406 | 无 |
| 文卫平 | 5698 | 唯一身份 | 1 | 咽喉专科 | https://www.fahsysu.org.cn/node/5698 | 无 |
| 祝小林 | 5676 | 唯一身份 | 1 | 咽喉专科 | https://www.fahsysu.org.cn/node/5676 | 无 |
| 陈林 | 35791 | 唯一身份 | 1 | 咽喉专科 | https://www.fahsysu.org.cn/node/35791 | 无 |
| 邓洁 | 29067 | 唯一身份 | 1 | 咽喉专科 | https://www.fahsysu.org.cn/node/29067 | 无 |
| 王章锋 | 5680 | 唯一身份 | 1 | 咽喉专科 | https://www.fahsysu.org.cn/node/5680 | 无 |
| 付清玲 | 5674 | 唯一身份 | 1 | 变态反应专科 | https://www.fahsysu.org.cn/node/5674 | 无 |
| 黄刚 | 5664 | 唯一身份 | 2 | 肾移植专科、器官移植科 | https://www.fahsysu.org.cn/node/5664 | 无 |
| 邱江 | 5653 | 唯一身份 | 2 | 肾移植专科、器官移植科 | https://www.fahsysu.org.cn/node/5653 | 无 |
| 傅茜 | 35698 | 唯一身份 | 1 | 肾移植专科 | https://www.fahsysu.org.cn/node/35698 | 无 |
| 赵强 | 5671 | 唯一身份 | 2 | 肝移植专科、器官移植科 | https://www.fahsysu.org.cn/node/5671 | 无 |
| 唐云华 | 38159 | 唯一身份 | 1 | 肝移植专科 | https://www.fahsysu.org.cn/node/38159 | 无 |
| 陈国栋 | 5647 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5647 | 无 |
| 陈茂根 | 5658 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5658 | 无 |
| 郭志勇 | 5663 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5663 | 无 |
| 胡安斌 | 5650 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5650 | 无 |
| 何晓顺 | 5649 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5649 | 无 |
| 鞠卫强 | 5665 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5665 | 无 |
| 刘龙山 | 5667 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5667 | 无 |
| 马毅 | 5652 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5652 | 无 |
| 王东平 | 5655 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5655 | 无 |
| 王长希 | 5654 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5654 | 无 |
| 吴成林 | 5670 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5670 | 无 |
| 朱晓峰 | 5657 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5657 | 无 |
| 陈颖华 | 5659 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5659 | 无 |
| 邓素雄 | 5661 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5661 | 无 |
| 邓荣海 | 5660 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5660 | 无 |
| 李军 | 5666 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5666 | 无 |
| 王国栋 | 5668 | 唯一身份 | 1 | 器官移植科 | https://www.fahsysu.org.cn/node/5668 | 无 |
| 万鹏霞 | 5753 | 唯一身份 | 1 | 眼科 | https://www.fahsysu.org.cn/node/5753 | 无 |
| 陈婷婷 | 34343 | 唯一身份 | 1 | 眼科 | https://www.fahsysu.org.cn/node/34343 | 无 |
| 陈雪梅（曾用名：陈咏冲） | 5750 | 唯一身份 | 1 | 眼科 | https://www.fahsysu.org.cn/node/5750 | 无 |
| 甘世斌 | 20861 | 唯一身份 | 1 | 眼科 | https://www.fahsysu.org.cn/node/20861 | 无 |
| 霍丽君 | 5751 | 唯一身份 | 1 | 眼科 | https://www.fahsysu.org.cn/node/5751 | 无 |
| 苏毅华 | 33056 | 唯一身份 | 1 | 眼科 | https://www.fahsysu.org.cn/node/33056 | 无 |
| 余芬芬 | 33169 | 唯一身份 | 1 | 眼科 | https://www.fahsysu.org.cn/node/33169 | 无 |
| 朱文珲 | 5755 | 唯一身份 | 1 | 眼科 | https://www.fahsysu.org.cn/node/5755 | 无 |
| 何倩婷 | 25474 | 唯一身份 | 1 | 口腔颌面外科 | https://www.fahsysu.org.cn/node/25474 | 无 |
| 李祥 | 34931 | 唯一身份 | 1 | 口腔颌面外科 | https://www.fahsysu.org.cn/node/34931 | 无 |
| 舒大龙 | 38112 | 唯一身份 | 1 | 口腔颌面外科 | https://www.fahsysu.org.cn/node/38112 | 无 |
| 朱双喜 | 34929 | 唯一身份 | 1 | 口腔颌面外科 | https://www.fahsysu.org.cn/node/34929 | 无 |
| 陈珊 | 29277 | 唯一身份 | 1 | 口内修复科 | https://www.fahsysu.org.cn/node/29277 | 无 |
| 吉利 | 31338 | 唯一身份 | 1 | 口内修复科 | https://www.fahsysu.org.cn/node/31338 | 无 |
| 姜瑞 | 33076 | 唯一身份 | 1 | 口内修复科 | https://www.fahsysu.org.cn/node/33076 | 无 |
| 聂二民 | 29071 | 唯一身份 | 1 | 口内修复科 | https://www.fahsysu.org.cn/node/29071 | 无 |
| 彭伟 | 25785 | 唯一身份 | 1 | 口内修复科 | https://www.fahsysu.org.cn/node/25785 | 无 |
| 任静 | 38209 | 唯一身份 | 1 | 口内修复科 | https://www.fahsysu.org.cn/node/38209 | 无 |
| 燕王翔 | 29226 | 唯一身份 | 1 | 口内修复科 | https://www.fahsysu.org.cn/node/29226 | 无 |
| 陈松龄 | 5701 | 唯一身份 | 1 | 口腔科 | https://www.fahsysu.org.cn/node/5701 | 无 |
| 冯崇锦 | 5703 | 唯一身份 | 1 | 口腔科 | https://www.fahsysu.org.cn/node/5703 | 无 |
| 王安训 | 5705 | 唯一身份 | 1 | 口腔科 | https://www.fahsysu.org.cn/node/5705 | 无 |
| 杨军英 | 5706 | 唯一身份 | 1 | 口腔科 | https://www.fahsysu.org.cn/node/5706 | 无 |
| 张春元 | 5707 | 唯一身份 | 1 | 口腔科 | https://www.fahsysu.org.cn/node/5707 | 无 |
| 陈宇 | 5708 | 同名待甄别 | 1 | 口腔科 | https://www.fahsysu.org.cn/node/5708 | 同名不同数字 ID 分行保留 |
| 郭俊兵 | 5710 | 唯一身份 | 1 | 口腔科 | https://www.fahsysu.org.cn/node/5710 | 无 |
| 黄代营 | 5711 | 唯一身份 | 1 | 口腔科 | https://www.fahsysu.org.cn/node/5711 | 无 |
| 安珂 | 5777 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5777 | 无 |
| 陈宇 | 5784 | 同名待甄别 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5784 | 同名不同数字 ID 分行保留 |
| 房洁渝 | 5785 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5785 | 无 |
| 冯霞 | 5778 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5778 | 无 |
| 黄雄庆 | 5780 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5780 | 无 |
| 黄文起 | 5779 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5779 | 无 |
| 江楠 | 5786 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5786 | 无 |
| 孙来保 | 5781 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5781 | 无 |
| 肖颖 | 5791 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5791 | 无 |
| 肖亮灿 | 5782 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5782 | 无 |
| 徐康清 | 5783 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5783 | 无 |
| 张旭宇 | 5795 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5795 | 无 |
| 张劲军 | 5794 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5794 | 无 |
| 林世清 | 5787 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5787 | 无 |
| 刘家欣 | 39253 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/39253 | 无 |
| 莫利求 | 5788 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5788 | 无 |
| 丘煜鑫 | 36757 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/36757 | 无 |
| 王钟兴 | 5790 | 唯一身份 | 1 | 麻醉科 | https://www.fahsysu.org.cn/node/5790 | 无 |
| 刘俊茹 | 775 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/775 | 无 |
| 李娟 | 768 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/768 | 无 |
| 童秀珍 | 770 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/770 | 无 |
| 许多荣 | 771 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/771 | 无 |
| 邹外一 | 779 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/779 | 无 |
| 周振海 | 773 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/773 | 无 |
| 郑冬 | 772 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/772 | 无 |
| 谷景立 | 32822 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/32822 | 无 |
| 黄蓓晖 | 774 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/774 | 无 |
| 李晓哲 | 35916 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/35916 | 无 |
| 苏畅 | 777 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/777 | 无 |
| 王荷花 | 778 | 唯一身份 | 1 | 血液内科 | https://www.fahsysu.org.cn/node/778 | 无 |
| 陈旻湖 | 781 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/781 | 无 |
| 陈白莉 | 793 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/793 | 无 |
| 何瑶 | 782 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/782 | 无 |
| 毛仁 | 23536 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/23536 | 无 |
| 彭穗 | 785 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/785 | 无 |
| 任明 | 786 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/786 | 无 |
| 王锦辉 | 787 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/787 | 无 |
| 熊理守 | 789 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/789 | 无 |
| 邢象斌 | 795 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/795 | 无 |
| 肖英莲 | 788 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/788 | 无 |
| 朱森林 | 792 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/792 | 无 |
| 张宁 | 796 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/796 | 无 |
| 张盛洪 | 797 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/797 | 无 |
| 曾志荣 | 790 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/790 | 无 |
| 冯瑞 | 29397 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/29397 | 无 |
| 李莉 | 35760 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/35760 | 无 |
| 邱云 | 25717 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/25717 | 无 |
| 王锦萍 | 794 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/794 | 无 |
| 熊珊珊 | 38455 | 唯一身份 | 1 | 消化内科 | https://www.fahsysu.org.cn/node/38455 | 无 |
| 郭禹标 | 798 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/798 | 无 |
| 廖槐 | 806 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/806 | 无 |
| 罗益锋 | 807 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/807 | 无 |
| 唐可京 | 799 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/799 | 无 |
| 谢灿茂 | 800 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/800 | 无 |
| 曾勉 | 5771 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/5771 | 无 |
| 周燕斌 | 803 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/803 | 无 |
| 陈海红 | 31204 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/31204 | 无 |
| 杜宏春 | 38132 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/38132 | 无 |
| 关开泮 | 804 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/804 | 无 |
| 黄建强 | 805 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/805 | 无 |
| 黄鑫炎 | 38785 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/38785 | 无 |
| 匡煜坤 | 29237 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/29237 | 无 |
| 林耿鹏 | 25606 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/25606 | 无 |
| 刘杨丽 | 36747 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/36747 | 无 |
| 谭卫平 | 29503 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/29503 | 无 |
| 张菁 | 31107 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/31107 | 无 |
| 朱坚华 | 29370 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.fahsysu.org.cn/node/29370 | 无 |
| 陈伟英 | 809 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/809 | 无 |
| 陈崴 | 808 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/808 | 无 |
| 陈雄辉 | 818 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/818 | 无 |
| 郭群英 | 810 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/810 | 无 |
| 黄锋先 | 811 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/811 | 无 |
| 李剑波 | 819 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/819 | 无 |
| 刘庆华 | 814 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/814 | 无 |
| 李志坚 | 813 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/813 | 无 |
| 毛海萍 | 815 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/815 | 无 |
| 文琼 | 821 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/821 | 无 |
| 王欣 | 820 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/820 | 无 |
| 许元文 | 822 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/822 | 无 |
| 阳晓 | 816 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/816 | 无 |
| 张涤华 | 823 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/823 | 无 |
| 黄娜娅 | 31193 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/31193 | 无 |
| 吴海珊 | 38311 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/38311 | 无 |
| 王娅婷 | 36239 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/36239 | 无 |
| 夏茜 | 28957 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/28957 | 无 |
| 叶红坚 | 32541 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/32541 | 无 |
| 余健文 | 29454 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/29454 | 无 |
| 郑勋华 | 25780 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/25780 | 无 |
| 钟忠 | 35682 | 唯一身份 | 1 | 肾内科 | https://www.fahsysu.org.cn/node/35682 | 无 |
| 连帆 | 824 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/824 | 无 |
| 梁柳琴 | 825 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/825 | 无 |
| 许韩师 | 826 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/826 | 无 |
| 肖游君 | 25886 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/25886 | 无 |
| 杨念生 | 827 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/827 | 无 |
| 叶玉津 | 829 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/829 | 无 |
| 詹钟平 | 830 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/830 | 无 |
| 赵继军 | 833 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/833 | 无 |
| 邱茜 | 831 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/831 | 无 |
| 王双 | 832 | 唯一身份 | 1 | 风湿免疫科 | https://www.fahsysu.org.cn/node/832 | 无 |
| 曹筱佩 | 834 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/834 | 无 |
| 洪澍彬 | 839 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/839 | 无 |
| 黄知敏 | 840 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/840 | 无 |
| 李海 | 841 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/841 | 无 |
| 刘烈华 | 842 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/842 | 无 |
| 李延兵 | 835 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/835 | 无 |
| 廖志红 | 836 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/836 | 无 |
| 肖海鹏 | 837 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/837 | 无 |
| 喻爽 | 844 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/844 | 无 |
| 刘娟 | 25419 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/25419 | 无 |
| 崔卫玲 | 29409 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/29409 | 无 |
| 何筱莹 | 31190 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/31190 | 无 |
| 金洁雯 | 38088 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/38088 | 无 |
| 柯伟健 | 38121 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/38121 | 无 |
| 梁巍巍 | 35743 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/35743 | 无 |
| 闵运兵 | 843 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/843 | 无 |
| 卫国红 | 29051 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/29051 | 无 |
| 万学思 | 29101 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/29101 | 无 |
| 许丽娟 | 31191 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/31191 | 无 |
| 徐文明 | 29426 | 唯一身份 | 1 | 内分泌内科 | https://www.fahsysu.org.cn/node/29426 | 无 |
| 崔毅 | 845 | 唯一身份 | 1 | 内镜中心 | https://www.fahsysu.org.cn/node/845 | 无 |
| 丁震 | 28902 | 唯一身份 | 1 | 内镜中心 | https://www.fahsysu.org.cn/node/28902 | 无 |
| 谭年娣 | 28391 | 唯一身份 | 1 | 内镜中心 | https://www.fahsysu.org.cn/node/28391 | 无 |
| 李佩文 | 30715 | 唯一身份 | 1 | 内科门诊 | https://www.fahsysu.org.cn/node/30715 | 无 |
| 王丹 | 30714 | 唯一身份 | 1 | 内科门诊 | https://www.fahsysu.org.cn/node/30714 | 无 |
| 龚迎迎 | 33071 | 唯一身份 | 2 | 老年病科、特需一科（老年病科） | https://www.fahsysu.org.cn/node/33071 | 无 |
| 蒋小云 | 852 | 唯一身份 | 1 | 儿科一科 | https://www.fahsysu.org.cn/node/852 | 无 |
| 李燕虹 | 855 | 唯一身份 | 1 | 儿科一科 | https://www.fahsysu.org.cn/node/855 | 无 |
| 莫樱 | 853 | 唯一身份 | 1 | 儿科一科 | https://www.fahsysu.org.cn/node/853 | 无 |
| 陈丽植 | 35711 | 唯一身份 | 1 | 儿科一科 | https://www.fahsysu.org.cn/node/35711 | 无 |
| 陈美姬 | 34056 | 唯一身份 | 1 | 儿科一科 | https://www.fahsysu.org.cn/node/34056 | 无 |
| 黄柳一 | 854 | 唯一身份 | 1 | 儿科一科 | https://www.fahsysu.org.cn/node/854 | 无 |
| 姜梦婕 | 35630 | 唯一身份 | 1 | 儿科一科 | https://www.fahsysu.org.cn/node/35630 | 无 |
| 裴瑜馨 | 32512 | 唯一身份 | 1 | 儿科一科 | https://www.fahsysu.org.cn/node/32512 | 无 |
| 岳智慧 | 856 | 唯一身份 | 1 | 儿科一科 | https://www.fahsysu.org.cn/node/856 | 无 |
| 黄礼彬 | 861 | 唯一身份 | 1 | 儿科二科 | https://www.fahsysu.org.cn/node/861 | 无 |
| 罗学群 | 858 | 唯一身份 | 1 | 儿科二科 | https://www.fahsysu.org.cn/node/858 | 无 |
| 马华梅 | 859 | 唯一身份 | 1 | 儿科二科 | https://www.fahsysu.org.cn/node/859 | 无 |
| 陈秋莉 | 848 | 唯一身份 | 1 | 儿科二科 | https://www.fahsysu.org.cn/node/848 | 无 |
| 郭松 | 36749 | 唯一身份 | 1 | 儿科二科 | https://www.fahsysu.org.cn/node/36749 | 无 |
| 柯志勇 | 862 | 唯一身份 | 1 | 儿科二科 | https://www.fahsysu.org.cn/node/862 | 无 |
| 唐燕来 | 35712 | 唯一身份 | 1 | 儿科二科 | https://www.fahsysu.org.cn/node/35712 | 无 |
| 张军 | 31111 | 唯一身份 | 1 | 儿科二科 | https://www.fahsysu.org.cn/node/31111 | 无 |
| 张晓莉 | 38128 | 唯一身份 | 1 | 儿科二科 | https://www.fahsysu.org.cn/node/38128 | 无 |
| 黄越芳 | 863 | 唯一身份 | 1 | 儿科三科（新生儿科） | https://www.fahsysu.org.cn/node/863 | 无 |
| 余慕雪 | 864 | 唯一身份 | 1 | 儿科三科（新生儿科） | https://www.fahsysu.org.cn/node/864 | 无 |
| 李晓瑜 | 865 | 唯一身份 | 1 | 儿科三科（新生儿科） | https://www.fahsysu.org.cn/node/865 | 无 |
| 刘美娜 | 867 | 唯一身份 | 1 | 儿科三科（新生儿科） | https://www.fahsysu.org.cn/node/867 | 无 |
| 沈振宇 | 868 | 唯一身份 | 1 | 儿科三科（新生儿科） | https://www.fahsysu.org.cn/node/868 | 无 |
| 李易娟 | 866 | 唯一身份 | 1 | 儿科ICU | https://www.fahsysu.org.cn/node/866 | 无 |
| 梁玉坚 | 33151 | 唯一身份 | 1 | 儿科ICU | https://www.fahsysu.org.cn/node/33151 | 无 |
| 徐玲玲 | 33069 | 唯一身份 | 1 | 儿科ICU | https://www.fahsysu.org.cn/node/33069 | 无 |
| 裴中 | 870 | 唯一身份 | 1 | 神经科 | https://www.fahsysu.org.cn/node/870 | 无 |
| 王雪晶 | 37040 | 唯一身份 | 1 | 神经科 | https://www.fahsysu.org.cn/node/37040 | 无 |
| 曾进胜 | 872 | 唯一身份 | 1 | 神经科 | https://www.fahsysu.org.cn/node/872 | 无 |
| 陈裴 | 35659 | 唯一身份 | 1 | 神经科 | https://www.fahsysu.org.cn/node/35659 | 无 |
| 尚文锦 | 38110 | 唯一身份 | 1 | 神经科 | https://www.fahsysu.org.cn/node/38110 | 无 |
| 周香雪 | 880 | 唯一身份 | 1 | 神经科 | https://www.fahsysu.org.cn/node/880 | 无 |
| 李洵桦 | 882 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/882 | 无 |
| 陈子怡 | 890 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/890 | 无 |
| 丁雪冰 | 34899 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/34899 | 无 |
| 廖松洁 | 875 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/875 | 无 |
| 吴琪 | 884 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/884 | 无 |
| 姚晓黎 | 885 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/885 | 无 |
| 张为西 | 887 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/887 | 无 |
| 陈定邦 | 889 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/889 | 无 |
| 戴启麟 | 891 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/891 | 无 |
| 丰岩清 | 893 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/893 | 无 |
| 方莹莹 | 892 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/892 | 无 |
| 黄鑫 | 29218 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/29218 | 无 |
| 梁颖茵 | 32589 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/32589 | 无 |
| 吴超 | 33067 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/33067 | 无 |
| 冼文彪 | 33114 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/33114 | 无 |
| 郑一帆 | 33062 | 唯一身份 | 1 | 神经一科 | https://www.fahsysu.org.cn/node/33062 | 无 |
| 黄海威 | 896 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/896 | 无 |
| 洪华 | 895 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/895 | 无 |
| 刘刚 | 20863 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/20863 | 无 |
| 李玲 | 35738 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/35738 | 无 |
| 盛文利 | 898 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/898 | 无 |
| 陶玉倩 | 899 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/899 | 无 |
| 邢世会 | 877 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/877 | 无 |
| 余剑 | 900 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/900 | 无 |
| 张健 | 878 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/878 | 无 |
| 陈歆然 | 35586 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/35586 | 无 |
| 党超 | 873 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/873 | 无 |
| 林健雯 | 902 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/902 | 无 |
| 李骄星 | 20881 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/20881 | 无 |
| 林少英 | 36940 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/36940 | 无 |
| 欧紫琳 | 29069 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/29069 | 无 |
| 王莹 | 876 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/876 | 无 |
| 曾缨 | 903 | 唯一身份 | 1 | 神经二科（脑血管病专科） | https://www.fahsysu.org.cn/node/903 | 无 |
| 范玉华 | 904 | 唯一身份 | 1 | 神经三科（神经功能专科） | https://www.fahsysu.org.cn/node/904 | 无 |
| 李晶晶 | 901 | 唯一身份 | 1 | 神经三科（神经功能专科） | https://www.fahsysu.org.cn/node/901 | 无 |
| 倪冠中 | 29032 | 唯一身份 | 1 | 神经三科（神经功能专科） | https://www.fahsysu.org.cn/node/29032 | 无 |
| 谭双全 | 26414 | 唯一身份 | 1 | 神经三科（神经功能专科） | https://www.fahsysu.org.cn/node/26414 | 无 |
| 陈玲 | 869 | 唯一身份 | 1 | 神经科ICU | https://www.fahsysu.org.cn/node/869 | 无 |
| 冯慧宇 | 881 | 唯一身份 | 1 | 神经科ICU | https://www.fahsysu.org.cn/node/881 | 无 |
| 冯黎 | 33066 | 唯一身份 | 1 | 神经科ICU | https://www.fahsysu.org.cn/node/33066 | 无 |
| 孙逊沙 | 20882 | 唯一身份 | 1 | 神经科ICU | https://www.fahsysu.org.cn/node/20882 | 无 |
| 王海燕 | 33032 | 唯一身份 | 1 | 神经科ICU | https://www.fahsysu.org.cn/node/33032 | 无 |
| 周鸿雁 | 879 | 唯一身份 | 1 | 神经科ICU | https://www.fahsysu.org.cn/node/879 | 无 |
| 崔立谦 | 906 | 唯一身份 | 1 | 临床心理科（门诊） | https://www.fahsysu.org.cn/node/906 | 无 |
| 陈艺莉 | 910 | 唯一身份 | 1 | 心血管内科 | https://www.fahsysu.org.cn/node/910 | 无 |
| 马虹 | 907 | 唯一身份 | 1 | 心血管内科 | https://www.fahsysu.org.cn/node/907 | 无 |
| 王琴梅 | 909 | 唯一身份 | 1 | 心血管内科 | https://www.fahsysu.org.cn/node/909 | 无 |
| 姚凤娟 | 5595 | 唯一身份 | 2 | 心血管内科、超声医学科 | https://www.fahsysu.org.cn/node/5595 | 无 |
| 黄涌 | 912 | 唯一身份 | 1 | 心血管内科 | https://www.fahsysu.org.cn/node/912 | 无 |
| 罗劲华 | 36851 | 唯一身份 | 1 | 心血管内科 | https://www.fahsysu.org.cn/node/36851 | 无 |
| 郑东诞 | 914 | 唯一身份 | 1 | 心血管内科 | https://www.fahsysu.org.cn/node/914 | 无 |
| 董吁钢 | 915 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/915 | 无 |
| 黄至斌 | 918 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/918 | 无 |
| 罗初凡 | 16991 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/16991 | 无 |
| 廖新学 | 919 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/919 | 无 |
| 唐安丽 | 920 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/920 | 无 |
| 吴杏 | 928 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/928 | 无 |
| 王礼春 | 941 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/941 | 无 |
| 杨达雅 | 23544 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/23544 | 无 |
| 庄晓东 | 929 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/929 | 无 |
| 冯冲 | 36850 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/36850 | 无 |
| 郭玥 | 33149 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/33149 | 无 |
| 黄煜 | 923 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/923 | 无 |
| 江竞舟 | 35915 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/35915 | 无 |
| 卢贵华 | 25427 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/25427 | 无 |
| 冷秀玉 | 924 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/924 | 无 |
| 熊振宇 | 38081 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/38081 | 无 |
| 曾武涛 | 922 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/922 | 无 |
| 赵静静 | 29450 | 唯一身份 | 1 | 心内一科 | https://www.fahsysu.org.cn/node/29450 | 无 |
| 李怡 | 945 | 唯一身份 | 1 | 心内二科（心介科） | https://www.fahsysu.org.cn/node/945 | 无 |
| 龙明 | 946 | 唯一身份 | 1 | 心内二科（心介科） | https://www.fahsysu.org.cn/node/946 | 无 |
| 马跃东 | 925 | 唯一身份 | 1 | 心内二科（心介科） | https://www.fahsysu.org.cn/node/925 | 无 |
| 彭龙云 | 926 | 唯一身份 | 1 | 心内二科（心介科） | https://www.fahsysu.org.cn/node/926 | 无 |
| 胡承恒 | 944 | 唯一身份 | 1 | 心内二科（心介科） | https://www.fahsysu.org.cn/node/944 | 无 |
| 胡洵 | 29234 | 唯一身份 | 1 | 心内二科（心介科） | https://www.fahsysu.org.cn/node/29234 | 无 |
| 刘岗 | 31090 | 唯一身份 | 1 | 心内二科（心介科） | https://www.fahsysu.org.cn/node/31090 | 无 |
| 麦炜颐 | 930 | 唯一身份 | 1 | 心内三科（高血压血管病） | https://www.fahsysu.org.cn/node/930 | 无 |
| 欧志君 | 931 | 唯一身份 | 1 | 心内三科（高血压血管病） | https://www.fahsysu.org.cn/node/931 | 无 |
| 陶军 | 932 | 唯一身份 | 1 | 心内三科（高血压血管病） | https://www.fahsysu.org.cn/node/932 | 无 |
| 夏文豪 | 934 | 唯一身份 | 1 | 心内三科（高血压血管病） | https://www.fahsysu.org.cn/node/934 | 无 |
| 何江 | 38071 | 唯一身份 | 1 | 心内三科（高血压血管病） | https://www.fahsysu.org.cn/node/38071 | 无 |
| 苏晨 | 927 | 唯一身份 | 1 | 心内三科（高血压血管病） | https://www.fahsysu.org.cn/node/927 | 无 |
| 徐诗岳 | 31145 | 唯一身份 | 1 | 心内三科（高血压血管病） | https://www.fahsysu.org.cn/node/31145 | 无 |
| 张小宇 | 29083 | 唯一身份 | 1 | 心内三科（高血压血管病） | https://www.fahsysu.org.cn/node/29083 | 无 |
| 张焰 | 13569 | 唯一身份 | 1 | 心内五科（心血管康复科） | https://www.fahsysu.org.cn/node/13569 | 无 |
| 何建桂 | 939 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/939 | 无 |
| 柳俊 | 940 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/940 | 无 |
| 刘晨 | 32844 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/32844 | 无 |
| 吴德熙 | 30375 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/30375 | 无 |
| 吴素华 | 942 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/942 | 无 |
| 董玢 | 38129 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/38129 | 无 |
| 黄沛森 | 38087 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/38087 | 无 |
| 纪程程 | 38473 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/38473 | 无 |
| 魏方菲 | 35628 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/35628 | 无 |
| 吴泽璇 | 35080 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/35080 | 无 |
| 薛睿聪 | 28386 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/28386 | 无 |
| 朱文根 | 38540 | 唯一身份 | 1 | 心内六科（CCU） | https://www.fahsysu.org.cn/node/38540 | 无 |
| 李淑娟 | 25429 | 唯一身份 | 1 | 心血管儿科 | https://www.fahsysu.org.cn/node/25429 | 无 |
| 覃有振 | 935 | 唯一身份 | 1 | 心血管儿科 | https://www.fahsysu.org.cn/node/935 | 无 |
| 王慧深 | 936 | 唯一身份 | 1 | 心血管儿科 | https://www.fahsysu.org.cn/node/936 | 无 |
| 巴宏军 | 39252 | 唯一身份 | 1 | 心血管儿科 | https://www.fahsysu.org.cn/node/39252 | 无 |
| 朱玲 | 938 | 唯一身份 | 1 | 心血管儿科 | https://www.fahsysu.org.cn/node/938 | 无 |
| 陈光献 | 947 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/947 | 无 |
| 梁孟亚 | 5537 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/5537 | 无 |
| 区景松 | 23546 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/23546 | 无 |
| 吴钟凯 | 949 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/949 | 无 |
| 徐颖琦 | 950 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/950 | 无 |
| 殷胜利 | 952 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/952 | 无 |
| 姚尖平 | 951 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/951 | 无 |
| 张希 | 953 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/953 | 无 |
| 熊迈 | 5538 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/5538 | 无 |
| 许哲 | 25512 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/25512 | 无 |
| 周立 | 23547 | 唯一身份 | 1 | 心脏外科 | https://www.fahsysu.org.cn/node/23547 | 无 |
| 荣健 | 943 | 唯一身份 | 1 | 体外循环科 | https://www.fahsysu.org.cn/node/943 | 无 |
| 黄勇 | 31409 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/31409 | 无 |
| 荆小莉 | 5756 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/5756 | 无 |
| 刘江辉 | 20880 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/20880 | 无 |
| 刘志豪 | 31405 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/31405 | 无 |
| 魏红艳 | 31406 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/31406 | 无 |
| 王科科 | 31410 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/31410 | 无 |
| 徐嘉 | 31442 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/31442 | 无 |
| 杨震 | 933 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/933 | 无 |
| 詹红 | 5761 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/5761 | 无 |
| 黄应雄 | 35584 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/35584 | 无 |
| 廖瑾莉 | 31441 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/31441 | 无 |
| 梁艳冰 | 5762 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/5762 | 无 |
| 叶子 | 31407 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/31407 | 无 |
| 郑梓煜 | 31408 | 唯一身份 | 1 | 急诊科 | https://www.fahsysu.org.cn/node/31408 | 无 |
| 包勇 | 5830 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/5830 | 无 |
| 陈勇 | 5837 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/5837 | 无 |
| 彭振维 | 5833 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/5833 | 无 |
| 任玉峰 | 5834 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/5834 | 无 |
| 王岩 | 5836 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/5836 | 无 |
| 毕月 | 38145 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/38145 | 无 |
| 陈瑞莞 | 5831 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/5831 | 无 |
| 何潇芳 | 38113 | 同名待甄别 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/38113 | 同名不同数字 ID 分行保留 |
| 牛绍清 | 33085 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/33085 | 无 |
| 彭芳 | 5832 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/5832 | 无 |
| 沈国平 | 5835 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/5835 | 无 |
| 王成涛 | 31088 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/31088 | 无 |
| 韦广滟 | 38114 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/38114 | 无 |
| 吴双 | 35695 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/35695 | 无 |
| 王雪涔 | 38116 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/38116 | 无 |
| 张群 | 29320 | 唯一身份 | 1 | 放射治疗科 | https://www.fahsysu.org.cn/node/29320 | 无 |
| 龙健婷 | 5828 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/5828 | 无 |
| 许丽霞 | 25473 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/25473 | 无 |
| 张家兴 | 5829 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/5829 | 无 |
| 陈翠 | 31146 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/31146 | 无 |
| 陈凯 | 35592 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/35592 | 无 |
| 戴强生 | 5827 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/5827 | 无 |
| 花蕊熙 | 25605 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/25605 | 无 |
| 何潇芳 | 38613 | 同名待甄别 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/38613 | 同名不同数字 ID 分行保留 |
| 汪芳 | 38108 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/38108 | 无 |
| 叶文 | 31147 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/31147 | 无 |
| 张梦萍 | 28258 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/28258 | 无 |
| 郑胄三 | 35705 | 唯一身份 | 1 | 肿瘤科 | https://www.fahsysu.org.cn/node/35705 | 无 |
| 成艳美 | 34804 | 唯一身份 | 1 | 心胸外科ICU | https://www.fahsysu.org.cn/node/34804 | 无 |
| 王翠苹 | 33314 | 唯一身份 | 1 | 心胸外科ICU | https://www.fahsysu.org.cn/node/33314 | 无 |
| 杨嵩 | 33035 | 唯一身份 | 1 | 心胸外科ICU | https://www.fahsysu.org.cn/node/33035 | 无 |
| 陈泽雄 | 5715 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5715 | 无 |
| 金明华 | 5724 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5724 | 无 |
| 李琼 | 5716 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5716 | 无 |
| 伍新林 | 5719 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5719 | 无 |
| 张诗军 | 5720 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5720 | 无 |
| 陈树清 | 20875 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/20875 | 无 |
| 邓伟 | 20876 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/20876 | 无 |
| 黄春莲 | 5722 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5722 | 无 |
| 黄颖娟 | 5723 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5723 | 无 |
| 林佑武 | 5726 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5726 | 无 |
| 刘嘉辉 | 29052 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/29052 | 无 |
| 孟君 | 5727 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5727 | 无 |
| 孙保国 | 5728 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5728 | 无 |
| 谭畅 | 5729 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5729 | 无 |
| 韦志辉 | 5730 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/5730 | 无 |
| 吴国珍 | 20864 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/20864 | 无 |
| 汪园园 | 38070 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/38070 | 无 |
| 周厚明 | 25423 | 唯一身份 | 1 | 中医科 | https://www.fahsysu.org.cn/node/25423 | 无 |
| 陈木开 | 5735 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/5735 | 无 |
| 韩建德 | 5736 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/5736 | 无 |
| 罗迪青 | 5737 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/5737 | 无 |
| 陈小红 | 5741 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/5741 | 无 |
| 廖绮曼 | 5744 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/5744 | 无 |
| 刘隽华 | 28714 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/28714 | 无 |
| 马春光 | 29212 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/29212 | 无 |
| 唐旭华 | 31141 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/31141 | 无 |
| 叶艳婷 | 33309 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/33309 | 无 |
| 周晖 | 5747 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/5747 | 无 |
| 赵玉昆 | 34932 | 唯一身份 | 1 | 皮肤科 | https://www.fahsysu.org.cn/node/34932 | 无 |
| 陈曦 | 5796 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/5796 | 无 |
| 陈少贞 | 30753 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/30753 | 无 |
| 刘汉军 | 5800 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/5800 | 无 |
| 刘鹏 | 5801 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/5801 | 无 |
| 王楚怀 | 5802 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/5802 | 无 |
| 赵江莉 | 38214 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/38214 | 无 |
| 丁明晖 | 5803 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/5803 | 无 |
| 韩秀兰 | 36160 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/36160 | 无 |
| 江沁 | 33228 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/33228 | 无 |
| 梁崎 | 34219 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/34219 | 无 |
| 李咏雪 | 33461 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/33461 | 无 |
| 冷雁 | 31102 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/31102 | 无 |
| 吴秀勤 | 33224 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/33224 | 无 |
| 张桂芳 | 36204 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/36204 | 无 |
| 张珊珊 | 35683 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/35683 | 无 |
| 张思韵 | 38126 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/38126 | 无 |
| 张洲 | 33153 | 唯一身份 | 1 | 康复医学科 | https://www.fahsysu.org.cn/node/33153 | 无 |
| 初建平 | 5554 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5554 | 无 |
| 冯仕庭 | 5562 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5562 | 无 |
| 范淼 | 5561 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5561 | 无 |
| 关键 | 31701 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/31701 | 无 |
| 郭燕 | 5563 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5563 | 无 |
| 李向民 | 5564 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5564 | 无 |
| 罗宴吉 | 31699 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/31699 | 无 |
| 孟悛非 | 31687 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/31687 | 无 |
| 彭振鹏 | 31702 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/31702 | 无 |
| 沈冰奇 | 5558 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5558 | 无 |
| 孙灿辉 | 5567 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5567 | 无 |
| 王焕军 | 31691 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/31691 | 无 |
| 余深平 | 5570 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5570 | 无 |
| 杨有优 | 5568 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5568 | 无 |
| 杨智云 | 5569 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5569 | 无 |
| 郑可国 | 5571 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5571 | 无 |
| 张小玲 | 31694 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/31694 | 无 |
| 张朝晖 | 5559 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5559 | 无 |
| 邝健谊 | 5556 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5556 | 无 |
| 江利 | 5555 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/5555 | 无 |
| 李雪华 | 31686 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/31686 | 无 |
| 王霁朏 | 38312 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/38312 | 无 |
| 赵静 | 31688 | 唯一身份 | 1 | 放射诊断专科 | https://www.fahsysu.org.cn/node/31688 | 无 |
| 黄勇慧 | 5573 | 唯一身份 | 1 | 放射介入专科 | https://www.fahsysu.org.cn/node/5573 | 无 |
| 向贤宏 | 5578 | 唯一身份 | 1 | 放射介入专科 | https://www.fahsysu.org.cn/node/5578 | 无 |
| 杨建勇 | 5574 | 唯一身份 | 1 | 放射介入专科 | https://www.fahsysu.org.cn/node/5574 | 无 |
| 庄文权 | 5575 | 唯一身份 | 1 | 放射介入专科 | https://www.fahsysu.org.cn/node/5575 | 无 |
| 郭文波 | 5576 | 唯一身份 | 1 | 放射介入专科 | https://www.fahsysu.org.cn/node/5576 | 无 |
| 林润 | 25408 | 唯一身份 | 1 | 放射介入专科 | https://www.fahsysu.org.cn/node/25408 | 无 |
| 谭国胜 | 5577 | 唯一身份 | 1 | 放射介入专科 | https://www.fahsysu.org.cn/node/5577 | 无 |
| 范文哲 | 5580 | 唯一身份 | 1 | 肿瘤介入科 | https://www.fahsysu.org.cn/node/5580 | 无 |
| 王于 | 5581 | 唯一身份 | 1 | 肿瘤介入科 | https://www.fahsysu.org.cn/node/5581 | 无 |
| 吴艳琴 | 35812 | 唯一身份 | 1 | 肿瘤介入科 | https://www.fahsysu.org.cn/node/35812 | 无 |
| 姚望 | 33148 | 唯一身份 | 1 | 肿瘤介入科 | https://www.fahsysu.org.cn/node/33148 | 无 |
| 赵月 | 35648 | 唯一身份 | 1 | 肿瘤介入科 | https://www.fahsysu.org.cn/node/35648 | 无 |
| 王晓燕 | 30518 | 唯一身份 | 1 | 核医学科 | https://www.fahsysu.org.cn/node/30518 | 无 |
| 张祥松 | 5548 | 唯一身份 | 1 | 核医学科 | https://www.fahsysu.org.cn/node/5548 | 无 |
| 陈丹云 | 5549 | 唯一身份 | 1 | 核医学科 | https://www.fahsysu.org.cn/node/5549 | 无 |
| 陈维安 | 5550 | 唯一身份 | 1 | 核医学科 | https://www.fahsysu.org.cn/node/5550 | 无 |
| 岳殿超 | 5553 | 唯一身份 | 1 | 核医学科 | https://www.fahsysu.org.cn/node/5553 | 无 |
| 陈立达 | 25889 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/25889 | 无 |
| 陈淑玲 | 32032 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/32032 | 无 |
| 匡铭 | 5582 | 同名待甄别 | 2 | 超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/5582 | 同名不同数字 ID 分行保留 |
| 刘东红 | 5583 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/5583 | 无 |
| 梁瑾瑜 | 5589 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/5589 | 无 |
| 王竹 | 5593 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/5593 | 无 |
| 王伟 | 5592 | 同名待甄别 | 2 | 超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/5592 | 同名不同数字 ID 分行保留 |
| 谢红宁 | 5585 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/5585 | 无 |
| 徐明 | 20891 | 唯一身份 | 2 | 超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/20891 | 无 |
| 谢晓华 | 5594 | 唯一身份 | 2 | 超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/5594 | 无 |
| 谢晓燕 | 5586 | 唯一身份 | 2 | 超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/5586 | 无 |
| 郑艳玲 | 5596 | 唯一身份 | 2 | 超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/5596 | 无 |
| 程美清 | 38734 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/38734 | 无 |
| 陈瑜君 | 31956 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/31956 | 无 |
| 段妤 | 38208 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/38208 | 无 |
| 黄光亮 | 5587 | 唯一身份 | 2 | 超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/5587 | 无 |
| 胡航通 | 38806 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/38806 | 无 |
| 刘保娴 | 32232 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/32232 | 无 |
| 刘丽 | 5591 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/5591 | 无 |
| 雷婷 | 33214 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/33214 | 无 |
| 李薇 | 29084 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/29084 | 无 |
| 李晓菊 | 38176 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/38176 | 无 |
| 阮思敏 | 38936 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/38936 | 无 |
| 佟文娟 | 38757 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/38757 | 无 |
| 谭洋 | 38152 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/38152 | 无 |
| 庄博文 | 29158 | 唯一身份 | 2 | 超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/29158 | 无 |
| 郑巧 | 36784 | 唯一身份 | 1 | 超声医学科 | https://www.fahsysu.org.cn/node/36784 | 无 |
| 张晓儿 | 33352 | 唯一身份 | 2 | 超声医学科、介入超声专科 | https://www.fahsysu.org.cn/node/33352 | 无 |
| 林满霞 | 20890 | 唯一身份 | 1 | 介入超声专科 | https://www.fahsysu.org.cn/node/20890 | 无 |
| 黄通毅 | 38693 | 唯一身份 | 1 | 介入超声专科 | https://www.fahsysu.org.cn/node/38693 | 无 |
| 刘敏 | 25838 | 同名待甄别 | 1 | 医学检验科 | https://www.fahsysu.org.cn/node/25838 | 同名不同数字 ID 分行保留 |
| 欧阳涓 | 25887 | 唯一身份 | 1 | 医学检验科 | https://www.fahsysu.org.cn/node/25887 | 无 |
| 陈培松 | 5840 | 唯一身份 | 1 | 医学检验科 | https://www.fahsysu.org.cn/node/5840 | 无 |
| 陈文芳 | 5804 | 唯一身份 | 1 | 病理科 | https://www.fahsysu.org.cn/node/5804 | 无 |
| 韩安家 | 5805 | 唯一身份 | 1 | 病理科 | https://www.fahsysu.org.cn/node/5805 | 无 |
| 彭挺生 | 5808 | 唯一身份 | 1 | 病理科 | https://www.fahsysu.org.cn/node/5808 | 无 |
| 王芬 | 5816 | 唯一身份 | 1 | 病理科 | https://www.fahsysu.org.cn/node/5816 | 无 |
| 王连唐 | 5809 | 唯一身份 | 1 | 病理科 | https://www.fahsysu.org.cn/node/5809 | 无 |
| 余俐 | 5812 | 唯一身份 | 1 | 病理科 | https://www.fahsysu.org.cn/node/5812 | 无 |
| 刘大伟 | 30447 | 唯一身份 | 1 | 病理科 | https://www.fahsysu.org.cn/node/30447 | 无 |
| 邸宇琴 | 38127 | 唯一身份 | 1 | 分子诊断与基因检测中心 | https://www.fahsysu.org.cn/node/38127 | 无 |
| 陈杰 | 30465 | 唯一身份 | 1 | 药学部 | https://www.fahsysu.org.cn/node/30465 | 无 |
| 陈攀 | 30466 | 唯一身份 | 1 | 药学部 | https://www.fahsysu.org.cn/node/30466 | 无 |
| 黎曙霞 | 5817 | 唯一身份 | 1 | 药学部 | https://www.fahsysu.org.cn/node/5817 | 无 |
| 唐欲博 | 30467 | 唯一身份 | 1 | 药学部 | https://www.fahsysu.org.cn/node/30467 | 无 |
| 夏延哲 | 33213 | 唯一身份 | 1 | 药学部 | https://www.fahsysu.org.cn/node/33213 | 无 |
| 曾嘉炜 | 30468 | 唯一身份 | 1 | 药学部 | https://www.fahsysu.org.cn/node/30468 | 无 |
| 赵丽岩 | 30469 | 唯一身份 | 1 | 药学部 | https://www.fahsysu.org.cn/node/30469 | 无 |
| 隋昳 | 29817 | 唯一身份 | 1 | 临床营养科 | https://www.fahsysu.org.cn/node/29817 | 无 |
| 王妍 | 23548 | 唯一身份 | 1 | 健康管理中心 | https://www.fahsysu.org.cn/node/23548 | 无 |
| 张亚东 | 25337 | 唯一身份 | 1 | 健康管理中心 | https://www.fahsysu.org.cn/node/25337 | 无 |
| 何文 | 5540 | 唯一身份 | 1 | 特需一科（老年病科） | https://www.fahsysu.org.cn/node/5540 | 无 |
| 元刚 | 5541 | 唯一身份 | 1 | 特需一科（老年病科） | https://www.fahsysu.org.cn/node/5541 | 无 |
| 劳敏曦 | 25416 | 唯一身份 | 1 | 特需一科（老年病科） | https://www.fahsysu.org.cn/node/25416 | 无 |
| 邵奕嘉 | 35681 | 唯一身份 | 1 | 特需一科（老年病科） | https://www.fahsysu.org.cn/node/35681 | 无 |
| 吴芳 | 32703 | 唯一身份 | 1 | 特需一科（老年病科） | https://www.fahsysu.org.cn/node/32703 | 无 |
| 张玲 | 29299 | 唯一身份 | 1 | 特需一科（老年病科） | https://www.fahsysu.org.cn/node/29299 | 无 |
| 丁美琳 | 36759 | 唯一身份 | 1 | 特需二科 | https://www.fahsysu.org.cn/node/36759 | 无 |
| 李进 | 29070 | 唯一身份 | 1 | 特需二科 | https://www.fahsysu.org.cn/node/29070 | 无 |
| 苏磊 | 25837 | 唯一身份 | 1 | 特需二科 | https://www.fahsysu.org.cn/node/25837 | 无 |
| 陈锡林 | 657 | 唯一身份 | 1 | 特需三科 | https://www.fahsysu.org.cn/node/657 | 无 |
| 黄展鹏 | 29542 | 唯一身份 | 1 | 转化医学研究中心 | https://www.fahsysu.org.cn/node/29542 | 无 |
| 纪卫东 | 5820 | 唯一身份 | 1 | 转化医学研究中心 | https://www.fahsysu.org.cn/node/5820 | 无 |
| 林水宾 | 5821 | 唯一身份 | 1 | 转化医学研究中心 | https://www.fahsysu.org.cn/node/5821 | 无 |
| 徐彩霞 | 5824 | 唯一身份 | 1 | 转化医学研究中心 | https://www.fahsysu.org.cn/node/5824 | 无 |
| 杨蜀岚 | 5823 | 唯一身份 | 1 | 转化医学研究中心 | https://www.fahsysu.org.cn/node/5823 | 无 |
| 邵兰 | 5822 | 唯一身份 | 1 | 转化医学研究中心 | https://www.fahsysu.org.cn/node/5822 | 无 |
| 王子洋 | 38111 | 唯一身份 | 1 | 转化医学研究中心 | https://www.fahsysu.org.cn/node/38111 | 无 |
| 张灿峰 | 38122 | 唯一身份 | 1 | 转化医学研究中心 | https://www.fahsysu.org.cn/node/38122 | 无 |


## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| 无 | 无 | 无 | 无 |

## 输出文件

- Excel 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx`
- CSV 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 90 |
| 原始医生卡片记录 | 881 |
| 跨入口去重前候选关系 | 881 |
| 跨入口去重后唯一候选 | 860 |
| 排除非医生候选 | 0 |
| 合规医生详情页 | 860 |
| 最终医生身份 | 860 |
| 覆盖科室数 | 90 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 245 |
| 慢性病 | 294 |
| 术后恢复/康复 | 275 |
| 生殖疾病 | 103 |
| 疑难重症 | 393 |
| 肿瘤 | 460 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 泌尿外科 | 32 |
| 超声医学科 | 30 |
| 神经外科 | 26 |
| 妇科 | 26 |
| 放射诊断专科 | 23 |
| 肾内科 | 22 |
| 器官移植科 | 20 |
| 内分泌内科 | 20 |
| 消化内科 | 19 |
| 产科 | 18 |
| 麻醉科 | 18 |
| 呼吸与危重症医学科 | 18 |
| 心内一科 | 18 |
| 中医科 | 18 |
| 生殖医学中心 | 17 |
| 脊柱外科 | 17 |
| 神经二科（脑血管病专科） | 17 |
| 康复医学科 | 17 |
| 关节外科 | 16 |
| 神经一科 | 16 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 同名待甄别 | 16 |
| 非医生页面或姓名异常 | 1 |
| 详情正文为空或未识别 | 7 |
| 职称/身份需人工复核 | 9 |

## 列表页读取异常

| 页码 | URL | 错误 |
|---|---|---|
| 无 | 无 | 无 |

## 详情页读取异常

| 来源链接 | 错误 |
|---|---|
| 无 | 无 |

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
