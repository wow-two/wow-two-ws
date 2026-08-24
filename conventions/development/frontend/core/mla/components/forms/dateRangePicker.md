# DateRangePicker

*Last updated: 2026-08-20*

> The span trigger — one button for both ends, opening a [RangeCalendar](rangeCalendar.md) that closes on completion.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `DateRangePicker.spec.md`.

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

- must speak `DateRange` — `{ start, end }`, both `Temporal.PlainDate`
- must expect the popover to close itself once both ends are picked
- should leave `placeholder` at `Pick a range`
- should leave `format` alone — it renders each end in the locale short form
- must set `name` for a plain form post — it ships `{name}_start` and `{name}_end`
- must take the ends as Temporal — the spec still types them as `Date`
