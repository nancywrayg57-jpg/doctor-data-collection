# Issue #59 中山大学肿瘤防治中心照片补录 FULL 报告

> 日期：2026-08-16
> Phase：FULL_READY_FOR_FINAL_OWNER_AUDIT
> 照片政策：OWNER_APPROVED_PAGE_REFERENCED_DERIVATIVE_ORIGINAL_BYTES

## 四数对账

| 应采 | 实采 | 失败 | 留空 |
|---:|---:|---:|---:|
| 542 | 536 | 6 | 7 |

留空数包含失败三态 6 行和 taxonomy 不适用 1 行；实采 + 留空 = 543 条总范围。

| 失败三态 | 数量 |
|---|---:|
| 详情不可达 | 3 |
| 无照片容器 | 3 |
| 占位图 | 0 |

- taxonomy 单列：https://www.sysucc.org.cn/taxonomy/term/267，姓名“医学教育”，不访问、不采集；照片两列留空并追加“来源非医生详情页，照片不适用”。
- 详情不可达率：3/542（0.55%），未超过 10% 熔断线。
- 照片总字节：94451923 bytes（90.08 MiB）。
- 最大单张：317437 bytes；超过 5 MiB：0 张。
- 页面未引用路径的构造/探测请求：0；第三方来源请求：0。
- 传输不完整原样重试：0 次；每个请求至多重试 1 次。
- 官网标题别名映射：15 条；仅用于校验来源页身份，不修改底表姓名等字段。
- 总底表：payload/CSV/XLSX 三载体行数与 25 列逐值一致；仅目标行照片两列、失败行和 taxonomy 行异常提示允许变化。
- 画像：现有来源映射 544 份；成功实采且有既有画像的 536 份只新增照片嵌入区块；0 条无画像行未新建画像；索引未改。

## 工件

- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_full_payload.json
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_full_reconciliation.csv
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_full_report.md

## 合规边界

1. 只访问 542 条既有医院官网 doctor 来源链接及页面自身引用的 .title-4-0 .item-media img 公开照片；taxonomy 行不访问。
2. 使用官网首页建立的常规 Cookie 会话和对应详情页 Referer；页面引用 media_2_3_400_600 派生图原始响应字节保存，不压缩。
3. 禁止构造或探测页面未引用图片路径；禁止第三方来源请求。
4. 失败仅按“详情不可达 / 无照片容器 / 占位图”留空并追加异常提示。
