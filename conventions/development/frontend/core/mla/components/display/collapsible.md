# Collapsible

*Last updated: 2026-09-10*

> One region that opens and closes, with its trigger wired to it.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must fold a single region — advanced settings, a long body, a detail block
- must compose `CollapsibleTrigger` and `CollapsibleContent`; the root pairs their ids
- should bind `v-model:open` when an outer control has to open it

---

## Instead of

| Reach for | When |
|---|---|
| [Accordion](accordion.md) | several regions share one open set |
| `DisclosureButton` | only the button is wanted, over the caller's own region |
| `Drawer` | the region should leave the flow and cover the page |

---

## Values

- should leave `defaultOpen` off; open on mount only when the body is the point
