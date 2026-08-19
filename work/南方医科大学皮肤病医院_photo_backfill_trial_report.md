# Issue #83 南方医科大学皮肤病医院 照片补录 TRIAL 报告

## 授权与范围

- GitHub Issue：<https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/83>
- Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
- 医院官网：<https://www.gdskin.com/>
- 代表医生目录：<https://www.gdskin.com/Showclass.aspx?id=906>
- 固定范围：77 行；来源链接唯一 77 条；照片双列在 TRIAL 前均为空。
- 历史科室字段为空，按 Issue 要求改以分类入口分层；本样本覆盖 9/9 个入口：901, 902, 906, 910, 913, 915, 917, 921, 922。
- 职称层级：{"正高": 4, "副高": 2, "中级": 3, "初级": 1}。

## 串行访问与结构诊断

- 固定浏览器 UA；无 Cookie、无代理、无并发；请求间隔下限 2.0 秒。
- 本轮共 17 次官网网络请求，实测最小相邻启动间隔 2.000000 秒。
- 既有成功照片复用 9 张，不重新下载；本轮仅新下载 1 张替换照片。
- 页面唯一 `/uploadimg/` 正文 `img src` 才可进入候选；WebResource、备案图标及 logo/banner/nav/foot 全部排除。
- 页面引用照片原始字节直接保存，不压缩、不转码、不构造未引用路径。

| 分类入口 | 姓名 | 详情 ID | 正文 img HTML | 判定依据 |
|---|---|---:|---|---|
| 901 | 顾有守 | 3829 | `<img alt="" src="../uploadimg/广东省皮肤病医院顾有守.jpg" width="300" height="325">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |
| 902 | 杨斌 | 3847 | `<img style="border: 0px currentColor;" alt="" src="../system_dntb/../uploadimg/杨斌2021.jpg" width="400" height="600" align="">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |
| 906 | 谷梅 | 3849 | `<img src="../system_dntb/../uploadimg/谷梅2021.jpg" align="" width="400" height="600" alt="">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |
| 921 | 何仁亮 | 3854 | `<img alt="" src="../uploadimg/何仁亮.jpg" width="400" height="525">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |
| 913 | 鲜华 | 4287 | `<img width="400" height="525" alt="" src="../uploadimg/鲜华.jpg">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |
| 906 | 吉苏云 | 4846 | `<img alt="" src="../uploadimg/吉苏云.jpg" width="300" height="394">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |
| 922 | 钟泽敏 | 5576 | `<img width="400" align="" alt="" src="../system_dntb/../uploadimg/钟泽敏.jpg">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |
| 910 | 王柳苑 | 5580 | `<img width="400" ="" align="" alt="" src="../system_dntb/../uploadimg/王柳苑 .jpg">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |
| 915 | 杜美毅 | 5596 | `<img src="../system_dntb/../uploadimg/杜美毅.jpg" align="" width="200" height="200" alt="">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |
| 917 | 严婷婷 | 5599 | `<img src="../system_dntb/../uploadimg/严婷婷 .jpg" align="" width="400" ="" alt="">` | only the unique page-referenced img src resolving under /uploadimg/ is eligible; WebResource, filing icon and all site decorations are excluded |

## 已知占位判例

- 文海泉详情：<https://www.gdskin.com/ShowNews.ASPX?ID=5566>，页面实际引用：<https://www.gdskin.com/uploadimg/占位.png>。
- 文件名明文门禁：`explicit_chinese_placeholder_filename`；HTTP 200，4959 bytes，200×200。
- SHA-256：`d2565a802cdc8d7ca29f218cd60685542d139a7de68ffc9ee559011e2f693aac`，与 Owner 指定 known-SHA 一致：`True`。
- 该字节仅用于门禁取证，未写入磁盘、未计入 10 位实采样本。

## Owner 裁决后的替换对照

| 原样本 | 替换人 | 入口 | 职称层变化 | 替换理由 |
|---|---|---:|---|---|
| 吴芳芳 | 谷梅 | 906 | 初级→正高 | 入口906/初级唯一替代人于碧慧同样无照片容器；Owner裁决入口覆盖优先并允许入口内跨层，取最高可用层 |
| 孟凡琪 | 杜美毅 | 915 | 初级→初级 | 原样本及龚洋洋/郭先荟候选的NBSP尾缀页面引用均悬空；按Owner指定改用同入口同层且资源200的杜美毅 |
| 杨超 | 钟泽敏 | 922 | 中级→中级 | 原页面无照片容器；按Owner裁决同入口同层替换 |

最终 10 人分层按 Owner 裁决以实际构成为准：{"正高": 4, "副高": 2, "中级": 3, "初级": 1}；入口覆盖保持 9/9。

## 原样本失败证据行

| 姓名 | 入口 | 详情ID | 失败类 | 页面引用数 | 页面原引用 | 编码传输URL | 照片HTTP | 判定特征 | UTC |
|---|---:|---:|---|---:|---|---|---:|---|---|
| 吴芳芳 | 906 | 6197 | 无照片容器 |  | `-` | `-` | - | 全页无 /uploadimg/ 引用；仅 WebResource 与备案装饰图 | 2026-08-19T11:24:41Z |
| 孟凡琪 | 915 | 5593 | 照片资源不可达 | 1 | `../system_dntb/../uploadimg/孟凡琪 .jpg` | `https://www.gdskin.com/uploadimg/%E5%AD%9F%E5%87%A1%E7%90%AA%C2%A0%20%C2%A0.jpg` | 404 | 页面原引用含 NBSP+空格尾缀；浏览器语义编码后仍为404，禁止构造变体 | 2026-08-19T11:24:41Z |
| 杨超 | 922 | 6200 | 无照片容器 |  | `-` | `-` | - | 全页无 /uploadimg/ 引用；仅 WebResource 与备案装饰图 | 2026-08-19T11:24:41Z |

孟凡琪证据同时保留含 NBSP 的页面原引用与标准百分号编码 URL；未构造、未探测任何路径变体。

### 替代候选失败留档（供 FULL）

| 姓名 | 入口 | 详情ID | 失败类 | 页面引用数 | 页面原引用 | 编码传输URL | 照片HTTP | 判定特征 | UTC |
|---|---:|---:|---|---:|---|---|---:|---|---|
| 于碧慧 | 906 | 6196 | 无照片容器 |  | `-` | `-` | - | 入口906/初级唯一替代候选同样无 /uploadimg/ 引用 | 2026-08-19T12:07:00Z |
| 龚洋洋 | 915 | 5594 | 照片资源不可达 | 1 | `../system_dntb/../uploadimg/龚洋洋 .jpg` | `https://www.gdskin.com/uploadimg/%E9%BE%9A%E6%B4%8B%E6%B4%8B%C2%A0.jpg` | 404 | 页面原引用含NBSP尾缀；仅作浏览器语义百分号编码后仍为404，禁止构造变体 | 2026-08-19T12:20:58Z |
| 郭先荟 | 915 | 5595 | 照片资源不可达 | 1 | `../system_dntb/../uploadimg/郭先荟 .jpg` | `https://www.gdskin.com/uploadimg/%E9%83%AD%E5%85%88%E8%8D%9F%C2%A0.jpg` | 404 | 页面属性以&nbsp;表达NBSP尾缀；按浏览器语义解析并编码后仍为404，禁止构造变体 | 2026-08-19T12:27:35Z |

龚洋洋、郭先荟证据均保留 NBSP 页面引用与仅用于传输的百分号编码 URL；与孟凡琪共同构成本站 NBSP 尾缀悬空判例。于碧慧保留无照片容器证据。

## 10 位实采结果

- 10/10 详情 HTTP 200，10/10 照片 HTTP 200，失败与结构异常共 0。
- 总字节 7158350，平均 715835；预计全院 77 行约 52.57 MiB。
- >5 MiB：0；>20 MiB：0；跨医生重复 SHA：0。
- 联系表：`work/南方医科大学皮肤病医院_photo_backfill_trial_contact_sheet.jpg`；当前视觉状态：`PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`。

| 入口 | 姓名 | 层级 | 详情页 | 页面引用照片 | 声明类型 | 实际格式 | 尺寸 | 字节 | 来源 | SHA-256 |
|---|---|---|---|---|---|---|---:|---:|---|---|
| 901 | 顾有守 | 正高 | https://www.gdskin.com/ShowNews.ASPX?ID=3829 | https://www.gdskin.com/uploadimg/广东省皮肤病医院顾有守.jpg | image/jpeg | jpg | 156×185 | 24320 | 复用 | 28ab8844986935af70cc86ae2749994561576c643eaaee7a3f4805e9edf57668 |
| 902 | 杨斌 | 正高 | https://www.gdskin.com/ShowNews.ASPX?ID=3847 | https://www.gdskin.com/uploadimg/杨斌2021.jpg | image/jpeg | jpg | 800×1200 | 731906 | 复用 | 87216049d9ba63d03595964aa3ad347ac1b77ac9aad9276539fcb1e45a311461 |
| 906 | 吉苏云 | 副高 | https://www.gdskin.com/ShowNews.ASPX?ID=4846 | https://www.gdskin.com/uploadimg/吉苏云.jpg | image/jpeg | jpg | 800×1200 | 526479 | 复用 | e2b74bec18c43d923b984881dc7a8dd3772a2066f7754c3d93717002d481c1ca |
| 906 | 谷梅 | 正高 | https://www.gdskin.com/ShowNews.ASPX?ID=3849 | https://www.gdskin.com/uploadimg/谷梅2021.jpg | image/jpeg | jpg | 1879×2819 | 2489392 | 复用 | fea29092ec4c1ab235917837b8ad991476998722cee1a8c95f1cf78baf403d8f |
| 910 | 王柳苑 | 中级 | https://www.gdskin.com/ShowNews.ASPX?ID=5580 | https://www.gdskin.com/uploadimg/王柳苑.jpg | image/jpeg | jpg | 800×1200 | 680685 | 复用 | c6b1de349d140ef6b97960a1342d49cc9570c961d3f869543d3a1f18abfd5213 |
| 913 | 鲜华 | 副高 | https://www.gdskin.com/ShowNews.ASPX?ID=4287 | https://www.gdskin.com/uploadimg/鲜华.jpg | image/jpeg | jpg | 800×1200 | 533486 | 复用 | f8471531bcb0c7abd68acdb5e7acee79a58e17a6770e1be9bc682362147e7e16 |
| 915 | 杜美毅 | 初级 | https://www.gdskin.com/ShowNews.ASPX?ID=5596 | https://www.gdskin.com/uploadimg/杜美毅.jpg | image/jpeg | jpg | 800×1112 | 602980 | 新下载 | 1e5ca9ee46183ff98dd29495e8b33b3e1b802c022d6f11ef2aff0be0f5c19d9e |
| 917 | 严婷婷 | 中级 | https://www.gdskin.com/ShowNews.ASPX?ID=5599 | https://www.gdskin.com/uploadimg/严婷婷.jpg | image/jpeg | jpg | 800×1200 | 522389 | 复用 | 8e82ed6a0f9d49c7272e1bc79823a1e0a724c746e6a971fcbaf045ef485a6f82 |
| 921 | 何仁亮 | 正高 | https://www.gdskin.com/ShowNews.ASPX?ID=3854 | https://www.gdskin.com/uploadimg/何仁亮.jpg | image/jpeg | jpg | 800×1200 | 524595 | 复用 | 4f02999f07f998ee915708597dee3fbf98152c88e585fe48bbb72be77e0301fd |
| 922 | 钟泽敏 | 中级 | https://www.gdskin.com/ShowNews.ASPX?ID=5576 | https://www.gdskin.com/uploadimg/钟泽敏.jpg | image/jpeg | jpg | 800×1200 | 522118 | 复用 | 1a7c3faba1025d1d92005d187e32cd7aa2a8ef34a1c535dc8df00665dc9754a0 |

## 工程与保护门禁

1. ROOT 由 `Path(__file__).resolve().parents[1]` 定位；payload/manifest/report 只记录仓库相对路径。
2. 引用工件哈希按仓库 blob（文本 CRLF→LF，二进制原字节）口径计算。
3. 中文“占位”文件名、known-SHA、query Base64、近单色、跨医生同 SHA、灰底拼图空白/不可见格均拦截。

| 受保护文件 | 字节 | SHA-256 |
|---|---:|---|
| `work/珠三角三甲医院_医生画像自动采集总底表_payload.json` | 24998174 | `66ea238b9ef3327117129028dc8581668081ac16190b1f6e4e8cc3569129d5aa` |
| `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.csv` | 18645284 | `69d7a2a2393057b34d26630fff042f5ac3274adef8ca35fba8286c28d6934871` |
| `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.xlsx` | 5110845 | `f02226df0425b241da5b86aa7ca104997e7eb8e22ea96ced31a23a2232d66810` |
| `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 5590 | `cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a` |

- 本院画像树：78 个文件，聚合 SHA-256 `64dd7f0edf76d9c6c6c95711b5c54b59a419d782f7478605f5c408ac1af29653`。
- 正式照片树前后一致：`{"exists": false, "file_count": 0, "bytes": 0, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}`。
- TRIAL 仅写 `work/` 工件，未回填总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件提交、推送并发布 `TRIAL_READY_FOR_OWNER_AUDIT` 后停止。未取得 Owner 在关联 PR 明确下发的 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填正式资产。
