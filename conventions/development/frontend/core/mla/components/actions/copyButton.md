# CopyButton

*Last updated: 2026-09-10*

> A one-click clipboard write that swaps to a copied state on its own.
> What an action is → [action](../../constructs/visual/action.md).

## Reach for it when

- must reach for it beside a code block, ID, token, or share URL
- must reach for it rather than wiring `navigator.clipboard` behind a [Button](button.md)
- should read the slot's `{ copied, error }` when the label swaps, not only the icon

---

## Instead of

| Reach for | When |
|---|---|
| [Button](button.md) | the command is anything other than a clipboard write |
| [Button](button.md) | the payload is rich or multi-part — the copied text is a plain string |
