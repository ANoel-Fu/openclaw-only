#!/bin/bash
# A 股/基金日报 - 定时任务脚本
# 运行时间：每个交易日 9:30 AM

cd /root/.openclaw/workspace

# 生成日报
python3 scripts/daily-stock-report.py > /tmp/daily-report-$(date +%Y%m%d).txt 2>&1

# 通过飞书发送（使用 OpenClaw message 工具）
REPORT=$(cat /tmp/daily-report-$(date +%Y%m%d).txt)

# 发送到当前会话
echo "$REPORT"
