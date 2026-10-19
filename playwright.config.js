import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tests",
  testMatch: /lab\.spec\.js/,
  timeout: 60000,
  use: { baseURL: "http://127.0.0.1:8765" },
  webServer: {
    command: "python3 -m http.server 8765",
    url: "http://127.0.0.1:8765/index.html",
    reuseExistingServer: true,
  },
  projects: [
    { name: "desktop", use: { viewport: { width: 1440, height: 900 } } },
    { name: "phone", use: { viewport: { width: 390, height: 844 }, isMobile: true } },
  ],
});
