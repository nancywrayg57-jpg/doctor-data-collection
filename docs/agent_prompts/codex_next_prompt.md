# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`IMAGE_REPAIR_IN_PROGRESS`。Claude owner 的首次画像审计为不通过；当前仅执行 31 条 `亮眼经历线索` 导航污染的最小返修，不得重新追加或扩大范围。

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
Status: IMAGE_REPAIR_IN_PROGRESS
Phase: FULL_APPEND_AND_OBSIDIAN_REPAIR
LedgerSequence: 10
Hospital: 南方医科大学口腔医院(海珠广场院区)
City: 广州市
OfficialHomeURL: https://www.smukqyy.cn/home
DoctorDirectoryURL: https://www.smukqyy.cn/section/341 https://www.smukqyy.cn/section/342 https://www.smukqyy.cn/section/434 https://www.smukqyy.cn/section/343 https://www.smukqyy.cn/section/385 https://www.smukqyy.cn/section/384 https://www.smukqyy.cn/section/386 https://www.smukqyy.cn/section/431 https://www.smukqyy.cn/section/504
AuditDecision: 不通过（画像阶段；其余数量、来源和字段均已通过）
AuditSource: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/6#issuecomment-5252683492
AuditBlocker: 本院 31/95 条亮眼经历线索包含导航文本，且被画像原样渲染。
RepairScope: 仅修正本院 31 行的亮眼经历线索与异常提示；仅覆盖对应 31 份本轮自动画像；不得触碰其他医院、其他字段或人工精修画像。
Task: 复用导航剥离逻辑清洗亮眼经历；无有效经历则留空；增加「亮眼经历含导航文本，已清洗/已清空」提示；同步单院/总 payload、CSV/XLSX 和更新报告；刷新对应 31 份自动画像；保持本院 95 行、95 份画像和 95 个索引链接；新增测试、提交推送 PR #6 并请求 Claude 返修复审。
ObsidianRoot: D:\workspace\信息收集整理\医生画像仓库\01_试点医院
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/5
```

执行边界：

1. 只执行 PR #6 owner 评论修正后的当前医院及 9 个海珠广场院区官方科室入口；不扩大到总院、番禺、盘福或沙河院区。
2. 当前禁止再次运行正式追加或使用 `--allow-generic-append`；底表只允许修改本院受污染 31 行的 `亮眼经历线索` 与 `异常提示`。
3. 画像覆盖只限对应 31 份本轮自动生成文件；不得覆盖其他医院或人工精修画像；索引须保持 95 个有效链接。
4. 返修结果提交并成功推送后请求 Claude 复审；Claude 明确通过且 PR 已合并关闭前，不得领取下一个 Issue。
5. `Doctor data single-Issue monitor` 已在首次完整画像生成并提交推送后启用；当前只监控 Issue #5 / PR #6，不得提前领取下一 Issue。

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
