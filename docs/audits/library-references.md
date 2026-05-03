# P5 — External library audit

*Last updated: 2026-05-03*

> **Phase**: P5 of [`ui-beta-roadmap.md`](../ui-beta-roadmap.md)
> **Goal**: Walk component lists from Radix · shadcn · Mantine · MUI · Ark UI · React Aria. For each component, decide: useful for wow-two ecosystem? Y/N · already in beta? Y/N · if both criteria match, add to P3 target list.
> **Status**: Initial audit. Re-walk after each major P3 push.

---

## Methodology

| Library | Source of truth | Components counted |
|---|---|---|
| **Radix Primitives** | `radix-ui/primitives` GitHub `packages/react/` | 60 packages (incl. utility hooks) |
| **shadcn/ui** | [ui.shadcn.com/docs/components](https://ui.shadcn.com/docs/components) | 58 |
| **Mantine** | [mantine.dev/core/package](https://mantine.dev/core/package/) | 95 |
| **MUI Material** | [mui.com/material-ui/all-components](https://mui.com/material-ui/all-components/) | 60 |
| **Ark UI** | [ark-ui.com/docs/components](https://ark-ui.com/) | 58 |
| **React Aria Components** | `adobe/react-spectrum` `packages/react-aria-components/src/` | 60 |
| **`@wow-two-beta/ui`** | repo `src/` snapshot | 119 (13 primitives + 49 atoms + 57 molecules) |

---

## Library snapshots

### Radix Primitives

**Components (34):** `accessible-icon`, `accordion`, `alert-dialog`, `announce`, `arrow`, `aspect-ratio`, `avatar`, `checkbox`, `collapsible`, `context-menu`, `dialog`, `dropdown-menu`, `form`, `hover-card`, `label`, `menu`, `menubar`, `navigation-menu`, `one-time-password-field`, `password-toggle-field`, `popover`, `progress`, `radio-group`, `scroll-area`, `select`, `separator`, `slider`, `switch`, `tabs`, `toast`, `toggle`, `toggle-group`, `toolbar`, `tooltip`

**Primitives / utilities (13):** `collection`, `dismissable-layer`, `focus-guards`, `focus-scope`, `popper`, `portal`, `presence`, `primitive`, `roving-focus`, `slot`, `visually-hidden`, `direction`, `compose-refs`

**Hooks (10):** `use-callback-ref`, `use-controllable-state`, `use-effect-event`, `use-escape-keydown`, `use-is-hydrated`, `use-layout-effect`, `use-previous`, `use-rect`, `use-size`, `id`, `context`

### shadcn/ui

Accordion · Alert · Alert Dialog · Aspect Ratio · Avatar · Badge · Breadcrumb · Button · Button Group · Calendar · Card · Carousel · Chart · Checkbox · Collapsible · Combobox · Command · Context Menu · Data Table · Date Picker · Dialog · Direction · Drawer · Dropdown Menu · Empty · Field · Hover Card · Input · Input Group · Input OTP · Item · Kbd · Label · Menubar · Native Select · Navigation Menu · Pagination · Popover · Progress · Radio Group · Resizable · Scroll Area · Select · Separator · Sheet · Sidebar · Skeleton · Slider · Sonner · Spinner · Switch · Table · Tabs · Textarea · Toast · Toggle · Toggle Group · Tooltip · Typography

### Mantine

**Layout:** AppShell · AspectRatio · Center · Container · Flex · Grid · Group · SimpleGrid · Space · Stack
**Inputs:** AlphaSlider · AngleSlider · Checkbox · Chip · ColorInput · ColorPicker · Fieldset · FileInput · HueSlider · Input · JsonInput · MaskInput · NativeSelect · NumberInput · PasswordInput · PinInput · Radio · RangeSlider · Rating · SegmentedControl · Slider · Switch · Textarea · TextInput
**Combobox:** Autocomplete · Combobox · MultiSelect · Pill · PillsInput · Select · TagsInput
**Buttons:** ActionIcon · Button · CloseButton · CopyButton · FileButton · UnstyledButton
**Navigation:** Anchor · Breadcrumbs · Burger · NavLink · Pagination · Stepper · TableOfContents · Tabs · Tree
**Feedback:** Alert · Loader · Notification · Progress · RingProgress · SemiCircleProgress · Skeleton
**Overlays:** Affix · Dialog · Drawer · FloatingIndicator · FloatingWindow · HoverCard · LoadingOverlay · Menu · Modal · Overlay · Popover · Tooltip
**Data display:** Accordion · Avatar · BackgroundImage · Badge · Card · ColorSwatch · Image · Indicator · Kbd · NumberFormatter · OverflowList · Spoiler · ThemeIcon · Timeline
**Typography:** Blockquote · Code · Highlight · List · Mark · Table · Text · Title · Typography
**Misc:** Box · Collapse · Divider · FocusTrap · Marquee · Paper · Portal · ScrollArea · Scroller · Transition · VisuallyHidden

### MUI Material

**Inputs:** Autocomplete · Button · ButtonGroup · Checkbox · Floating Action Button · Number Field · Radio Group · Rating · Select · Slider · Switch · Text Field · Transfer List · Toggle Button
**Data display:** Avatar · Badge · Chip · Divider · Icons · Material Icons · List · Table · Tooltip · Typography
**Feedback:** Alert · Backdrop · Dialog · Progress · Skeleton · Snackbar
**Surfaces:** Accordion · App Bar · Card · Paper
**Navigation:** Bottom Navigation · Breadcrumbs · Drawer · Link · Menu · Menubar · Pagination · Speed Dial · Stepper · Tabs
**Layout:** Box · Container · Grid · Stack · Image List
**Lab:** Masonry · Timeline
**Utils:** Click-Away Listener · CssBaseline · Modal · No SSR · Popover · Popper · Portal · Textarea Autosize · Transitions · useMediaQuery

### Ark UI

**Components:** Accordion · Angle Slider · Avatar · Carousel · Checkbox · Clipboard · Collapsible · Color Picker · Combobox · Date Picker · Dialog · Editable · Field · Fieldset · File Upload · Floating Panel · Image Cropper · Hover Card · Listbox · Marquee · Menu · Number Input · Pagination · Password Input · Pin Input · Popover · Progress (Circular + Linear) · QR Code · Radio Group · Rating Group · Scroll Area · Segment Group · Select · Signature Pad · Slider · Splitter · Steps · Switch · Tabs · Tags Input · Timer · Toast · Toggle · Toggle Group · Tooltip · Tour · Tree View
**Utilities:** Client Only · Download Trigger · Environment · Focus Trap · Format Byte · Format Time · Format Relative Time · Frame · Highlight · JSON Tree View · Locale · Presence · Swap

### React Aria Components

Autocomplete · Breadcrumbs · Button · Calendar · Checkbox · Collection · ColorArea · ColorField · ColorPicker · ColorSlider · ColorSwatch · ColorSwatchPicker · ColorThumb · ColorWheel · ComboBox · DateField · DatePicker · Dialog · Disclosure · DragAndDrop · DropZone · FieldError · FileTrigger · Form · GridList · Group · Header · Heading · HiddenDateInput · Input · Keyboard · Label · Link · ListBox · Menu · Meter · Modal · NumberField · OverlayArrow · Popover · ProgressBar · RadioGroup · SearchField · Select · SelectionIndicator · Separator · SharedElementTransition · Slider · Switch · Table · Tabs · TagGroup · Text · TextArea · TextField · Toast · ToggleButton · ToggleButtonGroup · Toolbar · Tooltip

---

## Master matrix

Legend: ✓ = present · — = absent · *(name)* = present under a different name · β = `@wow-two-beta/ui`

Verdict codes:
- **✅** — already in β
- **➕L3 / L4 / L5 / L6** — add to P3 list at the indicated layer
- **⏳** — already on the L5 candidate list, not yet built
- **⏭** — intentional skip (with reason)
- **🔁** — covered by composition (no dedicated component needed)

### Layout primitives

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Box | — | — | ✓ | ✓ | — | ✓ *(Group)* | ✓ | ✅ |
| Stack | — | — | ✓ | ✓ | — | — | ✓ | ✅ |
| HStack/VStack | — | — | *(Group)* | — | — | — | ✓ | ✅ |
| Grid | — | — | ✓ | ✓ | — | — | ✓ | ✅ |
| SimpleGrid (auto-fit) | — | — | ✓ | — | — | — | ✓ *(Grid)* | ✅ |
| Container | — | — | ✓ | ✓ | — | — | ✓ | ✅ |
| Flex | — | — | ✓ | — | — | — | ✓ | ✅ |
| Center | — | — | ✓ | — | — | — | ✓ | ✅ |
| Cluster (wrapping row) | — | — | *(Group)* | — | — | — | ✓ | ✅ |
| Inline (text-flow row) | — | — | — | — | — | — | ✓ | ✅ |
| Frame (aspect-locked container) | — | — | — | — | ✓ | — | ✓ | ✅ |
| TwoColumn (sidebar+main) | — | — | — | — | — | — | ✓ | ✅ |
| Spacer | — | — | ✓ *(Space)* | — | — | — | ✓ | ✅ |
| AspectRatio | ✓ | ✓ | ✓ | — | — | — | ✓ | ✅ |
| ScrollArea | ✓ | ✓ | ✓ | — | ✓ | — | ✓ | ✅ |
| Separator/Divider | ✓ | ✓ | ✓ *(Divider)* | ✓ | — | ✓ | ✓ | ✅ |
| AppShell | — | — | ✓ | *(AppBar)* | — | — | — | ➕L6 (defer — full-app frame) |
| Paper / Surface | — | — | ✓ | ✓ | — | — | 🔁 *(Card)* | ⏭ — Card covers it |
| Affix (sticky helper) | — | — | ✓ | — | — | — | — | ⏭ — utility, not a component |
| Masonry | — | — | — | ✓ | — | — | — | ⏭ — niche, Grid handles |
| ImageList | — | — | — | ✓ | — | — | — | ⏭ — niche |

### Typography & display primitives

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Text | — | *(Typography)* | ✓ | ✓ | — | ✓ | ✓ | ✅ |
| Heading | — | *(Typography)* | ✓ *(Title)* | ✓ | — | ✓ | ✓ | ✅ |
| Code | — | — | ✓ | — | — | — | ✓ | ✅ |
| Kbd | — | ✓ | ✓ | — | — | ✓ *(Keyboard)* | ✓ | ✅ |
| Mark | — | — | ✓ | — | — | — | ✓ | ✅ |
| Highlight (text find-marker) | — | — | ✓ | — | ✓ | — | ✓ | ✅ |
| Quote / Blockquote | — | — | ✓ *(Blockquote)* | — | — | — | ✓ | ✅ |
| List (ul/ol semantic) | — | — | ✓ | ✓ | — | — | — | ➕L4 (lightweight, semantic) |
| Snippet (copy-cmd block) | — | — | — | — | — | — | ✓ | ✅ |
| Avatar | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✅ |
| AvatarGroup | — | — | — | — | — | — | ✓ | ✅ |
| Badge | — | ✓ | ✓ | ✓ | — | — | ✓ | ✅ |
| BadgeOverlay (positioned) | — | — | *(Indicator)* | *(Badge w/ overlap)* | — | — | ✓ | ✅ |
| CountBadge | — | — | — | — | — | — | ✓ | ✅ |
| NotificationDot | — | — | *(Indicator)* | — | — | — | ✓ | ✅ |
| Tag / Chip | — | — | — | ✓ *(Chip)* | — | ✓ *(TagGroup)* | ✓ *(Tag)* | ✅ |
| Image | — | — | ✓ | — | — | — | ✓ | ✅ |
| Card | — | ✓ | ✓ | ✓ | — | — | ✓ | ✅ |
| EmptyState | — | ✓ *(Empty)* | — | — | — | — | ✓ | ✅ |
| Stat / Metric | — | — | — | — | — | — | ✓ | ✅ |
| TrendIndicator | — | — | — | — | — | — | ✓ | ✅ |
| Status (dot+label) | — | — | — | — | — | — | ✓ | ✅ |
| StatusIndicator | — | — | — | — | — | — | ✓ | ✅ |
| KeyboardShortcut | — | — | — | — | — | — | ✓ | ✅ |
| InfoRow (label-value pair) | — | — | — | — | — | — | ✓ | ✅ |
| DescriptionList (dl) | — | — | — | — | — | — | ✓ | ✅ |
| SectionHeader | — | — | — | — | — | — | ✓ | ✅ |
| ColorSwatch (single chip) | — | — | ✓ | — | — | ✓ | — | ➕L4 |
| ThemeIcon (icon+bg+color) | — | — | ✓ | — | — | — | 🔁 *(IconButton/Box)* | ⏭ — composition |

### Buttons & actions

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Button | — | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✅ |
| ButtonGroup | — | ✓ | — | ✓ | — | — | ✓ | ✅ |
| IconButton (a.k.a. ActionIcon) | — | — | ✓ *(ActionIcon)* | *(Button)* | — | — | ✓ | ✅ |
| FAB | — | — | — | ✓ | — | — | ✓ | ✅ |
| ToggleButton | — | ✓ *(Toggle)* | — | ✓ | ✓ *(Toggle)* | ✓ | ✓ | ✅ |
| ToggleButtonGroup | — | ✓ *(Toggle Group)* | ✓ *(Chip.Group)* | ✓ | ✓ *(Toggle Group)* | ✓ | ✓ | ✅ |
| SegmentedControl | — | — | ✓ | — | ✓ *(Segment Group)* | — | ✓ | ✅ |
| CopyButton | — | — | ✓ | — | — | — | ✓ | ✅ |
| DisclosureButton | — | — | — | — | — | — | ✓ | ✅ |
| OverlayButton (positioned) | — | — | — | — | — | — | ✓ | ✅ |
| CloseButton (X icon button) | — | — | ✓ | — | — | — | 🔁 *(IconButton+lucide X)* | ⏭ — composition |
| Burger (hamburger toggle) | — | — | ✓ | — | — | — | 🔁 *(IconButton+icon)* | ⏭ — composition |
| FileButton (file picker trigger) | — | — | ✓ | — | — | ✓ *(FileTrigger)* | 🔁 *(FilePicker covers)* | ⏭ — covered |
| UnstyledButton | — | — | ✓ | — | — | — | 🔁 *(`asChild`)* | ⏭ — polymorphism rule covers |
| SpeedDial (FAB+menu) | — | — | — | ✓ | — | — | — | ➕L5 (compose FAB+Menu) |
| Link | — | — | ✓ *(Anchor)* | ✓ | — | ✓ | ✓ | ✅ |
| NavLink | — | — | ✓ | — | — | — | ✓ *(NavItem)* | ✅ |

### Form controls (atomic inputs)

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| TextInput | — | ✓ *(Input)* | ✓ | ✓ *(TextField)* | — | ✓ *(TextField)* | ✓ | ✅ |
| Textarea | — | ✓ | ✓ | ✓ *(TextField multiline)* | — | ✓ | ✓ | ✅ |
| EmailInput | — | — | — | — | — | — | ✓ | ✅ |
| PasswordInput | — | — | ✓ | — | ✓ | — | ✓ | ✅ |
| PasswordToggleField | ✓ | — | — | — | — | — | 🔁 *(PasswordInput visible toggle)* | ⏭ — covered |
| SearchInput | — | — | — | — | — | ✓ *(SearchField)* | ✓ | ✅ |
| TelInput | — | — | — | — | — | — | ✓ | ✅ |
| UrlInput | — | — | — | — | — | — | ✓ | ✅ |
| NumberInput | — | — | ✓ | ✓ *(NumberField)* | ✓ | ✓ *(NumberField)* | ✓ | ✅ |
| CurrencyInput | — | — | — | — | — | — | ✓ | ✅ |
| PercentInput | — | — | — | — | — | — | ✓ | ✅ |
| MaskedInput | — | — | ✓ *(MaskInput)* | — | — | — | ✓ | ✅ |
| PinInput / OTP | — | ✓ *(Input OTP)* | ✓ | — | ✓ | — | ✓ | ✅ |
| OneTimePasswordField | ✓ | *(Input OTP)* | — | — | — | — | 🔁 *(PinInput)* | ⏭ — covered |
| Checkbox | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✅ |
| CheckboxGroup | — | — | *(Checkbox.Group)* | — | — | — | ✓ | ✅ |
| Radio | ✓ *(RadioGroup)* | ✓ *(RadioGroup)* | ✓ | ✓ *(RadioGroup)* | ✓ *(RadioGroup)* | ✓ *(RadioGroup)* | ✓ | ✅ |
| RadioGroup | ✓ | ✓ | *(Radio.Group)* | ✓ | ✓ | ✓ | ✓ | ✅ |
| Switch | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✅ |
| Slider | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✅ |
| RangeSlider | — | — | ✓ | ✓ *(Slider range)* | — | — | — | ➕L4 (extend Slider) |
| AngleSlider | — | — | ✓ | — | ✓ | — | — | ⏭ — niche |
| Rating | — | — | ✓ | ✓ | ✓ *(Rating Group)* | — | — | ➕L4 |
| Chip (filter chip) | — | — | ✓ | — | — | — | 🔁 *(Tag toggleable)* | ⏭ — Tag covers |
| ChoiceCard (large radio card) | — | — | — | — | — | — | ✓ | ✅ |
| FilePicker / FileUpload | — | — | ✓ *(FileInput)* | — | ✓ *(File Upload)* | ✓ *(FileTrigger)* | ✓ *(FilePicker — atomic)* | ✅ atomic; ⏳L5 (Dropzone) |
| ColorInput | — | — | ✓ | — | ✓ *(Color Picker)* | ✓ *(ColorField)* | — | ➕L5 (with picker) |
| JsonInput | — | — | ✓ | — | — | — | — | ⏭ — niche |
| NativeSelect (fallback) | — | ✓ | ✓ | — | — | — | — | ➕L3 (low-effort, useful for SSR-light cases) |

### Form wrappers & meta

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Form (root wrapper) | ✓ | — | — | — | — | ✓ | — | ➕L4 (semantic root, validation hooks) |
| FormField | *(Form.Field)* | ✓ *(Field)* | — | — | ✓ *(Field)* | — | ✓ | ✅ |
| Fieldset | — | — | ✓ | — | ✓ | — | ✓ | ✅ |
| Legend | — | — | *(Fieldset.Legend)* | — | — | — | ✓ | ✅ |
| Label | ✓ | ✓ | — | — | ✓ *(Field.Label)* | ✓ | ✓ | ✅ |
| FormErrorMessage | — | *(Field error)* | — | — | *(Field error)* | ✓ *(FieldError)* | ✓ | ✅ |
| FormHelperText | — | *(Field description)* | — | — | *(Field helper)* | — | ✓ | ✅ |
| Group (input cluster) | — | — | ✓ | — | — | ✓ | ✓ *(InputGroup)* | ✅ |
| InputAddon (prefix/suffix) | — | — | *(TextInput.Section)* | *(TextField adornment)* | — | — | ✓ | ✅ |
| LabeledInput | — | — | — | — | — | — | ✓ | ✅ |
| CharacterCount | — | — | — | — | — | — | ✓ | ✅ |
| PasswordStrength | — | — | — | — | — | — | ✓ | ✅ |
| CheckboxField (Field+Checkbox) | — | — | — | — | — | — | ✓ | ✅ |
| RadioField | — | — | — | — | — | — | ✓ | ✅ |
| SwitchField | — | — | — | — | — | — | ✓ | ✅ |
| TransferList (dual-listbox) | — | — | — | ✓ | — | — | — | ⏭ — niche, defer |

### Selection menus

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Select (single) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ⏳L5 |
| MultiSelect | — | — | ✓ | — | *(Select multi)* | — | — | ⏳L5 |
| Combobox (typeahead+select) | ✓ | ✓ | ✓ | ✓ *(Autocomplete)* | ✓ | ✓ *(ComboBox)* | — | ⏳L5 |
| Autocomplete (free-text+suggest) | — | — | ✓ | ✓ | — | ✓ | — | ⏳L5 (Combobox variant) |
| Listbox (raw selection list) | — | — | — | — | ✓ | ✓ *(ListBox)* | — | ➕L5 (raw primitive for Select/Combobox internals) |
| TagsInput | — | — | ✓ | — | ✓ *(Tags Input)* | ✓ *(TagGroup)* | — | ⏳L5 |
| PillsInput | — | — | ✓ | — | — | — | 🔁 *(TagsInput)* | ⏭ — same shape |
| Pill (tag-as-chip) | — | — | ✓ | — | — | — | 🔁 *(Tag)* | ⏭ — Tag covers |
| Menu (raw menu primitive) | ✓ | — | ✓ | ✓ | ✓ | ✓ | — | ⏳L5 |
| DropdownMenu (button+menu) | ✓ | ✓ | *(Menu)* | *(Menu)* | *(Menu)* | *(Menu+Button)* | — | ⏳L5 |
| ContextMenu (right-click) | ✓ | ✓ | — | — | — | — | — | ⏳L5 |
| Menubar (top-level menu bar) | ✓ | ✓ | — | ✓ | — | — | — | ➕L5 |
| Command (palette / fuzzy menu) | — | ✓ | — | — | — | — | — | ⏳L5 (CommandPalette) |
| NavigationMenu (mega-menu) | ✓ | ✓ | — | — | — | — | — | ➕L5 |

### Date & time

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Calendar | — | ✓ | (in @mantine/dates) | (in @mui/x-date-pickers) | (in Date Picker) | ✓ | — | ➕L4 (date grid only) |
| DateField (atomic input) | — | — | (in @mantine/dates) | — | — | ✓ | — | ➕L4 |
| TimeField (atomic input) | — | — | — | — | — | — | — | ➕L4 |
| DatePicker (input+popover+cal) | — | ✓ | (in @mantine/dates) | (in @mui/x-date-pickers) | ✓ | ✓ | — | ⏳L5 |
| DateRangePicker | — | — | (in @mantine/dates) | (in @mui/x-date-pickers) | — | — | — | ➕L5 |
| TimePicker | — | — | (in @mantine/dates) | (in @mui/x-date-pickers) | — | — | — | ⏳L5 |
| RangeCalendar | — | — | (in @mantine/dates) | — | — | ✓ | — | ➕L5 |
| HiddenDateInput (a11y helper) | — | — | — | — | — | ✓ | — | ⏭ — internal helper, not consumer-facing |

### Color

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| ColorPicker (full) | — | — | ✓ | — | ✓ | ✓ | — | ⏳L5 |
| ColorField (text-input HEX) | — | — | ✓ *(ColorInput)* | — | — | ✓ | — | ➕L4 |
| ColorArea (2D picker) | — | — | — | — | — | ✓ | — | ➕L5 (part of ColorPicker) |
| ColorWheel | — | — | — | — | — | ✓ | — | ➕L5 (part of ColorPicker) |
| ColorSlider (channel slider) | — | — | ✓ *(HueSlider/AlphaSlider)* | — | — | ✓ | — | ➕L5 (part of ColorPicker) |
| ColorSwatch (chip preview) | — | — | ✓ | — | — | ✓ | — | ➕L4 |
| ColorSwatchPicker (palette) | — | — | — | — | — | ✓ | — | ➕L5 |

### Disclosure

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Accordion | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | ⏳L5 |
| Collapsible | ✓ | ✓ | ✓ *(Collapse)* | — | ✓ | ✓ *(Disclosure)* | — | ⏳L5 |
| Disclosure / DisclosureGroup | — | — | — | — | — | ✓ | 🔁 *(DisclosureButton at L4 covers trigger)* | ➕L5 (full state-managed) |
| Spoiler (read-more wrapper) | — | — | ✓ | — | — | — | — | ⏭ — Collapsible covers |
| Tabs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ⏳L5 |
| Stepper (with state) | — | — | ✓ | ✓ | ✓ *(Steps)* | — | — | ⏳L5 (we have ProgressSteps display-only at L4) |

### Overlays & floating

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Modal (centered overlay) | — | — | ✓ | ✓ | — | ✓ | — | ⏳L5 |
| Dialog (semantic alias) | ✓ | ✓ | ✓ | ✓ *(Dialog)* | ✓ | ✓ | — | ⏳L5 |
| AlertDialog (confirm) | ✓ | ✓ | — | — | — | — | — | ⏳L5 |
| Drawer (side panel) | — | ✓ | ✓ | ✓ | — | — | — | ⏳L5 |
| Sheet (bottom drawer) | — | ✓ | — | — | — | — | — | 🔁 *(Drawer with `side="bottom"`)* |
| Popover | ✓ | ✓ | ✓ | ✓ *(Popover util)* | ✓ | ✓ | — | ⏳L5 |
| HoverCard | ✓ | ✓ | ✓ | — | ✓ | — | — | ⏳L5 |
| Tooltip | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✅ |
| Toast (single) | ✓ | ✓ | — | ✓ *(Snackbar)* | ✓ | ✓ | ✓ | ✅ |
| Toaster (manager / queue) | — | ✓ *(Sonner)* | ✓ *(notifications)* | — | — | — | — | ⏳L5 |
| Banner / inline notification | — | — | ✓ *(Notification)* | — | — | — | ✓ | ✅ |
| LoadingOverlay (block-with-spinner) | — | — | ✓ | ✓ *(Backdrop)* | — | — | 🔁 *(Skeleton/LoadingState)* | ➕L5 (explicit overlay variant) |
| FloatingPanel / FloatingWindow | — | — | ✓ | — | ✓ | — | — | ⏭ — niche, defer |
| FloatingIndicator (animated marker) | — | — | ✓ | — | — | — | — | ⏭ — niche |
| Affix (sticky-on-scroll) | — | — | ✓ | — | — | — | — | ⏭ — utility |
| Backdrop / Overlay (raw scrim) | — | — | ✓ *(Overlay)* | ✓ *(Backdrop)* | — | — | — | ➕L5 (used by Modal/Drawer internally) |

### Navigation

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Breadcrumb | — | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✅ |
| Pagination | — | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✅ |
| NavItem | — | — | ✓ *(NavLink)* | — | — | — | ✓ | ✅ |
| Sidebar | — | ✓ | ✓ *(AppShell.Navbar)* | ✓ *(Drawer)* | — | — | — | ➕L6 (haven uses; pattern-level) |
| AppBar / TopBar | — | — | ✓ *(AppShell.Header)* | ✓ | — | — | — | ➕L6 |
| BottomNavigation | — | — | — | ✓ | — | — | — | ⏭ — mobile-specific, defer |
| Toolbar | ✓ | — | — | — | — | ✓ | — | ➕L5 |
| TableOfContents | — | — | ✓ | — | — | — | — | ⏭ — niche, defer |
| Tour (guided walkthrough) | — | — | — | — | ✓ | — | — | ⏭ — L7 pattern, defer indefinitely |

### Feedback

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Alert | — | ✓ | ✓ | ✓ | — | — | ✓ | ✅ |
| Banner | — | — | — | — | — | — | ✓ | ✅ |
| Callout | — | — | — | — | — | — | ✓ | ✅ |
| Notification (toast inline body) | — | — | ✓ | — | — | — | 🔁 *(Toast)* | ⏭ — covered |
| Spinner / Loader | — | ✓ | ✓ *(Loader)* | — | — | — | ✓ | ✅ |
| InlineSpinner | — | — | — | — | — | — | ✓ | ✅ |
| LoadingState | — | — | — | — | — | — | ✓ | ✅ |
| Skeleton | — | ✓ | ✓ | ✓ | — | — | ✓ | ✅ |
| ProgressBar | ✓ | ✓ *(Progress)* | ✓ *(Progress)* | ✓ | ✓ | ✓ | ✓ | ✅ |
| ProgressCircle | — | — | ✓ *(RingProgress/SemiCircleProgress)* | ✓ *(Circular)* | ✓ *(Circular)* | — | ✓ | ✅ |
| ProgressSteps (display) | — | — | ✓ *(Stepper display)* | — | — | — | ✓ | ✅ |
| MeterBar (rated value) | — | — | — | — | — | ✓ *(Meter)* | ✓ | ✅ |

### Data display

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Table (semantic) | — | ✓ | ✓ | ✓ | — | ✓ | — | ⏳L5 |
| DataTable (sort/filter/paginate) | — | ✓ | — | (separate `@mui/x-data-grid`) | — | — | — | ⏳L5 |
| List (semantic) | — | — | ✓ | ✓ | — | — | — | ➕L4 |
| Tree / TreeView | — | — | ✓ | (separate `@mui/x-tree-view`) | ✓ | — | — | ⏳L5 |
| Timeline | — | — | ✓ | ✓ *(Lab)* | — | — | — | ➕L5 |
| Carousel | — | ✓ | (in @mantine/carousel) | — | ✓ | — | — | ⏳L5 |
| Chart | — | ✓ *(Chart)* | (in @mantine/charts) | — | — | — | — | ⏭ — domain layer (consumers wrap viz lib) |
| OverflowList ("+N more") | — | — | ✓ | — | — | — | — | ➕L4 |
| ResizablePanels / Splitter | — | ✓ *(Resizable)* | — | — | ✓ *(Splitter)* | — | — | ⏳L5 |

### Specialized

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| RichTextEditor | — | — | (in @mantine/tiptap) | — | — | — | — | ⏳L5 |
| Editable (inline edit) | — | — | — | — | ✓ | — | — | ➕L5 |
| Marquee (scrolling text) | — | — | ✓ | — | ✓ | — | — | ⏭ — niche |
| QRCode | — | — | — | — | ✓ | — | — | ⏭ — niche, no haven need yet |
| SignaturePad | — | — | — | — | ✓ | — | — | ⏭ — niche |
| ImageCropper | — | — | — | — | ✓ | — | — | ⏭ — niche |
| Clipboard (copy primitive) | — | — | — | — | ✓ | — | 🔁 *(`useClipboard` + CopyButton)* | ⏭ — covered |
| Timer (stopwatch/countdown) | — | — | — | — | ✓ | — | — | ⏭ — niche |
| Announce (screen-reader live) | ✓ | — | — | — | — | — | — | ➕L2 (a11y primitive) |
| DragAndDrop / DropZone | — | — | — | — | — | ✓ | 🔁 *(FilePicker covers basic)* | ➕L5 (Dropzone) — already on L5 list as FileUpload |

### Foundation primitives (L2)

| Concept | Radix | shadcn | Mantine | MUI | Ark | RA | β | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Slot (asChild merge) | ✓ | — | — | — | — | — | ✓ | ✅ |
| Portal | ✓ | — | ✓ | ✓ | — | — | ✓ | ✅ |
| VisuallyHidden | ✓ | — | ✓ | — | — | — | ✓ | ✅ |
| Presence (mount/unmount anim) | ✓ | — | ✓ *(Transition)* | ✓ *(Transitions)* | ✓ | — | ✓ | ✅ |
| DirectionProvider (LTR/RTL) | ✓ | ✓ *(Direction)* | — | — | — | — | ✓ | ✅ |
| AccessibleIcon | ✓ | — | — | — | — | — | ✓ | ✅ |
| FocusScope (focus trap) | ✓ | — | ✓ *(FocusTrap)* | — | ✓ *(Focus Trap)* | — | ✓ | ✅ |
| DismissableLayer | ✓ | — | — | ✓ *(Click-Away Listener)* | — | — | ✓ | ✅ |
| AnchoredPositioner (Popper) | ✓ *(Popper)* | — | — | ✓ *(Popper)* | — | — | ✓ | ✅ |
| RovingFocusGroup | ✓ | — | — | — | — | — | ✓ | ✅ |
| Collection (descendant tracking) | ✓ | — | — | — | — | ✓ | ✓ | ✅ |
| FormControlContext | — | — | — | — | — | — | ✓ | ✅ (bespoke) |
| ScrollLockProvider | — | — | — | — | — | — | ✓ | ✅ |
| Announce (live region) | ✓ | — | — | — | — | — | — | ➕L2 |
| OverlayArrow (tip arrow) | ✓ *(Arrow)* | — | — | — | — | ✓ | — | ➕L2 |

---

## Synthesis — additions to P3

Items below are net-new from this audit (not already in beta and not already on the L5 candidate list). Cross-reference with [`ui-beta-roadmap.md`](../ui-beta-roadmap.md) §P3 target list and `system/sessions/ui-beta-build/context.md` open items.

### L2 primitives (new)

| Component | Why | Sources |
|---|---|---|
| **Announce** | A11y live-region helper — needed for status messages, toast queues. | Radix |
| **OverlayArrow** | Reusable tip-arrow primitive for floating elements. We use floating-ui already; expose a styled wrapper. | Radix · React Aria |

### L3 atoms (new)

| Component | Why | Sources |
|---|---|---|
| **NativeSelect** | Atomic native `<select>` fallback for low-effort cases (forms in non-critical surfaces, mobile-first contexts). Cheap to ship. | shadcn · Mantine |

### L4 molecules (new)

| Component | Why | Sources |
|---|---|---|
| **Form** (root) | Semantic `<form>` wrapper with submit/validation hooks; pairs with FormField. | Radix · React Aria |
| **List** | Semantic `<ul>/<ol>` with bullet styles + spacing tokens. Lightweight typography piece. | Mantine · MUI |
| **OverflowList** | "+N more" auto-truncating row — common UI pattern (chips, avatars, tags). | Mantine |
| **Calendar** | Atomic month grid (no input). Building block for DatePicker. Standalone use as date display. | shadcn · React Aria |
| **DateField** | Tokenized atomic date input (mm/dd/yyyy segments). Accessible alternative to native `<input type="date">`. | React Aria |
| **TimeField** | Atomic time input (hh:mm with am/pm segments). | React Aria |
| **ColorField** | Text-input HEX/RGB color entry. Standalone or paired with Swatch. | Mantine · React Aria |
| **ColorSwatch** | Single-color preview chip. Used in palettes, picker triggers. | Mantine · React Aria |
| **RangeSlider** | Two-thumb slider variant. Extend existing Slider. | Mantine · MUI |
| **Rating** | Star-rating input. Common in haven (review/feedback flows). | Mantine · MUI · Ark |

### L5 organisms (new — to add to existing L5 list)

| Component | Why | Sources |
|---|---|---|
| **Listbox** | Raw selection list primitive. Powers Select/Combobox internals; also useful standalone. | Ark · React Aria |
| **Menubar** | Top-level menu bar (File / Edit / View pattern). | Radix · shadcn · MUI |
| **NavigationMenu** | Mega-menu navigation (top-level site nav with rich content panes). | Radix · shadcn |
| **Toolbar** | Container for grouped controls (toolbars in editors, action bars). | Radix · React Aria |
| **DateRangePicker** | Two-date selection variant. | Mantine · MUI |
| **RangeCalendar** | Two-date calendar grid. | React Aria |
| **ColorPicker** (full) | Composes ColorArea + ColorWheel + ColorSliders + Swatches + ColorField. | Mantine · Ark · React Aria |
| **ColorArea** · **ColorWheel** · **ColorSlider** · **ColorSwatchPicker** | Building blocks of ColorPicker — shippable on their own. | React Aria |
| **Disclosure / DisclosureGroup** (state-managed) | Single-region show/hide with ARIA. Different from L4 DisclosureButton (which is just trigger). | Radix · React Aria |
| **Stepper (state-managed)** | Stateful workflow stepper — distinct from L4 ProgressSteps (display only). | Mantine · MUI · Ark |
| **Backdrop / Overlay** | Raw scrim primitive used by Modal, Drawer, LoadingOverlay. Ship as standalone. | Mantine · MUI |
| **LoadingOverlay** | Block container with spinner + scrim — common loading-state pattern. | Mantine |
| **Editable** | Inline-editable text (click-to-edit). | Ark |
| **Timeline** | Vertical event/activity feed. | Mantine · MUI Lab |
| **List (advanced)** | Semantic list with primary/secondary/avatar slots — beyond L4 plain list. | MUI |
| **SpeedDial** | FAB with radial menu. Composition: FAB + Menu. | MUI |

### L5 already on candidate list (confirmed by audit, no change)

Modal · Dialog · AlertDialog · Drawer · Popover · HoverCard · Menu · ContextMenu · DropdownMenu · CommandPalette · Combobox · Select · MultiSelect · TagsInput · DatePicker · TimePicker · FileUpload (Dropzone) · TagsInput · Tabs · Accordion · Collapsible · Toaster · Table · DataTable · Tree · Carousel · ResizablePanels · RichTextEditor

Strong haven priorities flagged in context.md still hold: **Select · MultiSelect · Collapsible · DataTable · FloatingBar**.

### L6 patterns (deferred — not in P3 scope)

| Pattern | Why deferred |
|---|---|
| **Sidebar / NavSection** | Pattern-level (already noted as L6 in context.md). Haven's expandable left nav. |
| **AppShell** | Full-app frame (header + nav + main + footer). Mantine has it. L6/L7 territory. |
| **AppBar / TopBar** | Top app bar — pairs with Sidebar at L6. |

---

## Skip list (intentional non-builds)

Components present in references but excluded with rationale:

| Component | Source | Reason |
|---|---|---|
| Paper / Surface | Mantine · MUI | `Card` covers; no separate surface primitive needed |
| Affix | Mantine | Sticky-on-scroll is a utility, not a component (CSS `position: sticky`) |
| CssBaseline / Reset | MUI | Tailwind preflight covers |
| NoSsr | MUI | Beta is CSR-only (decision locked) |
| TextareaAutosize | MUI | Ship as variant of Textarea, not separate component |
| TableOfContents | Mantine | Niche; consumer apps rarely need it |
| Masonry | MUI | Niche; CSS Grid covers most layouts |
| ImageList | MUI | Niche; Grid + Image covers |
| BottomNavigation | MUI | Mobile-specific; defer to a mobile-pattern phase if ever needed |
| Tour | Ark | Walkthrough pattern — L7 territory, no haven need |
| QRCode | Ark | Niche; consumers can wrap external lib |
| SignaturePad | Ark | Niche; not in haven |
| ImageCropper | Ark | Niche; not in haven |
| Marquee | Mantine · Ark | Decorative, low-value |
| FloatingPanel / FloatingWindow | Mantine · Ark | Niche; Drawer covers most cases |
| FloatingIndicator | Mantine | Niche animated UI element |
| AngleSlider | Mantine · Ark | Niche; included only inside ColorPicker if at all |
| JsonInput | Mantine | Niche developer tool |
| TransferList | MUI | Niche dual-list pattern; revisit if a real need surfaces |
| Spoiler | Mantine | Read-more — Collapsible covers |
| Burger / CloseButton | Mantine | Compositions of IconButton + lucide icon |
| ThemeIcon | Mantine | Composition of IconButton + Box bg |
| Pill / PillsInput | Mantine | Same shape as Tag / TagsInput |
| FileButton | Mantine · React Aria | FilePicker (atomic) covers; Dropzone (L5) covers visual surface |
| OneTimePasswordField / PasswordToggleField | Radix | PinInput / PasswordInput already cover the same UX |
| Chart | shadcn · Mantine charts | Domain-layer concern; consumer wraps a viz lib (recharts, visx, etc.) |
| HiddenDateInput | React Aria | Internal a11y helper, not a consumer-facing component |
| UnstyledButton | Mantine | `asChild` / `Slot` covers polymorphism — already documented in P1 rules |

---

## Open follow-ups

- **P4 Haven audit** (`docs/audits/haven-component-gaps.md`) — to be produced alongside this once initial layer build is complete (per user direction). Will cross-reference haven's component inventory against this matrix and the L5 build-out.
- **Re-walk schedule**: this doc is a snapshot. Re-walk each major lib at the end of P3 (when L5 lands) and again before P6 — libraries gain components quickly.
- **One mid-build addition path**: when a haven component or a real consumer surfaces a need not in this matrix, add it to the relevant L4/L5 section + this doc's matrix in the same commit.
