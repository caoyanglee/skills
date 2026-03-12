# SwiftUI Implementation Patterns

## Table of Contents
1. [App & Scene Setup](#app--scene-setup)
2. [Adaptive Colors & Appearance](#adaptive-colors--appearance)
3. [Native Feel Modifiers](#native-feel-modifiers)
4. [Layout Best Practices](#layout-best-practices)
5. [Animations](#animations)
6. [SF Symbols](#sf-symbols)
7. [Accessibility](#accessibility)

---

## App & Scene Setup

```swift
@main struct MyApp: App {
  @NSApplicationDelegateAdaptor(AppDelegate.self) var delegate
  
  var body: some Scene {
    WindowGroup {
      ContentView()
        .frame(minWidth: 800, minHeight: 500)
    }
    .defaultSize(width: 1000, height: 650)
    .commands {
      // Custom menu commands
    }
    
    Settings {
      SettingsView()
    }
  }
}
```

---

## Adaptive Colors & Appearance

Always use semantic colors and materials — never hardcode hex values.

```swift
// ✅ Good — adapts to light/dark automatically
Text("Label").foregroundStyle(.primary)
Text("Detail").foregroundStyle(.secondary)
Text("Hint").foregroundStyle(.tertiary)

// ✅ System colors
Color.accentColor         // User's accent color
Color(.controlBackground) // Control backgrounds
Color(.windowBackground)  // Window background

// ❌ Bad — hardcoded
Text("Label").foregroundColor(Color(hex: "#000000"))

// Material backgrounds
RoundedRectangle(cornerRadius: 8)
  .fill(.regularMaterial)

// Dynamic color with light/dark variants
Color(light: Color(.sRGB, red: 0.9, green: 0.9, blue: 0.9),
      dark:  Color(.sRGB, red: 0.15, green: 0.15, blue: 0.15))
```

---

## Native Feel Modifiers

Essential modifiers for native macOS feel:

```swift
// Prevent text selection (for UI labels, not content)
Text("Title").textSelection(.disabled)

// Cursor default for clickable items in macOS
.onHover { hovering in cursor = hovering ? .pointingHand : .arrow }

// Disable focus ring where inappropriate
.focusable(false)

// Native vibrancy/material background
.background(.sidebar)            // Sidebar fill
.background(.windowBackground)   // Main window fill
.background(.regularMaterial)    // Blur material

// Rounded corners with continuous curve (Apple squircle style)
.clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))

// Context menu (right-click)
.contextMenu { MenuItems() }

// Drag source
.draggable(item)

// Drop target
.dropDestination(for: Item.self) { items, _ in handle(items) }
```

---

## Layout Best Practices

```swift
// Use container-relative sizing instead of fixed sizes
.containerRelativeFrame(.horizontal, count: 3, span: 1, spacing: 16)

// Adaptive grid
LazyVGrid(columns: [GridItem(.adaptive(minimum: 180))], spacing: 16) {
  ForEach(items) { ItemView($0) }
}

// Standard content padding
.padding()              // 16pt all sides
.padding(.horizontal, 20)

// Toolbar integration with safe area
.ignoresSafeArea(.container, edges: .top)  // Allow content under toolbar

// Dividers
Divider()  // Full-width separator
```

### NavigationSplitView (preferred for macOS)
```swift
NavigationSplitView {
  SidebarView()
    .navigationSplitViewColumnWidth(min: 180, ideal: 240)
} detail: {
  DetailView()
}
.navigationSplitViewStyle(.balanced)
// or .prominentDetail for content-focused layouts
```

---

## Animations

Use Apple's spring animations for a native feel:

```swift
// Default spring (most common)
withAnimation(.spring()) { state.toggle() }

// Snappy spring (for immediate responses)
withAnimation(.snappy) { value = newValue }

// Smooth spring (for large content transitions)
withAnimation(.smooth) { isExpanded.toggle() }

// Custom spring
withAnimation(.spring(response: 0.35, dampingFraction: 0.75)) { }

// Matched geometry (hero animation)
.matchedGeometryEffect(id: item.id, in: namespace)

// Transition
.transition(.move(edge: .trailing).combined(with: .opacity))
```

### Animation Principles
- Use spring animations (not linear/easeInOut) for interactive gestures
- Keep durations short: 0.2–0.4s for most UI transitions
- Animate appearance/disappearance with `.opacity` + `.scale(0.95)` combined

---

## SF Symbols

SF Symbols are the standard icon system for macOS.

```swift
// Basic symbol
Image(systemName: "folder.fill")

// With rendering mode
Image(systemName: "heart.fill")
  .symbolRenderingMode(.hierarchical)   // Depth with opacity
  .symbolRenderingMode(.palette)        // Multiple colors
  .symbolRenderingMode(.multicolor)     // Preset colors
  .symbolRenderingMode(.monochrome)     // Single color

// Symbol effect (macOS 14+)
Image(systemName: "wifi")
  .symbolEffect(.pulse)                 // Subtle pulse animation
  .symbolEffect(.bounce, value: trigger)
  .symbolEffect(.variableColor.cumulative)

// Variable value (for signals, volume, etc.)
Image(systemName: "wifi", variableValue: 0.7)

// Control size (adapts to context automatically)
Image(systemName: "gear")
  .imageScale(.large)   // .small, .medium, .large
  .font(.title2)        // Scales the symbol
```

### Common macOS Symbols

| Usage              | Symbol Name                     |
|--------------------|---------------------------------|
| Settings/Prefs     | `gear`, `gearshape`             |
| Add                | `plus`, `plus.circle.fill`      |
| Remove/Delete      | `minus`, `trash`                |
| Edit               | `pencil`, `square.and.pencil`   |
| Share              | `square.and.arrow.up`           |
| Search             | `magnifyingglass`               |
| Filter             | `line.3.horizontal.decrease.circle` |
| Folder             | `folder`, `folder.fill`         |
| Document           | `doc`, `doc.fill`               |
| Back/Forward       | `chevron.left`, `chevron.right` |
| Expand/Collapse    | `chevron.up`, `chevron.down`    |
| Sidebar toggle     | `sidebar.left`                  |
| Info               | `info.circle`                   |
| Warning            | `exclamationmark.triangle`      |
| Success            | `checkmark.circle.fill`         |
| Close              | `xmark`, `xmark.circle.fill`    |

---

## Accessibility

```swift
// Accessibility label (for screen readers)
Image(systemName: "star.fill")
  .accessibilityLabel("Favorite")

// Hint for complex interactions
Button("Submit") { }
  .accessibilityHint("Submits the form and saves changes")

// Group related elements
VStack { ... }
  .accessibilityElement(children: .combine)

// Dynamic type support (automatic with system fonts)
Text("Body").font(.body)   // Scales with user preference

// Reduce motion
@Environment(\.accessibilityReduceMotion) var reduceMotion
let animation: Animation = reduceMotion ? .none : .spring()
```
