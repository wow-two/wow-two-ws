# Naming final acceptance

*Last updated: 2026-09-15*

> Convention acceptance of settled N100/N101 names; SDK implementation remains independently verified.

## Scope

- Read `context.md`, `sdk-naming-inventory.md`, the construct/behavior indexes and affected definitions.
- Accepted naming decisions are supplied by the parent task; stale pending-status prose in those trackers is being reconciled by the parent.
- Inspected Parser, Exporter, Formatter, Transport, Serializer, Bus, Validator, Authenticator, Service and Model rules.
- Preserved the accepted distinctions: metrics and guest-session behavior use Service; identity evidence uses Authenticator; hash integrity uses Validator; actual event payloads retain Event; internal envelopes use Model; the test HTTP mirror uses ApiResponse.
- No SDK build, restore, source mutation, Git operation or release verification was performed by this acceptance lane.

---

## Verified acceptance

- All seven named Parser/Exporter/Formatter/Transport/Serializer/Bus/Validator definitions appear in both role indexes.
- Validator permits structured domain integrity results without FluentValidation inheritance. The validation domain scopes FluentValidation and its SDK consumption rules to input/field validation.
- Parser syntax decoding, Serializer representation encoding/decoding, Formatter display text and Exporter data-exchange output are distinguished by responsibility.
- Authenticator establishes identity from evidence; HashChainValidator therefore does not force the Google identity check into Validator.
- Service already covers orchestration/compute with no narrower role, allowing guest-session and instrumentation behavior without adding Session or Metrics suffixes.
- The retired per-type stored-JSON wrapper remains retired; Serializer points to stored-JSON ownership rather than recreating it.
- Parent repairs verified during this pass: implementation prefixes may name a collaborator without stacking competing suffixes; Formatter retains its suffix without imposing one exact type name globally; Transport routes application publish/send to Bus and workflow orchestration to Service; Validator points to the actual Consumption heading.
- Final whole backend link check: 159 Markdown files, 1,050 local links/heading fragments, zero missing file or heading targets. Heading fragments were checked using generated GitHub-style slugs; no remote-site validation is claimed.

---

## Resolved follow-through

The parent applied both final wording repairs; this lane reread the changed rules and repeated the link/fragment check:

- `core/mla/constructs/data/model.md:36–37` requires initialization before use and explicitly permits application messages while preserving the no-Dto boundary. The wrapped event retains its Event suffix.
- `core/mla/constructs/behavior/validator.md:25–26` and `behavior/service.md:24–25` scope Validates/Provides to concrete implementations and point interface documentation to its inherited owner.

Paths in this section are relative to `conventions/development/backend/dotnet`.

No remaining convention blocker was found in this bounded naming acceptance. The settled vocabulary and applicable definition/index consistency support convention-level BC03/BC25 closure; SDK source completion remains separate.

---

## Implementation boundary

- Accepted suffixes do not prove current SDK folder placement, documentation, runtime behavior or package correctness.
- Parser mixed responsibilities, exporter placement, transport wrappers and shared serialization integration remain source conformance work in the existing SDK sweep.
- Historical inventory names and old verification reports are evidence of earlier states; their presence is not a remaining live declaration or a new convention defect.
- Final status prose and N100/N101 tracker closure are owned by the parent, not by this report.
