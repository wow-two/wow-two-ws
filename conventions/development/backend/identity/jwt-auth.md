# JWT auth

*Last updated: 2026-06-13*

How a product wires JWT **validation** and **issuance** from the backend-beta SDK. Two independent registrations on **one shared signing key**; the SDK carries **no user model** — the app maps its own user into `Claim`s and passes them in.

## Two halves, one key

| Concern | Extension | Configures (`Action<T>`) | Wires |
|---|---|---|---|
| Validate inbound bearer tokens | `AddJwtBearerAuthentication` | `JwtOptions` | ASP.NET `JwtBearer` scheme + `TokenValidationParameters` |
| Issue signed tokens | `AddJwtTokenIssuance` | `JwtTokenIssuerOptions` | `ITokenIssuer` → `JwtTokenIssuer` (singleton) + `TimeProvider.System` |

Both live under `src/Identity/Jwt/` (validation) and `src/Identity/Jwt/Issuance/` (issuance). They do **not** know about each other at runtime — the contract that links them is the **same symmetric key on both sides**. A token issued with `JwtTokenIssuerOptions.SigningKey` validates only if `JwtOptions.SymmetricKey` is byte-identical (HMAC). Issuer/Audience must also line up: issued `iss`/`aud` (`JwtTokenIssuerOptions.Issuer` / `.Audience`) must equal the validator's `JwtOptions.Issuer` / `.Audience`.

> An API that only **accepts** tokens (Auth0 / Entra ID / Supabase issued them) registers `AddJwtBearerAuthentication` **only**. An auth service that mints tokens for its own API registers **both**, same key. Don't add issuance to a pure resource server.

## Validation — `AddJwtBearerAuthentication`

`JwtServiceCollectionExtensions.AddJwtBearerAuthentication(this IServiceCollection, Action<JwtOptions>)`. Throws at registration if mis-configured — fail-fast, not fail-open:

- `JwtOptions.Issuer` — **required** (`InvalidOperationException` if blank).
- `JwtOptions.Audience` — **required** (same).
- Exactly one key source — **required**: `JwtOptions.SymmetricKey` (HMAC dev/shared-secret) **or** `JwtOptions.JwksUri` (asymmetric / managed keys via OIDC discovery). Supplying neither throws.

Hardened defaults baked into the scheme (do not re-set in the product): `ValidateIssuer` / `ValidateAudience` / `ValidateIssuerSigningKey` all on, `RequireHttpsMetadata = true`, `SaveToken = true`, `MapInboundClaims = false` (raw claim types — no legacy SOAP remapping). Tunable via options: `JwtOptions.ValidateLifetime` (default `true`), `JwtOptions.ClockSkew` (default 30s).

```csharp
builder.Services.AddJwtBearerAuthentication(o =>
{
    o.Issuer   = "https://my-issuer";
    o.Audience = "my-api";
    o.SymmetricKey = builder.Configuration["Jwt:Key"]!;   // OR o.JwksUri for managed keys
});

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();
```

`AddJwtBearerAuthentication` registers the scheme only — the product still calls `UseAuthentication()` / `UseAuthorization()` in the pipeline.

## Issuance — `AddJwtTokenIssuance` + `ITokenIssuer`

`JwtIssuanceServiceCollectionExtensions.AddJwtTokenIssuance(this IServiceCollection, Action<JwtTokenIssuerOptions>)` registers `ITokenIssuer` as a singleton (`JwtTokenIssuer`). It is a **pure library** — usable from workers / console apps with no ASP.NET middleware.

`JwtTokenIssuerOptions`:

| Member | Meaning | Default |
|---|---|---|
| `JwtTokenIssuerOptions.Issuer` | `iss` claim | `""` |
| `JwtTokenIssuerOptions.Audience` | default `aud` (overridable per call) | `""` |
| `JwtTokenIssuerOptions.Lifetime` | default token lifetime | 1h |
| `JwtTokenIssuerOptions.SigningKey` | symmetric HMAC key — **required** (throws on first resolve if blank); ≥ 32 bytes for HS256; source from a secret store, never hard-code | `""` |
| `JwtTokenIssuerOptions.Algorithm` | `HS256` (default) / `HS384` / `HS512` — any other value throws | `HS256` |

### `ITokenIssuer.Issue` — the only method, app supplies the claims

```csharp
string Issue(IEnumerable<Claim> claims, TokenIssuanceContext? context = null);
```

The SDK **never constructs claims**. The product maps its own user model into `Claim`s and passes them in:

```csharp
var token = _tokens.Issue(
    new[]
    {
        new Claim(JwtRegisteredClaimNames.Sub, user.Id),
        new Claim("user_role", user.Role),
    },
    new TokenIssuanceContext(Lifetime: TimeSpan.FromHours(24)));
```

`TokenIssuanceContext(TimeSpan? Lifetime = null, string? Audience = null, IReadOnlyDictionary<string,object>? AdditionalHeaders = null)` — per-call overrides; unset members fall back to `JwtTokenIssuerOptions`. `JwtTokenIssuer` stamps `iat` / `nbf` / `exp` from the injected `TimeProvider` (fake-clock-testable), not from wall clock.

## Registering both — shared key

```csharp
var jwtKey = builder.Configuration["Auth:JwtKey"]!;   // one secret, both halves

builder.Services.AddJwtTokenIssuance(o =>
{
    o.Issuer     = "my-auth";
    o.Audience   = "my-api";
    o.SigningKey = jwtKey;
});
builder.Services.AddJwtBearerAuthentication(o =>
{
    o.Issuer       = "my-auth";    // == issuer above
    o.Audience     = "my-api";     // == audience above
    o.SymmetricKey = jwtKey;       // == signing key above
});
```

Same key + matching `iss`/`aud` ⇒ tokens this service mints validate on this service (and any sibling sharing the secret). Diverge the key and every token 401s.

## Not in scope (v1)

Refresh tokens, revocation, asymmetric issuance (RS*/ES*), and key rotation are **not** implemented for issuance — only symmetric HMAC. Validation already accepts asymmetric/managed keys via `JwtOptions.JwksUri`. Key rotation is the v2 seam (an `IKeyProvider`-shaped extension); do not assume it exists — there is no such symbol in source today.

## See also

- [settings.md](../runtime/settings.md) — bind `Issuer`/`Audience`/key from config + secret store, not literals
- [result-pattern.md](../foundation/result-pattern.md) — surface auth failures as `DomainError`, not thrown exceptions, in app code
- [authoring.md](../authoring.md) — cite-the-symbol rule these citations follow
- SDK `wow-two-sdk.backend.beta` → `src/Identity/Jwt/README.md` (validation) + `src/Identity/Jwt/Issuance/README.md` (issuance) — quickstarts + JWKS examples
