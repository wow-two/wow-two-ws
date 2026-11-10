# API communication

*Last updated: 2026-11-05*

> How our own services call each other, and how those calls stop being allowed.
> Purpose — every new service gets one way to prove who is calling, instead of inventing a key per pair of services.
> Use case — reach here when a service calls another of ours, runs work a person started, or must react to lost access.

Settled for Ocharo's move to Identity, developer, 2026-11-05. Shapes: Files'
`engineering/research/files-analysis-2026-10/t8-identity-contracts.md`. Build state: `ocharo-platform`
`engineering/planning/identity-cutover.md` #52.

## One mechanism

- must call another of our services with a token Identity issued, never a shared key or a forwarded cookie.
- must use client credentials when the service acts as itself, such as a job with no person.
- must use token exchange when it acts for a person: the token keeps the person and adds `act`.
- must verify a token offline against the issuer's JWKS, checking signature, audience, lifetime and scope.
- must read the caller through the one principal (person, service or key), so a policy never branches by scheme.

## Tokens

- must request one token per caller and target, listing every scope that client may use there; never one per action.
- must set the audience to the target's URI, so a token for one service is refused by every other.
- must keep tokens short, 5-10 minutes, with no refresh token; the caller renews near expiry.
- must cache by session and target when acting for a person, and by target when acting as the service.
- must name scopes `{service}.{action}`, such as `files.write`; where an action needs two words, `{service}.{noun}-{verb}`, such as `harvest.events-read` (Events integration, 2026-11-10).
- must name exactly one target with `resource` on a client-credentials token request; Identity answers `invalid_target` without it (Events integration, 2026-11-10).

## What a call may do

- `scope` says what the calling app may ask of that service.
- the role and `org_permission` claims say what the person may do.
- must require both on a person's call; a service's own call has only `scope`.
- must check record-level rules against the service's own data, never by listing records in a token.

## Proving a client

- must authenticate a client with its secret by default; a client may name a key set (`private_key_jwt`) instead.
- must keep the method out of calling code, so a switch changes configuration only.
- must generate a secret in the descriptor and link it across repositories with `from`, never type it per environment.

## Long-running work

Work a person started outlives their token, so a job never depends on it.

- must authorize when the work is accepted, then run it as the service with the person recorded.
- must never store a person's token in a job.
- must declare each long operation's reaction to each signal. Defaults: sign-out continues, access loss cancels.
- must tag a live operation, such as a stream or an agent run, with `sid`, so sign-out cancels it.

## Revocation signal

Offline tokens stay valid until they expire, so a signal closes that gap.

- must publish two events, signed with Identity's key: session ended (`sid`, `sub`) and access changed (`sub`, `org_id`).
- must deliver them through the be sdk: `IEvent`, `IEventHandler<T>`, and `Messaging/Webhooks` as signed HTTP with retries.
- must end the app's session on session ended, and force a token refresh on access changed.
- must refuse a matching token through a deny list kept until that token would have expired.
- must check Identity live only for actions a service names as dangerous, such as deleting an organization.
- a lost signal leaves staleness bounded by the token lifetime.
- a service's own token has no `sid` or `org_id`, so no signal revokes it; only its lifetime limits it.

## Outside this mechanism

- API keys: only callers outside Identity, such as Files' outside tenants, mapped onto the same principal.
- a service's private worker, reached only by that service, may keep its own key (`ImageWorker:Key`).
- browsers reach a service through their backend or a signed URL.
- SignalR (be sdk `Realtime`) pushes to browsers, never between services: it needs a live connection and retries nothing.
