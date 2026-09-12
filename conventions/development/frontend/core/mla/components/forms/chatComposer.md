# ChatComposer

*Last updated: 2026-09-10*

> The message box for a thread — an autogrowing textarea, a toolbar, and a send button.
> A [control](../../constructs/visual/control.md) edits the message; the caller owns the send operation.

## Reach for it when

- must compose a message into a running thread, not a document
- must handle a keystroke send and a newline in the same box
- should hang attach or model pickers off `leading` and `trailing`

---

## Instead of

| Reach for | When |
|---|---|
| [TextAreaInput](textAreaInput.md) | the page owns the send and the box only collects text |
| [MarkdownEditor](markdownEditor.md) | the author writes a document and wants a preview |
| `MessageList` | the surface renders the thread rather than composing into it |

---

## Values

- must avoid sending while an IME composition is in progress.
- should use Enter to send only when the product also gives a clear newline gesture.

- should leave `submitOn` at `enter` — the chat default readers expect
- should leave `maxHeight` at `200` px; past it the textarea scrolls
