# School template design

## Build decision

- Lane: A - Django + React
- Scope: public informational site first; portal deferred
- Active design generator: `ui-design`
- Standard: [`premium-web-design-standard`](../../../designs/premium-web-design-standard.md) v1
- Domain brief: [`school-design-brief`](../../../designs/school/school-design-brief.md)

## Design direction

Calm, welcoming academic visual system with clear hierarchy, high-contrast
text, generous spacing, responsive layouts, visible focus states, and semantic
landmarks — implemented per the school design brief's homepage architecture,
color direction, and motion tiers.

**Status:** `frontend/src/App.jsx` and `styles.css` predate this standard and
still reflect the earlier minimal direction (single-viewport hero, no scroll
motion, no section rhythm). They have not yet had the design-refresh pass —
`product-design-lead` and `ui-designer` owe this template a rebuild against
the brief before it is shown to a client as the reference school template.

## Safety constraints

Do not include minors' personal data in public content. Portal work requires a
separate authentication, authorization, retention, consent, and audit phase.
