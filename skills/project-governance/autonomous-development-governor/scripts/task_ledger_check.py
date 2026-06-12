#!/usr/bin/env python3
"""Validate an autonomous-development-governor task ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


VALID_STATES = {"planning", "implementing", "verifying", "blocked", "done"}
EMPTY_EVIDENCE = {"", "none", "none yet", "n/a", "na", "pending", "todo", "unknown"}


TEMPLATE = {
    "items": [
        {
            "item": "Example capability or validation item",
            "state": "verifying",
            "evidence": "command, file, screenshot, or runtime proof",
            "can_continue_locally": True,
            "next_action": "run the missing smoke check",
            "blocker_input": "",
        }
    ]
}


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return "; ".join(text(part) for part in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def is_empty_evidence(value: Any) -> bool:
    normalized = text(value).strip().lower()
    return normalized in EMPTY_EVIDENCE


def boolish(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.strip().lower() in {"yes", "true", "1"}:
            return True
        if value.strip().lower() in {"no", "false", "0"}:
            return False
    return None


def load_items(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    raise ValueError("ledger must be a JSON array or an object with an items array")


def validate(items: list[dict[str, Any]], completion_gate: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not items:
        errors.append("ledger has no items")

    for index, item in enumerate(items, start=1):
        label = text(item.get("item") or item.get("name") or f"item #{index}")
        state = text(item.get("state")).lower()
        evidence = item.get("evidence")
        can_continue = boolish(item.get("can_continue_locally"))
        next_action = text(item.get("next_action"))
        blocker_input = text(item.get("blocker_input"))

        if state not in VALID_STATES:
            errors.append(f"{label}: invalid state '{state}'")
            continue

        if state == "done" and is_empty_evidence(evidence):
            errors.append(f"{label}: done item has no concrete evidence")

        if state == "blocked":
            if can_continue is not False:
                errors.append(f"{label}: blocked item must set can_continue_locally to false")
            if not blocker_input:
                errors.append(f"{label}: blocked item must name the required external input")

        if can_continue is True and state == "blocked":
            errors.append(f"{label}: local-doable item cannot remain blocked")

        if can_continue is True and state != "done" and not next_action:
            warnings.append(f"{label}: local-doable unfinished item should name next_action")

        if completion_gate and can_continue is True and state != "done":
            errors.append(f"{label}: completion gate failed; local-doable work remains")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", nargs="?", type=Path, help="JSON task ledger to validate")
    parser.add_argument("--template", action="store_true", help="print a minimal ledger template")
    parser.add_argument("--completion-gate", action="store_true", help="fail if local-doable items are unfinished")
    args = parser.parse_args()

    if args.template:
        print(json.dumps(TEMPLATE, ensure_ascii=False, indent=2))
        return 0
    if not args.ledger:
        parser.error("ledger is required unless --template is used")

    try:
        items = load_items(args.ledger)
        errors, warnings = validate(items, args.completion_gate)
    except Exception as exc:  # noqa: BLE001 - CLI should surface parse errors plainly.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"items: {len(items)}")
    print(f"warnings: {len(warnings)}")
    print(f"errors: {len(errors)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
