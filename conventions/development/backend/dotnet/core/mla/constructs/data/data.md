# Data components

*Last updated: 2026-09-10*

> The component kinds that carry data, with value or entity identity defined by their role.
> Purpose — a data component is inert until something reads it, which is why it is MLA rather than LLA.
> Use case — naming or declaring a type that holds rather than does.

## The kinds

| Kind | Carries |
|---|---|
| [entity](entity.md) | a table-mapped row, owning its identity |
| [value object](value-object.md) | values stored inside a row, owning no identity |
| [dto](dto.md) | a projection onto the wire |
| [api request](api-request.md) | the body one controller action binds |
| [application request](application-request.md) | the message a caller dispatches in-process |
| [result](result.md) | the carrier — a typed success or an `AppError` |
| [model](model.md) | what an operation produced, carried inside the result |
| [constants](constants.md) | the class that owns a value's authority |
| [enums](enums.md) | a closed set of named options we own |
| [settings](settings.md) | the record a configuration section binds into |
| [options](options.md) | the record a caller fills in code, defaults already set |
| [spec](spec.md) | declarative input consumed by behavior |
| [capabilities](capabilities.md) | supported operations, a kind of model |
| [entity configuration](../../domains/persistence/access/ef/entity-configuration.md) | an EF mapping for one entity |

---

## Shared rules

- declaration and documentation baseline →
  [language constructs](../../../lla/constructs/constructs.md) § *Data components*.
- must state its own accessor pair — `init` where nothing writes after construction, `set` where something does.
- must state a role-specific form or starter as an override of that baseline.
- must state role, location and declaration only; shape and flow belong to the domain that uses the type.
