# 2026-08-12 Issue #11 南方医科大学第五附属医院试采

## 目标与门禁

按 GitHub Issue #11 只处理南方医科大学第五附属医院两个 owner 指定官方入口，逐入口普查 `yisheng_xq.php` 医生详情，按详情 ID 跨入口去重后试采 10 位医生；只生成 TRIAL 审计材料，不写统一总底表，不生成本院正式 Obsidian 画像。

- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/11`
- 台账序号：14
- 城市：广州市（从化区）
- 官网首页：`http://www.ny5y.cn/`
- 工作分支：`codex/mhrj/issue-11-ny5y-trial`
- Pull Request：`https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/13`
- Codex developer：`xtzhou247`
- Claude owner：`nancywrayg57-jpg`
- 当前阶段：`TRIAL_WAITING_CLAUDE_AUDIT`

Claude 明确审计“通过”或“有条件通过”并把固定提示词切换为 `FULL_APPEND_AND_OBSIDIAN` 前，禁止正式追加、生成本院正式画像或领取其他 Issue。

## 授权入口与排除范围

本轮仅使用：

1. `http://www.ny5y.cn/zhuanjia_mingyi.php?id=100`
2. `http://www.ny5y.cn/zhuanjia_lingnan.php?id=162`

严格拒绝 `keshi_jianjie.php`、`keyanjiaoxue_zhuanjia.php?id=55`、异常附加查询参数、第三方域名和非 `yisheng_xq.php?id=<数字>` 详情 URL。两个入口均为普通 HTTP 200，无登录、验证码或反爬挑战；未进行任何绕过。

## 入口普查结果

| 分类 | 官方入口 | 页面性质 | 列表页 | 原始详情链接 | 唯一详情 | 归属 |
|---|---|---|---:|---:|---:|---|
| 专家风采 | `zhuanjia_mingyi.php?id=100` | 官网单页专家名单 | 1 | 134 | 133 | 南方医科大学第五附属医院官网专家风采栏目 |
| 岭南名医 | `zhuanjia_lingnan.php?id=162` | 官网单页荣誉专家名单 | 1 | 80 | 80 | 南方医科大学第五附属医院官网岭南名医荣誉栏目 |

- 入口候选关系：213。
- 跨入口重叠详情：79。
- 专家风采独有：54。
- 岭南名医独有：1。
- 跨入口去重后唯一详情：134。
- 两入口均未发现分页链接或独立院区归属。

## 站点适配决策

新增最小站点级适配 `ny5y_official_expert`：

1. `ny5y_entry_kind()` 只接受两个 owner 入口及各自唯一 `id` 参数。
2. `ny5y_detail_id()` 只接受同站 `/yisheng_xq.php?id=<数字>`，用于严格过滤和跨入口详情身份去重。
3. 列表只读取满足上述规则的详情链接；不跟随其他栏目或分页猜测。
4. 详情只读取 `.yuanzhang`、`.suoshulei`、`.xq_zhicheng`、`.xq_content`、`.xq_xiangxi_jieshao_xq` 五个 DOM 区块，避免导航污染。
5. `.yuanzhang` 姓名只取容器直接文本，排除内嵌 `<span>` 中的行政职务。
6. “专家风采/岭南名医”是栏目或荣誉分组，不写入真实科室；详情没有科室时保持空白并标记人工复核。
7. “岭南名医”保留在职称身份和亮眼经历线索中，且亮眼经历只从详情正文抽取，不使用列表父容器噪声。
8. TRIAL 抽样对长列表做等距分散，并保持多入口轮询，以提高科室覆盖；不改变其他站点默认采样顺序。

## 试采命令与结果

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "南方医科大学第五附属医院" `
  --entry-url "http://www.ny5y.cn/zhuanjia_mingyi.php?id=100" `
  --entry-url "http://www.ny5y.cn/zhuanjia_lingnan.php?id=162" `
  --trial-only --max-doctors 10 --no-xlsx `
  --min-departments 5 --min-entry-categories 2 `
  --max-pages 5
```

- 模式：`trial_only`
- 样本：10 位，10 个唯一官方详情 URL
- 入口覆盖：2 类（专家风采、岭南名医）
- 真实科室覆盖：9 个
- 列表失败：0
- 详情失败：0
- 排除非医生：0
- 异常提示：1 条
- 未生成试采 XLSX
- `master_updated=false`

## 样本摘要

| 姓名 | 科室 | 职称摘要 | 来源入口 | 异常提示 |
|---|---|---|---|---|
| 黄艺洪 | 留空 | 主任医师、医学硕士、岭南名医 | 岭南名医 | 科室需人工复核 |
| 司昌荣 | 中医科 | 主任中医师、岭南名医 | 专家风采 | 无 |
| 许志松 | 儿童重症医学科 | 副主任医师、岭南名医 | 专家风采 | 无 |
| 尹凯 | 全科 | 三级教授、医学博士、博士生导师、岭南名医 | 专家风采 | 无 |
| 王敏聪 | 关节外科 | 副主任医师 | 专家风采 | 无 |
| 李志强 | 口腔科 | 副主任医师、医学硕士、岭南名医 | 专家风采 | 无 |
| 肖芬球 | 妇科 | 副主任医师 | 专家风采 | 无 |
| 梁健华 | 影像诊断科 | 副主任医师、岭南名医 | 专家风采 | 无 |
| 罗扬 | 泌尿外科 | 副主任医师 | 专家风采 | 无 |
| 王宏波 | 神经内科 | 副主任医师、岭南名医 | 专家风采 | 无 |

黄艺洪为岭南名医入口唯一独有详情，官网 `.suoshulei` 仅显示荣誉栏目而非真实科室，因此科室留空；未根据正文中的神经方向推断科室。

## 字段与合规核验

- payload 10 行、CSV 10 行，逐字段差异 0。
- 10 个来源唯一，全部严格匹配 `http://www.ny5y.cn/yisheng_xq.php?id=<数字>`。
- `keshi_jianjie.php`、`keyanjiaoxue_zhuanjia.php`、新闻、采购、招聘、患者评价和导航污染命中 0。
- 学历、科研、论文等官网公开证据保留在详情正文和证据线索中，未混入专长字段，也未作营销改写。
- 未使用第三方平台、患者评价、排名、隐私或登录后数据。
- 未绕过登录、验证码、反爬或权限限制。
- 未生成正式画像。

## 总底表安全证明

试采前后以下四项 SHA-256 完全一致，且总底表中本院仍为 0 行：

| 资产 | SHA-256 |
|---|---|
| 总底表 XLSX | `95503CADE849592F13750D3F8AB059E5253CBA4CAEBBE0B9A2B1442D671916B1` |
| 总底表 CSV | `4E5AEBDE5402525E1921224C34EE685188E834B0E518ED0683283C8D3A517DCC` |
| 总 payload | `7A4DB2080093A572F85000DDE2D71D834CA3EEC69D6E7E10C4A1978704439499` |
| 总底表更新报告 | `69CA4AD9DB1C0D9B3E7824BDADFF9AF4A2B8B73D929DF2B4BC632F842E07FF3B` |

## 验证结果

- Python 编译通过。
- 采集器与画像生成器共 34 项测试全部通过。
- NY5Y 测试覆盖严格 URL、列表过滤、详情 DOM、姓名内嵌职务清洗、荣誉科室清空、分散抽样、79 条跨入口重叠和完整 payload 链路。
- `git diff --check` 通过。

## 阻塞、根因、解决方法与防复发

### 1. Python 依赖不在 bundled 默认搜索路径

- 根因：bundled Python 缺少采集依赖，系统 `python` 不可依赖。
- 解决：复用既有临时依赖目录，通过 `PYTHONPATH` 配合 bundled Python；未安装机器级依赖。
- 预防：每轮先核验解释器绝对路径和依赖导入，不依赖命令名。

### 2. 首次科室覆盖门禁只得到 3 个科室

- 根因：通用采样按来源 URL 字符串排序，NY5Y 详情 ID 与页面科室分布均存在聚集，前 10 位不能代表全院目录。
- 解决：仅对 NY5Y TRIAL 使用入口内等距分散采样，再跨入口轮询；最终覆盖 9 个真实科室。
- 预防：长单页目录的 TRIAL 采样应同时验证入口覆盖和候选位置分散，不把字符串顺序当作业务代表性。

### 3. 补丁锚点误命中相邻采集器并触发熔断

- 根因：多个函数有相同 `by_link` 和返回字典结构，初始短锚点把改动插入通用解析器、GZZOC/NBKJ，而不是目标函数。
- 解决：按 Agent.md 连续两次失败熔断；管理员解除后用函数名与局部行号交叉核验，恢复 GZZOC/NBKJ 原逻辑，并证明只有 `collect_generic()` 使用站点详情身份去重。
- 预防：重复结构补丁必须使用函数级唯一锚点；补丁后用 `rg -B/-A` 枚举所有命中作用域，再运行完整回归测试。

### 4. 姓名字段混入行政职务

- 根因：`.yuanzhang.get_text()` 同时读取姓名直接文本和内嵌 `<span>` 职务文本。
- 解决：姓名只读取 `.yuanzhang` 直接文本节点，职务仍留在详情页面其他官方字段中。
- 预防：结构化 DOM 字段需要测试嵌套标签，不能默认整容器文本均属于同一字段。

### 5. 岭南名医栏目被误当作科室

- 根因：岭南独有详情的 `.suoshulei` 显示荣誉栏目，通用列表回退又可能将入口分类填回科室。
- 解决：NY5Y 详情和候选回退均清空荣誉分类；官网没有真实科室时留空并标记人工复核。
- 预防：荣誉类入口必须进入通用科室禁用集合，真实科室只能来自详情页明确证据。

## 提交与 PR

- 本地 TRIAL 提交：`7d8ed02b1cd7e311ccb10f7010a858344dcf3fe8`
- Git Data API 远端 TRIAL 提交：`714614fd6fc6a8033b71d0aa9d2247eb0ee3e5b5`
- 本地/远端 tree：`51599e05fdbb419ef85ae06118c5a729c1f4f3c8`
- PR #13：`https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/13`
- PR 仅以 `Refs #11` 关联当前 Issue，未使用 `Closes #11`；TRIAL 审计通过后仍需同一 Issue 的 FULL 和最终画像审计。

## 工件

- `work/collect_official_doctors_batch.py`
- `work/tests/test_collect_official_doctors_batch.py`
- `work/南方医科大学第五附属医院_official_doctors_payload.json`
- `work/珠三角三甲医院_医生画像自动采集总底表_payload.json`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.xlsx`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.csv`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表_更新报告.md`
- `医生画像仓库/99_资料来源/珠三角三甲医院_Obsidian缺失画像补充生成报告.md`
- `医生画像仓库/01_试点医院/南方医科大学第五附属医院/`
- `docs/architecture_decisions/2026-08-12_issue_11_ny5y_trial.md`
- `docs/agent_prompts/codex_next_prompt.md`

<Handoff_State>
Target: Issue #11 南方医科大学第五附属医院 FULL 与最终画像审计
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/11
GitHubPR: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/13
Phase: FULL_WAITING_FINAL_PROFILE_AUDIT
Completed:
- 已通过 PR #12 owner 固定提示词同步门禁并同步最新 main
- 已取得 Claude 对 TRIAL 的明确“通过”和 FULL_APPEND_AND_OBSIDIAN 指令
- 已全量采集并追加 134 位医生，生成本院 134 份画像和 1 个索引
- 已清理本院三份 TRIAL 临时工件，保留正式单院 payload、总底表和正式画像
CurrentFacts:
- 入口候选关系 213，去重后唯一候选 134，跨入口重叠 79
- 全量 134 位、唯一官方来源 134、列表失败 0、详情失败 0、非医生排除 0
- 总底表 8 家医院、2299 位医生；本批新增 134、重复跳过 0
- 黄艺洪官网未给真实科室，科室留空并标记人工复核
- payload/CSV/XLSX 本院各 134 行，逐字段差异 0；39 项测试通过
- 本院画像 134、索引双链 134、来源缺失/多余 0；可选证据区块错配 0
Next:
- 提交并通过非强制 Git Data API 推送当前 FULL 结果到 PR #13 原分支
- 等待 Claude 对最终画像明确审计；不得自行批准或合并 PR
Constraints:
- 仅医院官网公开渠道
- 不使用第三方平台、不绕过登录/验证码、不采集患者隐私
- 不纳入科室介绍和研究生导师栏目，不自行扩围
- 最终画像审计通过、PR 合并关闭、Issue 关闭、CI 成功前不领取其他 Issue
Artifacts:
- work/南方医科大学第五附属医院_official_doctors_payload.json
- 医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.xlsx
- 医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.csv
- 医生画像仓库/01_试点医院/南方医科大学第五附属医院/
- docs/architecture_decisions/2026-08-12_issue_11_ny5y_trial.md
</Handoff_State>

## FULL_APPEND_AND_OBSIDIAN 完成状态

Claude owner 在 PR #13 明确审计 TRIAL“通过”，并下发完整 `FULL_APPEND_AND_OBSIDIAN` 指令。PR #12 已由 `xtzhou247` 审批后由 owner 合并；当前分支合并最新 `origin/main`，只在固定提示词发生冲突，并按 owner 最新 FULL 指令解析为单一执行态。

### 全量采集与总底表

- 专家风采唯一详情 133、岭南名医唯一详情 80、候选关系 213、跨入口重叠 79、去重后 134。
- 全量医生 134、唯一官方来源 134、列表失败 0、详情失败 0、非医生排除 0。
- 新增 NY5Y 写入前硬门禁：在任何总底表写操作前校验两个入口计数、唯一数、重叠数、结果行数、错误数、严格来源 URL、擅长前缀、黄艺洪空科室/异常/荣誉证据。
- 擅长字段统一剥离开头 `擅长：` / `擅长:`；原始证据保留在 `specialty_raw`。无 `.xq_content` 显式擅长的 3 条保持空白。
- 总底表由 2165 行增至 2299 行，医院数由 7 增至 8；本批新增 134、重复跳过 0、显式刷新 0。
- 单院 payload、总 payload、CSV、XLSX 中本院均为 134 行、134 个唯一来源；除全局 `序号` 作用域外逐业务字段差异 0。
- 六个工作表均完成修改后渲染检查；公式错误扫描为 0。

### Obsidian 画像

- 仅以 `--hospital 南方医科大学第五附属医院 --generate-missing-only` 生成本院，未覆盖任何既有画像。
- 本院生成 134 份正式画像、跳过 0，生成 `_索引.md` 1 份，索引 Obsidian 双链 134。
- 画像来源与总底表 134 个来源一一对应；缺失来源 0、多余来源 0、非 NY5Y 官方详情来源 0。
- 黄艺洪画像科室为空、复核状态为待人工复核、保留岭南名医荣誉及 `id=282` 官网来源。
- 教育与进修经历区块 66 份、科研项目与成果区块 73 份、论文与学术产出区块 76 份；逐画像对照官网详情正文关键词，区块出现与证据门禁错配 0。
- 业务内容中第三方 URL、患者评价和疗效承诺命中 0。3 组同名医生以不同来源和消歧文件名保留，来源无重复。

### 最终资产 SHA-256

| 资产 | SHA-256 |
|---|---|
| 总 payload | `11C51AF1C35FE98201144B7D3DAABBB61EE34D6B870E33EA8EE5A55E89D523D1` |
| 本院正式 payload | `169DE54ED99A257E7C6FA9219F2FA2067BC8763A2114C0DD5B28C3B654D639AD` |
| 总底表 XLSX | `607F7EBCE6C5A4D79D3FDEAF298DEB825DFACAAA2BB79ADF1999DB55BE5F6078` |
| 总底表 CSV | `C6284540677BB14214ED20E976245DE2C7FA0213BB01D0809B2331FCBA1EEA4E` |
| 总底表更新报告 | `E0308D5B6AEEF621B655840F2F92D988F95196E6AB8700CF960AE8AB017E334C` |
| 缺失画像补充生成报告 | `2F3C6E8456BCEAC673E306AA27EBF33AF337E3E3CA6FE81F2E970AC216CF6088` |

## FULL 阻塞、根因、解决方法与防复发

### 6. 全量采集完成后 Node.js 运行时查找失败

- 现象：134 个官网详情已顺序采集并通过 NY5Y 写入前门禁，CSV/总 payload 已更新；生成 XLSX 时 CLI 报“未找到 Node.js，无法生成 Excel 底表”并退出，造成 CSV/JSON 已更新而 XLSX/更新报告仍为旧版的短暂不一致。
- 根因：`BUNDLED_NODE` 硬编码为另一台 Windows 用户 `C:\Users\zhouxinting\...\node.exe`；当前用户为 `Administrator`，且 `node` 不在 PATH。
- 解决：将 bundled Node 路径改为基于 `Path.home()` 的当前用户路径，保留 PATH 回退；增加 bundled 优先、PATH 回退和两者缺失三项单测。利用已经完整保存的总 payload 离线重建 XLSX 和更新报告，没有重复请求 134 个官网详情。
- 防复发：机器相关运行时路径禁止硬编码用户名；长耗时采集必须先持久化单院 payload，并让写表阶段支持从现有 payload 离线恢复。执行前快速核验 Node 绝对路径可用性。

### 7. 临时校验器的 shell 转义与清理策略阻塞

- 现象：一次内嵌 Python 正则被 PowerShell 解析器拒绝；三次精确 `Remove-Item` 清理命令在执行前被桌面安全策略拒绝。
- 根因：复杂正则嵌在 PowerShell 双层引号中，括号与转义冲突；桌面策略对删除命令采用保守拦截。
- 解决：把只读校验写入本轮临时 Python 文件；三份文本 TRIAL 工件用 Patch 精确删除。临时目录先用 `git clean -ndx -- <唯一目录>` dry-run 证明范围，再用同一精确 path 执行清理。
- 防复发：复杂校验优先使用受版本范围控制的临时脚本；任何临时目录清理先 dry-run，且绝不对 workspace 根或通配范围执行删除。

## 最终验证

- 采集器与画像生成器 39 项测试通过，用时约 0.255 秒。
- Python 编译通过，`git diff --check` 通过。
- 总底表 134 行三资产逐字段对账通过，六个工作表视觉检查通过，公式错误 0。
- 134 份画像、134 个来源、134 个索引双链和可选证据区块逐项验证通过。
