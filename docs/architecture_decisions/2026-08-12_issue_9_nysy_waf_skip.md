# 2026-08-12 Issue #9 南方医科大学第三附属医院 WAF 跳过记录

## 目标与 owner 裁决

- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/9`
- 工作分支：`codex/mhrj/issue-9-nysy-trial`
- 台账序号：13
- 医院：南方医科大学第三附属医院
- 官网首页：`http://www.nysy.com.cn/`
- Issue 指定入口：`http://www.nysy.com.cn/cn/ksts/`

owner 在 Issue #9 评论 `issuecomment-5255218176` 明确裁决：若常规访问因反爬挑战无法取得真实页面，直接跳过该院，将序号 13 标记为 `跳过-反爬拦截`；禁止挑战应答、浏览器指纹模拟或其他绕过行为。回报证据后等待 owner 关闭 Issue，再下发下一家医院。

## 常规访问证据

2026-08-12 仅使用未附加挑战应答、指纹伪造或认证信息的普通 HTTP GET 复核：

| URL | HTTP 状态 | Server | 结论 |
|---|---:|---|---|
| `http://www.nysy.com.cn/` | 412 Precondition Failed | `CT2-WAAP` | 未取得真实官网页面 |
| `http://www.nysy.com.cn/cn/ksts/` | 405 Not Allowed | `CT2-WAAP` | 未取得 Issue 指定入口真实内容 |

本轮没有使用第三方来源，没有绕过反爬，没有尝试发现或替换其他医生入口。

## 已完成动作

1. 按 owner 裁决停止入口普查和 10 位医生试采。
2. 未运行采集器，未创建试采 CSV、payload 或医生记录。
3. 官网入口台账序号 13 已标记为 `跳过-反爬拦截`：
   - `入口台账!T14:X14` 写入 WAF 证据、跳过动作、复核结果、合规备注和更新时间；
   - `人工复核清单!G14:I14` 写入跳过动作、复核结果和 WAF 证据。
4. 仅增大上述两张表第 14 行高度，确保长文本可读；未重排或重做工作簿样式。
5. 统一总底表未写入，南方医科大学第三附属医院记录数保持 0。

## 数据状态与关键资产

- 统一总底表：2,165 行。
- 本院记录：0 行。
- 总底表 XLSX SHA-256：`95503CADE849592F13750D3F8AB059E5253CBA4CAEBBE0B9A2B1442D671916B1`。
- 入口台账修改前 SHA-256：`BB1F47BAEB4FC4B828CA51C7E8B1C35F42E165D3F5BBC97AAA3804B9AA6B76B6`。
- 入口台账修改后 SHA-256：`32E7D5BF072267D1727EE79BB7034CE3BD99C937EE57BD9DCCDD35CB1CE252CC`。

## 验证结果

- 台账内容差异严格限制为 8 个目标单元格；无其他单元格值变化。
- 五个工作表均完成渲染检查，`入口台账` 与 `人工复核清单` 完成聚焦视觉核验。
- 工作簿公式错误扫描：0。
- 总底表仍为 2,165 行，本院 0 行。
- `git diff --check` 与提交范围核验在推送前执行。

## 阻塞、根因、解决方法与防复发

### 1. 官方站点由 WAF 拦截普通访问

- 阻塞：官网首页返回 HTTP 412，Issue 指定入口返回 HTTP 405，响应服务器均为 `CT2-WAAP`，无法取得真实页面。
- 根因：站点 WAF/反爬策略拒绝当前常规 HTTP 访问；在合规边界内无法继续确认入口性质或采集医生信息。
- 解决：执行 owner 的显式跳过裁决，仅记录可复核的 HTTP 状态和响应服务器，不进行任何绕过尝试。
- 防复发：以后遇到同类 WAF，先用最小普通请求确认状态；若不能取得真实页面，立即停止采集，将站点、状态码、响应特征和未写入底表事实写入台账与 ADR，等待 owner 裁决。

### 2. 固定提示词滞后于当前工作分支

- 阻塞：恢复执行时 `docs/agent_prompts/codex_next_prompt.md` 仍记录已完成的 Issue #7，与当前 Issue #9 分支不一致。
- 根因：Issue #9 领取后尚未把新任务状态同步到固定提示词入口。
- 解决：以用户本轮明确的“继续执行 Issue #9”、GitHub Issue 正文、owner 评论和当前分支四方证据恢复执行，并将固定提示词更新为 Issue #9 的 WAF 跳过等待状态。
- 防复发：每次领取 Issue 后立即在首个提交前更新固定提示词；通用监控继续把分支、Issue、PR、提示词和 ADR 一致性作为硬门禁。

### 3. GitHub API 传输连续超时

- 阻塞：本地提交完成后，Git Data API 推送连续三轮无法通过前置只读检查；前两轮为 TLS handshake timeout，第三轮在有限重试后为 `20.205.243.168:443` TCP 连接超时。
- 影响：失败均发生在 `gh api user` 或读取 `main` 引用阶段；没有上传 blob、创建 GitHub commit、创建远端分支、PR 或 Issue 评论。
- 根因假设：当前 Windows 主机到 `api.github.com:443` 的链路临时不可达或不稳定，而不是仓库权限、身份、提交内容或 Git Data API Schema 错误。失败前已成功核验身份为 `xtzhou247`，并确认远端 `main=d5422061d1fb38de9456e8956e549f2c85929953`。
- 已采取措施：先做单次最小重试，再给临时推送器增加有限传输重试和“引用创建结果不明时先只读核验”保护；网络仍未恢复。
- 熔断与恢复：按 Agent.md 连续失败上限停止远端命令。待 GitHub API 连通后，从 `gh api user --jq .login`、远端分支不存在性和 `origin/main` 父提交一致性重新核验；只允许非强制 Git Data API 推送当前本地提交，不得改用绕过既有门禁的强制推送。

## 当前结论与下一步

Issue #9 已按 owner 裁决完成本地跳过记录并形成提交，但 GitHub API 网络熔断导致尚未推送。连通性恢复后的下一步仅允许：重新核验 `xtzhou247` 身份与远端状态，非强制推送原分支，创建关联 `Closes #9` 的 PR，并在 Issue 回报 WAF 证据。随后等待 owner 审计、合并 PR 并关闭 Issue；在这些门禁完成前不得领取其他 Issue。

<Handoff_State>
Target: Issue #9 南方医科大学第三附属医院 WAF 跳过审计
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/9
Branch: codex/mhrj/issue-9-nysy-trial
Phase: REMOTE_PUSH_BLOCKED
Completed:
- 普通 GET 复核官网首页 HTTP 412、指定入口 HTTP 405，Server 均为 CT2-WAAP
- 未绕过反爬、未运行试采、未写入统一总底表
- 台账序号 13 已标记为 跳过-反爬拦截
CurrentFacts:
- 总底表 2165 行，本院 0 行
- 工作簿公式错误 0，五表视觉核验完成
Next:
- GitHub API 连通后重新核验身份、main 父提交与远端分支状态
- 通过非强制 Git Data API 推送当前本地提交
- 创建关联 Closes #9 的 PR，并在 Issue 回报证据
- 等待 owner 审计、合并 PR、关闭 Issue
Constraints:
- 禁止挑战应答、浏览器指纹模拟或任何反爬绕过
- 不自行批准或合并 PR
- 不领取其他 Issue
Artifacts:
- 医生画像仓库/99_资料来源/珠三角三甲医院官网入口台账.xlsx
- work/南方医科大学第三附属医院_waf_block_report.md
</Handoff_State>
