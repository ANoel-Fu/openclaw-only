# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 🔧 API Keys & Services

### Search Engines (Priority Order)

1. **Tavily** (Primary) - AI-optimized search ✅ **已配置**
   - API Key: `~/.openclaw/.env` (TAVILY_API_KEY)
   - 配置时间：2026-03-11
   - 使用场景：科技新闻、研究查询、一般搜索
   - 命令示例：
     ```bash
     # 一般搜索
     node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "query"
     
     # 新闻搜索（限定最近 1 天）
     node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "query" --topic news --days 1
     
     # 深度搜索
     node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "query" --deep
     ```

2. **Brave Search** (Fallback) - Requires BRAVE_API_KEY
   - Status: Not configured

### Notes
- Tavily is the default search engine for all web queries
- For tech/news queries, always prefer Tavily

---

## 📰 科技日报推送配置

**推送时间**：每日上午（用户要求）
**日期规则**：严格限定为当天日期，不获取历史新闻
**数据源**：Tavily AI 搜索（`--topic news --days 1`）

**推送格式**：
- 分类：航天、AI 前沿、消费电子、企业动态、市场观察
- 每条新闻标注来源和相关性
- 末尾标注数据来源和日期

---

## 📚 Java 学习日报配置

**推送时间**：每天早上 9:30、晚上 23:00
**题库位置**：`~/.openclaw/workspace/memory/java-interview-questions-complete.json`
**题库更新**：每天凌晨 2 点自动从 小林 coding 爬取更新
**题目数量**：326 道（小林 coding 官方题库）
**每日推送**：5 道随机题目

**题库源（小林 coding）**：
1. Java 基础：https://www.xiaolincoding.com/interview/java.html（95 题）
2. Java 集合：https://www.xiaolincoding.com/interview/collections.html（54 题）
3. Java 并发：https://www.xiaolincoding.com/interview/juc.html（72 题）
4. JVM：https://www.xiaolincoding.com/interview/jvm.html（40 题）
5. Spring：https://www.xiaolincoding.com/interview/spring.html（65 题）

**题库格式**：
```json
{
  "id": 1,
  "category": "Java 基础",
  "question": "题目内容",
  "answer": "详细答案（含解析、代码示例）",
  "url": "https://www.xiaolincoding.com/...",
  "timesSent": 0,
  "lastSent": null
}
```

**推送格式**：
- Markdown 格式文本（飞书自动渲染）
- 每题包含：问题、详细答案、来源链接
- **链接规则**：锚点有空格时提供两个版本（去除空格、替换为 -）
- 分类覆盖：Java 基础、集合、并发、JVM、Spring 等
- 末尾显示学习统计（无鼓励语）

**脚本位置**：
- 推送脚本：`~/.openclaw/workspace/scripts/java-daily-report-v4.py`
- 题库更新：`~/.openclaw/workspace/scripts/java-question-bank-updater.py`（使用 Tavily）

**Cron 配置**：
```bash
# Java 题库自动更新 - 每天凌晨 2 点（Tavily）
0 2 * * * python3 scripts/java-question-bank-updater.py

# Java 学习日报 - 每天 9:30 和 23:00
30 9 * * * TZ=Asia/Shanghai scripts/java-daily-report-v4.py
0 23 * * * TZ=Asia/Shanghai scripts/java-daily-report-v4.py
```

**格式规范**：`~/.openclaw/workspace/memory/java-daily-report-format-spec.md`

**题库统计**（2026-03-14 10:28）：
- 总题目：326 道
- 分类：Java 基础 (95)、并发 (72)、Spring (65)、集合 (54)、JVM (40)
- 学习周期：约 65 天完成一轮（每天 5 道）
