# Sparkline

*Last updated: 2026-09-10*

> The inline trend — a shape with no axes, no scales and no legend.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show a direction beside a figure — in a table cell, a card, a [StatCard](statCard.md)
- must expect no axes; a reader who needs values needs a real chart
- should colour it by inheritance where it sits inside already-toned copy

---

## Instead of

| Reach for | When |
|---|---|
| [StatCard](statCard.md) | the endpoint is the story and the shape is not |
| [HeatmapCalendarGrid](heatmapCalendarGrid.md) | the series is per-day over a year |
| [GanttTimeline](ganttTimeline.md) | the marks are spans on a schedule |
| [AudioWaveformPreview](audioWaveformPreview.md) | the bars are audio peaks the reader seeks through |

---

## Values

- must provide a meaningful text alternative for its trend; use the same scale when comparing series.
