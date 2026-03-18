# AI/科技日报 - 数据来源配置

## 📰 综合新闻门户（科技频道）

### 腾讯新闻
- **科技频道**: `https://news.qq.com/ch/tech`
- **互联网频道**: `https://news.qq.com/ch/internet`
- **RSS**: `https://rsshub.app/qq/news/tech`

### 网易新闻
- **科技频道**: `https://tech.163.com/`
- **IT 频道**: `https://tech.163.com/it/`
- **互联网**: `https://tech.163.com/internet/`
- **RSS**: `https://rsshub.app/netease/news/tech`

### 新浪科技
- **主站**: `https://tech.sina.com.cn/`
- **互联网**: `https://tech.sina.com.cn/internet/`
- **IT 时代**: `https://tech.sina.com.cn/it/`
- **RSS**: `https://rsshub.app/sina/tech`

### 搜狐科技
- **科技频道**: `https://www.sohu.com/channel/tech`
- **RSS**: `https://rsshub.app/sohu/tech`

---

## 🚀 垂直科技媒体

### 36 氪
- **主站**: `https://36kr.com/`
- **快讯**: `https://36kr.com/newsflashes`
- **RSS**: `https://rsshub.app/36kr`

### 虎嗅
- **主站**: `https://www.huxiu.com/`
- **RSS**: `https://rsshub.app/huxiu/article`

### 界面新闻·科技
- **科技频道**: `https://www.jiemian.com/channels/4.html`
- **RSS**: `https://rsshub.app/jiemian/tech`

### 钛媒体
- **主站**: `https://www.tmtpost.com/`
- **RSS**: `https://rsshub.app/tmtpost/author`

### 品玩
- **主站**: `https://www.pingwest.com/`
- **RSS**: `https://rsshub.app/pingwest`

---

## 🤖 AI 专业媒体

### 机器之心
- **主站**: `https://www.jiqizhixin.com/`
- **RSS**: `https://rsshub.app/jiqizhixin/article`

### 量子位
- **主站**: `https://www.qbitai.com/`
- **公众号**: 量子位 (微信)
- **RSS**: `https://rsshub.app/qbitai`

### 新智元
- **主站**: `https://www.newai.pro/`
- **公众号**: 新智元 (微信)

### AI 科技大本营
- **主站**: `https://zhuanlan.zhihu.com/ai-tech`
- **公众号**: AI 科技大本营

---

## 📱 科技自媒体/博客

### 少数派
- **主站**: `https://sspai.com/`
- **RSS**: `https://rsshub.app/sspai/latest`

### 爱范儿
- **主站**: `https://www.ifanr.com/`
- **RSS**: `https://rsshub.app/ifanr`

### 差评
- **主站**: `https://www.chaping.cn/`
- **公众号**: 差评

### 科技美学
- **主站**: `https://www.kejimeixue.com/`

---

## 🌐 国际科技媒体（中文）

### TechCrunch 中文
- **主站**: `https://www.techcrunchchina.cn/`

### CNET 中文
- **主站**: `https://www.cnet.com/`

### The Verge（英文）
- **主站**: `https://www.theverge.com/`
- **RSS**: `https://rsshub.app/theverge`

### Wired（英文）
- **主站**: `https://www.wired.com/`
- **RSS**: `https://rsshub.app/wired`

---

## 📊 行业数据/报告

### 艾瑞咨询
- **主站**: `https://www.iresearch.com.cn/`

### 易观分析
- **主站**: `https://www.analysys.cn/`

### QuestMobile
- **主站**: `https://www.questmobile.com.cn/`

### 中国信通院
- **主站**: `https://www.caict.ac.cn/`

---

## 🔧 技术社区

### Hacker News
- **主站**: `https://news.ycombinator.com/`
- **RSS**: `https://rsshub.app/hackernews`

### GitHub Trending
- **主站**: `https://github.com/trending`
- **RSS**: `https://rsshub.app/github/trending/daily`

### V2EX
- **主站**: `https://www.v2ex.com/`
- **RSS**: `https://rsshub.app/v2ex/topics`

### 掘金
- **主站**: `https://juejin.cn/`
- **RSS**: `https://rsshub.app/juejin/category/all`

---

## 📋 使用建议

### 1. RSS 聚合
使用 RSSHub 统一获取各平台 RSS 源，避免直接抓取 HTML。

### 2. 去重策略
- 按标题相似度去重（阈值 85%）
- 按内容指纹去重
- 同一事件多源报道合并

### 3. 分类标签
- `#AI` - 人工智能相关
- `#互联网` - 互联网公司动态
- `#硬件` - 手机/芯片/消费电子
- `#投资` - 融资/并购/IPO
- `#政策` - 行业监管/政策
- `#国际` - 海外科技动态

### 4. 优先级权重
```
高优先级：36 氪、虎嗅、机器之心、量子位
中优先级：腾讯科技、网易科技、新浪科技
低优先级：其他综合门户
```

### 5. 更新频率
- 快讯类：每 15 分钟
- 深度文章：每 2 小时
- 日报汇总：每日 9:00 AM

---

## 🛠️ 自动化配置

如需使用 OpenClaw 的 cron 技能定时抓取，可配置：

```yaml
# ~/.openclaw/workspace/config/tech-daily-cron.yaml
schedule: "0 9 * * *"  # 每天上午 9 点
sources:
  - name: 36kr
    url: https://rsshub.app/36kr
  - name: huxiu
    url: https://rsshub.app/huxiu/article
  - name: jiqizhixin
    url: https://rsshub.app/jiqizhixin/article
output:
  format: markdown
  channel: feishu  # 或其他通知渠道
```

---

*最后更新：2026-03-18*
