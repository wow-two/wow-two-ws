# Summary

*Last updated: 2026-09-10*

> The `<summary>` block — the mandated first word per type-kind, plus tone. The canonical summary reference.

## Starter table [REQUIRED]

The first word of every `<summary>` is fixed by what the thing is.

- must take a **type's** starter from its own doc — [components](../../../mla/components/components.md)
  or [constructs](../../../mla/constructs/constructs.md).
- must take a **member's** starter from [constructs](../../constructs/constructs.md), which fixes them by role.
- must take a **construct's** starter from the same file, which rules on every C# form.
- must not reintroduce a table here — a starter belongs with the thing it starts.

---

## Summary — tightest accurate sentence

- must be one sentence, opening with the mandated starter word.
- **capability interface** (entity trait with members) — `Defines a/an {noun} {that|with} {capability}`, never
  `Defines the contract for {types} that {verb}…`
  - ✅ `Defines an entity with creation and update timestamps.`
  - ❌ `Defines the contract for entities that participate in timestamp auditing, CreatedAt and UpdatedAt.`
- **empty marker interface** (no members, tags a category) — `Defines the marker for {X}`.
  - must not call it a "shape" — a marker has none.
  - must define a broad tagged concept inline, with an em-dash.
  - ✅ `Defines the marker for an entity — a type persisted to a data store.`
- **`the contract for` is banned after `Defines`** — the verb declares one.
  - name the capability directly.
  - ✅ `Defines audit-field stamping on save.`
  - ❌ `Defines the contract for stamping audit fields on save.`
- **behavior interface** (handler, stamper, service-shaped contract) — name the action as a noun phrase.
  - ✅ `Defines JWT issuance for an admin session.`
- must not spill member-level detail into the type summary — the members carry it.
- must drop filler — `the SDK convention`, `with a custom X type`.
  - the signature already shows the type parameter.
- indexer summary content → [indexers](../../components/indexers.md).

---

## The falsifiability test [REQUIRED]

One question decides whether a `<summary>` defines the type or describes today's arrangement:

> **Could this sentence go false without the type changing?**

If yes, it is not a definition — it records a circumstance, which rots while the type stays put.

Companion rule: **a summary states the referent (what the thing *is*), never an affordance (what a consumer can
*do* with it)** — an affordance is a fact about callers, and callers change.

### The six shapes that fail it

- **Circumstance as definition** — `The domain model, wire DTO and stored shape in one.` → wire model splits off
- **Affordance as identity** — `Represents a phone number dialed on scan.` → a click-to-copy path ships
- **Implementation as identity** — `A contact card — encodes to a vCard 3.0 payload.` → the encoding changes
- **Inventory or count** — `The 10 content variants.` → an eleventh arrives
- **Relationship as identity** — `The counterpart of <see cref="CodeRuleSet"/>.` → the sibling is renamed or deleted
- **Status or lifecycle** — `The new replacement for the old resolver.` → "new" stops being true, immediately

### Applying it

- must run it on every `<summary>` written or touched.
- a failing sentence is not always deleted — ask where the fact belongs.
  - `documentation.md` § *Where a fact belongs* routes it, often to `<remarks>` (a directive) or a `//`.
- it composes with the anti-pattern catalogue, never duplicates it.
  - the catalogue asks *does this belong here*; the test asks *is this a definition at all*.
  - a sentence can pass one and fail the other.
- **`<remarks>` is exempt** — a directive may describe the present, and is expected to stop being true.
  - `Swap in MaxMind GeoLite2 to make country rules match.`

---

## Properties on entities + DTOs

- accessor starters → [language constructs](../../constructs/constructs.md) § *Member documentation*.
- must state what the property holds, even when the name shows it.
- must apply the accessor starter to the consumer-visible accessors; initialization is not a later write.
- applies to every C# model kind, value objects included.
  - must not carry the frontend's bare noun phrase across — `The network name.` is the TypeScript style.
  - C# has properties, and the accessor is what the starter names.
- a method producing a formatted payload takes `<inheritdoc />` + `<remarks>`, never a re-described `<summary>`.
  - a summary spelling the format out (`Builds the <c>WIFI:T:…;S:…;;</c> payload`) restates the code and goes stale.
  - `<remarks>` carries only what the code doesn't show — escaping rules, an omitted segment, a spec quirk.
- must name the referent only when the value is not the type's own
  ([documentation](documentation.md) § *Name the referent*).
  - ✅ `Gets the order of the rule that matched the scan`
  - `ChannelEntity.Slug` takes a bare `Gets or sets the kebab-case slug`
- PKs / FKs take a `<summary>` like every other member — state what the key identifies.
- must state what the value is, never who sets it, when, or how.
  - no "stamped by the interceptor", no "populated by the DB".
  - an entity-trait contract describes the field; the population mechanism is the implementer's choice.
  - ✅ `Gets or sets the timestamp when the entity was created.`
  - ❌ `Gets or sets the UTC timestamp when the entity was created. Stamped by the audit interceptor on insert.`
- must not restate a type-implied fact.
  - `DateTimeOffset` is already a timestamp — never "UTC timestamp".
  - `IHasXmin` already implies Postgres — never "Postgres xmin" on the member.

---

## Fields

- field starters and collaborator exclusions →
  [language constructs](../../constructs/constructs.md) § *Member documentation*.
- value summaries must state the authority that fixes the choice →
  [constants](../../../mla/components/constants.md).
