<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref } from "vue";
import { Button } from "@wow-two-beta/ui-vue/presentation/actions";
import { useMediaQuery } from "@wow-two-beta/ui-vue/foundation/device";
import { products } from "./Catalog";
import Icon from "./shared/Icon.vue";
import type { PrototypeApi } from "./shared/PrototypeApi";

const palettes = [
  {
    id: "mist",
    name: "Mist",
    note: "Cool, focused workspace",
    color: "#eff3f7",
  },
  {
    id: "paper",
    name: "Paper",
    note: "Warm editorial canvas",
    color: "#f6f2ea",
  },
  {
    id: "mono",
    name: "Porcelain",
    note: "Neutral, minimal canvas",
    color: "#f4f4f4",
  },
];
const route = ref(location.hash.slice(1) || "home");
const dark = ref(false);
const palette = ref("mist");
const sidebarOpen = ref(false);
const reviewOpen = ref(false);
const scenario = ref("populated");
const revision = ref(0);
const message = ref("");
const toastKind = ref("success");
const toastTimer = ref<ReturnType<typeof setTimeout> | undefined>();
const resetDialog = ref<HTMLDialogElement | null>(null);
const sidebar = ref<HTMLElement | null>(null);
const menuButton = ref<HTMLButtonElement | null>(null);
const closeMenuButton = ref<HTMLButtonElement | null>(null);
const isPhone = useMediaQuery("(max-width: 767px)");
const product = computed(() =>
  products.find((item) => item.slug === route.value),
);
const currentIndex = computed(() =>
  products.findIndex((item) => item.slug === route.value),
);
const accent = computed(() => product.value?.accent ?? "#12685c");
const api = computed<PrototypeApi>(() => {
  const key = `wow2-first-ten-v1:${product.value?.slug ?? "home"}`;
  return {
    state<T>(initial: T): T {
      try {
        const saved = localStorage.getItem(key);
        if (saved) {
          const parsed: unknown = JSON.parse(saved);
          if (compatibleTopLevel(parsed, initial)) return parsed as T;
          toast(
            "Saved sample data has an incompatible shape. The starting sample is shown.",
            "warning",
          );
        }
      } catch {
        toast(
          "Saved sample data could not be read. The starting sample is shown.",
          "warning",
        );
      }
      return JSON.parse(JSON.stringify(initial)) as T;
    },
    save(state: unknown): void {
      try {
        localStorage.setItem(key, JSON.stringify(state));
      } catch {
        toast(
          "Browser storage is unavailable. This session still works; export to keep your changes.",
          "warning",
        );
      }
    },
    toast,
    download(filename: string, contents: string, mime = "text/plain"): void {
      const url = URL.createObjectURL(new Blob([contents], { type: mime }));
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      toast(`Export prepared: ${filename}. Sample data only.`);
    },
    money: (value: number) =>
      new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 2,
      }).format(value),
    today: "2026-09-29",
    navigate,
  };
});

onMounted(() => {
  window.addEventListener("hashchange", syncRoute);
  window.addEventListener("keydown", handleNavigationKey);
});
onUnmounted(() => {
  window.removeEventListener("hashchange", syncRoute);
  window.removeEventListener("keydown", handleNavigationKey);
  if (toastTimer.value) clearTimeout(toastTimer.value);
});

function navigate(slug: string): void {
  location.hash = slug;
}
function syncRoute(): void {
  route.value = location.hash.slice(1) || "home";
  if (sidebarOpen.value) closeNavigation();
  scenario.value = "populated";
  message.value = "";
  window.scrollTo({ top: 0 });
}
function toast(
  text: string,
  kind: "success" | "error" | "info" | "warning" = "success",
): void {
  message.value = text;
  toastKind.value = kind;
  if (toastTimer.value) clearTimeout(toastTimer.value);
  toastTimer.value = setTimeout(() => {
    message.value = "";
  }, 7000);
}
function changeScenario(event: Event): void {
  scenario.value = (event.target as HTMLSelectElement).value;
}
function reset(): void {
  try {
    localStorage.removeItem(
      `wow2-first-ten-v1:${product.value?.slug ?? "home"}`,
    );
  } catch {
    toast("Storage could not be cleared.", "error");
    return;
  }
  revision.value++;
  scenario.value = "populated";
  resetDialog.value?.close();
  toast("This product’s sample data has been restored.");
}
function next(): void {
  navigate(products[(currentIndex.value + 1) % products.length]!.slug);
}
function skipToMain(): void {
  document.getElementById("main-workspace")?.focus();
}
function compatibleTopLevel(candidate: unknown, initial: unknown): boolean {
  if (
    !candidate ||
    typeof candidate !== "object" ||
    Array.isArray(candidate) ||
    !initial ||
    typeof initial !== "object"
  )
    return false;
  const saved = candidate as Record<string, unknown>;
  return Object.entries(initial).every(([key, value]) => {
    const actual = saved[key];
    if (Array.isArray(value)) return Array.isArray(actual);
    if (value === null) return actual === null || typeof actual === "object";
    if (typeof value === "number")
      return typeof actual === "number" && Number.isFinite(actual);
    return actual !== undefined && typeof actual === typeof value;
  });
}
async function openNavigation(): Promise<void> {
  sidebarOpen.value = true;
  await nextTick();
  closeMenuButton.value?.focus();
}
function closeNavigation(): void {
  sidebarOpen.value = false;
  void nextTick(() => menuButton.value?.focus());
}
function cardAccent(color: string): string {
  return dark.value ? `color-mix(in srgb, ${color} 48%, #eaf3ee)` : color;
}
function handleNavigationKey(event: KeyboardEvent): void {
  if (!sidebarOpen.value || !isPhone.value) return;
  if (event.key === "Escape") {
    event.preventDefault();
    closeNavigation();
    return;
  }
  if (event.key !== "Tab") return;
  const items = sidebar.value?.querySelectorAll<HTMLElement>(
    "a[href],button:not([disabled])",
  );
  if (!items?.length) return;
  const first = items[0],
    last = items[items.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last?.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first?.focus();
  }
}
</script>

<template>
  <div
    class="lab"
    :data-theme="dark ? 'dark' : 'light'"
    :data-palette="palette"
    :style="{
      '--accent-fill': accent,
      '--accent': dark ? `color-mix(in srgb, ${accent} 48%, #eaf3ee)` : accent,
    }"
  >
    <button class="skip-link" @click="skipToMain">Skip to workspace</button>
    <aside
      ref="sidebar"
      class="sidebar"
      :class="{ 'mobile-open': sidebarOpen }"
    >
      <button
        ref="closeMenuButton"
        class="icon-button menu-close"
        aria-label="Close product navigation"
        @click="closeNavigation"
      >
        <Icon name="x" />
      </button>
      <a class="brand" href="#home"
        ><span class="brand-mark">w<span>²</span></span
        ><span>Product lab<small>THE FIRST TEN</small></span></a
      >
      <a href="#home" class="overview-link" :class="{ active: !product }"
        ><Icon name="home" /> Overview <span>10</span></a
      >
      <p class="nav-label">EXPLORE A WORKFLOW</p>
      <nav aria-label="Product prototypes">
        <a
          v-for="(item, index) in products"
          :key="item.slug"
          :href="`#${item.slug}`"
          :class="{ active: route === item.slug }"
          :aria-current="route === item.slug ? 'page' : undefined"
        >
          <span class="nav-icon" :style="{ color: cardAccent(item.accent) }"
            ><Icon :name="item.icon"
          /></span>
          <span>{{ item.short }}</span
          ><span class="nav-number">{{
            String(index + 1).padStart(2, "0")
          }}</span>
        </a>
      </nav>
      <div class="sidebar-bottom">
        <span class="status-dot"></span> Local concept lab
        <p>Sample data · Sep 29, 2026<br />Nothing is sent to customers.</p>
      </div>
    </aside>
    <div
      v-if="sidebarOpen && isPhone"
      class="nav-shade"
      @click="closeNavigation"
    ></div>
    <div class="main-column" :inert="sidebarOpen && isPhone">
      <header class="topbar">
        <button
          ref="menuButton"
          class="icon-button menu-toggle"
          aria-label="Open product navigation"
          :aria-expanded="sidebarOpen"
          @click="openNavigation"
        >
          <Icon name="layers" />
        </button>
        <div class="breadcrumb">
          <span>WoW2</span><span>/</span
          ><strong>{{ product?.short ?? "First ten" }}</strong
          ><span class="prototype-label">PROTOTYPE</span>
        </div>
        <div class="topbar-actions">
          <button
            class="icon-button"
            :aria-label="
              dark ? 'Switch to light theme' : 'Switch to dark theme'
            "
            @click="dark = !dark"
          >
            <Icon :name="dark ? 'sun' : 'moon'" />
          </button>
          <Button class="btn secondary small" @click="reviewOpen = !reviewOpen"
            ><Icon name="settings" />
            <span>{{
              reviewOpen ? "Close review" : "Design review"
            }}</span></Button
          >
        </div>
      </header>
      <div v-if="reviewOpen" class="review-tray">
        <div>
          <p class="eyebrow">DESIGN PROPOSALS · NOT LOCKED</p>
          <h2>Change the canvas. Keep the workflow.</h2>
          <p class="small muted">
            Three in-context palette proposals. Layout and product accent stay
            constant.
          </p>
        </div>
        <div class="palette-options">
          <button
            v-for="item in palettes"
            :key="item.id"
            class="palette-card"
            :class="{ selected: palette === item.id }"
            :aria-pressed="palette === item.id"
            @click="palette = item.id"
          >
            <span class="palette-preview" :style="{ background: item.color }"
              ><span></span><i :style="{ background: accent }"></i
              ><span></span></span
            ><strong>{{ item.name }}</strong
            ><small>{{ item.note }}</small>
          </button>
        </div>
        <div v-if="product" class="review-notes grid-2">
          <div>
            <p class="eyebrow">LAYOUT RATIONALE</p>
            <p>{{ product.layout }}</p>
          </div>
          <div>
            <p class="eyebrow">HUMAN DECISION</p>
            <p>{{ product.decision }}</p>
          </div>
          <div>
            <p class="eyebrow">FIRST PRODUCTION SLICE</p>
            <p>{{ product.build }}</p>
          </div>
          <div>
            <p class="eyebrow">COMPETITIVE TEST</p>
            <p>{{ product.risk }}</p>
          </div>
        </div>
      </div>
      <main id="main-workspace" tabindex="-1">
        <template v-if="!product">
          <section class="hub-hero">
            <div>
              <p class="eyebrow">TEN SMALL PRODUCTS. ONE CLEAR STANDARD.</p>
              <h1>Useful work.<br /><span>Quiet software.</span></h1>
              <p class="hero-copy">
                A working concept for each of our first ten ideas. Explore the
                task, make a decision, and see what changes.
              </p>
              <a href="#retainer" class="btn primary"
                >Start with Retainer <Icon name="arrow-right"
              /></a>
            </div>
            <div class="hero-note">
              <p class="eyebrow">THE PRODUCT PHILOSOPHY</p>
              <blockquote>
                Get The Work Done<br />&amp; Never Bother Me.
              </blockquote>
              <div class="divider"></div>
              <p>
                One outcome people can recognize.<br />Evidence before
                “done.”<br />Reminders only by choice.
              </p>
              <span class="badge neutral">Interactive research · v0.1</span>
            </div>
          </section>
          <div class="hub-section-heading">
            <div>
              <p class="eyebrow">THE CONFIRMED TEN</p>
              <h2>Choose a problem to solve</h2>
            </div>
            <p class="small muted">Proposed monthly prices · unvalidated</p>
          </div>
          <div class="product-grid">
            <a
              v-for="(item, index) in products"
              :key="item.slug"
              :href="`#${item.slug}`"
              class="product-card"
              :style="{ '--card-accent': cardAccent(item.accent) }"
            >
              <div class="product-card-top">
                <span class="product-symbol"
                  ><Icon :name="item.icon" :size="23" /></span
                ><span class="card-index"
                  >{{ String(index + 1).padStart(2, "0") }} /
                  {{ item.id }}</span
                >
              </div>
              <p class="eyebrow">{{ item.audience }}</p>
              <h3>{{ item.name }}</h3>
              <p class="card-promise">{{ item.promise }}</p>
              <div class="card-bottom">
                <span>${{ item.price }}<small>/mo hypothesis</small></span
                ><span class="card-open"
                  >Explore <Icon name="arrow-right" :size="16"
                /></span>
              </div>
            </a>
          </div>
          <section class="hub-footnote">
            <Icon name="alert" />
            <div>
              <strong>Concepts, not launched services.</strong>
              <p>
                All records are synthetic. Changes stay in this browser. Email,
                payments, monitoring, CI execution, and external approvals are
                simulated. Export sample work before resetting it.
              </p>
            </div>
          </section>
        </template>
        <template v-else>
          <div class="prototype-tools">
            <span
              ><span class="status-dot"></span> Synthetic workspace · changes
              saved on this browser</span
            >
            <div class="actions">
              <label class="scenario-label"
                >Preview state
                <select
                  aria-label="Preview state"
                  :value="scenario"
                  @change="changeScenario"
                >
                  <option value="populated">Working sample</option>
                  <option value="empty">First visit</option>
                  <option value="loading">Loading</option>
                  <option value="error">Connection error</option>
                </select></label
              ><button
                class="btn ghost small"
                @click="resetDialog?.showModal()"
              >
                <Icon name="reset" :size="15" /> Reset sample
              </button>
            </div>
          </div>
          <component
            :is="product.component"
            v-if="scenario === 'populated'"
            :key="`${product.slug}:${revision}`"
            :api="api"
          />
          <section
            v-else-if="scenario === 'empty'"
            class="scenario-panel empty-state"
          >
            <span class="scenario-icon"
              ><Icon :name="product.icon" :size="30"
            /></span>
            <p class="eyebrow">{{ product.name }}</p>
            <h1>Your first useful result starts here.</h1>
            <p>{{ product.promise }}</p>
            <div class="callout info">{{ product.workflow }}</div>
            <button class="btn primary" @click="scenario = 'populated'">
              Explore with sample data <Icon name="arrow-right" />
            </button>
            <p class="small muted">
              First-visit design preview. Your saved sample work is preserved.
            </p>
          </section>
          <section
            v-else-if="scenario === 'loading'"
            class="scenario-panel"
            aria-busy="true"
          >
            <p class="eyebrow">STATE PREVIEW</p>
            <h1>Loading {{ product.short.toLowerCase() }}…</h1>
            <p class="muted">Keep your place while records arrive.</p>
            <div class="skeleton-row"></div>
            <div class="skeleton-row"></div>
            <div class="skeleton-row short"></div>
            <button class="btn secondary" @click="scenario = 'populated'">
              Finish loading preview
            </button>
          </section>
          <section v-else class="scenario-panel empty-state">
            <span class="scenario-icon"><Icon name="alert" :size="30" /></span>
            <p class="eyebrow">STATE PREVIEW</p>
            <h1>We couldn’t load the latest records.</h1>
            <p>
              Your saved work is still here. Nothing was submitted or
              overwritten.
            </p>
            <button class="btn primary" @click="scenario = 'populated'">
              Retry sample connection
            </button>
            <p class="small muted">
              Simulated connection error; this prototype runs locally.
            </p>
          </section>
          <footer class="product-footer">
            <span>{{ product.id }} · {{ product.boundary }}</span
            ><button class="btn ghost small" @click="next">
              Next prototype <Icon name="arrow-right" :size="16" />
            </button>
          </footer>
        </template>
      </main>
    </div>
    <div
      v-if="message"
      class="toast"
      :class="toastKind"
      role="status"
      aria-live="polite"
    >
      <Icon
        :name="
          toastKind === 'error' || toastKind === 'warning' ? 'alert' : 'check'
        "
      /><span>{{ message }}</span
      ><button
        class="icon-button"
        aria-label="Dismiss notification"
        @click="message = ''"
      >
        <Icon name="x" :size="16" />
      </button>
    </div>
    <dialog ref="resetDialog" class="modal" aria-labelledby="reset-title">
      <div class="modal-header">
        <h2 id="reset-title">Restore sample data?</h2>
        <button
          class="icon-button"
          aria-label="Close reset dialog"
          @click="resetDialog?.close()"
        >
          <Icon name="x" />
        </button>
      </div>
      <div class="modal-body">
        <p>
          This resets only {{ product?.short }} in this browser. Export your
          sample work first if you want to keep it.
        </p>
      </div>
      <div class="modal-footer">
        <button class="btn secondary" @click="resetDialog?.close()">
          Keep my changes</button
        ><button class="btn danger" @click="reset">
          Restore original sample
        </button>
      </div>
    </dialog>
  </div>
</template>
