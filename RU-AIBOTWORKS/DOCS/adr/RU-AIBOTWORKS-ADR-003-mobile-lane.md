# RU-AIBOTWORKS-ADR-003 — Mobile lane

**Status:** Accepted · **Date:** 2026-09-14 · **Decider:** CEO Uzwal Gutta
**Author:** Enterprise AI Architect

---

## Context

The charter had two delivery lanes: Lane A (Django + React, database-backed) and Lane B
(static-first, content-heavy). Mobile had no lane. `multi-platform-apps` existed as a
plugin with four agents, but no architecture, no build pipeline and no release path.

The CEO directed that Android app building be a first-class capability, and — asked to
choose one of Kotlin/Compose, Flutter or React Native — chose **all three**.

## Decision

Add **Lane C — Mobile**, with three sub-lanes and a shared quality and release spine.

| Sub-lane | Stack | Chosen for | Windows build |
|---|---|---|---|
| **C1** | Kotlin + Jetpack Compose | Highest native UX ceiling; Material Design 3 | Android: yes |
| **C2** | Flutter (Dart 3) | One codebase Android + iOS + web | Android: yes · iOS: needs macOS |
| **C3** | React Native + Expo | Reuses the web lane's TypeScript and React skills | Android: yes |

Three stacks is a deliberate cost. It is justified by the sub-lanes serving genuinely
different client shapes, and it is bounded by a rule:

> **One sub-lane per project.** `web-architect` picks C1, C2 or C3 at the Architecture
> phase and records it in the project's `DESIGN.md`. A project never carries two.

This mirrors invariant 13 (one design generator active per build) and exists for the
same reason: two active mobile stacks in one session give the workforce contradictory
platform instructions.

### Sub-lane selection rule

| Client shape | Sub-lane |
|---|---|
| Android-only, premium UX, deep platform integration | **C1** Kotlin + Compose |
| Android and iOS from one budget | **C2** Flutter |
| Already buying our web lane, wants a mobile companion | **C3** React Native |

### The iOS limit, stated up front

Xcode is macOS-only. Lane C builds Android on Windows in all three sub-lanes. C2 and C3
write iOS-capable code but **cannot compile it here**. Any iOS deliverable requires a
macOS runner budgeted before the project starts. This is told to the client at scoping,
not discovered at release.

## Consequences

A new **Mobile Engineering** department under `web-architect`, with four teams:

| Team | Lead | Members |
|---|---|---|
| Android Native | `android-architect` | Kotlin, Compose, Material 3, performance, Play Store |
| Flutter Cross-Platform | `flutter-expert` | Dart, state management, platform channels |
| React Native Cross-Platform | `react-native-engineer` | Expo, native modules |
| Mobile Quality & Release | `mobile-qa-lead` | QA automation, accessibility, mobile security, store compliance |

Mobile adds engineers beyond the 202-strong delivery baseline. The count is computed
from the registry, not asserted here.

Three plugin-equivalents are added to the ownership map — `android-native`,
`flutter-development`, `react-native-development` — all owned by `web-architect`,
keeping plugin ownership 1:1 with an officer as invariant 5 requires.

---

## Related

- [RU-AIBOTWORKS-ADR-002](RU-AIBOTWORKS-ADR-002-organisation-structure.md) — organisation structure
- [RU-AIBOTWORKS-ADR-004](RU-AIBOTWORKS-ADR-004-compliance-posture.md) — compliance posture
