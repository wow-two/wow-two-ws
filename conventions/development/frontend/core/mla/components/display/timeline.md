# Timeline

*Last updated: 2026-09-10*

> The vertical rail — events in order, joined by a connector line.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show what happened in order — a status history, a release log, a case file
- must compose `TimelineItem` with `TimelineTitle` and `TimelineDescription`
- should keep the entries a fixed set; the last item's connector is suppressed for you

---

## Instead of

| Reach for | When |
|---|---|
| [ActivityFeed](activityFeed.md) | the entries are actor-verb-target sentences with avatars |
| [StepCard](stepCard.md) | the steps are instructions in a row rather than events on a rail |
| [Gantt](gantt.md) | each entry spans a range and the ranges are compared |
| [List](list.md) | the order carries no time |

---

## Values

- should leave `align` at `left`; a centred rail costs width for no meaning
