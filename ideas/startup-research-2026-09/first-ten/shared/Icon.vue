<script setup lang="ts">
import { computed } from "vue";
import {
  Wallet,
  Code2,
  Inbox,
  BookOpen,
  Users,
  FileText,
  Flag,
  CalendarDays,
  Layers,
  Mic,
  ArrowRight,
  Check,
  Plus,
  Search,
  Download,
  ChevronDown,
  X,
  Sun,
  Moon,
  Play,
  Bell,
  Settings2,
  Home,
  ExternalLink,
  RotateCcw,
  TriangleAlert,
  Clock3,
} from "lucide-vue-next";

const props = defineProps<{ name: string; size?: number }>();
const icons = {
  wallet: Wallet,
  code: Code2,
  inbox: Inbox,
  book: BookOpen,
  users: Users,
  file: FileText,
  flag: Flag,
  calendar: CalendarDays,
  layers: Layers,
  mic: Mic,
  "arrow-right": ArrowRight,
  check: Check,
  plus: Plus,
  search: Search,
  download: Download,
  chevron: ChevronDown,
  x: X,
  sun: Sun,
  moon: Moon,
  play: Play,
  bell: Bell,
  settings: Settings2,
  home: Home,
  external: ExternalLink,
  reset: RotateCcw,
  alert: TriangleAlert,
  clock: Clock3,
};
const icon = computed(
  () => icons[props.name as keyof typeof icons] ?? FileText,
);
</script>

<template>
  <component
    :is="icon"
    :size="size ?? 18"
    :stroke-width="1.7"
    aria-hidden="true"
  />
</template>
