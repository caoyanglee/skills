# Electron & Web Native macOS Patterns

## Table of Contents
1. [Core Principles](#core-principles)
2. [Window Chrome](#window-chrome)
3. [Typography & Colors](#typography--colors)
4. [Native-Style Components](#native-style-components)
5. [CSS Design Tokens](#css-design-tokens)
6. [Electron-Specific APIs](#electron-specific-apis)
7. [Common Pitfalls](#common-pitfalls)

---

## Core Principles

When building Electron or web apps targeting macOS:

1. **Use system fonts** (`-apple-system`, `BlinkMacSystemFont`) — never load custom fonts that duplicate SF Pro
2. **Respect dark mode** — always use `@media (prefers-color-scheme: dark)`
3. **Default cursor for UI** — use `cursor: default` on buttons/controls (not `pointer`, which feels webby)
4. **No focus outlines by default** — use macOS-style focus rings (`box-shadow: 0 0 0 3px rgba(0,122,255,0.35)`)
5. **Native vibrancy** — use Electron's `vibrancy` option or CSS `backdrop-filter` for translucency
6. **13pt body text** — macOS default is 13pt, not 16pt (browser default)
7. **Disable text selection on UI chrome** — use `user-select: none` on buttons, labels, toolbars

---

## Window Chrome

### Electron BrowserWindow Configuration
```javascript
const win = new BrowserWindow({
  width: 900,
  height: 600,
  minWidth: 480,
  minHeight: 300,
  
  // macOS native title bar with traffic lights
  titleBarStyle: 'hiddenInset',     // Content under title bar, traffic lights visible
  // or 'hidden'                     // No title bar at all
  // or 'default'                    // Standard macOS title bar
  
  // Translucency
  vibrancy: 'sidebar',              // 'menu', 'popover', 'sidebar', 'under-window'
  visualEffectState: 'active',
  
  // Traffic lights position (with hiddenInset)
  trafficLightPosition: { x: 12, y: 16 },
  
  backgroundColor: '#00000000',     // Transparent for vibrancy
  
  // Modern rounded corners (macOS default)
  roundedCorners: true,
  
  webPreferences: {
    nodeIntegration: false,
    contextIsolation: true,
    preload: path.join(__dirname, 'preload.js'),
  }
})
```

### CSS Window Drag Region
```css
/* Make title bar area draggable */
.titlebar {
  -webkit-app-region: drag;
  height: 52px;  /* Enough for traffic lights */
}

/* Interactive elements inside drag region must opt out */
.titlebar button,
.titlebar input,
.titlebar a {
  -webkit-app-region: no-drag;
}
```

### Traffic Light Safe Area
```css
/* Account for traffic light buttons (12px from left, ~28px width each + 8px gaps) */
.titlebar {
  padding-left: 76px;  /* Space for 3 traffic lights */
  padding-right: 16px;
  display: flex;
  align-items: center;
  height: 52px;
}
```

---

## Typography & Colors

### Complete Design Token System
```css
/* === TYPOGRAPHY === */
:root {
  --font-system: -apple-system, BlinkMacSystemFont, "SF Pro Text",
                 "Helvetica Neue", Arial, sans-serif;
  --font-mono:   "SF Mono", ui-monospace, Menlo, Monaco, 
                 "Cascadia Code", monospace;
  
  --text-xs:   11px;   /* Caption 2 */
  --text-sm:   12px;   /* Caption 1 */
  --text-base: 13px;   /* Body (macOS default) */
  --text-md:   15px;   /* Subheadline */
  --text-lg:   17px;   /* Headline/Body (iOS) */
  --text-xl:   20px;   /* Title 3 */
  --text-2xl:  22px;   /* Title 2 */
  --text-3xl:  28px;   /* Title 1 */
  
  --weight-regular:  400;
  --weight-medium:   500;
  --weight-semibold: 600;
  --weight-bold:     700;
}

/* === LIGHT MODE COLORS === */
:root {
  --color-accent:          #007AFF;
  --color-accent-hover:    #0070E0;
  --color-accent-active:   #0062C0;
  
  --color-label:           rgba(0, 0, 0, 0.85);
  --color-label-2:         rgba(0, 0, 0, 0.5);
  --color-label-3:         rgba(0, 0, 0, 0.25);
  --color-label-4:         rgba(0, 0, 0, 0.1);
  
  --color-bg:              #FFFFFF;
  --color-bg-secondary:    #F5F5F7;
  --color-bg-tertiary:     #EBEBEB;
  --color-bg-grouped:      #F2F2F7;
  
  --color-fill:            rgba(120, 120, 128, 0.2);
  --color-fill-2:          rgba(120, 120, 128, 0.16);
  --color-fill-3:          rgba(118, 118, 128, 0.12);
  
  --color-separator:       rgba(60, 60, 67, 0.29);
  --color-separator-opaque:#C6C6C8;
  
  --color-control-bg:      rgba(255, 255, 255, 0.95);
  --color-sidebar-bg:      rgba(246, 246, 246, 0.85);
  
  --shadow-sm:  0 1px 2px rgba(0,0,0,0.12);
  --shadow-md:  0 2px 8px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08);
  --shadow-lg:  0 8px 32px rgba(0,0,0,0.16), 0 2px 8px rgba(0,0,0,0.08);
  --shadow-window: 0 20px 60px rgba(0,0,0,0.3), 0 2px 4px rgba(0,0,0,0.1);
}

/* === DARK MODE COLORS === */
@media (prefers-color-scheme: dark) {
  :root {
    --color-accent:          #0A84FF;
    --color-accent-hover:    #1A94FF;
    --color-accent-active:   #0070E0;
    
    --color-label:           rgba(255, 255, 255, 0.85);
    --color-label-2:         rgba(255, 255, 255, 0.55);
    --color-label-3:         rgba(255, 255, 255, 0.25);
    --color-label-4:         rgba(255, 255, 255, 0.1);
    
    --color-bg:              #1C1C1E;
    --color-bg-secondary:    #2C2C2E;
    --color-bg-tertiary:     #3A3A3C;
    --color-bg-grouped:      #1C1C1E;
    
    --color-fill:            rgba(120, 120, 128, 0.36);
    --color-fill-2:          rgba(120, 120, 128, 0.32);
    --color-fill-3:          rgba(118, 118, 128, 0.24);
    
    --color-separator:       rgba(84, 84, 88, 0.65);
    --color-separator-opaque:#38383A;
    
    --color-control-bg:      rgba(255, 255, 255, 0.05);
    --color-sidebar-bg:      rgba(30, 30, 30, 0.85);
    
    --shadow-sm:  0 1px 2px rgba(0,0,0,0.4);
    --shadow-md:  0 2px 8px rgba(0,0,0,0.4), 0 1px 2px rgba(0,0,0,0.3);
    --shadow-lg:  0 8px 32px rgba(0,0,0,0.5), 0 2px 8px rgba(0,0,0,0.3);
    --shadow-window: 0 20px 60px rgba(0,0,0,0.7), 0 2px 4px rgba(0,0,0,0.3);
  }
}
```

---

## Native-Style Components

### Sidebar
```css
.sidebar {
  width: 240px;
  min-width: 180px;
  background: var(--color-sidebar-bg);
  -webkit-backdrop-filter: blur(20px) saturate(1.8);
  backdrop-filter: blur(20px) saturate(1.8);
  border-right: 1px solid var(--color-separator);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  user-select: none;
}

.sidebar-section-header {
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--color-label-2);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 12px 10px 4px;
}

.sidebar-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 10px;
  border-radius: 6px;
  margin: 1px 6px;
  font-size: var(--text-base);
  color: var(--color-label);
  cursor: default;
}

.sidebar-row:hover { background: var(--color-fill-3); }
.sidebar-row.active {
  background: var(--color-accent);
  color: white;
}
.sidebar-row.active .sidebar-icon { color: white; }
```

### Toolbar
```css
.toolbar {
  height: 52px;
  display: flex;
  align-items: center;
  padding: 0 12px;
  gap: 4px;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-separator);
  user-select: none;
  -webkit-app-region: drag;
}
.toolbar > * { -webkit-app-region: no-drag; }

.toolbar-button {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: var(--color-label);
  cursor: default;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}
.toolbar-button:hover { background: var(--color-fill-3); }
.toolbar-button:active { background: var(--color-fill-2); }
.toolbar-button.active {
  background: var(--color-accent);
  color: white;
}
```

### List / Table Rows
```css
.list-item {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  font-size: var(--text-base);
  color: var(--color-label);
  cursor: default;
  border-radius: 6px;
  user-select: none;
}
.list-item:hover { background: var(--color-fill-3); }
.list-item.selected { background: var(--color-accent); color: white; }
.list-item.selected .secondary { color: rgba(255,255,255,0.7); }
/* When container not focused: */
.list-item.selected.inactive { background: var(--color-fill); color: var(--color-label); }
```

---

## Electron-Specific APIs

### System Theme Detection
```javascript
const { nativeTheme } = require('electron')

// Get current theme
console.log(nativeTheme.shouldUseDarkColors)  // true in dark mode

// Listen for changes
nativeTheme.on('updated', () => {
  mainWindow.webContents.send('theme-changed', nativeTheme.shouldUseDarkColors)
})
```

### System Colors via Electron
```javascript
const { systemPreferences } = require('electron')
// macOS system accent color
const accent = systemPreferences.getAccentColor()  // hex string like '007AFF'
```

### Context Menu (native)
```javascript
const { Menu, MenuItem } = require('electron')

const menu = new Menu()
menu.append(new MenuItem({ label: 'Copy', role: 'copy' }))
menu.append(new MenuItem({ type: 'separator' }))
menu.append(new MenuItem({ label: 'Delete', click: () => deleteItem() }))

// Show on right-click
window.addEventListener('contextmenu', (e) => {
  e.preventDefault()
  menu.popup({ window: remote.getCurrentWindow() })
})
```

---

## Common Pitfalls

| ❌ Avoid                              | ✅ Do Instead                                    |
|---------------------------------------|--------------------------------------------------|
| `cursor: pointer` on buttons          | `cursor: default`                                |
| `font-size: 16px` body               | `font-size: 13px` for macOS body                 |
| `border-radius: 4px` everywhere       | Use HIG radius values (5–10px by context)        |
| `box-shadow` for windows without blur | Add `backdrop-filter` for authentic depth        |
| Hardcoded `#000` / `#fff` colors     | Use CSS variables with dark mode variants        |
| `outline: none` globally             | Only remove outline; add focus ring instead      |
| Custom fonts loading SF Pro           | Use `-apple-system` system font stack            |
| Fixed pixel widths for sidebars      | Use `min-width` / `max-width` + drag to resize   |
| WebKit scrollbars default            | Style with `::-webkit-scrollbar` for native look |

### Native Scrollbar Style
```css
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.25);
  border-radius: 4px;
  border: 2px solid transparent;
  background-clip: content-box;
}
::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.4); }
@media (prefers-color-scheme: dark) {
  ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.25); }
  ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.4); }
}
```
