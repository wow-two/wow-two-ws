# Calendar

*Last updated: 2026-09-10*

> The inline month grid that picks one date — no trigger, no popover, always on the page.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must keep the grid open — a booking step, a filter rail, a settings panel
- must pick exactly one day, with the month steppable around it
- should reach for it as [DatePicker](datePicker.md)'s panel, which mounts this component

---

## Instead of

| Reach for | When |
|---|---|
| [DatePicker](datePicker.md) | the grid belongs behind a trigger |
| [RangeCalendar](rangeCalendar.md) | the selection has two ends |
| [DateInput](dateInput.md) | the date is typed rather than clicked |
| `EventCalendar` | the days are read for what is on them, not picked |

---

## Values

- must derive week order and displayed day names from the active locale or an explicit caller override.

- should bound the grid with `min` and `max` before reaching for a predicate
