# AlertModal

*Last updated: 2026-10-26*

> The confirm — a modal locked to `alertdialog` that a stray click outside cannot dismiss.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).

## Reach for it when

- must gate a destructive or irreversible act — delete, revoke, discard
- must force an explicit choice; there is no corner close affordance
- should name the consequence in the description, not only in the title

---

## Instead of

| Reach for | When |
|---|---|
| [Modal](modal.md) | the flow is not a confirm and dismissing it costs nothing |
| `UndoBar` | the act is reversible — undo after it beats a confirm before it |
| [ActionSheet](actionSheet.md) | a phone picks between several actions, one of them destructive |
| `TypedConfirmModal` | an irreversible act hits a production target — the reader types its ID first |

---

## Values

- should land initial focus on the safe option, `Cancel`
- must use the styled app warning modal for product edits, discard navigation, deletion and ordinary CRUD confirmations; show a warning icon, a clear consequence and explicit action labels
- must not use `window.alert`, `window.confirm` or `window.prompt` for those app flows
- must reserve native dialogs for a critical app/browser condition where the app cannot present a reliable modal, such as the browser-required `beforeunload` safeguard
- must retain unsaved-edit protection during a browser close or reload; this exception does not permit native confirmation during ordinary in-app product editing
- must restore focus to the initiating control and cancel the pending intent when the owning view or session ends
- must ask for the target's typed ID through `TypedConfirmModal` before an irreversible production act
- must use `TypedConfirmField` with `useTypedConfirmation` when the typed ID sits inside a larger dialog or form
- must send the typed text unchanged as the API's `confirm` when the endpoint takes one
- must show a refusal in the modal's `error`, read per [state and data](../../domains/data/state-and-data.md#transport)
- phone layout → [responsive](../../../../shapes/app/responsive/responsive.md#dialogs)
