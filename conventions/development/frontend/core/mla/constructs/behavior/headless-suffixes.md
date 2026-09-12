# Headless Suffixes

*Last updated: 2026-09-10*

> The keep-list of suffixes that name a **seam** — a role a component consumes and never renders.
> Purpose — a behavioral contract and its implementation share a role that remains meaningful without rendering.
> Use case — declaring an interface, its default implementation, or the options a call takes.

## Rules [REQUIRED]

- must end a seam's name with a suffix from the table below, never with a component suffix
  ([visual kinds](../visual/visual.md) § *Suffix routing*).
- must declare a seam in its capability module — `auth/` · `query/` · `flags/` · `analytics/` · `foundation/`.
- must not declare a seam under `presentation/` — a folder there holds a renderable component and its parts.
- must name a seam for the role, not for its first implementation — the implementation prefixes the role.

```txt
// ✅ the role names the contract; each implementation prefixes it
export interface LogSink { write(entry: LogEntry): void }
export class MemoryLogSink implements LogSink { … }
// ❌ the contract named after the one thing that implements it today
export interface ConsoleLogger { … }
```

---

## Seam suffixes

| Role | Suffix | In the SDK |
|---|---|---|
| supplies one capability behind a contract | `*Provider` | `MemoryAnalyticsProvider` |
| wraps a third-party engine to a house contract | `*Adapter` | `IconAdapter` |
| moves bytes or messages over a wire | `*Transport` | `UploadTransport` |
| terminal write target | `*Sink` | `MemoryLogSink` |
| origin values are read from | `*Source` | `ConfigSource` |
| app-side seam over a client-side resource | `*Broker` | `StorageBroker` |
| talks to exactly one remote service | `*Client` | `ApiClient` |
| in-process publish / subscribe | `*Bus` | `FeedbackBus` |
| name to implementation lookup | `*Registry` | `CommandRegistry` |
| one interchangeable algorithm | `*Strategy` | `BearerStrategy` |
| decides whether and when | `*Policy` | `RetryPolicy` |

- a seam's data shapes — `*Descriptor` · `*Result` · `*Options` — are declared in
  [data](../data/data.md), not here; this keep-list names behavior roles only.
- must keep `*Broker` for a client-side resource seam ([naming](../../../lla/notation/naming/naming.md)).

```ts
// ✅ each suffix carries a different obligation
export interface RetryPolicy { shouldRetry(attempt: number, error: unknown): boolean }
export interface ApiClientOptions { readonly baseUrl: string; readonly retry?: RetryPolicy }
// ❌ Options standing in for a Policy — knobs do not decide, they are read by something that decides
export interface RetryOptions { shouldRetry(attempt: number): boolean }
```

---

## Provider — the shared word

`*Provider` is the one suffix on both keep-lists, and the two roles never live in the same file.

- must declare the **seam** as a `.ts` interface in its capability module — `AnalyticsProvider` · `FlagProvider`.
- must declare the **component** through its framework's provider form ([provider](../visual/provider.md)).
- must not let one file be both — a component installs a seam, it is not the seam.

```txt
✅ src/analytics/AnalyticsProvider.ts     — the seam a consumer implements
✅ src/auth/AuthProvider.vue              — the component that installs a strategy for its subtree
❌ src/presentation/display/FlagProvider.ts   (a seam under presentation/)
```

---

## Neighbours

- [visual kinds](../visual/visual.md) — the kinds that render, and the suffix each one fixes
- [provider](../visual/provider.md) — the component kind that installs a seam for a subtree
- [naming](../../../lla/notation/naming/naming.md) — file, folder, and co-located non-component suffixes
- [state and data](../../domains/data/state-and-data.md) — where the seams these name are wired
