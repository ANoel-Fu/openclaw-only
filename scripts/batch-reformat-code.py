#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量重新格式化所有代码块
标准：
- 完整的变量名
- 正确的泛型格式
- 合理的空格
- 统一缩进（4空格）
- 大括号在同一行
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

# 常见类型到变量名的映射
VAR_MAP = {
    'List': 'list',
    'Map': 'map',
    'Set': 'set',
    'String': 'str',
    'Integer': 'num',
    'int': 'i',
    'Double': 'value',
    'Object': 'obj',
    'Class': 'clazz',
    'Handler': 'handler',
    'Request': 'request',
    'Response': 'response',
    'UserRepository': 'userRepository',
    'PaymentGateway': 'paymentGateway',
    'OrderRepository': 'orderRepository',
    'OrderService': 'orderService',
    'UserService': 'userService',
    'Person': 'person',
    'Student': 'student',
    'Singleton': 'instance',
    'MyClass': 'myClass',
}

def infer_var_name(type_name):
    """从类型名推断变量名"""
    if type_name in VAR_MAP:
        return VAR_MAP[type_name]
    # 默认：首字母小写
    if len(type_name) > 1:
        return type_name[0].lower() + type_name[1:]
    return type_name.lower()

def fix_generic_types(code):
    """修复泛型格式"""
    # 修复 List<String>< String> -> List<String>
    code = re.sub(r'(\w+<[^>]+>)<\s*\w+\s*>', r'\1', code)
    # 修复 List<> -> List<T>
    code = re.sub(r'(\w+)<>', r'\1<>', code)
    return code

def fix_method_calls(code):
    """修复方法调用"""
    # 修复 System.. println -> System.out.println
    code = re.sub(r'System\.\.\s*(\w+)', r'System.out.\1', code)
    # 修复 Arrays. asList -> Arrays.asList
    code = re.sub(r'Arrays\.\s*asList', r'Arrays.asList', code)
    code = re.sub(r'Collections\.\s*(\w+)', r'Collections.\1', code)
    return code

def fix_missing_vars_in_line(line):
    """修复单行中的变量名丢失"""
    # 修复 private Type; -> private Type varName;
    def fix_private_field(match):
        type_name = match.group(1)
        # 检查是否已经有变量名
        rest = match.group(2)
        if rest and rest.strip():
            return match.group(0)  # 已经有变量名，保持不变
        var_name = infer_var_name(type_name)
        return f'private {type_name} {var_name};'
    
    line = re.sub(r'private\s+(\w+)(\s*);', fix_private_field, line)
    
    # 修复 static Type; -> static Type varName;
    def fix_static_field(match):
        type_name = match.group(1)
        rest = match.group(2)
        if rest and rest.strip() and not rest.strip().startswith('='):
            return match.group(0)
        var_name = infer_var_name(type_name)
        return f'static {type_name} {var_name}'
    
    line = re.sub(r'static\s+(\w+)(\s*[=;])', fix_static_field, line)
    
    # 修复 Type = new -> Type varName = new
    def fix_declaration(match):
        type_name = match.group(1)
        rest = match.group(2)
        if '=' in rest and not re.search(r'\w+\s*=', rest):
            # 没有变量名
            var_name = infer_var_name(type_name)
            return f'{type_name} {var_name} ='
        return match.group(0)
    
    line = re.sub(r'(\w+<[^>]*>)\s*(=\s*new)', fix_declaration, line)
    line = re.sub(r'(\w+)\s*(=\s*new)', fix_declaration, line)
    
    return line

def fix_loops_and_conditions(code):
    """修复循环和条件语句"""
    # 修复 for(int = 0; -> for(int i = 0;
    def fix_for_loop(match):
        init = match.group(1)
        if '=' in init and not re.search(r'int\s+\w+\s*=', init):
            init = re.sub(r'int\s*=', r'int i =', init)
        return f'for({init};'
    
    code = re.sub(r'for\(([^;]+);', fix_for_loop, code)
    
    # 修复 ++) -> i++)
    code = re.sub(r'for\(([^;]+);([^;]+);\s*\+\+\s*\)', r'for(\1; \2; i++)', code)
    
    return code

def reformat_code(code_text):
    """重新格式化代码"""
    if not code_text.strip():
        return ''
    
    # 1. 修复泛型
    code_text = fix_generic_types(code_text)
    
    # 2. 修复方法调用
    code_text = fix_method_calls(code_text)
    
    # 3. 修复循环
    code_text = fix_loops_and_conditions(code_text)
    
    # 4. 分行处理
    # 在合理位置换行
    code_text = re.sub(r'(@\w+)', r'\n\1', code_text)
    code_text = re.sub(r'(public|private|protected|static|final|void|class|interface)\s+', r'\n\1 ', code_text)
    code_text = re.sub(r';\s*', ';\n', code_text)
    code_text = re.sub(r'\{', '{\n', code_text)
    code_text = re.sub(r'\}', '\n}', code_text)
    
    # 5. 清理空行
    lines = [line.strip() for line in code_text.split('\n') if line.strip()]
    
    # 6. 修复每行的变量名
    lines = [fix_missing_vars_in_line(line) for line in lines]
    
    # 7. 添加缩进
    result = []
    indent = 0
    for line in lines:
        if line.startswith('}'):
            indent = max(0, indent - 1)
        result.append('    ' * indent + line)
        if line.endswith('{') and not line.startswith('//'):
            indent += 1
    
    return '\n'.join(result)

def fix_answer(answer):
    """修复答案中的所有代码块"""
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
                    formatted = reformat_code(raw_code)
                    new_lines.extend(formatted.split('\n'))
                new_lines.append('```')
        elif in_code:
            code_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    print("=" * 80)
    print("批量重新格式化代码块")
    print("=" * 80)
    print()
    
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    code_questions = [q for q in questions if '```' in q['answer']]
    
    print(f"题库总题数：{len(questions)} 道")
    print(f"包含代码块的题目：{len(code_questions)} 道")
    print()
    
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
    
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 已保存到题库")

if __name__ == "__main__":
    main()
