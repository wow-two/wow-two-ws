# Delivery

*Last updated: 2026-10-01*

> Service packaging and shipping; existing container and hosting rules remain authoritative.

## Activation

- must use the [image-publish contract](../../../../../../deployment/descriptor/deploy-descriptor.md#builds-and-versions).
- must use [single-host serving](../../../../../../deployment/hosting/single-host-serving.md) for the combined SPA/API shape.
- must define this vector's additional artifact and rollout rules when a service needs a different delivery shape.
- must record artifact identity, runtime configuration and rollback ownership for that change.
- must not treat this shell as a replacement for a product's existing release procedure.

---

## Open

- delivery rules beyond the existing image/hosting contracts activate with a concrete alternative deliverable.
