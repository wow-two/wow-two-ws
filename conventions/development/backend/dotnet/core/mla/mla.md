# Mla

*Last updated: 2026-09-10*

> Role definitions and application rules within one codebase, shared by services, libraries, SDKs and CLIs.

## The three buckets

| Bucket | Answers | Lead |
|---|---|---|
| [constructs](constructs/constructs.md) | what role am I declaring | the suffix keep-list and the coining gate |
| [components](components/components.md) | what is complete on its own | the self-sufficiency gate |
| [domains](domains/domains.md) | which technology or use case | one folder per capability |

- must route architecture, build and host composition to [shapes](../../shapes/shapes.md).

---

## One type, one file [REQUIRED]

- must follow [files](../lla/constructs/constructs.md#files) for symbol placement and companions.
- must state only a scoped deviation here or in the role's owner.

### Partial types

A `partial` is the one sanctioned second file, and only for a reason the split itself makes visible.

| Reason | Example |
|---|---|
| a source generator owns the other half | `[GeneratedRegex]`, `JsonSerializerContext` |
| the composition order must read on its own, apart from what each step does | `HostConfiguration` |

- must name a part `{Type}.{Aspect}.cs`, beside the base file in the same folder —
  `HostConfiguration.Extensions.cs`, never `HostConfigurationExtensions.cs` in a second folder.
- must keep the type doc on `{Type}.cs` alone; a part carries no `<summary>` for the type.
- must let the base file read alone — a reader who opens only `{Type}.cs` learns what the type is and,
  where order matters, in what order it runs
  ([host configuration](../../shapes/service/platform/startup/host-configuration.md) § *The partial split*).
- must not add a part for a reason the table does not list — a third reason earns a row here first.

---

## Writing a doc in this scope

Holds for a construct doc and a component doc alike; each family lead states only what it adds.

- must cite [notation](../lla/notation/notation.md) rather than restate a default it does not override.
- may close with `## Neighbours` — links out, one line each, carrying no rules.

---

## The boundary

- must route a contract requiring both owned services to comply to [hla](../hla/hla.md).
- must adapt a third party here — we own only our end of that wire.
- must sink a rule to [lla](../lla/notation/notation.md) when it holds for any symbol, whatever kind it is.
