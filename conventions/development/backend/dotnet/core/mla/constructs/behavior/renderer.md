# Renderers

*Last updated: 2026-09-10*

> A model transformed into a representation such as text, markup or an image.

## Location

### Folder
- must use `Renderers/` for a role folder under the domain that owns the capability.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- inherited documentation → [behavior](behavior.md) § *Shared rules*.

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Renders**, naming the input model and output representation.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Renderer`.
- contract and implementation prefixes → [constructs](../constructs.md) § *Role and shape*.

---

## Content

- failure modes and carrier selection → [results](../../components/result.md).
- static eligibility → [constructs](../constructs.md) § *Static or instance*.
