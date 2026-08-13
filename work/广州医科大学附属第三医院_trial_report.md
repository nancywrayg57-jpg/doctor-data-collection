---
类型: 自动采集试跑报告
医院: 广州医科大学附属第三医院
城市: 广州市
采集日期: 2026-08-13
来源范围: 医院官网
采集入口: https://www.gy3y.cn/ks/team.html
适配器: gy3y_static_team_directory
---

# 广州医科大学附属第三医院 官方医生自动采集试跑报告

## 结论

本次试采只读取医院官网公开专家列表页和医生详情页。系统没有使用第三方平台、没有绕过登录或验证码、没有采集私人联系方式或患者信息。

本轮生成医生自动采集试采底表，共 10 位唯一医生；官网列表页原始卡片记录 580 条；读取入口分类 104 个；覆盖 10 个科室；详情页失败 0 条。

## 台账来源

| 项目 | 内容 |
|---|---|
| 城市 | 广州市 |
| 医院 | 广州医科大学附属第三医院 |
| 官网首页 | https://www.gy3y.cn/index |
| 本轮医生入口 | https://www.gy3y.cn/ks/team.html |
| 入口来源 | GitHub Issue #27（入口台账主表与 owner 人工复核裁决一致） |
| 原台账医生入口 | https://www.gy3y.cn/ks/team.html |
| 台账人工复核 | 确认可采集 |
| 采集难度初判 | A-优先自动采集 |

## 入口普查表

| 分类 | 官方入口 | 页面性质 | 列表分页 | 授权详情关系 | 唯一授权详情 | 范围外详情 | 归属医院/中心 | 独立实体核验 |
|---|---|---|---:|---:|---:|---:|---|---|
| 荔湾院区 | https://www.gy3y.cn/ks/team.html | 静态全院区医生总目录 | 1 | 390 | 370 | 需逐详情核验 | 广州医科大学附属第三医院 | owner 已裁决两院区均属同一法人；官网同域静态目录 |
| 黄埔院区 | https://www.gy3y.cn/ks/team.html | 静态全院区医生总目录 | 1 | 190 | 185 | 需逐详情核验 | 广州医科大学附属第三医院 | owner 已裁决两院区均属同一法人；官网同域静态目录 |

### 动态目录专项证据

- 医生分页/载入方式：单个 team.html 一次性列出两院区全部科室关系，无下一页或加载更多
- 医生目录公开接口：不适用
- 医生详情公开接口：不适用
- 接口出处证据：不适用
- 院区/分组：2 个；科室分类：104 个
- 医生-科室关系：580 条
- 唯一详情 ID：438 个
- 有姓名详情 ID：10 个
- 空姓名详情 ID：0 个
- 去重后的非空姓名值：10 个
- 同名不同详情 ID：0 组
- 非空/空科室块：99 / 5
- 两院区关系：荔湾院区 390 条；黄埔院区 190 条
- 跨院区详情 ID：117 个

| 同名 | 详情 ID |
|---|---|
| 无 | 无 |

## 跨入口去重与试采覆盖

- 各入口唯一医生详情 URL 关系数：580
- 跨入口去重后唯一候选：438
- 跨入口重复关系：142
- 试采覆盖入口分类：10 个（荔湾院区内科门诊、荔湾院区内镜中心、荔湾院区呼吸与危重症医学科、荔湾院区心血管内科、荔湾院区神经内科、荔湾院区精神医学科、荔湾院区肾内科、黄埔院区心血管内科、黄埔院区神经内科、黄埔院区超声医学科）

| 重复医生 | 唯一详情 URL | 出现入口 |
|---|---|---|
| 李文杰 | https://www.gy3y.cn/ks/nkxt/xxgnk/doctor_6.html | 荔湾院区心血管内科；黄埔院区心血管内科 |
| 蔡玉宇 | https://www.gy3y.cn/ks/nkxt/xxgnk/doctor_9.html | 荔湾院区心血管内科；黄埔院区心血管内科 |
| 梁燕玲 | https://www.gy3y.cn/ks/nkxt/sjnk/doctor_11.html | 荔湾院区神经内科；黄埔院区神经内科 |
| 刘子凡 | https://www.gy3y.cn/ks/nkxt/sjnk/doctor_13.html | 荔湾院区神经内科；黄埔院区神经内科 |
| 刘宇明 | https://www.gy3y.cn/ks/nkxt/sjnk/doctor_16.html | 荔湾院区神经内科；黄埔院区神经内科 |
| 喻延 | https://www.gy3y.cn/ks/nkxt/hxnk/doctor_20.html | 荔湾院区呼吸与危重症医学科；荔湾院区内科门诊 |
| 梁贤球 | https://www.gy3y.cn/ks/nkxt/hxnk/doctor_22.html | 荔湾院区呼吸与危重症医学科；荔湾院区内科门诊 |
| 黄越前 | https://www.gy3y.cn/ks/nkxt/xhnk/doctor_28.html | 荔湾院区消化内科；黄埔院区消化内科 |
| 张建瑜 | https://www.gy3y.cn/ks/nkxt/fsmyk/doctor_32.html | 荔湾院区风湿免疫科；黄埔院区风湿免疫科 |
| 张莹 | https://www.gy3y.cn/ks/nkxt/nfmk/doctor_33.html | 荔湾院区内分泌代谢科；黄埔院区内分泌代谢科 |
| 林榕 | https://www.gy3y.cn/ks/nkxt/nfmk/doctor_36.html | 荔湾院区内分泌代谢科；黄埔院区内分泌代谢科 |
| 陈慧 | https://www.gy3y.cn/ks/nkxt/nfmk/doctor_37.html | 荔湾院区内分泌代谢科；黄埔院区内分泌代谢科 |
| 乔安意 | https://www.gy3y.cn/ks/wkxt/pwyq/doctor_53.html | 荔湾院区普外一区（肝胆外科）；黄埔院区肝胆外科 |
| 杨波 | https://www.gy3y.cn/ks/wkxt/gkyq/doctor_66.html | 荔湾院区脊柱外科；黄埔院区骨科 |
| 潘永谦 | https://www.gy3y.cn/ks/mjz/tjzx/doctor_68.html | 荔湾院区健康管理中心；黄埔院区健康管理中心 |
| 范震波 | https://www.gy3y.cn/ks/wkxt/csgk/doctor_77.html | 荔湾院区创伤骨科；黄埔院区骨科 |
| 李育斌 | https://www.gy3y.cn/ks/wkxt/mnwk/doctor_94.html | 荔湾院区泌尿外科；黄埔院区泌尿外科 |
| 李映桃 | https://www.gy3y.cn/ks/fckyjs/fys/doctor_111.html | 荔湾院区广州妇产科研究所；荔湾院区产 科（广州重症孕产妇救治中心）；黄埔院区产科 |
| 生秀杰 | https://www.gy3y.cn/ks/fckyjs/fys/doctor_113.html | 荔湾院区广州妇产科研究所；荔湾院区妇 科；荔湾院区妇科肿瘤病区 |
| 李维枢 | https://www.gy3y.cn/ks/fckyjs/fk/doctor_115.html | 荔湾院区妇 科；黄埔院区妇科 |
| 谭鹰 | https://www.gy3y.cn/ks/fckyjs/fk/doctor_117.html | 荔湾院区妇 科；荔湾院区妇科肿瘤病区 |
| 黄凯清 | https://www.gy3y.cn/ks/fckyjs/fk/doctor_118.html | 荔湾院区妇 科；黄埔院区妇科 |
| 刘明星 | https://www.gy3y.cn/ks/fckyjs/fckmz/doctor_121.html | 荔湾院区妇产科门诊；黄埔院区妇科 |
| 杨洁 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_137.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 黄青 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_138.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 许海燕 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_139.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 李斯晨 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_142.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 陈敦金 | https://www.gy3y.cn/ks/fckyjs/fys/doctor_143.html | 荔湾院区广州妇产科研究所；荔湾院区产 科（广州重症孕产妇救治中心）；荔湾院区产前诊断科（胎儿医学中心）；黄埔院区产科 |
| 陈敏 | https://www.gy3y.cn/ks/fckyjs/fys/doctor_144.html | 荔湾院区广州妇产科研究所；荔湾院区产前诊断科（胎儿医学中心）；黄埔院区胎儿医学与产前诊断科 |
| 李志华 | https://www.gy3y.cn/ks/fckyjs/cqzdk/doctor_145.html | 荔湾院区产前诊断科（胎儿医学中心）；黄埔院区胎儿医学与产前诊断科 |
| 刘娟 | https://www.gy3y.cn/ks/fckyjs/fk/doctor_147.html | 荔湾院区妇 科；荔湾院区盆底诊治中心；黄埔院区妇科 |
| 崔其亮 | https://www.gy3y.cn/ks/ek/ek1/doctor_148.html | 荔湾院区儿 科（普通儿科、新生儿科）；黄埔院区新生儿科 |
| 陈耀勇 | https://www.gy3y.cn/ks/ek/ek1/doctor_149.html | 荔湾院区儿 科（普通儿科、新生儿科）；黄埔院区儿科 |
| 张慧 | https://www.gy3y.cn/ks/ek/ek1/doctor_150.html | 荔湾院区儿 科（普通儿科、新生儿科）；黄埔院区儿童保健科；黄埔院区新生儿科 |
| 秦媛怡 | https://www.gy3y.cn/ks/mjz/tjzx/doctor_188.html | 荔湾院区健康管理中心；黄埔院区健康管理中心 |
| 蔡名金 | https://www.gy3y.cn/ks/yjbm/fsk/doctor_189.html | 荔湾院区放射科；荔湾院区介入放射；黄埔院区介入放射 |
| 梁伟翔 | https://www.gy3y.cn/ks/yjbm/csyx/doctor_192.html | 荔湾院区超声医学科；黄埔院区超声医学科 |
| 谢亦农 | https://www.gy3y.cn/ks/fckyjs/cqzdk/doctor_193.html | 荔湾院区产前诊断科（胎儿医学中心）；黄埔院区胎儿医学与产前诊断科 |
| 王伟群 | https://www.gy3y.cn/ks/yjbm/csyx/doctor_194.html | 荔湾院区超声医学科；黄埔院区超声医学科 |
| 夏勇 | https://www.gy3y.cn/ks/yjbm/jyk/doctor_196.html | 荔湾院区检验科；黄埔院区医学检验科 |
| 宋亭 | https://www.gy3y.cn/ks/yjbm/fsk/doctor_203.html | 荔湾院区放射科；黄埔院区医学影像科/放射科 |
| 张家云 | https://www.gy3y.cn/ks/yjbm/fsk/doctor_208.html | 荔湾院区放射科；黄埔院区医学影像科/放射科 |
| 王寿平 | https://www.gy3y.cn/ks/wkxt/mzk/doctor_210.html | 荔湾院区麻醉科；黄埔院区麻醉科 |
| 孙筱放 | https://www.gy3y.cn/ks/fckyjs/fys/doctor_211.html | 荔湾院区广州妇产科研究所；荔湾院区广东省产科重大疾病重点实验室 |
| 谭小华 | https://www.gy3y.cn/ks/ek/ek1/doctor_214.html | 荔湾院区儿 科（普通儿科、新生儿科）；黄埔院区新生儿科 |
| 余琳 | https://www.gy3y.cn/ks/fckyjs/ck/doctor_215.html | 荔湾院区产 科（广州重症孕产妇救治中心）；黄埔院区产科 |
| 刘玉冰 | https://www.gy3y.cn/ks/fckyjs/ck/doctor_217.html | 荔湾院区产 科（广州重症孕产妇救治中心）；黄埔院区产科 |
| 石宇 | https://www.gy3y.cn/ks/fckyjs/fckmz/doctor_221.html | 荔湾院区妇产科门诊；黄埔院区妇科 |
| 张文 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_222.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 贺芳 | https://www.gy3y.cn/ks/fckyjs/fys/doctor_223.html | 荔湾院区广州妇产科研究所；荔湾院区产 科（广州重症孕产妇救治中心）；黄埔院区产科 |
| 张费通 | https://www.gy3y.cn/ks/ek/ek1/doctor_229.html | 荔湾院区儿 科（普通儿科、新生儿科）；黄埔院区儿科 |
| 吴繁 | https://www.gy3y.cn/ks/ek/ek1/doctor_230.html | 荔湾院区儿 科（普通儿科、新生儿科）；黄埔院区新生儿科 |
| 钟柳英 | https://www.gy3y.cn/ks/fckyjs/ck/doctor_233.html | 荔湾院区产 科（广州重症孕产妇救治中心）；黄埔院区产科 |
| 孙嫣 | https://www.gy3y.cn/ks/nkxt/xhnk/doctor_234.html | 荔湾院区消化内科；黄埔院区消化内科；黄埔院区内镜中心 |
| 陈兢思 | https://www.gy3y.cn/ks/fckyjs/cqzdk/doctor_235.html | 荔湾院区产前诊断科（胎儿医学中心）；黄埔院区胎儿医学与产前诊断科 |
| 陈友权 | https://www.gy3y.cn/ks/nkxt/xxgnk/doctor_236.html | 荔湾院区心血管内科；黄埔院区心血管内科 |
| 岑东芝 | https://www.gy3y.cn/ks/nkxt/pwszlk/doctor_238.html | 荔湾院区肿瘤科；荔湾院区核医学科、放射治疗科 |
| 李莉 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_244.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 陈德雄 | https://www.gy3y.cn/ks/mjz/qk/doctor_248.html | 荔湾院区全科医学科；黄埔院区全科医学科 |
| 潘兴飞 | https://www.gy3y.cn/ks/nkxt/grjbk/doctor_249.html | 荔湾院区感染疾病科；黄埔院区感染疾病科 |
| 燕翼 | https://www.gy3y.cn/ks/nkxt/xxgnk/doctor_251.html | 荔湾院区心血管内科；黄埔院区心血管内科 |
| 麦凤鸣 | https://www.gy3y.cn/ks/fckyjs/ck/doctor_252.html | 荔湾院区产 科（广州重症孕产妇救治中心）；荔湾院区妇产科门诊；黄埔院区产科 |
| 黄蓓 | https://www.gy3y.cn/ks/fckyjs/fckmz/doctor_255.html | 荔湾院区妇产科门诊；黄埔院区产科 |
| 王簕 | https://www.gy3y.cn/ks/wkxt/gkyq/doctor_257.html | 荔湾院区脊柱外科；荔湾院区再生医学与3D打印技术转化研究中心 |
| 刘先保 | https://www.gy3y.cn/ks/wkxt/mzk/doctor_258.html | 荔湾院区麻醉科；黄埔院区麻醉科 |
| 罗超元 | https://www.gy3y.cn/ks/wkxt/wcwk/doctor_261.html | 荔湾院区普外二区（胃肠外科）；黄埔院区胃肠外科 |
| 谭岱峰 | https://www.gy3y.cn/ks/ek/ek1/doctor_263.html | 荔湾院区儿 科（普通儿科、新生儿科）；黄埔院区新生儿科 |
| 江庆萍 | https://www.gy3y.cn/ks/yjbm/blk/doctor_264.html | 荔湾院区病理科；黄埔院区病理科 |
| 熊汉真 | https://www.gy3y.cn/ks/yjbm/blk/doctor_266.html | 荔湾院区病理科；黄埔院区病理科 |
| 彭娟 | https://www.gy3y.cn/ks/yjbm/blk/doctor_267.html | 荔湾院区病理科；黄埔院区病理科 |
| 付熙 | https://www.gy3y.cn/ks/fckyjs/fk/doctor_276.html | 荔湾院区妇 科；黄埔院区妇科 |
| 张弛 | https://www.gy3y.cn/ks/wkxt/gkeq/doctor_279.html | 荔湾院区关节外科；荔湾院区再生医学与3D打印技术转化研究中心 |
| 洪宏海 | https://www.gy3y.cn/ks/yjbm/jyk/doctor_281.html | 荔湾院区检验科；黄埔院区医学检验科 |
| 陈静 | https://www.gy3y.cn/ks/wgk/yk/doctor_282.html | 荔湾院区眼 科；黄埔院区眼科 |
| 王琨 | https://www.gy3y.cn/ks/yjbm/csyx/doctor_284.html | 荔湾院区超声医学科；黄埔院区超声医学科 |
| 黄健威 | https://www.gy3y.cn/ks/yjbm/fsk/doctor_285.html | 荔湾院区放射科；黄埔院区医学影像科/放射科 |
| 曾毅 | https://www.gy3y.cn/ks/fckyjs/ck/doctor_287.html | 荔湾院区产 科（广州重症孕产妇救治中心）；黄埔院区产科 |
| 王世祥 | https://www.gy3y.cn/ks/nkxt/xxgnk/doctor_288.html | 荔湾院区心血管内科；黄埔院区心血管内科 |
| 刘盛华 | https://www.gy3y.cn/ks/wkxt/xxwk/doctor_291.html | 荔湾院区心胸外科；黄埔院区心胸外科 |
| 李南 | https://www.gy3y.cn/ks/fckyjs/cqzdk/doctor_293.html | 荔湾院区产前诊断科（胎儿医学中心）；黄埔院区胎儿医学与产前诊断科 |
| 黄敏 | https://www.gy3y.cn/ks/mjz/tjzx/doctor_301.html | 荔湾院区健康管理中心；黄埔院区健康管理中心 |
| 王双勇 | https://www.gy3y.cn/ks/wgk/yk/doctor_303.html | 荔湾院区眼 科；黄埔院区眼科 |
| 闻毅颐 | https://www.gy3y.cn/ks/wgk/yk/doctor_311.html | 荔湾院区眼 科；黄埔院区眼科 |
| 赵忠芳 | https://www.gy3y.cn/ks/wkxt/zxmrk/doctor_312.html | 荔湾院区整形美容科；黄埔院区医疗美容科 |
| 吴乙璇 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_313.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 潘玲兰 | https://www.gy3y.cn/ks/fckyjs/fk/doctor_316.html | 荔湾院区妇 科；黄埔院区产科 |
| 陈永铃 | https://www.gy3y.cn/ks/wgk/yk/doctor_317.html | 荔湾院区眼 科；黄埔院区眼科 |
| 刘海英 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_318.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 王慧慧 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_319.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 林琼燕 | https://www.gy3y.cn/ks/fckyjs/fk/doctor_323.html | 荔湾院区妇 科；荔湾院区盆底诊治中心；黄埔院区妇科 |
| 张刚 | https://www.gy3y.cn/ks/ek/xewk/doctor_324.html | 荔湾院区小儿外科；黄埔院区小儿外科 |
| 林育辉 | https://www.gy3y.cn/ks/nkxt/xxgnk/doctor_334.html | 荔湾院区心血管内科；黄埔院区心血管内科 |
| 曾利芳 | https://www.gy3y.cn/ks/nkxt/xhnk/doctor_336.html | 荔湾院区消化内科；黄埔院区消化内科；黄埔院区内镜中心 |
| 邵明 | https://www.gy3y.cn/ks/wkxt/csgk/doctor_337.html | 荔湾院区创伤骨科；黄埔院区骨科 |
| 何泓 | https://www.gy3y.cn/ks/fckyjs/fk/doctor_340.html | 荔湾院区妇 科；荔湾院区妇科肿瘤病区 |
| 陆志锋 | https://www.gy3y.cn/ks/nkxt/xxgnk/doctor_346.html | 荔湾院区心血管内科；黄埔院区心血管内科 |
| 李舜 | https://www.gy3y.cn/ks/wkxt/ttk/doctor_348.html | 荔湾院区疼痛科；黄埔院区疼痛科 |
| 何雨 | https://www.gy3y.cn/ks/yjbm/csyx/doctor_349.html | 荔湾院区超声医学科；黄埔院区超声医学科 |
| 李任远 | https://www.gy3y.cn/ks/nkxt/nfmk/doctor_350.html | 荔湾院区内分泌代谢科；黄埔院区内分泌代谢科 |
| 张莉 | https://www.gy3y.cn/ks/nkxt/xhnk/doctor_354.html | 荔湾院区消化内科；黄埔院区消化内科；黄埔院区内镜中心 |
| 应瑛 | https://www.gy3y.cn/ks/fckyjs/szyxk/doctor_358.html | 荔湾院区生殖医学科（生殖医学中心）；黄埔院区生殖医学中心 |
| 郭奇桑 | https://www.gy3y.cn/ks/fckyjs/fk/doctor_359.html | 荔湾院区妇 科；黄埔院区妇科 |
| 周军 | https://www.gy3y.cn/ks/wkxt/wcwk/doctor_401.html | 荔湾院区普外二区（胃肠外科）；黄埔院区普通外科 |
| 高元妹 | https://www.gy3y.cn/ks/nkxt/hxnk/doctor_422.html | 荔湾院区呼吸与危重症医学科；黄埔院区呼吸与危重症医学科 |
| 刘佳 | https://www.gy3y.cn/ks/mjz/lcyyk/doctor_426.html | 荔湾院区临床营养科；黄埔院区临床营养科 |
| 李林艳 | https://www.gy3y.cn/ks/mjz/lcyyk/doctor_427.html | 荔湾院区临床营养科；黄埔院区临床营养科 |
| 徐学虎 | https://www.gy3y.cn/ks/wkxt/wcwk/doctor_437.html | 荔湾院区普外二区（胃肠外科）；荔湾院区普外二区（乳腺外科）；黄埔院区普通外科 |
| 唐毅 | https://www.gy3y.cn/ks/wkxt/rxwk/doctor_438.html | 荔湾院区普外二区（乳腺外科）；黄埔院区乳腺外科 |
| 徐鋆耀 | https://www.gy3y.cn/ks/wkxt/pwyq/doctor_444.html | 荔湾院区普外一区（肝胆外科）；黄埔院区普通外科；黄埔院区肝胆外科 |
| 熊中堂 | https://www.gy3y.cn/ks/yjbm/blk/doctor_445.html | 荔湾院区病理科；黄埔院区病理科 |
| 王娜 | https://www.gy3y.cn/ks/yjbm/blk/doctor_446.html | 荔湾院区病理科；黄埔院区病理科 |
| 李磊 | https://www.gy3y.cn/ks/yjbm/jyk/doctor_449.html | 荔湾院区检验科；黄埔院区医学检验科 |
| 陈戎 | https://www.gy3y.cn/ks/wkxt/wcwk/doctor_452.html | 荔湾院区普外二区（胃肠外科）；黄埔院区普通外科 |
| 刘树基 | https://www.gy3y.cn/ks/mjz/qk/doctor_463.html | 荔湾院区全科医学科；黄埔院区全科医学科 |
| 张文华 | https://www.gy3y.cn/ks/wkxt/mzk/doctor_469.html | 荔湾院区麻醉科；黄埔院区麻醉科 |
| 杨展翔 | https://www.gy3y.cn/ks/wkxt/csgk/doctor_478.html | 荔湾院区创伤骨科；黄埔院区骨科 |
| 郭元 | https://www.gy3y.cn/ks/mjz/tjzx/doctor_487.html | 荔湾院区健康管理中心；黄埔院区健康管理中心 |
| 饶芳 | https://www.gy3y.cn/ks/mjz/tjzx/doctor_488.html | 荔湾院区健康管理中心；黄埔院区健康管理中心 |
| 杨宁 | https://www.gy3y.cn/ks/mjz/tjzx/doctor_489.html | 荔湾院区健康管理中心；黄埔院区健康管理中心 |
| 冯智毅 | https://www.gy3y.cn/ks/mjz/tjzx/doctor_490.html | 荔湾院区健康管理中心；黄埔院区健康管理中心 |
| 林 琳 | https://www.gy3y.cn/ks/mjz/tjzx/doctor_491.html | 荔湾院区健康管理中心；黄埔院区健康管理中心 |
| 谭娜娜 | https://www.gy3y.cn/ks/mjz/tjzx/doctor_492.html | 荔湾院区健康管理中心；黄埔院区健康管理中心 |
| 崔鹏 | https://www.gy3y.cn/ks/wkxt/pwyq/doctor_494.html | 荔湾院区普外一区（肝胆外科）；黄埔院区肝胆外科 |
| 曾青山 | https://www.gy3y.cn/ks/mjz/lcyyk/doctor_502.html | 荔湾院区临床营养科；黄埔院区临床营养科 |
| 王晓彤 | https://www.gy3y.cn/ks/mjz/lcyyk/doctor_503.html | 荔湾院区临床营养科；黄埔院区临床营养科 |
| 罗唯师 | https://www.gy3y.cn/ks/wkxt/sjwk/doctor_621.html | 荔湾院区神经外科；黄埔院区神经外科 |

## 广医三院两院区详情身份对账

- 静态目录详情 ID：438
- 本轮已读取详情 ID：10
- 多院区/多科室详情 ID：126
- 跨院区详情 ID：117
- 护理身份核验：静态总目录只展示姓名，不展示职称身份；TRIAL 仅核验 10 位详情，其中纯护理身份排除 0 位

| 姓名 | 详情 ID | 裁决 | 详情关系 | 合并院区科室 | 主详情 | 其余详情 |
|---|---|---|---:|---|---|---|
| 无 | 无 | 无 | 0 | 无 | 无 | 无 |

## 已排除或范围外候选

| 入口 | 列表身份 | 来源链接 | 排除原因 |
|---|---|---|---|
| 无 | 无 | 无 | 无 |

## 输出文件

- Excel 底表：未生成（本轮使用 --no-xlsx）
- CSV 底表：`D:\workspace\信息收集整理\work\广州医科大学附属第三医院_trial_doctors.csv`

## 采集统计

| 指标 | 数量 |
|---|---:|
| 读取列表文档数 | 104 |
| 原始医生卡片记录 | 580 |
| 跨入口去重前候选关系 | 580 |
| 跨入口去重后唯一候选 | 438 |
| 排除非医生候选 | 0 |
| 合规医生详情页 | 438 |
| 最终医生身份 | 10 |
| 覆盖科室数 | 10 |
| 列表页失败数 | 0 |
| 详情页失败数 | 0 |
| 已建画像匹配数 | 0 |

## 重点关注范围统计

| 范围 | 医生数 |
|---|---:|
| 免疫/风湿/感染 | 2 |
| 慢性病 | 3 |
| 疑难重症 | 7 |
| 肿瘤 | 1 |

## 科室数量 Top 20

| 科室 | 医生数 |
|---|---:|
| 荔湾院区心血管内科 | 2 |
| 荔湾院区神经内科 | 2 |
| 黄埔院区超声医学科 | 1 |
| 黄埔院区心血管内科 | 1 |
| 荔湾院区内科门诊 | 1 |
| 黄埔院区神经内科 | 1 |
| 荔湾院区精神医学科 | 1 |
| 荔湾院区呼吸与危重症医学科 | 1 |
| 荔湾院区肾内科 | 1 |
| 荔湾院区内镜中心 | 1 |

## 异常与复核提示

| 提示 | 数量 |
|---|---:|
| 无 | 0 |

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
