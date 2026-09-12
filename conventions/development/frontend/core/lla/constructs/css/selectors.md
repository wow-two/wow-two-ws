# Selectors

*Last updated: 2026-09-10*

> Every selector form, the few a Tailwind-only codebase still writes, and the ones that start a specificity war.
> Purpose — a selector reaches a box the markup cannot name; every other reach belongs in the class attribute.
> Use case — reach here before writing a rule in a stylesheet, or a bracket selector inside a class.

## The selectors

| Selector | Means | Verdict |
|---|---|---|
| type — `html` · `body` | the global reset's two targets | `use` |
| class — `.dark` | the theme switch every semantic token hangs off | `use` |
| class — `.prose` | the scope styling HTML an author wrote, not a component | `use` |
| descendant inside `.prose` — `.prose h2` | authored content the component tree never sees | `use` |
| universal `*` with `::before` / `::after` | the reduced-motion safety net's reach | `use` |
| `:where()` | a match that adds no specificity | `use` |
| pseudo-class — `:hover` · `:focus-visible` | a state a variant already carries in the markup | `banned` |
| pseudo-element — `::marker` · `::placeholder` | a generated part inside authored content | `use with care` |
| vendor pseudo-element — `::-webkit-slider-thumb` | a native control's shadow part | `use with care` |
| bracket selector in a class — `[&>*]:` | a child a component owns but cannot class | `use with care` |
| `:has()` | a parent matched by its descendants | `use with care` |
| attribute — `[data-state='open']` | component state, better written as a `data-[…]` variant | `use with care` |
| `:is()` · `:not()` | a grouped match, and a negated one | `use with care` |
| id — `#panel` | one element, at specificity nothing overrides | `banned` |
| a class targeting a component's internals | reach across a component boundary | `banned` |
| element selector outside the reset or `.prose` | every instance of a tag, app-wide | `banned` |
| `!important` | a declaration that outranks the cascade | `banned` |

- must keep every stylesheet rule inside the four jobs raw CSS still owns ([css](css.md)).
- must reach for a variant in the markup before a pseudo-class in CSS ([variants](../tailwind/variants.md)).
- must wrap a theme or scope selector in `:where()` so an app's own rule still wins.
- must use a bracket selector only for a generated child — a list marker, a slider thumb.
- must keep the `!important` exception to the reduced-motion safety net, and nowhere else.

---

## Banned

- **an id selector** — reach for a class or a `data-*` attribute; an id outranks every class, so the only way to
  override it later is a second id or `!important`, and both spread.
- **a rule targeting another component's internals** — reach for a prop or a slot
  ([constructs](../../../mla/constructs/constructs.md)); the internal structure is not a contract, so the rule
  breaks on a refactor with no compile error anywhere.
- **an element selector outside the reset and `.prose`** — reach for a utility; `button { … }` reaches every
  button in the app including the library's, and it cannot be overridden from the markup.
- **`!important`** — use the normal cascade or a variant; a class merger does not rewrite stylesheet declarations.
  Important utilities use separate merge groups ([Tailwind](../tailwind/tailwind.md)).
- **a pseudo-class in a stylesheet** — reach for `hover:` / `focus-visible:` / `disabled:`; a state defined away from
  the markup leaves the class string looking complete while the box behaves otherwise.

```css
/* ✅ scoped to authored content, zero added specificity, marker styled where no class can go */
.prose li::marker {
  color: var(--color-muted-foreground);
}

/* ❌ an id and an important: nothing in the markup can override either */
#panel {
  padding: 1rem !important;
}
```

---

## Neighbours

- [at-rules](at-rules.md) — the blocks these rules live in
- [values](values.md) — what a matched declaration is allowed to hold
- [variants](../tailwind/variants.md) — the state and child selectors written in the markup instead
- [css](css.md) — the four jobs raw CSS keeps
