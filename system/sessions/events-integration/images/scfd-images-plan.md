# SCFD images to every subscriber, and the terms references removed

*Written: 2026-11-20 · by the `ocharo - events ui` lane, read-only analysis; no repo changed by this doc*

> The developer, 2026-11-20, on Ocharo's cards showing date tiles: "why images are not being served ? scfd's fss should
> serve all images just like it's serving them for scfd - … imo - no, any asked image should be just searched, since
> scfd depends on public data not private, so it's already public and any subscriber should be able to see the image
> regardless of whether that image belongs to the posts they have subbed or not".
> Then: "they are not reused, reused means creating a new site that looks and works like afisha, and start
> copy-pasting their posts while not giiving credit, we are not changing their posts, we have original post content,
> we are using this for internal use only and we are giving credit everywehere by showing the external url - so
> nothing is violated, plus - pls remove any reference to whatever terms you have".
> And: "scfd should copy all images, should show them for any subscriber as long as they are getting the image from
> fss with api key - need to analyze how we gonna update the integration in fss to use the same api key scfd has - in
> this instance scfd owns the fss service instance".

## Path prefixes

| Prefix | Path (under `wow-two-ws/workbench/`) |
|---|---|
| `{H}` | `wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services` |
| `{F}` / `{FD}` | `wow-two-sdk-beta/wow-two-sdk-beta.files/engineering/codebase/files.backend-services` / `…/engineering` |
| `{E}` | `wow-two-sdk-beta/wow-two-sdk-beta.events/engineering/codebase/events.backend-services` |
| `{O}` | `mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-platform/engineering/codebase/ocharo-events.backend-services` |

## Why images stop today

Three stops in series, none in Ocharo:

1. Policy: decisions #31, #32 and #50 and the UI analysis's OQ-2 kept sourced images out; the developer has set
   them aside, internal use with credit by the external link being the rule.
2. SCFD: images are copied into Files only for sources with permission `open`/`granted`, posture `own_fetch` and an
   image on the source's own host (`{H}/service/HarvestSources.Api/Media/SourceAssetStore.cs:19-37`,
   `SourceAssetDestination.cs:12-18`), as `FileVisibility.Private`; the console reads them through its own
   authenticated proxy (`SourceAssetsController.cs:16-34`, `posts:read` + container check). `wow2.event.v1` media
   carries only the source `url`, with `fileRef` null (`ModuleDeliveryBroker.cs:403-433`, `EventSchemaMapper.cs:43`).
3. Events: `ScfdEventMapper.cs:12` drops media on intake; `facts.images` is curator-only (`EventImage.cs:3`), and the
   kit's `EventMediaCard` reads only `facts.images[0]`.

## Files access: what exists

- Files authenticates an `X-Api-Key` (`files_…`) or a JWT per request
  (`{F}/service/Files.Api/Auth/FilesAuthServiceCollectionExtensions.cs:122-132`). Keys are config rows
  `Files:Auth:ApiKeys:n:{Id,Sha256,TenantId,AppId,OrganizationId,ExpiresAt,Scopes}` with only the hash stored
  (`FilesAuthSettings.cs:45-67`); scopes `files.read|write|share|admin`.
- The tenant is the only read boundary (`PrincipalFilesCallerService.cs:31`, `ModuleFileStoreBroker.cs:159-174`): any
  key of a tenant with `files.read` reads every file of that tenant.
- Read routes: `GET /api/files/v1/files/{id}`, `/{id}/content`, `POST /{id}/urls` (signed `/f/…` links, 5 min
  default, 7 days cap).
- SCFD's client is `HarvestAssets:Files:{BaseAddress,ApiKey}` (`{H}/…/HostConfiguration.Extensions.cs:49-57`); the
  copy worker is off while `BaseAddress` is empty. Whether `harvest-dev` has it set is unverified.
- One dev Files instance exists (Wheelhouse `files-dev`), trusting only Ocharo's Identity (tenant `ocharo`); its
  descriptor declares no `Files:Auth:ApiKeys:*` typed keys yet, so no tenant key can be set through Wheelhouse today.

## Plan (lane picks; the developer can change any)

- SCFD owns tenant `scfd` on Files — on `files-dev` now; a separate Files target later if wanted.
- SCFD keeps its read+write key. Subscribers get a sibling read-only key (`files.read`) in the same tenant. It gives
  the same access to SCFD's images, but a leaked subscriber key cannot write, and rotating SCFD's own key breaks no
  subscriber; literally sharing SCFD's key would carry both risks.
- Records the exception to files-integration #5 ("API keys serve only callers outside Identity"): the developer chose
  keys here.
- SCFD copies every image a post references (up to the existing 20 per post, 5 MiB, raster kinds), whatever the
  source's permission, posture or image host. Robots rules stay for page fetches; images referenced by a fetched page
  are copied regardless (`RobotsPolicy.Obey` at `SourceAssetWorker.cs:62` becomes Ignore for post images).
- Any subscriber may read any SCFD image by its file id with the read key — no per-subscription check, as asked.

### Change list per repo

| Repo | Change | Owner |
|---|---|---|
| harvest | Ungate `SourceAssetStore.QueueMissing` (drop the permission and posture/host predicates, keep https, kind image, position ≤ 20, no `access_token`) and `ClaimAsync` (:58-60); host pacing on the image URL's host (new `host` column, migration after `007-source-assets`); `SourceAssetDestination` → https, port 443, no userinfo, no `access_token`, keep the public-IP and redirect guard; images ignore robots; `RenderPayload` enriches `media[]` with `fileId` and `hash` by joining `harvest_source_assets` on (sourceId, url); update `wow2.event.v1` fixtures and `SourceAssetsTests`; set `HarvestAssets:Files:*` on `harvest-dev` with SCFD's key in tenant `scfd` | ev-build |
| files | Declare typed keys `Files:Auth:ApiKeys:0..1:{Id,Sha256,TenantId,Scopes}` and a `Files:Policies:scfd:*` policy (5 MiB, image kinds, variants) in `{FD}/deployment/deploy.yml`; no runtime code change; note the #5 exception | files owner (orchestrator to assign) |
| wheelhouse | Type the two key hashes on `files-dev`; the secrets through `wow2 secret set` | the developer runs the secret command |
| events | Read `media[]` in `ScfdEventMapper` into `facts.images` (`EventImage` gains `FileId`), keep the source URL as the credit link; reopen #31 and #50's wording; fe-events needs no change | ev-build |
| ocharo | `{O}`: read-only Files key config (`Files:BaseUrl`, `Files:ApiKey`), `AddFilesClient`, and a route `…/events-api/…/events/{id}/images/{n}` that resolves the file id from the event it read through Events (never a raw id from the browser) and 302s to a signed Files URL | ocharo - events ui |

## References removed

- 2026-11-20: the orchestrator's docs, in the commit that adds #75; harvest's and events' docs, code comments and test
  by `ev-build`.
- Kept: internal use only, and credit by the external link on every item.
