# Repositories

*Last updated: 2026-09-10*

> A data-access seam over rows, documents, blobs, caches or files, independent of its storage engine.

## Location

### Folder
- must sit in a `Repositories/` folder under the domain whose data it stores.
- must split reads from writes by **folder** when a repository grows — `Queries/`, `Commands/`.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Accesses**, whichever direction the class runs in.
- must name the data it reaches, never the storage commands it runs.
- must carry `<remarks>` only when a multi-method command class needs a directive.

```csharp
// ✅ names the rows
/// <summary>Accesses OLX external listings that have not been enriched yet.</summary>
// ❌ names the mechanism, which changes without the contract changing
/// <summary>Accesses listings using a Dapper query with a join.</summary>
```

### Construct
- must take the storage collaborator through its constructor → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Repository`, prefixed by the rows it reaches — `OlxListingsRepository`.
- must not suffix a class `Query` / `Command` — those name a [dispatched message](../data/application-request.md).

```csharp
// ✅
public sealed class OlxListingsRepository(IDbConnectionFactory connectionFactory)
// ❌ `Query` names a mediator message, so the same word carries two roles
public sealed class UnenrichedListingsQuery
```

---

## Content

- failure modes and carrier selection → [results](../../components/result.md).
- storage access → [persistence](../../domains/persistence/persistence.md).
