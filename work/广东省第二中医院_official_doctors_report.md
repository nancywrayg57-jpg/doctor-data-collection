---
类型: 全量采集归并审计报告
医院: 广东省第二中医院
城市: 广州市
采集日期: 2026-08-12
来源范围: 医院官网
采集入口: https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850 https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850
适配器: gdzy5413_official_specialist
---

# 广东省第二中医院 官方医生全量采集归并审计报告

## 结论

本次试跑只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集全量采集底表，共 342 位唯一医生；官网列表页原始卡片记录 367 条；读取入口分类 2 个；覆盖 65 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 广东省第二中医院 |
| 官网首页 | https://www.gdzy5413.com/main/main.aspx |
| 本轮医生入口 | https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850 https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 |
| 入口来源 | Claude owner Issue 显式多入口 |
| 原台账医生入口 | https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850 |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | A-优先自动采集 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
| 名医名家 | https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850 | 医院官网名医名家单页名单 | 1 | 37 | 21 | 0 | 广东省第二中医院（官网名医名家栏目） | owner 已裁决院区/门诊均属同一法人实体授权范围 |
| 各科专家 | https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 医院官网各科专家单页主目录（ksdoctorinfo 已获 TRIAL-2 授权） | 1 | 346 | 346 | 0 | 广东省第二中医院（官网各科专家栏目） | owner 已裁决院区/门诊均属同一法人实体授权范围 |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：367
- 跨入口去重后唯一候选：367
- 跨入口重复关系：0
- 试采覆盖入口分类：2 个（名医名家、各科专家）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 无 | 无 | 无 |

## 广东省第二中医院同名归并对账

- 详情关系：367
- 最终身份：342
- 白云院区样本：79
- 多链接同一人归并样本：10

| 姓名 | 裁决 | 详情关系 | 合并科室 | 主详情 | 其余详情 |
|---|---|---:|---|---|---|
| 郭智涛 | 同名待甄别 | 1 | 乳腺科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=1290 | 无 |
| 郭智涛 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=614 | 无 |
| 郭智涛 | 同名待甄别 | 1 | 乳腺科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=154 | 无 |
| 张俊杰 | 唯一身份 | 1 | 针灸康复六区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=100&typeid=98&cid=100&ksid=98&id=428 | 无 |
| 范德辉 | 同一人归并 | 3 | 针灸康复科五区、特诊室、针灸康复五区 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=1452 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=615；https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=299 |
| 刘星 | 唯一身份 | 1 | 针灸康复六区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=100&typeid=98&cid=100&ksid=98&id=429 | 无 |
| 刘军 | 唯一身份 | 1 |  | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=1571 | 无 |
| 蔡荣华 | 同一人归并 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1000&typeid=909&cid=1000&ksid=909&id=512 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=526 |
| 邱健行 | 同名待甄别 | 1 |  | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=160 | 无 |
| 邱健行 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=596 | 无 |
| 蔡妙珊 | 唯一身份 | 1 | 五山门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1003&typeid=901&cid=1003&ksid=901&id=436 | 无 |
| 杨思华 | 同名待甄别 | 1 |  | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=484 | 无 |
| 杨思华 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=601 | 无 |
| 沈越 | 唯一身份 | 1 | 五山门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1003&typeid=901&cid=1003&ksid=901&id=437 | 无 |
| 王清海 | 同名待甄别 | 1 |  | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=499 | 无 |
| 王清海 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=598 | 无 |
| 王清海 | 同名待甄别 | 1 | 心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=47 | 无 |
| 魏东 | 同一人归并 | 2 | 五山门诊、感染性疾病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1480&typeid=1472&cid=1480&ksid=1472&id=644 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1003&typeid=901&cid=1003&ksid=901&id=438 |
| 余德钊 | 同名待甄别 | 1 | 儿科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=504 | 无 |
| 余德钊 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=605 | 无 |
| 余德钊 | 同名待甄别 | 2 | 儿科、白云院区儿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=979&typeid=896&cid=979&ksid=896&id=430 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=286 |
| 刘晓俊 | 唯一身份 | 1 | 五山门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1003&typeid=901&cid=1003&ksid=901&id=439 | 无 |
| 李爱华 | 同名待甄别 | 1 |  | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=549 | 无 |
| 李爱华 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=606 | 无 |
| 周亦农 | 同名待甄别 | 2 | 五山门诊、淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1006&typeid=902&cid=1006&ksid=902&id=435 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=517 |
| 周亦农 | 同名待甄别 | 1 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=988&typeid=898&cid=988&ksid=898&id=514 | 无 |
| 谢波 | 同名待甄别 | 1 | 妇科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=554 | 无 |
| 谢波 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=604 | 无 |
| 谢波 | 同名待甄别 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=390 | 无 |
| 劳宗洪 | 唯一身份 | 1 | 五山门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1009&typeid=903&cid=1009&ksid=903&id=441 | 无 |
| 陈宁 | 同名待甄别 | 1 | 呼吸科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=564 | 无 |
| 陈宁 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=610 | 无 |
| 陈宁 | 同名待甄别 | 1 | 呼吸与危重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=341 | 无 |
| 元国华 | 唯一身份 | 1 | 五山门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1009&typeid=903&cid=1009&ksid=903&id=442 | 无 |
| 戈焰 | 同名待甄别 | 2 | 特诊室 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=569 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=603 |
| 戈焰 | 同名待甄别 | 1 | 脾胃病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=68 | 无 |
| 李宝国 | 唯一身份 | 1 | 五山门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1012&typeid=904&cid=1012&ksid=904&id=440 | 无 |
| 汪何 | 同名待甄别 | 1 |  | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=574 | 无 |
| 汪何 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=600 | 无 |
| 汪何 | 同名待甄别 | 1 | 内分泌科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=34&typeid=32&cid=34&ksid=32&id=346 | 无 |
| 林晓洁 | 同名待甄别 | 1 | 治未病(健康体检)中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=482 | 无 |
| 林晓洁 | 同名待甄别 | 1 | 儿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=163 | 无 |
| 吕朝晖 | 同名待甄别 | 1 | 骨二科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=599 | 无 |
| 吕朝晖 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=613 | 无 |
| 吕朝晖 | 同名待甄别 | 1 | 骨伤二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=103 | 无 |
| 郑洁莉 | 唯一身份 | 1 | 治未病(健康体检)中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=483 | 无 |
| 高敏 | 同名待甄别 | 1 | 脑病科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=614 | 无 |
| 高敏 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=611 | 无 |
| 高敏 | 同名待甄别 | 1 | 脑病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=319 | 无 |
| 杨美芝 | 唯一身份 | 1 | 治未病(健康体检)中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=484 | 无 |
| 陈可静 | 同名待甄别 | 1 | 儿科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=629 | 无 |
| 陈可静 | 同名待甄别 | 2 | 特诊室、儿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=287 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=608 |
| 梁兆凤 | 唯一身份 | 1 | 治未病(健康体检)中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=486 | 无 |
| 吕雄 | 同名待甄别 | 1 | 内分泌科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=634 | 无 |
| 吕雄 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=602 | 无 |
| 吕雄 | 同名待甄别 | 1 | 内分泌科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=34&typeid=32&cid=34&ksid=32&id=345 | 无 |
| 钟文鑫 | 唯一身份 | 1 | 治未病(健康体检)中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=487 | 无 |
| 黄琳 | 同名待甄别 | 1 |  | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=659 | 无 |
| 黄琳 | 同名待甄别 | 2 | 内科、特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=549 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=607 |
| 孙正平 | 唯一身份 | 1 | 治未病(健康体检)中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=488 | 无 |
| 许学猛 | 同名待甄别 | 1 |  | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=669 | 无 |
| 许学猛 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=599 | 无 |
| 许学猛 | 同名待甄别 | 2 | 骨伤一科、骨伤三科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=60 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=398 |
| 周盛杰 | 唯一身份 | 1 | 治未病(健康体检)中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=650 | 无 |
| 靳利利 | 同名待甄别 | 1 | 心血管科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=699 | 无 |
| 靳利利 | 同名待甄别 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=519 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=471 |
| 靳利利 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=612 | 无 |
| 靳利利 | 同名待甄别 | 1 | 心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=36 | 无 |
| 徐云英 | 唯一身份 | 1 | 白云院区皮肤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1078&typeid=1076&cid=1078&ksid=1076&id=371 | 无 |
| 陈高峰 | 同名待甄别 | 2 | 肿瘤科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=714 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=281 |
| 陈高峰 | 同名待甄别 | 1 | 白云院区肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=706 | 无 |
| 陈高峰 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=609 | 无 |
| 黄晓萍 | 唯一身份 | 1 | 白云院区耳鼻喉科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1082&typeid=1080&cid=1082&ksid=1080&id=773 | 无 |
| 卢桂梅 | 同名待甄别 | 1 | 内科 | https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=824 | 无 |
| 卢桂梅 | 同名待甄别 | 1 | 特诊室 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=597 | 无 |
| 胡想国 | 唯一身份 | 1 | 白云院区口腔科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1086&typeid=1084&cid=1086&ksid=1084&id=375 | 无 |
| 李桂明 | 同名待甄别 | 1 | 白云院区心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=718 | 无 |
| 李桂明 | 同名待甄别 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=553 | 无 |
| 李桂明 | 同名待甄别 | 1 | 心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=317 | 无 |
| 李德军 | 同名待甄别 | 1 | 白云院区心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=719 | 无 |
| 李德军 | 同名待甄别 | 1 | 心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=318 | 无 |
| 肖根发 | 唯一身份 | 1 | 白云院区心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=720 | 无 |
| 李国彬 | 唯一身份 | 1 | 白云院区心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=721 | 无 |
| 廖坤莹 | 唯一身份 | 1 | 白云院区心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=765 | 无 |
| 周嘉澄 | 同名待甄别 | 1 | 白云院区脑病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1094&typeid=1092&cid=1094&ksid=1092&id=714 | 无 |
| 周嘉澄 | 同名待甄别 | 1 | 脑病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=582 | 无 |
| 彭玉 | 唯一身份 | 1 | 白云院区脑病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1094&typeid=1092&cid=1094&ksid=1092&id=715 | 无 |
| 郭红 | 唯一身份 | 1 | 白云院区脑病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1094&typeid=1092&cid=1094&ksid=1092&id=716 | 无 |
| 蔡艺贞 | 唯一身份 | 1 | 白云院区脑病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1094&typeid=1092&cid=1094&ksid=1092&id=717 | 无 |
| 黎智燊 | 同一人归并 | 2 | 白云院区肿瘤科、肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=695 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=696 |
| 史清华 | 同名待甄别 | 1 | 白云院区肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=707 | 无 |
| 史清华 | 同名待甄别 | 1 | 肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=282 | 无 |
| 武如通 | 同名待甄别 | 1 | 白云院区肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=708 | 无 |
| 武如通 | 同名待甄别 | 1 | 肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=322 | 无 |
| 周伶 | 唯一身份 | 1 | 白云院区肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=709 | 无 |
| 吕丽琼 | 唯一身份 | 1 | 白云院区肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=710 | 无 |
| 李有武 | 唯一身份 | 1 | 麻醉科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=110&typeid=108&cid=110&ksid=108&id=158 | 无 |
| 徐凯 | 唯一身份 | 1 | 白云院区针康复一区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=350 | 无 |
| 高海燕 | 唯一身份 | 1 | 白云院区针康复一区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=351 | 无 |
| 叶恒 | 唯一身份 | 1 | 白云院区针康复一区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=698 | 无 |
| 秦小红 | 唯一身份 | 1 | 白云院区针康复一区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=699 | 无 |
| 杜家津 | 唯一身份 | 1 | 白云院区针康复一区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=700 | 无 |
| 周杰 | 唯一身份 | 1 | 白云院区针康复三区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=352 | 无 |
| 张振宁 | 唯一身份 | 1 | 白云院区针康复三区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=656 | 无 |
| 袁智先 | 唯一身份 | 1 | 白云院区针康复三区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=701 | 无 |
| 邸富荣 | 唯一身份 | 1 | 白云院区针康复三区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=702 | 无 |
| 邓间开 | 唯一身份 | 1 | 白云院区针康复三区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=703 | 无 |
| 林妙君 | 唯一身份 | 1 | 白云院区针康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=704 | 无 |
| 马洪举 | 唯一身份 | 1 | 白云院区针康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=705 | 无 |
| 张晓燕 | 唯一身份 | 1 | 白云院区针康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=722 | 无 |
| 凌翠敏 | 唯一身份 | 1 | 白云院区针康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=723 | 无 |
| 刘文丽 | 唯一身份 | 1 | 白云院区针康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=724 | 无 |
| 李婷 | 唯一身份 | 1 | 白云院区针康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=759 | 无 |
| 贺青涛 | 唯一身份 | 1 | 白云院区针康复六区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1114&typeid=1112&cid=1114&ksid=1112&id=586 | 无 |
| 刘悦 | 同一人归并 | 2 | 白云院区针康复六区、康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1114&typeid=1112&cid=1114&ksid=1112&id=587 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=496 |
| 何桥景 | 唯一身份 | 1 | 白云院区针康复六区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1114&typeid=1112&cid=1114&ksid=1112&id=588 | 无 |
| 林湖广 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=733 | 无 |
| 刘莉 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=734 | 无 |
| 谢秋平 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=735 | 无 |
| 杨淑荃 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=736 | 无 |
| 王朋莉 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=737 | 无 |
| 陈小燕 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=738 | 无 |
| 李翠香 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=739 | 无 |
| 官华良 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=740 | 无 |
| 张勤锐 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=741 | 无 |
| 林楚钊 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=742 | 无 |
| 冯小芹 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=743 | 无 |
| 郑钦毫 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=744 | 无 |
| 王传鑫 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=745 | 无 |
| 彭震峰 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=746 | 无 |
| 刘仁金 | 唯一身份 | 1 | 白云院区传统疗法区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=747 | 无 |
| 杨栋 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=567 | 无 |
| 陈志勇 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=570 | 无 |
| 朱冬娇 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=571 | 无 |
| 何国建 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=573 | 无 |
| 吴振中 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=574 | 无 |
| 梁韵妮 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=575 | 无 |
| 庄婷婷 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=577 | 无 |
| 高辰 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=725 | 无 |
| 林雪珊 | 同名待甄别 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=726 | 无 |
| 林雪珊 | 同名待甄别 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=506 | 无 |
| 杨宇愿 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=727 | 无 |
| 陈博 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=728 | 无 |
| 陈云生 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=729 | 无 |
| 郑恭鹏 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=730 | 无 |
| 王子鸣 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=731 | 无 |
| 邱俊芸 | 唯一身份 | 1 | 白云院区康复治疗区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=732 | 无 |
| 唐敏 | 唯一身份 | 1 | 眼科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=314 | 无 |
| 王霜玲 | 唯一身份 | 1 | 眼科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=315 | 无 |
| 彭明欢 | 唯一身份 | 1 | 眼科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=653 | 无 |
| 王燕 | 唯一身份 | 1 | 眼科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=777 | 无 |
| 李嘉愔 | 唯一身份 | 1 | 眼科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=778 | 无 |
| 胡方欣 | 唯一身份 | 1 | 眼科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=779 | 无 |
| 林彦君 | 唯一身份 | 1 | 眼科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=780 | 无 |
| 梁凤鸣 | 唯一身份 | 1 | 眼科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=781 | 无 |
| 胡丹霞 | 唯一身份 | 1 | 耳鼻喉门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1143&typeid=1141&cid=1143&ksid=1141&id=617 | 无 |
| 丘友如 | 唯一身份 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=546 | 无 |
| 冷建国 | 同名待甄别 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=547 | 无 |
| 冷建国 | 同名待甄别 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=518 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=470 |
| 陈永光 | 唯一身份 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=548 | 无 |
| 谢建军 | 唯一身份 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=550 | 无 |
| 孙玉冰 | 同名待甄别 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=551 | 无 |
| 孙玉冰 | 同名待甄别 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=520 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=472 |
| 许杰红 | 同名待甄别 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=552 | 无 |
| 许杰红 | 同名待甄别 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=522 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=474 |
| 任建华 | 唯一身份 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=554 | 无 |
| 杨晓文 | 唯一身份 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=555 | 无 |
| 袁琳 | 同一人归并 | 2 | 内科、感染性疾病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=558 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1480&typeid=1472&cid=1480&ksid=1472&id=652 |
| 金小洣 | 唯一身份 | 1 | 内科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=560 | 无 |
| 邬淼林 | 同一人归并 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=521 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=473 |
| 邱联群 | 同名待甄别 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=523 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=475 |
| 邱联群 | 同名待甄别 | 1 | 风湿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=400 | 无 |
| 陈红林 | 唯一身份 | 1 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=524 | 无 |
| 陈礼锦 | 唯一身份 | 1 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=525 | 无 |
| 孔庆新 | 同一人归并 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=527 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=991&typeid=899&cid=991&ksid=899&id=516 |
| 孙俊 | 同一人归并 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=528 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=991&typeid=899&cid=991&ksid=899&id=515 |
| 宋腾菊 | 同名待甄别 | 2 | 淘金门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=529 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=997&typeid=908&cid=997&ksid=908&id=513 |
| 宋腾菊 | 同名待甄别 | 2 | 儿科、白云院区儿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=979&typeid=896&cid=979&ksid=896&id=760 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=120 |
| 张诚光 | 唯一身份 | 1 | 药学部 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=406 | 无 |
| 范宋玲 | 唯一身份 | 1 | 药学部 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=407 | 无 |
| 李文兵 | 唯一身份 | 1 | 药学部 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=408 | 无 |
| 黄晓巧 | 唯一身份 | 1 | 药学部 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=409 | 无 |
| 李庆勇 | 唯一身份 | 1 | 药学部 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=410 | 无 |
| 吴星火 | 唯一身份 | 1 | 药学部 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=411 | 无 |
| 张建军 | 唯一身份 | 1 | 药学部 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=511 | 无 |
| 李典鸿 | 唯一身份 | 1 | 急诊科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=489 | 无 |
| 江儒文 | 唯一身份 | 1 | 急诊科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=490 | 无 |
| 梁文坚 | 唯一身份 | 1 | 急诊科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=491 | 无 |
| 刘征彦 | 唯一身份 | 1 | 急诊科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=492 | 无 |
| 李继庭 | 唯一身份 | 1 | 急诊科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=493 | 无 |
| 陈垚 | 唯一身份 | 1 | 急诊科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=495 | 无 |
| 赵丽芸 | 唯一身份 | 1 | 重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=383 | 无 |
| 王同汉 | 唯一身份 | 1 | 重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=384 | 无 |
| 方统念 | 唯一身份 | 1 | 重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=385 | 无 |
| 陈海生 | 唯一身份 | 1 | 重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=386 | 无 |
| 刘秋江 | 唯一身份 | 1 | 重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=387 | 无 |
| 曹金梅 | 唯一身份 | 1 | 针灸康复门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1284&typeid=1282&cid=1284&ksid=1282&id=580 | 无 |
| 聂斌 | 唯一身份 | 1 | 针灸康复门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1284&typeid=1282&cid=1284&ksid=1282&id=647 | 无 |
| 曾科学 | 唯一身份 | 1 | 针灸康复门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1284&typeid=1282&cid=1284&ksid=1282&id=693 | 无 |
| 吴文锋 | 唯一身份 | 1 | 针灸康复门诊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1284&typeid=1282&cid=1284&ksid=1282&id=697 | 无 |
| 刘联彬 | 唯一身份 | 1 | 骨伤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1490&typeid=1488&cid=1490&ksid=1488&id=641 | 无 |
| 陈竹生 | 同名待甄别 | 1 | 骨伤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1490&typeid=1488&cid=1490&ksid=1488&id=642 | 无 |
| 陈竹生 | 同名待甄别 | 1 | 白云院区骨科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=749 | 无 |
| 夏雄智 | 同名待甄别 | 1 | 骨伤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1490&typeid=1488&cid=1490&ksid=1488&id=643 | 无 |
| 夏雄智 | 同名待甄别 | 1 | 白云院区骨科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=750 | 无 |
| 黄培红 | 同一人归并 | 2 | 心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=125 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1518&typeid=1516&cid=1518&ksid=1516&id=658 |
| 梁宏宇 | 唯一身份 | 1 | 心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1518&typeid=1516&cid=1518&ksid=1516&id=66 | 无 |
| 苏慧 | 唯一身份 | 1 | 心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=127 | 无 |
| 袁丁 | 唯一身份 | 1 | 心血管科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=308 | 无 |
| 岳丽丽 | 唯一身份 | 1 | 脑病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=404 | 无 |
| 梁迪赛 | 唯一身份 | 1 | 脑病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=583 | 无 |
| 黄年斌 | 唯一身份 | 1 | 脑病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=72 | 无 |
| 李静 | 唯一身份 | 1 | 脾胃病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=100 | 无 |
| 许书维 | 唯一身份 | 1 | 脾胃病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=215 | 无 |
| 申昌国 | 唯一身份 | 1 | 脾胃病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=399 | 无 |
| 刘蔚 | 唯一身份 | 1 | 脾胃病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=640 | 无 |
| 饶梅冰 | 唯一身份 | 1 | 脾胃病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=80 | 无 |
| 钟毅 | 唯一身份 | 1 | 脾胃病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=83 | 无 |
| 张伦 | 唯一身份 | 1 | 脾胃病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=97 | 无 |
| 范明 | 唯一身份 | 1 | 脾胃病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=99 | 无 |
| 郝小梅 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=342 | 无 |
| 赵海方 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=343 | 无 |
| 宫静 | 唯一身份 | 1 | 呼吸与危重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=657 | 无 |
| 李慧 | 同名待甄别 | 1 | 呼吸与危重症医学科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=87 | 无 |
| 李慧 | 同名待甄别 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=768 | 无 |
| 李慧 | 同名待甄别 | 1 | 白云院区骨科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=751 | 无 |
| 莫伟 | 唯一身份 | 1 | 内分泌科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=34&typeid=32&cid=34&ksid=32&id=347 | 无 |
| 佘卫吉 | 唯一身份 | 1 | 内分泌科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=34&typeid=32&cid=34&ksid=32&id=348 | 无 |
| 张念华 | 唯一身份 | 1 | 肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=285 | 无 |
| 尹建华 | 唯一身份 | 1 | 肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=321 | 无 |
| 李寿杰 | 唯一身份 | 1 | 肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=323 | 无 |
| 谢壁元 | 唯一身份 | 1 | 肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=449 | 无 |
| 吴建奇 | 唯一身份 | 1 | 肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=450 | 无 |
| 付啸峰 | 唯一身份 | 1 | 肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=452 | 无 |
| 高海利 | 唯一身份 | 1 | 肿瘤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=651 | 无 |
| 高伟 | 唯一身份 | 1 | 风湿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=402 | 无 |
| 饶晶 | 唯一身份 | 1 | 风湿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=403 | 无 |
| 贾二涛 | 唯一身份 | 1 | 风湿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=775 | 无 |
| 杨阳 | 唯一身份 | 1 | 风湿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=776 | 无 |
| 张秋林 | 唯一身份 | 1 | 肾病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=43&typeid=41&cid=43&ksid=41&id=253 | 无 |
| 雷天香 | 唯一身份 | 1 | 肾病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=43&typeid=41&cid=43&ksid=41&id=255 | 无 |
| 张奡 | 唯一身份 | 1 | 肾病科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=43&typeid=41&cid=43&ksid=41&id=256 | 无 |
| 赵冬 | 唯一身份 | 1 | 外一科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=414 | 无 |
| 林谋清 | 唯一身份 | 1 | 外一科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=417 | 无 |
| 黄正宇 | 唯一身份 | 1 | 外一科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=419 | 无 |
| 翟胜 | 唯一身份 | 1 | 外一科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=420 | 无 |
| 袁道彰 | 唯一身份 | 1 | 外一科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=774 | 无 |
| 王炜 | 唯一身份 | 1 | 外二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=257 | 无 |
| 陈晓鑫 | 唯一身份 | 1 | 外二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=432 | 无 |
| 姜开文 | 唯一身份 | 1 | 外二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=434 | 无 |
| 张隆鑫 | 唯一身份 | 1 | 外二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=654 | 无 |
| 于锋 | 唯一身份 | 1 | 外二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=79 | 无 |
| 刘文刚 | 唯一身份 | 1 | 骨伤一科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=118 | 无 |
| 魏凌峰 | 唯一身份 | 1 | 骨伤一科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=223 | 无 |
| 赵传喜 | 唯一身份 | 1 | 骨伤一科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=224 | 无 |
| 刘欣 | 唯一身份 | 1 | 骨伤一科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=309 | 无 |
| 董旻 | 唯一身份 | 1 | 骨伤二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=105 | 无 |
| 张兵 | 唯一身份 | 1 | 骨伤二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=219 | 无 |
| 郑轩 | 唯一身份 | 1 | 骨伤二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=220 | 无 |
| 邱剑鸣 | 唯一身份 | 1 | 骨伤二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=225 | 无 |
| 董云鹏 | 唯一身份 | 1 | 骨伤二科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=405 | 无 |
| 吴少鹏 | 唯一身份 | 1 | 骨伤三科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=110 | 无 |
| 李参天 | 唯一身份 | 1 | 骨伤三科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=221 | 无 |
| 邓崇礼 | 唯一身份 | 1 | 骨伤三科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=226 | 无 |
| 张宇 | 唯一身份 | 1 | 骨伤三科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=283 | 无 |
| 梁灿德 | 唯一身份 | 1 | 骨伤三科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=284 | 无 |
| 张玉蓉 | 同名待甄别 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=106 | 无 |
| 张玉蓉 | 同名待甄别 | 1 | 白云院区妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=976&typeid=895&cid=976&ksid=895&id=755 | 无 |
| 徐莉 | 唯一身份 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=107 | 无 |
| 陈小平 | 唯一身份 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=112 | 无 |
| 纪珮 | 唯一身份 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=134 | 无 |
| 徐丹 | 唯一身份 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=135 | 无 |
| 陈靓芬 | 唯一身份 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=136 | 无 |
| 郭涛 | 唯一身份 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=205 | 无 |
| 王慧 | 同名待甄别 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=298 | 无 |
| 王慧 | 同名待甄别 | 1 | 白云院区妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=976&typeid=895&cid=976&ksid=895&id=756 | 无 |
| 刘婷 | 唯一身份 | 1 | 妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=391 | 无 |
| 李雪真 | 唯一身份 | 1 | 乳腺科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=155 | 无 |
| 黄映飞 | 唯一身份 | 1 | 乳腺科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=156 | 无 |
| 梁喆盈 | 唯一身份 | 1 | 乳腺科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=157 | 无 |
| 付亚斐 | 唯一身份 | 1 | 乳腺科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=370 | 无 |
| 黄向阳 | 唯一身份 | 1 | 肛肠科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=68&typeid=66&cid=68&ksid=66&id=393 | 无 |
| 徐琛 | 唯一身份 | 1 | 肛肠科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=68&typeid=66&cid=68&ksid=66&id=394 | 无 |
| 周永霞 | 唯一身份 | 1 | 儿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=109 | 无 |
| 叶艳芬 | 唯一身份 | 1 | 儿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=119 | 无 |
| 罗凛 | 唯一身份 | 1 | 推拿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=75&typeid=73&cid=75&ksid=73&id=423 | 无 |
| 郑林标 | 唯一身份 | 1 | 推拿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=75&typeid=73&cid=75&ksid=73&id=424 | 无 |
| 朱光 | 唯一身份 | 1 | 推拿科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=75&typeid=73&cid=75&ksid=73&id=425 | 无 |
| 朱铭华 | 唯一身份 | 1 | 皮肤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=84&typeid=82&cid=84&ksid=82&id=150 | 无 |
| 骆伟雄 | 唯一身份 | 1 | 皮肤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=84&typeid=82&cid=84&ksid=82&id=151 | 无 |
| 龚五洲 | 唯一身份 | 1 | 皮肤科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=84&typeid=82&cid=84&ksid=82&id=153 | 无 |
| 黄凡 | 唯一身份 | 1 | 针灸康复一区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=88&typeid=86&cid=88&ksid=86&id=304 | 无 |
| 陆彦青 | 唯一身份 | 1 | 针灸康复一区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=88&typeid=86&cid=88&ksid=86&id=562 | 无 |
| 杨海涛 | 唯一身份 | 1 | 针灸康复一区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=88&typeid=86&cid=88&ksid=86&id=563 | 无 |
| 谭俊青 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=288 | 无 |
| 李蔼文 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=359 | 无 |
| 王康椿 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=361 | 无 |
| 黄双旺 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=362 | 无 |
| 刘启波 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=363 | 无 |
| 邓丽梅 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=365 | 无 |
| 李冉 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=389 | 无 |
| 李前宁 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=766 | 无 |
| 何宇巍 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=767 | 无 |
| 邓超 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=769 | 无 |
| 黎翠翠 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=770 | 无 |
| 梅闯闯 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=771 | 无 |
| 卢建伟 | 唯一身份 | 1 | 检验科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=772 | 无 |
| 冯宁娜 | 唯一身份 | 1 | 医技科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=443 | 无 |
| 陈伟萍 | 唯一身份 | 1 | 医技科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=444 | 无 |
| 邓敏君 | 唯一身份 | 1 | 医技科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=445 | 无 |
| 陈乐 | 唯一身份 | 1 | 医技科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=446 | 无 |
| 赖媛媛 | 唯一身份 | 1 | 医技科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=447 | 无 |
| 梁虹宇 | 唯一身份 | 1 | 医技科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=448 | 无 |
| 孟睿 | 唯一身份 | 1 | 医技科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=453 | 无 |
| 董明 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=497 | 无 |
| 黄承武 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=498 | 无 |
| 陈海城 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=499 | 无 |
| 马连东 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=500 | 无 |
| 魏国辉 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=501 | 无 |
| 邱俊杰 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=502 | 无 |
| 李雪芳 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=503 | 无 |
| 代树程 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=504 | 无 |
| 沈鸿 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=505 | 无 |
| 邓秀珍 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=507 | 无 |
| 林立军 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=508 | 无 |
| 李琎 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=509 | 无 |
| 王蓉 | 唯一身份 | 1 | 康复治疗中心 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=510 | 无 |
| 张庆元 | 唯一身份 | 1 | 口腔科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=138 | 无 |
| 温映萍 | 唯一身份 | 1 | 口腔科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=143 | 无 |
| 苏淑娟 | 唯一身份 | 1 | 口腔科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=144 | 无 |
| 陈倩倩 | 唯一身份 | 1 | 口腔科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=145 | 无 |
| 鲁洁 | 唯一身份 | 1 | 口腔科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=146 | 无 |
| 张雯 | 唯一身份 | 1 | 口腔科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=273 | 无 |
| 刘建 | 唯一身份 | 1 | 针灸康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=300 | 无 |
| 苏美意 | 唯一身份 | 1 | 针灸康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=646 | 无 |
| 陈敬伟 | 唯一身份 | 1 | 针灸康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=648 | 无 |
| 张炎明 | 唯一身份 | 1 | 针灸康复五区 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=649 | 无 |
| 张嘉良 | 唯一身份 | 1 | 白云院区骨科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=752 | 无 |
| 江艺 | 唯一身份 | 1 | 白云院区骨科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=753 | 无 |
| 张瑜 | 唯一身份 | 1 | 白云院区骨科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=754 | 无 |
| 杨宇航 | 唯一身份 | 1 | 白云院区妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=976&typeid=895&cid=976&ksid=895&id=757 | 无 |
| 柯婵 | 唯一身份 | 1 | 白云院区妇科 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=976&typeid=895&cid=976&ksid=895&id=758 | 无 |

## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| 无 | 无 | 无 | 无 |

## 输出文件

- Excel 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx`
- CSV 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 2 |
| 原始医生卡片记录 | 367 |
| 跨入口去重前候选关系 | 367 |
| 跨入口去重后唯一候选 | 367 |
| 排除非医生候选 | 0 |
| 唯一医生详情页 | 342 |
| 覆盖科室数 | 65 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 36 |
| 慢性病 | 122 |
| 术后恢复/康复 | 100 |
| 生殖疾病 | 37 |
| 疑难重症 | 82 |
| 肿瘤 | 48 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 特诊室 | 17 |
| 白云院区传统疗法区 | 15 |
| 白云院区康复治疗区 | 15 |
| 康复治疗中心 | 14 |
| 检验科 | 14 |
| 淘金门诊 | 13 |
| 内科 | 11 |
| 妇科 | 11 |
| 肿瘤科 | 10 |
| 心血管科 | 9 |
| 脾胃病科 | 9 |
| 眼科 | 8 |
| 医技科 | 7 |
| 治未病(健康体检)中心 | 7 |
| 药学部 | 7 |
| 乳腺科 | 6 |
| 五山门诊 | 6 |
| 急诊科 | 6 |
| 白云院区针康复五区 | 6 |
| 白云院区骨科 | 6 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 科室需人工复核 | 9 |
| 同名待甄别 | 89 |
| 多详情职称不一致 | 12 |
| 职称/身份需人工复核 | 48 |

## 列表页读取异常

| 页码 | URL | 错误 |
|---|---|---|
| 无 | 无 | 无 |

## 详情页读取异常

| 来源链接 | 错误 |
|---|---|
| 无 | 无 |

## 人工复核建议

1. 优先复核“异常提示”不为空的医生。
2. “亮眼经历线索”只作为官方证据线索，不直接改写为对外宣传语。
3. 官网没有展示的擅长、经历、疾病标签保持空白，不补造。
4. 标记为试采门禁的适配器必须先完成小样本复核；只有取得 Claude 明确通过指令后才可全量追加。

## 合规边界

- 仅使用医院官网公开网页。
- 不采集私人电话、私人微信、家庭住址、患者隐私或非公开排班信息。
- 不使用第三方医疗平台评价、排名、患者评论。
- 不写“保证治愈”“包治疑难杂症”“疗效第一”等无法由官网证明的表达。
