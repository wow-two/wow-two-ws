# TrendIndicator

*Last updated: 2026-08-23*

> A signed delta with an arrow — whether a metric moved the right way.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `TrendIndicator.spec.md`.

## Reach for it when

- must report a change in a metric rather than its level
- must sit beside the figure it qualifies — a stat, a cell, a card
- should be reached for where the sign alone answers the question

---

## Instead of

| Reach for | When |
|---|---|
| `Stat` | the figure itself is the subject and the delta rides inside it |
| `Sparkline` | the shape of the series matters, not one delta |
| [MeterBar](meterBar.md) | the value is a level against a threshold |

---

## Values

- must set `isInverse` wherever a rise is bad — error rate, churn, latency
- must pass `format` when the delta is not a percentage; the default renders `+N%`
- should set `label` to name the comparison window — "vs last week"
- should leave `size` at `sm`; it is tuned to sit beside body copy
