# StatusIndicator

*Last updated: 2026-08-23*

> A tone dot with a line of copy — a service's health, at a glance.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `StatusIndicator.spec.md`.

## Reach for it when

- must report a system's state in words — "All systems normal", "Degraded"
- must carry that copy itself; a bare mark with no text is an indicator, not this
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

- must set `label` or its slot — neither ships a default
- must set `tone` from the status vocabulary; it defaults to `success`
- should set `description` for the freshness line — "Updated 2m ago"
- should set `hasPulse` only for a live feed; the ring animates on every render
