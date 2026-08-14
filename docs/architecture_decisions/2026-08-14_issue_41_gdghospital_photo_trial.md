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

## 9. 当前停止点

提交代码、10 人 CSV/XLSX/JSON/报告/预览、10 张照片和本 ADR，通过非强制方式发布原分支并创建 `Closes #41` PR。CI 成功后恢复自动化并等待 owner 对 TRIAL、照片压缩和画像宽度方案审计；不得自行执行 FULL、生成正式画像、合并 PR、关闭 Issue 或领取下一 Issue。

<Handoff_State>
Target: Issue #41 广东省人民医院照片采集首发 TRIAL
AgentConstitution: D:\workspace\信息收集整理\Agent.md
RouteDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md
RequirementDoc: D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/41
Branch: codex/mhrj/issue-41-gdghospital-photo-trial
Phase: TRIAL_AWAITING_OWNER_AUDIT
Completed:
- 官网完整普查：26 分组、83 科室、1,343 关系/唯一 ID、9 纯护理排除、1,334 合规候选
- 10 人/10 科室 TRIAL，10 张官网本人职业照，详情和照片失败均为 0
- 新增照片 Schema、GDGH 专用适配器、工作簿照片列、Obsidian 相对图片引用能力和 FULL 硬熔断
- 总底表 XLSX/CSV/更新报告长度、时间戳和 SHA-256 前后完全一致
- 123 项单测、5 表视觉核验、10 图视觉核验和 FULL 负向门禁通过
Next:
- owner 审计 TRIAL 字段、分院归属、照片样本、容量估算和压缩/宽度方案
- 只有 owner 明确通过并下发 FULL_APPEND_AND_OBSIDIAN 后才解除 FULL 熔断
Constraints:
- 仅官网公开页面和本人职业照；禁第三方、患者影像/案例/评价、隐私、登录/验证码规避
- 不写总底表、不生成正式画像、不自行合并 PR 或关闭 Issue
Artifacts:
- D:\workspace\信息收集整理\work\广东省人民医院_trial_payload.json
- D:\workspace\信息收集整理\work\广东省人民医院_trial_doctors.csv
- D:\workspace\信息收集整理\work\广东省人民医院_trial_doctors.xlsx
- D:\workspace\信息收集整理\work\广东省人民医院_trial_report.md
- D:\workspace\信息收集整理\work\广东省人民医院_official_doctors_preview.png
- D:\workspace\信息收集整理\医生画像仓库\01_试点医院\广东省人民医院\照片
</Handoff_State>
