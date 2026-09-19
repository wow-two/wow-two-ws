# Formatters

*Last updated: 2026-09-13*

> Values expressed as display text under culture or format rules.

## Location

### Folder
- must use `Formatters/` under the domain that owns the displayed value.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- inherited documentation → [behavior](behavior.md) § *Shared rules*.

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Formats**, naming the value and resulting display text.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Formatter` when expressing values as formatted display text is the responsibility.
- contract and implementation prefixes → [constructs](../constructs.md) § *Role and shape*.

---

## Content

### Boundary
- may format numbers, dates, quantities or durations, including relative-time phrases.
- may produce humanized text through word inflection, ordinals and counted phrases.
- must retain `Formatter` as the role suffix — `HumanizedTextFormatter` names the humanized-text capability.
- must keep business decisions and data retrieval outside the formatter.
- document, markup or image composition → [renderers](renderer.md).
- data exchange documents → [exporters](exporter.md).
- format syntax decoding → [parsers](parser.md).

### Inputs
- must make the culture source explicit in the contract: argument, configured default or ambient culture.
- must document format defaults and unsupported-format behavior where format selection is exposed.
- must document null and empty-input behavior where those inputs are supported.
- must obtain the current time through the [clock seam](time.md) when producing relative-time text.
- must state time-zone assumptions when they affect the displayed value.
- failure carriers → [results](../../components/result.md).
