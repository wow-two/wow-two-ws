# Backend convention acceptance — 2026-09-13

Scope: read-only acceptance of settled P01–P06 plus P07 references while root applies P07. Files under `conventions/development/backend/dotnet`; no SDK source inspection, package restore, repository mutation or Git operation. Current `context.md` and `conventions-audit.md` used, historical reports treated as historical. P08 and N100/N101 deliberately excluded.

## P08 follow-up — root verification

P08 is now applied: per-type Json role/static exception removed, stored JSON moved to the persistence owner,
HTTP links to that separate contract, component/construct indexes reconciled. All 973 local file/heading
targets across the 153 current backend documents resolve under the same simple slug check. Whitespace checks
pass in both repositories. N100/N101 remain excluded; this is not final acceptance of their naming decisions
or runtime SDK verification. Findings below preserve the earlier pre-repair evidence.

## Findings

### A01 — Qualify the validator-type requirement for extension-only validation

- File: `conventions/development/backend/dotnet/core/mla/domains/validation/validation.md:9` and `:13`.
- Current contract says `must use a validator for caller-supplied payloads` and `must define a dedicated validator type through the validator construct` without qualifying when a dedicated type is chosen.
- Same file `:20` permits a pure validation extension method for a small rule set. P02 explicitly settled extension methods OR dedicated validators.
- This is a current wording ambiguity, not a demonstrated runtime defect: an adopter reading Contract literally can require a class even for the permitted extension-only case.
- Mechanical repair: distinguish external validation from a dedicated validator type in Contract; make the construct instruction conditional on authoring a dedicated validator. Retain provider/consumer integration for the dedicated-validator path.

### A02 — Remove repeated ownership of settled rules

- `conventions/development/backend/dotnet/core/mla/constructs/patterns/prototype.md:51` repeats the original-instance tracked-write obligation and copied-replacement prohibition owned by `core/mla/domains/persistence/access/ef/ef.md:25–28`.
- `conventions/development/backend/dotnet/core/mla/mla.md:23` and `core/mla/constructs/data/api-request.md:16` repeat the same-file mapping-companion obligation owned by `core/mla/domains/api/api-messages.md:46`.
- These statements currently agree. They are ownership duplication under root `conventions/conventions.md`'s explicit one-owner rule, not a new design fork or conflicting runtime behavior.
- Mechanical repair: keep each obligation at its application owner; replace repetitions with scoped references. The general file rule already permits explicitly scoped companion exceptions at `core/lla/constructs/constructs.md:112`.

## Acceptance evidence

- Enumerated Markdown links throughout `conventions/development/backend/dotnet`: all relative local file targets exist.
- Enumerated local Markdown `#fragment` links throughout the same tree: all resolve to a matching generated heading anchor (simple GitHub-style slug computation; no website rendering claimed).
- Focused searches found no remaining blanket class-entity conversion, handwritten-equality ban, constructor-validity default, omission-as-ban wording, or handler-to-handler request-send example in current normative files.
- Entity declaration, comparison scope, hash-key stability and original-instance EF writes agree.
- Explicit value-object equality includes matching hashing and order/duplicate semantics.
- FastCloner is the selected graph-copy convention; execution verification remains a separate documented SDK task. No new library result is claimed.
- Request mapping companion exceptions cover file, folder, naming and summary; complex HTTP bodies are not misrepresented as technically impossible.
- Handler reuse uses services; direct handler calls and service-hidden nested sends are prohibited; event publication remains distinct.
- P07's pre-edit Open entry was observed but excluded as root's active edit, not a new finding.

No additional behavioral decision is required by this bounded acceptance pass.

## Root disposition

All A01/A02 cleanup applied: external method/dedicated-validator alternatives are explicit, the dedicated-type rule is conditional, and tracked-write/request-companion duplicates now link to their owners. P07 was applied in the service testing owner and linked from SDK testing. This report retains pre-repair finding locations; source lines can move. Final whitespace and affected link checks passed. P08 and N100/N101 remain outside this bounded acceptance verdict.
