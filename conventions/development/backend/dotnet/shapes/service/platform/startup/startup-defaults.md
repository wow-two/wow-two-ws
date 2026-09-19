# Startup defaults

*Last updated: 2026-09-10*

> The shared API boot bundle and its host-owned opt-ins.

## Registration

- must boot an API host through `AddApiDefaults()` and `UseApiDefaults()`.
- must call them from the two [host configuration](host-configuration.md) entry points.
- must configure auth, mediator and data explicitly between `AddApiDefaults()` and `Build()`.
- must opt into controllers separately; the boot bundle does not register them.
- must install the controller [JSON contract](../responses/serialization.md) when using controllers.

```csharp
using WoW.Two.Sdk.Backend.Beta.Meta;

builder.AddApiDefaults(options => options.ServiceName = "{service}");
// Configure the product's auth, mediator and data here.
var app = builder.Build();
app.UseApiDefaults(pipeline =>
{
    pipeline.UseAuthentication();
    pipeline.UseAuthorization();
});
```

---

## Configuration

- must tune the bundle through `ApiDefaultsOptions`; do not copy its implementation into a product.
- must read option names and defaults from the SDK's `ApiDefaultsOptions` documentation.
- must treat `ExposeOpenApi=null` as Development-only exposure; `true` and `false` are explicit overrides.
- must supply CORS origins and validator assemblies explicitly when those concerns are needed.
- must raise a missing composition seam in the SDK instead of forking the bundle in the product.
- must follow [middleware dependencies](host-configuration.md#middleware) for auth and metadata-dependent additions.
- must place auth in the `UseApiDefaults` callback when limiter or cache policies depend on identity.
