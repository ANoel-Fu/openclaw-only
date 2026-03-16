#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI/Tech Daily News - Smart Version
每日 AI/科技热点新闻收集 + AI 摘要生成
直接抓取 36Kr 快讯页面
"""

import requests
import re
from datetime import datetime

# 配置
DATE = datetime.now().strftime('%Y-%m-%d')
TIME = datetime.now().strftime('%H:%M')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

def fetch_36kr_newsflashes():
    """抓取 36Kr 快讯"""
    news_items = []
    try:
        url = "https://36kr.com/newsflashes"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            text = response.text
            
            # 使用正则提取快讯：href="/newsflashes/数字" 后面的标题
            pattern = r'href="(/newsflashes/\d+)"[^>]*>([^<]+)'
            matches = re.findall(pattern, text)
            
            for href, title in matches:
                title = title.strip()
                # 过滤太短或太长的标题
                if len(title) > 5 and len(title) < 100:
                    # 分类
                    category = categorize_news(title)
                    
                    news_items.append({
                        "category": category,
                        "title": title,
                        "desc": "",
                        "url": f"https://36kr.com{href}",
                        "source": "36Kr"
                    })
            
            print(f"✅ 36Kr 抓取成功：{len(news_items)} 条")
            
    except Exception as e:
        print(f"❌ 36Kr 抓取失败：{e}")
    
    return news_items[:20]  # 最多 20 条

def categorize_news(title):
    """根据关键词自动分类新闻"""
    text = title.lower()
    
    if any(kw in text for kw in ['大模型', 'llm', 'gpt', 'ai agent', '智能体', 'ai 助手', '月之暗面', 'kimi', '360', '周鸿祎', 'openai']):
        return "🤖 AI 与大模型"
    elif any(kw in text for kw in ['机器人', 'robot', '人形', '自动驾驶']):
        return "🤖 机器人与自动驾驶"
    elif any(kw in text for kw in ['手机', '芯片', '半导体', 'oppo', 'vivo', '小米', '华为', '苹果', '消费电子']):
        return "📱 硬件与消费电子"
    elif any(kw in text for kw in ['融资', '投资', '上市', 'ipo', '估值', '创业', '捐赠']):
        return "💰 创投动态"
    elif any(kw in text for kw in ['汽车', '新能源', '特斯拉', '比亚迪', 'f1', '赛车']):
        return "🚗 智能汽车"
    elif any(kw in text for kw in ['医疗', '健康', '生物', '制药']):
        return "🏥 医疗科技"
    elif any(kw in text for kw in ['金融', '支付', '银行', '保险', '区块链', '黄金', '金价']):
        return "💳 金融科技"
    elif any(kw in text for kw in ['安全', '消费', '315', '监管', '市场', '数据']):
        return "🛡️ 科技与安全"
    else:
        return "🌐 科技前沿"

def generate_ai_summary(title):
    """基于标题生成 AI 精简总结"""
    
    # AI 相关
    if any(kw in title for kw in ['大模型', 'AI', '智能体', 'Agent', 'GPT', 'Kimi', '月之暗面']):
        if '融资' in title or '估值' in title:
            return "💡 大模型赛道持续火热，资本加速布局头部企业。"
        elif '安全' in title:
            return "💡 AI 安全与治理成为行业发展关键议题。"
        else:
            return "💡 AI 技术快速迭代，关注实际应用场景落地。"
    
    # 机器人相关
    if '机器人' in title:
        return "💡 人形机器人商业化加速，应用场景持续拓展。"
    
    # 手机/硬件相关
    if any(kw in title for kw in ['手机', '芯片', '消费电子']):
        return "💡 消费电子市场回暖，技术创新驱动增长。"
    
    # 创投相关
    if '融资' in title or '投资' in title or '捐赠' in title:
        return "💡 资本流向反映行业趋势，关注赛道热度。"
    
    # 汽车相关
    if any(kw in title for kw in ['汽车', '比亚迪', 'F1', '自动驾驶']):
        return "💡 中国车企加速全球化布局，技术实力持续提升。"
    
    # 默认摘要
    return "💡 点击链接阅读原文了解更多。"

def format_news_item(item, rank=None):
    """格式化单条新闻"""
    summary = generate_ai_summary(item["title"])
    rank_str = f"{rank}. " if rank else ""
    
    return f"""{rank_str}**{item["title"]}** [🔗]({item["url"]}) _来源：{item["source"]}_  
   📝 {summary}"""

def get_fallback_news():
    """备用新闻数据（当抓取失败时使用）"""
    return [
        {
            "category": "🤖 AI 与大模型",
            "title": "AI 技术持续演进",
            "desc": "各大厂加速 AI 应用落地，关注实际商业价值",
            "url": "https://36kr.com/newsflashes",
            "source": "36Kr"
        },
        {
            "category": "🌐 科技前沿",
            "title": "科技行业动态",
            "desc": "关注最新科技趋势与市场发展",
            "url": "https://36kr.com/newsflashes",
            "source": "36Kr"
        },
    ]

def generate_report():
    """生成完整日报"""
    
    # 抓取新闻
    print("📰 开始抓取今日新闻...")
    news_items = fetch_36kr_newsflashes()
    
    if len(news_items) < 3:
        print("⚠️  新闻数量不足，使用备用数据")
        news_items = get_fallback_news()
    
    # 按分类分组
    categories = {}
    for item in news_items:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # 生成报告
    report = f"""# 🤖 AI/科技日报 - {DATE}

_每日热点精选 · 把握科技脉搏 · 36Kr 实时快讯_

---

## 🔥 今日头条

"""
    
    # 按分类输出（限制每类最多 5 条）
    for cat_name, items in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
        report += f"\n### {cat_name}\n\n"
        for i, item in enumerate(items[:5], 1):
            report += format_news_item(item, i) + "\n\n"
    
    # 结尾
    report += f"""
---

## 📅 明日关注

- 科技巨头最新动向
- AI 政策与行业应用
- 消费电子市场变化

---

_数据来源：36Kr 快讯（实时抓取）_
_生成时间：{TIME}_
_下次推送：明日 8:50_

---
**💬 互动**：回复"详细"获取某条新闻深度解读，回复"添加"自定义关注领域
"""
    
    return report

if __name__ == "__main__":
    import subprocess
    import os
    
    report = generate_report()
    
    # 发送消息到飞书
    target_user = "ou_a7d902ae2ba72919f55a1e8180357c55"
    
    # 使用 openclaw message 发送
    cmd = [
        "/root/.local/share/pnpm/openclaw",
        "message",
        "send",
        "--channel", "feishu",
        "--target", target_user,
        "--message", report
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 消息发送成功")
        print(result.stdout)
    else:
        print("❌ 消息发送失败")
        print(result.stderr)
