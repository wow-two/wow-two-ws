# Overlays

*Last updated: 2026-08-22*

> Which overlay to reach for, and with what values — the application register over the SDK's `overlays/` group.
> Use case — picking between two surfaces that both work, or fixing the value one carries here.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).

## Components

| Component | Reach for it when |
|---|---|
| [ActionSheet](actionSheet.md) | a phone offers a short list of actions, one tap each |
| [AlertModal](alertModal.md) | a destructive act needs an explicit confirm |
| [Backdrop](backdrop.md) | a custom surface needs a scrim of its own |
| [BottomSheet](bottomSheet.md) | the reader resizes the surface between snap heights |
| [Drawer](drawer.md) | a long or ancillary body opens from a viewport edge |
| [HoverCard](hoverCard.md) | a hover previews something inline, read-only |
| [Modal](modal.md) | a flow owns the screen until it resolves |
| [Popover](popover.md) | content belongs to one trigger and the page need not dim |
| [Tour](tour.md) | a feature is walked, spotlighting one target per step |
