# Snippet

*Last updated: 2026-09-10*

> Code with its own copy button — the copyable form of a code block.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show a command, a key, or a URL the reader will paste somewhere
- must hand the copy text in as a string; the button copies the prop, not the DOM

---

## Instead of

| Reach for | When |
|---|---|
| [Code](code.md) | the code is only read, never copied |
| `CopyButton` | the copied value is not code and needs no mono setting |

---

## Values

- should leave `variant` at `inline` for a one-liner; `block` for many lines
