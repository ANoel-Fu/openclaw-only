#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析小林 coding 5 个模块的所有面试题，生成完整题库
"""

import json
import re

# 5 个模块的原始内容（从 web_fetch 获取）
MODULES = {
    "Java 基础": "java_base.txt",
    "Java 集合": "java_collections.txt",
    "Java 并发": "java_juc.txt",
    "JVM": "java_jvm.txt",
    "Spring": "java_spring.txt",
}

URLS = {
    "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
    "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
    "Java 并发": "https://www.xiaolincoding.com/interview/juc.html",
    "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
    "Spring": "https://www.xiaolincoding.com/interview/spring.html",
}

def parse_questions_from_text(text, category):
    """从文本中解析所有题目"""
    questions = []
    
    # 匹配问题标题（包含问号的标题）
    # 小林 coding 的格式：# 问题标题？
    pattern = r'#\s*(.+?\?)'
    
    matches = re.finditer(pattern, text)
    
    for match in matches:
        question_text = match.group(1).strip()
        
        # 跳过不包含实质内容的问题
        if len(question_text) < 5 or question_text.startswith('SECURITY'):
            continue
        
        # 获取问题后的答案内容
        start_pos = match.end()
        
        # 找到下一个问题标题的位置
        next_match = re.search(r'#\s*.+?\?', text[start_pos:])
        if next_match:
            end_pos = start_pos + next_match.start()
        else:
            end_pos = len(text)
        
        # 提取答案
        answer_text = text[start_pos:end_pos].strip()
        
        # 清理答案文本
        answer_lines = []
        for line in answer_text.split('\n'):
            # 跳过空行和纯格式行
            line = line.strip()
            if line and not line.startswith('<<<') and not line.startswith('>>>') and not line.startswith('SECURITY'):
                answer_lines.append(line)
        
        answer = '\n'.join(answer_lines)[:5000]  # 限制答案长度
        
        if answer:
            questions.append({
                "category": category,
                "question": question_text,
                "answer": answer,
                "url": URLS[category]
            })
    
    return questions

def main():
    all_questions = []
    
    for category, filename in MODULES.items():
        try:
            # 读取缓存的文件内容
            with open(f'/tmp/{filename}', 'r', encoding='utf-8') as f:
                content = f.read()
            
            questions = parse_questions_from_text(content, category)
            print(f"{category}: 解析到 {len(questions)} 道题目")
            all_questions.extend(questions)
        except FileNotFoundError:
            print(f"{category}: 文件不存在，跳过")
    
    print(f"\n总共解析到 {len(all_questions)} 道题目")
    
    # 保存到文件
    output = {
        "questions": all_questions,
        "lastUpdated": "2026-03-12",
        "modules": list(MODULES.keys()),
        "totalQuestions": len(all_questions),
        "source": "小林 coding 面试题汇总",
        "urls": list(URLS.values())
    }
    
    with open('/root/.openclaw/workspace/memory/java-interview-questions-all-modules.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"已保存到 /root/.openclaw/workspace/memory/java-interview-questions-all-modules.json")
    
    # 打印各模块统计
    print("\n=== 各模块题目统计 ===")
    for category in MODULES.keys():
        count = len([q for q in all_questions if q['category'] == category])
        print(f"{category}: {count} 道")

if __name__ == "__main__":
    main()
