# Windows & Chrome

## Table of Contents
1. [Window Types](#window-types)
2. [Title Bar](#title-bar)
3. [Toolbar](#toolbar)
4. [Sidebar](#sidebar)
5. [Split Views](#split-views)
6. [Panels & Inspectors](#panels--inspectors)
7. [Sheets & Dialogs](#sheets--dialogs)
8. [Popovers](#popovers)
9. [HUD & Overlays](#hud--overlays)

---

## Window Types

| Type               | Usage                                        | Notes                              |
|--------------------|----------------------------------------------|------------------------------------|
| Document window    | Main app windows                             | Resizable, titled                  |
| Utility window     | Floats above other windows (Inspector)       | Smaller title bar, always on top   |
| Panel              | Non-document helper windows                  | Similar to utility                 |
| Borderless         | Custom chrome (media players, etc.)          | No title bar — provide controls    |
| Sheet              | Modal dialog attached to parent window       | Slides down from title bar         |
| Alert              | System alert/error messages                  | Center-aligned, modal              |
| Popover            | Contextual UI attached to a control          | Has an arrow pointer               |

### SwiftUI Window Declaration
```swift
@main struct MyApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
    .defaultSize(width: 900, height: 600)
    .windowResizability(.contentMinSize)

    Settings {
      SettingsView()
    }
  }
}
```

---

## Title Bar

### Title Bar Modes

**Standard title bar:**
- Window controls (traffic lights): red (close), yellow (minimize), green (fullscreen)
- Title text centered or leading
- Optional document icon

**Transparent / full-size content view:**
- Content extends under title bar
- Use blur/vibrancy for visual separation
- Good for media apps, galleries, dashboards

**Hidden title bar with toolbar only:**
- Clean, toolbar-centered design
- Modern macOS app style (Finder, Xcode)

### SwiftUI
```swift
// Full-size content view
WindowGroup {
  ContentView()
}
.windowStyle(.hiddenTitleBar)

// In the view:
.ignoresSafeArea()

// Custom toolbar-integrated title
.toolbar {
  ToolbarItem(placement: .principal) {
    Text("My App").fontWeight(.semibold)
  }
}
```

### AppKit
```swift
window.titlebarAppearsTransparent = true
window.styleMask.insert(.fullSizeContentView)
window.titleVisibility = .hidden

// Move traffic lights position
window.standardWindowButton(.closeButton)?.frame.origin = CGPoint(x: 12, y: ...)
```

### Window Controls (Traffic Lights)
- Always keep in **top-left** corner (macOS convention — never move to right)
- Spacing: 8pt between buttons
- Size: 12pt diameter
- Positions: Close at x=12, Minimize at x=32, Zoom at x=52 from left edge

---

## Toolbar

macOS toolbars sit below the title bar. Items should be icons or icon+label.

### SwiftUI Toolbar
```swift
.toolbar {
  // Leading items
  ToolbarItemGroup(placement: .navigation) {
    Button(action: goBack) {
      Image(systemName: "chevron.left")
    }
  }

  // Center / principal
  ToolbarItem(placement: .principal) {
    Picker("View", selection: $mode) { ... }
      .pickerStyle(.segmented)
  }

  // Trailing items
  ToolbarItemGroup(placement: .primaryAction) {
    Button("New", systemImage: "plus") { }
    Button("Share", systemImage: "square.and.arrow.up") { }
  }
}
.toolbarStyle(.unified)         // Merged title bar + toolbar
.toolbarStyle(.unifiedCompact)  // Shorter combined bar
.toolbarStyle(.expanded)        // Separate title bar + toolbar
```

### AppKit NSToolbar
```swift
let toolbar = NSToolbar(identifier: "main")
toolbar.delegate = self
toolbar.displayMode = .iconOnly   // .iconOnly, .iconAndLabel, .labelOnly
window.toolbar = toolbar
```

### Toolbar Icon Guidelines
- Use SF Symbols for all toolbar icons
- Prefer 16–18pt symbol size in toolbar
- Use `.toolbar` rendering mode for proper system tinting
- Group related actions; separate groups with `NSToolbarFlexibleSpaceItem`

---

## Sidebar

The sidebar shows navigation and filtering. Follow the standard sidebar pattern:

### Width Guidelines
| Role              | Width   |
|-------------------|---------|
| Compact sidebar   | 180pt   |
| Standard sidebar  | 220–260pt|
| Wide sidebar      | 280–320pt|

### SwiftUI NavigationSplitView
```swift
NavigationSplitView(columnVisibility: $visibility) {
  // Sidebar
  List(selection: $selectedItem) {
    Section("Favorites") {
      Label("Home", systemImage: "house").tag(Item.home)
      Label("Recent", systemImage: "clock").tag(Item.recent)
    }
    Section("Library") {
      ForEach(items) { item in
        Label(item.name, systemImage: item.icon).tag(item)
      }
    }
  }
  .listStyle(.sidebar)
  .navigationTitle("Library")
} detail: {
  // Main content
  DetailView(item: selectedItem)
}
```

### Sidebar Visual Rules
- Row selection uses system blue (highlighted) or light gray (unfocused)
- Section headers: uppercase, 11pt, secondary label color
- Row height: 28–32pt with icon
- Sidebar background: `NSColor.windowBackgroundColor` with vibrancy (`.sidebar` material)

---

## Split Views

### SwiftUI
```swift
// Two-panel (sidebar + content)
NavigationSplitView { SidebarView() } detail: { DetailView() }

// Three-panel (sidebar + content + inspector)
NavigationSplitView {
  SidebarView()
} content: {
  ContentListView()
} detail: {
  InspectorView()
}
```

### Inspector (Trailing Panel)
```swift
// macOS 14+
.inspector(isPresented: $showInspector) {
  InspectorView()
    .inspectorColumnWidth(min: 200, ideal: 260, max: 400)
}
```

---

## Panels & Inspectors

Inspectors/panels show contextual details. They typically float on the trailing side.

### AppKit Floating Panel
```swift
let panel = NSPanel(contentRect: ..., 
                    styleMask: [.titled, .closable, .utilityWindow],
                    backing: .buffered, defer: false)
panel.isFloatingPanel = true
panel.becomesKeyOnlyIfNeeded = true  // Doesn't steal key focus
```

### Size: 
- Width: 260–320pt
- Background: `NSColor.windowBackgroundColor` or `.underWindowBackground`

---

## Sheets & Dialogs

### Sheets (Modal, attached to window)
```swift
.sheet(isPresented: $showSheet) {
  VStack(spacing: 16) {
    Text("Title").font(.headline)
    Text("Description").foregroundStyle(.secondary)
    HStack {
      Button("Cancel") { showSheet = false }
        .keyboardShortcut(.cancelAction)
      Button("Confirm") { confirm(); showSheet = false }
        .buttonStyle(.borderedProminent)
        .keyboardShortcut(.defaultAction)
    }
  }
  .padding(20)
  .frame(minWidth: 300)
}
```

### Alerts
```swift
.alert("Delete File?", isPresented: $showAlert) {
  Button("Delete", role: .destructive) { delete() }
  Button("Cancel", role: .cancel) { }
} message: {
  Text("This action cannot be undone.")
}
```

### Alert Design Rules
- Destructive button: Red label, right-aligned
- Cancel: Always present, keyboard shortcut Escape
- Default action: Keyboard shortcut Return
- Max 3 buttons; use sheets for more options

---

## Popovers

Contextual UI attached to a button or view. Avoid using for critical actions.

### SwiftUI
```swift
Button("Options") {
  showPopover = true
}
.popover(isPresented: $showPopover, arrowEdge: .bottom) {
  VStack(alignment: .leading, spacing: 8) {
    Button("Action 1") { }
    Divider()
    Button("Action 2") { }
  }
  .padding(12)
  .frame(width: 200)
}
```

### Design Rules
- Width: 200–320pt
- Arrow points to triggering element
- Background: `.popover` material (blurred)
- Dismiss by clicking outside

---

## HUD & Overlays

HUD (Head-Up Display) windows — used for floating non-interactive overlays.

### AppKit HUD
```swift
let hud = NSPanel(...)
hud.styleMask = [.hudWindow, .titled, .utilityWindow]
// Renders with dark glass appearance
```

### Toast / Notification Overlay (CSS)
```css
.toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(40, 40, 40, 0.9);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  backdrop-filter: blur(12px);
  animation: fadeInUp 0.25s ease;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateX(-50%) translateY(8px); }
  to   { opacity: 1; transform: translateX(-50%) translateY(0); }
}
```
