# Issue #43 广东省妇幼保健院照片 TRIAL

> 日期：2026-08-14
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/43>
> 分支：`codex/mhrj/issue-43-gdmch-photo-trial`
> Phase：`TRIAL`
> 医院：广东省妇幼保健院
> 官网：<https://www.e3861.com/>
> 医生目录：<https://www.e3861.com/keshizhuanjia/zhuanjiajieshao>

## 1. 目标与执行边界

本轮只完成 Issue #43 明确授权的官网目录普查、10 位医生试采、本人职业照下载和审计材料，不写统一总底表、不生成正式 Obsidian 医生画像、不执行 FULL。

固定边界：

1. 只使用 `e3861.com` 官网公开页面和 `wx.e3861.com` 官方图片子域。
2. 不构造医生或科室检索词，只遍历官网声明的服务端分页。
3. 照片只接受 `/sfyAdmin/Images/Doctor/` 路径，并由响应魔数决定实际扩展名。
4. 官网默认 `/sfyAdmin/Images/Default/doct.png` 只计为占位图，不作为医生本人职业照。
5. 患者、儿童、案例影像、评价、排名、排班日期/时段、隐私和第三方平台均不得进入正式字段或照片工件。
6. 所有广东省妇幼保健院非 `--trial-only` 命令在联网和总底表写入前触发 `GDMCH FULL 发布熔断`；`--allow-generic-append` 不能绕过。

## 2. 官网目录普查结论

### 2.1 分页、ID 与范围

| 指标 | 现场结果 |
|---|---:|
| 服务端公开 GET 分页 | 111 |
| 原始卡片关系 | 884 |
| 唯一数字详情 ID | 884 |
| 重复关系 | 0 |
| 号源/系统账号/非医生身份排除 | 49 |
| 排除后合规医生候选 | 835 |
| 合规候选中有本人职业照 | 658 |
| 合规候选中仅有默认占位图 | 177 |
| 全目录默认占位图 | 225 |

详情严格契约：

- 目录：`/keshizhuanjia/zhuanjiajieshao`
- 分页：空白 `searchDoctor`、空白 `searchDepartment` 与服务端 `page=<N>`
- 详情：`/keshizhuanjia/zhuanjiajieshao/<数字ID>.html`
- 详情容器：`.expert-detail`
- 照片：`https://wx.e3861.com/sfyAdmin/Images/Doctor/`

目录只有自由文本检索框，没有服务端科室分类树。科室与院区仅从详情页 `出诊安排` 括号标签保守提取；日期和时段不进入正式字段。

49 个排除候选均在试采报告中按数字 ID、名称、列表身份、来源链接和理由逐项列出。典型示例包括 `续费专用号`、`test123`、`系统管理员-正式库`、`急诊号`、`政府免费筛查就诊号`、`名医工作室`、`专科医生`。现场证据修正了预普查阶段的“42 个排除、842 个合规候选”估算；不得为了匹配旧估算而把 7 个明确的非医生身份纳入医生范围。

### 2.2 四院区归属

官网同一专家目录和统一页脚列示以下四院区：

| 院区 | 官方链接 |
|---|---|
| 番禺院区 | <https://www.e3861.com/keshizhuanjia/panyuyuanqu> |
| 越秀院区 | <https://www.e3861.com/keshizhuanjia/yuexiuyuanqu> |
| 天河院区 | <https://www.e3861.com/keshizhuanjia/tianheyuanqu> |
| 清远院区 | <https://www.e3861.com/keshizhuanjia/qingyuanyuanqu> |

医院介绍页、目录页和首页未发现“独立法人”“法人单位”“统一社会信用代码”等独立实体信号，`independent_entity_count=0`，因此未触发清远院区独立法人熔断。

## 3. 实现决策

新增专用适配器 `gdmch_paginated_expert_photo`：

1. 精确识别 `https://www.e3861.com/keshizhuanjia/zhuanjiajieshao`，禁止通用模板直接接纳号源账号。
2. 写出前固定校验 111 页、884 个数字 ID、49 个排除候选、835 个合规候选、658 个本人职业照候选。
3. TRIAL 只从 658 个本人职业照候选中按目录页跨度抽取 10 位，避免默认占位图进入照片样本。
4. 10 位样本必须覆盖至少 3 个真实科室；本院统计先移除院区后缀，再拆分顿号科室，禁止把“番禺院区、越秀院区”误计为科室。
5. 排班标题和后续相邻 DOM 尾段一起截断；标题与时段分成多个节点时，命中标题后立即终止正文段遍历。
6. 照片保留官网原始字节，不压缩；记录文件名、字节数、SHA-256、魔数、宽度、高度和官网 URL。
7. 照片文件名为 `姓名-首个原子科室-主职称-医院.<魔数扩展名>`；同名覆盖冲突追加详情 ID，已有不同内容时拒绝覆盖。
8. 任一图片大于 200KB 或宽度大于 800px 时置为 `WAITING_OWNER_LARGE_IMAGE_POLICY`；本轮 10 图均未命中，状态为 `OWNER_APPROVED_ORIGINAL_NO_WIDTH_LIMIT`。
9. 新增 `work/tests/test_gdmch_photo_trial.py`，覆盖严格 URL、分页、号源排除、跨 DOM 排班尾段清洗、照片尺寸、科室/院区拆分、精确 TRIAL 门禁和 FULL 熔断。

## 4. TRIAL 结果

### 4.1 样本与字段

- 最终样本：10 位真实医生、10 个唯一数字详情 ID。
- 详情失败：0。
- 科室覆盖：14 个原子科室，超过 Issue 要求的至少 3 个。
- 院区样本覆盖：番禺、越秀、天河、清远。
- 排班片段排除：12；正式字段排班写入：0。
- 患者案例排除：0；正式字段患者/病例/评价/排名扫描命中：0。
- 私用区字符：0。
- 异常提示：2 行 `详情正文为空或未识别`，均保持普通优先级且无重点标签提权。

10 位样本为：李文萍、范保维、和秀魁、陈炳豪、胡春玲、陈凤媚、伍苑宾、柴成伟、王春艳、杨洋。逐 ID、科室、院区和来源链接见 `work/广东省妇幼保健院_trial_report.md`。

### 4.2 照片审计

| 指标 | 结果 |
|---|---:|
| 应采 | 10 |
| 实采 | 10 |
| 失败 | 0 |
| 无照片 | 0 |
| 总字节数 | 535,093 |
| 平均字节数 | 53,509 |
| 最大单张 | 126,269 |
| 大于 200KB | 0 |
| 宽度大于 800px | 0 |

10 张图片已逐张视觉确认，全部为单人白大褂职业照；没有患者、儿童、合影、新闻配图或案例影像。所有文件的字节数、SHA-256、扩展名魔数和宽高均与 payload 对账一致。

## 5. 总底表零变更证据

最终 TRIAL 前后以下三份受保护资产的长度、UTC 修改时间和 SHA-256 完全一致：

| 文件 | 长度 | LastWriteTimeUtc | SHA-256 |
|---|---:|---|---|
| `珠三角三甲医院_医生画像自动采集总底表.xlsx` | 3,603,182 | `2026-08-14T06:46:58.8236271Z` | `F7F574988CEED831ACBE08E86A7B4DF9FCC998020F984880C9F8E4A98973309F` |
| `珠三角三甲医院_医生画像自动采集总底表.csv` | 14,642,292 | `2026-08-14T06:46:58.7816221Z` | `065EFC0C8673545AF90A231E16569AE417173A278DD4927690EE36AF23D6BFEA` |
| `珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 4,784 | `2026-08-14T06:46:59.0444180Z` | `18179EDAB02F311947455A2A17B1850DB1E13F7897813B95FF53CDDF88A7974A` |

## 6. 验证闭环

- `py_compile`：采集器与新增测试通过。
- `python -m unittest discover -s work/tests -p 'test_*.py'`：133 项通过。
- `git diff --check`：通过。
- FULL 负向验证：非 TRIAL 命令退出 1，报告 `GDMCH FULL 发布熔断`，总底表三文件哈希不变。
- 真实 TRIAL：111 页顺序公开 GET、10 行、10 图、详情失败 0、总底表零变更。
- 10 张图片逐张视觉复核：全部为医生本人单人职业照。

最终试采工件：

| 文件 | 长度 | SHA-256 |
|---|---:|---|
| `work/广东省妇幼保健院_trial_payload.json` | 89,602 | `E957B9DDE746CBA8AC6818914AB603857BE928873EB9BFBA4AE05399BD033A60` |
| `work/广东省妇幼保健院_trial_doctors.csv` | 16,786 | `26FDECD35B42EBEB6236B694D7592BBC31FAB0DA7857494081C6218828446EA7` |
| `work/广东省妇幼保健院_trial_report.md` | 35,612 | `860D6EFF9DCF66D05DBD8290C4F4698426B64406F047C75EA32B07BF71A70287` |

## 7. 阻塞、根因、解决与防复发

### 7.1 PowerShell 诊断变量解析

- 阻塞：`"$p:"` 被 PowerShell 当作作用域变量；`$Host` 是只读系统变量；`"$base?..."` 把问号并入变量名。
- 根因：诊断脚本使用了 PowerShell 特殊变量名和有歧义的插值边界。
- 解决：改用格式化字符串、任务专用 `$imgHost`，URL 参数由 Python `urlencode` 或 PowerShell `-f` 明确拼接。
- 防复发：诊断变量使用任务前缀；URL 查询参数禁止依赖有歧义的双引号插值。

### 7.2 Bundled Python 缺少 requests/bs4

- 阻塞：系统 `python.exe` 是 Windows Store 占位符；Codex bundled Python 可执行但默认缺少 `requests` 和 `bs4`。
- 根因：解释器与任务依赖分布在不同的已验证运行目录。
- 解决：固定使用 workspace dependency loader 返回的 bundled Python，仅给当前进程设置已验证的 Issue #37 临时依赖目录为 `PYTHONPATH`；未安装全局包、未修改系统 PATH。
- 防复发：执行前先做 `requests`、`bs4`、`openpyxl` 导入探针；临时依赖不存在时停止并建立新的任务级环境。

### 7.3 预普查计数与现场严格分类不一致

- 阻塞：首次真实门禁显示排除 49 而非预估 42，合规候选 835 而非 842；目录 884 张卡片都有官方子域图片 URL，但其中 225 张是默认占位图，只有 658 个合规候选具备本人职业照。
- 根因：预普查只统计了显式号源标记，没有把 `名医工作室`、`儿科义诊医生`、`产前诊断专科医生`、`尹爱华名医工作室`、`盆底磁治疗预约`、`续费医生`、`专科医生` 七个非姓名身份纳入排除；同时把官方占位图误计为本人职业照。
- 解决：以 884 个数字 ID 的现场逐项证据为准，排除 49 个明确非医生候选；本人职业照只接受 `/Images/Doctor/`，默认图只留计数证据。
- 防复发：区分“官方图片 URL 可得”和“本人职业照可得”；非医生排除同时执行姓名结构、账号标记和护理身份校验，并在报告中输出完整逐 ID 表。

### 7.4 排班标题与尾段跨 DOM 节点

- 阻塞：两次真实验证中，胡春玲、陈凤媚的正文仍含院区、周次和上午时段；连续两次失败后按 Agent.md 熔断。管理员随后明确发送“解除熔断”，才恢复执行。
- 根因：官网将 `出诊时间` 标题与后续院区/时段拆成多个相邻 DOM 段；初版只清除标题所在段，仍继续接纳后续段。
- 解决：命中排班标题后保留标题前正文并立即终止详情正文段遍历；对两个真实详情页做定点探针，修复后排班命中均为 0。
- 防复发：新增“排班标题节点与时段节点分离”单元测试；正式字段继续执行周次、星期、上午、下午和排班标题扫描。

### 7.5 科室统计误拆院区顿号

- 阻塞：通用覆盖统计把 `乳腺科（番禺院区、越秀院区）` 拆成院区碎片，显示 18 个伪科室。
- 根因：通用函数直接按顿号拆分，没有先去掉本院专用院区后缀。
- 解决：增加 GDMCH 专用统计，先移除受控四院区后缀，再拆分原子科室；最终为 14 个真实科室。
- 防复发：新增科室/多院区组合回归测试，报告只使用专用统计结果。

## 8. 当前停止点

TRIAL 代码、测试、payload、CSV、报告、10 张照片和本 ADR准备提交到原 Issue #43 分支。提交前再次复核 GitHub 身份为 `xtzhou247`、远端分支 ref 与本地提交 parent；仅允许 SSH 非强制 fast-forward push。创建 `base=main`、关联 `Closes #43` 的 PR 后等待 governance CI，并请求 owner 进行 TRIAL 审计。不得自行执行 FULL、合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #43 广东省妇幼保健院 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/43
Branch: codex/mhrj/issue-43-gdmch-photo-trial
Phase: TRIAL_READY_TO_PUSH
Completed:
- 111 页、884 唯一数字 ID 普查；49 非医生排除、835 合规候选
- 合规候选本人职业照 658、默认占位图 177；四院区归属证据完整、独立实体信号 0
- 10 位真实医生、14 个科室、10 张本人职业照；详情/照片失败均为 0
- 排班/患者/导航/私用区字段门禁通过；133 项单元测试通过
- 总底表 XLSX/CSV/更新报告前后长度、时间和 SHA-256 一致
Next:
- 精确暂存、提交；复核身份和远端 ref 后 SSH 非强制 fast-forward push
- 创建关联 Issue #43、base=main 的 PR，等待 CI 后请求 owner TRIAL 审计
- 仅 owner 明确通过并切换 FULL_APPEND_AND_OBSIDIAN 后解除 FULL 发布熔断
Constraints:
- 仅官网公开页面和医生本人职业照；禁患者/儿童影像、案例、评价、隐私、第三方和登录/验证码规避
- 当前只允许 TRIAL，不写总底表、不生成正式画像、不执行 FULL
- 不自行合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广东省妇幼保健院_trial_payload.json
- D:\workspace\信息收集整理\work\广东省妇幼保健院_trial_doctors.csv
- D:\workspace\信息收集整理\work\广东省妇幼保健院_trial_report.md
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\广东省妇幼保健院\照片
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-14_issue_43_gdmch_photo_trial.md
</Handoff_State>
