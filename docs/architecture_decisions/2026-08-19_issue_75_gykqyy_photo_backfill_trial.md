# Issue #75 广州医科大学附属口腔医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/75>
- 工作分支：`codex/mhrj/issue-75-gykqyy-photo-backfill-trial`
- Phase：`TRIAL`；正式资产必须零修改。
- 固定工作集：总底表本院 297 行既有详情 URL，全部为 `https://www.gykqyy.com/list.html?category=55&id=<ID>`，TRIAL 前 `照片链接`、`照片文件` 全空。
- 唯一允许的数据入口：医生目录页面自身调用的同站公开 `GET https://www.gykqyy.com/api/article/getZhuanjiaList?category=55`，以及响应 `image` 字段实际引用的 `/uploads/<日期>/<hash>.<格式>` 原图。
- 禁止枚举其他 category、探测页面未声明接口、构造未引用照片路径、使用第三方来源或写入正式照片目录。

## category 范围冲突与 Owner 裁决

Issue 原要求 10 人样本覆盖至少两个 category，但领取后只读核验发现：

1. 总底表固定 297 条全部为 category=55。
2. 页面源码只在 `currentId.value == 55` 分支调用 `getZhuanjiaList`。
3. 获准 API 的 384 个含 `image` 字段对象出现记录，其 `yccms_category_id` 全部为 55。

Codex 先在 Issue #75 镜像 `TRIAL_SCOPE_BLOCKED`，未生成工件、未下载照片。Owner 随后明确采纳方案 A：豁免第二 category，固定 category=55；TRIAL 改为覆盖至少两个官网科室（按 `keshi_ids`/科室字段），科室首原子尽量分散，职称分层尽可能覆盖。裁决链接：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/75#issuecomment-5332759199>。

## 页面调用证据与接口防御

新增 `work/gykqyy_photo_backfill_trial.py`，执行以下门禁：

1. 先读取精确目录 URL，并验证 HTML 同时包含 `currentId.value == 55`、`getZhuanjiaList`、`item3.image || './images/null.jpg'` 与 `item3.yccms_category_id`。
2. 只请求带显式 `category=55` 的获准 API；响应必须为 HTTP 200、`application/json`、顶层对象且业务 `code=1`。
3. 只以 `data.list` 科室树中的 297 个公开 ID 为固定工作集；`banner` 仅用于合并同 ID 的非空字段，范围外空白焦点项不进入工作集。
4. API 与总底表执行逐 ID、逐姓名严格对账；来源 URL 只接受精确 HTTPS host、`/list.html`、category=55 与数字 ID。
5. 照片 URL 只接受精确同站 `/uploads/YYYYMMDD/32位十六进制文件名.<jpg|jpeg|png|gif|webp>`，拒绝 query、fragment、其他 host、站点根 URL、`/images/null.jpg` 与公共静态资源。
6. 所有图片响应检查 HTTP、最终 host、Content-Type、魔数、实际扩展名、Pillow 解码尺寸、原始字节 SHA-256 与 20 MiB 熔断；不压缩、不转码。
7. 照片首次不可达时才按 30 秒间隔做第二次请求；若状态波动则抛出 `STATUS_FLICKER_REQUIRES_ISSUE_COMMENT_AND_AGGREGATION`，要求先回报 Issue/PR，再进入 Owner 规定的聚合协议。

## API 固定范围与 image 信号普查

- 分组：5。
- 官网科室：31。
- 医生-科室关系：317。
- `data.list` 唯一固定医生 ID：297，与总底表逐 ID 完全一致。
- `banner` + 科室树含 `image` 字段对象出现次数：384；category 唯一值为 55。
- 297 行 image 信号：有效 `/uploads` 原图 58；空/null image 231；非 `/uploads` 值 8（均不作为原图、不请求）。
- 58 个有效照片候选的职称层：正高 22、副高 36、其他 0。

因此本批无法在“有有效 image 原图”的前提下覆盖主治/医师等“其他”职称层。按 Owner 的“尽可能覆盖”裁决，TRIAL 使用正高 5 + 副高 5，并在报告和 payload 固化这一客观限制；未把无有效 image 的医生伪作照片样本。

## TRIAL 结果

- 固定样本：10 人、10 个不同科室首原子、`keshi_ids` 联集 14 个，满足裁决后的至少两个官网科室门禁。
- 职称层：正高 5、副高 5。
- 照片响应：10/10 HTTP 200；照片失败 0；状态波动 0；越出官网 0。
- 原始照片总字节：5,299,759；最小 188,668；中位数 489,452；平均 529,975；最大 1,081,247。
- >5 MiB：0；>20 MiB：0。
- 排除资源下载 0；其他 category 请求 0；未引用路径构造/探测 0；第三方来源 0。

样本：

| ID | 姓名 | 科室首原子 | 职称层 | bytes |
|---:|---|---|---|---:|
| 195 | 李江 | 越秀院区口腔修复科 | 正高 | 479,630 |
| 136 | 张清彬 | 荔湾院区颞下颌关节科 | 正高 | 561,160 |
| 80 | 江千舟 | 荔湾院区牙体牙髓科 | 正高 | 575,788 |
| 51 | 朴正国 | 荔湾院区口腔颌面外科 | 正高 | 188,668 |
| 110 | 刘畅 | 荔湾院区口腔正畸科 | 正高 | 499,274 |
| 152 | 张云燕 | 越秀院区儿童口腔科 | 副高 | 1,081,247 |
| 5 | 杜发亮 | 专家门诊特诊中心 | 副高 | 465,186 |
| 241 | 余挺 | 越秀院区牙周病科 | 副高 | 516,522 |
| 287 | 熊洁 | 荔湾院区综合急诊科 | 副高 | 459,206 |
| 258 | 张斌 | 正畸与儿童口腔中心 | 副高 | 473,078 |

联系表已目视复核：10/10 均为单人成人职业照，无占位图、二维码、公共装饰、患者、儿童或合影。payload 视觉状态为 `PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。

## 正式资产保护

TRIAL 前后对以下资产执行字节/SHA-256 或目录聚合快照，结果完全一致：

1. 入口台账 JSON/CSV/XLSX。
2. 总底表 JSON/CSV/XLSX 与更新报告。
3. 本院 298 个 Markdown 文件组成的画像树。
4. 正式照片目录（TRIAL 前后均不存在）。

TRIAL 只在 `work/` 下生成独立照片与审计工件；没有修改总底表、正式画像、`_索引.md` 或创建正式照片目录。

## 验证

- Python `py_compile`：通过。
- Issue #75 专项单元测试：11/11 通过，覆盖严格来源 URL、category=55、页面调用标记、JSON Content-Type、API 结构、照片路径、样本层级、既有照片熔断、manifest 留痕和视觉门禁。
- 全仓测试首次被 bundled Python 缺少既有 `requests` 依赖阻断，8 个旧测试模块导入失败、没有业务断言失败；只读核验仓库外既有 `C:\Users\Administrator\AppData\Local\Temp\codex-issue22-python-deps` 后，以 `PYTHONPATH` 注入重跑，全仓 375/375 通过，未安装依赖、未修改仓库或系统环境。
- `--validate`：`TRIAL_VALIDATED samples=10 photos=10`。
- manifest/payload/10 张原图逐一复算字节、SHA-256、魔数/扩展名和尺寸一致；联系表已完成视觉复核。
- 独立重新下载李江、张斌两张代表照片：均 HTTP 200 / `image/jpeg`，字节数与 SHA-256 分别和 TRIAL 工件完全一致。
- 正式资产前后快照完全一致，正式照片目录仍不存在。

## 工件

- `work/gykqyy_photo_backfill_trial.py`
- `work/tests/test_gykqyy_photo_backfill_trial.py`
- `work/广州医科大学附属口腔医院_photo_backfill_trial_payload.json`
- `work/广州医科大学附属口腔医院_photo_backfill_trial_manifest.csv`
- `work/广州医科大学附属口腔医院_photo_backfill_trial_report.md`
- `work/广州医科大学附属口腔医院_photo_backfill_trial_contact_sheet.jpg`
- `work/广州医科大学附属口腔医院_photo_backfill_trial_photos/`（10 张 API image 原图）

## 停止点

当前为 `TRIAL_READY_FOR_OWNER_AUDIT`。提交、标准 Git fast-forward 推送并创建关联 Issue #75 的 PR 后等待 Owner 审计；未取得 Owner 在关联 PR 的明确 `FULL_APPEND_AND_OBSIDIAN` 前，不得写正式资产。

<Handoff_State>
Target: Issue #75 广州医科大学附属口腔医院照片补录 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/75
GitHubRepo: https://github.com/nancywrayg57-jpg/doctor-data-collection.git
Branch: codex/mhrj/issue-75-gykqyy-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- Owner 已裁决固定 category=55，改按官网科室覆盖
- 完成 297 固定 ID 与 API/底表逐 ID 对账
- 完成 10 科室首原子、正高 5 + 副高 5 的 10 张 API image 原始照片 TRIAL
- 完成 manifest、payload、report、联系表、专项测试和正式资产零修改验证
CurrentFacts:
- 固定范围 297；有效 /uploads 照片候选 58，正高 22、副高 36、其他 0
- TRIAL 10 张共 5,299,759 bytes，照片响应 10/10 HTTP 200，状态波动 0
- category 唯一值 55；其他 category 请求、接口探测、路径构造与第三方来源均为 0
- 本院画像树 298 文件；正式照片目录仍不存在；总底表和台账未变化
Next:
- 提交并以标准 Git fast-forward 推送当前分支，创建关联 Issue #75 的 PR
- 等待 Owner TRIAL 审计；仅 Owner 明确下发 FULL_APPEND_AND_OBSIDIAN 后才可写正式资产
Constraints:
- 只请求 category=55 的页面自身公开 API 与 image 字段实际引用原图
- 禁止枚举其他 category、探测未声明接口、构造路径、第三方来源和正式资产写入
- 自动化在 TRIAL 成功提交、推送并进入等待 Owner 审计后恢复 ACTIVE
Artifacts:
- work/gykqyy_photo_backfill_trial.py
- work/tests/test_gykqyy_photo_backfill_trial.py
- work/广州医科大学附属口腔医院_photo_backfill_trial_payload.json
- work/广州医科大学附属口腔医院_photo_backfill_trial_manifest.csv
- work/广州医科大学附属口腔医院_photo_backfill_trial_report.md
- work/广州医科大学附属口腔医院_photo_backfill_trial_contact_sheet.jpg
- work/广州医科大学附属口腔医院_photo_backfill_trial_photos/
- docs/architecture_decisions/2026-08-19_issue_75_gykqyy_photo_backfill_trial.md
</Handoff_State>
