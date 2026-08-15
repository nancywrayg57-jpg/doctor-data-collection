---
类型: 自动采集试跑报告
医院: 广东药科大学附属第一医院
城市: 广州市
采集日期: 2026-08-15
来源范围: 医院官网
采集入口: https://www.gy120.net/zhuanjia.asp
适配器: gy120_asp_department_expert_photo
---

# 广东药科大学附属第一医院 官方医生自动采集试跑报告

## 结论

本次试采只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集试采底表，共 10 位唯一医生；官网列表页原始卡片记录 407 条；读取入口分类 4 个；覆盖 10 个科室；详情页失败 0 条。

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
- 有姓名详情 ID：10 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：10 个
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
- 试采覆盖入口分类：2 个（内科、外科）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 无 | 无 | 无 |

## 广东药科大学附属第一医院推荐区、科室树、编码与照片试采对账

- 官网旧版 ASP 单页目录：推荐区 58 次 / 56 个唯一 ArticleID；角色 首席专家=14、科室负责人=44；全部与科室树重叠 58 次。
- 科室树：57 个科室，其中空科室 3 个；医生—科室关系 / 唯一数字 ArticleID：349 / 349。
- 详情顺序公开 GET：成功 349，失败 0；纯护理身份排除 2，合规候选 347。
- 试采固定 10 位：覆盖科室 10 个（内分泌科（共和门诊）、呼吸与危重症医学科（健康管理中心）、心内一科（健康管理中心）、心内二科（健康管理中心）、普外一科（肝胆外科）、消化内科（健康管理中心）、肥胖专病治疗组（健康管理中心）、肾内科（健康管理中心）、血液内科、风湿免疫科（健康管理中心））；首席专家 4、科室负责人 5、非推荐医生 2。
- 公开出诊点标签普查：健康管理中心=159、农林门诊=80、共和门诊=34；多出诊点详情 26 个。仅保留官网明确地点标签，不采集日期、星期、上午/下午等排班时段。
- 编码自检：响应头无 charset、meta 错标 UTF-8；按现场字节严格 GB18030/GBK 解码；替换字符 0、高置信乱码标记 0、列表/详情姓名不一致 0。
- 详情清洗：排班正式字段写入 0，排名/患者片段排除 0，患者案例排除 0，私用区字符 0。
- 照片普查：本人职业照 346、占位图 0、空图 0、拒绝路径 1。
- 照片四数：应采 10 / 实采 10 / 连续两次失败留空 0 / 无照片 0；本轮触发单次重试 0 张。
- 照片传输策略：同一官方图片 URL + 同一公开详情页 Referer + 同一请求头；首次 HTTP 非 200 或 Timeout/ConnectionError/ChunkedEncodingError/IncompleteRead 后等待 1 秒，仅重试 1 次；不注入 Cookie、不绕过验证；连续两次失败则留空并标注；原图不压缩；平均 547328 bytes，估算 346 张 / 189375488 bytes，大图阈值命中 8 张。
- 普通公开会话：requests 常规公开 GET；图片仅携带同域公开详情页 Referer，失败时保持 URL/Referer/请求头不变并等待 1 秒重试一次；未注入 Cookie、未绕过登录/验证码/挑战，未访问非公开接口；最终 Cookie 名称仅留痕为 `ASPSESSIONIDAGQCTAAC、mycookie`。当前仍为 TRIAL，严禁写总底表或生成正式 Obsidian 画像。

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
| 42 | 丁彩屏 | 丁彩屏 | 医技 | 检验科 | 检验科 | 官网详情未标注 | 教授、主任医师、硕士生导师 | rejected | 详情已读取 | https://www.gy120.net/articleshow.asp?articleid=42 |
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

### 试采照片字节、魔数、SHA-256、尺寸及重试对账

| 姓名 | ArticleID | 科室 | 主职称 | 文件名 | 字节数 | 宽×高 | SHA-256 | 重试次数 | 官网照片 |
|---|---|---|---|---|---:|---:|---|---:|---|
| 周万兴 | 75 | 心内一科 | 主任医师 | 周万兴-心内一科-主任医师-广东药科大学附属第一医院.jpg | 350856 | 1507×2010 | `a1d4aead3d2f2b0b661898109787272b9832977879e5b1845cba15de24f402c2` | 0 | https://www.gy120.net/files/20180104110230278.jpg |
| 曾智桓 | 139 | 心内二科 | 主任医师 | 曾智桓-心内二科-主任医师-广东药科大学附属第一医院.jpg | 489760 | 715×1072 | `dd7b918d5481478d92076bbf1a915c8aa560a28cd24e2a378bd4b7b9e1fdabba` | 0 | https://www.gy120.net/files/20180104120656967.JPG |
| 叶美莲 | 115 | 血液内科 | 主任医师 | 叶美莲-血液内科-主任医师-广东药科大学附属第一医院.jpg | 1277038 | 1645×2467 | `200b2f9390cd4d35f0150b69ba1c95fdfb1371ebddd5e01223936783b5cb90dc` | 0 | https://www.gy120.net/files/20180104124306593.jpg |
| 袁伟锋 | 40 | 呼吸与危重症医学科 | 主任医师 | 袁伟锋-呼吸与危重症医学科-主任医师-广东药科大学附属第一医院.jpg | 18414 | 170×227 | `1aebca1aed82d83f7645ca2ffa7f79ad629d42f9c925f80aa51371559d394b26` | 0 | https://www.gy120.net/files/20240830083641469.jpg |
| 吕路 | 209 | 肾内科 | 主任医师 | 吕路-肾内科-主任医师-广东药科大学附属第一医院.jpg | 379258 | 663×995 | `04fe02e4bb76e38e2e2a41f13051702bca1dca21a88b973e7d8645cfe9f36e82` | 0 | https://www.gy120.net/files/20180104120031498.JPG |
| 叶健华 | 53 | 内分泌科 | 主任医师 | 叶健华-内分泌科-主任医师-广东药科大学附属第一医院.jpg | 255646 | 478×716 | `46860b2b716d6aef838c629cf4adf6a7736dfcbee79cfab6e8d65b0bad280cc0` | 0 | https://www.gy120.net/files/20180104114120442.JPG |
| 何兴祥 | 156 | 消化内科 | 主任医师 | 何兴祥-消化内科-主任医师-广东药科大学附属第一医院.jpg | 692572 | 1473×1964 | `f84f1be675b71c326eade53bf4c3de259ddf6e573bf825044bb2b3b0a757c560` | 0 | https://www.gy120.net/files/20180122104317435.jpg |
| 肖文豪 | 257 | 风湿免疫科 | 副主任医师 | 肖文豪-风湿免疫科-副主任医师-广东药科大学附属第一医院.jpg | 41074 | 300×429 | `707d86850a8a5fb3a41a60d7819aaf85fadd87fbc6288c844cbc4c16fcd8867e` | 0 | https://www.gy120.net/files/20240830165913114.jpg |
| 孙慧琳 | 230 | 肥胖专病治疗组 | 主任医师 | 孙慧琳-肥胖专病治疗组-主任医师-广东药科大学附属第一医院.jpg | 1734432 | 1335×2002 | `757fdec9eb40a4b5f9fc2fa6bd175dadb91787a8e332e5679c53eeaca8906a6f` | 0 | https://www.gy120.net/files/20180104113746126.JPG |
| 区奕猛 | 7 | 普外一科（肝胆外科） | 主任医师 | 区奕猛-普外一科（肝胆外科）-主任医师-广东药科大学附属第一医院.jpg | 234226 | 458×687 | `9047d6a43b420ed195e0fd0b47dce5317792e9fc974e1cd46d2f4583948bc3d7` | 0 | https://www.gy120.net/files/20190917091728518.JPG |

### 管理员批准的连续两次失败留空标注

| 姓名 | ArticleID | 详情 Referer | 官网照片 | 两次结果 | 处置 |
|---|---|---|---|---|---|
| 无 | 无 | 无 | 无 | 无 | 无 |


## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| https://www.gy120.net/zhuanjia.asp | 护师，国际造口治疗师 | https://www.gy120.net/articleshow.asp?articleid=404 | 官网详情专业职称明确为纯护理身份，按医生画像范围排除 |
| https://www.gy120.net/zhuanjia.asp | 副主任护师，血液内科护士长/静疗专科组长 | https://www.gy120.net/articleshow.asp?articleid=603 | 官网详情专业职称明确为纯护理身份，按医生画像范围排除 |

## 输出文件

- Excel 底表：未生成（本轮使用 --no-xlsx）
- CSV 底表：`D:\workspace\信息收集整理\work\广东药科大学附属第一医院_trial_doctors.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 4 |
| 原始医生卡片记录 | 407 |
| 跨入口去重前候选关系 | 349 |
| 跨入口去重后唯一候选 | 349 |
| 排除非医生候选 | 2 |
| 合规医生详情页 | 347 |
| 最终医生身份 | 10 |
| 覆盖科室数 | 10 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 4 |
| 慢性病 | 8 |
| 术后恢复/康复 | 3 |
| 疑难重症 | 4 |
| 肿瘤 | 2 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 心内一科 | 1 |
| 心内二科 | 1 |
| 血液内科 | 1 |
| 呼吸与危重症医学科 | 1 |
| 肾内科 | 1 |
| 内分泌科 | 1 |
| 消化内科 | 1 |
| 风湿免疫科 | 1 |
| 肥胖专病治疗组 | 1 |
| 普外一科（肝胆外科） | 1 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 无 | 0 |

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
