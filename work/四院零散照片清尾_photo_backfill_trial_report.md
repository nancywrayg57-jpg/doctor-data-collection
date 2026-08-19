# Issue #85 四院零散照片清尾 TRIAL 报告

- Phase：`TRIAL`
- 固定范围：249 行（174 + 48 + 25 + 2）
- TRIAL：12 行（5 + 5 + 1 + 1）
- 四数：12 = 0 实采 + 12 失败留痕
- 失败分类：详情不可达 0 / 照片资源不可达 3 / 无照片容器 1 / 占位图 8
- 正式资产修改：False
- 视觉状态：`PASSED_ZERO_DOWNLOADS_FAILURE_EVIDENCE_CONTACT_SHEET_REVIEW`

## 样本对账

| 医院 | 姓名 | 详情 HTTP | 页面照片引用 | 结果 | 判定依据 |
|---|---|---:|---|---|---|
| 广东省妇幼保健院 | 贾杰 | 200 | https://wx.e3861.com/sfyAdmin/Images/Default/doct.png | 占位图 | 详情照片位命中显式 default/placeholder 门禁；页面共享 /uploads/ 图为预约二维码，按 known-SHA 排除 |
| 广东省妇幼保健院 | 袁超 | 200 | https://wx.e3861.com/sfyAdmin/Images/Default/doct.png | 占位图 | 详情照片位命中显式 default/placeholder 门禁；页面共享 /uploads/ 图为预约二维码，按 known-SHA 排除 |
| 广东省妇幼保健院 | 秦克旺 | 200 | https://wx.e3861.com/sfyAdmin/Images/Default/doct.png | 占位图 | 详情照片位命中显式 default/placeholder 门禁；页面共享 /uploads/ 图为预约二维码，按 known-SHA 排除 |
| 广东省妇幼保健院 | 陈佳 | 200 | https://wx.e3861.com/sfyAdmin/Images/Default/doct.png | 占位图 | 详情照片位命中显式 default/placeholder 门禁；页面共享 /uploads/ 图为预约二维码，按 known-SHA 排除 |
| 广东省妇幼保健院 | 胡克 | 200 | https://wx.e3861.com/sfyAdmin/Images/Default/doct.png | 占位图 | 详情照片位命中显式 default/placeholder 门禁；页面共享 /uploads/ 图为预约二维码，按 known-SHA 排除 |
| 广东省第二人民医院 | 杨莲娣 | 200 | /static//seygw//resources/upload/2024/05/28/default_ys.gif | 占位图 | 详情照片位命中显式 default/placeholder 门禁 |
| 广东省第二人民医院 | 陈鹏程 | 200 | http://www.gd2h.com/system/profile/upload/2024/10/19/bc6b6e0a-9d42-4cc9-8a63-406963832c04.jpg | 照片资源不可达 | double_404 |
| 广东省第二人民医院 | 廖耀华 | 200 | /static//seygw//resources/upload/2024/05/28/6353983839070312502861929.jpg | 照片资源不可达 | double_404 |
| 广东省第二人民医院 | 陈抒扬 | 200 | /static//seygw//resources/upload/2024/05/28/default_ys.gif | 占位图 | 详情照片位命中显式 default/placeholder 门禁 |
| 广东省第二人民医院 | 刘婷 | 200 | /static//seygw//resources/upload/2024/05/28/default_ys.gif | 占位图 | 详情照片位命中显式 default/placeholder 门禁 |
| 广州中医药大学第一附属医院 | 王超 | 200 |  | 无照片容器 | 详情页无符合既有医院白名单的本人职业照引用 |
| 广东药科大学附属第一医院 | 臧晶 | 200 | files/20260514205657708.JPG | 照片资源不可达 | bounded_transfer_failure |

## 容器与占位诊断

- 省妇幼本人照片位严格沿用 `.expert-detail .detail-head .img-box img`；`/Images/Default/doct.png` 为显式占位。
- 省妇幼页面共享 `/uploads/20250421/99cfbdba…jpg` 经原字节复核为预约二维码，跨页共享且不属于本人照片容器。
- 二维码：HTTP 200，18293 bytes，235×234，SHA-256 `d374158a2f4a485f1b402591def08daac36d1b10e0d6bcfbd5989d597318eb9c`；未落盘。
- 省二医本人照片位严格沿用 `img.col-lg-3.col-6` / `.grjj img`；`default_ys.gif` 为显式默认图。
- 广中医一附沿用 `.zj-list.details` 内既有专家资源白名单；广药附一沿用 `.part1 .img img` 与 `/files/`、`/upsfile/` 既有判例。
- 所有页面仅使用实际引用；未构造、猜测或探测任何未引用路径。

## 请求与保护

- 真实请求：20；最小相邻启动间隔：1.0 秒；串行：True。
- 固定浏览器 UA；未手工注入 Cookie；禁用环境代理；无并发。
- 总底表 JSON/CSV/XLSX、更新报告、入口台账及四院正式画像树前后摘要完全一致。

## 工件

- `work/四院零散照片清尾_photo_backfill_trial_payload.json`
- `work/四院零散照片清尾_photo_backfill_trial_manifest.csv`
- `work/四院零散照片清尾_photo_backfill_trial_report.md`
- `work/四院零散照片清尾_photo_backfill_trial_contact_sheet.jpg`
- `work/四院零散照片清尾_photo_backfill_trial_photos/`
