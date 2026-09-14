# CEO operating manual

**RU AI Botworks · Uzwal Gutta (alias Ujwal Gutta)**

<!-- Hand-authored. Never generated. -->

## Your job

Four decisions. Everything else is delegated to twelve officers commanding 202
staff.

| Decision | Frequency | Where it happens |
|---|---|---|
| **What to build** | Per engagement | `/build` |
| **Whether the design is right** | Per template | Design gate — you approve `DESIGN.md` |
| **Whether to override a veto** | Rare, and should stay rare | Escalation |
| **Off-stack technology** | Rare | `cto` proposes, you approve |

If you find yourself making a fifth kind of decision regularly, an officer is
missing or under-specified. Treat it as an org signal, not a workload problem.

---

## The veto discipline

Three officers can stop a release. You are the only override. This is the most
consequential power you hold and the easiest to erode.

**Before overriding, ask three questions:**

1. Is the finding wrong, or merely inconvenient? Overriding a correct finding
   because of a deadline is how the gate stops meaning anything.
2. What changes so this does not recur? An override without a follow-up is a
   decision to accept the same block next month.
3. Would you show the client the receipt trail for this release? If the answer is
   no, that is your answer.

**Record every override.** Date, veto holder, finding, reason, follow-up. If the
log grows, the gate is miscalibrated and `testing-architect` or
`platform-architect` needs to hear it. A veto overridden three times is a rule
nobody believes.

---

## Capacity

The real constraint is not agents. It is **you**, because two gates need your
signature.

| Running in parallel | Your load | Verdict |
|---|---|---|
| 1 template | ~2 decisions/day | Comfortable |
| 2 templates | ~4 decisions/day | Sustainable |
| 3 templates | ~6 decisions/day | Ceiling — design approval starts getting rubber-stamped |
| 4+ | — | You become the bottleneck, and the design gate silently degrades |

**Three concurrent templates is the ceiling** until you delegate design approval,
and design approval is the last thing to delegate because it is the
differentiation.

Second constraint: Tier C plugin contention. Two templates needing different Tier
C sets means `dependency-steward` is installing and uninstalling constantly.
Schedule same-lane templates together where possible.

---

## What drives cost

| Driver | Control | Owner |
|---|---|---|
| Model tier per officer | Opus only for reviewers, vetoes, architects | You, once |
| Context baseline | Tier C uninstalled between projects | `dependency-steward` |
| Rework loops | Design gate catching problems before Build | `design-owner` |
| Tier 0 (Fable 5) | Opt-in only, for multi-hour migrations | `cto` proposes |
| Plugin sprawl | Certification required before install | `dependency-steward` |

The largest single lever is the third row. A problem caught at the Design gate
costs one decision; the same problem caught at Verify costs a full Build cycle
across multiple agents and a full dispatch cycle.

**Measure one number weekly:** baseline context tokens per session. If it climbs
month over month, Tier C is not coming out, and that is the leading indicator
that discipline has slipped.

---

## Weekly rhythm

| When | What | Who |
|---|---|---|
| Monday | Pick the week's templates. Check the override log | You |
| Any day | Approve `DESIGN.md` per template | You |
| Any day | Approve merges | You |
| Friday | Pin review: any upstream bumps? Recertify | `dependency-steward` |
| Friday | Context baseline check | `dependency-steward` |
| Monthly | `ciagent` drift review — has agent behaviour changed? | `dependency-steward` |
| Quarterly | Is any Tier A plugin still earning its place? | `dependency-steward` |

That last row is the one nobody does. Removal is the step every agent stack
skips, and it is the difference between a stack that stays fast and one that
rots.

---

## Commercial shape

Not pricing advice — structural observations about where margin lives.

**The differentiator is the receipt trail.** Everyone sells AI-written code.
Almost nobody can hand a client an Ed25519-signed, hash-chained,
offline-verifiable record of every action taken on their project. Lead with that
in regulated verticals — healthcare, education, finance — where it converts from
a nice-to-have into a procurement requirement.

**Margin compounds down the reuse ladder.** Template one costs the most; template
eleven should cost a fraction, because it is a recombination of rungs already
built. If it does not, the shared layer was never properly extracted. That is a
build problem showing up as a margin problem.

**The decline list protects margin.** Every row in it is an engagement that would
have consumed disproportionate time. "Any engagement where the gate cannot run"
is the important one: without the gate you are selling commodity code at
commodity rates.

---

## Red flags

Ordered by how quietly they arrive.

| Flag | Means | Act |
|---|---|---|
| Two templates look like siblings | `DESIGN.md` is decorative | Stop. Fix before template five |
| You approved a merge without reading the review | The Verify gate is theatre | Slow down or reduce parallelism |
| Override log growing | Gate miscalibrated | `testing-architect` recalibrates |
| Context baseline climbing | Tier C not uninstalled | `dependency-steward` |
| `ciagent` flips ignored | Agent behaviour drifting unnoticed | Review before the next pin bump |
| An orchestrator answered `/build` | **Invariant 8 broken** | Stop immediately. This is the boundary |

The last row is the one that turns your company back into someone else's.

---

## The obligation that replaces it

There is no longer a scenario where the workforce is taken away. MIT is perpetual
and irrevocable, the fork is on disk, and no permission is needed from anyone.

What replaces that worry is maintenance. You now own 202 agents that someone else
used to maintain, and the upstream tree grew from 112 to 192 agents in four
months. Walking away from that cadence entirely means writing those improvements
yourself; accepting it blindly means an unreviewed tree feeding an auto-promoting
pipeline.

The middle path is rule 4 — **stay mergeable.** Company frontmatter uses keys
upstream does not, so merges stay clean. Extend by default; rewrite by decision.
Every rewritten agent body is a divergence you have chosen to maintain forever,
and `dependency-steward` logs each one.

Review upstream monthly, not continuously. Certify what you accept. The point of
owning it is that the timing is yours.

---

## The sentence to keep

**You own all 214. What you own, you govern. The gate is the product.**

<!-- MANUAL:START id=ceo-notes -->
Override log, capacity observations, cost notes.
<!-- MANUAL:END id=ceo-notes -->
