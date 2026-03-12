#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取小林 coding Java 面试题的所有题目
"""

import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = "https://www.xiaolincoding.com"

# 5 个题库 URL
URLS = {
    "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
    "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
    "Java 并发": "https://www.xiaolincoding.com/interview/juc.html",
    "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
    "Spring": "https://www.xiaolincoding.com/interview/spring.html",
}

def fetch_page(url):
    """获取页面内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_questions(html, category):
    """解析页面中的所有题目"""
    questions = []
    
    if not html:
        return questions
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 查找所有问题标题（通常是 h2 或 h3 标签，带有 # 链接）
    # 小林 coding 的格式通常是：## [#](#问题标题) 问题标题
    for header in soup.find_all(['h2', 'h3', 'h4']):
        # 查找问题文本
        question_text = header.get_text(strip=True)
        
        # 跳过不包含问题的标题
        if not question_text or '?' not in question_text:
            continue
        
        # 查找对应的答案内容
        answer_parts = []
        next_element = header.find_next_sibling()
        
        while next_element:
            # 如果遇到下一个问题标题，停止
            if next_element.name in ['h2', 'h3', 'h4']:
                break
            
            # 获取文本内容
            if hasattr(next_element, 'get_text'):
                text = next_element.get_text(strip=True)
                if text:
                    answer_parts.append(text)
            
            next_element = next_element.find_next_sibling()
        
        answer = '\n'.join(answer_parts)
        
        # 提取 URL（当前页面的 URL）
        page_url = BASE_URL + "/interview/" + category.replace(" ", "").lower() + ".html"
        if category == "Java 基础":
            page_url = "https://www.xiaolincoding.com/interview/java.html"
        elif category == "Java 集合":
            page_url = "https://www.xiaolincoding.com/interview/collections.html"
        elif category == "Java 并发":
            page_url = "https://www.xiaolincoding.com/interview/juc.html"
        elif category == "JVM":
            page_url = "https://www.xiaolincoding.com/interview/jvm.html"
        elif category == "Spring":
            page_url = "https://www.xiaolincoding.com/interview/spring.html"
        
        questions.append({
            "category": category,
            "question": question_text,
            "answer": answer[:3000] if len(answer) > 3000 else answer,  # 限制答案长度
            "url": page_url
        })
    
    return questions

def main():
    all_questions = []
    
    for category, url in URLS.items():
        print(f"正在抓取 {category}...")
        html = fetch_page(url)
        
        if html:
            questions = parse_questions(html, category)
            print(f"  抓取到 {len(questions)} 道题目")
            all_questions.extend(questions)
        else:
            print(f"  抓取失败")
    
    print(f"\n总共抓取到 {len(all_questions)} 道题目")
    
    # 保存到文件
    output = {
        "questions": all_questions,
        "lastUpdated": "2026-03-12",
        "modules": list(URLS.keys()),
        "totalQuestions": len(all_questions),
        "source": "小林 coding 面试题汇总",
        "urls": list(URLS.values())
    }
    
    with open('/root/.openclaw/workspace/memory/java-interview-questions-all-modules.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"已保存到 /root/.openclaw/workspace/memory/java-interview-questions-all-modules.json")
    
    # 打印前 5 道题目作为示例
    print("\n=== 题目示例 ===")
    for i, q in enumerate(all_questions[:5], 1):
        print(f"{i}. [{q['category']}] {q['question'][:50]}...")

if __name__ == "__main__":
    main()
