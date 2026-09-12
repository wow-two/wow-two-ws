# Image

*Last updated: 2026-09-10*

> A picture with a fallback for when it fails to load.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must render content the reader looks at — a photo, a screenshot, a cover
- must fill the fallback slot; without one a broken source leaves a broken image
- should wrap it in `AspectRatio` when the box must not resize as the file loads

---

## Instead of

| Reach for | When |
|---|---|
| [Avatar](avatar.md) | the picture stands for a person or an account |
| `Icon` | the mark is a glyph rather than a file |
| [PdfViewer](pdfViewer.md) | the file is a document with pages |

---

## Values

- must provide meaningful alternative text for informative content and an empty alternative for decoration.
