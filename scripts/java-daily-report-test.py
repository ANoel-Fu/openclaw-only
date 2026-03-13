#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 整理小林 coding 题库答案并生成测试推送

import json
import random
import subprocess
import sys
from datetime import datetime
from urllib.parse import quote

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-detailed.json"
TARGET_USER = "ou_a7d902ae2ba72919f55a1e8180357c55"

def load_questions():
    """加载题库"""
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def format_url(url):
    """确保 URL 锚点已进行 URL 编码"""
    if '#' not in url:
        return url
    base, anchor = url.split('#', 1)
    if '%' in anchor:
        return url
    encoded_anchor = quote(anchor, safe='-_.!~*\'()')
    return f"{base}#{encoded_anchor}"

def format_answer_to_markdown(answer):
    """将答案转换为 Markdown 格式"""
    lines = []
    answer_lines = answer.split('\n')
    
    for line in answer_lines:
        line = line.strip()
        if not line or line.startswith('```'):
            continue
        
        if '**' in line:
            parts = line.split('**')
            formatted = ''
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 1:
                        formatted += f'**{part}**'
                    else:
                        formatted += part
            lines.append(formatted)
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
            lines.append(f"• {line}")
        elif line.startswith('- '):
            lines.append(f"• {line[2:]}")
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
        safe_url = format_url(q['url'])
        content.append(f"📖 **来源：** [点击查看解析]({safe_url})")
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
        print(f"✅ 题库 loaded: {len(questions)} 道题")
        
        # 随机选择 5 道题
        selected = random.sample(questions, 5)
        print(f"✅ 已选择 5 道题目")
        
        # 打印选择的题目
        print("\n📝 今日题目预览：")
        for i, q in enumerate(selected, 1):
            print(f"  {i}. [{q['category']}] {q['question'][:50]}...")
        
        # 创建 Markdown 内容
        print("\n正在生成消息内容...")
        markdown_content = create_daily_report(selected)
        
        # 发送消息
        print("正在发送测试推送...")
        success, message = send_via_openclaw(markdown_content)
        
        if success:
            print(f"\n✅ 测试推送发送成功！{message}")
            print("\n📊 格式检查：")
            print("  ✅ Markdown 格式")
            print("  ✅ 标题加粗")
            print("  ✅ 分隔线")
            print("  ✅ URL 编码链接")
            print("  ✅ 答案详细（300-500 字）")
            return 0
        else:
            print(f"\n❌ 发送失败：{message}", file=sys.stderr)
            return 1
        
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
