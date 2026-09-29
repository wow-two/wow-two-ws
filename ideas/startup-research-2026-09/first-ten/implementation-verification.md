# First ten — implementation verification

Verified: 2026-09-29

This record covers the ten new repositories under `workbench/ventures`. Earlier prototype verification is separate and does not count as evidence for these applications. Checks used synthetic local data only. No external message, production deployment or customer transaction occurred.

## Automated checks

| Product | Backend cases, including two Access cases | Frontend cases | Customer-local CLI cases |
|---|---:|---:|---:|
| Retainer Balance | 5 passed | 6 passed | — |
| Documentation Checker | 4 passed | 2 passed | 1 passed |
| File Watch | 6 passed | 2 passed | 1 passed |
| Procedure Review | 5 passed | 6 passed | — |
| Training Seats | 5 passed | 6 passed | — |
| EPUB Review | 12 passed | 5 passed | — |
| Customer Promises | 9 passed | 4 passed | — |
| Vendor Renewals | 5 passed | 6 passed | — |
| Config Checker | 5 passed | 5 passed | 1 passed |
| Podcast Readiness | 13 passed | 5 passed | — |

Total: **69 backend, 47 frontend, 3 CLI cases passed.** Product cases exercise domain invariants, real SQLite storage and authenticated HTTP boundaries as recorded in each repository. The common Access theory runs once for Development and once for Production. Seventeen additional isolated authentication contract checks preceded integration; they are not included in the totals.

All ten frontends passed strict TypeScript, Vue SFC compilation, ESLint without warnings, Prettier, and Vite production builds. Each bundle was copied into its API host. The [format report](verification-artifacts/frontend-format-results.txt) and [dependency/compose checks](verification-artifacts/packaging-input-checks.json) are saved. Exact test commands and scopes are in each repository’s `engineering/development/verification.md` or `engineering/versions/0.1.0.md`.

## Actual browser workflows

The root verifier operated the built SPAs through localhost HTTPS, using SDK login and server-issued cookies. Desktop flows used a 1440px viewport; each product was checked at 390px without document-level horizontal overflow. Podcast guest view was checked separately at 390px. These checks do not claim a complete accessibility audit, every browser, every breakpoint, dark-mode coverage, or load testing.

| Product | Observed end-to-end result |
|---|---|
| Retainer Balance | Created a 24-hour period, imported a CSV entry, reconciled 3 hours, recorded evidence for 3 additional hours, published a statement, and reloaded to 27 authorized / 3 confirmed / 24 remaining. |
| Documentation Checker | Imported a failing report, assigned an owner, imported a passing run at the same source location, and reloaded with the owner retained. |
| File Watch | Created a daily UTC feed, observed collector-offline state, saved a calendar exception, and reloaded the persisted excepted occurrence. Actual receipt/heartbeat/scan failure behavior was covered by HTTP and executable CLI tests, not a browser-driven live collector. |
| Procedure Review | Registered a versioned source, acknowledged ownership, completed both review checks with evidence, and reloaded the procedure in the current lane. |
| Training Seats | Created sponsor entitlement and cohorts, reserved learners, confirmed that future attendance is rejected, recorded attendance for a past cohort, published a sponsor statement, and reloaded persisted allocations. |
| EPUB Review | Created a publication, imported a synthetic Ace failure report, resolved machine and human checks with evidence, created a proof-specific packet, and reloaded it. A selection-stability defect discovered here was fixed and covered by a frontend regression. |
| Customer Promises | Captured a commitment, recorded owner confirmation, saved a progress update, prepared and approved a digest, and reloaded the approved but unsent digest with its latest update. |
| Vendor Renewals | Registered a term, observed its computed notice deadline, acknowledged it, recorded cancellation intent and reason, and reloaded the decision. No vendor cancellation occurred. |
| Config Checker | Generated two manifests using the real local HMAC CLI, imported only fingerprints, approved the exact snapshot pair, and verified approval after reload reversed the display order. A reverse-order matching defect was fixed with HTTP regressions and rechecked in the browser. |
| Podcast Readiness | Created an episode and scoped guest link, signed the producer out, submitted the anonymous guest packet, signed the producer back in, recorded technical evidence, and reloaded a ready episode with all four requirements complete. |

## Exports

Every product’s browser export produced a real downloaded JSON file. All ten parsed successfully and contained their expected resource type. The [export manifest](verification-artifacts/browser-exports.json) records filenames, sizes and SHA-256 hashes. EPUB repeat downloads were byte-identical. The browser automation download-event hook timed out although files were saved normally; filesystem verification resolved that observation.

## Review and fixes

Independent agent reviews and browser checks drove targeted fixes: stable documentation ownership across runs; exact configuration snapshot bindings, reversed comparison matching and request-state cleanup; file occurrence concurrency and completed-scan-only heartbeat; deterministic customer digest update ordering; complete podcast idempotency payload checks; conservative Ace outcome parsing and stable finding selection; scoped immutable statement exports and consistent snapshot reads. Regression checks passed after these changes.

## Packaging and runtime

All ten local SDK checksum checks and Docker Compose configuration checks passed. The single-instance pilot image explicitly owns startup migrations (`Database__ApplyMigrations=true`), preventing fresh developer-product images with absent tables. Runtime SQLite data and key files are excluded from Docker context. All ten local Release publishes succeeded; their built frontend assets and migration metadata were present, with no runtime database or Data Protection key files. The [Release packaging report](verification-artifacts/release-publish-results.json) records each check. Container build/run is a separate unexecuted check.

The initial .NET hot-reload watcher crashed when generated frontend bundles were replaced. The launch script now uses the documented rebuild-on-change `--no-hot-reload` mode, excludes runtime data and marks generated frontend content unwatched. A trusted existing localhost certificate was checked without changing trust. No HTTPS protection was removed.

At handoff, all ten task-owned product watchers and the earlier prototype server were stopped gracefully with exit code 0. Temporary browser viewport overrides were reset. Use the product launch scripts in the [venture index](../../../workbench/ventures/first-ten.md) to run a product for review.

## Limits and remaining launch work

- Verified target: local, single-instance, authenticated personal workspaces. This is not a production-readiness claim.
- Package publication/distribution, production HTTPS proxy, container execution, backup restoration, monitoring, retention and operational ownership remain launch gates.
- Email verification/recovery, shared teams, billing and outbound delivery are not configured. Product-specific dossier limits still apply.
- Prices, acquisition channels, retention, revenue and the $20–50 monthly operating assumption are unvalidated.
- Code and evidence are saved locally. Child repositories have no task-created commits/pushes/remotes; unrelated root staged work was preserved.
