# 2026-08-13 Issue #33 广州市中医院 TRIAL 与 FULL

## 目标与门禁

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/33
- 工作分支：`codex/mhrj/issue-33-gzszyy-trial`
- Phase：`TRIAL`
- 台账序号：39（A级队列最后一家）
- 医院：广州市中医院
- 官网首页：https://www.gzszyy.com/patient/
- 医生目录：https://www.gzszyy.com/expert/
- 人工复核：确认可采集

本阶段只允许普查 `/expert/` 的顶层目录、筛选模式、科室树、唯一详情、分页和院区，并试采 10 位医生且至少覆盖 3 个科室/分类；不得写统一总底表、生成正式 Obsidian 画像或自行进入 FULL。

## 目录结构与范围裁决

新增专用适配器 `gzszyy_department_expert_directory`，只接受精确入口 `https://www.gzszyy.com/expert/`，拒绝 query、fragment、其他子域和筛选子页作为任务入口。详情 URL 只接受 `https://www.gzszyy.com/expert/<20xx>/<字母数字>.html`。

官网入口存在四类路径，语义如下：

1. 未筛选的 `/expert/<页>/` 是全院“名医名家”目录，共 18 页、423 个唯一详情 ID，用于核验全院身份覆盖。
2. `/expert/<页>/dp/<ID>/` 是科室筛选目录，35 个科室入口、37 个静态分页、433 条医生—科室关系、422 个唯一详情 ID，用于获取科室归属。
3. `/expert/<页>/pr/<ID>/` 是职称筛选，入口首页有 18 个有效链接。
4. `/expert/<页>/le/<ID>/` 是专家级别筛选，入口首页有 3 个有效链接。

`pr` 和 `le` 只作为筛选语义证据，不重复采集。全院身份以未筛选目录与 `dp` 科室树的并集为准；`dp` 详情必须全部出现在顶层目录中，否则停止。现场集合对账结果：顶层 423 ID、`dp` 422 ID，`dp` 专属 0，顶层专属 1。

唯一顶层专属详情 `lNbWW4by` 为李爱平。官网卡片和详情页均未展示科室、职称或正文，但姓名与官方详情 URL 有效，因此保留为官方候选并让缺失字段保持空白，不推断、不补造。它与口腔科医生李佳芮的详情 ID `lNbWw4by` 仅字母大小写不同，实际是两个独立页面和两位不同人员，必须按大小写敏感 ID 分开。

## 院区与出诊点证据

官网首页公开列出 5 个医疗服务地点：

- 珠玑院区：https://www.gzszyy.com/district1_zzlyq/
- 天河新院区：https://www.gzszyy.com/district1_thxyq/
- 同德院区：https://www.gzszyy.com/district1_tdfy/
- 五羊门诊部：https://www.gzszyy.com/district1_wymzb/
- 同德门诊部：https://www.gzszyy.com/district1_tdmzb/

首页还列出广州医科大学中西医临床学院和广州市中医中药研究所，但两者不是院区或门诊部，不计入医疗服务地点范围。

详情页 `.doctor-code .qr-img span[title]` 是医生明确的院区/出诊点证据。10 位试采中 8 位有标签、2 位未标注；标签关系为珠玑路院区 7、同德围分院 3、同德综合门诊部 1，3 位医生有多个标签。详情页明确标签与列表卡片科室共同保留在 `科室_列表卡片`，原 `科室_分类页` 继续只保留科室关系；不得根据首页范围推断某医生属于未明示院区，也不得构造院区—科室笛卡尔关系。

## 详情解析与字段规则

1. 列表只读取 `ul.doctor-list > li` 的正式医生卡片。
2. 姓名只读卡片 `h2 a` 和详情 `.doctor-resume h1`；详情姓名与列表不一致时标记异常。
3. 科室从 `dp` 分类、列表 `.depart-info` 和详情正式科室链接归并。
4. 职称只读显式“职称”字段；主详情职称不拼接筛选词或页面导航。
5. 擅长只读正式 `p.good-at` 或列表显式擅长段；重复“擅长/专长”前缀全部清除。
6. 简介只读 `.doctor-items-intro`，复用排班和患者案例清洗，排班/时段不进入四个正式文本字段。
7. 纯护理身份使用目录显式职称排除并在 payload/report 留痕；异常记录不打疾病标签或提升优先级。
8. 同一详情 ID 的跨科室关系归并到单行；同名不同 ID 保留并标记待甄别。

## 两次诊断与防复发

### 科室 iconfont 私用区字符污染

详情科室链接内部包含 iconfont 私用区字符 `U+E68A`。最初直接使用 `anchor.get_text()`，使字符 `` 混入科室名。根因是详情 DOM 将图标节点嵌在科室锚点内，而通用空白清洗不会删除 Unicode 私用区字符。

最小修正是在详情科室原子值进入归并前删除 `U+E000–U+F8FF`，并新增含嵌套 `<i></i>` 的 DOM 回归用例。最终试采 CSV 全字段私用区字符命中为 0。防复发要求是后续不能只对最终展示字符串做清洗，必须在结构化原子字段边界删除装饰性私用区字符。

### 顶层专属详情空科室门禁误判

加入顶层 18 页与 `dp` 树集合门禁后，首次真实运行被 `顶层目录专属详情 lNbWW4by 缺少官方科室归属` 安全拦截。总底表未写入，三份受保护资产哈希未变化。

根因是门禁把“全院官方候选必须有科室”错误等同于“官网没有展示时允许留空”的宪法口径。只读核验确认 `lNbWW4by` 是李爱平的有效官方详情，而另一个大小写不同的 `lNbWw4by` 是李佳芮，不能大小写归一后合并。

最小修正是保留顶层专属详情，若顶层卡片也无科室则保持空白；集合仍严格要求 `dp` 树不得出现顶层全院目录之外的 ID。测试新增“顶层专属空科室详情仍进入普查”的场景。防复发要求是完整性门禁验证来源与身份覆盖，字段缺失通过异常提示处理，不得把官网空字段当成范围外证据。

## 最终全目录普查

- 顶层全院目录：18 页、423 个唯一详情 ID。
- `dp` 科室树：35 个科室入口、37 个静态分页、433 条关系、422 个唯一详情 ID。
- 合并后：434 条医生—科室/顶层关系、423 个唯一详情 ID。
- 有姓名详情 ID：423；空姓名 0；去重后的非空姓名值 419。
- 同名不同 ID：4 组：林少贞、唐瑾秋、王健、高三德。
- 多科室 ID：11；有科室 422，空科室 1。
- 纯护理身份排除：5；排除后合规候选 418。
- 科室分页错误 0；试采详情错误 0。

5 个纯护理身份排除为：黄金兰（主管护师）、王少敏（主任护师）、曾会萍（主任护师）、周素金（主管护师）、谭萍云（主管护师）。所有排除均保留官方详情 URL 和明确理由。

## 最终真实 TRIAL

命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "广州市中医院" `
  --trial-only --max-doctors 10 --no-xlsx
```

结果：

- 试采 10 位：叶穗林、蔡迎峰、李丽霞、赵云燕、叶绍伟、吕永慧、梁劲军、吴薏婷、邓力、许幸仪。
- 覆盖 11 个科室：体检科、名医堂、心病科（心血管内科）、肛肠科、肿瘤一区、肿瘤二区、脑病科（神经内科）、脾胃科（消化内科）、重症医学科、针灸科、骨伤科。
- 10 个姓名唯一、10 个来源链接唯一；来源全部严格匹配本院官方详情 URL。
- 详情失败 0、异常提示 0、非医生页面混入 0。
- 四个正式文本字段中的排班/时段命中 0、患者案例或可识别信息命中 0、私用区字符命中 0。
- 详情二维码院区/出诊点标签按官网原文留痕；无标签的 2 位不补造。
- 未使用第三方平台，未绕过登录、验证码或反爬，未采集患者评价、隐私或非公开数据。
- 使用 `--trial-only --no-xlsx`，未写统一总底表、未生成 XLSX、未生成正式 Obsidian 画像。

## 验证

- `py_compile`：采集器与测试文件通过。
- 广州市中医院专项测试：6 项通过，覆盖 URL 范围、`dp/pr/le` 语义、顶层/科室分页、DOM、排班清洗、护理排除、院区证据和顶层专属空字段详情。
- 全仓库测试：95 项通过。
- CSV：表头 + 10 位医生，23 列，独立解析成功。
- payload/CSV 独立断言：18/423、37/422、434/423、35 科室、5 护理排除、418 合规候选、10 个唯一合规来源全部符合基线。
- 排班、患者可识别信息、私用区字符、异常提示逐字段扫描均为 0。
- `git diff --check`：通过。
- 统一总底表三资产 SHA-256 与运行前完全一致：
  - CSV：`0C88E3E0F1DEFC42B3A71CAA5A79974AE8A6BE54874E0EE08D3794E54C96DB37`
  - XLSX：`DD89CC77EC4A3512DEF8D8A11BD78EF7777A88AC13DA5654743CDECBFEAB265D`
  - 更新报告：`2CB4D60D79B5F39042ADB8D6AC1E14C6A9D5B79DF19B0811AE904EBEEF0FBF6F`

## 工件与停止点

本轮提交代码、测试、ADR 与三份原始 TRIAL 工件：

- `work/广州市中医院_trial_payload.json`
- `work/广州市中医院_trial_doctors.csv`
- `work/广州市中医院_trial_report.md`

三份工件受 `.gitignore` 影响，发布时只精确强制暂存这三个路径，不修改忽略规则。材料进入关联 PR 且 CI 成功后，请求 `nancywrayg57-jpg` 明确给出 `通过` / `有条件通过` / `不通过`。只有 owner 明确通过并把唯一有效指令切换为 `FULL_APPEND_AND_OBSIDIAN` 后，才可在同一 Issue 和分支继续正式追加；不得自行进入 FULL、合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #33 广州市中医院 TRIAL 审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/33
Branch: codex/mhrj/issue-33-gzszyy-trial
Phase: WAITING_OWNER_TRIAL_AUDIT
Completed:
- 新增广州市中医院严格专用适配器，完成顶层全院目录、dp 科室树、pr/le 筛选与院区/出诊点普查
- 普查 18 页顶层目录与 37 页 dp 科室目录，归并 434 关系、423 唯一 ID，排除 5 个纯护理身份
- 试采 10 位覆盖 11 科室，0 详情失败、0 异常、0 排班/患者信息/私用区字符污染
CurrentFacts:
- 顶层 423 ID、dp 422 ID；唯一顶层专属空字段详情 lNbWW4by 按官网原样保留
- 纯护理排除后合规候选 418；总底表 CSV/XLSX/更新报告未改变
- 官网首页 5 个院区/门诊部；样本 8 位有详情二维码标签、2 位未标注
Next:
- 提交并通过非强制 Git Data API 发布原分支，创建 base=main 且 Closes #33 的 TRIAL PR
- CI 成功后请求 nancywrayg57-jpg 明确审计；未切换 FULL_APPEND_AND_OBSIDIAN 前停止
Constraints:
- 仅医院官网公开页面；禁止第三方平台、患者评价、隐私、登录/验证码绕过
- 官网缺失字段留空；院区/出诊点只保留详情明确标签，不推断
- 不写统一总底表，不生成正式 Obsidian 画像，不自行进入 FULL
- 不普通 push、不强推、不合并 PR、不关闭 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广州市中医院_trial_payload.json
- D:\workspace\信息收集整理\work\广州市中医院_trial_doctors.csv
- D:\workspace\信息收集整理\work\广州市中医院_trial_report.md
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_33_gzszyy_trial.md
</Handoff_State>

## FULL 授权与身份聚类

PR #34 的 `governance-check` 成功后，owner `nancywrayg57-jpg` 于 2026-08-13 在当前 PR 明确审计 TRIAL **通过**，并把唯一有效指令切换为 `FULL_APPEND_AND_OBSIDIAN`。FULL 沿用 434 关系、423 唯一详情 ID、5 个纯护理排除、418 个合规详情的审计基线。

对 4 组同名详情逐页核验后采用以下确定性裁决，不使用名字或大小写的启发式归一：

1. 林少贞 `ELe31Mb6` / `JxboyNeg`：同职称、同专长和同背景，归并为一个身份。
2. 唐瑾秋 `4QbYVOdz` / `X7ax9byv`：专长和经历高度一致，科室互补，归并为一个身份并保留 `多详情职称不一致`。
3. 高三德 `LDdwkmd1` / `QBeXY8ay`：背景一致，科室互补，归并为一个身份并保留 `多详情职称不一致`。
4. 王健 `3YaOggax` / `WZdP6yaK`：分别为检验病理科副主任技师与外科主任医师，保留两行并标记 `同名待甄别`。

新增 `merge_gzszyy_identity_rows` 只接受上述已审计 ID 组，未知同名默认分行；新增 `validate_gzszyy_full_append`，在总底表写入前同时校验范围基线、护理排除、418 个合规 ID 的身份聚类覆盖、最终主来源唯一、空姓名、同名裁决、多详情职称差异、异常行提权、擅长前缀、排班、患者信息和私用区字符。

最终身份数为 415：418 个合规详情减去 3 个同一人双详情组各 1 个重复身份。身份聚类对账为 415 行，完整映射全部 418 个合规详情 ID。

## FULL 安全拦截与现场漂移

### 顶层专属详情名称和正文发生官网更新

第一次 FULL 在写表前被 `lNbWW4by` 的旧快照门禁拦截，总底表 CSV/XLSX/更新报告哈希保持 TRIAL 基线不变。只读现场核验发现，官网当前顶层卡片和详情页均把该 ID 明确展示为 **李爱民**，且详情页新增了公开肿瘤中心履历正文；TRIAL 时记录的“李爱平且正文为空”已漂移。大小写不同的 `lNbWw4by` 仍是另一位口腔科医生，二者继续严格分开。

最小修正是不再把旧姓名和旧空正文永久硬编码，只要求 `lNbWW4by` 的最终行姓名与本轮逐 ID 官方详情对账一致；科室、显式职称和显式擅长仍因官网未展示而留空，不推断。修正后专项和全量测试通过，第二次 FULL 才进入正式写表。

### 二维码标题包含院区展示噪声

写后对账发现两个 `.doctor-code .qr-img span[title]` 并非纯地点名：

- `jnegL6aw` 的标题为 `广州医科大学附属中医医院同德围分院_综合门诊妇科_钟居孟T(60875)`。
- `openxlb7` 的标题为 `珠玑路院区v珠玑路院区`。

DOM 证据确认两者仍是官方公开二维码标题，但包含医院、科室、姓名、编号或重复分隔噪声。最小修正是在该原子字段边界只提取现场明确出现的 4 个规范标签：`珠玑路院区`、`同德围分院`、`同德综合门诊部`、`五羊门诊部`；未知标题不进入院区字段。FULL 门禁同步要求所有详情标签必须属于这 4 类。

使用显式 `--refresh-existing-hospital` 重新采集并刷新同来源的本院 415 行，结果为新增 0、刷新 415、总行数仍 4574、详情失败 0；未处理其他医院。随后只刷新带脚本自动生成标记的本院 415 份画像，人工画像保护保持生效。

## FULL 最终结果

命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "广州市中医院" `
  --allow-generic-append
```

最终刷新命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "广州市中医院" `
  --allow-generic-append --refresh-existing-hospital
```

结果：

- 顶层全院目录 18 页、423 ID；`dp` 科室树 35 个入口、37 页、422 ID；合并 434 关系、423 ID。
- 纯护理排除 5 个；合规详情 418 个；最终身份/正式行 415 个；详情失败 0。
- 3 组同一身份归并；1 组实质不同同名保留 2 行；`多详情职称不一致` 2 行；`同名待甄别` 2 行。
- 本院异常提示不为空 16 行：职称/身份需人工复核 12、科室需人工复核 1、多详情职称不一致 2、同名待甄别 2（同一行可含多个提示）。所有异常行均为普通优先级且疾病/重点标签为空。
- 院区/出诊点规范关系：珠玑路院区 228、同德围分院 137、同德综合门诊部 122、五羊门诊部 28；未标注者保持空白。
- 总底表从 4159 增至 4574 行，共 14 家医院；本院 415 行、415 个唯一来源，全部与 FULL payload 正式字段逐行一致。
- 最终受保护资产 SHA-256：
  - CSV：`95E59269410D95ACBF04D156BFBFE08A8322D2C7A0A34FFDF3D5BC4AF90515AA`
  - XLSX：`865DFA33B30D51CD79F3B5989252C835D820B93D0D536C695285CAFA5A9A074F`
  - 更新报告：`48E5F074FD3FBE6B81DFCF7D83C92C641E1DB305B6FD9140E455EC1E5AE14ED0`

## 工作簿与 Obsidian 验收

- CSV 与 XLSX 均为表头加 4574 行、23 列，`自动采集底表` 全单元格逐值一致。
- XLSX 保留 6 个工作表：`自动采集底表`、`复核清单`、`科室统计`、`重点范围统计`、`医院统计`、`采集说明`；公式错误字面量扫描为 0。
- 使用工作簿渲染对 6 个工作表的关键范围做视觉检查；表头、交替行色、长文本换行、统计汇总和说明页均可读，无空白/破损页或关键字段裁切。
- `generate_obsidian_profiles.py --hospital "广州市中医院" --generate-missing-only` 首次生成 415 份本院画像、跳过 0、重建索引 1。
- 院区标题修正后使用 `--refresh-auto-generated` 只刷新 415 份脚本自动画像，生成 0、刷新 415、跳过 0、索引重建 1。
- 本院目录有 415 份画像和 1 个 `_索引.md`；索引声明 415，含 415 个唯一 Wiki 目标且目标文件全部存在；415 个总底表来源各自只映射 1 份画像。
- 王健两种身份分别生成 `王健.md` 与 `王健_检验病理科.md`；李爱民生成 `李爱民.md`，无文件覆盖。
- 未发现患者评价、排名、正向疗效保证或第三方来源；模板中的“不得/不添加疗效承诺”仅为否定合规提示。

## 清理与最终验证

正式追加、工作簿和画像验收完成后，精确删除本院三份 TRIAL 工件：

- `work/广州市中医院_trial_payload.json`
- `work/广州市中医院_trial_doctors.csv`
- `work/广州市中医院_trial_report.md`

受保护的总底表三资产、FULL payload/报告、正式画像和索引均保留。最终 `py_compile` 通过；广州市中医院专项 9 项通过；全仓库 98 项通过；`git diff --check` 通过。

<Handoff_State>
Target: Issue #33 广州市中医院最终画像审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/33
PR: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/34
Branch: codex/mhrj/issue-33-gzszyy-trial
Phase: WAITING_OWNER_FINAL_PROFILE_AUDIT
Completed:
- 完成 423 个官方详情逐 ID 对账、5 个护理排除、418 个合规详情身份聚类和 415 个最终身份追加
- 完成 CSV/XLSX/更新报告一致性、6 工作表结构/视觉和 0 公式错误核验
- 生成并刷新本院 415 份自动画像，完成 415 个索引目标和 415 个来源一一核验
- 精确清理三份 TRIAL 文件，保留 FULL 工件与正式资产
CurrentFacts:
- 总底表 14 家医院、4574 位医生；广州市中医院 415 行、16 行异常提示不为空
- 同一人归并 3 组；王健同名不同身份 2 行；规范院区关系仅 4 类
- FULL payload/报告、总底表三资产、本院 415 画像和索引均已完成本地验收
Next:
- 提交并通过非强制 Git Data API 更新原分支
- 等待 CI 成功后请求 nancywrayg57-jpg 对最终画像和归并对账明确审计
- 不得自行合并 PR、关闭 Issue 或领取下一 Issue
Constraints:
- 仅医院官网公开来源；官网未展示字段留空，不推断院区
- 不普通 push、不强推；不合并 PR、不关闭 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广州市中医院_official_doctors_payload.json
- D:\workspace\信息收集整理\work\广州市中医院_official_doctors_report.md
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表_更新报告.md
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\广州市中医院\_索引.md
</Handoff_State>
