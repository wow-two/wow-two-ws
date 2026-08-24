# State & data

*Last updated: 2026-08-24*

> How the app reaches its API, where shared state is allowed to live, and how a mutation reconciles.
> Purpose — a cache written from the input rather than the response shows state the server never confirmed.
> Use case — wiring a query or a mutation, or deciding whether a value belongs in the cache at all.

## API client — same-origin `/api`

- must call the API with relative URLs (`/api/...`) — the SPA is served from the .NET host's `wwwroot` in
  production, so there is no base-URL config and no CORS.
- must keep the same origin true in dev through the app's proxy, never a base-URL branch — the proxy target,
  its certificate and its port are [dev server](../../../../shapes/app/platform/dev-server.md) § *The `/api` proxy*.

---

## Client shape

A thin `fetch` wrapper in `src/api/`:

- **`client.ts`** — `request<T>()` helper + an `api` object of typed methods (`getStatus`, `listServers`, …);
  each method documents its route: `/** GET /api/servers — all registered servers. */`.
- **`types.ts`** — request/response DTOs + `ProblemDetails` (RFC 7807).
- must return a `Result<T>` from every method — a non-2xx and a network failure (status `0`) both come back
  as a failure the caller branches on, never as a throw ([result](../../constructs/data/result.md)).
- must map the failure to an `AppError`, carrying the status and the parsed `ProblemDetails` in `metadata`.
- must handle `204` / empty bodies (return `undefined as T`), and set `Accept: application/json` and
  `Content-Type` only when there is a body.
- consumes the backend `ApiResponse<T>` success envelope
  ([api messages](../../../../../backend/dotnet/core/mla/domains/api/api-messages.md)) and its `Problem()` error shape
  ([problem details](../../../../../backend/dotnet/shapes/service/platform/responses/problem-details.md)).

```ts
/** Maps a non-2xx or transport failure to the app's failure type. */
function toAppError(status: number, problem: ProblemDetails | null): AppError;

const result = await api.listServers();                  // Result<ReadonlyArray<ServerDto>>
if (isFail(result)) return renderFailure(result.failure);
```

---

## State management

| Concern | Choice |
|---|---|
| Local UI state | `useState` / `useReducer` |
| Shared app state | **React Context + hooks** — no Redux/Zustand |
| **Server-state** | **TanStack Query** behind a `use{Resource}` hook returning a `Result`; not for UI state |
| Persistence | `localStorage`, namespaced key `{brand}:{app}:{feature}` |
| View routing | the `createAppRouter` data router ([routing](../../../../shapes/app/routing/routing.md)) |

- **server-state vs UI-state** — Query holds only cached copies of what the server owns (lists, entities, their
  loading/error, pagination, poll). Everything else stays `useState` / Context: form inputs and drafts,
  toggles, open-closed, selection, theme, and client-process state (a batch runner's jobs/ticker). The test:
  *would it survive a reload by re-fetching from the server?* → Query; else local.
- must fetch inside hooks, not components ([hooks](../../constructs/behavior/hooks.md)); abort on unmount with
  `AbortController`.
- must map DTO → domain model at the hook boundary ([models](../../constructs/data/models.md)); never leak a
  raw DTO into the view tree.

---

## Mutations — passive only (no optimistic updates)

- must reflect **only the backend-confirmed result** — never pre-write the cache from the mutation input, and
  never roll back.
- must reconcile the cache on **success** from the server's returned value (`invalidateQueries`, or
  `setQueryData` with the response); the UI updates to confirmed state.
- must leave the cache untouched on **failure** — the UI already shows the correct prior state — and surface
  the returned `AppError`.
- the SDK `useAppMutation` wrapper has **no `onMutate` seam**, so an optimistic update is not expressible; a
  mutation never auto-retries.

---

## Query layer

- must read what ships today in the SDK repo's `engineering/planning/capability-ledger.md`
  — a surface register lives beside its code, never in a convention.
