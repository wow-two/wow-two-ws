# Services

*Last updated: 2026-09-10*

> The fallback behavior component — business logic, orchestration or compute with no narrower role.
> Purpose — every verb that is not another component's is still a named responsibility.
> Use case — when the [role gate](../constructs.md) selects `Service` because no narrower role fits.

## Location

### Folder
- must sit in a `Services/` folder under the domain that owns the work.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Provides**, naming the work it does for its caller.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

```csharp
// ✅ names the work, not the type
/// <summary>Provides channel and pipeline seeding on application startup.</summary>
// ❌ restates the suffix, so the responsibility stays unsaid
/// <summary>Provides the channel service.</summary>
```

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Service`, prefixed by the work — `ChannelsSeedService`.
- must reach for the narrower suffix when one fits — a `Service` that only maps is a `Mapper`.

```csharp
// ✅
public sealed class PipelineConfigService(IPipelineRepository repository)
// ❌ `Manager` names no verb
public sealed class PipelineManager
```

---

## Content

- failure modes and carrier selection → [results](../../components/result.md).
- application payloads → [models](../data/model.md).
