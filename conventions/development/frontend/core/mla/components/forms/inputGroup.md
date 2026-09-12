# InputGroup

*Last updated: 2026-09-10*

> A row or column of controls joined into one — the input mirror of `ButtonGroup`.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must reach for it when adjacent controls read as one connected control
- must keep every segment a real control — a fixed string is an [InputAddon](inputAddon.md)
- should reach for `orientation="vertical"` when the segments stack

---

## Instead of

| Reach for | When |
|---|---|
| [InputAddon](inputAddon.md) | a segment is a fixed, uneditable string |
| `ButtonGroup` | the segments run commands rather than hold values |
| `Stack` | the controls stay visually separate |
| [Fieldset](fieldset.md) | the grouping is semantic and needs one name |
