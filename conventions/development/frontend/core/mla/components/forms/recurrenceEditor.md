# RecurrenceEditor

*Last updated: 2026-09-10*

> The repeat rule an end user builds — frequency, interval, and an end, with the next occurrences listed back.
> What a control is → [control](../../constructs/visual/control.md).

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

- should narrow the rule with `byDay` or `byMonthDay`, and end it with `count` or `until`
- should leave `previewCount` at `5` — enough to check the rule, short enough to scan
