#!/usr/bin/env python3
"""
company.py — the single source of truth for every company figure.

Invariant 11 says any number appearing in two documents derives from one
computed source. This is that source. Documents quote COMPANY[...]; the
consistency checker fails the build if a document disagrees with it.
"""
from __future__ import annotations


# ─── Company identity. Every document derives its name from here. ────────────
IDENTITY = {
    "company":    "RU AI Botworks",
    "ceo":        "Uzwal Gutta",
    "ceo_alias":  "Ujwal Gutta",
    "ceo_full":   "Uzwal Gutta (alias Ujwal Gutta)",
    "fork_org":   "ruai-botworks",          # set to your real GitHub org
    "fork_repo":  "ruai-botworks/agents",
    "retired_names": ["Gutta AI", "gutta/agents", "Gutta-Uzwal"],   # checker fails if these reappear
}

# ─── The officers. Hand-written, owned, genome-validated. ────────────────────
# (name, level, reports_to, model, power, responsibility)
OFFICERS = [
    ("cto",                "L4", "CEO",                 "inherit", "",
     "Triage size, dispatch, off-stack proposals"),
    ("product-owner",      "L3", "cto",                 "sonnet",  "",
     "Success criteria, scope, the Requirements gate"),
    ("design-owner",       "L3", "cto",                 "inherit", "",
     "DESIGN.md, aesthetic family, the Design gate"),
    ("web-architect",      "L3", "cto",                 "opus",    "",
     "Lane A/B choice, component structure, API shape"),
    ("data-architect",     "L3", "cto",                 "opus",    "",
     "Schema, grain, retention, service contracts"),
    ("platform-architect", "L3", "cto",                 "opus",    "",
     "CI shape, environments, Cedar policy, plugin architecture"),
    ("testing-architect",  "L3", "cto",                 "sonnet",  "",
     "Quality bar, gate contents, blocking vs advisory"),
    ("quality-compliance", "L3", "cto",                 "opus",    "VETO",
     "Documented non-conformance blocks the release"),
    ("merge-authority",    "L2", "testing-architect",   "opus",    "READ-ONLY",
     "Whether this merges. Holds no Write or Edit"),
    ("security-engineer",  "L2", "platform-architect",  "opus",    "VETO",
     "Vulnerabilities, receipt-chain verification, /audit"),
    ("sre",                "L2", "platform-architect",  "opus",    "VETO",
     "Production instability blocks the release"),
    ("release-manager",    "L2", "platform-architect",  "sonnet",  "",
     "Promotion and failure routing. Routes, never fixes"),
    ("dependency-steward", "L2", "platform-architect",  "sonnet",  "",
     "Fork log, pins, certification, Tier C teardown"),
]

RESERVED_DECISIONS = frozenset(
    {
        "what to build",
        "whether the design is right",
        "whether to override a veto",
        "off-stack technology",
    }
)

FUNCTION = {
    "cto": "Direct", "product-owner": "Direct", "design-owner": "Direct",
    "web-architect": "Build", "data-architect": "Build", "platform-architect": "Build",
    "testing-architect": "Verify", "merge-authority": "Verify",
    "security-engineer": "Verify", "quality-compliance": "Verify",
    "release-manager": "Ship", "sre": "Ship", "dependency-steward": "Ship",
}

# ─── Plugin ownership. All 94 map to exactly one officer, so all 202 engineers
#     land deterministically. An unmapped plugin fails the build. ─────────────
PLUGIN_OWNER: dict[str, str] = {}

def _own(officer: str, *plugins: str) -> None:
    for p in plugins:
        if p in PLUGIN_OWNER:
            raise SystemExit(f"duplicate ownership of plugin '{p}'")
        PLUGIN_OWNER[p] = officer

_own("web-architect",
     "backend-development", "frontend-mobile-development", "multi-platform-apps",
     "developer-essentials", "api-scaffolding", "python-development",
     "javascript-typescript", "systems-programming", "jvm-languages",
     "web-scripting", "functional-programming", "julia-development",
     "arm-cortex-microcontrollers", "shell-scripting", "dotnet-contribution",
     "payment-processing", "blockchain-web3", "game-development",
     "framework-migration", "codebase-cleanup", "code-refactoring",
     "debugging-toolkit")                                                   # 22

_own("data-architect",
     "database-design", "database-migrations", "data-engineering",
     "data-validation-suite", "machine-learning-ops", "llm-application-dev",
     "llm-finetuning", "dgx-spark-ops", "runapi-mcp", "quantitative-trading",
     "application-performance", "database-cloud-optimization")              # 12

_own("platform-architect",
     "cloud-infrastructure", "kubernetes-operations", "deployment-strategies",
     "cicd-automation", "protect-mcp", "signed-audit-trails", "block-no-verify",
     "team-collaboration", "operating-kit")                                 # 9

_own("sre",
     "incident-response", "observability-monitoring", "distributed-debugging",
     "error-diagnostics")                                                   # 4

_own("design-owner",
     "ui-design", "meigen-ai-design", "brand-landingpage",
     "pptx-deck-creation")                                                  # 4

_own("product-owner",
     "seo-content-creation", "seo-technical-optimization", "seo-analysis-monitoring",
     "content-marketing", "social-publishing", "business-analytics",
     "startup-business-analyst", "before-you-build", "customer-sales-automation",
     "storymap-skill")                                                      # 10

_own("testing-architect",
     "unit-testing", "qa-orchestra", "ciagent", "performance-testing-review",
     "tdd-workflows", "error-debugging")                                    # 6

_own("merge-authority",
     "comprehensive-review", "conductor", "skill-forge-essentials")         # 3

_own("security-engineer",
     "security-scanning", "backend-api-security", "frontend-mobile-security",
     "reverse-engineering")                                                 # 4

_own("quality-compliance",
     "security-compliance", "accessibility-compliance", "hr-legal-compliance",
     "review-agent-governance")                                             # 4

_own("release-manager",
     "git-pr-workflows", "deployment-validation", "code-documentation",
     "documentation-generation", "documentation-standards", "c4-architecture",
     "api-testing-observability", "file-conversion")                        # 8

_own("dependency-steward",
     "plugin-eval", "dependency-management", "pensyve", "context-management") # 4

_own("cto",
     "agent-orchestration", "full-stack-orchestration", "agent-teams",
     "ship-mate")                                                           # 4

# Held in the fork, governed, never dispatched. Recorded not deleted, so the
# fork stays mergeable with upstream.
DECLINED_PLUGINS = {"blockchain-web3", "game-development", "quantitative-trading",
                    "arm-cortex-microcontrollers", "reverse-engineering"}


# ─── Design generators. Own several; activate exactly ONE per build. ─────────
# Two visual generators active in one session give contradictory instructions.
# The constraint is concurrency, not ownership. design-owner picks one per
# template and records it in that project's DESIGN.md.
DESIGN_GENERATORS = {
    "ui-ux-pro-max": {
        "source":  "nextlevelbuilder/ui-ux-pro-max-skill",   # second ecosystem: pin separately
        "install": "/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill",
        "activate":"/plugin install ui-ux-pro-max@ui-ux-pro-max-skill",
        "requires":"python3 (stdlib only, no network calls)",
        "licence": "UNVERIFIED — verify before commercial use",   # see note below
        "strength":"Industry reasoning rules; 22 stacks incl. Django-adjacent + Flutter",
        "use_for": ["healthcare", "ecommerce", "lms", "saas-dashboard", "crm", "booking"],
    },
    "ui-design": {
        "source":  "in-fork (wshobson)", "install": "/plugin install ui-design",
        "requires":"none", "licence": "MIT (covered by the fork)",
        "strength":"Web + mobile UI/UX, already pinned and certified",
        "use_for": ["school", "corporate", "restaurant"],
    },
    "brand-landingpage": {
        "source":  "in-fork (wshobson)", "install": "/plugin install brand-landingpage",
        "requires":"none", "licence": "MIT (covered by the fork)",
        "strength":"Brand discovery through to deployment-ready landing page",
        "use_for": ["portfolio"],
    },
}

# Figures from the repository README (Aug 2026). Third-party listings disagree
# badly — 57/67/79/84/107 styles, 95/97/127/161/192 palettes seen in the wild.
# Trust the repo, not the aggregators.
UI_UX_PRO_MAX_FACTS = {
    "styles": "79 searchable (50 active)", "palettes": 192, "font_pairings": 74,
    "ux_guidelines": 119, "reasoning_rules": 192, "chart_types": 25, "stacks": 22,
}

# ─── The data lab. Exploration zone; the licence gate is the door out. ───────
LAB = {
    "db":        "labs/lab.duckdb",          # DuckDB, embedded, no server
    "models":    "labs/models",
    "automl":    "pycaret==3.4.0",           # frozen line. 4.0 is alpha + BUSL control plane
    "python":    "3.11-3.13",                # 3.14 blocked on PEP 649 upstream
    "owner":     "data-architect",
    "licence_clearance": "web-compliance-engineer",
    "commercial_ok": ["CC0-1.0", "PDDL", "CC-BY-4.0", "CC-BY-SA-4.0", "ODC-BY",
                      "ODbL-1.0", "MIT", "Apache-2.0", "proprietary"],
    "rule": "A promoted model may ENTER the pipeline. It has not shipped.",
}

# ─── Upstream facts, verified against the repository, not recalled. ──────────
UPSTREAM = {
    "repo": "wshobson/agents", "licence": "MIT",
    "plugins": 94, "agents": 202, "skills": 183, "commands": 105,
    "orchestrators": 16, "agents_documented_by_name": 105,
    "stars": "39.5k", "forks": "4.2k", "commits": 569,
    "external_plugins": ["pensyve", "qa-orchestra", "storymap-skill", "ciagent"],
}

COMPANY = {
    "officers": len(OFFICERS),
    "engineers": UPSTREAM["agents"],
    "agents_total": len(OFFICERS) + UPSTREAM["agents"],
    "plugins_mapped": len(PLUGIN_OWNER),
    "vetoes": sum(1 for o in OFFICERS if o[4] == "VETO"),
    "read_only": sum(1 for o in OFFICERS if o[4] == "READ-ONLY"),
    "l3": sum(1 for o in OFFICERS if o[1] == "L3"),
    "l2": sum(1 for o in OFFICERS if o[1] == "L2"),
    "functions": len(set(FUNCTION.values())),
    "deepest_chain": 3,
    "invariants": 12,
    "gate_families": 9,
    "templates": 10,
}

COMPANY.update({"name": IDENTITY["company"], "ceo": IDENTITY["ceo_full"]})

def selfcheck() -> list[str]:
    errs = []
    names = [o[0] for o in OFFICERS]
    if len(names) != len(set(names)):
        errs.append("duplicate officer name")
    for n, lvl, rpt, *_ in OFFICERS:
        if rpt != "CEO" and rpt not in names:
            errs.append(f"{n} reports to '{rpt}' which does not exist")
    if COMPANY["vetoes"] != 3:
        errs.append(f"veto count is {COMPANY['vetoes']}, must be exactly 3")
    if set(FUNCTION) != set(names):
        errs.append("FUNCTION map and OFFICERS disagree")
    if COMPANY["plugins_mapped"] != UPSTREAM["plugins"]:
        errs.append(f"{COMPANY['plugins_mapped']} plugins mapped, upstream has {UPSTREAM['plugins']}")
    lvl = {o[0]: o[1] for o in OFFICERS}
    order = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}
    for n, l, rpt, *_ in OFFICERS:            # authority must never invert
        if rpt != "CEO" and order[lvl[rpt]] <= order[l]:
            errs.append(f"authority inverts: {n} ({l}) reports to {rpt} ({lvl[rpt]})")
    return errs

if __name__ == "__main__":
    import json, sys
    e = selfcheck()
    for x in e:
        print(f"DEFECT  {x}", file=sys.stderr)
    print(json.dumps(COMPANY, indent=2))
    sys.exit(1 if e else 0)
