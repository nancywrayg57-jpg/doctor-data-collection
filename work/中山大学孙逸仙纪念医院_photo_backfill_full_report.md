# Issue #69 中山大学孙逸仙纪念医院照片补录 FULL 报告

> 日期：2026-08-18
> Phase：`FULL_READY_FOR_FINAL_OWNER_AUDIT`

## 四数对账

| 目标 | 实采 | 失败 | 落盘 | 留空 |
|---:|---:|---:|---:|---:|
| 658 | 597 | 61 | 597 | 61 |

- 复用已审计 TRIAL：10；FULL 新抓取：587；其余待抓取目标：648。
- 失败率：9.27%；状态闪烁：1；已完成 5 轮聚合并复用冻结原图：1。

| 失败三态 | 数量 |
|---|---:|
| 详情不可达 | 1 |
| 无照片容器 | 0 |
| 占位图 | 60 |

## 大小与来源

| 大小分桶 | 数量 |
|---|---:|
| <200KiB | 375 |
| 200KiB-1MiB | 108 |
| 1-5MiB | 111 |
| 5-20MiB | 3 |
| >20MiB | 0 |

- 总字节：315,236,079（300.63 MiB）；最大：10,364,909 bytes。
- 超过 5 MiB：3；超过 20 MiB：0。
- 路由：{"doctor": 198, "node": 399}；原图路径：{"doctor-subdir": 421, "files-root": 176}。
- 页面未引用路径探测 0；第三方来源 0；TRIAL/正式下载均只使用医生照片容器的页面实际引用。

## >5 MiB Owner 终审清单

- 梁安靖｜https://www.gzsys.org.cn/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/doctor/12463.jpg｜10,364,909 bytes｜3840×5760｜`5e801f22a1ffea6025b772d357fefb88328b68d6a15c1742529dfaf353e05fab`
- 曾伟科｜https://www.gzsys.org.cn/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/doctor/12169.jpg｜5,659,744 bytes｜1548×2064｜`f7e1203dfe7c672f883744091861e2f11e9878d2cf3191bd2854925af2d2af91`
- 梁中锟｜https://www.gzsys.org.cn/sites/syshospital.prod.sysucloud1.sysu.edu.cn/files/doctor/13903.jpg｜5,530,814 bytes｜2400×3600｜`c4ec6bb5d9a6e1d646aa6e481cc06363431dcd4dcd28c2c710dedc51b5cd12d7`

## 失败证据

- 丁红｜占位图｜https://www.gzsys.org.cn/doctor/15624｜占位图
- 钟志坚｜占位图｜https://www.gzsys.org.cn/doctor/15597｜占位图
- 梅少芬｜占位图｜https://www.gzsys.org.cn/doctor/15607｜占位图
- 胡玉新｜占位图｜https://www.gzsys.org.cn/doctor/15629｜占位图
- 刘昀昀｜占位图｜https://www.gzsys.org.cn/node/17010｜占位图
- 冯华英｜占位图｜https://www.gzsys.org.cn/doctor/15609｜占位图
- 杨泉林｜占位图｜https://www.gzsys.org.cn/doctor/15606｜占位图
- 张玉兰｜占位图｜https://www.gzsys.org.cn/doctor/15611｜占位图
- 陈锡龙｜占位图｜https://www.gzsys.org.cn/doctor/15619｜占位图
- 刁飞宇｜占位图｜https://www.gzsys.org.cn/doctor/15632｜占位图
- 谭桂明｜占位图｜https://www.gzsys.org.cn/doctor/15602｜占位图
- 苏浩彬｜占位图｜https://www.gzsys.org.cn/doctor/15616｜占位图
- 蓝球生｜占位图｜https://www.gzsys.org.cn/node/17001｜占位图
- 罗兴喜｜占位图｜https://www.gzsys.org.cn/doctor/15630｜占位图
- 麦贤弟｜占位图｜https://www.gzsys.org.cn/doctor/15612｜占位图
- 张蜀宁｜占位图｜https://www.gzsys.org.cn/doctor/15420｜占位图
- 刘梅兰｜占位图｜https://www.gzsys.org.cn/doctor/15378｜占位图
- 梅志勇｜占位图｜https://www.gzsys.org.cn/doctor/15610｜占位图
- 张国扬｜占位图｜https://www.gzsys.org.cn/node/17023｜占位图
- 曾宪平｜占位图｜https://www.gzsys.org.cn/doctor/15600｜占位图
- 赖义明｜占位图｜https://www.gzsys.org.cn/node/15473｜占位图
- 范新祥｜占位图｜https://www.gzsys.org.cn/doctor/15417｜占位图
- 李佳佳｜占位图｜https://www.gzsys.org.cn/node/17002｜占位图
- 余妙真｜占位图｜https://www.gzsys.org.cn/doctor/15608｜占位图
- 刘文宙｜占位图｜https://www.gzsys.org.cn/doctor/15578｜占位图
- 江川｜占位图｜https://www.gzsys.org.cn/doctor/15495｜占位图
- 郑眉光｜详情不可达｜https://www.gzsys.org.cn/node/25208｜详情不可达：#1 2026-08-18T10:51:20Z HTTP 404 text/html | #2 2026-08-18T10:51:51Z HTTP 404 text/html | #3 2026-08-18T10:52:21Z HTTP 404 text/html
- 徐永腾｜占位图｜https://www.gzsys.org.cn/node/15535｜占位图
- 林宝珠｜占位图｜https://www.gzsys.org.cn/doctor/15613｜占位图
- 熊慧｜占位图｜https://www.gzsys.org.cn/doctor/15470｜占位图
- 马坚池｜占位图｜https://www.gzsys.org.cn/doctor/15405｜占位图
- 唐增奇｜占位图｜https://www.gzsys.org.cn/node/15357｜占位图
- 周明根｜占位图｜https://www.gzsys.org.cn/node/16983｜占位图
- 梁建军｜占位图｜https://www.gzsys.org.cn/node/16986｜占位图
- 王英｜占位图｜https://www.gzsys.org.cn/node/16989｜占位图
- 李睿歆｜占位图｜https://www.gzsys.org.cn/node/17005｜占位图
- 凌小婷｜占位图｜https://www.gzsys.org.cn/node/17008｜占位图
- 王东雁｜占位图｜https://www.gzsys.org.cn/node/17017｜占位图
- 王静姝｜占位图｜https://www.gzsys.org.cn/node/17018｜占位图
- 程帝｜占位图｜https://www.gzsys.org.cn/doctor/15561｜占位图
- 刘婷｜占位图｜https://www.gzsys.org.cn/doctor/15374｜占位图
- 何剑峰｜占位图｜https://www.gzsys.org.cn/doctor/15345｜占位图
- 沈婷｜占位图｜https://www.gzsys.org.cn/node/17015｜占位图
- 梅静思｜占位图｜https://www.gzsys.org.cn/node/17013｜占位图
- 聂晓露｜占位图｜https://www.gzsys.org.cn/doctor/15451｜占位图
- 张露｜占位图｜https://www.gzsys.org.cn/node/17024｜占位图
- 李凌｜占位图｜https://www.gzsys.org.cn/node/17004｜占位图
- 李梓敬｜占位图｜https://www.gzsys.org.cn/doctor/15536｜占位图
- 余韵｜占位图｜https://www.gzsys.org.cn/doctor/15513｜占位图
- 蔡志清｜占位图｜https://www.gzsys.org.cn/node/17028｜占位图
- 何明亮｜占位图｜https://www.gzsys.org.cn/node/16999｜占位图
- 刘正豪｜占位图｜https://www.gzsys.org.cn/node/17011｜占位图
- 麦岚｜占位图｜https://www.gzsys.org.cn/node/17012｜占位图
- 刘艳琼｜占位图｜https://www.gzsys.org.cn/node/17009｜占位图
- 植耀炜｜占位图｜https://www.gzsys.org.cn/node/17025｜占位图
- 周林｜占位图｜https://www.gzsys.org.cn/node/17026｜占位图
- 王静｜占位图｜https://www.gzsys.org.cn/doctor/15566｜占位图
- 林少丹｜占位图｜https://www.gzsys.org.cn/node/17007｜占位图
- 陈钦标｜占位图｜https://www.gzsys.org.cn/node/16994｜占位图
- 廖文华｜占位图｜https://www.gzsys.org.cn/node/17006｜占位图
- 戴佳颖｜占位图｜https://www.gzsys.org.cn/node/16996｜占位图

## 三载体、画像与抽样

- 总底表 payload/CSV/XLSX 逐值一致；仅本院照片两列及失败行异常提示允许变化。
- 成功 597 份 AUTO 画像严格 +2/-0；失败画像零触碰；不新建画像；`_索引.md` 零修改。
- FULL 抽样拼图：`D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_photo_backfill_full_audit_sheet.jpg`，包含最小、最大及 8 个确定性随机样本。
- 入口台账 JSON/CSV/XLSX 与总底表更新报告保持不变。

## 工件

- `D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_photo_backfill_full_payload.json`
- `D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_photo_backfill_full_reconciliation.csv`
- `D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_photo_backfill_full_report.md`
- `D:\workspace\信息收集整理\work\中山大学孙逸仙纪念医院_photo_backfill_full_audit_sheet.jpg`
