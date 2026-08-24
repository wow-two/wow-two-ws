# TimeInput

*Last updated: 2026-08-20*

> The typed time — an `HH:MM` input forgiving about how it is typed, with hour and minute columns behind a clock.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `TimeInput.spec.md`.

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

- must speak `Temporal.PlainTime`; `null` is the cleared state
- should accept `9`, `09`, `930`, `9:30` and `09:30` as typed — all commit alike
- should leave `minuteStep` at `5` and `placeholder` at `--:--`
- must leave `native` off by default; the browser panel cannot carry the theme
- must take the value as Temporal — the spec still types it as `{ hours, minutes }`
