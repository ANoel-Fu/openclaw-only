#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 从小林 coding 题库网站爬取的内容解析并生成题库 JSON

import json
import re
from urllib.parse import quote

def parse_module(content, module_name, base_url):
    """解析一个模块的题目内容"""
    questions = []
    
    # 匹配所有题目（### 标题）
    pattern = r'### \[#\]\([^)]*\)\s*([^\n]+)\n+(.*?)(?=\n+### \[#\]|\n+## \[#\]|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, (question, answer_content) in enumerate(matches):
        # 清理问题文本
        question = question.strip()
        
        # 提取答案（去除 Markdown 代码块标记，保留内容）
        answer = answer_content.strip()
        
        # 生成锚点链接（URL 编码）
        anchor = question.replace('`', '').replace('#', '').strip()
        encoded_anchor = quote(anchor, safe='-_.!~*\'()')
        url = f"{base_url}#{encoded_anchor}"
        
        questions.append({
            "module": module_name,
            "question": question,
            "answer": answer[:2000] + "..." if len(answer) > 2000 else answer,  # 限制答案长度
            "url": url
        })
    
    return questions

def main():
    # 读取爬取的内容文件（假设已经保存到本地）
    modules = {
        "Java 基础": {
            "file": "/tmp/java.html",
            "url": "https://www.xiaolincoding.com/interview/java.html"
        },
        "Java 集合": {
            "file": "/tmp/collections.html",
            "url": "https://www.xiaolincoding.com/interview/collections.html"
        },
        "Java 并发": {
            "file": "/tmp/juc.html",
            "url": "https://www.xiaolincoding.com/interview/juc.html"
        },
        "JVM": {
            "file": "/tmp/jvm.html",
            "url": "https://www.xiaolincoding.com/interview/jvm.html"
        },
        "Spring": {
            "file": "/tmp/spring.html",
            "url": "https://www.xiaolincoding.com/interview/spring.html"
        }
    }
    
    all_questions = []
    stats = {}
    
    for module_name, module_info in modules.items():
        try:
            with open(module_info['file'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            questions = parse_module(content, module_name, module_info['url'])
            all_questions.extend(questions)
            stats[module_name] = len(questions)
            
            print(f"✅ {module_name}: {len(questions)} 道题")
        except FileNotFoundError:
            print(f"❌ 文件不存在：{module_info['file']}")
    
    # 输出统计
    print("\n📊 题库统计：")
    total = sum(stats.values())
    for module, count in stats.items():
        print(f"  {module}: {count} 道")
    print(f"  总计：{total} 道")
    
    # 保存为 JSON
    output = {
        "total": total,
        "stats": stats,
        "questions": all_questions
    }
    
    with open('/root/.openclaw/workspace/memory/java-interview-questions-full.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 题库已保存到：/root/.openclaw/workspace/memory/java-interview-questions-full.json")

if __name__ == "__main__":
    main()
