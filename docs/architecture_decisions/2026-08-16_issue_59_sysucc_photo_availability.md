# Issue #59 中山大学肿瘤防治中心照片可得性核验

> 日期：2026-08-16
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/59>
> 分支：`codex/mhrj/issue-59-photo-availability-sysucc`
> Phase：`PHOTO_FOUND_STOP_FOR_OWNER_TRIAL`

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

## 5. 后续 Agent 最小上下文

Issue #59 已在首个 owner 样本发现标准 `<img src>` 本人职业照。新会话应先读取本 ADR、Issue #59 与其关联 PR 的 owner 评论；在 owner 明确切换常规照片 `TRIAL` 前，不继续采样、不下载正式照片、不回填底表或画像。

<Handoff_State>
Target: Issue #59 中山大学肿瘤防治中心照片补录
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/59
Branch: codex/mhrj/issue-59-photo-availability-sysucc
Phase: PHOTO_FOUND_STOP_FOR_OWNER_TRIAL
Completed:
- 在首个 owner 预检样本 /node/3795 发现标准 img src 本人职业照
- 完成页面标题、DOM 归属、图片响应、SHA-256、魔数、尺寸和视觉复核
- 按发现照片分支停止，正式资产零修改
Next:
- 提交并推送核验报告与本 ADR
- 创建关联 PR 并等待 owner 切换常规照片 TRIAL
Constraints:
- 只使用医院官网页面自身引用的公开资源
- 不构造或探测页面未引用图片路径
- 不自行进入 TRIAL、FULL 或下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_availability_verify_report.md
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-16_issue_59_sysucc_photo_availability.md
</Handoff_State>
