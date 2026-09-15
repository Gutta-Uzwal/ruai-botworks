# Build from scratch — step by step

**RU AI Botworks · CEO Uzwal Gutta (alias Ujwal Gutta)**

<!-- Hand-authored. Start here with an empty folder and a terminal. -->

Every command, in order. Nothing assumed, nothing skipped. Steps are numbered
continuously so you can say "I'm stuck on 14" and it means one thing.

**Before anything: read the rule.** Every stage ends with a change promoted to
`main` through the full gate. Not "installed" — promoted. A stage that ends with
software installed and nothing shipped has proved nothing.

---

## Stage 0 — Machine ready

**Step 1.** Install the prerequisites.

```bash
node --version      # need 18+   → playwright, mermaid-cli, hooks
python3 --version   # need 3.12+
git --version
gh --version        # GitHub CLI
```

**Step 2.** Install `uv` — the upstream fork uses it, not pip.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

**Step 3.** Confirm Claude Code is 2.1+ (plugin marketplace needs it).

```bash
claude --version
```

**Step 4.** Note the hard limit now, not later: **iOS cannot build on Windows.**
Xcode is macOS-only. If you intend to sell native iOS, budget a macOS runner
today. Otherwise Flutter is your Apple path.

> **Stage 0 exits when** all five commands above return a version.

---

## Stage 1 — Repository skeleton

**Step 5.** Create the repository.

```bash
mkdir ruai-botworks && cd ruai-botworks && git init
git branch -M main
git checkout -b uat && git checkout -b dev
```

Three branches mirroring environments: `dev` → `uat` → `main`.

**Step 6.** Create the structure.

```bash
mkdir -p .claude/{agents,standards/{company,functions},plugins,policy/cedar,commands}
mkdir -p scripts projects/_shared docs/charter .github/workflows
```

**Step 7.** Protect `main` and `uat` immediately. This is the first thing that
must be true, because everything downstream assumes nothing reaches production by
hand.

```bash
gh api -X PUT repos/:owner/:repo/branches/main/protection \
  -f required_pull_request_reviews[required_approving_review_count]=1 \
  -F enforce_admins=true -F restrictions=null
```

> **Stage 1 exits when** a direct `git push origin main` is rejected.

---

## Stage 2 — The thirteen officers

Write these before installing anything. They are the company; everything else is
staff.

**Step 8.** Write thirteen files in `.claude/agents/`. Nothing else goes in that
directory, ever.

| File | Level | Reports to | Decides |
|---|---|---|---|
| `cto.md` | L4 | CEO | Triage size, dispatch, off-stack proposals |
| `product-owner.md` | L3 | cto | What "done" means |
| `design-owner.md` | L3 | cto | Aesthetic family, owns `DESIGN.md` |
| `web-architect.md` | L3 | cto | Lane A or Lane B, structure, API shape |
| `data-architect.md` | L3 | cto | Schema, grain, retention, contracts |
| `platform-architect.md` | L3 | cto | CI, environments, Cedar policy |
| `testing-architect.md` | L3 | cto | Quality bar, blocking vs advisory |
| `quality-compliance.md` | L3 | cto | Non-conformance blocks release — **VETO** |
| `merge-authority.md` | L2 | testing-architect | Whether this merges — **READ-ONLY** |
| `security-engineer.md` | L2 | platform-architect | Vulnerabilities — **VETO** |
| `sre.md` | L2 | platform-architect | Production instability — **VETO** |
| `release-manager.md` | L2 | platform-architect | Promotion and routing |
| `dependency-steward.md` | L2 | platform-architect | Pins, certification, teardown |

**Step 9.** Frontmatter shape. Get this exactly right — a malformed agent
**silently never loads** and raises no error anywhere.

```markdown
---
name: merge-authority
description: "Decides whether work merges. Read-only: holds no Write or Edit."
model: opus
tools: [Read, Grep, Glob]
reports_to: testing-architect
decision_level: L2
---
You decide whether this merges. Nobody else makes that call.
...
```

**Note the quotes around `description`.** That field contains a colon. Unquoted,
YAML reads it as a mapping and the agent never loads. This exact defect hid three
reviewers in a previous build, and it is invisible on inspection.

**Step 10.** Name check. Do **not** call the reviewer `code-reviewer` — the
workforce you are about to install already contains an agent with that name.
Two agents, one name, different authority makes the single most important
decision in the company ambiguous. It is `merge-authority`.

**Step 11.** Write the source of truth and its self-check.

```bash
cp scripts/company.py scripts/        # officers, plugin ownership, all figures
python3 scripts/company.py            # must print 13 officers, 215 agents, 3 vetoes
```

> **Stage 2 exits when** `company.py` self-check passes with **exactly 3 vetoes**
> and no inverted authority.

---

## Stage 3 — Prove the machine runs

**The stage everyone skips, and the reason most agent companies never ship.**

**Step 12.** Write `scripts/genome.py` asserting the first four invariants:
reporting lines resolve, authority never inverts, exactly three vetoes, the
reserved-decision list has not shrunk.

**Step 13.** Write the minimal gate.

```yaml
# .github/workflows/uat-gate.yml
on: { push: { branches: [uat] } }
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/company.py
      - run: python3 scripts/genome.py --validate
  promote:
    needs: gate                    # depends on SUCCESS, not a pass percentage
    runs-on: ubuntu-latest
    steps:
      - run: gh pr merge --merge uat-to-main
```

**Step 14.** Push one trivial change — a typo — all the way through.

```bash
git checkout dev && echo "." >> docs/charter/00-START-HERE.md
git commit -am "typo" && git push origin dev
gh pr create --base uat --head dev && gh pr merge --merge
```

> **Stage 3 exits when** all of these are true:
> - `/build` triaged it as XS and did **not** run a full lifecycle
> - Every gate job reported **success**, not "mostly passed"
> - Promotion happened without anyone pushing to `main`
> - `genome.py --validate` passed

**If Stage 3 fails, stop.** Fix the pipeline before installing anything. Adding
202 engineers to a pipeline that has never completed one lap means debugging two
unknowns at once.

---

## Stage 4 — Fork and own the workforce

**Step 15.** Register the marketplace. This loads nothing into context.

```bash
claude
/plugin marketplace add wshobson/agents
```

**Step 16.** Fork and vendor. MIT permits this outright and permanently.

```bash
gh repo fork wshobson/agents --org <your-org> --fork-name agents --clone=false
git clone https://github.com/<your-org>/agents .claude/plugins
cd .claude/plugins && git checkout <commit-sha> && cd -   # NEVER "main"
```

**Step 17.** Keep the licence. This is the single condition on complete
authority — retain `LICENSE` and the original copyright line. No royalty, no
reporting, no approval.

**Step 18.** Verify the four external plugins separately. They are **not**
covered by the main MIT grant: `pensyve`, `qa-orchestra`, `storymap-skill`,
`ciagent`, plus the `hol-guard` payload. Check `qa-orchestra` first — it is
gate-blocking, so an unverified licence sits on your path to production.

**Step 19.** Find both Fable-tier agents before one runs quietly. Fable costs
roughly **2.6× Opus** ($10/$50 per MTok plus a ~30% heavier tokenizer).

```bash
grep -rl 'model: fable' .claude/plugins
```

**Step 20.** Create `fork.toml` recording origin, your fork, the pin, promotions
(empty), divergences (empty), and external licences.

> **Stage 4 exits when** the gate fails on a deliberately unpinned entry.

---

## Stage 5 — Govern all 215

**Step 21.** Generate the roster from the tree, not from upstream docs. The
catalogue documents 105 of its 202 agents; the rest exist and are nameless.

```bash
python3 scripts/roster.py --fork .claude/plugins --out docs/charter/08-employee-roster.md
python3 scripts/roster.py --fork .claude/plugins --validate
```

**Step 22.** Confirm the count came from the filesystem.

```bash
find .claude/plugins -path '*/agents/*.md' | wc -l
```

If that disagrees with the roster, the generator found something the docs did
not — which is the entire point of generating it.

**Step 23.** Every engineer defaults to **L1**. Promotion requires an officer's
request, a written reason, a date, and an entry in `[promotions]` in `fork.toml`.

**Step 24.** Add invariants 5–12 to `genome.py`, and wire
`check_consistency.py` into the gate.

> **Stage 5 exits when** every agent in the tree has `reports_to` and
> `decision_level`, and an ungoverned agent fails the build.

---

## Stage 6 — Install Tier A, certified

**Step 25.** Install the twelve corrected Tier A plugins. **This list is
corrected** — the README's example structure is wrong about where `django-pro`
lives.

```bash
/plugin install api-scaffolding          # django-pro, fastapi-pro  ← Lane A backbone
/plugin install python-development       # python-pro
/plugin install javascript-typescript    # javascript-pro, typescript-pro
/plugin install multi-platform-apps      # frontend-developer, ui-ux-designer
/plugin install backend-development      # backend-architect, tdd-orchestrator
/plugin install database-design          # database-architect, sql-pro
/plugin install comprehensive-review     # architect-reviewer, security-auditor
/plugin install ui-design                # ui-designer, accessibility-expert
/plugin install observability-monitoring # performance-engineer, database-optimizer
/plugin install codebase-cleanup         # test-automator  ← the only test generator
/plugin install security-scanning        # threat-modeling-expert
/plugin install git-pr-workflows
```

**Installing `python-development` alone does not give you Django.** `django-pro`
and `fastapi-pro` live in `api-scaffolding`. Similarly `frontend-developer` is in
`multi-platform-apps`, and `test-automator` is in `codebase-cleanup`.

**Step 26.** Certify everything before first use.

```bash
/plugin install plugin-eval
uv run plugin-eval certify .claude/plugins/plugins/api-scaffolding
```

Record every certification ID against its pin in `fork.toml`.

> **Stage 6 exits when** one real change, built by a forked engineer, reviewed by
> `merge-authority` and promoted through the gate, has reached `main`.

---

## Stage 7 — Governance and policy

**Step 27.** Install the governance tier.

```bash
/plugin install protect-mcp review-agent-governance block-no-verify dependency-management
```

**Step 28.** Run `protect-mcp` in **audit mode** — receipts on, enforcement off —
for one full template build.

```toml
[policy]
mode = "audit"
```

**Step 29.** Read the receipts. Then write Cedar policy from what the agents
actually did.

**Policy written ahead of evidence is either ceremony or an obstacle, and
obstacles get loosened under deadline.** That is how every policy system dies.

**Step 30.** Prove the enforcement works.

```bash
# merge-authority must be unable to write, with a receipt proving it
# block-no-verify must reject a --no-verify attempt
git commit --no-verify -m "test"      # expect: blocked
```

> **Stage 7 exits when** the receipt chain verifies **offline**, and a client
> could be handed it.

---

## Stage 8 — Design and QA

**Step 31.** Install the design and QA tier.

```bash
# in-fork generators — already pinned and certified with the fork
/plugin install ui-design brand-landingpage

# second ecosystem — pin, certify and licence-check separately
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "school education" --design-system -p "School"

/plugin install qa-orchestra ciagent      # external — pin and certify separately
```

**Step 31a.** Verify the `ui-ux-pro-max` licence before any client work. Listings
note its content cannot be previewed due to licence restrictions, and a
non-commercial licence would make it unusable here. `web-compliance-engineer`
owns this gate.

**Step 31b.** Record the chosen generator in each project's `DESIGN.md` and
enforce invariant 13 — one active per build.

**Step 32.** Make `DESIGN.md` a gated phase. Invariant 10: no project without one.

**Step 33.** `qa-orchestra` blocks. **`ciagent` is advisory and must stay
advisory** — golden-trace diffing against non-deterministic models produces false
positives, and a flaky blocker teaches people to bypass the gate.

**Step 34.** Playwright with an isolated profile, always. The default persistent
profile means a test can pass because of state left by the previous run.

> **Stage 8 exits when** two templates from different aesthetic families **do not
> look like siblings.** That is the real test of the design layer.

---

## Stage 9 — First template

**Step 35.** Build School, hybrid scope: informational to production first, the
portal second. A portal is an authn/authz and data-protection project wearing a
website costume, and that is not where you learn your own pipeline.

> **Stage 9 exits when** you could show a client both the site **and** the signed
> receipt trail.

---

## Stage 10 — Templates 2 to 10

**Step 36.** Follow the order. It is load-bearing.

| # | Template | Lane | Why here |
|---|---|---|---|
| 2 | Corporate | A | Proves template reuse |
| 3 | Portfolio | B | Design proving ground, no database |
| 4 | Restaurant | B | Static-first survives Core Web Vitals |
| 5 | **Booking** | A | **Keystone — three templates inherit its time-slot engine** |
| 6 | Healthcare | A | Heaviest regulatory load |
| 7 | E-commerce | A | Integrate payments, never implement |
| 8 | LMS | A | Video and completion tracking are bigger than they look |
| 9 | SaaS dashboard | A | Multi-tenancy is an ADR before any code |
| 10 | CRM | A | Consumes every ladder rung |

**Step 37.** Build each rung of the reuse ladder **once**, into
`projects/_shared/`: Shell → Content → Accounts → Time slots → Commerce →
Dashboards.

**Step 38.** `dependency-steward` uninstalls Tier C after every template. This is
the step everyone skips and the reason context budgets rot.

---

## Timeline

| Stage | Duration | Cumulative |
|---|---|---|
| 0–1 Machine and skeleton | 1 session | — |
| 2 Thirteen officers | 2–4 sessions | ~1 week |
| 3 **Prove the machine runs** | 1–3 sessions | ~1.5 weeks |
| 4 Fork and own | 2–3 sessions | ~2 weeks |
| 5 Govern all 215 | 2–3 sessions | ~2.5 weeks |
| 6 Tier A certified | 3–5 sessions | ~3.5 weeks |
| 7 Governance and policy | 4–7 sessions | ~5 weeks |
| 8 Design and QA | 3–5 sessions | ~6 weeks |
| 9 First template | 1–2 weeks | ~8 weeks |
| 10 Templates 2–10 | 6–10 weeks | **~14–18 weeks** |

**Three to four months.** Compress by running Stages 5 and 8 in parallel. Extend
if Stage 3 reveals a lifecycle gap, which is the most likely outcome and the most
valuable.

Anyone promising this in two weeks is describing installation, not a company.

---

## The five things that will go wrong

1. **Stage 3 fails and reveals a lifecycle gap.** Most likely, most valuable.
   Fix before installing anything.
2. **Cedar policy written from imagination.** Agents stall, someone loosens it
   under deadline, the policy system dies. Audit mode exists to prevent this.
3. **`ciagent` false positives erode trust in the gate.** Keep it advisory.
4. **Tier C never gets uninstalled.** Watch the weekly context baseline.
5. **The ten templates look like siblings.** Catch it at Stage 8's exit
   criterion, not at template eight.

---

## Done

The company is running when this is true:

```
You:  /build "restaurant site for Client X"
      cto triages → design-owner drafts → you approve the design
      → architects dispatch forked engineers → every call signed
      → merge-authority blocks once → you approve the merge
      → nine job families green → promoted → docs regenerate
      → Tier C uninstalled
You:  [two decisions. Nothing else.]
```

Two decisions per template build. Reachable in about three months.

<!-- MANUAL:START id=build-log -->
Actual stage durations, and what went wrong.
<!-- MANUAL:END id=build-log -->
