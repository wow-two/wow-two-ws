# Guidance

*Last updated: 2026-10-18*

> Explanation a screen needs once — a legend, a control's reach, how to read a chart — behind an info button,
> with a first-run intro and a remembered "seen" state.

## Placement

- must keep inline only copy that changes the next action on every read
  ([UI copy](../../../../../../design/content/ui-copy.md)).
- must put content read once behind an info button: a legend or colour key, what a control reaches, a how-to hint.
- must not put behind it what the screen cannot be operated without — a field error, a consequence, a next step.
- must not add a title's description line that only explains a control the info button already explains.

---

## Info button

- must sit right after the title it explains, inside the title row; one per titled region.
- must be an icon-only ghost `Button`, `sm` and `square`, holding the `Info` glyph at 16px, named `About {title}`.
- must reach 44px on phones without growing the title row — a negative block margin absorbs the extra height.
- must open every section at once — a [Popover](../../components/overlays/popover.md) from `md`, a
  [BottomSheet](../../components/overlays/bottomSheet.md) on phones.
- must head the panel with the region's title and each section with its own; a single section takes none.
- must hold a close button, close on Escape and an outside click, and return focus to the button.

---

## Intro

- may open once by itself, the first time the reader meets a region whose reading is not obvious — a grid, a chart.
- must wait until the region has rendered, its button shows whole and most of the first step's target is on screen.
- must not open while focus is in a field, a menu or another dialog; it retries a few times, then waits a visit.
- must show the info button's own sections, one per step — one source for both, at most four steps.
- must open in a popover above the info button on every screen class — a sheet would hide the region.
- must show its place (`2 of 3`), Back, Next or Done, and a close button; the last step names the info button.
- must move focus to Next or Done on open, and announce each step politely.
- may ring each step's target; the ring holds still under reduced motion.
- must count as seen the moment it opens, so a reload or a skip never brings it back.
- must not chain into another intro, return as a nag, or ask for anything
  ([product principles](../../../../../../conventions.md#product-principles)).

---

## Seen state

- must key each intro by a stable `{page}.{region}` id; changed content takes a new id.
- must store seen ids per user on the server where the app keeps per-user preferences.
- must otherwise store them through the [storage](../storage/storage.md) seam, under one versioned app key.
- must read storage that cannot be written as seen — an intro that cannot be remembered never shows.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| server preference | the user's seen ids beside their preferences | the app keeps per-user preferences |
| local-storage | the ids under one versioned key, via the storage broker | a single-user app, or no per-user store |
| memory | an in-process set behind the same seam | tests |

---

```txt
✅ <InfoPopover title="Calendar" intro="deployments.calendar" :steps>   key and intro behind one button
❌ a legend row under the calendar on every visit                      read once, shown forever
❌ the intro in a bottom sheet over the calendar it explains           the region disappears
```

---

## Neighbours

- [TourPopover](../../components/overlays/tourPopover.md) — a multi-target walk over a whole feature, not one region
- [UI copy](../../../../../../design/content/ui-copy.md) — how many words a screen carries inline
- [storage](../storage/storage.md) — the seam the seen ids persist through
- [responsive](../../../../shapes/app/responsive/responsive.md) — the phone class and its touch target
