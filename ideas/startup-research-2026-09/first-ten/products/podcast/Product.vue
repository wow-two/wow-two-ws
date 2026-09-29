<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

type Guest = {
  name: string;
  email: string;
  bio: string;
  pronunciation: string;
  headshot: string;
  participationReviewed: boolean;
};
type Episode = {
  id: number;
  title: string;
  date: string;
  time: string;
  guest: Guest;
  techChecked: boolean;
  recorded: boolean;
  reminders: string[];
};
type EpisodeStage = "Needs prep" | "Ready" | "Recorded";
const props = defineProps<{ api: PrototypeApi }>();
const state = ref(
  props.api.state<{ episodes: Episode[] }>({
    episodes: [
      {
        id: 112,
        title: "Making room for better work",
        date: "2026-09-30",
        time: "15:00 UTC",
        guest: {
          name: "Lena Park",
          email: "lena@example.com",
          bio: "Lena studies how small teams create healthier working routines.",
          pronunciation: "LEE-nuh PARK",
          headshot: "",
          participationReviewed: false,
        },
        techChecked: true,
        recorded: false,
        reminders: [],
      },
      {
        id: 113,
        title: "The craft of a useful question",
        date: "2026-10-02",
        time: "16:00 UTC",
        guest: {
          name: "Omar Ellis",
          email: "omar@example.com",
          bio: "Omar is an independent interviewer and researcher of everyday decisions.",
          pronunciation: "OH-mar EL-iss",
          headshot: "omar-portrait.jpg",
          participationReviewed: true,
        },
        techChecked: true,
        recorded: false,
        reminders: [],
      },
      {
        id: 114,
        title: "Building a practice that lasts",
        date: "2026-10-05",
        time: "14:00 UTC",
        guest: {
          name: "Mira Chen",
          email: "mira@example.com",
          bio: "",
          pronunciation: "",
          headshot: "",
          participationReviewed: false,
        },
        techChecked: false,
        recorded: false,
        reminders: [],
      },
      {
        id: 111,
        title: "A little more attention",
        date: "2026-09-25",
        time: "15:00 UTC",
        guest: {
          name: "Jules Gray",
          email: "jules@example.com",
          bio: "Jules writes about attention, place, and the things people notice.",
          pronunciation: "JOOLZ GRAY",
          headshot: "jules-gray.jpg",
          participationReviewed: true,
        },
        techChecked: true,
        recorded: true,
        reminders: [],
      },
    ],
  }),
);
const selectedId = ref(112);
const guestDialog = ref<HTMLDialogElement | null>(null);
const reminderDialog = ref<HTMLDialogElement | null>(null);
const addDialog = ref<HTMLDialogElement | null>(null);
const guestBio = ref("");
const guestPronunciation = ref("");
const guestHeadshot = ref("");
const guestReviewed = ref(false);
const guestError = ref("");
const newTitle = ref("");
const newName = ref("");
const newEmail = ref("");
const newDate = ref("2026-10-08");
const newTime = ref("15:00 UTC");
const addError = ref("");
const stages: EpisodeStage[] = ["Needs prep", "Ready", "Recorded"];
const selected = computed(
  () =>
    state.value.episodes.find((item) => item.id === selectedId.value) ??
    state.value.episodes[0]!,
);
const selectedChecks = computed(() => checks(selected.value));
const complete = computed(
  () => selectedChecks.value.filter((item) => item.done).length,
);
const percent = computed(() => complete.value * 25);
const ready = computed(
  () => state.value.episodes.filter((item) => stage(item) === "Ready").length,
);
const needsPrep = computed(
  () =>
    state.value.episodes.filter((item) => stage(item) === "Needs prep").length,
);
const missing = computed(() =>
  selectedChecks.value.filter((item) => !item.done),
);
const nextEpisode = computed(
  () =>
    state.value.episodes
      .filter((item) => !item.recorded && item.date >= props.api.today)
      .sort((a, b) => a.date.localeCompare(b.date))[0],
);
const remindedToday = computed(() =>
  selected.value.reminders.includes(props.api.today),
);
watch(state, (value) => props.api.save(value), { deep: true });

function inputValue(event: Event): string {
  return (event.target as HTMLInputElement).value;
}
function checks(
  item: Episode,
): { label: string; done: boolean; helper: string }[] {
  return [
    {
      label: "Guest biography",
      done: item.guest.bio.trim().length >= 20,
      helper: "A short introduction in their own words",
    },
    {
      label: "Headshot reference",
      done: Boolean(item.guest.headshot),
      helper: item.guest.headshot || "An asset reference for episode artwork",
    },
    {
      label: "Participation information reviewed",
      done: item.guest.participationReviewed,
      helper: "Producer-supplied terms · sample acknowledgment only",
    },
    {
      label: "Technical check confirmed",
      done: item.techChecked,
      helper: "Producer confirms a separate audio check",
    },
  ];
}
function stage(item: Episode): EpisodeStage {
  return item.recorded
    ? "Recorded"
    : checks(item).every((check) => check.done)
      ? "Ready"
      : "Needs prep";
}
function stageClass(item: Episode): string {
  return stage(item) === "Ready"
    ? "success"
    : stage(item) === "Recorded"
      ? "neutral"
      : "warning";
}
function openGuest(): void {
  guestBio.value = selected.value.guest.bio;
  guestPronunciation.value = selected.value.guest.pronunciation;
  guestHeadshot.value = selected.value.guest.headshot;
  guestReviewed.value = selected.value.guest.participationReviewed;
  guestError.value = "";
  guestDialog.value?.showModal();
}
function saveGuest(event: Event): void {
  event.preventDefault();
  if (guestBio.value.trim().length < 20) {
    guestError.value = "Add a biography of at least 20 characters.";
    return;
  }
  if (!/\.(jpe?g|png|webp)$/i.test(guestHeadshot.value.trim())) {
    guestError.value =
      "Enter an image filename ending in .jpg, .png, or .webp. No file will be uploaded.";
    return;
  }
  if (!guestReviewed.value) {
    guestError.value =
      "Review the sample participation information before saving this demonstration.";
    return;
  }
  selected.value.guest = {
    ...selected.value.guest,
    bio: guestBio.value.trim(),
    pronunciation: guestPronunciation.value.trim(),
    headshot: guestHeadshot.value.trim(),
    participationReviewed: guestReviewed.value,
  };
  guestDialog.value?.close();
  props.api.toast(
    "Sample guest form saved locally. No assets uploaded or signature collected.",
  );
}
function toggleTech(): void {
  if (selected.value.recorded) return;
  selected.value.techChecked = !selected.value.techChecked;
  props.api.toast(
    selected.value.techChecked
      ? "Technical check marked confirmed in the sample."
      : "Technical check reopened.",
  );
}
function markRecorded(): void {
  if (stage(selected.value) !== "Ready") return;
  selected.value.recorded = true;
  props.api.toast(
    "Episode marked recorded in the prototype. No media was captured.",
  );
}
function recordReminder(): void {
  if (remindedToday.value || missing.value.length === 0) return;
  selected.value.reminders.push(props.api.today);
  reminderDialog.value?.close();
  props.api.toast("Reminder simulation recorded. No email was sent.");
}
function openEpisode(): void {
  newTitle.value = "";
  newName.value = "";
  newEmail.value = "";
  addError.value = "";
  addDialog.value?.showModal();
}
function addEpisode(event: Event): void {
  event.preventDefault();
  if (
    newTitle.value.trim().length < 5 ||
    newName.value.trim().length < 2 ||
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newEmail.value.trim()) ||
    !/^\d{4}-\d{2}-\d{2}$/.test(newDate.value) ||
    !Number.isFinite(Date.parse(newDate.value)) ||
    newDate.value < props.api.today ||
    !/^([01]\d|2[0-3]):[0-5]\d UTC$/.test(newTime.value)
  ) {
    addError.value =
      "Enter an episode title, guest name, valid email, upcoming date, and time such as 15:00 UTC.";
    return;
  }
  if (
    state.value.episodes.some(
      (item) =>
        item.guest.email.toLowerCase() ===
          newEmail.value.trim().toLowerCase() &&
        item.date === newDate.value &&
        item.time === newTime.value,
    )
  ) {
    addError.value = "This guest already has an episode at that time.";
    return;
  }
  const id = Math.max(...state.value.episodes.map((item) => item.id)) + 1;
  state.value.episodes.push({
    id,
    title: newTitle.value.trim(),
    date: newDate.value,
    time: newTime.value,
    guest: {
      name: newName.value.trim(),
      email: newEmail.value.trim(),
      bio: "",
      pronunciation: "",
      headshot: "",
      participationReviewed: false,
    },
    techChecked: false,
    recorded: false,
    reminders: [],
  });
  selectedId.value = id;
  addDialog.value?.close();
  props.api.toast("Sample episode added. No guest invitation was sent.");
}
function exportPack(): void {
  props.api.download(
    `episode-${selected.value.id}-readiness.json`,
    JSON.stringify(
      {
        synthetic: true,
        date: props.api.today,
        stage: stage(selected.value),
        readiness: checks(selected.value),
        episode: selected.value,
        note: "Local sample record; not a release signature or a recording.",
      },
      null,
      2,
    ),
    "application/json",
  );
}
</script>

<template>
  <div data-product="podcast">
    <header class="workspace-heading">
      <div>
        <p class="eyebrow">Guestroom · pre-production</p>
        <h1 class="page-title">Ready before the red light.</h1>
        <p class="page-description">
          A calm place for the small details that make a guest feel prepared.
        </p>
      </div>
      <div class="actions">
        <button class="btn secondary" @click="exportPack">
          Export episode pack</button
        ><button class="btn primary" @click="openEpisode">Add episode</button>
      </div>
    </header>
    <section class="podcast-next panel">
      <div class="podcast-showmark" aria-hidden="true">
        <span>STILL<br />CURIOUS</span><i></i><small>THE PODCAST</small>
      </div>
      <div class="podcast-next-copy">
        <p class="eyebrow">Next recording · Still Curious</p>
        <h2>{{ nextEpisode?.title ?? "No upcoming recordings" }}</h2>
        <p class="muted">
          {{
            nextEpisode
              ? `${nextEpisode.guest.name} · ${nextEpisode.date} · ${nextEpisode.time}`
              : "Add an episode when your next guest is confirmed."
          }}
        </p>
      </div>
      <div class="podcast-stat">
        <strong>{{ ready }}</strong
        ><span>ready to record</span>
      </div>
      <div class="podcast-stat">
        <strong>{{ needsPrep }}</strong
        ><span>need preparation</span>
      </div>
    </section>
    <div class="podcast-layout">
      <section aria-label="Episode readiness board" class="podcast-board">
        <div v-for="column in stages" :key="column" class="podcast-column">
          <header class="podcast-column-title">
            <h2>{{ column }}</h2>
            <span class="badge neutral">{{
              state.episodes.filter((item) => stage(item) === column).length
            }}</span>
          </header>
          <button
            v-for="item in state.episodes.filter(
              (record) => stage(record) === column,
            )"
            :key="item.id"
            class="podcast-card"
            :class="{ selected: selected.id === item.id }"
            @click="selectedId = item.id"
          >
            <span class="podcast-card-top"
              ><span class="eyebrow">EP {{ item.id }}</span
              ><span class="small muted">{{ item.date.slice(5) }}</span></span
            ><strong>{{ item.title }}</strong
            ><span class="podcast-card-person"
              ><span class="avatar">{{
                item.guest.name
                  .split(" ")
                  .map((word) => word[0])
                  .join("")
              }}</span
              ><span>{{ item.guest.name }}</span></span
            ><progress
              :value="checks(item).filter((check) => check.done).length"
              max="4"
              :aria-label="`${item.guest.name} readiness`"
            ></progress
            ><span class="small muted"
              >{{ checks(item).filter((check) => check.done).length }}/4
              preparation items</span
            >
          </button>
          <div
            v-if="!state.episodes.some((item) => stage(item) === column)"
            class="podcast-column-empty"
          >
            {{
              column === "Ready"
                ? "Complete every preparation item to move an episode here."
                : "No episodes in this stage."
            }}
          </div>
        </div>
      </section>
      <aside class="panel podcast-inspector">
        <div class="panel-header">
          <div>
            <p class="eyebrow">Episode {{ selected.id }} · guest detail</p>
            <h2>{{ selected.guest.name }}</h2>
            <p class="small muted">{{ selected.date }} · {{ selected.time }}</p>
          </div>
          <span class="badge" :class="stageClass(selected)">{{
            stage(selected)
          }}</span>
        </div>
        <div class="panel-body stack">
          <div class="podcast-readiness">
            <strong>{{ percent }}%</strong>
            <div>
              <span>Recording preparation</span>
              <p class="small muted">{{ complete }} of 4 items complete</p>
            </div>
          </div>
          <ul class="podcast-checklist">
            <li v-for="check in selectedChecks" :key="check.label">
              <span
                class="podcast-check-icon"
                :class="{ complete: check.done }"
                aria-hidden="true"
                >{{ check.done ? "✓" : "○" }}</span
              >
              <div>
                <strong>{{ check.label }}</strong>
                <p class="small muted">{{ check.helper }}</p>
                <span class="visually-hidden">{{
                  check.done ? "Complete" : "Incomplete"
                }}</span>
              </div>
            </li>
          </ul>
          <div class="actions">
            <button
              class="btn primary"
              :disabled="selected.recorded"
              @click="openGuest"
            >
              Preview guest form</button
            ><button
              class="btn secondary"
              :disabled="selected.recorded"
              @click="toggleTech"
            >
              {{
                selected.techChecked
                  ? "Reopen technical check"
                  : "Confirm technical check"
              }}
            </button>
          </div>
          <section class="podcast-guest-notes">
            <p class="eyebrow">Host notes</p>
            <p>
              {{
                selected.guest.bio || "The guest biography will appear here."
              }}
            </p>
            <p class="small muted">
              Pronunciation:
              {{ selected.guest.pronunciation || "Not supplied" }}
            </p>
          </section>
          <button
            class="btn secondary"
            :disabled="
              missing.length === 0 || remindedToday || selected.recorded
            "
            @click="reminderDialog?.showModal()"
          >
            {{
              remindedToday
                ? "Reminder simulated today"
                : "Preview missing-item reminder"
            }}
          </button>
          <p v-if="selected.reminders.length" class="small muted">
            {{ selected.reminders.length }} reminder simulation(s) recorded · no
            email sent
          </p>
          <button
            class="btn primary"
            :disabled="stage(selected) !== 'Ready'"
            @click="markRecorded"
          >
            {{
              selected.recorded
                ? "Recorded · simulated"
                : "Mark recorded · simulated"
            }}
          </button>
          <p class="small muted">
            Readiness records preparation. It does not record audio or certify
            guest consent.
          </p>
        </div>
      </aside>
    </div>
    <dialog
      ref="guestDialog"
      class="modal"
      aria-labelledby="podcast-guest-title"
    >
      <form novalidate @submit="saveGuest">
        <div class="modal-header">
          <div>
            <p class="eyebrow">Guest-facing preview · synthetic</p>
            <h2 id="podcast-guest-title">
              Welcome, {{ selected.guest.name.split(" ")[0] }}.
            </h2>
          </div>
          <button
            class="icon-button"
            type="button"
            aria-label="Close guest form"
            @click="guestDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p>
            You’re joining <strong>Still Curious</strong> on
            {{ selected.date }} at {{ selected.time }}. A few details help us
            introduce you.
          </p>
          <label class="field"
            >Your short biography<textarea
              class="textarea"
              rows="3"
              :value="guestBio"
              @input="guestBio = inputValue($event)"
            ></textarea></label
          ><label class="field"
            >How do we say your name?<input
              class="input"
              :value="guestPronunciation"
              placeholder="A phonetic spelling is welcome"
              @input="guestPronunciation = inputValue($event)" /></label
          ><label class="field"
            >Headshot filename<input
              class="input"
              :value="guestHeadshot"
              placeholder="lena-park.jpg"
              @input="guestHeadshot = inputValue($event)"
            /><span class="small muted"
              >Reference only. This prototype does not upload or display the
              image.</span
            ></label
          >
          <div class="callout info">
            Sample participation information: this conversation is planned for
            an edited podcast episode. The producer supplies the actual terms
            and handles any release separately.
          </div>
          <label class="podcast-checkbox"
            ><input
              type="checkbox"
              :checked="guestReviewed"
              @change="
                guestReviewed = ($event.target as HTMLInputElement).checked
              "
            /><span
              >I reviewed this sample information. This checkbox is not a
              signature.</span
            ></label
          >
          <p v-if="guestError" role="alert" class="podcast-error">
            {{ guestError }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn secondary"
            @click="guestDialog?.close()"
          >
            Cancel</button
          ><button type="submit" class="btn primary">
            Save sample guest form
          </button>
        </div>
      </form>
    </dialog>
    <dialog
      ref="reminderDialog"
      class="modal"
      aria-labelledby="podcast-reminder-title"
    >
      <div class="modal-header">
        <h2 id="podcast-reminder-title">Missing-item reminder</h2>
        <button
          class="icon-button"
          aria-label="Close reminder preview"
          @click="reminderDialog?.close()"
        >
          ×
        </button>
      </div>
      <div class="modal-body stack">
        <span class="badge warning">Local preview · never sent</span>
        <p class="small muted">To: {{ selected.guest.email }}</p>
        <h3>A few details before Still Curious</h3>
        <p>
          Hi {{ selected.guest.name.split(" ")[0] }}, here’s what remains before
          {{ selected.date }}:
        </p>
        <ul>
          <li v-for="item in missing" :key="item.label">{{ item.label }}</li>
        </ul>
        <p>Thanks for helping us prepare for a thoughtful conversation.</p>
      </div>
      <div class="modal-footer">
        <button class="btn secondary" @click="reminderDialog?.close()">
          Close</button
        ><button
          class="btn primary"
          :disabled="remindedToday || missing.length === 0"
          @click="recordReminder"
        >
          Record simulated reminder
        </button>
      </div>
    </dialog>
    <dialog ref="addDialog" class="modal" aria-labelledby="podcast-add-title">
      <form novalidate @submit="addEpisode">
        <div class="modal-header">
          <h2 id="podcast-add-title">Add an upcoming episode</h2>
          <button
            class="icon-button"
            type="button"
            aria-label="Close episode form"
            @click="addDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <label class="field"
            >Episode title<input
              class="input"
              :value="newTitle"
              @input="newTitle = inputValue($event)" /></label
          ><label class="field"
            >Guest name<input
              class="input"
              :value="newName"
              @input="newName = inputValue($event)" /></label
          ><label class="field"
            >Guest email<input
              class="input"
              type="email"
              :value="newEmail"
              placeholder="guest@example.com"
              @input="newEmail = inputValue($event)"
          /></label>
          <div class="form-grid">
            <label class="field"
              >Recording date<input
                class="input"
                type="date"
                :min="api.today"
                :value="newDate"
                @input="newDate = inputValue($event)" /></label
            ><label class="field"
              >Recording time<input
                class="input"
                :value="newTime"
                placeholder="15:00 UTC"
                @input="newTime = inputValue($event)"
            /></label>
          </div>
          <p v-if="addError" role="alert" class="podcast-error">
            {{ addError }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            class="btn secondary"
            type="button"
            @click="addDialog?.close()"
          >
            Cancel</button
          ><button class="btn primary" type="submit">Create episode</button>
        </div>
      </form>
    </dialog>
  </div>
</template>
