# 2026-08-11 Claude 选院、试采审计与 Codex 完整执行

## 目标

将单医院流程固定为：Claude 选择目标并同时下发医院官网首页与医生目录入口，Codex 试采 10 位，Claude 审计试采，通过后 Codex 完成全量追加和 Obsidian 画像，完成后等待 Claude 选择下一家。

## 决策

1. Claude 读取官网入口台账的 `入口台账` 工作表和统一总底表，负责选择目标医院。
2. `人工复核结果=确认可采集` 是硬门禁；未确认医院直接跳过。A级仅为采集优先级，不能替代人工确认。
3. 已存在于统一总底表的医院直接跳过，避免重复追加。
4. Claude 必须在 `docs\agent_prompts\codex_next_prompt.md` 中写明台账序号、医院名称、城市、医院官网首页 URL 和医生目录入口 URL。
5. Codex 不自行选院。提示词缺少目标医院、医院官网首页或医生目录入口时停止等待。
6. `TRIAL` 阶段只试采 10 位医生，不写入总底表，完成后交给 Claude 审计。
7. Claude 结论为 `通过` 或 `有条件通过` 后，将提示词阶段改为 `FULL_APPEND_AND_OBSIDIAN`。Codex 无需管理员二次确认，完成全量采集、追加、检查和画像生成。
8. 正式追加和画像完成后不再设置第二次业务审计。Codex 向 Claude 回报并停止，下一家医院由 Claude 重新选择。
9. Obsidian 医生画像固定存储根目录为 `D:\workspace\信息收集整理\医生画像仓库\01_试点医院`。
10. 管理员当前只标注到序号 39 `广州市中医院`，官网首页为 `https://www.gzszyy.com/patient/`，医生目录入口为 `https://www.gzszyy.com/expert/`。完成序号 39 后停止，等待管理员更新台账标注。

## 已更新文件

- `D:\workspace\信息收集整理\Agent.md`
- `D:\workspace\信息收集整理\codex工程经验.md`
- `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集执行路线图.md`
- `D:\workspace\信息收集整理\docs\2026-08-10_医生画像采集任务需求确认.md`
- `D:\workspace\信息收集整理\docs\2026-08-10_Claude医生画像审计启动提示词.md`
- `D:\workspace\信息收集整理\docs\2026-08-10_远端Codex医生画像采集启动提示词.md`
- `D:\workspace\信息收集整理\docs\agent_prompts\codex_next_prompt.md`

## 当前状态

固定提示词入口当前为 `WAITING_FOR_CLAUDE_TARGET`，未预设下一家医院。Claude 启动后应现场读取台账和总底表，再下发当前目标，不得引用旧文档中的静态候选医院。

## 后续 Agent 最小上下文

1. 先读根目录 `Agent.md` 和本记录。
2. Claude 独占常规选院职责，Codex 只执行明确目标。
3. 只审计试采；通过后完整执行不再二审。
4. Codex 完成本院后停止等待 Claude。
5. 序号 39 是当前自动推进终点。
