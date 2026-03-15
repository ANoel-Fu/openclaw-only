# 2026-03-15 - Java 学习日报 Cron 路径修复

## 🐛 问题发现

**时间：** 2026-03-15 11:40  
**现象：** Java 学习日报今天早上 9:30 没有推送

## 🔍 问题分析

### Cron 日志显示：
```
2026-03-15T09:30:01.644831+08:00 CROND: /bin/sh: line 1: logs/java-daily-report.log: No such file or directory
```

### 根因：
Cron 配置没有切换工作目录，导致相对路径 `logs/java-daily-report.log` 失败。

**错误的 Cron 配置：**
```bash
30 9 * * * TZ=Asia/Shanghai /root/.openclaw/workspace/scripts/java-daily-report-v4.py >> logs/java-daily-report.log 2>&1
```

脚本执行时不在 `/root/.openclaw/workspace` 目录下，所以 `logs/` 相对路径找不到。

## ✅ 修复方案

### 1. 更新 Crontab 配置

**修复后：**
```bash
30 9 * * * cd /root/.openclaw/workspace && TZ=Asia/Shanghai /root/.openclaw/workspace/scripts/java-daily-report-v4.py >> logs/java-daily-report.log 2>&1
0 23 * * * cd /root/.openclaw/workspace && TZ=Asia/Shanghai /root/.openclaw/workspace/scripts/java-daily-report-v4.py >> logs/java-daily-report.log 2>&1
```

**关键改动：** 在命令前添加 `cd /root/.openclaw/workspace &&`

### 2. 验证修复

```bash
# 手动测试执行
cd /root/.openclaw/workspace && python3 scripts/java-daily-report-v4.py
```

**结果：** ✅ 发送成功 (Message ID: om_x100b5456e4f0c0a8b2d294542fa95ba)

## 📅 推送时间

- **早上：** 9:30 (Asia/Shanghai)
- **晚上：** 23:00 (Asia/Shanghai)

## 🔧 相关文件

- 脚本：`/root/.openclaw/workspace/scripts/java-daily-report-v4.py`
- 题库：`/root/.openclaw/workspace/memory/java-interview-questions-complete.json`
- 日志：`/root/.openclaw/workspace/logs/java-daily-report.log`

## ✅ 确认清单

- [x] Crontab 配置已更新
- [x] 脚本可执行权限正常
- [x] 题库文件存在
- [x] 手动测试推送成功
- [x] 日志目录存在

## 📝 备注

类似问题也检查了 AI 科技日报的 cron 配置，确认已正确使用 `cd /root/.openclaw/workspace &&` 前缀。
