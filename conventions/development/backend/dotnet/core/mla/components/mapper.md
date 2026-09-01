# Mappers

*Last updated: 2026-08-24*

> The type that turns one shape into another and does nothing else.
> Purpose — a translation lives outside both shapes, so neither side learns about the other.
> Use case — an entity becoming a DTO, a token becoming a type, a case style becoming another.

> Defined at [mappers — the construct](../constructs/behavior/mapper.md); this doc carries every condition for using one.

## Reaching for one

- must reach here when the data arrives as an argument and the output is a function of it — pure, no
  injection, no I/O, nothing stored.
- must reach for a [`Service`](../constructs/behavior/service.md) instead once the transform needs an
  injected collaborator, and for a [`Broker`](../constructs/behavior/broker.md) once it needs I/O.
- must reach for a [`Factory`](../constructs/patterns/factories.md) instead when the output type is the
  point and the arguments are ingredients that were never one shape.
- must not reach here for a rule that decides *whether* to do something — a predicate over policy is a
  `Policy`, not a translation.

---

## Static or instance

Both gates in [constructs](../constructs/constructs.md) § *Static or instance* apply.

- must declare a `static class` only when the transform is arrangement and exactly one variant exists —
  a case style, a topic name, a header table.
- must declare an instance type when the transform is a real algorithm, or when the operation names a
  family a caller could pick from, so the choice is made at registration.
- must not read purity as a licence for `static` — a pure type with two variants still goes instance.

---

## Members

- must take everything it needs as arguments, so the same inputs always give the same output.
- must name the method for the target, not the source — `ToSnakeCase`, `ToDto`, `ToTypeToken`.
- must return a new instance and leave every argument untouched.
- must not overload on the source type alone; a second source shape is a second method with its own name.
- must not hold a field that outlives a call — no cache, no counter, no last-value.

---

## Failure

- must return a [`Result`](result.md) when the input can be unmappable and the caller can act on it — an
  unparseable token, a payload that will not decode.
- must throw an argument guard for a programmer error, such as a null argument.
- must not return a default or a null to signal an unmappable input; that hides the failure at every call site.

---

## Registration

- must register an instance mapper against its contract in the owning domain's `Add*` extension.
- must not register a `static class` — it has no seam and needs none.
- must not resolve a mapper from the container inside another mapper; a mapper that needs a collaborator
  is a `Service`.

---

## Neighbours

- [mappers — the construct](../constructs/behavior/mapper.md) — what it is and how it is declared
- [constructs](../constructs/constructs.md) § *`Factory` vs `Mapper`* — which end the caller cares about
- [result](result.md) — what an unmappable input hands back
