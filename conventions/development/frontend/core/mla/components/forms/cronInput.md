# CronInput

*Last updated: 2026-09-10*

> The cron expression, typed, with a plain-English readout under it that says what was actually written.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must store a schedule in the form a job runner already reads
- must serve a reader who writes cron directly — an operator, not an end user
- should reach for it where the schedule is infrastructure rather than a person's calendar

---

## Instead of

| Reach for | When |
|---|---|
| [RecurrenceEditor](recurrenceEditor.md) | the reader is an end user, and the rule is calendar-shaped |
| [TimePicker](timePicker.md) | the value is one clock time, not a repetition |
| [TextInput](textInput.md) | the string is not a schedule and needs no readout |
