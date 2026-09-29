# First-ten startup implementation

*Updated: 2026-09-29*

## Completed scope

The user authorized creating and implementing all ten products under `workbench/ventures`. All ten independent repositories now contain locally verified v0.1 applications: Vue 3 interfaces, .NET 10 APIs, SDK authentication, SQLite migrations, domain workflows, export artifacts and tests. This is local pilot completion, not production deployment or market validation.

Canonical handoff: [venture index](../../../workbench/ventures/first-ten.md). Evidence: [implementation verification](../../../ideas/startup-research-2026-09/first-ten/implementation-verification.md). Track: [implementation status](../../../ideas/startup-research-2026-09/first-ten/implementation-status.md). Earlier [research and prototype](../../../ideas/startup-research-2026-09/first-ten/first-ten.md) remain separate evidence.

The ten products are Retainer Balance, Documentation Checker, File Watch, Procedure Review, Training Seats, EPUB Review, Customer Promises, Vendor Renewals, Config Checker and Podcast Readiness. They are registered in `scripts/active.sh`; the port ledger reserves their non-conflicting API/frontend ports. Each has its own `.git`, `.slnx`, launch script and product documentation.

## Verified results

- 69 backend cases, 47 frontend cases and 3 customer-local CLI cases passed. Backend totals include Development and Production access checks per product. Seventeen earlier isolated auth checks are separate.
- All ten passed strict TypeScript/Vue compilation, ESLint, Prettier and Vite builds. All ten local Release publishes passed asset/schema-presence and database/key-exclusion checks.
- Actual localhost HTTPS browser workflows persisted domain state through reload. All ten passed 390px page-overflow checks; desktop workflows used 1440px. Podcast anonymous guest flow was checked separately.
- All ten downloaded valid JSON exports. SHA-256 manifests, dependency/Compose checks, frontend formatting results and Release packaging evidence are saved under `ideas/startup-research-2026-09/first-ten/verification-artifacts`.
- Agent reviews and browser findings were repaired and regression-checked. Latest Config Checker fix preserves approval when displaying the same exact snapshot pair in reverse order.
- Docker Compose configuration passes; Docker image execution, proxy deployment and backup restoration remain unverified.

## Runtime and package state

All ten task-owned product watchers and prototype server were stopped gracefully after implementation verification. The user subsequently requested running and viewing three products. Retainer Balance is running in managed terminal session `92702` at `https://localhost:8300/`; Documentation Checker in `3762` at `https://localhost:8302/`; File Watch in `51696` at `https://localhost:8304/`. Root owns all three sessions, including the two handed over by the developer agent. Frontend deploys and backend builds succeeded; trusted HTTPS readiness was verified. Browser opens were queued once per URL through `open_in_codex`. Keep these three runtimes alive across the user's review turns. The other seven products and prototype server remain stopped.

Temporary QA viewport overrides were reset in the preceding turn. Local QA data belongs to an isolated synthetic account; a newly registered local account receives an empty workspace. Launch prerequisites and other ports remain in the venture index.

Development requires .NET 10, Node 24.11.x and pnpm 10.33.2. The existing localhost HTTPS certificate was verified trusted without modifying trust. Watchers use `--no-hot-reload` rebuild mode and exclude generated assets/runtime data. Scoped native escalation resolved sandbox host/socket/restore constraints where required. No approval request remains pending.

Backend SDK: `10.0.60-beta.local.20260927.8`, seven checksummed NuGet packages per repository. Binary NuGet artifacts are ignored. Frontend SDK: existing built SDK dist packed as `ui-vue-0.0.7-pilot.tgz`, checksummed and file-pinned; it differs from published `0.0.7`. Shared SDK and template source were not edited. Reproducible remote builds require a published feed or distribution of these exact artifacts.

## Launch boundaries

One personal workspace per authenticated account; SQLite assumes a single instance. SDK cookies, CSRF, Argon2id, lockout, default-deny authorization, persisted Data Protection keys and isolated identity storage are implemented. Production registration defaults closed. Team membership, recovery/email verification, billing, outbound delivery, hosting, monitoring, retention and backup restoration remain launch work. Approval/renewal/digest records do not send messages or execute external actions.

Budget stays $20–50 per product monthly until validated revenue can justify approximately $300. No measured hosting costs, customer retention, acquisition or revenue evidence was produced. Retainer Balance remains the first paid-pilot candidate from the earlier analysis.

## Git and ownership

Root commit permission ON / push OFF; child repositories commit OFF / push OFF. No task-created commits, pushes or remotes. Foreign staged files and unrelated edits remain preserved. An earlier `git commit --only` attempt was rejected by the local hook; a whole-index commit would include foreign staged work, so no workaround commit ran. Task source and evidence are saved locally.

All three agent lanes completed: business (retainer/procedures/training/renewals), developer (docs/files/config), creator (EPUB/promises/podcast). Root completed common access, packaging, registration/ports, browser verification and handoff. No implementation task is pending within the authorized local v0.1 scope.
