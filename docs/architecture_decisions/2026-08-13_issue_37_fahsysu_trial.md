# 2026-08-13 Issue #37 中山大学附属第一医院 TRIAL / FULL

## 目标与执行边界

- GitHub Issue：https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/37
- 工作分支：`codex/mhrj/issue-37-fahsysu-trial`
- Phase：`FULL_PUBLISH_BLOCKED_HUMAN_INTERVENTION_REQUIRED`
- 台账序号：7
- 医院：中山大学附属第一医院
- 官网首页：https://www.fahsysu.org.cn/home
- 医生目录：https://www.fahsysu.org.cn/page/6945
- 人工复核：确认可采集（D-待人工补官网）

TRIAL 阶段只普查官网公开目录并试采 10 位医生（至少 3 个科室）；当时不得写统一总底表、生成正式 Obsidian 画像、采集台账序号 8 的黄埔院区专属目录，或自行进入 FULL。该限制在 owner 明确审计通过并切换 `FULL_APPEND_AND_OBSIDIAN` 后仅对“不得采序号 8”继续有效。

## FULL 阶段授权与边界

2026-08-13，owner `nancywrayg57-jpg` 在 PR #38 明确给出 TRIAL“通过”，并将有效指令切换为 `FULL_APPEND_AND_OBSIDIAN`：

- 本轮按序号 7 的 `/page/6945` 目录全量采集，不推断结构化院区归属。
- 对账基线固定为 881 条医生—专科关系、860 个唯一数字 node ID、8 组同名不同 ID；正式行数由逐 ID 对账、明确护理身份排除与身份聚类决定。
- 逐 ID 对账和正式身份映射必须进入最终画像审计材料；任何明显偏离在总底表写入前硬阻断。
- 台账序号 8 黄埔院区未来执行时，必须把其目录 node ID 与本轮 860-ID 集合逐一对账；命中本轮 ID 的医生不得在序号 8 重复入库。不得按姓名猜测或跨目录启发式合并。

## 专用适配器与范围规则

新增专用适配器 `fahsysu_drupal_expert_directory`：

1. 入口只接受无 query/fragment 的 `https://www.fahsysu.org.cn/page/6945`。
2. 详情只接受同一官方域名、无 query/fragment 的 `/node/<数字ID>`。
3. 医生关系只来自 `.action-item > .action-item-content > .action-item-right > .action-item-list` 中的严格医生标签；页面其他 node 链接不授权。
4. 同一数字 ID 的跨科室关系以顿号归并；同名不同数字 ID 保持独立，样本命中时标记“同名待甄别”。
5. 列表的“正高/副高”只作为目录关系线索；正式职称只取详情 `.other-left-text` 的显式“职称”字段。
6. 详情只读 `article.node--type-doctor` 下的 `.other-2` 与 `.showcase-text-content`；所有 `calendar-*` DOM 排除。排名、患者信息和私用区字符不得进入正式字段。
7. 试采按科室确定性轮转，保证至少覆盖 3 个科室；FULL 模式必须先通过 860-ID、881 关系、逐 ID/身份映射、同名分行、来源与污染检查的写入前硬门禁。
8. 不提交搜索词、不构造筛选组合、不探测页面未声明接口。

## 官网目录普查

- 服务端完整输出单页长列表；分页、上一页/下一页和加载更多控件均未发现，分页计数为 1。
- 顶层 `.action-item` 容器 42 个：32 个包含医生关系，10 个为空结构容器。
- 空容器：手术麻醉中心、输血科、高压氧科、保健门诊中心、精准医学研究院、临床研究中心、药物临床试验机构、动物实验中心、无菌动物研究平台、消毒供应中心。
- 下级专科 90 个；医生—专科关系 881 条；唯一数字 ID 860 个；跨专科重复关系增量 21 条。
- 目录职级关系：正高 447，副高 434。该字段不写入正式职称。
- 同名不同数字 ID 8 组：庄锦涛、涂响安、匡铭、梁力建、王伟、刘敏、陈宇、何潇芳。
- 目录正文中“院本部/本部/东院区/东院/南沙/南院区/黄埔/院区”均为 0。

## 院区与黄埔范围结论

目录页没有结构化院区字段。10 位试采详情中，仅陈振光详情的工作履历出现“东院”3 次，属于官方履历正文中的任职证据，不是统一的医生院区归属字段。本轮只把该信息作为“官网存在东院履历证据”留痕，不将履历词推断写入结构化科室或院区字段。

本轮未访问、未采集台账序号 8 的黄埔院区专属目录。目录和 10 位详情均未出现“黄埔”，但因目录没有统一院区标注，仍无法证明或排除未抽样医生是否含黄埔归属；等待 owner 根据 TRIAL 材料裁决，不自行扩大范围。

## TRIAL 结果

命令：

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "中山大学附属第一医院" `
  --trial-only --max-doctors 10 --min-departments 3 --no-xlsx
```

结果：

- 10 位：郭宇、陈昆、陈蕾、陈炜、邓春华、高勇、涂响安、刘钧澄、唐冰、陈振光。
- 覆盖 9 个科室值；邓春华和高勇分别按同一数字 ID 归并 2 条跨科室关系。
- 10 个来源数字 ID 唯一；详情失败 0；非医生页面混入 0。
- 涂响安命中全目录同名不同 ID 组，保留为独立 ID `735`，标记“同名待甄别”，保持普通优先级、空重点标签。
- 正式职称全部来自详情显式字段，没有把正高/副高拼入职称。
- 详情排班 DOM 排除 400 个；排名/患者片段排除 2 个；四正式文本字段中的排班、患者/排名词、私用区字符和擅长前缀均为 0。
- 使用 `--trial-only --no-xlsx`；未写统一总底表、未生成试采 XLSX、未生成 Obsidian 画像。

## 阻塞、根因、解决方法与防复发

### 1. 本地 Python 命令和依赖不可用

- 现象：PowerShell 的 `python` 指向 WindowsApps 占位程序；Codex 捆绑 Python 虽可执行，但缺少 `requests` 与 `beautifulsoup4`。
- 根因：运行时 PATH 未暴露真实 Python，且捆绑环境仅含部分文档/表格依赖。
- 解决：使用 Codex 工作区依赖中明确解析出的 Python 路径；仅把 `requests`/`beautifulsoup4` 安装到仓库外 `C:\Users\Administrator\AppData\Local\Temp\codex-issue37-python-deps`，通过本轮专用 `PYTHONPATH` 加载。
- 防复发：后续先运行解释器与 `import requests, bs4, openpyxl` 探针；不得反复调用 WindowsApps 的 `python`，不得把临时依赖写入仓库或修改全局 Python。

### 2. 首次真实 TRIAL 解析关系为 0

- 现象：写出前报错“官网目录未发现严格 action-item 医生关系”，没有生成工件。
- 根因：实际医生标签层级为 `.action-item-list > .action-item-list-text > .action-item-list-tag > a`，初版选择器漏掉 `.action-item-list-text`。
- 解决：局部读取一层 DOM 后，只补齐该固定结构层级，并同步更新模拟 DOM 测试。
- 防复发：测试必须完整模拟真实层级；现场变更时先输出目标节点的一层子元素和父链，不凭类名猜测后代结构。

### 3. 第二次真实 TRIAL 的顶层分组门禁冲突

- 现象：严格解析已得到 881 条关系，但门禁报“顶层分组应为 42，实际 32”。达到连续 2 次验证失败后按 `Agent.md` 熔断。
- 根因：页面有 42 个顶层容器，其中 10 个没有 `.action-item-content`；初版统计只从医生关系反推分组，因此得到 32，把“页面结构容器”与“有效关系分组”混成一个指标。
- 解决：管理员解除熔断后，将指标分层为 `census_group_count=42`、`census_relationship_group_count=32`、`census_empty_group_count=10`，并保存空容器名称。空容器计入结构普查，但绝不构造医生/专科关系。
- 防复发：门禁同时固定 42/32/10 三个计数；报告明确显示三层含义；测试断言顶层容器、关系分组和空容器分别计算。

### 4. 院区证据表述过强

- 现象：初步观察曾表述“目录与详情均未发现院区字段”，后续只读扫描发现陈振光详情履历含“东院”3 次。
- 根因：把“没有结构化院区字段”误写成“原始详情文本没有院区词”，证据层级混淆。
- 解决：分别统计目录页与样本详情原始 HTML 院区词；对命中详情保留 ID、姓名、来源和计数，同时标明只作履历证据、不推断结构化归属。
- 防复发：院区审计固定拆成三项：目录词扫描、详情词扫描、结构化字段存在性；任何履历命中不得自动写入科室/院区字段。

### 5. Git Data API 提交消息被 PowerShell 序列化为数组

- 现象：6 个 blob 和远端 tree 均已按本地 SHA 校验成功，但创建 commit 返回 HTTP 422，提示 `properties/message ... is not a string`；远端分支引用尚未创建。
- 根因：PowerShell 捕获 `git show --format=%B` 的多行输出时得到字符串数组，直接放入 JSON 后把 `message` 序列化为数组，而 GitHub Git Data API 要求单一字符串。
- 解决：先确认远端同名 ref 仍不存在；用 `Out-String` 将命令输出显式归一为标量字符串并 `TrimEnd()`，再创建 commit；只有 commit tree/parent 与本地一致后才以 `force=false` 创建 ref。
- 防复发：所有进入 Git Data API JSON 的 CLI 多行输出必须先做标量化；API 失败后先查 ref，禁止盲目重复更新引用。孤立 blob/tree 不构成分支发布，也不得误报为推送成功。

### 6. 远端 API commit 无法由展示字段精确重建

- 现象：Git Data API 已成功创建远端 commit/ref，tree 和 parent 与本地一致，但 GitHub 生成的 commit SHA 与本地 SHA 不同；API 返回的 `verification.payload` 为空。使用展示出来的作者/提交者时间、时区和消息组合无法重建远端 SHA，本地引用因此没有更新。
- 根因：GitHub 返回的 JSON 展示字段不足以还原提交对象的原始字节；没有 verified payload 时，继续猜测时区或尾换行会产生不同 OID。
- 解决：停止对象字段猜测，使用一次只读 `git -c http.version=HTTP/1.1 fetch --no-tags origin refs/heads/<branch>:refs/remotes/origin/<branch>` 获取 GitHub 实际对象；确认 fetch OID 与 API ref OID 一致后，再用 `git update-ref` 将本地分支精确同步到该对象。
- 防复发：Git Data API 发布后优先执行只读 fetch 同步对象；只有 API 明确返回 verified payload 时才允许按原始 payload 重建。绝不以 tree 相同为由伪称 commit OID 已同步，也不强制覆盖分支。

### 7. Artifact-tool 无法整张渲染超长总底表

- 现象：修改前 XLSX 基线验收时，总底表 `自动采集底表` 整张渲染请求约为 `5704x446519px`，artifact-tool 报 `Auto render too large`；入口台账 5 个工作表已正常渲染，总底表没有被修改。
- 证据：artifact-tool 已成功导入总底表并识别 6 个工作表、`自动采集底表 A1:W5233`、`复核清单 A1:W494` 等范围；公式错误扫描为 0，仅整张超长 PNG 渲染超过尺寸上限。
- 根因：长表的可视高度随 5233 行累加，超出渲染器单图尺寸限制，不是工作簿损坏或 Excel 占用。
- 解决：对超过 250 行的工作表固定渲染表头 30 行、代表性中段 30 行、末尾 30 行；短表仍渲染完整使用范围。分块后 6 张表全部生成视觉证据。
- 防复发：XLSX 验收先读取 used range；超长表不得发起 `autoCrop: all` 整表请求，统一使用“表头/中段/末尾”分块渲染，并保留全表内容/公式扫描作为非视觉覆盖证据。

### 8. 首次 FULL 被职称与正式文本门禁拦截

- 现象：860 个详情顺序读取完成后，`FAHSYSU FULL 写入前门禁` 在任何总底表写入前拒绝结果：2 个详情成功页没有显式职称；正式文本还命中“好医生/名医录/排行榜”荣誉词和 3 条带可识别年龄的患者/病例描述。FULL 验证失败计数为 1；三份受保护总底表资产哈希保持不变。
- 证据：只读逐 ID 诊断确认详情失败为 0；无显式职称的仅为 ID `5780` 黄雄庆、ID `5795` 张旭宇，官网详情只显示“科室：麻醉科”。污染来自详情 `医疗特长` 在没有 `【...】` 分隔时吞入后续履历/荣誉长段；患者规则命中 ID `5605` 陈柏龄、`5665` 鞠卫强、`5654` 王长希的年龄/病例原句。
- 根因：详情正文已经逐句执行排名/患者过滤，但 `specialty` 分支在提取“医疗特长”后只去前缀，没有再次执行同一逐句过滤；FULL validator 又把“官网未展示职称”误当失败，而项目口径要求官网无字段时留空并复核，不能用目录正高/副高补造。
- 解决：在 `parse_fahsysu_detail` 的擅长分支复用同一排名/患者逐句排除规则；显式职称缺失继续留空，加入“职称/身份需人工复核”，并由异常不提权门禁保证普通优先级和空标签。仍严格禁止把目录正高/副高写入正式职称。
- 防复发：详情解析测试新增“医疗特长后无分隔符且串入荣誉/患者案例”的回归场景；FULL 门禁分别检查“目录线索不得冒充职称”和“官网缺失职称必须留空+复核”，不再把两种证据状态混为一谈。

### 9. 首次最小修正的清洗变量误入错误作用域

- 现象：首次 FULL 根因修正后，FAHSYSU 专项测试有 3 项报 `NameError: clean_specialty is not defined`；按连续 2 次失败门禁再次熔断，未重跑 FULL。
- 证据：只读检索显示 `specialty_sentences/clean_specialty` 被补丁误插入 `build_master_payload` 约第 1033 行，而 `parse_fahsysu_detail` 约第 3729 行引用该局部变量但未定义。总底表 XLSX、CSV、更新报告哈希仍与 FULL 前基线完全一致，且没有残留采集进程。
- 根因：补丁以通用 `return {` 为锚点，命中了文件中更早的同形结构；大文件存在多个相似返回块，锚点上下文不足。
- 解决：管理员解除熔断后，精确删除 `build_master_payload` 中误入的 11 行，并以 `parse_fahsysu_detail` 的 `kept = [...]` 和紧随其后的返回块为唯一局部上下文插入清洗变量。
- 防复发：大文件补丁必须使用函数内唯一上下文与前后语句双锚点；应用后立即 `rg` 确认新变量只位于目标函数，再运行专项测试，禁止仅凭补丁成功响应判断位置正确。

### 10. 患者年龄识别只覆盖单向语序

- 现象：解除熔断并修正变量作用域后，6 个既有 FAHSYSU 测试通过，但新增回归用例仍保留“曾为100岁患者开展手术”句子。
- 证据：现有患者案例正则只匹配“患者……100岁”等患者词在前的语序；该回归句为“100岁患者”，年龄在前，因此没有被过滤。
- 根因：患者可识别信息规则没有覆盖中文中常见的“年龄+患者”反向组合。
- 解决：在共用患者案例检测函数中增加 `年龄……患者` 的对称匹配，距离仍限制为同句 30 字以内，避免扩大为普通临床年龄讨论的无界过滤。
- 防复发：回归测试同时保留排名荣誉串入和“年龄+患者”语序；后续新增患者可识别模式必须先在共用检测函数补齐，详情正文和擅长字段统一复用，不在适配器里维护分叉规则。

### 11. FULL 发布阶段 GitHub API 连续两次瞬态失败

- 第一次现象：Git Data API 已逐个完成 650/871 个 blob 的 SHA 校验后，GitHub `POST /git/blobs` 返回 `TLS handshake timeout`。脚本在创建 tree、commit 或更新 ref 前退出。
- 第一次根因判断：主机到 `api.github.com` 的 TLS 握手瞬断；此前 650 个对象均由 GitHub 返回与本地完全一致的 blob SHA，不是内容、权限或 Git 对象格式错误。
- 第一次最小修正：只读确认远端 ref 仍为旧提交 `c5f173978bcbddcf75a7892f0e54947871a1b3c2`，随后将上传并发从 4 降为 2，仅为 TLS/连接重置类瞬态错误加入最多 3 次的有界重试。
- 第二次现象：871/871 个 blob 全部重新上传并逐 SHA 校验成功，但 `POST /git/trees` 返回 GitHub HTTP 502；脚本仍在 commit/ref 写入前退出。
- 第二次根因判断：Create Tree 的 874 条变更项在 GitHub 边缘或服务端瞬态失败。请求所引用的 871 个 blob 已全部由同一仓库 API 验证存在，3 个删除路径明确；本地 tree 为 `db6c3b92a95657f223bfcb6a4343cd8bf62bfbe5`，没有证据表明 tree 内容本身非法。
- 熔断证据：第二次失败后只读核验 `gh api user` 仍为 `xtzhou247`；远端分支 ref 与 PR #38 `headRefOid` 均仍为旧提交 `c5f173978bcbddcf75a7892f0e54947871a1b3c2`；读取目标 tree `db6c3b92...` 返回 404，证明 GitHub 没有创建目标 tree，更没有创建可发布 commit 或更新分支。
- 当前处理：按 `Agent.md` 连续 2 次失败门禁停止所有远端写入，保持自动化 PAUSED，等待管理员再次明确解除本轮发布熔断。
- 下次恢复最短路径：先复核身份、工作区干净、远端 ref 仍等于本地提交父节点；除本次新增的 ADR 阻塞记录 blob 外，不再重复上传已逐项验证的其他 blob。只上传并校验最新 ADR blob，然后直接用本地提交全部 blob SHA + 旧 tree 作为 `base_tree` 重试 Create Tree（仅对 502/连接类错误做有界重试）；必须得到与本地 tree 完全相同的 SHA，才创建 commit。创建 commit 后再次比较旧 ref，并仅以 `force=false` 更新；若任一步再失败立即停止。
- 防复发：大量小文件发布固定拆成“blob 上传/校验”和“tree/commit/ref”两阶段并持久化完成清单；恢复时从已验证阶段续跑，不重新制造长时间上传窗口。tree、commit、ref 调用也统一使用与 blob 相同的瞬态网络有界重试，但任何 Schema、SHA 或身份错误不得重试。

## FULL 最终结果

- 目录对账基线保持不变：42 个顶层容器（32 个含关系、10 个空容器）、90 个下级专科、881 条医生—专科关系、860 个唯一数字 node ID。
- 逐 ID 对账 860 项、身份映射 860 项、正式写入 860 行；详情失败 0、护理排除 0、重复跳过 0。
- 8 组同名不同 ID 共 16 行全部按 node ID 分行保留并标记：庄锦涛、涂响安、匡铭、梁力建、王伟、刘敏、陈宇、何潇芳。
- 29 条异常记录均保持普通优先级且重点范围/标签为空，没有异常提权。ID `5780` 黄雄庆、ID `5795` 张旭宇的官网详情无显式职称，职称保守留空并标记人工复核，未用目录“正高/副高”补造。
- 四个正式文本字段中的排名/患者案例、排班、导航、私用区字符以及擅长多重前缀检查均为 0。
- 总底表从 5232 行增加到 6092 行，当前为 16 家医院；本院 860 行的 `已建画像` 在画像生成后通过 `--rebuild-master-only` 离线同步为“是”，未重新联网采集。

## Obsidian 画像闭环

- 生成本院正式画像 860 个、跳过 0、重建索引 1；未覆盖人工画像。
- FULL payload、总底表和画像三方的唯一官网 `/node/<数字ID>` 集合均为 860，集合差异均为 0。
- 每个画像恰有 1 个本院官网 node URL；不存在同一 URL 被多个画像占用。
- `_索引.md` 含 860 个唯一 wiki 链接，与 860 个画像文件名一一对应，无漏链或悬空链接。
- 8 组同名的 16 个 node ID 均映射到独立画像文件；同名第二行以科室后缀消除文件名覆盖。
- 画像目录共 861 个 Markdown 文件（860 画像 + 1 索引）；按“文件名 + 文件 SHA-256”排序构造的清单哈希为 `D179136696B1B2FDACB55B8F0BD7A647BBB5801E044BAD72B1CBE128C6C62910`。

## 工作簿最终验收

- 使用 `@oai/artifact-tool` 重新导入画像同步后的总底表并扫描 6 张工作表；公式错误命中 0。
- `自动采集底表` 使用范围为 `A1:W6093`；`医院统计` 为 `A1:F17`，中山大学附属第一医院显示医生数 860、已建画像数 860。
- 对超过 250 行的工作表按表头/中段/末尾各 30 行分块渲染，短表完整渲染；6 张工作表的内容、表头、交替底色与关键统计均可读，未发现破损、错列或明显截断。

## 最终验证闭环

- FAHSYSU 专项：7/7 通过。
- 全仓单元测试：118/118 通过。
- `py_compile`：采集器、画像生成器和采集器测试文件通过。
- 真实 FULL payload 再执行 `validate_fahsysu_full_append`：通过，860 正式行、860 逐 ID 对账、860 身份映射。
- CSV 独立解析：6092 行、23 列、16 家医院；本院 860 个唯一 node ID、860 个“已建画像=是”、29 条异常、0 个非法来源。
- 画像 frontmatter：860/860 包含本院名称和唯一官方 node URL；索引 860 条且唯一。
- `git diff --check` 与 `git fsck --no-dangling`：通过。

## 最终哈希

- FULL payload：`23CFDC86FBB350EC1ED37F62EC7888D8C3ED5E595A6DA96F937ADE33E709FE2C`
- FULL 报告：`2D1B820181A5606B5496DD4E43E5F777233715A67923CF171180F4870DBECF48`
- 总底表 XLSX：`09E25E58E41E9A5C398ECC8F94660953A1AF7EB4A535B0B7A2DE8F508517A8C3`
- 总底表 CSV：`B9470F65BCB25FA7090BA1D7069623BEC5CA788CA521F43E7C1E16D9496ECA03`
- 总底表更新报告：`C01BA4FE3A8D5BDCB94BAB7E97A4B0D90290DB1E36EDD9B090D23498C7267E34`
- 总底表 payload：`D5DB4859B9E290327FAB93C5AFCC05C8452DFF141C496AC7DB0B1D7716D4E7EF`
- Obsidian 补充生成报告：`AD1F37BD836EB59B668DD13FDACB15FED963DE96E008DB9C02511BECDDB87247`
- 本院索引：`A0221A9435CFB7CE121FB83235AF9959FC4E72E107D186AA90DFECF877D8A2D9`

## 清理与停止点

在 FULL、画像、索引和离线回写均验收后，已精确删除以下 3 个 TRIAL 临时工件：

- `work/中山大学附属第一医院_trial_payload.json`
- `work/中山大学附属第一医院_trial_doctors.csv`
- `work/中山大学附属第一医院_trial_report.md`

总底表 XLSX/CSV、更新报告、FULL payload/报告、正式画像、索引和其他受保护资产均未删除。当前停止点为：提交并通过非强制 Git Data API 更新原分支，等待 PR #38 CI 成功后请求 owner 最终画像审计；不得自行合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #37 中山大学附属第一医院 FULL 最终画像审计
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/37
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/38
Branch: codex/mhrj/issue-37-fahsysu-trial
Phase: FULL_PUBLISH_BLOCKED_HUMAN_INTERVENTION_REQUIRED
Completed:
- 860 个唯一 node ID 全量追加；逐 ID 对账、身份映射、8 组同名 16 行和黄埔未来按 node ID 去重预案已留痕
- 总底表当前 16 家/6092 行；本院 860 行，异常 29，详情失败/护理排除/重复写入均为 0
- 本院 860 个画像、860 个索引链接、860 个唯一来源 URL 一一对应；已离线同步已建画像为 860
- 使用 artifact-tool 完成 6 张工作表公式扫描与分块/完整视觉验收
- 10 类阻塞均按现象、证据、根因、解决和防复发记录；管理员解除熔断后最终执行成功，失败计数归零
CurrentFacts:
- FULL payload/报告分别为 `work/中山大学附属第一医院_official_doctors_payload.json` 和 `work/中山大学附属第一医院_official_doctors_report.md`
- 画像目录为 `医生画像仓库/01_试点医院/中山大学附属第一医院`；补充报告记录生成 860、跳过 0、重建索引 1
- 3 个 TRIAL 临时工件已精确删除；受保护资产未删除
Next:
- 管理员再次明确解除 FULL 发布熔断后，从 ADR 记录的 Create Tree 恢复点继续；不得在未授权时第三次写入
- 发布成功后只读 fetch GitHub 实际 commit 对象同步本地，等待 PR #38 CI 成功
- CI 成功后留言请求 nancywrayg57-jpg 最终画像审计；恢复自动化后停止
Constraints:
- 仅当前 Issue #37、原分支和 PR #38；不得处理其他 Issue
- 仅官方公开页面；禁止第三方平台、患者评价、隐私、登录/验证码绕过
- 不采台账序号 8 黄埔专属目录；未来只按 node ID 与本轮 860-ID 集合去重，不按姓名猜测
- 不覆盖人工画像；不自行合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\中山大学附属第一医院_official_doctors_payload.json
- D:\workspace\信息收集整理\work\中山大学附属第一医院_official_doctors_report.md
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\中山大学附属第一医院
- D:\workspace\信息收集整理\docs\architecture_decisions\2026-08-13_issue_37_fahsysu_trial.md
</Handoff_State>
