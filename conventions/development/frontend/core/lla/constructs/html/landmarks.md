# Landmarks

*Last updated: 2026-09-10*

> The sectioning elements a screen reader offers as jump targets, and the ones that offer nothing.
> Purpose — a landmark is a shortcut past the chrome; a `div` with the same classes is a wall of content.
> Use case — reach here when laying out a shell, a page frame or any region a reader should be able to skip to.

## The elements

| Element | Means | Verdict |
|---|---|---|
| `<main>` | the page's primary content — one per page | `use` |
| `<nav>` | a block of navigation links | `use` |
| `<header>` | introductory content for the page or its nearest section | `use` |
| `<footer>` | closing content for the page or its nearest section | `use` |
| `<aside>` | content tangential to what surrounds it | `use` |
| `<section>` | a thematic section; a landmark when accessibly named | `use with care` |
| `<article>` | a self-contained composition that stands alone | `use with care` |
| `<search>` | a search or filtering region | `use with care` |
| `<address>` | contact details for its nearest `<article>` or page | `use with care` |
| `aria-label` on a repeated landmark | which of several navs or regions this one is | `use` |
| `role="region"` + `aria-label` on a `<div>` | a landmark where no element fits | `use with care` |
| `role="banner"` · `role="contentinfo"` | the page header and footer, restored by hand | `use with care` |
| `<section>` with no accessible name | not exposed as an implicit region landmark | `banned` |
| a second `<main>` on one page | two answers to "where does the content start" | `banned` |
| `<div class="page">` in place of `<main>` | the skip target removed | `banned` |
| `<section>` chosen for its `padding` | sectioning used as a styling hook | `banned` |

- must give each routed page one `<main>`, holding everything that is not shell
  ([routing](../../../../shapes/app/routing/routing.md)).
- must name repeated landmarks with `aria-labelledby` or `aria-label` so their purpose is distinguishable.
- must name a section landmark with `aria-labelledby` pointing to its heading, or an explicit `aria-label`.
- must use `<div>` for a styling group; a nested heading alone does not name its enclosing section.
- must scope `<header>` / `<footer>` to their nearest section — inside `<article>` they stop being page landmarks.
- must keep the shell's landmarks in the layout component, never re-declared per page
  ([architecture](../../../../shapes/app/architecture/architecture.md)).
- must reserve `<article>` for content that still makes sense lifted out — a blog post, not a card.

---

## Banned

- **an unnamed section intended as a landmark** — add an accessible name or use `<div>`;
  an unnamed `<section>` is not implicitly a region landmark.
- **a second `<main>` on one page** — reach for `<section>`; the skip-to-content shortcut targets the first
  `<main>`, so the second becomes content no shortcut reaches.
- **`<div class="page">` where `<main>` belongs** — reach for `<main>`; a screen-reader user loses the one jump that
  skips the header and nav on every page, and re-reads the chrome on each navigation.
- **`<section>` chosen because a rule targets it** — reach for `<div>` plus a utility; sectioning changes the
  landmark list, so styling through it makes the accessibility tree a side effect of the design.

```vue
<!-- ✅ named landmarks — two navs stay distinguishable, main is the single skip target -->
<header><nav aria-label="Primary"><!-- … --></nav></header>
<main class="mx-auto max-w-6xl px-4"><slot /></main>
<footer><nav aria-label="Legal"><!-- … --></nav></footer>

<section :aria-labelledby="headingId">
  <h2 :id="headingId">Saved codes</h2>
</section>

<!-- ❌ a region with no name, and no skip target at all -->
<section class="mx-auto max-w-6xl px-4"><slot /></section>
```

---

## Neighbours

- [headings](headings.md) — what names a `<section>`
- [flow](flow.md) — the box to reach for when no landmark fits
- [interactive](interactive.md) — the links a `<nav>` holds
- [architecture](../../../../shapes/app/architecture/architecture.md) — which layer owns the shell
