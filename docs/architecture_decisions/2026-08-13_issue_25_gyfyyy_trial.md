# 2026-08-13 Issue #25 广州医科大学附属第一医院 TRIAL

## 目标与门禁

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/25
- Phase：`TRIAL`
- 台账序号：34
- 医院：广州医科大学附属第一医院
- 官网首页：https://www.gyfyyy.cn/
- 医生目录入口：https://www.gyfyyy.cn/cn/ks/
- 人工复核：确认可采集
- 本阶段只允许普查官方科室树并试采 10 位医生，样本至少覆盖 3 个科室；不得写统一总底表、生成正式 Obsidian 画像或自行进入 FULL。

## 入口普查与页面结构

入口是医院官网静态科室树，不需要调用接口：

- 科室：59 个；59 个 `doctorList.html` 均读取成功，其中 6 个当前无医生列表关系。
- 医生-科室关系：650 条。
- 去重后唯一 `doctor_<id>`：646 个。
- 跨科室详情 ID：4 个：
  - `101` 陈如冲：呼吸与危重症医学科、变态反应科。
  - `549` 陈礼全：妇科、女性盆底专科。
  - `607` 冯励：内科门诊、外科门诊。
  - `618` 潘卫红：内科门诊、外科门诊。
- 纯护理身份候选：9 个，均在正式行生成前排除并写入排除对账。
- 列表分页：无。每个科室的单个 `doctorList.html` 一次性列出团队，没有分页参数或“加载更多”。
- 科室 URL：`/cn/ks/<分类>/<科室>/`，另有 `/cn/ks/<科室>/` 单层路径。
- 专家团队 URL：科室路径下的 `doctorList.html`。
- 医生详情 URL：同一科室路径下的 `doctor_<数字ID>.html`。
- 详情 DOM：姓名只读 `section.doctorcard strong`；职称/身份只读 `section.doctorcard b`；擅长只读 `section.doctorcard p`；简介只读 `section.doctorintro p`。

旧台账候选入口 `/cn/ylfw/czcx/` 当前跳转 404；Issue #25 经 owner 人工复核指定的新入口 `/cn/ks/` 正常。本轮只使用 Issue 指定的新入口。

## 适配器决策

通用模板只能发现入口页的科室链接，不能递归科室专家团队，因此增加最小专用适配器 `gyfyyy_static_department_tree`：

1. 适配器只匹配精确域名 `gyfyyy.cn`、精确路径 `/cn/ks/`，不接受 query、fragment、子域或旧入口。
2. 科室入口只接受同域 `/cn/ks/` 下 1 至 2 层目录路径。
3. 医生详情只接受对应科室路径内的 `doctor_<数字ID>.html`；跨域、跨科室路径、query 和其他页面全部拒绝。
4. 先完整读取 59 个科室团队页，再以数字 ID 归并跨科室归属；同一 ID 只生成一行，科室使用顿号合并。
5. 只有护理身份且没有医师、医士、研究员或教授身份的团队成员排除，并在 payload/report 留痕。
6. TRIAL 选择优先覆盖尚未出现的科室，再补齐至 10 位，保证至少 3 科室。
7. 详情只解析 `doctorcard` 与 `doctorintro`，不会把页面下方患者案例、新闻或其他页面区块写入医生正文。
8. 擅长字段剥离官网固定“擅长”前缀；官网未显示的信息保持空白。
9. 适配器正式追加仍受 `--allow-generic-append` 显式参数和 owner 在关联 PR 中的 `FULL_APPEND_AND_OBSIDIAN` 指令门禁约束。

## 失败、根因、解决与防复发

### 第一次采集验证失败

首次使用现有通用模板执行：

```powershell
--entry-url https://www.gyfyyy.cn/cn/ks/ --trial-only --max-doctors 10 --min-departments 3 --no-xlsx
```

结果为 0 候选、退出码 1，未生成工件、未写总底表。根因不是医院站点断网，而是通用模板只检查当前入口 HTML，不会把科室导航递归为 59 个专家团队页。

解决方法是增加上述严格静态科室树适配器，并在任何第二次真实 TRIAL 前先完成模拟 DOM 专项测试和完整回归测试。防复发措施包括精确 URL 范围、完整科室普查、ID 归并、护理排除、详情 DOM 白名单与最小科室覆盖门禁。

### 网络状态

本轮医院官网入口、59 个团队页和 10 个样本详情均成功读取，真实 TRIAL 为 0 列表错误、0 详情错误；因此当前业务阻塞不由医院官网网络问题造成。此前 GitHub Git HTTPS 曾出现 443 超时，属于 GitHub 链路的间歇性故障；GitHub API 身份及 Issue 查询当前正常。远端发布前仍须重新核验身份、远端 main/head，并使用非强制更新。

### 清洗测试修正

首次增加“擅长”前缀测试时，官网正文为“擅长呼吸……”而不是必带冒号。原正则只处理“擅长：”，导致 1 项单元测试失败；真实采集命令因测试前置失败未执行。最小修正为让冒号可选，随后完整测试 64 项通过并重新生成最终 TRIAL 工件。该失败属于测试阶段的纯解析口径验证，不是第二次真实采集失败。

### Git Data API 提交时区归一化

首次通过 Git Data API 创建远端 commit 对象时，blob、tree、父提交、作者、提交者与消息均一致，但 API 将本地 Git 原始头中的 `+0800` 时区归一化为同一时刻的 `Z/+0000`，导致本地 commit SHA 与 API 返回 SHA 不同。统一 UTC 后第二次保护检查仍停止；逐字节计算进一步确认 GitHub Commit API 还会去掉提交消息末尾的单个 LF：对本地 commit 原始字节只移除最后一个 `\n` 后，计算 SHA 与 API 返回值精确相等。两次保护检查都没有创建或覆盖远端 ref，API 产生的提交对象均无分支引用。

解决方法是在远端分支尚不存在、提交尚未发布的前提下，将本地提交作者/提交者时间统一为 UTC，并通过 Git plumbing 生成无消息末尾 LF 的精确 commit 对象，再用 compare-and-swap 更新当前本地分支 ref；随后重新构建完全一致的远端 commit 并创建新 ref。防复发措施：今后使用 Git Data API 发布前，本地提交时间统一为 UTC、消息尾字节与 API 行为对齐；只有本地/远端 tree、parent、commit SHA 全部相等才创建或更新 ref。

## 最终真实 TRIAL

命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "广州医科大学附属第一医院" `
  --entry-url "https://www.gyfyyy.cn/cn/ks/" `
  --trial-only --max-doctors 10 --min-departments 3 --no-xlsx
```

本机实际使用 Codex bundled Python，并通过仓库外临时依赖目录 `C:\Users\Administrator\AppData\Local\Temp\codex-issue22-python-deps` 注入 `requests`、`beautifulsoup4` 与 `openpyxl`。

结果：

- 试采医生：10 位。
- 覆盖科室：10 个，满足至少 3 科室门禁。
- 详情页失败：0。
- 异常提示：0。
- 非医生页面混入：0；9 个纯护理身份候选均在正式行生成前排除。
- 样本姓名：钟南山、黄铮、肖洁、徐评议、曾文铤、陈学清、陈小燕、陈广原、叶慧玲、余金龙。
- 来源链接：全部为 `https://www.gyfyyy.cn/cn/ks/.../doctor_<数字ID>.html`。
- 使用第三方平台：否。
- 绕过登录、验证码、反爬：否。
- 采集患者评价、排班时段或隐私：否。
- 写入统一总底表：否；XLSX、CSV 和更新报告修改时间均保持本轮执行前状态。
- 生成 XLSX：否。
- 生成正式 Obsidian 画像：否。

## 验证

- `python -m py_compile`：采集器与测试文件通过。
- 新增专项测试：5 项通过，覆盖精确 URL 范围、详情 DOM 白名单、跨科室 ID 归并、护理身份排除、异常行不打标签与 10 位分散采样。
- 完整测试：65 项通过。
- `git diff --check`：通过。
- 最终 payload：59 科室、650 关系、646 唯一 ID、4 个跨科室 ID、9 个护理排除、10 位样本、10 科室覆盖、0 详情失败。

## 工件与下一步

- `work/广州医科大学附属第一医院_trial_payload.json`
- `work/广州医科大学附属第一医院_trial_doctors.csv`
- `work/广州医科大学附属第一医院_trial_report.md`
- `work/collect_official_doctors_batch.py`
- `work/tests/test_collect_official_doctors_batch.py`
- `docs/architecture_decisions/2026-08-13_issue_25_gyfyyy_trial.md`

提交、非强制推送并创建关联 `Closes #25` 的 PR 后停止，等待 `nancywrayg57-jpg` 对 TRIAL 明确给出“通过 / 有条件通过 / 不通过”。只有 owner 明确通过且将 Phase 切换为 `FULL_APPEND_AND_OBSIDIAN` 后，才能在同一 Issue、分支和 PR 内进行全量追加、总底表验证与 Obsidian 画像生成。

<Handoff_State>
Target: Issue #25 广州医科大学附属第一医院 TRIAL 审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/25
Branch: codex/mhrj/issue-25-gyfyyy-trial
InstructionChannel: Issue #25 + 关联 PR owner 评论/Review
Completed:
- 完成 59 科室、650 关系、646 唯一详情 ID 的官方静态科室树普查
- 新增严格 gyfyyy_static_department_tree 适配器与专项测试
- 完成 10 位医生真实 TRIAL，覆盖 10 科室，0 详情失败、0 异常、0 非医生混入
- 未写统一总底表、未生成 XLSX、未生成正式画像
CurrentFacts:
- 4 个跨科室 ID 已按 ID 归并；9 个纯护理身份候选已排除留痕
- 首次通用模板 0 候选根因是缺少科室树递归，不是医院官网断网
- 完整测试 65 项通过，最终 TRIAL 工件已生成
Next:
- 等待 owner 在关联 PR 明确审计 TRIAL；不得自行进入 FULL
Constraints:
- 仅医院官网公开静态页面；禁止第三方、接口探测、登录/验证码绕过、患者评价与隐私
- FULL 必须同时具备 owner 审计通过和 Phase: FULL_APPEND_AND_OBSIDIAN 明确指令
- 不自行合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广州医科大学附属第一医院_trial_payload.json
- D:\workspace\信息收集整理\work\广州医科大学附属第一医院_trial_doctors.csv
- D:\workspace\信息收集整理\work\广州医科大学附属第一医院_trial_report.md
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_25_gyfyyy_trial.md
</Handoff_State>

## FULL_APPEND_AND_OBSIDIAN（2026-08-13）

### Owner 门禁

`nancywrayg57-jpg` 于 PR #26 明确审计 TRIAL 为“通过”，并下发 `Phase: FULL_APPEND_AND_OBSIDIAN`。执行约束包括：59 科室 / 650 关系 / 646 唯一 ID / 9 个纯护理身份排除对账；同名多详情按身份聚类；跨科室归属合并；排班时段不入库；异常提示保留；清理 TRIAL 工件后请求最终画像审计。

### FULL 失败、根因、解决与防复发

1. 第一次 FULL 在正式写表前门禁停止：部分官网详情正文连续出现多个“擅长”前缀，原清洗只剥离一次。该次没有写入正式资产。最小修正为重复剥离全部前缀，并增加专项测试；完整测试随后通过。
2. 初版 FULL 生成 637 个合规详情 ID 行，但把 25 组同名不同 ID 全部简单标记为“同名待甄别”，没有执行 owner 指定的身份聚类。根因是 `collect_gyfyyy` 只有同名计数，没有复用现有的官方字段相似度与身份聚类规则。最小修正后：21 组可由姓名、职称、擅长/简介官方字段确认的同一人归并；4 组实质不同或无法确认的同名保留 8 行并继续标记“同名待甄别”。最终 637 个合规详情 ID 对账为 616 个身份，全部详情 ID 在 `gyfyyy_detail_reconciliation` 与 `gyfyyy_identity_reconciliation` 留痕。
3. 画像生成后曾误先执行 `--rebuild-master-only`；该命令按旧 XLSX（2938 行）重建，短暂把 CSV/JSON 回退到旧基线。根因是 XLSX 尚未完成更新，重建源顺序错误。医院正式 payload、画像和旧 XLSX 均未受损；随后以“旧 XLSX 基线 + 已验证 616 行正式 payload”离线恢复到 3554 行。防复发：当 CSV 已领先 XLSX 时，不得先调用 `--rebuild-master-only`；必须先更新 XLSX，或显式以正式 payload 构建 master。
4. 报告一度把合并后的顿号科室字符串当成一个科室，覆盖统计显示 66。最小修正为按顿号拆分原子科室；排除 2 条姓名格式异常行后的正式覆盖为 53 个原子科室。该问题只影响统计展示，不影响身份或数据行。
5. 最终禁入扫描发现官网 `doctorintro` 白名单区块内仍混有排班字段：103 行详情正文命中“开诊/出诊/每周时段”，其中 10 行还进入亮眼经历线索。根因是 DOM 白名单只排除了页面外部污染，没有剥离白名单区块内部的排班片段。新增统一排班清洗，覆盖带标签排班段、专家/特需门诊每周句、裸“每周出诊”和纯日期时段；离线刷新正式 payload、总表、616 份画像和 XLSX 后，上述四个正式文本字段排班命中均为 0，临床、教育、科研正文保留。防复发测试已加入解析器专项用例。
6. 最终跨格式断言再次发现：本院 official payload 已完成排班清洗，但 master payload / CSV / XLSX 仍保留旧本院文本，10 份自动画像也由旧 master 生成。根因是上一步只刷新了医院正式 payload，master 合并时未显式启用同院刷新，导致同来源旧行被跳过；这不是采集器清洗失效。使用现有 `build_master_payload(..., refresh_incoming=True)` 纯离线原位刷新 616 行（新增 0、跳过 0），随后重建 CSV / XLSX / 报告，并用 `--generate-missing-only --refresh-auto-generated --hospital` 只刷新本院 616 份带自动标记画像和索引，人工画像及其他医院均未覆盖。防复发：正式字段修正必须按“医院 payload → master payload/CSV → XLSX/报告 → 自动画像/索引”顺序同步，并在提交前分别扫描每一层，不能只验证源 payload。

以上没有触发连续 2 次真实采集失败：同名缺口是首次完整结果审计发现并一次修正；重建顺序错误是离线资产构建顺序问题，已从未损坏的正式 payload 一次恢复。

### 最终 FULL 对账

- 官网科室：59；医生-科室关系：650；唯一详情 ID：646。
- 纯护理身份排除：9；合规详情 ID：637。
- 跨科室详情 ID：4，仍按 ID 归并科室归属。
- 同名不同详情 ID：25 组；其中同一人归并 21 组，实质不同同名保留 4 组 / 8 行。
- 最终本院身份：616；列表读取失败 0；详情读取失败 0。
- 最终异常提示行：36，其中同名待甄别 8、职称/身份需人工复核 12、详情正文为空或未识别 11、姓名格式异常 2、多详情职称不一致 4；复合提示会同时计入不同原因。异常行不打疾病标签、不提升优先级。
- 来源链接均为 `https://www.gyfyyy.cn/cn/ks/.../doctor_<数字ID>.html`；主来源 616 个唯一；归并详情链接在身份对账中留痕。
- 总底表从 2938 行增至 3554 行；当前 11 家医院。本院 616 行，`已建画像=是` 616。
- 未使用第三方平台；未绕过登录、验证码或反爬；未入库患者评价、隐私或排班时段。排班禁入扫描覆盖 `擅长诊疗方向摘录`、`亮眼经历线索`、`列表简介`、`详情正文摘录`，最终命中均为 0。

### Obsidian 与 XLSX

- 本院正式画像：616 份；全部带自动生成标记。
- `_索引.md`：616 个唯一 Wiki 链接、616 个唯一官方来源链接；缺失 0、跳过 0。
- 初版 637 份画像中，21 份次要详情链接画像在身份归并后成为本轮未提交冗余自动工件；核验全部带自动标记后精确删除。其他医院、人工画像、总底表和索引未删除。
- 使用 `@oai/artifact-tool` 导入旧 XLSX 并更新原有 6 张工作表，保留表名、列宽、冻结窗格和 `TableStyleMedium2` 蓝白交替样式。
- 最终工作表范围：主表 `A1:W3555`、复核清单 `A1:W327`、科室统计 `A1:B328`、重点范围统计 `A1:B7`、医院统计 `A1:F12`、采集说明 `A1:B23`。
- 六张表均完成顶部视觉渲染；另核验主表尾部、复核清单尾部和医院统计。本院医院统计为医生数 616、待复核 616、已建画像 616；公式错误扫描 0。
- `py_compile` 通过；完整单元测试 69 项通过。最终跨资产断言确认 JSON / CSV / XLSX 均为 3554 行，本院 616 行、616 个唯一主来源、616 份画像、616 个唯一索引 Wiki 链接及官方来源链接；总表四个正式文本字段和全部本院画像的排班命中均为 0。
- 精确清理三份已完成使命的 TRIAL 工件；正式 payload、正式报告、总底表和画像保留。

### 最终工件

- `work/广州医科大学附属第一医院_official_doctors_payload.json`
- `work/广州医科大学附属第一医院_official_doctors_report.md`
- `work/广州医科大学附属第一医院_obsidian_missing_report.md`
- `work/珠三角三甲医院_医生画像自动采集总底表_payload.json`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.csv`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.xlsx`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表_更新报告.md`
- `医生画像仓库/01_试点医院/广州医科大学附属第一医院/`

<Handoff_State>
Target: Issue #25 广州医科大学附属第一医院最终画像审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/25
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/26
Branch: codex/mhrj/issue-25-gyfyyy-trial
InstructionChannel: Issue #25 + PR #26 owner 评论/Review
Completed:
- owner TRIAL 审计通过后完成 FULL_APPEND_AND_OBSIDIAN
- 637 个合规详情 ID 经身份聚类形成 616 个最终身份；21 组同一人归并、4 组同名实质不同保留双行
- 总底表 3554 行，本院 616 行；XLSX/CSV/JSON/报告一致
- 本院 616 份画像与 616 条唯一索引链接完成，TRIAL 工件已清理
CurrentFacts:
- 59 科室、650 关系、646 唯一 ID、9 护理排除、0 列表/详情读取失败
- 本院 36 行带保守异常提示，均保留在画像与索引供最终审计；异常行未打标签
- 当前只等待 owner 最终画像审计、CI、PR 合并和 Issue 关闭双门禁
Next:
- Codex 提交并非强制更新原分支，在 PR #26 请求最终画像审计后停止
- 不自行合并 PR、关闭 Issue 或领取下一 Issue
Constraints:
- 仅官方公开渠道；禁止第三方、患者评价、隐私、登录/验证码绕过和排班时段入库
- 不覆盖其他医院或人工画像，不自行处理其他 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广州医科大学附属第一医院_official_doctors_payload.json
- D:\workspace\信息收集整理\work\广州医科大学附属第一医院_official_doctors_report.md
- D:\workspace\信息收集整理\work\广州医科大学附属第一医院_obsidian_missing_report.md
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\广州医科大学附属第一医院\_索引.md
</Handoff_State>
