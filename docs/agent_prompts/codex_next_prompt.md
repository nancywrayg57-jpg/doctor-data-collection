# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`WAITING_FOR_CLAUDE_TARGET`。尚无 Claude 针对具体医院的新指令，Codex 不得自行选择医院或开始采集。

## GitHub 身份

目标仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`

1. Codex 是 developer，GitHub 账号为 `xtzhou247`。
2. Claude 是 owner，GitHub 账号为 `nancywrayg57-jpg`。
3. Codex 负责实现、采集、检查、文档沉淀、分支提交和 PR。
4. Claude 负责审计结果、指导下一步、输出 Codex 提示词、审批或合并 PR。
5. Codex 不直接推送或合并 `main`。
6. Codex 远端写入前必须确认 GitHub 登录身份为 `xtzhou247`；若当前身份是 `nancywrayg57-jpg`，只允许只读检查。

## 当前动作

1. 先读取 `D:\workspace\信息收集整理\Agent.md`、路线图、需求文档和最新架构决策。
2. 当前没有目标医院，停止采集并等待 Claude owner 或管理员更新本文件。
3. 不得从台账自行选择下一家医院，不得沿用旧文档中的“下一家医院”记录。
4. 检查当前目录和 GitHub 身份只能做只读操作；未获明确授权不得初始化仓库或远端写入。

## Claude 下发格式

Claude 选择目标后必须把本文件更新为以下两个阶段之一。

### 试采阶段

```text
Status: READY
Phase: TRIAL
LedgerSequence: <台账序号，当前不得大于 39>
Hospital: <医院名称>
City: <城市>
OfficialHomeURL: <医院官网首页完整 URL>
DoctorDirectoryURL: <医生目录官方入口完整 URL>
ReviewStatus: 确认可采集
Difficulty: <台账采集难度>
Task: 试采 10 位医生，不写入统一总底表；输出试采材料后停止等待 Claude 审计。
```

### 完整执行阶段

```text
Status: READY
Phase: FULL_APPEND_AND_OBSIDIAN
LedgerSequence: <与试采一致>
Hospital: <与试采一致>
City: <与试采一致>
OfficialHomeURL: <与试采一致>
DoctorDirectoryURL: <与试采一致>
AuditDecision: 通过 | 有条件通过
AuditConditions: <无则写“无”>
Task: 全量采集并追加统一总底表，检查 XLSX/CSV/更新报告，生成本院 Obsidian 画像并核验索引，清理试采文件，向 Claude 回报后停止。
ObsidianRoot: D:\workspace\信息收集整理\医生画像仓库\01_试点医院
```

完成台账序号 39 `广州市中医院` 后，Claude 应将状态改为：

```text
Status: STOP_WAITING_FOR_LEDGER_UPDATE
Reason: 管理员当前只标注到序号 39，等待更新入口台账标注。
```

## 合规红线

1. 仅使用医院官网等官方公开渠道。
2. 禁止第三方平台、患者评价、隐私、登录或验证码绕过。
3. 官网没有的信息保持空白，不推断、不补造。
4. 不生成疗效承诺、排名、患者评价或无来源亮点。
