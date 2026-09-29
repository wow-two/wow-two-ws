# The first ten: product and implementation review

*Prepared: 2026-09-29 · Status: implementation proposals and interactive prototypes*

The ten confirmed ideas now have a common product philosophy, individual implementation dossiers, and a clickable Vue workspace. The deliverable tests whether each proposed product can explain and complete a valuable task. It does not establish willingness to pay or production reliability.

Open **[prototype.html](prototype.html)** in a browser. Everything needed to render the suite is embedded in that file; no CDN, login, API key, backend, or paid service is required. The editable source is this folder. The source can also be built and served locally using the commands below.

## The recommendation

Keep all ten prototypes available for interviews. Start production validation with **Retainer**, **Documentation example tester**, and **Missing-file monitor**. Select the first production build by paid pilot evidence and access to buyers, not by the relative polish of these mockups. Retainer is the default first choice because an agency can test the entire proposed outcome using a time export and one real client conversation.

Do not launch ten independent production services simultaneously. The same founder must acquire customers, support imports, handle security updates, and learn what people retain. A small prototype costs little; an unattended paid service creates an ongoing obligation. Build a second service when the first has a repeatable acquisition path or a documented reason to stop it.

## Product map

| Order | Product and implementation dossier | Smallest valuable paid outcome | Proposed monthly price | First paid user to recruit |
|---|---|---|---:|---|
| 1 | [Retainer balance tracker](products/retainer/product.md) · W0252 | Agreed balance and extra-work decision for one client period | $39 | Agency owner with recurring retainers |
| 2 | [Documentation example tester](products/docs/product.md) · W0012 | A broken documentation example reaches an accountable maintainer | $39 | Developer-tool team with executable docs |
| 3 | [Missing-file monitor](products/files/product.md) · W0031 | A missed expected file becomes one actionable incident | $39 | Operations lead receiving scheduled exports |
| 4 | [Procedure review tracker](products/procedures/product.md) · W0263 | An existing procedure has a current owner and review receipt | $29 | Operations team maintaining a wiki |
| 5 | [Training seat reconciler](products/training/product.md) · W0289 | A provider closes a cohort with an agreed seat reconciliation | $59 | Independent provider selling team training |
| 6 | [EPUB review workspace](products/epub/product.md) · W0521 | A proof handoff contains version-specific findings and human evidence | $39 | Small EPUB production studio |
| 7 | [Customer promise tracker](products/promises/product.md) · W0276 | Accepted customer commitments receive owner-approved updates | $59 | Small B2B customer-success team |
| 8 | [Vendor renewal deadline tracker](products/renewals/product.md) · W0261 | A verified notice deadline receives an evidenced decision | $29 | Founder or office operations lead |
| 9 | [Environment configuration checker](products/config/product.md) · W0034 | A release distinguishes intentional differences from unexplained drift | $39 | Engineering team with several environments |
| 10 | [Podcast guest readiness tracker](products/podcast/product.md) · W0507 | An episode is ready with verified guest assets and permission evidence | $29 | Producer handling multiple recurring shows |

All prices are hypotheses. The market research established competing products and plausible workflows; it did not verify these prices with customers. Dossiers name the incumbent/free substitute that each product must beat.

## What to review

1. Open a product and complete its main workflow. Use **Reset sample** to restore only that product.
2. Change data and inspect the resulting balance, status, or decision record. Exports reflect current sample state.
3. Open **Design review** to compare Mist, Paper, and Porcelain canvases in context. These are proposals, not approved design locks.
4. Try **Preview state** for first-visit, loading, and recoverable connection-error design. Those controls preserve saved data.
5. Read the product dossier for the actual backend invariants, roles, integration boundaries, launch gates, and remaining mock behavior.

## What works and what remains proposed

| Implemented in the prototype | Proposed for production |
|---|---|
| Ten Vue workspaces with distinct task layouts | Ten independently authorized product repositories |
| Interactive selection, forms, validation, workflow mutations | Authenticated tenant-scoped APIs and durable server storage |
| Browser-local persistence and sample-data reset | Multi-user concurrency, audit retention, backups and restore |
| Downloadable evidence/ledger/reconciliation artifacts | Real input connectors and verifiable remote receipts |
| Explicit simulated approvals and imported fixture results | Identity-bound approvals and customer-owned runners |
| Light/dark themes, palette proposals, responsive shell | Full assistive-technology audit and production telemetry |
| No paid APIs or external requests required | Billing, email delivery, secrets management and abuse controls |

## Revenue arithmetic, not a forecast

At the proposed prices, a single product needs roughly **129 customers at $39**, **85 at $59**, or **173 at $29** to exceed $5,000 gross monthly recurring revenue. Three $39 products with 50, 40, and 40 paying accounts total **$5,070 gross MRR**. Payment fees, refunds, discounts, taxes, acquisition expense, infrastructure, and founder time reduce the amount retained.

The portfolio does not diversify distribution automatically. Ten tools sold through the same unproven acquisition channel can fail together. Validate a buyer and repeatable route to that buyer for every product.

## Analysis and engineering documents

- [Product philosophy](product-philosophy.md): common principles and how each product interprets them.
- [Implementation plan](implementation-plan.md): production architecture, reusable vectors, effort, budget and validation gates.
- [Design analysis](design-analysis.md): layout choices, token proposals, states, accessibility and reference evidence.
- [Verification](verification.md): checks actually executed and limits of those checks.
- [Earlier market research](../startup-research-2026-09.md): the source of the confirmed shortlist.

## Reproduce or edit

The local prototype uses Vue 3.5.41, TypeScript 5.9.3, Vite 6.4.3 and Tailwind 4.3.3, with the locally available Vue SDK 0.0.7. Existing SDK dependencies were reused through ignored local symlinks; no SDK source or package registry was modified. A fresh environment needs those exact dependencies and access to the matching SDK package.

```sh
npm run check
npm run build
node make-portable.mjs
python3 preview.py
```

`preview.py` binds only to an ephemeral `127.0.0.1` port and serves `dist/`. It is an unauthenticated static research preview, not a product deployment. The portable file remains usable after the temporary preview server stops. Browser storage is local to its origin; opening the portable file and the server may use different sample state. Private browsing or blocked storage can prevent persistence; exports still work.
