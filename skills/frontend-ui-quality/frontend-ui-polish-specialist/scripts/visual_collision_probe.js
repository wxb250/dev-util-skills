#!/usr/bin/env node
"use strict";

function parseArgs(argv) {
  const args = { selector: "input,button,select,textarea,a,[role='button'],[role='dialog']", viewports: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--url") args.url = argv[++i];
    else if (arg === "--selector") args.selector = argv[++i];
    else if (arg === "--ignore") args.ignore = argv[++i];
    else if (arg === "--viewport") args.viewports.push(argv[++i]);
    else if (arg === "--max-elements") args.maxElements = Number(argv[++i]);
    else if (arg === "--help") args.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!args.viewports.length) args.viewports = ["1440x900", "390x844"];
  if (!args.maxElements) args.maxElements = 250;
  return args;
}

function usage() {
  console.log(`Usage: node visual_collision_probe.js --url <url> [--viewport 1440x900] [--selector <css>] [--ignore <css>]

Checks selected visible elements for viewport overflow, center-point blockers, and obvious interactive overlap.
Requires the project to provide playwright or @playwright/test.`);
}

function loadPlaywright() {
  try {
    return require("@playwright/test").chromium;
  } catch {
    return require("playwright").chromium;
  }
}

function parseViewport(value) {
  const match = /^(\d+)x(\d+)$/.exec(value);
  if (!match) throw new Error(`Invalid viewport '${value}', expected WIDTHxHEIGHT`);
  return { width: Number(match[1]), height: Number(match[2]) };
}

async function inspect(page, selector, ignore, maxElements) {
  return page.evaluate(
    ({ selector, ignore, maxElements }) => {
      const viewport = { width: window.innerWidth, height: window.innerHeight };
      const findings = [];
      const ignored = ignore ? Array.from(document.querySelectorAll(ignore)) : [];
      const isIgnored = (element) => ignored.some((candidate) => candidate === element || candidate.contains(element));
      const isVisible = (element) => {
        const style = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        return style.visibility !== "hidden" && style.display !== "none" && rect.width > 1 && rect.height > 1;
      };
      const elements = Array.from(document.querySelectorAll(selector))
        .filter((element) => !isIgnored(element) && isVisible(element))
        .slice(0, maxElements)
        .map((element, index) => {
          const rect = element.getBoundingClientRect();
          const label =
            element.getAttribute("data-testid") ||
            element.getAttribute("aria-label") ||
            element.id ||
            element.name ||
            element.textContent.trim().slice(0, 40) ||
            element.tagName.toLowerCase();
          return {
            index,
            label,
            tag: element.tagName.toLowerCase(),
            rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height, right: rect.right, bottom: rect.bottom },
          };
        });

      if (document.documentElement.scrollWidth > viewport.width + 2) {
        findings.push(`page has horizontal overflow: scrollWidth=${document.documentElement.scrollWidth}, viewport=${viewport.width}`);
      }

      for (const item of elements) {
        if (item.rect.x < -1 || item.rect.right > viewport.width + 1) {
          findings.push(`${item.label}: clipped horizontally (${Math.round(item.rect.x)}..${Math.round(item.rect.right)} of ${viewport.width})`);
        }
        const cx = item.rect.x + item.rect.width / 2;
        const cy = item.rect.y + item.rect.height / 2;
        if (cx >= 0 && cx <= viewport.width && cy >= 0 && cy <= viewport.height) {
          const hit = document.elementFromPoint(cx, cy);
          const element = document.querySelectorAll(selector)[item.index];
          if (hit && element && hit !== element && !element.contains(hit) && !hit.contains(element)) {
            findings.push(`${item.label}: center point is blocked by ${hit.tagName.toLowerCase()}`);
          }
        }
      }

      for (let i = 0; i < elements.length; i += 1) {
        for (let j = i + 1; j < elements.length; j += 1) {
          const a = elements[i];
          const b = elements[j];
          const x = Math.max(0, Math.min(a.rect.right, b.rect.right) - Math.max(a.rect.x, b.rect.x));
          const y = Math.max(0, Math.min(a.rect.bottom, b.rect.bottom) - Math.max(a.rect.y, b.rect.y));
          const area = x * y;
          const minArea = Math.min(a.rect.width * a.rect.height, b.rect.width * b.rect.height);
          if (area > 64 && area / minArea > 0.08) {
            findings.push(`${a.label} overlaps ${b.label} (${Math.round(area)}px^2)`);
          }
        }
      }

      return { elementCount: elements.length, findings };
    },
    { selector, ignore, maxElements }
  );
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.url) {
    usage();
    process.exit(args.help ? 0 : 2);
  }
  const chromium = loadPlaywright();
  const browser = await chromium.launch({ headless: true });
  const allFindings = [];
  try {
    for (const value of args.viewports) {
      const viewport = parseViewport(value);
      const page = await browser.newPage({ viewport });
      await page.goto(args.url, { waitUntil: "networkidle" });
      const result = await inspect(page, args.selector, args.ignore, args.maxElements);
      console.log(`${value}: elements=${result.elementCount}, findings=${result.findings.length}`);
      for (const finding of result.findings) {
        const line = `${value}: ${finding}`;
        allFindings.push(line);
        console.log(`ERROR: ${line}`);
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }
  process.exit(allFindings.length ? 1 : 0);
}

main().catch((error) => {
  console.error(`ERROR: ${error.message}`);
  process.exit(2);
});
