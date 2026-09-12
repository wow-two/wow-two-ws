# Gantt

*Last updated: 2026-09-10*

> Tasks as bars on a date axis, with dependency arrows.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must compare spans across a plan — what runs when, and what waits on what
- should pass `from` and `to` when the window should be fixed rather than derived

---

## Instead of

| Reach for | When |
|---|---|
| [Timeline](timeline.md) | each entry is an instant rather than a span |
| [ScheduleView](scheduleView.md) | the axis is one day's hours across resources |
| [EventCalendar](eventCalendar.md) | the reader browses by month, week or day |

---

## Values

- should leave `cellWidth` at `40`, `rowHeight` at `36`, `labelWidth` at `200` px
- should leave `hasWeekends` on so the reader can count working days
