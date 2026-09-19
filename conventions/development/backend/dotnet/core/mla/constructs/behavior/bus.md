# Buses

*Last updated: 2026-09-15*

> Application-facing publishing and sending that delegates delivery to a transport.

## Location

### Folder
- must use `Buses/` under the messaging domain that owns the capability.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- inherited documentation → [behavior](behavior.md) § *Shared rules*.

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Dispatches**, naming the messages and delivery abstraction.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Bus` for the application-facing publish/send responsibility.
- contract and implementation prefixes → [constructs](../constructs.md) § *Role and shape*.

---

## Content

- must accept application messages without requiring callers to construct transport envelopes.
- must prepare delivery metadata and delegate medium-specific delivery to a [transport](transport.md).
- must distinguish publish-to-subscribers from send-to-destination when exposing both operations.
- must keep provider-specific delivery mechanics and message business handling outside the bus.
- must document send/publish completion in terms of the underlying delivery guarantee.
- must not imply durability or completed handler execution merely because a send completed.
- must preserve explicit caller metadata according to the contract and document generated defaults.
- failure carriers → [results](../../components/result.md).
