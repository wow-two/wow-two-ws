# Responsive proposals

*Last updated: 2026-10-16*

> Draft rules for the [responsive](responsive.md) convention, open for discussion — none binds a product yet.
> Use case — the owner's review in Wheelhouse v0.5.

## Review

- must not apply a draft below as a rule; only [responsive](responsive.md) binds a product.
- must move a promoted draft into the doc that owns it, as written, and delete it here.
- must delete a rejected proposal; git keeps the record.

---

## Proposals

Each entry: the draft rule, why it is needed, and how the Vue UI SDK (`@wow-two-beta/ui-vue`) would carry it.
Listed in the order a page applies them.

### Breakpoints and containers

- draft — must switch each pattern at its named step: `sm` dialogs · `md` tables and navigation · `lg` list and
  detail, sidebars.
- draft — must adapt a component inside a pane that can be narrow on a wide screen by its container
  (`@container`, `@sm:`), not the viewport.
- why — a `DataTable` in a 20rem list pane on desktop stays a table at phone width; a viewport query cannot see it.
- SDK — the step defaults already agree (`stackBreakpoint` `md`, `ListDetailLayout` `lg`, `AppShell`
  `sidebarBreakpoint` `lg`); `Table` would gain a container mode on Tailwind 4's built-in container queries.

### Touch targets and spacing

- draft — must give a touch target a 44 × 44px hit area under a coarse pointer even when its glyph is smaller, and
  keep 8px between adjacent targets; a fine pointer keeps the 24 × 24px floor.
- why — the 44px rule says nothing of spacing or of hit area versus glyph, so a dense row of icon buttons passes
  on paper and mis-taps in the hand. Apple sets 44pt; WCAG 2.2 SC 2.5.8 sets 24px with a spacing exception.
- SDK — `Button` and the icon buttons grow their hit area under Tailwind's `pointer-coarse:` variant;
  `ButtonGroup` and `Toolbar` add the gap.

### Hover-only affordances

- draft — must show a hover-revealed control at rest under a coarse pointer, or move it into the row's menu; a
  tooltip never carries information found nowhere else.
- why — Tailwind 4's `hover:` applies only where the device can hover, so a control revealed on hover never
  appears on a phone.
- SDK — `useHoverCapability` and `usePointerType` exist; `HoverCard` would open on tap, as a `Popover`, under a
  coarse pointer.

### Swipe row actions

- draft — must offer a phone row's two main actions by swipe — the main one leading, the destructive one
  trailing — through `SwipeActionsLayout`, and keep both in the row's menu.
- why — the owner wants swipe for the two main row actions; WCAG 2.2 SC 2.5.7 requires a single-pointer path for
  every drag, and a swipe is not discoverable.
- SDK — `DataTable` would gain a row-actions descriptor that wraps each stacked card in `SwipeActionsLayout`
  below `md` and renders the row menu at every width.
- open — one action per side, or both trailing as in a mail list.

### Long press and edge gestures

- draft — may open a row's menu on long press; must leave edge swipes and pinch zoom to the browser.
- why — iOS uses the edge swipe for back, so a page that captures it breaks back; blocking zoom fails WCAG
  SC 1.4.4.
- SDK — `useLongPress` and `ContextMenu` exist; `SwipeActionsLayout` would ignore a drag that starts at a screen
  edge.

### Pull to refresh

- draft — must refresh a phone list on a pull from its top when the page has a refresh command, running that same
  refresh.
- why — the toolbar refresh sits out of thumb reach, and a pull is the gesture phone users try first.
- SDK — `PullToRefreshLayout` wired to `useRefresh`, so a pull shows the matched skeleton refresh; it would set
  `overscroll-behavior-y: contain` so the browser's own pull-to-reload stays out.
- open — `AppShellMain` is the one scroll container and `PullToRefreshLayout` wants to be its own; one yields.

### Bottom bar behaviour

- draft — must keep the bottom bar fixed while the page scrolls; a place beyond five lives inside a destination
  or the account menu, never behind a "More" tab.
- why — a bar that hides on scroll moves its targets under the thumb; a "More" tab puts destinations a tap
  deeper.
- SDK — `BottomNavMenu` already pins by default (`isFixed`); hiding it is left to the keyboard proposal below.

### Sticky actions and safe areas

- draft — must pin a phone page's primary action in a bottom action bar above the bottom bar, and add
  `viewport-fit=cover` to the viewport so every pinned edge pads by `env(safe-area-inset-*)`.
- why — the action beside the page heading ([shell](../shell/shell.md#page-heading)) scrolls away on a long
  phone page; without `viewport-fit=cover`, iOS letterboxes the page and the safe-area insets stay unused.
- SDK — `StickyLayout` pins the bar; `BottomNavMenu` and `ModalContent` already pad by the insets; a safe-area
  utility in `index.css` would serve app-owned edges. Promotion edits [document](../platform/document.md#head).

### Virtual keyboard

- draft — must keep the focused field and a full-screen dialog's footer above the on-screen keyboard, and hide
  the bottom bar while the keyboard is open.
- why — the keyboard covers the lower half of a phone; a pinned footer or bar either hides behind it or rides up
  over the field being typed in.
- SDK — none today: `interactive-widget=resizes-content` in the viewport serves Chromium and Firefox, and a new
  `useVisualViewport` hook serves Safari; `ModalContent` and `BottomNavMenu` would read it.

### Forms on phones

- draft — must choose each field's keyboard and autofill: the typed input (`EmailInput`, `TelInput`,
  `NumberInput`, `UrlInput`), an `autocomplete` token on identity, address and payment fields, `enterkeyhint` on
  the last field, and 16px input text on phones.
- why — the wrong keyboard and a missed autofill are the main costs of typing on a phone, and iOS Safari zooms
  into any input whose text is under 16px.
- SDK — the typed inputs set `type`; they would also set `inputmode`, default `autocomplete` and phone
  `text-base`. Password autofill → [PasswordInput](../../../core/mla/components/forms/passwordInput.md).

### Pages versus dialogs

- draft — must give a form its own route when it has several sections, earns a deep link, or opens from several
  places; a short single-purpose edit stays a `Modal`.
- why — `con-t-013` and the Wheelhouse backlog leave this open; on phones both render full screen, so the choice is
  URL, history and length, not size.
- SDK — none needed; overlay interception already serves both ([routing](../routing/routing.md#places)).

### Typography and density

- draft — must keep body and input text at 16px on phones, and `cozy` density or roomier under a coarse pointer.
- why — desktop density makes a row shorter than a fingertip, and phone text under 16px strains reading.
- SDK — `TableDensity` and the list densities would default by pointer (`pointer-coarse:`); the theme type scale
  would gain a phone step.

### Images and icons

- draft — must reserve every image's aspect ratio and lazy-load images below the fold; must give an icon-only
  control an accessible name and the full touch hit area.
- why — a late image shifts a phone layout under the thumb, and icon-only buttons are a page's smallest targets.
- SDK — `AspectRatioLayout` and `ImagePreview` exist; responsive sources stay with
  [assets](../platform/assets.md#images), icon sizes with [lucide](../../../core/mla/domains/icons/lucide/lucide.md).

### Orientation

- draft — must work in both orientations and never lock one; on a short landscape phone the bottom bar drops its
  labels.
- why — WCAG SC 1.3.4 forbids an orientation lock, and a landscape phone loses a third of its height to the bar.
- SDK — `useOrientation` exists; `BottomNavMenu` would hide labels under a short-height media query.

### Transitions

- draft — must animate a route change and the list-to-detail swap with the View Transitions API, and a progress
  step with a state transition, all under `motion-safe:`.
- why — the settled motion rule names no mechanism, and today the list-detail swap and `ProgressStepsIndicator`
  change instantly.
- SDK — the router adapter would wrap navigation in `document.startViewTransition` where the browser has it;
  `ListDetailLayout` and `ProgressStepsIndicator` would animate their own changes; other browsers swap instantly.

### Background progress

- draft — must keep a long task visible after its dialog closes, as a compact progress notice — a deployment
  rollout.
- why — on a phone the dialog covers the screen, and closing it today hides the task.
- SDK — the `notify()` feedback bus would gain progress notices any app can publish, drawn with `ProgressBar`.

### Offline and slow network

- draft — must show one quiet offline state in the shell, keep last good content, and disable writes while
  offline with the reason on the control.
- why — phones drop the network mid-task, and a write that fails offline costs the reader's input.
- SDK — `useOnlineStatus` exists; the shell would raise a `Banner` from it, and `useAppQuery` would pause while
  offline.

### Testing at widths

- draft — must run the browser suite at each class's verify size in Chromium and WebKit with touch on the phone,
  check reflow at 320px, and pass one real-phone check before a version closes.
- why — the SDK's phone layouts broke in WebKit alone, emulation misses the keyboard, safe areas and gestures,
  and WCAG SC 1.4.10 sets 320px.
- SDK — its browser tests already run Chromium, WebKit and Firefox; a shared viewport preset per class would
  ship beside them for apps.

---

## Sources

- touch targets — [WCAG 2.2 SC 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) ·
  [Apple HIG accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).
- gestures — [WCAG 2.2 SC 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html) ·
  [SC 1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html).
- bottom bar — [Android navigation bar](https://developer.android.com/develop/ui/compose/components/navigation-bar)
  (three to five destinations) ·
  [Apple HIG tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars).
- viewport, keyboard, safe areas —
  [MDN viewport meta](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport).
- pointer and hover variants — [Tailwind states](https://tailwindcss.com/docs/hover-focus-and-other-states).
- orientation and reflow — [SC 1.3.4](https://www.w3.org/WAI/WCAG22/Understanding/orientation.html) ·
  [SC 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).
