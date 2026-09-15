#!/usr/bin/env python3
"""
ru_aibotworks_authorship.py — the generated tree is written by the generator, not by hand.

RU-AIBOTWORKS has one source of truth and several derived trees. The failure mode
this guards against is quiet and common: somebody fixes a typo in a generated
`AGENT.md` instead of in the registry, the next generation reverts it, and the fix
is lost without anyone noticing.

The rule:

    REGISTRY/      human-authored, reviewed like code
    PLATFORM/      human-authored
    DOCS/          human-authored
    DEPARTMENTS/   GENERATED — never edited directly
    PORTAL/        GENERATED
    DATABASE/*seed.sql  GENERATED
    .claude/agents/              GENERATED — synced from the registry
    agent-tools.json             GENERATED

This is the repository expression of STD-AGENT-001 A1.6: nothing writes its own
configuration, including us.

    python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_authorship.py                     # working tree
    python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_authorship.py --base origin/main  # a range of commits
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

GENERATED = (
    re.compile(r"^RU-AIBOTWORKS/DEPARTMENTS/"),
    re.compile(r"^RU-AIBOTWORKS/PORTAL/"),
    re.compile(r"^RU-AIBOTWORKS/DATABASE/.*seed\.sql$"),
    re.compile(r"^\.claude/agents/.*\.md$"),
    re.compile(r"^agent-tools\.json$"),
)

# Changing one of these is what legitimately causes the generated tree to change.
SOURCES = (
    re.compile(r"^RU-AIBOTWORKS/REGISTRY/"),
    re.compile(r"^RU-AIBOTWORKS/PLATFORM/"),
)


def sh(*args: str) -> str:
    result = subprocess.run(args, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def changed_files(base: str | None) -> list[str]:
    if base:
        out = sh("git", "diff", "--name-only", f"{base}...HEAD")
    else:
        out = sh("git", "diff", "--name-only", "HEAD")
    return [f for f in out.splitlines() if f]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=None, help="compare against this ref instead of the working tree")
    args = parser.parse_args()

    files = changed_files(args.base)
    if not files:
        print("no changed files to check")
        return 0

    touched_generated = [f for f in files if any(p.match(f) for p in GENERATED)]
    touched_sources = [f for f in files if any(p.match(f) for p in SOURCES)]

    print(f"changed: {len(files)} file(s) — "
          f"{len(touched_generated)} generated, {len(touched_sources)} source")

    # A generated file changing with no source change means someone edited the
    # output. The generator is deterministic, so that cannot happen any other way.
    if touched_generated and not touched_sources:
        print("\nAUTHORSHIP VIOLATION", file=sys.stderr)
        print(
            "  Generated files changed with no change to the registry or the platform.\n"
            "  That means the output was edited directly, and the next generation will\n"
            "  revert it silently.\n",
            file=sys.stderr,
        )
        for f in touched_generated[:10]:
            print(f"    {f}", file=sys.stderr)
        if len(touched_generated) > 10:
            print(f"    ... and {len(touched_generated) - 10} more", file=sys.stderr)
        print(
            "\n  Fix: make the change in REGISTRY and regenerate.\n"
            "       python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_generate.py",
            file=sys.stderr,
        )
        return 1

    print("OK  authorship boundary intact — generated trees follow their source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
