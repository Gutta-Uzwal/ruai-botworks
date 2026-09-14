#!/usr/bin/env python3
"""
check_consistency.py — invariant 11, enforced.

Any figure appearing in two documents must derive from one source. This reads
company.py and fails the build when a document contradicts it, or uses a name
that was renamed.

    python scripts/check_consistency.py docs/charter
"""
from __future__ import annotations
import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from company import COMPANY, OFFICERS, UPSTREAM, IDENTITY  # noqa: E402

OFFICER_NAMES = {o[0] for o in OFFICERS}

# A figure written in prose must match the source. (regex, expected, label)
CLAIMS = [
    (r"\*\*(\d+)\s+officers\b",               COMPANY["officers"],   "officer count (total)"),
    (r"·\s*(\d+)\s+officers\b",               COMPANY["officers"],   "officer count (total)"),
    (r"\b(\d+)\s+agents? total\b",            COMPANY["agents_total"], "total agents"),
    (r"one CEO and \*\*(\d+) agents\*\*",     COMPANY["agents_total"], "charter headline"),
    (r"\*\*(\d+)\s+plugins\b",                UPSTREAM["plugins"],   "plugin count (total)"),
    (r"all\s+(\d+)\s+plugins\b",              UPSTREAM["plugins"],   "plugin count (total)"),
    (r"\b(\d+)\s+engineers documented\b",     None,                  "roster count (generated)"),
    (r"exactly\s+(\d+)\s+standing vetoes",    COMPANY["vetoes"],     "veto count"),
]

# Names retired during design. Their presence means a document was not updated.
RETIRED = {
    "code-reviewer": "merge-authority — the workforce already has an agent named "
                     "code-reviewer; two agents with one name holding different "
                     "authority makes the merge decision ambiguous",
}

def check(root: Path) -> int:
    docs = sorted(root.glob("*.md"))
    if not docs:
        print(f"no documents under {root}", file=sys.stderr)
        return 2
    problems: list[str] = []

    for d in docs:
        text = d.read_text(encoding="utf-8")
        lines = text.splitlines()

        for pat, expected, label in CLAIMS:
            if expected is None:
                continue
            for m in re.finditer(pat, text):
                got = int(m.group(1))
                if got != expected:
                    ln = text[: m.start()].count("\n") + 1
                    problems.append(f"{d.name}:{ln}  {label}: document says {got}, source says {expected}")

        for old, why in RETIRED.items():
            for i, line in enumerate(lines, 1):
                # a retired name used as an identifier, not inside an explanation of the rename
                low = line.lower().replace("*", "").replace("_", "")
                exempt = ("rename", "retired", "collision", "workforce", "upstream",
                          "not call", "agent named", "officer holding", "already contains")
                is_roster_row = re.match(r"^\|\s*`[a-z0-9-]+`\s*\|\s*L1\s*\|", line)
                if re.search(rf"`{re.escape(old)}`", line) and not is_roster_row \
                   and not any(e in low for e in exempt):
                    problems.append(f"{d.name}:{i}  retired name `{old}` -> use `{why.split(' —')[0]}`")

    # the company name must be current everywhere, and the old one gone for good
    for d in docs:
        text = d.read_text(encoding="utf-8")
        for stale in IDENTITY["retired_names"]:
            for i, line in enumerate(text.splitlines(), 1):
                if stale in line and "retired" not in line.lower():
                    problems.append(f"{d.name}:{i}  retired company name '{stale}' -> '{IDENTITY['company']}'")

    # every officer must be documented somewhere in the set
    allbody = "\n".join(d.read_text(encoding="utf-8") for d in docs)
    for name in sorted(OFFICER_NAMES):
        if f"`{name}`" not in allbody:
            problems.append(f"officer `{name}` appears in no document")

    print(f"checked {len(docs)} documents against company.py")
    if problems:
        print("\nCONSISTENCY DEFECTS", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        print(f"\n{len(problems)} defect(s). Nothing promotes.", file=sys.stderr)
        return 1
    print(f"OK  {IDENTITY['company']} — {COMPANY['officers']} officers, "
          f"{COMPANY['agents_total']} agents, {COMPANY['vetoes']} vetoes. Every document agrees.")
    return 0

if __name__ == "__main__":
    raise SystemExit(check(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
