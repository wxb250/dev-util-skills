#!/usr/bin/env python3
"""Validate user-auth facility evidence against the baseline checklist."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


EMPTY = {"", "none", "none yet", "n/a", "na", "pending", "todo", "unknown", "待补充"}


TEMPLATE = {
    "password_based": True,
    "registration_supported": True,
    "flows": {
        "access_entry": "Protected route or first-use gate evidence",
        "login": "Loading, success, wrong credential, network failure, and retry evidence",
        "registration": "Duplicate account, invalid input, verification, and completion evidence",
        "recovery": "Forgot-password/reset path, identity verification, resend/cooldown, expired/wrong code evidence",
        "logout_expiry": "Logout clears scoped state and expired sessions redirect predictably",
        "account_switching": "Previous user's profile/progress/cache is cleared or refreshed",
        "error_copy": "User-safe error/status copy evidence",
        "browser_evidence": "Desktop and constrained viewport browser evidence",
    },
}


BASE_REQUIRED = ["access_entry", "login", "logout_expiry", "account_switching", "error_copy", "browser_evidence"]


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return "; ".join(text(part) for part in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def missing(value: Any) -> bool:
    return text(value).strip().lower() in EMPTY


def bool_value(data: dict[str, Any], key: str, default: bool) -> bool:
    value = data.get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"yes", "true", "1"}
    return default


def validate(data: dict[str, Any]) -> list[str]:
    flows = data.get("flows")
    if not isinstance(flows, dict):
        raise ValueError("input must contain a flows object")

    required = list(BASE_REQUIRED)
    if bool_value(data, "registration_supported", True):
        required.append("registration")
    if bool_value(data, "password_based", True):
        required.append("recovery")

    errors: list[str] = []
    for key in required:
        if missing(flows.get(key)):
            errors.append(f"missing {key} evidence")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("auth_evidence", nargs="?", type=Path, help="JSON auth facility evidence")
    parser.add_argument("--template", action="store_true", help="print a minimal evidence template")
    args = parser.parse_args()

    if args.template:
        print(json.dumps(TEMPLATE, ensure_ascii=False, indent=2))
        return 0
    if not args.auth_evidence:
        parser.error("auth evidence JSON is required unless --template is used")

    try:
        data = json.loads(args.auth_evidence.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("input must be a JSON object")
        errors = validate(data)
    except Exception as exc:  # noqa: BLE001 - CLI should surface parse errors plainly.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
