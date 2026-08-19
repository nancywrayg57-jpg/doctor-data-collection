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
