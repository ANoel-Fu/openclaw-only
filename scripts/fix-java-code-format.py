#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 Java 题库中的代码格式问题
- 将压缩成一行的代码恢复成多行
- 修复丢失的变量名
- 添加正确的换行和缩进
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

def fix_java_code(code_text):
    """
    修复 Java 代码格式
    - 在注解后换行
    - 在访问修饰符后换行
    - 在分号后换行
    - 在括号后合理换行
    - 修复缩进
    """
    if not code_text.strip():
        return ''
    
    # 首先处理一些明显的模式
    lines = []
    
    # 将代码按一定规则拆分
    # 1. 在注解后拆分 (@Service, @Autowired, @Override 等)
    code_text = re.sub(r'(@\w+)', r'\n\1', code_text)
    
    # 2. 在访问修饰符前拆分 (public, private, protected)
    code_text = re.sub(r'\s+(public|private|protected|static|final|abstract)', r'\n\1', code_text)
    
    # 3. 在分号后换行
    code_text = re.sub(r';\s*', ';\n', code_text)
    
    # 4. 在左大括号后换行
    code_text = re.sub(r'\{', '{\n', code_text)
    
    # 5. 在右大括号前换行
    code_text = re.sub(r'\}', '\n}', code_text)
    
    # 6. 移除多余的空行
    lines = [line.strip() for line in code_text.split('\n') if line.strip()]
    
    # 7. 添加缩进
    formatted_lines = []
    indent_level = 0
    indent_str = '    '
    
    for line in lines:
        # 检测减少缩进
        if line.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        formatted_lines.append(indent_str * indent_level + line)
        
        # 检测增加缩进
        if line.endswith('{'):
            indent_level += 1
    
    return '\n'.join(formatted_lines)

def fix_question_answer(answer):
    """修复答案中的代码块"""
    # 查找代码块
    code_block_pattern = r'```\s*(\w*)\s*\n(.*?)```'
    
    def replace_code_block(match):
        lang = match.group(1) or 'java'
        code = match.group(2)
        
        # 修复代码格式
        fixed_code = fix_java_code(code)
        
        return f'```{lang}\n{fixed_code}\n```'
    
    # 替换所有代码块
    fixed_answer = re.sub(code_block_pattern, replace_code_block, answer, flags=re.DOTALL)
    
    return fixed_answer

def main():
    # 加载题库
    print("正在加载题库...")
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    fixed_count = 0
    
    # 修复包含代码块的题目
    for i, q in enumerate(questions):
        if '```' in q['answer']:
            original = q['answer']
            fixed = fix_question_answer(q['answer'])
            
            if original != fixed:
                q['answer'] = fixed
                fixed_count += 1
                print(f"修复了题目 {q['id']}: {q['question'][:30]}...")
    
    # 保存修复后的题库
    print(f"\n共修复了 {fixed_count} 道题目的代码格式")
    print("正在保存...")
    
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 修复完成！")

if __name__ == "__main__":
    main()
