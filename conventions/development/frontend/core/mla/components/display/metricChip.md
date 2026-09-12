# MetricChip

*Last updated: 2026-09-10*

> Icon, mini-label and value in one inline chip — the unit of a stat strip.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must line several measurements across one row — duration, size, count
- must keep each chip inline; a chip is a strip member, not a tile
- should pass label and value as scalars, and use the slots only for rich content

---

## Instead of

| Reach for | When |
|---|---|
| [Stat](stat.md) | the metric is a headline KPI with its own tile |
| [InfoRow](infoRow.md) | the pair is a full-width row with the value pushed right |
| [Badge](badge.md) | the chip carries a word rather than a label-value pair |
| [Status](status.md) | the chip names a state rather than measuring something |

---

## Values

- should leave `tone` at `neutral`; tint only when the value itself is good or bad
- should leave `size` at `sm` — the chip belongs to a strip, not a header
