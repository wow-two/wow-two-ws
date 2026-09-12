# Options

*Last updated: 2026-09-10*

> The class a caller fills in code to steer a component's behavior; it binds to no configuration section.
> Purpose — an `Add*` extension ships working defaults, so the caller overrides only what differs.
> Use case — any knob supplied through a delegate or a `new`, which is every knob an SDK exposes.

## Location

### Folder
- must sit beside the `Add*` extension that consumes it, under the domain it configures.
- must not take an `Options/` folder — one registration reads the type, and separating the two hides
  which extension owns the knobs.
- must sit in the reading layer's `Settings/` folder in a service, beside its sibling `Settings` records —
  a service declares few `Options` of its own, because a service *is* the host and reads a section instead.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Holds**, and name the behavior the values steer.
- must not name a configuration section — an `Options` binds to none.

```csharp
// ✅ names what the values steer
/// <summary>Holds the casing applied to generated SQL identifiers.</summary>
// ❌ names a section, which this type never has
/// <summary>Holds the SqlNaming settings section.</summary>
```

### Construct
- declaration baseline → [data](data.md) § *Shared rules*.
- must declare `{ get; set; }` — the `Action<T>` idiom assigns each member in turn, and a record carries
  settable members without losing `with` or its value equality.
- defaults → [constructs](../constructs.md) § *`Settings` vs `Options`*.
- required-member enforcement → [constructs](../constructs.md) § *`Settings` vs `Options`*.

### Type name
- must suffix with `Options` — `SqlNamingOptions`, `DbUpOptions`.
- must name the subject configured, never the method that takes it — `SqlNamingOptions`, not
  `AddDapperConventionsOptions`.

---

## Against `Settings`

Which of the two a type is → [constructs](../constructs.md) § *`Settings` vs `Options`*. The origin decides
the suffix, and the suffix decides the rest:

| | `Options` | `Settings` |
|---|---|---|
| Filled by | the caller's delegate, after construction | the binder, at startup |
| Members | `{ get; set; }` | `{ get; init; }` |
| Defaults | on every omittable member, both alike | same |
| A must-supply member | `required`, taken as an `Add*` parameter | `required`, named in the section |
| `required` enforced by | validation — `Activator` bypasses it | validation — the binder bypasses it |

- must rename the type when its values move between caller code and configuration binding.
- must take its new accessor shape from the destination role; shared default rules still apply.

---

## Neighbours

- [options](../../components/options.md) — the delegate, registration, and member docs
- [settings](settings.md) — the same values once configuration supplies them
