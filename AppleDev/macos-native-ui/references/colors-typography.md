# Colors & Typography

## Table of Contents
1. [System Colors](#system-colors)
2. [Semantic Colors](#semantic-colors)
3. [Vibrancy & Materials](#vibrancy--materials)
4. [Typography — SF Fonts](#typography--sf-fonts)
5. [Text Styles](#text-styles)

---

## System Colors

Apple-defined system colors automatically adapt to light/dark mode and high-contrast settings.

### Base Palette

| Color Name        | Light Mode (approx) | Dark Mode (approx) | Usage                      |
|-------------------|---------------------|--------------------|----------------------------|
| systemBlue        | #007AFF             | #0A84FF            | Links, actions, selection  |
| systemGreen       | #34C759             | #30D158            | Success, positive           |
| systemRed         | #FF3B30             | #FF453A            | Errors, destructive actions |
| systemOrange      | #FF9500             | #FF9F0A            | Warnings                    |
| systemYellow      | #FFCC00             | #FFD60A            | Cautions                    |
| systemPurple      | #AF52DE             | #BF5AF2            | Accents                     |
| systemPink        | #FF2D55             | #FF375F            | Special accents             |
| systemTeal        | #5AC8FA             | #64D2FF            | Informational               |
| systemIndigo      | #5856D6             | #5E5CE6            | Accents                     |
| systemGray        | #8E8E93             | #8E8E93            | Neutral content             |
| systemGray2       | #AEAEB2             | #636366            | Secondary neutral           |
| systemGray3       | #C7C7CC             | #48484A            | Tertiary neutral            |
| systemGray4       | #D1D1D6             | #3A3A3C            | Quaternary neutral          |
| systemGray5       | #E5E5EA             | #2C2C2E            | Background fills            |
| systemGray6       | #F2F2F7             | #1C1C1E            | Grouped background          |

### SwiftUI Usage
```swift
Color(.systemBlue)
Color(.systemBackground)    // Adaptive white/black
Color(.secondarySystemBackground)
Color(.tertiarySystemBackground)
```

### AppKit Usage
```swift
NSColor.systemBlue
NSColor.labelColor
NSColor.secondaryLabelColor
NSColor.controlAccentColor  // User's accent color preference
```

### CSS/Electron Usage
```css
/* Use macOS system color keywords where supported */
color: -apple-system-blue;
background: -apple-system-background;

/* Fallback with CSS variables */
:root {
  --system-blue: #007AFF;
  --label: rgba(0,0,0,0.85);
  --secondary-label: rgba(0,0,0,0.5);
  --separator: rgba(60,60,67,0.29);
  --background: #FFFFFF;
  --secondary-background: #F2F2F7;
  --grouped-background: #F2F2F7;
}
@media (prefers-color-scheme: dark) {
  :root {
    --system-blue: #0A84FF;
    --label: rgba(255,255,255,0.85);
    --secondary-label: rgba(255,255,255,0.55);
    --separator: rgba(84,84,88,0.65);
    --background: #1C1C1E;
    --secondary-background: #2C2C2E;
    --grouped-background: #1C1C1E;
  }
}
```

---

## Semantic Colors

Use semantic colors rather than literal color values to ensure proper dark mode adaptation.

| Semantic Name          | Role                                           |
|------------------------|------------------------------------------------|
| label                  | Primary text                                   |
| secondaryLabel         | Secondary/supplementary text                   |
| tertiaryLabel          | Tertiary text (placeholders, disabled)         |
| quaternaryLabel        | Barely visible text                            |
| systemFill             | Thin overlay fills (e.g., slider tracks)       |
| secondarySystemFill    | Medium-weight overlay fills                    |
| tertiarySystemFill     | Thicker overlay fills                          |
| quaternarySystemFill   | Opaque fills                                   |
| placeholderText        | Placeholder text in text fields               |
| separator              | Thin lines, dividers                           |
| opaqueSeparator        | Separators without transparency                |
| link                   | Tappable/clickable content                     |
| controlAccentColor     | Respects user's System Preferences accent      |

---

## Vibrancy & Materials

macOS materials use blur + translucency for depth. Always prefer system materials over custom backgrounds.

### SwiftUI
```swift
.background(.regularMaterial)
.background(.thickMaterial)
.background(.thinMaterial)
.background(.ultraThinMaterial)
.background(.ultraThickMaterial)
// In a vibrancy context:
.background(.windowBackground)
.background(.sidebar)
```

### AppKit
```swift
NSVisualEffectView()  // material: .sidebar, .menu, .popover, .hudWindow, etc.
```

### CSS/Electron
```css
/* Native-like blur effect */
background: rgba(255,255,255,0.72);
-webkit-backdrop-filter: blur(20px) saturate(1.8);
backdrop-filter: blur(20px) saturate(1.8);

@media (prefers-color-scheme: dark) {
  background: rgba(30,30,30,0.72);
}
```

---

## Typography — SF Fonts

macOS uses the **San Francisco (SF)** typeface family:
- **SF Pro** — Main text font for UI
- **SF Pro Rounded** — Softer feel, used in friendly contexts
- **SF Mono** — Monospaced, for code
- **New York** — Serif, for long-form reading

### CSS/Electron Font Stack
```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
               "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
}
code, pre {
  font-family: "SF Mono", ui-monospace, Menlo, Monaco, monospace;
}
```

### Font Weight Mapping
| CSS weight | Name       | Usage                         |
|-----------|------------|-------------------------------|
| 100       | Ultralight | Large display titles only     |
| 200       | Thin       | Display use                   |
| 300       | Light      | Large text                    |
| 400       | Regular    | Body text                     |
| 500       | Medium     | Emphasized body               |
| 600       | Semibold   | Buttons, labels               |
| 700       | Bold       | Headlines                     |
| 800       | Heavy      | Large display                 |
| 900       | Black      | Display only                  |

---

## Text Styles

### macOS HIG Text Style Scale

| Style           | Size (pt) | Weight    | Usage                              |
|-----------------|-----------|-----------|------------------------------------|
| Large Title     | 34        | Regular   | Page/view title (rare in macOS)    |
| Title 1         | 28        | Regular   | Primary view titles                |
| Title 2         | 22        | Regular   | Section titles                     |
| Title 3         | 20        | Regular   | Tertiary titles                    |
| Headline        | 17        | Semibold  | Emphasized body                    |
| Body            | 17        | Regular   | Standard body text                 |
| Callout         | 16        | Regular   | Secondary body                     |
| Subheadline     | 15        | Regular   | Below headlines                    |
| Footnote        | 13        | Regular   | Supplementary text                 |
| Caption 1       | 12        | Regular   | Captions                           |
| Caption 2       | 11        | Regular   | Smallest text, use sparingly       |

### SwiftUI
```swift
Text("Title").font(.title)
Text("Body").font(.body)
Text("Caption").font(.caption)
```

### AppKit
```swift
NSFont.systemFont(ofSize: NSFont.systemFontSize)    // 13pt default
NSFont.boldSystemFont(ofSize: NSFont.systemFontSize)
NSFont.systemFont(ofSize: 17, weight: .semibold)
```

### CSS
```css
.title    { font-size: 28px; font-weight: 400; letter-spacing: 0.36px; }
.headline { font-size: 17px; font-weight: 600; }
.body     { font-size: 13px; font-weight: 400; }  /* macOS default is 13pt */
.caption  { font-size: 11px; font-weight: 400; }
```

> **Note:** macOS default body text is **13pt**, not 17pt (which is iOS body size). Use 13pt as the base for desktop apps.

### Line Height & Tracking
- Body text: line-height ~1.4–1.5
- Headlines: line-height ~1.1–1.2
- Tracking: slightly negative for large sizes (`letter-spacing: -0.02em` for titles)
