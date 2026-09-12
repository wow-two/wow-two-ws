# Select

*Last updated: 2026-09-10*

> One value from an enumerable set — a trigger that opens a floating listbox, no typing required.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must pick one value from a set that is known, small-to-medium, and not typed into
- must compose the parts — `SelectTrigger`, `SelectValue`, `SelectContent`, `SelectItem`
- should reach for its generic pair: the key drives equality and serialization, the payload comes back

---

## Instead of

| Reach for | When |
|---|---|
| [Combobox](combobox.md) | the set is large or remote and the reader types to narrow it |
| [MultiSelect](multiSelect.md) | more than one value may be picked |
| [RadioGroup](radioGroup.md) | the set is short enough to lay out unfolded |
| [Listbox](listbox.md) | the list stays open and owns the surface it sits on |
| `DropdownMenu` | the entries run commands rather than set a value |

---

## Values

- should leave `placement` at `bottom` — the panel drops under the trigger
