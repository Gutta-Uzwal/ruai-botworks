# RU-AIBOTWORKS — build plan v2

**CEO Uzwal Gutta (alias Ujwal Gutta)** · supersedes `_builddocs/01-BUILD-FROM-SCRATCH.md`

<!-- The original build plan remains in _builddocs as the historical input. It is
     correct about the gate and wrong about where the workforce comes from — see
     ADR-001. This document is the plan we are executing. -->

Every figure below is computed by `PLATFORM/ru_aibotworks_registry.py`.
None is typed by hand.

---

## What changed from v1

| | v1 | v2 | Why |
|---|---|---|---|
| Workforce source | fork `wshobson/agents` | **built natively from a registry** | The fork was never vendored, and forked agents carry no registration record, blast radius or tool contract. See [ADR-001](adr/ADR-001-agent-construction-model.md). |
| Officers | 13 | **19** | HR, Payroll, Finance, Service Management and an independent DPO, under a new COO. See [ADR-002](adr/ADR-002-organisation-structure.md). |
| Lanes | A, B | **A, B, C1, C2, C3** | Android is now first-class, in all three stacks. See [ADR-003](adr/ADR-003-mobile-lane.md). |
| Compliance | implied | **matrix, attached per template** | See [ADR-004](adr/ADR-004-compliance-posture.md). |
| Structure | officer → 34 engineers | **officer → team lead → engineers** | 34 direct reports is not an organisation. |
| Control database | none | **SQL Server `RU_AIBOTWORKS`** | The org, the contracts, the trajectory log, the meter. |

The rule that has not changed: **every stage ends with a change promoted to `main`
through the full gate.** A stage that ends with something installed and nothing shipped
has proved nothing.

---

## Stage status

| Stage | What it delivers | Status |
|---|---|---|
| 0 | Machine ready | ✅ done |
| 1 | Repository skeleton | ✅ done |
| 2 | The officers | ✅ **19 written and generated** |
| 3 | Prove the machine runs | ⬜ **next — do not skip** |
| 4 | The registry and the generator | ✅ done |
| 5 | Govern every agent | ✅ done — 24 genome checks green |
| 6 | The control database | ✅ done — schema and seed loaded |
| 7 | Governance and policy | ⬜ audit mode, then Cedar from receipts |
| 8 | Design and QA | ⬜ |
| 9 | First template — School | ⬜ |
| 10 | Templates 2–10 | ⬜ |
| **11** | **Human Resources** | ✅ **registry built** · ⬜ operating |
| **12** | **Payroll** | ✅ **registry built** · ⬜ metering live |
| **13** | **Finance** | ✅ **registry built** · ⬜ budgets enforced |
| **14** | **Service Management** | ✅ **registry built** · ⬜ desk open |
| **15** | **Data Protection Office** | ✅ **registry built** · ⬜ DPIA run |
| **16** | **Mobile — Lane C** | ✅ **registry built** · ⬜ first app |

---

## Stage 3 — Prove the machine runs

**The stage everyone skips, and the reason most agent companies never ship.**

Nothing below Stage 3 matters until one trivial change has travelled `dev` → `uat` →
`main` through every gate job. Adding 259 agents to a pipeline that has never completed
one lap means debugging two unknowns at once.

```bash
# 1. The genome must be green before anything is pushed
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_genome.py --validate

# 2. Generated output must not be stale
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_generate.py --check

# 3. Push one typo all the way through
git checkout dev
echo "." >> RU-AIBOTWORKS/DOCS/charter/01-start-here.md
git commit -am "typo" && git push origin dev
gh pr create --base uat --head dev && gh pr merge --merge
```

> **Stage 3 exits when** every gate job reports **success** — not "mostly passed" —
> promotion happened without anyone pushing to `main`, and `cto` triaged the change as XS
> without running a full lifecycle.

---

## Stage 11 — Human Resources

**Officer:** `hr-director` (L3, reports to `coo`) · **8 staff** · 3 teams

This is not metaphorical HR. STD-AGENT-001 §34 makes registration, change management, the
autonomy ladder and a review cadence mandatory. Each needs an owner, and an unowned
lifecycle control is a control that has already lapsed.

| Team | Owns |
|---|---|
| Agent Lifecycle | Registration records, onboarding, tool grants, decommission, credential revocation |
| Capability & Training | Skills curricula, competence assessment, the autonomy ladder |
| Performance & Records | Agreement rates, evaluation outcomes, the workforce record of truth |

**Steps.**

1. **Registration records exist for all 278 agents.** Already generated — one
   `REGISTRATION.yaml` per agent, each carrying a blast radius that is a number and a
   bound. `agent-registrar` owns them from here.
2. **Wire the review clock.** Every record carries `review_due` 182 days out. A lapsed
   review **suspends** the agent; it does not produce a warning that somebody notes.
3. **Stand up the autonomy ladder.** Every agent starts at L0-propose-only or
   L1-supervised. `autonomy-ladder-assessor` promotes only on: agreement rate above
   threshold over a statistically useful sample, a clean evaluation suite, and no policy
   violation in the window.
4. **Write the decommission runbook.** `agent-offboarding-specialist` revokes, then
   **proves the revoked credential no longer works.** A revoke call returning success is
   not evidence.

> **Stage 11 exits when** one agent has been registered, promoted one rung, and
> decommissioned — with the credential revocation verified by test, not by assertion.

---

## Stage 12 — Payroll

**Officer:** `payroll-controller` (L3, reports to `coo`) · **6 staff** · 2 teams

An AI company's payroll is tokens and wall clock. If it is not metered per agent, the
company does not know what any part of it costs.

| Team | Owns |
|---|---|
| Metering | Per-agent token and agent-hour accounting, allocated to project and client |
| Payroll Operations | Rate cards, period close, statements, reconciliation to the provider invoice |

**Steps.**

1. **Meter every run.** `ops.AgentRun` and `fin.MeterEntry` are already in the database.
   Tokens are attributed to the agent that spent them **including its sub-agents**.
2. **Load the rate card.** Seeded from the registry: Opus 5/25, Sonnet 3/15, Haiku 1/5,
   Fable 10/50 per MTok. Rates are versioned by effective date so a historical period
   recosts to what it actually cost.
3. **Flag the premium tier explicitly.** Fable is roughly 2.6× Opus. A premium tier used
   quietly is the expensive kind.
4. **Reconcile monthly.** `payroll-reconciliation-auditor` explains every variance against
   the provider invoice. An unexplained variance is a meter defect or a leak — never an
   accounting nuisance.

> **Stage 12 exits when** one period closes with `fin.vw_PayrollByAgent` fully reconciled
> and the variance explained in writing.

---

## Stage 13 — Finance

**Officer:** `finance-controller` (L3, reports to `coo`) · **8 staff** · 3 teams

| Team | Owns |
|---|---|
| Financial Planning & Analysis | Budgets, forecasts, cost per template built |
| Controlling | Cost governance, spend anomaly detection, procurement and licence spend |
| Revenue & Billing | Client billing, revenue recognition, margin per engagement |

**Steps.**

1. **Every budget names its enforcement point.** `fin.Budget` has a CHECK constraint
   refusing any row whose `OnExhaustion` is not `halt` or `halt_and_escalate`. A budget
   that warns and continues is not a budget, so the database will not store one.
2. **Set the six dimensions** per agent and per project: steps, tokens, cost, wall clock,
   mutations, fan-out.
3. **Baseline before capping.** `spend-anomaly-detector` alerts on deviation from an
   agent's *own* baseline; absolute thresholds miss a cheap agent going wrong.
4. **Measure unit economics.** Cost per template **including rework** — the second attempt
   is part of the unit cost.

> **Stage 13 exits when** a test run exhausts each budget dimension and **halts** rather
> than warning or retrying, with the halt visible in `ops.AgentRun.HaltedByBudget`.

---

## Stage 14 — Service Management

**Officer:** `service-management-lead` (L3, reports to `coo`) · **10 staff** · 4 teams

The service layer between clients and delivery. The division of labour with Site
Reliability is deliberate and must stay clear:

> **Service Management coordinates and communicates. SRE executes and stops things.**

| Team | Owns |
|---|---|
| Service Desk | Intake, triage and fulfilment of every client request |
| Incident & Problem | Business-side incident coordination, root-cause elimination, known errors |
| Change & Release Governance | Change calendar, risk assessment, **the freeze windows the policy plane reads** |
| Service Level & Catalogue | SLA definition, measurement, reporting, the service catalogue |

**Steps.**

1. **Publish the catalogue, including what we decline.** `svc.CatalogueItem` requires a
   reason on anything not offered, so a salesperson cannot promise a declined domain by
   accident.
2. **Only commit to SLAs you measure today.** `svc.Sla` refuses a row with
   `IsMeasuredToday = 0`. An unmeasured SLA is a promise nobody can keep or disprove.
3. **Make the freeze window machine-readable.** `svc.ChangeFreeze` is what
   `change_freeze.active` resolves against in every tool contract. The most-cited industry
   incident happened during a freeze that existed only in a calendar invitation.
4. **Close against evidence.** `svc.Request` requires `ClosureEvidence` before `ClosedAt`
   can be set. Nothing is closed for age.
5. **Start the regulatory clock at awareness.** `major-incident-commander` opens
   `svc.BreachClock` and tells the DPO in the same minute.

> **Stage 14 exits when** a client request, an incident and a change have each been run
> end to end, and a declared freeze has actually blocked a `release.promote`.

---

## Stage 15 — Data Protection Office

**Officer:** `data-protection-officer` (L3, **reports to the CEO directly**) · **8 staff** · 3 teams

Independent of every function it assesses, per GDPR Art. 38(3). It holds **no veto**: it
raises findings, and `quality-compliance` blocks on them. Read-only throughout — an
assessor that can edit what it assesses is not independent.

| Team | Owns |
|---|---|
| Privacy Engineering | GDPR and HIPAA assessment, DPIA, privacy by design |
| Data Subject Rights & Records | DSAR handling, Art. 30 records, **the breach clocks** |
| Residency & Retention | Cross-border transfer, residency, enforced retention |

**Steps.**

1. **Build the Article 30 record** before any client work. Knowing where a person's data
   lives after the request arrives is too late — the clock has already started.
2. **Run a DPIA on the Healthcare and CRM templates** before either is built.
3. **Two standing engineering rules**, both enforced rather than documented:
   - **PCI DSS — integrate, never implement.** Hosted fields only, SAQ-A scope. A project
     that would put a card number in our database is rescoped or declined.
   - **HIPAA — PHI never enters a context window.** Healthcare builds run on synthetic
     fixtures, agents capped at `max_tier: 2`, no egress beyond the allowlist.
4. **Own the clocks.** GDPR Art. 33 gives 72 hours from awareness; HIPAA's Breach
   Notification Rule gives 60 days. A clock nobody owns is a clock that runs out.

> **Stage 15 exits when** a DPIA is on file for the Healthcare template and a simulated
> breach has exercised the 72-hour clock end to end, including the awareness timestamp
> being defensible.

---

## Stage 16 — Mobile, Lane C

**Officer:** `web-architect` (L3) · **17 engineers** · 4 teams

Three stacks, **one per project, never two** — the same constraint as the design
generator, for the same reason.

| Sub-lane | Stack | Chosen when |
|---|---|---|
| **C1** | Kotlin + Jetpack Compose | Android-only, premium UX, deep platform integration |
| **C2** | Flutter / Dart 3 | Android and iOS from one budget |
| **C3** | React Native + Expo | Client already buying the web lane |

**Steps.**

1. **Add Lane C to the gate.** `gradle test` / `flutter test` / `jest`, plus the device
   matrix, as blocking jobs.
2. **Pick the device matrix from the client's real user base**, not from popularity
   charts, and profile on a low-end device rather than a flagship.
3. **State the iOS limit at scoping.** Xcode is macOS-only. All three sub-lanes build
   Android on Windows; C2 and C3 write iOS-capable code they cannot compile here. An iOS
   deliverable needs a macOS runner budgeted before the project starts.
4. **Store nothing sensitive on device.** Keystore only, no secrets in the bundle, and
   accept that a shipped app is a decompiled app.

> **Stage 16 exits when** one Android app is built in **each** of C1, C2 and C3, and the
> three do not look like siblings — the same anti-sameness test the web lanes face.

---

## The standing commands

```bash
# the source of truth, computed
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_registry.py --table

# the harness — 24 checks over every agent
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_genome.py --validate --verbose

# regenerate every agent package, and sync officers into .claude/agents/
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_generate.py

# fail if anything generated is stale — this is the gate's version
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_generate.py --check

# rebuild the CEO portal
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_portal.py

# rebuild and load the control database
python RU-AIBOTWORKS/PLATFORM/ru_aibotworks_seed_sql.py
sqlcmd -S localhost -E -C -b -i RU-AIBOTWORKS/DATABASE/seed.sql
```

**To hire an agent:** add ~12 lines to a file in `REGISTRY/workforce/`,
run the genome, run the generator. Its charter, registration record, tool contracts,
evaluation contract, skills, database rows and portal entry all follow. There is no
second place to edit.

---

## The five things that will go wrong

1. **Stage 3 is skipped because everything else is already built.** It is the one stage
   whose absence you discover at the worst moment. Do it next.
2. **Cedar policy written from imagination.** Run `protect-mcp` in audit mode for one full
   template build first. Policy written ahead of evidence becomes an obstacle, and
   obstacles get loosened under deadline.
3. **The corporate departments become documentation.** HR, Payroll, Finance and Service
   Management are built in the registry and not yet *operating*. A department that exists
   only as agent files is an org chart, not a function.
4. **Three mobile stacks become three half-maintained stacks.** One sub-lane per project,
   and `dependency-steward` tears down what the project did not use.
5. **The generated tree gets hand-edited.** Someone fixes a typo in an `AGENT.md` instead
   of the registry, and the next generation silently reverts it. `--check` in the gate is
   what catches this.
