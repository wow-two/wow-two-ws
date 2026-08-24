# RecurrenceEditor

*Last updated: 2026-08-20*

> The repeat rule an end user builds — frequency, interval, and an end, with the next occurrences listed back.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `RecurrenceEditor.spec.md`.

## Reach for it when

- must capture "every other Tuesday until March" from someone who thinks in calendars
- must round-trip an RFC-5545 rule a calendar server already speaks
- should reach for it wherever the schedule shows up on a person's calendar

---

## Instead of

| Reach for | When |
|---|---|
| [CronInput](cronInput.md) | the reader writes cron, and the consumer is a job runner |
| [DateRangePicker](dateRangePicker.md) | the value is one span, not a repetition |
| [DateTimeInput](dateTimeInput.md) | the value is a single moment |
| `EventCalendar` | occurrences are read rather than defined |

---

## Values

- must speak `RecurrenceRule` — `freq` and `interval` are always carried
- should narrow the rule with `byDay` or `byMonthDay`, and end it with `count` or `until`
- must expect `FREQ=WEEKLY` at `interval` `1` when uncontrolled
- must anchor `from` on a `Temporal.PlainDate`; it defaults to today
- should leave `previewCount` at `5` — enough to check the rule, short enough to scan
- must set `name` for a plain form post; the hidden input carries the `RRULE:` string
- must not pass `weekStart` — the spec lists it, the code has no such prop
