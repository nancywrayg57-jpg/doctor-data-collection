# Issue #57 中山大学附属第三医院照片可得性核验

> 日期：2026-08-16
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/57>
> 分支：`codex/mhrj/issue-57-photo-availability-zssy`
> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`

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

当前停止等待 owner 审计样本、大图分布与容量估算。未取得 owner 明确 `FULL_APPEND_AND_OBSIDIAN` 前，不回填三载体、不刷新画像、不写正式照片目录。

<Handoff_State>
Target: Issue #57 中山大学附属第三医院照片可得性核验
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/57
Branch: codex/mhrj/issue-57-photo-availability-zssy
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/58
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 在首个 owner 预检样本 /node/11100 发现 CSS 背景本人职业照
- 完成浏览器 DOM、普通公开会话、图片响应、SHA-256、魔数和视觉复核
- 按发现照片分支立即停止，正式资产零修改
- Owner 已采纳可得性结论并切换常规 TRIAL
- 完成 10 位、10 科室、四职称层级照片 TRIAL；10/10 实图成功，熔断三态为 0
- 完成逐图字节/SHA-256/魔数/尺寸、容量估算、联系表视觉复核与正式资产零变更对账
Next:
- 提交并通过非强制 Git Data API 更新原分支与 PR #58
- 等待 owner 审计 TRIAL，并明确是否下发 FULL_APPEND_AND_OBSIDIAN
Constraints:
- 只使用详情页自身引用的官方本人职业照
- 不构造或探测页面未引用图片路径
- 未获 FULL 授权前不写总底表、画像或正式照片目录
Artifacts:
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_availability_verify_report.md
- D:\workspace\信息收集整理\work\zssy_photo_backfill_trial.py
- D:\workspace\信息收集整理\work\tests\test_zssy_photo_backfill_trial.py
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_payload.json
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_manifest.csv
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_report.md
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_contact_sheet.jpg
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_photos
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-16_issue_57_zssy_photo_availability.md
</Handoff_State>
