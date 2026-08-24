# Control

*Last updated: 2026-08-23*

> A widget that owns exactly one value and hands every change back to its caller.
> Purpose — one model contract across 70-odd inputs, so a form binds any of them the same way.
> Use case — text, numbers, dates, colours, files, code, or anything a user edits.

## Gate

- must **own one value** — a component that fires a command and reads nothing back is an [action](action.md).
- must be fully controlled: it renders the value it is given and never keeps a private copy of the truth.
- must carry no label, helper, or error of its own — those belong to the [field](field.md) that wraps it.
- must not submit; a component with a submit is a form ([forms](../../domains/forms/forms.md)).

```txt
✅ TextInput · NumberInput · SelectInput · ComboboxInput · SliderInput · ColorPicker · JsonEditor
❌ AddressForm             (it owns several values and a submit — a form)
```

---

## Location

### Group

- must live in `presentation/forms/` in the SDK, beside the fields that wrap it.
- must live in the product's sub-domain when the value's shape is the product's — the SDK ships generic ones.

```txt
✅ presentation/forms/currencyInput/{CurrencyInput.vue, CurrencyInput.spec.md, index.ts}
❌ presentation/display/slider/Slider.vue      (a display never emits a value)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name the value's shape — a hex colour, a cron string, a date range.

### Construct

- must read the form-control context for `id`, invalid, disabled, and required.
- must render one focusable element that carries the label's `htmlFor` target ([primitive](primitive.md)).

### Component name

- must end `*Input` for a raw typeable control, `*Picker` for a selector that opens its own panel.
- must end `*Editor` for an editing surface over one format — `JsonEditor` · `MarkdownEditor`.
- must end `*Controls` for a control set that submits nothing of its own.
- must admit `*Group` for a homogeneous set of one control — `RadioGroup` · `CheckboxGroup` — and `*Area` for a
  free-drag surface — all shape words ([visual kinds](visual.md) § *Shape words*).

```vue
<script setup lang="ts">
/** Renders a numeric input with a leading currency symbol. */
defineOptions({ name: 'CurrencyInput', inheritAttrs: false });
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must name the value prop `modelValue`, typed to the value's own type, never to `string` for convenience.
- must carry `isDisabled`, `isReadOnly`, `isInvalid`, and `isRequired`, each defaulting to the context.
- must keep the component generic over `T` when it takes an option list.

### Slots

- must expose the decorations a caller replaces — `leading`, `trailing`, `option`, `empty`.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit `update:modelValue` with the parsed value, never with the raw DOM event.
- must emit `update:modelValue` on every committed change, and nothing else on a keystroke it rejects.

```vue
<script setup lang="ts">
defineProps<{ modelValue?: number; isInvalid?: boolean }>();                     // ✅
defineEmits<{ (e: 'update:modelValue', value: number | undefined): void }>();    // ✅ parsed
defineEmits<{ (e: 'change', event: Event): void }>();                            // ❌ raw event
</script>
```

---

## Composition

- must be wrapped by a [field](field.md) whenever it needs a label — the control never grows one.
- must compose [action](action.md) and [indicator](indicator.md) in its decoration slots — a clear button, a meter.
- must open its panel as an [overlay](overlay.md) rather than pushing siblings out of the way.
- must not mount a [view](view.md), a [panel](panel.md), or another control's field wrapper.

```txt
✅ Field → CurrencyInput → InputAddon    ·    ColorPicker → Popover → ColorArea
❌ CurrencyInput → Label                 (the label belongs to the field)
```

---

## Neighbours

- [forms](../../components/forms/forms.md) — which one to reach for, and with what values
- [field](field.md) — the labelled wrapper that gives a control its name, helper, and error
- [action](action.md) — the kind for a trigger that owns no value
- [forms](../../domains/forms/forms.md) — submit, validation, and how a control binds to a form
- [visual kinds](visual.md) — every other kind, and the composition ladder
