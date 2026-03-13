#!/bin/bash
# Java 学习日报 - 每日推送 5 道 Java 面试题（飞书富文本卡片格式）
# 每天早上 9:30 和晚上 23:00 推送
# 题库来源：小林 coding - 5 大模块（Java 基础/集合/并发/JVM/Spring）

set -e

# 设置完整的 PATH，确保 cron 环境下能找到 node 等命令
export PATH="/root/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin:/bin"

DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M')
LOG_FILE="/root/.openclaw/workspace/logs/java-daily-report.log"
TARGET_USER="ou_a7d902ae2ba72919f55a1e8180357c55"
QUESTIONS_FILE="/root/.openclaw/workspace/memory/java-interview-questions-detailed.json"
SCRIPT_DIR="/root/.openclaw/workspace/scripts"

# 确保日志目录存在
mkdir -p /root/.openclaw/workspace/logs

echo "[$DATE $TIME] 开始生成 Java 学习日报（富文本卡片格式）..." >> "$LOG_FILE"

# 使用 Python 生成富文本卡片内容
CARD_CONTENT=$(python3 << 'PYTHON_SCRIPT'
import json
import random
from datetime import datetime

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-detailed.json"

def load_questions():
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def select_questions(questions, count=5):
    if len(questions) >= count:
        return random.sample(questions, count)
    return questions

def format_answer_for_card(answer):
    """将答案格式化为飞书富文本格式"""
    content = []
    answer_lines = answer.split('\n')
    
    for line in answer_lines:
        line = line.strip()
        if not line:
            continue
        
        # 处理加粗文本 **text**
        if line.startswith('**') and '**' in line[2:]:
            parts = line.split('**')
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 1:  # 加粗部分
                        content.append({"tag": "text", "text": part, "style": ["bold"]})
                    else:
                        content.append({"tag": "text", "text": part})
        # 处理编号列表 1. 2. 3.
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.'):
            content.append({"tag": "text", "text": f"• {line}\n"})
        # 处理项目列表 - 
        elif line.startswith('- '):
            content.append({"tag": "text", "text": f"• {line[2:]}\n"})
        # 处理代码块标记
        elif line.startswith('```'):
            continue
        # 普通文本
        else:
            content.append({"tag": "text", "text": f"{line}\n"})
    
    return content

def create_question_block(index, category, question, answer, url, total):
    """创建单个题目的富文本内容"""
    content = []
    
    # 题目标题和分隔线
    content.append([
        {"tag": "text", "text": "───\n"},
        {"tag": "text", "text": f"{index}️⃣【{category}】", "style": ["bold"]},
    ])
    
    # 问题
    content.append([
        {"tag": "text", "text": f"\nQ: {question}\n", "style": ["bold"]},
    ])
    
    # 答案标题
    content.append([
        {"tag": "text", "text": "✅ 答案：", "style": ["bold"]},
    ])
    
    # 答案内容（格式化为多行文本）
    answer_rows = []
    current_row = []
    
    answer_lines = answer.split('\n')
    for line in answer_lines:
        line = line.strip()
        if not line or line.startswith('```'):
            continue
        
        # 处理加粗
        if '**' in line:
            parts = line.split('**')
            row_parts = []
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 1:
                        row_parts.append({"tag": "text", "text": part, "style": ["bold"]})
                    else:
                        row_parts.append({"tag": "text", "text": part})
            content.append(row_parts)
        # 处理编号
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
            content.append([{"tag": "text", "text": f"• {line}\n"}])
        # 处理项目符号
        elif line.startswith('- '):
            content.append([{"tag": "text", "text": f"• {line[2:]}\n"}])
        # 普通文本
        else:
            content.append([{"tag": "text", "text": f"{line}\n"}])
    
    # 来源链接
    content.append([
        {"tag": "text", "text": "\n📖 "},
        {"tag": "text", "text": "来源：", "style": ["bold"]},
        {"tag": "text", "text": " "},
        {"tag": "a", "href": url, "text": url},
    ])
    
    return content

def create_daily_report(questions):
    """创建完整的日报富文本内容"""
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    
    content = []
    
    # 标题
    content.append([
        {"tag": "text", "text": "📚 "},
        {"tag": "text", "text": f"Java 学习日报 - 第{day_of_year}天", "style": ["bold"]},
        {"tag": "text", "text": f" ({today.strftime('%Y-%m-%d')})"},
    ])
    
    # 副标题
    content.append([
        {"tag": "text", "text": "💡 每天 5 道题，系统掌握 Java 面试核心知识点"},
    ])
    
    # 题目内容
    total = len(questions)
    for i, q in enumerate(questions, 1):
        block = create_question_block(
            index=i,
            category=q['category'],
            question=q['question'],
            answer=q['answer'],
            url=q['url'],
            total=total
        )
        content.extend(block)
    
    # 底部统计
    categories = list(set(q['category'] for q in questions))
    content.append([
        {"tag": "text", "text": "───\n"},
        {"tag": "text", "text": "📊 今日学习统计", "style": ["bold"]},
    ])
    content.append([
        {"tag": "text", "text": f"📝 今日题目：{total}道  |  📖 模块：{', '.join(categories)}"},
    ])
    content.append([
        {"tag": "text", "text": "───\n"},
        {"tag": "text", "text": "💪 坚持每天学习，大厂 offer 等着你！", "style": ["bold"]},
        {"tag": "text", "text": "\n📖 来源：小林 coding 面试题汇总"},
    ])
    
    return content

# 主程序
questions = load_questions()
selected = select_questions(questions, 5)
content = create_daily_report(selected)

result = {
    "title": "",
    "content": content
}

print(json.dumps(result, ensure_ascii=False))
PYTHON_SCRIPT
)

# 使用 openclaw message send 发送富文本消息
# 飞书富文本消息需要通过特定的 API 发送
cd /root/.openclaw/workspace

# 方法 1：尝试使用 openclaw message 发送（如果支持富文本）
# 方法 2：直接使用飞书 API

# 这里我们使用 Python 脚本直接调用飞书 API
python3 << PYTHON_SEND
import json
import requests
import os

# 飞书 API 配置
APP_ID = os.environ.get('FEISHU_APP_ID', 'cli_a591dd18a0c09014')
APP_SECRET = os.environ.get('FEISHU_APP_SECRET', 'Fq8j2M78yQxkQ5bQjGKvWUAI')

# 获取 access_token
def get_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    response = requests.post(url, json=payload)
    result = response.json()
    return result.get('tenant_access_token')

# 发送富文本消息
def send_rich_text_message(access_token, user_id, content):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 富文本消息格式
    payload = {
        "receive_id": user_id,
        "msg_type": "interactive",
        "content": json.dumps({
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": content
                    }
                }
            ]
        })
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# 但更简单的方式是使用 openclaw message 工具
# 因为我们已经在 bash 脚本中，直接调用即可
PYTHON_SEND

# 简化方案：直接使用 openclaw message send，但需要构造正确的富文本格式
# 飞书富文本消息的 content 字段是 JSON 字符串

CONTENT_JSON=$(echo "$CARD_CONTENT" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin)))")

# 发送消息
/root/.local/share/pnpm/openclaw message send \
    --channel feishu \
    --target "$TARGET_USER" \
    --message "$CONTENT_JSON" \
    2>&1 | tee -a "$LOG_FILE"

echo "[$DATE $TIME] Java 学习日报发送完成（富文本卡片格式）" >> "$LOG_FILE"
