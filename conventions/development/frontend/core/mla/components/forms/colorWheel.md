# ColorWheel

*Last updated: 2026-09-10*

> The hue ring — one value in degrees, and the only circular geometry in the folder.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must edit hue alone, where the wrap from `359` back to `0` should read as continuous
- must pair it with a [ColorArea](colorArea.md) to make a full picker by hand
- should reach for it over a strip where the panel is round rather than boxed

---

## Instead of

| Reach for | When |
|---|---|
| [ColorSlider](colorSlider.md) | hue fits a strip, or a second channel needs the same shape |
| [ColorArea](colorArea.md) | the axes are saturation and brightness |
| [ColorPicker](colorPicker.md) | the panel is the house one, which uses a hue strip |

---

## Values

- should leave `size` at `200` px and `thickness` at `30` px
- should leave `step` at `1` — one degree per arrow press
