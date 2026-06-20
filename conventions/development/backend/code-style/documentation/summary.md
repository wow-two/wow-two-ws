# Summary

*Last updated: 2026-06-17*

> The `<summary>` block — its mandated first word per type-kind (the starter table) + tone. The canonical summary reference; every convention links here.

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

**Defines / Represents / Handles** — the CQRS verb trio, by layer: **Defines** an interface / marker definition · **Represents** a concrete message model · **Handles** a handler. Same three verbs apply to the mediator markers — see [mediator.md](../../messaging/mediator.md) (§ Comment conventions).

## Summary — tightest accurate sentence

- One sentence. Start with the mandated starter word.
- For **capability interfaces** (entity traits with members), prefer `Defines a/an {noun} {that|with} {capability}` over `Defines the contract for {types} that {verb}…`. Shorter, same meaning.
  - ✅ `Defines an entity with creation and update timestamps.`
  - ❌ `Defines the contract for entities that participate in timestamp auditing — CreatedAt populated on insert, UpdatedAt on every update.`
- For an **empty marker interface** (no members — it tags a category rather than imposing a shape), use `Defines the marker for {X}`. Don't call it a "shape" — a marker has none. When the tagged concept is broad, define it inline with an em-dash.
  - ✅ `Defines the marker for an entity — a type persisted to a data store.`
- For **behavior interfaces** (handlers, stampers, service-shaped contracts), `Defines the contract for {action}` is fine — there's no noun to name.
- Don't spill member-level detail into the type summary — the members carry it.
- Drop filler: `the SDK convention`, `with a custom X type` (the type parameter is already visible in the signature).

## Properties on entities + DTOs

- Start with `Gets` or `Gets or sets` — always state what the property holds, even if obvious from name
- Always state the parent entity context: `Gets or sets the kebab-case slug of the channel`, not `Gets or sets the slug`
- PKs / FKs: `<summary>` only — skip `<example>` (UUIDs are self-explanatory; fake values add noise)
- **State what the value is — not who sets it, when, or how.** No "stamped by the interceptor", "populated by the DB", "set at construction". An entity-trait contract describes the field; the population mechanism (interceptor, trigger, app code) is the implementer's choice and must not leak in.
  - ✅ `Gets or sets the timestamp when the entity was created.`
  - ❌ `Gets or sets the UTC timestamp when the entity was created. Stamped by the audit interceptor on insert; preserved on every subsequent update.`
- **Don't restate type-implied facts** — `DateTimeOffset` is already a timestamp (don't write "UTC timestamp"); an interface named `IHasXmin` already implies Postgres (don't repeat "Postgres xmin" on the member)
