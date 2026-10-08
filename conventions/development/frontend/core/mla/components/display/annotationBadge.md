# AnnotationBadge

*Last updated: 2026-09-10*

> The marked run that opens a thread — inline highlight, or a bare numbered pin.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must attach a comment to a run of text the reader can click back into
- must set `isPinOnly` for a margin or floating pin, and position it with a class
- should set `isResolved` rather than unmounting — it re-tones and strikes the run

---

## Instead of

| Reach for | When |
|---|---|
| [MarkText](markText.md) | the run is tinted and nothing opens when it is clicked |
| [HighlightText](highlightText.md) | the runs come from a search query |
| [CommentThreadGroup](commentThreadGroup.md) | the surface is the thread itself rather than its anchor |

---

## Values

- should leave `tone` at `comment`; `isResolved` overrides the tone on its own
