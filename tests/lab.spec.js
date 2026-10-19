import { test, expect } from "@playwright/test";

async function dismiss(page) {
  const skip = page.locator("[data-tour-skip]");
  if (await skip.isVisible().catch(() => false)) await skip.click();
  const dock = page.getByRole("button", { name: "Dock the monkey" });
  if (await dock.isVisible().catch(() => false)) await dock.click();
  const splash = page.locator("[data-splash-ok]");
  if (await splash.isVisible().catch(() => false)) await splash.click();
}

test("home, guide chat, and a lesson", async ({ page }, info) => {
  const size = info.project.name;
  await page.goto("/index.html");
  await dismiss(page);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await page.screenshot({ path: `docs/screenshots/home-${size}.png`, fullPage: false });
  await page.locator("#monkey-dock").click();
  await expect(page.locator("[data-aibot] .py-chat")).toBeVisible();
  await page.locator("#py-chat-input").fill("what can you help with");
  await page.locator(".py-chat-form button[type=submit]").click();
  await expect(page.locator(".py-chat-log")).toContainText("Model Context Protocol");
  await page.screenshot({ path: `docs/screenshots/bot-${size}.png` });
  await page.goto("/rooms/T2-R1.html");
  await dismiss(page);
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Tokens");
  await page.screenshot({ path: `docs/screenshots/lesson-${size}.png` });
});

test("short phone keeps the chat input and Send in view", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 430 });
  await page.goto("/index.html");
  await dismiss(page);
  await page.locator("#monkey-dock").click();
  const input = page.locator("#py-chat-input");
  const send = page.locator(".py-chat-form button[type=submit]");
  await expect(input).toBeVisible();
  await expect(send).toBeVisible();
  const hit = await page.evaluate(() => {
    function exposed(selector) {
      const node = document.querySelector(selector);
      const rect = node.getBoundingClientRect();
      const inside = rect.top >= 0 && rect.bottom <= window.innerHeight && rect.left >= 0 && rect.right <= window.innerWidth;
      const top = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
      return { inside, covered: !(top === node || node.contains(top)) };
    }
    return { input: exposed("#py-chat-input"), send: exposed(".py-chat-form button[type=submit]") };
  });
  expect(hit.input.inside).toBe(true);
  expect(hit.input.covered).toBe(false);
  expect(hit.send.inside).toBe(true);
  expect(hit.send.covered).toBe(false);
});

test("offline reload still opens a lesson and the chat", async ({ page, context }) => {
  await page.goto("/index.html");
  await dismiss(page);
  await page.evaluate(async () => {
    const ready = await navigator.serviceWorker.ready;
    await ready.update();
  });
  await page.reload();
  await dismiss(page);
  await context.setOffline(true);
  await page.reload();
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await page.goto("/rooms/T2-R1.html");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Tokens");
  await page.locator("#monkey-dock").click();
  await page.locator("#py-chat-input").fill("what is a token");
  await page.locator(".py-chat-form button[type=submit]").click();
  await expect(page.locator(".py-chat-log")).toContainText(/token/i);
  await context.setOffline(false);
});
