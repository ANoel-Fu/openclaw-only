#!/bin/bash
# 测试脚本 - 模拟 cron 环境执行日报任务

echo "=== 测试 Cron 环境 ==="
echo "PATH: $PATH"
echo "当前时间：$(date)"
echo ""

echo "=== 测试 Java 日报脚本 ==="
cd /root/.openclaw/workspace
TZ=Asia/Shanghai bash scripts/java-daily-report.sh
JAVA_EXIT=$?
echo "Java 日报退出码：$JAVA_EXIT"
echo ""

echo "=== 测试科技日报脚本 ==="
cd /root/.openclaw/workspace
bash scripts/ai-tech-daily.sh
TECH_EXIT=$?
echo "科技日报退出码：$TECH_EXIT"
echo ""

echo "=== 测试结果 ==="
if [ $JAVA_EXIT -eq 0 ] && [ $TECH_EXIT -eq 0 ]; then
    echo "✅ 所有脚本测试通过！"
else
    echo "❌ 有脚本执行失败，请检查日志"
fi
