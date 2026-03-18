#!/usr/bin/env python3
# 测试各来源抓取情况

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import re
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def test_36kr():
    print("\n=== 测试 36Kr ===")
    items = []
    try:
        url = "https://36kr.com/newsflashes"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            text = response.text
            pattern = r'href="(/newsflashes/\d+)"[^>]*>([^<]+)'
            matches = re.findall(pattern, text)
            
            for href, title in matches[:5]:
                title = title.strip()
                if 5 < len(title) < 100:
                    items.append({
                        "title": title,
                        "url": f"https://36kr.com{href}",
                        "source": "36Kr"
                    })
                    print(f"✓ [{title[:60]}...] 来源：36Kr")
    except Exception as e:
        print(f"❌ 失败：{e}")
    
    return items

def test_qbitai():
    print("\n=== 测试量子位 ===")
    items = []
    try:
        url = "https://www.qbitai.com/"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            text = response.text
            pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, text)
            
            count = 0
            for href, title in matches:
                title = title.strip()
                if (5 < len(title) < 100 and 
                    'http' in href and 
                    ('qbitai.com' in href or href.startswith('/')) and
                    count < 5):
                    full_url = href if href.startswith('http') else f"https://www.qbitai.com{href}"
                    items.append({
                        "title": title,
                        "url": full_url,
                        "source": "量子位"
                    })
                    print(f"✓ [{title[:60]}...] 来源：量子位")
                    count += 1
    except Exception as e:
        print(f"❌ 失败：{e}")
    
    return items

def test_netease():
    print("\n=== 测试网易科技 ===")
    items = []
    try:
        url = "https://tech.163.com/"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            text = response.text
            pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, text)
            
            count = 0
            for href, title in matches:
                title = title.strip()
                if (5 < len(title) < 100 and 
                    '163.com' in href and
                    '广告' not in title and
                    count < 5):
                    items.append({
                        "title": title,
                        "url": href,
                        "source": "网易科技"
                    })
                    print(f"✓ [{title[:60]}...] 来源：网易科技")
                    count += 1
    except Exception as e:
        print(f"❌ 失败：{e}")
    
    return items

if __name__ == "__main__":
    print("📰 测试各来源抓取情况")
    print("=" * 60)
    
    all_items = []
    all_items.extend(test_36kr())
    all_items.extend(test_qbitai())
    all_items.extend(test_netease())
    
    print("\n" + "=" * 60)
    print(f"✅ 总计抓取：{len(all_items)} 条")
    
    # 统计来源
    sources = {}
    for item in all_items:
        src = item["source"]
        if src not in sources:
            sources[src] = 0
        sources[src] += 1
    
    print("\n📊 来源分布:")
    for src, count in sources.items():
        print(f"  {src}: {count} 条")
