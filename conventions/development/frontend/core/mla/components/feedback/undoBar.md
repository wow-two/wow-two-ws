# UndoBar

*Last updated: 2026-09-10*

> The snackbar with one reversal — a destructive act that stays undoable for a few seconds.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).

## Reach for it when

- must follow a delete, an archive, or a move the reader may not have meant
- must be the only offer of its kind on screen; it is one bar, never a queue
- should be reached for over a confirm dialog when the act is cheap to reverse

---

## Instead of

| Reach for | When |
|---|---|
| `AlertModal` | the act cannot be reversed and has to be confirmed first |
| [ToastHost](toastHost.md) | several notices may stack, or nothing is reversible |
| [Toast](toast.md) | the card is mounted by hand with no lifecycle |

---

## Values

- must keep the reversal available for its advertised interval and expose an operable undo action.

- should set `hasCountdown` only where the deadline matters — it animates every frame
