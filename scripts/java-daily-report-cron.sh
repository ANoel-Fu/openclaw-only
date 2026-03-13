#!/bin/bash
# Java 学习日报 - Cron 包装脚本
# 用于定时任务调用

# 设置环境变量
export PATH="/root/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin:/bin"
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 脚本目录
SCRIPT_DIR="/root/.openclaw/workspace/scripts"
LOG_FILE="/root/.openclaw/workspace/logs/java-daily-report.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# 记录开始时间
echo "[$DATE] [CRON] 开始执行 Java 学习日报..." >> "$LOG_FILE"

# 执行 Python 脚本
cd "$SCRIPT_DIR"
python3 java-daily-report-v4.py >> "$LOG_FILE" 2>&1

# 记录结束时间
DATE=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$DATE] [CRON] Java 学习日报执行完成" >> "$LOG_FILE"
