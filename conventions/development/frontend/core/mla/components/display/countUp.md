# CountUp

*Last updated: 2026-09-10*

> A number that counts up once — on mount, or when it scrolls into view.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must land a headline figure on a marketing or results page
- must set `canTriggerOnView` when the figure sits below the fold
- should stay a one-shot; a figure that keeps changing is an animated number

---

## Instead of

| Reach for | When |
|---|---|
| [AnimatedNumber](animatedNumber.md) | the value changes again and every change should tween |
| [Stat](stat.md) | the figure is a dashboard KPI rather than a landing claim |
| [Sparkline](sparkline.md) | the story is the trend rather than the final number |

---

## Values

- should leave `from` at `0` and `duration` at `1500` ms
- should leave `as` at `span`
