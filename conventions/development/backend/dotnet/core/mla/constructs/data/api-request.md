# Api requests

*Last updated: 2026-09-10*

> The presentation-layer body a client sends, bound by one controller action.
> Purpose — the `Api` qualifier is what tells the wire body apart from the application message it maps to.
> Use case — every endpoint that accepts a body.

## Location

### Folder
- must sit in a `Requests/` folder under the domain the endpoint serves.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- type summary baseline → [data](data.md) § *Shared rules*.
- must name the body it carries.
- must carry no `<remarks>` — a request body directs the consumer to nothing; this overrides
  [remarks](../../../lla/notation/documentation/remarks.md) § *Admission*.

```csharp
// ✅ names the action's body
/// <summary>Represents the create-namespace request body.</summary>
// ❌ names the type instead of the body
/// <summary>Represents an api request.</summary>
```

### Construct
- declaration baseline → [data](data.md) § *Shared rules*.
- must expose the request as `public`.
- must declare `{ get; init; }` — the model binder sets init-only members, so nothing needs `set`.

### Type name
- must be named `{Verb}{Noun}ApiRequest`, verb-first — it exists for one controller action.
- must take the entity as the noun, or the domain when the action spans more than one entity.
- must carry `Api` — never a bare `Request`, and never `Dto`, which is the payload's suffix.
