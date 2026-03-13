# DogSeek - OpenClaw Web Content Scraper Skill

## 项目概述

DogSeek 是一个专为 OpenClaw 设计的网页内容抓取技能，使用 **Scrapling** 和 **html2text** 实现高效的网页内容提取和 Markdown 转换。特别针对微信公众号文章进行了优化处理。

---

## 开发过程总结

### 1. 需求分析
- **目标**: 开发一个供 OpenClaw 调用的 skill，实现网页抓取、噪声过滤和 Markdown 转换
- **核心功能**: 
  - 使用 Scrapling 进行网页内容抓取（支持动态渲染）
  - 使用 html2text 将 HTML 转换为 Markdown
  - 过滤噪声元素（script、style、广告等）
  - 提取主要内容
  - 特别优化微信公众号文章分析

### 2. 技术选型
| 组件 | 用途 |
|------|------|
| **Scrapling** | 强大的网页抓取库，支持动态渲染和反爬绕过 |
| **html2text** | HTML 到 Markdown 的转换工具 |
| **BeautifulSoup4** | HTML 解析和内容提取 |

### 3. 核心类设计：DogSeekScraper

```python
class DogSeekScraper:
    """网页内容抓取器，使用 Scrapling 和 html2text"""
    
    NOISE_SELECTORS = [...]      # 噪声元素选择器列表
    WECHAT_NOISE_SELECTORS = [...]  # 微信特有噪声
    
    def __init__(self):           # 初始化 html2text 配置
    def fetch_page(self, url)     # 抓取网页内容
    def filter_noise(html)        # 过滤噪声元素（正则）
    def extract_main_content(html)# 提取主要内容（BeautifulSoup）
    def convert_to_markdown(html) # HTML 转 Markdown
    def scrape(url)               # 完整抓取流程
```

### 4. 关键实现细节

#### a) html2text API 修复
**问题**: `html2text` 库的 API 更新，旧版使用 `.convert()`，新版使用 `.handle()`

**修复过程**:
- 初始代码（错误）：`markdown = self.h2t.convert(main_content)`
- 修复后：`markdown = self.h2t.handle(main_content)`

#### b) 列表格式匹配问题
**问题**: html2text 输出带前导空格的列表项 `  * 项目一`，测试断言无法匹配

**解决方案**: 使用正则表达式支持可选前导空格
```python
import re
has_list = bool(re.search(r'[\s]*[*-] 项目一', markdown))
self.assertTrue(has_list, f"应保持列表格式。实际输出：{repr(markdown)}")
```

### 5. 依赖安装过程

由于 Scrapling 的依赖链，需要按顺序安装多个包：
1. curl_cffi - Scrapling 基础依赖
2. playwright - 浏览器自动化支持
3. playwright install chromium - 安装 Chromium 引擎
4. browserforge - User-Agent 指纹生成
5. msgspec - 数据结构处理
6. html2text 和 beautifulsoup4

---

## 验证结果

### 单元测试执行结果

所有测试通过：
- test_scraper_initialization ... ok
- test_filter_noise_method ... ok
- test_extract_main_content ... ok
- test_html2text_conversion ... ok
- test_noise_filtering ... ok
- test_wechat_article_format ... ok
- test_real_url_fetch ... skipped (网络测试)

**总结**: 6 个测试，0 个失败，0 个错误

### 测试覆盖内容

| 测试项 | 验证点 | 结果 |
|--------|--------|------|
| test_scraper_initialization | Scraper 正确初始化 | OK |
| test_filter_noise_method | 噪声元素过滤功能 | OK |
| test_extract_main_content | 主要内容提取逻辑 | OK |
| test_html2text_conversion | HTML 到 Markdown 转换 | OK |
| test_noise_filtering | script/style 移除验证 | OK |
| test_wechat_article_format | 微信公众号文章处理 | OK |

---

## 使用说明

### Python API 使用

```python
from dogseek import DogSeekScraper

# 创建爬虫实例
scraper = DogSeekScraper()

# 抓取网页并转换为 Markdown
markdown_content = scraper.scrape("https://example.com")

# 或者分步操作
html = scraper.fetch_page("https://example.com")
filtered = scraper.filter_noise(html)
main_content = scraper.extract_main_content(filtered)
markdown = scraper.convert_to_markdown(main_content)
```

### CLI 使用

```bash
python3 dogseek.py https://mp.weixin.qq.com/example
```

---

## 文件结构

```
skills/dogseek/
├── dogseek.py          # 核心爬虫类实现
├── test_dogseek.py     # 单元测试
└── README.md           # 本文档

dogseek/                # 完整项目目录
├── dogseek.py          # 核心实现
├── test_dogseek.py     # 测试文件
├── design.md           # 设计文档
├── skill_config.json   # OpenClaw 配置
└── requirements.txt    # Python 依赖
```

---

## 已知问题与解决

### 1. Python 字节码缓存问题
**现象**: 修改代码后测试仍报错旧错误  
**解决**: 清除 __pycache__ 目录

### 2. html2text API 兼容性
**现象**: 'HTML2Text' object has no attribute 'convert'  
**解决**: 使用 .handle() 替代 .convert()

---

## 依赖清单

| 包名 | 用途 |
|------|------|
| scrapling | 网页抓取 |
| html2text | HTML 转 Markdown |
| beautifulsoup4 | HTML 解析 |
| playwright | 浏览器自动化 |
| browserforge | User-Agent 生成 |
| curl_cffi | cURL 绑定 |
| msgspec | 数据结构处理 |

---

## 后续改进方向

1. **异步支持**: 添加 async/await 版本的爬虫方法
2. **缓存机制**: 实现网页内容缓存，减少重复请求
3. **更多格式支持**: 扩展支持 PDF、Word 等文档类型
4. **智能摘要**: 集成大模型生成内容摘要

---
*文档版本：1.0*  
*最后更新：2026-03-12*
