#!/usr/bin/env python3
"""Validate the governance genome for the owned officer layer."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__:
    from . import company
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import company


RESERVED_DECISIONS = frozenset(
    {
        "what to build",
        "whether the design is right",
        "whether to override a veto",
        "off-stack technology",
    }
)


def validate() -> list[str]:
    errors = list(company.selfcheck())
    officers = company.OFFICERS
    names = {officer[0] for officer in officers}
    levels = {officer[0]: officer[1] for officer in officers}
    authority_order = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}

    for name, level, reports_to, *_ in officers:
        if reports_to != "CEO" and reports_to not in names:
            errors.append(f"{name} reports to unknown officer '{reports_to}'")
        if reports_to != "CEO" and authority_order[levels[reports_to]] <= authority_order[level]:
            errors.append(
                f"authority inverts: {name} ({level}) reports to "
                f"{reports_to} ({levels[reports_to]})"
            )

    veto_count = sum(1 for officer in officers if officer[4] == "VETO")
    if veto_count != 3:
        errors.append(f"veto count is {veto_count}, must be exactly 3")

    missing_decisions = RESERVED_DECISIONS - company.RESERVED_DECISIONS
    if missing_decisions:
        errors.append(
            "reserved decisions removed: " + ", ".join(sorted(missing_decisions))
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true", help="validate governance invariants")
    args = parser.parse_args()
    if not args.validate:
        parser.error("use --validate to run the genome checks")

    errors = validate()
    if errors:
        for error in errors:
            print(f"DEFECT  {error}", file=sys.stderr)
        return 1

    print("genome valid: reporting lines, authority, vetoes, and reserved decisions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
