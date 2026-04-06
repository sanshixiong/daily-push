# 定时推送系统

通过 GitHub Actions 实现每天自动推送邮件。

## 推送时间

| 日报 | 时间 |
|------|------|
| 股市日报 | 每天 19:30 |
| 求职日报 | 每天 08:00 |

## 配置 Secrets

进入 Settings → Secrets → Actions，添加：

- `EMAIL_PASSWORD`: QQ邮箱授权码
- `RECEIVER_EMAIL`: 接收邮箱