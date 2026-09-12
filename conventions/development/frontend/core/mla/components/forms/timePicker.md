# TimePicker

*Last updated: 2026-09-10*

> The time trigger — a button opening hour and minute columns, with no text entry at all.
> What a control is → [control](../../constructs/visual/control.md).

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

- should choose an interval that matches the real appointment or booking constraint.

- should leave `minuteStep` at `5`; raise it to `15` or `30` for slot booking
