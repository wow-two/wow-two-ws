# Redundancy

*Last updated: 2026-10-21*

> **Status — for review.** Proposed 2026-10-21, and nothing applies it yet. Review it before any product gets a second
> server.
> How a product survives a server's failure: up to three servers in ranked roles, plus one storage that serves nothing.
> Purpose — one model for uptime, backups and full recovery, so every product recovers the same way.

| Role | Runs | Who gets it |
|---|---|---|
| primary | dev and prod, every service | every product |
| secondary | prod, the services the owner keeps | opt-in, for uptime |
| tertiary | prod, the services the owner keeps | opt-in, after a secondary |
| storage | no service: backups, volume copies, the encrypted vault export | every product with data |

---

## Roles

- must run an environment as every service of its product on one server; a product never splits services across
  servers.
- must run dev on the primary only; the standbys (secondary, tertiary) exist for prod uptime.
- must list every service on a standby by default; the owner opts a non-core service out.
- must put the secondary on another provider or region than the primary, and the tertiary apart from both where
  possible: one provider's outage never takes two roles.
- must keep the storage with a provider that no role server uses.
- may hold one product's primary and another product's standby on the same server; a role belongs to a product.

---

## Data flow

- must replicate PostgreSQL from the primary to the secondary, asynchronously, and on to the tertiary by cascading; a
  standby stays read-only until it is promoted.
- must copy each service's file volumes (uploads, SQLite, Data Protection keys) to the standbys, with SQLite through
  its safe snapshot. The copy interval is no longer than the product's recovery point.
- must send backups from the primary to the storage, encrypted before they leave the host: the database's base backup
  with its write-ahead log, and volume snapshots.
- must keep secrets in the storage only as the vault's encrypted export; the root key never goes there (decision 67:
  the owner's offline copy, later a passkey).
- must set each product's recovery point and recovery time. The proposed prod defaults are a recovery point of
  1 minute with a secondary (24 hours without one) and a recovery time of 15 minutes.

---

## Failover

- must fail over only after the primary fails health checks from two vantage points (the control host and a standby),
  never on the control host's view alone.
- must fence the old primary before promoting: stop its services or cut its public traffic, so two primaries never
  take writes.
- must promote the secondary's database, then point the product's hosts at the secondary; the tertiary then replicates
  from the new primary.
- must start as a manual Promote action with a typed confirmation; automatic failover follows once drills pass.
- must have a bound domain behind the Cloudflare proxy to fail over. An sslip.io baseline host names one server's
  address, so it cannot move ([domains](../hosting/domains.md)).
- must rebuild a returning old primary as a standby of the new primary; it never resumes as primary on its own.
- must run a background or scheduled job (a jobs worker, a cron, an outbound email) on whichever server is primary;
  a promoted standby starts it, so jobs keep running while the old primary is down.
- should move a product by adding the new server as a standby, letting it catch up and promoting it. The old server
  stays as a standby for seven days, replacing the backup-and-restore move.

---

## Coordination

- must let Wheelhouse, or a service of its own on each server, coordinate every failover step: fence, recover the
  database to a point in time, prove the copy is current, start services and jobs, and check the product's
  infrastructure before traffic moves.
- must record each step live and in the audit trail, like the other infrastructure jobs.
- must run Wheelhouse itself on the same model: its own primary, standbys and storage.

---

## Full recovery

- must be able to rebuild every role from the storage alone: new servers, enrollment, the latest base backup and its
  log, the volume copies, and the vault export unlocked with the owner's root key.
- must keep Wheelhouse's own database and data volume in the storage as well.
- must make storage objects versioned and locked for the retention window, so a compromised server can add backups
  but never delete them.
- must give servers credentials that can only add objects; only the owner's recovery credential reads or deletes.
- must rehearse a full recovery every quarter and record how long the restore took.

---

## Open for review

- **Wheelhouse's standby.** It follows this model (Coordination), so where its standbys run, and which of its
  parts must keep watching while its primary is down, still needs a design.
- **Failover traffic.** Cloudflare's load balancer switches on its own health checks but is paid. The free path is
  Wheelhouse rewriting the proxied DNS records itself, and it depends on the control host.
- **Write loss.** Asynchronous replication can lose the last seconds of writes; synchronous replication costs write
  latency on every request.
- **Sessions.** Without replicated Data Protection keys, users sign in again after a failover.
- **Cost.** Every standby is a server bill. Decision 58 covers builds only, so each standby is the owner's call.
- **Names.** primary, secondary, tertiary and storage, unless review picks better ones.

---

## Planned

- The SDKs first gain these capabilities (replication, point-in-time recovery, failover hooks, job ownership).
- Then Wheelhouse adds roles per product, replication in placement, a storage connection, Promote and recovery
  drills, and runs itself the same way. All of it is backlog, with v0.7's one-click infrastructure.
