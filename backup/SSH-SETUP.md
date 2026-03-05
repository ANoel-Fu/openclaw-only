# 🔑 SSH 密钥配置指南

## 当前状态

已生成 SSH 密钥对：
- **私钥**: `~/.ssh/id_ed25519`
- **公钥**: `~/.ssh/id_ed25519.pub`

## 添加公钥到 GitHub

### 方法一：手动添加（推荐）

1. 复制公钥内容：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   
   公钥内容：
   ```
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIvXGhPhqaCmuS0RbPkSv6zhed7hfPdQgnqHr/e6fSZ8 openclaw-backup
   ```

2. 访问 GitHub SSH 密钥设置页面：
   https://github.com/settings/keys

3. 点击 "New SSH key"

4. 填写：
   - **Title**: `openclaw-backup`
   - **Key type**: Authentication Key
   - **Key**: 粘贴上面的公钥内容

5. 点击 "Add SSH key"

### 方法二：使用 gh CLI

```bash
gh ssh-key add ~/.ssh/id_ed25519.pub --title "openclaw-backup"
```

## 验证配置

添加完成后，测试连接：

```bash
ssh -T git@github.com
```

成功时会显示：
```
Hi ANoel-Fu! You've successfully authenticated, but GitHub does not provide shell access.
```

## 推送代码

验证通过后，执行：

```bash
cd ~/.openclaw/workspace
git push -u origin master
```

---

_创建时间：2026-03-05_
