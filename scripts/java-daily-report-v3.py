#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Java 学习日报 - 飞书富文本卡片格式推送（v3 - 直接调用飞书 API）

import json
import random
import requests
import sys
from datetime import datetime

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-detailed.json"
TARGET_USER = "ou_a7d902ae2ba72919f55a1e8180357c55"

# 飞书 API 配置
FEISHU_APP_ID = "cli_a591dd18a0c09014"
FEISHU_APP_SECRET = "Fq8j2M78yQxkQ5bQjGKvWUAI"
FEISHU_API_BASE = "https://open.feishu.cn"

def get_access_token():
    """获取飞书 access_token"""
    url = f"{FEISHU_API_BASE}/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    response = requests.post(url, json=payload, timeout=10)
    result = response.json()
    if result.get('code') != 0:
        raise Exception(f"获取 access_token 失败：{result}")
    return result.get('tenant_access_token')

def load_questions():
    """加载题库"""
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def select_questions(questions, count=5):
    """随机选择 count 道不重复的题目"""
    if len(questions) >= count:
        return random.sample(questions, count)
    return questions

def format_answer_to_markdown(answer):
    """将答案转换为 Markdown 格式"""
    lines = []
    answer_lines = answer.split('\n')
    
    for line in answer_lines:
        line = line.strip()
        if not line or line.startswith('```'):
            continue
        
        # 处理加粗 **text**
        if '**' in line:
            parts = line.split('**')
            formatted = ''
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 1:  # 加粗部分
                        formatted += f'**{part}**'
                    else:
                        formatted += part
            lines.append(formatted)
        # 处理编号
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
            lines.append(f"• {line}")
        # 处理项目符号
        elif line.startswith('- '):
            lines.append(f"• {line[2:]}")
        # 普通文本
        else:
            lines.append(line)
    
    return '\n'.join(lines)

def create_daily_report(questions):
    """创建完整的日报富文本内容（Markdown 格式）"""
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    
    content = []
    
    # 标题
    content.append(f"# 📚 Java 学习日报 - 第{day_of_year}天 ({today.strftime('%Y-%m-%d')})")
    content.append("")
    content.append("💡 每天 5 道题，系统掌握 Java 面试核心知识点")
    content.append("")
    
    # 题目内容
    for i, q in enumerate(questions, 1):
        content.append("---")
        content.append(f"## {i}️⃣【{q['category']}】")
        content.append("")
        content.append(f"**Q: {q['question']}**")
        content.append("")
        content.append("**✅ 答案：**")
        content.append("")
        
        # 格式化答案
        formatted_answer = format_answer_to_markdown(q['answer'])
        content.append(formatted_answer)
        content.append("")
        
        # 来源链接
        content.append(f"📖 **来源：** [{q['url']}]({q['url']})")
        content.append("")
    
    # 底部统计
    categories = list(set(q['category'] for q in questions))
    content.append("---")
    content.append("## 📊 今日学习统计")
    content.append("")
    content.append(f"📝 今日题目：{len(questions)}道  |  📖 模块：{', '.join(categories)}")
    content.append("")
    content.append("---")
    content.append("")
    content.append("**💪 坚持每天学习，大厂 offer 等着你！**")
    content.append("")
    content.append("📖 来源：小林 coding 面试题汇总")
    
    return '\n'.join(content)

def send_rich_text_message(access_token, user_id, markdown_content):
    """发送文本消息（使用 text 消息类型，支持 Markdown 渲染）"""
    url = f"{FEISHU_API_BASE}/open-apis/im/v1/messages"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 使用 text 消息类型，飞书会自动渲染 Markdown
    payload = {
        "receive_id": user_id,
        "msg_type": "text",
        "content": json.dumps({
            "text": markdown_content
        })
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    result = response.json()
    
    if result.get('code') != 0:
        raise Exception(f"发送消息失败：{result}")
    
    return result

def main():
    try:
        # 获取 access_token
        print("正在获取 access_token...")
        access_token = get_access_token()
        
        # 加载题库
        print("正在加载题库...")
        questions = load_questions()
        
        # 随机选择 5 道题
        selected = select_questions(questions, 5)
        print(f"已选择 {len(selected)} 道题目")
        
        # 创建 Markdown 内容
        print("正在生成消息内容...")
        markdown_content = create_daily_report(selected)
        
        # 发送消息
        print("正在发送消息...")
        result = send_rich_text_message(access_token, TARGET_USER, markdown_content)
        
        message_id = result.get('data', {}).get('message_id', 'unknown')
        print(f"✅ Java 学习日报发送成功！Message ID: {message_id}")
        
        return 0
        
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
