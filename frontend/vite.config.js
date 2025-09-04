import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

// Read version from root package.json
const packageJsonPath = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'package.json');
const packageJson = fs.readFileSync(packageJsonPath, 'utf-8');
const { version } = JSON.parse(packageJson);

export default defineConfig({
  define: {
    '__APP_VERSION__': JSON.stringify(version),
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 8080, // Set frontend port
    proxy: {
      '/api': {
        target: 'http://localhost:8700', // Backend FastAPI
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
      '/p': {
        target: 'http://localhost:8700', // Backend FastAPI
        changeOrigin: true,
        // No rewrite needed, path should be passed as is
      },
    },
  },
})