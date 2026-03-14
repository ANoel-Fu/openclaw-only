# Java 学习日报 - 格式规范（永久保存）

**创建时间：** 2026-03-13  
**最后更新：** 2026-03-14  
**用户要求：** 记住这个格式，之后无论修改什么问题都保持这个格式

---

## 📋 格式规范

### 1. 消息类型
- **格式：** Markdown 纯文本
- **发送方式：** `openclaw message send --message <markdown_text>`
- **渲染：** 飞书自动渲染 Markdown

### 2. 整体结构

```markdown
# 📚 Java 学习日报 - 第 X 天 (YYYY-MM-DD)

💡 每天 5 道题，系统掌握 Java 面试核心知识点

---

## 1️⃣【分类】

**Q: 问题？**

**✅ 答案：**

答案内容（支持加粗、列表等格式）

📖 **来源链接 1（去除空格）：** [点击跳转](URL_no_space)
📖 **来源链接 2（替换为 -）：** [点击跳转](URL_dash)

---

## 2️⃣【分类】

...

---

## 📊 今日学习统计

📝 今日题目：5 道
📖 模块：模块 1, 模块 2, ...

```

### 3. 格式细节

#### 标题
- 主标题：`# 📚 Java 学习日报 - 第 X 天 (YYYY-MM-DD)`
- 副标题：`💡 每天 5 道题，系统掌握 Java 面试核心知识点`
- 题目：`## 1️⃣【分类】`
- 统计：`## 📊 今日学习统计`

#### 分隔线
- 使用 `---` 分隔各部分

#### 加粗
- 问题：`**Q: 问题？**`
- 答案标题：`**✅ 答案：**`
- 来源标题：`📖 **来源链接 X：**`

#### 链接规则（重要！）
**当锚点存在空格时，提供两个链接版本：**

示例：
- 当前题目：`jvm、jdk、jre 三者关系`
- 链接 1（去除空格）：`jvm、jdk、jre 三者关系`
- 链接 2（将空格替换成 -）：`jvm、jdk、jre-三者关系`

**推送格式：**
```markdown
📖 **来源链接 1（去除空格）：** [点击跳转](URL_no_space)
📖 **来源链接 2（替换为 -）：** [点击跳转](URL_dash)
```

**当锚点不存在空格时，使用单一链接：**
```markdown
📖 **来源：** [点击查看解析](URL)
```

#### 列表
- 使用 `• ` 作为列表符号
- 编号格式：`• 1.内容`

#### 答案格式
- 支持加粗：`**关键词**`
- 支持列表：`• 列表项`
- 分段清晰，每段之间空一行

### 4. 推送时间
- 每天早上 9:30
- 每天晚上 23:00

### 5. 题库配置

#### 题库文件
- **位置：** `/root/.openclaw/workspace/memory/java-interview-questions-complete.json`
- **更新方式：** 每天凌晨 2 点自动从 小林 coding 爬取更新（使用 Tavily）
- **题目总数：** 326 道（小林 coding 官方题库）

#### 题库源（小林 coding）
1. **Java 基础：** https://www.xiaolincoding.com/interview/java.html（95 题）
2. **Java 集合：** https://www.xiaolincoding.com/interview/collections.html（54 题）
3. **Java 并发：** https://www.xiaolincoding.com/interview/juc.html（72 题）
4. **JVM：** https://www.xiaolincoding.com/interview/jvm.html（40 题）
5. **Spring：** https://www.xiaolincoding.com/interview/spring.html（65 题）

#### 题目格式
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

#### 答案要求
- 详细解析（300-500 字）
- 包含：核心概念、原理、场景、注意事项、代码示例
- 链接：必须带锚点（具体到题目位置）

### 6. 脚本路径
- **推送脚本：** `/root/.openclaw/workspace/scripts/java-daily-report-v4.py`
- **题库更新：** `/root/.openclaw/workspace/scripts/java-question-bank-updater.py`（使用 Tavily extract）

### 7. Cron 配置
```bash
# Java 题库自动更新 - 每天凌晨 2 点（Tavily）
0 2 * * * cd /root/.openclaw/workspace && python3 scripts/java-question-bank-updater.py >> logs/java-question-bank-update.log 2>&1

# Java 学习日报 - 每天早上 9:30 和晚上 23:00 (Asia/Shanghai)
30 9 * * * TZ=Asia/Shanghai /root/.openclaw/workspace/scripts/java-daily-report-v4.py >> logs/java-daily-report.log 2>&1
0 23 * * * TZ=Asia/Shanghai /root/.openclaw/workspace/scripts/java-daily-report-v4.py >> logs/java-daily-report.log 2>&1
```

---

## ⚠️ 重要提醒

**无论后续如何修改（如添加题目、修改答案、调整推送时间等），都必须保持此 Markdown 格式不变！**

**特别注意：**
- ✅ 链接规则：锚点有空格时必须提供两个版本
- ✅ 题库更新：每天凌晨 2 点自动爬取，保持不重复
- ✅ 无鼓励语：日报末尾不再显示鼓励语

---

## 📝 格式示例

```markdown
# 📚 Java 学习日报 - 第 73 天 (2026-03-14)

💡 每天 5 道题，系统掌握 Java 面试核心知识点

---

## 1️⃣【Java 基础】

**Q: JVM、JDK、JRE 三者关系？**

**✅ 答案：**

JVM 是 Java 虚拟机（运行环境）；JRE=JVM+ 核心类库（运行时环境）；JDK=JRE+ 开发工具（编译器、调试器等）。关系：JDK > JRE > JVM。

📖 **来源链接 1（去除空格）：** [点击跳转](https://www.xiaolincoding.com/interview/java.html#jvm%E3%80%81jdk%E3%80%81jre%E4%B8%89%E8%80%85%E5%85%B3%E7%B3%BB)
📖 **来源链接 2（替换为 -）：** [点击跳转](https://www.xiaolincoding.com/interview/java.html#jvm%E3%80%81jdk%E3%80%81jre-%E4%B8%89%E8%80%85%E5%85%B3%E7%B3%BB)

---

## 📊 今日学习统计

📝 今日题目：5 道
📖 模块：Java 基础，JVM, Spring

```

---

## 🔄 更新日志

### 2026-03-14 - 重大更新
- ✅ **题库更新**：使用 Tavily extract 获取小林 coding 官方题库
- ✅ **题目数量**：326 道（Java 基础 95、并发 72、Spring 65、集合 54、JVM 40）
- ✅ **链接规则**：锚点有空格时提供两个版本（去除空格、替换为 -）
- ✅ **删除鼓励语**：移除日报末尾的鼓励语
- ✅ **自动更新**：每天凌晨 2 点执行

### 2026-03-13
- ✅ 初始版本：28 道精选题，每题 300-500 字详细解析
- ✅ Markdown 格式推送
- ✅ URL 锚点自动编码

---

**此格式已永久保存，后续所有修改都必须遵循此规范！**
