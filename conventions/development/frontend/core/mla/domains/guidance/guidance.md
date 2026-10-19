# Guidance

*Last updated: 2026-10-19*

> The context a region needs — a legend, what a control applies to, the gestures it takes, the period and units of
> its figures — behind an info button that opens on click. A guided first-visit tour is a separate pattern.

## Placement

- must keep inline only copy that changes the next action on every read
  ([UI copy](../../../../../../design/content/ui-copy.md)).
- must put behind the info button what a region needs explained once: its context, legend, instructions and units.
- must not put behind it what the screen cannot be operated without — a field error, a consequence, a next step.
- must not keep a description line under a title that is pure context; it moves behind the title's info button.

---

## Content

- must give the region's context: what it shows, and where its figures come from.
- must give each legend the region draws — colour, mark, line, icon — drawn the way the region draws it.
- must give the instructions and gestures the region takes, such as `Drag to move · Pinch or Ctrl + scroll to zoom`.
- must give the units and periods of its figures, such as `minutes over the last 30 days`.
- must explain only its own region; a nested region with its own legend takes its own button.
- must head the panel with the region's title and each section with its own; a single section takes none.
- should fit without scrolling; a long legend moves to the region it explains rather than growing one panel.

---

## Info button

- must sit right after the title it explains, in the title row and outside the heading element, so the heading's
  name stays the title; one per titled region.
- must be an icon-only ghost `Button`, `sm` and `square`, holding the `Info` glyph at 16px, named `About {title}`.
- must reach 44px on phones without growing the title row — a negative block margin absorbs the extra height.
- must be dimmed — the subtle foreground — and take the foreground on hover, focus and while open.
- must open on click only: never by itself, never on hover.
- must open every section at once — a [Popover](../../components/overlays/popover.md) from `md`, a
  [BottomSheet](../../components/overlays/bottomSheet.md) on phones.
- must open the popover on the side with room, below by preference, and cap its height to that room, scrolling
  inside rather than past the screen's edge.
- must hold a close button, close on Escape and an outside click, and return focus to the button.

---

## Reveal

- must, on a device that hovers with a fine pointer — `(hover: hover) and (pointer: fine)` — stay hidden until the
  pointer is over its region or focus is inside it.
- must take as its region the nearest ancestor that declares one (`data-info-scope`): a panel declares itself.
- must hide by opacity only, never `display` or `visibility`, so it stays in the tab order and focus reveals it.
- must, on a touch device — no hover, or a coarse pointer — always show, dimmed: nothing hovers there, and a tap
  that revealed it would first act on whatever it landed on.
- must show while open, and always when it belongs to no region.
- must not animate the reveal under reduced motion.

---

## Tours

- A guided first-visit tour is a separate pattern ([TourPopover](../../components/overlays/tourPopover.md)): its own
  text, a blurred spotlight over the page, and its own seen state.
- must not open an info button's panel, step through its sections or remember it as seen.
- must not share text with an info button; a tour says what to do first, the info button what the region means.

---

```txt
✅ Services  ⓘ          the legend, "Drag to move · Pinch or Ctrl + scroll to zoom" and what the lines measure inside
✅ ⓘ dimmed on a phone  a touch screen has no hover, so the button never hides there
❌ a legend row under the map on every visit       read once, shown forever
❌ the panel opening by itself on the first visit  that is a tour, a separate pattern
❌ the button inside the <h2>                      the heading's name becomes "Services About Services"
```

---

## Neighbours

- [TourPopover](../../components/overlays/tourPopover.md) — a guided walk over a whole feature, not one region's context
- [UI copy](../../../../../../design/content/ui-copy.md) — how many words a screen carries inline
- [responsive](../../../../shapes/app/responsive/responsive.md) — the phone class and its touch target
