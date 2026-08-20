# 2026-08-20 Issue #87 导航文本污染清理 TRIAL

## 目标与授权

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/87>。
- 工作分支：`codex/mhrj/issue-87-breadcrumb-cleanup-trial`；基线 `8c591d902e8435d8c203f9f639c8454cd6687601`。
- Phase：`TRIAL`；TaskType：`GOVERN_BREADCRUMB_CLEANUP`。
- 本阶段只允许对总底表 `详情正文摘录` 596 个污染单元格做 dry-run，普查 242 份污染画像，并抽样 10 个官方 DOM 对照；正式总底表、正式画像、入口台账、索引与更新报告零修改。
- Codex 领取评论：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/87#issuecomment-5350803278>。

## 实现与剥离规则

新增 `work/govern_breadcrumb_cleanup_trial.py`，提供 `--trial` 与 `--validate`：

1. 启动时逐值核验 payload/CSV/XLSX 三载体 9,222 行一致。
2. SYSUCC 使用整体特征搜索 `<页面类型> 面包屑 首页 / ... / <页面类型> <站方标题> `，支持 `临床专家`、`科研学者` 与住院医师规范化培训页；不假设只能从字段开头命中。
3. ZSSY 使用重复页标题锚搜索 `导航痕迹 首页 / [专家介绍 /] <页标题> <页标题> `，只把第一个页标题连同 DOM breadcrumb 纳入删除段，保留正文中的第二个页标题。
4. 所有试算值严格为原值前缀 + 原值后缀；不执行 `strip`、空白归一、姓名改写、行性质调整或其他列更新。
5. 如果导航段前紧邻孤立 `'` / `’` / `‘`，只标记 `ISOLATED_QUOTE_PRESERVED_PENDING_OWNER` 并保留该字符，等待 owner 裁决；专项离线测试覆盖该边界。
6. `repository_digest_bytes()` 对 `.md/.csv/.json/.py/.txt/.yaml/.yml` 先做 CRLF/CR → LF，再计算仓库 blob 摘要；XLSX 按原始字节。

## TRIAL 全量对账

底表试算精确闭合：

| 医院 | 污染单元格 | 规则构成 |
|---|---:|---|
| 中山大学肿瘤防治中心 | 506 | 503 临床专家 + 2 科研学者 + 1 住培页 |
| 中山大学附属第三医院 | 90 | 60 专家页 + 30 科室/栏目页 |
| 合计 | 596 | 596 = 506 + 90 |

画像影响精确闭合：

| 医院 | 污染画像 | 导航标记承载次数 |
|---|---:|---:|
| 中山大学肿瘤防治中心 | 204 | 210 |
| 中山大学附属第三医院 | 38 | 78 |
| 合计 | 242 | 288 |

242 份画像均能通过 frontmatter `来源链接` 映射回 596 行工作集；没有画像污染而底表未命中的例外。画像清单记录实际承载行号、区块与重复次数，FULL 不得只假设 `## 详情正文摘录`。

## 八个异型载体与现场差异

当前基线可精确复现 8 份违反常见单行 `临床专家 面包屑` 形态的 SYSUCC 画像：

1. `医学教育.md`：住培页，承载于教育与科研两个区块。
2. `卢雅立.md`：正文前缀 + 两处承载。
3. `周冠群.md`：科研与论文两个区块承载。
4. `宋远斌.md`：教育与科研两个区块承载。
5. `温丽丽.md`：科研与论文两个区块承载。
6. `罗敏.md`：教育与科研两个区块承载。
7. `谢丹.md`：`科研学者` 页面类型。
8. `郑利民.md`：`科研学者` 页面类型。

Owner Issue 预核验写明 8 个异型底表导航段位于字段中段，部分前邻孤立撇号。当前 `main 8c591d90` 的三载体现场却显示：596/596 拟删除段从字符串索引 0 开始，0 行前邻孤立撇号；八个异型只在画像承载布局中精确闭合。TRIAL 保留 search-anywhere 与撇号边界测试，但没有把未复现假设写入正式变更；FULL 前需 owner 对该差异明确裁决。

站方页标题与底表 `姓名` 不同共 16 行：SYSUCC 10 行、ZSSY 6 行。SYSUCC 包括 `刘慧 -> 刘慧(小)` 与 9 个既有姓名污染，ZSSY 6 行均为科室短名与官方完整标题不同。本批全部只留证，不修改姓名、复核状态、异常提示或其他列。

## 刘慧站方变体

底表第 889 行姓名为 `刘慧`，官方页面 `<title>` 与导航终止标题均为 `刘慧(小)`。试算只删除：

```text
临床专家 面包屑 首页 / 临床科室 / 放疗系列 / 放疗科 / 临床专家 刘慧(小)
```

底表姓名继续保留 `刘慧`。匹配逻辑以官方站方页标题作为导航段终止锚，不要求把站方后缀写回姓名。

## 官方 DOM 对照

`requests.Session(trust_env=False)` 使用固定浏览器 UA、无手工 Cookie、无代理、无并发，10 次请求全部串行，最小相邻启动间隔 1.0 秒。仅请求底表现存官方来源链接，不构造新路径。

- SYSUCC 6 行：丘惠娟、张蓓、卢雅立、谢丹、刘慧、郑利民；含 3 个异型画像载体与刘慧站方后缀。
- ZSSY 4 行：刘慧、刘穗玲、余步云、变态反应；含科室名画像。
- 10/10 HTTP 200，均找到 `nav.breadcrumb`；DOM breadcrumb 与拟删除段完全一致或为其严格组成，官方 `<title>` 与导航终止标题一致。

## 正式资产保护

TRIAL 前后以下仓库 blob 摘要完全一致：

1. 官网入口台账 XLSX。
2. 总底表 payload JSON、CSV、XLSX 与更新报告。
3. SYSUCC 与 ZSSY 两院完整画像树。
4. 两院 `_索引.md` 独立摘要。

`formal_assets_modified=False`。本分支只新增 Issue #87 脚本、测试、试算清单、画像影响清单、DOM 证据、TRIAL 摘要与本 ADR。

## 工件与验证

- `work/govern_breadcrumb_cleanup_trial.py`
- `work/tests/test_govern_breadcrumb_cleanup_trial.py`
- `work/GOVERN-2_导航文本污染清理_trial_evidence.json`
- `work/GOVERN-2_导航文本污染清理_trial_manifest.csv`
- `work/GOVERN-2_导航文本污染清理_profile_impact.csv`
- `work/GOVERN-2_导航文本污染清理_dom_evidence.csv`
- `work/GOVERN-2_导航文本污染清理_trial_summary.md`

已通过：

- 脚本与专项测试 `py_compile`。
- Issue #87 专项测试：12/12。
- 全仓 `unittest discover`：526/526。
- `--trial`：`rows=596 profiles=242 dom=10 formal_modified=False`。
- `--validate`：同上，且当前正式资产仍等于 TRIAL 快照。
- `git diff --cached --check`：通过；精确暂存 8 个 Issue #87 文件，禁入工件与密钥模式扫描均无命中。
- 本地 `governance-check` 等价门禁：`SUCCESS`。

当前阶段为 `TRIAL_READY_FOR_OWNER_AUDIT`。只允许精确暂存 Issue #87 实现、测试、五份证据工件与本 ADR，提交后以标准 Git 协议 fast-forward 推送当前分支并创建关闭 Issue #87 的 PR。等待 `governance-check` 成功后发布审计材料并恢复单 Issue 监控；未取得 owner 在当前 PR 明确下发的 FULL 指令前，不得回填正式资产、合并 PR、关闭 Issue 或领取下一任务。

<Handoff_State>
Target: Issue #87 GOVERN-2 导航文本污染清理 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubRepo: https://github.com/nancywrayg57-jpg/doctor-data-collection.git
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/87
Branch: codex/mhrj/issue-87-breadcrumb-cleanup-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 596 个底表单元格 dry-run 闭合为 SYSUCC 506 + ZSSY 90
- 242 份画像影响普查闭合为 SYSUCC 204 + ZSSY 38，288 个实际承载位置
- 8 个异型画像载体、刘慧(小)、16 个站方标题差异与当前 0 中段/0 撇号现场差异已留证
- 10 个官方 DOM 串行对照全部 HTTP 200 且同意拟删除边界
- 正式总底表、画像、索引、台账与报告的仓库 blob 摘要前后完全一致
CurrentFacts:
- 当前只完成 TRIAL，不含任何正式底表或画像更新
- 自动化保持 PAUSED，待提交、推送、PR 与 governance-check 成功后恢复
Next:
- 精确提交并标准非强制推送当前分支，创建关闭 Issue #87 的 PR
- governance-check 成功后在 PR 回报 TRIAL_READY_FOR_OWNER_AUDIT
- 等待 owner 对当前基线 0 中段/0 撇号差异和 FULL 范围作唯一明确裁决
Constraints:
- FULL 前不得写正式总底表或画像
- 只删除导航段，前后正文逐字符保留；不改姓名、行类型、复核状态、异常提示或其他列
- 只认 owner 在关联 PR 的明确阶段指令
Artifacts:
- work/govern_breadcrumb_cleanup_trial.py
- work/tests/test_govern_breadcrumb_cleanup_trial.py
- work/GOVERN-2_导航文本污染清理_trial_evidence.json
- work/GOVERN-2_导航文本污染清理_trial_manifest.csv
- work/GOVERN-2_导航文本污染清理_profile_impact.csv
- work/GOVERN-2_导航文本污染清理_dom_evidence.csv
- work/GOVERN-2_导航文本污染清理_trial_summary.md
- docs/architecture_decisions/2026-08-20_issue_87_breadcrumb_cleanup_trial.md
</Handoff_State>
