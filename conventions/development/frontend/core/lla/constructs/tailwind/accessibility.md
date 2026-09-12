# Accessibility

*Last updated: 2026-09-10*

> The utilities that change what a screen reader gets rather than what the screen shows, and their misuses.
> Purpose — these are the only utilities whose whole effect is invisible, so a wrong one is never caught by looking.
> Use case — reach here whenever text must exist for a reader and not for the eye, or the reverse.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `sr-only` | text kept in the tree, clipped to a pixel on screen | `use` |
| `not-sr-only` | that text revealed again, usually at a breakpoint | `use` |
| `focus:not-sr-only` | a skip link that appears when tabbed to | `use` |
| `sr-only` on an icon-only control's label | the accessible name, as visible text | `use with care` |
| `sr-only` on a live region | a status announced but not shown | `use` |
| `forced-color-adjust-auto` | colours handed over to the user's forced-colors palette | `use` |
| `forced-color-adjust-none` | our colours kept in forced-colors mode | `use with care` |
| `forced-colors:` variant | a rule that only applies in forced-colors mode | `use` |
| `motion-safe:` · `motion-reduce:` | motion gated on the user's preference ([variants](variants.md)) | `use` |
| `sr-only` used to hide from everyone | text a reader still announces | `banned` |
| `sr-only` on an interactive element with no focus reveal | a control that takes focus invisibly | `banned` |
| `sr-only` text duplicating a visible label | the same name announced twice | `banned` |
| `hidden` on a live region | an announcement that never fires ([display](display.md)) | `banned` |

- must reach for `sr-only` when a reader needs text the design does not show, and `hidden` when nobody needs it.
- must pair `sr-only` on anything focusable with `focus:not-sr-only`, so a keyboard user can see where they are.
- must prefer `aria-label` on an icon-only control, and `sr-only` where a real text node reads better
  ([global attributes](../html/global-attributes.md)).
- must leave a live region rendered and announce through mutation, never through mounting it
  ([display](display.md)).
- must keep `forced-color-adjust-none` to a swatch or a brand mark, where the colour *is* the content.
- must check a `sr-only` string against the visible one — the two must not both be announced.

---

## Banned

- **`sr-only` used to hide from everyone** — reach for `hidden`; `sr-only` clips the box to a pixel but leaves it in
  the accessibility tree, so a screen-reader user hears content no sighted user can see, including stale text.
- **`sr-only` on a focusable element with no reveal** — reach for `focus:not-sr-only`; the element still takes focus,
  so a keyboard user tabs to a one-pixel box and the page appears to lose focus entirely.
- **`sr-only` text duplicating a visible label** — reach for one or the other; the reader announces both, so a button
  reading "Delete" is heard as "Delete Delete".
- **`hidden` on a live region** — reach for `sr-only` ([display](display.md)); `display: none` removes the region from
  the tree, so the mutation that should trigger the announcement lands on nothing.

```vue
<!-- ✅ named once, revealed on focus, and a live region that stays in the tree -->
<a href="#main" class="sr-only focus:not-sr-only">Skip to content</a>
<button type="button"><IconTrash aria-hidden="true" class="size-4" /><span class="sr-only">Delete</span></button>
<p role="status" class="sr-only">{{ savedCount }} codes saved</p>

<!-- ❌ announced twice, and a status region that never announces at all -->
<button type="button"><span class="sr-only">Delete</span>Delete</button>
<p role="status" class="hidden">{{ savedCount }} codes saved</p>
```

---

## Neighbours

- [display](display.md) — `hidden`, and why it is not interchangeable with `sr-only`
- [global attributes](../html/global-attributes.md) — `aria-label`, `aria-hidden`, `role`
- [variants](variants.md) — `focus:`, `forced-colors:`, `motion-reduce:`
- [interactive](../html/interactive.md) — the icon-only controls that need a name

---

## Verification

- must verify keyboard focus order, visible focus, activation and escape/dismissal without a pointer.
- must verify focus in forced colors; shadow-based indicators need the [outline fallback](border.md).
- must verify reduced motion removes nonessential movement without removing state feedback.
- must verify text contrast and control boundaries in light and dark themes.
- must verify zoom and reflow with long labels, validation messages and translated content.
- must verify RTL reading order, logical spacing and directional interaction where supported.
- must verify accessible names, roles, states and live announcements with assistive technology on affected interactions.
- must not treat a passing automated accessibility scan as proof of keyboard or announcement correctness.
- matrix and evidence ownership → [library testing](../../../../shapes/library/testing/testing.md).
