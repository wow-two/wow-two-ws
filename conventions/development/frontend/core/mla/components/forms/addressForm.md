# AddressForm

*Last updated: 2026-09-10*

> A country-aware address block — the country drives the region options and the postal label.
> Kind → [control](../../constructs/visual/control.md).

## Reach for it when

- must reach for it when a form posts a whole postal address as one value
- must name the composite group and each address input; one outer label cannot name every inner input
- must follow the form adapter's documented serialization contract when using native submission.
- should set `isCompact` on a phone, where city, region and postal stack in one column

---

## Instead of

| Reach for | When |
|---|---|
| [Field](field.md) per line | the product owns the address shape, its labels, or its order |
| [Fieldset](fieldset.md) + [Legend](legend.md) | one line of the address needs an error of its own |
| [PhoneInput](phoneInput.md) | the country-aware value is a dialling number |
