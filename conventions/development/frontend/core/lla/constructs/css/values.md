# Values

*Last updated: 2026-09-10*

> Every value form a declaration may hold — functions, colours, units — and the ones with no token behind them.
> Purpose — a value is where a hard-coded number enters the codebase, and where the theme stops applying.
> Use case — reach here before typing a number or a colour into CSS or into an arbitrary utility value.

## The values

| Value | Means | Verdict |
|---|---|---|
| `var(--token)` | a token read back out | `use` |
| `var(--token, fallback)` | a token with a default when unset | `use with care` |
| `calc()` | arithmetic across units | `use with care` |
| `color-mix(in srgb, …)` | a token blended toward another colour or transparency | `use` |
| `linear-gradient()` · `radial-gradient()` | an ambient surface wash | `use with care` |
| `cubic-bezier()` | an easing curve, declared once as an `--ease-*` token | `use` |
| `rgb(r g b / a)` | the space-separated colour form with alpha | `use with care` |
| a hex literal in `@theme` | the raw value a token resolves to | `use` |
| a hex literal in a component | a colour outside the theme | `banned` |
| `rem` · `em` | type-relative length — the scale's own unit | `use` |
| `px` | a device pixel, for a hairline or a border | `use with care` |
| `%` · `fr` · `ch` | a fraction of the parent, the track, the character | `use with care` |
| `svh` · `dvh` · `lvh` | viewport height that survives a mobile toolbar | `use` |
| `vh` | viewport height that a mobile toolbar breaks | `use with care` |
| `ms` · `s` | duration, declared once as a `--duration-*` token | `use` |
| `deg` · `turn` | rotation | `use` |
| `0` unitless | zero, which needs no unit | `use` |
| `transparent` · `currentColor` · `inherit` | the keyword colours | `use` |
| an arbitrary utility value — `text-[10px]` | a value the scale does not offer | `use with care` |
| an arbitrary value duplicating a scale step | a second spelling of an existing token | `banned` |
| a raw duration or easing in a utility | motion outside the motion scale | `banned` |
| `!important` in a value position | a declaration that outranks the cascade | `banned` |

- must express a colour as a token, and blend it with `color-mix()` or a `/` alpha, never a new literal.
- must declare a duration or easing once as a token, then consume it as `duration-(--duration-base)`.
- must reach for `svh` / `dvh` over `vh` for anything sized against the viewport on mobile.
- must keep a hex literal inside `@theme` ([custom properties](custom-properties.md)).
- must not add a scale step for one use ([tailwind](../tailwind/tailwind.md)).

---

## Banned

- **a hex or named colour inside a component** — reach for the semantic token ([color](../tailwind/color.md)); a
  literal cannot re-point under `.dark`, so the component renders correctly in exactly one theme.
- **an arbitrary value duplicating a scale step** — use the scale spelling; a literal does not follow a changed
  token even when the merger correctly resolves its utility group.
- **a raw duration or easing in a utility** — reach for the motion tokens
  ([transitions](../tailwind/transitions.md)); a hand-typed `300ms` drifts from the scale and is not covered by the
  reduced-motion safety net's token-based reasoning.
- **`!important`** — follow [selectors](selectors.md) § *The selectors*.

```css
/* ✅ tokens all the way down — the blend and the easing both flip with the theme */
.surface-glow {
  background-image: radial-gradient(135% 135% at 100% 112%,
    color-mix(in srgb, var(--color-primary) 14%, transparent), transparent 52%);
}

/* ❌ a literal that cannot re-point for dark mode, and a duration outside the scale */
.panel {
  background: #7c3aed;
  transition: opacity 240ms ease-in;
}
```

---

## Neighbours

- [custom properties](custom-properties.md) — where a literal is allowed to live
- [at-rules](at-rules.md) · [selectors](selectors.md) — the blocks and targets these values sit in
- [color](../tailwind/color.md) · [spacing](../tailwind/spacing.md) — the scales these values should already be
- [transitions](../tailwind/transitions.md) — the motion tokens
