#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从小林coding网站爬取Java面试题
"""

import json
import re
import subprocess

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

# 分类URL映射
CATEGORIES = {
    "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
    "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
    "Java 并发": "https://www.xiaolincoding.com/interview/concurrent.html",
    "Spring": "https://www.xiaolincoding.com/interview/spring.html",
    "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
}

def fetch_page(url):
    """抓取网页内容"""
    cmd = ["/root/.local/share/pnpm/openclaw", "web-fetch", url, "--extractMode", "markdown", "--maxChars", "20000"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        print(f"抓取失败: {e}")
        return None

def parse_questions(content, category):
    """解析题目和答案"""
    questions = []
    
    if not content:
        return questions
    
    # 移除安全提示
    content = re.sub(r'<<<EXTERNAL_UNTRUSTED_CONTENT.*?>>>', '', content, flags=re.DOTALL)
    content = re.sub(r'SECURITY NOTICE:.*?(?=<<<|$)', '', content, flags=re.DOTALL)
    
    # 按题目分割（以 ### [#](#... 开头）
    sections = re.split(r'###\s*\[#\]\(#[^)]+\)', content)
    
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
        answer = re.sub(r'\n+', '\n\n', answer)  # 合并多个空行
        
        questions.append({
            "question": question,
            "answer": answer,
            "category": category,
            "url": CATEGORIES.get(category, ""),
        })
    
    return questions

def main():
    print("=" * 80)
    print("开始爬取小林coding面试题")
    print("=" * 80)
    print()
    
    all_questions = []
    
    for category, url in CATEGORIES.items():
        print(f"正在抓取: {category}...")
        content = fetch_page(url)
        if content:
            questions = parse_questions(content, category)
            print(f"  解析到 {len(questions)} 道题目")
            all_questions.extend(questions)
        else:
            print(f"  ❌ 抓取失败")
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
