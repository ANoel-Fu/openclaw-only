#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小林 coding Java 面试题完整爬虫 v3
改进版：使用正则表达式直接匹配问题标题
"""

import requests
import re
import json
import time

# 配置
MODULES = {
    "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
    "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
    "Java 并发": "https://www.xiaolincoding.com/interview/juc.html",
    "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
    "Spring": "https://www.xiaolincoding.com/interview/spring.html",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
}

def fetch_page(url, max_retries=3):
    """获取页面内容"""
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
    return None

def parse_questions_regex(html, category):
    """使用正则表达式解析题目"""
    questions = []
    
    if not html:
        return questions
    
    # 匹配 Markdown 风格的问题标题：## [#](#xxx) 问题标题？
    # 或者：# 问题标题？
    pattern = r'(?:^|\n)\s*#+\s*(?:\[#\]\([^)]*\)\s*)?([^\n]+?\?)'
    
    matches = re.finditer(pattern, html, re.MULTILINE)
    
    positions = []
    for match in matches:
        question_text = match.group(1).strip()
        # 清理 Markdown 格式
        question_text = re.sub(r'\[.*?\]\(.*?\)', '', question_text).strip()
        
        if len(question_text) >= 5 and '?' in question_text:
            positions.append((match.start(), match.end(), question_text))
    
    # 提取每个问题对应的答案
    for i, (start, end, question_text) in enumerate(positions):
        # 答案从当前问题结束到下一个问题开始
        if i < len(positions) - 1:
            next_start = positions[i+1][0]
            answer_text = html[end:next_start]
        else:
            answer_text = html[end:end+10000]  # 最后一个问题，取后面 10000 字符
        
        # 清理答案中的 HTML 标签和多余空白
        answer_text = re.sub(r'<[^>]+>', '', answer_text)
        answer_text = re.sub(r'\n\s*\n', '\n\n', answer_text)
        answer_text = answer_text.strip()
        
        # 限制长度
        if len(answer_text) > 5000:
            answer_text = answer_text[:5000] + "..."
        
        if answer_text:
            questions.append({
                "category": category,
                "question": question_text,
                "answer": answer_text,
                "url": MODULES[category]
            })
    
    return questions

def main():
    print("=" * 60)
    print("小林 coding Java 面试题完整爬虫 v3")
    print("=" * 60)
    
    all_questions = []
    
    for category, url in MODULES.items():
        print(f"\n【{category}】")
        print(f"URL: {url}")
        
        html = fetch_page(url)
        
        if html:
            questions = parse_questions_regex(html, category)
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
        
        time.sleep(2)
    
    # 最终保存
    print("\n" + "=" * 60)
    print(f"总共抓取到 {len(all_questions)} 道题目")
    print("=" * 60)
    
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
    
    # 打印示例
    print("\n=== 题目示例（前 3 道）===")
    for i, q in enumerate(all_questions[:3], 1):
        print(f"{i}. [{q['category']}] {q['question'][:50]}...")
        print(f"   答案长度：{len(q['answer'])} 字符")

if __name__ == "__main__":
    main()
