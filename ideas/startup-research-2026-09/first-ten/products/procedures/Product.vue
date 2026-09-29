<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

type ReviewStatus = "due" | "reviewing" | "verified";
interface Procedure {
  id: string;
  title: string;
  owner: string;
  team: string;
  source: string;
  version: number;
  body: string;
  due: string;
  status: ReviewStatus;
  history: string[];
}
interface ReviewState {
  procedures: Procedure[];
}
const props = defineProps<{ api: PrototypeApi }>();
const state = ref(
  props.api.state<ReviewState>({
    procedures: [
      {
        id: "P-101",
        title: "Client launch handoff",
        owner: "Maya Patel",
        team: "Client operations",
        source: "https://example.com/wiki/client-launch",
        version: 3,
        body: "1. Confirm the delivery owner and support contact.\n2. Check the client has access to the final files.\n3. Record open questions in the handoff register.\n4. Schedule the first service review.",
        due: "2026-09-25",
        status: "due",
        history: ["2026-08-25 · Maya Patel · v3 reviewed"],
      },
      {
        id: "P-102",
        title: "Refund exception review",
        owner: "Jonas Reed",
        team: "Finance operations",
        source: "https://example.com/wiki/refund-review",
        version: 2,
        body: "1. Record the original invoice reference.\n2. Capture the requested exception and supporting evidence.\n3. Obtain the finance owner’s approval.\n4. Confirm the final outcome with the account owner.",
        due: "2026-09-29",
        status: "reviewing",
        history: ["2026-09-28 · Jonas Reed · review started"],
      },
      {
        id: "P-103",
        title: "New contractor access",
        owner: "Leah Okafor",
        team: "People operations",
        source: "https://example.com/wiki/contractor-access",
        version: 4,
        body: "1. Confirm the internal sponsor.\n2. List required systems and access expiry dates.\n3. Record who approved each access request.\n4. Confirm the contractor knows how to report an issue.",
        due: "2026-10-22",
        status: "verified",
        history: ["2026-09-22 · Leah Okafor · v4 verified until 2026-10-22"],
      },
      {
        id: "P-104",
        title: "Weekly service handover",
        owner: "Maya Patel",
        team: "Client operations",
        source: "https://example.com/wiki/service-handover",
        version: 1,
        body: "1. List unresolved client commitments.\n2. Confirm a next owner for each commitment.\n3. Note coverage gaps and agreed fallback contacts.",
        due: "2026-09-28",
        status: "due",
        history: ["2026-08-28 · Maya Patel · v1 reviewed"],
      },
    ],
  }),
);
const selectedId = ref("P-101");
const activeStatus = ref<ReviewStatus | "all">("all");
const sourceChecked = ref(false);
const stepsChecked = ref(false);
const attestation = ref("");
const error = ref("");
const editing = ref(false);
const revisedBody = ref("");
const revisionReason = ref("");
const addDialog = ref<HTMLDialogElement | null>(null);
const newTitle = ref("");
const newOwner = ref("Maya Patel");
const newSource = ref("");
const newError = ref("");
const columns: { key: ReviewStatus; label: string; help: string }[] = [
  { key: "due", label: "Review due", help: "A fresh pair of eyes" },
  { key: "reviewing", label: "In review", help: "Check, revise, then attest" },
  { key: "verified", label: "Current", help: "A dated human decision" },
];
const selected = computed(() =>
  state.value.procedures.find((item) => item.id === selectedId.value),
);
const visibleColumns = computed(() =>
  columns.filter(
    (column) =>
      activeStatus.value === "all" || column.key === activeStatus.value,
  ),
);
const dueCount = computed(
  () => state.value.procedures.filter((item) => item.status === "due").length,
);
watch(state, (value) => props.api.save(value), { deep: true });
watch(selectedId, () => {
  sourceChecked.value = false;
  stepsChecked.value = false;
  attestation.value = "";
  error.value = "";
  editing.value = false;
});

function selectProcedure(id: string): void {
  selectedId.value = id;
}
function startReview(): void {
  if (!selected.value || selected.value.status === "reviewing") return;
  sourceChecked.value = false;
  stepsChecked.value = false;
  attestation.value = "";
  error.value = "";
  selected.value.status = "reviewing";
  selected.value.history.unshift(
    `${props.api.today} · ${selected.value.owner} · review started`,
  );
  props.api.toast(
    "Review opened. The earlier verification remains in history.",
  );
}
function beginRevision(): void {
  if (!selected.value) return;
  revisedBody.value = selected.value.body;
  revisionReason.value = "";
  error.value = "";
  editing.value = true;
}
function saveRevision(): void {
  if (!selected.value) return;
  if (
    revisedBody.value.trim().length < 30 ||
    revisionReason.value.trim().length < 12 ||
    revisedBody.value.trim() === selected.value.body
  ) {
    error.value =
      "Change the procedure excerpt and explain the revision in at least 12 characters.";
    return;
  }
  selected.value.version += 1;
  selected.value.body = revisedBody.value.trim();
  selected.value.status = "reviewing";
  selected.value.history.unshift(
    `${props.api.today} · v${selected.value.version} revision · ${revisionReason.value.trim()}`,
  );
  sourceChecked.value = false;
  stepsChecked.value = false;
  attestation.value = "";
  editing.value = false;
  error.value = "";
  props.api.toast(
    "Local revision saved. Verify the updated steps before attesting.",
  );
}
function attest(): void {
  if (!selected.value) return;
  error.value = "";
  if (selected.value.status !== "reviewing") {
    error.value = "Start a review before recording an attestation.";
    return;
  }
  if (
    !sourceChecked.value ||
    !stepsChecked.value ||
    attestation.value.trim().length < 12
  ) {
    error.value =
      "Complete both checks and describe what you verified in at least 12 characters.";
    return;
  }
  const nextDate = new Date(`${props.api.today}T12:00:00Z`);
  nextDate.setUTCDate(nextDate.getUTCDate() + 30);
  selected.value.due = nextDate.toISOString().slice(0, 10);
  selected.value.status = "verified";
  selected.value.history.unshift(
    `${props.api.today} · ${selected.value.owner} attested v${selected.value.version} · ${attestation.value.trim()}`,
  );
  props.api.toast(
    "Attestation recorded locally. Next review is due in 30 days.",
  );
}
function addProcedure(): void {
  newError.value = "";
  let validUrl = false;
  try {
    validUrl = new URL(newSource.value.trim()).protocol === "https:";
  } catch {
    validUrl = false;
  }
  if (newTitle.value.trim().length < 5 || !validUrl) {
    newError.value =
      "Provide a descriptive title and a valid HTTPS source URL.";
    return;
  }
  if (
    state.value.procedures.some(
      (item) => item.source === newSource.value.trim(),
    )
  ) {
    newError.value =
      "This source is already registered. Review its existing record.";
    return;
  }
  const id = `P-${101 + state.value.procedures.length}`;
  state.value.procedures.push({
    id,
    title: newTitle.value.trim(),
    owner: newOwner.value,
    team: "Operations",
    source: newSource.value.trim(),
    version: 1,
    body: "No excerpt supplied. Add a local revision after reviewing the source.",
    due: props.api.today,
    status: "due",
    history: [`${props.api.today} · registered for first review`],
  });
  selectedId.value = id;
  newTitle.value = "";
  newSource.value = "";
  addDialog.value?.close();
  props.api.toast("Procedure registered locally. The source was not fetched.");
}
function exportRegister(): void {
  props.api.download(
    "procedure-review-register.json",
    JSON.stringify(
      { synthetic: true, asOf: props.api.today, ...state.value },
      null,
      2,
    ),
    "application/json",
  );
}
</script>

<template>
  <section data-product="procedures">
    <header class="workspace-heading">
      <div>
        <p class="eyebrow">FIELDGUIDE / REVIEW CYCLE</p>
        <h1 class="page-title">Keep the way you work current.</h1>
        <p class="page-description">
          Small reviews. Named owners. A visible reason to trust each procedure.
        </p>
      </div>
      <div class="actions">
        <button class="btn secondary" @click="exportRegister">
          Export register</button
        ><button
          class="btn primary"
          @click="
            newError = '';
            addDialog?.showModal();
          "
        >
          Register procedure
        </button>
      </div>
    </header>
    <div class="review-summary">
      <strong>{{ dueCount }} procedures need a fresh review</strong
      ><span class="muted small"
        >{{ state.procedures.length }} procedures · 30-day review cycle ·
        Northline Studio</span
      >
    </div>
    <div class="tabs" aria-label="Review status">
      <button
        class="tab"
        :class="{ active: activeStatus === 'all' }"
        :aria-pressed="activeStatus === 'all'"
        @click="activeStatus = 'all'"
      >
        All procedures</button
      ><button
        v-for="column in columns"
        :key="column.key"
        class="tab"
        :class="{ active: activeStatus === column.key }"
        :aria-pressed="activeStatus === column.key"
        @click="activeStatus = column.key"
      >
        {{ column.label }}
      </button>
    </div>
    <div class="procedure-layout">
      <div
        class="review-board"
        :class="{ 'single-column': visibleColumns.length === 1 }"
      >
        <section
          v-for="column in visibleColumns"
          :key="column.key"
          class="review-column"
        >
          <div class="column-heading">
            <h2>
              {{ column.label }}
              <span class="badge neutral">{{
                state.procedures.filter((item) => item.status === column.key)
                  .length
              }}</span>
            </h2>
            <p class="muted small">{{ column.help }}</p>
          </div>
          <button
            v-for="procedure in state.procedures.filter(
              (item) => item.status === column.key,
            )"
            :key="procedure.id"
            class="procedure-card"
            :class="{ selected: selectedId === procedure.id }"
            :aria-pressed="selectedId === procedure.id"
            @click="selectProcedure(procedure.id)"
          >
            <span class="eyebrow">{{ procedure.team }}</span
            ><strong>{{ procedure.title }}</strong
            ><span class="card-meta"
              ><span class="avatar">{{
                procedure.owner
                  .split(" ")
                  .map((part) => part[0])
                  .join("")
              }}</span
              ><span>{{ procedure.owner }}</span></span
            ><span class="small muted"
              >v{{ procedure.version }} ·
              {{ procedure.status === "verified" ? "Next review" : "Due" }}
              {{ procedure.due }}</span
            >
          </button>
          <p
            v-if="!state.procedures.some((item) => item.status === column.key)"
            class="empty-state"
          >
            Nothing
            {{ column.key === "verified" ? "verified yet" : "waiting here" }}.
          </p>
        </section>
      </div>
      <aside v-if="selected" class="panel review-desk">
        <div class="panel-header">
          <div>
            <p class="eyebrow">REVIEW DESK / {{ selected.id }}</p>
            <h2>{{ selected.title }}</h2>
          </div>
          <span
            class="badge"
            :class="selected.status === 'verified' ? 'success' : 'warning'"
            >v{{ selected.version }}</span
          >
        </div>
        <div class="panel-body stack">
          <div class="small muted">
            Owner: {{ selected.owner }}<br />Source reference:
            <span class="source-reference">{{ selected.source }}</span>
          </div>
          <p class="small muted">
            The excerpt below is local synthetic content. Source documents are
            not fetched or edited.
          </p>
          <form v-if="editing" class="stack" @submit.prevent="saveRevision">
            <label class="field"
              >Revised excerpt<textarea
                v-model="revisedBody"
                class="textarea"
                rows="7"
              ></textarea></label
            ><label class="field"
              >What changed?<textarea
                v-model="revisionReason"
                class="textarea"
                rows="2"
                placeholder="Explain the operational change"
              ></textarea>
            </label>
            <div class="actions">
              <button class="btn primary" type="submit">Save revision</button
              ><button
                class="btn ghost"
                type="button"
                @click="
                  editing = false;
                  error = '';
                "
              >
                Cancel revision
              </button>
            </div>
          </form>
          <template v-else>
            <pre class="procedure-excerpt">{{ selected.body }}</pre>
            <div class="actions">
              <button
                v-if="selected.status !== 'reviewing'"
                class="btn primary"
                @click="startReview"
              >
                {{
                  selected.status === "verified"
                    ? "Reopen review"
                    : "Start review"
                }}</button
              ><button class="btn secondary" @click="beginRevision">
                Revise excerpt
              </button>
            </div></template
          >
          <form
            v-if="selected.status === 'reviewing' && !editing"
            class="attestation-form stack"
            @submit.prevent="attest"
          >
            <h3>What did you verify?</h3>
            <label class="checklist"
              ><input v-model="sourceChecked" type="checkbox" /> I compared the
              current source with this excerpt.</label
            ><label class="checklist"
              ><input v-model="stepsChecked" type="checkbox" /> I checked the
              steps against how the team works.</label
            ><label class="field"
              >Review evidence<textarea
                v-model="attestation"
                class="textarea"
                rows="3"
                placeholder="Example: Ran the handoff using Friday’s delivery; owner and access checks still match."
              ></textarea></label
            ><button class="btn primary" type="submit">
              Attest current version
            </button>
          </form>
          <p v-if="error" class="callout warning" role="alert">{{ error }}</p>
          <div v-if="selected.status === 'verified'" class="callout success">
            Current until {{ selected.due }}. This records a human review, not a
            compliance certification.
          </div>
          <details>
            <summary>Review history ({{ selected.history.length }})</summary>
            <ol class="review-history">
              <li v-for="(item, index) in selected.history" :key="index">
                {{ item }}
              </li>
            </ol>
          </details>
        </div>
      </aside>
    </div>
    <dialog ref="addDialog" class="modal" aria-labelledby="procedure-add-title">
      <form @submit.prevent="addProcedure">
        <div class="modal-header">
          <h2 id="procedure-add-title">Register a procedure</h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close procedure form"
            @click="addDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <label class="field"
            >Procedure title<input
              v-model="newTitle"
              class="input"
              placeholder="Monthly account review" /></label
          ><label class="field"
            >Source URL<input
              v-model="newSource"
              class="input"
              placeholder="https://example.com/wiki/account-review" /></label
          ><label class="field"
            >Review owner<select v-model="newOwner" class="select">
              <option>Maya Patel</option>
              <option>Jonas Reed</option>
              <option>Leah Okafor</option>
            </select></label
          >
          <p v-if="newError" role="alert" class="callout warning">
            {{ newError }}
          </p>
        </div>
        <div class="modal-footer">
          <button class="btn ghost" type="button" @click="addDialog?.close()">
            Cancel</button
          ><button class="btn primary" type="submit">
            Add to review queue
          </button>
        </div>
      </form>
    </dialog>
  </section>
</template>
