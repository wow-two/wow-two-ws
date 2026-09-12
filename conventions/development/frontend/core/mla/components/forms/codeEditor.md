# CodeEditor

*Last updated: 2026-09-10*

> Source entry with a line-number gutter and explicit keyboard indentation behavior.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect source the reader edits — a snippet, a config, a template

---

## Instead of

| Reach for | When |
|---|---|
| [JsonEditor](jsonEditor.md) | the value is JSON and must parse before it commits |
| [MarkdownEditor](markdownEditor.md) | the value is prose and the author wants a preview |
| [TextAreaInput](textAreaInput.md) | the text needs no gutter and no Tab handling |
| `Code` | the source is read and never edited |

---

## Values

- must follow the [editor keyboard contract](../../constructs/visual/control.md#input-behavior) when Tab indents.

- should raise `minHeight` past `12rem` only for a whole file, not a snippet
