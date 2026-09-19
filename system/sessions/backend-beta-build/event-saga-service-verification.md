# Event saga service verification

*Last updated: 2026-09-13*

## Scope

- `IEventSagaRunner` / `EventSagaRunner` → `IEventSagaService` / `EventSagaService`.
- Both declarations now live in `Messaging/EventSaga/Services/`, with matching namespaces.
- Updated the exact singleton DI registration, logger type, XML, feature docs, specifications and planning references.
- Preserved `RunAsync`, ordered execution, compensation order, cancellation and DI override behavior.
- Corrected the summary and scope table: one scope is created per execution, before the step loop, and shared by all steps.
- Corrected the routing-guard citation in `Saga.md` to the actual `InProcessEventSagaTransport.cs` owner.
- No new tests, package changes or Git mutations.

---

## Checks

- SDK-wide old-name search, excluding generated output and the parent-owned historical sweep tracker, returned no references.
- SDK `git diff --check` passed.
- Core compilation passed using isolated temporary outputs while the coordinator tests awaited native approval:
  `dotnet build WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1 -p:BuildProjectReferences=false -p:IntermediateOutputPath=/private/tmp/event-saga-isolated-obj/ -p:OutputPath=/private/tmp/event-saga-isolated-bin/`.
- Final build: exit 0, 21 warnings, 0 errors. Log: `/private/tmp/event-saga-service-build.log`.
- Isolated-output setup initially failed to locate the project-reference artifacts. The existing, previously built
  `Data/Abstractions` reference and runtime DLLs were copied into the corresponding temporary paths, then the build passed.
  Normal SDK/test output directories were not replaced by this check.

---

## Coverage limits

- No existing test directly exercises `EventSagaService.RunAsync`; this rename has compile and source-reference coverage.
- Coordinator/saga-state-machine tests and their native approval status are recorded separately in
  [coordinator-service-verification.md](coordinator-service-verification.md). They do not establish event-saga runtime coverage.
- This is scoped local verification, not a full SDK build, release or consumer-compatibility gate.
