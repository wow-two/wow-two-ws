# Tooltip

*Last updated: 2026-09-10*

> One short label on hover or focus — the smallest thing that floats.
> Kind → [overlay](../../constructs/visual/overlay.md).

## Reach for it when

- may explain an already named icon-only control or expand a truncated label
- must carry text only; it takes no focus and holds nothing operable
- should stay optional — the app must work for a reader who never hovers

---

## Instead of

| Reach for | When |
|---|---|
| `HoverCard` | the hover previews a card of content rather than a label |
| `Popover` | the panel holds a control the reader must reach |
| [KeyboardShortcut](keyboardShortcut.md) | the label is only the accelerator for a command |

---

## Values

- must preserve the trigger's accessible name and use the tooltip for description.

- should leave `openDelay` at `700` ms and `closeDelay` at `0` — the OS pattern
- should leave `placement` at `top`
