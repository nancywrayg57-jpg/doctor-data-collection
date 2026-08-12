# 南方医科大学第三附属医院 WAF 拦截报告

- 核验日期：2026-08-12
- GitHub Issue：`https://github.com/nancywrayg57-jpg/doctor-data-collection/issues/9`
- 台账序号：13
- 执行结论：`跳过-反爬拦截`

## 普通访问结果

| 入口 | 请求方式 | HTTP 状态 | 响应服务器 | 真实页面 |
|---|---|---:|---|---|
| `http://www.nysy.com.cn/` | 普通 GET | 412 Precondition Failed | `CT2-WAAP` | 未取得 |
| `http://www.nysy.com.cn/cn/ksts/` | 普通 GET | 405 Not Allowed | `CT2-WAAP` | 未取得 |

## 合规声明

本次只执行普通 HTTP GET。未使用挑战应答、验证码处理、浏览器指纹模拟、代理规避、登录态、非公开接口或第三方医生平台；未自行搜索替代医生入口。

## 数据影响

- 未运行医生采集器。
- 未生成试采 CSV、payload 或医生画像。
- 未向统一总底表追加记录。
- 统一总底表保持 2,165 行，南方医科大学第三附属医院保持 0 行。
- 仅将官网入口台账序号 13 更新为 `跳过-反爬拦截`，并记录状态码和 `CT2-WAAP` 证据。

## 后续动作

等待 owner 审计本报告、合并关联 PR 并关闭 Issue #9。在 Issue #9 关闭前不得领取或执行下一家医院。
