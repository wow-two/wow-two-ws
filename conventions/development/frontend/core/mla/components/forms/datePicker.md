# DatePicker

*Last updated: 2026-08-20*

> The date trigger — a button showing the formatted date, opening a [Calendar](calendar.md) in a popover.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `DatePicker.spec.md`.

## Reach for it when

- must pick one day from a form row that has no space for a standing grid
- must show the chosen date formatted for reading, not as an ISO string
- should reach for it as the default date control; typing is the exception

---

## Instead of

| Reach for | When |
|---|---|
| [DateInput](dateInput.md) | the reader types the date faster than clicking it |
| [Calendar](calendar.md) | the grid should stay open on the page |
| [DateRangePicker](dateRangePicker.md) | the selection has two ends |
| [DateTimeInput](dateTimeInput.md) | a time of day rides with the date |

---

## Values

- must speak `Temporal.PlainDate`; `null` is a real selection, meaning cleared
- should leave `placeholder` at `Pick a date`
- should leave `format` alone — it renders locale numeric year, short month, day
- must set `name` for a plain form post; the hidden input carries the ISO date
- should bound with `min` and `max`, both forwarded to the calendar
- must take the value as Temporal — the spec still types it as `Date`
