# TimeInput

*Last updated: 2026-09-10*

> The typed time — an `HH:MM` input forgiving about how it is typed, with hour and minute columns behind a clock.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must let the reader type a time they already know — an opening hour, a shift start
- must accept a loose keystroke run rather than demanding a mask
- should reach for it over [TimePicker](timePicker.md) where times are entered in bulk

---

## Instead of

| Reach for | When |
|---|---|
| [TimePicker](timePicker.md) | the time is chosen off a column, not typed |
| [DateTimeInput](dateTimeInput.md) | a day rides with the time |
| [CronInput](cronInput.md) | the value is a schedule rather than one clock time |

---

## Values

- must use a clock-time value when neither a date nor a time zone belongs to the field.

- should accept `9`, `09`, `930`, `9:30` and `09:30` as typed — all commit alike
