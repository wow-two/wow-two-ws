<script setup lang="ts">
import { computed, ref, useTemplateRef, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

const props = defineProps<{ api: PrototypeApi }>();

type Result = "passed" | "failed";
interface Attempt {
  id: number;
  result: Result;
  label: string;
}
interface Check {
  id: string;
  title: string;
  path: string;
  language: string;
  owner: string;
  status: Result;
  code: string;
  fixedCode: string;
  error: string;
  patched: boolean;
  assignmentNote: string;
  attempts: Attempt[];
}

const initialChecks: Check[] = [
  {
    id: "create-client",
    title: "Create your first client",
    path: "guides/quickstart.md:24",
    language: "TypeScript",
    owner: "Maya Chen",
    status: "failed",
    patched: false,
    assignmentNote: "",
    code: "import { Client } from './sample-sdk';\n\nconst client = new Client({\n  apiKey: process.env.DEMO_TOKEN\n});\nawait client.orders.create({ amount: 2500 });",
    fixedCode:
      "import { Client } from './sample-sdk';\n\nconst client = new Client({\n  token: process.env.DEMO_TOKEN\n});\nawait client.orders.create({ amount: 2500 });",
    error:
      "TS2353: 'apiKey' does not exist in type ClientOptions. The sample fixture expects 'token'.",
    attempts: [{ id: 1, result: "failed", label: "Release 2.8 · sample run" }],
  },
  {
    id: "pagination",
    title: "Walk through every page",
    path: "guides/pagination.md:61",
    language: "TypeScript",
    owner: "Unassigned",
    status: "failed",
    patched: false,
    assignmentNote: "",
    code: "const page = await client.orders.list({ limit: 25 });\n\nfor (const item of page.data) {\n  console.log(item.id);\n}\nconst next = page.nextCursor;",
    fixedCode:
      "const page = await client.orders.list({ limit: 25 });\n\nfor (const item of page.items) {\n  console.log(item.id);\n}\nconst next = page.nextCursor;",
    error:
      "TS2339: Property 'data' does not exist on type Page<Order>. The sample fixture returns 'items'.",
    attempts: [{ id: 1, result: "failed", label: "Release 2.8 · sample run" }],
  },
  {
    id: "retry-policy",
    title: "Configure request retries",
    path: "guides/retries.md:18",
    language: "C#",
    owner: "Leo Silva",
    status: "passed",
    patched: true,
    assignmentNote: "",
    code: "var options = new DemoClientOptions\n{\n    MaxRetries = 3,\n    Timeout = TimeSpan.FromSeconds(10)\n};",
    fixedCode:
      "var options = new DemoClientOptions\n{\n    MaxRetries = 3,\n    Timeout = TimeSpan.FromSeconds(10)\n};",
    error: "",
    attempts: [{ id: 1, result: "passed", label: "Release 2.8 · sample run" }],
  },
  {
    id: "webhook-signature",
    title: "Verify a webhook signature",
    path: "guides/webhooks.md:42",
    language: "C#",
    owner: "Ari Patel",
    status: "passed",
    patched: true,
    assignmentNote: "",
    code: "var verified = DemoSignature.Verify(\n    requestBody,\n    requestSignature,\n    fixtureKey\n);\nAssert.True(verified);",
    fixedCode:
      "var verified = DemoSignature.Verify(\n    requestBody,\n    requestSignature,\n    fixtureKey\n);\nAssert.True(verified);",
    error: "",
    attempts: [{ id: 1, result: "passed", label: "Release 2.8 · sample run" }],
  },
];
const assignmentDialog = useTemplateRef<HTMLDialogElement>("assignmentDialog");
const state = ref(props.api.state({ checks: initialChecks, assignments: 0 }));
const selectedId = ref("pagination");
const filter = ref("all");
const detailTab = ref("snippet");
const assignmentOwner = ref("");
const assignmentReason = ref("");
const formError = ref("");

const selected = computed(() =>
  state.value.checks.find((check) => check.id === selectedId.value),
);
const failing = computed(
  () => state.value.checks.filter((check) => check.status === "failed").length,
);
const passing = computed(() => state.value.checks.length - failing.value);
const totalAttempts = computed(() =>
  state.value.checks.reduce((sum, check) => sum + check.attempts.length, 0),
);
const visibleChecks = computed(() =>
  state.value.checks.filter(
    (check) => filter.value === "all" || check.status === "failed",
  ),
);
const selectedCode = computed(() =>
  selected.value
    ? selected.value.patched
      ? selected.value.fixedCode
      : selected.value.code
    : "",
);

watch(state, (value) => props.api.save(value), { deep: true });

function openAssignment() {
  if (!selected.value) return;
  assignmentOwner.value =
    selected.value.owner === "Unassigned" ? "" : selected.value.owner;
  assignmentReason.value = selected.value.assignmentNote;
  formError.value = "";
  assignmentDialog.value?.showModal();
}

function assignOwner() {
  const owner = assignmentOwner.value.trim();
  const reason = assignmentReason.value.trim();
  if (!owner || reason.length < 8) {
    formError.value =
      "Choose an owner and add at least 8 characters of handoff context.";
    return;
  }
  if (!selected.value) return;
  selected.value.owner = owner;
  selected.value.assignmentNote = reason;
  state.value.assignments += 1;
  assignmentDialog.value?.close();
  props.api.toast(
    "Owner assigned in this local prototype. No notification sent.",
  );
}

function applySampleFix() {
  if (!selected.value || selected.value.patched) return;
  selected.value.patched = true;
  props.api.toast(
    "Sample patch staged locally. Rerun the check to update its result.",
  );
}

function rerunCheck() {
  if (!selected.value) return;
  const check = selected.value;
  check.status = check.patched ? "passed" : "failed";
  check.attempts.push({
    id: check.attempts.length + 1,
    result: check.status,
    label: `Simulated rerun ${check.attempts.length}`,
  });
  props.api.toast(
    `Simulated check ${check.status}. No code executed.`,
    check.status === "passed" ? "success" : "info",
  );
}

function exportReport() {
  props.api.download(
    "snippet-check-report.json",
    JSON.stringify(
      {
        prototype: true,
        generatedOn: props.api.today,
        summary: {
          passing: passing.value,
          failing: failing.value,
          attempts: totalAttempts.value,
        },
        checks: state.value.checks,
      },
      null,
      2,
    ),
    "application/json",
  );
  props.api.toast("Local report exported.");
}
</script>

<template>
  <section data-product="docs">
    <header class="workspace-heading">
      <div>
        <div class="eyebrow">Snippetline / documentation checks</div>
        <h1 class="page-title">Your examples are part of the product.</h1>
        <p class="page-description">
          Find the broken example. Give it an owner. Verify the correction.
        </p>
      </div>
      <button class="btn secondary" @click="exportReport">
        Export run report
      </button>
    </header>

    <div class="docs-release panel">
      <div>
        <span class="badge neutral">Sample repository</span
        ><strong> compass / developer-docs </strong>
      </div>
      <div class="small muted">
        Release 2.8 · customer CI runner · {{ api.today }}
      </div>
    </div>

    <div class="metrics">
      <div class="metric">
        <div class="metric-label">Failing examples</div>
        <div class="metric-value">{{ failing }}</div>
        <div class="metric-note">Need a verified correction</div>
      </div>
      <div class="metric">
        <div class="metric-label">Passing examples</div>
        <div class="metric-value">
          {{ passing }} / {{ state.checks.length }}
        </div>
        <div class="metric-note">Latest result per example</div>
      </div>
      <div class="metric">
        <div class="metric-label">Check attempts</div>
        <div class="metric-value">{{ totalAttempts }}</div>
        <div class="metric-note">Includes simulated reruns</div>
      </div>
    </div>

    <div class="docs-workbench">
      <aside class="panel docs-run-list" aria-label="Documentation checks">
        <div class="panel-header">
          <h2>Checks</h2>
          <span class="badge neutral">{{ visibleChecks.length }}</span>
        </div>
        <div class="tabs" aria-label="Check filter">
          <button
            class="tab"
            :class="{ active: filter === 'all' }"
            :aria-pressed="filter === 'all'"
            @click="filter = 'all'"
          >
            All examples
          </button>
          <button
            class="tab"
            :class="{ active: filter === 'failed' }"
            :aria-pressed="filter === 'failed'"
            @click="filter = 'failed'"
          >
            Failing
          </button>
        </div>
        <button
          v-for="check in visibleChecks"
          :key="check.id"
          class="docs-check"
          :class="{ 'is-selected': selectedId === check.id }"
          :aria-pressed="selectedId === check.id"
          @click="selectedId = check.id"
        >
          <span
            class="badge"
            :class="check.status === 'passed' ? 'success' : 'danger'"
            >{{ check.status }}</span
          >
          <strong>{{ check.title }}</strong
          ><span class="small mono muted">{{ check.path }}</span>
          <span class="small muted"
            >{{ check.owner }} · {{ check.language }}</span
          >
        </button>
        <div v-if="visibleChecks.length === 0" class="empty-state">
          All examples pass. Nothing needs triage.
        </div>
      </aside>

      <section
        v-if="selected"
        class="panel docs-code-panel"
        aria-label="Selected documentation example"
      >
        <div class="panel-header">
          <div>
            <div class="eyebrow">Example detail</div>
            <h2>{{ selected.title }}</h2>
          </div>
          <span
            class="badge"
            :class="selected.status === 'passed' ? 'success' : 'danger'"
          >
            {{ selected.status }}</span
          >
        </div>
        <div class="tabs" aria-label="Example detail view">
          <button
            class="tab"
            :class="{ active: detailTab === 'snippet' }"
            :aria-pressed="detailTab === 'snippet'"
            @click="detailTab = 'snippet'"
          >
            Snippet &amp; result
          </button>
          <button
            class="tab"
            :class="{ active: detailTab === 'history' }"
            :aria-pressed="detailTab === 'history'"
            @click="detailTab = 'history'"
          >
            Run history ({{ selected.attempts.length }})
          </button>
        </div>
        <div v-if="detailTab === 'snippet'" class="panel-body stack">
          <div class="small mono muted">
            {{ selected.path }} · {{ selected.language }}
          </div>
          <pre
            class="code-block docs-code"
          ><code>{{ selectedCode }}</code></pre>
          <div v-if="selected.status === 'failed'" class="callout warning">
            <strong>Compiler report</strong>
            <p class="mono small">{{ selected.error }}</p>
          </div>
          <div v-else class="callout success">
            <strong>Example passes its fixture.</strong>
            <p class="small">
              A passing fixture verifies this example, not the live service.
            </p>
          </div>
          <div
            v-if="selected.patched && selected.status === 'failed'"
            class="callout info"
          >
            Sample patch staged. The previous result stays failed until you
            rerun.
          </div>
          <div class="actions">
            <button
              class="btn secondary"
              :disabled="selected.patched"
              @click="applySampleFix"
            >
              {{
                selected.patched ? "Sample patch applied" : "Apply sample fix"
              }}
            </button>
            <button class="btn primary" @click="rerunCheck">
              Simulate rerun
            </button>
          </div>
          <p class="small muted">
            Prototype results use deterministic fixtures. No repository is
            connected.
          </p>
        </div>
        <ol v-else class="panel-body timeline" aria-label="Run history">
          <li
            v-for="attempt in selected.attempts.slice().reverse()"
            :key="attempt.id"
            class="timeline-item"
          >
            <span
              class="badge"
              :class="attempt.result === 'passed' ? 'success' : 'danger'"
              >{{ attempt.result }}</span
            >
            <strong> Attempt {{ attempt.id }}</strong>
            <p class="small muted">{{ attempt.label }}</p>
          </li>
        </ol>
      </section>

      <aside v-if="selected" class="stack docs-context">
        <section class="panel">
          <div class="panel-header"><h2>Resolution owner</h2></div>
          <div class="panel-body stack">
            <strong>{{ selected.owner }}</strong>
            <p class="small muted">
              {{
                selected.assignmentNote ||
                "Keep the correction close to the team that owns it."
              }}
            </p>
            <button class="btn secondary" @click="openAssignment">
              Assign owner
            </button>
          </div>
        </section>
        <section class="panel">
          <div class="panel-header"><h2>Release context</h2></div>
          <div class="panel-body stack small">
            <div>
              <span class="muted">Target SDK</span>
              <p class="mono">Sample SDK 2.8</p>
            </div>
            <div>
              <span class="muted">Runner</span>
              <p>Customer CI · Node / .NET</p>
            </div>
            <div>
              <span class="muted">Publish decision</span>
              <p>Human review required</p>
            </div>
            <div class="divider"></div>
            <p class="muted">
              Only a changed failure needs attention. Passing checks stay quiet.
            </p>
          </div>
        </section>
      </aside>
    </div>

    <dialog
      ref="assignmentDialog"
      class="modal"
      aria-labelledby="docs-assign-title"
    >
      <form @submit.prevent="assignOwner">
        <div class="modal-header">
          <h2 id="docs-assign-title">Assign this example</h2>
          <button
            class="icon-button"
            type="button"
            aria-label="Close assignment"
            @click="assignmentDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p class="small muted">{{ selected?.title }} · local handoff only</p>
          <label class="field"
            >Owner<select v-model="assignmentOwner" class="select">
              <option value="">Choose a teammate</option>
              <option>Maya Chen</option>
              <option>Leo Silva</option>
              <option>Ari Patel</option>
            </select></label
          >
          <label class="field"
            >Handoff context<textarea
              v-model="assignmentReason"
              class="textarea"
              rows="3"
              placeholder="Which SDK change should the owner review?"
            ></textarea>
          </label>
          <p v-if="formError" role="alert" class="callout warning">
            {{ formError }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            class="btn secondary"
            type="button"
            @click="assignmentDialog?.close()"
          >
            Cancel</button
          ><button class="btn primary">Save assignment</button>
        </div>
      </form>
    </dialog>
  </section>
</template>
