# Transports

*Last updated: 2026-09-14*

> Sends or receives messages through a selected delivery medium.

## Location

### Folder
- must use `Transports/` under the domain that owns delivery.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- inherited documentation → [behavior](behavior.md) § *Shared rules*.

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Transports**, naming the messages and delivery medium.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Transport` when owning message delivery through a medium.
- may split sending and receiving into separate contracts.
- contract and implementation prefixes → [constructs](../constructs.md) § *Role and shape*.

---

## Content

### Boundary
- must adapt supplied messages and delivery metadata to the selected medium.
- may use an external messaging provider or an in-process channel.
- may delegate encoding, routing and settlement to collaborators.
- must hand received messages to the processing contract without owning their business meaning.
- business message execution → [handlers](handler.md).
- broader external integration roles → [brokers](broker.md).
- application-facing publish/send over a transport → [buses](bus.md).
- workflow orchestration using those delivery contracts → [services](service.md).

### Delivery contract
- must state what send completion guarantees: local acceptance, provider acceptance or confirmed delivery.
- must document supported ordering, durability and redelivery guarantees without assuming stronger ones.
- must expose unsupported capabilities and unroutable-destination behavior explicitly.
- must state resource ownership and start/stop behavior where receiving owns a lifecycle.
- must observe cancellation where supported and document operations that cannot be interrupted.
- failure carriers → [results](../../components/result.md).
