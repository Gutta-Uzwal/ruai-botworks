# RU-AIBOTWORKS

Agentic AI employees that build and look after websites and Android apps.
CEO: Uzwal Gutta.

Start with the charter: [ru-aibotworks/docs/charter/01-start-here.md](ru-aibotworks/docs/charter/01-start-here.md).
Open the CEO portal: [ru-aibotworks/portal/index.html](ru-aibotworks/portal/index.html).

## Where things live

```text
ru-aibotworks/                 the company
  registry/                    single source of truth — edit here, nowhere else
    workforce/                 one file per department
  platform/                    the tooling that reads the registry
    templates/                 vendored inputs to the generators
  departments/                 GENERATED — one package per agent
    _officers/                 GENERATED — the officers and team-lead promotions
  database/                    SQL Server schema (authored) and seed (GENERATED)
  portal/                      GENERATED — CEO pages and the architecture diagram
  docs/                        build plan, ADRs, agent harness
    adr/                       decision records
    charter/                   GENERATED — start here, organisation, roster
designs/                        the design standard, plus one brief per domain
  <domain>/                    e.g. school — emotional target, colour, page architecture
templates/                     reference builds shown to prospective clients
  <domain>/<template-name>/    e.g. school/premium-v1
projects/                      real client work, copied from a template and diverged
  <domain>/<client-project>/
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
| Section | `lowercase` | `registry/` |
| Folder below a section | `lowercase-kebab` | `workforce/`, `frontend-engineering/` |
| Data, doc or page file | `<kebab>.<ext>` | `tools.yaml` |
| Decision record | `ADR-NNN-<kebab>.md` | `ADR-003-mobile-lane.md` |
| Python module | `ru_aibotworks_<snake>.py` | `ru_aibotworks_genome.py` |
| Agent package | fixed names | `AGENT.md`, `SKILL.md` |

`ru_aibotworks_layout.py` enforces this in the gate.

## After changing the registry

```text
python ru-aibotworks/platform/ru_aibotworks_genome.py --validate
python ru-aibotworks/platform/ru_aibotworks_generate.py
python ru-aibotworks/platform/ru_aibotworks_charter.py
python ru-aibotworks/platform/ru_aibotworks_portal.py
python ru-aibotworks/platform/ru_aibotworks_archify.py
python ru-aibotworks/platform/ru_aibotworks_seed_sql.py
```
