# MWC 2026 Agent News 网站

每天自动汇总 MWC 2026 与 AI Agent 相关新闻的聚合网站。

## 🌐 在线访问

**主站**: https://grand-zuccutto-93c8a0.netlify.app  
**RSS 订阅**: https://grand-zuccutto-93c8a0.netlify.app/rss.xml

---

## 📁 项目结构

```
mwc2026-agent-news/
├── index.html          # 主页面（包含新闻数据和展示逻辑）
├── rss.xml             # RSS 订阅源
├── _redirects          # Netlify 路由配置
├── update_news.py      # 新闻更新脚本
└── README.md           # 本文件
```

---

## 🔄 自动更新机制

### 定时任务
- **频率**: 每天上午 8:00 (北京时间)
- **任务 ID**: `5fb50b0e-bd99-42a8-9a07-d016d49f7227`
- **执行内容**: 
  1. 搜索 "MWC 2026 agent" 等关键词
  2. 更新 index.html 新闻数据
  3. 自动部署到 Netlify

### 手动更新
```bash
cd /Users/dingcaozhi/.openclaw/workspace/mwc2026-agent-news
python3 update_news.py
```

---

## ⚙️ 配置优化（可选）

### 启用 Brave Search API（推荐）
获取更好的新闻搜索结果：

```bash
openclaw configure --section web
# 输入 Brave Search API Key
```

获取 API Key: https://brave.com/search/api/

### 添加更多新闻源
在 `update_news.py` 中的 `NEWS_SOURCES` 列表中添加 RSS 源：

```python
NEWS_SOURCES = [
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
    {"name": "Your Source", "url": "https://example.com/rss"},
]
```

---

## 📊 当前功能

- ✅ 响应式新闻卡片布局
- ✅ 分类筛选（全部/技术/产品/商业/展会）
- ✅ 实时搜索
- ✅ RSS 订阅
- ✅ 每日自动更新
- ✅ 暗色主题 UI
- ✅ 移动端适配

---

## 🛠️ 技术栈

- **前端**: 原生 HTML5 + CSS3 + JavaScript
- **部署**: Netlify
- **自动化**: OpenClaw Cron + Agent
- **数据源**: Web Search API + RSS

---

## 📝 更新日志

### 2026-03-03
- 初始版本发布
- 12 条 MWC 2026 Agent 相关新闻
- 自动更新系统部署完成

---

**Maintained by**: AI Agent  
**Last Updated**: 2026-03-03
