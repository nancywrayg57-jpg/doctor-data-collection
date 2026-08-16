# Issue #59 中山大学肿瘤防治中心照片可得性核验

> 日期：2026-08-16
> GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/59>
> 分支：`codex/mhrj/issue-59-photo-availability-sysucc`
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`

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

## 9. Owner FULL 授权与全量标题普查

Owner 于 PR #60 评论中明确给出 TRIAL `通过`，并切换为 `FULL_APPEND_AND_OBSIDIAN`。有效执行口径为：逐行处理 542 个数字 node；允许保存页面自身引用的 `media_2_3_400_600` 派生图原始响应字节且不压缩；`/taxonomy/term/267` 不访问，照片两列留空并追加“来源非医生详情页，照片不适用”；三载体逐值一致；画像只外科式插入照片区块；详情不可达率超过 10% 熔断。

正式写入前只读普查全部 542 个数字 node：542/542 页面可达且均为 doctor 模板，不可达 0。标题核验一次性固化 15 条仅用于身份校验的别名，不修改底表姓名：

- `/node/3741` 肖祥胜、`/node/1488` 周宁宁、`/node/1482` 李宇红、`/node/1505` 王德深、`/node/1479` 王树森；
- `/node/1485` 王风华、`/node/1475` 黄慧强、`/node/1683` 曹新平、`/node/1658` 刘慧(小)、`/node/3883` 张琳；
- `/node/3723` 秦自科、`/node/3645` 邱际亮、`/node/3612` 杨浩贤、`/node/6668` 刘敏、`/node/1528` 郭灵。

## 10. 首次 FULL 失败、根因与防复发

首次 FULL 在约第 279 行、邓婷 `/node/3706` 处停止。根因不是网络或照片请求失败，而是该既有底表行的科室字段被旧正文污染；原文件名逻辑把超长科室全文直接拼入照片文件名，触发 Windows 路径长度错误。事务尚未交换，正式总底表、画像和照片目录均为零修改。

最小修正为新增 `photo_filename_department`：科室为空或清洗后长度超过 40 字时，仅在照片文件名中使用“未标注”，不修改底表科室字段。542 行普查中仅邓婷一行触发回退；新增回归测试固定该口径。唯一一次授权重试成功完成，未发生第二次 FULL 失败。

防复发措施：所有照片文件名字段必须先做长度与非法字符约束；事务交换前继续验证临时照片集合、三载体、画像外科式差异和受保护资产哈希，任何异常均回滚而不触碰正式目录。

## 11. FULL 结果与正式差异

- 范围闭环：总范围 543；应采数字 node 542；实采 536；失败 6；taxonomy 不适用 1；留空 7；`536 + 6 = 542`、`6 + 1 = 7`、`536 + 7 = 543`。
- 失败三态：详情不可达 3、无照片容器 3、占位图 0。详情不可达率 `3/542 = 0.55%`，未触发 10% 熔断。
- 536 张照片均为页面直接引用的官方职业照响应字节，总计 94,451,923 bytes（90.08 MiB）；最大单张 317,437 bytes；超过 5 MiB 为 0；页面未引用路径构造/探测 0；第三方来源 0。
- payload、CSV、XLSX 均为 543 行、25 列且逐值一致。正式行差异共 1,079 个单元格：`照片链接` 536、`照片文件` 536、`异常提示` 7；其他列零修改。taxonomy 仅追加不适用提示，照片两列保持空白。
- 本院 Markdown 文件保持 544 个，其中 `_索引.md` 1 个、医生画像 543 个。成功实采的 536 个既有画像只新增照片嵌入区块；未新建画像；索引未修改；另 1 个既有范围外来源保持不变。
- 正式照片目录为 536 个文件、94,451,923 bytes；磁盘文件集合、字节、SHA-256、魔数、尺寸与 FULL payload 一致。
- 入口台账 SHA-256 保持 `D6B08B3F284654024FAD0EEAC3377B095025DC294732DB030E8CC5B81655B782`；总底表更新报告 SHA-256 保持 `CD6FFF06B933F4A765838281F52F06F3E1228FCEA37E5D3B4A9441BD8120D96A`。

## 12. 验证与停止点

- `work/sysucc_photo_backfill_trial.py --validate` 通过：536 照片、6 失败、1 不适用。
- Issue #59 专项 unittest 16/16；完整 unittest 218/218 通过。正式写入后将原依赖现场空照片字段的范围测试改为显式构造 TRIAL 前基线副本，生产门禁逻辑不放宽。
- 最终 XLSX 使用指定 `@oai/artifact-tool` 重新导入；6 个工作表齐全，关键范围 `A1:Y12` 可读，公式错误扫描 0，蓝白交替表格样式渲染正常。
- 事务构建、正式交换和回滚门禁均通过；未使用替代 XLSX writer。

当前停止点为 `FULL_READY_FOR_FINAL_OWNER_AUDIT`。工件提交并非强制推送到原 PR #60 后，只等待 owner 最终画像审计；不得自行合并 PR、关闭 Issue 或处理下一 Issue。

<Handoff_State>
Target: Issue #59 中山大学肿瘤防治中心照片补录 FULL
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/59
Branch: codex/mhrj/issue-59-photo-availability-sysucc
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/60
Phase: FULL_READY_FOR_FINAL_OWNER_AUDIT
Completed:
- Owner 已明确审计 TRIAL 通过并切换 FULL_APPEND_AND_OBSIDIAN
- 只读普查 542/542 数字 node 标题并固化 15 条身份校验别名
- 逐行闭环 542+1：实采 536、失败 6、taxonomy 不适用 1、留空 7
- 三载体 543 行 25 列逐值一致；正式差异仅照片两列与 7 行异常提示
- 536 个既有画像仅新增照片区块；不新建画像、不改索引
- 专项 16/16、完整 218/218、FULL validator、照片字节和 XLSX 视觉验证均通过
Next:
- 提交并以 base_tree 分批构造照片 tree，通过非强制 Git Data API 更新原分支与 PR #60
- CI 成功后发布 FULL_READY_FOR_FINAL_OWNER_AUDIT 审计信标
- 恢复自动化并等待 owner 最终画像审计
Constraints:
- 只使用详情页自身引用的官方本人职业照
- 保留 styles 派生图与 itok，不构造或探测原图路径
- taxonomy 不访问；画像只外科式插入照片区块
- 不自行合并 PR、关闭 Issue 或处理下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\sysucc_photo_backfill_trial.py
- D:\workspace\信息收集整理\work\tests\test_sysucc_photo_backfill_trial.py
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_full_payload.json
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_full_reconciliation.csv
- D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_full_report.md
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\中山大学肿瘤防治中心\照片
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-16_issue_59_sysucc_photo_availability.md
</Handoff_State>
