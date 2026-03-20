#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终打磨：修复剩余的细节问题
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

def polish_code(code_text):
    """打磨代码细节"""
    if not code_text.strip():
        return ''
    
    # 1. 修复关键字分行问题
    # public\nstatic\nvoid -> public static void
    code_text = re.sub(r'public\s+\n\s*static\s+\n\s*void', 'public static void', code_text)
    code_text = re.sub(r'public\s+\n\s*class', 'public class', code_text)
    code_text = re.sub(r'public\s+\n\s*abstract', 'public abstract', code_text)
    code_text = re.sub(r'private\s+\n\s*static', 'private static', code_text)
    
    # 2. 修复方法调用 .method() -> obj.method()
    # 找到常见的模式并修复
    lines = code_text.split('\n')
    result_lines = []
    
    for i, line in enumerate(lines):
        # 修复 .add() -> list.add()
        if re.search(r'^\s*\.\s*\w+\(', line):
            # 需要推断变量名
            prev_lines = '\n'.join(lines[max(0, i-5):i])
            
            # 尝试找到变量声明
            var_match = re.search(r'(\w+)<[^>]*>\s+(\w+)\s*=', prev_lines)
            if var_match:
                var_name = var_match.group(2)
                line = re.sub(r'^\s*\.', f'{var_name}.', line)
            else:
                # 默认变量名
                if '.add(' in line:
                    line = re.sub(r'^\s*\.', 'list.', line)
                elif '.toArray(' in line:
                    line = re.sub(r'^\s*\.', 'list.', line)
                elif '.clone(' in line:
                    line = re.sub(r'^\s*\.', 'super.', line)
        
        # 3. 修复赋值语句
        # MyClass = (MyClass) super.clone() -> MyClass obj = (MyClass) super.clone()
        if re.search(r'^\s*[A-Z]\w+\s*=\s*\(', line):
            type_name = re.match(r'^\s*([A-Z]\w+)\s*=', line).group(1)
            var_name = type_name[0].lower() + type_name[1:]
            line = re.sub(r'^\s*([A-Z]\w+)\s*=', f'{type_name} {var_name} =', line)
        
        # 4. 修复 catch(ExceptionType) -> catch(ExceptionType e)
        if 'catch(' in line and not re.search(r'catch\([^)]+\s+\w+\)', line):
            line = re.sub(r'catch\((\w+)\)', r'catch(\1 e)', line)
        
        # 5. 修复 for(int i = 0; i < ...) 中的变量
        if 'for(' in line and 'int =' in line:
            line = re.sub(r'int\s*=', 'int i =', line)
        
        result_lines.append(line)
    
    return '\n'.join(result_lines)

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
                    polished = polish_code(raw_code)
                    new_lines.extend(polished.split('\n'))
                new_lines.append('```')
        elif in_code:
            code_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    print("最终打磨代码块...")
    
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    code_questions = [q for q in data['questions'] if '```' in q['answer']]
    print(f"需要处理：{len(code_questions)} 道题")
    
    fixed = 0
    for q in code_questions:
        original = q['answer']
        q['answer'] = fix_answer(q['answer'])
        if original != q['answer']:
            fixed += 1
    
    print(f"优化了 {fixed} 道题")
    
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 完成！")

if __name__ == "__main__":
    main()
