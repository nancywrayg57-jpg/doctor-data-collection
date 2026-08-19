# 2026-08-19 Issue #83 南方医科大学皮肤病医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/83>。
- 医院：南方医科大学皮肤病医院；官网：<https://www.gdskin.com/>。
- 医生入口：Showclass 901/902/906/910/913/915/917/921/922 共 9 个分类；详情固定为 `ShowNews.ASPX?ID=<正整数>`。
- Phase：`TRIAL`；固定范围为总底表本院 77 行，照片双列全空，既有异常提示保持不动。
- 工作分支：`codex/mhrj/issue-83-gdskin-photo-backfill-trial`；基线 `361831ddb611cbd0c2a337b9004fb70f49c2e318`。
- Codex 领取评论：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/83#issuecomment-5341138462>。

本阶段只允许完成唯一 `/uploadimg/` 正文照片容器诊断、10 人 TRIAL、manifest/payload/report/灰底联系表/10 张页面引用原始字节、专项测试和本 ADR。未取得 Owner 在关联 PR 中明确下发的 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填总底表、修改正式画像或创建正式照片目录。

## 失败熔断、范围阻塞与 Owner 裁决

首次 TRIAL 连续两次验证失败后，Codex 依 `Agent.md` 熔断并先镜像 Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/83#issuecomment-5341352222>。

1. 第一次失败发生在文海泉已知占位判例的中文 URL 传输。页面实际引用保留原值，最小修正只在 `urllib` 请求传输层按浏览器语义百分号编码 Unicode path；Owner 后续追认该修正不是构造路径。
2. 第二次运行只成功 7/10：吴芳芳、杨超详情 200 但无 `/uploadimg/` 容器；孟凡琪页面原引用含 NBSP/空格尾缀，浏览器语义编码后照片资源 404。7 张成功照片 SHA 均唯一；“7≠10”是基数派生提示，不是真实跨医生重复。

Owner 首次解除熔断并允许同入口/同职称层替换、保留既有 7 张。Codex 只读核验发现入口 906/初级唯一候选于碧慧同样无容器，因此在未下载候选的情况下再次停止并请求唯一范围裁决。Owner 随后批准入口 906 跨职称层选谷梅，并批准孟凡琪→龚洋洋、杨超→钟泽敏。

恢复运行后谷梅、钟泽敏成功，但龚洋洋页面实际 NBSP 尾缀引用仍为 404，仅得到 9/10；Codex 再次停止并镜像 Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/83#issuecomment-5342024025>。Owner 最终在 <https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/83#issuecomment-5342092456> 指定杜美毅（ID 5596，入口 915/初级）并预核验详情及照片资源 200，同时定格郭先荟为同族 NBSP 悬空引用。最终恢复严格复用现有 9 张，仅联网下载杜美毅 1 张。

## 访问路径与照片容器

1. 全部请求使用固定常规浏览器 UA、无 Cookie、无代理、无并发；网络请求相邻启动间隔不小于 2 秒。
2. 详情只接受官网 HTTPS `ShowNews.ASPX?ID=<正整数>`；照片只接受该详情页唯一 `img src` 实际解析至官网 `/uploadimg/` 的 URL。
3. 只对页面原始 Unicode 引用做浏览器语义传输编码；payload 同时保留原引用、规范化 Unicode URL 与 transport URL，不构造或探测任何未引用变体。
4. `/WebResource.axd`、备案图标以及 logo/banner/nav/foot 等站架资源全部排除。
5. 中文“占位”文件名、query Base64 blank/placeholder/default、known-SHA、全图唯一颜色数不大于 2、跨医生同 SHA、灰底联系表空白/不可见格均为硬门禁。

文海泉（ID 5566）页面实际引用 `占位.png`；资源 SHA-256 为 `d2565a802cdc8d7ca29f218cd60685542d139a7de68ffc9ee559011e2f693aac`、200×200、4,959 bytes。该字节只用于双门禁取证，未写入磁盘，也未计入 10 位样本。

## 样本替换与失败证据

最终替换矩阵：

| 原样本 | 替换人 | 入口 | 职称层变化 | 裁决依据 |
|---|---|---:|---|---|
| 吴芳芳 | 谷梅 | 906 | 初级→正高 | 同入口初级候选于碧慧也无容器；Owner 裁决入口覆盖优先并允许跨层 |
| 孟凡琪 | 杜美毅 | 915 | 初级→初级 | 孟凡琪、龚洋洋、郭先荟的 NBSP 尾缀引用均悬空；Owner 指定资源 200 的杜美毅 |
| 杨超 | 钟泽敏 | 922 | 中级→中级 | 原页面无照片容器；同入口同层替换 |

原样本失败证据定格为吴芳芳/杨超 `无照片容器`、孟凡琪 `照片资源不可达`。供 FULL 引用的候选证据为于碧慧 `无照片容器`，以及龚洋洋/郭先荟 `照片资源不可达`。孟凡琪、龚洋洋、郭先荟均在 payload/report 保留含 NBSP 的页面引用和 `%C2%A0` transport URL；未尝试任何路径变体。

## TRIAL 结果与视觉验收

- 固定范围 77 行、77 个唯一详情 URL；样本覆盖 9/9 分类入口。
- 最终样本：顾有守、杨斌、吉苏云、谷梅、王柳苑、鲜华、杜美毅、严婷婷、何仁亮、钟泽敏。
- 职称层级为正高 4、副高 2、中级 3、初级 1；覆盖本院全部可用标准层。
- 10 个样本详情和照片资源全部 HTTP 200；10 张 SHA-256 全部唯一；JPEG 10 张，共 7,158,350 bytes；单图大于 5 MiB 与 20 MiB 均为 0。
- 两轮首页/代表详情可达性复测均为 HTTP 200，两轮间隔至少 30 秒。整个成功恢复运行包含 17 次真实网络请求，最小相邻启动间隔 2.0 秒；9 张既有成功照片原字节复用，仅杜美毅新下载。
- 灰底深色边框联系表逐格目视检查通过：10/10 均为可见单人医生职业照；未见患者、儿童、合影、二维码、装饰图、空白格或不可见格。
- 视觉状态：`PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`。

## 正式资产保护

TRIAL 前后快照完全一致：

- 总底表 JSON：`66ea238b9ef3327117129028dc8581668081ac16190b1f6e4e8cc3569129d5aa`。
- 总底表 CSV：`69d7a2a2393057b34d26630fff042f5ac3274adef8ca35fba8286c28d6934871`。
- 总底表 XLSX：`f02226df0425b241da5b86aa7ca104997e7eb8e22ea96ced31a23a2232d66810`。
- 总底表更新报告：`cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a`。
- 本院画像树：78 个文件，聚合 SHA-256 `64dd7f0edf76d9c6c6c95711b5c54b59a419d782f7478605f5c408ac1af29653`。
- 正式照片目录运行前后均不存在。

## 工件与验证

关键工件：

- `work/gdskin_photo_backfill_trial.py`
- `work/tests/test_gdskin_photo_backfill_trial.py`
- `work/南方医科大学皮肤病医院_photo_backfill_trial_payload.json`
- `work/南方医科大学皮肤病医院_photo_backfill_trial_manifest.csv`
- `work/南方医科大学皮肤病医院_photo_backfill_trial_report.md`
- `work/南方医科大学皮肤病医院_photo_backfill_trial_contact_sheet.jpg`
- `work/南方医科大学皮肤病医院_photo_backfill_trial_photos/`（10 张页面引用原始字节）

精确暂存后的仓库 blob（LF）内容 SHA-256：

- payload：`2f5dffdd792e7fefa7d48b432c640d68aeade968e3f6fef298334ca0aab7182a`。
- manifest：`9883a014bab6c900413a425a18247826b7d3aefb7783137a25cf82b486551b0e`。
- report：`9e31329c309f32f94db658beb9fe961afe72ae5eacc502bc831c0f5f9630b74d`。
- contact sheet：`f52a9f901087ba0f1a6e215ddd908d4844668df58e0a0fc48fc674b64c0395f3`。

验证结果：

- Issue #83 专项测试：16/16 通过。
- `--mark-visual-pass` 后 `--validate` 通过。
- Issue #83 + NY5Y 共享基座 + ZSSY 底层基座顺序回归：41/41 通过。
- 全仓 `unittest discover`：478/478 通过。当前 bundled primary Python 缺少既有 `requests`/`bs4` 依赖，首次发现阶段出现 12 个导入错误；改用本机既有且依赖齐全的 Codex runtime backup Python 后全量通过，未安装依赖、未为环境问题修改生产代码。
- 精确暂存 17 个 Issue #83 文件；`git diff --cached --check` 通过。

## 当前停止点

当前阶段为 `TRIAL_READY_FOR_OWNER_AUDIT`。只允许完成回归验证、精确暂存、提交，以标准 Git 协议 fast-forward 推送当前分支，创建关联 Issue #83 的 PR，并在 `governance-check` 成功后发布 TRIAL 审计材料；随后恢复自动监控并等待 Owner 审计。不得自行进入 FULL、合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #83 南方医科大学皮肤病医院照片补录 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/83
Branch: codex/mhrj/issue-83-gdskin-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 按 Owner 最终裁决复用 9 张既有原字节，仅下载杜美毅，完成 10 人/9 入口 TRIAL
- 固化 Unicode URL 传输编码与孟凡琪/龚洋洋/郭先荟 NBSP 悬空引用证据
- known-SHA 和中文占位双门禁通过；联系表 10/10 目视通过；正式资产零修改
- 专项测试 16/16、共享顺序回归 41/41、全仓 478/478、TRIAL 验证通过
CurrentFacts:
- 固定范围 77 行，照片双列仍全空；本院正式照片目录不存在
- TRIAL 10 张 JPEG 共 7,158,350 bytes，SHA 全部唯一，>5 MiB 与 >20 MiB 均为 0
- payload 视觉状态 PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS
Next:
- 完成共享基座和全仓回归、精确暂存、提交并标准 fast-forward 推送当前分支
- 创建关联 Issue #83 的 PR，等待 governance-check 后发布 TRIAL_READY_FOR_OWNER_AUDIT
- 仅 Owner 在当前 PR 明确下发 FULL_APPEND_AND_OBSIDIAN 后继续
Constraints:
- 仅医院官网页面实际引用原始字节；串行间隔至少 2 秒
- 禁止第三方来源、Cookie、代理、挑战绕过、构造未引用路径、患者素材和 TRIAL 正式资产写入
- 不得合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- work/南方医科大学皮肤病医院_photo_backfill_trial_payload.json
- work/南方医科大学皮肤病医院_photo_backfill_trial_manifest.csv
- work/南方医科大学皮肤病医院_photo_backfill_trial_report.md
- work/南方医科大学皮肤病医院_photo_backfill_trial_contact_sheet.jpg
- work/南方医科大学皮肤病医院_photo_backfill_trial_photos/
</Handoff_State>
