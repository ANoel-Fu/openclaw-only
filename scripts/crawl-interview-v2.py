#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 requests 爬取小林coding面试题
"""

import json
import re
import requests
from bs4 import BeautifulSoup

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

CATEGORIES = {
    "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
    "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
    "Java 并发": "https://www.xiaolincoding.com/interview/concurrent.html",
    "Spring": "https://www.xiaolincoding.com/interview/spring.html",
    "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
}

def fetch_page(url):
    """抓取网页内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'  # 强制使用 UTF-8
        return response.text
    except Exception as e:
        print(f"  抓取失败: {e}")
        return None

def parse_html(html, category):
    """解析HTML提取题目"""
    questions = []
    
    if not html:
        return questions
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 找到所有题目（通常是 h3 或特定 class）
    # 小林coding的题目结构：h3 标题 + 内容
    sections = soup.find_all(['h3', 'h2'])
    
    for section in sections:
        # 获取题目
        question = section.get_text().strip()
        
        # 跳过非题目标题
        if not question or len(question) < 5:
            continue
        
        # 获取答案（下一个兄弟元素直到下一个标题）
        answer_parts = []
        current = section.find_next_sibling()
        
        while current and current.name not in ['h2', 'h3']:
            # 提取文本
            text = current.get_text()
            if text.strip():
                answer_parts.append(text)
            current = current.find_next_sibling()
        
        if answer_parts:
            answer = '\n\n'.join(answer_parts)
            
            # 清理答案
            answer = re.sub(r'\n{3,}', '\n\n', answer)
            
            questions.append({
                "question": question,
                "answer": answer,
                "category": category,
                "url": CATEGORIES.get(category, ""),
            })
    
    return questions

def main():
    print("=" * 80)
    print("开始爬取小林coding面试题 (v2)")
    print("=" * 80)
    print()
    
    all_questions = []
    
    for category, url in CATEGORIES.items():
        print(f"正在抓取: {category}...")
        html = fetch_page(url)
        if html:
            questions = parse_html(html, category)
            print(f"  解析到 {len(questions)} 道题目")
            all_questions.extend(questions)
        print()
    
    print(f"共抓取到 {len(all_questions)} 道题目")
    
    if all_questions:
        # 添加ID
        for i, q in enumerate(all_questions, 1):
            q["id"] = i
            q["timesSent"] = 0
            q["lastSent"] = None
        
        # 保存
        data = {"questions": all_questions}
        with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已保存到题库")
    else:
        print("❌ 没有抓取到题目")

if __name__ == "__main__":
    main()
