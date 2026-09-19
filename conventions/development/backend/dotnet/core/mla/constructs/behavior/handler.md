# Handlers

*Last updated: 2026-09-13*

> The single receiver bound to one dispatched message.
> Purpose — the use case lives in one type, reachable without its caller knowing it.
> Use case — every `Command`, `Query` and `Event` that reaches a handler.

## Location

### Folder
- must sit in a `CommandHandlers/`, `QueryHandlers/` or `EventHandlers/` folder, one per message kind,
  beside the matching `Commands/` · `Queries/` · `Events/` folder.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Handles**, and `<see cref>` the message it takes.
- interface starter → [language constructs](../../../lla/constructs/constructs.md#type-documentation).

```csharp
// ✅ names the message it is bound to
/// <summary>Handles <see cref="ChannelGetAllQuery"/>.</summary>
// ❌ describes the work instead of the binding
/// <summary>Gets every channel from the database.</summary>
```

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.
- must put the dispatched input on the message.

### Type name
- must suffix with `Handler` and name it for its message — `ChannelGetAllQueryHandler`.

```csharp
// ✅
public sealed class ChannelGetAllQueryHandler(IChannelRepository repository)
// ❌ named for the work, so its message is unfindable
public sealed class ChannelReader
```

---

## Content

- response contract → [service results](../../../../shapes/service/platform/responses/results.md).
- application payloads → [models](../data/model.md).
- request composition and shared services → [dispatch](../../domains/messaging/messaging.md#dispatch).
