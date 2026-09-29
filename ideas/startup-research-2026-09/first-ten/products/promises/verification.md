# Customer promises prototype verification

## Final integrated status

Root completed strict compilation, browser workflow/validation checks, actual export inspection, reload persistence, and responsive light/dark checks on 2026-09-29. See [the authoritative suite verification](../../verification.md) for the exact executed subset and limits. Sample state was reset before handover.

## Earlier lane review

The notes below describe the lane review at its original point in time; any pending root checks are superseded by the integrated record above.

Status: account-scoped digest source review complete; updated UI verification pending root review.

- Root reported strict vue-tsc and Vite build success before this account-scoping change. Rebuild remains pending.
- Source inspection confirms typed local state, local JSON/text exports and no external requests.
- Captured promises start unconfirmed. Confirming an owner increases the record revision.
- Empty/short updates cannot mutate the ledger; Delivered requires accepted ownership.
- Digest account defaults to Northstar Labs and has no all-account option, independently of the ledger filter.
- Preparation includes only the selected account’s confirmed records. Snapshot signatures bind that account and revisions.
- Changing Digest account synchronously clears the draft; approval/export require a refreshed, nonempty, current snapshot.
- Exports use account-specific filenames and headers. Full-ledger JSON is explicitly labeled internal.
- Approved digests are copied snapshots and remain unchanged when later commitments update.
- Active, overdue and delivered metrics derive from current records using the fixed sample date.

Root reported browser execution of owner confirmation, Delivered status and new unconfirmed promise creation before this change. The original digest dialog still showed all accounts; this revision removes that behavior. These are parent-reported observations, not checks executed by this lane.

CUA attempt: in-app browser unavailable; browser inventory empty. Native Arc was not touched, per root coordination. Updated digest isolation, draft invalidation, downloaded contents and reload persistence remain pending root execution. Root owns browser and responsive/theme verification.

Account-isolation smoke: ledger All accounts → Digest account Northstar Labs → Preview client digest (Northstar only; new unconfirmed record excluded) → change dialog account to Morrow Studio (draft cleared; approval/export disabled) → Refresh digest (Morrow only) → approve and export account-named text → select Northstar (invalidates again) → refresh and approve/export → close → ledger filter Lumen Works → preview remains Northstar → export internal ledger and inspect both approved snapshots → reload. Full setup and exact labels: product.md.

Remaining production gaps: server-enforced account authorization, client delivery, due-date amendments, external notifications and multi-user concurrency. Persisted pre-change approved snapshots lack an account field; they are retained only in internal ledger history and are not available for client-digest export. Reset sample data for the complete reproducible smoke sequence.
