# ColorSwatchPicker

*Last updated: 2026-09-10*

> The inline palette — a fixed set of swatches, arrow-navigable in both axes, with no panel to open.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must constrain the choice to a palette the product owns — brand, tag, category colours
- must keep the choice on the page rather than behind a trigger
- should reach for it as [ColorPicker](colorPicker.md)'s preset row, which is this component

---

## Instead of

| Reach for | When |
|---|---|
| [ColorPicker](colorPicker.md) | any colour is allowed, not only the palette |
| [ColorSwatch](colorSwatch.md) | one chip is shown and nothing is chosen |
| [RadioGroup](radioGroup.md) | the options carry labels and the colour is decoration |
| [ChoiceCard](choiceCard.md) | each option needs a title and description |

---

## Values

- should leave `swatchSize` at `md` and `swatchShape` at `square`
