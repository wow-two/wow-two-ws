# First-ten verification

*Executed 2026-09-29 · Local synthetic prototypes only*

## Build and source

- `npm run build` passed: strict `vue-tsc --noEmit` followed by Vite production bundling.
- Ten product SFCs compile against the same typed prototype API and public Vue SDK entrypoints.
- `make-portable.mjs` embeds the compiled JavaScript and CSS into one `prototype.html` file. It needs no external asset or API.
- The business-product lane additionally executed isolated actual-SFC state/invariant checks for retainer, procedures, training and renewals. These are state checks, not browser or backend tests.
- No production server, authentication, billing, email, connector, cryptography, checker execution or multi-user authorization was tested. None is implemented by the mock suite.

## Browser-executed workflows

The root agent operated the built suite through the in-app browser. Form errors below were observed in the rendered UI. Each product was reloaded after its mutations to check browser-local persistence. Actual downloaded files were read from the local Downloads folder and checked against the resulting state.

| Product | Executed actions and observed outcome | Download evidence |
|---|---|---|
| Retainer | Reconciled original 4h; imported/reconciled 3.5h; requested/approved 3h; prepared statement; duplicate T-105 rejected. 26.5h consumed / 27h authorized / 0.5h available survived reload. | `brightside-september-ledger.json`: balance 30 minutes |
| Docs | Empty owner form rejected; assigned Maya; unchanged rerun failed; sample correction plus rerun passed; history preserved failure/failure/pass. | `snippet-check-report.json`: 1 failing, 3 passing, 6 attempts |
| Files | Empty row count rejected; receipt 1,248 rows; calendar exception added/removed; clock advanced twice. Received 3/5, late 1, waiting 1 survived reload. | `arrival-calendar.json`: inventory receipt and simulation clock persisted |
| Procedures | Attestation without checks/evidence blocked; revised excerpt to v4; checked both review statements; recorded evidence. Current until 2026-10-29 survived reload. | `procedure-review-register.json`: version, due date and history retained |
| Training | Empty substitution rejected; replaced Noah with Alex without consuming an extra seat; marked attended; reserved and released Jordan. 12 purchased / 2 attended / 3 reserved / 7 available survived reload. | `orbit-training-seat-statement.json`: available 7 with substitution history |
| EPUB | Empty evidence rejected; resolved/reopened finding; imported fifth finding; empty proof label rejected; created Proof 02; returned to Proof 01. Client review blocked until all five findings resolved; recorded review survived reload. | `field-notes-proof-1.json`: reviewed true, five resolved findings |
| Promises | Confirmed owner; empty update rejected; recorded delivery; empty capture rejected; created unconfirmed promise. Digest omitted it. Account change cleared the draft and disabled approval/export; refreshed Morrow-only digest approved. State survived reload. | `client-digest-morrow-studio.txt`: one Morrow commitment only; `customer-commitments.json`: five commitments and immutable approved account snapshot |
| Renewals | Decision blocked before acknowledgment; changed owner to Jonas; acknowledged; recorded cancellation intent; reopened. Owner and decision history survived reload. | `renewal-decisions.json`: internal history, derived dates, externalSubscriptionChanged false |
| Config | Empty collector reference/reason rejected; simulated missing-key correction; approved/revoked difference; new manifest invalidated an earlier approval. | `configuration-comparison.json`: missing 1, review 3, approved 0, matching 2 |
| Podcast | Simulated missing-item reminder; invalid guest form rejected; added headshot reference and acknowledgment; reopened/reconfirmed technical check; marked recorded. Recorded/100% survived reload. | `episode-112-readiness.json`: Recorded with four completed checks |

The full per-product smoke scenarios include additional cases beyond this executed subset. They are acceptance instructions, not claims that every case was run. The root results here supersede earlier lane notes that browser verification was pending.

## Responsive and theme checks

- All ten routes were visited at viewport settings **390×844, 820×1180 and 1440×900**, in light and dark themes: **60 route/theme/size checks**.
- No page-level horizontal overflow occurred. The desktop browser's scrollbar reduced measured content widths to 375/805/1425px. The configuration table scrolls inside its own panel as designed.
- Screenshots were visually inspected for the overview, desktop EPUB workspace, and phone podcast workspace in light/dark themes. This is representative visual review, not a claim of 60 independently inspected screenshots.
- Mist, Paper and Porcelain controls changed the actual canvas to their respective color tokens while preserving the selected workflow.
- First-visit, loading, connection-error and restored working-sample previews rendered. Returning to the working sample preserved saved proof review state.
- Mobile navigation focused its close button, made the background inert, accepted Escape, and restored focus to the menu trigger.
- The browser console returned no warning/error records during the exercised suite.
- All ten sample workspaces were reset through their visible reset dialogs before handover.
- Final phone regression after touch-target fixes found no visible product button below 44px height and no page overflow on any route. The mobile-only close button remained hidden on desktop.

## Limits and follow-up

This is not an accessibility certification, cross-browser matrix, penetration test, end-to-end service test, or market validation. Screen-reader speech, contrast across every nested component, very long translated strings, timezone/DST behavior, real file parsing and multi-user races still need production checks.

The in-app browser blocks `file:` navigation by policy. The standalone artifact was generated and inspected structurally, but was not browser-executed through a `file:` URL. The HTTP loopback build was browser-verified; no browser policy was bypassed. Users can open the saved portable artifact in their own browser or use the documented loopback preview.

Browser storage is a demo convenience with top-level shape recovery, not a production schema/migration layer. Do not enter confidential customer data into these sample workspaces. Exports are synthetic test artifacts, not evidence of real customer approvals, contract changes, accessibility compliance, recordings, file arrivals, or deployed configuration changes.
