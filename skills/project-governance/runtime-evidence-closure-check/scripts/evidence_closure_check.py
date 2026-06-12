#!/usr/bin/env python3
"""Validate producer/store/consumer/acceptance evidence closure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


EMPTY = {"", "none", "none yet", "n/a", "na", "pending", "todo", "unknown", "待补充"}
REQUIRED_FIELDS = {
    "producer": "real action that creates the record",
    "store_api": "persistence or query evidence",
    "consumer": "UI/report/API consumer evidence",
    "acceptance": "end-to-end action -> query -> visible record evidence",
}


TEMPLATE = {
    "scenarios": [
        {
            "name": "Generate report creates visible run record",
            "producer": "User action, job, or domain event that writes the record",
            "store_api": "Database/API/log query showing the record and ownership scope",
            "consumer": "Page/report/dashboard path showing the same real record",
            "acceptance": "Steps and evidence for trigger -> query -> visible consumer",
            "isolation": "User/tenant/session isolation evidence if applicable",
            "secret_safety": "No secrets or raw internal payloads in records",
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


def missing(value: Any) -> bool:
    return text(value).strip().lower() in EMPTY


def load_scenarios(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("scenarios"), list):
        return data["scenarios"]
    if isinstance(data, dict):
        return [data]
    raise ValueError("input must be an object, array, or object with scenarios array")


def validate(scenarios: list[dict[str, Any]], require_isolation: bool) -> list[str]:
    errors: list[str] = []
    if not scenarios:
        errors.append("no evidence scenarios supplied")

    for index, scenario in enumerate(scenarios, start=1):
        name = text(scenario.get("name") or f"scenario #{index}")
        for field, purpose in REQUIRED_FIELDS.items():
            if missing(scenario.get(field)):
                errors.append(f"{name}: missing {field} evidence ({purpose})")
        if require_isolation and missing(scenario.get("isolation")):
            errors.append(f"{name}: missing isolation evidence")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", nargs="?", type=Path, help="JSON evidence scenarios")
    parser.add_argument("--template", action="store_true", help="print a minimal evidence template")
    parser.add_argument("--require-isolation", action="store_true", help="require isolation evidence for every scenario")
    args = parser.parse_args()

    if args.template:
        print(json.dumps(TEMPLATE, ensure_ascii=False, indent=2))
        return 0
    if not args.evidence:
        parser.error("evidence JSON is required unless --template is used")

    try:
        scenarios = load_scenarios(args.evidence)
        errors = validate(scenarios, args.require_isolation)
    except Exception as exc:  # noqa: BLE001 - CLI should surface parse errors plainly.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"scenarios: {len(scenarios)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
