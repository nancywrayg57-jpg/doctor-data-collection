# 广东省第二中医院照片补录 TRIAL 报告

- GitHub Issue：#73
- 医院官网：https://www.gdzy5413.com/
- 医生目录：https://www.gdzy5413.com/main/famousdoctorinfo.aspx?fid=81&cid=851&pid=850
- 固定范围：342（ksdoctorinfo 321 + specialist 21）
- TRIAL：10 张页面引用原始响应照片；specialist 2 + ksdoctorinfo 8
- 科室首原子：10 个
- 职称分层：{"正高": 4, "其他": 4, "副高": 2}
- 视觉复核：PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10

## 两类详情模板结构诊断

### specialist

- 代表医生：靳利利
- 代表详情：https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=699
- 容器选择器：`.main_left_img .docimg_title + .docimg_ming + .docimg_cover + div[style*='background:url']`
- URL 特征：main_left_img 内 docimg_title 姓名一致，且恰有一个 inline background:url(/UploadFiles/image/<file>)
- 现场 HTML 片段：

```html
<div class="docimg_title">靳利利</div> <div class="docimg_ming" val="心血管科主任、主任中医师、教授、医学博士、硕士研究生导师"> </div> <div class="docimg_cover"></div> <div style=" overflow:hidden; width:340px; background:url(/UploadFiles/image/2014-2/20140214052754190.jpg) no-repeat center; height:369px;"></div>
```

### ksdoctorinfo

- 代表医生：孙正平
- 代表详情：https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=488
- 容器选择器：`资料卡 div[style*='width: 120px'] > img[width='120px'][height='155px']`
- URL 特征：资料卡姓名字段一致，且恰有一个 120px×155px img 指向 /UploadFiles/image/<file>
- 现场 HTML 片段：

```html
<div style="float: left; width: 120px;"> <img border="5px" style="border-color: Black;" src="/UploadFiles/image/2014-3/20140305102314685_s.jpg" width="120px" height="155px" /> </div>
```

## 排除清单

- `template-style-assets`：path contains /style/images/；模板 logo、边框、按钮、排班图或装饰图，不在医生照片容器内。
- `public-navigation-footer-assets`：known 就诊指南/专家目录/页脚/二维码 asset identifiers；全站公共资源，不是医生本人职业照。
- `empty-upload-path`：path is /UploadFiles/image/ without filename；详情页明确没有照片文件，禁止构造或猜测文件名。
- `placeholder-name-markers`：default/placeholder/nopic/noimage variants；占位图命名特征，不作为本人职业照。
- `placeholder-response-content`：known placeholder SHA-256 or <=4 KiB small 120×160-class response；拦截 URL 文件名伪装为医生照片、实际内容为‘暂无图片’的小型合法 JPEG。
- `outside-doctor-container`：image/background reference is outside the authorized template container；仅采页面本人照片容器实际引用版本，其他页面资源全部排除。

## 样本对账

| # | 模板 | 姓名 | 科室首原子 | 主职称 | 页面 | 照片 | 字节 | 尺寸 |
|---:|---|---|---|---|---|---|---:|---:|
| 1 | specialist | 靳利利 | 心血管科 | 主任中医师 | [详情](https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=699) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/2014-2/20140214052754190.jpg) | 52,324 | 342×369 |
| 2 | specialist | 范德辉 | 针灸康复科五区 | 主任中医师 | [详情](https://www.gdzy5413.com/main/doctor/specialist.aspx?typeid=1452) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/2014-4/20140410101222463.jpg) | 52,289 | 342×369 |
| 3 | ksdoctorinfo | 孙正平 | 治未病(健康体检)中心 | 主治中医师 | [详情](https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=104&typeid=102&cid=104&ksid=102&id=488) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/2014-3/20140305102314685_s.jpg) | 72,684 | 178×160 |
| 4 | ksdoctorinfo | 周永霞 | 儿科 | 主任医师 | [详情](https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=72&typeid=70&cid=72&ksid=70&id=109) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/upload/633821470657860797.jpg) | 12,269 | 86×126 |
| 5 | ksdoctorinfo | 陈伟萍 | 医技科 | 副主任医师 | [详情](https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=929&typeid=134&cid=929&ksid=134&id=444) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/2014-3/20140301102516894_s.jpg) | 11,443 | 75×100 |
| 6 | ksdoctorinfo | 宫静 | 呼吸与危重症医学科 | 副主任中医师 | [详情](https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=31&typeid=29&cid=31&ksid=29&id=657) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/2017-2/20170215031752407_s.jpg) | 164,184 | 248×365 |
| 7 | ksdoctorinfo | 林谋清 | 外一科 | 主治中医师 | [详情](https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=47&typeid=45&cid=47&ksid=45&id=417) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/2014-2/20140228033357452_s.jpg) | 27,977 | 150×100 |
| 8 | ksdoctorinfo | 何宇巍 | 检验科 | 主管技师 | [详情](https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=926&typeid=131&cid=926&ksid=131&id=767) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/2023-3/20230327102839830_s.jpg) | 12,991 | 71×100 |
| 9 | ksdoctorinfo | 付啸峰 | 肿瘤科 | 医师 | [详情](https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=37&typeid=35&cid=37&ksid=35&id=452) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/2014-3/20140302120454663_s.jpg) | 27,701 | 123×160 |
| 10 | ksdoctorinfo | 唐敏 | 眼科 | 主任医师 | [详情](https://www.gdzy5413.com/main/ks/templet2/ksdoctorinfo.aspx?bid=1139&typeid=1137&cid=1139&ksid=1137&id=314) | [页面引用版本](https://www.gdzy5413.com/UploadFiles/image/2025-10/20251014024358559_s.png) | 13,999 | 100×100 |

## 字节与验证

- 总字节：447,861
- 最小/中位数/平均/最大：11,443 / 27,839 / 44,786 / 164,184
- 大小分桶：{"<200KiB": 10, "200KiB-1MiB": 0, "1-5MiB": 0, "5-20MiB": 0, ">20MiB": 0}
- 实际魔数格式：{"jpg": 3, "png": 7}；响应头/魔数格式不一致 6 张，落盘扩展名均跟随实际魔数。
- 详情页：10/10 HTTP 200；照片：10/10 HTTP 200。
- 每张照片均验证最终 host、HTTP、Content-Type、魔数、SHA-256 与可解码尺寸；原始响应字节未压缩、未转码。
- 页面未引用路径构造/探测：0；第三方来源：0；登录/验证码/WAF 绕过：0。常规浏览器 UA 属 Issue #73 明确允许的正常官网请求。

## 正式资产保护

- TRIAL 前后快照一致：True。
- 本院画像树：343 文件；正式照片目录存在：False。
- 本轮仅写 work/ TRIAL 工件；总底表三载体、入口台账三载体、更新报告、342 份画像和 _索引.md 均未修改。

## 工件

- `work/广东省第二中医院_photo_backfill_trial_payload.json`
- `work/广东省第二中医院_photo_backfill_trial_manifest.csv`
- `work/广东省第二中医院_photo_backfill_trial_report.md`
- `work/广东省第二中医院_photo_backfill_trial_contact_sheet.jpg`
- `work/广东省第二中医院_photo_backfill_trial_photos/`
