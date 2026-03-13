#!/usr/bin/env python3
"""
DogSeek - Web Content Scraper for OpenClaw

使用 Scrapling 和 html2text 抓取网页内容并转换为 Markdown 格式。
特别优化微信公众号文章分析。
"""

import sys
import argparse
import json
import os
import re

try:
    from scrapling import Fetcher
except ImportError:
    print("错误：请先安装依赖 - pip install scrapling html2text")
    sys.exit(1)

try:
    import html2text
except ImportError:
    print("错误：请先安装依赖 - pip install scrapling html2text")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("错误：需要安装 beautifulsoup4 - pip install beautifulsoup4")
    sys.exit(1)


class DogSeekScraper:
    """网页内容抓取器，使用 Scrapling 和 html2text"""
    
    NOISE_SELECTORS = [
        'script', 'style', 'noscript', 'svg', 'iframe',
        '.ad', '.advertisement', '[class*="ad"]',
        '.nav', '.navigation', '[class*="nav"]',
        '.sidebar', '.aside', '[class*="sidebar"]',
        '.footer', '[class*="footer"]',
    ]

    def __init__(self):
        """初始化爬虫和 html2text 配置"""
        self.fetcher = Fetcher()
        
        # 配置 html2text
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False      # 保留链接
        self.h2t.ignore_images = True      # 忽略图片
        self.h2t.bypass_tables = False     # 保留表格结构
        self.h2t.body_width = 0            # 不限制换行宽度

    def fetch_page(self, url: str) -> str:
        """抓取网页内容"""
        try:
            response = self.fetcher.get(url)
            # Scrapling Response 使用 status 属性而非 status_code
            if response.status != 200:
                raise ValueError(f"获取网页失败，状态码 {response.status}")
            # 使用 Scrapling 的选择器获取 body 内容
            return response.css("body").get() or response.text
        except Exception as e:
            raise RuntimeError(f"抓取失败 {url}: {str(e)}")

    def filter_noise(self, html_content: str) -> str:
        """过滤噪声元素"""
        noise_patterns = [
            r'<script[^>]*>.*?</script>',
            r'<style[^>]*>.*?</style>',
            r'<!--.*?-->',
        ]
        content = html_content
        for pattern in noise_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        return content

    def extract_main_content(self, html_content: str) -> str:
        """提取主要内容"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 常用的内容区域选择器
        CONTENT_SELECTORS = [
            'article', 'main', '.content', '.post', '#content', '#main'
        ]
        
        main_content = None
        for selector in CONTENT_SELECTORS:
            elements = soup.select(selector)
            if elements:
                main_content = elements[0]
                break
        
        # 如果没有找到特定内容区域，使用 body 或整个文档
        if not main_content:
            main_content = soup.body or soup
        
        # 移除噪声元素
        for element in main_content.select(', '.join(self.NOISE_SELECTORS)):
            element.decompose()
        
        return str(main_content) if main_content else ''

    def convert_to_markdown(self, html_content: str) -> str:
        """将 HTML 转换为 Markdown"""
        filtered_html = self.filter_noise(html_content)
        main_content = self.extract_main_content(filtered_html)
        markdown = self.h2t.handle(main_content)
        return markdown.strip()

    def scrape(self, url: str) -> str:
        """完整抓取流程：获取网页并转换为 Markdown"""
        print(f"正在抓取：{url}")
        html = self.fetch_page(url)
        return self.convert_to_markdown(html)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='DogSeek - 使用 Scrapling 和 html2text 抓取网页并转换为 Markdown'
    )
    parser.add_argument('url', help='要抓取的网页 URL')
    args = parser.parse_args()
    
    scraper = DogSeekScraper()
    
    try:
        markdown_content = scraper.scrape(args.url)
        print("\n" + "="*50)
        print("Markdown 内容:")
        print("="*50)
        print(markdown_content)
        print("="*50)
    except Exception as e:
        print(f"\n错误：{str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
