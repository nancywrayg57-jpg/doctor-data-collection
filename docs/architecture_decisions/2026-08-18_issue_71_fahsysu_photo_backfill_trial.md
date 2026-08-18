# Issue #71 中山大学附属第一医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/71>。
- 医院：中山大学附属第一医院。
- 官网：<https://www.fahsysu.org.cn/>。
- 医生目录：<https://www.fahsysu.org.cn/page/6945>。
- Phase：`TRIAL`；正式资产必须零修改。
- 工作分支：`codex/mhrj/issue-71-fahsysu-photo-backfill-trial`，基线提交 `4d355675aead44805fcdeba184ac59bca4992710`。
- Owner 于 <https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/71#issuecomment-5328041611> 批准：10 张成功照片采用正高 5 + 副高 5、覆盖 10 个不同科室首原子；黄雄庆和张旭宇作为 2 条“其他”层无照片容器证据，TRIAL 对账共 12 行。

## 范围与来源边界

1. 总底表本院固定范围为 860 行、860 个唯一 `https://www.fahsysu.org.cn/node/<ID>` 详情 URL；TRIAL 前 `照片链接`、`照片文件` 均为空。
2. 本院画像目录为 861 个文件（860 份画像 + `_索引.md`），正式照片目录不存在。
3. 医生照片只取 `.other-left .other-media .media-img[data-image-url]` 页面实际引用的 `styles/focal_point_480` 派生图；URL 必须携带且只携带一个非空 `itok`，原始响应字节不压缩、不转码。
4. 不构造、猜测或探测页面未引用的原图路径；`styles/mini200`、banner、`inline-images`、`default_images` 和装饰资源不得下载。
5. 详情页和照片最终响应必须停留在 `fahsysu.org.cn`；照片必须通过 HTTP、Content-Type、魔数、SHA-256 和尺寸验证。超过 5 MiB 单列，超过 20 MiB 立即熔断。

## 范围阻塞与 Owner 裁决

初始范围核验发现，能归入“其他”层的记录只有黄雄庆和张旭宇，两人详情页均无本人职业照。Codex 在 Issue 发布 `TRIAL_SCOPE_BLOCKED`：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/71#issuecomment-5328032228>。

Owner 的唯一裁决为：

1. 成功照片样本采用郭宇、陈昆、陈蕾、陈炜、高勇、陈华东、程钢、雷艺炎、汪睿、林维浩。
2. 10 人分别覆盖普通外科、神经外科、烧伤与创面修复科、泌尿外科、男科、小儿外科、整形外科、胸外科、血管外科、甲状腺外科；职称分层为正高 5、副高 5。
3. 黄雄庆 `node/5780`、张旭宇 `node/5795` 各生成一条 `无照片容器` 证据；必须记录现场 UTC、HTTP、`focal_point_480` 引用数和公共资源 URL/判定特征，但不得下载这些资源。

## 实现与一次诊断修正

- 新增 `work/fahsysu_photo_backfill_trial.py`，复用上一批已验证的 HTTP 会话、魔数、尺寸和快照工具，但使用 Issue #71 独立的 URL、样本、证据与验证门禁。
- 新增 `work/tests/test_fahsysu_photo_backfill_trial.py`，覆盖详情 URL、唯一 `itok`、页面引用派生图、公共图标排除、姓名一致性、Owner 固定样本、12 行 manifest 和失败证据格式。
- 第一次 TRIAL 在写 payload 前被失败证据校验拦截：容器级 HTML 解析器看到 0 个医生照片候选，而预探测正则看到 5 个 `mini200` 图标。
- 根因：5 个公共图标位于页面 action media，不在医生职业照容器内；页面另有 banner，但不属于 Owner 要求的 5 个 `mini200` 证据。
- 最小修正：当医生照片容器缺失时，只从页面其余 `data-image-url` 中筛选官方 `styles/mini200` URL作为排除证据，同时明确记录“医生照片容器缺失”。第一次失败留下的 10 个可重建 `work/` 临时照片经精确列举后删除；总底表、画像、入口台账和正式照片目录未触碰。
- 修正后的现场诊断与专项测试通过，第二次 TRIAL 成功；未触发连续两次失败熔断。

## TRIAL 结果

- 对账：12 行 = 成功照片 10 + `无照片容器` 证据 2。
- 详情：12/12 HTTP 200；照片：10/10 HTTP 200；状态闪烁、照片失败、占位图、第三方来源和页面未引用路径探测均为 0。
- 成功照片：10 个唯一 `focal_point_480?...itok=` 页面引用；JPEG 8 张、PNG 2 张；总字节 1,769,345。
- 字节统计：最小 138,120；中位数 164,711；平均 176,934；最大 240,886。
- 大小分桶：`<200KiB=8`、`200KiB-1MiB=2`、`1-5MiB=0`、`5-20MiB=0`、`>20MiB=0`；按样本均值线性估算 860 行约 145.11 MiB，仅作容量估算。
- 联系表视觉复核：10/10 均为单人成人职业照，无占位图、二维码、公共装饰图、患者、儿童或合影；payload 已固化 `PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。

## 两条失败证据

1. 黄雄庆：`https://www.fahsysu.org.cn/node/5780`，现场 `2026-08-18T12:28:35Z`，HTTP 200，`focal_point_480` 引用数 0，医生照片容器缺失。
2. 张旭宇：`https://www.fahsysu.org.cn/node/5795`，现场 `2026-08-18T12:28:36Z`，HTTP 200，`focal_point_480` 引用数 0，医生照片容器缺失。

两页均只记录以下 5 个 `mini200` 公共图标 URL 作为排除证据，下载数和落盘数均为 0：

- `action-9-1-3.png?itok=N7xVlmOY`
- `action-9-1-6.png?itok=e9BYn97e`
- `action-9-1-1_0.png?itok=lMXpEjLC`
- `action-9-2-8.png?itok=XyTEzUHK`
- `action-9-1-2_0.png?itok=thPXMwH8`

完整绝对 URL、HTTP、UTC 与判定特征已同时写入 payload、12 行 manifest 和报告。

## 正式资产保护

- TRIAL 前后入口台账、总底表 JSON/CSV/XLSX、总底表更新报告、861 个本院文件聚合快照和不存在的正式照片目录快照完全一致。
- TRIAL 只写 `work/` 工件；未回填三载体、未刷新画像、未创建正式照片目录。

## 工件

- `work/中山大学附属第一医院_photo_backfill_trial_payload.json`
- `work/中山大学附属第一医院_photo_backfill_trial_manifest.csv`
- `work/中山大学附属第一医院_photo_backfill_trial_report.md`
- `work/中山大学附属第一医院_photo_backfill_trial_contact_sheet.jpg`
- `work/中山大学附属第一医院_photo_backfill_trial_photos/`（10 个页面引用版本的原始响应字节）

## 验证与停止点

- `py_compile`：通过。
- Issue #71 专项测试：11/11 通过。
- 全仓测试：329/329 通过；使用仓库外既有本机 Python 运行时及其 `requests 2.34.2`、`beautifulsoup4 4.15.0`、`openpyxl 3.1.5`、`Pillow 12.2.0`，未安装依赖、未修改系统 PATH 或仓库依赖配置。
- `--validate`：通过，10 张照片 + 2 条失败证据 + 12 行 manifest 闭环。
- 当前停止点：`TRIAL_READY_FOR_OWNER_AUDIT`。提交、推送并创建关联 Issue #71 的 PR 后等待 owner 审计；未取得明确 `FULL_APPEND_AND_OBSIDIAN` 前不得写正式资产。

<Handoff_State>
Target: Issue #71 中山大学附属第一医院照片补录 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/71
Branch: codex/mhrj/issue-71-fahsysu-photo-backfill-trial
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/72
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 完成 Owner 裁决的正高 5 + 副高 5、10 科室、10 张页面引用 focal_point_480 原始字节照片
- 完成黄雄庆、张旭宇 2 条无照片容器失败证据；manifest 共 12 行
- 完成联系表视觉复核、正式资产零修改验证、11 项专项测试和 329 项全仓测试
CurrentFacts:
- 固定范围 860 行 / 860 唯一 node URL，TRIAL 前照片字段全空
- TRIAL 照片 10 张，总字节 1,769,345；失败证据 2 条；排除资源下载 0
- 正式照片目录仍不存在；总底表和 861 个本院文件快照未变化
Next:
- 创建关联 Issue #71 的 PR，等待 owner TRIAL 审计
- 仅 owner 明确下发 FULL_APPEND_AND_OBSIDIAN 后才可写正式资产
Constraints:
- 只采页面实际引用 focal_point_480 URL 的原始响应字节并保留唯一 itok
- 禁止构造原图、下载 mini200/banner/inline/default_images 或使用第三方来源
- 失败证据必须包含资源 URL 或判定特征；TRIAL 正式资产零修改
Artifacts:
- work/中山大学附属第一医院_photo_backfill_trial_payload.json
- work/中山大学附属第一医院_photo_backfill_trial_manifest.csv
- work/中山大学附属第一医院_photo_backfill_trial_report.md
- work/中山大学附属第一医院_photo_backfill_trial_contact_sheet.jpg
- work/中山大学附属第一医院_photo_backfill_trial_photos/
</Handoff_State>

## FULL 授权与 Owner 裁决

- Owner 在 PR #72 明确给出 `TRIAL_AUDIT_PASSED → FULL_APPEND_AND_OBSIDIAN`：<https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/72#issuecomment-5328313673>。
- FULL 固定范围仍为 860 条：复用 10 张已审计 TRIAL 照片和黄雄庆、张旭宇 2 条已审计失败证据，对其余 848 条执行采集。
- 杨嵩 `node/33035` 的详情页 HTTP 200 且存在唯一页面引用 `focal_point_480?...itok=`，但照片资源在 3 次请求和随后 5 轮、每轮间隔至少 60 秒的聚合探测中均不可达；未构造无 `itok` 原图路径，未取得或落盘照片字节。
- Owner 复测同一照片资源为 HTTP 404，并裁决按第四类“照片资源不可达”定格留痕后继续 FULL：<https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/72#issuecomment-5328766700>。完整 5 轮证据保存于 `work/中山大学附属第一医院_photo_backfill_full_flicker_probe.json`。

## FULL 事务结果

- 四数对账：固定目标 860，实采 820，正式照片落盘 820，失败留空 40。
- TRIAL 复用：成功照片 10、失败证据 2；其余 848 条中成功 810、失败 38。
- 失败分布：既有兼容计数“详情不可达”10、“照片资源不可达”1、“无照片容器”29、“占位图”0。归入兼容计数的照片请求失败行仍逐行保存详情 HTTP、页面引用数、资源 URL、重试 UTC/HTTP 与判定特征，没有用分类名替代证据。
- 正式照片总字节 129,293,979（123.30 MiB），最大单图 337,418 bytes；超过 5 MiB / 20 MiB 均为 0。
- 只采页面实际引用的 `focal_point_480` 原始响应字节；页面未引用路径探测 0、第三方来源 0。
- 三载体逐值一致；底表差异共 1,680 个单元格：`照片链接` 820、`照片文件` 820、`异常提示` 40。
- 成功 820 份 AUTO 画像严格 +2/-0；40 份失败画像零触碰；未新建画像；`_索引.md` 零变化。
- 入口台账 JSON/CSV/XLSX 和总底表更新报告保持 FULL 前哈希与字节数不变。

## FULL 工件与目视复核

- `work/fahsysu_photo_backfill_full.py`
- `work/tests/test_fahsysu_photo_backfill_full.py`
- `work/中山大学附属第一医院_photo_backfill_full_payload.json`
- `work/中山大学附属第一医院_photo_backfill_full_reconciliation.csv`
- `work/中山大学附属第一医院_photo_backfill_full_report.md`
- `work/中山大学附属第一医院_photo_backfill_full_audit_sheet.jpg`
- `work/中山大学附属第一医院_photo_backfill_full_flicker_probe.json`
- `医生画像仓库/01_试点医院/中山大学附属第一医院/照片/`（820 张）

审计拼图包含最小、最大及 8 个确定性随机样本；2026-08-18 目视复核 10/10 均为单人成人职业照，无占位图、二维码、公共装饰图、患者、儿童或合影。

## FULL 独立验证与停止点

- `work/fahsysu_photo_backfill_full.py --validate-full`：`FULL_VALIDATED`，820 成功、40 失败。
- Issue #71 TRIAL + FULL 标准库 `unittest` 专项测试：21/21 通过。
- 全仓 `unittest discover`：339/339 通过。
- 独立范围复算：对账 860 行；正式照片 820 张 / 129,293,979 bytes；修改画像 820；失败画像触碰 0；`_索引.md` 变化 0；受保护资产哈希差异 0。
- `git diff --check`：通过。
- 当前停止点：`FULL_READY_FOR_FINAL_OWNER_AUDIT`。提交并以标准 Git 协议 fast-forward 推送当前分支后，在 PR #72 发布 `FULL_DONE`；不合并 PR、不直接修改 `main`，等待 owner 最终审计。

<Handoff_State>
Target: Issue #71 中山大学附属第一医院照片补录 FULL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/71
Branch: codex/mhrj/issue-71-fahsysu-photo-backfill-trial
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/72
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: FULL_READY_FOR_FINAL_OWNER_AUDIT
Completed:
- 固定 860 条闭环：820 张正式照片、40 条失败留空，三载体逐值一致
- 820 份成功画像严格 +2/-0；40 份失败画像和 _索引.md 零触碰
- 杨嵩 3 次请求 + 5 轮聚合失败证据按 owner 裁决定格为“照片资源不可达”
- 目视复核 10/10、专项 21/21、全仓 339/339、FULL 安装校验和独立资产复算通过
CurrentFacts:
- 照片总字节 129,293,979；最大 337,418；超过 5 MiB / 20 MiB 均为 0
- 失败分布：兼容计数详情不可达 10、照片资源不可达 1、无照片容器 29、占位图 0
- 底表差异 1,680 个单元格：照片链接 820、照片文件 820、异常提示 40
Next:
- 标准 Git 协议 fast-forward 推送当前分支并在 PR #72 发布 FULL_DONE
- 等待 owner 最终审计；不得自行合并 PR 或领取下一家医院
Constraints:
- 只采页面实际引用 focal_point_480 URL 的原始响应字节并保留唯一 itok
- 禁止构造原图、下载 mini200/banner/inline/default_images 或使用第三方来源
- 自动化仅在成功提交、推送和 PR 回报后恢复为 ACTIVE；活跃业务执行期间保持 PAUSED
Artifacts:
- work/中山大学附属第一医院_photo_backfill_full_payload.json
- work/中山大学附属第一医院_photo_backfill_full_reconciliation.csv
- work/中山大学附属第一医院_photo_backfill_full_report.md
- work/中山大学附属第一医院_photo_backfill_full_audit_sheet.jpg
- work/中山大学附属第一医院_photo_backfill_full_flicker_probe.json
- 医生画像仓库/01_试点医院/中山大学附属第一医院/照片/
</Handoff_State>
