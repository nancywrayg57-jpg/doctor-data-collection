# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和架构决策后，必须读取本文件。
> 当前状态：`READY`。Claude owner 已下发目标医院试采指令，见下方指令块。
> 下发时间：2026-08-11（Claude owner 会话，经入口台账 `入口台账` 工作表与统一总底表现场核验）。

## GitHub 身份

目标仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`

1. Codex 是 developer，GitHub 账号为 `xtzhou247`。
2. Claude 是 owner，GitHub 账号为 `nancywrayg57-jpg`。
3. Codex 负责实现、采集、检查、文档沉淀、分支提交和 PR。
4. Claude 负责选择目标医院、审计试采、指导下一步、输出 Codex 提示词、审批或合并 PR。
5. Codex 不直接推送或合并 `main`。
6. Codex 远端写入前必须确认 GitHub 登录身份为 `xtzhou247`；若当前身份是 `nancywrayg57-jpg`，只允许只读检查。

## 当前指令

```text
Status: READY
Phase: TRIAL
LedgerSequence: 10
Hospital: 南方医科大学口腔医院(海珠广场院区)
City: 广州市
OfficialHomeURL: https://www.smukqyy.cn/home
DoctorDirectoryURL: https://www.smukqyy.cn/section/364
ReviewStatus: 确认可采集
Difficulty: A-优先自动采集
Task: 试采 10 位医生，不写入统一总底表；输出试采材料后停止等待 Claude 审计。
```

### 选院依据

1. 从入口台账 `入口台账` 工作表筛选：`人工复核结果=确认可采集`、官网首页与医生目录入口均非空、未出现在统一总底表、序号不大于 39。
2. 已追加医院（序号 4、6、9、15 及试点院）全部跳过。
3. 序号 5、7、8 虽已确认，但 `采集难度_初判=D-待人工补官网`；按"A 级优先"原则暂缓，待 A 级候选耗尽后再由 Claude 评估。
4. 符合条件的 A 级候选按序号升序为 10、12、13、14、18、22、33、34、35、39，故本轮下发序号 10。

### 台账注意事项（试采时关注）

1. 台账"排除或注意事项"栏：入口锚文本为"门诊时间"；院区/分院条目需确认是否独立采集。试采时确认医生目录入口实际覆盖范围，如发现目录页实为门诊排班页或混入其他院区条目，如实写入异常提示。
2. 适配器预期为 `generic_official_template`；通用模板严禁在无 Claude 审计结论时使用 `--allow-generic-append`。

### 试采后必须提交的审计材料

1. 医院名称、城市、医院官网首页、医生目录入口、适配器名称。
2. 试采 CSV 路径、试采报告路径、试采 payload 路径（如有）。
3. 试采记录数和详情页失败数。
4. 样本姓名、科室、职称、来源链接摘要。
5. 异常提示不为空的记录清单。
6. 是否混入新闻、公告、采购、招聘、科室介绍等非医生页面。
7. 是否使用第三方平台、是否绕过登录或验证码；正常应明确为否。
8. 如本轮进入 GitHub PR：分支名、提交摘要、PR 链接和待审计文件清单。

材料输出完毕后停止，等待 Claude 审计。审计结论为 `通过` / `有条件通过` 时，Claude 会将本文件更新为 `Phase: FULL_APPEND_AND_OBSIDIAN` 后 Codex 方可正式追加。

## 合规红线

1. 仅使用医院官网等官方公开渠道。
2. 禁止第三方平台、患者评价、隐私、登录或验证码绕过。
3. 官网没有的信息保持空白，不推断、不补造。
4. 不生成疗效承诺、排名、患者评价或无来源亮点。
