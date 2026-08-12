# Codex 下一步提示词

> 用途：Claude owner 或管理员写给 Codex developer 的最新可执行提示词。
> 当前状态：`REMOTE_PUSH_BLOCKED`。Issue #9 已按 owner 裁决停止试采并完成台账跳过记录及本地提交；GitHub API 连续超时触发熔断，只允许在连通性恢复后继续原分支推送、创建 PR 和回报证据。

## GitHub 身份与范围

- 仓库：`https://github.com/nancywrayg57-jpg/doctor-data-collection.git`
- Codex developer：`xtzhou247`
- Claude owner：`nancywrayg57-jpg`
- 工作分支：`codex/mhrj/issue-9-nysy-trial`
- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/9`
- Pull Request：待从当前分支创建

任何远端写入前必须确认登录身份为 `xtzhou247`。Codex 不直接推送或合并 `main`，不自行批准 PR。

## 当前动作

```text
Status: REMOTE_PUSH_BLOCKED
Phase: WAF_SKIP
LedgerSequence: 13
Hospital: 南方医科大学第三附属医院
City: 广州市
OfficialHomeURL: http://www.nysy.com.cn/
DoctorDirectoryURL: http://www.nysy.com.cn/cn/ksts/
ReviewStatus: 跳过-反爬拦截
Task: GitHub API 连通后重新核验 xtzhou247 身份、main 父提交与远端分支状态；推送本地提交，创建关联 Closes #9 的 PR；在 Issue #9 回报证据后停止。
```

## Owner 裁决与现场证据

- 裁决：Issue #9 owner 评论 `https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/9#issuecomment-5255218176`。
- 官网首页普通 GET：HTTP 412，`Server: CT2-WAAP`。
- Issue 指定入口普通 GET：HTTP 405，`Server: CT2-WAAP`。
- 两个入口均未取得真实页面。
- 未进行挑战应答、浏览器指纹模拟或其他绕过；未使用第三方来源。

## 已完成事实

- 入口普查与 10 位医生试采已按 owner 裁决停止。
- 未运行采集器，未创建试采 CSV/payload，未生成医生画像。
- 统一总底表保持 2,165 行，本院 0 行。
- 台账序号 13 已标记为 `跳过-反爬拦截`。
- 台账仅修改 8 个目标单元格；五个工作表已完成视觉核验，公式错误 0。
- 最新 ADR：`docs/architecture_decisions/2026-08-12_issue_9_nysy_waf_skip.md`。
- 本地提交：`349e288`（WAF 跳过工件）；尚未推送。
- GitHub API 已连续出现 TLS/TCP 连接超时，熔断期间不得重复远端命令。

## 当前门禁

1. 只处理 Issue #9、当前分支和恢复后由该分支创建的唯一 PR。
2. 创建 PR 后，只等待 `nancywrayg57-jpg` 对 WAF 跳过结果的审计、合并和 Issue 关闭。
3. PR 必须明确 `Closes #9`；不得自行批准或合并。
4. 只有 owner 审计通过、PR 已合并关闭、Issue #9 已关闭且必需 CI 成功后，才允许检查下一 Issue。
5. 通用单 Issue 监控在本轮提交推送和 PR/Issue 回报完成前保持 `PAUSED`。
6. 恢复远端动作前必须先确认 GitHub API 连通、身份为 `xtzhou247`、远端分支仍不存在且 `main` 未偏离本地父提交；任何冲突只报告，不强制覆盖。

## 合规红线

- 禁止挑战应答、验证码处理、浏览器指纹模拟、代理规避或任何反爬绕过。
- 禁止第三方平台、患者评价、隐私、登录后或非公开数据。
- 不自行寻找替代医生入口，不补造医生信息。
