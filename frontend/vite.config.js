
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true
  },
  build: {
    outDir: '../frontend_dist', // за да може Flask да сервира билднатите файлове
    emptyOutDir: true
  }
})