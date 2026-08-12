# 2026-08-13 Issue #22 广州医科大学附属口腔医院试采

## 目标与门禁

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/22
- Phase：`TRIAL`
- 台账序号：33
- 医院：广州医科大学附属口腔医院
- 官网首页：https://www.gykqyy.com/
- 医生目录：https://www.gykqyy.com/list.html?category=55
- 只允许普查和 10 位医生试采，样本须覆盖至少 3 个科室。
- 本阶段不得写统一总底表、不得生成正式 Obsidian 画像；推送 PR 后停止等待 owner 审计。

## 动态页面与接口来源证据

医生目录是 Vue 动态页。目录 HTML 内联脚本明确包含以下页面自身 `axios.get` 调用：

1. `https://www.gykqyy.com/api/article/getZhuanjiaList`
2. `https://www.gykqyy.com/api/article/getArticleDetail`，参数为页面 URL 已公开的 `category_id` 与 `article_id`。

两个接口均为与目录相同的 `www.gykqyy.com` 域名，GET 请求，无鉴权、Cookie、内部参数或验证码。适配器每次执行先读取公开目录 HTML，并且只有在 HTML 同时明确包含上述两个接口时才调用；缺少证据即熔断，防止猜测或探测页面未使用的接口。

页面源码另有普通文章列表分页组件，但医生分类 `currentId == 55` 走 `getZhuanjiaList` 分支，不传 `page`、`pageNo` 或 `pageSize`。因此医生目录实测为 1 个数据页、一次性返回，不存在医生分页请求。Issue 中“有分页”属于执行前预判，以现场页面分支和接口响应为准。

## 入口普查结果

- 医生数据页：1 个。
- 院区/分组：5 个。
- 科室分类：31 个，其中东晓南门诊部当前关系数为 0。
- 医生-科室关系：317 条。
- 去重后唯一详情 ID：297 个。
- 非空唯一姓名：295 个。
- 同名不同 ID：2 组：方颖（128、307），赵稚宁（29、323）。
- 焦点推荐 `id=328` 姓名、科室、职称均为空且不在科室医生树中，排除，不作为医生候选。
- 详情数据方式：按科室树公开 ID 调用页面明确声明的 `getArticleDetail?category_id=55&article_id=<公开ID>`；详情页追溯 URL 为 `list.html?category=55&id=<公开ID>`。

## 站点适配决策

通用 HTML 采集器无法读取 Vue 首屏前的动态医生树，也无法证明其自行发现的接口属于页面调用范围，因此增加最小专用适配器 `gykqyy_public_doctor_api`：

1. 入口仅匹配精确域名 `gykqyy.com`、精确路径 `/list.html` 与 `category=55`。
2. 先检查目录 HTML 的接口声明，再访问接口。
3. 以科室树中的公开详情 ID 为授权候选集合，按 ID 去重，保留多科室归属。
4. TRIAL 采样按官网权重顺序并优先覆盖尚未出现的科室，确保 10 位样本覆盖至少 3 科室。
5. 详情响应必须是 HTTP 200、JSON Content-Type、顶层对象且业务 `code=1`；否则记录失败，不接受 HTML 错误页。
6. 同名不同 ID 不自动合并；后续若进入 FULL，记录应标为“同名待甄别”。

## 真实 TRIAL 结果

命令：

```powershell
python .\work\collect_official_doctors_batch.py --hospital "广州医科大学附属口腔医院" --trial-only --max-doctors 10 --min-departments 3 --no-xlsx
```

本机实际使用 Codex bundled Python，并将缺失的 `requests`、`beautifulsoup4` 临时安装到仓库外目录 `C:\Users\Administrator\AppData\Local\Temp\codex-issue22-python-deps`。

结果：

- 试采医生：10 位。
- 覆盖科室组合：10 个，满足至少 3 科室门禁。
- 详情接口失败：0。
- 异常提示：0。
- 非医生页面混入：0。
- CSV 与 payload 逐字段一致。
- 使用第三方平台：否。
- 绕过登录、验证码或反爬：否。
- 写入总底表：否。
- 生成 Obsidian 正式画像：否。

样本：李江、张清彬、江千舟、朴正国、吴哲、刘畅、申玉芹、杨雪超、王丽萍、曾素娟。

## 治理文档迁移

按 Issue #22 流程变更公告更新：

- `Agent.md` §0 必读清单和 §5 GitHub 协作口径改为“唯一 open 且指派 `xtzhou247` 的任务 Issue + 关联 PR owner 评论/Review”。
- 路线图所有领取、审计与阶段切换条款迁移到同一指令通道。
- `docs/agent_prompts/codex_next_prompt.md` 保持 main 已合并的墓碑内容，不删除、不改写。

## 阻塞、根因、解决与防复发

1. 早期 `git fetch` 多次出现 TLS/连接失败；随后重新 fetch 成功并以 fast-forward 同步到 `origin/main@45f9340`。最终推送前 `git fetch` 又出现 GitHub 443 连接超时，但同轮 GitHub API 身份、remote main 与分支查询成功，目录页、业务接口和真实 TRIAL 也成功。结论是 Git HTTPS 链路存在间歇性网络故障，不是持续断网；使用 GitHub API 复核远端并通过非强制 Git Data API 发布。
2. 默认 `python` 是 Microsoft Store 占位符；改用 bundled Python。
3. bundled Python 缺少 `requests` 与 `beautifulsoup4`；为避免污染仓库和系统环境，仅安装到 Issue 临时目录，并通过 `PYTHONPATH` 注入。
4. 第一次专项单测 mock 返回普通 `object`，缺少 `session.headers`；这是测试桩错误，改为真实空 `requests.Session` 后通过。未修改业务接口逻辑。
5. 执行前预判“医生有分页”与现场事实不一致；适配器不猜测分页接口，以 HTML 实际分支与公开 API 响应为证，并在报告中明确记录为单一数据页。
6. 首次检查远端分支时，PowerShell 将 `gh api` 的 404 JSON 错误正文捕获成非空字符串，误判为分支存在；改为以 `gh` 退出码判断 404，remote main SHA 与本地父提交仍完全一致，未发生远端冲突或写入。

防复发措施：严格域名/路径/分类匹配；接口调用前验证页面声明；JSON Content-Type 和结构防御；目录 ID 去重；同名不同 ID 不自动合并；真实 TRIAL 强制 `--min-departments 3`；总底表与画像目录用 Git 路径 diff 独立确认未改。

## 验证

- 新增 `GykqyyPublicDoctorApiTests`：适配器范围、科室分散采样、页面声明接口门禁与 payload 结构。
- 专项测试通过：3 项；采集器完整测试集通过：50 项。
- Python 编译通过：采集器与测试文件。
- 真实 TRIAL：10 位、10 科室组合、0 详情失败、0 异常。
- 受保护资产：统一总底表 XLSX/CSV/更新报告和 `医生画像仓库/01_试点医院` 均无 Git diff。

## 工件

- `work/广州医科大学附属口腔医院_trial_payload.json`
- `work/广州医科大学附属口腔医院_trial_doctors.csv`
- `work/广州医科大学附属口腔医院_trial_report.md`
- `work/collect_official_doctors_batch.py`
- `work/tests/test_collect_official_doctors_batch.py`
- `Agent.md`
- `docs/2026-08-10_医生画像采集执行路线图.md`

<Handoff_State>
Target: Issue #22 广州医科大学附属口腔医院官方医生 TRIAL 审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/22
GitHubRepo: https://github.com/nancywrayg57-jpg/doctor-data-collection.git
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
InstructionChannel: 唯一 open 且指派 xtzhou247 的任务 Issue + 关联 PR owner 评论/Review
RetiredPromptTombstone: D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md
Completed:
- 已普查医生动态目录：1 个数据页、5 分组、31 科室、317 关系、297 唯一详情 ID
- 已验证页面内联 Vue 脚本明确调用的两个同域公开接口
- 已完成 10 位医生真实试采，覆盖 10 个科室组合，0 详情失败、0 异常
- 已增加最小专用适配器、专项测试和治理文档迁移
CurrentFacts:
- TRIAL 工件已生成，未写统一总底表，未生成正式 Obsidian 画像
- 方颖与赵稚宁分别存在同名不同 ID，FULL 时不得自动合并
- GitHub API 与官网访问正常；Git HTTPS 仍有间歇性 443 超时，发布改走非强制 Git Data API
Next:
- 提交并推送当前分支，创建关联 Issue #22 的 PR
- 停止等待 nancywrayg57-jpg 对 TRIAL 给出明确通过/有条件通过/不通过
- 未收到 owner 明确 FULL_APPEND_AND_OBSIDIAN 指令前禁止全量追加
Constraints:
- 仅医院官网公开页面与页面明确调用的同域公开接口
- 禁止接口猜测、登录/验证码/反爬绕过、第三方平台、患者评价与隐私
- TRIAL 阶段禁止总底表写入和正式画像生成
Artifacts:
- D:\workspace\信息收集整理\work\广州医科大学附属口腔医院_trial_payload.json
- D:\workspace\信息收集整理\work\广州医科大学附属口腔医院_trial_doctors.csv
- D:\workspace\信息收集整理\work\广州医科大学附属口腔医院_trial_report.md
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_22_gykqyy_trial.md
</Handoff_State>
