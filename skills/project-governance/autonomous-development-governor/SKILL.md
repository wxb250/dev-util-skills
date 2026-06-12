---
name: autonomous-development-governor
description: Govern autonomous software development progress, verification, blockers, and completion decisions. Use when Codex must decide whether to continue local development or validation, declare work done, classify unfinished items, manage evidence quality, respond to "why not do it", or supervise development before/after multi-session coordination without duplicating worker orchestration.
---

# Autonomous Development Governor

## Overview

Use this skill as the decision layer above ordinary implementation and above `multi-session-project-coordinator`. It decides what should continue automatically, what is genuinely blocked, what evidence is sufficient, and whether Codex may honestly say the work is done.

Do not use this skill to create worker threads, manage worktrees, or merge worker branches directly. When the decision is "this needs multiple sessions," invoke `multi-session-project-coordinator` for thread/worktree mechanics.

## Core Workflow

1. Read the user's plan or request, current repo state, recent test/build evidence, `git status`, and any worker or review summaries.
2. Build a task ledger with one row per promised capability, validation item, documentation item, worker output, or user-visible risk.
3. Classify each row as `planning`, `implementing`, `verifying`, `blocked`, or `done`.
4. Apply the gates in `references/decision-gates.md` before declaring anything blocked or done.
5. Continue local, non-destructive work when the remaining item is doable in the current environment. Do not ask the user to confirm routine tests, builds, Docker checks, API smoke checks, or browser smoke checks if they are already within the user's request.
6. Stop and ask only for true external inputs or unsafe actions: production deployment, destructive git/filesystem operations, real secrets, paid external calls, production credentials, or cross-scope work.
7. Before final response, run the Completion Gate and report evidence by ladder level: source, unit tests, build, container/runtime, browser, external integration.

## Task Ledger

Use a compact ledger internally or in reports:

```text
Item: <capability or validation>
State: <planning|implementing|verifying|blocked|done>
Evidence: <commands, files, screenshots, worker summaries, or "none yet">
Can continue locally: <yes|no>
Next action: <run test/build/smoke, fix, dispatch coordinator, ask user, record blocker>
Blocker input, if any: <exact credential/environment/decision needed>
```

If the user asks "why not do it" or challenges an unfinished item, immediately rerun this ledger for all "not done" items. Anything with `Can continue locally: yes` should move back to implementation or verification, not remain in the final answer as a passive caveat.

## Decision Rules

- Treat local tests, builds, Docker compose rebuilds, health checks, Playwright/browser smoke checks, and API smoke checks as doable unless the environment proves otherwise.
- Treat real SMS provider calls, production keys, paid APIs, external network gateways, live deployment, and customer data access as external blockers unless the user explicitly provides safe test credentials and approval.
- User-visible problems outrank internal polish: raw errors, internal enum labels, infinite polling, broken copy, stale success claims, or visible developer terms should be fixed or clearly escalated before broad refactors.
- Documentation must follow code reality. If code, API docs, delivery docs, and test reports disagree, classify it as Reality Drift and resolve or report the mismatch.
- When completion depends on runtime evidence, activity logs, audit logs, evidence pages, reports, dashboards, or orchestration/run history, use `runtime-evidence-closure-check` to verify the producer-to-consumer loop before making the completion decision.
- A slow or silent review worker is not a permanent blocker. Wait only for the agreed threshold, then close or mark it as "review not returned" and continue with available evidence.
- Do not call a task complete solely because a worker said it is done. Confirm expected files, diffs, validation output, and role boundaries.

## Multi-Session Handoff

Use `multi-session-project-coordinator` when at least two independent workstreams would shorten elapsed time without creating heavy conflicts.

Before invoking it, provide:

- the task ledger rows that justify parallelism
- proposed worker scopes and forbidden areas
- evidence still required for Completion Gate
- stop conditions and external blockers already identified

After worker results return, this skill resumes ownership of completion decisions: classify outputs, decide whether more local verification is needed, and prevent premature "done" claims.

## Reporting Shape

When reporting progress or final results, keep the evidence layered:

```text
Done:
- <item> - evidence: <test/build/file/runtime proof>

Not done:
- <item> - reason: <external blocker or failed local evidence>
- Need from user: <exact input>, or next local action: <command/check>

Completion decision:
- <done|not done|blocked>
- Local doable work remaining: <none|list>
```

Never hide unrun verification inside a success summary. If browser, container, or external integration evidence is missing, say whether it is locally runnable and what should happen next.

## Scripts

- `scripts/task_ledger_check.py --template` prints a JSON task-ledger template.
- `scripts/task_ledger_check.py ledger.json --completion-gate` fails if any local-doable item remains unfinished or any `done` item lacks evidence.

## References

- For exact gate definitions, read `references/decision-gates.md`.
- For state names and evidence categories, read `references/status-taxonomy.md`.
- For cross-skill collaboration conventions in this repo, read `../_shared/skill-collaboration-protocol.md`.
