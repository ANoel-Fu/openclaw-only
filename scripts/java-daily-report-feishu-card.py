#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Java 学习日报 - 飞书卡片格式推送
# 使用飞书富文本卡片格式，支持表格、代码块、链接等

import json
import random
import sys
from datetime import datetime

# 读取题库
QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-detailed.json"

def load_questions():
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def select_questions(questions, count=5):
    """随机选择 count 道不重复的题目"""
    if len(questions) >= count:
        return random.sample(questions, count)
    return questions

def format_table(rows, headers=None):
    """格式化表格为飞书富文本格式"""
    content = []
    if headers:
        # 表头
        header_row = [{"tag": "text", "text": " | ".join(headers)}]
        content.append(header_row)
        # 分隔线
        content.append([{"tag": "text", "text": "---"}])
    # 数据行
    for row in rows:
        content.append([{"tag": "text", "text": " | ".join(str(cell) for cell in row)}])
    return content

def create_question_block(index, category, question, answer, url, total):
    """创建单个题目的富文本内容"""
    content = []
    
    # 题目标题
    content.append([
        {"tag": "text", "text": f"{index}️⃣【{category}】", "style": ["bold"]},
    ])
    
    # 问题
    content.append([
        {"tag": "text", "text": f"Q: {question}", "style": ["bold"]},
    ])
    
    # 答案（分段处理）
    answer_lines = answer.split('\n')
    for line in answer_lines:
        line = line.strip()
        if line:
            # 检查是否包含代码示例
            if line.startswith('```') or (line.startswith('    ') and len(line) > 4):
                continue  # 跳过代码块标记
            elif line.startswith('**') and line.endswith('**'):
                # 小标题
                content.append([
                    {"tag": "text", "text": line.strip('**'), "style": ["bold"]},
                ])
            elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                # 编号列表
                content.append([
                    {"tag": "text", "text": f"• {line}"},
                ])
            elif line.startswith('- '):
                # 项目列表
                content.append([
                    {"tag": "text", "text": f"• {line[2:]}"},
                ])
            else:
                content.append([
                    {"tag": "text", "text": line},
                ])
    
    # 来源链接
    content.append([
        {"tag": "text", "text": "📖 "},
        {"tag": "text", "text": "来源：", "style": ["bold"]},
        {"tag": "text", "text": " "},
        {"tag": "a", "href": url, "text": url},
    ])
    
    # 分隔线（最后一题不加）
    if index < total:
        content.append([
            {"tag": "text", "text": "───"},
        ])
    
    return content

def create_daily_report(questions):
    """创建完整的日报富文本内容"""
    today = datetime.now()
    day_count = (today - datetime(today.year, 1, 1)).days
    
    content = []
    
    # 标题
    content.append([
        {"tag": "text", "text": "📚 "},
        {"tag": "text", "text": f"Java 学习日报 - 第{day_count}天", "style": ["bold"]},
        {"tag": "text", "text": f" ({today.strftime('%Y-%m-%d')})"},
    ])
    
    # 副标题
    content.append([
        {"tag": "text", "text": "💡 每天 5 道题，系统掌握 Java 面试核心知识点"},
    ])
    
    # 分隔线
    content.append([
        {"tag": "text", "text": "───"},
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
    
    # 学习统计
    content.append([
        {"tag": "text", "text": "📊 今日学习统计", "style": ["bold"]},
    ])
    content.append([
        {"tag": "text", "text": f"📝 今日题目：{total}道"},
        {"tag": "text", "text": f"  |  📖 模块：{', '.join(set(q['category'] for q in questions))}"},
    ])
    
    # 底部
    content.append([
        {"tag": "text", "text": "───"},
    ])
    content.append([
        {"tag": "text", "text": "💪 坚持每天学习，大厂 offer 等着你！", "style": ["bold"]},
    ])
    content.append([
        {"tag": "text", "text": "📖 来源：小林 coding 面试题汇总"},
    ])
    
    return content

def main():
    # 加载题库
    questions = load_questions()
    
    # 随机选择 5 道题
    selected = select_questions(questions, 5)
    
    # 创建富文本内容
    content = create_daily_report(selected)
    
    # 输出 JSON 格式
    result = {
        "title": "",
        "content": content
    }
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
