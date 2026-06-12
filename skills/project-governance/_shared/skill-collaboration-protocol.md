# Skill Collaboration Protocol

Use this shared protocol when a task naturally crosses multiple skills. It keeps skills cooperative without making each skill duplicate the others.

## Collaboration States

- `discovering`: locate repo facts, source materials, current behavior, and unknowns.
- `designing`: define architecture, domain, API, workflow, or UI decisions.
- `planning`: turn design into implementable steps and acceptance evidence.
- `coordinating`: split work across sessions, worktrees, roles, or review lanes.
- `implementing`: change code, tests, docs, scripts, or assets.
- `verifying`: run tests, builds, runtime checks, browser checks, or external integration checks.
- `delivering`: prepare commits, PRs, delivery docs, reports, or release notes.

## Handoff Packet

When one skill hands work to another, preserve this compact packet:

```text
Goal: <specific outcome>
Current state: <collaboration state>
Source truth: <files, docs, URLs, commands, or thread summaries>
Decisions locked: <choices the next skill must not reopen>
Open questions: <only high-impact unknowns>
Allowed scope: <files/domains/actions>
Forbidden scope: <files/domains/actions>
Evidence so far: <tests/builds/screenshots/runtime checks>
Next skill: <skill name and why>
Stop condition: <when to ask the user or escalate>
```

## Recommended Chains

- Major feature or redesign:
  `define-goal -> codebase-orientation -> architecture-freeze-check -> design-from-materials/domain-solution-designer -> development-playbook-writer -> autonomous-development-governor -> multi-session-project-coordinator`

- API feature:
  `design-from-materials -> domain-solution-designer -> api-contract-designer -> api-request-builder -> autonomous-development-governor`

- Frontend experience:
  `ui-ux-pro-max -> frontend-ui-polish-specialist -> playwright/playwright-interactive -> frontend-critical-flow-acceptance -> autonomous-development-governor`

- Runtime evidence, reports, logs, or orchestration views:
  `autonomous-development-governor -> runtime-evidence-closure-check -> frontend-critical-flow-acceptance -> autonomous-development-governor`

- Multi-worker development:
  `autonomous-development-governor -> multi-session-project-coordinator -> domain/frontend/test/doc skills -> autonomous-development-governor`

- Commit, CI, and PR:
  `autonomous-development-governor -> gh-fix-ci/gh-address-comments/yeet`

## Rules

- Do not reopen upstream decisions unless new evidence invalidates them.
- Do not claim completion from a handoff alone; run the receiving skill's required gate.
- Do not use a specialized skill as a generic planner when a governance or design skill should decide first.
- Prefer the smallest next skill that can move the task forward.
- If a skill finds local verification is still doable, return to `autonomous-development-governor` rather than finalizing with a passive caveat.
