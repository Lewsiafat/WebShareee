import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
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