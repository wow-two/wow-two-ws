# Haven platform stack (#16) -- evidence

*Last updated: 2026-11-21*

Haven's own SCFD, Identity and Files on `ocharo-vps`, apart from Ocharo's `harvest-dev`, `files-dev`, `ocharo-dev` and
`events-dev`. Host addresses stay out of this public repo: `<ip>` stands for the server's dashed public address.

## Status

- ✅ SCFD `harvest-prod` healthy, `v0.2.54`, own database `harvest_prod`
- ✅ Identity `identity-prod` healthy, `v0.5.24`, own database `identity_prod`
- ✅ Files `files-prod` healthy, `v0.1.19`, own database `files_prod` and `data` volume
- ✅ SCFD stored a private asset in Haven's Files with a token from Haven's Identity
- ✅ Anthropic key in `harvest-prod`'s vault; `processing budget` reads state
- ✅ Spend guard open: `LimitUsd 135`, `SoftShare 0.8`, `CycleStartDay 25`; `harvest-dev` drops to 60, $195 in all
- ✅ Telegram on: deployment `f16213fc`, log "Registered the Telegram webhook at
  `https://haven-identity.<ip>.sslip.io/api/telegram/webhook`"; the webhook answers 401 without its secret
- ✅ Bot is `@haven_agents_dev_bot`: the stored token's `getMe` names it, read inside the container (job `fe2ee346`);
  `getWebhookInfo` shows our URL, 0 pending, no error. `BotUserName` switched to match (deployment `41af69ef`); the
  first `/start` went to `@haven_agents_bot`, whose webhook isn't ours
- ✅ Instance admin: `admin create` with the developer's phone, job `117f9e1c`, `admin-result` `status created`,
  `isRoleGranted true`, subject `01a1fb2f-844a-77ca-85e0-1e364742f079`
- ✅ `harvest-prod` console sign-in on: `OperatorSubjectIds:0` = that subject, deployment `8fd15133` (migrate
  `distributed_cache` 0 → 1, config check consistent); Sign in lands on Haven Identity's `/sign-in` with phone sign-in
- ✅ The developer signed in to the Haven SCFD console through Haven Identity by Telegram, 2026-11-21 04:23 local
  ([01-scfd-console-signed-in.png](01-scfd-console-signed-in.png): `SR`, `v0.2.54`, Sources 5, 7 sections)
- ✅ Files read-back through the console: Sources loaded a source icon from
  `/api/sources/{id}/assets/{asset}` → 200, and `files-prod` logged `GET /api/files/v1/files` 200 six times
  ([02-scfd-sources-files-icon.png](02-scfd-sources-files-icon.png))
- Haven's Identity uses `@haven_agents_dev_bot` ("Haven Agents Dev Bot") for now (developer, 2026-11-21: "dev
  worked"); `@haven_agents_bot` stays free for a later move, which needs its token stored and the dev bot's webhook
  cleared

## Names

Wheelhouse names a target's Compose project, database, config folder and baseline host `<product>-<environment>` per
server, so Haven takes each product's `prod` environment on `ocharo-vps`.

| Product | Target | Site | Database |
|---|---|---|---|
| SCFD `harvest` | `harvest-prod` | `haven-scfd.<ip>.sslip.io` | `harvest_prod` |
| Identity `identity` | `identity-prod` | `haven-identity.<ip>.sslip.io` | `identity_prod` |
| Files `files` | `files-prod` | `haven-files.<ip>.sslip.io` | `files_prod` |

- `files_prod` was placed for Ocharo prod in Wheelhouse v0.14; it now holds Haven's Files
- Ocharo prod's own SCFD and Files on `ocharo-vps` need a Wheelhouse instance part (backlog § Hosting, `b7f5e17`), or
  another server

## Deploys (2026-11-21)

| Target | Deployment | Steps |
|---|---|---|
| `harvest-prod` | `1c48b263` | migrate harvest 0 → 18, ai 0 → 6; config check consistent; 1 service healthy; site answered |
| `files-prod` | `8c464db0` | succeeded |
| `identity-prod` | `622ba256` | failed at config check: `Identity:SignUp:Profile:DisplayName` rendered `false` |
| `identity-prod` | `5e20a2e9` | migrate identity 0 → 13; config check consistent; 1 service healthy; site answered |

## Identity

Discovery, read from the Mac:

```
issuer          https://haven-identity.<ip>.sslip.io/
token_endpoint  https://haven-identity.<ip>.sslip.io/connect/token
scopes          files.read files.write harvest.containers-manage harvest.entries-write harvest.events-read
                harvest.links-submit harvest.pipelines-manage harvest.pipelines-read harvest.pipelines-run
                harvest.posts-read harvest.sources-manage harvest.subscriptions-manage harvest.tenants-manage
                openid profile email phone offline_access
```

- Registrations are owner keys on `identity-prod`, declared on the product with `everyService` so they render:
  resources `0 harvest`, `1 files`; clients `0 harvest-console` (code, SCFD callback and sign-out URIs),
  `1 harvest-files` (`client_credentials`, `files.read` `files.write`)
- Client secrets: generated in Wheelhouse, linked into `harvest-prod` (`Identity:Client:ClientSecret`,
  `HarvestAssets:Files:Identity:ClientSecret`)
- Certificates: the image's `keys generate` piped straight into the vault, never printed; expiries set -- signing
  2027-03-20, encryption 2027-06-18, data protection 2028-11-19
- `Identity:SignUp:Profile:DisplayName` and `:Picture` are `Optional`: the descriptor's `Off` parses as YAML `false`

## SCFD → Identity → Files

`harvest-prod` log, 2026-11-21 03:35 local:

```
POST https://haven-identity.<ip>.sslip.io/connect/token   -> 200
POST https://haven-files.<ip>.sslip.io/api/files/v1/files -> 201
```

`files-prod` log over the same window: `POST /api/files/v1/files 201` once.

## Spend guard

`dotnet HarvestSources.Api.dll processing budget` on `harvest-prod`, job `3cc6d5c8`, exit 0:

```json
{"state":"off","windowStartUtc":"2026-10-25T00:00:00+00:00","windowEndUtc":"2026-11-25T00:00:00+00:00",
 "spentMicroUsd":0,"projectedMicroUsd":0,"readFailed":false,"rows":[],"spentUsd":0.0000,"projectedUsd":0.0000}
```

After `LimitUsd 135` and Apply (deployment `1b6adb16`), job `2454fa07`, exit 0:

```json
{"state":"open","windowStartUtc":"2026-10-25T00:00:00+00:00","windowEndUtc":"2026-11-25T00:00:00+00:00",
 "spentMicroUsd":0,"projectedMicroUsd":0,"readFailed":false,"rows":[],"spentUsd":0.0000,"limitUsd":135.0000,
 "softUsd":108.0000,"projectedUsd":0.0000}
```

## Settings read (`harvest-prod`)

| Key | Source |
|---|---|
| `Ai:Providers:anthropic:ApiKey` | vault, v2 |
| `Harvest:Processing:Ai:Enabled` | stored `true` |
| `Harvest:Processing:Tags:Models:0`, `Extraction:Models:0` | stored `anthropic/claude-haiku-5-5` |
| `Harvest:Processing:Extraction:Wanted:1` | stored `listing` / `real-estate` |
| `Harvest:Processing:Budget:CycleStartDay` | stored `25` |
| `Harvest:ServiceAccess:Authority` | stored, Haven Identity issuer |
| `Identity:Client:ClientSecret` | linked from `identity-prod` |
| `HarvestAssets:Files:BaseAddress` | stored, Haven Files origin |
