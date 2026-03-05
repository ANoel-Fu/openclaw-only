# 🤖 OpenClaw 自动备份

## 配置说明

**备份时间：** 每天凌晨 2:00 (GMT+8)

**备份内容：**
- Git 工作区变更
- 配置文件更新
- 记忆文件变更

## 脚本位置

- **脚本**: `/root/.openclaw/cron/git-backup.sh`
- **日志**: `/root/.openclaw/logs/git-backup.log`

## Cron 配置

```bash
# 查看当前 cron 任务
crontab -l | grep OpenClaw

# 输出：
# OpenClaw 工作区自动备份 - 每天凌晨 2 点执行
# 0 2 * * * /root/.openclaw/cron/git-backup.sh
```

## 日志查看

```bash
# 查看最新日志
tail -20 /root/.openclaw/logs/git-backup.log

# 实时查看
tail -f /root/.openclaw/logs/git-backup.log

# 查看历史日志
cat /root/.openclaw/logs/git-backup.log
```

## 手动触发备份

```bash
/root/.openclaw/cron/git-backup.sh
```

## 修改备份时间

编辑 crontab：
```bash
crontab -e
```

修改时间（格式：`分 时 日 月 周`）：

| 时间 | Cron 表达式 | 说明 |
|------|------------|------|
| 每天 2:00 | `0 2 * * *` | 默认配置 |
| 每天 0:00 | `0 0 * * *` | 午夜 |
| 每 6 小时 | `0 */6 * * *` | 高频备份 |
| 每周一 9:00 | `0 9 * * 1` | 每周一次 |

## 禁用自动备份

注释掉 cron 任务：
```bash
crontab -e
# 在行首添加 #
# 0 2 * * * /root/.openclaw/cron/git-backup.sh
```

或删除：
```bash
crontab -l | grep -v "git-backup.sh" | crontab -
```

## 故障排查

### 备份失败

1. 检查日志：
   ```bash
   tail -50 /root/.openclaw/logs/git-backup.log
   ```

2. 检查 SSH 连接：
   ```bash
   ssh -T git@github.com
   ```

3. 手动测试脚本：
   ```bash
   /root/.openclaw/cron/git-backup.sh
   ```

### 常见问题

**Q: 提示 "Another instance is running"**
A: 删除锁文件：`rm /tmp/openclaw-git-backup.lock`

**Q: 推送失败 "Permission denied"**
A: 检查 SSH 密钥是否有效，或重新添加公钥到 GitHub

**Q: 无变更但显示有变更**
A: 可能是文件权限变化，Git 会检测到

---

_配置日期：2026-03-05_
