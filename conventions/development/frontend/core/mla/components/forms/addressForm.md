# AddressForm

*Last updated: 2026-08-24*

> A country-aware address block — the country drives the region options and the postal label.
> What a form is → [field](../../constructs/visual/field.md).
> Its full surface → `AddressForm.spec.md`.

## Reach for it when

- must reach for it when a form posts a whole postal address as one value
- must wrap it in a [Field](field.md) to name it — the block is a `role="group"`, not a control
- should set `name` for a native post; it emits `{name}.line1` and the rest as hidden inputs
- should set `isCompact` on a phone, where city, region and postal stack in one column

---

## Instead of

| Reach for | When |
|---|---|
| [Field](field.md) per line | the product owns the address shape, its labels, or its order |
| [Fieldset](fieldset.md) + [Legend](legend.md) | one line of the address needs an error of its own |
| [PhoneInput](phoneInput.md) | the country-aware value is a dialling number |

---

## Values

- must bind `modelValue` — `value` is React's spelling, and wins when both are set
- must expect its own English copy; the block ships every sub-label unlocalised
- must expect region options for `US` and `CA` only — every other country takes free text
- must leave `isDisabled` and `isReadOnly` unset to inherit the field's context
- must read `AddressForm.spec.md` as stale — the Vue props are `isDisabled`, `isReadOnly`, `isCompact`
