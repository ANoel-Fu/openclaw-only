#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用正则表达式解析 HTML，提取所有题目
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

def parse_with_regex(filepath, category):
    """使用正则表达式解析 HTML"""
    questions = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 h3 标签中的问题标题（包含问号）
    # 格式：<h3 id="xxx"><a href="#xxx" class="header-anchor">#</a> 问题标题？</h3>
    pattern = r'<h3[^>]*id="([^"]+)"[^>]*>.*?</h3>'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        full_tag = match.group(0)
        
        # 提取问题文本（去掉 anchor 标签）
        text_match = re.search(r'>([^<]+)</h3>', full_tag)
        if not text_match:
            continue
        
        question_text = text_match.group(1).strip()
        
        # 跳过不包含问号或太短的
        if '?' not in question_text or len(question_text) < 5:
            continue
        
        # 获取答案（从当前 h3 结束到下一个 h2 或 h3 开始）
        start_pos = match.end()
        
        # 找到下一个标题位置
        next_h2 = re.search(r'<h2[^>]*>', content[start_pos:])
        next_h3 = re.search(r'<h3[^>]*>', content[start_pos:])
        
        # 取最近的标题位置
        next_positions = []
        if next_h2:
            next_positions.append(next_h2.start())
        if next_h3:
            next_positions.append(next_h3.start())
        
        if next_positions:
            end_pos = start_pos + min(next_positions)
        else:
            end_pos = len(content)
        
        answer_html = content[start_pos:end_pos]
        
        # 清理 HTML 标签
        answer_text = re.sub(r'<[^>]+>', '', answer_html)
        answer_text = re.sub(r'\s*\n\s*', '\n', answer_text)
        answer_text = answer_text.strip()
        
        # 限制长度
        if len(answer_text) > 5000:
            answer_text = answer_text[:5000] + "..."
        
        if answer_text:
            questions.append({
                "category": category,
                "question": question_text,
                "answer": answer_text,
                "url": URLS[category]
            })
    
    return questions

def main():
    print("=" * 60)
    print("使用正则表达式解析 HTML，提取所有题目")
    print("=" * 60)
    
    all_questions = []
    
    for category, filepath in MODULES_FILES.items():
        print(f"\n【{category}】")
        questions = parse_with_regex(filepath, category)
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
    print("\n=== 题目示例（前 5 道）===")
    for i, q in enumerate(all_questions[:5], 1):
        print(f"{i}. [{q['category']}] {q['question'][:60]}...")
        print(f"   答案长度：{len(q['answer'])} 字符")

if __name__ == "__main__":
    main()
