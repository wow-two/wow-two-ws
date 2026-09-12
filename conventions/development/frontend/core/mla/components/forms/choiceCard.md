# ChoiceCard

*Last updated: 2026-09-10*

> A radio wearing a card — the option needs a description or an icon to be choosable.
> What a field is → [field](../../constructs/visual/field.md).

## Reach for it when

- must offer a choice whose label alone under-specifies it — a plan, a tier, a mode
- must sit inside a [RadioGroup](radioGroup.md); the group owns the selection and the name
- should reach for it when the options are few and each deserves a paragraph

---

## Instead of

| Reach for | When |
|---|---|
| [Radio](radio.md) | the option is a bare label with nothing to explain |
| `OptionTile` | the tile runs a command instead of setting a value |
| `ToggleButtonGroup` | the choices are short and fit one strip |
| `Card` | the card is content and nothing is being chosen |

---

## Values

- should leave `size` at `md`; `lg` only where the description runs long
