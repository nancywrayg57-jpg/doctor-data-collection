# Issue #53 存量治理清理与 XLSX 写入门禁

> 日期：2026-08-15
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/53>
> 分支：`codex/mhrj/issue-53-governance-cleanup`
> Phase：`GOVERNANCE_WRITE_BLOCKED`
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
- 相关完整 unittest 套件：125 项通过（采集、画像生成、Issue #53 治理脚本）。
- Issue #53 dry-run：通过，输出 343/0/258/121/686 的现场对账数字。
- `git diff --check`：通过。

## 4. 阻塞、根因与处置

正式事务第一次执行在临时 XLSX 构建门禁停止，错误为：

```text
Error [ERR_MODULE_NOT_FOUND]: Cannot find package '@oai/artifact-tool'
imported from D:\workspace\信息收集整理\work\build_doctor_workbook.mjs
```

根因：Issue #53 声明“XLSX 更新走 FULL 同款既有链路（不依赖 @oai/artifact-tool 的台账技能）”，但仓库当前唯一 FULL XLSX 构建器 `work/build_doctor_workbook.mjs` 第 2 行仍直接导入 `@oai/artifact-tool`；加载器指定的 `C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules` 当前不存在该包。写表链路与 Issue 的运行时假设不一致。

事务未进入正式资产替换阶段，临时目录已清理；上表五份受保护资产哈希复核全部不变。未使用 openpyxl、Excel COM、LibreOffice 或 OOXML 手改绕过门禁，也未修改台账或任何画像。

恢复条件：管理员恢复加载器提供的 `@oai/artifact-tool`，或在当前 Issue/关联 PR 明确授权另一条可审计的 XLSX 写入链路。恢复后直接运行：

```powershell
C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\work\governance_cleanup_issue_53.py --apply
```

同一缺包条件下不做无效重试。

<Handoff_State>
Target: Issue #53 存量亮眼污染清理+已建画像回填+同名甄别辅助表
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/53
Branch: codex/mhrj/issue-53-governance-cleanup
Phase: GOVERNANCE_WRITE_BLOCKED
Completed:
- 建立 9,222 行/21 院及受保护资产哈希基线
- 完成 PR #6 导航逻辑补强、来源级自动画像刷新限制、事务脚本及测试
- dry-run 确认 A=343、B=0、C=258 行/121 组、逐单元格差异=686
- 首次正式事务在临时 XLSX 构建门禁停止，正式资产零修改
Next:
- 恢复加载器指定 node_modules 中的 @oai/artifact-tool，或由 owner 明确授权另一 XLSX 链路
- 运行 governance_cleanup_issue_53.py --apply，核验哈希、逐单元格差异、画像及索引
- 生成正式治理报告、同名辅助表和画像刷新后提交同一 PR 审计
Constraints:
- 纯离线，不访问官网
- 不修改官网入口台账，序号 10/12/27 继续挂账
- 不使用替代 spreadsheet 库、Excel COM 或 OOXML 手改绕过 XLSX 门禁
- 只允许底表行字段“亮眼经历线索”“异常提示”“已建画像”变化
Artifacts:
- D:\workspace\信息收集整理\work\governance_cleanup_issue_53.py
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-15_issue_53_governance_cleanup.md
</Handoff_State>
