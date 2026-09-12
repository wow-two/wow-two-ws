# FilePicker

*Last updated: 2026-09-10*

> A button that opens the OS file dialog — the small file control, with no drop target.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must take a file from a button press in a dense row or toolbar
- must fit where a dropzone would not — a settings row, an inline avatar swap

---

## Instead of

| Reach for | When |
|---|---|
| [FileUpload](fileUpload.md) | the whole surface takes a drop and rejects by type, size, or count |
| `Button` | the press runs a command and reads no file back |

---

## Values

- must validate the chosen file before processing or upload; an accept hint is not validation.

- should leave `size` at `md`; it matches the input row it sits in
