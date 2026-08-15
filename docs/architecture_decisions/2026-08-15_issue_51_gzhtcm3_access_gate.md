# Issue #51 广州中医药大学第三附属医院 TRIAL 可达性门禁

> 日期：2026-08-15
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/51>
> 分支：`codex/mhrj/issue-51-gzhtcm3-photo-trial`
> Phase：`TRIAL_ACCESS_BLOCKED`
> 医院：广州中医药大学第三附属医院
> owner 指定官网：<http://www.gzhtcm3.com/>
> owner 指定目录：<http://www.gzhtcm3.com/wsjs/zzts.htm>

## 1. 目标与停止条件

Issue #51 要求先现场核验指定官网与 `wsjs/zzts` 入口的可达性、编码和页面性质；若被拦、遇挑战或验证码，必须停止且不得绕过。只有入口可达并确认为官方医生目录后，才允许继续普查、访问医生详情、下载职业照片和运行 10 位 TRIAL。

本轮只对 owner 明确下发的两个 HTTP URL 执行普通公开 GET。未猜测或补充 HTTPS、非 `www`、新域名、镜像或第三方入口；未变更请求头、未注入 Cookie、未登录，也未尝试绕过站点拦截。

## 2. 现场证据

### 2.1 第一轮普通 GET

| URL | HTTP | 响应字节 | 重定向 | 结果 |
|---|---:|---:|---:|---|
| `http://www.gzhtcm3.com/` | 404 | 186 | 0 | 无标题、无可用导航或医生入口 |
| `http://www.gzhtcm3.com/wsjs/zzts.htm` | 404 | 186 | 0 | 无标题、无可用栏目内容 |

### 2.2 第二轮证据确认

| URL | HTTP | 响应字节 | Content-Type | 结果 |
|---|---:|---:|---|---|
| `http://www.gzhtcm3.com/` | 403 | 1,584 | `text/html` | 页面标题 `403`、正文 `Forbidden`，并显示“无权访问，因为非法请求被拒绝”；Request ID `7674221657261820185` |
| `http://www.gzhtcm3.com/wsjs/zzts.htm` | 404 | 162 | `text/html` | 正文为 `Sorry, Page Not Found` |

请求使用 `python-requests/2.34.2` 默认普通请求头，`Cookie` 为空；两轮均无重定向。首页在 404 与 403 间变化，而指定目录持续 404，当前无法取得栏目正文、标题、编码元数据、科室树、分页或医生关系。

## 3. 阻塞、根因与处置

- 阻塞：指定首页出现明确的官方访问拦截页，指定医生目录持续返回不存在；无法证明 `wsjs/zzts` 是当前公开医生目录，也无法形成合规的封闭采集范围。
- 根因判断：owner 下发的旧站 URL 当前至少同时存在访问控制和路径失效现象。仅凭公开非 200 响应无法进一步判断是 WAF 策略、站点迁移、旧路径下线还是临时故障；继续改请求头、注入 Cookie、枚举新 URL 或借助第三方搜索都会越出 Issue 授权和合规红线。
- 处置：状态切换为 **`TRIAL_ACCESS_BLOCKED`**，立即停止医生详情、照片和 TRIAL；提交本证据给 owner。按 Issue 预设流程，可由 owner 审计后直接跳过并关闭 Issue；若不跳过，必须由 owner 明确下发新的完整官方入口和唯一范围后才能恢复。
- 防复发：D 级旧站在任何适配器代码或医生请求前固定执行首页/目录 HTTP、重定向、页面标题、编码、栏目性质与范围门禁；任一入口被拦或失效时只保存最小证据，不自行发现替代域名或扩围。

## 4. 资产保护证明

本轮没有创建本院 `work` 工件或 Obsidian 画像目录；统一总底表中本院记录为 0。三份受保护资产内容哈希保持 Issue #49 合并后的基线：

| 受保护资产 | 长度 | SHA-256 |
|---|---:|---|
| `珠三角三甲医院_医生画像自动采集总底表.xlsx` | 4,427,427 | `DE43F144BC82440BE2F42923A71B8BEF6B619044656FE9C53849B4FAABE55472` |
| `珠三角三甲医院_医生画像自动采集总底表.csv` | 17,366,142 | `E6BE9E931174F96F8581AEFB28CCA0725F920C02859E824FA011873FB5F7C2CE` |
| `珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 5,604 | `AE2522550F2CF9719A64503F1AD3E8F3A32921EDA59C7AC688E9FF8F1C5757E7` |

## 5. 当前结论

本轮没有进入页面解析、医生普查或 TRIAL，因此不存在可提交的 10 位样本、照片或详情对账。当前唯一合规动作是将可达性证据推送到 PR，等待 owner 明确审计跳过或重新下发官方入口。

<Handoff_State>
Target: Issue #51 广州中医药大学第三附属医院 TRIAL 可达性门禁
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/51
Branch: codex/mhrj/issue-51-gzhtcm3-photo-trial
Phase: TRIAL_ACCESS_BLOCKED
Completed:
- 普通 GET 现场核验指定官网与目录；首页出现明确 403 拦截，目录持续 404
- 未访问医生详情、未下载照片、未运行 TRIAL、未写统一总底表或生成画像
- 已核验本院总底表记录、work 工件和画像目录均为 0，并记录受保护资产哈希
Next:
- 提交并推送本 ADR，创建关联 Issue #51 的 PR，请 owner 审计可达性证据
- owner 可按 Issue 预设流程裁决跳过；若继续，须明确下发新的完整官方入口与唯一范围
Constraints:
- 禁止变更请求头、Cookie 注入、登录/验证码/WAF 绕过
- 禁止自行猜测 HTTPS、非 www、新域名、镜像或第三方入口
- owner 未解除范围与可达性门禁前不得运行 TRIAL
Artifacts:
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-15_issue_51_gzhtcm3_access_gate.md
</Handoff_State>
