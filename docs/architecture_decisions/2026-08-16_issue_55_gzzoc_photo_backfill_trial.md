# Issue #55 中山大学中山眼科中心存量照片补录 TRIAL

> 日期：2026-08-16
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/55>
> 分支：`codex/mhrj/issue-55-photo-backfill-gzzoc`
> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 照片政策：`WAITING_OWNER_DERIVATIVE_OR_ORIGINAL_DECISION`

## 1. 目标与边界

本轮只处理总底表中 `医院=中山大学中山眼科中心` 且 `照片文件` 为空的 205 行，按 Issue #55 先完成 10 位、至少 3 个科室的照片 TRIAL。TRIAL 不写总底表 payload/CSV/XLSX，不刷新正式画像，不进入 FULL。

固定合规边界：

1. 只访问 205 行既有 `来源链接` 中的医院官网数字 node 详情页。
2. 只接受详情页与医生姓名同一 `.showcase-5-0` 容器中唯一 `.showcase-media img` 引用的本人职业照。
3. 只接受 `gzzoc.org.cn` 同域 `/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/` 公开资源；拒绝页头、页尾、预约图、正文插图、占位图和第三方域名。
4. 页面引用的 `?itok=` 参数按原值请求；不构造、不替换、不探测任何页面未引用的原图 URL。
5. 下载保留官网响应原始字节，不压缩；图片逐张核验字节数、SHA-256、魔数和宽高。
6. FULL 在 owner 完成 TRIAL 审计与大图裁决前由 CLI 硬熔断。

## 2. 现场范围与选样

总底表 payload 现场对账：

- 中山大学中山眼科中心且 `照片文件` 为空：205 行。
- 上述 205 行 `照片链接` 也全部为空。
- 来源链接：205 个唯一数字 node，均为 `http(s)://www.gzzoc.org.cn/node/<ID>`。
- 非空科室口径：20 种。

选样采用确定性规则：按总底表顺序优先抽取尚未覆盖的科室，再补足到 10 位。最终 10 位覆盖 10 个原始科室口径，超过 Issue 要求的至少 3 个科室。

| 姓名 | 详情 ID | 底表原始科室 | 命名首原子科室 | 主职称 |
|---|---:|---|---|---|
| 易珍 | 12767 | 小儿眼病与眼遗传病科 | 小儿眼病与眼遗传病科 | 主治医师 |
| 原永广 | 3195 | 斜视、弱视、双眼视觉功能 | 斜视 | 主治医师 |
| 付月 | 3163 | 玻璃体、视网膜视神经疾病 | 玻璃体 | 主治医师 |
| 罗燕 | 3160 | 玻璃体、视网膜视神经疾病、眼免疫与葡萄膜炎 | 玻璃体 | 教授 |
| 何嫦 | 3274 | 白内障 | 白内障 | 副主任医师 |
| 戴烨 | 3119 | 眼免疫与葡萄膜炎 | 眼免疫与葡萄膜炎 | 副主任医师 |
| 于珊珊 | 3182 | 眼底疾病 | 眼底疾病 | 副主任医师 |
| 吕林 | 3170 | 眼底疾病、高度近视科 | 眼底疾病 | 教授 |
| 曲艺欣 | 14195 | 眼整形与泪器病 | 眼整形与泪器病 | 主治医师 |
| 刘耀明 | 3302 | 眼眶病与眼肿瘤 | 眼眶病与眼肿瘤 | 主治医师 |

## 3. 实现决策

新增专用脚本 `work/gzzoc_photo_backfill.py`：

1. 从总底表 payload 读取固定 205 行范围；范围行数、照片链接空值、来源链接唯一性或域名任一漂移即停止。
2. TRIAL 固定为 10 位、至少 3 个科室；不允许通过参数扩大或缩小 Issue 规定样本。
3. 详情页不可达率超过 10% 时触发 `[FATAL - HUMAN_INTERVENTION_REQUIRED]`；任何职业照 DOM 结构或姓名不一致立即熔断，照片下载前停止。
4. URL 白名单只接受页面属性实际引用的同域公开资源。脚本可以记录 `src/srcset/data-src/data-original` 中出现的 URL，但不会从派生图路径推导原图。
5. 文件名固定为 `姓名-首原子科室-主职称-医院.<魔数扩展名>`；同名目标已存在且内容不同才追加详情 ID，仍冲突则拒绝覆盖。
6. TRIAL 结果写入独立 JSON/CSV/Markdown 和 10 张样本照片；四份总底表受保护资产在执行前后做 SHA-256 对账。
7. 新增 `work/tests/test_gzzoc_photo_backfill.py`，覆盖严格详情/图片 URL、职业照容器与姓名绑定、正文图片排除、页面引用原图记录、跨科室选样、职称与科室命名、魔数/尺寸和原图探测零容忍。

## 4. TRIAL 结果

- 详情请求：10/10 HTTP 200；不可达率 0%。
- 职业照 DOM：10/10 与预核验结构一致；姓名 10/10 与底表一致。
- 照片下载：10/10 成功；失败 0。
- 科室覆盖：10 个原始科室口径。
- 照片总字节：9,135,521；平均 913,552 bytes。
- 照片尺寸：10/10 均为 960×1440；全部命中宽度大于 800px 的大图裁决门禁。
- 按平均值线性估算 205 行派生图容量：187,278,160 bytes，约 178.60 MiB。该数字只用于 owner 裁决，不代表 FULL 实际照片可得数或最终容量。
- 页面职业照容器引用的原图 URL：0；构造原图路径请求：0；原图大小未知。
- 联系表人工视觉复核：10 张均为单人医生职业照，未发现患者、儿童、合影、占位图或通用图。

10 张样本逐图字节、SHA-256、尺寸、官网 URL 和命名清单见：

- `work/中山大学中山眼科中心_photo_backfill_trial_payload.json`
- `work/中山大学中山眼科中心_photo_backfill_trial_doctors.csv`
- `work/中山大学中山眼科中心_photo_backfill_trial_report.md`
- `work/中山大学中山眼科中心_photo_backfill_trial_contact_sheet.jpg`

## 5. 派生图与原图裁决事实

官网详情页实际引用路径形如：

```text
/sites/zoc.live1.sysucloud2.sysu.edu.cn/files/styles/large_960_x_auto_/public/...jpg?itok=...
```

10 个职业照容器均没有通过 `srcset`、`data-src` 或 `data-original` 引用 `/files/public/...` 原图。按 Issue 红线，Codex 没有移除 `/styles/large_960_x_auto_/` 构造原图路径，也没有发送任何探测请求。

因此当前可审计的二选一结论为：

1. 页面派生图：有 10 张真实样本、原始响应字节、960×1440 尺寸和 205 行线性容量估算。
2. 原图：当前页面授权 URL 集合中不可得，不能伪造样本或大小估算。

FULL 只可在 owner 明确裁决以下一种路径后继续：批准使用页面实际引用的派生图；或由 owner 下发页面自身引用的原图入口。Codex 不自行扩大 URL 白名单。

## 6. 零变更与验证闭环

TRIAL 前后四份受保护资产 SHA-256 完全一致：

| 资产 | SHA-256 |
|---|---|
| 总底表 payload | `30D6FAA36C404B6C39CA4D07D63D117C5D723EDBFAB5D8EF1E7B3FE6FA583D3C` |
| 总底表 CSV | `35396CEB412BA6BC98CEE2E592019C21A95A2513CED79937EB7F84B7CD561914` |
| 总底表 XLSX | `B61ED7E3E3FA24FC3F61ED7F103DBE684EDB2F341E74098197A9E4D730902834` |
| 总底表更新报告 | `CD6FFF06B933F4A765838281F52F06F3E1228FCEA37E5D3B4A9441BD8120D96A` |

验证结果：

- `py_compile`：通过。
- Issue #55 专项 unittest：8/8 通过。
- FULL 负向熔断：退出码 1，联网和总底表写入前停止，四份受保护资产哈希不变。
- 真实 TRIAL：10 行、10 图、10 科室、详情/结构/图片失败均为 0。
- 10 图逐张字节/SHA-256/魔数/尺寸验证：通过。
- 联系表视觉复核：通过。

## 7. 阻塞、根因、修正与防复发

专项测试首次执行发现文件名主职称把“副主任医师”降格为“主任医师”。根因是子串匹配顺序中较短的“主任医师”位于“副主任医师”之前。最小修正为把更长职称置前；回归测试固定 `副主任医师、医学博士 → 副主任医师`，随后 8/8 专项测试通过。真实 TRIAL 未在该缺陷下运行，未产生错误文件名。

防复发措施：

1. 职称只使用固定最长优先列表，缺失写“未标注”，不从姓名或简介猜测。
2. 职业照必须同时通过同容器姓名、唯一 DOM、官方同域路径、响应 Content-Type、魔数和尺寸门禁。
3. 页面未引用的原图请求计数必须恒为 0；validator 发现非零立即失败。
4. TRIAL 和 FULL 分离；无 owner 大图裁决时所有非 `--trial-only` 命令硬熔断。

## 8. 当前停止点

TRIAL 工件已完成本地验收。下一步只允许提交并通过非强制 Git Data API 推送原分支、创建关联 Issue #55 的 PR，然后等待 owner 对 TRIAL 给出明确“通过”或“有条件通过”并裁决大图路径。未切换到 FULL 指令前，不得写入总底表、刷新正式画像、下载其余 195 行照片、合并 PR 或关闭 Issue。

<Handoff_State>
Target: Issue #55 中山大学中山眼科中心存量照片补录 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/55
Branch: codex/mhrj/issue-55-photo-backfill-gzzoc
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 核验 205 行照片补录固定范围与 205 个唯一官网数字 node
- 完成 10 位/10 科室详情与职业照 TRIAL，10 图全部下载和四重校验通过
- 完成 10 图联系表人工视觉复核，未发现患者、儿童、合影、占位图或通用图
- 完成页面派生图实测与 205 行容量估算；原图引用 0、原图探测 0
- 完成专项测试、FULL 负向熔断和受保护资产零变更验证
Next:
- 提交并通过非强制 Git Data API 推送原分支，创建关联 Issue #55 的 PR
- 等待 owner TRIAL 审计与派生图/原图裁决
- 只有 owner 明确通过并切换 FULL 后才能处理剩余范围、写总底表和刷新画像
Constraints:
- 只使用既有来源链接详情页自身引用的官方本人职业照
- 禁止构造或探测页面未引用原图；禁止患者/儿童影像、占位图、通用图
- TRIAL 不写总底表 payload/CSV/XLSX，不刷新正式画像
- 不自行 approve/merge PR，不关闭 Issue，不领取其他 Issue
Artifacts:
- D:\workspace\信息收集整理\work\gzzoc_photo_backfill.py
- D:\workspace\信息收集整理\work\tests\test_gzzoc_photo_backfill.py
- D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_trial_payload.json
- D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_trial_doctors.csv
- D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_trial_report.md
- D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_trial_contact_sheet.jpg
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\中山大学中山眼科中心\照片
</Handoff_State>
