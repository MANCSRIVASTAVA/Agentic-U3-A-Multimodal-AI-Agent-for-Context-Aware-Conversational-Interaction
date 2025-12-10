import { defineConfig } from '@playwright/test'
export default defineConfig({
  testDir: 'src/test/e2e',
  use: { baseURL: 'http://localhost:5173', headless: true }
})
