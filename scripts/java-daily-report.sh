#!/bin/bash
# Java 学习日报 - 每日推送 5 道 Java 面试题
# 每天早上 9:30 和晚上 23:00 推送
# 题库来源：小林 coding - 5 大模块（Java 基础/集合/并发/JVM/Spring）

set -e

# 设置完整的 PATH，确保 cron 环境下能找到 node 等命令
export PATH="/root/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin:/bin"

DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M')
LOG_FILE="/root/.openclaw/workspace/logs/java-daily-report.log"
TARGET_USER="ou_a7d902ae2ba72919f55a1e8180357c55"
QUESTIONS_FILE="/root/.openclaw/workspace/memory/java-interview-questions-merged.json"

# 确保日志目录存在
mkdir -p /root/.openclaw/workspace/logs

echo "[$DATE $TIME] 开始生成 Java 学习日报..." >> "$LOG_FILE"

# 使用 Python 从 JSON 题库中随机选择 5 道题目
SELECTED_QUESTIONS=$(python3 << PYTHON_SCRIPT
import json
import random

# 读取题库
with open('$QUESTIONS_FILE', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']
total = len(questions)

# 随机选择 5 道不重复的题目
if total >= 5:
    selected = random.sample(questions, 5)
else:
    selected = questions

# 输出为 bash 可读的格式：category|question|answer|url
for q in selected:
    print(f"{q['category']}|{q['question']}|{q['answer']}|{q['url']}")
PYTHON_SCRIPT
)

# 构建消息内容
MESSAGE="📚 *Java 学习日报* - $DATE

今日精选 5 道面试题（5 大模块）：

"

COUNT=1
while IFS='|' read -r CATEGORY QUESTION ANSWER URL; do
    MESSAGE+="${COUNT}. *【${CATEGORY}】${QUESTION}*
   💡 ${ANSWER}
   🔗 <${URL}|查看详细解析>

"
    COUNT=$((COUNT + 1))
done <<< "$SELECTED_QUESTIONS"

MESSAGE+="
---
💪 坚持每天学习，大厂 offer 等着你！
来源：小林 coding 面试题汇总
模块：Java 基础 | Java 集合 | Java 并发 | JVM | Spring"

# 发送消息到飞书
cd /root/.openclaw/workspace
/root/.local/share/pnpm/openclaw message send --channel feishu --target "$TARGET_USER" --message "$MESSAGE" 2>&1 | tee -a "$LOG_FILE"

echo "[$DATE $TIME] Java 学习日报发送完成" >> "$LOG_FILE"
