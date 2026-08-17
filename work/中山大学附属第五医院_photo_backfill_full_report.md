# Issue #61 中山大学附属第五医院照片补录 FULL 报告

> 日期：2026-08-17
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`
> 照片政策：`OWNER_APPROVED_PAGE_REFERENCED_STYLES_WATERMARK_ORIGINAL_BYTES`

## 四数对账

| 范围 / 应采 | 实采 | 失败 | 留空 |
|---:|---:|---:|---:|
| 413 | 410 | 3 | 3 |

| 失败三态 | 数量 |
|---|---:|
| 详情不可达 | 1 |
| 无照片容器 | 1 |
| 占位图 | 1 |

- 总问题率：3/413（0.73%），未超过 30% 熔断线。
- 照片总字节：108888826 bytes（103.84 MiB）。
- 最大单张：6649475 bytes；超过 5 MiB：1 张；超过 20 MiB：0 张。
- 页面未引用路径的构造/探测请求：0；第三方来源：0。
- 传输不完整原样重试：0 次；每个请求至多重试 1 次。
- 总底表：payload/CSV/XLSX 三载体行数与 25 列逐值一致；仅本院 413 行的照片两列及失败行异常提示允许变化。
- 画像：既有 413 份画像中，实采成功的 410 份仅新增方案 A 照片引用区块；失败留空画像零触碰；不新建画像；`_索引.md` 零修改。

## >5 MiB Owner 终审清单

| 姓名 | URL | 字节 | 尺寸 |
|---|---|---:|---:|
| 陈贤珍 | <https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-07/20240208173237537.jpg?itok=RSFCQ8E7> | 6649475 | 4831×4833 |

## 工件

- `D:\workspace\信息收集整理\work\中山大学附属第五医院_photo_backfill_full_payload.json`
- `D:\workspace\信息收集整理\work\中山大学附属第五医院_photo_backfill_full_reconciliation.csv`
- `D:\workspace\信息收集整理\work\中山大学附属第五医院_photo_backfill_full_report.md`
- `D:\workspace\信息收集整理\医生画像仓库\01_试点医院\中山大学附属第五医院\照片`
- `D:\workspace\信息收集整理\docs\中山五院照片嵌入方式裁决单.md`

## 合规边界

1. 只访问 413 条既有医院官网医生详情链接及页面 `.field.field-featured-media.field-item img` 容器自身引用的 `styles/watermark` 派生图。
2. 使用官网首页建立的常规 Cookie 会话和对应详情页 Referer；保留 `itok`，按页面引用原始响应字节保存，不压缩。
3. 禁止构造或探测页面未引用图片路径；禁止第三方来源。
4. 失败仅按“详情不可达 / 无照片容器 / 占位图”留空并追加异常提示。
