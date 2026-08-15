---
类型: 全量采集归并审计报告
医院: 广东药科大学附属第一医院
城市: 广州市
采集日期: 2026-08-15
来源范围: 医院官网
采集入口: https://www.gy120.net/zhuanjia.asp
适配器: gy120_asp_department_expert_photo
---

# 广东药科大学附属第一医院 官方医生全量采集归并审计报告

## 结论

本次全量采集只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集全量采集底表，共 340 位唯一医生；官网列表页原始卡片记录 407 条；读取入口分类 4 个；覆盖 115 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 广东药科大学附属第一医院 |
| 官网首页 | https://www.gy120.net/ |
| 本轮医生入口 | https://www.gy120.net/zhuanjia.asp |
| 入口来源 | GitHub Issue #47（与官网入口台账序号 24 一致） |
| 原台账医生入口 | https://www.gy120.net/zhuanjia.asp |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | D-待人工补官网 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
| 首席专家/科室负责人+科室专家树 | https://www.gy120.net/zhuanjia.asp | 官网旧版 ASP 单页静态专家目录 | 1 | 407 | 349 | 2 | 广东药科大学附属第一医院 | 农林门诊、共和门诊、健康管理中心均由同一官网详情出诊标签与医院页脚地址证明；未发现独立法人入口 |

### 动态目录专项证据

- 医生分页/载入方式：同一旧版 ASP 静态 HTML；不构造分页、关键词或搜索请求
- 医生目录公开接口：不适用
- 医生详情公开接口：不适用
- 接口出处证据：不适用
- 院区/分组：0 个；科室分类：57 个
- 医生-科室关系：349 条
- 唯一详情 ID：349 个
- 有姓名详情 ID：340 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：340 个
- 同名不同详情 ID：8 组
- 非空/空科室块：57 / 3
- 院区/出诊点标签关系：无
- 跨院区/出诊点详情 ID：0 个

| 同名 | 详情 ID |
|---|---|
| 周万兴 | 75,505 |
| 张卫 | 138,378 |
| 郭煜 | 379,150 |
| 余炯标 | 245,614 |
| 张滨 | 507,552 |
| 林强 | 576,510,577,611,578 |
| 董群伟 | 579,141,580,612,581 |
| 王华 | 161,526 |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：349
- 跨入口去重后唯一候选：349
- 跨入口重复关系：58
- 试采覆盖入口分类：0 个（无）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 无 | 无 | 无 |

## 广东药科大学附属第一医院推荐区、科室树、编码与照片全量采集对账

- 官网旧版 ASP 单页目录：推荐区 58 次 / 56 个唯一 ArticleID；角色 首席专家=14、科室负责人=44；全部与科室树重叠 58 次。
- 科室树：57 个科室，其中空科室 3 个；医生—科室关系 / 唯一数字 ArticleID：349 / 349。
- 详情顺序公开 GET：成功 349，失败 0；纯护理身份排除 2，合规候选 347。
- FULL 最终身份 340 行；同一官网照片归并 3 组；实质不同同名 7 组 / 14 行。
- 公开出诊点标签普查：健康管理中心=159、农林门诊=80、共和门诊=34；多出诊点详情 26 个。仅保留官网明确地点标签，不采集日期、星期、上午/下午等排班时段。
- 编码自检：响应头无 charset、meta 错标 UTF-8；按现场字节严格 GB18030/GBK 解码；替换字符 0、高置信乱码标记 0、列表/详情姓名不一致 0。
- 详情清洗：排班尾段排除 1、正式字段写入 0；排名/患者片段排除 0，患者案例排除 0；私用区字符清洗 1、正式字段残留 0。
- 照片普查：本人职业照 347、占位图 0、空图 0、拒绝路径 0。
- 照片四数：应采 340 / 实采 338 / 连续两次失败留空 2 / 无照片 2；本轮触发单次重试 4 张。
- 照片传输策略：同一官方图片 URL + 同一公开详情页 Referer + 同一请求头；首次 HTTP 非 200 或 Timeout/ConnectionError/ChunkedEncodingError/IncompleteRead 后等待 1 秒，仅重试 1 次；不注入 Cookie、不绕过验证；连续两次失败则留空并标注；原图不压缩；平均 462587 bytes，估算 347 张 / 160517689 bytes，大图阈值命中 205 张。
- 普通公开会话：requests 常规公开 GET；图片仅携带同域公开详情页 Referer，失败时保持 URL/Referer/请求头不变并等待 1 秒重试一次；未手工注入 Cookie、未绕过登录/验证码/挑战，未访问非公开接口；最终 Cookie 名称仅留痕为 `ASPSESSIONIDAGQCTAAC、mycookie`。Owner 已在 PR #48 明确审计通过并切换 FULL_APPEND_AND_OBSIDIAN；本报告为正式追加与画像生成输入。

### 四类科室汇总

| 类别 | 科室数 | 医生—科室关系 | 官方入口 |
|---|---:|---:|---|
| 内科 | 9 | 56 | https://www.gy120.net/zhuanjia.asp |
| 外科 | 12 | 79 | https://www.gy120.net/zhuanjia.asp |
| 其他科室 | 28 | 157 | https://www.gy120.net/zhuanjia.asp |
| 医技 | 8 | 57 | https://www.gy120.net/zhuanjia.asp |

### 57 个科室逐项关系

| 类别 | 科室 | 详情关系 |
|---|---|---:|
| 内科 | 心内一科 | 6 |
| 内科 | 心内二科 | 6 |
| 内科 | 血液内科 | 7 |
| 内科 | 呼吸与危重症医学科 | 8 |
| 内科 | 肾内科 | 6 |
| 内科 | 内分泌科 | 8 |
| 内科 | 消化内科 | 13 |
| 内科 | 风湿免疫科 | 1 |
| 内科 | 肥胖专病治疗组 | 1 |
| 外科 | 普外一科（肝胆外科） | 6 |
| 外科 | 普外二科（胃肠外科） | 3 |
| 外科 | 普外三科（整形美容科） | 6 |
| 外科 | 泌尿外科 | 11 |
| 外科 | 神经外科 | 9 |
| 外科 | 心胸外科 | 4 |
| 外科 | 乳腺科 | 2 |
| 外科 | 创伤与关节外科（骨一科） | 11 |
| 外科 | 脊柱外科（骨二科） | 7 |
| 外科 | 运动医学科（骨三科） | 5 |
| 外科 | 足踝与创面修复科（骨四科） | 7 |
| 外科 | 神经内科(头痛门诊) | 8 |
| 其他科室 | 中西医结合代谢病科 | 8 |
| 其他科室 | 急诊科 | 9 |
| 其他科室 | 疼痛科 | 1 |
| 其他科室 | 感染科共和诊室 | 0 |
| 其他科室 | 伤口造口治疗室 | 1 |
| 其他科室 | 妇产科 | 11 |
| 其他科室 | 儿科 | 5 |
| 其他科室 | 肠道门诊（农林） | 3 |
| 其他科室 | 门诊(普通外科) | 0 |
| 其他科室 | 门诊(普通内科) | 6 |
| 其他科室 | 介入治疗科 | 1 |
| 其他科室 | 口腔科 | 16 |
| 其他科室 | 心理科 | 3 |
| 其他科室 | 眼科 | 9 |
| 其他科室 | 正骨科 | 8 |
| 其他科室 | 耳鼻咽喉科 | 8 |
| 其他科室 | 皮肤科 | 3 |
| 其他科室 | 中医科 | 13 |
| 其他科室 | 康复医学科 | 12 |
| 其他科室 | 肿瘤一科 | 9 |
| 其他科室 | 肿瘤二科 | 3 |
| 其他科室 | 全科医学科 | 8 |
| 其他科室 | 重症医学科 | 4 |
| 其他科室 | 麻醉科 | 9 |
| 其他科室 | 理疗科 | 0 |
| 其他科室 | 健康管理部 | 3 |
| 其他科室 | 静脉导管护理门诊 | 3 |
| 其他科室 | 电生理专科门诊 | 1 |
| 医技 | 输血科 | 1 |
| 医技 | 药学部 | 13 |
| 医技 | 医学影像科 | 6 |
| 医技 | 检验科 | 17 |
| 医技 | 病理科 | 4 |
| 医技 | 物检科 | 9 |
| 医技 | 临床营养科 | 4 |
| 医技 | 核医学科 | 3 |

### 推荐区 58 次出现与科室树重叠对账

| ArticleID | 推荐角色 | 姓名/科室 | 来源链接 |
|---|---|---|---|
| 443 | 首席专家 | 郭姣 中西医结合代谢病科 | https://www.gy120.net/ArticleShow.asp?ArticleID=443 |
| 45 | 首席专家 | 潘宣 口腔科 | https://www.gy120.net/ArticleShow.asp?ArticleID=45 |
| 156 | 首席专家 | 何兴祥 消化内科 | https://www.gy120.net/ArticleShow.asp?ArticleID=156 |
| 75 | 首席专家 | 周万兴 心内一科 | https://www.gy120.net/ArticleShow.asp?ArticleID=75 |
| 101 | 首席专家 | 洪铭范 神经内科(头痛门诊) | https://www.gy120.net/ArticleShow.asp?ArticleID=101 |
| 133 | 首席专家 | 陈吉生 药学部 | https://www.gy120.net/ArticleShow.asp?ArticleID=133 |
| 24 | 首席专家 | 王希成 肿瘤一科 | https://www.gy120.net/ArticleShow.asp?ArticleID=24 |
| 145 | 首席专家 | 张威 神经外科 | https://www.gy120.net/ArticleShow.asp?ArticleID=145 |
| 7 | 首席专家 | 区奕猛 普外一科（肝胆外科） | https://www.gy120.net/ArticleShow.asp?ArticleID=7 |
| 76 | 首席专家 | 潘学谊 血液内科 | https://www.gy120.net/ArticleShow.asp?ArticleID=76 |
| 1 | 首席专家 | 刘华 全科医学科 | https://www.gy120.net/ArticleShow.asp?ArticleID=1 |
| 257 | 首席专家 | 肖文豪 风湿免疫科 | https://www.gy120.net/ArticleShow.asp?ArticleID=257 |
| 505 | 首席专家 | 周万兴 心内二科 | https://www.gy120.net/ArticleShow.asp?ArticleID=505 |
| 530 | 首席专家 | 王向宇 神经外科 | https://www.gy120.net/ArticleShow.asp?ArticleID=530 |
| 16 | 科室负责人 | 张伟斌 普外二科（胃肠外科） | https://www.gy120.net/ArticleShow.asp?ArticleID=16 |
| 24 | 科室负责人 | 王希成 肿瘤一科 | https://www.gy120.net/ArticleShow.asp?ArticleID=24 |
| 40 | 科室负责人 | 袁伟锋 呼吸与危重症医学科 | https://www.gy120.net/ArticleShow.asp?ArticleID=40 |
| 53 | 科室负责人 | 叶健华 内分泌科 | https://www.gy120.net/ArticleShow.asp?ArticleID=53 |
| 55 | 科室负责人 | 张永成 乳腺科 | https://www.gy120.net/ArticleShow.asp?ArticleID=55 |
| 60 | 科室负责人 | 钟德泉 神经外科 | https://www.gy120.net/ArticleShow.asp?ArticleID=60 |
| 91 | 科室负责人 | 鲍炯琳 眼科 | https://www.gy120.net/ArticleShow.asp?ArticleID=91 |
| 139 | 科室负责人 | 曾智桓 心内二科 | https://www.gy120.net/ArticleShow.asp?ArticleID=139 |
| 150 | 科室负责人 | 郭煜 输血科 | https://www.gy120.net/ArticleShow.asp?ArticleID=150 |
| 174 | 科室负责人 | 张明兴 康复医学科 | https://www.gy120.net/ArticleShow.asp?ArticleID=174 |
| 177 | 科室负责人 | 洪敏 中医科 | https://www.gy120.net/ArticleShow.asp?ArticleID=177 |
| 196 | 科室负责人 | 曾育辉 急诊科 | https://www.gy120.net/ArticleShow.asp?ArticleID=196 |
| 201 | 科室负责人 | 王森 泌尿外科 | https://www.gy120.net/ArticleShow.asp?ArticleID=201 |
| 209 | 科室负责人 | 吕路 肾内科 | https://www.gy120.net/ArticleShow.asp?ArticleID=209 |
| 212 | 科室负责人 | 吴礼浩 消化内科 | https://www.gy120.net/ArticleShow.asp?ArticleID=212 |
| 236 | 科室负责人 | 李平 普外三科（整形美容科） | https://www.gy120.net/ArticleShow.asp?ArticleID=236 |
| 242 | 科室负责人 | 马立恒 医学影像科 | https://www.gy120.net/ArticleShow.asp?ArticleID=242 |
| 243 | 科室负责人 | 罗永平 普外一科（肝胆外科） | https://www.gy120.net/ArticleShow.asp?ArticleID=243 |
| 248 | 科室负责人 | 黄飞麒 正骨科 | https://www.gy120.net/ArticleShow.asp?ArticleID=248 |
| 253 | 科室负责人 | 陆崇 健康管理部 | https://www.gy120.net/ArticleShow.asp?ArticleID=253 |
| 257 | 科室负责人 | 肖文豪 风湿免疫科 | https://www.gy120.net/ArticleShow.asp?ArticleID=257 |
| 258 | 科室负责人 | 赵泳谊 临床营养科 | https://www.gy120.net/ArticleShow.asp?ArticleID=258 |
| 268 | 科室负责人 | 茹晃耀 重症医学科 | https://www.gy120.net/ArticleShow.asp?ArticleID=268 |
| 279 | 科室负责人 | 李张维 口腔科 | https://www.gy120.net/ArticleShow.asp?ArticleID=279 |
| 314 | 科室负责人 | 幸冰峰 中西医结合代谢病科 | https://www.gy120.net/ArticleShow.asp?ArticleID=314 |
| 332 | 科室负责人 | 刘爱群 神经内科(头痛门诊) | https://www.gy120.net/ArticleShow.asp?ArticleID=332 |
| 340 | 科室负责人 | 关则兵 血液内科 | https://www.gy120.net/ArticleShow.asp?ArticleID=340 |
| 342 | 科室负责人 | 孟翠萍 儿科 | https://www.gy120.net/ArticleShow.asp?ArticleID=342 |
| 345 | 科室负责人 | 袁建伟 核医学科 | https://www.gy120.net/ArticleShow.asp?ArticleID=345 |
| 351 | 科室负责人 | 杨小蓉 检验科 | https://www.gy120.net/ArticleShow.asp?ArticleID=351 |
| 370 | 科室负责人 | 林忠伟 心内一科 | https://www.gy120.net/ArticleShow.asp?ArticleID=370 |
| 387 | 科室负责人 | 骆婕 妇产科 | https://www.gy120.net/ArticleShow.asp?ArticleID=387 |
| 390 | 科室负责人 | 杨曙 肿瘤二科 | https://www.gy120.net/ArticleShow.asp?ArticleID=390 |
| 431 | 科室负责人 | 周辉 神经外科 | https://www.gy120.net/ArticleShow.asp?ArticleID=431 |
| 475 | 科室负责人 | 陈建颜 麻醉科 | https://www.gy120.net/ArticleShow.asp?ArticleID=475 |
| 482 | 科室负责人 | 肖海平 心胸外科 | https://www.gy120.net/ArticleShow.asp?ArticleID=482 |
| 484 | 科室负责人 | 沈建红 物检科 | https://www.gy120.net/ArticleShow.asp?ArticleID=484 |
| 485 | 科室负责人 | 何雁冰 疼痛科 | https://www.gy120.net/ArticleShow.asp?ArticleID=485 |
| 487 | 科室负责人 | 仇志坤 药学部 | https://www.gy120.net/ArticleShow.asp?ArticleID=487 |
| 497 | 科室负责人 | 郑坚奕 心内二科 | https://www.gy120.net/ArticleShow.asp?ArticleID=497 |
| 511 | 科室负责人 | 朱辉 脊柱外科（骨二科） | https://www.gy120.net/ArticleShow.asp?ArticleID=511 |
| 515 | 科室负责人 | 李晓初 创伤与关节外科（骨一科） | https://www.gy120.net/ArticleShow.asp?ArticleID=515 |
| 523 | 科室负责人 | 刘琦 口腔科 | https://www.gy120.net/ArticleShow.asp?ArticleID=523 |
| 531 | 科室负责人 | 张福宏 耳鼻咽喉科 | https://www.gy120.net/ArticleShow.asp?ArticleID=531 |

### 349 个唯一 ArticleID 逐详情对账

| ArticleID | 列表姓名 | 详情姓名 | 类别 | 列表科室 | 详情科室 | 公开出诊点 | 职称 | 照片状态 | 处置 | 来源链接 |
|---|---|---|---|---|---|---|---|---|---|---|
| 370 | 林忠伟 | 林忠伟 | 内科 | 心内一科 | 心内一科 | 健康管理中心 | 医学博士、主任医师、教授、硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=370 |
| 75 | 周万兴 | 周万兴 | 内科 | 心内一科 | 心内一科 | 健康管理中心 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=75 |
| 72 | 雷达 | 雷达 | 内科 | 心内一科 | 心内一科 | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=72 |
| 119 | 朱桂平 | 朱桂平 | 内科 | 心内一科 | 心内一科 | 健康管理中心 | 教授、主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=119 |
| 107 | 李国标 | 李国标 | 内科 | 心内一科 | 心内一科 | 健康管理中心 | 教授、主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=107 |
| 500 | 韩彬 | 韩彬 | 内科 | 心内一科 | 心内一科 | 健康管理中心 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=500 |
| 505 | 周万兴 | 周万兴 | 内科 | 心内二科 | 心内二科 | 健康管理中心 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=505 |
| 139 | 曾智桓 | 曾智桓 | 内科 | 心内二科 | 心内二科 | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=139 |
| 229 | 张莉 | 张莉 | 内科 | 心内二科 | 心内二科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=229 |
| 138 | 张卫 | 张卫 | 内科 | 心内二科 | 心内二科 | 健康管理中心 | 教授、主任医师、硕士生导师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=138 |
| 497 | 郑坚奕 | 郑坚奕 | 内科 | 心内二科 | 心内二科 | 健康管理中心 | 副主任医师、副教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=497 |
| 498 | 王宗涛 | 王宗涛 | 内科 | 心内二科 | 心内二科 | 健康管理中心 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=498 |
| 76 | 潘学谊 | 潘学谊 | 内科 | 血液内科 | 血液内科 | 健康管理中心 | 教授，主任医师，硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=76 |
| 340 | 关则兵 | 关则兵 | 内科 | 血液内科 | 血液内科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=340 |
| 115 | 叶美莲 | 叶美莲 | 内科 | 血液内科 | 血液内科 | 官网详情未标注 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=115 |
| 341 | 迟作华 | 迟作华 | 内科 | 血液内科 | 血液内科 | 官网详情未标注 | 副主任医师，副教授，血液学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=341 |
| 379 | 郭煜 | 郭煜 | 内科 | 血液内科 | 血液内科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=379 |
| 547 | 周兰兰 | 周兰兰 | 内科 | 血液内科 | 血液内科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=547 |
| 380 | 曾文彬 | 曾文彬 | 内科 | 血液内科 | 血液内科 | 健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=380 |
| 40 | 袁伟锋 | 袁伟锋 | 内科 | 呼吸与危重症医学科 | 呼吸与危重症医学科 | 健康管理中心 | 主任医师、医学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=40 |
| 222 | 王虹 | 王虹 | 内科 | 呼吸与危重症医学科 | 呼吸与危重症医学科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=222 |
| 223 | 关向群 | 关向群 | 内科 | 呼吸与危重症医学科 | 呼吸与危重症医学科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=223 |
| 416 | 毛锐 | 毛锐 | 内科 | 呼吸与危重症医学科 | 呼吸与危重症医学科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=416 |
| 567 | 崔莉 | 崔莉 | 内科 | 呼吸与危重症医学科 | 呼吸与危重症医学科 | 健康管理中心 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=567 |
| 574 | 邢秋云 | 邢秋云 | 内科 | 呼吸与危重症医学科 | 呼吸与危重症医学科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=574 |
| 568 | 张少卿 | 张少卿 | 内科 | 呼吸与危重症医学科 | 呼吸与危重症医学科 | 健康管理中心 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=568 |
| 357 | 李兰英 | 李兰英 | 内科 | 呼吸与危重症医学科 | 呼吸与危重症医学科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=357 |
| 209 | 吕路 | 吕路 | 内科 | 肾内科 | 肾内科 | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=209 |
| 121 | 蒋文功 | 蒋文功 | 内科 | 肾内科 | 肾内科 | 健康管理中心 | 教授、主任医师、硕士生导师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=121 |
| 157 | 黄培华 | 黄培华 | 内科 | 肾内科 | 肾内科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=157 |
| 569 | 杨天开 | 杨天开 | 内科 | 肾内科 | 肾内科 | 健康管理中心 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=569 |
| 61 | 桓文穆 | 桓文穆 | 内科 | 肾内科 | 肾内科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=61 |
| 62 | 黄华 | 黄华 | 内科 | 肾内科 | 肾内科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=62 |
| 53 | 叶健华 | 叶健华 | 内科 | 内分泌科 | 内分泌科 | 共和门诊 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=53 |
| 54 | 周昭远 | 周昭远 | 内科 | 内分泌科 | 内分泌科 | 健康管理中心 | 副教授、副主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=54 |
| 354 | 孙平 | 孙平 | 内科 | 内分泌科 | 内分泌科 | 健康管理中心、共和门诊 | 副主任医师，副教授，硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=354 |
| 204 | 马承红 | 马承红 | 内科 | 内分泌科 | 内分泌科 | 健康管理中心、共和门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=204 |
| 327 | 胡丽 | 胡丽 | 内科 | 内分泌科 | 内分泌科 | 健康管理中心、共和门诊 | 住院医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=327 |
| 205 | 廖瘳 | 廖瘳 | 内科 | 内分泌科 | 内分泌科 | 共和门诊、健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=205 |
| 328 | 刘楠 | 刘楠 | 内科 | 内分泌科 | 内分泌科 | 共和门诊、健康管理中心 | 住院医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=328 |
| 329 | 莫旭旭 | 莫旭旭 | 内科 | 内分泌科 | 内分泌科 | 共和门诊、健康管理中心 | 住院医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=329 |
| 156 | 何兴祥 | 何兴祥 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 二级教授、主任医师、博士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=156 |
| 212 | 吴礼浩 | 吴礼浩 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=212 |
| 66 | 邝小枫 | 邝小枫 | 内科 | 消化内科 | 消化内科 | 共和门诊、农林门诊 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=66 |
| 453 | 钱国强 | 钱国强 | 内科 | 消化内科 | 消化内科 | 农林门诊 | 教授，主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=453 |
| 214 | 谢文瑞 | 谢文瑞 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 主任医师，教授，硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=214 |
| 211 | 袁瑜 | 袁瑜 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=211 |
| 210 | 蔡洁毅 | 蔡洁毅 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=210 |
| 441 | 林绍强 | 林绍强 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 教授、博士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=441 |
| 566 | 秦治初 | 秦治初 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=566 |
| 293 | 李兰 | 李兰 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=293 |
| 294 | 罗丹萍 | 罗丹萍 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 住院医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=294 |
| 296 | 周慧敏 | 周慧敏 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 住院医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=296 |
| 292 | 梁芬芬 | 梁芬芬 | 内科 | 消化内科 | 消化内科 | 健康管理中心 | 住院医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=292 |
| 257 | 肖文豪 | 肖文豪 | 内科 | 风湿免疫科 | 风湿免疫科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=257 |
| 230 | 孙慧琳 | 孙慧琳 | 内科 | 肥胖专病治疗组 | 肥胖专病治疗组 | 健康管理中心 | 主任医师、教授、医学博士、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=230 |
| 7 | 区奕猛 | 区奕猛 | 外科 | 普外一科（肝胆外科） | 普外一科（肝胆外科） | 官网详情未标注 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=7 |
| 8 | 连福珍 | 连福珍 | 外科 | 普外一科（肝胆外科） | 普外一科（肝胆外科） | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=8 |
| 243 | 罗永平 | 罗永平 | 外科 | 普外一科（肝胆外科） | 普外一科（肝胆外科） | 健康管理中心 | 主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=243 |
| 179 | 马兴标 | 马兴标 | 外科 | 普外一科（肝胆外科） | 普外一科（肝胆外科） | 官网详情未标注 | 副教授 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=179 |
| 245 | 余炯标 | 余炯标 | 外科 | 普外一科（肝胆外科） | 普外一科（肝胆外科） | 农林门诊 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=245 |
| 275 | 黄树圭 | 黄树圭 | 外科 | 普外一科（肝胆外科） | 普外一科（肝胆外科） | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=275 |
| 16 | 张伟斌 | 张伟斌 | 外科 | 普外二科（胃肠外科） | 普外二科（胃肠外科） | 健康管理中心 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=16 |
| 15 | 吴敏华 | 吴敏华 | 外科 | 普外二科（胃肠外科） | 普外二科（胃肠外科） | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=15 |
| 413 | 陈丹 | 陈丹 | 外科 | 普外二科（胃肠外科） | 普外二科（胃肠外科） | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=413 |
| 236 | 李平 | 李平 | 外科 | 普外三科（整形美容科） | 普外三科（整形美容科） | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=236 |
| 172 | 惠俐 | 惠俐 | 外科 | 普外三科（整形美容科） | 普外三科（整形美容科） | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=172 |
| 237 | 陈元良 | 陈元良 | 外科 | 普外三科（整形美容科） | 普外三科（整形美容科） | 健康管理中心 | 副主任医师，副教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=237 |
| 238 | 赵欣欣 | 赵欣欣 | 外科 | 普外三科（整形美容科） | 普外三科（整形美容科） | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=238 |
| 590 | 余文林 | 余文林 | 外科 | 普外三科（整形美容科） | 普外三科（整形美容科） | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=590 |
| 591 | 刘志刚 | 刘志刚 | 外科 | 普外三科（整形美容科） | 普外三科（整形美容科） | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=591 |
| 377 | 郑祥光 | 郑祥光 | 外科 | 泌尿外科 | 泌尿外科 | 农林门诊 | 教授，主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=377 |
| 51 | 罗力 | 罗力 | 外科 | 泌尿外科 | 泌尿外科 | 健康管理中心 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=51 |
| 159 | 王玺坤 | 王玺坤 | 外科 | 泌尿外科 | 泌尿外科 | 健康管理中心 | 教授、主任医师、医学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=159 |
| 546 | 陈三三 | 陈三三 | 外科 | 泌尿外科 | 泌尿外科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=546 |
| 200 | 李峻 | 李峻 | 外科 | 泌尿外科 | 泌尿外科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=200 |
| 201 | 王森 | 王森 | 外科 | 泌尿外科 | 泌尿外科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=201 |
| 160 | 钱聚标 | 钱聚标 | 外科 | 泌尿外科 | 泌尿外科 | 官网详情未标注 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=160 |
| 180 | 王忠 | 王忠 | 外科 | 泌尿外科 | 泌尿外科 | 官网详情未标注 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=180 |
| 202 | 白亮 | 白亮 | 外科 | 泌尿外科 | 泌尿外科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=202 |
| 203 | 高炜城 | 高炜城 | 外科 | 泌尿外科 | 泌尿外科 | 官网详情未标注 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=203 |
| 507 | 张滨 | 张滨 | 外科 | 泌尿外科 | 泌尿外科 | 健康管理中心 | 主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=507 |
| 145 | 张威 | 张威 | 外科 | 神经外科 | 神经外科 | 官网详情未标注 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=145 |
| 530 | 王向宇 | 王向宇 | 外科 | 神经外科 | 神经外科 | 健康管理中心 | 主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=530 |
| 60 | 钟德泉 | 钟德泉 | 外科 | 神经外科 | 神经外科 | 健康管理中心 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=60 |
| 58 | 殷利明 | 殷利明 | 外科 | 神经外科 | 神经外科 | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=58 |
| 431 | 周辉 | 周辉 | 外科 | 神经外科 | 神经外科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=431 |
| 467 | 刘沣 | 刘沣 | 外科 | 神经外科 | 神经外科 | 健康管理中心 | 教授、副主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=467 |
| 206 | 赵展 | 赵展 | 外科 | 神经外科 | 神经外科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=206 |
| 207 | 王文涛 | 王文涛 | 外科 | 神经外科 | 神经外科 | 健康管理中心 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=207 |
| 208 | 徐伟光 | 徐伟光 | 外科 | 神经外科 | 神经外科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=208 |
| 482 | 肖海平 | 肖海平 | 外科 | 心胸外科 | 心胸外科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=482 |
| 70 | 章海波 | 章海波 | 外科 | 心胸外科 | 心胸外科 | 官网详情未标注 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=70 |
| 233 | 祝曙光 | 祝曙光 | 外科 | 心胸外科 | 心胸外科 | 官网详情未标注 | 主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=233 |
| 105 | 黄壮荣 | 黄壮荣 | 外科 | 心胸外科 | 心胸外科 | 农林门诊 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=105 |
| 55 | 张永成 | 张永成 | 外科 | 乳腺科 | 乳腺科 | 农林门诊 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=55 |
| 373 | 沙莉 | 沙莉 | 外科 | 乳腺科 | 乳腺科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=373 |
| 576 | 林强 | 林强 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 健康管理中心 | 主任医师、博士、硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=576 |
| 579 | 董群伟 | 董群伟 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 农林门诊 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=579 |
| 161 | 王华 | 王华 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=161 |
| 515 | 李晓初 | 李晓初 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=515 |
| 420 | 宋炎成 | 宋炎成 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 健康管理中心 | 主任医师、教授、硕士生导师、医学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=420 |
| 219 | 王晓东 | 王晓东 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=219 |
| 34 | 冯振华 | 冯振华 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=34 |
| 221 | 郝群禹 | 郝群禹 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=221 |
| 35 | 郭洲 | 郭洲 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=35 |
| 455 | 昌宏 | 昌宏 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 健康管理中心 | 副主任医师 副教授 医学博士 骨科支部党支部书记 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=455 |
| 516 | 蔡杨庭 | 蔡杨庭 | 外科 | 创伤与关节外科（骨一科） | 创伤与关节外科（骨一科） | 健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=516 |
| 141 | 董群伟 | 董群伟 | 外科 | 脊柱外科（骨二科） | 脊柱外科（骨二科） | 农林门诊 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=141 |
| 510 | 林强 | 林强 | 外科 | 脊柱外科（骨二科） | 脊柱外科（骨二科） | 健康管理中心 | 主任医师、博士、硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=510 |
| 511 | 朱辉 | 朱辉 | 外科 | 脊柱外科（骨二科） | 脊柱外科（骨二科） | 健康管理中心 | 副主任医师、副教授、医学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=511 |
| 36 | 洪曼杰 | 洪曼杰 | 外科 | 脊柱外科（骨二科） | 脊柱外科（骨二科） | 官网详情未标注 | 主任医师、教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=36 |
| 512 | 胡伶平 | 胡伶平 | 外科 | 脊柱外科（骨二科） | 脊柱外科（骨二科） | 健康管理中心 | 副主任医师、副教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=512 |
| 37 | 巫培康 | 巫培康 | 外科 | 脊柱外科（骨二科） | 脊柱外科（骨二科） | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=37 |
| 490 | 王健 | 王健 | 外科 | 脊柱外科（骨二科） | 脊柱外科（骨二科） | 健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=490 |
| 577 | 林强 | 林强 | 外科 | 运动医学科（骨三科） | 运动医学科（骨三科） | 健康管理中心 | 主任医师、博士、硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=577 |
| 580 | 董群伟 | 董群伟 | 外科 | 运动医学科（骨三科） | 运动医学科（骨三科） | 农林门诊 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=580 |
| 526 | 王华 | 王华 | 外科 | 运动医学科（骨三科） | 运动医学科（骨三科） | 健康管理中心 | 外科学副教授，骨外科副主任医师，临床医学概论教研室主任 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=526 |
| 527 | 罗学辉 | 罗学辉 | 外科 | 运动医学科（骨三科） | 运动医学科（骨三科） | 健康管理中心 | 主任医师 骨三科负责人 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=527 |
| 525 | 庾广文 | 庾广文 | 外科 | 运动医学科（骨三科） | 运动医学科（骨三科） | 健康管理中心 | 医学博士，副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=525 |
| 611 | 林强 | 林强 | 外科 | 足踝与创面修复科（骨四科） | 足踝与创面修复科（骨四科） | 健康管理中心 | 常务副院长（主持行政工作）、骨科中心主任、主任医师、博士、博士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=611 |
| 612 | 董群伟 | 董群伟 | 外科 | 足踝与创面修复科（骨四科） | 足踝与创面修复科（骨四科） | 农林门诊 | 副院长、主任医师、教授、硕士研究生导师、岭南名医、羊城好医生 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=612 |
| 613 | 王凤雄 | 王凤雄 | 外科 | 足踝与创面修复科（骨四科） | 足踝与创面修复科（骨四科） | 官网详情未标注 | 足踝与创面修复科科主任 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=613 |
| 614 | 余炯标 | 余炯标 | 外科 | 足踝与创面修复科（骨四科） | 足踝与创面修复科（骨四科） | 农林门诊 | 副主任医师，副教授，硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=614 |
| 615 | 王飞 | 王飞 | 外科 | 足踝与创面修复科（骨四科） | 足踝与创面修复科（骨四科） | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=615 |
| 616 | 林宇凤 | 林宇凤 | 外科 | 足踝与创面修复科（骨四科） | 足踝与创面修复科（骨四科） | 官网详情未标注 | 主治医师，北京大学医学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=616 |
| 617 | 林伟鹏 | 林伟鹏 | 外科 | 足踝与创面修复科（骨四科） | 足踝与创面修复科（骨四科） | 官网详情未标注 | 主治医师，硕士研究生 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=617 |
| 101 | 洪铭范 | 洪铭范 | 外科 | 神经内科(头痛门诊) | 神经内科(头痛门诊) | 农林门诊、健康管理中心 | 教授、主任医师、博士生导师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=101 |
| 228 | 彭忠兴 | 彭忠兴 | 外科 | 神经内科(头痛门诊) | 神经内科(头痛门诊) | 健康管理中心 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=228 |
| 332 | 刘爱群 | 刘爱群 | 外科 | 神经内科(头痛门诊) | 神经内科(头痛门诊) | 健康管理中心 | 主任医师、教授、硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=332 |
| 486 | 周志华 | 周志华 | 外科 | 神经内科(头痛门诊) | 神经内科(头痛门诊) | 健康管理中心 | 副教授，副主任医师，硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=486 |
| 151 | 余青云 | 余青云 | 外科 | 神经内科(头痛门诊) | 神经内科(头痛门诊) | 健康管理中心 | 主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=151 |
| 109 | 刘玉华 | 刘玉华 | 外科 | 神经内科(头痛门诊) | 神经内科(头痛门诊) | 健康管理中心 | 主任医师、教授、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=109 |
| 410 | 危智盛 | 危智盛 | 外科 | 神经内科(头痛门诊) | 神经内科(头痛门诊) | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=410 |
| 411 | 刁胜朋 | 刁胜朋 | 外科 | 神经内科(头痛门诊) | 神经内科(头痛门诊) | 健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=411 |
| 443 | 郭姣 | 郭姣 | 其他科室 | 中西医结合代谢病科 | 中西医结合代谢病科 | 健康管理中心 | 医学博士，主任医师，二级教授，博士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=443 |
| 465 | 李雄 | 李雄 | 其他科室 | 中西医结合代谢病科 | 中西医结合代谢病科 | 农林门诊 | 原中南大学湘雅医院特聘教授，博士生导师，主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=465 |
| 314 | 幸冰峰 | 幸冰峰 | 其他科室 | 中西医结合代谢病科 | 中西医结合代谢病科 | 共和门诊、健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=314 |
| 445 | 朴胜华 | 朴胜华 | 其他科室 | 中西医结合代谢病科 | 中西医结合代谢病科 | 健康管理中心 | 副研究员、副主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=445 |
| 466 | 金英花 | 金英花 | 其他科室 | 中西医结合代谢病科 | 中西医结合代谢病科 | 健康管理中心 | 主任中医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=466 |
| 598 | 万利梅 | 万利梅 | 其他科室 | 中西医结合代谢病科 | 中西医结合代谢病科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=598 |
| 317 | 陈滢宇 | 陈滢宇 | 其他科室 | 中西医结合代谢病科 | 中西医结合代谢病科 | 健康管理中心 | 医学博士，主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=317 |
| 324 | 刁蔚欣 | 刁蔚欣 | 其他科室 | 中西医结合代谢病科 | 中西医结合代谢病科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=324 |
| 196 | 曾育辉 | 曾育辉 | 其他科室 | 急诊科 | 急诊科 | 官网详情未标注 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=196 |
| 197 | 梁秋玲 | 梁秋玲 | 其他科室 | 急诊科 | 急诊科 | 官网详情未标注 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=197 |
| 343 | 黄穗霞 | 黄穗霞 | 其他科室 | 急诊科 | 急诊科 | 官网详情未标注 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=343 |
| 610 | 常威 | 常威 | 其他科室 | 急诊科 | 急诊科 | 官网详情未标注 | 副主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=610 |
| 608 | 朱海平 | 朱海平 | 其他科室 | 急诊科 | 急诊科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=608 |
| 609 | 韦焕杰 | 韦焕杰 | 其他科室 | 急诊科 | 急诊科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=609 |
| 346 | 陈瑞芳 | 陈瑞芳 | 其他科室 | 急诊科 | 急诊科 | 官网详情未标注 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=346 |
| 347 | 李孟升 | 李孟升 | 其他科室 | 急诊科 | 急诊科 | 官网详情未标注 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=347 |
| 436 | 张凡 | 张凡 | 其他科室 | 急诊科 | 急诊科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=436 |
| 485 | 何雁冰 | 何雁冰 | 其他科室 | 疼痛科 | 疼痛科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=485 |
| 404 | 何淑敏 | 何淑敏 | 其他科室 | 伤口造口治疗室 | 伤口造口治疗室 | 农林门诊、共和门诊 | 护师，国际造口治疗师 | available | 护理身份排除 | https://www.gy120.net/articleshow.asp?articleid=404 |
| 387 | 骆婕 | 骆婕 | 其他科室 | 妇产科 | 妇产科 | 农林门诊 | 主任医师、硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=387 |
| 112 | 陶莹 | 陶莹 | 其他科室 | 妇产科 | 妇产科 | 农林门诊 | 教授，主任医师，硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=112 |
| 164 | 王浩 | 王浩 | 其他科室 | 妇产科 | 妇产科 | 农林门诊 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=164 |
| 100 | 何力 | 何力 | 其他科室 | 妇产科 | 妇产科 | 农林门诊 | 主任医师、教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=100 |
| 336 | 李筠 | 李筠 | 其他科室 | 妇产科 | 妇产科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=336 |
| 96 | 高瑞萍 | 高瑞萍 | 其他科室 | 妇产科 | 妇产科 | 农林门诊 | 教授、主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=96 |
| 384 | 郭琴 | 郭琴 | 其他科室 | 妇产科 | 妇产科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=384 |
| 396 | 廖凤儿 | 廖凤儿 | 其他科室 | 妇产科 | 妇产科 | 农林门诊 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=396 |
| 432 | 赵曼丹 | 赵曼丹 | 其他科室 | 妇产科 | 妇产科 | 农林门诊 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=432 |
| 605 | 郭苑莉 | 郭苑莉 | 其他科室 | 妇产科 | 妇产科 | 官网详情未标注 | 副主任医师、医学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=605 |
| 606 | 郑婷 | 郑婷 | 其他科室 | 妇产科 | 妇产科 | 官网详情未标注 | 副主任医师，硕士研究生 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=606 |
| 342 | 孟翠萍 | 孟翠萍 | 其他科室 | 儿科 | 儿科 | 健康管理中心 | 主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=342 |
| 11 | 冯卓玲 | 冯卓玲 | 其他科室 | 儿科 | 儿科 | 官网详情未标注 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=11 |
| 167 | 钱蔚珍 | 钱蔚珍 | 其他科室 | 儿科 | 儿科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=167 |
| 4 | 潘昊 | 潘昊 | 其他科室 | 儿科 | 儿科 | 健康管理中心 | 副教授、副主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=4 |
| 597 | 王崧 | 王崧 | 其他科室 | 儿科 | 儿科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=597 |
| 149 | 贺爱辉 | 贺爱辉 | 其他科室 | 肠道门诊（农林） | 肠道门诊（农林） | 官网详情未标注 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=149 |
| 32 | 张少华 | 张少华 | 其他科室 | 肠道门诊（农林） | 肠道门诊（农林） | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=32 |
| 325 | 李烨 | 李烨 | 其他科室 | 肠道门诊（农林） | 肠道门诊（农林） | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=325 |
| 117 | 尹金柱 | 尹金柱 | 其他科室 | 门诊(普通内科) | 门诊(普通内科) | 共和门诊 | 教授、主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=117 |
| 560 | 苏妤 | 苏妤 | 其他科室 | 门诊(普通内科) | 门诊(普通内科) | 官网详情未标注 | 副主任医师、国家二级心理咨询师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=560 |
| 158 | 管红斌 | 管红斌 | 其他科室 | 门诊(普通内科) | 门诊(普通内科) | 共和门诊 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=158 |
| 447 | 王洪云 | 王洪云 | 其他科室 | 门诊(普通内科) | 门诊(普通内科) | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=447 |
| 364 | 杨驱云 | 杨驱云 | 其他科室 | 门诊(普通内科) | 门诊(普通内科) | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=364 |
| 334 | 黄四邑 | 黄四邑 | 其他科室 | 门诊(普通内科) | 门诊(普通内科) | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=334 |
| 276 | 武兴杰 | 武兴杰 | 其他科室 | 介入治疗科 | 介入治疗科 | 农林门诊 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=276 |
| 523 | 刘琦 | 刘琦 | 其他科室 | 口腔科 | 口腔科 | 农林门诊、健康管理中心 | 主任医师，教授。医学博士，留美学者，研究生导师，博士后合作导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=523 |
| 45 | 潘宣 | 潘宣 | 其他科室 | 口腔科 | 口腔科 | 农林门诊 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=45 |
| 113 | 王玉栋 | 王玉栋 | 其他科室 | 口腔科 | 口腔科 | 农林门诊、共和门诊 | 教授，主任医师，硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=113 |
| 94 | 冯铁军 | 冯铁军 | 其他科室 | 口腔科 | 口腔科 | 农林门诊 | 副教授 主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=94 |
| 44 | 黎慧瑜 | 黎慧瑜 | 其他科室 | 口腔科 | 口腔科 | 共和门诊、农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=44 |
| 46 | 周银凤 | 周银凤 | 其他科室 | 口腔科 | 口腔科 | 官网详情未标注 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=46 |
| 279 | 李张维 | 李张维 | 其他科室 | 口腔科 | 口腔科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=279 |
| 277 | 康成容 | 康成容 | 其他科室 | 口腔科 | 口腔科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=277 |
| 289 | 陈凯 | 陈凯 | 其他科室 | 口腔科 | 口腔科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=289 |
| 288 | 陈慧芝 | 陈慧芝 | 其他科室 | 口腔科 | 口腔科 | 农林门诊 | 副教授 、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=288 |
| 291 | 许志锋 | 许志锋 | 其他科室 | 口腔科 | 口腔科 | 农林门诊 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=291 |
| 183 | 贺凌飞 | 贺凌飞 | 其他科室 | 口腔科 | 口腔科 | 共和门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=183 |
| 281 | 马穗齐 | 马穗齐 | 其他科室 | 口腔科 | 口腔科 | 共和门诊 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=281 |
| 278 | 李梁 | 李梁 | 其他科室 | 口腔科 | 口腔科 | 农林门诊 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=278 |
| 285 | 周倩冰 | 周倩冰 | 其他科室 | 口腔科 | 口腔科 | 共和门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=285 |
| 290 | 何智君 | 何智君 | 其他科室 | 口腔科 | 口腔科 | 农林门诊 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=290 |
| 68 | 张柏芳 | 张柏芳 | 其他科室 | 心理科 | 心理科 | 共和门诊、健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=68 |
| 104 | 黄雪薇 | 黄雪薇 | 其他科室 | 心理科 | 心理科 | 农林门诊 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=104 |
| 102 | 皇甫丽 | 皇甫丽 | 其他科室 | 心理科 | 心理科 | 共和门诊、健康管理中心 | 教授、主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=102 |
| 91 | 鲍炯琳 | 鲍炯琳 | 其他科室 | 眼科 | 眼科 | 健康管理中心 | 教授、主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=91 |
| 108 | 林敏 | 林敏 | 其他科室 | 眼科 | 眼科 | 官网详情未标注 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=108 |
| 80 | 罗小静 | 罗小静 | 其他科室 | 眼科 | 眼科 | 共和门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=80 |
| 147 | 周斌兵 | 周斌兵 | 其他科室 | 眼科 | 眼科 | 农林门诊 | 主任医师，副教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=147 |
| 148 | 朱宇东 | 朱宇东 | 其他科室 | 眼科 | 眼科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=148 |
| 215 | 林文雄 | 林文雄 | 其他科室 | 眼科 | 眼科 | 健康管理中心 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=215 |
| 216 | 李青 | 李青 | 其他科室 | 眼科 | 眼科 | 健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=216 |
| 587 | 臧晶 | 臧晶 | 其他科室 | 眼科 | 眼科 | 健康管理中心 | 主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=587 |
| 298 | 王文娟 | 王文娟 | 其他科室 | 眼科 | 眼科 | 农林门诊 | 住院医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=298 |
| 578 | 林强 | 林强 | 其他科室 | 正骨科 | 正骨科 | 健康管理中心 | 主任医师、博士、硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=578 |
| 581 | 董群伟 | 董群伟 | 其他科室 | 正骨科 | 正骨科 | 农林门诊 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=581 |
| 248 | 黄飞麒 | 黄飞麒 | 其他科室 | 正骨科 | 正骨科 | 共和门诊、健康管理中心 | 主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=248 |
| 247 | 陈扬声 | 陈扬声 | 其他科室 | 正骨科 | 正骨科 | 共和门诊、健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=247 |
| 561 | 陈晓波 | 陈晓波 | 其他科室 | 正骨科 | 正骨科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=561 |
| 84 | 姚乃捷 | 姚乃捷 | 其他科室 | 正骨科 | 正骨科 | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=84 |
| 249 | 赵晓 | 赵晓 | 其他科室 | 正骨科 | 正骨科 | 健康管理中心、共和门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=249 |
| 302 | 林展 | 林展 | 其他科室 | 正骨科 | 正骨科 | 共和门诊、健康管理中心 | 医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=302 |
| 531 | 张福宏 | 张福宏 | 其他科室 | 耳鼻咽喉科 | 耳鼻咽喉科 | 农林门诊 | 主任医师、教授、临床医学专业硕士、耳鼻咽喉科主任 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=531 |
| 137 | 姚良忠 | 姚良忠 | 其他科室 | 耳鼻咽喉科 | 耳鼻咽喉科 | 农林门诊 | 主任医师 、教授、 硕士研究生导师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=137 |
| 193 | 潘智灵 | 潘智灵 | 其他科室 | 耳鼻咽喉科 | 耳鼻咽喉科 | 农林门诊 | 主任医师、教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=193 |
| 532 | 左可军 | 左可军 | 其他科室 | 耳鼻咽喉科 | 耳鼻咽喉科 | 官网详情未标注 | 医学博士，主任医师，教授，硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=532 |
| 403 | 刘俊捷 | 刘俊捷 | 其他科室 | 耳鼻咽喉科 | 耳鼻咽喉科 | 农林门诊 | 副主任医师、副教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=403 |
| 401 | 朱艳丽 | 朱艳丽 | 其他科室 | 耳鼻咽喉科 | 耳鼻咽喉科 | 农林门诊 | 副主任医师、副教授、医学硕士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=401 |
| 533 | 党华 | 党华 | 其他科室 | 耳鼻咽喉科 | 耳鼻咽喉科 | 官网详情未标注 | 副主任医师，副教授，硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=533 |
| 534 | 武俊男 | 武俊男 | 其他科室 | 耳鼻咽喉科 | 耳鼻咽喉科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=534 |
| 5 | 单孔荣 | 单孔荣 | 其他科室 | 皮肤科 | 皮肤科 | 健康管理中心、共和门诊 | 副教授、副主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=5 |
| 428 | 罗丽芳 | 罗丽芳 | 其他科室 | 皮肤科 | 皮肤科 | 共和门诊、健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=428 |
| 330 | 宋燕平 | 宋燕平 | 其他科室 | 皮肤科 | 皮肤科 | 健康管理中心、共和门诊 | 医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=330 |
| 177 | 洪敏 | 洪敏 | 其他科室 | 中医科 | 中医科 | 健康管理中心 | 主任中医师、教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=177 |
| 178 | 章伟明 | 章伟明 | 其他科室 | 中医科 | 中医科 | 共和门诊、农林门诊 | 教授、主任中医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=178 |
| 195 | 甄毅锋 | 甄毅锋 | 其他科室 | 中医科 | 中医科 | 官网详情未标注 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=195 |
| 548 | 邓晶晶 | 邓晶晶 | 其他科室 | 中医科 | 中医科 | 健康管理中心 | 医学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=548 |
| 549 | 刘芳 | 刘芳 | 其他科室 | 中医科 | 中医科 | 共和门诊 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=549 |
| 564 | 蒋平平 | 蒋平平 | 其他科室 | 中医科 | 中医科 | 健康管理中心 | 副主任医师、医学博士、特聘副研究员、硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=564 |
| 565 | 赵玮璇 | 赵玮璇 | 其他科室 | 中医科 | 中医科 | 健康管理中心 | 医学博士，副主任中医师、特聘副研究员，讲师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=565 |
| 311 | 卢秉慧 | 卢秉慧 | 其他科室 | 中医科 | 中医科 | 健康管理中心 | 副主任中医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=311 |
| 313 | 王叶青 | 王叶青 | 其他科室 | 中医科 | 中医科 | 农林门诊、共和门诊 | 副主任中医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=313 |
| 315 | 叶龙霖 | 叶龙霖 | 其他科室 | 中医科 | 中医科 | 共和门诊、健康管理中心 | 医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=315 |
| 407 | 聂文强 | 聂文强 | 其他科室 | 中医科 | 中医科 | 健康管理中心 | 医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=407 |
| 463 | 廖锐 | 廖锐 | 其他科室 | 中医科 | 中医科 | 健康管理中心 | 医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=463 |
| 469 | 黎子毓 | 黎子毓 | 其他科室 | 中医科 | 中医科 | 共和门诊、健康管理中心 | 医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=469 |
| 174 | 张明兴 | 张明兴 | 其他科室 | 康复医学科 | 康复医学科 | 健康管理中心 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=174 |
| 173 | 黄旭明 | 黄旭明 | 其他科室 | 康复医学科 | 康复医学科 | 共和门诊、农林门诊 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=173 |
| 175 | 石艺华 | 石艺华 | 其他科室 | 康复医学科 | 康复医学科 | 健康管理中心 | 副教授、主任中医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=175 |
| 176 | 王秀坤 | 王秀坤 | 其他科室 | 康复医学科 | 康复医学科 | 官网详情未标注 | 副主任技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=176 |
| 552 | 张滨 | 张滨 | 其他科室 | 康复医学科 | 康复医学科 | 健康管理中心 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=552 |
| 553 | 单莎瑞 | 单莎瑞 | 其他科室 | 康复医学科 | 康复医学科 | 官网详情未标注 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=553 |
| 440 | 洪峰 | 洪峰 | 其他科室 | 康复医学科 | 康复医学科 | 官网详情未标注 | 医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=440 |
| 559 | 宋海泳 | 宋海泳 | 其他科室 | 康复医学科 | 康复医学科 | 健康管理中心 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=559 |
| 554 | 杨杏萍 | 杨杏萍 | 其他科室 | 康复医学科 | 康复医学科 | 农林门诊 | 中西医结合临床（七年制）硕士、康复医学与理疗学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=554 |
| 555 | 员凤英 | 员凤英 | 其他科室 | 康复医学科 | 康复医学科 | 健康管理中心 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=555 |
| 556 | 曾垂魁 | 曾垂魁 | 其他科室 | 康复医学科 | 康复医学科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=556 |
| 557 | 周礼 | 周礼 | 其他科室 | 康复医学科 | 康复医学科 | 官网详情未标注 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=557 |
| 24 | 王希成 | 王希成 | 其他科室 | 肿瘤一科 | 肿瘤一科 | 农林门诊 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=24 |
| 337 | 秦鑫添 | 秦鑫添 | 其他科室 | 肿瘤一科 | 肿瘤一科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=337 |
| 218 | 丁颖 | 丁颖 | 其他科室 | 肿瘤一科 | 肿瘤一科 | 农林门诊 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=218 |
| 254 | 杨帆 | 杨帆 | 其他科室 | 肿瘤一科 | 肿瘤一科 | 农林门诊 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=254 |
| 393 | 苏琼菲 | 苏琼菲 | 其他科室 | 肿瘤一科 | 肿瘤一科 | 官网详情未标注 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=393 |
| 430 | 张琼霞 | 张琼霞 | 其他科室 | 肿瘤一科 | 肿瘤一科 | 农林门诊 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=430 |
| 493 | 曹燕青 | 曹燕青 | 其他科室 | 肿瘤一科 | 肿瘤一科 | 农林门诊 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=493 |
| 596 | 王哲 | 王哲 | 其他科室 | 肿瘤一科 | 肿瘤一科 | 官网详情未标注 | 副主任医师，副教授，硕士研究生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=596 |
| 256 | 李玉齐 | 李玉齐 | 其他科室 | 肿瘤一科 | 肿瘤一科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=256 |
| 390 | 杨曙 | 杨曙 | 其他科室 | 肿瘤二科 | 肿瘤二科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=390 |
| 252 | 舒阳春 | 舒阳春 | 其他科室 | 肿瘤二科 | 肿瘤二科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=252 |
| 395 | 莫凯岚 | 莫凯岚 | 其他科室 | 肿瘤二科 | 肿瘤二科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=395 |
| 1 | 刘华 | 刘华 | 其他科室 | 全科医学科 | 全科医学科 | 健康管理中心 | 教授、主任医师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=1 |
| 143 | 徐丽梅 | 徐丽梅 | 其他科室 | 全科医学科 | 全科医学科 | 健康管理中心 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=143 |
| 142 | 王晓军 | 王晓军 | 其他科室 | 全科医学科 | 全科医学科 | 共和门诊 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=142 |
| 170 | 石雁 | 石雁 | 其他科室 | 全科医学科 | 全科医学科 | 共和门诊 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=170 |
| 155 | 陈艳波 | 陈艳波 | 其他科室 | 全科医学科 | 全科医学科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=155 |
| 194 | 郭雨青 | 郭雨青 | 其他科室 | 全科医学科 | 全科医学科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=194 |
| 408 | 张晓妹 | 张晓妹 | 其他科室 | 全科医学科 | 全科医学科 | 健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=408 |
| 584 | 李晓华 | 李晓华 | 其他科室 | 全科医学科 | 全科医学科 | 健康管理中心 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=584 |
| 19 | 劳志刚 | 劳志刚 | 其他科室 | 重症医学科 | 重症医学科 | 官网详情未标注 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=19 |
| 268 | 茹晃耀 | 茹晃耀 | 其他科室 | 重症医学科 | 重症医学科 | 官网详情未标注 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=268 |
| 270 | 王素宁 | 王素宁 | 其他科室 | 重症医学科 | 重症医学科 | 官网详情未标注 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=270 |
| 271 | 吴昊 | 吴昊 | 其他科室 | 重症医学科 | 重症医学科 | 官网详情未标注 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=271 |
| 475 | 陈建颜 | 陈建颜 | 其他科室 | 麻醉科 | 麻醉科 | 官网详情未标注 | 主任医师、教授 、博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=475 |
| 48 | 蔡杰衡 | 蔡杰衡 | 其他科室 | 麻醉科 | 麻醉科 | 官网详情未标注 | 教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=48 |
| 185 | 马翔 | 马翔 | 其他科室 | 麻醉科 | 麻醉科 | 官网详情未标注 | 副主任医师 、副教授 、麻醉学硕士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=185 |
| 187 | 陈志峰 | 陈志峰 | 其他科室 | 麻醉科 | 麻醉科 | 官网详情未标注 | 副主任医师 ，副教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=187 |
| 476 | 陈宗 | 陈宗 | 其他科室 | 麻醉科 | 麻醉科 | 官网详情未标注 | 副主任医师 /，副教授， 麻醉学硕士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=476 |
| 188 | 吴志镇 | 吴志镇 | 其他科室 | 麻醉科 | 麻醉科 | 官网详情未标注 | 主治医师 ， 麻醉学硕士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=188 |
| 477 | 李洁 | 李洁 | 其他科室 | 麻醉科 | 麻醉科 | 官网详情未标注 | 主治医师 、 麻醉学硕士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=477 |
| 321 | 苏一冬 | 苏一冬 | 其他科室 | 麻醉科 | 麻醉科 | 官网详情未标注 | 主治医师，麻醉学硕士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=321 |
| 607 | 周巧梅 | 周巧梅 | 其他科室 | 麻醉科 | 麻醉科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=607 |
| 253 | 陆崇 | 陆崇 | 其他科室 | 健康管理部 | 健康管理部 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=253 |
| 67 | 吴一平 | 吴一平 | 其他科室 | 健康管理部 | 健康管理部 | 官网详情未标注 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=67 |
| 232 | 梁葳 | 梁葳 | 其他科室 | 健康管理部 | 健康管理部 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=232 |
| 426 | 李远添 | 李远添 | 其他科室 | 静脉导管护理门诊 | 静脉导管护理门诊 | 农林门诊 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=426 |
| 603 | 李巧姬 | 李巧姬 | 其他科室 | 静脉导管护理门诊 | 静脉导管护理门诊 | 官网详情未标注 | 副主任护师，血液内科护士长/静疗专科组长 | available | 护理身份排除 | https://www.gy120.net/articleshow.asp?articleid=603 |
| 604 | 朱洁桃 | 朱洁桃 | 其他科室 | 静脉导管护理门诊 | 静脉导管护理门诊 | 官网详情未标注 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=604 |
| 378 | 张卫 | 张卫 | 其他科室 | 电生理专科门诊 | 电生理专科门诊 | 健康管理中心 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=378 |
| 150 | 郭煜 | 郭煜 | 医技 | 输血科 | 输血科 | 健康管理中心 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=150 |
| 171 | 吴红卫 | 吴红卫 | 医技 | 药学部 | 药学部 | 农林门诊 | 教授、主任药师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=171 |
| 133 | 陈吉生 | 陈吉生 | 医技 | 药学部 | 药学部 | 官网详情未标注 | 教授、主任药师、硕士生导师、 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=133 |
| 122 | 杨泽民 | 杨泽民 | 医技 | 药学部 | 药学部 | 官网详情未标注 | 教授、主任药师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=122 |
| 263 | 陈永 | 陈永 | 医技 | 药学部 | 药学部 | 农林门诊 | 教授、主任药师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=263 |
| 487 | 仇志坤 | 仇志坤 | 医技 | 药学部 | 药学部 | 官网详情未标注 | 副主任药师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=487 |
| 262 | 沈勇刚 | 沈勇刚 | 医技 | 药学部 | 药学部 | 官网详情未标注 | 副教授、主任药师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=262 |
| 239 | 袁少筠 | 袁少筠 | 医技 | 药学部 | 药学部 | 官网详情未标注 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=239 |
| 299 | 陈碧珊 | 陈碧珊 | 医技 | 药学部 | 药学部 | 农林门诊 | 副主任药师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=299 |
| 570 | 吴荣佳 | 吴荣佳 | 医技 | 药学部 | 药学部 | 官网详情未标注 | 副主任药师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=570 |
| 571 | 关石凤 | 关石凤 | 医技 | 药学部 | 药学部 | 官网详情未标注 | 副主任中药房 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=571 |
| 300 | 赖莎 | 赖莎 | 医技 | 药学部 | 药学部 | 农林门诊 | 副主任药师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=300 |
| 572 | 陈慧 | 陈慧 | 医技 | 药学部 | 药学部 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=572 |
| 301 | 李艳 | 李艳 | 医技 | 药学部 | 药学部 | 农林门诊 | 主管药师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=301 |
| 242 | 马立恒 | 马立恒 | 医技 | 医学影像科 | 医学影像科 | 农林门诊 | 教授、主任医师、博士、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=242 |
| 225 | 曾文彦 | 曾文彦 | 医技 | 医学影像科 | 医学影像科 | 农林门诊 | 副主任医师、副教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=225 |
| 226 | 庄娘妥 | 庄娘妥 | 医技 | 医学影像科 | 医学影像科 | 官网详情未标注 | 副主任医师，副教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=226 |
| 240 | 杨清华 | 杨清华 | 医技 | 医学影像科 | 医学影像科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=240 |
| 389 | 罗武 | 罗武 | 医技 | 医学影像科 | 医学影像科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=389 |
| 592 | 李琼华 | 李琼华 | 医技 | 医学影像科 | 医学影像科 | 官网详情未标注 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=592 |
| 42 | 丁彩屏 | 丁彩屏 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=42 |
| 351 | 杨小蓉 | 杨小蓉 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 主任技师、副教授、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=351 |
| 537 | 李瑞莹 | 李瑞莹 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师、副教授 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=537 |
| 538 | 刘思敏 | 刘思敏 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=538 |
| 539 | 卢汉威 | 卢汉威 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师、副教授、临床基础检验教研室主任 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=539 |
| 540 | 卢景辉 | 卢景辉 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师、副教授、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=540 |
| 541 | 马晓桂 | 马晓桂 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师、副教授、医学检验系临床免疫检验教研室主任 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=541 |
| 542 | 张涛 | 张涛 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师、副教授、生化大组组长 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=542 |
| 562 | 徐晓松 | 徐晓松 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=562 |
| 543 | 黄演婷 | 黄演婷 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=543 |
| 544 | 秦建川 | 秦建川 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=544 |
| 563 | 官煜彬 | 官煜彬 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师、检验科体液室组长 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=563 |
| 353 | 钟亮尹 | 钟亮尹 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=353 |
| 348 | 陈林珍 | 陈林珍 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 主管技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=348 |
| 350 | 冯红梅 | 冯红梅 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=350 |
| 352 | 余佩芝 | 余佩芝 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 主管技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=352 |
| 349 | 陈少莲 | 陈少莲 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 副主任技师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=349 |
| 190 | 杨宁 | 杨宁 | 医技 | 病理科 | 病理科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=190 |
| 600 | 潘斌才 | 潘斌才 | 医技 | 病理科 | 病理科 | 官网详情未标注 | 病理学主任医师、岭南名医 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=600 |
| 191 | 李红 | 李红 | 医技 | 病理科 | 病理科 | 农林门诊 | 副教授、副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=191 |
| 601 | 宋玉兰 | 宋玉兰 | 医技 | 病理科 | 病理科 | 官网详情未标注 | 无 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=601 |
| 361 | 杨焰 | 杨焰 | 医技 | 物检科 | 物检科 | 官网详情未标注 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=361 |
| 362 | 黄密伶 | 黄密伶 | 医技 | 物检科 | 物检科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=362 |
| 593 | 周玉婷 | 周玉婷 | 医技 | 物检科 | 物检科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=593 |
| 594 | 余瑾 | 余瑾 | 医技 | 物检科 | 物检科 | 官网详情未标注 | 心电学副主任医师、医学硕士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=594 |
| 356 | 陈虹 | 陈虹 | 医技 | 物检科 | 物检科 | 官网详情未标注 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=356 |
| 358 | 金文敏 | 金文敏 | 医技 | 物检科 | 物检科 | 官网详情未标注 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=358 |
| 359 | 钟华 | 钟华 | 医技 | 物检科 | 物检科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=359 |
| 360 | 严冬梅 | 严冬梅 | 医技 | 物检科 | 物检科 | 官网详情未标注 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=360 |
| 484 | 沈建红 | 沈建红 | 医技 | 物检科 | 物检科 | 官网详情未标注 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=484 |
| 258 | 赵泳谊 | 赵泳谊 | 医技 | 临床营养科 | 临床营养科 | 健康管理中心 | 副教授、主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=258 |
| 589 | 林伟群 | 林伟群 | 医技 | 临床营养科 | 临床营养科 | 健康管理中心 | 副主任医师、医学博士 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=589 |
| 259 | 刘翠冰 | 刘翠冰 | 医技 | 临床营养科 | 临床营养科 | 官网详情未标注 | 营养师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=259 |
| 260 | 欧俏文 | 欧俏文 | 医技 | 临床营养科 | 临床营养科 | 健康管理中心 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=260 |
| 345 | 袁建伟 | 袁建伟 | 医技 | 核医学科 | 核医学科 | 农林门诊 | 教授、主任医师、硕士生导师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=345 |
| 272 | 刘雄英 | 刘雄英 | 医技 | 核医学科 | 核医学科 | 农林门诊 | 副主任医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=272 |
| 273 | 陈桐生 | 陈桐生 | 医技 | 核医学科 | 核医学科 | 农林门诊 | 主治医师 | available | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=273 |

### 纯护理身份逐 ID 排除表

| ArticleID | 姓名 | 官网详情职称 | 列表科室 | 排除理由 | 来源链接 |
|---|---|---|---|---|---|
| 404 | 何淑敏 | 护师，国际造口治疗师 | 伤口造口治疗室 | 官网详情专业职称明确为纯护理身份，按医生画像范围排除 | https://www.gy120.net/articleshow.asp?articleid=404 |
| 603 | 李巧姬 | 副主任护师，血液内科护士长/静疗专科组长 | 静脉导管护理门诊 | 官网详情专业职称明确为纯护理身份，按医生画像范围排除 | https://www.gy120.net/articleshow.asp?articleid=603 |

### 同名身份聚类与主详情裁决

| 姓名 | ArticleID | 裁决 | 详情关系 | 合并科室/出诊点 | 主详情 ID | 主详情来源 |
|---|---|---|---:|---|---|---|
| 周万兴 | 75,505 | 同一官方照片归并 | 2 | 心内一科（健康管理中心）、心内二科（健康管理中心） | 75 | https://www.gy120.net/articleshow.asp?articleid=75 |
| 张卫 | 138 | 同名待甄别 | 1 | 心内二科（健康管理中心） | 138 | https://www.gy120.net/articleshow.asp?articleid=138 |
| 张卫 | 378 | 同名待甄别 | 1 | 电生理专科门诊（健康管理中心） | 378 | https://www.gy120.net/articleshow.asp?articleid=378 |
| 郭煜 | 379 | 同名待甄别 | 1 | 血液内科（健康管理中心） | 379 | https://www.gy120.net/articleshow.asp?articleid=379 |
| 郭煜 | 150 | 同名待甄别 | 1 | 输血科（健康管理中心） | 150 | https://www.gy120.net/articleshow.asp?articleid=150 |
| 余炯标 | 245 | 同名待甄别 | 1 | 普外一科（肝胆外科）（农林门诊） | 245 | https://www.gy120.net/articleshow.asp?articleid=245 |
| 余炯标 | 614 | 同名待甄别 | 1 | 足踝与创面修复科（骨四科）（农林门诊） | 614 | https://www.gy120.net/articleshow.asp?articleid=614 |
| 张滨 | 507 | 同名待甄别 | 1 | 泌尿外科（健康管理中心） | 507 | https://www.gy120.net/articleshow.asp?articleid=507 |
| 张滨 | 552 | 同名待甄别 | 1 | 康复医学科（健康管理中心） | 552 | https://www.gy120.net/articleshow.asp?articleid=552 |
| 林强 | 576,510,577,578 | 同名待甄别 | 4 | 创伤与关节外科（骨一科）（健康管理中心）、脊柱外科（骨二科）（健康管理中心）、运动医学科（骨三科）（健康管理中心）、正骨科（健康管理中心） | 576 | https://www.gy120.net/articleshow.asp?articleid=576 |
| 林强 | 611 | 同名待甄别 | 1 | 足踝与创面修复科（骨四科）（健康管理中心） | 611 | https://www.gy120.net/articleshow.asp?articleid=611 |
| 董群伟 | 579,141,580,581 | 同名待甄别 | 4 | 创伤与关节外科（骨一科）（农林门诊）、脊柱外科（骨二科）（农林门诊）、运动医学科（骨三科）（农林门诊）、正骨科（农林门诊） | 579 | https://www.gy120.net/articleshow.asp?articleid=579 |
| 董群伟 | 612 | 同名待甄别 | 1 | 足踝与创面修复科（骨四科）（农林门诊） | 612 | https://www.gy120.net/articleshow.asp?articleid=612 |
| 王华 | 161 | 同名待甄别 | 1 | 创伤与关节外科（骨一科）（健康管理中心） | 161 | https://www.gy120.net/articleshow.asp?articleid=161 |
| 王华 | 526 | 同名待甄别 | 1 | 运动医学科（骨三科）（健康管理中心） | 526 | https://www.gy120.net/articleshow.asp?articleid=526 |

### 全量采集照片字节、魔数、SHA-256、尺寸及重试对账

| 姓名 | ArticleID | 科室 | 主职称 | 文件名 | 字节数 | 宽×高 | SHA-256 | 重试次数 | 官网照片 |
|---|---|---|---|---|---:|---:|---|---:|---|
| 林忠伟 | 370 | 心内一科 | 主任医师 | 林忠伟-心内一科-主任医师-广东药科大学附属第一医院.jpg | 395298 | 658×987 | `54518c7ef680d927d00ef34a68d59f26ce8f383ed054539223e88d266f664c12` | 0 | https://www.gy120.net/files/20180104120805720.JPG |
| 周万兴 | 75 | 心内一科 | 主任医师 | 周万兴-心内一科-主任医师-广东药科大学附属第一医院.jpg | 350856 | 1507×2010 | `a1d4aead3d2f2b0b661898109787272b9832977879e5b1845cba15de24f402c2` | 0 | https://www.gy120.net/files/20180104110230278.jpg |
| 雷达 | 72 | 心内一科 | 主任医师 | 雷达-心内一科-主任医师-广东药科大学附属第一医院.jpg | 212028 | 415×622 | `bcc2f67338b8db6a3ba8920b7609dc66eb5936cb77236ebd6a85fa40f05945be` | 0 | https://www.gy120.net/files/20180104120715637.JPG |
| 朱桂平 | 119 | 心内一科 | 主任医师 | 朱桂平-心内一科-主任医师-广东药科大学附属第一医院.jpg | 401308 | 650×975 | `ff02d2b2f8b6460fb0ebbeff4180d78f80eb9225c189553104ab5de36808edde` | 0 | https://www.gy120.net/files/20180104120928691.JPG |
| 李国标 | 107 | 心内一科 | 主任医师 | 李国标-心内一科-主任医师-广东药科大学附属第一医院.jpg | 519462 | 706×1059 | `89a25d988fc3f67cdf273caeea9cbc4590046602535ddbe7487d7935c9b4d1db` | 0 | https://www.gy120.net/files/20180104120732096.JPG |
| 韩彬 | 500 | 心内一科 | 未标注 | 韩彬-心内一科-未标注-广东药科大学附属第一医院.jpg | 2584 | 119×174 | `e96302a866e89bbef91a865e465158d325d9528e1046ee0e5c83b179d66b774e` | 0 | https://www.gy120.net/files/20230112210956665.jpg |
| 曾智桓 | 139 | 心内二科 | 主任医师 | 曾智桓-心内二科-主任医师-广东药科大学附属第一医院.jpg | 489760 | 715×1072 | `dd7b918d5481478d92076bbf1a915c8aa560a28cd24e2a378bd4b7b9e1fdabba` | 0 | https://www.gy120.net/files/20180104120656967.JPG |
| 张莉 | 229 | 心内二科 | 副主任医师 | 张莉-心内二科-副主任医师-广东药科大学附属第一医院.jpg | 424158 | 609×913 | `9fc875f363ce6a4c6a049dc67f1e79e9b2eef975f7f2331d2180946de19ed05b` | 0 | https://www.gy120.net/files/20180104120828928.JPG |
| 张卫 | 138 | 心内二科 | 主任医师 | 张卫-心内二科-主任医师-广东药科大学附属第一医院.jpg | 480726 | 660×990 | `84b1dbc0e6bd6455d3d4eac88550100275cca03f0728620ee2551356d0c71526` | 0 | https://www.gy120.net/files/20180104120909407.JPG |
| 张卫 | 378 | 电生理专科门诊 | 主任医师 | 张卫-电生理专科门诊-主任医师-广东药科大学附属第一医院.jpg | 480726 | 660×990 | `84b1dbc0e6bd6455d3d4eac88550100275cca03f0728620ee2551356d0c71526` | 0 | https://www.gy120.net/files/20180104120854924.JPG |
| 郑坚奕 | 497 | 心内二科 | 副主任医师 | 郑坚奕-心内二科-副主任医师-广东药科大学附属第一医院.jpg | 1516426 | 1654×2362 | `d323a7d1666df4e8c2beb9d1c4c5ce45bb72a7b8ff7c4c6f3d6ffb55411ee8c9` | 0 | https://www.gy120.net/files/20240831081452128.JPG |
| 王宗涛 | 498 | 心内二科 | 未标注 | 王宗涛-心内二科-未标注-广东药科大学附属第一医院.jpg | 2584 | 119×174 | `e96302a866e89bbef91a865e465158d325d9528e1046ee0e5c83b179d66b774e` | 0 | https://www.gy120.net/files/20230112210956665.jpg |
| 潘学谊 | 76 | 血液内科 | 主任医师 | 潘学谊-血液内科-主任医师-广东药科大学附属第一医院.jpg | 365700 | 610×915 | `fddf227560f2119ee2e3c0a82e9ab5734177b177fe0638d1b8f5801fd7c44a90` | 0 | https://www.gy120.net/files/20200228111554274.jpg |
| 关则兵 | 340 | 血液内科 | 副主任医师 | 关则兵-血液内科-副主任医师-广东药科大学附属第一医院.jpg | 393522 | 648×972 | `984889ad349b3eb9306c9c4280c451ffc918de4a6696aecc7abc0fbcdbbe67da` | 0 | https://www.gy120.net/files/20180104121045767.JPG |
| 叶美莲 | 115 | 血液内科 | 主任医师 | 叶美莲-血液内科-主任医师-广东药科大学附属第一医院.jpg | 1277038 | 1645×2467 | `200b2f9390cd4d35f0150b69ba1c95fdfb1371ebddd5e01223936783b5cb90dc` | 0 | https://www.gy120.net/files/20180104124306593.jpg |
| 迟作华 | 341 | 血液内科 | 副主任医师 | 迟作华-血液内科-副主任医师-广东药科大学附属第一医院.jpg | 63092 | 409×614 | `f087e31d7f254b8df7743d44dab5e1b86a6d300ee05ca2d5df2798d3525abced` | 0 | https://www.gy120.net/files/20200114152700940.jpg |
| 郭煜 | 379 | 血液内科 | 副主任医师 | 郭煜-血液内科-副主任医师-广东药科大学附属第一医院.jpg | 584622 | 684×1026 | `b1c84efefa8a845ee13b74aa784268bf591fc3fd2bf48425ccfdd361390e0a88` | 0 | https://www.gy120.net/files/20180104120101408.JPG |
| 郭煜 | 150 | 输血科 | 副主任医师 | 郭煜-输血科-副主任医师-广东药科大学附属第一医院.jpg | 584622 | 684×1026 | `b1c84efefa8a845ee13b74aa784268bf591fc3fd2bf48425ccfdd361390e0a88` | 0 | https://www.gy120.net/files/20180104120116608.JPG |
| 周兰兰 | 547 | 血液内科 | 副主任医师 | 周兰兰-血液内科-副主任医师-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260423204121866.jpg |
| 曾文彬 | 380 | 血液内科 | 主治医师 | 曾文彬-血液内科-主治医师-广东药科大学附属第一医院.jpg | 29142 | 117×175 | `c7ce75f4adef194d770611743f5c76a9ddff2008a467453d8bc9168ea856306e` | 0 | https://www.gy120.net/files/20180718151433122.jpg |
| 袁伟锋 | 40 | 呼吸与危重症医学科 | 主任医师 | 袁伟锋-呼吸与危重症医学科-主任医师-广东药科大学附属第一医院.jpg | 18414 | 170×227 | `1aebca1aed82d83f7645ca2ffa7f79ad629d42f9c925f80aa51371559d394b26` | 0 | https://www.gy120.net/files/20240830083641469.jpg |
| 王虹 | 222 | 呼吸与危重症医学科 | 副主任医师 | 王虹-呼吸与危重症医学科-副主任医师-广东药科大学附属第一医院.jpg | 474552 | 664×996 | `d7f6a4405194ce32093ff336d62b4717450465c091f0e4392b782e47b4235c29` | 0 | https://www.gy120.net/files/20180104113148588.JPG |
| 关向群 | 223 | 呼吸与危重症医学科 | 副主任医师 | 关向群-呼吸与危重症医学科-副主任医师-广东药科大学附属第一医院.jpg | 520922 | 686×1029 | `ed40c7f90c7b1252769a89bcaed790ad80e69b197d7d5182b68dc9aef94357a0` | 0 | https://www.gy120.net/files/20180104113052941.JPG |
| 毛锐 | 416 | 呼吸与危重症医学科 | 副主任医师 | 毛锐-呼吸与危重症医学科-副主任医师-广东药科大学附属第一医院.jpg | 1132578 | 1200×1800 | `af4e403fe9e6c6a8a78011696b14633a83bed8c501ce36ae1a28e3e271fc7a8a` | 0 | https://www.gy120.net/files/20170808090455757.JPG |
| 崔莉 | 567 | 呼吸与危重症医学科 | 未标注 | 崔莉-呼吸与危重症医学科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 邢秋云 | 574 | 呼吸与危重症医学科 | 副主任医师 | 邢秋云-呼吸与危重症医学科-副主任医师-广东药科大学附属第一医院.jpg | 17844 | 250×350 | `aa9bae1e1d1d17c6db091f577cf507efd9b8be1d74742ba7ebbb232ffe57b944` | 0 | https://www.gy120.net/files/20260511205022741.JPG |
| 张少卿 | 568 | 呼吸与危重症医学科 | 未标注 | 张少卿-呼吸与危重症医学科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 李兰英 | 357 | 呼吸与危重症医学科 | 副主任医师 | 李兰英-呼吸与危重症医学科-副主任医师-广东药科大学附属第一医院.jpg | 453918 | 626×938 | `438fd6dbee2d70c2bf733321c149fa906954f94e0bb313c92b24afa42bbbb1b2` | 0 | https://www.gy120.net/files/20180104113128283.JPG |
| 吕路 | 209 | 肾内科 | 主任医师 | 吕路-肾内科-主任医师-广东药科大学附属第一医院.jpg | 379258 | 663×995 | `04fe02e4bb76e38e2e2a41f13051702bca1dca21a88b973e7d8645cfe9f36e82` | 0 | https://www.gy120.net/files/20180104120031498.JPG |
| 蒋文功 | 121 | 肾内科 | 主任医师 | 蒋文功-肾内科-主任医师-广东药科大学附属第一医院.jpg | 603628 | 718×1077 | `e2c5ad89f4906cd036db8d76437cf61abe6fdb8ec218a26ba552a939061f238d` | 0 | https://www.gy120.net/files/20180104120010627.JPG |
| 黄培华 | 157 | 肾内科 | 副主任医师 | 黄培华-肾内科-副主任医师-广东药科大学附属第一医院.jpg | 415988 | 649×973 | `60fa9fb746ba505c48f650eb214566c823c8e264c12877d8234c2d5f162d9d98` | 0 | https://www.gy120.net/files/20180104115817678.JPG |
| 杨天开 | 569 | 肾内科 | 未标注 | 杨天开-肾内科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 桓文穆 | 61 | 肾内科 | 副主任医师 | 桓文穆-肾内科-副主任医师-广东药科大学附属第一医院.jpg | 354418 | 636×954 | `17e300471df26f04f2c9bdc27a2504ff924317128be5486d9ed2ba8deac63b4a` | 0 | https://www.gy120.net/files/20180104115604573.JPG |
| 黄华 | 62 | 肾内科 | 副主任医师 | 黄华-肾内科-副主任医师-广东药科大学附属第一医院.jpg | 348144 | 634×951 | `6cb3fa649c7b90337a0d0209bfd393fb572301a41bcb0cd9696cbbfc5de6a894` | 0 | https://www.gy120.net/files/20180104115756238.JPG |
| 叶健华 | 53 | 内分泌科 | 主任医师 | 叶健华-内分泌科-主任医师-广东药科大学附属第一医院.jpg | 255646 | 478×716 | `46860b2b716d6aef838c629cf4adf6a7736dfcbee79cfab6e8d65b0bad280cc0` | 0 | https://www.gy120.net/files/20180104114120442.JPG |
| 周昭远 | 54 | 内分泌科 | 副主任医师 | 周昭远-内分泌科-副主任医师-广东药科大学附属第一医院.jpg | 509834 | 659×988 | `ec4891159332194eff6b1fc8eb115ad1a93b02b2a3ad3c25997e68b08a159990` | 0 | https://www.gy120.net/files/20180104113850689.JPG |
| 孙平 | 354 | 内分泌科 | 副主任医师 | 孙平-内分泌科-副主任医师-广东药科大学附属第一医院.jpg | 1128098 | 1200×1800 | `7d0dfec23095f0ca54f57f2cd3ff8491f6073827923bc2c7b838ef1f6b659f7a` | 0 | https://www.gy120.net/files/20150729145423807.JPG |
| 马承红 | 204 | 内分泌科 | 副主任医师 | 马承红-内分泌科-副主任医师-广东药科大学附属第一医院.jpg | 368884 | 598×897 | `8b1cc380fd6c3202732f3a372b5753d669708f67260814cdbbb5b0f32d6c3c34` | 0 | https://www.gy120.net/files/20180104114136399.JPG |
| 胡丽 | 327 | 内分泌科 | 住院医师 | 胡丽-内分泌科-住院医师-广东药科大学附属第一医院.jpg | 24732 | 117×175 | `cee0373eee25e97104fca8a13c8778bc6a3e190382f05bf3e9e6c294e63a1cf6` | 0 | https://www.gy120.net/files/20180718153341145.jpg |
| 廖瘳 | 205 | 内分泌科 | 主治医师 | 廖瘳-内分泌科-主治医师-广东药科大学附属第一医院.jpg | 50070 | 160×240 | `2ad6980fe5f36633321307838a1ba8f735b94fb987497fcca9e5267aa1a9554a` | 0 | https://www.gy120.net/files/20130922114954888.JPG |
| 刘楠 | 328 | 内分泌科 | 住院医师 | 刘楠-内分泌科-住院医师-广东药科大学附属第一医院.jpg | 28080 | 117×175 | `ef1af5d0c5cdbf122c85cfde39bfc3fb8b4b1d0782717fad9f3b28e64ba4d66f` | 0 | https://www.gy120.net/files/20180718153403520.jpg |
| 莫旭旭 | 329 | 内分泌科 | 住院医师 | 莫旭旭-内分泌科-住院医师-广东药科大学附属第一医院.jpg | 24174 | 117×167 | `c3db84d1a9a13181ad4c87bc3327464d47c04916b13e7370f731038a84a66864` | 0 | https://www.gy120.net/files/20180718153421362.jpg |
| 何兴祥 | 156 | 消化内科 | 主任医师 | 何兴祥-消化内科-主任医师-广东药科大学附属第一医院.jpg | 692572 | 1473×1964 | `f84f1be675b71c326eade53bf4c3de259ddf6e573bf825044bb2b3b0a757c560` | 0 | https://www.gy120.net/files/20180122104317435.jpg |
| 吴礼浩 | 212 | 消化内科 | 主任医师 | 吴礼浩-消化内科-主任医师-广东药科大学附属第一医院.jpg | 380168 | 661×991 | `627907e014b9c67cb06c5a1d2e41cc9a797c4707a1cfcb1c94563a0063c7282c` | 0 | https://www.gy120.net/files/20180104120304023.JPG |
| 邝小枫 | 66 | 消化内科 | 主任医师 | 邝小枫-消化内科-主任医师-广东药科大学附属第一医院.jpg | 348662 | 617×926 | `a75e5d45afec1b2f834ae587393efae757eeb1268c8d64d423601f57d2bc77a8` | 0 | https://www.gy120.net/files/20180104120245176.JPG |
| 钱国强 | 453 | 消化内科 | 主任医师 | 钱国强-消化内科-主任医师-广东药科大学附属第一医院.jpg | 30168 | 119×170 | `28788efde8cf871be7ec92230455a0ead5b26aad903d33fa161b4c985ae0f7c4` | 0 | https://www.gy120.net/files/20190514095400375.jpg |
| 谢文瑞 | 214 | 消化内科 | 主任医师 | 谢文瑞-消化内科-主任医师-广东药科大学附属第一医院.jpg | 404464 | 662×993 | `16600647cdfb19614cf38b78b22aff1a5133462a3ee178f56b2b6c8b2977793a` | 0 | https://www.gy120.net/files/20180104120322356.JPG |
| 袁瑜 | 211 | 消化内科 | 副主任医师 | 袁瑜-消化内科-副主任医师-广东药科大学附属第一医院.jpg | 412152 | 657×985 | `4ad8b44f3be6975276bb0b1db5ac2c1f9322a946f561ba66f16c53ff19289572` | 0 | https://www.gy120.net/files/20180104120344290.JPG |
| 蔡洁毅 | 210 | 消化内科 | 副主任医师 | 蔡洁毅-消化内科-副主任医师-广东药科大学附属第一医院.jpg | 381548 | 644×966 | `97cadb919e0826502482e3317b3e416b54e9f274ec43b0a486c45c48b655c0ed` | 0 | https://www.gy120.net/files/20180104120222653.JPG |
| 林绍强 | 441 | 消化内科 | 教授 | 林绍强-消化内科-教授-广东药科大学附属第一医院.jpg | 43578 | 390×567 | `0af18c3cccda460820864d41628544c641c7a7c941201d82c3e7b524addae28c` | 0 | https://www.gy120.net/files/20181207101943621.jpg |
| 秦治初 | 566 | 消化内科 | 未标注 | 秦治初-消化内科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 李兰 | 293 | 消化内科 | 主治医师 | 李兰-消化内科-主治医师-广东药科大学附属第一医院.jpg | 27586 | 117×156 | `eef3ecadf345ae6fe33d5624b3d1b8cdae5a7c613c9981a9f97b315c9b084865` | 0 | https://www.gy120.net/files/20180718154403481.jpg |
| 罗丹萍 | 294 | 消化内科 | 住院医师 | 罗丹萍-消化内科-住院医师-广东药科大学附属第一医院.jpg | 23172 | 117×175 | `cd11b860a1f7153214a10d2e2cc3157f5e89b4e2fddbdc27d5f47a6949162b93` | 0 | https://www.gy120.net/files/20180718154422258.jpg |
| 周慧敏 | 296 | 消化内科 | 住院医师 | 周慧敏-消化内科-住院医师-广东药科大学附属第一医院.jpg | 26160 | 117×170 | `a31ab288364b52dda05b8f7bd0209752bf006c3dd2b815b27a334306e4a66c54` | 0 | https://www.gy120.net/files/20180718154451972.jpg |
| 梁芬芬 | 292 | 消化内科 | 住院医师 | 梁芬芬-消化内科-住院医师-广东药科大学附属第一医院.jpg | 24302 | 117×168 | `26b2be19d29b4264fc149f6f1e5e3982daf899f94584605926e31121a0679e87` | 0 | https://www.gy120.net/files/20180718154343936.jpg |
| 肖文豪 | 257 | 风湿免疫科 | 副主任医师 | 肖文豪-风湿免疫科-副主任医师-广东药科大学附属第一医院.jpg | 41074 | 300×429 | `707d86850a8a5fb3a41a60d7819aaf85fadd87fbc6288c844cbc4c16fcd8867e` | 0 | https://www.gy120.net/files/20240830165913114.jpg |
| 孙慧琳 | 230 | 肥胖专病治疗组 | 主任医师 | 孙慧琳-肥胖专病治疗组-主任医师-广东药科大学附属第一医院.jpg | 1734432 | 1335×2002 | `757fdec9eb40a4b5f9fc2fa6bd175dadb91787a8e332e5679c53eeaca8906a6f` | 0 | https://www.gy120.net/files/20180104113746126.JPG |
| 区奕猛 | 7 | 普外一科（肝胆外科） | 主任医师 | 区奕猛-普外一科（肝胆外科）-主任医师-广东药科大学附属第一医院.jpg | 234226 | 458×687 | `9047d6a43b420ed195e0fd0b47dce5317792e9fc974e1cd46d2f4583948bc3d7` | 0 | https://www.gy120.net/files/20190917091728518.JPG |
| 连福珍 | 8 | 普外一科（肝胆外科） | 副主任医师 | 连福珍-普外一科（肝胆外科）-副主任医师-广东药科大学附属第一医院.jpg | 236202 | 449×674 | `565e9d8c21931cdbe0bf10c460c30e1349017cc65ef2375d399766646ec95d2d` | 0 | https://www.gy120.net/files/20180104114258901.JPG |
| 罗永平 | 243 | 普外一科（肝胆外科） | 主任医师 | 罗永平-普外一科（肝胆外科）-主任医师-广东药科大学附属第一医院.jpg | 306922 | 522×783 | `bfcdf8a1377885e672ff0b60f3aa259e0b7a121ecdae654adf23077b52f2ca1c` | 0 | https://www.gy120.net/files/20180104114337004.JPG |
| 马兴标 | 179 | 普外一科（肝胆外科） | 副主任医师 | 马兴标-普外一科（肝胆外科）-副主任医师-广东药科大学附属第一医院.jpg | 544230 | 654×981 | `4f545a39ff3ddc894b28cedeb40dd966138bd09f541d4ff70c656049d45a236e` | 0 | https://www.gy120.net/files/20180104114538455.JPG |
| 余炯标 | 245 | 普外一科（肝胆外科） | 主治医师 | 余炯标-普外一科（肝胆外科）-主治医师-广东药科大学附属第一医院.jpg | 54752 | 166×249 | `456b84e9eb61cebe4d1480c283c128c7af88505bcb1100d27cd7bbc1d3832937` | 0 | https://www.gy120.net/files/20140928100409222.JPG |
| 余炯标 | 614 | 足踝与创面修复科（骨四科） | 副主任医师 | 余炯标-足踝与创面修复科（骨四科）-副主任医师-广东药科大学附属第一医院.jpg | 25246 | 250×358 | `5a5e9a979cdb3e2a360b39e35a58646d2dd4e2cdf8f1b720659a2dbf0bf01ab1` | 0 | https://www.gy120.net/files/20260720135827914.jpg |
| 黄树圭 | 275 | 普外一科（肝胆外科） | 副主任医师 | 黄树圭-普外一科（肝胆外科）-副主任医师-广东药科大学附属第一医院.jpg | 56456 | 250×350 | `a5d2f6c6fb0b34c66707cd739709ee442e3bdac9ed51de57fa6c7fa774273cf7` | 0 | https://www.gy120.net/files/20260514204645360.JPG |
| 张伟斌 | 16 | 普外二科（胃肠外科） | 主任医师 | 张伟斌-普外二科（胃肠外科）-主任医师-广东药科大学附属第一医院.jpg | 662402 | 1034×1551 | `707ab7fd673266c42a68ff2d0a5752d43ae65d02e3c439eef1efde3107164156` | 0 | https://www.gy120.net/files/20180104124413714.jpg |
| 吴敏华 | 15 | 普外二科（胃肠外科） | 副主任医师 | 吴敏华-普外二科（胃肠外科）-副主任医师-广东药科大学附属第一医院.jpg | 245308 | 464×697 | `cbd2ede899033b260c3bd83af1a1d6626869b263bb0dc932c4ebc430a093dabf` | 0 | https://www.gy120.net/files/20180104114227043.JPG |
| 陈丹 | 413 | 普外二科（胃肠外科） | 副主任医师 | 陈丹-普外二科（胃肠外科）-副主任医师-广东药科大学附属第一医院.jpg | 1112750 | 1200×1800 | `78544b4485db92272cdd953565fe57c0cd5f1d26c743058051446f7966e21747` | 0 | https://www.gy120.net/files/20170803154822524.JPG |
| 李平 | 236 | 普外三科（整形美容科） | 副主任医师 | 李平-普外三科（整形美容科）-副主任医师-广东药科大学附属第一医院.jpg | 433622 | 631×946 | `c4e12a778c0fc4207e77e814aa645cfb56c8a3385ccd31882e2ff00766381df7` | 0 | https://www.gy120.net/files/20180104122729402.JPG |
| 惠俐 | 172 | 普外三科（整形美容科） | 主任医师 | 惠俐-普外三科（整形美容科）-主任医师-广东药科大学附属第一医院.jpg | 377178 | 598×899 | `cd926ebd91f905c8835516c07cf625fece4478b3118814ef2ca184dd0d5c4841` | 0 | https://www.gy120.net/files/20180104122752431.JPG |
| 陈元良 | 237 | 普外三科（整形美容科） | 副主任医师 | 陈元良-普外三科（整形美容科）-副主任医师-广东药科大学附属第一医院.jpg | 474708 | 653×980 | `652fa115caf9dc1f8cf64ced54437e475ddef776e1d40939f66682dbe2ebbb79` | 0 | https://www.gy120.net/files/20180104122644813.JPG |
| 赵欣欣 | 238 | 普外三科（整形美容科） | 副主任医师 | 赵欣欣-普外三科（整形美容科）-副主任医师-广东药科大学附属第一医院.jpg | 51016 | 648×972 | `8185e4c23918eacd2519786632b5dd6b797ee4e6cc1353d884b1184b498fdd5a` | 0 | https://www.gy120.net/files/20180104122702898.JPG |
| 余文林 | 590 | 普外三科（整形美容科） | 副主任医师 | 余文林-普外三科（整形美容科）-副主任医师-广东药科大学附属第一医院.jpg | 10648 | 250×281 | `ef2d6e0ae41dc6afc1038a6854aac2531483e53a49d5b6508f4eca1a291a1290` | 0 | https://www.gy120.net/files/20260517165244239.jpg |
| 刘志刚 | 591 | 普外三科（整形美容科） | 副主任医师 | 刘志刚-普外三科（整形美容科）-副主任医师-广东药科大学附属第一医院.png | 124958 | 250×350 | `46c77fd02d3eeed2c8b72b0c2d9fbd70d51122631ba9110dde1fccd3fce9f9d2` | 0 | https://www.gy120.net/files/20260517165559123.png |
| 郑祥光 | 377 | 泌尿外科 | 主任医师 | 郑祥光-泌尿外科-主任医师-广东药科大学附属第一医院.jpg | 659564 | 801×1201 | `06f9bd40879e183c1bd1baae16cb83482591fc59c3af5ea9773a064c5a7349d4` | 0 | https://www.gy120.net/files/20180104114038631.JPG |
| 罗力 | 51 | 泌尿外科 | 主任医师 | 罗力-泌尿外科-主任医师-广东药科大学附属第一医院.jpg | 550854 | 691×1036 | `8a40878e48c4e31530ecc44f25854ca6440b777b55174f48de1972f7e82156b6` | 0 | https://www.gy120.net/files/20180104113938126.JPG |
| 王玺坤 | 159 | 泌尿外科 | 主任医师 | 王玺坤-泌尿外科-主任医师-广东药科大学附属第一医院.jpg | 459398 | 647×971 | `438aa06fa15777e312e1b35fd2e8733941b81c2d9ce5f551806b4d59fee3a56e` | 0 | https://www.gy120.net/files/20180104114015114.JPG |
| 陈三三 | 546 | 泌尿外科 | 副主任医师 | 陈三三-泌尿外科-副主任医师-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260423204121866.jpg |
| 李峻 | 200 | 泌尿外科 | 副主任医师 | 李峻-泌尿外科-副主任医师-广东药科大学附属第一医院.jpg | 596042 | 714×1072 | `eae4f0ea90bdbd43115e4b60608445510ba9cc0a720e67f14deb596541713633` | 0 | https://www.gy120.net/files/20180104113916937.JPG |
| 王森 | 201 | 泌尿外科 | 副主任医师 | 王森-泌尿外科-副主任医师-广东药科大学附属第一医院.jpg | 37440 | 533×800 | `0bec5bffae01adb6354edb61e050feb3a0db5fc994a06d48e32028e17c2bd68b` | 0 | https://www.gy120.net/files/20230609160738886.jpg |
| 钱聚标 | 160 | 泌尿外科 | 未标注 | 钱聚标-泌尿外科-未标注-广东药科大学附属第一医院.jpg | 809724 | 1034×1551 | `17ba29bb6df4d761fd5e7188950ffaedbbdb08a5e9039748932a16d253763809` | 0 | https://www.gy120.net/files/20180104124133380.jpg |
| 王忠 | 180 | 泌尿外科 | 主任医师 | 王忠-泌尿外科-主任医师-广东药科大学附属第一医院.jpg | 529238 | 717×1076 | `e31e3c3944b0f12c28458a48d6192dfcc9555aea839ed89f64546e2f4b3aafcc` | 0 | https://www.gy120.net/files/20180104114057053.JPG |
| 白亮 | 202 | 泌尿外科 | 副主任医师 | 白亮-泌尿外科-副主任医师-广东药科大学附属第一医院.jpg | 41410 | 160×240 | `221ab96bf03ac9e47eb64718c4e659cbb176db9c92508f7203270db60b7b62ba` | 0 | https://www.gy120.net/files/20130917121516056.JPG |
| 高炜城 | 203 | 泌尿外科 | 主治医师 | 高炜城-泌尿外科-主治医师-广东药科大学附属第一医院.jpg | 49744 | 160×240 | `51422ff0eca76dba8577d2a14dc48607aad557373e4c28860c3050c936db8972` | 0 | https://www.gy120.net/files/20130917121602263.JPG |
| 张滨 | 507 | 泌尿外科 | 主任医师 | 张滨-泌尿外科-主任医师-广东药科大学附属第一医院.png | 632918 | 494×623 | `0be03b8c69fa83f72cc6ae6ef7fe602ab31d1b9e4c750ffe6f87aa2cabcf4057` | 0 | https://www.gy120.net/files/20230309110142825.jpg |
| 张滨 | 552 | 康复医学科 | 未标注 | 张滨-康复医学科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428210457661.jpg |
| 张威 | 145 | 神经外科 | 主任医师 | 张威-神经外科-主任医师-广东药科大学附属第一医院.jpg | 285656 | 1644×2192 | `1380f2603db2f82a3c0027fde56cbf5a6e846ee929e8aa10fb98335a00ff7663` | 0 | https://www.gy120.net/files/20180104110657969.jpg |
| 王向宇 | 530 | 神经外科 | 主任医师 | 王向宇-神经外科-主任医师-广东药科大学附属第一医院.jpg | 23828 | 294×412 | `21875e09bb785adc6d9285b31b309be420b67ded7509f14fb45dc0e9f61a9389` | 0 | https://www.gy120.net/files/20250730113330632.jpg |
| 钟德泉 | 60 | 神经外科 | 主任医师 | 钟德泉-神经外科-主任医师-广东药科大学附属第一医院.jpg | 422822 | 631×946 | `930dfe3fd2a09ce9f8864d5474fcb9f5b80011b84c4d69eaa60f4367c5be3657` | 1 | https://www.gy120.net/files/20180104115133989.JPG |
| 殷利明 | 58 | 神经外科 | 主任医师 | 殷利明-神经外科-主任医师-广东药科大学附属第一医院.jpg | 515132 | 685×1027 | `edd6e79a27edd3c48b6b5cedcbc8afe165c660c8a5ce770c259d886d4cda9aed` | 0 | https://www.gy120.net/files/20180104115449246.JPG |
| 周辉 | 431 | 神经外科 | 副主任医师 | 周辉-神经外科-副主任医师-广东药科大学附属第一医院.jpg | 2059476 | 2511×3600 | `036ab108bae86abc6bb471ebc1a1006cc861c6699e81eca5baa700aa826d6309` | 0 | https://www.gy120.net/files/20171218110440771.jpg |
| 刘沣 | 467 | 神经外科 | 副主任医师 | 刘沣-神经外科-副主任医师-广东药科大学附属第一医院.jpg | 21106 | 263×346 | `3815401a50ed42bbe68bbceb0caf52fd3c032398349dccbc254f97f22bc0f028` | 0 | https://www.gy120.net/files/20200409093533496.jpg |
| 赵展 | 206 | 神经外科 | 副主任医师 | 赵展-神经外科-副主任医师-广东药科大学附属第一医院.jpg | 486580 | 683×1024 | `5e23f85b68ab8c18e9685bad2537b4c48bdec22f1ea8469c2e9c4a39f1867331` | 0 | https://www.gy120.net/files/20180104115516564.JPG |
| 王文涛 | 207 | 神经外科 | 主任医师 | 王文涛-神经外科-主任医师-广东药科大学附属第一医院.jpg | 38908 | 254×338 | `f9eeff069591146a2c5d266970212773a61ed09a57f3300f7bdec248f3674306` | 0 | https://www.gy120.net/files/20180104115340937.jpg |
| 徐伟光 | 208 | 神经外科 | 副主任医师 | 徐伟光-神经外科-副主任医师-广东药科大学附属第一医院.jpg | 49034 | 160×240 | `fa97707efb025fd685239288bd4003c01c527d9030662c0db24734b2285f3218` | 0 | https://www.gy120.net/files/20130922122616458.JPG |
| 肖海平 | 482 | 心胸外科 | 副主任医师 | 肖海平-心胸外科-副主任医师-广东药科大学附属第一医院.jpg | 1691520 | 1654×2362 | `8aab59dbcb8024ca3cec6248b7fef9d07c877414cf7b267a88a0ee9d3c595536` | 0 | https://www.gy120.net/files/20240831082605529.JPG |
| 章海波 | 70 | 心胸外科 | 主任医师 | 章海波-心胸外科-主任医师-广东药科大学附属第一医院.jpg | 424824 | 623×933 | `367f17db7cc1ade95fc7a7832b7de3f6e0da3f6b40a8e3b49f2129f8c8ed2962` | 0 | https://www.gy120.net/files/20180104120602844.JPG |
| 祝曙光 | 233 | 心胸外科 | 主任医师 | 祝曙光-心胸外科-主任医师-广东药科大学附属第一医院.jpg | 499230 | 710×1065 | `4fad8f4f5612624c8e388ee5c26937fd0ca35df4b87f866b3d566c76663b7060` | 0 | https://www.gy120.net/files/20180104120619915.JPG |
| 黄壮荣 | 105 | 心胸外科 | 主任医师 | 黄壮荣-心胸外科-主任医师-广东药科大学附属第一医院.jpg | 478164 | 679×1018 | `0f1ce2af3a2b89aa72e50bdf11bbf6e79b4a5e83f4cd7e8fc4caa772185d071c` | 0 | https://www.gy120.net/files/20180104120523254.JPG |
| 张永成 | 55 | 乳腺科 | 主任医师 | 张永成-乳腺科-主任医师-广东药科大学附属第一医院.jpg | 494358 | 666×999 | `34a654061c3054c02e7a51bece9d2caa234221fbbcd41f007310d1a62fba24c7` | 0 | https://www.gy120.net/files/20180104114355341.JPG |
| 沙莉 | 373 | 乳腺科 | 副主任医师 | 沙莉-乳腺科-副主任医师-广东药科大学附属第一医院.jpg | 1199846 | 1645×2467 | `2cb65a56a629896d2edda202ef2aec88654578211e76ad68a3837f9ed0d149f7` | 0 | https://www.gy120.net/files/20180104124200135.jpg |
| 林强 | 576 | 创伤与关节外科（骨一科） | 主任医师 | 林强-创伤与关节外科（骨一科）-主任医师-广东药科大学附属第一医院.jpg | 3673536 | 1950×2942 | `65471bbcde6eee9d09e5f08231b9fbaa854a0cc2ebc9f5c6eda2a615b4d7103e` | 0 | https://www.gy120.net/files/20240226151958546.jpg |
| 林强 | 611 | 足踝与创面修复科（骨四科） | 主任医师 | 林强-足踝与创面修复科（骨四科）-主任医师-广东药科大学附属第一医院.jpg | 24462 | 250×375 | `fc1decc61bbb3077e2eadae167e805eae7fc96eed6e48182e4cef9f8ba8d5315` | 0 | https://www.gy120.net/files/20260720135124598.jpg |
| 董群伟 | 579 | 创伤与关节外科（骨一科） | 主任医师 | 董群伟-创伤与关节外科（骨一科）-主任医师-广东药科大学附属第一医院.jpg | 253554 | 481×723 | `785626fb415ae44348ba7db253e8b237dc2adccf58e9635aa32965a0d8eb1533` | 0 | https://www.gy120.net/files/20180104112712860.JPG |
| 董群伟 | 612 | 足踝与创面修复科（骨四科） | 主任医师 | 董群伟-足踝与创面修复科（骨四科）-主任医师-广东药科大学附属第一医院.jpg | 24828 | 250×377 | `dd6520e1621186083038be1a3f3ea9862e99a321f1ce55a54fd46c3ca830f7a9` | 0 | https://www.gy120.net/files/20260720135441345.jpg |
| 王华 | 161 | 创伤与关节外科（骨一科） | 副主任医师 | 王华-创伤与关节外科（骨一科）-副主任医师-广东药科大学附属第一医院.jpg | 647670 | 754×1130 | `26e8eb761a14d72141d2b2b5e6d3f86bf73c85d234d6aff7b9a8e4b9e95fc251` | 0 | https://www.gy120.net/files/20180104112945839.JPG |
| 王华 | 526 | 运动医学科（骨三科） | 副主任医师 | 王华-运动医学科（骨三科）-副主任医师-广东药科大学附属第一医院.jpg | 2584 | 119×174 | `e96302a866e89bbef91a865e465158d325d9528e1046ee0e5c83b179d66b774e` | 0 | https://www.gy120.net/files/20230112171714885.jpg |
| 李晓初 | 515 | 创伤与关节外科（骨一科） | 副主任医师 | 李晓初-创伤与关节外科（骨一科）-副主任医师-广东药科大学附属第一医院.jpg | 55324 | 574×760 | `fb80fdfd7fabd06b35bfefb32407a75e480d2a41f4c82ab9607e950d595a1687` | 0 | https://www.gy120.net/files/20240830144857318.jpg |
| 宋炎成 | 420 | 创伤与关节外科（骨一科） | 主任医师 | 宋炎成-创伤与关节外科（骨一科）-主任医师-广东药科大学附属第一医院.jpg | 428876 | 656×984 | `584c2a09f89da71da192f497f9b0489c22a56bf4e47a4865f592e97b4a5858c8` | 0 | https://www.gy120.net/files/20180104112922200.JPG |
| 王晓东 | 219 | 创伤与关节外科（骨一科） | 主任医师 | 王晓东-创伤与关节外科（骨一科）-主任医师-广东药科大学附属第一医院.jpg | 442004 | 672×1009 | `41ae94f75507d2aa45ecfb43626b1c58a9198e0aa2eadaba2a6e6445fc5ff005` | 0 | https://www.gy120.net/files/20180104111711113.JPG |
| 冯振华 | 34 | 创伤与关节外科（骨一科） | 副主任医师 | 冯振华-创伤与关节外科（骨一科）-副主任医师-广东药科大学附属第一医院.jpg | 460952 | 640×960 | `e2a71706332c39374a5500bc76fd091d99bef6465b4fcfecb8b58f0c981700fa` | 0 | https://www.gy120.net/files/20180104112732165.JPG |
| 郝群禹 | 221 | 创伤与关节外科（骨一科） | 副主任医师 | 郝群禹-创伤与关节外科（骨一科）-副主任医师-广东药科大学附属第一医院.jpg | 517138 | 672×1009 | `9b31498a85f598881cbaad5d875eefc081974498daa016e15dc0e299a162b093` | 0 | https://www.gy120.net/files/20180104112819717.JPG |
| 郭洲 | 35 | 创伤与关节外科（骨一科） | 副主任医师 | 郭洲-创伤与关节外科（骨一科）-副主任医师-广东药科大学附属第一医院.jpg | 513930 | 672×1008 | `2c38e6e56b3be267b26ff26b14f10478fd7c1acfa87a9f2146146c80261ae4f4` | 0 | https://www.gy120.net/files/20180104112756510.JPG |
| 昌宏 | 455 | 创伤与关节外科（骨一科） | 副主任医师 | 昌宏-创伤与关节外科（骨一科）-副主任医师-广东药科大学附属第一医院.jpg | 49840 | 300×428 | `a406643e819ade13c4e62bfd17a387218a3c56ac2dec66f244c184bdfff4a06b` | 0 | https://www.gy120.net/files/20251201103248562.jpg |
| 蔡杨庭 | 516 | 创伤与关节外科（骨一科） | 主治医师 | 蔡杨庭-创伤与关节外科（骨一科）-主治医师-广东药科大学附属第一医院.jpg | 27386 | 203×275 | `7388958e32b032d7ee7b5300e8e64b21b004cee9f4c318c9bfed06054d7e2755` | 0 | https://www.gy120.net/files/20240830145449107.jpg |
| 朱辉 | 511 | 脊柱外科（骨二科） | 副主任医师 | 朱辉-脊柱外科（骨二科）-副主任医师-广东药科大学附属第一医院.jpg | 1408960 | 1654×2362 | `081228a6629081f65809bb359822c16cdb298e24170175fa22ab8e0b6c53c435` | 0 | https://www.gy120.net/files/20240830084232853.JPG |
| 洪曼杰 | 36 | 脊柱外科（骨二科） | 主任医师 | 洪曼杰-脊柱外科（骨二科）-主任医师-广东药科大学附属第一医院.jpg | 526764 | 676×1013 | `bf623f2cd4b09866799fb3fff4cbc5b69f5c921ac5d6ec7ae799ee5c2aeb2a44` | 0 | https://www.gy120.net/files/20180104112840332.JPG |
| 胡伶平 | 512 | 脊柱外科（骨二科） | 副主任医师 | 胡伶平-脊柱外科（骨二科）-副主任医师-广东药科大学附属第一医院.jpg | 689766 | 1034×1551 | `e1e99c5f89b537c2c3ebb51d9b748f9a9a8aa6d7a2bc78b18f8dc4838604e272` | 0 | https://www.gy120.net/files/20240830150748283.jpg |
| 巫培康 | 37 | 脊柱外科（骨二科） | 副主任医师 | 巫培康-脊柱外科（骨二科）-副主任医师-广东药科大学附属第一医院.jpg | 518260 | 690×1035 | `fdeabebbc2b8c1dea64d90eaf47ee056aa2591b7576e0bfd36841d9587c0cef2` | 0 | https://www.gy120.net/files/20180104113002899.JPG |
| 王健 | 490 | 脊柱外科（骨二科） | 主治医师 | 王健-脊柱外科（骨二科）-主治医师-广东药科大学附属第一医院.jpg | 35978 | 236×370 | `3cbc77f3cd20ec72d2386ed8b1b7ef17e6eb61e8cc0e51ceb0ad9b14fe073e3b` | 0 | https://www.gy120.net/files/20240830145822924.jpg |
| 罗学辉 | 527 | 运动医学科（骨三科） | 主任医师 | 罗学辉-运动医学科（骨三科）-主任医师-广东药科大学附属第一医院.jpg | 34172 | 260×363 | `4cfb4ff6bf4e80dee8df6cf61157d6d45c3fd39000f66d8a2655548485214e37` | 0 | https://www.gy120.net/files/20250718160138406.jpg |
| 庾广文 | 525 | 运动医学科（骨三科） | 副主任医师 | 庾广文-运动医学科（骨三科）-副主任医师-广东药科大学附属第一医院.jpg | 2584 | 119×174 | `e96302a866e89bbef91a865e465158d325d9528e1046ee0e5c83b179d66b774e` | 0 | https://www.gy120.net/files/20230112171714885.jpg |
| 王凤雄 | 613 | 足踝与创面修复科（骨四科） | 科主任 | 王凤雄-足踝与创面修复科（骨四科）-科主任-广东药科大学附属第一医院.jpg | 24674 | 250×356 | `ca9ff3bf4baed45b41197442b7a9685757480653149f7136bc352ff62ce69530` | 0 | https://www.gy120.net/files/20260720135656425.jpg |
| 王飞 | 615 | 足踝与创面修复科（骨四科） | 副主任医师 | 王飞-足踝与创面修复科（骨四科）-副主任医师-广东药科大学附属第一医院.jpg | 29094 | 250×362 | `416009f9c30e45660c58300468ac45ef02c55ecddb35af8e19c8b94cd73f86f2` | 0 | https://www.gy120.net/files/20260720140028908.jpg |
| 林宇凤 | 616 | 足踝与创面修复科（骨四科） | 主治医师 | 林宇凤-足踝与创面修复科（骨四科）-主治医师-广东药科大学附属第一医院.jpg | 23572 | 250×356 | `1a9c4237ccaa4fdb92065ccd2022e3f60887045fed443f416a0a96545b237900` | 0 | https://www.gy120.net/files/20260720140137997.jpg |
| 林伟鹏 | 617 | 足踝与创面修复科（骨四科） | 主治医师 | 林伟鹏-足踝与创面修复科（骨四科）-主治医师-广东药科大学附属第一医院.jpg | 26098 | 250×356 | `aa1c8674a1e0caae8ccc27f10f11c0fbd61a7dd42062f3e35c27fbf22889e294` | 0 | https://www.gy120.net/files/20260720140252406.jpg |
| 洪铭范 | 101 | 神经内科(头痛门诊) | 主任医师 | 洪铭范-神经内科(头痛门诊)-主任医师-广东药科大学附属第一医院.jpg | 375776 | 946×1263 | `698f6aef1f6375f635fa0b04d600b6d0584e20cadeb4220223da6b7e02531487` | 0 | https://www.gy120.net/files/20180104125649423.jpg |
| 彭忠兴 | 228 | 神经内科(头痛门诊) | 主任医师 | 彭忠兴-神经内科(头痛门诊)-主任医师-广东药科大学附属第一医院.jpg | 371924 | 657×986 | `0ad4c0db631ab36da41bc73010455a91c686c31a5651d210e898d46f58871ea9` | 0 | https://www.gy120.net/files/20180104115001520.JPG |
| 刘爱群 | 332 | 神经内科(头痛门诊) | 主任医师 | 刘爱群-神经内科(头痛门诊)-主任医师-广东药科大学附属第一医院.jpg | 348324 | 602×903 | `4bdb21bcff146ecaca69b5486bd2af385f7fdd18a4f75096fe3cd87cebc115aa` | 0 | https://www.gy120.net/files/20180104114653954.JPG |
| 周志华 | 486 | 神经内科(头痛门诊) | 副主任医师 | 周志华-神经内科(头痛门诊)-副主任医师-广东药科大学附属第一医院.jpg | 177342 | 1080×1283 | `ecb66b93ef6cb01bfeabb1b5197c6182c3d50c3a3b7ac047bb180fc64f5b5789` | 0 | https://www.gy120.net/files/20220802092405468.jpg |
| 余青云 | 151 | 神经内科(头痛门诊) | 主任医师 | 余青云-神经内科(头痛门诊)-主任医师-广东药科大学附属第一医院.jpg | 512046 | 676×1015 | `1df4ffc0ab233f1761715e57ebab9420f4021e1c3c60dbbc4049a0128a9fce97` | 0 | https://www.gy120.net/files/20180104115045094.JPG |
| 刘玉华 | 109 | 神经内科(头痛门诊) | 主任医师 | 刘玉华-神经内科(头痛门诊)-主任医师-广东药科大学附属第一医院.jpg | 476010 | 663×994 | `6980d87bf5732d54b34bb25647f1c7aeafea9f814c629cd7162d373560e2dd75` | 0 | https://www.gy120.net/files/20180104114713126.JPG |
| 危智盛 | 410 | 神经内科(头痛门诊) | 副主任医师 | 危智盛-神经内科(头痛门诊)-副主任医师-广东药科大学附属第一医院.jpg | 559468 | 742×1113 | `818d6d5e44c68b3332c6960870b123cffdab3db65b610f6ebbbd48d8351d332b` | 0 | https://www.gy120.net/files/20180104115025733.JPG |
| 刁胜朋 | 411 | 神经内科(头痛门诊) | 主治医师 | 刁胜朋-神经内科(头痛门诊)-主治医师-广东药科大学附属第一医院.jpg | 24376 | 117×175 | `7133326ba1d0a867cc3225f2d3177a61fb3cc323a7101b0e38b30bdf72c6a982` | 0 | https://www.gy120.net/files/20180718150916524.jpg |
| 郭姣 | 443 | 中西医结合代谢病科 | 主任医师 | 郭姣-中西医结合代谢病科-主任医师-广东药科大学附属第一医院.jpg | 9984 | 119×174 | `0679f08c76f78c58fa5ad1d85232f333d66953611047f99cc281197927c9ddd9` | 0 | https://www.gy120.net/files/20190124144632627.jpg |
| 李雄 | 465 | 中西医结合代谢病科 | 主任医师 | 李雄-中西医结合代谢病科-主任医师-广东药科大学附属第一医院.jpg | 2020694 | 1820×2729 | `f869d7dcbdefa9884ca742e2ede3596c7f4c3a336a45e71ae6cdd247c32bf37d` | 0 | https://www.gy120.net/files/20200228111433234.jpg |
| 幸冰峰 | 314 | 中西医结合代谢病科 | 副主任医师 | 幸冰峰-中西医结合代谢病科-副主任医师-广东药科大学附属第一医院.jpg | 1499932 | 1654×2362 | `775f887c66f4e074be957efd173c7b7c0e1a47a93fe59f4ea098c84ac9be63cd` | 0 | https://www.gy120.net/files/20241031092218165.JPG |
| 朴胜华 | 445 | 中西医结合代谢病科 | 副主任医师 | 朴胜华-中西医结合代谢病科-副主任医师-广东药科大学附属第一医院.jpg | 10640 | 119×178 | `114b16052dc66bde03eda7c8b478c7b6262826257c3833f7efc1c244fb4cd701` | 0 | https://www.gy120.net/files/20190124145617412.jpg |
| 金英花 | 466 | 中西医结合代谢病科 | 主任中医师 | 金英花-中西医结合代谢病科-主任中医师-广东药科大学附属第一医院.jpg | 27996 | 211×300 | `faef39794919a23e7ce5da5bec3d313e6391cdb474db6a0d4fb17ec81b602124` | 0 | https://www.gy120.net/files/20260604154225450.jpg |
| 万利梅 | 598 | 中西医结合代谢病科 | 副主任医师 | 万利梅-中西医结合代谢病科-副主任医师-广东药科大学附属第一医院.jpg | 61120 | 250×350 | `62b9e73e583657e06cfa4310102656717b288237f8f12de8414476061d002b50` | 0 | https://www.gy120.net/files/20260514203545119.JPG |
| 陈滢宇 | 317 | 中西医结合代谢病科 | 主治医师 | 陈滢宇-中西医结合代谢病科-主治医师-广东药科大学附属第一医院.jpg | 5585098 | 4000×4000 | `dd431a6313ca551925aca734ad97f043c379d3843e5c858f404ba574c858d050` | 0 | https://www.gy120.net/files/20240520164432195.jpg |
| 刁蔚欣 | 324 | 中西医结合代谢病科 | 副主任医师 | 刁蔚欣-中西医结合代谢病科-副主任医师-广东药科大学附属第一医院.jpg | 484770 | 672×1008 | `892896793e262d966a1efe3a22947ba3ddee58b3bc0f2e2cdfdbc35ac6db2d8e` | 0 | https://www.gy120.net/files/20180104110924821.JPG |
| 曾育辉 | 196 | 急诊科 | 主任医师 | 曾育辉-急诊科-主任医师-广东药科大学附属第一医院.jpg | 651994 | 772×1158 | `e8b16060c7b4985e56b9a821022a13eda94c324f2ac91df5b626ba8bebb91134` | 0 | https://www.gy120.net/files/20181108170605452.jpg |
| 梁秋玲 | 197 | 急诊科 | 副主任医师 | 梁秋玲-急诊科-副主任医师-广东药科大学附属第一医院.jpg | 223642 | 446×669 | `477012a56a2658fe5dcb5b7fdca920a1e317196d83022a6eda554ad3023530b4` | 0 | https://www.gy120.net/files/20180104113301187.JPG |
| 黄穗霞 | 343 | 急诊科 | 主治医师 | 黄穗霞-急诊科-主治医师-广东药科大学附属第一医院.jpg | 1155736 | 1200×1800 | `5c5c2169ca0087d5ad8ada10c9c6249bbeac382f03e280d296a063e798bb704a` | 0 | https://www.gy120.net/files/20150722145123301.JPG |
| 常威 | 610 | 急诊科 | 副主任医师 | 常威-急诊科-副主任医师-广东药科大学附属第一医院.jpg | 61030 | 250×350 | `16801c681608ef023c1ec38f06e81258a7d29b2c612b3aabf1f60cea4873db7e` | 0 | https://www.gy120.net/files/20260514204856797.JPG |
| 朱海平 | 608 | 急诊科 | 副主任医师 | 朱海平-急诊科-副主任医师-广东药科大学附属第一医院.png | 216942 | 293×425 | `dc815c0b68924f93cf8d137e1f15bc8309ed53ae5bf14e92e00c7138b88f3e1f` | 0 | https://www.gy120.net/files/20260604155240019.png |
| 韦焕杰 | 609 | 急诊科 | 副主任医师 | 韦焕杰-急诊科-副主任医师-广东药科大学附属第一医院.jpg | 59620 | 250×350 | `12035ee6f1f1ac4b114741c7815876087ff62e24da52de5defdc42e5c77e3946` | 0 | https://www.gy120.net/files/20260514203321870.JPG |
| 陈瑞芳 | 346 | 急诊科 | 副主任医师 | 陈瑞芳-急诊科-副主任医师-广东药科大学附属第一医院.jpg | 473190 | 624×936 | `c350570f9f2c660622436e244f31dccefe088237939c513efa4a4a9420ef2fef` | 0 | https://www.gy120.net/files/20180104113240441.JPG |
| 李孟升 | 347 | 急诊科 | 主治医师 | 李孟升-急诊科-主治医师-广东药科大学附属第一医院.jpg | 1132506 | 1200×1800 | `a0c011a33b1cc84fb5f8d69a39c190ea2988d0cd41a58329a99fd7991310f950` | 0 | https://www.gy120.net/files/20150729090455267.JPG |
| 张凡 | 436 | 急诊科 | 副主任医师 | 张凡-急诊科-副主任医师-广东药科大学附属第一医院.jpg | 45488 | 117×170 | `7e108063fd288b6f7cf9fdfcdb321d927e6f88a6be4d63c4b5b7d7f456423b9e` | 0 | https://www.gy120.net/files/20180801082352429.jpg |
| 何雁冰 | 485 | 疼痛科 | 副主任医师 | 何雁冰-疼痛科-副主任医师-广东药科大学附属第一医院.jpg | 5596 | 206×205 | `3a7e17022adf1dd8e3be442a6965e7117fff573ee2397f07f7dd7c51a17852ea` | 0 | https://www.gy120.net/files/20220718113811054.jpg |
| 骆婕 | 387 | 妇产科 | 主任医师 | 骆婕-妇产科-主任医师-广东药科大学附属第一医院.jpg | 1498056 | 1654×2362 | `21954749a96086557eec450e6b98a23bdf4852581507eef4de9749b55fbfb6a5` | 0 | https://www.gy120.net/files/20240831082750532.JPG |
| 陶莹 | 112 | 妇产科 | 主任医师 | 陶莹-妇产科-主任医师-广东药科大学附属第一医院.jpg | 1401640 | 1645×2467 | `6c545c3509a48bbf6ab49c2dd7bb0745e76c85c8faa613a0468feb19343546b3` | 0 | https://www.gy120.net/files/20180104124222756.jpg |
| 王浩 | 164 | 妇产科 | 主任医师 | 王浩-妇产科-主任医师-广东药科大学附属第一医院.jpg | 550576 | 706×1059 | `b04c2a2d05101ef74316c6c659ccad9294bd3053fde541668feafde55590160d` | 0 | https://www.gy120.net/files/20180104112145812.JPG |
| 何力 | 100 | 妇产科 | 主任医师 | 何力-妇产科-主任医师-广东药科大学附属第一医院.jpg | 233612 | 446×669 | `8de0423e3d6d0af9d52be1334b651d01be70c1946942b40e43f1482cc87343a9` | 0 | https://www.gy120.net/files/20180104111232921.JPG |
| 李筠 | 336 | 妇产科 | 副主任医师 | 李筠-妇产科-副主任医师-广东药科大学附属第一医院.jpg | 458234 | 638×958 | `cc4bc415c22e431e2b57dfc9cfaf732f9596e7db19d5ffdb5f3e74b044b8c13d` | 0 | https://www.gy120.net/files/20180104112120454.JPG |
| 高瑞萍 | 96 | 妇产科 | 主任医师 | 高瑞萍-妇产科-主任医师-广东药科大学附属第一医院.jpg | 457728 | 649×974 | `483c5a8017bdb6ae9640d25bae7b887b15ec11bea331f5fa909df35f356cdde2` | 0 | https://www.gy120.net/files/20180104111813475.JPG |
| 郭琴 | 384 | 妇产科 | 副主任医师 | 郭琴-妇产科-副主任医师-广东药科大学附属第一医院.jpg | 125916 | 533×800 | `8ddae9fbaf2d6ea5709d197a4dd316ae909074a837d7ce3daeeabf4be6d15d9f` | 0 | https://www.gy120.net/files/20170905161539635.jpg |
| 廖凤儿 | 396 | 妇产科 | 主治医师 | 廖凤儿-妇产科-主治医师-广东药科大学附属第一医院.jpg | 28770 | 117×175 | `27e039bed84404896374d58966f1a6435c638bcb7afe1bb377436fec7bafa70c` | 0 | https://www.gy120.net/files/20180718165515846.jpg |
| 赵曼丹 | 432 | 妇产科 | 主治医师 | 赵曼丹-妇产科-主治医师-广东药科大学附属第一医院.jpg | 1118646 | 1200×1800 | `9e6229b3e1767c95952642e6fc18d26235dab3e2294bf40568bc280abd910365` | 0 | https://www.gy120.net/files/20171229110602278.JPG |
| 郭苑莉 | 605 | 妇产科 | 副主任医师 | 郭苑莉-妇产科-副主任医师-广东药科大学附属第一医院.jpg | 54814 | 250×350 | `d0bfe242a5e81eb5598b8470cb9cca022992e3e21a57c7f059834e6e42ca74d8` | 0 | https://www.gy120.net/files/20260514203016453.JPG |
| 郑婷 | 606 | 妇产科 | 副主任医师 | 郑婷-妇产科-副主任医师-广东药科大学附属第一医院.jpg | 54810 | 250×350 | `5c9691519d4ccceb151ea1099d87b18c69bcf1fdeb9a17c35093bb82cf4e53ac` | 0 | https://www.gy120.net/files/20260514203707502.JPG |
| 孟翠萍 | 342 | 儿科 | 主任医师 | 孟翠萍-儿科-主任医师-广东药科大学附属第一医院.jpg | 571592 | 702×1053 | `afe198a3c04b62457d0f0cb36a625237ff318778af093a26003a06d76133f0d3` | 0 | https://www.gy120.net/files/20180104111310666.JPG |
| 冯卓玲 | 11 | 儿科 | 副主任医师 | 冯卓玲-儿科-副主任医师-广东药科大学附属第一医院.jpg | 232766 | 486×729 | `b022c454c3e374fb6f06257b59bc8a88f531fb0f54f97d4ccf3cbdbf0a7c58ec` | 0 | https://www.gy120.net/files/20180104111110656.JPG |
| 钱蔚珍 | 167 | 儿科 | 副主任医师 | 钱蔚珍-儿科-副主任医师-广东药科大学附属第一医院.jpg | 566522 | 694×1040 | `2e3a1689c21865539efe6e1ced611623d249b1e0d66da0af9ebfc7607685783e` | 0 | https://www.gy120.net/files/20180104111404635.JPG |
| 潘昊 | 4 | 儿科 | 副主任医师 | 潘昊-儿科-副主任医师-广东药科大学附属第一医院.jpg | 209690 | 430×645 | `f207d5f106edf3bcc30057eafd2fcac98ec08235ac427d8ac1074f9ea60a285b` | 0 | https://www.gy120.net/files/20180104111337881.JPG |
| 王崧 | 597 | 儿科 | 副主任医师 | 王崧-儿科-副主任医师-广东药科大学附属第一医院.jpg | 62624 | 250×350 | `7b3f4701617381b053ea5f39eb4b6808b2a52209a49aec9c1ae8cb2c04935da2` | 0 | https://www.gy120.net/files/20260514202429467.jpg |
| 贺爱辉 | 149 | 肠道门诊（农林） | 副主任医师 | 贺爱辉-肠道门诊（农林）-副主任医师-广东药科大学附属第一医院.jpg | 423340 | 600×900 | `396c094a0abe343bb04bace89ab7b636244f09bd41b336e3ebb2f21d93af808a` | 0 | https://www.gy120.net/files/20180104110950604.JPG |
| 张少华 | 32 | 肠道门诊（农林） | 主任医师 | 张少华-肠道门诊（农林）-主任医师-广东药科大学附属第一医院.jpg | 1212966 | 1645×2467 | `de6ba5331ee351be0e438966d436eee385a13a206241ab8f38bf4af1ff1bf218` | 0 | https://www.gy120.net/files/20180104124352347.jpg |
| 李烨 | 325 | 肠道门诊（农林） | 副主任医师 | 李烨-肠道门诊（农林）-副主任医师-广东药科大学附属第一医院.jpg | 536448 | 676×1013 | `7eb7feddd89a46a5258c097f3c8ed42a8976f6bea6e36d52c2382bb8b8652544` | 0 | https://www.gy120.net/files/20180104111016393.JPG |
| 尹金柱 | 117 | 门诊(普通内科) | 主任医师 | 尹金柱-门诊(普通内科)-主任医师-广东药科大学附属第一医院.jpg | 521464 | 680×1020 | `2eaffd4574f3df9a8bdff3cb026eb1d6045efe831f7719bd0ecb5b7951f5a202` | 0 | https://www.gy120.net/files/20180104113825450.JPG |
| 苏妤 | 560 | 门诊(普通内科) | 副主任医师 | 苏妤-门诊(普通内科)-副主任医师-广东药科大学附属第一医院.jpg | 24480 | 250×356 | `9c63b5aad79e224fe2f6b308cb0cb451499255eb6ad28d9d429f1703fdef4534` | 0 | https://www.gy120.net/files/20260720140738764.jpg |
| 管红斌 | 158 | 门诊(普通内科) | 主任医师 | 管红斌-门诊(普通内科)-主任医师-广东药科大学附属第一医院.jpg | 252238 | 468×702 | `aa0293399ac982951e97ebb8ae942b70e3840201cb11c7b8e3374ce8ef48b42c` | 0 | https://www.gy120.net/files/20180104113709081.JPG |
| 王洪云 | 447 | 门诊(普通内科) | 副主任医师 | 王洪云-门诊(普通内科)-副主任医师-广东药科大学附属第一医院.jpg | 9944 | 119×178 | `bdda0a475aadee19d38f3cf4a68c889fd942a428af0781673b15899444659909` | 0 | https://www.gy120.net/files/20190124150103835.jpg |
| 杨驱云 | 364 | 门诊(普通内科) | 副主任医师 | 杨驱云-门诊(普通内科)-副主任医师-广东药科大学附属第一医院.jpg | 1055648 | 2251×2770 | `bec261baa05f0620a9eb9b92842d91ca11fc3b3b0ecf1ef3301e26a16a06b09c` | 0 | https://www.gy120.net/files/20231225095323164.jpg |
| 黄四邑 | 334 | 门诊(普通内科) | 副主任医师 | 黄四邑-门诊(普通内科)-副主任医师-广东药科大学附属第一医院.jpg | 496612 | 645×966 | `a08c5bdaa76edd1f0c8218c7c115a80ec2acbea16a5b56be6aa7191b2d9f9ec7` | 0 | https://www.gy120.net/files/20180104113725386.JPG |
| 武兴杰 | 276 | 介入治疗科 | 主任医师 | 武兴杰-介入治疗科-主任医师-广东药科大学附属第一医院.jpg | 644556 | 737×1105 | `d160231280dac7a5e362a26f0a8b42979d2d665c621a732f98ca1c20e0e05b66` | 0 | https://www.gy120.net/files/20180104122359778.JPG |
| 刘琦 | 523 | 口腔科 | 主任医师 | 刘琦-口腔科-主任医师-广东药科大学附属第一医院.jpg | 45884 | 400×560 | `63175a69df21d0608f09422cd0805b6440aed787f1194a6822d32cfc0daf63c2` | 0 | https://www.gy120.net/files/20250616104301031.jpg |
| 潘宣 | 45 | 口腔科 | 主任医师 | 潘宣-口腔科-主任医师-广东药科大学附属第一医院.jpg | 364492 | 2493×3491 | `627ac6a8e387fbd2ee0f6cf277ce5d91e34424b65de0e5c269855eb478faa205` | 0 | https://www.gy120.net/files/20180104110101569.jpg |
| 王玉栋 | 113 | 口腔科 | 主任医师 | 王玉栋-口腔科-主任医师-广东药科大学附属第一医院.jpg | 506656 | 646×969 | `597884f1ab60d5545c42685c2bd6fe80e3682a4d89b0e7845e76a3a948ad0aea` | 0 | https://www.gy120.net/files/20230612092158921.JPG |
| 冯铁军 | 94 | 口腔科 | 主任医师 | 冯铁军-口腔科-主任医师-广东药科大学附属第一医院.jpg | 352684 | 1179×1572 | `84d63e4acc3741f2368e2cbd929bbc71c8a0d4010f33bddc122240d374b4cd21` | 0 | https://www.gy120.net/files/20180104110552007.jpg |
| 黎慧瑜 | 44 | 口腔科 | 副主任医师 | 黎慧瑜-口腔科-副主任医师-广东药科大学附属第一医院.jpg | 530484 | 686×1029 | `a1bcc3efb1e90bb53d57e087cb4de59997d78596d1e334e0917874ba7d1dce30` | 0 | https://www.gy120.net/files/20180104113540660.JPG |
| 周银凤 | 46 | 口腔科 | 副主任医师 | 周银凤-口腔科-副主任医师-广东药科大学附属第一医院.jpg | 447984 | 630×945 | `b7980caaadbe0f77f11acddea8ef8e166387bffd132ba85b145b936b7e09010f` | 0 | https://www.gy120.net/files/20180104113622404.JPG |
| 李张维 | 279 | 口腔科 | 副主任医师 | 李张维-口腔科-副主任医师-广东药科大学附属第一医院.jpg | 289068 | 1270×1761 | `0630dc5023cb300718bf24ba1e1e7e09f675e4850bd5ce6e8ded7d9137091683` | 0 | https://www.gy120.net/files/20230609160522401.jpg |
| 康成容 | 277 | 口腔科 | 副主任医师 | 康成容-口腔科-副主任医师-广东药科大学附属第一医院.jpg | 39003 | 116×175 | `8f170e1e063fcf94893efc18ff1b992687e42bdc2ca36d32c1a35396306328e9` | 0 | https://www.gy120.net/files/20150720101439912.JPG |
| 陈凯 | 289 | 口腔科 | 副主任医师 | 陈凯-口腔科-副主任医师-广东药科大学附属第一医院.jpg | 1151616 | 1200×1800 | `a3e6c8d8d950c4281c64f4f2f83fadfc0b9614f500b78577bb1c4293893c6b86` | 0 | https://www.gy120.net/files/20150720102026057.JPG |
| 陈慧芝 | 288 | 口腔科 | 副主任医师 | 陈慧芝-口腔科-副主任医师-广东药科大学附属第一医院.jpg | 446012 | 642×963 | `a18902d4284b26ee58b24c2dc2f702d16c06099eff6aacbb1d9c3c3579d62b01` | 0 | https://www.gy120.net/files/20180104113458743.JPG |
| 许志锋 | 291 | 口腔科 | 主治医师 | 许志锋-口腔科-主治医师-广东药科大学附属第一医院.jpg | 1203098 | 1200×1800 | `218c5a28f343700b0a6d453fb8438d541f9ed13441072370f2ab9c13ce6c5890` | 0 | https://www.gy120.net/files/20150818110456321.JPG |
| 贺凌飞 | 183 | 口腔科 | 副主任医师 | 贺凌飞-口腔科-副主任医师-广东药科大学附属第一医院.jpg | 478214 | 678×1017 | `f6f407a48db47b72dd7f584cd1d1aea0c6d6bc823acd488ed586f3fc63da3574` | 0 | https://www.gy120.net/files/20180104113520501.JPG |
| 马穗齐 | 281 | 口腔科 | 主治医师 | 马穗齐-口腔科-主治医师-广东药科大学附属第一医院.jpg | 1298660 | 1200×1800 | `6443a8e30cd5c9852007be800587b0ab542518f0fb56537963e30f0c257d010f` | 0 | https://www.gy120.net/files/20150720101741232.JPG |
| 李梁 | 278 | 口腔科 | 主治医师 | 李梁-口腔科-主治医师-广东药科大学附属第一医院.jpg | 1171058 | 1200×1800 | `d514b46b2dd32f92e9ed903c4a0285abc65b04320dd3633ebb679381be68de3d` | 0 | https://www.gy120.net/files/20150720101321988.JPG |
| 周倩冰 | 285 | 口腔科 | 副主任医师 | 周倩冰-口腔科-副主任医师-广东药科大学附属第一医院.jpg | 25250 | 117×160 | `cf547725d27eead9b10c8e315397d66268ec41f31f2b882ac077038e54555e5f` | 0 | https://www.gy120.net/files/20180718170640805.jpg |
| 何智君 | 290 | 口腔科 | 主治医师 | 何智君-口腔科-主治医师-广东药科大学附属第一医院.jpg | 1293624 | 1200×1800 | `04764aa64ec827d418d6e681f29109b0c435f0086de883376a18854d26821323` | 0 | https://www.gy120.net/files/20150720102127144.JPG |
| 张柏芳 | 68 | 心理科 | 主任医师 | 张柏芳-心理科-主任医师-广东药科大学附属第一医院.jpg | 446492 | 637×956 | `40f711bf8dd26e1c738a8c24461878845ea7575b04c0b65f5c8d94ca1af46018` | 0 | https://www.gy120.net/files/20180104120455621.JPG |
| 黄雪薇 | 104 | 心理科 | 主任医师 | 黄雪薇-心理科-主任医师-广东药科大学附属第一医院.jpg | 202006 | 398×597 | `47e5bcf5b52666764ba4bf4de63458f62dddcdee276c9d433c4fd7dc55fa8479` | 0 | https://www.gy120.net/files/20180104120438561.JPG |
| 皇甫丽 | 102 | 心理科 | 主任医师 | 皇甫丽-心理科-主任医师-广东药科大学附属第一医院.jpg | 540736 | 659×989 | `7796d0d2871f9f283f1f1c3953a2a0a3def0fb8ce8981e94be393d4d70152f3a` | 0 | https://www.gy120.net/files/20180104120421923.JPG |
| 鲍炯琳 | 91 | 眼科 | 主任医师 | 鲍炯琳-眼科-主任医师-广东药科大学附属第一医院.jpg | 396098 | 605×908 | `0f2654c79360e88cc808c4cbc5b940ed3c564af1ade0d1403f7b37d2da5f2fac` | 0 | https://www.gy120.net/files/20180104121112147.JPG |
| 林敏 | 108 | 眼科 | 副主任医师 | 林敏-眼科-副主任医师-广东药科大学附属第一医院.jpg | 837470 | 1034×1551 | `7bb7a0d12cb5314a3971a759bb0f539c669b84f8caa8b371c8be434236001955` | 0 | https://www.gy120.net/files/20180104124040999.jpg |
| 罗小静 | 80 | 眼科 | 副主任医师 | 罗小静-眼科-副主任医师-广东药科大学附属第一医院.jpg | 212292 | 424×636 | `8df216ceeee08092c3ace9cb2bd413dccacbf4a6011b87ef9204dbe8b27ae83a` | 0 | https://www.gy120.net/files/20180104121154064.JPG |
| 周斌兵 | 147 | 眼科 | 主任医师 | 周斌兵-眼科-主任医师-广东药科大学附属第一医院.jpg | 437646 | 624×937 | `3476e1cf066aa5e0c054deba0f1c12f98abe0886c95a595e68158997aab6f195` | 0 | https://www.gy120.net/files/20180104121231262.JPG |
| 朱宇东 | 148 | 眼科 | 副主任医师 | 朱宇东-眼科-副主任医师-广东药科大学附属第一医院.jpg | 630748 | 743×1114 | `8ec4d7622a72641f91cf704217e1335d176a6d86091202a6038f1abb5c4c5d28` | 0 | https://www.gy120.net/files/20180104121249286.JPG |
| 林文雄 | 215 | 眼科 | 主任医师 | 林文雄-眼科-主任医师-广东药科大学附属第一医院.jpg | 590788 | 706×1059 | `cfa3eaf87846bf83c18f3e4483b5e0bf5932206f319ce2b0d4d674c6818f7925` | 0 | https://www.gy120.net/files/20180104121133519.JPG |
| 李青 | 216 | 眼科 | 主治医师 | 李青-眼科-主治医师-广东药科大学附属第一医院.jpg | 49518 | 160×240 | `d467357250518728e8049cdc0a5baadcd4274becf3b8632852f81216ea8d306b` | 0 | https://www.gy120.net/files/20130922162848534.JPG |
| 王文娟 | 298 | 眼科 | 住院医师 | 王文娟-眼科-住院医师-广东药科大学附属第一医院.jpg | 26842 | 117×168 | `71b2db2414d65c327e20c70eac3b0e2625d6f4e06acb3887b590c879fbb1fada` | 0 | https://www.gy120.net/files/20180718171339800.jpg |
| 黄飞麒 | 248 | 正骨科 | 主任医师 | 黄飞麒-正骨科-主任医师-广东药科大学附属第一医院.jpg | 524516 | 693×1039 | `ad2380343d4a50e77cb4eb0946b0c1c8f9399dcf8245003f44ec001f2cb98696` | 0 | https://www.gy120.net/files/20180104122836619.JPG |
| 陈扬声 | 247 | 正骨科 | 主治医师 | 陈扬声-正骨科-主治医师-广东药科大学附属第一医院.jpg | 49498 | 166×249 | `e87679f780a331ef4678a7cd336d1c5ca0aa80017aba42de67da972fd28b34a9` | 0 | https://www.gy120.net/files/20140928112113051.JPG |
| 陈晓波 | 561 | 正骨科 | 副主任医师 | 陈晓波-正骨科-副主任医师-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 姚乃捷 | 84 | 正骨科 | 主任医师 | 姚乃捷-正骨科-主任医师-广东药科大学附属第一医院.jpg | 544008 | 684×1026 | `a38c92ed0a93b5d93385632f99810057fcfee3e2c37924c6d5f879f8d18c07a5` | 0 | https://www.gy120.net/files/20180104123037714.JPG |
| 赵晓 | 249 | 正骨科 | 副主任医师 | 赵晓-正骨科-副主任医师-广东药科大学附属第一医院.jpg | 592056 | 714×1071 | `7577b67e1b787f70bb92f1099787181f65d2d75ff30185a37126a0c1d6938c89` | 0 | https://www.gy120.net/files/20180104122900022.JPG |
| 林展 | 302 | 正骨科 | 医师 | 林展-正骨科-医师-广东药科大学附属第一医院.jpg | 1126022 | 1200×1800 | `f8d57848f497675f917ab716d77fd2c0da147448da88db10f8132304e1537e9a` | 0 | https://www.gy120.net/files/20150729083514875.JPG |
| 张福宏 | 531 | 耳鼻咽喉科 | 主任医师 | 张福宏-耳鼻咽喉科-主任医师-广东药科大学附属第一医院.jpg | 64478 | 357×535 | `add6228b0ed6db7611e2b15248c4578633fa2891b80b5582bd755153a2bca122` | 0 | https://www.gy120.net/files/20250922100847560.jpg |
| 姚良忠 | 137 | 耳鼻咽喉科 | 主任医师 | 姚良忠-耳鼻咽喉科-主任医师-广东药科大学附属第一医院.jpg | 575990 | 728×1092 | `f5123e3db264d6fc4b8764db455152fe94db44c3aadb77c9e325d46fb902923d` | 0 | https://www.gy120.net/files/20180104111640587.JPG |
| 潘智灵 | 193 | 耳鼻咽喉科 | 主任医师 | 潘智灵-耳鼻咽喉科-主任医师-广东药科大学附属第一医院.jpg | 552698 | 707×1061 | `c2f90fb5e18ed5937c9a19fc5edd2a0e988aafbd9c7e3e234b4197bf7e7c37e2` | 0 | https://www.gy120.net/files/20180104111508173.JPG |
| 左可军 | 532 | 耳鼻咽喉科 | 主任医师 | 左可军-耳鼻咽喉科-主任医师-广东药科大学附属第一医院.jpg | 39822 | 285×378 | `d3f508c668c3ce7630722bc05236993acca7c86b493020e7fd8dd8cdf7bebfaf` | 0 | https://www.gy120.net/files/20260128170250688.jpg |
| 刘俊捷 | 403 | 耳鼻咽喉科 | 副主任医师 | 刘俊捷-耳鼻咽喉科-副主任医师-广东药科大学附属第一医院.jpg | 1125510 | 1200×1800 | `e34b88b3e932b54f90b6e24fda0df5ea90a20fff860ad748c1b7c46451b23b58` | 0 | https://www.gy120.net/files/20190830171444880.JPG |
| 朱艳丽 | 401 | 耳鼻咽喉科 | 副主任医师 | 朱艳丽-耳鼻咽喉科-副主任医师-广东药科大学附属第一医院.jpg | 1063350 | 1200×1800 | `ddac940f7d93a0b4e58c09f1d94e1e6b59fdf8b64178af4b139bbdc10afd5f57` | 0 | https://www.gy120.net/files/20190830171546666.JPG |
| 党华 | 533 | 耳鼻咽喉科 | 副主任医师 | 党华-耳鼻咽喉科-副主任医师-广东药科大学附属第一医院.jpg | 36710 | 261×329 | `c702b9a6fd36bc495b0fc3ec9e5bc4a6ee2fe24e5c563482580fe1df24d135ae` | 0 | https://www.gy120.net/files/20260128170901670.jpg |
| 武俊男 | 534 | 耳鼻咽喉科 | 副主任医师 | 武俊男-耳鼻咽喉科-副主任医师-广东药科大学附属第一医院.jpg | 17112 | 285×378 | `e429930d63c7d88f48577f6df9e83db2c3c8be0993c2ca002ec16698a69350b5` | 0 | https://www.gy120.net/files/20260128171156706.jpg |
| 单孔荣 | 5 | 皮肤科 | 副主任医师 | 单孔荣-皮肤科-副主任医师-广东药科大学附属第一医院.jpg | 425260 | 619×928 | `55b3db754a6e942e63bc41155f90c83f85e46ac03ace45c6a114909d5fbdd48e` | 0 | https://www.gy120.net/files/20180104113646368.JPG |
| 罗丽芳 | 428 | 皮肤科 | 主治医师 | 罗丽芳-皮肤科-主治医师-广东药科大学附属第一医院.jpg | 93708 | 390×567 | `59a450a0117377d5018796e32cd4dfe96415e252317d2d44d1b35863043295ac` | 0 | https://www.gy120.net/files/20171204085948435.jpg |
| 宋燕平 | 330 | 皮肤科 | 医师 | 宋燕平-皮肤科-医师-广东药科大学附属第一医院.jpg | 27240 | 117×166 | `7c424b4fb13fac67c307d1822e37828c63249239c0ba932df42c03b6a9df3079` | 0 | https://www.gy120.net/files/20180719095824801.jpg |
| 洪敏 | 177 | 中医科 | 主任中医师 | 洪敏-中医科-主任中医师-广东药科大学附属第一医院.jpg | 481644 | 631×947 | `5494ea987b14a5635de43f46ed6c9e9c825f4c0d7493da8cd637ee61334a1a9d` | 0 | https://www.gy120.net/files/20180104123108083.JPG |
| 章伟明 | 178 | 中医科 | 主任中医师 | 章伟明-中医科-主任中医师-广东药科大学附属第一医院.jpg | 397676 | 599×898 | `385b2b0990a0d513c622121d13c5a5e3ba052ff474db68424fa5195eb7b8ca8b` | 0 | https://www.gy120.net/files/20180104123212331.JPG |
| 甄毅锋 | 195 | 中医科 | 副主任医师 | 甄毅锋-中医科-副主任医师-广东药科大学附属第一医院.jpg | 540764 | 702×1053 | `ea36a90786209948827ca2f5680f1ee97a9f91e4f6793836764e5b31cde64a4d` | 0 | https://www.gy120.net/files/20180104112650750.JPG |
| 邓晶晶 | 548 | 中医科 | 医学博士 | 邓晶晶-中医科-医学博士-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428202932288.jpg |
| 刘芳 | 549 | 中医科 | 未标注 | 刘芳-中医科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428203244040.jpg |
| 蒋平平 | 564 | 中医科 | 副主任医师 | 蒋平平-中医科-副主任医师-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 赵玮璇 | 565 | 中医科 | 副主任中医师 | 赵玮璇-中医科-副主任中医师-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 卢秉慧 | 311 | 中医科 | 副主任中医师 | 卢秉慧-中医科-副主任中医师-广东药科大学附属第一医院.jpg | 13436 | 76×115 | `573deabcce77a87c89b43699cf1f75c195285ae4e633882a087a433149fa0273` | 0 | https://www.gy120.net/files/20151209154018517.jpg |
| 王叶青 | 313 | 中医科 | 副主任中医师 | 王叶青-中医科-副主任中医师-广东药科大学附属第一医院.jpg | 58146 | 957×957 | `efa26ae9e75b608741120957b3ed3cf5ce20a315c54070b4f7a9f827cca38352` | 0 | https://www.gy120.net/files/20200115104249408.jpg |
| 叶龙霖 | 315 | 中医科 | 医师 | 叶龙霖-中医科-医师-广东药科大学附属第一医院.jpg | 24668 | 117×168 | `1a9a22fbbd5ee0dff1bdf692d6dffe7371b3f3c1f7a1382794d3736b5b29d8f8` | 0 | https://www.gy120.net/files/20180718114708085.jpg |
| 聂文强 | 407 | 中医科 | 医师 | 聂文强-中医科-医师-广东药科大学附属第一医院.jpg | 25706 | 117×170 | `b53ce72bbcfdd2f488dc3f5907f6f513f8538e4dc9a0749c5e11955afe73b079` | 0 | https://www.gy120.net/files/20180718114448383.jpg |
| 廖锐 | 463 | 中医科 | 医师 | 廖锐-中医科-医师-广东药科大学附属第一医院.jpg | 10490 | 325×433 | `06b1b47ca14bc747c08ba88bc01f72acc2f0c14823ff23e976676926daa82893` | 0 | https://www.gy120.net/files/20200115110055604.jpg |
| 黎子毓 | 469 | 中医科 | 医师 | 黎子毓-中医科-医师-广东药科大学附属第一医院.jpg | 105134 | 1080×1440 | `8970a0a86672ac7b147b5ff2393e1da3d3724d6c8231937530e2fbb36567bd9d` | 0 | https://www.gy120.net/files/20200827104417646.jpg |
| 张明兴 | 174 | 康复医学科 | 主任医师 | 张明兴-康复医学科-主任医师-广东药科大学附属第一医院.jpg | 561710 | 681×1021 | `d96057c1f94e9dabae3bec7c1338164b151d21e22d83660e8507a3f9dd95debf` | 0 | https://www.gy120.net/files/20190521165937060.JPG |
| 黄旭明 | 173 | 康复医学科 | 主任医师 | 黄旭明-康复医学科-主任医师-广东药科大学附属第一医院.jpg | 572268 | 700×1050 | `5f7cc7b5c93313cd174f2cb821b3c2f55b28ab727055383ff22181dccc7062c2` | 0 | https://www.gy120.net/files/20180104113325908.JPG |
| 石艺华 | 175 | 康复医学科 | 主任中医师 | 石艺华-康复医学科-主任中医师-广东药科大学附属第一医院.jpg | 595966 | 718×1077 | `3de767e1e4c10fab3fa122bf3faeecc87a605d41a6a6516cef7b6cc2825a8b3b` | 0 | https://www.gy120.net/files/20180104113348736.JPG |
| 王秀坤 | 176 | 康复医学科 | 副主任 | 王秀坤-康复医学科-副主任-广东药科大学附属第一医院.jpg | 517058 | 666×999 | `d278e9e230ce1d723045ff8a708c367230d1e3ea60e8dd8a1544d9b3827173bd` | 0 | https://www.gy120.net/files/20180104113415113.JPG |
| 单莎瑞 | 553 | 康复医学科 | 未标注 | 单莎瑞-康复医学科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428211929099.jpg |
| 洪峰 | 440 | 康复医学科 | 医师 | 洪峰-康复医学科-医师-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 宋海泳 | 559 | 康复医学科 | 未标注 | 宋海泳-康复医学科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 杨杏萍 | 554 | 康复医学科 | 博士 | 杨杏萍-康复医学科-博士-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 员凤英 | 555 | 康复医学科 | 未标注 | 员凤英-康复医学科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 曾垂魁 | 556 | 康复医学科 | 副主任医师 | 曾垂魁-康复医学科-副主任医师-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 周礼 | 557 | 康复医学科 | 未标注 | 周礼-康复医学科-未标注-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 王希成 | 24 | 肿瘤一科 | 主任医师 | 王希成-肿瘤一科-主任医师-广东药科大学附属第一医院.jpg | 231222 | 452×677 | `570d58beaa74452d54748a872b2a510238ac6ec779911f0272230a8322360346` | 0 | https://www.gy120.net/files/20230612092055691.JPG |
| 秦鑫添 | 337 | 肿瘤一科 | 副主任医师 | 秦鑫添-肿瘤一科-副主任医师-广东药科大学附属第一医院.jpg | 584222 | 682×1024 | `01932d4c97847730f960c8823016f552cb572e929623075871fe29e5c749ddc3` | 0 | https://www.gy120.net/files/20180104123532973.JPG |
| 丁颖 | 218 | 肿瘤一科 | 主任医师 | 丁颖-肿瘤一科-主任医师-广东药科大学附属第一医院.jpg | 198490 | 435×652 | `4ebed2fc6f95f7ce05d838351947fb9e6a1aa5322c133a4baa1af1eb9b8e1cfe` | 0 | https://www.gy120.net/files/20180104123311774.JPG |
| 杨帆 | 254 | 肿瘤一科 | 主任医师 | 杨帆-肿瘤一科-主任医师-广东药科大学附属第一医院.jpg | 544018 | 667×1001 | `f39393b9eb3585634e007de7a51ce8530362d41a99fbfbc3d679a57789597c24` | 0 | https://www.gy120.net/files/20180104123633628.JPG |
| 苏琼菲 | 393 | 肿瘤一科 | 主治医师 | 苏琼菲-肿瘤一科-主治医师-广东药科大学附属第一医院.jpg | 30928 | 117×175 | `037710810738834ab1927d4d102291a70fb10eb1ab454c4045c5a94a701cc0a3` | 0 | https://www.gy120.net/files/20180719102116146.jpg |
| 张琼霞 | 430 | 肿瘤一科 | 主治医师 | 张琼霞-肿瘤一科-主治医师-广东药科大学附属第一医院.jpg | 3557660 | 2067×2953 | `18a3619e953260933779b5051ffa5da91851fee398dd4ceb9433c69ee56f4b31` | 0 | https://www.gy120.net/files/20171218084247944.jpg |
| 曹燕青 | 493 | 肿瘤一科 | 未标注 | 曹燕青-肿瘤一科-未标注-广东药科大学附属第一医院.jpg | 2584 | 119×174 | `e96302a866e89bbef91a865e465158d325d9528e1046ee0e5c83b179d66b774e` | 0 | https://www.gy120.net/files/20230112210956665.jpg |
| 王哲 | 596 | 肿瘤一科 | 副主任医师 | 王哲-肿瘤一科-副主任医师-广东药科大学附属第一医院.jpg | 58180 | 250×350 | `a19ebfa7a38281823665e3ba1744a01e98327720fe477a35de09c8d3f1301c0f` | 0 | https://www.gy120.net/files/20260514203613060.JPG |
| 李玉齐 | 256 | 肿瘤一科 | 副主任医师 | 李玉齐-肿瘤一科-副主任医师-广东药科大学附属第一医院.jpg | 531296 | 701×1052 | `690bd85d39d1f2fefb8f92815526d3174d323d1f7286c0e9f463e8f7b9d09ad7` | 0 | https://www.gy120.net/files/20180104123338147.JPG |
| 杨曙 | 390 | 肿瘤二科 | 副主任医师 | 杨曙-肿瘤二科-副主任医师-广东药科大学附属第一医院.jpg | 525662 | 663×994 | `a9900630758896c8fd21efeb6e072baaf40a3fbd1a06c3d4658e8182020a5bfd` | 0 | https://www.gy120.net/files/20180104123704983.JPG |
| 舒阳春 | 252 | 肿瘤二科 | 副主任医师 | 舒阳春-肿瘤二科-副主任医师-广东药科大学附属第一医院.jpg | 443154 | 609×914 | `b47b871e5f10fd51a69f2c9655251244fcd6e31aa7b907013fa395ca4c01f6b7` | 0 | https://www.gy120.net/files/20180104123554533.JPG |
| 莫凯岚 | 395 | 肿瘤二科 | 副主任医师 | 莫凯岚-肿瘤二科-副主任医师-广东药科大学附属第一医院.jpg | 28628 | 117×175 | `154fe6a9d557982757d17481ec85f1ac0a8470b240bea451ca3c3c18edc8f4c0` | 0 | https://www.gy120.net/files/20180719101912250.jpg |
| 刘华 | 1 | 全科医学科 | 主任医师 | 刘华-全科医学科-主任医师-广东药科大学附属第一医院.jpg | 662192 | 763×1144 | `c69e345eb30f43b9dce6737499dd88c60a29571d27f2fea171fc3154a254c0bd` | 0 | https://www.gy120.net/files/20180104112218514.JPG |
| 徐丽梅 | 143 | 全科医学科 | 主任医师 | 徐丽梅-全科医学科-主任医师-广东药科大学附属第一医院.jpg | 550778 | 660×990 | `dafa9469eca11a590e3be2cf154dc0fd6ef6650d31ac8902e6286fb45b00aa75` | 0 | https://www.gy120.net/files/20180104112626782.JPG |
| 王晓军 | 142 | 全科医学科 | 主任医师 | 王晓军-全科医学科-主任医师-广东药科大学附属第一医院.jpg | 259528 | 468×703 | `8af77bd0a7faa888c30f646259983de250b6c28cfbb468689a5315093d9a1f4f` | 0 | https://www.gy120.net/files/20180104112522026.JPG |
| 石雁 | 170 | 全科医学科 | 主任医师 | 石雁-全科医学科-主任医师-广东药科大学附属第一医院.jpg | 472752 | 673×1009 | `77f84290cd4ef2d5508cd1ccfc2dfb6b643ffae94f48bcc9514d475f2955b9e8` | 0 | https://www.gy120.net/files/20180104112440844.JPG |
| 陈艳波 | 155 | 全科医学科 | 副主任医师 | 陈艳波-全科医学科-副主任医师-广东药科大学附属第一医院.jpg | 564886 | 696×1044 | `947a5a8c07980bc96c3047bd39c030d3b79da528abd226fcd3420e539623e8af` | 0 | https://www.gy120.net/files/20180104112319660.JPG |
| 郭雨青 | 194 | 全科医学科 | 副主任医师 | 郭雨青-全科医学科-副主任医师-广东药科大学附属第一医院.jpg | 547620 | 698×1046 | `c2ae80945d2b2cbbf08b80494da78fc8ff6561097966aaae4212a5bd3c4be768` | 0 | https://www.gy120.net/files/20180104112340160.JPG |
| 张晓妹 | 408 | 全科医学科 | 主治医师 | 张晓妹-全科医学科-主治医师-广东药科大学附属第一医院.jpg | 29426 | 117×175 | `556891e45e71ff0f3627de00406af88e69af34b6a1566b0051ef43352cb55a33` | 0 | https://www.gy120.net/files/20180719102351039.jpg |
| 李晓华 | 584 | 全科医学科 | 副主任医师 | 李晓华-全科医学科-副主任医师-广东药科大学附属第一医院.jpg | 62694 | 250×350 | `d1eb95214472a43ef8fed06db81d1bab1f51b42023c4137034a97341c6c503c7` | 0 | https://www.gy120.net/files/20260514202214738.JPG |
| 劳志刚 | 19 | 重症医学科 | 主任医师 | 劳志刚-重症医学科-主任医师-广东药科大学附属第一医院.jpg | 747892 | 1034×1551 | `adb10a91e7a2481f105cb8f1035a60d7d9686ca458df1fa016579a858f14298d` | 0 | https://www.gy120.net/files/20180104125735086.jpg |
| 茹晃耀 | 268 | 重症医学科 | 副主任医师 | 茹晃耀-重症医学科-副主任医师-广东药科大学附属第一医院.jpg | 1038542 | 1200×1800 | `5f9b821044202d08011acd79bcfb3d9527a9e240d1477802f1bf060537ba52ba` | 0 | https://www.gy120.net/files/20210719092937287.JPG |
| 王素宁 | 270 | 重症医学科 | 主治医师 | 王素宁-重症医学科-主治医师-广东药科大学附属第一医院.jpg | 1124862 | 1200×1800 | `dadafc9a777b572d67ae169e4b8cd0d8d003254ad89f21526ba5f8f2904c26c9` | 0 | https://www.gy120.net/files/20150729083800410.JPG |
| 吴昊 | 271 | 重症医学科 | 主治医师 | 吴昊-重症医学科-主治医师-广东药科大学附属第一医院.jpg | 1252566 | 1200×1800 | `0871131008261e0aad809c3867a6ec2f72a08c929e03ced9719f25a44965ec66` | 0 | https://www.gy120.net/files/20150729083913261.JPG |
| 陈建颜 | 475 | 麻醉科 | 主任医师 | 陈建颜-麻醉科-主任医师-广东药科大学附属第一医院.jpg | 2041282 | 1750×2450 | `2b435ae5e9d99715249e72cf3f855dc6cbd93654521f32f7c059100b4926d5af` | 0 | https://www.gy120.net/files/20210816144835535.jpg |
| 蔡杰衡 | 48 | 麻醉科 | 主任医师 | 蔡杰衡-麻醉科-主任医师-广东药科大学附属第一医院.jpg | 2090716 | 1750×2450 | `60899743c65aba7756e7deee88bdf61a7493580985e3cc1a24bf58cac89a815d` | 0 | https://www.gy120.net/files/20210816150324302.jpg |
| 马翔 | 185 | 麻醉科 | 副主任医师 | 马翔-麻醉科-副主任医师-广东药科大学附属第一医院.jpg | 1963522 | 1750×2450 | `11964382f82c2fb1ab05db4229dd8ee660c47353dac04bf57d423456c6a7ff7e` | 0 | https://www.gy120.net/files/20210816150253282.jpg |
| 陈志峰 | 187 | 麻醉科 | 副主任医师 | 陈志峰-麻醉科-副主任医师-广东药科大学附属第一医院.jpg | 2060754 | 1750×2450 | `8bc171bf0c9a96cd38a1a0c201c01d87044088d1677230b8316449c01817ca32` | 0 | https://www.gy120.net/files/20210816150212361.jpg |
| 陈宗 | 476 | 麻醉科 | 副主任医师 | 陈宗-麻醉科-副主任医师-广东药科大学附属第一医院.jpg | 1997108 | 1750×2450 | `21b06d79471b57c83ab8281c5e3cd0812bcfe083184bb59b9782b230e8b6c8f6` | 0 | https://www.gy120.net/files/20210816145844190.jpg |
| 吴志镇 | 188 | 麻醉科 | 主治医师 | 吴志镇-麻醉科-主治医师-广东药科大学附属第一医院.jpg | 2051192 | 1750×2450 | `25220276e8e622281ce71dd6377789c10234a5b2074411752eb4dcb0dd76e5c5` | 0 | https://www.gy120.net/files/20210816150042617.jpg |
| 李洁 | 477 | 麻醉科 | 主治医师 | 李洁-麻醉科-主治医师-广东药科大学附属第一医院.jpg | 1859042 | 1750×2450 | `037cea9769967a111b90725aef361dab8513a9948e70a66c16d3ff11e8586bef` | 0 | https://www.gy120.net/files/20210816150450215.jpg |
| 苏一冬 | 321 | 麻醉科 | 主治医师 | 苏一冬-麻醉科-主治医师-广东药科大学附属第一医院.jpg | 2003882 | 1750×2450 | `78b375f12affde3caa97e1d14c0347bff398ea35c443ff5981e6d93e0ef74dc9` | 0 | https://www.gy120.net/files/20210816151041332.jpg |
| 周巧梅 | 607 | 麻醉科 | 副主任医师 | 周巧梅-麻醉科-副主任医师-广东药科大学附属第一医院.jpg | 61558 | 250×350 | `d6960bb47d9a5f2fb20e9e2241ef0e69d3d865cf21aa8598921350a6734b2f10` | 0 | https://www.gy120.net/files/20260514205314262.JPG |
| 陆崇 | 253 | 健康管理部 | 副主任医师 | 陆崇-健康管理部-副主任医师-广东药科大学附属第一医院.jpg | 218628 | 452×679 | `174b58d371ca58a489f35cdd5313d58186f5dcffe818c3c3ad0e65fee7f4a3a7` | 0 | https://www.gy120.net/files/20180104120157918.JPG |
| 吴一平 | 67 | 健康管理部 | 副主任医师 | 吴一平-健康管理部-副主任医师-广东药科大学附属第一医院.jpg | 812516 | 1034×1551 | `653eb59ff7f20e55b47d74abe9642ab784843903af0d21fea8b4555f356598fc` | 0 | https://www.gy120.net/files/20180104124242268.jpg |
| 梁葳 | 232 | 健康管理部 | 副主任医师 | 梁葳-健康管理部-副主任医师-广东药科大学附属第一医院.jpg | 17994 | 250×350 | `96051ee668ebddce7b0d0a379bb6cc3d35341256b81cc815ff56d986e7b3f802` | 0 | https://www.gy120.net/files/20260512214748054.jpg |
| 李远添 | 426 | 静脉导管护理门诊 | 未标注 | 李远添-静脉导管护理门诊-未标注-广东药科大学附属第一医院.jpg | 98422 | 240×360 | `9ede96a921909dba43621aa84df212516e7121534c34d51bf25dda0f5863b8b9` | 0 | https://www.gy120.net/files/20171030171416535.jpg |
| 朱洁桃 | 604 | 静脉导管护理门诊 | 未标注 | 朱洁桃-静脉导管护理门诊-未标注-广东药科大学附属第一医院.jpg | 18386 | 250×350 | `1993a7f9db80d81b3f2e3b323703341f342b476974877edf6d6b1bdde9c6aa7d` | 0 | https://www.gy120.net/files/20260512212353586.JPG |
| 吴红卫 | 171 | 药学部 | 教授 | 吴红卫-药学部-教授-广东药科大学附属第一医院.jpg | 223748 | 430×645 | `5880cc928cf56148fd28281d42131840bfcee0d270250f755ae7fa90c2448bb0` | 0 | https://www.gy120.net/files/20180104121635300.JPG |
| 陈吉生 | 133 | 药学部 | 教授 | 陈吉生-药学部-教授-广东药科大学附属第一医院.jpg | 245922 | 469×704 | `a36bb449c1f49c2e2bbae58e3da4ca8389e0427253b3eb8c679a7ebdda054e39` | 0 | https://www.gy120.net/files/20180104121313245.JPG |
| 杨泽民 | 122 | 药学部 | 教授 | 杨泽民-药学部-教授-广东药科大学附属第一医院.jpg | 562494 | 709×1064 | `4168ea5cee878c2ec3bbc7b7cb8aedf5a12232a7fdb5a30b34084d1f6da55402` | 0 | https://www.gy120.net/files/20180104121933363.JPG |
| 陈永 | 263 | 药学部 | 教授 | 陈永-药学部-教授-广东药科大学附属第一医院.jpg | 559610 | 712×1068 | `44c47025abda392ebb26fac7c9e6f80833fee1969655edf2f85738160fc718be` | 0 | https://www.gy120.net/files/20180104121335488.JPG |
| 仇志坤 | 487 | 药学部 | 副主任 | 仇志坤-药学部-副主任-广东药科大学附属第一医院.jpg | 164042 | 676×1036 | `2fd00a495a6b9a836cc1808b71a7c269d05e7d2f2629113b773358706383176b` | 0 | https://www.gy120.net/files/20220914173305762.jpg |
| 沈勇刚 | 262 | 药学部 | 副教授 | 沈勇刚-药学部-副教授-广东药科大学附属第一医院.jpg | 541542 | 687×1031 | `d2fa09d0e47e376339bd75cbb5a9f12d34e816896ea69b1440a9e50363ff0777` | 0 | https://www.gy120.net/files/20180104121401559.JPG |
| 袁少筠 | 239 | 药学部 | 未标注 | 袁少筠-药学部-未标注-广东药科大学附属第一医院.jpg | 529348 | 679×1018 | `8e731f9ecae7f293b5ec4a627a4c53c5a7aeafeaac7f54e740b9f6f95243f8df` | 0 | https://www.gy120.net/files/20180104122210385.JPG |
| 陈碧珊 | 299 | 药学部 | 副主任 | 陈碧珊-药学部-副主任-广东药科大学附属第一医院.jpg | 1126754 | 1200×1800 | `ef3fbd17c168ebe23bd4574eb67ca713a489208496994bd5124459d1f549f855` | 0 | https://www.gy120.net/files/20150729101111395.JPG |
| 吴荣佳 | 570 | 药学部 | 副主任 | 吴荣佳-药学部-副主任-广东药科大学附属第一医院.jpg | 17838 | 250×350 | `7418bc64901b4adf9ab571537bae45c98864dc9207a6ce7711c9a3e2dbfef028` | 0 | https://www.gy120.net/files/20260512214541061.jpg |
| 关石凤 | 571 | 药学部 | 副主任 | 关石凤-药学部-副主任-广东药科大学附属第一医院.jpg | 25350 | 250×356 | `b3c7e9bc90f0fd48e5a6ada817cfa5068f1f717a6804514f6b9bd482abd754a4` | 0 | https://www.gy120.net/files/20260703221139347.jpg |
| 赖莎 | 300 | 药学部 | 副主任 | 赖莎-药学部-副主任-广东药科大学附属第一医院.jpg | 30132 | 117×175 | `2a47448d3d71e5eb6ba679c487e5c6016d4ded23743da97d22cfafc3321bbc76` | 0 | https://www.gy120.net/files/20180719103611634.jpg |
| 陈慧 | 572 | 药学部 | 副主任医师 | 陈慧-药学部-副主任医师-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 李艳 | 301 | 药学部 | 未标注 | 李艳-药学部-未标注-广东药科大学附属第一医院.jpg | 26310 | 110×165 | `5df588bc5b282c92ed945275e1575793147bd3ebb31e9f6cdfa9954f764e4a19` | 0 | https://www.gy120.net/files/20180301115443779.jpg |
| 马立恒 | 242 | 医学影像科 | 主任医师 | 马立恒-医学影像科-主任医师-广东药科大学附属第一医院.jpg | 493282 | 628×942 | `981aa03ea23a2a21656061f93931d4555d3f4680ca6e1c086c8379ade74caaca` | 0 | https://www.gy120.net/files/20180104122315762.JPG |
| 曾文彦 | 225 | 医学影像科 | 副主任医师 | 曾文彦-医学影像科-副主任医师-广东药科大学附属第一医院.jpg | 261084 | 487×730 | `a647a0c27b2dd872fad5e24d5f97516504acf3aa2ec87a257f33373602c6cf1d` | 0 | https://www.gy120.net/files/20180104122255966.JPG |
| 庄娘妥 | 226 | 医学影像科 | 副主任医师 | 庄娘妥-医学影像科-副主任医师-广东药科大学附属第一医院.jpg | 252690 | 465×699 | `ef04c7b7583d9346e13921b9ace6599a93bef5a5a4408f016e5bf73a0f619ebc` | 0 | https://www.gy120.net/files/20180104122527867.JPG |
| 杨清华 | 240 | 医学影像科 | 副主任医师 | 杨清华-医学影像科-副主任医师-广东药科大学附属第一医院.jpg | 643442 | 757×1135 | `4d5a1a7098586aef05c46498798b8e13ee1688af940fa66f66ad0b17c7ab6780` | 0 | https://www.gy120.net/files/20180104122506679.JPG |
| 罗武 | 389 | 医学影像科 | 副主任医师 | 罗武-医学影像科-副主任医师-广东药科大学附属第一医院.jpg | 713390 | 1034×1551 | `9278c317888f8dcae4b250666bf2b18af8f3ce33e242a12fca397621d1b6f0a4` | 0 | https://www.gy120.net/files/20180104124102216.jpg |
| 李琼华 | 592 | 医学影像科 | 未标注 | 李琼华-医学影像科-未标注-广东药科大学附属第一医院.jpg | 57140 | 250×350 | `c0ed6ada400eeae3dc4d6b30272d23d9695261090453a4a5b29cdc7053b7dbc9` | 0 | https://www.gy120.net/files/20260514203453544.JPG |
| 丁彩屏 | 42 | 检验科 | 主任医师 | 丁彩屏-检验科-主任医师-广东药科大学附属第一医院.jpg | 31398 | 160×240 | `8f41bb222d6f2406e5fc3ceeb9174a848da2d64fb4ae019814897640c0b46cd1` | 0 | https://www.gy120.net/upsfile/丁彩萍.jpg |
| 杨小蓉 | 351 | 检验科 | 副教授 | 杨小蓉-检验科-副教授-广东药科大学附属第一医院.jpg | 1203382 | 1645×2467 | `2e86de1eab553d86f7503448cc474e76477ff31199470fafc19481eebedf7b3f` | 0 | https://www.gy120.net/files/20180105121953842.jpg |
| 李瑞莹 | 537 | 检验科 | 副教授 | 李瑞莹-检验科-副教授-广东药科大学附属第一医院.jpg | 40126 | 351×460 | `ac877b5c4a399fb20f3d42c7b2354da52026d9de93a1d3e445e1c27970f57e42` | 0 | https://www.gy120.net/files/20260422213727998.jpg |
| 刘思敏 | 538 | 检验科 | 副主任 | 刘思敏-检验科-副主任-广东药科大学附属第一医院.jpg | 32284 | 351×460 | `79ac19a39362f2b3419353945fa274e4aad73fb40a85dad48ffcb24d07b66daf` | 0 | https://www.gy120.net/files/20260422214531552.jpg |
| 卢汉威 | 539 | 检验科 | 副教授 | 卢汉威-检验科-副教授-广东药科大学附属第一医院.jpg | 41706 | 351×460 | `8ee4bb43077f4d3765d4f3c25ebcbd35ca25e01ff6881359b5d2e1704540e68c` | 0 | https://www.gy120.net/files/20260423201716585.jpg |
| 卢景辉 | 540 | 检验科 | 副教授 | 卢景辉-检验科-副教授-广东药科大学附属第一医院.jpg | 42196 | 351×460 | `a5bcb882d16a9f350de7ae48ffdf014f0dd4458aa1e23e8970c2c90269b65578` | 0 | https://www.gy120.net/files/20260423202055170.jpg |
| 马晓桂 | 541 | 检验科 | 副教授 | 马晓桂-检验科-副教授-广东药科大学附属第一医院.jpg | 39780 | 351×460 | `cbdd046e17fbc9c11d42a86b5536c40d11aa3eccd9b3a5a86e7e79488a663de2` | 0 | https://www.gy120.net/files/20260423202523891.jpg |
| 张涛 | 542 | 检验科 | 副教授 | 张涛-检验科-副教授-广东药科大学附属第一医院.jpg | 42366 | 351×460 | `bb9ecc0d8fac0a20b77a8f4d2cef3a9f7ab7f6ac409a03a71d135ecf39628a1f` | 0 | https://www.gy120.net/files/20260423202843988.jpg |
| 徐晓松 | 562 | 检验科 | 副主任 | 徐晓松-检验科-副主任-广东药科大学附属第一医院.jpg | 30284 | 250×333 | `1f7a7e1ae76878de81288c2a9a1350de93f9efcd28e84e93de54f97c72819218` | 0 | https://www.gy120.net/files/20260705141946929.jpg |
| 黄演婷 | 543 | 检验科 | 副主任 | 黄演婷-检验科-副主任-广东药科大学附属第一医院.jpg | 47790 | 351×460 | `16ad4488924da0e45c909f64098fb1032fe4228570e224838c9c8d285e564316` | 0 | https://www.gy120.net/files/20260423203057568.jpg |
| 秦建川 | 544 | 检验科 | 副主任 | 秦建川-检验科-副主任-广东药科大学附属第一医院.jpg | 53332 | 351×460 | `35d73fb76321f1b838e0d1fb4fb5f22df540686c399734ac1439296fd4657db7` | 0 | https://www.gy120.net/files/20260423203310475.jpg |
| 官煜彬 | 563 | 检验科 | 副主任 | 官煜彬-检验科-副主任-广东药科大学附属第一医院.jpg | 25916 | 250×356 | `f4d054ae5cc60474b62cab06baadd46ee524db0012a1cdc9f40d587a3922fe07` | 0 | https://www.gy120.net/files/20260705142607510.jpg |
| 钟亮尹 | 353 | 检验科 | 副主任 | 钟亮尹-检验科-副主任-广东药科大学附属第一医院.jpg | 1204002 | 1200×1800 | `fe2fae5b666e72f7a55c1f753fd2588fc132b1cfd036f884a5a6d55516e1e5ca` | 0 | https://www.gy120.net/files/20150729105957417.JPG |
| 陈林珍 | 348 | 检验科 | 未标注 | 陈林珍-检验科-未标注-广东药科大学附属第一医院.jpg | 1050984 | 1200×1800 | `c5ebeb9c28111f6c78c775514c340e258d053306fd74b91fc5a50dad6be878d0` | 0 | https://www.gy120.net/files/20150729105009687.JPG |
| 冯红梅 | 350 | 检验科 | 副主任 | 冯红梅-检验科-副主任-广东药科大学附属第一医院.jpg | 1173632 | 1200×1800 | `b79452f4212ad8b10cb551f0722db8e6f6f862a6d49542c6d187deb3fe521323` | 0 | https://www.gy120.net/files/20150729105358264.JPG |
| 余佩芝 | 352 | 检验科 | 未标注 | 余佩芝-检验科-未标注-广东药科大学附属第一医院.jpg | 1238938 | 1200×1800 | `2247ddd19c1ded71f54956eba6dbac056a6903b199bdd13ac41b7bdd9da1add4` | 0 | https://www.gy120.net/files/20150729105731834.JPG |
| 陈少莲 | 349 | 检验科 | 副主任 | 陈少莲-检验科-副主任-广东药科大学附属第一医院.jpg | 1184510 | 1200×1800 | `dd095b54e7133e22be74c40f1af2e13c03ed89d79c96485c42365fb36a2fa140` | 0 | https://www.gy120.net/files/20150729105059404.JPG |
| 杨宁 | 190 | 病理科 | 副主任医师 | 杨宁-病理科-副主任医师-广东药科大学附属第一医院.jpg | 600032 | 721×1081 | `c310a0f3a3b9336d34c78d93c3c2e23f6ea8ede9cb288aa71fd7bd97f8a51d9f` | 0 | https://www.gy120.net/files/20180104110846788.JPG |
| 潘斌才 | 600 | 病理科 | 主任医师 | 潘斌才-病理科-主任医师-广东药科大学附属第一医院.jpg | 15990 | 211×300 | `0b20e4aa62f0bdcd0c42ae37c3ba1c262c7c478768cb2a632835f59a49d8a3eb` | 0 | https://www.gy120.net/files/20260608213436980.jpg |
| 李红 | 191 | 病理科 | 副主任医师 | 李红-病理科-副主任医师-广东药科大学附属第一医院.jpg | 489574 | 673×1009 | `9536fe4e1d3896d931e7416491aebd49c53c2e111af12f9b90fddd1a3b257552` | 0 | https://www.gy120.net/files/20180104110822587.JPG |
| 宋玉兰 | 601 | 病理科 | 未标注 | 宋玉兰-病理科-未标注-广东药科大学附属第一医院.jpg | 58568 | 250×350 | `5d8ecf02ed750ead9a2ce8eb0faa4747b883066d3d19ad7b301d5c30e1109a8c` | 0 | https://www.gy120.net/files/20260514204609554.jpg |
| 杨焰 | 361 | 物检科 | 主任医师 | 杨焰-物检科-主任医师-广东药科大学附属第一医院.jpg | 1203720 | 1645×2467 | `5a68291d6bb968eca93f04707bd6e81a68988e9f0d4830c1063e351220e18198` | 0 | https://www.gy120.net/files/20180105121929937.jpg |
| 黄密伶 | 362 | 物检科 | 副主任医师 | 黄密伶-物检科-副主任医师-广东药科大学附属第一医院.jpg | 454084 | 1200×1800 | `974f4c5b25e27755f4f7b22516188883c1ede1235e3a62b1de87674cfd6d7781` | 0 | https://www.gy120.net/files/20150730083705618.JPG |
| 余瑾 | 594 | 物检科 | 副主任医师 | 余瑾-物检科-副主任医师-广东药科大学附属第一医院.jpg | 67126 | 250×350 | `e322e27e20716ebbc4620c6a24558e297ebfdc3edf8ba40b6ae18a511b2e8851` | 0 | https://www.gy120.net/files/20260514205126862.jpg |
| 陈虹 | 356 | 物检科 | 主治医师 | 陈虹-物检科-主治医师-广东药科大学附属第一医院.jpg | 29228 | 117×175 | `74d51a53883326542bef8992d859e38b6fb102c32782d62fc39e61f5b5e3c857` | 0 | https://www.gy120.net/files/20180719104440003.jpg |
| 金文敏 | 358 | 物检科 | 主治医师 | 金文敏-物检科-主治医师-广东药科大学附属第一医院.jpg | 1091142 | 1200×1800 | `bc8d184d53068a492462183b4ff028e8a9713d745a9034587b0dc23bcd38da5e` | 1 | https://www.gy120.net/files/20150730082737226.JPG |
| 钟华 | 359 | 物检科 | 副主任医师 | 钟华-物检科-副主任医师-广东药科大学附属第一医院.jpg | 52690 | 751×748 | `1736e00b53526405e2be5e781481a65924dd286ecab9eb853a6b68c4d9f631d8` | 0 | https://www.gy120.net/files/20230214104805597.jpg |
| 严冬梅 | 360 | 物检科 | 主治医师 | 严冬梅-物检科-主治医师-广东药科大学附属第一医院.jpg | 1166834 | 1200×1800 | `cf33a8a4a659592561cc1bc566e349b488912d5b33c2381c2d708ebbcdde9d49` | 0 | https://www.gy120.net/files/20150730083243945.JPG |
| 沈建红 | 484 | 物检科 | 副主任医师 | 沈建红-物检科-副主任医师-广东药科大学附属第一医院.jpg | 18564 | 260×378 | `2633ef7cd5b854b7d0192eb596331759704483cd83eee2553ce0dfc37b8ec074` | 0 | https://www.gy120.net/files/20220407112143895.jpg |
| 赵泳谊 | 258 | 临床营养科 | 主任医师 | 赵泳谊-临床营养科-主任医师-广东药科大学附属第一医院.jpg | 430580 | 607×911 | `ed6422ebf6a6463c9045660f0f0e8e31efcbcd7177e8d549126415749afaf34b` | 0 | https://www.gy120.net/files/20180104122552284.JPG |
| 林伟群 | 589 | 临床营养科 | 副主任医师 | 林伟群-临床营养科-副主任医师-广东药科大学附属第一医院.jpg | 17180 | 211×300 | `7ddf8b4e9c6541f409212640ec8fdacc730d77ebc76a3df9c92f464a0c2558ae` | 0 | https://www.gy120.net/files/20260428212134003.jpg |
| 刘翠冰 | 259 | 临床营养科 | 未标注 | 刘翠冰-临床营养科-未标注-广东药科大学附属第一医院.jpg | 48181 | 160×240 | `369f3328e35ce631a97f15587f08413e95ab73e2d0efd7fb8dd766d8cff9e2a6` | 0 | https://www.gy120.net/files/20141014100811856.JPG |
| 欧俏文 | 260 | 临床营养科 | 主治医师 | 欧俏文-临床营养科-主治医师-广东药科大学附属第一医院.jpg | 11104 | 117×175 | `e9b649cbe7a15ab4085bd3d77e8c2a02ca12ac20407ad7955ee4eba86d7c12c2` | 0 | https://www.gy120.net/files/20160122145920109.jpg |
| 袁建伟 | 345 | 核医学科 | 主任医师 | 袁建伟-核医学科-主任医师-广东药科大学附属第一医院.jpg | 534266 | 670×1005 | `d09fe2e9b12eea0c06b8bff0d5c45549c91c9a12cd0f6fa8b4267435269d7691` | 0 | https://www.gy120.net/files/20180104113029988.JPG |
| 刘雄英 | 272 | 核医学科 | 副主任医师 | 刘雄英-核医学科-副主任医师-广东药科大学附属第一医院.jpg | 1143310 | 1200×1800 | `17064375d19e5f0dcd07d85a7f941f6ff392d304b0bea8a73057099d41652072` | 0 | https://www.gy120.net/files/20150720091044493.JPG |
| 陈桐生 | 273 | 核医学科 | 主治医师 | 陈桐生-核医学科-主治医师-广东药科大学附属第一医院.jpg | 422946 | 1200×1800 | `7cfd24f859838150a3600b010037a4be5c905f311dae9cb4ee64a084bf3ff16b` | 0 | https://www.gy120.net/files/20150729083319598.JPG |

### 管理员批准的连续两次失败留空标注

| 姓名 | ArticleID | 详情 Referer | 官网照片 | 两次结果 | 处置 |
|---|---|---|---|---|---|
| 臧晶 | 587 | https://www.gy120.net/articleshow.asp?articleid=587 | https://www.gy120.net/files/20260514205657708.JPG | HTTP 404；HTTP 404 | 官网本人职业照连续两次获取失败，按管理员裁决留空 |
| 周玉婷 | 593 | https://www.gy120.net/articleshow.asp?articleid=593 | https://www.gy120.net/files/20260514205726492.JPG | HTTP 404；HTTP 404 | 官网本人职业照连续两次获取失败，按管理员裁决留空 |


## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| https://www.gy120.net/zhuanjia.asp | 护师，国际造口治疗师 | https://www.gy120.net/articleshow.asp?articleid=404 | 官网详情专业职称明确为纯护理身份，按医生画像范围排除 |
| https://www.gy120.net/zhuanjia.asp | 副主任护师，血液内科护士长/静疗专科组长 | https://www.gy120.net/articleshow.asp?articleid=603 | 官网详情专业职称明确为纯护理身份，按医生画像范围排除 |

## 输出文件

- Excel 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx`
- CSV 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 4 |
| 原始医生卡片记录 | 407 |
| 跨入口去重前候选关系 | 349 |
| 跨入口去重后唯一候选 | 349 |
| 排除非医生候选 | 2 |
| 合规医生详情页 | 347 |
| 最终医生身份 | 340 |
| 覆盖科室数 | 115 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 67 |
| 慢性病 | 114 |
| 术后恢复/康复 | 78 |
| 生殖疾病 | 26 |
| 疑难重症 | 93 |
| 肿瘤 | 117 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 检验科 | 17 |
| 口腔科 | 16 |
| 消化内科 | 13 |
| 中医科 | 13 |
| 药学部 | 13 |
| 康复医学科 | 12 |
| 泌尿外科 | 11 |
| 妇产科 | 11 |
| 神经外科 | 9 |
| 创伤与关节外科（骨一科） | 9 |
| 急诊科 | 9 |
| 眼科 | 9 |
| 肿瘤一科 | 9 |
| 麻醉科 | 9 |
| 物检科 | 9 |
| 呼吸与危重症医学科 | 8 |
| 内分泌科 | 8 |
| 神经内科(头痛门诊) | 8 |
| 中西医结合代谢病科 | 8 |
| 耳鼻咽喉科 | 8 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 职称/身份需人工复核 | 23 |
| 详情正文为空或未识别 | 5 |
| 同名待甄别 | 14 |
| 官网正文私用区字符已清洗 | 1 |
| 官网本人职业照连续两次获取失败，按管理员裁决留空 | 2 |

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
