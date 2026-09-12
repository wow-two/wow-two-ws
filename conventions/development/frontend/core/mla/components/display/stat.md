# Stat

*Last updated: 2026-09-10*

> The KPI tile — a label, a big value, an optional trend and helper line.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must headline a measurement on a dashboard or a summary grid
- must pass a signed `trend` value — the sign picks the arrow and the colour
- should use the helper line for the comparison window, not for a second metric

---

## Instead of

| Reach for | When |
|---|---|
| [MetricChip](metricChip.md) | the measurement is one member of an inline strip |
| [InfoRow](infoRow.md) | the pair is a label and value in a full-width row |
| [Sparkline](sparkline.md) | the trend's shape matters more than its endpoint |
| [CountUp](countUp.md) | the figure is a landing-page claim rather than a live KPI |

---

## Values

- should leave `size` at `md`
