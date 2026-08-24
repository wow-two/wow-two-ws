# MeterBar

*Last updated: 2026-08-23*

> A gauge whose fill changes tone as the value crosses its thresholds.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `MeterBar.spec.md`.

## Reach for it when

- must read as a level rather than as progress — quota, capacity, disk, score
- must change tone on its own as the value worsens
- must not be picked where a high value is the good one — the map is low-is-good

---

## Instead of

| Reach for | When |
|---|---|
| [ProgressBar](progressBar.md) | the bar tracks a task running to completion |
| `Sparkline` | the shape of the series matters more than the current level |
| [TrendIndicator](trendIndicator.md) | the report is the movement, not the level |

---

## Values

- must pass `thresholds` as `[good, warn]`; they default to `[max * 0.7, max * 0.9]`
- must set `label`; the `meter` role carries no accessible name otherwise
- should leave `max` at `100` and `size` at `md`; only `sm`–`lg` are sized
