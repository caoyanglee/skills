---
name: macos-native-ui
description: >
  Expert guide for designing and implementing macOS apps with native Apple aesthetics following
  the Human Interface Guidelines (HIG). Use when building, reviewing, or improving macOS UI
  across SwiftUI, AppKit, or Electron/web apps. Covers window chrome, title bars, toolbars,
  sidebars, split views, status bar and menu bar apps, controls (buttons, text fields, pickers,
  tables), system colors, SF fonts, vibrancy/materials, SF Symbols, spacing, layout, animations,
  dark mode, and accessibility. Trigger on requests like "make this look native on Mac",
  "build a macOS menu bar app", "style this like a native macOS app", "implement a sidebar
  like Finder", "create a status bar item", or any macOS UI design/implementation task.
---

# macOS Native UI

This skill provides Apple Human Interface Guidelines (HIG) and implementation patterns to build macOS apps that look and feel native — covering SwiftUI, AppKit, and Electron/web.

## Framework Selection

Determine the target framework first:

| Scenario                           | Framework              | Reference                                      |
|------------------------------------|------------------------|------------------------------------------------|
| New macOS app, modern Swift        | **SwiftUI**            | `references/swiftui-patterns.md`               |
| Existing AppKit app, full control  | **AppKit**             | `references/appkit-patterns.md`                |
| Cross-platform / Electron app      | **Electron/Web CSS**   | `references/electron-web-patterns.md`          |
| Multi-framework or unsure          | Read all three         | All framework reference files                  |

## Core Design References

Load these references based on the task:

| Task                                        | Reference File                          |
|---------------------------------------------|-----------------------------------------|
| Colors, dark mode, system colors, materials | `references/colors-typography.md`       |
| Typography, SF fonts, text sizes            | `references/colors-typography.md`       |
| Spacing, padding, corner radii, dimensions  | `references/layout-spacing.md`          |
| Buttons, text fields, pickers, lists        | `references/controls.md`               |
| Windows, title bars, toolbars, sidebars     | `references/windows-chrome.md`          |
| Menu bar apps, status items, context menus  | `references/menu-statusbar.md`          |

## Key Principles

Always apply these rules without needing to read reference files:

1. **Never hardcode colors** — use semantic/system colors that adapt to light/dark mode
2. **System font stack** — use `-apple-system` / `NSFont.systemFont` / SwiftUI `.body`; never load SF Pro as a custom web font
3. **8pt grid** — all spacing should be multiples of 4 or 8
4. **Continuous corner radius** — use `.continuous` style for Apple's squircle curve (SwiftUI); `border-radius` values from 5–10px by context
5. **Vibrancy for panels/sidebars** — use materials (`.regularMaterial`, `NSVisualEffectView`, `backdrop-filter`) rather than solid backgrounds
6. **SF Symbols for all icons** — never use emoji or third-party icon libraries for UI chrome
7. **`cursor: default` not `pointer`** — on macOS, interactive controls use the arrow cursor (web default `pointer` looks out of place)
8. **13pt body text on macOS** — desktop default is 13pt, not 16pt (browser default) or 17pt (iOS)
9. **Traffic lights stay top-left** — never move window controls to the right side
10. **Spring animations** — use `.spring()` / `.snappy` / `.smooth` for interactions; avoid linear easing

## Workflow

When given a UI task:

1. **Identify framework** — SwiftUI, AppKit, or Electron/web
2. **Load relevant reference(s)** — use the table above to pick which files to read
3. **Apply HIG patterns** — implement using the code samples and specs from reference files
4. **Verify dark mode** — ensure all colors adapt; test both appearances
5. **Check accessibility** — add `accessibilityLabel`, support keyboard navigation, verify Dynamic Type (SwiftUI)

## Common Tasks Quick Reference

**Status bar / menu bar app** → Read `references/menu-statusbar.md`

**Sidebar + split view layout** → Read `references/windows-chrome.md` (Split Views section)

**Custom window chrome** → Read `references/windows-chrome.md` (Title Bar + Toolbar sections) + `references/electron-web-patterns.md` (if web)

**Button/control styling** → Read `references/controls.md`

**Dark mode color system** → Read `references/colors-typography.md`

**Electron CSS design tokens** → Read `references/electron-web-patterns.md` (has complete CSS variable system)
