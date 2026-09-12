# MarkdownEditor

*Last updated: 2026-09-10*

> Markdown with a live preview — a syntax toolbar over the selection and a rendered pane beside it.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must author a document the reader wants to see rendered as they write
- must accept the toolbar's fixed set — bold, italic, code, link, list, quote, H1, H2
- should reach for it for release notes, descriptions, docs — anything long-lived

---

## Instead of

| Reach for | When |
|---|---|
| [ChatComposer](chatComposer.md) | the text is a message with a send, not a document |
| [CodeEditor](codeEditor.md) | the text is source and there is nothing to preview |
| [TextAreaInput](textAreaInput.md) | the text carries no formatting at all |
| `Code` | the markdown is rendered read-only elsewhere |

---

## Values

- must apply the HTML sanitization and URL policy when replacing a rendered preview.

- should leave `defaultView` at `split`; drop to `edit` where the pane is too narrow
- should leave `minHeight` at `18rem` — the split panes need the height to be useful
