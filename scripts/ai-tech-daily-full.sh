#!/bin/bash
# AI/Tech Daily News - Full Automation Script
# 每日 AI/科技热点新闻自动收集并发送

set -e

# 配置
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M')
LOG_FILE="/root/.openclaw/workspace/logs/ai-tech-daily.log"

# 确保日志目录存在
mkdir -p /root/.openclaw/workspace/logs

# 记录开始时间
echo "[$DATE $TIME] 开始生成 AI/科技日报..." >> "$LOG_FILE"

# 使用 OpenClaw sessions_send 发送消息到主会话
# 这会触发 AI 收集新闻并发送给用户
cd /root/.openclaw/workspace

# 调用 OpenClaw 发送消息
# 注意：这需要在 OpenClaw 环境中运行
cat << EOF | /root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.2.26_@napi-rs+canvas@0.1.95_@types+express@5.0.6_hono@4.12.3_node-llama-cpp@3.15.1/node_modules/openclaw/dist/cli.js sessions send --label "ai-tech-daily" --message "请生成今天的 AI/科技日报" 2>&1 | tee -a "$LOG_FILE"
EOF

echo "[$DATE $TIME] AI/科技日报发送完成" >> "$LOG_FILE"
