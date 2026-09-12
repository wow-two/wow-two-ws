# Architecture

*Last updated: 2026-09-10*

> Arrangement selection and solution organization for backend services.

## Arrangements

- must use [Clean Architecture](clean/clean.md) unless the service explicitly chooses another arrangement.
- must document a different arrangement before implementing it.
- must not treat the [onion](onion/onion.md), [hexagonal](hexagonal/hexagonal.md) or
  [vertical-slice](vertical-slice/vertical-slice.md) shells as established alternatives.
- must give each arrangement its own folder and declare its dependency direction and project mapping there.
- must leave arrangement-specific component placement to that arrangement.

---

## Solution organization

- must apply the [repo solution layout](../../../../../repo/structure/repo-structure.md).
- must group projects in PascalCase virtual solution folders.
- must distinguish virtual solution folders from physical source directories.
- must include every project intended for solution builds or test discovery in the solution.
- may declare an empty virtual folder for a planned extraction.

| Folder | Projects |
|---|---|
| `Services/` | hosts and their product layers |
| `Platform/` | SDK-bound extractables |
| `Libraries/` | product shared libraries outside service code |
| `Tools/` | CLIs and developer utilities |
| `Tests/` | test projects |

- must allow `Services` to reference `Platform`, never the reverse.
- must keep `Platform` independent of product types; BCL, SDK and its declared package dependencies are allowed.
- must keep an SDK extraction a move and namespace adjustment; use [extraction](../../../../../sdk-extraction.md).

---

## Solution encoding

- must encode virtual folders and project paths in the repository's `.slnx` solution.
- must place a project beneath the intended `<Folder>` element.
- must not apply classic `.sln` GUID nesting instructions to `.slnx` files.

```xml
<Folder Name="/Platform/">
  <Project Path="Brand.Platform.Core/Brand.Platform.Core.csproj" />
</Folder>
```

---

## Where a folder is created

- must read folder names from their core construct/component owner.
- must read Clean project placement from [Clean placement](clean/clean.md#placement).
- must read intra-project domain grouping from [domain structuring](clean/domain-structuring.md).
