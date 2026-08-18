# 2026-08-19 Issue #77 广州医科大学附属脑科医院照片补录 TRIAL

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
