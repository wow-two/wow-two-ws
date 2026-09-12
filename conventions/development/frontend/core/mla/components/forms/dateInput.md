# DateInput

*Last updated: 2026-09-10*

> The typed date — a `YYYY-MM-DD` text input with a [Calendar](calendar.md) on its trailing button.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must let the reader type a date they already know — a birth date, an invoice date
- must keep the grid as the fallback, not the primary route to the value
- should reach for it over [DatePicker](datePicker.md) where dates are entered in bulk

---

## Instead of

| Reach for | When |
|---|---|
| [DatePicker](datePicker.md) | the date is browsed for, not known |
| [DateTimeInput](dateTimeInput.md) | a time of day rides with the date |
| [TimeInput](timeInput.md) | only the time of day is captured |
| [Calendar](calendar.md) | the grid should stay open on the page |

---

## Values

- must use a date-only value for calendar dates; a timezone conversion must not move the selected day.

- should bound with `min` and `max`, both forwarded to the calendar
