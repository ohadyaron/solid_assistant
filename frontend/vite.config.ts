import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['occt-import-js'], // Don't pre-bundle occt-import-js to avoid WASM issues
  },
  build: {
    commonjsOptions: {
      include: [/occt-import-js/, /node_modules/],
    },
  },
  server: {
    headers: {
      // Enable SharedArrayBuffer for WASM
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
    },
  },
})
