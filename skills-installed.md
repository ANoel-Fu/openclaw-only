# 已安装技能清单

安装时间：2026-03-09

## 🎨 设计与 UI (4 个)

| 技能 | 来源 | 安全风险 |
|------|------|----------|
| `frontend-design` | anthropics/skills | - |
| `web-design-guidelines` | vercel-labs/agent-skills | Medium |
| `ui-ux-pro-max` | nextlevelbuilder/ui-ux-pro-max-skill | Low |
| `agent-browser` | vercel-labs/agent-browser | ⚠️ **Critical** |

> ⚠️ **注意**: `agent-browser` 有 Critical 风险评级，使用时需审查代码

---

## 🛠️ 技能创建 (1 个)

| 技能 | 来源 | 安全风险 |
|------|------|----------|
| `skill-creator` | anthropics/skills | Low |

---

## 🔍 SEO 优化 (4 个)

| 技能 | 来源 | 安全风险 |
|------|------|----------|
| `ai-seo` | coreyhaines31/marketingskills | Medium |
| `programmatic-seo` | coreyhaines31/marketingskills | - |
| `seo-geo` | resciencelab/opc-skills | - |
| `seo-audit` | coreyhaines31/marketingskills | Medium |

---

## 📈 营销与增长 (8 个)

| 技能 | 来源 | 安全风险 |
|------|------|----------|
| `marketing-ideas` | coreyhaines31/marketingskills | - |
| `launch-strategy` | coreyhaines31/marketingskills | - |
| `pricing-strategy` | coreyhaines31/marketingskills | - |
| `content-strategy` | coreyhaines31/marketingskills | Medium |
| `social-content` | coreyhaines31/marketingskills | - |
| `baoyu-post-to-x` | jimliu/baoyu-skills | Medium |
| `paid-ads` | coreyhaines31/marketingskills | Low |
| `ai-marketing-videos` | inference-sh-8/skills | ⚠️ **Critical** |

> ⚠️ **注意**: `ai-marketing-videos` 有 Critical 风险评级 + 1 个 Socket 警报，使用前务必审查

---

## 📊 商业分析 (2 个)

| 技能 | 来源 | 安全风险 |
|------|------|----------|
| `market-sizing-analysis` | wshobson/agents | Low |
| `startup-metrics-framework` | wshobson/agents | Low |

---

## 🔬 研究与沟通 (3 个)

| 技能 | 来源 | 安全风险 |
|------|------|----------|
| `deep-research` | 199-biotechnologies/claude-deep-research-skill | - |
| `professional-communication` | softaworks/agent-toolkit | - |
| `tailored-resume-generator` | composiohq/awesome-claude-skills | Low |

---

## 📋 总计

- **新安装**: 22 个技能
- **已有技能**: 13 个 (capability-evolver, finance-news, find-skills, github, gog, akshare-stock, notion, obsidian, skill-vetter, stock-watcher, summarize, tavily, weather, tencentcloud-lighthouse-skill)
- **合计**: 35 个技能

---

## ⚠️ 安全提醒

以下技能有较高安全风险，建议在使用前审查源码：

1. **`agent-browser`** - Critical Risk (浏览器自动化，权限较高)
2. **`ai-marketing-videos`** - Critical Risk + 1 Socket Alert

---

## 📁 技能位置

- 新技能：`~/.openclaw/workspace/.agents/skills/`
- 原有技能：`~/.openclaw/workspace/skills/`

---

## 🚀 下一步建议

1. 审查高风险技能的源码
2. 测试核心工作流（设计 → SEO → 营销 → 发布）
3. 使用 `skill-creator` 沉淀你的专属工作流
4. 配置 `agent-browser` 配合 Chrome Extension 使用
