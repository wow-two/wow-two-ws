# Parsers

*Last updated: 2026-09-13*

> A format's text, bytes or stream decoded into structured data.

## Location

### Folder
- must use `Parsers/` under the domain that owns the parsed shape.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- inherited documentation → [behavior](behavior.md) § *Shared rules*.

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Parses**, naming the input format and produced shape.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Parser` when interpreting format syntax is the responsibility.
- contract and implementation prefixes → [constructs](../constructs.md) § *Role and shape*.

---

## Content

### Members
- must keep the operation to decoding the supplied representation.
- may normalize format-specific syntax while producing the parsed shape.
- may implement one format or select among parsers under the same parsing contract.
- must state how automatic format selection handles unknown or ambiguous formats.
- must keep business orchestration and operations on the parsed result outside the parser.
- shape translation without syntax decoding → [mappers](mapper.md).

### Failure
- must document malformed, incomplete and empty-input behavior.
- must declare whether parsing rejects, skips or returns partial data when input contains errors.
- must distinguish invalid input from a valid empty result when callers need that distinction.
- failure carriers and `Parse` / `TryParse` pairs → [results](../../components/result.md) § *Failure*.

### Streams
- must leave a caller-owned stream open unless ownership transfer is explicit in the contract.
- must document stream consumption and any seeking requirements.
- must accept and observe cancellation for asynchronous parsing.
- must document when deferred parsing reads the stream and requires it to remain open.
