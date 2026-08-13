---
类型: 自动采集试跑报告
医院: 广州市中医院
城市: 广州市
采集日期: 2026-08-13
来源范围: 医院官网
采集入口: https://www.gzszyy.com/expert/
适配器: gzszyy_department_expert_directory
---

# 广州市中医院 官方医生自动采集试跑报告

## 结论

本次试采只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集试采底表，共 10 位唯一医生；官网列表页原始卡片记录 434 条；读取入口分类 37 个；覆盖 11 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 广州市中医院 |
| 官网首页 | https://www.gzszyy.com/patient/ |
| 本轮医生入口 | https://www.gzszyy.com/expert/ |
| 入口来源 | GitHub Issue #33（与官网入口台账一致） |
| 原台账医生入口 | https://www.gzszyy.com/expert/ |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | A-优先自动采集 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
| 官网顶层全院专家目录 | https://www.gzszyy.com/expert/ | 医院官网名医名家未筛选目录；用于校验全院详情 ID 覆盖 | 18 | 423 | 423 | 0 | 广州市中医院 | 同域公开目录；与 dp 科室树逐 ID 对账 |
| 官网 dp 科室专家树 | https://www.gzszyy.com/expert/ | 医院官网名医名家目录；dp 科室筛选为全院普查入口 | 37 | 433 | 422 | 5 | 广州市中医院 | 同域单一医院；首页院区/门诊部与详情二维码标签独立留痕 |

### 动态目录专项证据

- 医生分页/载入方式：顶层全院目录 18 页校验身份覆盖；35 个 dp 科室筛选入口共 37 页提供科室关系；pr/le 仅为职称/级别筛选证据
- 医生目录公开接口：不适用
- 医生详情公开接口：不适用
- 接口出处证据：不适用
- 院区/分组：5 个；科室分类：35 个
- 医生-科室关系：434 条
- 唯一详情 ID：423 个
- 有姓名详情 ID：423 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：419 个
- 同名不同详情 ID：4 组
- 非空/空科室块：422 / 1
- 院区/出诊点标签关系：珠玑路院区 7 条；同德围分院 3 条；同德综合门诊部 1 条
- 跨院区/出诊点详情 ID：3 个

| 同名 | 详情 ID |
|---|---|
| 林少贞 | ELe31Mb6,JxboyNeg |
| 唐瑾秋 | 4QbYVOdz,X7ax9byv |
| 王健 | 3YaOggax,WZdP6yaK |
| 高三德 | LDdwkmd1,QBeXY8ay |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：434
- 跨入口去重后唯一候选：423
- 跨入口重复关系：11
- 试采覆盖入口分类：11 个（体检科、名医堂、心病科（心血管内科）、肛肠科、肿瘤一区、肿瘤二区、脑病科（神经内科）、脾胃科（消化内科）、重症医学科、针灸科、骨伤科）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 叶穗林 | https://www.gzszyy.com/expert/2026/w9aADOev.html | 名医堂；心病科（心血管内科） |
| 蔡迎峰 | https://www.gzszyy.com/expert/2026/X7axvrdy.html | 名医堂；骨伤科 |
| 李丽霞 | https://www.gzszyy.com/expert/2026/KQe1wRbJ.html | 名医堂；针灸科 |
| 赵云燕 | https://www.gzszyy.com/expert/2026/46dBgJe7.html | 名医堂；重症医学科 |
| 叶绍伟 | https://www.gzszyy.com/expert/2026/9wdLwbjP.html | 名医堂；脑病科（神经内科） |
| 吕永慧 | https://www.gzszyy.com/expert/2026/WPe9xdLy.html | 名医堂；脾胃科（消化内科） |
| 梁劲军 | https://www.gzszyy.com/expert/2026/4zbq7rep.html | 名医堂；肛肠科 |
| 黄金兰 | https://www.gzszyy.com/expert/2026/8mepzrbM.html | 肿瘤二区；血液科 |
| 许幸仪 | https://www.gzszyy.com/expert/2026/WZdPwbKg.html | 脑病科（神经内科）；体检科 |
| 高三德 | https://www.gzszyy.com/expert/2026/LDdwkmd1.html | 治未病科；普通内科、杂病门诊 |
| 赵明昂 | https://www.gzszyy.com/expert/2026/J0dNYLbL.html | 针灸康复科；同德综合门诊部 |

## 广州市中医院院区/出诊点证据

- 顶层全院目录 / dp 科室树：18 页、423 ID / 37 页、422 ID
- 顶层目录专属详情：1 个（lNbWW4by）；dp 树专属详情：0 个
- 筛选链接：dp 35 个（科室）、pr 18 个（职称）、le 3 个（专家级别）；pr/le 不重复采集
- 纯护理排除后合规候选：418 个
- 官网公开院区/门诊部范围：5 个
- 试采详情：10 个；有二维码院区/出诊点标签 8 个；未标注 2 个
- 多院区/出诊点标签详情：3 个
- 详情标签计数：珠玑路院区 7 条；同德围分院 3 条；同德综合门诊部 1 条
- 字段处理：详情页明确标签与列表卡片科室共同保留在 `科室_列表卡片`；不推断院区与科室之间未由官网明示的组合关系。

| 官网公开院区/门诊部 | 官方链接 |
|---|---|
| 珠玑院区 | https://www.gzszyy.com/district1_zzlyq/ |
| 天河新院区 | https://www.gzszyy.com/district1_thxyq/ |
| 同德院区 | https://www.gzszyy.com/district1_tdfy/ |
| 五羊门诊部 | https://www.gzszyy.com/district1_wymzb/ |
| 同德门诊部 | https://www.gzszyy.com/district1_tdmzb/ |

| 姓名 | 详情 ID | 科室归属 | 详情二维码院区/出诊点 | 来源链接 |
|---|---|---|---|---|
| 叶穗林 | w9aADOev | 名医堂、心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/w9aADOev.html |
| 蔡迎峰 | X7axvrdy | 名医堂、骨伤科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/X7axvrdy.html |
| 李丽霞 | KQe1wRbJ | 名医堂、针灸科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/KQe1wRbJ.html |
| 赵云燕 | 46dBgJe7 | 名医堂、重症医学科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/46dBgJe7.html |
| 叶绍伟 | 9wdLwbjP | 名医堂、脑病科（神经内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/9wdLwbjP.html |
| 吕永慧 | WPe9xdLy | 名医堂、脾胃科（消化内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/WPe9xdLy.html |
| 梁劲军 | 4zbq7rep | 名医堂、肛肠科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4zbq7rep.html |
| 吴薏婷 | 4zbqjrdp | 肿瘤一区 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4zbqjrdp.html |
| 邓力 | olej25ej | 肿瘤二区 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/olej25ej.html |
| 许幸仪 | WZdPwbKg | 脑病科（神经内科）、体检科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/WZdPwbKg.html |

## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| https://www.gzszyy.com/expert/ | 黄金兰 主管护师 | https://www.gzszyy.com/expert/2026/8mepzrbM.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |
| https://www.gzszyy.com/expert/ | 王少敏 主任护师 | https://www.gzszyy.com/expert/2026/pnelpJeK.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |
| https://www.gzszyy.com/expert/ | 曾会萍 主任护师 | https://www.gzszyy.com/expert/2026/8mep2bMy.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |
| https://www.gzszyy.com/expert/ | 周素金 主管护师 | https://www.gzszyy.com/expert/2026/4zbq2dpr.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |
| https://www.gzszyy.com/expert/ | 谭萍云 主管护师 | https://www.gzszyy.com/expert/2026/MvbmEAbY.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |

## 输出文件

- Excel 底表：未生成（本轮使用 --no-xlsx）
- CSV 底表：`D:\workspace\信息收集整理\work\广州市中医院_trial_doctors.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 37 |
| 原始医生卡片记录 | 434 |
| 跨入口去重前候选关系 | 434 |
| 跨入口去重后唯一候选 | 423 |
| 排除非医生候选 | 5 |
| 合规医生详情页 | 418 |
| 最终医生身份 | 10 |
| 覆盖科室数 | 11 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 1 |
| 慢性病 | 3 |
| 术后恢复/康复 | 2 |
| 生殖疾病 | 1 |
| 疑难重症 | 7 |
| 肿瘤 | 5 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 名医堂 | 7 |
| 脑病科（神经内科） | 2 |
| 心病科（心血管内科） | 1 |
| 骨伤科 | 1 |
| 针灸科 | 1 |
| 重症医学科 | 1 |
| 脾胃科（消化内科） | 1 |
| 肛肠科 | 1 |
| 肿瘤一区 | 1 |
| 肿瘤二区 | 1 |
| 体检科 | 1 |

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
