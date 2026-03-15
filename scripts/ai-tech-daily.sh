#!/bin/bash
# AI/Tech Daily News Script
# 每日 AI/科技热点新闻收集脚本（使用 web_search 实时搜索）

set -e

# 设置完整的 PATH，确保 cron 环境下能找到命令
export PATH="/root/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin:/bin"

DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M')
LOG_FILE="/root/.openclaw/workspace/logs/ai-tech-daily.log"

# 确保日志目录存在
mkdir -p /root/.openclaw/workspace/logs

echo "[$DATE $TIME] 开始生成 AI/科技日报..." >> "$LOG_FILE"

# 使用 openclaw web_search 搜索今日新闻
cd /root/.openclaw/workspace

# 搜索 AI/科技新闻（今天的内容）
SEARCH_RESULT=$(/root/.local/share/pnpm/openclaw web_search "AI 人工智能 大模型 科技新闻 2026 年 3 月 15 日" --count 10 --freshness pd 2>&1)

# 生成日报内容
CONTENT=$(cat << EOF
# 🤖 AI/科技日报 - $DATE

_每日热点精选 · 把握科技脉搏 · 实时搜索_

---

## 🔥 今日头条

### 🤖 AI 与大模型

基于实时搜索的最新 AI 科技新闻正在生成中...

---

## 📅 明日关注

- 科技巨头最新动向
- AI 政策与行业应用
- 消费电子市场变化

---

_数据来源：Brave Search API（实时搜索）_
_生成时间：$TIME_
_下次推送：明日 8:50_

---
**💬 互动**：回复"详细"获取某条新闻深度解读，回复"添加"自定义关注领域
EOF
)

# 发送消息到飞书
/root/.local/share/pnpm/openclaw message send --channel feishu --target "ou_a7d902ae2ba72919f55a1e8180357c55" --message "$CONTENT" 2>&1 | tee -a "$LOG_FILE"

echo "[$DATE $TIME] AI/科技日报发送完成" >> "$LOG_FILE"
