# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`READY`（FULL_APPEND_AND_OBSIDIAN）。Issue #17 序号 22：TRIAL-2 复审**通过**（PR #19 评论 2026-08-12），Codex 获授权完整执行，7 项条件见下方指令块。

## GitHub 身份

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`；Claude owner：`nancywrayg57-jpg`
- 工作分支：`codex/mhrj/issue-17-gdzy5413-trial`；PR：#19；Issue：#17
- Codex 不直接推送或合并 `main`，不自行批准业务 PR。

## 当前指令

```text
Status: READY
Phase: FULL_APPEND_AND_OBSIDIAN
LedgerSequence: 22
Hospital: 广东省第二中医院
City: 广州市
OfficialHomeURL: https://www.gdzy5413.com/main/main.aspx
DoctorDirectoryURL: https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850 https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850
AllowedDetailPatterns: doctor/specialist.aspx?typeid=N + /main/ks/templet2/ksdoctorinfo.aspx（严格五参数）
AuditDecision: 通过
AuditConditions: ①范围=852 全部 346 条+851 的 21 位，身份聚类归并（基线：852 唯一姓名 289、851/852 同名 20，最终唯一人数以归并对账表为准，明显偏离须回报）；②职称以主详情为准，多详情职称不一致写异常提示「多详情职称不一致」，不拼接；③同名实质不同各留一行+「同名待甄别」；④医院字段统一「广东省第二中医院」，院区/门诊归属保留科室原值；⑤异常提示原样入库；⑥擅长前缀剥离、无显式标签留空；⑦归并对账表（346 关系→最终行数推导）列入画像审计材料。
Task: 全量采集并追加统一总底表（--allow-generic-append），检查 XLSX/CSV/更新报告，生成本院 Obsidian 画像并核验索引，清理试采文件，推送 PR #19 请求画像审计后停止。
ObsidianRoot: D:\workspace\信息收集整理\医生画像仓库\01_试点医院
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
