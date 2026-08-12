# 2026-08-12 Issue #11 南方医科大学第五附属医院试采

## 目标与门禁

按 GitHub Issue #11 只处理南方医科大学第五附属医院两个 owner 指定官方入口，逐入口普查 `yisheng_xq.php` 医生详情，按详情 ID 跨入口去重后试采 10 位医生；只生成 TRIAL 审计材料，不写统一总底表，不生成本院正式 Obsidian 画像。

- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/11`
- 台账序号：14
- 城市：广州市（从化区）
- 官网首页：`http://www.ny5y.cn/`
- 工作分支：`codex/mhrj/issue-11-ny5y-trial`
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

## 工件

- `work/collect_official_doctors_batch.py`
- `work/tests/test_collect_official_doctors_batch.py`
- `work/南方医科大学第五附属医院_trial_doctors.csv`
- `work/南方医科大学第五附属医院_trial_payload.json`
- `work/南方医科大学第五附属医院_trial_report.md`
- `docs/architecture_decisions/2026-08-12_issue_11_ny5y_trial.md`
- `docs/agent_prompts/codex_next_prompt.md`

<Handoff_State>
Target: Issue #11 南方医科大学第五附属医院试采
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/11
Phase: TRIAL_WAITING_CLAUDE_AUDIT
Completed:
- 已逐入口普查两个 owner 指定官网入口
- 已按详情 ID 去重后试采 10 位，覆盖两个入口和 9 个真实科室
- 已严格排除非 yisheng_xq 详情 URL，修正姓名内嵌职务和荣誉分类科室污染
- 已验证总底表四项资产未变化，本院仍为 0 行
CurrentFacts:
- 入口候选关系 213，去重后唯一候选 134，跨入口重叠 79
- 样本 10 位、唯一官方来源 10、详情失败 0、异常提示 1
- 黄艺洪官网未给真实科室，科室留空并标记人工复核
- 34 项测试通过，CSV/payload 逐字段差异 0
Next:
- 提交并用 Git Data API 推送分支，创建引用 Issue #11 的 TRIAL PR
- 等待 Claude 试采审计；通过前禁止正式追加和画像生成
Constraints:
- 仅医院官网公开渠道
- 不使用第三方平台、不绕过登录/验证码、不采集患者隐私
- 不纳入科室介绍和研究生导师栏目，不自行扩围
- 不自行批准或合并 PR，不领取其他 Issue
Artifacts:
- work/南方医科大学第五附属医院_trial_doctors.csv
- work/南方医科大学第五附属医院_trial_payload.json
- work/南方医科大学第五附属医院_trial_report.md
- docs/architecture_decisions/2026-08-12_issue_11_ny5y_trial.md
</Handoff_State>
