# ColorPicker

*Last updated: 2026-08-20*

> The assembled colour control — a trigger opening a panel of area, hue, optional alpha, hex field and presets.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `ColorPicker.spec.md`.

## Reach for it when

- must let the reader pick any colour, not one off a fixed list
- must hold the value as a hex string — `#RRGGBB`, or `#RRGGBBAA` under alpha
- should reach for it before assembling a panel out of the parts yourself

---

## Instead of

| Reach for | When |
|---|---|
| [ColorSwatchPicker](colorSwatchPicker.md) | the choice is a fixed palette, inline, with no free colour |
| [ColorInput](colorInput.md) | the reader types a hex and needs no panel |
| [ColorArea](colorArea.md) | you are building a bespoke panel and need only the SV square |
| [ColorSlider](colorSlider.md) | one channel is being edited on its own |
| [ColorSwatch](colorSwatch.md) | the colour is shown and never edited |

---

## Values

- must leave `defaultValue` at `#3b82f6` unless the form opens on a real colour
- should leave `triggerVariant` at `full` and `triggerSize` at `md`
- should set `triggerVariant` to `swatch` in a toolbar, `value` in dense or code copy
- must set `hasAlpha` only where the stored hex carries `AA` — it is off by default
- should pass the product palette as `presets`; omitted or empty hides the row
- must set `name` for a plain form post — the hidden input ships the hex
- must take `hasAlpha` and `triggerVariant` from the code — the spec omits both
