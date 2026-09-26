# Graph Report - ruaibotworks  (2026-09-26)

## Corpus Check
- 674 files · ~828,687 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 5, .jsonl 2, .css 2)

## Summary
- 560 nodes · 863 edges · 49 communities (36 shown, 13 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 47 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c08f3a40`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ru_aibotworks_registry.py
- Genome Invariant Checks
- package.json
- Portal Page Rendering
- ru_aibotworks_archify.py
- CORE DIRECTIVE: IMAGE-FIRST WEBSITE DESIGN TO CODE
- Company
- What You Must Do When Invoked
- contact/urls.py
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
- Appendix B - Canonical Sources (read these before reinventing)
- Collection
- Thinking Orbs
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- 12. THE COMBINATORIAL VARIATION ENGINE
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- 29. ANTI-AI-SLOP RULES
- tasteskill: Anti-Slop Frontend Skill
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- Web Interface Guidelines
- manage.py
- 33. DEFAULT SECTION PACKS
- 14. HERO MINIMALISM RULES
- 37. EXAMPLE INTERPRETATIONS
- 1. THE THREE DIALS (Core Configuration)
- 7. DIAL DEFINITIONS (Technical Reference)

## God Nodes (most connected - your core abstractions)
1. `Company` - 53 edges
2. `CORE DIRECTIVE: IMAGE-FIRST WEBSITE DESIGN TO CODE` - 39 edges
3. `Genome` - 34 edges
4. `Agent` - 19 edges
5. `tasteskill: Anti-Slop Frontend Skill` - 16 edges
6. `Thinking Orbs` - 16 edges
7. `Appendix B - Canonical Sources (read these before reinventing)` - 15 edges
8. `e()` - 14 edges
9. `main()` - 14 edges
10. `4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)` - 12 edges

## Surprising Connections (you probably didn't know these)
- `6.A Hardware Acceleration` --references--> `left()`  [INFERRED]
  .claude/skills/taste-skill/SKILL.md → ru-aibotworks/platform/ru_aibotworks_archify.py
- `6.A Hardware Acceleration` --references--> `top()`  [INFERRED]
  .claude/skills/taste-skill/SKILL.md → ru-aibotworks/platform/ru_aibotworks_archify.py
- `Genome` --uses--> `Company`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_genome.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `build_model()` --uses--> `Company`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_archify.py → ru-aibotworks/platform/ru_aibotworks_registry.py
- `main()` --uses--> `Company`  [INFERRED]
  ru-aibotworks/platform/ru_aibotworks_archify.py → ru-aibotworks/platform/ru_aibotworks_registry.py

## Import Cycles
- None detected.

## Communities (49 total, 13 thin omitted)

### Community 0 - "ru_aibotworks_registry.py"
Cohesion: 0.05
Nodes (51): argparse, is_agent(), main(), check_authorship.py — the rule that makes "engineers do not write code" real.…, sh(), check(), Path, check_consistency.py — invariant 11, enforced. Any figure appearing in two… (+43 more)

### Community 1 - "Genome Invariant Checks"
Cohesion: 0.11
Nodes (14): Genome, L2 is reachable only by being the declared lead of a team that exists., Orchestrators are invoked by an officer inside a phase, never by /build., No generated document may assert a headcount the registry does not compute., §10 AGT-TOOL-01 — a tool with an incomplete contract is Tier 3 and denied., §23 AGT-DES-01 — a null rollback on a Tier 2+ tool is a design finding., §34.3 — there is no autonomy level at which Tier 4 becomes automatic., A1.4 — agents get soft-delete and tombstones, never a hard-delete verb. (+6 more)

### Community 2 - "package.json"
Cohesion: 0.08
Nodes (25): @playwright/cli, react, react-dom, vite, @vitejs/plugin-react, vitest, dependencies, react (+17 more)

### Community 3 - "Portal Page Rendering"
Cohesion: 0.21
Nodes (24): discover_projects(), e(), main(), page_architecture(), page_governance(), page_hierarchy(), render(), subtree_size() (+16 more)

### Community 4 - "ru_aibotworks_archify.py"
Cohesion: 0.11
Nodes (30): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS, html (+22 more)

### Community 5 - "CORE DIRECTIVE: IMAGE-FIRST WEBSITE DESIGN TO CODE"
Cohesion: 0.06
Nodes (34): 10. IMAGE-FIRST CODEX WEBSITE WORKFLOW, 11. WHEN TO TRIGGER IMAGE GENERATION FIRST, 13. WEBSITE REFERENCE RULE, 15. RESPONSIVE FIRST-VIEW RULE, 16. ANTI-NESTED-BOX RULE, 17. REDUCE MICRO-UI CLUTTER RULE, 18. SECTION IMAGE GENERATION RULE, 19. WEBSITE IMAGE SYSTEM RULE (+26 more)

### Community 6 - "Company"
Cohesion: 0.07
Nodes (47): date, datetime, main(), organisation(), ru_aibotworks_charter.py — generate the charter from the registry. The charter…, roster(), start_here(), blast_radius_for() (+39 more)

### Community 7 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

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

### Community 26 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 27 - "Collection"
Cohesion: 0.10
Nodes (19): AI & LLM Platforms, Automotive, Awesome Claude Design, Backend, Database & DevOps, Collection, Design & Creative Tools, Developer Tools & IDEs, E-commerce & Retail (+11 more)

### Community 28 - "Thinking Orbs"
Cohesion: 0.12
Nodes (16): Announce Status Once, Basic Usage, Built-In Runtime Behavior, Choose the Size, Choose the State, Common Pitfalls, Core Contract, Handoff (+8 more)

### Community 29 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 30 - "10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)"
Cohesion: 0.20
Nodes (10): 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know), Animation Library Choice, Cards & Containers, Galleries & Media, Hero Paradigms, Layout & Grids, Micro-Interactions & Effects, Navigation & Menus (+2 more)

### Community 31 - "12. THE COMBINATORIAL VARIATION ENGINE"
Cohesion: 0.25
Nodes (8): 12. THE COMBINATORIAL VARIATION ENGINE, Background Character, Hero Architecture, Motion-Implied Language, Section System, Signature Component Set, Theme Paradigm, Typography Character

### Community 32 - "9. AI TELLS (Forbidden Patterns)"
Cohesion: 0.25
Nodes (8): 9.A Visual & CSS, 9. AI TELLS (Forbidden Patterns), 9.B Typography, 9.C Layout & Spacing, 9.D Content & Data ("Jane Doe" Effect), 9.E External Resources & Components, 9.F Production-Test Tells (banned outright), 9.G EM-DASH BAN (the single most-violated Tell)

### Community 33 - "11. REDESIGN PROTOCOL"
Cohesion: 0.29
Nodes (7): 11.A Detect the Mode (first action), 11.B Audit Before Touching, 11.C Preservation Rules, 11.D Modernisation Levers (priority order), 11.E Decision Tree: Targeted Evolution vs Full Redesign, 11.F What Never Changes Silently, 11. REDESIGN PROTOCOL

### Community 34 - "3. DEFAULT ARCHITECTURE & CONVENTIONS"
Cohesion: 0.29
Nodes (7): 3.A Stack, 3.B State, 3.C Icons, 3.D Emoji Policy, 3. DEFAULT ARCHITECTURE & CONVENTIONS, 3.E Responsiveness & Layout Mechanics, 3.F Dependency Verification (mandatory)

### Community 35 - "29. ANTI-AI-SLOP RULES"
Cohesion: 0.33
Nodes (6): 29. ANTI-AI-SLOP RULES, Content slop, Density slop, Layout slop, Typography slop, Visual slop

### Community 36 - "tasteskill: Anti-Slop Frontend Skill"
Cohesion: 0.33
Nodes (6): 13. OUT OF SCOPE, 14. FINAL PRE-FLIGHT CHECK, 2.A When to reach for a real design system (use official packages), 2.B When the brief is an aesthetic, not a system, 2. BRIEF → DESIGN SYSTEM MAP, tasteskill: Anti-Slop Frontend Skill

### Community 37 - "0. BRIEF INFERENCE (Read the Room Before Anything Else)"
Cohesion: 0.40
Nodes (5): 0.A Read these signals first, 0.B Output a one-line "Design Read" before generating, 0. BRIEF INFERENCE (Read the Room Before Anything Else), 0.C If the brief is ambiguous, ask one question, do not guess, 0.D Anti-Default Discipline

### Community 38 - "12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)"
Cohesion: 0.40
Nodes (5): 12.A File Location, 12.B Required Frontmatter, 12.C Required Body Sections, 12.D Block-Library Discipline, 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)

### Community 39 - "5. CONTEXT-AWARE PROACTIVITY"
Cohesion: 0.40
Nodes (5): 5.A Sticky-Stack - Canonical Skeleton, 5.B Horizontal-Pan - Canonical Skeleton, 5.C Scroll-Reveal Stagger - Canonical Skeleton (lighter alternative), 5. CONTEXT-AWARE PROACTIVITY, 5.D Forbidden Animation Patterns

### Community 40 - "8. DARK MODE PROTOCOL"
Cohesion: 0.40
Nodes (5): 8.A Token Strategy (pick one, stick to it), 8.B Do Not Prescribe Specific Colors Here, 8.C Default Mode, 8.D Test in Both Modes Before Finishing, 8. DARK MODE PROTOCOL

### Community 41 - "Web Interface Guidelines"
Cohesion: 0.40
Nodes (4): Guidelines Source, How It Works, Usage, Web Interface Guidelines

### Community 43 - "33. DEFAULT SECTION PACKS"
Cohesion: 0.50
Nodes (4): 12-section pack, 33. DEFAULT SECTION PACKS, 4-section pack, 8-section pack

### Community 44 - "14. HERO MINIMALISM RULES"
Cohesion: 0.50
Nodes (4): 14. HERO MINIMALISM RULES, Absolute Hero Rules, Headline Rule, Hero Cleanliness Rule

### Community 45 - "37. EXAMPLE INTERPRETATIONS"
Cohesion: 0.50
Nodes (4): 37. EXAMPLE INTERPRETATIONS, Example 1, Example 2, Example 3

### Community 46 - "1. THE THREE DIALS (Core Configuration)"
Cohesion: 0.50
Nodes (4): 1.A Dial Inference (design read → dial values), 1.B Use-Case Presets, 1.C How the Dials Drive Output, 1. THE THREE DIALS (Core Configuration)

### Community 47 - "7. DIAL DEFINITIONS (Technical Reference)"
Cohesion: 0.50
Nodes (4): 7. DIAL DEFINITIONS (Technical Reference), DESIGN_VARIANCE (Level 1-10), MOTION_INTENSITY (Level 1-10), VISUAL_DENSITY (Level 1-10)

## Knowledge Gaps
- **240 isolated node(s):** `1. ACTIVE BASELINE CONFIGURATION`, `2. MANDATORY IMAGE-FIRST RULE`, `3. GENERATE ENOUGH IMAGES RULE`, `4. CODEX-SPECIFIC SECTION IMAGE RULE`, `5. DO NOT CROP OLD IMAGES RULE` (+235 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 330 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tasteskill: Anti-Slop Frontend Skill` connect `tasteskill: Anti-Slop Frontend Skill` to `9. AI TELLS (Forbidden Patterns)`, `11. REDESIGN PROTOCOL`, `3. DEFAULT ARCHITECTURE & CONVENTIONS`, `ru_aibotworks_archify.py`, `0. BRIEF INFERENCE (Read the Room Before Anything Else)`, `12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)`, `5. CONTEXT-AWARE PROACTIVITY`, `8. DARK MODE PROTOCOL`, `1. THE THREE DIALS (Core Configuration)`, `7. DIAL DEFINITIONS (Technical Reference)`, `Appendix B - Canonical Sources (read these before reinventing)`, `4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)`, `10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)`?**
  _High betweenness centrality (0.184) - this node is a cross-community bridge._
- **Why does `6. PERFORMANCE & ACCESSIBILITY GUARDRAILS` connect `ru_aibotworks_archify.py` to `tasteskill: Anti-Slop Frontend Skill`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `Company` (e.g. with `build_model()` and `main()`) actually correct?**
  _`Company` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Agent` (e.g. with `blast_radius_for()` and `classification_for()`) actually correct?**
  _`Agent` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1. ACTIVE BASELINE CONFIGURATION`, `2. MANDATORY IMAGE-FIRST RULE`, `3. GENERATE ENOUGH IMAGES RULE` to the rest of the system?**
  _240 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ru_aibotworks_registry.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05384615384615385 - nodes in this community are weakly interconnected._
- **Should `Genome Invariant Checks` be split into smaller, more focused modules?**
  _Cohesion score 0.10569105691056911 - nodes in this community are weakly interconnected._