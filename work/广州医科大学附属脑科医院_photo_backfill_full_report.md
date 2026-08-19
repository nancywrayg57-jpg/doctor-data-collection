# Issue #77 广州医科大学附属脑科医院照片补录 FULL 报告

> 日期：2026-08-19
> Phase：`FULL_FIXED_READY_FOR_OWNER_REAUDIT`

## 四数对账

| 固定目标 | 实采 | 失败留空 | 正式落盘 | 照片字段留空 |
|---:|---:|---:|---:|---:|
| 183 | 179 | 4 | 179 | 4 |

- 复用已审计 TRIAL：10；FULL 新抓取成功：169；FULL 新抓取失败：4；新抓取目标：173。
- 详情状态波动 0；照片状态波动 0；页面未引用路径探测 0；第三方来源 0。

| 失败四类 | 数量 |
|---|---:|
| 详情不可达 | 0 |
| 照片资源不可达 | 0 |
| 无照片容器 | 0 |
| 占位图 | 4 |

## 失败逐条证据

- 李荷花｜占位图｜https://www.gzbrain.cn/myzj/info_itemid_766.html｜{"cross_doctor_sources":["https://www.gzbrain.cn/myzj/info_itemid_765.html","https://www.gzbrain.cn/myzj/info_itemid_766.html"],"decoded_query_filename":"blank2.jpg","detection_feature":"same-SHA cross-doctor reuse sha256=42dac34e29cd304174e89e8552fadacd4a0380b9e3346b9f5c5ebf2393cb96fd; full-image unique_color_count=1 all pixels RGBA=(255,255,255,255); query Base64 decodes to blank2.jpg","excluded_resource_examples":[],"observed_utc":"2026-08-19T01:56:51Z","owner_audit_comment":"https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/78#issuecomment-5336568337","photo_reference_count":1,"resource_urls":["https://www.gzbrain.cn/uploadfiles/2019/05/20190514181659427.jpg?YmxhbmsyLmpwZw==","https://www.gzbrain.cn/uploadfiles/2019/05/20190514181942717.jpg?YmxhbmsyLmpwZw=="],"sha256":"42dac34e29cd304174e89e8552fadacd4a0380b9e3346b9f5c5ebf2393cb96fd","template_signature":".single_con > .single_cn > .single-img > img[src]","unique_color_count":1}
- 李莹珊｜占位图｜https://www.gzbrain.cn/myzj/info_itemid_765.html｜{"cross_doctor_sources":["https://www.gzbrain.cn/myzj/info_itemid_765.html","https://www.gzbrain.cn/myzj/info_itemid_766.html"],"decoded_query_filename":"blank2.jpg","detection_feature":"same-SHA cross-doctor reuse sha256=42dac34e29cd304174e89e8552fadacd4a0380b9e3346b9f5c5ebf2393cb96fd; full-image unique_color_count=1 all pixels RGBA=(255,255,255,255); query Base64 decodes to blank2.jpg","excluded_resource_examples":[],"observed_utc":"2026-08-19T01:56:51Z","owner_audit_comment":"https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/78#issuecomment-5336568337","photo_reference_count":1,"resource_urls":["https://www.gzbrain.cn/uploadfiles/2019/05/20190514181659427.jpg?YmxhbmsyLmpwZw==","https://www.gzbrain.cn/uploadfiles/2019/05/20190514181942717.jpg?YmxhbmsyLmpwZw=="],"sha256":"42dac34e29cd304174e89e8552fadacd4a0380b9e3346b9f5c5ebf2393cb96fd","template_signature":".single_con > .single_cn > .single-img > img[src]","unique_color_count":1}
- 程道猛｜占位图｜https://www.gzbrain.cn/myzj/info_itemid_877.html｜{"detection_feature":"strict container references generic doctor_img1.jpg default","excluded_resource_examples":[{"feature":"strict container references generic doctor_img1.jpg default","reason":"占位图","url":"https://www.gzbrain.cn/uploadfiles/image/doctor_img1.jpg?ZG9jdG9yX2ltZzEuanBn"}],"observed_utc":"2026-08-18T21:02:11Z","photo_reference_count":1,"resource_urls":["https://www.gzbrain.cn/uploadfiles/image/doctor_img1.jpg?ZG9jdG9yX2ltZzEuanBn"],"template_signature":".single_con > .single_cn > .single-img > img[src]"}
- 梁卉薇｜占位图｜https://www.gzbrain.cn/myzj/info_itemid_989.html｜{"detection_feature":"响应呈小尺寸占位图特征：5686 bytes；96×48","excluded_resource_examples":[],"observed_utc":"2026-08-18T21:02:38Z","photo_reference_count":1,"resource_urls":["https://www.gzbrain.cn/uploadfiles/2019/06/20190614161949707.bmp?dmNyZWRpc3QuYm1w"],"template_signature":".single_con > .single_cn > .single-img > img[src]"}

## 照片与大小

| 大小分桶 | 数量 |
|---|---:|
| <200KiB | 132 |
| 200KiB-1MiB | 29 |
| 1-5MiB | 17 |
| 5-20MiB | 1 |
| >20MiB | 0 |

- 照片总字节 70,817,296（67.54 MiB）；最大 11,646,846 bytes。
- 超过 5 MiB 1；超过 20 MiB 0；声明/魔数不一致 18。
- 实际格式：{"png": 66, "jpg": 113}；重复 SHA-256 组 1；跨医生重复 SHA-256 组 0。

## >5 MiB Owner 终审清单

- 徐文军｜https://www.gzbrain.cn/uploadfiles/2019/05/20190507083727201.jpg?5b6Q5paH5YabLmpwZw==｜11,646,846 bytes｜3024×3024｜`eef393825403f18cf1384eefa96597957830a8549c4814b01ddc9b7efc1233c1`

## 三载体、画像与视觉门禁

- 总底表 payload/CSV/XLSX 逐值一致；只修改本院成功行 `照片链接`、`照片文件` 与失败行 `异常提示`。
- 逐单元格变化 362：{"照片链接": 179, "照片文件": 179, "异常提示": 4}。
- FULL reconciliation/manifest 对每张照片逐一复算字节、SHA-256、魔数/扩展名、尺寸和同站页面引用 URL；URL query Base64 占位词、全图唯一颜色数 ≤2、跨医生同 SHA 均已固化拦截；照片目录零孤儿零缺失。
- 成功 179 份 AUTO 画像严格 +2/-0；失败 4 份零触碰；`_索引.md` 零修改。
- FULL 抽样拼图覆盖最小、最大、8 个确定性随机；全量视觉联系表 8 页覆盖 179 张，已由 Codex 逐页目视确认为单人医生职业照，未见患者、儿童、合影、二维码、装饰或占位图。
- 入口台账、总底表更新报告与全部 TRIAL 工件保持不变。

## 工件

- `work/广州医科大学附属脑科医院_photo_backfill_full_payload.json`
- `work/广州医科大学附属脑科医院_photo_backfill_full_reconciliation.csv`
- `work/广州医科大学附属脑科医院_photo_backfill_full_report.md`
- `work/广州医科大学附属脑科医院_photo_backfill_full_audit_sheet.jpg`
- `work/广州医科大学附属脑科医院_photo_backfill_full_visual_review/`
- `医生画像仓库/01_试点医院/广州医科大学附属脑科医院/照片/`

## 停止点

`FULL_FIXED_READY_FOR_OWNER_REAUDIT`。完成本地实图和工作簿目视核验、提交并推送 PR #78 后发布 `FULL_FIXED_DONE`；不得自行合并、关闭 Issue 或领取下一任务。
