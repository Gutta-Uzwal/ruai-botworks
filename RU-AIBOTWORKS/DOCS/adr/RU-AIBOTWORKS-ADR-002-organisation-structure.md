# RU-AIBOTWORKS-ADR-002 — Organisation structure

**Status:** Accepted · **Date:** 2026-09-14 · **Decider:** CEO Uzwal Gutta
**Author:** Enterprise AI Architect

---

## Context

The company had 13 officers, all on the delivery line under `cto`. The CEO directed that
HR, Payroll, Finance and Service Management be added.

Three constraints bound the answer:

- **Invariant 3** — exactly three standing vetoes, held by the same officers. Adding a
  fourth veto is a build failure.
- **Invariant 2** — authority never inverts across a reporting line.
- **The two-decision target** — a full template build should reach the CEO twice. Every
  new direct report to the CEO erodes that.

A fourth constraint came from the Standard: §33 names *AI governance / risk* and
*Data / backup owner* as accountable roles the 13 officers only partly covered, and
GDPR Art. 38(3) requires a Data Protection Officer to report to the highest management
level and to receive no instructions on how to perform the role.

## Decision

Add six officers. Thirteen becomes nineteen.

```
CEO · Uzwal Gutta · L5
├── cto · L4 ─────────────────── DELIVERY
│   ├── product-owner · L3
│   ├── design-owner · L3
│   ├── web-architect · L3
│   ├── data-architect · L3
│   ├── platform-architect · L3
│   ├── testing-architect · L3
│   ├── quality-compliance · L3 · VETO
│   ├── merge-authority · L2 · READ-ONLY   (via testing-architect)
│   ├── security-engineer · L2 · VETO      (via platform-architect)
│   ├── sre · L2 · VETO                    (via platform-architect)
│   ├── release-manager · L2               (via platform-architect)
│   └── dependency-steward · L2            (via platform-architect)
│
├── coo · L4 ─────────────────── CORPORATE            ← NEW
│   ├── hr-director · L3                              ← NEW
│   ├── payroll-controller · L3                       ← NEW
│   ├── finance-controller · L3                       ← NEW
│   └── service-management-lead · L3                  ← NEW
│
└── data-protection-officer · L3 ── INDEPENDENT       ← NEW
```

### Why a COO rather than more reports to the CTO

Payroll meters what delivery spends. Putting it under `cto` makes a delivery officer the
controller of its own cost — the same structural defect standing rule 10 already names
("The CEO cannot be the one who ships"). Corporate functions need a line that does not
run through the person under delivery pressure.

### Why the DPO reports to the CEO

GDPR Art. 38(3). The DPO must be independent of the functions it assesses and must reach
the highest management level directly. Routing it through `coo` or `cto` would make the
role advisory in name and subordinate in fact.

### Why the DPO holds no veto

`quality-compliance` already holds the compliance veto. Under GDPR the DPO advises,
monitors and reports — it does not hold an operational stop button. The division is:

> **DPO raises the finding. `quality-compliance` blocks the release. Only the CEO unblocks.**

Vetoes stay at exactly three. Invariant 3 holds unchanged.

## Team layer

Officers previously had up to 34 direct reports. A team layer is inserted:

```
Officer (L3) → Team Lead (L2, promoted and logged) → Engineers (L1)
```

Team leads are **deliberate promotions** under the existing mechanism — an officer's
request, a written reason, a date, an entry in the promotions register. Invariant 6 is
satisfied by using it as designed rather than by exempting anyone from it. A team lead
coordinates and sequences; it still cannot decide scope, merge, or ship.

## Consequences

| Figure | Before | After |
|---|---|---|
| Officers | 13 | **19** |
| L4 chiefs | 1 | **2** |
| L3 officers | 7 | **12** |
| L2 named authorities | 5 | 5 |
| Standing vetoes | 3 | **3** — unchanged |
| CEO direct reports | 1 | **3** (`cto`, `coo`, `data-protection-officer`) |
| Reserved CEO decisions | 4 | 4 — unchanged |

The CEO gains one corporate escalation path and one independent privacy channel, and
keeps the four reserved decisions untouched. The two-decision-per-build target is
unaffected: neither `coo` nor the DPO sits on the `/build` path.

---

## Related

- [RU-AIBOTWORKS-ADR-001](RU-AIBOTWORKS-ADR-001-agent-construction-model.md) — agent construction model
- [RU-AIBOTWORKS-ADR-003](RU-AIBOTWORKS-ADR-003-mobile-lane.md) — mobile lane
