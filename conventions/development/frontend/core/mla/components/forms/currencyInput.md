# CurrencyInput

*Last updated: 2026-09-10*

> An amount of money — a [NumberInput](numberInput.md) with a leading symbol pinned inside the box.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect a price, a balance, a limit — anything denominated
- must separate currency identity and display formatting from the numeric value; use the agreed exact-number contract where precision requires it
- should reach for every [NumberInput](numberInput.md) prop — they pass straight through

---

## Instead of

| Reach for | When |
|---|---|
| [NumberInput](numberInput.md) | the number is a quantity rather than money |
| [PercentInput](percentInput.md) | the number is a rate and the suffix is `%` |
| [MaskedInput](maskedInput.md) | the format is rigid and the value is a string |

- should choose the step from the currency and business precision; currencies do not share one minor unit.
