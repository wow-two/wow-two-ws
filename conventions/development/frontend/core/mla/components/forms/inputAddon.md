# InputAddon

*Last updated: 2026-09-10*

> The joined prefix and suffix around one input — `https://`, `.com`, `kg`.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must reach for it when a fixed, uneditable string frames the value
- must keep the addon out of the posted value — the control still owns that
- should fill the `leading` and `trailing` slots for an icon or a select instead of copy

---

## Instead of

| Reach for | When |
|---|---|
| [InputGroup](inputGroup.md) | every segment is an editable control |
| [CurrencyInput](currencyInput.md) | the prefix is a currency symbol on a number |
| [PercentInput](percentInput.md) | the suffix is `%` on a number |
| [SearchInput](searchInput.md) | the decoration is a search icon and a clear button |
| a control's own decoration slot | the mark sits inside the input's border |

---

## Values

- should keep the copy to a token or two — the segment does not wrap
