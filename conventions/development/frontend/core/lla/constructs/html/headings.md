# Headings

*Last updated: 2026-09-10*

> The six heading elements, the outline they build, and the shapes that build no outline at all.
> Purpose — headings are how a screen-reader user navigates a page; a wrong level is a wrong map.
> Use case — reach here before adding a section title, and whenever a component must title itself.

## The elements

| Element | Means | Verdict |
|---|---|---|
| `<h1>` | the page's single subject | `use` |
| `<h2>` | a top-level section of that page | `use` |
| `<h3>` | a subsection of an `<h2>` | `use` |
| `<h4>` · `<h5>` · `<h6>` | deeper nesting, rarely earned | `use with care` |
| a heading level taken from a prop | the level a component's placement decides | `use with care` |
| `<hgroup>` | a heading with its subtitle attached | `use with care` |
| a heading inside `<section>` / `<article>` | content structure; explicit naming is separate | `use` |
| a visually hidden heading (`sr-only`) | structure for the outline that the design does not show | `use` |
| a `<div>` or `<p>` styled to look like a heading | a title outside the outline | `banned` |
| `role="heading" aria-level` on a `<div>` | a heading rebuilt out of a meaningless box | `banned` |
| a level chosen for its font size | an outline that follows the type scale | `banned` |
| more than one `<h1>` per routed page | two competing page subjects | `banned` |
| a skipped level (`<h2>` → `<h4>`) | a gap the outline reads as a missing section | `banned` |

- must give each routed page exactly one `<h1>` naming its subject
  ([routing](../../../../shapes/app/routing/routing.md)).
- must descend one level at a time — the next heading is one deeper, the same, or shallower.
- must pick the level from the section's depth, then size it with a utility
  ([typography](../tailwind/typography.md)).
- section naming → [landmarks](landmarks.md); nesting a heading does not assign the section an accessible name.
- must take the level from a prop when a component renders at more than one depth.

---

## Banned

- **a `<div>` or `<p>` styled to look like a heading** — reach for the real element; it never enters the heading list,
  so a screen-reader user jumping heading-to-heading skips the section entirely.
- **`role="heading" aria-level="2"` on a `<div>`** — reach for `<h2>`; the role restores the announcement but two
  attributes now have to agree with the surrounding depth, and neither moves when the section does.
- **a level chosen for its font size** — reach for the level the depth dictates plus a `text-*` utility; sizing
  through the tag couples the outline to the type scale, so a design tweak silently rewrites the structure.
- **a second `<h1>` on one routed page** — reach for `<h2>`; two page subjects leave assistive technology with no
  single answer to "what is this page".
- **a skipped level** — reach for the next level down; the gap is announced as a missing section, and a reader assumes
  content failed to load.

```vue
<!-- ✅ depth picks the tag, the utility picks the size; the component takes its level from its placement -->
<h2 class="text-lg font-semibold text-foreground">Saved codes</h2>
<component :is="HeadingTag[props.level]" class="text-sm font-medium">{{ props.title }}</component>

<!-- ❌ the tag chosen for its size — the outline now tracks the type scale -->
<h4 class="text-lg font-semibold text-foreground">Saved codes</h4>
```

---

## Neighbours

- [landmarks](landmarks.md) — the regions these headings name
- [text](text.md) — the prose a heading opens
- [typography](../tailwind/typography.md) — the size, weight and tracking utilities
- [constructs](../../../mla/constructs/constructs.md) — where a level prop is declared
- [accessibility](../tailwind/accessibility.md) — `sr-only`, for a heading the design does not show
