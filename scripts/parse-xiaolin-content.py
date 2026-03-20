#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析抓取的内容并更新题库
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

def parse_content(text, category):
    """解析内容提取题目"""
    questions = []
    
    # 移除安全提示
    text = re.sub(r'<<<EXTERNAL_UNTRUSTED_CONTENT.*?>>>', '', text, flags=re.DOTALL)
    text = re.sub(r'SECURITY NOTICE:.*?(?=<<<|$)', '', text, flags=re.DOTALL)
    
    # 按题目分割（以 ### [#](#... 开头）
    sections = re.split(r'###\s*\[#\]\(#[^)]+\)', text)
    
    for section in sections[1:]:  # 跳过第一个（通常是介绍）
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        # 第一行是题目
        question = lines[0].strip()
        if not question or len(question) < 5:
            continue
        
        # 剩余是答案
        answer = '\n'.join(lines[1:]).strip()
        
        # 清理答案
        answer = re.sub(r'\n{3,}', '\n\n', answer)
        
        questions.append({
            "question": question,
            "answer": answer,
            "category": category,
        })
    
    return questions

def main():
    # 读取之前抓取的内容（从web_fetch输出保存的文件）
    # 这里简化处理，实际应该从web_fetch获取
    
    print("请先将web_fetch抓取的内容保存到 /tmp/xiaolin_java.txt")
    print("然后运行此脚本解析")

if __name__ == "__main__":
    main()
