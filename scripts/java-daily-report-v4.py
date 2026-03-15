#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Java 学习日报 - Markdown 格式推送（v4 - 使用 openclaw message send）

# 设置完整的 PATH，确保 cron 环境下能找到 node 命令
import os
os.environ['PATH'] = '/root/.nvm/versions/node/v22.22.0/bin:' + os.environ.get('PATH', '')

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

def format_java_code(code_text):
    """
    格式化 Java 代码（简单版本）
    - 统一缩进为 4 个空格
    - 移除多余空行
    - 保持代码结构清晰
    """
    if not code_text.strip():
        return ''
    
    lines = code_text.split('\n')
    formatted_lines = []
    indent_level = 0
    indent_str = '    '  # 4 空格缩进
    
    for line in lines:
        stripped = line.strip()
        
        # 跳过空行（但保留代码块内的合理空行）
        if not stripped:
            if formatted_lines and formatted_lines[-1]:  # 避免连续空行
                formatted_lines.append('')
            continue
        
        # 检测减少缩进的符号（}）
        if stripped.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        # 添加当前行（带缩进）
        formatted_lines.append(indent_str * indent_level + stripped)
        
        # 检测增加缩进的符号（{）
        if stripped.endswith('{') or stripped.endswith(':'):
            indent_level += 1
    
    # 移除末尾的连续空行
    while formatted_lines and not formatted_lines[-1]:
        formatted_lines.pop()
    
    return '\n'.join(formatted_lines)

def format_answer_to_markdown(answer):
    """将答案转换为 Markdown 格式（支持飞书代码块 + Java 格式化）"""
    lines = []
    answer_lines = answer.split('\n')
    
    in_code_block = False
    code_lines = []
    code_language = ''
    
    for line in answer_lines:
        # 检测代码块开始（多种格式）
        if line.strip().startswith('```java') or line.strip().startswith('``` Java'):
            in_code_block = True
            code_language = 'java'
            continue
        elif line.strip().startswith('```') and not in_code_block:
            in_code_block = True
            code_language = 'java'  # 默认使用 java
            continue
        
        # 检测代码块结束
        if in_code_block and line.strip() == '```':
            # 输出代码块（飞书格式 + Java 格式化）
            if code_lines:
                # 先合并代码，然后格式化
                raw_code = '\n'.join(code_lines)
                formatted_code = format_java_code(raw_code)
                lines.append(f"```java\n{formatted_code}\n```")
            in_code_block = False
            code_lines = []
            code_language = ''
            continue
        
        # 在代码块内，收集代码行（保留原始缩进用于后续格式化）
        if in_code_block:
            code_lines.append(line)
            continue
        
        # 不在代码块内，正常处理文本
        line_stripped = line.strip()
        if not line_stripped:
            lines.append('')
            continue
        
        # 处理加粗 **text**
        if '**' in line_stripped:
            parts = line_stripped.split('**')
            formatted = ''
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 1:  # 加粗部分
                        formatted += f'**{part}**'
                    else:
                        formatted += part
            lines.append(formatted)
        # 处理编号
        elif line_stripped.startswith('1.') or line_stripped.startswith('2.') or line_stripped.startswith('3.'):
            lines.append(f"• {line_stripped}")
        # 处理项目符号
        elif line_stripped.startswith('- '):
            lines.append(f"• {line_stripped[2:]}")
        # 普通文本
        else:
            lines.append(line_stripped)
    
    # 如果代码块没有正确关闭，也要输出（带格式化）
    if in_code_block and code_lines:
        raw_code = '\n'.join(code_lines)
        formatted_code = format_java_code(raw_code)
        lines.append(f"```java\n{formatted_code}\n```")
    
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
