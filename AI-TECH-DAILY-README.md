# 🤖 AI/科技日报自动化系统

## 当前状态

✅ **已配置** - 每日 AI/科技热点新闻自动收集系统

## 使用方式

### 方式一：手动触发（立即可用）

直接对我说：
- "生成今天的 AI 日报"
- "科技新闻"
- "AI 日报"

我会立即为你收集并发送当日的热点新闻。

### 方式二：自动定时发送（推荐）

#### 方案 A：使用系统 crontab（需要服务器权限）

1. 编辑 crontab：
```bash
crontab -e
```

2. 添加以下行（每天早上 8:00 自动发送）：
```bash
0 8 * * * cd /root/.openclaw/workspace && bash scripts/ai-tech-daily.sh >> /root/.openclaw/workspace/logs/ai-tech-daily.log 2>&1
```

3. 保存退出，系统会每天自动执行

#### 方案 B：使用 OpenClaw HEARTBEAT（简单推荐）

在 `HEARTBEAT.md` 中添加每日检查任务，系统会定期自动执行。

**优点：**
- 无需配置 crontab
- OpenClaw 自动管理
- 可以灵活调整频率

**配置方法：**
告诉我"设置每天早上 8 点发送 AI 日报"，我会帮你配置。

---

## 日报内容

每日包含：
- 🔥 **今日头条** - AI 与大模型、科技巨头动态、前沿科技
- 📊 **行业观察** - 深度分析和趋势解读
- 💡 **深度推荐** - 精选文章和链接
- 📅 **明日关注** -  upcoming events

## 数据来源

- 虎嗅网 (huxiu.com)
- 36Kr (36kr.com)
- 晚点 (latepost.com)
- 其他科技媒体

## 自定义选项

你可以要求：
- **调整发送时间** - "改为每天早上 9 点发送"
- **添加关注领域** - "添加关注：自动驾驶、芯片、Web3"
- **调整频率** - "改为每周发送一次"
- **暂停发送** - "暂时停止 AI 日报"

---

## 日志查看

查看发送历史：
```bash
cat /root/.openclaw/workspace/logs/ai-tech-daily.log
```

---

## 技术支持

如有问题，随时问我！😊
