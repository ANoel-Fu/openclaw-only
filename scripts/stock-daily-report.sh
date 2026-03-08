#!/bin/bash
# 每日股票/基金日报脚本
# 执行时间：每个交易日早上 9:00

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/stock-daily-$(date +%Y%m%d).log"
REPORT_FILE="$WORKSPACE/logs/stock-report-$(date +%Y%m%d).md"

mkdir -p "$WORKSPACE/logs"

echo "=== 股票日报开始 $(date) ===" >> "$LOG_FILE"

# 生成日报内容
REPORT_DATE=$(date +%Y年%m月%d日)

# 获取 A 股市场概览（使用 akshare）
python3 << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/new-akshare-stock')

try:
    import akshare as ak
    import pandas as pd
    
    # 获取 A 股实时行情
    print("📊 A 股市场概览\n")
    
    # 主要指数
    indices = [
        ("000001", "上证指数"),
        ("399001", "深证成指"),
        ("399006", "创业板指"),
        ("000016", "上证 50"),
        ("000300", "沪深 300"),
    ]
    
    for code, name in indices:
        try:
            df = ak.stock_zh_a_spot_em()
            if df is not None and not df.empty:
                stock_data = df[df['代码'] == code]
                if not stock_data.empty:
                    row = stock_data.iloc[0]
                    latest = float(row['最新价']) if pd.notna(row['最新价']) else 0
                    change = float(row['涨跌幅']) if pd.notna(row['涨跌幅']) else 0
                    print(f"{name} ({code}): {latest:.2f}  {change:+.2f}%")
        except Exception as e:
            print(f"{name}: 数据获取失败")
    
    print("\n" + "="*50 + "\n")
    
    # 热门板块
    print("🔥 热门板块\n")
    try:
        board_df = ak.stock_board_industry_name_em()
        if board_df is not None and not board_df.empty:
            top_gainers = board_df.nlargest(5, '涨跌幅')
            for _, row in top_gainers.iterrows():
                print(f"{row['板块名称']}: {row['涨跌幅']:+.2f}%")
    except Exception as e:
        print("板块数据获取失败")
    
    print("\n" + "="*50 + "\n")
    
    # 资金流向
    print("💰 资金流向\n")
    try:
        fund_df = ak.stock_individual_fund_flow_rank(indicator="今日")
        if fund_df is not None and not fund_df.empty:
            print("主力净流入前 5:")
            for _, row in fund_df.head(5).iterrows():
                print(f"{row['名称']}: {row['主力净流入-净额']}万")
    except Exception as e:
        print("资金流向数据获取失败")
        
except Exception as e:
    print(f"Error: {e}")

PYTHON_SCRIPT

# 保存报告到文件
python3 << 'PYTHON_SAVE' > "$REPORT_FILE"
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/new-akshare-stock')

try:
    import akshare as ak
    import pandas as pd
    from datetime import datetime
    
    report_date = datetime.now().strftime("%Y年%m月%d日")
    
    print(f"# 📈 每日股票/基金日报\n")
    print(f"_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
    print(f"---\n")
    
    # 主要指数
    print("## 📊 市场指数\n")
    
    indices = [
        ("000001", "上证指数"),
        ("399001", "深证成指"),
        ("399006", "创业板指"),
        ("000016", "上证 50"),
        ("000300", "沪深 300"),
    ]
    
    print("| 指数 | 代码 | 最新价 | 涨跌幅 |")
    print("|------|------|--------|--------|")
    
    try:
        df = ak.stock_zh_a_spot_em()
        if df is not None and not df.empty:
            for code, name in indices:
                stock_data = df[df['代码'] == code]
                if not stock_data.empty:
                    row = stock_data.iloc[0]
                    latest = float(row['最新价']) if pd.notna(row['最新价']) else 0
                    change = float(row['涨跌幅']) if pd.notna(row['涨跌幅']) else 0
                    change_str = f"{change:+.2f}%"
                    print(f"| {name} | {code} | {latest:.2f} | {change_str} |")
    except Exception as e:
        print("| 数据获取失败 | - | - | - |")
    
    print("\n---\n")
    
    # 热门板块
    print("## 🔥 热门板块\n")
    
    try:
        board_df = ak.stock_board_industry_name_em()
        if board_df is not None and not board_df.empty:
            top_gainers = board_df.nlargest(10, '涨跌幅')
            print("| 排名 | 板块 | 涨跌幅 | 领涨股 |")
            print("|------|------|--------|--------|")
            for i, (_, row) in enumerate(top_gainers.iterrows(), 1):
                print(f"| {i} | {row['板块名称']} | {row['涨跌幅']:+.2f}% | {row.get('领涨股', '-')} |")
    except Exception as e:
        print("板块数据获取失败")
    
    print("\n---\n")
    
    # 资金流向
    print("## 💰 主力资金流向\n")
    
    try:
        fund_df = ak.stock_individual_fund_flow_rank(indicator="今日")
        if fund_df is not None and not fund_df.empty:
            print("### 主力净流入前 10\n")
            print("| 排名 | 股票 | 主力净流入 (万) |")
            print("|------|------|----------------|")
            for i, (_, row) in enumerate(fund_df.head(10).iterrows(), 1):
                net = row.get('主力净流入 - 净额', 0)
                print(f"| {i} | {row['名称']} | {net:,.0f} |")
    except Exception as e:
        print("资金流向数据获取失败")
    
    print("\n---\n")
    
    # 基金排行
    print("## 📈 基金排行\n")
    
    try:
        fund_df = ak.fund_open_fund_rank_em()
        if fund_df is not None and not fund_df.empty:
            top_funds = fund_df.nlargest(10, '日增长率')
            print("| 排名 | 基金代码 | 基金名称 | 日增长率 |")
            print("|------|----------|----------|----------|")
            for i, (_, row) in enumerate(top_funds.iterrows(), 1):
                print(f"| {i} | {row['基金代码']} | {row['基金名称']} | {row['日增长率']:+.2f}% |")
    except Exception as e:
        print("基金数据获取失败")
    
    print("\n---\n")
    print("_⚠️ 数据仅供参考，不构成投资建议_")
    
except Exception as e:
    print(f"# ❌ 报告生成失败\n\n错误：{e}")

PYTHON_SAVE

echo "报告已保存到：$REPORT_FILE" >> "$LOG_FILE"
echo "=== 股票日报结束 $(date) ===" >> "$LOG_FILE"

# 通过 OpenClaw 发送报告到飞书
if [ -f "$REPORT_FILE" ]; then
    # 使用 message 工具发送报告
    cd "$WORKSPACE"
    cat "$REPORT_FILE" | head -50
fi
