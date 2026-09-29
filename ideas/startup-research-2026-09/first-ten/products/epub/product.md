# Proofroom — EPUB accessibility review packets

Proposal dated 2026-09-29 · W0521 · selected order 6 · proposed $39/month.

## Decision and philosophy

Serve freelance ebook formatters working repeatedly with small publishers. The promised outcome is a client-review packet that explains what was found, what a person changed, and which proof the evidence describes. The core object is a **versioned finding with evidence**, rather than an accessibility score.

People decide whether an alternative description is useful, a reading sequence makes sense, and a delivery meets the agreed scope. Software can normalize supplied checker output, locate an issue, retain decisions and identify missing evidence. It must never silently interpret a resolved checkbox as certification. No automated rewriting, legal assurance, assistive-technology claim, or universal accessibility badge belongs in the MVP.

Quiet by default means a working queue and explicit exports. Reminders require opt-in, an owner and a useful pending task. A clean report never triggers marketing or an unsolicited client message.

## Advantage to falsify

[Ace by DAISY](https://daisy.github.io/ace/) already supplies a free accessibility checker. Its [HTML report documentation](https://daisy.github.io/ace/docs/report-html/) describes violations, location details, metadata, outlines and image information that assist human review. Sources checked 2026-09-29. Repackaging those findings is insufficient differentiation.

The narrow hypothesis is that small production teams pay for proof-specific ownership, remediation evidence and client handoff across revisions. Compare directly against Ace HTML output plus a shared spreadsheet. Imported findings and human judgments must remain distinguishable. The packet must save recurring coordination effort; prettier typography alone fails the experiment.

## Core journey and screens

1. Select a publication and proof. See unresolved findings and outstanding human checks.
2. Import a supplied checker report, retaining its tool/version, original identifiers and provenance.
3. Select a file from the publication outline, then a finding. Inspect the source location and explanation.
4. Record an owner, correction and review method. Resolve only that proof’s finding.
5. Finish human checks, prepare a client packet, and record the client decision separately.
6. Create the next proof. Previous evidence remains available; affected checks reopen until reverified.

The mock uses an original publication banner, a file outline, a queue and an evidence inspector. At 1440px these are three working columns. At 820px the outline spans the top. At 390px the sections stack without horizontal page scrolling. The detail panel is a context sample, not a rendered uploaded EPUB. Dialogs cover new proofs and client-review preparation.

Empty: the Open filter shows an explicit completed-queue state. Validation: a unique proof label and evidence of at least 12 characters are required. Conflict: a production stale revision returns a conflict with a compare/reload path; the single-browser mock instead keeps evidence isolated per proof. Failure: malformed reports must be rejected with a field location and no partial mutation. Real report import and asynchronous failure states remain proposed.

## MVP and boundaries

MVP: report JSON import, finding normalization, proof identity, assignees, manual review checklist, evidence notes, version comparison and client packet export. Begin with customer-supplied reports; owning an EPUB checking service is a later decision.

Exclude EPUB editing, OCR, AI description generation, reader emulation, publication hosting, compliance certification and automatic publication. The current mock imports one built-in Ace-style finding; it does not parse files or invoke Ace.

## Domain model and invariants

- `Publication` owns `ProofVersion`; each production version has a content hash and immutable original report.
- `Finding` identity combines proof, source rule and location; it never overwrites a previous proof’s evidence.
- `ReviewEvidence` records author, method, timestamp and the proof being reviewed.
- `ClientReview` refers to a version and a fixed evidence snapshot; later changes make a new review necessary.
- Resolution requires evidence and an owner. All requested human checks remain visible.
- A new proof does not inherit successful checks automatically. The mock conservatively reopens every finding.
- Review completion means the agreed packet was reviewed, not that a legal or technical standard was satisfied.

## Proposed implementation

Use a Vue feature module and a .NET application boundary for publications, proofs, findings and review packets. Candidate shared UI capabilities are labeled forms, validation, dialogs, toasts and selectable lists from `@wow-two-beta/ui-vue`. Verify the pinned package’s actual public exports before replacing native prototype controls; legacy React `@wow-two-beta/ui` is not this target. No SDK method names are assumed here.

Proposed routes: `POST /api/publications`, `POST /api/publications/{id}/proofs`, `POST /api/proofs/{id}/report-imports`, `PATCH /api/findings/{id}`, `POST /api/proofs/{id}/reviews`, and `GET /api/proofs/{id}/packet`. Reads and commands require tenant and publication authorization; a client reviewer can see only its scoped packet.

`ReportImported`, `FindingResolved`, `ProofCreated`, and `ReviewRecorded` are proposed domain events. Imports use an idempotency key plus content hash. Writes require a revision token. Export jobs consume an immutable proof snapshot; repeated jobs produce the same artifact. An optional Ace worker must run without external network access, with archive traversal checks, decompression limits, process timeouts and bounded output. Start without that worker to fit the initial budget.

## Ownership and security

Publishers retain their text, reports and evidence. Allow export and deletion subject to explicitly agreed retention. Store minimal excerpts; never render report HTML directly. Sanitize filenames, treat markup as text, cap report sizes and reject archive bombs if EPUB upload is later added. Use tenant-scoped identifiers and audit sensitive access. Client links, if later implemented, expire and can be revoked. Prototype records remain synthetic JSON in browser storage; there is no authentication or real tenant isolation.

## Economics and experiment

One report can be free. Test $39/month for repeat client libraries, proof history and review packets. Proposed pilot limits: 20 publications, 100 report imports/month and 10MB per report. Keep original media with the customer. Deterministic report handling, capped storage and explicit exports target $20–50/month operating spend before revenue; hosting has not been quoted, and founder time is excluded. Unlock approximately $300/month only after paid renewal and measured load justify it.

Activation: a formatter imports one report and exports a packet containing both machine findings and human evidence. Retention: the same formatter completes a second paid client proof cycle. Compare 20 historical ebooks with ten formatters; seek three paid $39 pilots that renew after another proof cycle. Kill if raw Ace output plus a spreadsheet is equally convenient, or evidence upkeep costs more time than it saves. At $39, 129 active subscriptions yield $5,031 gross MRR; this is arithmetic, not a demand forecast.

## Design references and system

The references above were inspected as documentation, not as visual screenshots. Extracted interaction moves: retain rule/location context, distinguish automatically found issues from manual checks, and use document outlines for navigation. The proof selector and client-review gate are original conceptual proposals. No vendor logo or page layout is copied.

Chosen direction: an editorial workbench with a restrained original book cover, generous reading area and compact issue queue. Root’s three canvas palettes remain selectable proposals; none is a user-approved lock. Both themes use `--canvas` for surroundings, `--surface` for evidence, `--surface-alt` for excerpts, `--ink`/`--muted` for reading hierarchy, and `--accent-soft` for selected findings. Danger and warning are accompanied by text. A proposed reusable pattern is a version selector plus evidence inspector. New proof and client review use native dialogs with labels, keyboard behavior and visible buttons.

## Staged delivery and acceptance

1. Review this local prototype and its task completion flow; choose a canvas direction separately.
2. Run an authorized artifact comparison with real formatters before production investment.
3. Implement import, tenant authorization, immutable proof identity and revision-safe evidence commands.
4. Add packet generation and invite-only client review after proving demand; add sandboxed checking only if needed.

Acceptance requires previous proof evidence to remain unchanged, current-version metrics to recompute, incomplete human checks to block recorded review, and exports to match the selected proof. Production acceptance additionally requires malformed-report tests, authorization tests and replay-safe imports. No runtime checklist is a compliance certification.

## Exact prototype smoke steps

1. Open EPUB and use the shell’s reset control. `Proof 01` shows four open findings and 0% resolved.
2. Click `Save evidence & resolve` with empty evidence. An inline validation error appears; no finding resolves.
3. Enter `Added a contextual diagram description and reviewed it.` Click `Save evidence & resolve`. The queue shows three open findings and 25% resolved.
4. Click `Reopen finding`. Four findings are open again; earlier evidence remains editable.
5. Click `Import supplied Ace findings`. A fifth finding appears; the import button disables.
6. Click `New proof version`, then `Create proof` empty. A unique-label error appears. Enter `Proof 02`, create it, and verify all five checks reopen.
7. Switch to `Proof 01`. Its earlier evidence remains on the original finding.
8. Click `Prepare client review`. Recording review is disabled while findings remain open.
9. Resolve every item using a descriptive note. Open client review and click `Record simulated client review`. The local review badge appears; nothing is sent.
10. Click `Export review packet`. Downloaded JSON names the selected proof and includes current findings/evidence.
11. Reload to verify local persistence; switch theme and check 390px, 820px and 1440px layouts.

Implemented mutations: sample import, resolve, reopen, new proof and simulated client review. Missing capabilities: real report/EPUB parsing, authenticated users, notifications, actual client review and external storage. Root owns integrated build/browser verification; this document supplies the acceptance scenario, not a claim those checks ran.
