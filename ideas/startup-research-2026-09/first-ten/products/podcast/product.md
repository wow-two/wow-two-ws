# Guestroom — podcast guest readiness

Proposal dated 2026-09-29 · W0507 · selected order 10 · proposed $29/month.

## Decision and philosophy

Serve a producer coordinating recurring guest interviews. The promise is that a guest arrives prepared and the producer can see which required items remain before recording. The core object is an **episode-specific readiness checklist**, supported by reusable guest information. The guest experience should be brief, welcoming and usable without learning a production tool.

The producer chooses requirements, supplies participation terms and confirms technical preparation. The guest provides their own biography, pronunciation and asset references. Software checks completeness, shows missing items and prepares a targeted reminder. It never infers consent, signs a release, claims recording readiness from an unchecked device test or sends a reminder without explicit authorization. Quiet by default means no automatic invitation and no repeated nagging when nothing changes.

## Advantage and incumbent challenge

[Transistor’s feature page](https://transistor.fm/features/), checked 2026-09-29, documents podcast hosting, distribution and collaborator access. This validates adjacent production tooling, not a separate guest-intake budget. [Riverside’s guest preparation guide](https://riverside.fm/blog/higher-quality-guest-interviews), opened through current search, describes sharing interview logistics and preparing guests; its [guest checklist resource](https://riverside.fm/community-guides/guest-checklist-tips-for-recording-day) makes the free substitute explicit.

Forms, Calendar and Drive can accomplish much of this job. The testable distinction is one guest-facing packet tied to an episode date, showing exactly what remains without reconciling several tools. Saving producer chasing time is the proposed paid value. No claim is made that an incumbent cannot add this feature or that their users want another subscription.

## Core journey and screens

1. A producer creates an episode with a named guest, recording date and explicit timezone.
2. The producer previews a guest form before sharing it through an authorized production channel.
3. The guest supplies biography, pronunciation, headshot reference and reviews producer-supplied participation information.
4. The producer confirms the separate technical check. Readiness recomputes from required items.
5. If anything remains, preview a reminder naming only missing items. An authorized send is a separate production action.
6. Once requirements are complete, mark the episode recorded and retain its packet for postproduction.

An original show tile anchors the workspace. The board uses Needs prep, Ready and Recorded columns; these stages derive from actual state. A selected-guest inspector combines checklist, host notes and next actions. At desktop width, board and inspector sit side-by-side. At 820px the inspector moves below the board. At 390px columns stack, keeping complete cards readable without horizontal scrolling. A guest-facing modal demonstrates the separate tone and minimal questions.

Empty: a board column states how an episode enters it. After the final upcoming episode is recorded, the next-recording banner invites adding another. Validation: the form checks biography length, image filename extension and the demonstration acknowledgment. Episode creation requires title, guest, valid email, upcoming date and `HH:mm UTC` time. Duplicate guest/date/time combinations are rejected. The mock uses UTC exclusively to avoid pretending it implements timezone conversion.

Failure and conflict: production must retain incomplete guest drafts, reject expired invitation tokens, and let a producer compare concurrent changes. A changed episode date requires a reviewed new schedule notification rather than silent guest assumptions. Those network/identity states are proposed, not connected here. In the mock, a recorded episode locks its preparation controls.

## MVP and non-goals

MVP: episode board, one guest packet, minimal asset references, producer checklist, targeted reminder preview, explicit submission acknowledgment and episode export. Start with links or filenames rather than hosting headshots. Reuse a guest profile only with permission, while keeping participation acknowledgment specific to the episode.

Exclude recording, audio processing, transcription, hosting, scheduling marketplace, talent discovery, guest outreach, legal release generation and electronic signature. Technical-check completion is a producer statement, not an automated device inspection. The local guest form does not upload any image or create a legally effective consent record.

## Entities and invariants

`Show` owns `Episode`; `GuestProfile` supplies reusable details while `EpisodeGuest` retains episode-specific requirements. `ReadinessItem` stores who checked it, its method and time. `ParticipationRecord` refers to producer-supplied terms and the exact version reviewed. `ReminderDraft` refers to a snapshot of outstanding items.

Ready means every required item is complete. Recorded can follow Ready only. A producer can reopen the technical check before recording, which moves the episode back to Needs prep. A reminder is ineligible when no items remain; production deduplicates by episode, recipient, missing-item set and schedule window. Recording media is a different object and cannot be inferred from a workflow status. Editing a guest profile must not silently rewrite historical episode packets.

## Proposed implementation and integration

Use a Vue module for the producer board, guest form and checklist. A .NET API owns shows, episodes, invitations, submissions and reminder policy. Candidate shared `@wow-two-beta/ui-vue` capabilities include fields, validation, dialogs, badges, toasts and progress indicators. Verify available public Vue exports before adoption; do not invent SDK methods or use the legacy React package.

Proposed routes: `POST /api/shows/{id}/episodes`, `PATCH /api/episodes/{id}`, `POST /api/episodes/{id}/invitations`, `GET /api/guest-packets/{token}`, `PUT /api/guest-packets/{token}`, `POST /api/episodes/{id}/checks/{key}`, `POST /api/episodes/{id}/reminder-drafts`, and `GET /api/episodes/{id}/packet`. Guest access is scoped to one episode; producer access requires show membership. Revision tokens prevent lost edits. Submission commands carry idempotency keys so retries do not duplicate records.

Proposed events: `EpisodeCreated`, `GuestPacketSubmitted`, `ReadinessChanged`, `ReminderApproved`, `EpisodeMarkedRecorded`. Reminder jobs run only for explicit show-level opt-in and approved communication policies. An outbox deduplicates delivery and stores provider status separately from preparation status. Daily job candidates must respect timezone, guest suppression and a maximum send frequency. No automatic upload or unrestricted link fetching is required.

## Data ownership and security

Guests control their submitted personal details; producers own episode coordination records within their agreed retention policy. Use short-lived revocable invite tokens, rate limits and show-scoped authorization. Keep guest contact details out of public episode pages and logs. Sanitize filenames and never fetch arbitrary supplied URLs server-side. If asset uploads are later justified, enforce size/type limits and malware checks. Prototype data is synthetic local browser storage; it has no authentication, external upload, email, signatures or protected customer vault.

## Pricing, cost and paid experiment

Propose two active episodes free, then $29/month for reusable guest records, templates and repeat preparation workflows. Suggested initial paid cap: 20 active episodes and 200 reminders/month, with metadata and asset references only. This targets $20–50/month operating cost before revenue; no vendor quote or measured cost is implied. Avoid paid recording APIs and image storage. Raise the ceiling toward $300/month only after revenue and measured storage/delivery volume justify it. Founder labor and guest support can dominate hosting cost.

Activation: one guest completes their packet before the episode date without producer re-entry. Retention: the producer uses the tool for the next four interviews. Observe ten producers across four episodes each; compare their existing form/email workflow. Require three paid $29 pilots, lower repeated chasing and renewal after another production cycle. Kill if guest completion falls below the existing workflow or producers see no reason to pay. At $29, 173 active subscribers yield $5,017 gross MRR; no conversion or retention forecast is established.

## Design references and system

The source pages above were inspected as text/documentation. The extracted conceptual moves are a short guest preparation packet, date-specific instructions and producer collaborators. There is no claim of visual screenshot analysis. The original three-column readiness board and warm guest form are recommended interaction proposals, not copied product interfaces.

Root’s three canvas palettes remain selectable; none is an approved lock. `--canvas` surrounds work, `--surface-alt` groups stages, `--surface` holds episodes and `--accent-soft` marks readiness details. The original show mark uses the product accent; it is CSS text and geometry, not a fetched image. Light/dark share hierarchy and status text. Proposed reusable controls are an episode card, checklist with evidence, guest packet form and explicit reminder preview. Every icon-only close control has a label; native dialogs retain keyboard operation.

## Staged build and acceptance

1. Review the local board, guest form and palette proposals at all three device widths.
2. Run an authorized manual comparison with producers before buying integrations.
3. Implement authenticated episodes, scoped invitations and revision-safe guest submissions.
4. Implement opted-in reminders with preview, rate limits and replay-safe outbox delivery.
5. Add asset storage or recording-provider integration only when paying customers demonstrate the need.

Acceptance requires stages and percentage to derive from checklist state, technical-check reversal to move a card back, recorded status to require readiness and reminder retries to avoid duplication. Production gates add invitation isolation, stale-edit handling, timezone tests, delivery suppression and explicit consent/terms version handling. No acceptance test treats a checkbox as a legal signature.

## Exact prototype smoke steps

1. Use the shell reset control. The board shows two Needs prep, one Ready and one Recorded episode.
2. Select Lena Park’s `Making room for better work`. Readiness is 50%; headshot reference and participation review are missing.
3. Click `Preview missing-item reminder`; only the missing items appear. Click `Record simulated reminder`. The button becomes `Reminder simulated today`; no email is sent.
4. Click `Preview guest form`, then `Save sample guest form` without a headshot. An inline filename error appears.
5. Enter `lena-park.jpg`; check the sample participation acknowledgment. Save. Lena’s card moves to Ready and shows 100%.
6. Click `Reopen technical check`. Readiness becomes 75% and the card returns to Needs prep. Click `Confirm technical check` to restore Ready.
7. Click `Mark recorded · simulated`. The card moves to Recorded and preparation controls lock. No media is recorded.
8. Click `Add episode`, then `Create episode` empty. Validation prevents creation. Add a title, guest, `guest@example.com`, upcoming date and `15:00 UTC`. Create it; the new episode starts at 0%.
9. Click `Export episode pack`. JSON includes the selected guest, current readiness, dates and simulated reminder history.
10. Reload to verify persistence. Switch light/dark and inspect 390px, 820px and 1440px layouts.

Implemented mutations: episode creation, guest submission, technical-check toggle, simulated reminder and recorded status. Remaining mocks: invitations, file uploads, identities, legal releases, recording, email and server persistence. Root owns integrated build/browser verification; these steps are the reproducible scenario, not a claim they ran.
