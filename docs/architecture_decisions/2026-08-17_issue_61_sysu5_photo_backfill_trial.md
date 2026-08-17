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

## 裁决依据缺口

Issue 正文引用的 `docs/中山五院照片嵌入方式裁决单.md` 在本次 `origin/main` 基线中不存在。Issue 正文已完整写明方案 A，但 TRIAL 不修改画像，因此本阶段可以完成；在 FULL 前应由 owner 确保该裁决依据可追溯。若后续授权 FULL，仍只能按当前 Issue/PR 的明确指令执行，不得仅凭本 ADR 推进。

## 验证

- `python -m py_compile work/sysu5_photo_backfill_trial.py work/tests/test_sysu5_photo_backfill_trial.py`
- `python -m unittest work.tests.test_sysu5_photo_backfill_trial -v`：11/11 通过。
- 通过仓库外既有临时依赖目录做 `requests/bs4/openpyxl` 导入探针后，`python -m unittest discover -s work/tests -p 'test_*.py' -v`：231/231 通过；未安装全局依赖、未修改系统 PATH 或仓库依赖配置。
- `python work/sysu5_photo_backfill_trial.py --validate`：通过。
- 联系表已使用原始分辨率视图人工核验并固化 `MANUAL_CONTACT_SHEET_REVIEW_PASSED`。
- 工件逐图字节/SHA-256 闭环、正式资产前后快照、`git diff --check` 与 `git fsck --no-progress` 均通过；`git fsck` 仅报告仓库既有 dangling 对象，无对象损坏。

## 当前停止点

提交并创建关联 Issue #61 的 PR 后，停止在 owner TRIAL 审计门禁。不得自行进入 FULL，不得合并 PR、关闭 Issue或处理下一 Issue。

<Handoff_State>
Target: Issue #61 中山大学附属第五医院照片补录 TRIAL 审计
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/61
Branch: codex/mhrj/issue-61-sysu5-photo-backfill-trial
Completed:
- 413 行范围与照片空字段门禁通过
- 10 人跨 10 科室、正高/副高/其他分层 TRIAL 完成
- 10/10 页面引用派生图下载与三重核验完成
- 联系表人工视觉核验通过
- 正式资产前后快照一致
RequiredArtifacts:
- work/中山大学附属第五医院_photo_backfill_trial_payload.json
- work/中山大学附属第五医院_photo_backfill_trial_manifest.csv
- work/中山大学附属第五医院_photo_backfill_trial_report.md
- work/中山大学附属第五医院_photo_backfill_trial_contact_sheet.jpg
- work/中山大学附属第五医院_photo_backfill_trial_photos/
ContextInjection:
- 当前只能审计 TRIAL；owner 未明确切换 FULL_APPEND_AND_OBSIDIAN 前禁止正式写入
- Issue 引用的 docs/中山五院照片嵌入方式裁决单.md 在基线缺失，FULL 前需确保裁决依据可追溯
</Handoff_State>
