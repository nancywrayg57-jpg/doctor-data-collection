# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`READY`（TRIAL）。序号 14 全流程已完成（PR #13 已合并、Issue #11 已关闭，总底表 2299）；当前任务为 **Issue #14 序号 18 广东省中医院芳村分院试采**，完整指令见 Issue #14。

## GitHub 身份

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`；Claude owner：`nancywrayg57-jpg`
- Codex 不直接推送或合并 `main`，不自行批准业务 PR；远端写入前确认身份为 `xtzhou247`。

## 当前指令

```text
Status: READY
Phase: TRIAL
LedgerSequence: 18
Hospital: 广东省中医院芳村分院
City: 广州市
OfficialHomeURL: https://www.gdhtcm.com/college/index_100000301137599.html
DoctorDirectoryURL: https://www.gdhtcm.com/expert/index_100000000817179.html
ReviewStatus: 确认可采集（owner 预核验受限：站点从海外审计环境不可达，Codex 须现场核验可达性与入口性质）
Difficulty: A-优先自动采集
Task: ①核验入口可达性与性质；②【硬门禁】院区归属核验（多院区体系，须确认芳村分院专属/标注，全集团共用无标注则熔断回报）；③普查后试采 10 位（≥3 科室），不写入总底表；材料推送 PR 后停止等待 Claude 审计。
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/14
```

处置规则：现场无法访问或反爬拦截 → 按管理员裁决直接跳过该院（标记+证据回报，owner 关 Issue 后下发序号 22 广东省第二中医院）。

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
