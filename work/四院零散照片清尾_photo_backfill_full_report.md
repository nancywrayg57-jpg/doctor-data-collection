# Issue #85 四院零散照片清尾 FULL 报告

> 日期：2026-08-20
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`
> 授权：PR #86 owner comment 2026-08-19T15:25:00Z: TRIAL_AUDIT_PASSED -> FULL_APPEND_AND_OBSIDIAN; fixed four-hospital scope 249; administrator confirmation 2026-08-20 limits execution to Issue #85 / PR #86

## 249 行对账

`249 = 0 补采 + 33 维持留痕 + 216 更新留痕`

| 医院 | 固定范围 | 补采 | 维持留痕 | 更新留痕 |
|---|---:|---:|---:|---:|
| 广东省妇幼保健院 | 174 | 0 | 0 | 174 |
| 广东省第二人民医院 | 48 | 0 | 6 | 42 |
| 广州中医药大学第一附属医院 | 25 | 0 | 25 | 0 |
| 广东药科大学附属第一医院 | 2 | 0 | 2 | 0 |

| 失败分类 | 数量 |
|---|---:|
| 占位图 | 213 |
| 无照片容器 | 28 |
| 照片资源不可达 | 8 |
| 详情不可达 | 0 |

## 数据与画像约束

- 总底表 payload/CSV/XLSX 逐值一致；逐单元格变化 216：{"异常提示": 216}。
- 补采行仅填写照片双列且原异常提示不变；留痕行照片双列保持空白，既有等价判定维持，其他行仅追加幂等失败提示。
- 补采画像 0 份严格 `+2/-0`；失败画像 249 份零触碰；四院 `_索引.md` 零修改。
- 成功照片联系表覆盖 0 张 / 0 页；失败抽样 8 格（每院 2 格）。
- 视觉状态：`PASSED_ALL_FULL_SUCCESS_CONTACT_SHEETS_AND_FAILURE_AUDIT_SAMPLES`。

## 图片大小终审

- 照片总字节 0；最大 0 bytes。
- 超过 5 MiB：0；超过 20 MiB：0（必须为 0）。

- 无

## 合规与请求

- 仅四院官网详情页实际引用；构造未引用路径 0，第三方来源 0，二维码 known-SHA 未落盘。
- 串行请求 265 次，最小相邻启动间隔 1.0 秒；无环境代理、无并发、无手工 Cookie。
- 入口台账、总底表更新报告、退役提示词与 TRIAL 工件保持不变。

## 工件

- `work/四院零散照片清尾_photo_backfill_full_payload.json`
- `work/四院零散照片清尾_photo_backfill_full_reconciliation.csv`
- `work/四院零散照片清尾_photo_backfill_full_report.md`
- `work/四院零散照片清尾_photo_backfill_full_failure_audit_sheet.jpg`
- `work/四院零散照片清尾_photo_backfill_full_success_visual_review/`（补采为 0 时不生成）

## 停止点

完成本地实图与工作簿视觉核验、`--validate-full`、测试、提交、标准推送和 CI 后，在 PR #86 发布 `FULL_DONE`，等待 Owner 终审；不得自行合并、关闭 Issue 或领取下一任务。
