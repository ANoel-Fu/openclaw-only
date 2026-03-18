# ✅ AI/科技日报 - 配置完成

**最后更新：** 2026-03-18  
**状态：** ✅ 正常运行

---

## 🎉 已完成配置

### 1. 数据来源（直接抓取）

| 来源 | 类型 | 状态 |
|------|------|------|
| 36Kr | 快讯 | ✅ 正常 |
| 虎嗅 | 文章 | ✅ 正常 |
| 量子位 | AI 专业 | ✅ 正常 |
| 机器之心 | AI 专业 | ✅ 正常 |
| 腾讯科技 | 综合门户 | ✅ 正常 |
| 网易科技 | 综合门户 | ✅ 正常 |
| 新浪科技 | 综合门户 | ✅ 正常 |

### 2. 定时任务配置

- ⏰ **推送时间：** 每天上午 8:50（北京时间）
- 📤 **推送渠道：** 飞书（已配置你的账号）
- 📊 **最大条目：** 20 条/天
- 🔄 **去重阈值：** 85% 相似度
- 🏷️ **自动分类：** 8 大类别

### 3. 脚本位置

```
/root/.openclaw/workspace/scripts/
├── ai-tech-daily.sh          # 主启动脚本
├── ai-tech-daily-full.sh     # 完整版本
└── ai-tech-daily-smart.py    # Python 抓取脚本（核心）
```

---

## 📋 日报格式

```markdown
# 🤖 AI/科技日报 - 2026-03-18 周三

_每日热点精选 · 把握科技脉搏 · 综合多家来源_

---

## 🔥 今日头条

### 🤖 AI 与大模型

1. **[标题](链接)** 🔗 _来源：36Kr_
   📝 AI 领域持续创新，技术边界不断拓展。

2. **[标题](链接)** 🔗 _来源：量子位_
   📝 点击链接阅读原文了解更多。

### 📱 硬件与消费电子

1. **[标题](链接)** 🔗 _来源：网易科技_
   📝 消费电子市场回暖，技术创新驱动增长。

---

## 📅 明日关注

- 科技巨头最新动向
- AI 政策与行业应用
- 消费电子市场变化

---

_数据来源：36Kr, 量子位，机器之心，网易科技（综合抓取）_
_生成时间：08:50_
_下次推送：明日 8:50_

---
**💬 互动**：回复"详细"获取某条新闻深度解读，回复"添加"自定义关注领域
```

---

## 🚀 管理命令

### 查看定时任务
```bash
crontab -l | grep ai-tech-daily
```

### 手动测试
```bash
# 运行脚本（输出到控制台 + 发送飞书）
python3 /root/.openclaw/workspace/scripts/ai-tech-daily-smart.py
```

### 查看日志
```bash
tail -f /root/.openclaw/workspace/logs/ai-tech-daily.log
```

### 暂停推送
```bash
# 编辑 crontab
crontab -e
# 在对应行前加 # 注释掉
```

---

## 🛠️ 自定义配置

### 修改推送时间

编辑 crontab：
```bash
crontab -e
```

修改时间（cron 格式）：
```bash
# 每天 8:50
50 8 * * * python3 /root/.openclaw/workspace/scripts/ai-tech-daily-smart.py

# 每天 9:00
0 9 * * * python3 /root/.openclaw/workspace/scripts/ai-tech-daily-smart.py

# 工作日 9:00
0 9 * * 1-5 python3 /root/.openclaw/workspace/scripts/ai-tech-daily-smart.py
```

### 添加新数据源

编辑 `scripts/ai-tech-daily-smart.py`，添加新的抓取函数：

```python
def fetch_your_source():
    """抓取自定义来源"""
    news_items = []
    try:
        url = "https://example.com/tech"
        response = requests.get(url, headers=HEADERS, timeout=15)
        # ... 解析逻辑
    except Exception as e:
        print(f"❌ 自定义来源 抓取失败：{e}")
    return news_items[:15]

# 在 generate_report() 中调用
all_news.extend(fetch_your_source())
```

### 修改分类标签

编辑 `categorize_news()` 函数中的关键词：

```python
def categorize_news(title):
    text = title.lower()
    
    if any(kw in text for kw in ['你的关键词']):
        return "🏷️ 你的分类名"
    # ...
```

---

## ⚠️ 注意事项

1. **网络访问**：确保服务器可以访问配置的新闻网站
2. **反爬虫**：部分网站可能有反爬机制，如抓取失败请检查 User-Agent
3. **去重逻辑**：当前使用标题相似度去重（85% 阈值）
4. **推送权限**：飞书机器人需要消息推送权限

---

## 🆘 故障排查

### 问题：收不到日报
1. 检查 cron 任务：`crontab -l`
2. 查看日志：`cat /root/.openclaw/workspace/logs/ai-tech-daily.log`
3. 手动测试：`python3 scripts/ai-tech-daily-smart.py`

### 问题：抓取失败
1. 检查网络连接：`curl -I https://36kr.com`
2. 检查 Python 依赖：`pip3 list | grep requests`
3. 查看详细错误：查看日志文件

### 问题：内容重复
1. 调整去重阈值（脚本中的 `threshold=0.85`）
2. 检查是否有重复的数据源

---

## 📊 推送时间表

| 日报类型 | 推送时间 | 状态 |
|---------|---------|------|
| AI/科技日报 | 每天 8:50 | ✅ 正常 |

---

## 📞 技术支持

如需添加新数据源、修改推送格式或集成其他功能，请告诉我！

---

**配置完成时间：** 2026-03-18  
**最后测试：** 2026-03-18 10:05 ✅
