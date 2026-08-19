# Issue #77 广州医科大学附属脑科医院照片补录 TRIAL 报告

## 门禁与范围

- Phase：`TRIAL_READY_FOR_OWNER_AUDIT`（视觉状态：`PASSED_SINGLE_ADULT_PROFESSIONAL_PORTRAITS_10_OF_10`）。
- 医院官网：https://www.gzbrain.cn/
- 医生目录：https://www.gzbrain.cn/myzj/list.html
- 固定范围：183 行 / 183 个唯一 `myzj/info_itemid_<N>.html`；TRIAL 前照片两列非空 0。
- 样本：10 人、10 个不同科室首原子；职称分层 {"正高": 4, "副高": 3, "中级": 2, "其他": 1}。
- TRIAL 只写 `work/` 工件；入口台账、总底表三载体、报告、184 个本院 Markdown 和正式照片目录前后快照一致：True。

## 访问与照片容器结构诊断

- 请求实现：`urllib-default-get/no-cookie/no-proxy/no-custom-headers`；Cookie 0；代理禁用；未添加浏览器型请求头、Referer 或第三方来源。
- 首页、目录和 10 个详情页均为 HTTP 200；状态闪烁 0，详情失败 0。
- 严格容器：`.single_con > .single_cn > .single-img > img[src]`。10/10 页面在 `.single_con` 的直接子 `.single_cn` 下仅有一个直接子 `.single-img`，其中恰有一个直接 `img[src]`；该 URL 是唯一可下载候选。
- URL 门禁：同站 HTTPS；路径严格为 `/uploadfiles/YYYY/MM/<文件>.<jpg|jpeg|png|gif|webp>`；保留页面实际引用的不透明查询串；禁止构造、去查询串、猜测或探测其他路径。
- 10 个页面照片引用唯一数 10；页面外部图片引用只作排除诊断，不下载。页面未引用路径探测 0；排除资源下载 0；第三方来源 0。

代表性容器 HTML（宁玉萍；其余逐页片段在 manifest/payload）：

```html
<div class="single-img"> <img alt="" src="/uploadfiles/2019/06/20190610095458209.png?5a6B546J6JCNLnBuZw=="/> </div>
```

## 自拟排除清单与患者红线

- 公共图标：严格照片容器之外的 header/menu/action 图标一律排除
- 装饰图片：banner、医院环境、新闻/科普卡片及任何非 single-img 资源一律排除
- 二维码：路径或语义命中 qrcode/qr_code/erweima/weixin/wechat 时排除
- 占位图：路径命中 placeholder/nopic/noimage/default 时定格为占位图，不下载
- 院徽/Logo：路径命中 logo、favicon、gongan 或位于页眉区域时排除
- 患者及合影：即使位于候选容器，联系表目视发现患者、儿童、合影或非本人职业照也必须排除

- 判定依据：结构白名单先于路径白名单；即使路径形似图片，只要不在严格医生照片容器内即排除。
- 专科医院患者红线：自动结构门禁不能替代实图判断，必须以 10 图联系表逐图排除患者、儿童、合影或其他可识别患者信息。
- 视觉结论：10/10 均已目视确认为医生本人单人职业照；未见患者、儿童、合影、二维码、公共装饰或占位图。

## 成功结果

- 详情成功 10/10；照片成功 10/10；无照片容器、占位图、照片资源不可达均为 0。
- 页面引用原始字节直接落盘，不压缩、不转码；按魔数命名。声明扩展名与魔数不一致 1（成友军页面 URL/Content-Type 声明 JPEG，但原始魔数为 PNG，因此文件按 `.png` 命名）。
- 总字节 2,225,954；最小 21,126；中位数 84,408；平均 222,595；最大 954,574。
- 大小分桶：{"<200KiB": 7, "200KiB-1MiB": 3, "1-5MiB": 0, "5-20MiB": 0, ">20MiB": 0}；>5 MiB 0；>20 MiB 0。
- 按样本平均值线性估算 183 行约 38.85 MiB，仅作容量估算，不代表 FULL 成功率。

- 宁玉萍｜神经内科｜主任医师（正高）｜86,227 bytes｜197×266｜`png`｜`8324542d39f1d4890c4b9ec1ff3f91efdc43acb03271bc7046410d2b04f28bb7`
- 成友军｜神经外科｜副主任医师（副高）｜79,908 bytes｜201×320｜`png`｜`a10a649dae3e0852774d53b8111b30259582aab7cd28ee509788eba9478f7525`
- 周素妙｜中西医结合科｜主治医师（中级）｜82,589 bytes｜969×1264｜`jpg`｜`2f46ddc9a40de1729299a44cb928c108a5572762bc5070be393f882c3c39e586`
- 张双春｜临床心理科｜心理治疗师（其他）｜533,853 bytes｜1507×1573｜`jpg`｜`41a23de684a5f474fbf5489b39597985030a273b5fb821441f9f3f47db9bca8a`
- 周亮｜社区精神科｜教授（正高）｜21,126 bytes｜302×403｜`jpg`｜`63b8c2d2b1f747859604c631e319fbc64102c3d89840a232c3eb960b8c0c34d0`
- 彭妙官｜内分泌科｜副主任医师（副高）｜954,574 bytes｜6000×7500｜`jpg`｜`80929a070621228295f0a59d2fcd6d8f6e6d938336545ac4c431d4153ae50e80`
- 王治华｜司法鉴定科｜主治医师（中级）｜98,392 bytes｜598×882｜`jpg`｜`ac7c6efbc721081135536142ec8550187dcf68462d040fc40f5703137d51415b`
- 郭耀光｜康复科｜副主任医师（副高）｜44,227 bytes｜413×626｜`jpg`｜`d8f3edf932b08f13a5e931ca8a38b72599fba85a009d9ce035c260bd7cc0c8cd`
- 张继辉｜睡眠与节律医学中心｜研究员（正高）｜41,734 bytes｜451×566｜`jpg`｜`c80bd4a06ad0d7fc624e06584704df4d16a4415eb8b5761ae5a6a37e342da0fe`
- 韩为｜中医科｜主任中医师（正高）｜283,324 bytes｜600×900｜`jpg`｜`5ee970aacf8f33c828cc89840500e6733a584fa2e395ac818adc42fb4c1849ee`

## Owner 大图终审清单（>5 MiB）

- 无

## 工件与停止点

- Payload：`work/广州医科大学附属脑科医院_photo_backfill_trial_payload.json`
- Manifest：`work/广州医科大学附属脑科医院_photo_backfill_trial_manifest.csv`
- 联系表：`work/广州医科大学附属脑科医院_photo_backfill_trial_contact_sheet.jpg`
- 原图目录：`work/广州医科大学附属脑科医院_photo_backfill_trial_photos`（10 张）
- 当前停止点：`TRIAL_READY_FOR_OWNER_AUDIT`。未取得 Owner 明确 `FULL_APPEND_AND_OBSIDIAN` 前，不得修改正式资产。
