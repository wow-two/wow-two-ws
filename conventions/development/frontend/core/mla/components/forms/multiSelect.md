# MultiSelect

*Last updated: 2026-09-10*

> Zero-to-many behind a trigger — the picks come back as removable tags inside the box.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect several values from a set too long to lay out unfolded
- must compose the parts — `MultiSelectTrigger`, `MultiSelectTags`, `MultiSelectContent`
- should reach for it when the picks must stay visible after the panel closes

---

## Instead of

| Reach for | When |
|---|---|
| [CheckboxGroup](checkboxGroup.md) | the set is short enough to show whole |
| [Combobox](combobox.md) | the reader types to narrow and picks exactly one |
| [TagsInput](tagsInput.md) | the reader invents values rather than choosing them |
| [Listbox](listbox.md) | the list stays open and owns the surface it sits on |

---

## Values

- should leave `placement` at `bottom` — the panel drops under the trigger
