import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwind from "@tailwindcss/vite";

export default defineConfig({
  base: "./",
  plugins: [vue(), tailwind()],
  build: {
    cssCodeSplit: false,
    modulePreload: false,
    assetsInlineLimit: 1000000,
  },
});
