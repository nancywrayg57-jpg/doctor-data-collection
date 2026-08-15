# Issue #49 广州中医药大学第一附属医院 TRIAL 范围门禁

> 日期：2026-08-15
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/49>
> 分支：`codex/mhrj/issue-49-gztcm-photo-trial`
> Phase：`TRIAL_SCOPE_BLOCKED`
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

## 5. 范围门禁结论

当前状态为 **`TRIAL_SCOPE_BLOCKED`**，停止 TRIAL。

owner 需要在 Issue #49 或其关联 PR 中明确裁决以下唯一一种范围：

1. 仅授权指定的 41 人“名医荟萃”精选子集，并明确接受它不代表全院完整覆盖；或
2. 授权一个明确、封闭的官方科室入口集合，并说明是否包含 9 个大类及其全部下级科室；或
3. 因缺少可确认的全院入口集合而跳过本院。

在 owner 给出唯一明确裁决前，禁止开发或修改适配器、禁止运行 10 人 TRIAL、禁止下载照片、禁止写统一总底表、禁止生成正式画像，也不得领取其他 Issue。

## 6. 总底表保护证明

本轮停止时，统一总底表中 `医院` 字段精确等于“广州中医药大学第一附属医院”的记录为 0；`work` 目录中以该医院命名的 TRIAL 工件为 0。

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

## 8. 验证范围

本轮只新增范围门禁 ADR，没有修改采集器、测试、台账、总底表或画像逻辑。必要验证为：五个公开页面/分页的 HTTP 与结构核验、总底表精确医院行数、TRIAL 工件不存在、`git diff --check`、Markdown 编码与 Git 对象检查。

<Handoff_State>
Target: Issue #49 广州中医药大学第一附属医院 TRIAL 范围裁决
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/49
Branch: codex/mhrj/issue-49-gztcm-photo-trial
Phase: TRIAL_SCOPE_BLOCKED
Completed:
- 官网首页、指定名医荟萃、科室介绍和大内科页面均以普通公开 GET 返回 HTTP 200
- 指定名医荟萃分页已核验为 41 人、3 页、每页 20；第 3 页 1 人
- 官网另有 9 类独立科室树；大内科页面当前列出 13 个科室入口
- 已按 Issue 风险条款停止，未访问医生详情、未下载照片、未运行 TRIAL、未写总底表
CurrentFacts:
- 指定入口是 41 人精选名医集合，不能证明全院完整覆盖
- 总底表中本院精确 0 行；本院 TRIAL 工件 0 个
Next:
- 等待 owner 唯一裁决：仅授权 41 人精选子集、授权明确封闭科室入口集合，或跳过本院
- 获得唯一裁决前不执行 TRIAL、不开发适配器、不写总底表
Constraints:
- 仅官方公开页面；禁第三方、患者信息、排班入库、登录/验证码/挑战绕过
- 不自行把 /ksjs/ 或下级科室加入采集范围，不自行选择院区或补入口
- 不自行合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-15_issue_49_gztcm_scope_gate.md
</Handoff_State>
