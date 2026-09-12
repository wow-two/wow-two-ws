# InfoRow

*Last updated: 2026-09-10*

> One label-value row, with the value pushed to the far edge.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show one or two pairs — inside a card body, a summary strip, a drawer
- should switch to `stacked` when the value is long enough to collide with its label

---

## Instead of

| Reach for | When |
|---|---|
| [DescriptionList](descriptionList.md) | there are many pairs and they want a semantic `<dl>` |
| [MetricChip](metricChip.md) | the pair is one member of an inline stat strip |
| [Stat](stat.md) | the value is a headline metric with its own tile |
| [Table](table.md) | the pairs repeat per record and want columns |

---

## Values

- should leave `layout` at `inline`; `stacked` when the value wraps
