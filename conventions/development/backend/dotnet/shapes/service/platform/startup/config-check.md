# Config check

*Last updated: 2026-11-01*

> The `config check` verb: a service's own settings validation, run without serving, so a bad setting is caught
> before a container restarts instead of by a failing container. Exits, the result line and the deploy step mirror
> [`migrate`](../../../../core/mla/domains/persistence/migrations/migrations.md#actions).
> Stored-data rules for a setting → [settings](../../../../core/mla/components/settings.md#stored-data); host
> wiring and boot → [host configuration](host-configuration.md#config-check).

## Model

| Finding | `config check` | Deployed boot | Local run |
|---|---|---|---|
| a missing required value, or a value its rules reject | exit `1` | refuses | may start, logs |
| an unknown key under the service's own sections | exit `1` | refuses | may start, logs |
| stranding: people left no way to use the service | exit `1` | refuses, logs `Critical` | may start, logs |
| a stricter rule over stored rows | no finding | applies at each row's next use | same |
| a loosened rule, or a step added at a person's next action | no finding | applies at once | same |

---

## Verb

- must ship `app config check` in every service that has settings.
- must host the verb in the be sdk, as it hosts `migrate`; the service registers its own stored-data checks.
- must register a setting's stored-data checks in the `Add{Domain}` registration that binds it.
- must run the boot's own settings validation, never a second copy of its rules.
- must start no listener and no hosted service, and write nothing: no row, file, lock or cache entry.
- must answer before `Configure`, so a check runs no startup work → [Program.cs](host-configuration.md#programcs).
- must collect every finding in one run, so one fix needs one rerun.

---

## Invalid values

- must refuse the start on a value its own rule rejects, whatever rows exist.
- must report a missing required setting as `invalid`, code `required`.
- must check rules across settings too, such as a minimum above its maximum (`range`).
- must exit `1` for it from `config check`, before any container restarts.
- must state the rule in the setting's `validate` → [settings registration](../../../../core/mla/components/settings.md#registration).
- must name the setting in the log, never a secret value.

---

## Unknown keys

- must refuse a key under the service's own sections that no settings record binds, and exit `1` for it at the check.
- must declare the service's root section with the be sdk's `AddSettingsRoot`; the check walks every key under it
  against the bound settings records, so a key under a section no record binds is found too.
- must let a retired or misspelt key refuse the start, never fall back silently to a default.
- must name the key in `unknown` and in the log, never its value.
- must not check a section the framework or another component owns, such as `Logging` or `AllowedHosts`.

---

## Changes over stored data

Settings can change under rows an earlier release wrote.

- must apply at once a change that loosens a rule, or only adds a step at a person's next action.
- must apply a stricter rule over stored rows at each row's next use, where the value can be checked (a password once
  it matches its hash).
- must not refuse a start for a stricter rule over stored rows.

---

## Stranding

- must call a change stranding when it leaves some people no way to use the service, such as a removed sign-in
  method that is some people's only one.
- must refuse a stranding change at `config check` and at a deployed boot.
- must log `Critical` at a boot refusal: the setting, the count and how to resolve it.
- must give each `stranded` entry the rule's `code`, the setting and the count.

---

## Database access

- must read the database in one read-only transaction through the service's own connection string.
- must count rows; never read a personal value out.
- must finish in seconds: indexed counts only, never a scan per row.
- must back each count with an index the owner's migration set creates.
- must exit `2` with `error` when the database cannot be reached.

---

## Output

- must print one `config-result` JSON line per run, the last stdout line, starting `config-result `.
- must carry only setting names, codes, counts and the exit; never an email, phone number, name, id or secret.
- must keep `message` to the rule broken, never a secret value.
- must write `code` as a short kebab-case rule id, such as `range` or `only-method-removed`.

| Field | Holds |
|---|---|
| `verb` | `check` |
| `exit` | `0`, `1` or `2` |
| `service` | the service name |
| `invalid` | each `{code, setting, message}` |
| `unknown` | key names |
| `stranded` | each `{code, setting, count}` |
| `durationMs` | wall time of the run |
| `error` | exit `2` only, in place of `invalid`, `unknown` and `stranded`; no secret |

```text
config-result {"verb":"check","exit":0,"service":"identity","invalid":[],"unknown":[],"stranded":[],"durationMs":380}
config-result {"verb":"check","exit":1,"service":"identity","invalid":[{"code":"range","setting":"Identity:Password:MinLength","message":"20 exceeds MaxLength 16"}],"unknown":["Identity:SignUp:Enabled"],"stranded":[{"code":"only-method-removed","setting":"Identity:Methods:Password:IsEnabled","count":3}],"durationMs":412}
config-result {"verb":"check","exit":2,"service":"identity","error":"database unreachable","durationMs":30012}
```

---

## Exit codes

- must exit as `migrate` does for the codes it shares:
  - `0` — consistent: `invalid`, `unknown` and `stranded` are all empty
  - `1` — refused: an invalid value, an unknown key or a stranding change
  - `2` — failed: the check could not finish, such as an unreachable database

---

## Deploy

How the runner runs it → [config check at deploy](../../../../../../../deployment/descriptor/deploy-descriptor.md#config-check).

- must declare the verb in the descriptor's `configCheck:` item, one per service that has settings.
- must need only the service's own settings and database: no other network, no file outside the image.
- must finish within the item's `timeout`, `2m` by default; a run past it counts as failed (`2`).
- must run it in a one-off container after `migrate` and before the restart, on every release deploy.
- must run it on every settings-only apply, from the image the target runs.
- must run it on a return to an older release: that release's own check, after its `migrate check`.
- must stop the deploy on a refusal or a failure, with the old release still serving.

---

## Boot

- must run the same checks at every boot → [host configuration](host-configuration.md#config-check).
- must refuse on a failed check at a deployed boot.
- may start on a local run and log the findings.

---

## History

- must keep no settings history in the service.
- the deploy tool records who changed what and when → [settings at deploy](../../../../../../../deployment/descriptor/deploy-descriptor.md#settings-at-deploy).
