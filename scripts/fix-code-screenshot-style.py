#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按照截图标准修复代码块格式
- 大括号 { 在同一行
- 4 空格缩进
- 完整变量名
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

def fix_code_line_by_line(code_text):
    """
    逐行修复压缩的代码
    标准格式：
    public synchronized V put(K key, V value) {
        // comment
        if (condition) {
            statement;
        }
    }
    """
    if not code_text.strip():
        return ''
    
    lines = code_text.split('\n')
    
    # 如果已经有合理格式（超过 5 行），保持原样
    if len(lines) > 5:
        return code_text
    
    # 1. 在注解后换行
    code_text = re.sub(r'(@\w+)', r'\n\1', code_text)
    
    # 2. 在关键字前换行（但保持 { 在同一行）
    keywords = ['public', 'private', 'protected', 'static', 'void', 'int', 'String', 
                'return', 'if', 'else', 'for', 'while', 'new', 'this', 'class', 
                'interface', 'extends', 'implements', 'try', 'catch', 'finally']
    for kw in keywords:
        # 在关键字前换行，但 { 保持在上一行
        code_text = re.sub(r' (' + kw + r'\b)', r'\n\1', code_text)
    
    # 3. 在分号后换行
    code_text = re.sub(r';', ';\n', code_text)
    
    # 4. 在左大括号前保留空格，不换行
    # 已经处理了
    
    # 5. 在右大括号前换行
    code_text = re.sub(r'\}', '\n}', code_text)
    
    # 6. 在注释前换行
    code_text = re.sub(r' (//.+)', r'\n\1', code_text)
    
    # 7. 清理空行
    lines = [line.strip() for line in code_text.split('\n') if line.strip()]
    
    # 8. 添加缩进（{ 不单独占一行）
    result = []
    indent = 0
    for line in lines:
        if line.startswith('}'):
            indent = max(0, indent - 1)
        
        # 如果行以 { 结尾，当前行用当前缩进，下一行增加缩进
        result.append('    ' * indent + line)
        
        if line.endswith('{'):
            indent += 1
    
    return '\n'.join(result)

def fix_missing_variables(code_text):
    """
    修复丢失的变量名
    """
    # 修复 private Type; -> private Type varName;
    def fix_field(match):
        type_name = match.group(1)
        var_name = type_name[0].lower() + type_name[1:] if len(type_name) > 1 else type_name.lower()
        return f'private {type_name} {var_name};'
    
    code_text = re.sub(r'private\s+(\w+)\s*;', fix_field, code_text)
    
    # 修复 this. =; -> this.var = var;
    def fix_this(match):
        type_hint = match.group(1) if match.group(1) else 'var'
        var_name = type_hint[0].lower() + type_hint[1:] if len(type_hint) > 1 else 'var'
        return f'this.{var_name} = {var_name};'
    
    code_text = re.sub(r'this\. (\w*)\s*=\s*(\w*)\s*;', fix_this, code_text)
    code_text = re.sub(r'this\.\s*=\s*;', 'this.var = var;', code_text)
    
    # 修复 (Type){ -> (Type varName) {
    def fix_param(match):
        type_name = match.group(1)
        var_name = type_name[0].lower() + type_name[1:] if len(type_name) > 1 else type_name.lower()
        return f'({type_name} {var_name}) {{'
    
    code_text = re.sub(r'\((\w+)\)\s*\{', fix_param, code_text)
    
    return code_text

def fix_answer(answer):
    """
    修复答案中的所有代码块
    """
    lines = answer.split('\n')
    new_lines = []
    in_code = False
    code_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # 检测代码块开始
        if stripped.startswith('```'):
            if not in_code:
                in_code = True
                code_lines = []
                new_lines.append('```java')
            else:
                # 代码块结束
                in_code = False
                if code_lines:
                    raw_code = '\n'.join(code_lines)
                    # 先修复变量名，再格式化
                    fixed_code = fix_missing_variables(raw_code)
                    fixed_code = fix_code_line_by_line(fixed_code)
                    new_lines.extend(fixed_code.split('\n'))
                new_lines.append('```')
        elif in_code:
            code_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    print("=" * 80)
    print("按照截图标准修复代码块")
    print("=" * 80)
    print()
    
    # 加载题库
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    code_questions = [q for q in questions if '```' in q['answer']]
    
    print(f"题库总题数：{len(questions)} 道")
    print(f"包含代码块的题目：{len(code_questions)} 道")
    print()
    
    # 修复
    fixed = 0
    for i, q in enumerate(code_questions, 1):
        original = q['answer']
        q['answer'] = fix_answer(q['answer'])
        
        if original != q['answer']:
            fixed += 1
        
        if i % 20 == 0 or i == len(code_questions):
            print(f"已修复 {i}/{len(code_questions)} 道...")
    
    print()
    print(f"✅ 修复完成！共修复 {fixed} 道题目")
    
    # 保存
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 已保存到题库")

if __name__ == "__main__":
    main()
