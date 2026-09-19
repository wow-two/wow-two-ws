# Testing

*Last updated: 2026-09-13*

> Service test tiers, method names and shared harness ownership.

## Tiers

- must put pure, deterministic, I/O-free logic in the Unit tier.
- must put repository/handler tests below HTTP in the Integration tier.
- must put complete HTTP request flows in the E2E tier using `WebApplicationFactory<Program>` or its SDK wrapper.
- must favor E2E coverage for services whose dependencies can run locally.
- must cover success, validation, invariants, authentication and ownership edges per feature.
- must verify unauthorized ownership reads do not reveal existence.
- must not infer frontend behavior from backend tests; retain frontend-specific verification.

---

## Harness

- must use xUnit and the shared SDK harness appropriate to the tier.
- must use AwesomeAssertions for fluent assertions.
- must use `FakeTimeProvider` for controllable time-dependent paths.
- must follow [database testing](../../../../core/mla/domains/persistence/testing/test-databases.md) for providers and fixtures.
- must file bus fixtures with messaging and auth helpers with identity.
- must keep product-specific host wiring and auth helpers in the product test project.
- must not copy generic SDK host factories or fixtures for a later extraction.
- must stub only genuinely external third-party services; use WireMock for HTTP stubs.
- must run in-process code generation, detectors and queues for real when exercising their integration.
- must wait for asynchronous work with bounded polling, not fixed sleeps.
- must run required container-backed checks locally and in CI before shipping.
- must apply [test build properties](../../platform/build/directory-build-props.md#test-runs).

---

## Layout

- must name product test projects `{Product}.Tests.{Type}`.
- must use `Unit`, `Integration` or `E2E` for those tiers.
- may use a single subject noun for a specialized suite, such as `Migrations`.
- must not use the ambiguous bare `{Product}.Tests` name for a product suite.
- must group test projects in the virtual `Tests/` solution folder from [solution organization](../architecture.md).
- must keep any physical test directory distinct from its virtual solution-folder name.
- must document prerequisites and suite coverage in the project's folder lead document.
- must apply the [repository document rule](../../../../../../repo/structure/repo-structure.md#3-doc-rule--no-readme-below-root).

---

## Method naming

- must name tests `{Unit}_Should{Expectation}_When{Condition}`.
- must use PascalCase within segments; underscores separate segments, not words.
- must name the tested action, expected behavior and scenario rather than implementation details.
- may omit `_When{Condition}` only for unconditional behavior.
- must name the HTTP status in an HTTP response test, such as `Create_ShouldReturn400_WhenInputIsInvalid`.
- must name the behavioral outcome in a below-HTTP test, such as `Lookup_ShouldReturnMissing_WhenKeyIsUnknown`.
- must not require an HTTP status in a repository, pure-logic or other non-HTTP test.

---

## Ownership

- must keep shared tier, layout and naming rules here.
- must place provider-specific fixture and reset rules in the domain that owns the provider.
- must link domain-specific test rules instead of restating them here.

---

## Body documentation

- must keep test names descriptive under the method-naming rules above; a comment does not replace the scenario or expectation in the name.
- may use `// Arrange`, `// Act` and `// Assert` when they clarify the body's phases; the markers are optional.
- may add a scenario or rationale comment when the name and code leave a relevant fact unclear; must not require a second gist for every test.
- must not repeat the test name or narrate self-explanatory statements in body comments.
- must preserve comments that explain non-obvious setup, timing, provider behavior or assertions; optional markers are not grounds for blanket comment deletion.
- test XML documentation exemptions remain governed by the [notation owner](../../../../core/lla/notation/documentation/documentation.md).
