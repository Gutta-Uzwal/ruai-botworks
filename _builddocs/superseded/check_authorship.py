#!/usr/bin/env python3
"""
check_authorship.py — the rule that makes "engineers do not write code" real.

Humans may edit specs. Agents may edit code. A commit that violates this fails
the build, so the boundary is enforced by CI rather than by agreement.

    python check_authorship.py --base origin/main --head HEAD
"""
from __future__ import annotations
import argparse, re, subprocess, sys

HUMAN_WRITABLE = (re.compile(r"^specs/.*\.ya?ml$"),
                  re.compile(r"^docs/.*"),
                  re.compile(r"^\.github/agents/.*\.agent\.md$"),
                  re.compile(r"^\.github/copilot-instructions\.md$"))

AGENT_ONLY = (re.compile(r"^src/.*\.py$"),
              re.compile(r"^pipelines/.*\.py$"),
              re.compile(r"^tests/.*\.py$"),
              re.compile(r"^resources/.*\.ya?ml$"),
              re.compile(r"^databricks\.ya?ml$"))

# Identities whose commits count as agent-authored.
AGENT_AUTHORS = ("Copilot", "copilot-swe-agent", "github-actions[bot]",
                 "223556219+Copilot@users.noreply.github.com")

def sh(*a: str) -> str:
    return subprocess.run(a, capture_output=True, text=True, check=True).stdout.strip()

def is_agent(author: str, email: str) -> bool:
    blob = f"{author} {email}".lower()
    return any(t.lower() in blob for t in AGENT_AUTHORS)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--head", default="HEAD")
    a = ap.parse_args()

    shas = sh("git", "rev-list", f"{a.base}..{a.head}").splitlines()
    violations, agent_commits, human_commits = [], 0, 0

    for sha in shas:
        author, email = sh("git", "show", "-s", "--format=%an%n%ae", sha).splitlines()[:2]
        files = sh("git", "diff-tree", "--no-commit-id", "--name-only", "-r", sha).splitlines()
        agent = is_agent(author, email)
        agent_commits += agent; human_commits += not agent
        for f in files:
            if not f:
                continue
            if agent:
                if any(p.match(f) for p in HUMAN_WRITABLE):
                    violations.append(f"{sha[:8]} AGENT edited a human-owned file: {f}")
            else:
                if any(p.match(f) for p in AGENT_ONLY):
                    violations.append(
                        f"{sha[:8]} HUMAN ({author}) wrote code: {f}\n"
                        f"         -> edit the spec and let the agent regenerate it")
                elif not any(p.match(f) for p in HUMAN_WRITABLE):
                    violations.append(f"{sha[:8]} HUMAN ({author}) touched an unclassified path: {f}")

    print(f"commits: {len(shas)}  agent-authored: {agent_commits}  human-authored: {human_commits}")
    if violations:
        print("\nAUTHORSHIP VIOLATIONS\n" + "\n".join("  " + v for v in violations), file=sys.stderr)
        print(f"\n{len(violations)} violation(s). Nothing promotes.", file=sys.stderr)
        return 1
    print("OK  authorship boundary intact.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
