# 2026-08-13 Issue #31 广州医科大学附属脑科医院 TRIAL

## 目标与门禁

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/31
- 工作分支：`codex/mhrj/issue-31-gzbrain-trial`
- Phase：`TRIAL`
- 台账序号：37
- 医院：广州医科大学附属脑科医院
- 官网首页：https://www.gzbrain.cn/
- 医生目录：https://www.gzbrain.cn/myzj/list.html
- 人工复核：确认可采集（台账难度仍为 `D-待人工补官网`）

本阶段只允许现场核验官方入口、完成全目录关系普查并试采 10 位医生，至少覆盖 3 个科室或分类；不得写统一总底表、生成正式 Obsidian 画像或自行进入 FULL。

## 访问阻塞诊断与合规裁决

owner 预核验环境与本机既有浏览器型 `requests.Session` 对首页和目录返回 nginx HTTP 403，最初表现为网络或站点访问阻塞。诊断只使用普通公开请求，没有提交搜索表单、处理挑战、模拟浏览器指纹、使用代理或第三方数据源。

现场对比确认根因不是本机断网：

- Python 标准库 `urllib` 默认 GET 可从 IIS 正常取得首页、目录、31 个列表页和试采详情页，HTTP 状态均为 200；
- 既有浏览器型 `requests` 会话在相同 URL 上命中 nginx 403；
- 因此这是服务端对客户端请求形态的差异化路由，不是普通网络丢失，也不是目录不可公开访问。

最小解决方案是为本院专用适配器使用 `urllib` 默认非浏览器公开 GET，固定不发送 Cookie、不配置代理、不伪装浏览器、不解答挑战。适配器只允许精确官方域名和静态路径；任何页面读取不完整均在写工件前停止。

## 目录结构与适配器决策

新增专用适配器 `gzbrain_static_expert_directory`：

1. 入口只匹配 `https://www.gzbrain.cn/myzj/list.html`，拒绝 query、fragment、其他子域和其他栏目。
2. 列表分页只接受 `/myzj/list_page_<正整数>.html`；详情只接受 `/myzj/info_itemid_<数字>.html`。
3. 只读取 `.expert_list ul.ul > li` 的正式目录卡片，排除推荐轮播、新闻等非目录链接。
4. 列表卡片提取姓名、职称/科室、专长和排班；排班只用于院区存在性普查，绝不进入医生输出字段。
5. 详情只读取官方医生介绍容器；排班片段和患者案例/病例式可识别叙述在生成正式字段前删除。
6. 纯护理身份按详情职称排除；异常记录不打疾病标签或重点关注标签。
7. `人工复核结果=确认可采集` 是执行授权，`采集难度_初判` 只作为优先级元数据，不再错误要求必须为 A 级。

目录首页分页器只显示当前窗口和末页，例如 `1、2、3、4、31`，不会渲染全部中间页码。首次修正后的真实 TRIAL 因代码错误要求“所有中间页码都必须可见”而停止，报错为 `官网专家目录分页编号不连续。`。根因是把稀疏分页导航误当成完整页码清单，不是官网断页或网络失败。

解除熔断后做最小修正：以严格白名单解析出的最大页码作为末页，并生成 `1..末页` 的完整静态 URL；每一页仍必须真实返回 200，否则整次普查失败。新增 `1、2、31` 稀疏分页回归测试，防止再次把窗口分页误判为缺页。

## 全目录普查

- 静态列表页：31 页，全部读取成功。
- 医生目录关系：183 条。
- 唯一详情 ID：183 个，无跨页重复 ID。
- 有姓名详情 ID：183 个；空姓名详情 ID：0。
- 去重后的非空姓名：181 个。
- 同名不同详情 ID：2 组：沈峰（551、102037），王丹逢（990、1231）。
- 科室分类：35 个；182 条关系有科室，1 条关系科室为空。
- 排班文本中的院区/地点存在性证据：芳村 153、荔湾 35、江村 13、白云 2、总部 1。该证据未进入医生职业字段。
- 列表页失败：0；范围外详情关系：0；跨入口重复：0。

## 最终真实 TRIAL

命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "广州医科大学附属脑科医院" `
  --trial-only --max-doctors 10 --min-departments 3 --no-xlsx
```

结果：

- 试采 10 位：宁玉萍、黄兴兵、周亮、郭建雄、黄雄、唐牟尼、徐贵云、周素妙、张继辉、韩为。
- 覆盖 10 个科室：神经内科、精神科、社区精神科、慢性病科、物质依赖科、老年精神科、情感障碍科、中西医结合科、睡眠与节律医学中心、中医科。
- 10 个姓名唯一、10 个来源链接唯一，来源全部严格匹配 `https://www.gzbrain.cn/myzj/info_itemid_<数字>.html`。
- 详情页失败 0、异常提示 0、非医生页面混入 0、护理身份排除 0。
- 医生正式文本字段中的排班/时段命中 0；患者案例或患者可识别内容命中 0。
- `schedule_field_ingested_count=0`，`patient_case_exclusion_count=0`；本轮样本详情本身未出现需要删除的患者案例句。
- 未使用第三方平台，未绕过登录、验证码或反爬，未采集患者评价、隐私或排班时段。
- 使用 `--trial-only --no-xlsx`，未写统一总底表、未生成 XLSX、未生成正式 Obsidian 画像。

## 验证

- 采集测试完整回归：75 项通过。
- 稀疏分页专项：从可见 `1、2、31` 正确生成 31 个页面 URL。
- CSV 经独立表格运行时导入：`A1:W11` 为 11 行 × 23 列（表头 + 10 位医生），结构可解析。
- TRIAL JSON/CSV：10 位医生，31 页、183 个唯一详情 ID、10 科室、0 列表错误、0 详情错误。
- 来源 URL 白名单、排班文本、患者案例/可识别信息均做逐字段扫描，违规命中为 0。
- `git diff --check`：通过。
- 统一总底表 CSV、XLSX、更新报告 SHA-256 与运行前基线完全一致：
  - CSV：`918fcf9e3d605c422e5f597b10726e3076700473656c1f149235edc91fa758d3`
  - XLSX：`b43be2a2cf7c4c05bfb6e5d021f0e21ff6bb4cc21532425bc1b18c1b2ff2961b`
  - 更新报告：`4576d2bec851d561cf10d4f7ce449b62401f32f0118b7c9545641814f1034ee3`

## Git Data API 发布熔断与恢复

本地 TRIAL 提交完成后的首次发布在首个 blob 请求即返回 HTTP 422。根因是临时发布器调用 `gh api` 时遗漏 `--input -`，JSON 没有作为请求体传入。补齐标准输入参数后的第二次发布在 blob SHA 校验阶段停止：发布器将 `encoding: null` 写成 `options.encoding ?? "utf8"`，nullish 合并使 Git blob 原始字节仍按 UTF-8 字符串读取，再次转为 base64 时已发生内容改变，GitHub 返回的 blob SHA 与本地 Git blob 不一致。

两次失败都发生在 tree、commit 和 ref 创建之前；远端同名分支不存在、PR 为 0、`main` 未移动，只产生无分支引用的孤立 blob。达到连续两次失败上限后按 `Agent.md` 熔断，管理员随后明确解除发布熔断。

恢复时只修正仓库外临时发布器的字节读取：显式区分 `undefined` 与 `null`，保留 `null` 使 `spawnSync` 返回 `Buffer`；每个远端 blob 必须与本地 Git blob SHA 相同，tree、parent、commit 和最终 ref 逐层校验；创建 ref 前再次核验 `xtzhou247` 身份、远端 `main` 未变化且同名分支仍不存在。任一校验失败都不得创建或覆盖 ref。

## 工件与下一步

TRIAL 临时工件按仓库规则保留在本地并被 `.gitignore` 排除；owner 可从同一工作区审计：

- `work/广州医科大学附属脑科医院_trial_payload.json`
- `work/广州医科大学附属脑科医院_trial_doctors.csv`
- `work/广州医科大学附属脑科医院_trial_report.md`

提交专用适配器、测试和本 ADR，通过非强制 Git Data API 发布原分支并创建 `Closes #31` 审计 PR 后停止。只有 owner 在关联 PR 中明确给出 `通过` / `有条件通过` 并切换为 `FULL_APPEND_AND_OBSIDIAN`，才可在同一 Issue 和分支继续全量追加；不得自行合并 PR、关闭 Issue、生成正式画像或领取下一 Issue。

<Handoff_State>
Target: Issue #31 广州医科大学附属脑科医院 TRIAL 审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/31
Branch: codex/mhrj/issue-31-gzbrain-trial
Phase: WAITING_OWNER_TRIAL_AUDIT
Completed:
- 识别客户端请求形态差异，使用合规的 urllib 默认公开 GET 完成官方静态目录普查
- 新增严格 gzbrain 专用适配器、患者案例句过滤和稀疏分页回归保护
- 普查 31 页、183 个唯一详情 ID；试采 10 位覆盖 10 科室，0 详情失败、0 排班/患者信息污染
CurrentFacts:
- 统一总底表未写入，CSV/XLSX/更新报告哈希与基线一致
- TRIAL 临时工件只在本地工作区，未纳入 Git
Next:
- 等待 nancywrayg57-jpg 在关联 PR 对 TRIAL 明确审计
- 只有明确通过并下发 FULL_APPEND_AND_OBSIDIAN 后才继续同一 Issue
Constraints:
- 仅医院官网公开静态页面；禁止 Cookie、代理、浏览器指纹模拟、挑战/验证码绕过、第三方来源
- 排班仅作院区证据，不进入医生字段；病例叙述与患者可识别信息不入库
- 不自行合并 PR、关闭 Issue、进入 FULL 或领取其他 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广州医科大学附属脑科医院_trial_payload.json
- D:\workspace\信息收集整理\work\广州医科大学附属脑科医院_trial_doctors.csv
- D:\workspace\信息收集整理\work\广州医科大学附属脑科医院_trial_report.md
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_31_gzbrain_trial.md
</Handoff_State>
