# ProgressCircle

*Last updated: 2026-08-23*

> The ring — the same completion as a bar, wherever only a square fits.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `ProgressCircle.spec.md`.

## Reach for it when

- must sit in a tile, a stat card, a button, or beside an avatar
- must go indeterminate by omitting `value` — the ring then spins at a fixed quarter
- should be reached for where the number is glanced at rather than read precisely

---

## Instead of

| Reach for | When |
|---|---|
| [ProgressBar](progressBar.md) | the row has width and the fraction is read precisely |
| [Spinner](spinner.md) | nothing determinate will ever be known |
| [MeterBar](meterBar.md) | the value is a level against a threshold |

---

## Values

- must set `label`; the `progressbar` role carries no accessible name otherwise
- must scale `thickness` with `size` — the radius is `(size - thickness) / 2`
- should leave `size` at `40` and `thickness` at `4` px; the pair is tuned
- should leave `tone` at `brand` and `max` at `100`
