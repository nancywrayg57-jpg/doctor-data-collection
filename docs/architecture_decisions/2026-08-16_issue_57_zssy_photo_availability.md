# Issue #57 中山大学附属第三医院照片可得性核验

> 日期：2026-08-16
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/57>
> 分支：`codex/mhrj/issue-57-photo-availability-zssy`
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`

## 1. 目标与门禁

Issue #57 要求先核验该院官网是否提供医生本人照片。若 30 个详情页与至少 3 个列表模板页均为零照片，则提交跳过证据；若任一页面发现照片，则立即停止并回报呈现方式与样例 URL，由 owner 改下发常规 TRIAL。

## 2. 现场发现

在官网常规会话中打开专家目录后，首个 owner 预检样本 <https://www.zssy.com.cn/node/11100> 即发现张晓红本人职业照：

- 详情页 HTTP 200，浏览器标题为 `张晓红 | 中山大学附属第三医院`。
- 照片不在 `<img>`、`srcset` 或懒加载属性中。
- 关键选择器为 `.physician-details-left .physician-details-media .media-img`。
- 页面用 `data-image-url` 声明相对路径，并在渲染后写入内联 `background-image`。
- 页面引用 URL 为 <https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/2014021909275728200283.jpg>。
- 图片响应为 `200 image/jpeg`，189,270 bytes，SHA-256 为 `35249FDB9C9A2EE3D48FA4E899837607D36B44822175B3253461413C828C7FBD`。
- 视觉复核为单人成人职业照，不是患者、儿童、占位图或通用图。

## 3. 根因与决策

owner 三页预核验遗漏 CSS 背景图，只检查 `<img>`、懒加载等常见图片元素；该站医生照片实际通过 `data-image-url` + `.media-img` 背景图呈现。

依 Issue 的二选一门禁，本轮采用 `PHOTO_FOUND_STOP_FOR_OWNER_TRIAL`：

1. 首个详情样本命中后立即停止；不再访问其余 29 个详情页或其他列表模板页。
2. 不修改总底表三载体、更新报告、画像和照片目录。
3. 不构造或探测页面未引用图片路径。
4. 将命中证据提交原 Issue，等待 owner 切换到常规 TRIAL。

## 4. 可得性核验工件与阶段切换

- 核验报告：`work/中山大学附属第三医院_photo_availability_verify_report.md`
- Owner 于 2026-08-16T11:23:32Z 在 PR #58 采纳发现结论，独立复核张晓红照片的 HTTP、字节与 SHA-256 一致，并将 Issue #57 切换为常规照片 `TRIAL`。
- 新指令固定为 10 位、至少 3 科室并覆盖正高/副高/中级/初级；照片仅取医生详情区页面自身引用 URL，使用常规 Cookie 会话与对应详情页 Referer；TRIAL 不写正式资产。

## 5. Git Data API 推送一致性修正

首次创建远端 commit 时，本地 SHA 一致性门禁发现 GitHub 返回的 commit SHA 与本地不同并停止，远端分支未创建。只读比较证明 tree、父提交、作者、提交者和时间均一致；唯一差异是推送代码对 commit message 使用 `rstrip("\n")`，删除了本地 commit 对象末尾换行，生成孤立 commit `ebce329a…`。

第二次改用 `git show --format=%B`，该命令输出包含两个末尾换行，再次生成 SHA 不同的孤立 commit `511b07ca…`，门禁继续阻止创建 ref。管理员明确授权第三次重试后，最终直接读取 `git cat-file commit HEAD` 原始字节，以首个 `b"\n\n"` 分隔 headers/message，原样保留 message 恰好一个末尾 LF。GitHub 返回 SHA 与本地 `2b68c16a…` 严格一致后才非强制创建远端 ref，并建立 PR #58。

防复发规则：需要复现本地 commit SHA 时，不得依赖格式化输出、裁剪、标准化或重写 commit message；必须从原始 commit object 提取消息字节，并在创建或更新 ref 前执行本地/远端 commit SHA 强一致门禁。

## 6. TRIAL 固定样本与实现

从总底表该院 780 行照片字段为空范围中固定选择 10 位，覆盖 10 个科室与完整职称层级：

| 层级 | 人数 | 样本 |
|---|---:|---|
| 正高 | 3 | 张晓红、张炎、吴玲玲 |
| 副高 | 2 | 李名安、唐新意 |
| 中级 | 2 | 巴俊慧、杨婷 |
| 初级 | 3 | 周攀、黄晓飞、李舣婷 |

新增 `work/zssy_photo_backfill_trial.py` 与专项测试：

1. 从 780 行中只读核验范围、照片空值、来源唯一性与官方数字 node 链接。
2. 只接受 `.physician-details-left` 内唯一 `.physician-details-media .media-img` 的 `data-image-url` 或一致的内联 `background-image`；排除同页“脑病服务、出诊、服务、云上三院、二维码”等通用图。
3. 官网首页建立常规 Cookie 会话，详情页和图片均使用公开页面正常请求；照片请求携带对应详情页 Referer。
4. 实图仅写入 `work/中山大学附属第三医院_photo_backfill_trial_photos`，按 `名字-科室-职称-医院.扩展名` 命名；双语科室选择已有底表中的中文原子，不补造字段。
5. 逐图核验 HTTP、Content-Type、魔数、字节、SHA-256 和尺寸；页面未引用路径构造/探测计数固定为 0。

## 7. TRIAL 结果与大图分布

- 详情页：10/10 HTTP 200；照片下载 10/10 HTTP 200。
- 科室覆盖：10；职称分层：正高 3、副高 2、中级 2、初级 3。
- 熔断三态：详情不可达 0、无照片容器 0、占位图 0；结构异常 0、照片失败 0，问题占比 0%。
- 样本总字节：4,953,604；平均 495,360 bytes。
- 按平均值对 780 行线性估算：386,380,800 bytes，约 368.48 MiB；只用于 owner FULL 裁决，不代表实际最终容量。
- 单张大于 200KB：4/10；宽度大于 800px：6/10。
- 10 个 SHA-256 全部唯一；联系表视觉复核 10/10 均为单人成人职业照，未发现患者、儿童、合影、占位图、站点通用图或二维码。

## 8. 正式资产零变更与验证

- 总底表 payload/CSV/XLSX/更新报告前后 SHA-256 完全一致。
- 本院画像树保持 743 个文件、2,400,787 bytes、SHA-256 `9242708B2A268AFD40AEA54E60B73D04AF97C3C3655B5ECD1415C31E59974D4E`。
- 本院正式照片目录执行前后均不存在；TRIAL 未创建或写入正式照片目录。
- `py_compile` 通过；Issue #57 专项 unittest 9/9 通过；现有完整 unittest 195/195 通过；TRIAL payload validator 通过。

TRIAL 工件：

- `work/中山大学附属第三医院_photo_backfill_trial_payload.json`
- `work/中山大学附属第三医院_photo_backfill_trial_manifest.csv`
- `work/中山大学附属第三医院_photo_backfill_trial_report.md`
- `work/中山大学附属第三医院_photo_backfill_trial_contact_sheet.jpg`
- `work/中山大学附属第三医院_photo_backfill_trial_photos/`

## 9. FULL 前 780 页标题与媒体结构只读普查

Owner 于 2026-08-16T11:49:02Z 在 PR #58 明确给出 TRIAL `通过`、批准页面引用原图原始字节且不压缩，并下发 `FULL_APPEND_AND_OBSIDIAN`。FULL 首轮因官网标题与底表姓名不一致停止；用户随后明确授权“只读普查全部 780 页标题并一次性固化所有别名后继续 FULL”。

只读普查使用同一常规 Cookie 会话逐页访问 780 条既有官网来源链接，只读取详情 HTML，不下载或写入正式照片、底表和画像。结果：

- 范围：780/780；请求失败 0；标题后缀/媒体 DOM 结构异常 0；传输不完整重试 0。
- 媒体结构：本人照片候选 737、无照片容器 38、占位图 5，与后续 FULL 四数轨迹一致。
- 标题不一致共 9 条，完整固化如下；映射只用于来源页身份校验，不修改底表姓名或其他业务字段。

| 来源链接 | 底表姓名 | 官网标题主体 |
|---|---|---|
| <https://www.zssy.com.cn/node/6008> | 内科 | 内科ICU |
| <https://www.zssy.com.cn/node/14062> | 外科 | 外科ICU |
| <https://www.zssy.com.cn/node/14071> | 精神 | 精神（心理）科 |
| <https://www.zssy.com.cn/node/14068> | 口腔科 | 口腔医学中心 |
| <https://www.zssy.com.cn/node/14098> | 变态反应 | 变态反应（过敏）学科 |
| <https://www.zssy.com.cn/node/11316> | 甲状腺 | 甲状腺、乳腺外科 |
| <https://www.zssy.com.cn/node/15410> | 神经外科 | 神经外科（天河） |
| <https://www.zssy.com.cn/node/15466> | 精神 | 精神（心理）科 |
| <https://www.zssy.com.cn/node/30221> | 脑病方向 | 针灸专科（脑病方向） |

根因：原实现只在 FULL 顺序执行时按遇到的第一条未知标题停止，导致别名逐条暴露；同时把“标题别名仅存在于 GOVERN-1 无画像行”当成不成立的前提。完整普查证明新增 3 条别名均属于已有画像来源，但其媒体分别为无照片容器或占位图，因此不会产生错误照片刷新。

防复发：`PAGE_TITLE_ALIAS_BY_SOURCE` 固定完整 9 条；专项测试逐键逐值断言完整映射；别名来源只允许落在 Issue #57 固定 780 行中，不再错误限定为 38 条无画像来源。任一未来未固化标题仍由详情标题强校验停止，而不会静默映射。

## 10. FULL 事务结果

- 四数对账：应采 780、实采 737、失败 43、留空 43。
- 失败三态：详情不可达 0、无照片容器 38、占位图 5；详情不可达率 0%，未触发 10% 熔断。
- 照片总字节 274,074,265（261.38 MiB）；最大单张 2,063,418 bytes；超过 5 MiB 为 0。
- 网络仅使用页面自身引用 URL、常规 Cookie 与对应详情页 Referer；页面未引用路径构造/探测 0，第三方来源 0；发生 1 次 `IncompleteRead`，按完全相同请求原样重试一次后成功。
- 总底表 payload/CSV/XLSX 仍为 9,222 行、25 列逐值一致。允许变更 1,517 个单元格：照片链接 737、照片文件 737、失败行异常提示 43；其余字段零修改。
- 既有画像来源 742 份；其中 737 份只插入照片 Markdown 块，5 份失败来源保持不变；38 条无画像治理行不新建画像；`_索引.md` 未修改。
- 正式照片目录共 737 个文件，磁盘总字节与 FULL payload 对账一致；全部逐文件核验字节数、SHA-256、魔数、扩展名与尺寸。
- 事务先在 `issue57_full_*` 临时目录完成三载体、照片和画像全量验证，再统一替换；成功后临时目录自动清理。

入口台账与更新报告保持受保护基线不变：

- 入口台账 SHA-256：`D6B08B3F284654024FAD0EEAC3377B095025DC294732DB030E8CC5B81655B782`
- 更新报告 SHA-256：`CD6FFF06B933F4A765838281F52F06F3E1228FCEA37E5D3B4A9441BD8120D96A`

## 11. FULL 验证与审计工件

- FULL payload validator 通过；专项 unittest 16/16、完整 unittest 202/202、`py_compile` 与 `git diff --check` 通过。
- artifact-tool 对最终 XLSX 六个工作表执行了关键区域检查、公式错误扫描与逐表视觉渲染；0 个公式错误，样式、表头、行高、冻结窗格和现有布局保持一致。
- 从 737 张正式照片按序等距抽取 20 张做视觉复核，均为单人成人职业照，未发现患者、儿童、合影、二维码、通用图或占位图。

FULL 工件：

- `work/中山大学附属第三医院_photo_backfill_full_payload.json`
- `work/中山大学附属第三医院_photo_backfill_full_reconciliation.csv`
- `work/中山大学附属第三医院_photo_backfill_full_report.md`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.csv`
- `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.xlsx`
- `医生画像仓库/01_试点医院/中山大学附属第三医院/照片/`

当前已到达 `FULL_READY_FOR_FINAL_OWNER_AUDIT` 停止点；等待 owner 最终画像审计、PR 合并与 Issue 关闭，不自行进入下一 Issue。

<Handoff_State>
Target: Issue #57 中山大学附属第三医院照片补录 FULL
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/57
Branch: codex/mhrj/issue-57-photo-availability-zssy
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/58
Phase: FULL_READY_FOR_FINAL_OWNER_AUDIT
Completed:
- 在首个 owner 预检样本 /node/11100 发现 CSS 背景本人职业照
- 完成浏览器 DOM、普通公开会话、图片响应、SHA-256、魔数和视觉复核
- 按发现照片分支立即停止，正式资产零修改
- Owner 已采纳可得性结论并切换常规 TRIAL
- 完成 10 位、10 科室、四职称层级照片 TRIAL；10/10 实图成功，熔断三态为 0
- 完成逐图字节/SHA-256/魔数/尺寸、容量估算、联系表视觉复核与正式资产零变更对账
- Owner 明确 TRIAL 通过并下发 FULL_APPEND_AND_OBSIDIAN
- 只读普查 780/780 页并一次性固化完整 9 条标题别名；请求失败和结构异常均为 0
- FULL 四数闭环为 780/737/43/43；失败三态为 0/38/5，正式照片 274,074,265 bytes
- 总底表三载体 9,222 行、25 列逐值一致；仅照片两列和 43 条失败异常提示变化
- 外科式刷新 737/742 份既有画像；38 条无画像行不新建，索引不变
- 完成逐图哈希/魔数/尺寸、全量测试、六工作表视觉检查与受保护资产哈希核验
Next:
- 提交并通过非强制 Git Data API 更新原分支与 PR #58
- 在 PR #58 留下 `FULL_READY_FOR_FINAL_OWNER_AUDIT` 审计信标
- 等待 owner 最终画像审计、PR 合并与 Issue 关闭
Constraints:
- 只使用详情页自身引用的官方本人职业照
- 不构造或探测页面未引用图片路径
- 不自行合并 PR、关闭 Issue 或处理下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_availability_verify_report.md
- D:\workspace\信息收集整理\work\zssy_photo_backfill_trial.py
- D:\workspace\信息收集整理\work\tests\test_zssy_photo_backfill_trial.py
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_payload.json
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_manifest.csv
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_report.md
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_contact_sheet.jpg
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_photos
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_full_payload.json
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_full_reconciliation.csv
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_full_report.md
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\中山大学附属第三医院\照片
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-16_issue_57_zssy_photo_availability.md
</Handoff_State>
