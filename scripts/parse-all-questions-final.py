#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版：直接搜索包含问号或明显是问题的文本
"""

import json
import re

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

def parse_questions(filepath, category):
    """解析 HTML 文件中的所有问题"""
    questions = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 模式 1: 匹配 >问题文本？< 格式
    pattern1 = r'>([^<>]+?\?)\s*<'
    
    # 模式 2: 匹配 h 标签中的问题
    pattern2 = r'<h[2-4][^>]*>(?:<a[^>]*>#</a>\s*)?([^<]+?)</h[2-4]>'
    
    found_positions = set()
    
    # 使用模式 1
    for match in re.finditer(pattern1, content):
        question_text = match.group(1).strip()
        
        # 过滤
        if len(question_text) < 5 or len(question_text) > 200:
            continue
        if question_text in found_positions:
            continue
        
        # 检查是否真的是问题（包含问号或明显是问题格式）
        if '?' not in question_text and not any(x in question_text for x in ['是什么', '为什么', '怎么', '如何', '区别', '哪些', '吗']):
            continue
        
        found_positions.add(question_text)
        
        # 获取答案
        start_pos = match.end()
        # 找下一个问题或标题
        next_q = re.search(pattern1, content[start_pos:])
        next_h = re.search(r'<h[1-3]', content[start_pos:])
        
        positions = []
        if next_q:
            positions.append(next_q.start())
        if next_h:
            positions.append(next_h.start())
        
        end_pos = start_pos + min(positions) if positions else start_pos + 5000
        
        answer_html = content[start_pos:end_pos]
        answer_text = re.sub(r'<[^>]+>', ' ', answer_html)
        answer_text = re.sub(r'\s+', ' ', answer_text).strip()
        
        if len(answer_text) > 5000:
            answer_text = answer_text[:5000] + "..."
        
        if answer_text and len(answer_text) > 50:
            questions.append({
                "category": category,
                "question": question_text,
                "answer": answer_text,
                "url": URLS[category]
            })
    
    return questions

def main():
    print("=" * 60)
    print("改进版：提取所有题目")
    print("=" * 60)
    
    all_questions = []
    
    for category, filepath in MODULES_FILES.items():
        print(f"\n【{category}】")
        questions = parse_questions(filepath, category)
        print(f"  ✅ 提取到 {len(questions)} 道题目")
        all_questions.extend(questions)
    
    print("\n" + "=" * 60)
    print(f"总共提取到 {len(all_questions)} 道题目")
    print("=" * 60)
    
    print("\n各模块题目统计：")
    for category in MODULES_FILES.keys():
        count = len([q for q in all_questions if q['category'] == category])
        print(f"  {category}: {count} 道")
    
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
    
    print("\n=== 题目示例（前 5 道）===")
    for i, q in enumerate(all_questions[:5], 1):
        print(f"{i}. [{q['category']}] {q['question'][:60]}...")
        print(f"   答案长度：{len(q['answer'])} 字符")

if __name__ == "__main__":
    main()
