# Exporters

*Last updated: 2026-09-13*

> Structured data written as a data exchange document, such as CSV or XLSX.

## Location

### Folder
- must use `Exporters/` under the domain that owns the exported data.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- inherited documentation → [behavior](behavior.md) § *Shared rules*.

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Exports**, naming the data and destination format.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Exporter` when producing a data exchange document is the responsibility.
- contract and implementation prefixes → [constructs](../constructs.md) § *Role and shape*.

---

## Content

### Boundary
- must export supplied data; fetching it and coordinating delivery belong to the caller.
- must keep business decisions outside the exporter.
- must state the output format and schema rules, including columns, headers and ordering where applicable.
- must state culture, encoding and empty-input behavior where they affect the exported document.
- use `Exporter` for data exchange documents; general presentation → [renderers](renderer.md).
- shape translation without document output → [mappers](mapper.md).
- input syntax decoding → [parsers](parser.md).

### Destination
- must leave a caller-owned stream open unless ownership transfer is explicit in the contract.
- must document seeking requirements and whether a failed or canceled export can leave partial output.
- must document whether output is streamed or buffered when it affects supported input size.
- must accept cancellation for asynchronous export and document any synchronous phase that cannot observe it.
- failure carriers → [results](../../components/result.md).
