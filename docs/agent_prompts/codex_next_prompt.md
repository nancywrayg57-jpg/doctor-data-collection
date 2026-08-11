# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话必须先读取项目宪法、路线图、需求文档和 Issue #7 最新 ADR。
> 当前状态：`WAITING_CLAUDE_PROFILE_AUDIT`。Issue #7 全量追加、画像生成和验证已完成；推送后只等待 Claude 最终画像审计。

## GitHub 身份

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`
- Claude owner：`nancywrayg57-jpg`
- 工作分支：`codex/mhrj/issue-7-gdskin-trial`
- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/7`

Codex 不直接推送或合并 `main`，不自行批准 PR。任何远端写入前必须再次确认登录身份为 `xtzhou247`。

## 当前动作

```text
Status: WAITING_CLAUDE_PROFILE_AUDIT
Phase: PROFILE_AUDIT
LedgerSequence: 12
Hospital: 南方医科大学皮肤病医院
City: 广州市
OfficialHomeURL: https://www.gdskin.com/
DoctorDirectoryURL: https://www.gdskin.com/Showclass.aspx?id=901 https://www.gdskin.com/Showclass.aspx?id=902 https://www.gdskin.com/Showclass.aspx?id=906 https://www.gdskin.com/Showclass.aspx?id=910 https://www.gdskin.com/Showclass.aspx?id=913 https://www.gdskin.com/Showclass.aspx?id=915 https://www.gdskin.com/Showclass.aspx?id=917 https://www.gdskin.com/Showclass.aspx?id=921 https://www.gdskin.com/ShowClass.aspx?id=922 https://www.gdskin.com/ShowClass.aspx?id=924
ReviewStatus: 确认可采集
Difficulty: A-优先自动采集
Adapter: gdskin_aspnet_expert
AuditDecision: 有条件通过
AuditConditions: ①全量预期约77位，偏离须回报；②同一医生同时属于首席/知名专家和真实科室分类时，科室优先真实科室，荣誉身份保留在职称/亮眼线索，避免总底表科室写成首席专家/知名专家；③核验各入口分页完整性；④924零记录入口留痕跳过；⑤异常提示原样入库；⑥无显式擅长标签留空。
Task: FULL_APPEND_AND_OBSIDIAN 已完成；提交推送本轮全量工件，在 PR #8 请求 Claude 最终画像审计后停止。
```

## Claude 试采审计结论

- 来源：PR #8 owner 评论 `https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/8#issuecomment-5254355944`
- 结论：`有条件通过`
- 授权：`FULL_APPEND_AND_OBSIDIAN`
- 非阻塞修正：将画像生成器的仓库根目录从固定 `D:\workspace\...` 路径改为脚本相对路径，保证跨平台测试可复跑。

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

## FULL_APPEND_AND_OBSIDIAN 完成事实

- 总底表由 2,088 行增至 2,165 行，本院新增 77 行；既有 2,088 行逐字段变化 0。
- 本院 77 个唯一官网来源；单院 payload、总 payload、CSV 逐字段差异 0。
- XLSX 2,165 行 × 23 列与总 payload 逐单元格差异 0；六工作表视觉核验通过，公式错误 0。
- 生成 77 份本院画像与 77 个唯一索引链接，跳过 0，异常提示 4。
- 教育与进修、科研成果、论文产出区块分别命中 61、49、52 份画像，证据门禁差异 0。
- 文海泉、杨斌、陈永锋、顾有守仅有荣誉入口，官网未展示当前科室，科室留空并标记复核。
- 李畅畅、熊明洲、王成、赵培祯无显式擅长标签，擅长字段和画像区块留空，履历进入教育/科研/论文区块。
- Python 编译及 28 项测试通过。

## 管理员新增字段口径

管理员 2026-08-11 明确允许收录医院官网公开的学历、科研和论文段落，并允许在画像模板新增对应区块。

执行口径：

1. 专长字段只保存专长/擅长段落，不混入学历、科研或论文。
2. 学历、科研、论文保留在官方详情正文和亮眼经历证据链中。
3. 画像模板/生成器已增加可选的“教育与进修经历”“科研项目与成果”“论文与学术产出”区块，仅有官方证据时渲染。
4. Claude 已明确下发 `FULL_APPEND_AND_OBSIDIAN`；本轮画像只允许基于正式追加后的统一总底表字段生成。

## 最终画像审计材料

- `work/南方医科大学皮肤病医院_official_doctors_payload.json`
- `医生画像仓库/01_试点医院/南方医科大学皮肤病医院/`
- `医生画像仓库/99_资料来源/南方医科大学皮肤病医院_Obsidian画像生成报告.md`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.xlsx`
- `docs/architecture_decisions/2026-08-11_issue_7_gdskin_full_append.md`

## 当前门禁

1. 精确提交并推送本轮工件后停止，不再执行新的采集或画像写入。
2. 只认 Claude owner 在 PR #8 评论或 Review 中对最终画像明确给出的“通过”“有条件通过”或“不通过”。
3. 若要求返修，只处理 Issue #7、当前分支和 PR #8，先定位证据再做最小修正。
4. 只有最终画像审计通过且 PR #8 已合并关闭，才可领取下一 Issue。
5. 不自行批准或合并 PR，不领取或执行其他 Issue。

## 合规红线

- 仅使用医院官网公开渠道。
- 禁止第三方平台、患者评价、排名、隐私、登录或验证码绕过。
- 官网没有的信息保持空白，不推断、不补造。
- 学历、科研和论文只保留可追溯原文证据，不转化为疗效承诺或无来源营销包装。
