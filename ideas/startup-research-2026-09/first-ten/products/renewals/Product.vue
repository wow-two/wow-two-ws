<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

type Decision = "undecided" | "renew" | "cancel";
interface Renewal {
  id: string;
  vendor: string;
  category: string;
  annualCost: number;
  renewalDate: string;
  noticeDays: number;
  owner: string;
  acknowledged: boolean;
  decision: Decision;
  reason: string;
  source: string;
  history: string[];
}
interface RenewalState {
  contracts: Renewal[];
}
const props = defineProps<{ api: PrototypeApi }>();
const state = ref(
  props.api.state<RenewalState>({
    contracts: [
      {
        id: "R-101",
        vendor: "SlateDesk",
        category: "Customer support",
        annualCost: 2400,
        renewalDate: "2026-10-31",
        noticeDays: 30,
        owner: "Maya Patel",
        acknowledged: false,
        decision: "undecided",
        reason: "",
        source: "Master agreement · section 8.2",
        history: [
          "2026-09-15 · notice period entered and checked by Maya Patel",
        ],
      },
      {
        id: "R-102",
        vendor: "Mailflow",
        category: "Email delivery",
        annualCost: 720,
        renewalDate: "2026-11-15",
        noticeDays: 30,
        owner: "Jonas Reed",
        acknowledged: true,
        decision: "undecided",
        reason: "",
        source: "Order form · renewal paragraph",
        history: ["2026-09-20 · Jonas Reed acknowledged the notice window"],
      },
      {
        id: "R-103",
        vendor: "CloudMetric",
        category: "Product analytics",
        annualCost: 1800,
        renewalDate: "2026-12-01",
        noticeDays: 30,
        owner: "Leah Okafor",
        acknowledged: false,
        decision: "undecided",
        reason: "",
        source: "Subscription terms · section 4",
        history: ["2026-09-16 · imported from owner-maintained register"],
      },
      {
        id: "R-104",
        vendor: "SketchPad",
        category: "Design collaboration",
        annualCost: 480,
        renewalDate: "2026-10-10",
        noticeDays: 30,
        owner: "Maya Patel",
        acknowledged: false,
        decision: "undecided",
        reason: "",
        source: "Annual order confirmation",
        history: ["2026-09-28 · late notice window discovered during review"],
      },
      {
        id: "R-105",
        vendor: "Atlas Notes",
        category: "Knowledge base",
        annualCost: 360,
        renewalDate: "2027-01-01",
        noticeDays: 0,
        owner: "Leah Okafor",
        acknowledged: true,
        decision: "renew",
        reason: "Team reviewed the usage and retained the current plan.",
        source: "Owner-confirmed billing settings",
        history: ["2026-09-25 · renewal intent recorded by Leah Okafor"],
      },
    ],
  }),
);
const selectedId = ref("R-101");
const view = ref<"open" | "all">("open");
const ownerDraft = ref("Maya Patel");
const ownerError = ref("");
const decisionDialog = ref<HTMLDialogElement | null>(null);
const addDialog = ref<HTMLDialogElement | null>(null);
const decisionDraft = ref<"renew" | "cancel">("renew");
const decisionReason = ref("");
const decisionError = ref("");
const vendorDraft = ref("");
const costDraft = ref("");
const dateDraft = ref("2026-12-15");
const noticeDraft = ref("30");
const sourceDraft = ref("");
const addError = ref("");
const owners = ["Maya Patel", "Jonas Reed", "Leah Okafor"];
const selected = computed(() =>
  state.value.contracts.find((contract) => contract.id === selectedId.value),
);
const openContracts = computed(() =>
  state.value.contracts.filter((contract) => contract.decision === "undecided"),
);
const timeline = computed(() =>
  state.value.contracts
    .filter(
      (contract) => view.value === "all" || contract.decision === "undecided",
    )
    .sort((a, b) => deadline(a).localeCompare(deadline(b))),
);
const actionValue = computed(() =>
  openContracts.value
    .filter((contract) => daysLeft(contract) <= 30)
    .reduce((sum, contract) => sum + contract.annualCost, 0),
);
watch(state, (value) => props.api.save(value), { deep: true });
watch(
  selectedId,
  () => {
    ownerDraft.value = selected.value?.owner ?? owners[0] ?? "";
    ownerError.value = "";
  },
  { immediate: true },
);

function deadline(contract: Renewal): string {
  const date = new Date(`${contract.renewalDate}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() - contract.noticeDays);
  return date.toISOString().slice(0, 10);
}
function daysLeft(contract: Renewal): number {
  return Math.round(
    (new Date(`${deadline(contract)}T12:00:00Z`).getTime() -
      new Date(`${props.api.today}T12:00:00Z`).getTime()) /
      86400000,
  );
}
function urgency(contract: Renewal): string {
  const days = daysLeft(contract);
  return days < 0
    ? `${Math.abs(days)} days past notice date`
    : days === 0
      ? "Notice date is today"
      : `${days} days to decide`;
}
function assignOwner(): void {
  if (!selected.value) return;
  if (!owners.includes(ownerDraft.value)) {
    ownerError.value = "Select a named owner.";
    return;
  }
  if (selected.value.owner === ownerDraft.value) {
    ownerError.value = "Choose a different owner to record a handoff.";
    return;
  }
  selected.value.owner = ownerDraft.value;
  selected.value.acknowledged = false;
  selected.value.history.unshift(
    `${props.api.today} · assigned to ${ownerDraft.value}; acknowledgment required`,
  );
  ownerError.value = "";
  props.api.toast("Owner reassigned locally. No notification was sent.");
}
function acknowledge(): void {
  if (!selected.value || selected.value.acknowledged) return;
  selected.value.acknowledged = true;
  selected.value.history.unshift(
    `${props.api.today} · ${selected.value.owner} acknowledged the date · simulated`,
  );
  props.api.toast("Owner acknowledgment simulated and recorded.");
}
function openDecision(): void {
  if (!selected.value) return;
  decisionDraft.value =
    selected.value.decision === "cancel" ? "cancel" : "renew";
  decisionReason.value = selected.value.reason;
  decisionError.value = "";
  decisionDialog.value?.showModal();
}
function recordDecision(): void {
  if (!selected.value) return;
  decisionError.value = "";
  if (!selected.value.acknowledged) {
    decisionError.value =
      "The current owner must acknowledge the notice window first.";
    return;
  }
  if (decisionReason.value.trim().length < 15) {
    decisionError.value =
      "Explain the decision and next step in at least 15 characters.";
    return;
  }
  selected.value.decision = decisionDraft.value;
  selected.value.reason = decisionReason.value.trim();
  selected.value.history.unshift(
    `${props.api.today} · ${selected.value.owner} recorded ${decisionDraft.value} intent · ${decisionReason.value.trim()}`,
  );
  view.value = "all";
  decisionDialog.value?.close();
  props.api.toast(
    "Decision recorded locally. The vendor subscription has not been changed.",
  );
}
function reopenDecision(): void {
  if (!selected.value || selected.value.decision === "undecided") return;
  selected.value.history.unshift(
    `${props.api.today} · previous ${selected.value.decision} intent reopened for review`,
  );
  selected.value.decision = "undecided";
  selected.value.reason = "";
  props.api.toast("Decision reopened; previous intent remains in the history.");
}
function addContract(): void {
  addError.value = "";
  const parsed = new Date(`${dateDraft.value}T12:00:00Z`);
  const cost = Number(costDraft.value);
  const days = Number(noticeDraft.value);
  const dateValid =
    /^\d{4}-\d{2}-\d{2}$/.test(dateDraft.value) &&
    !Number.isNaN(parsed.getTime()) &&
    parsed.toISOString().slice(0, 10) === dateDraft.value;
  if (
    vendorDraft.value.trim().length < 3 ||
    !dateValid ||
    !costDraft.value.trim() ||
    !Number.isFinite(cost) ||
    cost < 0 ||
    cost > 1000000 ||
    !noticeDraft.value.trim() ||
    !Number.isInteger(days) ||
    days < 0 ||
    days > 365 ||
    sourceDraft.value.trim().length < 8
  ) {
    addError.value =
      "Provide vendor, valid renewal date, nonnegative annual USD cost, 0–365 notice days, and a source reference.";
    return;
  }
  if (
    state.value.contracts.some(
      (contract) =>
        contract.vendor.toLowerCase() ===
        vendorDraft.value.trim().toLowerCase(),
    )
  ) {
    addError.value = "This vendor already exists in the sample register.";
    return;
  }
  const id = `R-${101 + state.value.contracts.length}`;
  state.value.contracts.push({
    id,
    vendor: vendorDraft.value.trim(),
    category: "Software subscription",
    annualCost: Math.round(cost * 100) / 100,
    renewalDate: dateDraft.value,
    noticeDays: days,
    owner: "Maya Patel",
    acknowledged: false,
    decision: "undecided",
    reason: "",
    source: sourceDraft.value.trim(),
    history: [
      `${props.api.today} · manually registered; source requires owner verification`,
    ],
  });
  selectedId.value = id;
  view.value = "all";
  vendorDraft.value = "";
  costDraft.value = "";
  sourceDraft.value = "";
  addDialog.value?.close();
  props.api.toast(
    "Vendor registered locally. Dates have not been independently verified.",
  );
}
function exportDecisions(): void {
  props.api.download(
    "renewal-decisions.json",
    JSON.stringify(
      {
        synthetic: true,
        asOf: props.api.today,
        currency: "USD",
        contracts: state.value.contracts.map((contract) => ({
          ...contract,
          noticeDeadline: deadline(contract),
          daysToNotice: daysLeft(contract),
          externalSubscriptionChanged: false,
        })),
      },
      null,
      2,
    ),
    "application/json",
  );
}
</script>

<template>
  <section data-product="renewals">
    <header class="workspace-heading">
      <div>
        <p class="eyebrow">NOTICE / RENEWAL PLANNING</p>
        <h1 class="page-title">Decide before the window closes.</h1>
        <p class="page-description">
          Northline Studio · notice dates first, renewal dates second
        </p>
      </div>
      <div class="actions">
        <button class="btn secondary" @click="exportDecisions">
          Export decisions</button
        ><button
          class="btn primary"
          @click="
            addError = '';
            addDialog?.showModal();
          "
        >
          Add vendor
        </button>
      </div>
    </header>
    <div class="renewal-context">
      <span
        ><strong>{{ openContracts.length }}</strong> decisions open</span
      ><span
        ><strong>{{ api.money(actionValue) }}</strong> annual value with notice
        dates within 30 days or overdue</span
      ><span class="muted small"
        >As of {{ api.today }} · owner-supplied dates</span
      >
    </div>
    <div class="renewal-layout">
      <section class="deadline-agenda">
        <div class="agenda-heading">
          <h2>Notice windows</h2>
          <div class="tabs">
            <button
              class="tab"
              :class="{ active: view === 'open' }"
              :aria-pressed="view === 'open'"
              @click="view = 'open'"
            >
              Needs decision</button
            ><button
              class="tab"
              :class="{ active: view === 'all' }"
              :aria-pressed="view === 'all'"
              @click="view = 'all'"
            >
              All vendors
            </button>
          </div>
        </div>
        <div class="notice-timeline">
          <button
            v-for="contract in timeline"
            :key="contract.id"
            class="deadline-card"
            :class="{
              selected: selectedId === contract.id,
              overdue:
                daysLeft(contract) < 0 && contract.decision === 'undecided',
            }"
            :aria-pressed="selectedId === contract.id"
            @click="selectedId = contract.id"
          >
            <span class="date-stamp"
              ><span>{{
                new Date(`${deadline(contract)}T12:00:00Z`).toLocaleString(
                  "en-US",
                  { month: "short", timeZone: "UTC" },
                )
              }}</span
              ><strong>{{ deadline(contract).slice(8) }}</strong></span
            ><span class="deadline-content"
              ><span class="actions"
                ><strong>{{ contract.vendor }}</strong
                ><span
                  class="badge"
                  :class="
                    contract.decision !== 'undecided'
                      ? 'success'
                      : daysLeft(contract) < 0
                        ? 'danger'
                        : daysLeft(contract) <= 7
                          ? 'warning'
                          : 'neutral'
                  "
                  >{{
                    contract.decision === "undecided"
                      ? urgency(contract)
                      : `${contract.decision} intent`
                  }}</span
                ></span
              ><span class="small muted"
                >{{ contract.category }} ·
                {{ api.money(contract.annualCost) }}/year</span
              ><span class="small"
                >{{ contract.owner }} ·
                {{
                  contract.acknowledged
                    ? "acknowledged"
                    : "awaiting acknowledgment"
                }}</span
              ></span
            >
          </button>
          <div v-if="!timeline.length" class="empty-state">
            <h3>No undecided vendors</h3>
            <p>
              Recorded intentions remain available under All vendors. External
              actions still belong to the owner.
            </p>
          </div>
        </div>
      </section>
      <aside v-if="selected" class="panel decision-desk">
        <div class="panel-header">
          <div>
            <p class="eyebrow">DECISION FILE / {{ selected.id }}</p>
            <h2>{{ selected.vendor }}</h2>
            <p class="small muted">
              {{ selected.category }} ·
              {{ api.money(selected.annualCost) }} annual value
            </p>
          </div>
        </div>
        <div class="panel-body stack">
          <div class="date-comparison">
            <div>
              <span class="metric-label">Decide by</span
              ><strong>{{ deadline(selected) }}</strong
              ><span class="small"
                >{{ selected.noticeDays }} calendar-day notice</span
              >
            </div>
            <div>
              <span class="metric-label">Renews on</span
              ><strong>{{ selected.renewalDate }}</strong
              ><span class="small muted">Separate contractual date</span>
            </div>
          </div>
          <p v-if="daysLeft(selected) < 0" class="callout warning">
            The supplied notice date has passed. Recording cancellation intent
            cannot undo an automatic renewal. The owner must check the actual
            agreement and vendor response.
          </p>
          <p class="small muted">
            Source: {{ selected.source }}. These synthetic dates are manually
            supplied; date arithmetic does not interpret contract terms.
          </p>
          <section class="owner-block stack">
            <label class="field"
              >Decision owner<select v-model="ownerDraft" class="select">
                <option v-for="owner in owners" :key="owner">
                  {{ owner }}
                </option>
              </select></label
            >
            <div class="actions">
              <button class="btn secondary small" @click="assignOwner">
                Assign owner</button
              ><button
                v-if="!selected.acknowledged"
                class="btn secondary small"
                @click="acknowledge"
              >
                Simulate acknowledgment</button
              ><span v-else class="badge success">Owner acknowledged</span>
            </div>
            <p v-if="ownerError" role="alert" class="callout warning">
              {{ ownerError }}
            </p>
          </section>
          <div v-if="selected.decision !== 'undecided'" class="decision-record">
            <p class="eyebrow">RECORDED INTENT / {{ selected.decision }}</p>
            <p>{{ selected.reason }}</p>
            <p class="small muted">
              No vendor change has been made by this prototype.
            </p>
            <button class="btn ghost small" @click="reopenDecision">
              Reopen decision
            </button>
          </div>
          <button class="btn primary" @click="openDecision">
            {{
              selected.decision === "undecided"
                ? "Record renewal decision"
                : "Revise decision"
            }}
          </button>
          <details>
            <summary>Decision history ({{ selected.history.length }})</summary>
            <ol class="decision-history">
              <li v-for="(event, index) in selected.history" :key="index">
                {{ event }}
              </li>
            </ol>
          </details>
        </div>
      </aside>
    </div>
    <dialog
      ref="decisionDialog"
      class="modal"
      aria-labelledby="renewal-decision-title"
    >
      <form @submit.prevent="recordDecision">
        <div class="modal-header">
          <h2 id="renewal-decision-title">
            Decision for {{ selected?.vendor }}
          </h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close decision form"
            @click="decisionDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <fieldset class="decision-options">
            <legend>What should happen next?</legend>
            <label
              ><input
                v-model="decisionDraft"
                type="radio"
                value="renew"
                name="renewal-intent"
              /><span
                ><strong>Plan to renew</strong
                ><small>Keep the service for another term</small></span
              ></label
            ><label
              ><input
                v-model="decisionDraft"
                type="radio"
                value="cancel"
                name="renewal-intent"
              /><span
                ><strong>Plan to cancel</strong
                ><small
                  >Owner must complete the vendor’s cancellation process</small
                ></span
              ></label
            >
          </fieldset>
          <label class="field"
            >Reason and next step<textarea
              v-model="decisionReason"
              class="textarea"
              rows="4"
              placeholder="Usage reviewed; Maya will confirm the renewal amount with the vendor."
            ></textarea>
          </label>
          <p v-if="decisionError" role="alert" class="callout warning">
            {{ decisionError }}
          </p>
          <p class="small muted">
            Records an internal decision only. No cancellation, renewal, email
            or payment is executed.
          </p>
        </div>
        <div class="modal-footer">
          <button
            class="btn ghost"
            type="button"
            @click="decisionDialog?.close()"
          >
            Cancel</button
          ><button class="btn primary" type="submit">Save decision</button>
        </div>
      </form>
    </dialog>
    <dialog ref="addDialog" class="modal" aria-labelledby="renewal-add-title">
      <form @submit.prevent="addContract">
        <div class="modal-header">
          <h2 id="renewal-add-title">Add vendor notice window</h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close vendor form"
            @click="addDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <label class="field"
            >Vendor name<input
              v-model="vendorDraft"
              class="input"
              placeholder="Acme Software"
          /></label>
          <div class="form-grid">
            <label class="field"
              >Annual value (USD)<input
                v-model="costDraft"
                class="input"
                inputmode="decimal"
                placeholder="1200" /></label
            ><label class="field"
              >Renewal date<input v-model="dateDraft" class="input" type="date"
            /></label>
          </div>
          <label class="field"
            >Notice period in calendar days<input
              v-model="noticeDraft"
              class="input"
              inputmode="numeric" /></label
          ><label class="field"
            >Source reference<input
              v-model="sourceDraft"
              class="input"
              placeholder="Order form, section 7.1"
          /></label>
          <p v-if="addError" role="alert" class="callout warning">
            {{ addError }}
          </p>
          <p class="small muted">
            Owner defaults to Maya Patel. Check the actual notice rules before
            relying on a date.
          </p>
        </div>
        <div class="modal-footer">
          <button class="btn ghost" type="button" @click="addDialog?.close()">
            Cancel</button
          ><button class="btn primary" type="submit">Add notice window</button>
        </div>
      </form>
    </dialog>
  </section>
</template>
