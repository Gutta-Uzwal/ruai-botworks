# Engineering roster standard

<!-- Hand-authored. The rules. The roster itself is generated. -->

## Why this document exists and the roster does not

The upstream catalogue documents **105 of its 202 agents**. `docs/agents.md`
opens with "all 202 local specialized AI agents" and its model distribution table
sums to 202 — Fable 2, Opus 54, Sonnet 70, Haiku 24, Inherit 52 — while the
category tables beneath it name 105. Roughly 97 engineers exist in the tree and
appear in no document.

They cannot be documented by transcription, because there is nothing to
transcribe from. They are documented by **enumeration**: `scripts/roster.py`
walks the fork, reads every agent's frontmatter, assigns a reporting line from
the plugin it lives in, and writes the roster. Whatever is in the tree is in the
roster. The count is discovered, never asserted.

This is the same principle the previous company used for `genome.py` —
*"extracted from the agent files, not maintained by hand, so it cannot drift from
what the org actually is."* Applied here to 202 engineers instead of 86.

---

## What every engineer must have

No agent runs without all six. Missing any one is a build failure, not a warning.

| Field | Source | Meaning |
|---|---|---|
| `name` | frontmatter | Unique across the company. Collisions are defects |
| `description` | frontmatter | The responsibility. What this engineer is for |
| `model` | frontmatter | Cost tier — `fable`, `opus`, `sonnet`, `haiku`, `inherit` |
| `plugin` | directory | Where it lives. Determines its officer |
| `reports_to` | assignment rules | Exactly one officer. Never a peer |
| `decision_level` | assignment rules | `L1` unless deliberately promoted and logged |

---

## Roles: what each level may do

| Level | Held by | May decide | May not |
|---|---|---|---|
| **L5** | CEO — human, 1 | Commercial direction, veto override | Ship code |
| **L4** | `cto` — 1 | Triage size, dispatch, off-stack proposals | Override a veto |
| **L3** | 7 officers | Anything binding their function | Cross into another function |
| **L2** | 5 officers | One named call each | Anything outside that call |
| **L1** | **every engineer — ~202** | Implementation approach inside an assigned task | Decide scope, merge, or ship |

**Every inherited engineer is L1 by default.** This is the rule that turns 202
capable agents into an organisation. An agent with no declared authority is not
neutral — it is an agent that might assume it has some. Declaring them all L1 and
promoting only by logged, deliberate act is what makes the hierarchy real rather
than decorative.

Promotion requires: an officer's request, a written reason, a date, and an entry
in `[promotions]` in `fork.toml`. `genome.py` fails the build on any L2+ engineer
absent from that list.

---

## Responsibilities by function

What "doing the job properly" means for each group of engineers.

### Build — Web · `web-architect` · 34 engineers
Implement inside a chosen lane. The lane is not theirs to pick. They produce
candidates, never merges, and stop at the first thing that needs an architectural
decision rather than inventing one.
*Contains:* language specialists (`python-pro`, `typescript-pro`, `golang-pro`,
`rust-pro`, `java-pro`…), framework specialists (`django-pro`, `fastapi-pro`,
`frontend-developer`), platform specialists (`flutter-expert`, `ios-developer`),
and the declined domains held but not dispatched.

### Build — Data · `data-architect` · 17 engineers
Schema, pipelines, models. **Grain discipline is the standing responsibility** —
grain errors are the most expensive defect class in the catalogue and the hardest
to reverse after launch. No engineer here changes a schema without an ADR.

### Build — Platform · `platform-architect` · 13 engineers
Environments, deployment, observability, and the policy plane. Responsible for
the audit-mode → enforcement transition on Cedar, and for the standing rule that
**no gate job depends on a service the company does not operate.**

### Direct — Design · `design-owner` · 4 engineers
Render what `DESIGN.md` decides. They do not choose the aesthetic family; that is
a CEO-approved decision. Their responsibility is fidelity to it, and flagging when
a requested design would produce a sibling of an existing template.

### Direct — Product · `product-owner` · 16 engineers
Content, SEO, business analysis, customer communication. The largest non-code
group. Responsible for everything a client reads rather than runs.

### Verify — Testing · `testing-architect`
Produce evidence, not opinions. A test that passes because of state left by the
previous run is a defect, so **isolated profiles always.** Responsible for keeping
advisory checks advisory — a flaky blocker teaches people to bypass the gate.

### Verify — Review · `merge-authority`
**Read-only.** No `Write`, no `Edit`, enforced by Cedar policy with a signed
receipt per call. Responsible for the one decision nobody else makes. A reviewer
who can silently fix what it found leaves no review behind.

### Verify — Security · `security-engineer`
Vulnerability assessment, threat modelling, secure coding review. Holds a veto.
Responsible for verifying the receipt chain offline.
**Never assigned Fable tier** — its cyber and bio safety classifiers fall back to
Opus on security content anyway, so the premium buys nothing.

### Verify — Compliance · `quality-compliance`
Accessibility, legal, HR, regulatory evidence. Holds a veto. Produces evidence;
the *authority* to say "this does not ship" rests with the officer, never the
engineer.

### Ship — Docs and release · `release-manager`
Documentation regenerates from what shipped. Responsible for routing failures to
the owning officer rather than fixing them — a release manager who fixes is a
release manager who is no longer neutral about whether to ship.

### Ship — Dependencies · `dependency-steward`
Fork log, pins, certification, Tier C teardown. The standing responsibility
nobody enjoys: **removal.** Reviews quarterly whether each plugin still earns its
context cost.

---

## Assignment rules

Every one of the 94 plugins maps to exactly one officer, which is what makes
placement of all 202 deterministic. An unmapped plugin **fails the build** rather
than defaulting somewhere convenient.

| Officer | Plugins owned |
|---|---|
| `web-architect` | 22 — backend, frontend, mobile, all 10 language plugins, payments, migration, cleanup, debugging |
| `platform-architect` | 13 — cloud, k8s, deployment, CI/CD, observability, incident, policy plane |
| `data-architect` | 12 — databases, data engineering, ML/LLM, performance |
| `product-owner` | 10 — SEO ×3, content, social, business ×3, sales, story mapping |
| `release-manager` | 8 — git/PR, deployment validation, all documentation plugins |
| `testing-architect` | 6 — unit testing, QA, ciagent, perf review, TDD, error debugging |
| `security-engineer` | 4 — scanning, API security, frontend/mobile security, reverse engineering |
| `quality-compliance` | 4 — security compliance, accessibility, HR/legal, review governance |
| `design-owner` | 4 — UI design, AI design, landing pages, decks |
| `dependency-steward` | 4 — plugin-eval, dependency management, memory, context |
| `cto` | 4 — orchestration plugins. **Invoked inside a phase, never as entry point** |
| `merge-authority` | 3 — comprehensive review, conductor, skill forge |

---

## Generating the roster

```bash
# writes the full roster for every engineer in the tree
python scripts/roster.py --fork .claude/plugins --out docs/charter/08-employee-roster.md

# gate mode — exits non-zero on any defect
python scripts/roster.py --fork .claude/plugins --validate
```

Wire `--validate` into the repository gate family alongside `genome.py`.

### What the gate catches

Tested against a 106-agent tree with defects deliberately injected. All four were
caught and the build failed:

| Defect | Why it matters |
|---|---|
| **No frontmatter** | The agent **silently never loads**. Nothing errors anywhere |
| **Unquoted colon in `description`** | YAML reads it as a mapping. This is the exact defect that hid three reviewers in the previous company |
| **Unmapped plugin** | An engineer with no officer is an engineer nobody is accountable for |
| **Ungoverned agent** | Missing `reports_to` after assignment — invariant 5 |

The colon check earned its place during testing: it caught a description *this
document's author* mistyped while transcribing. The defect class is not
hypothetical and it is not rare.

---

## Two things to resolve at fork time

**1. Name collision on `code-reviewer`.** The workforce contains an engineer
called `code-reviewer` (opus, `comprehensive-review`). The officer holding merge
authority was also called `code-reviewer`. **The officer is renamed
`merge-authority`** throughout, and the assignment rules already reflect it. Two
agents with one name, holding different authority, makes the single most
important decision in the company ambiguous.

**2. The second Fable agent.** The model table declares Fable 2; only
`legacy-modernizer` is documented. Fable runs roughly **2.6× the cost of Opus**
($10/$50 per MTok plus a ~30% heavier tokenizer). Run
`grep -rl 'model: fable' .claude/plugins` and record both in `fork.toml` with an
explicit opt-in, or neither runs.

---

## The check that closes the gap

```bash
# what the docs claim vs what exists
find .claude/plugins -path '*/agents/*.md' | wc -l
```

If that number is not what the roster reports, the generator found something the
documentation did not — which is the entire point of generating it.

<!-- MANUAL:START id=roster-standard-notes -->
Promotions granted, collisions resolved, engineers retired.
<!-- MANUAL:END id=roster-standard-notes -->
