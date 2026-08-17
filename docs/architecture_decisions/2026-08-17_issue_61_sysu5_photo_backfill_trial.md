# Issue #61 中山大学附属第五医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：`#61`。
- 医院：中山大学附属第五医院。
- 官网：<https://www.sysu5.cn/>。
- 医生目录：<https://www.sysu5.cn/medical-service/department-expert/doctor/category?category_target_id=All&combine=>。
- 当前阶段：`FULL_READY_FOR_FINAL_OWNER_AUDIT`。
- 本阶段只允许 10 人跨科室、跨职称照片试采；总底表、正式照片目录、413 份画像和索引必须零修改。
- 未取得当前关联 PR 中 owner 明确 `通过` / `有条件通过` 且切换为 `FULL_APPEND_AND_OBSIDIAN` 前，禁止执行正式回填、正式照片写入或画像嵌入。

## 范围与页面结构证据

1. 统一总底表中本院范围为 413 行、413 个唯一官网医生详情 URL；413 行的 `照片链接`、`照片文件` 均为空。
2. 固定样本 10 人覆盖 10 个科室，职称分层为正高 3 人、副高 3 人、其他 4 人。
3. 官网首页、目录页和 10 个详情页均通过常规公开会话返回 HTTP 200。
4. 详情页标题严格等于 `姓名 | 中山大学附属第五医院`，`body` 含 `page-node-type-doctor`。
5. 本人职业照唯一位于 `.field.field-featured-media.field-item img`；其 `src` 直接引用同域 `/sites/default/files/styles/watermark/public/...?...itok=...` 派生图。
6. 图片请求只使用详情页自身引用 URL并携带对应详情页 Referer；未删改 `itok`，未构造或探测页面未引用的原图路径。

## TRIAL 实现边界

- 脚本：`work/sysu5_photo_backfill_trial.py`。
- 专项测试：`work/tests/test_sysu5_photo_backfill_trial.py`。
- 脚本只提供 `--trial-only`、`--mark-visual-pass` 和 `--validate`，没有 FULL 写入路径。
- 来源 URL 只接受 `sysu5.cn` 数字医生详情路径；照片 URL 只接受详情页容器直接引用的 `styles/watermark/public` 路径和唯一非空 `itok` 查询参数。
- 占位图检测复用 Issue #59 口径：仅对小于 40 KiB 的 GIF 按 `nopic/noimage/placeholder` 路径标记，或低色板且浅灰中性像素占比至少 70% 判定；彩色小 GIF 不因体积小被误判。
- 每张实图核验 HTTP、原始字节、SHA-256、魔数、扩展名和尺寸；原始响应字节直接落盘，不压缩。
- TRIAL 前后对入口台账、总底表 payload/CSV/XLSX、更新报告、本院画像 Markdown 树和正式照片目录做哈希/树快照比对。
- 详情不可达、无照片容器、占位图或照片下载失败合计超过 30% 时熔断。

## 结果

- 试采：10/10 成功；详情失败、结构异常、无照片容器、占位图和照片下载失败均为 0。
- 联系表人工核验：10 张均为对应详情页的单人成人职业照；未见占位图、公共装饰图、二维码、患者、儿童或合影。
- 总字节：3,570,848；最小 74,834；中位数 325,595；平均 357,084；最大 1,109,955。
- 大小分桶：`<200KiB` 4 张、`200KiB-1MiB` 5 张、`1-5MiB` 1 张、`>5MiB` 0 张；超过 200 KiB 共 6 张。
- 按样本平均值估算 413 张约 140.64 MiB；该数字仅为容量估算，不代表 FULL 实际数量或大小。
- 受保护正式资产执行前后快照完全一致。

## 工件

- `work/中山大学附属第五医院_photo_backfill_trial_payload.json`
- `work/中山大学附属第五医院_photo_backfill_trial_manifest.csv`
- `work/中山大学附属第五医院_photo_backfill_trial_report.md`
- `work/中山大学附属第五医院_photo_backfill_trial_contact_sheet.jpg`
- `work/中山大学附属第五医院_photo_backfill_trial_photos/`

## FULL 授权与实现

- Owner 在 PR #62 评论 <https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/62#issuecomment-5311539010> 明确给出 `TRIAL 通过`，并将 Phase 切换为 `FULL_APPEND_AND_OBSIDIAN`。
- `work/sysu5_photo_backfill_trial.py` 已增加 `--full` 与 `--validate-full`：413 行全量、失败三态、30% 总问题熔断、5 MiB Owner 报告线、20 MiB 单张熔断线、非 jpg/png/gif/webp 格式熔断、payload/CSV/XLSX 三载体逐值验证、照片逐图字节/SHA-256/魔数/尺寸验证、方案 A 画像字节级最小插入和事务回滚。
- FULL 前置普查再次确认：413 行、413 个唯一详情 URL、413 份既有画像、413/413 唯一 `## 基础信息` 锚点、零既有图片引用；`_索引.md` 哈希已固化。
- Owner fenced Markdown 已原样写入 `docs/中山五院照片嵌入方式裁决单.md`，逐字符比对长度 1238、结果完全一致，裁决依据缺口已解决。

## FULL 首次执行停止证据

- 2026-08-17 只执行一次 `--full`；在事务临时区推进到进度信标 225/413 时，累计实采 223、失败 2，随后命中大图熔断。
- 熔断照片为页面照片容器直接引用的 `styles/watermark` 派生图：<https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-07/20240208173237537.jpg?itok=RSFCQ8E7>。
- 响应原始字节：`6,649,475` bytes（约 6.34 MiB），超过 Owner 明确的 5 MiB 上限；脚本抛出 `[FATAL - HUMAN_INTERVENTION_REQUIRED]` 并停止。
- 因熔断发生在事务落盘前，未生成 FULL payload/CSV/report，正式照片目录仍不存在；总底表 payload/CSV/XLSX、入口台账、更新报告、413 份画像及 `_索引.md` 均零修改。
- 未继续请求、未重试 FULL、未压缩或改写该图片，等待 Owner 对该单张 >5 MiB 页面引用派生图给出明确裁决。

## 验证

- `python -m py_compile work/sysu5_photo_backfill_trial.py work/tests/test_sysu5_photo_backfill_trial.py`
- `python -m unittest work.tests.test_sysu5_photo_backfill_trial -v`：17/17 通过。
- 通过仓库外既有临时依赖目录做 `requests/bs4/openpyxl` 导入探针后，`python -m unittest discover -s work/tests -p 'test_*.py' -v`：237/237 通过；未安装全局依赖、未修改系统 PATH 或仓库依赖配置。
- 项目指定 XLSX writer `@oai/artifact-tool` 最小 ESM import 探针通过；未改用 openpyxl/COM/LibreOffice/OOXML 写入。
- `python work/sysu5_photo_backfill_trial.py --validate`：通过。
- 联系表已使用原始分辨率视图人工核验并固化 `MANUAL_CONTACT_SHEET_REVIEW_PASSED`。
- 工件逐图字节/SHA-256 闭环、正式资产前后快照、`git diff --check` 与 `git fsck --no-progress` 均通过；`git fsck` 仅报告仓库既有 dangling 对象，无对象损坏。

## Owner 大图裁决与门禁更新

- Owner 在 PR #62 评论 <https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/62#issuecomment-5311804470> 独立核验阻塞图为标准单人职业照，并批准该图及本批同类页面引用派生图保留原始字节、不压缩、原样收录。
- 5 MiB 改为 Owner 报告阈值：`>5 MiB` 继续采集，但 FULL 报告必须逐张列出姓名、URL、字节和尺寸供最终实图审计。
- 单张 `>20 MiB` 或响应魔数不属于 jpg/png/gif/webp 时仍立即触发 `[FATAL - HUMAN_INTERVENTION_REQUIRED]`。
- 其余 FULL 指令不变；Owner 明确要求重新执行 FULL。

## FULL 重新执行结果

- 2026-08-17 按新裁决重新执行一次 `--full`，事务安装成功，Phase 为 `FULL_READY_FOR_FINAL_OWNER_AUDIT`。
- 四数闭环：范围/应采 `413`，实采 `410`，失败 `3`，留空 `3`；问题率 `0.73%`。
- 失败三态各 1 条：唐德钱为占位图；刘继红详情页 HTTP 404；袁亚君无照片容器。三行照片字段留空并追加对应异常提示。
- 正式照片共 410 张（JPG 306、PNG 104），总字节 `108,888,826`（103.84 MiB）；逐图磁盘字节数与 SHA-256 独立复算均零不一致。
- 最大图为陈贤珍 `6,649,475` bytes、4831×4833、SHA-256 `6047aebc1e4098207afef36ada8eae3138e5f2325ffb3f04675ef8243f7738c2`；`>5 MiB` 共 1 张，`>20 MiB` 为 0，已写入 FULL 报告 Owner 终审清单。
- 页面未引用路径探测为 0、第三方来源为 0、传输不完整重试为 0；图片均为详情页容器直接引用的 `styles/watermark` 派生 URL并保留 `itok`。

## FULL 安装与受保护资产验证

- 总底表 payload/CSV/XLSX 共 9222 行、25 列逐值一致；本院行变更共 823 个字段：照片链接 410、照片文件 410、失败异常提示 3，范围外行与其他字段零变化。
- 410 份既有画像各只增加 2 行（方案 A 图片引用行及空行），合计新增 820 行、删除 0 行；3 份失败画像零触碰，不新建画像。
- 正式照片目录磁盘集合与 payload 对账为 410/410；逐图字节、SHA-256、魔数、扩展名和尺寸均通过安装后验证。
- `_索引.md`、官网入口台账、总底表更新报告均 `git diff --quiet` 返回 0，保持零修改。
- FULL 工件：
  - `work/中山大学附属第五医院_photo_backfill_full_payload.json`
  - `work/中山大学附属第五医院_photo_backfill_full_reconciliation.csv`
  - `work/中山大学附属第五医院_photo_backfill_full_report.md`
  - `医生画像仓库/01_试点医院/中山大学附属第五医院/照片/`

## 最终验证

- `python -m py_compile work/sysu5_photo_backfill_trial.py work/tests/test_sysu5_photo_backfill_trial.py`：通过。
- 专项测试：19/19 通过，覆盖 5–20 MiB 放行、`>20 MiB` 熔断、非支持格式熔断和大图报告清单。
- 全仓测试：239/239 通过。
- 项目指定 XLSX writer `@oai/artifact-tool` 最小 ESM import 通过；正式 XLSX 由该 writer 生成，未替换写入实现。
- `python work/sysu5_photo_backfill_trial.py --validate-full`：通过。
- `git diff --check`：通过；工作区变更集合严格落在 Issue #61 授权路径内。

## Owner FULL 终审返修与根因

- Owner 在 PR #62 评论 <https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/62#issuecomment-5312107744> 判定唐德钱不是占位图，并下发 5 项最小返修。
- 根因不是下载后把 GIF 格式一律判为占位图：`downloaded_placeholder_reason` 原本已限制为小于 40 KiB 的 GIF。实际根因是 URL 白名单只接受 `styles/watermark` 派生路径，页面直引 `/sites/default/files/...gif` 原图被拒；随后原图系统目录中的 `default` 又误命中页面级占位标记，导致在下载前错误留空。
- 最小修正只放行同域、页面照片容器直接引用、无查询参数且不经过其他 `styles/` 的原图路径；`styles/watermark` 仍要求唯一非空 `itok`。删除了不具备字节/视觉证据的页面级 `default/avatar` 预判，下载后的 40 KiB 小 GIF 路径标记或灰底占比启发式保持不变。
- 防复发测试新增两类：唐德钱页面直引原图必须解析为 `原图`；198,358 bytes GIF 不得仅因格式判占位。既有彩色小 GIF 放行与浅灰小 GIF 占位测试继续通过。

## 唐德钱事务返修结果

- 第一次返修执行在任何业务资产写入前因 bundled Python 缺少 `requests/beautifulsoup4/openpyxl` 而停止；工作区只保留尚未提交的代码与测试修改。随后对仓库外既有临时依赖目录执行三项最小 import 探针，通过后第二次执行成功；未安装全局依赖或修改系统 PATH。
- 页面详情与照片均 HTTP 200；照片 URL 为页面容器直接引用的同域原图，带详情页 Referer 请求，未构造路径。
- 唐德钱正式照片：`唐德钱-口腔科-医师-中山大学附属第五医院.gif`，GIF89a 单帧，198,358 bytes，700×857，SHA-256 `c6761035731abb8f37f4c67e9a6bf9971eb2aae48c1adb783bee2dd601a0178b`；原始响应字节未压缩。
- 总底表相对返修前只变更唐德钱一行 3 个单元格：回填照片链接、回填照片文件、移除本次 FULL 追加的占位失败提示。payload/CSV/XLSX 仍为 9222 行、25 列逐值一致。
- 唐德钱画像只新增方案 A 图片引用与空行，共 `+2/-0`；其他 412 份画像、`_索引.md`、入口台账和总底表更新报告零修改。
- 四数更新为范围/应采 413、实采 411、失败 2、留空 2；剩余失败为刘继红详情 HTTP 404 与袁亚君无照片容器，占位图 0。
- 正式照片更新为 411 张（JPG 306、PNG 104、GIF 1），总字节 `109,087,184`；唯一 >5 MiB 图片仍为陈贤珍，>20 MiB 为 0。
- 从原始 FULL 基线累计逐单元格差异为 824：照片链接 411、照片文件 411、失败异常提示 2。

## 返修验证

- `python -m py_compile`：通过。
- 专项测试：21/21 通过；全仓测试：241/241 通过。
- `python work/sysu5_photo_backfill_trial.py --validate-full`：通过。
- `@oai/artifact-tool` 最小 ESM import：通过；返修 XLSX 仍由项目指定 writer 生成。
- 411 张照片磁盘集合、字节、SHA-256、魔数、扩展名和尺寸闭环；三载体与 FULL payload 目标行一致。
- `git diff --check` 与 `git fsck --no-progress` 通过；`git fsck` 仅报告仓库既有 dangling 对象，无对象损坏。

## 当前停止点

本记录、返修实现与工件提交到原 Issue #61 分支后，自动化保持 `PAUSED`，在 PR #62 发布返修完成信标并等待 Owner 只复核其明确的 5 项。不得合并 PR、关闭 Issue 或处理下一 Issue。

<Handoff_State>
Target: Issue #61 中山大学附属第五医院照片补录 FULL 最小返修复核
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/61
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/62
Branch: codex/mhrj/issue-61-sysu5-photo-backfill-trial
Completed:
- 已修正页面直引原图被 `/sites/default/files/` 中 `default` 误判占位的根因
- 唐德钱 198,358 bytes GIF 原始字节已收录，SHA-256 与尺寸闭环
- 唐德钱底表两列已回填并移除占位失败提示，三载体一致
- 唐德钱画像仅执行方案 A `+2/-0`，其余画像和保护资产零修改
- 四数已更新为 413/411/2/2，占位图 0；照片 411 张、109,087,184 bytes
- 专项 21/21、全仓 241/241、validate-full、artifact-tool import、diff check 与 fsck 通过
RequiredArtifacts:
- work/中山大学附属第五医院_photo_backfill_full_payload.json
- work/中山大学附属第五医院_photo_backfill_full_reconciliation.csv
- work/中山大学附属第五医院_photo_backfill_full_report.md
- 医生画像仓库/01_试点医院/中山大学附属第五医院/照片/唐德钱-口腔科-医师-中山大学附属第五医院.gif
- 医生画像仓库/01_试点医院/中山大学附属第五医院/唐德钱.md
- docs/architecture_decisions/2026-08-17_issue_61_sysu5_photo_backfill_trial.md
ContextInjection:
- 当前 Phase 为 FULL_READY_FOR_FINAL_OWNER_AUDIT；等待 nancywrayg57-jpg 只复核 5 项最小返修
- 自动化保持 PAUSED；不得自行合并、关闭 Issue 或领取下一 Issue
- Owner 通过后仍只等待 Owner 合并；双门禁完全满足前不得进入下一 Issue
</Handoff_State>
