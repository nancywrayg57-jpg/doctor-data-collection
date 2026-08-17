# Issue #67 广州市中医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：`#67`。
- 医院：广州市中医院。
- 官网：<https://www.gzszyy.com/>。
- 医生目录：<https://www.gzszyy.com/expert/>。
- Phase：`TRIAL`；只允许 10 人照片试采，正式资产保持零修改。
- 工作分支：`codex/mhrj/issue-67-gzszyy-photo-backfill-trial`，基线为 Issue #65 合并后的 `origin/main` 提交 `fc845a26993d555150b52a3c67b9dea12a2b5217`。
- 当前阶段：`TRIAL_READY_FOR_OWNER_AUDIT`。未取得关联 PR 中 `nancywrayg57-jpg` 明确审计通过并切换为 `FULL_APPEND_AND_OBSIDIAN` 前，不得执行 415 行正式回填、正式照片写入或画像刷新。

## 范围与来源边界

1. 总底表中本院固定范围为 415 行、415 个唯一官网详情 URL；TRIAL 前 415 行的 `照片链接`、`照片文件` 均为空。
2. 详情来源仅接受 `https://www.gzszyy.com/expert/<年份>/<ID>.html`，并要求详情 `h1` 姓名与目标行一致。
3. 照片只取 `.doctor-resume div.doctor-img` 唯一 `img[src]` 的页面实际引用；只接受医院页面引用的 `https://oss.gzszyy.com/<YYYYMMDD>/<数字>.<格式>`。
4. 图片请求携带对应详情页 Referer；不构造、猜测或探测页面未引用路径。
5. `div.qr-img` 院区预约二维码、`static.gzszyy.com/images/` 装饰/资质/社交图标及空 `src` 不进入候选。
6. 占位检测沿用小 GIF 双侧边界；不得单凭格式或尺寸判占位。单图超过 5 MiB 进入 owner 终审清单，超过 20 MiB 或魔数异常立即熔断。

## 实现

- 新增 TRIAL 脚本：`work/gzszyy_photo_backfill_trial.py`。
- 新增专项测试：`work/tests/test_gzszyy_photo_backfill_trial.py`。
- 脚本使用标准库 Cookie 会话、重定向留痕、显式 HTTP 状态与 Content-Type 检查；照片核验覆盖原始字节、SHA-256、魔数、扩展名和尺寸。
- 脚本只提供 `--trial-only`、`--mark-visual-pass`、`--validate`，本阶段不提供 FULL 写入入口。
- 联系表只使用 TRIAL 独立目录中的原始响应字节生成，不写正式照片目录。

## 固定样本与结果

- 固定 10 人覆盖 10 个科室首原子，职称分层为正高 3 人、副高 3 人、其他 4 人。
- 样本：叶穗林、吴薏婷、林少贞、陈庆强、欧阳智、周艳利、夏思、赵鸿、金华伟、陈燕珊。
- 详情实采 10/10、照片实采 10/10；详情错误、无照片容器、占位图、照片错误和熔断问题均为 0。
- 10 张均为详情 `doctor-img` 实际引用的医院 OSS 原图；第三方来源 0、二维码/装饰图混入 0、页面未引用路径探测 0。
- 总字节 2,114,508；最小 19,404；中位数 224,293；平均 211,451；最大 279,273。
- 大小分桶：小于 200 KiB 2 张、200 KiB 至 1 MiB 8 张、1 至 5 MiB 0 张、5 至 20 MiB 0 张；以样本均值估算 415 行约 83.69 MiB，该值只用于容量估算。
- 联系表逐格视觉复核：10/10 均为单人成人职业照，无占位图、二维码、公共装饰图、患者、儿童或合影；payload 已固化 `PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。

## 正式资产保护

- TRIAL 前后入口台账 JSON/CSV/XLSX、总底表 payload/CSV/XLSX、总底表更新报告、画像 Markdown 聚合快照和正式照片目录快照一致。
- 本院画像为 415 份医生画像加 `_索引.md`，共 416 个 Markdown；均保留 `<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->` 标记，TRIAL 前零图片引用。
- 本院正式照片目录在 TRIAL 前后均不存在。

## 工件

- `work/广州市中医院_photo_backfill_trial_payload.json`
- `work/广州市中医院_photo_backfill_trial_manifest.csv`
- `work/广州市中医院_photo_backfill_trial_report.md`
- `work/广州市中医院_photo_backfill_trial_contact_sheet.jpg`
- `work/广州市中医院_photo_backfill_trial_photos/`

## 验证与停止点

- `py_compile`：通过。
- 专项测试：11/11 通过。
- 全仓测试：293/293 通过；仅通过仓库外临时 `PYTHONPATH` 提供既有测试所需的 `requests` 与 `beautifulsoup4`，未修改全局 Python、系统 PATH 或仓库依赖配置。
- TRIAL `--validate`：通过。
- 下一步只允许提交并更新 Issue #67 对应 PR，回报 `TRIAL_READY_FOR_OWNER_AUDIT` 后停止等待 owner 审计。
