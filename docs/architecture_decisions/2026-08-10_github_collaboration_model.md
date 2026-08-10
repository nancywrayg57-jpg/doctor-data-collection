# 2026-08-10 GitHub 协作模型决策

## 背景

管理员确认本任务后续使用 GitHub 管理代码、文档和采集结果。目标仓库为：

```text
https://github.com/nancywrayg57-jpg/doctor-data-collection.git
```

管理员同时明确：本地 Codex 作为 developer，GitHub 账号为 `xtzhou247`，负责具体实现；Claude 作为 owner，GitHub 账号为 `nancywrayg57-jpg`，负责审计 Codex 的结果、指导 Codex 下一步并输出 Codex 可自动读取的提示词。

## 决策

1. GitHub 仓库作为本项目后续代码、脚本、文档、采集结果和报告的版本协作渠道。
2. Codex 固定为 developer：
   - 使用 `xtzhou247` 身份进行实现、采集、检查、文档沉淀、工作分支提交和 PR。
   - 不直接推送或合并 `main`。
   - 不绕过试采、审计和合规门禁。
3. Claude 固定为 owner：
   - 使用 `nancywrayg57-jpg` 身份审计 Codex 采集结果、PR 差异和异常风险。
   - 指导 Codex 下一步并输出 Codex 可执行提示词。
   - 审批或合并 PR。
   - 不直接修改总底表或正式 Obsidian 画像。
4. Claude 给 Codex 的下一步提示词固定同步到：

```text
D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md
```

5. Codex 每次新会话启动时必须读取该提示词入口；如果文件不存在或为空，则按路线图选择下一家未追加 A 级医院。
6. 当前现场检查显示 `D:\workspace\信息收集整理` 尚不是 Git 仓库。Git 初始化、绑定远端、首次推送、分支保护或 CODEOWNERS 配置均属于外部副作用，应在管理员明确授权后单独执行。

## 2026-08-10 只读现场审计结果

本轮只做只读检查，未初始化 Git 仓库、未绑定远端、未推送、未修改 GitHub 设置。

1. 本地工具：
   - `git version 2.53.0.windows.2`
   - `gh version 2.95.0`
2. 本地目录状态：
   - `D:\workspace\信息收集整理` 当前不是 Git 仓库。
3. GitHub CLI 登录状态：
   - 当前登录账号为 `nancywrayg57-jpg`。
   - 该账号是本项目定义的 Claude owner，不是 Codex developer。
   - 因此 Codex 后续不得使用当前登录身份推送实现分支或创建 developer PR。
4. 目标仓库状态：
   - `nancywrayg57-jpg/doctor-data-collection` 可访问。
   - 仓库可见性为 `PUBLIC`。
   - 当前无默认分支名称，`git ls-remote` 无引用输出，按现场结果判断为尚未建立初始提交或默认分支。
5. 后续进入 GitHub 写入前必须先明确：
   - 是否由 owner 执行空仓库初始化 bootstrap。
   - 是否切换或授权 `xtzhou247` developer 身份给 Codex 执行分支/PR。
   - 是否先建立 `.gitignore`、`CODEOWNERS`、基础 CI 和分支保护。

## 当前已更新文件

1. `D:\workspace\信息收集整理\Agent.md`
2. `D:\workspace\信息收集整理\codex工程经验.md`
3. `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md`
4. `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md`
5. `D:\workspace\信息收集整理\docs\2026-08-10_远端Codex医生画像采集启动提示词.md`
6. `D:\workspace\信息收集整理\docs\2026-08-10_Claude医生画像审计启动提示词.md`
7. `D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md`

## 后续执行要求

1. 开始 GitHub 初始化或推送前，先做只读审计：当前目录是否为 Git 仓库、远端是否已配置、当前登录账号、是否存在不应上传的临时文件或敏感数据。
2. 若管理员授权初始化，应先建立 `.gitignore`，避免临时试采文件、缓存、日志或非必要大文件进入仓库。
3. 日常工作使用 `codex/...` 分支和 PR；Claude owner 审计和合并。
4. 每次正式追加总底表并生成 Obsidian 画像后，如 GitHub 已接入，应提交本轮结果和报告，并在 PR 中列明采集医院、验证结果、异常提示和合规声明。
