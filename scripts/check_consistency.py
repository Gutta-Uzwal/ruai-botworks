#!/usr/bin/env python3
"""
check_consistency.py — invariant 11, enforced.

Any figure appearing in two documents must derive from one computed source. That
source is RU-AIBOTWORKS-REGISTRY, read through ru_aibotworks_registry.py. This reads
the prose and fails the build when a document contradicts it, or uses a name that
was retired.

    python scripts/check_consistency.py RU-AIBOTWORKS/RU-AIBOTWORKS-DOCS docs/charter
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "RU-AIBOTWORKS" / "RU-AIBOTWORKS-PLATFORM"))
from ru_aibotworks_registry import Company  # noqa: E402

COMPANY = Company.load()
FIG = COMPANY.figures
IDENTITY = COMPANY.identity

OFFICER_NAMES = {o.name for o in COMPANY.officers}

# A figure written in prose must match the computed source.
#
# Only COMPANY-SCOPE claims are checked. A company-scope claim is one the author
# marked as a headline figure - bolded, or set off in a "· N officers ·" summary
# line. Two things are deliberately NOT matched:
#
#   "The company had 13 officers"     historical prose, correct as written
#   "· **8 staff** · 3 teams"          a per-department count, not a company total
#
# A checker that flags those trains people to ignore it, which is worse than not
# having one.
#   (pattern, expected, label)
CLAIMS: list[tuple[str, int, str]] = [
    (r"\*\*(\d+)\s+officers?\*\*",            FIG["officers"],     "officer count"),
    (r"·\s*(\d+)\s+officers",                FIG["officers"],     "officer count"),
    (r"\*\*(\d+)\s+agents?\s+total\*\*",      FIG["agents_total"], "total agents"),
    (r"\*\*(\d+)\s+agents?\*\*",              FIG["agents_total"], "total agents"),
    (r"·\s*(\d+)\s+agents",                  FIG["agents_total"], "total agents"),
    (r"all\s+(\d+)\s+agents",                FIG["agents_total"], "total agents"),
    (r"exactly\s+(\d+)\s+standing vetoes",     FIG["vetoes"],       "veto count"),
    (r"\*\*(\d+)\s+departments?\*\*",         FIG["departments"],  "department count"),
    (r"·\s*(\d+)\s+departments",             FIG["departments"],  "department count"),
    (r"\*\*(\d+)\s+teams?\*\*",               FIG["teams"],        "team count"),
    (r"·\s*(\d+)\s+teams(?!\s*·\s*\d+\s+leads)", FIG["teams"],  "team count"),
    (r"\*\*(\d+)\s+reserved decisions\*\*",   FIG["reserved_decisions"], "reserved decisions"),
]

# Names retired during design. Their presence means a document was not updated.
RETIRED_AGENT_NAMES = {
    "code-reviewer-officer": "merge-authority",
    "tdd-orchestrator": "tdd-practice-engineer — 'orchestrator' in the name made "
                        "dispatch authority ambiguous",
}

# Phrases that signal a line is explaining a rename rather than using the old name.
EXEMPT = ("rename", "renamed", "retired", "collision", "supersed", "upstream",
          "not call", "agent named", "already contains", "was wrong", "historical",
          "v1", "before", "->", "→")


def check(roots: list[Path]) -> int:
    docs: list[Path] = []
    for root in roots:
        if root.is_file():
            docs.append(root)
        else:
            docs.extend(sorted(root.rglob("*.md")))
    if not docs:
        print(f"no documents under {', '.join(str(r) for r in roots)}", file=sys.stderr)
        return 2

    problems: list[str] = []

    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        lines = text.splitlines()
        rel = doc.resolve().relative_to(ROOT)

        for pattern, expected, label in CLAIMS:
            for m in re.finditer(pattern, text):
                got = int(m.group(1))
                if got != expected:
                    ln = text[: m.start()].count("\n") + 1
                    problems.append(
                        f"{rel}:{ln}  {label}: document says {got}, registry computes {expected}"
                    )

        for old, replacement in RETIRED_AGENT_NAMES.items():
            for i, line in enumerate(lines, 1):
                low = line.lower()
                if re.search(rf"`{re.escape(old)}`", line) and not any(x in low for x in EXEMPT):
                    problems.append(f"{rel}:{i}  retired name `{old}` -> use `{replacement}`")

        for stale in IDENTITY["retired_names"]:
            for i, line in enumerate(lines, 1):
                if stale in line and not any(x in line.lower() for x in EXEMPT):
                    problems.append(
                        f"{rel}:{i}  retired company name '{stale}' "
                        f"-> '{IDENTITY['company']['name']}'"
                    )

    # Every officer must be documented somewhere in the set. An officer nobody
    # wrote down is an officer nobody can hold to account.
    allbody = "\n".join(d.read_text(encoding="utf-8") for d in docs)
    for name in sorted(OFFICER_NAMES):
        if f"`{name}`" not in allbody and name not in allbody:
            problems.append(f"officer `{name}` appears in no document")

    print(f"checked {len(docs)} documents against the registry")
    if problems:
        print("\nCONSISTENCY DEFECTS", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        print(f"\n{len(problems)} defect(s). Nothing promotes.", file=sys.stderr)
        return 1

    print(
        f"OK  {IDENTITY['company']['name']} - {FIG['officers']} officers, "
        f"{FIG['agents_total']} agents, {FIG['vetoes']} vetoes. Every document agrees."
    )
    return 0


if __name__ == "__main__":
    targets = [Path(a).resolve() for a in sys.argv[1:]] or [
        ROOT / "RU-AIBOTWORKS" / "RU-AIBOTWORKS-DOCS"
    ]
    raise SystemExit(check(targets))
