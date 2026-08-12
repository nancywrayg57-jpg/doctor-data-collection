# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`READY`（TRIAL-2，范围已裁决）。Issue #17 序号 22 广东省第二中医院：第一轮 851 试采有条件通过；852 普查触发分院区熔断后，owner 已裁决（PR #19 评论 2026-08-12）——**852 全部 346 条纳入范围**；TRIAL-2 继续执行。

## GitHub 身份

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`；Claude owner：`nancywrayg57-jpg`
- 工作分支：`codex/mhrj/issue-17-gdzy5413-trial`；PR：#19；Issue：#17
- Codex 不直接推送或合并 `main`，不自行批准业务 PR。

## 当前指令

```text
Status: READY
Phase: TRIAL
Round: TRIAL-2
LedgerSequence: 22
Hospital: 广东省第二中医院
City: 广州市
OfficialHomeURL: https://www.gdzy5413.com/main/main.aspx
DoctorDirectoryURL: https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850 https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850
AllowedDetailPatterns: doctor/specialist.aspx?typeid=N + /main/ks/templet2/ksdoctorinfo.aspx（严格五参数）
ScopeRuling: 852 全部 346 条均属本院范围（白云院区 79 条、淘金门诊 24 条、五山门诊 8 条一并纳入；台账仅序号 22 一行，院区/门诊无独立台账行，同一法人实体）。总底表医院字段统一写「广东省第二中医院」，院区/门诊归属保留在科室字段原值或出诊点信息中。
MergeRule: 同名多链接（43 人 57 条关系）按「姓名+详情内容身份」归并——职称/简介实质一致=同一人一行（科室顿号合并、来源取主详情、其余链接记报告）；实质不同=各留一行+异常提示「同名待甄别」。851/852 同名 20 位同规则；851 独有刘军保留。归并对账表（346 id→最终唯一人数）列入 FULL 审计材料。
Task: 按上述范围与归并规则执行真实 TRIAL-2 抽样 10 位（≥3 真实科室，样本须含至少 1 位白云院区条目与至少 1 例多链接归并案例），不写入统一总底表；材料推送 PR #19 后停止等待 Claude 复审。
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/17
```

## 流程口径（管理员 2026-08-11/12）

TRIAL-2 复审通过 → FULL_APPEND_AND_OBSIDIAN（851 的 21 位 + 852 全量按归并规则合并，追加无中途审计）→ **画像审计** → 通过后合并 PR #19 → 关闭 Issue #17 后才可领取下一家。同时只允许一个 open 任务 Issue。

## 待管理员事项（留痕）

1. 台账序号 10、12 行入口字段修正（PR #6 / Issue #7 留痕）。
2. 存量 5 家医院「亮眼经历线索」导航污染 343 条，待裁决清理。
3. 序号 13『跳过-反爬拦截』（PR #10）；序号 18『跳过-无全院官方目录入口』（PR #16，补全院入口后可复排）。

## 合规红线

1. 仅使用医院官网等官方公开渠道。
2. 禁止绕过登录、验证码、反爬或权限限制；禁第三方平台、患者评价、隐私。
3. 官网没有的信息保持空白，不推断、不补造。
4. 不生成疗效承诺、排名、患者评价或无来源亮点。
