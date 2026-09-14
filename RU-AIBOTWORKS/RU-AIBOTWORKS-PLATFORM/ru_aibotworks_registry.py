#!/usr/bin/env python3
"""
ru_aibotworks_registry.py — the single computed source for every RU-AIBOTWORKS figure.

Invariant 11: any figure appearing in two documents derives from one computed source.
This is that source. Nothing here is asserted; everything is counted from the registry
YAML. A document that disagrees with this module fails the consistency check.

    python ru_aibotworks_registry.py            # print the company figures as JSON
    python ru_aibotworks_registry.py --table    # print them as a readable table
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any

import yaml

REGISTRY_DIR = Path(__file__).resolve().parent.parent / "RU-AIBOTWORKS-REGISTRY"
NAMES_FILE = "ru-aibotworks-names.yaml"
WORKFORCE_DIR = REGISTRY_DIR / "workforce"

# Levels. Team leads are L2 by logged promotion; every other engineer is L1.
LEVEL_ENGINEER = "L1"
LEVEL_LEAD = "L2"

AUTHORITY = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}

# Departments whose headcount is the charter's delivery baseline of 202. Mobile and
# the corporate departments are additions and are counted separately so the growth
# is visible rather than absorbed.
DELIVERY_BASELINE_DEPARTMENTS = {
    "office-of-the-cto",
    "product",
    "design",
    "web-engineering",
    "data-and-ai",
    "platform-engineering",
    "quality-engineering",
    "code-review",
    "security",
    "compliance-and-governance",
    "release-engineering",
    "site-reliability",
    "supply-chain",
}
MOBILE_EXPANSION_DEPARTMENTS = {"mobile-engineering"}
CORPORATE_DEPARTMENTS = {
    "human-resources",
    "payroll",
    "finance",
    "service-management",
    "data-protection-office",
}


def _load(name: str) -> Any:
    path = REGISTRY_DIR / name
    if not path.exists():
        raise SystemExit(f"registry file missing: {path}")
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


@dataclass(frozen=True)
class Agent:
    """One non-officer agent. Its level is computed, never declared."""

    name: str
    role: str
    model: str
    plugin: str
    department: str
    team: str
    tier: int
    lead: bool
    read_only: bool
    domains: tuple[str, ...]
    skills: tuple[dict[str, str], ...]
    level: str = LEVEL_ENGINEER
    person: str = ""   # the name a human uses; `name` is the dispatch handle

    @property
    def cohort(self) -> str:
        if self.department in CORPORATE_DEPARTMENTS:
            return "corporate"
        if self.department in MOBILE_EXPANSION_DEPARTMENTS:
            return "mobile-expansion"
        return "delivery-baseline"


@dataclass(frozen=True)
class Officer:
    name: str
    level: str
    reports_to: str
    function: str
    division: str
    model: str
    power: str
    decides: str
    max_tier: int
    tools: tuple[str, ...]
    added: str
    charter: str
    refuses: str
    person: str = ""

    @property
    def read_only(self) -> bool:
        return "Write" not in self.tools and "Edit" not in self.tools


@dataclass
class Company:
    identity: dict[str, Any] = field(default_factory=dict)
    officers: list[Officer] = field(default_factory=list)
    departments: list[dict[str, Any]] = field(default_factory=list)
    agents: list[Agent] = field(default_factory=list)
    tools: dict[str, Any] = field(default_factory=dict)

    # ─────────────────────────── loading ───────────────────────────
    @classmethod
    def load(cls) -> "Company":
        identity = _load("ru-aibotworks-identity.yaml")
        names = (
            (_load(NAMES_FILE) or {}).get("assigned", {})
            if (REGISTRY_DIR / NAMES_FILE).exists()
            else {}
        )
        officers = [
            Officer(
                name=o["name"],
                level=o["level"],
                reports_to=o["reports_to"],
                function=o["function"],
                division=o["division"],
                model=o["model"],
                power=o.get("power", "") or "",
                decides=o["decides"],
                max_tier=int(o["max_tier"]),
                tools=tuple(o["tools"]),
                added=o.get("added", "original"),
                charter=" ".join(o["charter"].split()),
                refuses=" ".join(o["refuses"].split()),
                person=names.get(o["name"], ""),
            )
            for o in _load("ru-aibotworks-officers.yaml")["officers"]
        ]
        departments = _load("ru-aibotworks-departments.yaml")["departments"]
        tools = _load("ru-aibotworks-tools.yaml")

        officer_level = {o.name: o.level for o in officers}
        department_officer = {d["id"]: d["officer"] for d in departments}

        agents: list[Agent] = []
        for path in sorted(WORKFORCE_DIR.glob("ru-aibotworks-*.yaml")):
            with path.open(encoding="utf-8") as handle:
                doc = yaml.safe_load(handle)
            dept = doc["department"]
            # A team lead is promoted to L2 only where there is room above it: the
            # department's officer must be L3 or higher. Under an L2 officer the lead
            # coordinates at L1, because an L2 reporting to an L2 inverts authority.
            owning_level = officer_level[department_officer[dept]]
            lead_gets_l2 = AUTHORITY[owning_level] > AUTHORITY[LEVEL_LEAD]
            for a in doc["agents"]:
                is_lead = bool(a.get("lead", False))
                agents.append(
                    Agent(
                        name=a["name"],
                        role=a["role"],
                        model=a["model"],
                        plugin=a["plugin"],
                        department=dept,
                        team=a["team"],
                        tier=int(a["tier"]),
                        lead=is_lead,
                        read_only=bool(a.get("read_only", False)),
                        domains=tuple(a.get("domains", [])),
                        skills=tuple(a.get("skills", [])),
                        level=LEVEL_LEAD if (is_lead and lead_gets_l2) else LEVEL_ENGINEER,
                        person=names.get(a["name"], ""),
                    )
                )
        return cls(identity, officers, departments, agents, tools)

    # ─────────────────────────── lookups ───────────────────────────
    @cached_property
    def officer_by_name(self) -> dict[str, Officer]:
        return {o.name: o for o in self.officers}

    @cached_property
    def agent_by_name(self) -> dict[str, Agent]:
        return {a.name: a for a in self.agents}

    @cached_property
    def department_by_id(self) -> dict[str, dict[str, Any]]:
        return {d["id"]: d for d in self.departments}

    @cached_property
    def teams(self) -> list[dict[str, Any]]:
        out = []
        for dept in self.departments:
            for team in dept["teams"]:
                out.append({**team, "department": dept["id"], "officer": dept["officer"]})
        return out

    @cached_property
    def team_by_key(self) -> dict[tuple[str, str], dict[str, Any]]:
        return {(t["department"], t["id"]): t for t in self.teams}

    def agents_in(self, department: str, team: str | None = None) -> list[Agent]:
        return [
            a
            for a in self.agents
            if a.department == department and (team is None or a.team == team)
        ]

    def officer_of(self, agent: Agent) -> Officer:
        return self.officer_by_name[self.department_by_id[agent.department]["officer"]]

    def reports_to_of(self, agent: Agent) -> str:
        """
        An engineer reports to its team lead, and a lead to its department officer.

        Where the department's officer is itself L2, the lead was not promoted (there
        is no room above it), so the department is flat: every member reports to the
        officer directly and the lead coordinates without a reporting line under it.
        """
        dept = self.department_by_id[agent.department]
        if agent.lead:
            return dept["officer"]
        lead_name = self.team_by_key[(agent.department, agent.team)]["lead"]
        lead = self.agent_by_name.get(lead_name)
        if lead is None or lead.level != LEVEL_LEAD:
            return dept["officer"]
        return lead_name

    # ─────────────────────────── figures ───────────────────────────
    @cached_property
    def figures(self) -> dict[str, Any]:
        by_cohort: dict[str, int] = {}
        for a in self.agents:
            by_cohort[a.cohort] = by_cohort.get(a.cohort, 0) + 1

        models: dict[str, int] = {}
        for a in self.agents:
            models[a.model] = models.get(a.model, 0) + 1

        tiers: dict[int, int] = {}
        for a in self.agents:
            tiers[a.tier] = tiers.get(a.tier, 0) + 1

        officers_added = sum(1 for o in self.officers if o.added != "original")
        leads = sum(1 for a in self.agents if a.lead)
        promoted = sum(1 for a in self.agents if a.level == LEVEL_LEAD)

        registered_tools = self.tools["tools"]
        granted_tools = [t for t in registered_tools if t.get("granted_to") != []]

        return {
            "company": self.identity["company"]["name"],
            "ceo": self.identity["ceo"]["full"],
            # headcount
            "officers": len(self.officers),
            "officers_original": len(self.officers) - officers_added,
            "officers_added": officers_added,
            "engineers_delivery_baseline": by_cohort.get("delivery-baseline", 0),
            "engineers_mobile_expansion": by_cohort.get("mobile-expansion", 0),
            "staff_corporate": by_cohort.get("corporate", 0),
            "workforce_total": len(self.agents),
            "agents_total": len(self.officers) + len(self.agents),
            "charter_delivery_core": 13 + by_cohort.get("delivery-baseline", 0),
            # structure
            "divisions": len({d["division"] for d in self.departments}),
            "departments": len(self.departments),
            "teams": len(self.teams),
            "team_leads": leads,
            "team_leads_promoted_l2": promoted,
            "team_leads_coordinating_l1": leads - promoted,
            "functions": len({o.function for o in self.officers}),
            "deepest_chain": self.deepest_chain,
            # authority
            "chiefs_l4": sum(1 for o in self.officers if o.level == "L4"),
            "officers_l3": sum(1 for o in self.officers if o.level == "L3"),
            "officers_l2": sum(1 for o in self.officers if o.level == "L2"),
            "vetoes": sum(1 for o in self.officers if o.power == "VETO"),
            "read_only_officers": sum(1 for o in self.officers if o.read_only),
            "reserved_decisions": len(self.identity["reserved_decisions"]),
            "ceo_direct_reports": sum(1 for o in self.officers if o.reports_to == "CEO"),
            # tooling and delivery
            "tools_registered": len(registered_tools),
            "tools_granted": len(granted_tools),
            "tools_registered_denied": len(registered_tools) - len(granted_tools),
            "max_tier_granted": max(
                (t["irreversibility"] for t in granted_tools), default=0
            ),
            "lanes": len(self.identity["lanes"]),
            "templates": len(self.identity["templates"]),
            "plugins_mapped": len({a.plugin for a in self.agents}),
            "skills_total": sum(len(a.skills) for a in self.agents),
            "named": sum(1 for a in self.agents if a.person)
                     + sum(1 for o in self.officers if o.person),
            "unnamed": sum(1 for a in self.agents if not a.person)
                       + sum(1 for o in self.officers if not o.person),
            "model_mix": dict(sorted(models.items(), key=lambda kv: -kv[1])),
            "tier_mix": dict(sorted(tiers.items())),
        }

    @cached_property
    def deepest_chain(self) -> int:
        """Longest reporting chain from CEO down to a leaf engineer."""

        def officer_depth(name: str, seen: frozenset[str]) -> int:
            if name == "CEO" or name in seen:
                return 0
            officer = self.officer_by_name.get(name)
            if officer is None:
                return 0
            return 1 + officer_depth(officer.reports_to, seen | {name})

        officer_hops = max(
            (officer_depth(o.name, frozenset()) for o in self.officers), default=0
        )
        # engineers add one hop under their officer, leads one, members two
        member_extra = 2 if any(not a.lead for a in self.agents) else 1
        return officer_hops + member_extra


def main() -> int:
    company = Company.load()
    figures = company.figures
    if "--table" in sys.argv:
        width = max(len(k) for k in figures)
        for key, value in figures.items():
            if isinstance(value, dict):
                value = ", ".join(f"{k}={v}" for k, v in value.items())
            print(f"{key.ljust(width)}  {value}")
    else:
        print(json.dumps(figures, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
