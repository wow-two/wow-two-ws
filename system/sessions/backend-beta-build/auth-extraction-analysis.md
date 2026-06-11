# Auth extraction analysis — Haven.Auth → backend.beta

*Last updated: 2026-05-07*

## Goal

Extract Haven.Auth (passwordless phone-OTP login + Telegram bot delivery + JWT issuance + role gating) into the `wow-two-sdk.backend.beta` SDK, split cleanly into **abstract** building blocks (ship in SDK) and **specific** consumer-supplied pieces (stay in Haven, wire via DI).

The SDK already ships JWT bearer *validation*, OAuth providers (Google/Microsoft/GitHub/Apple), MFA TOTP, MFA WebAuthn, Argon2 password hashing — but **not** JWT *issuance*, **not** OTP, **not** OTP delivery channels, **not** role-policy abstraction. Haven fills these gaps.

---

## 1. The Haven.Auth flow at a glance

Three endpoints, two flows, one DB:

```
┌──────────────────────────────────────────────────────────────────────┐
│  Flow A — Passwordless OTP login (web UI)                            │
│                                                                      │
│  Web UI                                                              │
│    │                                                                 │
│    │ POST /auth/request-otp { phone, service }                       │
│    ▼                                                                 │
│  AuthController.RequestOtp                                           │
│    │                                                                 │
│    ├── IUserRepository.LookupByPhoneAsync(phone)                     │
│    │     └─→ users JOIN user_phones (Npgsql raw SQL)                 │
│    │     ├─→ 404 if not found                                        │
│    │     ├─→ 403 if !is_active                                       │
│    │     └─→ 422 "bot_not_linked" if telegram_user_id IS NULL        │
│    │                                                                 │
│    ├── IOtpService.CreateAsync(phone, service)                       │
│    │     ├─→ rate-limit check (5s window, unconsumed OTPs)           │
│    │     ├─→ generate 6-digit code (Random.Shared.Next)              │
│    │     ├─→ INSERT INTO otp_codes (TTL 5 min)                       │
│    │     └─→ return code                                             │
│    │                                                                 │
│    └── ITelegramService.SendOtpAsync(telegramUserId, code, service)  │
│          └─→ TelegramBotClient.SendMessageAsync                      │
│          └─→ 502 "telegram_send_failed" on exception                 │
│                                                                      │
│  Web UI                                                              │
│    │                                                                 │
│    │ POST /auth/verify-otp { phone, code, service }                  │
│    ▼                                                                 │
│  AuthController.VerifyOtp                                            │
│    │                                                                 │
│    ├── IOtpService.VerifyAsync(phone, code, service)                 │
│    │     ├─→ SELECT FROM otp_codes WHERE matches & !used             │
│    │     ├─→ check expiry / attempts (max 5) / service               │
│    │     ├─→ UPDATE used = true on success                           │
│    │     └─→ UPDATE attempts++ on wrong code                         │
│    │                                                                 │
│    ├── IUserRepository.LookupByPhoneAsync(phone) again               │
│    ├── role check against AllowedRoles[service] dict                 │
│    └── ITokenService.Generate(user, phone, service)                  │
│          └─→ HS256 JWT, 24h, claims: sub, phone, role, user_role,    │
│                                user_name, aud, iat, exp              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  Flow B — Telegram bot link (one-time setup, prerequisite for A)     │
│                                                                      │
│  Telegram client                                                     │
│    │                                                                 │
│    │ /start @haven_agents_bot                                        │
│    ▼                                                                 │
│  Telegram cloud → webhook → AuthController.HandleWebhook(Update)     │
│    │                                                                 │
│    └── ITelegramService.HandleWebhookAsync(update)                   │
│          ├─→ /start: send "Share Contact" reply keyboard             │
│          └─→ Contact message:                                        │
│                ├─→ PhoneNormalizer.Normalize(phone)                  │
│                ├─→ IUserRepository.LookupByPhoneAsync(phone)         │
│                │     ├─→ "phone_not_registered" if not found         │
│                │     └─→ "already_linked" if linked elsewhere        │
│                ├─→ IUserRepository.LinkTelegramAsync(userId, chatId) │
│                │     └─→ UPDATE users SET telegram_user_id           │
│                └─→ send "✅ Linked!" confirmation                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Storage:** PostgreSQL (Supabase Session Pooler), 3 tables — `users`, `user_phones`, `otp_codes`. Direct Npgsql ADO.NET (no EF, no Dapper).

**Auth signing:** Symmetric HS256 with the Supabase JWT secret (so Supabase-protected resources also accept the token).

**Role policy:** Hard-coded dict in the controller — `{ "admin": ["admin"], "crm": ["agent","admin"], "channels": ["agent","admin"] }`.

**Coupling:** Zero references to Haven business concepts (Listing, Property, Channel). Touches `Haven.Common` only for Telegram OTP delivery and config loader.

**Inter-service token validation:** there is **no** `/auth/validate-token` endpoint — earlier analysis assumed one. Each consuming service validates locally with the shared HS256 key (standard ASP.NET JWT bearer middleware). Frontend checks `exp` on every click.

---

## 2. Decomposition — abstract vs specific

The natural fault lines in Haven.Auth, mapped to SDK abstractions:

| Concern | Abstract? | Specific? | Notes |
|---|---|---|---|
| Generate + verify a short-lived code keyed by `(subject, scope)` | ✅ | — | Pure primitive; doesn't know what a "user" is |
| Where OTP records live (Postgres / Redis / in-memory) | abstract via `IOtpStore` | impl is consumer's choice | Ship `MemoryOtpStore` default; companion packages later for Postgres/Redis |
| How the code is generated (6 digits / 8 alphanumeric / etc.) | abstract via `IOtpCodeGenerator` | default is 6-digit numeric | One default impl, swappable |
| How the code is delivered (Telegram / SMS / email / voice) | abstract via `IOtpDeliveryHandler` | impl is per-channel | Telegram impl ships in companion package |
| Looking up users by phone / email / username | — | ✅ consumer-supplied | SDK doesn't dictate user model |
| Linking external IDs (Telegram chat ID, Discord ID, etc.) to a user | — | ✅ consumer-supplied | Channel-specific, semantic to consumer's auth model |
| Telegram bot webhook handling (state machine for `/start` + Contact) | — | ✅ consumer-supplied | Just consumer using Telegram.Bot directly; SDK doesn't try to abstract bot UX |
| Issuing a JWT from claims | ✅ | — | Pure: `IEnumerable<Claim> → string`; symmetric HS256 default impl |
| Validating a JWT (already shipped) | ✅ | — | Already in `identity/jwt` |
| "Which role is allowed in which service" policy | abstract via `IRolePolicy` | impl is dict-backed default + consumer-overrideable | Replaces Haven's hard-coded `AllowedRoles` |
| The `User` and `UserPhone` schemas | — | ✅ consumer-owned | SDK does not define an `IAuthUser` entity (see §4) |
| The `otp_codes` schema | ✅ (via `IOtpStore`) | — | SDK ships the conceptual schema; backends are separate packages |

**Rule of thumb for the split:**

> The SDK ships things that have a stable contract independent of any user model. The user model itself stays in the consumer.

This keeps the SDK orthogonal — same way `identity/jwt` doesn't ship a `User` entity, just bearer token *validation*.

---

## 3. Proposed SDK package layout (4 new packages)

All four go under `src/identity/` alongside the existing identity packages:

```
src/identity/
├── jwt/                          ← EXISTING (validation only) — AddJwtBearerAuthentication
├── jwt.issuance/                 ← NEW — ITokenIssuer + JwtTokenIssuer + JwtTokenIssuerOptions
├── otp/                          ← NEW — IOtpService + IOtpStore + IOtpCodeGenerator + IOtpDeliveryHandler + OtpOptions
├── otp.telegram/                 ← NEW — TelegramOtpDeliveryHandler (companion, opt-in)
├── policies/                     ← NEW — IRolePolicy + DictionaryRolePolicy + RolePolicyOptions
├── cookies/                      ← EXISTING
├── oidc/                         ← EXISTING
├── oauth.{google,microsoft,github,apple}/    ← EXISTING
├── identity-api/                 ← EXISTING
├── mfa.totp/                     ← EXISTING
├── mfa.webauthn/                 ← EXISTING
└── password-hashing.argon2/      ← EXISTING
```

Future companion packages (when needed, not v1):

```
src/identity/
├── otp.postgres/                 ← FUTURE — Postgres-backed IOtpStore
├── otp.redis/                    ← FUTURE — Redis-backed IOtpStore
├── otp.sms/                      ← FUTURE — Twilio/Vonage IOtpDeliveryHandler
└── otp.email/                    ← FUTURE — SendGrid/MailKit IOtpDeliveryHandler
```

### 3.1 `WoW.Two.Sdk.Backend.Beta.Identity.Otp` — core OTP service

**Public types:**

```csharp
namespace WoW.Two.Sdk.Backend.Beta.Identity.Otp;

/// <summary>Orchestrates OTP generation, storage, delivery hooking, and verification.</summary>
public interface IOtpService
{
    Task<OtpCreationResult> CreateAsync(string subject, string scope, CancellationToken ct = default);
    Task<OtpVerificationResult> VerifyAsync(string subject, string code, string scope, CancellationToken ct = default);
}

public sealed record OtpCreationResult(
    bool Success,
    string? Code,           // present on success — caller passes to delivery handler
    OtpFailureReason? FailureReason);

public sealed record OtpVerificationResult(
    bool Success,
    OtpFailureReason? FailureReason);

public enum OtpFailureReason
{
    RateLimited,
    Expired,
    InvalidCode,
    MaxAttemptsReached,
    ScopeMismatch,
}

/// <summary>Storage abstraction. Default impl is in-memory; Postgres/Redis ship separately.</summary>
public interface IOtpStore
{
    Task<bool> HasUnconsumedRecentAsync(string subject, string scope, TimeSpan window, CancellationToken ct);
    Task SaveAsync(OtpRecord record, CancellationToken ct);
    Task<OtpRecord?> FindActiveAsync(string subject, string code, string scope, CancellationToken ct);
    Task<OtpRecord?> FindLatestActiveAsync(string subject, string scope, CancellationToken ct);
    Task IncrementAttemptsAsync(Guid recordId, CancellationToken ct);
    Task MarkConsumedAsync(Guid recordId, CancellationToken ct);
}

public sealed record OtpRecord(
    Guid Id, string Subject, string Code, string Scope,
    DateTimeOffset CreatedAt, DateTimeOffset ExpiresAt,
    int Attempts, bool Consumed);

/// <summary>Code generation strategy.</summary>
public interface IOtpCodeGenerator
{
    string Generate();
}

/// <summary>Delivery channel abstraction. One impl per channel (Telegram, SMS, email, ...).</summary>
public interface IOtpDeliveryHandler
{
    Task<OtpDeliveryResult> SendAsync(OtpDeliveryEnvelope envelope, CancellationToken ct = default);
}

public sealed record OtpDeliveryEnvelope(
    string DeliveryAddress,   // phone, email, telegram chat id — channel-specific
    string Code,
    string Scope,
    IReadOnlyDictionary<string, string>? Metadata);

public sealed record OtpDeliveryResult(
    bool Success,
    string? FailureReason);

public sealed record OtpOptions
{
    public int CodeLength { get; init; } = 6;
    public TimeSpan CodeLifetime { get; init; } = TimeSpan.FromMinutes(5);
    public TimeSpan RateLimitWindow { get; init; } = TimeSpan.FromSeconds(5);
    public int MaxAttempts { get; init; } = 5;
}
```

**Registration:**

```csharp
// in OtpServiceCollectionExtensions.cs
public static IServiceCollection AddOtpService(
    this IServiceCollection services,
    Action<OtpOptions>? configure = null)
{
    services.Configure(configure ?? (_ => { }));
    services.TryAddScoped<IOtpService, OtpService>();
    services.TryAddSingleton<IOtpCodeGenerator, NumericOtpCodeGenerator>();
    services.TryAddSingleton<IOtpStore, MemoryOtpStore>();    // override with .AddOtpPostgresStore() or .AddOtpRedisStore()
    return services;
}
```

**Defaults shipped in this package:**
- `OtpService` — orchestrator implementing `IOtpService`
- `NumericOtpCodeGenerator` — N-digit numeric code (default 6)
- `MemoryOtpStore` — `ConcurrentDictionary`-backed; dev/test only

**NOT shipped here (companion packages):**
- Telegram delivery handler → `identity/otp.telegram`
- Postgres / Redis store backends → `identity/otp.postgres` / `identity/otp.redis` (future)

**Deps:** `Microsoft.Extensions.DependencyInjection.Abstractions`, `Microsoft.Extensions.Options`. That's it.

### 3.2 `WoW.Two.Sdk.Backend.Beta.Identity.Otp.Telegram` — Telegram delivery adapter

**Public types:**

```csharp
namespace WoW.Two.Sdk.Backend.Beta.Identity.Otp.Telegram;

public sealed class TelegramOtpDeliveryHandler : IOtpDeliveryHandler
{
    public TelegramOtpDeliveryHandler(ITelegramBotClient bot, IOptions<TelegramOtpOptions> options) { ... }
    public Task<OtpDeliveryResult> SendAsync(OtpDeliveryEnvelope envelope, CancellationToken ct = default) { ... }
}

public sealed record TelegramOtpOptions
{
    /// <summary>Template applied per scope. {0}=scope display name, {1}=code, {2}=lifetime minutes.</summary>
    public string MessageTemplate { get; init; }
        = "🔐 {0} login\n\nYour code: {1}\nExpires in {2} minutes.\n\nDon't share this code with anyone.";

    /// <summary>Map scope key → human-readable name. Falls back to scope key if not mapped.</summary>
    public IReadOnlyDictionary<string, string> ScopeDisplayNames { get; init; }
        = new Dictionary<string, string>(StringComparer.Ordinal);
}
```

**Registration:**

```csharp
public static IServiceCollection AddTelegramOtpDelivery(
    this IServiceCollection services,
    Action<TelegramOtpOptions>? configure = null)
{
    services.Configure(configure ?? (_ => { }));
    services.AddScoped<IOtpDeliveryHandler, TelegramOtpDeliveryHandler>();
    return services;
}
```

**Note:** Consumer must register `ITelegramBotClient` separately. SDK doesn't take the bot token — consumer's choice how that's wired (env var, secret manager, etc.). The Telegram chat ID (recipient) flows in via `OtpDeliveryEnvelope.DeliveryAddress`.

**Deps:** parent `identity/otp` + `Telegram.Bot`.

### 3.3 `WoW.Two.Sdk.Backend.Beta.Identity.Jwt.Issuance` — JWT issuance

**Public types:**

```csharp
namespace WoW.Two.Sdk.Backend.Beta.Identity.Jwt.Issuance;

public interface ITokenIssuer
{
    string Issue(IEnumerable<Claim> claims, TokenIssuanceContext? context = null);
}

public sealed record TokenIssuanceContext(
    TimeSpan? Lifetime = null,                    // overrides options default
    string? Audience = null,                      // overrides options default
    IReadOnlyDictionary<string, object>? AdditionalHeaders = null);

public sealed class JwtTokenIssuer : ITokenIssuer
{
    public JwtTokenIssuer(IOptions<JwtTokenIssuerOptions> options) { ... }
    public string Issue(IEnumerable<Claim> claims, TokenIssuanceContext? context = null) { ... }
}

public sealed record JwtTokenIssuerOptions
{
    public string Issuer { get; init; } = "";
    public string Audience { get; init; } = "";
    public TimeSpan Lifetime { get; init; } = TimeSpan.FromHours(1);
    public string SigningKey { get; init; } = "";          // symmetric — consumer's responsibility to source securely
    public string Algorithm { get; init; } = "HS256";      // HS256/HS384/HS512 supported in v1; RS*/ES* future
}
```

**Registration:**

```csharp
public static IServiceCollection AddJwtTokenIssuance(
    this IServiceCollection services,
    Action<JwtTokenIssuerOptions> configure)
{
    services.Configure(configure);
    services.AddSingleton<ITokenIssuer, JwtTokenIssuer>();
    return services;
}
```

**Deps:** `System.IdentityModel.Tokens.Jwt`, `Microsoft.IdentityModel.Tokens`. Same deps as the existing `identity/jwt` validation package.

**Why a sibling sub-package and not merge into `identity/jwt`?**

- `identity/jwt` is currently *bearer validation* — pulls in `Microsoft.AspNetCore.Authentication.JwtBearer`. Web hosts only.
- `identity/jwt.issuance` is a pure library — pulls only the token-handler bits. Console apps, workers, services-without-ASP.NET can use it.
- Keeping them separate lets a worker that *issues* tokens but doesn't run an HTTP server avoid pulling in ASP.NET Core auth.

### 3.4 `WoW.Two.Sdk.Backend.Beta.Identity.Policies` — role authorization policy

**Public types:**

```csharp
namespace WoW.Two.Sdk.Backend.Beta.Identity.Policies;

public interface IRolePolicy
{
    bool IsAllowed(string role, string scope);
}

public sealed class DictionaryRolePolicy : IRolePolicy
{
    public DictionaryRolePolicy(IOptions<RolePolicyOptions> options) { ... }
    public bool IsAllowed(string role, string scope)
        => options.Value.Map.TryGetValue(scope, out var roles) && roles.Contains(role);
}

public sealed record RolePolicyOptions
{
    public IReadOnlyDictionary<string, IReadOnlySet<string>> Map { get; init; }
        = new Dictionary<string, IReadOnlySet<string>>(StringComparer.Ordinal);
}
```

**Registration:**

```csharp
public static IServiceCollection AddRolePolicy(
    this IServiceCollection services,
    Action<RolePolicyOptions> configure)
{
    services.Configure(configure);
    services.TryAddSingleton<IRolePolicy, DictionaryRolePolicy>();
    return services;
}
```

**Deps:** `Microsoft.Extensions.DependencyInjection.Abstractions`, `Microsoft.Extensions.Options`. Trivial.

---

## 4. Why no `IAuthUser` entity abstraction in v1

The instinct to extract entity abstractions alongside auth is reasonable, but it bloats the SDK without paying for itself. Here's why v1 doesn't ship one:

**What the SDK actually needs from "user" — nothing.**

Walk through what each SDK package does:

- `IOtpService.CreateAsync(subject, scope)` — `subject` is a string (phone, email, username). The SDK doesn't care what kind of subject it is.
- `IOtpService.VerifyAsync(subject, code, scope)` — same; just stringly-keyed.
- `IOtpDeliveryHandler.SendAsync(envelope)` — `envelope.DeliveryAddress` is a string. Channel-specific.
- `ITokenIssuer.Issue(claims)` — claims are `IEnumerable<Claim>`. The SDK doesn't construct claims; the consumer does.
- `IRolePolicy.IsAllowed(role, scope)` — both strings.

**None of those signatures need a `User`.** The user model is a consumer concern — they look up their user, decide what's a `role`, decide what claims go into the token, and pass those primitives to the SDK.

**What this looks like in the consumer's `AuthController`:**

```csharp
[HttpPost("request-otp")]
public async Task<IActionResult> RequestOtp([FromBody] OtpRequest body, CancellationToken ct)
{
    // 1. Consumer-owned user lookup
    var user = await _users.FindByPhoneAsync(body.Phone, ct);
    if (user is null) return NotFound(new { error = "phone_not_found" });
    if (!user.IsActive) return StatusCode(403, new { error = "inactive" });
    if (user.TelegramChatId is null) return UnprocessableEntity(new { error = "bot_not_linked" });

    // 2. SDK: generate OTP
    var creation = await _otp.CreateAsync(body.Phone, body.Service, ct);
    if (!creation.Success) return _statusFor(creation.FailureReason!.Value);

    // 3. SDK: deliver via Telegram (handler resolved by DI)
    var envelope = new OtpDeliveryEnvelope(user.TelegramChatId, creation.Code!, body.Service, null);
    var delivery = await _delivery.SendAsync(envelope, ct);
    if (!delivery.Success) return StatusCode(502, new { error = "delivery_failed" });

    return Ok(new { success = true });
}

[HttpPost("verify-otp")]
public async Task<IActionResult> VerifyOtp([FromBody] VerifyRequest body, CancellationToken ct)
{
    // 1. SDK: verify OTP
    var verification = await _otp.VerifyAsync(body.Phone, body.Code, body.Service, ct);
    if (!verification.Success) return _statusFor(verification.FailureReason!.Value);

    // 2. Consumer-owned user lookup
    var user = await _users.FindByPhoneAsync(body.Phone, ct);
    if (user is null) return NotFound(new { error = "user_not_found" });

    // 3. SDK: role policy
    if (!_policy.IsAllowed(user.Role, body.Service))
        return StatusCode(403, new { error = "not_authorized" });

    // 4. SDK: issue JWT — consumer constructs claims from their user model
    var claims = new[]
    {
        new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
        new Claim("phone", body.Phone),
        new Claim("user_role", user.Role),
        new Claim("user_name", user.Name ?? ""),
        new Claim("aud", "authenticated"),
    };
    var token = _tokens.Issue(claims, new TokenIssuanceContext(Lifetime: TimeSpan.FromHours(24)));

    return Ok(new { success = true, token, user = new { user.Id, body.Phone, user.Name, user.Role } });
}
```

The consumer's `AuthController` is ~30 lines of glue code over the SDK. The SDK doesn't dictate user shape; consumer's model can have any fields.

**Bonus: this is exactly how the rest of the SDK works.** `identity/jwt` validation doesn't ship a `User` either. `identity/oauth.google` doesn't ship a `User`. `mfa.totp` doesn't ship a `User`. The SDK is a toolbox of orthogonal verbs; consumers compose them around their domain.

**When to revisit:** if 3+ consumers end up writing identical `AuthController` glue, ship a `Backend.Beta.Identity.Recipes.PasswordlessOtp` v2 recipe package that bundles `IUserStore<TUser>` + an opinionated controller. v1 doesn't need it.

---

## 5. Why split OTP delivery into a companion package

**`identity/otp` (core)** — zero external SDK deps beyond MS Extensions. Pure abstractions + in-memory default. No `Telegram.Bot`, no `Twilio`, no `SendGrid`.

**`identity/otp.telegram`** — depends on `Telegram.Bot` (LGPL or MIT? need to verify license is permissive enough for core meta-package). Companion, opt-in.

The reason: you don't want a consumer who delivers OTP via Twilio SMS pulling in `Telegram.Bot` transitively. Each delivery channel = one tiny companion package. Same pattern as `oauth.google` / `oauth.microsoft` — one package per provider.

**License check needed:** `Telegram.Bot` on NuGet is MIT-licensed (verify before shipping `otp.telegram` in core meta).

---

## 6. The Telegram-bot-link flow — why it stays in Haven

Haven's flow B (bot link) is **not** something the SDK should try to abstract. Reasons:

1. **It's just Telegram.Bot UX** — `/start` reply keyboard with "Share Contact" button, then `Update.Message.Contact` handling. That's standard `Telegram.Bot` work, fully covered by their library.
2. **Each consumer's bot is different.** Haven's bot says "Welcome to Haven CRM!" and only handles linking. Another consumer's bot might also do customer support, file uploads, command routing. The SDK shouldn't dictate bot UX.
3. **The SDK *does* give consumers what they need:**
   - `IUserRepository` is consumer-owned — their `LinkExternalIdAsync` method or equivalent
   - `IUserRepository.FindByPhoneAsync` is consumer-owned — used in bot webhook handler to validate phone
4. **The SDK does NOT need to know** that the user has linked Telegram. It just needs `OtpDeliveryEnvelope.DeliveryAddress` populated by the consumer's controller (consumer reads `user.TelegramChatId` from their model and passes it).

So Haven keeps:
- Its `TelegramService.HandleWebhookAsync` (state machine for /start + Contact)
- Its `IUserRepository.LinkTelegramAsync` (UPDATE users SET telegram_user_id)
- Its `PhoneNormalizer` (Uzbek-specific, stays in Haven; not extracted)

The SDK ships:
- `IOtpDeliveryHandler` interface
- `TelegramOtpDeliveryHandler` impl (uses `ITelegramBotClient.SendMessageAsync`)

That's a clean cut.

---

## 7. DI wiring — Haven's `AuthController` after extraction

```csharp
// Haven.Auth/Program.cs (post-extraction)

builder.Services
    // SDK packages
    .AddOtpService(o =>
    {
        o.CodeLength = 6;
        o.CodeLifetime = TimeSpan.FromMinutes(5);
        o.RateLimitWindow = TimeSpan.FromSeconds(5);
        o.MaxAttempts = 5;
    })
    .AddTelegramOtpDelivery(o =>
    {
        o.ScopeDisplayNames = new Dictionary<string, string>
        {
            ["crm"] = "Haven CRM",
            ["channels"] = "Haven Channels",
            ["admin"] = "Haven Admin",
        };
    })
    .AddJwtTokenIssuance(o =>
    {
        o.Issuer = "haven-auth";
        o.Audience = "authenticated";
        o.Lifetime = TimeSpan.FromHours(24);
        o.SigningKey = config.HavenPlatformDbJwtKey;
        o.Algorithm = "HS256";
    })
    .AddRolePolicy(o =>
    {
        o.Map = new Dictionary<string, IReadOnlySet<string>>(StringComparer.Ordinal)
        {
            ["admin"] = new HashSet<string> { "admin" },
            ["crm"] = new HashSet<string> { "agent", "admin" },
            ["channels"] = new HashSet<string> { "agent", "admin" },
        };
    });

// Haven-specific (stays in Haven)
builder.Services
    .AddSingleton<ITelegramBotClient>(sp =>
        new TelegramBotClient(config.HavenTelegramAgentBotToken))
    .AddScoped<IUserRepository, UserRepository>()                  // Haven-owned
    .AddScoped<IBotWebhookHandler, TelegramBotWebhookHandler>();   // Haven-owned (handles /start + link)
```

`AuthController` becomes thin glue (the snippet in §4 above).

`TelegramBotWebhookHandler` is consumer code (Haven-specific) that handles the bot-link UX — uses `IUserRepository.FindByPhoneAsync` and `IUserRepository.LinkTelegramAsync`, calls `ITelegramBotClient.SendMessageAsync` directly.

---

## 8. What the SDK does NOT cover (gaps to flag explicitly)

These are gaps in **Haven.Auth itself** — not gaps the SDK should silently fix. Documenting them so we're honest about scope:

| Gap | SDK position | Notes |
|---|---|---|
| Refresh tokens | Not shipped in v1 | `ITokenIssuer.Issue` is single-shot; refresh is a separate concept. Future: `Identity.Tokens.Refresh` |
| Logout / token revocation | Not shipped | Stateless JWTs can't be revoked without a denylist; future: `Identity.Tokens.Revocation` (denylist + middleware) |
| Per-IP OTP rate limiting | Not shipped | Per-subject rate limiting is in `IOtpService.CreateAsync`. Per-IP belongs in `web/ratelimit` (already shipped). |
| OTP attempt lockout (multi-hour) | Not shipped | `MaxAttempts` triggers per-OTP lockout (auto-reset after `CodeLifetime`). Persistent multi-hour lockout = future feature. |
| Email verification flow | Not shipped | Email channel = future `otp.email` package. Verification = consumer's own verb. |
| Multi-device session tracking | Not shipped | Stateless JWT model. Future: `Identity.Sessions` if ever needed. |
| Inter-service token validation endpoint | Not in scope | Each service validates locally with shared key (already shipped via `identity/jwt`). |

---

## 9. Sequencing the 4 packages

Recommended ship order (each independently shippable; each validates the next):

1. **`identity/policies`** — smallest, simplest, validates the package shape + spec/standard tooling. ~50 LOC.
2. **`identity/jwt.issuance`** — second smallest, well-known territory. ~150 LOC.
3. **`identity/otp`** — the meaty one (orchestrator + store + generator + delivery interface). ~400 LOC.
4. **`identity/otp.telegram`** — companion, depends on `identity/otp` already being shipped. ~80 LOC.

Total: ~700 LOC across 4 packages. Plus `spec.md` + `standard.md` + `Tests.cs` examples + `README.md` per package.

Estimated effort: 2–3 batches of work.

---

## 10. Tables

### 10.1 Components × Abstract / Specific verdict

| Component (Haven type) | Abstract / Specific / Hybrid | Proposed SDK type | DI lifetime | Package |
|---|---|---|---|---|
| OTP generate + verify orchestrator (`OtpRepository.CreateAsync` / `.VerifyAsync`) | Abstract | `IOtpService` (interface) + `OtpService` (default impl) | Scoped | `identity/otp` |
| OTP storage (Haven's raw Npgsql calls into `otp_codes`) | Abstract | `IOtpStore` + `MemoryOtpStore` default; `PostgresOtpStore` / `RedisOtpStore` future companions | Scoped (or Singleton for Memory) | `identity/otp` (interface + memory); future companion packages |
| OTP code generation (`Random.Shared.Next(100000, 999999)`) | Abstract | `IOtpCodeGenerator` + `NumericOtpCodeGenerator` default | Singleton | `identity/otp` |
| OTP delivery via Telegram (`TelegramService.SendOtpAsync`) | Hybrid | `IOtpDeliveryHandler` interface + `TelegramOtpDeliveryHandler` impl | Scoped | Interface in `identity/otp`, impl in `identity/otp.telegram` |
| OTP delivery via SMS / email / voice | Hybrid (future) | Same `IOtpDeliveryHandler` + per-channel impls | Scoped | Future companion packages |
| JWT issuance (`TokenService.Generate`) | Abstract | `ITokenIssuer` + `JwtTokenIssuer` default | Singleton | `identity/jwt.issuance` |
| Role gating (`AllowedRoles` dict) | Abstract | `IRolePolicy` + `DictionaryRolePolicy` default | Singleton | `identity/policies` |
| User lookup by phone (`IUserRepository.LookupByPhoneAsync`) | **Specific (consumer-owned)** | — | — | Stays in Haven |
| User-to-Telegram linking (`IUserRepository.LinkTelegramAsync`) | **Specific (consumer-owned)** | — | — | Stays in Haven |
| Telegram bot webhook state machine (`/start` + Contact handling) | **Specific (consumer-owned)** | — | — | Stays in Haven (just `Telegram.Bot` usage) |
| Phone normalization (`PhoneNormalizer.Normalize`, Uzbek-specific) | **Specific (locale-bound)** | — | — | Stays in Haven |
| Configuration loader (`ConfigurationLoader.Load`) | **Specific (Haven utility)** | — | — | Stays in Haven; .NET 9 IOptions covers SDK side |
| HTTP envelope (`AuthResponse`, `VerifyResponse`) | **Specific (controller DTOs)** | — | — | Stays in Haven; SDK ships `web/problemdetails` for errors |

### 10.2 Entity abstractions in v1

| Haven entity | Fields used by auth | Proposed SDK abstraction | Verdict |
|---|---|---|---|
| `users` (Haven entity) | `id`, `name`, `role`, `telegram_user_id`, `is_active` | None | **Don't ship — consumer owns user model. SDK works on string subjects + claims.** |
| `user_phones` (Haven entity) | `user_id`, `phone` | None | **Don't ship — consumer owns phone storage.** |
| `otp_codes` (Haven entity) | `id`, `phone`, `code`, `service`, `expires_at`, `attempts`, `used` | `OtpRecord` (record type) inside `IOtpStore` | **Ship** — but only as the `IOtpStore` contract surface. Schema lives in companion packages (`otp.postgres`, `otp.redis`). |
| Role enum (`agent` / `admin`) | string values | None | **Don't ship — consumer defines their roles.** `IRolePolicy.IsAllowed(string, string)` is string-keyed. |

Net: **one abstract entity ships** (`OtpRecord` inside `IOtpStore`), all others stay consumer-owned.

---

## 11. Open questions before drafting specs

1. **`Telegram.Bot` license** — confirm MIT (or other permissive) before shipping `otp.telegram` in core meta-package.
2. **`OtpRecord.Subject` typing** — keep as `string` (current proposal, max flexibility) or introduce a `Subject` value object with `(SubjectKind, Value)`? Recommend string for v1 simplicity.
3. **`IRolePolicy` semantics** — does it return bool or rich result? Current: bool. If consumers want reasons ("role_not_in_scope_X"), upgrade to `RolePolicyDecision { bool Allowed, string? Reason }` later.
4. **JWT issuance signing key sourcing** — current proposal: consumer passes raw string. Should we also support `IKeyProvider` for rotating keys / KMS-backed keys? Defer to v2.
5. **Should `IOtpService.CreateAsync` invoke `IOtpDeliveryHandler` itself, or just return the code and let the caller deliver?** Current proposal: return the code, caller delivers. Pros: caller controls delivery context (which channel, which recipient address — could be different than subject). Cons: caller can forget to deliver. Tradeoff favors caller-controlled.
6. **Default `IOtpStore` lifetime** — `MemoryOtpStore` should be Singleton (so the dictionary persists across requests). Document this clearly.

---

## 12. Risks

- **Telegram.Bot SDK churn** — Telegram.Bot v18+ changed several APIs (e.g. `SendMessageAsync` overloads). Pin a specific version range in `Directory.Packages.props`.
- **Schema drift between OTP store backends** — `otp.postgres` and `otp.redis` could diverge in field naming. Lock a canonical `OtpRecord` shape in `identity/otp` and require backends to map onto it.
- **JWT signing key rotation not addressed in v1** — consumers needing rotation will have to wait for v2 or roll their own. Document in `spec.md`.
- **Consumer "bot link" flow is not validated by the SDK** — if a consumer forgets to populate `OtpDeliveryEnvelope.DeliveryAddress` correctly, delivery silently fails. Mitigation: `TelegramOtpDeliveryHandler` should return a clear `OtpDeliveryResult.FailureReason` on empty / invalid chat ID.

---

## 13. Next concrete steps

1. Open `wow-two-sdk.backend.beta` repo.
2. Update `targets.md` to add the 4 new vectors (`identity/otp`, `identity/otp.telegram`, `identity/jwt.issuance`, `identity/policies`) under P2 (since they extend the already-shipped P2 identity area).
3. Update `ideas.md` with one paragraph per package describing the slot.
4. Draft `identity/policies/spec.md` + `standard.md` first (smallest, validates tooling).
5. Implement `identity/policies` end-to-end (csproj → impl → spec → tests → README).
6. Push, verify CI bumps version, update `context.md` with shipped state.
7. Move on to `identity/jwt.issuance`.
8. Then `identity/otp` (the heavy one).
9. Then `identity/otp.telegram`.
10. After all 4 ship: migrate Haven.Auth to consume them (dogfood).
