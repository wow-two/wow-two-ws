# Code

*Last updated: 2026-09-10*

> Code set in mono — inline inside a sentence, or as a block.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must set an identifier, a flag, or a path apart inside running copy
- must render a block the reader only reads — it styles, it never copies
- should wrap a block variant in a `<pre>` when the whitespace has to survive

---

## Instead of

| Reach for | When |
|---|---|
| [Snippet](snippet.md) | the reader is meant to copy the text |
| [Kbd](kbd.md) | the glyph is a key the reader presses |
| [DiffViewer](diffViewer.md) | two versions of the text are compared side by side |

---

## Values

- should leave `variant` at `inline`; `block` only for multi-line code
