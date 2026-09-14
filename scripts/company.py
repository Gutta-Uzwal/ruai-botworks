#!/usr/bin/env python3
"""Single source of truth for RU AI Botworks company figures."""
from __future__ import annotations

IDENTITY = {
    "company": "RU AI Botworks",
    "ceo": "Uzwal Gutta",
    "ceo_alias": "Ujwal Gutta",
    "ceo_full": "Uzwal Gutta (alias Ujwal Gutta)",
    "fork_org": "ruai-botworks",
    "fork_repo": "ruai-botworks/agents",
    "retired_names": ["Gutta AI", "gutta/agents", "Gutta-Uzwal"],
}

RESERVED_DECISIONS = frozenset(
    {
        "what to build",
        "whether the design is right",
        "whether to override a veto",
        "off-stack technology",
    }
)

OFFICERS = [
    ("cto", "L4", "CEO", "inherit", "", "Triage size, dispatch, off-stack proposals"),
    ("product-owner", "L3", "cto", "sonnet", "", "Success criteria, scope, the Requirements gate"),
    ("design-owner", "L3", "cto", "inherit", "", "DESIGN.md, aesthetic family, the Design gate"),
    ("web-architect", "L3", "cto", "opus", "", "Lane A/B choice, component structure, API shape"),
    ("data-architect", "L3", "cto", "opus", "", "Schema, grain, retention, service contracts"),
    ("platform-architect", "L3", "cto", "opus", "", "CI shape, environments, Cedar policy, plugin architecture"),
    ("testing-architect", "L3", "cto", "sonnet", "", "Quality bar, gate contents, blocking vs advisory"),
    ("quality-compliance", "L3", "cto", "opus", "VETO", "Documented non-conformance blocks the release"),
    ("merge-authority", "L2", "testing-architect", "opus", "READ-ONLY", "Whether this merges. Holds no Write or Edit"),
    ("security-engineer", "L2", "platform-architect", "opus", "VETO", "Vulnerabilities, receipt-chain verification, /audit"),
    ("sre", "L2", "platform-architect", "opus", "VETO", "Production instability blocks the release"),
    ("release-manager", "L2", "platform-architect", "sonnet", "", "Promotion and failure routing. Routes, never fixes"),
    ("dependency-steward", "L2", "platform-architect", "sonnet", "", "Fork log, pins, certification, Tier C teardown"),
]

FUNCTION = {
    "cto": "Direct", "product-owner": "Direct", "design-owner": "Direct",
    "web-architect": "Build", "data-architect": "Build", "platform-architect": "Build",
    "testing-architect": "Verify", "merge-authority": "Verify",
    "security-engineer": "Verify", "quality-compliance": "Verify",
    "release-manager": "Ship", "sre": "Ship", "dependency-steward": "Ship",
}

PLUGIN_OWNER: dict[str, str] = {}


def _own(officer: str, *plugins: str) -> None:
    for plugin in plugins:
        if plugin in PLUGIN_OWNER:
            raise SystemExit(f"duplicate ownership of plugin '{plugin}'")
        PLUGIN_OWNER[plugin] = officer


_own("web-architect",
     "backend-development", "frontend-mobile-development", "multi-platform-apps",
     "developer-essentials", "api-scaffolding", "python-development",
     "javascript-typescript", "systems-programming", "jvm-languages",
     "web-scripting", "functional-programming", "julia-development",
     "arm-cortex-microcontrollers", "shell-scripting", "dotnet-contribution",
     "payment-processing", "blockchain-web3", "game-development",
     "framework-migration", "codebase-cleanup", "code-refactoring",
     "debugging-toolkit")
_own("data-architect",
     "database-design", "database-migrations", "data-engineering",
     "data-validation-suite", "machine-learning-ops", "llm-application-dev",
     "llm-finetuning", "dgx-spark-ops", "runapi-mcp", "quantitative-trading",
     "application-performance", "database-cloud-optimization")
_own("platform-architect",
     "cloud-infrastructure", "kubernetes-operations", "deployment-strategies",
     "cicd-automation", "protect-mcp", "signed-audit-trails", "block-no-verify",
     "team-collaboration", "operating-kit")
_own("sre", "incident-response", "observability-monitoring", "distributed-debugging", "error-diagnostics")
_own("design-owner", "ui-design", "meigen-ai-design", "brand-landingpage", "pptx-deck-creation")
_own("product-owner",
     "seo-content-creation", "seo-technical-optimization", "seo-analysis-monitoring",
     "content-marketing", "social-publishing", "business-analytics",
     "startup-business-analyst", "before-you-build", "customer-sales-automation", "storymap-skill")
_own("testing-architect",
     "unit-testing", "qa-orchestra", "ciagent", "performance-testing-review",
     "tdd-workflows", "error-debugging")
_own("merge-authority", "comprehensive-review", "conductor", "skill-forge-essentials")
_own("security-engineer", "security-scanning", "backend-api-security", "frontend-mobile-security", "reverse-engineering")
_own("quality-compliance", "security-compliance", "accessibility-compliance", "hr-legal-compliance", "review-agent-governance")
_own("release-manager",
     "git-pr-workflows", "deployment-validation", "code-documentation",
     "documentation-generation", "documentation-standards", "c4-architecture",
     "api-testing-observability", "file-conversion")
_own("dependency-steward", "plugin-eval", "dependency-management", "pensyve", "context-management")
_own("cto", "agent-orchestration", "full-stack-orchestration", "agent-teams", "ship-mate")

DECLINED_PLUGINS = {
    "blockchain-web3", "game-development", "quantitative-trading",
    "arm-cortex-microcontrollers", "reverse-engineering",
}

DESIGN_GENERATORS = {
    "ui-ux-pro-max": {"source": "nextlevelbuilder/ui-ux-pro-max-skill", "licence": "UNVERIFIED"},
    "ui-design": {"source": "in-fork (wshobson)", "licence": "MIT"},
    "brand-landingpage": {"source": "in-fork (wshobson)", "licence": "MIT"},
}

UI_UX_PRO_MAX_FACTS = {
    "styles": "79 searchable (50 active)", "palettes": 192, "font_pairings": 74,
    "ux_guidelines": 119, "reasoning_rules": 192, "chart_types": 25, "stacks": 22,
}

LAB = {
    "db": "labs/lab.duckdb", "models": "labs/models", "automl": "pycaret==3.4.0",
    "python": "3.11-3.13", "owner": "data-architect",
    "licence_clearance": "web-compliance-engineer",
    "commercial_ok": ["CC0-1.0", "PDDL", "CC-BY-4.0", "CC-BY-SA-4.0", "ODC-BY",
                      "ODbL-1.0", "MIT", "Apache-2.0", "proprietary"],
    "rule": "A promoted model may ENTER the pipeline. It has not shipped.",
}

UPSTREAM = {
    "repo": "wshobson/agents", "licence": "MIT", "plugins": 94, "agents": 202,
    "skills": 183, "commands": 105, "orchestrators": 16,
    "agents_documented_by_name": 105, "stars": "39.5k", "forks": "4.2k",
    "commits": 569, "external_plugins": ["pensyve", "qa-orchestra", "storymap-skill", "ciagent"],
}

COMPANY = {
    "officers": len(OFFICERS), "engineers": UPSTREAM["agents"],
    "agents_total": len(OFFICERS) + UPSTREAM["agents"],
    "plugins_mapped": len(PLUGIN_OWNER),
    "vetoes": sum(1 for officer in OFFICERS if officer[4] == "VETO"),
    "read_only": sum(1 for officer in OFFICERS if officer[4] == "READ-ONLY"),
    "l3": sum(1 for officer in OFFICERS if officer[1] == "L3"),
    "l2": sum(1 for officer in OFFICERS if officer[1] == "L2"),
    "functions": len(set(FUNCTION.values())), "deepest_chain": 3,
    "invariants": 12, "gate_families": 9, "templates": 10,
    "name": IDENTITY["company"], "ceo": IDENTITY["ceo_full"],
}


def selfcheck() -> list[str]:
    errors = []
    names = [officer[0] for officer in OFFICERS]
    if len(names) != len(set(names)):
        errors.append("duplicate officer name")
    for name, _level, reports_to, *_ in OFFICERS:
        if reports_to != "CEO" and reports_to not in names:
            errors.append(f"{name} reports to '{reports_to}' which does not exist")
    if COMPANY["vetoes"] != 3:
        errors.append(f"veto count is {COMPANY['vetoes']}, must be exactly 3")
    if set(FUNCTION) != set(names):
        errors.append("FUNCTION map and OFFICERS disagree")
    if COMPANY["plugins_mapped"] != UPSTREAM["plugins"]:
        errors.append(f"{COMPANY['plugins_mapped']} plugins mapped, upstream has {UPSTREAM['plugins']}")
    levels = {officer[0]: officer[1] for officer in OFFICERS}
    order = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}
    for name, level, reports_to, *_ in OFFICERS:
        if reports_to != "CEO" and order[levels[reports_to]] <= order[level]:
            errors.append(f"authority inverts: {name} ({level}) reports to {reports_to} ({levels[reports_to]})")
    return errors


if __name__ == "__main__":
    import json
    import sys

    defects = selfcheck()
    for defect in defects:
        print(f"DEFECT  {defect}", file=sys.stderr)
    print(json.dumps(COMPANY, indent=2))
    sys.exit(1 if defects else 0)
