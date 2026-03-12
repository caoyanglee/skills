# Layout & Spacing

## Table of Contents
1. [Base Unit & Grid](#base-unit--grid)
2. [Standard Spacing Values](#standard-spacing-values)
3. [Window Dimensions](#window-dimensions)
4. [Content Margins](#content-margins)
5. [Safe Areas & Insets](#safe-areas--insets)
6. [Corner Radii](#corner-radii)

---

## Base Unit & Grid

macOS uses an **8pt base grid** (points, not pixels). All dimensions should be multiples of 4 or 8.

- **1x screens:** 1pt = 1px
- **2x Retina:** 1pt = 2px
- **Base unit:** 8pt
- **Half unit:** 4pt (for tight spacing)
- **Quarter unit:** 2pt (for micro-adjustments, borders)

---

## Standard Spacing Values

| Token   | Value  | Usage                                      |
|---------|--------|--------------------------------------------|
| xxxs    | 2pt    | Micro gaps (icon + label, badge borders)   |
| xxs     | 4pt    | Tight spacing within components            |
| xs      | 8pt    | Between related elements                   |
| sm      | 12pt   | Within groups                              |
| md      | 16pt   | Standard padding inside containers         |
| lg      | 20pt   | Section spacing                            |
| xl      | 24pt   | Between sections                           |
| xxl     | 32pt   | Major section gaps                         |
| xxxl    | 48pt   | Page-level spacing                         |

### CSS Variables
```css
:root {
  --space-2:  2px;
  --space-4:  4px;
  --space-8:  8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-20: 20px;
  --space-24: 24px;
  --space-32: 32px;
  --space-48: 48px;
}
```

---

## Window Dimensions

### Minimum Window Sizes
| Window Type             | Min Width | Min Height |
|-------------------------|-----------|------------|
| Document window         | 400pt     | 300pt      |
| Utility / Inspector     | 200pt     | 100pt      |
| Alert / Dialog          | 260pt     | auto       |
| Preferences window      | 440pt     | auto       |
| Full-size panel         | 480pt     | 320pt      |

### Typical Default Window Sizes
| App Type                | Width     | Height    |
|-------------------------|-----------|-----------|
| Simple utility          | 480–600   | 320–400   |
| Document editor         | 800–1200  | 600–900   |
| Settings/Prefs          | 560–740   | 400–600   |
| Browser/file viewer     | 900–1200  | 600–800   |

### NSWindow Default Style
```swift
// Titled + resizable + closable + miniaturizable
NSWindow(contentRect: NSRect(x: 0, y: 0, width: 800, height: 600),
         styleMask: [.titled, .closable, .miniaturizable, .resizable],
         backing: .buffered, defer: false)
```

---

## Content Margins

### Main Content Area
| Context             | Horizontal Margin | Vertical Margin |
|---------------------|------------------|----------------|
| Regular content     | 20pt             | 20pt           |
| Sidebar content     | 10pt             | 8pt            |
| Inspector/panel     | 16pt             | 16pt           |
| Alert body          | 20pt             | 16pt           |
| Toolbar             | 10pt             | —              |
| Status bar menu     | 16pt             | 8pt            |

### SwiftUI Padding
```swift
.padding()           // 16pt all sides
.padding(.horizontal, 20)
.padding(.vertical, 12)
.padding([.horizontal, .bottom])
```

### AppKit Constraints
```swift
// Use layout anchors — avoid hardcoded frames
view.topAnchor.constraint(equalTo: container.topAnchor, constant: 20).isActive = true
view.leadingAnchor.constraint(equalTo: container.leadingAnchor, constant: 20).isActive = true
```

---

## Safe Areas & Insets

- **Title bar height:** 28pt (regular), 22pt (with full-size content view)
- **Tab bar height:** 28pt
- **Toolbar height:** 38pt (default), 52pt (large)
- **Status bar menu popover arrow:** 16pt
- **Bottom bar / Touch Bar area:** 30pt (if present)

### Full-Size Content View (window extends under title bar)
```swift
// SwiftUI
.ignoresSafeArea()

// AppKit
window.titlebarAppearsTransparent = true
window.styleMask.insert(.fullSizeContentView)
```

---

## Corner Radii

macOS uses consistent corner radii across the system. Match these values for native feel.

| Element                       | Corner Radius |
|-------------------------------|---------------|
| App window                    | 10pt          |
| Panel / HUD window            | 8pt           |
| Menu                          | 6pt           |
| Popover                       | 8pt           |
| Button (regular)              | 5pt           |
| Button (large)                | 6pt           |
| Text field                    | 5pt           |
| Rounded rect button           | 6pt           |
| Tag / Badge                   | 4pt           |
| Tooltip                       | 4pt           |
| Notification banner           | 12pt          |
| Card / container              | 8–12pt        |
| Sidebar row selection         | 6pt           |
| Thumbnail / image preview     | 8pt           |

### CSS
```css
.button    { border-radius: 5px; }
.window    { border-radius: 10px; }
.popover   { border-radius: 8px; }
.card      { border-radius: 8px; }
.input     { border-radius: 5px; }
```

### SwiftUI
```swift
.clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
// Use .continuous for smoother Apple-style curves (squircle-like)
```
