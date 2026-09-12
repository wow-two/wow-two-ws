# FileUpload

*Last updated: 2026-09-10*

> The dropzone — a whole surface that takes a drag, falls back to a click, and flags what it rejects.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must accept a drag onto a region the reader can see and aim at
- must reject by type, size, or count and report which rule failed
- should reach for it when files are the screen's subject, not one row of it

---

## Instead of

| Reach for | When |
|---|---|
| [FilePicker](filePicker.md) | a button is all there is room for and nothing is rejected |
| `ProgressBar` | the transfer has started and only its progress is left to show |

---

## Values

- must validate uploads on the server; client filters only provide earlier feedback.

- should rewrite the `Drop files here, or click to browse` label to name the file kind
