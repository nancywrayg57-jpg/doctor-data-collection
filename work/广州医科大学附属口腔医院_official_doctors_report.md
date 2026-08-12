---
类型: 全量采集归并审计报告
医院: 广州医科大学附属口腔医院
城市: 广州市
采集日期: 2026-08-13
来源范围: 医院官网
采集入口: https://www.gykqyy.com/list.html?category=55
适配器: gykqyy_public_doctor_api
---

# 广州医科大学附属口腔医院 官方医生全量采集归并审计报告

## 结论

本次试跑只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集全量采集底表，共 297 位唯一医生；官网列表页原始卡片记录 317 条；读取入口分类 1 个；覆盖 46 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 广州医科大学附属口腔医院 |
| 官网首页 | https://www.gykqyy.com/ |
| 本轮医生入口 | https://www.gykqyy.com/list.html?category=55 |
| 入口来源 | GitHub Issue #22（与官网入口台账一致） |
| 原台账医生入口 | https://www.gykqyy.com/list.html?category=55 |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | A-优先自动采集 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
| 医生团队（category=55） | https://www.gykqyy.com/list.html?category=55 | 动态 Vue 医生目录；单次同域公开接口载入 | 1 | 317 | 297 | 1 | 广州医科大学附属口腔医院 | 官网同域、无鉴权、无内部参数 |

### 动态目录专项证据

- 医生分页/载入方式：医生专区由单次 getZhuanjiaList 请求一次性返回，无 page/pageNo 参数
- 医生目录公开接口：https://www.gykqyy.com/api/article/getZhuanjiaList
- 医生详情公开接口：https://www.gykqyy.com/api/article/getArticleDetail
- 接口出处证据：医生目录 HTML 内联 Vue 脚本的 axios.get 明确声明两个同域公开接口
- 院区/分组：5 个；科室分类：31 个
- 医生-科室关系：317 条
- 唯一详情 ID：297 个
- 有姓名详情 ID：297 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：295 个
- 同名不同详情 ID：2 组

| 同名 | 详情 ID |
|---|---|
| 方颖 | 128,307 |
| 赵稚宁 | 29,323 |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：317
- 跨入口去重后唯一候选：297
- 跨入口重复关系：0
- 试采覆盖入口分类：1 个（医生团队（category=55））

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 无 | 无 | 无 |

## 广东省第二中医院同名归并对账

- 详情关系：0
- 最终身份：0
- 白云院区样本：0
- 多链接同一人归并样本：0

| 姓名 | 裁决 | 详情关系 | 合并科室 | 主详情 | 其余详情 |
|---|---|---:|---|---|---|
| 无 | 无 | 0 | 无 | 无 | 无 |

## 广医口腔逐 ID 归并/排除对账

- 目录详情 ID：297
- 有姓名详情 ID / 正式行：297 / 297
- 空姓名详情 ID：0
- 同名不同 ID 分行：4

| 详情 ID | 姓名 | 处置 | 科室 | 来源链接 | 理由 |
|---|---|---|---|---|---|
| 195 | 李江 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=195 | 官网科室树唯一详情 ID |
| 136 | 张清彬 | 唯一 ID 保留 | 荔湾院区颞下颌关节科、越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=136 | 官网科室树唯一详情 ID |
| 80 | 江千舟 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=80 | 官网科室树唯一详情 ID |
| 196 | 郭吕华 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=196 | 官网科室树唯一详情 ID |
| 51 | 朴正国 | 唯一 ID 保留 | 荔湾院区口腔颌面外科、越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=51 | 官网科室树唯一详情 ID |
| 70 | 吴哲 | 唯一 ID 保留 | 荔湾院区口腔修复科、越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=70 | 官网科室树唯一详情 ID |
| 110 | 刘畅 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=110 | 官网科室树唯一详情 ID |
| 240 | 申玉芹 | 唯一 ID 保留 | 荔湾院区牙周病科、越秀院区牙周病科、专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=240 | 官网科室树唯一详情 ID |
| 210 | 杨雪超 | 唯一 ID 保留 | 越秀院区牙体牙髓科、专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=210 | 官网科室树唯一详情 ID |
| 123 | 王丽萍 | 唯一 ID 保留 | 荔湾院区口腔种植科、越秀院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=123 | 官网科室树唯一详情 ID |
| 31 | 曾素娟 | 唯一 ID 保留 | 荔湾院区儿童口腔科、专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=31 | 官网科室树唯一详情 ID |
| 3 | 杨莉 | 唯一 ID 保留 | 专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=3 | 官网科室树唯一详情 ID |
| 52 | 欧阳可雄 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=52 | 官网科室树唯一详情 ID |
| 301 | 王朝俭 | 唯一 ID 保留 | 放射科 | https://www.gykqyy.com/list.html?category=55&id=301 | 官网科室树唯一详情 ID |
| 182 | 鲍喆煊 | 唯一 ID 保留 | 越秀院区口腔黏膜病科、综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=182 | 官网科室树唯一详情 ID |
| 111 | 陈良娇 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=111 | 官网科室树唯一详情 ID |
| 239 | 于淼 | 唯一 ID 保留 | 越秀院区牙周病科、专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=239 | 官网科室树唯一详情 ID |
| 302 | 覃兆军 | 唯一 ID 保留 | 麻醉手术中心 | https://www.gykqyy.com/list.html?category=55&id=302 | 官网科室树唯一详情 ID |
| 259 | 陈建明 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=259 | 官网科室树唯一详情 ID |
| 171 | 周丽斌 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=171 | 官网科室树唯一详情 ID |
| 20 | 于丽娜 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=20 | 官网科室树唯一详情 ID |
| 152 | 张云燕 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=152 | 官网科室树唯一详情 ID |
| 198 | 黄江勇 | 唯一 ID 保留 | 越秀院区口腔修复科、专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=198 | 官网科室树唯一详情 ID |
| 5 | 杜发亮 | 唯一 ID 保留 | 专家门诊特诊中心、全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=5 | 官网科室树唯一详情 ID |
| 241 | 余挺 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=241 | 官网科室树唯一详情 ID |
| 287 | 熊洁 | 唯一 ID 保留 | 荔湾院区综合急诊科、便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=287 | 官网科室树唯一详情 ID |
| 213 | 杜暘 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=213 | 官网科室树唯一详情 ID |
| 258 | 张斌 | 唯一 ID 保留 | 正畸与儿童口腔中心 | https://www.gykqyy.com/list.html?category=55&id=258 | 官网科室树唯一详情 ID |
| 33 | 刘亚蕊 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=33 | 官网科室树唯一详情 ID |
| 81 | 张晓蓉 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=81 | 官网科室树唯一详情 ID |
| 128 | 方颖 | 同名不同 ID 分行保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=128 | 同名待甄别 |
| 112 | 吴晓雪 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=112 | 官网科室树唯一详情 ID |
| 138 | 张戎 | 唯一 ID 保留 | 越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=138 | 官网科室树唯一详情 ID |
| 172 | 匡威 | 唯一 ID 保留 | 越秀院区口腔颌面外科、专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=172 | 官网科室树唯一详情 ID |
| 197 | 罗涛 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=197 | 官网科室树唯一详情 ID |
| 211 | 朱玉婷 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=211 | 官网科室树唯一详情 ID |
| 4 | 林婷 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=4 | 官网科室树唯一详情 ID |
| 124 | 杨岚 | 唯一 ID 保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=124 | 官网科室树唯一详情 ID |
| 137 | 郝建锁 | 唯一 ID 保留 | 越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=137 | 官网科室树唯一详情 ID |
| 272 | 赵世勇 | 唯一 ID 保留 | 越秀院区口腔种植科、专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=272 | 官网科室树唯一详情 ID |
| 212 | 王伟东 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=212 | 官网科室树唯一详情 ID |
| 32 | 徐冬雪 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=32 | 官网科室树唯一详情 ID |
| 53 | 赵伟 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=53 | 官网科室树唯一详情 ID |
| 139 | 邓力 | 唯一 ID 保留 | 荔湾院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=139 | 官网科室树唯一详情 ID |
| 140 | 麦熙 | 唯一 ID 保留 | 荔湾院区颞下颌关节科、越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=140 | 官网科室树唯一详情 ID |
| 308 | 刘春江 | 唯一 ID 保留 | 麻醉手术中心 | https://www.gykqyy.com/list.html?category=55&id=308 | 官网科室树唯一详情 ID |
| 35 | 盛婷 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=35 | 官网科室树唯一详情 ID |
| 317 | 俞艳 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=317 | 官网科室树唯一详情 ID |
| 126 | 韦丽芬 | 唯一 ID 保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=126 | 官网科室树唯一详情 ID |
| 87 | 孔媛媛 | 唯一 ID 保留 | 荔湾院区牙体牙髓科、专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=87 | 官网科室树唯一详情 ID |
| 74 | 吕胡玲 | 唯一 ID 保留 | 荔湾院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=74 | 官网科室树唯一详情 ID |
| 106 | 秦文光 | 唯一 ID 保留 | 荔湾院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=106 | 官网科室树唯一详情 ID |
| 72 | 余培 | 唯一 ID 保留 | 荔湾院区口腔修复科、专家门诊特诊中心 | https://www.gykqyy.com/list.html?category=55&id=72 | 官网科室树唯一详情 ID |
| 118 | 赵陆 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=118 | 官网科室树唯一详情 ID |
| 256 | 欧玲伶 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=256 | 官网科室树唯一详情 ID |
| 82 | 张文娟 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=82 | 官网科室树唯一详情 ID |
| 83 | 闫亮 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=83 | 官网科室树唯一详情 ID |
| 300 | 吴磊 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=300 | 官网科室树唯一详情 ID |
| 55 | 张君伟 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=55 | 官网科室树唯一详情 ID |
| 59 | 黄珞 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=59 | 官网科室树唯一详情 ID |
| 141 | 李传洁 | 唯一 ID 保留 | 越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=141 | 官网科室树唯一详情 ID |
| 143 | 曹威 | 唯一 ID 保留 | 荔湾院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=143 | 官网科室树唯一详情 ID |
| 289 | 陈伟鸿 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=289 | 官网科室树唯一详情 ID |
| 69 | 梁倩 | 唯一 ID 保留 | 荔湾院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=69 | 官网科室树唯一详情 ID |
| 86 | 李阳 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=86 | 官网科室树唯一详情 ID |
| 103 | 朱德星 | 唯一 ID 保留 | 荔湾院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=103 | 官网科室树唯一详情 ID |
| 288 | 周子亮 | 唯一 ID 保留 | 荔湾院区综合急诊科 | https://www.gykqyy.com/list.html?category=55&id=288 | 官网科室树唯一详情 ID |
| 65 | 陈浩 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=65 | 官网科室树唯一详情 ID |
| 73 | 孙千月 | 唯一 ID 保留 | 荔湾院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=73 | 官网科室树唯一详情 ID |
| 88 | 李慧 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=88 | 官网科室树唯一详情 ID |
| 104 | 叶兰峰 | 唯一 ID 保留 | 荔湾院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=104 | 官网科室树唯一详情 ID |
| 129 | 曾妃菲 | 唯一 ID 保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=129 | 官网科室树唯一详情 ID |
| 251 | 杨凯 | 唯一 ID 保留 | 荔湾院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=251 | 官网科室树唯一详情 ID |
| 64 | 陈伦秋 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=64 | 官网科室树唯一详情 ID |
| 90 | 赵健 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=90 | 官网科室树唯一详情 ID |
| 108 | 姜新娣 | 唯一 ID 保留 | 荔湾院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=108 | 官网科室树唯一详情 ID |
| 58 | 刘耀然 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=58 | 官网科室树唯一详情 ID |
| 77 | 杨双 | 唯一 ID 保留 | 荔湾院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=77 | 官网科室树唯一详情 ID |
| 107 | 乔聪聪 | 唯一 ID 保留 | 荔湾院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=107 | 官网科室树唯一详情 ID |
| 134 | 查骏 | 唯一 ID 保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=134 | 官网科室树唯一详情 ID |
| 261 | 王记位 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=261 | 官网科室树唯一详情 ID |
| 105 | 唐樱花 | 唯一 ID 保留 | 荔湾院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=105 | 官网科室树唯一详情 ID |
| 132 | 李小宇 | 唯一 ID 保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=132 | 官网科室树唯一详情 ID |
| 186 | 李源静 | 唯一 ID 保留 | 荔湾院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=186 | 官网科室树唯一详情 ID |
| 203 | 李平 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=203 | 官网科室树唯一详情 ID |
| 242 | 张翠翠 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=242 | 官网科室树唯一详情 ID |
| 57 | 潘国凯 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=57 | 官网科室树唯一详情 ID |
| 92 | 黄雨婷 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=92 | 官网科室树唯一详情 ID |
| 200 | 赵爽 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=200 | 官网科室树唯一详情 ID |
| 37 | 李唐萍 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=37 | 官网科室树唯一详情 ID |
| 61 | 李智聪 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=61 | 官网科室树唯一详情 ID |
| 84 | 涂欣冉 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=84 | 官网科室树唯一详情 ID |
| 102 | 陈吉荣 | 唯一 ID 保留 | 荔湾院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=102 | 官网科室树唯一详情 ID |
| 155 | 谢灵芝 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=155 | 官网科室树唯一详情 ID |
| 202 | 陈志英 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=202 | 官网科室树唯一详情 ID |
| 216 | 魏珍 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=216 | 官网科室树唯一详情 ID |
| 223 | 陈勰 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=223 | 官网科室树唯一详情 ID |
| 244 | 聂敏 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=244 | 官网科室树唯一详情 ID |
| 247 | 安银哲 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=247 | 官网科室树唯一详情 ID |
| 277 | 陈斌 | 唯一 ID 保留 | 越秀院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=277 | 官网科室树唯一详情 ID |
| 312 | 谢俊明 | 唯一 ID 保留 | 综合医技科 | https://www.gykqyy.com/list.html?category=55&id=312 | 官网科室树唯一详情 ID |
| 39 | 郑蒲珏 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=39 | 官网科室树唯一详情 ID |
| 162 | 高旭广 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=162 | 官网科室树唯一详情 ID |
| 175 | 胡涌昕 | 唯一 ID 保留 | 综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=175 | 官网科室树唯一详情 ID |
| 183 | 吴瑛 | 唯一 ID 保留 | 综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=183 | 官网科室树唯一详情 ID |
| 185 | 唐智群 | 唯一 ID 保留 | 越秀院区口腔黏膜病科、综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=185 | 官网科室树唯一详情 ID |
| 187 | 晏挺林 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=187 | 官网科室树唯一详情 ID |
| 206 | 王涛 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=206 | 官网科室树唯一详情 ID |
| 220 | 李英华 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=220 | 官网科室树唯一详情 ID |
| 225 | 丁世俊 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=225 | 官网科室树唯一详情 ID |
| 243 | 唐春玲 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=243 | 官网科室树唯一详情 ID |
| 264 | 陈瑾 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=264 | 官网科室树唯一详情 ID |
| 273 | 苏汉福 | 唯一 ID 保留 | 越秀院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=273 | 官网科室树唯一详情 ID |
| 307 | 方颖 | 同名不同 ID 分行保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=307 | 同名待甄别 |
| 176 | 易根正 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=176 | 官网科室树唯一详情 ID |
| 194 | 杨晓彬 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=194 | 官网科室树唯一详情 ID |
| 204 | 罗有成 | 唯一 ID 保留 | 综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=204 | 官网科室树唯一详情 ID |
| 263 | 化珍 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=263 | 官网科室树唯一详情 ID |
| 265 | 袁韵仪 | 唯一 ID 保留 | 正畸与儿童口腔中心 | https://www.gykqyy.com/list.html?category=55&id=265 | 官网科室树唯一详情 ID |
| 278 | 魏永祥 | 唯一 ID 保留 | 越秀院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=278 | 官网科室树唯一详情 ID |
| 286 | 陈希立 | 唯一 ID 保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=286 | 官网科室树唯一详情 ID |
| 293 | 何露 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=293 | 官网科室树唯一详情 ID |
| 309 | 邓宇杰 | 唯一 ID 保留 | 麻醉手术中心 | https://www.gykqyy.com/list.html?category=55&id=309 | 官网科室树唯一详情 ID |
| 310 | 李明 | 唯一 ID 保留 | 麻醉手术中心 | https://www.gykqyy.com/list.html?category=55&id=310 | 官网科室树唯一详情 ID |
| 311 | 陈璐 | 唯一 ID 保留 | 病理科 | https://www.gykqyy.com/list.html?category=55&id=311 | 官网科室树唯一详情 ID |
| 314 | 马化森 | 唯一 ID 保留 | 放射科 | https://www.gykqyy.com/list.html?category=55&id=314 | 官网科室树唯一详情 ID |
| 315 | 李修元 | 唯一 ID 保留 | 放射科 | https://www.gykqyy.com/list.html?category=55&id=315 | 官网科室树唯一详情 ID |
| 316 | 杨淑华 | 唯一 ID 保留 | 麻醉手术中心 | https://www.gykqyy.com/list.html?category=55&id=316 | 官网科室树唯一详情 ID |
| 318 | 冯源 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=318 | 官网科室树唯一详情 ID |
| 319 | 程皓宇 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=319 | 官网科室树唯一详情 ID |
| 320 | 刘珍艳 | 唯一 ID 保留 | 麻醉手术中心 | https://www.gykqyy.com/list.html?category=55&id=320 | 官网科室树唯一详情 ID |
| 321 | 邱秋劲 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=321 | 官网科室树唯一详情 ID |
| 322 | 齐佳 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=322 | 官网科室树唯一详情 ID |
| 323 | 赵稚宁 | 同名不同 ID 分行保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=323 | 同名待甄别 |
| 324 | 朱冠雄 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=324 | 官网科室树唯一详情 ID |
| 325 | 蔡东萍 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=325 | 官网科室树唯一详情 ID |
| 326 | 闫春阳 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=326 | 官网科室树唯一详情 ID |
| 327 | 胡诗琳 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=327 | 官网科室树唯一详情 ID |
| 329 | 刘辉 | 唯一 ID 保留 | 麻醉手术中心 | https://www.gykqyy.com/list.html?category=55&id=329 | 官网科室树唯一详情 ID |
| 6 | 陈俊 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=6 | 官网科室树唯一详情 ID |
| 7 | 张海兵 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=7 | 官网科室树唯一详情 ID |
| 8 | 吴圣轩 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=8 | 官网科室树唯一详情 ID |
| 9 | 毛捷 | 唯一 ID 保留 | 正畸与儿童口腔中心 | https://www.gykqyy.com/list.html?category=55&id=9 | 官网科室树唯一详情 ID |
| 10 | 李五一 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=10 | 官网科室树唯一详情 ID |
| 11 | 王乐诗 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=11 | 官网科室树唯一详情 ID |
| 12 | 郑伟龙 | 唯一 ID 保留 | 正畸与儿童口腔中心 | https://www.gykqyy.com/list.html?category=55&id=12 | 官网科室树唯一详情 ID |
| 13 | 谭仲娟 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=13 | 官网科室树唯一详情 ID |
| 14 | 任文 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=14 | 官网科室树唯一详情 ID |
| 15 | 李雪洋 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=15 | 官网科室树唯一详情 ID |
| 16 | 周肖龙 | 唯一 ID 保留 | 正畸与儿童口腔中心 | https://www.gykqyy.com/list.html?category=55&id=16 | 官网科室树唯一详情 ID |
| 21 | 王思然 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=21 | 官网科室树唯一详情 ID |
| 22 | 刘佳玥 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=22 | 官网科室树唯一详情 ID |
| 23 | 林晓敏 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=23 | 官网科室树唯一详情 ID |
| 24 | 郝梦淅 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=24 | 官网科室树唯一详情 ID |
| 25 | 程哲贤 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=25 | 官网科室树唯一详情 ID |
| 26 | 孙思超 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=26 | 官网科室树唯一详情 ID |
| 27 | 李美文 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=27 | 官网科室树唯一详情 ID |
| 29 | 赵稚宁 | 同名不同 ID 分行保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=29 | 同名待甄别 |
| 30 | 曾丽婷 | 唯一 ID 保留 | 口腔预防科 | https://www.gykqyy.com/list.html?category=55&id=30 | 官网科室树唯一详情 ID |
| 34 | 张雨慧 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=34 | 官网科室树唯一详情 ID |
| 36 | 李益玲 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=36 | 官网科室树唯一详情 ID |
| 38 | 马明 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=38 | 官网科室树唯一详情 ID |
| 40 | 黄文燕 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=40 | 官网科室树唯一详情 ID |
| 41 | 封琼 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=41 | 官网科室树唯一详情 ID |
| 42 | 王云杰 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=42 | 官网科室树唯一详情 ID |
| 43 | 朱阳 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=43 | 官网科室树唯一详情 ID |
| 44 | 赵雪丹 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=44 | 官网科室树唯一详情 ID |
| 45 | 李州 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=45 | 官网科室树唯一详情 ID |
| 46 | 李琳娟 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=46 | 官网科室树唯一详情 ID |
| 48 | 营颖 | 唯一 ID 保留 | 正畸与儿童口腔中心 | https://www.gykqyy.com/list.html?category=55&id=48 | 官网科室树唯一详情 ID |
| 49 | 高诗祺 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=49 | 官网科室树唯一详情 ID |
| 50 | 黄宇航 | 唯一 ID 保留 | 荔湾院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=50 | 官网科室树唯一详情 ID |
| 54 | 韩国旭 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=54 | 官网科室树唯一详情 ID |
| 56 | 闫璟 | 唯一 ID 保留 | 综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=56 | 官网科室树唯一详情 ID |
| 60 | 韩志琪 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=60 | 官网科室树唯一详情 ID |
| 62 | 朱川东 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=62 | 官网科室树唯一详情 ID |
| 63 | 赵天宇 | 唯一 ID 保留 | 荔湾院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=63 | 官网科室树唯一详情 ID |
| 67 | 葛逸飞 | 唯一 ID 保留 | 荔湾院区口腔黏膜病科 | https://www.gykqyy.com/list.html?category=55&id=67 | 官网科室树唯一详情 ID |
| 68 | 刘韦佳 | 唯一 ID 保留 | 荔湾院区口腔黏膜病科 | https://www.gykqyy.com/list.html?category=55&id=68 | 官网科室树唯一详情 ID |
| 71 | 赵丽丹 | 唯一 ID 保留 | 荔湾院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=71 | 官网科室树唯一详情 ID |
| 75 | 李倩倩 | 唯一 ID 保留 | 荔湾院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=75 | 官网科室树唯一详情 ID |
| 76 | 苗辛超 | 唯一 ID 保留 | 荔湾院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=76 | 官网科室树唯一详情 ID |
| 78 | 黄超仪 | 唯一 ID 保留 | 荔湾院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=78 | 官网科室树唯一详情 ID |
| 85 | 刘泽妮 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=85 | 官网科室树唯一详情 ID |
| 91 | 向鹏飞 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=91 | 官网科室树唯一详情 ID |
| 93 | 周子伊 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=93 | 官网科室树唯一详情 ID |
| 94 | 李宁 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=94 | 官网科室树唯一详情 ID |
| 95 | 陈璇 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=95 | 官网科室树唯一详情 ID |
| 96 | 张玉静 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=96 | 官网科室树唯一详情 ID |
| 97 | 张晓萌 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=97 | 官网科室树唯一详情 ID |
| 100 | 董惠贤 | 唯一 ID 保留 | 荔湾院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=100 | 官网科室树唯一详情 ID |
| 109 | 周灏雯 | 唯一 ID 保留 | 荔湾院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=109 | 官网科室树唯一详情 ID |
| 113 | 张先跃 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=113 | 官网科室树唯一详情 ID |
| 114 | 王硕 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=114 | 官网科室树唯一详情 ID |
| 115 | 童晓洁 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=115 | 官网科室树唯一详情 ID |
| 119 | 张兵 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=119 | 官网科室树唯一详情 ID |
| 120 | 王瑜 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=120 | 官网科室树唯一详情 ID |
| 121 | 曹宇鸣 | 唯一 ID 保留 | 正畸与儿童口腔中心 | https://www.gykqyy.com/list.html?category=55&id=121 | 官网科室树唯一详情 ID |
| 122 | 陈宝仪 | 唯一 ID 保留 | 荔湾院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=122 | 官网科室树唯一详情 ID |
| 130 | 葛青 | 唯一 ID 保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=130 | 官网科室树唯一详情 ID |
| 133 | 陈韵欣 | 唯一 ID 保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=133 | 官网科室树唯一详情 ID |
| 135 | 黄茵茵 | 唯一 ID 保留 | 荔湾院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=135 | 官网科室树唯一详情 ID |
| 142 | 张颖 | 唯一 ID 保留 | 荔湾院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=142 | 官网科室树唯一详情 ID |
| 144 | 朱明静 | 唯一 ID 保留 | 越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=144 | 官网科室树唯一详情 ID |
| 145 | 钟文超 | 唯一 ID 保留 | 越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=145 | 官网科室树唯一详情 ID |
| 146 | 黎星阳 | 唯一 ID 保留 | 越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=146 | 官网科室树唯一详情 ID |
| 147 | 吴安桐 | 唯一 ID 保留 | 越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=147 | 官网科室树唯一详情 ID |
| 148 | 刘振龙 | 唯一 ID 保留 | 荔湾院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=148 | 官网科室树唯一详情 ID |
| 151 | 袁珊珊 | 唯一 ID 保留 | 越秀院区颞下颌关节科 | https://www.gykqyy.com/list.html?category=55&id=151 | 官网科室树唯一详情 ID |
| 153 | 周凤 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=153 | 官网科室树唯一详情 ID |
| 154 | 徐晓雅 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=154 | 官网科室树唯一详情 ID |
| 156 | 彭博 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=156 | 官网科室树唯一详情 ID |
| 158 | 杨晶晶 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=158 | 官网科室树唯一详情 ID |
| 159 | 闫娈 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=159 | 官网科室树唯一详情 ID |
| 160 | 徐明雪 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=160 | 官网科室树唯一详情 ID |
| 161 | 米会会 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=161 | 官网科室树唯一详情 ID |
| 163 | 陈依静 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=163 | 官网科室树唯一详情 ID |
| 164 | 曾鉴鸿 | 唯一 ID 保留 | 正畸与儿童口腔中心 | https://www.gykqyy.com/list.html?category=55&id=164 | 官网科室树唯一详情 ID |
| 165 | 向茜 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=165 | 官网科室树唯一详情 ID |
| 166 | 孟斯 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=166 | 官网科室树唯一详情 ID |
| 167 | 郭艺佳 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=167 | 官网科室树唯一详情 ID |
| 168 | 蔡雪培 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=168 | 官网科室树唯一详情 ID |
| 169 | 李云阳 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=169 | 官网科室树唯一详情 ID |
| 170 | 李键文 | 唯一 ID 保留 | 越秀院区儿童口腔科 | https://www.gykqyy.com/list.html?category=55&id=170 | 官网科室树唯一详情 ID |
| 173 | 王慧菁 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=173 | 官网科室树唯一详情 ID |
| 174 | 廖婷 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=174 | 官网科室树唯一详情 ID |
| 177 | 朱素文 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=177 | 官网科室树唯一详情 ID |
| 178 | 岳海琼 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=178 | 官网科室树唯一详情 ID |
| 179 | 刘于冬 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=179 | 官网科室树唯一详情 ID |
| 180 | 魏志斌 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=180 | 官网科室树唯一详情 ID |
| 181 | 谭国忠 | 唯一 ID 保留 | 越秀院区口腔颌面外科 | https://www.gykqyy.com/list.html?category=55&id=181 | 官网科室树唯一详情 ID |
| 184 | 王一舟 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=184 | 官网科室树唯一详情 ID |
| 188 | 欧晶晶 | 唯一 ID 保留 | 综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=188 | 官网科室树唯一详情 ID |
| 189 | 陈冠影 | 唯一 ID 保留 | 越秀院区口腔黏膜病科、综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=189 | 官网科室树唯一详情 ID |
| 190 | 刘元 | 唯一 ID 保留 | 越秀院区口腔黏膜病科 | https://www.gykqyy.com/list.html?category=55&id=190 | 官网科室树唯一详情 ID |
| 191 | 吴志聪 | 唯一 ID 保留 | 越秀院区口腔黏膜病科 | https://www.gykqyy.com/list.html?category=55&id=191 | 官网科室树唯一详情 ID |
| 192 | 刘晓 | 唯一 ID 保留 | 综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=192 | 官网科室树唯一详情 ID |
| 193 | 何晓茜 | 唯一 ID 保留 | 越秀院区口腔黏膜病科 | https://www.gykqyy.com/list.html?category=55&id=193 | 官网科室树唯一详情 ID |
| 199 | 钟梅 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=199 | 官网科室树唯一详情 ID |
| 201 | 冯玉环 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=201 | 官网科室树唯一详情 ID |
| 205 | 曹婷婷 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=205 | 官网科室树唯一详情 ID |
| 207 | 陈佳敏 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=207 | 官网科室树唯一详情 ID |
| 208 | 刘芳岐 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=208 | 官网科室树唯一详情 ID |
| 209 | 石安迪 | 唯一 ID 保留 | 越秀院区口腔修复科 | https://www.gykqyy.com/list.html?category=55&id=209 | 官网科室树唯一详情 ID |
| 214 | 杨会肖 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=214 | 官网科室树唯一详情 ID |
| 215 | 吴青松 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=215 | 官网科室树唯一详情 ID |
| 217 | 王蕾 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=217 | 官网科室树唯一详情 ID |
| 218 | 祁文婷 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=218 | 官网科室树唯一详情 ID |
| 219 | 刘鹏程 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=219 | 官网科室树唯一详情 ID |
| 221 | 李晓星 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=221 | 官网科室树唯一详情 ID |
| 222 | 何颖 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=222 | 官网科室树唯一详情 ID |
| 224 | 蔡冬萍 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=224 | 官网科室树唯一详情 ID |
| 226 | 王兴羽 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=226 | 官网科室树唯一详情 ID |
| 227 | 赵虹灵 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=227 | 官网科室树唯一详情 ID |
| 228 | 夏娟 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=228 | 官网科室树唯一详情 ID |
| 229 | 马彦冉 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=229 | 官网科室树唯一详情 ID |
| 230 | 马朝阳 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=230 | 官网科室树唯一详情 ID |
| 231 | 李文芝 | 唯一 ID 保留 | 综合二科（老年口腔科） | https://www.gykqyy.com/list.html?category=55&id=231 | 官网科室树唯一详情 ID |
| 232 | 潘宇倩 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=232 | 官网科室树唯一详情 ID |
| 233 | 江烨 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=233 | 官网科室树唯一详情 ID |
| 234 | 钟婷 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=234 | 官网科室树唯一详情 ID |
| 236 | 万民婷 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=236 | 官网科室树唯一详情 ID |
| 237 | 黄文绵 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=237 | 官网科室树唯一详情 ID |
| 238 | 黄丽珊 | 唯一 ID 保留 | 越秀院区牙体牙髓科 | https://www.gykqyy.com/list.html?category=55&id=238 | 官网科室树唯一详情 ID |
| 246 | 陈楠楠 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=246 | 官网科室树唯一详情 ID |
| 248 | 廖倬逸 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=248 | 官网科室树唯一详情 ID |
| 249 | 魏修群 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=249 | 官网科室树唯一详情 ID |
| 250 | 宫海环 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=250 | 官网科室树唯一详情 ID |
| 252 | 王晓宇 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=252 | 官网科室树唯一详情 ID |
| 253 | 姜珊 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=253 | 官网科室树唯一详情 ID |
| 254 | 陈朕 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=254 | 官网科室树唯一详情 ID |
| 255 | 樊晓淼 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=255 | 官网科室树唯一详情 ID |
| 257 | 罗春媛 | 唯一 ID 保留 | 越秀院区牙周病科 | https://www.gykqyy.com/list.html?category=55&id=257 | 官网科室树唯一详情 ID |
| 260 | 钟雯 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=260 | 官网科室树唯一详情 ID |
| 262 | 林炳鹏 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=262 | 官网科室树唯一详情 ID |
| 267 | 彭菁 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=267 | 官网科室树唯一详情 ID |
| 268 | 罗明 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=268 | 官网科室树唯一详情 ID |
| 269 | 郭陈琳 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=269 | 官网科室树唯一详情 ID |
| 270 | 胡耀政 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=270 | 官网科室树唯一详情 ID |
| 271 | 张琰 | 唯一 ID 保留 | 越秀院区口腔正畸科 | https://www.gykqyy.com/list.html?category=55&id=271 | 官网科室树唯一详情 ID |
| 275 | 刘蓉 | 唯一 ID 保留 | 越秀院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=275 | 官网科室树唯一详情 ID |
| 276 | 陈馥淳 | 唯一 ID 保留 | 越秀院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=276 | 官网科室树唯一详情 ID |
| 282 | 孙浩波 | 唯一 ID 保留 | 全科口腔中心 | https://www.gykqyy.com/list.html?category=55&id=282 | 官网科室树唯一详情 ID |
| 283 | 季若桐 | 唯一 ID 保留 | 越秀院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=283 | 官网科室树唯一详情 ID |
| 284 | 罗嘉欣 | 唯一 ID 保留 | 越秀院区口腔种植科 | https://www.gykqyy.com/list.html?category=55&id=284 | 官网科室树唯一详情 ID |
| 290 | 王俊妹 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=290 | 官网科室树唯一详情 ID |
| 291 | 杨艳艳 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=291 | 官网科室树唯一详情 ID |
| 292 | 黄佳欣 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=292 | 官网科室树唯一详情 ID |
| 294 | 荣容 | 唯一 ID 保留 | 荔湾院区综合急诊科 | https://www.gykqyy.com/list.html?category=55&id=294 | 官网科室树唯一详情 ID |
| 295 | 李京 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=295 | 官网科室树唯一详情 ID |
| 296 | 邓鑫 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=296 | 官网科室树唯一详情 ID |
| 297 | 陈莎 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=297 | 官网科室树唯一详情 ID |
| 298 | 刘钢 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=298 | 官网科室树唯一详情 ID |
| 299 | 曾骏 | 唯一 ID 保留 | 便民口腔诊疗中心 | https://www.gykqyy.com/list.html?category=55&id=299 | 官网科室树唯一详情 ID |
| 303 | 王任钦 | 唯一 ID 保留 | 克山门诊部 | https://www.gykqyy.com/list.html?category=55&id=303 | 官网科室树唯一详情 ID |
| 304 | 欧阳珊 | 唯一 ID 保留 | 克山门诊部 | https://www.gykqyy.com/list.html?category=55&id=304 | 官网科室树唯一详情 ID |
| 305 | 梁志英 | 唯一 ID 保留 | 克山门诊部 | https://www.gykqyy.com/list.html?category=55&id=305 | 官网科室树唯一详情 ID |

## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| https://www.gykqyy.com/list.html?category=55 |  | https://www.gykqyy.com/list.html?category=55&id=328 | 焦点推荐记录未出现在科室医生树中且姓名为空，排除 |

## 输出文件

- Excel 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.xlsx`
- CSV 底表：`D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院_医生画像自动采集总底表.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 1 |
| 原始医生卡片记录 | 317 |
| 跨入口去重前候选关系 | 317 |
| 跨入口去重后唯一候选 | 297 |
| 排除非医生候选 | 1 |
| 唯一医生详情页 | 297 |
| 覆盖科室数 | 46 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 12 |
| 慢性病 | 2 |
| 术后恢复/康复 | 10 |
| 疑难重症 | 85 |
| 肿瘤 | 25 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 越秀院区牙体牙髓科 | 29 |
| 越秀院区儿童口腔科 | 18 |
| 荔湾院区牙体牙髓科 | 17 |
| 荔湾院区儿童口腔科 | 17 |
| 越秀院区牙周病科 | 15 |
| 荔湾院区口腔颌面外科 | 14 |
| 全科口腔中心 | 14 |
| 越秀院区口腔修复科 | 13 |
| 越秀院区口腔正畸科 | 12 |
| 口腔预防科 | 12 |
| 荔湾院区口腔正畸科 | 11 |
| 越秀院区口腔颌面外科 | 11 |
| 荔湾院区口腔种植科 | 10 |
| 便民口腔诊疗中心 | 10 |
| 荔湾院区口腔修复科 | 9 |
| 荔湾院区牙周病科 | 9 |
| 正畸与儿童口腔中心 | 8 |
| 越秀院区颞下颌关节科 | 8 |
| 麻醉手术中心 | 7 |
| 越秀院区口腔种植科 | 7 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 同名待甄别 | 4 |
| 职称/身份需人工复核 | 29 |
| 详情正文为空或未识别 | 11 |

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
