# 2026-08-19 Issue #79 南方医科大学第五附属医院照片补录 TRIAL

## 目标与授权

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/79>。
- 医院：南方医科大学第五附属医院。
- 官网：<http://www.ny5y.cn/>。
- 医生目录：主入口 <http://www.ny5y.cn/zhuanjia_mingyi.php?id=100>（133 行）；岭南名医入口 <http://www.ny5y.cn/zhuanjia_lingnan.php?id=162>（1 行）。
- Phase：`TRIAL`；固定范围为总底表本院 134 行，TRIAL 正式资产必须零修改。
- 工作分支：`codex/mhrj/issue-79-ny5y-photo-backfill-trial`；基线 `1119e5924cb1ec33a0c2b2ee8e239619ba6b97e0`。
- Codex 领取评论：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/79#issuecomment-5336914111>。

本轮只允许完成照片容器结构诊断、10 人 TRIAL、manifest/payload/report/联系表/10 张页面引用原图、专项测试和 ADR。未取得 Owner 在关联 PR 中明确下发的 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填照片字段、创建正式照片目录或刷新画像。

## 两次失败熔断与 Owner 裁决

Issue #79 首轮执行严格按 `Agent.md` 的连续两次失败规则熔断，并先镜像 GitHub：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/79#issuecomment-5336971992>。

1. 第一次失败发生在联网前：复用框架仍要求正高/副高/中级/初级四层同时存在，而本院固定 134 行实际分布为正高 39、副高 92、中级 3、初级 0。最小修正为按实际三层选取 3 正高、4 副高、3 中级并覆盖至少 5 科室。
2. 第二次失败发生在任何详情请求或工件写入前：无浏览器 UA 的默认 `urllib` 请求首页返回 HTTP 502。此前 PowerShell 对固定 10 个详情及其照片资源均为 200，因此停止进一步请求并等待 Owner 裁决。

Owner 在 <https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/79#issuecomment-5337015097> 明确下发 `OWNER_RULING → RESUME_TRIAL`，解除熔断并裁决：

1. 追认三层职称最小修正。
2. 允许所有请求携带固定常规浏览器 User-Agent；仍禁止 Cookie、代理绕道和挑战破解。
3. 首页只留痕、不作为采集门禁；固定详情页及其唯一容器照片资源才是门禁。
4. 恢复后先对首页和抽样详情执行两轮、间隔至少 30 秒的 UA 可达性复测；详情/照片若波动，须先回报再启动五轮聚合探测。

## 访问路径与合规边界

Issue #79 专用实现使用以下最小路径：

1. Python 标准库 `urllib` GET，固定 User-Agent 为 `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36`。
2. `ProxyHandler({})` 显式禁用代理；不安装 Cookie 处理器，不携带非站方 Cookie，不处理挑战或验证码。
3. 详情只接受 `http(s)://(www.)ny5y.cn/yisheng_xq.php?id=<正整数>`；最终照片 URL 必须仍为官网且路径以 `/ueditor/php/upload/image/` 开头。
4. 只下载唯一 `div.yisheng_xq_bug_left` 内联 `background-image` 实际引用的资源；不构造或探测页面未引用路径。
5. `images/logo.jpg`、`images/gzwm.jpg`、`images/float*.png`、政府徽标、正文 ueditor 叙事配图和容器外所有资源均排除。
6. 不使用第三方来源，不采集患者评价、隐私、登录后或非公开数据。

## FATAL 解除后的两轮可达性证据

两轮间隔超过 30 秒；首页和固定抽样详情均为 HTTP 200。首页结果仅留痕，抽样详情是门禁。

| 轮次 | 目标 | HTTP | Content-Type | 字节 | UTC |
|---:|---|---:|---|---:|---|
| 1 | 首页（非门禁） | 200 | text/html | 213826 | 2026-08-19T03:15:12Z |
| 1 | 黄艺洪详情 ID 282（门禁） | 200 | text/html | 15810 | 2026-08-19T03:15:13Z |
| 2 | 首页（非门禁） | 200 | text/html | 213826 | 2026-08-19T03:15:44Z |
| 2 | 黄艺洪详情 ID 282（门禁） | 200 | text/html | 15810 | 2026-08-19T03:15:44Z |

## 医生照片容器与占位门禁

10 个样本详情页均只接受：

```text
div.yisheng_xq_bug_left[style*="background-image"]
```

判定规则：

1. 容器必须恰有一个，详情页姓名必须与底表姓名完全一致。
2. 只解析该容器内联 `background-image` 的页面实际引用；页面其他图片绝不提升为候选。
3. 照片 URL 的 path 或 Base64 query 解码出现 `blank`、`placeholder`、`default` 时拦截。
4. 图片全图唯一颜色数不大于 2 时拦截。
5. 不同详情页出现同一 SHA-256 时停止并转 Owner 人工追认。
6. 联系表使用灰底和深色边框；任何空白或不可见格均停止并转人工复判。

本次 10 个详情、照片 URL 和 SHA-256 均唯一；四层占位门禁命中 0。

## 样本设计与 TRIAL 结果

固定样本为 10 人，覆盖 8 个科室，职称层级为正高 3、副高 4、中级 3、初级 0；已覆盖本院全部可用职称层。

| 姓名 | 科室 | 主职称 | 层级 | 详情 HTTP | 照片 HTTP | 实际格式 | 字节 | 尺寸 |
|---|---|---|---|---:|---:|---|---:|---:|
| 黄艺洪 | 未标注 | 主任医师 | 正高 | 200 | 200 | PNG | 189404 | 413×582 |
| 司昌荣 | 中医科 | 主任中医师 | 正高 | 200 | 200 | PNG | 737680 | 738×1024 |
| 安得辉 | 中医科 | 主治中医师 | 中级 | 200 | 200 | PNG | 2282621 | 935×1361 |
| 周姗 | 中心实验室 | 副研究员 | 副高 | 200 | 200 | PNG | 1252401 | 2666×4000 |
| 郭丽冬 | 临床营养科 | 副主任医师 | 副高 | 200 | 200 | PNG | 131036 | 413×579 |
| 王波涛 | 介入血管外科 | 副主任技师 | 副高 | 200 | 200 | JPEG | 132784 | 900×1350 |
| 沈玉才 | 儿童重症医学科 | 主任医师 | 正高 | 200 | 200 | PNG | 206664 | 413×579 |
| 吴智勇 | 精神心理科 | 主治医师 | 中级 | 200 | 200 | PNG | 155326 | 413×579 |
| 许桂璇 | 精神心理科 | 主治医师 | 中级 | 200 | 200 | PNG | 111273 | 413×579 |
| 杨柳 | 超声诊断科 | 副主任医师 | 副高 | 200 | 200 | JPEG | 193711 | 1269×1392 |

- 详情成功 10/10，照片成功 10/10；详情失败、结构异常、无照片容器、占位图和照片资源不可达均为 0。
- 10 张共 5,392,900 bytes；PNG 8、JPEG 2；声明格式与魔数格式全部一致。
- 大于 5 MiB 的单图为 0，大于 20 MiB 为 0。
- 联系表逐格目视确认 10/10 都是可见的单人职业照；未见患者、儿童、合影、二维码、装饰图或空白占位格。
- payload 视觉状态为 `PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`。

## 正式资产保护

TRIAL 前后受保护快照完全一致：

- 总底表 JSON：`4a71e0a10b43349c246f33e4448ae8882ed8ee79443d1f25cb5a25191ba25bb1`。
- 总底表 CSV：`07c8b7aa21c86d5797da03719eea5daf8e6c253132713899296bd8d3693b2db7`。
- 总底表 XLSX：`8fcb09d6a64f73731b5d5b70463d3f928e338f6c8056097f1f68a51f847323c7`。
- 总底表更新报告：`cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a`。
- 本院画像树：135 个文件、496,582 bytes，聚合 SHA-256 `1492e5ac46f1bf4ccb7cb5d06249c4208298e33596fd8c2f62def5a4992a2d2a`。
- 正式照片目录运行前后均不存在。

## 工件与验证

关键工件：

- `work/ny5y_photo_backfill_trial.py`
- `work/tests/test_ny5y_photo_backfill_trial.py`
- `work/南方医科大学第五附属医院_photo_backfill_trial_payload.json`
- `work/南方医科大学第五附属医院_photo_backfill_trial_manifest.csv`
- `work/南方医科大学第五附属医院_photo_backfill_trial_report.md`
- `work/南方医科大学第五附属医院_photo_backfill_trial_contact_sheet.jpg`
- `work/南方医科大学第五附属医院_photo_backfill_trial_photos/`（10 张页面引用原始字节）

工件 SHA-256：

- payload：`4edfdf6d492689ece4d74ed079a36567f52022fa545373a4782013daf9c8f473`。
- manifest：`f0774ecfa4d0ee027a24566d8a7a80cd6bf9601dc55ce3f11d93f7aa99366327`。
- report：`229bf297f53739dd4da1522aedb4efeb115e0863bc2ffa450ab5bc0f6d773fe4`。
- contact sheet：`13c8240e0204bf40159cb33146b78ccacad38a18f7877b7756993c83a7815f7b`。

验证结果：

- Issue #79 专项测试：9/9 通过。
- `--mark-visual-pass` 后 `--validate` 通过。
- 全仓 `unittest discover`：426/426 通过。
- 首次全仓回归使用精简 Codex Python 时，因既有 `requests`/`bs4` 未安装导致 10 个模块无法导入；切换到仓库既有、依赖齐全的本机 Python 后 426/426 通过，未安装依赖、未修改代码处理该环境问题。

## 当前停止点

当前阶段为 `TRIAL_READY_FOR_OWNER_AUDIT`。只允许精确暂存、提交，以标准 Git 协议 fast-forward 推送当前分支，创建关联 Issue #79 的 PR，并在 `governance-check` 通过后发布 TRIAL 审计材料。随后恢复自动监控并等待 Owner 审计；不得自行进入 FULL、合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #79 南方医科大学第五附属医院照片补录 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/79
Branch: codex/mhrj/issue-79-ny5y-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- Owner 已解除两次失败熔断，并追认三层职称抽样与浏览器 UA 访问路径
- 两轮首页/抽样详情 UA 可达性复测均为 HTTP 200，间隔至少 30 秒
- 完成 10 人、8 科室、正高3/副高4/中级3 的 TRIAL 和原始字节工件
- 联系表 10/10 目视通过；四层占位门禁命中 0
- 正式总底表、本院 135 个 Markdown 与正式照片目录零修改
- 专项 9/9、全仓 426/426、TRIAL 验证通过
CurrentFacts:
- 固定范围 134 行，照片双列仍全空；本院正式照片目录不存在
- TRIAL 10 张共 5,392,900 bytes，PNG 8、JPEG 2，>5 MiB 与 >20 MiB 均为 0
- payload 状态 PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS
Next:
- 精确暂存、提交并标准 fast-forward 推送当前分支，创建关联 Issue #79 的 PR
- 等待 governance-check 后发布 TRIAL_READY_FOR_OWNER_AUDIT
- 仅 Owner 在当前 PR 明确下发 FULL_APPEND_AND_OBSIDIAN 后继续
Constraints:
- 仅 Owner 批准的固定浏览器 UA urllib 官方公开 GET；无 Cookie、代理、挑战绕过或第三方来源
- 只采唯一 yisheng_xq_bug_left 容器页面实际引用的原始字节，不构造或探测页面未引用路径
- 患者及任何患者可识别信息绝对禁止；TRIAL 正式资产零修改
- 不得合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- work/南方医科大学第五附属医院_photo_backfill_trial_payload.json
- work/南方医科大学第五附属医院_photo_backfill_trial_manifest.csv
- work/南方医科大学第五附属医院_photo_backfill_trial_report.md
- work/南方医科大学第五附属医院_photo_backfill_trial_contact_sheet.jpg
- work/南方医科大学第五附属医院_photo_backfill_trial_photos/
</Handoff_State>

## FULL 阶段：两次失败、Owner allowlist 裁决与第三次事务

Owner 在 PR #80 的 `TRIAL_AUDIT_PASSED → FULL_APPEND_AND_OBSIDIAN` 评论中授权固定 134 行 FULL：
<https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/80#issuecomment-5337189780>。

FULL 前两次执行均完整回滚、正式资产零残留：

1. 第一次在王敏聪（详情 ID 458）停止。详情 HTTP 200，但页面是无医生正文、姓名、职称及 `div.yisheng_xq_bug_left` 的空医院模板。最小修正仅将该实证分类为 `无照片容器`，并将职称一致性门禁限定在成功媒体行。
2. 第二次结构预检得到 132 行可采、2 行无照片容器；正式事务完成 `134 = 132 + 2` 后，被跨详情同 SHA 门禁阻断。陈特立 IDs 489/314 共用 SHA `d48a3b1b579a99f88d01d48d201cdc5001efd9361095a81e81c2b1fc93e372f7`；何卓凯 IDs 494/478 共用 SHA `de6da92057b28cb02f8b431ebf32e7b73f9e8229d05571be7ef5d3a1c28c22fc`。Codex 未自行认定，先在 PR 镜像 FATAL 并等待人工裁决。

Owner 在 <https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/80#issuecomment-5337332486> 独立核验四个详情页及两张实图后解除熔断并裁决：

1. 精确批准陈特立 `(489,314)` 与何卓凯 `(494,478)` 两组 same-person allowlist；除此之外任何跨详情同 SHA 仍须拦截。
2. 两行分别保留各自页面实际引用 URL、各自正式文件及画像嵌入；manifest/对账表的四行均写入 Owner 裁决证据。
3. 追认王敏聪 ID 458 的 `无照片容器` 分类及“成功媒体行才执行职称一致性门禁”的最小修正。
4. 预期四数对账固定为 `134 = 实采 132 + 失败 2（无照片容器）`。

第三次 FULL 事务按该精确 allowlist 成功完成；适配层继续拒绝任何非 allowlist 重复 SHA。

## FULL 数据结果

- 固定范围：134 行；实采 132，失败留空 2。
- 失败行：王敏聪 ID 458、孙乐栋 ID 274；两者详情均 HTTP 200，但无医生正文及唯一照片容器，照片双列留空并将结构化证据写入 `异常提示`。
- TRIAL 原字节复用 10 张；FULL 新下载 122 张；请求路径仍为固定浏览器 UA 的官方公开 urllib GET，无 Cookie、代理、挑战绕过、构造路径或第三方来源。
- 正式照片 132 张，共 28,996,303 bytes；PNG 101、JPEG 31；最大单图 2,546,664 bytes。
- 尺寸分桶：`<200 KiB` 108、`200 KiB–1 MiB` 21、`1–5 MiB` 3、`5–20 MiB` 0、`>20 MiB` 0。
- 总底表精确字段 diff 266 个：`照片链接` 132、`照片文件` 132、`异常提示` 2；总底表更新报告保持不变。
- 132 份成功画像均恰好插入方案 A 的 `+2/-0`；2 份失败画像零修改；`_索引.md` 零修改。院目录仍为 135 个 Markdown 文件（132 份已嵌照片的成功画像、2 份未改失败画像、1 个索引）。
- 正式照片目录包含 132 个文件；所有画像照片引用唯一性与落盘存在性检查通过。

## FULL 视觉审计与验证

- 六张分页联系表已逐页目视检查，132/132 均为可见单人职业照；未见患者、儿童、合影、二维码、装饰图、空白格或不可见格。
- 10 人审计表已逐格目视检查通过；`--mark-visual-pass` 成功写入 `PASSED_ALL_FULL_CONTACT_SHEETS_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`。
- `--validate-full` 通过：`expected=134 downloaded=132 failed=2`。
- Issue #79 FULL 专项测试 11/11 通过。
- 全仓测试最终 437/437 通过。第一次全仓回归发现新增测试调用 `configure_framework()` 后泄漏模块全局状态；唯一修正为用 `try/finally` 作用域替换并恢复相关全局，第二次全仓回归全部通过。
- XLSX 使用指定 `@oai/artifact-tool` 打开并检查六张工作表；目标行、两条失败、两组 allowlist、待复核清单和医院统计均核验，公式错误扫描为 0。

最终 SHA-256：

- 总底表 CSV：`76cc746cd16cd6151da6e2ee22645bc9b93e7896f89c7dcb6bb01915def72f39`。
- 总底表 XLSX：`cf9a6c20df19da719f205837daccf923cd36859cf8e84f8b434f887b2a200fa3`。
- 总底表更新报告：`cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a`。
- FULL payload：`1d553db887c50e03b92fb8afbd95dbbd403e19ca8b181421e9715cc04a5ad94c`。
- FULL reconciliation CSV：`8f8c1b37b01b5c9fb57cb189430f350f002a8d191d5519f319bb407071990e5a`。
- FULL report：`2fd1adddb7168fbdcf52bf4c24ec9a5b2739971597d22dc1e1bc1ac98931b5`。
- FULL audit sheet：`c0050299b0ca7a0f4ef627e35ebc175880275340437c3c8870b83a0226addb66`。

## FULL 当前停止点

当前阶段为 `FULL_READY_FOR_FINAL_OWNER_AUDIT`。只允许精确暂存 Issue #79 FULL 文件、提交、确认远端仍指向 TRIAL commit 后以标准 Git 协议 fast-forward 推送当前分支，等待 `governance-check` 成功，再在 PR #80 发布 `FULL_DONE`。随后恢复自动监控并等待 Owner 最终审计；不得合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #79 南方医科大学第五附属医院照片补录 FULL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/79
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/80
Branch: codex/mhrj/issue-79-ny5y-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: FULL_READY_FOR_FINAL_OWNER_AUDIT
Completed:
- Owner 精确批准两组 same-person duplicate-SHA allowlist，第三次 FULL 事务成功
- 完成 134 = 实采 132 + 无照片容器 2；总底表、132 张正式照片与 132 份画像已同步
- 六页 132 张联系表和 10 人审计表目视通过
- --validate-full、专项 11/11、全仓 437/437、XLSX 六表和公式错误扫描全部通过
CurrentFacts:
- 两条失败为王敏聪 ID 458、孙乐栋 ID 274，照片双列留空且异常提示有结构化证据
- 两组重复 SHA 仅限陈特立 IDs 489/314 与何卓凯 IDs 494/478；其他跨医生重复组为 0
- 132 张照片共 28,996,303 bytes，PNG 101/JPEG 31，>5 MiB 与 >20 MiB 均为 0
Next:
- 精确暂存、提交并标准 fast-forward 推送当前分支
- 等待 governance-check 后在 PR #80 发布 FULL_DONE
- 恢复 monitor ACTIVE 并等待 Owner 最终审计
Constraints:
- 不得合并 PR、关闭 Issue 或领取下一 Issue
- 仅官方公开来源；禁止 Cookie、代理、挑战绕过、构造未引用路径、第三方来源与患者素材
Artifacts:
- work/南方医科大学第五附属医院_photo_backfill_full_payload.json
- work/南方医科大学第五附属医院_photo_backfill_full_reconciliation.csv
- work/南方医科大学第五附属医院_photo_backfill_full_report.md
- work/南方医科大学第五附属医院_photo_backfill_full_audit_sheet.jpg
- work/南方医科大学第五附属医院_photo_backfill_full_visual_review/
- 医生画像仓库/01_试点医院/南方医科大学第五附属医院/照片/
</Handoff_State>
