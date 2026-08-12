# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`TRIAL_SCOPE_BLOCKED`。Issue #14 的两个指定 URL 均可达，但院区归属硬门禁不通过；已停止试采并等待 Claude owner 裁决唯一范围。

## GitHub 身份

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`；Claude owner：`nancywrayg57-jpg`
- Codex 不直接推送或合并 `main`，不自行批准业务 PR；远端写入前确认身份为 `xtzhou247`。

## 当前指令

```text
Status: TRIAL_SCOPE_BLOCKED
Phase: TRIAL
LedgerSequence: 18
Hospital: 广东省中医院芳村分院
City: 广州市
OfficialHomeURL: https://www.gdhtcm.com/college/index_100000301137599.html
DoctorDirectoryURL: https://www.gdhtcm.com/expert/index_100000000817179.html
ReviewStatus: 现场可达；指定官网 URL 实为芳村急诊科专科页，指定医生目录实为集团国医大师团队且唯一医生未标注芳村，院区归属硬门禁不通过
Difficulty: A-优先自动采集
Task: 停止 TRIAL，提交入口结构证据并等待 owner 在“芳村完整入口 / 授权仅采名医荟萃中明确标注芳村的 18 位保守子集 / 跳过本院”之间给出唯一裁决；裁决前不采集医生、不写总底表。
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/14
```

现场证据：两个 URL 普通 HTTPS 200；`/college/index_100000301137599.html` 是芳村医院急诊科专科页；`/expert/index_100000000817179.html` 是集团国医大师团队且只有林毅 1 位，其出诊点为二沙、研修楼和大学城。相邻 `名医荟萃` 页面 240 位中仅 18 张卡片明确标注芳村医院，但它不是全院完整目录，Codex 不自行替换入口或范围。

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
