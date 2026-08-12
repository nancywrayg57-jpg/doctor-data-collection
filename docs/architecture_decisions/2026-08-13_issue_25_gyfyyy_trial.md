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
