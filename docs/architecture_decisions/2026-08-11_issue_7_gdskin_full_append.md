# 2026-08-11 Issue #7 南方医科大学皮肤病医院全量追加与画像

## 目标与门禁

Claude owner 在 PR #8 评论中给出 `有条件通过` 并明确下发 `FULL_APPEND_AND_OBSIDIAN`：

- 审计评论：`https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/8#issuecomment-5254355944`
- 工作分支：`codex/mhrj/issue-7-gdskin-trial`
- 当前 Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/7`
- 当前 PR：`https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/8`
- 当前状态：`WAITING_CLAUDE_PROFILE_AUDIT`

本轮只处理 Issue #7；不得领取其他 Issue，不得自行批准或合并 PR。

## Claude 六项条件落地

1. 全量唯一医生 77 位，与试采普查基线一致；偏离写入前门禁未触发。
2. 同一详情同时属于荣誉分组与真实科室时优先真实科室。仅存在于“首席专家/知名专家”入口的文海泉、杨斌、陈永锋、顾有守，官网未展示当前院内科室，科室留空并写入 `科室需人工复核`，未作推断。
3. 10 个入口分页数为 `1、1、2、1、1、1、1、1、1、1`；906 完整读取两页。
4. 924 保留零记录入口留痕，未写入医生记录。
5. 异常提示原样入库：仅 4 条 `科室需人工复核`。
6. 李畅畅、熊明洲、王成、赵培祯的官网页面没有显式专长/擅长标签，`擅长诊疗方向摘录` 与画像“简介/擅长”区块保持空白；学历、科研、论文正文分别进入对应证据区块。

## 全量采集与总底表结果

- 入口唯一详情数：`1、3、29、7、8、14、6、4、5、0`。
- 入口候选关系：77；唯一候选：77；跨入口重复：0。
- 排除非医生：`王辉 主管护师` 1 位。
- 列表失败：0；详情失败：0；非官方来源：0。
- 新增医生：77；重复跳过：0。
- 统一总底表：2,088 行增至 2,165 行。
- 目标医院：77 行、77 个唯一官网详情 URL。
- 既有 2,088 行逐字段变化：0。
- 单院 payload、总 payload、CSV 的目标医院 77 行逐字段差异：0（排除作用域不同的 `序号` 后比较）。
- XLSX `自动采集底表` 2,165 行 × 23 列与总 payload 逐单元格差异：0；公式错误扫描 0。

## Obsidian 画像结果

- 仅处理南方医科大学皮肤病医院，未补生成其他医院历史缺口。
- 医生画像：77 份。
- `_索引.md`：1 份，唯一画像链接 77 个，缺失链接 0。
- 跳过记录：0。
- 异常提示不为空：4。
- 可选证据区块命中画像数：教育与进修 61、科研项目与成果 49、论文与学术产出 52。
- 每份画像的官网来源集合与总底表 77 个来源完全一致。
- 每个可选区块均满足“有官网正文证据才渲染、无证据不渲染”，差异 0。
- 4 份无显式专长页面的“简介/擅长”区块保持空白，未使用列表姓名/职称或履历正文兜底。

## 核心资产哈希

| 资产 | SHA-256 |
|---|---|
| 总底表 XLSX | `95503CADE849592F13750D3F8AB059E5253CBA4CAEBBE0B9A2B1442D671916B1` |
| 总底表 CSV | `469BD3F30A51F3D62C954B749FD04929F7E6F0269A781193347660CDD83DFA83` |
| 总 payload | `7A4DB2080093A572F85000DDE2D71D834CA3EEC69D6E7E10C4A1978704439499` |
| 总底表更新报告 | `56B4ADD35D38C3DB26E7B0A422E56A12ED70D3C18704A2362460535735644DD6` |
| 本院正式 payload | `996B181149280D32B69890C004925AC51DB1E8C7C1DC194379DF3165C902A0E7` |
| 本院画像生成报告 | `CD498AB4AD8E05DFDD8820EA213942AAD6996B19B4FF748770842530ECE7E669` |

## 验证结果

- Python 编译通过。
- 采集器与画像生成器共 28 项测试全部通过。
- `git diff --check` 通过。
- XLSX 六个工作表完成修改前后视觉对照；样式、表头、冻结行、统计表和长文本换行无本轮回归。
- XLSX 公式错误扫描 0。
- 试采 CSV/payload/报告已在 owner 审计完成后按 FULL 指令清理；可从 PR #8 早期提交恢复。

## 阻塞、根因、解决方法与防复发

### 1. Python 运行时依赖不完整

- 根因：Windows `python.exe` 是 Microsoft Store 占位符；bundled Python 缺少 `requests` 与 `beautifulsoup4`。
- 解决：复用 Issue #5 已保存的用户临时依赖目录，通过 `PYTHONPATH` 配合 bundled Python；未安装机器级依赖。
- 预防：先核验解释器绝对路径与依赖导入，不依赖 `python` 命令名。

### 2. Spreadsheet Node 依赖入口缺失

- 根因：仓库没有本地 `node_modules`，工作簿生成器无法解析 `@oai/artifact-tool`。
- 解决：创建被 Git 忽略的本地 junction，指向 Codex bundled `node_modules`。
- 预防：写表前先验证 artifact-tool 依赖入口；junction 不进入提交。

### 3. 多入口参数传递错误

- 根因：`--entry-url` 使用 `action=append`，每个入口必须重复传入参数名。
- 解决：用 PowerShell 参数数组逐入口追加 `--entry-url` 与 URL。
- 预防：后续多入口命令统一由数组生成，不手工拼接位置参数。

### 4. 荣誉分组被误当作科室

- 根因：4 位医生只存在于 901/902 荣誉入口，没有真实科室分类；初始全量写入前门禁因此拦截。
- 解决：真实科室分类优先；仅荣誉入口时科室留空并标记人工复核，入口普查仍保留来源类目。
- 预防：GDSKIN 全量写入前强制校验入口计数、分页、失败数、排除数及“首席/知名专家”科室残留。

### 5. 无标签正文进入职称与擅长区块

- 根因：4 个详情页没有“专长/简介”标签，压平正文被当作职称；画像生成器又用列表简介兜底擅长。
- 解决：以“毕业于/从事”等履历标记切分职称与正文；擅长只认显式字段，不再用列表简介或履历兜底。
- 预防：单元测试覆盖无标签详情的职称、擅长、学历科研论文三类归位，并在画像验收中检查空擅长区块。

### 6. 验证器标识符口径不一致

- 根因：排除项预期写成姓名 `王辉`，正式 payload 保存完整列表原文 `王辉 主管护师`。
- 解决：验证器按完整官方列表标题核对。
- 预防：排除项同时区分规范姓名与官方原文，不把验证器口径错误当作业务数据缺陷。

### 7. Git Data API 上传文本对象时 blob SHA 不一致

- 根因：Windows 工作树对部分已提交文本执行 CRLF 展开；直接从工作文件读取字节并上传时，远端生成的 blob SHA 与 Git 索引中的 LF 规范化 blob SHA 不一致。
- 解决：在创建远端 tree 前按 Git 索引记录的 blob SHA 从本地对象库读取原始字节，逐对象上传并校验返回 SHA；任一 SHA 不一致即停止，不更新远端引用。
- 预防：Git Data API 推送统一以提交对象为数据源，不以工作树文件字节为数据源；创建 tree 后还必须核验远端 tree 与本地提交 tree 完全一致，再执行非强制引用更新。

### 8. Git Data API 提交信息被序列化为数组

- 根因：PowerShell 将原生命令的多行标准输出解析为字符串数组；对 `git log --pretty=%B` 结果直接调用 `Trim()` 后仍为数组，GitHub commit API 因 `message` 不是字符串而拒绝请求。
- 解决：创建请求前显式合并并转换为单一字符串，同时本地反序列化 JSON 复核 `message` 类型，再调用 commit API。
- 预防：所有 Git Data API 请求在远端写入前先做本地 Schema 类型检查，尤其核验 `message`、`sha`、`parents` 与 `force` 的标量/数组类型。

## 当前结论与下一步

Issue #7 的 `FULL_APPEND_AND_OBSIDIAN` 已完成。下一步只允许：精确提交并推送本轮全量工件，在 PR #8 请求 Claude 对最终画像给出明确审计结论。只有“最终画像审计通过”且“PR #8 已合并并关闭”同时满足后，才允许领取下一 Issue。

<Handoff_State>
Target: Issue #7 南方医科大学皮肤病医院最终画像审计
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/7
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/8
Phase: WAITING_CLAUDE_PROFILE_AUDIT
Completed:
- 已全量采集并追加 77 位医生，总底表 2165 行
- 已生成 77 份本院画像和 77 个索引链接
- 已完成 28 项测试、跨资产逐字段对账和 XLSX 逐单元格/视觉验证
CurrentFacts:
- 入口计数 1/3/29/7/8/14/6/4/5/0，列表/详情失败 0
- 4 位仅荣誉入口医生科室留空并保留复核提示
- 4 位无显式擅长页面擅长区块留空，学历科研论文证据保留
Next:
- 提交并推送当前分支
- 请求 Claude 最终画像审计
- 审计通过且 PR 合并关闭前不得领取其他 Issue
Constraints:
- 仅医院官网公开渠道
- 不自行批准或合并 PR
- 不领取其他 Issue
Artifacts:
- work/南方医科大学皮肤病医院_official_doctors_payload.json
- 医生画像仓库/01_试点医院/南方医科大学皮肤病医院/
- 医生画像仓库/99_资料来源/南方医科大学皮肤病医院_Obsidian画像生成报告.md
</Handoff_State>
