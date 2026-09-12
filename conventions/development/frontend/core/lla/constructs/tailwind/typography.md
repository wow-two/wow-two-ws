# Typography

*Last updated: 2026-09-10*

> Every type utility — size, weight, family, alignment, wrapping — and the spellings a translation breaks.
> Purpose — the type scale is a fixed set of steps, and a size outside it is a design decision made in passing.
> Use case — reach here before sizing, weighting or truncating text.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `text-xs` … `text-5xl` | the size scale, each step with its own line height | `use` |
| `font-normal` · `font-medium` · `font-semibold` · `font-bold` | the weight scale | `use` |
| `font-sans` · `font-mono` | the family tokens | `use` |
| `leading-none` · `leading-tight` · `leading-relaxed` | line height overriding the size step's default | `use` |
| `tracking-tight` · `tracking-normal` · `tracking-wide` | letter spacing | `use` |
| `text-left` · `text-center` · `text-right` | alignment | `use` |
| `text-start` · `text-end` | alignment that follows the writing direction | `use` |
| `italic` · `not-italic` | slant | `use` |
| `uppercase` · `lowercase` · `capitalize` · `normal-case` | letter casing, applied visually | `use with care` |
| `underline` · `line-through` · `no-underline` · `underline-offset-*` | decoration | `use` |
| `truncate` | one line, clipped with an ellipsis | `use` |
| `text-ellipsis` · `text-clip` with `line-clamp-*` | a clamp across several lines | `use` |
| `whitespace-nowrap` · `whitespace-pre` · `whitespace-pre-wrap` | how whitespace and breaks are kept | `use` |
| `break-words` · `break-all` · `text-wrap` · `text-balance` | where a long run may break | `use with care` |
| `tabular-nums` · `ordinal` · `slashed-zero` | font features, for numbers that must not jitter | `use` |
| `list-none` · `list-disc` · `list-decimal` · `list-inside` | list markers ([lists](../html/lists.md)) | `use` |
| `indent-*` · `align-middle` · `align-baseline` | first-line indent, and inline alignment | `use with care` |
| an arbitrary size — `text-[10px]`, `text-[11px]` | a step below the scale's floor | `use with care` |
| `antialiased` · `subpixel-antialiased` | font smoothing | `use with care` |
| `uppercase` as the only way a label reads as a label | casing carrying meaning | `banned` |
| `truncate` on a flex child with no `min-w-0` | an ellipsis that never appears | `banned` |
| a raw font stack — `font-['Geist']` | a family outside the token | `banned` |
| `whitespace-nowrap` on user-supplied text | a string that cannot wrap and so overflows | `banned` |

- must take the size from the scale, and reach for `text-[10px]` only where a dense control leaves nothing smaller.
- must reach for `tabular-nums` on any number that updates in place — a timer, a counter, a price.
- must pair `truncate` with `min-w-0` on a flex child ([sizing](sizing.md)).
- must declare a family as a `--font-*` token, then consume it as `font-sans` / `font-mono`
  ([custom properties](../css/custom-properties.md)).
- must style authored article prose through the `.prose` scope, not per-run utilities ([css](../css/css.md)).
- must keep `uppercase` decorative — the readable label stays in the markup.

---

## Banned

- **`uppercase` carrying the meaning** — reach for the words themselves; the utility changes only the rendering, so a
  screen reader announces the original casing and the label the user hears is not the one on screen.
- **`truncate` on a flex child with no `min-w-0`** — reach for `min-w-0`; the item's default minimum is its content
  width, so the ellipsis never appears and the row overflows instead.
- **a raw font stack** — reach for the `--font-*` token; a stack written in a class is invisible to an app overriding
  the family, so one component keeps the SDK's font after a rebrand.
- **`whitespace-nowrap` on user-supplied text** — reach for `truncate`; a long unbroken string forces its container
  wider than the viewport, adding a horizontal scrollbar to the whole page.

```vue
<!-- ✅ scale step, tabular figures for a value that updates, truncation wired to shrink -->
<span class="min-w-0 truncate text-sm font-medium">{{ file.name }}</span>
<span class="text-xs tabular-nums text-muted-foreground">{{ elapsed }}</span>

<!-- ❌ nowrap on user text — one long name widens the page -->
<span class="whitespace-nowrap text-sm">{{ file.name }}</span>
```

---

## Neighbours

- [color](color.md) — the foreground tokens these sizes are painted in
- [flexbox](flexbox.md) · [overflow](overflow.md) — what makes `truncate` work
- [text](../html/text.md) — the elements carrying the meaning behind the weight
- [custom properties](../css/custom-properties.md) — where `--font-*` is declared
