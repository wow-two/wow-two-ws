# Tailwind v4

*Last updated: 2026-09-10*

> Every Tailwind utility group, the verdict on each, and the authoring at-rules that extend the framework.
> Purpose — Tailwind is the only styling layer here, so a group's verdict *is* the styling rule for that property.
> Use case — reach here before writing a class family this codebase has not written before.

## The groups

| Group | Verdict | Doc |
| --- | --- | --- |
| color | `use` — semantic tokens only | [color](color.md) |
| border | `use` | [border](border.md) |
| flexbox | `use` — the default layout tool | [flexbox](flexbox.md) |
| sizing | `use` | [sizing](sizing.md) |
| typography | `use` | [typography](typography.md) |
| position | `use` | [position](position.md) |
| spacing | `use` | [spacing](spacing.md) |
| display | `use` | [display](display.md) |
| transitions | `use` — via motion tokens | [transitions](transitions.md) |
| effects | `use` | [effects](effects.md) |
| transforms | `use` | [transforms](transforms.md) |
| interactivity | `use` | [interactivity](interactivity.md) |
| overflow | `use` | [overflow](overflow.md) |
| grid | `use` — two-dimensional layout only | [grid](grid.md) |
| z-index | `use` — semantic tiers only | [z-index](z-index.md) |
| filters | `use with care` | [filters](filters.md) |
| accessibility | `use` | [accessibility](accessibility.md) |
| box | `use` | [box](box.md) |
| tables | `use` | [tables](tables.md) |
| variants | `use` | [variants](variants.md) |
| authoring | see the doc | [authoring](authoring.md) |

---

## The rules every group inherits

- must compose classes through `cn()`, never a template literal — `tailwind-merge` resolves a consumer's override
  ([styling](../../../../shapes/app/platform/styling.md)).
- must reach for a scale step before an arbitrary value; an arbitrary value earns itself only where no step exists.
- must write the scale name, never the raw measurement — `gap-2`, not `gap-[0.5rem]`.

---

## Banned

- **the `!` important modifier** — use `cn()` ordering or a variant. The house ban covers both `!px-0` and `px-0!`;
  v4 accepts the prefix for compatibility. Important and ordinary utilities remain separate merge groups.
- **`@apply`** — reach for a `tailwind-variants` recipe or a component. It moves classes out of the markup, where
  `tailwind-merge` can no longer see them, so the box stops being overridable.
- **a template-literal class string carrying a condition** — use `cn()`; class-attribute order does not decide
  the CSS cascade when conflicting utilities remain.
- **a raw palette class** (`bg-slate-900`, `text-zinc-500`) — reach for the semantic token ([color](color.md)).

---

## Class merging

- must test a custom class family against the installed `tailwind-merge` version before promising overrides.
- must verify generated CSS separately from merge output; accepting a class string does not prove CSS emission.
- custom utilities → [authoring](authoring.md).

---

## Neighbours

- [css](../css/css.md) — the four jobs left to raw CSS
- [styling](../../../../shapes/app/platform/styling.md) — wiring, `cn()`, dark mode
