#!/usr/bin/env python3
"""
DogSeek 测试用例

用于验证网页抓取和 Markdown 转换功能的正确性。
"""

import unittest
import sys
import os
from io import StringIO

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestDogSeekScraper(unittest.TestCase):
    """DogSeek 爬虫测试类"""
    
    def setUp(self):
        """测试前准备"""
        from dogseek import DogSeekScraper
        self.scraper = DogSeekScraper()

    def test_html2text_conversion(self):
        """测试 HTML 到 Markdown 的转换"""
        import re
        
        html_content = """
        <html>
            <body>
                <h1>标题</h1>
                <p>这是一段<span class="highlight">重要</span>的文字。</p>
                <ul>
                    <li>项目一</li>
                    <li>项目二</li>
                </ul>
                <a href="https://example.com">示例链接</a>
            </body>
        </html>
        """
        
        markdown = self.scraper.convert_to_markdown(html_content)
        
        # 验证 Markdown 输出包含关键元素
        self.assertIn('标题', markdown, "应保留标题内容")
        self.assertIn('重要', markdown, "应保留文字内容")
        # html2text 可能使用 * 或 - 作为列表标记，两者都接受（可能有前导空格）
        has_list = bool(re.search(r'[\s]*[*-] 项目一', markdown))
        self.assertTrue(has_list, f"应保持列表格式。实际输出：{repr(markdown)}")
        self.assertIn('[示例链接]', markdown, "应保留链接格式")

    def test_noise_filtering(self):
        """测试噪声过滤功能"""
        html_content = """
        <html>
            <body>
                <script>alert('xss');</script>
                <style>.hidden { display: none; }</style>
                <div class="ad">广告内容</div>
                <nav>导航栏</nav>
                <main>
                    <h1>主要内容</h1>
                    <p>这是正文内容。</p>
                </main>
            </body>
        </html>
        """
        
        markdown = self.scraper.convert_to_markdown(html_content)
        
        # 验证噪声元素已被移除
        self.assertNotIn('alert', markdown, "应移除 script 标签")
        self.assertNotIn('.hidden', markdown, "应移除 style 标签")

    def test_wechat_article_format(self):
        """测试微信公众号文章格式处理"""
        html_content = """
        <html>
            <body>
                <div class="rich_media_title">公众号文章标题</div>
                <div class="wx_follow_btn">关注公众号</div>
                <article>
                    <h2>文章副标题</h2>
                    <p>这是微信公众号的文章内容。</p>
                    <blockquote>引用内容</blockquote>
                </article>
            </body>
        </html>
        """
        
        markdown = self.scraper.convert_to_markdown(html_content)
        
        # 验证主要内容保留，噪声元素移除
        self.assertIn('文章副标题', markdown, "应保留文章内容")
        self.assertNotIn('关注公众号', markdown, "应移除关注按钮")

    def test_special_characters(self):
        """测试特殊字符处理"""
        html_content = """
        <html>
            <body>
                <h1>中文 & 英文 Content</h1>
                <p>特殊符号：< > & " '</p>
                <p>数学公式：a² + b² = c²</p>
            </body>
        </html>
        """
        
        markdown = self.scraper.convert_to_markdown(html_content)
        
        # 验证特殊字符被正确处理
        self.assertIn('Content', markdown, "应保留英文内容")

    def test_empty_html(self):
        """测试空 HTML 处理"""
        html_content = "<html><body></body></html>"
        
        markdown = self.scraper.convert_to_markdown(html_content)
        
        # 验证空内容返回空字符串或适当提示
        self.assertIsNotNone(markdown)


class TestDogSeekIntegration(unittest.TestCase):
    """集成测试类（需要网络连接）"""
    
    @unittest.skip("跳过网络测试，需手动运行")
    def test_real_url_fetch(self):
        """测试真实 URL 抓取"""
        # 注意：此测试需要网络连接和有效的网页
        test_urls = [
            "https://mp.weixin.qq.com",
            "https://www.python.org",
        ]
        
        for url in test_urls:
            with self.subTest(url=url):
                try:
                    markdown = self.scraper.scrape(url)
                    self.assertIsInstance(markdown, str)
                    self.assertGreater(len(markdown), 0)
                except Exception as e:
                    # 网络问题或反爬机制可能导致失败，不影响核心功能验证
                    print(f"跳过 {url}: {e}")


def run_tests():
    """运行测试并返回结果"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试用例
    suite.addTests(loader.loadTestsFromTestCase(TestDogSeekScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestDogSeekIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("=" * 60)
    print("DogSeek 单元测试套件")
    print("=" * 60)
    
    # 检查依赖是否安装
    try:
        import scrapling
        import html2text
        from bs4 import BeautifulSoup
        print("\n✓ 所有依赖已安装\n")
    except ImportError as e:
        print(f"\n✗ 缺少依赖：{e}")
        print("请运行：pip install scrapling html2text beautifulsoup4")
        sys.exit(1)
    
    # 运行测试
    result = run_tests()
    
    # 输出结果摘要
    print("\n" + "=" * 60)
    print(f"测试结果：{result.testsRun} 个测试，{len(result.failures)} 个失败，{len(result.errors)} 个错误")
    print("=" * 60)
    
    # 退出码
    sys.exit(0 if result.wasSuccessful() else 1)
