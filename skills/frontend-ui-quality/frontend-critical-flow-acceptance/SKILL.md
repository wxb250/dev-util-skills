---
name: frontend-critical-flow-acceptance
description: Use when frontend changes touch critical user flows such as login, registration, modal dialogs, route transitions, form submission, payment-like confirmation, exam submission, export/download, or fullscreen reading before claiming the work is done.
---

# Frontend Critical Flow Acceptance

## Overview

This skill prevents "tests pass but the user sees a grey screen / blank page / dead button" failures. It is a final interaction gate for frontend work, not a replacement for debugging, UI polish, unit tests, or build verification.

## When To Use

Use this after any change that affects:

- Login, registration, auth prompts, session recovery, or first-use gates.
- Dialogs, drawers, popovers, overlays, fullscreen readers, or portals.
- Primary calls to action, route changes, form submit, exam submit, export, download, upload, or payment-like confirmation.
- Shared UI primitives that can affect many screens, especially Radix, Headless UI, shadcn-style wrappers, portals, z-index, focus traps, or scroll locks.

Do not use this for copy-only edits, pure docs changes, backend-only work, or broad visual design feedback. Use `frontend-ui-polish-specialist` for visual refinement, `systematic-debugging` for unknown bugs, `test-driven-development` for fixes, and `verification-before-completion` before final claims.

## Required Gate

Before saying a critical frontend flow is complete:

1. Identify the exact user path in plain language, for example "home question -> login modal -> login -> workspace with draft question".
2. Run normal verification first: relevant unit tests and production build.
3. Exercise the path in a real browser, preferably with Playwright or the app browser.
4. Verify user-visible outcomes, not just DOM existence.
5. Capture evidence: screenshot path, Playwright assertion output, or concise manual browser notes.

If step 3 is skipped, do not claim the flow is fixed or complete. Say what was verified and what still needs browser validation.

## Browser Acceptance Checklist

For each critical path, check the states that users actually experience:

- Visible: the expected screen, modal, panel, or result is visibly above overlays and not clipped.
- Clickable: primary and secondary buttons can be clicked and are not blocked by invisible layers.
- Recoverable: close, cancel, back, retry, or correction actions work.
- Responsive: one desktop viewport and one constrained viewport do not hide primary actions.
- Safe copy: no raw errors, API URLs, stack traces, framework names, ports, or developer-only wording leak to users.
- User-facing copy: labels, status text, empty states, and success/error messages explain user tasks, results, and next steps without exposing AI generation or implementation details.
- State preserved: drafts, answers, selected tabs, or submitted results remain when the flow promises they will.

If visible, clickable, or responsive checks reveal overlap, clipping, cramped controls, or hidden actions, use `frontend-ui-polish-specialist` for the visual collision fix.

Portal and overlay flows require an extra layer check:

- Overlay has a lower z-index than content.
- Content has explicit positioning when rendered in a portal.
- Focus lands inside the visible content.
- `elementFromPoint()` at the center of the dialog hits dialog content, not the backdrop.

## Minimal Playwright Pattern

Use this style for a fast smoke check when no e2e test exists:

```js
const { chromium } = await import("@playwright/test");
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto("http://127.0.0.1:3001/", { waitUntil: "networkidle" });
await page.locator("#homeQuestion").fill("我想学习人工智能基础");
await page.locator(".home-send-button").click();
await page.locator(".home-login-dialog").waitFor({ state: "visible" });
const result = await page.evaluate(() => {
  const dialog = document.querySelector(".home-login-dialog");
  const overlay = document.querySelector(".ui-dialog-overlay");
  const center = document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2);
  return {
    dialogVisible: !!dialog && dialog.getBoundingClientRect().height > 0,
    dialogZIndex: dialog ? getComputedStyle(dialog).zIndex : "",
    overlayZIndex: overlay ? getComputedStyle(overlay).zIndex : "",
    centerClass: center?.className?.toString() ?? ""
  };
});
console.log(result);
await browser.close();
```

Adapt selectors and URLs to the project. Keep the check focused on the changed flow.

For repeatable checks, write the path as a JSON scenario and run `scripts/critical_flow_smoke.js scenario.json`.

## Leader Rule For Multi-Worker Work

When integrating worker output, do not accept "tests pass" as sufficient for critical frontend flows. Require at least one of:

- A browser screenshot showing the final visible state.
- A Playwright smoke result for the changed path.
- A concise manual validation note with viewport, route, action, and observed result.

If a worker changed shared primitives, the leader must independently run one representative browser path before merging or reporting completion.

## Common Failure Modes

- Modal backdrop appears but content is behind it.
- Button click changes state but no visible feedback appears.
- Mobile viewport hides submit/register/export actions.
- Route navigation works only after refresh.
- Submitted answers/results disappear because live data refresh overwrites local review state.
- Download/fullscreen buttons open the wrong artifact.
