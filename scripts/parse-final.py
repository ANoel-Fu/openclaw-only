#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小林 coding Java 面试题解析器 - 最终版
从 HTML 文件中提取所有题目和答案
"""

import json
import re
from bs4 import BeautifulSoup

MODULES_FILES = {
    "Java 基础": "/root/.openclaw/workspace/tmp-java-base.html",
    "Java 集合": "/root/.openclaw/workspace/tmp-collections.html",
    "Java 并发": "/root/.openclaw/workspace/tmp-juc.html",
    "JVM": "/root/.openclaw/workspace/tmp-jvm.html",
    "Spring": "/root/.openclaw/workspace/tmp-spring.html",
}

URLS = {
    "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
    "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
    "Java 并发": "https://www.xiaolincoding.com/interview/juc.html",
    "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
    "Spring": "https://www.xiaolincoding.com/interview/spring.html",
}

def parse_html(filepath, category):
    """解析 HTML 文件"""
    questions = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 查找所有 h3 标签（问题标题通常在 h3 中）
    for header in soup.find_all(['h2', 'h3']):
        question_text = header.get_text(strip=True)
        
        # 跳过不包含问号或太短的标题
        if '?' not in question_text or len(question_text) < 5:
            continue
        
        # 收集答案内容
        answer_parts = []
        next_elem = header.find_next_sibling()
        
        while next_elem and next_elem.name not in ['h2', 'h3', 'h4']:
            if hasattr(next_elem, 'get_text'):
                text = next_elem.get_text(strip=True)
                if text and len(text) > 20:
                    answer_parts.append(text)
            next_elem = next_elem.find_next_sibling()
        
        answer = '\n'.join(answer_parts)
        
        # 清理和限制
        answer = re.sub(r'\n\s*\n', '\n\n', answer).strip()
        if len(answer) > 5000:
            answer = answer[:5000] + "..."
        
        if answer and len(answer) > 100:
            questions.append({
                "category": category,
                "question": question_text,
                "answer": answer,
                "url": URLS[category]
            })
    
    return questions

def main():
    print("=" * 60)
    print("小林 coding Java 面试题解析器")
    print("=" * 60)
    
    all_questions = []
    
    for category, filepath in MODULES_FILES.items():
        print(f"\n【{category}】")
        questions = parse_html(filepath, category)
        print(f"  ✅ 提取到 {len(questions)} 道题目")
        all_questions.extend(questions)
    
    print("\n" + "=" * 60)
    print(f"总共提取到 {len(all_questions)} 道题目")
    print("=" * 60)
    
    print("\n各模块题目统计：")
    for category in MODULES_FILES.keys():
        count = len([q for q in all_questions if q['category'] == category])
        print(f"  {category}: {count} 道")
    
    # 保存
    output = {
        "questions": all_questions,
        "lastUpdated": "2026-03-12",
        "modules": list(MODULES_FILES.keys()),
        "totalQuestions": len(all_questions),
        "source": "小林 coding 面试题汇总",
        "urls": list(URLS.values()),
        "status": "completed"
    }
    
    with open('/root/.openclaw/workspace/memory/java-interview-questions-all-modules.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已保存到：/root/.openclaw/workspace/memory/java-interview-questions-all-modules.json")
    
    # 示例
    print("\n=== 题目示例（前 3 道）===")
    for i, q in enumerate(all_questions[:3], 1):
        print(f"{i}. [{q['category']}] {q['question'][:60]}...")
        print(f"   答案长度：{len(q['answer'])} 字符")

if __name__ == "__main__":
    main()
