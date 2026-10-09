# SelectPicker

*Last updated: 2026-10-09*

> One value from an enumerable set — a trigger that opens a floating listbox, no typing required.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must pick one value from a set that is known, small-to-medium, and not typed into
- must compose the parts — `SelectPickerTrigger`, `SelectPickerValue`, `SelectPickerContent`, `SelectPickerItem`
- should reach for its generic pair: the key drives equality and serialization, the payload comes back

---

## Instead of

| Reach for | When |
|---|---|
| [ComboboxPicker](comboboxPicker.md) | the set is large or remote and the reader types to narrow it |
| [MultiSelectPicker](multiSelectPicker.md) | more than one value may be picked |
| [RadioGroup](radioGroup.md) | the set is short enough to lay out unfolded |
| [ListboxPicker](listboxPicker.md) | the list stays open and owns the surface it sits on |
| `DropdownMenu` | the entries run commands rather than set a value |

---

## Values

- should leave `placement` at `bottom` — the panel drops under the trigger


## Product adoption

- must use the SDK picker for visible application dropdowns; CSS on native `select` cannot style the operating-system popup consistently
- must keep popup surfaces, selected indicators, focus, keyboard navigation and disabled handling in the SDK
- may compose an application wrapper for translated labels and product layout; must not duplicate popup mechanics
- must pass semantic values to application handlers, preserving number and string identity
- must retain required-field validation and disable choices while their enclosing form is locked, including teleported menus
- must show the committed value until a server-backed change succeeds; a pending request may disable the picker
- must verify the expanded popup in the product, not only its closed trigger or a successful build
- should guard migrated presentation directories against reintroducing raw visible `select` elements
