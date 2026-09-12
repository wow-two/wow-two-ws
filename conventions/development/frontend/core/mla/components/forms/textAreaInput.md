# TextAreaInput

*Last updated: 2026-09-10*

> Multi-line plain text, with an appropriate manual or automatic sizing contract.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect text that runs past one line — a note, a description, a reason
- should pair it with [CharacterCount](characterCount.md) wherever a cap is enforced

---

## Instead of

| Reach for | When |
|---|---|
| [TextInput](textInput.md) | the value is a single line and Enter should submit |
| [MarkdownEditor](markdownEditor.md) | the text carries formatting and wants a preview |
| [ChatComposer](chatComposer.md) | the text is a message and the box owns the send |
| [CodeEditor](codeEditor.md) | the text is source and needs a gutter and Tab handling |

---

## Values

- should leave `rows` at `3`; raise it where the expected answer is a paragraph
- should leave `size` at `md`, `border` at `sm`, `ring` at `md` — the input house set
