# 2026-08-10 Codex 与 Claude 启动提示词决策

## 背景

管理员提供两份参考附件：

- `C:\Users\zhouxinting\Desktop\资料库\远端 Codex-CICD启动提示词.md`
- `C:\Users\zhouxinting\Desktop\资料库\claude-CICD启动提示词.md`

管理员要求学习附件后，结合当前医生画像采集任务需求文档和执行路线图，编写本任务专用的两份提示词并保存到 `D:\workspace\信息收集整理\docs`。

参考附件中的 GitHub CI/CD、Issue、PR、merge、CODEOWNER、UI 端测内容不直接适用于本项目。本项目迁移其“启动前自检、角色边界、连续承接、门禁、审计结论、熔断、Handoff_State”结构，改写为官方医生数据采集协作流程。

## 决策

1. 新增 `docs\2026-08-10_远端Codex医生画像采集启动提示词.md`。
2. 新增 `docs\2026-08-10_Claude医生画像审计启动提示词.md`。
3. Codex 提示词定位为执行代理：
   - 读取 `Agent.md`、`codex工程经验.md`、路线图、需求文档和最新架构决策。
   - 列出入口台账中已确认 A 级医院。
   - 选择管理员指定医院或下一家未追加医院。
   - 每家医院先试采 10 位医生，不写入总底表。
   - 输出试采结果并等待管理员确认或 Claude 审计。
   - 管理员直接确认，或 Claude 试采审计结论为 `通过` / `有条件通过` 后，Codex 可正式追加；Claude 通过后无需管理员二次确认。
   - 正式追加后检查总底表、生成或补充本院 Obsidian 画像、清理临时文件、记录状态并输出 `Handoff_State`。
   - 本院 Obsidian 画像完成后，才进入下一家医院。
4. Claude 提示词定位为独立审计代理：
   - 不采集、不改表；管理员已授权其试采审计 `通过` / `有条件通过` 结论作为 Codex 追加门禁。
   - 审计试采、正式追加或 Obsidian 画像结果。
   - 检查来源合规、字段错位、非医生页面、异常提示、画像风险。
   - 结论只使用 `通过`、`有条件通过`、`不通过`。
5. 两份提示词均固化合规红线：
   - 仅医院官网等官方公开渠道。
   - 禁止第三方平台、患者评价、隐私、登录或验证码绕过。
   - 官网没有的信息留空，不推断、不补造、不营销包装。
6. 管理员补充确认：Claude 审计试采通过后无需管理员再次确认；每次正式追加总底表后即可开始 Obsidian 画像生成，画像完成后再进入下一家医院。
7. 管理员补充确认：本任务后续使用 GitHub 仓库 `https://github.com/nancywrayg57-jpg/doctor-data-collection.git` 管理代码、文档和采集结果。
8. Codex 作为 developer，GitHub 账号为 `xtzhou247`，负责实现、采集、检查、文档沉淀、工作分支提交和 PR；不得直接推送或合并 `main`。
9. Claude 作为 owner，GitHub 账号为 `nancywrayg57-jpg`，负责审计 Codex 结果、指导下一步、输出 Codex 提示词、审批或合并 PR。
10. Claude 给 Codex 的下一步提示词固定同步到 `D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md`，Codex 新会话启动时必须读取。

## 当前事实

1. 当前统一总底表更新报告曾显示：5 家医院、1993 位医生、37 条异常提示。
2. 已追加医院曾包括：中山大学附属第五医院、中山大学中山眼科中心、南部战区空军医院、中山大学肿瘤防治中心、中山大学附属第三医院。
3. 既有路线图记录下一家未追加 A 级医院为：南方医科大学口腔医院(海珠广场院区)，但提示词要求后续 Agent 执行前必须重新核验入口台账和总底表。
4. Obsidian 状态曾出现路线图旧状态与后续架构决策、现场文件不一致风险；提示词要求涉及画像任务时必须重新核验数量。

## 关键文件

- `D:\workspace\信息收集整理\docs\2026-08-10_远端Codex医生画像采集启动提示词.md`
- `D:\workspace\信息收集整理\docs\2026-08-10_Claude医生画像审计启动提示词.md`
- `D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md`
- `D:\workspace\信息收集整理\Agent.md`
- `D:\workspace\信息收集整理\codex工程经验.md`
- `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md`
- `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md`
