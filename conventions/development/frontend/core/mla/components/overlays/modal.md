# Modal

*Last updated: 2026-11-01*

> The centred blocking dialog — the default surface when a flow must own the screen until it resolves.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).

## Reach for it when

- must hold a flow that owns the screen — a form, an edit, a picker
- must block the page; nothing behind the scrim is reachable until it closes
- should carry a title, a body, and a footer of actions

---

## Instead of

| Reach for | When |
|---|---|
| [AlertModal](alertModal.md) | the flow requires explicit confirmation of a destructive consequence |
| [Drawer](drawer.md) | the body is long or ancillary and the page stays the subject |
| [BottomSheet](bottomSheet.md) | the reader resizes the surface between snap heights |
| [Popover](popover.md) | the content belongs to one trigger and the page need not dim |

---

## Values

- must let a dirty-flow owner guard dismissal without changing a form into an alert dialog.
- phone layout → [responsive](../../../../shapes/app/responsive/responsive.md#dialogs).

---

## Height

- must pick `ModalContent` `height` by what the content does while the dialog is open:

| Content while open | `height` | Panel |
|---|---|---|
| changes — streams in, loads, switches step | `fixed` | the height paired with `size`, capped at the window |
| settled when it opens — confirm, alert, short prompt | `auto` (default) | fits its content, capped at the window |

- must keep one height across a multi-step dialog's steps — set it once on `ModalContent`, never per step.
- must let `ModalBody` scroll what overflows → [responsive](../../../../shapes/app/responsive/responsive.md#dialogs).
- must take a fixed height from `size` — `sm` 24rem · `md` 32rem · `lg` 40rem · `xl` 48rem · `full` the window;
  never set a panel's height by class.
- implementation → [ModalContent spec](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe/src/presentation/overlays/modal/ModalContent.spec.md).
