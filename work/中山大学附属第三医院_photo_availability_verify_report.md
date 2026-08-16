# 中山大学附属第三医院照片可得性核验报告

> Issue：[#57](https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/57)
> Phase：`VERIFY_PHOTO_AVAILABILITY`
> 核验日期：2026-08-16
> 结论：`PHOTO_FOUND_STOP_FOR_OWNER_TRIAL`

## 1. 执行范围

按 Issue #57 先建立官网常规会话，再打开指定专家目录与 owner 预检样本。首个详情样本即发现页面明确引用的本人职业照，因此依 Issue 的“发现照片后立即停止”分支终止普查；未继续访问其余 29 个详情页，也未开展其他列表模板页核验。

本轮未修改总底表 payload、CSV、XLSX、更新报告、画像或照片目录。

## 2. 命中样本

| 项目 | 结果 |
|---|---|
| 医生 | 张晓红 |
| 详情页 | <https://www.zssy.com.cn/node/11100> |
| 页面标题 | `张晓红 \| 中山大学附属第三医院` |
| 首页 / 详情页 HTTP | `200 / 200` |
| 页面容器 | `.physician-details-left .physician-details-media .media-img` |
| 呈现方式 | `data-image-url` + 内联 `background-image` 的 CSS 背景图 |
| 页面引用照片 | <https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/2014021909275728200283.jpg> |
| 照片响应 | `200 image/jpeg`，189,270 bytes |
| SHA-256 | `35249FDB9C9A2EE3D48FA4E899837607D36B44822175B3253461413C828C7FBD` |
| 魔数 | `FFD8FFE000104A4649460001`（JPEG） |
| 视觉复核 | 单人成人职业照；不是患者、儿童、占位图或站点通用图 |

页面渲染后的关键 DOM：

```html
<div class="physician-details-media">
  <div
    class="media-img"
    data-toggle="bgImage"
    data-image-url="/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/2014021909275728200283.jpg"
    style="background-image: url(...);"
  ></div>
</div>
```

该容器与“张晓红”姓名位于同一 `.physician-details-left` 医生详情区。页面另有 banner、导航图标、二维码、页脚 APP 图和 Lightbox 控件图，均不属于医生本人照片，已排除。

## 3. 会话与合规

- 使用官网首页首次响应建立常规浏览会话，随后同一会话访问详情页；只记录 Cookie 名称 `3c6e856e6a804d4b9f597865f16e91e0`、`CT6T`、`CT6TS`，不记录 Cookie 值。
- 照片 URL 来自页面自身 `data-image-url`，没有构造、替换或探测任何未引用图片路径。
- 浏览器渲染 DOM 与普通公开 HTTP 会话互相验证；没有登录、验证码、挑战求解或非公开接口访问。

## 4. 根因与下一步

owner 预核验的“无照片”结论遗漏了 CSS 背景图：详情页不使用医生 `<img>`、`srcset` 或懒加载属性，而由站点脚本把 `data-image-url` 写入 `.media-img` 的 `background-image`。因此“全院官网不提供医生照片”的前提不成立。

按 Issue #57 指令，当前停止并等待 owner：

1. 将任务切换为常规照片 `TRIAL`；
2. 明确抽样规模、照片路径政策与后续 FULL 门禁；
3. Codex 在新指令前不继续普查、不下载正式照片、不写正式资产。
