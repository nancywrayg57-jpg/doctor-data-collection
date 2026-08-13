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
