# Issue #55 中山大学中山眼科中心照片补录 FULL 报告

> 日期：2026-08-16
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`
> 照片政策：`OWNER_APPROVED_PAGE_REFERENCED_LARGE_960_ORIGINAL_BYTES`

## 四数对账

| 应采 | 实采 | 失败 | 留空 |
|---:|---:|---:|---:|
| 205 | 205 | 0 | 0 |

| 失败三态 | 数量 |
|---|---:|
| 详情不可达 | 0 |
| 无照片元素 | 0 |
| 占位图 | 0 |

- 详情不可达率：0/205（0.00%），未超过 10% 熔断线。
- 照片总字节：167098636 bytes（159.36 MiB）。
- 最大单张：1929832 bytes；超过 5 MiB：0 张。
- 页面未引用原图的构造/探测请求：0。
- 总底表：payload/CSV/XLSX 三载体行数与 25 列逐值一致；仅目标行照片两列及失败行异常提示允许变化。
- 画像：成功实采对应自动画像仅新增照片嵌入区块；失败留空画像保持不变；索引文件名与链接集合无需变化。

## 工件

- `D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_full_payload.json`
- `D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_full_reconciliation.csv`
- `D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_full_report.md`

## 合规边界

1. 只访问 205 条既有医院官网来源链接及页面自身引用的 `large_960_x_auto_` 公开资源。
2. `itok` 与 Referer 按 owner 指令原样使用；响应原始字节保存，不压缩。
3. 禁止构造或探测页面未引用的原图；禁止患者、儿童、合影、占位图或通用图入库。
4. 失败仅按“详情不可达 / 无照片元素 / 占位图”留空并追加异常提示。
