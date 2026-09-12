# NumberInput

*Last updated: 2026-09-10*

> A number typed or stepped — `type="number"` with a stepper pair on the trailing edge.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect a quantity the reader may want to type exactly
- must bound the range with native `min` and `max`; they fall through to the input
- should reach for it as the base under [CurrencyInput](currencyInput.md) and
  [PercentInput](percentInput.md)

---

## Instead of

| Reach for | When |
|---|---|
| [Slider](slider.md) | the value is approximate and the range matters more than the digits |
| [Knob](knob.md) | the parameter is continuous and sits in a dense control panel |
| [CurrencyInput](currencyInput.md) | the number is money and needs a symbol |
| [PercentInput](percentInput.md) | the number is a rate and needs a `%` |
| [PinInput](pinInput.md) | the digits are a code, not a quantity |

---

## Values

- should leave `step` at `1`; set it to the smallest meaningful increment otherwise
- should leave `size` at `md`, `border` at `sm`, `ring` at `md` — the input house set
