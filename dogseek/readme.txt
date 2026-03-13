DogSeek skill 开发完成并测试通过！

**功能实现：**
- ✅ 使用 Scrapling 进行网页抓取（支持动态渲染）
- ✅ 使用 html2text 将 HTML 转换为 Markdown
- ✅ 噪声过滤：移除 script、style、广告、导航等元素
- ✅ 主要内容提取：识别 article、main、content 等标签
- ✅ 微信公众号文章优化处理

**文件结构：**
```
skills/dogseek/
├── dogseek.py      # 核心爬虫类
└── test_dogseek.py # 单元测试

dogseek/
├── dogseek.py
├── test_dogseek.py
├── design.md       # 设计文档
├── skill_config.json # OpenClaw 配置
├── requirements.txt
└── readme.txt
```

**测试验证：**
- ✅ 6 个单元测试全部通过
- ✅ HTML 到 Markdown 转换正确
- ✅ 噪声过滤功能正常
- ✅ 微信公众号文章格式处理正确
- ✅ 特殊字符处理正确

**依赖已安装：** scrapling, html2text, beautifulsoup4, playwright, browserforge, msgspec