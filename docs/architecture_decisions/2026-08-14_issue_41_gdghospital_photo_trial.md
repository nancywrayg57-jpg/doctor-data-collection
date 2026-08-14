# Issue #41 广东省人民医院照片采集首发 TRIAL

## 1. 目标与授权边界

- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/41`
- 工作分支：`codex/mhrj/issue-41-gdghospital-photo-trial`
- 基线：`3f9ca945f83f02779e44c79daf4faf6e063b0002`
- 医院：广东省人民医院（入口台账序号 19，人工复核 `确认可采集`）
- 官网首页：`https://www.gdghospital.org.cn/xzfz/list.html`
- 医生目录：`https://www.gdghospital.org.cn/DepartmentSearch/list.html`
- 当前 Phase：`TRIAL`
- 授权范围：官网公开页面普通 GET 普查，输出 10 位、至少 3 科室、含 10 张本人职业照的试采工件；不得写总底表、不得生成正式画像、不得执行 FULL。
- FULL 门禁：owner 审计 TRIAL 并明确裁决照片压缩和画像宽度方案、同时下发 `FULL_APPEND_AND_OBSIDIAN` 前，脚本保持硬熔断。

## 2. 官网范围与结构结论

本轮只使用 `gdghospital.org.cn` 官网同域公开页面，未登录、未注入 Cookie、未处理验证码/挑战、未调用非公开接口，也未使用第三方平台。

| 项目 | 现场结果 |
|---|---:|
| 顶层分组 | 26 |
| 科室 | 83 |
| 医生—科室关系 | 1,343 |
| 唯一数字详情 ID | 1,343 |
| 有官方同域头像的关系 | 1,343 |
| 纯护理身份排除 | 9 |
| 护理排除后候选 | 1,334 |
| 跨科室复用同一 itemid | 0 |
| 同名不同 ID | 52 组 |

严格页面契约：

- 科室页：`/Specialistthree/index_subjectid_<subjectid>.html`
- 医生详情：`/Expertlistt/info_itemid_<itemid>_subjectid_<subjectid>.html`
- 详情容器：`.sub_ex_Info`
- 详情正文：`.divmore`，无该节点时再保守检查 `.divtxtbox`
- 照片：详情容器或列表卡片中的官网同域 `/uploadfiles/` 图片
- 83 个科室页均由服务端一次性输出完整医生卡片，未发现分页、加载更多或筛选接口。
- `门诊时间地点` 及其后尾段不进入正式字段；患者案例、排名、患者评价、导航和私用区字符均在写出前门禁复核。

## 3. 分院/研究所归属证据

官网 `https://www.gdghospital.org.cn/expert/list.html` 公开展示 4 个分院/研究所入口。详情页未出现“独立法人”“法人单位”“统一社会信用代码”等独立法人证据，因此未触发独立法人熔断。

| 名称 | 官方详情 | 官网归属证据结论 |
|---|---|---|
| 广东省心血管病研究所 | `https://www.gdghospital.org.cn/expert/info_itemid_69.html` | 广东省人民医院所属研究所 |
| 广东省老年医学研究所 | `https://www.gdghospital.org.cn/expert/info_itemid_68.html` | 官网明确“一套人马、两块牌子”，由广东省人民医院代管 |
| 惠福分院 | `https://www.gdghospital.org.cn/expert/info_itemid_67.html` | 广东省人民医院重要组成部分 |
| 广东省肺癌研究所 | `https://www.gdghospital.org.cn/expert/info_itemid_65.html` | 广东省人民医院所属研究所 |

## 4. 实现决策

### 4.1 专用适配器与强门禁

- 新增适配器：`gdghospital_static_department_expert`。
- 只接受严格目录、科室和详情 URL；照片只接受 HTTPS、官网同域、`/uploadfiles/` 路径。
- 照片扩展名由 JPEG/PNG/GIF/WebP 魔数确定，不信任 URL 后缀；保存前记录字节数和 SHA-256。
- 照片文件名为 `姓名-首个原子科室-主职称-医院.<实际扩展名>`；非法字符替换为 `_`；四段冲突时追加详情 ID；已有不同内容时拒绝覆盖。
- 同名身份继续按职称、擅长和正文相似度聚类；实质不同的身份分行保留并标记 `同名待甄别`。任何异常行都清空重点标签并降为普通优先级。
- 试采固定要求 10 个最终身份、至少 3 科室、10 张可核验照片；现场计数、护理排除、来源域、正式字段污染、照片路径/魔数/大小/SHA-256、分院证据均在写出前强校验。
- 所有非 `--trial-only` 的广东省人民医院运行均在联网采集和总底表写入前失败；`--allow-generic-append` 不能绕过该熔断。

### 4.2 Schema、工作簿与画像能力

- `BASE_HEADERS` 新增 `照片链接`、`照片文件`，既有总底表记录读取时自动补空值。
- 工作簿 `自动采集底表` 和 `复核清单` 扩展到 25 列（A:Y），新增两列宽度；`采集说明` 增加照片样本数、平均字节、全院估算字节和 owner 裁决状态。
- Obsidian 生成器只接受安全的仓库相对路径；当 `照片文件` 有值时，在 `## 基础信息` 表格上方生成 `![姓名](照片/文件名)`，禁止 HTTP、HTTPS、base64、路径穿越或非 `照片/文件名` 结构。
- 本轮只通过单元测试验证画像引用能力，没有生成广东省人民医院正式画像。

## 5. TRIAL 结果

样本覆盖 10 个不同科室，详情失败 0、照片失败 0、异常提示 0。10 张图片已逐张视觉确认，均为医生本人单人职业照，无患者影像、合影或新闻配图。

- 平均单张：12,206 bytes
- 护理排除后全院估算：1,334 张
- 估算总容量：16,282,804 bytes（约 15.53 MiB）
- 方案状态：`WAITING_OWNER_SIZE_POLICY`

详细的 10 人字段、照片文件名、单张字节数、SHA-256、官网照片 URL 和分院证据见 `work/广东省人民医院_trial_report.md`。

## 6. 总底表零变更证据

TRIAL 前后以下文件的长度、UTC 修改时间和 SHA-256 完全一致：

| 文件 | 长度 | LastWriteTimeUtc | SHA-256 |
|---|---:|---|---|
| `珠三角三甲医院_医生画像自动采集总底表.xlsx` | 2,934,607 | `2026-08-13T15:35:33.0628573Z` | `09E25E58E41E9A5C398ECC8F94660953A1AF7EB4A535B0B7A2DE8F508517A8C3` |
| `珠三角三甲医院_医生画像自动采集总底表.csv` | 12,291,095 | `2026-08-13T15:35:33.0349161Z` | `088FBEA03F9D5CE0F1EC39BEB0CD8B99973546D379DC43C9D34C49A834620C53` |
| `珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 4,674 | `2026-08-13T15:35:33.0989753Z` | `0C056331F7AAF3D5AEB8286DD3BCCE71215EF2F6CB0FABDE541BDC7661DDBE73` |

## 7. 验证闭环

- Python/Node 语法检查通过。
- `python -m unittest discover -s work/tests -p 'test_*.py' -v`：123 项通过；新增 GDGH 专项覆盖严格 URL、真实格式魔数、10 图门禁、同名异常降级和抽样去重。
- 工作簿 5 张表均使用 artifact-tool 完成结构检查、公式错误扫描和视觉渲染；公式错误 0，25 列表头/行高/照片字段可读。
- 10 张照片逐张视觉复核；文件数 10、文件名唯一 10、大小对账差异 0、SHA-256 对账差异 0。
- FULL 负向门禁验证：带 `--allow-generic-append` 的非 TRIAL 命令在采集前退出 1，并报告 `GDGH FULL 发布熔断`。
- `git diff --check` 通过；行尾提示仅为 Windows 工作区的 CRLF 转换预告，未修改全局 Git 配置。

## 8. 阻塞、根因、解决与防复发

### 8.1 GitHub HTTPS reset 与 SSH/fast-forward 恢复

- 阻塞：恢复链前段的 GitHub smart-HTTP 查询/发布发生连接重置，无法可靠判断远端写入是否成功。
- 根因：GitHub HTTPS 传输链路瞬时 reset，不是业务工件、权限或 ref 冲突。
- 解决：停止盲目重试；先只读核验远端 ref。管理员完成 SSH 配置和 fast-forward 同步后，本轮再次确认 `HEAD == origin/main == 3f9ca945...`、身份为 `xtzhou247`，再从该基线继续。
- 防复发：任何传输失败先查远端 ref；发布只允许“远端当前 SHA 等于新提交 parent”的非强制快进，禁止 force push。

### 8.2 签名提交重建与 Create Tree 恢复点

- 阻塞：前序恢复过程中，签名提交对象重建未形成可验证的一致提交，Create Tree 后的发布链因此停止。
- 根因：带签名提交的对象身份/签名不能通过重新拼装 tree/commit 文本安全推断；继续尝试会放大远端不确定性。
- 解决：不伪造或猜测签名对象；保留已验证 tree 证据，管理员完成 SSH 和 fast-forward 同步后，以确认的 `origin/main` 为唯一基线重新开始当前 Issue 分支执行。
- 防复发：签名对象失败时只记录 tree、parent、作者和远端 ref 证据，不重建签名；恢复点必须先与远端 ref 交叉核验。

### 8.3 Windows Python 占位符与临时 PYTHONPATH

- 阻塞：系统 `python.exe` 指向 Windows Store 占位符，默认解释器不能稳定加载本项目依赖。
- 根因：PATH 中的占位符不是实际运行时；依赖位于 Codex bundled runtime 和已验证的临时 Python 包目录。
- 解决：固定使用 `C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`，并仅为本轮命令设置已验证 `PYTHONPATH`。
- 本轮复发快速恢复：bundled Python 可执行文件存在，但直接运行测试仍因缺少 `requests` 中止；现场确认 `C:\Users\Administrator\AppData\Local\Temp\codex-doctor-trial2-6e103c2f32134fb28cb233887b5034b1` 同时包含 `requests`、`bs4`、`openpyxl` 后，仅对测试进程设置该目录为 `PYTHONPATH`，先执行三模块导入探针，再重跑得到 123 项通过。
- 防复发：先调用 workspace dependency loader 定位解释器；若导入探针失败，只读查找任务临时依赖目录并用 `Test-Path` 同时核验 `requests`、`bs4`、`openpyxl`，仅设置进程级 `PYTHONPATH`。临时目录不存在时停止并重新建立任务级依赖环境，不安装全局包、不修改系统 PATH、不把临时路径写入仓库配置。

### 8.4 artifact-tool 模块解析

- 阻塞：临时核验脚本不能从仓库根目录直接解析 `@oai/artifact-tool`。
- 根因：技能要求的依赖只存在于 Codex bundled `node_modules`，不应复制或安装到仓库。
- 解决：在 `.codex_tmp/issue41` 使用 Windows junction 指向 loader 返回的 bundled `node_modules`；仓库既有 `work/node_modules` junction 继续供工作簿构建器使用。
- 防复发：始终调用 workspace dependency loader；只在会话临时目录创建 junction，禁止 npm install、依赖复制或修改 bundled 目录。

### 8.5 第一次真实 TRIAL 只有 9 个最终身份

- 阻塞：第一次真实 TRIAL 在写出前门禁中止：先抽取的 10 个详情 ID 经身份聚类后只剩 9 人、9 张照片。
- 根因：抽样器按科室覆盖选中了同名且资料一致的详情 ID `33825` 与 `25508`；身份归并规则正确将其视为同一人，但抽样器未预先保证规范化姓名唯一。
- 解决：只修改 TRIAL 抽样器，在保持科室覆盖的同时先按规范化姓名去重；不放宽 10 人、10 图、身份聚类或现场计数门禁。第二次真实 TRIAL 成功得到 10 人/10 图。
- 防复发：抽样阶段同时记录“初选详情 ID 数、规范化姓名数、归并后身份数”；三者不满足目标时在下载/写出前补选，不通过删除归并或降低目标行数规避。

### 8.6 单元测试夹具姓名不合法

- 阻塞：首次全量单测中，新增模拟门禁测试使用 `医生0` 等含数字假姓名，被真实姓名格式校验正确拒绝。
- 根因：测试夹具不符合生产口径，不是采集器缺陷。
- 解决：将夹具改为 10 个合法中文测试姓名后重跑；123 项全部通过。
- 防复发：门禁测试夹具必须满足与官网样本一致的核心字段口径，不能通过弱化生产校验让无效夹具通过。

### 8.7 第一次 FULL 的零宽字符阻塞与部分照片清理

- 阻塞：owner 在 PR #42 明确 TRIAL `通过` 并下发 `FULL_APPEND_AND_OBSIDIAN` 后，第一次 FULL 在总底表写入前被姓名格式门禁拦截；11 个官网姓名含 `U+200B` 零宽字符。该次运行已下载 1,299 张未跟踪的部分照片，但 XLSX、CSV 和更新报告的基线 SHA-256 均未变化。
- 根因：全局 `clean_text` 没有移除 `U+200B/U+200C/U+200D/U+FEFF`，官网不可见格式字符因此进入 GDGH 姓名校验；采集写表门禁正常阻止了不合规数据落盘。
- 解决：只新增 GDGH 专用 `gdgh_clean_text`，不改变其他医院既有清洗口径；先用精确目录 dry-run 核验，再仅清理 `医生画像仓库/01_试点医院/广东省人民医院/照片/` 中 1,299 张未跟踪部分照片，保留已跟踪的 10 张 TRIAL 照片。第二次 FULL 为熔断前最后一次授权尝试，成功完成写入。
- 防复发：专用适配器在姓名、科室、职称和正文进入门禁前统一做不可见格式字符探针；任何 FULL 失败先比较受保护总底表 SHA，再按精确目录区分已跟踪样本与未跟踪部分下载，禁止宽泛清理或第三次盲目重跑。

### 8.8 工作簿表名与 Markdown 图片引用的验证误报

- 阻塞：临时 artifact-tool 核验脚本首次沿用旧交接中的 5 表名称，现场工作簿实际为 6 表；画像生成后，简化正则又把 18 条文件名含成对半角括号的图片引用误判为路径提前闭合。
- 根因：验证器假设落后于现场工件；CommonMark 允许链接目标中出现平衡括号，正则不能替代 Markdown 解析器。
- 解决：先通过 workbook inspect 动态确认 6 张表，再修正核验范围；图片引用改用 bundled `marked` 的 Markdown AST 全量解析，1,309 条引用全部解析到正确相对路径，未修改任何图片文件名或画像正文。
- 防复发：工作簿验证先枚举真实 sheet，再按现有名称建立范围；Markdown 链接和图片必须用语法解析器核验，正则只用于快速定位，不作为最终门禁。

### 8.9 大批量 Git Data API Create Tree 超时

- 阻塞：2,614 个唯一变更 blob 均已上传并逐 SHA 校验，但把 2,624 条长路径变更一次性平铺提交到 `POST /git/trees` 时，GitHub 连续返回 502，最终返回 504；目标 tree 查询为 404，远端分支仍停在父提交 `7ece6f5765e3fdb93834eca34d3b109ddc77d9cf`，没有产生半发布状态。
- 根因：单次 Create Tree 请求同时包含 1,299 个新增照片路径和 1,310 个画像路径，长中文路径形成的大型平铺 JSON 在 GitHub 边缘/服务端超时；blob、身份、权限和本地 Git tree 均已独立验证，不是数据对象错误。
- 第一次恢复尝试：保留 blob SHA 检查点并改为分层 tree。1,309 项照片子树创建成功，SHA 为 `7578865e12250356d064f27197a294d7a8ea4e34`；但包含 1,311 项的广东省人民医院画像目录子树仍连续出现网络错误、502/504，最终返回 422 `input was too large to process`。目标 root tree 和远端 ref 均未生成或更新。
- 解决：上述平铺与分层方案构成连续两次发布修复失败，按熔断规则停止 Git Data API 写入。管理员于 2026-08-14 明确授权改用 SSH；本轮仅在再次确认身份为 `xtzhou247`、远端 ref 仍为 `7ece6f5765e3fdb93834eca34d3b109ddc77d9cf`、新提交 parent 等于该 ref 后，执行一次不带 force 的 SSH fast-forward push。
- 防复发：超过 1,000 个长路径文件时，不再把 Git Data API Create Tree 作为默认发布通道；优先使用管理员已授权且能由服务端原子校验 fast-forward 的 SSH 非强制 push。任何传输失败先查询远端 ref 和 PR head，确认是否已落地后再决定是否重试；禁止 force push，保留 `.codex_tmp/issue41-publish/` 检查点直到远端 tree 与本地 tree 一致。

## 9. FULL 追加结果

owner 审计与授权：`https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/42#issuecomment-5289100722`。当前院照片政策为 `OWNER_APPROVED_ORIGINAL_NO_WIDTH_LIMIT`：保留官网原图、不压缩、画像使用标准 Markdown 直接嵌入且不限宽。

### 9.1 逐 ID 与身份归并闭环

| 指标 | 结果 |
|---|---:|
| 顶层分组 | 26 |
| 科室 | 83 |
| 官网关系/唯一详情 ID | 1,343 |
| 纯护理排除 | 9 |
| 合规详情 ID | 1,334 |
| 最终医生身份 | 1,309 |
| 身份归并减少 | 25 |
| 详情失败 | 0 |

机器闭环结果：1,334 个合规详情 ID 在身份归并表中出现 1,334 次且唯一；再与 9 个护理排除 ID 合并后得到 1,343 个唯一 ID，交集为 0。最终 1,309 行中唯一来源链接 1,309 个、唯一姓名 1,274 个；同名实质不同身份继续分行并保留 `同名待甄别`。

### 9.2 总底表结果

- 总记录从 6,092 增至 7,401，新增 1,309、重复跳过 0、既有刷新 0；当前 17 家医院、25 列。
- 广东省人民医院 1,309 行；异常提示不为空 168 行。提示汇总：`同名待甄别` 69、`职称/身份需人工复核` 102、`多详情职称不一致` 2、`详情正文为空或未识别` 3；同一行可含多个提示。
- 更新后 SHA-256：XLSX `F7F574988CEED831ACBE08E86A7B4DF9FCC998020F984880C9F8E4A98973309F`；CSV `149E4F14446204C65F54B5A85F5A31917DB14A03DAC1C9D14470C7AEA4AFDB0D`；更新报告 `ED26448B9A6C6F76FE09E75D96A452126073C8635F49789D39895B3D814497AB`。

### 9.3 照片四数与大图实况

| 照片应采 | 实采 | 失败 | 无照片 |
|---:|---:|---:|---:|
| 1,309 | 1,309 | 0 | 0 |

- 文件总字节数 18,942,264，平均 14,471 bytes；1,309 个文件与 payload 的字节数、SHA-256、扩展名魔数全部一致。
- 格式分布：JPEG 1,296、GIF 12、PNG 1。
- 最大文件为 `袁凯旋-检验科-主管技师-广东省人民医院.png`，1,340,291 bytes、896×1,152；另有 `梁盛华-心外科-医师-广东省人民医院.jpg` 为 1,279×1,700、93,215 bytes。两张均已视觉确认是官网单人职业照；本院按 owner 已明确的原图不压缩、不限宽政策保留，后续医院仍执行“大于 200KB 或宽度大于 800px 先回报”的新院门禁。

## 10. Obsidian 与工作簿终检

- 使用 `--hospital 广东省人民医院 --generate-missing-only` 新生成 1,309 份医生画像，刷新 0、跳过 0，并生成 `_索引.md`。
- Markdown AST 核验：1,309 个唯一来源、1,309 条标准相对图片引用、1,309 个真实照片文件；不安全路径 0、缺图 0、错配 0。
- 索引核验：1,309 条唯一画像链接，缺失目标 0、未入索引画像 0；索引记录异常提示不为空 168。
- artifact-tool 终检：6 张工作表、6 个表对象；`自动采集底表` 7,402 行含表头、25 列；`复核清单` 691 行含表头、25 列；公式错误扫描 0。6 张表均完成渲染检查，未发现截断关键表头、破损区域或不可读布局。

## 11. 当前停止点

FULL 代码、1,309 行总底表增量、全量 payload/报告、1,309 张照片、1,309 份画像、索引、补充生成报告和本 ADR 已精确暂存并提交。按管理员本轮明确授权，改用 SSH 对原分支执行一次非强制 fast-forward push；推送后必须核验 GitHub branch ref、PR #42 `headRefOid` 和远端 tree 均与本地一致。仅在推送成功后清理 `.codex_tmp/issue41-publish/` 检查点；CI 成功后在 PR #42 请求 owner 最终画像审计并恢复自动化。不得自行合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #41 广东省人民医院 FULL_APPEND_AND_OBSIDIAN
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/41
PullRequest: https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/42
Branch: codex/mhrj/issue-41-gdghospital-photo-trial
Phase: FULL_READY_TO_SSH_PUSH
Completed:
- 1,343 唯一详情 ID 闭环：9 护理排除、1,334 合规详情、1,309 最终身份、详情失败 0
- 总底表新增 1,309，达到 17 家医院、7,401 位医生、25 列
- 照片四数 1,309/1,309/0/0，字节、SHA-256、魔数全量一致
- 新生成 1,309 份画像；1,309 个索引链接和 1,309 个安全图片引用闭环
- 更新后 6 张工作表结构、公式错误和视觉终检通过
Next:
- 将本 ADR amend 进既有 FULL 提交；复核身份、远端 ref 与提交 parent 后执行一次 SSH 非强制 fast-forward push
- 推送后核验 branch ref、PR head 和 tree；成功后精确清理发布检查点
- CI 成功后请求 owner 最终画像审计并等待，不得自行合并或关闭
Constraints:
- 仅官网公开页面和本人职业照；禁第三方、患者影像/案例/评价、隐私、登录/验证码规避
- 本院照片原图不压缩、画像不限宽；后续医院大图阈值重新回报
- 不自行合并 PR、关闭 Issue 或领取下一 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广东省人民医院_official_doctors_payload.json
- D:\workspace\信息收集整理\work\广东省人民医院_official_doctors_report.md
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx
- D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\广东省人民医院
</Handoff_State>
