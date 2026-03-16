#!/bin/bash
# AI/Tech Daily News Script
# 每日 AI/科技热点新闻收集脚本（36Kr 实时抓取）

set -e

# 设置完整的 PATH，确保 cron 环境下能找到命令
export PATH="/root/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin:/bin"

DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M')
LOG_FILE="/root/.openclaw/workspace/logs/ai-tech-daily.log"

# 确保日志目录存在
mkdir -p /root/.openclaw/workspace/logs

echo "[$DATE $TIME] 开始生成 AI/科技日报..." >> "$LOG_FILE"

cd /root/.openclaw/workspace

# 运行 Python 脚本生成并发送日报
python3 scripts/ai-tech-daily-smart.py 2>&1 | tee -a "$LOG_FILE"

echo "[$DATE $TIME] AI/科技日报发送完成" >> "$LOG_FILE"
