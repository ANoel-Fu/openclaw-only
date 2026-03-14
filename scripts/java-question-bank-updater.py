#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Java 题库自动更新脚本 - 每天凌晨 2 点从 小林 coding 爬取最新题库
# 使用 Tavily API 获取题库内容

import json
import os
import re
import sys
import subprocess
from datetime import datetime
from urllib.parse import quote, unquote

# 题库源配置
QUESTION_SOURCES = [
    {
        "url": "https://www.xiaolincoding.com/interview/java.html",
        "category": "Java 基础",
        "search_query": "site:xiaolincoding.com interview java 基础面试题"
    },
    {
        "url": "https://www.xiaolincoding.com/interview/collections.html",
        "category": "Java 集合",
        "search_query": "site:xiaolincoding.com interview collections 集合面试题"
    },
    {
        "url": "https://www.xiaolincoding.com/interview/juc.html",
        "category": "Java 并发",
        "search_query": "site:xiaolincoding.com interview juc 并发面试题"
    },
    {
        "url": "https://www.xiaolincoding.com/interview/jvm.html",
        "category": "JVM",
        "search_query": "site:xiaolincoding.com interview jvm 虚拟机面试题"
    },
    {
        "url": "https://www.xiaolincoding.com/interview/spring.html",
        "category": "Spring",
        "search_query": "site:xiaolincoding.com interview spring 面试题"
    }
]

OUTPUT_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"
STATE_FILE = "/root/.openclaw/workspace/memory/java-daily-push-state.json"
TAVILY_API_KEY = ""

def get_tavily_api_key():
    """获取 Tavily API Key"""
    global TAVILY_API_KEY
    if TAVILY_API_KEY:
        return TAVILY_API_KEY
    
    TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '')
    if not TAVILY_API_KEY:
        try:
            with open('/root/.openclaw/.env', 'r') as f:
                for line in f:
                    if line.startswith('TAVILY_API_KEY='):
                        TAVILY_API_KEY = line.strip().split('=', 1)[1]
                        break
        except:
            pass
    return TAVILY_API_KEY

def tavily_search(query, n=20):
    """使用 Tavily search 搜索"""
    api_key = get_tavily_api_key()
    if not api_key:
        print(f"❌ 未找到 TAVILY_API_KEY")
        return None
    
    try:
        cmd = [
            'node',
            '/root/.openclaw/workspace/skills/tavily-search/scripts/search.mjs',
            query,
            '-n', str(n)
        ]
        env = os.environ.copy()
        env['TAVILY_API_KEY'] = api_key
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"❌ Tavily search 失败：{result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Tavily search 异常：{e}")
        return None

def tavily_extract(url):
    """使用 Tavily extract 获取页面内容"""
    api_key = get_tavily_api_key()
    if not api_key:
        return None
    
    try:
        cmd = [
            'node',
            '/root/.openclaw/workspace/skills/tavily-search/scripts/extract.mjs',
            url
        ]
        env = os.environ.copy()
        env['TAVILY_API_KEY'] = api_key
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except Exception as e:
        return None

def parse_questions_from_search(search_result, category):
    """从 Tavily search 结果中解析题目"""
    questions = []
    
    if not search_result:
        return questions
    
    # 解析 Sources 部分
    sources_pattern = r'\*\*\s*(.+?)\s*\*\*\s*\(relevance:\s*(\d+)%\)\s*\n\s*(https?://[^\s]+)'
    matches = re.findall(sources_pattern, search_result)
    
    for match in matches:
        title = match[0].strip()
        relevance = int(match[1])
        url = match[2].strip()
        
        # 只处理题库页面（忽略首页和其他页面）
        if not any(page in url for page in ['/java.html', '/collections.html', '/juc.html', '/jvm.html', '/spring.html']):
            continue
        
        # 标题通常是题目或分类说明
        if '面试题' in title or '汇总' in title:
            continue
        
        # 创建题目（答案需要从 extract 获取）
        questions.append({
            "question": title.replace('#', '').strip(),
            "answer": "待补充...",
            "category": category,
            "url": url,
            "timesSent": 0,
            "lastSent": None
        })
    
    return questions

def parse_questions_from_extract(content, category, base_url):
    """从 Tavily extract 内容中解析题目"""
    questions = []
    
    if not content:
        return questions
    
    # 小林 coding 的格式：### [#](#锚点) 题目文本
    # 或者：## [#](#锚点) 分类名
    pattern = r'(?:###|##)\s*\[#\]\(#([^)]+)\)\s*(.+?)\s*\n(.*?)(?=(?:###|##)|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        anchor = match[0].strip()
        title_or_category = match[1].strip()
        answer_text = match[2].strip()
        
        # 跳过分类标题（没有答案内容或答案很短）
        if len(answer_text) < 50 or any(skip in title_or_category for skip in ['汇总', '面试', '目录', '首页']):
            continue
        
        # 清理答案文本
        answer_text = re.sub(r'^\n+', '', answer_text)
        answer_text = re.sub(r'\n{3,}', '\n\n', answer_text)
        
        # 生成 URL（确保有 .html）
        safe_chars = '-_.!~*\'()'
        # 如果 base_url 不以.html 结尾，添加.html
        if not base_url.endswith('.html'):
            full_url = f"{base_url}.html#{quote(anchor, safe=safe_chars)}"
        else:
            full_url = f"{base_url}#{quote(anchor, safe=safe_chars)}"
        
        questions.append({
            "question": title_or_category,
            "answer": answer_text[:2000],  # 限制答案长度
            "category": category,
            "url": full_url,
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
    
    for q in new:
        q_key = q['question'].strip()
        if q_key in existing_map:
            existing_q = existing_map[q_key]
            q['timesSent'] = existing_q.get('timesSent', 0)
            q['lastSent'] = existing_q.get('lastSent', None)
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
    
    state = load_state()
    print(f"📋 上次更新：{state.get('lastUpdate', '从未')}")
    print(f"📊 当前题库：{state.get('totalQuestions', 0)} 道")
    
    print("\n📖 正在加载现有题库...")
    existing_questions = load_existing_questions()
    print(f"✅ 已加载 {len(existing_questions)} 道题目")
    
    all_new_questions = []
    for source in QUESTION_SOURCES:
        print(f"\n🔍 正在获取：{source['category']}")
        print(f"   URL: {source['url']}")
        
        # 使用 extract 获取页面内容
        content = tavily_extract(source['url'])
        if content:
            questions = parse_questions_from_extract(
                content,
                source['category'],
                source['url'].replace('.html', '')
            )
            print(f"   ✅ 解析到 {len(questions)} 道题目")
            all_new_questions.extend(questions)
        else:
            print(f"   ⚠️ 获取失败，跳过")
    
    print(f"\n📊 总共获取：{len(all_new_questions)} 道题目")
    
    if not all_new_questions:
        print("⚠️ 未获取到任何题目，保持现有题库")
        return 0
    
    print("\n🔄 正在去重...")
    unique_questions = deduplicate_questions(all_new_questions)
    print(f"✅ 去重后：{len(unique_questions)} 道题目")
    
    print("\n🔗 正在合并题库...")
    merged_questions = merge_questions(existing_questions, unique_questions)
    
    for i, q in enumerate(merged_questions, 1):
        q['id'] = i
    
    print(f"\n💾 正在保存题库...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({"questions": merged_questions}, f, ensure_ascii=False, indent=2)
    
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
