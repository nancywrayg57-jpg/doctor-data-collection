# Issue #65 广州医科大学附属第三医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：`#65`。
- 医院：广州医科大学附属第三医院。
- 官网：<https://www.gy3y.cn/index>。
- 医生目录：<https://www.gy3y.cn/kstd/zjjs.html>。
- 当前阶段：`TRIAL_READY_FOR_OWNER_AUDIT`。
- 本阶段只允许固定 10 人跨科室、跨职称照片试采；入口台账、总底表 payload/CSV/XLSX、更新报告、正式照片目录、422 份医生画像和 `_索引.md` 必须零修改。
- 未取得当前关联 PR 中 owner 明确 `通过` / `有条件通过` 且切换为 `FULL_APPEND_AND_OBSIDIAN` 前，禁止正式回填、正式照片写入、画像嵌入或入口台账改写。

## 范围与站点差异

1. 统一总底表中本院范围为 422 行、422 个唯一官网医生详情 URL；422 行的 `照片链接`、`照片文件` 均为空。
2. Owner 预核验的已知不可达范围项为李文杰 `doctor_6`；固定 TRIAL 样本不包含该项，本轮未重试、未绕过，也未据此构造照片路径。
3. 官网首页、医生目录和详情页当前均以 `text/plain` MIME 返回 HTML 正文。脚本只在 MIME 为 `text/html` 或 `text/plain` 且正文前 8 KiB 存在 HTML 结构标记时接受，其他内容类型或纯文本仍拒绝。
4. 候选预检中发现部分旧详情 URL 跳转站内 `404.html`，均在固化样本前剔除；最终 10 个固定样本全部直达各自详情页、标题与姓名/医院一致，并各有唯一 `div.photo img`。
5. 照片只取详情页 `div.photo` 容器实际引用；正文叙事图、floatcard 和公共装饰图不进入候选。图片请求携带对应详情页 Referer，不构造或探测页面未引用路径。

## TRIAL 实现边界

- 脚本：`work/gy3y_photo_backfill_trial.py`。
- 专项测试：`work/tests/test_gy3y_photo_backfill_trial.py`。
- 来源基线：从 Issue #63 的 TRIAL-only 提交 `1e1fbfc27db1051a59be44abeea55369870aea88` 最小适配；没有复制其后续 FULL 能力。
- 脚本只提供 `--trial-only`、`--mark-visual-pass` 和 `--validate`，没有 FULL 写入路径。
- 来源 URL 只接受 `gy3y.cn/ks/.../doctor_<数字ID>.html`；照片 URL 只接受唯一 `div.photo` 容器实际引用、同域、无查询参数的授权路径。
- 占位检测沿用双侧边界：仅对小于 40 KiB 的 GIF 按 `nopic/noimage/placeholder` 路径标记或低色板且浅灰中性像素占比至少 70% 判定；不得单凭 GIF 格式判占位。
- 每张实图核验 HTTP、原始字节、SHA-256、魔数、扩展名和尺寸；原始响应字节直接落盘，不压缩。
- TRIAL 前后对入口台账、总底表 payload/CSV/XLSX、更新报告、本院画像 Markdown 树和正式照片目录做哈希/树快照比对。
- 单张大于 5 MiB 只进入 owner 后续 FULL 审计清单；单张大于 20 MiB 或异常格式立即熔断。本轮均未命中。

## 固定样本与结果

- 固定样本 10 人覆盖 10 个科室，含荔湾、黄埔两个院区；职称分层为正高 3 人、副高 3 人、其他 4 人。
- 样本：许治强、张建瑜、谭湘萍、关国晟、谭慧珍、黎经兰、詹鸿、麦伟文、马晓燕、彭天文。
- 实采 10/10；详情错误、结构不一致、无照片容器、占位图、照片错误均为 0；熔断问题 0/10。
- 页面引用路径为 `Upload原图` 10 张；第三方来源 0，页面未引用路径探测 0。
- 总字节 616,386；最小 31,518；中位数 44,252；平均 61,638；最大 175,149。
- 大小分桶：小于 200 KiB 10 张；超过 5 MiB 0 张；以样本均值估算 422 行约 24.81 MiB，该数字仅用于容量预估，不代表 FULL 实际结果。
- 联系表逐格人工视觉复核：10/10 均为对应医生的单人成人职业照；无正文叙事图、患者、儿童、合影、占位图、二维码或公共装饰图。
- 正式受保护资产前后快照完全一致；本院正式照片目录仍不存在。

## 工件

- `work/广州医科大学附属第三医院_photo_backfill_trial_payload.json`
- `work/广州医科大学附属第三医院_photo_backfill_trial_manifest.csv`
- `work/广州医科大学附属第三医院_photo_backfill_trial_report.md`
- `work/广州医科大学附属第三医院_photo_backfill_trial_contact_sheet.jpg`
- `work/广州医科大学附属第三医院_photo_backfill_trial_photos/`

## 验证与停止点

- `python -m py_compile work/gy3y_photo_backfill_trial.py work/tests/test_gy3y_photo_backfill_trial.py`：通过。
- 专项测试 `python -m unittest work.tests.test_gy3y_photo_backfill_trial -v`：12/12 通过。
- 仓库外既有临时依赖目录完成 `requests/bs4/openpyxl/PIL` 最小 import 探针后，全仓测试 `python -m unittest discover -s work/tests -p 'test_*.py'`：271/271 通过；未安装全局依赖、未修改系统 PATH 或仓库依赖配置。
- `python work/gy3y_photo_backfill_trial.py --validate`：通过。
- 联系表已固化 `PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。
- 当前只允许提交 TRIAL 工件并创建同一 Issue #65 的 developer PR，随后等待 `nancywrayg57-jpg` 审计。
- Owner 未明确切换为 `FULL_APPEND_AND_OBSIDIAN` 前，不得写入总底表、正式照片目录或画像，不得自行合并、关闭 Issue 或领取下一任务。
