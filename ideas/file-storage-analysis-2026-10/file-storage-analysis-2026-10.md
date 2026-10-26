# File Storage — full analysis before the build

*Last updated: 2026-10-26*

> The analysis batch behind the files domain repo (#3 in [platform apps](../../docs/platform-apps.md)): how many
> services and instance kinds it needs, what products store today, the whole feature vector, the contract, what it
> needs from Identity, how wide the library is, and the icon pack. The [service spec](../file-storage-service-spec.md)
> stays the build source; settled findings move into it, and this folder keeps the evidence.

## Inputs

- spec: [file-storage-service-spec.md](../file-storage-service-spec.md) — D6 and D8 open; D7 decided 2026-10-26.
- identity analysis [T4](../identity-analysis-2026-10/t4-integration-modes.md): File Storage is an API resource (M8),
  takes client-credentials tokens (M10), token exchange later (M11).
- [domain structure](../../conventions/development/repo/structure/domain-structure.md): one repo per domain, packages
  by layer, the spec moves into the repo's `product/product.md`.
- developer, 2026-10-26: its own repo, separate from the be sdk; new libraries leave the sdk one domain at a time,
  bigger domains first.
- developer, 2026-10-26: beside one instance per owner, a second kind — a shared files host on a cheaper or
  storage-fit server that several products point at — to migrate files, and to start a product without a large server.
- developer, 2026-10-26: D7 — public delivery with gates (password, expiry, more); analyse every feature; the whole
  vector goes to the backlog; build what products need now, the rest in parallel after the first release.
- developer, 2026-10-26: an icon pack for every file extension; compression in scope; asked whether one big files
  library should hold the server as one of its parts.
- developer, 2026-10-26: the Identity chat is preparing the domain library template; this batch hands it Files' asks.

---

## Tracks

| # | Track | File | State |
|---|---|---|---|
| T1 | Services, roles and instance kinds (A owner, B shared host), tenant moves | [t1-services-tenancy.md](t1-services-tenancy.md) | ✅ |
| T2 | Feature vector: every capability, phased; sharing gates; compression | [t2-feature-vector.md](t2-feature-vector.md) | ✅ |
| T3 | Consumers: what products store today → the first slice | [t3-consumers.md](t3-consumers.md) | ✅ |
| T4 | Contract: brokers, HTTP API, hosting routes, events, errors | [t4-contract.md](t4-contract.md) | ✅ |
| T5 | Identity: what Files needs; asks for the Identity chat | [t5-identity.md](t5-identity.md) | ✅ |
| T6 | Library shape: one files domain, packages, what stays in core | [t6-library-shape.md](t6-library-shape.md) | ✅ |
| T7 | File icon pack | [t7-file-icons.md](t7-file-icons.md) | ✅ |

---

## Points

The decision queue: parents before children, blocking first. Each line: the question → the pick, and the track
holding the evidence. Tick a line when the developer answers; the answer moves into the spec.

### A · Scope and placement — blocks the repo

- [x] Q1 (developer 2026-10-26) its own domain repo, not a be sdk module
- [ ] Q2 one `files` domain — storage, server, formats, compression, images, documents, video, icons — with
  granular packages → yes (T6)
- [ ] Q3 repo `wow-two-sdk-beta.files`; the empty `wow-two-platform.storage.file` archived by the developer → yes (T6)
- [ ] Q4 core keeps `Storage/` byte adapters, since core's Messaging claim check reads them; Files builds on them → yes (T6)
- [ ] Q5 `Media/Images` and `Media/Pdf` move to Files; Word, Markdown, Captions, Tabular stay in core → yes (T6)
- [ ] Q6 amend domain structure § Scope: a stateless library moves with the domain whose pipeline uses it → yes (T6)

### B · Services and instances

- [ ] Q7 one image, three roles (`api`, `worker`, `delivery`), one process in P1 → yes (T1)
- [ ] Q8 B is the same image in `Tenancy:Mode=Shared`; A is the same with one tenant row → yes (T1)
- [ ] Q9 WoW2's own instance is the first B; Ocharo runs an A → yes (T1)
- [ ] Q10 Form 3 becomes B, hosted off the control host → yes (T1)
- [ ] Q11 tenant moves: signed export bundle + byte copy or bucket re-point; public URLs on the tenant's host → yes (T1)
- [ ] Q12 B's server and byte store fold into D6 → yes (T1)

### C · Features and the first slice

- [ ] Q13 P1 = Ocharo (A) + Harvest captures, Events media, optionally ForeverPin logos (B); the rest to the backlog (T2, T3)
- [ ] Q14 share gates in P1: expiry, password, max downloads, one-time, revoke; sign-in and email gates in P2 (T2)
- [ ] Q15 user content on its own origin (`files.{domain}`) from P1 → yes (T2, T4)
- [ ] Q16 on-the-fly transforms through signed params in P2, own Skia renderer, no imgproxy → yes (T2)
- [ ] Q17 video posters in P2; transcoding and HLS in P3 on a named consumer → yes (T2)
- [ ] Q18 lifecycle expiry and the orphan sweep move to P1 for Harvest → yes (T3)

### D · Contract

- [ ] Q19 one broker set for Module and Client (`IFileUploads`, `IFileStore`, `IFileReferences`, `IFileUrls`,
  `IFileShares`, `IFileTransforms`, `IFileArchives`, `IFileJobs`, `IFileAdmin`) → yes (T4)
- [ ] Q20 `FileId` UUIDv7, instance-independent; storage keys by content hash per tenant → yes (T4)
- [ ] Q21 browsers upload through backend-minted tickets in P1; user tokens with the `files` audience in P2 → yes (T4, T5)
- [ ] Q22 resumable uploads by tus 1.0 (tusdotnet) in P2 → yes (T4)

### E · Identity

- [ ] Q23 Files uses our Identity (M8, M10; M11 in P2) and does not wait for it: P1 runs on existing client-credentials
  and API-key handlers → yes (T5)
- [ ] Q24 hand the T5 § 3 asks (I-1 … I-11) to the Identity chat; I-4 multi-issuer and I-5 API keys are new there → send (T5)

### F · Icons

- [ ] Q25 one generated pack: ~24 kind glyphs + extension label, from one registry shared by be and fe → yes (T7)
- [ ] Q26 no brand logos in P1 → yes (T7)

### Self-served

- ✅ D7 recorded as decided in [platform apps](../../docs/platform-apps.md) § Decisions and removed from platform decisions
- ✅ spec updated with the settled points: own repo, shared host B, D7 scope, compression and icons in scope
- ⬜ `catalog.yml` entry and the platform-apps row renamed once Q2 and Q3 settle
- ⬜ the repo waits for the Identity chat's domain template (`wow-two-sdk-beta.domain-template`)
