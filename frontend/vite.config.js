import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

const backend = process.env.BACKEND_URL ?? 'http://localhost:8000'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  // shortcut: 98.css uses `@media (not(hover))`, which lightningcss can't minify; drop if 98.css is replaced.
  build: { cssMinify: false },
  server: {
    proxy: { '/jobs': backend, '/batches': backend },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test-setup.js',
  },
})
