# ColorInput

*Last updated: 2026-09-10*

> The hex text input — typed, with a live swatch adornment, and no panel behind it.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must let the reader type or paste a hex, from a spec, a brand doc, or a designer
- must show the parsed colour back while typing, without opening anything
- should pair it with [ColorPicker](colorPicker.md), which mounts one inside its panel

---

## Instead of

| Reach for | When |
|---|---|
| [ColorPicker](colorPicker.md) | the colour is dragged out of a panel rather than typed |
| [ColorSwatchPicker](colorSwatchPicker.md) | the choice is a fixed palette |
| [ColorSwatch](colorSwatch.md) | the hex is displayed and never edited |
| [TextInput](textInput.md) | the string is not a colour and needs no swatch or parse |

---

## Values

- should accept `#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`, with or without the `#`
- should leave `swatchShape` at `square` and `hasAlpha` off
