# Specs

*Last updated: 2026-09-10*

> A declarative input shape consumed by a behavior component.

## Location

### Folder
- must sit beside the other input models of the domain that consumes it.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- documentation baseline → [data](data.md).

### Construct
- declaration baseline → [data](data.md).

### Type name
- must suffix with `Spec`, named for the subject it describes.
- must use `Spec` for declarative behavior input, rather than a wire `Dto` or a configuration-bound `Settings`.

---

## Content

- must allow an abstract record root for a closed family of specs; concrete cases use the data-carrier default.
- must keep operations in the behavior component that consumes the spec.
