# 2026-08-13 Issue #35 中山大学孙逸仙纪念医院 TRIAL

## 目标与门禁

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/35
- 工作分支：`codex/mhrj/issue-35-gzsys-trial`
- Phase：`TRIAL`
- 台账序号：5
- 医院：中山大学孙逸仙纪念医院
- 官网首页：https://www.gzsys.org.cn/home
- 医生目录：https://www.gzsys.org.cn/doctor/592/search
- 人工复核：确认可采集（D-待人工补官网）

本阶段只允许现场核验公开入口、普查默认医生目录及页面公开分类树并试采 10 位（至少 3 科室）；不得写统一总底表、生成正式 Obsidian 画像或自行进入 FULL。

## 可达性与页面性质

入口是医院官方域名下公开 Drupal“名医名师”目录。常规 `requests.Session` 首次请求按站点逻辑发生 302 并设置普通 Cookie `CT6T`、`CT6TS`，同一会话随后稳定返回 HTTP 200；官网首页也返回 200。全程未遇验证码、挑战应答、指纹要求或登录门禁，未使用代理、浏览器指纹模拟、挑战求解或任何绕过行为。

目录入口包含关键词输入和四个筛选字典。适配器只解析筛选项留痕，不提交搜索词、不遍历筛选组合，也不探测页面未声明的接口。本轮字典为：科室树 96 项、人才项目 4 项、导师资格 5 项、职称 33 项。

## 通用模板误采根因与专用适配器

通用模板会同时发现医生 `/node/<ID>`、科室 `/node/<ID>` 以及部分 `/doctor/<ID>` 别名，首屏即产生医生页和科室页混采。根因是该站复用 Drupal node 路径，路径和链接文本不足以证明医生身份。

新增专用适配器 `gzsys_drupal_doctor_cards`，范围规则如下：

1. 任务入口必须精确匹配 `https://www.gzsys.org.cn/doctor/592/search`，拒绝 query、fragment 和其他路径作为目标入口。
2. 唯一授权关系源是列表 DOM `.card-4-0`；姓名与详情主链接只读 `.card-title a`，职称只读 `.card-subtitle-content`，科室只读 `.card-tag`。
3. 详情路径只接受同域 `/node/<数字ID>` 或 `/doctor/<数字ID>`；二者按数字 ID 归一，不能按 URL 字符串分裂身份。全目录原始主链接为 node 432、doctor 232，但共有 664 个唯一数字 ID。
4. 分页只接受页面声明的默认 `All` 查询，从 `page=0` 连续构造到声明末页；不遍历搜索词或筛选组合。
5. 详情只读 `.other-2`：姓名 `.other-left-title`，职称/科室 `.other-left-text`，简介 `.desc.line-6`。`.calendar-3-1` 排班整体排除。
6. 科室多值以顿号合并；私用区字符在原子字段边界删除；排名、好医生/名医录、患者评价/案例片段逐句排除，不进入四个正式文本字段。
7. 列表或详情仅标注护理身份的候选排除并留痕；若详情排除导致样本不足，继续使用确定性轮转序列补足 10 位。

## 最终全目录普查

- 默认目录分页：23 页（`page=0..22`）。
- 严格 `.card-4-0` 卡片关系：664 条；唯一数字 ID：664；跨页重复 ID：0。
- 有姓名 ID：664；空姓名 0；非空姓名值 664；同名不同 ID 0 组。
- 非空科室 664；空科室 0；去重后的科室值 65 个。
- 纯护理排除 6 个：王庄斐、徐静、陈丽莉、黄佩贤、温作珍、黄淑婷。
- 排除后合规候选 658 个；列表分页错误 0；试采详情错误 0。

## 最终真实 TRIAL

命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "中山大学孙逸仙纪念医院" `
  --trial-only --max-doctors 10 --min-departments 3 --no-xlsx
```

结果：

- 样本 10 位：宋尔卫、陈样新、姚和瑞、唐亚梅、陈穗俊、黄海、严励、沈君、詹俊、刘宜敏。
- 覆盖 11 个科室值：乳腺内科、乳腺外科、内分泌内科、心血管内科、放射科影像专科、泌尿外科、消化内科、神经科、耳鼻喉科、肿瘤内科、肿瘤科放疗专科。
- 10 个姓名唯一、10 个来源链接唯一；来源均严格匹配本院官方 `/node/<ID>` 或 `/doctor/<ID>`。
- 详情失败 0、异常提示 0、非医生页面混入 0。
- 详情中识别并排除 7 个排班 DOM；排除 4 个排名/好医生/名医录片段；四个正式文本字段中的排班、患者信息、排名词和私用区字符均为 0。
- 使用 `--trial-only --no-xlsx`，未写统一总底表、未生成试采 XLSX、未生成正式 Obsidian 画像。

## 两次诊断与防复发

### 科室多值分隔符

首次真实试采发现姚和瑞的详情科室为 `乳腺内科, 肿瘤内科`。根因是官网原文使用英文逗号，而既有跨科室口径要求顿号合并。最小修正是在结构化科室字段边界按中英文逗号、分号、斜线和顿号切分、去重，并统一以顿号拼接；回归测试覆盖该 DOM。

### 排名/荣誉文本进入简介

首次样本复核发现个别详情简介含“羊城好医生”和“岭南名医录”。虽然是官网公开履历，但 Issue 明确要求排名或“好医生榜”等不得进入正式画像文本。最小修正是将详情简介拆为句子，排除好医生、名医录、排行榜、排名及患者案例/评价句，再生成简介和亮眼经历；其余官方临床与履历证据保留。防复发通过专项 DOM 测试与最终四字段关键字扫描实现。

两次修正均属于同一轮首次运行后的样本复核，没有触发连续 2 次失败熔断；最终全量测试与真实 TRIAL 均通过。

## 验证与零写入证据

- `py_compile`：采集器通过。
- 中山大学孙逸仙纪念医院专项测试：8 项通过，覆盖精确入口、数字 ID 别名、默认分页、严格卡片 DOM、详情噪声/排班/私用区清洗、科室顿号归一、确定性轮转和写出前范围漂移拦截。
- 全仓库测试：100 项通过。
- CSV：表头 + 10 位医生，23 列，可独立解析。
- `git diff --check`：通过。
- 统一总底表三资产 SHA-256 在 TRIAL 前后完全一致：
  - CSV：`95E59269410D95ACBF04D156BFBFE08A8322D2C7A0A34FFDF3D5BC4AF90515AA`
  - XLSX：`865DFA33B30D51CD79F3B5989252C835D820B93D0D536C695285CAFA5A9A074F`
  - 更新报告：`48E5F074FD3FBE6B81DFCF7D83C92C641E1DB305B6FD9140E455EC1E5AE14ED0`

## 工件与停止点

本轮提交代码、测试、ADR 与三份原始 TRIAL 工件：

- `work/中山大学孙逸仙纪念医院_trial_payload.json`
- `work/中山大学孙逸仙纪念医院_trial_doctors.csv`
- `work/中山大学孙逸仙纪念医院_trial_report.md`

三份工件受 `.gitignore` 影响，发布时只精确强制暂存这些路径，不修改忽略规则。材料进入关联 PR 且 CI 成功后，请求 `nancywrayg57-jpg` 明确给出 `通过` / `有条件通过` / `不通过`。只有 owner 明确通过并把唯一有效指令切换为 `FULL_APPEND_AND_OBSIDIAN` 后，才可在同一 Issue 和分支继续正式追加；不得自行进入 FULL、合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #35 中山大学孙逸仙纪念医院 TRIAL 审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/35
Branch: codex/mhrj/issue-35-gzsys-trial
Phase: WAITING_OWNER_TRIAL_AUDIT
Completed:
- 新增 gzsys 严格专用适配器，完成默认 All 分页、卡片关系、筛选字典和详情 DOM 普查
- 普查 23 页、664 卡片/唯一 ID，排除 6 个纯护理身份，试采 10 位覆盖 11 个科室值
- 详情失败/异常/非医生混入为 0；排班、患者信息、排名词、私用区字符均未进入四正式文本字段
CurrentFacts:
- 默认目录合规候选 658；页面筛选字典仅留痕、不遍历
- 常规站点 Cookie 会话可达，无挑战绕过；总底表 CSV/XLSX/更新报告未改变
Next:
- 提交并通过非强制 Git Data API 发布原分支，创建 base=main 且 Closes #35 的 TRIAL PR
- CI 成功后请求 nancywrayg57-jpg 明确审计；未切换 FULL_APPEND_AND_OBSIDIAN 前停止
Constraints:
- 仅医院官网公开页面；禁止第三方平台、患者评价、隐私、登录/验证码绕过
- 不遍历搜索词/筛选组合，不探测页面未声明接口，官网缺失字段留空
- 不写统一总底表，不生成正式 Obsidian 画像，不自行进入 FULL
- 不普通 push、不强推、不合并 PR、不关闭 Issue
Artifacts:
- D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_trial_payload.json
- D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_trial_doctors.csv
- D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_trial_report.md
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_35_gzsys_trial.md
</Handoff_State>

---

# 2026-08-13 Issue #35 FULL_APPEND_AND_OBSIDIAN 完成记录

## owner 门禁与执行授权

- PR #36 owner 评论：https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/36#issuecomment-5278732575
- 审计结论：`通过`。
- 生效阶段：`FULL_APPEND_AND_OBSIDIAN`。
- owner 条件：以 `664 唯一 ID − 6 护理 = 658 合规候选` 为对账基线；逐 ID 对账和身份聚类进入最终画像审计材料；无显式擅长保持空白；多院区只保留官网明确证据；沿用异常不提权、排班/患者/排名/私用区零命中门禁。

## FULL 写入前门禁

新增 `validate_gzsys_full_append`，在任何总底表写入前验证：

1. 23 页、664 卡片/唯一数字 ID、65 个科室值和筛选字典计数未漂移。
2. 正式数字 ID 与护理排除数字 ID 互斥，合计完整覆盖 664 个 ID。
3. 逐 ID 对账表无空 ID、无重复 ID，并且处置与正式行/护理排除清单一致。
4. 身份归并对账对每个合规 ID 恰好映射一次；本轮全目录没有同名组，因此 658 个合规 ID 对应 658 个唯一身份，不作启发式归并。
5. 正式来源只接受 `gzsys.org.cn` 的 `/node/<数字ID>` 或 `/doctor/<数字ID>`；医院、采集入口和来源类型必须一致。
6. 异常行保持普通优先级，重点范围和疾病标签为空。
7. 擅长前缀、排班、患者信息、排名文本和私用区字符不得进入正式字段。

FULL 报告新增完整的“逐 ID / 身份归并对账表”，664 个 ID 均列出姓名、裁决、来源链接和理由。

## 熔断、根因与解除后的最小修复

### 原熔断过程

1. 第一次 FULL 验证在写表前失败：新增 `identity_reconciliation` 误插入上一医院适配器的返回路径，GZSYS 返回时变量未定义。
2. 移回 GZSYS 作用域后，第二次 FULL 验证仍被硬门禁阻断：官网 ID `25208` 详情失败 1 条，且 14 位医生详情自由简介含显式开诊/出诊/门诊时间。
3. 两次失败后按 `Agent.md` 停止修改并触发 `[FATAL - HUMAN_INTERVENTION_REQUIRED]`；CSV/XLSX/更新报告哈希仍保持 TRIAL 基线，没有发生半写入。
4. 管理员随后明确“解除本轮熔断并授权最小诊断修复”，由此开启新的诊断窗口。

### 根因证据

- 默认 All 目录第 18 页仍公开列出 ID `25208`：郑眉光、副主任医师、神经外科、来源 `https://www.gzsys.org.cn/node/25208`。
- 该详情在常规官网会话的三次请求中返回 HTTP 404；后续复核也可能因站点状态返回 403，但目录卡片关系稳定存在。不能删除这个授权目录 ID，也不能把官网缺失内容补造。
- GZSYS `.desc.line-6` 是自由简介，部分医生把“院本部开诊时间”“南院区开诊时间”“出诊时间”“门诊时间”等排班文字直接放在简介段尾。原解析器只排除了独立 `.calendar-3-1` DOM，未清除这些内联排班尾段。

### 最小修复与防复发

- 新增 GZSYS 专用 `strip_gzsys_schedule_text`，只删除明确的开诊/出诊/门诊/特诊时间段和紧邻的院区周次尾段；如果排班后还有显式“特长/擅长/专长/简介”标签，则保留后续临床内容。
- FULL 门禁只容许已知 ID `25208` 的显式详情失败；它仍以目录姓名、职称、科室和来源生成正式异常行，`详情页状态=失败`，异常提示包含“详情页读取失败”，并保持普通优先级、空重点标签。任何其他详情失败仍阻断写表；若 `25208` 后续恢复 HTTP 200，同样可正常通过。
- 专项测试覆盖内联排班删除、排班后特长保留、无标签院区排班尾段、完整 664 ID 对账、`25208` 唯一允许失败和异常不提权。

## 正式追加与逐 ID 对账

正式命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "中山大学孙逸仙纪念医院" `
  --allow-generic-append
```

结果：

- `mode=master_append`。
- 本院正式行：658。
- 新增写入：658；重复跳过：0；既有刷新：0。
- 总底表：4574 → 5232 行，医院数 15。
- 目录/对账：664 唯一 ID；正式 ID 658；护理排除 ID 6；正式与排除无重叠；并集 664。
- 护理排除 ID：`14598`、`16987`、`18532`、`14576`、`16988`、`15353`。
- 详情失败：仅 ID `25208` 郑眉光；正式异常行完整保留目录证据。
- 异常提示不为空：81 行；全部普通优先级且重点范围/疾病标签为空。
- 显式擅长非空：64 行；其余 594 行按官网无独立标签保持空白，不从简介推断回填。
- 排班 DOM/内联排班排除计数：479；排名/患者片段排除：51；最终正式字段中的排班、患者信息、排名词、私用区字符、擅长前缀均为 0。

FULL 正式追加后、画像生成前 SHA-256：

- CSV：`CB4A5C2D29F6CB38AB36C091C15996F12CE0BBEF24156BF32733AE70C3175616`
- XLSX：`3B143AF17928AA51ADC543D6D509C8D867CB42C610B97FE63B278ABAD2A3CCDC`
- 更新报告：`1C540562E58C224EB4DB458EE96EC453FE0DA584DB80BC010C0C9101090CB2F2`
- FULL payload：`06218952E96AFAD04BF658B3C30C89F474C16452ED3FACA7CACFFBF9C48D17F4`
- FULL 归并审计报告：`56D3736C236AE1345050E0B51396FA8952A9B0A2F2AD413514D7538A86203CD3`

## XLSX 验收

按表格技能使用 `@oai/artifact-tool` 导入正式 XLSX 并检查全部 6 个工作表：

| 工作表 | 现场范围 | 验收结果 |
|---|---:|---|
| 自动采集底表 | `A1:W5233` | 5232 数据行；本院行连续，首尾切片可读 |
| 复核清单 | `A1:W494` | 493 条复核清单，结构正常 |
| 科室统计 | `A1:B553` | 552 个科室值，计数可读 |
| 重点范围统计 | `A1:B7` | 6 类汇总，计数可读 |
| 医院统计 | `A1:F16` | 本院 658、待复核 658、已建画像 658 |
| 采集说明 | `A1:B23` | 本批医院 658、新增 658、详情失败 1、总行 5232 |

工作簿共 6 个表和 6 个表格对象；无公式，公式错误值扫描 0；全部工作表及主表本院首尾切片均完成视觉检查，未发现空白工作表、关键文本裁切或破损布局。

画像生成后离线执行 `python .\work\collect_official_doctors_batch.py --rebuild-master-only`，只根据现有画像文件同步总表 `已建画像` 与统计/报告，不联网、不重新采集。完成后没有采集器或 Node 残留进程；总表仍为 15 家医院、5232 行，本院 658 行全部为 `已建画像=是`，医院统计同步为 658。采集说明仍保留本批医院 658、新增 658、详情失败 1，没有发生业务字段或批次元数据漂移。

画像后最终 SHA-256：

- CSV：`5F7AFF7ECBECE155D1D3F4947285A38B4FE9735386C0D9861C42F5315D62CAEF`
- XLSX：`965714088B20B4DD79C0A207276ED3858448FD35177E0FB8FDFB202F2518B4EE`
- 更新报告：`655A822D1C4D2E07C662239179F6F0E3CF1A6E948104F0CD7A7D78E96207B5E3`
- FULL payload（未变）：`06218952E96AFAD04BF658B3C30C89F474C16452ED3FACA7CACFFBF9C48D17F4`
- FULL 归并审计报告（未变）：`56D3736C236AE1345050E0B51396FA8952A9B0A2F2AD413514D7538A86203CD3`

最终 CSV 与 XLSX 均为表头加 5232 行、23 列。本院 658 行逐格一致；全量比较只发现既有旧医院 4 个单元格和 CSV 表头 1 个单元格保留历史 BOM 字符，未在本 Issue 越界清洗。

## Obsidian 画像与索引

命令：

```powershell
python .\work\generate_obsidian_profiles.py `
  --hospital "中山大学孙逸仙纪念医院" `
  --generate-missing-only
```

结果：

- 新生成 658 份；刷新 0；跳过 0；重建 1 个本院索引。
- `658 总表行 = 658 画像文件 = 658 索引链接 = 658 索引官网来源`。
- 总表姓名、画像文件名和索引链接均为 658 个唯一值；缺失、多余、重复、来源不一致全部为 0。
- 81 条异常提示均出现在相应画像；郑眉光画像明确保留详情失败，林㼆画像明确保留姓名异常提示，不提权且不自行改名。
- 本院全部画像与索引的排名/患者/排班/私用区关键词扫描为 0。

## TRIAL 清理与保留工件

在 FULL、XLSX 和画像全部验收后，精确删除三份本院 TRIAL 工件：

- `work/中山大学孙逸仙纪念医院_trial_payload.json`
- `work/中山大学孙逸仙纪念医院_trial_doctors.csv`
- `work/中山大学孙逸仙纪念医院_trial_report.md`

受保护的总底表 CSV/XLSX、总底表更新报告、FULL payload/report、正式画像和 `_索引.md` 均已现场复核仍存在。

## 验证与当前停止点

- GZSYS 专项：13 项通过。
- 全仓库回归：111 项通过。
- `py_compile`：通过。
- `git diff --check`：通过。
- CSV/payload/逐 ID/身份归并/异常不提权/正式字段合规扫描：通过。
- XLSX 全工作表值、公式和视觉验收：通过。
- Obsidian 画像数量、唯一来源映射、文件名和索引验收：通过。

下一步只允许：提交本轮 FULL 工件与本 ADR，经身份复核后用非强制 Git Data API 更新原分支，等待 PR #36 CI 成功，请求 `nancywrayg57-jpg` 最终画像审计，然后恢复通用监控自动化并停止。不得自行合并 PR、关闭 Issue、领取其他 Issue 或进入下一医院。

<Handoff_State>
Target: Issue #35 中山大学孙逸仙纪念医院最终画像审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/35
PR: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/36
Branch: codex/mhrj/issue-35-gzsys-trial
Phase: WAITING_OWNER_FINAL_PROFILE_AUDIT
Completed:
- FULL 658 行追加完成；664 ID = 658 正式 + 6 护理排除，逐 ID 与身份归并对账完整
- XLSX 六工作表值/公式/视觉验收完成；658 份画像与索引一一映射完成
- 三份 TRIAL 工件已精确清理；FULL payload/report、总底表和正式画像保留
CurrentFacts:
- 总底表 15 家医院、5232 行；本院 658 行，81 条异常均未提权
- 唯一详情失败为目录仍公开列出的 ID 25208 郑眉光，画像中保留异常和目录证据
Next:
- 提交、非强制 Git Data API 推送原分支、等待 CI、请求 owner 最终画像审计并停止
Constraints:
- 仅官方公开渠道；禁止第三方平台、患者评价、隐私、登录/验证码绕过
- 不自行合并 PR、关闭 Issue、领取下一 Issue或进入下一医院
Artifacts:
- D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_official_doctors_payload.json
- D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_official_doctors_report.md
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\中山大学孙逸仙纪念医院\_索引.md
</Handoff_State>
