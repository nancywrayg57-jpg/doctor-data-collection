# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。
> 当前状态：`TRIAL_WAITING_CLAUDE_AUDIT`。Issue #11 的入口普查、10 位试采、测试和总底表未变化核验已完成；提交推送并创建 TRIAL PR 后，只等待 Claude 审计。

## GitHub 身份与范围

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`
- Claude owner：`nancywrayg57-jpg`
- 工作分支：`codex/mhrj/issue-11-ny5y-trial`
- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/11`
- Pull Request：`https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/13`

任何远端写入前必须确认登录身份为 `xtzhou247`。Codex 不直接推送或合并 `main`，不自行批准 PR。

## 当前动作

```text
Status: TRIAL_WAITING_CLAUDE_AUDIT
Phase: TRIAL
LedgerSequence: 14
Hospital: 南方医科大学第五附属医院
City: 广州市
OfficialHomeURL: http://www.ny5y.cn/
DoctorDirectoryURL: http://www.ny5y.cn/zhuanjia_mingyi.php?id=100 http://www.ny5y.cn/zhuanjia_lingnan.php?id=162
ReviewStatus: 确认可采集
Task: 把 Issue #11 TRIAL 代码、测试、入口普查表、试采 CSV/payload/报告、ADR 和本提示词提交推送并创建关联 PR；随后停止业务执行，等待 Claude 试采审计。
```

## 已完成事实

- 两入口普通 HTTP GET 均为 200，无登录、验证码或反爬挑战。
- 专家风采：原始详情链接 134，唯一详情 133，单页。
- 岭南名医：原始/唯一详情 80，单页。
- 候选关系 213，跨入口重叠 79，去重后唯一详情 134。
- 试采 10 位，覆盖两个入口、9 个真实科室；列表失败 0、详情失败 0。
- 黄艺洪为岭南独有详情，官网没有给真实科室，科室留空并标记 `科室需人工复核`。
- 10 个来源均严格匹配同站 `yisheng_xq.php?id=<数字>`；未纳入科室介绍或研究生导师栏目。
- payload/CSV 各 10 行，逐字段差异 0；34 项测试通过。
- 统一总底表 XLSX/CSV、总 payload、更新报告哈希前后不变，本院仍为 0 行。
- TRIAL PR：`https://github.com/nancywrayg57-jpg/doctor-data-collection/pull/13`；仅使用 `Refs #11` 关联，未提前关闭 Issue。
- 最新 ADR：`docs/architecture_decisions/2026-08-12_issue_11_ny5y_trial.md`。

## 当前门禁

1. 只处理 Issue #11、当前分支和后续对应 PR。
2. TRIAL PR 创建后，只等待 `nancywrayg57-jpg` 对试采给出明确“通过”“有条件通过”或“不通过”。
3. 只有 Claude 明确通过且本提示词切换为 `FULL_APPEND_AND_OBSIDIAN` 后，才允许全量追加、总底表验证和本院画像生成。
4. 审计通过前不得使用 `--allow-generic-append`，不得生成本院正式画像，不得领取其他 Issue。
5. 若 Claude 要求返修，只对 Issue #11 当前分支做最小修正，并继续使用非强制 Git Data API 更新远端引用。

## 合规红线

- 仅使用两个 owner 指定医院官网公开入口及其同站 `yisheng_xq.php?id=<数字>` 详情。
- 禁止扩展到 `keshi_jianjie.php`、`keyanjiaoxue_zhuanjia.php?id=55` 或其他未授权栏目。
- 禁止第三方平台、患者评价、排名、隐私、登录后或非公开数据。
- 禁止挑战应答、验证码处理、浏览器指纹模拟、代理规避或任何反爬绕过。
- 官网没有的信息留空；学历、科研、论文只保留官方证据，不推断、不补造、不营销改写。
