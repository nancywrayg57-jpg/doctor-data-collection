# Issue #81 南方医科大学口腔医院(海珠广场院区)照片补录 TRIAL 报告

> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 生成日期：2026-08-19
> 视觉复核：`PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`

## 范围与抽样

- 固定范围：95 行、95 个唯一详情 URL；照片双列全空。
- 9 个 section 分布：{"341": 12, "342": 12, "343": 10, "384": 12, "385": 12, "386": 12, "431": 7, "434": 11, "504": 7}。
- TRIAL：10 位，覆盖全部 9 个 section；职称分层 正高 2、副高 2、中级 3、初级 3，覆盖正高/副高/中级/初级四层。
- 详情 HTTP 200：10/10；实图 10/10；失败/结构异常 0。
- 固定浏览器 UA urllib：Cookie 0、代理 0、挑战绕过 0、页面未引用路径探测 0、第三方来源 0。

## UA 可达性复测

| 轮次 | 目标 | HTTP | Content-Type | 字节 | UTC |
|---:|---|---:|---|---:|---|
| 1 | homepage_non_gate | 200 | text/html | 154301 | 2026-08-19T08:24:16Z |
| 1 | sample_detail_gate | 200 | text/html | 48297 | 2026-08-19T08:24:16Z |
| 2 | homepage_non_gate | 200 | text/html | 154301 | 2026-08-19T08:24:46Z |
| 2 | sample_detail_gate | 200 | text/html | 48297 | 2026-08-19T08:24:47Z |

## 容器结构诊断

- 唯一允许容器：`img.content_img` 的 `src`。
- `/Home/images/`、`/Public/Home/images/` 与其他所有页面图片均排除。

### 管东华 / section 341 / ID 36

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload/2024-07-19/6699c33ac6fdc.png">
```

- 页面引用：`/Uploads/Upload/2024-07-19/6699c33ac6fdc.png`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload/2024-07-19/6699c33ac6fdc.png
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded

### 孟文霞 / section 386 / ID 135

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload/product0686234001434443704.jpg">
```

- 页面引用：`/Uploads/Upload/product0686234001434443704.jpg`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload/product0686234001434443704.jpg
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded

### 张彩美 / section 434 / ID 157

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload/2018-07-09/5b4317fa3c9a2.JPG">
```

- 页面引用：`/Uploads/Upload/2018-07-09/5b4317fa3c9a2.JPG`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload/2018-07-09/5b4317fa3c9a2.JPG
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded

### 陈欢 / section 342 / ID 373

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload//2026-04-09/177572048531460.jpg">
```

- 页面引用：`/Uploads/Upload//2026-04-09/177572048531460.jpg`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload//2026-04-09/177572048531460.jpg
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded

### 梁慧珉 / section 341 / ID 523

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload//2025-09-12/175764026032115.png">
```

- 页面引用：`/Uploads/Upload//2025-09-12/175764026032115.png`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload//2025-09-12/175764026032115.png
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded

### 唐凤翔 / section 504 / ID 532

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload/2021-11-02/6180c7563e11c.jpg">
```

- 页面引用：`/Uploads/Upload/2021-11-02/6180c7563e11c.jpg`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload/2021-11-02/6180c7563e11c.jpg
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded

### 何龙文 / section 343 / ID 555

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload/2022-08-18/62fdb8797c6aa.jpg">
```

- 页面引用：`/Uploads/Upload/2022-08-18/62fdb8797c6aa.jpg`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload/2022-08-18/62fdb8797c6aa.jpg
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded

### 叶晓平 / section 384 / ID 632

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload//2025-01-03/173587601925582.jpg">
```

- 页面引用：`/Uploads/Upload//2025-01-03/173587601925582.jpg`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload//2025-01-03/173587601925582.jpg
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded

### 熊华翠 / section 385 / ID 641

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload//2025-04-22/174531719793431.jpg">
```

- 页面引用：`/Uploads/Upload//2025-04-22/174531719793431.jpg`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload//2025-04-22/174531719793431.jpg
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded

### 曹恒隆 / section 431 / ID 690

```html
<img width="118" height="147" class="content_img" src="/Uploads/Upload//2025-11-28/176432358774135.jpg">
```

- 页面引用：`/Uploads/Upload//2025-11-28/176432358774135.jpg`
- 规范化 URL：https://www.smukqyy.cn/Uploads/Upload//2025-11-28/176432358774135.jpg
- 判定：only the unique img.content_img src is eligible; /Home/images/, /Public/Home/images/ and all other page images are excluded


## TRIAL 原始字节

- 10 张共 5192350 bytes；平均 519235 bytes。
- >5 MiB：0；>20 MiB：0。
- 仅保存页面实际引用响应原始字节；未压缩、未转码；扩展名随实际魔数。

| 姓名 | section | 科室 | 层级 | 字节 | 尺寸 | 声明/实际 | SHA-256 | 页面引用照片 |
|---|---:|---|---|---:|---:|---|---|---|
| 管东华 | 341 | 口腔种植修复科 | 正高 | 88568 | 257×312 | png/png | `4c068d8acb174336f9c832b922f9586b7f47efc4e9cef626a4947f61a89bc390` | https://www.smukqyy.cn/Uploads/Upload/2024-07-19/6699c33ac6fdc.png |
| 陈欢 | 342 | 牙体牙髓病科一室 | 副高 | 444539 | 960×1390 | jpg/png | `59b1eb5935128c8f66a9b49c829fd0262c33cf915f60ae6091ebaa0ac152d0ae` | https://www.smukqyy.cn/Uploads/Upload//2026-04-09/177572048531460.jpg |
| 何龙文 | 343 | 口腔正畸科 | 中级 | 1028744 | 1191×1730 | jpg/jpg | `92269f9be96873fec245b1e925edc08ad0aea7376e93a597fd844d68d624ebc9` | https://www.smukqyy.cn/Uploads/Upload/2022-08-18/62fdb8797c6aa.jpg |
| 叶晓平 | 384 | 口腔颌面外科 | 初级 | 602552 | 2192×2644 | jpg/jpg | `74b45d3480c36d28d9d122002cffd2536207f6dfe825517c9a7ed17b26c8ae83` | https://www.smukqyy.cn/Uploads/Upload//2025-01-03/173587601925582.jpg |
| 熊华翠 | 385 | 儿童口腔科 | 副高 | 522338 | 780×1134 | jpg/jpg | `7f94dbd0146c84f81d72f722650c7d7c5eb37f8897dd56410712a60ca7a89e8a` | https://www.smukqyy.cn/Uploads/Upload//2025-04-22/174531719793431.jpg |
| 孟文霞 | 386 | 牙周黏膜病科 | 正高 | 71298 | 500×750 | jpg/jpg | `7abc21086c1fcd473b3c07ca5804d1472a83856334d724fb502677cfc9dd9508` | https://www.smukqyy.cn/Uploads/Upload/product0686234001434443704.jpg |
| 曹恒隆 | 431 | 口腔预防科 | 初级 | 73918 | 1280×1392 | jpg/jpg | `dff448f56df96ad0cbcae42884f0d9488cf83db85399f4b10029bb2bfe05c075` | https://www.smukqyy.cn/Uploads/Upload//2025-11-28/176432358774135.jpg |
| 张彩美 | 434 | 牙体牙髓病科二室 | 中级 | 114582 | 300×450 | unknown/jpg | `d702ae5049a79f0372e864d1dae9d0a13c68ec9f64c36769a378f0491666ae8c` | https://www.smukqyy.cn/Uploads/Upload/2018-07-09/5b4317fa3c9a2.JPG |
| 唐凤翔 | 504 | 舒适化治疗中心 | 中级 | 331927 | 591×880 | jpg/jpg | `ef2884e2155aad7d66c26380049d8e03e47b95d539c3bce68033d9e67c824e42` | https://www.smukqyy.cn/Uploads/Upload/2021-11-02/6180c7563e11c.jpg |
| 梁慧珉 | 341 | 口腔种植修复科 | 初级 | 1913884 | 1446×1994 | png/png | `3198b5a5da9b5734a74cfdb9879b77faee21188b9a9b1e4b1254c90417735261` | https://www.smukqyy.cn/Uploads/Upload//2025-09-12/175764026032115.png |

详细清单见 `work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_manifest.csv` 与 `work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_payload.json`。

## 工程与占位门禁

1. ROOT 由 `Path(__file__).resolve().parents[1]` 定位；payload/manifest/report 只记录仓库相对路径。
2. 发布时引用工件 SHA-256 必须按仓库 blob（LF）计算。
3. query Base64 占位标记、全图唯一颜色数不大于 2、跨医生同 SHA、灰底拼图空白/不可见格均拦截。
4. 联系表：`work/南方医科大学口腔医院(海珠广场院区)_photo_backfill_trial_contact_sheet.jpg`；当前状态 `PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`。

## 正式资产零修改

| 文件 | 字节 | SHA-256 |
|---|---:|---|
| `work/珠三角三甲医院_医生画像自动采集总底表_payload.json` | 24975646 | `a71842fa134023d566df7bf8aa977f6ff8412d9c3b57d8ebbb75057d68bb46b0` |
| `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.csv` | 18622756 | `7ee9c59ac8f9d2e42dd1ed7508f4f181f9371e2e413767b62d1b8280df4289ff` |
| `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表.xlsx` | 5105950 | `cf9a6c20df19da719f205837daccf923cd36859cf8e84f8b434f887b2a200fa3` |
| `医生画像仓库/99_资料来源/珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 5590 | `cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a` |

- 本院画像树：96 个文件，聚合 SHA-256 `5958ced55c4e0cb36c0bc7e161666324578fc6f4cfae66e5677b9ce8356755b2`。
- 正式照片树前后一致：`{"exists": false, "file_count": 0, "bytes": 0, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}`。
- TRIAL 仅写 `work/` 工件，未回填总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件提交并发布 `TRIAL_READY_FOR_OWNER_AUDIT` 后停止。未取得 PR #82（创建后）的明确 `FULL_APPEND_AND_OBSIDIAN` 指令前，不得回填正式资产。
