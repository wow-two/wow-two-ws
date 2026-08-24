# ProgressBar

*Last updated: 2026-08-23*

> The horizontal track — a task's completion read left to right.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `ProgressBar.spec.md`.

## Reach for it when

- must report a task running to a known end — an upload, an import, a render
- must go indeterminate by omitting `value`, while the end is still unknown
- should reach for it wherever the row has width to spare

---

## Instead of

| Reach for | When |
|---|---|
| [ProgressCircle](progressCircle.md) | the report has to fit a tile, a button, or an avatar |
| [MeterBar](meterBar.md) | the number is a level with a bad zone, not a task |
| [ProgressSteps](progressSteps.md) | the work is named stages rather than a percentage |
| [Spinner](spinner.md) | no fraction is knowable and none ever will be |

---

## Values

- must set `label`; the `progressbar` role carries no accessible name otherwise
- must pass `value` on the same scale as `max` — it is clamped to `0..max`
- should leave `max` at `100`, so the value reads as a percentage
- should leave `tone` at `brand` — `success` and `danger` state an outcome
- should leave `size` at `md` — only `sm`–`lg` carry a thickness
