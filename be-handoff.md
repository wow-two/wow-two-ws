# Handoff — backend SDK conventions sweep

> Current continuation: [conventions sweep and remaining decisions](system/sessions/backend-beta-build/conventions-audit.md).
> Resolve the conventions before resuming SDK implementation. The historical status below is not the current baseline.

*Last updated: 2026-08-25*

> Historical handoff, retained for the settled decisions and the reasoning behind disputed names.
> Active work and counts belong to the linked audit and the SDK's `be-convention-sweep.md`.

## Historical state — 2026-08-25

`wow-two-sdk.backend.beta` — **332 tests passing, 0 failing**, build green, 978 source files.

| Suite | Passing |
|---|---|
| `Data` · `Foundation` · `Identity` | 20 · 94 · 2 |
| `Mediator` · `Messaging` | 68 · 96 (+1 skipped) |
| `Migrations` · `Web` | 14 · 38 |

Committed and pushed through `1efbab3` (SDK) and `770f49e` (`wow-two-ws`). The SDK tree carries **10
uncommitted files** and `wow-two-ws` **13** — the work below the commit line is this session's tail
(the options seam, `C8`, the sweep file) plus another lane's frontend edits in `wow-two-ws`. Stage the
backend lane only; the `fe-*` docs and `conventions/development/frontend/` belong to another chat.

Sweep file: `wow-two-sdk.backend.beta/be-convention-sweep.md` — **6 rows open**, 58 shipped, 4 refuted.
The 31 product rows moved to `smart-qr-poc/smartqr-be-update.md` on 2026-08-25; this file measures the SDK.

---

## Historical remainder — 2026-08-25

### Three rows that are notes, not work

Each records a settled fact and needs only its ✅ and a one-line landed narrative.

- `N10` — the rename became moot: `ValidationResult` no longer exists.
- `N57` — `AzureServiceBusOptions.ConnectionString` keeps its placeholder, because the type stays on
  `AddOptions<T>()` for a `PostConfigure` chain that cannot construct a `required` member.
- `N93` — the `Scheduler` fold row was split (`BackgroundService` for a timer, `Service` for a caller)
  and the code already landed on it.

### Two rows that are real work

- **`N24`** — ship a JSON serializer holding its options in a type-keyed dictionary, so products stop
  declaring their own. `N25` re-tests the `Json` keep-list row once it lands, since that suffix's only
  claim was pinning options.
- **`R8`** — add `Result<TSuccess, TFailure>`. A caller cannot branch exhaustively on `AppError` today.
  Rides with the deferred status-enum idea below.

### Four disputed names

`N34` landed 19 of 29. The battery still reports these, and each carries a live counter-argument from the
challenge round — do not apply the first verdict without re-reading the dispute.

| Type | Verdict | Counter |
|---|---|---|
| `IMasterKeyProvider` + `EnvironmentMasterKeyProvider` | `Repository` | `Service` — it fails five of `repository.md`'s own checks |
| `ClaimProviderProfile` | `Options` | `Spec` — it is positional and init-only, which `options.md` forbids |
| `UserAccountManager` | `Service` | `Repository` — the how-stored knowledge does not sit behind `IUserRepository` |
| `IAuditCurrentUserAccessor` | `Service` | `ICurrentUserService`, moved to `Data/Abstractions/` — `Identity/CurrentUser/ICurrentUser.cs` already holds this role under a second name |

`DatabaseProvider` is an enum and the fold does not reach it; a counter argues the noun should be
`DatabaseEngine` anyway. That one is a naming call, not a fold.

---

## Decisions not to relitigate

- **`Interceptor` and `Handler` are the whole vocabulary.** A `Handler` is the type the message was
  addressed to; an `Interceptor` is any step it passes through first, whatever that step does. The job
  goes in the middle word — `ValidatingInterceptor`, `IConsumeObservingInterceptor`. `Behavior`, `Filter`
  and `Observer` all fold there; a framework-owned name stays exempt.
- **`Observer` was refuted as a keep-list role**, 3 of 3 refuters. It names a position and a permission,
  never a verb, so § *Adding a new suffix* returns `Service` at its own gate.
- **A consumer never gates an SDK fix** — `dev-cycle.md` § of that name. Breaking a consumer is not a
  reason to keep a shape the conventions reject.
- **No decision log in code.** `inline.md` § *Exclusions* bans refactor narration, rationale essays, and
  defending a rejected shape — including the positively-restated form (`// X, not Y`).
- **A lone implementation takes the bare role name** (`constructs.md:132`), so every `Default…` prefix
  went.
- **The mediator returns a `Result` by default.** `AddMediator` registers `ExceptionMappingInterceptor`
  first, so it is outermost by construction; `AddMediator(o => o.ExceptionToResult = false)` opts out.
  Ten paths still throw legitimately, all pre-pipeline or the throw-return bridge.

---

## Deferred, with a reason

- **A status enum keyed to HTTP.** `AppErrorType` keys the mapping today. The idea is to replace it with
  our own status vocabulary. Deferred deliberately; `results.md:75` was scoped rather than dropped.
- **Elastic pipeline steps** — `wow-two-sdk.backend.beta/engineering/planning/messaging/elastic-pipeline-steps.md`.
  A pipeline whose steps switch between a direct call and a queue so one slow step scales alone. Idea only,
  with its costs written down: the flow turns asynchronous, so a step may flip only if it is idempotent,
  order-free and serializable — which no contract can declare yet.

---

## Raised as tasks

In `10x-ws/system/planning/pln-tasks.md`, Career section:

- `car-t-014` — a startup failure log channel, for a failure before the pipeline exists (DI resolution,
  options binding, third-party probes). Rides with `car-t-008` and `car-t-013`.
- `car-t-013` — one registration mechanism for `Options` and `Settings`. **Largely delivered** this
  session as `AddValidatedOptions` / `AddValidatedSettings`; re-read before treating it as open.
- `car-t-012` — ProblemDetails creation behind an interface.
- `car-t-011` — the diagnostics construct doc.

---

## Working agreements

- **Proceed without asking** when the next step needs no decision. Batching, ordering and mechanical
  follow-through are not forks. Reserve the chat for a real one.
- **Refine in the chat, store settled points in the doc.**
- **Agents stage and commit; the developer publishes.** `git push` never.
- **Three repos, three commits** — `wow-two-ws`, `wow-two-sdk.backend.beta`, and any product repo each
  commit from inside their own tree. `workbench/` is gitignored by `wow-two-ws`.
- **Verify by measurement, not by reading.** Every row here was closed against a re-run of
  `engineering/planning/sweep.sh` plus `dotnet build` and `dotnet test`, never against a claim.
- **Agent passes cost content.** Three doc-rewrite passes converged 206 → 48 → 33 findings, and the third
  dropped caller-facing facts to satisfy the cap. Stop the loop when the fix rate inverts and finish by hand.
