# Graph Report - ruaibotworks  (2026-09-26)

## Corpus Check
- 667 files · ~805,548 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 5, .jsonl 2, .css 2)

## Summary
- 347 nodes · 654 edges · 26 communities (16 shown, 10 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `79dbc209`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- sys
- Genome Invariant Checks
- Frontend Build Configuration
- Portal Page Rendering
- Org Chart Diagram Generator
- ru_aibotworks_registry.py
- Company
- What You Must Do When Invoked
- roster.py
- graphify reference: extra exports and benchmark
- RU-AIBOTWORKS — repo-wide instructions
- Django App Configuration
- graphify reference: query, path, explain
- Reporting Chain Depth
- School Backend Service
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- .claude/CLAUDE.md
- extraction-spec.md

## God Nodes (most connected - your core abstractions)
1. `Company` - 53 edges
2. `Genome` - 34 edges
3. `Agent` - 19 edges
4. `e()` - 14 edges
5. `main()` - 14 edges
6. `What You Must Do When Invoked` - 12 edges
7. `/graphify` - 11 edges
8. `page_hierarchy()` - 11 edges
9. `generate()` - 11 edges
10. `page_projects()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Genome` --uses--> `Company`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_genome.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `build_model()` --uses--> `Company`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_archify.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `main()` --uses--> `Company`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_archify.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `assign()` --uses--> `Company`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_names.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `main()` --uses--> `Company`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_portal.py → ru-aibotworks/platform/ru_aibotworks_registry.py

## Import Cycles
- None detected.

## Communities (26 total, 10 thin omitted)

### Community 0 - "sys"
Cohesion: 0.08
Nodes (23): is_agent(), main(), check_authorship.py — the rule that makes "engineers do not write code" real.…, sh(), check(), Path, check_consistency.py — invariant 11, enforced. Any figure appearing in two…, company.py — the single source of truth for every company figure. Invariant 11… (+15 more)

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

### Community 5 - "ru_aibotworks_registry.py"
Cohesion: 0.12
Nodes (22): argparse, dataclasses, functools, hashlib, pathlib, ru_aibotworks_genome.py — the governance genome. Validates the company against…, assign(), load_existing() (+14 more)

### Community 6 - "Company"
Cohesion: 0.07
Nodes (46): date, datetime, main(), organisation(), ru_aibotworks_charter.py — generate the charter from the registry. The charter…, roster(), start_here(), blast_radius_for() (+38 more)

### Community 7 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 8 - "roster.py"
Cohesion: 0.15
Nodes (11): main(), parse_agent(), Path, roster.py — generate the employee roster from the fork, never by hand. The…, Extract frontmatter. A file whose YAML will not parse is a defect, not a skip., render(), scan(), collections (+3 more)

### Community 9 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 10 - "RU-AIBOTWORKS — repo-wide instructions"
Cohesion: 0.33
Nodes (5): Folder structure, graphify, Project status tracking, RU-AIBOTWORKS — repo-wide instructions, Website design work

### Community 11 - "Django App Configuration"
Cohesion: 0.29
Nodes (5): django_apps, ContactConfig, AppConfig, ContentConfig, AppConfig

### Community 12 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 19 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 20 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 21 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

## Knowledge Gaps
- **62 isolated node(s):** `graphify`, `Usage`, `What graphify is for`, `Step 0 - GitHub repos and multi-path merge (only if a URL or several paths)`, `Step 1 - Ensure graphify is installed` (+57 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 147 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Company` connect `Company` to `sys`, `Genome Invariant Checks`, `Portal Page Rendering`, `Org Chart Diagram Generator`, `ru_aibotworks_registry.py`, `Reporting Chain Depth`?**
  _High betweenness centrality (0.166) - this node is a cross-community bridge._
- **Why does `Genome` connect `Genome Invariant Checks` to `Portal Page Rendering`, `ru_aibotworks_registry.py`, `Company`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Why does `build_model()` connect `Org Chart Diagram Generator` to `Company`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `Company` (e.g. with `build_model()` and `main()`) actually correct?**
  _`Company` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Agent` (e.g. with `blast_radius_for()` and `classification_for()`) actually correct?**
  _`Agent` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Usage`, `What graphify is for` to the rest of the system?**
  _62 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `sys` be split into smaller, more focused modules?**
  _Cohesion score 0.08021390374331551 - nodes in this community are weakly interconnected._