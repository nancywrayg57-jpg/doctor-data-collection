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
