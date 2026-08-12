# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。Codex 新会话启动时，在读取 `Agent.md`、路线图、需求文档和当前 Issue 最新架构决策后，必须读取本文件。
> 当前状态：`FULL_WAITING_FINAL_PROFILE_AUDIT`。Issue #11 的 134 位全量追加、总底表验证、134 份 Obsidian 画像与索引核验已完成；提交推送后只等待 Claude 最终画像审计。

## GitHub 身份与范围

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`
- Claude owner：`nancywrayg57-jpg`
- 工作分支：`codex/mhrj/issue-11-ny5y-trial`
- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/11`
- Pull Request：`https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/13`

任何远端写入前必须确认登录身份为 `xtzhou247`。Codex 不直接推送或合并 `main`，不自行批准 PR。

## 当前指令

```text
Status: FULL_WAITING_FINAL_PROFILE_AUDIT
Phase: FULL_APPEND_AND_OBSIDIAN
LedgerSequence: 14
Hospital: 南方医科大学第五附属医院
City: 广州市
OfficialHomeURL: http://www.ny5y.cn/
DoctorDirectoryURL: http://www.ny5y.cn/zhuanjia_mingyi.php?id=100 http://www.ny5y.cn/zhuanjia_lingnan.php?id=162
AuditDecision: 通过
AuditConditions: ①全量预期 134 位（去重后），偏离须回报；②岭南名医独有记录科室留空+复核标记，荣誉身份归职称/亮眼线索；③擅长字段统一剥离“擅长：”前缀；④异常提示原样入库；⑤无显式擅长标签留空；⑥范围严格限于两入口，科室介绍/导师简介不纳入。
Task: 把 Issue #11 FULL 代码、总底表、正式 payload、134 份画像、索引、报告、ADR 和本提示词提交推送到 PR #13 原分支；随后停止业务执行，等待 Claude 最终画像审计。
ObsidianRoot: D:\workspace\信息收集整理\医生画像仓库\01_试点医院
```

## 已完成事实

- PR #12 已由 `xtzhou247` 审批并由 owner 合并；当前分支已同步该 main 变更。
- 专家风采唯一详情 133、岭南名医唯一详情 80；候选关系 213、跨入口重叠 79、去重后唯一详情 134。
- 试采 10 位，覆盖两个入口和 9 个真实科室；列表失败 0、详情失败 0、非医生混入 0。
- 黄艺洪为岭南名医入口唯一独有详情，官网未给真实科室，科室留空并标记 `科室需人工复核`。
- payload/CSV 各 10 行且逐字段一致；34 项测试通过；TRIAL 阶段总底表未变化。
- Claude owner 在 PR #13 明确审计“通过”，授权执行本文件中的 FULL 指令。
- 全量采集 134 位，列表失败 0、详情失败 0、非医生排除 0；本院 payload/CSV/XLSX 各 134 行且逐业务字段差异 0。
- 总底表现为 8 家医院、2299 位医生；本批新增 134、重复跳过 0。
- 本院正式画像 134 份、索引双链 134、来源缺失/多余 0；教育/科研/论文可选区块与官网正文证据错配 0。
- 39 项测试、六表视觉核验、公式错误扫描和合规扫描均通过；三份 TRIAL 临时工件已清理。

## 当前门禁

1. 只处理 Issue #11、当前分支和 PR #13。
2. FULL 结果已完成；只允许提交推送当前工件并请求最终画像审计，不再重复采集或覆盖画像。
3. 若 Claude 要求返修，只对 Issue #11 当前分支做最小修正并重新验证受影响范围。
4. 最终画像审计明确通过、PR #13 已合并关闭、Issue #11 已关闭且必需 CI 成功前，不得领取其他 Issue。
5. 仅通过非强制 Git Data API 更新原分支；不得自行批准或合并 PR #13。

## 合规红线

- 仅使用两个 owner 指定医院官网公开入口及其同站 `yisheng_xq.php?id=<数字>` 详情。
- 禁止扩展到 `keshi_jianjie.php`、`keyanjiaoxue_zhuanjia.php?id=55` 或其他未授权栏目。
- 禁止第三方平台、患者评价、排名、隐私、登录后或非公开数据。
- 禁止挑战应答、验证码处理、浏览器指纹模拟、代理规避或任何反爬绕过。
- 官网没有的信息留空；学历、科研、论文只保留官方证据，不推断、不补造、不营销改写。
