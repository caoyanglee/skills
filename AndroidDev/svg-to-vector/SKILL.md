---
name: svg-to-vector
description: "Batch convert SVG files to Android VectorDrawable XML. Use when: converting SVG icons to Android XML; bulk SVG to vector drawable; svg2android batch; generating res/drawable XML from design assets; SVG folder to VectorDrawable."
argument-hint: "Path to folder containing SVG files (default: current workspace root)"
---

# SVG → Android VectorDrawable 批量转换

## 适用场景

- 需要将一批 SVG 图标转换成 Android `res/drawable/` 用的 VectorDrawable XML
- 设计资源交付，文件夹内有大量 `.svg` 文件
- 等效于 https://inloop.github.io/svg2android/ 的批量版能力

## 前置条件

- macOS/Linux 系统，Python 3（无需额外安装任何依赖）
- SVG 文件应为标准矢量图（支持 `<path>`, `<circle>`, `<rect>`, `<g>`, `<defs>`, `<clipPath>`）

## 使用步骤

### 1. 确认目标文件夹

用户给出包含 SVG 的文件夹路径（可以有子文件夹，脚本会递归扫描）。

### 2. 将脚本放到目标目录

把 [svg_to_vector.py](./scripts/svg_to_vector.py) 复制到目标 SVG 文件夹根目录，或直接在命令行通过 `--root` 参数指定路径。

```bash
cp ~/.copilot/skills/svg-to-vector/scripts/svg_to_vector.py /path/to/svg/folder/
cd /path/to/svg/folder
python3 svg_to_vector.py
```

或者不复制，直接从 skill 位置执行并传入 `--root` 参数：

```bash
python3 ~/.copilot/skills/svg-to-vector/scripts/svg_to_vector.py --root /path/to/svg/folder
```

### 3. 查看输出

脚本运行后会在目标文件夹内创建 `vectordrawable/` 子目录，所有生成的 XML 文件**平铺**其中（对应 Android `res/drawable/` 结构）。

终端输出示意：
```
  SKIP  media/play=true.svg
  SKIP  media/속성 1=1.svg
  ...
=======================================================
Converted : 429
Skipped   : 7
Errors    : 0
Output    : /path/to/svg/folder/vectordrawable
```

### 4. 文件名规则

| 处理 | 说明 |
|---|---|
| **跳过** | 文件名含非 ASCII 字符（中文/韩文）或 `=` |
| **小写化** | `MyIcon.svg` → `myicon` |
| **空格/横杠** → `_` | `edit icon_del.svg` → `edit_icon_del.xml` |
| **去除特殊字符** | 只保留 `[a-z0-9_]` |
| **重名碰撞** | 两个文件夹有同名 SVG → `sys_ic_rest.xml` + `sys_ic_rest_2.xml` |

### 5. 转换映射参考

| SVG 元素/属性 | VectorDrawable 输出 |
|---|---|
| `<path d="…">` | `<path android:pathData="…"/>` |
| `<circle cx cy r>` | 转为双弧线路径 `<path>` |
| `<rect x y width height>` | 转为矩形路径 `<path>` |
| `<g clip-path="url(#id)">` | `<group><clip-path …/> …</group>` |
| `<g>` 无 clip | 展平，直接处理子元素 |
| `fill` | `android:fillColor` |
| `fill-opacity` | `android:fillAlpha` |
| `fill-rule="evenodd"` | `android:fillType="evenOdd"` |
| `stroke` / `stroke-width` | `android:strokeColor` / `android:strokeWidth` |
| `<defs>` | 仅提取 clipPath 定义，不输出 |

## 常见问题

**Q: 生成的 XML 在 Android Studio 预览有问题？**
原 SVG 用了 `<linearGradient>` / `<mask>` / `<text>` 等 VectorDrawable 不支持的特性。脚本目前不转换这些，需手动处理。

**Q: 想保留子文件夹结构？**
打开脚本，找到 `OUTPUT_DIR = WORKSPACE / "vectordrawable"` 这一行，改为按原始相对路径输出即可（或告诉 Copilot 帮你修改脚本）。

**Q: 文件名含 `=` 的 SVG 被跳过了，我想转换它？**
先手动把文件名中的 `=` 替换成 `_` 之类的安全字符，再重新运行脚本。

## 脚本来源

[svg_to_vector.py](./scripts/svg_to_vector.py) — Python 3 stdlib only（`xml.etree.ElementTree`, `pathlib`, `re`）
