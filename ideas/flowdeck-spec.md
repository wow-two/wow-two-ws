# FlowDeck — Visual Application Flow Debugger

*Last updated: 2026-03-03 08:00 PM*

## Section 1: Original Idea (Compact)

### What
React app that replaces Swagger as the go-to local dev tool. Connects to .NET backend, visualizes entire request flows as interactive node graphs (n8n-style). Real-time tracing via SignalR.

### Core Loop
1. Backend starts → code analyzer scans endpoints, builds flow graphs (controller → service → repo chain)
2. React app connects → receives available flows (grouped by endpoint)
3. Dev picks a flow (e.g. `POST /auth/sign-up`) → sees node pipeline
4. First node = pre-built API form (fields auto-detected: email, password, etc.) → form data persisted in localStorage
5. Dev clicks Send → request fires → each node lights up in real-time via SignalR as execution hits that layer
6. Success = green pipeline · Failure = red node with error details

### Backend Engine
- **Static analysis** at startup: scans controllers → resolves DI chain → builds method-call graphs (nodes)
- **Runtime tracing**: interceptors/loggers on each layer serialize input/output per node (skip streams, large objects)
- **Transport**: SignalR hub streams node-hit events to React client in real-time

### Frontend
- Side menu: all registered flows (endpoints)
- Main canvas: node graph (n8n-style) with live status
- Each node: method name, input/output preview, timing, status
- First node: interactive request form (auto-generated from endpoint signature)

### Key Value Props
- Zero-config Swagger replacement with visual flow
- See exactly where a request fails and why
- No need for breakpoints — trace the full pipeline visually
- Form data persistence = rapid re-testing

---

## Section 2: Revision & Feasibility

### What Works
- **MediatR pipeline = natural fit**: wow-two already uses MediatR + pipeline behaviors — these are *perfect* interception points (no custom IL weaving needed)
- **SignalR is native**: ASP.NET Core has first-class SignalR support — real-time node streaming is trivial
- **DI graph is queryable**: .NET's `IServiceCollection` can be inspected at startup to map dependency chains
- **Swagger metadata exists**: ASP.NET already builds endpoint metadata (OpenAPI) — reuse for form generation
- **Local-only scope**: no auth/deployment complexity — just a dev tool

### What Doesn't Work (As Described)
| Claim | Problem | Fix |
|-------|---------|-----|
| "Code analyzer scans and builds flow at startup" | Static analysis of arbitrary C# call chains is compiler-level hard (polymorphism, async, lambdas, conditionals) | Don't statically analyze. Use **runtime tracing** only — intercept MediatR pipeline + EF Core + registered services via DI decorators |
| "Creates nodes for method calls with I/O serialization" | Serializing arbitrary method params risks circular refs, huge objects, streams, `IQueryable` | Whitelist serializable types. Use `[FlowDeckTrace]` attribute for opt-in. Cap payload size (e.g. 4KB). Show "skipped" for rest |
| "n8n-style node graph" | Full graph editor is massive scope — n8n is 100K+ LOC | Use a simple **linear pipeline view** (vertical/horizontal) — not a free-form graph. Reserve graph for v2 |
| "All flows available in the system" | Discovering every possible code path is impossible without running it | Show **registered endpoints only**. Flows build dynamically as requests execute — not pre-computed |

### Revised Architecture

**Backend (NuGet package: `wow-two-platform.devtools.flowdeck`)**

```
Instrumentation layer (auto-registered via DI):
├── MediatR PipelineBehavior  → traces handler entry/exit + I/O
├── EF Core Interceptor       → traces DB calls + SQL + timing
├── HttpClient DelegatingHandler → traces outbound HTTP
├── Custom [FlowDeckTrace]    → opt-in for any service method
└── FlowDeck SignalR Hub      → streams trace events to client
    └── GET /flowdeck/meta    → endpoint list + parameter schemas (from OpenAPI)
```

- No static analysis. All tracing is runtime via middleware/behaviors/interceptors.
- Each trace event: `{ flowId, nodeId, nodeName, layer, input?, output?, error?, durationMs, timestamp }`
- Conditional registration: `if (env.IsDevelopment()) services.AddFlowDeck();`

**Frontend (React + Vite)**

```
App shell:
├── Sidebar          → endpoint list (from /flowdeck/meta)
├── RequestPanel     → auto-generated form (from OpenAPI schema)
├── PipelineView     → vertical node list with live status
│   ├── Node: Endpoint hit     [green/red] [12ms]
│   ├── Node: Validation       [green/red] [2ms]
│   ├── Node: MediatR Handler  [green/red] [45ms]
│   ├── Node: EF Core query    [green/red] [23ms] [SQL preview]
│   └── Node: Response         [green/red] [total ms]
└── DetailPanel      → selected node's I/O, error stack, SQL
```

**Tech Stack**

| Layer | Tech | Why |
|-------|------|-----|
| Tracing | MediatR `IPipelineBehavior`, EF `IInterceptor`, `DelegatingHandler` | Already in wow-two stack, zero new deps |
| Real-time | SignalR | Native ASP.NET Core, already familiar |
| Metadata | OpenAPI/Swashbuckle reflection | Reuse existing endpoint metadata for forms |
| Frontend | React + Vite + @xyflow/react (React Flow) | React Flow = lightweight node renderer (MIT, 22KB), not full n8n |
| Forms | react-hook-form + JSON Schema (from OpenAPI) | Auto-generate forms from endpoint schemas |
| State | Zustand | Minimal, fits small tool scope |
| Styling | Tailwind | Fast, no design system needed |

### Phased Approach

**Phase 1 — Tracer MVP** (backend only)
- MediatR pipeline behavior that logs handler execution with I/O
- SignalR hub that broadcasts trace events
- `/flowdeck/meta` endpoint returning registered routes + schemas

**Phase 2 — Viewer MVP** (React)
- Endpoint sidebar + request form (auto-generated)
- Linear pipeline view with live SignalR updates
- Basic I/O inspection panel

**Phase 3 — Rich Tracing**
- EF Core interceptor (SQL preview, timing)
- HttpClient tracing (outbound calls)
- `[FlowDeckTrace]` attribute for custom methods
- Error stack traces in failure nodes

**Phase 4 — DX Polish**
- Form data persistence (localStorage)
- Request history / replay
- Flow comparison (diff two executions)
- Export trace as JSON for sharing

### Wow-Two Fit
- Ships as `wow-two-platform.devtools.flowdeck` (backend NuGet) + `wow-two-apps.flowdeck` (React app)
- One-liner setup: `services.AddFlowDeck()` + `app.MapFlowDeckHub()`
- Leverages existing platform packages (DI, MediatR, EF Core patterns)
- Could become the flagship wow-two-apps product — first real "wow" demo of the ecosystem
