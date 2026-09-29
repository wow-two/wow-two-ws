<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

type LearnerStatus = "enrolled" | "attended" | "released";
interface Learner {
  id: string;
  name: string;
  email: string;
  cohort: string;
  status: LearnerStatus;
  replaces: string;
  notes: string[];
}
interface TrainingState {
  purchased: number;
  learners: Learner[];
  adjustments: string[];
}
const props = defineProps<{ api: PrototypeApi }>();
const state = ref(
  props.api.state<TrainingState>({
    purchased: 12,
    learners: [
      {
        id: "L-101",
        name: "Mira Hassan",
        email: "mira@example.com",
        cohort: "C-SEP",
        status: "attended",
        replaces: "",
        notes: ["2026-09-24 · attendance confirmed by coordinator"],
      },
      {
        id: "L-102",
        name: "Noah Kim",
        email: "noah@example.com",
        cohort: "C-SEP",
        status: "enrolled",
        replaces: "",
        notes: ["2026-09-10 · reserved under ORB-2026-04"],
      },
      {
        id: "L-103",
        name: "Asha Rao",
        email: "asha@example.com",
        cohort: "C-OCT",
        status: "enrolled",
        replaces: "",
        notes: ["2026-09-15 · reserved under ORB-2026-04"],
      },
      {
        id: "L-104",
        name: "Owen Blake",
        email: "owen@example.com",
        cohort: "C-OCT",
        status: "enrolled",
        replaces: "",
        notes: ["2026-09-15 · reserved under ORB-2026-04"],
      },
      {
        id: "L-105",
        name: "Sofia Costa",
        email: "sofia@example.com",
        cohort: "C-SEP",
        status: "released",
        replaces: "",
        notes: ["2026-09-20 · replaced by Hana Mori; seat preserved"],
      },
      {
        id: "L-106",
        name: "Hana Mori",
        email: "hana@example.com",
        cohort: "C-SEP",
        status: "enrolled",
        replaces: "L-105",
        notes: ["2026-09-20 · substituted for Sofia Costa"],
      },
    ],
    adjustments: [
      "12 seats purchased under sponsor agreement ORB-2026-04; synthetic contract.",
    ],
  }),
);
const cohorts = [
  {
    id: "C-SEP",
    name: "Facilitation foundations",
    date: "2026-09-24",
    capacity: 8,
  },
  {
    id: "C-OCT",
    name: "Remote workshop practice",
    date: "2026-10-14",
    capacity: 8,
  },
];
const selectedId = ref("L-102");
const cohortFilter = ref("all");
const includeReleased = ref(false);
const learnerDialog = ref<HTMLDialogElement | null>(null);
const releaseDialog = ref<HTMLDialogElement | null>(null);
const mode = ref<"add" | "substitute">("add");
const learnerName = ref("");
const learnerEmail = ref("");
const learnerCohort = ref("C-OCT");
const changeReason = ref("");
const error = ref("");
const releaseReason = ref("");
const releaseError = ref("");
const selected = computed(() =>
  state.value.learners.find((learner) => learner.id === selectedId.value),
);
const occupied = computed(() =>
  state.value.learners.filter((learner) => learner.status !== "released"),
);
const attended = computed(
  () =>
    state.value.learners.filter((learner) => learner.status === "attended")
      .length,
);
const reserved = computed(
  () =>
    state.value.learners.filter((learner) => learner.status === "enrolled")
      .length,
);
const available = computed(() => state.value.purchased - occupied.value.length);
const roster = computed(() =>
  state.value.learners.filter(
    (learner) =>
      (cohortFilter.value === "all" || learner.cohort === cohortFilter.value) &&
      (includeReleased.value || learner.status !== "released"),
  ),
);
watch(state, (value) => props.api.save(value), { deep: true });

function cohortName(id: string): string {
  return cohorts.find((cohort) => cohort.id === id)?.name ?? id;
}
function cohortUsed(id: string): number {
  return occupied.value.filter((learner) => learner.cohort === id).length;
}
function canAttend(learner: Learner): boolean {
  return (
    (cohorts.find((cohort) => cohort.id === learner.cohort)?.date ?? "9999") <=
    props.api.today
  );
}
function openLearnerForm(nextMode: "add" | "substitute"): void {
  if (nextMode === "substitute" && selected.value?.status !== "enrolled")
    return;
  mode.value = nextMode;
  learnerName.value = "";
  learnerEmail.value = "";
  changeReason.value = "";
  error.value = "";
  learnerCohort.value =
    nextMode === "substitute" ? (selected.value?.cohort ?? "C-OCT") : "C-OCT";
  learnerDialog.value?.showModal();
}
function saveLearner(): void {
  error.value = "";
  const name = learnerName.value.trim();
  const email = learnerEmail.value.trim().toLowerCase();
  if (name.length < 3 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    error.value = "Enter a full name and a valid email address.";
    return;
  }
  if (occupied.value.some((learner) => learner.email.toLowerCase() === email)) {
    error.value = "This learner already holds a seat in this agreement.";
    return;
  }
  const cohort = cohorts.find((item) => item.id === learnerCohort.value);
  if (!cohort) {
    error.value = "Choose a valid cohort.";
    return;
  }
  const previous = mode.value === "substitute" ? selected.value : undefined;
  if (
    mode.value === "substitute" &&
    (!previous || previous.status !== "enrolled")
  ) {
    error.value = "Only an enrolled, unconsumed seat can be substituted.";
    return;
  }
  if (mode.value === "add" && available.value <= 0) {
    error.value =
      "All purchased seats are allocated. Release an unused seat first.";
    return;
  }
  if (
    cohortUsed(cohort.id) - (previous?.cohort === cohort.id ? 1 : 0) >=
    cohort.capacity
  ) {
    error.value = "This cohort is full. Select another cohort.";
    return;
  }
  if (mode.value === "substitute" && changeReason.value.trim().length < 8) {
    error.value = "Explain the substitution in at least 8 characters.";
    return;
  }
  const id = `L-${101 + state.value.learners.length}`;
  if (previous) {
    previous.status = "released";
    previous.notes.unshift(
      `${props.api.today} · replaced by ${name} · ${changeReason.value.trim()}`,
    );
  }
  state.value.learners.push({
    id,
    name,
    email,
    cohort: cohort.id,
    status: "enrolled",
    replaces: previous?.id ?? "",
    notes: [
      `${props.api.today} · ${previous ? `substituted for ${previous.name}; purchased balance unchanged` : "seat reserved by coordinator"}`,
    ],
  });
  state.value.adjustments.unshift(
    `${props.api.today} · ${previous ? `${previous.name} → ${name}: substitution` : `${name}: one seat allocated`}`,
  );
  selectedId.value = id;
  cohortFilter.value = "all";
  learnerDialog.value?.close();
  props.api.toast(
    previous
      ? "Learner substituted locally. No extra seat consumed."
      : "Seat reserved locally. No invitation was sent.",
  );
}
function markAttendance(): void {
  if (
    !selected.value ||
    selected.value.status === "released" ||
    !canAttend(selected.value)
  )
    return;
  const next = selected.value.status === "attended" ? "enrolled" : "attended";
  selected.value.status = next;
  selected.value.notes.unshift(
    `${props.api.today} · attendance ${next === "attended" ? "confirmed" : "correction: restored to enrolled"}`,
  );
  props.api.toast(
    next === "attended"
      ? "Attendance recorded. The seat remains consumed."
      : "Attendance corrected. The seat remains reserved.",
  );
}
function releaseSeat(): void {
  releaseError.value = "";
  if (!selected.value || selected.value.status !== "enrolled") return;
  if (releaseReason.value.trim().length < 8) {
    releaseError.value = "Explain why the unused seat is being released.";
    return;
  }
  selected.value.status = "released";
  selected.value.notes.unshift(
    `${props.api.today} · seat released · ${releaseReason.value.trim()}`,
  );
  state.value.adjustments.unshift(
    `${props.api.today} · ${selected.value.name}: one unused seat returned`,
  );
  releaseDialog.value?.close();
  props.api.toast("Unused seat returned to the sponsor allowance.");
}
function exportSponsor(): void {
  props.api.download(
    "orbit-training-seat-statement.json",
    JSON.stringify(
      {
        synthetic: true,
        sponsor: "Orbit Foundation",
        agreement: "ORB-2026-04",
        asOf: props.api.today,
        purchased: state.value.purchased,
        attended: attended.value,
        reserved: reserved.value,
        available: available.value,
        cohorts,
        learners: state.value.learners,
        audit: state.value.adjustments,
      },
      null,
      2,
    ),
    "application/json",
  );
}
</script>

<template>
  <section data-product="training">
    <header class="workspace-heading">
      <div>
        <p class="eyebrow">SEATBOOK / CORPORATE AGREEMENT</p>
        <h1 class="page-title">One agreement. Every seat accounted for.</h1>
        <p class="page-description">
          Orbit Foundation · ORB-2026-04 · Autumn workshop programme
        </p>
      </div>
      <div class="actions">
        <button class="btn secondary" @click="exportSponsor">
          Export sponsor statement</button
        ><button class="btn primary" @click="openLearnerForm('add')">
          Reserve a seat
        </button>
      </div>
    </header>
    <section class="panel seat-summary">
      <div class="seat-equation">
        <div>
          <span class="metric-label">Purchased</span
          ><strong>{{ state.purchased }}</strong>
        </div>
        <span class="equation-sign">−</span>
        <div>
          <span class="metric-label">Attended</span
          ><strong>{{ attended }}</strong>
        </div>
        <span class="equation-sign">−</span>
        <div>
          <span class="metric-label">Reserved</span
          ><strong>{{ reserved }}</strong>
        </div>
        <span class="equation-sign">=</span>
        <div class="seat-balance">
          <span class="metric-label">Available</span
          ><strong>{{ available }}</strong>
        </div>
      </div>
      <div
        class="seat-map"
        role="img"
        :aria-label="`${attended} attended, ${reserved} reserved, ${available} available out of ${state.purchased} seats`"
      >
        <span
          v-for="seat in state.purchased"
          :key="seat"
          class="seat-tile"
          :class="
            seat <= attended
              ? 'attended'
              : seat <= attended + reserved
                ? 'reserved'
                : 'available'
          "
          >{{ seat.toString().padStart(2, "0") }}</span
        >
      </div>
      <p class="small muted">
        Substitutions transfer a reservation. They never consume a second seat.
      </p>
    </section>
    <div class="cohort-strip">
      <button
        v-for="cohort in cohorts"
        :key="cohort.id"
        class="cohort-ticket"
        :class="{ active: cohortFilter === cohort.id }"
        :aria-pressed="cohortFilter === cohort.id"
        @click="cohortFilter = cohortFilter === cohort.id ? 'all' : cohort.id"
      >
        <span class="eyebrow">{{ cohort.date }}</span
        ><strong>{{ cohort.name }}</strong
        ><span class="small muted"
          >{{ cohortUsed(cohort.id) }} / {{ cohort.capacity }} cohort places ·
          {{ cohort.date > api.today ? "Upcoming" : "Attendance open" }}</span
        >
      </button>
    </div>
    <div class="training-layout">
      <section class="panel">
        <div class="panel-header">
          <div>
            <h2>Sponsor roster</h2>
            <p class="small muted">
              {{
                cohortFilter === "all"
                  ? "All cohorts"
                  : cohortName(cohortFilter)
              }}
            </p>
          </div>
          <label class="checklist small"
            ><input v-model="includeReleased" type="checkbox" /> Show released
            learners</label
          >
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Learner</th>
                <th>Cohort</th>
                <th>Seat status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="learner in roster"
                :key="learner.id"
                :class="{ selected: selectedId === learner.id }"
              >
                <td>
                  <button class="learner-link" @click="selectedId = learner.id">
                    {{ learner.name }}</button
                  ><small class="muted">{{ learner.email }}</small>
                </td>
                <td>
                  {{ cohortName(learner.cohort)
                  }}<small v-if="learner.replaces" class="muted"
                    >Substitution · no new seat</small
                  >
                </td>
                <td>
                  <span
                    class="badge"
                    :class="
                      learner.status === 'attended'
                        ? 'success'
                        : learner.status === 'released'
                          ? 'neutral'
                          : 'info'
                    "
                    >{{ learner.status }}</span
                  >
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="!roster.length" class="empty-state">
            No learners match this view. Select another cohort or reserve a
            seat.
          </div>
        </div>
      </section>
      <aside v-if="selected" class="panel learner-desk">
        <div class="panel-header">
          <div>
            <p class="eyebrow">LEARNER DETAIL</p>
            <h2>{{ selected.name }}</h2>
          </div>
          <span class="avatar">{{
            selected.name
              .split(" ")
              .map((part) => part[0])
              .join("")
          }}</span>
        </div>
        <div class="panel-body stack">
          <div>
            <p class="small muted">{{ selected.email }}</p>
            <strong>{{ cohortName(selected.cohort) }}</strong>
            <p class="small muted">{{ selected.id }} · {{ selected.status }}</p>
          </div>
          <p v-if="selected.replaces" class="callout info">
            Transferred from
            {{
              state.learners.find(
                (learner) => learner.id === selected?.replaces,
              )?.name
            }}. The agreement balance did not change.
          </p>
          <div v-if="selected.status !== 'released'" class="stack">
            <button
              class="btn primary"
              :disabled="!canAttend(selected)"
              @click="markAttendance"
            >
              {{
                selected.status === "attended"
                  ? "Correct attendance"
                  : "Mark attended"
              }}
            </button>
            <p v-if="!canAttend(selected)" class="small muted">
              Attendance opens on the cohort date.
            </p>
            <button
              v-if="selected.status === 'enrolled'"
              class="btn secondary"
              @click="openLearnerForm('substitute')"
            >
              Substitute learner</button
            ><button
              v-if="selected.status === 'enrolled'"
              class="btn ghost"
              @click="
                releaseReason = '';
                releaseError = '';
                releaseDialog?.showModal();
              "
            >
              Release unused seat
            </button>
          </div>
          <p v-else class="callout info">
            This record is retained for the sponsor’s audit trail. It consumes
            no seat.
          </p>
          <div>
            <h3>Seat history</h3>
            <ol class="seat-history">
              <li v-for="(note, index) in selected.notes" :key="index">
                {{ note }}
              </li>
            </ol>
          </div>
        </div>
      </aside>
    </div>
    <dialog
      ref="learnerDialog"
      class="modal"
      aria-labelledby="training-learner-title"
    >
      <form @submit.prevent="saveLearner">
        <div class="modal-header">
          <h2 id="training-learner-title">
            {{
              mode === "substitute" ? "Substitute learner" : "Reserve a seat"
            }}
          </h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close learner form"
            @click="learnerDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p v-if="mode === 'substitute'" class="callout info">
            Replacing {{ selected?.name }}. One reservation moves to the new
            learner.
          </p>
          <label class="field"
            >Learner name<input
              v-model="learnerName"
              class="input"
              autocomplete="off"
              placeholder="Alex Morgan" /></label
          ><label class="field"
            >Learner email<input
              v-model="learnerEmail"
              class="input"
              autocomplete="off"
              placeholder="alex@example.com" /></label
          ><label class="field"
            >Cohort<select v-model="learnerCohort" class="select">
              <option
                v-for="cohort in cohorts"
                :key="cohort.id"
                :value="cohort.id"
              >
                {{ cohort.name }} · {{ cohort.date }}
              </option>
            </select></label
          ><label v-if="mode === 'substitute'" class="field"
            >Reason for substitution<textarea
              v-model="changeReason"
              class="textarea"
              rows="2"
              placeholder="Original learner changed teams"
            ></textarea>
          </label>
          <p v-if="error" role="alert" class="callout warning">{{ error }}</p>
          <p class="small muted">
            This changes the local roster only. No learner or sponsor will be
            contacted.
          </p>
        </div>
        <div class="modal-footer">
          <button
            class="btn ghost"
            type="button"
            @click="learnerDialog?.close()"
          >
            Cancel</button
          ><button class="btn primary" type="submit">
            {{
              mode === "substitute"
                ? "Confirm substitution"
                : "Confirm reservation"
            }}
          </button>
        </div>
      </form>
    </dialog>
    <dialog
      ref="releaseDialog"
      class="modal"
      aria-labelledby="training-release-title"
    >
      <form @submit.prevent="releaseSeat">
        <div class="modal-header">
          <h2 id="training-release-title">
            Release {{ selected?.name }}’s unused seat
          </h2>
          <button
            type="button"
            class="icon-button"
            aria-label="Close seat release"
            @click="releaseDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p>
            The learner’s record stays in history. The sponsor will regain one
            available seat.
          </p>
          <label class="field"
            >Reason<textarea
              v-model="releaseReason"
              class="textarea"
              rows="3"
            ></textarea>
          </label>
          <p v-if="releaseError" role="alert" class="callout warning">
            {{ releaseError }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            class="btn ghost"
            type="button"
            @click="releaseDialog?.close()"
          >
            Keep reservation</button
          ><button class="btn primary" type="submit">
            Confirm seat release
          </button>
        </div>
      </form>
    </dialog>
  </section>
</template>
