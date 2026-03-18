#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI/Tech Daily News - Real-time Version
每日 AI/科技热点新闻收集 - 只抓取实时新闻
"""

import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# 配置
DATE = datetime.now().strftime('%Y-%m-%d')
TIME = datetime.now().strftime('%H:%M')
WEEKDAY = datetime.now().strftime('%A')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def fetch_36kr_newsflashes():
    """抓取 36Kr 快讯（实时性最好）"""
    news_items = []
    try:
        url = "https://36kr.com/newsflashes"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            text = response.text
            pattern = r'href="(/newsflashes/\d+)"[^>]*>([^<]+)'
            matches = re.findall(pattern, text)
            
            for href, title in matches[:25]:
                title = title.strip()
                if 5 < len(title) < 100:
                    category = categorize_news(title)
                    news_items.append({
                        "category": category,
                        "title": title,
                        "desc": "",
                        "url": f"https://36kr.com{href}",
                        "source": "36Kr",
                        "hours_ago": 0
                    })
            
            print(f"✅ 36Kr 抓取成功：{len(news_items)} 条")
            
    except Exception as e:
        print(f"❌ 36Kr 抓取失败：{e}")
    
    return news_items[:20]

def fetch_huxiu():
    """抓取虎嗅（最新文章）"""
    news_items = []
    try:
        url = "https://www.huxiu.com/article/"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            text = response.text
            
            pattern = r'<a[^>]*href="(/article/(\d+)\.html)"[^>]*title="([^"]+)"'
            matches = re.findall(pattern, text)
            
            for href, _, title in matches[:20]:
                title = title.strip()
                if 5 < len(title) < 100 and '广告' not in title:
                    category = categorize_news(title)
                    news_items.append({
                        "category": category,
                        "title": title,
                        "desc": "",
                        "url": f"https://www.huxiu.com{href}",
                        "source": "虎嗅",
                        "hours_ago": 2
                    })
            
            print(f"✅ 虎嗅 抓取成功：{len(news_items)} 条")
            
    except Exception as e:
        print(f"❌ 虎嗅 抓取失败：{e}")
    
    return news_items[:8]

def fetch_netease_tech():
    """抓取网易科技（只抓取快讯）"""
    news_items = []
    try:
        # 使用网易科技快讯页面
        url = "https://tech.163.com/special/00097UHL/tech_haojiao.html"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找快讯
            for a in soup.find_all('a', href=True)[:30]:
                href = a['href']
                if '163.com' in href:
                    title = a.get_text().strip()
                    if 5 < len(title) < 100 and '广告' not in title:
                        category = categorize_news(title)
                        news_items.append({
                            "category": category,
                            "title": title,
                            "desc": "",
                            "url": href,
                            "source": "网易科技",
                            "hours_ago": 1
                        })
            
            print(f"✅ 网易科技 抓取成功：{len(news_items)} 条")
            
    except Exception as e:
        print(f"❌ 网易科技 抓取失败：{e}")
    
    # 如果快讯抓取失败，使用备用方案
    if len(news_items) < 5:
        try:
            url = "https://tech.163.com/"
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找最新文章（带时间标签的）
                for time_tag in soup.find_all('span', class_='time'):
                    time_str = time_tag.get_text().strip()
                    
                    # 只取"今天"或"小时前"的内容
                    if '今天' in time_str or '小时前' in time_str:
                        article_div = time_tag.find_parent()
                        if article_div:
                            title_tag = article_div.find('a')
                            if title_tag and title_tag.get('href'):
                                title = title_tag.get_text().strip()
                                href = title_tag['href']
                                
                                if 5 < len(title) < 100 and '163.com' in href:
                                    category = categorize_news(title)
                                    news_items.append({
                                        "category": category,
                                        "title": title,
                                        "desc": "",
                                        "url": href,
                                        "source": "网易科技",
                                        "hours_ago": 1
                                    })
                
                print(f"✅ 网易科技（备用）抓取成功：{len(news_items)} 条")
                
        except Exception as e:
            print(f"❌ 网易科技备用方案失败：{e}")
    
    return news_items[:10]

def categorize_news(title):
    """根据关键词自动分类新闻"""
    text = title.lower()
    
    if any(kw in text for kw in ['大模型', 'llm', 'gpt', 'ai agent', '智能体', 'ai 助手', '月之暗面', 'kimi', '360', '周鸿祎', 'openai', 'anthropic', 'gemini', 'claude', '人工智能']):
        return "🤖 AI 与大模型"
    elif any(kw in text for kw in ['机器人', 'robot', '人形', '自动驾驶', '特斯拉 fsd', '无人驾驶']):
        return "🤖 机器人与自动驾驶"
    elif any(kw in text for kw in ['手机', '芯片', '半导体', 'oppo', 'vivo', '小米', '华为', '苹果', '消费电子', '骁龙', '麒麟']):
        return "📱 硬件与消费电子"
    elif any(kw in text for kw in ['融资', '投资', '上市', 'ipo', '估值', '创业', '捐赠', '并购', '收购']):
        return "💰 创投动态"
    elif any(kw in text for kw in ['汽车', '新能源', '特斯拉', '比亚迪', 'f1', '赛车', '蔚来', '小鹏', '理想']):
        return "🚗 智能汽车"
    elif any(kw in text for kw in ['医疗', '健康', '生物', '制药', '基因']):
        return "🏥 医疗科技"
    elif any(kw in text for kw in ['金融', '支付', '银行', '保险', '区块链', '比特币', '加密货币']):
        return "💳 金融科技"
    elif any(kw in text for kw in ['安全', '隐私', '黑客', '漏洞', '数据泄露', '监管', '反垄断']):
        return "🛡️ 科技与安全"
    else:
        return "🌐 科技前沿"

def generate_ai_summary(title, source):
    """基于标题生成 AI 精简总结"""
    
    if any(kw in title for kw in ['大模型', 'AI', '智能体', 'Agent', 'GPT', 'Kimi', '月之暗面', 'OpenAI']):
        if '融资' in title or '估值' in title:
            return "💡 大模型赛道持续火热，资本加速布局头部企业。"
        elif '安全' in title or '监管' in title:
            return "💡 AI 安全与治理成为行业发展关键议题。"
        elif '发布' in title or '推出' in title:
            return "💡 AI 技术快速迭代，关注实际应用场景落地。"
        else:
            return "💡 AI 领域持续创新，技术边界不断拓展。"
    
    if '机器人' in title or '自动驾驶' in title:
        return "💡 智能驾驶与人形机器人商业化加速推进。"
    
    if any(kw in title for kw in ['手机', '芯片', '半导体', '消费电子']):
        return "💡 消费电子市场回暖，技术创新驱动增长。"
    
    if '融资' in title or '投资' in title or '上市' in title:
        return "💡 资本流向反映行业趋势，关注赛道热度。"
    
    if any(kw in title for kw in ['汽车', '比亚迪', '特斯拉', '新能源', '蔚来']):
        return "💡 中国车企加速全球化布局，技术实力持续提升。"
    
    return "💡 点击链接阅读原文了解更多。"

def format_news_item(item, rank=None):
    """格式化单条新闻"""
    summary = generate_ai_summary(item["title"], item["source"])
    rank_str = f"{rank}. " if rank else ""
    
    return f"""{rank_str}**{item["title"]}** [🔗]({item["url"]}) _来源：{item["source"]}_  
   📝 {summary}"""

def generate_report():
    """生成完整日报"""
    
    print("📰 开始抓取实时新闻...")
    all_news = []
    
    # 优先抓取 36Kr 快讯（最实时）
    all_news.extend(fetch_36kr_newsflashes())
    
    # 虎嗅
    all_news.extend(fetch_huxiu())
    
    # 网易科技
    all_news.extend(fetch_netease_tech())
    
    print(f"📊 总计抓取：{len(all_news)} 条")
    
    # 按来源分配名额（确保多样性）
    source_quota = {"36Kr": 8, "虎嗅": 6, "网易科技": 6}
    source_counts = {}
    filtered_news = []
    
    for item in all_news:
        src = item["source"]
        quota = source_quota.get(src, 3)
        
        if src not in source_counts:
            source_counts[src] = 0
        
        if source_counts[src] < quota:
            filtered_news.append(item)
            source_counts[src] += 1
    
    all_news = filtered_news[:20]
    
    # 按分类分组
    categories = {}
    for item in all_news:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # 生成报告
    weekday_map = {
        'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三',
        'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'
    }
    weekday_cn = weekday_map.get(WEEKDAY, '')
    
    report = f"""# 🤖 AI/科技日报 - {DATE} {weekday_cn}

_每日热点精选 · 把握科技脉搏 · 综合多家来源_

---

## 🔥 今日头条

"""
    
    # 按分类输出
    for cat_name, items in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
        report += f"\n### {cat_name}\n\n"
        for i, item in enumerate(items[:5], 1):
            report += format_news_item(item, i) + "\n\n"
    
    # 结尾
    sources_used = list(set([item["source"] for item in all_news]))
    
    report += f"""
---

## 📅 明日关注

- 科技巨头最新动向
- AI 政策与行业应用
- 消费电子市场变化

---

_数据来源：{', '.join(sources_used)}（实时抓取）_
_生成时间：{TIME}_
_下次推送：明日 8:50_

---
**💬 互动**：回复"详细"获取某条新闻深度解读，回复"添加"自定义关注领域
"""
    
    return report

if __name__ == "__main__":
    import subprocess
    
    report = generate_report()
    
    # 发送消息到飞书
    target_user = "ou_a7d902ae2ba72919f55a1e8180357c55"
    
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
    else:
        print("❌ 消息发送失败")
        print(result.stderr)
