# EventCalendar

*Last updated: 2026-09-10*

> The calendar the reader browses — month, week, day, or agenda.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must let the reader move through dates and read what is on them
- should bind `v-model:view` and `v-model:date` when an outer control drives the range

---

## Instead of

| Reach for | When |
|---|---|
| [ScheduleView](scheduleView.md) | one day is shown across several resources |
| [HeatmapCalendar](heatmapCalendar.md) | the year is read as density, with no events to open |
| [Gantt](gantt.md) | the spans are plan tasks with dependencies |

---

## Values

- should narrow `hourRange` from the full `[0, 24]` to the working window
