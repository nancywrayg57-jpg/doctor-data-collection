# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`TRIAL_SCOPE_BLOCKED`（TRIAL-2）。序号 18 已按 owner 裁决跳过（PR #16 合并、Issue #14 关闭、台账留痕）；当前任务为 **Issue #17 序号 22 广东省第二中医院补充试采范围裁决**，完整证据见 PR #19 和当前 Issue ADR。

## GitHub 身份

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`；Claude owner：`nancywrayg57-jpg`
- Codex 不直接推送或合并 `main`，不自行批准业务 PR；远端写入前确认身份为 `xtzhou247`。

## 当前指令

```text
Status: TRIAL_SCOPE_BLOCKED
Phase: TRIAL
LedgerSequence: 22
Hospital: 广东省第二中医院
City: 广州市
OfficialHomeURL: https://www.gdzy5413.com/main/main.aspx
DoctorDirectoryURL: https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850 https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850
AllowedDetailPatterns: doctor/specialist.aspx?typeid=N + ksdoctorinfo（852 同站官方详情）
ReviewStatus: 确认可采集（owner 预核验：入口 curl 200 有效；详情模式 doctor/specialist.aspx?typeid=N；UA 敏感属正常 HTTP 头非绕过）
Difficulty: A-优先自动采集
Task: 852 普查发现白云院区 79 条及淘金/五山门诊 32 条；按“分院区条目熔断回报”停止。等待 owner 明确这些范围是全部纳入、排除白云院区、同时排除院区和门诊，或给出其他精确范围。裁决同步后才抽样试采 10 位（≥3 真实科室），不写入总底表。851 部分无需重试。
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/17
```

执行要点：名医名家为荣誉分类，与各科专家按医生身份（姓名+详情标识）跨模式去重、荣誉归职称/亮眼线索、科室优先真实科室；两块牌子单一实体按"广东省第二中医院"入库；分院区条目熔断回报；遇真实挑战/验证码按既定规则熔断跳过。

## 流程口径（管理员 2026-08-11/12）

领取 Issue 第一步 approve 提示词同步 PR → 试采审计通过 → FULL_APPEND_AND_OBSIDIAN（追加无中途审计）→ **画像审计** → 通过后合并 PR → 关闭 Issue 后才可领取下一家。同时只允许一个 open 任务 Issue。无法采集则跳过。

## 待管理员事项（留痕）

1. 台账序号 10、12 行入口字段修正（PR #6 / Issue #7 留痕）。
2. 存量 5 家医院「亮眼经历线索」导航污染 343 条，待裁决清理。
3. 序号 13『跳过-反爬拦截』（PR #10）；序号 18『跳过-无全院官方目录入口』（PR #16，补全院入口后可复排）。

## 合规红线

1. 仅使用医院官网等官方公开渠道。
2. 禁止绕过登录、验证码、反爬或权限限制；禁第三方平台、患者评价、隐私。
3. 官网没有的信息保持空白，不推断、不补造。
4. 不生成疗效承诺、排名、患者评价或无来源亮点。
