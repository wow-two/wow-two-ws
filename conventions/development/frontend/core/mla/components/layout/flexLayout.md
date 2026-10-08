# FlexLayout

*Last updated: 2026-09-10*

> The bare flex box — no direction, no gap, no alignment of its own.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must build a one-off flex line the [StackLayout](stackLayout.md) variant matrix cannot spell
- must carry the arrangement in classes rather than in props
- should stay rare — a row or a column with a gap is a [StackLayout](stackLayout.md)

---

## Instead of

| Reach for | When |
|---|---|
| [StackLayout](stackLayout.md) | the direction, gap and alignment are named props |
| [CenterLayout](centerLayout.md) | the one job is centring on both axes |
| [InlineLayout](inlineLayout.md) | the row wraps and the items share one gap |
| [BoxLayout](boxLayout.md) | nothing has to sit on a flex line at all |
