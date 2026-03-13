---
name: "dogseek"
description: "🐶 网页内容抓取工具 - 支持微信公众号、新闻文章、技术博客等，自动提取正文并转换为 Markdown 格式"
user-invocable: true
metadata:{"requires":{"bins":["python3"]}} 
aliases: ["webfetch", "article-scraper", "content-extractor"]
---

# 🐶 DogSeek - 网页内容抓取工具

**一句话**: 丢给 dogseek 一个 URL，它帮你提取纯净的文章内容！

## 🔧 技能指令

当需要总结网页、公众号文章或博客时：

```bash
python3 {{skill_path}}/dogseek.py {{url}}
```

## 💡 使用场景

- 📰 **微信公众号文章** - 自动过滤广告和干扰元素
- 🌐 **新闻网站** - 提取正文，去除导航和侧边栏
- 🧑‍💻 **技术博客** - 保留代码块格式
- 📄 **任意网页** - 智能识别主要内容区域

## ✨ 特色功能

1. **自动去噪**: 移除广告、弹窗、无关链接
2. **Markdown 输出**: 保留标题层级、列表、代码块
3. **微信公众号优化**: 特别处理微信文章的特殊格式
4. **反爬绕过**: 智能 User-Agent，支持动态渲染页面
5. **容错机制**: 自动识别主要内容区域

## 📝 示例用法

```bash
# 抓取公众号文章
python3 ~/.openclaw/skills/dogseek/dogseek.py https://mp.weixin.qq.com/s/xxx

# 抓取技术博客
python3 ~/.openclaw/skills/dogseek/dogseek.py https://dev.to/article-title

# 抓取新闻网站
python3 ~/.openclaw/skills/dogseek/dogseek.py https://news.example.com/story
```

## 🛠️ 技术实现

- **Scrapling**: 强大的网页抓取引擎，支持动态渲染和反爬绕过
- **html2text**: HTML → Markdown 转换
- **BeautifulSoup4**: HTML 解析和内容提取
- **智能过滤**: 自动识别并移除噪声元素（广告、导航等）

## 🎯 输出格式

```markdown
# 文章标题

作者 | 发布时间

正文内容...

- 列表项一
- 列表项二

> 引用内容

**代码块示例**
```python
print("Hello World")
```
```

## ⚡ 快速上手

1. **直接调用**: `dogseek https://example.com`
2. **自动识别**: 支持微信公众号、知乎、掘金等主流平台
3. **纯净输出**: 只返回核心内容，无广告干扰

---

*版本：1.0 | 最后更新：2026-03-13*
