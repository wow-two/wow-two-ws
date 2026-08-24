# At-rules

*Last updated: 2026-08-23*

> Every CSS at-rule, which of them a Tailwind-only codebase still writes, and the ones a utility replaces.
> Purpose — most at-rules have a variant that does the same job in the markup, where the class can be seen.
> Use case — reach here before adding a block to a stylesheet, and whenever a rule needs a condition.

## The at-rules

Six at-rules appear across both stylesheets: `@import`, `@theme`, `@custom-variant`, `@source`, `@keyframes`, `@media`.

| At-rule | Means | Verdict |
|---|---|---|
| `@import 'tailwindcss'` | the framework, pulled in first | `use` |
| `@import` of a package stylesheet | a dependency's tokens, resolved by the bundler | `use` |
| `@import` of a remote stylesheet | a blocking request to another origin | `banned` |
| `@theme` | the token block Tailwind generates utilities from | `use` |
| `@source` | an extra path the class scanner must read | `use` |
| `@custom-variant` | a named variant, such as class-based `dark` | `use` |
| `@utility` | a first-class utility that `tailwind-merge` can resolve | `use with care` |
| `@variant` | a variant applied inside a CSS rule | `use with care` |
| `@keyframes` | an animation body — no utility form exists | `use` |
| `@media (prefers-reduced-motion: reduce)` | the reduced-motion safety net | `use` |
| `@media` for a breakpoint | a width condition a `sm:` / `lg:` variant already carries | `banned` |
| `@supports` | a feature test around a progressive enhancement | `use with care` |
| `@container` | a query against an ancestor's width rather than the viewport | `use with care` |
| `@layer` | explicit cascade ordering | `use with care` |
| `@font-face` | a self-hosted font family | `use with care` |
| `@property` | a typed custom property that can be animated | `use with care` |
| `@page` · `@counter-style` | print boxes, and list markers | `use with care` |
| `@scope` · `@starting-style` | a bounded subtree, and an entry-animation start value | `use with care` |
| `@apply` | a utility list moved out of the markup | `banned` |
| `@config` · `@plugin` | the v3 JavaScript configuration seam | `banned` |
| `@charset` · `@namespace` | encoding and XML namespace declarations | `banned` |

- must express a breakpoint as a variant in the markup, never as a `@media` block in a stylesheet.
- must define an animation body in `@keyframes` and reference it through an `--animate-*` token
  ([custom properties](custom-properties.md)).
- must keep the reduced-motion safety net global, so an untagged animation cannot slip past it.
- must reach for `@utility` over `@apply` on the terms [authoring](../tailwind/authoring.md) fixes.

---

## Banned

- **`@apply`** — reach for a `tailwind-variants` recipe or a component ([tailwind](../tailwind/tailwind.md)); it moves
  classes where `tailwind-merge` cannot see them, so a consumer's override no longer wins and the box stops being
  overridable at all.
- **`@media` for a breakpoint** — reach for `sm:` / `md:` / `lg:` ([variants](../tailwind/variants.md)); a
  breakpoint in CSS is invisible from the markup, so a reader sees no reason the box changes and edits the wrong file.
- **`@import` of a remote stylesheet** — reach for a bundled dependency; the request blocks first paint, and
  the origin has to be allowed through the CSP.
- **`@config` · `@plugin`** — reach for `@theme` and `@utility`; both re-open the v3 JavaScript config that
  CSS-first Tailwind replaced, splitting the token source across two languages.
- **`@charset` · `@namespace`** — reach for the bundler's UTF-8 default; both are legal only before any other
  rule, so a later import silently voids them.

```css
/* ✅ animation body in @keyframes, exposed as a token, honoured by the safety net */
@theme {
  --animate-fade-in: fade-in var(--duration-base) var(--ease-out);
}
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ❌ a breakpoint hidden in a stylesheet — invisible from the markup it changes */
@media (min-width: 640px) {
  .card { padding: 1.5rem; }
}
```

---

## Neighbours

- [custom properties](custom-properties.md) — what `@theme` declares
- [selectors](selectors.md) — what a rule inside these blocks may target
- [authoring](../tailwind/authoring.md) — `@theme`, `@source`, `@custom-variant`, `@utility` as Tailwind's own surface
- [styling](../../../../shapes/app/platform/styling.md) — the wiring order and the `@source` depth
