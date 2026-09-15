# Premium web design standard

Every DESIGN.md, on every project and every template, must declare compliance
with this standard by name and version: `Standard: premium-web-design-standard v1`.
This is the Design gate `design-owner` holds. A DESIGN.md that does not name
this standard does not pass the gate.

This file is the single source. Do not copy its text into an agent prompt, a
DESIGN.md, or a skill file — reference it by path so there is one place to
update and every agent reads the current version.

## What "premium" means here

The delivered site must read as art-directed, not generated: a visitor could
not tell it apart from a $50k agency build. It is not a card grid, not a
gradient blob, not a Bootstrap layout with the class names changed.

## 1. Before any code: five questions

`product-design-lead` answers these in DESIGN.md before `ui-designer` or any
web engineer starts implementation:

1. Who is the audience, and what should they feel in the first 5 seconds?
2. What is the one primary action this page exists to produce?
3. What is the visual story across the scroll — what does the visitor
   discover, in what order?
4. What makes this build different from a thousand others in the same
   category?
5. Where are the 1–3 signature "wow moments," and where does the page
   deliberately stay calm?

## 2. Design system, decided once

Define before building any page, as tokens (`--color-*`, `--font-*`,
`--space-*`, `--radius-*`, `--shadow-*`):

- **Typography** — one display family, one body family, a real size scale
  with dramatic hierarchy (not every heading the same weight and size).
- **Spacing** — a fixed scale, not ad hoc `17px` / `23px` values.
- **Color** — primary, secondary, accent, background, surface, text, muted
  text, border, success/warning/error. A real palette, not the default
  purple-blue-pink AI gradient unless the brand calls for it.
- **Grid** — 12-column desktop / 8 tablet / 4 mobile, with content aligned
  across sections.

## 3. Motion has three tiers, not one

- **Micro** — button/link/icon hover, card lift, image zoom. Fast, subtle.
- **Section** — scroll-triggered reveal, staggered content, counters,
  timeline progression.
- **Signature** — 1–3 major moments per site only (hero reveal, a large
  interactive visual, a cinematic transition). Everything animating is the
  same as nothing animating.

Use `transform`/`opacity` for performant animation. Respect
`prefers-reduced-motion` — reduce, don't remove, the design.

## 4. Section rhythm

No two consecutive sections may share the same layout shape (two-column,
two-column, two-column is a defect). Alternate background treatment
(light → tinted → full-bleed image → dark) so the scroll has visual rhythm,
not a uniform white page broken only by text.

## 5. The anti-generic-AI checklist

Before calling a build done, `design-owner` checks the rendered page against
this list and rejects anything found:

- Gradient blobs / excessive glassmorphism
- Every card and container at the same border-radius
- Three-identical-cards as the default section shape
- Shadows on everything instead of spacing/contrast/type doing the work
- Filler copy ("revolutionary," "empowering," generic Lorem ipsum)
- Identical layout repeated across 3+ sections
- A hero that is centered text + button on a plain background

## 6. Responsive and accessibility gate

Test at 1440 / 1280 / 1024 / 768 / 430 / 390 / 375px — each tier is a
deliberate composition, not a shrunk desktop layout. Ship semantic HTML,
full keyboard navigation, visible focus states, alt text, contrast that
passes, and `prefers-reduced-motion` support. None of this is optional or
deferred to a later pass.

## 7. Self-critique before shipping

`design-owner` runs this pass on every build, and a build that fails it goes
back to `ui-designer`/`web-architect`, not to review:

- **Blur test** — blur the page; is there still one clear focal point?
- **5-second test** — who, what, why-trust, what's-next, all readable in
  5 seconds on the hero?
- **Scroll test** — does the page down read as introduction → discovery →
  proof → experience → differentiation → action, or as section-section-section?
- **Agency test** — "what would a professional creative director change?" —
  apply one visible refinement pass before declaring done.

## Domain briefs

A domain-specific brief narrows this standard for one vertical's emotional
goals, color direction, and page architecture. It never replaces this
standard — it sits alongside it. See `Design/<domain>/` for the brief that
matches the current build's domain (e.g.
[`school/school-design-brief.md`](school/school-design-brief.md)). If no
brief exists yet for a domain, `product-design-lead` writes one as part of
that project's DESIGN.md work, and it becomes the standing brief for every
later build in that domain.
