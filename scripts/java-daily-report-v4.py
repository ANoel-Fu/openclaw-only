#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Java 学习日报 - Markdown 格式推送（v4 - 使用 openclaw message send）

import json
import random
import subprocess
import sys
from datetime import datetime
from urllib.parse import quote

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"
TARGET_USER = "ou_a7d902ae2ba72919f55a1e8180357c55"

def load_questions():
    """加载题库"""
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def format_url(url, variant='original'):
    """
    确保 URL 锚点已进行 URL 编码
    
    Args:
        url: 原始 URL
        variant: 'original'（保留空格）, 'no-space'（去除空格）, 'dash'（替换为连字符）
    """
    if '#' not in url:
        return url
    base, anchor = url.split('#', 1)
    
    # URL 解码锚点（获取原始文本）
    from urllib.parse import unquote
    original_anchor = unquote(anchor)
    
    # 转为小写
    anchor_lower = original_anchor.lower()
    
    # 根据 variant 处理空格
    if variant == 'no-space':
        # 去除所有空格
        anchor_lower = anchor_lower.replace(' ', '')
    elif variant == 'dash':
        # 空格替换为连字符
        anchor_lower = anchor_lower.replace(' ', '-')
    # else: original 保留空格
    
    # URL 编码
    encoded_anchor = quote(anchor_lower, safe='-_.!~*\'()')
    
    return f"{base}#{encoded_anchor}"

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
    """创建完整的日报 Markdown 内容"""
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    
    content = []
    
    # 标题
    content.append(f"# 📚 Java 学习日报 - 第{day_of_year}天 ({today.strftime('%Y-%m-%d')})")
    content.append("")
    content.append("💡 每天 5 道题，系统掌握 Java 面试核心知识点")
    content.append("")
    content.append("---")
    content.append("")
    
    # 题目内容
    for i, q in enumerate(questions, 1):
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
        
        # 来源链接（自动编码）
        original_url = format_url(q['url'], 'original')
        no_space_url = format_url(q['url'], 'no-space')
        dash_url = format_url(q['url'], 'dash')
        
        # 检查锚点是否包含空格
        from urllib.parse import unquote
        anchor = unquote(q['url'].split('#')[-1])
        has_space = ' ' in anchor
        
        if has_space:
            # 如果包含空格，提供两个链接版本（使用更简单的格式）
            content.append(f"📖 **来源链接 1（去除空格）：** [点击跳转]({no_space_url})")
            content.append(f"📖 **来源链接 2（替换为-）：** [点击跳转]({dash_url})")
        else:
            # 不包含空格，使用原始链接
            content.append(f"📖 **来源：** [点击查看解析]({original_url})")
        content.append("")
        content.append("---")
        content.append("")
    
    # 底部统计
    categories = list(set(q['category'] for q in questions))
    content.append("## 📊 今日学习统计")
    content.append("")
    content.append(f"📝 今日题目：{len(questions)}道")
    content.append(f"📖 模块：{', '.join(categories)}")
    content.append("")
    content.append("---")
    content.append("")
    content.append("**💪 坚持每天学习，大厂 offer 等着你！**")
    content.append("")
    content.append("📖 来源：小林 coding 面试题汇总")
    
    return '\n'.join(content)

def send_via_openclaw(message_text):
    """通过 openclaw message send 发送消息"""
    cmd = [
        "/root/.local/share/pnpm/openclaw",
        "message", "send",
        "--channel", "feishu",
        "--target", TARGET_USER,
        "--message", message_text
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            # 提取 Message ID
            for line in result.stdout.split('\n'):
                if 'Message ID:' in line:
                    return True, line.strip()
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def main():
    try:
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
        success, message = send_via_openclaw(markdown_content)
        
        if success:
            print(f"✅ Java 学习日报发送成功！{message}")
            return 0
        else:
            print(f"❌ 发送失败：{message}", file=sys.stderr)
            return 1
        
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
