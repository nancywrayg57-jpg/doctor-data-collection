# 2026-08-19 Issue #85 四院零散照片清尾 TRIAL

## 目标与授权

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/85>。
- 工作分支：`codex/mhrj/issue-85-photo-backfill-cleanup-trial`；基线 `0266bacec4e9d528469581c0d6268df34abe303a`。
- Phase：`TRIAL`；固定工作集为四院总底表现存 249 条照片双列全空行：广东省妇幼保健院 174、广东省第二人民医院 48、广州中医药大学第一附属医院 25、广东药科大学附属第一医院 2。
- 本阶段只允许复测固定 12 行样本，产出 manifest、payload、报告、灰底联系表、测试和本 ADR；正式总底表、正式画像、入口台账与正式照片目录零修改。
- Codex 领取评论：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/85#issuecomment-5343413918>。

## 熔断、根因与 Owner 裁决

首次 TRIAL 因 12 个样本均无成功照片、旧实现拒绝为空成功集生成联系表而失败。只读现场诊断闭合为 8 个占位图、3 个照片资源不可达、1 个无照片容器。最小修正后第二次 TRIAL 已生成 12 格失败证据联系表，但 payload 元数据仍按原始底表键 `医院` 读取已经规范化为英文 sample schema 的结果，触发 `KeyError`。连续两次真实运行失败后，Codex 依 `Agent.md` 熔断、停止修改和重跑，并先镜像 Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/85#issuecomment-5343759577>。

Owner 随后在 <https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/85#issuecomment-5343802966> 明确发布 `OWNER_RULING → RESUME_TRIAL`：

1. 接受清尾批 `0 成功 / 12 失败` 的合法闭合结果，以及 12 格灰底失败证据联系表和 `PASSED_ZERO_DOWNLOADS_FAILURE_EVIDENCE_CONTACT_SHEET_REVIEW` 视觉状态。
2. Owner 复测确认陈鹏程照片引用 HTTP 301 转 HTTPS 后最终为 HTTP 404；原“可补采”预期作废，以照片资源不可达定格。
3. 批准联系表支持空成功集、`sample_by_hospital` 改读 `hospital`，并补 `run_trial()` 元数据装配离线测试；允许修正后重跑一次 TRIAL。

获准后的唯一重跑成功。旧失败联系表已移入可恢复隔离目录 `C:\Users\Administrator\AppData\Local\Temp\doctor-data-issue85-failed-run-20260819-1504`，未删除受保护文件。

## 实现与固定样本

新增 `work/four_hospital_photo_cleanup_trial.py`，复用 `collect_official_doctors_batch.py` 内四院既有详情解析、照片 URL 白名单、下载重试、魔数与尺寸规则，不新增未引用路径。脚本固定验证 249 行范围和 `5 + 5 + 1 + 1` 样本计划，使用无代理、无手工 Cookie 的串行会话，真实请求相邻启动间隔至少 1 秒。

固定样本：

- 广东省妇幼保健院：贾杰、袁超、秦克旺、陈佳、胡克。
- 广东省第二人民医院：杨莲娣、陈鹏程、廖耀华、陈抒扬、刘婷。
- 广州中医药大学第一附属医院：王超。
- 广东药科大学附属第一医院：臧晶。

新增 `work/tests/test_four_hospital_photo_cleanup_trial.py`，覆盖固定范围、样本构成、必选判例、来源契约、占位门禁、失败四类、命名、仓库 blob 换行归一、manifest 字段、零成功视觉状态，以及 `run_trial()` 规范化 sample schema 的元数据装配。

## TRIAL 四数与现场证据

TRIAL 最终四数为：

| 指标 | 结果 |
|---|---:|
| 固定范围 | 249 |
| TRIAL 样本 | 12 |
| 补采成功 | 0 |
| 失败留痕 | 12 |
| 详情不可达 | 0 |
| 照片资源不可达 | 3 |
| 无照片容器 | 1 |
| 占位图 | 8 |

分院结论：

1. 广东省妇幼保健院 5/5 详情 HTTP 200，严格照片位均引用 `https://wx.e3861.com/sfyAdmin/Images/Default/doct.png`，按显式 default 门禁归为占位图。五页均出现的 `/uploads/20250421/99cfbdba56620ba44a7c2e8b6bec9515.jpg` 原字节为预约二维码：18,293 bytes、235×234、SHA-256 `d374158a2f4a485f1b402591def08daac36d1b10e0d6bcfbd5989d597318eb9c`；作为跨页共享功能图排除且不落盘。
2. 广东省第二人民医院 5/5 详情 HTTP 200。杨莲娣、陈抒扬、刘婷命中 `default_ys.gif` 占位；陈鹏程与廖耀华均保留页面实际引用，唯一重试后两次 HTTP 404，归为照片资源不可达。
3. 广州中医药大学第一附属医院王超详情 HTTP 200，无既有白名单内本人职业照容器，归为无照片容器。
4. 广东药科大学附属第一医院臧晶详情 HTTP 200，页面实际引用 `files/20260514205657708.JPG`，既有有界请求唯一重试后仍传输失败，归为照片资源不可达。

本轮真实请求 20 次，最小相邻启动间隔 1.0 秒；全部串行，无环境代理、手工 Cookie、并发、挑战绕过、第三方来源或未引用路径探测。

## 视觉验收

灰底深色边框联系表共 12 格，逐格显示姓名、医院、科室、职称、失败分类和页面原始引用。逐格目视确认：12/12 格均可见且边界完整，无空白格、不可见格或误导性职业照；8 个占位图、3 个照片资源不可达、1 个无照片容器与 payload 完全一致。

视觉状态为 `PASSED_ZERO_DOWNLOADS_FAILURE_EVIDENCE_CONTACT_SHEET_REVIEW`。该状态只证明失败证据联系表已目视，不声称存在或通过了本人职业照。

## 正式资产保护

TRIAL 前后 `repository_digest_bytes()` 摘要完全一致：

| 受保护资产 | SHA-256 |
|---|---|
| 入口台账 XLSX | `5899390cc2055de16f7ea7d930646f1bb558609d94b4349af2eea940e42fd0c3` |
| 总底表 payload JSON | `2c6599f176d81e9d8b1d5f46ae5aeb1c1539c9878309044847e7dbb2b0ca6fd3` |
| 总底表 CSV | `996f09a64d14ae50d031d1545576212297199530f828d7ba49d7808c04cd221b` |
| 总底表 XLSX | `67aa00a8e99c16d852b89c90a5e357497992b0053308be2d826d70c6acbf54a6` |
| 总底表更新报告 | `e6debbd0d912c1a54dacbf5329a908841a0959e9752faa5be133aa00f613a217` |
| 广东省妇幼保健院正式画像树 | `7a78feb0fff9b252824379c52e958d0ddbe678fa61081ec80901bd84a3bc5638` |
| 广东省第二人民医院正式画像树 | `e072c643fbede5c396b8061af569d5b5321cd308b3d867a2607167d81a153809` |
| 广州中医药大学第一附属医院正式画像树 | `c8aa1bcfee6c8ceb12de7ff4357f9856270b686222c4281b20a77e694eb4c770` |
| 广东药科大学附属第一医院正式画像树 | `93c8b97747dcee79b27870851a7e66a6e42ed5b44facace4bc368479f357edb9` |

## 工件与验证

TRIAL 工件：

- `work/四院零散照片清尾_photo_backfill_trial_payload.json`
- `work/四院零散照片清尾_photo_backfill_trial_manifest.csv`
- `work/四院零散照片清尾_photo_backfill_trial_report.md`
- `work/四院零散照片清尾_photo_backfill_trial_contact_sheet.jpg`
- 成功照片为 0，因此没有创建空的 TRIAL 照片目录。

验证结果：

- `py_compile`：TRIAL 脚本与专项测试通过。
- Issue #85 专项测试：11/11 通过。
- Issue #85 + 四院既有适配器顺序回归：52/52 通过。
- 全仓 `unittest discover`：502/502 通过。
- `--validate`：`scope=249 sample=12 downloaded=0 failed=12`，通过。
- `git diff --check`：通过。

当前阶段为 `TRIAL_READY_FOR_OWNER_AUDIT`。只允许精确暂存 Issue #85 实现、测试、四份工件与本 ADR，核对仓库 blob（LF）哈希后提交，以标准 Git 协议 fast-forward 推送当前分支并创建关闭 Issue #85 的 PR。等待 `governance-check` 成功后在 PR 发布 TRIAL 审计材料并恢复自动监控；未取得 Owner 在当前 PR 明确下发的 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填正式资产、合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #85 四院零散照片补录清尾 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubRepo: https://github.com/nancywrayg57-jpg/doctor-data-collection.git
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/85
Branch: codex/mhrj/issue-85-photo-backfill-cleanup-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 固定 249 行和 12 行样本门禁闭合，现场结果为 0 成功、12 失败
- 失败四类为 0 详情不可达、3 照片资源不可达、1 无照片容器、8 占位图
- 12 格失败证据联系表已目视通过，正式资产前后摘要完全一致
- Issue #85 专项 11/11、四院顺序回归 52/52、全仓 502/502、--validate 通过
CurrentFacts:
- Owner 已接受零成功闭合口径并确认陈鹏程资源 404 判定
- 正式总底表、正式画像、入口台账和正式照片目录均未修改
Next:
- 精确暂存、提交并标准 fast-forward 推送当前分支，创建关联 Issue #85 的 PR
- 等待 governance-check 成功后发布 TRIAL_READY_FOR_OWNER_AUDIT，恢复监控并等待 Owner 审计
Constraints:
- 未取得当前 PR 的 FULL_APPEND_AND_OBSIDIAN 前禁止正式回填
- 仅官方公开来源；不构造未引用路径；失败画像与索引零触碰
Artifacts:
- work/four_hospital_photo_cleanup_trial.py
- work/tests/test_four_hospital_photo_cleanup_trial.py
- work/四院零散照片清尾_photo_backfill_trial_payload.json
- work/四院零散照片清尾_photo_backfill_trial_manifest.csv
- work/四院零散照片清尾_photo_backfill_trial_report.md
- work/四院零散照片清尾_photo_backfill_trial_contact_sheet.jpg
- docs/architecture_decisions/2026-08-19_issue_85_four_hospital_photo_cleanup_trial.md
</Handoff_State>
