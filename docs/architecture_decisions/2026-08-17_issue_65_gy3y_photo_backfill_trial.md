# Issue #65 广州医科大学附属第三医院照片补录 TRIAL + FULL

## 目标与授权

- GitHub Issue：`#65`。
- 医院：广州医科大学附属第三医院。
- 官网：<https://www.gy3y.cn/index>。
- 医生目录：<https://www.gy3y.cn/kstd/zjjs.html>。
- 关联 PR：`#66`。Owner 已于 `2026-08-17T08:45:04Z` 明确给出 TRIAL `通过` 并切换为 `FULL_APPEND_AND_OBSIDIAN`。
- `/html/images/doctor.jpg` 由 Codex 按既定占位政策自行判定，后经 owner FULL 终审实图核验成立；不得表述为管理员事前确认。该判定只适用于这一精确路径，不扩展到其他 `/html/images/*` 路径，也不改变既有小 GIF 双侧占位检测边界。
- Owner 于 `2026-08-17T11:10:48Z` 撤销固定“5+1”返修集合，授权对原 66 条“详情不可达”执行 5 轮聚合探测、轮间隔至少 60 秒，并以执行时点结果动态闭环。
- 当前本地阶段：`FULL_READY_FOR_FINAL_OWNER_AUDIT`。不得自行合并 PR、关闭 Issue 或领取下一家医院。

## 范围与站点差异

1. 固定范围为总底表中本院 422 行、422 个唯一官网医生详情 URL；FULL 前 422 行的 `照片链接`、`照片文件` 均为空。
2. 原 66 条“详情不可达”来源全部执行 5 轮探测，每轮使用新官网首页会话，相邻轮开始间隔至少 60 秒；每条每轮保留原始 HTTP 跳转链与 UTC 时间戳。任一轮出现有效本人照片即当场冻结原始字节，后续轮继续探测但不得覆盖；5 轮均未采得照片时才按聚合状态归入失败三态。
3. 官网首页、医生目录和详情页当前均以 `text/plain` MIME 返回 HTML 正文。脚本只在 MIME 为 `text/html` 或 `text/plain` 且正文前 8 KiB 存在 HTML 结构标记时接受，其他内容类型或纯文本仍拒绝。
4. 页面标题允许姓名与 `_` 分隔符之间存在官网原始空白；仍要求标题姓名与目标行一致。
5. 照片只取详情页唯一 `div.photo` 容器实际引用；正文叙事图、floatcard 和公共装饰图不进入候选。图片请求携带对应详情页 Referer，不构造或探测页面未引用路径。

## 实现与事务边界

- 脚本：`work/gy3y_photo_backfill_trial.py`。
- 专项测试：`work/tests/test_gy3y_photo_backfill_trial.py`。
- 来源基线：从 Issue #63 的 TRIAL-only 提交 `1e1fbfc27db1051a59be44abeea55369870aea88` 最小适配；在 owner FULL 授权后移植同类事务能力，但删除 Issue #63 的入口台账写入逻辑。
- 脚本保留 `--trial-only`、`--mark-visual-pass`、`--validate`，并增加 `--full`、`--validate-full`。
- 来源 URL 只接受 `gy3y.cn/ks/.../doctor_<数字ID>.html`；照片 URL 只接受唯一 `div.photo` 容器实际引用、同域、无查询参数的授权路径。`/html/images/doctor.jpg` 按既定政策和 owner 事后核验精确归类为占位图。
- 占位检测沿用双侧边界：仅对小于 40 KiB 的 GIF 按 `nopic/noimage/placeholder` 路径标记或低色板且浅灰中性像素占比至少 70% 判定；不得单凭 GIF 格式判占位。
- 每张实图核验 HTTP、原始字节、SHA-256、魔数、扩展名和尺寸；原始响应字节直接落盘，不压缩。
- FULL 仅允许目标 422 行的 `照片链接`、`照片文件`、`异常提示` 三列变化；失败行照片字段留空，异常提示追加式且幂等。
- 画像仅在实采成功的既有 `<!-- AUTO-GENERATED -->` 画像基础信息区新增单行照片引用；失败来源零触碰，不新建画像，不修改 `_索引.md`。
- XLSX 继续使用现有 `collector.build_workbook` → `@oai/artifact-tool` 写入链，不使用 openpyxl、COM、LibreOffice 或手工 OOXML 替代。
- FULL 落盘后，范围稳定性测试使用显式只读模式读取已回填底表；生产 TRIAL/FULL 前置门禁仍默认拒绝已有照片字段。
- 单张大于 5 MiB 进入 owner 终审清单；单张大于 20 MiB 或异常格式立即熔断。

## 固定样本与结果

- 固定样本 10 人覆盖 10 个科室，含荔湾、黄埔两个院区；职称分层为正高 3 人、副高 3 人、其他 4 人。
- 样本：许治强、张建瑜、谭湘萍、关国晟、谭慧珍、黎经兰、詹鸿、麦伟文、马晓燕、彭天文。
- 实采 10/10；详情错误、结构不一致、无照片容器、占位图、照片错误均为 0；熔断问题 0/10。
- 页面引用路径为 `Upload原图` 10 张；第三方来源 0，页面未引用路径探测 0。
- 总字节 616,386；最小 31,518；中位数 44,252；平均 61,638；最大 175,149。
- 大小分桶：小于 200 KiB 10 张；超过 5 MiB 0 张；以样本均值估算 422 行约 24.81 MiB，该数字仅用于容量预估，不代表 FULL 实际结果。
- 联系表逐格人工视觉复核：10/10 均为对应医生的单人成人职业照；无正文叙事图、患者、儿童、合影、占位图、二维码或公共装饰图。
- TRIAL 正式受保护资产前后快照完全一致；本院正式照片目录在 TRIAL 阶段仍不存在。

## FULL 五轮聚合返修与四数闭环

- 聚合证据：原 66 条来源 × 5 轮 = 330 次详情探测；轮次开始 UTC 为 `11:32:40Z / 11:33:40Z / 11:34:40Z / 11:35:40Z / 11:36:40Z`，四个实测间隔均不少于 60 秒。每条对账证据均保留 5 个轮次标记、HTTP 跳转链和完整 UTC 时间戳。
- 动态新增实采 8 张：詹鸿 `doctor_78`（第 4 轮冻结）；苏春宏 `doctor_112`、苏志源 `doctor_224`、熊汉真 `doctor_266`、陈艳红 `doctor_343`、周咪咪 `doctor_459`、沈华伟 `doctor_460`、龙文 `doctor_461`（均第 1 轮冻结）。后续轮未覆盖已冻结字节。
- 新增 8 张逐图视觉复核均为单人成人职业照，无占位图、二维码、公共装饰图、患者、儿童或合影；身份追溯仍以标题姓名匹配且唯一 `div.photo` 引用为准，留待 owner 最终审计。
- Owner 三轮并集 7 ID 仅作对照：`12/31/190/224/266/310/326`；本次 5 轮中 `224/266` 实采，其余 5 条维持详情不可达。该对照不构成固定恢复集合门禁。
- 范围 422 = 应采 422 = 实采 356 + 失败留空 66；总问题率约 15.64%，低于 30% 熔断阈值。
- 失败三态：`详情不可达=58`、`无照片容器=0`、`占位图=8`。8 个占位项均为精确路径 `/html/images/doctor.jpg`，其占位判定已经 owner 事后核验。
- 总底表行差异 778 = `照片链接 356 + 照片文件 356 + 异常提示 66`；除授权列外无变化。
- 总底表 JSON/CSV/XLSX 三载体照片结果一致；正式照片文件 356，与对账工件和成功行一一对应。
- 画像完整性：既有画像 422、修改 356、未修改 66、缺失 0、新建 0；`_索引.md` 未修改。
- 既有 348 张照片逐文件 SHA-256 保持不变；原占位 8 行、聚合后仍失败 58 行及其画像零触碰。第三方来源访问 0、页面未引用路径探测 0、超过 20 MiB 0。

## 照片规模与大图终审清单

- 照片总数 356，总字节 79,081,002（约 75.42 MiB），全部为页面实际引用的 `Upload原图`。
- 大小分布：`<200KiB=275`、`200KiB-1MiB=65`、`1-5MiB=15`、`5-20MiB=1`。
- 唯一超过 5 MiB 的照片：黎燕霞，6,055,447 bytes，2208×2944 PNG；页面引用 URL：<https://www.gy3y.cn/Upload/202412/638708193728200798.png>；SHA-256：`04cf3c45d6a0955142adc3c7a9221a4dcd85363e4b902eabab4e3e454a3c2d1a`。

## 受保护资产

FULL 前后以下资产哈希保持不变：

- 总底表更新报告：`cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a`。
- 入口台账 JSON：`a82957b29a78551c50cb443fe75e8784a80a93d7e3c8fa7359490addb6a667ae`。
- 入口台账 CSV：`8219d8eeb3fb085cfac5595ecf97cc4a487525312ea38dbaa41ae702e91c0bf9`。
- 入口台账 XLSX：`04273e1500e8dcb2483280fd53ed775543f0159531eca6f247a5bdf3a70a8911`。

## 工件

- `work/广州医科大学附属第三医院_photo_backfill_trial_payload.json`
- `work/广州医科大学附属第三医院_photo_backfill_trial_manifest.csv`
- `work/广州医科大学附属第三医院_photo_backfill_trial_report.md`
- `work/广州医科大学附属第三医院_photo_backfill_trial_contact_sheet.jpg`
- `work/广州医科大学附属第三医院_photo_backfill_trial_photos/`
- `work/广州医科大学附属第三医院_photo_backfill_full_payload.json`
- `work/广州医科大学附属第三医院_photo_backfill_full_reconciliation.csv`
- `work/广州医科大学附属第三医院_photo_backfill_full_report.md`
- `医生画像仓库/01_试点医院/广州医科大学附属第三医院/照片/`
- 总底表 payload/CSV/XLSX 与 348 份既有医生画像的照片块最小更新。

## 验证与停止点

- `python -m py_compile work/gy3y_photo_backfill_trial.py work/tests/test_gy3y_photo_backfill_trial.py`：通过。
- 专项测试 `python -m unittest work.tests.test_gy3y_photo_backfill_trial -v`：23/23 通过，覆盖 5 轮全来源探测、首次有效照片冻结、后续轮不覆盖、原始 302 跳转码保留和 66×5 证据验证。
- 仓库外既有临时依赖目录完成最小 import 探针后，全仓测试 `python -m unittest discover -s work/tests -p 'test_*.py'`：282/282 通过；未安装全局依赖、未修改系统 PATH 或仓库依赖配置。
- TRIAL `--validate`：通过；FULL `--validate-full`：通过。
- 联系表已固化 `PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。
- XLSX 已通过 `@oai/artifact-tool` 导入、公式错误扫描和六工作表渲染检查；6 个工作表齐全，公式错误命中 0，视觉复核无严重布局缺陷。
- 下一步仅允许把 FULL 结果提交到原 Issue #65 分支并更新 PR #66，评论 `FULL_READY_FOR_FINAL_OWNER_AUDIT` 后停止等待 `nancywrayg57-jpg` 最终审计。
