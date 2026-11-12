# Events infrastructure: next build

*Reviewed: 2026-11-05. Scope includes shared Harvest, its private adapters, Events, Ocharo Desk and Haven.*

## Recommendation

Run Harvest as a shared API. Use it to deliver **Afisha → Events review → Ocharo Desk** and **OLX → Haven Supply**. Events owns reviewed event facts and private tracking. Supply is the first boundary for listing intake and classification. Haven owns the commercial experience.

## Verified baseline

| Area | Current evidence | Consequence |
|---|---|---|
| Public Harvest | Local commit `d77daf6` adds API-only service access. An isolated Identity issuer authenticated an operator and two consumers. Each consumer read its own feed and was denied the other feed and tenant administration. | Deploy with separate operator, Events and Haven client grants. |
| Private adapters | Reviewed commit `fcd6b2c627473acc7993d63b730b16138af9f520`; source readers, Ocharo filtering and a host reuse public Harvest. The approved push advanced `main` from `4d5accc` on 2026-11-05. [Delivery CI](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest-adapters/actions/runs/41936924373) passed and published [v0.1.1](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest-adapters/releases/tag/v0.1.1), including its image and Wheelhouse bundle. | Keep source-specific parsing and Ocharo policy here. |
| Private security scanning | The [CodeQL run](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest-adapters/actions/runs/41936923692) failed to upload results for all 4 languages because Advanced Security is not enabled for this private repository. | Resolve code-scanning availability separately; delivery success does not establish a successful security scan. |
| Ocharo Desk | Reviewed checkout at `c4c5f79489f3154cc544a72b3c364910b46397b9`; feed, deadline, detail, editing and calendar components exist. The importer inserts new keys and skips existing keys. No Harvest reference was found in Desk's backend/frontend source. | Reuse the screens; replace manual-only intake and reconcile changes through Events. |
| Events | The [Events spec](events-service-spec.md) and Ocharo ownership decision exist. Neither proposed Events checkout exists locally; GitHub returned `404` for both proposed repository names. This is not proof that inaccessible repositories do not exist. | Treat Events as an unimplemented capability in this workspace. |
| Local operation | The API-only Docker preview passed health, configuration and migration checks. Its two live OLX deliveries survived a container restart. | Verify the configured proxy and service clients on the shared dev target. |
| Haven | The opt-in Harvest OLX reader passed the intake tests over PostgreSQL. | Verify the shared subscription and switch OLX intake before porting Domtut. |

## Build order

| Priority | Build or finish | Owner | Exit criterion |
|---|---|---|---|
| 1 | Prove shared Harvest access in dev. | Harvest Hosting, Identity configuration and Wheelhouse | Issue separate credentials for the operator, Events and Haven. Confirm each consumer reads its own feed and receives a refusal for admin operations or the other tenant's feed. |
| 2 | Finish the first two pull consumers. | Events and Haven | A live Afisha record becomes a review candidate. Live OLX records arrive through the selected proxy and become Haven intake rows. Replays resolve to the same records. |
| 3 | Cut over the product intake paths. | Events, Ocharo Platform and Haven | Show an accepted event in Desk with existing tracking preserved. Match Haven's existing listing keys and preserve triage. Reconcile migration totals and prove rollback. |
| 4 | Finish operating controls before unattended schedules expand. | Public Harvest, Events and deployment configuration | Enforce request budgets during transport, purge expired data according to policy, expose source freshness and consumer lag, and demonstrate crash/restart recovery. |
| 5 | Complete evidence and source coverage from real misses. | Public Harvest and private adapters | Version source readings/mappings; retain participation/contact evidence; accept the existing ANONS, Craftfair and Uzexpocentre readers against bounded live samples. Measure relevance, duplicates and missed deadlines. |
| 6 | Complete the Events capability and deadline actions. | Events, with Desk as consumer | Cover occurrences, series, places/organizers, imports, calendar feeds and read-only agent access; add deduplicated reminders through the chosen notification boundary. |

Priorities describe delivery order, not a requirement to finish every acceptance check before starting Events development. Priority 4 gates broad unattended operation. Priority 5 evidence needed to explain the first candidate belongs in priority 2; the complete versioned reading system follows as its own pass.

## Shared Harvest access

Run one shared Harvest API per environment. Harvest has its own Identity issuer. Identity and Files continue
to run per product owner. Operators and consumers authenticate with separate confidential clients. Each client
exchanges its ID and secret for a short-lived bearer token with the Harvest resource as its audience.

The operator client receives explicit administration scopes. Each product client maps to one active tenant and
the scopes it needs. A subscription reader uses `events.read` at Identity and `events:read` in Harvest.
Harvest intersects the issued scopes with the binding and checks ownership before reading a feed. Ocharo and
Haven own their user sign-in and any views they build. Add organization-based API grants when a consumer needs
them. [Deployment settings](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/deployment/deployment.md#shared-api-access)

The API-only image removes the hosted console and browser session routes. Local Compose supports a development
operator key. Wheelhouse uses bearer mode with a Harvest issuer, audience and client bindings. Register and
test those dev credentials before rollout.

## OLX and Haven cutover

- The new API preview captured two live OLX listings in run `01a1ac8c-a022-714d-b797-5ffa5b966bfa` and
  delivered two `post.new` events. It made four requests over three work pages with zero failures.
  The run stopped at its configured page limit.
- The published backend SDK `10.0.105-beta` owns the guarded proxy transport. Private adapters choose the OLX
  route and supply an approved endpoint. Start with GeoNode or Decodo and compare the same bounded search.
  [Provider comparison](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest-adapters/engineering/research/olx-egress-options.md)
- Haven Supply can pull a Harvest subscription from its existing `sup-intake-olx` pipeline. It upserts on the
  existing provider and external ID, then saves the subscription cursor. The intake test confirmed that a newer
  snapshot preserves the prior row ID and phone, and the next pull resumes from its saved cursor.
- Supply is the first boundary for private intake and classification. Extract a separate service if another
  product needs classified output or Supply needs its own lifecycle. Haven owns triage and publishing.
- Harvest supersedes the ListingShelf product idea. Keep the legacy collector for Domtut and OLX rollback
  through cutover. Port Domtut, reconcile delivery and retire the legacy runtime before archiving its history.
  [Haven cutover](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/maxs-projects/ventures/saas/10x-ven-haven/engineering/deployment/deployment.md#harvest-olx-cutover)

## Events intake and review

- Use the existing [pull broker](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/bc0c8ac7e008f0e75c8e5f35d5250e14e2bd4c74/engineering/codebase/harvest.backend-services/packages/Abstractions/Delivery/IDeliveryBroker.cs#L5-L16). The older Events spec assumes webhook delivery; public Harvest explicitly ships pull first.
- Persist received observations and the next cursor in the same Events database transaction. Advance only after the entire page is durable, including any quarantined invalid records. Human review must not block intake.
- Deduplicate retries by delivery `EventId`, scoped to the Harvest instance/subscription. Use `ItemId` for content identity across subscriptions and resyncs. Apply the highest `Revision` per `PostId`; delivery has no global order. These fields are defined by [DeliveryEvent](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/bc0c8ac7e008f0e75c8e5f35d5250e14e2bd4c74/engineering/codebase/harvest.backend-services/packages/Abstractions/Delivery/DeliveryEvent.cs#L5-L41).
- Process lifecycle and run/health events separately from post payload revisions. A missing source page changes evidence availability; it does not establish cancellation of the real event.
- Retain the source instance, pipeline, post/revision, original link, capture reference, observed time, source fields and mapping version for each observation. Preserve the input needed for review within the applicable retention policy.
- Match exact source identity first. Propose cross-source matches using edition, title, place and dates; require review for ambiguous merges. Co-located events and different annual editions remain distinct.
- Separate observed facts, reviewed catalog facts and organization tracking. A source correction must not overwrite a reviewer's accepted date, an organization's stage or private notes. Show the proposed changes and their evidence.
- Distinguish listing publication time, event dates, application deadlines, participation route and contact purpose. Unknown admission, fees and dates remain unknown. Visitor access never proves seller, exhibitor or runway access.
- Start with a private `ocharo-fashion` catalog. Desk uses Ocharo Identity for its users and checks membership in its backend. The Events backend consumes Harvest with its service credential.
- Test replay, out-of-order revisions, a crash around cursor commit, a malformed record, conflicting dates, a source disappearance and a cross-organization read. These cases define the consumer's correctness.

The [current event mapper](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/bc0c8ac7e008f0e75c8e5f35d5250e14e2bd4c74/engineering/codebase/harvest.backend-services/packages/Module/Extraction/EventSchemaMapper.cs#L8-L38) provides dates, place, offers, contacts and source tags. It does not expose every deadline, participation or contact-ownership concept from the Events spec as a typed field. Retain native evidence and record missing mappings explicitly; correct generic contracts upstream when the first consumer needs them.

## Desk migration

- Follow Ocharo's decided ownership: Events owns catalog **and tracking**. Desk owns its page, organization authorization and references to Ocharo entities. Avoid a second canonical tracking writer.
- Use the existing [Desk import service](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-platform/engineering/codebase/brand-workspace.backend-services/BrandWorkspace.Infrastructure/Events/Services/EventImportService.cs:21) as migration evidence: it deliberately skips existing keys. It cannot reconcile ongoing reschedules or corrections.
- Produce a dry-run migration with a stable old-to-new identity map. Preserve every stored status, priority, note, provenance link and language; do not assume all existing titles are Uzbek.
- Preserve uncertainty when converting legacy date fields. A stored first-of-month placeholder must remain month precision; legacy `estimated` values must not become confirmed dates.
- Route Desk through the Events contract and retain its existing views until shared components can replace them with equivalent behavior. Freeze the old canonical writer at cutover; keep the export and rollback path until reconciliation passes.

## Operation before expansion

- Extend the existing limits rather than adding a second scheduler. The [engine accounts for usage and checks run limits at step boundaries](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/bc0c8ac7e008f0e75c8e5f35d5250e14e2bd4c74/engineering/codebase/harvest.backend-services/packages/Module/Engine/HarvestEngine.cs#L307-L386). Reserve request allowance before transport attempts and stop byte consumption within a request, including robots and redirects.
- Implement retention maintenance. The [engine's documented exclusions](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/bc0c8ac7e008f0e75c8e5f35d5250e14e2bd4c74/engineering/codebase/harvest.backend-services/packages/Module/Engine/engine.md#L25-L33) include retention; expiry columns and retention declarations do not themselves delete stored bytes. Test purge propagation and required audit records.
- Distinguish a healthy process from fresh data. Expose last successful source run, partial/refused runs, next due work, stale leases, subscription cursor lag, quarantined observations and oldest unresolved review.
- Give operators explicit pause, resume, replay and resync controls. Prove existing lease fencing survives a worker restart and that Events resumes from its committed cursor.
- Test backup/restore with database state and durable session keys. Keep optional provider sessions and source provisioning within their current single-process ownership limits until replica-safe coordination is implemented.

## Complete the domain after the first slice

| Capability | Completion direction |
|---|---|
| Evidence | Store immutable source readings and mapping results with schema/parser versions. Preserve field-level attribution and human overrides. Add schema validation before relying on arbitrary source payloads. |
| Events model | Complete occurrences, edition/series identity, places/organizers, uncertain dates, explicit cancellation/rescheduling, deadlines, participation routes and offers. Do not generate a future edition solely from recurrence. |
| Review | Complete conflict resolution, merge/unmerge history, reject/archive behavior and optimistic concurrency. Keep private tracking isolated from shared catalog facts. |
| Consumer forms | Keep one broker contract and conformance suite across the module and HTTP client. Extract reusable UI parts from the working Desk integration. Add the hosted surfaces named consumers need. |
| Calendar and actions | Export reviewed facts with stable calendar identifiers and revisions. Schedule each reminder once per event/deadline revision, cancel obsolete reminders, and enforce current organization access. Decide the outbound notification route before sending. |
| Media | Reconcile the spec's shared Files references with today's inline captures and source media URLs. Define ownership, retention and attribution before importing media durably; do not assume the old Files integration is already bound. |

## Repository and spec alignment

- Keep generic fetching, lifecycle, delivery, source-reading schemas and engine operating controls in `wow-two-sdk-beta.harvest`.
- Keep named readers, provider protocols and Ocharo relevance policy in `wow-two-sdk-beta.harvest-adapters`.
- Recommend one Events domain repository, `wow-two-sdk-beta.events`, containing its module/client and host when required. The older spec's separate `wow-two-platform.events` host conflicts with the current [capability forms convention](../conventions/development/capability-forms.md). Keep this name as a proposal until the implementation task creates/registers it.
- Reconcile the Events spec with pull delivery, the current Identity/machine-auth boundary, evidence-backed corrections and migration semantics before implementation. Keep the first host consistent with the named consumer's isolation need; do not build a second implementation of the module.
- Reconcile dated backlog rows with code and releases. Repository creation, private Afisha/OLX readers and current SDK adoption must not remain listed as future work if already delivered.

## Defer until a consumer or measured gap requires it

- Defer Harvest webhook push while pull supports the first consumer. Add push through the shared durable dispatcher when a named consumer needs it.
- Defer AI extraction, translation and fuzzy auto-publication until deterministic coverage, provenance and review are measurable. AI may propose evidence-backed results; it does not replace source facts or admission checks.
- Defer more social connectors, browser rendering and paid providers until existing sources reveal a coverage or access gap. Their code/configuration presence does not establish a verified live integration.
- Reuse the Events/Desk and Haven views and the existing notification boundary.

## Supporting decisions

- [Events service spec](events-service-spec.md) defines the domain and the old delivery/placement assumptions to reconcile.
- [Ocharo app boundaries](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/docs/app-boundaries.md:65) records the catalog-and-tracking ownership decision.
- [Private source acceptance backlog](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest-adapters/engineering/planning/backlog.md:7) records live Identity, source, provider and rollout gaps.
- [Afisha field audit](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest-adapters/engineering/research/afisha-field-audit.md:56) distinguishes raw captures, source fields, mappings and future analysis.
- [Ocharo source review](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest-adapters/engineering/research/ocharo-source-review.md:1) records source roles and participation-evidence constraints; its dated web observations require new bounded acceptance.
