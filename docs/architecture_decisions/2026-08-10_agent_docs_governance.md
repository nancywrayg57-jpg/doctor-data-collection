# 2026-08-10 Agent 宪法与 Codex 工程经验沉淀决策

## 背景

管理员要求先学习 `D:\学习资料26.7.9\Agent.md` 和 `D:\学习资料26.7.9\Codex工程经验.md`，再结合当前医生画像采集任务需求，在项目根目录生成本任务专用的 `Agent.md` 和 `codex工程经验.md`。

参考文件来自 ZennoProxy v2 项目，核心可迁移结构包括：项目宪法、每次会话必读、双 Agent 分工、先读后写、诊断优先、门禁、交接信标、工程经验和快速检查清单。ZennoProxy 专属的 GitHub、资金、CI/CD、部署和代理业务内容不迁移到本项目。

## 决策

1. 在项目根目录新增 `Agent.md`，作为本项目唯一 Agent 宪法文件。
2. 在项目根目录新增 `codex工程经验.md`，作为 Codex 执行采集、表格、画像和交接任务时的经验清单。
3. `Agent.md` 固化以下红线：
   - 仅使用医院官网等官方公开渠道。
   - 禁止第三方平台、患者评价、隐私、登录或验证码绕过。
   - 每家医院正式追加前必须先试采 10 位医生。
   - 管理员确认或 Claude 审计通过后才允许正式追加。
   - 官网没有的信息留空，不推断、不补造、不营销改写。
   - 清理前必须列出精确文件，不删除入口台账、总底表、报告和正式画像。
4. `codex工程经验.md` 沉淀以下执行经验：
   - 入口台账是医院入口单点来源。
   - 通用模板先试采，质量不合格再考虑专用适配器。
   - 总底表 XLSX、CSV 和更新报告需要同步检查。
   - 大医院追加可能超时，禁止未确认进程状态时重复写表。
   - Obsidian 画像进入续跑或验收前必须做数量核验。
5. 路线图继续作为具体执行流程依据；根目录 `Agent.md` 作为执行红线和会话启动约束。

## 当前事实

1. `D:\workspace\信息收集整理\Agent.md` 已生成。
2. `D:\workspace\信息收集整理\codex工程经验.md` 已生成。
3. 当前统一总底表更新报告显示：5 家医院、1993 位医生、37 条异常提示。
4. 已追加医院包括：中山大学附属第五医院、中山大学中山眼科中心、南部战区空军医院、中山大学肿瘤防治中心、中山大学附属第三医院。
5. 下一家未追加 A 级医院在既有路线图中记录为：南方医科大学口腔医院(海珠广场院区)，后续执行前仍需重新读取入口台账核验。
6. Obsidian 画像状态存在报告与现场数量不一致风险：已有补充生成报告显示中山大学附属第三医院新生成 780 份画像，但现场 Markdown 计数需要重新专项核验。后续不得直接把旧报告当作画像完成证据。

## 后续 Agent 启动要求

后续 Agent 处理本项目时，先读：

1. `D:\workspace\信息收集整理\Agent.md`
2. `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md`
3. `D:\workspace\信息收集整理\docs\architecture_decisions\` 下与当前任务相关的最新记录

如果任务涉及画像生成或验收，必须先核验：

1. 总底表记录数。
2. 各医院 Markdown 文件数。
3. 各医院 `_索引.md` 链接数。
4. 是否存在重名覆盖、缺失画像或异常姓名。

## 2026-08-10 GitHub 协作补充

管理员确认本任务后续使用 GitHub 仓库 `https://github.com/nancywrayg57-jpg/doctor-data-collection.git` 管理代码、文档和采集结果。`Agent.md` 已补充以下长期规则：

1. Codex 是 developer，GitHub 账号为 `xtzhou247`，负责实现、采集、检查、文档沉淀、工作分支提交和 PR。
2. Claude 是 owner，GitHub 账号为 `nancywrayg57-jpg`，负责审计 Codex 结果、指导下一步、输出 Codex 提示词、审批或合并 PR。
3. Claude 输出给 Codex 的下一步提示词固定同步到 `D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md`。
4. Codex 每次启动时必须读取该提示词入口；如不存在或为空，按路线图执行默认下一步。
5. 当前现场检查显示项目根目录尚不是 Git 仓库；Git 初始化、绑定远端、首次推送和 GitHub 保护规则配置需管理员明确授权后单独执行。

## 关键文件

- `D:\workspace\信息收集整理\Agent.md`
- `D:\workspace\信息收集整理\codex工程经验.md`
- `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md`
- `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md`
- `D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-10_doctor_collection_execution_route.md`
- `D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-10_obsidian_profile_generation.md`
