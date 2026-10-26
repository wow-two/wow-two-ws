# WoW Two Files — Own File Storage for Every Product

*Last updated: 2026-10-26*

> One way to store, transform, compress, protect, share and serve files, shipped in the three
> [capability forms](../conventions/development/capability-forms.md) from its own domain repo. Products stop writing
> their own `MediaStore`.
>
> **Status:** the developer chose to build it on 2026-10-21; first consumer Ocharo. Its own repo, separate from the be
> sdk, and D7 decided 2026-10-26. Open: [platform decisions](../docs/platform-decisions.md) D6, D8. Pre-build analysis
> and its decision queue: [file storage analysis](file-storage-analysis-2026-10/file-storage-analysis-2026-10.md).

## Problem

- Ocharo stores files five ways: Desk in PostgreSQL `bytea` (media, exports, sourcing up to 64 MiB), Catalogue and
  Brand in SQLite plus `App_Data/blobs`, Blog and Marketing in their own blob folders, Studio as strings inside
  state JSON, Assets in Git LFS.
- the same `MediaStore` (content-hash paths, WebP previews) is copied into Catalogue, Brand and Blog; limits differ
  per copy (15, 20, 30 MB) and Desk repeats Catalogue's limits.
- nothing has file metadata, quotas, scanning, signed downloads or a CDN; Desk serves every file through the API.
- across WoW2 only ListingShelf (local `photos/`) and TranscriptForge (2 GB uploads) store files; no product uses the
  SDK `Storage/` module yet.

---

## Placement

- **Form 1 · library** — the files module over the be sdk's `Storage/` byte adapters, plus the fe upload kit; for one
  product with files in its own bucket.
- **Form 2 · self-hosted service** — the module hosted with an API and an admin console, as one image; for one
  owner's apps.
- **Form 3 · provided service** — the shared files host below: the same image, run by us off the control host.

- decided 2026-10-26: File Storage lives in its own domain repo, separate from the be sdk, per
  [domain structure](../conventions/development/repo/structure/domain-structure.md); new libraries leave the sdk one
  domain at a time, bigger ones first.
- confirmed 2026-10-26: one files domain — storage, server, formats, compression, images, documents, video, icons —
  in one repo of granular packages: `wow-two-sdk-beta.files`, named 2026-10-26. Core keeps `Storage/` byte
  adapters, which its Messaging claim check reads; `Media/Images` and `Media/Pdf` move in
  ([T6](file-storage-analysis-2026-10/t6-library-shape.md)).
- the repo `wow-two-platform.storage.file` holds only an empty 2024 solution.
- every form authorizes with [Identity](identity-service-spec.md) claims: organization, app and role.

### Instances per owner

Decided 2026-10-25: one instance per owner, shared by that owner's services.

- WoW2's own instance belongs to the WoW2 apps: Harvest's captures and the [Events](events-service-spec.md) catalogs'
  media live there.
- Ocharo's media — products, brand, uploads, its files about events — starts as a tenant on the shared files host
  (2026-10-26) and moves to Ocharo's own instance later.
- a self-hosted Harvest and Events ship with a File Storage instance in the same bundle, split the same way.
- a record that uses a file holds a reference; the file lives while any reference does, so pruning a capture never
  removes a published image, and nothing is copied between services of one owner.

### Shared files host

Decided 2026-10-26: beside the per-owner instances, a shared files host runs the same image, or nearly the same, for
many products at once, on a cheaper or storage-fit server.

- a product points at it by configuration and keeps only file ids: no bucket, storage code or large server of its own.
- it carries file migrations: from legacy stores, and between instances as a product grows or shrinks.
- confirmed 2026-10-26: one image with three roles (`api`, `worker`, `delivery`), one process in P1; the shared
  host runs it in `Shared` tenancy mode, an owner's instance in `Single` mode with one tenant row.
- WoW2's own instance is the first shared host; Ocharo starts on it too.
- a tenant moves between instances by a signed export bundle plus a byte copy or a bucket re-point; public URLs sit
  on the tenant's own hostname, so a move is a DNS change.
- its server and byte store fold into D6.
- design: analysis [T1](file-storage-analysis-2026-10/t1-services-tenancy.md).

---

## What already exists

- be SDK `Storage/`: `IBlobRepository` (save, read, exists, delete, info, list) over the local file system,
  S3-compatible (MinIO, R2, any `ServiceUrl`) and Azure Blob; tested against s3mock and Azurite.
- signed URLs through `IBlobUrlIssuer`: S3 presign, Azure SAS, or HMAC routes in `Transfer/` (100 MB uploads).
- be SDK `Media/Images/SkiaImageService.cs`: probe, resize, crop, watermark, collage, EXIF, BlurHash, perceptual hash.
- fe SDK: `filePicker`, `fileUploadPicker`, `imageCropEditor`, `imageEditor`, `imagePreview`, an upload queue with
  multipart POST; `forms/fileUpload` is empty.
- Ocharo's proposal (`ocharo-platform/engineering/research/desk/2026-10-09-media-storage-strategy.md`): one private
  media capability, metadata in PostgreSQL, bytes through the WoW2 blob abstraction, API-proxied uploads first,
  short-lived signed URLs. This spec adopts it.

---

## Features

P1 is the Ocharo slice; P2 completes the vector; P3 waits on a named consumer.

### Store

- a `files` table: id, organization, app, owner, name, content type, size, SHA-256, visibility, state, timestamps (P1).
- content-hash keys `{org}/{sha[..2]}/{sha}`; dedup within an organization, never across (P1).
- references and orphan collection: a file lives while a record points at it (P1, for Harvest's pruning).
- lifecycle expiry after N days (P1).
- soft delete with a retention window, then purge (P1).
- versioning of a named file (P2); legal hold (P3).

### Upload

- API-proxied upload with size, type and magic-byte checks per app policy (P1).
- direct presigned PUT for large files, completed by a server-side check (P2).
- resumable uploads (tus) for GLB, video and ZIP over 100 MB (P2).
- malware scan through a ClamAV sidecar before a file turns `ready` (P2).

### Transform

- image variants on upload: thumbnail, preview, WebP; sizes per app policy, replacing each app's preview code (P1).
- EXIF strip on public images, BlurHash for placeholders (P1).
- PDF page images, video poster frames, AVIF (P2); background removal through Desk's worker as a variant (P2).
- on-the-fly transforms through signed URL parameters on our own renderer (P2); video transcoding on a named
  consumer (P3).

### Serve

- private by default: short-lived signed URLs, checked against the caller's organization and role (P1).
- user content on its own origin, `files.{domain}`, never on an app's host (P1).
- public files (catalogue and blog images) on immutable `/media/{sha}` URLs with year-long caching (P1).
- a CDN in front of public files (P2); image resizing at the edge (P3).
- range requests for video and large downloads (P1).

### Share

Decided 2026-10-26 (D7): files go out publicly, through share links behind gates.

- P1 gates: expiry, password, download limits, one-time links, revoke.
- P2 gates: sign-in and email; further gates in the [feature vector](file-storage-analysis-2026-10/t2-feature-vector.md) § 9.
- a share page per link with preview and download-all as ZIP.

### Compress and recognize

- compression and archives in scope: streamed ZIP downloads, archive creation and extraction with bomb guards.
- one registry of file types — extensions, MIME types, magic bytes — drives type checks and an icon pack covering
  every extension ([T7](file-storage-analysis-2026-10/t7-file-icons.md)).

### Limits and admin

- quotas per organization and app; a usage figure on every upload response (P2).
- console: usage by app and organization, largest files, recent uploads, orphans, failed scans, a file browser
  with preview and download audit (P1 usage and browser, P2 the rest).
- an audit row for every upload, delete and private download (P1).

### Developer surface

- be SDK files client: upload, attach to a record, get a signed URL, delete; one broker set for every form (P1),
  per the [contract](file-storage-analysis-2026-10/t4-contract.md).
- browsers upload and download through tickets and signed URLs their backend mints (P1).
- Identity: Files validates its tokens offline, takes client-credentials calls and later token exchange; the
  contracts are [T8](file-storage-analysis-2026-10/t8-identity-contracts.md).
- fe SDK upload kit: `fileUpload` with progress, retry and cancel; image crop before upload (exists) (P1).

---

## Backing store

- development and tests — the local file system adapter.
- hosted, recommended — Contabo Object Storage: S3-compatible, same provider as the products host, about
  €2.49 per 250 GB a month with no transfer fees; public files are rate-limited to 250 requests a second each.
- hosted, alternative — Cloudflare R2: no egress fees, a managed CDN beside it.
- self-hosted on the VPS — SeaweedFS (Apache-2.0) if bytes must stay on our disk; not MinIO, whose community
  edition went into maintenance in 2025 and stopped shipping images.
- backups: bucket versioning plus a nightly copy to a second provider (ties to the redundancy model).

---

## Ocharo slice (P1)

- Ocharo starts as a tenant on the shared files host, with its own hostname and one bucket per environment.
- its legacy files move in through the Wheelhouse migration module ([T9](file-storage-analysis-2026-10/t9-wheelhouse-migration.md));
  a later move to Ocharo's own instance is the first tenant move.
- Desk moves `bytea` media, exports and sourcing files out of PostgreSQL; rows keep the file id.
- Catalogue, Brand, Blog and Marketing drop their `MediaStore` copies for the SDK files client.
- Studio thumbnails leave the state JSON; garment models and Assets releases go to object storage by content hash,
  as `repository-review/creative-assets.md` already decided.

---

## Sequencing

The whole vector goes to the backlog; the build takes the slice products need now and grows the rest in parallel
after the first release (decided 2026-10-26).

1. the domain repo from the domain template: contract, files module with metadata, variants, signed URLs, shares and
   policy; the fe upload kit.
2. the service: host, API, console, Dockerfile, `deploy.yml`, conformance suite.
3. the shared files host: deploy; WoW2 apps and Ocharo join as tenants.
4. Ocharo: migrate through Wheelhouse — Catalogue and Brand first (smallest), Blog and Marketing, Desk last (largest).
5. P2 across the vector; Ocharo's own instance by a tenant move.

---

## Sources

- [MinIO alternatives](https://www.infoq.com/news/2025/12/minio-s3-api-alternatives/) — maintenance mode and replacements.
- [Contabo Object Storage launch](https://vpsbenchmarks.com/announcements/contabo-contabo-launches-new-all-inclusive-object-storage-01) — price per 250 GB; re-check before ordering.
