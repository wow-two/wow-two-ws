# Authoring

*Last updated: 2026-09-10*

> The at-rules Tailwind adds to CSS for extending itself, and the ones that reopen the configuration it replaced.
> Purpose — these five are the whole seam between our theme and the framework, so what goes through them is the API.
> Use case — reach here when adding a token, a variant, a scanned path or a utility of our own.

## The at-rules

| At-rule | Declares | Verdict |
|---|---|---|
| `@import 'tailwindcss'` | the framework, first line of the stylesheet | `use` |
| `@import '@wow-two-beta/ui/styles.css'` | the library's tokens, before any override | `use` |
| `@theme` | the token block every utility is generated from | `use` |
| `@theme inline` | tokens emitted without their variable indirection | `use with care` |
| `@source` | an extra path the class scanner must read | `use` |
| `@source not` | a path excluded from scanning | `use with care` |
| `@custom-variant` | a named variant — this is where `dark` is defined | `use` |
| `@utility` | a generated utility; merging needs a separate contract | `use with care` |
| `@variant` | an existing variant applied inside a CSS rule | `use with care` |
| `@keyframes` + an `--animate-*` token | an animation body and its handle | `use` |
| `@reference` | the theme pulled into a separate stylesheet for `@apply` | `banned` |
| `@apply` | a utility list moved out of the markup | `banned` |
| `@config` | a v3 JavaScript config file | `banned` |
| `@plugin` | a JavaScript plugin registered from CSS | `banned` |
| `tailwind.config.js` | the v3 configuration surface | `banned` |
| a component-local `@theme` block | duplicated global token ownership | `banned` |

- must add a token to `@theme` rather than a utility, whenever the new thing is a value
  ([custom properties](../css/custom-properties.md)).
- must reserve `@utility` for a new property shorthand, not a bundle of existing utilities.
- must configure and test the merger's class groups for an overridable custom utility; `@utility` does not do this.
- must define a variant with `@custom-variant` when it is used in more than one component.
- stylesheet placement → [CSS](../css/css.md) § *The four jobs*.

---

## Banned

- **`@apply`** — reach for a `tailwind-variants` recipe or a component; it moves classes where `tailwind-merge` cannot
  see them, so a consumer's `class` no longer overrides and the box stops being themeable from the outside.
- **`@reference`** — reach for one stylesheet; it exists to make `@apply` work in a second file, so adopting it means
  adopting the ban above along with a second place tokens are resolved.
- **`@config` · `@plugin` · `tailwind.config.js`** — reach for `@theme` and `@utility`; the v3 seam splits the token
  source across CSS and JavaScript, and the two are merged by the build rather than by anything a reader can see.
- **a component-local `@theme` block** — use the deliverable's stylesheet entry, linked from [CSS](../css/css.md).

```css
/* ✅ the whole seam: framework, library tokens, scan path, variant, overrides */
@import 'tailwindcss';
@import '@wow-two-beta/ui/styles.css';
@source '../../node_modules/@wow-two-beta/ui/dist';
@custom-variant dark (&:where(.dark, .dark *));
@theme {
  --color-primary: #7c3aed;
}

/* ❌ classes hoisted out of the markup — no consumer override reaches them again */
.btn-primary {
  @apply rounded-md bg-primary px-3 py-2 text-primary-foreground;
}
```

---

## Neighbours

- [at-rules](../css/at-rules.md) — the plain-CSS at-rules these sit beside
- [custom properties](../css/custom-properties.md) — what `@theme` declares
- [variants](variants.md) — what `@custom-variant` produces
- [styling](../../../../shapes/app/platform/styling.md) — the wiring order and the `@source` depth
