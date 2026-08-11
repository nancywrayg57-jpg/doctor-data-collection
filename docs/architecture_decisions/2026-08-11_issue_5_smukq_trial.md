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

## Claude TRIAL-2 通过与完整执行

Claude owner 在 PR #6 评论 `https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/6#issuecomment-5252272992` 对 TRIAL-2 给出明确结论 `通过`，并下发 `FULL_APPEND_AND_OBSIDIAN`。完整执行范围固定为海珠广场院区 9 个入口，预期约 95 位；不得纳入总院或其他院区。

2026-08-11 正式追加一次完成：

- 9 个入口全部成功，候选数分别为 `12、12、11、10、12、12、12、7、7`，合计 95 条。
- `mode=master_append`，批次 95 条，新增 95 条，重复跳过 0 条，详情失败 0 条。
- 目标医院 95 个来源链接全部唯一，均匹配 `https://www.smukqyy.cn/prods/<入口ID>/<数字>`，采集入口 ID 与来源 ID 错配 0 条。
- 科室覆盖 9 个，数量与各入口候选数完全一致；非医生页、异常姓名和其他院区来源均为 0。
- 总底表由 5 家、1993 位增加为 6 家、2088 位；全表异常提示记录由 37 条增加为 108 条。
- 本院异常提示不为空 71 条：63 条 `科室原文含正文，已清洗`，4 条同时含 `已清洗` 与 `通用模板低置信度`，4 条仅 `通用模板低置信度`。这些提示已原样写入总底表和本院索引。
- 本院 `擅长诊疗方向摘录` 56 条有显式标签内容，39 条无显式标签并保持空白；没有回填或推断。
- XLSX、CSV 和更新报告均已同步更新；XLSX 共 2089 行（含表头），`复核清单` 109 行（含表头），公式错误扫描 0。

正式追加后发现更新报告对多入口医院只取首个非空入口，导致本院 9 入口被压缩显示为单个入口。根因位于 `build_hospital_batches()` 的 `first_nonempty()` 聚合；已改为按医院保留全部唯一入口并增加回归测试。没有重跑网络采集，也没有重复追加数据。

## Obsidian 画像与清理结果

使用 `--generate-missing-only`，并额外跳过其余 4 家既有医院；默认跳过中山大学附属第五医院，因此本轮只生成目标医院：

- 新增医生画像 95 份，重建 `_索引.md` 1 份，跳过 0 条。
- 95 个画像来源链接唯一，并与本院总底表 95 个来源链接逐一相等；缺失 0、额外 0、非官方来源 0。
- `_索引.md` 含 95 个唯一画像链接，全部对应现存 Markdown；异常提示不为空统计为 71，提示与来源逐行对应。
- 目标目录共 96 个 Markdown（95 份画像 + 1 份索引）；全仓画像根目录 Markdown 由 1960 增加到 2056。
- 画像文件均带自动生成标记，无文件名覆盖、异常姓名、非医生页或核心字段缺失。

画像和索引核验完成后，已精确删除 3 个试采临时文件：`*_trial_doctors.csv`、`*_trial_payload.json`、`*_trial_report.md`。入口台账、总底表 XLSX/CSV、更新报告、正式 payload、画像和索引均保留。

## 当前结论与下一步

本院 `FULL_APPEND_AND_OBSIDIAN` 已完成。下一步只剩同一 Issue 的交付门禁：提交全部正式工件，使用 GitHub Git Data API 推送原分支，核对本地/远端 tree SHA；推送成功后启用 `Doctor data single-Issue monitor`，并在 PR #6 请求 Claude 最终画像审计。

`Doctor data single-Issue monitor` 启用后仍不得领取下一 Issue。只有 Claude 最终画像审计明确通过，且 PR #6 已合并并关闭，才允许进入下一 Issue。`Doctor data PR 6 audit monitor` 保持每 4 分钟检查本 PR，不检查或领取其他 Issue。

## Git 交付说明

1. TRIAL-2 远端 HEAD 为 `30de8e9ffbdaeba637d573bcdfce4dc5475f499a`，远端 tree 为 `41b5538b27b2412990420418eb185f5e095bcf94`。
2. 此前普通 Git HTTPS 推送在 `git-remote-https` 传输阶段卡住；本轮继续使用 GitHub Git Data API，不重复尝试普通 HTTPS push。
3. 正式交付提交必须动态读取提交差异，上传新增/修改 blob，并以当前远端 HEAD 为 parent 创建提交；远端 ref 更新后必须验证 tree SHA 与本地一致。

## 工件

- `D:\workspace\信息收集整理\work\collect_official_doctors_batch.py`
- `D:\workspace\信息收集整理\work\tests\test_collect_official_doctors_batch.py`
- `D:\workspace\信息收集整理\work\南方医科大学口腔医院(海珠广场院区)_official_doctors_payload.json`
- `D:\workspace\信息收集整理\work\珠三角三甲医院_医生画像自动采集总底表_payload.json`
- `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx`
- `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv`
- `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表_更新报告.md`
- `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_Obsidian缺失画像补充生成报告.md`
- `D:\workspace\信息收集整理\医生画像仓库\01_试点医院\南方医科大学口腔医院(海珠广场院区)`
- `D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md`

<Handoff_State>
Target: Issue #5 南方医科大学口腔医院(海珠广场院区)
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/5
GitHubPR: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/6
Phase: FULL_APPEND_AND_OBSIDIAN
Completed:
- Claude TRIAL-2 审计已通过
- 已从 9 个海珠广场院区入口正式追加 95 位医生
- 已核验总底表、XLSX、CSV、更新报告、异常提示和入口范围
- 已生成 95 份本院画像和 1 份索引，来源与索引均逐一核验
- 已清理 3 个试采临时文件并保留全部正式资产
- 已执行 13 项采集器单元测试并全部通过
CurrentFacts:
- 总底表为 6 家、2088 位、108 条异常；本院 95 位、71 条异常
- 本院 95 个来源唯一，9 科室全覆盖，非医生页/入口错配/详情失败均为 0
- 本院画像 95 份、索引链接 95 个、跳过 0、文件名覆盖 0
- single-Issue monitor 在正式工件提交推送前仍须保持 PAUSED
Next:
- 提交并通过 Git Data API 推送原 PR #6 分支，验证本地/远端 tree SHA
- 推送成功后启用 single-Issue monitor，并在 PR #6 请求 Claude 最终画像审计
- 每 4 分钟轮询审计与 PR 状态；审计通过且 PR 合并关闭前不得领取下一 Issue
Constraints:
- 仅医院官方公开渠道
- 只处理海珠广场院区 9 入口，不纳入总院或其他院区
- 不并行领取或执行其他 Issue
- 不自行批准或合并 PR
Artifacts:
- work\南方医科大学口腔医院(海珠广场院区)_official_doctors_payload.json
- 医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- 医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv
- 医生画像仓库\99_资料来源\珠三角三甲医院_Obsidian缺失画像补充生成报告.md
- 医生画像仓库\01_试点医院\南方医科大学口腔医院(海珠广场院区)
</Handoff_State>
