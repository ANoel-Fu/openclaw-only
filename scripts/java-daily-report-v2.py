#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Java 学习日报 - 飞书富文本卡片格式推送
# 使用飞书 API 发送富文本消息

import json
import random
import subprocess
import sys
from datetime import datetime

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-detailed.json"
TARGET_USER = "ou_a7d902ae2ba72919f55a1e8180357c55"

def load_questions():
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def select_questions(questions, count=5):
    """随机选择 count 道不重复的题目"""
    if len(questions) >= count:
        return random.sample(questions, count)
    return questions

def format_answer_lines(answer):
    """将答案格式化为飞书富文本行"""
    lines = []
    answer_lines = answer.split('\n')
    
    for line in answer_lines:
        line = line.strip()
        if not line or line.startswith('```'):
            continue
        
        # 处理加粗 **text**
        if '**' in line:
            parts = line.split('**')
            row = []
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 1:  # 加粗部分
                        row.append({"tag": "text", "text": part, "style": ["bold"]})
                    else:
                        row.append({"tag": "text", "text": part})
            lines.append(row)
        # 处理编号
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
            lines.append([{"tag": "text", "text": f"• {line}\n"}])
        # 处理项目符号
        elif line.startswith('- '):
            lines.append([{"tag": "text", "text": f"• {line[2:]}\n"}])
        # 普通文本
        else:
            lines.append([{"tag": "text", "text": f"{line}\n"}])
    
    return lines

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
        # 分隔线和题目标题
        content.append([
            {"tag": "text", "text": "───\n"},
            {"tag": "text", "text": f"{i}️⃣【{q['category']}】", "style": ["bold"]},
        ])
        
        # 问题
        content.append([
            {"tag": "text", "text": f"\nQ: {q['question']}\n", "style": ["bold"]},
        ])
        
        # 答案标题
        content.append([
            {"tag": "text", "text": "✅ 答案：", "style": ["bold"]},
        ])
        
        # 答案内容
        answer_lines = format_answer_lines(q['answer'])
        content.extend(answer_lines)
        
        # 来源链接
        content.append([
            {"tag": "text", "text": "\n📖 "},
            {"tag": "text", "text": "来源：", "style": ["bold"]},
            {"tag": "text", "text": " "},
            {"tag": "a", "href": q['url'], "text": q['url']},
        ])
    
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

def send_via_openclaw(content):
    """通过 openclaw message 工具发送消息"""
    result = {
        "title": "",
        "content": content
    }
    
    content_json = json.dumps(result, ensure_ascii=False)
    
    # 调用 openclaw message send
    cmd = [
        "/root/.local/share/pnpm/openclaw",
        "message", "send",
        "--channel", "feishu",
        "--target", TARGET_USER,
        "--message", content_json
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

def main():
    # 加载题库
    questions = load_questions()
    
    # 随机选择 5 道题
    selected = select_questions(questions, 5)
    
    # 创建富文本内容
    content = create_daily_report(selected)
    
    # 发送消息
    success = send_via_openclaw(content)
    
    if success:
        print("✅ Java 学习日报发送成功")
        sys.exit(0)
    else:
        print("❌ Java 学习日报发送失败", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
