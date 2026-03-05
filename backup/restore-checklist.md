# 🔍 恢复检查清单

完成系统重装后，按此清单逐项检查：

## ✅ 基础环境

- [ ] Node.js 20+ 已安装 (`node --version`)
- [ ] OpenClaw 已安装 (`openclaw --version`)
- [ ] Git 已配置 (`git --version`)
- [ ] SSH Key 已生成并添加到 GitHub

## ✅ 配置恢复

- [ ] `~/.openclaw/openclaw.json` 已创建
- [ ] 阿里云 DashScope API Key 已填写
- [ ] 飞书 App ID 和 Secret 已填写
- [ ] 网关 Token 已生成
- [ ] 配置文件语法正确（可用 `jq` 验证）

## ✅ 服务启动

- [ ] `openclaw gateway start` 执行成功
- [ ] `openclaw status` 显示正常
- [ ] 网关端口 18789 可访问

## ✅ 数据恢复

- [ ] workspace 目录已克隆
- [ ] SOUL.md 存在
- [ ] USER.md 存在
- [ ] IDENTITY.md 存在
- [ ] memory/ 目录存在（如有备份）

## ✅ 功能测试

- [ ] 发送测试消息到飞书
- [ ] AI 能正常回复
- [ ] 记忆功能正常
- [ ] 技能加载正常

## ✅ 安全加固

- [ ] GitHub 两步验证已启用
- [ ] API Key 权限最小化
- [ ] 敏感文件未公开
- [ ] 防火墙规则已配置

---

## 📝 备注

记录恢复过程中遇到的问题和解决方案：



---

_检查日期：________________
_检查人：________________
