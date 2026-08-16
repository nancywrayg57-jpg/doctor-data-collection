# Issue #53 存量治理清理完成与最终审计门禁

> 日期：2026-08-15，完成复核：2026-08-16
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/53>
> 分支：`codex/mhrj/issue-53-governance-cleanup`
> Phase：`GOVERNANCE_COMPLETE_WAITING_OWNER_AUDIT`
> 范围：早期五院离线存量治理；禁止访问官网

## 1. 现场基线

统一总底表 payload、CSV、XLSX 三层现场一致：9,222 行、21 家医院。早期五院行数合计 1,993：中山大学附属第五医院 413、中山大学中山眼科中心 205、南部战区空军医院 52、中山大学肿瘤防治中心 543、中山大学附属第三医院 780。

专项扫描结果：

- `亮眼经历线索` 含导航文本 343 行，全部位于中山大学肿瘤防治中心，与 Issue #53 预估一致。
- 使用补强后的 PR #6 同口径剥离逻辑后，343 行均无导航残留，清洗后留空 0 行。
- `已建画像` 全库分布为“是”8,411、“否”811、空值 0；现有画像来源链接没有任何“非是”匹配项，因此 B 子任务现场回填数为 0。早期五院仍无画像 38 行，全部属于中山大学附属第三医院。
- `异常提示` 含“同名待甄别”258 行；姓名去空格归一后为 121 组，机器规则初判“疑似同一人”8 组、“疑似不同人”113 组。
- 预期逐单元格差异 686 个：`亮眼经历线索` 343、`异常提示` 343；无其他字段变化。

修改前受保护资产：

| 资产 | 字节 | SHA-256 |
|---|---:|---|
| 官网入口台账 XLSX | 39,463 | `59434DCE71B18BDFE1CC1F8CB272903C5FA105526B5DF91A74E83BD2E05C2D68` |
| 总底表 XLSX | 4,427,427 | `DE43F144BC82440BE2F42923A71B8BEF6B619044656FE9C53849B4FAABE55472` |
| 总底表 CSV | 17,366,142 | `E6BE9E931174F96F8581AEFB28CCA0725F920C02859E824FA011873FB5F7C2CE` |
| 总底表更新报告 | 5,604 | `AE2522550F2CF9719A64503F1AD3E8F3A32921EDA59C7AC688E9FF8F1C5757E7` |
| 总底表 payload | 23,718,476 | `2614A8CE8DFB184EE59F38D315FB9DA82513F9848D2DD78A01C763CEEA8DC744` |

## 2. 最小实现决策

1. 在 `strip_profile_navigation_text` 前增加扁平斜杠面包屑剥离：识别 `面包屑 首页 / ... / 叶节点 正文`，删除路径段和重复叶标签，保留医生姓名及正文；沿用 PR #6 的 `extract_clean_highlights` 证据提取口径。
2. `generate_missing_profiles` 增加可选 `refresh_sources`，使 `--refresh-auto-generated` 语义能进一步限制到受影响来源；无自动标记画像仍受保护。
3. 新增 Issue #53 事务脚本：先在临时目录依次构建 payload → CSV/XLSX → 报告 → 画像副本，全部门禁通过后才替换正式资产；替换失败自动回滚。
4. B 子任务只将“字段为空且来源链接实际存在画像”的行回填“是”；不把“否”或其他非空值改写。当前现场为零变更。
5. C 子任务只读生成 Markdown；同名按姓名去空格归一，机器判断优先使用相同来源、照片路径/内容哈希，其次使用同院科室、职称和擅长相似度；结论不回写总底表。

## 3. 验证结果

- `py_compile`：通过。
- 修复人工画像保护哈希误判：`manifest_hash(..., marker_filter=...)` 在筛选自动/人工画像时排除 `_索引.md`，避免合法索引重建触发回滚；全量画像哈希仍保留索引。
- 相关完整 unittest 套件：173 项通过（采集、画像生成、Issue #53 治理脚本，含新增索引哈希回归测试）。
- Issue #53 dry-run：通过，输出 343/0/258/121/686 的现场对账数字。
- `git diff --check`：通过。
- 加载器指定的 `@oai/artifact-tool` 版本 2.8.39 已完成最小 import；总底表与台账均用该运行时导入、逐表渲染并扫描公式错误，结果为 0。
- 总底表 XLSX 与 payload 逐字段比较：9,222 行、25 列、21 院，差异 0；CSV 与 payload 逐字段差异同为 0。
- 台账修改前后全工作簿比较：仅 `K11/W11/X11/K13/W13/X13/V28/W28/X28` 9 个值单元格变化，公式差异 0，非目标单元格差异 0。
- 最终完整 unittest 复跑 173 项通过；`py_compile` 与 `git diff --check` 通过。

## 4. 阻塞历史、根因与恢复

正式事务第一次执行在临时 XLSX 构建门禁停止，错误为：

```text
Error [ERR_MODULE_NOT_FOUND]: Cannot find package '@oai/artifact-tool'
imported from D:\workspace\信息收集整理\work\build_doctor_workbook.mjs
```

根因：Issue #53 声明“XLSX 更新走 FULL 同款既有链路（不依赖 @oai/artifact-tool 的台账技能）”，但仓库当前唯一 FULL XLSX 构建器 `work/build_doctor_workbook.mjs` 第 2 行仍直接导入 `@oai/artifact-tool`；加载器指定的 `C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules` 当前不存在该包。写表链路与 Issue 的运行时假设不一致。

第一次失败的事务未进入正式资产替换阶段，当时上表五份受保护资产哈希全部不变。未使用 openpyxl、Excel COM、LibreOffice 或 OOXML 手改绕过门禁。

恢复条件是管理员恢复加载器提供的 `@oai/artifact-tool`。owner 在 PR #54 下发 `RESUME-APPLY` 后，依赖目录、`package.json` 与最小 import 均已现场通过，正式事务按原方案完成：

```powershell
C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\work\governance_cleanup_issue_53.py --apply
```

正式事务完成 payload → CSV/XLSX → 报告 → 画像副本验证 → 原子替换，并精准刷新中山大学肿瘤防治中心 343 份自动画像及 1 个索引；未新增画像、未覆盖人工/无自动标记画像。原缺包阻断已解除，不再运行 `--apply`，避免在清洗后状态重复执行。

owner 同一指令块同时解锁台账序号 10/12/27：序号 10 改为海珠广场院区 9 个官方入口；序号 12 改为 10 个官方分类入口并保留 924 零记录；序号 27 按 PR #52 证据标为入口不可达/已废弃。台账只改 3 行、9 个值单元格，详细对账见 `docs/2026-08-16_issue_53_台账逐单元格差异.csv`。

## 5. 完成状态与最终哈希

| 资产 | 最终 SHA-256 |
|---|---|
| 官网入口台账 XLSX | `D6B08B3F284654024FAD0EEAC3377B095025DC294732DB030E8CC5B81655B782` |
| 总底表 XLSX | `B61ED7E3E3FA24FC3F61ED7F103DBE684EDB2F341E74098197A9E4D730902834` |
| 总底表 CSV | `648CD892BE28A46E1988BC7836328C741751113986CF6A1D6924321E52F5BD2A` |
| 总底表更新报告 | `7053E0A3B1B7A2A2EAC6C3EE5EB008AF744AE1D8821A05BA00AE98806CE4A11B` |
| 总底表 payload | `30D6FAA36C404B6C39CA4D07D63D117C5D723EDBFAB5D8EF1E7B3FE6FA583D3C` |
| 五院无自动标记画像聚合 | `70A37A506E5033D187F703E7F84E97E503F691BC5AB19FA5C9F3BA48B2A35DFE` |

最终业务对账：A=343/343/0，B=0/38，C=258/121，底表逐单元格差异=686，画像精准刷新=343，索引重建=1，台账=3 行/9 值单元格。当前停止在 owner 最终治理审计门禁；Codex 不批准、不合并 PR，也不领取下一 Issue。

<Handoff_State>
Target: Issue #53 存量亮眼污染清理+已建画像回填+同名甄别辅助表
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/53
Branch: codex/mhrj/issue-53-governance-cleanup
Phase: GOVERNANCE_COMPLETE_WAITING_OWNER_AUDIT
Completed:
- 建立 9,222 行/21 院及受保护资产哈希基线
- 完成 PR #6 导航逻辑补强、来源级自动画像刷新限制、事务脚本及测试
- 完成 A=343/343/0、B=0/38、C=258/121、逐单元格差异=686 的正式治理
- 精准刷新中山大学肿瘤防治中心自动画像 343 份与索引 1 个；人工画像聚合哈希不变
- @oai/artifact-tool 2.8.39 已恢复并通过最小 import、双工作簿逐表渲染和公式错误扫描
- 按 owner RESUME-APPLY 修正台账序号 10/12/27，共 3 行/9 值单元格
- 最终 payload/CSV/XLSX 9,222 行、21 院，逐字段差异 0
Next:
- 提交并通过非强制 Git Data API 更新原分支
- 将 PR #54 转为 Ready，回报最终对账数字并等待 owner 最终治理审计
- owner 审计、CI、PR 合并、Issue 关闭双门禁满足前，不领取下一 Issue
Constraints:
- 纯离线，不访问官网
- 不使用替代 spreadsheet 库、Excel COM 或 OOXML 手改绕过 XLSX 门禁
- 只允许底表行字段“亮眼经历线索”“异常提示”“已建画像”变化
- 台账只允许 owner RESUME-APPLY 明确解锁的序号 10/12/27 三行
Artifacts:
- D:\workspace\信息收集整理\work\governance_cleanup_issue_53.py
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-15_issue_53_governance_cleanup.md
- D:\workspace\信息收集整理\docs\2026-08-15_issue_53_治理清理对账报告.md
- D:\workspace\信息收集整理\docs\2026-08-16_issue_53_台账逐单元格差异.csv
- D:\workspace\信息收集整理\docs\同名待甄别辅助表.md
</Handoff_State>
