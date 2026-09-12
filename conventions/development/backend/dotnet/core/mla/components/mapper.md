# Mappers

*Last updated: 2026-09-10*

> Applying the [mapper construct](../constructs/behavior/mapper.md) to pure transformations.

## Location

- must use the construct's [location](../constructs/behavior/mapper.md#location).

---

## Declaration

- must use the construct's [declaration](../constructs/behavior/mapper.md#declaration).
- must apply the [static-or-instance gates](../constructs/constructs.md#static-or-instance).

---

## Content

- must choose a mapper when output depends only on arguments, with no I/O or injected collaborator.
- must choose a service when orchestration needs collaborators, or a broker when it reaches an external system.
- must choose a factory when constructing the output type is the purpose and inputs are separate ingredients.
- must choose a policy for a decision governing whether another operation should run.
- must name a method for its target — `ToSnakeCase`, `ToDto`, `ToTypeToken`.
- must leave its arguments unchanged.
- must not overload solely on the source shape when that hides a different mapping contract.
- must not retain a cache, counter or last value between calls.
- must apply the [result failure policy](result.md#failure) to unmappable inputs and argument guards.
- must treat a failure result as an explicit output; totality does not mean every input succeeds.

---

## Registration

- must register an instance mapper against its contract in the owning domain's registration.
- must not register a static mapper.
- must not resolve collaborators through the container inside a mapper.
