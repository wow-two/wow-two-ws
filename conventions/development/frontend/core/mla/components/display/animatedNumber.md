# AnimatedNumber

*Last updated: 2026-09-10*

> A number that tweens whenever it changes — a live figure, not an entrance.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show a value that keeps updating — a live count, a running total, a price
- must expect every change to tween, including an interrupting one
- should own the formatting through `format`; the raw tween value is a float

---

## Instead of

| Reach for | When |
|---|---|
| [CountUp](countUp.md) | the number animates once, on mount or on scroll |
| [Stat](stat.md) | the number is a labelled KPI tile rather than a bare figure |
| [Text](text.md) | the value changing does not need to be noticed |

---

## Values

- should leave `duration` at `500` ms — it repeats on every update
- should leave `as` at `span` so the figure stays inline
