<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

type CommitmentStatus = "Planned" | "In progress" | "Blocked" | "Delivered";
type Update = { date: string; text: string; status: CommitmentStatus };
type Commitment = {
  id: number;
  title: string;
  account: string;
  owner: string;
  due: string;
  ownerAccepted: boolean;
  status: CommitmentStatus;
  source: string;
  revision: number;
  updates: Update[];
};
type DigestItem = {
  id: number;
  title: string;
  account: string;
  owner: string;
  due: string;
  status: CommitmentStatus;
  revision: number;
  update: string;
};
type Digest = {
  id: number;
  date: string;
  account: string;
  signature: string;
  items: DigestItem[];
  approved: boolean;
};
const props = defineProps<{ api: PrototypeApi }>();
const state = ref(
  props.api.state<{ commitments: Commitment[]; digests: Digest[] }>({
    commitments: [
      {
        id: 1,
        title: "Deliver the account migration plan",
        account: "Northstar Labs",
        owner: "Alex Rivera",
        due: "2026-09-30",
        ownerAccepted: false,
        status: "Planned",
        source: "Renewal call · 24 September",
        revision: 1,
        updates: [
          {
            date: "2026-09-24",
            text: "Customer expects a migration plan before their October rollout.",
            status: "Planned",
          },
        ],
      },
      {
        id: 2,
        title: "Confirm export format compatibility",
        account: "Morrow Studio",
        owner: "Priya Shah",
        due: "2026-09-28",
        ownerAccepted: true,
        status: "Blocked",
        source: "Implementation workshop · 22 September",
        revision: 1,
        updates: [
          {
            date: "2026-09-26",
            text: "Waiting for one sample CSV from the implementation lead.",
            status: "Blocked",
          },
        ],
      },
      {
        id: 3,
        title: "Share the administrator onboarding guide",
        account: "Northstar Labs",
        owner: "Alex Rivera",
        due: "2026-10-02",
        ownerAccepted: true,
        status: "In progress",
        source: "Success check-in · 25 September",
        revision: 1,
        updates: [
          {
            date: "2026-09-28",
            text: "Draft guide is complete; screenshots need a final review.",
            status: "In progress",
          },
        ],
      },
      {
        id: 4,
        title: "Document the agreed support escalation path",
        account: "Lumen Works",
        owner: "Jordan Lee",
        due: "2026-09-27",
        ownerAccepted: true,
        status: "Delivered",
        source: "Account handover · 20 September",
        revision: 1,
        updates: [
          {
            date: "2026-09-27",
            text: "Escalation contacts and response expectations reviewed by the account team.",
            status: "Delivered",
          },
        ],
      },
    ],
    digests: [],
  }),
);
const selectedId = ref(1);
const accountFilter = ref("All accounts");
const digestAccount = ref("Northstar Labs");
const updateText = ref("");
const updateStatus = ref<CommitmentStatus>("In progress");
const updateError = ref("");
const addDialog = ref<HTMLDialogElement | null>(null);
const digestDialog = ref<HTMLDialogElement | null>(null);
const newTitle = ref("");
const newAccount = ref("Northstar Labs");
const newOwner = ref("Alex Rivera");
const newDue = ref("2026-10-06");
const newSource = ref("");
const addError = ref("");
const draftDigest = ref<Digest | null>(null);
const selected = computed(
  () =>
    state.value.commitments.find((item) => item.id === selectedId.value) ??
    state.value.commitments[0]!,
);
const accounts = computed(() => [
  ...new Set(state.value.commitments.map((item) => item.account)),
]);
const visible = computed(() =>
  state.value.commitments
    .filter(
      (item) =>
        accountFilter.value === "All accounts" ||
        item.account === accountFilter.value,
    )
    .sort((a, b) => a.due.localeCompare(b.due)),
);
const active = computed(() =>
  state.value.commitments.filter((item) => item.status !== "Delivered"),
);
const overdue = computed(
  () => active.value.filter((item) => item.due < props.api.today).length,
);
const unconfirmed = computed(
  () => active.value.filter((item) => !item.ownerAccepted).length,
);
const delivered = computed(
  () =>
    state.value.commitments.filter((item) => item.status === "Delivered")
      .length,
);
const digestItems = computed(() =>
  state.value.commitments
    .filter(
      (item) => item.account === digestAccount.value && item.ownerAccepted,
    )
    .sort((a, b) => a.due.localeCompare(b.due)),
);
const digestSignature = computed(() =>
  JSON.stringify([
    digestAccount.value,
    ...digestItems.value.map((item) => [item.id, item.revision]),
  ]),
);
const latestDigest = computed(() =>
  state.value.digests
    .filter((item) => item.account === digestAccount.value)
    .at(-1),
);
const draftStale = computed(() =>
  Boolean(
    draftDigest.value &&
    (draftDigest.value.account !== digestAccount.value ||
      draftDigest.value.signature !== digestSignature.value ||
      draftDigest.value.items.some(
        (item) => item.account !== digestAccount.value,
      )),
  ),
);
const digestExportable = computed(() =>
  Boolean(
    draftDigest.value &&
    !draftStale.value &&
    draftDigest.value.items.length > 0,
  ),
);
watch(state, (value) => props.api.save(value), { deep: true });
watch(
  digestAccount,
  () => {
    draftDigest.value = null;
  },
  { flush: "sync" },
);
watch(
  selected,
  (item) => {
    updateStatus.value =
      item.status === "Planned" ? "In progress" : item.status;
    updateText.value = "";
    updateError.value = "";
  },
  { immediate: true },
);

function inputValue(event: Event): string {
  return (event.target as HTMLInputElement).value;
}
function statusClass(status: CommitmentStatus): string {
  return status === "Delivered"
    ? "success"
    : status === "Blocked"
      ? "danger"
      : status === "In progress"
        ? "info"
        : "neutral";
}
function acceptOwner(): void {
  selected.value.ownerAccepted = true;
  selected.value.revision++;
  props.api.toast(
    "Owner confirmation recorded locally for the sample commitment.",
  );
}
function recordUpdate(event: Event): void {
  event.preventDefault();
  if (updateText.value.trim().length < 10) {
    updateError.value =
      "Write a useful customer-safe update of at least 10 characters.";
    return;
  }
  if (updateStatus.value === "Delivered" && !selected.value.ownerAccepted) {
    updateError.value =
      "Confirm the owner before marking this commitment delivered.";
    return;
  }
  selected.value.status = updateStatus.value;
  selected.value.revision++;
  selected.value.updates.push({
    date: props.api.today,
    text: updateText.value.trim(),
    status: updateStatus.value,
  });
  updateText.value = "";
  updateError.value = "";
  props.api.toast(
    "Update saved internally. Preview a new digest before sharing.",
  );
}
function setStatus(event: Event): void {
  updateStatus.value = inputValue(event) as CommitmentStatus;
}
function openNew(): void {
  newTitle.value = "";
  newSource.value = "";
  addError.value = "";
  addDialog.value?.showModal();
}
function addCommitment(event: Event): void {
  event.preventDefault();
  if (
    newTitle.value.trim().length < 8 ||
    newSource.value.trim().length < 5 ||
    !/^\d{4}-\d{2}-\d{2}$/.test(newDue.value) ||
    !Number.isFinite(Date.parse(newDue.value))
  ) {
    addError.value =
      "Add a clear promise, a valid due date, and the conversation that established it.";
    return;
  }
  if (
    state.value.commitments.some(
      (item) =>
        item.title.toLowerCase() === newTitle.value.trim().toLowerCase() &&
        item.account === newAccount.value,
    )
  ) {
    addError.value =
      "That account already has this promise. Update its existing record.";
    return;
  }
  const id = Math.max(...state.value.commitments.map((item) => item.id)) + 1;
  state.value.commitments.push({
    id,
    title: newTitle.value.trim(),
    account: newAccount.value,
    owner: newOwner.value,
    due: newDue.value,
    ownerAccepted: false,
    status: "Planned",
    source: newSource.value.trim(),
    revision: 1,
    updates: [
      {
        date: props.api.today,
        text: "Promise captured; awaiting named owner confirmation.",
        status: "Planned",
      },
    ],
  });
  accountFilter.value = "All accounts";
  selectedId.value = id;
  addDialog.value?.close();
  props.api.toast("Promise captured. The owner still needs to confirm it.");
}
function previewDigest(): void {
  if (!accounts.value.includes(digestAccount.value)) {
    props.api.toast(
      "Choose one valid account before preparing a digest.",
      "warning",
    );
    return;
  }
  draftDigest.value = {
    id: state.value.digests.length + 1,
    date: props.api.today,
    account: digestAccount.value,
    signature: digestSignature.value,
    approved: false,
    items: digestItems.value.map((item) => ({
      id: item.id,
      title: item.title,
      account: item.account,
      owner: item.owner,
      due: item.due,
      status: item.status,
      revision: item.revision,
      update: item.updates.at(-1)?.text ?? "",
    })),
  };
  if (!digestDialog.value?.open) digestDialog.value?.showModal();
}
function approveDigest(): void {
  if (
    !draftDigest.value ||
    draftDigest.value.approved ||
    !digestExportable.value
  )
    return;
  draftDigest.value.approved = true;
  state.value.digests.push(
    JSON.parse(JSON.stringify(draftDigest.value)) as Digest,
  );
  props.api.toast("Digest approved locally. No customer message was sent.");
}
function exportLedger(): void {
  props.api.download(
    "customer-commitments.json",
    JSON.stringify(
      {
        synthetic: true,
        scope:
          "Internal full ledger; may contain multiple accounts. Not a client digest.",
        date: props.api.today,
        ...state.value,
      },
      null,
      2,
    ),
    "application/json",
  );
}
function exportDigest(): void {
  if (!draftDigest.value || !digestExportable.value) return;
  const lines = [
    "CUSTOMER COMMITMENTS — SYNTHETIC PREVIEW",
    `Account: ${draftDigest.value.account}`,
    `Prepared ${draftDigest.value.date}`,
    `Status: ${draftDigest.value.approved ? "Approved locally; not sent" : "Draft; not approved"}`,
    ...draftDigest.value.items.map(
      (item) =>
        `\n${item.account}\n${item.title}\nOwner: ${item.owner} | Due: ${item.due} | ${item.status}\n${item.update}`,
    ),
  ];
  const accountSlug = draftDigest.value.account
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
  props.api.download(`client-digest-${accountSlug}.txt`, lines.join("\n"));
}
</script>

<template>
  <div data-product="promises">
    <header class="workspace-heading">
      <div>
        <p class="eyebrow">Kept · customer commitments</p>
        <h1 class="page-title">A promise deserves an owner.</h1>
        <p class="page-description">
          Keep the words from a customer conversation connected to the work that
          follows.
        </p>
      </div>
      <div class="actions">
        <button class="btn secondary" @click="exportLedger">
          Export commitments</button
        ><button class="btn primary" @click="openNew">Capture a promise</button>
      </div>
    </header>
    <div class="metrics">
      <div class="metric">
        <span class="metric-label">Active commitments</span
        ><strong class="metric-value">{{ active.length }}</strong
        ><span class="metric-note">Across {{ accounts.length }} accounts</span>
      </div>
      <div class="metric">
        <span class="metric-label">Past due</span
        ><strong class="metric-value promises-danger">{{ overdue }}</strong
        ><span class="metric-note">Needs an honest update</span>
      </div>
      <div class="metric">
        <span class="metric-label">Awaiting an owner</span
        ><strong class="metric-value">{{ unconfirmed }}</strong
        ><span class="metric-note">Excluded from client digests</span>
      </div>
      <div class="metric">
        <span class="metric-label">Delivered</span
        ><strong class="metric-value">{{ delivered }}</strong
        ><span class="metric-note">Evidence remains in the ledger</span>
      </div>
    </div>
    <div class="promises-layout">
      <section class="panel promises-timeline">
        <div class="panel-header">
          <div>
            <h2>Commitment timeline</h2>
            <p class="small muted">
              Customer-specific agreements, in due-date order.
            </p>
          </div>
          <label class="field"
            ><span class="visually-hidden">Filter account</span
            ><select
              class="select"
              :value="accountFilter"
              @change="accountFilter = inputValue($event)"
            >
              <option>All accounts</option>
              <option v-for="account in accounts" :key="account">
                {{ account }}
              </option>
            </select></label
          >
        </div>
        <div class="promises-rows">
          <button
            v-for="item in visible"
            :key="item.id"
            class="promises-row"
            :class="{ selected: selected.id === item.id }"
            @click="selectedId = item.id"
          >
            <span class="promises-date"
              ><strong>{{ item.due.slice(8) }}</strong
              ><span>{{
                item.due.slice(5, 7) === "09"
                  ? "SEP"
                  : item.due.slice(5, 7) === "10"
                    ? "OCT"
                    : item.due.slice(5, 7)
              }}</span></span
            ><span class="promises-row-copy"
              ><span class="eyebrow">{{ item.account }}</span
              ><strong>{{ item.title }}</strong
              ><span class="small muted"
                >{{ item.owner }} ·
                {{
                  item.ownerAccepted
                    ? "Owner confirmed"
                    : "Owner confirmation needed"
                }}</span
              ></span
            ><span class="badge" :class="statusClass(item.status)">{{
              item.status
            }}</span>
          </button>
        </div>
        <div v-if="visible.length === 0" class="empty-state">
          No commitments match this account.
        </div>
      </section>
      <aside class="stack">
        <section class="panel promises-detail">
          <div class="panel-header">
            <div>
              <p class="eyebrow">
                {{ selected.account }} · commitment {{ selected.id }}
              </p>
              <h2>{{ selected.title }}</h2>
            </div>
          </div>
          <div class="panel-body stack">
            <div class="promises-ownership">
              <div class="avatar">
                {{
                  selected.owner
                    .split(" ")
                    .map((word) => word[0])
                    .join("")
                }}
              </div>
              <div>
                <strong>{{ selected.owner }}</strong>
                <p class="small muted">Due {{ selected.due }}</p>
              </div>
              <span
                class="badge"
                :class="selected.ownerAccepted ? 'success' : 'warning'"
                >{{
                  selected.ownerAccepted ? "Confirmed" : "Unconfirmed"
                }}</span
              >
            </div>
            <button
              v-if="!selected.ownerAccepted"
              class="btn secondary"
              @click="acceptOwner"
            >
              Confirm owner · simulated
            </button>
            <div class="promises-origin">
              <span class="eyebrow">Where this promise came from</span>
              <p>{{ selected.source }}</p>
            </div>
            <div class="stack">
              <h3>Updates</h3>
              <article
                v-for="(update, index) in selected.updates"
                :key="index"
                class="promises-update"
              >
                <span class="small muted"
                  >{{ update.date }} · {{ update.status }}</span
                >
                <p>{{ update.text }}</p>
              </article>
            </div>
            <form class="stack" novalidate @submit="recordUpdate">
              <label class="field"
                >Current status<select
                  class="select"
                  :value="updateStatus"
                  @change="setStatus"
                >
                  <option>Planned</option>
                  <option>In progress</option>
                  <option>Blocked</option>
                  <option>Delivered</option>
                </select></label
              ><label class="field"
                >Customer-safe update<textarea
                  class="textarea"
                  rows="3"
                  :value="updateText"
                  :aria-invalid="Boolean(updateError)"
                  aria-describedby="promises-update-error"
                  placeholder="What changed, and what happens next?"
                  @input="updateText = inputValue($event)"
                ></textarea>
              </label>
              <p
                v-if="updateError"
                id="promises-update-error"
                class="promises-error"
                role="alert"
              >
                {{ updateError }}
              </p>
              <button type="submit" class="btn primary">Record update</button>
              <p class="small muted">
                Updates stay internal until a human approves a digest.
              </p>
            </form>
          </div>
        </section>
        <section class="panel">
          <div class="panel-body stack">
            <p class="eyebrow">Client communication</p>
            <h2>One clear, reviewed update.</h2>
            <p class="muted">
              Prepare one account’s confirmed commitments. The ledger filter
              does not change the digest recipient.
            </p>
            <label class="field"
              >Digest account<select
                class="select"
                :value="digestAccount"
                @change="digestAccount = inputValue($event)"
              >
                <option v-for="account in accounts" :key="account">
                  {{ account }}
                </option>
              </select></label
            ><button class="btn secondary" @click="previewDigest">
              Preview client digest</button
            ><span v-if="latestDigest" class="small muted"
              >{{ latestDigest.account }} · digest
              {{ latestDigest.id }} approved locally · {{ latestDigest.date }} ·
              never sent</span
            >
          </div>
        </section>
      </aside>
    </div>
    <dialog ref="addDialog" class="modal" aria-labelledby="promise-new-title">
      <form novalidate @submit="addCommitment">
        <div class="modal-header">
          <h2 id="promise-new-title">Capture a customer promise</h2>
          <button
            class="icon-button"
            type="button"
            aria-label="Close promise form"
            @click="addDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <label class="field"
            >What was promised?<input
              class="input"
              :value="newTitle"
              placeholder="Deliver the security review summary"
              @input="newTitle = inputValue($event)"
          /></label>
          <div class="form-grid">
            <label class="field"
              >Account<select
                class="select"
                :value="newAccount"
                @change="newAccount = inputValue($event)"
              >
                <option v-for="account in accounts" :key="account">
                  {{ account }}
                </option>
              </select></label
            ><label class="field"
              >Owner<select
                class="select"
                :value="newOwner"
                @change="newOwner = inputValue($event)"
              >
                <option>Alex Rivera</option>
                <option>Priya Shah</option>
                <option>Jordan Lee</option>
              </select></label
            >
          </div>
          <label class="field"
            >Due date<input
              class="input"
              type="date"
              :value="newDue"
              @input="newDue = inputValue($event)" /></label
          ><label class="field"
            >Source conversation<input
              class="input"
              :value="newSource"
              placeholder="Customer call · 29 September"
              @input="newSource = inputValue($event)"
          /></label>
          <p v-if="addError" class="promises-error" role="alert">
            {{ addError }}
          </p>
          <p class="small muted">
            A request becomes a commitment when its owner accepts
            responsibility.
          </p>
        </div>
        <div class="modal-footer">
          <button
            class="btn secondary"
            type="button"
            @click="addDialog?.close()"
          >
            Cancel</button
          ><button class="btn primary" type="submit">Save commitment</button>
        </div>
      </form>
    </dialog>
    <dialog
      ref="digestDialog"
      class="modal"
      aria-labelledby="promise-digest-title"
    >
      <div class="modal-header">
        <h2 id="promise-digest-title">Client digest preview</h2>
        <button
          class="icon-button"
          aria-label="Close digest preview"
          @click="digestDialog?.close()"
        >
          ×
        </button>
      </div>
      <div class="modal-body stack">
        <label class="field"
          >Digest account<select
            class="select"
            :value="digestAccount"
            @change="digestAccount = inputValue($event)"
          >
            <option v-for="account in accounts" :key="account">
              {{ account }}
            </option>
          </select></label
        ><template v-if="draftDigest"
          ><div class="callout info">
            <strong>{{ draftDigest.account }}</strong> ·
            {{
              draftDigest.approved
                ? "Approved in this prototype. No message has been sent."
                : "Draft for human approval. Unconfirmed commitments are excluded."
            }}
          </div>
          <article
            v-for="item in draftDigest.items"
            :key="item.id"
            class="promises-digest-item"
          >
            <p class="eyebrow">{{ item.account }}</p>
            <h3>{{ item.title }}</h3>
            <p>{{ item.update }}</p>
            <p class="small muted">
              {{ item.status }} · {{ item.owner }} · due {{ item.due }}
            </p>
          </article>
          <div v-if="draftDigest.items.length === 0" class="empty-state">
            This account has no confirmed commitments. Confirm an owner before
            preparing its digest.
          </div>
          <p v-if="draftStale" class="promises-error" role="alert">
            The account’s commitments changed. Refresh the digest before
            approval or export.
          </p></template
        >
        <div v-else class="callout warning" role="status">
          Account changed. The previous draft was cleared. Refresh the digest
          for {{ digestAccount }}.
        </div>
        <button
          v-if="!draftDigest || draftStale"
          class="btn secondary"
          @click="previewDigest"
        >
          Refresh digest
        </button>
      </div>
      <div class="modal-footer">
        <button
          class="btn secondary"
          :disabled="!digestExportable"
          @click="exportDigest"
        >
          Export digest</button
        ><button
          class="btn primary"
          :disabled="!digestExportable || draftDigest?.approved"
          @click="approveDigest"
        >
          {{
            draftDigest?.approved
              ? "Approved locally"
              : "Approve digest · simulated"
          }}
        </button>
      </div>
    </dialog>
  </div>
</template>
