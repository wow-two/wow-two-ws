# Product manifest (retired)

*Last updated: 2026-10-27*

> Retired 2026-10-27: a product's identity — name, description, homepage and each service's name and description —
> lives in its deployment descriptor, `engineering/deployment/deploy.yml`
> ([§ Identity](../../deployment/descriptor/deploy-descriptor.md#identity)), per Wheelhouse decision 7 (one manifest per
> repo, format A). No repo writes `product/product.json` any more.
> Use case — moving a repo that still carries `product/product.json`, or reading one while it does.

## Existing files

- must move a repo's `product/product.json` into its `deploy.yml` and delete the file in the same commit.
- must pin pipelines `v0.11.0` or later before the move; an older generator refuses the identity keys.
- Wheelhouse still reads `product/product.json` at a commit whose `deploy.yml` declares no identity, under the same
  consumption rules, and shows the operator a notice to move it.
- Once `deploy.yml` declares an identity, Wheelhouse ignores `product/product.json`.
- [product.schema.json](product.schema.json) stays only to validate the files that remain until each moves.

---

## Moving

| `product/product.json` | `engineering/deployment/deploy.yml` |
|---|---|
| `manifest`, `$schema` | dropped; the descriptor's own `descriptor` and `$schema` line apply |
| `name` | `name`, beside `product:` |
| `description` | `description`, beside `product:` |
| `homepage` | `homepage`, beside `product:` |
| `services.<key>.name` · `description` | `name` · `description` under `services.<key>` |

The limits stay the same: names 1–80 characters, descriptions 1–200, `homepage` an `http` or `https` address without
credentials, at most 300; every text one line. What a good name and description are:
[deploy descriptor § Identity](../../deployment/descriptor/deploy-descriptor.md#identity).
