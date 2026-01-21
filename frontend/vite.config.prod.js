import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import fs from "fs";
import path from "path";

// Read version from root package.json
const packageJsonPath = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
  "package.json",
);
const packageJson = fs.readFileSync(packageJsonPath, "utf-8");
const { version } = JSON.parse(packageJson);

export default defineConfig({
  base: '/WebShareee/', // Absolute base path for sub-directory deployment
  define: {
    __APP_VERSION__: JSON.stringify(version),
  },
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  // No proxy needed for deployment build usually
});
