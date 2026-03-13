#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 修复 Java 题库链接 - 将中文锚点进行 URL 编码

import json
from urllib.parse import quote

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-detailed.json"

def fix_url(url):
    """修复 URL 中的中文锚点"""
    if '#' not in url:
        return url
    
    base, anchor = url.split('#', 1)
    # 对锚点进行 URL 编码
    encoded_anchor = quote(anchor, safe='-_.!~*\'()')
    return f"{base}#{encoded_anchor}"

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
        q['url'] = new_url
        
        if old_url != new_url:
            print(f"✓ {q['id']}. {old_url}")
            print(f"  → {new_url}")
    
    # 保存修复后的题库
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已修复 {len(questions)} 道题目的链接")

if __name__ == "__main__":
    main()
