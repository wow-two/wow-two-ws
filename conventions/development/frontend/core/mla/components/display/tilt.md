# Tilt

*Last updated: 2026-09-10*

> A card that leans towards the cursor — a hover flourish, nothing more.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must add depth to a hero card or a feature tile on a marketing page
- must stay decorative — reduced motion disables the tilt entirely
- should wrap the card rather than replace it; it renders a plain box

---

## Instead of

| Reach for | When |
|---|---|
| [Card](card.md) | the box needs no motion |
| [ScrollReveal](scrollReveal.md) | the motion is an entrance rather than a hover |
| `HoverCard` | the hover should reveal content, not lean the card |

---

## Values

- should leave `maxAngle` at `12`° and `perspective` at `800`
- should leave `scale` at `1`; a growing card fights its neighbours in a grid
