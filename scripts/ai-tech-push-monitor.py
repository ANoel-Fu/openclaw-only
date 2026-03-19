#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI/Tech Push Monitor - 推送健康检查
检查最近的推送是否成功，失败则告警
"""

import os
import subprocess
from datetime import datetime, timedelta

# 确保环境变量
os.environ['PATH'] = '/root/.nvm/versions/node/v22.22.0/bin:/root/.local/share/pnpm/bin:/usr/local/bin:/usr/bin:/bin:' + os.environ.get('PATH', '')
os.environ['TZ'] = 'Asia/Shanghai'

LOG_FILE = "/root/.openclaw/workspace/logs/ai-tech-daily.log"
TARGET_USER = "ou_a7d902ae2ba72919f55a1e8180357c55"

def check_push_status():
    """检查最近的推送状态"""
    try:
        if not os.path.exists(LOG_FILE):
            send_alert("⚠️ 日志文件不存在")
            return
        
        # 读取最后 50 行日志
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()[-50:]
        
        # 查找最近的推送记录
        last_push_time = None
        push_success = False
        
        for line in reversed(lines):
            if '开始抓取今日新闻' in line:
                # 提取时间（从日志文件行无法直接获取，改用文件修改时间）
                break
            if '消息发送成功' in line:
                push_success = True
                break
            if '消息发送失败' in line or '❌' in line:
                push_success = False
                break
        
        # 检查日志文件修改时间
        mtime = os.path.getmtime(LOG_FILE)
        last_modified = datetime.fromtimestamp(mtime)
        now = datetime.now()
        
        # 如果最近 2 小时内有日志但没有成功标记
        if (now - last_modified).total_seconds() < 7200:
            if not push_success:
                send_alert(f"❌ 推送失败检测\n\n最近推送时间：{last_modified.strftime('%Y-%m-%d %H:%M')}\n状态：发送失败\n\n请检查日志：{LOG_FILE}")
            else:
                print("✅ 推送状态正常")
        else:
            print("ℹ️ 2 小时内无推送记录（正常）")
    
    except Exception as e:
        send_alert(f"⚠️ 监控脚本异常\n\n错误：{str(e)}")

def send_alert(message):
    """发送告警消息"""
    print(f"🚨 发送告警：{message}")
    
    cmd = [
        "/root/.local/share/pnpm/openclaw",
        "message",
        "send",
        "--channel", "feishu",
        "--target", TARGET_USER,
        "--message", f"""🚨 **AI/科技日报推送告警**

{message}

---
_监控脚本自动检测 · {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 告警已发送")
    else:
        print(f"❌ 告警发送失败：{result.stderr}")

if __name__ == "__main__":
    check_push_status()
