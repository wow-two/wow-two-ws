# JWT auth

*Last updated: 2026-09-10*

> Bearer validation and token issuance as separate registrations with an explicit trust configuration.

## Configuration

- must use the [identity configuration](../identity.md#configuration) naming and settings rules.
- must source signing secrets from configuration or a secret store, never a source literal.
- must configure issuer, audience and one intended verification-key source.
- must keep token issuance off a resource server that only accepts an external issuer's tokens.
- must match issuer, audience and key bytes when issuing and validating with the same symmetric key.
- must not infer authorization from successful signature verification alone.

---

## Validation

- must register bearer validation through `AddJwtBearerAuthentication`.
- must wire authentication and authorization in the host pipeline.
- must keep issuer, audience, signature and lifetime validation enabled for normal protected endpoints.
- must use HTTPS for remote metadata in a deployed service.
- must not assume registration enforces mutually exclusive key sources: the current helper rejects neither-present only.
- must not assume the helper enforces HTTPS metadata: it follows the supplied metadata URI's scheme.
- must treat `JwksUri` as the helper's metadata-address input, not assume any raw key-set URL is valid discovery metadata.
- current semantics → [JWT registration source](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Identity/Jwt/JwtServiceCollectionExtensions.cs).

---

## Issuance

- must register issuance separately through `AddJwtTokenIssuance` when the service owns token issuance.
- must map the product's identity into claims at the issuance boundary.
- must use the injected clock for token timestamps.
- must validate signing algorithm and key requirements through the issuance contract.
- must not assume refresh, revocation, asymmetric signing or rotation from the symmetric issuer alone.
- current API → [issuance source](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Identity/Jwt/Issuance/JwtTokenIssuer.cs).
