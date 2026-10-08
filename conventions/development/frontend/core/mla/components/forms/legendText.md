# LegendText

*Last updated: 2026-09-10*

> The `<legend>` — the name a whole [FieldsetLayout](fieldsetLayout.md) answers to.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must reach for it as the first child of a [FieldsetLayout](fieldsetLayout.md), never on its own
- must carry the name the group answers to, not the name of one control inside it
- should keep it to a phrase — a page reader announces it before every control in the group

---

## Instead of

| Reach for | When |
|---|---|
| [LabelText](labelText.md) | the copy names one control |
| `SectionHeading` | the region is visual and posts no fields |
