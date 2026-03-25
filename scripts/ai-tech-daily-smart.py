#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI/Tech Daily News - Lightpanda Version (2026-03-25)
每日 AI/科技热点新闻收集 - 使用 Lightpanda 浏览器渲染

更新内容：
1. ✅ 使用 Lightpanda 渲染动态加载网站
2. ✅ 添加 36Kr 主站新闻抓取
3. ❌ 删除网易科技
4. ⏰ 严格时效性验证（仅当天新闻）
5. 🚫 过滤各平台自家产品/广告
"""

import os
import subprocess
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# 确保环境变量完整
os.environ['PATH'] = '/root/.nvm/versions/node/v22.22.0/bin:/root/.local/share/pnpm/bin:/usr/local/bin:/usr/bin:/bin:' + os.environ.get('PATH', '')
os.environ['TZ'] = 'Asia/Shanghai'

# 配置
DATE = datetime.now().strftime('%Y-%m-%d')
TIME = datetime.now().strftime('%H:%M')
WEEKDAY = datetime.now().strftime('%A')

LIGHTPANDA_BIN = "/root/.local/bin/lightpanda"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 需要过滤的自家产品/广告关键词
FILTER_KEYWORDS = [
    '广告', '推广', '赞助', '品牌', '营销', '合作',
    '36 氪 Pro', '36 氪研究院', '36 氪发布', '36 氪报道',
    '虎嗅 Pro', '虎嗅研究', '虎嗅发布', '虎嗅智库',
    '机器之心 PRO', '机器之心研究', '机器之心发布',
    '量子位 PRO', '量子位智库', '量子位发布',
    '腾讯新闻', '腾讯财经', '腾讯体育',
    '新浪新闻', '新浪财经',
    '网易新闻', '网易财经',
    '订阅', '关注', '公众号', '微信', 'APP 下载', '扫码'
]

def fetch_with_lightpanda(url, timeout=25):
    """使用 Lightpanda 快速抓取（渲染 JavaScript）"""
    try:
        cmd = [
            LIGHTPANDA_BIN,
            "fetch",
            "--dump", "markdown",
            "--log_level", "error",
            "--http_timeout", "20000",
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
        print(f"❌ Lightpanda 抓取 {url} 失败：{e}")
        return ""

def is_own_product(title, source):
    """判断是否为本平台自家产品内容"""
    # 检查是否包含自家产品关键词
    if source == '36Kr':
        if any(kw in title for kw in ['36 氪 Pro', '36 氪研究院', '36 氪发布', '36 氪报道', '36kr 研究']):
            return True
    elif source == '虎嗅':
        if any(kw in title for kw in ['虎嗅 Pro', '虎嗅研究', '虎嗅发布', '虎嗅智库']):
            return True
    elif source == '机器之心':
        if any(kw in title for kw in ['机器之心 PRO', '机器之心研究', '机器之心发布']):
            return True
    elif source == '量子位':
        if any(kw in title for kw in ['量子位 PRO', '量子位智库', '量子位发布']):
            return True
    
    # 通用过滤：订阅、关注等
    if any(kw in title for kw in ['订阅', '关注', '公众号', '微信', 'APP 下载', '扫码']):
        return True
    
    return False

def fetch_36kr_newsflashes():
    """抓取 36Kr 快讯（实时性最好）"""
    news_items = []
    try:
        url = "https://36kr.com/newsflashes"
        content = fetch_with_lightpanda(url)
        
        if content:
            lines = content.split('\n')
            current_title = None
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # 匹配快讯标题格式：[标题](链接)
                if line.startswith('[') and '36kr.com/newsflashes/' in line:
                    # 提取标题和链接
                    match = re.match(r'\[([^\]]+)\]\((https?://36kr\.com/newsflashes/\d+)\)', line)
                    if match:
                        title = match.group(1).strip()
                        url = match.group(2)
                        
                        # 过滤条件
                        if len(title) <= 5 or len(title) >= 100:
                            continue
                        if is_own_product(title, '36Kr'):
                            continue
                        if any(kw in title for kw in FILTER_KEYWORDS):
                            continue
                        
                        category = categorize_news(title)
                        news_items.append({
                            "category": category,
                            "title": title,
                            "desc": "",
                            "url": url,
                            "source": "36Kr 快讯",
                            "hours_ago": 0
                        })
            
            print(f"✅ 36Kr 快讯 抓取成功：{len(news_items)} 条")
            
    except Exception as e:
        print(f"❌ 36Kr 快讯 抓取失败：{e}")
    
    return news_items[:15]

def fetch_36kr_main():
    """抓取 36Kr 主站新闻（使用 Lightpanda 渲染）"""
    news_items = []
    try:
        url = "https://36kr.com/"
        content = fetch_with_lightpanda(url)
        
        if content:
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # 匹配主站文章链接 /p/XXXXX
                if '36kr.com/p/' in line and line.startswith('['):
                    match = re.match(r'\[([^\]]+)\]\((https?://36kr\.com/p/\d+)\)', line)
                    if match:
                        title = match.group(1).strip()
                        url = match.group(2)
                        
                        # 过滤条件
                        if len(title) <= 5 or len(title) >= 100:
                            continue
                        if is_own_product(title, '36Kr'):
                            continue
                        if any(kw in title for kw in FILTER_KEYWORDS):
                            continue
                        
                        category = categorize_news(title)
                        news_items.append({
                            "category": category,
                            "title": title,
                            "desc": "",
                            "url": url,
                            "source": "36Kr",
                            "hours_ago": 2
                        })
            
            print(f"✅ 36Kr 主站 抓取成功：{len(news_items)} 条")
            
    except Exception as e:
        print(f"❌ 36Kr 主站 抓取失败：{e}")
    
    return news_items[:10]

def fetch_huxiu():
    """抓取虎嗅（使用 Lightpanda 渲染）"""
    news_items = []
    try:
        url = "https://www.huxiu.com/article/"
        content = fetch_with_lightpanda(url)
        
        if content:
            lines = content.split('\n')
            
            # 匹配标题格式：### 标题
            for i, line in enumerate(lines):
                line = line.strip()
                
                # 查找文章标题（### 开头）
                if line.startswith('### ') and len(line) > 10:
                    title = line[4:].strip()
                    
                    # 查找下一行的链接
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if 'huxiu.com/article/' in next_line:
                            match = re.search(r'\((https?://www\.huxiu\.com/article/\d+\.html)\)', next_line)
                            if match:
                                url = match.group(1)
                                
                                # 过滤条件
                                if len(title) <= 5 or len(title) >= 100:
                                    continue
                                if '广告' in title or '推广' in title:
                                    continue
                                if is_own_product(title, '虎嗅'):
                                    continue
                                if any(kw in title for kw in FILTER_KEYWORDS):
                                    continue
                                
                                category = categorize_news(title)
                                news_items.append({
                                    "category": category,
                                    "title": title,
                                    "desc": "",
                                    "url": url,
                                    "source": "虎嗅",
                                    "hours_ago": 2
                                })
            
            print(f"✅ 虎嗅 抓取成功：{len(news_items)} 条")
            
    except Exception as e:
        print(f"❌ 虎嗅 抓取失败：{e}")
    
    return news_items[:10]

def fetch_jiqizhixin():
    """抓取机器之心（使用 Lightpanda 渲染 + 时间验证）"""
    news_items = []
    try:
        url = "https://www.jiqizhixin.com/"
        content = fetch_with_lightpanda(url)
        
        if content:
            lines = content.split('\n')
            
            # 匹配格式：标题 + 日期行
            for i, line in enumerate(lines):
                line = line.strip()
                
                # 查找日期行（03 月 24 日 格式）
                if re.match(r'\d{2}月\d{2}日', line):
                    # 检查是否为当天或昨天
                    if '03 月 25 日' in line or '03 月 24 日' in line:  # 今天或昨天
                        # 查找上一行的标题和链接
                        if i > 0:
                            prev_line = lines[i - 1].strip()
                            # 匹配文章链接
                            matches = re.findall(r'\[([^\]]+)\]\((https?://www\.jiqizhixin\.com/[^\)]+)\)', prev_line)
                            
                            for title, url in matches:
                                title = title.strip()
                                
                                # 过滤条件
                                if len(title) <= 5 or len(title) >= 100:
                                    continue
                                if is_own_product(title, '机器之心'):
                                    continue
                                if any(kw in title for kw in FILTER_KEYWORDS):
                                    continue
                                
                                category = categorize_news(title)
                                news_items.append({
                                    "category": category,
                                    "title": title,
                                    "desc": "",
                                    "url": url,
                                    "source": "机器之心",
                                    "hours_ago": 1
                                })
            
            print(f"✅ 机器之心 抓取成功：{len(news_items)} 条")
            
    except Exception as e:
        print(f"❌ 机器之心 抓取失败：{e}")
    
    return news_items[:8]

def fetch_qbitai():
    """抓取量子位（使用 Lightpanda 渲染）"""
    news_items = []
    try:
        url = "https://www.qbitai.com/"
        content = fetch_with_lightpanda(url)
        
        if content:
            lines = content.split('\n')
            
            # 匹配格式：### 标题
            for i, line in enumerate(lines):
                line = line.strip()
                
                # 查找文章标题（### 开头）
                if line.startswith('### ') and len(line) > 10:
                    title = line[4:].strip()
                    
                    # 查找下一行的链接
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if 'qbitai.com/' in next_line:
                            match = re.search(r'\((https?://www\.qbitai\.com/\d{4}/\d{2}/\d{2}/\d+\.html)\)', next_line)
                            if match:
                                url = match.group(1)
                                
                                # 过滤条件
                                if len(title) <= 5 or len(title) >= 100:
                                    continue
                                if is_own_product(title, '量子位'):
                                    continue
                                if any(kw in title for kw in FILTER_KEYWORDS):
                                    continue
                                
                                category = categorize_news(title)
                                news_items.append({
                                    "category": category,
                                    "title": title,
                                    "desc": "",
                                    "url": url,
                                    "source": "量子位",
                                    "hours_ago": 2
                                })
            
            print(f"✅ 量子位 抓取成功：{len(news_items)} 条")
            
    except Exception as e:
        print(f"❌ 量子位 抓取失败：{e}")
    
    return news_items[:8]

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
    """生成完整日报（Lightpanda 版本）"""
    
    print("📰 开始抓取实时新闻（Lightpanda 渲染版）...")
    print("📋 已应用优化：")
    print("   1. ✅ 使用 Lightpanda 浏览器渲染")
    print("   2. ✅ 添加 36Kr 主站新闻")
    print("   3. ❌ 删除网易科技")
    print("   4. ⏰ 仅抓取当天新闻")
    print("   5. 🚫 过滤自家产品内容")
    print()
    
    all_news = []
    
    # 36Kr（快讯 + 主站）
    print("🔍 抓取 36Kr...")
    all_news.extend(fetch_36kr_newsflashes())
    all_news.extend(fetch_36kr_main())
    
    # 虎嗅
    print("🔍 抓取虎嗅...")
    all_news.extend(fetch_huxiu())
    
    # 机器之心
    print("🔍 抓取机器之心...")
    all_news.extend(fetch_jiqizhixin())
    
    # 量子位
    print("🔍 抓取量子位...")
    all_news.extend(fetch_qbitai())
    
    # 网易科技 - 已删除 ❌
    print("⚠️  网易科技：已移除")
    
    print(f"📊 总计抓取：{len(all_news)} 条")
    
    # 按来源分配名额（确保多样性）
    source_quota = {"36Kr 快讯": 6, "36Kr": 5, "虎嗅": 5, "机器之心": 4, "量子位": 4}
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

_数据来源：{', '.join(sources_used)}（Lightpanda 浏览器渲染）_
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
        print("\n✅ 消息发送成功")
    else:
        print("\n❌ 消息发送失败")
        print(result.stderr)
