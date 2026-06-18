# Documentation

*Last updated: 2026-06-17*

## XML doc format

- **One-liner by default** — `<summary>`, `<remarks>`, `<example>` content is a compact single line
- **Inline tags** — opening and closing tags on the same line as the content, never on separate lines
- **Exception** — `<remarks>` with numbered flow steps (3+ steps) may use multi-line for readability

```csharp
// ✅ Correct — compact one-liner, tags inline
/// <summary>Defines a handler for extracting phone numbers from a listing via HTTP.</summary>
/// <remarks>Single responsibility — no image extraction, no browser dependency.</remarks>

// ✅ OK — multi-line remarks for numbered flow (exception)
/// <summary>Provides channel and pipeline seeding on application startup.</summary>
/// <remarks>
/// Seed flow:
///   1. Read channels from seed file
///   2. Upsert channels + sources via EF Core
///   3. Insert missing pipeline rows with code defaults
/// </remarks>

// ❌ Wrong — multi-line summary, tags on separate lines
/// <summary>
/// Defines an extraction handler for browser-based data.
/// Each channel implements its own logic.
/// </summary>
```

## Required tags per type-kind

`/// <summary>` is required on every public type and member. `/// <example>` is required where the table below marks it.

| Type-kind | Required tags | Notes |
|---|---|---|
| Interface | `<summary>` | No `<example>` — interfaces define shape, examples are for implementations |
| Enum | `<summary>` + `<example>` (when/where used) | Plus `<summary>` + `<example>` on each value |
| Entity (record mapping to table) | `<summary>` + `<example>` (entity description) | Per-member `<summary>` + `<example>`; PKs/FKs skip `<example>` |
| DTO | `<summary>` + `<example>` | Same as entity |
| Settings record | `<summary>` + `<example>` (appsettings section name) | Per-member `<summary>` + `<example>` |
| Service / Client / Repository | `<summary>` + `<remarks>` (flow / key behavior) | Methods get `<summary>` one-liner |
| Static class (constants, helpers, registries) | `<summary>` | Members may or may not need `<summary>` depending on visibility |
| Extension class | `<summary>` (purpose of the extensions) | Each extension method gets its own `<summary>` |
| Configuration class (EF `IEntityTypeConfiguration<T>`) | `<summary>` one-liner | No `<remarks>` or `<example>` |
| Handler (query/command) | `<summary>` = `Handles <see cref="{Q|C}"/>.` | Nothing else |
| Result type (Success/Failure containers) | `<summary>` + `<example>` on the abstract base and each variant | Members per the entity rule |

## Starter table (REQUIRED)

The first word of every `<summary>` is fixed by type-kind. This is the canonical reference — every other file in `conventions/` links here.

| Type-kind | Starter | Example |
|---|---|---|
| Interface | **Defines** | `Defines the contract for stamping audit fields on save.` |
| Enum | **Defines** | `Defines the execution status of a pipeline run.` |
| Enum value | (describe the meaning, no fixed verb) | `Pipeline finished successfully.` |
| Entity / record / model class | **Represents** | `Represents an external listing channel.` |
| DTO | **Represents** (or describe projection) | `Represents a flat channel projection for the CRM grid.` |
| Service | **Provides** | `Provides channel and pipeline seeding on application startup.` |
| Client (HTTP wrapper) | **Wraps** or **Integrates with** | `Wraps the Telegram Bot API for sending messages and managing topics.` |
| Factory | **Creates** | `Creates AI clients keyed by provider + model tier.` |
| Repository | **Fetches** (read-heavy) or **Persists** (write-heavy) | `Fetches unclassified listings via Dapper.` |
| CQRS marker / handler interface (`IQuery`, `ICommand`, `IQueryHandler`, …) | **Defines** | `Defines a query that returns <typeparamref name="TResult"/>.` |
| Query/Command (concrete CQRS message) | **Represents** | `Represents a query to get all channels with their pipelines and sources.` |
| Query/Command handler | **Handles `<see cref="X"/>`** | `Handles <see cref="ChannelGetAllQuery"/>.` |
| Static constants class | **Contains** | `Contains the canonical kebab-case slugs for every channel.` |
| Static registry class | **Tracks** or **Holds** | `Tracks live pipeline executions keyed by pipeline id.` |
| Extension class | **Provides** | `Provides registration extensions for the time wrapper.` |
| Extension method | (verb at start: `Adds`, `Uses`, `Maps`, `Configures`) | `Adds the JWT bearer authentication scheme with sane defaults.` |
| Configuration class (settings record) | **Configuration for** | `Configuration for AI classification pipeline behavior.` |
| EF `IEntityTypeConfiguration<T>` class | **Configures** | `Configures the listings table mapping and relationships.` |
| HostConfiguration extension | **Configures** | `Configures typed HTTP clients for external API integrations.` |
| Hosted service | **Runs** or **Schedules** | `Runs EF Core migrations on application startup with connect-retry.` |
| Result base (abstract) | **Represents the outcome of** | `Represents the outcome of reading seed data for an entity type.` |
| Result `Success` variant | (describe the success state) | `Seed data read successfully — entities ready for upsert.` |
| Result `Failure` variant | (describe the failure state) | `Seed data read failed — error tracked for diagnostics.` |
| Property (read-only) | **Gets** | `Gets the kebab-case slug of the channel.` |
| Property (read-write) | **Gets or sets** | `Gets or sets the kebab-case slug of the channel.` |
| Method (action) | Verb at start: `Adds`, `Gets`, `Creates`, `Sends`, `Configures`, `Maps`, `Builds` | `Sends the OTP to the resolved Telegram chat.` |
| Controller (class) | **Manages** (resource) · **Reports** (non-resource) | `Manages portfolio products.` · `Reports the vault's seal state.` |
| Controller action | Verb at start (HTTP method shape): `Gets`, `Creates`, `Updates`, `Deletes`, `Executes`, `Cancels` | `Gets all channels with their pipelines.` |
| Request model (`{Verb}{Noun}ApiRequest`) | **Represents** | `Represents the create-code request body.` |

A doc violating the starter table is a style miss regardless of content quality.

**Defines / Represents / Handles** — the CQRS verb trio, by layer: **Defines** an interface / marker definition · **Represents** a concrete message model · **Handles** a handler. Same three verbs apply to the mediator markers — see [mediator.md](../messaging/mediator.md) (§ Comment conventions).

## Summary & remarks tone

### Summary — tightest accurate sentence

- One sentence. Start with the mandated starter word.
- For **capability interfaces** (entity traits with members), prefer `Defines a/an {noun} {that|with} {capability}` over `Defines the contract for {types} that {verb}…`. Shorter, same meaning.
  - ✅ `Defines an entity with creation and update timestamps.`
  - ❌ `Defines the contract for entities that participate in timestamp auditing — CreatedAt populated on insert, UpdatedAt on every update.`
- For an **empty marker interface** (no members — it tags a category rather than imposing a shape), use `Defines the marker for {X}`. Don't call it a "shape" — a marker has none. When the tagged concept is broad, define it inline with an em-dash.
  - ✅ `Defines the marker for an entity — a type persisted to a data store.`
- For **behavior interfaces** (handlers, stampers, service-shaped contracts), `Defines the contract for {action}` is fine — there's no noun to name.
- Don't spill member-level detail into the type summary — the members carry it.
- Drop filler: `the SDK convention`, `with a custom X type` (the type parameter is already visible in the signature).

### Remarks — directive, not explanatory

`<remarks>` tells the consumer **what to do**, not how the SDK works internally.

- Open with an imperative: `Use with …`, `Wire via …`, `For X, prefer …`, `Populate … at construction.`
- Cut tech-facts and rationale — performance reasoning, compiler-quirk explanations, provider/EF behavior, "throws X on drift", who-reads-the-value.
  - ✅ `For Postgres, prefer <see cref="IHasXmin"/> instead.`
  - ❌ `Maps to SqlServer's 8-byte rowversion column; EF Core throws DbUpdateConcurrencyException when the stored value drifts from the original.`
- Omit `<remarks>` entirely when the summary already says enough.

## Member docs — additional rules

### Parameters

- Document **every** parameter with a compact `<param name="x">` — noun phrase, no filler, no type restatement.
  - ✅ `<param name="appliedBy">The host stamp recorded on each applied row.</param>`
  - ❌ `<param name="appliedBy">A string that is the value used for the appliedBy column.</param>`

### Exceptions

- A method documents the exceptions **it itself throws** with `/// <exception cref="…">{trigger}</exception>` — **not** exceptions propagated from callees (inner / nested).
  - ✅ `<exception cref="MigrationDriftException">An applied migration's checksum no longer matches its source.</exception>`

### Properties on entities + DTOs

- Start with `Gets` or `Gets or sets` — always state what the property holds, even if obvious from name
- Always state the parent entity context: `Gets or sets the kebab-case slug of the channel`, not `Gets or sets the slug`
- PKs / FKs: `<summary>` only — skip `<example>` (UUIDs are self-explanatory; fake values add noise)
- **State what the value is — not who sets it, when, or how.** No "stamped by the interceptor", "populated by the DB", "set at construction". An entity-trait contract describes the field; the population mechanism (interceptor, trigger, app code) is the implementer's choice and must not leak in.
  - ✅ `Gets or sets the timestamp when the entity was created.`
  - ❌ `Gets or sets the UTC timestamp when the entity was created. Stamped by the audit interceptor on insert; preserved on every subsequent update.`
- **Don't restate type-implied facts** — `DateTimeOffset` is already a timestamp (don't write "UTC timestamp"); an interface named `IHasXmin` already implies Postgres (don't repeat "Postgres xmin" on the member)

### `<example>` content rules

`<example>` values must be **human-readable** — no C# type names, class names, or code identifiers in the example body:

- ✅ `Collection of channels` — not ❌ `Collection of ChannelEntity`
- ✅ `Seed file missing from expected path` — not ❌ `SeedFailure.FileNotFound`
- ✅ Describe the meaning, not the C# value

Use `<see cref="..."/>` inside `<summary>` when referencing code; reserve `<example>` for runtime values or descriptions.

### Cross-references

- `<see cref="X"/>` for inline references inside `<summary>` and `<remarks>` — the IDE resolves the link
- Never paste a type name as plain text when a `<see cref>` would link it

## Terminology

- **Collection** — use "collection" in `<summary>` and `<example>` when referring to any grouping type (`List<T>`, `T[]`, `Dictionary<K,V>`, etc.). Keeps docs stable when the implementation type changes.
- **The {entity}** — refer to the owning entity by name (`the channel`, `the listing`), not by C# type name in prose. The type name belongs in `<see cref>`.

## Inline comments (within method bodies)

Explain a non-trivial step with an **imperative one-liner** in step/order tone — present-tense verb, essentials only, one line. Skip when the code is self-evident.

```csharp
// Acquire the advisory lock so only one host migrates at a time.
await dialect.AcquireLockAsync(connection, ct);

// Fetch the applied set, then diff against the source.
var applied = await history.GetAppliedAsync(connection, ct);
```

- ✅ `// Skip the Dev folder — it holds unpromoted drafts.`
- ❌ `// This loop iterates over the directories and for each one it checks whether…` (multi-line / restates code)

## What NOT to document

- Internal types and members — XML doc is generated by `<GenerateDocumentationFile>` but warnings are suppressed; brief one-liners only if context isn't obvious
- Auto-generated code — skip
- `Program.cs` 3-liner — skip
- Test classes / methods — name carries the meaning

## See also

- [models.md](models.md) — record style + general property rules
- [entities.md](../persistence/entities.md) — entity-specific doc rules
- [enums.md](../persistence/enums.md) — enum value documentation
- [services.md](../architecture/services.md) — service / client / factory naming
- [mediator.md](../messaging/mediator.md) — query/command/handler naming + docs
