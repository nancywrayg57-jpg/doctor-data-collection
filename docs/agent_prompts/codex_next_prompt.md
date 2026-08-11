# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话必须先读取项目宪法、路线图、需求文档和 Issue #7 ADR。
> 当前状态：`WAITING_CLAUDE_TRIAL_AUDIT`。Issue #7 试采材料已准备，仅等待 Claude owner 审计；禁止正式追加或生成本院画像。

## GitHub 身份

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`
- Claude owner：`nancywrayg57-jpg`
- 工作分支：`codex/mhrj/issue-7-gdskin-trial`
- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/7`

Codex 不直接推送或合并 `main`，不自行批准 PR。任何远端写入前必须再次确认登录身份为 `xtzhou247`。

## 当前动作

```text
Status: WAITING_CLAUDE_TRIAL_AUDIT
Phase: TRIAL
LedgerSequence: 12
Hospital: 南方医科大学皮肤病医院
City: 广州市
OfficialHomeURL: https://www.gdskin.com/
DoctorDirectoryURL: https://www.gdskin.com/Showclass.aspx?id=901 https://www.gdskin.com/Showclass.aspx?id=902 https://www.gdskin.com/Showclass.aspx?id=906 https://www.gdskin.com/Showclass.aspx?id=910 https://www.gdskin.com/Showclass.aspx?id=913 https://www.gdskin.com/Showclass.aspx?id=915 https://www.gdskin.com/Showclass.aspx?id=917 https://www.gdskin.com/Showclass.aspx?id=921 https://www.gdskin.com/ShowClass.aspx?id=922 https://www.gdskin.com/ShowClass.aspx?id=924
ReviewStatus: 确认可采集
Difficulty: A-优先自动采集
Adapter: gdskin_aspnet_expert
Task: 已完成10入口普查和10位试采，不写统一总底表；提交PR后停止，等待Claude给出通过、有条件通过或不通过。
```

## 已验证试采事实

- 10 个入口唯一医生详情数：`1、3、29、7、8、14、6、4、5、0`。
- 906 为 2 页；924 当前没有可采医生详情。
- 入口候选关系 77，按详情 URL 去重后唯一候选 77，现场跨入口重复 0。
- 917 的 `王辉 主管护师` 已排除。
- 试采 10 位、10 个唯一官网详情 URL，覆盖 9 个分类。
- 列表失败 0、详情失败 0、样本异常提示 0。
- CSV 与 payload 逐字段差异 0。
- 总底表 XLSX/CSV、总 payload、更新报告的 SHA-256 均未变化。
- Python 编译及 23 项测试通过。

## 管理员新增字段口径

管理员 2026-08-11 明确允许收录医院官网公开的学历、科研和论文段落，并允许在画像模板新增对应区块。

执行口径：

1. 专长字段只保存专长/擅长段落，不混入学历、科研或论文。
2. 学历、科研、论文保留在官方详情正文和亮眼经历证据链中。
3. 画像模板/生成器已增加可选的“教育与进修经历”“科研项目与成果”“论文与学术产出”区块，仅有官方证据时渲染。
4. 当前仍为 TRIAL，本院未生成任何画像；只有 Claude 试采审计通过并明确下发 `FULL_APPEND_AND_OBSIDIAN` 后才可使用。

## 审计材料

- `work/南方医科大学皮肤病医院_trial_doctors.csv`
- `work/南方医科大学皮肤病医院_trial_payload.json`
- `work/南方医科大学皮肤病医院_trial_report.md`
- `docs/architecture_decisions/2026-08-11_issue_7_gdskin_trial.md`

## 当前门禁

1. Claude owner 只在 PR 评论或 Review 中以“通过”“有条件通过”“不通过”给出有效结论。
2. 未明确通过时，不运行正式追加，不修改统一总底表，不生成本院 Obsidian 画像。
3. Claude 通过后必须先把本文件更新为 `FULL_APPEND_AND_OBSIDIAN`，再执行全量采集、追加、画像和索引核验。
4. 最终画像仍需 Claude 审计；只有画像审计通过且 PR 已合并关闭，才可领取下一 Issue。
5. 本 Issue 完成前不领取或执行其他 Issue，不自行批准或合并 PR。

## 合规红线

- 仅使用医院官网公开渠道。
- 禁止第三方平台、患者评价、排名、隐私、登录或验证码绕过。
- 官网没有的信息保持空白，不推断、不补造。
- 学历、科研和论文只保留可追溯原文证据，不转化为疗效承诺或无来源营销包装。
