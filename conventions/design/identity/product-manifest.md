# Product manifest

*Last updated: 2026-10-15*

> One file per product repo, `product/product.json`, holding the product's identity text: name, description,
> homepage, and each service's name and description.
> Purpose — the repository owns what a product calls itself; a console shows a cached copy and never edits one.
> Use case — adding identity text to a product repo, or reading a product's name, description or homepage.

## Ownership

- must keep identity text in the manifest; must not store it as a row a console edits.
- must keep icons as files, never as manifest entries ([product icons](product-icons.md#paths)).
- must keep slug, repository, lifecycle, release source and environments out of the manifest.
- must keep builds, ports and versions in `deploy.yml`; the manifest only labels a service
  ([deploy descriptor](../../deployment/descriptor/deploy-descriptor.md#format)).

---

## Path

- must place the file at `product/product.json`, directly in `product/`, one per product repo.
- must write UTF-8 JSON without comments, at most 16 KiB.
- must validate the file against [product.schema.json](product.schema.json).
- should point `$schema` at that file, relative to the repo, so editors validate as you type.

---

## Format

```json
{
  "$schema": "../../../../conventions/design/identity/product.schema.json",
  "manifest": 1,
  "name": "Haven",
  "description": "Listings, leads and clients for a realtor.",
  "homepage": "https://haven.example",
  "services": {
    "auth": { "name": "Accounts", "description": "Sign-in and accounts." },
    "edge": { "name": "Site" }
  }
}
```

| Key | Required | Meaning |
|---|---|---|
| `manifest` | yes | format version; `1` |
| `name` | yes | display name, 1–80 characters |
| `description` | yes | one line on what the product does, 1–200 characters |
| `homepage` | no | the public `http` or `https` address, at most 300 characters |
| `services.<key>` | no | `name` and `description`, same limits; at least one of them; at most 32 services |

- must write every text as one line: no control characters, no leading or trailing space.
- must not put credentials in `homepage`.
- must take `<key>` from a key under `services:` in `engineering/deployment/deploy.yml`.
- must not add a key the schema lacks; a new key needs a new `manifest` version.
- may omit a service; its consumer then shows the service key.
- may omit `homepage`; a product with no site has none.

---

## Consumption

- must read the file at a commit of the product's default branch.
- must key what it keeps by that commit; must not expire it on a timer.
- must replace a kept copy only with one read at a newer commit.
- must drop the kept copy when a newer commit has no file; the product then falls back to its recorded values.
- must ignore an invalid or oversized file: keep the last valid copy and show the operator the reason.
- must not fail a request because the file is invalid, missing or unreachable.
- must show every field as text; must not interpret markup in it.
