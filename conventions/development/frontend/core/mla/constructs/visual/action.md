# Action

*Last updated: 2026-08-23*

> A trigger that runs a command and carries no value of its own.
> Purpose — separating "do this" from "set this" keeps a control's model contract out of every button.
> Use case — submit, copy, delete, open a menu, toggle a mode, fire an app command.

## Gate

- must **carry no value** — a component whose output is read back is a [control](control.md).
- must be operable by keyboard as a button, with a real `<button>` unless `asChild` swaps it.
- must not navigate to a place — a destination trigger is a [nav](nav.md).
- must stay indifferent to what the command does; the caller owns the effect.

```txt
✅ Button · CopyButton · FabButton · SpeedDialButton · Toolbar · DisclosureButton · ToggleButton
❌ Switch                   (its on/off state is the value — a control)
```

---

## Location

### Group

- must live in `presentation/actions/` in the SDK, grouped strips included — `ButtonGroup`, `SegmentedControl`.
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

```vue
<script setup lang="ts">
/** Renders a clipboard-copy button with a copied-state swap. */
defineOptions({ name: 'CopyButton', inheritAttrs: false });
</script>
```

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

```vue
<script setup lang="ts">
defineProps<{ isDisabled?: boolean; isLoading?: boolean; loadingText?: string }>();   // ✅
defineSlots<{ leading(): unknown; default(): unknown; trailing(): unknown }>();       // ✅
defineEmits<{ (e: 'press'): void }>();                                                // ❌ click already exists
</script>
```

---

## Composition

- must be mounted by any kind — an action is a leaf, so nothing forbids it a home.
- must compose only [display](display.md) and [indicator](indicator.md) inside its slots.
- must open an [overlay](overlay.md) by flipping the overlay's model, never by mounting it as a child.

```txt
✅ SectionHeading → Button → Spinner       (a busy action swaps its leading slot)
❌ Button → Modal                          (the trigger owning the surface it opens)
```

---

## Neighbours

- [actions](../../components/actions/actions.md) — which one to reach for, and with what values
- [control](control.md) — the kind for a widget that owns a value
- [nav](nav.md) — the kind for a trigger that moves rather than runs
- [overlay](overlay.md) — the surface an action opens
- [visual kinds](visual.md) — every other kind, and the composition ladder
