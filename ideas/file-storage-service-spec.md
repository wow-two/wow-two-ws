# WoW Two Files — Own File Storage for Every Product

*Last updated: 2026-10-25*

> `wow-two-platform.storage.file`: one way to store, transform, protect and serve files, shipped in the three
> [capability forms](../conventions/development/capability-forms.md). Products stop writing their own `MediaStore`.
>
> **Status:** the developer chose to build it on 2026-10-21; first consumer Ocharo. Open choices:
> [platform decisions](../docs/platform-decisions.md) D6–D8.

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

- **Form 1 · library** — a files module over `Storage/` and `Media/Images` in the be SDK, the upload kit in the
  fe SDK; for one product with files in its own bucket.
- **Form 2 · self-hosted service** — the module hosted with an API and an admin console, as the
  `wow-two-platform.storage.file` image; for one owner's apps: Ocharo runs its own.
- **Form 3 · provided service** — the same image, run once by us on the WoW2 control host, for the portfolio.

- the repo `wow-two-platform.storage.file` exists with an empty solution (2 commits, 2024); it becomes the service.
- every form authorizes with [Identity](identity-service-spec.md) claims: organization, app and role.

### Instances per owner

Decided 2026-10-25: one instance per owner, shared by that owner's services.

- WoW2's own instance belongs to the WoW2 apps: Harvest's captures and the [Events](events-service-spec.md) catalogs'
  media live there.
- Ocharo's instance holds only Ocharo's media: products, brand, uploads and its own files about events.
- a self-hosted Harvest and Events ship with a File Storage instance in the same bundle, split the same way.
- a record that uses a file holds a reference; the file lives while any reference does, so pruning a capture never
  removes a published image, and nothing is copied between services of one owner.

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
- references and orphan collection: a file lives while a record points at it (P1 references, P2 sweep).
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

### Serve

- private by default: short-lived signed URLs, checked against the caller's organization and role (P1).
- public files (catalogue and blog images) on immutable `/media/{sha}` URLs with year-long caching (P1).
- a CDN in front of public files (P2); image resizing at the edge (P3).
- range requests for video and large downloads (P1).

### Limits and admin

- quotas per organization and app; a usage figure on every upload response (P2).
- console: usage by app and organization, largest files, recent uploads, orphans, failed scans, a file browser
  with preview and download audit (P1 usage and browser, P2 the rest).
- an audit row for every upload, delete and private download (P1).

### Developer surface

- be SDK files client: upload, attach to a record, get a signed URL, delete; one contract for every form (P1).
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

- Ocharo runs Form 2 beside its Identity instance, one bucket per environment.
- Desk moves `bytea` media, exports and sourcing files out of PostgreSQL; rows keep the file id.
- Catalogue, Brand, Blog and Marketing drop their `MediaStore` copies for the SDK files client.
- Studio thumbnails leave the state JSON; garment models and Assets releases go to object storage by content hash,
  as `repository-review/creative-assets.md` already decided.

---

## Sequencing

1. be SDK: files module with metadata, variants, signed URLs and policy; fe SDK `fileUpload`.
2. `wow-two-platform.storage.file`: host, API, console, Dockerfile, `deploy.yml`, conformance suite.
3. Ocharo: deploy, then migrate Catalogue and Brand first (smallest), Blog and Marketing, Desk last (largest).
4. P2 across the vector; then Form 3 for the portfolio.

---

## Sources

- [MinIO alternatives](https://www.infoq.com/news/2025/12/minio-s3-api-alternatives/) — maintenance mode and replacements.
- [Contabo Object Storage launch](https://vpsbenchmarks.com/announcements/contabo-contabo-launches-new-all-inclusive-object-storage-01) — price per 250 GB; re-check before ordering.
