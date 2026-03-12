#!/bin/bash
# AI/Tech Daily News Script
# 每日 AI/科技热点新闻收集脚本（带 AI 智能摘要）

set -e

# 设置完整的 PATH，确保 cron 环境下能找到 node、python3 等命令
export PATH="/root/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin:/bin"

DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M')
LOG_FILE="/root/.openclaw/workspace/logs/ai-tech-daily.log"

# 确保日志目录存在
mkdir -p /root/.openclaw/workspace/logs

echo "[$DATE $TIME] 开始生成 AI/科技日报..." >> "$LOG_FILE"

# 生成日报内容
CONTENT=$(python3 /root/.openclaw/workspace/scripts/ai-tech-daily-smart.py)

# 发送消息到飞书
cd /root/.openclaw/workspace
/root/.local/share/pnpm/openclaw message send --channel feishu --target "ou_a7d902ae2ba72919f55a1e8180357c55" --message "$CONTENT" 2>&1 | tee -a "$LOG_FILE"

echo "[$DATE $TIME] AI/科技日报发送完成" >> "$LOG_FILE"
