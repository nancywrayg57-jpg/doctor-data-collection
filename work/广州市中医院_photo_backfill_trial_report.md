# Issue #67 广州市中医院照片补录 TRIAL 报告

## 结论

- 阶段：`TRIAL_READY_FOR_OWNER_AUDIT`
- 范围：本院 415 行，TRIAL 前照片字段全空。
- 固定样本：10 人 / 10 个科室首原子；职称分层 `正高 3 / 副高 3 / 其他 4`。
- 实采：10/10；问题 0；熔断问题 0。
- 照片总字节：2,114,508；最小 19,404；中位数 224,293；平均 211,451；最大 279,273。
- 大小分桶：<200KiB=2、200KiB-1MiB=8、1-5MiB=0、5-20MiB=0；超过 5 MiB：0；超过 20 MiB：0。
- 估算 415 行容量：约 83.69 MiB（仅容量估算，不代表 FULL 实际结果）。

## 来源与排除边界

- 官网首页：<https://www.gzszyy.com/>
- 医生目录：<https://www.gzszyy.com/expert/>
- 详情来源仅接受 `https://www.gzszyy.com/expert/<年份>/<ID>.html`。
- 照片仅取详情 `.doctor-resume div.doctor-img` 唯一 `img[src]`，并仅接受页面实际引用的 `https://oss.gzszyy.com/<YYYYMMDD>/<数字>.<格式>`。
- 图片请求携带对应详情页 Referer；不构造或探测页面未引用路径。
- `div.qr-img`、`static.gzszyy.com/images/`、空 `src` 均不进入候选。
- 占位检测沿用小 GIF 双侧边界；未单凭格式或尺寸判定占位。

## 固定样本

| 姓名 | 科室 | 职称 | 字节数 | 尺寸 | SHA-256 |
|---|---|---|---:|---:|---|
| 叶穗林 | 名医堂 | 主任中医师 | 19,404 | 288×400 | `c3c8347426b0332b3905bc2c3d00042acd84cb1f75f921c93a30b21bdd8f0457` |
| 吴薏婷 | 肿瘤一区 | 主任中医师 | 279,273 | 1152×1600 | `ca9bcb32a766027a1b1dd238d1216ba4791a41ea93ba88c90cbe277cb63f3ea5` |
| 林少贞 | 针灸科 | 主任中医师 | 247,360 | 1152×1600 | `0d3e956b8063ed352709ac61e007abf4b82cbe4bffc361e91efb0c663d5a8a13` |
| 陈庆强 | 肿瘤二区 | 副主任中医师 | 226,780 | 1152×1600 | `31a4c1590dba5e8a1f6f382b3c22d980b529cca64d1ff506749727f8a3c3adb8` |
| 欧阳智 | 脑病科（神经内科） | 副主任中医师 | 237,663 | 1152×1600 | `7d5a95c99a7c00e7351a360c29d9e79b9b0a4d130003257bc17e20dfb86e9359` |
| 周艳利 | 肾病科 | 副主任中医师 | 221,414 | 1152×1600 | `1854814b6bd7809a4a3932493c73f528b7330fea1c93eaec1314c8bae1c9828c` |
| 夏思 | 血液科 | 主治医师 | 190,372 | 2000×1333 | `b460cd7e7b165327d2d7a118d6e88ce02369fc64864e1ae399d9d0f6fbb7b3c5` |
| 赵鸿 | 重症医学科 | 主治医师 | 221,807 | 1152×1600 | `26419fd234293aca4ee41ba2ebacb220531034a98d6fa6f5e853e2722f1464bc` |
| 金华伟 | 肺病科（呼吸内科） | 医师 | 209,904 | 1152×1600 | `c0d934ff82d581ba1ec42fd412c4813ab983b533e2c8b4d428975c351a2f79d2` |
| 陈燕珊 | 内分泌科 | 医师 | 260,531 | 1152×1600 | `23c4ffbe5c4e24f6e21b4130695782eb4c6da72dfe73aaee0b0a00af09532859` |

## 正式资产保护

- TRIAL 仅写入 `work` 独立工件；入口台账、总底表三载体、总底表更新报告、415 份画像、索引和正式照片目录前后快照一致。
- 本院 415 份画像与 `_索引.md` 均保留 `<!-- AUTO-GENERATED-BY: work/generate_obsidian_profiles.py -->`；TRIAL 前零图片引用，正式照片目录不存在。
- 联系表：`D:\workspace\信息收集整理\work\广州市中医院_photo_backfill_trial_contact_sheet.jpg`。
- 联系表视觉结论：`PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。

## 停止点

TRIAL 工件完成后停止，等待 `nancywrayg57-jpg` 审计联系表、逐图来源和大小分布。未取得关联 PR 中 owner 明确 `通过` / `有条件通过` 且切换为 `FULL_APPEND_AND_OBSIDIAN` 前，不得修改正式资产。
