# DateInput

*Last updated: 2026-08-20*

> The typed date — a `YYYY-MM-DD` text input with a [Calendar](calendar.md) on its trailing button.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `DateInput.spec.md`.

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

- must speak `Temporal.PlainDate`; `null` is the cleared state
- should leave `placeholder` at `YYYY-MM-DD` — it names the accepted format
- must leave `native` off by default; the browser panel cannot carry the theme
- should set `native` only where the platform picker is the point — a mobile-first form
- should bound with `min` and `max`, both forwarded to the calendar
- must take the value as Temporal — the spec still types it as `Date`
