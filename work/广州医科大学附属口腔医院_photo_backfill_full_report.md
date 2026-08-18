# Issue #75 广州医科大学附属口腔医院照片补录 FULL 报告

> 日期：2026-08-19
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`

## 四数对账

| 固定目标 | 实采 | 失败留空 | 正式落盘 |
|---:|---:|---:|---:|
| 297 | 58 | 239 | 58 |

- 复用已审计 TRIAL：10；FULL 新抓取成功：48；新抓取目标：287。
- API category 唯一值：["55"]；其他 category 请求 0；未声明接口探测 0；构造路径 0。

| 失败四类（8 条非 uploads 暂按无照片容器计数，待 Owner 终审） | 数量 |
|---|---:|
| 详情不可达 | 0 |
| 照片资源不可达 | 0 |
| 无照片容器 | 239 |
| 占位图 | 0 |

## 8 条非 uploads image 字段终审清单

- ID 311｜陈璐｜image=`https://www.gykqyy.com`｜判定 `OWNER_FINAL_CLASSIFICATION_REQUIRED`｜UTC 2026-08-18T19:45:51Z
- ID 322｜齐佳｜image=`https://www.gykqyy.com`｜判定 `OWNER_FINAL_CLASSIFICATION_REQUIRED`｜UTC 2026-08-18T19:45:51Z
- ID 323｜赵稚宁｜image=`https://www.gykqyy.com`｜判定 `OWNER_FINAL_CLASSIFICATION_REQUIRED`｜UTC 2026-08-18T19:45:51Z
- ID 324｜朱冠雄｜image=`https://www.gykqyy.com`｜判定 `OWNER_FINAL_CLASSIFICATION_REQUIRED`｜UTC 2026-08-18T19:45:51Z
- ID 325｜蔡东萍｜image=`https://www.gykqyy.com`｜判定 `OWNER_FINAL_CLASSIFICATION_REQUIRED`｜UTC 2026-08-18T19:45:51Z
- ID 326｜闫春阳｜image=`https://www.gykqyy.com`｜判定 `OWNER_FINAL_CLASSIFICATION_REQUIRED`｜UTC 2026-08-18T19:45:51Z
- ID 327｜胡诗琳｜image=`https://www.gykqyy.com`｜判定 `OWNER_FINAL_CLASSIFICATION_REQUIRED`｜UTC 2026-08-18T19:45:51Z
- ID 329｜刘辉｜image=`https://www.gykqyy.com`｜判定 `OWNER_FINAL_CLASSIFICATION_REQUIRED`｜UTC 2026-08-18T19:45:51Z

## 照片与大小

| 大小分桶 | 数量 |
|---|---:|
| <200KiB | 11 |
| 200KiB-1MiB | 45 |
| 1-5MiB | 2 |
| 5-20MiB | 0 |
| >20MiB | 0 |

- 照片总字节 28,129,642（26.83 MiB）；最大 2,202,646 bytes。
- 超过 5 MiB 0；超过 20 MiB 0；状态波动 0。
- 实际格式：{"jpg": 41, "png": 17}；重复 SHA-256 组 0。

## >5 MiB Owner 终审清单

- 无

## 三载体、画像与审计

- 总底表 payload/CSV/XLSX 逐值一致；只修改本院 `照片链接`、`照片文件` 与失败行 `异常提示`。
- 逐单元格变化 355：{"照片链接": 58, "照片文件": 58, "异常提示": 239}。
- FULL reconciliation/manifest 对 58 张逐一复算字节、SHA-256、魔数/扩展名与尺寸；照片目录零孤儿零缺失。
- 成功 58 份 AUTO 画像严格 +2/-0；失败 239 份零触碰；`_索引.md` 零修改。
- 入口台账 JSON/CSV/XLSX、总底表更新报告与全部 TRIAL 工件保持不变。
- FULL 抽样拼图：`work/广州医科大学附属口腔医院_photo_backfill_full_audit_sheet.jpg`（最小、最大、8 个确定性随机样本）。

## 工件

- `work/广州医科大学附属口腔医院_photo_backfill_full_payload.json`
- `work/广州医科大学附属口腔医院_photo_backfill_full_reconciliation.csv`
- `work/广州医科大学附属口腔医院_photo_backfill_full_report.md`
- `work/广州医科大学附属口腔医院_photo_backfill_full_audit_sheet.jpg`
- `医生画像仓库/01_试点医院/广州医科大学附属口腔医院/照片/`（58 张）

## 停止点

`FULL_READY_FOR_FINAL_OWNER_AUDIT`。提交并推送 PR #76 后停止；不得自行合并 PR、关闭 Issue 或领取下一任务。
