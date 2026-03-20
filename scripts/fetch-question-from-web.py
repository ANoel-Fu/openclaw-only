#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 xiaolincoding.com 重新抓取题目内容
修复变量名丢失的问题
"""

import json
import re
import subprocess
import sys

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

# 需要修复的题目 ID 列表
BROKEN_IDS = [8, 39, 66, 68, 92, 96, 146, 147, 150, 165, 193, 206, 239, 274]

def fetch_url_content(url):
    """使用 web_fetch 工具抓取网页内容"""
    cmd = [
        "/root/.local/share/pnpm/openclaw",
        "web-fetch",
        url,
        "--extractMode", "markdown"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"抓取失败：{url}")
            print(f"错误：{result.stderr}")
            return None
    except Exception as e:
        print(f"异常：{e}")
        return None

def extract_question_from_html(content, question_text):
    """从网页内容中提取题目和答案"""
    # 简单实现：找到题目相关的部分
    # 实际可能需要更复杂的解析
    
    if not content:
        return None
    
    # 这里需要根据实际网页结构调整
    # 暂时返回 None，表示需要手动处理
    return None

def main():
    print("=" * 80)
    print("从网站重新抓取题目内容")
    print("=" * 80)
    print()
    
    # 加载题库
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions_map = {q['id']: q for q in data['questions']}
    
    # 统计需要修复的题目
    to_fix = [qid for qid in BROKEN_IDS if qid in questions_map]
    print(f"需要修复的题目：{len(to_fix)} 道")
    print()
    
    # 逐个抓取
    for i, qid in enumerate(to_fix, 1):
        q = questions_map[qid]
        print(f"[{i}/{len(to_fix)}] ID {qid}: {q['question'][:30]}...")
        print(f"    来源：{q['url']}")
        
        # 抓取网页内容
        content = fetch_url_content(q['url'])
        if content:
            print(f"    ✅ 抓取成功，内容长度：{len(content)}")
            # TODO: 解析并更新题库
        else:
            print(f"    ❌ 抓取失败")
        print()
    
    print("完成！")

if __name__ == "__main__":
    main()
