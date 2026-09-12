# Color

*Last updated: 2026-09-10*

> Every colour utility family, the token layer each must consume, and the spellings that cannot flip for dark mode.
> Purpose — a semantic token is one name resolving to two values, which is the whole of our dark-mode support.
> Use case — reach here before writing any class that names a colour.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `bg-*` · `text-*` · `border-*` | surface, foreground and edge colour | `use` |
| `ring-*` · `ring-offset-*` | the focus ring and the gap under it | `use` |
| `outline-*` | the outline colour, where a ring cannot reach | `use with care` |
| `divide-*` | the rule between siblings | `use` |
| `fill-*` · `stroke-*` | an inline SVG's paint | `use` |
| `accent-*` | a native control's accent colour | `use` |
| `caret-*` · `placeholder-*` · `decoration-*` | caret, placeholder and underline colour | `use with care` |
| `from-*` · `via-*` · `to-*` | a gradient's colour stops | `use with care` |
| a semantic token — `bg-primary`, `text-muted-foreground` | the 24-token surface that flips under `.dark` | `use` |
| a paired token — `bg-primary text-primary-foreground` | a surface with its guaranteed-readable foreground | `use` |
| a soft pair — `bg-success-soft text-success-soft-foreground` | the low-emphasis form of a severity | `use` |
| an alpha modifier — `bg-muted/40`, `text-foreground/70` | a token at partial opacity | `use` |
| `bg-transparent` · `text-current` · `text-inherit` | the keyword colours | `use` |
| `bg-black/45` · `text-white/60` over media | a scrim that must not flip with the theme | `use with care` |
| a raw scale — `bg-brand-500`, `text-accent-300` | a specific shade, behind the semantic layer | `use with care` |
| a stock palette class — `bg-slate-900`, `text-zinc-500` | a colour outside the theme entirely | `banned` |
| `bg-white` · `text-black` on a themed surface | a colour that is wrong in one of the two themes | `banned` |
| an arbitrary colour — `bg-[#7c3aed]` | a literal with no token behind it | `banned` |
| a foreground not paired with its surface | contrast left to chance | `banned` |

- must reach for a semantic token first, a raw scale only when a specific shade is the point.
- must pair every surface token with its `-foreground` partner, and never mix pairs across roles.
- must express a tint through the alpha modifier — `bg-primary/10` — rather than a lighter palette step.
- must let `.dark` do the flipping; a class that names light or dark explicitly is a token that is missing.
- must reserve `text-white` / `bg-black` for a scrim over media, where the surface below is not themed.
- must declare a new colour as a token before using it ([custom properties](../css/custom-properties.md)).

---

## Banned

- **a stock palette class on themed chrome** — use the semantic token; literal color content such as a swatch
  follows its component contract rather than the surrounding surface theme.
- **`bg-white` · `text-black` on a themed surface** — reach for `bg-background` / `text-foreground`; both are fixed
  values, so the surface stops tracking the theme while everything around it moves.
- **an arbitrary colour** — reach for a token in `@theme`; the literal is invisible to a theme audit, and an app
  overriding the token leaves this one box behind.
- **a foreground with no matching surface** — reach for the pair; contrast was measured per pair, so mixing
  `text-primary-foreground` onto `bg-muted` lands outside the ratios the tokens were tuned to.

```vue
<!-- ✅ paired tokens, tint through alpha, focus ring on its own token -->
<span class="bg-success-soft text-success-soft-foreground ring-ring">Published</span>
<div class="bg-primary/10 text-primary">7 pending</div>

<!-- ❌ stock palette: correct in light, unreadable in dark, and invisible to a theme override -->
<span class="bg-slate-100 text-slate-900">Published</span>
```

---

## Neighbours

- [border](border.md) — where `ring-*` and `border-*` sit in the focus recipe
- [effects](effects.md) · [filters](filters.md) — opacity, shadow and the backdrop washes
- [custom properties](../css/custom-properties.md) — where a token is declared and re-pointed
- [styling](../../../../shapes/app/platform/styling.md) — dark mode, `cn()`, and app-level overrides
