#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI/Tech News - Real-time Alert
AI/科技新闻实时推送 - 重要新闻即时推送
"""

import subprocess
import json
import re
from datetime import datetime

LIGHTPANDA_BIN = "/root/.local/bin/lightpanda"

# 重要新闻关键词（触发实时推送）
BREAKING_KEYWORDS = [
    # AI 重大事件
    'gpt-5', 'gpt5', 'gpt 5',
    'openai', 'anthropic', 'google deepmind',
    '大模型', '人工智能', 'agi',
    '月之暗面', 'kimi', '智谱', '百川',
    
    # 重大融资/上市
    'ipo', '上市', '融资', '估值', '收购',
    
    # 重大产品发布
    '发布', '推出', '上线', '官宣',
    
    # 重大政策
    '监管', '政策', '审查', '禁令',
]

# 推送阈值（兴趣分数）
ALERT_THRESHOLD = 1.3

USER_INTERESTS = {
    "🤖 AI 与大模型": 1.5,
    "📱 硬件与消费电子": 1.2,
    "💰 创投动态": 1.0,
    "🚗 智能汽车": 1.0,
    "🌐 科技前沿": 0.8,
    "🤖 机器人与自动驾驶": 1.3,
    "🏥 医疗科技": 0.9,
    "💳 金融科技": 0.9,
    "🛡️ 科技与安全": 1.1,
}

def fetch_with_lightpanda(url, timeout=20):
    """使用 Lightpanda 快速抓取"""
    try:
        cmd = [
            LIGHTPANDA_BIN,
            "fetch",
            "--dump", "markdown",
            "--log_level", "error",
            "--timeout", "20000",
            url
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return result.stdout if result.returncode == 0 else ""
            
    except Exception as e:
        return ""

def is_breaking_news(title):
    """判断是否为重要新闻"""
    title_lower = title.lower()
    
    # 检查关键词
    for keyword in BREAKING_KEYWORDS:
        if keyword in title_lower:
            return True
    
    # 检查数字（大额融资）
    if re.search(r'(\d+[亿万]?)', title):
        return True
    
    return False

def categorize_news(title):
    """分类新闻"""
    text = title.lower()
    
    if any(kw in text for kw in ['大模型', 'llm', 'gpt', 'ai', 'openai', 'anthropic', '人工智能']):
        return "🤖 AI 与大模型"
    elif any(kw in text for kw in ['融资', '投资', '上市', 'ipo', '估值', '收购']):
        return "💰 创投动态"
    elif any(kw in text for kw in ['手机', '芯片', '半导体', '小米', '华为', '苹果']):
        return "📱 硬件与消费电子"
    elif any(kw in text for kw in ['汽车', '新能源', '特斯拉', '比亚迪']):
        return "🚗 智能汽车"
    else:
        return "🌐 科技前沿"

def send_alert(news_items):
    """发送实时推送"""
    if not news_items:
        return
    
    target_user = "ou_a7d902ae2ba72919f55a1e8180357c55"
    
    # 生成推送消息
    message = f"""# 🚨 AI/科技快讯 - {datetime.now().strftime('%H:%M')}

## 重要新闻提醒

"""
    
    for i, item in enumerate(news_items[:5], 1):
        category = categorize_news(item["title"])
        message += f"""
### {i}. {category}

**{item["title"]}** [🔗]({item["url"]}) _来源：{item["source"]}_

"""
    
    message += f"""
---
_共 {len(news_items)} 条重要新闻 · 详细日报请等待明日 8:50 推送_
"""
    
    cmd = [
        "/root/.local/share/pnpm/openclaw",
        "message",
        "send",
        "--channel", "feishu",
        "--target", target_user,
        "--message", message
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 实时推送成功：{len(news_items)} 条")
    else:
        print(f"❌ 推送失败：{result.stderr}")

def check_36kr():
    """检查 36Kr 快讯"""
    print("🔍 检查 36Kr 快讯...")
    content = fetch_with_lightpanda("https://36kr.com/newsflashes")
    
    breaking_news = []
    pattern = r'\[([^\]]+)\]\((https?://36kr\.com/newsflashes/\d+)\)'
    matches = re.findall(pattern, content)
    
    for title, url in matches[:20]:
        title = title.strip()
        if 5 < len(title) < 100 and is_breaking_news(title):
            breaking_news.append({
                "title": title,
                "url": url,
                "source": "36Kr"
            })
    
    return breaking_news

def check_qbitai():
    """检查量子位"""
    print("🔍 检查量子位...")
    content = fetch_with_lightpanda("https://www.qbitai.com/")
    
    breaking_news = []
    pattern = r'\[([^\]]+)\]\((https?://www\.qbitai\.com/[^)]+)\)'
    matches = re.findall(pattern, content)
    
    for title, url in matches[:15]:
        title = title.strip()
        if 5 < len(title) < 100 and is_breaking_news(title):
            breaking_news.append({
                "title": title,
                "url": url,
                "source": "量子位"
            })
    
    return breaking_news

if __name__ == "__main__":
    print("🚨 开始检查重要新闻...")
    
    all_breaking = []
    all_breaking.extend(check_36kr())
    all_breaking.extend(check_qbitai())
    
    print(f"📊 发现 {len(all_breaking)} 条重要新闻")
    
    if all_breaking:
        send_alert(all_breaking)
    else:
        print("ℹ️  暂无重要新闻")
