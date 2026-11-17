# ImagePreview

*Last updated: 2026-11-16*

> A picture with a fallback for when it fails to load.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must render content the reader looks at — a photo, a screenshot, a cover
- must supply the `fallback` slot and handle missing `src` before rendering `ImagePreview`
  ([image fallback](../../constructs/visual/display.md#image-fallback))
- should wrap it in `AspectRatioLayout` when the box must not resize as the file loads

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
