# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`SKIP_AWAITING_OWNER_AUDIT`。Claude owner 已明确裁决 Issue #14 跳过本院；台账序号 18 已按要求留痕，现等待 owner 审计、合并 PR #16 并关闭 Issue #14。

## GitHub 身份

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`；Claude owner：`nancywrayg57-jpg`
- Codex 不直接推送或合并 `main`，不自行批准业务 PR；远端写入前确认身份为 `xtzhou247`。

## 当前指令

```text
Status: SKIP_AWAITING_OWNER_AUDIT
Phase: SKIP
LedgerSequence: 18
Hospital: 广东省中医院芳村分院
City: 广州市
OfficialHomeURL: https://www.gdhtcm.com/college/index_100000301137599.html
DoctorDirectoryURL: https://www.gdhtcm.com/expert/index_100000000817179.html
ReviewStatus: owner 已裁决跳过；台账序号 18 已标记“跳过-无全院官方目录入口”并留痕，未采集医生、未写总底表
Difficulty: A-优先自动采集
Task: 等待 owner 审计本次跳过台账工件、合并 PR #16 并关闭 Issue #14；双门禁完成前不领取序号 22 或任何其他 Issue。若 owner 提出返修，仅处理 Issue #14 原分支和 PR #16。
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/14
```

裁决与工件：owner 在 PR #16 明确选择“跳过本院”，否决仅采 18 位精选子集。台账序号 18 的 `人工复核结果` 已更新为 `跳过-无全院官方目录入口`，`人工备注` 保留两个指定 URL 的实际性质、200+ 与 18 位非全院覆盖差异、未采集/未写总底表及复排条件，`更新时间` 为 2026-08-12。双门禁完成后，通用监控将自动检查 owner 下发的下一家，无需管理员再次发送执行指令。

## 流程口径（管理员 2026-08-11/12）

领取 Issue 第一步 approve 提示词同步 PR → 试采审计通过 → FULL_APPEND_AND_OBSIDIAN（追加无中途审计）→ **画像审计** → 通过后合并 PR → 关闭 Issue 后才可领取下一家。同时只允许一个 open 任务 Issue。

## 待管理员事项（留痕）

1. 台账序号 10、12 行入口字段修正（PR #6 / Issue #7 留痕）。
2. 存量 5 家医院「亮眼经历线索」导航污染 343 条，待裁决清理。
3. 序号 13 已标记『跳过-反爬拦截』（PR #10）。

## 合规红线

1. 仅使用医院官网等官方公开渠道。
2. 禁止绕过登录、验证码、反爬或权限限制；禁第三方平台、患者评价、隐私。
3. 官网没有的信息保持空白，不推断、不补造。
4. 不生成疗效承诺、排名、患者评价或无来源亮点。
