# Issue #61 中山大学附属第五医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：`#61`。
- 医院：中山大学附属第五医院。
- 官网：<https://www.sysu5.cn/>。
- 医生目录：<https://www.sysu5.cn/medical-service/department-expert/doctor/category?category_target_id=All&combine=>。
- 当前阶段：`TRIAL_READY_FOR_OWNER_AUDIT`。
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
- `work/sysu5_photo_backfill_trial.py` 已增加 `--full` 与 `--validate-full`：413 行全量、失败三态、30% 总问题熔断、单张超过 5 MiB 立即停止、payload/CSV/XLSX 三载体逐值验证、照片逐图字节/SHA-256/魔数/尺寸验证、方案 A 画像字节级最小插入和事务回滚。
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

## 当前停止点

保持自动化 `PAUSED`，停止在单张照片超过 5 MiB 的 Owner 裁决门禁。取得当前 PR 中 Owner 明确裁决前，不得再次执行 FULL、不得压缩或跳过该图片、不得合并 PR、关闭 Issue或处理下一 Issue。

<Handoff_State>
Target: Issue #61 中山大学附属第五医院照片补录 FULL 大图裁决
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/61
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/62
Branch: codex/mhrj/issue-61-sysu5-photo-backfill-trial
Completed:
- 413 行范围与照片空字段门禁通过
- 10 人跨 10 科室、正高/副高/其他分层 TRIAL 完成
- 10/10 页面引用派生图下载与三重核验完成
- 联系表人工视觉核验通过
- Owner 已明确 TRIAL 通过并切换 FULL_APPEND_AND_OBSIDIAN
- FULL 事务化实现、方案 A 字节级保护与裁决单已完成；专项 17/17、全量 237/237
- FULL 首次执行命中 6,649,475 bytes 页面引用派生图，按 >5 MiB 门禁停止
- 正式资产零修改，未生成 FULL 工件
RequiredArtifacts:
- docs/中山五院照片嵌入方式裁决单.md
- work/sysu5_photo_backfill_trial.py
- work/tests/test_sysu5_photo_backfill_trial.py
ContextInjection:
- 阻塞 URL：https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-07/20240208173237537.jpg?itok=RSFCQ8E7
- 阻塞字节：6,649,475；超过 Owner 5 MiB 上限
- 只能等待 Owner 对该大图给出明确裁决；不得自行压缩、跳过或重跑 FULL
</Handoff_State>
