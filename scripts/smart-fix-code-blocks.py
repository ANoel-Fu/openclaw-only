#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能修复题库中的代码块
重点：让人类可读
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

# 常见变量名映射（用于推断丢失的变量名）
VAR_PATTERNS = {
    'UserRepository': 'userRepository',
    'PaymentGateway': 'paymentGateway',
    'OrderRepository': 'orderRepository',
    'String': 'str',
    'List': 'list',
    'Map': 'map',
    'Set': 'set',
    'Object': 'obj',
    'Handler': 'handler',
    'Request': 'request',
    'Response': 'response',
    'Person': 'person',
    'Singleton': 'instance',
}

def infer_var_name(type_name):
    """从类型名推断变量名"""
    # 首字母小写
    if not type_name:
        return 'var'
    return type_name[0].lower() + type_name[1:]

def fix_compressed_code(code_text):
    """
    修复压缩成一行的 Java 代码
    """
    if not code_text.strip():
        return ''
    
    # 如果已经有合理的换行（超过 3 行），保持原样
    lines = code_text.split('\n')
    if len(lines) > 3:
        return code_text
    
    # 1. 在注解后换行
    code_text = re.sub(r'(@\w+)', r'\n\1', code_text)
    
    # 2. 在关键字前换行
    keywords = ['public', 'private', 'protected', 'static', 'void', 'int', 'String', 
                'return', 'if', 'else', 'for', 'while', 'new', 'this', 'class', 
                'interface', 'extends', 'implements']
    for kw in keywords:
        code_text = re.sub(r' (?=' + kw + r'\b)', r'\n', code_text)
    
    # 3. 在分号后换行
    code_text = re.sub(r';', ';\n', code_text)
    
    # 4. 在大括号后换行
    code_text = re.sub(r'\{', '{\n', code_text)
    code_text = re.sub(r'\}', '\n}', code_text)
    
    # 5. 在逗号后换行（方法参数）
    code_text = re.sub(r', ', ',\n', code_text)
    
    # 6. 在注释前换行
    code_text = re.sub(r' (//.+)', r'\n\1', code_text)
    
    # 7. 清理空行
    lines = [line.strip() for line in code_text.split('\n') if line.strip()]
    
    # 8. 添加缩进
    result = []
    indent = 0
    for line in lines:
        if line.startswith('}'):
            indent = max(0, indent - 1)
        result.append('    ' * indent + line)
        if line.endswith('{'):
            indent += 1
    
    return '\n'.join(result)

def fix_missing_vars(code_text):
    """
    修复丢失的变量名
    """
    # 修复 this. =; 模式
    def fix_this_assignment(match):
        type_hint = match.group(1) if match.group(1) else 'var'
        var_name = infer_var_name(type_hint)
        return f'this.{var_name} = {var_name};'
    
    code_text = re.sub(r'this\. (\w*)\s*=\s*(\w*)\s*;', fix_this_assignment, code_text)
    code_text = re.sub(r'this\.\s*=\s*;', lambda m: 'this.var = var;', code_text)
    
    # 修复 private Type; 模式
    def fix_private_field(match):
        type_name = match.group(1)
        var_name = infer_var_name(type_name)
        return f'private {type_name} {var_name};'
    
    code_text = re.sub(r'private\s+(\w+)\s*;', fix_private_field, code_text)
    
    # 修复 (Type){ 模式（方法参数）
    def fix_method_param(match):
        type_name = match.group(1)
        var_name = infer_var_name(type_name)
        return f'({type_name} {var_name}) {{'
    
    code_text = re.sub(r'\((\w+)\)\s*\{', fix_method_param, code_text)
    
    return code_text

def fix_code_block(code_text):
    """
    完整修复代码块
    """
    # 先修复变量名
    code_text = fix_missing_vars(code_text)
    # 再格式化
    code_text = fix_compressed_code(code_text)
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
        if line.strip() == '```' or line.strip().startswith('```'):
            if not in_code:
                # 代码块开始
                in_code = True
                code_lines = []
                # 检查是否有语言标识
                if 'java' in line.lower() or line.strip() == '```':
                    new_lines.append('```java')
                else:
                    new_lines.append(line)
            else:
                # 代码块结束
                in_code = False
                if code_lines:
                    raw_code = '\n'.join(code_lines)
                    fixed_code = fix_code_block(raw_code)
                    new_lines.extend(fixed_code.split('\n'))
                new_lines.append('```')
        elif in_code:
            code_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    print("=" * 80)
    print("智能修复题库代码块 - 让人类可读")
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
