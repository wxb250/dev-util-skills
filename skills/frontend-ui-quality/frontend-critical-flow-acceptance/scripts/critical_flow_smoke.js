#!/usr/bin/env node
"use strict";

const fs = require("fs");

function loadPlaywright() {
  try {
    return require("@playwright/test").chromium;
  } catch {
    return require("playwright").chromium;
  }
}

function usage() {
  console.log(`Usage: node critical_flow_smoke.js <scenario.json>

Scenario shape:
{
  "url": "http://127.0.0.1:3000",
  "viewport": {"width": 1440, "height": 900},
  "steps": [
    {"action": "fill", "selector": "#question", "value": "hello"},
    {"action": "click", "selector": "button[type=submit]"},
    {"action": "waitFor", "selector": ".dialog", "state": "visible"},
    {"action": "assertVisible", "selector": ".dialog"},
    {"action": "assertClickable", "selector": "button.close"}
  ],
  "screenshot": "output/critical-flow.png"
}`);
}

function assertScenario(scenario) {
  if (!scenario || typeof scenario !== "object") throw new Error("scenario must be a JSON object");
  if (!scenario.url) throw new Error("scenario.url is required");
  if (!Array.isArray(scenario.steps)) throw new Error("scenario.steps must be an array");
}

async function assertClickable(page, selector) {
  const locator = page.locator(selector).first();
  await locator.waitFor({ state: "visible" });
  const box = await locator.boundingBox();
  if (!box) throw new Error(`${selector} has no bounding box`);
  const blockedBy = await page.evaluate(
    ({ selector, x, y }) => {
      const element = document.querySelector(selector);
      const hit = document.elementFromPoint(x, y);
      if (!element || !hit) return "missing element or hit target";
      if (hit === element || element.contains(hit) || hit.contains(element)) return "";
      return `${hit.tagName.toLowerCase()}${hit.id ? `#${hit.id}` : ""}${hit.className ? `.${String(hit.className).replace(/\s+/g, ".")}` : ""}`;
    },
    { selector, x: box.x + box.width / 2, y: box.y + box.height / 2 }
  );
  if (blockedBy) throw new Error(`${selector} is blocked by ${blockedBy}`);
}

async function runStep(page, step) {
  const action = step.action;
  if (action === "goto") {
    await page.goto(step.url, { waitUntil: step.waitUntil || "networkidle" });
  } else if (action === "fill") {
    await page.locator(step.selector).fill(step.value || "");
  } else if (action === "click") {
    await page.locator(step.selector).click();
  } else if (action === "waitFor") {
    await page.locator(step.selector).waitFor({ state: step.state || "visible", timeout: step.timeout || 10000 });
  } else if (action === "assertVisible") {
    await page.locator(step.selector).waitFor({ state: "visible", timeout: step.timeout || 10000 });
  } else if (action === "assertText") {
    const text = await page.locator(step.selector).innerText({ timeout: step.timeout || 10000 });
    if (!text.includes(step.text || "")) throw new Error(`${step.selector} does not contain expected text`);
  } else if (action === "assertClickable") {
    await assertClickable(page, step.selector);
  } else if (action === "screenshot") {
    await page.screenshot({ path: step.path, fullPage: step.fullPage !== false });
  } else {
    throw new Error(`Unsupported action: ${action}`);
  }
}

async function main() {
  const scenarioPath = process.argv[2];
  if (!scenarioPath || scenarioPath === "--help") {
    usage();
    process.exit(scenarioPath === "--help" ? 0 : 2);
  }
  const scenario = JSON.parse(fs.readFileSync(scenarioPath, "utf8"));
  assertScenario(scenario);

  const chromium = loadPlaywright();
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: scenario.viewport || { width: 1440, height: 900 } });
  try {
    await page.goto(scenario.url, { waitUntil: scenario.waitUntil || "networkidle" });
    for (let index = 0; index < scenario.steps.length; index += 1) {
      await runStep(page, scenario.steps[index]);
      console.log(`step ${index + 1}/${scenario.steps.length}: ${scenario.steps[index].action}`);
    }
    if (scenario.screenshot) {
      await page.screenshot({ path: scenario.screenshot, fullPage: true });
      console.log(`screenshot: ${scenario.screenshot}`);
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(`ERROR: ${error.message}`);
  process.exit(1);
});
