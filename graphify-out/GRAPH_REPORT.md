# Graph Report - ruaibotworks  (2026-09-26)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 277 nodes · 595 edges · 19 communities (13 shown, 6 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.95)
- Token cost: 79,155 input · 2,223 output

## Graph Freshness
- Built from commit: `b3948092`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Authorship & Consistency Checks
- Genome Invariant Checks
- Frontend Build Configuration
- Portal Page Rendering
- Org Chart Diagram Generator
- Agent Harness Validation
- Agent Package Generation
- Company Charter Generation
- SQL Seed Data Generation
- Agent Registry Core Model
- Agent Reporting Hierarchy
- Django App Configuration
- Officer Registry Lookup
- Reporting Chain Depth
- School Backend Service

## God Nodes (most connected - your core abstractions)
1. `Company` - 53 edges
2. `Genome` - 34 edges
3. `Agent` - 19 edges
4. `e()` - 14 edges
5. `main()` - 14 edges
6. `page_hierarchy()` - 11 edges
7. `generate()` - 11 edges
8. `page_projects()` - 10 edges
9. `phead()` - 10 edges
10. `shell()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Genome` --uses--> `Company`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_genome.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `blast_radius_for()` --uses--> `Agent`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_generate.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `classification_for()` --uses--> `Agent`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_generate.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `clocks_for()` --uses--> `Agent`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_generate.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `grants_for()` --uses--> `Agent`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_generate.py → ru-aibotworks/platform/ru_aibotworks_registry.py

## Import Cycles
- None detected.

## Communities (19 total, 6 thin omitted)

### Community 0 - "Authorship & Consistency Checks"
Cohesion: 0.06
Nodes (37): argparse, is_agent(), main(), check_authorship.py — the rule that makes "engineers do not write code" real.…, sh(), check(), Path, check_consistency.py — invariant 11, enforced. Any figure appearing in two… (+29 more)

### Community 1 - "Genome Invariant Checks"
Cohesion: 0.11
Nodes (14): Genome, L2 is reachable only by being the declared lead of a team that exists., Orchestrators are invoked by an officer inside a phase, never by /build., No generated document may assert a headcount the registry does not compute., §10 AGT-TOOL-01 — a tool with an incomplete contract is Tier 3 and denied., §23 AGT-DES-01 — a null rollback on a Tier 2+ tool is a design finding., §34.3 — there is no autonomy level at which Tier 4 becomes automatic., A1.4 — agents get soft-delete and tombstones, never a hard-delete verb. (+6 more)

### Community 2 - "Frontend Build Configuration"
Cohesion: 0.08
Nodes (23): react, react-dom, vite, @vitejs/plugin-react, vitest, dependencies, react, react-dom (+15 more)

### Community 3 - "Portal Page Rendering"
Cohesion: 0.21
Nodes (24): discover_projects(), e(), main(), page_architecture(), page_governance(), page_hierarchy(), render(), subtree_size() (+16 more)

### Community 4 - "Org Chart Diagram Generator"
Cohesion: 0.16
Nodes (23): html, build_model(), bottom(), left(), right(), top(), e(), elbow() (+15 more)

### Community 5 - "Agent Harness Validation"
Cohesion: 0.16
Nodes (13): django_http, django_urls, hashlib, json, load_json(), main(), Any, Path (+5 more)

### Community 6 - "Agent Package Generation"
Cohesion: 0.21
Nodes (14): clocks_for(), digest(), generate(), main(), ru_aibotworks_generate.py — emit every agent package from the registry. Per…, Return a map of relative path -> content. Nothing is written here., The runtime-reachable tool registry, at the repository root. Only grantable…, render_agent_tools_json() (+6 more)

### Community 7 - "Company Charter Generation"
Cohesion: 0.28
Nodes (7): main(), organisation(), ru_aibotworks_charter.py — generate the charter from the registry. The charter…, roster(), start_here(), Company, Any

### Community 8 - "SQL Seed Data Generation"
Cohesion: 0.27
Nodes (12): blast_radius_for(), classification_for(), grants_for(), A bound with a number. §34.1: "we would have to investigate" is not a blast…, render_registration(), build(), main(), merge() (+4 more)

### Community 9 - "Agent Registry Core Model"
Cohesion: 0.18
Nodes (10): dataclasses, date, datetime, functools, pathlib, as_of(), _load(), The registry's edition date. Generators use this, never date.today(). (+2 more)

### Community 10 - "Agent Reporting Hierarchy"
Cohesion: 0.22
Nodes (6): claude_tools_for(), The Claude Code tool list implied by the grant. Read-only agents never get…, render_agent_md(), Agent, An engineer reports to its team lead, and a lead to its department officer.…, One non-officer agent. Its level is computed, never declared.

### Community 11 - "Django App Configuration"
Cohesion: 0.29
Nodes (5): django_apps, ContactConfig, AppConfig, ContentConfig, AppConfig

### Community 12 - "Officer Registry Lookup"
Cohesion: 0.29
Nodes (3): main(), main(), Officer

## Knowledge Gaps
- **15 isolated node(s):** `ruai-school-backend`, `react`, `react-dom`, `vite`, `@vitejs/plugin-react` (+10 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 89 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Company` connect `Company Charter Generation` to `Authorship & Consistency Checks`, `Genome Invariant Checks`, `Portal Page Rendering`, `Org Chart Diagram Generator`, `Agent Package Generation`, `SQL Seed Data Generation`, `Agent Registry Core Model`, `Agent Reporting Hierarchy`, `Officer Registry Lookup`, `Reporting Chain Depth`?**
  _High betweenness centrality (0.262) - this node is a cross-community bridge._
- **Why does `Genome` connect `Genome Invariant Checks` to `Authorship & Consistency Checks`, `Portal Page Rendering`, `Officer Registry Lookup`, `Company Charter Generation`?**
  _High betweenness centrality (0.219) - this node is a cross-community bridge._
- **Why does `build_model()` connect `Org Chart Diagram Generator` to `Agent Registry Core Model`, `Company Charter Generation`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `Company` (e.g. with `build_model()` and `main()`) actually correct?**
  _`Company` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Agent` (e.g. with `blast_radius_for()` and `classification_for()`) actually correct?**
  _`Agent` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ruai-school-backend`, `react`, `react-dom` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Authorship & Consistency Checks` be split into smaller, more focused modules?**
  _Cohesion score 0.05803921568627451 - nodes in this community are weakly interconnected._