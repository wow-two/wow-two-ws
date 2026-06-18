# wow-two — Workspace Planning

*Last updated: 2026-06-17*

> Cross-cutting work that spans repos — **SDK** (`wow-two-sdk-beta.backend.beta`) extracts + **conventions**.
> App-specific tasks live in each app's `engineering/planning/backlog.md`, not here.
> Shape: the [engineering-planning convention](../conventions/planning/engineering-planning/engineering-planning-conventions.md), minus `Versions` (the workspace isn't a versioned product).

## Decisions

| Decision | Rationale |
|---|---|
| Actor / caller-context **rides the message** (inputs-on-message); sourced at the edge, never read in the handler | replay · audit · transport-agnostic — the message is the complete intent |
| Presentation request = `{Verb}{Noun}ApiRequest` (body-only); message = `{Noun}{Verb}Command`/`Query`; map via `ToCommand(callerContext, id)` at the edge | one layer boundary, no field leakage; `Api` marks presentation, never `Dto` (response) or bare `Request` |
| `FailureCategory` extended per-app now (smart-qr `+402`, secrets-vault `+503`) | unblock products; bake the **union** into the canonical SDK enum at extract |
| Response payload is always `{Entity}Dto`; `Response` is the `ApiResponse<T>` envelope's word only | kills the `MeResponse` vs `CodeDto` confusion |

## Backlog

Ordered, top = next. Type: `feature` · `issue` · `check` · `idea`.

### Conventions

| Item | Type | Notes |
|---|---|---|
| `request-models.md` + `response-models.md` + doc-format pattern | feature | presentation-layer closure (in progress) |
| Dto-vs-`Response` cleanup | issue | convention states it; renaming `MeResponse`→`{X}Dto` is a per-app task |
| domain-first example rename in `controllers.md` | issue | examples are verb-first; `mediator.md` mandates domain-first |
| adopt the doc-format pattern across all convention docs | check | keyword · ✅/❌ · sparing `MUST`/`SHOULD` |

### → beta SDK (`wow-two-sdk-beta.backend.beta`)

| Item | Type | Notes |
|---|---|---|
| `IClock` + `DateTimeOffset` clock → `Foundation.Time` | feature | adopt = pure delete in products (decided) |
| `FailureCategory` union (`+402` / `+503`) → canonical enum | feature | bake at extract time |
| `ApiResponse<T>` envelope → `Web.Contracts` | feature | products delete the inline copy |
| `ToCommand` / `ApiRequest` support (source-gen mapper? base type?) | idea | evaluate once the convention is adopted in apps |
| remaining v0.2 extract items (13-item list) | feature | detail in drydock `engineering/planning/backlog.md` |

## Log

- **2026-06-17:** workspace planning created — scope: SDK extracts + conventions (apps tracked per-repo). Presentation-layer convention pass underway.
