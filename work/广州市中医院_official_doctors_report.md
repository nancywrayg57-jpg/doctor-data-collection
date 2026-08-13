---
类型: 全量采集归并审计报告
医院: 广州市中医院
城市: 广州市
采集日期: 2026-08-13
来源范围: 医院官网
采集入口: https://www.gzszyy.com/expert/
适配器: gzszyy_department_expert_directory
---

# 广州市中医院 官方医生全量采集归并审计报告

## 结论

本次全量采集只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集全量采集底表，共 415 位唯一医生；官网列表页原始卡片记录 434 条；读取入口分类 37 个；覆盖 36 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 广州市中医院 |
| 官网首页 | https://www.gzszyy.com/patient/ |
| 本轮医生入口 | https://www.gzszyy.com/expert/ |
| 入口来源 | GitHub Issue #33（与官网入口台账一致） |
| 原台账医生入口 | https://www.gzszyy.com/expert/ |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | A-优先自动采集 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
| 官网顶层全院专家目录 | https://www.gzszyy.com/expert/ | 医院官网名医名家未筛选目录；用于校验全院详情 ID 覆盖 | 18 | 423 | 423 | 0 | 广州市中医院 | 同域公开目录；与 dp 科室树逐 ID 对账 |
| 官网 dp 科室专家树 | https://www.gzszyy.com/expert/ | 医院官网名医名家目录；dp 科室筛选为全院普查入口 | 37 | 433 | 422 | 5 | 广州市中医院 | 同域单一医院；首页院区/门诊部与详情二维码标签独立留痕 |

### 动态目录专项证据

- 医生分页/载入方式：顶层全院目录 18 页校验身份覆盖；35 个 dp 科室筛选入口共 37 页提供科室关系；pr/le 仅为职称/级别筛选证据
- 医生目录公开接口：不适用
- 医生详情公开接口：不适用
- 接口出处证据：不适用
- 院区/分组：5 个；科室分类：35 个
- 医生-科室关系：434 条
- 唯一详情 ID：423 个
- 有姓名详情 ID：423 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：419 个
- 同名不同详情 ID：4 组
- 非空/空科室块：422 / 1
- 院区/出诊点标签关系：珠玑路院区 228 条；同德围分院 137 条；同德综合门诊部 122 条；五羊门诊部 28 条
- 跨院区/出诊点详情 ID：160 个

| 同名 | 详情 ID |
|---|---|
| 林少贞 | ELe31Mb6,JxboyNeg |
| 唐瑾秋 | 4QbYVOdz,X7ax9byv |
| 王健 | 3YaOggax,WZdP6yaK |
| 高三德 | LDdwkmd1,QBeXY8ay |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：434
- 跨入口去重后唯一候选：423
- 跨入口重复关系：11
- 试采覆盖入口分类：36 个（五羊门诊部、体检科、儿科、内分泌科、医学影像科、口腔科、同德综合门诊部、名医堂、外科、妇科、心病科（心血管内科）、急诊科、普通内科、杂病门诊、检验病理科、治未病科、皮肤科、眼科、睡眠心理科、耳鼻喉科、肛肠科、肺病科（呼吸内科）、肾病科、肿瘤一区、肿瘤二区、脉管炎科、脑病科（神经内科）、脾胃科（消化内科）、药学部、血液科、超声医学科、重症医学科、针灸康复科、针灸科、骨伤科、麻醉科）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 叶穗林 | https://www.gzszyy.com/expert/2026/w9aADOev.html | 名医堂；心病科（心血管内科） |
| 蔡迎峰 | https://www.gzszyy.com/expert/2026/X7axvrdy.html | 名医堂；骨伤科 |
| 李丽霞 | https://www.gzszyy.com/expert/2026/KQe1wRbJ.html | 名医堂；针灸科 |
| 赵云燕 | https://www.gzszyy.com/expert/2026/46dBgJe7.html | 名医堂；重症医学科 |
| 叶绍伟 | https://www.gzszyy.com/expert/2026/9wdLwbjP.html | 名医堂；脑病科（神经内科） |
| 吕永慧 | https://www.gzszyy.com/expert/2026/WPe9xdLy.html | 名医堂；脾胃科（消化内科） |
| 梁劲军 | https://www.gzszyy.com/expert/2026/4zbq7rep.html | 名医堂；肛肠科 |
| 黄金兰 | https://www.gzszyy.com/expert/2026/8mepzrbM.html | 肿瘤二区；血液科 |
| 许幸仪 | https://www.gzszyy.com/expert/2026/WZdPwbKg.html | 脑病科（神经内科）；体检科 |
| 高三德 | https://www.gzszyy.com/expert/2026/LDdwkmd1.html | 治未病科；普通内科、杂病门诊 |
| 赵明昂 | https://www.gzszyy.com/expert/2026/J0dNYLbL.html | 针灸康复科；同德综合门诊部 |

## 广州市中医院院区/出诊点证据

- 顶层全院目录 / dp 科室树：18 页、423 ID / 37 页、422 ID
- 顶层目录专属详情：1 个（lNbWW4by）；dp 树专属详情：0 个
- 筛选链接：dp 35 个（科室）、pr 18 个（职称）、le 3 个（专家级别）；pr/le 不重复采集
- 纯护理排除后合规候选：418 个
- 最终身份：415；同一人归并 3 组；实质不同同名 1 组 / 2 行
- 官网公开院区/门诊部范围：5 个
- 试采详情：418 个；有二维码院区/出诊点标签 289 个；未标注 129 个
- 多院区/出诊点标签详情：160 个
- 详情标签计数：珠玑路院区 228 条；同德围分院 137 条；同德综合门诊部 122 条；五羊门诊部 28 条
- 字段处理：详情页明确标签与列表卡片科室共同保留在 `科室_列表卡片`；不推断院区与科室之间未由官网明示的组合关系。

| 官网公开院区/门诊部 | 官方链接 |
|---|---|
| 珠玑院区 | https://www.gzszyy.com/district1_zzlyq/ |
| 天河新院区 | https://www.gzszyy.com/district1_thxyq/ |
| 同德院区 | https://www.gzszyy.com/district1_tdfy/ |
| 五羊门诊部 | https://www.gzszyy.com/district1_wymzb/ |
| 同德门诊部 | https://www.gzszyy.com/district1_tdmzb/ |

| 姓名 | 详情 ID | 科室归属 | 详情二维码院区/出诊点 | 来源链接 |
|---|---|---|---|---|
| 叶穗林 | w9aADOev | 名医堂、心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/w9aADOev.html |
| 蔡迎峰 | X7axvrdy | 名医堂、骨伤科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/X7axvrdy.html |
| 李丽霞 | KQe1wRbJ | 名医堂、针灸科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/KQe1wRbJ.html |
| 赵云燕 | 46dBgJe7 | 名医堂、重症医学科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/46dBgJe7.html |
| 罗永佳 | nXe0LGex | 名医堂 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/nXe0LGex.html |
| 祝维峰 | oQeZ6Jep | 名医堂 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/oQeZ6Jep.html |
| 徐雯 | pmbk7Ybz | 名医堂 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/pmbk7Ybz.html |
| 叶绍伟 | 9wdLwbjP | 名医堂、脑病科（神经内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/9wdLwbjP.html |
| 吕永慧 | WPe9xdLy | 名医堂、脾胃科（消化内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/WPe9xdLy.html |
| 梁劲军 | 4zbq7rep | 名医堂、肛肠科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4zbq7rep.html |
| 梁慕筠 | oQeZ0Ebp | 名医堂 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/oQeZ0Ebp.html |
| 吴薏婷 | 4zbqjrdp | 肿瘤一区 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4zbqjrdp.html |
| 李金昌 | MYer06bO | 肿瘤一区 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/MYer06bO.html |
| 梁洪江 | l9avgrbG | 肿瘤一区 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/l9avgrbG.html |
| 刘平庄 | LDdwjwb1 | 肿瘤一区 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/LDdwjwb1.html |
| 罗溢昌 | X7axGrey | 肿瘤一区 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/X7axGrey.html |
| 樊杜英 | zPdy8WbQ | 肿瘤一区 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/zPdy8WbQ.html |
| 吴彬 | xkazm8eJ | 肿瘤一区 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/xkazm8eJ.html |
| 林家祎 | w9aA87ev | 肿瘤一区 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/w9aA87ev.html |
| 崔萌萌 | YRdGYraD | 肿瘤一区 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/YRdGYraD.html |
| 邓力 | olej25ej | 肿瘤二区 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/olej25ej.html |
| 陈庆强 | pmbk5Xez | 肿瘤二区 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/pmbk5Xez.html |
| 吴锦燕 | Mvbmw0eY | 肿瘤二区 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/Mvbmw0eY.html |
| 梁艳菊 | openZle7 | 肿瘤二区 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/openZle7.html |
| 唐阳 | GRb490dB | 肿瘤二区 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/GRb490dB.html |
| 林少贞 | JxboyNeg | 针灸科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/JxboyNeg.html |
| 陈楚云 | 5xe73je7 | 针灸科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/5xe73je7.html |
| 王兴 | Vyb82mev | 针灸科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/Vyb82mev.html |
| 吴涓 | K9b68neE | 针灸科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/K9b68neE.html |
| 张去飞 | olej2Rej | 针灸科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/olej2Rej.html |
| 谢丽琴 | MvbmwOeY | 针灸科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/MvbmwOeY.html |
| 黄文盖 | JxboYjeg | 针灸科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/JxboYjeg.html |
| 赵奕 | openZRe7 | 针灸科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/openZRe7.html |
| 卢立宏 | pnelO5dK | 针灸科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/pnelO5dK.html |
| 刘文文 | 4zbqj2dp | 针灸科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4zbqj2dp.html |
| 卢翠娜 | MYer0EbO | 针灸科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/MYer0EbO.html |
| 陈琼茹 | jneg56bw | 针灸科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/jneg56bw.html |
| 王成银 | J0dN6dLO | 脑病科（神经内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/J0dN6dLO.html |
| 黄坚红 | N1aMAaWm | 脑病科（神经内科） | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/N1aMAaWm.html |
| 许幸仪 | WZdPwbKg | 脑病科（神经内科）、体检科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/WZdPwbKg.html |
| 欧阳智 | YqaQlenj | 脑病科（神经内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/YqaQlenj.html |
| 翁旭亮 | y5eVMdEP | 脑病科（神经内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/y5eVMdEP.html |
| 吕金丹 | lNbWJayg | 脑病科（神经内科） | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/lNbWJayg.html |
| 刘青 | 4QbYKezq | 脑病科（神经内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4QbYKezq.html |
| 张汉樑 | QBeX5lay | 脑病科（神经内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/QBeX5lay.html |
| 邱铃铃 | ELe3Mb69 | 脑病科（神经内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/ELe3Mb69.html |
| 雷源 | QBeXWdyK | 脑病科（神经内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/QBeXWdyK.html |
| 黑赏艳 | 4oeEKmb0 | 脑病科（神经内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4oeEKmb0.html |
| 梁洁 | APdRqbGy | 脑病科（神经内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/APdRqbGy.html |
| 杨玲 | GRb41dBL | 脑病科（神经内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/GRb41dBL.html |
| 刘恒 | K9b6nbEv | 脑病科（神经内科） | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/K9b6nbEv.html |
| 高婷婷 | Jrb2KdWL | 脑病科（神经内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/Jrb2KdWL.html |
| 林振坤 | oQeZJepZ | 脑病科（神经内科） | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/oQeZJepZ.html |
| 陈秀慧 | 3YaOpbxq | 脑病科（神经内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/3YaOpbxq.html |
| 张艳红 | M7e5Ba2v | 脑病科（神经内科） | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/M7e5Ba2v.html |
| 王晓捷 | Vyb8mdvA | 脑病科（神经内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/Vyb8mdvA.html |
| 樊春华 | 8mepY2aM | 脾胃科（消化内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/8mepY2aM.html |
| 吴宇金 | nXe0vbxr | 脾胃科（消化内科） | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/nXe0vbxr.html |
| 古伟明 | pmbkR5az | 脾胃科（消化内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/pmbkR5az.html |
| 杨洁 | olejRRej | 脾胃科（消化内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/olejRRej.html |
| 康宜兵 | pnelY5aK | 脾胃科（消化内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/pnelY5aK.html |
| 林穗芳 | 4QbY59bz | 脾胃科（消化内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4QbY59bz.html |
| 何润明 | jnegJYdw | 脾胃科（消化内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/jnegJYdw.html |
| 杨以琳 | open5Rd7 | 脾胃科（消化内科） | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/open5Rd7.html |
| 詹原泉 | Jxbo2jag | 脾胃科（消化内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/Jxbo2jag.html |
| 陈文剑 | MvbmZOdY | 脾胃科（消化内科） | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/MvbmZOdY.html |
| 廖媛 | 4zbqx2ap | 脾胃科（消化内科） | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/4zbqx2ap.html |
| 丛龙玲 | MYerkEaO | 脾胃科（消化内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/MYerkEaO.html |
| 林志鹏 | l9av2maG | 脾胃科（消化内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/l9av2maG.html |
| 王学川 | LDdwpRe1 | 脾胃科（消化内科） | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/LDdwpRe1.html |
| 范嘉伟 | JxbovAag | 脾胃科（消化内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/JxbovAag.html |
| 胡淑文 | M7e5WZb2 | 脾胃科（消化内科） | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/M7e5WZb2.html |
| 梁依敏 | y5eVJBeE | 脾胃科（消化内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/y5eVJBeE.html |
| 李郡 | zPdyP7bQ | 脾胃科（消化内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/zPdyP7bQ.html |
| 苏子珊 | xkazpYdJ | 脾胃科（消化内科） | 同德围分院 | https://www.gzszyy.com/expert/2026/xkazpYdJ.html |
| 张健谊 | 8mepRXbM | 脾胃科（消化内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/8mepRXbM.html |
| 陈智恒 | zPdypzbQ | 脾胃科（消化内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/zPdypzbQ.html |
| 张宁怡 | 4QbYQObz | 脾胃科（消化内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4QbYQObz.html |
| 戴媺 | QBeXDWey | 血液科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/QBeXDWey.html |
| 夏思 | LDdwEma1 | 血液科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/LDdwEma1.html |
| 蒋群 | 4QbYEKbz | 血液科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4QbYEKbz.html |
| 戚淑娟 | BDbDRnel | 重症医学科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/BDbDRnel.html |
| 李莉 | 4oeElkd0 | 重症医学科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4oeElkd0.html |
| 赵鸿 | YQdJZodO | 重症医学科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/YQdJZodO.html |
| 张学宏 | y1aKOnaQ | 重症医学科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/y1aKOnaQ.html |
| 雷晓兰 | YRdGZ0bD | 重症医学科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/YRdGZ0bD.html |
| 吴宇瑶 | YRdGwrdD | 重症医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/YRdGwrdD.html |
| 谷孝芝 | 9wdLg4bj | 重症医学科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/9wdLg4bj.html |
| 吴立友 | pmbk5ezJ | 肾病科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/pmbk5ezJ.html |
| 赵威 | MvbmOeYA | 肾病科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/MvbmOeYA.html |
| 黄智莉 | pnel5aKB | 肾病科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/pnel5aKB.html |
| 周艳利 | MYerEdOB | 肾病科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/MYerEdOB.html |
| 陈家湄 | Jxbojagw | 肾病科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/Jxbojagw.html |
| 俸维 | l9avmeG1 | 肾病科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/l9avmeG1.html |
| 丘泽培 | 8mepZ1bM | 肾病科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/8mepZ1bM.html |
| 李娟 | openRe7A | 肾病科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/openRe7A.html |
| 唐瑾秋 | X7ax9byv | 肾病科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/X7ax9byv.html |
| 陈欢欢 | olejYWdj | 肾病科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/olejYWdj.html |
| 柯嘉儿 | MvbmqpbY | 肾病科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/MvbmqpbY.html |
| 邬旭芳 | 4zbqQ3bp | 肾病科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4zbqQ3bp.html |
| 黄彩兰 | pmbk2xaz | 肾病科 | 同德围分院 | https://www.gzszyy.com/expert/2026/pmbk2xaz.html |
| 刘伙亮 | openR4e7 | 肾病科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/openR4e7.html |
| 毛凯凤 | JxboZzag | 肾病科 | 同德围分院 | https://www.gzszyy.com/expert/2026/JxboZzag.html |
| 李辉远 | jnegklew | 肾病科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/jnegklew.html |
| 谢丹丹 | MYer2weO | 肾病科 | 同德围分院 | https://www.gzszyy.com/expert/2026/MYer2weO.html |
| 李季 | LDdwRb1Y | 肾病科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/LDdwRb1Y.html |
| 蒙向欣 | olejRejN | 肾病科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/olejRejN.html |
| 周文斌 | Vyb895dv | 心病科（心血管内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/Vyb895dv.html |
| 李乙根 | BDbDkxal | 心病科（心血管内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/BDbDkxal.html |
| 陈勇 | YRdG9QaD | 心病科（心血管内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/YRdG9QaD.html |
| 叶玺 | YRdG67bD | 心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/YRdG67bD.html |
| 何皓颋 | 46dBBXd7 | 心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/46dBBXd7.html |
| 黄洁红 | 4oeERva0 | 心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4oeERva0.html |
| 高雅琦 | YQdJ62dO | 心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/YQdJ62dO.html |
| 徐文伟 | y1aKrReQ | 心病科（心血管内科） | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/y1aKrReQ.html |
| 常勇 | 9wdL9wej | 心病科（心血管内科） | 珠玑路院区、五羊门诊部、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/9wdL9wej.html |
| 方奕芬 | N1aM8AeW | 心病科（心血管内科） | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/N1aM8AeW.html |
| 何艳 | 3YaOYpdx | 心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/3YaOYpdx.html |
| 叶瑞妍 | YqaQWldn | 心病科（心血管内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/YqaQWldn.html |
| 陈东雄 | lNbW6Jay | 心病科（心血管内科） | 同德围分院 | https://www.gzszyy.com/expert/2026/lNbW6Jay.html |
| 郭文平 | zPdy6zeQ | 心病科（心血管内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/zPdy6zeQ.html |
| 郑舒馨 | J0dN7meL | 心病科（心血管内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/J0dN7meL.html |
| 方惠玉 | APdR6qdG | 心病科（心血管内科） | 同德围分院 | https://www.gzszyy.com/expert/2026/APdR6qdG.html |
| 刘伟强 | YQdJPlaO | 心病科（心血管内科） | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/YQdJPlaO.html |
| 成莎 | J0dNk6eL | 心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/J0dNk6eL.html |
| 刘昕 | WZdPNwaK | 心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/WZdPNwaK.html |
| 黄婧妍 | xkazq5eJ | 心病科（心血管内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/xkazq5eJ.html |
| 徐嘉欣 | y5eVOMaE | 心病科（心血管内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/y5eVOMaE.html |
| 何志凌 | openzDe7 | 心病科（心血管内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/openzDe7.html |
| 简小兵 | Jrb2WPdW | 内分泌科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/Jrb2WPdW.html |
| 王文英 | ELe3wne6 | 内分泌科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/ELe3wne6.html |
| 李慧枝 | Vyb8E5dv | 内分泌科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/Vyb8E5dv.html |
| 陈丽兰 | 5xe7XGa7 | 内分泌科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/5xe7XGa7.html |
| 赵志祥 | K9b69QaE | 内分泌科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/K9b69QaE.html |
| 邓伟明 | M7e5LZd2 | 内分泌科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/M7e5LZd2.html |
| 李宝玲 | N1aM9BaW | 内分泌科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/N1aM9BaW.html |
| 秦棱 | J0dN8KaL | 内分泌科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/J0dN8KaL.html |
| 陈燕珊 | y1aK6zeQ | 内分泌科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/y1aK6zeQ.html |
| 伊娜 | GRb4L0bB | 内分泌科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/GRb4L0bB.html |
| 叶焰 | pnelxleK | 肺病科（呼吸内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/pnelxleK.html |
| 丘梅清 | 4zbq2Rdp | 肺病科（呼吸内科） | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/4zbq2Rdp.html |
| 里自然 | JxboVzag | 肺病科（呼吸内科） | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/JxboVzag.html |
| 刘红宇 | MvbmOpeY | 肺病科（呼吸内科） | 同德围分院 | https://www.gzszyy.com/expert/2026/MvbmOpeY.html |
| 刘新宇 | openx4b7 | 肺病科（呼吸内科） | 同德围分院 | https://www.gzszyy.com/expert/2026/openx4b7.html |
| 张基磊 | 8mep81eM | 肺病科（呼吸内科） | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/8mep81eM.html |
| 熊艳云 | 4zbq73ep | 肺病科（呼吸内科） | 同德综合门诊部 | https://www.gzszyy.com/expert/2026/4zbq73ep.html |
| 梁仕勤 | LDdwVJb1 | 肺病科（呼吸内科） | 珠玑路院区 | https://www.gzszyy.com/expert/2026/LDdwVJb1.html |
| 高婉玲 | l9avlVdG | 肺病科（呼吸内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/l9avlVdG.html |
| 蔡松 | APdR8zaG | 肺病科（呼吸内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/APdR8zaG.html |
| 金华伟 | MYer8wbO | 肺病科（呼吸内科） | 同德围分院 | https://www.gzszyy.com/expert/2026/MYer8wbO.html |
| 苏丽玲 | YqaQOqdn | 肺病科（呼吸内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/YqaQOqdn.html |
| 李俐 | lNbWqXey | 肺病科（呼吸内科） | 官网详情未标注 | https://www.gzszyy.com/expert/2026/lNbWqXey.html |
| 李关宁 | oQeZzvep | 外科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/oQeZzvep.html |
| 郭宇明 | KQe1G3bJ | 外科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/KQe1G3bJ.html |
| 邝仰东 | Jrb27JdW | 外科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/Jrb27JdW.html |
| 张惠东 | ELe3yrb6 | 外科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/ELe3yrb6.html |
| 史振军 | GRb4z2eB | 外科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/GRb4z2eB.html |
| 杨泽娟 | M7e5Rxa2 | 外科 | 珠玑路院区、五羊门诊部、同德综合门诊部 | https://www.gzszyy.com/expert/2026/M7e5Rxa2.html |
| 张宏 | K9b60QeE | 外科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/K9b60QeE.html |
| 严文兵 | 5xe7pwa7 | 外科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/5xe7pwa7.html |
| 耿燚 | WPe9DPdL | 外科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/WPe9DPdL.html |
| 郑晔辉 | K9b6YLaE | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/K9b6YLaE.html |
| 黄琼刁 | MYerEkdO | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/MYerEkdO.html |
| 金享林 | olejnzej | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/olejnzej.html |
| 周坤炎 | 46dB12b7 | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/46dB12b7.html |
| 李向平 | MYermwdO | 外科 | 珠玑路院区、五羊门诊部 | https://www.gzszyy.com/expert/2026/MYermwdO.html |
| 杨保参 | Vyb8B2ev | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/Vyb8B2ev.html |
| 林欢 | JxboONbg | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/JxboONbg.html |
| 李富荣 | w9aAm1av | 外科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/w9aAm1av.html |
| 韩树坤 | M7e5Aqe2 | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/M7e5Aqe2.html |
| 王健 | WZdP6yaK | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/WZdP6yaK.html |
| 何平胜 | 46dB82a7 | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/46dB82a7.html |
| 吴江平 | lNbWQWey | 外科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/lNbWQWey.html |
| 杨振淮 | QBeXrkby | 外科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/QBeXrkby.html |
| 田立新 | 4QbYy0bz | 外科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/4QbYy0bz.html |
| 李均乐 | 46dBnnd7 | 外科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/46dBnnd7.html |
| 龙云 | BDbD0Ybl | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/BDbD0Ybl.html |
| 詹一飞 | 5xe7W8e7 | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/5xe7W8e7.html |
| 杜猛 | xkazYeJ0 | 脉管炎科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/xkazYeJ0.html |
| 黎建华 | zPdy7aQr | 脉管炎科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/zPdy7aQr.html |
| 周毅平 | w9aAOdvM | 脉管炎科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/w9aAOdvM.html |
| 李顺宁 | 46dBXa79 | 脉管炎科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/46dBXa79.html |
| 王昕冉 | BDbDxbl2 | 脉管炎科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/BDbDxbl2.html |
| 张锦生 | 4oeEva0B | 脉管炎科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4oeEva0B.html |
| 黄春发 | YQdJ2dOG | 脉管炎科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/YQdJ2dOG.html |
| 钟镜锋 | YRdG7dDz | 脉管炎科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/YRdG7dDz.html |
| 卢楠 | YqaQAMan | 脉管炎科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/YqaQAMan.html |
| 范小华 | MYergBaO | 肛肠科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/MYergBaO.html |
| 陈诗伟 | 8mep9XaM | 肛肠科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/8mep9XaM.html |
| 柳霞 | l9avlrdG | 肛肠科 | 同德综合门诊部 | https://www.gzszyy.com/expert/2026/l9avlrdG.html |
| 李洋 | jnegZ9dw | 肛肠科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/jnegZ9dw.html |
| 陈超云 | olejZWej | 肛肠科 | 同德综合门诊部 | https://www.gzszyy.com/expert/2026/olejZWej.html |
| 简丽丝 | l9avmLeG | 肛肠科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/l9avmLeG.html |
| 黄阳勇 | MYer86bO | 肛肠科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/MYer86bO.html |
| 朱华聪 | 4zbqADbp | 肛肠科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4zbqADbp.html |
| 周征 | olejq5dj | 妇科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/olejq5dj.html |
| 王勇 | WPe9Q3eL | 妇科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/WPe9Q3eL.html |
| 禹安琪 | nXe0VXbx | 妇科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/nXe0VXbx.html |
| 钟居孟 | jnegL6aw | 妇科 | 同德围分院 | https://www.gzszyy.com/expert/2026/jnegL6aw.html |
| 王欣 | pmbkZXaz | 妇科 | 同德综合门诊部 | https://www.gzszyy.com/expert/2026/pmbkZXaz.html |
| 潘艳芳 | pnel56aK | 妇科 | 同德综合门诊部 | https://www.gzszyy.com/expert/2026/pnel56aK.html |
| 于杰 | 8mepQ6aM | 妇科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/8mepQ6aM.html |
| 卢巧毅 | 4zbqYrbp | 妇科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/4zbqYrbp.html |
| 唐媛 | MYerR6eO | 妇科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/MYerR6eO.html |
| 严杏 | LDdwmwa1 | 妇科 | 同德围分院 | https://www.gzszyy.com/expert/2026/LDdwmwa1.html |
| 麦观艳 | xkazB5aJ | 妇科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/xkazB5aJ.html |
| 黄亚南 | w9aAQ7av | 妇科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/w9aAQ7av.html |
| 孟聪 | openrle7 | 妇科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/openrle7.html |
| 宋燕 | JxboQKeg | 妇科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/JxboQKeg.html |
| 李秀然 | MvbmQ0bY | 妇科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/MvbmQ0bY.html |
| 肖达民 | 8mep2rbM | 儿科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/8mep2rbM.html |
| 石艳红 | J0dNxzaL | 儿科 | 五羊门诊部、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/J0dNxzaL.html |
| 陈致雯 | 3YaO7Nax | 儿科 | 五羊门诊部、同德综合门诊部 | https://www.gzszyy.com/expert/2026/3YaO7Nax.html |
| 廖寒林 | YqaQ1Yan | 儿科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/YqaQ1Yan.html |
| 刘艳荣 | APdRgReG | 儿科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/APdRgReG.html |
| 朱丽臻 | y5eVm1dE | 儿科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/y5eVm1dE.html |
| 范文萃 | QBeX6mby | 儿科 | 五羊门诊部、同德综合门诊部 | https://www.gzszyy.com/expert/2026/QBeX6mby.html |
| 刘婧平 | X7axozey | 儿科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/X7axozey.html |
| 卢景熙 | WZdP1neK | 儿科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/WZdP1neK.html |
| 徐丹 | 4QbYvpdz | 儿科 | 五羊门诊部、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/4QbYvpdz.html |
| 赖碧婷 | oQeZV6ep | 儿科 | 五羊门诊部、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/oQeZV6ep.html |
| 朱永健 | Jrb2vvbW | 儿科 | 五羊门诊部、同德围分院 | https://www.gzszyy.com/expert/2026/Jrb2vvbW.html |
| 李梦瑶 | ELe32Qd6 | 儿科 | 五羊门诊部、同德围分院 | https://www.gzszyy.com/expert/2026/ELe32Qd6.html |
| 李盼 | GRb4R6eB | 儿科 | 五羊门诊部、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/GRb4R6eB.html |
| 郑玲玲 | 4oeEZma0 | 儿科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4oeEZma0.html |
| 杜广亮 | lNbWngay | 儿科 | 五羊门诊部、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/lNbWngay.html |
| 姚美美 | l9avYgeG | 儿科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/l9avYgeG.html |
| 王惟岩 | YQdJE9bO | 儿科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/YQdJE9bO.html |
| 吴菁菁 | QBeX78dy | 儿科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/QBeX78dy.html |
| 关俊辉 | 46dBLJa7 | 骨伤科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/46dBLJa7.html |
| 张维 | zPdyrWeQ | 骨伤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/zPdyrWeQ.html |
| 林晓光 | pmbkoYbz | 骨伤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/pmbkoYbz.html |
| 田天照 | xkazK8bJ | 骨伤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/xkazK8bJ.html |
| 彭志华 | y1aKZneQ | 骨伤科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/y1aKZneQ.html |
| 刘保新 | BDbD9ndl | 骨伤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/BDbD9ndl.html |
| 陈胜 | YRdG50aD | 骨伤科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/YRdG50aD.html |
| 周就荣 | l9avjgaG | 骨伤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/l9avjgaG.html |
| 李嘉晖 | 3YaOJBex | 骨伤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/3YaOJBex.html |
| 潘俊曦 | lNbW7gby | 骨伤科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/lNbW7gby.html |
| 岑祖怡 | 4oeE9ke0 | 骨伤科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/4oeE9ke0.html |
| 张胜 | 9wdL84dj | 骨伤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/9wdL84dj.html |
| 周伟君 | J0dN9zbL | 骨伤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/J0dN9zbL.html |
| 陈立业 | 3YaOyNdx | 骨伤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/3YaOyNdx.html |
| 李安 | WZdPZnaK | 骨伤科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/WZdPZnaK.html |
| 秦启宁 | YqaQ0Yen | 骨伤科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/YqaQ0Yen.html |
| 梁浩东 | y5eVP1bE | 骨伤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/y5eVP1bE.html |
| 黄鹏 | APdRoReG | 骨伤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/APdRoReG.html |
| 周沛 | QBeXomdy | 骨伤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/QBeXomdy.html |
| 温俊贤 | 4QbYWpez | 骨伤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4QbYWpez.html |
| 周剑鹏 | YQdJqobO | 骨伤科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/YQdJqobO.html |
| 徐铮 | 4zbqVRdp | 骨伤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4zbqVRdp.html |
| 付忠泉 | 3YaOEBdx | 骨伤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/3YaOEBdx.html |
| 冯庆辉 | w9aAPzev | 骨伤科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/w9aAPzev.html |
| 张智琳 | xkazvraJ | 急诊科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/xkazvraJ.html |
| 林宏 | X7axnJdy | 急诊科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/X7axnJdy.html |
| 范小红 | zPdyoVaQ | 急诊科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/zPdyoVaQ.html |
| 王书浩 | BDbD1Bdl | 急诊科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/BDbD1Bdl.html |
| 谢慧君 | 9wdLJWaj | 急诊科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/9wdLJWaj.html |
| 肖曼 | y1aKQzdQ | 急诊科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/y1aKQzdQ.html |
| 蔡飙 | w9aANBbv | 急诊科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/w9aANBbv.html |
| 陈亚勇 | 46dBNxd7 | 急诊科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/46dBNxd7.html |
| 孔祥照 | 4oeE8Nd0 | 急诊科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4oeE8Nd0.html |
| 孙铄 | YRdGvybD | 急诊科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/YRdGvybD.html |
| 包婷婷 | YQdJ8DaO | 急诊科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/YQdJ8DaO.html |
| 王桂红 | WZdPQleK | 急诊科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/WZdPQleK.html |
| 吴金梅 | J0dN0KaL | 急诊科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/J0dN0KaL.html |
| 罗刚 | APdR10bG | 急诊科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/APdR10bG.html |
| 张林芳 | N1aM1BaW | 急诊科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/N1aM1BaW.html |
| 魏星 | 3YaO8Gbx | 急诊科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/3YaO8Gbx.html |
| 石文君 | YqaQ7qdn | 急诊科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/YqaQ7qdn.html |
| 肖珍科 | KQe163aJ | 麻醉科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/KQe163aJ.html |
| 陈陈燕 | GRb462eB | 麻醉科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/GRb462eB.html |
| 谭花 | M7e57xb2 | 麻醉科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/M7e57xb2.html |
| 劳俊铭 | K9b6W7dE | 麻醉科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/K9b6W7dE.html |
| 刘栋 | 5xe79wb7 | 麻醉科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/5xe79wb7.html |
| 潘伶俐 | WPe99PeL | 麻醉科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/WPe99PeL.html |
| 黄嘉瑜 | nXe087ex | 麻醉科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/nXe087ex.html |
| 陈洲 | jnegp9aw | 麻醉科 | 同德围分院 | https://www.gzszyy.com/expert/2026/jnegp9aw.html |
| 尧新华 | oQeZ8vbp | 麻醉科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/oQeZ8vbp.html |
| 鲁义 | ELe36rd6 | 麻醉科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/ELe36rd6.html |
| 王保 | 5xe7AGb7 | 麻醉科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/5xe7AGb7.html |
| 周朴 | Jrb28JeW | 麻醉科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/Jrb28JeW.html |
| 于林 | oQeZw2ap | 睡眠心理科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/oQeZw2ap.html |
| 张红玉 | Jrb2gjdW | 睡眠心理科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/Jrb2gjdW.html |
| 王若愚 | KQe1Y0eJ | 睡眠心理科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/KQe1Y0eJ.html |
| 刘恩益 | ELe3j4d6 | 睡眠心理科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/ELe3j4d6.html |
| 高三德 | QBeXY8ay | 治未病科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/QBeXY8ay.html |
| 唐瑾秋 | 4QbYVOdz | 治未病科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4QbYVOdz.html |
| 高三德 | LDdwkmd1 | 治未病科、普通内科、杂病门诊 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/LDdwkmd1.html |
| 杜文坚 | LDdw0Je1 | 治未病科 | 五羊门诊部、珠玑路院区 | https://www.gzszyy.com/expert/2026/LDdw0Je1.html |
| 田晓航 | ELe3Y4b6 | 治未病科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/ELe3Y4b6.html |
| 魏赈权 | KQe1V0aJ | 治未病科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/KQe1V0aJ.html |
| 潘雨薇 | oQeZZ2ep | 治未病科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/oQeZZ2ep.html |
| 李国栋 | LDdwEga1 | 治未病科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/LDdwEga1.html |
| 黄自浩 | l9avYLeG | 治未病科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/l9avYLeG.html |
| 刘玉 | WZdPMyeK | 治未病科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/WZdPMyeK.html |
| 陈群雄 | l9avQVeG | 体检科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/l9avQVeG.html |
| 刘淑果 | LDdwVwb1 | 体检科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/LDdwVwb1.html |
| 马万里 | K9b6X9eE | 皮肤科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/K9b6X9eE.html |
| 潘慧宜 | 5xe71Ab7 | 皮肤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/5xe71Ab7.html |
| 刘敏怡 | WPe913eL | 皮肤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/WPe913eL.html |
| 谢凌鹏 | LDdwngb1 | 皮肤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/LDdwngb1.html |
| 蒋淑明 | Vyb81odv | 皮肤科 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/Vyb81odv.html |
| 乐元 | jnegxZaw | 皮肤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/jnegxZaw.html |
| 张蓉 | jnegZ6dw | 皮肤科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/jnegZ6dw.html |
| 张丽 | MYerEBdO | 皮肤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/MYerEBdO.html |
| 杨波涛 | WPe924aL | 皮肤科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/WPe924aL.html |
| 陈绮蕾 | nXe0YXax | 皮肤科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/nXe0YXax.html |
| 温璞 | KQe1WjbJ | 口腔科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/KQe1WjbJ.html |
| 吴琴艳 | Jrb2xveW | 口腔科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/Jrb2xveW.html |
| 孔羽 | ELe3QQb6 | 口腔科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/ELe3QQb6.html |
| 宋亚平 | GRb4Q6dB | 口腔科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/GRb4Q6dB.html |
| 李佳芮 | lNbWw4by | 口腔科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/lNbWw4by.html |
| 李煦 | APdRMzbG | 口腔科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/APdRMzbG.html |
| 黄淇 | YQdJY9bO | 口腔科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/YQdJY9bO.html |
| 项琳怡 | Mvbm2EdY | 口腔科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/Mvbm2EdY.html |
| 彭冲 | openYYd7 | 口腔科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/openYYd7.html |
| 陈传耀 | oQeZY6dp | 口腔科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/oQeZY6dp.html |
| 孙璇 | y5eV5BdE | 口腔科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/y5eV5BdE.html |
| 杜红彦 | pmbk8Xdz | 眼科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/pmbk8Xdz.html |
| 王蓉 | olejZ5ej | 眼科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/olejZ5ej.html |
| 骆煌 | MvbmO0eY | 眼科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/MvbmO0eY.html |
| 谢晓燕 | JxboVKag | 眼科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/JxboVKag.html |
| 闫冉 | 8mep86eM | 眼科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/8mep86eM.html |
| 简月玲 | openxlb7 | 眼科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/openxlb7.html |
| 陈伟豪 | y1aKYldQ | 眼科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/y1aKYldQ.html |
| 张瑜 | 9wdLYpej | 眼科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/9wdLYpej.html |
| 王怡 | YqaQNMbn | 眼科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/YqaQNMbn.html |
| 李建良 | pnelx6eK | 眼科 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/pnelx6eK.html |
| 江坚 | M7e59Re2 | 耳鼻喉科 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/M7e59Re2.html |
| 郑妮亚 | ELe39nb6 | 耳鼻喉科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/ELe39nb6.html |
| 黄丽燕 | Jrb29PaW | 耳鼻喉科 | 同德综合门诊部 | https://www.gzszyy.com/expert/2026/Jrb29PaW.html |
| 周雪 | Vyb86oev | 耳鼻喉科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/Vyb86oev.html |
| 徐宁聪 | N1aMEPaW | 耳鼻喉科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/N1aMEPaW.html |
| 杨晓倩 | 9wdLApej | 耳鼻喉科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/9wdLApej.html |
| 周宇 | X7axVzdy | 耳鼻喉科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/X7axVzdy.html |
| 彭庆源 | N1aM7PdW | 耳鼻喉科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/N1aM7PdW.html |
| 徐艳玲 | y1aKAldQ | 耳鼻喉科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/y1aKAldQ.html |
| 林少贞 | ELe31Mb6 | 针灸康复科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/ELe31Mb6.html |
| 马卫东 | M7e5yBe2 | 针灸康复科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/M7e5yBe2.html |
| 明康文 | nXe09Gax | 针灸康复科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/nXe09Gax.html |
| 黎崖冰 | GRb4x1bB | 针灸康复科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/GRb4x1bB.html |
| 黄应杰 | WZdPYleK | 针灸康复科 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/WZdPYleK.html |
| 段渊 | GRb4WgaB | 针灸康复科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/GRb4WgaB.html |
| 赵明昂 | J0dNYLbL | 针灸康复科、同德综合门诊部 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/J0dNYLbL.html |
| 曹湘萍 | WPe9rxaL | 针灸康复科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/WPe9rxaL.html |
| 李良 | nXe0Rvbx | 针灸康复科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/nXe0Rvbx.html |
| 张万清 | jneg5Ybw | 针灸康复科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/jneg5Ybw.html |
| 柴芳芳 | Jxbojzag | 针灸康复科 | 珠玑路院区、五羊门诊部 | https://www.gzszyy.com/expert/2026/Jxbojzag.html |
| 陈振兴 | pmbk55ez | 针灸康复科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/pmbk55ez.html |
| 李富铭 | olejvYej | 针灸康复科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/olejvYej.html |
| 王梦华 | BDbDwAal | 针灸康复科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/BDbDwAal.html |
| 张玉辉 | xkazn7aJ | 普通内科、杂病门诊 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/xkazn7aJ.html |
| 杨周瑞 | zPdymwdQ | 普通内科、杂病门诊 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/zPdymwdQ.html |
| 邹爱萍 | X7ax6Jdy | 普通内科、杂病门诊 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/X7ax6Jdy.html |
| 谭锦培 | X7axlnay | 普通内科、杂病门诊 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/X7axlnay.html |
| 郑婕 | N1aMJQbW | 同德综合门诊部 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/N1aMJQbW.html |
| 徐志坚 | zPdywVaQ | 同德综合门诊部 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/zPdywVaQ.html |
| 高文凯 | 46dBrxd7 | 同德综合门诊部 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/46dBrxd7.html |
| 周俐 | BDbDqBdl | 同德综合门诊部 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/BDbDqBdl.html |
| 沈蓉 | xkaz6raJ | 同德综合门诊部 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/xkaz6raJ.html |
| 陈莉 | 4oeEqNe0 | 同德综合门诊部 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/4oeEqNe0.html |
| 肖春 | 9wdLvgaj | 同德综合门诊部 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/9wdLvgaj.html |
| 揭英柱 | WZdPzzaK | 同德综合门诊部 | 珠玑路院区、五羊门诊部、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/WZdPzzaK.html |
| 官娜 | YqaQ67bn | 同德综合门诊部 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/YqaQ67bn.html |
| 廖堪善 | lNbW8Xdy | 同德综合门诊部 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/lNbW8Xdy.html |
| 黄欢溢 | M7e5QRe2 | 同德综合门诊部 | 珠玑路院区、五羊门诊部、同德综合门诊部 | https://www.gzszyy.com/expert/2026/M7e5QRe2.html |
| 陶慧芳 | YRdGRybD | 同德综合门诊部 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/YRdGRybD.html |
| 王晓 | YQdJNDdO | 同德综合门诊部 | 五羊门诊部、同德综合门诊部 | https://www.gzszyy.com/expert/2026/YQdJNDdO.html |
| 伍彦坤 | y1aKLrbQ | 同德综合门诊部 | 同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/y1aKLrbQ.html |
| 梁月云 | APdRPLaG | 同德综合门诊部 | 珠玑路院区、同德围分院、同德综合门诊部 | https://www.gzszyy.com/expert/2026/APdRPLaG.html |
| 陆玉婷 | y5eV75aE | 同德综合门诊部 | 珠玑路院区、同德综合门诊部 | https://www.gzszyy.com/expert/2026/y5eV75aE.html |
| 顾颖敏 | nXe007ex | 五羊门诊部 | 珠玑路院区、五羊门诊部 | https://www.gzszyy.com/expert/2026/nXe007ex.html |
| 刘荣东 | olej0Wbj | 五羊门诊部 | 五羊门诊部 | https://www.gzszyy.com/expert/2026/olej0Wbj.html |
| 李碧茜 | 4oeEPKd0 | 五羊门诊部 | 珠玑路院区、五羊门诊部 | https://www.gzszyy.com/expert/2026/4oeEPKd0.html |
| 黄锦才 | MvbmYpbY | 五羊门诊部 | 五羊门诊部 | https://www.gzszyy.com/expert/2026/MvbmYpbY.html |
| 黄海胜 | 8mepk1dM | 五羊门诊部 | 五羊门诊部 | https://www.gzszyy.com/expert/2026/8mepk1dM.html |
| 李根良 | pnel2lbK | 五羊门诊部 | 五羊门诊部 | https://www.gzszyy.com/expert/2026/pnel2lbK.html |
| 赵晓红 | openg4a7 | 五羊门诊部 | 珠玑路院区、五羊门诊部 | https://www.gzszyy.com/expert/2026/openg4a7.html |
| 王花 | l9av8VdG | 五羊门诊部 | 五羊门诊部 | https://www.gzszyy.com/expert/2026/l9av8VdG.html |
| 钟燊明 | LDdwKJd1 | 五羊门诊部 | 五羊门诊部 | https://www.gzszyy.com/expert/2026/LDdwKJd1.html |
| 吴滢珏 | jnegnldw | 五羊门诊部 | 五羊门诊部、珠玑路院区 | https://www.gzszyy.com/expert/2026/jnegnldw.html |
| 杨詠嘉 | olej0zbj | 五羊门诊部 | 五羊门诊部 | https://www.gzszyy.com/expert/2026/olej0zbj.html |
| 李钊杨 | QBeXMlay | 五羊门诊部 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/QBeXMlay.html |
| 李晚君 | opengDa7 | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/opengDa7.html |
| 张亿星 | JxbojNag | 医学影像科 | 同德围分院 | https://www.gzszyy.com/expert/2026/JxbojNag.html |
| 吴美仙 | MYer9kdO | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/MYer9kdO.html |
| 崔东 | 8mepkrdM | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/8mepkrdM.html |
| 蔡银连 | 4zbqZRdp | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4zbqZRdp.html |
| 赖振辉 | X7ax1nby | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/X7ax1nby.html |
| 莫树群 | 4oeExKd0 | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4oeExKd0.html |
| 谈燊 | YQdJQlbO | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/YQdJQlbO.html |
| 郭美芬 | l9avZgaG | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/l9avZgaG.html |
| 邓富鑫 | zPdyXwbQ | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/zPdyXwbQ.html |
| 梁晓韵 | w9aA11av | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/w9aA11av.html |
| 彭佳 | YRdG8QeD | 医学影像科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/YRdG8QeD.html |
| 王修银 | 9wdLZgaj | 检验病理科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/9wdLZgaj.html |
| 王健 | 3YaOggax | 检验病理科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/3YaOggax.html |
| 曾博煌 | 4QbY70ez | 检验病理科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/4QbY70ez.html |
| 江沂 | J0dNOLeL | 检验病理科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/J0dNOLeL.html |
| 李丽明 | KQe19oeJ | 药学部 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/KQe19oeJ.html |
| 刘若轩 | pnel2JbK | 药学部 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/pnel2JbK.html |
| 邓志军 | MvbmYAbY | 药学部 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/MvbmYAbY.html |
| 张晓玲 | nXe0AVax | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/nXe0AVax.html |
| 何超颖 | jneg7Zew | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/jneg7Zew.html |
| 郭美珍 | olejAYdj | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/olejAYdj.html |
| 支孟妮 | pmbk6raz | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/pmbk6raz.html |
| 粟云云 | pnel87eK | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/pnel87eK.html |
| 郭佩欣 | Mvbm7EeY | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/Mvbm7EeY.html |
| 郑楠 | openGYa7 | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/openGYa7.html |
| 冯政君 | JxboAAeg | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/JxboAAeg.html |
| 张展东 | M7e5lqd2 | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/M7e5lqd2.html |
| 杜慕萱 | K9b6mLaE | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/K9b6mLaE.html |
| 李鸯 | 5xe7D8a7 | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/5xe7D8a7.html |
| 张红艳 | Vyb8X2bv | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/Vyb8X2bv.html |
| 计宏媛 | WPe938bL | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/WPe938bL.html |
| 戴志兵 | GRb4kgaB | 超声医学科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/GRb4kgaB.html |
| 李爱民 | lNbWW4by | 无 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/lNbWW4by.html |

### 同名身份聚类裁决

| 姓名 | 详情 ID | 裁决 | 原详情关系 | 合并科室 | 院区/出诊点 | 主详情 | 其余详情 |
|---|---|---|---:|---|---|---|---|
| 林少贞 | JxboyNeg,ELe31Mb6 | 同一人归并 | 2 | 针灸科、针灸康复科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/ELe31Mb6.html | https://www.gzszyy.com/expert/2026/JxboyNeg.html |
| 唐瑾秋 | X7ax9byv,4QbYVOdz | 同一人归并 | 2 | 肾病科、治未病科 | 珠玑路院区 | https://www.gzszyy.com/expert/2026/4QbYVOdz.html | https://www.gzszyy.com/expert/2026/X7ax9byv.html |
| 王健 | WZdP6yaK | 同名待甄别 | 1 | 外科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/WZdP6yaK.html | 无 |
| 王健 | 3YaOggax | 同名待甄别 | 1 | 检验病理科 | 官网详情未标注 | https://www.gzszyy.com/expert/2026/3YaOggax.html | 无 |
| 高三德 | QBeXY8ay,LDdwkmd1 | 同一人归并 | 3 | 治未病科、普通内科、杂病门诊 | 珠玑路院区、同德围分院 | https://www.gzszyy.com/expert/2026/QBeXY8ay.html | https://www.gzszyy.com/expert/2026/LDdwkmd1.html |

## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| https://www.gzszyy.com/expert/ | 黄金兰 主管护师 | https://www.gzszyy.com/expert/2026/8mepzrbM.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |
| https://www.gzszyy.com/expert/ | 王少敏 主任护师 | https://www.gzszyy.com/expert/2026/pnelpJeK.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |
| https://www.gzszyy.com/expert/ | 曾会萍 主任护师 | https://www.gzszyy.com/expert/2026/8mep2bMy.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |
| https://www.gzszyy.com/expert/ | 周素金 主管护师 | https://www.gzszyy.com/expert/2026/4zbq2dpr.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |
| https://www.gzszyy.com/expert/ | 谭萍云 主管护师 | https://www.gzszyy.com/expert/2026/MvbmEAbY.html | 官网科室目录仅标注护理身份，排除医生画像采集范围 |

## 输出文件

- Excel 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx`
- CSV 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 37 |
| 原始医生卡片记录 | 434 |
| 跨入口去重前候选关系 | 434 |
| 跨入口去重后唯一候选 | 423 |
| 排除非医生候选 | 5 |
| 合规医生详情页 | 418 |
| 最终医生身份 | 415 |
| 覆盖科室数 | 36 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 415 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 59 |
| 慢性病 | 152 |
| 术后恢复/康复 | 82 |
| 生殖疾病 | 59 |
| 疑难重症 | 101 |
| 肿瘤 | 80 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 外科 | 26 |
| 骨伤科 | 25 |
| 心病科（心血管内科） | 23 |
| 脾胃科（消化内科） | 23 |
| 脑病科（神经内科） | 20 |
| 肾病科 | 19 |
| 儿科 | 19 |
| 急诊科 | 17 |
| 同德综合门诊部 | 17 |
| 妇科 | 15 |
| 针灸康复科 | 14 |
| 超声医学科 | 14 |
| 针灸科 | 13 |
| 肺病科（呼吸内科） | 13 |
| 麻醉科 | 12 |
| 五羊门诊部 | 12 |
| 医学影像科 | 12 |
| 名医堂 | 11 |
| 口腔科 | 11 |
| 内分泌科 | 10 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 职称/身份需人工复核 | 12 |
| 多详情职称不一致 | 2 |
| 同名待甄别 | 2 |
| 科室需人工复核 | 1 |

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
