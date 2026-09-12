# FormErrorMessage

*Last updated: 2026-09-10*

> The error line under a control — the node the control's `aria-describedby` points at.
> What feedback is → [feedback](../../constructs/visual/feedback.md).

## Reach for it when

- must let it read the context's `errors`; it renders every client and server message
- must not hand-roll an error paragraph — only this node registers as the described-by target
- should pass `message` only as a single hand-written override

---

## Instead of

| Reach for | When |
|---|---|
| [Field](field.md) | the control already has a wrapper that renders the error |
| [FormHelperText](formHelperText.md) | the copy is a hint, and yields while an error shows |
| `Alert` | the failure belongs to the whole form, not one control |
