<script setup lang="ts">
import { computed, ref, useTemplateRef, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

const props = defineProps<{ api: PrototypeApi }>();

interface Feed {
  id: string;
  name: string;
  partner: string;
  due: number;
  grace: number;
  prefix: string;
}
interface Receipt {
  feedId: string;
  date: string;
  filename: string;
  rows: number;
  minute: number;
}
interface Exception {
  feedId: string;
  date: string;
  reason: string;
}
type FeedStatus = "received" | "late" | "grace" | "expected" | "excused";

const feeds: Feed[] = [
  {
    id: "ledger",
    name: "Settlement ledger",
    partner: "Northstar Payments",
    due: 540,
    grace: 30,
    prefix: "settlement",
  },
  {
    id: "returns",
    name: "Return adjustments",
    partner: "Fieldwork Commerce",
    due: 600,
    grace: 30,
    prefix: "returns",
  },
  {
    id: "inventory",
    name: "Warehouse availability",
    partner: "Morrow Supply",
    due: 660,
    grace: 30,
    prefix: "inventory",
  },
  {
    id: "orders",
    name: "Wholesale orders",
    partner: "Juniper Trade",
    due: 720,
    grace: 60,
    prefix: "orders",
  },
  {
    id: "prices",
    name: "Regional price book",
    partner: "Atlas Distribution",
    due: 840,
    grace: 30,
    prefix: "prices",
  },
];
const days = [
  { date: "2026-09-29", weekday: "Tue", day: "29", month: "Sep" },
  { date: "2026-09-30", weekday: "Wed", day: "30", month: "Sep" },
  { date: "2026-10-01", weekday: "Thu", day: "01", month: "Oct" },
  { date: "2026-10-02", weekday: "Fri", day: "02", month: "Oct" },
  { date: "2026-10-03", weekday: "Sat", day: "03", month: "Oct" },
];
const receiptDialog = useTemplateRef<HTMLDialogElement>("receiptDialog");
const exceptionDialog = useTemplateRef<HTMLDialogElement>("exceptionDialog");
const state = ref(
  props.api.state({
    minute: 750,
    receipts: [
      {
        feedId: "ledger",
        date: "2026-09-29",
        filename: "settlement_2026-09-29.csv",
        rows: 2418,
        minute: 537,
      },
      {
        feedId: "returns",
        date: "2026-09-29",
        filename: "returns_2026-09-29.csv",
        rows: 82,
        minute: 604,
      },
    ] as Receipt[],
    exceptions: [
      {
        feedId: "prices",
        date: "2026-10-01",
        reason: "Partner inventory count: no price feed expected.",
      },
    ] as Exception[],
  }),
);
const selectedDate = ref(props.api.today);
const selectedFeedId = ref("inventory");
const receiptFilename = ref("");
const receiptRows = ref("");
const exceptionDate = ref(props.api.today);
const exceptionReason = ref("");
const formError = ref("");

const selected = computed(() =>
  feeds.find((feed) => feed.id === selectedFeedId.value),
);
const selectedReceipt = computed(() =>
  state.value.receipts.find(
    (receipt) =>
      receipt.feedId === selectedFeedId.value &&
      receipt.date === selectedDate.value,
  ),
);
const selectedException = computed(() =>
  state.value.exceptions.find(
    (exception) =>
      exception.feedId === selectedFeedId.value &&
      exception.date === selectedDate.value,
  ),
);
const dailyFeeds = computed(() =>
  feeds.map((feed) => ({ feed, status: getStatus(feed, selectedDate.value) })),
);
const receivedCount = computed(
  () => dailyFeeds.value.filter((item) => item.status === "received").length,
);
const lateCount = computed(
  () => dailyFeeds.value.filter((item) => item.status === "late").length,
);
const expectedCount = computed(
  () => dailyFeeds.value.filter((item) => item.status !== "excused").length,
);
const waitingCount = computed(
  () =>
    dailyFeeds.value.filter(
      (item) => item.status === "expected" || item.status === "grace",
    ).length,
);

watch(state, (value) => props.api.save(value), { deep: true });

function time(minute: number) {
  return `${Math.floor(minute / 60)
    .toString()
    .padStart(2, "0")}:${(minute % 60).toString().padStart(2, "0")}`;
}

function getStatus(feed: Feed, date: string): FeedStatus {
  if (
    state.value.exceptions.some(
      (item) => item.feedId === feed.id && item.date === date,
    )
  )
    return "excused";
  if (
    state.value.receipts.some(
      (item) => item.feedId === feed.id && item.date === date,
    )
  )
    return "received";
  if (date > props.api.today || state.value.minute < feed.due)
    return "expected";
  return state.value.minute <= feed.due + feed.grace ? "grace" : "late";
}

function statusLabel(status: FeedStatus) {
  return {
    received: "Received",
    late: "Late",
    grace: "Within grace",
    expected: "Expected",
    excused: "Calendar exception",
  }[status];
}

function statusClass(status: FeedStatus) {
  return {
    received: "success",
    late: "danger",
    grace: "warning",
    expected: "neutral",
    excused: "info",
  }[status];
}

function openReceipt() {
  if (!selected.value) return;
  receiptFilename.value = `${selected.value.prefix}_${selectedDate.value}.csv`;
  receiptRows.value = "";
  formError.value = "";
  receiptDialog.value?.showModal();
}

function recordReceipt() {
  if (!selected.value) return;
  const rows = Number(receiptRows.value);
  const expected = `${selected.value.prefix}_${selectedDate.value}.csv`;
  if (
    receiptFilename.value.trim() !== expected ||
    !Number.isSafeInteger(rows) ||
    rows <= 0
  ) {
    formError.value = `Use ${expected} and a positive whole row count.`;
    return;
  }
  if (selectedReceipt.value || selectedException.value) {
    formError.value =
      "This occurrence already has a receipt or calendar exception. Review it first.";
    return;
  }
  state.value.receipts.push({
    feedId: selected.value.id,
    date: selectedDate.value,
    filename: expected,
    rows,
    minute: state.value.minute,
  });
  receiptDialog.value?.close();
  props.api.toast("Receipt simulated locally. No file was uploaded.");
}

function openException() {
  exceptionDate.value = selectedDate.value;
  exceptionReason.value = "";
  formError.value = "";
  exceptionDialog.value?.showModal();
}

function saveException() {
  const reason = exceptionReason.value.trim();
  if (
    !days.some((day) => day.date === exceptionDate.value) ||
    reason.length < 8
  ) {
    formError.value =
      "Choose a displayed calendar date and provide at least 8 characters of context.";
    return;
  }
  const occurrence = (item: Receipt | Exception) =>
    item.feedId === selectedFeedId.value && item.date === exceptionDate.value;
  if (
    state.value.receipts.some(occurrence) ||
    state.value.exceptions.some(occurrence)
  ) {
    formError.value =
      "This occurrence already has a receipt or exception. Choose another date.";
    return;
  }
  state.value.exceptions.push({
    feedId: selectedFeedId.value,
    date: exceptionDate.value,
    reason,
  });
  selectedDate.value = exceptionDate.value;
  exceptionDialog.value?.close();
  props.api.toast(
    "Calendar exception saved locally. This occurrence no longer expects a file.",
  );
}

function removeException() {
  state.value.exceptions = state.value.exceptions.filter(
    (item) =>
      !(
        item.feedId === selectedFeedId.value && item.date === selectedDate.value
      ),
  );
  props.api.toast("Exception removed. The expected arrival is restored.");
}

function advanceClock() {
  state.value.minute = Math.min(1080, state.value.minute + 30);
  props.api.toast(
    `Simulation clock advanced to ${time(state.value.minute)} UTC. No alerts sent.`,
    "info",
  );
}

function exportCalendar() {
  props.api.download(
    "arrival-calendar.json",
    JSON.stringify(
      {
        prototype: true,
        timezone: "UTC",
        today: props.api.today,
        simulationMinute: state.value.minute,
        feeds,
        receipts: state.value.receipts,
        exceptions: state.value.exceptions,
        selectedDay: {
          date: selectedDate.value,
          expected: expectedCount.value,
          received: receivedCount.value,
          late: lateCount.value,
        },
      },
      null,
      2,
    ),
    "application/json",
  );
  props.api.toast("Local arrival calendar exported.");
}
</script>

<template>
  <section data-product="files">
    <header class="workspace-heading">
      <div>
        <div class="eyebrow">Arrival / partner file calendar</div>
        <h1 class="page-title">Know what should have arrived.</h1>
        <p class="page-description">
          A quiet watch over your partner feeds, with room for real-world
          calendars.
        </p>
      </div>
      <button class="btn secondary" @click="exportCalendar">
        Export arrival calendar
      </button>
    </header>

    <div class="files-clock panel">
      <div>
        <span class="eyebrow">Simulation clock · Sep 29</span>
        <strong class="mono"
          >{{ time(state.minute) }} <span class="small muted">UTC</span></strong
        >
      </div>
      <div class="actions">
        <span class="small muted">Nothing is polling your systems.</span>
        <button
          class="btn secondary small"
          :disabled="state.minute >= 1080"
          @click="advanceClock"
        >
          Advance 30 minutes
        </button>
      </div>
    </div>

    <nav class="files-days" aria-label="Arrival dates">
      <button
        v-for="day in days"
        :key="day.date"
        class="files-day"
        :class="{ selected: selectedDate === day.date }"
        :aria-pressed="selectedDate === day.date"
        :aria-label="`${day.weekday} ${day.month} ${day.day}`"
        @click="selectedDate = day.date"
      >
        <span class="small">{{ day.weekday }}</span
        ><strong>{{ day.day }}</strong>
        <span class="small">{{ day.month }}</span>
        <span class="files-date-note"
          >{{
            state.exceptions.filter((item) => item.date === day.date).length
          }}
          exceptions</span
        >
      </button>
    </nav>

    <div class="metrics">
      <div class="metric">
        <div class="metric-label">Received / expected</div>
        <div class="metric-value">
          {{ receivedCount }} / {{ expectedCount }}
        </div>
        <div class="metric-note">For {{ selectedDate }}</div>
      </div>
      <div class="metric">
        <div class="metric-label">Past grace period</div>
        <div class="metric-value">{{ lateCount }}</div>
        <div class="metric-note">Needs operator attention</div>
      </div>
      <div class="metric">
        <div class="metric-label">Still waiting</div>
        <div class="metric-value">{{ waitingCount }}</div>
        <div class="metric-note">Upcoming or within grace</div>
      </div>
    </div>

    <div class="files-workspace">
      <section class="panel">
        <div class="panel-header">
          <h2>Expected arrivals</h2>
          <span class="badge neutral">UTC calendar</span>
        </div>
        <div class="files-timeline">
          <button
            v-for="item in dailyFeeds"
            :key="item.feed.id"
            class="files-arrival"
            :class="{ selected: selectedFeedId === item.feed.id }"
            :aria-pressed="selectedFeedId === item.feed.id"
            @click="selectedFeedId = item.feed.id"
          >
            <span class="files-time mono">{{ time(item.feed.due) }}</span>
            <span class="files-rail" aria-hidden="true"><span></span></span>
            <span class="files-arrival-body"
              ><strong>{{ item.feed.name }}</strong>
              <span class="small muted"
                >{{ item.feed.partner }} · {{ item.feed.grace }} min grace</span
              >
              <span class="badge" :class="statusClass(item.status)">{{
                statusLabel(item.status)
              }}</span></span
            >
          </button>
        </div>
      </section>

      <aside v-if="selected" class="panel files-detail">
        <div class="panel-header">
          <div>
            <div class="eyebrow">Feed detail</div>
            <h2>{{ selected.name }}</h2>
          </div>
        </div>
        <div class="panel-body stack">
          <span
            class="badge"
            :class="statusClass(getStatus(selected, selectedDate))"
          >
            {{ statusLabel(getStatus(selected, selectedDate)) }}</span
          >
          <dl class="files-facts">
            <div>
              <dt>Partner</dt>
              <dd>{{ selected.partner }}</dd>
            </div>
            <div>
              <dt>Expected by</dt>
              <dd class="mono">{{ time(selected.due) }} UTC</dd>
            </div>
            <div>
              <dt>Escalates after</dt>
              <dd class="mono">
                {{ time(selected.due + selected.grace) }} UTC
              </dd>
            </div>
            <div>
              <dt>Filename rule</dt>
              <dd class="mono">{{ selected.prefix }}_YYYY-MM-DD.csv</dd>
            </div>
          </dl>
          <div v-if="selectedReceipt" class="callout success">
            <strong>Receipt recorded</strong>
            <p class="small mono">{{ selectedReceipt.filename }}</p>
            <p class="small">
              {{ selectedReceipt.rows.toLocaleString() }} rows ·
              {{ time(selectedReceipt.minute) }} UTC
            </p>
            <p class="small">
              {{
                selectedReceipt.minute > selected.due + selected.grace
                  ? "Arrived after grace."
                  : "Arrived within the allowed window."
              }}
            </p>
          </div>
          <div v-else-if="selectedException" class="callout info">
            <strong>No file expected</strong>
            <p class="small">{{ selectedException.reason }}</p>
            <button class="btn secondary small" @click="removeException">
              Remove exception
            </button>
          </div>
          <div
            v-else-if="getStatus(selected, selectedDate) === 'late'"
            class="callout warning"
          >
            <strong>The expected file is late.</strong>
            <p class="small">
              Check with the partner or record a confirmed calendar exception.
            </p>
          </div>
          <div v-else class="callout info">
            <strong>Waiting quietly.</strong>
            <p class="small">
              An expected file becomes late only after its grace period.
            </p>
          </div>
          <button
            class="btn primary"
            :disabled="Boolean(selectedReceipt || selectedException)"
            @click="openReceipt"
          >
            Simulate file receipt
          </button>
          <button class="btn secondary" @click="openException">
            Add calendar exception
          </button>
          <p class="small muted">
            Your collector would send filename and row count. The file stays in
            your environment.
          </p>
        </div>
      </aside>
    </div>

    <dialog
      ref="receiptDialog"
      class="modal"
      aria-labelledby="files-receipt-title"
    >
      <form @submit.prevent="recordReceipt">
        <div class="modal-header">
          <h2 id="files-receipt-title">Simulate a file receipt</h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close receipt"
            @click="receiptDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p class="small muted">
            {{ selected?.name }} · {{ selectedDate }} · metadata only
          </p>
          <label class="field"
            >Filename<input
              v-model="receiptFilename"
              class="input"
              spellcheck="false"
          /></label>
          <label class="field"
            >Row count<input
              v-model="receiptRows"
              class="input"
              inputmode="numeric"
              placeholder="e.g. 1248"
          /></label>
          <p v-if="formError" class="callout warning" role="alert">
            {{ formError }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn secondary"
            @click="receiptDialog?.close()"
          >
            Cancel
          </button>
          <button class="btn primary">Record simulated receipt</button>
        </div>
      </form>
    </dialog>

    <dialog
      ref="exceptionDialog"
      class="modal"
      aria-labelledby="files-exception-title"
    >
      <form @submit.prevent="saveException">
        <div class="modal-header">
          <h2 id="files-exception-title">Calendar exception</h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close exception"
            @click="exceptionDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p class="small muted">
            Skip one expected arrival for {{ selected?.name }}.
          </p>
          <label class="field"
            >Date<select v-model="exceptionDate" class="select">
              <option v-for="day in days" :key="day.date" :value="day.date">
                {{ day.date }}
              </option>
            </select></label
          >
          <label class="field"
            >Partner-confirmed reason<textarea
              v-model="exceptionReason"
              class="textarea"
              rows="3"
              placeholder="Explain why no file is expected on this date."
            ></textarea>
          </label>
          <p v-if="formError" class="callout warning" role="alert">
            {{ formError }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn secondary"
            @click="exceptionDialog?.close()"
          >
            Cancel
          </button>
          <button class="btn primary">Save calendar exception</button>
        </div>
      </form>
    </dialog>
  </section>
</template>
