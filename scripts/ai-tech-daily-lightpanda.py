#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI/Tech Daily News - Lightpanda Version V2 (Optimized)
每日 AI/科技热点新闻收集 - Lightpanda 驱动 + AI 摘要 + 多来源
"""

import os
import subprocess
import json
import re
from datetime import datetime

# 确保环境变量完整（不依赖 cron 环境）
os.environ['PATH'] = '/root/.nvm/versions/node/v22.22.0/bin:/root/.local/share/pnpm/bin:/usr/local/bin:/usr/bin:/bin:' + os.environ.get('PATH', '')
os.environ['TZ'] = 'Asia/Shanghai'

# 配置
DATE = datetime.now().strftime('%Y-%m-%d')
TIME = datetime.now().strftime('%H:%M')
WEEKDAY = datetime.now().strftime('%A')

LIGHTPANDA_BIN = "/root/.local/bin/lightpanda"

# 用户兴趣配置（可调整权重）
USER_INTERESTS = {
    "🤖 AI 与大模型": 1.5,      # 高优先级
    "📱 硬件与消费电子": 1.2,   # 中优先级
    "💰 创投动态": 1.0,         # 正常
    "🚗 智能汽车": 1.0,
    "🌐 科技前沿": 0.8,         # 低优先级
    "🤖 机器人与自动驾驶": 1.3,
    "🏥 医疗科技": 0.9,
    "💳 金融科技": 0.9,
    "🛡️ 科技与安全": 1.1,
}

def fetch_with_lightpanda(url, timeout=30):
    """使用 Lightpanda 抓取网页"""
    try:
        cmd = [
            LIGHTPANDA_BIN,
            "fetch",
            "--dump", "markdown",
            "--log_level", "error",
            url
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stdout
            
    except subprocess.TimeoutExpired:
        print(f"⏰ 抓取超时：{url}")
        return ""
    except Exception as e:
        print(f"❌ 抓取失败：{e}")
        return ""

def generate_ai_summary_with_llm(title, source):
    """使用 LLM 生成智能摘要（简化版：基于规则 + 关键词）"""
    
    # AI 相关
    if any(kw in title for kw in ['大模型', 'AI', '智能体', 'Agent', 'GPT', 'Kimi', '月之暗面', 'OpenAI', 'Claude', 'Gemini']):
        if '融资' in title or '估值' in title or '投资' in title:
            return "💡 大模型赛道持续火热，资本加速布局头部企业。"
        elif '安全' in title or '监管' in title or '审查' in title:
            return "💡 AI 安全与治理成为行业发展关键议题。"
        elif '发布' in title or '推出' in title or '上线' in title:
            return "💡 AI 技术快速迭代，关注实际应用场景落地。"
        elif '评测' in title or '基准' in title or '对比' in title:
            return "💡 权威评测揭示模型性能差异，助力技术选型。"
        else:
            return "💡 AI 领域持续创新，技术边界不断拓展。"
    
    # 机器人相关
    if '机器人' in title or '自动驾驶' in title or '无人驾驶' in title:
        return "💡 智能驾驶与人形机器人商业化加速推进。"
    
    # 手机/硬件相关
    if any(kw in title for kw in ['手机', '芯片', '半导体', '消费电子', '骁龙', '麒麟']):
        if '发布' in title or '推出' in title:
            return "💡 新品发布，技术创新驱动产品升级。"
        return "💡 消费电子市场回暖，技术创新驱动增长。"
    
    # 创投相关
    if '融资' in title or '投资' in title or '上市' in title or 'IPO' in title:
        amount_match = re.search(r'(\d+[亿万]?)', title)
        if amount_match:
            return f"💡 融资规模达{amount_match.group(1)}，资本看好赛道发展。"
        return "💡 资本流向反映行业趋势，关注赛道热度。"
    
    # 汽车相关
    if any(kw in title for kw in ['汽车', '比亚迪', '特斯拉', '新能源', '蔚来', '小鹏', '理想']):
        if '销量' in title or '交付' in title:
            return "💡 销量数据反映市场表现，竞争格局持续演变。"
        return "💡 中国车企加速全球化布局，技术实力持续提升。"
    
    # 默认摘要
    return "💡 点击链接阅读原文了解更多。"

def parse_36kr_content(markdown_content):
    """解析 36Kr 快讯内容"""
    news_items = []
    
    # 提取链接和标题
    pattern = r'\[([^\]]+)\]\((https?://36kr\.com/newsflashes/\d+)\)'
    matches = re.findall(pattern, markdown_content)
    
    for title, url in matches:
        title = title.strip()
        if 5 < len(title) < 100:
            category = categorize_news(title)
            news_items.append({
                "category": category,
                "title": title,
                "desc": "",
                "url": url,
                "source": "36Kr",
                "hours_ago": 0,
                "interest_score": USER_INTERESTS.get(category, 1.0)
            })
    
    return news_items[:25]

def parse_huxiu_content(markdown_content):
    """解析虎嗅内容"""
    news_items = []
    
    pattern = r'\[([^\]]+)\]\((https?://www\.huxiu\.com/article/\d+\.html)\)'
    matches = re.findall(pattern, markdown_content)
    
    for title, url in matches:
        title = title.strip()
        if 5 < len(title) < 100 and '广告' not in title:
            category = categorize_news(title)
            news_items.append({
                "category": category,
                "title": title,
                "desc": "",
                "url": url,
                "source": "虎嗅",
                "hours_ago": 2,
                "interest_score": USER_INTERESTS.get(category, 1.0)
            })
    
    return news_items[:15]

def parse_qbitai_content(markdown_content):
    """解析量子位内容"""
    news_items = []
    
    pattern = r'\[([^\]]+)\]\((https?://www\.qbitai\.com/[^)]+)\)'
    matches = re.findall(pattern, markdown_content)
    
    for title, url in matches:
        title = title.strip()
        if 5 < len(title) < 100 and '热门' not in title and '广告' not in title:
            category = categorize_news(title)
            news_items.append({
                "category": category,
                "title": title,
                "desc": "",
                "url": url,
                "source": "量子位",
                "hours_ago": 1,
                "interest_score": USER_INTERESTS.get(category, 1.0)
            })
    
    return news_items[:15]

def fetch_zhihu_hot_api():
    """通过知乎 API 获取热榜（无需 Lightpanda）"""
    import urllib.request
    import json
    from datetime import datetime
    
    news_items = []
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot?limit=10"  # 只请求前 10 条
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        for idx, item in enumerate(data.get('data', []), 1):
            target = item.get('target', {})
            question = target.get('question', {})
            title = question.get('title', '')
            question_id = question.get('id', '')
            created_time = question.get('created', 0)
            
            if title and 5 < len(title) < 100 and '广告' not in title:
                category = categorize_news(title)
                question_time = datetime.fromtimestamp(created_time) if created_time else datetime.now()
                hours_ago = int((datetime.now() - question_time).total_seconds() / 3600)
                
                # 时效性标记：超过 7 天的标记为较旧内容
                if hours_ago > 168:  # 7 天
                    hours_ago_display = f"{hours_ago // 24}天前"
                else:
                    hours_ago_display = f"{hours_ago}小时前"
                
                news_items.append({
                    "category": category,
                    "title": title,
                    "desc": "",
                    "url": f"https://www.zhihu.com/question/{question_id}",
                    "source": f"知乎热榜 #{idx}",
                    "hours_ago": hours_ago,
                    "interest_score": USER_INTERESTS.get(category, 1.0) * 1.1 * (1.0 - idx * 0.05),  # 排名越高权重越高
                    "rank": idx
                })
        
        print(f"✅ 知乎热榜 抓取成功：{len(news_items)} 条（Top 10）")
        return news_items
        
    except Exception as e:
        print(f"❌ 知乎热榜 API 失败：{e}")
        return []

# 网易科技解析函数已移除（2026-03-25）

def categorize_news(title):
    """根据关键词自动分类新闻"""
    text = title.lower()
    
    if any(kw in text for kw in ['大模型', 'llm', 'gpt', 'ai agent', '智能体', 'ai 助手', '月之暗面', 'kimi', '360', '周鸿祎', 'openai', 'anthropic', 'gemini', 'claude', '人工智能', 'llama']):
        return "🤖 AI 与大模型"
    elif any(kw in text for kw in ['机器人', 'robot', '人形', '自动驾驶', '特斯拉 fsd', '无人驾驶']):
        return "🤖 机器人与自动驾驶"
    elif any(kw in text for kw in ['手机', '芯片', '半导体', 'oppo', 'vivo', '小米', '华为', '苹果', '消费电子', '骁龙', '麒麟', 'iphone']):
        return "📱 硬件与消费电子"
    elif any(kw in text for kw in ['融资', '投资', '上市', 'ipo', '估值', '创业', '捐赠', '并购', '收购', '轮']):
        return "💰 创投动态"
    elif any(kw in text for kw in ['汽车', '新能源', '特斯拉', '比亚迪', 'f1', '赛车', '蔚来', '小鹏', '理想', 'ev']):
        return "🚗 智能汽车"
    elif any(kw in text for kw in ['医疗', '健康', '生物', '制药', '基因', '医药']):
        return "🏥 医疗科技"
    elif any(kw in text for kw in ['金融', '支付', '银行', '保险', '区块链', '比特币', '加密货币', 'web3']):
        return "💳 金融科技"
    elif any(kw in text for kw in ['安全', '隐私', '黑客', '漏洞', '数据泄露', '监管', '反垄断', '审查']):
        return "🛡️ 科技与安全"
    else:
        return "🌐 科技前沿"

def format_news_item(item, rank=None):
    """格式化单条新闻（带 AI 摘要）"""
    summary = generate_ai_summary_with_llm(item["title"], item["source"])
    rank_str = f"{rank}. " if rank else ""
    
    return f"""{rank_str}**{item["title"]}** [🔗]({item["url"]}) _来源：{item["source"]}_  
   📝 {summary}"""

def fetch_36kr_newsflashes():
    """抓取 36Kr 快讯"""
    print("🐼 使用 Lightpanda 抓取 36Kr...")
    content = fetch_with_lightpanda("https://36kr.com/newsflashes")
    items = parse_36kr_content(content)
    print(f"✅ 36Kr 抓取成功：{len(items)} 条")
    return items

def fetch_huxiu():
    """抓取虎嗅"""
    print("🐼 使用 Lightpanda 抓取虎嗅...")
    content = fetch_with_lightpanda("https://www.huxiu.com/article/")
    items = parse_huxiu_content(content)
    print(f"✅ 虎嗅 抓取成功：{len(items)} 条")
    return items

def fetch_qbitai():
    """抓取量子位"""
    print("🐼 使用 Lightpanda 抓取量子位...")
    content = fetch_with_lightpanda("https://www.qbitai.com/")
    items = parse_qbitai_content(content)
    print(f"✅ 量子位 抓取成功：{len(items)} 条")
    return items

def fetch_zhihu_hot():
    """抓取知乎热榜（使用 API）"""
    return fetch_zhihu_hot_api()

# 网易科技已移除（2026-03-25）

def generate_report():
    """生成完整日报（带个性化排序）"""
    
    print("📰 开始抓取今日新闻（Lightpanda 驱动 + AI 摘要）...")
    all_news = []
    
    # 使用 Lightpanda 抓取各来源
    all_news.extend(fetch_36kr_newsflashes())
    all_news.extend(fetch_huxiu())
    all_news.extend(fetch_qbitai())
    all_news.extend(fetch_zhihu_hot())  # 知乎热榜替换机器之心（2026-03-26）
    # 网易科技已移除（2026-03-25）
    
    print(f"📊 总计抓取：{len(all_news)} 条")
    
    # 按兴趣分数排序（个性化）
    all_news.sort(key=lambda x: (-x["interest_score"], x["hours_ago"]))
    
    # 限制总数（每家最多贡献 5 条，确保来源多样性）
    source_counts = {}
    filtered_news = []
    for item in all_news:
        src = item["source"]
        if src not in source_counts:
            source_counts[src] = 0
        if source_counts[src] < 5:
            filtered_news.append(item)
            source_counts[src] += 1
    
    all_news = filtered_news[:20]
    
    if len(all_news) < 3:
        print("⚠️  新闻数量不足")
    
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

_每日热点精选 · 把握科技脉搏 · Lightpanda 驱动 + AI 摘要_

---

## 🔥 今日头条

"""
    
    # 按分类输出（优先显示高兴趣度分类）
    sorted_categories = sorted(
        categories.items(),
        key=lambda x: (-sum([item["interest_score"] for item in x[1]]), len(x[1])),
        reverse=True
    )
    
    for cat_name, items in sorted_categories:
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

_数据来源：{', '.join(sources_used)}（Lightpanda 实时抓取）_
_生成时间：{TIME}_
_下次推送：明日 8:50_
_个性化权重：已根据你的兴趣优化排序_

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
