---
name: frontend-ui-polish-specialist
description: Use when improving an existing frontend page or component's visual polish, layout, spacing, responsive behavior, component consistency, interaction states, or finished UI quality without redesigning the product, creating a new design system, or changing backend behavior.
---

# Frontend UI Polish Specialist

## Overview

Polish existing frontend UI so it looks deliberate, consistent, and production-ready while staying faithful to the project's current style. Prefer local components, tokens, and patterns before adding anything new.

## Boundaries

Use this skill for existing UI optimization:

- Tightening spacing, alignment, density, hierarchy, color use, typography scale, borders, shadows, and radius.
- Fixing visual defects such as overlap, overflow, cramped buttons, inconsistent cards, awkward empty states, missing loading/error states, or mobile horizontal scroll.
- Making existing components and pages feel coherent across desktop and mobile viewports.

Do not use this skill for:

- Designing a brand-new page, brand, visual identity, or design system; use `ui-ux-pro-max`.
- Implementing Figma designs; use the relevant Figma skill.
- Writing a detailed implementation plan; use `superpowers:writing-plans`.
- Coordinating multi-session workers; use `multi-session-project-coordinator`.
- Backend, API, database, infrastructure, or non-visual performance work.

## Component Library First

Before changing UI, discover the project's existing frontend system:

- Read `package.json`, framework config, style config, app entry points, shared component directories, and nearby pages.
- Identify installed UI libraries and primitives such as shadcn/ui, Radix, Ant Design, Element Plus, MUI, Chakra, Bootstrap, Tailwind, lucide, or project-specific components.
- Identify design tokens and style conventions: CSS variables, Tailwind theme values, SCSS variables, utility classes, spacing scale, radius scale, color tokens, typography utilities, and icon set.
- Inspect neighboring screens to learn the page's actual style: density, grid rhythm, card treatment, control sizing, copy length, motion, and state patterns.

Default to reuse:

- Use existing Button, Dialog, Tabs, Select, Table, Card, Form, Tooltip, Icon, Layout, Header, Sidebar, Empty, Skeleton, Toast, and Badge components when available.
- Prefer existing props, variants, sizes, tokens, and class composition patterns over hand-built markup.
- Add a new lightweight wrapper only when no suitable local component exists or the existing component cannot express the needed UI state.
- If adding a wrapper, match local naming, file placement, props style, styling approach, accessibility conventions, and visual density.

Do not introduce a new UI library or icon set unless the user explicitly asks or the current project has no reasonable local option.

## Polish Workflow

1. Inspect the current UI implementation and adjacent examples before proposing changes.
2. Identify the page's existing style contract: component source, layout system, spacing rhythm, color language, type scale, radius/shadow treatment, and responsive breakpoints.
3. List the visible UI issues in priority order:
   - layout stability, overflow, overlap, and responsiveness
   - hierarchy, grouping, and scanability
   - component consistency and state completeness
   - polish details such as spacing, icon alignment, hover/focus/disabled states, empty/loading/error states
4. Make the smallest changes that solve the visible issues while matching the current style.
5. Preserve product scope, information architecture, copy intent, data contracts, and backend behavior unless the user explicitly asks for more.
6. Verify the result on at least one desktop and one mobile viewport. Use Playwright screenshots when a dev server or static preview is available.

## Visual Collision Guard

Treat overlap and obstruction as first-class polish defects across every UI surface, not as form-specific issues.

Check for:

- Controls, labels, helper text, badges, icons, loaders, error text, and action buttons overlapping or covering each other.
- Inputs, segmented controls, filters, toolbars, table headers, sticky bars, cards, sidebars, modals, drawers, popovers, and toasts being clipped or squeezed until content becomes unreadable.
- Invisible blockers such as overlays, sticky headers, backdrops, or absolute-positioned elements preventing expected clicks.
- Dynamic states that change layout: long localized text, validation errors, loading labels, extra actions, empty states, success banners, pagination, and user-generated content.

For compound controls such as input plus button, label plus control, filter plus action, status plus action, or table cell plus menu, prefer resilient layout over hard squeezing:

- Use wrapping, vertical stacking, stable gaps, `min-width: 0`, `max-width`, intentional truncation, or grid/flex constraints.
- Keep primary actions visible and reachable at desktop, narrow desktop, and mobile widths.
- Preserve semantic labels and focus order when controls reflow.
- Re-check hover, focus, disabled, loading, error, and success states after the layout fix.

## User-Facing Copy Principles

When changing any text visible in the software UI, write for real users instead of developers, judges, demo presenters, or AI-tool operators.

- Explain the user's task, state, result, or next step; do not explain internal implementation.
- Do not expose model behavior, API calls, generation pipelines, debug details, ports, stack traces, framework names, or system prompts in the main UI.
- Avoid temporary, placeholder, perfunctory, or obviously AI-generated phrasing.
- Button copy should name a clear action. Status copy should state a clear result. Empty-state copy should tell the user what they can do next.
- Keep tone accurate, natural, and restrained, like part of a mature product rather than a development log, defense note, or system instruction.
- Remove any sentence that does not help the user understand the page, complete a task, or decide the next step.

Before finalizing UI copy, check:

- Does the user really need to see this sentence?
- Does it reveal implementation details or AI-tool traces?
- Can a first-time user understand it immediately?
- Does it clearly state the current state, available action, or actual result?

## UI Priorities

- Stable layout: no text overlap, clipped controls, unwanted horizontal scroll, sticky element collisions, or layout shifts from dynamic content.
- Clear hierarchy: screen title, primary action, secondary actions, filters, status, and content groups are visually distinguishable.
- Consistent components: matching control heights, icon sizes, border radius, shadows, table density, card structure, and form treatment.
- Complete states: hover, focus, active, disabled, selected, loading, empty, error, and success states are visible and accessible enough.
- Responsive behavior: mobile layouts reflow rather than shrink awkwardly; long labels wrap or truncate intentionally.
- Accessibility basics: semantic controls, visible focus, adequate contrast, labels for icon-only buttons, and keyboard-reachable interactions.

## Verification Standard

Before claiming UI polish is complete:

- Run the project's relevant lint, typecheck, build, or test command when available and proportional to the change.
- Preview the touched UI if the project can run locally.
- Check at least desktop and mobile widths; include tablet or narrow desktop when the layout suggests risk.
- Exercise changed components with long text, validation errors, loading states, and extra actions when those states could affect size or wrapping.
- Confirm no new hardcoded design system appears: no random colors, ad hoc component variants, unrelated font changes, or new icon families.
- If screenshots reveal visual defects, fix them before final delivery.

## Common Mistakes

- Rebuilding local components from scratch instead of using the existing component library.
- Importing a new UI kit for one page.
- Changing product flow or page architecture while claiming to do visual polish.
- Applying a fashionable style that conflicts with the rest of the app.
- Fixing desktop while breaking mobile, or checking only the default viewport.
- Using cards inside cards, oversized hero typography inside dense tools, random gradients, emoji icons, or decorative effects that do not match the product.
