#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Java 题库自动更新脚本 - 每天凌晨 2 点从 小林 coding 爬取最新题库

import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import quote, unquote

# 题库源配置
QUESTION_SOURCES = [
    {
        "url": "https://www.xiaolincoding.com/interview/java.html",
        "category": "Java 基础"
    },
    {
        "url": "https://www.xiaolincoding.com/interview/collections.html",
        "category": "Java 集合"
    },
    {
        "url": "https://www.xiaolincoding.com/interview/juc.html",
        "category": "Java 并发"
    },
    {
        "url": "https://www.xiaolincoding.com/interview/jvm.html",
        "category": "JVM"
    },
    {
        "url": "https://www.xiaolincoding.com/interview/spring.html",
        "category": "Spring"
    }
]

OUTPUT_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"
STATE_FILE = "/root/.openclaw/workspace/memory/java-daily-push-state.json"

def fetch_page_content(url):
    """使用 web_fetch 获取页面内容"""
    import subprocess
    cmd = ["/root/.local/share/pnpm/openclaw", "web-fetch", url, "--extract-mode", "markdown"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"❌ 获取 {url} 失败：{result.stderr}")
            return None
    except Exception as e:
        print(f"❌ 获取 {url} 异常：{e}")
        return None

def parse_questions_from_markdown(markdown_content, category):
    """从 Markdown 内容中解析题目"""
    questions = []
    
    if not markdown_content:
        return questions
    
    # 查找题目模式（通常是 ### 或 ## 开头的问题）
    # 小林 coding 的格式通常是：### #问题文本？
    pattern = r'###\s*#?(.+?)\?\s*\n(.*?)(?=###|\Z)'
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    
    for match in matches:
        question_text = match[0].strip()
        answer_text = match[1].strip()
        
        # 清理答案文本
        answer_text = re.sub(r'^\n+', '', answer_text)
        answer_text = re.sub(r'\n{3,}', '\n\n', answer_text)
        
        # 生成 URL 锚点
        anchor = question_text.lower()
        base_url = None
        
        # 根据分类确定基础 URL
        for source in QUESTION_SOURCES:
            if source["category"] == category:
                base_url = source["url"].replace('.html', '')
                break
        
        if base_url:
            # 生成文件名
            filename = base_url.split('/')[-1]
            url = f"{base_url}.html#{quote(anchor, safe='-_.!~*\'()')}"
        else:
            url = f"https://www.xiaolincoding.com/interview/java.html#{quote(anchor, safe='-_.!~*\'()')}"
        
        questions.append({
            "question": question_text,
            "answer": answer_text,
            "category": category,
            "url": url,
            "timesSent": 0,
            "lastSent": None
        })
    
    return questions

def load_existing_questions():
    """加载现有题库"""
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('questions', [])
        except Exception as e:
            print(f"⚠️ 加载现有题库失败：{e}")
            return []
    return []

def load_state():
    """加载上次更新状态"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"lastUpdate": None, "totalQuestions": 0, "sources": {}}

def save_state(state):
    """保存更新状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def deduplicate_questions(questions):
    """去重：基于问题文本"""
    seen = set()
    unique = []
    duplicates = 0
    
    for q in questions:
        q_key = q['question'].strip()
        if q_key not in seen:
            seen.add(q_key)
            unique.append(q)
        else:
            duplicates += 1
    
    print(f"📊 去重：{duplicates} 道重复题目已移除")
    return unique

def merge_questions(existing, new):
    """合并题库，保留已有题目的发送记录"""
    existing_map = {q['question'].strip(): q for q in existing}
    merged = []
    updated_count = 0
    new_count = 0
    
    # 首先添加所有新题目
    for q in new:
        q_key = q['question'].strip()
        if q_key in existing_map:
            # 保留已有题目的发送记录
            existing_q = existing_map[q_key]
            q['timesSent'] = existing_q.get('timesSent', 0)
            q['lastSent'] = existing_q.get('lastSent', None)
            # 如果答案有更新，标记
            if q['answer'] != existing_q.get('answer', ''):
                updated_count += 1
            merged.append(q)
        else:
            new_count += 1
            merged.append(q)
    
    print(f"📊 合并：{updated_count} 道题目已更新，{new_count} 道新题目")
    return merged

def main():
    print("=" * 60)
    print(f"📚 Java 题库自动更新")
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 加载状态
    state = load_state()
    print(f"📋 上次更新：{state.get('lastUpdate', '从未')}")
    print(f"📊 当前题库：{state.get('totalQuestions', 0)} 道")
    
    # 加载现有题库
    print("\n📖 正在加载现有题库...")
    existing_questions = load_existing_questions()
    print(f"✅ 已加载 {len(existing_questions)} 道题目")
    
    # 从每个源获取题目
    all_new_questions = []
    for source in QUESTION_SOURCES:
        print(f"\n🔍 正在获取：{source['category']} ({source['url']})")
        
        # 获取页面内容
        content = fetch_page_content(source['url'])
        if content:
            # 解析题目
            questions = parse_questions_from_markdown(content, source['category'])
            print(f"   ✅ 解析到 {len(questions)} 道题目")
            all_new_questions.extend(questions)
        else:
            print(f"   ⚠️ 获取失败，跳过")
    
    print(f"\n📊 总共获取：{len(all_new_questions)} 道题目")
    
    # 去重
    print("\n🔄 正在去重...")
    unique_questions = deduplicate_questions(all_new_questions)
    print(f"✅ 去重后：{len(unique_questions)} 道题目")
    
    # 合并题库
    print("\n🔗 正在合并题库...")
    merged_questions = merge_questions(existing_questions, unique_questions)
    
    # 重新编号
    for i, q in enumerate(merged_questions, 1):
        q['id'] = i
    
    # 保存题库
    print(f"\n💾 正在保存题库...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({"questions": merged_questions}, f, ensure_ascii=False, indent=2)
    
    # 更新状态
    state['lastUpdate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    state['totalQuestions'] = len(merged_questions)
    state['sources'] = {s['category']: len([q for q in merged_questions if q['category'] == s['category']]) 
                       for s in QUESTION_SOURCES}
    save_state(state)
    
    print("\n" + "=" * 60)
    print("✅ 题库更新完成！")
    print(f"📊 总题目数：{len(merged_questions)} 道")
    print(f"📋 分类统计:")
    for cat, count in sorted(state['sources'].items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count} 道")
    print(f"⏰ 完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
