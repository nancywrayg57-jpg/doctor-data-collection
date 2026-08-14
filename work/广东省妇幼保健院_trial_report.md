---
类型: 自动采集试跑报告
医院: 广东省妇幼保健院
城市: 广州市
采集日期: 2026-08-14
来源范围: 医院官网
采集入口: https://www.e3861.com/keshizhuanjia/zhuanjiajieshao
适配器: gdmch_paginated_expert_photo
---

# 广东省妇幼保健院 官方医生自动采集试跑报告

## 结论

本次试采只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集试采底表，共 10 位唯一医生；官网列表页原始卡片记录 884 条；读取入口分类 111 个；覆盖 14 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 广东省妇幼保健院 |
| 官网首页 | https://www.e3861.com/ |
| 本轮医生入口 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao |
| 入口来源 | GitHub Issue #43（与官网入口台账序号 21 一致） |
| 原台账医生入口 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | D-待人工补官网 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
|  | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao | 官网服务端专家目录分页；卡片含姓名、职称和官方子域职业照 | 111 | 884 | 884 | 49 | 广东省妇幼保健院 | 四院区共用官网专家目录和统一页脚；未发现独立法人标识 |

### 动态目录专项证据

- 医生分页/载入方式：111 个服务端公开 GET 分页；仅空白 searchDoctor/searchDepartment，不构造检索词
- 医生目录公开接口：不适用
- 医生详情公开接口：不适用
- 接口出处证据：不适用
- 院区/分组：0 个；科室分类：0 个
- 医生-科室关系：884 条
- 唯一详情 ID：884 个
- 有姓名详情 ID：10 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：10 个
- 同名不同详情 ID：4 组
- 非空/空科室块：0 / 0
- 院区/出诊点标签关系：番禺院区 8 条；越秀院区 3 条；天河院区 2 条；清远院区 2 条
- 跨院区/出诊点详情 ID：0 个

| 同名 | 详情 ID |
|---|---|
| 郭庆禄 | 34640,34931 |
| 周真 | 32647,32821 |
| 刘颖 | 32499,33007 |
| 何裕 | 32750,33134 |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：884
- 跨入口去重后唯一候选：884
- 跨入口重复关系：0
- 试采覆盖入口分类：14 个（中医科、乳腺科、儿科、内科、妇科、小儿便秘外科、小儿外科、小儿普外科、小儿疝微创、小儿肿瘤外科、小儿骨科、小儿黄疸外科、新生儿科、普通儿科）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 无 | 无 | 无 |

## 广东省妇幼保健院目录、四院区与照片 TRIAL 对账

- 官网服务端分页：111 页；原始卡片 / 唯一数字详情 ID：884 / 884。
- 重复关系：0；号源/系统账号/非医生排除：49；排除后合规候选：835。
- 科室结构：目录只提供自由文本检索框，无服务端科室分类树；样本科室仅从详情出诊安排括号标签保守提取，日期时段不入库。
- 试采覆盖科室：14 个（中医科、乳腺科、儿科、内科、妇科、小儿便秘外科、小儿外科、小儿普外科、小儿疝微创、小儿肿瘤外科、小儿骨科、小儿黄疸外科、新生儿科、普通儿科）；详情失败：0。
- 四院区官网归属证据：4 条；独立实体信号：0。
- 详情清洗：排班片段排除 12，排名/患者片段排除 0，患者案例排除 0；正式字段排班写入 0、私用区字符 0。
- 照片四数：应采 10 / 实采 10 / 失败 0 / 无照片 0。
- 本人职业照可得 / 官网默认占位图：658 / 177（全目录默认占位图 225）。
- 平均照片大小：53509 bytes；按 658 位有本人职业照候选估算全院照片容量：35208922 bytes。
- 大图阈值：`单张 >200KB 或宽 >800px`；命中 0 张；照片政策状态：`OWNER_APPROVED_ORIGINAL_NO_WIDTH_LIMIT`。原图不压缩；命中阈值时必须等待 owner 裁决本院 FULL 策略。
- 普通公开会话：requests 常规公开 GET；无登录、Cookie 注入、验证码/挑战求解或非公开接口。

### 四院区官方归属证据

| 院区 | 官方链接 | 归属结论 |
|---|---|---|
| 番禺院区 | https://www.e3861.com/keshizhuanjia/panyuyuanqu | 官网同一专家目录与统一页脚列示的广东省妇幼保健院院区；未发现独立法人标识 |
| 越秀院区 | https://www.e3861.com/keshizhuanjia/yuexiuyuanqu | 官网同一专家目录与统一页脚列示的广东省妇幼保健院院区；未发现独立法人标识 |
| 天河院区 | https://www.e3861.com/keshizhuanjia/tianheyuanqu | 官网同一专家目录与统一页脚列示的广东省妇幼保健院院区；未发现独立法人标识 |
| 清远院区 | https://www.e3861.com/keshizhuanjia/qingyuanyuanqu | 官网同一专家目录与统一页脚列示的广东省妇幼保健院院区；未发现独立法人标识 |

### 10 位样本逐 ID 对账

| 详情 ID | 姓名 | 科室 | 院区 | 详情状态 | 来源链接 |
|---|---|---|---|---|---|
| 32441 | 李文萍 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32441.html |
| 32507 | 范保维 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32507.html |
| 32514 | 和秀魁 | 妇科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32514.html |
| 32686 | 陈炳豪 | 小儿骨科、小儿外科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32686.html |
| 32478 | 胡春玲 | 内科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32478.html |
| 32439 | 陈凤媚 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32439.html |
| 32614 | 伍苑宾 | 普通儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32614.html |
| 32448 | 柴成伟 | 小儿普外科、小儿肿瘤外科、小儿黄疸外科、小儿便秘外科、小儿疝微创 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32448.html |
| 32749 | 王春艳 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32749.html |
| 34810 | 杨洋 | 儿科、新生儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34810.html |

### 49 个非医生候选逐 ID 排除表

| 详情 ID | 名称 | 列表身份 | 来源链接 | 排除理由 |
|---|---|---|---|---|
| 33000 | 乳腺专科门诊 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33000.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35596 | 产前诊断手术号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35596.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35597 | 免费产前筛查发券号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35597.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35071 | 名医工作室 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35071.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33153 | Z双胎多胎门诊 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33153.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35166 | 杨东新主任团队号 | 副主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35166.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32779 | 管理员 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32779.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35076 | 双胎多胎门诊 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35076.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35599 | 日间门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35599.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35598 | 宫腔镜专用号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35598.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35603 | 免费产前筛查及诊断号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35603.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32780 | 续费专用号 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32780.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35594 | 妇科手术号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35594.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32999 | P双胎多胎门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32999.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32938 | 盆底筛查咨询 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32938.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35088 | 罕见病会诊号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35088.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35089 | test123 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35089.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35091 | 中医治疗号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35091.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35093 | 手术咨询号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35093.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35094 | 妇科计生门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35094.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35095 | 盘底筛查治疗 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35095.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32566 | 系统管理员-正式库 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32566.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35096 | 儿科义诊医生 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35096.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32576 | 脱敏注射号 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32576.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32914 | 急诊号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32914.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35686 | 产前诊断专科医生 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35686.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35604 | 治疗号(开单专用) | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35604.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 34770 | 多科会诊号 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34770.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33001 | 助孕贴专用号 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33001.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35090 | 口腔保健号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35090.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32455 | 尹爱华名医工作室 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32455.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35050 | 鼻炎专科号 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35050.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 34732 | 中医针灸美容及减重专科号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34732.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35055 | 内分泌及肥胖中西医结合号 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35055.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35601 | 日间手术评估及术后随访 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35601.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35066 | 卵巢功能减退门诊 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35066.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32971 | 发热门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32971.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33286 | 生育力保存免费咨询医生 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33286.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33326 | 盆底磁治疗预约 | 医士 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33326.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 34678 | 续费医生 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34678.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35600 | 宫腔镜手术号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35600.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35602 | 日间手术门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35602.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35730 | 口腔科急诊号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35730.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32897 | F双胎多胎门诊 | 副主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32897.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33269 | 早孕专科号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33269.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35476 | 早孕门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35476.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33271 | 专科医生 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33271.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35109 | 中医简易门诊 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35109.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35110 | 政府免费筛查就诊号 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35110.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |

### TRIAL 照片命名、字节、魔数、SHA-256 与尺寸对照

| 姓名 | 科室 | 主职称 | 文件名 | 字节数 | 宽×高 | SHA-256 | 官网照片 |
|---|---|---|---|---:|---:|---|---|
| 李文萍 | 乳腺科 | 主任医师 | 李文萍-乳腺科-主任医师-广东省妇幼保健院.png | 76443 | 185×280 | `e3b0a1cc72ba61876a749f92607177a68579a72a95b997cb93fb94f0ebbc3d1d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f5b379df-5903-4c8d-80fa-d80866a7e850-280.png |
| 范保维 | 妇科 | 主任医师 | 范保维-妇科-主任医师-广东省妇幼保健院.png | 84458 | 208×280 | `889bfdbc2dc580709367df824c0b74ba7cbe32e14447ac7ddef6d94847192dde` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5663f017-754e-46b2-9c4a-6fea6fba319e-280.png |
| 和秀魁 | 妇科 | 主任医师 | 和秀魁-妇科-主任医师-广东省妇幼保健院.png | 126269 | 232×280 | `1736b885aa1c0dbb0b19ffa60b19903eaabd2ecbf4b0aa3f39cbedd3be329b34` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ea66d3c1-7739-4cd0-b7a0-43a69107d0c7-280.png |
| 陈炳豪 | 小儿骨科 | 主治医师 | 陈炳豪-小儿骨科-主治医师-广东省妇幼保健院.jpg | 7217 | 210×280 | `257593f07b5d3b24ac8b2b429373c7204eab89f3ceed93339c701adbf1f4e511` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0532d852-4598-4f3a-86b3-802e7105f779-280.jpg |
| 胡春玲 | 内科 | 主任医师 | 胡春玲-内科-主任医师-广东省妇幼保健院.png | 73201 | 186×280 | `ed35d5d847ad63690204c2f6af7fd9da60969df1fccabdd4cbf59ddd37476faf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ccc2d01a-15f4-42fa-8cd1-71488a420ede-280.jpg |
| 陈凤媚 | 中医科 | 主任中医师 | 陈凤媚-中医科-主任中医师-广东省妇幼保健院.png | 82927 | 205×280 | `d9a745035de2d9f2dcf68d384d9b8b498bf32e967e1b574657918b2c938920f5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1d81e6e0-56ec-4693-aa26-500baa678d64-280.png |
| 伍苑宾 | 普通儿科 | 主治医师 | 伍苑宾-普通儿科-主治医师-广东省妇幼保健院.jpg | 6238 | 187×280 | `02970b1d99b80cf3f27dabe7d1f97a3516bc2f8569b05bec78a8bc4efdb10053` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fbaac087-66ae-461f-b8ad-3a7bd9e0ce93-280.jpg |
| 柴成伟 | 小儿普外科 | 主任医师 | 柴成伟-小儿普外科-主任医师-广东省妇幼保健院.jpg | 7469 | 199×280 | `388651332639ed3602266ffc551ff220448eb8769af298e6a36610e8b22a2497` | https://wx.e3861.com/sfyAdmin/Images/Doctor/dc00ee52-b31e-4684-a692-354b7301af10-280.jpg |
| 王春艳 | 妇科 | 主治医师 | 王春艳-妇科-主治医师-广东省妇幼保健院.jpg | 5953 | 158×280 | `4e949581395b4a226160d2a9ea2296b4899befc2ac96f432d66bdfb508e356c8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d4ea40ab-c37a-4f68-a65e-82db43c3e49d-280.jpg |
| 杨洋 | 儿科 | 主治医师 | 杨洋-儿科-主治医师-广东省妇幼保健院.png | 64918 | 181×280 | `304ff8a3383604a620b94f76cf30c4e57144d088ec6ba67c576f77ba34ed8cb4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e60eb84d-ddb2-4e6d-a85a-c514b7265049-280.png |


## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=2 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33000.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=4 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35596.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=4 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35597.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=5 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35071.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=5 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33153.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=12 | 副主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35166.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=13 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32779.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=27 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35076.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=34 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35599.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=36 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35598.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=41 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35603.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=49 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32780.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=56 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35594.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=57 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32999.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=57 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32938.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=57 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35088.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=61 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35089.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=68 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35091.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=73 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35093.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=74 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35094.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=74 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35095.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=74 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32566.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=74 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35096.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=77 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32576.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=78 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32914.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=79 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35686.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=80 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35604.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=81 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34770.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=82 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33001.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=82 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35090.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=86 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32455.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=89 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35050.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=89 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34732.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=90 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35055.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=90 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35601.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=93 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35066.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=95 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32971.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=95 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33286.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=95 | 医士 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33326.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=96 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34678.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=96 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35600.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=97 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35602.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=106 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35730.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=109 | 副主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32897.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=109 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33269.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=110 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35476.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=110 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33271.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=110 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35109.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=111 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35110.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |

## 输出文件

- Excel 底表：未生成（本轮使用 --no-xlsx）
- CSV 底表：`D:\workspace\信息收集整理\work\广东省妇幼保健院_trial_doctors.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 111 |
| 原始医生卡片记录 | 884 |
| 跨入口去重前候选关系 | 884 |
| 跨入口去重后唯一候选 | 884 |
| 排除非医生候选 | 49 |
| 合规医生详情页 | 835 |
| 最终医生身份 | 10 |
| 覆盖科室数 | 14 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 4 |
| 慢性病 | 2 |
| 术后恢复/康复 | 2 |
| 生殖疾病 | 4 |
| 疑难重症 | 1 |
| 肿瘤 | 4 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 妇科 | 3 |
| 乳腺科 | 1 |
| 小儿骨科 | 1 |
| 小儿外科 | 1 |
| 内科 | 1 |
| 中医科 | 1 |
| 普通儿科 | 1 |
| 小儿普外科 | 1 |
| 小儿肿瘤外科 | 1 |
| 小儿黄疸外科 | 1 |
| 小儿便秘外科 | 1 |
| 小儿疝微创 | 1 |
| 儿科 | 1 |
| 新生儿科 | 1 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 详情正文为空或未识别 | 2 |

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
