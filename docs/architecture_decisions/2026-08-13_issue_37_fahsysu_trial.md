# 2026-08-13 Issue #37 中山大学附属第一医院 TRIAL

## 目标与执行边界

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/37
- 工作分支：`codex/mhrj/issue-37-fahsysu-trial`
- Phase：`TRIAL`
- 台账序号：7
- 医院：中山大学附属第一医院
- 官网首页：https://www.fahsysu.org.cn/home
- 医生目录：https://www.fahsysu.org.cn/page/6945
- 人工复核：确认可采集（D-待人工补官网）

本阶段只普查官网公开目录并试采 10 位医生（至少 3 个科室）。不得写统一总底表、生成正式 Obsidian 画像、采集台账序号 8 的黄埔院区专属目录，或自行进入 FULL。

## 专用适配器与范围规则

新增专用适配器 `fahsysu_drupal_expert_directory`：

1. 入口只接受无 query/fragment 的 `https://www.fahsysu.org.cn/page/6945`。
2. 详情只接受同一官方域名、无 query/fragment 的 `/node/<数字ID>`。
3. 医生关系只来自 `.action-item > .action-item-content > .action-item-right > .action-item-list` 中的严格医生标签；页面其他 node 链接不授权。
4. 同一数字 ID 的跨科室关系以顿号归并；同名不同数字 ID 保持独立，样本命中时标记“同名待甄别”。
5. 列表的“正高/副高”只作为目录关系线索；正式职称只取详情 `.other-left-text` 的显式“职称”字段。
6. 详情只读 `article.node--type-doctor` 下的 `.other-2` 与 `.showcase-text-content`；所有 `calendar-*` DOM 排除。排名、患者信息和私用区字符不得进入正式字段。
7. 试采按科室确定性轮转，保证至少覆盖 3 个科室；当前适配器对非 TRIAL 模式硬阻断。
8. 不提交搜索词、不构造筛选组合、不探测页面未声明接口。

## 官网目录普查

- 服务端完整输出单页长列表；分页、上一页/下一页和加载更多控件均未发现，分页计数为 1。
- 顶层 `.action-item` 容器 42 个：32 个包含医生关系，10 个为空结构容器。
- 空容器：手术麻醉中心、输血科、高压氧科、保健门诊中心、精准医学研究院、临床研究中心、药物临床试验机构、动物实验中心、无菌动物研究平台、消毒供应中心。
- 下级专科 90 个；医生—专科关系 881 条；唯一数字 ID 860 个；跨专科重复关系增量 21 条。
- 目录职级关系：正高 447，副高 434。该字段不写入正式职称。
- 同名不同数字 ID 8 组：庄锦涛、涂响安、匡铭、梁力建、王伟、刘敏、陈宇、何潇芳。
- 目录正文中“院本部/本部/东院区/东院/南沙/南院区/黄埔/院区”均为 0。

## 院区与黄埔范围结论

目录页没有结构化院区字段。10 位试采详情中，仅陈振光详情的工作履历出现“东院”3 次，属于官方履历正文中的任职证据，不是统一的医生院区归属字段。本轮只把该信息作为“官网存在东院履历证据”留痕，不将履历词推断写入结构化科室或院区字段。

本轮未访问、未采集台账序号 8 的黄埔院区专属目录。目录和 10 位详情均未出现“黄埔”，但因目录没有统一院区标注，仍无法证明或排除未抽样医生是否含黄埔归属；等待 owner 根据 TRIAL 材料裁决，不自行扩大范围。

## TRIAL 结果

命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "中山大学附属第一医院" `
  --trial-only --max-doctors 10 --min-departments 3 --no-xlsx
```

结果：

- 10 位：郭宇、陈昆、陈蕾、陈炜、邓春华、高勇、涂响安、刘钧澄、唐冰、陈振光。
- 覆盖 9 个科室值；邓春华和高勇分别按同一数字 ID 归并 2 条跨科室关系。
- 10 个来源数字 ID 唯一；详情失败 0；非医生页面混入 0。
- 涂响安命中全目录同名不同 ID 组，保留为独立 ID `735`，标记“同名待甄别”，保持普通优先级、空重点标签。
- 正式职称全部来自详情显式字段，没有把正高/副高拼入职称。
- 详情排班 DOM 排除 400 个；排名/患者片段排除 2 个；四正式文本字段中的排班、患者/排名词、私用区字符和擅长前缀均为 0。
- 使用 `--trial-only --no-xlsx`；未写统一总底表、未生成试采 XLSX、未生成 Obsidian 画像。

## 阻塞、根因、解决方法与防复发

### 1. 本地 Python 命令和依赖不可用

- 现象：PowerShell 的 `python` 指向 WindowsApps 占位程序；Codex 捆绑 Python 虽可执行，但缺少 `requests` 与 `beautifulsoup4`。
- 根因：运行时 PATH 未暴露真实 Python，且捆绑环境仅含部分文档/表格依赖。
- 解决：使用 Codex 工作区依赖中明确解析出的 Python 路径；仅把 `requests`/`beautifulsoup4` 安装到仓库外 `C:\Users\Administrator\AppData\Local\Temp\codex-issue37-python-deps`，通过本轮专用 `PYTHONPATH` 加载。
- 防复发：后续先运行解释器与 `import requests, bs4, openpyxl` 探针；不得反复调用 WindowsApps 的 `python`，不得把临时依赖写入仓库或修改全局 Python。

### 2. 首次真实 TRIAL 解析关系为 0

- 现象：写出前报错“官网目录未发现严格 action-item 医生关系”，没有生成工件。
- 根因：实际医生标签层级为 `.action-item-list > .action-item-list-text > .action-item-list-tag > a`，初版选择器漏掉 `.action-item-list-text`。
- 解决：局部读取一层 DOM 后，只补齐该固定结构层级，并同步更新模拟 DOM 测试。
- 防复发：测试必须完整模拟真实层级；现场变更时先输出目标节点的一层子元素和父链，不凭类名猜测后代结构。

### 3. 第二次真实 TRIAL 的顶层分组门禁冲突

- 现象：严格解析已得到 881 条关系，但门禁报“顶层分组应为 42，实际 32”。达到连续 2 次验证失败后按 `Agent.md` 熔断。
- 根因：页面有 42 个顶层容器，其中 10 个没有 `.action-item-content`；初版统计只从医生关系反推分组，因此得到 32，把“页面结构容器”与“有效关系分组”混成一个指标。
- 解决：管理员解除熔断后，将指标分层为 `census_group_count=42`、`census_relationship_group_count=32`、`census_empty_group_count=10`，并保存空容器名称。空容器计入结构普查，但绝不构造医生/专科关系。
- 防复发：门禁同时固定 42/32/10 三个计数；报告明确显示三层含义；测试断言顶层容器、关系分组和空容器分别计算。

### 4. 院区证据表述过强

- 现象：初步观察曾表述“目录与详情均未发现院区字段”，后续只读扫描发现陈振光详情履历含“东院”3 次。
- 根因：把“没有结构化院区字段”误写成“原始详情文本没有院区词”，证据层级混淆。
- 解决：分别统计目录页与样本详情原始 HTML 院区词；对命中详情保留 ID、姓名、来源和计数，同时标明只作履历证据、不推断结构化归属。
- 防复发：院区审计固定拆成三项：目录词扫描、详情词扫描、结构化字段存在性；任何履历命中不得自动写入科室/院区字段。

### 5. Git Data API 提交消息被 PowerShell 序列化为数组

- 现象：6 个 blob 和远端 tree 均已按本地 SHA 校验成功，但创建 commit 返回 HTTP 422，提示 `properties/message ... is not a string`；远端分支引用尚未创建。
- 根因：PowerShell 捕获 `git show --format=%B` 的多行输出时得到字符串数组，直接放入 JSON 后把 `message` 序列化为数组，而 GitHub Git Data API 要求单一字符串。
- 解决：先确认远端同名 ref 仍不存在；用 `Out-String` 将命令输出显式归一为标量字符串并 `TrimEnd()`，再创建 commit；只有 commit tree/parent 与本地一致后才以 `force=false` 创建 ref。
- 防复发：所有进入 Git Data API JSON 的 CLI 多行输出必须先做标量化；API 失败后先查 ref，禁止盲目重复更新引用。孤立 blob/tree 不构成分支发布，也不得误报为推送成功。

## 验证与零写入证据

- FAHSYSU 专项测试：5 项通过。
- `py_compile`：采集器和测试文件通过。
- CSV：表头加 10 行、23 列，可用 UTF-8-SIG 独立解析。
- 统一总底表三资产及入口台账在 TRIAL 前后 SHA-256 完全一致：
  - 入口台账 XLSX：`10434A9C5F430A5F1A31D59A7EAEB56E9BEB68A50B232FAAEF7DA72821ED1B4D`
  - 总底表 XLSX：`965714088B20B4DD79C0A207276ED3858448FD35177E0FB8FDFB202F2518B4EE`
  - 总底表 CSV：`EA810318D4CE3624B448B2444B296FDCF9F475866AD40A23A713FD1A0883CAEE`
  - 更新报告：`CAA07A9F2851E69EFFC4F84F1A015EBBE1F072DE21B193ABE528AE513BDADCE3`

## 工件与停止点

- `work/中山大学附属第一医院_trial_payload.json`
- `work/中山大学附属第一医院_trial_doctors.csv`
- `work/中山大学附属第一医院_trial_report.md`

三份 TRIAL 工件受 `.gitignore` 影响，发布时只精确强制暂存这些路径，不修改忽略规则。工件、代码、测试和 ADR 同批进入关联 PR；CI 成功后请求 `nancywrayg57-jpg` 明确审计。owner 未明确给出 `通过` / `有条件通过` 并切换为 `FULL_APPEND_AND_OBSIDIAN` 前，不得进入 FULL。

<Handoff_State>
Target: Issue #37 中山大学附属第一医院 TRIAL 审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/37
Branch: codex/mhrj/issue-37-fahsysu-trial
Phase: WAITING_OWNER_TRIAL_AUDIT
Completed:
- 新增 FAHSYSU 严格专用适配器，完成 42/32/10 分层目录结构、90 专科、881 关系、860 唯一 ID 普查
- 试采 10 位覆盖 9 个科室值，详情失败 0，同名/跨科室/院区证据均留痕
- 记录本轮全部运行环境、DOM、计数和证据层级阻塞及防复发门禁
CurrentFacts:
- 目录正高/副高只作线索；正式职称全部来自详情显式字段
- 目录无院区词；陈振光履历含东院证据，但无统一结构化院区归属，黄埔仍不可判定
- 总底表 CSV/XLSX/更新报告未改变
Next:
- 提交并通过非强制 Git Data API 发布原分支，创建 base=main 且 Closes #37 的 TRIAL PR
- CI 成功后请求 nancywrayg57-jpg 明确审计；未切换 FULL_APPEND_AND_OBSIDIAN 前停止
Constraints:
- 仅医院官网公开页面；禁止第三方平台、患者评价、隐私、登录/验证码绕过
- 不提交搜索、不探测未声明接口、不采台账序号 8 黄埔专属目录
- 不写统一总底表、不生成 Obsidian 画像、不自行进入 FULL
Artifacts:
- D:\workspace\信息收集整理\work\中山大学附属第一医院_trial_payload.json
- D:\workspace\信息收集整理\work\中山大学附属第一医院_trial_doctors.csv
- D:\workspace\信息收集整理\work\中山大学附属第一医院_trial_report.md
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_37_fahsysu_trial.md
</Handoff_State>
