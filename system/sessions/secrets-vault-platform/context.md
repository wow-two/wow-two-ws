# Handoff — secrets-vault `v0.2` (Full SDK migration)

*Super-compact. Resume cold from here. Date: 2026-06-26.*

## Paths
- **Vault**: `wow-two-ws/workbench/wow-two-platform/wow-two-platform.secrets-vault/` → backend `engineering/codebase/secrets-vault.backend-services/Wow-Two-Platform.Secrets-Vault.sln` · frontend `…/secrets-vault.frontend-services/` (React 19 / Vite).
- **Kit (SDK)**: `wow-two-sdk-beta/wow-two-sdk.backend.beta/` — pinned **`10.0.40-beta`**. Extracted leaves: `src/Foundation/Security` (envelope crypto) · `src/Foundation/Audit` (hash-chain).
- **forever-pin** (mirror for result-model + tests): `ventures/10x-venture-forever-pin/`.
- **Version docs**: vault `engineering/versions/v0.2/{v0.2.md, v0.2-analysis.md}` · `versions.md` · `engineering/planning/backlog.md`.
- **Version-doc convention**: `wow-two-ws/conventions/planning/version-planning/version-docs.md`.

## `v0.2` status (Type: Adoption · 10 iterations) — only 9+10 LEFT
| # | Iteration | State |
|---|---|---|
| 1 | Request pipeline (mediator + result envelope + entities) | done |
| 2 | Time + enum storage (`TimeProvider`, enums-as-text) | done |
| 3 | Host floor (`AddApiDefaults`/`UseApiDefaults` + kit JWT bearer) | done |
| 4 | Persistence base (`AppDbContextBase`) | done |
| 5 | Envelope cryptography (extract + adopt) | done |
| 6 | Hash-chained audit (extract + adopt) | done |
| 7 | Test harness (SDK `Testing` + `Testing.Data`) | done |
| 8 | Test structure (unit / integration / migrations tiering) | done |
| 9 | **Console UI — adopt `@wow-two-beta/ui`** (component swap, layout unchanged) | **TODO** |
| 10 | **Verification** | **TODO** |

Build green on `40`; **66 unit tests pass**. Integration + migrations tiers need Docker (Postgres) — not yet run.

## How things are wired now (post-adoption)
- **Result model**: single `AppResult<T>` (`Mediator.Result`) + `AppError`/`AppErrorType` (`Foundation.Errors`); fail = `AppErrors.X("msg")`; controllers `result.Match(ok=>…, fail=>this.ToProblem(fail.Error))` (`Api/ControllerProblemExtensions.cs`, SDK error→HTTP mapper via `AddApiDefaults`). Deleted: `FailureCategory`, `ISecretsVaultFailure`, `Api/ApiResults.cs`; `*Result.cs` = `Success`-only.
- **Crypto**: `AddEnvelopeCryptography(o => o.MasterKeyEnvironmentVariable="VAULT_MASTER_KEY")`; SDK `ICryptoCore`/`ISealKeeper`/`EncryptedPayload` from `Foundation.Security`; **AAD stays vault-side** (`$"{ns}/{key}"`, `$"dek:{ns}"`). ⚠️ malformed key → `MasterKeyFormatException` on `Unseal()` (fail-fast at boot).
- **Audit**: `AuditEntry : IHashChainedEntry`; `Domain/Audit/AuditEntryCanonicalizer` (domain fields only — SDK prepends Scheme+Sequence+PreviousHash); `AddHashChain<AuditEntry,AuditEntryCanonicalizer>()`; `EfAuditLog` injects `IHashChainSealer` → `Seal(entry,last)`.
- **Time**: BCL `TimeProvider` via `AddTimeProviders()`; tests use `Microsoft.Extensions.TimeProvider.Testing` `FakeTimeProvider`.
- **Tests**: `SecretsVault.Tests` (unit) · `SecretsVault.Tests.Integration` (`Harness/Tests/Support`) · `SecretsVault.Tests.Migrations` (`Testing.Data`).

## Git
- Last commit `f94f38a feat: adopted sdk layers` (the PRE-this-adoption checkpoint).
- **UNCOMMITTED**: this whole backend adoption (re-pin `40` + result migration + crypto/audit/time) + the `v0.2.md` ticks. Big change. **Developer commits manually — don't run git writes** (stage only on explicit ask). Suggested msg: `feat: adopt SDK 10.0.40 — AppResult<T> + envelope crypto + hash-chain audit + TimeProvider`.
- Separate repo `wow-two-ws`: convention edits (response-style no-tick rule + backend-conventions reorg by another lane) — own commit.

## Next (do in order)
1. **Commit** the backend adoption (offer to stage).
2. **Iter 9 — frontend** `@wow-two-beta/ui`: swap `LoginForm`, `SetSecretForm`, `TokenRevealModal`, `ErrorBanner`, `Spinner`, `SealStatus`, `SecretsTable`, `NamespacePanel`, `TokensPanel` for the lib (keep API client + auth gate; **layout unchanged**). Confirm the lib's component API first. FE proxy → `https://localhost:8200` (`secure:false`).
3. **Iter 10 — verify**: run integration + migrations on Docker; live smoke (login → manage ns/secrets/tokens → resolve via data-plane token → cross-ns 403 → sealed 503). Tick `[x]` + flip `Status` → Complete.

## Gotchas / conventions
- **No `✅`/`❌`/tick emoji** (chat or doc headings) — words + `[x]`. (Now in `response-style.md`.)
- **Version docs**: `**Type:**` field; iteration name = bare noun (no `: goal`); Adoption verbs `Adopt …`/`Extract … → SDK`; no heading emoji; Verification is the last iteration. Tick `[x]` as each lands.
- **Run backend**: `https` launch profile (binds 8200) + env `VAULT_MASTER_KEY` (base64 32) + `VAULT_ADMIN_PASSWORD_HASH` (Argon2id PHC). Admin login works while sealed. Generate hash via the kit's `Argon2PasswordHasher<T>.HashPassword`.
- **Lanes**: multiple chats edit the vault; the errors-model/settings/CQRS lane has landed. Stay in lane; assume existing changes are intentional.
- **Deferred**: a full UI **layout redesign** (distinct from the Iter-9 component swap) → backlog, next Feature version.
- Memories: `project_errors_layer_investigation` (now adopted), `reference_kit_jwt_bearer_init_only_bug` (fixed+shipped).
