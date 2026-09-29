<script setup lang="ts">
import { computed, ref, useTemplateRef, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

const props = defineProps<{ api: PrototypeApi }>();

interface Approval {
  reason: string;
  expires: string;
  staging: string;
  production: string;
}
interface ConfigKey {
  id: string;
  name: string;
  category: string;
  staging: string;
  production: string;
  owner: string;
  approval: Approval | null;
}
interface AuditItem {
  id: number;
  key: string;
  action: string;
  detail: string;
}
type KeyStatus = "missing" | "different" | "approved" | "matching";

const initialKeys: ConfigKey[] = [
  {
    id: "database",
    name: "DATABASE_URL",
    category: "Database endpoint",
    owner: "Platform team",
    staging: "sample-a41c",
    production: "sample-b72e",
    approval: {
      reason: "Each environment uses its own database.",
      expires: "2026-10-29",
      staging: "sample-a41c",
      production: "sample-b72e",
    },
  },
  {
    id: "payments",
    name: "PAYMENT_API_KEY",
    category: "Sensitive key",
    owner: "Billing team",
    staging: "sample-c31a",
    production: "",
    approval: null,
  },
  {
    id: "log",
    name: "LOG_LEVEL",
    category: "Application setting",
    owner: "Platform team",
    staging: "sample-d24b",
    production: "sample-e59c",
    approval: null,
  },
  {
    id: "session",
    name: "SESSION_SIGNING_KEY",
    category: "Sensitive key",
    owner: "Identity team",
    staging: "",
    production: "sample-f88d",
    approval: null,
  },
  {
    id: "region",
    name: "DEFAULT_REGION",
    category: "Application setting",
    owner: "Platform team",
    staging: "sample-g15f",
    production: "sample-g15f",
    approval: null,
  },
  {
    id: "search",
    name: "SEARCH_ENABLED",
    category: "Feature setting",
    owner: "Search team",
    staging: "sample-h73a",
    production: "sample-h73a",
    approval: null,
  },
];
const approvalDialog = useTemplateRef<HTMLDialogElement>("approvalDialog");
const resolutionDialog = useTemplateRef<HTMLDialogElement>("resolutionDialog");
const state = ref(
  props.api.state({
    keys: initialKeys,
    manifestVersion: 1,
    audit: [] as AuditItem[],
  }),
);
const selectedId = ref("payments");
const filter = ref("all");
const reason = ref("");
const expiry = ref("2026-10-29");
const sourceRun = ref("");
const formError = ref("");

const selected = computed(() =>
  state.value.keys.find((key) => key.id === selectedId.value),
);
const missingCount = computed(
  () => state.value.keys.filter((key) => getStatus(key) === "missing").length,
);
const differencesCount = computed(
  () => state.value.keys.filter((key) => getStatus(key) === "different").length,
);
const approvedCount = computed(
  () => state.value.keys.filter((key) => getStatus(key) === "approved").length,
);
const matchingCount = computed(
  () => state.value.keys.filter((key) => getStatus(key) === "matching").length,
);
const visibleKeys = computed(() =>
  state.value.keys.filter(
    (key) =>
      filter.value === "all" ||
      ["missing", "different"].includes(getStatus(key)),
  ),
);
const recentAudit = computed(() =>
  state.value.audit.slice().reverse().slice(0, 5),
);

watch(state, (value) => props.api.save(value), { deep: true });

function getStatus(key: ConfigKey): KeyStatus {
  if (!key.staging || !key.production) return "missing";
  if (key.staging === key.production) return "matching";
  if (
    key.approval &&
    key.approval.expires >= props.api.today &&
    key.approval.staging === key.staging &&
    key.approval.production === key.production
  )
    return "approved";
  return "different";
}

function statusLabel(status: KeyStatus) {
  return {
    missing: "Missing key",
    different: "Review difference",
    approved: "Approved difference",
    matching: "Matching",
  }[status];
}

function statusClass(status: KeyStatus) {
  return {
    missing: "danger",
    different: "warning",
    approved: "info",
    matching: "success",
  }[status];
}

function addAudit(key: string, action: string, detail: string) {
  state.value.audit.push({
    id: state.value.audit.length + 1,
    key,
    action,
    detail,
  });
}

function openApproval() {
  reason.value = "";
  expiry.value = "2026-10-29";
  formError.value = "";
  approvalDialog.value?.showModal();
}

function approveDifference() {
  const context = reason.value.trim();
  const expiration = Date.parse(`${expiry.value}T00:00:00Z`);
  const today = Date.parse(`${props.api.today}T00:00:00Z`);
  if (
    context.length < 12 ||
    !Number.isFinite(expiration) ||
    expiration < today ||
    expiration > today + 90 * 86400000
  ) {
    formError.value =
      "Add at least 12 characters of context and an expiry within the next 90 days.";
    return;
  }
  if (!selected.value || getStatus(selected.value) !== "different") {
    formError.value = "Only a present, unapproved difference can be approved.";
    return;
  }
  selected.value.approval = {
    reason: context,
    expires: expiry.value,
    staging: selected.value.staging,
    production: selected.value.production,
  };
  addAudit(selected.value.name, "Difference approved", context);
  approvalDialog.value?.close();
  props.api.toast(
    "Difference approved locally for this exact fingerprint pair.",
  );
}

function openResolution() {
  sourceRun.value = "";
  formError.value = "";
  resolutionDialog.value?.showModal();
}

function resolveMissingKey() {
  const run = sourceRun.value.trim();
  if (run.length < 5) {
    formError.value =
      "Enter a sample collector run reference of at least 5 characters.";
    return;
  }
  if (!selected.value || getStatus(selected.value) !== "missing") return;
  const key = selected.value;
  const target = key.staging ? "production" : "staging";
  state.value.manifestVersion += 1;
  key[target] = `sample-new-${state.value.manifestVersion}`;
  addAudit(
    key.name,
    "Simulated missing key resolved",
    `${target} receipt from ${run}; new difference needs review.`,
  );
  resolutionDialog.value?.close();
  props.api.toast(
    "Simulated manifest received. The key is present; its difference still needs review.",
    "info",
  );
}

function revokeApproval() {
  if (!selected.value) return;
  selected.value.approval = null;
  addAudit(
    selected.value.name,
    "Approval revoked",
    "Difference returned to review.",
  );
  props.api.toast("Approval revoked locally.");
}

function simulateNewManifest() {
  const key = state.value.keys.find((item) => item.id === "database");
  if (!key) return;
  state.value.manifestVersion += 1;
  key.production = `sample-db-${state.value.manifestVersion}`;
  selectedId.value = key.id;
  addAudit(
    key.name,
    "Simulated manifest imported",
    "Production fingerprint changed; previous approval no longer applies.",
  );
  props.api.toast(
    "Sample database fingerprint changed. Its previous approval no longer covers this pair.",
    "info",
  );
}

function exportComparison() {
  props.api.download(
    "configuration-comparison.json",
    JSON.stringify(
      {
        prototype: true,
        comparedOn: props.api.today,
        manifestVersion: state.value.manifestVersion,
        summary: {
          missing: missingCount.value,
          review: differencesCount.value,
          approved: approvedCount.value,
          matching: matchingCount.value,
        },
        keys: state.value.keys.map((key) => ({
          ...key,
          status: getStatus(key),
        })),
        audit: state.value.audit,
      },
      null,
      2,
    ),
    "application/json",
  );
  props.api.toast("Local comparison exported. All fingerprints are synthetic.");
}
</script>

<template>
  <section data-product="config">
    <header class="workspace-heading">
      <div>
        <div class="eyebrow">Parity / environment review</div>
        <h1 class="page-title">Different on purpose?</h1>
        <p class="page-description">
          Find missing keys. Explain intentional differences. Keep the evidence
          together.
        </p>
      </div>
      <div class="actions">
        <button class="btn secondary" @click="exportComparison">
          Export comparison
        </button>
        <button class="btn primary" @click="simulateNewManifest">
          Simulate new manifest
        </button>
      </div>
    </header>

    <div class="config-environments panel">
      <div>
        <span class="badge neutral">Sample project</span
        ><strong> compass-api </strong>
        <span class="small muted"
          >Manifest pair #{{ state.manifestVersion }}</span
        >
      </div>
      <div class="config-pair">
        <span><span class="config-env-dot"></span> Staging</span>
        <span class="muted" aria-hidden="true">↔</span
        ><span><span class="config-env-dot production"></span> Production</span>
      </div>
    </div>

    <div class="metrics">
      <div class="metric">
        <div class="metric-label">Missing keys</div>
        <div class="metric-value">{{ missingCount }}</div>
        <div class="metric-note">Require a customer-side correction</div>
      </div>
      <div class="metric">
        <div class="metric-label">Differences to review</div>
        <div class="metric-value">{{ differencesCount }}</div>
        <div class="metric-note">Present in both environments</div>
      </div>
      <div class="metric">
        <div class="metric-label">Approved differences</div>
        <div class="metric-value">{{ approvedCount }}</div>
        <div class="metric-note">{{ matchingCount }} more keys match</div>
      </div>
    </div>

    <div class="config-workspace">
      <section class="panel config-comparison">
        <div class="panel-header">
          <h2>Key comparison</h2>
          <span class="small muted">Synthetic fingerprints only</span>
        </div>
        <div class="tabs" aria-label="Comparison filter">
          <button
            class="tab"
            :class="{ active: filter === 'all' }"
            :aria-pressed="filter === 'all'"
            @click="filter = 'all'"
          >
            All keys ({{ state.keys.length }})
          </button>
          <button
            class="tab"
            :class="{ active: filter === 'review' }"
            :aria-pressed="filter === 'review'"
            @click="filter = 'review'"
          >
            Needs review ({{ missingCount + differencesCount }})
          </button>
        </div>
        <div class="table-wrap">
          <table class="data-table config-table">
            <thead>
              <tr>
                <th scope="col">Key</th>
                <th scope="col">Staging</th>
                <th scope="col">Production</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="key in visibleKeys"
                :key="key.id"
                :class="{ selected: selectedId === key.id }"
              >
                <th scope="row">
                  <button
                    class="config-key"
                    :aria-pressed="selectedId === key.id"
                    @click="selectedId = key.id"
                  >
                    <span class="mono">{{ key.name }}</span
                    ><span class="badge" :class="statusClass(getStatus(key))">
                      {{ statusLabel(getStatus(key)) }}</span
                    >
                  </button>
                </th>
                <td>
                  <span v-if="key.staging" class="mono small">{{
                    key.staging
                  }}</span>
                  <span v-else class="badge danger">Absent</span>
                </td>
                <td>
                  <span v-if="key.production" class="mono small">{{
                    key.production
                  }}</span>
                  <span v-else class="badge danger">Absent</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="visibleKeys.length === 0" class="empty-state">
          Every key is present and every difference is reviewed.
        </div>
        <div class="config-footnote small muted">
          A matching fingerprint proves equality, not correctness.
        </div>
      </section>

      <aside v-if="selected" class="panel config-detail">
        <div class="panel-header">
          <div>
            <div class="eyebrow">Review decision</div>
            <h2 class="mono">{{ selected.name }}</h2>
          </div>
        </div>
        <div class="panel-body stack">
          <span class="badge" :class="statusClass(getStatus(selected))">{{
            statusLabel(getStatus(selected))
          }}</span>
          <div class="small">
            <span class="muted">Owner</span>
            <p>{{ selected.owner }} · {{ selected.category }}</p>
          </div>
          <template v-if="getStatus(selected) === 'missing'">
            <div class="callout warning">
              <strong
                >Missing in
                {{ selected.staging ? "production" : "staging" }}.</strong
              >
              <p class="small">
                Correct the environment in your own tools. A new manifest
                provides evidence of the fix.
              </p>
            </div>
            <button class="btn primary" @click="openResolution">
              Record simulated fix
            </button>
          </template>
          <template v-else-if="getStatus(selected) === 'different'">
            <div v-if="selected.approval" class="callout warning">
              <strong>Previous approval no longer applies.</strong>
              <p class="small">
                The fingerprint pair changed or the review period expired. Make
                a fresh decision.
              </p>
            </div>
            <div v-else class="callout info">
              <strong>Both keys exist; the fingerprints differ.</strong>
              <p class="small">
                Environment-specific values can be intentional. Document why
                this pair is acceptable.
              </p>
            </div>
            <button class="btn primary" @click="openApproval">
              Approve difference
            </button>
          </template>
          <template v-else-if="getStatus(selected) === 'approved'">
            <div class="callout success">
              <strong>Intentional difference</strong>
              <p class="small">{{ selected.approval?.reason }}</p>
              <p class="small">
                Review expires {{ selected.approval?.expires }}.
              </p>
            </div>
            <button class="btn secondary" @click="revokeApproval">
              Revoke approval
            </button>
          </template>
          <div v-else class="callout success">
            <strong>The fingerprints match.</strong>
            <p class="small">
              No parity issue was found. Environment policy remains your team's
              responsibility.
            </p>
          </div>
          <div class="divider"></div>
          <p class="small muted">
            Only synthetic fingerprints appear here. Keep review notes free of
            secret values.
          </p>
        </div>
      </aside>
    </div>

    <section class="panel config-audit">
      <div class="panel-header">
        <h2>Decision trail</h2>
        <span class="badge neutral">{{ state.audit.length }} local events</span>
      </div>
      <div v-if="recentAudit.length === 0" class="panel-body small muted">
        Your review decisions will appear here.
      </div>
      <div
        v-for="event in recentAudit"
        :key="event.id"
        class="list-row config-audit-row"
      >
        <span class="mono muted small">#{{ event.id }}</span>
        <div>
          <strong>{{ event.action }}</strong>
          <p class="small muted">{{ event.key }} · {{ event.detail }}</p>
        </div>
      </div>
    </section>

    <dialog
      ref="approvalDialog"
      class="modal"
      aria-labelledby="config-approval-title"
    >
      <form @submit.prevent="approveDifference">
        <div class="modal-header">
          <h2 id="config-approval-title">Approve an intentional difference</h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close approval"
            @click="approvalDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p class="small mono">{{ selected?.name }}</p>
          <label class="field"
            >Why should these values differ?<textarea
              v-model="reason"
              class="textarea"
              rows="3"
              placeholder="Describe the environment-specific behavior; do not paste values."
            ></textarea>
          </label>
          <label class="field"
            >Review expiry<input v-model="expiry" type="date" class="input"
          /></label>
          <p class="small muted">
            Approval covers this exact fingerprint pair. A new value requires
            review.
          </p>
          <p v-if="formError" class="callout warning" role="alert">
            {{ formError }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn secondary"
            @click="approvalDialog?.close()"
          >
            Cancel
          </button>
          <button class="btn primary">Save approval</button>
        </div>
      </form>
    </dialog>

    <dialog
      ref="resolutionDialog"
      class="modal"
      aria-labelledby="config-resolution-title"
    >
      <form @submit.prevent="resolveMissingKey">
        <div class="modal-header">
          <h2 id="config-resolution-title">
            Record a simulated customer-side fix
          </h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close resolution"
            @click="resolutionDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p class="small">
            A synthetic manifest will mark the key present with a distinct
            fingerprint.
          </p>
          <label class="field"
            >Collector run reference<input
              v-model="sourceRun"
              class="input"
              placeholder="sample-run-104"
          /></label>
          <p class="callout info small">
            This changes the mock manifest only. No environment is edited.
          </p>
          <p v-if="formError" class="callout warning" role="alert">
            {{ formError }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn secondary"
            @click="resolutionDialog?.close()"
          >
            Cancel
          </button>
          <button class="btn primary">Confirm simulated manifest</button>
        </div>
      </form>
    </dialog>
  </section>
</template>
