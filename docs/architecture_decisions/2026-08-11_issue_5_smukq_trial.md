# 2026-08-11 Issue #5 南方医科大学口腔医院试采

## 目标

按 GitHub Issue #5 和固定提示词，对台账序号 10 `南方医科大学口腔医院(海珠广场院区)` 执行 10 位医生试采，只生成审计材料，不写入统一总底表。

## 执行门禁

- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/5`
- 台账序号：10
- 城市：广州市
- 医院等级：三级甲等
- 官网首页：`https://www.smukqyy.cn/home`
- 医生目录入口：`https://www.smukqyy.cn/section/364`
- 台账人工复核：确认可采集
- 适配器：`generic_official_template`
- 工作分支：`codex/mhrj/issue-5-smukq-trial`
- 试采 PR：`https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/6`

台账名称、两条 URL、采集难度和人工复核状态均与 Issue 一致；试采前统一总底表中该院记录数为 0。

## 执行动作

```powershell
python .\work\collect_official_doctors_batch.py --hospital "南方医科大学口腔医院(海珠广场院区)" --trial-only --max-doctors 10 --no-xlsx
```

本轮实际使用已有 Bundled Python，并通过本轮临时目录提供缺失的 `requests` 和 `beautifulsoup4`；没有修改仓库依赖或机器级 Python 环境。

## 试采结果

- 官网列表原始卡片：17 条
- 唯一试采记录：10 条
- 详情页失败：0 条
- 列表页失败：0 条
- 实际生成 CSV、payload 和报告；因使用 `--no-xlsx`，未生成试采 XLSX
- 统一总底表 XLSX、CSV 和更新报告的 SHA-256 与修改时间在试采前后完全一致
- 脚本输出：`master_updated=false`

## 样本摘要与质量发现

| 序号 | 姓名 | 科室字段摘要 | 职称关键词 | 来源 | 初步判断 |
|---:|---|---|---|---|---|
| 1 | 就诊须知 | 空 | 医师、博士、硕士 | `https://www.smukqyy.cn/doctor/166` | 非医生页；实际为住院须知 |
| 2 | 万蕾 | 牙体牙髓病科一室，后接大段简介 | 主任医师、博士、硕士 | `https://www.smukqyy.cn/prods/364/200` | 医生页；科室字段污染 |
| 3 | 就诊须知 | 口腔颌面外科 | 医师 | `https://www.smukqyy.cn/doctor/163` | 非医生页；实际为联系方式 |
| 4 | 王贺 | 牙体牙髓病科一室 | 主治医师、医师、医学博士、博士 | `https://www.smukqyy.cn/prods/364/479` | 医生页 |
| 5 | 张伟炎 | 科室后接个人经历 | 主治医师、医师 | `https://www.smukqyy.cn/prods/364/279` | 医生页；科室字段污染 |
| 6 | 何敏昭 | 科室后接学历简介 | 主治医师、医师 | `https://www.smukqyy.cn/prods/364/376` | 医生页；科室字段污染 |
| 7 | 庞海伶 | 科室后接职称学历 | 主治医师、医师、医学硕士、硕士 | `https://www.smukqyy.cn/prods/364/501` | 医生页；科室字段污染 |
| 8 | 汤晶晶 | 科室后接职称学历 | 主治医师、医师、医学硕士、硕士 | `https://www.smukqyy.cn/prods/364/503` | 医生页；科室字段污染 |
| 9 | 李晓娜 | 科室后接大段擅长和任职 | 副主任医师、硕士 | `https://www.smukqyy.cn/prods/364/107` | 医生页；科室字段污染 |
| 10 | 覃媛冬 | 科室后接大段简介 | 主治医师、医师、医学博士 | `https://www.smukqyy.cn/prods/364/480` | 医生页；科室字段污染 |

集中异常：

1. 10 条中 2 条为医院官网内的非医生页面，姓名均被误识别为 `就诊须知`。
2. 8 条真实医生记录中 7 条的 `科室_分类页` 混入简介正文。
3. 自动报告只统计 1 条 `科室需人工复核`，未覆盖另一条非医生页和多数科室字段污染，异常数量明显低估。
4. 所有来源均为 `www.smukqyy.cn` 官方域名；未使用第三方平台，未绕过登录或验证码。
5. 发现的联系方式为医院官网公开科室联系方式页面内容，不作为医生私人联系方式采集或使用。

## 根因假设

通用模板同时把 `/prods/364/...` 医生详情和 `/doctor/...` 就诊须知页面当作候选详情页，说明 URL/锚文本过滤不足；分类上下文提取范围过宽，又使医生简介拼入 `科室_分类页`。本 Issue 仅授权试采，因此本轮不修改采集逻辑。

## Claude 审计与返修

Claude owner 在 PR #6 给出结论 `不通过`，确认 2/10 非医生页、7/8 科室污染、3 条擅长字段混入导航文本，并要求只做六项最小修正。Codex 随后在同一分支完成：

1. 对 `/section/364` 目录只接收同目录 `/prods/364/N` 详情链接，排除 `/doctor/N`。
2. 姓名黑名单增加 `就诊须知`、`住院须知`、`联系我们`、`门诊时间`。
3. 通用科室字段在 `介绍：`、简介/擅长/职称标签、年份和完整句之前截断，并保留“原文含正文，已清洗”告警。
4. 擅长只从带冒号或独立标签行的 `擅长` / 等价标签抽取；删除无标签正文回填，并在 `介绍：` 前终止。
5. 非医生页或姓名异常记录不生成重点优先级、重点关注范围和重点疾病标签。
6. 增加非医生页、科室正文污染和擅长导航污染三类告警。

对应单元测试共 10 项，覆盖 URL 过滤、姓名黑名单、科室清洗、严格擅长抽取、无效记录标签门禁和三类告警，结果全部通过。

第一次返修试采发现带显式 `擅长：` 的两条记录仍会连带收入后续 `介绍：` 正文；定位为停止标签遗漏后补充 `介绍` 终止规则和回归测试。第二次返修试采为最终待审计工件，结果：

- 试采记录：恰好 10 条；详情页失败 0 条。
- 列表发现：15 条，最终 10 条来源全部匹配 `https://www.smukqyy.cn/prods/364/N`。
- 非医生页：0 条；导航名称：0 条。
- `科室_分类页`：10/10 均为 `牙体牙髓病科一室`，无简介、年份或句子污染。
- `擅长诊疗方向摘录`：3 条来自显式标签，7 条因无显式标签保持空白；导航污染 0 条，`介绍：` 正文污染 0 条。
- 异常提示：8 条 `科室原文含正文，已清洗`；另外两类告警由单元测试覆盖，本批次未触发。
- 来源域名：10/10 为 `www.smukqyy.cn`；未使用第三方平台，未绕过登录或验证码。
- 总底表仍为 5 家医院、1993 位医生、37 条异常提示；目标医院正式记录数为 0。
- 总底表 XLSX、CSV、更新报告的 SHA-256 和修改时间在返修试采前后保持不变，脚本输出 `master_updated=false`。

## 有条件通过后的科室覆盖核验

Claude owner 在 PR #6 对返修试采给出 `有条件通过`，但把“全量采集前确认实际覆盖全院各科室”列为硬门禁：如果 `/section/364` 只能发现单一科室，必须停止追加并回报实际覆盖与各科室入口方案。

2026-08-11 只读核验医院官网首页及科室页后确认：

1. 官网导航把 `/section/364` 明确归在 `总院`，名称为 `牙体牙髓病科一室`；它不是 `海珠广场院区` 的入口。
2. `/section/364` 页面只发现 16 个 `/prods/364/N` 详情 URL，返修后的当前收集逻辑识别 15 条候选；无论按 15 或 16 计，都只覆盖总院单一科室，不能作为全院数据或海珠广场院区数据正式追加。
3. 官网首页导航共列出 39 个唯一 `/section/N` 链接，分属总院、番禺院区、海珠广场院区、盘福院区和沙河院区。
4. `海珠广场院区` 官方导航实际列出 9 个独立科室入口，只读统计共发现 95 个同目录官方医生详情 URL：

| 科室 | 入口 | 唯一详情 URL 数 |
|---|---|---:|
| 口腔种植修复科 | `https://www.smukqyy.cn/section/341` | 12 |
| 牙体牙髓病科一室 | `https://www.smukqyy.cn/section/342` | 12 |
| 牙体牙髓病科二室 | `https://www.smukqyy.cn/section/434` | 11 |
| 口腔正畸科 | `https://www.smukqyy.cn/section/343` | 10 |
| 儿童口腔科 | `https://www.smukqyy.cn/section/385` | 12 |
| 口腔颌面外科 | `https://www.smukqyy.cn/section/384` | 12 |
| 牙周黏膜病科 | `https://www.smukqyy.cn/section/386` | 12 |
| 口腔预防科 | `https://www.smukqyy.cn/section/431` | 7 |
| 舒适化治疗中心 | `https://www.smukqyy.cn/section/504` | 7 |

因此已按 Claude 条件停止正式追加。当前还存在两个未满足门禁：

1. 固定提示词 `docs/agent_prompts/codex_next_prompt.md` 现场仍为 `Phase: TRIAL`，尚未切换为 `FULL_APPEND_AND_OBSIDIAN`。
2. Issue 名称指定 `海珠广场院区`，但台账和固定提示词给出的 `/section/364` 属于总院。需要 Claude owner 或管理员明确：是修正为上述 9 个海珠广场院区入口，还是扩大为所有院区/全院入口；Codex 不自行改变医院或 URL。

## Claude 范围裁决与 TRIAL-2

Claude owner 在 PR #6 接受上述覆盖核验，确认台账原 `/section/364` 为错误入口，并裁决本 Issue 只处理 `南方医科大学口腔医院(海珠广场院区)` 的 9 个官方科室入口，不扩大到总院、番禺、盘福或沙河院区。由于首轮返修样本实际来自总院，owner 下发 TRIAL-2：重新试采 10 位医生、至少覆盖 3 个科室、不写总底表。

固定提示词已按 owner 评论更新为 9 个入口。采集器做了以下最小扩展：

1. 新增可重复传入的 `--entry-url`，只接受与医院官网同域的显式入口，并保留原台账入口和 owner 覆盖来源。
2. 多入口候选使用轮询方式抽样，避免 `--max-doctors 10` 全部落在第一个科室。
3. 新增 `--min-departments` 结果门禁；显式多入口出现列表错误或任一入口无候选时直接失败，防止部分入口成功却误报完整。
4. 对 SMUKQ `/section/N` 只接受同目录 `/prods/N/数字`；精确匹配链接不再因卡片职称文本被截断而被通用评分误删，仍拒绝 `/doctor/N` 和跨目录 `/prods/`。
5. 每条结果记录实际 `采集入口`，payload 和报告记录 9 个入口、原台账错误入口、入口来源及科室覆盖数；`--no-xlsx` 时不再误报已生成 Excel。

单元测试扩展到 12 项，覆盖多入口顺序去重、跨入口轮询抽样、SMUKQ 同目录低文本链接保留以及首轮六项修正，结果全部通过。

TRIAL-2 最终结果：

- 9 个入口全部读取成功，候选详情 URL 数依次为 `12、12、11、10、12、12、12、7、7`，合计 95 条，与覆盖核验一致。
- 最终试采 10 位医生，覆盖 9 个不同科室，超过 owner 要求的至少 3 个科室。
- 10/10 来源均为 `https://www.smukqyy.cn/prods/<入口ID>/<数字>`，入口 ID 与来源 ID 全部一致；非医生记录 0 条。
- 列表页失败 0 条，详情页失败 0 条，擅长导航/介绍正文污染 0 条。
- 8 条保留 `科室原文含正文，已清洗` 告警，其中郑俊发另有 `通用模板低置信度`；该记录姓名、科室、职称、官方详情 URL 均可追溯。
- 无显式擅长标签的 9 条记录保持空白；1 条显式标签内容保持原文，不回填、不推断。
- 总底表仍为 5 家医院、1993 位医生、37 条异常提示；目标医院 0 条。XLSX、CSV 和更新报告的 SHA-256 与修改时间均未变化，`master_updated=false`。
- 本轮使用 `--no-xlsx`，只更新试采 CSV、payload 和报告，没有生成试采 XLSX。

## 当前结论与下一步

TRIAL-2 已完成并满足 owner 的入口归属、跨科室覆盖和字段质量门禁。下一步是把本轮代码、测试、提示词、试采工件和本 ADR 提交推送到原分支及 PR #6，请 Claude 复审。只有 owner 明确通过并下发 `FULL_APPEND_AND_OBSIDIAN` 后，才能正式追加总底表和生成画像。

在 Claude 最终画像审计明确通过且本 PR 已合并关闭前，不得领取下一个 Issue。

`Doctor data single-Issue monitor` 继续暂停。只有同一医院完成全量追加、总底表验证、Obsidian 画像生成、索引核验，并把结果提交推送后才允许启用；启用后仍须等 Claude 最终画像审计通过且 PR 合并关闭，才能实际领取下一个 Issue。

`Doctor data PR 6 audit monitor` 继续每 4 分钟检查 PR #6 的 Claude 评论、Review 和状态，不领取其他 Issue。

## Git 交付说明

1. 本地提交为 `dc36210ecd06e7ab9296fe9c36d50fea7e3b7728`。
2. 两次 Git HTTPS 推送均卡在 `git-remote-https` 传输阶段；远端 API 当时确认分支尚不存在，遗留进程已精确终止，没有重复分支或部分推送。
3. 后续使用 GitHub Git Data API创建远端提交和分支；远端提交为 `58c96e812113c2179c70817331092f53cd2b36f2`。
4. 远端 tree SHA 与本地提交 tree SHA 均为 `c966e8d8accea57913ee401e024e1be298fe50ea`，5 个交付文件内容完全一致。
5. 后续如需返修，应先重新核验 Git HTTPS 传输状态；不得在不确认远端分支状态时重复推送。

## 工件

- `D:\workspace\信息收集整理\work\collect_official_doctors_batch.py`
- `D:\workspace\信息收集整理\work\tests\test_collect_official_doctors_batch.py`
- `D:\workspace\信息收集整理\work\南方医科大学口腔医院(海珠广场院区)_trial_doctors.csv`
- `D:\workspace\信息收集整理\work\南方医科大学口腔医院(海珠广场院区)_trial_payload.json`
- `D:\workspace\信息收集整理\work\南方医科大学口腔医院(海珠广场院区)_trial_report.md`
- `D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md`

<Handoff_State>
Target: 南方医科大学口腔医院(海珠广场院区) TRIAL-2
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/5
Phase: TRIAL
Completed:
- 已按 Claude owner 裁决把范围修正为海珠广场院区 9 个官方科室入口
- 已扩展采集器支持多入口、轮询抽样、科室门禁和完整性门禁
- 已生成 TRIAL-2 的 10 条试采 CSV、payload 和报告
- 已执行 12 项单元测试并全部通过
- 已确认总底表未写入
CurrentFacts:
- 9 个入口共发现 95 个同目录官方医生详情 URL，入口读取错误 0
- 试采恰好 10 条，覆盖 9 个科室，非医生页 0，详情失败 0
- 擅长导航或介绍正文污染 0；8 条保留科室原文已清洗告警
- 固定提示词为海珠广场院区 9 入口 TRIAL-2
- 总底表仍为 5 家、1993 位、37 条异常，目标医院 0 条
Next:
- 将 TRIAL-2 提交推送同一 PR #6，请 Claude 复审
- 取得 FULL_APPEND_AND_OBSIDIAN 指令后完成全量追加和画像提交推送
- 审计通过且 PR 合并关闭前不得领取下一个 Issue
Constraints:
- 仅医院官方公开渠道
- 当前未写入总底表
- 当前禁止使用 --allow-generic-append
- 只处理海珠广场院区，不扩大到其他院区
Artifacts:
- work\南方医科大学口腔医院(海珠广场院区)_trial_doctors.csv
- work\南方医科大学口腔医院(海珠广场院区)_trial_payload.json
- work\南方医科大学口腔医院(海珠广场院区)_trial_report.md
</Handoff_State>
