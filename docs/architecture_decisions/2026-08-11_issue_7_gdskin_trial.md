# 2026-08-11 Issue #7 南方医科大学皮肤病医院试采

## 目标与门禁

按 GitHub Issue #7 对南方医科大学皮肤病医院官网专家团队 10 个入口逐入口普查，按官方医生详情 URL 跨入口去重后试采 10 位医生，样本覆盖至少 3 个分类；只生成试采审计材料，不写入统一总底表。

- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/7`
- 台账序号：12
- 城市：广州市
- 官网首页：`https://www.gdskin.com/`
- 适配器：`gdskin_aspnet_expert`
- 工作分支：`codex/mhrj/issue-7-gdskin-trial`
- Codex developer：`xtzhou247`
- Claude owner：`nancywrayg57-jpg`
- 当前阶段：`TRIAL`；Claude 明确审计通过前，禁止正式追加和生成本院正式画像

## 入口普查结果

官网列表使用 ASP.NET GridView，医生详情 URL 形如 `ShowNews.ASPX?ID=<数字>`；906 通过 ASP.NET `__doPostBack(..., 'Page$2')` 提供第二页。

| 分类 | 入口 ID | 页面性质 | 列表页 | 唯一医生详情 URL | 归属 |
|---|---:|---|---:|---:|---|
| 首席专家 | 901 | 官网 ASP.NET GridView 专家列表 | 1 | 1 | 南方医科大学皮肤病医院官网专家团队栏目 |
| 知名专家 | 902 | 官网 ASP.NET GridView 专家列表 | 1 | 3 | 南方医科大学皮肤病医院官网专家团队栏目 |
| 皮肤内科 | 906 | 官网 ASP.NET GridView 专家列表 | 2 | 29 | 南方医科大学皮肤病医院官网专家团队栏目 |
| 外阴皮肤病/性病科 | 910 | 官网 ASP.NET GridView 专家列表 | 1 | 7 | 南方医科大学皮肤病医院官网专家团队栏目 |
| 整形美容外科 | 913 | 官网 ASP.NET GridView 专家列表 | 1 | 8 | 南方医科大学皮肤病医院官网专家团队栏目 |
| 中医皮肤科 | 915 | 官网 ASP.NET GridView 专家列表 | 1 | 14 | 南方医科大学皮肤病医院官网专家团队栏目 |
| 激光美肤中心 | 917 | 官网 ASP.NET GridView 专家列表 | 1 | 6 | 南方医科大学皮肤病医院官网专家团队栏目 |
| 皮肤外科 | 921 | 官网 ASP.NET GridView 专家列表 | 1 | 4 | 南方医科大学皮肤病医院官网专家团队栏目 |
| 儿童皮肤科 | 922 | 官网 ASP.NET GridView 专家列表 | 1 | 5 | 南方医科大学皮肤病医院官网专家团队栏目 |
| 珠江新城医学美容中心 | 924 | 官网专家团队分类页，当前无可采医生详情 | 1 | 0 | 南方医科大学皮肤病医院·珠江新城医学美容中心 |

现场未发现入口属于独立挂牌机构或非本院实体；全部页面保持在 `www.gdskin.com` 同站专家团队栏目。924 虽为珠江新城中心分类，但当前没有医生详情，仍作为零记录入口留痕，不自行剔除。

## 去重与排除

- 10 个入口内唯一详情 URL 关系数：77。
- 以详情 ID 归一化后唯一候选：77。
- 本次现场没有同一详情 URL 跨入口重复，重复清单为空；去重逻辑和完整链路测试仍保留。
- 917 另发现 `王辉 主管护师`，详情 `https://www.gdskin.com/ShowNews.ASPX?ID=5737`，因身份不属于医生角色已排除，未参与 6 位医生计数和试采。
- 列表页失败 0，详情页失败 0，非官方链接 0。

## 试采命令与结果

```powershell
python .\work\collect_official_doctors_batch.py `
  --hospital "南方医科大学皮肤病医院" `
  --trial-only --max-doctors 10 `
  --min-departments 3 --min-entry-categories 3 `
  --max-pages 5 --no-xlsx `
  --entry-url <Issue #7 指定的 10 个官网入口>
```

- 模式：`trial_only`
- 样本：10 位，10 个唯一官方详情 URL
- 样本入口覆盖：9 类，超过至少 3 类门禁
- 详情失败：0
- 异常提示不为空：0
- 试采 XLSX：未生成（使用 `--no-xlsx`）
- `master_updated=false`

## 样本摘要

| 序号 | 姓名 | 分类 | 职称摘要 | 擅长摘要 | 来源 |
|---:|---|---|---|---|---|
| 1 | 杨立刚 | 外阴皮肤病/性病科 | 主任医师 | 性传播疾病、感染及过敏性皮肤病、面部皮炎 | `ShowNews.ASPX?ID=3852` |
| 2 | 何仁亮 | 皮肤外科 | 主任医师、硕士研究生导师 | 皮肤瘢痕与创面、皮肤肿瘤、皮肤血管 | `ShowNews.ASPX?ID=3854` |
| 3 | 杨斌 | 知名专家 | 主任医师、博士生导师、院长 | 免疫性皮肤病、损容性皮肤病 | `ShowNews.ASPX?ID=3847` |
| 4 | 陈永锋 | 知名专家 | 主任医师、博士研究生导师 | 银屑病、结缔组织病、自身免疫性大疱病、皮肤肿瘤等重症疑难皮肤病 | `ShowNews.ASPX?ID=3848` |
| 5 | 顾有守 | 首席专家 | 主任医师、教授、首席专家 | 疑难及重症皮肤病 | `ShowNews.ASPX?ID=3829` |
| 6 | 曲永彬 | 中医皮肤科 | 主任医师、医学硕士 | 银屑病、痤疮、黄褐斑 | `ShowNews.ASPX?ID=4324` |
| 7 | 裴小平 | 儿童皮肤科 | 副主任医师、医学硕士 | 儿童皮肤病、遗传性皮肤病、特应性皮炎 | `ShowNews.ASPX?ID=5002` |
| 8 | 鲜华 | 整形美容外科 | 副主任医师、医学博士 | 毛发相关性皮肤病、皮肤瘢痕、脂肪加/减精雕塑形 | `ShowNews.ASPX?ID=4287` |
| 9 | 刘振锋 | 激光美肤中心 | 主任医师、医学博士、硕士研究生导师 | 痤疮、色素性疾病、血管性疾病、皮肤激光美容、面部年轻化 | `ShowNews.ASPX?ID=5000` |
| 10 | 谷梅 | 皮肤内科 | 主任医师、医学硕士 | 过敏性皮肤病、痤疮及疤痕 | `ShowNews.ASPX?ID=3849` |

## 字段归位与管理员新增口径

官网 `.labelContent` 部分详情页不写显式 `简介：`，而是用相邻 `<p>` 分隔专长与个人履历。初版压平文本后导致刘振锋的学历、科研和论文内容进入 `擅长诊疗方向摘录`。

管理员 2026-08-11 明确授权：允许收录官网公开的学历、科研和论文段落，并允许在画像模板新增对应区块。落地口径如下：

1. `擅长诊疗方向摘录` 只保留专长/擅长段落。
2. 后续官方段落保留在 `详情正文摘录`，学历、科研、论文信息不会丢失。
3. `亮眼经历线索` 仍只摘取可追溯官方证据，并执行导航污染检测。
4. 画像模板和生成器增加可选的 `教育与进修经历`、`科研项目与成果`、`论文与学术产出` 区块；仅在官方正文命中时渲染，不推断、不补造、不生成空区块。
5. 当前仍为 TRIAL，不生成本院画像；上述画像能力只随代码和模板进入 Claude 审计。

修正后，10 位样本的专长字段中学历/科研/论文混入数为 0；刘振锋的专长恢复为 5 项方向，`详情正文摘录` 仍包含博士毕业、科研基金和 SCI 论文证据。

## 异常与合规声明

- 样本异常提示：无。
- 已排除非医生候选：1 位主管护师，已在报告单列。
- 导航污染扫描：科室、擅长、亮眼经历、列表简介、详情正文命中 0。
- 未使用第三方平台，未采集患者评价、排名、问诊内容或私人联系方式。
- 未绕过登录、验证码、反爬或权限限制。
- 官网没有展示的字段保持空白，不推断、不补造。
- 学历、科研、论文仅保留官网原文证据，不改写为疗效承诺或营销结论。

## 总底表安全证明

试采前后以下四项 SHA-256 完全一致：

| 资产 | SHA-256 |
|---|---|
| 总底表 XLSX | `2475FB7891F2F75A02FEB7EDA1485CEC107C9AB4BE26F8FFEF9E919FCC0BD9F5` |
| 总底表 CSV | `8932FD9E7AAC3203E51F22FD0D59338ACF7567BDDEE9772DFB60AE003E39107C` |
| 总 payload | `9D7536208E30E7E5D68FE71CB436ED3486E6254C50EFB1BA421E13CBAFFA6BEB` |
| 总底表更新报告 | `BF661CA9D3870F3A0688B65522B8CB4D2954BC5DC19D71CC969F73726A7A36B0` |

## 验证结果

- Python 编译通过。
- 采集器与画像生成器共 23 项测试全部通过。
- 完整 `collect_generic()` 测试覆盖多入口、跨入口重复、非医生排除、普查表和样本分类覆盖。
- 新增无 `简介：` 标签但有相邻 `<p>` 的字段边界测试。
- 新增画像三个可选官方证据区块的提取与渲染测试。
- payload/CSV 均为 10 行，逐字段差异 0。
- 10 个来源 URL 唯一且全部匹配 `https://www.gdskin.com/ShowNews.ASPX?ID=<数字>`。
- 未生成试采 XLSX；未修改或生成正式画像。
- `git diff --check` 通过。

## 阻塞、解决方法与防复发

### 1. 重复统计循环导致补丁误插入其他采集器

- 根因：多个采集器具有相同的 `warning_counter` 循环，缺少函数级唯一锚点。
- 解决：以 `generic details:` 和多入口返回字段联合定位，将 GDSKIN 聚合块只保留在 `collect_generic()`。
- 预防：涉及重复函数结构的补丁必须使用函数名和函数内唯一字符串联合锚点；补丁后用 `rg` 证明定义只出现于预期函数。

### 2. 辅助函数测试通过但完整返回作用域错误

- 根因：初版只测试 URL、GridView 和分页辅助函数，没有直接调用 `collect_generic()`。
- 解决：新增 mock 完整链路测试，直接断言 payload 的普查、去重、排除、覆盖和 rows。
- 预防：新适配器必须至少有一项从入口读取到完整 payload 返回的集成级测试。

### 3. 测试把有序输出误当业务门禁

- 根因：采样行返回前会按优先级/科室排序，入口分类顺序不稳定；Issue 只要求覆盖集合。
- 解决：使用无序分类集合和采集入口集合断言。
- 预防：只有协议明确要求顺序时才断言列表顺序；覆盖门禁使用集合或计数。

### 4. ASP.NET 详情页无简介标签导致专长跨段落

- 根因：`compact_visible_text()` 压平 `<p>`，正则只在显式 `简介：` 处停止。
- 解决：优先按非空 `<p>` 解析；专长只取当前段，后续段落进入简介；无段落结构时保留旧标签回退。
- 预防：字段抽取测试必须覆盖“显式标签”和“仅 DOM 段落分隔”两种结构；长期信息不允许挤入专长字段。

### 5. 验证脚本使用 PowerShell 简写造成解析失败

- 根因：`?姓名` 被解析为命令名。
- 解决：改用完整 `Where-Object { $_.姓名 -eq ... }`。
- 预防：包含中文属性名的交付验证脚本不使用无空格管道简写。

## 当前结论与下一步

Issue #7 的 TRIAL 材料已准备完毕，下一步仅允许：精确提交代码、测试、模板、试采 CSV/payload/报告、ADR 和固定提示词，通过 GitHub Git Data API 推送工作分支，创建引用 Issue #7 的 PR，请求 Claude owner 给出 `通过`、`有条件通过` 或 `不通过`。Claude 明确通过前不得正式追加、生成本院画像或领取其他 Issue。

## 工件

- `work/collect_official_doctors_batch.py`
- `work/generate_obsidian_profiles.py`
- `work/tests/test_collect_official_doctors_batch.py`
- `work/tests/test_generate_obsidian_profiles.py`
- `work/南方医科大学皮肤病医院_trial_doctors.csv`
- `work/南方医科大学皮肤病医院_trial_payload.json`
- `work/南方医科大学皮肤病医院_trial_report.md`
- `医生画像仓库/模板/医生画像模板.md`
- `docs/architecture_decisions/2026-08-11_issue_7_gdskin_trial.md`
- `docs/agent_prompts/codex_next_prompt.md`

<Handoff_State>
Target: Issue #7 南方医科大学皮肤病医院试采
GitHubIssue: https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/7
Phase: TRIAL_WAITING_CLAUDE_AUDIT
Completed:
- 已逐入口普查 10 个官网专家团队入口
- 已按详情 URL 去重后试采 10 位，覆盖 9 个分类
- 已排除 917 的主管护师，924 已以零记录入口留痕
- 已修正无简介标签页面的专长/简介段落归位
- 已增加官网学历、科研、论文的可选画像区块，但未生成本院画像
- 已验证总底表四项资产未变化
CurrentFacts:
- 入口候选关系 77，去重后唯一候选 77，跨入口重复 0
- 样本 10 位、10 个唯一官方来源、详情失败 0、异常提示 0
- 23 项测试通过，CSV/payload 逐字段差异 0
Next:
- 使用 Git Data API 推送分支并创建 PR
- 等待 Claude 试采审计；通过前禁止正式追加和画像生成
Constraints:
- 仅医院官网公开渠道
- 不使用第三方平台、不绕过登录/验证码、不采集患者隐私
- 学历、科研、论文可收录，但必须保留官方证据并放入对应字段/画像区块
- 不自行批准或合并 PR，不领取其他 Issue
Artifacts:
- work/南方医科大学皮肤病医院_trial_doctors.csv
- work/南方医科大学皮肤病医院_trial_payload.json
- work/南方医科大学皮肤病医院_trial_report.md
- docs/architecture_decisions/2026-08-11_issue_7_gdskin_trial.md
</Handoff_State>
