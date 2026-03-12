#!/bin/bash
# 最终测试 - 完全模拟 cron 环境

# 模拟 cron 的最小 PATH
export PATH="/usr/bin:/bin"

echo "=== 模拟真实 Cron 环境 ==="
echo "PATH: $PATH"
echo "时间：$(date)"
echo ""

# 测试 Java 日报（脚本内部会设置 PATH）
echo "=== 测试 Java 日报脚本 ==="
cd /root/.openclaw/workspace
TZ=Asia/Shanghai bash scripts/java-daily-report.sh > /tmp/java-test.log 2>&1
JAVA_EXIT=$?
if [ $JAVA_EXIT -eq 0 ]; then
    echo "✅ Java 日报执行成功"
    tail -3 /tmp/java-test.log
else
    echo "❌ Java 日报执行失败"
    cat /tmp/java-test.log
fi
echo ""

# 测试科技日报（脚本内部会设置 PATH）
echo "=== 测试科技日报脚本 ==="
cd /root/.openclaw/workspace
bash scripts/ai-tech-daily.sh > /tmp/tech-test.log 2>&1
TECH_EXIT=$?
if [ $TECH_EXIT -eq 0 ]; then
    echo "✅ 科技日报执行成功"
    tail -3 /tmp/tech-test.log
else
    echo "❌ 科技日报执行失败"
    cat /tmp/tech-test.log
fi
echo ""

echo "=== 最终结果 ==="
if [ $JAVA_EXIT -eq 0 ] && [ $TECH_EXIT -eq 0 ]; then
    echo "✅✅✅ 所有测试通过！明天会正常推送！"
else
    echo "❌ 有失败，需要修复"
fi
