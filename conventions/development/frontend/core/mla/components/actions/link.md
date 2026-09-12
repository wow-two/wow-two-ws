# Link

*Last updated: 2026-09-10*

> Inline text that goes somewhere — the one member of this folder that moves rather than runs.
> Kind → [nav](../../constructs/visual/nav.md).

## Reach for it when

- must reach for it for a destination inside prose, a caption, or a footer
- must wrap a router link with `asChild` — middle-click and prefetch survive
- should reach for it when the destination reads as text, not as a control

---

## Instead of

| Reach for | When |
|---|---|
| [Button](button.md) | the trigger runs a command → [action](../../constructs/visual/action.md) |
| `Button asChild` | the destination has to carry a button's weight — a CTA |
| `ToolbarLink` | the destination sits inside a [Toolbar](toolbar.md)'s roving strip |
| `NavItem` | the destination is a row in a sidebar or nav structure → [nav](../../constructs/visual/nav.md) |
