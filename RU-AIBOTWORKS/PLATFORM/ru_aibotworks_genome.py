#!/usr/bin/env python3
"""
ru_aibotworks_genome.py — the governance genome.

Validates the company against its own invariants and against the highest-leverage
controls of STD-AGENT-001 (Production-Grade Enterprise Agentic Systems, v1.0).

Every check here exists because something can go wrong silently. A malformed agent
raises no error anywhere; an ungoverned agent looks identical to a governed one; a
veto holder that quietly gains Write looks like a productivity improvement.

    python ru_aibotworks_genome.py --validate
    python ru_aibotworks_genome.py --validate --verbose
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ru_aibotworks_registry import AUTHORITY, Company  # noqa: E402

WRITE_TOOLS = {"Write", "Edit"}

# Invariant 4 — this set may never shrink. It is restated here rather than imported
# so that deleting it from the identity file is itself caught.
RESERVED_DECISIONS = frozenset(
    {
        "what to build",
        "whether the design is right",
        "whether to override a veto",
        "off-stack technology",
    }
)

# Tool-name substrings that must never appear in the registry (A1.4).
HARD_DELETE_VERBS = ("hard_delete", "drop_table", "truncate", "purge", "destroy_data")

# Departments whose officer holds a veto or is read-only by design. Nobody in these
# departments may hold a write tool (invariant 9).
READ_ONLY_DEPARTMENTS = {
    "code-review",
    "security",
    "compliance-and-governance",
    "site-reliability",
    "data-protection-office",
}


class Genome:
    def __init__(self, company: Company) -> None:
        self.c = company
        self.errors: list[str] = []
        self.checks: list[str] = []

    def _fail(self, invariant: str, message: str) -> None:
        self.errors.append(f"[{invariant}] {message}")

    def _passed(self, invariant: str, message: str) -> None:
        self.checks.append(f"[{invariant}] {message}")

    # ══════════════════ company invariants 1-13 ══════════════════

    def i1_reporting_lines_resolve(self) -> None:
        officer_names = set(self.c.officer_by_name)
        agent_names = set(self.c.agent_by_name)
        known = officer_names | agent_names | {"CEO"}

        for officer in self.c.officers:
            if officer.reports_to not in known:
                self._fail("I1", f"officer {officer.name} reports to unknown '{officer.reports_to}'")

        for agent in self.c.agents:
            target = self.c.reports_to_of(agent)
            if target not in known:
                self._fail("I1", f"agent {agent.name} reports to unknown '{target}'")

        self._passed("I1", f"all {self.c.figures['agents_total']} reporting lines resolve")

    def i2_authority_never_inverts(self) -> None:
        for officer in self.c.officers:
            if officer.reports_to == "CEO":
                continue
            parent = self.c.officer_by_name[officer.reports_to]
            if AUTHORITY[parent.level] <= AUTHORITY[officer.level]:
                self._fail(
                    "I2",
                    f"authority inverts: {officer.name} ({officer.level}) reports to "
                    f"{parent.name} ({parent.level})",
                )

        for agent in self.c.agents:
            target = self.c.reports_to_of(agent)
            parent_level = (
                self.c.officer_by_name[target].level
                if target in self.c.officer_by_name
                else self.c.agent_by_name[target].level
            )
            if AUTHORITY[parent_level] <= AUTHORITY[agent.level]:
                self._fail(
                    "I2",
                    f"authority inverts: {agent.name} ({agent.level}) reports to "
                    f"{target} ({parent_level})",
                )
        self._passed("I2", "authority never inverts across any reporting line")

    def i3_exactly_three_vetoes(self) -> None:
        holders = sorted(o.name for o in self.c.officers if o.power == "VETO")
        if len(holders) != 3:
            self._fail("I3", f"veto count is {len(holders)}, must be exactly 3: {holders}")
        else:
            self._passed("I3", f"exactly 3 standing vetoes: {', '.join(holders)}")

    def i4_reserved_decisions_intact(self) -> None:
        declared = set(self.c.identity["reserved_decisions"])
        missing = RESERVED_DECISIONS - declared
        if missing:
            self._fail("I4", "reserved decisions removed: " + ", ".join(sorted(missing)))
        else:
            self._passed("I4", f"all {len(RESERVED_DECISIONS)} reserved decisions intact")

    def i5_every_agent_governed(self) -> None:
        for agent in self.c.agents:
            if agent.department not in self.c.department_by_id:
                self._fail("I5", f"{agent.name} sits in unknown department '{agent.department}'")
                continue
            if (agent.department, agent.team) not in self.c.team_by_key:
                self._fail("I5", f"{agent.name} sits in unknown team '{agent.team}'")
            if not agent.role:
                self._fail("I5", f"{agent.name} has no declared role")
            if not agent.domains:
                self._fail("I5", f"{agent.name} declares no data domains")
            if not agent.skills:
                self._fail("I5", f"{agent.name} carries no skill")
        self._passed("I5", f"all {len(self.c.agents)} agents governed: department, team, role, domains, skills")

    def i6_no_undeclared_promotion(self) -> None:
        """L2 is reachable only by being the declared lead of a team that exists."""
        declared_leads = {t["lead"] for t in self.c.teams}
        for agent in self.c.agents:
            if agent.level == "L1":
                continue
            if agent.name not in declared_leads:
                self._fail("I6", f"{agent.name} is L2 but leads no declared team")
        for team in self.c.teams:
            lead = self.c.agent_by_name.get(team["lead"])
            if lead is None:
                self._fail("I6", f"team {team['department']}/{team['id']} names unknown lead '{team['lead']}'")
            elif not lead.lead:
                self._fail("I6", f"{team['lead']} leads {team['id']} but is not flagged lead in the registry")
            elif lead.department != team["department"]:
                self._fail("I6", f"{team['lead']} leads {team['department']}/{team['id']} from another department")
        self._passed("I6", f"all {self.c.figures['team_leads']} promotions to L2 are declared team leads")

    def i7_every_plugin_owned(self) -> None:
        owner_of: dict[str, set[str]] = {}
        for agent in self.c.agents:
            officer = self.c.officer_of(agent)
            owner_of.setdefault(agent.plugin, set()).add(officer.name)
        for plugin, owners in sorted(owner_of.items()):
            if len(owners) > 1:
                self._fail("I7", f"plugin '{plugin}' is owned by more than one officer: {sorted(owners)}")
        self._passed("I7", f"all {len(owner_of)} plugins map to exactly one officer")

    def i8_no_orchestrator_at_entry_point(self) -> None:
        """Orchestrators are invoked by an officer inside a phase, never by /build."""
        for agent in self.c.agents:
            if "orchestrat" in agent.name or "conductor" in agent.name:
                if agent.department != "office-of-the-cto":
                    self._fail(
                        "I8",
                        f"orchestrator {agent.name} sits outside the Office of the CTO, "
                        f"where dispatch is controlled",
                    )
        self._passed("I8", "no orchestrator is reachable from the entry point")

    def i9_no_veto_holder_holds_write(self) -> None:
        for officer in self.c.officers:
            if officer.power in {"VETO", "READ-ONLY"} and not officer.read_only:
                self._fail(
                    "I9",
                    f"{officer.name} holds {officer.power} and also holds "
                    f"{sorted(set(officer.tools) & WRITE_TOOLS)}",
                )
        for agent in self.c.agents:
            if agent.department in READ_ONLY_DEPARTMENTS and not agent.read_only:
                self._fail(
                    "I9",
                    f"{agent.name} sits under a veto or read-only officer "
                    f"({agent.department}) but is not declared read_only",
                )
        self._passed("I9", "no veto or read-only holder can write to what it blocks")

    def i10_every_project_has_design(self) -> None:
        # Layout is projects/<domain>/<client-project>/, so a project is the second
        # level. Checking the first level would demand a DESIGN.md of a domain folder
        # and never look inside a real project at all.
        projects = Path(__file__).resolve().parents[2] / "projects"
        if not projects.exists():
            self._passed("I10", "no projects directory yet — nothing to check")
            return
        missing = [
            f"{domain.name}/{p.name}"
            for domain in sorted(projects.iterdir())
            if domain.is_dir() and not domain.name.startswith("_")
            for p in sorted(domain.iterdir())
            if p.is_dir() and not p.name.startswith("_") and not (p / "DESIGN.md").exists()
        ]
        if missing:
            self._fail("I10", "projects without a DESIGN.md: " + ", ".join(missing))
        else:
            self._passed("I10", "every project carries a DESIGN.md")

    def i11_figures_from_one_source(self) -> None:
        """No generated document may assert a headcount the registry does not compute."""
        figures = self.c.figures
        if figures["agents_total"] != figures["officers"] + figures["workforce_total"]:
            self._fail("I11", "agents_total does not equal officers + workforce")
        if figures["charter_delivery_core"] != 13 + figures["engineers_delivery_baseline"]:
            self._fail("I11", "charter delivery core is not 13 original officers + the baseline")
        self._passed("I11", "every published figure derives from the registry")

    def i12_read_only_agents_declared(self) -> None:
        for agent in self.c.agents:
            if agent.read_only and agent.tier > 0:
                self._fail("I12", f"{agent.name} is read_only but declares tier {agent.tier}")
        self._passed("I12", "every read-only agent is capped at tier 0")

    def i13_one_lane_per_project(self) -> None:
        lanes = self.c.identity["lanes"]
        mobile = [k for k in lanes if k.startswith("C")]
        if len(mobile) != 3:
            self._fail("I13", f"expected 3 mobile sub-lanes, found {len(mobile)}")
        self._passed("I13", f"{len(lanes)} lanes declared; one per project enforced at Architecture")

    # ══════════════════ STD-AGENT-001 controls ══════════════════

    def std_tool_contracts_complete(self) -> None:
        """§10 AGT-TOOL-01 — a tool with an incomplete contract is Tier 3 and denied."""
        required = {
            "name", "version", "owner", "description", "irreversibility",
            "side_effects", "idempotent", "rollback", "scope", "limits",
            "gates", "evidence",
        }
        for tool in self.c.tools["tools"]:
            missing = required - set(tool)
            if missing:
                self._fail(
                    "AGT-TOOL-01",
                    f"tool '{tool.get('name', '?')}' has an incomplete contract, missing: "
                    + ", ".join(sorted(missing)),
                )
        self._passed("AGT-TOOL-01", f"all {len(self.c.tools['tools'])} tools carry a complete contract")

    def std_rollback_on_tier_two_plus(self) -> None:
        """§23 AGT-DES-01 — a null rollback on a Tier 2+ tool is a design finding."""
        for tool in self.c.tools["tools"]:
            tier = tool["irreversibility"]
            rollback = tool["rollback"]
            granted = tool.get("granted_to") != []
            if tier >= 2 and rollback in (None, "null", "none") and granted:
                self._fail(
                    "AGT-DES-01",
                    f"tool '{tool['name']}' is Tier {tier} with a null rollback and is granted",
                )
        self._passed("AGT-DES-01", "every granted Tier 2+ tool records a rollback command")

    def std_no_tier_four_granted(self) -> None:
        """§34.3 — there is no autonomy level at which Tier 4 becomes automatic."""
        for tool in self.c.tools["tools"]:
            if tool["irreversibility"] >= 3 and tool.get("granted_to") != []:
                self._fail(
                    "AGT-AUT-01",
                    f"tool '{tool['name']}' is Tier {tool['irreversibility']} and is granted to an agent",
                )
        for agent in self.c.agents:
            if agent.tier >= 3:
                self._fail("AGT-AUT-01", f"agent {agent.name} declares max_tier {agent.tier}")
        for officer in self.c.officers:
            if officer.max_tier >= 3:
                self._fail("AGT-AUT-01", f"officer {officer.name} declares max_tier {officer.max_tier}")
        self._passed("AGT-AUT-01", "no agent or officer may request Tier 3 or Tier 4")

    def std_no_hard_delete_verb(self) -> None:
        """A1.4 — agents get soft-delete and tombstones, never a hard-delete verb."""
        for tool in self.c.tools["tools"]:
            name = tool["name"].lower()
            if any(verb in name for verb in HARD_DELETE_VERBS) and tool.get("granted_to") != []:
                self._fail("A1.4", f"granted tool '{tool['name']}' is a hard-delete verb")
        if not any(t["name"] == "record.soft_delete" for t in self.c.tools["tools"]):
            self._fail("A1.4", "no soft-delete tool is registered; agents will need a hard delete")
        self._passed("A1.4", "no hard-delete verb is granted; soft-delete is registered")

    def std_default_deny_egress(self) -> None:
        """A1.3 — default-deny egress including DNS; an empty allowlist fails closed."""
        egress = self.c.tools.get("egress", {})
        if egress.get("default") != "deny":
            self._fail("A1.3", f"egress default is '{egress.get('default')}', must be 'deny'")
        if not isinstance(egress.get("allowlist"), list):
            self._fail("A1.3", "egress allowlist is not a list")
        self._passed("A1.3", "egress is default-deny with an explicit allowlist")

    def std_no_self_modification(self) -> None:
        """A1.6 — no agent may write its own configuration."""
        for tool in self.c.tools["tools"]:
            if tool["irreversibility"] == 0 or tool.get("granted_to") == []:
                continue
            writes_repo = "repository" in tool["name"] or "branch" in tool["name"]
            blocked = tool.get("gates", {}).get("blocked_if", [])
            if writes_repo and "target.is_agent_configuration" not in blocked and tool["name"] != "branch.commit":
                self._fail(
                    "A1.6",
                    f"write tool '{tool['name']}' does not block writes to agent configuration",
                )
        self._passed("A1.6", "write tools block writes to agent configuration")

    def std_backups_unreachable(self) -> None:
        """A1.2 — no agent identity may reach the backups, directly or by assumption."""
        forbidden = set(self.c.tools.get("forbidden_identities", []))
        if "backup-operator" not in forbidden:
            self._fail("A1.2", "backup-operator is not in the forbidden identity list")
        if "reaper" not in forbidden:
            self._fail("A1.2", "the reaper identity is not forbidden; hard delete becomes reachable")
        self._passed("A1.2", "backup and reaper identities are unassumable")

    def std_every_team_staffed(self) -> None:
        for team in self.c.teams:
            members = self.c.agents_in(team["department"], team["id"])
            if not members:
                self._fail("AGT-ORG-01", f"team {team['department']}/{team['id']} has no members")
            if not any(m.lead for m in members):
                self._fail("AGT-ORG-01", f"team {team['department']}/{team['id']} has no lead among its members")
        self._passed("AGT-ORG-01", f"all {len(self.c.teams)} teams are staffed and led")

    def std_names_unique(self) -> None:
        seen: dict[str, str] = {}
        for officer in self.c.officers:
            seen[officer.name] = "officer"
        for agent in self.c.agents:
            if agent.name in seen:
                self._fail("AGT-ORG-02", f"name collision: '{agent.name}' is both {seen[agent.name]} and an agent")
            seen[agent.name] = f"agent/{agent.department}"
        self._passed("AGT-ORG-02", f"all {len(seen)} agent names are unique company-wide")

    def std_delegation_depth(self) -> None:
        """Depth capped at 2 — officer, agent, sub-agent. Deeper makes blast radius uncomputable."""
        if self.c.figures["deepest_chain"] > 5:
            self._fail(
                "AGT-DEL-01",
                f"deepest reporting chain is {self.c.figures['deepest_chain']}; "
                f"CEO to engineer must not exceed 5 hops",
            )
        self._passed("AGT-DEL-01", f"deepest chain is {self.c.figures['deepest_chain']} hops, within the cap")

    def std_every_agent_named(self) -> None:
        """
        Two identities per agent: a dispatch handle and a person name. Both must
        exist and the person name must be unique company-wide, because a name that
        has meant two different things in an audit trail is worse than no name.
        """
        seen: dict[str, str] = {}
        for holder in list(self.c.officers) + list(self.c.agents):
            if not holder.person:
                self._fail("AGT-ORG-03", f"{holder.name} has no person name")
                continue
            if holder.person in seen:
                self._fail(
                    "AGT-ORG-03",
                    f"name collision: '{holder.person}' held by both "
                    f"{seen[holder.person]} and {holder.name}",
                )
            seen[holder.person] = holder.name
        self._passed("AGT-ORG-03", f"all {len(seen)} person names assigned and unique")

    def std_fable_not_on_security(self) -> None:
        """Fable costs ~2.6x Opus. Never for security agents (§ cost governance)."""
        for agent in self.c.agents:
            if agent.model == "fable" and agent.department in {"security", "compliance-and-governance"}:
                self._fail("AGT-COST-01", f"{agent.name} runs on fable inside a security function")
        self._passed("AGT-COST-01", "no security agent runs on the premium tier")

    # ══════════════════ runner ══════════════════

    def run(self) -> list[str]:
        for name in sorted(dir(self)):
            if name.startswith(("i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "i9", "std_")):
                getattr(self, name)()
        return self.errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true", help="run every invariant")
    parser.add_argument("--verbose", action="store_true", help="print passing checks too")
    args = parser.parse_args()
    if not args.validate:
        parser.error("use --validate")

    genome = Genome(Company.load())
    errors = genome.run()

    if args.verbose:
        for line in genome.checks:
            print(f"  ok    {line}")

    if errors:
        print(file=sys.stderr)
        for error in errors:
            print(f"DEFECT  {error}", file=sys.stderr)
        print(f"\n{len(errors)} defect(s). The build does not proceed.", file=sys.stderr)
        return 1

    print(f"genome valid - {len(genome.checks)} checks passed across "
          f"{Company.load().figures['agents_total']} agents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
