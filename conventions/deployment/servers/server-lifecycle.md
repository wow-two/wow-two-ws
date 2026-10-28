# Server lifecycle

*Last updated: 2026-10-28*

> The steps a VPS follows from purchase to retirement, and the rule each step keeps.
> Purpose — one list to audit a host against; commands and values stay in the runbook.
> Use case — buying, enrolling, wiring, backing up, moving or retiring a host.

Runbook → [VPS runbook](../../../workbench/wow-two-platform/wow-two-platform.wheelhouse/engineering/deployment/vps/vps.md#products-host)
· [network and access](../../../workbench/wow-two-platform/wow-two-platform.wheelhouse/engineering/deployment/vps/network.md)
· [local rehearsal](../../../workbench/wow-two-platform/wow-two-platform.wheelhouse/engineering/deployment/deployment.md#local-server).

Point ids (`M6`) cite the [migrations analysis](../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

| Host | Runs |
|---|---|
| control | both Wheelhouse consoles, PostgreSQL, Traefik, the canary; no product |
| products | products only: PostgreSQL, Traefik, one tailnet node per private site |

---

## Order

- must order Ubuntu 26.04 amd64 with 8 GB RAM, 100 GB disk and a provider out-of-band console.
- may use any provider Wheelhouse registers (`OVH`, `Contabo`); a provider is an enum member plus its integration.
- must run `create-admin.sh` first on a root-only image, so an administrator signs in with a key.
- must verify the SSH host fingerprint in the provider's console before the first connection; never trust a scan.
- must keep the purchase with the owner; Wheelhouse holds no credential that can order, reinstall or cancel.
- must give each host a stable lowercase server ID, never reused for another machine.
- must keep hosts, tailnet names and accounts out of every repository ([secrets](../../security/secrets/secrets.md)).

---

## Bootstrap

- must prepare a host with the kit: `bootstrap-products.sh` on a products host, `bootstrap.sh` on the control host.
- must copy the reviewed kit from the repo over verified SSH before each run; a host never fetches it.
- should prove a kit change with `rehearse.py products` before it reaches a real host.
- must install Docker and Tailscale from their official repositories; a script never upgrades an installed package.
- must give the `wheelhouse-deploy` account runner keys alone, each `restrict`ed; its Docker group is host control.
- must turn SSH password, keyboard-interactive and root sign-in off; the administrator's password is for the console.
- must default-deny inbound traffic except 80 and 443, which Traefik answers for public sites; SSH stays tailnet-only.
- must publish a host port on loopback only; UFW alone does not stop Docker.
- must install security updates unattended without reboots; the owner reboots in a window.
- must upgrade Docker and Tailscale by hand: an engine upgrade restarts every container.

---

## Tailnet

- must keep the policy in the repo (`tailnet-policy.hujson`); the owner pastes it, and its tests must pass.
- must tag every machine: `tag:control`, `tag:products`, `tag:product-site`, `tag:canary`.
- must let a tagged node reach nothing but its granted path; only the control host reaches a products host, on SSH.
- must join a products host with `--advertise-tags=tag:products` and a site node with a `tag:product-site` key.
- must disable key expiry on the control host; a tagged node never expires.
- must close public SSH on a products host once an SSH session over the tailnet works (`--tailnet-only-ssh`).
- may keep the control host's SSH public only while GitHub-hosted CI deploys over it, keys only and `restrict`ed.
- must serve private HTTPS through Tailscale Serve, never Funnel.

---

## Runner key

- must give each console its own Ed25519 identity per server, living only in that console's volume.
- must pin the products host's tailnet address and its verified host key, never a MagicDNS name.
- must authorize the key with `authorize-runner.sh`; it refuses a dev key and an address outside the tailnet.
- must prove the console reaches the host before registering the server.

---

## Platform

- must run PostgreSQL 18 ([version rule](../../development/backend/dotnet/core/mla/domains/persistence/database/postgres/postgres.md#version)), Traefik and the `platform` network from the kit, on fixed addresses.
- must keep the consoles on `control`, apart from workloads, so a workload never reaches a console.
- must rerun `prepare.py` after every kit update; it keeps credentials and renders Compose again.
- must never delete a populated PostgreSQL volume to repeat initialization.

---

## Products

- must give each product environment its own role and database `<product>_{dev,prod}`: no superuser, no role creation.
- must host in that database the product's sets and every per-product instance's sets; a shared instance gets its
  own database on its own server ([migrations](../../development/backend/dotnet/core/mla/domains/persistence/migrations/migrations.md#model), M6).
- must create the product's declared untrusted `extensions` as superuser when placing its database
  ([descriptor](../descriptor/deploy-descriptor.md#migrate), M41).
- must keep a service's settings at `config/<product>-<environment>/<service>.json` under the deploy root:
  `0444` in a `0700` folder.
- must set `AllowedHosts` to `<site host>;localhost` and `Deployment:TrustedProxies` to Traefik's `platform` address.
- must give each private site one tailnet node per environment: `<node>-dev` for dev, `<node>` for prod; a public
  site answers on its domain or its sslip.io baseline host ([domains](../hosting/domains.md)).
- must pull private images with a classic token of `read:packages` alone, expiring, from a machine account.
- must keep that token in the deploy account's Docker config; `prepare.py` refuses any other scope.
- must register the server, import the product from its hub catalog, then add its dev and prod environments in prod.
- must deploy dev first and promote after ([release flow](../descriptor/deploy-descriptor.md#release-flow)).

---

## Backups

- must treat a prod snapshot as a restore point on the same disk, never as a backup.
- must back up databases, key volumes and runner state, encrypted, off the provider before public cutover.
- must keep decryption credentials off the host and set a retention before unattended operation.
- must restore into an empty database before trusting a backup.
- must recover a failed schema change forward or from the snapshot; an image rollback never undoes a migration, and
  the older image's `migrate check` gates it ([migrations](../../development/backend/dotnet/core/mla/domains/persistence/migrations/migrations.md#compatibility), M2, M15).

---

## Move

- must move a product environment through a backup and a restore on the new host, never a live copy.
- must freeze writes for ten minutes at most, switch DNS once the restore verifies and keep the old host seven days.

---

## Retire

- must take a final backup, remove the host's tailnet nodes and revoke its runner key before cancelling.
- must confirm a decommission with a fresh second factor.

---

## Planned

- enrollment, tailnet keys, the policy and product wiring run from Wheelhouse — v0.5 Iteration 21.
- a registry token per deploy replaces the host token — Iteration 21.
- backups off the provider, with a restore proof — Iteration 12.
- move and decommission as recorded jobs — v0.7.
- Cloudflare domains — Iteration 11 ([domains](../hosting/domains.md)); public ingress and baseline hosts shipped 2026-10-20.
- standby servers and a backup-only storage — [redundancy](redundancy.md), for review.
