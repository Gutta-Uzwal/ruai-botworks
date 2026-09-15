# RU-AIBOTWORKS

Agentic AI employees that build and look after websites and Android apps.
CEO: Uzwal Gutta.

Start with the charter: [RU-AIBOTWORKS/DOCS/charter/RU-AIBOTWORKS-01-start-here.md](RU-AIBOTWORKS/DOCS/charter/RU-AIBOTWORKS-01-start-here.md).
Open the CEO portal: [RU-AIBOTWORKS/PORTAL/RU-AIBOTWORKS-index.html](RU-AIBOTWORKS/PORTAL/RU-AIBOTWORKS-index.html).

## Where things live

```text
RU-AIBOTWORKS/                 the company
  REGISTRY/                    single source of truth — edit here, nowhere else
    workforce/                 one file per department
  PLATFORM/                    the tooling that reads the registry
    templates/                 vendored inputs to the generators
  DEPARTMENTS/                 GENERATED — one package per agent
    _officers/                 GENERATED — the officers and team-lead promotions
  DATABASE/                    SQL Server schema (authored) and seed (GENERATED)
  PORTAL/                      GENERATED — CEO pages and the architecture diagram
  DOCS/                        build plan, ADRs, agent harness
    adr/                       decision records
    charter/                   GENERATED — start here, organisation, roster
projects/                      client work, one folder per site; built by the company
.claude/agents/                GENERATED — the officers Claude Code loads
.github/                       the UAT gate, instructions, the agentic-safety skill
scripts/agent_harness.py       repo-level tool-contract and receipt checks
agent-tools.json               GENERATED — the runtime-reachable tool surface
receipts/  review-receipts/    append-only, hash-chained audit trail
_builddocs/                    the original build kit, kept for provenance
  superseded/                  scripts the platform replaced
```

`agent_harness.py`, `agent-tools.json` and the receipt folders stay at the
repository root on purpose: the policy hooks resolve them from there.

## Naming

| Kind | Form | Example |
|---|---|---|
| Section | `UPPERCASE` | `REGISTRY/` |
| Folder below a section | `lowercase-kebab` | `workforce/`, `frontend-engineering/` |
| Data, doc or page file | `RU-AIBOTWORKS-<kebab>.<ext>` | `RU-AIBOTWORKS-tools.yaml` |
| Decision record | `RU-AIBOTWORKS-ADR-NNN-<kebab>.md` | `RU-AIBOTWORKS-ADR-003-mobile-lane.md` |
| Python module | `ru_aibotworks_<snake>.py` | `ru_aibotworks_genome.py` |
| Agent package | fixed names | `AGENT.md`, `SKILL.md` |

`ru_aibotworks_layout.py` enforces this in the gate.

## After changing the registry

```text
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_genome.py --validate
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_generate.py
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_charter.py
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_portal.py
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_archify.py
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_seed_sql.py
```
