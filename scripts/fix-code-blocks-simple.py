#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单直接的代码块修复脚本
使用正则表达式直接替换
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

def format_compressed_java(code):
    """
    格式化压缩成一行的 Java 代码
    """
    if not code or '\n' in code:
        return code  # 已经有多行，不处理
    
    # 1. 在注解后换行
    code = re.sub(r'(@\w+)', r'\n\1', code)
    
    # 2. 在关键字前换行
    code = re.sub(r' (public|private|protected|static|void|int|String|return|if|new|this|class)', r'\n\1', code)
    
    # 3. 在分号后换行
    code = re.sub(r';', ';\n', code)
    
    # 4. 在大括号后换行
    code = re.sub(r'\{', '{\n', code)
    code = re.sub(r'\}', '\n}', code)
    
    # 5. 清理多余空行
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    
    # 6. 添加缩进
    result = []
    indent = 0
    for line in lines:
        if line.startswith('}'):
            indent = max(0, indent - 1)
        result.append('    ' * indent + line)
        if line.endswith('{'):
            indent += 1
    
    return '\n'.join(result)

def fix_answer(answer):
    """
    修复答案中的代码块
    匹配模式：```\n压缩的代码\n```
    """
    pattern = r'```\n([^\n]+)\n```'
    
    def replace(match):
        code = match.group(1)
        formatted = format_compressed_java(code)
        return f'```java\n{formatted}\n```'
    
    return re.sub(pattern, replace, answer)

def main():
    print("开始修复...")
    
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed = 0
    for q in data['questions']:
        if '```' in q['answer']:
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
