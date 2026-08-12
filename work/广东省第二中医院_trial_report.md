---
类型: 自动采集试跑报告
医院: 广东省第二中医院
城市: 广州市
采集日期: 2026-08-12
来源范围: 医院官网
采集入口: https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850 https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850
适配器: gdzy5413_official_specialist
---

# 广东省第二中医院 官方医生自动采集试跑报告

## 结论

本次试跑只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集试采底表，共 10 位唯一医生；官网列表页原始卡片记录 21 条；识别到官网列表分页 2 页；覆盖 5 个科室；详情页失败 0 条。

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
| 名医名家 | https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850 | 医院官网名医名家单页名单 | 1 | 37 | 21 | 0 | 广东省第二中医院（官网名医名家栏目） | 两块牌子为同一实体；未发现分院区归属 |
| 各科专家 | https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 医院官网各科专家页（发现另一详情模板但不在本 Issue 授权范围） | 1 | 0 | 0 | 346 | 广东省第二中医院（官网各科专家栏目） | 两块牌子为同一实体；未发现分院区归属 |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：21
- 跨入口去重后唯一候选：21
- 跨入口重复关系：0
- 试采覆盖入口分类：1 个（名医名家）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 无 | 无 | 无 |

## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王清海 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=47 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 靳利利 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=36 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄培红 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=125 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 袁丁 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=308 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 苏 慧 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=127 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李桂明 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=317 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李德军 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=22&typeid=20&cid=22&ksid=20&id=318 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 岳丽丽 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=404 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 高敏 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=319 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄年斌 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=72 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 周嘉澄 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=582 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梁迪赛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=25&typeid=23&cid=25&ksid=23&id=583 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李 静 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=100 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 许书维 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=215 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 申昌国 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=399 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 范 明 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=99 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 戈焰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=68 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 饶梅冰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=80 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘蔚 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=640 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 钟 毅 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=83 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张 伦 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=28&typeid=26&cid=28&ksid=26&id=97 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 赵海方 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=343 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 宫静 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=657 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈宁 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=341 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李慧 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=87 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郝小梅 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=342 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 汪何 汪何 莫伟 吕雄 佘卫吉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=34&typeid=32&cid=34&ksid=32&id=346 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 莫伟 汪何 莫伟 吕雄 佘卫吉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=34&typeid=32&cid=34&ksid=32&id=347 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吕雄 汪何 莫伟 吕雄 佘卫吉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=34&typeid=32&cid=34&ksid=32&id=345 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 佘卫吉 汪何 莫伟 吕雄 佘卫吉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=34&typeid=32&cid=34&ksid=32&id=348 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈高峰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=281 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 史清华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=282 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张念华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=285 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 高海利 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=651 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 武如通 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=322 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吴建奇 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=450 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 尹建华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=321 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李寿杰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=323 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 付啸峰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=452 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黎智燊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=696 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 谢壁元 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=449 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 贾二涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=775 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杨阳 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=776 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邱联群 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=400 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 高伟 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=402 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 饶晶 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=40&typeid=38&cid=40&ksid=38&id=403 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 雷天香 雷天香 张奡 张秋林 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=43&typeid=41&cid=43&ksid=41&id=255 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张奡 雷天香 张奡 张秋林 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=43&typeid=41&cid=43&ksid=41&id=256 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张秋林 雷天香 张奡 张秋林 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=43&typeid=41&cid=43&ksid=41&id=253 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘征彦 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=492 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李继庭 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=493 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈 垚 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=495 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李典鸿 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=489 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 江儒文 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=490 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梁文坚 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1274&typeid=1272&cid=1274&ksid=1272&id=491 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 方统念 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=385 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈海生 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=386 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘秋江 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=387 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 赵丽芸 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=383 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王同汉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1279&typeid=1277&cid=1279&ksid=1277&id=384 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄培红 黄培红 梁宏宇 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1518&typeid=1516&cid=1518&ksid=1516&id=658 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梁宏宇 黄培红 梁宏宇 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1518&typeid=1516&cid=1518&ksid=1516&id=66 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 赵冬 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=414 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林谋清 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=417 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄正宇 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=419 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 翟胜 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=420 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 袁道彰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=774 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈晓鑫 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=432 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 姜开文 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=434 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张隆鑫 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=654 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 于 锋 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=79 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王炜 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=50&typeid=48&cid=50&ksid=48&id=257 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 许学猛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=60 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘文刚 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=118 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 魏凌峰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=223 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 赵传喜 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=224 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘欣 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=53&typeid=51&cid=53&ksid=51&id=309 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吕朝晖 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=103 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 董 旻 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=105 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张兵 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=219 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郑轩 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=220 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邱剑鸣 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=225 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 董云鹏 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=56&typeid=54&cid=56&ksid=54&id=405 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吴少鹏 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=110 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李参天 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=221 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邓崇礼 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=226 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张宇 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=283 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梁灿德 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=284 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 许学猛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=59&typeid=57&cid=59&ksid=57&id=398 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 徐莉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=107 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 纪珮 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=134 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郭涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=205 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王慧 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=298 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 谢波 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=390 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘婷 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=391 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 徐丹 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=135 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈靓芬 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=136 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈小平 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=112 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张玉蓉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=62&typeid=60&cid=62&ksid=60&id=106 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郭智涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=154 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李雪真 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=155 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄映飞 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=156 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梁喆盈 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=157 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 付亚斐 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=65&typeid=63&cid=65&ksid=63&id=370 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄向阳 黄向阳 徐琛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=68&typeid=66&cid=68&ksid=66&id=393 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 徐琛 黄向阳 徐琛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=68&typeid=66&cid=68&ksid=66&id=394 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 周永霞 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=109 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 叶艳芬 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=119 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 宋腾菊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=120 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林晓洁 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=163 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 余德钊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=286 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈可静 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=287 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 罗凛 罗凛 郑林标 朱光 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=75&typeid=73&cid=75&ksid=73&id=423 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郑林标 罗凛 郑林标 朱光 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=75&typeid=73&cid=75&ksid=73&id=424 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 朱光 罗凛 郑林标 朱光 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=75&typeid=73&cid=75&ksid=73&id=425 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张庆元 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=138 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 温映萍 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=143 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 苏淑娟 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=144 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈倩倩 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=145 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 鲁 洁 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=146 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张雯 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=958&typeid=76&cid=958&ksid=76&id=273 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 朱铭华 朱铭华 骆伟雄 龚五洲 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=84&typeid=82&cid=84&ksid=82&id=150 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 骆伟雄 朱铭华 骆伟雄 龚五洲 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=84&typeid=82&cid=84&ksid=82&id=151 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 龚五洲 朱铭华 骆伟雄 龚五洲 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=84&typeid=82&cid=84&ksid=82&id=153 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 曹金梅 曹金梅 聂 斌 曾科学 吴文锋 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1284&typeid=1282&cid=1284&ksid=1282&id=580 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 聂 斌 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1284&typeid=1282&cid=1284&ksid=1282&id=647 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 曾科学 曹金梅 聂 斌 曾科学 吴文锋 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1284&typeid=1282&cid=1284&ksid=1282&id=693 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吴文锋 曹金梅 聂 斌 曾科学 吴文锋 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1284&typeid=1282&cid=1284&ksid=1282&id=697 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邱健行 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=596 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 卢桂梅 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=597 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王清海 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=598 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 许学猛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=599 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 汪何 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=600 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杨思华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=601 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吕雄 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=602 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 戈 焰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=603 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 谢波 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=604 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 余德钊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=605 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李爱华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=606 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄琳 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=607 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈可静 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=608 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈高峰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=609 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈宁 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=610 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 高敏 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=611 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 靳利利 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=612 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吕朝晖 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=613 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郭智涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=614 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 范德辉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1464&typeid=1462&cid=1464&ksid=1462&id=615 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 魏东 魏东 袁琳 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1480&typeid=1472&cid=1480&ksid=1472&id=644 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 袁琳 魏东 袁琳 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1480&typeid=1472&cid=1480&ksid=1472&id=652 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘联彬 刘联彬 陈竹生 夏雄智 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1490&typeid=1488&cid=1490&ksid=1488&id=641 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈竹生 刘联彬 陈竹生 夏雄智 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1490&typeid=1488&cid=1490&ksid=1488&id=642 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 夏雄智 刘联彬 陈竹生 夏雄智 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1490&typeid=1488&cid=1490&ksid=1488&id=643 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 唐敏 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=314 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王霜玲 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=315 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 彭明欢 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=653 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王 燕 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=777 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李嘉愔 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=778 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 胡方欣 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=779 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林彦君 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=780 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梁凤鸣 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=781 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 胡丹霞 耳鼻喉门诊 胡丹霞 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1143&typeid=1141&cid=1143&ksid=1141&id=617 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 丘友如 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=546 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 冷建国 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=547 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈永光 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=548 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄琳 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=549 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 谢建军 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=550 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 孙玉冰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=551 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 许杰红 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=552 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李桂明 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=553 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 任建华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=554 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杨晓文 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=555 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 袁琳 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=558 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 金小洣 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1151&typeid=1149&cid=1151&ksid=1149&id=560 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘 悦 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=496 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 董 明 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=497 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄承武 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=498 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈海城 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=499 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 马连东 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=500 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 魏国辉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=501 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邱俊杰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=502 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李雪芳 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=503 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 代树程 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=504 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 沈 鸿 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=505 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林雪珊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=506 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邓秀珍 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=507 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林立军 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=508 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李 琎 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=509 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王 蓉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=957&typeid=955&cid=957&ksid=955&id=510 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄凡 黄凡 陆彦青 杨海涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=88&typeid=86&cid=88&ksid=86&id=304 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陆彦青 黄凡 陆彦青 杨海涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=88&typeid=86&cid=88&ksid=86&id=562 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杨海涛 黄凡 陆彦青 杨海涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=88&typeid=86&cid=88&ksid=86&id=563 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘 建 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=300 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 苏美意 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=646 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈敬伟 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=648 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张炎明 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=649 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 范德辉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=97&typeid=95&cid=97&ksid=95&id=299 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张俊杰 张俊杰 刘星 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=100&typeid=98&cid=100&ksid=98&id=428 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘星 张俊杰 刘星 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=100&typeid=98&cid=100&ksid=98&id=429 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林晓洁 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=482 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 周盛杰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=650 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郑洁莉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=483 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 孙正平 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=488 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杨美芝 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=484 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 钟文鑫 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=487 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梁兆凤 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=486 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李有武 麻醉科 李有武 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=110&typeid=108&cid=110&ksid=108&id=158 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 谭俊青 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=288 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李慧 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=768 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邓超 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=769 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黎翠翠 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=770 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梅闯闯 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=771 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 卢建伟 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=772 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘启波 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=363 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李前宁 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=766 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李冉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=389 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李蔼文 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=359 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邓丽梅 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=365 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王康椿 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=361 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄双旺 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=362 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 何宇巍 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=767 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 冯宁娜 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=443 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈伟萍 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=444 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邓敏君 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=445 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈乐 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=446 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 赖媛媛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=447 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梁虹宇 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=448 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 孟睿 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=453 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张诚光 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=406 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 范宋玲 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=407 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李文兵 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=408 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄晓巧 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=409 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李庆勇 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=410 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吴星火 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=411 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张建军 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1248&typeid=886&cid=1248&ksid=886&id=511 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈竹生 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=749 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 夏雄智 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=750 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李慧 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=751 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张嘉良 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=752 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 江艺 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=753 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张瑜 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=970&typeid=892&cid=970&ksid=892&id=754 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张玉蓉 张玉蓉 王慧 杨宇航 柯婵 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=976&typeid=895&cid=976&ksid=895&id=755 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王慧 张玉蓉 王慧 杨宇航 柯婵 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=976&typeid=895&cid=976&ksid=895&id=756 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杨宇航 张玉蓉 王慧 杨宇航 柯婵 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=976&typeid=895&cid=976&ksid=895&id=757 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 柯婵 张玉蓉 王慧 杨宇航 柯婵 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=976&typeid=895&cid=976&ksid=895&id=758 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 余德钊 余德钊 宋腾菊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=979&typeid=896&cid=979&ksid=896&id=430 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 宋腾菊 余德钊 宋腾菊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=979&typeid=896&cid=979&ksid=896&id=760 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 徐云英 白云院区皮肤科 徐云英 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1078&typeid=1076&cid=1078&ksid=1076&id=371 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黄晓萍 白云院区耳鼻喉科 黄晓萍 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1082&typeid=1080&cid=1082&ksid=1080&id=773 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 胡想国 白云院区口腔科 胡想国 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1086&typeid=1084&cid=1086&ksid=1084&id=375 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李桂明 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=718 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李德军 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=719 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 肖根发 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=720 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李国彬 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=721 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 廖坤莹 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1090&typeid=1088&cid=1090&ksid=1088&id=765 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 周嘉澄 周嘉澄 彭玉 郭红 蔡艺贞 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1094&typeid=1092&cid=1094&ksid=1092&id=714 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 彭玉 周嘉澄 彭玉 郭红 蔡艺贞 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1094&typeid=1092&cid=1094&ksid=1092&id=715 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郭红 周嘉澄 彭玉 郭红 蔡艺贞 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1094&typeid=1092&cid=1094&ksid=1092&id=716 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 蔡艺贞 周嘉澄 彭玉 郭红 蔡艺贞 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1094&typeid=1092&cid=1094&ksid=1092&id=717 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 黎智燊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=695 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈高峰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=706 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 史清华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=707 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 武如通 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=708 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 周伶 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=709 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吕丽琼 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1098&typeid=1096&cid=1098&ksid=1096&id=710 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 徐凯 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=350 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 高海燕 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=351 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 叶恒 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=698 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 秦小红 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=699 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杜家津 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1102&typeid=1100&cid=1102&ksid=1100&id=700 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 周杰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=352 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张振宁 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=656 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 袁智先 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=701 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邸富荣 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=702 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邓间开 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1106&typeid=1104&cid=1106&ksid=1104&id=703 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林妙君 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=704 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 马洪举 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=705 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张晓燕 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=722 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 凌翠敏 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=723 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘文丽 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=724 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李婷 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1110&typeid=1108&cid=1110&ksid=1108&id=759 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘悦 刘悦 何桥景 贺青涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1114&typeid=1112&cid=1114&ksid=1112&id=587 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 何桥景 刘悦 何桥景 贺青涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1114&typeid=1112&cid=1114&ksid=1112&id=588 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 贺青涛 刘悦 何桥景 贺青涛 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1114&typeid=1112&cid=1114&ksid=1112&id=586 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林湖广 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=733 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘莉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=734 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 谢秋平 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=735 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杨淑荃 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=736 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王朋莉 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=737 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈小燕 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=738 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李翠香 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=739 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 官华良 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=740 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 张勤锐 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=741 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林楚钊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=742 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 冯小芹 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=743 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郑钦毫 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=744 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王传鑫 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=745 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 彭震峰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=746 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘仁金 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1118&typeid=1116&cid=1118&ksid=1116&id=747 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杨栋 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=567 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈志勇 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=570 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 朱冬娇 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=571 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 何国建 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=573 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 吴振中 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=574 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 梁韵妮 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=575 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 庄婷婷 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=577 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 高辰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=725 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 林雪珊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=726 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 杨宇愿 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=727 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈博 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=728 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈云生 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=729 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 郑恭鹏 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=730 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 王子鸣 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=731 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邱俊芸 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1122&typeid=1120&cid=1122&ksid=1120&id=732 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 冷建国 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=470 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 靳利利 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=471 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 孙玉冰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=472 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邬淼林 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=473 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 许杰红 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=474 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邱联群 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=985&typeid=897&cid=985&ksid=897&id=475 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 周亦农 淘金门诊皮肤科 周亦农 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=988&typeid=898&cid=988&ksid=898&id=514 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 孙俊 孙俊 孔庆新 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=991&typeid=899&cid=991&ksid=899&id=515 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 孔庆新 孙俊 孔庆新 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=991&typeid=899&cid=991&ksid=899&id=516 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 宋腾菊 淘金门诊儿科 宋腾菊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=997&typeid=908&cid=997&ksid=908&id=513 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 蔡荣华 淘金门诊按摩科 蔡荣华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1000&typeid=909&cid=1000&ksid=909&id=512 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 周亦农 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=517 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 冷建国 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=518 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 靳利利 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=519 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 孙玉冰 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=520 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邬淼林 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=521 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 许杰红 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=522 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 邱联群 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=523 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈红林 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=524 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 陈礼锦 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=525 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 蔡荣华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=526 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 孔庆新 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=527 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 孙俊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=528 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 宋腾菊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1229&typeid=1227&cid=1229&ksid=1227&id=529 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 蔡妙珊 蔡妙珊 沈越 魏东 刘晓俊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1003&typeid=901&cid=1003&ksid=901&id=436 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 沈越 蔡妙珊 沈越 魏东 刘晓俊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1003&typeid=901&cid=1003&ksid=901&id=437 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 魏东 蔡妙珊 沈越 魏东 刘晓俊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1003&typeid=901&cid=1003&ksid=901&id=438 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 刘晓俊 蔡妙珊 沈越 魏东 刘晓俊 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1003&typeid=901&cid=1003&ksid=901&id=439 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 周亦农 五山门诊皮肤科 周亦农 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1006&typeid=902&cid=1006&ksid=902&id=435 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 劳宗洪 劳宗洪 元国华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1009&typeid=903&cid=1009&ksid=903&id=441 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 元国华 劳宗洪 元国华 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1009&typeid=903&cid=1009&ksid=903&id=442 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |
| https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=852&pid=850 | 李宝国 五山门诊针灸康复科 李宝国 | https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1012&typeid=904&cid=1012&ksid=904&id=440 | Issue #17 仅授权 specialist.aspx?typeid=<数字>；另一详情模板只计范围证据，不请求采集 |

## 输出文件

- Excel 底表：未生成（本轮使用 --no-xlsx）
- CSV 底表：`D:\workspace\信息收集整理\work\广东省第二中医院_trial_doctors.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 官网列表分页数 | 2 |
| 原始医生卡片记录 | 21 |
| 跨入口去重前候选关系 | 21 |
| 跨入口去重后唯一候选 | 21 |
| 排除非医生候选 | 0 |
| 唯一医生详情页 | 10 |
| 覆盖科室数 | 5 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 2 |
| 慢性病 | 5 |
| 术后恢复/康复 | 1 |
| 生殖疾病 | 1 |
| 疑难重症 | 6 |
| 肿瘤 | 2 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 乳腺科 | 1 |
| 呼吸科 | 1 |
| 妇科 | 1 |
| 心血管科 | 1 |
| 针灸康复科五区 | 1 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 科室需人工复核 | 5 |

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
