# Sizing

*Last updated: 2026-09-10*

> Every width, height and constraint utility, and the sizes that break a mobile viewport or a flex row.
> Purpose — a size is where a layout stops being fluid, so each fixed one has to earn itself.
> Use case — reach here before pinning a dimension, and whenever something must fill or must not grow.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `w-*` · `h-*` | width and height from the spacing scale | `use` |
| `size-*` | both axes at once — the icon and avatar form | `use` |
| `w-full` · `h-full` | the parent's full measure | `use` |
| `w-auto` · `h-auto` | back to the content's own size | `use` |
| `w-px` · `h-px` | a one-pixel rule or hairline | `use` |
| `w-1/2` · `w-1/3` · `w-2/3` | a fraction of the parent | `use with care` |
| `min-w-0` · `min-h-0` | a flex or grid child allowed to shrink | `use` |

- must add `min-w-0` to a flex or grid child whose content must truncate — its default minimum is its content,
  so `truncate` never engages without it.
| `min-w-*` · `min-h-*` | a floor the content cannot go below | `use` |
| `max-w-*` · `max-h-*` | a ceiling — including the `max-w-{size}` prose measures | `use` |
| `max-w-full` | a child that cannot exceed its parent | `use` |
| `min-h-svh` · `min-h-dvh` | full viewport height that survives a mobile toolbar | `use` |
| `min-h-screen` · `h-screen` | `100vh`, which a mobile toolbar overshoots | `use with care` |
| `basis-*` | a flex item's starting size ([flexbox](flexbox.md)) | `use with care` |
| `size-[1em]` | an icon tracking its own font size | `use with care` |
| an arbitrary viewport size — `max-h-[60vh]` | a ceiling relative to the viewport | `use with care` |
| `w-(--anchor-width)` | a size measured at runtime and passed as a property | `use` |
| an arbitrary rem width — `w-[20rem]`, `min-w-[14rem]` | a measurement outside the scale | `use with care` |
| a fixed `w-*` on a text container | a box that cannot fit a longer translation | `banned` |
| `h-*` on a container of flowing text | a height clipping or leaking its own content | `banned` |
| `w-screen` inside a scrollable page | a width that includes the scrollbar | `banned` |

- must reach for `size-*` when both axes match, which is every icon and every avatar.
- must size a container with `max-w-*` and a `min-w-*` floor rather than a fixed `w-*`.
- must let text set its own height, and bound the box with `max-h-*` plus an overflow rule ([overflow](overflow.md)).
- must prefer a token over an arbitrary size where the measure comes from runtime.

---

## Banned

- **a fixed `w-*` on a text container** — reach for `max-w-*` with `min-w-0`; a longer translation or a long
  word overflows a fixed box, so the same class clips content in one locale and not another.
- **`h-*` on a container of flowing text** — reach for `min-h-*`; a fixed height clips the last line at a larger
  font size and leaves a gap at a smaller one, and the user's font setting decides which.
- **`w-screen` inside a scrollable page** — reach for `w-full`; `100vw` includes the vertical scrollbar, so the
  element is wider than its own container and adds a horizontal scrollbar.

```vue
<!-- ✅ bounded rather than fixed; icon sized on both axes at once -->
<div class="min-w-0 max-w-md">
  <IconFile aria-hidden="true" class="size-4 shrink-0" />
  <p class="truncate">{{ file.name }}</p>
</div>

<!-- ❌ a fixed width and height: clips a longer translation, and clips a larger font -->
<div class="h-10 w-64">
  <p>{{ file.name }}</p>
</div>
```

---

## Neighbours

- [flexbox](flexbox.md) · [grid](grid.md) — the parents that decide what a size means
- [spacing](spacing.md) — the same scale, applied as gaps and padding
- [overflow](overflow.md) — what a bounded box does with content that exceeds it
- [box](box.md) — `aspect-*` and `object-*`, the ratio-first way to size media
- [values](../css/values.md) — the units a size is written in, `svh` / `dvh` among them
