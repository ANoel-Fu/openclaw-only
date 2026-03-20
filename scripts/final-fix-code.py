#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复：让人类可读的代码格式
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

def smart_fix_code(code_text):
    """
    智能修复代码，保持人类可读
    """
    if not code_text.strip():
        return ''
    
    # 如果代码已经有合理格式（超过 5 行且每行不太长），保持原样
    lines = code_text.split('\n')
    if len(lines) > 5 and max(len(l) for l in lines) < 100:
        return code_text
    
    # 1. 在注解后换行
    code_text = re.sub(r'(@\w+)', r'\n\1', code_text)
    
    # 2. 在方法声明的大括号前保留（不换行）
    # 先保护方法签名
    code_text = re.sub(r'(\w+\s*\([^)]*\))\s*\{', r'\1 {', code_text)
    
    # 3. 在分号后换行
    code_text = re.sub(r';', ';\n', code_text)
    
    # 4. 在左大括号后换行（但大括号本身不换行）
    code_text = re.sub(r'\{ ', '{\n', code_text)
    code_text = re.sub(r'\{', '{\n', code_text)
    
    # 5. 在右大括号前换行
    code_text = re.sub(r'\}', '\n}', code_text)
    
    # 6. 清理多余空行
    lines = [line.strip() for line in code_text.split('\n') if line.strip()]
    
    # 7. 添加缩进
    result = []
    indent = 0
    for line in lines:
        if line.startswith('}'):
            indent = max(0, indent - 1)
        result.append('    ' * indent + line)
        if line.endswith('{') and not line.startswith('public') and not line.startswith('private'):
            indent += 1
    
    return '\n'.join(result)

def fix_variables(code_text):
    """
    修复变量名
    """
    # 常见类型到变量名的映射
    var_map = {
        'UserRepository': 'userRepository',
        'PaymentGateway': 'paymentGateway',
        'OrderRepository': 'orderRepository',
        'OrderService': 'orderService',
        'UserService': 'userService',
        'String': 'value',
        'int': 'num',
        'Object': 'obj',
    }
    
    # 修复 private Type; -> private Type varName;
    def fix_field(match):
        type_name = match.group(1)
        var_name = var_map.get(type_name, type_name.lower())
        return f'private {type_name} {var_name};'
    
    code_text = re.sub(r'private\s+(\w+)\s*;', fix_field, code_text)
    
    # 修复 this.var = var; -> this.fieldName = fieldName;
    code_text = re.sub(r'this\.var = var;', 'this.value = value;', code_text)
    
    # 修复 final Type; -> final Type fieldName;
    def fix_final_field(match):
        type_name = match.group(1)
        # 从类型名推断：UserRepository -> userRepository
        if len(type_name) > 1:
            var_name = type_name[0].lower() + type_name[1:]
        else:
            var_name = type_name.lower()
        return f'private final {type_name} {var_name};'
    
    code_text = re.sub(r'private final (\w+)\s*;', fix_final_field, code_text)
    
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
        
        if stripped.startswith('```'):
            if not in_code:
                in_code = True
                code_lines = []
                new_lines.append('```java')
            else:
                in_code = False
                if code_lines:
                    raw_code = '\n'.join(code_lines)
                    fixed = fix_variables(raw_code)
                    fixed = smart_fix_code(fixed)
                    new_lines.extend(fixed.split('\n'))
                new_lines.append('```')
        elif in_code:
            code_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    print("开始最终修复...")
    
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    code_questions = [q for q in data['questions'] if '```' in q['answer']]
    print(f"需要修复：{len(code_questions)} 道题")
    
    fixed = 0
    for q in code_questions:
        original = q['answer']
        q['answer'] = fix_answer(q['answer'])
        if original != q['answer']:
            fixed += 1
    
    print(f"修复了 {fixed} 道题")
    
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 完成！")

if __name__ == "__main__":
    main()
