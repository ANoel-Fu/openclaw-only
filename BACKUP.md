# 🦞 OpenClaw 复活指南

> 系统重装后，按此指南恢复你的 AI 助理

## ⚡ 快速恢复（5 分钟）

### 第一步：安装 Node.js 和 OpenClaw

```bash
# 安装 Node.js 20+
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 OpenClaw
sudo npm install -g openclaw
```

### 第二步：克隆备份仓库

```bash
# 创建工作目录
mkdir -p ~/.openclaw
cd ~/.openclaw

# 克隆你的备份
git clone git@github.com:ANoel-Fu/openclaw-only.git workspace
```

### 第三步：恢复配置

```bash
# 从备份恢复配置文件
cp workspace/backup/openclaw.config.template.json ~/.openclaw/openclaw.json

# 【重要】编辑配置文件，填入你的真实密钥
nano ~/.openclaw/openclaw.json
```

需要填写的密钥：
- `models.providers.bailian.apiKey` - 阿里云 DashScope API Key
- `channels.feishu.appId` - 飞书应用 ID
- `channels.feishu.appSecret` - 飞书应用密钥
- `gateway.auth.token` - 网关认证 Token（可生成新的）

### 第四步：启动 OpenClaw

```bash
# 启动网关服务
openclaw gateway start

# 验证状态
openclaw status
```

### 第五步：恢复身份和记忆

```bash
cd ~/.openclaw/workspace

# 你的身份文件已恢复（SOUL.md, USER.md, IDENTITY.md 等）
# 检查记忆文件
ls -la memory/
```

---

## 📦 备份内容清单

### 已备份（本仓库）

| 文件 | 说明 | 敏感性 |
|------|------|--------|
| `SOUL.md` | AI 人格和行为准则 | 🔓 公开 |
| `USER.md` | 用户信息和偏好 | 🔒 私密 |
| `IDENTITY.md` | AI 身份信息 | 🔓 公开 |
| `TOOLS.md` | 工具配置笔记 | 🔒 私密 |
| `AGENTS.md` | 工作区规范 | 🔓 公开 |
| `HEARTBEAT.md` | 心跳任务配置 | 🔓 公开 |
| `backup/openclaw.config.template.json` | 配置模板（密钥已脱敏） | ⚠️ 需填写 |
| `backup/restore-checklist.md` | 恢复检查清单 | 🔓 公开 |
| `backup/install-skills.sh` | 技能安装脚本 | 🔓 公开 |

### 需手动备份（敏感信息）

以下文件**未上传到 GitHub**，需自行安全保存：

```bash
#  credentials/ - 渠道凭证
~/.openclaw/credentials/

#  openclaw.json - 完整配置（含密钥）
~/.openclaw/openclaw.json

#  memory/main.sqlite - 会话记忆数据库
~/.openclaw/memory/main.sqlite
```

**建议：** 使用密码管理器（如 1Password、Bitwarden）保存敏感密钥。

---

## 🔧 详细恢复步骤

### 1. 获取 API 密钥

#### 阿里云 DashScope（通义千问）
1. 访问：https://dashscope.console.aliyun.com/
2. 登录阿里云账号
3. 创建/获取 API Key
4. 填入 `openclaw.json` 的 `models.providers.bailian.apiKey`

#### 飞书机器人
1. 访问：https://open.feishu.cn/app
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 配置事件订阅和机器人权限
5. 填入 `openclaw.json` 的 `channels.feishu` 部分

### 2. 安装扩展插件

```bash
cd ~/.openclaw/workspace
bash backup/install-skills.sh
```

或手动安装：
```bash
npm install -g @sliverp/qqbot
npm install -g @largezhou/ddingtalk
npm install -g @mocrane/wecom
npm install -g adp-openclaw
```

### 3. 验证恢复

```bash
# 检查配置
openclaw status

# 测试对话
openclaw chat "测试恢复是否成功"

# 检查记忆
ls -la ~/.openclaw/memory/
```

---

## 🚨 常见问题

### Q: GitHub Token 过期怎么办？
A: USER.md 中记录了 Token 过期时间。过期前：
```bash
# 生成新 Token
gh auth refresh

# 或手动更新 ~/.openclaw/openclaw.json 中的 GitHub 配置
```

### Q: 飞书机器人不响应？
A: 检查：
1. 飞书应用已发布
2. 事件订阅 URL 正确指向你的服务器
3. 机器人已添加到聊天

### Q: 记忆文件丢失？
A: `memory/main.sqlite` 是会话记忆数据库。如未备份，历史对话会丢失，但核心配置不受影响。

---

## 📅 备份维护

### 定期更新备份

```bash
cd ~/.openclaw/workspace

# 提交最新配置
git add .
git commit -m "backup: $(date +%Y-%m-%d)"

# 推送到 GitHub
git push origin main
```

### 建议备份频率
- **配置变更时**：立即备份
- **重要对话后**：更新 USER.md 和 MEMORY.md
- **每月**：检查 Token 有效期

---

## 🔐 安全提示

1. **不要将完整配置（含密钥）上传到公开仓库**
2. 使用 `backup/openclaw.config.template.json` 作为模板
3. 真实密钥保存在本地，用密码管理器保护
4. 定期更换 API Token
5. 启用 GitHub 两步验证

---

## 📞 需要帮助？

- OpenClaw 文档：https://docs.openclaw.ai
- 社区 Discord：https://discord.com/invite/clawd
- 技能市场：https://clawhub.com

---

_最后更新：2026-03-05_
_备份版本：v1.0_
