# RU AI Botworks — start here

<!-- The constitution. Hand-authored. Figures derive from scripts/company.py. -->

**CEO:** Uzwal Gutta (alias Ujwal Gutta) · **Officers:** 13 · **Engineers:** 202 · **215 agents total**

## What this company is

A software company with one CEO and **215 agents**.

202 came from `wshobson/agents` — 94 plugins, 183 skills,
105 commands, 16 orchestrators, **MIT licensed**.
They were forked, vendored and brought in-house. 13 more were written here:
the officers who decide, review, and stop releases.

**All 215 are owned outright.** MIT grants the right to use, copy, modify,
merge, publish, distribute, sublicense and sell. The grant is perpetual and cannot
be revoked. The CEO holds complete authority over every file.

Ownership carries a second edge: **what you own, you maintain.**

## What it sells

Ten website templates, built to order, through a gate nothing bypasses. The
product is not the code — everyone has AI writing code now. The product is
**provable build quality**:

- 9 deterministic job families, all green or nothing ships
- A read-only reviewer reporting outside the team that wrote the code
- Human approval before any merge
- 3 vetoes only the CEO can override
- An Ed25519-signed, hash-chained, offline-verifiable receipt for every action

## The ten standing rules

**1. Every agent is owned and governed.** All 215 carry a reporting line and a
decision level. An agent nobody governs is an agent nobody is accountable for.

**2. No orchestrator answers `/build`.** The 16 orchestrators are invoked *by* an
officer, *inside* a phase. Capability does not confer authority.

**3. The fork is the source of truth. Upstream is an input.** Merges are reviewed,
certified and accepted deliberately — never pulled automatically.

**4. Stay mergeable.** Company frontmatter uses keys upstream does not, so merges
stay clean. Extend by default; rewrite by decision; log every divergence.

**5. Certify before use.** Every plugin passes `plugin-eval` before first use and
on every pin bump.

**6. Policy is written from receipts, never imagination.** `protect-mcp` runs in
audit mode for one full build first.

**7. A flaky check never blocks promotion.** `ciagent` is advisory. A flaky
blocker teaches people to bypass the gate.

**8. Tier C is uninstalled between projects.** The discipline everyone skips.

**9. Every project has a `DESIGN.md`.** The only defence against ten siblings.

**10. The CEO cannot be the one who ships.** Officers under delivery pressure must
not hold the stop button.

## The four decisions that are yours alone

| Decision | Why it cannot be delegated |
|---|---|
| **What to build** | Commercial priority |
| **Whether the design is right** | The anti-sameness judgement |
| **Whether to override a veto** | 3 officers can stop a release; only you unstop it |
| **Off-stack technology** | Changes cost structure, not just stack |

## The document set

| # | Document | Answers |
|---|---|---|
| 01 | `01-BUILD-FROM-SCRATCH.md` | **Every command, in order, from an empty folder** |
| 02 | `02-organisation.md` | The 13 officers, vetoes, dispatch map |
| 03 | `03-architecture.md` | Layers, fork log, 12 invariants, the gate |
| 04 | `04-workflow.md` | Phases, dispatch mechanic, routing, commands |
| 05 | `05-project-catalogue.md` | Ten templates, two lanes, what we decline |
| 06 | `06-ceo-manual.md` | Running it: capacity, cost, veto discipline |
| 07 | `07-ownership-and-licence.md` | What is owned, under what terms |
| 08 | `08-employee-roster.md` | **Generated** — every engineer in the tree |
| 09 | `09-roster-standard.md` | Roles, responsibilities, assignment rules |
| 10 | `10-data-engineering-pipeline.md` | Spec in, PySpark out, Copilot builds it |
| 11 | `11-data-lab.md` | Kaggle → DuckDB → PyCaret, and the licence gate out |

Scripts: `company.py` (source of truth), `roster.py`, `check_consistency.py`,
`check_authorship.py`, `lab/kaggle_ingest.py`, `lab/lab_run.py`.

## What is rejected

| Rejected | Because |
|---|---|
| Ruflo, ECC, Superpowers, OpenHands | Rival lifecycles. Two orchestrators means ambiguous routing |
| OpenViking | `pensyve` ships in the marketplace already pinned |
| ui-ux-pro-max | `ui-design` + `brand-landingpage` are in-ecosystem |
| Installing all 94 plugins | The author's own design says don't |
| Agency Swarm, AgentVerse | Python frameworks. Rewriting the company in code to gain nothing |

<!-- MANUAL:START id=charter-notes -->
Amendments, and what forced them.
<!-- MANUAL:END id=charter-notes -->
