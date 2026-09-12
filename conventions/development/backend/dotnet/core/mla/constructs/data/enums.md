# Enums

*Last updated: 2026-09-10*

> A closed set of named options we own — the values a field may hold, fixed at compile time.
> Purpose — a magic value carries no meaning and no compiler check; the name carries both.
> Use case — any field whose value comes from a fixed, known set that we, not a third party, decide.

## Location

### Folder
- must sit in an `Enums/` folder under the domain that owns the set.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Refers to**, and name the thing the set classifies.
- must not list the members in the type summary — each member documents itself.

```csharp
// ✅ names what is classified
/// <summary>Refers to the way a code resolves its destination.</summary>
// ❌ lists members, so the summary drifts on every addition
/// <summary>Static, dynamic or geo.</summary>
```

### Construct
- must declare an `enum` → [constructs](../../../lla/constructs/constructs.md) § *Data components*.
- must leave the underlying type implicit unless a store or wire format fixes it.
- must not declare a `[Flags]` set unless the values genuinely combine.

### Type name
- must be singular — `ChannelType`, never `ChannelTypes`.
- must carry the domain noun and nothing else — never an `Enum` suffix.
- must not name the storage — `CodeStatus`, never `CodeStatusColumn`.

---

## Neighbours

- [enums](../../components/enums.md) — members, attributes, and how a store maps one
