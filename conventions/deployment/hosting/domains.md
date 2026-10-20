# Domains

*Last updated: 2026-10-20*

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
- must give a deployed site whose product has no domain yet a baseline public host on its server's IP, through
  sslip.io: `<product>-dev.<ip>.sslip.io` in dev, `<product>.<ip>.sslip.io` in prod, with the IP's dots as dashes
  (`ocharo-studio-dev.203-0-113-10.sslip.io`); a product's second site adds `-<site>` after the product.
- must let Wheelhouse fill the baseline host; binding a domain replaces it.

---

## Exposure

- must put a public site on a bound domain behind the Cloudflare proxy; DNS-01 issues its certificate.
- must serve a baseline host from the server's own ingress on ports 80 and 443, with an HTTP-01 certificate.
- must keep SSH and Wheelhouse's control path on the tailnet.
- must keep service-to-service calls on the server's `platform` network.
- may leave a private site on its tailnet node until its host is bound ([server lifecycle](../servers/server-lifecycle.md)).
