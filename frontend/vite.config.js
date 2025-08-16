import { defineConfig } from 'vite'
import { resolve } from 'path'
import react from '@vitejs/plugin-react'

export default defineConfig({
	server: { 
    host: '0.0.0.0',
    port: 3000 
  },
  preview: { port: 8080 },
  plugins: [react()],
  root: resolve(__dirname, 'src'),
  publicDir: 'public',
  build: {
    outDir: 'build',
  },
  css: {
    preprocessorOptions: {
       scss: {
         silenceDeprecations: [
           'import',
           'mixed-decls',
           'color-functions',
           'global-builtin',
         ],
       },
    },
 },
})
