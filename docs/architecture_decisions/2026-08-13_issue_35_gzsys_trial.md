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
