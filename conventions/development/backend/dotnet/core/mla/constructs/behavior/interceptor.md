# Interceptors

*Last updated: 2026-08-25*

> A step a message passes through on its way to its handler.
> Purpose — one word for every position in a chain, so a reader stops guessing what `Behavior` meant.
> Use case — validating a request, authorizing it, opening a scope, recording it, rehydrating its body.

## The line against `Handler`

One question separates them: does the type **handle** the message, or does it sit between the caller and
whatever does?

- must use `Handler` for the type the message was addressed to — it does the work and produces the answer.
- must use `Interceptor` for anything the message passes through first, whatever that step does with it.
- must not read the power a step happens to use as the dividing line — cancelling, filtering, rewriting and
  merely watching are all interception, and a step that only watches is still not the addressee.

---

## Location

### Folder
- must sit in an `Interceptors/` folder under the domain whose chain it joins.

### File
- must give it its own file, named for the type → [one type, one file](../../mla.md).

---

## Declaration

### Type name
- must suffix with `Interceptor`.
- must name **what this step does** in the word before the suffix — `ValidatingInterceptor`,
  `AuthorizingInterceptor`, `ObservingInterceptor`, `TracingInterceptor`.
- must take that word from the step's job, never from the chain it sits in — a step named for its phase
  says where it runs, which the registration already says.
- may carry a phase or transport word further left when two chains hold the same job —
  `ClaimCheckRehydrateConsumeInterceptor`. The suffix stays last, the job stays beside it.
- must not stack a second role word — a step is one thing.

### Contract
- must declare the chain's contract once per chain, named for what passes through it —
  `IRequestInterceptor`, `IConsumeInterceptor`.
- must keep a read-only chain a separate contract from one that can short-circuit, so the power a step has
  is visible in what it implements rather than promised in prose.

---

## Content

- must receive the next step and decide whether to call it — that is what makes it a chain rather than a list.
- must not settle, complete or answer the message itself; that is the handler's, and doing both leaves the
  message settled twice.
- must state its ordering requirement in `<remarks>` when it has one, because registration order is the only
  control the container offers.
- must not depend on another interceptor's presence — a chain a host composes freely cannot promise one.

---

## Neighbours

- [handler](handler.md) — the type the message was addressed to
- [pipelines](../patterns/pipelines.md) — the ordered flow interceptors compose
- [constructs](../constructs.md) § *Folds* — `Behavior`, `Filter` and `Observer` all fold here
