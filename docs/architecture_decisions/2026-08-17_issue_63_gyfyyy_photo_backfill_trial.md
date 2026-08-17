# Issue #63 广州医科大学附属第一医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：`#63`。
- 医院：广州医科大学附属第一医院。
- 官网：<https://www.gyfyyy.cn/>。
- 医生目录：<https://www.gyfyyy.cn/cn/ylfw/czcx/>。
- 当前阶段：`TRIAL_READY_FOR_OWNER_AUDIT`。
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
