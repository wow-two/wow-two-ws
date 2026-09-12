# Custom properties

*Last updated: 2026-09-10*

> Every kind of `--*` declaration, where each is allowed to live, and the ones that leave a value with two owners.
> Purpose — a custom property is the only value in the codebase both CSS and a utility class can read.
> Use case — reach here before declaring a token, overriding one for dark mode, or setting one from script.

## The declarations

- token declaration ownership → [CSS](css.md) § *The four jobs*.

| Declaration | Means | Verdict |
|---|---|---|
| `--color-*` in `@theme` | a colour token, and the `bg-` / `text-` / `border-` utilities it generates | `use` |
| `--radius-*` · `--font-*` in `@theme` | the corner and family scales | `use` |
| `--duration-*` · `--ease-*` · `--animate-*` in `@theme` | the motion scale and its named animations | `use` |
| `--z-index-*` in `@theme` | the semantic stacking tiers | `use` |
| a raw scale (`--color-brand-500`) in `@theme` | a full palette kept behind the semantic layer | `use with care` |
| a semantic token re-pointed in `.dark` | the same name resolving to a different value per theme | `use` |
| a raw scale re-pointed in `.dark` | a palette whose numbers stop meaning their shade | `banned` |
| a token overridden in a consuming app's `@theme` | an app's brand replacing a default | `use` |
| `--*` declared on `:root` outside `@theme` | a variable no utility is generated from | `banned` |
| `--*` declared on a component's own element | a value scoped to one subtree | `use with care` |
| `--*` set through an inline `style` binding | a runtime measurement CSS cannot compute | `use with care` |
| `var(--token)` read inside a utility | a token consumed as `bg-(--token)` or `text-(--token)` | `use` |
| `var(--token, fallback)` | a value with a default when the token is unset | `use with care` |
| a hex or `rgb()` literal in a component | a colour with no token behind it | `banned` |
| a token named for its value (`--color-blue-600`) | a name that lies once the theme changes | `banned` |
| `@property` | a typed, animatable custom property | `use with care` |

- must declare utility-generating theme tokens in `@theme`; stylesheet placement belongs to [CSS](css.md).
- must name a token for its role — `--color-primary`, `--color-muted-foreground` — never for the colour it holds.
- must re-point only the semantic layer in `.dark`, leaving the raw scales fixed.
- must consume a token through the utility Tailwind generates from it, not through `var()` in a `style` attribute.
- must reach for an inline `--*` only for a value measured at runtime, such as an anchor's width.
- must let a consuming app override a token by re-declaring the same name
  ([styling](../../../../shapes/app/platform/styling.md)).

---

## Banned

- **`--*` declared on `:root` outside `@theme`** — reach for `@theme`; Tailwind v4 generates utilities only from
  `@theme`, so a `:root` variable produces no `bg-*` class and every use site falls back to arbitrary values.
- **a raw scale re-pointed under `.dark`** — reach for a semantic token; `--color-brand-500` naming one shade in light
  and another in dark makes every numeric reference in the codebase ambiguous.
- **a hex or `rgb()` literal inside a component** — reach for the semantic token ([color](../tailwind/color.md)); a
  literal cannot flip for dark mode, so the component is correct in exactly one theme.
- **a token named after its value** — reach for a role name; `--color-blue-600` re-pointed to violet by an app leaves
  every reader believing the wrong thing, and renaming it later touches every consumer.

```css
/* ✅ role-named token in @theme, re-pointed for dark — the utility flips with it */
@theme {
  --color-primary: #7c3aed;
}
.dark {
  --color-primary: #8b5cf6;
}

/* ❌ outside @theme: no bg-brand utility is generated, and the literal never flips */
:root {
  --brand: #7c3aed;
}
```

---

## Neighbours

- [at-rules](at-rules.md) — `@theme`, and the wiring order it sits in
- [values](values.md) — `var()`, `color-mix()` and what reads a token
- [color](../tailwind/color.md) — the semantic token set as utilities
- [styling](../../../../shapes/app/platform/styling.md) — how an app overrides the defaults
