# 2026-08-13 Issue #22 广州医科大学附属口腔医院 TRIAL 与 FULL

## 目标与门禁

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/22
- GitHub PR：https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/24
- 当前 Phase：`FULL_APPEND_AND_OBSIDIAN` 已完成，等待最终画像审计。
- 台账序号：33
- 医院：广州医科大学附属口腔医院
- 官网首页：https://www.gykqyy.com/
- 医生目录：https://www.gykqyy.com/list.html?category=55
- TRIAL 原门禁：只允许普查和 10 位医生试采，样本须覆盖至少 3 个科室，不写统一总底表、不生成正式画像。
- owner `nancywrayg57-jpg` 已于 2026-08-12 在 PR #24 明确审计“通过”并下发 `Phase: FULL_APPEND_AND_OBSIDIAN`，因此 FULL 授权生效。

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
- 有姓名详情 ID：297 个；空姓名详情 ID：0 个；去重姓名值：295 个。
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

## Owner 审计与口径澄清

owner 在 PR #24 的 TRIAL 审计结论为“通过”，并授权全量追加、总表校验、Obsidian 画像和索引核验。指令中的“297 ID 中 2 条无姓名详情”是将 297 个有姓名详情 ID 与 295 个去重姓名值的差额误解为空姓名；现场逐 ID 对账证明：

- 297 个目录唯一详情 ID 全部有姓名，正式保留 297 行。
- 295 是去重后的姓名值数量，差额来自两组同名不同 ID：方颖（128、307）与赵稚宁（29、323）。
- 上述 4 行均分开保留并写入“同名待甄别”，未把真实医生当作空姓名删除。
- 焦点推荐 `id=328` 姓名为空且不在科室医生树中，继续作为范围外空白记录排除，不属于 297 个授权详情 ID。

## FULL 追加与画像结果

- 官网医生-科室关系：317 条；唯一详情 ID：297 个；正式行：297；空姓名：0；详情失败：0。
- 总底表从 2641 行增加至 2938 行，医院数从 9 家增加至 10 家。
- 本院来源链接 297 条且全部唯一；本院 297 行 `已建画像=是`。
- 生成 297 份正式画像与 1 份 `_索引.md`；索引双链 297 条、唯一目标 297 个、缺失目标 0。
- 每份画像只对应 1 个唯一官方来源链接；方颖、赵稚宁 4 份同名画像均保留“同名待甄别”。
- 排除固定“合规边界”免责声明后，业务正文未命中“保证治愈 / 包治 / 疗效第一 / 百分百治愈”等疗效承诺词。
- TRIAL CSV、payload 和报告已按 SOP 清理；正式 payload、全量审计报告、画像缺失报告和正式资产保留。

## 实现与防复发

1. `fetch_json` 对网络异常以及 HTTP 429/500/502/503/504 增加最多 3 次有限重试和递增等待；非 JSON、错误结构与业务失败仍立即按原规则失败，不放宽来源边界。
2. 新增 GYKQYY FULL 写表前门禁，强制核验 317 关系、297 唯一 ID、详情失败 0、正式行等于有姓名 ID、来源链接唯一、逐 ID 对账齐全和同名 4 行标记。
3. 报告分别展示“有姓名详情 ID”“空姓名详情 ID”“去重姓名值”，并输出 297 条逐 ID 归并/排除对账，防止再次混淆 295/297 口径。
4. 画像生成增加 `--refresh-auto-generated`，只刷新带 `AUTO-GENERATED-BY` 标记的脚本画像，不覆盖人工精修画像；异常提示写入画像正文。
5. 离线重建总底表时按画像中的来源链接同步 `已建画像`；同时保留最近一次 FULL 批次元数据，避免为了刷新画像状态而把本院新增 297 行的批次事实覆盖成“无/0”。

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
7. FULL 前只读诊断中详情 ID 179、181 曾瞬时返回 HTTP 502，单独重试均成功；有限重试后正式 FULL 为 0 详情失败。根因是医院官方接口瞬时 5xx，不是稳定数据缺失。
8. 恢复执行时首次 `gh api user` 报 `error connecting to api.github.com`，紧接着 Issue/PR API 查询成功；这进一步证明 GitHub 链路为间歇性网络异常而非持续断网。远端写入前仍必须重新核验身份。
9. FULL 后首次 `--rebuild-master-only` 正确回写了 297 个画像状态，但将报告批次元数据重置为“无/0”；根因是离线重建未携带最近批次元数据。最小修正为只在离线重建时继承现有 master payload 的批次字段，并增加专项测试。

防复发措施：严格域名/路径/分类匹配；接口调用前验证页面声明；JSON Content-Type 和结构防御；网络/429/5xx 有限重试；目录 ID 去重；同名不同 ID 不自动合并；FULL 写表前强门禁；画像只按自动标记刷新；离线重建保留最近批次事实；发布前同时核验 GitHub 身份、远端 head 与本地工件。

## 验证

- Python 编译通过；完整测试集 60 项通过（采集器 51、画像生成器 9）。
- 数据对账：CSV 与 XLSX 均为 2938 行；本院 297 行、297 个唯一 ID/来源、297 个已建画像标记。
- XLSX 为 6 个工作表、6 个表格，主表范围 `A1:W2939`；公式错误扫描 0；全部工作表完成视觉检查，无样式退化。
- 画像对账：297 文件、297 唯一索引双链、缺失目标 0、每份画像 1 个唯一官方来源、疗效承诺式业务断言 0。
- `docs/agent_prompts/codex_next_prompt.md` 保持墓碑内容且无修改。

## 工件

- `work/广州医科大学附属口腔医院_official_doctors_payload.json`
- `work/广州医科大学附属口腔医院_official_doctors_report.md`
- `work/广州医科大学附属口腔医院_obsidian_missing_report.md`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.csv`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.xlsx`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表_更新报告.md`
- `医生画像仓库/01_试点医院/广州医科大学附属口腔医院/`
- `work/collect_official_doctors_batch.py`
- `work/generate_obsidian_profiles.py`
- `work/tests/test_collect_official_doctors_batch.py`
- `work/tests/test_generate_obsidian_profiles.py`
- `Agent.md`
- `docs/2026-08-10_医生画像采集执行路线图.md`

<Handoff_State>
Target: Issue #22 广州医科大学附属口腔医院最终画像审计
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
- owner 已明确 TRIAL 审计通过并授权 FULL_APPEND_AND_OBSIDIAN
- 已正式追加 297 行，总底表共 2938 行；已生成 297 份画像并核验 297 条索引双链
- 已增加有限重试、FULL 写表前强门禁、逐 ID 对账、自动画像安全刷新和离线画像状态同步
CurrentFacts:
- 本院 297 个唯一详情 ID 均有姓名；295 是去重姓名值，不是存在 2 个空姓名详情
- 方颖 128/307、赵稚宁 29/323 共 4 行均分开保留并标记“同名待甄别”
- 总底表 10 家、2938 行；本院 297 行全部已建画像；297 画像/297 索引链接/0 缺失
- GitHub 与医院官网链路存在已证实的瞬时网络异常，正式 FULL 通过有限重试实现 0 详情失败
Next:
- 将当前 FULL 工件非强制推送到 PR #24，并请求 nancywrayg57-jpg 明确给出最终画像审计结论
- 停止业务执行；不得自行合并 PR、关闭 Issue #22 或领取下一 Issue
Constraints:
- 仅医院官网公开页面与页面明确调用的同域公开接口
- 禁止接口猜测、登录/验证码/反爬绕过、第三方平台、患者评价与隐私
- 只有 owner 最终画像审计通过、PR 合并关闭、Issue 关闭且必需 CI 成功后才能检查下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广州医科大学附属口腔医院_official_doctors_payload.json
- D:\workspace\信息收集整理\work\广州医科大学附属口腔医院_official_doctors_report.md
- D:\workspace\信息收集整理\work\广州医科大学附属口腔医院_obsidian_missing_report.md
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\广州医科大学附属口腔医院
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_22_gykqyy_trial.md
</Handoff_State>
