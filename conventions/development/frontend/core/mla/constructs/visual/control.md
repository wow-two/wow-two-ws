# Control

*Last updated: 2026-09-10*

> A widget editing one semantic value, which may contain several coordinated parts.
> Purpose — a shared value contract lets a form bind simple and composite controls consistently.
> Use case — text, numbers, dates, colours, files, code, or anything a user edits.

## Gate

- must edit a semantic value: text, a selection, a range or a structured value.
- must classify selection by what callers use it for, not by whether today's prop is named `modelValue`.
- must follow [controlled state](../../../lla/notation/naming/props.md#controlled-state) for ownership and resets.
- must leave external label, helper and error composition to a [field](field.md).
- may include internal sub-control labels when one structured value needs several independently named inputs.
- may compose a send or commit action; a control does not own the enclosing form's validation/submission lifecycle.

```txt
✅ DateTimeInput edits a wall clock; a color area edits coordinated channels
❌ A tab root classified as a form control only because it tracks the active tab
```

---

## Location

### Group

- must live in `presentation/forms/` in the SDK, beside the fields that wrap it.
- must live in the product's sub-domain when the value's shape is the product's — the SDK ships generic ones.

```txt
✅ presentation/forms/currencyInput/{CurrencyInput.vue, CurrencyInput.spec.md, index.ts}
❌ presentation/display/slider/Slider.vue      (its primary contract edits a committed value)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name the value's shape — a hex colour, a cron string, a date range.

### Construct

- must read the form-control context when present; standalone controls use their own IDs, names and state props.
- must register a focus target for focus-on-error; a composite may have several focusable children.
- must name a native input with its label target and a composite with group semantics and named child controls.

### Component name

- must end `*Input` for direct value entry, `*Picker` for choosing a value from presented alternatives.
- must end `*Editor` for an editing surface over one format — `JsonEditor` · `MarkdownEditor`.
- must end `*Controls` for a control set that submits nothing of its own.
- must admit `*Group` for a homogeneous set of one control — `RadioGroup` · `CheckboxGroup` — and `*Area` for a
  free-drag surface — all shape words ([visual kinds](visual.md) § *Shape words*).

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must type the committed value to its semantic shape; framework spelling belongs to
  [Vue macros](../../../lla/constructs/vue/macros.md) or [React](../../../lla/constructs/react/react.md).
- must inherit invalid, disabled, read-only and required state unless an explicit override is supplied.
- must distinguish whole-control disabled state from an item/day availability predicate.
- must preserve native attribute spellings and flag precedence from [props](../../../lla/notation/naming/props.md).
- must keep the component generic over `T` when it takes an option list.

### Slots

- must expose the decorations a caller replaces — `leading`, `trailing`, `option`, `empty`.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must report committed values through the framework model contract, not raw DOM events.
- must distinguish draft changes from committed changes; a rejected draft must not replace the committed value.
- must state whether commit occurs during input, on blur, or through an explicit action in the component spec.

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- may build a composite from other controls, actions, indicators and mode views.
- must give an inline picker an in-flow body; use an [overlay](overlay.md) only for its floating presentation.
- must keep each internal control's name and focus behavior valid under the enclosing value editor.
- must leave the enclosing form lifecycle to the [forms domain](../../domains/forms/forms.md).

---

## Input behavior

- must preserve incomplete draft text where parsing before commit would block valid typing.
- must process IME composition without submitting, tokenizing or rejecting an unfinished composition.
- must handle paste, selection replacement, caret movement and autofill through the same value contract.
- must clear draft errors on the relevant new edit and discard stale asynchronous validation results.
- must preserve pending edits when a save is in flight; submission races belong to the forms domain.
- must provide an advertised keyboard exit when an editor intercepts `Tab`.
- must provide a keyboard and single-pointer alternative for drag-only value changes.
- must test controlled/uncontrolled, null clear, external update, reset and disabled/read-only behavior.
- must test grouped labels, focus-on-error, composition, paste and locale changes for bespoke controls.

---

## Neighbours

- [forms](../../components/forms/forms.md) — which one to reach for, and with what values
- [field](field.md) — the labelled wrapper that gives a control its name, helper, and error
- [action](action.md) — the kind for a trigger that owns no value
- [forms](../../domains/forms/forms.md) — submit, validation, and how a control binds to a form
- [visual kinds](visual.md) — every other kind, and the composition contract
