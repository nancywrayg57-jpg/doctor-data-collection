---
类型: 全量采集归并审计报告
医院: 广东省妇幼保健院
城市: 广州市
采集日期: 2026-08-14
来源范围: 医院官网
采集入口: https://www.e3861.com/keshizhuanjia/zhuanjiajieshao
适配器: gdmch_paginated_expert_photo
---

# 广东省妇幼保健院 官方医生全量采集归并审计报告

## 结论

本次全量采集只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集全量采集底表，共 832 位唯一医生；官网列表页原始卡片记录 884 条；读取入口分类 111 个；覆盖 89 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 广东省妇幼保健院 |
| 官网首页 | https://www.e3861.com/ |
| 本轮医生入口 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao |
| 入口来源 | GitHub Issue #43（与官网入口台账序号 21 一致） |
| 原台账医生入口 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | D-待人工补官网 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
|  | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao | 官网服务端专家目录分页；卡片含姓名、职称和官方子域职业照 | 111 | 884 | 884 | 49 | 广东省妇幼保健院 | 四院区共用官网专家目录和统一页脚；未发现独立法人标识 |

### 动态目录专项证据

- 医生分页/载入方式：111 个服务端公开 GET 分页；仅空白 searchDoctor/searchDepartment，不构造检索词
- 医生目录公开接口：不适用
- 医生详情公开接口：不适用
- 接口出处证据：不适用
- 院区/分组：0 个；科室分类：0 个
- 医生-科室关系：884 条
- 唯一详情 ID：884 个
- 有姓名详情 ID：832 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：832 个
- 同名不同详情 ID：4 组
- 非空/空科室块：0 / 0
- 院区/出诊点标签关系：番禺院区 505 条；天河院区 181 条；越秀院区 299 条；清远院区 71 条
- 跨院区/出诊点详情 ID：0 个

| 同名 | 详情 ID |
|---|---|
| 郭庆禄 | 34640,34931 |
| 周真 | 32647,32821 |
| 刘颖 | 32499,33007 |
| 何裕 | 32750,33134 |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：884
- 跨入口去重后唯一候选：884
- 跨入口重复关系：0
- 试采覆盖入口分类：89 个（40+女性健康、三叉神经痛专病、中医儿科、中医科、中西医结合儿科、乳腺疾病影像学诊断、乳腺科、产前诊断、产科、体检科、体重管理、便民、儿科、儿科发热、儿科呼吸、儿科消化、儿科药学、儿童保健科、儿童内分泌遗传代谢、儿童内分泌遗传代谢科、儿童咳喘药学服务、儿童过敏多学科联合、儿童过敏性鼻炎、儿童风湿病科、入园入托体检、公卫科、内科、医学美容科、医疗美容科、口腔科、外科、妇女保健科、妇科、小儿便秘外科、小儿内科神经内科、小儿地中海贫血、小儿外科、小儿普外科、小儿泌尿外科、小儿疝微创、小儿神经外科、小儿肾内科、小儿肿瘤内科、小儿肿瘤外科、小儿胸壁筛查、小儿胸外科、小儿血液病、小儿铅中毒、小儿骨科、小儿黄疸外科、康复医学科、心理科、心脏中心、成人泌尿外科、放射科、新生儿外科、新生儿科、早孕、早孕关爱、普通儿科、暑假包皮、更年期、毒物检验室、特需儿童预防接种咨询、生殖健康与不孕症科、生育力保存多学科、甲状腺外科、疼痛科、病理科、痉挛型脑瘫SDR治疗专病、皮肤性病科、眼科、耳鼻咽喉头颈外科、肛肠外科、脊柱裂脊髓栓系专病、脑机接口睡眠中心、药学、药学咨询、营养科、血友病专病、血管瘤、超声诊断科、身高管理、遗传病专科诊疗、静脉曲张、鞘膜积液日间手术、颅缝早闭头颅畸形专病、骨科、麻醉科）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 无 | 无 | 无 |

## 广东省妇幼保健院目录、四院区与照片全量采集对账

- 官网服务端分页：111 页；原始卡片 / 唯一数字详情 ID：884 / 884。
- 重复关系：0；号源/系统账号/非医生排除：51；排除后合规候选：833。
- 科室结构：目录只提供自由文本检索框，无服务端科室分类树；样本科室仅从详情出诊安排括号标签保守提取，日期时段不入库。
- 全量采集覆盖科室：89 个（40+女性健康、三叉神经痛专病、中医儿科、中医科、中西医结合儿科、乳腺疾病影像学诊断、乳腺科、产前诊断、产科、体检科、体重管理、便民、儿科、儿科发热、儿科呼吸、儿科消化、儿科药学、儿童保健科、儿童内分泌遗传代谢、儿童内分泌遗传代谢科、儿童咳喘药学服务、儿童过敏多学科联合、儿童过敏性鼻炎、儿童风湿病科、入园入托体检、公卫科、内科、医学美容科、医疗美容科、口腔科、外科、妇女保健科、妇科、小儿便秘外科、小儿内科神经内科、小儿地中海贫血、小儿外科、小儿普外科、小儿泌尿外科、小儿疝微创、小儿神经外科、小儿肾内科、小儿肿瘤内科、小儿肿瘤外科、小儿胸壁筛查、小儿胸外科、小儿血液病、小儿铅中毒、小儿骨科、小儿黄疸外科、康复医学科、心理科、心脏中心、成人泌尿外科、放射科、新生儿外科、新生儿科、早孕、早孕关爱、普通儿科、暑假包皮、更年期、毒物检验室、特需儿童预防接种咨询、生殖健康与不孕症科、生育力保存多学科、甲状腺外科、疼痛科、病理科、痉挛型脑瘫SDR治疗专病、皮肤性病科、眼科、耳鼻咽喉头颈外科、肛肠外科、脊柱裂脊髓栓系专病、脑机接口睡眠中心、药学、药学咨询、营养科、血友病专病、血管瘤、超声诊断科、身高管理、遗传病专科诊疗、静脉曲张、鞘膜积液日间手术、颅缝早闭头颅畸形专病、骨科、麻醉科）；详情失败：0。
- 最终身份：832；同一人归并 1 组；实质不同同名 3 组。
- 四院区官网归属证据：4 条；独立实体信号：0。
- 详情清洗：排班片段排除 866，排名/患者片段排除 0，患者案例排除 0；正式字段排班写入 0、私用区字符 0。
- 照片四数：应采 658 / 实采 658 / 失败 0 / 无照片 174。
- 本人职业照可得 / 官网默认占位图：658 / 175（全目录默认占位图 225）。
- 平均照片大小：48095 bytes；按 658 位有本人职业照候选估算全院照片容量：31646510 bytes。
- 大图阈值：`单张 >200KB 或宽 >800px`；命中 0 张；照片政策状态：`OWNER_APPROVED_ORIGINAL_NO_WIDTH_LIMIT`。原图不压缩；命中阈值时必须等待 owner 裁决本院 FULL 策略。
- 普通公开会话：requests 常规公开 GET；无登录、Cookie 注入、验证码/挑战求解或非公开接口。

### 四院区官方归属证据

| 院区 | 官方链接 | 归属结论 |
|---|---|---|
| 番禺院区 | https://www.e3861.com/keshizhuanjia/panyuyuanqu | 官网同一专家目录与统一页脚列示的广东省妇幼保健院院区；未发现独立法人标识 |
| 越秀院区 | https://www.e3861.com/keshizhuanjia/yuexiuyuanqu | 官网同一专家目录与统一页脚列示的广东省妇幼保健院院区；未发现独立法人标识 |
| 天河院区 | https://www.e3861.com/keshizhuanjia/tianheyuanqu | 官网同一专家目录与统一页脚列示的广东省妇幼保健院院区；未发现独立法人标识 |
| 清远院区 | https://www.e3861.com/keshizhuanjia/qingyuanyuanqu | 官网同一专家目录与统一页脚列示的广东省妇幼保健院院区；未发现独立法人标识 |

### 833 个合规详情逐 ID 对账

| 详情 ID | 姓名 | 科室 | 院区 | 详情状态 | 来源链接 |
|---|---|---|---|---|---|
| 32798 | 何伟健 | 心理科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32798.html |
| 32791 | 于海静 | 乳腺科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32791.html |
| 32786 | 王永南 | 乳腺科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32786.html |
| 32568 | 邹素文 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32568.html |
| 32787 | 朱彩霞 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32787.html |
| 32569 | 余海云 | 乳腺科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32569.html |
| 32441 | 李文萍 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32441.html |
| 32788 | 万舰 | 乳腺科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32788.html |
| 32440 | 张安秦 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32440.html |
| 32442 | 陈中扬 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32442.html |
| 32789 | 罗懿忠 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32789.html |
| 32443 | 连臻强 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32443.html |
| 32790 | 杨剑敏 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32790.html |
| 32570 | 谢四梅 | 乳腺科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32570.html |
| 32444 | 许娟 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32444.html |
| 32762 | 邱桂霞 | 小儿肾内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32762.html |
| 32469 | 王伟光 | 普通儿科、小儿肾内科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32469.html |
| 32572 | 肖梦加 | 乳腺科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32572.html |
| 32451 | 郭莉 | 产前诊断 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32451.html |
| 34559 | 饶腾子 | 产前诊断 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34559.html |
| 32769 | 李陈 | 产前诊断、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32769.html |
| 35069 | 贾杰 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35069.html |
| 32452 | 吴菁 | 产前诊断、遗传病专科诊疗 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32452.html |
| 32453 | 尹爱华 | 产前诊断 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32453.html |
| 32904 | 李静姝 | 产前诊断、早孕关爱 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32904.html |
| 32799 | 何薇 | 产前诊断 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32799.html |
| 32584 | 石晓梅 | 产前诊断 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32584.html |
| 32800 | 杜丽 | 产前诊断、遗传病专科诊疗 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32800.html |
| 32801 | 熊盈 | 产前诊断 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32801.html |
| 32802 | 赵馨 | 产前诊断 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32802.html |
| 32760 | 黄艺文 | 小儿普外科、小儿外科、小儿疝微创 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32760.html |
| 33009 | 王逾男 | 产前诊断 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33009.html |
| 32578 | 李刚龙 | 小儿普外科、小儿肿瘤外科、小儿疝微创 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32578.html |
| 32580 | 董踌 | 小儿外科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32580.html |
| 32777 | 岑龙 | 小儿普外科、小儿肿瘤外科、小儿外科、小儿疝微创 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32777.html |
| 32447 | 朱小春 | 小儿普外科、小儿肿瘤外科、新生儿外科、小儿泌尿外科、小儿外科、小儿便秘外科、小儿黄疸外科、小儿疝微创 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32447.html |
| 32472 | 葛午平 | 新生儿外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32472.html |
| 32579 | 黄白沙 | 小儿普外科、小儿疝微创 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32579.html |
| 33019 | 赵颖 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33019.html |
| 32792 | 张心丽 | 耳鼻咽喉头颈外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32792.html |
| 33063 | 申晓宁 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33063.html |
| 32793 | 林小燕 | 耳鼻咽喉头颈外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32793.html |
| 33030 | 袁超 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33030.html |
| 33073 | 韩宝义 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33073.html |
| 32794 | 赵哲成 | 耳鼻咽喉头颈外科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32794.html |
| 33026 | 于菲菲 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33026.html |
| 33088 | 孙维国 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33088.html |
| 32574 | 刘漪 | 耳鼻咽喉头颈外科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32574.html |
| 33072 | 颜小龙 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33072.html |
| 32795 | 师小径 | 耳鼻咽喉头颈外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32795.html |
| 32797 | 陈曦 | 耳鼻咽喉头颈外科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32797.html |
| 32445 | 邹宇 | 耳鼻咽喉头颈外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32445.html |
| 32796 | 郭良芬 | 耳鼻咽喉头颈外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32796.html |
| 32446 | 麦飞 | 耳鼻咽喉头颈外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32446.html |
| 32756 | 李一心 | 耳鼻咽喉头颈外科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32756.html |
| 33071 | 冯嘉宝 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33071.html |
| 32449 | 尚宁 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32449.html |
| 32592 | 邹敬江 | 医疗美容科、血管瘤、医学美容科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32592.html |
| 32806 | 谭梅军 | 医疗美容科、血管瘤、医学美容科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32806.html |
| 32807 | 姜金豆 | 医疗美容科、血管瘤、医学美容科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32807.html |
| 32726 | 孙赛 | 医学美容科 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32726.html |
| 32591 | 陈容容 | 医疗美容科、血管瘤、医学美容科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32591.html |
| 32457 | 胡葵葵 | 医疗美容科、血管瘤、医学美容科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32457.html |
| 32526 | 潘小英 | 产前诊断 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32526.html |
| 32600 | 李甜甜 | 妇女保健科、妇科、更年期、40+女性健康 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32600.html |
| 32810 | 吕霄 | 妇女保健科、妇科、更年期、40+女性健康 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32810.html |
| 32598 | 李丽美 | 妇女保健科、妇科、更年期、40+女性健康 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32598.html |
| 32597 | 黄雪萍 | 妇女保健科、妇科、更年期、40+女性健康 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32597.html |
| 32461 | 夏建红 | 妇女保健科、妇科、更年期、40+女性健康 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32461.html |
| 32973 | 高奎杰 | 中西医结合儿科、普通儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32973.html |
| 32805 | 杨东新 | 中西医结合儿科、中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32805.html |
| 33083 | 杜岚岚 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33083.html |
| 33080 | 林健瑶 | 中西医结合儿科、普通儿科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33080.html |
| 32456 | 秦克旺 | 甲状腺外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32456.html |
| 32586 | 毛武 | 甲状腺外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32586.html |
| 35073 | 陈佳 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35073.html |
| 32877 | 史浩 | 肛肠外科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32877.html |
| 32951 | 邓航 | 肛肠外科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32951.html |
| 32565 | 乔平进 | 成人泌尿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32565.html |
| 32587 | 王子祥 | 甲状腺外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32587.html |
| 33008 | 王越 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33008.html |
| 32434 | 潘碧琦 | 儿童内分泌遗传代谢、中医科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32434.html |
| 32808 | 刘舒 | 儿童内分泌遗传代谢 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32808.html |
| 33040 | 罗先琼 | 儿童内分泌遗传代谢 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33040.html |
| 32593 | 李韵 | 儿童内分泌遗传代谢 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32593.html |
| 32594 | 邓智 | 儿童内分泌遗传代谢 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32594.html |
| 33203 | 王波 | 儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33203.html |
| 32595 | 张也 | 儿童内分泌遗传代谢 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32595.html |
| 32459 | 苏海浩 | 儿童内分泌遗传代谢、普通儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32459.html |
| 32907 | 陈上清 | 儿童内分泌遗传代谢 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32907.html |
| 33035 | 武丽 | 妇女保健科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33035.html |
| 32512 | 毛玲芝 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32512.html |
| 32507 | 范保维 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32507.html |
| 32972 | 叶祥 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32972.html |
| 32612 | 郭小燕 | 普通儿科、小儿血液病、小儿地中海贫血、血友病专病 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32612.html |
| 33189 | 赵小琴 | 普通儿科、小儿血液病 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33189.html |
| 33123 | 饶姣 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33123.html |
| 33045 | 黄景思 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33045.html |
| 33128 | 刘琴 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33128.html |
| 32460 | 孙善权 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32460.html |
| 33003 | 聂川 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33003.html |
| 33098 | 许芳 | 新生儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33098.html |
| 33004 | 向建文 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33004.html |
| 32466 | 帅春 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32466.html |
| 32534 | 张永 | 新生儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32534.html |
| 32505 | 文斌 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32505.html |
| 32610 | 肖丹 | 营养科、产科、体重管理、儿童过敏多学科联合 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32610.html |
| 32468 | 夏燕琼 | 营养科、产科、体重管理、儿童过敏多学科联合 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32468.html |
| 32771 | 郑新杰 | 营养科、产科、体重管理、儿童过敏多学科联合 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32771.html |
| 32609 | 田爽 | 营养科、体重管理 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32609.html |
| 32817 | 梅世伟 | 静脉曲张、血管瘤、放射科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32817.html |
| 33267 | 张钰颖 | 眼科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33267.html |
| 32596 | 杨思慧 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32596.html |
| 32604 | 冯庆阳 | 眼科、儿童过敏多学科联合 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32604.html |
| 33062 | 李丹丹 | 眼科 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33062.html |
| 32814 | 郑姣 | 眼科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32814.html |
| 32717 | 曾杞汶 | 眼科、儿童过敏多学科联合 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32717.html |
| 32605 | 穆歌 | 眼科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32605.html |
| 32908 | 何慧 | 儿童内分泌遗传代谢 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32908.html |
| 32815 | 谢素贞 | 眼科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32815.html |
| 32463 | 黄学林 | 眼科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32463.html |
| 32608 | 张振瑜 | 眼科、儿童过敏多学科联合 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32608.html |
| 32618 | 唐晶 | 小儿胸外科、小儿胸壁筛查 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32618.html |
| 32620 | 刘千里 | 小儿胸外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32620.html |
| 32621 | 商子寅 | 小儿胸外科、小儿胸壁筛查 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32621.html |
| 32809 | 马远珠 | 妇女保健科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32809.html |
| 32471 | 洪淳 | 小儿胸外科、小儿胸壁筛查 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32471.html |
| 32599 | 方俊 | 妇女保健科、更年期 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32599.html |
| 33046 | 刘蕾 | 普通儿科、儿童风湿病科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33046.html |
| 32822 | 周佳亮 | 新生儿外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32822.html |
| 32462 | 肖尚杰 | 新生儿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32462.html |
| 33180 | 李清青 | 皮肤性病科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33180.html |
| 32819 | 刁友涛 | 皮肤性病科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32819.html |
| 32820 | 李晓伟 | 皮肤性病科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32820.html |
| 32617 | 李真真 | 皮肤性病科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32617.html |
| 33048 | 汪青园 | 新生儿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33048.html |
| 32623 | 黄蓉 | 新生儿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32623.html |
| 32745 | 肖慧媚 | 小儿内科神经内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32745.html |
| 32470 | 常燕群 | 康复医学科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32470.html |
| 32494 | 刘芳 | 小儿内科神经内科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32494.html |
| 32435 | 徐宁 | 康复医学科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32435.html |
| 33032 | 杨娇 | 儿科消化、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33032.html |
| 32631 | 董川 | 儿科消化 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32631.html |
| 33213 | 郝彤彤 | 儿科消化 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33213.html |
| 32744 | 林兴 | 儿科消化 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32744.html |
| 32480 | 刘鸿 | 儿科消化、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32480.html |
| 32831 | 高利伟 | 儿科消化 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32831.html |
| 32607 | 吴怡凝 | 眼科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32607.html |
| 32629 | 林汇政 | 儿科消化 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32629.html |
| 32481 | 罗文雄 | 儿科消化 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32481.html |
| 32835 | 胡兢晶 | 普通儿科、儿童风湿病科 | 番禺院区、天河院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32835.html |
| 32479 | 马志明 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32479.html |
| 32628 | 陈思 | 内科、早孕关爱、便民 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32628.html |
| 32765 | 郭运忠 | 内科、脑机接口睡眠中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32765.html |
| 32824 | 张艳 | 内科、早孕关爱、便民 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32824.html |
| 32825 | 吕小飞 | 内科、早孕关爱、便民 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32825.html |
| 32473 | 徐力堃 | 内科、便民 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32473.html |
| 33049 | 郭祯 | 内科、早孕关爱、便民 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33049.html |
| 35005 | 张静 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35005.html |
| 32474 | 邹燕敦 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32474.html |
| 32826 | 刘祎婷 | 内科、早孕关爱、便民 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32826.html |
| 32827 | 林常青 | 内科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32827.html |
| 32829 | 赖锦斌 | 内科、便民 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32829.html |
| 32752 | 麦华超 | 内科、早孕关爱、便民 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32752.html |
| 35075 | 胡克 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35075.html |
| 32625 | 钟旋 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32625.html |
| 32476 | 范丽梅 | 内科、早孕关爱、便民 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32476.html |
| 32626 | 余丹峰 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32626.html |
| 32881 | 袁力 | 产科、早孕关爱 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32881.html |
| 32922 | 余干锋 | 产科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32922.html |
| 32482 | 李嘉蔚 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32482.html |
| 32483 | 梁海英 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32483.html |
| 32554 | 江剑辉 | 儿童内分泌遗传代谢科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32554.html |
| 32484 | 温济英 | 产科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32484.html |
| 32828 | 叶文慧 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32828.html |
| 33238 | 邢佳玲 | 产科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33238.html |
| 32920 | 田秀秀 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32920.html |
| 32923 | 金璟 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32923.html |
| 33150 | 彭静 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33150.html |
| 32957 | 周柏序 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32957.html |
| 32812 | 王意 | 妇女保健科、妇科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32812.html |
| 33152 | 余晖 | 产科、早孕关爱 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33152.html |
| 32486 | 袁晓兰 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32486.html |
| 32675 | 麦子霞 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32675.html |
| 32729 | 牛静 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32729.html |
| 32919 | 耿新明 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32919.html |
| 32634 | 侯明敏 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32634.html |
| 32834 | 张温麑 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32834.html |
| 34640 | 郭庆禄 | 乳腺疾病影像学诊断 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34640.html |
| 32514 | 和秀魁 | 妇科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32514.html |
| 32541 | 李荔 | 妇科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32541.html |
| 32548 | 王三锋 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32548.html |
| 32669 | 李海萍 | 妇科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32669.html |
| 32624 | 叶一林 | 疼痛科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32624.html |
| 32823 | 黄希照 | 疼痛科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32823.html |
| 32643 | 马赛 | 小儿泌尿外科、小儿外科、鞘膜积液日间手术 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32643.html |
| 32642 | 欧阳可育 | 小儿泌尿外科、小儿外科、鞘膜积液日间手术 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32642.html |
| 32487 | 劳伟华 | 小儿泌尿外科、鞘膜积液日间手术 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32487.html |
| 32740 | 张协武 | 小儿泌尿外科、小儿外科、鞘膜积液日间手术 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32740.html |
| 32644 | 罗迦耀 | 小儿泌尿外科、鞘膜积液日间手术 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32644.html |
| 32488 | 林炎坤 | 小儿泌尿外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32488.html |
| 32489 | 叶志球 | 静脉曲张、血管瘤、放射科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32489.html |
| 32490 | 陈广道 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32490.html |
| 32647 | 周真 | 儿科呼吸、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32647.html |
| 32836 | 谢梅 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32836.html |
| 32648 | 庞焕香 | 儿科呼吸、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32648.html |
| 32491 | 李增清 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32491.html |
| 32492 | 郭素华 | 儿科呼吸 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32492.html |
| 33113 | 方元龙 | 新生儿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33113.html |
| 32838 | 谭艳芳 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32838.html |
| 32493 | 林英 | 儿科呼吸、儿童过敏多学科联合 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32493.html |
| 32495 | 叶宁 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32495.html |
| 32652 | 陈圳荣 | 口腔科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32652.html |
| 32653 | 陈润哲 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32653.html |
| 32929 | 刘宏璐 | 口腔科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32929.html |
| 32496 | 黄群 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32496.html |
| 32841 | 陈宇翔 | 口腔科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32841.html |
| 32755 | 李心悦 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32755.html |
| 35080 | 刘慧华 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35080.html |
| 32654 | 周鹏 | 口腔科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32654.html |
| 32655 | 万绵佳 | 口腔科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32655.html |
| 32477 | 罗毅平 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32477.html |
| 32656 | 辛婧蕾 | 口腔科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32656.html |
| 32843 | 贺俊成 | 口腔科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32843.html |
| 32842 | 闫怡轩 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32842.html |
| 32941 | 曹行羽 | 小儿神经外科、脊柱裂脊髓栓系专病、颅缝早闭头颅畸形专病、痉挛型脑瘫SDR治疗专病 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32941.html |
| 32942 | 桂剑 | 小儿神经外科、脊柱裂脊髓栓系专病、颅缝早闭头颅畸形专病、痉挛型脑瘫SDR治疗专病 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32942.html |
| 32506 | 谭晓嫦 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32506.html |
| 32970 | 梁月梅 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32970.html |
| 32640 | 刘珊珊 | 产科、早孕关爱 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32640.html |
| 32508 | 麦碧 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32508.html |
| 32667 | 布俏雯 | 妇科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32667.html |
| 32850 | 陈永秀 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32850.html |
| 32851 | 洪小山 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32851.html |
| 33178 | 禤坚艳 | 早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33178.html |
| 33239 | 吴歆怡 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33239.html |
| 32522 | 卢家璋 | 小儿神经外科、脊柱裂脊髓栓系专病、颅缝早闭头颅畸形专病 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32522.html |
| 32672 | 胡桂英 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32672.html |
| 32917 | 张灏 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32917.html |
| 35077 | 宋匀韵 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35077.html |
| 35103 | 艾君 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35103.html |
| 32475 | 袁建章 | 内科、便民 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32475.html |
| 32668 | 周妍 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32668.html |
| 33129 | 彭燕 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33129.html |
| 32852 | 宋悦 | 妇科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32852.html |
| 32853 | 黄晓文 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32853.html |
| 32639 | 谭春玲 | 产科、早孕关爱 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32639.html |
| 32509 | 陈伟芳 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32509.html |
| 32721 | 曾曼曼 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32721.html |
| 32510 | 罗喜平 | 妇科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32510.html |
| 32998 | 黄玲 | 妇科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32998.html |
| 32937 | 何路路 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32937.html |
| 32513 | 孙小丽 | 妇科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32513.html |
| 32670 | 何少仪 | 产科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32670.html |
| 32515 | 薛素华 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32515.html |
| 34607 | 陈偲 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34607.html |
| 32516 | 孟钊 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32516.html |
| 33082 | 鲁敏 | 妇科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33082.html |
| 32671 | 伍恒英 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32671.html |
| 33264 | 李青 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33264.html |
| 32664 | 谭虎 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32664.html |
| 32535 | 许虹 | 生殖健康与不孕症科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32535.html |
| 32497 | 肖宗辉 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32497.html |
| 32503 | 翁慧男 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32503.html |
| 32504 | 张曦倩 | 生殖健康与不孕症科、生育力保存多学科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32504.html |
| 32767 | 李浩 | 生殖健康与不孕症科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32767.html |
| 32500 | 刘风华 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32500.html |
| 32848 | 陈烨 | 生殖健康与不孕症科、早孕关爱 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32848.html |
| 32882 | 黄菊 | 生殖健康与不孕症科、早孕关爱 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32882.html |
| 32661 | 王松露 | 生殖健康与不孕症科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32661.html |
| 32498 | 王芳 | 生殖健康与不孕症科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32498.html |
| 32436 | 郑毅春 | 生殖健康与不孕症科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32436.html |
| 32845 | 杜鹏 | 生殖健康与不孕症科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32845.html |
| 32501 | 汪李虎 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32501.html |
| 32502 | 董梅 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32502.html |
| 33069 | 张力佳 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33069.html |
| 32847 | 朱秀兰 | 生殖健康与不孕症科、早孕关爱 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32847.html |
| 32685 | 陈成贤 | 三叉神经痛专病 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32685.html |
| 32775 | 樊琳 | 生殖健康与不孕症科、早孕关爱 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32775.html |
| 32766 | 李湘元 | 生殖健康与不孕症科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32766.html |
| 35000 | 林镇耿 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35000.html |
| 32940 | 钟添兰 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32940.html |
| 32438 | 邓雪梅 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32438.html |
| 32783 | 马书鸽 | 中医科、中医儿科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32783.html |
| 32854 | 何田田 | 中医科、中医儿科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32854.html |
| 32676 | 郑小红 | 中医科、中医儿科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32676.html |
| 33052 | 邱少红 | 中医科、中医儿科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33052.html |
| 32784 | 张晓莹 | 中医科、中医儿科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32784.html |
| 32782 | 宋曙霞 | 中医科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32782.html |
| 33220 | 谢璐 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33220.html |
| 32686 | 陈炳豪 | 小儿骨科、小儿外科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32686.html |
| 34518 | 李恺 | 新生儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34518.html |
| 32859 | 金龙 | 小儿骨科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32859.html |
| 33127 | 袁玉美 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33127.html |
| 35035 | 罗威娜 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35035.html |
| 33044 | 张银婷 | 小儿骨科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33044.html |
| 32688 | 邓尚梁 | 康复医学科、小儿骨科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32688.html |
| 32855 | 宁静 | 儿童保健科、特需儿童预防接种咨询、入园入托体检、儿童过敏多学科联合 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32855.html |
| 32520 | 柯海劲 | 儿童保健科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32520.html |
| 32679 | 赵英 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32679.html |
| 33265 | 卢秀霞 | 儿童保健科、入园入托体检 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33265.html |
| 32857 | 刘瑛 | 儿童保健科、特需儿童预防接种咨询、入园入托体检 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32857.html |
| 32856 | 吴春艳 | 儿童保健科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32856.html |
| 32518 | 吴婕翎 | 儿童保健科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32518.html |
| 32889 | 黄维勇 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32889.html |
| 32681 | 朱然科 | 儿童保健科、特需儿童预防接种咨询、入园入托体检 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32681.html |
| 32682 | 陈小燕 | 儿童保健科、入园入托体检 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32682.html |
| 33033 | 吴亚男 | 体检科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33033.html |
| 32738 | 茹晓平 | 体检科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32738.html |
| 32860 | 魏然 | 产前诊断 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32860.html |
| 32694 | 李玲 | 产前诊断 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32694.html |
| 32804 | 朱娟 | 产前诊断 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32804.html |
| 33214 | 陈勇 | 儿科发热 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33214.html |
| 32454 | 麦明琴 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32454.html |
| 32946 | 曾莹莹 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32946.html |
| 33012 | 邓恋 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33012.html |
| 32707 | 朱晓勤 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32707.html |
| 32821 | 周真 | 皮肤性病科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32821.html |
| 33056 | 郭甜 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33056.html |
| 33028 | 刘晶 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33028.html |
| 33130 | 孙丽娟 | 普通儿科、儿科发热 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33130.html |
| 35079 | 黄珊 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35079.html |
| 33135 | 黎静 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33135.html |
| 32528 | 谢丹宇 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32528.html |
| 32944 | 胡恬 | 小儿铅中毒 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32944.html |
| 32704 | 李伟涛 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32704.html |
| 32697 | 马媛媛 | 普通儿科、小儿肾内科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32697.html |
| 32862 | 李容汉 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32862.html |
| 32863 | 陈华佳 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32863.html |
| 32864 | 黄丽林 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32864.html |
| 35105 | 祝娟 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35105.html |
| 32699 | 李敏敏 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32699.html |
| 33011 | 彭淑梅 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33011.html |
| 32556 | 黄冬平 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32556.html |
| 33006 | 陈运彬 | 普通儿科、新生儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33006.html |
| 35082 | 蔡双明 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35082.html |
| 32519 | 朱冬生 | 儿童保健科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32519.html |
| 32890 | 李新 | 乳腺科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32890.html |
| 32858 | 胡华芸 | 儿童保健科、特需儿童预防接种咨询、入园入托体检、儿童过敏多学科联合 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32858.html |
| 32861 | 彭武江 | 儿童保健科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32861.html |
| 32754 | 肖雨 | 儿童保健科、入园入托体检 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32754.html |
| 35229 | 杨致远 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35229.html |
| 32450 | 王丽敏 | 超声诊断科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32450.html |
| 32524 | 陈燕 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32524.html |
| 32895 | 闫凤英 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32895.html |
| 33027 | 周宇恒 | 产科、早孕关爱 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33027.html |
| 32530 | 李慧 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32530.html |
| 32868 | 刘丽霞 | 产科、早孕关爱 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32868.html |
| 32949 | 彭端龙 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32949.html |
| 32950 | 谢玉欢 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32950.html |
| 34859 | 刘环 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34859.html |
| 32871 | 赵君 | 产科、早孕关爱 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32871.html |
| 32708 | 杨艳 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32708.html |
| 32948 | 钟彩娟 | 早孕关爱 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32948.html |
| 33266 | 徐珍 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33266.html |
| 32880 | 马瑞霞 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32880.html |
| 32531 | 林小红 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32531.html |
| 32872 | 黎云 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32872.html |
| 32930 | 刘务贞 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32930.html |
| 32532 | 殷文静 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32532.html |
| 32499 | 刘颖 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32499.html |
| 32533 | 饶美兰 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32533.html |
| 32947 | 黄咏欣 | 产科 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32947.html |
| 33005 | 叶秀桢 | 新生儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33005.html |
| 32713 | 罗鑫刚 | 康复医学科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32713.html |
| 32622 | 原丽科 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32622.html |
| 34645 | 田松 | 新生儿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34645.html |
| 32525 | 吕成超 | 小儿外科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32525.html |
| 33014 | 王艳丽 | 新生儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33014.html |
| 32691 | 李铁 | 小儿外科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32691.html |
| 32932 | 刘佳慧 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32932.html |
| 32693 | 刘业根 | 小儿外科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32693.html |
| 32538 | 苏念军 | 生殖健康与不孕症科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32538.html |
| 32537 | 黄翠玉 | 生殖健康与不孕症科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32537.html |
| 33181 | 蓝国豪 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33181.html |
| 32849 | 齐诠 | 生殖健康与不孕症科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32849.html |
| 32873 | 农璎琦 | 生殖健康与不孕症科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32873.html |
| 32931 | 李国豪 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32931.html |
| 32714 | 罗燕群 | 生殖健康与不孕症科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32714.html |
| 32874 | 吴喜才 | 内科、便民 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32874.html |
| 32478 | 胡春玲 | 内科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32478.html |
| 32875 | 何柳瑜 | 内科、早孕关爱、便民 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32875.html |
| 32830 | 邵光 | 内科、早孕关爱、便民 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32830.html |
| 32539 | 徐金龙 | 口腔科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32539.html |
| 33101 | 李静 | 眼科、儿童过敏多学科联合 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33101.html |
| 32616 | 陈胡林 | 皮肤性病科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32616.html |
| 32954 | 肖英 | 妇科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32954.html |
| 32955 | 马芳 | 妇科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32955.html |
| 32540 | 李屹 | 妇科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32540.html |
| 32662 | 孙力 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32662.html |
| 33205 | 曾珊珊 | 妇科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33205.html |
| 32718 | 陈冰冰 | 妇科 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32718.html |
| 32710 | 李小芳 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32710.html |
| 32542 | 李智敏 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32542.html |
| 32543 | 彭秀红 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32543.html |
| 32544 | 黄彩彩 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32544.html |
| 32545 | 邓庆珊 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32545.html |
| 32719 | 赖贺 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32719.html |
| 32785 | 蔡仁燕 | 妇科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32785.html |
| 32546 | 詹新林 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32546.html |
| 32952 | 吴自如 | 口腔科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32952.html |
| 32551 | 谢芳 | 妇科 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32551.html |
| 32722 | 钟沅月 | 妇科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32722.html |
| 35084 | 张晓玲 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35084.html |
| 32547 | 江雪芳 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32547.html |
| 35085 | 杨伟健 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35085.html |
| 32732 | 骆婉婷 | 妇科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32732.html |
| 34838 | 刘盼 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34838.html |
| 35086 | 钟隽镌 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35086.html |
| 32562 | 黄晓晖 | 妇科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32562.html |
| 32879 | 丁堪铄 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32879.html |
| 32549 | 余凡 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32549.html |
| 32550 | 廖碧翎 | 妇科 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32550.html |
| 32511 | 韦相才 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32511.html |
| 34700 | 徐惠锟 | 早孕关爱 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34700.html |
| 32770 | 麦彩园 | 产科、早孕关爱 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32770.html |
| 33051 | 陈树汉 | 小儿泌尿外科、小儿外科、鞘膜积液日间手术 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33051.html |
| 32645 | 石通 | 小儿泌尿外科、鞘膜积液日间手术 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32645.html |
| 33021 | 苏晓华 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33021.html |
| 32552 | 陈嵘 | 产科、早孕关爱 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32552.html |
| 33050 | 池秀芳 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33050.html |
| 35001 | 熊文雯 | 妇科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35001.html |
| 32553 | 赵莉娜 | 产科、早孕关爱 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32553.html |
| 33187 | 吴锦华 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33187.html |
| 32960 | 徐跃心 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32960.html |
| 32977 | 王铜朗 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32977.html |
| 35068 | 陈祥楠 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35068.html |
| 32963 | 麻醉科 | 麻醉科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32963.html |
| 32437 | 赵春梅 | 妇科、中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32437.html |
| 32731 | 关心怡 | 妇科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32731.html |
| 32964 | 纪淑玲 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32964.html |
| 32730 | 胡财喜 | 中医科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32730.html |
| 32734 | 刘文娟 | 生殖健康与不孕症科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32734.html |
| 32969 | 妇科急诊 | 妇科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32969.html |
| 32994 | 曹昉欣 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32994.html |
| 33022 | 何雪仪 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33022.html |
| 32674 | 张煦 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32674.html |
| 32883 | 夏学颖 | 医学美容科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32883.html |
| 33160 | 吕杰 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33160.html |
| 35072 | 王俊平 | 新生儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35072.html |
| 32991 | 周雯 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32991.html |
| 33249 | 龙芳 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33249.html |
| 32601 | 黄千峰 | 体检科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32601.html |
| 32751 | 刘秋慧 | 眼科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32751.html |
| 32993 | 曾鑫瑶 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32993.html |
| 32690 | 曾瑶琴 | 体检科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32690.html |
| 32979 | 谭妙华 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32979.html |
| 32995 | 刘小珊 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32995.html |
| 33078 | 刘鑫鹏 | 新生儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33078.html |
| 32739 | 李子珊 | 体检科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32739.html |
| 32803 | 刘倩 | 产前诊断 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32803.html |
| 33186 | 产科急诊 | 产科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33186.html |
| 32742 | 路攀 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32742.html |
| 32997 | 邓诗婷 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32997.html |
| 32741 | 潘婉婷 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32741.html |
| 32980 | 刘敏琴 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32980.html |
| 32839 | 沈海广 | 儿科呼吸 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32839.html |
| 32905 | 董子炎 | 成人泌尿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32905.html |
| 32985 | 刘柯君 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32985.html |
| 32555 | 唐远平 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32555.html |
| 32911 | 吕颖 | 中西医结合儿科、普通儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32911.html |
| 32901 | 高文龙 | 耳鼻咽喉头颈外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32901.html |
| 32781 | 潘明沃 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32781.html |
| 32886 | 陈洽鑫 | 耳鼻咽喉头颈外科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32886.html |
| 33323 | 杨寒 | 血管瘤 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33323.html |
| 32677 | 刘翠 | 儿童保健科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32677.html |
| 32885 | 胡庆 | 口腔科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32885.html |
| 32660 | 阮建兴 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32660.html |
| 32646 | 刘运可 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32646.html |
| 32878 | 陈文芬 | 妇科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32878.html |
| 32657 | 龚照 | 生殖健康与不孕症科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32657.html |
| 32589 | 林秀 | 医疗美容科、血管瘤、医学美容科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32589.html |
| 32439 | 陈凤媚 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32439.html |
| 32603 | 高彩凤 | 眼科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32603.html |
| 32716 | 罗卓迪 | 皮肤性病科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32716.html |
| 32680 | 车頔 | 儿童保健科、特需儿童预防接种咨询、入园入托体检、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32680.html |
| 32575 | 黄亚萍 | 耳鼻咽喉头颈外科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32575.html |
| 32571 | 李帅杰 | 乳腺科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32571.html |
| 32891 | 刘嘉芬 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32891.html |
| 32892 | 向义 | 小儿外科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32892.html |
| 32581 | 肖静 | 小儿普外科、小儿肿瘤外科、小儿疝微创 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32581.html |
| 32727 | 洪淑贞 | 产科、早孕关爱 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32727.html |
| 32458 | 曾可 | 儿童内分泌遗传代谢 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32458.html |
| 32583 | 方利元 | 产前诊断、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32583.html |
| 32638 | 李晓楠 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32638.html |
| 32684 | 林惠芳 | 儿童保健科、入园入托体检 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32684.html |
| 33133 | 苏贝贝 | 儿童内分泌遗传代谢 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33133.html |
| 33064 | 方琴 | 麻醉科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33064.html |
| 32663 | 李莉 | 生殖健康与不孕症科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32663.html |
| 32840 | 李文成 | 小儿肾内科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32840.html |
| 33141 | 刘菡 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33141.html |
| 32976 | 邓超群 | 耳鼻咽喉头颈外科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32976.html |
| 33068 | 杨浩鸣 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33068.html |
| 33086 | 苏丹晨 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33086.html |
| 33018 | 张海红 | 麻醉科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33018.html |
| 32602 | 韩争争 | 小儿血液病 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32602.html |
| 32613 | 谭琪琪 | 普通儿科、儿童风湿病科 | 番禺院区、天河院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32613.html |
| 32992 | 陈晓伟 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32992.html |
| 35054 | 何景优 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35054.html |
| 32832 | 张丽 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32832.html |
| 32833 | 易菁 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32833.html |
| 32635 | 许林莉 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32635.html |
| 33013 | 莫力 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33013.html |
| 32924 | 郑丽蓉 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32924.html |
| 32933 | 李海婷 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32933.html |
| 32774 | 周睿琼 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32774.html |
| 32659 | 黄倩文 | 生殖健康与不孕症科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32659.html |
| 32689 | 卢桂贤 | 体检科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32689.html |
| 32943 | 吴碧燕 | 体检科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32943.html |
| 32636 | 周平 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32636.html |
| 32705 | 唐玲 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32705.html |
| 32698 | 鲁灵龙 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32698.html |
| 32529 | 赵聪伶 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32529.html |
| 32701 | 李丽贤 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32701.html |
| 32865 | 徐建锋 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32865.html |
| 34721 | 刘翠兰 | 儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34721.html |
| 32866 | 刘岚 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32866.html |
| 32702 | 徐海南 | 普通儿科、儿科发热 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32702.html |
| 32464 | 高薇薇 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32464.html |
| 32876 | 石婧 | 皮肤性病科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32876.html |
| 32757 | 张洋洋 | 乳腺科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32757.html |
| 32867 | 付亚林 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32867.html |
| 35100 | 王林淦 | 普通儿科、小儿内科神经内科 | 天河院区、番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35100.html |
| 33016 | 聂碧林 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33016.html |
| 35098 | 孙铭佩 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35098.html |
| 32665 | 王媛媛 | 生殖健康与不孕症科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32665.html |
| 32615 | 余楚岚 | 康复医学科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32615.html |
| 32703 | 吴巧 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32703.html |
| 33017 | 王昀 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33017.html |
| 33257 | 杨小敏 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33257.html |
| 33244 | 何琼 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33244.html |
| 32700 | 郑少章 | 儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32700.html |
| 33112 | 丁辉阳 | 新生儿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33112.html |
| 35092 | 卢启明 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35092.html |
| 32711 | 欧阳菲 | 产科、早孕关爱 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32711.html |
| 32649 | 王亚曙 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32649.html |
| 33087 | 孙艺娟 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33087.html |
| 32915 | 张儒森 | 疼痛科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32915.html |
| 33060 | 黄彩霞 | 麻醉科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33060.html |
| 33208 | 潘汝涛 | 小儿骨科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33208.html |
| 33034 | 漆冬梅 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33034.html |
| 33099 | 周易 | 体检科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33099.html |
| 32687 | 朱海鹏 | 小儿骨科、小儿外科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32687.html |
| 32750 | 何裕 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32750.html |
| 32723 | 卢颖 | 妇科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32723.html |
| 33202 | 杨小乐 | 儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33202.html |
| 32611 | 郑涵 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32611.html |
| 32772 | 李碧云 | 普通儿科、小儿内科神经内科 | 天河院区、番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32772.html |
| 33025 | 陈秋蓉 | 儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33025.html |
| 33070 | 贺牡丹 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33070.html |
| 32706 | 李海洋 | 麻醉科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32706.html |
| 33059 | 杨亮 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33059.html |
| 34897 | 潘乐乐 | 早孕 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34897.html |
| 33074 | 黄微 | 麻醉科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33074.html |
| 32709 | 乐珍 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32709.html |
| 32811 | 欧燕兰 | 妇女保健科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32811.html |
| 32696 | 李素丽 | 普通儿科、儿科发热 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32696.html |
| 32898 | 邓贵华 | 妇女保健科、药学、40+女性健康 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32898.html |
| 33038 | 王海彦 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33038.html |
| 34572 | 刘慧 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34572.html |
| 33209 | 田碧霞 | 普通儿科、儿童风湿病科 | 番禺院区、天河院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33209.html |
| 32527 | 钟燕芳 | 产前诊断 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32527.html |
| 33184 | 田莹莹 | 普通儿科、儿科发热 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33184.html |
| 33111 | 段姣 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33111.html |
| 32637 | 贺丽荣 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32637.html |
| 32844 | 徐丽清 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32844.html |
| 32630 | 涂莹 | 儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32630.html |
| 33243 | 吕金芳 | 中医科、中医儿科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33243.html |
| 32614 | 伍苑宾 | 普通儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32614.html |
| 32521 | 郭勇 | 儿童保健科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32521.html |
| 33002 | 陈常贤 | 儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33002.html |
| 32936 | 赵秋仪 | 妇科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32936.html |
| 33154 | 李远雄 | 儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33154.html |
| 32633 | 段红丽 | 产科、早孕关爱 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32633.html |
| 33102 | 金文艳 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33102.html |
| 35104 | 叶燕彬 | 儿童保健科、入园入托体检 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35104.html |
| 33015 | 杜惠莹 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33015.html |
| 32884 | 王柱 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32884.html |
| 32869 | 陈雅颂 | 产科、早孕关爱 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32869.html |
| 32965 | 蒋东丽 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32965.html |
| 32837 | 赵慧 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32837.html |
| 32683 | 梁德懿 | 儿童保健科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32683.html |
| 32590 | 叶媛 | 医疗美容科、血管瘤、医学美容科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32590.html |
| 32743 | 费佳裕 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32743.html |
| 35099 | 张嘉雯 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35099.html |
| 32816 | 任建兵 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32816.html |
| 32764 | 戴慧敏 | 中西医结合儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32764.html |
| 32921 | 陈小莹 | 产科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32921.html |
| 32573 | 邓梦夏 | 耳鼻咽喉头颈外科、儿童过敏性鼻炎 | 天河院区、番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32573.html |
| 33092 | 郭梓君 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33092.html |
| 32536 | 易艳红 | 生殖健康与不孕症科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32536.html |
| 32846 | 姚俐 | 生殖健康与不孕症科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32846.html |
| 33007 | 刘颖 | 新生儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33007.html |
| 32724 | 徐丽群 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32724.html |
| 32465 | 张春一 | 新生儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32465.html |
| 35034 | 梁树 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35034.html |
| 32632 | 孙博 | 儿科消化、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32632.html |
| 33055 | 付锐剑 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33055.html |
| 35070 | 吕莉娟 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35070.html |
| 33010 | 许露 | 新生儿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33010.html |
| 32619 | 刘颖兴 | 小儿胸外科、小儿胸壁筛查 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32619.html |
| 32918 | 彭苏珺 | 产科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32918.html |
| 32673 | 杨晨露 | 产科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32673.html |
| 32658 | 张倩玉 | 生殖健康与不孕症科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32658.html |
| 32517 | 刘婷艳 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32517.html |
| 32695 | 余莉 | 儿童保健科、特需儿童预防接种咨询、入园入托体检、儿童过敏多学科联合 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32695.html |
| 32678 | 邓钰红 | 儿童保健科、入园入托体检 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32678.html |
| 32560 | 邓文 | 毒物检验室 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32560.html |
| 32606 | 张晓明 | 眼科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32606.html |
| 32712 | 陈婷 | 耳鼻咽喉头颈外科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32712.html |
| 33270 | 郭丽萍 | 乳腺科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33270.html |
| 32582 | 周林 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32582.html |
| 32725 | 梁萌梦 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32725.html |
| 35081 | 陈露雨 | 内科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35081.html |
| 33065 | 陈佩玲 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33065.html |
| 34682 | 彭玲莉 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34682.html |
| 32906 | 施然 | 医疗美容科、医学美容科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32906.html |
| 32813 | 赵欢欢 | 眼科、儿童过敏多学科联合 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32813.html |
| 33024 | 丁茸 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33024.html |
| 35097 | 李明洁 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35097.html |
| 33061 | 吴佳瑶 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33061.html |
| 35106 | 林颖仪 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35106.html |
| 33121 | 姜欣怡 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33121.html |
| 32966 | 张璐璐 | 40+女性健康 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32966.html |
| 35087 | 邹静静 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35087.html |
| 32912 | 孙艳秋 | 康复医学科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32912.html |
| 32902 | 唐珮瑜 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32902.html |
| 32641 | 鲍俏 | 小儿泌尿外科、小儿外科、鞘膜积液日间手术 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32641.html |
| 32715 | 操日亮 | 小儿骨科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32715.html |
| 32945 | 张敏 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32945.html |
| 33103 | 刘璐 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33103.html |
| 33131 | 温俊坚 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33131.html |
| 33204 | 黄原昕 | 妇科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33204.html |
| 32900 | 梁天浩 | 耳鼻咽喉头颈外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32900.html |
| 32720 | 杜重洋 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32720.html |
| 32939 | 王伟嘉 | 妇科、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32939.html |
| 34871 | 刘磊 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34871.html |
| 32692 | 陈煜 | 小儿疝微创、小儿外科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32692.html |
| 32967 | 谭晓琪 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32967.html |
| 33183 | 柯宇媚 | 口腔科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33183.html |
| 33093 | 缪佳予 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33093.html |
| 32588 | 张恒山 | 中西医结合儿科、儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32588.html |
| 32650 | 郑泽吟 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32650.html |
| 32956 | 孙钰玮 | 妇科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32956.html |
| 33020 | 杨威 | 内科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33020.html |
| 33110 | 马炜峻 | 小儿泌尿外科、鞘膜积液日间手术 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33110.html |
| 32968 | 李善昌 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32968.html |
| 32961 | 陈明维 | 产科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32961.html |
| 32959 | 邓应君 | 产科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32959.html |
| 32627 | 黎伟健 | 内科、早孕关爱、便民 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32627.html |
| 32913 | 田晨 | 皮肤性病科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32913.html |
| 34606 | 文泳欣 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34606.html |
| 33156 | 郭洪良 | 内科、早孕关爱、便民 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33156.html |
| 33031 | 梁健女 | 儿科消化、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33031.html |
| 32916 | 庄泽钦 | 疼痛科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32916.html |
| 32737 | 段顺艳 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32737.html |
| 33047 | 张杰 | 康复医学科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33047.html |
| 33120 | 王楚杰 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33120.html |
| 32958 | 张怡奎 | 小儿泌尿外科、小儿外科、鞘膜积液日间手术 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32958.html |
| 34981 | 马冬菊 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34981.html |
| 32974 | 李雨菲 | 口腔科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32974.html |
| 32903 | 刘梅玉 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32903.html |
| 32666 | 欧阳斌 | 生殖健康与不孕症科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32666.html |
| 32448 | 柴成伟 | 小儿普外科、小儿肿瘤外科、小儿黄疸外科、小儿便秘外科、小儿疝微创 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32448.html |
| 32523 | 贺振华 | 小儿神经外科、脊柱裂脊髓栓系专病、颅缝早闭头颅畸形专病、痉挛型脑瘫SDR治疗专病 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32523.html |
| 32953 | 何佳珊 | 口腔科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32953.html |
| 32776 | 许伟滨 | 心脏中心 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32776.html |
| 32925 | 张彦 | 遗传病专科诊疗 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32925.html |
| 32926 | 丁红珂 | 遗传病专科诊疗 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32926.html |
| 32934 | 王鑫瑶 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32934.html |
| 32927 | 齐一鸣 | 遗传病专科诊疗 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32927.html |
| 32928 | 卢建 | 遗传病专科诊疗 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32928.html |
| 32563 | 冯长征 | 放射科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32563.html |
| 33037 | 缪勤飞 | 小儿内科神经内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33037.html |
| 32758 | 曾子纯 | 乳腺科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32758.html |
| 33253 | 高月华 | 早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33253.html |
| 32778 | 任竹潇 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32778.html |
| 33042 | 肖焕舜 | 内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33042.html |
| 32962 | 蔡诗琴 | 产科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32962.html |
| 35847 | 刘庚英 | 新生儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35847.html |
| 32909 | 张益阳 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32909.html |
| 32935 | 夏菁 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32935.html |
| 33188 | 梁国宽 | 体检科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33188.html |
| 33185 | 梁诗琪 | 妇科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33185.html |
| 32467 | 黄水清 | 新生儿科、普通儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32467.html |
| 32975 | 温锦尚 | 口腔科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32975.html |
| 32910 | 尹钊红 | 妇女保健科、妇科、更年期、40+女性健康 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32910.html |
| 32818 | 张晓红 | 普通儿科、小儿血液病、小儿地中海贫血、血友病专病、小儿肿瘤内科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32818.html |
| 33057 | 黄健雄 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33057.html |
| 33066 | 薛玉欣 | 妇科 | 越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33066.html |
| 33041 | 陈雪莲 | 妇科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33041.html |
| 33097 | 余东玲 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33097.html |
| 35083 | 梁润强 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35083.html |
| 32735 | 韦锦燕 | 生殖健康与不孕症科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32735.html |
| 33043 | 胡思涛 | 耳鼻咽喉头颈外科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33043.html |
| 33134 | 何裕 | 体检科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33134.html |
| 33182 | 邓惠诗 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33182.html |
| 33081 | 袁静敏 | 疼痛科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33081.html |
| 33100 | 姚仲伟 | 新生儿科、普通儿科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33100.html |
| 33109 | 程雪飞 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33109.html |
| 33058 | 严隆丽 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33058.html |
| 33149 | 宗云 | 妇女保健科、妇科、更年期、40+女性健康 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33149.html |
| 32736 | 杨淑梅 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32736.html |
| 33176 | 王建勋 | 眼科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33176.html |
| 33175 | 张旭 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33175.html |
| 32651 | 何威 | 小儿肾内科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32651.html |
| 33191 | 郑婕 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33191.html |
| 33210 | 戢婷 | 心理科、脑机接口睡眠中心 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33210.html |
| 33155 | 李芷茵 | 口腔科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33155.html |
| 33211 | 黄洁平 | 心理科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33211.html |
| 33212 | 刘慧娟 | 心理科、脑机接口睡眠中心 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33212.html |
| 35102 | 康朦梦 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35102.html |
| 32763 | 陆文聪 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32763.html |
| 33218 | 刘王凯 | 儿科呼吸、普通儿科、儿童过敏多学科联合 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33218.html |
| 33219 | 马颖 | 儿童保健科、儿童过敏多学科联合 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33219.html |
| 33237 | 钟庆涛 | 小儿泌尿外科、小儿外科、鞘膜积液日间手术 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33237.html |
| 33241 | 赵红杰 | 普通儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33241.html |
| 33023 | 谢露露 | 儿科呼吸 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33023.html |
| 33190 | 姚逸峰 | 口腔科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33190.html |
| 33246 | 张永桃 | 普通儿科、儿科发热 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33246.html |
| 33272 | 杨云舒 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33272.html |
| 34896 | 阳柳 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34896.html |
| 33245 | 吴青华 | 儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33245.html |
| 34664 | 李超迪 | 血管瘤 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34664.html |
| 34705 | 徐银玉 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34705.html |
| 34720 | 吴淑莲 | 医疗美容科、医学美容科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34720.html |
| 34783 | 卢洁仪 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34783.html |
| 34857 | 廖裕兴 | 口腔科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34857.html |
| 34858 | 杨朝湘 | 放射科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34858.html |
| 32773 | 裴铮 | 儿科、小儿内科神经内科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32773.html |
| 34860 | 廖燕玲 | 口腔科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34860.html |
| 34874 | 彭妍童 | 口腔科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34874.html |
| 32746 | 李健梅 | 公卫科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32746.html |
| 34856 | 刘丹 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34856.html |
| 34875 | 周钦浩 | 口腔科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34875.html |
| 32887 | 麦建彩 | 公卫科、体检科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32887.html |
| 34873 | 谭雨欣 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34873.html |
| 32747 | 梁柳仙 | 公卫科、体检科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32747.html |
| 35128 | 黄婷 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35128.html |
| 32733 | 张华明 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32733.html |
| 34914 | 缪定标 | 口腔科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34914.html |
| 32557 | 罗小琴 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32557.html |
| 34935 | 刘惠 | 心脏中心 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34935.html |
| 32749 | 王春艳 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32749.html |
| 34978 | 王瑞青 | 儿科消化 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34978.html |
| 32978 | 谢禹 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32978.html |
| 34980 | 凌皓 | 中医科、儿童过敏多学科联合 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34980.html |
| 32888 | 朱素婧 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32888.html |
| 35049 | 文笛 | 医疗美容科、医学美容科 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35049.html |
| 35053 | 易爱文 | 康复医学科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35053.html |
| 33159 | 陕萌萌 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33159.html |
| 35078 | 罗辉 | 麻醉科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35078.html |
| 33242 | 陈霞 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33242.html |
| 35127 | 李诗韵 | 儿童保健科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35127.html |
| 34892 | 刁雨菁 | 妇科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34892.html |
| 35225 | 刘泳如 | 营养科、产科、体重管理、儿童过敏多学科联合 | 番禺院区、越秀院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35225.html |
| 33079 | 冯阳春 | 内科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33079.html |
| 35228 | 王万鹏 | 口腔科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35228.html |
| 35245 | 罗芳梅 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35245.html |
| 32753 | 姚少敏 | 儿童保健科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32753.html |
| 35252 | 唐茂兴 | 生殖健康与不孕症科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35252.html |
| 33122 | 欧爱华 | 儿童保健科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33122.html |
| 35255 | 黄启威 | 小儿神经外科、脊柱裂脊髓栓系专病 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35255.html |
| 33096 | 黄朝阳 | 耳鼻咽喉头颈外科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33096.html |
| 35284 | 曹颖璇 | 医疗美容科、医学美容科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35284.html |
| 33036 | 郭志鹏 | 儿科发热 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33036.html |
| 34915 | 莫镜 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34915.html |
| 35305 | 管小念 | 产科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35305.html |
| 32981 | 赵新月 | 乳腺科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32981.html |
| 35318 | 吴伟晴 | 普通儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35318.html |
| 33067 | 李幼雪 | 乳腺科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33067.html |
| 35330 | 杨凡 | 医疗美容科、医学美容科 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35330.html |
| 32982 | 禤嘉明 | 中医科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32982.html |
| 35361 | 张奕纯 | 小儿普外科、小儿肿瘤外科、小儿外科、小儿疝微创 | 番禺院区、天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35361.html |
| 32983 | 杨鸿 | 中医科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32983.html |
| 35402 | 黄恩然 | 口腔科 | 番禺院区、越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35402.html |
| 32984 | 周浩 | 中医科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32984.html |
| 35419 | 曾译墨 | 产前诊断、早孕关爱 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35419.html |
| 35496 | 李美霞 | 儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35496.html |
| 32986 | 黄如湘 | 中医科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32986.html |
| 35687 | 赵磊 | 小儿泌尿外科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35687.html |
| 32987 | 刘源杰 | 中医科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32987.html |
| 35709 | 胡祖荣 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35709.html |
| 32988 | 陈奕莹 | 中医科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32988.html |
| 35711 | 黄思敏 | 中医科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35711.html |
| 32989 | 赖美娴 | 中医科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32989.html |
| 35731 | 黄泳仪 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35731.html |
| 32759 | 陈运聪 | 小儿外科、外科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32759.html |
| 35101 | 陶珮 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35101.html |
| 35815 | 黄伟坚 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35815.html |
| 32990 | 李婷 | 小儿外科、暑假包皮 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32990.html |
| 35816 | 杨世辉 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35816.html |
| 33094 | 陆嘉杰 | 小儿外科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33094.html |
| 35817 | 涂艳萍 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35817.html |
| 32577 | 李鹏 | 小儿外科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32577.html |
| 35818 | 潘云祥 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35818.html |
| 32761 | 周斌 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32761.html |
| 35822 | 刘金凤 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35822.html |
| 32558 | 王淑珍 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32558.html |
| 35477 | 廖海玲 | 儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35477.html |
| 35756 | 林曼敏 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35756.html |
| 35844 | 周梦园 | 药学 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35844.html |
| 32559 | 韩颖 | 儿科、身高管理 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32559.html |
| 32728 | 黎玉涵 | 妇科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32728.html |
| 35755 | 孔泳婷 | 麻醉科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35755.html |
| 32893 | 文元义 | 儿科、儿科消化 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32893.html |
| 33177 | 魏良铜 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33177.html |
| 34573 | 张海迪 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34573.html |
| 34936 | 李月 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34936.html |
| 34952 | 王桃 | 儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34952.html |
| 33179 | 胡彩兰 | 体检科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33179.html |
| 32768 | 王智琴 | 皮肤性病科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32768.html |
| 32894 | 刘丽娜 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32894.html |
| 32748 | 周金婵 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32748.html |
| 32896 | 吴志君 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32896.html |
| 32870 | 段冬梅 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32870.html |
| 34934 | 潘秀芹 | 产科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34934.html |
| 32561 | 郜红艺 | 病理科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32561.html |
| 32567 | 王穗琼 | 药学咨询 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32567.html |
| 32899 | 王铁桥 | 儿童咳喘药学服务、儿科药学 | 天河院区、番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32899.html |
| 32564 | 陈俊柱 | 骨科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32564.html |
| 34949 | 廖嘉炜 | 骨科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34949.html |
| 32585 | 唐卉 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32585.html |
| 33029 | 钟丽英 | 中西医结合儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33029.html |
| 32996 | 王际晴 | 新生儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32996.html |
| 34570 | 萧国良 | 新生儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34570.html |
| 34931 | 郭庆禄 | 乳腺疾病影像学诊断 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34931.html |
| 34810 | 杨洋 | 儿科、新生儿科 | 清远院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34810.html |
| 35107 | 邹新飞 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35107.html |
| 35108 | 杨文钊 | 官网详情未标注 | 官网详情未标注 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35108.html |
| 33247 | 钟迪 | 儿科 | 越秀院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33247.html |
| 34811 | 郑璇儿 | 新生儿科 | 天河院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34811.html |
| 33084 | 梁姗姗 | 康复医学科 | 番禺院区 | 详情已读取 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33084.html |

### 51 个非医生候选逐 ID 排除表

| 详情 ID | 名称 | 列表身份 | 来源链接 | 排除理由 |
|---|---|---|---|---|
| 33000 | 乳腺专科门诊 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33000.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35596 | 产前诊断手术号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35596.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35597 | 免费产前筛查发券号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35597.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35071 | 名医工作室 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35071.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33153 | Z双胎多胎门诊 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33153.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35166 | 杨东新主任团队号 | 副主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35166.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32779 | 管理员 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32779.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35076 | 双胎多胎门诊 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35076.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35599 | 日间门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35599.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35598 | 宫腔镜专用号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35598.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35603 | 免费产前筛查及诊断号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35603.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32780 | 续费专用号 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32780.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35594 | 妇科手术号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35594.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32999 | P双胎多胎门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32999.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32938 | 盆底筛查咨询 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32938.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35088 | 罕见病会诊号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35088.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35089 | test123 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35089.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35091 | 中医治疗号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35091.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35093 | 手术咨询号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35093.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35094 | 妇科计生门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35094.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35095 | 盘底筛查治疗 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35095.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32566 | 系统管理员-正式库 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32566.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35096 | 儿科义诊医生 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35096.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32576 | 脱敏注射号 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32576.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32914 | 急诊号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32914.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35686 | 产前诊断专科医生 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35686.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35604 | 治疗号(开单专用) | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35604.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 34770 | 多科会诊号 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34770.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33001 | 助孕贴专用号 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33001.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35090 | 口腔保健号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35090.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32455 | 尹爱华名医工作室 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32455.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35050 | 鼻炎专科号 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35050.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 34732 | 中医针灸美容及减重专科号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34732.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35055 | 内分泌及肥胖中西医结合号 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35055.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35601 | 日间手术评估及术后随访 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35601.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35066 | 卵巢功能减退门诊 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35066.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32971 | 发热门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32971.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33286 | 生育力保存免费咨询医生 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33286.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33326 | 盆底磁治疗预约 | 医士 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33326.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 34678 | 续费医生 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34678.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35600 | 宫腔镜手术号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35600.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35602 | 日间手术门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35602.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35730 | 口腔科急诊号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35730.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 32897 | F双胎多胎门诊 | 副主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32897.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33269 | 早孕专科号 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33269.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35476 | 早孕门诊 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35476.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 33271 | 专科医生 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33271.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35109 | 中医简易门诊 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35109.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35110 | 政府免费筛查就诊号 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35110.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| 35111 | 体重管理 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35111.html | FULL 末尾验收确认目录卡片为服务项或收费账号，排除医生画像范围 |
| 35129 | 马淑丹 | 收费 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35129.html | FULL 末尾验收确认目录卡片为服务项或收费账号，排除医生画像范围 |

### 全量采集照片命名、字节、魔数、SHA-256 与尺寸对照

| 姓名 | 科室 | 主职称 | 文件名 | 字节数 | 宽×高 | SHA-256 | 官网照片 |
|---|---|---|---|---:|---:|---|---|
| 何伟健 | 心理科 | 主任医师 | 何伟健-心理科-主任医师-广东省妇幼保健院.jpg | 7107 | 183×280 | `ca28b9543ed38297146dbf65a46c56d729910ad87196283980506d7cc02740c8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b35b9c78-e7fb-4d5f-adb3-8d573cede8e8-280.jpg |
| 于海静 | 乳腺科 | 主任医师 | 于海静-乳腺科-主任医师-广东省妇幼保健院.png | 69407 | 186×280 | `43c41214c66923993a12aaf6ceee64ce22c0dfab8eb326bd1b459651012638a5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c1b1b777-1578-4b3e-ba0c-d1e326345b7f-280.png |
| 王永南 | 乳腺科 | 主任医师 | 王永南-乳腺科-主任医师-广东省妇幼保健院.png | 113871 | 220×280 | `366f723f678b3ba1e5487fd2443c3fdcd2cfeeb8338ebe25c98ed575d6c536b2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/47a0f8f8-8915-47f0-bcfe-b6acb13e9f3b-280.png |
| 邹素文 | 乳腺科 | 主治医师 | 邹素文-乳腺科-主治医师-广东省妇幼保健院.png | 66540 | 184×280 | `0e398282f5cf3ed9b1af7d55a53e23079cb508994d43202366cdd95ed609f844` | https://wx.e3861.com/sfyAdmin/Images/Doctor/94c1bdcd-5b56-45a9-b9ad-06b3e6ad174e-280.png |
| 朱彩霞 | 乳腺科 | 主任医师 | 朱彩霞-乳腺科-主任医师-广东省妇幼保健院.jpg | 7018 | 210×280 | `bfdf8c0c14ae96b7d2e72641509a7ebff7a43195ca77b1f6c6cc4b916c41ffb3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/756c1a97-4c18-455d-8db4-3f23262cbef7-280.jpg |
| 余海云 | 乳腺科 | 主任医师 | 余海云-乳腺科-主任医师-广东省妇幼保健院.jpg | 5763 | 187×280 | `51c59f1666ce90831e1b93483aaa8c26061447a20652c907dbd0c2e96b8be613` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e70f2d89-466a-4be1-9a6a-9f91c0779398-280.jpg |
| 李文萍 | 乳腺科 | 主任医师 | 李文萍-乳腺科-主任医师-广东省妇幼保健院.png | 76443 | 185×280 | `e3b0a1cc72ba61876a749f92607177a68579a72a95b997cb93fb94f0ebbc3d1d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f5b379df-5903-4c8d-80fa-d80866a7e850-280.png |
| 万舰 | 乳腺科 | 主任医师 | 万舰-乳腺科-主任医师-广东省妇幼保健院.png | 65704 | 184×280 | `bc7d70ae4931205e278d831d3dec2d6063f3bfd98777f39e4945afa063fe7b2a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/906be956-73ae-4caa-b5bf-8654dcac0886-280.png |
| 张安秦 | 乳腺科 | 主任医师 | 张安秦-乳腺科-主任医师-广东省妇幼保健院.png | 68716 | 186×280 | `c9f604942bd676de880ac4148778b950bad45e3f8f88a24a6574be1816db258a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/cb483995-d716-4e12-b4b4-b7360efae4c9-280.png |
| 陈中扬 | 乳腺科 | 主任医师 | 陈中扬-乳腺科-主任医师-广东省妇幼保健院.png | 104144 | 204×280 | `57d36b5c6c51be771ffcd17d8e35bc474b4444a56c04a085a0a3841bbb17a2ba` | https://wx.e3861.com/sfyAdmin/Images/Doctor/981d429b-91c9-4385-8b0e-03f8ef77a610-280.png |
| 罗懿忠 | 乳腺科 | 主任医师 | 罗懿忠-乳腺科-主任医师-广东省妇幼保健院.png | 66202 | 183×280 | `116402af6ab444bf1aca0912707fa489e6165edf93c5a15f75e9ed7d6ad998d2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c5f901db-c48d-4e2a-9015-94f3254ac79f-280.png |
| 连臻强 | 乳腺科 | 主任医师 | 连臻强-乳腺科-主任医师-广东省妇幼保健院.jpg | 6092 | 199×280 | `5dab1549f9b74c48e4f2df66a209a3756a7aa20957ae4e7c357267d0a8d38f26` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9c362037-86fc-43bf-9056-9a0433f60a2c-280.jpg |
| 杨剑敏 | 乳腺科 | 主任医师 | 杨剑敏-乳腺科-主任医师-广东省妇幼保健院.png | 71554 | 202×280 | `0099d11622ec153340de7dbf59e9b34cd7141e049793299d50e25d355739b5bb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b60ba30c-eb13-4b70-8110-91cc8e682ffe-280.png |
| 谢四梅 | 乳腺科 | 主治医师 | 谢四梅-乳腺科-主治医师-广东省妇幼保健院.jpg | 6468 | 187×280 | `3c86142277b4e2cb19732a90114dc80a7fb32f0215337894833b44e5a52f19dd` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ce71a649-2800-443d-b8ca-258055b425c7-280.jpg |
| 许娟 | 乳腺科 | 主任医师 | 许娟-乳腺科-主任医师-广东省妇幼保健院.jpg | 5917 | 179×280 | `2228f0b27a1c6df28f200761993b1e7dc46fd2601362a82ccae30ec43dc32faf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5eb18238-9d12-4409-9a2e-65199c69e253-280.jpg |
| 邱桂霞 | 小儿肾内科 | 主治医师 | 邱桂霞-小儿肾内科-主治医师-广东省妇幼保健院.png | 65455 | 185×280 | `9b9e7d305de421ba80261bd1a6e5124b7084ac40aeb56009c02f879e0e3d80ea` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e28928ba-0363-40c0-814e-5be8b315a98b-280.png |
| 王伟光 | 普通儿科 | 主任医师 | 王伟光-普通儿科-主任医师-广东省妇幼保健院.jpg | 6875 | 222×280 | `fadd363eca21a9c5fd043a77970ffd327a6e67a6661e2299e632d9efc9a37793` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a46b74ff-438b-4b73-bb64-3710904f1589-280.jpg |
| 肖梦加 | 乳腺科 | 主治医师 | 肖梦加-乳腺科-主治医师-广东省妇幼保健院.png | 70973 | 186×280 | `d453a63783d7a1d9908701c76c9e4015a64c473a633df1e3609a758d0d8b4df8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/57447a30-ade5-4dd7-96a2-40b2d0171032-280.png |
| 郭莉 | 产前诊断 | 主任医师 | 郭莉-产前诊断-主任医师-广东省妇幼保健院.png | 48073 | 187×280 | `a37943764384f4daf352343c60f645edeff2f7ae381030d20af4e09db28bbc70` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7c44c8d9-1f68-498a-a0d4-b993600319f2-280.png |
| 饶腾子 | 产前诊断 | 主任医师 | 饶腾子-产前诊断-主任医师-广东省妇幼保健院.png | 54072 | 187×280 | `a5faa787e9cf4568744d74761a7decf45cc6e8507bf790485be7af13a1e8deb6` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fa7ee400-e377-41a2-991b-efe9dae69d89-280.png |
| 李陈 | 产前诊断 | 主治医师 | 李陈-产前诊断-主治医师-广东省妇幼保健院.png | 46625 | 187×280 | `44cc32fc4bca33008e8f86e98fa864da0fb8ed57fd1924abdcc484333339be3e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/45dfdd60-b2d0-4496-9775-17e115fb006b-280.png |
| 吴菁 | 产前诊断 | 主任医师 | 吴菁-产前诊断-主任医师-广东省妇幼保健院.png | 40992 | 187×280 | `ee88756e67a3b5b05121f3891914f780611c81daf29ee8e1ebaf2d06cbd69796` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3ccbde63-1107-4216-9b6c-223b9aea02d2-280.png |
| 尹爱华 | 产前诊断 | 主任医师 | 尹爱华-产前诊断-主任医师-广东省妇幼保健院.png | 42710 | 187×280 | `4b746510e62971da54f9fb72100a72667e6ec524c9f32103c03b6ea25a4af3a0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ae33b8ca-1f83-4cdf-b319-4e3802c67f9b-280.png |
| 李静姝 | 产前诊断 | 医师 | 李静姝-产前诊断-医师-广东省妇幼保健院.png | 54587 | 187×280 | `70dcff476db0595e4df618cbd7f9f0d484650ce84b53454dcbcf9b8d6dcf119f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ac2e66c0-08a9-4a8b-a242-2c701e3a104d-280.png |
| 何薇 | 产前诊断 | 主任医师 | 何薇-产前诊断-主任医师-广东省妇幼保健院.png | 48314 | 187×280 | `97aafd2a0033b5b65fd1db5835a79169e68f47c80fa85e6619903b20fd5d07ba` | https://wx.e3861.com/sfyAdmin/Images/Doctor/49676140-efdb-4f2f-a1cb-ccd6f3d6d271-280.png |
| 石晓梅 | 产前诊断 | 主任医师 | 石晓梅-产前诊断-主任医师-广东省妇幼保健院.png | 53608 | 187×280 | `f3dfc2a5989f210231dd3a1a3ede4554a5268b0f191897dd8f5b072b32edc988` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7d243117-bbd5-48b5-9f8a-c77236193a72-280.png |
| 杜丽 | 产前诊断 | 主任医师 | 杜丽-产前诊断-主任医师-广东省妇幼保健院.png | 65073 | 240×280 | `a999a83ff59bc42efe4857ef85b53e08f9f07313ab142a3f2a392ebc96e52dd9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7677aac1-03a1-465c-b4e9-bdf0d81e6cfd-280.png |
| 熊盈 | 产前诊断 | 主任医师 | 熊盈-产前诊断-主任医师-广东省妇幼保健院.png | 41737 | 187×280 | `1fe74b66406adf69bdfd65f5790bd6a15365362355ac3ff6af7b953203211b1c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c7b01743-fb7f-49c0-84fa-5259e703d41e-280.png |
| 赵馨 | 产前诊断 | 主任医师 | 赵馨-产前诊断-主任医师-广东省妇幼保健院.png | 48965 | 187×280 | `b100398a0808ad87d6a6f4ddaf7786c8012cc126eec3d7fe5fee8f2b353fe28a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/edc1e70a-cfb8-4062-892d-23e2257f5644-280.png |
| 黄艺文 | 小儿普外科 | 主治医师 | 黄艺文-小儿普外科-主治医师-广东省妇幼保健院.jpg | 8063 | 210×280 | `8da4e6cccfdf2fef3d8bb9f8c3351c78d8a2a3e4b74b50f91fe276529786de6a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/03d9b700-1c11-47e2-83ea-d571e0522bf5-280.jpg |
| 王逾男 | 产前诊断 | 主治医师 | 王逾男-产前诊断-主治医师-广东省妇幼保健院.png | 50578 | 187×280 | `50b5ee2c3208d13d75bf83b3084f4460027eb77d21a18e0603ae4e640475cad8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f3c55f1f-507e-46c3-b8c4-5471a31446ce-280.png |
| 李刚龙 | 小儿普外科 | 主治医师 | 李刚龙-小儿普外科-主治医师-广东省妇幼保健院.jpg | 7555 | 225×280 | `afb32b32249c0d37cfba0023a2e000e36064a2290c86696c1ffa7db41e4bb910` | https://wx.e3861.com/sfyAdmin/Images/Doctor/cf4affc2-2522-41b8-9eec-06f1842c346a-280.jpg |
| 董踌 | 小儿外科 | 主治医师 | 董踌-小儿外科-主治医师-广东省妇幼保健院.jpg | 5507 | 210×280 | `c48b939d744ee0bcf788ba4dfe57e7225ff44da5bd35c45233d56e3871ce1d87` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c705bb96-1a57-4da0-b589-d991d742a2a4-280.jpg |
| 岑龙 | 小儿普外科 | 主治医师 | 岑龙-小儿普外科-主治医师-广东省妇幼保健院.jpg | 6883 | 248×280 | `cce6988742324ec712561443136003925bbe8454b1190d33ae9d8a2133e5b20b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/755e541d-1b75-4fb8-abf3-3f4753218b58-280.jpg |
| 朱小春 | 小儿普外科 | 主任医师 | 朱小春-小儿普外科-主任医师-广东省妇幼保健院.png | 69086 | 184×280 | `1bf808b1f35fc4f6de390c8bc1606e82df52aba831f17770ec01b2a2f5f3dbf9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fc1ea1b8-a3bb-43f9-bf7e-86ff86ecf77e-280.png |
| 葛午平 | 新生儿外科 | 主任医师 | 葛午平-新生儿外科-主任医师-广东省妇幼保健院.png | 68526 | 184×280 | `7efc7cb172fa1c3e3e22119bdb777225d0173372c86e11d93b7227b52467cb1d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/73f14cbb-425d-4a9c-990f-e05972723932-280.png |
| 黄白沙 | 小儿普外科 | 主治医师 | 黄白沙-小儿普外科-主治医师-广东省妇幼保健院.jpg | 8565 | 185×280 | `a3083155ff86aef6509fc1d95a73a669e370a0cf4976506bdc090d5eeadf219b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/82f3ae26-55db-49cf-9793-4167e782e8ae-280.jpg |
| 赵颖 | 麻醉科 | 主治医师 | 赵颖-麻醉科-主治医师-广东省妇幼保健院.png | 49640 | 187×280 | `008fb033aa0db72c6b69e098c649677f693c008100ed675e408a8fd4c7a3d9c7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e77b957a-2474-41a0-9f43-28cdd08226b0-280.png |
| 张心丽 | 耳鼻咽喉头颈外科 | 主任医师 | 张心丽-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.jpg | 9645 | 280×280 | `c88334102e11ff31c9319e5fe7265676f45365afbb1fb771e0810c9b4495cc54` | https://wx.e3861.com/sfyAdmin/Images/Doctor/90c9506e-96cc-4ca6-9c38-7dd18fbfd3da-280.jpg |
| 申晓宁 | 麻醉科 | 主治医师 | 申晓宁-麻醉科-主治医师-广东省妇幼保健院.png | 69672 | 187×280 | `796bb166475a5d47342eebd7c6504cc1506e65fb9f93b1637e6ad0594972724b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a3e68dcc-cce4-49a5-8243-58352f79ed94-280.png |
| 林小燕 | 耳鼻咽喉头颈外科 | 主任医师 | 林小燕-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.jpg | 7572 | 185×280 | `00f6c22ff5d6041d95d5fc84147b49ff2629ef991d7957881cd32622e73d0176` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8d3ed5ef-df9e-4b6c-9599-71d123aba1cd-280.jpg |
| 韩宝义 | 麻醉科 | 主任医师 | 韩宝义-麻醉科-主任医师-广东省妇幼保健院.png | 49934 | 187×280 | `39242177a63d2a885235dfcd2f6da6af4b773cc2fe07f5952b25a7c86f822ea7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/110784fa-4b4a-4ea8-a720-712230431cb9-280.png |
| 赵哲成 | 耳鼻咽喉头颈外科 | 主任医师 | 赵哲成-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.jpg | 9283 | 280×280 | `15424efd9474443d23ea9c26220d89e8f665861d5350afc5ccffedb26d39cdfd` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d30cd581-4cd8-46f4-a457-96ea04e1cc39-280.jpg |
| 于菲菲 | 麻醉科 | 主治医师 | 于菲菲-麻醉科-主治医师-广东省妇幼保健院.png | 68285 | 187×280 | `37fb3878941c244d7e8d65305a277d972225ad4857c42364574413ac88b43c05` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1a6c2c27-67b4-4441-ae15-7963321f3610-280.png |
| 孙维国 | 麻醉科 | 主任医师 | 孙维国-麻醉科-主任医师-广东省妇幼保健院.png | 69792 | 187×280 | `c7d6ce9fed867e7f57035a99363fb12a4cbef0ce267cb4677553955aaaf82975` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d2782099-c3ad-49cc-ae50-46b7c12ba662-280.png |
| 刘漪 | 耳鼻咽喉头颈外科 | 主治医师 | 刘漪-耳鼻咽喉头颈外科-主治医师-广东省妇幼保健院.jpg | 8803 | 204×280 | `c4a1104e9ec599371ae4a496ebc754f69a2e183e26e39683f7cda102015c021e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7e7dc9bc-3dfa-432e-abba-5ffbbb8a0f4a-280.jpg |
| 颜小龙 | 麻醉科 | 主治医师 | 颜小龙-麻醉科-主治医师-广东省妇幼保健院.png | 70400 | 187×280 | `483c6017c2cc1e00e5ac71a1b397d9893de3e6b41c69b749e5e3518011b5afe8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9224d832-a7a9-48d6-8197-d0d515c2c88d-280.png |
| 师小径 | 耳鼻咽喉头颈外科 | 主任医师 | 师小径-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.png | 107106 | 223×280 | `e3c996f36d64e2c4b691e3c68448baf436e430417c4f3f2499116b1187e2f909` | https://wx.e3861.com/sfyAdmin/Images/Doctor/76b3c100-7010-4720-b424-ce7a6ef9ad2f-280.png |
| 陈曦 | 耳鼻咽喉头颈外科 | 主任医师 | 陈曦-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.png | 107666 | 214×280 | `a861da63f00682016b2d4fd3469a9d0f503e4f20aeb4346ca95497596893f500` | https://wx.e3861.com/sfyAdmin/Images/Doctor/81b3ea0c-6ed1-4887-bd3e-ce188b1e4c15-280.png |
| 邹宇 | 耳鼻咽喉头颈外科 | 主任医师 | 邹宇-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.jpg | 9278 | 280×280 | `5bda1cee4a1655db2ec5a49f713b87e59f339c523705793087a6e84ac25d4bd8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/57c54f45-9711-4209-95df-9ab8c77b5049-280.jpg |
| 郭良芬 | 耳鼻咽喉头颈外科 | 主任医师 | 郭良芬-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.png | 112982 | 188×280 | `087bb0651af03bcdfe4230f0f1d0146ad9e46dba9581a4b47693f61c4208be7f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fe05cb52-8bdc-4938-8f17-8e58b45e916d-280.png |
| 麦飞 | 耳鼻咽喉头颈外科 | 主任医师 | 麦飞-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.jpg | 7723 | 210×280 | `5a8fae2a82b6357ed90708da11682c5b9d4c573db49b20bd2a8584a907888de8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/271e0751-88a7-4227-aade-67686f4c7585-280.jpg |
| 李一心 | 耳鼻咽喉头颈外科 | 主治医师 | 李一心-耳鼻咽喉头颈外科-主治医师-广东省妇幼保健院.png | 104999 | 191×280 | `aed4f2df8360ab370757c5bd19492004cb49b23b7eb85a243addf1bdf93fcdc6` | https://wx.e3861.com/sfyAdmin/Images/Doctor/971b6f0d-8f0a-405a-a250-1e662fbf6f11-280.jpg |
| 冯嘉宝 | 麻醉科 | 主任医师 | 冯嘉宝-麻醉科-主任医师-广东省妇幼保健院.png | 51786 | 186×280 | `bc77d4da20c826b9796418921516ebb13fcd615b4226a81eb5038c09aab8d23f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/44657bc4-a4c1-45b3-a901-c5c31ed32851-280.png |
| 尚宁 | 未标注 | 主任医师 | 尚宁-未标注-主任医师-广东省妇幼保健院.png | 76164 | 210×280 | `9910ad807ff2efc784a6863e93c4bbf64929faa8f61206149b68102a839706dc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a610ee3e-9c40-44de-a6cc-4f8753ae22c6-280.png |
| 邹敬江 | 医疗美容科 | 主治医师 | 邹敬江-医疗美容科-主治医师-广东省妇幼保健院.jpg | 4987 | 187×280 | `e44871e05aceb1bbe8761e70da9194b0db5c4a5608485dcc1494f151eed1b98f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ede5475a-727a-4545-ae1c-84ba99bb17d1-280.jpg |
| 谭梅军 | 医疗美容科 | 主任医师 | 谭梅军-医疗美容科-主任医师-广东省妇幼保健院.jpg | 5528 | 187×280 | `8e5e75a5a28d0811e32b1bde7f21194f0c57683bd64c0333939693e9c6a77b3e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/629341dc-e1d0-4695-86e1-90111e998582-280.jpg |
| 姜金豆 | 医疗美容科 | 主任医师 | 姜金豆-医疗美容科-主任医师-广东省妇幼保健院.jpg | 7144 | 265×280 | `89c67678a1a39de2b5a769aa5814d2954b929cf55086af48898d230317f710dc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8cca34bb-6299-448c-8e9f-884b09d81d83-280.jpg |
| 孙赛 | 医学美容科 | 主治医师 | 孙赛-医学美容科-主治医师-广东省妇幼保健院.jpg | 6638 | 209×280 | `b74bdc79493775b3f85a2537889ff4772d7113251754e0b992b6369e3fa97c2a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3b1d2340-2a06-49d0-ab6e-8f61c757e539-280.jpg |
| 陈容容 | 医疗美容科 | 主任医师 | 陈容容-医疗美容科-主任医师-广东省妇幼保健院.png | 76270 | 183×280 | `5a3fef00ffcea9dbda33e3599c3fecf07a002f660ee2eb2efa3d243cd818dee8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c9f9c83c-5764-4cb2-812d-d96a3bc8c594-280.png |
| 胡葵葵 | 医疗美容科 | 主任医师 | 胡葵葵-医疗美容科-主任医师-广东省妇幼保健院.jpg | 7835 | 280×280 | `17e7f58fcd133f3891f19710ef225b873fa4154cdfd4bada28b6b01095c897cf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8c36f27f-b3ca-43a4-b010-a2527f20e86b-280.jpg |
| 潘小英 | 产前诊断 | 主任医师 | 潘小英-产前诊断-主任医师-广东省妇幼保健院.png | 46574 | 187×280 | `afe962e2c147157fea2ae53033a6b36345675e6a9ba32600b62f415ec2c2b344` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7c189ee6-6763-40bf-a606-0dafe681f282-280.png |
| 李甜甜 | 妇女保健科 | 主治医师 | 李甜甜-妇女保健科-主治医师-广东省妇幼保健院.png | 84267 | 226×280 | `af40c759edd6a54e091020d0b95a7e5cfa8df3991e7b2b377bcf6dfd30981872` | https://wx.e3861.com/sfyAdmin/Images/Doctor/66cb7c35-ce8c-427c-9c21-bd38d2f03746-280.png |
| 吕霄 | 妇女保健科 | 主任医师 | 吕霄-妇女保健科-主任医师-广东省妇幼保健院.jpg | 6343 | 199×280 | `2e82a087e111e1f8ddfc492cb32edf90d76ec634fffa1adcb953907a0859e5cb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1a2dc278-0692-46af-b7e5-f87d3a4167c3-280.jpg |
| 李丽美 | 妇女保健科 | 主任医师 | 李丽美-妇女保健科-主任医师-广东省妇幼保健院.png | 63373 | 173×280 | `df4f74cf163518b2d6d391e5de48d0edf06501bb9badf13ae0613b8d32e3ede2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4b904e0c-55a0-4acf-9825-5448e502a5e5-280.png |
| 黄雪萍 | 妇女保健科 | 主治医师 | 黄雪萍-妇女保健科-主治医师-广东省妇幼保健院.png | 77372 | 188×280 | `053477e2f8c12e779a034adac7dccc791f37c1a422b5e96f2b2b58247899609d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c84aae01-1615-4e61-81c7-60c9ce70801f-280.png |
| 夏建红 | 妇女保健科 | 主任医师 | 夏建红-妇女保健科-主任医师-广东省妇幼保健院.png | 71552 | 184×280 | `2898fa301d61d50259daa5bfd83b868256d664f15ec6f24e3abfbe17f516337c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d897cc00-3023-4bfa-ab4d-b5ffb2413bf6-280.png |
| 高奎杰 | 中西医结合儿科 | 医师 | 高奎杰-中西医结合儿科-医师-广东省妇幼保健院.jpg | 6339 | 248×280 | `d282063b82eb774947768ec35df895fa80601dec52bd56222d97c282f27b6109` | https://wx.e3861.com/sfyAdmin/Images/Doctor/287be1ee-23b0-492e-b7c2-2fd84f2e35af-280.jpg |
| 杨东新 | 中西医结合儿科 | 主任医师 | 杨东新-中西医结合儿科-主任医师-广东省妇幼保健院.jpg | 6212 | 211×280 | `64ce7b28f09248c825e8e1dfe2223e342e892ebc58b465f8e1ebccba151d8132` | https://wx.e3861.com/sfyAdmin/Images/Doctor/cc02a534-3f3a-4a19-8f05-91788a74767a-280.jpg |
| 杜岚岚 | 新生儿科 | 主任医师 | 杜岚岚-新生儿科-主任医师-广东省妇幼保健院.png | 67768 | 244×280 | `fa2836fcd11fd509ee9c7e367890778e1f21c9a91cdbb30678aadd515ef707bf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/920a1f31-9ef8-4986-ae1b-ba54390aee4b-280.jpg |
| 林健瑶 | 中西医结合儿科 | 主治医师 | 林健瑶-中西医结合儿科-主治医师-广东省妇幼保健院.jpg | 7452 | 210×280 | `ec98fedc450b9a9abbc28c0f456ffa12f0320176ae84654bb75404728d4649c0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a9866f11-4e5c-4fed-be1d-3e7f4fcb8b69-280.jpg |
| 毛武 | 甲状腺外科 | 主任医师 | 毛武-甲状腺外科-主任医师-广东省妇幼保健院.jpg | 7401 | 256×280 | `8171a18ddcf8971cf0546d2a905b3e09799c713ee5a1247d1729bb19f7a0ba76` | https://wx.e3861.com/sfyAdmin/Images/Doctor/18762b27-4202-4021-b35a-fd4bc87f7f55-280.jpg |
| 史浩 | 肛肠外科 | 主任医师 | 史浩-肛肠外科-主任医师-广东省妇幼保健院.png | 62438 | 180×280 | `0b7a57c697ca336e98486a987ae3a8fe0515ff05e5e083430e4462b8fb36429f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ce843da9-6065-4a4e-a13d-4b25492dd832-280.png |
| 邓航 | 肛肠外科 | 医师 | 邓航-肛肠外科-医师-广东省妇幼保健院.png | 76821 | 205×280 | `4b8ebb53aa5b864b7a48306cee57101fb594a7d79d52552bce1cdc62b4ac158a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/269f34dc-cb02-467c-afb9-323f1f72eff1-280.png |
| 乔平进 | 成人泌尿外科 | 主任医师 | 乔平进-成人泌尿外科-主任医师-广东省妇幼保健院.png | 61091 | 183×280 | `b1216f2997b25b92e783a7b02c00faa35b12340790f5136875ab6348e37d131e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0b22e1e7-b9af-4acb-bb9c-7801deef772a-280.png |
| 王子祥 | 甲状腺外科 | 主治医师 | 王子祥-甲状腺外科-主治医师-广东省妇幼保健院.jpg | 8014 | 280×280 | `a60f4c2f97ea3999f2fb974c6b9d9180b759a341c761ebaf8cf7cc28b8ba5e1e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1775de04-494d-4045-ae20-cf0f7643d95a-280.jpg |
| 王越 | 新生儿科 | 主任医师 | 王越-新生儿科-主任医师-广东省妇幼保健院.png | 60652 | 174×280 | `cb1793699aed1081d2b5d0bc5b3a55d4aa54f06e0f422ce6f9318bed06a42848` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a7179590-aade-46fa-880f-2435d1609c76-280.png |
| 潘碧琦 | 儿童内分泌遗传代谢 | 主任中医师 | 潘碧琦-儿童内分泌遗传代谢-主任中医师-广东省妇幼保健院.png | 61167 | 183×280 | `ff41863c68662ed3f270876509f648541584652f37a56f6042318ec9c7751f67` | https://wx.e3861.com/sfyAdmin/Images/Doctor/286ed235-7820-4cc8-8369-d7960729fafb-280.png |
| 刘舒 | 儿童内分泌遗传代谢 | 主任医师 | 刘舒-儿童内分泌遗传代谢-主任医师-广东省妇幼保健院.png | 83662 | 196×280 | `06407422735c4b129ec03938e3ff9ec3198ba06f47245885ab8de034c3383354` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8c814b38-3b52-45fc-90ae-48863bf362ee-280.jpg |
| 罗先琼 | 儿童内分泌遗传代谢 | 主任医师 | 罗先琼-儿童内分泌遗传代谢-主任医师-广东省妇幼保健院.jpg | 7336 | 261×280 | `40361208fe653c9b4d85f95e725d4a79b4b271dd4039db4bd2a2f2e18288b1bb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/98a4db94-ee77-4ef2-a466-7ff6983c0ebd-280.jpg |
| 李韵 | 儿童内分泌遗传代谢 | 主治医师 | 李韵-儿童内分泌遗传代谢-主治医师-广东省妇幼保健院.png | 69264 | 176×280 | `2621ece733432634ea73245af8fa339b96fac0a7a104f0a1be576d5a5b27e003` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a56418cf-ce6d-4c53-a3c5-9457ce658730-280.png |
| 邓智 | 儿童内分泌遗传代谢 | 主治医师 | 邓智-儿童内分泌遗传代谢-主治医师-广东省妇幼保健院.png | 70994 | 184×280 | `73b81a96ce8714a08cb00e2b3112c2ea1fc88726306f6cedf75afff77ebffd29` | https://wx.e3861.com/sfyAdmin/Images/Doctor/49124d39-4173-4213-8f4a-909f01f6fb62-280.png |
| 王波 | 儿科 | 主任医师 | 王波-儿科-主任医师-广东省妇幼保健院.jpg | 7677 | 192×280 | `fb8d9d19ffeecefd827ccada356e245551a62eb16fd9592bebd5a0266b8fd93d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c1c6aa9b-d598-4ff1-904b-aeea48e53be9-280.jpg |
| 张也 | 儿童内分泌遗传代谢 | 主治医师 | 张也-儿童内分泌遗传代谢-主治医师-广东省妇幼保健院.png | 71888 | 176×280 | `bfc0eef2ef4b2b149b3486696b1554636faeec1950369ce797b1296f7bab904c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/29052c50-c8f9-4730-8eb2-f635a7366385-280.png |
| 苏海浩 | 儿童内分泌遗传代谢 | 主任医师 | 苏海浩-儿童内分泌遗传代谢-主任医师-广东省妇幼保健院.png | 61211 | 173×280 | `68b2595c41d6a7bd8a85474441252795261f30056b619bf8ead6b6384a406f30` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1689a5ad-d40c-4278-8499-06d2a8a1671b-280.png |
| 陈上清 | 儿童内分泌遗传代谢 | 主治医师 | 陈上清-儿童内分泌遗传代谢-主治医师-广东省妇幼保健院.png | 77127 | 186×280 | `db46bdf37cf8816184c92050a774291b0993f98403da6ea963bf739e8d276360` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f1bb1941-5fd3-4db7-96e0-0a68e7a12c95-280.png |
| 武丽 | 妇女保健科 | 主任医师 | 武丽-妇女保健科-主任医师-广东省妇幼保健院.png | 77005 | 185×280 | `12b484a1e8d383cdf5866702f4501e34d6e0935fd86322661971656a74b911c8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e78273df-fca6-494c-95ee-178916e61e25-280.png |
| 毛玲芝 | 妇科 | 主任医师 | 毛玲芝-妇科-主任医师-广东省妇幼保健院.png | 82906 | 209×280 | `c8b917d758576722b1bd79ee7a2a77e8a5b5f44e4015ccb71a820c1e73fd7e33` | https://wx.e3861.com/sfyAdmin/Images/Doctor/61adc601-f633-41fb-8ee1-1a762de4e7f0-280.png |
| 范保维 | 妇科 | 主任医师 | 范保维-妇科-主任医师-广东省妇幼保健院.png | 84458 | 208×280 | `889bfdbc2dc580709367df824c0b74ba7cbe32e14447ac7ddef6d94847192dde` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5663f017-754e-46b2-9c4a-6fea6fba319e-280.png |
| 叶祥 | 普通儿科 | 主治医师 | 叶祥-普通儿科-主治医师-广东省妇幼保健院.jpg | 7025 | 262×280 | `f7d3f6de36c36352d79c7da716672aa717760dd0cfca4dbebdc40d45fc3fdd3d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/eae2488e-c253-430c-8296-a5a1303a9607-280.jpg |
| 郭小燕 | 普通儿科 | 主任医师 | 郭小燕-普通儿科-主任医师-广东省妇幼保健院.jpg | 7166 | 246×280 | `ee281176c74f58472ed5340706d352abc1dc372a3de20f246c732e12d596bda1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9bfab702-4dc0-4c23-8495-a3db5545876b-280.jpg |
| 赵小琴 | 普通儿科 | 主治医师 | 赵小琴-普通儿科-主治医师-广东省妇幼保健院.jpg | 4960 | 187×280 | `7c1d5e79a4138eb515cb5f181e54aea2fea1fb56e9ad2bb86bb4a1df8308d4d8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fc15876c-f763-444c-bddb-19624fc9f6f1-280.jpg |
| 饶姣 | 心脏中心 | 主任医师 | 饶姣-心脏中心-主任医师-广东省妇幼保健院.png | 74841 | 186×280 | `71795a8ff91bc900a68b7e103616c9db37d73eb7073b7f56725e1b24cf7559ed` | https://wx.e3861.com/sfyAdmin/Images/Doctor/53ac3fc6-d0b6-493b-82fe-88a0afe2940a-280.png |
| 黄景思 | 心脏中心 | 主任医师 | 黄景思-心脏中心-主任医师-广东省妇幼保健院.png | 74243 | 226×280 | `438181b3c6bd6eca2556e06b11356425285d411b1256f6ec3cbf91d452e0d646` | https://wx.e3861.com/sfyAdmin/Images/Doctor/504c6181-cd14-4883-a491-951398e93f5c-280.png |
| 刘琴 | 心脏中心 | 主任医师 | 刘琴-心脏中心-主任医师-广东省妇幼保健院.png | 81581 | 203×280 | `812239a89cf289f8ca92732fe5b610f954e90242b8263ce7036ea9da3b69d73b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8905e3db-805e-4822-8d3f-4da04cccc946-280.png |
| 孙善权 | 心脏中心 | 主任医师 | 孙善权-心脏中心-主任医师-广东省妇幼保健院.png | 130938 | 196×280 | `a4807565c7932d8a1bb27e192efccb9da9098c3f71d8ab48af2bbc983996b921` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f1f009d5-589a-42f8-8632-1c60ad31a6f7-280.png |
| 聂川 | 新生儿科 | 主任医师 | 聂川-新生儿科-主任医师-广东省妇幼保健院.png | 65947 | 174×280 | `9c44127bd0ddd1955e6baf100a304ddf139aaec9b3ad0a5bb807e78dfe4b9307` | https://wx.e3861.com/sfyAdmin/Images/Doctor/61be5ee1-b4b3-47a7-b776-95eaeeed90b9-280.png |
| 向建文 | 新生儿科 | 主任医师 | 向建文-新生儿科-主任医师-广东省妇幼保健院.png | 68011 | 179×280 | `a42e0621db812512b0d70c30f3f923aac3f15d63ad5b562a57bee763b20ce5f7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ee7acb8b-c490-4daa-b08b-3179beb60c7c-280.png |
| 帅春 | 新生儿科 | 主任医师 | 帅春-新生儿科-主任医师-广东省妇幼保健院.png | 69047 | 187×280 | `844e7d95eb2dd6f6c656586de27a473240d40759da4a0735e5c23521ef2c9a1f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/eb4a07fc-e457-47ba-b8cb-10be61518437-280.png |
| 张永 | 新生儿科 | 主任医师 | 张永-新生儿科-主任医师-广东省妇幼保健院.png | 61255 | 171×280 | `e06cb51d9bfd505fb9bc6f4fe195b11d541442fadb42f88f423818744f557ee4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ed37971a-5a2a-4343-b17a-a2b2c9991667-280.png |
| 文斌 | 妇科 | 主任医师 | 文斌-妇科-主任医师-广东省妇幼保健院.png | 68968 | 191×280 | `d9c082677c3522868146d05a9f752bea36bb98ec8ba6b01f5231482317efd5af` | https://wx.e3861.com/sfyAdmin/Images/Doctor/884d4e92-f821-4b87-a112-b0957d98944e-280.png |
| 肖丹 | 营养科 | 主治医师 | 肖丹-营养科-主治医师-广东省妇幼保健院.png | 89091 | 187×280 | `7cad2cf41a774f63d78c1d76bc1c8b0251b456b69c8df512cd8973318138f0d5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/564e7db6-ff33-4caf-9f5b-1fc57a7f21a1-280.png |
| 夏燕琼 | 营养科 | 主任医师 | 夏燕琼-营养科-主任医师-广东省妇幼保健院.png | 79077 | 186×280 | `d2f2a1b020349ba3e2cb597e294895fd2623a605328aa303c72931423a35cceb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e0f8fca3-d366-431a-b254-6b2039b1ddcd-280.png |
| 郑新杰 | 营养科 | 主治医师 | 郑新杰-营养科-主治医师-广东省妇幼保健院.jpg | 6653 | 185×280 | `74e76838fa5b13b36515494b050ad9860d2e5028a08b0a5831f7dff35098dc62` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5162de36-a6c0-4acd-8f99-b5764a1c6cb3-280.jpg |
| 田爽 | 营养科 | 主治医师 | 田爽-营养科-主治医师-广东省妇幼保健院.png | 94549 | 201×280 | `34e597f01fe24ac6fea8c22a0b571bff4274f5a6ece1c2c42c99605f5ea23ddf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/93553d22-55c5-44fa-a85d-5fab9c5a1f02-280.jpg |
| 梅世伟 | 静脉曲张 | 主任医师 | 梅世伟-静脉曲张-主任医师-广东省妇幼保健院.jpg | 5709 | 187×280 | `176bd4177634e62e1079da5578d4569a62ed3a8364b0a76ee0b70f2ef8eefe57` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fd66ac88-4652-4374-917d-a3c0feee4d3a-280.jpg |
| 张钰颖 | 眼科 | 主治医师 | 张钰颖-眼科-主治医师-广东省妇幼保健院.png | 48829 | 187×280 | `4abe8fc6eb4b5ffbe201d9b15e39432149e496ee0adf18f0fd692f1f6cf195a3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ccc07317-6c0d-4f31-ac87-2d12b59c4672-280.png |
| 冯庆阳 | 眼科 | 主治医师 | 冯庆阳-眼科-主治医师-广东省妇幼保健院.png | 59454 | 187×280 | `688c5f87b7b91f1e0f09ac95c2de49a2223ec8175f4c7417d7d4e929f0bb1ddf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ab70b324-c65a-4766-9021-aecffe97e6a2-280.png |
| 李丹丹 | 眼科 | 主治医师 | 李丹丹-眼科-主治医师-广东省妇幼保健院.png | 65429 | 187×280 | `f09f0f1e34438d73787a86d1944f9968b173db4f8eb3c64f6b69e110664c41a2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/39b56725-8bbb-4178-9f9c-2f67bdb70f96-280.png |
| 郑姣 | 眼科 | 主任医师 | 郑姣-眼科-主任医师-广东省妇幼保健院.jpg | 5283 | 187×280 | `086d6121f3a165187a38b53dcec9e8843d22e0a62a18ca485d538060c71e1b86` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a1441bab-bbe7-431f-a4f4-e40e39e0b6d1-280.jpg |
| 曾杞汶 | 眼科 | 主治医师 | 曾杞汶-眼科-主治医师-广东省妇幼保健院.png | 61374 | 186×280 | `323a9435331852570873e508b3ff35c49234193662917f456f2b0da1d505936d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/dc797a53-b198-4cd9-8e31-6acddacc8214-280.png |
| 穆歌 | 眼科 | 主任医师 | 穆歌-眼科-主任医师-广东省妇幼保健院.png | 64831 | 186×280 | `5471a4537b5c15758e1370e58efae359edafd2a20ab899581e465d98a687e345` | https://wx.e3861.com/sfyAdmin/Images/Doctor/477fbbc2-2bf2-4782-9a91-a1efa0a71913-280.png |
| 何慧 | 儿童内分泌遗传代谢 | 主治医师 | 何慧-儿童内分泌遗传代谢-主治医师-广东省妇幼保健院.png | 71385 | 181×280 | `3c7a2ba801e4058b0c94be86cdc6405bfb740c6deba98bac1f8c838f1c653390` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bfdca454-7426-4279-aa4d-c58043d8741f-280.png |
| 谢素贞 | 眼科 | 主任医师 | 谢素贞-眼科-主任医师-广东省妇幼保健院.png | 64724 | 186×280 | `a791e557e7ba9c1c6dd9276d11b23641e5cb6c3703c0458012f624a1511bfa31` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4b1fc257-5553-4098-ad89-41249d73db9f-280.png |
| 黄学林 | 眼科 | 主任医师 | 黄学林-眼科-主任医师-广东省妇幼保健院.png | 46028 | 186×280 | `fad61a5f6c49425b8767148a3c71991ce48e16fe50244de131c1202851220352` | https://wx.e3861.com/sfyAdmin/Images/Doctor/80588d56-7380-413b-ab9b-88d7dd611dba-280.png |
| 张振瑜 | 眼科 | 主治医师 | 张振瑜-眼科-主治医师-广东省妇幼保健院.png | 56627 | 187×280 | `a6cc6f6ba6abf7a707566bf6087d396f510a0ba9cc876b91d41cda16ac014f42` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a204c9ae-e373-4011-82a3-170f13d2ca35-280.png |
| 唐晶 | 小儿胸外科 | 主任医师 | 唐晶-小儿胸外科-主任医师-广东省妇幼保健院.jpg | 7251 | 199×280 | `1e1bae60df4fc9375b9040696c659966f3ac933dde43a320a837e759fa45b0ea` | https://wx.e3861.com/sfyAdmin/Images/Doctor/793273e2-b65a-4b61-8d2e-549de07bd556-280.jpg |
| 刘千里 | 小儿胸外科 | 主治医师 | 刘千里-小儿胸外科-主治医师-广东省妇幼保健院.jpg | 6757 | 229×280 | `17630f9a6f7f0201e39de6a21857f063ae4f123582cae1cd08011a7d13bc24a5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/16eb9674-7765-4371-a470-c59d22b7e36e-280.jpg |
| 商子寅 | 小儿胸外科 | 主任医师 | 商子寅-小儿胸外科-主任医师-广东省妇幼保健院.png | 80678 | 210×280 | `8bc43b37176cfbb9214fc61062addddd6c51cf61706f43be3c1e3dd905a8aa15` | https://wx.e3861.com/sfyAdmin/Images/Doctor/034b6e6c-f3dd-4507-a7c5-74d0c9124771-280.png |
| 马远珠 | 妇女保健科 | 主任医师 | 马远珠-妇女保健科-主任医师-广东省妇幼保健院.jpg | 7328 | 200×280 | `94f2f7622bc73385f75463eae5741220bf57fd9c3ba1a8f1731ee2bc7f8b8834` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a26907ab-a318-4d3d-9465-8933f228bdbf-280.jpg |
| 洪淳 | 小儿胸外科 | 主任医师 | 洪淳-小儿胸外科-主任医师-广东省妇幼保健院.png | 66248 | 186×280 | `762e0e3d62500c19edfe9f28b257b56957b24b6b6115bf2ca9efe64c21e0429a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6ff9fd9c-8ffe-4be9-8c4a-8cfa5c38da80-280.png |
| 方俊 | 妇女保健科 | 主治医师 | 方俊-妇女保健科-主治医师-广东省妇幼保健院.png | 64882 | 178×280 | `1c6cfa9fc1027b429de72a6d6c634bcc69bb7180b8b95124ee0504162e0973c2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6cfad2f2-33b8-4994-97d9-e5e70d1f467a-280.png |
| 刘蕾 | 普通儿科 | 主治医师 | 刘蕾-普通儿科-主治医师-广东省妇幼保健院.jpg | 5559 | 187×280 | `a1c1fe541f0b465086d11e0a914ae83ef7dc819a6dd460bbfd8a2e4adcbd5345` | https://wx.e3861.com/sfyAdmin/Images/Doctor/519150a7-c258-4d7b-bee0-71749c6e8eb3-280.jpg |
| 周佳亮 | 新生儿外科 | 主任医师 | 周佳亮-新生儿外科-主任医师-广东省妇幼保健院.jpg | 5846 | 187×280 | `ef918c9e44c2ae14500d5e007ec8808fd7e9873f05dd4e5c8f22952c8a45aaac` | https://wx.e3861.com/sfyAdmin/Images/Doctor/002dafdf-7bf5-4576-bdc0-0b276b517773-280.jpg |
| 肖尚杰 | 新生儿外科 | 主任医师 | 肖尚杰-新生儿外科-主任医师-广东省妇幼保健院.png | 61014 | 185×280 | `55cbd5778a06b026844b3f8af0745b699b4efdd089f86c80c514883f4e8dc808` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b0205843-0559-448f-b86d-23d1c39c7d28-280.png |
| 李清青 | 皮肤性病科 | 主治医师 | 李清青-皮肤性病科-主治医师-广东省妇幼保健院.jpg | 7656 | 200×280 | `0ac033b07884926e52f435cdd6d0aa6eca3c1c315cac00c078b4b337c6457dd0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bbd63746-e4c3-485b-8b4e-a508d9094726-280.jpg |
| 李晓伟 | 皮肤性病科 | 主任医师 | 李晓伟-皮肤性病科-主任医师-广东省妇幼保健院.png | 55990 | 187×280 | `f0ca9d47f29d71acb7d3dbaadf2c5685e46ef2ae11607fc74f522fd3d9a0dc71` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a0e3afa3-8664-4bf2-86da-c97b9dd51a8d-280.png |
| 李真真 | 皮肤性病科 | 主任医师 | 李真真-皮肤性病科-主任医师-广东省妇幼保健院.jpg | 5206 | 187×280 | `167082c2ab40f30d6c0457a1e2544f0a701e1ff5e7d6c70d9ef25530c505275a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1d10d0d1-9e4d-46f6-abb6-c690b5934bc0-280.jpg |
| 汪青园 | 新生儿外科 | 主治医师 | 汪青园-新生儿外科-主治医师-广东省妇幼保健院.jpg | 6784 | 187×280 | `2e6f66222bf8a0ccf28bb7069456cf365fd0a0cb01afd97c456898ffee5f7ef4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/107e56f2-1326-43c6-be4e-d527fb66e354-280.jpg |
| 黄蓉 | 新生儿外科 | 主治医师 | 黄蓉-新生儿外科-主治医师-广东省妇幼保健院.jpg | 8082 | 217×280 | `42d3b5a0463199e19789a20d1a2f6d2cb1e15a1d95b74b1e9d4dd5adca958cad` | https://wx.e3861.com/sfyAdmin/Images/Doctor/307e78a3-009d-4f46-817b-c09ee1683d73-280.jpg |
| 肖慧媚 | 小儿内科神经内科 | 主治医师 | 肖慧媚-小儿内科神经内科-主治医师-广东省妇幼保健院.png | 86184 | 205×280 | `0321fa81fbf54784484c4cd43ecc12e8d715dd582d769933077fb5261a352ef2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9de0f23c-566a-4e68-b593-5f98d59362ae-280.png |
| 常燕群 | 康复医学科 | 主任医师 | 常燕群-康复医学科-主任医师-广东省妇幼保健院.png | 117257 | 202×280 | `6bd610f12fa7c15d4fcad4ef546fecfb4fef78c6d309714bad718d5fda41529d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/db809b31-c7e6-47bf-bc36-6f1c32f8e56f-280.png |
| 刘芳 | 小儿内科神经内科 | 主任医师 | 刘芳-小儿内科神经内科-主任医师-广东省妇幼保健院.png | 74930 | 208×280 | `0c115b79a70daf3951d71644de6074ca25fe7d041bdf7fdbce2b8d9e3bf636ec` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c394a0b7-2248-4bf2-b356-56acca2f7e91-280.png |
| 徐宁 | 康复医学科 | 主任医师 | 徐宁-康复医学科-主任医师-广东省妇幼保健院.png | 74108 | 210×280 | `8a93e17cf36e83b9e3acbdcc2074e7c154c8ae4cbc3010aef1367a472fa9863e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/70269500-aac8-4dfb-9f4c-d0178490e83d-280.png |
| 杨娇 | 儿科消化 | 主治医师 | 杨娇-儿科消化-主治医师-广东省妇幼保健院.png | 90273 | 198×280 | `c2409a23ae73bba769c3b81d35bc1265d2e4c3140f222494984bbb8ac64f1272` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c42b78a0-edb0-446c-9612-be9620ca4eec-280.png |
| 董川 | 儿科消化 | 主治医师 | 董川-儿科消化-主治医师-广东省妇幼保健院.png | 99789 | 234×280 | `ca8c0de9df4d6c7d1821328acf8e21120c49715670efbda451032913284ae329` | https://wx.e3861.com/sfyAdmin/Images/Doctor/74b916ef-0114-42fc-8f07-6d81371e3bfd-280.png |
| 郝彤彤 | 儿科消化 | 主治医师 | 郝彤彤-儿科消化-主治医师-广东省妇幼保健院.png | 86595 | 199×280 | `927732b2118baeae930ff39aabcec5e2103109aaf3c4ca3084c41f7b4fa4438c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/838c9d81-7dd4-45ae-8319-f890c888ffc1-280.png |
| 林兴 | 儿科消化 | 主任医师 | 林兴-儿科消化-主任医师-广东省妇幼保健院.png | 86695 | 196×280 | `d736ca499faf3e4fc71284ef5e43d33b50e0fb2d85fde2fa4c7a5a287e738e24` | https://wx.e3861.com/sfyAdmin/Images/Doctor/03825e2e-3e15-416b-a15d-19954ed71587-280.png |
| 刘鸿 | 儿科消化 | 主任医师 | 刘鸿-儿科消化-主任医师-广东省妇幼保健院.jpg | 7820 | 258×280 | `1a61db69c8181594e1b183dc1ad5cb778244be73ed88a290d5986a1a8d933ba8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6e4aa902-644e-4cb1-92f2-c5ff2077574e-280.jpg |
| 高利伟 | 儿科消化 | 主任医师 | 高利伟-儿科消化-主任医师-广东省妇幼保健院.png | 93963 | 202×280 | `6e36d4dc389782b35996ecc6d6c53cce9f153606c6ac403b2ba0c9a59a19c5c3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a15e109f-be7f-4ca7-9cfc-5569993e9825-280.png |
| 吴怡凝 | 眼科 | 主治医师 | 吴怡凝-眼科-主治医师-广东省妇幼保健院.png | 68105 | 187×280 | `128629f7cd61a4a7db9c153789bff592a092be9754af183119adab228ff3c4dc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ef09a322-ec58-4f18-a791-d7c464204a83-280.png |
| 林汇政 | 儿科消化 | 主治医师 | 林汇政-儿科消化-主治医师-广东省妇幼保健院.png | 91692 | 199×280 | `f692d6d8a4ac9320663b78d304a6d5cd83dc98a49adb6f06cee8011268e2a9e3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e3f53b05-8929-4760-b0fc-dabc97ff80ff-280.png |
| 罗文雄 | 儿科消化 | 主任医师 | 罗文雄-儿科消化-主任医师-广东省妇幼保健院.png | 92487 | 204×280 | `6bf1986887a7bc12127d0fbf0e61b7c3252560d004477f2c969059f10fadc6e7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d10e45c3-9b33-4b22-b2b9-674a8602f9f5-280.png |
| 胡兢晶 | 普通儿科 | 主任医师 | 胡兢晶-普通儿科-主任医师-广东省妇幼保健院.jpg | 6153 | 211×280 | `39c13c584a0e4758542b55644ae0e187cf2f5dba854f41b1f1ed6678608f4a6d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/35d0a1ce-df72-4e68-86e8-7687db958b88-280.jpg |
| 马志明 | 内科 | 主任医师 | 马志明-内科-主任医师-广东省妇幼保健院.png | 76111 | 185×280 | `09efcc816ac8f9edec31692fa66c284ff2d39830d36c622ca1bf23bda0690c31` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2e280e6b-6bce-4349-968c-94fb7a4a9898-280.jpg |
| 陈思 | 内科 | 主任医师 | 陈思-内科-主任医师-广东省妇幼保健院.png | 72972 | 187×280 | `63705442691a3355620e12c78b47b103b02f5eff1628f69fc5b3f1957efca6ba` | https://wx.e3861.com/sfyAdmin/Images/Doctor/262238bc-3bc8-46d5-856b-d9ef9132b9cd-280.jpg |
| 郭运忠 | 内科 | 主任医师 | 郭运忠-内科-主任医师-广东省妇幼保健院.png | 73228 | 187×280 | `b74c29cc93ac222e67dc4f698ee6847a22bd06c90ebc49596c578e76fcc1dae8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3a0523fa-5d6c-4eb0-89ef-0e33ba7dedf3-280.jpg |
| 张艳 | 内科 | 主任医师 | 张艳-内科-主任医师-广东省妇幼保健院.png | 64659 | 186×280 | `7b843788ec8bcb4c2654efa7c202e4001c902031bbe95ef97c5f55cdac740403` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3657de4b-4710-48bd-8960-76e630d0f684-280.jpg |
| 吕小飞 | 内科 | 主任医师 | 吕小飞-内科-主任医师-广东省妇幼保健院.png | 73010 | 186×280 | `2e2ab2633be80238f461170094ffb286125986c732d32925487972568addf0ed` | https://wx.e3861.com/sfyAdmin/Images/Doctor/edee984c-5cf5-41a0-bc56-1f4ebf366a43-280.jpg |
| 徐力堃 | 内科 | 主任医师 | 徐力堃-内科-主任医师-广东省妇幼保健院.png | 68236 | 186×280 | `9640b0f83382f9d312467204aa97dc5102c48b5f0645e91042c40653bfdf5a90` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5e85901f-5a68-4f80-a51c-e3285f7c4883-280.jpg |
| 郭祯 | 内科 | 主任医师 | 郭祯-内科-主任医师-广东省妇幼保健院.jpg | 5564 | 187×280 | `1e4c654da8557efe22143f3a7228c8acd60192f3feca86575c4a6ecce16fa16a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/41346c4b-9607-4dda-8c2f-94126a7e421c-280.jpg |
| 邹燕敦 | 内科 | 主任医师 | 邹燕敦-内科-主任医师-广东省妇幼保健院.png | 71198 | 186×280 | `88632f3f1a9f1890739ab810f5d9cf5e8f34c640de5fcfc5ff77a9c0c8d6ff07` | https://wx.e3861.com/sfyAdmin/Images/Doctor/31986bbb-c545-4cf5-ad05-67b8b238561e-280.jpg |
| 刘祎婷 | 内科 | 主任医师 | 刘祎婷-内科-主任医师-广东省妇幼保健院.jpg | 5792 | 174×280 | `7d857eaf5c0a902e38bac0ae34a699391ece11a7e6159c8b4a49c7160d8d4bb3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b105b9be-edf4-41e3-ae61-35d1639f2a46-280.jpg |
| 林常青 | 内科 | 主任医师 | 林常青-内科-主任医师-广东省妇幼保健院.png | 72840 | 186×280 | `42bfe6d684c324bdb6cc4f746fa2183c224a68fd66864dd97304c69db1ca016e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c9625316-f696-43d3-8dcc-7c7bf73772dc-280.jpg |
| 赖锦斌 | 内科 | 主任医师 | 赖锦斌-内科-主任医师-广东省妇幼保健院.png | 71089 | 187×280 | `ad9b5b8b966371a973247a69455f9a48d2ee2fd35887b6bbe52234dfb21f994a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ede6f5a2-8e0e-48e3-9a07-5cf553f98afc-280.jpg |
| 麦华超 | 内科 | 主治医师 | 麦华超-内科-主治医师-广东省妇幼保健院.png | 66052 | 186×280 | `600eb833f36f2e65044c66177de5e8f3aa3c62121c9ca448874865c783bd86d5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4bb327f1-62a6-48a6-860e-fe5798a71dce-280.jpg |
| 钟旋 | 内科 | 主治医师 | 钟旋-内科-主治医师-广东省妇幼保健院.jpg | 7006 | 206×280 | `60e22b81fde18ed0028d6457f1defcf410d3054245c5c31078bc59cb14e2d819` | https://wx.e3861.com/sfyAdmin/Images/Doctor/07d30e05-25e0-4a57-b8ba-93bb0c674cf5-280.jpg |
| 范丽梅 | 内科 | 主任医师 | 范丽梅-内科-主任医师-广东省妇幼保健院.png | 73015 | 186×280 | `a1a9bca953dca82d3b6019b935ad277251844b3dc645d29a766879da020f5e1f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/73bfe71b-b138-4476-81cd-41763925f555-280.jpg |
| 余丹峰 | 内科 | 主任医师 | 余丹峰-内科-主任医师-广东省妇幼保健院.jpg | 5335 | 187×280 | `6157573f3cbb7b6c9c03f9093db3d150bcbcb8c71208c5c0e58c920b11a4e11e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/09c39efc-f59c-4470-8f2b-b48c785647b8-280.jpg |
| 袁力 | 产科 | 主任医师 | 袁力-产科-主任医师-广东省妇幼保健院.png | 97920 | 221×280 | `2eaea78e95bbb89d37ede4453ee0ecb3d824753d56960dea4e322892ba673127` | https://wx.e3861.com/sfyAdmin/Images/Doctor/58b02d37-4ac5-437a-b9a3-f749ea53b23c-280.png |
| 余干锋 | 产科 | 医师 | 余干锋-产科-医师-广东省妇幼保健院.png | 71540 | 187×280 | `13ed90fb794144e9adda01c7af5edc961eaafb8b82a9103d8081fe2a8dcc8d17` | https://wx.e3861.com/sfyAdmin/Images/Doctor/76cfb736-89d8-40b3-a045-4f6545d7155c-280.png |
| 李嘉蔚 | 产科 | 主任医师 | 李嘉蔚-产科-主任医师-广东省妇幼保健院.png | 83130 | 204×280 | `261bcca3dc16485f923af2e6d74b2bb8d13378750db26aa1dadb8be62b9eea36` | https://wx.e3861.com/sfyAdmin/Images/Doctor/090f952d-4f39-43be-9693-5881caf2538d-280.png |
| 梁海英 | 产科 | 主任医师 | 梁海英-产科-主任医师-广东省妇幼保健院.jpg | 7674 | 168×280 | `9bde02f63aaef310783b6b8c97749228d201159ba4f53a3812bb4b492838ba1c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/73b3b2c5-1b76-4ef7-813c-30222f34c300-280.jpg |
| 江剑辉 | 儿童内分泌遗传代谢科 | 主任医师 | 江剑辉-儿童内分泌遗传代谢科-主任医师-广东省妇幼保健院.png | 71715 | 183×280 | `97d495ebc801fa82ebd1e8aea9e451a8329bf90dc130f41342f0e57c98496f12` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e41769e9-7415-44e0-b3e0-d58512d59322-280.png |
| 温济英 | 产科 | 主任医师 | 温济英-产科-主任医师-广东省妇幼保健院.jpg | 4637 | 187×280 | `d9a231db498507ab453ec263770aec7b68a914c459b565f3744caa57aa3b0e44` | https://wx.e3861.com/sfyAdmin/Images/Doctor/79d6a722-49e6-4869-918d-bf33c314448a-280.jpg |
| 叶文慧 | 内科 | 主任医师 | 叶文慧-内科-主任医师-广东省妇幼保健院.png | 68134 | 186×280 | `ab1e78147eb42d1558e9cd6a5508f5fd12b0a41b3c2092ae72b3506b40c5601f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ad043616-411d-4bec-8ad8-2054c18e362c-280.jpg |
| 邢佳玲 | 产科 | 主治医师 | 邢佳玲-产科-主治医师-广东省妇幼保健院.jpg | 6818 | 270×280 | `37dab526c2f56d3688d7843757db066de665e7edc0c2ac30e93a4e1ef0337f28` | https://wx.e3861.com/sfyAdmin/Images/Doctor/415c1952-ce0e-41e2-aeec-49f3f8eb0041-280.jpg |
| 彭静 | 产科 | 主任医师 | 彭静-产科-主任医师-广东省妇幼保健院.jpg | 8580 | 280×280 | `45444867bd72122d5298aeb0e9bd777e5df2b14e8a839478b68d0defb67558a4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4a4e71ae-1290-433c-a8b0-bcfaf9802784-280.jpg |
| 王意 | 妇女保健科 | 主任医师 | 王意-妇女保健科-主任医师-广东省妇幼保健院.png | 76393 | 179×280 | `c6edd63bd524039d110076e6d0c8687fdd6430e4f7b58557ddcfbbca04c0838f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/34db6875-45da-47ef-9b56-0e177186b4cd-280.png |
| 余晖 | 产科 | 主治医师 | 余晖-产科-主治医师-广东省妇幼保健院.jpg | 6585 | 190×280 | `3aae4c1570ae7125f847487bf885b0af8a6c0d3fb42be929b292613989af20d6` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9f3f7180-7253-4af7-bfac-0a5237bbabc2-280.jpg |
| 袁晓兰 | 产科 | 主任医师 | 袁晓兰-产科-主任医师-广东省妇幼保健院.jpg | 7750 | 199×280 | `a5822f9935cd69957f6b70976bf5f1855ec7d0e5ee6329e92657783e98d2e37e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/03dec1d1-b9b4-48f7-a322-d3f6dab7e893-280.jpg |
| 麦子霞 | 产科 | 主治医师 | 麦子霞-产科-主治医师-广东省妇幼保健院.jpg | 7984 | 192×280 | `1f3e0db037497fe0527a4867346e43dbe2070682e74e767c282541c5a2de428f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/39dfedad-dd63-4643-960e-581626475976-280.jpg |
| 牛静 | 妇科 | 主治医师 | 牛静-妇科-主治医师-广东省妇幼保健院.png | 61058 | 182×280 | `e0bfeab650b60df5f24806d23fe5d2d92dd5886d66cc58b8f39bd7d81f1d56a5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9430bad1-8e67-48db-a5f8-f4c0881b36a8-280.png |
| 侯明敏 | 产科 | 主任医师 | 侯明敏-产科-主任医师-广东省妇幼保健院.jpg | 7146 | 199×280 | `5973ea8d65ccd16971e4178635fdd2ab978f383ab0a222602881317519d1c6c3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6453eec0-cf6b-48ae-ac82-eb20a9203e1d-280.jpg |
| 张温麑 | 产科 | 主任医师 | 张温麑-产科-主任医师-广东省妇幼保健院.jpg | 6533 | 178×280 | `531f2e194f1723e398856da1dfd4da10696d1aa03dd9781837d689c0ae996a5a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/feb58523-dc2f-452d-9a02-cad045aab8d9-280.jpg |
| 郭庆禄 | 乳腺疾病影像学诊断 | 主任医师 | 郭庆禄-乳腺疾病影像学诊断-主任医师-广东省妇幼保健院.jpg | 7444 | 205×280 | `fd82e54ba9a12518e0f996fe3e397bb32d96b6c5136356908840d6c2eeb7e02b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bf3a264b-0bdf-46f4-ac11-89c06922fec7-280.jpg |
| 和秀魁 | 妇科 | 主任医师 | 和秀魁-妇科-主任医师-广东省妇幼保健院.png | 126269 | 232×280 | `1736b885aa1c0dbb0b19ffa60b19903eaabd2ecbf4b0aa3f39cbedd3be329b34` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ea66d3c1-7739-4cd0-b7a0-43a69107d0c7-280.png |
| 李荔 | 妇科 | 主任医师 | 李荔-妇科-主任医师-广东省妇幼保健院.png | 65001 | 178×280 | `1ee5c503d2764e662b36b4b9e246744b53365deb26a9f9f40466fc02a1eb6c4b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/41f8da8d-23ad-4c35-ae1a-9fa62ce296bf-280.png |
| 王三锋 | 妇科 | 主任医师 | 王三锋-妇科-主任医师-广东省妇幼保健院.png | 80652 | 218×280 | `02d3d04b99380160ad37b1b244771fb7b4c0179b52e966d440e346f724f42fba` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1b0fcd18-2a0e-4ccf-9101-8be5b246d7a9-280.png |
| 李海萍 | 妇科 | 主任医师 | 李海萍-妇科-主任医师-广东省妇幼保健院.png | 97128 | 208×280 | `0ceefd329cd7038269437bda07b17a16d2620498455bb351f4eea1d85d345316` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2714e7ac-9b9e-40e4-b33c-2ebfcc098a52-280.png |
| 叶一林 | 疼痛科 | 主治医师 | 叶一林-疼痛科-主治医师-广东省妇幼保健院.png | 84755 | 199×280 | `8f5f0f834f6cab7a759ce85a1d0bb6c377c5144f52c6128f367cbec21529fbcc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/305892b1-6826-4ead-936a-32c755ec8d96-280.png |
| 黄希照 | 疼痛科 | 主任医师 | 黄希照-疼痛科-主任医师-广东省妇幼保健院.png | 63769 | 164×280 | `5fbef64f66da818278bc24e47659de34e7e6e8fdcad33adc612e2e306b855f83` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2675d8e8-5db9-4b41-a21b-212c1a0ae197-280.png |
| 马赛 | 小儿泌尿外科 | 主治医师 | 马赛-小儿泌尿外科-主治医师-广东省妇幼保健院.png | 58795 | 181×280 | `f8c95b51b8bedee9ca0ddcfbf82d212a770198bdaddaf440f877d3f77af72e4b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3b5ed325-e3f0-4d74-8204-f3c15a907aff-280.png |
| 欧阳可育 | 小儿泌尿外科 | 主任医师 | 欧阳可育-小儿泌尿外科-主任医师-广东省妇幼保健院.png | 76396 | 187×280 | `929e8e083fb58838b6a8e1717e60680794b85225d123cb4ea3ea306b2eeb7cec` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f5176ed0-ffe5-48d3-8187-e42bfcacc1d0-280.png |
| 劳伟华 | 小儿泌尿外科 | 主任医师 | 劳伟华-小儿泌尿外科-主任医师-广东省妇幼保健院.jpg | 7682 | 206×280 | `897f0e00e744308ae17a859274627dc3549191b26ccceffc0c38d263f571841a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e838de0d-d3f5-4439-bcb1-4d2d6c55eb2d-280.jpg |
| 张协武 | 小儿泌尿外科 | 主治医师 | 张协武-小儿泌尿外科-主治医师-广东省妇幼保健院.png | 62176 | 187×280 | `fa18783602b5e7c8d478d2caed112c88845238208ca4f7ed0e7be20fa3d7506c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c1f6d68b-cf43-4c03-ad99-8eb152abfc98-280.png |
| 罗迦耀 | 小儿泌尿外科 | 主治医师 | 罗迦耀-小儿泌尿外科-主治医师-广东省妇幼保健院.png | 66302 | 181×280 | `1a21e00d5f70d9fcde27e4e4a83264d3e5a04b2ef4dce58636d29c597d10dfbc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/953e91a6-84a3-43b3-838b-729afdfcd974-280.png |
| 林炎坤 | 小儿泌尿外科 | 主任医师 | 林炎坤-小儿泌尿外科-主任医师-广东省妇幼保健院.jpg | 7894 | 206×280 | `bdf969972cc3b29dbf4b019ea97185f5ddca87364e56e909f52f6d3edb34c283` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4b0bb6d5-e0e2-4434-8dba-033ff7d39313-280.jpg |
| 陈广道 | 儿科呼吸 | 主任医师 | 陈广道-儿科呼吸-主任医师-广东省妇幼保健院.png | 91248 | 226×280 | `f66bbf003083a89c38331e28b763b95e17e7c3884ab02f01d3edbb2100d2e430` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8c2cddd7-0ba7-4a25-9c9c-99ba43e3744c-280.png |
| 周真 | 儿科呼吸 | 主任医师 | 周真-儿科呼吸-主任医师-广东省妇幼保健院.png | 86682 | 253×280 | `740de85b948a4028783dafa6995eb7648ec78c80c4928f637a6c493015ec8917` | https://wx.e3861.com/sfyAdmin/Images/Doctor/94e34d19-54c7-422d-b01d-a4e3eaabe4da-280.png |
| 周真 | 皮肤性病科 | 主任医师 | 周真-皮肤性病科-主任医师-广东省妇幼保健院.jpg | 7296 | 183×280 | `c27797e7423f2bb52dc460f20133532ac44498c5351e1988b1c8d097f8e336e8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ffcaafd0-f6cb-4082-a53e-2616a15016b2-280.jpg |
| 谢梅 | 儿科呼吸 | 主任医师 | 谢梅-儿科呼吸-主任医师-广东省妇幼保健院.jpg | 9581 | 271×280 | `c0cce49cb5d6e537386b12da252874e3ae1ef8ae2cd951f9afe73e0ce0f52b92` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a6210319-98e2-48cf-b061-e189551f0a5f-280.jpg |
| 庞焕香 | 儿科呼吸 | 主任医师 | 庞焕香-儿科呼吸-主任医师-广东省妇幼保健院.png | 84172 | 183×280 | `0ebc4d8539a27f086c6ab6acffbfe79964d37f3955f1e284f67f2d87bf3b8940` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2673d27b-5a6a-4e33-813e-fb9603cc4c1d-280.png |
| 李增清 | 儿科呼吸 | 主任医师 | 李增清-儿科呼吸-主任医师-广东省妇幼保健院.png | 140540 | 293×280 | `1a5c7d8e55c5cdf3c0fd52b8ca0e2fe6ca0852be93cbfe850d62c0fbede04937` | https://wx.e3861.com/sfyAdmin/Images/Doctor/44e2536c-e756-4381-b450-8555f5f7f1c4-280.png |
| 郭素华 | 儿科呼吸 | 主任医师 | 郭素华-儿科呼吸-主任医师-广东省妇幼保健院.jpg | 9087 | 283×280 | `ed8c09f165acdcb52e69d511b76257969e868e618ed4fde7db2b4a4fb00a2176` | https://wx.e3861.com/sfyAdmin/Images/Doctor/72bdb00a-911d-4e56-b4c8-5a80143b2acf-280.jpg |
| 方元龙 | 新生儿外科 | 主治医师 | 方元龙-新生儿外科-主治医师-广东省妇幼保健院.jpg | 8344 | 210×280 | `001b6d9b7b37c415b638ef64022e0a76cab6fc9dfff826753b63a3fcb3f2ca3a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e0f1d1b9-1757-4b57-8ed0-da48824d1727-280.jpg |
| 谭艳芳 | 儿科呼吸 | 主任医师 | 谭艳芳-儿科呼吸-主任医师-广东省妇幼保健院.jpg | 10183 | 263×280 | `8a27f404144f097632b90ae7a7fb5f296122625242c00128e9f2f65c5a65d149` | https://wx.e3861.com/sfyAdmin/Images/Doctor/71646e16-ca9d-452d-9dda-0a004c4edcb4-280.jpg |
| 林英 | 儿科呼吸 | 主任医师 | 林英-儿科呼吸-主任医师-广东省妇幼保健院.png | 99569 | 265×280 | `738308ec927d74e175f47253f86ddface2717794a047ff2e9a65f59082c86d2b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f26205d6-3f79-4319-a04b-2f1c6c95dc14-280.png |
| 陈圳荣 | 口腔科 | 主治医师 | 陈圳荣-口腔科-主治医师-广东省妇幼保健院.png | 107992 | 255×280 | `564db02d44eb538b6dbf45bb114f5cb388256107d8298d08cbed9ab05d7259ba` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9bd5f53f-0187-4241-9688-d884d2944d5c-280.png |
| 陈润哲 | 口腔科 | 主治医师 | 陈润哲-口腔科-主治医师-广东省妇幼保健院.png | 62879 | 175×280 | `beb6a3ddaef297b0f40d99c1fc19c30bd87208595836b38a0763b863fba66544` | https://wx.e3861.com/sfyAdmin/Images/Doctor/733c1cb5-fddf-4a85-b575-01a8ce48464b-280.png |
| 刘宏璐 | 口腔科 | 主治医师 | 刘宏璐-口腔科-主治医师-广东省妇幼保健院.png | 71532 | 171×280 | `734e679c6ffd00a5a955302db631795ec7e9f3ee4ca3d4df8ffece399366e43d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9db6039b-533c-4e7b-9fa7-d4a01fb7aecf-280.png |
| 黄群 | 口腔科 | 主任医师 | 黄群-口腔科-主任医师-广东省妇幼保健院.png | 61155 | 167×280 | `adc8cb3ad2c11e92e8410244e088fcc60e0ac7b6f87ff2cc3abaf48a8416d3ac` | https://wx.e3861.com/sfyAdmin/Images/Doctor/99ba725f-052e-40f8-82f5-0f79e1dcf9bd-280.png |
| 李心悦 | 口腔科 | 主治医师 | 李心悦-口腔科-主治医师-广东省妇幼保健院.png | 61466 | 180×280 | `5ce56c32ff68c36a134293587c1d7624b8c08c99198cd43224527418f54c25d1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f851dc51-b980-43c4-a0e1-7fbf6a0b002a-280.png |
| 刘慧华 | 内科 | 主治医师 | 刘慧华-内科-主治医师-广东省妇幼保健院.png | 72993 | 187×280 | `cd4ccb03fedde6a1eb238528fbb227f28b1d943dbe9a36eab7949a8a69080ea7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a9abff3a-b93f-4a9b-9f72-3c1bcb4d4d2d-280.jpg |
| 周鹏 | 口腔科 | 主治医师 | 周鹏-口腔科-主治医师-广东省妇幼保健院.png | 55566 | 160×280 | `32cd8de5dc6a8b06de3ecfe8396e14183d560983b5995d098a06bd959332585e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7848d5ae-464c-4d77-ba11-589d09a405ce-280.png |
| 万绵佳 | 口腔科 | 主治医师 | 万绵佳-口腔科-主治医师-广东省妇幼保健院.png | 69912 | 162×280 | `e48ec15b35b7375cf63821abdbb5e51f890301492fd606c17bee3f1f44737be0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8c7da630-ad56-46d0-a92e-2e4185506d0f-280.png |
| 罗毅平 | 内科 | 主任医师 | 罗毅平-内科-主任医师-广东省妇幼保健院.png | 72722 | 187×280 | `1733ddc97fef5ffe7a6237ee4bd6e0cc26055e41eb14a37dc7de2d32ea68c326` | https://wx.e3861.com/sfyAdmin/Images/Doctor/18548a18-f3eb-48f6-bae7-eba3a930e27f-280.jpg |
| 闫怡轩 | 口腔科 | 主任医师 | 闫怡轩-口腔科-主任医师-广东省妇幼保健院.png | 64006 | 185×280 | `099ca15a7d1202ed4bd78356ec78f7b8214457099b1f8496b5fce105406512c1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/10a0cbe8-ad7e-44dd-b825-04a50d291aef-280.png |
| 曹行羽 | 小儿神经外科 | 主治医师 | 曹行羽-小儿神经外科-主治医师-广东省妇幼保健院.png | 60007 | 150×280 | `e73bedd1b79f8bf168a6dd600e0217421d945f7b048fd09ccc2711d1ec202c24` | https://wx.e3861.com/sfyAdmin/Images/Doctor/26d6be4f-7481-48a4-ab6f-e1a71ec81143-280.png |
| 桂剑 | 小儿神经外科 | 主治医师 | 桂剑-小儿神经外科-主治医师-广东省妇幼保健院.png | 54495 | 147×280 | `c1a65f410e877c18c3e0ed59d6443b6bf19a58fb3a21ad27c743399f3aed9623` | https://wx.e3861.com/sfyAdmin/Images/Doctor/673eea0d-58e0-424e-860e-637a3018d2d3-280.png |
| 谭晓嫦 | 妇科 | 主任医师 | 谭晓嫦-妇科-主任医师-广东省妇幼保健院.png | 84381 | 191×280 | `d86c78978dc6f7f7c17751170b7bfc2a54dc34bcd892e138e8eee7eae8cf1c8d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4a0706ad-002d-4bef-aff5-51d8afedf342-280.png |
| 梁月梅 | 产科 | 主治医师 | 梁月梅-产科-主治医师-广东省妇幼保健院.png | 72524 | 195×280 | `8f1229e88ae7e3dc9738c478411a024f75157a19f4382679e069ece9ca77c944` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4b7daa58-534e-4ad6-9485-3dd0389a31e9-280.png |
| 刘珊珊 | 产科 | 主治医师 | 刘珊珊-产科-主治医师-广东省妇幼保健院.png | 72753 | 250×280 | `0cd79ccbc5ebaf9dbd867e0ce1a1374064424e77a389ec33976b6efa4a6a6551` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bc3fbf03-91d5-4362-bf8a-da5adcc5476d-280.png |
| 麦碧 | 妇科 | 主任医师 | 麦碧-妇科-主任医师-广东省妇幼保健院.png | 91269 | 193×280 | `c996d07191eed020d24d09955ccd221eb8a9a19e31707cfb716208030d301434` | https://wx.e3861.com/sfyAdmin/Images/Doctor/db7dcf4a-fa28-4e1c-a04c-6656b35b32db-280.png |
| 布俏雯 | 妇科 | 主治医师 | 布俏雯-妇科-主治医师-广东省妇幼保健院.png | 118941 | 280×280 | `8bf8c8dea80a3141b949ffd685a8bf19752b3931383d96a432dfc8e7abf97515` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d789f2b2-953e-4997-ab22-58853908d90d-280.png |
| 陈永秀 | 妇科 | 主任医师 | 陈永秀-妇科-主任医师-广东省妇幼保健院.png | 107720 | 212×280 | `b8bcd26456941aeb980938856f9a85607f08fb815cfe747c024d07e42ade631b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/aa3b7d11-f6a0-4403-a7f0-47ebb3bf7907-280.jpg |
| 洪小山 | 妇科 | 主任医师 | 洪小山-妇科-主任医师-广东省妇幼保健院.png | 68713 | 189×280 | `3671d9f6ff56e3e4e0f3d3d593597b0727528c4f05957a4862dd1b163cccd5ae` | https://wx.e3861.com/sfyAdmin/Images/Doctor/005bc944-7522-4a77-9ae0-a3824ec0255f-280.png |
| 禤坚艳 | 早孕关爱 | 主任医师 | 禤坚艳-早孕关爱-主任医师-广东省妇幼保健院.png | 73659 | 224×280 | `5e8064845df0006fbdbf24b1d8d454ce8d577c00c45a03795e413affea3f0111` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5c5df6cd-aa8f-471c-b90c-e215fee50c20-280.png |
| 吴歆怡 | 妇科 | 主治医师 | 吴歆怡-妇科-主治医师-广东省妇幼保健院.jpg | 9020 | 192×280 | `7b817ff635a13ab389dffba156e32c98d524c072c71b34623c360d4119f1fd94` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c276c2db-4a37-40e1-8b6d-b452a3113cce-280.jpg |
| 卢家璋 | 小儿神经外科 | 主任医师 | 卢家璋-小儿神经外科-主任医师-广东省妇幼保健院.png | 64678 | 190×280 | `9dcafb831af045677ccf5743a6db257954ebbcb6419dd169ab25cc542a51e011` | https://wx.e3861.com/sfyAdmin/Images/Doctor/986b4bde-7245-4e6b-86f0-404cb68b11cf-280.png |
| 胡桂英 | 妇科 | 主任医师 | 胡桂英-妇科-主任医师-广东省妇幼保健院.jpg | 9229 | 280×280 | `8365584b63f0b12c187025ed2f64de18baa74f59f3eb704ad9b791baa75ac7da` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d7344db7-e6a4-49dd-848d-5b4795349002-280.jpg |
| 张灏 | 内科 | 主治医师 | 张灏-内科-主治医师-广东省妇幼保健院.png | 79729 | 212×280 | `1b21d4600994fd7b906a69d8548dc08157c502b5403ff4e627acee5fe6ae6110` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2322f629-b220-4bb0-9d47-af796682c7c0-280.png |
| 艾君 | 妇科 | 主治医师 | 艾君-妇科-主治医师-广东省妇幼保健院.png | 117771 | 200×280 | `48689868153cd00aee68ea12af2a236d40750ca787304c663c70db963632a0ed` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0f697c93-c10a-4d56-95f4-6c22704f9640-280.png |
| 袁建章 | 内科 | 主任医师 | 袁建章-内科-主任医师-广东省妇幼保健院.png | 50555 | 210×280 | `bdafe80ac5ae50e8bbf5d3e38d21ff1d97b51edbeed41409ae370275379406f2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/29ee7edb-1742-4314-a842-59bebb9ab2f9-280.jpg |
| 周妍 | 产科 | 主治医师 | 周妍-产科-主治医师-广东省妇幼保健院.jpg | 7893 | 187×280 | `d00ba0fbc7535b720cd1c9162492c546d28204ee573ed467b69dba949c63d6ec` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3c2bf8ef-0679-4957-b548-961d2454cac4-280.jpg |
| 彭燕 | 内科 | 主治医师 | 彭燕-内科-主治医师-广东省妇幼保健院.png | 63608 | 187×280 | `8fb08d0b65887a13996c135b9183e2cb985273fea7eb5b9f23770435487ead08` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3f1267a2-a7a6-4177-a1d9-53d71fcda350-280.jpg |
| 宋悦 | 妇科 | 主任医师 | 宋悦-妇科-主任医师-广东省妇幼保健院.png | 87646 | 188×280 | `a0cdb99ff66cd9aae1fe7d5f17fa05927a30ebd5be089214978e4e2dda0e2c53` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f6e58afc-8272-43f3-b681-8a32e36ad8ab-280.png |
| 黄晓文 | 妇科 | 主任医师 | 黄晓文-妇科-主任医师-广东省妇幼保健院.png | 89573 | 189×280 | `35300c8a4b0003e8d37eeac748f03aed596aa8ffa00aba4b8f80abd1aa88f7d9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7626c955-2dd1-4272-92bb-0c0d5a04e97d-280.png |
| 陈伟芳 | 妇科 | 主任医师 | 陈伟芳-妇科-主任医师-广东省妇幼保健院.jpg | 7328 | 210×280 | `a9eb092f550921b07f1b3b7ba2fb6443dfff20fcc6d0b889ba4f4dd2fedb69aa` | https://wx.e3861.com/sfyAdmin/Images/Doctor/71e5ec62-e150-4e18-934f-e7583c650fd5-280.jpg |
| 罗喜平 | 妇科 | 主任医师 | 罗喜平-妇科-主任医师-广东省妇幼保健院.jpg | 7557 | 191×280 | `f39ab4b12336abe4e8c2bf7bb0da5dd2a30e529e1e2a4df82b5d484a8d303b34` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5036bb58-c080-4b13-8ffa-10aea71332b4-280.jpeg |
| 黄玲 | 妇科 | 医师 | 黄玲-妇科-医师-广东省妇幼保健院.png | 90866 | 200×280 | `f14dfcb52e5f392eddb282b195c655e36d4b378d5bb309d29f9de6c81c3fdfff` | https://wx.e3861.com/sfyAdmin/Images/Doctor/097dfee2-1506-4fc9-b709-217a8c1a32c1-280.png |
| 何路路 | 妇科 | 主治医师 | 何路路-妇科-主治医师-广东省妇幼保健院.jpg | 7270 | 177×280 | `6b27bd107cb88161ccf5ff599404f87c24afeb6c80fd04471460fb34d8da5aa0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/936d6d3d-b326-4dcf-84a0-fca65826fb6d-280.jpg |
| 孙小丽 | 妇科 | 主任医师 | 孙小丽-妇科-主任医师-广东省妇幼保健院.png | 106686 | 226×280 | `a606f128e2909a44e736dab1ab38114c99336f33b2cebffefc3142cc8d8dbcba` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3ac7c6ff-5d51-4c96-bf1e-7745db959833-280.png |
| 何少仪 | 产科 | 主治医师 | 何少仪-产科-主治医师-广东省妇幼保健院.jpg | 8006 | 280×280 | `f60300ca7a903a6bacb9ef4822127b4b0a3a929b1aac3e2d1e988003c610d39e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1f60e957-559a-42ec-b082-51b9871796ec-280.jpg |
| 薛素华 | 妇科 | 主任医师 | 薛素华-妇科-主任医师-广东省妇幼保健院.jpg | 9634 | 210×280 | `0afb70d7f0b47ac12327d73b7e09e148d569adc3026f3b6b39696d2572cb9008` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a9e78301-bad9-48dc-93d6-b075a4f1fb6b-280.jpg |
| 陈偲 | 产科 | 主治医师 | 陈偲-产科-主治医师-广东省妇幼保健院.png | 81809 | 280×280 | `1a56e57b9862b37828221cad9b64c7c96928e0f689e891d074b68daef9b60cd7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1d62d669-be7b-4b30-9f99-b882d48fef5c-280.png |
| 孟钊 | 妇科 | 主任医师 | 孟钊-妇科-主任医师-广东省妇幼保健院.png | 64467 | 188×280 | `ff6b345b2c6d7187650b837b6701b8bd2bb800dc294baa17ec00256276a24f25` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4e547d97-a6f1-4d18-ba31-a44588cf9177-280.png |
| 鲁敏 | 妇科 | 主治医师 | 鲁敏-妇科-主治医师-广东省妇幼保健院.png | 83471 | 281×280 | `5c188a1e04bc41c999581584f0d3326d649e81ae0f2b01ffd0338209fea6b404` | https://wx.e3861.com/sfyAdmin/Images/Doctor/942df850-b2b3-4814-a1b7-f450e92e5c01-280.png |
| 伍恒英 | 妇科 | 主治医师 | 伍恒英-妇科-主治医师-广东省妇幼保健院.jpg | 8842 | 267×280 | `60691d8d38986c94412cbfa68e72e5fcf393cb46ff239c495bcbc95057e2a112` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3f04156e-ea42-46ee-8124-75270b65f8a0-280.jpg |
| 李青 | 产科 | 主治医师 | 李青-产科-主治医师-广东省妇幼保健院.png | 71037 | 181×280 | `c7a551f1dc171764c096a35f54db4b9314eb993d09e27907cdc4f906e72d2403` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4d710a1a-b086-4a67-a701-0474ee63f0e4-280.png |
| 谭虎 | 生殖健康与不孕症科 | 主治医师 | 谭虎-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 6954 | 199×280 | `8803fe72da537ad5d72e5d8748bdbed194cf40ad3256685899fa4915ffeb45ed` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9b3abd5f-9539-419e-a312-b20b1ef74dc7-280.JPG |
| 许虹 | 生殖健康与不孕症科 | 主任医师 | 许虹-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 8342 | 185×280 | `aec4eea194af5ae7b20115f0445c5a66fb3c971e5d4ffce879b4a04c95f796d7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/73f877f0-153e-418d-ac2a-ecedbe7f1033-280.jpg |
| 肖宗辉 | 生殖健康与不孕症科 | 主任医师 | 肖宗辉-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 7170 | 199×280 | `7befa23abfd27d94741bd3f2ca1b5e55b223aaf5f7414aab8b005b3531b7dd0d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f9f9ece6-7327-41ec-b58e-7c08c0d083b5-280.JPG |
| 翁慧男 | 生殖健康与不孕症科 | 主任医师 | 翁慧男-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 7202 | 199×280 | `512910017d57174ba287902809d581396873e2049cf61978f54d3e395d3ba164` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e4b73c13-0550-4c4c-b172-e7dcb4d7e5f5-280.JPG |
| 张曦倩 | 生殖健康与不孕症科 | 主任医师 | 张曦倩-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 8811 | 199×280 | `16405a352c42ced489d715b248c1664a581861c44b6e6da0aa17b74a3c78ba27` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f487e6e8-75e4-4021-9a2c-7cdb2f180760-280.JPG |
| 李浩 | 生殖健康与不孕症科 | 主治医师 | 李浩-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 7799 | 199×280 | `74418f6503a20d0a61795083590512262e80441d98afc483e5f120520cbf503c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2edb742d-3809-417c-8bad-4047fb053e42-280.JPG |
| 刘风华 | 生殖健康与不孕症科 | 主任医师 | 刘风华-生殖健康与不孕症科-主任医师-广东省妇幼保健院.png | 88123 | 207×280 | `92491ba836a87eab8757558f7de445c0a0a34eb9bd08ced6e398f792f612c8a0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/edcd7796-4172-48c7-92b2-cd8eaa2f0f30-280.jpg |
| 陈烨 | 生殖健康与不孕症科 | 主任医师 | 陈烨-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 7201 | 199×280 | `8672c0254cfe4dde505ffc2f23a6db4c59dd1608a701540e8bd60c0682e4bb30` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6e3ec3f2-e444-4329-955d-f97703f0fb96-280.JPG |
| 黄菊 | 生殖健康与不孕症科 | 主任医师 | 黄菊-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 7383 | 199×280 | `5f194a64dd24d3c9ecbc3f073c63496e24c9278b137c377b64cec9a86abba85e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4e359bf1-28d3-4aba-af67-bf085f2d427d-280.JPG |
| 王松露 | 生殖健康与不孕症科 | 主治医师 | 王松露-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 8375 | 199×280 | `80e2ce0e0f430e89ab89097019ad07b2e00603767bfd9c2ac78d2a1fc560646f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f568f16a-8d0b-4fec-b9cb-602f5f0e10fc-280.JPG |
| 王芳 | 生殖健康与不孕症科 | 主任医师 | 王芳-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 8180 | 199×280 | `806b3263affcf858b6d9c2c8ba1bf428753f17b2bc8a6f833fd383dd4ff826e0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/87edd22a-7fc1-43fa-9768-dad94a3f1bb3-280.JPG |
| 郑毅春 | 生殖健康与不孕症科 | 主任中医师 | 郑毅春-生殖健康与不孕症科-主任中医师-广东省妇幼保健院.jpg | 7667 | 199×280 | `ca1b63e77733b67408f2f3683b425c3cb43f592a1290960d99459764dbaaa29e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/05651822-a254-40e9-8959-b7709781c2d8-280.JPG |
| 杜鹏 | 生殖健康与不孕症科 | 主任医师 | 杜鹏-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 7427 | 199×280 | `7607348a91cc978575c766c65cf0094438f0b5d86f1ad4272db6140b0ce0953e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0de133b5-1dd2-4232-a653-3fbee97945e5-280.JPG |
| 汪李虎 | 生殖健康与不孕症科 | 主任医师 | 汪李虎-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 7744 | 199×280 | `40f16ce33db2900f918ca12f6fe85aab1b18c3f27acf695cb5600fa2a8d420ec` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e058ff91-f3b2-4a2e-a6f4-fcf012a5535f-280.JPG |
| 董梅 | 生殖健康与不孕症科 | 主任医师 | 董梅-生殖健康与不孕症科-主任医师-广东省妇幼保健院.png | 62417 | 187×280 | `4a89b4770a94052e5dbbfaa2c280b0c6bdc9417cb45e79f0c5ff46f3bfcab094` | https://wx.e3861.com/sfyAdmin/Images/Doctor/dde15801-4a20-4fa4-a521-9e3ae5cd80f1-280.png |
| 张力佳 | 生殖健康与不孕症科 | 主治医师 | 张力佳-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 7932 | 199×280 | `5876d753f33bd6d823e7cf18b3dd39abaab479282e482ae06591bf0918c8bb97` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2432779a-2e4c-4e64-8d17-5ecf77122d79-280.JPG |
| 朱秀兰 | 生殖健康与不孕症科 | 主任医师 | 朱秀兰-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 7472 | 199×280 | `032a4aa4ed34fb0c18defdcbe03ab0d92a74ffcbc51577fdca8552b20142b561` | https://wx.e3861.com/sfyAdmin/Images/Doctor/92613ddf-1c7f-4b5d-8237-b568e06fa3e3-280.JPG |
| 陈成贤 | 三叉神经痛专病 | 主任医师 | 陈成贤-三叉神经痛专病-主任医师-广东省妇幼保健院.png | 66803 | 189×280 | `100ee52ffd44658c8123808ab2c98bbd77d43537f4e83102d56ffe3e2cc8bb91` | https://wx.e3861.com/sfyAdmin/Images/Doctor/dba8b529-e8e1-43ad-b44d-680c16da7808-280.png |
| 樊琳 | 生殖健康与不孕症科 | 主治医师 | 樊琳-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 8582 | 199×280 | `683c8e713e20d25c0ff3970cdf0b31d9ffd21b616ec116ed6f3f1bdb1bde7f92` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f8c4c347-da88-42ff-b71c-6e91ae9e2902-280.JPG |
| 李湘元 | 生殖健康与不孕症科 | 主治医师 | 李湘元-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 6587 | 199×280 | `4426f127e1d382fc06538afcf4f95b547ec4986ef65d6c5b42ee678f427fcd17` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3da8ac70-129a-429a-9014-e1d7676f9fa4-280.JPG |
| 林镇耿 | 中医科 | 主治医师 | 林镇耿-中医科-主治医师-广东省妇幼保健院.png | 69815 | 186×280 | `8a00b4e7cd835d5c8073e049650b54016469a9b5fdd340f2a8931a8c94370f7a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0ca12276-25c6-444d-9d00-599d7321b600-280.png |
| 钟添兰 | 中医科 | 医师 | 钟添兰-中医科-医师-广东省妇幼保健院.png | 70126 | 186×280 | `49945dd6c7ff3afa101e5fb5b879e056854c84170e944b2d2f63d3eb5aa4ea75` | https://wx.e3861.com/sfyAdmin/Images/Doctor/cf421ae2-5b0b-45f7-88ee-443fcafd7847-280.png |
| 邓雪梅 | 中医科 | 主任中医师 | 邓雪梅-中医科-主任中医师-广东省妇幼保健院.jpg | 6891 | 175×280 | `9130d476826c99d282549140f560c53490a4551b0778ab9665bb94db20dc1182` | https://wx.e3861.com/sfyAdmin/Images/Doctor/57934eed-8d33-4270-baa8-52a19b0e6938-280.jpg |
| 马书鸽 | 中医科 | 主任中医师 | 马书鸽-中医科-主任中医师-广东省妇幼保健院.jpg | 7367 | 213×280 | `221a578cbf0f3d4f074625c2c45115a1c84ae6cafac478fc994eb42fdc92c7c6` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fa9c0254-3e48-4a69-a8f8-4bf8be92bf3e-280.jpg |
| 何田田 | 中医科 | 主任医师 | 何田田-中医科-主任医师-广东省妇幼保健院.jpg | 8156 | 189×280 | `19970ee19b49d94142c01b235b07fbf0ba8b849f38dabe946c125f5fcd7aa511` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b455cea4-eeff-46cf-9abc-f2239bac879b-280.jpg |
| 郑小红 | 中医科 | 主任医师 | 郑小红-中医科-主任医师-广东省妇幼保健院.png | 71640 | 184×280 | `22f073739decde49ab00d0c3b7068459945b61f9b7472e53450c8a1c818dba44` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f8d54721-8184-447f-a69d-c35e648992fa-280.png |
| 邱少红 | 中医科 | 主任中医师 | 邱少红-中医科-主任中医师-广东省妇幼保健院.jpg | 7009 | 210×280 | `d9a5b320f5f3de9378eeb42eaa482fad1238345abcd6f8397d26ce69c61141b5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f0a0dfcc-ed2b-474a-b693-da53eb43dd7f-280.jpg |
| 张晓莹 | 中医科 | 主任医师 | 张晓莹-中医科-主任医师-广东省妇幼保健院.jpg | 7811 | 210×280 | `2cb26da28c13012f4aaa9117bd9d46b77bd5c14160aabd8b88be85e9a1869a4c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0bf3f1d3-c3b9-4c49-8e73-a66492f8c4ce-280.jpg |
| 宋曙霞 | 中医科 | 主任中医师 | 宋曙霞-中医科-主任中医师-广东省妇幼保健院.jpg | 7137 | 203×280 | `e16166f3370b2b206073e2f3a8ead7c55d418bb0b4be24ec860142be1db204c7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/854d05d2-d09f-4e63-96ab-08ba99cef090-280.jpg |
| 谢璐 | 中医科 | 主任医师 | 谢璐-中医科-主任医师-广东省妇幼保健院.png | 128040 | 229×280 | `dfab55be802583a28d81333372eaf30275ad1c5d1b4d33bc6f2f8391e850e8a3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c4faebbb-892a-4a36-9bd7-97d4d783b940-280.png |
| 陈炳豪 | 小儿骨科 | 主治医师 | 陈炳豪-小儿骨科-主治医师-广东省妇幼保健院.jpg | 7217 | 210×280 | `257593f07b5d3b24ac8b2b429373c7204eab89f3ceed93339c701adbf1f4e511` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0532d852-4598-4f3a-86b3-802e7105f779-280.jpg |
| 金龙 | 小儿骨科 | 主任医师 | 金龙-小儿骨科-主任医师-广东省妇幼保健院.png | 68986 | 185×280 | `d68f9d9f55b71bcd47ea7b4e4c7419f859bb49db84cbcc4df1463108784badcf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/40101bfe-58c7-4c57-9629-8821d230d38a-280.png |
| 张银婷 | 小儿骨科 | 医师 | 张银婷-小儿骨科-医师-广东省妇幼保健院.png | 64263 | 185×280 | `1d05059e24ba9ab6ac0feb733d97c0c4a112a876406e5ddb8bcdbe79c589e3dd` | https://wx.e3861.com/sfyAdmin/Images/Doctor/97747e3b-493b-4802-8b26-c6452fd6d0cb-280.png |
| 邓尚梁 | 康复医学科 | 主治医师 | 邓尚梁-康复医学科-主治医师-广东省妇幼保健院.jpg | 5240 | 199×280 | `a341ad52ae7cd2154eeb4d75c62eb8999f78e6fbb4c5d34c29087d5dc92be1c8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c21cd4dc-0af2-44e1-9a0e-bfce9ee6c43f-280.jpg |
| 宁静 | 儿童保健科 | 主任医师 | 宁静-儿童保健科-主任医师-广东省妇幼保健院.png | 74893 | 176×280 | `12f3de8d4fe6066867729e7ac1ac16226e60ca9764d3695b809eb11d7d5f8cf9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b7a10636-da2c-4641-9f30-962e6635a471-280.png |
| 柯海劲 | 儿童保健科 | 主任医师 | 柯海劲-儿童保健科-主任医师-广东省妇幼保健院.png | 68173 | 172×280 | `ad742c70c73887128d05b3eda715e37a951b7fd553310bd6700e9b532a67ffb1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3ac16453-5c9d-432a-a6e4-587f3c841dd1-280.png |
| 赵英 | 未标注 | 主任医师 | 赵英-未标注-主任医师-广东省妇幼保健院.png | 101378 | 220×280 | `818fca7de6de67193812a0ca834bd09a0f1816b62278877457e9747a940384c1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/88b45705-49fc-4367-b940-2b6c9db9deda-280.png |
| 卢秀霞 | 儿童保健科 | 主治医师 | 卢秀霞-儿童保健科-主治医师-广东省妇幼保健院.png | 54381 | 186×280 | `6dcd6cbcb622943296fae67bbfd1b30061287604567d1d39eb32169474d3ead4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b5da94cb-f814-40b7-989e-e9ff65c1a035-280.png |
| 刘瑛 | 儿童保健科 | 主任医师 | 刘瑛-儿童保健科-主任医师-广东省妇幼保健院.png | 83747 | 169×280 | `765e5ad7344d21020936cc566ecb3e1150fc949a8a549e836910eb0e0a47fbd3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7d1d3f73-009d-40c6-ad76-182380c10103-280.png |
| 吴春艳 | 儿童保健科 | 主任医师 | 吴春艳-儿童保健科-主任医师-广东省妇幼保健院.jpg | 6917 | 199×280 | `c1cb0b85b6bc06557f1f4cf7670cbaec1f7291a2226a43872b0e1655e34619ef` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b0c92c06-65b8-421f-8851-b071ac7bd138-280.jpg |
| 吴婕翎 | 儿童保健科 | 主任医师 | 吴婕翎-儿童保健科-主任医师-广东省妇幼保健院.png | 68227 | 175×280 | `ac859ba3969644d07945670e75e843101233398a475cfc279e289243b7bd7f49` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bf0fb6c2-2494-4600-95c1-c4f6d33a87e3-280.png |
| 黄维勇 | 未标注 | 主治医师 | 黄维勇-未标注-主治医师-广东省妇幼保健院.png | 78456 | 234×280 | `5573095d6ee355639120402987735579a1f30e399f7095d2129ce788ef1d763b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ee37a671-8a61-4919-bc65-b8a9d98cdd28-280.png |
| 朱然科 | 儿童保健科 | 主任医师 | 朱然科-儿童保健科-主任医师-广东省妇幼保健院.jpg | 7267 | 215×280 | `9b497fb388f1cf1742a0b42a9f72c66fbb55322e179e2b33bbc6e1027fa105c8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/29501aa0-f276-45e0-8770-a27d621fb384-280.jpg |
| 陈小燕 | 儿童保健科 | 主治医师 | 陈小燕-儿童保健科-主治医师-广东省妇幼保健院.png | 72767 | 189×280 | `11ffda8a7ed082ce7198615f26eb72502f413f2050a5dbb8750280aba8954361` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1d20024c-125e-457d-b147-319988ea0875-280.jpg |
| 茹晓平 | 体检科 | 主治医师 | 茹晓平-体检科-主治医师-广东省妇幼保健院.png | 112327 | 251×280 | `da8dcb978ff945aa639ea8d03d80face5066d884b410553479d96cc7c271a3de` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e200cac4-7749-4c50-9db8-157b2df13c2e-280.png |
| 魏然 | 产前诊断 | 主任医师 | 魏然-产前诊断-主任医师-广东省妇幼保健院.png | 43850 | 187×280 | `0e11343fffc43e12e91b752f0864899a9d0559c20489604bc40fab86d86fe67c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a8412244-e368-4944-a478-6fc860a7f6f0-280.png |
| 李玲 | 产前诊断 | 主任医师 | 李玲-产前诊断-主任医师-广东省妇幼保健院.png | 49241 | 187×280 | `b0c51589af9a3e1c5dacd82e1da8be74f7a8975c570230f3d562bcb2b6a4a70f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3e310d49-06e6-45fd-b4f0-3d17b64c5341-280.png |
| 朱娟 | 产前诊断 | 主任医师 | 朱娟-产前诊断-主任医师-广东省妇幼保健院.png | 40104 | 187×280 | `24d2a1c3d79af7595717c4ceaf22c3c9a51b355992a6469be0cca6f86e3a319a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9e0189ef-2e5c-4b0e-bc65-001cd45763ef-280.png |
| 麦明琴 | 未标注 | 主任医师 | 麦明琴-未标注-主任医师-广东省妇幼保健院.png | 76046 | 194×280 | `23d48ebc8e07370155285ed0aef861b34f9def99ecf7538cb4e111e88d6dfdf3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/38f3a2b6-25fe-4cff-919e-56fc30036f2f-280.png |
| 邓恋 | 麻醉科 | 主任医师 | 邓恋-麻醉科-主任医师-广东省妇幼保健院.png | 70980 | 187×280 | `6d21bb6df1177af857ce311bedccee5af751bbccbe3244088c21553e9cebbd1b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fa6dfefb-c0a5-45f1-884d-3dc145c97d48-280.png |
| 刘晶 | 麻醉科 | 主任医师 | 刘晶-麻醉科-主任医师-广东省妇幼保健院.png | 62418 | 187×280 | `22d2c63cfd8628f298d6d5c889639e213dcad828cbd61a6ca055bcf4995da7bb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fd804b20-ab61-4c06-b424-02cbba4f22ad-280.png |
| 胡恬 | 小儿铅中毒 | 主治医师 | 胡恬-小儿铅中毒-主治医师-广东省妇幼保健院.jpg | 6341 | 199×280 | `95e4f07d5dce2dba4b542ebabb556e94d98bf861b3c24f13dfc083708e1a095c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fafbfefc-a8e7-4ec3-b415-c046438be5a0-280.jpeg |
| 马媛媛 | 普通儿科 | 主治医师 | 马媛媛-普通儿科-主治医师-广东省妇幼保健院.png | 81355 | 190×280 | `157d3820e1ceb718d1f9c4d101d4be6d23e2c31b38dea29fe356c9758eb69048` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ce065ed7-df78-4377-83f7-f0f7f6e4b356-280.png |
| 李容汉 | 普通儿科 | 主任医师 | 李容汉-普通儿科-主任医师-广东省妇幼保健院.png | 90147 | 190×280 | `410cf576d4e0945fc859554bf8ace9ebc5c99033ba8fe4a1d479b67d60473e44` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bedb9b87-d1e8-46f6-93cb-1c54559df9d7-280.png |
| 李敏敏 | 普通儿科 | 主任医师 | 李敏敏-普通儿科-主任医师-广东省妇幼保健院.png | 64759 | 163×280 | `1a327381e185dfc6f3ed1ff73235c5c55a2c04d41bc33df5c7626639b82d94a2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f80c84e9-3d71-4457-a686-7e616188043b-280.png |
| 彭淑梅 | 普通儿科 | 主任医师 | 彭淑梅-普通儿科-主任医师-广东省妇幼保健院.png | 90959 | 187×280 | `cf42ba12a955d3929ca9df1f618b992d32e0ab64f80d21dcbf51a796b48bda6e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bbcef78c-07e2-479a-8871-bd909ea77356-280.png |
| 黄冬平 | 普通儿科 | 主任医师 | 黄冬平-普通儿科-主任医师-广东省妇幼保健院.jpg | 6045 | 187×280 | `379eb0901c15efde6aefc5c97e15fde61036c22fdef11072ebf7029049244844` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c8ab4d90-2350-47b2-88d2-5bb4a867828d-280.jpg |
| 陈运彬 | 普通儿科 | 主任医师 | 陈运彬-普通儿科-主任医师-广东省妇幼保健院.png | 159615 | 284×280 | `1a29257d03214f2f5fa7711bd5091b7e810b45853c2679a4240359218bfc17a8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2e189565-d03c-4869-a0df-7ce446090eaf-280.png |
| 蔡双明 | 未标注 | 主任医师 | 蔡双明-未标注-主任医师-广东省妇幼保健院.jpg | 8055 | 259×280 | `7f5daa3900e33eb1ab474283aecc78392c4b25baa9561d915719d698d4c004de` | https://wx.e3861.com/sfyAdmin/Images/Doctor/71e7b9e2-2aa3-4c1a-be73-53e807d3e9b5-280.jpg |
| 朱冬生 | 儿童保健科 | 主任医师 | 朱冬生-儿童保健科-主任医师-广东省妇幼保健院.png | 60687 | 176×280 | `cbbedc42d3238ee54760c86884db1975c394eb23151155cbc1035aa35cca65b8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/68070d12-7b32-4493-a7cf-f3e5fa60f8b3-280.png |
| 李新 | 乳腺科 | 主任医师 | 李新-乳腺科-主任医师-广东省妇幼保健院.jpg | 9021 | 261×280 | `f15c22493ce5a8630ab3d60e30f64843e37b37d90470950c40ea1934c9e078f7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/982daee9-e048-47ec-abfc-93af5ca75a65-280.jpg |
| 彭武江 | 儿童保健科 | 主任医师 | 彭武江-儿童保健科-主任医师-广东省妇幼保健院.jpg | 6326 | 178×280 | `6939f57c2926e8ea8c69063a2e733bacdfe3777ec4897b3652f0774ab8ab4448` | https://wx.e3861.com/sfyAdmin/Images/Doctor/262a304d-11af-49b3-a327-598a2c989fea-280.jpg |
| 肖雨 | 儿童保健科 | 主治医师 | 肖雨-儿童保健科-主治医师-广东省妇幼保健院.png | 74375 | 189×280 | `511f007440abf37216e782ae9646980bb93645cacdd6b8753802e6d4eec19b37` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3b534875-8460-41be-bd05-a5c90163428f-280.jpg |
| 王丽敏 | 超声诊断科 | 主任医师 | 王丽敏-超声诊断科-主任医师-广东省妇幼保健院.png | 115162 | 216×280 | `a16d72dff7f0ac5842d982c4755b5ebb3e4d3eba33c4748656d5ea4d18e573d3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/87528976-d94a-4c6f-ab3d-6259e9cc3d80-280.png |
| 闫凤英 | 产科 | 主任医师 | 闫凤英-产科-主任医师-广东省妇幼保健院.jpg | 7288 | 205×280 | `8a33435a4c0a5370f1212382a6b2390d28f443bc32e4ec9804f535ffd4dd2148` | https://wx.e3861.com/sfyAdmin/Images/Doctor/83561c7c-c990-4036-9ea5-898f18c74cae-280.jpg |
| 周宇恒 | 产科 | 主任医师 | 周宇恒-产科-主任医师-广东省妇幼保健院.jpg | 5839 | 200×280 | `dbc0a4f06931290781383b342c6407d849eff40c2f571d64f34d40cfe3f9a903` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ad962cca-13ad-4efb-8f5d-02148b9984e5-280.jpg |
| 李慧 | 产科 | 主任医师 | 李慧-产科-主任医师-广东省妇幼保健院.png | 96404 | 251×280 | `003021126fd0272d1197ad33234f1393573b6624f10b4e00e59014997a8a50f2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/40bd3471-eeab-4c63-a76e-75bd94b38539-280.png |
| 刘丽霞 | 产科 | 主任医师 | 刘丽霞-产科-主任医师-广东省妇幼保健院.jpg | 5176 | 190×280 | `0cf3bf58a05b85413a8bfa7d792194e732ba8f1c59e92fd33c0bdcf509b4d021` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8e7d9583-f50a-4e3b-b48a-03a7b4abb04d-280.jpg |
| 彭端龙 | 产科 | 医师 | 彭端龙-产科-医师-广东省妇幼保健院.jpg | 5572 | 187×280 | `79bed2b337f2d71f01fe6c47e5f554a35d54d6f88858c33e6054c9e905690359` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1954909e-6b11-48f2-8e8d-432c90c187a4-280.jpg |
| 谢玉欢 | 产科 | 医师 | 谢玉欢-产科-医师-广东省妇幼保健院.jpg | 6571 | 187×280 | `6a24874e1e0334daf5754452dfd0d140fb60f6c84d20a78f9058e32d559a09ba` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e7a389aa-231f-413c-8aa6-9e900fc1fba9-280.jpg |
| 赵君 | 产科 | 主任医师 | 赵君-产科-主任医师-广东省妇幼保健院.jpg | 8385 | 192×280 | `0937a48f8565d9588a6a99c3b86c7fd46b97366df6ccc2d6158a96fcf6a4fee1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/296236d0-8479-48eb-b6c2-ae6567d3b8c4-280.jpg |
| 杨艳 | 妇科 | 主治医师 | 杨艳-妇科-主治医师-广东省妇幼保健院.jpg | 7505 | 280×280 | `c364874009d0161c2792d3792f570abd9a127dfc105c6d5de1176683031e5af5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0acc157c-c43b-4b32-b28a-5acbd2fab37e-280.jpg |
| 徐珍 | 妇科 | 主治医师 | 徐珍-妇科-主治医师-广东省妇幼保健院.jpg | 6552 | 224×280 | `d57599101382fbf944956d5e9c06ccf192f6e9ccdba24dc29dc5f9c4ab4e55cc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7703de12-59db-4f2a-bf72-14a1f2a8eed5-280.jpg |
| 马瑞霞 | 产科 | 主任医师 | 马瑞霞-产科-主任医师-广东省妇幼保健院.jpg | 6067 | 187×280 | `7d38ffeb4bfda273020147a6c03a0f9d8afa06fe025a8849c6602657b981b841` | https://wx.e3861.com/sfyAdmin/Images/Doctor/17139ea6-4e2f-4e8e-a6dc-cd68fa703bed-280.jpg |
| 林小红 | 产科 | 主任医师 | 林小红-产科-主任医师-广东省妇幼保健院.jpg | 7091 | 187×280 | `369a9de0a2fcdc6dd1127d618d8dd367c39c8eb9e22854ba54611b30c6b1f66c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/624f696b-74fe-48d7-8ba2-e507e600cf60-280.jpg |
| 黎云 | 产科 | 主任医师 | 黎云-产科-主任医师-广东省妇幼保健院.jpg | 5885 | 187×280 | `9f7e94ac34ab6f611801564b1c6e5222864b57f3d755c234512f0592497e41a7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b680d6bf-8025-4d81-ac4d-f90b5d84e7f5-280.jpg |
| 殷文静 | 产科 | 主任医师 | 殷文静-产科-主任医师-广东省妇幼保健院.jpg | 6332 | 187×280 | `fac28d1e510c21f415295f4a4c16232fbd89b9688dc4aa4943134bb95f5484ad` | https://wx.e3861.com/sfyAdmin/Images/Doctor/aabd17bb-9f72-424a-a00f-e737e6d6c660-280.jpg |
| 刘颖 | 生殖健康与不孕症科 | 主任医师 | 刘颖-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 8856 | 199×280 | `900f70dd00040708bf78490344136df91b193896d6c975c140a4206894b14cfe` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2d159e27-4080-4bc7-bfe2-57e4492523cf-280.JPG |
| 饶美兰 | 产科 | 主任医师 | 饶美兰-产科-主任医师-广东省妇幼保健院.jpg | 6320 | 210×280 | `78526af98779ac0254b70c50177205a97d14bec392b393cda1f35a69963dc385` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d27dd621-7a64-427b-8e92-7ae5439d7d8c-280.jpg |
| 黄咏欣 | 产科 | 主治医师 | 黄咏欣-产科-主治医师-广东省妇幼保健院.jpg | 7599 | 200×280 | `89be6ffe4b3247c70bfce0f88e17770470de62687503e09757707338838ccac2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7a3a776f-88e1-456b-9638-bcde5db0f0f9-280.jpg |
| 叶秀桢 | 新生儿科 | 主任医师 | 叶秀桢-新生儿科-主任医师-广东省妇幼保健院.jpg | 6127 | 187×280 | `7824408cc1c3d7a6f7621e0e566f9c18e6ff12d3cf0ac119441344c5823a2217` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b443c570-34d9-431f-ba40-5ee2d4040cd7-280.jpg |
| 罗鑫刚 | 康复医学科 | 主任医师 | 罗鑫刚-康复医学科-主任医师-广东省妇幼保健院.png | 102487 | 263×280 | `332b2e6ec8e5e9bac021f276b48de2f90c4c4791c5ab13a2196bde8587a57d39` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e471cf79-07e3-44fa-92a5-f6c0e457560d-280.jpg |
| 原丽科 | 未标注 | 主任医师 | 原丽科-未标注-主任医师-广东省妇幼保健院.jpg | 6714 | 186×280 | `1a4c86a6287c440fbc13d7ed7f4492dec91ef32a65993ebbf5e0e2738aabaf6f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/730bfbcc-8a3f-4b9a-b8c9-33ecddc5f166-280.jpg |
| 田松 | 新生儿外科 | 主治医师 | 田松-新生儿外科-主治医师-广东省妇幼保健院.jpg | 6639 | 200×280 | `cf92fd0b2a41cdff3b0d1d9db3e465ecb11f9ef0b30624eea79d789b1d384295` | https://wx.e3861.com/sfyAdmin/Images/Doctor/731aa943-42d4-4d88-80b1-d08a262343a1-280.jpg |
| 吕成超 | 小儿外科 | 主任医师 | 吕成超-小儿外科-主任医师-广东省妇幼保健院.jpg | 6673 | 223×280 | `b89cd95f59f38e5925de550b84fcde00a05a58d371aa57d603d51bffacea51f0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/adc7e567-61e4-4469-b7a0-0a2117d6a2fb-280.jpg |
| 李铁 | 小儿外科 | 主治医师 | 李铁-小儿外科-主治医师-广东省妇幼保健院.jpg | 5185 | 187×280 | `0d74eef98792508163eb8152eba81374f495f12b0d826ea9de392f861dfe7258` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bd0e735d-d163-4a07-9404-6d12acf1c2c3-280.jpg |
| 刘业根 | 小儿外科 | 主治医师 | 刘业根-小儿外科-主治医师-广东省妇幼保健院.jpg | 8155 | 280×280 | `4584952ac0b19bb50b94caa438ae36a068894bc1bba8138d3c038974dcb344e8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0976bbc5-c0c7-4cdd-ab83-850e8300169c-280.jpg |
| 苏念军 | 生殖健康与不孕症科 | 主任医师 | 苏念军-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 9110 | 199×280 | `3000339b6981d0b2e2c7b5b66332085612e68519e95dcec8ac19372e1cc254c9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6ac11a4e-230c-4182-9029-f96d84200a7f-280.JPG |
| 黄翠玉 | 生殖健康与不孕症科 | 主任医师 | 黄翠玉-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 8681 | 199×280 | `9d121285807291b38c6f60affdebf677aa3a13daa013d2d116d14a86dd73a732` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1484ddae-a3e6-4af4-9af4-a51dfd06ecac-280.JPG |
| 齐诠 | 生殖健康与不孕症科 | 主任医师 | 齐诠-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 9038 | 199×280 | `ad292f3f404b00e6ca6cae1a9aee0403bc84df580f3b33c80d91beacab5212f5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6359c6dc-ec07-4e0b-813b-ef4dd85e1231-280.JPG |
| 农璎琦 | 生殖健康与不孕症科 | 主任医师 | 农璎琦-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 7140 | 199×280 | `369c9dcf81623be0de9f86519022bf26ddaf59771389f1c6efa2a4f9b7289d7f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5fafb5fd-bfea-4fed-b876-93f17c6be97e-280.JPG |
| 罗燕群 | 生殖健康与不孕症科 | 主任医师 | 罗燕群-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 6531 | 199×280 | `ac03f657b18eead6eaf6cf8262204889892eda7574bd90cfd8e04c31a7305ae3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5fb29e9e-bb3c-4aa7-960d-6a2d677db784-280.JPG |
| 吴喜才 | 内科 | 主任医师 | 吴喜才-内科-主任医师-广东省妇幼保健院.png | 73948 | 187×280 | `cace229878931e2262a933ca8e9b4ed7659b5e35ec2db52837f255661d0a596c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/cf644f7f-f2b3-4c3c-94b2-5cf5d011d81e-280.jpg |
| 胡春玲 | 内科 | 主任医师 | 胡春玲-内科-主任医师-广东省妇幼保健院.png | 73201 | 186×280 | `ed35d5d847ad63690204c2f6af7fd9da60969df1fccabdd4cbf59ddd37476faf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ccc2d01a-15f4-42fa-8cd1-71488a420ede-280.jpg |
| 何柳瑜 | 内科 | 主任医师 | 何柳瑜-内科-主任医师-广东省妇幼保健院.png | 73234 | 187×280 | `450712c6f2ce1ff6a0df6a14487eb1d6e553b6187ff65927ca1a276b0b697f8e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1b1469d2-bc7d-4ae6-b930-6a8788b3fc08-280.jpg |
| 邵光 | 内科 | 主任医师 | 邵光-内科-主任医师-广东省妇幼保健院.png | 74524 | 210×280 | `c7259138b2bcc936b0086dad11ea370e3fa402fe891f830cee7d36ad009f3895` | https://wx.e3861.com/sfyAdmin/Images/Doctor/897ae883-1671-4e66-bb08-dfa997994a28-280.jpg |
| 李静 | 眼科 | 主治医师 | 李静-眼科-主治医师-广东省妇幼保健院.png | 75513 | 187×280 | `f73516d94fc72370a679ca70b8a846fd21b1f28e54063130ea413d3ab03a1ef5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a4892c02-38fd-401c-b811-7b9380ba3749-280.png |
| 陈胡林 | 皮肤性病科 | 主任医师 | 陈胡林-皮肤性病科-主任医师-广东省妇幼保健院.jpg | 5901 | 190×280 | `f9f8a02805925baaa709c4b4a69369721a7c578970756b24e363db9af0983725` | https://wx.e3861.com/sfyAdmin/Images/Doctor/72596073-518b-460b-948a-53442fbb3b6c-280.jpg |
| 肖英 | 妇科 | 医师 | 肖英-妇科-医师-广东省妇幼保健院.png | 105641 | 234×280 | `797f5dcc758ad827bc453e9e4b147acdc668dea3b198ae67672ef7d591bb3ea7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5ae3d2e0-8fa6-47e7-bec5-b00517958200-280.png |
| 李屹 | 妇科 | 主任医师 | 李屹-妇科-主任医师-广东省妇幼保健院.png | 105389 | 196×280 | `721e569285930812355412ffd00672db44b6e830293acf337ccb37f78931d4f7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d611ab21-93c3-4cd2-8d53-a72cc4ec230a-280.png |
| 孙力 | 生殖健康与不孕症科 | 主治医师 | 孙力-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 8178 | 199×280 | `7f847c5b7150fb35edc735503cc391e789421de286019bc45b873995976d9684` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4e02956e-d57b-48df-a463-2c19ecc6d6fe-280.JPG |
| 曾珊珊 | 妇科 | 医师 | 曾珊珊-妇科-医师-广东省妇幼保健院.png | 124112 | 225×280 | `ad3fdd08492093a7332b71181675f29c388ba00be977afe99d9d805c28eb1c4d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3fec0967-0fa7-40c8-aa39-d37c07ac6a7c-280.png |
| 陈冰冰 | 妇科 | 主治医师 | 陈冰冰-妇科-主治医师-广东省妇幼保健院.png | 105494 | 205×280 | `d891e00425388aafb857fe8e40caa55a78610c446e903d8581ed715e1231f220` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a518f939-e639-477c-b63e-1fd3409647c2-280.png |
| 李小芳 | 产科 | 主治医师 | 李小芳-产科-主治医师-广东省妇幼保健院.png | 107889 | 270×280 | `e52683e26e0bdfa74bfecc3305f675ef2a0690e365f0a71887e5f695a28491b4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/853a3d5a-abcf-4a9c-8a07-3f304a242bfa-280.png |
| 李智敏 | 妇科 | 主任医师 | 李智敏-妇科-主任医师-广东省妇幼保健院.png | 88817 | 227×280 | `f3ef10ec05174eb3aa51fd7ec09076ccf3e17c303ff8fdbb480bcd16c0e85c67` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e6fff01a-4396-4547-a14b-073c773fc972-280.png |
| 彭秀红 | 妇科 | 主任医师 | 彭秀红-妇科-主任医师-广东省妇幼保健院.png | 98637 | 216×280 | `ab45c6528fb254498dc9b9c5b6dbe5624b6ffbfff9ca76517463c08c71f0a05b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7c55aea0-be7f-44c2-9f60-4d429a6d9c26-280.png |
| 黄彩彩 | 妇科 | 主任医师 | 黄彩彩-妇科-主任医师-广东省妇幼保健院.jpg | 6988 | 186×280 | `030efa2324c393692e242123343619de9fd34595624519ae463b57bdbd68851e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2005d43d-5c3c-4628-b7d5-fd7023b7d1b3-280.jpg |
| 邓庆珊 | 妇科 | 主任医师 | 邓庆珊-妇科-主任医师-广东省妇幼保健院.png | 71459 | 211×280 | `87948a45d874b83cdf5d2c44b3a18168eb9ea12d1146a0b92aa1e27759d46776` | https://wx.e3861.com/sfyAdmin/Images/Doctor/921361bd-f9e7-4fda-9d50-234269827147-280.png |
| 赖贺 | 产科 | 主治医师 | 赖贺-产科-主治医师-广东省妇幼保健院.png | 75737 | 219×280 | `a8d2f7024b327a71348a3c2f129568a21bea73a8b3f6ac25c59eab885d529fcb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c1f47c60-8a37-43f7-8b20-10d1f61bd41d-280.png |
| 蔡仁燕 | 妇科 | 主任中医师 | 蔡仁燕-妇科-主任中医师-广东省妇幼保健院.png | 76813 | 233×280 | `05c3eb784b4ce85f51d3cce9a0fe803c5d6221abff08e6de0e0c712c448b7fb6` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3f65ca55-731a-4c5d-b00e-f7396f242cfa-280.png |
| 詹新林 | 妇科 | 主任医师 | 詹新林-妇科-主任医师-广东省妇幼保健院.png | 84844 | 244×280 | `fcb6849b0d482419b59e1e6c57588707e90b1615e36caf279ca4c42cccf59b39` | https://wx.e3861.com/sfyAdmin/Images/Doctor/653d0a32-8ef9-46d2-b3af-009e55f0e47d-280.png |
| 谢芳 | 妇科 | 主任医师 | 谢芳-妇科-主任医师-广东省妇幼保健院.jpg | 7275 | 248×280 | `2506d3f9886a8a04da0dd6dbfb3300feef83480079dd5b607658ae4ef19b8f02` | https://wx.e3861.com/sfyAdmin/Images/Doctor/52b4cc35-6a47-40d5-a0c2-860197b8c6d3-280.jpg |
| 钟沅月 | 妇科 | 主任医师 | 钟沅月-妇科-主任医师-广东省妇幼保健院.png | 93501 | 193×280 | `cc2df79b49a42768173c8178a4c31370f641bc0586df7cd72c8d35e5982f912a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/39ce2383-325e-4d3e-a0d3-c062263b79b9-280.png |
| 江雪芳 | 妇科 | 主任医师 | 江雪芳-妇科-主任医师-广东省妇幼保健院.jpg | 6054 | 178×280 | `afe7d54f864ee578ee52454e8415ec9623383c6caf885c9a3bdc1a3faea7446b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ea4f4259-fcc0-4564-be4d-26c0a192586d-280.jpg |
| 杨伟健 | 未标注 | 主任医师 | 杨伟健-未标注-主任医师-广东省妇幼保健院.png | 56306 | 187×280 | `77fb4d2e799d71a5e35fbf416370ea96d0f0fc48e17f01763bfca1e2b76fc6bc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e0fba881-aec6-4c42-84ba-e08b8c1c8b3c-280.png |
| 骆婉婷 | 妇科 | 主治医师 | 骆婉婷-妇科-主治医师-广东省妇幼保健院.png | 86598 | 197×280 | `69d2734b76ac5469925e7b855f4b2fe6ae55a8e405753edd8105dc33024aeb79` | https://wx.e3861.com/sfyAdmin/Images/Doctor/cdf6c61f-ea8b-420c-95ec-d8f622ae0736-280.png |
| 刘盼 | 妇科 | 医师 | 刘盼-妇科-医师-广东省妇幼保健院.png | 132675 | 230×280 | `bc9624735b7e0c9cb52127556ab8deede22067a062b4b7d8c89fed03bfcbcfee` | https://wx.e3861.com/sfyAdmin/Images/Doctor/38a43ee8-c0bd-4f05-ae3f-bdd3bf7a72cf-280.png |
| 黄晓晖 | 妇科 | 主任医师 | 黄晓晖-妇科-主任医师-广东省妇幼保健院.png | 97026 | 186×280 | `238e96010e7cc79136fb219cbb1061dc01d08dd423f98ec24d564815ab7d6631` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7c332213-cd1c-4ab5-8e29-88b3d9bc2760-280.png |
| 丁堪铄 | 妇科 | 主任医师 | 丁堪铄-妇科-主任医师-广东省妇幼保健院.png | 91159 | 263×280 | `2ff3e0976239895e53d1c74ea51314b6a8b5fed222ab5742426bf00503efb2ca` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9ea9e104-0d70-4787-b60b-f297e74c09c7-280.png |
| 余凡 | 妇科 | 主任医师 | 余凡-妇科-主任医师-广东省妇幼保健院.jpg | 8195 | 194×280 | `fb4da1dff2c3bbfa88e62f27b3b35db422d3ba7f86fd62f6bbe6193d592027ba` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3e9de951-3a15-4101-ac15-e049bfc9d4fd-280.jpg |
| 廖碧翎 | 妇科 | 主任医师 | 廖碧翎-妇科-主任医师-广东省妇幼保健院.png | 90261 | 205×280 | `aa4845d624f566a38c72eda307105ba6e3a5e690029eff76c71ac2a9a4ef3ab9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/eff48004-5752-4dee-8749-a4dadd473106-280.png |
| 韦相才 | 妇科 | 主任医师 | 韦相才-妇科-主任医师-广东省妇幼保健院.jpg | 5464 | 187×280 | `3edc12c43125fc23e1d2d010fb6df8a348318533c7cfde6092a96d56d9e6dfa0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a04caa67-9c08-44b2-a408-40f14ffac092-280.jpg |
| 徐惠锟 | 早孕关爱 | 主治医师 | 徐惠锟-早孕关爱-主治医师-广东省妇幼保健院.jpg | 6091 | 176×280 | `673c53c799c83a0020511ae9729bbd66d79ee27b2c26fbfe078dabc27be4f8fc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/217a4062-8a75-4c12-abfa-b46c180e0cd0-280.jpg |
| 麦彩园 | 产科 | 主任医师 | 麦彩园-产科-主任医师-广东省妇幼保健院.jpg | 8376 | 280×280 | `4150063c391b0dd505955440c4277cf67a896a59b2f2cdccd05f6845d815b69b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/34f6c27b-f19b-4605-8b5b-79c55af3d138-280.jpg |
| 陈树汉 | 小儿泌尿外科 | 主治医师 | 陈树汉-小儿泌尿外科-主治医师-广东省妇幼保健院.png | 59502 | 182×280 | `9bda3577c5568500142be588142a512f0c40aed94dc24d3795a11297a25969a5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/dea2269b-7f48-45f9-be86-8af552939f9b-280.png |
| 石通 | 小儿泌尿外科 | 主任医师 | 石通-小儿泌尿外科-主任医师-广东省妇幼保健院.png | 57189 | 159×280 | `315d4efd9dc4bf29f623df3f404abe66cfcfc05fddc638014fa1c3dc212a696c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2a32e442-f566-47f2-a2cf-d4d1c63715a5-280.png |
| 苏晓华 | 产科 | 主治医师 | 苏晓华-产科-主治医师-广东省妇幼保健院.jpg | 5327 | 200×280 | `9cbe654ac4c4ce22a6a225078ff8f858c141f7f88a4193a43a52deb12b12f092` | https://wx.e3861.com/sfyAdmin/Images/Doctor/68d5a4c3-37b1-4b95-9831-a10a265bbfe8-280.jpg |
| 陈嵘 | 产科 | 主任医师 | 陈嵘-产科-主任医师-广东省妇幼保健院.jpg | 10117 | 420×280 | `8588e33f9c8e02ec770370620f6a0bd12c9d4028c249a0306e87283227386541` | https://wx.e3861.com/sfyAdmin/Images/Doctor/787312cf-e8f1-4322-9fea-ddc167bc237d-280.jpg |
| 赵莉娜 | 产科 | 主任医师 | 赵莉娜-产科-主任医师-广东省妇幼保健院.jpg | 6752 | 214×280 | `43c3433f34a3f287f02f17d4735a0d033c950e8ff7d28c61dab824dfefe7786e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0593ac95-973a-4ffa-bce8-f715ab0d2f6b-280.jpg |
| 吴锦华 | 妇科 | 主治医师 | 吴锦华-妇科-主治医师-广东省妇幼保健院.jpg | 6810 | 244×280 | `4cf3ee41fae27499a654d995538bb493eaee744723d1afc178539be095738a3a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b0478942-57e2-450e-b75a-352c8cba9399-280.jpg |
| 王铜朗 | 妇科 | 医师 | 王铜朗-妇科-医师-广东省妇幼保健院.jpg | 7021 | 210×280 | `bc7a1c9c367b945ca2ec408a70b120f27ddb35b545c94ced522ef2612d1403ce` | https://wx.e3861.com/sfyAdmin/Images/Doctor/44bdb6d5-2179-4b66-b4f0-c74fc07150c9-280.jpg |
| 陈祥楠 | 未标注 | 主任医师 | 陈祥楠-未标注-主任医师-广东省妇幼保健院.jpg | 7059 | 187×280 | `95c39777c980210aec1708138c34a5c1e39cbaf02affead928303b4158791848` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b4c93ad4-4d98-4371-9efd-f1809336ef41-280.jpg |
| 赵春梅 | 妇科 | 主任中医师 | 赵春梅-妇科-主任中医师-广东省妇幼保健院.png | 120622 | 278×280 | `25e3ad3d0d3e2ad1f48d7c3161d140764726811bbab869329abf9623e620ddab` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ea5ee2bf-7ed3-45f7-9892-d8da642359cf-280.jpg |
| 关心怡 | 妇科 | 主治医师 | 关心怡-妇科-主治医师-广东省妇幼保健院.png | 68200 | 280×280 | `18ca568c5f000456e95a6ef570a147fc281aaaae17e7cd788c1cccca3d7d4bb3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/70a098f8-8dc5-4e86-af76-3cdc4489e852-280.png |
| 纪淑玲 | 未标注 | 主治医师 | 纪淑玲-未标注-主治医师-广东省妇幼保健院.jpg | 8003 | 247×280 | `d372c9703f1cd31e6b9729aa623d395bcfcac04da35bc5640e73066d778b2074` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3491dfe4-240d-4a5b-a24b-3475399d370b-280.jpg |
| 胡财喜 | 中医科 | 主治医师 | 胡财喜-中医科-主治医师-广东省妇幼保健院.png | 82117 | 349×280 | `5af853a0965be1303d3aa8a76647b6e6131e0fbd451c6647a892064879f872a7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/deb62b7b-72a0-4023-9ccc-6d12c1f236d3-280.png |
| 刘文娟 | 生殖健康与不孕症科 | 主治医师 | 刘文娟-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 8994 | 199×280 | `483d305c947003895e5fd712c5965596fb0b2795fd509a7a2a308dfd87f1a2f3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a4397c41-95ac-4785-a49f-136463afe47c-280.JPG |
| 曹昉欣 | 儿科 | 医师 | 曹昉欣-儿科-医师-广东省妇幼保健院.png | 89204 | 202×280 | `c3c53535ced74aef6f9340ea6216d340385615e1c9f8ca158e40ceda1ddec07c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/aecdf061-dc86-437a-a386-b4f5bc0a4e46-280.png |
| 何雪仪 | 产科 | 主治医师 | 何雪仪-产科-主治医师-广东省妇幼保健院.jpg | 8408 | 280×280 | `a70a2f33d6c1598db38b53244c4ff17bbe0d16173175c35bed067c1a03856415` | https://wx.e3861.com/sfyAdmin/Images/Doctor/caff0980-4e0c-4b09-80c1-333cdedc614a-280.jpg |
| 张煦 | 妇科 | 主治医师 | 张煦-妇科-主治医师-广东省妇幼保健院.png | 89480 | 193×280 | `333ed7adf6d63ca498624c8676eed0964cd62832a325a2ba0a459ca92e39bdb9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9974f27a-6681-4c5b-9492-da9f270cefd5-280.png |
| 夏学颖 | 医学美容科 | 主任医师 | 夏学颖-医学美容科-主任医师-广东省妇幼保健院.jpg | 7295 | 275×280 | `4bd5a6ec2178f1319c7ce0818bada16c1b7f288ded5081fff795d14706dbd6f2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/68e4ad79-7306-4161-a3fd-dc90c4b96e62-280.jpg |
| 吕杰 | 产科 | 医师 | 吕杰-产科-医师-广东省妇幼保健院.jpg | 6319 | 158×280 | `25f2df7f030640c7ae694497c12d00c9ceb7ae40104ff95591a53288951b05c0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b064cf04-8235-4e28-9fd5-98f28a333087-280.jpg |
| 王俊平 | 新生儿科 | 主任医师 | 王俊平-新生儿科-主任医师-广东省妇幼保健院.png | 67281 | 167×280 | `61747afbe5f9ea70690ca6f8abc6f8939b2a40028d622b62ea2a52d5f7fd7d0c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/00bf8402-db1c-495c-8eab-21effcb103a1-280.png |
| 周雯 | 儿科 | 医师 | 周雯-儿科-医师-广东省妇幼保健院.jpg | 5808 | 158×280 | `d1b016be3588173b795977172c284fb33886aa2d4a00c5a3967f9e45259702b8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ee29212a-d2d5-4e74-884b-d5d4aa1b5e18-280.jpg |
| 龙芳 | 新生儿科 | 主任医师 | 龙芳-新生儿科-主任医师-广东省妇幼保健院.png | 69432 | 231×280 | `5d57c4d543bf600148f046e7aba5541562f903cd97f56014899cf32fea8f95bb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8d58f405-c427-46e3-9d8b-dde43d80d2e8-280.jpg |
| 黄千峰 | 体检科 | 主治医师 | 黄千峰-体检科-主治医师-广东省妇幼保健院.jpg | 7414 | 185×280 | `4417647a8c0bba097fadd5f7518a96465cf0330c51c93b2b338d7f4d673c9b38` | https://wx.e3861.com/sfyAdmin/Images/Doctor/927589cc-17bf-498d-ba50-13b46b84d3ab-280.jpg |
| 刘秋慧 | 眼科 | 主治医师 | 刘秋慧-眼科-主治医师-广东省妇幼保健院.png | 76450 | 188×280 | `bbad6018af5c3c553a1009676823bef54df9cc3d015b6b73c1bc9e0b3e965eb7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/885c5fb6-f5ef-4dad-ab0a-531b8c8df1cb-280.png |
| 曾鑫瑶 | 儿科 | 医师 | 曾鑫瑶-儿科-医师-广东省妇幼保健院.png | 85722 | 202×280 | `14f5df077b42e5dd997e2cedef7ef1348bf242d3b0dff55d6987db6ad73714df` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0d0d712a-f29b-4ea3-80c0-de3bfebeb567-280.png |
| 谭妙华 | 产科 | 医师 | 谭妙华-产科-医师-广东省妇幼保健院.jpg | 5454 | 158×280 | `5fffdda7c69e3a5a9ce8bc99a89b76b18a4f4c5b0c39c02c974d741d49fa7e86` | https://wx.e3861.com/sfyAdmin/Images/Doctor/14a95e5f-8dfb-4325-a743-1fa57ccf2873-280.jpg |
| 刘小珊 | 儿科 | 医师 | 刘小珊-儿科-医师-广东省妇幼保健院.png | 86242 | 190×280 | `f451818e433653ac0cf0890b5e44004ec30a4a1a3b2b52ea182e72262908d185` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c241b259-d3c3-4268-a364-109f5b2c10b5-280.png |
| 刘鑫鹏 | 新生儿科 | 医师 | 刘鑫鹏-新生儿科-医师-广东省妇幼保健院.png | 77066 | 201×280 | `732a4f35d198b2071f6d1872158f63ac2b61f2cff30005ce690525c9ea5323a2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4eda2de9-b392-471a-9d7d-77b545feee4c-280.png |
| 李子珊 | 体检科 | 主治医师 | 李子珊-体检科-主治医师-广东省妇幼保健院.png | 64822 | 179×280 | `d845b933ee516656801cfe3019c31ab7dd58cb1fa55e7a214c03745bd04325c7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/48b57634-3607-4cb8-9c94-ec95d58eb66b-280.png |
| 刘倩 | 产前诊断 | 主任医师 | 刘倩-产前诊断-主任医师-广东省妇幼保健院.png | 49301 | 187×280 | `94613ec1670da1cc106ed57e6b64d2e9bd7373cc1df72317402e47f267bb98c9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3488fa0c-5d72-430d-af43-1940eed7434c-280.png |
| 路攀 | 普通儿科 | 主治医师 | 路攀-普通儿科-主治医师-广东省妇幼保健院.jpg | 5341 | 192×280 | `c9e1aa46a7c014c8c6588a8967b4e6086f4bac51620639d48a0713b0f743df1c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0f787f5f-2ff4-4987-8cbb-3154bd529121-280.jpg |
| 邓诗婷 | 产科 | 医师 | 邓诗婷-产科-医师-广东省妇幼保健院.jpg | 7129 | 210×280 | `e78a4396a5c33a5e79205a569780fd26fc75be821977726880d2791131a01b13` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3e27fc65-970f-45fe-b84e-f6ed8965f08e-280.jpg |
| 潘婉婷 | 普通儿科 | 主治医师 | 潘婉婷-普通儿科-主治医师-广东省妇幼保健院.jpg | 6918 | 188×280 | `ff2d6c9648d88a469b9ef3afad01eb3ea64d3dd80b57180310b93cf5169a92ed` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8cbbc088-1d4f-4a1c-8773-16d97942f799-280.jpg |
| 刘敏琴 | 产科 | 医师 | 刘敏琴-产科-医师-广东省妇幼保健院.jpg | 6037 | 158×280 | `be5b9b345489acc1c09b27986af66a83f12ada009b0d582044df3643a27c782c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8c12bcf7-1b77-4578-84be-541dca7ca188-280.jpg |
| 沈海广 | 儿科呼吸 | 主任医师 | 沈海广-儿科呼吸-主任医师-广东省妇幼保健院.png | 146833 | 296×280 | `fc7250ca78e6d9a98978dc9e09ab1447aa3caff1509497d18ffdf1720c003d74` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bab24ddf-adab-462b-b09b-092e6d55390f-280.png |
| 刘柯君 | 产科 | 医师 | 刘柯君-产科-医师-广东省妇幼保健院.png | 81984 | 187×280 | `922c7cbbaf6d6775c883031f7fd03a803f6136c1a1fcb3b8d3b813e377cd730f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/357dafb0-8e68-4657-9b6c-c5394b291d76-280.png |
| 吕颖 | 中西医结合儿科 | 医师 | 吕颖-中西医结合儿科-医师-广东省妇幼保健院.jpg | 5621 | 200×280 | `564ba1a4ffa659db40c7db803e982182e02602f65655c9cfb43278281d8bc7c3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9abe1a8a-44cf-44fc-beac-de3ac12e216a-280.jpg |
| 高文龙 | 耳鼻咽喉头颈外科 | 医师 | 高文龙-耳鼻咽喉头颈外科-医师-广东省妇幼保健院.png | 101325 | 204×280 | `d97bd632cf532429a97824e917d0c6da1c8ba1c7f32ca1d090a0ea3d2c66076b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0e2381c3-739a-44ea-9fc9-7aae60df7f72-280.png |
| 潘明沃 | 中医科 | 主任中医师 | 潘明沃-中医科-主任中医师-广东省妇幼保健院.jpg | 11733 | 250×280 | `4ba0a60109fdb34e37f357d34d64be316e18c561ef65ed976f289a2c6a3ffc4e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0bbd7adf-b3eb-41a4-a941-f02ceb0b6e76-280.jpg |
| 陈洽鑫 | 耳鼻咽喉头颈外科 | 主任医师 | 陈洽鑫-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.png | 113285 | 219×280 | `7e96fbe5852b68d36ff49eefb4d4ffa09749d3e32afba02e61f40621923a58f4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2cc8f0da-b0b7-4b4e-b343-eb6a4a0085a3-280.png |
| 刘翠 | 儿童保健科 | 主治医师 | 刘翠-儿童保健科-主治医师-广东省妇幼保健院.jpg | 10188 | 280×280 | `b65b81bca68f06446f834b57123760102f41af60ea11db904300e0c271ff030b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ab65a414-a757-46c2-aa14-4cfd788823cc-280.jpg |
| 阮建兴 | 生殖健康与不孕症科 | 主治医师 | 阮建兴-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 7446 | 199×280 | `2c66726d2c6d79fe9fbcf2e1c17f9f2a236e7a6093606182f3c64003c7dc0ccf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b5b81258-29f2-4581-93ac-3dd2ec44758b-280.JPG |
| 刘运可 | 普通儿科 | 主治医师 | 刘运可-普通儿科-主治医师-广东省妇幼保健院.png | 107277 | 210×280 | `0e0b7e00c2e1020771a8f20c402655d1e2576669b7f6be9102a4e47dc1be4c5a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/07e7221c-977a-4495-adc9-226df28d479f-280.png |
| 陈文芬 | 妇科 | 主任医师 | 陈文芬-妇科-主任医师-广东省妇幼保健院.jpg | 9265 | 205×280 | `ce08b7f629d7d99432a45cf6bc47d572c32b688ae1808f5ad32032a35a4c3467` | https://wx.e3861.com/sfyAdmin/Images/Doctor/25fdfe73-ee01-4397-a59b-ba71eae3702b-280.jpg |
| 龚照 | 生殖健康与不孕症科 | 主治医师 | 龚照-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 8752 | 199×280 | `8d48b5611dba363f39f3599f9913ab6d9840a8388e45ae02d76486fadf658b03` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d614af3c-2072-4170-8ad2-8f62f3698442-280.JPG |
| 林秀 | 医疗美容科 | 主治医师 | 林秀-医疗美容科-主治医师-广东省妇幼保健院.jpg | 5590 | 187×280 | `1c4cabc02753f167bdf504f3f40bad20b9f0dbc1c3ff36f2b189e44cf6849792` | https://wx.e3861.com/sfyAdmin/Images/Doctor/64abbcb6-4a57-42dc-8ff3-aaff6ee380a6-280.jpg |
| 陈凤媚 | 中医科 | 主任中医师 | 陈凤媚-中医科-主任中医师-广东省妇幼保健院.png | 82927 | 205×280 | `d9a745035de2d9f2dcf68d384d9b8b498bf32e967e1b574657918b2c938920f5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1d81e6e0-56ec-4693-aa26-500baa678d64-280.png |
| 高彩凤 | 眼科 | 主治医师 | 高彩凤-眼科-主治医师-广东省妇幼保健院.png | 58124 | 187×280 | `cf912131005df7e9827d954530be443ff6d154a6f348cf6c66f24def3c458cf8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f4d4266e-c8ab-41e3-afba-6ebfe45462cc-280.png |
| 罗卓迪 | 皮肤性病科 | 主治医师 | 罗卓迪-皮肤性病科-主治医师-广东省妇幼保健院.png | 79646 | 210×280 | `e96d19656ad8cc0cf86235aacebaabcc409d1fb2bdaf891c421c03d61131c619` | https://wx.e3861.com/sfyAdmin/Images/Doctor/cffa60d8-9f8c-4a22-bf19-dc2302b8458a-280.png |
| 车頔 | 儿童保健科 | 主任医师 | 车頔-儿童保健科-主任医师-广东省妇幼保健院.png | 64766 | 183×280 | `707e6d16b3ee96823956e25c91cca7cf445bc3f0dea5a7f3db488d190eb68b64` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a0fa3bfc-68cf-42ff-83d4-4a236079401c-280.jpg |
| 黄亚萍 | 耳鼻咽喉头颈外科 | 主治医师 | 黄亚萍-耳鼻咽喉头颈外科-主治医师-广东省妇幼保健院.jpg | 9471 | 207×280 | `66feff695d73fed2049af7c957cb704318ffa3cc7e3a93f19a2b760bd2e44ca5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0c79b36d-0e51-4e88-a76d-f2f6c7edc505-280.jpg |
| 李帅杰 | 乳腺科 | 主治医师 | 李帅杰-乳腺科-主治医师-广东省妇幼保健院.jpg | 5611 | 187×280 | `8c7e8eca2791a1c61fde3ce9a19f61a078bbee681d2d780ed45f19251dbcc064` | https://wx.e3861.com/sfyAdmin/Images/Doctor/40dc5910-82fc-4d52-8ba5-881f6ce881bc-280.jpg |
| 刘嘉芬 | 中医科 | 主任中医师 | 刘嘉芬-中医科-主任中医师-广东省妇幼保健院.jpg | 9293 | 228×280 | `bcf17bd0d68f375ba39fd0dcfb2bf81ccc3f27c2e9d1323359b50d5f67001c80` | https://wx.e3861.com/sfyAdmin/Images/Doctor/efca319c-8a23-44fb-ba01-16a8797fbffc-280.jpg |
| 向义 | 小儿外科 | 主任医师 | 向义-小儿外科-主任医师-广东省妇幼保健院.jpg | 7977 | 240×280 | `35514713ca347bf5b2e1448b6cb8226d58b97befab2428802c5cd7bd4aef4e87` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b4a8b024-3f30-4333-ac3a-b4c71b6ee4ed-280.jpg |
| 洪淑贞 | 产科 | 主任医师 | 洪淑贞-产科-主任医师-广东省妇幼保健院.jpg | 6411 | 187×280 | `bc515d748eb296b6dbd16b4ad5da41a2a1e6b9d9ff7ae3afc7e436704dc9a809` | https://wx.e3861.com/sfyAdmin/Images/Doctor/51e03bbf-ddfc-4480-a5d1-e1b94374e1bf-280.jpg |
| 曾可 | 儿童内分泌遗传代谢 | 主任医师 | 曾可-儿童内分泌遗传代谢-主任医师-广东省妇幼保健院.jpg | 7977 | 194×280 | `b91651a7be82dc9a45969dc065decb6b6dc1ce654e0d4dc0fc7dc7588d80802c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c71e829a-d616-476f-91cb-6d917acdc63d-280.jpg |
| 方利元 | 产前诊断 | 主治医师 | 方利元-产前诊断-主治医师-广东省妇幼保健院.jpg | 5431 | 187×280 | `011f22492cabbdef19ad664849f1b6e914e7838122feaf02ac996c24dc110bec` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a8144746-3249-49d0-a449-60644a999ad8-280.jpg |
| 李晓楠 | 妇科 | 主治医师 | 李晓楠-妇科-主治医师-广东省妇幼保健院.jpg | 8034 | 196×280 | `2bc420cb54564b1e829b5948e4cb484066b6849089e11892036face1e8a40658` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3eb85ce1-2c96-456f-9947-a0c372944c07-280.jpg |
| 林惠芳 | 儿童保健科 | 主治医师 | 林惠芳-儿童保健科-主治医师-广东省妇幼保健院.png | 81177 | 280×280 | `27a557a5ec9433c60968c880510c7f715c0cd6218453e4fd3760c8c21f881366` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a4187d3b-39b4-444b-ab94-7ddd9b228fbc-280.jpg |
| 苏贝贝 | 儿童内分泌遗传代谢 | 医师 | 苏贝贝-儿童内分泌遗传代谢-医师-广东省妇幼保健院.png | 74849 | 175×280 | `6db922f92024178d36a26d11dd9d5328e63b1a276d0365811a71f66c9ebd03b8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9a00361a-338a-4bd1-91b1-b8b0558eb78b-280.png |
| 方琴 | 麻醉科 | 主任医师 | 方琴-麻醉科-主任医师-广东省妇幼保健院.png | 54599 | 187×280 | `921e0ce42cd3463d12b16daf40fad43ba25fa565ef09f6ae169e1aa31e8d6440` | https://wx.e3861.com/sfyAdmin/Images/Doctor/55e6fbce-f9db-4ed2-939a-e8458ee42167-280.png |
| 李莉 | 生殖健康与不孕症科 | 主治医师 | 李莉-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 8953 | 199×280 | `99122785e87320f96f0903eea4318142dd45f692eea25c437b938d161e9b882a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ef0ea260-dfc2-402e-a1ac-b7e3e375da51-280.JPG |
| 李文成 | 小儿肾内科 | 主任医师 | 李文成-小儿肾内科-主任医师-广东省妇幼保健院.png | 70459 | 183×280 | `5d00c40c462e63d2063ea788672812521d15a549ce9a27a64c28dc1676d54179` | https://wx.e3861.com/sfyAdmin/Images/Doctor/819b94d4-beee-4b44-9148-0aa121bd8b7c-280.png |
| 邓超群 | 耳鼻咽喉头颈外科 | 主治医师 | 邓超群-耳鼻咽喉头颈外科-主治医师-广东省妇幼保健院.png | 111751 | 204×280 | `be98dd227a1b226c90f547a527a96f60933e1b3eeb4362a122a681e6f4448927` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4ba1af3b-d56b-4fc6-996f-8a92051217e9-280.jpg |
| 杨浩鸣 | 新生儿科 | 主治医师 | 杨浩鸣-新生儿科-主治医师-广东省妇幼保健院.jpg | 7799 | 210×280 | `a26b7cfc361821f6edbde5ad4761e957560cea6bd3ae66fffac1838f0ca59853` | https://wx.e3861.com/sfyAdmin/Images/Doctor/64bbd970-c9de-4bd8-a321-cd89601976d2-280.jpeg |
| 苏丹晨 | 未标注 | 主任医师 | 苏丹晨-未标注-主任医师-广东省妇幼保健院.png | 69971 | 187×280 | `ee43c9b6f3602bf8a1eb4ff7e5218d86e0ccb7206d4778372cee2c10927a67a7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9f123ca8-ebcb-416a-8f41-d41e67005415-280.png |
| 韩争争 | 小儿血液病 | 主治医师 | 韩争争-小儿血液病-主治医师-广东省妇幼保健院.jpg | 6900 | 241×280 | `d2ac5947143d51e6dc7339ec18869e0d146c64541823cb16d4d4710bc1274450` | https://wx.e3861.com/sfyAdmin/Images/Doctor/31ce5c67-23dd-47d3-95ae-40661cf25205-280.jpg |
| 谭琪琪 | 普通儿科 | 主治医师 | 谭琪琪-普通儿科-主治医师-广东省妇幼保健院.jpg | 6526 | 209×280 | `d0a57f5cdd1d282b900dc04a4d603ae7d810d325721b5fedb30a7f098b7d88df` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0e3b3e5d-7a7e-4ed1-9960-ef0e8894b781-280.jpg |
| 陈晓伟 | 儿科 | 医师 | 陈晓伟-儿科-医师-广东省妇幼保健院.jpg | 5893 | 158×280 | `f8038e7f5407979b3612bd1c28e9119a08438388380d5fe5da2337998f3e36ba` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4b947cb7-19c6-44f7-9b9d-60c6f6df655f-280.jpg |
| 何景优 | 麻醉科 | 主治医师 | 何景优-麻醉科-主治医师-广东省妇幼保健院.png | 51834 | 187×280 | `48719176aaa23ae430d4749825a3971458e5e3ef9529f8b132426aa44bda4156` | https://wx.e3861.com/sfyAdmin/Images/Doctor/233134b7-2057-42c6-a0e3-6350e81ebd47-280.png |
| 张丽 | 产科 | 主任医师 | 张丽-产科-主任医师-广东省妇幼保健院.png | 109365 | 199×280 | `4e3e1812284690e4829b16efabb5545dc4a42933e099f8e253e0f71236bbc8cc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f93a1565-0eb0-420a-9ce8-93b532233a2b-280.png |
| 易菁 | 产科 | 主任医师 | 易菁-产科-主任医师-广东省妇幼保健院.png | 80295 | 237×280 | `20ad8b0ec08740696d1fcb968f184d767662fc51ab450bd3d35eb84463976764` | https://wx.e3861.com/sfyAdmin/Images/Doctor/96938d20-4bf9-4d05-9581-0adc714f9b0e-280.png |
| 莫力 | 麻醉科 | 主任医师 | 莫力-麻醉科-主任医师-广东省妇幼保健院.png | 62637 | 187×280 | `a73a0645f393a60bbd98552906d4ecd5341af64aab4fe347320f0e21b8e5d436` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c124fdbc-f10e-4d48-9e30-37a691a3bd79-280.png |
| 周睿琼 | 生殖健康与不孕症科 | 主治医师 | 周睿琼-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 8011 | 199×280 | `ccd86709dae55b1241ad36fe96a93ef73f6d9f5e21be4e05be79066b393a5193` | https://wx.e3861.com/sfyAdmin/Images/Doctor/88d721f4-94f7-47fa-a96e-c08d2ecaf4f5-280.JPG |
| 黄倩文 | 生殖健康与不孕症科 | 主任医师 | 黄倩文-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 6952 | 199×280 | `753475f8f03a605ec478c5035577e5df12c7b4a2446ef3831dede9ab374d22f7` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5673a7ef-5a0d-48c3-9eac-2e39b5781e01-280.JPG |
| 卢桂贤 | 体检科 | 主治医师 | 卢桂贤-体检科-主治医师-广东省妇幼保健院.png | 69966 | 184×280 | `0fa166ea358209e9ba6e57323f8e81fc7f8df88d965e9056ba6be8b61f7ddf36` | https://wx.e3861.com/sfyAdmin/Images/Doctor/520ce2d5-3e79-4d80-acc1-227fb5259c24-280.png |
| 周平 | 产科 | 主任医师 | 周平-产科-主任医师-广东省妇幼保健院.jpg | 6061 | 187×280 | `f1035d6b03f91218e2ba010b7e34e897c18c296c4508b8ac2b85e2c54294b7ad` | https://wx.e3861.com/sfyAdmin/Images/Doctor/df90999f-dc60-4dd7-905f-cef697d59ff6-280.jpg |
| 唐玲 | 普通儿科 | 主治医师 | 唐玲-普通儿科-主治医师-广东省妇幼保健院.png | 73257 | 190×280 | `60e0bad4ea82c9ef2e40e73d7b0f362308fae03fbb0dd9da7d89c89a9db38bc1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0b5a3bbb-326c-4799-aba5-d01993012318-280.png |
| 赵聪伶 | 未标注 | 主任医师 | 赵聪伶-未标注-主任医师-广东省妇幼保健院.png | 84697 | 210×280 | `fd12006bd05c21b8ee7f9cade76bff316dea6032faf6d4c53d7bf0b2f28a0787` | https://wx.e3861.com/sfyAdmin/Images/Doctor/949e50bd-72c8-45be-89de-86f7bfffeab3-280.png |
| 李丽贤 | 普通儿科 | 主治医师 | 李丽贤-普通儿科-主治医师-广东省妇幼保健院.jpg | 8673 | 218×280 | `13d739f8a859eae095525456550cd90fd4a73cae5eea7279b3ae87df59acf959` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0d5b49d0-aa51-4224-90c0-f27e785c741c-280.jpg |
| 石婧 | 皮肤性病科 | 主任医师 | 石婧-皮肤性病科-主任医师-广东省妇幼保健院.png | 85623 | 253×280 | `06a34898cee49c0e6d7c0891a82e5b49af8c9dff300e1c5dd53f38f4a0bedcbe` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0ba05f3e-5cc7-4208-adec-491d81227252-280.png |
| 张洋洋 | 乳腺科 | 主治医师 | 张洋洋-乳腺科-主治医师-广东省妇幼保健院.jpg | 6659 | 200×280 | `6caff8f01b70389e299b5491a6a98d4de6238f5b2214cc09b684c0eb54f0ac75` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3f61b022-5511-46a3-be0c-38bcce231fa8-280.jpg |
| 付亚林 | 儿科呼吸 | 主任医师 | 付亚林-儿科呼吸-主任医师-广东省妇幼保健院.png | 100286 | 211×280 | `b687b47fca9bf473591fc0b768a4e0347d5722e69d35fbcb2401fbea2df63768` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9dbc6bd6-3143-429a-9b2a-be4dea622d5a-280.png |
| 王林淦 | 普通儿科 | 主治医师 | 王林淦-普通儿科-主治医师-广东省妇幼保健院.png | 74729 | 206×280 | `f65ef078edd5a2ff1ed36d4a161baaa58b2d897978887c9f9dc503e32f48254d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1cf9e06a-5c71-423f-af16-49c1e1fa0cce-280.png |
| 聂碧林 | 麻醉科 | 主治医师 | 聂碧林-麻醉科-主治医师-广东省妇幼保健院.png | 48921 | 187×280 | `f40bc13bcc2a29790987c19f86d10b0288bd312d6500964535cd753e05d1580a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/742f35e6-0a2e-4531-b473-c29b12c0befa-280.png |
| 孙铭佩 | 麻醉科 | 主治医师 | 孙铭佩-麻醉科-主治医师-广东省妇幼保健院.png | 74429 | 187×280 | `e785fa8c9a95c96fba3fb642954164a66d5694d8ff08ca978436a2a99747cd23` | https://wx.e3861.com/sfyAdmin/Images/Doctor/30373755-88d9-4668-b785-ccd5f3ce993a-280.png |
| 王媛媛 | 生殖健康与不孕症科 | 主治医师 | 王媛媛-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 7074 | 199×280 | `3a0f596b331cdc871ed0556284e553fea3b0832964ab1f376d113e963947d516` | https://wx.e3861.com/sfyAdmin/Images/Doctor/400f165c-5855-4334-b615-fb4fee6d5906-280.JPG |
| 余楚岚 | 康复医学科 | 主治医师 | 余楚岚-康复医学科-主治医师-广东省妇幼保健院.png | 72090 | 206×280 | `e3e2ba02d3b4b6a1272ac3e31884b9a0774599970be84e718c9a918ffbf737d5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c569ded6-c745-4b87-afae-667772279e98-280.png |
| 王昀 | 麻醉科 | 主任医师 | 王昀-麻醉科-主任医师-广东省妇幼保健院.png | 70497 | 187×280 | `6caf0421b01fb82bd9ac2fca09976d26a25c1d18326d5aaaf48a57ab2a250ecf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c48c6f4f-39a6-4fb7-89ec-b8905d1f4f48-280.png |
| 杨小敏 | 麻醉科 | 主治医师 | 杨小敏-麻醉科-主治医师-广东省妇幼保健院.png | 66344 | 187×280 | `35d868213f1eced338351ec1377cfecc122e31f604867c3e4b9a2eda0868a174` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1b9b100e-f101-4ce7-b277-5989f7b79590-280.png |
| 何琼 | 普通儿科 | 医师 | 何琼-普通儿科-医师-广东省妇幼保健院.png | 77703 | 220×280 | `ce3830aa5b4a46e855491195ec98b41b1b502dd78f7d07d9ac99fbbb8c38fc12` | https://wx.e3861.com/sfyAdmin/Images/Doctor/29cecc96-3430-41cb-859a-4f52edbaad05-280.png |
| 郑少章 | 儿科 | 主治医师 | 郑少章-儿科-主治医师-广东省妇幼保健院.png | 68588 | 190×280 | `912d868a4b587f109133994bb60e7cafdb6d0ddf6ae4e1c94623cedfed5b0593` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fbe51868-c615-4434-8515-0492d1f742af-280.png |
| 丁辉阳 | 新生儿外科 | 医师 | 丁辉阳-新生儿外科-医师-广东省妇幼保健院.jpg | 7938 | 198×280 | `40eacb1b96a4ced453ee085e8cad436d63d7d3bba3ed89c3bc64dcc76cba582e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d2182b0e-036d-4ab0-a141-202578f1fdb8-280.jpg |
| 王亚曙 | 儿科呼吸 | 主治医师 | 王亚曙-儿科呼吸-主治医师-广东省妇幼保健院.png | 97736 | 222×280 | `a0366d208ff37ce81ac635d52a05958ae8e3e909e65919ca81ef3f4c8692ad45` | https://wx.e3861.com/sfyAdmin/Images/Doctor/81ea1966-fef3-4b3e-a638-7ba064c95ada-280.png |
| 孙艺娟 | 麻醉科 | 主任医师 | 孙艺娟-麻醉科-主任医师-广东省妇幼保健院.png | 79045 | 187×280 | `0d60929fb2b9af49017545568a0896de2c5c463ba25d692a8bc39f2cc55242c5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5bb5e169-5f92-4f6b-84ad-b113a44cdc9c-280.png |
| 张儒森 | 疼痛科 | 医师 | 张儒森-疼痛科-医师-广东省妇幼保健院.jpg | 7617 | 210×280 | `d24150408d0e61a4723b0cdf22235c7831eb0871026f33ee9267fd03b2d47391` | https://wx.e3861.com/sfyAdmin/Images/Doctor/def89e29-1516-42a3-9559-bd75c3aaed61-280.jpeg |
| 黄彩霞 | 麻醉科 | 主任医师 | 黄彩霞-麻醉科-主任医师-广东省妇幼保健院.png | 63539 | 187×280 | `c48097aaab98a88fb527598bd28c37676fabb75f9b6c115a13a7f12dc191bad3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0e614708-35e9-4abe-b274-28f8351da90f-280.png |
| 潘汝涛 | 小儿骨科 | 主治医师 | 潘汝涛-小儿骨科-主治医师-广东省妇幼保健院.png | 81734 | 199×280 | `e386f490dee1f7b839b8a68e9b6510fb869e725d95ece9ab2178f4e753212290` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e2d59c31-1c4b-46cd-9c02-aeb0c63aa354-280.png |
| 周易 | 体检科 | 主治医师 | 周易-体检科-主治医师-广东省妇幼保健院.jpg | 7907 | 251×280 | `c24f57bcd279ca6ad520404f4abdc77bf21b2015ba818a32704bc27740e393f2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/edc56170-d556-4b6e-893b-aa5255c32788-280.jpg |
| 朱海鹏 | 小儿骨科 | 主治医师 | 朱海鹏-小儿骨科-主治医师-广东省妇幼保健院.jpg | 7802 | 205×280 | `f38cd20fcf432333a3ce2b02006b525ba175ed57279de8c0f44e90bada32baca` | https://wx.e3861.com/sfyAdmin/Images/Doctor/714f1abc-384c-443c-918c-4544661620c5-280.jpg |
| 何裕 | 妇科 | 主治医师 | 何裕-妇科-主治医师-广东省妇幼保健院.jpg | 9341 | 280×280 | `6cd2bd3316959814cd9f46fab81f4d233c9ecd7f15c8402eab35c6629b6d10d6` | https://wx.e3861.com/sfyAdmin/Images/Doctor/591e0217-b05f-4ab8-bf95-5b99d6ac432c-280.jpg |
| 卢颖 | 妇科 | 主任医师 | 卢颖-妇科-主任医师-广东省妇幼保健院.jpg | 6994 | 186×280 | `b8d5a90621318ef3bb836133a8665e1cecea1fc436e7ce6bc633907487565587` | https://wx.e3861.com/sfyAdmin/Images/Doctor/51446548-1160-4b3f-b201-a0cd44662ad8-280.jpg |
| 郑涵 | 普通儿科 | 主治医师 | 郑涵-普通儿科-主治医师-广东省妇幼保健院.jpg | 9100 | 200×280 | `19da634dd91b7d65d7894c33637fab274542152fe6e11d17c150e4e2905fe814` | https://wx.e3861.com/sfyAdmin/Images/Doctor/572c0c9f-3b33-4ff3-939a-13ba9e7449cd-280.jpg |
| 李碧云 | 普通儿科 | 主治医师 | 李碧云-普通儿科-主治医师-广东省妇幼保健院.png | 112938 | 228×280 | `10caa38fde2d943b51d565bb12ca9f4c11357ad3414d2b9259edf9a4b360d822` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6581974f-a34c-456e-b6c9-baa1b7e9de1e-280.png |
| 贺牡丹 | 麻醉科 | 主任医师 | 贺牡丹-麻醉科-主任医师-广东省妇幼保健院.png | 51806 | 187×280 | `1701f6beb14edc5d2c8af0c61b81204b3454f407e9186663d6417c904a3a7674` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9626fc87-829b-4f7d-a67f-101f48b658c9-280.png |
| 杨亮 | 麻醉科 | 主治医师 | 杨亮-麻醉科-主治医师-广东省妇幼保健院.png | 70859 | 187×280 | `760df987525a1de15ecca675315a8531c2c4641a7c4677d91033f9100fdb68a9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c36b387a-6151-45ca-9e99-9e4f04573090-280.png |
| 黄微 | 麻醉科 | 主治医师 | 黄微-麻醉科-主治医师-广东省妇幼保健院.png | 58471 | 187×280 | `ef32c7de3629cd600addf64bebe88fd93774a33d3cdf4e89aff6fd13fb48b6d4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0fff6dc0-cb3e-475a-ac55-b997fa92aa81-280.png |
| 乐珍 | 妇科 | 主治医师 | 乐珍-妇科-主治医师-广东省妇幼保健院.jpg | 8010 | 187×280 | `bc6378cc3e0495979317bf028b82dbb105cadbdc5650e2611f798e6d17e6755b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3ea3b405-e486-41ce-a388-26ed99bac625-280.jpg |
| 欧燕兰 | 妇女保健科 | 主任医师 | 欧燕兰-妇女保健科-主任医师-广东省妇幼保健院.png | 83287 | 195×280 | `ddfd88a1674017880017a5412e01cfac79cc27e5638ad521e5911285009a4be2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e67afe9b-e430-4dcf-aac9-5ade9721afb9-280.png |
| 李素丽 | 普通儿科 | 主治医师 | 李素丽-普通儿科-主治医师-广东省妇幼保健院.png | 73625 | 249×280 | `f058cd55f8ddb9a116e52cf618f2621b8a25516cf00cbb87fc846bff9aae3815` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e5c8bbf5-f46f-4865-90fa-55d18c2da8aa-280.png |
| 邓贵华 | 妇女保健科 | 主任药师 | 邓贵华-妇女保健科-主任药师-广东省妇幼保健院.png | 92244 | 232×280 | `0135954a7e399af22598f2e4e252334f72821e1e77f8724a6efa72f6bd0861b1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/412591f9-84be-4c1c-95ef-8a85db44951e-280.png |
| 王海彦 | 麻醉科 | 主治医师 | 王海彦-麻醉科-主治医师-广东省妇幼保健院.png | 70031 | 187×280 | `227f978cc695f3e42a62e4d0c8ca7405c6ce664cea8c0cc54163eb301d123f79` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1b263b6b-ef77-4ee7-ad30-8a4976983447-280.png |
| 刘慧 | 心脏中心 | 主治医师 | 刘慧-心脏中心-主治医师-广东省妇幼保健院.jpg | 6853 | 210×280 | `0f1758058f9d0d648741a506617b28bd6775299dc7787854e3eadf120a237c67` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e166d049-550f-4d37-84d2-e2ed874a5a8e-280.jpg |
| 田碧霞 | 普通儿科 | 医师 | 田碧霞-普通儿科-医师-广东省妇幼保健院.jpg | 6785 | 282×280 | `45d0fb0e9823f7d2b30a4293ee8e53e1ea6d268c81870d10d95904c8df2f73d2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/66871e94-9918-43ff-9763-7f0f559fe437-280.jpg |
| 钟燕芳 | 产前诊断 | 主任医师 | 钟燕芳-产前诊断-主任医师-广东省妇幼保健院.png | 61687 | 187×280 | `8f60055f15010242fdb89e4a026a90836575052b9397f938ce752b1e1ca61f9a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/500f0434-4b73-4886-85cf-a47f5401648d-280.jpg |
| 贺丽荣 | 产科 | 主任医师 | 贺丽荣-产科-主任医师-广东省妇幼保健院.png | 90946 | 198×280 | `8457e3a7a058a3b1468630e72b386cd6e59013047d0416724c8ceb02141614e4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a605838f-14c3-4d1c-8fb5-5a31b8b38690-280.png |
| 徐丽清 | 生殖健康与不孕症科 | 主任医师 | 徐丽清-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 7578 | 199×280 | `e306225a7f0186e964f915185859d6a8fb93f066c1835be747d06a03b7806678` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ac605ac8-7c0e-444c-a800-af9dff74737d-280.JPG |
| 涂莹 | 儿科 | 主治医师 | 涂莹-儿科-主治医师-广东省妇幼保健院.jpg | 6072 | 187×280 | `e2aaf22f4992ff7e4adb0f8c20c6aba22bfc0df166652ca3a9eda4bc9a65c1a3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/76e13252-d773-40e8-97ed-67ed6c982318-280.jpeg |
| 吕金芳 | 中医科 | 主治医师 | 吕金芳-中医科-主治医师-广东省妇幼保健院.png | 72456 | 184×280 | `efdc323fee24a667183ceaccdc85d77b1c444c45a82173839452428f8354f857` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9cc5a3fe-a9cd-4dc7-a5db-a0fb5f453634-280.png |
| 伍苑宾 | 普通儿科 | 主治医师 | 伍苑宾-普通儿科-主治医师-广东省妇幼保健院.jpg | 6238 | 187×280 | `02970b1d99b80cf3f27dabe7d1f97a3516bc2f8569b05bec78a8bc4efdb10053` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fbaac087-66ae-461f-b8ad-3a7bd9e0ce93-280.jpg |
| 郭勇 | 儿童保健科 | 主任医师 | 郭勇-儿童保健科-主任医师-广东省妇幼保健院.png | 91359 | 200×280 | `af935facbf7756866172d2a5c9308b0c8c696c761ab62c9bfdc1ae38ef9c7ccb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5bdfa451-1d6e-4a77-8f85-88d426602d8b-280.png |
| 赵秋仪 | 妇科 | 医师 | 赵秋仪-妇科-医师-广东省妇幼保健院.jpg | 6466 | 199×280 | `2a4d8d874c03c21e4a00f766319889f71694535165c47146c4ad30b6123c0850` | https://wx.e3861.com/sfyAdmin/Images/Doctor/757ab77a-0784-4a1f-bd0a-774e7af8dd5b-280.jpeg |
| 段红丽 | 产科 | 主任医师 | 段红丽-产科-主任医师-广东省妇幼保健院.png | 99375 | 203×280 | `0c4c488a64fd83552b2927214adb9e05ec27639ae4ed855eba7ba8cdfd2fdb61` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0de4a9ed-2677-4d5a-8a0f-5575c2f5baff-280.png |
| 金文艳 | 妇科 | 主任医师 | 金文艳-妇科-主任医师-广东省妇幼保健院.png | 83061 | 197×280 | `36314079d76cf6854de1e0c951908dd02d1b54d0842ef44db6afe0bb2d32e637` | https://wx.e3861.com/sfyAdmin/Images/Doctor/57b76356-5f10-44e1-9feb-71ada2ed6aca-280.png |
| 叶燕彬 | 儿童保健科 | 主治医师 | 叶燕彬-儿童保健科-主治医师-广东省妇幼保健院.png | 78691 | 199×280 | `be87c99b14b73834360e80718fab11467c0718dd66e520891c1b74b333a56b5b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1c09ccf7-d4db-4625-bdfe-e0928371e68d-280.jpg |
| 王柱 | 新生儿科 | 主任医师 | 王柱-新生儿科-主任医师-广东省妇幼保健院.jpg | 6374 | 190×280 | `73d20d6239b76a8df6f01bbbf415a7bae3adc3566cb0b65f723583e79727a11e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9b07eb74-1631-4dbf-9a21-1045ed508263-280.jpg |
| 陈雅颂 | 产科 | 主任医师 | 陈雅颂-产科-主任医师-广东省妇幼保健院.jpg | 6838 | 199×280 | `7a0199adfd7504fca55e6abce601fddcfdd5da4ba7af1d712067f0c60b3b787c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/be7099f0-48eb-42c2-819b-f3a45fc10602-280.jpg |
| 蒋东丽 | 中医科 | 医师 | 蒋东丽-中医科-医师-广东省妇幼保健院.jpg | 7099 | 187×280 | `c8e46adc90b441b872b18aba9f6b0c76eaebf20296dfe362d03c11d2588f859f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8178243d-dc8b-4bdf-8aed-3a6f7dd66f6c-280.jpg |
| 赵慧 | 儿科呼吸 | 主任医师 | 赵慧-儿科呼吸-主任医师-广东省妇幼保健院.png | 102244 | 240×280 | `d4ca42bf7eb2f6ff9fdf6d0669be2998ba9f9991c93cfff56a10f09b23f8a846` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b874c0b9-02e0-4a68-97ba-6c936ebfa00c-280.png |
| 梁德懿 | 儿童保健科 | 主治医师 | 梁德懿-儿童保健科-主治医师-广东省妇幼保健院.png | 99589 | 210×280 | `9ad4d129c16dc1a12fa317c55e27d39eb280454380f4360afb2e3c75471d3144` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2c8a7792-22e0-48c2-8eb8-626c1c4dae1c-280.jpg |
| 叶媛 | 医疗美容科 | 主任医师 | 叶媛-医疗美容科-主任医师-广东省妇幼保健院.png | 101138 | 211×280 | `f26ffcd40cf566587197bb779bfb69106d2920acdfec85abfb22be93d2154f41` | https://wx.e3861.com/sfyAdmin/Images/Doctor/84419afc-8c64-4b7e-95ae-9ea147a01771-280.png |
| 费佳裕 | 普通儿科 | 主治医师 | 费佳裕-普通儿科-主治医师-广东省妇幼保健院.png | 96095 | 281×280 | `d5797171cb3885d8b79563fa1f912060015565e871203d62eba6cd12d87616cb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b14a9cfd-6805-4157-8ffe-4e4b5bae7aa5-280.png |
| 任建兵 | 新生儿科 | 主任医师 | 任建兵-新生儿科-主任医师-广东省妇幼保健院.png | 106224 | 255×280 | `6d20188a01a21df4ba37be2b32a92397da7621e5fb9c038ad20f17c5ac5dc78a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/54e6458f-4a20-427f-ac8b-a9b660bb00f2-280.png |
| 戴慧敏 | 中西医结合儿科 | 主治医师 | 戴慧敏-中西医结合儿科-主治医师-广东省妇幼保健院.png | 87280 | 245×280 | `96177af947aa3284a6118062e2052a6f442dc4ade57a131c93002a4107c2c8b3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1a6a2c5f-709d-4a3a-869d-b97e6e2b446b-280.png |
| 邓梦夏 | 耳鼻咽喉头颈外科 | 主治医师 | 邓梦夏-耳鼻咽喉头颈外科-主治医师-广东省妇幼保健院.jpg | 8113 | 200×280 | `32ce374aadc9349f4dbca3219f4843696c1d0e61e05c7bf2e60192795e2e1b73` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ab928d30-ba23-4dfd-bacf-4d744f5621bb-280.jpg |
| 郭梓君 | 儿科呼吸 | 主治医师 | 郭梓君-儿科呼吸-主治医师-广东省妇幼保健院.png | 109462 | 283×280 | `b9c42cc5f7e5c06140dc2737e3b52aa00c0730231458875a239b213970f13682` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6c8c38f4-95d0-4383-97c9-ba0821f619ec-280.png |
| 易艳红 | 生殖健康与不孕症科 | 主任医师 | 易艳红-生殖健康与不孕症科-主任医师-广东省妇幼保健院.jpg | 8267 | 199×280 | `3bf1d8d1e9914ff9e05f227d2d5910a8a53fb8d27056420781b143bc420c7b3c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a69ac647-08af-4d53-a492-b4badc99429f-280.JPG |
| 姚俐 | 生殖健康与不孕症科 | 主任医师 | 姚俐-生殖健康与不孕症科-主任医师-广东省妇幼保健院.png | 100962 | 213×280 | `3f0b2a32ee5e51aa51fa6ecb7162ac1e3d69162c88f6f4a90afcde238f543ce8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fa7048ed-96b5-46cb-a3a2-c12c9386f64c-280.png |
| 徐丽群 | 妇科 | 主治医师 | 徐丽群-妇科-主治医师-广东省妇幼保健院.jpg | 8233 | 192×280 | `f3a1ff30bebf158e3b367bdc3509dd4852b3105478a6a22a1a48c9440a8f3b1c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b461afda-f8bb-44cd-a2f6-bed7619a41ab-280.jpg |
| 张春一 | 新生儿科 | 主任医师 | 张春一-新生儿科-主任医师-广东省妇幼保健院.png | 62769 | 170×280 | `841733749317e437f97b562a9a8a4d276a40a3f4bcdaa91b324d5f1073cc68aa` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d3016dc4-61a2-43e8-bde3-9bf514243f60-280.png |
| 梁树 | 新生儿科 | 主任医师 | 梁树-新生儿科-主任医师-广东省妇幼保健院.png | 77653 | 187×280 | `011b66a629e8fd59d42e48399d487195cfe6f5cf2aedc823f1d46743d25f0fca` | https://wx.e3861.com/sfyAdmin/Images/Doctor/93e18bd8-8e87-4531-816a-933a8a6ac7ee-280.jpg |
| 孙博 | 儿科消化 | 主治医师 | 孙博-儿科消化-主治医师-广东省妇幼保健院.jpg | 6554 | 210×280 | `82f18f167f0fd3c750b92c59e62d9e80ca70c813b85e63e7bb9bfbbf52c688ac` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bb596960-c696-4e07-9f19-1f8f0e9b7690-280.jpeg |
| 吕莉娟 | 产科 | 主任医师 | 吕莉娟-产科-主任医师-广东省妇幼保健院.png | 51503 | 187×280 | `1608b1b8dbf49ea77af00805ba754b8cc443366dc606d45dd649c894688e2902` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5bb13868-4685-43a6-b064-eecc69e1a8b5-280.png |
| 许露 | 新生儿外科 | 主治医师 | 许露-新生儿外科-主治医师-广东省妇幼保健院.png | 72835 | 224×280 | `d9bba60946cc6c653595a15c4a4437b257bcd8d79b17e0d9e9e3eaf256424d3a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e66406da-1a5b-4648-8ec2-04d1fce1d25f-280.png |
| 刘颖兴 | 小儿胸外科 | 主治医师 | 刘颖兴-小儿胸外科-主治医师-广东省妇幼保健院.jpg | 5915 | 189×280 | `613e8deaf2927990361f7b17e2dd9ada95b448e85d386f8169ad528058c327f0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c528cd7b-bf86-4588-8edb-020394e3741c-280.jpg |
| 杨晨露 | 产科 | 主治医师 | 杨晨露-产科-主治医师-广东省妇幼保健院.png | 69713 | 187×280 | `bab72b9c3718d6885aa130ad9c5af499e7d2b7ecb933a8760d828aeeea9ecec3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/deea1ae2-2602-4368-b88b-708cfb798778-280.png |
| 张倩玉 | 生殖健康与不孕症科 | 主治医师 | 张倩玉-生殖健康与不孕症科-主治医师-广东省妇幼保健院.png | 68199 | 185×280 | `e60c6ec5a94618c6d915ca1e1eec4d7c152b7b4a95fa68269fc5fa9784895100` | https://wx.e3861.com/sfyAdmin/Images/Doctor/70faf05a-48c6-4201-b08b-3c35d4a8e6c1-280.png |
| 刘婷艳 | 妇科 | 主任医师 | 刘婷艳-妇科-主任医师-广东省妇幼保健院.jpg | 7529 | 192×280 | `840a0d7db43d869aeb3fcbe61c1537a356db36271fffbc87e415ea50d5af948e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/012118a2-221f-4508-abe8-dbbf548c2e19-280.jpg |
| 余莉 | 儿童保健科 | 主任医师 | 余莉-儿童保健科-主任医师-广东省妇幼保健院.png | 94500 | 223×280 | `e321e43a1ee185f526cfb97e379e86a6634a9fff16f7ccc4525247915f84b6c4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7dd45cda-6fbb-47cb-8063-b07647d3902a-280.png |
| 邓钰红 | 儿童保健科 | 主治医师 | 邓钰红-儿童保健科-主治医师-广东省妇幼保健院.jpg | 8423 | 210×280 | `c89d3cd3f4ad356eb63df2f10eef6561edf45c4febf2e71fe4b22fb954095039` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1494c7a2-f2d9-485c-ba04-996c5005d085-280.jpg |
| 张晓明 | 眼科 | 主治医师 | 张晓明-眼科-主治医师-广东省妇幼保健院.png | 71937 | 203×280 | `f1e0c5bd51902a30e822abfed15015ab4e2c9eaa4d839cf70cf2df975f6d96de` | https://wx.e3861.com/sfyAdmin/Images/Doctor/eae4fd9c-ec75-4803-9016-8d413226875c-280.png |
| 陈婷 | 耳鼻咽喉头颈外科 | 主治医师 | 陈婷-耳鼻咽喉头颈外科-主治医师-广东省妇幼保健院.png | 119072 | 216×280 | `46bb7549ec3291027b956f332e5ffdc27e120ed310e12cc9cef3f8373f0e3c38` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6c4f15ab-1626-433b-b215-d5b11c92c5dd-280.png |
| 郭丽萍 | 乳腺科 | 医师 | 郭丽萍-乳腺科-医师-广东省妇幼保健院.png | 75603 | 208×280 | `0c7caf82952e929dd39660db21637ac26a00b0889a56cf6f5082048ef56098d9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8db9546b-3f19-402c-bc59-fc3dd156f3cd-280.png |
| 陈露雨 | 内科 | 主任医师 | 陈露雨-内科-主任医师-广东省妇幼保健院.png | 66371 | 186×280 | `a34ca8e892d4f877cca95141ecb28144bb7177c2d46f9831af03983146374915` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8590917a-51f1-4f6e-acd4-84d748f167b1-280.jpg |
| 彭玲莉 | 麻醉科 | 主任医师 | 彭玲莉-麻醉科-主任医师-广东省妇幼保健院.png | 74000 | 187×280 | `c4418b784a54cc68019503949f0b0307d6856cea266650353dd2d3cbdc671da2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/962ab12c-6ad1-462f-9dce-4b89e5c4b72d-280.png |
| 施然 | 医疗美容科 | 医师 | 施然-医疗美容科-医师-广东省妇幼保健院.png | 68789 | 199×280 | `d194c38d09a27ca08d09f41d67225c59a187cd3d909ebc421c7410deb067ec2a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/89557b1d-054f-4695-a75b-ce41f96c8f84-280.png |
| 赵欢欢 | 眼科 | 主任医师 | 赵欢欢-眼科-主任医师-广东省妇幼保健院.png | 61646 | 187×280 | `8217081f0c6b3dc35f5a3bce433292a0608c6222a75a29d3e1ed2f524155a312` | https://wx.e3861.com/sfyAdmin/Images/Doctor/784e861c-7c93-4482-a6c5-5ba925673048-280.png |
| 丁茸 | 普通儿科 | 主治医师 | 丁茸-普通儿科-主治医师-广东省妇幼保健院.jpg | 6998 | 187×280 | `73362d199941010ff58693faf194d71cb43b661e87a5d04c62dcc5c5774d4811` | https://wx.e3861.com/sfyAdmin/Images/Doctor/de1d407b-b554-46ec-b80f-d2762c06cbd7-280.jpg |
| 李明洁 | 麻醉科 | 主治医师 | 李明洁-麻醉科-主治医师-广东省妇幼保健院.png | 52000 | 187×280 | `31d834f717579a35cb397760f473b4ed0feb875b04b36664a460393dac741e2e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c16a6536-1682-4c1d-af0a-6e324f12cebf-280.png |
| 吴佳瑶 | 麻醉科 | 主治医师 | 吴佳瑶-麻醉科-主治医师-广东省妇幼保健院.png | 73569 | 187×280 | `fb00c64198720f7286e6c10c5bb55f8341274a4a271600370bc434aa2a8dae8b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f7bc9538-776b-4158-b2b8-0b71621c5851-280.png |
| 姜欣怡 | 心脏中心 | 主治医师 | 姜欣怡-心脏中心-主治医师-广东省妇幼保健院.png | 69887 | 210×280 | `4fbec829893b36fc10d5275e5ac5a94415627d630a7a469d22b8cad7d6ae5106` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c6b283dc-c994-492b-959e-462070499ad1-280.png |
| 张璐璐 | 40+女性健康 | 主治医师 | 张璐璐-40+女性健康-主治医师-广东省妇幼保健院.jpg | 8318 | 280×280 | `b482bb80f8e52de64c9b2741f3b10fcb2c85820b9ec27f39ee808a28f15e86e0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a6c0bac4-579c-4178-8c50-2ecf02a3f3f7-280.jpg |
| 鲍俏 | 小儿泌尿外科 | 主任医师 | 鲍俏-小儿泌尿外科-主任医师-广东省妇幼保健院.jpg | 7127 | 193×280 | `16424568b95c7905c91f1b15c8e92e77b986f16f509853c43d40af904528106d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d0f716b5-9f35-4db4-9353-1633f28bbd58-280.jpg |
| 操日亮 | 小儿骨科 | 主治医师 | 操日亮-小儿骨科-主治医师-广东省妇幼保健院.jpg | 6903 | 210×280 | `4e6fd67f77ef0b65e8fc7ea72cf7bcba2513078ecbdd87668ff02eca4839c533` | https://wx.e3861.com/sfyAdmin/Images/Doctor/adaae11a-f436-48eb-9cbe-1ce3b7d94cb1-280.jpg |
| 刘璐 | 内科 | 主治医师 | 刘璐-内科-主治医师-广东省妇幼保健院.png | 73316 | 187×280 | `cf5997e2df26688e1ad6db391f0d59e979e7db243ee8e4f64fd66c99d9f6cb95` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3451ba19-9c02-449e-8178-af03344d4eb5-280.png |
| 黄原昕 | 妇科 | 医师 | 黄原昕-妇科-医师-广东省妇幼保健院.jpg | 5285 | 199×280 | `8e397b9135f511020b6dad0f5c7d1ad1deaedf38365e8db5ce486f918b5b3e7c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/14204b44-5fd6-4645-9a1d-bd50c48fe903-280.jpg |
| 梁天浩 | 耳鼻咽喉头颈外科 | 医师 | 梁天浩-耳鼻咽喉头颈外科-医师-广东省妇幼保健院.png | 118824 | 280×280 | `e58d14237a8eb3f2838e35ea467b2201e37fc0a68e86262bb6d936d284361a1d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b4e5d275-c976-42c3-a63e-b16f3669e94b-280.jpg |
| 杜重洋 | 妇科 | 主任医师 | 杜重洋-妇科-主任医师-广东省妇幼保健院.png | 87640 | 227×280 | `be80950c74ba735a784abc2416ccfc797dec8c5d756c1fd0c41b54cb7bc808ce` | https://wx.e3861.com/sfyAdmin/Images/Doctor/085b0358-0f07-46d8-9502-29d7a60447ab-280.png |
| 陈煜 | 小儿疝微创 | 主治医师 | 陈煜-小儿疝微创-主治医师-广东省妇幼保健院.jpg | 8040 | 251×280 | `8bbd37a2bdf4b7de099f320320c73f615f7d364c7e3d84fb535a0cef55a5092d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f468bc96-ebf6-4ccb-b28e-1c74c034b198-280.jpg |
| 谭晓琪 | 中医科 | 医师 | 谭晓琪-中医科-医师-广东省妇幼保健院.jpg | 8169 | 259×280 | `c0ad6560c90de91b13cbbc455df2da435e5bc6cebf56042b293c5616d79ccd0f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6d920570-4055-4df2-89c3-c598ba321748-280.jpg |
| 缪佳予 | 儿科呼吸 | 主治医师 | 缪佳予-儿科呼吸-主治医师-广东省妇幼保健院.png | 86897 | 210×280 | `22be0f642fc882f69c12bd7e291d6d920e45a4516fcac7d331138ebaeadcf9f2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2d20f694-3488-487b-adca-077c474aaea7-280.jpg |
| 张恒山 | 中西医结合儿科 | 主治医师 | 张恒山-中西医结合儿科-主治医师-广东省妇幼保健院.jpg | 7083 | 266×280 | `be5aef5d296abd03d207b6ec0ee75823b90298fe952da91006321f596618ae9a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ed708ff1-a4ab-4d01-848d-a56d7396c213-280.jpg |
| 郑泽吟 | 儿科呼吸 | 主治医师 | 郑泽吟-儿科呼吸-主治医师-广东省妇幼保健院.png | 73665 | 280×280 | `3dfcf5aa6d3cecc2617c45e4ecc3c7f4e1bb1908acd5bed9cc2e994cef83f926` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f7b90413-58fb-4e15-9281-d54d38fc68b2-280.png |
| 孙钰玮 | 妇科 | 医师 | 孙钰玮-妇科-医师-广东省妇幼保健院.jpg | 6284 | 199×280 | `62527ae228f66b9e20185e6ee6406098d33814d35cc51044901f6ae151e48829` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a26ffd44-277c-4195-9346-119da5de7546-280.jpg |
| 杨威 | 内科 | 主治医师 | 杨威-内科-主治医师-广东省妇幼保健院.png | 77539 | 186×280 | `40eee5bd2aa9c73afd2376fcc159717bce4d219c34809013095646f3277a55e8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/98db65f6-7d74-4093-8c3c-d80b156ec924-280.jpg |
| 马炜峻 | 小儿泌尿外科 | 主治医师 | 马炜峻-小儿泌尿外科-主治医师-广东省妇幼保健院.png | 56089 | 166×280 | `6afa3f9a5437c1cc2f41a36ff23d8f7889582c9b4fc43cc67046b84e53b109c8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/81d633a5-f70a-4ed8-9f0b-10a259b95bf0-280.png |
| 李善昌 | 未标注 | 医师 | 李善昌-未标注-医师-广东省妇幼保健院.jpg | 5232 | 211×280 | `9fc1322cb4676f5cc7dc24ab7dd2dbc7c82ea74915b649e86430f64bfb2173a1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e7e49b37-0cd5-4b01-9f71-3691b9b0cb2f-280.jpg |
| 黎伟健 | 内科 | 主任医师 | 黎伟健-内科-主任医师-广东省妇幼保健院.png | 77827 | 189×280 | `44adeb3ea5a807cdc63d8542e3329b9d211ae34ea2691bca173bbc0b393d40b4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1cca76be-a841-42fa-85b7-fd9efb6e48af-280.png |
| 文泳欣 | 儿科呼吸 | 医师 | 文泳欣-儿科呼吸-医师-广东省妇幼保健院.png | 76072 | 189×280 | `d4884c41d15a19b7219bd7cc39ceb4038d9517786094b47aa02e93eb486de68b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9bae13d7-8dc0-478a-887d-c4091b14dcc9-280.jpg |
| 郭洪良 | 内科 | 主治医师 | 郭洪良-内科-主治医师-广东省妇幼保健院.jpg | 5551 | 209×280 | `92b66e0be5ad4b3b60b156b8e11bda2c1908947417f5fcc08d82723f89455c1d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3aac7bbe-6121-4620-a947-0fb59a2b7575-280.jpg |
| 梁健女 | 儿科消化 | 主治医师 | 梁健女-儿科消化-主治医师-广东省妇幼保健院.jpg | 6371 | 187×280 | `a20401775f63226f4268b5260fd4d6469243b7a83413e7a922c2961ded24477b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a7da8af1-edbc-4b02-83ad-366da8875ac6-280.jpg |
| 庄泽钦 | 疼痛科 | 医师 | 庄泽钦-疼痛科-医师-广东省妇幼保健院.jpg | 6085 | 199×280 | `f387b0255c963bd9b89ce88b1cb2c9322ae25ec0e78136c054259ec2f29f4bdc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3641e970-99e6-4b58-8095-e6a7275a14fb-280.jpg |
| 张杰 | 康复医学科 | 主治医师 | 张杰-康复医学科-主治医师-广东省妇幼保健院.png | 108261 | 208×280 | `8621c9bd2eaffb23f59d331b019f5f10ecd0b9f8d97cb06460a727af48b04291` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ed3fb33c-e36b-42ca-9376-2f10d481496a-280.png |
| 张怡奎 | 小儿泌尿外科 | 医师 | 张怡奎-小儿泌尿外科-医师-广东省妇幼保健院.png | 88307 | 214×280 | `3bcfca212864ef3bcebae400510179c95def5510a0b19bd38755b0295b11c5f0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ca7e954d-77da-4d89-9cce-176bf43589c9-280.png |
| 马冬菊 | 新生儿科 | 主治医师 | 马冬菊-新生儿科-主治医师-广东省妇幼保健院.jpg | 7220 | 336×280 | `16f1466cea1fe4c832203ceeb44c724acc7e12aa0c8411893f1d71f6086d5f36` | https://wx.e3861.com/sfyAdmin/Images/Doctor/67b91e8b-e9eb-489d-809b-ba6b45c6c0fd-280.jpg |
| 欧阳斌 | 生殖健康与不孕症科 | 主治医师 | 欧阳斌-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 6181 | 181×280 | `f34d25775d8153563086d3b79c17d1a39940d2e7290c1563932309d0496c6a2b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5179b63f-94b7-4ec1-8a35-1de07170903f-280.jpg |
| 柴成伟 | 小儿普外科 | 主任医师 | 柴成伟-小儿普外科-主任医师-广东省妇幼保健院.jpg | 7469 | 199×280 | `388651332639ed3602266ffc551ff220448eb8769af298e6a36610e8b22a2497` | https://wx.e3861.com/sfyAdmin/Images/Doctor/dc00ee52-b31e-4684-a692-354b7301af10-280.jpg |
| 贺振华 | 小儿神经外科 | 主任医师 | 贺振华-小儿神经外科-主任医师-广东省妇幼保健院.jpg | 6281 | 190×280 | `aa805e3b731b8c25cd67eff32a5e3924e2a1074b0559ab3a27ace368a3d6fd69` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f445b28a-b285-4298-a1ef-e4050194e561-280.jpg |
| 许伟滨 | 心脏中心 | 主治医师 | 许伟滨-心脏中心-主治医师-广东省妇幼保健院.png | 69681 | 183×280 | `c0f3a116876a8bd30ffc60af446a8a9aca6bc0840a2d8450d03515609b0a2bc0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/cab749de-9df8-427f-ad19-9f4ea338c6d3-280.png |
| 丁红珂 | 遗传病专科诊疗 | 医师 | 丁红珂-遗传病专科诊疗-医师-广东省妇幼保健院.jpg | 5292 | 187×280 | `932a64dee03cf98b057d7c9c6b2abcc1d20851f352b79f866c003a99380f12b3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/435f82ea-7929-4fd0-b288-97d1427a1d59-280.jpg |
| 齐一鸣 | 遗传病专科诊疗 | 医师 | 齐一鸣-遗传病专科诊疗-医师-广东省妇幼保健院.png | 85114 | 226×280 | `666533dc2b2b59a8dbd048b2c5b4797a4191d188990edca53ebca153daaca92c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/94d2f2a6-ebc4-4b75-a25a-fb90ea052deb-280.png |
| 卢建 | 遗传病专科诊疗 | 医师 | 卢建-遗传病专科诊疗-医师-广东省妇幼保健院.png | 62479 | 187×280 | `5d6a6cdaa39d12f8c44999557df5c2212134c3f795362623547fb55ad735f65f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/db35a532-08ae-4813-b446-eea72fb1dd43-280.png |
| 缪勤飞 | 小儿内科神经内科 | 主治医师 | 缪勤飞-小儿内科神经内科-主治医师-广东省妇幼保健院.jpg | 6335 | 190×280 | `ad9b295143fcb1a8b5d4b8f4e7b6e35543fa4f953f2d272af0ff3b697a246c85` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e5e283c8-9459-4240-be14-ac584fa08bae-280.jpg |
| 曾子纯 | 乳腺科 | 主治医师 | 曾子纯-乳腺科-主治医师-广东省妇幼保健院.jpg | 5458 | 187×280 | `945c80195a5c60a1a8c461d2eff6863d58843b2a948e4750b4a6fa40bb634e9a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/785398d2-dc71-4380-97ac-d30a100da121-280.jpg |
| 任竹潇 | 新生儿科 | 主治医师 | 任竹潇-新生儿科-主治医师-广东省妇幼保健院.jpg | 6287 | 187×280 | `db72e777d933032f9d8d74990a1f55b0f51b7972d68932106813093f035c292d` | https://wx.e3861.com/sfyAdmin/Images/Doctor/dbf951e2-8baa-4db5-b8b7-1555887e2bca-280.jpg |
| 张益阳 | 心脏中心 | 医师 | 张益阳-心脏中心-医师-广东省妇幼保健院.png | 65982 | 210×280 | `e79a76fe068bbb151102622f6c74cb839ff5a785bc848b378aad4ff8b3eef286` | https://wx.e3861.com/sfyAdmin/Images/Doctor/70a2a88a-86a4-4d06-80c7-f90e8baa539c-280.png |
| 夏菁 | 生殖健康与不孕症科 | 医师 | 夏菁-生殖健康与不孕症科-医师-广东省妇幼保健院.png | 89310 | 224×280 | `b0359c787f40eb851f6ed011b107782f7a848325cbed47391ba1b1de21c2f098` | https://wx.e3861.com/sfyAdmin/Images/Doctor/47515720-680c-4e3e-b961-5748f2955839-280.png |
| 黄水清 | 新生儿科 | 主任医师 | 黄水清-新生儿科-主任医师-广东省妇幼保健院.jpg | 8736 | 210×280 | `32fa260247de9e14ff48d96a7bb765dd7ccd00eca5a5f290d46cd9a0b59ca409` | https://wx.e3861.com/sfyAdmin/Images/Doctor/580bff7e-0fb1-4a06-9c01-ba6211a036b9-280.jpg |
| 尹钊红 | 妇女保健科 | 医师 | 尹钊红-妇女保健科-医师-广东省妇幼保健院.jpg | 5637 | 199×280 | `006958eef31e50f834c7ccd4d0a72a9f54225598c96aecc5681b75bc8a4022ad` | https://wx.e3861.com/sfyAdmin/Images/Doctor/50429558-a2d5-45a1-948b-5a4654e44b9b-280.jpg |
| 张晓红 | 普通儿科 | 主任医师 | 张晓红-普通儿科-主任医师-广东省妇幼保健院.jpg | 6070 | 190×280 | `6d1ecc0137a3316497b77f3322ddc49d970684cd9652c424d6616d3b40c8638c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/4389e184-a8c5-4fcd-a7f0-4dccddcaba87-280.jpg |
| 薛玉欣 | 妇科 | 主管技师 | 薛玉欣-妇科-主管技师-广东省妇幼保健院.jpg | 10114 | 326×280 | `381850081852bfbc5b3775a3e5feca42572c8802638eb21ea618a62e1b5ec598` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f2a46c02-a996-48ff-831f-2fe02fd6a643-280.jpg |
| 陈雪莲 | 妇科 | 主任医师 | 陈雪莲-妇科-主任医师-广东省妇幼保健院.png | 110958 | 279×280 | `6bb9a311ddb916d055e45f077d4da2a4dca04b4535d0b3c859c0326e9685f63b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b2f966ec-cab0-4265-9edc-49d4872632c6-280.png |
| 韦锦燕 | 生殖健康与不孕症科 | 主治医师 | 韦锦燕-生殖健康与不孕症科-主治医师-广东省妇幼保健院.jpg | 7018 | 199×280 | `e581a2e3f95d9180c708ff2837eb19c73f3cd9c51d4e0aaab8b1199e403de773` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9350c2f3-07db-40f1-ac8c-29f9d8ab92f7-280.JPG |
| 胡思涛 | 耳鼻咽喉头颈外科 | 医师 | 胡思涛-耳鼻咽喉头颈外科-医师-广东省妇幼保健院.png | 132829 | 269×280 | `ed2719f82af32baebe313f9ab5e9aae5b00cc013b374e82189068f0242b161d0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c59cb4ff-504c-4f2a-adb5-452bfdf07f51-280.jpg |
| 袁静敏 | 疼痛科 | 主治医师 | 袁静敏-疼痛科-主治医师-广东省妇幼保健院.jpg | 7498 | 210×280 | `e5f14b9264aa90015d6fd9bcfc3a04ab7e136225d448099f333706d84c1e751a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6fed04d1-c253-4f67-ad2e-8c78404ddcfe-280.jpg |
| 姚仲伟 | 新生儿科 | 主任医师 | 姚仲伟-新生儿科-主任医师-广东省妇幼保健院.png | 62441 | 187×280 | `a0550fa3c95901baaf1f7fac21bb653ac2fda0e6ff1ee9136444c458491c8af9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ac9aef6e-4a02-4c4c-923d-00a95160eca4-280.png |
| 程雪飞 | 心脏中心 | 主治医师 | 程雪飞-心脏中心-主治医师-广东省妇幼保健院.png | 68879 | 186×280 | `aa5eac51b16744647ec5caba548dde0d92ea1784f97cba9bcb6926cf7d8cc9e1` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d63e6523-82a2-465c-9d25-e61f22f3b3ad-280.png |
| 严隆丽 | 新生儿科 | 主治医师 | 严隆丽-新生儿科-主治医师-广东省妇幼保健院.png | 73876 | 185×280 | `635b83d7371772f076e593016bcc99395c98c1c3af1039e29b3b977a5ebfe6e2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a721edfb-23fb-4db0-82d9-3da2272b4f34-280.png |
| 宗云 | 妇女保健科 | 医师 | 宗云-妇女保健科-医师-广东省妇幼保健院.png | 54614 | 156×280 | `0a4cd32527ed3ae00a3d0358eb0b3da1e515c58d312fc9faac7607eb989a29bc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0e1ba46b-05e1-4a1b-8c03-507c7c629409-280.jpg |
| 王建勋 | 眼科 | 主任医师 | 王建勋-眼科-主任医师-广东省妇幼保健院.png | 93716 | 210×280 | `84999cb852b735669afe4d5163acf995a7199dac76e4848377f4f7fddff6dd8a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ab9bf805-b34b-4bbe-8861-1d178317183a-280.png |
| 张旭 | 心脏中心 | 主任医师 | 张旭-心脏中心-主任医师-广东省妇幼保健院.png | 72604 | 187×280 | `4da65d413f5e5a9b2abdeac79b4f0db2384264c298cf2b87213c762055d27e48` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8ff069f6-9c9f-4782-a7a8-9f583c3e1fe0-280.png |
| 何威 | 小儿肾内科 | 主治医师 | 何威-小儿肾内科-主治医师-广东省妇幼保健院.png | 75766 | 186×280 | `8c34f90c57bda2bf629feef0b5a134c8d91cb0e11d143f7772933dc1aac15659` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c54f7322-baf9-420e-b0d4-50bb4122b162-280.png |
| 郑婕 | 产科 | 主任医师 | 郑婕-产科-主任医师-广东省妇幼保健院.jpg | 6444 | 187×280 | `67c526c27aaf55da6a4e6b5da6b6e5c10c7ff6b6d4a35e706d7e2d29ca905473` | https://wx.e3861.com/sfyAdmin/Images/Doctor/59c9904b-a2fd-4019-903b-7e435c5aed61-280.jpg |
| 戢婷 | 心理科 | 医师 | 戢婷-心理科-医师-广东省妇幼保健院.jpg | 6166 | 199×280 | `3ed9470cdc219fc3fc6665b9407ac6f9cf1a46f8892eb3d654ee5b643569062f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/78ef6d34-8498-471a-b263-ed8d8fddbcf4-280.jpg |
| 黄洁平 | 心理科 | 医师 | 黄洁平-心理科-医师-广东省妇幼保健院.jpg | 5976 | 199×280 | `7502abdb4a962ad7180b2fc85f90027552be642c4ed7ecabba930442224df24e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6e7ea2c9-3f03-4fe4-a14e-dc4826454e9e-280.jpg |
| 刘慧娟 | 心理科 | 未标注 | 刘慧娟-心理科-未标注-广东省妇幼保健院.png | 79019 | 187×280 | `e4e4891d8bc84ba0461c35000cf1cfe2b013204ac37d884530c733c2fdb1c960` | https://wx.e3861.com/sfyAdmin/Images/Doctor/45b2c19f-5d6a-4637-8d8d-a6417bc8eeee-280.jpg |
| 康朦梦 | 新生儿科 | 主治医师 | 康朦梦-新生儿科-主治医师-广东省妇幼保健院.jpg | 5906 | 189×280 | `4af17912cbe8a9335de4ff85700124b3ecff69b26f99918fda35be24d4f7fd22` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1870eb33-b562-461b-b69c-a7c4475896f0-280.jpg |
| 陆文聪 | 儿科 | 主治医师 | 陆文聪-儿科-主治医师-广东省妇幼保健院.png | 100859 | 287×280 | `b0dc7ea674a4b227e6c66261f9d2dfac38eee4bf7033fc94db692661e3d44a32` | https://wx.e3861.com/sfyAdmin/Images/Doctor/95418575-1844-4a7a-abb6-d02a7c8fcf02-280.png |
| 刘王凯 | 儿科呼吸 | 主任医师 | 刘王凯-儿科呼吸-主任医师-广东省妇幼保健院.png | 92751 | 191×280 | `033395c9cf44c5a4892e287e79e5d13ee9e9acb731d2a17d94af3567d2aca1c8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1b336020-4e03-4813-9ff6-41aaef9f583e-280.jpg |
| 马颖 | 儿童保健科 | 主任医师 | 马颖-儿童保健科-主任医师-广东省妇幼保健院.jpg | 8032 | 209×280 | `da59b0661b3b51d9a1bc60279b66c57486b858a854d77394a738e59480d32b53` | https://wx.e3861.com/sfyAdmin/Images/Doctor/52330460-c6c5-40bf-99e4-60aeadc4f675-280.jpg |
| 赵红杰 | 普通儿科 | 医师 | 赵红杰-普通儿科-医师-广东省妇幼保健院.png | 91689 | 245×280 | `054857daaa11e3b532726956f808ea43b9ed2255ff29b8bfa093537c77d03bf5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e6fe17ff-191d-43d6-a70f-fd332bdf1551-280.png |
| 谢露露 | 儿科呼吸 | 主治医师 | 谢露露-儿科呼吸-主治医师-广东省妇幼保健院.png | 145232 | 276×280 | `8657e2e9c81cfe5f5f2e0567cd79ea177129c257bbd4a58815d493e21013c4af` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b876c21e-bb00-41b4-b2ac-5289def7c071-280.png |
| 阳柳 | 新生儿科 | 医师 | 阳柳-新生儿科-医师-广东省妇幼保健院.png | 79527 | 280×280 | `d161535a801acd9c6a503d386d1b80f1747af3238aef624af8627a49f9fb6b73` | https://wx.e3861.com/sfyAdmin/Images/Doctor/70154220-1e5f-4f30-bdc0-29b0de26850e-280.png |
| 徐银玉 | 普通儿科 | 医师 | 徐银玉-普通儿科-医师-广东省妇幼保健院.jpg | 6642 | 238×280 | `c6bc0c61769dc7fcae49d6e146f7bc2a108451d5e0400d643d3c588fec0d05de` | https://wx.e3861.com/sfyAdmin/Images/Doctor/04f0811c-3bdf-4b06-9b5b-9f9e2d85a184-280.jpg |
| 吴淑莲 | 医疗美容科 | 医师 | 吴淑莲-医疗美容科-医师-广东省妇幼保健院.jpg | 6166 | 187×280 | `bbae55b96ca86858a87106928c88d68fd765f86fd7214a5dc9dd34b65d45a5b3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/df2e0bdf-40bd-4aad-a573-7096ad067955-280.jpg |
| 卢洁仪 | 普通儿科 | 医师 | 卢洁仪-普通儿科-医师-广东省妇幼保健院.png | 118788 | 204×280 | `613b401f460ab7061fbf38a2c677ff3c697eb34ce9d9ffbd96215634748877f9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/72e1eb3b-cf4b-461c-b108-b26b0309a178-280.png |
| 杨朝湘 | 放射科 | 主任医师 | 杨朝湘-放射科-主任医师-广东省妇幼保健院.jpg | 6617 | 199×280 | `df73a7c4e41ebf5ac0c3b6f1087857c344d924a1d7ebe77ee44e1a17b1f52afe` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e53a36b6-13c2-44fb-a4be-1fccaca39216-280.jpg |
| 裴铮 | 儿科 | 主治医师 | 裴铮-儿科-主治医师-广东省妇幼保健院.png | 98048 | 218×280 | `92a5348b2cbba7df29bb2a6236ea2580ab455f8315dcf748687accb3e7148797` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f41b4fd8-7613-46bd-b8fb-ce87327ad7a5-280.png |
| 麦建彩 | 公卫科 | 主任医师 | 麦建彩-公卫科-主任医师-广东省妇幼保健院.jpg | 7724 | 200×280 | `21fdf6f5d2a83dd8c06f038186ab07c92e1e38d23038987a51564a3c4d9ab5bd` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b6af4d57-4f0f-4d65-95ed-7dd866154221-280.jpg |
| 梁柳仙 | 公卫科 | 主治医师 | 梁柳仙-公卫科-主治医师-广东省妇幼保健院.png | 90919 | 196×280 | `463d0632b27f55051608a3f4e607c97829a16f338c5b46acd1e626e9cf1f6456` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a90c50af-316a-4451-8a67-eaf4bf5dc139-280.jpg |
| 张华明 | 妇科 | 主治医师 | 张华明-妇科-主治医师-广东省妇幼保健院.png | 150275 | 290×280 | `8618d68017bc2b3625e8fdcc052156a40421a69e9a8c0c3c186aa6d2aff3dfab` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b5c08e28-2eef-4a01-83cf-1c1241e2b351-280.png |
| 罗小琴 | 妇科 | 主任医师 | 罗小琴-妇科-主任医师-广东省妇幼保健院.jpg | 6391 | 210×280 | `e24422d80a2f37c85eadf46aeda9e843fd0a1d8dd9e2502a7de5b6fc30e001b3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d50bd1af-5fb1-444c-91b5-d598b50c2499-280.jpg |
| 刘惠 | 心脏中心 | 医师 | 刘惠-心脏中心-医师-广东省妇幼保健院.png | 66672 | 190×280 | `6488006ee5c8c68af2b15757f85d02100d1191184617eea7fc81005e79d97ebe` | https://wx.e3861.com/sfyAdmin/Images/Doctor/465b04db-df3b-4680-b1a1-dc438b4915f6-280.png |
| 王春艳 | 妇科 | 主治医师 | 王春艳-妇科-主治医师-广东省妇幼保健院.jpg | 5953 | 158×280 | `4e949581395b4a226160d2a9ea2296b4899befc2ac96f432d66bdfb508e356c8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d4ea40ab-c37a-4f68-a65e-82db43c3e49d-280.jpg |
| 王瑞青 | 儿科消化 | 医师 | 王瑞青-儿科消化-医师-广东省妇幼保健院.png | 79159 | 191×280 | `01ed3a1addf9a931d4e7ed5d320e7ec412b069a0105d13986c2c5c0039ceff99` | https://wx.e3861.com/sfyAdmin/Images/Doctor/a4b578fb-d9e0-4e41-a99c-33f6e5dac040-280.jpg |
| 谢禹 | 妇科 | 医师 | 谢禹-妇科-医师-广东省妇幼保健院.jpg | 5460 | 158×280 | `c5566bd9266e0c01785a8913c2f6b61dc331d0fa5230771c80cae46cc26df324` | https://wx.e3861.com/sfyAdmin/Images/Doctor/22f9e47c-78d7-4cff-b381-97c8b5e84ac2-280.jpg |
| 凌皓 | 中医科 | 医师 | 凌皓-中医科-医师-广东省妇幼保健院.jpg | 7757 | 187×280 | `75bd8933aee1962edf711d86b4da40a894e3652bd42754d963904bb3c51703a0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/87cfe6e4-6f84-4c5c-a821-9e07274e6145-280.jpg |
| 朱素婧 | 妇科 | 主任医师 | 朱素婧-妇科-主任医师-广东省妇幼保健院.jpg | 8211 | 205×280 | `3e989a9ec86d889136bd6f259f855f4b312e377712085f862b88616a0a64a243` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3540d919-5d54-412d-9292-0f10ee131136-280.jpg |
| 文笛 | 医疗美容科 | 医师 | 文笛-医疗美容科-医师-广东省妇幼保健院.png | 92484 | 210×280 | `76fe2ba374d76c036882f3bc2395df1ef2818323272f688e376d53ee8a38c116` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5e239074-89dc-4c8b-80c6-048f61f35b3e-280.png |
| 易爱文 | 康复医学科 | 主任医师 | 易爱文-康复医学科-主任医师-广东省妇幼保健院.jpg | 6668 | 190×280 | `1997a4e3511d75e44f4e9935d79dc4547b731a069dfed3266671d26a5887f93e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/47954a4d-95e4-4670-ad1c-7df9dd8e7b18-280.jpg |
| 陕萌萌 | 妇科 | 医师 | 陕萌萌-妇科-医师-广东省妇幼保健院.png | 99388 | 241×280 | `7306944f65830cd9447ab147bc3df012dbd0745709f19adb0215545d6016791f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e1eff8e1-da86-4879-8704-dd66d7d59ecb-280.png |
| 陈霞 | 妇科 | 医师 | 陈霞-妇科-医师-广东省妇幼保健院.png | 70707 | 204×280 | `4812119056558e918f97ee9f7d4f9ad290829c190d2369415c3b3ea49a2766f8` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ca139e1c-c16f-4cec-8e54-7772e83072ce-280.png |
| 李诗韵 | 儿童保健科 | 主任医师 | 李诗韵-儿童保健科-主任医师-广东省妇幼保健院.png | 125002 | 208×280 | `6aa42916045027bd0bd6e4d43d725d5320b74e8559f058a9c983b3d2b08af406` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e0c4a22c-356b-4c01-8343-e665337f76d6-280.png |
| 刁雨菁 | 妇科 | 医师 | 刁雨菁-妇科-医师-广东省妇幼保健院.png | 158769 | 292×280 | `88d9b0a4bd318f90f2af5358b5d5725be116cdf2499e6744155f61dcc8ede3bf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6c972e14-808f-492d-8f0e-a0403c3a9ef3-280.jpg |
| 刘泳如 | 营养科 | 医师 | 刘泳如-营养科-医师-广东省妇幼保健院.png | 46300 | 204×280 | `abc6a53270b62201137332c4e5e97ad7b5ddd43ad5afa36685b331d5650f27b6` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9c25d7f1-2421-4977-903f-f36b03d1c2a3-280.png |
| 冯阳春 | 内科 | 主任医师 | 冯阳春-内科-主任医师-广东省妇幼保健院.png | 81978 | 187×280 | `5924cab714f5c5606b1948a2b7523d1eae6715df3da9ad88aa70b543b195a178` | https://wx.e3861.com/sfyAdmin/Images/Doctor/5a5ab9fa-d246-4432-ab06-f6e5ed84cf80-280.png |
| 罗芳梅 | 普通儿科 | 医师 | 罗芳梅-普通儿科-医师-广东省妇幼保健院.jpg | 8825 | 394×280 | `2545b7fa6e6229d2223abdf88f46c6a7bc7295898376048e7e6c015133968b9f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c109119b-76ea-46e0-969e-db11472d5c6f-280.jpg |
| 姚少敏 | 儿童保健科 | 主治医师 | 姚少敏-儿童保健科-主治医师-广东省妇幼保健院.jpg | 7557 | 210×280 | `9e2b0429870a15523ee36daaec9e3fea409124f96e4b8b563b46978681ea81d9` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0cabddd2-309a-48ed-bd1a-3080634eb293-280.JPG |
| 欧爱华 | 儿童保健科 | 医师 | 欧爱华-儿童保健科-医师-广东省妇幼保健院.png | 68656 | 193×280 | `4f7ddcb30e6ac65d7fde4c04304613eb81c195cb80fa02cf1a71feac4f649155` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f02f379a-f8d7-458b-a8ae-de313179a9cf-280.png |
| 黄朝阳 | 耳鼻咽喉头颈外科 | 主任医师 | 黄朝阳-耳鼻咽喉头颈外科-主任医师-广东省妇幼保健院.jpg | 7734 | 200×280 | `90e9b57fb00d64a8431ab9a7c927b65e22a49d1808256b0e00dfce245ae9db42` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3c5e593b-a753-4ba7-b44b-a612940e9e0b-280.jpg |
| 曹颖璇 | 医疗美容科 | 医师 | 曹颖璇-医疗美容科-医师-广东省妇幼保健院.jpg | 6309 | 224×280 | `dc248566b6dd041a7d71d1c33a1fd7f9da2204040f8d66cf3f62f4d4009b84ad` | https://wx.e3861.com/sfyAdmin/Images/Doctor/c9122aa9-af01-4e86-a2be-941588930b66-280.jpg |
| 郭志鹏 | 儿科发热 | 医师 | 郭志鹏-儿科发热-医师-广东省妇幼保健院.png | 80553 | 195×280 | `cb2861bd0632d5384a65109bce795db7f9981256d81494ee0effd7c3e5adf2a2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/38d315d8-0692-46bf-ba51-40df8552b9df-280.png |
| 莫镜 | 新生儿科 | 主治医师 | 莫镜-新生儿科-主治医师-广东省妇幼保健院.jpg | 7006 | 189×280 | `e66495c225de712387106a38fc6069b12179d59d3edb187cdd1c5a305b3ddd00` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e70d02ed-7174-4bb5-967e-4909439f77d8-280.jpeg |
| 赵新月 | 乳腺科 | 医师 | 赵新月-乳腺科-医师-广东省妇幼保健院.jpg | 7380 | 202×280 | `ab392dbdfed14e3082c752451db066c0b0ede89c68587f20321b96234077f29c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8f3fab7c-f82c-4fb5-9562-8cf8db9f8d09-280.jpg |
| 吴伟晴 | 普通儿科 | 医师 | 吴伟晴-普通儿科-医师-广东省妇幼保健院.png | 93639 | 254×280 | `40d92a5dd6f466389aa60d2e7f6ec00ad8a8bad37bb5a2b13a5357d4279d12f5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/31e2329b-d870-49d1-9e0d-ae2f61050602-280.jpg |
| 李幼雪 | 乳腺科 | 医师 | 李幼雪-乳腺科-医师-广东省妇幼保健院.png | 85451 | 204×280 | `d25bc9e38beb6dfb75e5aca684e5cca27a58d41765b00c420b223f1c2433f71e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8fc9ea25-d2c8-466d-ac25-43886eab153b-280.png |
| 杨凡 | 医疗美容科 | 医师 | 杨凡-医疗美容科-医师-广东省妇幼保健院.png | 51329 | 180×280 | `b046f1dd9f206c8d7528dbd8ebce541fd7f345bbb129350c8cd06bbbcbe81724` | https://wx.e3861.com/sfyAdmin/Images/Doctor/576cefd2-4a72-4ae2-aff8-82c7d0d04fe6-280.png |
| 禤嘉明 | 中医科 | 医师 | 禤嘉明-中医科-医师-广东省妇幼保健院.jpg | 6226 | 187×280 | `3612e566fc890a877fedd56b1506f8bd9ae16c86999b2310c23a61ed1a4df08f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8c5edd42-29e6-437e-8492-ed394fcbf3a2-280.JPG |
| 杨鸿 | 中医科 | 医师 | 杨鸿-中医科-医师-广东省妇幼保健院.png | 81045 | 187×280 | `b02fd07033034875a16801a855627c7582bbd64666087d695db4018e127aa4cb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fc726202-8d0c-4f05-94c9-08f6e738a7bf-280.png |
| 周浩 | 中医科 | 医师 | 周浩-中医科-医师-广东省妇幼保健院.jpg | 6768 | 212×280 | `69f1884aedfd674d4869a55e18c188cb26c207db288c67a6e843e3d0f4794fa5` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e2badac4-47e9-42f2-98b3-5ad70e9030ab-280.jpg |
| 黄如湘 | 中医科 | 医师 | 黄如湘-中医科-医师-广东省妇幼保健院.png | 73692 | 187×280 | `0a62b587fbc65855eb58c99560e2771d24eaa0f75d82211001d51a17976afd11` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fbd111ff-dc18-413b-9387-47a9790767ae-280.png |
| 刘源杰 | 中医科 | 医师 | 刘源杰-中医科-医师-广东省妇幼保健院.png | 83930 | 188×280 | `35f4bcf9710b0ee70405f41ef8d015db6802117dee88ccb7a9012f451c0f69cc` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7e79cc1e-789c-4067-bb4c-4ffb084a54e3-280.png |
| 胡祖荣 | 未标注 | 主任医师 | 胡祖荣-未标注-主任医师-广东省妇幼保健院.png | 88477 | 206×280 | `8425e43d05c362bc4d4cf01dffc26ab0f9afe81c32b6d9b9e5c0963f88daed34` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9bf4bb54-f478-45b3-8d09-1f3abc2e7028-280.png |
| 陈奕莹 | 中医科 | 医师 | 陈奕莹-中医科-医师-广东省妇幼保健院.png | 77675 | 187×280 | `0ce1902492211bede728350629cd5e0b512908e5d843cda41afd05f2efd1cd8c` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ebf35e04-eff4-4d1a-a8d4-6009e8e28f55-280.png |
| 黄思敏 | 中医科 | 医师 | 黄思敏-中医科-医师-广东省妇幼保健院.jpg | 6170 | 199×280 | `d1eb3d42ad2c19af9d2daa6b8bc8db2bb90c69ad2c58bb0bbe9f46a11c24062e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/bdc32aa4-86bd-4298-ba4b-e942d55abfab-280.jpg |
| 赖美娴 | 中医科 | 医师 | 赖美娴-中医科-医师-广东省妇幼保健院.jpg | 6425 | 210×280 | `e6c8de5050feb0fa525f1e4a9ef003ef87e98655ab568782944c3265fd34b52a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/b8f335a2-42e1-463a-a70a-16ac94eb1b87-280.jpg |
| 陈运聪 | 小儿外科 | 医师 | 陈运聪-小儿外科-医师-广东省妇幼保健院.jpg | 7213 | 210×280 | `d4c9fb1c1a38b300448663188cf8f1df9a7f26b6a37dfb406a1c4a74288fe04b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ff6cdd37-76a3-4015-9cc1-38f03fd49323-280.jpg |
| 李婷 | 小儿外科 | 医师 | 李婷-小儿外科-医师-广东省妇幼保健院.jpg | 5177 | 164×280 | `7c235d0cc6b4a2436bab10ce2ccc1b3d7a2fb42cdb18c080a9b767b63fba7fd3` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9901ef4f-c7f5-4d5f-9fd2-6b3235037d33-280.jpg |
| 陆嘉杰 | 小儿外科 | 医师 | 陆嘉杰-小儿外科-医师-广东省妇幼保健院.png | 66895 | 209×280 | `98c5db623a37450a6b15c9a8ba459c099cafb86b5cda1c90c538fe31f09037cb` | https://wx.e3861.com/sfyAdmin/Images/Doctor/19b67028-900c-431b-a241-057e2c13457d-280.png |
| 李鹏 | 小儿外科 | 主治医师 | 李鹏-小儿外科-主治医师-广东省妇幼保健院.jpg | 6744 | 201×280 | `d53f41fb59c1faf24833e952bd334e55bf641a4f098eb5fe3e239ca85f618c2e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/0c89e2b4-96be-4646-a90a-8969de4eda8d-280.jpg |
| 周斌 | 儿科 | 主治医师 | 周斌-儿科-主治医师-广东省妇幼保健院.jpg | 6958 | 210×280 | `10b48a9fb27950f2c824982d5a3e19742e9e4655edf8accd2a955da26101e2df` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7b5db3c4-e624-4599-89ac-56891ebd8605-280.jpg |
| 王淑珍 | 儿科 | 主任医师 | 王淑珍-儿科-主任医师-广东省妇幼保健院.jpg | 5852 | 224×280 | `28bfa2c67fd269c98ead440f07c8efb9aff959e7bf2687ab8b8c814f52294a0e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/9a423c7f-fba8-47cf-8cb4-4e8652573200-280.jpg |
| 韩颖 | 儿科 | 主任医师 | 韩颖-儿科-主任医师-广东省妇幼保健院.png | 93225 | 219×280 | `5394e79f96fa75f9b0409e914e4e0a8278aad48eaa6aa86fd0c7dae6664f992e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/6c4bd998-f4f6-47e9-96a0-ba54b55121bb-280.jpg |
| 黎玉涵 | 妇科 | 主治医师 | 黎玉涵-妇科-主治医师-广东省妇幼保健院.jpg | 8726 | 280×280 | `41b832a03e12299a0e6957b45a48d9e592bfafc3468ab537f2bb6d7091361c22` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1d7ca391-2c6c-4eee-a6f5-8cb900de6185-280.jpg |
| 文元义 | 儿科 | 主任医师 | 文元义-儿科-主任医师-广东省妇幼保健院.png | 87697 | 253×280 | `be53dac7d9c67e904fd1e6d068667672f3feca9872998951bce6efb83cbee7d2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/62f3c317-b97d-45bf-b4f0-275baf13d93d-280.png |
| 魏良铜 | 儿科 | 主任医师 | 魏良铜-儿科-主任医师-广东省妇幼保健院.png | 77118 | 199×280 | `d77e12894da1651077cf1ab9f9ebe0f1789e9e84b26220a66365a6d7b018ec9f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d83fc807-5d6c-43b6-a61c-0cc25e1b0f80-280.png |
| 张海迪 | 儿科 | 医师 | 张海迪-儿科-医师-广东省妇幼保健院.png | 100352 | 205×280 | `08eb6e2ddf5e5034004bdbfbb7683b5d6e2e3d4440bb99031be60f27a9c3a79e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/902566e4-d88b-4554-b73e-0072b64387bf-280.png |
| 李月 | 儿科 | 医师 | 李月-儿科-医师-广东省妇幼保健院.png | 81479 | 298×280 | `9626d38dc1581249d9d32b4a11ad151c63e9733d5e1dc287427f4bb1c4dcec81` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f995b2af-b218-45b6-9223-db104fbbd4a0-280.png |
| 王桃 | 儿科 | 主治医师 | 王桃-儿科-主治医师-广东省妇幼保健院.png | 80466 | 194×280 | `5975e0dcd8a75625d3335bfe0c996f64a955f2b0f6793e247ce22d3288364b6e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e4a774bd-9dde-4718-aa7a-33eacef4c8dc-280.png |
| 胡彩兰 | 体检科 | 主任医师 | 胡彩兰-体检科-主任医师-广东省妇幼保健院.jpg | 6795 | 210×280 | `734a3a929b0d74174c06df4363ca0003866399441a3acf7fdd73b5b078c6597a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/3823d2b9-a88d-4d7f-a907-4d318477bd77-280.jpg |
| 王智琴 | 皮肤性病科 | 主治医师 | 王智琴-皮肤性病科-主治医师-广东省妇幼保健院.jpg | 8407 | 299×280 | `72b0dc354bc2a3fc320edc95d303256c12e40bf295f6413bf1524455248b567b` | https://wx.e3861.com/sfyAdmin/Images/Doctor/36b9b570-d251-490e-bb3d-caf1be069dfa-280.jpg |
| 刘丽娜 | 产科 | 主任医师 | 刘丽娜-产科-主任医师-广东省妇幼保健院.jpg | 6616 | 210×280 | `f80b11778111a52abcf2799676d20d0b6ec3ab8765ed498c6f254e657fecb5bf` | https://wx.e3861.com/sfyAdmin/Images/Doctor/7110cc3b-c2ee-42d7-9d98-7bf0d9786857-280.jpg |
| 周金婵 | 产科 | 主治医师 | 周金婵-产科-主治医师-广东省妇幼保健院.jpg | 7401 | 210×280 | `7555d3f78a439d39dd030d468e503f97b20508d734c362832f72cba247978930` | https://wx.e3861.com/sfyAdmin/Images/Doctor/73fcbf00-8591-483b-a1f6-0bc845e507ee-280.jpg |
| 吴志君 | 产科 | 主任医师 | 吴志君-产科-主任医师-广东省妇幼保健院.jpg | 6753 | 210×280 | `0b123aa61c1c49d5a1428d9153ae8ab67ff42ae8338c6abf4ee4d13a697ab705` | https://wx.e3861.com/sfyAdmin/Images/Doctor/2888ad29-c6bc-46f5-8905-92d1ecabe3e1-280.jpg |
| 段冬梅 | 产科 | 主任医师 | 段冬梅-产科-主任医师-广东省妇幼保健院.jpg | 6661 | 230×280 | `7aded96307c4b6d26d9c703e5d1406273b2affc259fca7611bc9fe87acf7161e` | https://wx.e3861.com/sfyAdmin/Images/Doctor/aaacae63-722a-4006-b23d-e8269b8a71ae-280.jpg |
| 潘秀芹 | 产科 | 主任医师 | 潘秀芹-产科-主任医师-广东省妇幼保健院.jpg | 8803 | 210×280 | `ebbbdedf169947e009eff968501ee81f6a474e3316a74d3270b116d538faaac4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/8cac6275-b8df-4862-a201-16c1e053eb9e-280.jpg |
| 王穗琼 | 药学咨询 | 主任药师 | 王穗琼-药学咨询-主任药师-广东省妇幼保健院.png | 99588 | 232×280 | `3141404d6a589c7a2f4ecd2c8f2d4e439bae8c276800953107ba3828d6833c9f` | https://wx.e3861.com/sfyAdmin/Images/Doctor/d5c9d12f-9f1a-4f76-8ffb-d43f5de03348-280.png |
| 陈俊柱 | 骨科 | 主任医师 | 陈俊柱-骨科-主任医师-广东省妇幼保健院.jpg | 6731 | 250×280 | `7a43401024a0cd6cbd23fa9af3facd623c6db4f886d026e234288eb24573f65a` | https://wx.e3861.com/sfyAdmin/Images/Doctor/db57e318-975f-472b-8a47-1a43301a8ceb-280.jpg |
| 廖嘉炜 | 骨科 | 医师 | 廖嘉炜-骨科-医师-广东省妇幼保健院.jpg | 8204 | 210×280 | `0cd8f0e3558c84048080c3048a2ae8b124451bdf7d987ca15e71886d9bea06c0` | https://wx.e3861.com/sfyAdmin/Images/Doctor/fcfc38ca-8fae-4d00-ab27-9e494a34b320-280.jpg |
| 唐卉 | 未标注 | 主治医师 | 唐卉-未标注-主治医师-广东省妇幼保健院.png | 49777 | 187×280 | `07c87b5aad043519769b00f5e072591e5f79a41b4ee0474202531dc30e63ba12` | https://wx.e3861.com/sfyAdmin/Images/Doctor/f0e12c14-2352-4446-a69e-872ef9e4cf93-280.png |
| 钟丽英 | 中西医结合儿科 | 医师 | 钟丽英-中西医结合儿科-医师-广东省妇幼保健院.jpg | 6684 | 210×280 | `73a42afd80409940d63582966945bdadf81645a014a55bcef0b9a79510941103` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1584e5c0-d615-4337-9588-5c609eff1e9b-280.JPG |
| 王际晴 | 新生儿科 | 医师 | 王际晴-新生儿科-医师-广东省妇幼保健院.png | 77932 | 202×280 | `98c21cdba190a93d4bfeb2257d4bd20628d58d4ea51bb70f97a026807ec942e2` | https://wx.e3861.com/sfyAdmin/Images/Doctor/ecec9165-e588-4800-a587-0a4c22552b8b-280.png |
| 萧国良 | 新生儿科 | 主治医师 | 萧国良-新生儿科-主治医师-广东省妇幼保健院.jpg | 7700 | 200×280 | `fedcfa780c6a60844957fb9f98dabf0c6d085ae9bfcf61c0426f866cd21f9283` | https://wx.e3861.com/sfyAdmin/Images/Doctor/1688f83a-c970-4e43-9262-699baebb99df-280.jpg |
| 杨洋 | 儿科 | 主治医师 | 杨洋-儿科-主治医师-广东省妇幼保健院.png | 64918 | 181×280 | `304ff8a3383604a620b94f76cf30c4e57144d088ec6ba67c576f77ba34ed8cb4` | https://wx.e3861.com/sfyAdmin/Images/Doctor/e60eb84d-ddb2-4e6d-a85a-c514b7265049-280.png |
| 郑璇儿 | 新生儿科 | 主治医师 | 郑璇儿-新生儿科-主治医师-广东省妇幼保健院.jpg | 6958 | 218×280 | `ec914c1bbf63a81f82b67ce73fa0778c5cad8e45866041976af4461c26b86542` | https://wx.e3861.com/sfyAdmin/Images/Doctor/39e1eca3-b3e0-4299-9c34-b9881d40f95d-280.jpg |

### 同名身份聚类裁决

| 姓名 | 详情 ID | 裁决 | 原关系数 | 合并科室 | 主详情 | 其余详情 |
|---|---|---|---:|---|---|---|
| 郭庆禄 | 34640,34931 | 同一人归并 | 2 | 乳腺疾病影像学诊断（清远院区） | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34640.html | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34931.html |
| 周真 | 32647 | 同名待甄别 | 1 | 儿科呼吸、儿童过敏多学科联合（番禺院区） | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32647.html | 无 |
| 周真 | 32821 | 同名待甄别 | 1 | 皮肤性病科（番禺院区） | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32821.html | 无 |
| 刘颖 | 32499 | 同名待甄别 | 1 | 生殖健康与不孕症科（番禺院区） | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32499.html | 无 |
| 刘颖 | 33007 | 同名待甄别 | 1 | 新生儿科（越秀院区） | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33007.html | 无 |
| 何裕 | 32750 | 同名待甄别 | 1 | 妇科（番禺院区） | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32750.html | 无 |
| 何裕 | 33134 | 同名待甄别 | 1 | 体检科（清远院区） | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33134.html | 无 |


## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=2 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33000.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=4 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35596.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=4 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35597.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=5 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35071.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=5 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33153.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=12 | 副主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35166.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=13 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32779.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=27 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35076.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=34 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35599.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=36 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35598.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=41 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35603.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=49 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32780.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=56 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35594.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=57 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32999.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=57 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32938.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=57 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35088.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=61 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35089.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=68 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35091.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=73 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35093.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=74 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35094.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=74 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35095.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=74 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32566.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=74 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35096.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=77 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32576.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=78 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32914.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=79 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35686.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=80 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35604.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=81 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34770.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=82 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33001.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=82 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35090.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=86 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32455.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=89 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35050.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=89 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34732.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=90 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35055.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=90 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35601.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=93 | 无 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35066.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=95 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32971.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=95 | 主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33286.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=95 | 医士 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33326.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=96 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/34678.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=96 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35600.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=97 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35602.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=106 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35730.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=109 | 副主任医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/32897.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=109 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33269.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=110 | 医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35476.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=110 | 主治医师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/33271.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=110 | 药师 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35109.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=111 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35110.html | 官网目录卡片为号源/系统账号/非姓名或护理身份，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=111 | 其他 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35111.html | FULL 末尾验收确认目录卡片为服务项或收费账号，排除医生画像范围 |
| https://www.e3861.com/keshizhuanjia/zhuanjiajieshao?searchDoctor=&searchDepartment=&page=111 | 收费 | https://www.e3861.com/keshizhuanjia/zhuanjiajieshao/35129.html | FULL 末尾验收确认目录卡片为服务项或收费账号，排除医生画像范围 |

## 输出文件

- Excel 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx`
- CSV 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 111 |
| 原始医生卡片记录 | 884 |
| 跨入口去重前候选关系 | 884 |
| 跨入口去重后唯一候选 | 884 |
| 排除非医生候选 | 51 |
| 合规医生详情页 | 833 |
| 最终医生身份 | 832 |
| 覆盖科室数 | 89 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 832 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 118 |
| 慢性病 | 105 |
| 术后恢复/康复 | 102 |
| 生殖疾病 | 148 |
| 疑难重症 | 182 |
| 肿瘤 | 125 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 妇科（番禺院区） | 29 |
| 产科（番禺院区） | 28 |
| 麻醉科（越秀院区） | 25 |
| 普通儿科（越秀院区） | 19 |
| 麻醉科（番禺院区） | 18 |
| 新生儿科（天河院区） | 17 |
| 妇科（越秀院区） | 16 |
| 口腔科（番禺院区） | 16 |
| 生殖健康与不孕症科（番禺院区） | 14 |
| 新生儿科（番禺院区） | 13 |
| 心脏中心（番禺院区） | 12 |
| 儿科呼吸（番禺院区） | 12 |
| 儿科（清远院区） | 12 |
| 普通儿科（天河院区） | 11 |
| 内科（番禺院区） | 11 |
| 产科（越秀院区） | 11 |
| 产科（清远院区） | 11 |
| 乳腺科（番禺院区、越秀院区） | 10 |
| 中医科（番禺院区） | 10 |
| 妇科（清远院区） | 10 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 详情正文为空或未识别 | 244 |
| 科室需人工复核 | 30 |
| 同名待甄别 | 6 |
| 职称/身份需人工复核 | 6 |

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
