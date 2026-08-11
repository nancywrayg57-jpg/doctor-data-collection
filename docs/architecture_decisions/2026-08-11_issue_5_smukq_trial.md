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

## 当前结论与下一步

返修后的 10 条试采已通过本地质量检查，但仍未取得 Claude 复审结论。更新试采材料提交同一 PR #6 后，等待 Claude owner 重新给出 `通过`、`有条件通过` 或 `不通过`；当前禁止正式追加。

在 Claude 审计明确通过且本 PR 已合并关闭前，不得领取下一个 Issue。

`Doctor data single-Issue monitor` 已按管理员最新口径暂停。试采 PR 审计或合并不构成启动条件；只有同一医院取得 `FULL_APPEND_AND_OBSIDIAN` 指令、完成全量追加、生成 Obsidian 画像、核验索引并把结果提交推送后，才允许启用该自动化。启用后仍须等待最终关联 PR 经 Claude 审计通过并合并关闭，才能实际领取下一个 Issue。

`Doctor data PR 6 audit monitor` 在返修提交推送并请求复审后恢复为每 4 分钟检查 PR #6 的 Claude 评论、Review 和状态，不领取其他 Issue。`Doctor data single-Issue monitor` 只有在完整阶段画像生成、索引核验和结果提交推送后才允许启动；启动后也必须等 Claude 对最终结果审计通过且 PR 合并关闭，才能领取下一 Issue。

## Git 交付说明

1. 本地提交为 `dc36210ecd06e7ab9296fe9c36d50fea7e3b7728`。
2. 两次 Git HTTPS 推送均卡在 `git-remote-https` 传输阶段；远端 API 当时确认分支尚不存在，遗留进程已精确终止，没有重复分支或部分推送。
3. 后续使用 GitHub Git Data API创建远端提交和分支；远端提交为 `58c96e812113c2179c70817331092f53cd2b36f2`。
4. 远端 tree SHA 与本地提交 tree SHA 均为 `c966e8d8accea57913ee401e024e1be298fe50ea`，5 个交付文件内容完全一致。
5. 后续如需返修，应先重新核验 Git HTTPS 传输状态；不得在不确认远端分支状态时重复推送。

## 工件

- `D:\workspace\信息收集整理\work\南方医科大学口腔医院(海珠广场院区)_trial_doctors.csv`
- `D:\workspace\信息收集整理\work\南方医科大学口腔医院(海珠广场院区)_trial_payload.json`
- `D:\workspace\信息收集整理\work\南方医科大学口腔医院(海珠广场院区)_trial_report.md`
- `D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md`

<Handoff_State>
Target: 南方医科大学口腔医院(海珠广场院区) 10 位医生试采
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/5
Phase: TRIAL
Completed:
- 已核验台账序号 10、官方 URL、确认可采集和总底表未追加状态
- 已生成 10 条试采 CSV、payload 和报告
- 已确认总底表未写入
CurrentFacts:
- 返修试采恰好 10 条，全部为 /prods/364/N 官方医生页，非医生页 0 条
- 10 条科室字段均清洗为牙体牙髓病科一室，擅长字段无导航或介绍正文污染
- 详情页失败 0 条，8 条记录保留科室原文污染已清洗告警
Next:
- 更新同一 PR #6 并请求 Claude 重新审计
- 审计通过后仍需取得 FULL_APPEND_AND_OBSIDIAN 指令并完成全量追加和画像提交推送
- 审计通过且 PR 合并关闭前不得领取下一个 Issue
Constraints:
- 仅医院官方公开渠道
- 当前未写入总底表
- 只实施 Claude 点名的六项最小修正
Artifacts:
- work\南方医科大学口腔医院(海珠广场院区)_trial_doctors.csv
- work\南方医科大学口腔医院(海珠广场院区)_trial_payload.json
- work\南方医科大学口腔医院(海珠广场院区)_trial_report.md
</Handoff_State>
