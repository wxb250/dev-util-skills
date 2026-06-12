---
name: runtime-evidence-closure-check
description: Use when a feature depends on runtime evidence, audit log, activity log, runs, orchestration, proof, evidence page, dashboard, report, 运行取证, 待取证, 运行记录, 编排记录, 证据页, 展示页没数据, or when a UI reads records but real actions may not create them.
---

# Runtime Evidence Closure Check

## Overview

Check that evidence features are closed loops, not display shells. A page, report, dashboard, audit trail, or orchestration view is not complete unless real user or system actions produce records that are stored, queryable, and shown back to the user.

## Boundaries

Use this skill for features involving runtime evidence, activity records, audit logs, orchestration runs, evidence dashboards, reports, operation history, job history, or "pending evidence" states.

Do not use this skill to decide whether the whole task is done; return that decision to `autonomous-development-governor`. Do not use it for browser clickability or visibility defects; use `frontend-critical-flow-acceptance` and `frontend-ui-polish-specialist`. Do not use it for formal security review of sensitive logging; use `security-threat-model` or `security-best-practices`.

## Closure Model

Verify four layers before accepting the feature:

- Producer: real business actions create evidence records. Examples include asking, generating, submitting, exporting, approving, retrying, completing jobs, or other domain actions.
- Store/API: records are persisted or durably emitted, scoped by user/tenant/session as appropriate, and exposed through the intended query path.
- Consumer: the UI, report, dashboard, or API response reads real records instead of mocks, stale fixtures, local-only state, or a manual demo endpoint.
- Acceptance: validation triggers a real action, queries the evidence through the same path the product uses, and confirms the record appears in the visible consumer.

If any layer is missing, call the feature incomplete even when the UI renders and tests pass.

## Inspection Workflow

1. Identify the promised evidence view or report and the records it claims to show.
2. Trace each displayed record type back to the real action that should produce it.
3. Check persistence, ownership, isolation, retention, and query filters for those records.
4. Confirm empty states distinguish "no actions yet" from "the producer is not wired".
5. Define at least one end-to-end evidence scenario: trigger real action -> query/store check -> consumer displays matching record.

## Evidence Scenarios

Use concrete scenarios rather than static existence checks:

- For an activity feed: perform the activity, then verify a new feed item with action, actor, time, and result.
- For orchestration or run history: trigger a real workflow, then verify the run appears with the expected type and status.
- For reports or dashboards: create or update source data, then verify the report changes through the normal read path.
- For audit logs: trigger the auditable event, then verify the log is scoped correctly and does not leak secrets or raw internal payloads.

## Scripts

- `scripts/evidence_closure_check.py --template` prints a reusable scenario template.
- `scripts/evidence_closure_check.py evidence.json --require-isolation` checks that each scenario includes Producer, Store/API, Consumer, Acceptance, and isolation evidence.

## Common Misses

- Building the consumer first and leaving producers unwired.
- Removing a manual "create record" endpoint without adding automatic record creation from real actions.
- Treating an empty state such as "pending evidence" as acceptable when actions should already have generated evidence.
- Testing only that `/runs`, `/logs`, or `/reports` can be read, without proving that real actions write to them.
- Letting records leak across users, tenants, sessions, or accounts.
