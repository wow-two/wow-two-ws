# Accordion

*Last updated: 2026-09-10*

> The disclosure group — several panels, one open set, arrow keys between them.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must stack sections the reader opens one at a time — an FAQ, a settings group
- must compose the sibling parts — `AccordionItem` · `Trigger` · `Content`
- should let the group own the open set; an item never tracks its own

---

## Instead of

| Reach for | When |
|---|---|
| [Collapsible](collapsible.md) | one region opens and closes, with no siblings |
| [Tabs](tabs.md) | exactly one panel is visible and they share a strip |
| [Tree](tree.md) | the sections nest inside each other |
| `DisclosureButton` | only the trigger is needed, over caller markup |

---

## Values

- should leave `type` at `single` — `multiple` only when panels are compared
