# HeatmapCalendar

*Last updated: 2026-09-10*

> The year grid — 53 weeks by 7 days, each cell shaded by its count.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show a whole year's activity at once — commits, streaks, sessions, logins
- must key the values by calendar date; a `Map` of dates to counts is the input
- should bind `onCellClick` as a prop; its presence makes a cell a button

---

## Instead of

| Reach for | When |
|---|---|
| [EventCalendar](eventCalendar.md) | the days hold events the reader reads and opens |
| [Sparkline](sparkline.md) | the series is a line rather than a per-day grid |
| [Gantt](gantt.md) | the marks span ranges rather than land on single days |

---

## Values

- must offer readable values and meaningful labels when the heatmap is interactive.

- should leave `hasLegend` on; the shading means nothing without its scale
