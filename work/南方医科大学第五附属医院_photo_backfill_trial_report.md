# Issue #79 南方医科大学第五附属医院照片补录 TRIAL 报告

> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 生成日期：2026-08-19
> 视觉复核：`PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`

## 范围与抽样

- 固定范围：134 行、134 个唯一详情 URL；照片双列全空。
- 采集入口：主入口 133 行，岭南名医入口 1 行；两者均为 Issue #79 明示官网入口。
- TRIAL：10 位、覆盖 8 个科室；职称分层 正高 3、副高 4、中级 3、初级 0。全院无初级记录，已覆盖全部可用层级。
- 详情 HTTP 200：10/10；实图 10/10；失败/结构异常 0。
- Owner 批准的固定浏览器 UA urllib：Cookie 0、代理 0、挑战绕过 0、页面未引用路径探测 0、第三方来源 0。
- 首页仅留痕、不是采集门禁；固定详情页及其唯一容器照片资源才是门禁。

## FATAL 解除后的 UA 可达性复测

- 两轮间隔：30 秒。
- User-Agent：`Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36`。

| 轮次 | 目标 | HTTP | Content-Type | 字节 | UTC |
|---:|---|---:|---|---:|---|
| 1 | homepage_non_gate | 200 | text/html | 213826 | 2026-08-19T03:15:12Z |
| 1 | sample_detail_gate | 200 | text/html | 15810 | 2026-08-19T03:15:13Z |
| 2 | homepage_non_gate | 200 | text/html | 213826 | 2026-08-19T03:15:44Z |
| 2 | sample_detail_gate | 200 | text/html | 15810 | 2026-08-19T03:15:44Z |

## 容器结构诊断

- 唯一允许容器：`div.yisheng_xq_bug_left` 的内联 `background-image`。
- 页面其他 `background-image`、正文 ueditor 叙事配图、logo、悬浮按钮、二维码和政府徽标全部排除。
- 排除样例：images/logo.jpg; images/gzwm.jpg; images/float1.png ... images/float5.png; dcs.conac.cn government badge; 正文 ueditor 叙事配图（非 yisheng_xq_bug_left 容器）。

### 沈玉才 / ID 40

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20221012/1665568725899149.png)">
```

- 页面引用：`/ueditor/php/upload/image/20221012/1665568725899149.png`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20221012/1665568725899149.png
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded

### 郭丽冬 / ID 261

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20221013/1665644960466120.png)">
```

- 页面引用：`/ueditor/php/upload/image/20221013/1665644960466120.png`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20221013/1665644960466120.png
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded

### 黄艺洪 / ID 282

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20221014/1665708290560747.png)">
```

- 页面引用：`/ueditor/php/upload/image/20221014/1665708290560747.png`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20221014/1665708290560747.png
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded

### 安得辉 / ID 320

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20240709/1720515914781586.png)">
```

- 页面引用：`/ueditor/php/upload/image/20240709/1720515914781586.png`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20240709/1720515914781586.png
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded

### 王波涛 / ID 332

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20250807/1754529229745740.jpg)">
```

- 页面引用：`/ueditor/php/upload/image/20250807/1754529229745740.jpg`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20250807/1754529229745740.jpg
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded

### 许桂璇 / ID 418

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20221014/1665718037585576.png)">
```

- 页面引用：`/ueditor/php/upload/image/20221014/1665718037585576.png`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20221014/1665718037585576.png
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded

### 吴智勇 / ID 419

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20221013/1665630004218214.png)">
```

- 页面引用：`/ueditor/php/upload/image/20221013/1665630004218214.png`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20221013/1665630004218214.png
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded

### 司昌荣 / ID 534

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20240708/1720438871119662.png)">
```

- 页面引用：`/ueditor/php/upload/image/20240708/1720438871119662.png`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20240708/1720438871119662.png
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded

### 杨柳 / ID 558

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20260507/1778115130809040.jpg)">
```

- 页面引用：`/ueditor/php/upload/image/20260507/1778115130809040.jpg`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20260507/1778115130809040.jpg
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded

### 周姗 / ID 565

```html
<div class="yisheng_xq_bug_left" style="background-image: url(/ueditor/php/upload/image/20260528/1779932414137710.png)">
```

- 页面引用：`/ueditor/php/upload/image/20260528/1779932414137710.png`
- 规范化 URL：http://www.ny5y.cn/ueditor/php/upload/image/20260528/1779932414137710.png
- 判定：only the unique yisheng_xq_bug_left inline background-image is eligible; all other page and narrative images are excluded


## TRIAL 原始字节

- 10 张共 5392900 bytes；平均 539290 bytes。
- >5 MiB：0；>20 MiB：0。
- 仅保存页面容器实际引用响应原始字节；未压缩、未转码；扩展名随实际魔数。

| 姓名 | 科室 | 层级 | 主职称 | 字节 | 尺寸 | 声明/实际 | SHA-256 | 页面引用照片 |
|---|---|---|---|---:|---:|---|---|---|
| 黄艺洪 | 未标注 | 正高 | 主任医师 | 189404 | 413×582 | png/png | `09dd5d58449660d19854fbef225a600bacc8af2e267aeddd5f299286e67dfd32` | http://www.ny5y.cn/ueditor/php/upload/image/20221014/1665708290560747.png |
| 司昌荣 | 中医科 | 正高 | 主任中医师 | 737680 | 738×1024 | png/png | `c6b46767b70b9b260b8535af5194a360667f55fc7421fa86f3c91ed3739ce52f` | http://www.ny5y.cn/ueditor/php/upload/image/20240708/1720438871119662.png |
| 安得辉 | 中医科 | 中级 | 主治中医师 | 2282621 | 935×1361 | png/png | `cdd64d7abea4f6008d7812249a02f1922b5ede8aed37b8329372201984f1a1b9` | http://www.ny5y.cn/ueditor/php/upload/image/20240709/1720515914781586.png |
| 周姗 | 中心实验室 | 副高 | 副研究员 | 1252401 | 2666×4000 | png/png | `209fe11bad6f7cc26b6e657618e001d523c2750d3e9594cf100d03c69416625f` | http://www.ny5y.cn/ueditor/php/upload/image/20260528/1779932414137710.png |
| 郭丽冬 | 临床营养科 | 副高 | 副主任医师 | 131036 | 413×579 | png/png | `15f99ae5b4fab5a3feaf2c948d029cfcce78523cd2626984b7b289c036ae83d8` | http://www.ny5y.cn/ueditor/php/upload/image/20221013/1665644960466120.png |
| 王波涛 | 介入血管外科 | 副高 | 副主任技师 | 132784 | 900×1350 | jpg/jpg | `8e3b35e6ea5879bbf95e2cb3131377c2217d89cda55bc9a10746eff9c4c4f3fe` | http://www.ny5y.cn/ueditor/php/upload/image/20250807/1754529229745740.jpg |
| 沈玉才 | 儿童重症医学科 | 正高 | 主任医师 | 206664 | 413×579 | png/png | `55ac91f09b246a6b6d7125e6ce22f8d792d58990728b8bb4d7f2ecec95c79817` | http://www.ny5y.cn/ueditor/php/upload/image/20221012/1665568725899149.png |
| 吴智勇 | 精神心理科 | 中级 | 主治医师 | 155326 | 413×579 | png/png | `5713431ca164465c8bb369aa0c9ef4d74d4f669ad58f0050380e134dd70916e5` | http://www.ny5y.cn/ueditor/php/upload/image/20221013/1665630004218214.png |
| 许桂璇 | 精神心理科 | 中级 | 主治医师 | 111273 | 413×579 | png/png | `7c3fc546bc87bbd41961b49f4672d15f2fb8fbbfd5c7602143128c59b56a587e` | http://www.ny5y.cn/ueditor/php/upload/image/20221014/1665718037585576.png |
| 杨柳 | 超声诊断科 | 副高 | 副主任医师 | 193711 | 1269×1392 | jpg/jpg | `e1fa82afeaf5b6e68c0dfc35199c6b9134eb81bf604b6f95cfe6eb2867ec34d0` | http://www.ny5y.cn/ueditor/php/upload/image/20260507/1778115130809040.jpg |

详细声明/实际双列、HTTP、魔数和命名见 `D:\workspace\信息收集整理\work\南方医科大学第五附属医院_photo_backfill_trial_manifest.csv` 与 `D:\workspace\信息收集整理\work\南方医科大学第五附属医院_photo_backfill_trial_payload.json`。

## 占位与视觉四门禁

1. query Base64 解码含 blank/placeholder/default 时拦截。
2. 全图唯一颜色数不大于 2 时拦截。
3. 跨医生同 SHA 时停止并标注“待 owner 追认”；本样本重复 SHA 组 0。
4. 拼图使用灰底和深色边框；空白/不可见格熔断。联系表：`D:\workspace\信息收集整理\work\南方医科大学第五附属医院_photo_backfill_trial_contact_sheet.jpg`。

视觉状态：`PASSED_10_OF_10_VISIBLE_SINGLE_DOCTOR_PROFESSIONAL_PORTRAITS`。

## 正式资产零修改

| 文件 | 字节 | SHA-256 |
|---|---:|---|
| `D:\workspace\信息收集整理\work\珠三角三甲医院_医生画像自动采集总底表_payload.json` | 24947704 | `4a71e0a10b43349c246f33e4448ae8882ed8ee79443d1f25cb5a25191ba25bb1` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv` | 18594814 | `07c8b7aa21c86d5797da03719eea5daf8e6c253132713899296bd8d3693b2db7` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx` | 5100604 | `8fcb09d6a64f73731b5d5b70463d3f928e338f6c8056097f1f68a51f847323c7` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 5590 | `cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a` |

- 本院画像树：135 个文件，聚合 SHA-256 `1492e5ac46f1bf4ccb7cb5d06249c4208298e33596fd8c2f62def5a4992a2d2a`。
- 正式照片树前后一致：`{"exists": false, "file_count": 0, "bytes": 0, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}`。
- TRIAL 仅写 `work/` 工件，未回填总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件完成后提交并发布 `TRIAL_READY_FOR_OWNER_AUDIT`，等待 Owner 审计。未取得当前 PR 的明确 `FULL_APPEND_AND_OBSIDIAN` 指令前，不得回填正式资产。
