# 🚀 首次推送指南

## 当前状态

✅ **已完成：**
- 仓库已初始化
- 备份文件已创建
- Git 提交已完成（本地）
- SSH 密钥已生成

⏳ **待完成：**
- 将 SSH 公钥添加到 GitHub
- 首次推送到远程仓库

## 需要手动操作的步骤

### 步骤 1：添加 SSH 公钥到 GitHub

**公钥内容：**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIvXGhPhqaCmuS0RbPkSv6zhed7hfPdQgnqHr/e6fSZ8 openclaw-backup
```

**操作步骤：**
1. 访问：https://github.com/settings/keys
2. 点击 "New SSH key"
3. Title: `openclaw-backup`
4. Key type: `Authentication Key`
5. 粘贴上面的公钥
6. 点击 "Add SSH key"

### 步骤 2：验证并推送

添加完成后，在终端执行：

```bash
# 验证 SSH 连接
ssh -T git@github.com

# 如果看到 "Hi ANoel-Fu! You've successfully authenticated"，继续下一步

# 推送到 GitHub
cd ~/.openclaw/workspace
git push -u origin master
```

### 步骤 3：验证推送成功

访问仓库页面确认文件已上传：
https://github.com/ANoel-Fu/openclaw-only

应该能看到：
- `BACKUP.md` - 主恢复指南
- `backup/openclaw.config.template.json` - 配置模板
- `backup/restore-checklist.md` - 恢复检查清单
- `backup/install-skills.sh` - 技能安装脚本
- `backup/SSH-SETUP.md` - SSH 配置指南
- `.gitignore` - Git 忽略规则

---

## 后续自动备份

首次推送成功后，后续备份只需：

```bash
cd ~/.openclaw/workspace
git add .
git commit -m "backup: $(date +%Y-%m-%d)"
git push
```

---

_创建时间：2026-03-05_
