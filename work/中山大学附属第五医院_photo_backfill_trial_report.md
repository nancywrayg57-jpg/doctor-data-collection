# Issue #61 中山大学附属第五医院照片补录 TRIAL 报告

## 执行结论

- 阶段：`TRIAL_READY_FOR_OWNER_AUDIT`；范围：413 行 / 413 个唯一官网详情 URL。
- 固定分层样本：10 人，覆盖 10 个科室，职称层级 `{"正高": 3, "副高": 3, "其他": 4}`。
- 实采：10；熔断问题：0/10（0.00%）。
- 仅请求详情页 `field-featured-media` 容器自身引用的 `styles/watermark` 派生图，逐字保留 `itok`；图片请求携带对应详情页 Referer；未构造或探测页面未引用原图路径。
- 未使用第三方来源，未绕过登录、验证码、反爬或权限限制。

## 大小分布

| 指标 | 结果 |
|---|---:|
| 总字节 | 3570848 |
| 最小 | 74834 |
| 中位数 | 325595 |
| 平均 | 357084 |
| 最大 | 1109955 |
| 超过 200 KiB | 6 |
| 超过 5 MiB | 0 |
| 413 行估算 | 140.64 MiB |

分桶：`{"200KiB-1MiB": 5, "<200KiB": 4, "1-5MiB": 1}`。

## 逐图三重核验与尺寸

| 姓名 | 科室 | 层级 | 主职称 | 文件名 | 字节 | 尺寸 | SHA-256 | 页面引用照片 |
|---|---|---|---|---|---:|---:|---|---|
| 丁立 | 感染病防治中心 | 正高 | 主任医师 | 丁立-感染病防治中心-主任医师-中山大学附属第五医院.jpg | 337311 | 800×1173 | 0dce45a0cc4a0f362ebd62f4d7fe0b29b2c43981a068f8364316ba6eca3f64cc | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2026-01/%E4%B8%81%E7%AB%8B20260114.jpg?itok=05NNMaX8 |
| 王莉 | 产科 | 正高 | 主任医师 | 王莉-产科-主任医师-中山大学附属第五医院.jpg | 91058 | 390×538 | 325c685b5ce081eb403c2e98ab1b845f23bb3d5251a6881ee9647e98e664b11e | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-07/1612726913074176486.jpg?itok=XaiKihUC |
| 何欢欢 | 分子影像中心 | 正高 | 研究员 | 何欢欢-分子影像中心-研究员-中山大学附属第五医院.png | 139452 | 358×441 | 4d04102ad969a66c7a98545c98b4718f1001890bf51843c37f618d090c177619 | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-07/1532281060787269620.png?itok=d7SsoPuq |
| 韩宗萍 | 临床营养科 | 副高 | 副主任医师 | 韩宗萍-临床营养科-副主任医师-中山大学附属第五医院.jpg | 327433 | 1181×1656 | d88fa95e914fd179b077f382f566e1c5d25a0b15a9b0df16f738327276ab7e8b | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-11/20240723170705207.jpg?itok=t8sBWUQb |
| 孙一 | 口腔科 | 副高 | 副主任医师 | 孙一-口腔科-副主任医师-中山大学附属第五医院.jpg | 1109955 | 1906×2668 | f4465894450ce933dd084255637206e47862434cac34d819927d0a7fcc8e063b | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2025-04/20250410162834341.jpg?itok=9Xhx2D7i |
| 林子玲 | 康复医学科 | 副高 | 副主任医师 | 林子玲-康复医学科-副主任医师-中山大学附属第五医院.jpg | 74834 | 390×567 | 71eddf34ed89eed8dd632721d7061a8ac8251a16bb0f475f8ad70e26f7bbd088 | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-07/1595378134940594203.jpg?itok=gqJkBoGL |
| 张玉龙 | 中医科 | 其他 | 医师 | 张玉龙-中医科-医师-中山大学附属第五医院.jpg | 386158 | 896×1228 | e530a3bed5244e4cbdbe9dde37d8221aa39e1bc073d902ff3bc0e305f562bbd1 | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-07/20231227153436028.jpg?itok=1QiSP_cz |
| 徐晓露 | 乳腺肿瘤内科 | 其他 | 医师 | 徐晓露-乳腺肿瘤内科-医师-中山大学附属第五医院.jpg | 591199 | 1000×1500 | 898784303439634a2270c6494bf738400ef5b459633ec31dc75e0f1491b880bc | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2026-07/%E5%BE%90%E6%99%93%E9%9C%B2%EF%BC%88185284%EF%BC%8920260708.jpg?itok=Qo_g9Y4Z |
| 余圆圆 | 创面修复与烧伤外科 | 其他 | 主治医师 | 余圆圆-创面修复与烧伤外科-主治医师-中山大学附属第五医院.png | 323758 | 424×591 | 6f75f49372bf191dfa3c04d93843445f7fb1a75695fccc1402103541b675f442 | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-07/20240521151603060.png?itok=Qwzp8mrZ |
| 刘天民 | 心血管内科 | 其他 | 主治医师 | 刘天民-心血管内科-主治医师-中山大学附属第五医院.jpg | 189690 | 593×756 | e609d34849e2364e0609ba126d739f3e96c966867597329a0b66be6ea46613bb | https://www.sysu5.cn/sites/default/files/styles/watermark/public/2024-07/1594578235279441829.jpg?itok=C85Egj3W |

详细 HTTP、引用属性、魔数和逐图命名清单见：`D:\workspace\信息收集整理\work\中山大学附属第五医院_photo_backfill_trial_manifest.csv` 与 `D:\workspace\信息收集整理\work\中山大学附属第五医院_photo_backfill_trial_payload.json`。

## 占位图检测

- 复用 Issue #59 口径：仅对小于 40 KiB 的 GIF 执行 `nopic/noimage/placeholder` 路径标记或低色板且浅灰中性像素占比至少 70% 判定；彩色小 GIF 不因体积小而误判。
- 页面级路径标记只作用于唯一照片容器引用；公共页头、招聘图、二维码和页脚图不属于候选容器。

## 联系表人工核验

- 联系表：`D:\workspace\信息收集整理\work\中山大学附属第五医院_photo_backfill_trial_contact_sheet.jpg`。
- 当前状态：`MANUAL_CONTACT_SHEET_REVIEW_PASSED`。
- 判定目标：10 张均应为对应医生的单人职业照，不得出现占位图、公共装饰图、二维码、患者、儿童或合影。

## 受保护正式资产零变更

| 文件 | 字节 | SHA-256 |
|---|---:|---|
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院官网入口台账.xlsx` | 40025 | `d6b08b3f284654024fad0eeac3377b095025dc294732db030e8cc5b81655b782` |
| `D:\workspace\信息收集整理\work\珠三角三甲医院_医生画像自动采集总底表_payload.json` | 24074769 | `bed5ba6d1b24aacc853f3471879d99abc88d52d57a8b63dc024bb9438a793bd9` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv` | 17722159 | `8a20ae4f0c2e79ff034a73bc84cea3d004f6a4e578aa2219c057060a7e0e6508` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx` | 4839414 | `96802c97c8b010e29bcfc32bc3e33300426ab1fdd0e685a643ef5daadcf11c7e` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 5590 | `cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a` |

- 本院画像 Markdown 树：414 个文件，SHA-256 `aa29b1260d6a0a88ebb3940516f158625e31db88378fe612138a00932d2dc14f`。
- 本院正式照片目录执行前后状态一致：`{"exists": false, "file_count": 0, "bytes": 0, "sha256": ""}`。
- TRIAL 只写入 `work` 独立工件，未写总底表、正式照片目录、画像或索引。

## 裁决依据缺口

Issue 正文引用的 `docs/中山五院照片嵌入方式裁决单.md` 在本次基线不存在。Issue 正文已完整给出方案 A，但 TRIAL 不执行画像写入，因此不影响本阶段；进入 FULL 前仍应由 owner 确保该裁决依据可追溯。

## 当前停止点

TRIAL 工件完成后停止，等待 owner 审计实图、大小分布、来源边界及缺失裁决单风险。未取得当前关联 PR 中 owner 明确 `通过` / `有条件通过` 且切换为 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填总底表、写正式照片目录或修改画像。
