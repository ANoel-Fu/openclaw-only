# 2026-03-15 - Java 学习日报 PATH 环境变量修复

## 🐛 问题发现

**时间：** 2026-03-15 23:00  
**现象：** Java 学习日报晚上 23:00 没有推送

## 🔍 问题分析

### Cron 日志显示执行了：
```
2026-03-15T23:00:01.955025+08:00 CROND: (root) CMD (cd /root/.openclaw/workspace && TZ=Asia/Shanghai /root/.openclaw/workspace/scripts/java-daily-report-v4.py >> logs/java-daily-report.log 2>&1)
```

### 但脚本日志显示：
```
❌ 发送失败：/root/.local/share/pnpm/openclaw: line 20: exec: node: not found
```

### 根因：
**Cron 环境 PATH 不完整，找不到 `node` 命令！**

脚本调用 `/root/.local/share/pnpm/openclaw` 发送消息，这个脚本需要 `node`，但 cron 的默认 PATH 只有：
```
/usr/bin:/bin
```

而 node 安装在：
```
/root/.nvm/versions/node/v22.22.0/bin/node
```

## ✅ 修复方案

### 在 Python 脚本开头设置 PATH 环境变量

**修改文件：** `/root/.openclaw/workspace/scripts/java-daily-report-v4.py`

**添加代码：**
```python
# 设置完整的 PATH，确保 cron 环境下能找到 node 命令
import os
os.environ['PATH'] = '/root/.nvm/versions/node/v22.22.0/bin:' + os.environ.get('PATH', '')
```

### 修改位置：
在 shebang 之后，其他 import 之前。

## 🧪 验证结果

```bash
cd /root/.openclaw/workspace && python3 scripts/java-daily-report-v4.py
```

**结果：** ✅ 发送成功 (Message ID: om_x100b54588766cd30b33276ef6cc110f)

## 📅 推送时间

- **早上：** 9:30 (Asia/Shanghai)
- **晚上：** 23:00 (Asia/Shanghai)

## 🔧 相关文件

- 脚本：`/root/.openclaw/workspace/scripts/java-daily-report-v4.py`
- 题库：`/root/.openclaw/workspace/memory/java-interview-questions-complete.json`
- 日志：`/root/.openclaw/workspace/logs/java-daily-report.log`

## ✅ 确认清单

- [x] Python 脚本已添加 PATH 设置
- [x] 手动测试推送成功
- [x] Cron 配置正确（包含 cd 工作目录）
- [x] 脚本可执行权限正常

## 📝 备注

这是今天修复的第二个 Java 日报 cron 问题：
1. 上午修复：添加 `cd /root/.openclaw/workspace &&` 切换工作目录
2. 晚上修复：在 Python 脚本内设置 PATH 环境变量

两个问题都解决了，明天开始应该能正常推送！
