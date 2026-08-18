# Issue #75 广州医科大学附属口腔医院照片补录 TRIAL 报告

## 门禁与范围

- GitHub Issue：#75
- Phase：TRIAL
- Owner 裁决：采纳方案 A，豁免第二 category；固定 category=55，改为覆盖至少两个官网科室。
- 医院官网：https://www.gykqyy.com/
- 医生目录：https://www.gykqyy.com/list.html?category=55
- 唯一获准 API：https://www.gykqyy.com/api/article/getZhuanjiaList?category=55
- 总底表固定范围：297 行；唯一来源 297；TRIAL 前照片字段非空 0。
- API 范围：5 分组、31 科室、317 医生-科室关系、297 唯一固定 ID；对象出现 384 次。
- category 现场值：["55"]；第二 category 请求/枚举/探测均为 0。

## 页面调用与接口留痕

- 目录页 HTTP 200 / `text/html`；已验证 `currentId.value == 55`、`getZhuanjiaList`、`item3.image || './images/null.jpg'` 和 `item3.yccms_category_id`。
- API HTTP 200 / `application/json`；最终 URL `https://www.gykqyy.com/api/article/getZhuanjiaList?category=55`；响应 619,644 bytes；SHA-256 `1e49812c45b6dc5bbb1c50214590b8f02b4b7e1ea7211124f40f1c14adfda709`；UTC `2026-08-18T19:19:56Z`。
- API 响应仅按 `data.list` 固定 297 ID 建立工作集；banner 范围外空白焦点项不进入固定范围。
- 未调用详情 API、未请求其他 category、未探测其他接口、未构造任何图片路径。

## image 字段普查与排除

- 固定 297 行 image 信号：{"NO_PHOTO_CONTAINER_EMPTY_IMAGE_FIELD": 231, "NO_PHOTO_CONTAINER_NON_UPLOAD_IMAGE_FIELD": 8, "VALID_REFERENCED_ORIGINAL": 58}。
- 有效 `/uploads/<日期>/<hash>.<格式>` 原图候选 58；其职称层可用数 {"正高": 22, "副高": 36, "其他": 0}。
- 有效照片候选中“其他”职称层为 0，故本批可实现的最大职称覆盖只有正高/副高；TRIAL 固定为 5 正高 + 5 副高并在此回报，不把无有效 image 的主治/医师伪作照片样本。
- 排除资源下载数 0；未引用路径构造/探测 0；第三方来源 0。

- API image 为空/null：无照片容器，记录字段值，不下载 fallback
- ./images/null.jpg：页面 fallback，占位资源，下载数必须为 0
- /images/ 下 search、yuandian、logo 等静态资源：公共装饰图，下载数必须为 0
- 非 www.gykqyy.com/uploads/<日期>/<hash>.<格式>：不是获准 image 原图，禁止构造或探测

## TRIAL 结果

- 样本 10/10；科室首原子 10 个；keshi_ids 联集 14 个；满足 Owner 裁决后的至少两个官网科室门禁。
- 职称层：{"正高": 5, "副高": 5}；照片成功 10/10；照片资源失败 0；状态波动 0。
- 10 张均为 API `image` 字段实际引用的官网原始响应字节，未压缩、未转码。
- 总字节 5,299,759；最小 188,668；中位数 489,452；平均 529,975；最大 1,081,247。
- 大小分桶：{"<200KiB": 1, "200KiB-1MiB": 8, "1-5MiB": 1, "5-20MiB": 0, ">20MiB": 0}；>5 MiB 0；>20 MiB 0。
- 联系表视觉状态：`PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。

## 样本清单

- 李江｜ID 195｜越秀院区口腔修复科｜主任医师（正高）｜keshi_ids=19｜479,630 bytes｜2269×2934｜`e18df6c7804c42c015073d05e0fef8822e5469e36ace36ccc2ddfc1b5c1ad948`
- 张清彬｜ID 136｜荔湾院区颞下颌关节科｜主任医师（正高）｜keshi_ids=15,30｜561,160 bytes｜2443×3309｜`fa52e14c6ac2ffed974bd22b90056adf9757d2eb999b1f421ad54be79bc92a7d`
- 江千舟｜ID 80｜荔湾院区牙体牙髓科｜主任医师（正高）｜keshi_ids=10｜575,788 bytes｜2473×3510｜`a0d9584bffefa19074d4e23bc0b2ab71c734bb6cfc8d3bb92f7865b5f5df2bd2`
- 朴正国｜ID 51｜荔湾院区口腔颌面外科｜主任医师（正高）｜keshi_ids=6,17｜188,668 bytes｜315×422｜`b67aed236e0c35cbfe7692048f40179da2ac44fc5d470472c0b64326c6720b6b`
- 刘畅｜ID 110｜荔湾院区口腔正畸科｜主任医师（正高）｜keshi_ids=13｜499,274 bytes｜1692×2572｜`f817cb3113f919a7d4afe73ff29b0869141600ba3359714df440d521395c8e3b`
- 张云燕｜ID 152｜越秀院区儿童口腔科｜副主任医师（副高）｜keshi_ids=16｜1,081,247 bytes｜697×924｜`47fd7198aa3a8b98703a7bc6293273e0a4acc4776ece6e01025a6850f4ab95b9`
- 杜发亮｜ID 5｜专家门诊特诊中心｜副主任医师（副高）｜keshi_ids=39,37｜465,186 bytes｜2481×3430｜`0070688121eb59065f534bfc6d00b687a8a3e113dd11cee72e4319a54029a157`
- 余挺｜ID 241｜越秀院区牙周病科｜副主任医师（副高）｜keshi_ids=21｜516,522 bytes｜2336×3213｜`900888f6dab3f91e374b18c0f8d17ff0ea574162347238e6be303d1dbac403f2`
- 熊洁｜ID 287｜荔湾院区综合急诊科｜副主任医师（副高）｜keshi_ids=24,27｜459,206 bytes｜2192×3150｜`d117442150125669cfd69bb6539bff146d57e8a4eca8c8e02b97a2d11c6cabfe`
- 张斌｜ID 258｜正畸与儿童口腔中心｜副主任医师（副高）｜keshi_ids=38｜473,078 bytes｜2386×3210｜`8b95af93cb573a2f88a634470e6a2c6c148cfc2696c557ee642ca8dfa1d672f3`

## >5 MiB Owner 终审清单

- 无

## 正式资产保护

- 入口台账 JSON/CSV/XLSX、总底表 JSON/CSV/XLSX、更新报告、本院 298 个 Markdown 文件聚合快照与正式照片目录在 TRIAL 前后完全一致：True。
- TRIAL 仅写 `work/` 独立工件；未回填底表、未刷新画像、未创建正式照片目录。

## 工件

- `work/广州医科大学附属口腔医院_photo_backfill_trial_payload.json`
- `work/广州医科大学附属口腔医院_photo_backfill_trial_manifest.csv`
- `work/广州医科大学附属口腔医院_photo_backfill_trial_report.md`
- `work/广州医科大学附属口腔医院_photo_backfill_trial_contact_sheet.jpg`
- `work/广州医科大学附属口腔医院_photo_backfill_trial_photos/`（10 张）

## 停止点

`TRIAL_READY_FOR_OWNER_AUDIT`。未取得 Owner 在关联 PR 的明确 `FULL_APPEND_AND_OBSIDIAN` 前，不写正式资产。
