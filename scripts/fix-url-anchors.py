#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 修复题库链接中的空格和大小写问题

import json
import re
from urllib.parse import quote

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-detailed.json"

def fix_anchor(anchor):
    """修复锚点：去掉空格，统一小写，中文保留"""
    # 1. 将空格替换为连字符
    anchor = anchor.replace(' ', '-')
    # 2. 转为小写（英文部分）
    anchor = anchor.lower()
    # 3. URL 编码（只编码中文字符）
    anchor = quote(anchor, safe='-_.!~*\'()')
    return anchor

def fix_url(url):
    """修复 URL 中的锚点"""
    if '#' not in url:
        return url
    
    base, anchor = url.split('#', 1)
    
    # URL 解码锚点（获取原始文本）
    from urllib.parse import unquote
    original_anchor = unquote(anchor)
    
    # 修复锚点
    fixed_anchor = fix_anchor(original_anchor)
    
    return f"{base}#{fixed_anchor}"

def main():
    # 加载题库
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    
    # 修复每个问题的链接
    print("修复链接：")
    for q in questions:
        old_url = q['url']
        new_url = fix_url(old_url)
        
        if old_url != new_url:
            print(f"✓ {q['id']}. {old_url}")
            print(f"  → {new_url}")
        
        q['url'] = new_url
    
    # 保存修复后的题库
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已修复 {len(questions)} 道题目的链接")
    
    # 显示修复后的示例
    print("\n📋 修复后的链接示例：")
    for i, q in enumerate(questions[:5], 1):
        anchor = q['url'].split('#')[-1]
        print(f"  {i}. #{anchor}")

if __name__ == "__main__":
    main()
