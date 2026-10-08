# ClusterLayout

*Last updated: 2026-09-10*

> The centred wrapping row — hero CTAs, auth-page actions, footer link groups.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must centre a row that wraps onto more lines as it fills
- should reach for it under a heading or a hero, where a row reads as centred

---

## Instead of

| Reach for | When |
|---|---|
| [InlineLayout](inlineLayout.md) | the row starts at the leading edge instead of the centre |
| [StackLayout](stackLayout.md) | the row stays on one line and the axis may change |
| `ButtonGroup` | the buttons read as one connected control |
| `Toolbar` | the commands share one tab stop |

---

## Values

- should reach for [InlineLayout](inlineLayout.md) rather than `justify="start"`
