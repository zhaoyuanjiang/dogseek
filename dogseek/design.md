# DogSeek - Web Content Scraper for OpenClaw

## 项目简介

dogseek 是一个专为 OpenClaw 设计的网页内容抓取技能，使用高效的 Scrapling 爬虫和 html2text 库，将网页内容转换为纯净的 Markdown 格式，便于大模型进行分析和总结。

**核心功能**:
- 智能网页内容抓取（支持抗反爬机制）
- JavaScript 渲染支持
- 噪声过滤（去除广告、导航栏、侧边栏等无关元素）
- HTML 到 Markdown 的高质量转换
- 特别优化微信公众号文章分析

## 环境安装

### 1. 安装 Python 依赖

```bash
pip install scrapling html2text
```

### 2. 安装 Scrapling 浏览器引擎

Scrapling 需要浏览器引擎来渲染 JavaScript 页面：

```bash
scrapling install
```

这将自动下载并配置所需的浏览器驱动（Chrome/Firefox）。

### 3. 验证安装

```bash
python3 -c "import scrapling; import html2text; print('Dependencies OK')"
```

## OpenClaw 配置指南

将 dogseek 技能添加到 OpenClaw 配置中：

1. 打开或创建 `openclaw.json` 配置文件
2. 在 `skills.paths` 中添加 dogseek 路径：

```json
{
  "skills": {
    "paths": ["./skills/dogseek"]
  }
}
```

3. 确保 `skill_config.json` 文件存在于 dogseek 目录中

## 使用方法

### 基本用法

```bash
python3 dogseek.py https://example.com
```

### 微信公众号文章分析示例

```bash
# 抓取并转换公众号文章为 Markdown
python3 dogseek.py https://mp.weixin.qq.com/s/xxxxx
```

### 输出格式

输出为纯 Markdown 文本，包含：
- 标题和正文内容
- 列表和引用块
- 链接（保留原始 URL）
- 表格数据

## 文件结构

```
skills/dogseek/
├── dogseek.py          # 主程序脚本
├── requirements.txt    # Python 依赖清单
├── test_dogseek.py     # 测试用例
└── skill_config.json   # OpenClaw 技能注册配置
```

## 技术栈

- **Scrapling**: 高效爬虫库，支持抗反爬和 JS 渲染
- **html2text**: HTML 到 Markdown 转换工具
- **Python 3.8+**: 编程语言

## 常见问题

### Q: 为什么抓取失败？
A: 检查网络连接，确认 Scrapling 浏览器引擎已正确安装（运行 `scrapling install`）。

### Q: 如何自定义噪声过滤规则？
A: 修改 dogseek.py 中的 `filter_noise()` 函数，添加或调整 CSS 选择器。

### Q: 支持哪些网站类型？
A: 支持所有公开网页，特别优化了微信公众号、新闻站点和博客平台。

## License

MIT License
