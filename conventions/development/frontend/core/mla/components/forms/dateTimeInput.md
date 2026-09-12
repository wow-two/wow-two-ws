# DateTimeInput

*Last updated: 2026-09-10*

> The one control that captures a day and a time together, as a single wall-clock value.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must capture a moment the reader states in one breath — a meeting start, a deadline
- must keep the day and the time in one value, so they validate as one
- should reach for it over a [DateInput](dateInput.md) and [TimeInput](timeInput.md) pair

---

## Instead of

| Reach for | When |
|---|---|
| [DateInput](dateInput.md) | the time of day is not part of the value |
| [TimeInput](timeInput.md) | the day is fixed and only the time is picked |
| [DatePicker](datePicker.md) | a day is browsed for and no time is needed |
| [RecurrenceEditor](recurrenceEditor.md) | the value is a repeating rule, not one moment |

---

## Values

- must distinguish a wall-clock value from a zoned instant; resolve the intended zone at the owning boundary.
