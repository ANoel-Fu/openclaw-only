#!/bin/bash

# AI/科技日报 - 定时任务安装脚本

echo "🔧 正在安装 AI/科技日报定时任务..."

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到 Node.js，请先安装"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
cd /root/.openclaw/workspace/scripts/tech-daily-fetch
npm install rss-parser node-fetch --save

# 创建系统 cron 任务
CRON_JOB="0 9 * * * cd /root/.openclaw/workspace/scripts/tech-daily-fetch && node tech-daily-fetch.js --send >> /tmp/tech-daily.log 2>&1"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "tech-daily-fetch.js"; then
    echo "⚠️  定时任务已存在"
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ 定时任务已添加：每天上午 9 点执行"
fi

# 显示当前 cron 配置
echo ""
echo "📋 当前 cron 任务:"
crontab -l | grep "tech-daily"

echo ""
echo "🧪 测试运行:"
echo "   node /root/.openclaw/workspace/scripts/tech-daily-fetch/tech-daily-fetch.js"
echo ""
echo "🚀 手动发送:"
echo "   node /root/.openclaw/workspace/scripts/tech-daily-fetch/tech-daily-fetch.js --send"
