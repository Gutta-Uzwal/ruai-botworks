#!/usr/bin/env python3
"""
ru_aibotworks_layout.py — the folder structure and naming convention, enforced.

A convention that lives only in someone's head decays one file at a time. This reads
every path git knows about (tracked, plus untracked-but-not-ignored) under
RU-AIBOTWORKS/ and fails when one breaks the rule.

The rule, in full:

    RU-AIBOTWORKS/<SECTION>/          sections are UPPERCASE, and there are exactly six
    .../<nested>/                     every folder below a section is lowercase-kebab
                                      (a leading underscore marks a non-department,
                                      e.g. DEPARTMENTS/_officers)
    <kebab>.<ext>                     every data, doc and page file — no company
                                      prefix; the section folder already says whose
                                      it is (reopened 2026-09-15: the prefix inside
                                      RU-AIBOTWORKS/ was judged redundant and dropped)
    ADR-NNN-<kebab>.md                a decision record keeps its own identifier
    ru_aibotworks_<snake>.py          Python modules — hyphens cannot be imported
    AGENT.md REGISTRATION.yaml ...    the agent package: fixed names the Claude
                                      agent and skill formats expect

    python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_layout.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
COMPANY = "RU-AIBOTWORKS"

SECTIONS = {"DATABASE", "DEPARTMENTS", "DOCS", "PLATFORM", "PORTAL", "REGISTRY"}

KEBAB = r"[a-z0-9]+(?:-[a-z0-9]+)*"
FOLDER = re.compile(rf"^_?{KEBAB}$")

# (pattern, where it applies) — first match wins, so the narrow rules come first.
FILE_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^(AGENT\.md|REGISTRATION\.yaml|TOOLS\.yaml|EVALUATION\.yaml|SKILL\.md)$"), "DEPARTMENTS"),
    (re.compile(r"^ru_aibotworks_[a-z0-9]+(?:_[a-z0-9]+)*\.py$"), "PLATFORM"),
    (re.compile(rf"^{KEBAB}\.html$"), "PLATFORM/templates"),
    (re.compile(rf"^ADR-\d{{3}}-{KEBAB}\.md$"), "DOCS/adr"),
    (re.compile(rf"^{KEBAB}(?:\.{KEBAB})?\.(?:md|yaml|sql|html|css|json)$"), ""),
]


def paths() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", COMPANY],
        capture_output=True, text=True, cwd=ROOT, check=True,
    ).stdout
    # A file deleted in the working tree but still in the index is not layout.
    return sorted({p for p in out.splitlines() if p and (ROOT / p).exists()})


def check() -> int:
    problems: list[str] = []
    files = paths()

    for path in files:
        parts = path.split("/")[1:]  # drop RU-AIBOTWORKS/
        if len(parts) < 2:
            problems.append(f"{path}  loose file at the company root; it belongs in a section")
            continue

        section, *folders, name = parts
        if section not in SECTIONS:
            problems.append(f"{path}  unknown section '{section}' (expected one of {sorted(SECTIONS)})")
            continue

        for folder in folders:
            if not FOLDER.match(folder):
                problems.append(f"{path}  folder '{folder}' is not lowercase-kebab")

        where = "/".join([section, *folders])
        for pattern, scope in FILE_RULES:
            if where.startswith(scope) and pattern.match(name):
                break
        else:
            problems.append(f"{path}  file name '{name}' breaks the naming rule")

    print(f"checked {len(files)} paths under {COMPANY}/")
    if problems:
        print("\nLAYOUT DEFECTS", file=sys.stderr)
        for p in problems[:40]:
            print("  " + p, file=sys.stderr)
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more", file=sys.stderr)
        print(f"\n{len(problems)} defect(s). Nothing promotes.", file=sys.stderr)
        return 1

    print("OK  every folder and file follows the convention.")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
