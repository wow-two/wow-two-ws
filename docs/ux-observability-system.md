# UX Observability & Error Reporting System

## Core Concept

End-to-end operation tracing with user-facing error reporting — combining distributed tracing and product-level incident management to enable a **build precise, ship fast** workflow.

---

## System Design

### 1. Operation Registry

A centralized list of all operations in the system, defined declaratively. Each operation entry includes:

- Operation type ID
- Expected flows and states
- Known error codes
- Help article mappings
- Toast message templates

This registry acts as a **contract** for each user-facing operation. You're not wiring up error handling ad hoc per feature — you register operations and the system handles the rest.

### 2. Correlation Chain

Every log and event includes three identifiers:

| ID | Purpose |
|---|---|
| **Operation Type ID** | Which operation is being performed (e.g., `user.update_profile`) |
| **Operation ID** | Unique instance of that operation |
| **Request ID** | Ties to the specific API request (returned in API response headers) |

This gives full traceability from UI action → API → backend logs.

### 3. User-Facing Error Reporting (Toast)

When something fails, the user sees a toast notification with two actions:

- **Report** — flags the operation ID and request ID so engineering/support can instantly pull the full trace without asking "what were you doing?"
- **Help** — routes to a contextual help article based on where and which operation failed

---

## Suggested Improvements

### Session-Level Context

- **Add a Session ID** to group all operations within a user session, enabling full journey reconstruction leading to the failure.

### Client-Side Context Capture

When the user clicks "Report," silently attach:

- Browser info and environment
- Active feature flags
- Last N UI events (breadcrumbs)
- Component tree / route at time of error

### Severity Classification

Not every toast should look the same:

| Severity | Example | UX |
|---|---|---|
| Retryable | Network timeout | Auto-retry + subtle toast |
| User error | Validation failure | Inline guidance, no report button |
| System failure | 500 error | Prominent toast + Report + Help |

### Help Link Routing

Map `operation_type_id × error_code` → specific help article via a lookup table. Falls back to a generic troubleshooting page when no match exists.

### Report Deduplication

Rate-limit reports: if the system is failing repeatedly, deduplicate by `operation_type + error_code` within a time window to avoid flooding support with 500 reports for the same root cause.

### User Feedback Loop

Let users optionally add a text description when reporting. Sometimes "I clicked save after editing the title" is worth more than the trace.

---

## Existing Systems Using Similar Patterns

| System | What They Do | Relation to This Pattern |
|---|---|---|
| **Sentry** | Breadcrumbs + error grouping + user feedback widget | Closest match, but developer-facing not user-facing |
| **Cloudflare Ray ID** | Every request gets a ray ID shown in error pages; support looks it up instantly | This pattern generalizes the Ray ID concept |
| **Linear** | Crash reports auto-attach session context and link to engineering tickets | Similar user → engineering pipeline |
| **LaunchDarkly + Datadog RUM** | Feature flag context tied to real user monitoring | Similar correlation approach |
| **Google Cloud Error Reporting** | Groups errors by stack trace with request correlation | Backend-only, no user-facing report button |

---

## Operation Registry Schema (Example)

```typescript
interface OperationDefinition {
  typeId: string;                  // e.g. "invoice.create"
  name: string;                    // Human-readable name
  category: string;                // Grouping for help docs
  expectedDurationMs: number;      // For timeout/slow detection
  retryable: boolean;
  errors: {
    [errorCode: string]: {
      severity: "retryable" | "user_error" | "system_failure";
      toastMessage: string;
      helpArticleSlug: string;
    };
  };
}
```

```typescript
interface OperationContext {
  operationTypeId: string;
  operationId: string;             // Unique per invocation
  requestId: string;               // From API response header
  sessionId: string;               // Groups all ops in a session
  timestamp: number;
  breadcrumbs: UIEvent[];          // Last N UI events
  metadata: Record<string, any>;   // Feature flags, route, etc.
}
```

---

## Why This Enables "Build Precise, Ship Fast"

By defining operations declaratively in a registry, you get:

- **Auto-generated toast messages** per operation type
- **Auto-routed help links** based on failure context
- **Pre-built log queries** for each operation
- **A testability checklist** — each registered operation defines what to verify before shipping
- **Instant support resolution** — no back-and-forth asking users to reproduce issues
