# AppKit Implementation Patterns

## Table of Contents
1. [View Hierarchy](#view-hierarchy)
2. [Auto Layout](#auto-layout)
3. [Appearance & Dark Mode](#appearance--dark-mode)
4. [Common Views](#common-views)
5. [NSViewController Lifecycle](#nsviewcontroller-lifecycle)
6. [NSWindowController](#nswindowcontroller)
7. [Notifications & KVO](#notifications--kvo)

---

## View Hierarchy

AppKit uses `NSView` as the base class. All views have a coordinate system with origin at **bottom-left** (flipped views at top-left).

```swift
// Standard flipped view (top-left origin — more intuitive for most layouts)
class FlippedView: NSView {
  override var isFlipped: Bool { true }
}

// Adding subviews
parentView.addSubview(childView)
view.subviews  // Array of subviews
```

---

## Auto Layout

Always use Auto Layout (NSLayoutConstraint or layout anchors). Avoid `frame` assignments unless in `layout()`.

```swift
// Setup: disable autoresizing mask
subview.translatesAutoresizingMaskIntoConstraints = false
view.addSubview(subview)

// Pin to edges with insets
NSLayoutConstraint.activate([
  subview.topAnchor.constraint(equalTo: view.topAnchor, constant: 20),
  subview.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
  subview.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
  subview.bottomAnchor.constraint(equalTo: view.bottomAnchor, constant: -20),
])

// Stack views (like HStack/VStack in SwiftUI)
let stack = NSStackView(views: [label, button])
stack.orientation = .horizontal   // or .vertical
stack.spacing = 8
stack.alignment = .centerY
stack.distribution = .fill
```

---

## Appearance & Dark Mode

```swift
// Current appearance
let isDark = NSApp.effectiveAppearance.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua

// Observe appearance changes
override func viewDidChangeEffectiveAppearance() {
  super.viewDidChangeEffectiveAppearance()
  updateColors()
}

// Force light/dark for a specific view
view.appearance = NSAppearance(named: .darkAqua)
view.appearance = NSAppearance(named: .aqua)

// Semantic colors (auto-adapt to appearance)
view.layer?.backgroundColor = NSColor.windowBackgroundColor.cgColor
label.textColor = NSColor.labelColor
field.textColor = NSColor.secondaryLabelColor

// ⚠️ Always resolve dynamic colors in drawing context:
let resolvedColor = NSColor.labelColor.resolvedColor(
  with: view.effectiveAppearance
)
```

---

## Common Views

### NSLabel (NSTextField as read-only)
```swift
let label = NSTextField(labelWithString: "Hello, macOS!")
label.textColor = .labelColor
label.font = NSFont.systemFont(ofSize: 13)
label.isEditable = false
label.isSelectable = false
label.isBezeled = false
label.drawsBackground = false
```

### NSVisualEffectView (Vibrancy/Blur)
```swift
let vibrancy = NSVisualEffectView()
vibrancy.material = .sidebar          // .menu, .popover, .hudWindow, .sidebar, .contentBackground
vibrancy.blendingMode = .behindWindow // .withinWindow for in-app blur
vibrancy.state = .active
view.addSubview(vibrancy)
```

### NSScrollView
```swift
let scroll = NSScrollView()
scroll.documentView = contentView
scroll.hasVerticalScroller = true
scroll.hasHorizontalScroller = false
scroll.autohidesScrollers = true
scroll.drawsBackground = false
```

### NSTableView
```swift
// Register cell view
tableView.register(NSNib(nibNamed: "CellView", bundle: nil), forIdentifier: .init("cell"))

// Delegate/Datasource
func numberOfRows(in tableView: NSTableView) -> Int { items.count }
func tableView(_ tv: NSTableView, viewFor col: NSTableColumn?, row: Int) -> NSView? {
  let cell = tv.makeView(withIdentifier: .init("cell"), owner: self) as? NSTableCellView
  cell?.textField?.stringValue = items[row].name
  return cell
}
```

---

## NSViewController Lifecycle

```swift
class MyViewController: NSViewController {
  override func loadView() {
    // Build view programmatically (if not using XIB)
    view = NSView(frame: NSRect(x: 0, y: 0, width: 800, height: 600))
    setupViews()
  }
  
  override func viewDidLoad() {
    super.viewDidLoad()
    // Initial setup
  }
  
  override func viewWillAppear() {
    super.viewWillAppear()
    // View about to become visible
  }
  
  override func viewDidAppear() {
    super.viewDidAppear()
    // Make first responder etc.
    view.window?.makeFirstResponder(searchField)
  }
  
  override func viewWillDisappear() {
    // Save state
  }
}
```

---

## NSWindowController

```swift
class MainWindowController: NSWindowController {
  convenience init() {
    let vc = MainViewController()
    let window = NSWindow(contentViewController: vc)
    window.setContentSize(NSSize(width: 900, height: 600))
    window.minSize = NSSize(width: 480, height: 300)
    window.title = "My App"
    window.center()
    self.init(window: window)
  }
  
  override func windowDidLoad() {
    super.windowDidLoad()
    window?.titlebarAppearsTransparent = false
    window?.toolbarStyle = .unified
  }
}

// Application delegate
func applicationDidFinishLaunching(_ notification: Notification) {
  mainWindowController = MainWindowController()
  mainWindowController?.showWindow(nil)
}
```

### Saving Window State
```swift
// Auto-restore window position
window.setFrameAutosaveName("MainWindow")

// Restore manually
if !window.setFrameUsingName("MainWindow") {
  window.center()
}
```

---

## Notifications & KVO

```swift
// Observe window focus
NotificationCenter.default.addObserver(
  self, selector: #selector(windowDidBecomeKey),
  name: NSWindow.didBecomeKeyNotification, object: window
)

@objc func windowDidBecomeKey() {
  // Update UI when window gains focus
}

// KVO for property changes
observation = someObject.observe(\.someProperty, options: [.new]) { _, change in
  DispatchQueue.main.async { self.update() }
}
```
