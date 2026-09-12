# Card

*Last updated: 2026-09-10*

> The bordered box — the generic surface the specific cards are built on.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must group content into a raised or outlined box with its own padding
- must reach for it whenever no card in this folder already names the case
- should compose the parts as siblings — `CardHeader` through `CardFooter`

---

## Instead of

| Reach for | When |
|---|---|
| [FeatureCard](featureCard.md) | the box is a marketing feature tile with a tinted icon |
| [PricingCard](pricingCard.md) | the box is a pricing tier with features and a call to action |
| [StepCard](stepCard.md) | the box is a numbered step in a how-it-works row |
| [Frame](../layout/frame.md) | the wrapper is reusable chrome rather than a content box |
| [SectionHeader](sectionHeader.md) | the block needs a header without a box around it |

---

## Values

- should keep one recipe per surface class across an app, rather than tuning per instance
