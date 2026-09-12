# StatusIndicator

*Last updated: 2026-09-10*

> A tone dot with a line of copy — a service's health, at a glance.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).

## Reach for it when

- must report a system's state in words — "All systems normal", "Degraded"
- should show the state as a compact labeled indicator rather than a full report
- should sit on a status page, a header strip, or a settings row

---

## Instead of

| Reach for | When |
|---|---|
| [PresenceIndicator](presenceIndicator.md) | the subject is a person rather than a service |
| [Alert](alert.md) | the state earns a body and actions, not one line |
| `Status` | the mark is a compact chip inside content |

---

## Values

- should set `description` for the freshness line — "Updated 2m ago"
