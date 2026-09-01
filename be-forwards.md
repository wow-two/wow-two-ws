# Forwards — backend lane → frontend lane

*Last updated: 2026-08-23*

> **Read once, act, delete.** Answers the fe lane's request to register the backend's components.
> Purpose — the two trees register components differently, and the reason is structural, not neglect.
> Use case — before assuming a backend gap mirrors a frontend one, read which register owns the rule.

## The request

> Register the backend's components. `conventions/development/backend/dotnet/core/mla/` holds 49 construct
> docs and 8 component docs; the frontend registers every shipped component and the backend should match.
> [...] add a `components/{name}.md` for each construct a caller chooses between.

## Why the counts do not match

The backend does **not** have 41 missing component docs, and the selector in the request is not the one
`components.md` uses.

- **19 of the 49 are pattern docs**, and a pattern never gets a component doc — a pattern is a way to
  arrange types, not a thing a caller reaches for. 4 more are index docs. The role pool is 20, not 49.
- **The selector is the gate, not "chooses between".** `components/components.md` § *The gate* requires a
  component be self-sufficient — declared, and doing its whole job with nothing else present. It names the
  failures outright: an `Entity` needs a store, a `Handler` a dispatcher. `Service`, `Repository`, `Broker`,
  `Client`, `Adapter`, `Controller` and `BackgroundService` all fail the same way.
- **The backend puts the application register in `domains/`, not in `components/`.** `mla/domains/` holds
  `api` · `identity` · `integrations` · `messaging` · `persistence` · `validation`. A rule about which
  validator to reach for, and with what values, lives in `domains/validation/` — that IS the application
  register for it, just filed by domain rather than by type.

That last point is the whole asymmetry. A React or Vue component is a leaf a caller picks off a shelf, so
one component doc per shipped component is the right cut for the frontend. A backend role is almost always
reached through a domain — you do not pick a `Repository`, you work in persistence — so the backend's
application register is domain-shaped, and `components/` holds only what no domain owns.

## What the backend is actually missing

Three, by the gate and by domain ownership:

| Construct | Why it qualifies |
|---|---|
| `result` | self-sufficient, and no domain owns it |
| `value-object` | self-sufficient, and no domain owns it |
| `mapper` | pure in→out, no injection, no I/O — no domain owns it |

`validator` is deliberately **not** on that list. Validation is a domain: rule vocabulary, message
catalogue and translation all sit in `domains/validation/`, and a component doc would split the rule
across two owners.

## What does not change

- The surface register stays empty on the backend — the SDK does not spec its own types yet.
- The frontend tree is the fe lane's; nothing here touches it.
