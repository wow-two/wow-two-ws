# Field

*Last updated: 2026-09-10*

> A [control](control.md) plus the copy that names it — label, helper, error, and the required and invalid state.
> Purpose — one wrapper owns the label wiring and the error slot, so no control has to grow its own.
> Use case — every control that appears in a form.

## Gate

- must name one semantic value and own its external label, helper and error presentation.
- must use a label association for one labelable element; use a named group for composite values.
- must distinguish generic field chrome from a fused `{Control}Field` that includes its control.
- must keep a collection of independently validated fields in a fieldset or form, not one label target.
- must let helper and error associations describe the relevant control without duplicating announcements.

---

## Location

### Group

- must live in `presentation/forms/` in the SDK, beside the control it wraps.
- must ship the generic wrapper (`Field`) and the fused pairs (`CheckboxField`) from the same group.

```txt
✅ presentation/forms/field/{Field.vue, Field.spec.md, index.ts}
❌ presentation/forms/field/Field.vue owns a second model beside its slotted TextInput
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must say what it wraps — `a label, control, helper, and error`.

### Construct

- must provide the form-control context — `id`, `isInvalid`, `isDisabled`, `isReadOnly`, `isRequired`.
- must publish inherited flags and accessible associations through the shared control context.
- must render the error in place of the helper, never both at once.

### Component name

- must end `*Field` — the generic wrapper included; `{Control}Field` names a fused pair.
- must apply the [forms contract](../../domains/forms/forms.md) to a `*Form`; a form is not generic field chrome.
- must admit `*Card` for a bordered choice and `*Text` for form copy — all shape words ([visual kinds](visual.md) §
  *Shape words*).
- must not prefix `Form*` — the wrapper is a field whether or not a form is around it.

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take `label`, `helper`, and `error` as scalar props, each with a same-named slot for rich content.
- must take `isRequired`, `isDisabled`, and `isReadOnly`, and publish each to the control through context.
- must keep generic chrome value-free; a fused field forwards its control's model contract without a second state owner.

### Slots

- must expose `default` for the control, plus `label`, `helper`, and `error` as the rich overrides.

### Emits

- must keep generic chrome free of value emits; a fused field forwards its control's value changes unchanged.

---

## Composition

- must wrap one semantic control or named composite value in the generic field's default slot.
- must not nest generic field providers for the same value; a fused field reuses existing context or installs it when standalone.
- must omit a duplicate visible label when outer chrome supplies only help/error for a fused field.
- must compose help, errors and optional explanations under the shared [composition contract](visual.md#composition-order).
- must register the focus target and described-by nodes with the owning control context.
- must preserve caller IDs and use generated IDs only when the caller supplied none.

---

## Neighbours

- [forms](../../components/forms/forms.md) — which one to reach for, and with what values
- [control](control.md) — the widget a field names
- [forms](../../domains/forms/forms.md) — submit, validation, and where a field's error comes from
- [primitive](primitive.md) — the form-control context that carries id and state to the control
- [visual kinds](visual.md) — every other kind, and the composition contract
