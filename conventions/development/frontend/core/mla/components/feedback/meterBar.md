# MeterBar

*Last updated: 2026-09-10*

> A gauge whose fill changes tone as the value crosses its thresholds.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).

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
