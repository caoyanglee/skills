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

> 🚧 规划中，暂无内容。

---

### 🔗 OpenClaw

| 技能 | 描述 | 语言 |
|------|------|------|
| [feishu-image](OpenClaw/feishu-image/) | 飞书图像发送工具：上传图片到飞书服务器并发送给用户或群组，支持 CLI、OpenClaw 集成、Node.js 模块三种用法 | JavaScript |

---

## 🔧 主要技术栈

| 类别 | 工具 / 库 |
|------|-----------|
| **Python** | pandas · openpyxl · python-docx · pypdf · pdfplumber · reportlab · python-pptx · pytesseract |
| **JavaScript** | Node.js · docx-js · slideConverter |
| **外部工具** | LibreOffice · pandoc · qpdf · poppler-utils · Tesseract OCR |
| **移动 / 桌面** | Android VectorDrawable · SwiftUI · AppKit |
| **平台集成** | 飞书开放平台 API |
