# Domains

*Last updated: 2026-10-19*

> How a product's sites get their hosts: one host per site and environment, bound in Wheelhouse, never in a repo.
> Purpose — one naming and ownership rule, so a host moves between servers by a binding change alone.

## Binding

- must bind each site to one host per environment in Wheelhouse; the descriptor names roles, never hosts
  ([sites and routing](../descriptor/deploy-descriptor.md#sites-and-routing)).
- must connect a DNS provider to Wheelhouse with a scoped token; Cloudflare is the first.
- must create, update and remove only the DNS records Wheelhouse owns.
- must apply a binding change as a recorded routes deployment, without a release.
- must track a domain's, certificate's and token's expiry.

---

## Hosts

- must serve a brand's apex from its marketing site and redirect `www` to it.
- must give each other product of the brand its own host, `studio.<domain>`, with its API under `/api`.
- must put dev on the product's own domain, `studio-dev.<domain>`; there is no shared preview domain.
- must choose the domain by the [naming rules](../../marketing/brand-naming-and-domains.md).

---

## Exposure

- must put a public site behind the Cloudflare proxy; DNS-01 issues its certificate.
- must keep SSH and Wheelhouse's control path on the tailnet.
- must keep service-to-service calls on the server's `platform` network.
- may leave a private site on its tailnet node until its host is bound ([server lifecycle](../servers/server-lifecycle.md)).
