# Props

*Last updated: 2026-09-10*

> The prop-name vocabulary every component reads by — boolean prefixes, handlers, render props, the controlled
> triad, and the two carve-outs. Prop **shape** (`readonly`, `interface`, and which access each framework
> fixes) is a [construct](../../../mla/constructs/constructs.md) rule; this doc names them.

## Vocabulary [REQUIRED]

| Kind | Prefix / shape | Examples |
|---|---|---|
| standalone boolean | `is*` · `has*` · `can*` · `show*` | `isDisabled` · `hasError` · `canResize` · `showLabel` |
| event handler | `on*` | `onClick` · `onSelect` · `onValueChange` |
| render-prop | `render*` | `renderItem` · `renderEmpty` · `renderTrigger` |

- must prefix a boolean naming visibility or display intent `show*` — it joins `is*` / `has*` / `can*`.
- must not invent a new un-prefixed boolean idiom.

---

## Inbound versus imperative

- must use `on*` for an **inbound** handler prop only — a callback passed *into* a component.
- must name a hook or view-model method the consumer **calls** with an imperative verb — `selectEmoji`,
  `clearSelection`, `setSearchKeyword` — never `on*`.
- may keep a bare verb (`clear`, `select`) inside a single-purpose component, and must disambiguate only when
  the surrounding scope makes it ambiguous.

| Do | Avoid |
|---|---|
| `onSelect` (prop) · `selectEmoji` (method you call) | `onSelectEmoji` for a method the consumer calls |
| `clearSelection` · `setSearchKeyword` | `onClearSelection` — a method dressed as a prop |

---

## Controlled state

- must select controlled mode when the model prop is not `undefined` at mount; omission selects uncontrolled mode.
- must keep that mode for the instance lifetime; changing mode requires a remount, not a silent fallback.
- must treat `null` as an explicit value only where the model contract permits clearing; it never selects mode.
- must accept either the model prop or its `default*` seed, never both for the same state axis.
- must read the seed once; later seed changes must not overwrite user edits.
- must render controlled state from the current prop; user intent requests a change without changing ownership.
- must update local state in uncontrolled mode and publish the same proposed-value notification.
- must send the proposed value as the model notification payload, not a DOM event; document any extra metadata.
- must not notify a user change merely because an external prop changes.
- must route reset through the state owner: controlled resets update the prop; uncontrolled resets restore the seed.
- must document read-only controlled usage or require a change listener for an editable surface.
- must reserve bare model roots for state axes; standalone custom flags still take `is*`, `has*`, `can*` or `show*`.
- framework spelling → [React](../../constructs/react/components.md#controlled-props) or
  [Vue](../../constructs/vue/macros.md#controlled-props).

---

## Carve-outs

- must pass a native attribute through unrenamed — a real DOM attribute (`type`, `name`, `id`, `role`) and
  every `aria-*` / `data-*` keep their exact HTML spelling, because they hit the element verbatim.
- must still take `is*` on a state flag the component owns and publishes — `isDisabled`, not `disabled`.
- must rename only a prop the component itself introduces, never one it forwards.
- must keep the recognized `asChild` idiom as spelled; native attributes and model roots have the exceptions above.

| Do | Avoid |
|---|---|
| `isDisabled` · `isInvalid` · `hasIcon` | `disabledFlag` · `invalid` · `iconBool` |
| `onChange` · `onValueChange` | `handleChange` · `changeCallback` · `onChanged` |
| `renderItem` | `itemRenderer` · `itemTemplate` |
| `{ open, defaultOpen, onOpenChange }` | `isOpen` + `defaultOpen` + `onOpenChange` |
| `aria-label` · `data-state` · native `type` | `ariaLabel` · `dataState` · `buttonType` |

```typescript
/** Defines props for the dismissible info banner. */
interface InfoBannerProps {
  readonly open?: boolean;
  readonly defaultOpen?: boolean;
  readonly onOpenChange?: (open: boolean) => void;
  readonly isDisabled?: boolean;
  readonly hasIcon?: boolean;
  readonly "aria-label"?: string;
  readonly asChild?: boolean;
}

const controlled: InfoBannerProps = { open: true, onOpenChange: (open) => console.log(open) };
const uncontrolled: InfoBannerProps = { defaultOpen: true };
// Invalid by contract: { open: true, defaultOpen: false }.
// An interface alone does not enforce this pair exclusion; validate it in the component's contract tests.
```

---

## Neighbours

- [naming](naming.md) — the file, folder and constant casing these props sit inside
- [constructs](../../../mla/constructs/constructs.md) — the prop **shape** rules: `readonly`, `interface`
