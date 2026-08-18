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
