# Validation

*Last updated: 2026-09-12*

> Input validity, phase ordering, and field failures independent of the validation provider.

## Contract

- must use a validator for caller-supplied payloads and an argument guard for programmer preconditions.
- must not run untrusted boundary input through throwing programmer-error guards.
- must keep each validation layer independently correct within its own scope.
- must not assume an outer layer already checked an inner layer's obligations.
- must define a dedicated validator type through the [validator construct](../../constructs/behavior/validator.md).

---

## Placement

- must start data and business validation outside model constructors, including entity and value-object rules; validation can grow independently of construction.
- may use a pure validation extension method for a small rule set; use a dedicated validator as composition, dependencies or rule reporting grow.
- must use the [FluentValidation integration](fluentvalidation/fluentvalidation.md) when authoring dedicated validators.
- must keep rules with the concept they validate; external placement does not transfer ownership to an unrelated storing entity.
- must validate created, copied or deserialized candidate data at the boundary that accepts it for use or persistence.
- must not claim that every constructed instance is already valid when validation is external.
- may enforce data validity in a constructor only as an exceptional, documented type contract; state why external validation is insufficient and how supported copy and deserialization paths preserve that contract.
- must keep programmer argument guards distinct from model data validation; the constructor exception does not prohibit guards for programmer preconditions.

---

## Phases

- must let authentication, media-type handling and syntactic binding complete at the delivery boundary.
- must resolve an existing target and check ownership before authored field validation.
- must return `NotFound` for a well-formed id that resolves to no target.
- must treat existence and permission failures as operation errors, not invented field failures.
- must run static payload constraints through the validator without persistence I/O.
- must apply transition constraints against the resolved prior state on the entity.
- must emit `ValidationError` for a correctable field the caller supplied, including field-specific uniqueness failures.
- must emit an operation `AppError` for stateful failures with no such field.
- must distinguish transitions between valid states from invariants that hold in every state.
- must not let a generic pre-handler validator invert this order for a target-bearing command.
- must not claim resolving in the handler changes validation already run by an interceptor.
- target-free commands may validate in the pipeline; target-bearing commands need the phase-ordering seam below.

---

## Layer independence

- must keep cross-aggregate checks at the layer that can reach the relevant data.
- must retain existence and ownership checks at the service boundary even when a caller resolved the entity.
- may reuse a correctly scoped resolution cache without skipping the check.
- must not treat a check-then-write probe as protection against concurrent conflicting writes.
- database constraints and their error translation remain part of the unresolved lower-pass design.

---

## Consumption

- must depend on the SDK `IValidator<T>` contract, not the concrete validation provider.
- must handle non-null `Validate(T)` output as the validation failure; null denotes valid input.
- may use `ValidateAndThrow(T)` only at a declared throwing boundary.
- must read advisory failures through `Inspect(T)` rather than treating them as write failures.
- must not let an advisory warning block a write; a blocking rule is an error.
- API → [validator contract](../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Validation/IValidator.cs).

---

## Field contract

- must emit a domain member path in `FieldError.Property`.
- must preserve that path through lower layers; delivery maps it when the wire model differs.
- must carry a stable rule code and permitted operands so clients can localize the rule.
- must not expose rejected secret values or secret-derived operands.
- must declare operation-specific sensitive members on the validator.
- must not normalize provider codes into a new wire vocabulary without an explicit contract change.

---

## HTTP

- must return field failures as HTTP `400`, through the shared [problem-details mapping](../../../../shapes/service/platform/responses/problem-details.md).
- must not use `422` merely because the failure is semantic; the service convention chooses `400`.
- must keep missing targets and permission failures on their own status mapping.
- must map result failures at the controller without hand-building field-error responses.
- may expose advisory inspection as a sub-resource such as `POST /codes/validate`.
- must leave frontend field placement to the client; an API changing domain/wire symmetry supplies a path translation.
- message localization → [FluentValidation integration](fluentvalidation/fluentvalidation.md#localization).

---

## Providers

- [FluentValidation](fluentvalidation/fluentvalidation.md) — rule authoring, registration, projection and sensitive operands.

---

## Open

- phase ordering: the current synchronous generic interceptor has no target-resolution/skip seam;
  complete that SDK seam before claiming it enforces the target-bearing phase order.
- lower-pass design: settle service rule sharing, authoritative database constraints and constraint-error translation.
- read seam: settle tracked writes after untracked reads; loading and mutating before `Attach` loses the original snapshot.
- validation scope: the SDK contract has no caller-selected ruleset or asynchronous validation overload.
