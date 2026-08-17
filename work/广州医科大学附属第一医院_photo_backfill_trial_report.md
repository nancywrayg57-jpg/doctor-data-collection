# Issue #63 广州医科大学附属第一医院照片补录 TRIAL 报告

## 执行结论

- 阶段：`TRIAL_READY_FOR_OWNER_AUDIT`；范围：616 行 / 616 个唯一官网详情 URL。
- 固定分层样本：10 人，覆盖 8 个科室，职称层级 `{"正高": 3, "副高": 3, "其他": 4}`。
- 实采：10；熔断问题：0/10（0.00%）。
- 两种页面引用路径：`{"Upload原图": 4, "doctor原图": 6}`；仅取详情页唯一 `div.photo img`，正文叙事图和 floatcard 等非候选区域未进入解析范围。
- 图片请求携带对应详情页 Referer；未构造或探测页面未引用路径；未使用第三方来源，未绕过登录、验证码、反爬或权限限制。

## 大小分布

| 指标 | 结果 |
|---|---:|
| 总字节 | 1949147 |
| 最小 | 3547 |
| 中位数 | 40699 |
| 平均 | 194914 |
| 最大 | 1031569 |
| 超过 200 KiB | 2 |
| 超过 5 MiB | 0 |
| 616 行估算 | 114.50 MiB |

分桶：`{"<200KiB": 8, "200KiB-1MiB": 2}`。

## 逐图三重核验与尺寸

| 姓名 | 科室 | 层级 | 主职称 | 路径风格 | 文件名 | 字节 | 尺寸 | SHA-256 | 页面引用照片 |
|---|---|---|---|---|---|---:|---:|---|---|
| 钟南山 | 呼吸与危重症医学科 | 正高 | 教授 | Upload原图 | 钟南山-呼吸与危重症医学科-教授-广州医科大学附属第一医院.jpg | 72435 | 325×400 | b28a3690894c9010557a38b0d022fbc7ca6c0873274dd760bb34b8764dfc2eaa | https://www.gyfyyy.cn/Upload/202112/637750146771733237.jpg |
| 黄铮 | 心血管内科 | 正高 | 主任医师 | doctor原图 | 黄铮-心血管内科-主任医师-广州医科大学附属第一医院.jpg | 37477 | 325×400 | a32a9814527d458c7d1551b9543d6f7957d1559795b71130a2355eed30571286 | https://www.gyfyyy.cn/images/doctor/HUANGZHENG.jpg |
| 赖克方 | 呼吸与危重症医学科 | 正高 | 教授 | doctor原图 | 赖克方-呼吸与危重症医学科-教授-广州医科大学附属第一医院.jpg | 40650 | 325×400 | a650b59bcbf78120b8ac50ac3f0a95dc504229678dfb22159721802f32f022e0 | https://www.gyfyyy.cn/images/doctor/LAIKEFANG.jpg |
| 欧阳铭 | 呼吸与危重症医学科 | 副高 | 副主任医师 | Upload原图 | 欧阳铭-呼吸与危重症医学科-副主任医师-广州医科大学附属第一医院.jpg | 1031569 | 325×400 | 24ddd364315b37328df698eb61b1608eee8509e4bc6c433bdba2386d4e171224 | https://www.gyfyyy.cn/Upload/202410/638658855425722392.jpg |
| 梁增伟 | 感染内科 | 副高 | 副主任医师 | Upload原图 | 梁增伟-感染内科-副主任医师-广州医科大学附属第一医院.jpg | 3547 | 100×145 | 99e69f0cb71236659d67a0b0bf2dd90d88feadb31cab90a5394d80b63a95adde | https://www.gyfyyy.cn/Upload/202411/638664968880753569.jpg |
| 韦兵 | 胸外科 | 副高 | 副主任医师 | doctor原图 | 韦兵-胸外科-副主任医师-广州医科大学附属第一医院.jpg | 39079 | 325×400 | b4602253cccc3784e20cf071e6128698a950c353907afeca4f70721f3e7923a9 | https://www.gyfyyy.cn/images/doctor/WEIBING.jpg |
| 何颖 | 针灸专业组 | 其他 | 主治医师 | doctor原图 | 何颖-针灸专业组-主治医师-广州医科大学附属第一医院.jpg | 81318 | 325×400 | 20f5dbe8ce6ff9c1ee2b567c3c0ae193a17f351e07e840c1f11dd4ee0f54fad4 | https://www.gyfyyy.cn/images/doctor/HEYIN.jpg |
| 黄泳璋 | 肾内科 | 其他 | 主治医师 | doctor原图 | 黄泳璋-肾内科-主治医师-广州医科大学附属第一医院.jpg | 40749 | 325×400 | 6823d1d084f986d34abc228a8493ad896ab42d87634e4b6fc8fa737c3d31a333 | https://www.gyfyyy.cn/images/doctor/HUANGYONGZHANG.jpg |
| 林婷婷 | 营养科 | 其他 | 主治医师 | doctor原图 | 林婷婷-营养科-主治医师-广州医科大学附属第一医院.jpg | 39484 | 325×400 | b66256c269193a8552a2c0306ba59030862ea9a40cf2565a76f1c8297a8cf495 | https://www.gyfyyy.cn/images/doctor/LINTINGTING.jpg |
| 孟冬梅 | 药学部 | 其他 | 主管药师 | Upload原图 | 孟冬梅-药学部-主管药师-广州医科大学附属第一医院.jpg | 562839 | 682×1024 | 88eb32848f8b9f84fd40b03819fcdb57fed6bf202780737c6e5beb96cc85fcfe | https://www.gyfyyy.cn/Upload/202411/638672803796004099.jpg |

详细 HTTP、引用属性、魔数和命名清单见：`D:\workspace\信息收集整理\work\广州医科大学附属第一医院_photo_backfill_trial_manifest.csv` 与 `D:\workspace\信息收集整理\work\广州医科大学附属第一医院_photo_backfill_trial_payload.json`。

## 占位图检测

- 仅小于 40 KiB 的 GIF 在命中 `nopic/noimage/placeholder` 路径标记或低色板且浅灰中性像素占比至少 70% 时判占位；不得单凭 GIF 格式判占位。
- 大尺寸人像 GIF 不进入小 GIF 占位启发式；样本 SHA-256 重复时门禁失败，防止站点通用图混入。

## 联系表人工核验

- 联系表：`D:\workspace\信息收集整理\work\广州医科大学附属第一医院_photo_backfill_trial_contact_sheet.jpg`。
- 当前状态：`PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。
- 判定目标：10 张均为对应医生的单人成人职业照，不得出现正文叙事图、患者、儿童、合影、占位图、二维码或公共装饰图。

## 受保护正式资产零变更

| 文件 | 字节 | SHA-256 |
|---|---:|---|
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院官网入口台账.xlsx` | 40025 | `d6b08b3f284654024fad0eeac3377b095025dc294732db030e8cc5b81655b782` |
| `D:\workspace\信息收集整理\work\珠三角三甲医院_医生画像自动采集总底表_payload.json` | 24173400 | `43e1a5ae729145c35dae0640077bfb5a6528434bfd4e9ceeb83926e417fa087c` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv` | 17820790 | `e41bc67b25c7ce5daba537d2b07eebc251ed3b33b1b33d5056f19fa47eb2b394` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx` | 4858499 | `f294857a29874048a780675b7dbc67a0ae705da459e618da42c0feecf7fb389e` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 5590 | `cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a` |

- 本院画像 Markdown 树：617 个文件，SHA-256 `0cdf9e07bbab31b019dbe7f127ab0ea5e5a1f1c434d3fa50c550d7066bd8fcef`。
- 本院正式照片目录执行前后状态一致：`{"exists": false, "file_count": 0, "bytes": 0, "sha256": ""}`。
- TRIAL 只写入 `work` 独立工件，未写入口台账、总底表三载体、正式照片目录、616 份画像或索引。

## 附带条款停止点

- Issue #63 要求在同一 PR 标记台账序号 15 南部战区空军医院为管理员裁决跳过；该条款已记录，但为满足本阶段“正式资产 TRIAL 零修改”，将在 Owner 通过并切换 FULL 后与正式事务一并执行。

## 当前停止点

TRIAL 工件完成后停止，等待 owner 审计实图、大小分布与来源边界。未取得当前关联 PR 中 owner 明确 `通过` / `有条件通过` 且切换为 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填总底表、写正式照片目录、修改画像或入口台账。
