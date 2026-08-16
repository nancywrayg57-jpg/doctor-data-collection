# Issue #59 中山大学肿瘤防治中心照片可得性核验

> 日期：2026-08-16
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/59>
> 分支：`codex/mhrj/issue-59-photo-availability-sysucc`
> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`

## 1. 目标与门禁

Issue #59 要求从该院 543 条既有来源链接抽取 30 个详情页，覆盖至少 10 个科室、职称分层和全部发现的页面模板变体，并核验至少 3 个列表模板页。若零照片则提交完整普查清单；若任一页面发现本人照片，则立即停止并回报呈现方式与样例 URL，由 owner 改下发常规照片 TRIAL。

## 2. 现场发现

普通公开会话访问首个 owner 预检样本 <https://www.sysucc.org.cn/node/3795> 时，详情原始 HTML 明确包含夏忠军本人照片：

- 页面标题：`夏忠军 | 中山大学肿瘤防治中心`。
- 页面模板：`body.page-node.page-node-type-doctor`。
- 医生照片位于 `.title-4-0 .item-media`，使用标准 `<img src>`。
- 页面引用 URL：<https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2023-04/xiazhongjun-xyzlk-202304.jpg?itok=a1jWIC9q>。
- 图片响应：`200 image/jpeg`，182,399 bytes，400×600。
- SHA-256：`C1EB82D91D0E2F04C3FD122DBACDB89AE433952CCE2FF200A88CE0A49E7FB829`。
- 视觉复核：穿白大褂的单人成人职业照，胸前为中山大学肿瘤防治中心标识；不是患者、儿童、合影、占位图、二维码或公共装饰图。

## 3. 根因与决策

Owner 预检称 `/node/3795` 与 `/node/3678` 仅命中公共装饰图 `2022-11/Bitmap.png`。现场原始 HTML 同时存在医生内容区标准 `<img src>`，证明预检结果漏掉 `.item-media` 医生照片。缺少 owner 扫描脚本，当前只记录证据差异，不推断更具体实现原因。

依 Issue 二选一门禁，本轮采用 `PHOTO_FOUND_STOP_FOR_OWNER_TRIAL`：

1. 取消后续 30+3 页零照片普查；
2. 不修改总底表、更新报告、画像和正式照片目录；
3. 不构造或探测页面未引用路径；
4. 等待 owner 切换到常规照片 TRIAL。

首轮固定结构诊断批次在返回首个命中前已完成 4 个详情页及 1 个底表既有 taxonomy 来源页。4 个详情页均命中同一照片结构。防复发措施：后续同类照片可得性核验必须在请求循环内部发现照片即 `break`，不得等待固定批次全部结束后再判定停止。

## 4. 工件与验证

- 核验报告：`work/中山大学肿瘤防治中心_photo_availability_verify_report.md`
- 临时视觉样本仅保存在系统临时目录，不纳入正式资产或 Git 工件。
- 仅官网公开来源；常规 Cookie 会话；第三方来源 0；页面未引用路径构造/探测 0。
- 正式数据资产零修改。

## 5. Owner 采纳与 TRIAL 切换

Owner 于 2026-08-16T14:51:16Z 在 PR #60 独立复核夏忠军照片的 HTTP、字节与 SHA-256 一致，采纳 `PHOTO_FOUND_STOP_FOR_OWNER_TRIAL` 结论，并将 Issue #59 切换为常规照片 `TRIAL`。

Owner 同时定位其原零照片预判根因：预核验 grep 正则 `[^\">]*` 在引号处截断，抓到属性名但抓不到 `src="URL"` 引号内的值。Codex 的固定结构诊断批次与“发现后循环内立即 break”防复发措施获认可。

TRIAL 固定要求为：10 位、至少 3 科室、职称分层、全部发现模板变体；只取 `.item-media` 页面自身引用 URL，保留派生图 `itok`，使用常规 Cookie 与详情页 Referer；交付实图、联系表、命名清单、逐图字节/SHA-256/魔数/尺寸、平均大小、543 行容量估算及派生图/原图说明。TRIAL 不写正式资产。

## 6. TRIAL 实现与固定样本

新增 `work/sysucc_photo_backfill_trial.py` 与专项测试，执行边界如下：

1. 从总底表只读锁定本院 543 行；照片两列全部为空，来源链接 543 个且唯一。范围中已知存在 1 条非数字 node 来源 `/taxonomy/term/267`，本轮不把该非医生来源纳入 10 位 TRIAL，FULL 前必须继续显式留痕处理。
2. 固定样本为夏忠军、李力人、吴锡文、张玉晶、张翼鷟、张伟光、刘方杰、何霞、刘卓炜、夏建川；覆盖 10 个科室/口径，其中正高 4、副高 5、其他 1，并覆盖主任医师、副主任医师、副主任技师、一级主任医师、教授与官网未标注职称。
3. 样本包含 owner 两个预检页 `/node/3795`、`/node/3678`，以及低/高 node ID、医技职称和异常字段页。
4. 只接受 `body.page-node-type-doctor > .title-4-0 .item-media img` 中页面直接引用的同站图片；标题必须与底表姓名一致。所有 URL 均逐字保留，未构造原图路径。
5. TRIAL 图片只写 `work/中山大学肿瘤防治中心_photo_backfill_trial_photos`，按 `名字-科室-职称-医院.扩展名` 命名；官网未展示的张玉晶科室与职称使用 `未标注`，不推断补造。

## 7. TRIAL 结果与大图政策证据

- 详情页 10/10 HTTP 200；照片 10/10 HTTP 200；无照片容器 0、占位图 0、结构异常 0、下载失败 0，熔断问题占比 0%。
- 发现模板只有 `body.page-node-type-doctor > .title-4-0 .item-media img` 一种，10/10 全覆盖，照片引用属性均为标准 `src`。
- 10/10 页面直接引用 `media_2_3_400_600` 派生图，均保留原 `itok`；直接引用原图 0，页面未引用路径构造/探测 0，第三方来源 0。
- 10 张均为 400×600 JPEG，总字节 1,766,318，平均 176,631 bytes；按平均值对 543 行线性估算 95,910,633 bytes，约 91.47 MiB。
- 单张大于 200KB 为 2/10，宽度大于 800px 为 0/10。10 个 SHA-256 全部唯一。
- 联系表人工视觉复核 10/10 均为单人成人职业照；未发现患者、儿童、合影、占位图、二维码或公共装饰图。
- 按 owner 明示的眼科中心判例，本轮提交页面直接引用派生图原始响应字节供预期批准；是否允许 FULL 仍等待 owner 唯一裁决。

## 8. 正式资产零变更与验证

- 总底表 payload/CSV/XLSX、更新报告和入口台账执行前后 SHA-256 完全一致。
- 本院画像树保持 544 个文件、2,591,214 bytes、SHA-256 `BD425998EF8B1D8B616D1521370A218DAE698404B80EE37C396D2C8C9FA81A7C`。
- 本院正式照片目录执行前后均不存在；TRIAL 未写总底表、正式画像或正式照片目录。
- `py_compile` 通过；Issue #59 专项 unittest 9/9、完整 unittest 211/211 通过；TRIAL payload validator 与逐图字节/SHA-256/魔数/尺寸复核通过。

当前停止点为 `TRIAL_READY_FOR_OWNER_AUDIT`。在 owner 明确给出 `通过` / `有条件通过` 并切换为 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填三载体、刷新画像或写正式照片目录。

<Handoff_State>
Target: Issue #59 中山大学肿瘤防治中心照片补录 TRIAL
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/59
Branch: codex/mhrj/issue-59-photo-availability-sysucc
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/60
Phase: TRIAL_READY_FOR_OWNER_AUDIT
Completed:
- 在首个 owner 预检样本 /node/3795 发现标准 img src 本人职业照并完成可得性停止点
- Owner 已采纳发现结论、定位原 grep 漏检根因并切换常规照片 TRIAL
- 完成 10 位、10 科室/口径、正高/副高/其他分层照片 TRIAL
- 10/10 详情与照片成功，熔断三态为 0；全部为页面自身引用的 400×600 派生图
- 完成逐图字节/SHA-256/魔数/尺寸、命名清单、容量估算和联系表视觉复核
- 正式数据资产零修改
Next:
- 提交并以非强制 Git Data API 更新原分支与 PR #60
- CI 成功后发布 TRIAL_READY_FOR_OWNER_AUDIT 审计信标
- 等待 owner 裁决派生图政策与 FULL_APPEND_AND_OBSIDIAN
Constraints:
- 只使用详情页自身引用的官方本人职业照
- 保留 styles 派生图与 itok，不构造或探测原图路径
- 不自行进入 FULL、合并 PR、关闭 Issue 或处理下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_availability_verify_report.md
- D:\workspace\信息收集整理\work\sysucc_photo_backfill_trial.py
- D:\workspace\信息收集整理\work\tests\test_sysucc_photo_backfill_trial.py
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_trial_payload.json
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_trial_manifest.csv
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_trial_report.md
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_trial_contact_sheet.jpg
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_trial_photos
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-16_issue_59_sysucc_photo_availability.md
</Handoff_State>
