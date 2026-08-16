# Issue #57 中山大学附属第三医院照片补录 TRIAL 报告

> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 生成日期：2026-08-16
> 视觉复核：`PASS_10_OF_10_SINGLE_ADULT_PROFESSIONAL_PORTRAITS`

## 范围与抽样

- 总底表目标范围：780 行；照片链接/照片文件均为空；来源链接唯一 780。
- 固定样本：10 位，覆盖 10 个科室；职称分层为 正高 3、副高 2、中级 2、初级 3。
- 详情页：HTTP 200 为 10/10；无照片容器 0；占位图 0；结构异常 0。
- 熔断三态合计 0/10（0.0%），未超过 owner 规定的 30% 门槛。
- 常规会话仅记录 Cookie 名称：3c6e856e6a804d4b9f597865f16e91e0, CT6T, CT6TS；不记录 Cookie 值。照片请求均携带对应详情页 Referer。

## 实图、命名与容量

- 实图：10 张；全部保存页面自身引用的官网响应原始字节，未压缩。
- 总字节：4953604；平均：495360 bytes。
- 按平均值对 780 行线性估算：386380800 bytes（约 368.48 MiB）；仅供 owner 裁决，不代表 FULL 最终可得数或实际容量。
- 单张 >200KB：4/10；宽 >800px：6/10。
- 页面未引用路径构造/探测请求：0；第三方来源：0。

| 姓名 | 科室 | 层级 | 主职称 | 文件名 | 字节 | 尺寸 | SHA-256 | 页面引用照片 |
|---|---|---|---|---|---:|---:|---|---|
| 张晓红 | 感染性疾病科 | 正高 | 主任医师 | 张晓红-感染性疾病科-主任医师-中山大学附属第三医院.jpg | 189270 | 500×702 | `35249fdb9c9a2ee3d48fa4e899837607d36b44822175b3253461413c828c7fbd` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/2014021909275728200283.jpg |
| 张炎 | 不育与性医学科 | 正高 | 主任医师 | 张炎-不育与性医学科-主任医师-中山大学附属第三医院.jpg | 129963 | 521×694 | `7141704879cda58dbac5bd2df50ef6e8d344fcde557ad354751b08b395304fa5` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/2014031122491698609594.jpg |
| 吴玲玲 | 产科 | 正高 | 主任医师 | 吴玲玲-产科-主任医师-中山大学附属第三医院.png | 1792350 | 2480×1949 | `63480558e9a2e05e5925a53370a72a90abfcc6965daa4b68cbeb92ed684d8244` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/f428bd0cdf91c5f705f7880f664a018.png |
| 李名安 | 介入科 | 副高 | 副主任医师 | 李名安-介入科-副主任医师-中山大学附属第三医院.jpg | 762255 | 2022×2172 | `60b88cda2d1276f0aae049ca5d9ee144bb782c63abfb77b50ec7d842e4352339` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/%E6%9D%8E%E5%90%8D%E5%AE%89.jpg |
| 唐新意 | 儿科 | 副高 | 副主任医师 | 唐新意-儿科-副主任医师-中山大学附属第三医院.jpg | 122750 | 390×567 | `e60bb5b46393650db6e19fe9a30b176d3ae7f4e462a585814a9a443b3e73c40e` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/2019031312012796557340.jpg |
| 巴俊慧 | 内科ICU | 中级 | 主治医师 | 巴俊慧-内科ICU-主治医师-中山大学附属第三医院.jpg | 169165 | 851×1179 | `9a76d854133d1483952b45ac5338b518ee0715c6ebc855981de00064dd4638a9` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/%E5%B7%B4%E5%B7%B4%E8%AF%81%E4%BB%B6%E7%85%A7.jpg |
| 杨婷 | 核医学科 | 中级 | 主治医师 | 杨婷-核医学科-主治医师-中山大学附属第三医院.png | 1256240 | 1280×1642 | `eb2b3a074a9da970f205e6a9c750e789a6e857c454879a30fdf118ab75bd6c87` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/%E6%9D%A8%E5%A9%B71.png |
| 周攀 | 脊柱侧弯中心 | 初级 | 医师 | 周攀-脊柱侧弯中心-医师-中山大学附属第三医院.jpg | 362675 | 1879×2334 | `b576d1ce4a9fd253e69de069986b433158aa572797b89778906d5cf50024a17b` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/1_18.jpg |
| 黄晓飞 | 脑血管外科 | 初级 | 医师 | 黄晓飞-脑血管外科-医师-中山大学附属第三医院.png | 88362 | 295×441 | `ee91b257b0f14039d4e6fbbb313416465a944cc83f95c4ace37ef4309a87898c` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/%E5%9B%BE%E7%89%872_4.png |
| 李舣婷 | 全科医学科 | 初级 | 住院医师 | 李舣婷-全科医学科-住院医师-中山大学附属第三医院.jpg | 80574 | 1080×1571 | `2167fb32b99ecfc1f292b9c1240952ca706f6377a934c3c24d48b52047d014d7` | https://www.zssy.com.cn/sites/zssy.prod.sysucloud1.sysu.edu.cn/files/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20210827182004.jpg |

详细 HTTP、魔数和逐图命名清单见：`D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_manifest.csv` 与 `D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_payload.json`。

## 视觉判定标准与复核

1. 本人职业照：必须位于该医生 `.physician-details-left .physician-details-media .media-img` 内，详情标题与底表姓名一致，照片由 `data-image-url` 或同容器内联 `background-image` 明确引用；联系表中视觉上为单人成人职业照。
2. 占位图：路径含 default/avatar/placeholder 等标记、多个医生重复同一 SHA-256、或视觉为站点通用图/云上三院入口图/期刊二维码时拒绝。
3. 站点通用图：即使位于同页，只要不属于医生左侧详情容器，或是“脑病服务、出诊、服务、云上三院、二维码”等功能图，均不采纳。
4. 联系表：`D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_contact_sheet.jpg`；人工复核 10/10 均为单人成人职业照，未发现患者、儿童、合影、占位图、站点通用图或二维码；状态为 `PASS_10_OF_10_SINGLE_ADULT_PROFESSIONAL_PORTRAITS`。

## 受保护正式资产零变更

| 文件 | 字节 | SHA-256 |
|---|---:|---|
| `D:\workspace\信息收集整理\work\珠三角三甲医院_医生画像自动采集总底表_payload.json` | 24006242 | `e7d366f45693e21e7912c0cfd6cb7e26e8c26c94e5174d9f5c7c39f9db790de8` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv` | 17409562 | `7f8fbfe8ac1772852bdce8ea5237e4593411ba54fbef010b8e7169335f86413f` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx` | 4723935 | `283217c4f74595b409b89933a2da8faf2046ca7d51810fac369df3a533f90b22` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 5590 | `cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a` |

- 本院画像树：743 个文件，SHA-256 `9242708b2a268afd40aea54e60b73d04af97c3c3655b5ecd1415c31e59974d4e`。
- 本院正式照片目录执行前后状态一致：{"exists": false, "file_count": 0, "bytes": 0, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}。
- TRIAL 照片只写入 `work` 下独立目录：`D:\workspace\信息收集整理\work\中山大学附属第三医院_photo_backfill_trial_photos`；未写总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件完成后停止，等待 owner 审计照片质量、样本大图分布和 780 行容量估算。未取得 owner 明确 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填三载体、刷新画像或写正式照片目录。
