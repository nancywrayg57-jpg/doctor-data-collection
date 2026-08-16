# Issue #57 中山大学附属第三医院照片可得性核验

> 日期：2026-08-16
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/57>
> 分支：`codex/mhrj/issue-57-photo-availability-zssy`
> Phase：`PHOTO_FOUND_WAITING_FOR_OWNER_TRIAL`

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

## 4. 工件与下一步

- 核验报告：`work/中山大学附属第三医院_photo_availability_verify_report.md`
- 下一步唯一有效指令：owner 在 Issue #57 或关联 PR 中明确下发常规照片 TRIAL。
- 在阶段切换前，Codex 保持停止，不进行正式照片下载或资产回填。

## 5. Git Data API 推送一致性修正

首次创建远端 commit 时，本地 SHA 一致性门禁发现 GitHub 返回的 commit SHA 与本地不同并停止，远端分支未创建。只读比较证明 tree、父提交、作者、提交者和时间均一致；唯一差异是推送代码对 commit message 使用 `rstrip("\n")`，删除了本地 commit 对象末尾换行。

最小修正为向 Git Data API 原样传递 `%B` 的完整消息字节，包括末尾换行。防复发规则：后续需要复现本地 commit SHA 时，不得裁剪、标准化或重写 commit message；创建 ref 前必须继续执行本地/远端 commit SHA 强一致门禁。

<Handoff_State>
Target: Issue #57 中山大学附属第三医院照片可得性核验
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/57
Branch: codex/mhrj/issue-57-photo-availability-zssy
Phase: PHOTO_FOUND_WAITING_FOR_OWNER_TRIAL
Completed:
- 在首个 owner 预检样本 /node/11100 发现 CSS 背景本人职业照
- 完成浏览器 DOM、普通公开会话、图片响应、SHA-256、魔数和视觉复核
- 按发现照片分支立即停止，正式资产零修改
Next:
- 提交并推送核验报告与 ADR
- 等待 owner 改下发常规照片 TRIAL
Constraints:
- 不继续 30+3 零照片普查
- 不构造或探测页面未引用图片路径
- 不写总底表、画像或正式照片目录
Artifacts:
- D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_availability_verify_report.md
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-16_issue_57_zssy_photo_availability.md
</Handoff_State>
