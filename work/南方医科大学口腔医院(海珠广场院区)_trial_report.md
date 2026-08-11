---
类型: 自动采集试跑报告
医院: 南方医科大学口腔医院(海珠广场院区)
城市: 广州市
采集日期: 2026-08-11
来源范围: 医院官网
采集入口: https://www.smukqyy.cn/section/341 https://www.smukqyy.cn/section/342 https://www.smukqyy.cn/section/434 https://www.smukqyy.cn/section/343 https://www.smukqyy.cn/section/385 https://www.smukqyy.cn/section/384 https://www.smukqyy.cn/section/386 https://www.smukqyy.cn/section/431 https://www.smukqyy.cn/section/504
适配器: generic_official_template
---

# 南方医科大学口腔医院(海珠广场院区) 官方医生自动采集试跑报告

## 结论

本次试跑只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集试采底表，共 10 位唯一医生；官网列表页原始卡片记录 95 条；识别到官网列表分页 9 页；覆盖 9 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 南方医科大学口腔医院(海珠广场院区) |
| 官网首页 | https://www.smukqyy.cn/home |
| 本轮医生入口 | https://www.smukqyy.cn/section/341 https://www.smukqyy.cn/section/342 https://www.smukqyy.cn/section/434 https://www.smukqyy.cn/section/343 https://www.smukqyy.cn/section/385 https://www.smukqyy.cn/section/384 https://www.smukqyy.cn/section/386 https://www.smukqyy.cn/section/431 https://www.smukqyy.cn/section/504 |
| 入口来源 | Claude owner PR #6 显式修正 |
| 原台账医生入口 | https://www.smukqyy.cn/section/364 |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | A-优先自动采集 |

## 输出文件

- Excel 底表：未生成（本轮使用 --no-xlsx）
- CSV 底表：`D:\workspace\信息收集整理\work\南方医科大学口腔医院(海珠广场院区)_trial_doctors.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 官网列表分页数 | 9 |
| 原始医生卡片记录 | 95 |
| 唯一医生详情页 | 10 |
| 覆盖科室数 | 9 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 疑难重症 | 2 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 口腔种植修复科 | 2 |
| 口腔正畸科 | 1 |
| 牙体牙髓病科二室 | 1 |
| 牙周黏膜病科 | 1 |
| 儿童口腔科 | 1 |
| 口腔预防科 | 1 |
| 口腔颌面外科 | 1 |
| 牙体牙髓病科一室 | 1 |
| 舒适化治疗中心 | 1 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 科室原文含正文，已清洗 | 8 |
| 通用模板低置信度 | 1 |

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
4. 专用适配器结果可直接进入正式追加；通用模板结果需先完成小样本试采复核，确认字段质量后再全量追加。

## 合规边界

- 仅使用医院官网公开网页。
- 不采集私人电话、私人微信、家庭住址、患者隐私或非公开排班信息。
- 不使用第三方医疗平台评价、排名、患者评论。
- 不写“保证治愈”“包治疑难杂症”“疗效第一”等无法由官网证明的表达。
