# 2026-08-13 Issue #39 中山大学附属第一医院黄埔院区 VERIFY_SKIP

## 目标与执行边界

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/39
- 工作分支：`codex/mhrj/issue-39-fahsysu-huangpu-verify-skip`
- Phase：`VERIFY_SKIP_AWAITING_OWNER_AUDIT`
- 台账序号：8
- 医院：中山大学附属第一医院黄埔院区（别名：中山大学附属第一医院东院）
- 官网首页：https://www.fahsysu.org.cn/home
- Issue 指定医生目录：https://www.fahsysu.org.cn/page/6945
- 人工复核：确认可采集；owner 初裁为“若无独立黄埔/东院目录，则与序号 7 同源已全量覆盖并跳过”

本 Issue 是轻量官网核验任务，不是医生试采。仅允许沿 `fahsysu.org.cn` 官网首页、可见导航和院区栏目核验是否存在黄埔院区/东院专属医生或专家目录；不得构造搜索、猜测路径、越域、采集医生详情、写总底表或生成画像。若发现独立目录必须熔断回报，由 owner 按 PR #38 的 860-ID 基线裁决增量方案。

## 官网只读核验证据

1. 官网首页 `https://www.fahsysu.org.cn/home` 返回 HTTP 200。可见导航中的“专家介绍”和“更多专家”均指向公共目录 `https://www.fahsysu.org.cn/page/6945`。
2. 公共目录 `https://www.fahsysu.org.cn/page/6945` 返回 HTTP 200；页面正文“黄埔”“东院”“院区”均为 0。该目录就是 Issue #37 / PR #38 已全量对账并入库的 860 个唯一 node ID 来源。
3. 首页可见院区入口“中山大学附属第一医院东院”指向官方子域 `http://dongyuan.fahsysu.org.cn/`。沿该已声明链接访问后，服务器跳转至院内页面 `http://www.fahsysu.org.cn/basic/35413`；HTTPS 规范地址 `https://www.fahsysu.org.cn/basic/35413` 返回 HTTP 200，标题为《关于东院改扩建期间相关业务告知书》。
4. 告知书正文明确：“东院改扩建期间，暂停所有服务”。该页面可见“专家介绍”仍只指向同一公共目录 `https://www.fahsysu.org.cn/page/6945`，未声明东院或黄埔专属医生目录。
5. 官网首页出现的“黄埔”命中是《规划床位1200张！中山一院脑科学中心在黄埔动工》新闻链接，不是院区医生/专家目录；本轮未访问新闻外链，未据新闻推断医生归属。

结论：在 Issue 授权的官网首页、可见导航和院区栏目范围内，没有发现独立黄埔院区/东院医生或专家目录；唯一专家入口仍为序号 7 已全量入库的 `/page/6945`。因此执行 owner 预裁的“跳过-同源已覆盖”路径，避免重复入库。

## 台账最小修改

- 文件：`医生画像仓库/99_资料来源/珠三角三甲医院官网入口台账.xlsx`
- 工作表：`入口台账`
- 目标：序号 8、中山大学附属第一医院黄埔院区，对应 `V9`（`人工复核结果`）
- 修改前：`确认可采集`
- 修改后：`跳过-与序号7同源目录已全量入库`

使用 `@oai/artifact-tool` 导入原工作簿，先渲染原格式，再仅改 `V9` 后导出。对源/输出全部工作表逐单元格比较：唯一值差异为 `入口台账!V9`，公式差异 0；公式错误扫描 0。入口台账 A:X 目标行及其余 4 张工作表均完成视觉通览，未发现破损、错列或不可读内容。

## 阻塞、根因、解决与防复发

### 1. 初始 Issue 缺少显式领取字段

- 现象：Issue 初始指令包含医院与公共目录背景，但没有显式 `OfficialHomeURL`、`DoctorDirectoryURL` 和 `ReviewStatus` 字段，不满足自动领取门禁。
- 根因：轻量 `VERIFY_SKIP` 指令沿用了非常规任务描述，没有完全使用通用 READY 字段模板。
- 解决：保持未领取、未建分支、未执行官网核验；owner 随后在 Issue 评论补齐完整字段，再重新通过唯一 Issue、身份、PR、分支和工作区门禁后领取。
- 防复发：任何 Phase（包括轻量 VERIFY_SKIP）都必须显式给出 Status、Phase、Hospital、OfficialHomeURL、DoctorDirectoryURL、ReviewStatus、完整 Task 与范围边界；不得从背景段落推断缺失字段。

### 2. 首次预览未覆盖实际修改列

- 现象：初次渲染范围只到 T 列，实际目标单元格 `V9` 未显示，因此不能据该图片声明视觉验收完成。
- 根因：预览脚本为控制宽度使用了 20 列上限，但台账实际有 24 列，`人工复核结果` 位于 V 列。
- 解决：将目标预览扩展为 A:X，重新渲染；同时对 5 张工作表分别渲染通览，并用源/输出逐单元格比较锁定唯一修改。
- 防复发：先定位目标列，再按目标列和工作表真实 used range 决定渲染范围；任何修改单元格必须出现在至少一张最终预览中，不能以邻近区域代替。

### 3. 恢复发布时工作簿复验运行时不可直接复用

- 现象：恢复到发布检查点后，系统 `PATH` 中没有 `node`；改用 Codex 捆绑 Node 后，位于临时目录根的验证脚本又无法解析 `@oai/artifact-tool`。随后用 `git archive --format=tar` 提取基线工作簿时，Windows `tar` 未正确落地中文路径。
- 根因：捆绑 Node 不保证进入交互 shell 的 `PATH`；ESM 依赖解析从脚本所在目录向上查找，不会使用另一个临时目录中的 `node_modules` junction；Windows tar 链路对本轮 Git 归档中的中文路径不可靠。
- 解决：通过 Codex workspace dependency loader 重新取得固定 Node 与依赖路径，在已具备 `node_modules` junction 的专用 runtime 目录执行同一验证脚本；基线改由 `git archive --format=zip` 生成并使用 PowerShell `Expand-Archive` 解包。最终再次确认 5 张表不变、唯一值差异为 `入口台账!V9`、公式差异为 0，并完成 5 张表视觉通览。
- 防复发：电子表格恢复执行时先加载 workspace dependencies，并从带 junction 的 conversation-specific runtime 目录运行 `.mjs`；中文路径的 Git 基线优先使用 ZIP + `Expand-Archive`，不要依赖系统 `node` 或 Windows tar 的隐式编码行为。运行时/归档故障只按环境诊断处理，不重做已验收的工作簿编辑，也不扩大仓库变更范围。

### 4. Git 暂存路径断言误判中文文件名

- 现象：两个授权文件已成功暂存，但发布保护脚本用 `git diff --cached --name-only` 的默认输出与中文原路径直接比较时，将 Git 的八进制转义路径误判为非目标文件，因此在提交前主动中止。
- 根因：Git 默认 `core.quotePath=true`，非 ASCII 路径会被引号和八进制字节序列表示，不适合直接与 PowerShell 中的 Unicode 路径字符串比较。
- 解决：保留暂存结果、不提交，补记本条记录后重新暂存 ADR；路径白名单校验改用 `git -c core.quotePath=false diff --cached --name-only`，随后再检查 staged 文件数、精确路径和 `git diff --cached --check`。
- 防复发：所有含中文路径的 Git 白名单断言必须显式关闭 quotePath 或使用 NUL 分隔的原始路径解析；不得把 Git 的展示层转义文本当成真实路径。

### 5. PowerShell 误解析 Git peel revision 且未自动熔断

- 现象：远端写入前的摘要命令直接使用 `git rev-parse HEAD^{tree}`，PowerShell 将花括号表达式拆解，Git 报出 ambiguous argument；同时 `$ErrorActionPreference='Stop'` 没有自动把该原生程序非零退出码转为终止错误，脚本仍打印了误导性的 `READY` 摘要。远端尚未开始写入。
- 根因：Git peel revision 在 PowerShell 中未整体加引号；原生可执行文件退出码与 PowerShell cmdlet 异常不是同一错误通道。
- 解决：不采信该摘要并停止远端步骤；将 revision 写为 `git rev-parse 'HEAD^{tree}'`，对关键原生命令逐项检查 `$LASTEXITCODE`，再重新核验身份、Issue、分支、干净工作区、父提交、tree 和远端 ref 不存在。
- 防复发：PowerShell 中所有含 `{}`、`^` 等元字符的 Git revision 必须作为单独的引号参数；发布门禁不得只依赖 `$ErrorActionPreference`，必须对 Git/GitHub CLI 的关键调用显式检查退出码和预期输出。

### 6. Git Data API 发布后的本地同步遇到 PowerShell 插值与消息换行差异

- 现象：远端 blob、tree、commit 和新 ref 均已成功创建且 tree/parent 正确，但首次 fetch refspec 中的 `$branch:` 被 PowerShell 识别为带作用域变量，造成分支值丢失；修正 fetch 后，本地提交与 GitHub API 提交的 SHA 不同，初始消息比较也因末尾换行数量不同而中止。
- 根因：双引号字符串中的变量名后直接跟冒号会触发 PowerShell 作用域语法；Git Data API 接收的 message 在发布脚本中经过 `TrimEnd`，而本地 `git commit` 对象保留了额外终止空行，因此内容树相同但 commit SHA 不同。
- 解决：refspec 改用 `${branch}` 明确变量边界；fetch GitHub 实际对象后逐项比较 tree、唯一 parent、作者/提交者、时间戳与规范化后的 message，并用 Base64 显示确认差异只是一行额外的 CRLF。确认语义对象一致且工作区干净后，使用 `git update-ref <branch> <remote> <old-local>` 将本地分支对齐远端提交。
- 防复发：PowerShell 字符串中变量后紧邻冒号时统一写 `${name}:`；Git Data API 创建提交后不假设 SHA 与本地 commit 相同，必须 fetch 实际对象并比较 tree、parent、身份元数据和规范化消息，再同步本地 ref。后续补充记录只能以 GitHub 实际提交为父做非强制快进。

### 7. 远端 main 摘要的内联拆分发生运算符绑定误判

- 现象：远端快进提交已完成实际对象同步，本地也已对齐；最终门禁把 `git ls-remote origin refs/heads/main` 与 `-split` 写在同一括号表达式中，PowerShell 得到首字符 `9` 而不是完整 SHA，因而主动报告 main drift。没有更新 `main`，也没有再次写远端分支。
- 根因：PowerShell 中原生命令调用和 `-split` 的内联组合存在易混淆的参数/运算符绑定，紧凑表达式没有先固定命令的完整文本结果。
- 解决：不采信首字符结果；先把 `git ls-remote` 完整输出保存为变量并检查 `$LASTEXITCODE`，再以空白正则拆分第一列，最后与预期 main SHA 比较。
- 防复发：外部命令输出的解析一律分成“执行并检查退出码—保存原始行—独立拆列—验证格式/长度”四步，禁止在发布门禁中用一行表达式同时调用命令与拆分结果。

### 8. Git smart-HTTP 在最终门禁发生连接重置

- 现象：准备最后一个 ADR 快进提交时，首个只读 `git ls-remote origin refs/heads/main` 返回 `Recv failure: Connection was reset`；脚本在暂存和提交前终止，远端、本地提交和工作簿均未改变。
- 根因：GitHub HTTPS 传输链路瞬时重置，不是 ref 冲突、权限错误或业务工件错误。
- 解决：保持原状态，不盲目重发写操作；远端 main 与工作分支 ref 改由已认证的 `gh api repos/.../git/ref/...` 分别读取并核验 SHA，再继续本地提交和 Git Data API 非强制快进。
- 防复发：Git smart-HTTP 出现 reset 时，先用 GitHub API 只读确认实际 ref；对象发布仍按“远端当前 SHA 必须等于本地新提交 parent”门禁执行，禁止因网络不确定性 force push 或重复创建分支。

## 停止点

提交本台账单元格和 ADR，通过非强制 Git Data API 发布原分支并创建关联 PR，等待 owner 对跳过证据和台账工件审计。不得自行合并 PR、关闭 Issue、采集医生或领取下一 Issue。

<Handoff_State>
Target: Issue #39 中山大学附属第一医院黄埔院区同源目录跳过审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/39
Branch: codex/mhrj/issue-39-fahsysu-huangpu-verify-skip
Phase: VERIFY_SKIP_AWAITING_OWNER_AUDIT
Completed:
- 官网首页、公共专家目录和官网声明的东院入口已按可见导航只读核验
- 东院入口跳转至“改扩建期间暂停所有服务”告知书；其专家入口仍为公共 `/page/6945`
- 未发现黄埔/东院独立医生目录；序号 8 `入口台账!V9` 已标记跳过同源
- 工作簿唯一值差异为 V9，公式差异和公式错误均为 0；5 张表完成视觉通览
Next:
- owner 审计跳过证据与台账工件
- owner 审计通过后合并 PR 并关闭 Issue #39
Constraints:
- 不采集医生、不写总底表、不生成画像
- 不构造搜索、不猜路径、不越域
- 不自行合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院官网入口台账.xlsx
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_39_fahsysu_huangpu_verify_skip.md
</Handoff_State>
