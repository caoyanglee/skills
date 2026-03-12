# Skills

个人常用技能库，涵盖 Android 开发、Apple/macOS 开发、通用文档处理、Flutter 开发以及开放平台集成等领域。

---

## 📁 目录结构

```
skills/
├── AndroidDev/       # Android 开发工具
├── AppleDev/         # macOS / Apple 开发指南
├── Common/           # 通用文档处理工具
├── FlutterDev/       # Flutter 开发（规划中）
└── OpenClaw/         # 开放平台集成工具
```

---

## 📦 技能清单

### 🤖 AndroidDev

| 技能 | 描述 | 语言 |
|------|------|------|
| [svg-to-vector](AndroidDev/svg-to-vector/) | 批量将 SVG 图标转换为 Android VectorDrawable XML，支持递归扫描、文件名规范化与碰撞检测 | Python |
| [nine-patch-analyzer](AndroidDev/nine-patch-analyzer/) | Android 点九图（.9.png）分析工具 | Python |

---

### 🍎 AppleDev

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [macos-native-ui](AppleDev/macos-native-ui/) | macOS 原生 UI 设计完全指南，遵循 Apple HIG，涵盖 SwiftUI、AppKit、Electron/Web 三大框架的最佳实践（系统颜色、SF Symbols、8pt 网格、弹簧动画等） | SwiftUI / AppKit / CSS |

---

### 📄 Common

| 技能 | 描述 | 语言 |
|------|------|------|
| [docx](Common/docx/) | Word 文档工具包：文本提取、文档生成（docx-js）、OpenXML 修改（WordFile 库）、修订追踪 | Python / JS |
| [pdf](Common/pdf/) | PDF 工具包：内容提取、表格提取、文档生成、合并拆分、表单填写、OCR，支持 CJK 字体 | Python |
| [pptx](Common/pptx/) | PowerPoint 工具包：幻灯片生成与修改、HTML→PPT 转换、文本替换、16 种预设配色方案 | Python / JS |
| [xlsx](Common/xlsx/) | Excel 工具包：数据分析、电子表格创建、公式完整性验证、LibreOffice 公式求值 | Python |
| [skill-creator](Common/skill-creator-0.1.0/) | 技能开发脚手架：新技能初始化、结构模板生成、打包与验证（6 步工作流） | Python |
| [find-skills](Common/find-skills/) | 技能发现工具：帮助找到可安装的 Skills，集成 Skills CLI 与 skills.sh 市场 | — |

---

### 🦋 FlutterDev

> **官方资源**: [flutter/skills](https://github.com/flutter/skills) - Flutter Agent Skills 官方仓库

| 技能 | 描述 |
|------|------|
| [flutter-accessibility](FlutterDev/flutter-accessibility/) | 配置 Flutter 应用程序以支持辅助技术（如屏幕阅读器）|
| [flutter-animation](FlutterDev/flutter-animation/) | 向 Flutter 应用添加动画效果 |
| [flutter-app-size](FlutterDev/flutter-app-size/) | 测量和减小 Flutter 应用包、APK 或 IPA 的大小 |
| [flutter-architecture](FlutterDev/flutter-architecture/) | 使用 Flutter 团队推荐的架构构建应用 |
| [flutter-caching](FlutterDev/flutter-caching/) | 在 Flutter 应用中缓存数据 |
| [flutter-concurrency](FlutterDev/flutter-concurrency/) | 在 Flutter 中在后台线程执行长时间运行的任务 |
| [flutter-databases](FlutterDev/flutter-databases/) | 在 Flutter 应用中使用数据库 |
| [flutter-environment-setup-linux](FlutterDev/flutter-environment-setup-linux/) | 配置 Linux 环境进行 Flutter 开发 |
| [flutter-environment-setup-macos](FlutterDev/flutter-environment-setup-macos/) | 配置 macOS 环境进行 Flutter 开发 |
| [flutter-environment-setup-windows](FlutterDev/flutter-environment-setup-windows/) | 配置 Windows 环境进行 Flutter 开发 |
| [flutter-http-and-json](FlutterDev/flutter-http-and-json/) | 在 Flutter 应用中发起 HTTP 请求和编解码 JSON |
| [flutter-layout](FlutterDev/flutter-layout/) | 使用 Flutter 的布局 widget 和约束系统构建应用布局 |
| [flutter-localization](FlutterDev/flutter-localization/) | 配置 Flutter 应用以支持不同的语言和地区 |
| [flutter-native-interop](FlutterDev/flutter-native-interop/) | 在 Flutter 应用中与 Android、iOS 和 Web 的原生 API 互操作 |
| [flutter-performance](FlutterDev/flutter-performance/) | 优化 Flutter 应用的性能 |
| [flutter-platform-views](FlutterDev/flutter-platform-views/) | 将原生视图添加到 Flutter 应用中 |
| [flutter-plugins](FlutterDev/flutter-plugins/) | 构建 Flutter 插件，为其他 Flutter 应用提供原生互操作 |
| [flutter-routing-and-navigation](FlutterDev/flutter-routing-and-navigation/) | 在 Flutter 应用中的不同页面/路由进行导航或深链接 |
| [flutter-state-management](FlutterDev/flutter-state-management/) | 在 Flutter 应用中管理状态 |
| [flutter-testing](FlutterDev/flutter-testing/) | 为 Flutter 添加单元测试、widget 测试或集成测试 |
| [flutter-theming](FlutterDev/flutter-theming/) | 使用 Flutter 的主题系统自定义应用主题 |

---

### 🔗 OpenClaw

飞书（Lark）集成工具集，涵盖文档、文件、消息、权限等多个场景。

| 技能 | 描述 | 类型 |
|------|------|------|
| [feishu-chat-history](OpenClaw/feishu-chat-history/) | 获取并总结飞书群聊历史记录、消息回顾 | 消息 |
| [feishu-cron-reminder](OpenClaw/feishu-cron-reminder/) | 创建定时任务，稳定投递周期性提醒到飞书会话 | 自动化 |
| [feishu-doc](OpenClaw/feishu-doc-1.2.7/) | 飞书文档/表单/表格/Wiki 内容读写，自动解析 URL 并转换为 Markdown | 文档 |
| [feishu-drive](OpenClaw/feishu-drive-1.0.0/) | 飞书云空间文件管理：上传/下载/移动/搜索文件、创建文件夹、管理元数据 | 文件 |
| [feishu-image](OpenClaw/feishu-image/) | 飞书图像发送工具：上传图片到飞书服务器并发送给用户或群组 | 媒体 |
| [feishu-perm](OpenClaw/feishu-perm/) | 飞书文件/文档权限管理：查看协作者、修改权限、共享设置 | 权限 |
| [feishu-screenshot](OpenClaw/feishu-screenshot/) | macOS 截屏并直接发送到飞书对话 | 媒体 |
| [feishu-send-file](OpenClaw/feishu-send-file/) | 将文件发送到飞书群聊或个人对话 | 文件 |

---

## 🔧 主要技术栈

| 类别 | 工具 / 库 |
|------|-----------|
| **Python** | pandas · openpyxl · python-docx · pypdf · pdfplumber · reportlab · python-pptx · pytesseract |
| **JavaScript** | Node.js · docx-js · slideConverter |
| **外部工具** | LibreOffice · pandoc · qpdf · poppler-utils · Tesseract OCR |
| **移动 / 桌面** | Android VectorDrawable · SwiftUI · AppKit |
| **平台集成** | 飞书开放平台 API |
