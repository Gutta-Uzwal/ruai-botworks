# RU-AIBOTWORKS-ADR-001 — Agent construction model

**Status:** Accepted · **Date:** 2026-09-14 · **Decider:** CEO Uzwal Gutta
**Author:** Enterprise AI Architect · **Supersedes:** Build plan Stage 4 (fork strategy)

---

## Context

The build plan (`_builddocs/01-BUILD-FROM-SCRATCH.md`, Stage 4) assumed the workforce
would arrive by forking `wshobson/agents` — 202 agents across 94 plugins, MIT licensed.

On inspection, `.claude/plugins/` is **empty**. The fork was never vendored. The company
on disk is 13 officer files and zero engineers. `docs/charter/08-employee-roster.md`
documents 106 engineers by name, none of which exist as files.

Separately, `Production-Grade Enterprise Agentic Systems — Engineering Standard v1.0`
(STD-AGENT-001) requires, per agent, a machine-readable **registration record** (§34.1)
carrying `blast_radius` as a bound with a number, `autonomy_level`, `max_tier`,
`budgets`, `data_domains` and `incident_clocks`. Upstream agents carry none of these.
A forked agent therefore **cannot pass Appendix B** without all of that being authored
anyway.

## Decision

Build every agent natively, generated from a single governed registry.

1. **One source of truth.** All company data — officers, departments, teams, agents,
   tools, promotions — lives in `REGISTRY/` as reviewable YAML. Nothing
   about the company is authored anywhere else.
2. **Artifacts are generated, never hand-edited.** Agent charters, registration records,
   skills, tool contracts, the SQL seed and the CEO portal are all emitted by
   `PLATFORM/` from the registry. Editing a generated file is a defect.
3. **Identity compatibility is preserved.** Agent `name` and `plugin` values match the
   existing roster, so the upstream fork can still be adopted later and map 1:1 onto
   our governed identities. Ownership is not traded away for optionality.
4. **Every figure is computed.** No document asserts a headcount. Invariant 11 holds by
   construction because there is exactly one place a number can come from.

## The four planes we own

STD-AGENT-001 §5 defines seven planes. This repository is not a runtime, so it owns
four of them and declares the other three as deployment obligations:

| Plane | Owned here | Artifact |
|---|---|---|
| 2. Policy | yes | Cedar policy generated from the registry's tiers and scopes |
| 6. Tool and data | yes | `ru-aibotworks-tools.yaml` — complete contracts, §10 |
| 7. Observability | yes | Hash-chained receipts, append-only, `receipts/` |
| — Governance | yes | Registration records, autonomy ladder, blast radius |
| 1. Control | **no — deployment obligation** | Kill switch, lease issuer, run registry |
| 3. Identity | **no — deployment obligation** | Short-lived scoped credentials |
| 5. Execution | **no — deployment obligation** | Kernel/hypervisor isolation |

Stating this explicitly is itself a control. A repository that claims to enforce
sandboxing it does not run is worse than one that names the gap.

## Consequences

**Gained.** Full ownership and design control of every agent. Standard compliance is
structural rather than retrofitted. Headcount is discovered from the registry, never
asserted. Departments can be added — HR, Payroll, Finance, Service Management — without
a second source of truth.

**Cost.** We maintain 100% of the workforce. There is no upstream to inherit fixes from.
The generator becomes load-bearing infrastructure and must itself be tested.

**Rejected alternatives.**

| Alternative | Rejected because |
|---|---|
| Fork `wshobson/agents` as planned | Registration records, blast radii and tool contracts must be authored regardless. The fork saves prose, not compliance work. |
| Hybrid — native officers, forked engineers | Two sources of truth. Invariant 11 becomes unenforceable across the boundary. |

---

## Related

- [RU-AIBOTWORKS-ADR-002](RU-AIBOTWORKS-ADR-002-organisation-structure.md) — organisation structure
- [RU-AIBOTWORKS-ADR-003](RU-AIBOTWORKS-ADR-003-mobile-lane.md) — mobile lane
