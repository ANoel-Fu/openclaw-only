#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI/Tech Daily News - Smart Version
每日 AI/科技热点新闻收集 + AI 摘要生成
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re

# 配置
DATE = datetime.now().strftime('%Y-%m-%d')
TIME = datetime.now().strftime('%H:%M')

# 新闻列表（标题 + 链接 + 分类）
NEWS_ITEMS = [
    {
        "category": "AI 与大模型",
        "title": "腾讯版小龙虾爆火",
        "desc": "能接入 QQ、飞书、钉钉等工具的 AI 助手，致歉已紧急扩容",
        "url": "https://www.huxiu.com/article/4840677.html",
        "source": "虎嗅"
    },
    {
        "category": "AI 与大模型",
        "title": "AI 短剧霍去病辟谣",
        "desc": "从业者集体辟谣：根本搜不到，不存在 3000 块钱 80 集",
        "url": "https://www.huxiu.com/article/4840071.html",
        "source": "虎嗅"
    },
    {
        "category": "AI 与大模型",
        "title": "智能经济新形态",
        "desc": "首现政府工作报告，AI 成为国家战略重点",
        "url": "https://www.huxiu.com/article/4839477.html",
        "source": "虎嗅"
    },
    {
        "category": "科技巨头动态",
        "title": "阿里字节死磕昔日赛道",
        "desc": "两大巨头在全军覆没的赛道再次交锋",
        "url": "https://www.huxiu.com/article/4840662.html",
        "source": "虎嗅·DT 商业观察"
    },
    {
        "category": "科技巨头动态",
        "title": "OPPO 一加宣布涨价",
        "desc": "3 月 10 号启动，vivo、小米、荣耀也拟定于 3 月涨价",
        "url": "https://www.huxiu.com/moment/recommended_feed.html",
        "source": "虎嗅 24 小时"
    },
    {
        "category": "科技巨头动态",
        "title": "B 站成巨头香饽饽",
        "desc": "扭亏之后，进可攻退可守",
        "url": "https://www.huxiu.com/article/4840187.html",
        "source": "虎嗅"
    },
    {
        "category": "前沿科技",
        "title": "中国医疗 AI 战事",
        "desc": "十年 To B 血泪史，从改变医生转向亲近患者",
        "url": "https://www.huxiu.com/article/4836991.html",
        "source": "虎嗅"
    },
    {
        "category": "前沿科技",
        "title": "Agent 安全花钱",
        "desc": "AI 代理支付安全成为新焦点，各大厂卷起来了",
        "url": "https://www.huxiu.com/article/4840660.html",
        "source": "虎嗅·动察 Beating"
    },
    {
        "category": "前沿科技",
        "title": "人人都在装龙虾",
        "desc": "AI 智能体热潮下的冷思考",
        "url": "https://www.huxiu.com/article/4840677.html",
        "source": "虎嗅·有机大橘子"
    },
]

INDUSTRY_NEWS = [
    {
        "title": "健康险市场",
        "desc": "离万亿市场只差一步，2026 年把油门踩到冒烟",
        "url": "https://www.huxiu.com/article/4840583.html",
        "source": "虎嗅"
    },
    {
        "title": "能源市场",
        "desc": "封锁波斯湾，石油天然气乱成一锅粥，或面临史上最大石油中断",
        "url": "https://www.huxiu.com/article/4840330.html",
        "source": "虎嗅"
    },
    {
        "title": "基建投资",
        "desc": "7 万亿投资，超级大基建来了",
        "url": "https://www.huxiu.com/article/4840646.html",
        "source": "虎嗅·国民经略"
    },
]

DEEP_READS = [
    {
        "title": "全民装虾，一戳就破的 AI 幻觉",
        "desc": "对 AI 热潮的理性思考",
        "url": "https://www.huxiu.com/article/4840567.html",
        "source": "虎嗅"
    },
    {
        "title": "阿里能从林俊旸时刻学到什么",
        "desc": "阿里战略反思",
        "url": "https://www.huxiu.com/article/4840193.html",
        "source": "虎嗅"
    },
    {
        "title": "原油失控？更大风暴正在逼近",
        "desc": "能源市场分析",
        "url": "https://www.huxiu.com/article/4840177.html",
        "source": "虎嗅·格隆"
    },
]

def fetch_article_summary(url):
    """抓取文章并生成精简摘要"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取文章标题
        title_tag = soup.find('h1', class_='article-title') or soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ""
        
        # 提取文章摘要/导语
        summary = ""
        # 尝试找摘要
        summary_tag = soup.find('div', class_='article-summary') or soup.find('meta', attrs={'name': 'description'})
        if summary_tag:
            summary = summary_tag.get('content', '') or summary_tag.get_text().strip()
        
        # 如果没找到摘要，尝试找前几段
        if not summary:
            paragraphs = soup.find_all('p')[:3]
            summary = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        # 清理和截断摘要（控制在 80 字以内）
        summary = re.sub(r'\s+', ' ', summary).strip()
        if len(summary) > 80:
            summary = summary[:77] + "..."
        
        return summary if summary else None
        
    except Exception as e:
        print(f"抓取失败 {url}: {e}")
        return None

def generate_ai_summary(title, desc, url):
    """基于标题和描述生成 AI 精简总结（模拟）"""
    # 实际部署时可以调用 AI API 生成更智能的摘要
    # 这里使用规则生成
    
    summaries = {
        "腾讯版小龙虾爆火": "💡 腾讯推出 AI 助手引发热议，因用户过多导致服务不稳定。AI 助手集成多平台是趋势，但需做好容量规划。",
        "AI 短剧霍去病辟谣": "💡 网传 3000 元 80 集 AI 短剧被从业者辟谣。AI 生成视频仍在早期，警惕过度炒作。",
        "智能经济新形态": "💡 AI 首次写入政府工作报告，上升为国家战略。政策红利将加速 AI 在各行业落地。",
        "阿里字节死磕昔日赛道": "💡 两大巨头重新关注曾被看好的赛道。互联网竞争进入新阶段，存量市场博弈加剧。",
        "OPPO 一加宣布涨价": "💡 手机厂商集体涨价，成本压力传导至消费端。2026 年手机市场或迎来价格普涨。",
        "B 站成巨头香饽饽": "💡 B 站扭亏为盈后价值重估。内容社区 + 商业化平衡是关键，巨头争夺用户时长。",
        "中国医疗 AI 战事": "💡 医疗 AI 十年发展从 To B 转向 To C。直接服务患者的模式更易商业化。",
        "Agent 安全花钱": "💡 AI 代理支付安全成新焦点。随着 AI 自主决策增多，资金安全风险需重视。",
        "人人都在装龙虾": "💡 AI Agent 热潮下的理性思考。技术炒作周期中，需区分真实价值与泡沫。",
    }
    
    # 尝试匹配预定义摘要
    for key, summary in summaries.items():
        if key in title:
            return summary
    
    # 默认返回描述 + 点评
    return f"💡 {desc} _（点击链接阅读原文）_"

def format_news_item(item, include_summary=True):
    """格式化单条新闻"""
    summary = ""
    if include_summary:
        summary = generate_ai_summary(item["title"], item["desc"], item["url"])
    
    return f"""- **{item["title"]}** - {item["desc"]} [🔗]({item["url"]}) _来源：{item["source"]}_  
  📝 {summary}"""

def generate_report():
    """生成完整日报"""
    
    # 按分类分组新闻
    categories = {}
    for item in NEWS_ITEMS:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # 生成 Markdown 报告
    report = f"""# 🤖 AI/科技日报 - {DATE}

_每日热点精选 · 把握科技脉搏_

---

## 🔥 今日头条
"""
    
    # 按分类输出
    for cat_name, items in categories.items():
        report += f"\n### {cat_name}\n\n"
        for item in items:
            report += format_news_item(item) + "\n\n"
    
    # 行业观察
    report += """
---

## 📊 行业观察

"""
    for item in INDUSTRY_NEWS:
        summary = generate_ai_summary(item["title"], item["desc"], item["url"])
        report += f"""- **{item["title"]}** - {item["desc"]} [🔗]({item["url"]}) _来源：{item["source"]}_  
  📝 {summary}

"""
    
    # 深度推荐
    report += """
---

## 💡 深度推荐

"""
    for i, item in enumerate(DEEP_READS, 1):
        summary = generate_ai_summary(item["title"], item["desc"], item["url"])
        report += f"""{i}. **{item["title"]}** - {item["desc"]} [🔗]({item["url"]}) _来源：{item["source"]}_  
   📝 {summary}

"""
    
    # 结尾
    report += f"""
---

## 📅 明日关注

- 科技巨头财报季
- AI 政策新动向
- 新能源市场变化

---

_数据来源：虎嗅、36Kr、晚点等科技媒体_
_生成时间：{TIME}_

---
**💬 互动**：回复"详细"获取某条新闻深度解读，回复"添加"自定义关注领域
"""
    
    return report

if __name__ == "__main__":
    print(generate_report())
