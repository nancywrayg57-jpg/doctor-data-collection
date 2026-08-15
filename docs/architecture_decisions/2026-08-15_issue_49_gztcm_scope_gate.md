# Issue #49 广州中医药大学第一附属医院 TRIAL 范围门禁

> 日期：2026-08-15
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/49>
> 分支：`codex/mhrj/issue-49-gztcm-photo-trial`
> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 医院：广州中医药大学第一附属医院
> 官网：<https://www.gztcm.com.cn/gztcm/gzb.html>
> owner 指定医生入口：<https://www.gztcm.com.cn/myzl/myhc/>

## 1. 目标与边界

Issue #49 要求先现场核验指定入口的可达性和页面性质。若“名医荟萃”只是荣誉子集，而官网另有全院科室目录，必须停止并回报 owner 裁决入口集合，不得由 Codex 自行扩围。

本轮只使用 `gztcm.com.cn` 医院官网公开页面和普通 HTTPS GET，未访问医生详情、未下载照片、未运行采集器、未创建 TRIAL 工件，也未写入统一总底表。未使用第三方平台、登录、Cookie 注入、验证码或挑战绕过。

## 2. 可达性与页面性质

2026-08-15 本机现场复核结果：

| URL | HTTP | 响应字节 | 页面标题 / 结构 | 结论 |
|---|---:|---:|---|---|
| `https://www.gztcm.com.cn/gztcm/gzb.html` | 200 | 49,418 | `公众版首页_广州中医药大学第一附属医院` | 官网首页普通公开 GET 可达 |
| `https://www.gztcm.com.cn/myzl/myhc/` | 200 | 36,526 | `名医荟萃_广州中医药大学第一附属医院` | 指定入口明确是“名医荟萃”栏目 |
| `https://www.gztcm.com.cn/ksjs/` | 200 | 37,850 | `科室介绍_广州中医药大学第一附属医院` | 官网另有独立科室树 |
| `https://www.gztcm.com.cn/gztcm/ksjs/nk/` | 200 | 31,411 | `大内科_广州中医药大学第一附属医院` | 科室树可继续下钻到临床科室集合 |

以上请求均未出现重定向、验证码或挑战页面，因此当前阻塞不是可达性或反爬问题，而是指定入口的范围完整性问题。

## 3. 指定入口是 41 人荣誉子集

指定 `myzl/myhc` 页面同时提供以下可核验分页元数据：

```text
size=20
page=1
itemCount=41
pageCount=3
```

使用官网页面自身的公开分页参数访问 `index.html?_page_=3` 返回 HTTP 200，元数据仍为 `page=3 / itemCount=41 / pageCount=3`，页面只有 1 个医生详情链接。由此确认该栏目合计 41 人，而不是只读取了第一页。

栏目标题直接标明“名医荟萃”，属于精选名医/荣誉性质集合。Issue 要求的是全院医生采集；仅凭这 41 人不能证明覆盖全院，也不能把该精选集合标记为全院完整目录。

## 4. 官网另有 9 类科室树

独立科室入口 `https://www.gztcm.com.cn/ksjs/` 当前公开列出 9 个大类：

1. 大内科
2. 大外科
3. 妇儿中心
4. 骨伤中心
5. 针灸推拿康复中心
6. 肿瘤中心
7. 脑病中心
8. 急诊中心
9. 其他

只读抽查“大内科”页面时，官网分页元数据为 `itemCount=13 / pageCount=1`，页面明确包含脾胃病科（胃肠病）、呼吸与危重症医学科、血液科、全科医学科（综合科）、肝胆病科等临床科室链接。这足以证明官网存在独立且明显更广的科室组织树。

本轮没有继续下钻这些科室、枚举医生或把 `/ksjs/` 自行加入采集范围；完整入口集合、科室边界和可能的院区归属必须由 owner 唯一裁决。

## 5. 范围门禁结论与解除

初次现场核验后状态为 **`TRIAL_SCOPE_BLOCKED`**，当时未下钻科室、未访问医生详情、未下载照片，也未运行 TRIAL。

2026-08-15，`nancywrayg57-jpg` 在 PR #50 明确裁决选项 2 并解除范围门禁：

1. 主范围固定为 `https://www.gztcm.com.cn/ksjs/` 九大类下全部科室入口；
2. `https://www.gztcm.com.cn/myzl/myhc/` 41 人“名医荟萃”作为补充通道并入；
3. 两个通道只按官网详情 ID 去重；名医详情未展示当前科室时留空并标注；
4. TRIAL 固定 10 位、至少 3 个真实科室、覆盖两个通道并包含本人职业照；
5. 未获 `FULL_APPEND_AND_OBSIDIAN` 明确授权前不得写统一总底表或生成正式画像。

当前 owner 授权范围已唯一闭合，状态切换为 **`TRIAL_READY_FOR_OWNER_AUDIT`**。

## 6. 总底表保护证明

初次停止时，统一总底表中 `医院` 字段精确等于“广州中医药大学第一附属医院”的记录为 0，且本院 TRIAL 工件为 0。完成真实 TRIAL 后再次复核，以下三项受保护资产的长度、修改时间和 SHA-256 仍与试采前完全一致，证明本轮未写统一总底表。

| 受保护资产 | 长度 | LastWriteTimeUtc | SHA-256 |
|---|---:|---|---|
| 总底表 XLSX | 4,360,914 | `2026-08-15T08:00:15.7908120Z` | `E4F358CB18EE5DAD4DB43B198193CF90C9129FFE77A017AFB1E61FFBA3514DF3` |
| 总底表 CSV | 17,197,217 | `2026-08-15T08:00:15.6515714Z` | `6860DDDAA34A14E082B1CAC18DC751FC7FE09734C1C46DFE2BAC70975CC8C16C` |
| 总底表更新报告 | 5,335 | `2026-08-15T08:00:15.8320383Z` | `05BF8151ECAAFBA43486090704F8E79426E2A2300E6B2B860E0222F97EF64C22` |

## 7. 阻塞、根因、解决方法与防复发

### 指定入口与全院采集范围不一致

- 阻塞：owner 指定 URL 是 41 人“名医荟萃”，同时官网存在 9 类科室树；当前无法证明 41 人覆盖全院。
- 根因：入口台账记录了一个官方精选栏目，但尚未完成“栏目性质、分页规模、全院覆盖和科室树关系”的范围核验。
- 解决：在任何医生详情或照片请求前执行页面性质与覆盖范围硬门禁；发现更广科室树后立即停止，由 owner 明确授权 41 人子集、封闭科室集合或跳过。
- 防复发：D 级入口在进入 TRIAL 前固定记录页面标题、分页总量、科室树、院区边界和“是否可声称全院覆盖”；未形成唯一授权集合不得让通用适配器自行发现并扩抓。

### 首次真实运行的报告失败

- 阻塞：首次真实 TRIAL 已完成普查、详情读取和照片处理，但通用报告渲染阶段触发 `KeyError: existing_profile_count`。
- 根因：GZTCM 新 payload 的 `meta` 未补齐通用 `render_report()` 既有契约字段；采集数据本身未失败，且 `--trial-only --no-xlsx` 保证未进入总底表写入。
- 最小修正：在 GZTCM `meta` 中补入按结果行计算的 `existing_profile_count`，不改通用报告契约和其他适配器。
- 防复发：GZTCM 写出前门禁、专项测试和全量回归同时保留；第二次真实 TRIAL 已成功写出 JSON、CSV 和报告，未再触发熔断。

### 照片异常的管理员裁决

- 失效官方图片允许按“无照片留空”处理并写明异常标注。
- 首次 HTTP 非 200 或 `Timeout`、`ConnectionError`、`ChunkedEncodingError`、`IncompleteRead` 时，等待 1 秒，以同一 URL、同一详情 Referer 和同一请求头仅重试 1 次；连续两次失败后留空并标注。
- 不变更请求头、不注入 Cookie、不绕过验证；成功图片保留官网原始字节，不压缩。

## 8. TRIAL 普查与样本结果

| 指标 | 结果 |
|---|---:|
| 官网科室大类 | 9 |
| 科室入口 | 70 |
| HTTP 404 科室专家目录 | 19 |
| HTTP 200 空专家目录 | 42 |
| HTTP 200 非空专家目录 | 9 |
| 科室树详情关系 / 唯一 ID | 41 / 41 |
| 名医荟萃详情 ID / 页数 | 41 / 3 |
| 双通道 ID 交集 | 0 |
| 合并后唯一详情 ID | 82 |
| 详情读取成功 / 失败 / 姓名不一致 | 82 / 0 / 0 |
| TRIAL 行数 / 双通道覆盖 / 真实科室覆盖 | 10 / 2 / 4 |
| 照片应采 / 实采 / 失败 / 留空 | 10 / 10 / 0 / 0 |
| 编码替换 / 高置信乱码 / 排班入库 / 私用区残留 | 0 / 0 / 0 / 0 |

TRIAL 样本为周岱翰（名医荟萃，官网详情未标当前科室并已标注）、晏显妮、罗立杰、李大年、汪双双、陈坚雄、江其龙、邱仕君、邓中光、张子敬；科室树样本覆盖心理睡眠科、肌病科、胃肠外科和结直肠外科。10 张照片均已逐张目视复核为单人职业头像或白大褂照片，未发现患者、合影、新闻图或占位图。

报告已逐条列出 70 个科室 URL、每科室唯一详情 ID、名医荟萃 41-ID 清单和 82-ID 对账。同名“邓中光”的两个不同详情 ID 保持独立，不按姓名误合并。

## 9. 验证闭环

- GZTCM 专项测试：`9/9` 通过。
- `work/tests` 全量单元测试：`165/165` 通过。
- JSON、CSV、报告均按 UTF-8 复核，无替换字符、高置信乱码或私用区残留。
- 只读对账确认：70 个唯一科室入口、41 个科室树关系、41 个名医关系、82 个唯一详情、10 行 CSV、10 张照片与报告 70 行科室表全部闭合。
- 10 张照片的本地字节数和 SHA-256 与 payload、报告逐张一致。
- FULL 门禁仍要求 PR #50 owner 明确审计通过并切换 `FULL_APPEND_AND_OBSIDIAN`；当前不得执行正式追加。

<Handoff_State>
Target: Issue #49 广州中医药大学第一附属医院照片 TRIAL 审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/49
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/50
Branch: codex/mhrj/issue-49-gztcm-photo-trial
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 已按 owner 裁决封闭 9 类 70 科室树 + 41 人名医荟萃范围，仅按详情 ID 去重
- 82 个唯一详情全部读取成功；TRIAL 10 行覆盖双通道和 4 个真实科室
- 10 张官网本人职业照全部下载、逐张目视复核并完成字节/尺寸/SHA-256 对账
- GZTCM 专项测试 9/9、全量单元测试 165/165 通过
- 总底表 XLSX、CSV 和更新报告的长度、时间、SHA-256 均保持不变
CurrentFacts:
- 70 科室中 19 个专家目录 404、42 个空目录、9 个非空目录；科室树 41 ID、名医 41 ID、交集 0、合计 82 ID
- 照片应采/实采/失败/留空为 10/10/0/0；编码、乱码、排班和私用区残留均为 0
- FULL 授权尚未下发，统一总底表和正式 Obsidian 画像均未变更
Next:
- 精确提交并通过非强制 Git Data API 更新原分支
- 在 PR #50 请求 owner 审计 TRIAL；等待明确通过并切换 FULL_APPEND_AND_OBSIDIAN
Constraints:
- 仅官方公开页面；禁第三方、患者信息、排班入库、登录/验证码/挑战绕过
- 不越出 owner 授权的 70 科室 + 41 名医范围；同名不同 ID 保持独立
- 当前不写总底表、不生成正式画像、不自行合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-15_issue_49_gztcm_scope_gate.md
- D:\workspace\信息收集整理\work\广州中医药大学第一附属医院_trial_payload.json
- D:\workspace\信息收集整理\work\广州中医药大学第一附属医院_trial_doctors.csv
- D:\workspace\信息收集整理\work\广州中医药大学第一附属医院_trial_report.md
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\广州中医药大学第一附属医院\照片
</Handoff_State>
