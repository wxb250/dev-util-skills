---
name: user-auth-facility-check
description: Use when evaluating or implementing user authentication facilities such as auth, login, registration, logout, forgot password, password reset, session recovery, SMS/email code, 鉴权, 登录, 注册, 忘记密码 before claiming an app has complete account access.
---

# User Auth Facility Check

## Overview

Check whether user authentication is a complete account-access facility, not just a login form. Treat recovery, session boundaries, account switching, and user-facing failure states as part of the baseline experience.

## Boundaries

Use this skill for product and implementation completeness around:

- Login, registration, logout, session expiry, protected-route gates, and first-use account prompts.
- Forgot password, password reset, account recovery, SMS/email code flows, resend/cooldown, and retry paths.
- Identity-scoped client state such as profile, progress, drafts, reports, and cached API data after login, logout, or account switching.

Do not use this skill as a formal security audit. Use `security-threat-model` or `security-best-practices` for threat modeling, cryptography, token storage hardening, abuse prevention, or compliance review. Use `frontend-ui-polish-specialist` for visual overlap, clipping, cramped controls, copy polish, and responsive layout defects. Use `frontend-critical-flow-acceptance` before claiming critical auth flows are complete in a browser.

## Facility Checklist

Verify the app has a coherent path for each supported account action:

- Access entry: protected pages route unauthenticated users to a clear login/register path without dead ends.
- Login: supported methods have loading, success, wrong credential, network failure, locked/rate-limited, and retry states.
- Registration: duplicate account, invalid input, verification, completion, and return-to-app states are handled.
- Recovery: any password-based account system exposes a reachable forgot-password/reset path unless the product explicitly forbids recovery. The path verifies identity, supports resend/cooldown, handles expired or wrong codes, lets the user return to login, and confirms completion.
- Logout and expiry: logout clears user-specific state, expired sessions redirect predictably, and protected data does not stay visible for the wrong user.
- Account switching: profile, progress, reports, drafts, recommendations, and cached API responses are scoped by authenticated user and are refreshed or cleared when the account changes.
- Error and status copy: messages tell users what happened and what to do next without leaking stack traces, raw API errors, provider names, tokens, ports, or debug details.

## Evidence Standard

Before calling auth infrastructure complete, collect evidence at three layers:

- Product map: list the user paths for login, registration, recovery, logout, expiry, and account switching.
- Code/data check: identify the client state, cache keys, API auth context, and storage records that are scoped to a user.
- Browser check: exercise at least one desktop and one constrained viewport for the main login path and any changed recovery/session path.

If a browser check reveals overlap, hidden buttons, clipped inputs, or invisible blockers, hand the visual defect to `frontend-ui-polish-specialist` rather than treating it as an auth-contract decision.

## Scripts

- `scripts/auth_facility_check.py --template` prints a reusable auth evidence template.
- `scripts/auth_facility_check.py auth-evidence.json` checks required login, recovery, logout, account-switching, copy, and browser evidence according to the declared auth capabilities.

## Common Misses

- Shipping login/register without forgot password or another documented recovery route.
- Reset links or verification codes that have no expired, wrong-code, resend, or retry state.
- Keeping the previous user's profile, progress, report, or local cache visible after account switching.
- Treating "button exists in DOM" as enough when the browser path is not visibly usable.
- Exposing raw backend errors instead of user-safe recovery guidance.
