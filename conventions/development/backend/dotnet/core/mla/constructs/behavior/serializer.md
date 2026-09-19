# Serializers

*Last updated: 2026-09-14*

> Object data encoded to, or decoded from, a specified representation.

## Location

### Folder
- must use `Serializers/` under the domain that owns the format contract.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- inherited documentation → [behavior](behavior.md) § *Shared rules*.

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Serializes**, naming the data and encoded format.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Serializer` when owning object encoding or decoding under a format contract.
- contract and implementation prefixes → [constructs](../constructs.md) § *Role and shape*.

---

## Content

### Boundary
- may encode and decode under the same format contract.
- must state the supported object shapes and representation, including encoding or content type where relevant.
- must state round-trip guarantees and any loss of data or type information.
- must keep business validation, data retrieval and delivery outside the serializer.
- syntax decoding without an object-serialization contract → [parsers](parser.md).
- display text → [formatters](formatter.md); data exchange documents → [exporters](exporter.md).
- per-type stored-JSON wrappers and options ownership → [stored JSON](../../domains/persistence/stored-json.md).

### Contract
- must document null, empty and malformed input behavior.
- must state how configuration affects the encoded representation and type reconstruction.
- must document caller-owned stream lifetime and consumption when exposing stream operations.
- must observe cancellation where asynchronous operations support it.
- failure carriers → [results](../../components/result.md).
