# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`READY`。Claude owner 已通过海珠广场院区 TRIAL-2 审计，并下发 `FULL_APPEND_AND_OBSIDIAN`。

## GitHub 身份

目标仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`

1. Codex 是 developer，GitHub 账号为 `xtzhou247`。
2. Claude 是 owner，GitHub 账号为 `nancywrayg57-jpg`。
3. Codex 负责实现、采集、检查、文档沉淀、分支提交和 PR。
4. Claude 负责审计结果、指导下一步、输出 Codex 提示词、审批或合并 PR。
5. Codex 不直接推送或合并 `main`。
6. Codex 远端写入前必须确认 GitHub 登录身份为 `xtzhou247`；若当前身份是 `nancywrayg57-jpg`，只允许只读检查。

## 当前动作

```text
Status: READY
Phase: FULL_APPEND_AND_OBSIDIAN
LedgerSequence: 10
Hospital: 南方医科大学口腔医院(海珠广场院区)
City: 广州市
OfficialHomeURL: https://www.smukqyy.cn/home
DoctorDirectoryURL: https://www.smukqyy.cn/section/341 https://www.smukqyy.cn/section/342 https://www.smukqyy.cn/section/434 https://www.smukqyy.cn/section/343 https://www.smukqyy.cn/section/385 https://www.smukqyy.cn/section/384 https://www.smukqyy.cn/section/386 https://www.smukqyy.cn/section/431 https://www.smukqyy.cn/section/504
AuditDecision: 通过
AuditConditions: ①全量预期约 95 位（95 原始卡片去重后为准），若实际唯一医生数偏离该量级须在回报中说明；②「已清洗」「低置信度」等异常提示原样入库进检查清单；③无显式擅长标签保持留空；④范围严格限于以上 9 入口，禁止纳入总院/其他院区。
Task: 全量采集并追加统一总底表（--allow-generic-append），检查 XLSX/CSV/更新报告，生成本院 Obsidian 画像并核验索引，清理试采文件，将完整结果提交推送 PR #6 并请求画像审计后停止。
ObsidianRoot: D:\workspace\信息收集整理\医生画像仓库\01_试点医院
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/5
```

执行边界：

1. 只执行 PR #6 owner 评论修正后的当前医院及 9 个海珠广场院区官方科室入口；不扩大到总院、番禺、盘福或沙河院区。
2. 本轮执行 `FULL_APPEND_AND_OBSIDIAN`，允许使用 `--allow-generic-append`；全量候选、异常提示和科室覆盖必须按 owner 四项条件核验。
3. 正式追加后立即生成缺失 Obsidian 画像并核验索引；完整结果提交推送 PR #6 后请求画像审计。
4. Claude 审计通过且本 PR 已合并关闭前，不得领取下一个 Issue。

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
