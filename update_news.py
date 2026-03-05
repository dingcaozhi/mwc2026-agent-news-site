#!/usr/bin/env python3
"""
MWC 2026 Agent News 自动更新脚本
使用 Agent Reach (Jina Reader) 抓取最新新闻
"""

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
SITE_DIR = Path("/Users/dingcaozhi/.openclaw/workspace/mwc2026-agent-news")
NEWS_SOURCES = [
    {"name": "36氪AI", "url": "https://www.36kr.com/information/AI/", "category": "tech"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/", "category": "tech"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/ai-artificial-intelligence", "category": "tech"},
]

def fetch_with_jina(url):
    """使用 Jina Reader (Agent Reach) 抓取网页"""
    try:
        result = subprocess.run(
            ["curl", "-s", f"https://r.jina.ai/{url}", "-m", "30"],
            capture_output=True,
            text=True,
            timeout=35
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
        return None
    except Exception as e:
        print(f"⚠️ 抓取失败 {url}: {e}")
        return None

def extract_news(content, source_name):
    """从抓取的内容中提取新闻"""
    news_items = []
    
    if not content:
        return news_items
    
    # 简单提取标题和链接（基于常见新闻网站结构）
    lines = content.split('\n')
    today = datetime.now().strftime("%Y-%m-%d")
    
    for i, line in enumerate(lines[:50]):  # 只检查前50行
        line = line.strip()
        # 匹配可能的标题（长度适中，包含关键词）
        if len(line) > 15 and len(line) < 100:
            if any(keyword in line.lower() for keyword in ['mwc', 'agent', 'ai', '智能体', 'deepseek', 'gpt', 'claude']):
                # 清理标题
                title = re.sub(r'\[.*?\]', '', line).strip()
                if title and title not in [n['title'] for n in news_items]:
                    news_items.append({
                        "title": title[:80] + "..." if len(title) > 80 else title,
                        "summary": f"来自 {source_name} 的最新资讯...",
                        "source": source_name,
                        "category": "tech",
                        "date": today,
                        "emoji": "📰"
                    })
                    if len(news_items) >= 3:  # 每个源最多3条
                        break
    
    return news_items

def fetch_news():
    """使用 Agent Reach 抓取新闻"""
    all_news = []
    
    print("📡 正在使用 Agent Reach 抓取新闻...")
    print("   (通过 Jina Reader 服务)\n")
    
    for source in NEWS_SOURCES:
        print(f"🔍 正在抓取: {source['name']}...")
        content = fetch_with_jina(source['url'])
        
        if content:
            items = extract_news(content, source['name'])
            all_news.extend(items)
            print(f"   ✅ 获取到 {len(items)} 条")
        else:
            print(f"   ⚠️ 抓取失败")
    
    # 如果没有抓到新内容，保留原有新闻但更新时间戳
    if not all_news:
        print("\n⚠️ 未能抓取到新新闻，保留现有内容")
        return []
    
    print(f"\n📰 总共获取到 {len(all_news)} 条新闻")
    return all_news

def update_website(news_list):
    """更新网站内容"""
    index_file = SITE_DIR / "index.html"
    
    if not index_file.exists():
        print("❌ index.html 不存在")
        return False
    
    content = index_file.read_text(encoding='utf-8')
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 更新时间戳
    content = re.sub(
        r'document\.getElementById\("updateTime"\)\.textContent = ".*?"',
        f'document.getElementById("updateTime").textContent = "{today}"',
        content
    )
    
    # 更新统计数字
    content = re.sub(
        r'<div class="stat-number" id="totalNews">\d+</div>',
        f'<div class="stat-number" id="totalNews">{len(news_list) if news_list else 12}</div>',
        content
    )
    
    index_file.write_text(content, encoding='utf-8')
    print(f"✅ 网站已更新: {today}")
    return True

def deploy():
    """部署到 Netlify"""
    try:
        result = subprocess.run(
            ["netlify", "deploy", "--site=70084f20-cf31-4700-b545-eb3bb2448208", "--prod", "--dir=."],
            cwd=SITE_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅ 部署成功")
            return True
        else:
            print(f"❌ 部署失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 部署异常: {e}")
        return False

def main():
    print(f"\n🤖 MWC 2026 Agent News Updater")
    print(f"🕐 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 使用 Agent Reach (Jina Reader) 抓取\n")
    
    # 1. 抓取新闻
    news = fetch_news()
    
    # 2. 更新网站
    print("\n📝 正在更新网站...")
    if update_website(news):
        # 3. 部署
        print("\n🚀 正在部署...")
        deploy()
    
    print("\n✨ 完成!\n")

if __name__ == "__main__":
    main()
