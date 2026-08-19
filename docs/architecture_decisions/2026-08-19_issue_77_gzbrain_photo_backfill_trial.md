# 2026-08-19 Issue #77 广州医科大学附属脑科医院照片补录 TRIAL + FULL

## 目标与授权

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/77>。
- 医院：广州医科大学附属脑科医院。
- 官网：<https://www.gzbrain.cn/>。
- 医生目录：<https://www.gzbrain.cn/myzj/list.html>。
- Phase：`TRIAL`；固定范围为总底表本院 183 行，正式资产必须零修改。
- 工作分支：`codex/mhrj/issue-77-gzbrain-photo-backfill-trial`；基线 `ce9d086b59965b38e9dcad680275ad2e5fa2f19a`。
- Codex 领取评论：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/77#issuecomment-5333426747>。

本轮只允许完成照片容器结构诊断、10 人 TRIAL、manifest/payload/report/联系表/10 张页面引用原图、专项测试和 ADR；未取得 Owner 明确 `FULL_APPEND_AND_OBSIDIAN` 前不得回填照片字段、创建正式照片目录或刷新画像。

## 访问路径与合规边界

采集期历史 ADR 已证明，浏览器型 `requests.Session` 会命中 nginx HTTP 403，而 Python 标准库默认 `urllib` 公开 GET 可访问 IIS 页面。Issue #77 现场重新核验首页、目录、固定样本详情和照片资源均可达，因此本轮继续使用本院已批准的最小访问路径：

1. 仅 Python 标准库 `urllib` GET；保留其默认非浏览器 User-Agent。
2. 显式禁用代理；不安装 Cookie 处理器，不添加 Referer、自定义浏览器请求头或浏览器指纹。
3. 不处理挑战、不绕过验证码或权限、不调用未声明接口、不使用第三方来源。
4. 详情只接受 `https://www.gzbrain.cn/myzj/info_itemid_<数字>.html`；最终响应不得越出官网。
5. 详情不可达时最多两次、间隔至少 30 秒留证；本次 10 人均首次 HTTP 200，未启动波动聚合协议。

## 医生照片容器与 URL 门禁

10 个样本详情页结构一致，严格本人照片容器为：

```text
.single_con > .single_cn > .single-img > img[src]
```

代表性 HTML：

```html
<div class="single-img"> <img alt="" src="/uploadfiles/2019/06/20190610095458209.png?5a6B546J6JCNLnBuZw=="/> </div>
```

判定规则：

1. `.single_con` 的直接子 `.single_cn` 下必须恰有一个直接子 `.single-img`，其中必须恰有一个直接 `img[src]`；页面其他区域的图片绝不提升为候选。
2. 照片 URL 必须由详情页实际引用，经 `urljoin` 后仍为同站 HTTPS，路径严格匹配 `/uploadfiles/YYYY/MM/<文件>.<jpg|jpeg|png|gif|webp>`。
3. 官网当前使用的查询串是不带键名的不透明 Base64 风格令牌；必须原样保留，禁止去查询串、构造所谓原图或猜测其他路径。
4. 公共图标、banner、医院环境、新闻/科普卡片、二维码、占位图、院徽/Logo 以及所有严格容器外资源只记录排除规则，不下载。
5. 即使资源通过结构和 URL 门禁，仍必须经联系表目视排除患者、儿童、合影、二维码、装饰或占位图；精神专科患者可识别信息绝对禁止进入资产。

## 样本设计

固定 10 人覆盖 10 个不同科室首原子，并在可用职业照中覆盖四层职称：正高 4、副高 3、中级 2、其他 1。

| 姓名 | 科室 | 职称 | 层级 | 详情 ID |
|---|---|---|---|---:|
| 宁玉萍 | 神经内科 | 主任医师 | 正高 | 966 |
| 成友军 | 神经外科 | 副主任医师 | 副高 | 803 |
| 周素妙 | 中西医结合科 | 主治医师 | 中级 | 96281 |
| 张双春 | 临床心理科 | 心理治疗师 | 其他 | 11791 |
| 周亮 | 社区精神科 | 教授 | 正高 | 4746 |
| 彭妙官 | 内分泌科 | 副主任医师 | 副高 | 100106 |
| 王治华 | 司法鉴定科 | 主治医师 | 中级 | 560 |
| 郭耀光 | 康复科 | 副主任医师 | 副高 | 101440 |
| 张继辉 | 睡眠与节律医学中心 | 研究员 | 正高 | 49356 |
| 韩为 | 中医科 | 主任中医师 | 正高 | 33179 |

## TRIAL 结果与视觉复核

- 固定范围：183 行、183 个唯一详情 URL；TRIAL 前 `照片链接` 与 `照片文件` 全空。
- 本院画像目录：183 份画像加 `_索引.md`，共 184 个 Markdown；正式照片目录不存在。
- 详情成功 10/10，照片成功 10/10；状态闪烁、详情失败、无照片容器、占位图、照片资源不可达均为 0。
- 10 个照片 URL 唯一、10 个 SHA-256 唯一；页面未引用路径探测 0、排除资源下载 0、第三方来源 0、Cookie 0。
- 原始响应总字节 2,225,954；最小 21,126；中位数 84,408；平均 222,595；最大 954,574。
- 大小分桶：`<200KiB=7`、`200KiB-1MiB=3`、`1-5MiB=0`、`5-20MiB=0`、`>20MiB=0`；无需 >5 MiB Owner 实图清单。
- 成友军页面 URL 扩展名和 Content-Type 声明为 JPEG，但原始字节魔数为 PNG；未转码、未压缩，文件按真实格式 `.png` 命名，其余 9 张声明扩展名与魔数一致。
- 联系表 SHA-256：`083900e1833a856ad8aa7bb0d1beed0b4cb7464fac35897893a29b6f62c61565`。
- 联系表已逐格目视确认：10/10 均为单人医生职业照，未见患者、儿童、合影、二维码、公共装饰或占位图；payload 状态为 `PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。

## 一次本地自校验修正

首次 TRIAL 完成网络与图片读取后，被写 payload 前的本地自校验拦截。根因是验证器把 HTML class 误写成 CSS 选择器形式：实际片段包含 `class="single-img"`，校验却搜索 `.single-img`。照片容器解析、网络响应和正式资产快照均正常。

最小修正是让验证器检查真实 HTML class 属性，并在专项测试中锁定该片段。首次失败仅留下 10 张可重建 `work/` 临时图和一张联系表；已精确列举并删除，未触碰总底表、入口台账、184 个本院 Markdown 或正式照片目录。修正后的第二次 TRIAL 成功，未达到连续两次修复失败熔断条件。

## 正式资产保护

TRIAL 前后以下受保护快照完全一致：

- 总底表 JSON：`e296b4f9f6cf15550aaac7d13f230b7822bd2fc34e9f3ed4118eba6c3ad12643`。
- 总底表 CSV：`c4cd6522231a630867fa4a01786013944737f9078b80de172133c55a7b037c7d`。
- 总底表 XLSX：`a01b0cab689872f790427f078fc48055da55b025daa565edd31eb5aee52b45a6`。
- 总底表更新报告：`cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a`。
- 官网入口台账：`04273e1500e8dcb2483280fd53ed775543f0159531eca6f247a5bdf3a70a8911`。
- 本院 184 个 Markdown 聚合 SHA-256：`15d890952f3f6288715cd7caf3836b0d0a0e7390ac9826be5b85f1fedc1b459a`。
- 正式照片目录运行前后均不存在。

## 工件与停止点

- `work/gzbrain_photo_backfill_trial.py`
- `work/tests/test_gzbrain_photo_backfill_trial.py`
- `work/广州医科大学附属脑科医院_photo_backfill_trial_payload.json`
- `work/广州医科大学附属脑科医院_photo_backfill_trial_manifest.csv`
- `work/广州医科大学附属脑科医院_photo_backfill_trial_report.md`
- `work/广州医科大学附属脑科医院_photo_backfill_trial_contact_sheet.jpg`
- `work/广州医科大学附属脑科医院_photo_backfill_trial_photos/`（10 张页面引用版本原始字节）

专项测试、全仓回归和 Git/工件完整性检查完成后，提交并以标准 Git 协议 fast-forward 推送当前分支，创建关联 Issue #77 的 PR 请求 Owner TRIAL 审计。当前停止点为 `TRIAL_READY_FOR_OWNER_AUDIT`；不得自行进入 FULL、合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #77 广州医科大学附属脑科医院照片补录 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/77
Branch: codex/mhrj/issue-77-gzbrain-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 固化 single_con/single_cn/single-img 唯一医生照片容器和同站 uploadfiles 不透明查询串门禁
- 完成 10 科室、正高4/副高3/中级2/其他1 的 10 人 TRIAL 与原始字节工件
- 联系表 10/10 目视通过，未见患者、儿童、合影、二维码、装饰或占位图
- 正式资产前后快照一致
CurrentFacts:
- 固定范围 183 行，照片两列仍全空；本院 184 个 Markdown 未修改，正式照片目录不存在
- TRIAL 10 张共 2,225,954 bytes，最大 954,574 bytes，>5 MiB 与 >20 MiB 均为 0
- 成友军 URL/Content-Type 声明 JPEG、原始魔数 PNG，按真实格式 .png 保留
Next:
- 提交、标准 fast-forward 推送并创建关联 Issue #77 的 PR
- 等待 nancywrayg57-jpg TRIAL 审计；仅明确 FULL_APPEND_AND_OBSIDIAN 后继续
Constraints:
- 仅默认 urllib 官方公开 GET；无 Cookie、代理、自定义浏览器头、挑战绕过或第三方来源
- 只采详情页严格容器实际引用的原始字节，不构造或探测页面未引用路径
- 患者及任何患者可识别信息绝对禁止；TRIAL 正式资产零修改
Artifacts:
- work/广州医科大学附属脑科医院_photo_backfill_trial_payload.json
- work/广州医科大学附属脑科医院_photo_backfill_trial_manifest.csv
- work/广州医科大学附属脑科医院_photo_backfill_trial_report.md
- work/广州医科大学附属脑科医院_photo_backfill_trial_contact_sheet.jpg
- work/广州医科大学附属脑科医院_photo_backfill_trial_photos/
</Handoff_State>

## FULL 授权与执行结果

Owner 于 PR #78 明确给出 `TRIAL_AUDIT_PASSED → FULL_APPEND_AND_OBSIDIAN`：<https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/78#issuecomment-5333776500>。本轮严格复用已审计 TRIAL 10 张，只对其余 173 条固定详情 URL 执行默认 `urllib` 官方公开 GET；无 Cookie、代理、自定义浏览器头、挑战绕过、页面未引用路径探测或第三方来源。

四数对账闭合：

| 固定目标 | 实采成功 | 失败留空 | 正式落盘 | 照片字段留空 |
|---:|---:|---:|---:|---:|
| 183 | 181 | 2 | 181 | 2 |

- TRIAL 复用 10；FULL 新抓取成功 171；FULL 新抓取失败 2。
- 失败四类：详情不可达 0、照片资源不可达 0、无照片容器 0、占位图 2。
- 详情状态波动 0；照片状态波动 0；未启动 5 轮聚合协议。

## FULL 两条占位边界诊断

1. 程道猛，详情 ID `877`：严格 `.single-img` 容器唯一引用 `https://www.gzbrain.cn/uploadfiles/image/doctor_img1.jpg?ZG9jdG9yX2ltZzEuanBn`。路径及文件名明确为站点通用 `doctor_img1.jpg` 默认资源，按路径侧占位边界在下载前排除；照片字段保持空白，画像零触碰。
2. 梁卉薇，详情 ID `989`：严格容器唯一引用同站页面实际声明的 BMP URL；资源首次 HTTP 200、`image/bmp`，但响应仅 5,686 bytes、96×48，命中小尺寸响应侧占位边界。该判例允许页面引用的非主流格式进入响应校验，但占位判定优先于异常格式熔断；照片字段保持空白，画像零触碰。

两条证据均记录观测 UTC、唯一资源 URL、引用数、模板签名和判定特征，并写入 FULL payload、reconciliation 与报告。

## 三载体、照片与画像结果

- 总底表 payload/CSV/XLSX 已逐值核对一致；只发生 364 个授权单元格变化：`照片链接` 181、`照片文件` 181、`异常提示` 2。
- 正式照片 181 张，共 70,819,590 bytes；实际格式 PNG 66、JPEG 115；声明格式与魔数不一致 18，均按实际魔数命名且保留原始字节。
- 最大照片为徐文军 11,646,846 bytes、3024×3024、SHA-256 `eef393825403f18cf1384eefa96597957830a8549c4814b01ddc9b7efc1233c1`；这是唯一超过 5 MiB 的照片，未出现超过 20 MiB 的资源。
- 181 份 AUTO 画像仅新增照片块，逐份严格 `+2/-0`；程道猛与梁卉薇两份失败画像零触碰；`_索引.md` 零修改。
- 入口台账、总底表更新报告及全部 TRIAL 工件前后哈希不变。

## 视觉与工作簿门禁

- FULL 抽样审计图覆盖最小、最大及 8 个确定性随机样本；8 页全量联系表覆盖 181/181 正式照片。
- 8 页逐格目视结果：全部为单人医生职业照，未见患者、儿童、合影、二维码、装饰或占位图；payload 状态为 `PASSED_ALL_FULL_CONTACT_SHEETS_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`。
- 唯一 >5 MiB 的徐文军原图已单独目视，确认为单人医生职业照。
- 更新后的总底表 XLSX 已重新导入核验：6 张工作表齐全、公式错误扫描为 0；6 张 `master_*` 预览逐表目视无空白页、破损表头、公式错误文本或明显布局异常。

## FULL 验证与工件

- FULL 专项测试：15/15 通过。
- 全仓 `unittest discover`：413/413 通过。
- `work/gzbrain_photo_backfill_full.py --validate-full`：`expected=183 downloaded=181 failed=2`，通过。
- FULL payload SHA-256：`99361f1846c88982cb59ae309c63b0bd3b9ab497fd9164f5f4f62e6455e9ad1c`。
- reconciliation SHA-256：`6f28fcc72270389f9b43f8e04b52e2b506b8c66ed88be931567c6398b2c2707d`。
- FULL 报告 SHA-256：`d8c44c7cf1ca239d4020d1fe385b35ba9610e9a22d48e4d8f27d719f3064b6d5`。
- 抽样审计图 SHA-256：`3f6d2454d0a15dc4409c948f4a6338127850fdf178874137c4f9ad9b7be6db3b`。

关键工件：

- `work/gzbrain_photo_backfill_full.py`
- `work/tests/test_gzbrain_photo_backfill_full.py`
- `work/广州医科大学附属脑科医院_photo_backfill_full_payload.json`
- `work/广州医科大学附属脑科医院_photo_backfill_full_reconciliation.csv`
- `work/广州医科大学附属脑科医院_photo_backfill_full_report.md`
- `work/广州医科大学附属脑科医院_photo_backfill_full_audit_sheet.jpg`
- `work/广州医科大学附属脑科医院_photo_backfill_full_visual_review/`（8 页）
- `医生画像仓库/01_试点医院/广州医科大学附属脑科医院/照片/`（181 张）

## FULL 当前停止点

当前阶段为 `FULL_DONE_WAITING_OWNER_FINAL_AUDIT`。只允许提交并以标准 Git 协议 fast-forward 推送当前分支、在 PR #78 发布 `FULL_DONE`；随后等待 Owner 最终审计。不得自行合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #77 广州医科大学附属脑科医院照片补录 FULL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/77
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/78
Branch: codex/mhrj/issue-77-gzbrain-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: FULL_DONE_WAITING_OWNER_FINAL_AUDIT
Completed:
- 固定 183 条完成 181 张官网页面引用原图回填，2 条占位失败留空
- 181 份 AUTO 画像严格 +2/-0；2 份失败画像与 _索引.md 零触碰
- 8 页联系表覆盖 181/181 并逐格目视通过；唯一 >5 MiB 原图单独通过
- 三载体逐值一致；专项 15/15、全仓 413/413、FULL 验证通过
CurrentFacts:
- 正式照片 181 张、70,819,590 bytes；PNG 66、JPEG 115；声明/魔数不一致 18
- 失败为程道猛 ID 877 默认图、梁卉薇 ID 989 小尺寸 BMP，占位证据完整
- Issue #77 与 PR #78 保持 open；当前只等待本提交发布及 Owner 最终审计
Next:
- 精确暂存、提交、fast-forward 推送当前分支
- 在 PR #78 发布 FULL_DONE 后等待 nancywrayg57-jpg 最终审计
Constraints:
- 仅默认 urllib 官方公开 GET；无 Cookie、代理、自定义浏览器头、挑战绕过或第三方来源
- 只采详情页严格容器实际引用的原始字节，不构造或探测页面未引用路径
- 患者及任何患者可识别信息绝对禁止
- 不得合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- work/广州医科大学附属脑科医院_photo_backfill_full_payload.json
- work/广州医科大学附属脑科医院_photo_backfill_full_reconciliation.csv
- work/广州医科大学附属脑科医院_photo_backfill_full_report.md
- work/广州医科大学附属脑科医院_photo_backfill_full_audit_sheet.jpg
- work/广州医科大学附属脑科医院_photo_backfill_full_visual_review/
- 医生画像仓库/01_试点医院/广州医科大学附属脑科医院/照片/
</Handoff_State>

## Owner FULL 终审退回与最小修正

Owner 于 PR #78 对提交 `13ddabc5` 给出 `FULL_AUDIT_REJECTED → FIX_REQUIRED`：<https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/78#issuecomment-5336568337>。除两条纯白占位图外，Owner 明确确认底表范围、181 份原文件三重、画像 `+2/-0`、XLSX/CSV 一致性、程道猛/梁卉薇占位判定、徐文军大图和既有测试均通过，因此本次只重算受两条修正影响的资产，未重新联网抓取或改动其他医生。

根因是既有 `placeholder_response_reason` 只检查 URL path 标记，以及“文件不大于 10 KiB 且宽高均不大于 128”的小尺寸边界。李莹珊（ID 765）与李荷花（ID 766）的同一纯白 JPEG 为 1,147 bytes、148×208，宽高未同时命中旧边界；同时旧联系表使用白底且没有预览框，纯白图片在 page_03 #11/#12 呈不可见空格，人工目视误判为通过。

两条记录的三重证据复算一致：

1. 两文件 SHA-256 均为 `42dac34e29cd304174e89e8552fadacd4a0380b9e3346b9f5c5ebf2393cb96fd`，但属于两个不同医生来源。
2. Pillow 全图解码唯一颜色数为 1，全部像素为 RGBA `(255,255,255,255)`。
3. 两个页面引用 URL 的 query `YmxhbmsyLmpwZw==` Base64 解码均为 `blank2.jpg`。

最小修正如下：

- 删除两张精确命名的正式照片；清空两行 `照片链接`、`照片文件`，追加幂等异常提示 `官网本人职业照补录失败：占位图`。
- 两份画像精确撤销照片块，并以 SHA-256 证明分别恢复为 `b8a1db1eee87f2a87d5b727203f11d485bcda385947bd7cd908ceb5614d8e4da`、`969a27157b9fb9bf83e5acf79fef423f4db3ce7cc70e155c74fcbfe53b77746e`，均与 `origin/main` 一致；`_索引.md` 仍与 `origin/main` 一致。
- 两条 reconciliation 改为“失败留空/占位图”；错误证据含 `resource_urls`、`photo_reference_count`、`observed_utc`，以及跨医生同 SHA、全图纯白单色、query 解码为 `blank2.jpg` 三项检测特征。
- 脚本固化四层门禁：query Base64 解码出现 `blank`/`placeholder`/`default`；全图唯一颜色数不大于 2；不同来源同 SHA 时停止并转人工复判，仅允许 Owner 本次已实审通过的沈峰同人双详情精确白名单；联系表预览格增加灰底和边框，空白/不可见格命中同一门禁时停止。
- 新增 `--fix-owner-rejected-placeholders` 事务模式；只从既有 FULL 状态重建受影响的底表、画像、对账、报告、抽样图和联系表，不重复网络采集。

## 修正后对账与验证

| 固定目标 | 实采成功 | 失败留空 | 正式落盘 | 照片字段留空 |
|---:|---:|---:|---:|---:|
| 183 | 179 | 4 | 179 | 4 |

- 失败四类：详情不可达 0、照片资源不可达 0、无照片容器 0、占位图 4；新增两条与既有程道猛、梁卉薇两条共同构成 4 条占位失败。
- 正式照片 179 张、70,817,296 bytes；PNG 66、JPEG 113；声明/魔数不一致 18；超过 5 MiB 仍仅徐文军一张；超过 20 MiB 为 0。
- 逐单元格变化 362：`照片链接` 179、`照片文件` 179、`异常提示` 4；总底表 payload/CSV/XLSX 逐值一致。
- 179 份 AUTO 画像保持 `+2/-0`；4 份失败画像与 `_索引.md` 零变化；两份退回画像已恢复 `origin/main`。
- FULL 抽样图与 8 页全量联系表已重新生成并逐格目视，覆盖 179/179；全部为单人医生职业照，未见患者、儿童、合影、二维码、装饰、占位或不可见空格。
- XLSX 重新导入确认 6 张工作表齐全，公式错误扫描为 0；6 张预览逐表目视无空白页、破损表头、公式错误文本或明显布局异常。
- FULL 专项测试 19/19；全仓 `unittest discover` 417/417；`--validate-full` 输出 `expected=183 downloaded=179 failed=4`。
- FULL payload SHA-256：`7d6ca4014a34404daa32c5b675c7124d94b30ecf12684b57436d7e3bbcfadb15`。
- reconciliation SHA-256：`f6a5936e74a5e89a7b40fe7baf498a6923dfcfb76c7e722b59a54034a08d45dc`。
- FULL 报告 SHA-256：`0467c390ba4166b8d2d0ae201916eea2bd62c637eef9a6d15df982f3a7b6e4ab`。
- 抽样审计图 SHA-256：`f7e4ce35027a051d7b94c372f0ba1e35214c613119b57dad254c3a8be5ce8f4d`。

当前停止点为 `FULL_FIXED_READY_FOR_OWNER_REAUDIT`。只允许精确暂存、提交、标准 Git fast-forward 推送原分支并在 PR #78 发布 `FULL_FIXED_DONE`；之后等待 Owner 针对受影响面和抽样回归复审。不得自行合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #77 广州医科大学附属脑科医院照片补录 FULL Owner 修正
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/77
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/78
Branch: codex/mhrj/issue-77-gzbrain-photo-backfill-trial
CodexDeveloper: xtzhou247
ClaudeOwner: nancywrayg57-jpg
Phase: FULL_FIXED_READY_FOR_OWNER_REAUDIT
Completed:
- 精确移除李莹珊 ID 765、李荷花 ID 766 两张纯白 blank2.jpg 占位图
- 四数重算为 183 = 179 实采 + 4 占位失败；两份画像恢复 origin/main，索引零触碰
- 固化 query Base64、唯一颜色数、跨医生同 SHA、联系表可见性四层门禁
- 179/179 视觉、XLSX 六表、专项 19/19、全仓 417/417、FULL 验证全部通过
CurrentFacts:
- 正式照片 179 张、70,817,296 bytes；PNG 66、JPEG 113；跨医生重复 SHA 组 0
- 失败为程道猛 ID 877、梁卉薇 ID 989、李莹珊 ID 765、李荷花 ID 766，均留空且证据完整
- Issue #77、PR #78 仍 open；当前等待修正提交发布后 Owner 复审
Next:
- 精确暂存、提交、标准 fast-forward 推送当前原分支
- 在 PR #78 发布 FULL_FIXED_DONE，恢复自动监控并等待 nancywrayg57-jpg 复审
Constraints:
- 仅默认 urllib 官方公开 GET；无 Cookie、代理、自定义浏览器头、挑战绕过或第三方来源
- 患者及任何患者可识别信息绝对禁止
- 不得合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- work/广州医科大学附属脑科医院_photo_backfill_full_payload.json
- work/广州医科大学附属脑科医院_photo_backfill_full_reconciliation.csv
- work/广州医科大学附属脑科医院_photo_backfill_full_report.md
- work/广州医科大学附属脑科医院_photo_backfill_full_audit_sheet.jpg
- work/广州医科大学附属脑科医院_photo_backfill_full_visual_review/
- 医生画像仓库/01_试点医院/广州医科大学附属脑科医院/照片/
</Handoff_State>
