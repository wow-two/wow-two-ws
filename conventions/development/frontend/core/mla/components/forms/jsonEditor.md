# JsonEditor

*Last updated: 2026-09-10*

> JSON as a value, not as text — a collapsible tree and a raw text mode over one parsed object.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must edit a value that must stay parseable — a config, a payload, a rule set
- must accept the bound value is the parsed object, never the serialized string
- should reach for it when the shape is nested enough that a tree beats a textarea

---

## Instead of

| Reach for | When |
|---|---|
| [CodeEditor](codeEditor.md) | the text is source and need not parse to commit |
| [TextAreaInput](textAreaInput.md) | the value is free text that happens to look structured |
| `Tree` | the structure is read and never edited |
| `DiffViewer` | two versions are compared rather than edited |

---

## Values

- should leave `defaultMode` at `tree` — text mode is the escape hatch, not the entry
- should leave `indent` at `2`; it only shapes the serialized text mode
