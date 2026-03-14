# Java 学习日报 - 完整配置文档

**创建时间：** 2026-03-14  
**最后更新：** 2026-03-14 11:00  
**状态：** ✅ 配置完成并运行中

---

## 📋 核心配置

### 推送时间
- **早上：** 9:30 (Asia/Shanghai)
- **晚上：** 23:00 (Asia/Shanghai)
- **频率：** 每天 2 次

### 题库配置
- **题库文件：** `/root/.openclaw/workspace/memory/java-interview-questions-complete.json`
- **题目数量：** 291 道（动态更新）
- **每日推送：** 5 道随机题目
- **学习周期：** 约 58 天完成一轮

### 题库源（小林 coding）
| 分类 | 题目数 | URL |
|------|--------|-----|
| Java 基础 | 76 道 | https://www.xiaolincoding.com/interview/java.html |
| Java 并发 | 67 道 | https://www.xiaolincoding.com/interview/juc.html |
| Spring | 60 道 | https://www.xiaolincoding.com/interview/spring.html |
| Java 集合 | 52 道 | https://www.xiaolincoding.com/interview/collections.html |
| JVM | 36 道 | https://www.xiaolincoding.com/interview/jvm.html |

---

## 🔧 脚本配置

### 推送脚本
**文件：** `/root/.openclaw/workspace/scripts/java-daily-report-v4.py`

**功能：**
- 从题库随机选择 5 道题目
- 生成 Markdown 格式消息
- 自动处理 URL 锚点编码
- 双链接规则（锚点有空格时提供两个版本）
- 通过 `openclaw message send` 发送到飞书

**关键配置：**
```python
QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"
TARGET_USER = "ou_a7d902ae2ba72919f55a1e8180357c55"
```

### 题库更新脚本
**文件：** `/root/.openclaw/workspace/scripts/java-question-bank-updater.py`

**功能：**
- 每天凌晨 2 点自动执行
- 使用 Tavily extract 获取小林 coding 题库内容
- 解析题目、答案、URL 锚点
- 去重、合并、保存题库
- 保留已有题目的发送记录

**关键配置：**
```python
QUESTION_SOURCES = [
    {"url": "https://www.xiaolincoding.com/interview/java.html", "category": "Java 基础"},
    {"url": "https://www.xiaolincoding.com/interview/collections.html", "category": "Java 集合"},
    {"url": "https://www.xiaolincoding.com/interview/juc.html", "category": "Java 并发"},
    {"url": "https://www.xiaolincoding.com/interview/jvm.html", "category": "JVM"},
    {"url": "https://www.xiaolincoding.com/interview/spring.html", "category": "Spring"}
]
OUTPUT_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"
```

---

## 📅 Cron 配置

**查看：** `crontab -l | grep java`

```bash
# Java 题库自动更新 - 每天凌晨 2 点（Tavily）
0 2 * * * cd /root/.openclaw/workspace && python3 scripts/java-question-bank-updater.py >> logs/java-question-bank-update.log 2>&1

# Java 学习日报 - 每天早上 9:30 和晚上 23:00 (Asia/Shanghai)
30 9 * * * TZ=Asia/Shanghai /root/.openclaw/workspace/scripts/java-daily-report-v4.py >> logs/java-daily-report.log 2>&1
0 23 * * * TZ=Asia/Shanghai /root/.openclaw/workspace/scripts/java-daily-report-v4.py >> logs/java-daily-report.log 2>&1
```

---

## 📝 推送格式规范

### 整体结构
```markdown
# 📚 Java 学习日报 - 第 X 天 (YYYY-MM-DD)

💡 每天 5 道题，系统掌握 Java 面试核心知识点

---

## 1️⃣【分类】

**Q: 问题？**

**✅ 答案：**

详细答案内容...

📖 **来源链接 1（去除空格）：** [点击跳转](URL_no_space)
📖 **来源链接 2（替换为 -）：** [点击跳转](URL_dash)

---

## 📊 今日学习统计

📝 今日题目：5 道
📖 模块：模块 1, 模块 2, ...

```

### 链接规则
**当锚点存在空格时，提供两个链接版本：**
- 链接 1：去除所有空格
- 链接 2：空格替换为连字符 `-`

**当锚点不存在空格时，使用单一链接：**
- 标准 URL（已 URL 编码）

### 答案格式
- 支持 Markdown 加粗：`**关键词**`
- 支持列表：`• 列表项`
- 支持编号：`• 1.内容`
- 分段清晰，每段之间空一行

### 无鼓励语
- 末尾仅显示学习统计
- 不显示"坚持每天学习，大厂 offer 等着你！"等鼓励语

---

## 🔑 题库格式

### 题目结构
```json
{
  "id": 1,
  "category": "Java 基础",
  "question": "题目内容",
  "answer": "详细答案（含解析、代码示例）",
  "url": "https://www.xiaolincoding.com/interview/java.html#锚点",
  "timesSent": 0,
  "lastSent": null
}
```

### 字段说明
- `id`: 题目编号（自动重新编号）
- `category`: 分类（Java 基础、Java 集合、Java 并发、JVM、Spring）
- `question`: 问题文本
- `answer`: 详细答案（300-500 字，含解析、代码示例）
- `url`: 来源链接（带锚点，已 URL 编码）
- `timesSent`: 发送次数（用于优先选择发送次数少的题目）
- `lastSent`: 上次发送日期

---

## 🛠️ 依赖配置

### Tavily API
- **API Key 位置：** `/root/.openclaw/.env`
- **环境变量：** `TAVILY_API_KEY`
- **用途：** 题库爬取、网页内容获取
- **规则：** 访问网址优先使用 Tavily

### Python 环境
- **版本：** Python 3.x
- **依赖库：** 标准库（json, os, re, subprocess, datetime, urllib.parse）

### Node.js 环境
- **版本：** Node.js 18+
- **用途：** 运行 Tavily 脚本
- **脚本位置：** `/root/.openclaw/workspace/skills/tavily-search/scripts/`

---

## 📊 状态文件

### 题库状态
**文件：** `/root/.openclaw/workspace/memory/java-daily-push-state.json`

**内容：**
```json
{
  "lastUpdate": "2026-03-14 10:55:32",
  "totalQuestions": 291,
  "sources": {
    "Java 基础": 76,
    "Java 并发": 67,
    "Spring": 60,
    "Java 集合": 52,
    "JVM": 36
  }
}
```

### 日志文件
- **题库更新日志：** `/root/.openclaw/workspace/logs/java-question-bank-update.log`
- **日报推送日志：** `/root/.openclaw/workspace/logs/java-daily-report.log`

---

## 📁 文件清单

### 核心文件
- ✅ `/root/.openclaw/workspace/memory/java-interview-questions-complete.json` - 题库
- ✅ `/root/.openclaw/workspace/memory/java-daily-push-state.json` - 状态文件
- ✅ `/root/.openclaw/workspace/memory/java-daily-report-format-spec.md` - 格式规范

### 脚本文件
- ✅ `/root/.openclaw/workspace/scripts/java-daily-report-v4.py` - 推送脚本
- ✅ `/root/.openclaw/workspace/scripts/java-question-bank-updater.py` - 题库更新脚本

### 配置文件
- ✅ `/root/.openclaw/workspace/TOOLS.md` - 工具配置（含 Tavily 配置）
- ✅ `/root/.openclaw/.env` - 环境变量（TAVILY_API_KEY）

### 日志文件
- 📝 `/root/.openclaw/workspace/logs/java-question-bank-update.log`
- 📝 `/root/.openclaw/workspace/logs/java-daily-report.log`

---

## ⚠️ 重要规则

### 用户要求（2026-03-14）
1. **双链接规则：** 锚点有空格时提供两个版本（去除空格、替换为 -）
2. **题库自动更新：** 每天凌晨 2 点从 5 个小林 coding 题库爬取
3. **删除鼓励语：** 移除日报末尾鼓励语
4. **访问网址优先使用 Tavily：** 所有 URL 访问场景优先使用 Tavily（search 或 extract）

### 维护注意事项
- ✅ 题库更新脚本使用 Tavily extract 获取内容
- ✅ URL 锚点自动编码（推送脚本处理）
- ✅ 保留已有题目的发送记录（timesSent, lastSent）
- ✅ 去重基于问题文本
- ✅ 答案长度限制 2000 字

---

## 🎯 学习效果

**每天 5 道题，291 道题库：**
- 📅 **58 天** 完成一轮
- 📅 **约 3 个月** 完成三轮巩固
- 📅 **6 个月** 系统掌握 Java 面试核心知识点

**题目覆盖：**
- Java 基础：76 道（概念、数据类型、面向对象、关键字、反射、注解、异常、IO、新特性）
- Java 集合：52 道（List、Map、Set、队列等）
- Java 并发：67 道（线程池、锁、volatile、AQS、并发工具等）
- JVM：36 道（内存模型、GC、类加载、性能调优等）
- Spring：60 道（IOC、AOP、Bean 生命周期、事务等）

---

## 🔄 版本历史

### v4 - 2026-03-14
- ✅ 使用 Tavily extract 获取题库（291 道）
- ✅ 双链接规则（锚点有空格时提供两个版本）
- ✅ 删除鼓励语
- ✅ URL 锚点正确解析

### v3 - 2026-03-13
- ✅ Markdown 格式推送
- ✅ URL 锚点自动编码
- ✅ 28 道精选题

---

**此配置文档已永久保存，后续所有修改都应参考此文档！**
