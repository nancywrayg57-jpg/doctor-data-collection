# Issue #77 广州医科大学附属脑科医院照片补录 FULL 报告

> 日期：2026-08-19
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`

## 四数对账

| 固定目标 | 实采 | 失败留空 | 正式落盘 | 照片字段留空 |
|---:|---:|---:|---:|---:|
| 183 | 181 | 2 | 181 | 2 |

- 复用已审计 TRIAL：10；FULL 新抓取成功：171；FULL 新抓取失败：2；新抓取目标：173。
- 详情状态波动 0；照片状态波动 0；页面未引用路径探测 0；第三方来源 0。

| 失败四类 | 数量 |
|---|---:|
| 详情不可达 | 0 |
| 照片资源不可达 | 0 |
| 无照片容器 | 0 |
| 占位图 | 2 |

## 失败逐条证据

- 程道猛｜占位图｜https://www.gzbrain.cn/myzj/info_itemid_877.html｜{"detection_feature":"strict container references generic doctor_img1.jpg default","excluded_resource_examples":[{"feature":"strict container references generic doctor_img1.jpg default","reason":"占位图","url":"https://www.gzbrain.cn/uploadfiles/image/doctor_img1.jpg?ZG9jdG9yX2ltZzEuanBn"}],"observed_utc":"2026-08-18T21:02:11Z","photo_reference_count":1,"resource_urls":["https://www.gzbrain.cn/uploadfiles/image/doctor_img1.jpg?ZG9jdG9yX2ltZzEuanBn"],"template_signature":".single_con > .single_cn > .single-img > img[src]"}
- 梁卉薇｜占位图｜https://www.gzbrain.cn/myzj/info_itemid_989.html｜{"detection_feature":"响应呈小尺寸占位图特征：5686 bytes；96×48","excluded_resource_examples":[],"observed_utc":"2026-08-18T21:02:38Z","photo_reference_count":1,"resource_urls":["https://www.gzbrain.cn/uploadfiles/2019/06/20190614161949707.bmp?dmNyZWRpc3QuYm1w"],"template_signature":".single_con > .single_cn > .single-img > img[src]"}

## 照片与大小

| 大小分桶 | 数量 |
|---|---:|
| <200KiB | 134 |
| 200KiB-1MiB | 29 |
| 1-5MiB | 17 |
| 5-20MiB | 1 |
| >20MiB | 0 |

- 照片总字节 70,819,590（67.54 MiB）；最大 11,646,846 bytes。
- 超过 5 MiB 1；超过 20 MiB 0；声明/魔数不一致 18。
- 实际格式：{"png": 66, "jpg": 115}；重复 SHA-256 组 2。

## >5 MiB Owner 终审清单

- 徐文军｜https://www.gzbrain.cn/uploadfiles/2019/05/20190507083727201.jpg?5b6Q5paH5YabLmpwZw==｜11,646,846 bytes｜3024×3024｜`eef393825403f18cf1384eefa96597957830a8549c4814b01ddc9b7efc1233c1`

## 三载体、画像与视觉门禁

- 总底表 payload/CSV/XLSX 逐值一致；只修改本院成功行 `照片链接`、`照片文件` 与失败行 `异常提示`。
- 逐单元格变化 364：{"照片链接": 181, "照片文件": 181, "异常提示": 2}。
- FULL reconciliation/manifest 对每张照片逐一复算字节、SHA-256、魔数/扩展名、尺寸和同站页面引用 URL；照片目录零孤儿零缺失。
- 成功 181 份 AUTO 画像严格 +2/-0；失败 2 份零触碰；`_索引.md` 零修改。
- FULL 抽样拼图覆盖最小、最大、8 个确定性随机；全量视觉联系表 8 页覆盖 181 张，已由 Codex 逐页目视确认为单人医生职业照，未见患者、儿童、合影、二维码、装饰或占位图。
- 入口台账、总底表更新报告与全部 TRIAL 工件保持不变。

## 工件

- `work/广州医科大学附属脑科医院_photo_backfill_full_payload.json`
- `work/广州医科大学附属脑科医院_photo_backfill_full_reconciliation.csv`
- `work/广州医科大学附属脑科医院_photo_backfill_full_report.md`
- `work/广州医科大学附属脑科医院_photo_backfill_full_audit_sheet.jpg`
- `work/广州医科大学附属脑科医院_photo_backfill_full_visual_review/`
- `医生画像仓库/01_试点医院/广州医科大学附属脑科医院/照片/`

## 停止点

`FULL_READY_FOR_FINAL_OWNER_AUDIT`。完成本地实图和工作簿目视核验、提交并推送 PR #78 后发布 `FULL_DONE`；不得自行合并、关闭 Issue 或领取下一任务。
