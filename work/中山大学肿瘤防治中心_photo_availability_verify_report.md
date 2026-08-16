# 中山大学肿瘤防治中心照片可得性核验报告

> Issue：[#59](https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/59)
> Phase：`VERIFY_PHOTO_AVAILABILITY`
> 核验日期：2026-08-16
> 结论：`PHOTO_FOUND_STOP_FOR_OWNER_TRIAL`

## 1. 执行范围

按 Issue #59 先访问医院官网首页建立常规公开会话，再访问指定临床专家目录与 owner 预检样本。首个详情样本 <https://www.sysucc.org.cn/node/3795> 即发现页面明确引用的夏忠军本人职业照，因此取消 30 个详情页及至少 3 个列表模板页的后续普查，不再扩大访问范围。

首轮预设的结构对比请求批次已依次完成以下页面后才返回汇总结果：

1. 官网首页与临床专家目录；
2. 4 个详情页：`/node/3795`、`/node/3678`、`/node/12740`、`/node/1664`；
3. 1 个底表既有非医生来源页：`/taxonomy/term/267`。

该固定批次的 4 个医生详情页均存在同一 `item-media` 医生照片结构；本报告以首个命中样本 `/node/3795` 为正式证据。发现后未再执行其他候选页、分页或接口请求。后续同类核验应在请求循环内命中即 `break`，避免固定诊断批次在首个命中后继续完成剩余预设请求。

本轮未修改总底表 payload、CSV、XLSX、更新报告、画像或正式照片目录。

## 2. 命中样本

| 项目 | 结果 |
|---|---|
| 医生 | 夏忠军 |
| 详情页 | <https://www.sysucc.org.cn/node/3795> |
| 页面标题 | `夏忠军 \| 中山大学肿瘤防治中心` |
| 页面 HTTP / Content-Type | `200 / text/html` |
| 页面大小 | 48,015 bytes |
| 页面模板 | `body.page-node.page-node-type-doctor` |
| 照片容器 | `.title-4-0 .item-media` 内的医生 `<img>` |
| 照片元素 class | `w-full p-sm rounded-6 bg-white shadow-md` |
| 呈现方式 | 标准 `<img src>`，不是 CSS 背景图或 JS 推导路径 |
| 页面引用照片 | <https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2023-04/xiazhongjun-xyzlk-202304.jpg?itok=a1jWIC9q> |
| 照片响应 | `200 image/jpeg`，182,399 bytes |
| 图片尺寸 | 400×600 |
| SHA-256 | `C1EB82D91D0E2F04C3FD122DBACDB89AE433952CCE2FF200A88CE0A49E7FB829` |
| 魔数 | `FFD8FFE000104A464946000101010060`（JPEG） |
| 视觉复核 | 单人成人职业照；穿白大褂，胸前为中山大学肿瘤防治中心标识；不是患者、儿童、合影、占位图、二维码或站点公共装饰图 |

关键 DOM 归属链：

```text
.container
  .layout.row.layout-builder__layout
    .views-element-container
      .title-4-0.d-flex
        .item-media
          img.w-full.p-sm.rounded-6.bg-white.shadow-md
```

## 3. 与 owner 预检差异

Owner 预检将 `/node/3795` 与 `/node/3678` 判为仅命中公共装饰图 `2022-11/Bitmap.png`。现场普通 HTTP 会话直接读取原始详情 HTML 后确认，两页除公共装饰图外还各有一个位于 `.item-media` 的标准医生 `<img src>`；照片路径位于：

```text
/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/
```

因此“详情页无本人照片”的前提不成立。现有证据只能确认预检扫描未纳入该医生内容区标准 `<img src>`，不能在缺少 owner 扫描脚本的情况下进一步推断具体实现原因。

## 4. 会话与合规

- 使用官网首页首次响应建立常规 Cookie 会话，Cookie 名称为 `CT6T`、`CT6TS`；不记录 Cookie 值。
- 目录、详情页和照片均为医院官方域名 `www.sysucc.org.cn` 的公开响应。
- 照片 URL 逐字来自 `/node/3795` 页面自身 `<img src>`；照片请求携带对应详情页 Referer。
- 未构造、替换或探测页面未引用图片路径；未访问第三方平台、登录后数据、患者评价或隐私信息。
- 临床专家目录在常规会话内返回 `200 text/html`、125,190 bytes；未绕过登录、验证码、挑战或权限控制。

## 5. 停止点与下一步

依 Issue #59 二选一门禁，本轮采用 `PHOTO_FOUND_STOP_FOR_OWNER_TRIAL`：

1. 不继续 30+3 页零照片普查；
2. 不写正式照片、底表或画像；
3. 将照片呈现方式、样例 URL、响应与视觉证据提交原 Issue / PR；
4. 等待 owner 将 Issue #59 切换为常规照片 `TRIAL` 并明确抽样、命名、大图和 FULL 门禁。
