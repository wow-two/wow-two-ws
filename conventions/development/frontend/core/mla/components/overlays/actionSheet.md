# ActionSheet

*Last updated: 2026-09-10*

> The iOS-style action list — a bottom sheet of stacked rows closed by a separated Cancel.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).

## Reach for it when

- must offer a short list of actions on a phone, one tap each
- should set the one destructive row apart from the rest
- must end with a Cancel row that only dismisses

---

## Instead of

| Reach for | When |
|---|---|
| [BottomSheet](bottomSheet.md) | the body is free content rather than a row per action |
| `DropdownMenu` | a pointer anchors the list to its trigger on a wide viewport |
| [AlertModal](alertModal.md) | the choice is one confirm, not a list |
| [Drawer](drawer.md) | the panel holds navigation rather than a one-shot action list |

---

## Values

- should pass `title` / `description` as strings, taking the slots only for rich content
