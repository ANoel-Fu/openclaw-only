# Lightpanda Browser 配置完成

**安装时间：** 2026-03-18  
**状态：** ✅ 正常运行

---

## 📦 安装位置

| 组件 | 路径 |
|------|------|
| Lightpanda 二进制 | `/root/.local/bin/lightpanda` |
| OpenClaw 技能 | `/root/.openclaw/workspace/skills/lightpanda/` |
| CDP 服务器 | `ws://127.0.0.1:9222` |

---

## 🚀 启动命令

### 后台运行（推荐）
```bash
# 启动 CDP 服务器
/root/.local/bin/lightpanda serve --host 127.0.0.1 --port 9222 --log_level info &

# 验证运行
curl http://127.0.0.1:9222/json/version
```

### 前台运行（调试用）
```bash
/root/.local/bin/lightpanda serve --host 127.0.0.1 --port 9222 --log_level debug
```

---

## 🔧 配置选项

### 基本选项
- `--host` - 监听地址（默认：127.0.0.1）
- `--port` - 监听端口（默认：9222）
- `--log_level` - 日志级别：info|debug|warn|error
- `--log_format` - 日志格式：pretty|json
- `--timeout` - 连接超时（秒，默认：10）

### 高级选项
- `--obey_robots` - 遵守 robots.txt
- `--http_proxy` - HTTP 代理
- `--http_max_concurrent` - 最大并发请求数（默认：10）
- `--cdp_max_connections` - 最大 CDP 连接数（默认：16）

---

## 📝 使用示例

### 方式 1：直接 Fetch（最简单）
```bash
# 获取网页内容（Markdown 格式）
lightpanda fetch --dump markdown https://example.com

# 获取 HTML
lightpanda fetch --dump html https://example.com

# 遵守 robots.txt
lightpanda fetch --dump markdown --obey_robots https://example.com
```

### 方式 2：Playwright 连接
```javascript
const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.connectOverCDP({
    endpointURL: 'ws://127.0.0.1:9222',
  });

  const context = await browser.newContext({});
  const page = await context.newPage();

  await page.goto('https://example.com');
  const title = await page.title();
  const content = await page.textContent('body');

  console.log(JSON.stringify({ title, content }));

  await page.close();
  await context.close();
  await browser.close();
})();
```

### 方式 3：Puppeteer 连接
```javascript
const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://127.0.0.1:9222'
  });

  const context = await browser.createBrowserContext();
  const page = await context.newPage();

  await page.goto('https://example.com', { waitUntil: 'networkidle0' });
  const title = await page.title();

  console.log(JSON.stringify({ title }));

  await page.close();
  await context.close();
  await browser.close();
})();
```

---

## 🎯 OpenClaw 集成

### 在 OpenClaw 中使用 Lightpanda

Lightpanda 技能已安装在：
`/root/.openclaw/workspace/skills/lightpanda/`

**使用场景：**
- 网页数据抓取
- 自动化测试
- AI 代理浏览
- 批量页面处理

**优势：**
- ⚡ 比 Chrome 快 11 倍
- 💾 内存占用少 9 倍
- 🚀 即时启动
- 🔌 CDP 兼容（Playwright/Puppeteer）

---

## ⚠️ 注意事项

### 限制
1. **单连接单页面** - 每个 CDP 连接只能创建 1 个 context 和 1 个 page
2. **无多标签** - 需要多页面时启动多个进程（不同端口）
3. **Web API 支持** - 部分 Web API 仍在开发中
4. **Google 搜索** - Google 会阻止 Lightpanda，建议使用 DuckDuckGo

### 最佳实践
- ✅ 保持 WebSocket 连接打开（浏览会话期间）
- ✅ 每次连接创建新的 context 和 page
- ✅ 使用完毕后关闭 page 和 context
- ✅ 多页面需求：启动多个进程（端口 9222, 9223, 9224...）

---

## 🛠️ 故障排查

### 检查服务状态
```bash
# 检查进程
ps aux | grep lightpanda

# 检查端口
netstat -tlnp | grep 9222

# 测试连接
curl http://127.0.0.1:9222/json/version
```

### 更新 Lightpanda
```bash
# 重新运行安装脚本（获取最新版本）
bash /root/.openclaw/workspace/skills/lightpanda/scripts/install.sh
```

### 常见问题

**Q: 连接被拒绝**
```bash
# 确保服务正在运行
/root/.local/bin/lightpanda serve --host 127.0.0.1 --port 9222 &
```

**Q: 页面加载失败**
- 检查网络连接
- 尝试添加 `--obey_robots` 选项
- 查看日志：`--log_level debug`

**Q: JavaScript 执行错误**
- Lightpanda 的 JS 引擎仍在开发中
- 某些复杂网站可能不兼容
- 考虑使用 Chrome 作为备选

---

## 📚 相关资源

- **GitHub:** https://github.com/lightpanda-io/browser
- **文档:** https://lightpanda.io/docs
- **Docker:** https://hub.docker.com/r/lightpanda/browser
- **Discord:** https://discord.gg/K63XeymfB5

---

**配置完成时间：** 2026-03-18  
**最后测试：** ✅ 正常运行
