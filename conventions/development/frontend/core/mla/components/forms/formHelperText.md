# FormHelperText

*Last updated: 2026-09-10*

> The hint line under a control — the node the control's `aria-describedby` points at.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must carry what the reader needs before typing — a format, a limit, a source
- must not hand-roll a hint paragraph; only this node registers as the described-by target
- must not restate a rule the error will repeat — inside a [Field](field.md) the error replaces it

---

## Instead of

| Reach for | When |
|---|---|
| [Field](field.md) | the control already has a wrapper that renders the helper |
| [FormErrorMessage](formErrorMessage.md) | the copy reports a broken rule rather than describing the input |
| [CharacterCount](characterCount.md) | the hint is a live count against a limit |
| `Tooltip` | the copy is optional detail and may stay hidden |

---

## Values

- should keep it to one line; a page reader announces the whole node after the name
