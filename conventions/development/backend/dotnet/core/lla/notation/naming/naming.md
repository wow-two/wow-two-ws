# Naming

*Last updated: 2026-09-10*

> Cross-cutting naming for backend types, members, and extension methods — the symbol name,
> never its file, namespace, or project.
> Purpose — the name says what a thing *does*; the brand lives in the package, never inside the code it ships.
> Use case — reach for it whenever you name a class, method, extension, or a bool-returning member.

## No brand / product prefix

- a **type, member, or extension-method** name carries **no product / brand prefix**
- `MigrateDatabaseAsync` not `MigrateSmartQrDatabaseAsync` · `DatabaseContext` not `SmartQrDbContext`
- **project / package names keep the brand** — `SmartQr.Api`, `WoW.Two.Sdk.Backend.Beta`
  - the carve-out is the name identifying the *assembly*, never the code inside it
- every symbol under `SmartQr.*` is already smart-qr's; the prefix tells a reader nothing the namespace doesn't

---

## `using static` is banned

- **never `using static`** on an extensions class or any other type — it strips the class name off the call site
  - `Clean(value)` no longer says which extension it came from
- call through the class — `ContentEncodingExtensions.Clean(value)`
  - or make it a real extension method, so the receiver carries the origin: `content.ToPayload()`
- bare function calls read as another language — C# puts the owning type in the call for readability.

---

## Predicates — `Is` / `Has` / `Can`

- a **bool-returning** method or property starts with `Is` / `Has` / `Can` (or `Should` / `Was` by tense), never `Be`
- `IsAbsoluteHttpUrl` not `BeAbsoluteHttpUrl` · `HasPendingChanges` · `CanRetry`
- `Be*` is FluentValidation slang (`.Must(BeValid)`) — it reads as an assertion, not a state query
  - keep it out of method names even when the method backs a `.Must(...)`

---

## Acronyms

- **Acronyms are always PascalCase, never all-caps** — `Id` not `ID`, `Api` not `API`, `Sql`, `Http`, `Json`, `Ui`.
- First letter capital, rest lowercase, **even when it distorts an established acronym**.
- Applies to type / namespace / folder / member names.
- Governs *all-caps runs* only — a mixed-case proper name (`OAuth`, `SendGrid`, `MailKit`) is unaffected.
- Canonical for the whole ecosystem — the backend-beta SDK follows it too
  (`engineering/architecture/package-layout.md`).

---

## Banned

- **Hungarian notation** — `m_`, `s_`, a leading `_` on anything but a private field.
