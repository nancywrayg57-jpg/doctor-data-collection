# Issue #67 广州市中医院照片补录 FULL 报告

> 日期：2026-08-17
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`
> 照片政策：`OWNER_APPROVED_UNIQUE_DOCTOR_IMG_OSS_ORIGINAL_BYTES`

## 四数对账

| 范围 / 应采 | 实采 | 失败 | 留空 |
|---:|---:|---:|---:|
| 415 | 415 | 0 | 0 |

| 失败三态 | 数量 |
|---|---:|
| 详情不可达 | 0 |
| 无照片容器 | 0 |
| 占位图 | 0 |

## 大小分布

| 分桶 | 数量 |
|---|---:|
| <200KiB | 130 |
| 200KiB-1MiB | 279 |
| 1-5MiB | 5 |
| 5-20MiB | 1 |
| >20MiB | 0 |

- 总问题率：0/415（0.00%），未超过 30% 熔断线。
- 照片总字节：101590176 bytes（96.88 MiB）。
- 最大单张：6193649 bytes；超过 5 MiB：1 张；超过 20 MiB：0 张。
- 详情不可达：初次请求后至少重试 2 次，间隔均不低于 30 秒，逐次 HTTP 状态与 UTC 已写入 payload；状态闪烁数 0。
- 页面未引用路径构造/探测：0；第三方来源：0；仅使用 `.doctor-resume div.doctor-img` 唯一引用及 `oss.gzszyy.com`。
- 排除 `div.qr-img`、`static.gzszyy.com/images/`、空 src 和页面未引用路径。
- 总底表：payload/CSV/XLSX 三载体逐值一致；仅本院 415 行照片两列及失败行异常提示允许变化。
- 画像：既有 415 份 AUTO 标记画像中，成功的 415 份仅在基础信息区新增照片引用；失败画像零触碰；不新建画像；`_索引.md` 零修改。
- 入口台账三载体与总底表更新报告保持不变。

## >5 MiB Owner 终审清单

| 姓名 | URL | 字节 | 尺寸 |
|---|---|---:|---:|
| 梁依敏 | <https://oss.gzszyy.com/20251118/140709731.png> | 6193649 | 1270×1217 |

## 工件

- `D:\workspace\信息收集整理\work\广州市中医院_photo_backfill_full_payload.json`
- `D:\workspace\信息收集整理\work\广州市中医院_photo_backfill_full_reconciliation.csv`
- `D:\workspace\信息收集整理\work\广州市中医院_photo_backfill_full_report.md`
- `D:\workspace\信息收集整理\医生画像仓库\01_试点医院\广州市中医院\照片`

## 合规边界

1. 只访问 415 条既有医院官网医生详情链接及页面唯一 `.doctor-resume div.doctor-img img[src]` 实际引用的医院 OSS 原图。
2. 照片请求携带对应详情页 Referer；保存页面引用版本原始字节，不压缩。
3. 禁止构造或探测页面未引用图片路径；禁止第三方来源；二维码、装饰图与空 src 不进入候选。
4. 失败仅按“详情不可达 / 无照片容器 / 占位图”留空并幂等追加异常提示。
