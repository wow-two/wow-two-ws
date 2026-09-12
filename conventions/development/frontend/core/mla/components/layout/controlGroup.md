# ControlGroup

*Last updated: 2026-09-10*

> The labelled control row — a muted label bound to the control beside or above it.
> Kind → [field](../../constructs/visual/field.md).

## Reach for it when

- must bind a muted label to a control in a settings or preferences list
- must stack such rows and have the hairlines fall between them
- should reach for it outside a form — a validated input is a form field

---

## Instead of

| Reach for | When |
|---|---|
| `Field` | the control is a form input with help and error text |
| [Stack](stack.md) | the label is not part of the arrangement |
| `ButtonGroup` | the row is commands, not a labelled control |

---

## Values

- should pass `labelWidth` to align labels down a stack — a CSS length, `"6rem"`
