# Issue #79 南方医科大学第五附属医院照片补录 FULL 报告

> 日期：2026-08-19
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`

## 四数对账

| 固定目标 | 实采 | 失败留空 | 正式落盘 | 照片字段留空 |
|---:|---:|---:|---:|---:|
| 134 | 132 | 2 | 132 | 2 |

- 复用已审计 TRIAL：10；FULL 新抓取成功：122；FULL 新抓取失败：2；新抓取目标：124。
- 详情状态波动 0；照片状态波动 0；页面未引用路径探测 0；第三方来源 0。

| 失败四类 | 数量 |
|---|---:|
| 详情不可达 | 0 |
| 照片资源不可达 | 0 |
| 无照片容器 | 2 |
| 占位图 | 0 |

## 失败逐条证据

- 王敏聪｜无照片容器｜http://www.ny5y.cn/yisheng_xq.php?id=458｜{"detection_feature":"HTTP 200 detail template contains no div.yisheng_xq_bug_left and no physician detail body","excluded_resource_examples":[],"observed_utc":"2026-08-19T07:21:57Z","photo_reference_count":0,"resource_urls":["http://www.ny5y.cn/yisheng_xq.php?id=458"],"template_signature":"div.yisheng_xq_bug_left inline background-image"}
- 孙乐栋｜无照片容器｜http://www.ny5y.cn/yisheng_xq.php?id=274｜{"detection_feature":"HTTP 200 detail template contains no div.yisheng_xq_bug_left and no physician detail body","excluded_resource_examples":[],"observed_utc":"2026-08-19T07:22:45Z","photo_reference_count":0,"resource_urls":["http://www.ny5y.cn/yisheng_xq.php?id=274"],"template_signature":"div.yisheng_xq_bug_left inline background-image"}

## 照片与大小

| 大小分桶 | 数量 |
|---|---:|
| <200KiB | 108 |
| 200KiB-1MiB | 21 |
| 1-5MiB | 3 |
| 5-20MiB | 0 |
| >20MiB | 0 |

- 照片总字节 28,996,303（27.65 MiB）；最大 2,546,664 bytes。
- 超过 5 MiB 0；超过 20 MiB 0；声明/魔数不一致 0。
- 实际格式：{"png": 101, "jpg": 31}；重复 SHA-256 组 2；跨医生重复 SHA-256 组 0。

## >5 MiB Owner 终审清单

- 无

## 三载体、画像与视觉门禁

- 总底表 payload/CSV/XLSX 逐值一致；只修改本院成功行 `照片链接`、`照片文件` 与失败行 `异常提示`。
- 逐单元格变化 266：{"照片链接": 132, "照片文件": 132, "异常提示": 2}。
- FULL reconciliation/manifest 对每张照片逐一复算字节、SHA-256、魔数/扩展名、尺寸和同站页面引用 URL；URL query Base64 占位词、全图唯一颜色数 ≤2、跨医生同 SHA 均已固化拦截；照片目录零孤儿零缺失。
- 成功 132 份 AUTO 画像严格 +2/-0；失败 2 份零触碰；`_索引.md` 零修改。
- FULL 抽样拼图覆盖最小、最大、8 个确定性随机；全量视觉联系表 6 页覆盖 132 张，已由 Codex 逐页目视确认为单人医生职业照，未见患者、儿童、合影、二维码、装饰或占位图。
- 入口台账、总底表更新报告与全部 TRIAL 工件保持不变。

## 工件

- `work/南方医科大学第五附属医院_photo_backfill_full_payload.json`
- `work/南方医科大学第五附属医院_photo_backfill_full_reconciliation.csv`
- `work/南方医科大学第五附属医院_photo_backfill_full_report.md`
- `work/南方医科大学第五附属医院_photo_backfill_full_audit_sheet.jpg`
- `work/南方医科大学第五附属医院_photo_backfill_full_visual_review/`
- `医生画像仓库/01_试点医院/南方医科大学第五附属医院/照片/`

## 停止点

`FULL_READY_FOR_FINAL_OWNER_AUDIT`。完成本地实图和工作簿目视核验、提交并推送 PR #80 后发布 `FULL_DONE`；不得自行合并、关闭 Issue 或领取下一任务。
