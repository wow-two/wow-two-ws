# Entity configurations

*Last updated: 2026-09-10*

> An EF mapping type for one entity; schema authority comes from the selected migration strategy.

## Location

- must use a `Configurations/` folder in the project selected by the deliverable's architecture.
- must give each configuration its own type-named file → [one type, one file](../../../../mla.md).

---

## Declaration

### Type doc

- must start the summary with `Configures`, naming the entity and its storage mapping.

```csharp
/// <summary>Configures the listing entity and its listings table.</summary>
```

### Type name

- must name the type `{Entity}Configuration` and implement `IEntityTypeConfiguration<{Entity}>`.

---

## Content

- must declare `Configure` as the only public member.
- must inherit the method documentation from `IEntityTypeConfiguration<T>`.
- may add remarks for runtime mapping facts the builder calls do not show.
- must use a block body.
- must apply [EF mapping rules](ef-mapping.md) for the chosen schema strategy.
- must order configuration as table/key, column types, conversions, relationships.
- must put each fluent call on a new line.

```csharp
/// <inheritdoc />
public void Configure(EntityTypeBuilder<ListingEntity> builder)
{
    builder
        .ToTable(ListingEntity.TableName);

    builder
        .HasKey(entity => entity.Id);
}
```
