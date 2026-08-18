# Issue #73 广东省第二中医院照片补录 TRIAL 与 FULL

## 目标与授权

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/73>。
- Pull Request：<https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/74>。
- 医院：广东省第二中医院。
- 官网：<https://www.gdzy5413.com/>。
- 医生目录：<https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850>。
- Phase：`TRIAL`；正式资产必须零修改。
- 工作分支：`codex/mhrj/issue-73-gdzy-photo-backfill-trial`，基线提交 `ab424b3c6504a5803232c5586d77c69164255ce4`。
- 领取记录：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/73#issuecomment-5330369655>。
- Issue 固定工作集为总底表本院 342 条既有官网详情 URL，其中 `ksdoctorinfo.aspx` 321 条、`specialist.aspx` 21 条；TRIAL 前 `照片链接`、`照片文件` 均为空。

## 官网可达性与两类模板结构诊断

Owner 侧预核验受 WAF/TLS 阻断，但 Codex 执行现场使用 Issue 明确允许的常规浏览器 UA 后，两类官方详情模板均直接 HTTP 200；未绕过 WAF、登录、验证码、权限或反爬机制。

1. `specialist.aspx?typeid=N`：本人照位于 `.main_left_img`，页面姓名为 `.docimg_title`，照片由相邻 `div` 的内联 `background:url(/UploadFiles/image/<file>)` 引用。
2. `ksdoctorinfo.aspx?...&id=N`：本人照位于基本资料卡的 `div[style*="width: 120px"]`，唯一 `img[width="120px"][height="155px"]` 的 `src` 为页面引用版本；空值 `/UploadFiles/image/` 明确代表无照片文件，不得构造路径。

TRIAL report 与 payload 分别固化了两类模板的现场 HTML 片段、容器选择器、URL 特征和代表详情 URL。

## 排除清单与响应验证

只接受上述本人照片容器实际引用的、最终 host 仍为 `gdzy5413.com` 的 `/UploadFiles/image/<file>` 响应。以下资源一律排除且下载数为 0：

1. `/style/images/` 下的模板 logo、边框、按钮、排班图和装饰图。
2. 固定就诊指南、专家目录、页脚、二维码及事业单位标识等公共图片。
3. 空路径 `/UploadFiles/image/`。
4. 文件名含 `default`、`placeholder`、`nopic`、`noimage` 等占位特征的资源。
5. 不在授权医生照片容器内的其他 `img` 或 CSS background 引用。

照片响应继续执行 HTTP、Content-Type、魔数、SHA-256、Pillow 解码尺寸和 20 MiB 熔断验证；原始响应字节不压缩、不转码。

## 一次视觉失败与最小修正

首轮 TRIAL 的联系表发现李雪真页面引用文件实际为浅蓝色“暂无图片”占位图：JPEG、86×126、1,622 bytes、SHA-256 `636b19e12d195b9da003dbbed0c68c0004864d6d86e990f8b606aa069b67b5a9`。黄映飞的不同页面引用 URL 返回相同字节和相同 SHA-256。

根因是首版只按 URL/文件名特征识别占位图，而该站把“暂无图片”保存为正常命名、HTTP 200、`image/jpeg` 且魔数有效的文件。

最小修正：

1. 新增响应内容级占位门禁：已知占位 SHA-256，或不大于 4 KiB 且尺寸不大于 120×160 的小型候选响应均拒绝作为职业照。
2. 固定样本将李雪真替换为同属“其他”职称层且科室首原子不冲突的孙正平；其页面引用照片为 178×160、72,684 bytes 的单人职业照。
3. 删除范围严格限定为首轮无效 TRIAL 的 4 个工件文件、10 张临时照片及其空目录；总底表、台账、正式画像、`_索引.md` 和正式照片目录未触碰。
4. 修正后第二次 TRIAL 成功；未触发连续两次失败熔断。

## TRIAL 结果

- 固定样本：10 张 = `specialist` 2 + `ksdoctorinfo` 8。
- 科室首原子：10 个不同值，分别为心血管科、针灸康复科五区、治未病(健康体检)中心、儿科、医技科、呼吸与危重症医学科、外一科、检验科、肿瘤科、眼科。
- 职称分层：正高 4、副高 2、其他 4；其他层包含主治中医师、主管技师和医师。
- 详情页：10/10 HTTP 200；照片：10/10 HTTP 200；最终 host 均为官网。
- 照片总字节 447,861；最小 11,443、中位数 27,839、平均 44,786、最大 164,184；10 张均小于 200 KiB，超过 5 MiB / 20 MiB 均为 0。
- 按实际魔数落盘 JPEG 3 张、PNG 7 张；其中 6 张 PNG 被旧站响应头误报为 `image/jpeg`，扩展名严格跟随实际魔数而非 URL 后缀或响应头。每张均保存页面实际引用版本的原始响应字节。
- 联系表目视复核：10/10 均为单人成人职业照，无占位图、二维码、公共装饰、患者、儿童或合影；payload 已记录 `PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。
- 页面未引用路径构造/探测 0、第三方来源 0、排除资源下载 0。

## 正式资产保护

- 入口台账 JSON/CSV/XLSX、总底表 JSON/CSV/XLSX、总底表更新报告、343 文件本院画像树和不存在的正式照片目录在 TRIAL 前后哈希/字节快照完全一致。
- 342 份医生画像均保留 AUTO 标记；`_索引.md` 存在且未修改。
- TRIAL 只写 `work/` 工件；未回填底表、未刷新画像、未创建正式照片目录。

## 工件

- `work/gdzy5413_photo_backfill_trial.py`
- `work/tests/test_gdzy5413_photo_backfill_trial.py`
- `work/广东省第二中医院_photo_backfill_trial_payload.json`
- `work/广东省第二中医院_photo_backfill_trial_manifest.csv`
- `work/广东省第二中医院_photo_backfill_trial_report.md`
- `work/广东省第二中医院_photo_backfill_trial_contact_sheet.jpg`
- `work/广东省第二中医院_photo_backfill_trial_photos/`（10 张）

## 验证与停止点

- `py_compile`：通过。
- Issue #73 专项测试：13/13 通过。
- 全仓 `unittest discover`：352/352 通过；使用仓库此前验证过的本机 Python 运行时及其 `requests 2.34.2`、`beautifulsoup4 4.15.0`、`openpyxl 3.1.5`、`Pillow 12.2.0`，未安装依赖或修改系统 PATH/仓库依赖配置。
- `--validate`：`TRIAL_VALIDATED`，10 张照片与 manifest/payload/report/结构诊断/正式资产快照闭环。
- 独立重下靳利利（specialist）和孙正平（ksdoctorinfo）两类代表照片：均 HTTP 200，字节数和 SHA-256 与工件完全一致。
- 当前停止点：`TRIAL_READY_FOR_OWNER_AUDIT`。提交、推送并创建关联 Issue #73 的 PR 后等待 owner 审计；未取得 owner 明确 `FULL_APPEND_AND_OBSIDIAN` 前不得写正式资产。

<Handoff_State>
Target: Issue #73 广东省第二中医院照片补录 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/73
Branch: codex/mhrj/issue-73-gdzy-photo-backfill-trial
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/74
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 完成两类详情模板结构诊断及 HTML 片段固化
- 完成 10 科室、正高 4 + 副高 2 + 其他 4 的 10 张页面引用原始响应照片
- 增加响应内容级占位图门禁，排除合法 JPEG 伪装的“暂无图片”
- 完成 manifest/payload/report/联系表和正式资产零修改验证
CurrentFacts:
- 固定范围 342 = ksdoctorinfo 321 + specialist 21；TRIAL 前照片字段全空
- TRIAL 照片 10 张，总字节 447,861；详情/照片均 10/10 HTTP 200
- 本院画像 343 文件；正式照片目录仍不存在；总底表和台账三载体未变化
Next:
- 完成全仓测试、提交、标准 Git 协议 fast-forward 推送并创建关联 Issue #73 的 PR
- 等待 owner TRIAL 审计；仅 owner 明确下发 FULL_APPEND_AND_OBSIDIAN 后才可写正式资产
Constraints:
- 只采两类本人照片容器实际引用的 /UploadFiles/image/<file> 原始响应字节
- 禁止构造页面未引用路径、下载公共/装饰/占位资源或使用第三方来源
- 自动化在 TRIAL 成功提交、推送并进入等待 owner 审计后恢复 ACTIVE
Artifacts:
- work/广东省第二中医院_photo_backfill_trial_payload.json
- work/广东省第二中医院_photo_backfill_trial_manifest.csv
- work/广东省第二中医院_photo_backfill_trial_report.md
- work/广东省第二中医院_photo_backfill_trial_contact_sheet.jpg
- work/广东省第二中医院_photo_backfill_trial_photos/
</Handoff_State>

## FULL 授权与熔断恢复

- Owner 在 PR #74 评论明确给出 `TRIAL_AUDIT_PASSED → FULL_APPEND_AND_OBSIDIAN`：<https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/74#issuecomment-5330738867>。
- 首次 FULL 临时事务在 `specialist` 页面发现官网姓名 `汪 何`、底表姓名 `汪何` 的 Unicode 空白差异；正式照片目录、总底表和画像均未安装。
- 最小修正首次回归仍被下游 TRIAL 解析器的严格姓名比较拒绝，按 `Agent.md` 连续两次失败门禁熔断。管理员随后在当前任务会话明确授权解除熔断。
- 恢复后的唯一修正是：先对官网姓名与底表姓名执行“只忽略 Unicode 空白”的一致性校验；校验通过后，把官网原始姓名传给既有模板解析器。没有放宽不同姓名、不同容器或不同来源的门禁；新增 `汪 何` / `汪何` 回归测试后专项 25/25 通过。

## 状态波动与 5 轮聚合

- FULL 在于锋详情页首次观察到 `2026-08-18T18:03:05Z HTTP 502 → 2026-08-18T18:03:35Z HTTP 200`，立即按 Owner 规则暂停，正式资产未安装。
- 页面当前实际引用照片为 `https://www.gdzy5413.com/UploadFiles/image/2014-4/20140430100008988.jpg`。
- 5 轮聚合从 `2026-08-18T18:04:27Z` 到 `18:08:27Z`，相邻轮次单调间隔均为 60 秒；5 轮首页和详情均 HTTP 200。
- 第 1 轮冻结页面引用原图：JPEG、422×544、38,916 bytes、SHA-256 `0047ae5e371040cc6bf8c97dc204608988ec2acf8ac669be77f96322be54855b`；后续 4 轮不覆盖。聚合 JSON 与冻结照片均进入 FULL payload 验证链。

## FULL 结果

- 四数闭环：固定目标 342 = 实采 305 + 失败留空 37；正式照片目录落盘 305；TRIAL 复用 10，FULL 新抓取成功 295，聚合冻结复用 1。
- 失败四类：详情不可达 0、照片资源不可达 0、无照片容器 30、占位图 7。30 条无照片容器均为 120×155 资料卡实际引用 `/UploadFiles/image/` 空目录；7 条占位图均保留资源 URL、引用数和内容判定特征。
- 占位图中 6 条为已知 1,622-byte、86×126 JPEG，SHA-256 `636b19e12d195b9da003dbbed0c68c0004864d6d86e990f8b606aa069b67b5a9`；李有武为另一张 1,320-byte、86×126 小型占位响应，由 `<=4 KiB + 小尺寸` 门禁拒绝。
- 原始响应总字节 8,364,320；最大 171,348 bytes；>5 MiB 0、>20 MiB 0。按实际魔数落盘 JPEG 42、PNG 263；详情模板分布 `specialist` 21、`ksdoctorinfo` 284。
- 总底表只发生 647 个允许的单元格变化：`照片链接` 305、`照片文件` 305、`异常提示` 37；payload/CSV/XLSX 9,222 行逐值一致。
- 305 份 AUTO 画像严格 +2/-0；37 份失败画像零触碰；画像文件集合不变，`_索引.md` SHA-256 不变。
- FULL manifest 对 305 张逐一重算字节数、SHA-256、魔数/扩展名与尺寸，照片目录零孤儿、零缺失。
- 抽样拼图覆盖最小、最大和 8 个确定性随机样本；目视复核 10/10 为单人成人职业照，未见占位图、二维码、公共装饰、患者、儿童或合影。

## FULL 工件与验证

- `work/gdzy5413_photo_backfill_full.py`
- `work/tests/test_gdzy5413_photo_backfill_full.py`
- `work/广东省第二中医院_photo_backfill_full_payload.json`
- `work/广东省第二中医院_photo_backfill_full_reconciliation.csv`
- `work/广东省第二中医院_photo_backfill_full_report.md`
- `work/广东省第二中医院_photo_backfill_full_audit_sheet.jpg`
- `work/广东省第二中医院_photo_backfill_full_flicker_probe.json`
- `work/广东省第二中医院_photo_backfill_full_flicker_probe_photo.bin`
- `医生画像仓库/01_试点医院/广东省第二中医院/照片/`（305 张）
- `--validate-full`：`FULL_VALIDATED`，305 实采、37 失败。
- `py_compile`：通过；Issue #73 TRIAL+FULL 专项测试 25/25；全仓 `unittest discover` 364/364 通过。
- 使用既有本机 Python 运行时及进程级依赖路径；现场版本 `requests 2.34.2`、`beautifulsoup4 4.15.0`、`openpyxl 3.1.5`、`Pillow 12.3.0`。未安装依赖、未修改系统 PATH 或仓库依赖配置。

<Handoff_State>
Target: Issue #73 广东省第二中医院照片补录 FULL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/73
Branch: codex/mhrj/issue-73-gdzy-photo-backfill-trial
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/74
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: FULL_READY_FOR_FINAL_OWNER_AUDIT
Completed:
- 342 条固定范围完成 305 实采 + 37 失败留空四数闭环
- 305 张页面引用原始响应照片完成 manifest 三重复算与正式落盘
- 305 份 AUTO 画像严格 +2/-0；37 份失败画像与 _索引.md 零触碰
- 于锋状态波动完成 5 轮 60 秒聚合并冻结首轮原图
- FULL_VALIDATED、专项 25/25、全仓 364/364、抽样拼图 10/10 目视通过
CurrentFacts:
- 失败四类为 0 详情不可达、0 照片资源不可达、30 无照片容器、7 占位图
- 正式照片 305 张，共 8,364,320 bytes；JPEG 42 + PNG 263；>5 MiB 0
- 总底表三载体 9,222 行逐值一致；允许字段变化 647 个单元格
Next:
- 提交并以标准 Git fast-forward 推送当前分支到 PR #74
- 发布 FULL_DONE，恢复 doctor-data-single-issue-monitor，等待 owner 最终审计
Constraints:
- 不自行合并 PR，不关闭 Issue，不领取下一家医院
- 仅 Owner 最终明确审计通过、PR 合并、Issue 关闭和 CI 成功后才进入下一 Issue 检查
Artifacts:
- work/广东省第二中医院_photo_backfill_full_payload.json
- work/广东省第二中医院_photo_backfill_full_reconciliation.csv
- work/广东省第二中医院_photo_backfill_full_report.md
- work/广东省第二中医院_photo_backfill_full_audit_sheet.jpg
- 医生画像仓库/01_试点医院/广东省第二中医院/照片/
</Handoff_State>
