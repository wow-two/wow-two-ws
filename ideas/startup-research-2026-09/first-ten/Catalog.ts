import type { Component } from "vue";
import Retainer from "./products/retainer/Product.vue";
import Docs from "./products/docs/Product.vue";
import Files from "./products/files/Product.vue";
import Procedures from "./products/procedures/Product.vue";
import Training from "./products/training/Product.vue";
import Epub from "./products/epub/Product.vue";
import Promises from "./products/promises/Product.vue";
import Renewals from "./products/renewals/Product.vue";
import Config from "./products/config/Product.vue";
import Podcast from "./products/podcast/Product.vue";

export interface Product {
  slug: string;
  id: string;
  name: string;
  short: string;
  icon: string;
  accent: string;
  audience: string;
  promise: string;
  price: number;
  workflow: string;
  layout: string;
  decision: string;
  boundary: string;
  build: string;
  risk: string;
  component: Component;
}

export const products: Product[] = [
  {
    slug: "retainer",
    id: "W0252",
    name: "Retainer balance tracker",
    short: "Retainer",
    icon: "wallet",
    accent: "#12685c",
    audience: "Small agencies & fractional teams",
    promise: "Know what is left before the next request arrives.",
    price: 39,
    workflow:
      "Import time → reconcile → request extra hours → export statement",
    layout:
      "A live allowance ledger beside the client statement connects every entry to its consequence.",
    decision:
      "The agency reconciles time; the client explicitly approves extra allowance.",
    boundary:
      "No automatic invoicing, client messages, payment collection, or invented approvals.",
    build: "CSV import, allowance ledger, approval receipt, period closing.",
    risk: "Harvest and spreadsheets already cover much of this job. Sell the approval workflow.",
    component: Retainer,
  },
  {
    slug: "docs",
    id: "W0012",
    name: "Documentation example tester",
    short: "Docs test",
    icon: "code",
    accent: "#5850b6",
    audience: "Developer-tool maintainers",
    promise: "Catch a broken example before your next user does.",
    price: 39,
    workflow:
      "Inspect failed sample → assign owner → import rerun → review evidence",
    layout:
      "Failure list and code-level evidence share one focused triage view.",
    decision:
      "The maintainer decides whether the code or its documentation needs correction.",
    boundary:
      "Execute only in customer-owned CI; the service receives bounded reports.",
    build:
      "Manifest format, local runner, CI report ingest, failure ownership.",
    risk: "Free test frameworks are strong substitutes. Distribution must begin with CI adoption.",
    component: Docs,
  },
  {
    slug: "files",
    id: "W0031",
    name: "Missing-file monitor",
    short: "File watch",
    icon: "inbox",
    accent: "#2a668a",
    audience: "Operations teams receiving scheduled files",
    promise: "Know which delivery needs a human, without opening every folder.",
    price: 39,
    workflow:
      "Review late delivery → inspect receipt → record arrival or calendar exception",
    layout:
      "Expected delivery windows lead; incident detail preserves the receipt trail.",
    decision:
      "An operator distinguishes an excused absence from a real delivery failure.",
    boundary:
      "Metadata receipts only; no customer file contents or storage credentials.",
    build:
      "Receipt endpoint, explicit UTC pilot schedules, incident lifecycle, opted-in notices.",
    risk: "Cronitor and Healthchecks cover generic jobs. Win on expected-file context.",
    component: Files,
  },
  {
    slug: "procedures",
    id: "W0263",
    name: "Procedure review tracker",
    short: "Procedure review",
    icon: "book",
    accent: "#826326",
    audience: "Small operations teams with existing wikis",
    promise: "Keep the instructions you rely on deliberately current.",
    price: 29,
    workflow:
      "Select due procedure → inspect source → record evidence → schedule review",
    layout:
      "A review queue opens an attestation workspace, never a competing document editor.",
    decision:
      "The responsible person reviews the actual procedure and records their judgment.",
    boundary:
      "A recorded review is not regulatory certification or proof the source is correct.",
    build: "URL registry, owner, cadence, version-aware review receipts.",
    risk: "Notion reminders are free enough for many teams. Test handover and audit demand.",
    component: Procedures,
  },
  {
    slug: "training",
    id: "W0289",
    name: "Training seat reconciler",
    short: "Training seats",
    icon: "users",
    accent: "#8b4f78",
    audience: "Independent B2B training providers",
    promise: "Close every cohort with an agreed seat count.",
    price: 59,
    workflow:
      "Import roster → match bookings → resolve substitution → close cohort",
    layout:
      "Purchased and attended seats sit together; exceptions receive the visual emphasis.",
    decision:
      "The provider resolves unmatched names and approves substitutions.",
    boundary:
      "No course hosting, learning grades, automated billing, or attendance surveillance.",
    build:
      "Booking and roster imports, seat allocation, substitutions, reconciliation export.",
    risk: "Arlo and existing LMS products include adjacent workflows. Target providers using spreadsheets.",
    component: Training,
  },
  {
    slug: "epub",
    id: "W0521",
    name: "EPUB review workspace",
    short: "EPUB review",
    icon: "file",
    accent: "#775e98",
    audience: "EPUB production studios & independent publishers",
    promise: "Make every proof review traceable to its evidence.",
    price: 39,
    workflow:
      "Import findings → assign evidence → resolve checks → record proof review",
    layout:
      "Book structure, finding queue, and review evidence form a focused editorial workspace.",
    decision:
      "A human verifies accessibility and reading experience against a specific proof.",
    boundary:
      "Checker findings and client review never imply accessibility certification.",
    build:
      "Ace report import, immutable proof versions, finding ownership, review packet.",
    risk: "Free Ace handles checks. Charge for collaboration, version discipline, and handoff.",
    component: Epub,
  },
  {
    slug: "promises",
    id: "W0276",
    name: "Customer promise tracker",
    short: "Promises",
    icon: "flag",
    accent: "#995641",
    audience: "Small B2B SaaS customer-success teams",
    promise: "Keep accepted customer commitments from disappearing.",
    price: 59,
    workflow:
      "Record commitment → assign owner → resolve blocker → approve customer digest",
    layout:
      "A commitment register puts obligation, owner, due date, and evidence together.",
    decision:
      "An authorized person accepts scope and approves each customer-facing update.",
    boundary:
      "Feature requests never become commitments automatically; no autonomous customer promises.",
    build:
      "Accepted promise record, change history, owner/due date, approved digest export.",
    risk: "CRM and Canny overlap. Validate demand for accepted obligations rather than feedback.",
    component: Promises,
  },
  {
    slug: "renewals",
    id: "W0261",
    name: "Vendor renewal deadline tracker",
    short: "Renewals",
    icon: "calendar",
    accent: "#426d4e",
    audience: "Small teams managing software vendors",
    promise: "Decide while you still have time to act.",
    price: 29,
    workflow:
      "Review notice deadline → record decision → attach evidence → close follow-up",
    layout:
      "A deadline horizon leads into a decision record; contract expiry is secondary.",
    decision:
      "A person verifies terms and performs any cancellation with the vendor.",
    boundary:
      "Dates are user-confirmed; the app never cancels contracts or gives legal assurance.",
    build:
      "Vendor register, verified notice date, decision receipt, notification schedule.",
    risk: "Calendars and procurement suites compete. Deadline ownership must justify a subscription.",
    component: Renewals,
  },
  {
    slug: "config",
    id: "W0034",
    name: "Environment configuration checker",
    short: "Config check",
    icon: "layers",
    accent: "#3e699a",
    audience: "Small engineering teams deploying multiple environments",
    promise: "See unexplained configuration drift before a release.",
    price: 39,
    workflow:
      "Inspect mismatch → explain allowed difference → import new manifest → review release",
    layout:
      "An environment matrix keeps deliberate differences distinct from unresolved drift.",
    decision: "An engineer approves a scoped exception and its expiry.",
    boundary:
      "No raw secrets or low-entropy secret hashes; no changes to deployed configuration.",
    build:
      "Local manifest CLI, presence checks, customer-held keyed comparison, expiring exceptions.",
    risk: "CI scripts are a credible free substitute. Test repeat drift pain before broad integrations.",
    component: Config,
  },
  {
    slug: "podcast",
    id: "W0507",
    name: "Podcast guest readiness tracker",
    short: "Guest ready",
    icon: "mic",
    accent: "#96622b",
    audience: "Podcast producers with recurring guest episodes",
    promise: "Walk into recording with the essentials already settled.",
    price: 29,
    workflow:
      "Review episode → check guest pack → verify permission → prepare handoff",
    layout:
      "Episode readiness wraps a guest checklist and producer handoff, not an audio timeline.",
    decision:
      "The producer verifies supplied assets, permission evidence, and recording readiness.",
    boundary:
      "No recording, transcription, hosting, automatic legal consent, or unsolicited reminders.",
    build:
      "Episode templates, guest submission link, evidence checklist, handoff export.",
    risk: "Forms, calendar, and Drive are strong substitutes. Target producers handling several shows.",
    component: Podcast,
  },
];
