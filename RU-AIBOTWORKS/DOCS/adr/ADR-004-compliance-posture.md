# ADR-004 — Compliance posture

**Status:** Accepted · **Date:** 2026-09-14 · **Decided by:** Enterprise AI Architect
**Delegated by:** CEO Uzwal Gutta — *"Any Data Compliance or HIPAA, GDPR applicable the
architect should be able to decide or create bots for that."*

---

## Context

RU-AIBOTWORKS sells ten website templates built to order. The product is provable build
quality. Two distinct compliance surfaces exist and are routinely conflated:

1. **Company surface** — we operate a fleet of credentialed agents. STD-AGENT-001,
   ISO/IEC 42001 and the EU AI Act apply to *us*, regardless of what we build.
2. **Client surface** — what a delivered template must satisfy depends entirely on the
   template. A restaurant site and a healthcare portal are not the same regulatory object.

Applying every regime to every project is the failure mode that makes compliance
ceremonial. Applying none until audit is the failure mode that makes it fatal.

## Decision

Compliance obligations attach **per project at scoping**, from a fixed matrix, and the
matrix is enforced by the gate rather than remembered.

### Company-level — always in force

| Regime | Why it applies | Owner |
|---|---|---|
| **STD-AGENT-001** | We run tool-using agents with credentials | `platform-architect` |
| **ISO/IEC 42001** | AI management system: roles, lifecycle, review cadence | `quality-compliance` |
| **EU AI Act Art. 14, 12, 19** | Human oversight, record-keeping, log retention — adopted voluntarily; most internal build agents are not Annex III high-risk | `quality-compliance` |
| **GDPR** | We process personal data of clients and site visitors | `data-protection-officer` |
| **OWASP Top 10 for Agentic Applications 2026** | The vocabulary security review will use | `security-engineer` |
| **WCAG 2.2 AA** | House standard on every delivered interface | `design-owner` |

### Project-level — attaches by template

| Template | Regimes | Triggering officer |
|---|---|---|
| School | GDPR · WCAG 2.2 AA · child-data care | `data-protection-officer` |
| Corporate | GDPR · WCAG 2.2 AA | `data-protection-officer` |
| Portfolio | GDPR (contact form only) · WCAG 2.2 AA | `data-protection-officer` |
| Restaurant | GDPR · WCAG 2.2 AA | `data-protection-officer` |
| Booking | GDPR · WCAG 2.2 AA | `data-protection-officer` |
| **Healthcare** | **HIPAA** · GDPR · WCAG 2.2 AA | `data-protection-officer` + `quality-compliance` |
| **E-commerce** | **PCI DSS 4.0 (SAQ-A)** · GDPR · WCAG 2.2 AA | `security-engineer` |
| LMS | GDPR · WCAG 2.2 AA · accessibility of media | `design-owner` |
| SaaS dashboard | GDPR · SOC 2 readiness · WCAG 2.2 AA | `quality-compliance` |
| CRM | GDPR · SOC 2 readiness · WCAG 2.2 AA | `data-protection-officer` |

### Two standing engineering rules

**PCI DSS — integrate, never implement.** Card data does not enter our systems. Stripe or
PayPal hosted fields only, keeping the client in SAQ-A scope. A project that would place
a PAN in our database is declined or rescoped. `security-engineer` holds this line and it
is a veto matter.

**HIPAA — PHI never enters an agent context window.** The healthcare template is built
against synthetic fixtures. A Business Associate Agreement is a client-side prerequisite
we do not assume. Agents on a HIPAA project run with `max_tier: 2` and no egress beyond
the allowlist. This is the §6.1 three-factor rule applied concretely: a session with PHI
scope gets no untrusted content and no outbound channel.

## The bots

Compliance is staffed, not documented. A **Data Protection Office** department is created
under `data-protection-officer` with three teams:

| Team | Agents |
|---|---|
| Privacy Engineering | `gdpr-compliance-officer`, `hipaa-compliance-officer`, `dpia-assessor` |
| Data Subject Rights & Records | `data-subject-rights-handler`, `records-of-processing-curator`, `breach-notification-coordinator` |
| Residency & Retention | `data-residency-analyst`, `retention-policy-enforcer` |

`breach-notification-coordinator` exists because of a clock: GDPR Art. 33 gives 72 hours
from awareness. HIPAA's Breach Notification Rule gives 60 days. A clock that nobody owns
is a clock that runs out. Each agent's registration record carries its `incident_clocks`
field per §34.1.

## Consequences

Compliance becomes a gate input rather than a document. Each project's `DESIGN.md` and
registration records name the applicable regimes; the gate fails a project whose template
implies a regime not listed. A project cannot quietly become a healthcare project.

The cost is real: HIPAA and PCI projects carry a heavier review load and a lower autonomy
ceiling. That is priced at scoping, not absorbed at build.

---

## Related

- [ADR-002](ADR-002-organisation-structure.md) — organisation structure
- [ADR-005](ADR-005-agent-anatomy.md) — agent anatomy
