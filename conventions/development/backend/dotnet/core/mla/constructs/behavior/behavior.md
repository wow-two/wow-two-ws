# Behavior components

*Last updated: 2026-09-10*

> The component kinds whose identity is what they do.
> Purpose — one suffix per verb, so a name carries the responsibility rather than the shape.
> Use case — naming or declaring a type that acts rather than holds.

## The kinds

| Kind | Does |
|---|---|
| [service](service.md) | business logic and orchestration — the fallback when no narrower role fits |
| [repository](repository.md) | reads and persists rows |
| [client](client.md) | calls one external provider in its own vocabulary |
| [broker](broker.md) | presents our vocabulary over an external dependency |
| [adapter](adapter.md) | fits a third-party type to an interface we declared |
| [handler](handler.md) | receives one dispatched message |
| [controller](controller.md) | dispatches at the HTTP edge |
| [validator](validator.md) | validates one request |
| [mapper](mapper.md) | transforms an input it is handed |
| [registry](registry.md) | owns key → type bindings registered at composition |
| [policy](policy.md) | decides whether, when or how often another operation runs |
| [builder](builder.md) | accumulates one value, ending in `Build()` |
| [background service](background-service.md) | runs work off the request path |
| [extensions](extensions.md) | static logic over a domain — no injection, no state |
| [time](time.md) | our seam over the clock |
| [json](json.md) | one type's storage seam |
| [interceptor](interceptor.md) | observes or controls a message in a chain |
| [tracker](tracker.md) | live operational state updated by producers and persisted nowhere |
| [renderer](renderer.md) | a model transformed into a representation such as text, markup or an image |
| [generator](generator.md) | a value derived or created from inputs, such as an identifier, code or matrix |
| [rasterizer](rasterizer.md) | a vector representation converted into pixels |
| [cipher](cipher.md) | encryption and decryption under a cryptographic contract |
| [hasher](hasher.md) | a digest computed from input under a hashing contract |
| [issuer](issuer.md) | an authentication artifact issued under an identity contract |
| [authenticator](authenticator.md) | evidence checked to establish an authenticated identity |

---

## Shared rules

- declaration and collaborator baseline →
  [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.
- must take them through a **primary constructor** — the parameter list is the dependency list, and a
  hand-written constructor that only assigns fields repeats it.
- must never assign to a primary-constructor parameter — the capture field the compiler synthesizes is not
  `readonly`, so the type's graph is fixed by this rule rather than by the compiler.
- must declare a `private readonly` field when an explicit constructor is written instead — the case is a
  constructor doing real work, never a plain assignment.
- must expose a collaborator to a derived type as a `protected readonly` field, never `internal` and never
  writable — a base class hands down what it holds, and nothing else may rebind it.
- must not reach for inheritance to share a collaborator — a derived type that only needs the dependency
  takes it through its own primary constructor and passes it up.
- type and member documentation →
  [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

- body layout → [style](../../../lla/notation/style/style.md) § *The body*.
