# Controls

## Table of Contents
1. [Buttons](#buttons)
2. [Text Fields](#text-fields)
3. [Checkboxes & Radio Buttons](#checkboxes--radio-buttons)
4. [Segmented Controls](#segmented-controls)
5. [Sliders & Steppers](#sliders--steppers)
6. [Pickers & Dropdowns](#pickers--dropdowns)
7. [Progress Indicators](#progress-indicators)
8. [Toggles & Switches](#toggles--switches)
9. [Search Fields](#search-fields)
10. [Tables & Lists](#tables--lists)

---

## Buttons

### Button Styles (HIG Hierarchy)

| Style         | Usage                            | Visual                    |
|---------------|----------------------------------|---------------------------|
| Primary (default) | Main action in a view          | Blue filled, rounded      |
| Secondary     | Secondary action                 | Gray/outline, rounded     |
| Destructive   | Irreversible action (delete)    | Red or gray, confirm first |
| Borderless    | Toolbar, inline actions         | Text only, no border      |
| Help          | Opens help documentation        | Circle with "?"           |
| Disclosure    | Expand/collapse                 | Triangle chevron          |

### Sizing
| Size     | Height | Font Size | Padding (H) |
|----------|--------|-----------|-------------|
| Mini     | 15pt   | 9pt       | 6pt         |
| Small    | 18pt   | 11pt      | 8pt         |
| Regular  | 22pt   | 13pt      | 12pt        |
| Large    | 28pt   | 15pt      | 16pt        |

### SwiftUI
```swift
// Primary
Button("Save") { }.buttonStyle(.borderedProminent)

// Secondary
Button("Cancel") { }.buttonStyle(.bordered)

// Destructive
Button("Delete", role: .destructive) { }

// Borderless
Button("More") { }.buttonStyle(.plain)

// With control size
Button("Submit") { }
  .controlSize(.large)
  .buttonStyle(.borderedProminent)
  .keyboardShortcut(.defaultAction)  // responds to Return key
```

### AppKit
```swift
// Standard push button
let btn = NSButton(title: "OK", target: self, action: #selector(confirm))
btn.bezelStyle = .rounded
btn.keyEquivalent = "\r"  // Return key = default button

// Destructive
btn.hasDestructiveAction = true  // macOS 14+

// Toolbar button
let tbBtn = NSButton(image: NSImage(systemSymbolName: "plus", ...)!, 
                     target: self, action: #selector(add))
tbBtn.bezelStyle = .toolbar
```

### CSS/Electron
```css
/* Primary button */
.btn-primary {
  background: var(--system-blue, #007AFF);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 13px;
  font-weight: 400;
  padding: 4px 14px;
  height: 22px;
  cursor: default;
  user-select: none;
}
.btn-primary:hover { background: #0070E0; }
.btn-primary:active { background: #0062C0; transform: scale(0.98); }

/* Secondary */
.btn-secondary {
  background: transparent;
  border: 1px solid rgba(0,0,0,0.2);
  border-radius: 5px;
  font-size: 13px;
  padding: 4px 14px;
  height: 22px;
  cursor: default;
}
@media (prefers-color-scheme: dark) {
  .btn-secondary { border-color: rgba(255,255,255,0.2); }
}
```

---

## Text Fields

### Styles
- **Default (rounded):** Standard input with border and background
- **Plain:** No visible border (used in search, inline editing)
- **Underline:** Uncommon on macOS, avoid

### SwiftUI
```swift
TextField("Placeholder", text: $value)
  .textFieldStyle(.roundedBorder)
  .controlSize(.large)

// Secure
SecureField("Password", text: $password)
  .textFieldStyle(.roundedBorder)
```

### AppKit
```swift
let field = NSTextField()
field.placeholderString = "Enter value"
field.bezelStyle = .roundedBezel
field.isBezeled = true
```

### CSS
```css
.text-field {
  height: 22px;
  padding: 2px 8px;
  border: 1px solid rgba(0,0,0,0.25);
  border-radius: 5px;
  background: white;
  font-size: 13px;
  outline: none;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
.text-field:focus {
  border-color: var(--system-blue, #007AFF);
  box-shadow: 0 0 0 3px rgba(0,122,255,0.3);
}
@media (prefers-color-scheme: dark) {
  .text-field {
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.2);
    color: white;
  }
}
```

---

## Checkboxes & Radio Buttons

### SwiftUI
```swift
Toggle("Enable feature", isOn: $enabled)
  .toggleStyle(.checkbox)      // Checkbox style

// Radio group
Picker("Option", selection: $selected) {
  Text("Option A").tag("a")
  Text("Option B").tag("b")
}.pickerStyle(.radioGroup)
```

### AppKit
```swift
let checkbox = NSButton(checkboxWithTitle: "Enable", target: self, action: #selector(toggle))

let radio = NSButton(radioButtonWithTitle: "Option A", target: self, action: #selector(select))
```

### CSS
```css
/* Style native checkboxes to match macOS */
input[type="checkbox"] {
  width: 14px;
  height: 14px;
  accent-color: var(--system-blue, #007AFF);
  cursor: default;
}
```

---

## Segmented Controls

Use for mutually exclusive views or modes (not for toggles in isolation).

### SwiftUI
```swift
Picker("View", selection: $selection) {
  Text("List").tag(0)
  Text("Grid").tag(1)
  Text("Column").tag(2)
}.pickerStyle(.segmented)
```

### AppKit
```swift
let seg = NSSegmentedControl(labels: ["List", "Grid"], trackingMode: .selectOne,
                              target: self, action: #selector(segmentChanged))
```

---

## Sliders & Steppers

### SwiftUI
```swift
Slider(value: $volume, in: 0...100)
Stepper("Count: \(count)", value: $count, in: 0...10)
```

### AppKit
```swift
let slider = NSSlider(value: 50, minValue: 0, maxValue: 100,
                      target: self, action: #selector(sliderChanged))
slider.sliderType = .linear
```

---

## Pickers & Dropdowns

### SwiftUI
```swift
// Inline picker
Picker("Sort by", selection: $sortKey) {
  Text("Name").tag("name")
  Text("Date").tag("date")
}.pickerStyle(.menu)     // Dropdown menu

// Inline radio
Picker(...).pickerStyle(.inline)
```

### AppKit
```swift
let popup = NSPopUpButton(frame: .zero, pullsDown: false)
popup.addItems(withTitles: ["Option 1", "Option 2"])
```

---

## Progress Indicators

### SwiftUI
```swift
// Indeterminate spinner
ProgressView()

// Determinate bar
ProgressView(value: 0.7)
  .progressViewStyle(.linear)

// With label
ProgressView("Loading…", value: progress, total: 1.0)
```

### AppKit
```swift
let spinner = NSProgressIndicator()
spinner.style = .spinning
spinner.startAnimation(nil)

let bar = NSProgressIndicator()
bar.style = .bar
bar.isIndeterminate = false
bar.doubleValue = 70
```

---

## Toggles & Switches

macOS 14+ supports native toggle switch style.

### SwiftUI
```swift
Toggle("Dark mode", isOn: $isDark)
  .toggleStyle(.switch)   // iOS-style switch (macOS 14+)
```

---

## Search Fields

### SwiftUI
```swift
TextField("Search", text: $query)
  .textFieldStyle(.roundedBorder)
  .overlay(Image(systemName: "magnifyingglass"), alignment: .leading)

// Or use SearchBar modifier (macOS 13+)
.searchable(text: $query, prompt: "Search")
```

### AppKit
```swift
let search = NSSearchField()
search.placeholderString = "Search"
```

### CSS
```css
.search-field {
  padding-left: 28px;  /* Space for search icon */
  background-image: url("data:image/svg+xml,...magnifying-glass...");
  background-repeat: no-repeat;
  background-position: 8px center;
  border-radius: 8px;   /* Fully rounded search bar */
}
```

---

## Tables & Lists

### SwiftUI
```swift
List(items, id: \.id) { item in
  HStack {
    Image(systemName: item.icon)
    Text(item.name)
    Spacer()
    Text(item.detail).foregroundStyle(.secondary)
  }
}
.listStyle(.sidebar)      // For sidebars
.listStyle(.inset)        // For content lists
.listStyle(.bordered)     // For inspector-style lists
```

### Row Height Guidelines
| List type        | Row height |
|------------------|-----------|
| Compact          | 18–20pt   |
| Default          | 24–28pt   |
| With subtitle    | 38–44pt   |
| With image       | 44–52pt   |

### Selection & Hover (CSS)
```css
.list-row {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 13px;
  cursor: default;
  user-select: none;
}
.list-row:hover {
  background: rgba(0,0,0,0.05);
}
.list-row.selected {
  background: var(--system-blue, #007AFF);
  color: white;
}
/* When window unfocused */
.list-row.selected:not(:focus-within) {
  background: rgba(0,0,0,0.1);
  color: inherit;
}
@media (prefers-color-scheme: dark) {
  .list-row:hover { background: rgba(255,255,255,0.08); }
  .list-row.selected:not(:focus-within) { background: rgba(255,255,255,0.1); }
}
```
