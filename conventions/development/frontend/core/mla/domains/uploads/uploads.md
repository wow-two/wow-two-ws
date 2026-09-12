# Uploads

*Last updated: 2026-09-10*

> Admission, scheduling and progress for a queue of files, over a transport seam the consumer implements.
> Purpose — the queue owns scheduling; how a byte reaches a server stays a decision the consumer makes.
> Use case — wiring a drop zone, capping concurrency, or pointing the queue at a different upload API.

## The contract

- must never throw at the caller — a rejected file, a failing transport and a cancel are all item statuses.
- must screen an admitted file against the accept list and the size cap up front.
- must still give a rejected file an id and a reason, so the caller can render why.
- must own scheduling only; the transport seam decides how bytes travel.
- must cap uploads in flight, clamping a configured concurrency below one back up.
- must hold a slot through a backoff wait — freeing it lets failing files spawn unbounded waiters.
- must take retry timing from the shared resilience primitives, so an upload backs off like every other request.
- must never retry a cancelled item; retrying a cancel makes the button lie.
- must refuse to retry a file rejected up front — re-sending it cannot change the verdict.
- must normalize progress on the ratio the transport reports, since a multipart body exceeds the file.
- must expose a monotonic version as the subscribed cursor; an item list is a fresh array per call.
- must notify on every mutation, progress included — throttling is the listener's job, not the queue's.
- must ignore a late write for a removed item, so a deleted row never resurrects.
- must return a disposer from a subscription ([hooks](../../constructs/behavior/hooks.md) § *Lifecycle rules*).

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| xhr | a multipart body reporting real upload progress | the default — a progress bar needs body progress |
| any transport | the transport seam over a presigned PUT or tus | the upload API is not a plain multipart post |

---

```txt
✅ createUploadQueue({ transport, accept: 'image/*', maxSize })
✅ queue.add(files)                       an oversized file returns as a failed item
❌ try { queue.add(files) } catch { … }    add never throws; read the item's rejection
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [data](../data/state-and-data.md) — the retry primitives and error coercion shared with requests
- [feedback](../feedback/feedback.md) — where a finished or failed upload is reported to the user
- [field](../../constructs/visual/field.md) — the control kind a queue is bound to

---

## Ownership

- must follow [security](../security/security.md#data) for server admission and retry authority.
- must treat unknown total progress as indeterminate; a ratio exists only when a meaningful total is known.
- must release file references, object URLs and transport resources on removal/disposal.
- must follow [domain lifetime](../domains.md#lifetime) for cancellation and late completions.
