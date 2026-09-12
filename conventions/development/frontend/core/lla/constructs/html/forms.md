# Forms

*Last updated: 2026-09-10*

> Every form element and the control attributes that make one usable, plus the shapes that lose the label.
> Purpose — the native control carries validation, autofill and the label association; a rebuilt one carries none.
> Use case — reach here before writing an input, and whenever a control needs a label, a group or an error.

## The elements

| Element | Means | Verdict |
|---|---|---|
| `<form>` | a submittable group with a submit path | `use` |
| `<label for>` | the accessible name, bound to one control by `id` | `use` |
| `<input type="text\|email\|url\|tel\|search\|password">` | a single-line value of a known kind | `use` |
| `<input type="number\|range">` | a numeric value, typed or dragged | `use` |
| `<input type="date\|time\|datetime-local\|month\|week">` | a temporal value with a native picker | `use` |
| `<input type="checkbox\|radio">` | a toggle, and one choice out of a named group | `use` |
| `<input type="file">` · `<input type="color">` | a file pick, and a colour pick | `use` |
| `<input type="hidden">` | a value submitted but never shown | `use with care` |
| `<input type="submit">` · `<input type="image">` | a submit control that is not a `<button>` | `banned` |
| `<textarea>` | a multi-line value | `use` |
| `<select>` · `<option>` · `<optgroup>` | a native choice from a fixed list | `use` |
| `<fieldset>` · `<legend>` | a named group of controls, disabled together | `use` |
| `<datalist>` | suggestions over a free-text input | `use with care` |
| `<output>` · `<progress>` · `<meter>` | a computed result, a task's progress, a gauge | `use with care` |
| `disabled` · `readonly` · `required` · `autocomplete` | the native control states | `use` |
| `<button type="submit">` inside `<form>` | the submit path a form needs to exist | `use` |
| `<input>` with no label and no `aria-label` | a control announced only by its type | `banned` |
| `placeholder` used as the label | a name that disappears on first keystroke | `banned` |
| `<form>` with no submit path | a group that swallows Enter and does nothing | `banned` |
| a `contenteditable` `<div>` as a text field | an input with no value, no name and no validation | `banned` |

- must bind every control to a `<label for>` whose target `id` comes from `useId()`, never a hand-written string.
- must reach for the type that matches the value — it picks the keyboard, the picker and the built-in validation.
- must name a radio group through a shared `name`, which is what makes the arrow keys move between its options.
- must group related controls in `<fieldset>` with a `<legend>`, and disable the group through `fieldset disabled`.
- must wire the error text through `aria-describedby` and the state through `aria-invalid`
  ([global attributes](global-attributes.md)).

---

## Banned

- **an `<input>` with no label and no `aria-label`** — reach for `<label for>`; the control is announced by its type
  alone, so a form of them reads as "edit text, edit text, edit text".
- **`placeholder` used as the label** — reach for a real `<label>`; the text vanishes on the first keystroke, so a
  user who is interrupted cannot recover what the field was for, and it fails contrast on most palettes.
- **`<form>` with no submit path** — reach for `<div>`, or add `<button type="submit">`; the form still captures Enter
  in a single-input field and reloads the page on it.
- **`<input type="submit">` · `<input type="image">`** — reach for `<button type="submit">`; the value doubles as the
  label, so the button text cannot hold an icon, an inline spinner or any markup.
- **a `contenteditable` `<div>` standing in for a text field** — reach for `<input>` / `<textarea>`; it has no value,
  no `name`, no `required`, and autofill and password managers never see it.

```vue
<!-- ✅ id from useId(), a real label, the error announced through describedby -->
<label :for="id" class="text-xs font-medium text-foreground">Email</label>
<input :id="id" type="email" autocomplete="email" :aria-invalid="!!error" :aria-describedby="errorId" />
<p :id="errorId" class="text-xs text-destructive">{{ error }}</p>

<!-- ❌ the placeholder is the only name — it disappears on the first keystroke -->
<input type="text" placeholder="Email" />
```

---

## Neighbours

- [interactive](interactive.md) — the submit button and the label's click target
- [global attributes](global-attributes.md) — `id`, `aria-invalid`, `aria-describedby`
- [forms](../../../mla/domains/forms/forms.md) — state, schema, server errors, the `Field` chrome
- [visual kinds](../../../mla/constructs/visual/visual.md) — the control components already built
