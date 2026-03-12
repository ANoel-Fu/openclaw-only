#!/bin/bash
# 模拟真实 cron 环境（最小 PATH）

# cron 的典型 PATH 非常精简
export PATH="/usr/local/bin:/usr/bin:/bin"

echo "=== 模拟真实 Cron 环境（最小 PATH）==="
echo "PATH: $PATH"
echo ""

# 测试 openclaw 命令是否能找到
echo "测试 openclaw 命令..."
which openclaw 2>/dev/null && echo "✅ 找到 openclaw" || echo "❌ 找不到 openclaw（正常，需要用完整路径）"

# 测试使用完整路径
echo ""
echo "测试使用完整路径..."
/root/.local/share/pnpm/openclaw --version 2>&1 | head -1

echo ""
echo "✅ 测试完成 - 脚本使用完整路径，不受 PATH 影响"
