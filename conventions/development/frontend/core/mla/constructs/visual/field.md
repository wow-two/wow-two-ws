# Field

*Last updated: 2026-08-23*

> A [control](control.md) plus the copy that names it — label, helper, error, and the required and invalid state.
> Purpose — one wrapper owns the label wiring and the error slot, so no control has to grow its own.
> Use case — every control that appears in a form.

## Gate

- must **name a control** — a component with no control inside it is a [display](display.md).
- must own the label, the helper, and the error; a component that owns only the value is a [control](control.md).
- must wire the label to the control by id, so clicking the label focuses it.
- must wrap exactly one value; several values under one label is a form ([forms](../../domains/forms/forms.md)).

```txt
✅ Field · LabeledInput · CheckboxField · RadioField · SwitchField
❌ Fieldset               (it groups fields under a legend — a layout for a form)
```

---

## Location

### Group

- must live in `presentation/forms/` in the SDK, beside the control it wraps.
- must ship the generic wrapper (`Field`) and the fused pairs (`CheckboxField`) from the same group.

```txt
✅ presentation/forms/field/{Field.vue, Field.spec.md, index.ts}
❌ presentation/forms/textField/TextField.vue     (the SDK ships Field + TextInput, not a fusion of both)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must say what it wraps — `a label, control, helper, and error`.

### Construct

- must provide the form-control context — `id`, `isInvalid`, `isDisabled`, `isReadOnly`, `isRequired`.
- must let the control read that context rather than passing the same flags down as props.
- must render the error in place of the helper, never both at once.

### Component name

- must end `*Field` — the generic wrapper included; `{Control}Field` names a fused pair.
- must end a submittable form `*Form`; it composes fields ([forms](../../domains/forms/forms.md)).
- must admit `*Card` for a bordered choice and `*Text` for form copy — all shape words ([visual kinds](visual.md) §
  *Shape words*).
- must not prefix `Form*` — the wrapper is a field whether or not a form is around it.

```vue
<script setup lang="ts">
/** Renders a label, control, helper, and error as one field. */
defineOptions({ name: 'Field' });
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take `label`, `helper`, and `error` as scalar props, each with a same-named slot for rich content.
- must take `isRequired`, `isDisabled`, and `isReadOnly`, and publish each to the control through context.
- must not take the value — the control it wraps owns that.

### Slots

- must expose `default` for the control, plus `label`, `helper`, and `error` as the rich overrides.

### Emits

- must declare no emits — the control emits the value, and the field never intercepts it.

```vue
<script setup lang="ts">
defineProps<{ label?: string; helper?: string; error?: string; isRequired?: boolean }>();   // ✅
defineProps<{ modelValue?: string }>();                                                     // ❌ not its value
</script>
```

---

## Composition

- must wrap exactly one [control](control.md) in its default slot.
- must be composed by a form, which supplies the error from validation ([forms](../../domains/forms/forms.md)).
- must compose [display](display.md) and [feedback](feedback.md) in its copy slots — a tooltip, a character count.
- must not mount a [panel](panel.md), a [view](view.md), or another field.

```txt
✅ AppForm → Field → SelectInput      ·      Field → label slot → Tooltip
❌ Field → Field                 (two labels for one value)
```

---

## Neighbours

- [forms](../../components/forms/forms.md) — which one to reach for, and with what values
- [control](control.md) — the widget a field names
- [forms](../../domains/forms/forms.md) — submit, validation, and where a field's error comes from
- [primitive](primitive.md) — the form-control context that carries id and state to the control
- [visual kinds](visual.md) — every other kind, and the composition ladder
