# DateRangePicker

*Last updated: 2026-09-10*

> The span trigger — one button for both ends, opening a [RangeCalendar](rangeCalendar.md) that closes on completion.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must take a from-and-to as one value, not as two independent fields
- must keep both ends under one label and one validation message
- should reach for it for any reporting or filtering window

---

## Instead of

| Reach for | When |
|---|---|
| [DatePicker](datePicker.md) | one day is picked |
| [RangeCalendar](rangeCalendar.md) | the grid should stay open on the page |
| [DateInput](dateInput.md) | each end is typed, and they validate separately |

---

## Values

- must name both ends of the range and validate their ordering as one semantic value.
