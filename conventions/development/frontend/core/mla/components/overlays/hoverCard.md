# HoverCard

*Last updated: 2026-09-10*

> The hover preview — richer than a tooltip, and it never takes focus from the page.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).

## Reach for it when

- must preview something inline on hover — a mention, a link, a data point
- should carry read-only content; the card does not trap focus
- must open on focus as well as hover, so a keyboard reaches it

---

## Instead of

| Reach for | When |
|---|---|
| [Popover](popover.md) | the panel holds a control the reader must reach and operate |
| `Tooltip` | the content is one short label rather than a card |
| [Modal](modal.md) | the preview is a place worth opening deliberately |

---

## Values

- should leave `openDelay` at `700`ms and `closeDelay` at `300`ms
- should leave `placement` at `bottom` and `offset` at `8` — the house anchor pair
