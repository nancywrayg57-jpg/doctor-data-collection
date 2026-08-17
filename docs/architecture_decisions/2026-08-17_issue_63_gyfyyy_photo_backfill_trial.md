# Issue #63 广州医科大学附属第一医院照片补录 TRIAL / FULL

## 目标与授权

- GitHub Issue：`#63`。
- 医院：广州医科大学附属第一医院。
- 官网：<https://www.gyfyyy.cn/>。
- 医生目录：<https://www.gyfyyy.cn/cn/ylfw/czcx/>。
- 当前阶段：`FULL_READY_FOR_FINAL_OWNER_AUDIT`。
- 本阶段只允许固定 10 人跨科室、跨职称照片试采；入口台账、总底表 payload/CSV/XLSX、更新报告、正式照片目录、616 份医生画像和 `_索引.md` 必须零修改。
- 未取得当前关联 PR 中 owner 明确 `通过` / `有条件通过` 且切换为 `FULL_APPEND_AND_OBSIDIAN` 前，禁止正式回填、正式照片写入、画像嵌入或入口台账改写。

## 范围与结构证据

1. 统一总底表中本院范围为 616 行、616 个唯一官网医生详情 URL；616 行的 `照片链接`、`照片文件` 均为空。
2. 固定样本 10 人覆盖 8 个科室，职称分层为正高 3 人、副高 3 人、其他 4 人。
3. 官网首页、Issue 指定医生目录和 10 个详情页均通过常规公开会话返回 HTTP 200。
4. 详情页标题以 `姓名_` 起始并包含本院全称；本人职业照唯一位于 `div.photo img`。
5. 两种页面直引原图路径同时存在并已覆盖：`/Upload/<年月>/<数字>.<扩展名>` 4 张，`/images/doctor/<拼音>.<扩展名>` 6 张。
6. 页面正文叙事图、floatcard 等非 `div.photo` 区域完全不进入候选解析；图片请求仅使用容器自身引用 URL并携带对应详情页 Referer，不构造或探测页面未引用路径。

## TRIAL 实现边界

- 脚本：`work/gyfyyy_photo_backfill_trial.py`。
- 专项测试：`work/tests/test_gyfyyy_photo_backfill_trial.py`。
- 脚本只提供 `--trial-only`、`--mark-visual-pass` 和 `--validate`，没有 FULL 写入路径。
- 来源 URL 只接受 `gyfyyy.cn` 科室路径内的 `doctor_<数字ID>.html`；照片 URL 只接受 `div.photo` 容器直引、同域、无查询参数的两类固定路径。
- 占位检测沿用 Issue #61 收官后的双侧边界：仅对小于 40 KiB 的 GIF 按 `nopic/noimage/placeholder` 路径标记或低色板且浅灰中性像素占比至少 70% 判定；不得单凭 GIF 格式判占位。
- 每张实图核验 HTTP、原始字节、SHA-256、魔数、扩展名和尺寸；原始响应字节直接落盘，不压缩。
- TRIAL 前后对入口台账、总底表 payload/CSV/XLSX、更新报告、本院画像 Markdown 树和正式照片目录做哈希/树快照比对。
- 单张大于 5 MiB 只记入 owner FULL 逐图审计清单；单张大于 20 MiB 是后续 FULL 熔断边界。本轮均未命中。

## 结果

- 实采 10/10，熔断问题 0/10。
- 路径风格：`Upload原图` 4，`doctor原图` 6。
- 总字节 1,949,147；最小 3,547；中位数 40,699；平均 194,914；最大 1,031,569。
- 大小分桶：小于 200 KiB 8 张，200 KiB–1 MiB 2 张；大于 5 MiB 0 张。
- 以样本均值估算 616 行约 114.50 MiB，该数字仅用于容量预估，不代表 FULL 实际结果。
- 联系表已逐格人工视觉复核：10/10 均为对应医生的单人成人职业照；无正文叙事图、患者、儿童、合影、占位图、二维码或公共装饰图。
- 正式受保护资产前后快照完全一致；本院正式照片目录仍不存在。

## 附带台账条款

- Issue #63 明确要求在同一 PR 将台账序号 15 南部战区空军医院追加“管理员裁决跳过（军队医院，2026-08-17）”，并把“下一步动作”改为“跳过”。
- 该条款已记录为本 Issue 待执行项；为满足当前 TRIAL “正式资产零修改”门禁，本阶段未改写入口台账。
- 只有 owner 通过 TRIAL 并切换 FULL 后，才允许将该台账变更纳入正式事务和 CSV/XLSX 一致性校验。

## 工件

- `work/广州医科大学附属第一医院_photo_backfill_trial_payload.json`
- `work/广州医科大学附属第一医院_photo_backfill_trial_manifest.csv`
- `work/广州医科大学附属第一医院_photo_backfill_trial_report.md`
- `work/广州医科大学附属第一医院_photo_backfill_trial_contact_sheet.jpg`
- `work/广州医科大学附属第一医院_photo_backfill_trial_photos/`

## 验证

- `python -m py_compile work/gyfyyy_photo_backfill_trial.py`：通过。
- 专项测试 `python -m unittest work.tests.test_gyfyyy_photo_backfill_trial -v`：11/11 通过。
- 通过仓库外既有临时依赖目录完成 `requests/bs4/openpyxl` 最小 import 探针后，全仓测试 `python -m unittest discover -s work/tests -p 'test_*.py'`：252/252 通过；未安装全局依赖、未修改系统 PATH 或仓库依赖配置。
- `python work/gyfyyy_photo_backfill_trial.py --validate`：通过。
- 联系表已使用原始分辨率视图逐格人工核验，并固化 `PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。
- 工件逐图字节/SHA-256/魔数/尺寸闭环、正式资产前后快照、`git diff --check` 和 `git fsck --no-progress` 通过；`git fsck` 仅报告仓库既有 dangling 对象，无对象损坏。

## 风险与下一步

1. 等待 `nancywrayg57-jpg` 在 Issue #63 关联 PR 评论或 Review 中审计联系表、来源边界、两种路径风格、大小分布和正式资产零修改证据。
2. 当前不得执行 FULL、改写入口台账、写正式照片目录、修改总底表或画像。
3. 若 owner 明确 `通过` / `有条件通过` 并切换为 `FULL_APPEND_AND_OBSIDIAN`，再在同一分支补充事务化 FULL 能力、常规 AUTO-GENERATED 照片块最小刷新、616 行四数对账和台账序号 15 跳过标记。
4. FULL 完成后仍由 owner 最终审计、合并 PR 并关闭 Issue；双门禁完全满足前不得领取下一 Issue。

## FULL Owner 门禁

- `nancywrayg57-jpg` 于 2026-08-17T06:40:37Z 在 PR #64 明确给出 `通过`，并把 Phase 切换为 `FULL_APPEND_AND_OBSIDIAN`。
- Owner 独立复算 TRIAL 10/10 字节、SHA-256、魔数和尺寸，复下钟南山、黄铮两张原图哈希一致，并确认联系表 10/10 单人职业照。
- Owner 明确授权 616 行全量、失败三态、三载体一致、常规 AUTO-GENERATED 画像照片块、5–20 MiB 单列终审、>20 MiB 熔断，以及台账序号 15 同事务跳过标记。

## FULL 结果

1. 四数闭环：范围/应采 616、实采 616、失败 0、留空 0；失败三态“详情不可达 / 无照片容器 / 占位图”均为 0。
2. 官网页面引用路径：`Upload原图` 355、`doctor原图` 261；未构造或探测页面未引用路径，第三方来源 0，传输不完整重试 0。
3. 照片总字节 78,803,761（75.15 MiB），最大单张 2,363,483；`<200KiB` 545、`200KiB-1MiB` 63、`1-5MiB` 8、`5-20MiB` 0、`>20MiB` 0。
4. 照片目录新增 616 个页面引用原始字节文件；逐图字节、SHA-256、魔数、扩展名和尺寸全量闭环。
5. 总底表 9,222 行保持不增不减；本院仅 `照片链接` 616 格、`照片文件` 616 格发生变化，共 1,232 个授权单元格；payload/CSV/XLSX 25 列逐值一致。
6. 616 份既有 `AUTO-GENERATED` 画像各只在“基础信息”区新增一行照片引用；不新建画像，`_索引.md` 哈希不变，其他画像字节不变。
7. 台账序号 15 南部战区空军医院只修改两格：“排除或注意事项”追加“管理员裁决跳过（军队医院，2026-08-17）”，“下一步动作”改为“跳过”；JSON/CSV/XLSX 一致。
8. XLSX 写入仅使用 workspace loader 提供的 `@oai/artifact-tool`；没有使用 openpyxl、COM、LibreOffice 或直接 OOXML 写入。工作簿修改前后均完成渲染检查。

## 一次最小修复记录

- 首次 FULL 在 600/616 后、正式资产落盘前安全停止。日志显示李培鑫官网标题为 `李培鑫 _心血管内科_...`，姓名后的下划线前多一个官网空格，而原校验只接受严格 `姓名_`。
- 根因是官网标题分隔符空白差异，不是姓名、来源或照片容器冲突。最小修复只把标题前缀校验调整为 `姓名 + 可选空白 + 下划线`，仍要求姓名位于标题首部且标题含医院全称。
- 新增回归测试，并对剩余 16 个详情页只读预检；第二次 FULL 成功。没有第二次业务失败，未触发两次失败熔断。

## FULL 验证

- `python work/gyfyyy_photo_backfill_trial.py --validate-full`：通过。
- 专项测试：18/18 通过；全仓测试：259/259 通过。
- `@oai/artifact-tool` 后置检查：总底表 6 个工作表、入口台账 5 个工作表均存在，公式错误扫描均为 0；11 个页签逐页渲染视觉检查通过，表头、交替行、宽度、冻结与目标台账行均可读。
- 台账序号 15 XLSX 目标为工作表第 16 行；目标说明和“跳过”与 JSON/CSV 一致。
- `git diff --check` 通过；`git fsck --no-progress` 未发现对象损坏；换行符检查确认大文件业务差异为本院 616 行照片字段和台账指定两格，不是整文件噪声。
- `work/pearl_delta_hospital_entry_ledger.json` 的历史索引内容为 CRLF，但仓库 `.gitattributes` 已指定 `eol=lf`；FULL 提交前仅对该文件执行一次 LF 规范化。使用 `--ignore-cr-at-eol` 复核后，业务差异仍严格只有台账序号 15 的上述两格。

## 当前交接

1. FULL 工件：`work/广州医科大学附属第一医院_photo_backfill_full_payload.json`、`work/广州医科大学附属第一医院_photo_backfill_full_reconciliation.csv`、`work/广州医科大学附属第一医院_photo_backfill_full_report.md`。
2. 当前只待 Codex 将同一分支提交通过 Git Data API `force=false` 推送，并在 PR #64 回报 `FULL_READY_FOR_FINAL_OWNER_AUDIT`。
3. 之后只等待 `nancywrayg57-jpg` 最终画像审计、PR 合并和 Issue 关闭；不得自行合并、关闭 Issue 或领取下一 Issue。
