# 中山大学孙逸仙纪念医院照片补录 TRIAL 报告

## 门禁与范围

- GitHub Issue：#69
- Phase：TRIAL
- 医院官网：https://www.gzsys.org.cn/
- 医生目录：https://www.gzsys.org.cn/doctor/592/search
- 总底表固定范围：658 行；来源链接唯一 658；TRIAL 前照片字段非空 0。
- 试采：10/10；科室首原子 10；职称分层 {"正高": 3, "副高": 4, "其他": 3}。

## 来源与会话边界

- 只解析 `.other-left .other-media .media-img[data-image-url]`；TRIAL 对公共 `mini200`、默认图、院徽和 inline-images 的下载数为 0。
- 照片路径风格：{"doctor-subdir": 5, "files-root": 5}；详情路由：{"node": 5, "doctor": 5}。
- 常规 Cookie 会话只记录名称：CT6T, CT6TS；所有照片请求携带对应详情页 Referer；页面未引用路径探测 0；第三方来源 0。
- 实现前结构诊断曾由宽泛 `data-image-url` 正则额外请求 18 个页面已引用 `mini200` 公共图标；未写文件、未进入 payload/联系表/正式资产。TRIAL 已改为容器限定解析，并以测试固定排除边界。

## 结果

- 详情成功 10/10；照片成功 10/10；详情失败 0；无照片容器 0；占位图 0；照片失败 0。
- 状态闪烁 0；>20 MiB 熔断 0；>5 MiB owner 清单 0。
- 总字节 11,933,516；最小 10,354；中位数 1,478,584；平均 1,193,351；最大 2,668,268。
- 大小分桶：{"<200KiB": 3, "200KiB-1MiB": 1, "1-5MiB": 6, "5-20MiB": 0, ">20MiB": 0}。
- 按样本平均值线性估算 658 行容量：785,224,958 bytes（748.85 MiB），只作容量估算。
- 联系表视觉状态：`PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`。

## 样本清单

- 宋尔卫｜乳腺外科｜主任医师｜node｜doctor-subdir｜23,352 bytes｜247×338｜`5ae0e992c91073ca0882ac0a1208a9634cff5c8104f6a56f151603398f7d9c8c`
- 陈样新｜心血管内科｜主任医师｜node｜files-root｜1,731,623 bytes｜2450×3589｜`08338ee737613de07f475332030be71b55e3762f6c1d831f0aabd334c093dbd8`
- 詹俊｜消化内科｜主任医师｜doctor｜doctor-subdir｜10,354 bytes｜168×240｜`e2296a8e111de8f690f827c58ca9bf33767353d6f59de7a7df30fdc1888844e5`
- 黄晓波｜乳腺放疗专科｜副主任医师｜node｜files-root｜132,642 bytes｜413×626｜`ce52e8fa1b3369e30493e3ecd204399b539d1386cc2f702bb76fe195ab7282de`
- 黎江｜乳腺肿瘤中心｜副研究员｜node｜files-root｜1,454,375 bytes｜913×862｜`159b33e2f9e81652654f9c3738d40ecad5eec0bb1dd2fb49841608ce02a20be2`
- 常瑞明｜健康体检中心｜副主任医师｜node｜doctor-subdir｜323,464 bytes｜768×1024｜`ef84c630a561675bb2eab1868d7bbd7c099f44a0bcceda50bcd41a5b90ec690c`
- 马剑达｜风湿免疫科｜副主任医师｜doctor｜files-root｜1,953,463 bytes｜2731×3740｜`7cd5dc63d4f60b2bca3543cbc9844ab64b01b1c19641811971d6ef84c66b5d0e`
- 黄泽坚｜肝胆外科｜主治医师｜doctor｜doctor-subdir｜2,668,268 bytes｜2148×3223｜`7dcce92abe4788f6ead53998745cd48ab888127b4845d5e49471bb691daa8ff4`
- 曾志芬｜全科医学科一科｜主治医师｜doctor｜doctor-subdir｜2,133,181 bytes｜2013×2863｜`ca3ce66587a77d31aeaca1c8a0f8b9ed19c6e0b03a826011883ebf1162feea48`
- 李卓｜肿瘤内科｜主治医师｜doctor｜files-root｜1,502,794 bytes｜1639×2314｜`0ce5b817b7e355845c29cbc8de8999dbf6894ea8c00b6012bef6486360aaa544`

## >5 MiB owner 终审清单

- 无

## 正式资产保护

- 入口台账、总底表 JSON/CSV/XLSX、更新报告、659 个本院 Markdown 聚合快照与正式照片目录在 TRIAL 前后完全一致：True。
- TRIAL 只写 `work/` 工件；未回填三载体、未刷新画像、未创建正式照片目录。

## 停止点

TRIAL 工件完成后停止，等待 owner 审计。未取得明确 `FULL_APPEND_AND_OBSIDIAN` 前，不得写正式资产。
