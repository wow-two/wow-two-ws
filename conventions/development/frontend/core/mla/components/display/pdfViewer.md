# PdfViewer

*Last updated: 2026-09-10*

> A PDF read in place — the browser's own viewer, framed with page and zoom controls.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must let a reader read a document without leaving the page
- should pass `pageCount` when it is known; it enables `n / total` and clamps paging

---

## Instead of

| Reach for | When |
|---|---|
| [Image](image.md) | the file is a picture rather than a paged document |
| [DiffViewer](diffViewer.md) | two texts are compared rather than one read |
| `Link` | the document should open in its own tab |

---

## Values

- must offer a usable open/download fallback when the embedded document cannot be rendered.
- must not treat hiding a download control as access protection.
