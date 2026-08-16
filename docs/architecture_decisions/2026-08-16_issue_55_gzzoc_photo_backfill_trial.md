# Issue #55 中山大学中山眼科中心存量照片补录 TRIAL

> 日期：2026-08-16
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/55>
> 分支：`codex/mhrj/issue-55-photo-backfill-gzzoc`
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`
> 照片政策：`OWNER_APPROVED_PAGE_REFERENCED_LARGE_960_DERIVATIVE`

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

## 8. FULL 授权与两次失败熔断

Owner 于 2026-08-16T07:00:16Z 在 PR #56 明确给出 TRIAL“通过”，批准 FULL 使用页面实际引用且保留 `itok` 的 `large_960_x_auto_` 派生图，并下发 205 行 `FULL_APPEND_AND_OBSIDIAN` 指令。

正式落盘前连续两次验证均被事务门禁安全阻断：

1. 首次 FULL 的临时 XLSX 读取句柄未及时关闭，Windows 文件锁使临时工作簿无法替换；正式资产零变化。修正为使用会关闭句柄的基础 XLSX 读取路径。
2. 第二次 FULL 调用当前画像生成器刷新旧模板画像，除照片块外还会整体改写 YAML、章节和正文，被“仅照片块变化”门禁阻断；正式资产仍零变化。

按 `Agent.md` 连续两次失败熔断后停止修改。管理员随后明确选择“外科式照片块插入”：保留旧画像全文，只在唯一 `## 基础信息` 标题后的空行插入 `![姓名](照片/文件名)`，不再调用全量画像生成器。

防复发门禁：

1. 画像以原始 UTF-8 字节处理，保留 BOM 与 LF/CRLF；删除新增照片块后必须与原画像逐字节一致。
2. 全院 Markdown 文件集合不变，发生字节变化的相对路径集合必须恰好等于成功实采画像集合；失败留空画像和 `_索引.md` 必须逐字节不变。
3. 已存在照片块、基础信息插入点缺失或不唯一、画像文件映射变化均立即停止。
4. 总底表前后逐单元格比较只允许目标 205 行的 `照片链接`、`照片文件`；只有失败行才允许追加 `异常提示`。

## 9. FULL 正式结果

- 应采 / 实采 / 失败 / 留空：`205 / 205 / 0 / 0`。
- 失败三态：详情不可达 0、无照片元素 0、占位图 0；不可达率 0%。
- 照片：205 张，合计 `167,098,636` bytes（约 159.36 MiB），最大单张 `1,929,832` bytes，超过 5 MiB 为 0。
- 页面引用原图计数 0；构造或探测原图请求 0；全部保存页面引用派生图的原始响应字节，未压缩。
- 总底表保持 9,222 行；目标 205 行三载体一致，恰好 410 个单元格变化：`照片链接` 205、`照片文件` 205，其他单元格零变化。
- 画像：205/205 各新增一个照片嵌入块；205 个文件 `git numstat` 均为 `+2/-0`，删除照片块后与旧文件逐字节一致。
- `_索引.md` SHA-256 保持 `0F8E475385158A63B222200882E757D2B978C9026EE5B3223902C67BA16D7F98`。
- 入口台账 SHA-256 保持 `D6B08B3F284654024FAD0EEAC3377B095025DC294732DB030E8CC5B81655B782`。
- 总底表更新报告 SHA-256 保持 `CD6FFF06B933F4A765838281F52F06F3E1228FCEA37E5D3B4A9441BD8120D96A`。

FULL 后三载体哈希：

| 资产 | SHA-256 |
|---|---|
| 总底表 payload | `E7D366F45693E21E7912C0CFD6CB7E26E8C26C94E5174D9F5C7C39F9DB790DE8` |
| 总底表 CSV | `7F8FBFE8AC1772852BDCE8EA5237E4593411BA54FBEF010B8E7169335F86413F` |
| 总底表 XLSX | `283217C4F74595B409B89933A2DA8FAF2046CA7D51810FAC369DF3A533F90B22` |

## 10. 验证与当前停止点

- `py_compile`：通过。
- Issue #55 专项 unittest：13/13 通过。
- 全量 unittest：186/186 通过。
- FULL payload validator：205 行四数、失败三态、逐图字节/SHA-256/魔数/尺寸、单张大小和磁盘集合全部通过。
- 总底表 payload/CSV/XLSX：9,222 行逐字段一致。
- Artifact-tool：六个工作表公式错误扫描 0；六表最终渲染检查通过，保持既有版式。
- `git diff --check`：通过。

当前只允许更新原 PR #56 并等待 owner 最终画像审计。不得自行合并 PR、关闭 Issue 或领取其他 Issue；自动化在提交并成功推送、进入等待审计状态前保持 PAUSED。

<Handoff_State>
Target: Issue #55 中山大学中山眼科中心存量照片补录 FULL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/55
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/56
Branch: codex/mhrj/issue-55-photo-backfill-gzzoc
Phase: FULL_READY_FOR_FINAL_OWNER_AUDIT
Completed:
- Owner 已通过 TRIAL 并批准使用页面实际引用的 large_960_x_auto_ 派生图
- 完成 205/205 正式照片补录；失败与留空均为 0
- 完成 payload/CSV/XLSX 三载体 205 行照片两列回填与逐字段一致性验证
- 完成 205 份旧模板画像的外科式照片块插入；索引和画像其余字节不变
- 完成 13 项专项测试、186 项全量测试和六表 artifact-tool 渲染验收
Next:
- 提交并在推送前再次核验 xtzhou247 身份
- 仅通过非强制 Git Data API 更新原分支和 PR #56
- 等待 nancywrayg57-jpg 最终画像审计、CI、合并和 Issue 关闭
Constraints:
- 只使用既有来源链接详情页自身引用的官方本人职业照
- 禁止构造或探测页面未引用原图；禁止患者/儿童影像、占位图、通用图
- 不自行 approve/merge/close，不领取其他 Issue
Artifacts:
- D:\workspace\信息收集整理\work\gzzoc_photo_backfill.py
- D:\workspace\信息收集整理\work\tests\test_gzzoc_photo_backfill.py
- D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_full_payload.json
- D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_full_reconciliation.csv
- D:\workspace\信息收集整理\work\中山大学中山眼科中心_photo_backfill_full_report.md
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\中山大学中山眼科中心\照片
</Handoff_State>
