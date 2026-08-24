# TimePicker

*Last updated: 2026-08-20*

> The time trigger — a button opening hour and minute columns, with no text entry at all.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `TimePicker.spec.md`.

## Reach for it when

- must constrain the time to a fixed interval — slots, appointments, bookings
- must keep the choice to pointer and arrow keys, with nothing to mistype
- should reach for it where the reader browses for a time rather than knowing one

---

## Instead of

| Reach for | When |
|---|---|
| [TimeInput](timeInput.md) | the reader types the time faster than picking it |
| [DateTimeInput](dateTimeInput.md) | a day rides with the time |
| [DateRangePicker](dateRangePicker.md) | the span is measured in days, not minutes |

---

## Values

- must speak `Temporal.PlainTime`; `null` is a real selection, meaning cleared
- should leave `minuteStep` at `5`; raise it to `15` or `30` for slot booking
- should leave `placeholder` at `Pick a time` and `format` at the `HH:MM` default
- must set `name` for a plain form post; the hidden input carries the value
- must take the value as Temporal — the spec still types it as `{ hours, minutes }`
