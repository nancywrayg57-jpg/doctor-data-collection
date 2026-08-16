# Issue #59 中山大学肿瘤防治中心照片补录 TRIAL 报告

> Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
> 生成日期：2026-08-16
> 视觉复核：`PASS_10_OF_10_SINGLE_ADULT_PROFESSIONAL_PORTRAITS`

## 范围与抽样

- 总底表目标范围：543 行；照片链接/照片文件均为空；来源链接唯一 543。
- 固定样本：10 位，覆盖 10 个科室；职称分层为 正高 4、副高 5、其他 1。
- 样本包含 owner 预检页 `/node/3795`、`/node/3678`，低/高 node ID、医技职称、教授和字段未标注页。
- 详情页：HTTP 200 为 10/10；无照片容器 0；占位图 0；结构异常 0。
- 发现的页面模板：body.page-node-type-doctor > .title-4-0 .item-media img=10；全部已由样本覆盖。
- 熔断三态合计 0/10（0.0%），未超过 owner 规定的 30% 门槛。
- 常规会话仅记录 Cookie 名称：CT6T, CT6TS；不记录 Cookie 值。照片请求均携带对应详情页 Referer。

## 实图、命名与容量

- 实图：10 张；全部保存页面自身引用的官网响应原始字节，未压缩。
- 总字节：1766318；平均：176631 bytes。
- 按平均值对 543 行线性估算：95910633 bytes（约 91.47 MiB）；仅供 owner 裁决，不代表 FULL 最终可得数或实际容量。
- 单张 >200KB：2/10；宽 >800px：0/10。
- 页面未引用路径构造/探测请求：0；第三方来源：0。

| 姓名 | 科室 | 层级 | 主职称 | 引用类型 | 文件名 | 字节 | 尺寸 | SHA-256 | 页面引用照片 |
|---|---|---|---|---|---|---:|---:|---|---|
| 夏忠军 | 血液肿瘤科 | 副高 | 副主任医师 | 派生图 | 夏忠军-血液肿瘤科-副主任医师-中山大学肿瘤防治中心.jpg | 182399 | 400×600 | `c1eb82d91d0e2f04c3fd122dbacdb89ae433952cce2ff200a88ce0a49e7fb829` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2023-04/xiazhongjun-xyzlk-202304.jpg?itok=a1jWIC9q |
| 李力人 | 结直肠科 | 正高 | 主任医师 | 派生图 | 李力人-结直肠科-主任医师-中山大学肿瘤防治中心.jpg | 184053 | 400×600 | `0e1c45a2d519c3dd26021f75dc3916cb72d916ad34cfa1d3c2e00823f21fc582` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2023-03/liliren-jzck-202303.jpg?itok=QCbgPT4_ |
| 吴锡文 | 临床营养科 | 副高 | 副主任医师 | 派生图 | 吴锡文-临床营养科-副主任医师-中山大学肿瘤防治中心.jpg | 222682 | 400×600 | `d70b9799fcdb36458b48837e547bacf56774c5432055b1c7c565b3297b61fbc7` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2026-05/%E5%90%B4%E9%94%A1%E6%96%87.jpg?itok=i2dpTSNg |
| 张玉晶 | 未标注 | 其他 | 未标注 | 派生图 | 张玉晶-未标注-未标注-中山大学肿瘤防治中心.jpg | 187622 | 400×600 | `d535a3de0a295263257412edd98e598cbd6963b693c7df4c1598a8c5e5537145` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2023-03/zhangyujing-flk-202303.jpg?itok=qKl-dvbf |
| 张翼鷟 | 儿童肿瘤科 | 正高 | 主任医师 | 派生图 | 张翼鷟-儿童肿瘤科-主任医师-中山大学肿瘤防治中心.jpg | 208499 | 400×600 | `e0678a83043c6d89f2110554562713370b331e69f602fadd870aabbfacc48e24` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2023-03/zhangyizhuo-etzlk-202303.jpg?itok=6w-up3rS |
| 张伟光 | 核医学科 | 副高 | 副主任技师 | 派生图 | 张伟光-核医学科-副主任技师-中山大学肿瘤防治中心.jpg | 119296 | 400×600 | `edcd869971132121384168562c3d4c7cefcaa5530805f2e9234490e88ff1f6d9` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/import_images/upload/users/74/20210715/%E5%85%89%E8%80%81%E5%B8%88.webp_68437.jpg?itok=5vTcwxJj |
| 刘方杰 | 放疗科 | 副高 | 副主任医师 | 派生图 | 刘方杰-放疗科-副主任医师-中山大学肿瘤防治中心.jpg | 196322 | 400×600 | `1923931437abc2735b77f93e127d6fa45876a481df185fd409c574dc9e9359dc` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2024-06/%E5%88%98%E6%96%B9%E6%9D%B0.JPG?itok=y-c78e3H |
| 何霞 | 检验科 | 副高 | 副主任技师 | 派生图 | 何霞-检验科-副主任技师-中山大学肿瘤防治中心.jpg | 105021 | 400×600 | `2bc3f13c5e7129785f81d8d9063cc475e594da6066efea5604ba80a880d72993` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2026-07/%E4%BD%95%E9%9C%9E-%E7%85%A7%E7%89%87.jpg?itok=7vxedyIq |
| 刘卓炜 | 泌尿外科 | 正高 | 一级主任医师 | 派生图 | 刘卓炜-泌尿外科-一级主任医师-中山大学肿瘤防治中心.jpg | 188412 | 400×600 | `8ea9c7ae22c01c2e8ec059e044b8581ab69995cd4daf3c5a314c39a1f8014c29` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2023-03/liuzhuowei-mnwk-202303.jpg?itok=o_PncJq1 |
| 夏建川 | 生物治疗中心 | 正高 | 教授 | 派生图 | 夏建川-生物治疗中心-教授-中山大学肿瘤防治中心.jpg | 172012 | 400×600 | `c1e9383171fb11bb0d3f28859da42a5a741f09a126e74aaac57fddf749b091bb` | https://www.sysucc.org.cn/sites/cc.prod.sysucloud2.sysu.edu.cn/files/styles/media_2_3_400_600/public/2023-03/xiajianchuan-swzlzx-202303.jpg?itok=YiziUGXZ |

详细 HTTP、魔数和逐图命名清单见：`D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_trial_manifest.csv` 与 `D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_trial_payload.json`。

## 派生图与原图引用说明

- 页面直接引用派生图：10/10；直接引用原图：0/10。
- 派生样式分布：{"media_2_3_400_600": 10}。
- 本轮逐字保留医生职业照容器自身引用的 URL 与 `itok`，未删除查询参数、未构造对应原图路径、未探测任何页面未引用资源。
- 若全部样本只引用派生图，则按 owner 明示的眼科中心判例，提交该派生图原始响应字节供 owner 预期批准；是否进入 FULL 仍由 owner 裁决。

## 视觉判定标准与复核

1. 本人职业照：必须位于该医生 `.title-4-0 .item-media img`，详情标题与底表姓名一致，照片由 `src`/明确懒加载属性直接引用；联系表中视觉上为单人成人职业照。
2. 占位图：路径含 default/avatar/placeholder/logo/Bitmap 等标记、多个医生重复同一 SHA-256，或视觉为公共装饰图、二维码、患者、儿童、合影时拒绝。
3. 联系表：`D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_trial_contact_sheet.jpg`；当前状态为 `PASS_10_OF_10_SINGLE_ADULT_PROFESSIONAL_PORTRAITS`。

## 受保护正式资产零变更

| 文件 | 字节 | SHA-256 |
|---|---:|---|
| `D:\workspace\信息收集整理\work\珠三角三甲医院_医生画像自动采集总底表_payload.json` | 23923488 | `4544ac26a4d0906961496ddc1056e931c256aaded1fbae2bc7f778ac6d12a7f8` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv` | 17571049 | `8c046da50f30515a873a3e0fde3aef4daecc1bcf5779e0986e228c05bd2eb41a` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx` | 4795863 | `43ec8f36dd4d77e185ee414ec8ebfaeab9e2a33e5396033266a1047af2e3311a` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表_更新报告.md` | 5590 | `cd6fff06b933f4a765838281f52f06f3e1228fcea37e5d3b4a9441bd8120d96a` |
| `D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院官网入口台账.xlsx` | 40025 | `d6b08b3f284654024fad0eeac3377b095025dc294732db030e8cc5b81655b782` |

- 本院画像树：544 个文件，SHA-256 `bd425998ef8b1d8b616d1521370a218dae698404b80ee37c396d2c8c9fa81a7c`。
- 本院正式照片目录执行前后状态一致：{"exists": false, "file_count": 0, "bytes": 0, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}。
- TRIAL 照片只写入 `work` 下独立目录：`D:\workspace\信息收集整理\work\中山大学肿瘤防治中心_photo_backfill_trial_photos`；未写总底表、正式画像或正式照片目录。

## 当前停止点

TRIAL 工件完成后停止，等待 owner 审计照片质量、样本大图分布、派生图政策和 543 行容量估算。未取得 owner 明确 `FULL_APPEND_AND_OBSIDIAN` 前，不得回填三载体、刷新画像或写正式照片目录。
