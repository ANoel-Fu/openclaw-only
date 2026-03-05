#!/bin/bash
# OpenClaw 技能安装脚本
# 用于系统恢复后快速安装所有扩展插件

set -e

echo "🦞 OpenClaw 技能安装脚本"
echo "========================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js 20+"
    exit 1
fi

echo "✅ Node.js 版本：$(node --version)"
echo ""

# 安装 QQ Bot
echo "📦 安装 QQ Bot..."
npm install -g @sliverp/qqbot@latest
echo "✅ QQ Bot 安装完成"
echo ""

# 安装钉钉
echo "📦 安装钉钉插件..."
npm install -g @largezhou/ddingtalk
echo "✅ 钉钉插件安装完成"
echo ""

# 安装企业微信
echo "📦 安装企业微信插件..."
npm install -g @mocrane/wecom
echo "✅ 企业微信插件安装完成"
echo ""

# 安装 ADP OpenClaw
echo "📦 安装 ADP OpenClaw..."
npm install -g adp-openclaw
echo "✅ ADP OpenClaw 安装完成"
echo ""

echo "🎉 所有技能安装完成！"
echo ""
echo "下一步："
echo "1. 配置 ~/.openclaw/openclaw.json"
echo "2. 运行 openclaw gateway start"
echo "3. 运行 openclaw status 验证"
