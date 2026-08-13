# 2026-08-13 Issue #27 广州医科大学附属第三医院 TRIAL

## 目标与门禁

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/27
- Phase：`TRIAL`
- 台账序号：35
- 医院：广州医科大学附属第三医院
- 官网首页：https://www.gy3y.cn/index
- 医生目录入口：https://www.gy3y.cn/ks/team.html
- 人工复核：确认可采集
- 本阶段只允许普查官方静态总目录并试采 10 位医生，样本至少覆盖 3 个院区科室；不得写统一总底表、生成正式 Obsidian 画像或自行进入 FULL。

## 指令与台账差异裁决

`入口台账` 主表序号 35 与 Issue #27 完全一致，医生目录入口为 `https://www.gy3y.cn/ks/team.html`。同一工作簿的 `人工复核清单` 仍保留旧入口 `https://www.gy3y.cn/kstd/zjjs.html` 且未回填人工结果，属于派生清单滞后；按 `Agent.md` 的唯一指令通道与 owner 明确裁决，本轮只使用 Issue 和入口台账主表共同指定的 `team.html`，未访问旧入口进行采集。

owner 已预先裁决荔湾院区、黄埔院区均属本院同一法人实体并全部纳入；院区归属保留在科室字段。本轮没有提交页面搜索表单，也没有调用或探测非公开接口。

Issue 要求顺带清理上一轮 `work/广州医科大学附属第一医院_trial_report.md`；该文件在本分支最新 `main` 基线已不存在，因此无需额外删除。

## 入口普查与页面结构

入口是一次性静态总目录：

- 目录 DOM：`section.areatab.tab > div.tabcontent > div.tabsingle` 对应两院区；每个院区只读取 `section.ksdoclist > dl > dt/dd` 的正式科室关系。
- 顶部 `section.threedslide` 是推荐轮播，会重复展示医生，适配器明确排除。
- 两院区：荔湾院区、黄埔院区。
- 科室分组容器：14 个 `section.ksdoclist`。
- 科室块：104 个；其中 99 个有医生关系、5 个为空。
- 医生—院区科室关系：580 条；荔湾 390 条，黄埔 190 条。
- 唯一 `doctor_<id>`：438 个；荔湾 370 个，黄埔 185 个，117 个 ID 同时出现在两院区。
- 多院区或多科室关系 ID：126 个，全部按数字 ID 归并院区/科室归属。
- 列表分页：0。单个 `team.html` 一次性给出两院区全部科室关系，无“下一页”或“加载更多”。
- 荔湾详情 URL：`/ks/<系统>/<科室>/doctor_<数字ID>.html`。
- 黄埔详情 URL：`/ks/hp/<系统>/<科室>/doctor_<数字ID>.html`。
- 详情 DOM：姓名只读 `section.doctorcard strong`；职称只读 `section.doctorcard b`；擅长只读 `section.doctorcard p`；简介只读 `section.doctorintro p`。独立 `section.calendar` 不读取。
- 静态总目录只展示姓名，不展示职称身份，无法在不读取 438 个详情的 TRIAL 阶段完成全院护理身份普查；最终 10 位详情样本中纯护理身份排除 0 位。FULL 若获授权，将逐详情应用既有护理身份排除规则并完整留痕。

## 适配器决策

新增最小专用适配器 `gy3y_static_team_directory`，不放宽上一院 `gyfyyy_static_department_tree` 的域名和路径边界：

1. 只匹配精确域名 `gy3y.cn`、精确路径 `/ks/team.html`，拒绝 query、fragment、子域与旧入口。
2. 医生详情只接受上述荔湾或黄埔同域静态路径；跨域、额外路径层级、query 和 fragment 全部拒绝。
3. 只从正式 `ksdoclist/dl/dt/dd` 发现医生关系，排除推荐轮播与搜索表单。
4. 两院区科室统一增加 `荔湾院区` / `黄埔院区` 前缀，同一数字 ID 合并跨院区和跨科室归属。
5. 复用已固化的详情 DOM 白名单、多重“擅长”前缀剥离、排班片段剥离、姓名黑名单、异常行不打标签及纯护理身份排除。
6. TRIAL 优先选入 1 位黄埔独有医生，再按未覆盖科室分散抽样，最终 10 位样本覆盖 10 个原子院区科室，且包含 1 个黄埔主详情与 2 个跨院区 ID。
7. 报告只渲染当前 payload 实际存在的医院专项对账，不再显示其他医院的空专项章节。
8. 适配器正式追加仍受 owner 在关联 PR 中明确 `FULL_APPEND_AND_OBSIDIAN` 指令及 `--allow-generic-append` 显式门禁约束。

## 网络与失败诊断

管理员曾要求确认阻塞是否为网络问题并恢复执行。此前 Git HTTPS 连续两次 443 失败属于 GitHub 链路的间歇性故障；改用 HTTP/1.1 后已成功同步最新 `origin/main`。本轮 GitHub API 身份和 Issue 查询正常，医院官网入口及最终 10 个样本详情均返回成功，因此当前业务任务没有网络阻塞。

恢复执行后的首次诊断命令使用新加载的文档 Python 运行时，该运行时不含项目依赖 `requests`；随后又确认系统 `python` 只是 Microsoft Store 别名。这两次都没有触达医院官网、没有运行采集器、没有生成或修改业务工件。根因是解释器选择，而不是网站或适配器失败；解决方法是沿用前序 ADR 已记录的 Codex bundled Python，并注入仓库外只读临时依赖目录 `C:\Users\Administrator\AppData\Local\Temp\codex-issue22-python-deps`，未安装或改写仓库依赖。

新增报告专项测试首次运行因测试 fixture 缺少模板必需键 `category_error_count` 而失败；只补齐测试元数据后通过，生产采集逻辑未修改。该问题属于模拟测试装配错误，不是第一次或第二次真实采集失败。

## 最终真实 TRIAL

命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "广州医科大学附属第三医院" `
  --entry-url "https://www.gy3y.cn/ks/team.html" `
  --trial-only --max-doctors 10 --min-departments 3 --no-xlsx
```

结果：

- 试采医生：10 位，姓名与来源链接均唯一。
- 覆盖原子院区科室：10 个，满足至少 3 科室门禁。
- 黄埔主详情：1 位；科室字段包含黄埔归属的样本：3 位。
- 样本姓名：江岚、关国晟、李文杰、黄寰、许治强、梁燕玲、周伯荣、魏立平、梁波、周鹏志。
- 详情页失败：0；异常提示：0；非医生页面混入：0；纯护理身份排除：0（仅指本轮 10 位已读取详情）。
- 详情来源均严格匹配 `https://www.gy3y.cn/ks/(hp/)?<系统>/<科室>/doctor_<数字ID>.html`。
- 四个正式文本字段的排班/出诊/每周时段命中：0。
- 未使用第三方平台；未绕过登录、验证码或反爬；未采集患者评价、隐私或排班时段。
- 未写统一总底表、未生成 XLSX、未生成正式 Obsidian 画像。
- 总底表 CSV、XLSX、更新报告在最终 TRIAL 前后 SHA-256 完全一致。

## 验证

- `python -m py_compile`：采集器与测试文件通过。
- 新增 gy3y 专项测试：4 项通过，覆盖精确 URL、正式目录/轮播排除、两院区 ID 归并、黄埔独有样本、10 位分散抽样与医院专属报告章节。
- 最终完整回归：73 项通过。
- TRIAL JSON 与 CSV：10 行逐字段一致。
- 样本姓名 10 个唯一、来源 10 个唯一、来源范围严格通过。
- `git diff --check`：最终提交前执行。

## 工件与下一步

- `work/广州医科大学附属第三医院_trial_payload.json`
- `work/广州医科大学附属第三医院_trial_doctors.csv`
- `work/广州医科大学附属第三医院_trial_report.md`
- `work/collect_official_doctors_batch.py`
- `work/tests/test_collect_official_doctors_batch.py`
- `docs/architecture_decisions/2026-08-13_issue_27_gy3y_trial.md`

提交、非强制推送并创建关联 `Closes #27` 的 PR 后停止，等待 `nancywrayg57-jpg` 对 TRIAL 明确给出“通过 / 有条件通过 / 不通过”。只有 owner 明确通过且在当前 PR 下发 `Phase: FULL_APPEND_AND_OBSIDIAN` 后，才能在同一 Issue、分支和 PR 内进行全量逐详情采集、护理排除对账、同名身份聚类、总底表验证与 Obsidian 画像生成。

<Handoff_State>
Target: Issue #27 广州医科大学附属第三医院 TRIAL 审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/27
Branch: codex/mhrj/issue-27-gy3y-trial
InstructionChannel: Issue #27 + 关联 PR owner 评论/Review
Completed:
- 完成两院区 104 科室块、580 关系、438 唯一详情 ID 的官方静态总目录普查
- 新增严格 gy3y_static_team_directory 适配器与专项测试
- 完成 10 位医生真实 TRIAL，覆盖 10 个原子院区科室，0 详情失败、0 异常、0 排班污染
- 未写统一总底表、未生成 XLSX、未生成正式画像
CurrentFacts:
- 荔湾 390 关系/370 唯一 ID；黄埔 190 关系/185 唯一 ID；117 个 ID 跨两院区
- 126 个 ID 有多院区或多科室关系，按数字 ID 归并并保留院区前缀
- 静态目录无身份字段，TRIAL 只确认 10 位详情纯护理身份排除 0 位；FULL 须逐详情完成全院对账
Next:
- 等待 owner 在关联 PR 明确审计 TRIAL；不得自行进入 FULL
Constraints:
- 仅医院官网公开静态页面；禁止第三方、搜索表单提交、接口探测、登录/验证码绕过、患者评价与隐私
- FULL 必须具备 owner 审计通过和 Phase: FULL_APPEND_AND_OBSIDIAN 明确指令
- 不自行合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广州医科大学附属第三医院_trial_payload.json
- D:\workspace\信息收集整理\work\广州医科大学附属第三医院_trial_doctors.csv
- D:\workspace\信息收集整理\work\广州医科大学附属第三医院_trial_report.md
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_27_gy3y_trial.md
</Handoff_State>
