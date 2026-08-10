# 2026-08-10 doctor-data-collection CI/CD 治理提示词决策

## 目标

基于管理员提供的通用 CI/CD 仓库治理提示词和目标仓库协作事实，形成一份只负责配置目标仓库的治理启动提示词。

## 输入

- `C:\Users\zhouxinting\Desktop\资料库\CICD 仓库治理启动提示词.md`
- `D:\workspace\信息收集整理\Agent.md`
- `D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-10_github_collaboration_model.md`

## 决策

1. 新增 `docs\2026-08-10_CICD仓库治理启动提示词.md`，作为本项目 GitHub 初始化和治理的执行入口。
2. 固定 owner 为 `nancywrayg57-jpg`，developer 为 `xtzhou247`，不保留附件中的占位账号。
3. 仓库日常 PR、审批和 CI 门禁由 Branch protection 负责；Ruleset `main owner gate` 只保留删除保护、非快进保护和线性历史，不启用 `update` / Restrict updates。
4. 空仓库 bootstrap 是 owner 仅有的一次直接创建 `main` 例外；治理 Agent 不导入本地业务项目，后续项目基线由独立开发任务处理。
5. required check 必须先通过真实 PR 发现，固定目标 context 为 `governance-check`，不得用 workflow 显示名称或空壳检查代替。
6. 治理验证只使用无业务含义的验证 PR；不得执行医院选择、试采、正式追加、Obsidian 画像、业务审计或任务提示词流转。
7. 公开仓库不得提交隐私、凭据、缓存、临时文件或无关个人资料；治理 CI 不运行任何项目业务脚本。
8. Actions secrets 当前不在任务范围，禁止设置占位值。

## 2026-08-10 只读现场事实

1. `nancywrayg57-jpg/doctor-data-collection` 为 Public 空仓库，没有默认分支和 refs。
2. 当前 merge commit、rebase merge、squash merge 均开启，自动删除分支关闭，尚未达到目标策略。
3. `xtzhou247` 已是 `write` 协作者。
4. 仓库无 CODEOWNERS、无 Actions workflow、无 Ruleset。
5. 本地 `D:\workspace\信息收集整理` 不是 Git 仓库。
6. 当前 GitHub CLI 登录身份为 owner `nancywrayg57-jpg`；该身份不得用于 Codex 日常开发提交。
7. 上述事实必须在实际治理前重新审计，不能作为永久状态。

## 关键文件

- `D:\workspace\信息收集整理\docs\2026-08-10_CICD仓库治理启动提示词.md`
- `D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-10_cicd_governance_prompt.md`

<Handoff_State>
Target: 为 doctor-data-collection 编写项目专用 CI/CD 仓库治理启动提示词
Completed:
- 已学习通用治理附件
- 已映射真实 GitHub 仓库和角色
- 已将提示词范围收敛为仓库配置和治理验证
- 已加入公开仓库文件边界和空仓库 bootstrap 顺序
- 已记录 2026-08-10 只读仓库快照
CurrentFacts:
- 本轮只写本地文档，未初始化 Git，未修改 GitHub 设置
Next:
- 管理员确认后，将新提示词交给治理 Agent 执行只读审计
- 治理 Agent取得明确授权后再执行 bootstrap 和保护规则配置
Constraints:
- 先审计后写入
- owner 与 developer 身份严格分离
- Ruleset 不启用 update / Restrict updates
- 不配置占位 secrets
Artifacts:
- D:\workspace\信息收集整理\docs\2026-08-10_CICD仓库治理启动提示词.md
</Handoff_State>
