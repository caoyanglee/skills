# Menu Bar & Status Bar

## Table of Contents
1. [Status Bar Items](#status-bar-items)
2. [Status Bar Menus](#status-bar-menus)
3. [Popover from Status Item](#popover-from-status-item)
4. [Menu Bar App Architecture](#menu-bar-app-architecture)
5. [Menu Design Rules](#menu-design-rules)
6. [Context Menus](#context-menus)
7. [App Menu Bar Menus](#app-menu-bar-menus)

---

## Status Bar Items

### SwiftUI MenuBarExtra (macOS 13+)
```swift
@main struct MyApp: App {
  var body: some Scene {
    // Main window (optional — omit for menu-bar-only apps)
    // WindowGroup { ContentView() }

    MenuBarExtra("My App", systemImage: "star.fill") {
      // Menu items
      Button("Open Window") { openWindow(id: "main") }
      Divider()
      Button("Quit") { NSApp.terminate(nil) }
    }
    .menuBarExtraStyle(.menu)     // Dropdown menu style
    // or
    .menuBarExtraStyle(.window)   // Popover window style
  }
}
```

### AppKit NSStatusItem
```swift
let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)

// Set icon
statusItem.button?.image = NSImage(systemSymbolName: "star.fill",
                                   accessibilityDescription: "My App")
statusItem.button?.image?.isTemplate = true  // IMPORTANT: allows tinting

// Attach menu
statusItem.menu = buildMenu()

// Or handle click manually
statusItem.button?.target = self
statusItem.button?.action = #selector(statusItemClicked)
```

### Icon Design Rules
- Always use `isTemplate = true` for automatic light/dark adaptation
- Icon size: **18×18pt** (appears at 16pt in the status bar)
- Use **SF Symbols** when possible; they're auto-templated
- Keep icons simple and monochromatic — avoid color in status bar icons
- Support multiple sizes: @1x (18px) and @2x (36px)

### Variable Status Bar Width
```swift
// Fixed square (icon only)
NSStatusItem.squareLength  // 22pt

// Variable (icon + text)
NSStatusItem.variableLength
statusItem.button?.title = "42°"
```

---

## Status Bar Menus

### NSMenu Structure
```swift
func buildMenu() -> NSMenu {
  let menu = NSMenu()
  
  // Section 1: App actions
  menu.addItem(NSMenuItem(title: "Open Dashboard", action: #selector(openDash), keyEquivalent: ""))
  menu.addItem(NSMenuItem(title: "Refresh", action: #selector(refresh), keyEquivalent: "r"))
  
  // Divider
  menu.addItem(NSMenuItem.separator())
  
  // Section 2: Settings
  let prefItem = NSMenuItem(title: "Preferences…", action: #selector(openPrefs), keyEquivalent: ",")
  prefItem.keyEquivalentModifierMask = [.command]
  menu.addItem(prefItem)
  
  // Section 3: Quit
  menu.addItem(NSMenuItem.separator())
  menu.addItem(NSMenuItem(title: "Quit", action: #selector(quit), keyEquivalent: "q"))
  
  return menu
}
```

### Menu Items with Icons
```swift
let item = NSMenuItem(title: "Settings", action: #selector(openSettings), keyEquivalent: "")
item.image = NSImage(systemSymbolName: "gear", accessibilityDescription: nil)
// System symbol images are auto-sized (~16pt) in menus
```

### Submenu
```swift
let parentItem = NSMenuItem(title: "Export As", action: nil, keyEquivalent: "")
let submenu = NSMenu()
submenu.addItem(NSMenuItem(title: "PDF", action: #selector(exportPDF), keyEquivalent: ""))
submenu.addItem(NSMenuItem(title: "PNG", action: #selector(exportPNG), keyEquivalent: ""))
parentItem.submenu = submenu
menu.addItem(parentItem)
```

### Dynamic Menu Content
```swift
// Update menu before display
func menuWillOpen(_ menu: NSMenu) {
  // Refresh dynamic items
  updateSyncStatusItem()
}
```

---

## Popover from Status Item

For richer UIs, show an NSPopover instead of a menu.

### AppKit
```swift
func showPopover() {
  let popover = NSPopover()
  popover.contentSize = NSSize(width: 320, height: 400)
  popover.behavior = .transient  // Close when clicking outside
  popover.contentViewController = NSHostingController(rootView: PopoverView())
  
  if let button = statusItem.button {
    popover.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
  }
}
```

### SwiftUI (MenuBarExtra window style)
```swift
MenuBarExtra("App", systemImage: "app") {
  PopoverContentView()
    .frame(width: 320, height: 400)
}
.menuBarExtraStyle(.window)
```

### Popover Design Guidelines
- Width: 280–360pt for standard apps
- Background: Use `NSVisualEffectView` (`.menu` or `.popover` material)
- Arrow direction: Pointing up (`.minY` preferred edge)
- Include close button or clear dismiss behavior

---

## Menu Bar App Architecture

### Menu-Bar-Only App (no Dock icon)
```swift
// Info.plist
// LSUIElement = true  (Application is agent — no Dock icon)

// Alternatively in SwiftUI App:
@NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

class AppDelegate: NSObject, NSApplicationDelegate {
  func applicationDidFinishLaunching(_ notification: Notification) {
    NSApp.setActivationPolicy(.accessory)  // Hide from Dock
  }
}
```

### Lifecycle
1. App launches → `applicationDidFinishLaunching`
2. Create `NSStatusItem` and configure icon
3. Attach `NSMenu` or set up popover handler
4. Optional: Open `NSWindow` or `NSPanel` for expanded views

### Login Item (auto-launch at login)
```swift
// macOS 13+
import ServiceManagement
SMAppService.mainApp.register()   // Enable launch at login
SMAppService.mainApp.unregister() // Disable
```

---

## Menu Design Rules

| Rule                          | Detail                                              |
|-------------------------------|-----------------------------------------------------|
| Section grouping              | Group related items; separate sections with dividers|
| Keyboard shortcuts            | Only assign if universally useful; don't overload   |
| Ellipsis (…)                  | Add after items that open a window/dialog           |
| Destructive items             | Place last; no confirmation in menus                |
| Disable unavailable items     | `item.isEnabled = false` — never hide them          |
| Check marks                   | Use `item.state = .on/.off` for toggle states       |
| Accessibility descriptions    | Set `accessibilityLabel` for all icon-only items    |

### Menu Item States
```swift
item.state = .on      // Checkmark
item.state = .off     // No checkmark
item.state = .mixed   // Dash (partial selection)
```

---

## Context Menus

Right-click / Control-click menus for contextual actions.

### SwiftUI
```swift
Text("Right-click me")
  .contextMenu {
    Button("Copy") { copy() }
    Button("Open") { open() }
    Divider()
    Button("Delete", role: .destructive) { delete() }
  }
```

### AppKit
```swift
override func rightMouseDown(with event: NSEvent) {
  let menu = NSMenu()
  menu.addItem(NSMenuItem(title: "Copy", action: #selector(copy), keyEquivalent: ""))
  NSMenu.popUpContextMenu(menu, with: event, for: self)
}
```

---

## App Menu Bar Menus

Standard macOS menu bar structure for regular apps (not menu-bar apps):

```
AppName  File  Edit  View  Window  Help
```

### Required Menus
- **App menu** (leftmost, named after app): About, Preferences (⌘,), Services, Hide/Show, Quit (⌘Q)
- **File**: New (⌘N), Open (⌘O), Save (⌘S), Print (⌘P)…
- **Edit**: Undo (⌘Z), Redo (⇧⌘Z), Cut/Copy/Paste/Select All
- **Window**: Minimize (⌘M), Zoom, Bring All to Front

### SwiftUI Menu Commands
```swift
@main struct MyApp: App {
  var body: some Scene {
    WindowGroup { ContentView() }
      .commands {
        CommandGroup(replacing: .appInfo) {
          Button("About My App") { showAbout() }
        }
        CommandMenu("Custom Menu") {
          Button("My Action") { }
            .keyboardShortcut("k", modifiers: [.command])
        }
      }
  }
}
```
