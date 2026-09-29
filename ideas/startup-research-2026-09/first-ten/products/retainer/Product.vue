<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

interface Entry {
  id: string;
  task: string;
  minutes: number;
  reviewed: boolean;
  date: string;
}
interface Extension {
  id: string;
  minutes: number;
  note: string;
  status: "requested" | "approved";
  approver: string;
}
interface Ledger {
  entries: Entry[];
  extensions: Extension[];
  digest: string;
}
const props = defineProps<{ api: PrototypeApi }>();
const state = ref(
  props.api.state<Ledger>({
    entries: [
      {
        id: "T-101",
        task: "September landing-page updates",
        minutes: 540,
        reviewed: true,
        date: "2026-09-10",
      },
      {
        id: "T-102",
        task: "Analytics repair and verification",
        minutes: 390,
        reviewed: true,
        date: "2026-09-17",
      },
      {
        id: "T-103",
        task: "Campaign design revisions",
        minutes: 210,
        reviewed: true,
        date: "2026-09-22",
      },
      {
        id: "T-104",
        task: "New partner page — confirm allowance",
        minutes: 240,
        reviewed: false,
        date: "2026-09-28",
      },
    ],
    extensions: [],
    digest: "",
  }),
);
const selectedId = ref("T-104");
const importDialog = ref<HTMLDialogElement | null>(null);
const extensionDialog = ref<HTMLDialogElement | null>(null);
const csv = ref("id,task,hours\nT-105,Launch handoff,3.5");
const importError = ref("");
const preview = ref<Entry[]>([]);
const extraHours = ref("3");
const extraNote = ref(
  "Finish the launch handoff and document the new partner page.",
);
const extensionError = ref("");
const approver = ref("Avery Chen");
const baseMinutes = 1440;
const rate = 95;
const confirmed = computed(() =>
  state.value.entries
    .filter((entry) => entry.reviewed)
    .reduce((sum, entry) => sum + entry.minutes, 0),
);
const unreviewed = computed(() =>
  state.value.entries
    .filter((entry) => !entry.reviewed)
    .reduce((sum, entry) => sum + entry.minutes, 0),
);
const approvedExtra = computed(() =>
  state.value.extensions
    .filter((item) => item.status === "approved")
    .reduce((sum, item) => sum + item.minutes, 0),
);
const available = computed(
  () => baseMinutes + approvedExtra.value - confirmed.value,
);
const selected = computed(() =>
  state.value.entries.find((entry) => entry.id === selectedId.value),
);
const pendingRequest = computed(() =>
  state.value.extensions.find((item) => item.status === "requested"),
);
watch(state, (value) => props.api.save(value), { deep: true });
watch(csv, () => {
  preview.value = [];
  importError.value = "";
});

function hours(minutes: number): string {
  return (minutes / 60).toLocaleString("en-US", { maximumFractionDigits: 2 });
}
function openImport(): void {
  preview.value = [];
  importError.value = "";
  importDialog.value?.showModal();
}
function reviewImport(): void {
  importError.value = "";
  preview.value = [];
  const lines = csv.value.trim().split(/\r?\n/);
  if (lines.shift()?.trim().toLowerCase() !== "id,task,hours") {
    importError.value =
      "Use the header id,task,hours. This prototype accepts unquoted comma-separated rows.";
    return;
  }
  if (!lines.length || lines.length > 100) {
    importError.value = "Include between 1 and 100 entries.";
    return;
  }
  const known = new Set(state.value.entries.map((entry) => entry.id));
  const rows: Entry[] = [];
  for (const [index, line] of lines.entries()) {
    const cells = line.split(",").map((cell) => cell.trim());
    const [id, task, amount] = cells;
    const minutes = Math.round(Number(amount) * 60);
    if (
      cells.length !== 3 ||
      !id ||
      !task ||
      !amount ||
      !Number.isFinite(Number(amount)) ||
      minutes <= 0 ||
      minutes > 1440
    ) {
      importError.value = `Row ${index + 2}: provide an ID, task, and hours greater than 0 and no more than 24.`;
      return;
    }
    if (known.has(id)) {
      importError.value = `Row ${index + 2}: ${id} already exists. Repeated imports cannot duplicate time.`;
      return;
    }
    known.add(id);
    rows.push({ id, task, minutes, reviewed: false, date: props.api.today });
  }
  preview.value = rows;
}
function commitImport(): void {
  if (!preview.value.length) return;
  state.value.entries.push(...preview.value);
  selectedId.value = preview.value[0]?.id ?? selectedId.value;
  state.value.digest = "";
  props.api.toast(
    `${preview.value.length} entries imported locally for review.`,
  );
  preview.value = [];
  importDialog.value?.close();
}
function reconcile(): void {
  if (!selected.value || selected.value.reviewed) return;
  selected.value.reviewed = true;
  state.value.digest = "";
  props.api.toast(
    "Entry reconciled. The allowance and client statement now include it.",
  );
}
function reopen(): void {
  if (!selected.value?.reviewed) return;
  selected.value.reviewed = false;
  state.value.digest = "";
  props.api.toast(
    "Entry returned to review; it no longer counts as confirmed consumption.",
  );
}
function openExtension(): void {
  extensionError.value = "";
  extensionDialog.value?.showModal();
}
function requestExtension(): void {
  extensionError.value = "";
  const minutes = Math.round(Number(extraHours.value) * 60);
  if (
    !extraHours.value.trim() ||
    !Number.isFinite(minutes) ||
    minutes <= 0 ||
    minutes > 2400 ||
    extraNote.value.trim().length < 12
  ) {
    extensionError.value =
      "Enter positive extra hours (maximum 40) and a reason of at least 12 characters.";
    return;
  }
  if (pendingRequest.value) {
    extensionError.value =
      "Resolve the existing request before creating another.";
    return;
  }
  state.value.extensions.push({
    id: `O-${state.value.extensions.length + 1}`,
    minutes,
    note: extraNote.value.trim(),
    status: "requested",
    approver: "",
  });
  state.value.digest = "";
  extensionDialog.value?.close();
  props.api.toast(
    "Overage request prepared locally. No client message was sent.",
  );
}
function approveExtension(): void {
  const request = pendingRequest.value;
  if (!request) return;
  if (approver.value.trim().length < 3) {
    extensionError.value = "Add the client approver’s full name.";
    return;
  }
  request.approver = approver.value.trim();
  request.status = "approved";
  state.value.digest = "";
  extensionError.value = "";
  props.api.toast(
    "Client approval simulated. The extra allowance is now available.",
  );
}
function prepareDigest(): void {
  state.value.digest = `Brightside Lab · September 2026\nConfirmed: ${hours(confirmed.value)} h\nAuthorized allowance: ${hours(baseMinutes + approvedExtra.value)} h\nBalance: ${hours(available.value)} h\nStill under review: ${hours(unreviewed.value)} h\nApproved extra fees: ${props.api.money((approvedExtra.value / 60) * rate)}\nThis is a synthetic local statement, not an invoice.`;
  props.api.toast("Client statement prepared from the current ledger.");
}
function exportLedger(): void {
  props.api.download(
    "brightside-september-ledger.json",
    JSON.stringify(
      {
        synthetic: true,
        client: "Brightside Lab",
        period: "2026-09",
        allowanceMinutes: baseMinutes,
        confirmedMinutes: confirmed.value,
        approvedExtraMinutes: approvedExtra.value,
        balanceMinutes: available.value,
        ...state.value,
      },
      null,
      2,
    ),
    "application/json",
  );
}
</script>

<template>
  <section data-product="retainer">
    <header class="workspace-heading">
      <div>
        <p class="eyebrow">ALLOWANCE / SEPTEMBER 2026</p>
        <h1 class="page-title">Make the next request clear.</h1>
        <p class="page-description">
          Brightside Lab · website care retainer · Northline Studio
        </p>
      </div>
      <div class="actions">
        <button class="btn secondary" @click="exportLedger">
          Export ledger</button
        ><button class="btn primary" @click="openImport">Import time</button>
      </div>
    </header>
    <div class="retainer-layout">
      <div class="stack">
        <section class="panel allowance-strip" aria-label="Retainer allowance">
          <div>
            <span class="metric-label">Confirmed work</span
            ><strong>{{ hours(confirmed) }} <small>hours</small></strong>
          </div>
          <div>
            <span class="metric-label">Authorized allowance</span
            ><strong
              >{{ hours(baseMinutes + approvedExtra) }}
              <small>hours</small></strong
            >
          </div>
          <div>
            <span class="metric-label">{{
              available < 0 ? "Needs approval" : "Available"
            }}</span
            ><strong :class="{ 'over-limit': available < 0 }"
              >{{ hours(Math.abs(available)) }} <small>hours</small></strong
            >
          </div>
          <progress
            class="allowance-meter"
            :value="confirmed"
            :max="baseMinutes + approvedExtra"
            :aria-label="`${hours(confirmed)} of ${hours(baseMinutes + approvedExtra)} hours consumed`"
          ></progress>
          <p class="small muted">
            {{ hours(unreviewed) }} hours await reconciliation. The original
            24-hour allowance stays in the record.
          </p>
        </section>
        <section class="panel">
          <div class="panel-header">
            <div>
              <p class="eyebrow">01 / RECONCILE</p>
              <h2>What consumed the allowance?</h2>
            </div>
            <span class="badge neutral"
              >{{ state.entries.length }} entries</span
            >
          </div>
          <div class="table-wrap">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Work delivered</th>
                  <th>Hours</th>
                  <th>Review</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="entry in state.entries"
                  :key="entry.id"
                  :class="{ 'entry-selected': selectedId === entry.id }"
                >
                  <td>
                    <button class="entry-link" @click="selectedId = entry.id">
                      {{ entry.task }}</button
                    ><small class="muted"
                      >{{ entry.date }} · {{ entry.id }}</small
                    >
                  </td>
                  <td class="mono">{{ hours(entry.minutes) }}</td>
                  <td>
                    <span
                      class="badge"
                      :class="entry.reviewed ? 'success' : 'warning'"
                      >{{ entry.reviewed ? "Confirmed" : "Review" }}</span
                    >
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="!state.entries.length" class="empty-state">
            Import a time export to start this month’s ledger.
          </div>
        </section>
        <section v-if="selected" class="panel panel-body entry-detail">
          <p class="eyebrow">ENTRY / {{ selected.id }}</p>
          <h3>{{ selected.task }}</h3>
          <p>
            {{ hours(selected.minutes) }} hours from the supplied time export.
            Confirm that this work belongs to the September retainer before
            including it in the client statement.
          </p>
          <div class="actions">
            <button
              v-if="!selected.reviewed"
              class="btn primary"
              @click="reconcile"
            >
              Reconcile entry</button
            ><button v-else class="btn secondary" @click="reopen">
              Return to review</button
            ><span class="small muted"
              >Source retained · no invoice created</span
            >
          </div>
        </section>
      </div>
      <aside class="stack">
        <section class="panel client-statement">
          <div class="panel-body">
            <p class="eyebrow">02 / CLIENT VIEW</p>
            <h2>September statement</h2>
            <p class="muted">
              A shared explanation, before an unexpected bill.
            </p>
            <div class="statement-line">
              <span>Included allowance</span><strong>24 h</strong>
            </div>
            <div class="statement-line">
              <span>Approved additions</span
              ><strong>{{ hours(approvedExtra) }} h</strong>
            </div>
            <div class="statement-line">
              <span>Confirmed consumption</span
              ><strong>{{ hours(confirmed) }} h</strong>
            </div>
            <div class="statement-line total">
              <span>{{
                available < 0 ? "Unapproved overage" : "Remaining"
              }}</span
              ><strong>{{ hours(Math.abs(available)) }} h</strong>
            </div>
            <p v-if="available < 0" class="callout warning">
              This work exceeds the authorized allowance. A request alone does
              not authorize extra charges.
            </p>
            <button class="btn secondary" @click="prepareDigest">
              Prepare client statement
            </button>
            <pre v-if="state.digest" class="digest-preview">{{
              state.digest
            }}</pre>
          </div>
        </section>
        <section class="panel panel-body">
          <p class="eyebrow">03 / AGREE THE NEXT STEP</p>
          <h3>Overage decisions</h3>
          <p class="small muted">
            Extra work at {{ api.money(rate) }}/hour. Client approval is
            simulated in this workspace.
          </p>
          <div
            v-for="extension in state.extensions"
            :key="extension.id"
            class="extension-row"
          >
            <div class="actions">
              <strong
                >{{ hours(extension.minutes) }} h ·
                {{ api.money((extension.minutes / 60) * rate) }}</strong
              ><span
                class="badge"
                :class="extension.status === 'approved' ? 'success' : 'warning'"
                >{{ extension.status }}</span
              >
            </div>
            <p>{{ extension.note }}</p>
            <small v-if="extension.approver"
              >Approved by {{ extension.approver }} · simulated</small
            >
          </div>
          <p v-if="!state.extensions.length" class="muted small">
            No extra work authorized this month.
          </p>
          <div v-if="pendingRequest" class="stack">
            <label class="field"
              >Client approver<input v-model="approver" class="input"
            /></label>
            <p v-if="extensionError" role="alert" class="callout warning">
              {{ extensionError }}
            </p>
            <button class="btn primary" @click="approveExtension">
              Simulate client approval
            </button>
          </div>
          <button v-else class="btn secondary" @click="openExtension">
            Request extra allowance
          </button>
        </section>
      </aside>
    </div>
    <dialog
      ref="importDialog"
      class="modal"
      aria-labelledby="retainer-import-title"
    >
      <form @submit.prevent="reviewImport">
        <div class="modal-header">
          <h2 id="retainer-import-title">Import time for review</h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close import"
            @click="importDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p class="small muted">
            Paste up to 100 unquoted CSV rows. Repeated source IDs are rejected.
            Imported time needs review before consuming the allowance.
          </p>
          <label class="field"
            >Time export<textarea
              v-model="csv"
              class="textarea mono"
              rows="7"
            ></textarea>
          </label>
          <p v-if="importError" role="alert" class="callout warning">
            {{ importError }}
          </p>
          <div v-if="preview.length" class="callout success">
            {{ preview.length }} valid entries ·
            {{
              hours(preview.reduce((sum, entry) => sum + entry.minutes, 0))
            }}
            hours ready for review.
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn ghost"
            @click="importDialog?.close()"
          >
            Cancel</button
          ><button type="submit" class="btn secondary">Review import</button
          ><button
            v-if="preview.length"
            type="button"
            class="btn primary"
            @click="commitImport"
          >
            Import {{ preview.length }}
            {{ preview.length === 1 ? "entry" : "entries" }}
          </button>
        </div>
      </form>
    </dialog>
    <dialog
      ref="extensionDialog"
      class="modal"
      aria-labelledby="retainer-extra-title"
    >
      <form @submit.prevent="requestExtension">
        <div class="modal-header">
          <h2 id="retainer-extra-title">Request extra allowance</h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close allowance request"
            @click="extensionDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <label class="field"
            >Extra hours<input
              v-model="extraHours"
              class="input"
              inputmode="decimal" /></label
          ><label class="field"
            >What will this cover?<textarea
              v-model="extraNote"
              class="textarea"
              rows="3"
            ></textarea>
          </label>
          <p v-if="extensionError" role="alert" class="callout warning">
            {{ extensionError }}
          </p>
          <p class="small muted">
            Prepared locally. No email is sent and no payment is collected.
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn ghost"
            @click="extensionDialog?.close()"
          >
            Cancel</button
          ><button class="btn primary" type="submit">
            Prepare approval request
          </button>
        </div>
      </form>
    </dialog>
  </section>
</template>
