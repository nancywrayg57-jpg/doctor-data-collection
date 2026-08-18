# Issue #71 中山大学附属第一医院照片补录 TRIAL 报告

## 门禁与范围

- Phase：`TRIAL_READY_FOR_OWNER_AUDIT`
- 医院官网：https://www.fahsysu.org.cn/
- 医生目录：https://www.fahsysu.org.cn/page/6945
- 固定范围：860 行 / 860 个唯一 `/node/<ID>`；TRIAL 前照片字段非空 0。
- Owner 裁决：10 张成功照片采用正高 5 + 副高 5、覆盖 10 个不同科室首原子；另以 2 条“其他”层无照片记录验证失败留证。
- TRIAL 对账：12 行 = 成功 10 + 失败留证 2。

## 来源与字节边界

- 只解析 `.other-left .other-media .media-img[data-image-url]` 中页面实际引用的 `styles/focal_point_480` URL，并保留每个 URL 唯一的 `itok`；不构造原图路径。
- 公共 `styles/mini200`、banner、inline-images、default_images 和装饰资源下载数：0。
- 页面未引用路径探测：0；第三方来源：0。
- 正式资产前后快照一致：True。

## 成功结果

- 详情成功 12/12；照片成功 10/10；职称分层 {"正高": 5, "副高": 5}。
- 总字节 1,769,345；最小 138,120；中位数 164,711；平均 176,934；最大 240,886。
- 大小分桶：{"<200KiB": 8, "200KiB-1MiB": 2, "1-5MiB": 0, "5-20MiB": 0, ">20MiB": 0}；>5 MiB owner 清单 0；>20 MiB 0。
- 按样本平均值线性估算 860 行：152,163,240 bytes（145.11 MiB），仅作容量估算。
- 联系表视觉状态：`PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。

- 郭宇｜普通外科｜主任医师｜138,120 bytes｜480×480｜`8f6ca8200e8c29c8fe4d2b91843db4fe53dfe5015563db341a803d5dfd9391c1`｜itok `bOTm8n47`
- 陈昆｜神经外科｜主任医师｜228,003 bytes｜480×480｜`20d3be34791aaae72bc893ace22a18d6f8c6f38c7692d33e0a2f8d13ea654d1f`｜itok `iEOQvbHw`
- 陈蕾｜烧伤与创面修复科｜主任医师｜155,594 bytes｜480×480｜`95bc0bf15134c3e6a3c2fca13b985a543ea7dbeffde2f9f34f6bf7a68330ef41`｜itok `dZ3rDTWU`
- 陈炜｜泌尿外科｜主任医师｜156,169 bytes｜480×480｜`6fcbb20198ae056cef4610f894284a741eaba6d65684661003160aec29c71dcc`｜itok `Ss1scQ85`
- 高勇｜男科｜主任医师｜147,348 bytes｜480×480｜`110f2579902d3458ae024a8e6f9a991da7366bd548b0cbc94ab29ab3c0efe5ef`｜itok `wNTLuzu8`
- 陈华东｜小儿外科｜副主任医师｜173,253 bytes｜480×480｜`86c9052b38279485a4a1be3cc8b094c8c01cbd7acd03d66ec97e5327a32739cf`｜itok `d6Jyu392`
- 程钢｜整形外科｜副主任医师｜154,419 bytes｜480×480｜`d007338ba3464aa43715e2decd461a9e23efe4e62656d6b158867f2bccf59427`｜itok `w_N9F_Il`
- 雷艺炎｜胸外科｜副主任医师｜195,696 bytes｜480×480｜`4dfdcfb3d07cf27510fabe2cee1e431cbfa45c89f63e3975949987239c9c25be`｜itok `9Tgdq8iX`
- 汪睿｜血管外科｜副主任医师｜240,886 bytes｜480×480｜`a8322ce000192e6cef84ad80bfb37f1c3101e74c529ef3499ad525dd23dc7e0e`｜itok `eMFgyMQO`
- 林维浩｜甲状腺外科｜副主任医师｜179,857 bytes｜480×480｜`eece333184d87678e10422ff4a34e2025875d85e9c5bffb06bf56e057d71ad96`｜itok `-VxB9nzJ`

## 两条失败路径证据

- 黄雄庆｜https://www.fahsysu.org.cn/node/5780｜HTTP 200｜UTC `2026-08-18T12:28:35Z`｜`无照片容器`｜focal_point_480 引用数=0；医生照片容器缺失；页面 media-img 仅有 5 个 path contains /styles/mini200/ 公共图标
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-1-3.png?itok=N7xVlmOY｜path contains /styles/mini200/
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-1-6.png?itok=e9BYn97e｜path contains /styles/mini200/
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-1-1_0.png?itok=lMXpEjLC｜path contains /styles/mini200/
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-2-8.png?itok=XyTEzUHK｜path contains /styles/mini200/
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-1-2_0.png?itok=thPXMwH8｜path contains /styles/mini200/
- 张旭宇｜https://www.fahsysu.org.cn/node/5795｜HTTP 200｜UTC `2026-08-18T12:28:36Z`｜`无照片容器`｜focal_point_480 引用数=0；医生照片容器缺失；页面 media-img 仅有 5 个 path contains /styles/mini200/ 公共图标
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-1-3.png?itok=N7xVlmOY｜path contains /styles/mini200/
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-1-6.png?itok=e9BYn97e｜path contains /styles/mini200/
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-1-1_0.png?itok=lMXpEjLC｜path contains /styles/mini200/
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-2-8.png?itok=XyTEzUHK｜path contains /styles/mini200/
  - https://www.fahsysu.org.cn/sites/1h.prod.sysucloud1.sysu.edu.cn/files/styles/mini200/public/action-9-1-2_0.png?itok=thPXMwH8｜path contains /styles/mini200/

两条记录均未下载照片字节、未创建照片文件；其 5 个 `mini200` URL 只作为排除证据记录。

## >5 MiB owner 终审清单

- 无

## 正式资产保护与停止点

- 入口台账、总底表 JSON/CSV/XLSX、更新报告、861 个本院文件聚合快照与不存在的正式照片目录在 TRIAL 前后完全一致。
- TRIAL 只写 `work/` 工件；未回填三载体、未刷新画像、未创建正式照片目录。
- 工件完成后停止，等待 owner 审计；未取得明确 `FULL_APPEND_AND_OBSIDIAN` 前不得写正式资产。
