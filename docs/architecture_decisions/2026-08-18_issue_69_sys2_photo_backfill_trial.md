# Issue #69 中山大学孙逸仙纪念医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：`#69`。
- 医院：中山大学孙逸仙纪念医院。
- 官网：<https://www.gzsys.org.cn/>。
- 有效医生目录：<https://www.gzsys.org.cn/doctor/592/search>。
- Phase：`TRIAL`；只允许固定 10 人照片试采，正式资产保持零修改。
- 工作分支：`codex/mhrj/issue-69-sys2-photo-backfill-trial`，基线提交 `504bd416091da952b4659e7641eeccc8cb7cd513`。
- Issue 正文原目录 `/mingyi` 返回 HTTP 404；owner 于 `2026-08-18T09:38:07Z` 更正目录并明确授权以总底表该院 658 个既有官网详情 URL 为工作集继续 TRIAL。

## 范围与来源边界

1. 总底表本院固定范围为 658 行、658 个唯一官网详情 URL；TRIAL 前 `照片链接`、`照片文件` 均为空。
2. 详情来源仅接受 `https://www.gzsys.org.cn/node/<ID>` 与 `https://www.gzsys.org.cn/doctor/<ID>`，并要求页面医生姓名与目标行一致。
3. 照片只取 `.other-left .other-media .media-img[data-image-url]` 的页面实际引用。
4. 只接受官网 `/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/doctor/<文件>` 与 `/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/<文件>` 两种原图路径；不构造、猜测或探测页面未引用路径。
5. `styles/mini200`、`default_images`、院徽和 `inline-images` 公共图标、占位及装饰资源不得进入候选。
6. 使用常规 Cookie 会话、跟随重定向并携带详情页 Referer；只记录 Cookie 名称，不记录值。单图超过 5 MiB 进入 owner 终审清单，超过 20 MiB 或魔数异常立即熔断。

## 实现与诊断披露

- 新增 TRIAL 脚本：`work/sys2_photo_backfill_trial.py`。
- 新增专项测试：`work/tests/test_sys2_photo_backfill_trial.py`。
- 脚本只提供 `--trial-only`、`--mark-visual-pass`、`--validate`，本阶段无 FULL 写入入口。
- 实现前结构诊断曾用宽泛 `data-image-url` 正则，在 3 个官网详情页额外请求共 18 次页面已引用的 `styles/mini200` 公共图标；均未落盘、未进入 payload、联系表或正式资产。owner 已裁定不构成违规；正式实现已收敛到医生照片容器限定解析，回归测试固定 TRIAL 排除资源下载数为 0。

## 固定样本与结果

- 样本：宋尔卫、陈样新、詹俊、黄晓波、黎江、常瑞明、马剑达、黄泽坚、曾志芬、李卓。
- 覆盖 10 个科室首原子；职称分层为正高 3、副高 4、其他 3。
- 详情路由覆盖 `node` 5 人、`doctor` 5 人；照片路径覆盖 `doctor-subdir` 5 张、`files-root` 5 张。
- 详情成功 10/10、照片成功 10/10；详情失败、无照片容器、占位图、照片失败、状态闪烁、超过 20 MiB 和第三方来源均为 0。
- 总字节 11,933,516；最小 10,354；中位数 1,478,584；平均 1,193,351；最大 2,668,268。
- 大小分桶：小于 200 KiB 3 张、200 KiB 至 1 MiB 1 张、1 至 5 MiB 6 张、5 至 20 MiB 0 张、超过 20 MiB 0 张；按样本均值线性估算 658 行约 748.85 MiB，仅作容量估算。
- 联系表逐格视觉复核：10/10 均为单人成人职业照，无占位图、二维码、公共装饰图、患者、儿童或合影；payload 已固化 `PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。

## 正式资产保护

- TRIAL 前后入口台账、总底表 JSON/CSV/XLSX、总底表更新报告、659 个本院 Markdown 聚合快照和正式照片目录快照完全一致。
- TRIAL 只写 `work/` 工件，未回填三载体、未刷新画像、未创建正式照片目录。

## 工件

- `work/中山大学孙逸仙纪念医院_photo_backfill_trial_payload.json`
- `work/中山大学孙逸仙纪念医院_photo_backfill_trial_manifest.csv`
- `work/中山大学孙逸仙纪念医院_photo_backfill_trial_report.md`
- `work/中山大学孙逸仙纪念医院_photo_backfill_trial_contact_sheet.jpg`
- `work/中山大学孙逸仙纪念医院_photo_backfill_trial_photos/`

## 验证与停止点

- `py_compile`：通过。
- 专项测试：12/12 通过。
- 全仓测试：311/311 通过；仅复用仓库外既有 `requests 2.34.2` 与 `beautifulsoup4 4.15.0`，未安装全局依赖、未修改系统 PATH 或仓库依赖配置。
- TRIAL `--validate`：通过。
- 下一步只允许提交、推送并创建关联 Issue #69 的 PR，回报 `TRIAL_READY_FOR_OWNER_AUDIT` 后等待 owner 审计；未取得明确 `FULL_APPEND_AND_OBSIDIAN` 前不得写正式资产。

## Owner TRIAL 审计与 FULL 授权

- PR：`#70`，分支与 Issue #69 一致，TRIAL CI `governance-check` 成功。
- owner `nancywrayg57-jpg` 于 `2026-08-18T09:57:03Z` 在 PR #70 明确下发 `TRIAL_AUDIT_PASSED → FULL_APPEND_AND_OBSIDIAN`。
- FULL 固定范围为总底表本院 658 条既有官网详情 URL；复用已审计的 10 张 TRIAL 原始字节，其余 648 条实时请求。
- 正式照片、总底表 JSON/CSV/XLSX 与 658 份既有 AUTO 画像采用临时事务区生成、全量验证后一次性替换，异常时回滚。
- 画像仅在 AUTO 标记的基础信息区插入照片行加空行，成功画像严格 `+2/-0`；失败画像和 `_索引.md` 零修改。
- 失败仅允许三态：详情不可达、无照片容器、占位图。不可达保留初次请求加 2 次、间隔至少 30 秒的 HTTP/UTC 证据；发现状态闪烁立即熔断并等待 5 轮聚合协议。
- 官网页面实际引用的原图超过 5 MiB 可收录但必须单列；超过 20 MiB 或魔数/格式异常立即熔断。

## FULL 实现与执行前校验

- 新增 `work/sys2_photo_backfill_full.py` 和 `work/tests/test_sys2_photo_backfill_full.py`。
- FULL 专项测试覆盖失败提示幂等、3 次请求与两个 30 秒间隔、小 GIF 路径与视觉双侧占位判定、画像严格 `+2/-0`、文件名冲突追加详情 ID，以及最小/最大/8 个确定性随机抽样。
- `py_compile` 成功；TRIAL + FULL 专项测试 18/18 成功。
- FULL 执行前现场校验：目标行 658、唯一来源 658、既有画像 658、AUTO 画像预插入 658；总底表 JSON/CSV/XLSX 三载体 9,222 行逐值一致；正式照片目录和 FULL 工件尚不存在。

## FULL 首次执行熔断与五轮聚合

- FULL 首次执行处理至 600/648 个新目标后，万欢（`https://www.gzsys.org.cn/node/25212`）页面实际引用原图在外层第 1 次请求中连续两次传输不完整、已读 1,023,176 bytes；30 秒后第 2 次请求 HTTP 200 `image/jpeg`。该变化被判为状态闪烁并立即熔断。
- 熔断后临时事务区已清理；保护快照与 TRIAL 后一致，正式照片目录及 FULL payload/CSV/report/audit sheet 均不存在。事件已回报 PR #70。
- 按 owner FULL 指令执行 5 轮聚合：轮次开始 UTC 为 `10:42:36Z / 10:43:36Z / 10:44:36Z / 10:45:36Z / 10:46:36Z`，单调时钟间隔 `60.0 / 60.0 / 60.015 / 60.0` 秒。
- 五轮首页与详情均 HTTP 200；第 1 轮当场冻结官网原始 JPEG 1,974,546 bytes、2505×3659、SHA-256 `d3d3f78dc0150c47af3b9d8a0333177748faab36b9e07874081003edca113011`，后续四轮继续探测详情但不覆盖冻结原图。
- 聚合工件：`work/中山大学孙逸仙纪念医院_photo_backfill_full_flicker_probe.json` 与 `work/中山大学孙逸仙纪念医院_photo_backfill_full_flicker_probe_photo.bin`；FULL 续跑将校验后复用冻结原始字节。

## FULL 最终结果与本地验收

- 四数闭环：目标 658 = 实采/落盘/画像刷新 597 + 失败留空 61；其中 TRIAL 复用 10、五轮聚合冻结复用 1、其余为本轮官网实采。问题率 9.27%，低于 30% 熔断线。
- 失败三态：详情不可达 1、无照片容器 0、占位图 60。唯一详情不可达为郑眉光 `https://www.gzsys.org.cn/node/25208`，三次均 HTTP 404 并最终落到 `/core/install.php`，UTC 为 `10:51:20Z / 10:51:51Z / 10:52:21Z`。
- 照片总字节 315,236,079（300.63 MiB），最大 10,364,909；大小分桶 `<200KiB=375 / 200KiB-1MiB=108 / 1-5MiB=111 / 5-20MiB=3 / >20MiB=0`。
- 路由 `node=399 / doctor=198`；原图路径 `doctor-subdir=421 / files-root=176`；页面未引用路径探测 0、第三方来源 0。
- 3 张超过 5 MiB 的 owner 终审清单：梁安靖 10,364,909 bytes（3840×5760）、曾伟科 5,659,744 bytes（1548×2064）、梁中锟 5,530,814 bytes（2400×3600）。本地逐张视觉复核均为单人成人职业照。
- 最小/最大/8 个确定性随机抽样拼图 10/10 本地视觉复核为单人成人职业照，无占位图、二维码、装饰图、患者、儿童或合影。
- 总底表变更单元格 1,255：照片链接 597、照片文件 597、失败行异常提示 61；成功画像 597 份严格 `+2/-0`，失败画像 61 份与 `_索引.md` 零修改。
- `--validate-full` 成功；全仓测试 318/318 成功。XLSX 共 6 个工作表，公式单元格 0、公式错误 0；总底表 JSON/CSV/XLSX 三载体 9,222 行逐值一致。
- FULL 工件：payload、658 行对账 CSV、报告、抽样拼图、五轮聚合 JSON 与冻结原图；正式照片目录共 597 个原始字节文件。
