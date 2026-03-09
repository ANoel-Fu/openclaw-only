#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股/基金日报 - 轻量版（同花顺数据源）
运行时间：每个交易日 9:30 AM
"""

import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import re

# 自选股列表（可自定义修改）
WATCHLIST = [
    "600519",  # 贵州茅台
    "000001",  # 平安银行
    "300750",  # 宁德时代
    "600036",  # 招商银行
    "002594",  # 比亚迪
    "601318",  # 中国平安
]

# 基金
FUND_LIST = [
    "513050",  # 中概互联 ETF
    "161725",  # 招商中证白酒
    "512690",  # 鹏华中证酒 ETF
    "512880",  # 证券 ETF
]

def fetch_stock_info(code):
    """从同花顺获取股票行情"""
    try:
        url = f"https://stockpage.10jqka.com.cn/{code}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://q.10jqka.com.cn/"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = "utf-8"
        
        # 简单解析页面关键数据
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 尝试提取价格信息
        price_elem = soup.find("span", class_="price") or soup.find("strong")
        change_elem = soup.find("span", class_="change")
        
        if price_elem:
            price = price_elem.get_text().strip()
            change = change_elem.get_text().strip() if change_elem else "N/A"
            return {"price": price, "change": change, "status": "OK"}
        else:
            return {"status": "PARSE_ERROR"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)}

def fetch_fund_info(code):
    """从天天基金获取基金净值"""
    try:
        url = f"http://fundgz.1234567.com.cn/js/{code}.js"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "http://fund.eastmoney.com/"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = "utf-8"
        
        # 解析 JSONP 响应
        match = re.search(r'jsonpgz\((.+)\)', resp.text)
        if match:
            data = json.loads(match.group(1))
            return {
                "price": data.get("gsz", "N/A"),
                "change": data.get("gszzl", "N/A"),
                "name": data.get("name", ""),
                "status": "OK"
            }
        return {"status": "PARSE_ERROR"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)}

def generate_report():
    """生成日报"""
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = []
    report.append("╔══════════════════════════════════════════════════════════╗")
    report.append(f"║       A 股/基金投资日报 | {today}                        ║")
    report.append("╚══════════════════════════════════════════════════════════╝")
    report.append("")
    
    # 股票部分
    report.append("📈 自选股行情")
    report.append("─" * 60)
    for code in WATCHLIST:
        data = fetch_stock_info(code)
        if data["status"] == "OK":
            report.append(f"  {code}: ¥{data['price']} ({data['change']})")
        else:
            report.append(f"  {code}: 数据获取失败")
    report.append("")
    
    # 基金部分
    report.append("💰 基金净值估算")
    report.append("─" * 60)
    for code in FUND_LIST:
        data = fetch_fund_info(code)
        if data["status"] == "OK":
            report.append(f"  {data.get('name', code)} ({code}): {data['price']} ({data['change']}%)")
        else:
            report.append(f"  {code}: 数据获取失败")
    report.append("")
    
    report.append("─" * 60)
    report.append("数据来源：同花顺 / 天天基金网")
    report.append("免责声明：数据仅供参考，不构成投资建议")
    report.append("=" * 60)
    
    return "\n".join(report)

if __name__ == "__main__":
    print(generate_report())
