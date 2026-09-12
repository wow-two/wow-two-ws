# Action

*Last updated: 2026-09-10*

> A trigger that runs a command and carries no value of its own.
> Purpose — separating "do this" from "set this" keeps a control's model contract out of every button.
> Use case — submit, copy, delete, open a menu, toggle a mode, fire an app command.

## Gate

- must trigger a command; the caller owns its product effect.
- must use a real button for a command and preserve keyboard behavior when composition replaces the element.
- must use [nav](nav.md) for a destination and [control](control.md) for an editable selected value.
- may keep transient interaction feedback such as copied or expanded state without becoming the value owner.

---

## Location

### Group

- must use the `actions/` group for command triggers and command strips; editable selection groups are controls.
- must live with its owner when it exists only inside one component — a compound `Root.Trigger`.

```txt
✅ presentation/actions/copyButton/{CopyButton.vue, CopyButton.spec.md, index.ts}
❌ presentation/actions/saveCodeButton/       (a product command, not a generic action)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must state the affordance, never the command a product wires to it.

### Construct

- must expose `asChild` where a caller needs a router link or a custom element in its place.
- must declare style axes as `variant × tone × size`, resolved from tokens
  ([styling](../../../../shapes/app/platform/styling.md)).

### Component name

- must end `*Button` — an action carries no value, so the button word is the whole role.
- must admit `*Group` for a grouped strip and `*Bar` for a fixed one — `Toolbar` — all shape words ([visual
  kinds](visual.md) § *Shape words*).
- must name the affordance — `CopyButton`, never `CopyToClipboardHandlerButton`.

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must carry `isDisabled` and `isLoading` as separate props — a busy action is not a forbidden one.
- must take the label as a slot, and keep any text prop for the loading swap only.

### Slots

- must expose `leading`, `default`, and `trailing` so an icon or a count rides beside the label.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must let the native `click` through rather than re-emitting it under another name.
- must emit the outcome when the action owns one — `copied`, `expanded`.

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- must keep a button's label content free of nested interactive controls.
- may compose buttons inside a command strip without making the strip itself a button.
- must coordinate an opened overlay as a sibling or compound surface, not a descendant of the native button.

---

## Neighbours

- [actions](../../components/actions/actions.md) — which one to reach for, and with what values
- [control](control.md) — the kind for a widget that owns a value
- [nav](nav.md) — the kind for a trigger that moves rather than runs
- [overlay](overlay.md) — the surface an action opens
- [visual kinds](visual.md) — every other kind, and the composition contract
