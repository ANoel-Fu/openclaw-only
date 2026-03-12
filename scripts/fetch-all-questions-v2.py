#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小林 coding Java 面试题完整爬虫
抓取 5 个模块的所有题目和答案
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os

# 配置
MODULES = {
    "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
    "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
    "Java 并发": "https://www.xiaolincoding.com/interview/juc.html",
    "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
    "Spring": "https://www.xiaolincoding.com/interview/spring.html",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

def fetch_page(url, max_retries=3):
    """获取页面内容，带重试机制"""
    for attempt in range(max_retries):
        try:
            print(f"  尝试获取 (第{attempt+1}次)...")
            response = requests.get(url, headers=HEADERS, timeout=60)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  获取失败：{e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return None

def parse_questions(html, category):
    """解析页面中的所有题目"""
    questions = []
    
    if not html:
        return questions
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 查找所有问题（h2, h3 标签，包含问号）
    for header in soup.find_all(['h2', 'h3', 'h4']):
        question_text = header.get_text(strip=True)
        
        # 跳过不包含问号或非问题的标题
        if not question_text or '?' not in question_text:
            continue
        
        # 跳过太短的标题
        if len(question_text) < 5:
            continue
        
        # 收集答案内容
        answer_parts = []
        next_element = header.find_next_sibling()
        
        while next_element:
            # 如果遇到下一个问题标题，停止
            if next_element.name in ['h2', 'h3', 'h4']:
                break
            
            # 获取文本内容
            if hasattr(next_element, 'get_text'):
                text = next_element.get_text(strip=True)
                if text and len(text) > 10:  # 跳过太短的内容
                    answer_parts.append(text)
            
            next_element = next_element.find_next_sibling()
        
        answer = '\n'.join(answer_parts)
        
        # 限制答案长度
        if len(answer) > 5000:
            answer = answer[:5000] + "..."
        
        if answer:
            questions.append({
                "category": category,
                "question": question_text,
                "answer": answer,
                "url": MODULES[category]
            })
    
    return questions

def main():
    print("=" * 60)
    print("小林 coding Java 面试题完整爬虫")
    print("=" * 60)
    
    all_questions = []
    
    for category, url in MODULES.items():
        print(f"\n【{category}】")
        print(f"URL: {url}")
        
        html = fetch_page(url)
        
        if html:
            questions = parse_questions(html, category)
            print(f"  ✅ 抓取到 {len(questions)} 道题目")
            all_questions.extend(questions)
            
            # 保存临时结果
            temp_output = {
                "questions": all_questions,
                "lastUpdated": "2026-03-12",
                "modules": list(MODULES.keys()),
                "totalQuestions": len(all_questions),
                "source": "小林 coding 面试题汇总",
                "urls": list(MODULES.values()),
                "status": "in_progress"
            }
            
            with open('/root/.openclaw/workspace/memory/java-interview-questions-all-modules.json', 'w', encoding='utf-8') as f:
                json.dump(temp_output, f, ensure_ascii=False, indent=2)
        else:
            print(f"  ❌ 抓取失败")
        
        # 等待一下，避免被反爬
        time.sleep(2)
    
    # 最终保存
    print("\n" + "=" * 60)
    print(f"总共抓取到 {len(all_questions)} 道题目")
    print("=" * 60)
    
    # 按模块统计
    print("\n各模块题目统计：")
    for category in MODULES.keys():
        count = len([q for q in all_questions if q['category'] == category])
        print(f"  {category}: {count} 道")
    
    output = {
        "questions": all_questions,
        "lastUpdated": "2026-03-12",
        "modules": list(MODULES.keys()),
        "totalQuestions": len(all_questions),
        "source": "小林 coding 面试题汇总",
        "urls": list(MODULES.values()),
        "status": "completed"
    }
    
    with open('/root/.openclaw/workspace/memory/java-interview-questions-all-modules.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存到：/root/.openclaw/workspace/memory/java-interview-questions-all-modules.json")
    
    # 打印前 5 道题目示例
    print("\n=== 题目示例（前 5 道）===")
    for i, q in enumerate(all_questions[:5], 1):
        print(f"{i}. [{q['category']}] {q['question'][:60]}...")
        print(f"   答案长度：{len(q['answer'])} 字符")

if __name__ == "__main__":
    main()
