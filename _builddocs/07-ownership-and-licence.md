# Ownership and licence position

<!-- Hand-authored. Never generated. The document a client's procurement will ask for. -->

**Company:** RU AI Botworks
**CEO:** Uzwal Gutta — also recorded as Ujwal Gutta
**Fork:** `ruai-botworks/agents` (from `wshobson/agents`, MIT)
**Asset:** 214 agents, 94 plugins, 183 skills, a release gate, a signed receipt trail.

---

## The position, stated plainly

Every agent that runs in this company is owned by this company. Two hundred and
two were inherited from `wshobson/agents` under the **MIT Licence** and forked
into `ruai-botworks/agents`. Twelve were written here.

MIT grants the right to **use, copy, modify, merge, publish, distribute,
sublicense and sell**. The grant is perpetual and irrevocable. It cannot be
withdrawn, re-priced, or made conditional later. Nobody's permission is required
to run, change, rebrand, or commercialise this tree.

**The CEO holds complete authority over all 214 files.**

---

## The one condition

MIT attaches a single obligation, and it is cheap: **the copyright notice and
licence text must travel with the code.**

Concretely:

- `LICENSE` stays in the fork, with the original copyright line intact.
- If the tree is distributed or shipped inside a product, that notice goes with it.
- Attribution in a `NOTICES` file is sufficient. No royalty, no reporting, no
  approval, no share of revenue.

This is not a limit on authority. It is a line of text. Keep it and every other
right is unconditional.

---

## What is **not** covered by that grant

Four plugins arrived as external `git-subdir` entries with separate maintainers,
plus one security payload. **The main MIT grant does not extend to them.**

| Component | Status | Action required |
|---|---|---|
| `pensyve` | Separate maintainer | Verify licence before treating as owned |
| `qa-orchestra` | Separate maintainer | Verify licence — this one is **gate-blocking** |
| `ciagent` | Separate maintainer | Verify licence |
| `storymap-skill` | Separate maintainer | Verify licence |
| `hol-guard` | Reviewed external payload, pinned `43b2dda` | Verify terms. **Can modify hook and settings config** |

`dependency-steward` verifies each before it is recorded as owned. Until
verified, they are governed but not assumed — and `qa-orchestra` deserves the
most attention because it blocks promotion, which means an unverified licence
sits on the critical path to production.

This distinction is not pedantry. A client's procurement team will ask, and
"everything is MIT" is the kind of confident answer that becomes a problem later.

---

## What ownership unlocks

Three things that were impossible while the tree was external.

**1. Universal governance.** Upstream agents carry no `reports_to` and no
`decision_level`, so an external tree could never pass `genome.py`. Owned, the
frontmatter can be extended — and invariants 5 and 6 now apply to all 214.
Two hundred and two capable agents with no declared authority is not a workforce;
it is 202 agents that might each think they can decide something.

**2. The right to sell it.** MIT permits sublicensing. The fork — governance
layer, gate, receipt trail and all — can become a product in its own right, not
just the thing that builds products. That is a second business model sitting
inside the first, and it exists because of the licence, not despite it.

**3. Rebranding.** The tree can carry this company's name. There is no
requirement to present it as someone else's work, only to retain the notice.

---

## What ownership costs

Stated with equal weight, because a charter that lists only the upside is
marketing.

**You now maintain what someone else was maintaining.** The upstream tree went
from 112 to 192 agents in four months. That was free labour. Forking does not
stop it — it stops it from arriving automatically, which is the point — but every
month you do not review upstream is a month of improvements you either write
yourself or forgo.

**Every divergence is permanent.** Rewriting an upstream agent's body creates a
merge conflict that recurs forever. Rule 4 exists for this: extend by default,
rewrite by decision, log every divergence. The `[divergences]` section of
`fork.toml` is the honest measure of how much maintenance you have taken on.

**An empty divergence list is the healthy state.** It means you hold complete
authority *and* still receive upstream work for free. That is the best available
position, and it is only reachable by deliberately not exercising authority you
have.

---

## The summary a client can be shown

> Every agent that touched your project is owned and governed by RU AI Botworks under a
> perpetual MIT grant. Each carries a declared reporting line and decision level,
> validated on every build. No agent merged its own work. Every action is recorded
> in an Ed25519-signed, hash-chained audit trail you can verify offline, without
> contacting us.

That paragraph is the product. The websites are what it is attached to.

<!-- MANUAL:START id=licence-notes -->
Licence verifications completed, with dates and findings.
<!-- MANUAL:END id=licence-notes -->
