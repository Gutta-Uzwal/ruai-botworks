#!/usr/bin/env python3
"""Validate agent tool contracts and hash-chained execution receipts."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = ROOT / "agent-tools.json"
DEFAULT_RECEIPTS = ROOT / "receipts"
APPROVALS = {"none", "single", "two_person"}
HARD_DELETE_WORDS = ("hard-delete", "hard_delete", "drop", "truncate", "purge")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc


def validate_registry(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        registry = load_json(path)
    except ValueError as exc:
        return [str(exc)]

    if registry.get("version") != 1:
        errors.append("registry version must be 1")
    egress = registry.get("egress")
    if not isinstance(egress, dict) or egress.get("default") != "deny":
        errors.append("egress default must be deny")
    if not isinstance(egress, dict) or not isinstance(egress.get("allowlist"), list):
        errors.append("egress allowlist must be an explicit list")

    tools = registry.get("tools")
    if not isinstance(tools, list) or not tools:
        return errors + ["tools must be a non-empty list"]

    names: set[str] = set()
    for index, tool in enumerate(tools):
        prefix = f"tools[{index}]"
        if not isinstance(tool, dict):
            errors.append(f"{prefix} must be an object")
            continue
        name = tool.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"{prefix}.name is required")
        elif name in names:
            errors.append(f"{prefix}.name duplicates {name}")
        else:
            names.add(name)

        for field in ("version", "owner", "description", "irreversibility",
                      "side_effects", "idempotent", "rollback", "scope",
                      "limits", "gates", "evidence"):
            if field not in tool:
                errors.append(f"{prefix}.{field} is required")

        tier = tool.get("irreversibility")
        if not isinstance(tier, int) or tier not in range(5):
            errors.append(f"{prefix}.irreversibility must be an integer from 0 to 4")
        elif tier >= 2 and (not isinstance(tool.get("rollback"), str)
                            or not tool["rollback"].strip()
                            or tool["rollback"] == "null"):
            errors.append(f"{prefix} tier {tier} requires a rollback command")
        elif tier >= 3 and tool.get("gates", {}).get("approval") == "none":
            errors.append(f"{prefix} tier {tier} requires approval")

        if any(word in str(name).lower() for word in HARD_DELETE_WORDS):
            errors.append(f"{prefix} exposes a prohibited destructive verb")
        gates = tool.get("gates")
        if not isinstance(gates, dict) or gates.get("approval") not in APPROVALS:
            errors.append(f"{prefix}.gates.approval must be one of {sorted(APPROVALS)}")
        limits = tool.get("limits")
        if not isinstance(limits, dict):
            errors.append(f"{prefix}.limits must be an object")
        else:
            for field in ("per_task", "per_agent_hour", "mutation_budget"):
                if not isinstance(limits.get(field), int) or limits[field] < 0:
                    errors.append(f"{prefix}.limits.{field} must be a non-negative integer")
        evidence = tool.get("evidence")
        if not isinstance(evidence, dict) or evidence.get("log_before_state") is not True:
            errors.append(f"{prefix}.evidence.log_before_state must be true")

    return errors


def receipt_digest(receipt: dict[str, Any]) -> str:
    payload = dict(receipt)
    payload.pop("digest", None)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def verify_receipts(directory: Path) -> list[str]:
    errors: list[str] = []
    previous = "GENESIS"
    files = sorted(directory.glob("*.json"))
    for path in files:
        try:
            receipt = load_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if receipt.get("previous_digest") != previous:
            errors.append(f"{path.name}: previous_digest does not match chain")
        if receipt.get("digest") != receipt_digest(receipt):
            errors.append(f"{path.name}: digest does not match receipt contents")
        previous = receipt.get("digest", previous)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "verify-receipts"))
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--receipts", type=Path, default=DEFAULT_RECEIPTS)
    args = parser.parse_args()

    errors = (validate_registry(args.registry)
              if args.command == "validate"
              else verify_receipts(args.receipts))
    if errors:
        for error in errors:
            print(f"DEFECT  {error}", file=sys.stderr)
        return 1
    print(f"{args.command} valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
