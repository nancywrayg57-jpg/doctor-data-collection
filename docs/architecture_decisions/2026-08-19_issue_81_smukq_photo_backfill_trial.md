# 2026-08-19 Issue #81 南方医科大学口腔医院（海珠广场院区）照片补录 TRIAL

## 目标与授权

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/81>。
- 医院：南方医科大学口腔医院(海珠广场院区)。
- 官网：<https://www.smukqyy.cn/>。
- 医生入口：9 个 section，分别为 341/342/343/384/385/386/431/434/504；详情固定为 `/prods/<section>/<id>`。
- Phase：`TRIAL`；固定范围为总底表本院 95 行，照片双列全空，既有异常提示保持不动。
- 工作分支：`codex/mhrj/issue-81-smukq-photo-backfill-trial`；基线 `5dac77bf19b52ea7bc00725b8f488fa577053bfb`。
- Codex 领取评论：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/81#issuecomment-5339335749>。

本轮只允许完成 `img.content_img` 容器结构诊断、10 人 TRIAL、manifest/payload/report/联系表/10 张页面引用原图、专项测试和 ADR。未取得 Owner 在关联 PR 中明确下发的 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填照片字段、创建正式照片目录或刷新画像。

## 固定范围与适配决策

- 总底表精确 95 行、95 个唯一详情 URL；照片链接和照片文件均为空。
- section 分布：341=12、342=12、343=10、384=12、385=12、386=12、431=7、434=11、504=7。
- 全院职称分类：正高 12、副高 11、中级 65、初级 6、其他 1。TRIAL 选择正高 2、副高 2、中级 3、初级 3，覆盖全部四个标准职称层和全部 9 个 section。
- 详情页唯一候选为 `<img class="content_img" src="/Uploads/Upload/...">`；姓名位于相邻 `span.content2_span1`。
- `/Home/images/`、`/Public/Home/images/` 及其他所有页面图片均排除；仅保存唯一 `img.content_img` 的 `src` 实际引用原始响应字节。
- 请求仅使用 Owner 批准的固定常规浏览器 UA、无 Cookie、无代理、无挑战绕过，不构造未引用路径。
- 工程整改从本批生效：`ROOT = Path(__file__).resolve().parents[1]`；payload/report 等只记录仓库相对路径；对外申报工件 SHA-256 以提交后的仓库 blob（LF）内容为准。

## TRIAL 执行结果

- 两轮固定浏览器 UA 可达性复测间隔超过 30 秒；首页与固定抽样详情两轮均为 HTTP 200。详情页才是采集门禁，首页仅留痕。
- 10 个详情全部 HTTP 200，唯一 `img.content_img` 容器解析成功 10/10，照片资源成功 10/10；详情失败、结构异常、无照片容器、占位图和资源失败均为 0。
- 样本覆盖全部 9 个 section；职称分层为正高 2、副高 2、中级 3、初级 3。
- 10 张页面引用原始字节共 5,192,350 bytes；PNG 3、JPEG 7；单图大于 5 MiB 和 20 MiB 均为 0，跨医生重复 SHA 组为 0。
- 陈欢的 URL 后缀/声明为 JPEG，但魔数为 PNG；张彩美资源声明为 `application/octet-stream`，魔数为 JPEG。两者均按 Owner 明示政策以魔数扩展名落盘，并在 manifest 保留声明/实际双列差异。
- 灰底深色边框联系表已逐格目视检查，10/10 均为可见单人职业照；未见患者、儿童、合影、二维码、装饰图、空白格或不可见格。视觉状态为 `PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`。

## 诊断与最小修正

1. 首次专项测试发现抽样常量误写为“梁慧珊”，而固定范围实行为“梁慧珉”。按底表唯一姓名与既定 section/初级层级修正后通过。
2. 首次 TRIAL 得到 9 张，张彩美照片因官网返回 `application/octet-stream` 被共享基座拒绝。现场响应为 HTTP 200、页面唯一容器实际引用、JPEG 魔数且 PIL 可解析；按 Issue #81 的“声明/魔数不一致按魔数落盘”条款，仅在本院适配层增加魔数优先识别，并补充回归测试。第二次 TRIAL 成功 10/10。
3. 首次全仓回归发现专项测试调用 `configure_framework()` 后泄漏共享模块状态，导致后续中山三院测试误用本院解析器。仅在测试生命周期中快照并恢复被替换模块状态；定向顺序回归 26/26、最终全仓回归 447/447 通过。

## 正式资产保护

TRIAL 前后快照一致：

- 总底表 JSON：`a71842fa134023d566df7bf8aa977f6ff8412d9c3b57d8ebbb75057d68bb46b0`。
- 总底表 CSV：`7ee9c59ac8f9d2e42dd1ed7508f4f181f9371e2e413767b62d1b8280df4289ff`。
- 总底表 XLSX：`cf9a6c20df19da719f205837daccf923cd36859cf8e84f8b434f887b2a200fa3`。
- 总底表更新报告：`cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a`。
- 本院画像树：96 个文件，聚合 SHA-256 `5958ced55c4e0cb36c0bc7e161666324578fc6f4cfae66e5677b9ce8356755b2`。
- 正式照片目录运行前后均不存在。

## 工件与验证

关键工件：

- `work/smukq_photo_backfill_trial.py`
- `work/tests/test_smukq_photo_backfill_trial.py`
- `work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_payload.json`
- `work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_manifest.csv`
- `work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_report.md`
- `work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_contact_sheet.jpg`
- `work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_photos/`（10 张原始字节）

仓库 blob（LF）内容 SHA-256：

- payload：`344f6d4894cccf65f399bb9c9538a059b25cd5fa78a6203bb4242b8519421685`。
- manifest：`adf0be3673d0ea16f6712cd3e8b4e1a0376c3fcb49cd9947a84b2884ba11e0df`。
- report：`352331a9e40e09ad267e3a857411591ebad1b978aa69053625473a6a2574ce72`。
- contact sheet：`08c7e82b510c679d587f808c8abe61de49dc5078203eaee5bf142358f665240b`。

验证结果：

- Issue #81 专项测试：10/10 通过。
- `--mark-visual-pass` 后 `--validate` 通过。
- 专项测试后接共享基座测试：26/26 通过，证明模块状态无泄漏。
- 全仓 `unittest discover`：447/447 通过。

## 当前停止点

当前为 `TRIAL_READY_FOR_OWNER_AUDIT`。只允许精确暂存、提交，以标准 Git 协议 fast-forward 推送当前分支，创建关联 Issue #81 的 PR；等待 `governance-check` 成功后发布 TRIAL 审计材料并恢复自动监控。未取得 Owner 在当前 PR 明确下发的 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填正式资产、合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #81 南方医科大学口腔医院(海珠广场院区)照片补录 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/81
Branch: codex/mhrj/issue-81-smukq-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 领取唯一 READY Issue 并从最新 origin/main 创建分支
- 完成 10 人、9 个 section、正高2/副高2/中级3/初级3 的 TRIAL 和页面引用原始字节工件
- 联系表 10/10 目视通过；四层占位门禁命中 0；正式资产零修改
- 实装仓库相对 ROOT、仓库相对工件路径和 blob LF 哈希政策
- 专项 10/10、顺序回归 26/26、全仓 447/447、TRIAL 验证通过
CurrentFacts:
- 固定范围 95 行，照片双列仍全空；本院正式照片目录不存在
- TRIAL 10 张共 5,192,350 bytes，PNG 3/JPEG 7，>5 MiB 与 >20 MiB 均为 0
- payload 视觉状态 PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS
Next:
- 精确暂存、提交并标准 fast-forward 推送当前分支，创建关联 Issue #81 的 PR
- 等待 governance-check 后发布 TRIAL_READY_FOR_OWNER_AUDIT
- 仅 Owner 在当前 PR 明确下发 FULL_APPEND_AND_OBSIDIAN 后继续
Constraints:
- TRIAL 正式资产零修改
- 仅官方公开来源；禁止 Cookie、代理、挑战绕过、构造未引用路径、第三方来源与患者素材
- 工件路径必须仓库相对；申报哈希必须按仓库 blob（LF）计算
Artifacts:
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_payload.json
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_manifest.csv
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_report.md
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_contact_sheet.jpg
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_photos/
</Handoff_State>

## FULL 恢复裁决与第三次事务

- Owner 在 PR #82 下发 [`TRIAL_AUDIT_PASSED → FULL_APPEND_AND_OBSIDIAN`](https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/82#issuecomment-5339639290)，授权固定 95 行进入 FULL。
- 前两次 FULL 临时事务分别命中“官网职称 span 与底表职称不完全一致”和联系表字体依赖缺口；两次均在安装正式资产前自动回滚，现场保护核验后按协议镜像 PR 并保持自动化暂停。
- Owner 随后以 [`OWNER_RULING → RESUME_FULL`](https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/82#issuecomment-5340078606) 解除两次熔断并裁决：姓名严格一致、唯一 `img.content_img` 和非空职称 span 为身份门禁，职称增删差异只留证；SMUKQ 薄适配层注入 `contact_sheet_font`；新增离线绘图与共享引擎 `trial.*` 静态兼容测试；离线测试通过后直接执行第三次 FULL。
- 第三次事务按执行时点重新取证并成功完成，未沿用第二次临时事务数字作为正式结果。

## FULL 实现与正式结果

- `work/smukq_photo_backfill_full.py` 提供 SMUKQ FULL 薄适配层，严格限定 `img.content_img` 与 `/Uploads/Upload/` 页面实引路径；保留标题差异证据，不修改总底表职称。
- 共享 FULL 框架新增可选 `validate_full_page_title` 钩子；未配置钩子的既有站点继续执行原严格职称一致门禁。
- 顺带治理已按 Owner 指令完成：`work/ny5y_photo_backfill_trial.py` 改为仓库相对 ROOT；NY5Y legacy Windows payload 路径在测试中按仓库相对位置解析，不修改第 13 批 payload 或正式资产。
- 正式四数对账：`95 = 95 实采 + 0 失败留空`；TRIAL 复用 10，FULL 新目标 85、下载成功 85、失败 0。
- 正式照片 95 张，共 44,595,301 bytes；JPEG 73、PNG 22；大于 5 MiB 1 张，大于 20 MiB 0；跨医生重复 SHA 组 0。
- 唯一大于 5 MiB 的廖阳阳照片为 7,191,769 bytes、3956×5120，已在全量视觉表第 4 页目视确认是可见单人医生职业照。
- 95 行总底表只更新照片链接与照片文件两列，共 190 个单元格变化；72 条本院既有异常提示均为历史采集期文本清洗留痕，未被照片补录覆盖。
- 95 份画像均严格 `+2/-0`；`_索引.md` 哈希保持不变；正式照片目录 95 个文件且与 payload 零孤儿、零缺失。

## FULL 视觉与工作簿验收

- 全量视觉联系表 4 页覆盖 95/95：第 1 至 3 页各 25 张，第 4 页 20 张；逐页未见空白格、占位图、患者、儿童、合影、二维码或装饰图。
- 视觉状态已通过 `--mark-visual-pass` 固化为 `PASSED_ALL_FULL_CONTACT_SHEETS_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`；随后 `--validate-full` 输出 `expected=95 downloaded=95 failed=0`。
- 使用 `@oai/artifact-tool` 只读导入总底表 XLSX：确认六个工作表 `自动采集底表 / 复核清单 / 科室统计 / 重点范围统计 / 医院统计 / 采集说明`，全部完成视觉渲染检查，无公式错误；该工作簿是物化值工作簿，六表未发现公式单元格。
- XLSX 目标范围为第 1995 至 2089 行，共 95 行；首、中、末代表行照片双列均正确，`医院统计` 显示医生数 95、待复核数 95、已建画像数 95。
- JSON/CSV/XLSX 均为 9,222 行；去除两个历史非本院记录内的 U+FEFF 展示字符后逐单元格一致，Issue #81 的 95 行原始值不存在载体差异。

## 保护、路径与验证闭环

- 入口台账、总底表更新报告、TRIAL payload/manifest/report/contact sheet 的字节数和 SHA-256 均与 FULL 前快照相同，Git diff 为 0；TRIAL 照片树也由 `--validate-full` 按聚合哈希复核不变。
- FULL payload/report 无绝对工作区路径，工件和画像路径均为仓库相对路径；`repository_relative_paths_only=true`，哈希政策为 `repository_blob_lf`。
- FULL payload、reconciliation、95 张照片、画像完整性清单、视觉页、三载体和受保护资产均由 `--validate-full` 复算通过。
- 最终专项顺序回归：SMUKQ TRIAL 10/10、SMUKQ FULL 15/15、NY5Y FULL 11/11，共 36/36。
- 最终全仓 `unittest discover`：462/462 通过。
- 为支持 FULL 已安装后的持续回归，TRIAL/FULL 两个测试仅增加阶段感知：FULL 工件存在时验证已安装 95 行与 FULL payload/保护快照一致；FULL 未安装时仍执行原 TRIAL 空字段与保护快照门禁，生产代码门禁未放宽。
- `git diff --check` 通过；仅提示两个既有文本工作区 CRLF 将按仓库 LF 规范进入索引。

## 索引态关键工件 SHA-256

以下值均从精确暂存后的 Git index blob 字节计算；文本文件因此采用仓库 LF 内容：

- FULL payload：`d88b62fccf2911b50fccb50d23c84ee8d7ccf154b340bcb611dc7e7a4b4a9340`。
- FULL reconciliation：`2de0cb57ebe631411e0d7220dbd308a1b75f1c1a82adb3ede4df1bd8ff5177da`。
- FULL report：`256f2fb486206277137445907a9815a19fb2045540662d15b7e9f34a76bda136`。
- FULL audit sheet：`81012793c1c3d1be1c611f138501b037c6e0f94a4ceedba8bf76507caa1c2652`。
- FULL visual page 01：`1251b0ae6aa0032e79cd6e82d0cdbc38f6e7a994287d4cf1e874c42cede3e77e`。
- FULL visual page 02：`a76acf2551766dc9cfdc91b697331b7ad710de6264d2bae1b3721afea5e5dcd8`。
- FULL visual page 03：`f6fc71116a0ac3ce5052645a45ed5fb800bf2509c2e8b3904a5e27feae6dac19`。
- FULL visual page 04：`20fea6207d1a6b4763139229f86e33f1d5c3626277da60faa961aee5e04c0313`。
- 总底表 payload：`66ea238b9ef3327117129028dc8581668081ac16190b1f6e4e8cc3569129d5aa`。
- 总底表 CSV：`69d7a2a2393057b34d26630fff042f5ac3274adef8ca35fba8286c28d6934871`。
- 总底表 XLSX：`f02226df0425b241da5b86aa7ca104997e7eb8e22ea96ced31a23a2232d66810`。

## FULL 停止点

当前阶段为 `FULL_READY_FOR_FINAL_OWNER_AUDIT`。本分支只允许标准 fast-forward 推送并在 PR #82 报 `FULL_DONE`；随后保持自动监控，等待 Owner 最终画像审计。不得自行合并 PR、关闭 Issue #81、修改受保护工件或领取下一 Issue。

<Handoff_State>
Target: Issue #81 南方医科大学口腔医院(海珠广场院区)照片补录 FULL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/81
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/82
Branch: codex/mhrj/issue-81-smukq-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: FULL_READY_FOR_FINAL_OWNER_AUDIT
Completed:
- Owner 解除两次熔断后完成第三次 FULL；95=95 实采+0 失败，正式照片与画像各 95
- 总底表照片双列 190 个单元格更新；画像 95 份严格 +2/-0；索引零修改
- 四页全量视觉 95/95 目视通过；唯一大于 5 MiB 照片实图通过
- artifact-tool 六表导入、公式错误扫描、逐表渲染和三载体 9,222 行一致性复核通过
- 受保护资产、仓库相对路径、照片孤儿/缺失、哈希/魔数/尺寸和视觉页复算全部通过
- 专项 36/36、全仓 462/462、git diff --check 通过
CurrentFacts:
- 总底表 21 家医院、9,222 位医生、1,841 条异常提示；核验日期 2026-08-19
- 本院 95 行照片双列均非空；既有异常提示 72 条保持原值
- FULL payload 状态 PASSED_ALL_FULL_CONTACT_SHEETS_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS
Next:
- 标准 fast-forward 推送当前分支，等待 governance-check 成功后在 PR #82 发布 FULL_DONE
- 恢复 doctor-data-single-issue-monitor 为 ACTIVE，等待 nancywrayg57-jpg 最终画像审计
- 不合并 PR、不关闭 Issue、不领取下一 Issue
Constraints:
- 仅医院官网页面实际引用的 img.content_img 原始字节；禁止第三方来源、构造未引用路径、Cookie/代理/挑战绕过
- 入口台账、总底表更新报告、TRIAL 工件和 _索引.md 继续受保护
- 工件路径仅仓库相对；申报哈希仅按暂存 Git blob（LF）计算
Artifacts:
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_full_payload.json
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_full_reconciliation.csv
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_full_report.md
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_full_audit_sheet.jpg
- work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_full_visual_review/
- 医生画像仓库/01_试点医院/南方医科大学口腔医院(海珠广场院区)/照片/
- 医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.xlsx
</Handoff_State>

## Owner 条件终审与跨 checkout 单点修正

- Owner 在 PR #82 下发 [`FULL_AUDIT_CONDITIONAL → FIX_REQUIRED`](https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/82#issuecomment-5340626833)：除跨 checkout 可复现性外，FULL 数据、照片、画像、视觉、三载体和测试证据全部通过，且通过项无需重做。
- Linux 失败根因是活动引用链 `smukq → ny5y → zssy_photo_backfill_trial.py` 的最底层 `ROOT` 仍硬编码为 Windows 工作区；同时 FULL 画像路径只调用 `Path(...).as_posix()`，无法在 POSIX 主机把输入中的 Windows 反斜杠识别为分隔符。
- 最小修正将 ZSSY 基座 `ROOT` 改为 `Path(__file__).resolve().parents[1]`，并将该基座写入 payload/快照/命令结果的路径统一经 `as_posix()` 输出；SMUKQ FULL 在构造 `Path` 前先把反斜杠归一化为 `/`，并显式拒绝 Windows 盘符绝对路径与 UNC 路径。
- 未修改本批总底表、正式照片、画像、TRIAL/FULL 数据工件或其他历史一次性脚本。

验证结果：

- ZSSY、NY5Y、SMUKQ 相关测试：61/61 通过。
- 全仓 `unittest discover`：462/462 通过。
- `smukq_photo_backfill_full.py --validate-full`：`expected=95 downloaded=95 failed=0`。
- `git diff --check`：通过。

当前阶段为 `FULL_FIXED_READY_FOR_PUSH`。仅允许精确暂存本次 3 个代码/测试文件与本 ADR，提交后以标准 Git 协议 fast-forward 推送原分支，并在 PR #82 发布 `FULL_FIXED_DONE`；随后恢复自动监控，等待 Owner 仅复审本修正与回归结果。

<Handoff_State>
Target: Issue #81 南方医科大学口腔医院(海珠广场院区)照片补录 FULL 单点修正
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/81
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/82
Branch: codex/mhrj/issue-81-smukq-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: FULL_FIXED_READY_FOR_PUSH
Completed:
- 修复 zssy 基座 Windows ROOT 硬编码及活动引用链路径正斜杠归一化
- 增加 Windows 盘符绝对路径拒绝回归断言
- 相关测试 61/61、全仓 462/462、FULL 95/95 验证通过
Next:
- 精确暂存、提交并 fast-forward 推送原分支
- PR #82 发布 FULL_FIXED_DONE 后恢复监控，等待 Owner 跨 checkout 复审
Constraints:
- 不修改已通过的 FULL 数据资产与视觉工件
- 不扩展治理至 Owner 明确排除的更老一次性脚本
- 不合并 PR、不关闭 Issue、不领取下一 Issue
</Handoff_State>
