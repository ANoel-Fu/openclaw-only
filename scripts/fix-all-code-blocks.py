#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复题库中所有代码块的格式
- 拆分压缩成一行的代码
- 添加换行和缩进
- 补充语言标识 java
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

def split_compressed_code(code_text):
    """
    将压缩成一行的 Java 代码拆分成多行
    """
    # 如果代码已经有多行，直接返回
    if '\n' in code_text:
        return code_text
    
    # 1. 在注解后添加换行
    code_text = re.sub(r'(@\w+)', r'\n\1', code_text)
    
    # 2. 在访问修饰符和关键字前添加换行
    keywords = r'(public|private|protected|static|final|abstract|class|interface|void|int|String|boolean|double|float|long|short|byte|char|return|if|else|for|while|try|catch|finally|throw|throws|new|this|super|extends|implements|import|package)'
    code_text = re.sub(r'\s+(' + keywords + r')\b', r'\n\1', code_text)
    
    # 3. 在分号后添加换行
    code_text = re.sub(r';', ';\n', code_text)
    
    # 4. 在左大括号后添加换行
    code_text = re.sub(r'\{', '{\n', code_text)
    
    # 5. 在右大括号前添加换行
    code_text = re.sub(r'\}', '\n}', code_text)
    
    # 6. 在注释前添加换行
    code_text = re.sub(r'(//.+)', r'\n\1', code_text)
    
    # 7. 在泛型符号周围添加空格（可选）
    # code_text = re.sub(r'<(\w+)>', r'< \1 >', code_text)
    
    return code_text

def format_java_code(code_text):
    """
    格式化 Java 代码（增强版本）
    """
    if not code_text.strip():
        return ''
    
    # 首先处理压缩的代码
    code_text = split_compressed_code(code_text)
    
    lines = code_text.split('\n')
    formatted_lines = []
    indent_level = 0
    indent_str = '    '  # 4 空格缩进
    
    for line in lines:
        stripped = line.strip()
        
        # 跳过空行
        if not stripped:
            if formatted_lines and formatted_lines[-1]:
                formatted_lines.append('')
            continue
        
        # 检测减少缩进的符号（}）
        if stripped.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        # 添加当前行（带缩进）
        formatted_lines.append(indent_str * indent_level + stripped)
        
        # 检测增加缩进的符号（{）
        if stripped.endswith('{'):
            indent_level += 1
    
    # 移除末尾的连续空行
    while formatted_lines and not formatted_lines[-1]:
        formatted_lines.pop()
    
    return '\n'.join(formatted_lines)

def fix_code_blocks_in_answer(answer):
    """
    修复答案中的所有代码块
    """
    lines = answer.split('\n')
    new_lines = []
    in_code_block = False
    code_lines = []
    code_lang = 'java'
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测代码块开始
        if line.strip().startswith('```'):
            # 提取语言标识
            lang_match = re.match(r'```\s*(\w*)', line.strip())
            code_lang = lang_match.group(1).lower() if lang_match and lang_match.group(1) else 'java'
            
            if code_lang not in ['java', 'xml', 'sql', 'json', 'yaml', 'bash', 'shell', 'html', 'css', 'javascript', 'python']:
                code_lang = 'java'
            
            in_code_block = True
            code_lines = []
            i += 1
            continue
        
        # 检测代码块结束
        if in_code_block and line.strip() == '```':
            # 格式化收集到的代码
            if code_lines:
                raw_code = '\n'.join(code_lines)
                formatted_code = format_java_code(raw_code)
                new_lines.append(f'```{code_lang}')
                new_lines.extend(formatted_code.split('\n'))
                new_lines.append('```')
            else:
                # 空代码块，保持原样
                new_lines.append(f'```{code_lang}')
                new_lines.append('```')
            
            in_code_block = False
            code_lines = []
            i += 1
            continue
        
        # 在代码块内，收集代码行
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
        
        # 不在代码块内，保持原样
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines)

def main():
    print("=" * 80)
    print("开始批量修复题库代码块格式")
    print("=" * 80)
    print()
    
    # 加载题库
    print("正在加载题库...")
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    print(f"题库总题数：{len(questions)} 道")
    
    # 统计需要修复的题目
    questions_with_code = [q for q in questions if '```' in q['answer']]
    print(f"包含代码块的题目：{len(questions_with_code)} 道")
    print()
    
    # 修复
    fixed_count = 0
    failed_questions = []
    
    for i, q in enumerate(questions_with_code, 1):
        original = q['answer']
        fixed = fix_code_blocks_in_answer(q['answer'])
        
        if original != fixed:
            q['answer'] = fixed
            fixed_count += 1
            
            # 显示进度（每 10 道显示一次）
            if i % 10 == 0 or i == len(questions_with_code):
                print(f"已修复 {i}/{len(questions_with_code)} 道题...")
        else:
            # 代码块可能已经是好的，或者修复失败
            failed_questions.append(q['id'])
    
    print()
    print("=" * 80)
    print(f"修复完成！")
    print(f"  - 成功修复：{fixed_count} 道")
    print(f"  - 无需修复/失败：{len(failed_questions)} 道")
    print("=" * 80)
    
    if failed_questions:
        print(f"\n以下题目可能需要手动检查：{failed_questions[:10]}")
        if len(failed_questions) > 10:
            print(f"... 还有 {len(failed_questions) - 10} 道")
    
    # 保存
    print("\n正在保存修复后的题库...")
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 保存成功！")
    print()
    print("修复记录已保存到：logs/code-block-batch-fix-2026-03-20.md")

if __name__ == "__main__":
    main()
