# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：尚无 Claude 针对具体医院的新审计指令，本文件先作为默认执行入口。

## GitHub 身份

目标仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`

1. Codex 是 developer，GitHub 账号为 `xtzhou247`。
2. Claude 是 owner，GitHub 账号为 `nancywrayg57-jpg`。
3. Codex 负责实现、采集、检查、文档沉淀、分支提交和 PR。
4. Claude 负责审计结果、指导下一步、输出 Codex 提示词、审批或合并 PR。
5. Codex 不直接推送或合并 `main`。
6. Codex 远端写入前必须确认 GitHub 登录身份为 `xtzhou247`；若当前身份是 `nancywrayg57-jpg`，只允许只读检查。

## 默认下一步

1. 先读取 `D:\workspace\信息收集整理\Agent.md`。
2. 再读取 `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md`、需求文档和最新架构决策。
3. 检查当前目录是否已接入 GitHub 仓库；如果不是 Git 仓库，只记录状态，不擅自初始化或推送。
4. 检查 GitHub 登录身份；如不是 `xtzhou247`，不要执行推送、PR 或远端写入。
5. 如管理员要求继续采集，则列出入口台账中已确认 A 级医院。
6. 选择管理员指定医院，或按入口台账顺序选择下一家未追加医院。
7. 先试采 10 位医生，不写入总底表。
8. 输出试采 CSV、报告、payload、样本摘要和异常提示，等待管理员确认或 Claude 审计。
9. 管理员确认通过，或 Claude 审计结论为 `通过` / `有条件通过` 后，正式追加总底表。
10. 正式追加后立即生成或补充本院 Obsidian 医生画像，核验画像数量和索引。
11. 清理无用试采文件，更新架构决策记录和 `<Handoff_State>`。

## 合规红线

1. 仅使用医院官网等官方公开渠道。
2. 禁止第三方平台、患者评价、隐私、登录或验证码绕过。
3. 官网没有的信息保持空白，不推断、不补造。
4. 不生成疗效承诺、排名、患者评价或无来源亮点。
