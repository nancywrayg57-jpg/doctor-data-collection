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

## 当前结论与下一步

当前样本存在明确非医生页面混入和集中字段污染，不建议在 Claude 审计前正式追加。已保留原始试采材料，等待 Claude owner 在 PR 评论区给出 `通过`、`有条件通过` 或 `不通过` 结论及最小修正要求。

在 Claude 审计明确通过且本 PR 已合并关闭前，不得领取下一个 Issue。

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
- 10 条中 2 条为非医生页面
- 8 条医生记录中 7 条科室字段混入简介
- 详情页失败 0 条，自动异常提示 1 条但实际问题更多
Next:
- 创建试采 PR并等待 Claude 在 PR 评论区审计
- 审计通过且 PR 合并关闭前不得领取下一个 Issue
Constraints:
- 仅医院官方公开渠道
- 当前未写入总底表
- 不修改未获授权的采集逻辑
Artifacts:
- work\南方医科大学口腔医院(海珠广场院区)_trial_doctors.csv
- work\南方医科大学口腔医院(海珠广场院区)_trial_payload.json
- work\南方医科大学口腔医院(海珠广场院区)_trial_report.md
</Handoff_State>
