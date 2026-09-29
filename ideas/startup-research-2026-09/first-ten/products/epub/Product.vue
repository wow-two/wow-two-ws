<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { PrototypeApi } from "../../shared/PrototypeApi";
import "./product.css";

type Finding = {
  id: string;
  title: string;
  file: string;
  location: string;
  source: "Ace sample" | "Human check";
  severity: "Serious" | "Moderate" | "Review";
  status: "Open" | "Resolved";
  owner: string;
  evidence: string;
  detail: string;
};
type Version = {
  id: number;
  label: string;
  imported: boolean;
  reviewed: boolean;
  findings: Finding[];
};
const props = defineProps<{ api: PrototypeApi }>();
const state = ref(
  props.api.state<{ activeVersion: number; versions: Version[] }>({
    activeVersion: 1,
    versions: [
      {
        id: 1,
        label: "Proof 01",
        imported: false,
        reviewed: false,
        findings: [
          {
            id: "f1",
            title: "Image alternative is missing",
            file: "chapter-02.xhtml",
            location: "Figure 2 · line 48",
            source: "Ace sample",
            severity: "Serious",
            status: "Open",
            owner: "Maya",
            evidence: "",
            detail:
              "Supplied sample finding: an informative diagram has an empty text alternative. A reviewer must judge the replacement in context.",
          },
          {
            id: "f2",
            title: "Publication language is absent",
            file: "package.opf",
            location: "Package metadata",
            source: "Ace sample",
            severity: "Moderate",
            status: "Open",
            owner: "Maya",
            evidence: "",
            detail:
              "Supplied sample finding: the package does not declare its primary language. Record the verified correction for this proof.",
          },
          {
            id: "f3",
            title: "Check heading sequence",
            file: "chapter-02.xhtml",
            location: "Chapter outline",
            source: "Human check",
            severity: "Review",
            status: "Open",
            owner: "Jon",
            evidence: "",
            detail:
              "Read the outline in context. Confirm headings describe the structure and navigation is understandable; automated findings cannot settle this judgment.",
          },
          {
            id: "f4",
            title: "Review reading order",
            file: "chapter-03.xhtml",
            location: "Sidebar and main text",
            source: "Human check",
            severity: "Review",
            status: "Open",
            owner: "Jon",
            evidence: "",
            detail:
              "Review the chapter with the agreed assistive-reading workflow. Document the method and result; this prototype does not run a reader or certify accessibility.",
          },
        ],
      },
    ],
  }),
);
const selectedId = ref("f1");
const filter = ref("All findings");
const evidence = ref("");
const owner = ref("Maya");
const error = ref("");
const versionLabel = ref("");
const versionError = ref("");
const versionDialog = ref<HTMLDialogElement | null>(null);
const reviewDialog = ref<HTMLDialogElement | null>(null);
const version = computed(
  () =>
    state.value.versions.find(
      (item) => item.id === state.value.activeVersion,
    ) ?? state.value.versions[0]!,
);
const selected = computed(
  () =>
    version.value.findings.find((item) => item.id === selectedId.value) ??
    version.value.findings[0]!,
);
const visible = computed(() =>
  version.value.findings.filter(
    (item) =>
      filter.value === "All findings" ||
      (filter.value === "Open"
        ? item.status === "Open"
        : item.source === "Human check"),
  ),
);
const openCount = computed(
  () => version.value.findings.filter((item) => item.status === "Open").length,
);
const manualDone = computed(
  () =>
    version.value.findings.filter(
      (item) => item.source === "Human check" && item.status === "Resolved",
    ).length,
);
const manualTotal = computed(
  () =>
    version.value.findings.filter((item) => item.source === "Human check")
      .length,
);
const progress = computed(() =>
  Math.round(
    (100 * (version.value.findings.length - openCount.value)) /
      version.value.findings.length,
  ),
);
const files = computed(() => [
  ...new Set(version.value.findings.map((item) => item.file)),
]);
watch(state, (value) => props.api.save(value), { deep: true });
watch(
  selected,
  (item) => {
    evidence.value = item.evidence;
    owner.value = item.owner;
    error.value = "";
  },
  { immediate: true },
);

function inputValue(event: Event): string {
  return (event.target as HTMLInputElement).value;
}
function selectVersion(event: Event): void {
  state.value.activeVersion = Number(inputValue(event));
  selectedId.value = version.value.findings[0]?.id ?? "";
}
function saveEvidence(event: Event): void {
  event.preventDefault();
  if (evidence.value.trim().length < 12) {
    error.value =
      "Describe the correction or review method in at least 12 characters.";
    return;
  }
  selected.value.evidence = evidence.value.trim();
  selected.value.owner = owner.value;
  selected.value.status = "Resolved";
  version.value.reviewed = false;
  error.value = "";
  props.api.toast("Evidence saved for this proof. No EPUB file was changed.");
}
function reopen(): void {
  selected.value.status = "Open";
  version.value.reviewed = false;
  props.api.toast("Finding reopened; client review needs refreshing.");
}
function importSample(): void {
  if (version.value.imported) return;
  version.value.findings.push({
    id: `f5-v${version.value.id}`,
    title: "Navigation label needs review",
    file: "nav.xhtml",
    location: "Contents · entry 3",
    source: "Ace sample",
    severity: "Moderate",
    status: "Open",
    owner: "Maya",
    evidence: "",
    detail:
      "Supplied sample finding: a navigation entry has an empty accessible name. Confirm the intended label against the actual book.",
  });
  version.value.imported = true;
  version.value.reviewed = false;
  props.api.toast(
    "One supplied Ace-style finding added locally. No checker ran.",
  );
}
function openVersion(): void {
  versionLabel.value = "";
  versionError.value = "";
  versionDialog.value?.showModal();
}
function createVersion(event: Event): void {
  event.preventDefault();
  const label = versionLabel.value.trim();
  if (
    !label ||
    state.value.versions.some(
      (item) => item.label.toLowerCase() === label.toLowerCase(),
    )
  ) {
    versionError.value = "Enter a new, unique proof label.";
    return;
  }
  const id = Math.max(...state.value.versions.map((item) => item.id)) + 1;
  const findings = version.value.findings.map((item) => ({
    ...item,
    status: "Open" as const,
    evidence: "",
  }));
  state.value.versions.push({
    id,
    label,
    imported: version.value.imported,
    reviewed: false,
    findings,
  });
  state.value.activeVersion = id;
  versionDialog.value?.close();
  props.api.toast(
    "New proof created. Earlier evidence is preserved; this proof needs review.",
  );
}
function recordReview(): void {
  if (openCount.value > 0) return;
  version.value.reviewed = true;
  reviewDialog.value?.close();
  props.api.toast(
    "Client review recorded in this simulation; no approval was sent.",
  );
}
function exportPacket(): void {
  props.api.download(
    `field-notes-proof-${version.value.id}.json`,
    JSON.stringify(
      {
        sample: true,
        publication: "Field Notes on Small Places",
        exported: props.api.today,
        scope:
          "Review evidence only; not a certification or an EPUB validation result.",
        version: version.value,
      },
      null,
      2,
    ),
    "application/json",
  );
}
</script>

<template>
  <div data-product="epub">
    <header class="workspace-heading">
      <div>
        <p class="eyebrow">Proofroom · publication review</p>
        <h1 class="page-title">Make every fix traceable.</h1>
        <p class="page-description">
          Bring findings, human judgment, and client review into one versioned
          packet.
        </p>
      </div>
      <div class="actions">
        <button class="btn secondary" @click="exportPacket">
          Export review packet</button
        ><button class="btn primary" @click="openVersion">
          New proof version
        </button>
      </div>
    </header>
    <section class="epub-publication panel">
      <div class="epub-cover" aria-hidden="true">
        <span>FIELD<br />NOTES</span><small>ON SMALL PLACES</small>
      </div>
      <div class="epub-publication-copy">
        <p class="eyebrow">Northline Press · synthetic publication</p>
        <h2>Field Notes on Small Places</h2>
        <p class="muted">A. Ellis · English · 12 chapters</p>
        <label class="field"
          >Review version<select
            class="select"
            :value="state.activeVersion"
            @change="selectVersion"
          >
            <option
              v-for="item in state.versions"
              :key="item.id"
              :value="item.id"
            >
              {{ item.label }}
            </option>
          </select></label
        >
      </div>
      <div class="epub-summary">
        <strong>{{ progress }}%</strong
        ><span class="muted">findings resolved</span
        ><progress
          :value="progress"
          max="100"
          aria-label="Findings resolved"
        ></progress
        ><span class="small"
          >{{ openCount }} open · {{ manualDone }}/{{ manualTotal }} human
          checks</span
        ><span v-if="version.reviewed" class="badge success"
          >Client review recorded · simulated</span
        >
      </div>
    </section>
    <div class="epub-workbench">
      <aside class="panel epub-outline" aria-label="Publication outline">
        <div class="panel-header"><h2>Publication outline</h2></div>
        <div class="panel-body stack">
          <button
            v-for="file in files"
            :key="file"
            class="epub-file"
            :class="{ selected: selected.file === file }"
            @click="
              selectedId =
                version.findings.find((item) => item.file === file)?.id ??
                selectedId
            "
          >
            <span class="mono">{{ file }}</span
            ><span class="badge neutral">{{
              version.findings.filter(
                (item) => item.file === file && item.status === "Open",
              ).length
            }}</span>
          </button>
          <p class="small muted">
            Locations come from supplied sample findings. No publication is
            uploaded.
          </p>
          <button
            class="btn secondary small"
            :disabled="version.imported"
            @click="importSample"
          >
            {{
              version.imported
                ? "Sample findings imported"
                : "Import supplied Ace findings"
            }}
          </button>
        </div>
      </aside>
      <section class="panel epub-findings" aria-label="Review findings">
        <div class="panel-header">
          <h2>Review queue</h2>
          <label class="visually-hidden" for="epub-filter"
            >Filter findings</label
          ><select
            id="epub-filter"
            class="select"
            :value="filter"
            @change="filter = inputValue($event)"
          >
            <option>All findings</option>
            <option>Open</option>
            <option>Human checks</option>
          </select>
        </div>
        <div class="epub-finding-list">
          <button
            v-for="item in visible"
            :key="item.id"
            class="epub-finding"
            :class="{ selected: selected.id === item.id }"
            @click="selectedId = item.id"
          >
            <span class="epub-finding-meta"
              ><span
                class="badge"
                :class="
                  item.status === 'Resolved'
                    ? 'success'
                    : item.source === 'Human check'
                      ? 'info'
                      : 'warning'
                "
                >{{
                  item.status === "Resolved" ? "Resolved" : item.severity
                }}</span
              ><span class="small muted">{{ item.source }}</span></span
            ><strong>{{ item.title }}</strong
            ><span class="small muted">{{ item.file }} · {{ item.owner }}</span>
          </button>
          <div v-if="visible.length === 0" class="empty-state">
            <h3>No open findings</h3>
            <p>Review the packet before recording a client decision.</p>
          </div>
        </div>
        <div class="panel-body">
          <button class="btn secondary" @click="reviewDialog?.showModal()">
            Prepare client review
          </button>
        </div>
      </section>
      <section class="panel epub-detail" aria-label="Finding detail">
        <div class="panel-header">
          <div>
            <p class="eyebrow">
              {{ selected.source }} · {{ selected.location }}
            </p>
            <h2>{{ selected.title }}</h2>
          </div>
        </div>
        <div class="panel-body stack">
          <p>{{ selected.detail }}</p>
          <div class="epub-excerpt">
            <p class="eyebrow">Publication context · sample</p>
            <h3>A place is more than a point.</h3>
            <p>
              The map follows the river from the old footbridge toward the
              gardens.
            </p>
            <p class="mono small">{{ selected.file }}</p>
          </div>
          <form class="stack" novalidate @submit="saveEvidence">
            <label class="field"
              >Review owner<select
                class="select"
                :value="owner"
                @change="owner = inputValue($event)"
              >
                <option>Maya</option>
                <option>Jon</option>
                <option>Leah</option>
              </select></label
            ><label class="field"
              >Correction or review evidence<textarea
                class="textarea"
                rows="4"
                :value="evidence"
                :aria-invalid="Boolean(error)"
                aria-describedby="epub-evidence-error"
                placeholder="Record what changed, where, and how it was checked…"
                @input="evidence = inputValue($event)"
              ></textarea>
            </label>
            <p
              v-if="error"
              id="epub-evidence-error"
              role="alert"
              class="epub-error"
            >
              {{ error }}
            </p>
            <div class="actions">
              <button class="btn primary" type="submit">
                Save evidence &amp; resolve</button
              ><button
                v-if="selected.status === 'Resolved'"
                class="btn ghost"
                type="button"
                @click="reopen"
              >
                Reopen finding
              </button>
            </div>
          </form>
          <p class="small muted">
            A resolved item records your evidence. It does not establish
            accessibility compliance.
          </p>
        </div>
      </section>
    </div>
    <dialog
      ref="versionDialog"
      class="modal"
      aria-labelledby="epub-version-title"
    >
      <form novalidate @submit="createVersion">
        <div class="modal-header">
          <h2 id="epub-version-title">Create a new proof</h2>
          <button
            class="icon-button"
            type="button"
            aria-label="Close new proof"
            @click="versionDialog?.close()"
          >
            ×
          </button>
        </div>
        <div class="modal-body stack">
          <p>
            Earlier evidence stays with its proof. Every finding reopens for
            this version.
          </p>
          <label class="field"
            >Proof label<input
              class="input"
              :value="versionLabel"
              :aria-invalid="Boolean(versionError)"
              placeholder="Proof 02"
              @input="versionLabel = inputValue($event)"
          /></label>
          <p v-if="versionError" role="alert" class="epub-error">
            {{ versionError }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            class="btn secondary"
            type="button"
            @click="versionDialog?.close()"
          >
            Cancel</button
          ><button class="btn primary" type="submit">Create proof</button>
        </div>
      </form>
    </dialog>
    <dialog
      ref="reviewDialog"
      class="modal"
      aria-labelledby="epub-review-title"
    >
      <div class="modal-header">
        <h2 id="epub-review-title">Client review packet</h2>
        <button
          class="icon-button"
          aria-label="Close client review"
          @click="reviewDialog?.close()"
        >
          ×
        </button>
      </div>
      <div class="modal-body stack">
        <p>
          <strong>{{ version.label }}</strong> ·
          {{ version.findings.length }} findings · {{ openCount }} unresolved
        </p>
        <div class="callout" :class="openCount ? 'warning' : 'success'">
          {{
            openCount
              ? "Resolve the findings and finish human checks before recording review."
              : "All listed checks have evidence. The client still decides whether this proof is acceptable."
          }}
        </div>
        <ul>
          <li v-for="item in version.findings" :key="item.id">
            {{ item.title }} — {{ item.status }}
          </li>
        </ul>
        <p class="small muted">
          This local simulation records review only. No signature, email,
          certification, or client access is created.
        </p>
      </div>
      <div class="modal-footer">
        <button class="btn secondary" @click="exportPacket">
          Export review packet</button
        ><button
          class="btn primary"
          :disabled="openCount > 0 || version.reviewed"
          @click="recordReview"
        >
          {{
            version.reviewed
              ? "Review already recorded"
              : "Record simulated client review"
          }}
        </button>
      </div>
    </dialog>
  </div>
</template>
